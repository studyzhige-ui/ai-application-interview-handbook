# 10. L3 接入层：工具契约、注册与发现

[← 09](09-ModelAccessAndRouting.md) · [Agent 主线](../README.md) · [11 →](11-ToolExecutionAndEffects.md)

> 主线位置：**L3 接入层**。模型接入后，需要让它发现并正确描述可调用的外部动作。
>
> 本章产物：**工具契约、目录、可见集合与版本策略**。

[工具是模型与执行系统之间的正式契约](#part-1) → [注册目录与本轮可见集合](#part-2) → [发现、加载与版本生命周期](#part-3)

<a id="part-1"></a>

## 1. 工具是模型与执行系统之间的正式契约

工具描述帮助模型选择，运行接口负责真实调用，底层服务负责实际动作。三者必须分开；可见工具的安全元数据也不能由模型自述决定。

### 先讲人话：为什么 Tool 不能只写成一个 Python 函数

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

### Tool Contract 的最小结构

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

### Schema 解决两个完全不同的问题

#### Model-facing Schema

帮助模型生成：

```json
{
  "query": "ToolExecutor",
  "path": "codex-rs/core"
}
```

#### Runtime Validation

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

### 结构校验 vs 语义校验

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

### Tool Description 也是协议的一部分

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

### Structured Result 也应该有 Contract

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

### Tool Arguments 出错时怎么处理

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

### Repair 不能无限循环

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

### Side-effect Metadata 为什么应该靠 Runtime 保存

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

<a id="part-2"></a>

## 2. 注册目录与本轮可见集合

注册能力不代表每轮都把全部 Schema 给模型。先按权限和环境筛选，再考虑任务相关性与发现策略。隐藏一个工具也不能替代执行时的权限检查。

### Registry 解决什么

最小 Tool Runtime 可以手写：

```python
TOOLS = {
    "read_file": read_file,
    "run_tests": run_tests,
}
```

但 Production 需要 Registry 管理：

```text
identity
schema
version
runtime handler
permission class
exposure mode
search metadata
health / availability
provider / tenant scope
```

Registry 是 Host 的能力目录，不等于“模型当前看得见的 Tool List”。

### Registry 与 Model-visible Tool Set 必须分开

假设系统注册 300 个 Tool：

```text
Registry = 300
```

不代表每轮都发送：

```text
Model-visible tools = 300
```

更合理：

```text
Full Capability Registry
        ↓
Policy / Tenant / Environment Filter
        ↓
Task / Intent Candidate Set
        ↓
Progressive Discovery
        ↓
Current Model-visible Tool Set
```

这能降低：

- Token 成本；
- Tool 选择混淆；
- Schema 冲突；
- Prompt cache 抖动；
- 暴露不必要高风险能力。

### Router 做什么

Router 不是简单的：

```python
handler = tools[name]
```

完整路径：

```text
Model Tool Call
→ normalize identity / namespace
→ resolve version
→ verify exposure
→ find runtime handler
→ permission / policy
→ dispatch
```

如果支持 MCP、Built-in Tool、Remote Tool、Code Mode、Subagent Tool，Router 还要统一不同来源。

### 为什么需要 Namespace

多个来源可能都有：

```text
search
read
execute
```

可以使用：

```text
filesystem.read
jira.search
github.search
mcp.crm.lookup
```

Namespace 解决：

- collision；
- provenance；
- permission；
- ownership；
- observability。

### Tool Exposure 不应该只有“注册 / 未注册”

成熟 Runtime 往往需要多种暴露模式：

```text
Direct
Deferred / Discoverable
Hidden
Code-only / Internal
Tenant-scoped
Environment-scoped
```

一个 Tool 可能存在于 Registry，但当前模型不能直接看到。

<a id="part-3"></a>

## 3. 发现、加载与版本生命周期

正确工具未被召回时，后续模型再强也难以完成任务；发现模块必须单独评测，并为不可用和版本变化提供明确语义。

### Progressive Discovery 的核心

当 Tool 数量很大时：

```text
先给能力目录 / namespace summary
→ Model / Router 识别需要哪个能力域
→ Tool Search / Capability Search
→ 加载少量相关 Schema
→ 再调用具体 Tool
```

这和传统数据库：

```text
先读 catalog
再访问具体 object
```

有些相似。

### Tool Discovery 可以怎么做

#### Rule / Intent Filter

```text
“查工单” → jira tools
“改代码” → filesystem + shell + test tools
```

优点：快、稳定。

#### Embedding / Semantic Search

对 Tool name / description / metadata 建索引，根据当前任务召回候选 Tool。

#### LLM Router

让一个较小模型先做 capability classification。

#### Hybrid

```text
hard policy filter
→ rule / intent narrowing
→ semantic tool retrieval
→ main model final choose
```

通常更稳。

### Discovery 的 Evaluation

不能只看最终任务成功率。

还应测：

```text
Tool Recall@K
Tool Selection Accuracy
Wrong-tool Rate
Discovery Latency
Schema Tokens Loaded
Fallback Rate
```

如果正确 Tool 根本没被召回，后面的 Main Agent 再强也没用。

### Tool Unavailable 怎么办

候选 Tool 可能：

- server down；
- permission denied；
- version mismatch；
- tenant 不可用；
- health degraded。

Runtime 应区分：

```text
not found
not exposed
temporarily unavailable
permission denied
unsupported version
```

然后决定：

```text
repair route
fallback capability
ask user
fail fast
```

### Registry 更新与版本问题

新增 / 升级 Tool 时需要考虑：

```text
schema compatibility
cache invalidation
old checkpoint resume
running session snapshot
permission policy
benchmark regression
```

一个长任务不应该在执行中途无意识地从 Tool v1 切到不兼容的 v2。

可以保存：

```text
capability_snapshot_id
schema_version
resolved_tool_version
```

### 版本升级怎么办

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

## 本章自测

<details>
<summary>Schema 合法为什么不等于操作合法？</summary>

Schema 主要检验形状，还需语义、身份、租户、权限、风险和业务约束检查。

</details>

<details>
<summary>Registry 与可见工具集合是什么关系？</summary>

Registry 是完整目录；可见集合是经过策略、环境和任务筛选后提供给当前模型的视图。

</details>

## 回到主线

现在应能独立说明：工具契约、目录、可见集合与版本策略。下一章：[L3 接入层：工具执行、副作用与取消](11-ToolExecutionAndEffects.md)。

对应真人问题：`AGENT-018`、`AGENT-019`、`AGENT-021`、`AGENT-022`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 09](09-ModelAccessAndRouting.md) · [Agent 主线](../README.md) · [11 →](11-ToolExecutionAndEffects.md)
