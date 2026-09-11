# 05｜Tool Registry、Router 与 Progressive Discovery

> 本章把旧 `09-ToolRegistryRouter` 与旧 `33-ToolDiscovery` 合并。它们本来就是同一个能力规模化问题：**Runtime 有越来越多 Tool 后，怎样管理、暴露、发现和路由，而不是把所有 Schema 永久塞给模型。**

## 1. Registry 解决什么

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

## 2. Registry 与 Model-visible Tool Set 必须分开

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

## 3. Router 做什么

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

## 4. 为什么需要 Namespace

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

## 5. Tool Exposure 不应该只有“注册 / 未注册”

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

## 6. Progressive Discovery 的核心

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

## 7. Tool Discovery 可以怎么做

### Rule / Intent Filter

```text
“查工单” → jira tools
“改代码” → filesystem + shell + test tools
```

优点：快、稳定。

### Embedding / Semantic Search

对 Tool name / description / metadata 建索引，根据当前任务召回候选 Tool。

### LLM Router

让一个较小模型先做 capability classification。

### Hybrid

```text
hard policy filter
→ rule / intent narrowing
→ semantic tool retrieval
→ main model final choose
```

通常更稳。

## 8. Discovery 的 Evaluation

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

## 9. Tool Unavailable 怎么办

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

## 10. 源码证据：Codex

固定快照中的 `ToolRouter` 明确区分：

- full registry；
- `model_visible_specs`；
- deferred tool search；
- namespace；
- code-mode tool identity。

`ToolExposure` 还能表达：

```text
Direct
Deferred
DeferredModelOnly
DirectModelOnly
CodeModeOnly
Hidden
```

这直接证明：

> 注册能力与本轮向模型暴露能力是两件事。

## 11. 源码证据：Claude Code

固定快照的 `Tool.ts` 中存在 `searchHint`，`ToolUseContext` 还包含 dynamic skill discovery / discovered skill names 等状态。

这与 HUMAN-A 中“Tool/Skill > 100 后如何按需发现”高度呼应。

## 12. Registry 更新与版本问题

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

## 13. HUMAN-A 对应

- `AGENT-019` Tool Lifecycle：10 来源；
- `AGENT-021` Dynamic Discovery / Progressive Loading：20 来源；
- `AGENT-024/025` Tool / Skill / MCP 边界与 Progressive Disclosure。

Verified Chain 中 `S077`、`S214`、`S236`、`S274` 都出现：

```text
Tool 多了
→ Discovery / Lazy Loading
→ Tool unavailable / failure
→ Schema / Permission / Fallback
```

## 14. 🎯 30 秒回答

> Tool Registry 是完整能力目录，当前 Model-visible Tool Set 只是它经过 tenant、policy、task 和 discovery 筛选后的一个视图。Tool 数量大时不应该把所有 Schema 一次塞入 Context，而应通过 namespace、intent/rule、semantic tool search 或混合路由做 Progressive Discovery，再把少量候选 Tool 暴露给模型。Router 负责把模型 Tool Call 解析到具体 runtime handler，并做版本、exposure 和 policy 检查。

## 15. ⚠️ 易错点

- Registry = 当前 Tool List——错；
- Tool 越多模型越强——可能反而更难选择；
- Discovery 只做 embedding search——不是唯一方案；
- Tool Search 命中就直接执行——仍需 Validation / Permission；
- 长任务中 Tool Catalog 可以随意变化——会破坏 Resume / Replay。

<details><summary>自测：为什么 Deferred Tool 能同时降低 Token 和风险？</summary>

因为它既不把所有 Schema 放进每轮 Context，也不默认向模型暴露所有能力；只有经过 Discovery / Policy 后才进入当前可见集合。
</details>