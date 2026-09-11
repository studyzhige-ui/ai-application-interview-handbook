# 07. Tool Contract：Production Tool 不只是一个函数

`AGENT-018`（Tool / Function Calling 完整链路）有 **29 个独立 HUMAN-A 来源**，`AGENT-019`（Tool Lifecycle）有 **10 个来源**，`AGENT-024`（Skill / Tool / MCP 等边界）有 **34 个来源**。

所以面试里只说：

> “Tool 就是一个 Python 函数，模型传参数调用。”

远远不够。

成熟 Agent Runtime 需要的是一个**可被发现、描述、校验、授权、执行、取消、追踪、版本化的能力契约**。

---

# 1. 先讲人话：Tool 为什么不是 function(args) -> value

普通函数：

```python
def add(a: int, b: int) -> int:
    return a + b
```

Production Agent Tool 还要回答：

```text
这个 Tool 叫什么？
模型怎么知道什么时候用？
参数 Schema 是什么？
参数错了怎么办？
它是只读还是写操作？
会不会产生不可逆副作用？
能不能并发跑？
要不要用户确认？
超时多久？
能不能取消？
执行进度怎样报告？
返回结果多大？
失败属于什么类型？
结果怎样进入 Context？
版本升级后旧 Call 怎么办？
```

因此更合理的抽象是：

```text
Tool Contract
= Identity
+ Description
+ Input Schema
+ Output Contract
+ Execution
+ Permission Metadata
+ Side-effect Semantics
+ Concurrency Semantics
+ Cancellation Semantics
+ Progress
+ Error Semantics
+ Version
```

---

# 2. Tool 的第一职责：让模型理解“这个能力是干什么的”

模型选择 Tool 时通常依赖：

- name；
- description；
- input schema；
- 当前 Context。

例如两个 Tool：

```text
search_docs
search_code
```

如果 description 都写：

```text
"Search things"
```

模型就很难稳定选择。

更好的描述：

```text
search_docs:
Search indexed product or policy documents for factual passages.

search_code:
Search repository source text and symbols before reading files.
```

💡 **Tool Description 本身就是 Runtime Prompt Surface。**

它会直接影响 Tool Selection Accuracy。

---

# 3. 一个教学级 Tool Protocol

```python
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any] | None = None
    version: str = "1"
    read_only: bool = True
    destructive: bool = False
    concurrency_safe: bool = True
    requires_approval: bool = False


@dataclass
class ToolContext:
    run_id: str
    user_id: str
    tenant_id: str
    cancel_token: Any


class Tool(Protocol):
    spec: ToolSpec

    async def execute(
        self,
        arguments: dict[str, Any],
        context: ToolContext,
    ) -> Any:
        ...
```

这比一个裸函数多出来的字段，不是“架构炫技”，而是为后面的 Runtime Decision 服务。

---

# 4. Tool Identity 为什么要稳定

模型和 Runtime 都需要通过 Tool Name 找能力：

```text
"read_file"
"run_test"
"create_ticket"
```

如果今天叫：

```text
create_jira
```

明天改成：

```text
jira_create_issue
```

旧 Session、缓存、Eval Dataset、Trace 可能都受影响。

因此成熟系统常需要：

- stable name；
- alias；
- version；
- deprecation；
- backward compatibility。

Claude Code 固定快照中的 `Tool.ts` 就存在 `aliases`，明确支持 Tool 重命名后的兼容查找。

---

# 5. Input Schema 是“模型与 Runtime 的协议”

例如：

```json
{
  "type": "object",
  "properties": {
    "path": {"type": "string"},
    "line_start": {"type": "integer", "minimum": 1},
    "line_end": {"type": "integer", "minimum": 1}
  },
  "required": ["path"]
}
```

这个 Schema 同时服务：

```text
Model generation constraint
Runtime validation
Documentation
Eval
Compatibility
```

所以 Tool Schema 不是只为了“让 API 接受 JSON”。

---

# 6. Output 也应该有 Contract

很多 Demo：

```python
return str(result)
```

Production 更适合：

```json
{
  "ok": true,
  "data": {...},
  "artifact_ref": null,
  "metadata": {
    "truncated": false
  }
}
```

失败：

```json
{
  "ok": false,
  "error": {
    "type": "not_found",
    "retryable": false,
    "message": "file does not exist"
  }
}
```

这样 Runtime 才能可靠决定：

