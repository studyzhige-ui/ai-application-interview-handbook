# 08. Tool Schema、Validation 与 Structured Result

`AGENT-022`（Structured Output / Tool Arguments Validation）在冻结 HUMAN-A 中有 **11 个独立来源**；它通常不会单独出现，而是接在 `AGENT-018` Tool Calling、`AGENT-020` Tool Failure 后面继续追。

很多候选人会说：

> “Function Calling 有 JSON Schema，所以参数一定是对的。”

这是一个典型误区。

Schema 能约束**形状**，但 Production Runtime 仍然必须处理：

```text
语法合法但语义错误
字段缺失
枚举错误
路径越界
资源不存在
版本不兼容
模型 hallucination
外部 Tool schema 漂移
Tool Result 不符合预期
```

---

# 1. 先讲人话：Structured ≠ Correct

假设 Tool：

```text
create_ticket(title, priority, assignee)
```

模型生成：

```json
{
  "title": "login bug",
  "priority": "P1",
  "assignee": "alice"
}
```

JSON 是合法的。

但仍然可能：

```text
P1 这个项目不允许模型自行创建
alice 已离职
当前 tenant 没有 alice
title 太短
用户没有创建权限
```

所以 Validation 至少有多层：

```text
Parse
→ Schema Validation
→ Semantic Validation
→ Policy Validation
→ Execution-time Validation
```

---

# 2. 五层 Validation 模型

## 2.1 Syntax / Parse

最基础：

```text
是不是合法 JSON？
```

错误：

```json
{"path": "a.py",}
```

Runtime 应该得到明确错误：

```text
invalid_json
```

而不是让底层 Tool 随机崩溃。

---

## 2.2 Schema Validation

例如：

```json
{
  "type": "object",
  "properties": {
    "path": {"type": "string"},
    "start_line": {"type": "integer", "minimum": 1}
  },
  "required": ["path"],
  "additionalProperties": false
}
```

可以检查：

- required；
- type；
- enum；
- range；
- pattern；
- additional fields。

---

## 2.3 Semantic Validation

Schema 合法：

```json
{"start_line": 100, "end_line": 20}
```

类型都对，但：

```text
start_line > end_line
```

属于语义错误。

又比如：

```json
{"currency": "USD", "amount": -100}
```

Schema 如果没写 minimum，仍然可能不合理。

---

## 2.4 Runtime / Resource Validation

参数可能完全合法，但环境不满足：

```text
文件不存在
branch 不存在
ticket 已删除
database connection unavailable
MCP server disconnected
```

这些只能在运行时检查。

---

## 2.5 Policy Validation

即使参数和资源都正确：

```text
这个用户是否允许执行？
这个 tenant 是否允许访问？
这个路径是否在 writable root？
这个 action 是否需要 approval？
```

这是 Permission / Policy，不应混成 Schema。

---

# 3. Runtime Validation Pipeline

一个实用链路：

```text
Raw Model Tool Call
      ↓
Parse
      ↓
Canonicalize / Normalize
      ↓
Schema Validate
      ↓
Semantic Validate
      ↓
Registry / Version Check
      ↓
Permission / Policy
      ↓
Execute
      ↓
Validate / Normalize Result
      ↓
Model-visible Tool Result
```

这里最重要的是：

> **不要让未校验的模型参数直接穿透到高风险执行层。**

---

# 4. 用 Pydantic 做最小示例

```python
from pathlib import Path
from pydantic import BaseModel, Field, model_validator


class ReadFileArgs(BaseModel):
    path: str = Field(min_length=1)
    start_line: int = Field(default=1, ge=1)
    end_line: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_range(self):
        if self.end_line is not None and self.start_line > self.end_line:
            raise ValueError("start_line must be <= end_line")
        return self


def validate_workspace_path(args: ReadFileArgs, workspace: Path) -> Path:
    target = (workspace / args.path).resolve()
    root = workspace.resolve()

    if root not in target.parents and target != root:
        raise ValueError("path escapes workspace")

    return target
```

这里已经有三层：

```text
Pydantic type/schema
→ cross-field semantic validation
→ workspace policy-like path boundary
```

实际 Production 里最后一层通常会放到更专门的 Policy / Sandbox 层。

---

# 5. 为什么不要依赖模型“自己修 JSON”

一种坏设计：

```text
参数解析失败
→ 把原字符串再交给模型
→ “请修正 JSON”
→ 无限循环
```

更合理：

```text
1. Runtime 先确定错误类别
2. 能 deterministic 修复的先本地修复
3. 需要模型重生成时，返回结构化 validation error
4. 设置 repair budget
5. 重复失败则改路或终止
```

例如：

```json
{
  "ok": false,
  "error_type": "invalid_arguments",
  "issues": [
    {
      "field": "start_line",
      "message": "must be <= end_line"
    }
  ],
  "repairable": true
}
```

模型下一轮更容易修正。

---

# 6. Repair 不是 Retry

这两个词面试里很容易混。

```text
Retry
= 用相同或近似相同输入再次执行

Repair
= 修改 Tool Call / 参数后重新执行
```

例如：

