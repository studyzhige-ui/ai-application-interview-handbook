# DeerFlow 2.0｜沿一次任务理解智能体怎样工作

[← Agent 产品源码学习](../README.md) · [通用 Agent 课程](../../../curriculum/09-agent/README.md) · [技术证据索引](../../../references/agent/README.md)

DeerFlow 是能够调用工具、处理文件并委派子任务的智能体系统。本组文档沿它的真实实现，学习一个用户请求怎样变成模型输入、工具操作、可继续的会话状态和可核对的执行记录。它是产品源码学习，不把 DeerFlow 的选择当成所有 Agent 的唯一标准。

**阅读前提：** 能理解 Python 函数、字典、异常和异步调用；知道模型可以返回工具调用，而工具由程序执行。需要回补时，先读 [Agent Loop](../../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md) 和 [工具执行](../../../curriculum/09-agent/docs/06-ToolExecutionAndFailure.md)。本组仍会就地解释检查点、中间件和作用域，不要求先背完框架 API。

## 核心设计

假设用户提出一个任务：

> 分析支付页重复提交的问题，必要时查询监控。这次只做最小修复，不要发布。我的长期习惯是先解释风险，再给方案。

这是贯穿四篇正文的**教学场景**，不是上游生产案例或实测结果。我们把示例用户、会话和运行分别记为 `u1`、`t1`、`r1`。

模型可以判断下一步应查日志还是读代码，却不会自动保存进度、打开一个安全的执行环境，或保证“不要发布”在长对话后仍有效。DeerFlow 在模型外组织这些责任：网关接纳请求，运行工作器组装主智能体，LangChain / LangGraph 执行模型与工具循环，中间件在明确时点处理输入、权限、状态和结果。默认完整产品入口是嵌入运行环境的 Gateway（网关），不是另起一套裸 LangGraph Server。[源码入口与部署边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/ARCHITECTURE.md)

```text
用户请求
   │
   ▼
Gateway：确认用户与会话，创建本次 Run
   │
   ▼
Run Worker：取得配置，组装主智能体
   │
   ▼
LangChain / LangGraph 执行骨架
   ├─ 中间件准备本轮 ModelRequest
   ├─ 模型回答，或提出 Tool Call
   ├─ 程序检查调用，执行工具，回填结果
   └─ 继续下一次模型调用，或结束
   │
   ├─ Checkpoint：保存以后继续所需的状态
   ├─ Run Journal：记录执行事件
   ├─ Workspace / 外部服务：承接真实副作用
   └─ DeerMem：在允许时异步提取长期用户信息
```

图中的几条保存路径不能互相代替。检查点中有“已经写文件”的消息，不保证文件还在；日志中有一次工具成功事件，也不自动证明文件内容符合业务要求。

## 1. 先认清四个运行对象

| 对象 | 在本例中是什么 | 为什么需要单独区分 |
|---|---|---|
| Thread（会话容器） | 用户围绕支付问题持续交谈的 `t1` | 可以承载多次用户请求和多次运行 |
| Run（一次运行） | 处理本次请求的 `r1` | 有独立身份、预算、取消和结束状态 |
| ThreadState（会话状态） | 消息、历史摘要、委派记录及文件环境标识等 | 决定智能体接下来怎样继续，不等于全部都发送给模型 |
| ModelRequest（一次模型请求） | 循环中某一次真正送入模型的消息和工具说明 | 是从状态与本次运行条件组装出的视图，可以临时增删内容 |

“Turn”在不同框架和界面中含义并不统一。本文说“用户轮次”时，指一次用户输入及其处理；说“模型调用”时，明确指一次模型请求，避免把工具循环次数与用户轮次数混算。[状态定义](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py) · [主智能体组装](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py)

## 2. 一次任务怎样经过系统

**接纳。** 网关确认用户身份和会话归属，并固定本次运行所需的项目等服务端上下文。来自客户端的同名字段不能因此成为身份或权限依据。示例中的“不要发布”属于用户任务约束；它与服务器对发布工具的授权，是需要同时满足的不同限制。

