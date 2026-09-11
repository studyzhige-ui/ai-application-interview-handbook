# 04｜Tool Contract、Schema 与 Validation

> 本章合并旧 `07-ToolContract` 与 `08-ToolSchemaValidation`。Tool 在 Production Agent 中不是一个普通函数，而是**模型与真实世界之间的协议边界**。

## 1. 先讲人话：为什么 Tool 不能只写成一个 Python 函数

Demo：

```python
def search_code(query: str) -> str:
    ...
```

Production 还必须回答：

```text
Tool 叫什么？
模型看到什么描述？
输入 Schema 是什么？
字段缺失 / 类型错怎么办？
这个 Tool 是否只读？
能不能并发？
是否需要权限？
会不会产生外部副作用？
怎样取消？
怎样返回结构化结果？
结果是否会污染 Context / Memory？
```

所以 Tool Contract 更接近：

```text
Identity
+ Description
+ Input Schema
+ Validation
+ Execution Semantics
+ Side-effect Semantics
+ Permission
+ Cancellation / Progress
+ Result Contract
```

## 2. Tool Contract 的最小结构

```python
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: dict
    read_only: bool
    destructive: bool
    concurrency_safe: bool
    handler: Callable[..., Any]
```

真实系统还会增加 version、timeout、permission class、tenant scope、result schema 等。

## 3. Schema 解决两个完全不同的问题

### Model-facing Schema

帮助模型生成：

```json
{
  "query": "ToolExecutor",
  "path": "codex-rs/core"
}
```

### Runtime Validation

决定这个输入**实际上能不能执行**。

模型生成了 JSON，不意味着可信。

因此完整路径：

```text
Model produces arguments
→ Parse
→ Schema validate
→ Semantic validate
→ Permission validate
→ Execute
```

## 4. 结构校验 vs 语义校验

Schema 能发现：

```text
missing field
wrong type
unknown enum
invalid JSON
```

但发现不了：

```text
path = ../../etc/passwd
amount = -100
branch = production
user_id 属于其它 tenant
```

这属于 Semantic / Policy Validation。

不要把：

```text
JSON Schema valid
```

误认为：

```text
这个动作安全且业务正确
```

## 5. Tool Description 也是协议的一部分

Tool 很多时，模型选择能力依赖：

- name；
- description；
- 参数语义；
- 示例；
- failure / limitation；
- search metadata。

描述太模糊：

```text
run(command)
```

很难帮助模型选择。

更明确：

```text
run_tests(target, timeout_seconds)
Runs repository tests for a specific target.
Does not modify source files.
```

Tool quality 不只是 handler 实现质量，还包括**模型是否能正确发现和使用它**。

## 6. Structured Result 也应该有 Contract

不要默认返回：

```text
一大段字符串
```

更稳定：

```json
{
  "status": "failed",
  "exit_code": 1,
  "summary": "2 tests failed",
  "artifact_ref": "tool-results/call_123.txt",
  "retryable": false
}
```

这样：

- Runtime 能分支；
- Model 更容易理解；
- Trace 更容易统计；
- 大结果可外部化。

## 7. Tool Arguments 出错时怎么处理

常见错误分类：

```text
Syntax Error
Schema Error
Semantic Error
Permission Error
Execution Error
Timeout
```

对于前两类，可把结构化错误反馈给模型做一次 Repair：

```json
{
  "error": "invalid_arguments",
  "field": "timeout_seconds",
  "expected": "integer between 1 and 300"
}
```

而不是：

```text
Exception: validation failed
```

## 8. Repair 不能无限循环

一个安全策略：

```text
invalid arguments
→ return structured feedback
→ model repairs
→ retry once / limited times
→ repeated same failure
→ alternate route or stop
```

必须与后面的 Loop Guard / Budget 联动。

## 9. Side-effect Metadata 为什么应该靠 Runtime 保存

模型可能说：

> “这个 Tool 只是读取。”

这不能作为安全依据。

Tool Contract 应由 Host / Runtime 声明：

```text
read_only
is_destructive
concurrency_safe
requires_approval
```

后续 Permission / Scheduler 只信 Runtime Metadata，不信模型自述。

## 10. 源码证据：Claude Code

固定快照的 `Tool.ts` 显示 Tool Contract 不只包含 Schema 和 `call()`，还包含：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior()`；
- Permission Context；
- Progress Callback；
- Result / Context Modifier；
- Tool Result Budget / Dynamic Discovery 相关状态。

这非常适合说明：

> Production Tool 是 Runtime Contract，不是 Function Signature。

## 11. 源码证据：Codex

固定 Codex 快照中的 `ToolExecutor` 把：

```text
tool_name
spec
exposure
search_info
supports_parallel_tool_calls
handle(invocation)
```

放在同一个执行契约中。

`ToolOutput` 又把：

- model-facing response；
- logging projection；
- host-only metadata；
- external context 标记；

分开表达。

这说明 Tool Input / Output 都应被 Runtime 当成正式协议对象。

## 12. 版本升级怎么办

Tool Schema 变化可能破坏：

- Prompt cache；
- Model selection behavior；
- Replay；
- persisted Run；
- old Checkpoint；
- Evaluation Dataset。

因此成熟 Tool 可以保存：

```text
tool_name
schema_version
runtime_version
```

并在 Resume / Replay 时明确兼容策略。

## 13. HUMAN-A 对应

- `AGENT-018` Tool Calling 完整链路：29 来源；
- `AGENT-019` Tool Lifecycle：10 来源；
- `AGENT-022` Structured Output / Validation：11 来源。

面试官常从：

```text
Tool Calling 是什么？
```

继续追：

```text
参数错了怎么办？
Tool 怎么注册？
Tool Schema 变了怎么办？
Tool Result 太大怎么办？
```

## 14. 🎯 30 秒回答

> Production Tool 不只是一个函数。它应该有稳定的 name/description、输入 Schema、Runtime Validation、side-effect 和 concurrency metadata、permission/cancellation 语义以及结构化 Result Contract。模型生成的参数永远是不可信输入，必须经过 parse、schema、semantic 和 policy 校验；错误可以结构化反馈给模型做有限 Repair，但不能无限重试。

## 15. ⚠️ 易错点

- Schema valid = 安全——错；
- Tool Description 只是文案——错，它影响模型选择；
- Tool Result 统一返回字符串——会损失结构化状态；
- `read_only` 由模型判断——错，应由 Runtime 声明；
- 参数错就自动无限 Retry——容易形成 Loop。

## 16. 🔍 继续追问

```text
Tool 多到几百个后怎么让模型选择？
Registry / Router 怎样设计？
Deferred Tool 是什么？
Tool 能否按需加载？
```

下一章进入 Tool Registry / Router / Progressive Discovery。

<details><summary>自测：为什么 JSON Schema 不能替代 Permission？</summary>

因为 Schema 只保证输入形状合法，不能判断该用户是否有权执行、资源是否属于当前 tenant、动作是否高风险或路径是否越界。
</details>