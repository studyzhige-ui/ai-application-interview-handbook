# 交付与连续目标｜回答之后还要完成什么

[← 上一章](04-native-batch-and-acp.md) · [本产品目录](README.md) · [下一章 →](06-history-and-recovery.md)

模型生成最终回答，只结束了推理链的一部分。工作器还要处理子任务事件、工作区变化、交付收据、检查点与运行终态；连续目标也要等这些事实成立后才能正确清除或续轮。

<a id="finalization"></a>
## 模型说完以后，工作器怎样真正交付

先看最终助手内容与本次产生的输出路径，确定暂定终态。图结束之后，工作器依次收齐缓冲的子任务步骤、记录工作区变化、刷写 Journal，再按 run_id 幂等写交付收据。收据描述这一运行实际给出了哪些内容和产物；它和自然语言回答是不同记录。

```text
模型流结束 → 暂定结果
    → 子任务事件与工作区变化
    → Journal flush → 交付收据
    → 保持持久 Run 仍活动，完成必要检查点写入
    → 与取消竞争重新仲裁 → 保存真实终态与用量
```

必要检查点仍在写入时，持久 Run 保持活动，防止其他工作器把线程当成可自由迁移或改写。丢失租约的旧工作器跳过持久收尾；新的拥有者负责恢复，旧工作器不能继续写一份较晚到达却已失效的成功结果。

若有新产物却无法保存交付收据，原本成功的运行可以改为 error。部分诊断/便利字段保存是尽力操作，不能把每个日志失败都说成同一种致命故障；但也不能因为模型回答已显示就忽略交付记录失败。[收尾顺序与终态仲裁](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/worker.py)

子任务事件的 flush 还保护在途存储写：宿主取消时等待该次写确认，再传播取消；存储本身失败或取消则把批次放回缓冲。这样“用户取消”不会轻易抹掉取消前已经产生的步骤证据。

<a id="continuous-goals"></a>
## 连续目标怎样决定继续，为什么不能提前清掉目标

普通轮次结束后，存在有效目标才进入目标判断。工作器读取完整状态和目标，检查用户输入、澄清卡片、取消、停止原因、预算及无进展条件。仍待用户回答时不自动催 Agent 继续；需要继续且约束允许，才安排隐藏续轮。判断之后重新读状态，避免旧结论覆盖用户刚修改的目标。

评估器看到的证据包括近期可见对话、其中配对的工具调用与结果，以及界面上已回答的人类输入卡。工具文本做有界缩短并保留来源标签；超预算时优先保留较新证据和被遗漏的最近用户要求。隐藏助手调用及结果通常不混进可见证据。这样评估不只听最终自述，也能看见文件、命令和交付动作，但它仍是模型判断，不能取代确定性测试。[目标证据构造](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/goal.py)

评估返回 satisfied，只产生“可完成候选”，此刻还不清空目标。等运行成功交付、收据与终态保存、取消仲裁结束后，再取得线程检查点写入预留；重读目标全值和可见对话签名，确认都与评估时一致，才按预期检查点 ID 清除。若别的工作器已经接纳新 Run、目标改变或检查点冲突，就保留目标，不用旧评估覆盖新工作。

评估器异常会保存未取得结论的阻塞状态并停止这次自动继续，记录异常类型而非可能含请求细节的原错误全文。运行 success、评估 satisfied、目标被安全清除是三个依次核验的事实。[续轮与延迟清除](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/worker.py)

<a id="8-工具返回后观察证据与任务成功仍然不同"></a>

## 返回消息、执行证据和任务完成怎样区分

普通工具异常经 `ToolErrorHandlingMiddleware` 转成带对应调用 ID 的错误 `ToolMessage`，模型可修正参数或换路径。LangGraph 暂停等控制流要继续传播，不能混成业务错误；取消也不能被通用重试吞掉。[错误与控制流][s1-wrappers]

| 表示 | 主要回答什么 |
|---|---|
| `ToolMessage` | 给下一次模型调用什么观察？ |
| Tool Receipt（工具收据） | 哪次执行、哪些参数与结果有记录？ |
| Run Journal（运行事件记录） | 产品历史怎样呈现本轮过程？ |
| 文件读回或业务验证 | 最终对象是否满足任务要求？ |

它们不保证保存完全相同的全文。大结果可在返回后外置或裁剪；外层收据还要能看到策略提前拒绝的结果，不能漏掉真实拒绝。[记录位置][s1-wrappers]

> ⚠️ 外部动作已成功、回填却超时，并不能证明动作没发生。再次执行前先核对实际状态，必要时依赖业务幂等或补偿；不能说所有 DeerFlow 工具都自动具备统一的外部幂等保证。

`task` 从父模型看也是工具，但会启动独立子智能体。父模型收到“子任务完成”之后，还要核对停止原因、收据和验收条件，不能只凭返回文字交付。[委派章的子任务结果](04-native-batch-and-acp.md#native-task)

<a id="10-取消以后谁负责把已经取得的资源释放完"></a>

## 取消后，已取得的资源由谁收尾

取消请求不保证同步操作已经停止，也不保证连接、锁与沙箱已释放。第三篇的 MCP owner task 和沙箱租约，在这里都要完成自己的收尾责任。

多处源码使用 shield-and-drain，可理解为**保护清理并等它完成，再传播取消**。例如子执行先关流，再释放沙箱持有与执行容量；MCP 由自己的拥有者退出；持久化初始化也要释放已取得的锁和连接。[运行资源约定][s3-runtime] · [子任务资源约定][s3-subagents]

这不是让一切操作无限等待。有些后台状态等待有宽限期并移交清理者，有些仍持有资源的清理不能靠超时遗弃。需要逐项明确谁拥有、取消如何传播、何时移交与最终谁回收，不给整个系统套一个统一超时。[异常等待与移交][s3-task-tool]

[← 上一章](04-native-batch-and-acp.md) · [本产品目录](README.md) · [下一章 →](06-history-and-recovery.md)

[s1-wrappers]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
[s3-runtime]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/AGENTS.md
[s3-subagents]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/subagents/AGENTS.md
[s3-task-tool]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/tools/builtins/task_tool.py