```text
HTTP 503
→ Retry

path="src/ap.py" 不存在
→ 先 search → Repair path
```

又比如：

```text
schema 缺 required field
→ Repair arguments
```

这个区分会直接影响 Runtime Policy。

---

# 7. 不要把所有 Validation Error 都给模型看

错误信息可能包含：

- Secret；
- internal path；
- SQL；
- stack trace；
- infrastructure metadata。

所以最好分：

```text
Internal Error
vs
Model-visible Error
```

例如内部：

```text
PermissionDenied: /home/prod/.aws/credentials
```

给模型：

```json
{
  "error_type": "permission_denied",
  "message": "requested path is outside allowed workspace"
}
```

既能指导 Repair，又避免泄露敏感边界。

---

# 8. Tool Result 为什么也要 Validation

大家通常只验证输入，不验证输出。

但外部 Tool / MCP Server 可能返回：

```text
字段缺失
类型变化
超大 Payload
不可信文本
恶意 Prompt Injection
```

所以 Result Pipeline 也可以有：

```text
Raw Result
→ Parse
→ Schema / Type Check
→ Size Limit
→ Security / Redaction
→ Normalize
→ Context Projection
```

特别是外部 MCP Server，更不能默认：

> “Server 返回的内容一定可信。”

---

# 9. Structured Result 的推荐形状

教学上可以统一：

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ToolError(BaseModel):
    type: str
    message: str
    retryable: bool = False
    repairable: bool = False


class ToolResult(BaseModel, Generic[T]):
    ok: bool
    data: T | None = None
    error: ToolError | None = None
    artifact_ref: str | None = None
    truncated: bool = False
```

这样模型和 Runtime 都能稳定理解：

```text
成功 / 失败
是否可 Retry
是否应 Repair
大结果是否被外部化
```

---

# 10. Schema 要不要写得越复杂越好？

不一定。

复杂 Schema 会增加：

- 模型生成难度；
- Token Cost；
- Versioning 成本；
- Compatibility 风险。

例如一个 Tool 有 40 个可选字段：

```text
模型可能经常选错字段组合
```

可以考虑拆成：

```text
search_ticket
update_ticket
close_ticket
```

而不是：

```text
manage_ticket(action, 40 params...)
```

Tool 粒度与 Schema 复杂度是联动的。

---

# 11. Enum 的 Trade-off

Schema：

```json
{"priority": {"enum": ["low", "medium", "high"]}}
```

优点：

- 约束模型；
- Runtime 简单；
- Eval 清楚。

缺点：

- 后端新增 `critical` 时，Schema 版本需要同步；
- 外部系统动态值不适合硬编码。

所以动态资源更适合：

```text
先 discovery / lookup
→ 得到 valid IDs
→ 再调用 write Tool
```

---

# 12. Tool Schema Versioning

假设 v1：

```json
{
  "query": "..."
}
```

v2：

```json
{
  "query": "...",
  "scope": "repo"
}
```

如果只是新增 optional field，兼容性相对好。

但如果：

```text
rename field
change enum
change semantic meaning
```

旧 Trace / Eval Dataset / Resume Session 可能出问题。

常见策略：

```text
1. additive changes first
2. aliases / migration
3. versioned tool name only when necessary
4. old version deprecation window
5. eval old cases before cutover
```

---

# 13. Codex 对“错误是否返回模型”的显式区分

固定源码：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/tools/src/function_call_error.rs` 直接定义：

```text
RespondToModel(String)
Fatal(String)
```

这是一个非常值得学习的 Runtime 区分：

```text
可作为 Observation 反馈给模型的调用错误
vs
破坏 Runtime invariant、应该中止的 fatal error
```

例如 Codex `router.rs` 解析 `tool_search` 参数失败时，会构造 `RespondToModel`；而 Tool Payload 类型与 Runtime 不兼容时可以走 Fatal。

这正好支持前面的 Repair / Fail 分层。

---

# 14. Codex Router 的 Schema / Parse 证据

`codex-rs/core/src/tools/router.rs` 的 `build_tool_call()` 会把协议层 `ResponseItem` 归一化成内部 `ToolCall`：

```text
FunctionCall
ToolSearchCall
CustomToolCall
→ ToolCall { tool_name, call_id, payload }
```

对 client-side `ToolSearchCall`，它显式做 `serde_json::from_value(...)`，解析失败时返回对模型可见的错误。

课程抽象：

> **Provider / Protocol Output 不能直接穿透 Tool Handler；应该先归一化为 Runtime 内部类型。**

---

# 15. Claude Code 的 Schema 证据

固定源码：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`Tool.ts` 当前直接支持：

```text
inputSchema
inputJSONSchema
optional outputSchema
```

还存在：

```text
inputsEquivalent(a, b)
```

这进一步说明 Production Tool 需要理解“输入是否等价”等运行时语义，而不只是反序列化 JSON。

---

# 16. Schema Validation 和 Permission 的边界

非常重要：

```text
Schema:
path 是 string

Semantic Validation:
path 的格式合法

Permission:
用户能不能读这个 path

Sandbox:
进程实际上能不能触碰这个 path
```

不要把：

```text
"allowed_paths" enum
```

