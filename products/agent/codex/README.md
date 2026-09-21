# OpenAI Codex｜从源码还原一个成熟 Coding Agent 是怎样运行的

[← Agent 产品源码学习](../README.md) · [↑ Products](../../README.md) · [Agent Curriculum](../../../curriculum/09-agent/README.md) · [Agent References](../../../references/agent/README.md)

> **源码仓库：** [openai/codex](https://github.com/openai/codex)  
> **固定源码快照：** [`bb054a2b03f15787dcc2f9bd8ebfde713bc5b695`](https://github.com/openai/codex/tree/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695)  
> **核验日期：** 2026-09-21

## 核心设计

理解 Codex，先抓住 **Thread → Session → Turn → StepContext** 这条主线。

一条长期任务属于 Thread，Core 中由 Session 维护。一次用户输入开始一个 Turn；真正请求模型前，Session 会捕获 `StepContext`，把这一轮采样要使用的模型、工具、环境和权限固定下来。模型如果返回 Tool Call，也不是直接执行，而是进入统一的 Tool Runtime，经过路由、Hook、Approval、Permission、Sandbox / Network 等边界，结果再写回历史并触发下一次采样。

```text
Thread
  ↓
Session
  ↓
Turn
  ↓
StepContext
  ↓
Context + 本轮 Tool Set
  ↓
Model ↔ Tool Runtime
  ↓
History / Persistence
```

Memory、MCP、Skills、Guardian、Goal 等能力并不需要各自重写主循环，而是通过 Extension Registry 进入 Thread、Turn、Context 和 Tool 的生命周期。Thread Store、Rollout、State DB、Rollout Trace 又分别承担恢复状态与诊断证据。

所以面试里可以先把 Codex 概括成：**一个边界很强的 Agent Core，再通过 Extension 把产品能力接进来。** 这句话是对源码结构的工程抽象，具体行为仍以本页记录的固定 commit 为准。

---

## 1. 先认识这个仓库，而不是先背 Agent 名词

固定快照中的 `codex-rs/Cargo.toml` 是一个很大的 Rust workspace。它包含一百多个 crate。真正与 Agent Runtime（Agent 运行时）直接相关的部分，可以先按职责理解成七层。

### 第一层：产品入口

用户并不是直接调用 `run_turn()`。

Codex CLI（命令行入口）本身就支持交互式 TUI、非交互执行、Review、Resume、Fork、Queue、MCP、Plugin、Sandbox、Debug、App Server、Exec Server 等多种模式。入口集中在：

- `codex-rs/cli/src/main.rs`
- `codex-rs/tui/`
- `codex-rs/exec/`
- `codex-rs/app-server/`

这意味着 Codex Core（核心运行时）并不是“整个产品”，而是被多个前端和服务端入口共同调用的执行内核。

### 第二层：协议与 App Server

桌面端、TUI 或其他客户端通过 App Server 协议操作 Thread（线程，可持续的会话容器）和 Turn（轮次，一次用户输入驱动的一段 Agent 工作）。

相关代码主要在：

- `codex-rs/app-server-protocol/`
- `codex-rs/app-server/src/request_processors/`

例如 `TurnStartParams` 会带着 thread id、输入、模型与本轮设置进入 App Server；App Server 再把请求转成 Core 能处理的操作。这里是“产品协议”和“Agent 内部执行循环”之间的边界。

### 第三层：Thread（线程，会话容器）与 Session（运行实例）

`ThreadManager` 负责创建、恢复、分叉和维护活跃 Thread。真正运行一条 Thread 的内部对象是 `Session`。

核心位置：

- `codex-rs/core/src/thread_manager.rs`
- `codex-rs/core/src/codex_thread.rs`
- `codex-rs/core/src/session/`

这里开始出现我们后面会一直看到的长期状态：历史、环境、权限、模型客户端、扩展状态、MCP 状态、工具状态、Token 使用量、上下文窗口状态和持久化句柄。

### 第四层：Turn 与模型循环

一次用户输入进入正在运行的 Thread 后，会进入 `run_turn`。

入口：

- `codex-rs/core/src/session/turn.rs`

它不是“一次模型调用”。一个 Turn 里面可能包含多次模型采样、多次工具调用、用户中途追加输入、上下文压缩和重试。模型请求、工具结果、再次采样会在这里组成真正的 Agent Loop（Agent 执行循环）。

### 第五层：扩展与能力系统

Codex 不是把所有能力写死在 `core` 里面。它有正式的 Extension API（扩展接口）。

App Server 会把 Goal、Guardian、Memory、MCP、Web Search、Image Generation、Skills、Queue 等扩展安装到 `ExtensionRegistry` 中。扩展可以参与：

- Thread 生命周期；
- Turn 生命周期；
- Context 注入；
- World State（世界状态）；
- Tool 注册；
- Tool 生命周期；
- Token 使用量；
- Skill 调用；
- MCP Server 贡献。

源码入口：

- `codex-rs/ext/extension-api/`
- `codex-rs/app-server/src/extensions.rs`
- `codex-rs/ext/*`

这一层很重要，因为 Memory、Skills、MCP 并不是教材里凭空抽象出来的“模块”，它们确实以扩展的方式接进 Codex Runtime。

### 第六层：执行与隔离

当模型决定调用工具时，Codex 不会直接 `spawn` 一个进程就结束。

真正执行会经过工具路由、Hook（钩子）、Approval（批准）、Permission Profile（权限配置）、Sandbox（沙箱）、Network Policy（网络策略）和执行环境。

相关代码包括：

- `codex-rs/core/src/tools/`
- `codex-rs/exec-server/`
- `codex-rs/sandboxing/`
- `codex-rs/linux-sandbox/`
- `codex-rs/windows-sandbox-service/`
- `codex-rs/network-proxy/`

### 第七层：持久化与诊断

一条 Thread 不是只存在内存里。

Codex 用 Thread Store（线程存储层）、Rollout（运行记录）和 State DB（状态数据库）保存可恢复状态；另外又有 Rollout Trace（运行追踪）保存更丰富的诊断证据。

相关代码：

- `codex-rs/thread-store/`
- `codex-rs/rollout/`
- `codex-rs/state/`
- `codex-rs/rollout-trace/`
- `codex-rs/analytics/`
- `codex-rs/otel/`

到这里，我们才有资格开始谈 Context、Memory、Tool。

---

## 2. Codex 自己的对象模型是什么

学习源码时最容易犯的错误，是先拿“Session / Run / Turn / Step”这种通用教学树去套产品。

Codex 自己更接近下面这套关系：

```text
Thread
长期会话容器
│
└── Session
    Core 内真正维护这条 Thread 的运行实例
    │
    ├── Turn
    │   一次用户输入驱动的一段 Agent 工作
    │   │
    │   ├── Sampling request #1
    │   ├── Tool call / Tool result
    │   ├── Sampling request #2
    │   ├── 用户中途 steer
    │   └── ...
    │
    └── 下一次 Turn
```

源码里还有 `StepContext`。它不是 App Server 协议里对用户公开的“Step”，而是 Core 在一次采样附近捕获的执行快照。它把当时的模型设置、工具表、环境与权限绑定在一起，避免“模型看到 A 版工具配置，但工具真正执行时已经变成 B 版配置”。

因此，本组文档不会把 `StepContext` 翻译成“一个用户可见步骤”。后文统一称它为：

> **StepContext（步骤上下文，一次模型采样与后续工具执行共享的运行快照）**

---

## 3. 一次真实 Turn 大致怎样流动

把代码细节先收起来，一次普通 Turn 可以先读成下面这个故事。

用户在 TUI、App 或非交互 CLI 中提交任务。产品层把它变成 Thread / Turn 请求，Core 找到或创建对应的 Session。Turn 开始后，Runtime 先检查有没有需要提前做的上下文压缩，再确定这次输入涉及哪些 Plugin、MCP Server、Skill 或环境。

然后 Session 捕获一个 `StepContext`。这一步相当于把“此刻这次采样应该使用的模型、工具、环境、权限和配置”拍成快照。

随后 Context 系统会把长期指令、项目指令、当前 World State、Memory、Skills、Plugin 信息、历史消息和本轮用户输入整理成模型真正可见的请求，同时 Tool Router（工具路由器）生成本轮允许模型调用的工具说明。

模型返回后有两种主要情况。

如果它给出最终回答，Turn 可以进入收尾。如果它发出 Tool Call（工具调用），Runtime 会检查工具是否存在、参数类型是否正确，再经过 Hook、权限、批准、沙箱和网络策略，最终执行工具。工具结果不会只打印到终端，而是会变成新的模型历史项，再进入下一次采样。

因此一条 Turn 的核心不是：

```text
用户 → 模型 → 答案
```

而是：

```text
用户输入
→ 捕获当前运行快照
→ 编译模型可见 Context 和 Tool Set
→ 模型决定
→ Runtime 执行动作
→ 结果写回历史
→ 再次编译请求
→ 直到完成、取消、失败或达到其他停止条件
```

这就是后面四篇文档共同围绕的主干。

---

## 4. 四篇正文分别追什么

### [01｜Context Lifecycle：上下文完整生命周期](01-context-lifecycle.md)

不从“Context 是什么”开始，而从 `TurnStart` 和 `run_turn` 开始，追：

用户输入怎样进入 Core；`StepContext` 怎样冻结当时的执行配置；`WorldState`、AGENTS.md、Developer Instructions（开发者指令）、Memory、Skills 等信息怎样进入模型请求；历史为什么平时只增量更新；Prompt Cache（提示缓存）和 WebSocket 增量续写怎样工作；Tool Result（工具结果）怎样进入下一轮；Context Window（上下文窗口）变大以后怎样触发不同类型的 Compaction（上下文压缩）；最后 Resume（恢复）和 Fork（分叉）怎样从持久化记录重新构造模型上下文。

### [02｜Memory Lifecycle：长期记忆完整生命周期](02-memory-lifecycle.md)

直接从源码中的三块 Memory 实现开始：

- `memories/write`
- `memories/read`
- `ext/memories`

然后追一条旧 Thread 怎样被选为 Memory 候选，Phase 1（第一阶段）怎样提取，Phase 2（第二阶段）怎样全局整理，最终怎样生成有界的 `memory_summary.md`；新 Session 怎样先看到摘要、再按需搜索更深证据；用户明确说“记住、忘掉、更新”时怎样走 ad-hoc note（临时追加记忆）路径；已经被实际使用的 Memory 怎样回写使用次数，并反过来影响后续保留和整理。

### [03｜Tool Lifecycle：工具完整生命周期](03-tool-lifecycle.md)

从 `ToolExecutor`、`ToolRegistry` 和 `ToolRouter` 出发，不把工具系统写成字段表。

重点解释：Core Tool、MCP Tool、Extension Tool 和 Dynamic Tool 怎样汇合到同一个 Registry；为什么“已经注册”不等于“模型这轮看得见”；大量 MCP Tool 为什么可以 Deferred（延迟暴露）并通过 `tool_search` 搜索；Skill（技能）为什么和 Tool 不是同一个概念；模型真正发出 Tool Call 以后，怎样经过 Hook、Approval、Guardian、Permission、Sandbox、Network，再进入真实执行；取消和失败又怎样保证历史仍然完整。

### [04｜Engineering & Evaluation：系统边界、故障、规模化与评测](04-engineering-evaluation.md)

这篇把前面三条链重新合在一起，并补上产品级的全局结构：

- CLI / App Server / Core 之间的产品边界；
- Extension Registry（扩展注册表）怎样把 Memory、Skills、MCP、Goal、Guardian 接入 Runtime；
- Multi-Agent（多智能体）与 Child Thread（子线程）；
- Code Mode（代码模式）与嵌套工具调用；
- Exec Server（执行服务器）和远端环境；
- Thread Store、Rollout、State DB、Rollout Trace 之间的区别；
- 网络断开、上下文超限、工具取消、沙箱拒绝等失败怎样由不同层处理；
- 大 Context、大 Tool Catalog、大 Skill Catalog 和长期 Memory 怎样避免把所有信息都塞给模型；
- 源码现有 Tests / Metrics / Trace 能证明什么，产品效果评测又还需要补什么。

---

## 5. 怎样区分“源码事实”和“工程解释”

每篇会尽量使用下面这种写法。

> **源码事实：** `ToolSearchHandler` 在固定快照中使用 BM25 建立延迟工具搜索索引。  
> **为什么这样设计：** 这让大量已注册工具不必全部进入首轮模型请求，从而减少 Tool Schema（工具模式定义）对 Context 的占用。  
> **不要误解：** 这不代表“Codex 永远只会用 BM25”，也不代表任何 Agent 都应该照搬 BM25。

这样做的目的，是避免把：

```text
我们认为合理的通用设计
```

写成：

```text
Codex 源码就是这样
```

---

## 6. 源码覆盖矩阵：这套文档具体核到了哪些系统

下面这张表不是“推荐阅读文件”，而是本文结论实际核验过的主干边界。一个机制只有同时找到定义、接入点或调用路径，才会写进正文。

| 系统边界 | 主要源码入口 | 在本文中的作用 |
|---|---|---|
| CLI / 产品命令入口 | `codex-rs/cli/src/main.rs`、`tui/`、`exec/` | 确认用户不是直接调用 Core；Resume、Fork、MCP、Plugin、Sandbox、App Server 等都是真实产品入口 |
| App Server 协议 | `app-server-protocol/`、`app-server/src/request_processors/` | 确认 Thread / Turn 的外部请求模型与 Core 内部执行模型怎样衔接 |
| Thread 创建与恢复 | `core/src/thread_manager.rs`、`core/src/codex_thread.rs` | 创建、恢复、Fork、维护活跃 Thread |
| Session / Turn Runtime | `core/src/session/`、`core/src/session/turn.rs` | 真正的 Agent Loop、StepContext、Context Window 与模型采样 |
| Session 长期服务 | `core/src/state/service.rs` | 核验 MCP、Extension、Tool、ModelClient、ThreadStore、Trace 等确实同时挂在 Session 上 |
| Extension 体系 | `ext/extension-api/`、`app-server/src/extensions.rs` | 核验 Memory、Skills、MCP、Goal、Guardian 等是通过正式生命周期接口接入，而非教材假设 |
| Context / History | `core/src/context/`、`context-fragments/`、`core/src/context_manager/` | 初始 Context、World State 差异、规范历史和模型可见片段 |
| Model request / cache | `core/src/client.rs`、`client_common.rs` | Prompt request、Prompt Cache key、WebSocket continuation |
| Compaction | `core/src/compact*.rs`、`session/context_window.rs` | Local / Remote / Token-Budget 三类 Context Window 迁移 |
| Memory 写入与读取 | `memories/write/`、`memories/read/`、`ext/memories/`、`state/src/runtime/memories.rs` | Phase 1、Phase 2、召回、引用、使用反馈、纠正和遗忘 |
| Tool Runtime | `tools/`、`core/src/tools/` | ToolExecutor、Registry、Router、Hook、Tool Search、并发和结果回填 |
| MCP | `codex-mcp/`、`rmcp-client/`、`core/src/mcp_tool_exposure.rs` | 外部 Tool catalog、MCP Runtime、暴露策略和执行 |
| Skills | `skills/`、`ext/skills/` | Skill catalog、预算、渐进式展开和 Tool / Context 接入 |
| 权限与执行环境 | `core/src/tools/orchestrator.rs`、`exec-server/`、`sandboxing/`、`network-proxy/` | Approval、Permission、Sandbox、Network 与本地 / 远端执行 |
| Multi-Agent | `core/src/agent/`、`core/src/tools/handlers/multi_agents_v2.rs` | 子 Agent 创建、消息投递、容量、预算和完成通知 |
| Code Mode | `code-mode/`、`code-mode-runtime/`、`core/src/tools/code_mode/` | 模型脚本和 nested Tool 怎样仍走统一 Tool Runtime |
| Thread Persistence | `thread-store/`、`rollout/`、`state/` | LiveThread、JSONL、SQLite 与 Resume / Fork 所需状态 |
| 深度诊断 | `rollout-trace/`、`analytics/`、`otel/` | 区分模型可见历史和真实 Runtime 事件，构造可回放证据 |
| 集成验证 | `core/tests/suite/`、各 crate tests | 验证 Context shape、MCP、Sandbox、Compaction、Multi-Agent、transport fallback 等真实路径 |

这张矩阵也说明一个重要的阅读边界：如果只从 `Context / Memory / Tool` 三个关键词搜索文件，很容易漏掉 App Server、Extension、Environment、Multi-Agent、Code Mode 和持久化边界，最后得到一个“看起来像 Agent 教材”的 Codex，而不是源码里的 Codex。

---

## 7. 源码阅读范围

这里的“完整”指的是：

> **对 Codex Agent Runtime 的主执行路径和所有直接参与 Context、Memory、Tool、Permission、Persistence、Recovery、Multi-Agent、Extension、Trace / Evaluation 的实现边界做完整追踪。**

它不意味着为了写 Agent 教材而逐行解释：

- Bazel 配置；
- 安装脚本；
- 发布流程；
- 每一个 TUI 组件；
- 每一个平台打包辅助工具。

这些代码当然属于仓库，但它们不会改变本文要解释的 Agent Runtime 语义。

源码核验至少从以下一级入口交叉确认：

`Cargo.toml` workspace → CLI / App Server → ThreadManager / Session → Turn loop → Extension API → Context / Memory / Tool → Exec / Sandbox → Thread Store / Rollout / State → Trace / Tests。

如果一个结论只在模板 Prompt 中出现、却找不到实际调用方，文档不会把它当成“已实现机制”。

---

## 8. 推荐阅读顺序

第一次不要边看源码路径边背类名。

建议按一个完整问题推进：

> **“我在 Codex 输入‘修复这个 bug’，接下来系统到底发生了什么？”**

先读本页建立产品地图，然后连续阅读：

```text
01 Context
→ 先看这次模型到底看见什么

02 Memory
→ 再看过去其他 Thread 的信息怎样跨 Session 进入今天的任务

03 Tool
→ 再看模型决定行动以后 Runtime 怎样真正执行

04 Engineering & Evaluation
→ 最后看故障、恢复、规模和如何证明系统有效
```

读完以后，应该能不依赖课程术语、直接用 Codex 自己的源码对象解释：

1. Thread（线程）、Session（运行实例）、Turn（轮次）、StepContext（步骤上下文） 分别解决什么问题；
2. 一条用户消息怎样变成模型请求；
3. 为什么历史不是每轮重新拼成一个巨大字符串；
4. Memory 为什么不是 Thread History 的别名；
5. 一万个工具为什么不应该全部直接暴露给模型；
6. 一个 Tool Call 为什么不能绕过 Approval / Sandbox；
7. Compaction 为什么不仅是“写一段摘要”；
8. Resume 为什么不是把 JSONL 从头读一遍；
9. Extension API 为什么是理解 Codex 能力系统的关键；
10. Tests、Metrics、Rollout Trace 和真正的任务级 Eval 各自能证明什么。
