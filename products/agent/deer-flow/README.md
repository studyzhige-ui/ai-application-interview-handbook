# DeerFlow 2.0｜沿一次任务理解智能体怎样工作

[← Agent 产品源码学习](../README.md) · [通用 Agent 课程](../../../curriculum/09-agent/README.md) · [技术证据索引](../../../references/agent/README.md)

DeerFlow 是能够调用工具、处理文件并委派子任务的智能体系统。本组文档沿它的真实实现，学习一个用户请求怎样变成模型输入、工具操作、可继续的会话状态和可核对的执行记录。它是产品源码学习，不把 DeerFlow 的选择当成所有 Agent 的唯一标准。

**阅读前提：** 能理解 Python 函数、字典、异常和异步调用；知道模型可以返回工具调用，而工具由程序执行。需要回补时，先读 [Agent Loop](../../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md) 和 [工具执行](../../../curriculum/09-agent/docs/06-ToolExecutionAndFailure.md)。检查点、中间件、消息合并与作用域会在使用时解释，不要求先背完框架 API。

## 核心设计

假设用户提出一个任务：

> 分析支付页重复提交的问题，必要时查询监控。这次只做最小修复，不要发布。我的长期习惯是先解释风险，再给方案。

这是贯穿四篇正文的**教学场景**，不是上游生产案例或实测结果。示例用户、会话和运行分别记为 `u1`、`t1`、`r1`。

模型可以判断下一步应查日志还是读代码，却不会自动保存进度、打开安全的执行环境，或保证“不要发布”在长对话后仍有效。DeerFlow 在模型外安排这些工作：Gateway（网关）接纳请求，Run Worker（运行工作器）组装主智能体，LangChain / LangGraph 驱动模型与工具循环，中间件在指定时点处理输入、权限、状态和结果。默认完整产品入口是嵌入运行环境的 Gateway，不是另起一套裸 LangGraph Server。[源码入口与部署边界][architecture]

```text
用户请求
   ↓
Gateway：确认用户与会话，创建本次 Run
   ↓
Run Worker：取得配置，组装主智能体
   ↓
准备模型输入 → 模型回答或提出工具调用
   ↑                         │
   └──── 回填结果 ← 检查并执行工具
   │
   └─ 不再继续调用时，处理本轮结束

保存与核对分别由以下对象承担：
Checkpoint   保存以后继续所需的智能体状态
Run Journal  记录运行中发生的事件
Workspace    保存工作文件；外部服务保有自己的状态
DeerMem      在允许时异步提取长期用户信息
```