- Repair；
- Retry；
- Fallback；
- Fail；
- 是否让模型看到完整结果。

---

# 7. Read-only / Destructive 为什么必须显式

比较：

```text
read_file
search_code
```

和：

```text
write_file
send_email
delete_branch
transfer_money
```

风险完全不同。

如果 Runtime 只知道 Tool Name，不知道 Side-effect Semantics，就很难做统一 Permission Policy。

可以定义：

```text
read_only = true
```

或：

```text
destructive = true
requires_approval = true
```

Claude Code `Tool.ts` 中明确存在：

- `isReadOnly(input)`；
- `isDestructive(input)`；
- `isConcurrencySafe(input)`。

这提供了非常直接的成熟实现证据。

---

# 8. 为什么这些属性有时必须“按输入判断”

同一个 Tool 可能：

```text
bash("ls")
```

近似只读；

但：

```text
bash("rm -rf build/")
```

具有破坏性。

所以 Tool Contract 不一定只是静态：

```python
is_destructive(tool)
```

而可能是：

```python
is_destructive(tool, input)
```

这就是为什么生产 Tool Policy 会比“白名单 Tool Name”复杂。

---

# 9. Concurrency Safety 是 Tool Contract 的一部分

两个 Tool 同时执行：

```text
read_file(a.py)
read_file(b.py)
```

通常没问题。

但：

```text
write_file(config.py)
write_file(config.py)
```

可能 Lost Update。

又比如：

```text
run_migration
```

可能根本不允许并发。

因此 Runtime 在并行 Tool Call 前需要知道：

> **这个能力是否 concurrency safe。**

第 12 章会深入 Side Effect 和 Concurrency。

---

# 10. Cancellation 也必须写进协议

用户在 Tool 执行时发送：

```text
“停下，不要继续。”
```

不同 Tool 行为不同：

```text
search → 可以取消
shell build → 可以发送 cancel signal
external payment → 可能已经不可取消
DB transaction → 需要 rollback semantics
```

Claude Code `Tool.ts` 中有：

```text
interruptBehavior(): cancel | block
```

这很好地说明：

> Tool 必须告诉 Runtime“新用户输入到来时，这个执行能不能中断”。

---

# 11. Progress 为什么不是 UI 小功能

长 Tool：

```text
扫描 20 万文件
运行 15 分钟测试
下载大数据集
远程 Agent Task
```

需要报告：

```text
started
progress
partial result
completed
```

Progress 可以服务：

- UI；
- timeout 判断；
- watchdog；
- trace；
- operator intervention。

Claude Code Tool Contract 有 progress callback，Task 还有 output file / offset 语义。

---

# 12. Tool Context 不应该靠全局变量

执行 Tool 时通常还需要：

```text
run_id
user / tenant
permission context
abort signal
workspace
trace context
secrets handle
quota
```

所以：

```python
execute(args)
```

在复杂系统中不够。

更合理：

```python
execute(args, runtime_context)
```

但 Runtime Context 要避免把所有内部对象都暴露给 Tool，最好提供最小能力接口。

---

# 13. Claude Code `Tool.ts` 提供的成熟证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

当前索引已直接确认 `Tool` 包含：

- `call(...)`；
- description；
- input schema / input JSON schema；
- optional output schema；
- aliases；
- `searchHint`；
- `isConcurrencySafe(input)`；
- `isEnabled()`；
- `isReadOnly(input)`；
- `isDestructive(input)`；
- `interruptBehavior()`；
- progress callback。

`ToolUseContext` 还包含：

- `AbortController`；
- MCP clients；
- agent definitions；
- permission decisions；
- nested memory；
- dynamic skill discovery；
- tool-result budget state。

这已经足够说明：

> Production Tool Contract 远远大于 Python Callable。

---

# 14. Codex Tool Layer 的证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

已确认路径：

- `codex-rs/tools/README.md`
- `codex-rs/tools/src/tool_call.rs`
- `codex-rs/tools/src/lib.rs`
- `codex-rs/core/src/tools/router.rs`

`tools/README.md` 明确把：

```text
schema sanitization
MCP / dynamic conversion
ToolExecutor
ToolCall
ToolOutput
```

抽成共享 Tool 层。

这同样说明 Tool 是 Runtime Protocol Boundary。

---

# 15. Tool Design 会影响模型表现

Anthropic 的 `Writing effective tools for agents — with agents` 强调一个关键点：

