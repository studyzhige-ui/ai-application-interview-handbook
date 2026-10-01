# DeerFlow｜固定源码与机制索引

[← Agent 资料](README.md) · [产品主线](../../products/agent/deer-flow/README.md)

固定 [4d5607229ef1ebe8a66c9b9644b91da9082c3221](https://github.com/bytedance/deer-flow/tree/4d5607229ef1ebe8a66c9b9644b91da9082c3221)，2026-10-01 02:07 UTC 核验 main。路径以下均以 backend/packages/harness/deerflow 为根；源码用于证明正文，不代替过程讲解。

| 要核验的过程 | 正文入口 | 关键实现 |
|---|---|---|
| 同线程准入、幂等与拥有者 | [Run 准入](../../products/agent/deer-flow/01-run-and-model-loop.md#run-admission) | [RunManager][runs] |
| 模型循环与故障分类 | [模型循环](../../products/agent/deer-flow/01-run-and-model-loop.md#model-loop) | [主图组装][assembly]、[模型错误][llm] |
| 工具检查与结果规范化 | [执行资源](../../products/agent/deer-flow/02-tools-and-resources.md) | [共同中间件链][wrappers] |
| 读版本与写入竞态 | [先读后写](../../products/agent/deer-flow/02-tools-and-resources.md#5-先读后写怎样防止基于旧文件反复修改) | [文件门控][readwrite] |
| 技能可见与动作级激活 | [技能与 MCP](../../products/agent/deer-flow/03-skills-and-mcp.md) | [技能授权][skill]、[组装][assembly]、[来源标记][wrappers] |
| 原生子任务如何返回与停止 | [task](../../products/agent/deer-flow/04-native-batch-and-acp.md#native-task) | [执行器][executor] |
| 批任务怎样续租和接管 | [批次](../../products/agent/deer-flow/04-native-batch-and-acp.md#81-普通-task-与-batch_task-的持久边界不同) | [批服务][batch] |
| 外部进程如何交接 | [ACP](../../products/agent/deer-flow/04-native-batch-and-acp.md#acp) | [ACP 工具][acp] |
| 模型输出怎样成为持久交付 | [收尾](../../products/agent/deer-flow/05-delivery-and-goals.md#finalization) | [工作器][worker] |
| 连续目标何时续轮、何时清除 | [目标](../../products/agent/deer-flow/05-delivery-and-goals.md#continuous-goals) | [评估证据][goal]、[最终仲裁][worker] |
| 摘要预算与保留规则 | [状态与恢复](../../products/agent/deer-flow/06-history-and-recovery.md) | [摘要中间件][summary] |
| full/delta 物化和线性恢复 | [检查点恢复](../../products/agent/deer-flow/06-history-and-recovery.md#checkpoint-recovery) | [访问器][checkpoint]、[工作器][worker] |
| 记忆筛选、候选和版本提交 | [长期记忆](../../products/agent/deer-flow/07-memory-pipeline.md) | [更新器][memory]、[宿主配置][memory-config] |

## 差异核对与验证边界

旧学习快照到上述提交的完整 Git tree 对照包含 419 个新增/变化文件，无删除文件。该统计是完整差异范围，不代表逐个文件精读。正文重读主要运行入口，并核对主图、工具与技能中间件、摘要、子任务、目标工作器和记忆更新器的相关变化。

写作期间又进行两次增量 tree 核对，最后固定到 02:07 UTC 的默认分支提交。与正文直接相关的改变包括：技能可见/激活动作分别授权、摘要生成模型与运行窗口预算分离、目标完成延迟到交付终态后清除、子任务直接返回工具结果及错误终态、取消收尾的事件/用量保存，以及默认关闭的可选记忆预筛选。所有引用使用同一最终快照；没有用 GitHub Compare 的截断文件列表替代全量 tree 对照。

没有运行 DeerFlow、模型请求、外部 MCP/ACP 或上游测试；文档中的轨迹是教学推演。保留的 labs 仅为旧版维护材料，不属于本次运行证据，也不是读者的前置任务。

[runs]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/manager.py
[assembly]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/lead_agent/agent.py
[llm]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/llm_error_handling_middleware.py
[wrappers]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
[readwrite]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py
[skill]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/authz/skill_filter.py
[executor]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/subagents/executor.py
[batch]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/subagents/batch_service.py
[acp]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/tools/builtins/invoke_acp_agent_tool.py
[worker]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/worker.py
[goal]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/goal.py
[summary]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py
[checkpoint]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/checkpoint_state.py
[memory]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py
[memory-config]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/config/memory_config.py