图中保存的是不同东西。检查点中有“已经写文件”的消息，不保证文件还在；日志中有一次工具成功事件，也不自动证明文件内容符合业务要求。第一篇的[一次运行轨迹](01-context-lifecycle.md#run-trace)会把这张图展开成可逐步核对的消息和文件变化。

## 1. 先认清四个运行对象

| 对象 | 在本例中是什么 | 为什么单独区分 |
|---|---|---|
| Thread（会话容器） | 围绕支付问题持续交谈的 `t1` | 可以承载多次用户请求和多次运行 |
| Run（一次运行） | 处理本次请求的 `r1` | 有独立身份、预算、取消和结束状态 |
| ThreadState（会话状态） | 消息、历史摘要、委派记录及文件环境标识等 | 程序据此继续工作，不等于全部发送给模型 |
| ModelRequest（一次模型请求） | 循环中某次真正送入模型的消息和工具说明 | 从状态与本次运行条件组装，可以临时增删内容 |

一次用户请求可能包含多次模型调用。例如先请模型决定读什么，再把读取结果交给模型继续判断；这仍可以属于同一个 Run。“Turn”在不同框架中含义不统一，本文分别使用“用户轮次”和“模型调用”，不把两者混算。[状态定义][state] · [主智能体组装][assembly]

## 2. 一次任务怎样经过系统

1. **接纳请求。** 网关确认用户身份和会话归属，固定本次项目等服务端上下文。客户端的同名字段不能成为身份或权限依据。“不要发布”是用户任务约束，服务器对发布工具的授权是另一项限制；执行必须同时满足适用限制。
2. **组装本次能力。** 工厂选择模型、工具和中间件。配置中存在能力，不等于本次启用：图片工具取决于模型视觉能力，记忆取决于开关与后端，子任务受委派政策与执行容量约束。组装描述可帮助比较两次运行的差异。[条件安装][assembly]
3. **准备输入并执行循环。** 程序选择必要消息与工具说明；模型提出工具名和参数后，程序检查并执行，再返回 `ToolMessage`（工具结果消息）。模型根据新观察继续。长期记忆不是每次模型调用都重新全量检索，工具错误、策略拒绝和用户取消也不是同一种“重试”信号。[共同执行链][tools]
4. **结束并核对保存。** 主任务结束、记忆入队、事实落盘和外部动作完成不是同一时刻。恢复与交付时分别确认，不只看一条 `completed` 状态。[记忆队列][queue] · [检查点访问器][checkpoint]

## 3. 阅读主线

| 顺序 | 正文 | 读完能够解释的问题 |
|---:|---|---|
| 1 | [上下文：从会话状态到模型真正看到的内容](01-context-lifecycle.md) | 一次工具往返怎样改变下一次输入；哪些内容保存、临时加入或压缩 |
| 2 | [记忆：从一次对话到可维护的长期事实](02-memory-lifecycle.md) | 默认写入如何走通，何时真正保存，怎样召回、纠错、隔离和删除 |
| 3 | [工具：从可发现能力到受控副作用](03-tool-lifecycle.md) | 看见工具为什么不等于获准执行；文件、技能与会话怎样协同 |
| 4 | [工程与评测：怎样继续、恢复并证明结果](04-engineering-evaluation.md) | 先认识正常 Run 与子任务，再判断保存、取消、恢复和验收 |

第一遍沿正文正常流程阅读；相关位置的折叠内容承接后端变体、兼容分支或实现细节，关键正确性边界留在正文。第二遍用[总图与综合自测](review/README.md)重建关系；动手时进入[源码小实验](labs/README.md)。实验只验证标明的函数和条件，不把纯函数测试当成完整服务验收。

## 4. 用问题寻找源码

| 正在追的问题 | 首先读哪里 | 再追到哪里 |
|---|---|---|
| 谁决定本次组件 | `agents/lead_agent/agent.py` | `agents/factory.py` 与共同中间件构建器 |
| 历史怎样变成输入 | `dynamic_context_middleware.py` | `durable_context_middleware.py`、`summarization_middleware.py` |
| 对话何时成为长期事实 | `memory_middleware.py` | `agents/memory/manager.py`、DeerMem 的 queue / updater / storage |
| 工具为什么不可见或被拒绝 | `tools/tools.py` | DeferredToolFilter、SkillToolPolicy、Guardrail 与 sandbox |
| 子任务结束后能相信什么 | `tools/builtins/task_tool.py` | `subagents/executor.py`、收据与验收条件检查 |
| 取消或重启后怎样继续 | `runtime/runs/worker.py` | CheckpointStateAccessor、RunJournal 与 RunEventStore |

包内路径的共同前缀是 `backend/packages/harness/deerflow/`。正文在结论附近链接证据，章末提供回看入口。架构说明用于找入口，具体分支以同一快照的实现与调用方为准。

## 5. 版本与使用边界

固定学习快照为 [bytedance/deer-flow 的 `e2feca1e567d9bafce657de8ad8bc668bd7ad513`](https://github.com/bytedance/deer-flow/tree/e2feca1e567d9bafce657de8ad8bc668bd7ad513)，核验日期为 2026-09-27。DeerFlow 2.0 是产品代际名称；应用包声明 `2.2.0-dev`，harness 包声明 `2.1.0`，均要求 Python `>=3.12`。应用版本、包版本和提交不能混用，开发快照不是已发布稳定版。[应用声明][app-version] · [harness 声明][harness-version]

通用机制回到 Agent 课程，其他产品差异回到[产品总入口](../README.md)。本组不以旧版深度研究工作流解释这套实现，也不作未经同版本核验的产品排名。阅读范围与验证边界分别记录在[源码修订记录](../../../guide/audits/deerflow-reader-first-2026-09-27.md)和[讲解精修记录](../../../guide/audits/deerflow-clarity-refinement-2026-09-27.md)。

下一篇：[01｜上下文生命周期 →](01-context-lifecycle.md)

[architecture]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/ARCHITECTURE.md
[state]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py
[assembly]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py
[tools]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
[queue]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py
[checkpoint]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/checkpoint_state.py
[app-version]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/pyproject.toml
[harness-version]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/pyproject.toml
