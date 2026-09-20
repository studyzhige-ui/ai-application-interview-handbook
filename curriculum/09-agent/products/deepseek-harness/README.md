# DeepSeek Harness｜从事件日志与插件树理解一个 Agent Harness

[← 成熟产品源码学习](../README.md) · [Agent 模块](../../README.md)

> **源码仓库：** [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)  
> **固定源码快照：** [`ddefc45fbc7f8e46dd73185e68295696d1297887`](https://github.com/deepseek-ai/deepseek-harness/tree/ddefc45fbc7f8e46dd73185e68295696d1297887)  
> **快照版本：** `0.1.6-alpha.2`；仓库 README 明确标记为 **developer preview（开发者预览）**，兼容性仍可能发生破坏性变化。  
> **核验日期：** 2026-09-20

DeepSeek Harness 很容易被误读成“DeepSeek 自己做了一个类似 Claude Code 的 CLI Agent”。

从源码看，它真正有价值的地方不在 UI，而在一套更底层的 Agent Harness（智能体运行框架）思想：

> **几乎所有能力都是 Cordis Plugin（插件）；运行中的重要事实优先写进 Append-only Session Log（仅追加会话日志）；模型真正看到的上下文，则是从这份日志投影出来的当前 Surface（模型可见表面）。**

这和 Codex、Claude Code 的实现形态都不一样。

如果先拿别的产品的 Thread / Memory / Tool Registry 概念来套，很容易漏掉 DeepSeek Harness 最核心的设计：

~~~text
Cordis 插件树
     ↓
服务 / Event / Tool / Prompt Contribution
     ↓
Agent Loop
     ↓
SessionEvent Append-only Log
     ↓
Surface Projection
     ↓
Model Request
~~~

因此这组文档仍然坚持一条原则：

> **先把 DeepSeek Harness 自己的执行模型讲清楚，再讨论它和通用 Agent 概念的对应关系。**

---

## 1. 先理解“everything is a plugin”到底是什么意思

DeepSeek Harness 的官方架构文档直接写明：

> Every part of the product is a plugin.

这里不是营销用语。

源码确实把模型适配器、Session、Tool Registry、Agent Loop、Compaction、Sandbox、Subagent、Skill、MCP、Approval 等都做成 Cordis（插件运行框架）里的 Service / Plugin。

例如：

~~~text
ctx.sessions
Session Store

ctx.systemPrompt
System Prompt 组装服务

ctx.tools
Tool Registry + Execution Pipeline

ctx.agents
Live Agent Registry

ctx.agentLoop
默认 Agent Driver

ctx.compaction
可选 Compaction Capability

ctx.subagents
可选 Subagent Capability

ctx.approval
Approval Capability
~~~

这些能力不是硬编码在一个巨大 `Agent` 类里。

### 为什么这件事重要

因为 DeepSeek Harness 的扩展方式不是：

> “到核心循环里再加一个 if。”

而更接近：

~~~text
定义一个能力 seam（接缝）
→ Provider 实现它
→ Consumer 使用它
→ Cordis 负责生命周期和依赖
~~~

例如 Compaction 分成：

~~~text
dsh-compaction
定义 ctx.compaction 接口

dsh-compaction-basic
提供默认实现

dsh-command-compact
消费这个能力，暴露 /compact
~~~

换成另一个 Compaction backend，不需要重写 Agent Loop。

---

## 2. 真实产品不是所有插件全开，而是 Profile / Bundle 组装出来的

仓库里存在很多 Package，不代表默认产品每次都会把它们全部装上。

DeepSeek Harness 用 Bundle / Profile 组合产品能力。

架构文档列出的主要 Profile 包括：

- `web`
- `headless`
- `sdk`
- `sdk-minimal`
- `acp`

其中 `dsh-base` 是多个 Profile 的共享底座。

固定快照里的 `packages/bundle/base/cordis.patch.yml` 能看到默认组合的重要事实，例如 Base 默认安装：

- LLM；
- Session；
- JSONL Session Persistence；
- Tool Runtime；
- System Prompt；
- Agent Loop；
- Sandbox；
- Approval / Permission Preset；
- Filesystem / Bash；
- Agent Instructions；
- Skill；
- Token Meter；
- Basic Compaction；
- Tool Result Pruner；
- Subagent Spawn / Fork；
- LLM Retry；
- MCP Resource 支持；
- Web Search / Fetch 等。

所以后面的正文会区分：

> **仓库提供的能力**

和

> **Base-backed shipped profile 默认组合的能力**

而不会因为源码目录存在一个 Package，就说它一定在所有运行模式中启用。

---

## 3. DeepSeek Harness 最重要的不变量：Model-visible means logged

理解这个产品，最值得先记住一句源码架构原则：

> **Model-visible means logged.**

也就是：

> **只要模型真正能看到某段上下文，它原则上就应该先成为可恢复的 Session Fact（会话事实），或者能由持久事实确定性重建。**

这会影响整个运行时设计。

例如：

- User Input 最终是 `user/message`；
- System Prompt 是 `system/message`；
- Assistant 完整结果是 `assistant/message`；
- Tool Call 是 `tool/call`；
- Tool Result 是 `tool/result`；
- Skill Catalog 是持久 user-role context；
- Approval policy / Sandbox mode 的改变有 durable event；
- Compaction summary 最终通过 replacement `user/message` 进入 Surface；
- Cross-session reference 被捕获成当前 Session 内的不可变 snapshot。

而像：

- live streaming chunk；
- `turn/start` / `step/start`；
- approval audit；
- retry bookkeeping；

这些可以写进 Session Log，但不一定进入模型 Surface。

所以：

~~~text
Session Log
≠
Model Context

Model Context
= Session Log 上的一个可重建 Surface Projection
~~~

这条边界是后面所有章节的主线。

---

## 4. 一次用户请求在源码里到底怎样跑

先不要看细节，先把一次完整 Agent Turn（智能体轮次）讲成故事。

用户提交：

> “找出测试失败原因并修复，不要修改公开 API。”

消息先进入 Agent Inbox（智能体待处理队列）。

Agent Loop 打开一个新的 durable：

`turn/start`

然后每一轮模型采样前，会执行 `agent/pre-step`。

在这一阶段，插件可以加入：

- Workspace Instructions；
- Session Reference；
- Runtime Context；
- Skill Catalog；
-用户显式 Skill 内容；
-其他当前 Step 需要的 Context。

随后 Runtime 组装：

- System Prompt；
- Tool Schemas；
-当前 User-role Context。

但此时这些新消息**还没有立刻写进 Session**。

接下来先经过：

`agent/request`

和：

`ctx.llm.prepareCall()`

把 provider / model / reasoning 等最终路由解析完。

只有这个阶段成功以后，Agent Loop 才提交：

- `system/message`
-这一 Step 被接受的 `user/message`
-必要的 `request/header`
-`request/context`

然后调用：

`session.deriveMessages()`

从当前 Surface 推导出真正要发送给模型的 history，并冻结这份 request。

模型开始流式输出。

Live Streaming 通过 `agent/assistant-stream` 提供给 UI 和观察者，但它不是 replay 真源。

流结束以后才落成：

-成功：`assistant/message`
-失败 / 中断：必要时 `assistant/attempt`

如果 Assistant 包含 Tool Call：

~~~text
tool/call
→ ToolRuntime pipeline
→ tool/result
~~~

Tool Result 再进入 Session Surface，于是 Agent Loop 进入下一 Step。

直到没有 Tool / Steering continuation，Turn 才写：

`turn/end`

所以 DeepSeek Harness 的核心循环可以概括成：

~~~text
Inbox
→ Pre-step Context Composition
→ Request Routing
→ Durable Admission
→ Surface Projection
→ LLM Stream
→ Durable Assistant Settlement
→ Tool Execution
→ Durable Tool Result
→ 下一 Step
~~~

---

## 5. 为什么它不是“messages 数组 + while loop”

很多简单 Agent 框架的状态中心是：

~~~text
messages = [...]
~~~

DeepSeek Harness 的状态中心是：

~~~text
append-only SessionEvent Log
              ↓
         Surface Projection
              ↓
        deriveMessages()
~~~

Surface 是当前模型应该看到的节点序列。

这允许 Runtime 做一些非常重要的事情。

### 压缩旧历史但不删除证据

Compaction 可以：

~~~text
原始事件仍然存在

A B C D E
│ │ │ │ │
└───────┘
   被新的 summary node shadow

Surface:
Summary D E
~~~

历史证据没有物理改写，模型可见视图却缩小了。

### Tool Result 可以被替换，但原始结果仍有来源

Tool Result Pruner 可以生成一个新的 `tool/result` replacement，并用 `sourceEventSeqs` 指向原始节点。

### Resume 可以重新投影当时的语义状态

不需要相信某个进程退出前恰好保存的 `messages` 数组。

这就是 Event Sourcing（事件溯源）思想在 Agent Runtime 里的具体落地。

---

## 6. Context Lifecycle 学什么

[01｜Context Lifecycle](01-context-lifecycle.md) 会从“用户这一轮输入以后，模型究竟看到什么”出发，连续追：

- Inbox 的 next-turn / next-step；
- `agent/pre-step` 怎样接纳 Context；
- System Prompt sections / contexts / Tool Schema 怎样组装；
- AGENTS.md / CLAUDE.md 怎样成为 durable context；
-为什么 Request Routing 成功以后才真正 commit User / System Message；
- `request/header` 与 `request/context` 怎样保存模型请求 envelope；
-`deriveMessages()` 怎样从 Surface 投影 history；
- Streaming 为什么不是 replay source；
- Tool Result 怎样回到 Context；
-Compaction / Pruning 怎样替换 Surface 而不改写原始 log；
-为什么 Compaction Summarizer 刻意重放相同 Prompt / Tools 前缀来复用 KV Cache。

---

## 7. Memory Lifecycle 为什么这次标题会和前两个产品不同

[02｜Memory Lifecycle](02-memory-lifecycle.md) 最重要的源码结论不是“DeepSeek Harness 的 Memory 怎么实现”，而是：

> **当前固定源码没有内建自动语义长期 Memory 系统。**

这必须忠于源码。

DeepSeek Harness 的长期信息边界实际是：

~~~text
AGENTS.md / CLAUDE.md
人工维护的 Workspace Instructions
≠
Memory

Session Log
当前 Session 的持久历史真源
≠
语义长期 Memory

Session Reference
把另一个 Session 的有限只读 Snapshot
注入当前 Session

Third-party Memory via MCP
真正的跨 Session 语义 Memory
由外部 Provider 负责
~~~

仓库甚至有明确设计记录：直接把某个 Memory 厂商 API 做进 DSH 会扩大产品表面；长期 Memory 已经可以通过通用 MCP boundary 表达，所以官方提供的是 **default-off MCP Memory 示例**，不是一个 DSH Universal Memory Service。

这篇会重点讲：

- Session History 和 Memory 的区别；
- Cross-session Reference 怎样防止旧 Session 内的指令变成 Prompt Injection；
-为什么 Reference 是 Snapshot 而不是 live link；
-第三方 Memory 写入 / 新 Session Recall 怎样通过 MCP 验证；
- Memory Provider 自己负责 embedding、storage、forgetting、conflict resolution 的边界。

---

## 8. Tool Lifecycle 学什么

[03｜Tool Lifecycle](03-tool-lifecycle.md) 会追完整链路：

~~~text
Plugin register ToolDefinition
→ Scoped Tool Registry
→ SystemPrompt.assemble() 得到 ToolSchema
→ Model tool-call
→ durable tool/call
→ argument validation
→ tools/pre-execute
→ monotonic guard
→ approval
→ tools/execute wrappers
→ Tool body
→ tools/post-execute
→ finalizeContent
→ tools/result observer
→ durable tool/result
→ 下一 Step
~~~

还会重点覆盖：

- Canonical JSON Value（规范工具值）和 model-facing content 为什么分开；
-为什么 Tool Argument 不允许在 Permission 后偷偷重写；
-Native Function Calling 与 PTC（Programmatic Tool Calling，程序化工具调用）；
-PTC 怎样让模型写 TypeScript，并通过 binding 再调用普通 Tool；
-MCP Tool 怎样原子换代、断线重连；
-Skill 为什么先发布 catalog，再按需加载正文；
-Approval / Permission Preset / Sandbox 是哪三层不同概念。

---

## 9. Engineering & Evaluation 学什么

[04｜Engineering & Evaluation](04-engineering-evaluation.md) 会把长期运行问题放回来：

- JSONL / Zstd Session Persistence；
- torn-tail crash recovery；
- interrupted Turn 怎么补 synthetic closer；
-为什么 Session format generation 不原地覆盖旧版本；
-LLM Retry 为什么“先 durable，再 sleep”；
-Context Overflow 如何通过 Compaction 形成有证据的 retry；
-Spawn / Fork Subagent 的 Context 差异；
-Continuable Subagent 怎样 cold resume；
-为什么 Fork 只继承 completed turns；
-Subagent Tool Scope 为什么不继承 Parent Authority；
-Plugin unload / provider replacement 怎样不破坏已接受运行；
-仓库里的 invariant companion、contract suite、catalog verifier、snapshot test、with-key e2e 分别证明什么。

---

## 10. 源码覆盖矩阵

| 系统边界 | 主要源码 / 文档 | 当前快照中确认的职责 |
|---|---|---|
| 产品架构 | `docs/architecture.md` | Cordis plugin tree、Profile / Bundle、capability seam |
| Agent 公共接口 | `packages/core/agent/` | Agent Registry、Inbox、Create / Resume、live events |
| Agent Driver | `packages/core/agent-loop/` | Turn / Step、Request、Streaming、Tool Loop |
| Session | `packages/core/session/` | Append-only events、Surface、`deriveMessages()` |
| System Prompt | `packages/core/system-prompt/` | Section / Context / Variables / Tool Schema assembly |
| Workspace Instructions | `packages/context/agent-instructions/` | AGENTS.md / CLAUDE.md baseline + nested change injection |
| Cross-session Context | `packages/context/session-reference/` | 有界、只读、untrusted session snapshot |
| Compaction | `packages/compaction/*` | Surface replacement、summary transaction、pruning、overflow recovery |
| Token Pressure | `token-meter` + Compaction | 统一 replay pricing 与阈值判断 |
| Tool Runtime | `packages/core/tools/` | Tool Registry、validation、policy、dispatch、result |
| PTC | `packages/core/tools/src/ptc.ts` + `ptc-runtime-node` | 程序化 Tool 调用、隔离 Node runtime |
| Approval | `packages/interaction/user-approval/` | 一次性批准、audit、fail-closed |
| Permission Preset | `packages/interaction/permission-presets/` | sandbox + approval 两个独立机制的用户级组合 |
| Sandbox | `packages/sandbox/*` | per-call filesystem policy、平台 provider、fail-closed |
| Skills | `packages/skill/*` | catalog、按需正文加载、显式 invocation |
| MCP | `packages/mcp/mcp-client/` | 连接、工具发现、原子 generation、重连、资源 |
| 内建长期 Memory | — | **当前没有 Universal Semantic Memory Service** |
| 外部长记忆 | `docs/user/guide/mcp-memory.md` | 通过 MCP Provider 接入，默认关闭 |
| Session Persistence | `packages/session/session-persistence-jsonl/` | JSONL / Zstd、单 writer、crash recovery、format migration |
| LLM Retry | `packages/llm/llm-retry/` | request-error waterfall、durable-before-wait retry |
| Subagent | `packages/subagent/*` | provider seam、spawn / fork、continuation、control |
| 默认组合 | `packages/bundle/base/cordis.patch.yml` | Base-backed profiles 实际加载的能力 |
| Tests / Gates | `package.json`、各 package tests、scripts | contract、invariant、catalog、snapshot、e2e、perf gates |

---

## 11. 这份源码最值得横向比较的四个设计选择

### 一：Context 本身是一个 Projection，而不是唯一真源

Codex / Claude Code 都有自己的持久化和 Context 变换机制。

DeepSeek Harness 更彻底地把：

~~~text
Durable Log
和
Model-visible View
~~~

分开。

这使 Compaction / Tool Result Pruning 不需要物理删除证据。

### 二：运行时扩展优先用 Event / Service Seam

Context Injection、Retry、Compaction、Approval 都不是不停修改一个 Agent Loop。

Agent Loop 提供稳定的事件接缝：

~~~text
agent/pre-step
agent/request
agent/request-error
agent/turn-stopping
tools/pre-execute
tools/execute
tools/post-execute
~~~

插件挂到这些 seam 上。

### 三：Memory 没有被为了“功能完整”强行内建

这是一个很值得学习的产品边界。

源码没有因为 Agent 产品“应该有 Memory”就造一个 Universal Memory DB。

已有 MCP 足以表达第三方长期记忆时，官方选择把 Provider-specific responsibility 留在外部系统。

### 四：Recoverability 被当成 Runtime Contract

很多动作都先留下 durable evidence，再进行异步工作：

~~~text
retry event
→ sleep
→ retry started

compaction/start
→ summary
→ replacement
→ compaction/end

approval/asked
→ external answer
→ approval/decided
~~~

这让 crash / cancel / resume 不再只能靠“猜上一次运行到哪里”。

---

## 12. 阅读顺序

建议按下面顺序读：

~~~text
README
先建立 Event Log / Surface / Plugin Tree 心智模型

01 Context
看一条用户输入怎样变成真正 Model Request

02 Memory
先纠正“持久历史 = 长期记忆”的误区

03 Tool
看 Capability 如何发现、授权、执行、回填

04 Engineering & Evaluation
看 Crash、Retry、Resume、Subagent、测试如何闭环
~~~

读完以后，应该能够不用背文件名，自己解释以下问题：

1. 为什么 DeepSeek Harness 的 Session Log 和模型 Context 不是同一个东西？
2. 为什么 `agent/request` 成功以后才提交当前 Step 的 System / User Message？
3. Surface replacement 为什么能压缩模型 Context，却仍然保留原始历史证据？
4. AGENTS.md / CLAUDE.md 为什么是 Instructions，而不是 Memory？
5. 为什么 DSH 当前不内建 Universal Semantic Memory？
6. Tool Runtime 为什么把 canonical value 和 model-facing content 分开？
7. 为什么 `tools/pre-execute` 后面还需要 monotonic guard？
8. Permission Preset、Approval、Sandbox 分别管什么？
9. PTC 为什么不是绕过 Tool Runtime，而是再次经过同一 Tool Pipeline？
10. LLM Retry 为什么必须在 sleep 之前先写 durable event？
11. Fork Subagent 为什么只继承 parent 的 completed turns？
12. Resume 为什么需要修复 interrupted turn，而不是单纯重新载入 JSONL？

下一篇：[Context Lifecycle →](01-context-lifecycle.md)
