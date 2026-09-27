# 04｜工程与评测：怎样继续、恢复并证明结果

[← 工具](03-tool-lifecycle.md) · [DeerFlow 总览](README.md) · [综合回顾 →](review/README.md)

支付页修复做到一半，用户点击取消。稍后重新打开会话，模型历史回到了运行前，但文件里已经有部分修改。应该把它判断成恢复失败吗？

不能只看一个“恢复”按钮。检查点能恢复智能体的继续状态，外部文件和服务却不一定随之倒退。本章把前面三篇放回完整运行，重点回答：**系统停止了什么，保留了什么，接下来应该核对什么，以及什么证据足以支持完成声明。**

## 1. 一次 Run 至少涉及四类事实

| 事实 | 主要承担者 | 回答的问题 |
|---|---|---|
| 运行处于哪个阶段 | Gateway 管理的 Run 记录 | 已接纳、执行中、结束还是失败 |
| 智能体接下来怎样继续 | LangGraph Checkpoint | 当前消息、摘要和其他状态是什么 |
| 运行中观察到什么 | Run Journal / RunEventStore | 哪次模型或工具调用产生了哪些事件 |
| 外部世界实际怎样 | Workspace、沙箱、外部服务 | 文件是否存在，消息是否发出，数据库是否改变 |

长期记忆还属于独立保存路径，不因一次 Run 历史回滚就自动回滚。第一篇说明请求视图可能不同于状态，第二篇说明队列可能尚未落盘，第三篇说明工具结果不等于业务验收；恢复必须承认这些差异。[运行层说明](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md) · [运行工作器](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/runs/worker.py)

## 2. 停止原因为什么不能都叫“任务完成”

模型可能自然给出最终回答，也可能因输出长度、安全策略、循环检测或预算耗尽而停止。DeerFlow 组装相应中间件处理这些情况：例如安全终止需要抑制该响应的工具调用，输出截断不能继续执行残缺参数，重复工具循环需要被识别。

