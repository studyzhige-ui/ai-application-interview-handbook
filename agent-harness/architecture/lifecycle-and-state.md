# Agent 执行过程与状态模型｜从一次输入到可恢复的结果

[架构总纲](README.md) · [概念归位表](concept-atlas.md) · [设计与自测](design-and-review.md) · [资料依据](sources.md)

> 本文把同一张四层图展开为执行视图和状态视图。状态名、接口名和记录结构除特别说明外均为教学设计，不是 Codex API 或所有框架的统一标准。

## 1. 先分清定义、实例与任务

Agent Definition 是可版本化的配置：角色说明、模型选择规则、工具集合、上下文策略和运行限制等。Agent Instance 是正在执行的实例。Task 是系统要完成的工作。

一个定义可以服务很多任务；同一任务可以使用多个执行角色；一个进程也可以运行多个实例。模型名称、进程、Agent 角色、业务任务不是同一个实体。

权限配置还必须与真实授权系统结合。即使某个 Agent Definition 写了“可以访问全部资源”，也不能因此越过当前用户或服务身份的实际权限。

## 2. Thread、Turn、Item：保留 Codex 原意，不泛化为行业标准

Codex App Server 的三个重要对象如下。[S03](sources.md#s03)

| 对象 | Codex 语境中的含义 | 必须区分 |
|---|---|---|
| Thread | 持续会话的容器，可以包含多个 Turn | 不是线程池中的操作系统线程，也不一定等于一个业务任务 |
| Turn | 一次用户输入触发的一段 Agent 工作，包含中间过程与输出 | 不是单次模型推理，也不只是“一问一答”两条消息 |
| Item | 有类型的输入输出单元，如消息、工具执行、文件修改等 | 一个 Item 可以有开始、增量、完成等多个 Event |

```text
Thread
├─ Turn A
│  ├─ 用户输入 Item
│  ├─ 工具执行 Item
│  │  └─ started → 若干进度事件 → completed
│  └─ Agent 输出 Item
└─ Turn B
   └─ 后续输入触发的新工作
```

这里是对象关系示意，不列举完整协议类型，也不意味着每个 Item 都支持同一种增量事件。

## 3. Task、Run、Attempt、Step：明确本系统自己的约定

| 对象 | 本文采用的工作定义 | 所在责任 |
|---|---|---|
| Task | 有业务目标、范围和验收条件的工作对象 | L1 |
| Run | 围绕任务开展的一次受管理执行，可以暂停和恢复 | L2 |
| Worker Attempt | 某个 Worker 对 Run 的一次承接或执行尝试 | L2 |
| Step | Runtime 自己定义的可记录推进单位 | L2 |
| Model Invocation | 一次模型请求及响应过程 | L2 经 L3 使用 L4 |
| Tool Call | 模型或系统提出的一次工具调用请求 | L2 / L3 |
| Operation | 需要在外部世界识别和核对的逻辑动作 | L2 记录，L3 / L4 兑现 |
| Artifact | 中间或最终产物及其引用 | L1 交付，L2 记录，L4 保存 |

一个 Task 可以关联多个 Run，例如重新执行或更换执行方案。Run 的恢复不必创建新 Run，但可以创建新的 Worker Attempt。一个 Run 与多少 Turn 关联由应用协议决定，不能把两棵对象树强行画成唯一层级。

```text
业务视图：Task → Run → Worker Attempt / Step / Operation
交互视图：Thread → Turn → Item → 生命周期事件
关联方式：稳定 ID 与明确关系，而不是依赖文本推断
```

同样，模型生成的 `tool_call_id` 未必适合作为跨重试的业务幂等键。一次模型重试可能生成新的调用 ID，但逻辑 Operation 仍然是同一个；这需要应用和 Runtime 明确识别规则。

## 4. 一次通用执行穿过哪些层

| 阶段 | 主责 | 输入与输出 | 必须守住的边界 |
|---|---|---|---|
| 接收任务 | L1 | 用户或事件输入 → Task 与契约 | 身份、范围、验收条件明确 |
| 创建执行 | L2 | Task → Run、配置版本和授权快照 | 不把未经验证的输入变成权限 |
| 准备状态 | L2 经 L3 | 读取历史、进展、待处理动作和产物引用 | 区分首次执行与恢复 |
| 获取信息 | L2 决策，L3 / L4 获取 | 查询 → 带来源和范围的证据 | 保留时效、身份与信任边界 |
| 构建上下文 | L2 | 指令、状态、证据、工具定义 → 模型输入 | 预算足够、关键约束不丢失 |
| 模型推理 | L2 经 L3 调用 L4 | 上下文 → 答案、行动或完成候选 | 生成不是执行，格式不是事实 |
| 解释与控制 | L2 | 候选 → 执行、等待、修改或停止 | 权限、预算、状态和并发条件 |
| 受控执行 | L3 / L4，L2 协调 | 合法请求 → 真实回执或明确错误 | 服务端仍执行自身授权和规则 |
| 记录与更新 | L2 经 L3 | 结果 → 可恢复进度和事件 | 外部副作用与本地记录存在故障窗口 |
| 核验与交付 | L1 + L2 | 证据 → 完成、等待、失败或转人工 | Turn 结束不自动等于 Task 成功 |

检索、核验和补充信息可以多次发生。不是所有任务都依次执行表中每一项，也不是所有任务都需要外部工具；表格表达责任和接口，而不是固定脚本。

## 5. 一个有边界的 Agent Loop

```text
load task + run state + current authorization
                ↓
check stop / cancel / budget / pending operations
                ↓
build context → invoke model → interpret candidate
                ↓
     ┌──────────┼─────────────┐
     ↓          ↓             ↓
  工具请求    用户输入请求     完成候选
     ↓          ↓             ↓
校验与授权    持久化等待     按契约核验
     ↓          ↓             ↓
记录动作意图  释放运行资源    通过 / 继续 / 升级
     ↓
受控执行或查询异步任务
     ↓
保存结果与证据 → 更新状态 → 下一轮
```

图里最容易被简化掉的是“pending operations”。恢复执行时，不能只问模型下一步做什么，必须先处理系统已经知道的未决动作。

同样，Loop 不能只在模型报完成时停止。用户取消、权限撤销、预算耗尽、持续无进展、依赖不可用都可能要求暂停或结束。模型的完成候选还要接受对应的结果验证。

深入：[Loop](../docs/03-AgentLoopRuntimeState.md)、[Goal / Stop / Budget](../docs/08-PlanningGoalStopBudget.md)。

## 6. 四类信息不能混成一个 Memory

| 信息 | 回答的问题 | 例子 | 正确性边界 |
|---|---|---|---|
| 模型上下文 | 这一次模型看到了什么？ | 指令、近期消息、证据摘要、可见工具 | 是有预算的工作视图，不是全部事实 |
| 执行状态 | 系统执行到哪里？ | 当前状态、待审批动作、未决 Operation、已用预算 | 应可被程序解释；需要恢复时必须可靠保存 |
| 长期记忆 | 哪些信息值得以后复用？ | 经授权保存的偏好、事实、经验或操作方法 | 可能过期、冲突或受污染，必须有生命周期 |
| 外部事实 | 真实系统已经发生了什么？ | 文件版本、外部任务状态、数据库记录 | 由相关权威系统拥有，需要时重新查询 |

历史记录是一组发生过的交互；Context 是为当前推理选出的视图；Checkpoint 是为了恢复执行保存的数据。它们可以共享内容，但不是同一物。

Memory 写入也应有过程：候选产生 → 来源与授权检查 → 去重与冲突处理 → 写入 → 后续检索 → 过期或删除。删除或权限变更还要考虑索引、缓存和派生摘要，不能只删除一处文本。

深入：[Memory](../docs/11-MemoryArchitectureLifecycle.md)、[Session / State / History](../docs/12-SessionStatePersistence.md)。

## 7. Compaction 应该改变什么，不应该改变什么

Compaction 改变的是**供后续模型使用的信息表示**。它不应该直接替换系统唯一的审批证据、动作回执或幂等记录。

建议明确两类数据：可压缩的推理工作材料，以及必须可靠保存、能按需重新加载的执行依据。重要依据通常包括目标与硬约束、待处理动作、审批绑定、稳定资源 ID、产物引用、外部回执与未解决问题。

在压缩之后，系统还需要能知道引用是否仍有效、事实是否已过期、后续写操作是否须重新读取状态。不能只用“压缩后 Token 降低了多少”评价正确性。

Compaction、长期任务交接和故障恢复是三个相关但不同的问题。Anthropic 的长运行 Harness 文章也指出，仅有压缩不足以保证跨上下文窗口持续取得可靠进展。[S14](sources.md#s14)

深入：[Compaction Correctness](../docs/10-ContextCompactionCorrectness.md)。

## 8. Run 状态与外部 Operation 状态分开

下面是可选的 Run 状态设计：

```text
created → queued → running
                    ├─ waiting_input → running
                    ├─ waiting_approval → running
                    ├─ waiting_external → running
                    ├─ suspended → running
                    ├─ completed
                    ├─ failed
                    └─ cancelling → cancelled
```

Operation 另有自己的状态，例如 `prepared / dispatched / succeeded / failed / unknown`。实际系统还应定义每个状态允许哪些转换，以及由谁写入。

这两种状态不能混合：Run 可以已经收到取消请求，但某个外部 Operation 已成功；Run 可以等待外部结果，而其 Worker 已经释放。等待人类或远程回调，不必持续占用模型请求和工作进程。

`unknown` 是必要的显式状态，不是需要用一句“应该失败了”填掉的空白。

## 9. 生产级难点：副作用与持久化不是一个原子动作

通用失败时间线：

```text
T0 记录 operation_id、目标资源、参数摘要与动作意图
T1 向外部服务提交动作
T2 外部服务执行成功
T3 回应丢失，或本地结果记录失败
T4 当前 Worker 退出
T5 新 Worker 接管 Run
```

新 Worker 不能因为本地没有成功记录就直接重做，也不能仅因为保存过意图就断定已经成功。

建议恢复顺序是：读取未决 Operation → 使用稳定标识查询外部状态或利用接口幂等契约 → 保存已核对结果 → 再继续。没有查询接口或可靠幂等语义时，应根据风险暂停、请求人工处理或采取明确的补偿流程，不能凭空承诺 exactly-once。

“先记意图再调用”缩小的是信息缺失范围，不会消除所有故障窗口。即使状态仍是 `prepared`，进程也可能在请求已发出但尚未更新 `dispatched` 时退出。

自动重试前至少要回答：错误属于传输、限流、参数、权限还是领域规则？动作是否幂等？前一次是否可能已执行？是否有剩余预算？重试会不会改变目标或参数？

深入：[Tool Failure](../docs/06-ToolExecutionFailure.md)、[Side Effect / Cancellation](../docs/07-ToolSideEffectCancellation.md)、[Checkpoint / Resume](../docs/13-CheckpointResumeReliability.md)、[通用后端机制](../../backend-engineering/README.md)。

## 10. 审批必须绑定到可识别动作

一个可审计的审批记录应明确：批准者身份、目标资源、动作类型、关键参数或其摘要、有效期、授权范围，以及相关状态或策略版本。

审批界面显示的内容、模型请求的内容和最终提交的内容需要一致。目标、关键参数或条件发生变化时，不能默认沿用旧批准。

审批后、实际执行前仍应检查当前身份权限和必要的资源前置条件。这防止“审批时允许、执行时条件已变”的问题。审批是跨 L1 交互、L2 控制、L3 传递和 L4 强制检查的完整链条。

取消审批不会自动撤销一个已经完成的外部动作。系统需要处理迟到批准、重复批准、迟到结果，以及取消与完成同时发生的竞态。

深入：[Permission / Approval / HITL](../docs/14-PermissionApprovalSandbox.md)。

## 11. Worker、执行环境和持久状态的生命周期

```text
持久状态：Task / Run / Event / Checkpoint / Operation / Artifact 引用
                        ↑
                可替换的 Harness Worker
                        ↓
           可按需要创建和重建的执行环境
```

Worker 负责推进执行，不应成为任务正确性唯一依赖的内存容器。执行环境丢失后，可以按策略重建，但其中尚未保存的文件和进程状态不会神奇恢复，必须事先决定哪些内容持久化。

如果需要多个 Worker 接管同一 Run，还要有租约、状态版本或等价并发控制，防止旧 Worker 与新 Worker 同时推进。Fencing 只有在相关写入方或接入边界实际检查时才有效，不能只在数据库保存一个数字就宣称所有外部动作都被隔离。

如果状态存储不可用，应明确哪些只读操作可以继续、哪些高风险写操作必须停下。不能为了保持“可用”而丢掉后续核对副作用所需的唯一证据。

会话、运行核心与环境解耦的产品参考见 [S04](sources.md#s04)。

## 12. Event、Trace、Audit 与 Artifact

| 记录 | 用途 | 设计提醒 |
|---|---|---|
| UI Streaming Event | 展示及时进展 | 可能需要断线重连、游标和去重；流式输出不是持久化承诺 |
| Durable Event / State | 恢复与状态重建 | 事件序列、幂等处理、版本和保留期要明确 |
| Trace | 调试、归因与性能分析 | 记录可观察输入输出、调用、耗时和用量；不要假设可获取模型私有内部推理 |
| Audit Record | 追溯身份、授权与动作 | 敏感操作可能要求完整保留，不能照搬调试采样策略 |
| Artifact | 交付或复查具体产物 | 标明位置、版本或内容摘要、访问权限、生命周期 |

一次 UI 展示可以由多个事件还原。真正重要的不是保存每一个 Token，而是知道哪些信息丢失会破坏恢复、授权证明或结果验收。

## 13. 一个参考状态记录

下面是用于讨论责任的简化结构，不是可直接替代数据库设计的产品 Schema：

```json
{
  "task_id": "task_001",
  "run_id": "run_001",
  "worker_attempt_id": "attempt_002",
  "thread_id": "thread_001",
  "status": "waiting_external",
  "state_version": 8,
  "agent_definition_version": "agent-v3",
  "policy_version": "policy-v2",
  "budget_used": {"model_calls": 4, "tool_calls": 3},
  "pending_operation_ids": ["op_001"],
  "approval_refs": ["approval_001"],
  "checkpoint_ref": "checkpoint_008",
  "artifact_refs": ["artifact_001"],
  "last_durable_event_sequence": 27
}
```

真实实现还需要身份与租户关联、任务契约、事件时间、错误、凭证引用和数据保留规则等。不要把原始 Secret 写进这样的通用状态对象，更不要默认整条记录都该发送给模型。

## 14. 三个不同的“完成”

**模型输出完成**表示一次生成结束。**Run 完成**表示这次受管理执行到达规定终态。**Task 成功**表示任务的验收条件得到满足。三者可能相邻发生，但不能互相推断。

交付时应说明已经完成什么、依据是什么、还有什么没有完成或无法确认。产物或外部回执比“我已完成”的自述更能支撑可核验结论。

最后用一句话串起状态视图：

> **模型使用当前上下文提出行动，Runtime 根据持久进度和权限控制执行，外部系统提供真实反馈，任务依据验收条件决定是否成功。**
