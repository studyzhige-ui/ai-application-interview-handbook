# OpenAI Codex｜从真实源码入口理解一个成熟 Coding Agent

[← 成熟产品源码学习](../README.md) · [Agent 模块](../../README.md)

> **源码仓库：** [openai/codex](https://github.com/openai/codex)  
> **固定快照：** [`5c5308fc9a9ee789049d646ef11e5400384b9c6f`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f)  
> **核验日期：** 2026-09-20  
> **当前性确认：** 本次重写时再次核验，该 commit 仍是 `openai/codex` 的 `main` HEAD。递归读取的源码树包含 9,254 个路径且 GitHub 返回 `truncated: false`。

Codex 的根 README 只用一句很朴素的话定义自己：它是一个在本地计算机上运行的 coding agent（编程智能体）。但真正打开源码后，会发现“本地运行”并不意味着“一个终端程序里写了一个模型循环”。当前 Rust workspace（Rust 工作区）已经拆成一百多个 crate（Rust 包），覆盖客户端入口、应用服务器、核心执行、执行环境、MCP、Skills、Memory、持久化、状态数据库、沙箱、网络策略、多 Agent、诊断和可观测性。

所以这组文档先不急着问“Codex 的 Memory 怎么做”。第一步应该先回答：

> **用户敲下一个任务以后，究竟经过哪些真实边界，最后才到模型和工具？**

---

## 1. 先看 Codex 的真实产品入口

`codex-rs/cli/src/main.rs` 是一个很重要的起点。它表明 `codex` 可执行文件并不是只有一种运行方式。

不带子命令时，参数会进入交互式 TUI（Terminal User Interface，终端用户界面）。此外，同一个 CLI 还提供非交互 `exec`、代码审查 `review`、MCP 管理、插件管理、App Server、远程控制、沙箱调试、Resume（恢复）、Fork（分叉）、Queue（排队消息）、Exec Server（执行环境服务）等入口。

这件事先帮我们纠正一个容易产生的误解：

> **`codex-core` 是 Agent 语义的核心，但它不是“整个 Codex 产品”。**

对于当前交互式 TUI，源码中的 `tui/src/app_server_session.rs` 明确把自己称为 “App-server session facade”。TUI 通过类型化 JSON-RPC（JSON 远程过程调用）和 App Server Client（应用服务器客户端）完成线程创建、恢复、分叉、Turn 启动、Steer（运行中追加指令）、Interrupt（中断）、Skills 查询、Memory 模式、审批等操作。它可以连接进程内 App Server，也可以连接远程 App Server。

因此更真实的主干是：

~~~text
用户 / IDE / TUI / 其他客户端
          ↓
      App Server 协议层
  校验请求、管理订阅和通知
          ↓
      ThreadManager
  创建、恢复、分叉 Thread
          ↓
   CodexThread / Session
  驱动一个长期 Agent 会话
          ↓
     Turn → 多次 Step
  模型采样 ↔ 工具 / 子 Agent
          ↓
执行环境 / Sandbox / MCP / Code Mode
          ↓
 Thread Store + Rollout + State DB
          ↓
恢复、查询、Memory、诊断
~~~

非交互 Exec 等入口可以有不同宿主路径，但最终共享大量 `codex-core` 的执行语义。这也是为什么读 Codex 不能只从 TUI 的 UI 组件开始，也不能只搜 `session/turn.rs` 就认为读完了产品。

---

## 2. App Server 不是“薄转发层”

App Server（应用服务器）做的事情比把 JSON 转给 Core 多得多。

`app-server/src/message_processor.rs` 在进程级创建并持有 `ThreadManager`、`ThreadStore`、环境管理器、认证、Queue（队列）、Goal（目标）服务和扩展注册表。源码还特意注明：Thread Store 是 **process-scoped（进程级）** 的；配置热加载可以改变单个 Thread 的行为，但不能让已经存在的 Thread 突然搬到另一种持久化后端或另一个存储根目录。

`request_processors/turn_processor.rs` 则负责公共 Turn 接口。它会先校验输入，例如拒绝不允许的远程图片 URL、检查用户输入长度，再把 `turn/start`、`turn/steer`、`turn/interrupt` 等 RPC 转换成 Core 能理解的操作。

这意味着用户输入真正进入 Agent Loop（Agent 执行循环）之前，已经经过了一个产品级边界：

~~~text
外部请求
→ 协议与输入校验
→ 找到目标 Thread
→ 形成 Core Operation
→ 才进入 Session / Turn
~~~

理解这个边界很重要，因为有些错误应该在这里直接拒绝，而不是让模型看到以后“自己决定”。

---

## 3. Thread、Turn 和 Step 是源码里的真实层级

在本书通用课程里，我们会为了教学定义自己的 Run / Turn / Step。到了 Codex 源码，必须服从它自己的对象语义。

### Thread：长期会话容器

`ThreadManager` 负责创建并维护 Thread。它可以启动新 Thread、恢复持久化 Thread、Fork 旧 Thread，也可以为 Multi-Agent（多智能体）场景从父 Thread 派生子 Agent。

一个 Thread 不是只有聊天文本。创建时还会绑定配置、模型提供方、执行环境、MCP 能力、插件选择、扩展状态、持久化方式和认证等运行条件。

### Turn：一次用户任务推进

Codex 的 Turn 通常从一批用户输入开始，直到这批工作停止、完成、被中断或报错。**一个 Turn 内可以有很多次模型采样，也可以执行很多个工具。**

因此不能把“模型请求一次”叫成 Codex Turn。

### Step：一次模型采样所使用的精确快照

`StepContext（步骤上下文）` 是理解 Codex 的关键对象之一。源码对它的注释是 “Request-scoped state that may change between model sampling requests”，也就是：

> **它保存一次模型请求使用的、在后续采样之间可能变化的那份运行时快照。**

它会固定当时的模型设置、环境、MCP Binding（MCP 绑定）、Tool Router（工具路由计划）、已加载的 `AGENTS.md` 等内容。这样模型在某一步看到的能力，与稍后真正执行那一步产生的 Tool Call（工具调用）保持一致。

举个最容易理解的例子：模型在 Step A 看到了某个 MCP 工具的旧版本；随后 MCP Catalog（工具目录）刷新。如果旧 Tool Call 延迟到刷新后才执行，Codex 仍然需要知道“这次调用是基于 Step A 那份能力视图产生的”，不能悄悄按新目录解释。

---

## 4. Extension Registry 是把成熟产品能力接入 Core 的关键层

上一版文档把 Memory、Skills、Guardian、MCP 等分别讲了，却没有先讲清楚它们为什么能进入同一个 Runtime。当前源码给出的答案是 `ExtensionRegistry（扩展注册表）`。

`ext/extension-api` 定义了一组类型化贡献点。扩展可以在不同生命周期提供能力，例如：

- Thread 创建、恢复、空闲和停止时执行自己的逻辑；
- Turn 开始、完成、异常时维护自己的状态；
- 给模型上下文贡献 Prompt Fragment（提示片段）或 World State（世界状态）；
- 提供 MCP Server、原生 Tool 或 Tool 生命周期观察器；
- 在审批发生时参与 Approval Review（批准审查）。

这里列出这些入口不是为了让你背接口名，而是为了说明一个架构关系：

> **Core 不需要把每一种产品功能硬编码成一条特殊分支；App Server 在创建 ThreadManager 时把一组扩展注册进去，Core 在稳定生命周期点调用它们。**

当前 `app-server/src/extensions.rs` 实际安装的扩展包括 Queue、History Notes（历史备注）、Goal、Git Attribution（Git 归因）、Guardian V2、Memories、MCP、插件 MCP、Web Search（网页搜索）、Image Generation（图像生成）和 Skills。Skills 还同时接入 Executor（执行器）、Orchestrator（编排器）和 Host（宿主）三个来源。

这就是后面几篇文档能把 Memory、Skills、Guardian 放在同一个系统里解释的源码基础。

---

## 5. Core 内部真正负责什么

`codex-core` 承担 Agent Runtime 的核心语义：Thread 内的 Session（会话运行时）、Turn 循环、模型请求、Context（上下文）与 World State、Tool Router、MCP 调用、审批与沙箱、多 Agent、Compaction（上下文压缩）、恢复和事件映射等。

可以把它理解成：

> **App Server 负责把产品请求组织成运行时操作；Core 负责让这次 Agent 工作在正确状态下真正向前推进。**

但 Core 也不会自己承担所有副作用。它还依赖专门的执行与平台层，例如 Exec Server（执行环境服务）、Sandbox（沙箱）、Network Proxy（网络代理 / 网络策略）、MCP Client、Code Mode Runtime（代码模式运行时）等。

---

## 6. 执行环境不是一把裸 Shell

当模型要执行命令时，Codex 并不是简单调用本机 `subprocess`。

当前 workspace 中有独立的 `exec-server`、`exec-server-protocol`、`sandboxing`、`linux-sandbox`、`windows-sandbox-rs`、`network-proxy`、`execpolicy` 等 crate。Step Context 也保存了 Environment Snapshot（环境快照）和选中的 Capability Root（能力根目录）。

这套设计让一次命令执行能够回答：

- 在哪个执行环境运行？
- 哪些目录可读、可写？
- 是否允许网络？
- 是否需要用户批准？
- 这个 Tool 是否可以申请更高权限？
- 如果第一次被沙箱拒绝，是否允许受控重试？

后面的 Tool Lifecycle 会沿源码把这条链完整展开。

---

## 7. 持久化有两类信息，不要都叫“历史”

Codex 同时存在 Rollout / Thread Store 和 State DB（状态数据库），它们用途不同。

`ThreadStore` 是 Thread 的持久化边界。Local Thread Store（本地线程存储）会把 canonical history（规范化历史）写入 Rollout JSONL 文件；`LiveThread` 则是活动 Thread 的首选持久化 API。

`codex-state` 是 SQLite-backed state（SQLite 状态层）。它从 Rollout 中提取可查询元数据，同时还承载 Queue、Goal、Memory Job 等运行状态。

可以先这样理解：

~~~text
Rollout / Thread Store
更接近“发生过什么，未来怎样恢复模型上下文”

State DB
更接近“为了快速查询和运行协调，需要哪些结构化状态”
~~~

它们会互相配合，但不是同一份数据换两个文件格式。

---

## 8. Multi-Agent 不是独立产品外壳，而是 Thread 系统上的派生执行

Codex 当前 Multi-Agent V2（多智能体第二版）把子 Agent 建在 Thread / Agent Control 体系上。

模型可以通过 `spawn_agent` 创建子 Agent，通过 `send_message` 传消息，通过 `followup_task` 给已有 Agent 新任务，还可以等待、中断和列出 Agent。`ThreadManager::spawn_subagent` 会从父 Thread 派生子 Thread；`ext/agent::AgentRunner` 也通过这个能力启动隔离的 Agent 执行。

源码的 Prompt 还明确说明多个 Agent 共享目录和文件系统，因此“多 Agent”并不意味着天然有文件隔离。共享工作区带来的并发冲突，是运行时和上层协作策略必须处理的问题。

Rollout Trace（运行轨迹）也把父子 Thread 和任务 / 消息传递记录为 interaction edge（交互边），这让多 Agent 的真实信息流可以在事后重建。

---

## 9. 四篇专题从真实架构中继续往下追

有了前面的产品地图，再进入四条生命周期就不会误以为 Codex 源码本身只有四个模块。

### [01｜Context Lifecycle](01-context-lifecycle.md)

从 `turn/start` 开始，沿 App Server → Core Turn → Step Context → World State → Model Request（模型请求）追踪一次上下文怎样形成；再继续看 Tool Result（工具结果）、Prompt Cache（提示缓存）、Compaction 和 Resume（恢复）。

### [02｜Memory Lifecycle](02-memory-lifecycle.md)

先确认 Memory Pipeline（记忆流水线）真实从哪里触发，再追 Phase 1（第一阶段提取）、Phase 2（第二阶段全局整理）、Memory Extension（记忆扩展）、召回、引用、使用反馈、纠错和遗忘。

### [03｜Tool Lifecycle](03-tool-lifecycle.md)

从 Core Tool、MCP、Extension、Dynamic Tool（动态工具）、Code Mode 和 Skills 的不同来源开始，追到 Tool Registry（工具注册表）、按需发现、审批、Guardian、Sandbox、并发、取消、真实执行和结果回填。

### [04｜Engineering & Evaluation](04-engineering-evaluation.md)

把入口、Core、执行、持久化、多 Agent 和可观测性重新合在一起，看错误分类、网络重试、WebSocket → HTTP 降级、恢复、Trace 和测试。评测部分会明确区分“源码已有验证”与“基于源码设计的课程评测方案”。

---

## 10. 这次源码核验发现了一处仓库内部说明滞后

这是理解“为什么必须读调用点”的一个真实例子。

`codex-rs/memories/README.md` 当前仍写着：

> Runtime orchestration for Phase 1 and Phase 2 still lives in `codex-core` under `codex-rs/core/src/memories/`.

但在本次固定 commit 的完整目录树中，**不存在 `codex-rs/core/src/memories/`**。

真实调用点位于：

`codex-rs/app-server/src/request_processors/turn_processor.rs`

这里在有输入的 Turn 成功启动后，并且线程的主执行环境已经配置时，调用：

`codex_memories_write::start_memories_startup_task(...)`

Memory 写入流水线本身则已经位于 `codex-rs/memories/write`。

因此后面的 Memory 文档以当前代码和测试为准，不沿用这句已经滞后的目录说明。这也是本组源码学习采用“目录树 → 调用点 → 测试 → 注释 / README”核验顺序的原因。

---

## 11. 源码覆盖地图

下面这张表不是“推荐你一次把所有目录背下来”，而是本次完整性审查的范围记录。每一层都已经进入后续正文或系统总览。

| 行为层 | 当前主要源码位置 |
|---|---|
| CLI 与产品入口 | `codex-rs/cli`、`codex-rs/tui`、`codex-rs/app-server*`、`codex-rs/exec` |
| Thread / Turn / Step | `codex-rs/core/src/thread_manager.rs`、`core/src/session/`、`core/src/codex_thread.rs` |
| 上下文与 Prompt | `core/src/context/`、`context_manager/`、`context-fragments`、`prompts` |
| 模型通信 | `core/src/client.rs`、`model-provider`、`codex-api`、`websocket-client` |
| Tool 与 Code Mode | `core/src/tools/`、`codex-rs/tools`、`code-mode*` |
| MCP / Connector / Plugin | `codex-mcp`、`rmcp-client`、`connectors`、`plugin`、`core-plugins`、`ext/mcp` |
| Skills / 扩展 | `skills`、`ext/skills`、`ext/extension-api`、`app-server/src/extensions.rs` |
| Memory | `memories/read`、`memories/write`、`ext/memories`、`state/src/runtime/memories.rs` |
| 权限与执行隔离 | `sandboxing`、`execpolicy`、`network-proxy`、平台 sandbox crate |
| 持久化与状态 | `thread-store`、`rollout`、`state` |
| Multi-Agent | `core/src/agent/`、`ext/agent`、`agent-graph-store`、collaboration tools |
| Guardian / 审批审查 | `core/src/guardian`、`ext/guardian-v2`、Extension Approval Review |
| 诊断与观测 | `analytics`、`otel`、`rollout-trace`、各层 integration tests |

这张地图的目的只有一个：当后面看到某个结论时，你能判断它属于产品哪一层，而不会把一个局部实现误认为整个 Codex。

---

## 12. 读完本组材料应该能自己重建什么

你不需要背完所有 crate 名称。更重要的是能从一条真实任务重新推导：

~~~text
用户从某个客户端提交任务
→ App Server 做产品协议和输入边界
→ ThreadManager 找到或创建长期 Thread
→ Turn 开始
→ 每次采样前捕获 Step Context
→ Context + Tool Plan 形成模型请求
→ 模型产生文本、工具调用或协作动作
→ Runtime 在权限、沙箱和执行环境中处理
→ Observation 回到历史，继续下一次采样
→ Context 过大时进入 Window / Compaction 生命周期
→ Canonical history 持久化
→ Memory 在独立后台流水线中从历史提炼长期知识
→ Resume / Fork 从持久化状态恢复
→ Metrics / Trace / Tests 帮助判断哪里出了问题
~~~

后面四篇就是把这条主线逐层放大，而不是另起四套互不相干的知识点。