当成全部安全机制。

Schema 是协议约束，不是安全边界。

---

# 17. Hallucination Handling

模型可能：

```text
调用不存在的 Tool
传不存在的 enum
编造资源 ID
引用已过期 capability
```

Runtime 应该做：

```text
unknown tool
→ structured unsupported_tool

invalid args
→ validation feedback

resource not found
→ runtime observation

repeated hallucination
→ loop guard / fallback / stop
```

不能：

```text
KeyError → 500
```

然后整个 Agent Service 崩掉。

---

# 18. 验证顺序为什么重要

错误顺序：

```text
先执行 SQL
→ 再检查 permission
```

显然太晚。

推荐：

```text
Cheap deterministic checks first
→ expensive/external checks later
→ execution last
```

例如：

```text
parse
→ schema
→ local semantic validation
→ policy
→ external resource check
→ execute
```

这样能降低成本和风险。

---

# 19. AI 应用场景：Search Tool

Tool：

```text
search_knowledge_base(query, top_k, filters)
```

可能错误：

```text
top_k = 100000
unknown tenant filter
filter field not indexed
query empty
```

Runtime 可以：

```text
schema: top_k 1..50
semantic: query non-empty after trim
policy: tenant_id 由 Runtime 注入，不允许模型传
result: cap payload size
```

这里一个非常重要的设计原则：

> **不要让模型控制它不应该控制的字段。**

例如 `tenant_id`、`user_id`、权限 scope 可以由 Runtime Context 注入，而不是暴露在 Tool Schema 让模型自由填写。

---

# 20. 高频易错点

⚠️ **JSON 合法 = Tool Call 正确**  
只完成 Syntax Layer。

⚠️ **所有字段都让模型传**  
身份、tenant、permission scope 等应由 Runtime 注入。

⚠️ **Validation Error 全部抛 Exception**  
可修复错误应该结构化反馈给模型。

⚠️ **Tool Result 默认可信**  
外部 Tool/MCP Result 也要做大小、安全、结构检查。

⚠️ **Schema 越复杂越专业**  
过度复杂会降低模型 Tool Accuracy。

---

# 21. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Tool Schema 只能约束结构，不能保证语义和权限正确。我会把 Tool Call 经过 Parse、Schema Validation、Semantic Validation、Registry/Version Check、Permission，再执行；执行结果也要做 Normalize、Size/Security Check 后才回填。错误分成可反馈模型进行 Repair 的调用错误和 Runtime Fatal，避免所有错误都直接把 Agent 崩掉。

## Level 2｜2–3 分钟

> 比如 read_file 的 path 是 string 只属于 Schema；start_line <= end_line 属于 semantic validation；文件是否存在是 runtime validation；用户能否读属于 permission；真正能否越界访问由 sandbox enforce。对于 invalid args，我会返回结构化 issues，让模型 repair，并设置 repair budget。tenant_id 这类安全字段不会让模型传，而由 Runtime Context 注入。Tool Result 也要验证，因为 MCP/外部系统返回内容不一定可信。

## Level 3｜继续追问

🔍 **Repair 和 Retry 区别？**  
Retry 是同类输入再次执行；Repair 是修改调用参数或路径再尝试。

🔍 **为什么需要 Fatal Error？**  
某些错误表示 Runtime invariant 破坏，继续让模型尝试没有意义甚至危险。

🔍 **怎样设计 Schema 才更利于模型？**  
字段少而语义清楚、enum 稳定、描述明确、避免互相矛盾的可选组合，并用 Eval 验证。

---

# 22. 本章证据

## HUMAN-A

- `AGENT-022` Structured Output / Validation：11 sources；
- `AGENT-020` Tool Failure：27 sources；
- `AGENT-019` Tool Lifecycle：10 sources。

## Claude Code

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

- `Tool.ts`：inputSchema / inputJSONSchema / outputSchema / inputsEquivalent。

## OpenAI Codex

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

- `codex-rs/core/src/tools/router.rs`
- `codex-rs/tools/src/function_call_error.rs`
- `codex-rs/core/src/tools/registry.rs`

## 权威资料

Anthropic — Writing effective tools for agents — with agents  
https://www.anthropic.com/engineering/writing-tools-for-agents

---

# 23. 自测

<details><summary>1. JSON Schema 能保证 Tool Call 正确吗？</summary>

不能。它主要约束结构，还需要 semantic、resource/runtime、permission/policy 等验证。
</details>

<details><summary>2. tenant_id 为什么通常不应该让模型传？</summary>

因为 tenant scope 是安全上下文，应来自认证后的 Runtime State。让模型自由填写会把权限边界变成可生成参数。
</details>

<details><summary>3. 为什么 Tool Result 也要 Validation？</summary>

外部 Tool/MCP Server 可能返回结构变化、超大 payload、不可信文本或敏感信息，必须归一化、限制大小、做安全处理后再进入 Context。
</details>

<details><summary>4. `RespondToModel` 与 `Fatal` 这种区分有什么价值？</summary>

前者允许把可修复调用错误变成 Observation，让模型 Repair；后者表示 Runtime 无法安全继续，应该终止或上抛。
</details>
