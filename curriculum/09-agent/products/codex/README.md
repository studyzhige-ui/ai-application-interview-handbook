# OpenAI Codex｜成熟 Coding Agent 的系统解剖

[← 成熟产品源码学习](../README.md) · [Agent 模块](../../README.md)

> **源码仓库：** [openai/codex](https://github.com/openai/codex)  
> **固定快照：** [`5c5308fc9a9ee789049d646ef11e5400384b9c6f`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f)  
> **核验日期：** 2026-09-20  
> **学习范围：** Codex Runtime 中与 Context、Memory、Tool、Permission、Persistence、Recovery、Trace / Evaluation 直接相关的完整调用链；UI 视觉实现、打包发布等不改变这些语义的外围代码不逐文件复述。

这组文档不是“Codex 有哪些功能”的产品介绍，而是沿源码回答：

> **一个成熟 Coding Agent 到底怎样把用户输入变成可执行、可恢复、可诊断的长期 Agent Session？**

---

## 1. 先看整个运行时

Codex 的核心不是一个 Prompt，而是一组长期协作的运行时边界：

```text
Client / TUI / App Server
          │
          ▼
      Thread / Session
  ThreadStore + Session State
          │
          ▼
        Turn
  用户输入、turn settings、
  hooks、plugin/MCP requirements
          │
          ▼
        Step
  捕获同一时刻的：
  model / permission / world state /
  tool router / environment
          │
          ├──────────────┐
          ▼              ▼
   Context / History   ToolRouter
   WorldState          Registry
          │              │
          └──────┬───────┘
                 ▼
             Prompt
       input + tools + base
       instructions + cache
                 │
                 ▼
          ModelClientSession
       Responses WS / HTTP
                 │
        ┌────────┴────────┐
        ▼                 ▼
  assistant output     tool call
        │                 │
        │        validate / hooks /
        │        approval / sandbox /
        │        execute / normalize
        │                 │
        └────────┬────────┘
                 ▼
       append canonical history
                 │
           next sampling Step
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
 turn complete       compaction / retry /
                     cancel / recovery
```

旁边还有三条持续存在的“非聊天”通道：

```text
Long-term Memory
Phase 1 extraction → Phase 2 consolidation
→ memory_summary / rollout summaries
→ next sessions recall

Persistence
LiveThread → ThreadStore
→ rollout JSONL + state DB
→ resume / fork / rollback reconstruction

Observability
OTEL / analytics + Rollout Trace
→ raw evidence → offline reducer → semantic graph
```

理解 Codex 的关键，就是不要把这三条通道和当前模型 Context 混成同一件事。

---

## 2. Session、Turn、Step 是三个不同的生命周期

### Session / Thread

Session 是长期运行边界，保存：

- thread identity；
- canonical conversation history；
- current Context Manager；
- token usage；
- context-window / compaction 状态；
- persistent Thread Store handle；
- extension / plugin / memory session state；
- session-scoped ModelClient；
- network / sandbox / permission runtime；
- multi-agent 和 trace 等服务。

### Turn

Turn 对应一次用户目标推进。它可以包含多次模型采样与多次 Tool Call。

`run_turn` 的源码说明非常直接：

```text
模型返回 tool call
→ Runtime 执行
→ tool output 回填
→ 再次 sampling

模型只返回最终 assistant message
→ 写入历史
→ turn complete
```

一个 Turn 还拥有：

- turn-scoped `ModelClientSession`；
- sticky routing state；
- turn settings；
- cancellation token；
- pending / steered input；
- turn diff；
- required MCP servers / plugins；
- telemetry context。

### Step

Step 是一次模型采样附近的“精确快照”。

为什么还要 Step？

因为一个 Turn 内可能发生：

- MCP server 刚启动；
- Tool catalog 改变；
- Environment 变 ready；
- Permission profile 改变；
- user steer 新输入进入；
- plugin / skill 选择改变。

Codex 把当时用于广告 Tool、组装 Context 和之后执行 Tool 的设置放进 `StepContext`。Tool Call 即使稍后才执行，也保留产生它的那个 Step，避免：

> 模型看到 A 版工具说明，但真正执行时却误用 B 版配置。

这是成熟 Harness 很重要的时序一致性设计。

---

## 3. 四条学习主线

### 01｜Context Lifecycle

[进入：上下文完整生命周期](01-context-lifecycle.md)

重点回答：

```text
用户输入怎样进入 Turn？
↓
哪些意图在模型前确定，哪些由模型解释？
↓
base / developer / world state / memory /
skills / plugins / environment 怎样进入 Context？
↓
为什么正常路径是增量 context diff？
↓
Prompt Cache 与 previous_response_id 怎样配合？
↓
Tool Result 怎样重新成为 Context？
↓
Context Window 怎么计数？
↓
Local / Remote / Token-Budget 三类 Compaction 怎么工作？
↓
Resume / Fork 怎样从 replacement-history checkpoint 重建？
```

---

### 02｜Memory Lifecycle

[进入：记忆完整生命周期](02-memory-lifecycle.md)

Codex 当前源码已经存在完整的 Memory 子系统，而不是把 Chat History 换个名字：

```text
eligible old thread
↓
Phase 1：过滤 rollout + 模型提取
↓
DB stage1 outputs
↓
Phase 2：选择 + 文件同步 + diff
↓
受限 consolidation agent
↓
memory_summary.md + rollout_summaries/
↓
新 Session 注入 summary
↓
按需 search / list / read 证据
↓
citation / usage 反馈
↓
纠正、forget、prune、再 consolidation
```

同时还有“用户明确要求 remember / forget / update”时的 append-only ad-hoc notes 路径。

---

### 03｜Tool Lifecycle

[进入：工具完整生命周期](03-tool-lifecycle.md)

Codex 的 Tool 系统不是单一函数表：

```text
built-in tools
MCP tools
extension tools
dynamic tools
hosted model tools
Skills / Code Mode
        ↓
      Registry
        ↓
AllowedTools / collision / policy
        ↓
Direct / Deferred / CodeMode / Hidden
        ↓
current model-visible Tool Router
        ↓
model tool call
        ↓
parse + payload validation + pre hooks
        ↓
approval + Guardian + sandbox + network
        ↓
parallel / serial execution
        ↓
post hooks + result normalization
        ↓
canonical tool output
        ↓
next model request
```

规模化方面，Deferred Tool 使用 `tool_search` 的 BM25 按需发现；Skills 采用预算化 catalog + progressive disclosure。

---

### 04｜Engineering & Evaluation

[进入：工程边界、失败与评测](04-engineering-evaluation.md)

把前三条链重新合到 Production Runtime：

- cancellation / retry / fallback；
- context overflow；
- tool collision / malformed output；
- permission / sandbox / network；
- MCP readiness；
- memory poisoning / stale memory；
- persistence / resume / fork / rollback；
- prompt cache 与 latency / token cost；
- 大 Context；
- 数万 Tools / Skills；
- OTEL / analytics / Rollout Trace；
- Agent、Context、Memory、Tool 的评测设计；
- 面试场景题。

---

## 4. 源码模块地图

下面不是全部 Workspace crate 的清单，而是四条生命周期最关键的源码边界。

| 关注点 | 关键源码 |
|---|---|
| Agent loop | `codex-rs/core/src/session/turn.rs` |
| Session / step capture | `codex-rs/core/src/session/` |
| Context typed fragments | `codex-rs/core/src/context/` |
| Context fragment abstraction | `codex-rs/context-fragments/` |
| Context history / normalization | `codex-rs/core/src/context_manager/` |
| Compaction | `core/src/compact.rs`、`compact_remote_v2*.rs`、`compact_token_budget.rs` |
| Model request / cache / transport | `codex-rs/core/src/client.rs` |
| Persistent thread history | `codex-rs/thread-store/`、`codex-rs/rollout/` |
| Resume / fork reconstruction | `core/src/session/rollout_reconstruction.rs` |
| Memory read / write | `codex-rs/memories/read/`、`memories/write/` |
| Memory model-facing extension | `codex-rs/ext/memories/` |
| Memory DB | `codex-rs/state/src/runtime/memories.rs` |
| Tool registry / router | `core/src/tools/registry.rs`、`router.rs`、`spec_plan.rs` |
| Tool execution | `core/src/tools/parallel.rs`、`orchestrator.rs`、`handlers/` |
| MCP | `codex-rs/mcp/`、`rmcp-client/`、`core/src/mcp_tool_exposure.rs` |
| Skills | `codex-rs/skills/`、`ext/skills/` |
| Extensions | `codex-rs/ext/extension-api/` 与 `ext/*` |
| Permission / sandbox | Tool orchestrator + sandbox crates |
| Metrics / analytics | `codex-rs/otel/`、`analytics/` |
| Deep diagnosis | `codex-rs/rollout-trace/` |
| Integration tests | `codex-rs/core/tests/suite/` + 各 crate tests |

---

## 5. Codex 自己写进源码仓库的 Context 设计原则

固定快照中的根 `AGENTS.md` 对“model-visible context”提出了非常强的约束，源码学习必须把它当成架构规则，而不是风格建议：

```text
普通流程只增量追加，不随意重写历史
↓
避免频繁变化的 Context 破坏 Prompt Cache
↓
任何自动注入项必须有硬上限
↓
单个 model-context item 不能无限增长
↓
新增注入内容应使用 typed fragment
↓
测试必须验证真实模型可见输入
```

其中还明确限制单一 Context Item 的规模，并要求较大的新增项接受额外审查。

这正好解释为什么源码里会出现：

- typed `ContextualUserFragment`；
- World State snapshot + diff；
- reference context baseline；
- bounded skill catalog；
- bounded MCP specs；
- bounded memory summary；
- compaction replacement history；
- stable synthetic IDs；
- prompt-cache-aware incremental request。

它们不是彼此无关的优化，而是同一个 Context Engineering 原则的不同落点。

---

## 6. 四个最值得带走的架构思想

### 6.1 模型可见状态必须有“编译边界”

Session 里存了很多东西，但不是全部都直接变成 Prompt。Codex 用 Context Contributor、World State、Tool Router、History normalization 等层把程序状态投影为当前模型请求。

### 6.2 长期正确性依赖“精确 checkpoint + 增量更新”

正常运行增量记录；Compaction 才产生 replacement-history checkpoint。恢复时从最新仍有效的 checkpoint + suffix replay，而不是永远从第一条 JSONL 重放。

### 6.3 大规模能力不能全部展开

Tools 使用 Deferred discovery；Skills 使用 budgeted catalog + progressive disclosure；MCP spec 有硬字节预算。能力增长时，首先控制“模型可见目录”，而不是把 Context Window 当垃圾桶。

### 6.4 可诊断性必须区分“模型看到什么”和“Runtime 实际发生什么”

Rollout Trace 明确分离：

```text
model-visible ConversationItem
≠
ToolCall / TerminalOperation / CodeCell / InferenceCall
```

调试器最终通过 interaction edges 把它们重新连起来。这是解释复杂 Agent Bad Case 的关键。

---

## 7. 阅读顺序

如果已经学完 Agent 通用课程：

```text
本页
→ 01 Context
→ 02 Memory
→ 03 Tool
→ 04 Engineering & Evaluation
```

读完以后，应该能从源码而不是术语回答：

1. Codex 一次请求的 Context 是怎样被编译出来的？
2. 为什么 Context 不能等于完整 Chat History？
3. Prompt Cache 为什么会反向约束 Context 结构？
4. Compaction 怎样保证压缩后还能 Resume / Fork？
5. Codex Memory 怎样从旧 Rollout 变成下一次 Session 的可用知识？
6. 用户纠正记忆怎样进入系统，旧记忆怎样被遗忘？
7. 注册了一万个工具后，为什么不需要一次暴露一万个 Schema？
8. MCP / Skills / built-in Tool 怎样进入统一执行边界？
9. Tool Call 的 permission / approval / sandbox 在哪里发生？
10. 网络断开、工具取消、Context overflow、恢复失败分别怎样处理？
11. 怎样评测 Memory、Context、Tool 和整个 Coding Agent？