终止保护还要考虑执行顺序。`after_model` 逆序分发时，安全处理应先清理不能执行的工具调用，再让其他统计与结束处理看到一致结果。主请求遇到真正的空停止响应时，有限的模型边界恢复与最终无可见内容的兜底，也不能混成无限的“再跑一轮”。[实际结束保护组装](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py#L701-L768)

模型错误处理与工具错误处理也不等同。前者可能发生在任何工具提议产生之前；后者可能已经接触外部系统。重试资格取决于错误类型、预算和副作用确定性。不能把“存在错误处理中间件”推广成每个模型、每个工具和每个后端都采用同一种故障切换政策。[模型错误边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/llm_error_handling_middleware.py) · [工具错误边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py#L166-L201)

因此验收时要分开：停止是否正常，是否保留了可用部分结果，目标是否满足，以及尚有何项未完成。某个状态字段为 `completed`，仍可能附带 `token_capped`、`turn_capped` 或 `loop_capped` 之类的停止原因。[子任务结果定义](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/executor.py#L95-L155)

## 3. 检查点保存状态，但通道的更新语义仍然有效

Checkpoint（检查点）保存可继续的智能体状态。每个状态字段的更新规则称为通道语义：例如消息可能按 ID 合并，产物引用可能去重追加，其他字段则由明确的归并函数处理。

假设当前消息为 A、B、C、D，想回到只有 A、B 的状态。普通更新 A、B 可能只是更新已有消息，不会删除 C、D。因此恢复和压缩需要 `Overwrite`，明确说“用这份值替换”，而不是“再合并一次”。

DeerFlow 用一个只负责状态变更的图写出新检查点。这张图有一个不执行业务的节点，但沿用实际智能体的状态结构和检查点机制，使新状态处在空闲位置，不误触发待执行模型或工具。自定义中间件可能贡献额外状态字段，所以不能只拿基础 `ThreadState` 恢复，否则扩展状态会被静默丢弃。[状态变更图与访问器](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/checkpoint_state.py#L1-L121)

## 4. full 与 delta 不只是存储大小不同

`full` 保存完整累积状态；`delta` 对适用的累积通道使用增量及周期快照。一个最小算术模型能说明动机：每步新增两条消息，前三步完整消息数为 2、4、6，三次全量保存共重复序列化 12 条消息；仅计新增部分则是 6 条。实际还包括周期快照、元数据和后端开销，这个例子不是存储压测结果。

代价是读取者必须重建状态。直接读取 saver 原始对象，可能只看到增量标记，而不是完整消息。因此统一通过 `CheckpointStateAccessor` 获取物化后的状态；需要的只是元数据时，另有不重建全部消息但仍经过兼容检查的入口。[访问器](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/checkpoint_state.py#L123-L231)

### 4.1 模式兼容不是双向对称

该快照默认 `full`，运行模式和增量快照频率在进程内固定，改变需要重启。跨进程共享检查点数据库时，也需要一致的解释方式。

`delta` 进程可以用旧的完整检查点作为重建起点；`full` 进程不能直接把 `delta` 检查点当完整状态读。反向切换需要先物化与转换，不是改一个配置就安全。不能把缺失字段默认为空消息，掩盖实际的模式不匹配。[模式与非对称迁移](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md)

### 4.2 为什么 delta 的恢复不能随意从旧点分叉

若多个分支共享旧祖先，祖先的待处理增量写可能让另一分支的内容进入恢复结果。DeerFlow 对相应的根会话恢复路径采取线性化：先物化选择的旧检查点，再把每个通道完整写到当前头部；归并通道使用 `Overwrite`，只存在于当前头部的新字段按实际结构重置。

`full` 不需要同样的增量祖先重放，可以保留其分叉语义。这里不能只背“delta 更省存储”，还必须说明它改变了恢复算法。[delta 恢复与回滚](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md) · [工作器实现](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/runs/worker.py)

## 5. 取消、编辑重跑和历史分支怎样保持一致

### 5.1 回滚点必须是完整的运行前状态

工作器在执行前捕获可物化状态、检查点位置与相关待处理写。如果捕获失败，应禁用相应回滚能力，不能拿半份状态冒充安全恢复点。

取消并选择回滚后，`full` 路径可以基于运行前检查点形成新头；`delta` 路径则在当前头部完整恢复捕获的通道，避免不安全的兄弟增量。两者还要保留实际智能体的扩展字段和服务端绑定。[回滚不变量](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md)

编辑旧输入后重跑，先产生一条临时替代历史。若新运行失败、超时或被中断，需要恢复运行前状态，并在流结束前把恢复值通知客户端；否则用户界面可能显示一条没有成功完成的新历史。

### 5.2 找旧检查点要沿亲缘关系，不是只看时间

同一 Thread 中可能有多条兄弟分支。按时间挑“目标消息之前最近的检查点”，可能取到别的分支。应沿当前头部的 `parent_config` 找真正祖先。

只有明确的旧数据缺少父链接等兼容条件，才进入有界时间顺序兜底；循环、悬空父节点、目标不匹配或存储错误，不能伪装成普通“没找到”，然后挑一个差不多的状态。[亲缘查找](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/app/gateway/checkpoint_lineage.py) · [兼容限制](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md)

### 5.3 为什么历史分支不能复制今天的工作区

假设第二轮才产生 `report.md`，用户从第一轮分支。直接复制当前工作区，会让新分支看到“未来才出现”的文件。

工作区没有每轮完整版本快照时，DeerFlow 对历史轮次分支不复制当前工作区；从最新轮次分支才可尽力复制当前文件。消息历史可回到过去，不代表文件系统也可时间旅行。[线程生命周期](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/THREAD_LIFECYCLE.md)

> ⚠️ **状态回滚不撤销外部世界。** 文件修改、已经发出的消息或远端数据库变化，需要另外的状态核验、业务幂等或补偿。检查点、日志和记忆都不能自动承担这些副作用的逆操作。

## 6. 日志与实时流为什么不能直接代替检查点

`RunJournal` 把模型、工具与运行回调组织为可持久的语义事件。实时输出的 token 片段适合界面流式显示，不宜直接成为成千上万条永久消息记录；完整模型消息、工具结果和运行事件具有另一种记录粒度。[RunJournal](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/journal.py)

### 6.1 同一次模型响应回调两次，不能变成两条答案

有些回调路径可能先返回响应，随后对同一模型运行 ID 补充用量。Journal 会合并相邻的对应信息，避免重复展示和重复统计。它维护的首份响应内容与后续用量补充有边界，迟到回调不能随意改写已经追加的历史事件。

这里防止的是产品侧重复计量，不是声明供应商真正收取了两次费用。诊断时要区分调用确实发生两次，还是同次调用的回调重复。[响应合并说明](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md)

### 6.2 历史界面与检查点需要共享轮次身份

界面消息历史主要由事件存储提供，而继续执行依赖检查点。分支继承了检查点消息，却没有对应事件时，界面可能只显示新产生的轮次。因此需要补入继承历史对应的事件，并给不同用户轮次合适的运行身份；不能让所有继承消息共享一个可被整体替换的 ID。

流式客户端断线后可以按序号继续获取事件；若需要的区间已经丢失，不能从现存最早事件假装无缝继续。系统需要报告重放缺口，让客户端重新读取持久状态，再建立一致视图。[事件流约定](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/RUN_EVENT_STREAM.md) · [线程生命周期](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/THREAD_LIFECYCLE.md)

### 6.3 补齐悬空工具调用，只修复了消息协议

中断可能留下一个工具调用，却没有对应结果。`DanglingToolCallMiddleware` 在后续模型调用前补齐相应协议表示，避免供应商因缺少结果拒绝请求。

但补出的错误消息不能证明外部动作没有发生。若请求已经送达外部服务，结果在返回途中丢失，真实结果仍需查服务端状态或执行证据。[悬空调用处理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/dangling_tool_call_middleware.py)

## 7. 子智能体隔离的是什么，又共享了什么

主智能体可以通过 `task` 委派一个自包含工作，例如只分析某类监控证据。从父模型看，它是一项工具；子级则有自己的消息、模型调用、工具约束和运行预算。

原生子图以 `checkpointer=False` 创建，避免继承父级检查点并污染父会话。它的一次性模型内部步骤，不是默认可跨用户轮次恢复的子会话。但这不表示没有子任务事件，也不表示系统没有持久批任务。[原生子执行](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/executor.py) · [子任务运行边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/AGENTS.md)

### 7.1 isolated 与 snapshot 是信息选择，不是两个独立物理世界

`isolated` 要求委派提示本身足够完整；`snapshot` 在派发时捕获父级必要历史，供子级理解背景。快照可以包含摘要、真实用户及可见助手消息，以及已经配对完成的工具历史，但父系统提示、秘密与执行权限不应原样复制为子模型指令。

父级工具调用在快照中表示为静态历史文本，而不是子级自己的工具协议。否则子级可能把“父级已经发送过消息”误认成“我已经执行过”，甚至把历史权限声明当新授权。

快照在派发时固定，父级后续变化不会偷偷修改子级已看到的历史。这里不继承的是**模型上下文中的权限声明**，不是说子执行完全没有用户身份或受控的运行上下文：用户、知识范围和其他执行约束仍通过明确的运行路径传递。[上下文快照](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/context_snapshot.py)

普通 `task` 还可以在派发时复制有效的本轮上传状态。空列表有意义：它表示本轮没有新上传，不能用旧会话全部文件替代；缺少或损坏状态则不能假装有这项能力。延迟执行的持久批任务没有同样的父运行上传边界，不能直接照搬。[上传状态与共享资源](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/AGENTS.md)

子级通常仍可共享父线程工作区和沙箱。**上下文隔离不等于文件隔离。** 两个子任务若同时修改同一文件，仍有冲突风险；把目录、输入和输出划分清楚，比仅增加子智能体数量更重要。

### 7.2 所有子任务共享一个持久隔离循环，不是每个子任务都开一个循环

原生子任务被送到进程中专门的持久异步事件循环，与父级请求循环分开。跨循环时，可以复制适合传播的上下文，却不能直接使用绑定父循环的 Journal、连接池或 Future。

DeerFlow 标记并排除相应循环绑定回调，同时保留适合传递的流式语义。需要记录子级中间件事件时，使用窄范围代理调度回父循环，而不是直接在子循环改父 Journal。[子任务代理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/builtins/task_tool.py#L94-L163) · [执行边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/AGENTS.md)

### 7.3 子消息压缩以后，步骤记录不能继续相信旧长度

一个工具步骤可能一次增加多个 ToolMessage，步骤捕获不能只看最后一条消息。子级压缩历史后，消息长度还可能变小，原来的扫描游标必须调整，否则之后的新步骤可能一直被漏记。

所以步骤记录既需要游标，也需要稳定身份或内容去重。子任务开始、步骤和结束事件分开保存，界面按任务展开，不把子级所有中间消息塞回父级普通对话。[步骤捕获](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/step_events.py)

## 8. 委派总量、执行容量与持久批任务是三层控制

同时最多执行三个子任务，不能防止模型连续创建一百批。因此需要分别限制本次运行总共委派多少、同一时刻执行多少，以及每个子任务最多花多少轮次、时间或 token。声明给模型的能力也要与启动时固定的真实执行容量一致，不能热更新文案后仍由旧控制器执行另一套限制。[容量与总量约定](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/AGENTS.md)

### 8.1 普通 task 与 batch_task 的持久边界不同

| 对象 | 保存什么 | 故障恢复意味着什么 |
|---|---|---|
| 普通子图 | 本次执行的内存状态与相应事件证据 | 不默认从某个子模型步骤检查点续跑 |
| `batch_task` 批任务 | 批次、任务项、执行说明、租约和有界结果 | 未完成项可由批服务按租约与尝试预算重新接管 |
| 父 Thread 检查点 | 父级继续状态和子任务摘要账本 | 父级能了解过去委派与结果，不等于持有完整子图检查点 |

批模式必须通过明确的工具选择，不能仅因提示很长就自动推定进入持久队列。工作器领取任务项后续租，完成时按拥有者身份写结果；进程停止时，未完成租约可以过期，其他工作器再接管。排队接纳失败与真正执行失败在尝试计数上也有不同处理。[批服务接纳](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/batch_service.py#L103-L195) · [续租、完成与恢复](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/batch_service.py#L290-L419)

这仍不是对外部副作用的精确一次保证。重新接管一个任务项，与从子模型的上一条消息原地续跑不同；重复执行风险需要结合业务操作和实际证据判断。

### 8.2 什么时候值得委派

委派会增加启动、重复发现和结果汇总成本。只有并行时延收益、专长或上下文隔离收益能覆盖这些成本，才值得使用。存在输入依赖或重叠可变状态时，不应简单并行派发；独立只读证据收集更容易拆分。这个判断应逐批重做，不能因为第一次委派有效，就把后续所有任务都交给子级。[主子任务路由政策](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/AGENTS.md)

## 9. 收据、可判定条件和业务质量为什么不能合成一个“通过”

子任务说“报告写好了”，至少要区分三个问题：它是否引用了真实的工具执行证据，目标文件是否存在或可读，以及内容是否满足业务要求。

收据引用检查帮助核对动作声明是否有对应记录；`acceptance_checks.py` 对文件存在、非空、写入读回，以及特定测试命令的执行证据等可判定条件进行检查。无法判断的自然语言条件标为 `UNVERIFIED`，不是自动通过。[验收叶条件定义](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/acceptance_checks.py#L1-L153)

例如空文件可以满足“存在”，却不满足“非空”；一句输出里出现 `pytest`，不能证明真执行了对应测试；零测试也不是测试通过。读取还应有字节界限，目录、符号链接或无法安全确定的目标不能被随意当普通文件。

该检查层刻意区分 `checked` 与 `holds`，并声明其执行证据边界。不要从这些叶条件推出“业务结论已经正确”，也不要把它说成系统里不存在任何其他强制门禁；整体阻断语义必须继续看实际调用方及配置。批任务的这条附加检查具有建议性，检查器故障不会自动把可用执行结果变成需要重试的任务失败。[批任务验收调用方](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/batch_service.py#L321-L359) · [批验收资源管理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/batch_acceptance.py)

## 10. 取消以后，谁负责把已经取得的资源释放完

取消意味着不再继续这份工作，但已经派发的同步操作可能仍在执行，连接可能仍持有数据库锁，沙箱可能仍有其他使用者。立即遗弃这些资源，会把错误留给下一次运行。

源码中多处采用 shield-and-drain（保护清理并等它完成）：暂缓把取消传播给调用者，先等待当前组件拥有的清理结束，再传播原取消。MCP 会话由其 owner task 退出；子执行需要先关流，再释放沙箱持有与执行容量；持久化初始化也需要释放自己取得的锁和连接。[运行资源约定](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/AGENTS.md) · [子任务资源约定](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/subagents/AGENTS.md)

这不是“一切操作都无限等”的通用建议。有些后台状态等待具有明确的宽限期并移交专门清理者，有些已持有资源的清理不能靠超时直接遗弃。需要逐项确认拥有者、取消传播、移交条件和最终回收，而不是给整套系统套一个统一超时。[子任务异常等待边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/builtins/task_tool.py#L58-L85)

## 11. 怎样知道两次运行用了同一套系统

行为不仅由模型名决定，还取决于提示、工具定义、技能、中间件顺序、上下文政策和配置。`AssemblyDescriptor`（组装描述）把相关身份与哈希组织起来，帮助定位行为差异；有需要的观察者时才计算昂贵部分，避免每次运行都为无人使用的诊断付出成本。

扩展中间件必须在完整链组装后合并并验证顺序，否则某插件可能插到错误位置，使观察者看到的并非真正最终请求，或把错误规范化与进度处理顺序倒置。哈希便于比较“是否不同”，但不能从哈希复原完整输入，也不能代替回放所需数据。[主智能体与扩展组装](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py) · [顺序不变量](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/extensions/ordering.py)

## 12. 评测应围绕故障窗口，而不是只数测试文件

先给支付修复场景定义验收：不能发布；需要确认文件修改；能够说明做过和未做过的验证。再设计下列受控变化。

| 故障或变化 | 应检查的结果 | 单靠什么不够 |
|---|---|---|
| 多轮后发生摘要压缩 | 当前约束与工具协议保留，后续仍能完成任务 | 输入 token 下降 |
| 工具副作用完成后丢失响应 | 不凭空断言未执行，不盲目重放 | 一条错误 ToolMessage |
| 子任务输出到一半取消 | 停止原因、部分结果、清理和资源持有一致 | 父界面显示取消 |
| 从历史轮次分支 | 消息祖先正确，不继承未来工作区文件 | 分支接口返回成功 |
| 流式事件出现缺口 | 客户端回到持久状态，而不是继续错误增量 | 前后端分别通过单测 |
| 记忆索引失败或队列未提交 | 分清可降级检索和未持久写入 | 没有抛异常 |

测试层次也应分开。纯函数测试适合状态合并与候选门控；中间件测试适合请求角色、拒绝与错误分支；检查点和数据库集成测试适合恢复语义；确定性回放可复现同一模型与工具轨迹；浏览器端到端测试验证服务、流和界面组合。真实模型、真实 MCP、远程沙箱及生产部署还需要各自的实测条件。[上游回放指南](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/REPLAY_E2E.md)

指标至少同时看任务结果、过程与资源：成功完成多少，失败发生在哪一层，使用了多少模型调用、工具调用和委派，消耗多少 token、时间与存储。安全拒绝率高但所有任务都做不成，不是有用系统；成本下降但约束丢失，也不是优化成功。没有实测时，把它们写成评测设计，不写成已经得到的提升结果。

## 本章小结

可靠执行建立在不同事实的一致解释上：Run 管运行阶段，Checkpoint 管继续状态，Journal 管事件，工作区与外部服务管真实结果。子任务隔离、批任务持久化、取消清理和验收条件又有各自边界。工程判断不是把这些都叫“持久化”或“恢复”，而是面对具体故障窗口，说明哪些事实可信、哪些未知、下一步怎样核对。

## 🎯 面试怎么回答

**Q：Agent 崩溃后怎样恢复并避免重复副作用？**

> 我会先恢复可继续的智能体状态，再核对尚不确定的外部动作。DeerFlow 用检查点访问器适配完整和增量状态，回滚时按通道语义替换，保留真实智能体的扩展字段。但检查点不撤销文件或外部服务；需要结合工具收据、日志与外部状态判断是否已经执行，业务侧再使用幂等或补偿。补齐消息协议只允许模型继续说话，不是证明动作从未发生。

**Q：子 Agent 不保存检查点，是不是不支持可靠长任务？**

> 不能从单一层得结论。DeerFlow 普通子图是一次性执行，不继承父检查点；执行步骤和结果仍可以留证据，父级还保留委派账本。显式 batch_task 则用持久任务项、租约和预算恢复调度。批任务恢复不等于从子模型某步原地续跑，也不自动保证外部副作用精确一次。

## ⚠️ 高频易错点

- **把回滚状态解释成撤销所有动作。** 外部系统可能已经改变。
- **把 completed 解释成目标满足。** 还要查看停止原因、未完成项和验收证据。
- **把共享沙箱解释成上下文完全共享。** 信息隔离和资源隔离是两条不同边界。
- **把叶条件成立解释成结论正确。** 文件存在、测试执行与业务质量不是同一件事。

## 本章自测

**任务 A：** 第一次运行写出一个非空报告，第二次运行修改它。用户从第一次运行之前的旧轮次建立分支。题设没有文件系统历史快照。请分别预测消息状态与工作区，解释为什么不能直接复制当前文件。

<details>
<summary>任务 A 提示</summary>

找出消息历史和文件版本各自的权威来源；不要把检查点看成磁盘快照。

</details>
<details>
<summary>任务 A 答案与解释</summary>

消息应按正确祖先恢复到选择的分支位置；不能把第二次修改后的当前工作区复制到历史分支，因为那会带入未来文件状态。没有文件版本快照时，应承认无法还原完整历史文件，而不是用当前文件冒充过去。

</details>

**任务 B：** 批任务执行状态已完成，验收条件是 `file:report.md exists` 和“论证正确”。文件真实存在但为空，且没有语义质量检查结果。要求给出每个条件的证据强度、不能宣称的结论，以及是否应仅因第二项未验证就自动按执行失败重试。

<details>
<summary>任务 B 提示</summary>

“存在”与“非空”不同；叶条件检查与批服务执行失败策略不同。

</details>
<details>
<summary>任务 B 答案与解释</summary>

在路径范围和读取条件都成立的前提下，空文件仍满足 exists；“论证正确”不能由该确定性叶检查判断，标为未验证。不能声称报告已通过业务质量验收，也不能把建议性检查未验证自动转换成执行失败重试。需要补充相应质量验证，再决定交付或返工。

</details>

回顾：[总图与综合自测 →](review/README.md)