**组装。** 主智能体工厂选择实际模型、工具集合和中间件。配置中存在某能力，不等于本次运行一定启用：图片工具取决于模型视觉能力，记忆取决于开关与后端，子任务还受本次委派政策和执行容量限制。`LeadAgentAssembly` 可以携带组装描述信息，帮助解释两次运行究竟哪里不同。[组装与条件安装](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py#L486-L770)

**准备模型输入。** 程序把近期消息、必要历史、长期记忆和本轮工具说明组织成请求。某些内容进入检查点，某些只在请求中出现。模型不是每次直接读取所有磁盘数据，也不是每轮都重新检索整份长期记忆。

**执行与回填。** 模型提出工具名和参数后，程序仍要检查发现状态、技能限制、授权及实际执行边界。工具返回 `ToolMessage`（工具结果消息），模型据此继续。工具异常、策略拒绝和用户取消具有不同语义，不能一律解释成“再试一次”。[共同工具执行链](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py)

**结束与保存。** 主任务结束、长期记忆入队、事实落盘和外部动作完成，不是同一个时间点。恢复时也必须分别核对这些对象，而不是仅看一条 `completed` 状态。[记忆队列](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py) · [检查点访问器](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/checkpoint_state.py)

## 3. 阅读主线

| 顺序 | 正文 | 读完能够解释的问题 |
|---:|---|---|
| 1 | [上下文：从会话状态到模型真正看到的内容](01-context-lifecycle.md) | 哪些信息要保存，哪些只临时加入；历史太长时怎样继续而不破坏协议 |
| 2 | [记忆：从一次对话到可维护的长期事实](02-memory-lifecycle.md) | 什么值得长期记住，何时真正写成，怎样召回、纠错、隔离和删除 |
| 3 | [工具：从可发现能力到受控副作用](03-tool-lifecycle.md) | 为什么看见工具不等于获准执行；技能、会话池与文件修改怎样协同 |
| 4 | [工程与评测：怎样继续、恢复并证明结果](04-engineering-evaluation.md) | 检查点、日志、子任务、取消和外部状态怎样共同决定可靠性 |

第一遍连续读正文及其小结；第二遍用 [总图与综合自测](review/README.md) 重建主线；动手时进入 [源码小实验](labs/README.md)。实验只验证标明的函数和条件，不把纯函数测试当成完整 DeerFlow 服务验收。

## 4. 用问题寻找源码

| 你正在追的问题 | 首先读哪里 | 再追到哪里 |
|---|---|---|
| 谁决定这次使用哪些组件 | `agents/lead_agent/agent.py` | `agents/factory.py` 与共同中间件构建器 |
| 历史怎样变成模型输入 | `dynamic_context_middleware.py` | `durable_context_middleware.py`、`summarization_middleware.py` |
| 对话何时变成长期事实 | `memory_middleware.py` | `agents/memory/manager.py`、DeerMem 的 queue / updater / storage |
| 模型为什么看不见或不能使用某个工具 | `tools/tools.py` | DeferredToolFilter、SkillToolPolicy、Guardrail 与 sandbox |
| 子任务结束后能相信什么 | `tools/builtins/task_tool.py` | `subagents/executor.py`、收据检查和验收条件检查 |
| 取消或重启后怎样继续 | `runtime/runs/worker.py` | CheckpointStateAccessor、RunJournal 与 RunEventStore |

上表中包内路径的共同前缀是 `backend/packages/harness/deerflow/`。详细结论的链接放在相应正文附近；架构说明用于找入口，具体分支以同一快照的实现与调用方为准。

## 5. 版本与使用边界

本组固定学习 [bytedance/deer-flow 的 `e2feca1e567d9bafce657de8ad8bc668bd7ad513` 快照](https://github.com/bytedance/deer-flow/tree/e2feca1e567d9bafce657de8ad8bc668bd7ad513)。DeerFlow 2.0 是产品代际名称；该快照的应用包声明 `2.2.0-dev`，harness 包声明 `2.1.0`，两者都要求 Python `>=3.12`。应用版本、包版本和精确提交不能混用，更不能把开发快照称为已发布稳定版。[应用声明](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/pyproject.toml) · [harness 声明](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/pyproject.toml)

本文不以旧版深度研究工作流解释这套实现，也不对其他产品作未经同版本核验的能力排名。通用机制回到 Agent 课程；其他产品差异回到 [产品总入口](../README.md)。阅读范围、问题去向、实测环境与未验证项见 [维护记录](../../../guide/audits/deerflow-reader-first-2026-09-27.md)。

下一篇：[01｜上下文生命周期 →](01-context-lifecycle.md)