> Tool 本身也应该用真实 Agent Evaluation 迭代。

原因很简单：

- 名字不清楚 → 选错 Tool；
- Schema 太复杂 → 参数错误；
- Result 太长 → Context 爆炸；
- Tool 粒度不合适 → 多步规划困难。

来源：

https://www.anthropic.com/engineering/writing-tools-for-agents

---

# 16. Tool 粒度怎么设计

太细：

```text
open_connection
send_header
send_body
parse_response
```

模型要编排大量低层动作。

太粗：

```text
do_everything_for_customer_support
```

模型缺乏组合性和可观察性。

更合理：

> **一个 Tool 对应一个语义清楚、可验证、边界明确的能力。**

例如：

```text
search_tickets
get_ticket_detail
create_jira_issue
```

---

# 17. Tool vs Skill vs MCP

先给一个简化边界：

```text
Tool
= 一次可执行能力

Skill
= 可发现、可加载的程序性知识 / scripts / resources 包

MCP
= Host 与外部能力 / Context 的标准连接协议
```

它们不是互斥：

```text
MCP Server
→ 暴露 Tool

Skill
→ 可能指导 Agent 何时调用某个 Tool
```

第 34–35 章会展开。

---

# 18. 高频易错点

⚠️ **Tool = Python Function**  
只能算最小实现，不是 Production Contract。

⚠️ **Tool Description 随便写**  
会直接影响模型选择。

⚠️ **所有 Tool 都能并行**  
写操作和共享资源可能冲突。

⚠️ **Tool 执行失败就抛异常结束 Agent**  
很多错误应该结构化回填，让模型 Repair。

⚠️ **危险 Tool 只靠 System Prompt 约束**  
必须有 Runtime Permission / Sandbox。

---

# 19. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Production Tool 不是一个裸函数，而是 Runtime Capability Contract。至少要有稳定 identity、description、input/output schema、execution、error semantics，并标明 read-only/destructive、permission、concurrency、cancellation 和 progress。模型负责选择和生成调用，Runtime 负责校验、授权、执行、记录和回填结果。

## Level 2｜2–3 分钟

> 我会把 Tool Spec 和 Tool Runtime 分开。Spec 给模型和 Registry 用，包括 name、description、schema、version、side-effect metadata；Executor 接收 args + runtime context。Tool Call 先 validation，再 permission/approval，再 execution。结果统一成 success/error contract。对于写操作，还要考虑 idempotency 和 concurrency safety；长 Tool 要支持 cancellation/progress。这样 Tool 才能进入统一 Harness。

## Level 3｜继续追问

🔍 **为什么 isDestructive 要看 input？**  
同一个 Shell Tool，不同命令风险不同。

🔍 **Tool Description 为什么要 Eval？**  
它直接影响模型选择、参数生成和调用成功率。

🔍 **Tool Version 为什么重要？**  
旧 Session、Trace、Eval Dataset 可能仍引用旧 Schema，需要兼容或迁移。

---

# 20. 本章 HUMAN-A

- `AGENT-018` Tool Calling Protocol：29 sources；
- `AGENT-019` Tool Lifecycle：10 sources；
- `AGENT-024` Capability Boundary：34 sources。

Verified Tool Follow-up Chain：

```text
Tool Lifecycle
→ Discovery
→ Schema / Version
→ Failure
→ Permission / Sandbox
```

---

# 21. 自测

<details><summary>1. 为什么 Tool Contract 需要 read_only / destructive？</summary>

因为 Runtime 要基于副作用风险做 permission、approval、sandbox 和并发决策，不能只看 Tool Name。
</details>

<details><summary>2. Tool Input Schema 有哪些作用？</summary>

帮助模型生成结构化参数、让 Runtime 做 validation、作为文档和 Eval Contract，并支持版本兼容。
</details>

<details><summary>3. 为什么 Tool 需要 interrupt/cancellation semantics？</summary>

长任务中用户可能修改需求或取消执行，不同 Tool 是否可中断、如何清理资源、是否已经产生副作用必须明确。
</details>

<details><summary>4. Tool 与 MCP 的关系是什么？</summary>

Tool 是可执行能力；MCP 是 Host/Client/Server 之间标准化暴露 Tool/Resource/Prompt 的协议。MCP Tool 进入 Host 后仍要经过本地 Runtime Policy。
</details>
