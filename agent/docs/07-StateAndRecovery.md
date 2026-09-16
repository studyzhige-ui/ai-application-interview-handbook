# 07. L2 运行层：执行状态、持久化与恢复

[← 06](06-MemoryLifecycle.md) · [Agent 主线](../README.md) · [08 →](08-MultiAgentCoordination.md)

> 主线位置：**L2 运行层**。信息可被使用还不够，任务中断后也要知道准确的执行事实。
>
> 本章产物：**可恢复的状态机与副作用核对协议**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 分两段读：先理解状态/历史/检查点，再推演恢复与副作用。这里先采用最小动作契约：有稳定 operation_id，返回成功/失败/未知，可核对外部结果；11章再展开 Executor，不必先学完整实现才能理解故障窗口。

[哪些状态必须独立于上下文存在](#part-1) → [状态所有权、并发和租户边界](#part-2) → [检查点与恢复边界](#part-3) → [先核对副作用，再继续推理](#part-4) → [暂停、取消、分叉、重放和接管](#part-5)

<a id="part-1"></a>

## 1. 哪些状态必须独立于上下文存在

运行层既要让模型“知道发生了什么”，更要让程序准确知道“做到哪里、谁在执行、哪些动作可能已经发生”。本章的 Run / 状态名是教学工作定义，Codex 的交互对象仍采用第04章的 Thread / Turn / Item 语义。

| 对象 | 保存的事实 | 不替代什么 |
|---|---|---|
| Context | 当前模型可见信息 | 不是唯一恢复依据 |
| Runtime State | 进度、待办、操作、审批、预算、版本 | 不是全部外部业务状态 |
| History / Event Log | 已发生的消息和执行事件 | 不自动等于可重放的外部动作 |
| Checkpoint | 恢复边界及关联状态/资源引用 | 不自动回滚外部世界 |
| Memory | 为未来复用而维护的信息 | 不替代操作回执和状态机 |
| Source of Truth | 外部系统的权威状态 | 不由 Agent 的总结决定 |

### State 应该保存什么

Runtime State 的目标不是“保存所有文本”，而是支持：

```text
下一步正确决策
恢复
取消
审计
并发控制
```

可以分几类。

#### Identity State

```text
session_id
run_id
turn_id
current_step_id
```

#### Control State

```text
status
current_goal
plan
budget
retry_count
active_tool_call
```

#### Environment State Reference

```text
workspace_id
sandbox_id
artifact ids
file generation
```

#### Safety State

```text
permission mode
approved action ids
policy version
```

#### Progress State

```text
completed steps
pending steps
blocked reason
```

### History 应该是事件流，而不是“一个超长字符串”

更稳妥的模型：

```text
Event 1: UserMessage
Event 2: ModelOutput
Event 3: ToolCall
Event 4: ToolResult
Event 5: Approval
Event 6: StateTransition
```

每条事件有：

```text
event_id
session_id
run_id
turn_id
timestamp
type
payload
correlation_id
```

这样 Trace、Replay、Checkpoint 才有可靠基础。

### Snapshot 与 Event Log 怎么配合

如果每次恢复都从第 1 条 Event 重放：

```text
session 越长
→ replay 越慢
```

一种常见设计是：

```text
Durable Event Log
+
Periodic State Snapshot
```

恢复时：

```text
load latest snapshot
→ replay newer events
```

这里是通用架构模式，不声称 Claude Code / Codex 一定使用同样的数据存储实现。

### Persistence 不等于把 Context 存下来

错误思维：

```text
把当前 prompt JSON 存 DB
→ resume 时再发给模型
```

问题是 Prompt 只是 State 的一个投影。

真正需要持久化的可能还有：

```text
side effects
artifact refs
tool call correlation
approval
budget
workspace version
pending task
```

因此：

> **Context 是可重新编译的 View；State 才是 Runtime 的事实。**

<a id="part-2"></a>

## 2. 状态所有权、并发和租户边界

读写状态必须绑定身份与版本。同一个会话可以选择排队、拒绝并发或隔离分支，但不能让两个写入者无协调覆盖状态。

### Tenant Isolation 为什么必须进入 State Schema

多租户系统不能只是：

```text
WHERE user_id = ?
```

在一个业务代码分支里“记得加”。

建议所有核心 State Object 自带：

```text
tenant_id
workspace_id
user_id
```

并在：

```text
storage key
query filter
cache key
tool permission
artifact path
trace scope
```

都显式传播。

对应 HUMAN-A `AGENT-017 Multi-tenant State Isolation`。

### Session Hijack / Cross-tenant Pollution

经典事故：

```text
cache key = session:{session_id}
```

如果 session_id 不是全局不可猜且查询没有 tenant boundary：

```text
Tenant A
→ 构造 B 的 session id
→ 读到 B state
```

更稳：

```text
session:{tenant_id}:{session_id}
```

但 Key 设计仍不能替代服务端授权检查。

### Concurrency：同一个 Session 同时来两个请求怎么办

例如：

```text
Request A: “继续执行任务”
Request B: “先停止，改需求”
```

如果两个 Worker 同时修改 State：

```text
Lost Update
Out-of-order Event
Duplicate Tool
```

可以使用：

```text
optimistic version
single owner lease
serialized event append
per-run queue
```

关键是：

> **同一 Run 的 State Transition 必须有并发协议。**

### State Version 为什么重要

伪代码：

```text
read state version=42
compute update
write where version=42
→ success: version=43
→ fail: someone else updated
```

这样可以发现 Lost Update。

对于长任务还可以维护：

```text
state_generation
checkpoint_generation
instruction_generation
```

后面 Resume 时很重要。

<a id="part-3"></a>

## 3. 检查点与恢复边界

保存什么取决于怎样恢复；仅保存最后一句回复不足以安全接管任务。

### Checkpoint 不是“把聊天记录存一下”

真正的可恢复执行至少要保存：

```text
Run identity
Current status
Goal / constraints
Plan / progress
Current step
Pending work
Tool call correlation
External side-effect ledger
Artifact references
Workspace version
Permission / approval state
Budget / retry state
Instruction generation
```

如果只保存 Messages：

```text
模型可能知道之前聊了什么
```

但 Runtime 不知道：

```text
哪一步已经真正成功执行
```

这会导致重复副作用。

### Checkpoint 应该发生在哪里

不是每个 CPU instruction 都能 checkpoint。

更适合在“语义安全点”：

```text
Tool result 已确认
State transition 已提交
Artifact 已持久化
外部副作用已登记
Plan step 已完成
```

例如：

```text
Tool call sent
但结果未知
```

这不是一个很好恢复的状态，因为 crash 后不知道 Tool 到底执行没执行。

### Checkpoint Schema 一个示例

```python
@dataclass
class Checkpoint:
    run_id: str
    generation: int
    state_version: int
    current_step: str
    plan_state: dict
    artifact_refs: list[str]
    side_effects: list[dict]
    pending_approvals: list[str]
    budget_state: dict
    instruction_version: str
```

重点不在字段名，而在：

```text
它能否让 Runtime 在另一台机器、另一个进程里继续正确执行？
```

### Cold Resume 与 Warm Resume

可以区分：

#### Warm Resume

```text
worker 还在
in-memory objects 还在
```

#### Cold Resume

```text
进程已经重启
只剩 durable state
```

如果系统只支持 Warm Resume：

```text
真正 crash 后仍恢复不了
```

所以 Production 设计要问：

> **哪些运行事实只在内存，哪些必须 durable？**

Codex Source Index 对 Thread Instructions 也明确区分 warm resume、cold resume / offline fork、live fork 的 instruction snapshot/provider 继承边界，这说明 Resume 不是简单“重新加载聊天”。

<a id="part-4"></a>

## 4. 先核对副作用，再继续推理

动作提交与本地保存之间可能出现不确定窗口。恢复必须先核对、去重或保留未决状态，而不是先重新调用模型让它猜。

### Resume 的第一步不是“继续调用模型”

恢复流程更像：

```text
Load checkpoint
→ Validate generation / ownership
→ Reconcile unfinished side effects
→ Re-open artifact / workspace references
→ Rebuild Context
→ Re-establish permission / provider state
→ Continue from safe step
```

如果跳过 Reconcile：

```text
旧 Tool 可能已经成功
→ Resume 又执行一次
```

### 最危险的问题：Tool 成功，但 Checkpoint 失败

HUMAN-A `AGENT-029` 就在问这个。

时间线：

```text
T0 Agent 调用 send_email
T1 Email API 返回成功
T2 Runtime 准备写 checkpoint
T3 DB crash
T4 Worker restart
T5 Checkpoint 仍显示 send_email 未完成
T6 Resume 再发一次
```

结果：

```text
用户收到两封邮件
```

所以：

> **Agent Reliability 最难的不是模型，而是 Side Effect 与 State Persistence 的一致性。**

### Idempotency 是第一道防线

如果 Tool 支持：

```text
idempotency_key = run_id + step_id
```

重复调用时下游识别：

```text
这个动作已经执行过
→ 返回原结果
→ 不重复副作用
```

适合：

```text
payment
message send
job submit
external create API
```

但不是所有外部系统都支持 Idempotency Key。

### Side-effect Ledger

Runtime 可以显式记录：

```text
operation_id
step_id
tool_name
request_fingerprint
status: planned/sent/confirmed/unknown
external_reference
result_hash
```

Resume 时：

```text
confirmed → 不再执行
unknown → reconcile with external system
planned  → 可以执行
```

这比：

```text
“看聊天记录猜是不是执行过”
```

可靠得多。

### Compensation 什么时候需要

有些操作不能幂等，但可以补偿：

```text
reserve inventory
→ later cancel reservation
```

这接近 Saga 思想：

```text
Action A
Action B
Action C failed
→ compensate B
→ compensate A
```

Agent Harness 不应该自己发明通用分布式事务，但需要知道：

> **外部副作用的恢复策略属于 Tool Contract / Workflow Contract。**

<a id="part-5"></a>

## 5. 暂停、取消、分叉、重放和接管

这些都是不同的生命周期操作。一个可继续的执行系统必须明确它们对已发生动作的影响。

### Long-running Task 的状态机

可以从：

```text
pending
running
paused
waiting_approval
waiting_external
completed
failed
cancelled
```

开始。

Claude Code Source Index 中 `Task.ts` 已确认有：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

这支持一个稳定抽象：

> **Task 应该是有身份、状态机、输出位置和终止语义的一等 Runtime 对象，而不是一个普通 async function。**

### Pause / Resume 与 HITL

Approval 场景：

```text
Agent 想执行 delete_production_table
→ Runtime emits interruption
→ Persist RunState
→ user approves / rejects
→ Resume
```

OpenAI Agents SDK 的 HITL 官方文档明确支持：

- Tool Call interruption；
- 序列化 RunState；
- 审批后 resume；
- approval 在 handoff / nested agent 中传播。

这说明：

> **HITL 本身就是 Checkpoint / Resume 的一种具体 Runtime 场景。**

### Cancellation 与 Resume 的关系

Cancel 不是简单把状态写成：

```text
cancelled
```

还要：

```text
propagate abort
stop child task
close stream
release lease
terminate sandbox process
mark unfinished tool state
persist final cancellation state
```

Claude Code 索引显示：

- Conversation / turn 层有 `AbortController`；
- Tool 层有 `interruptBehavior(): cancel | block`。

所以 Cancellation 是跨 Runtime / Tool 的协议。

### Resume 和 Fork 不一样

#### Resume

```text
继续同一个 Run / lineage
```

#### Fork

```text
从某个历史状态派生一个新 Run
```

Fork 需要回答：

```text
继承哪些 instructions？
继承哪些 memory？
继承 workspace snapshot 吗？
继承 side-effect ledger 吗？
新的 run_id 是什么？
```

Codex Source Index 中 Thread Instructions 的固定提交明确讨论：

- warm resume 保留 provider；
- cold resume / offline fork 重新提供；
- live fork / subagent 继承 applied snapshot，但不继承 source provider；
- refresh 要 cancellation-safe。

课程抽象：

> **Source Provider 与 Applied Snapshot 要分开建模。**

### Replay 是什么

Replay 至少有两种。

#### State Replay

```text
从 Event Log 重建 Runtime State
```

#### Execution Replay

```text
重新执行同样 Tool / Model Call
```

第二种很危险，因为外部环境可能已经变化，模型也不一定 deterministic。

所以 Production “Replay”常更适合：

```text
重放 evidence / events
→ 重建观察
→ Debug / Eval
```

而不是无脑再次触发副作用。

### Worker Lease 与 Ownership

多 Worker 系统还要防：

```text
Worker A 处理 Run 123
A 网络断开
调度器误以为 A 死了
Worker B 接管
A 又恢复
```

现在 A/B 可能同时推进。

需要：

```text
run owner / lease
lease generation / fencing
state version
```

防止 stale worker 写新状态。

这和 Redis 分布式锁里学过的 Fencing 思想相通，但 Runtime Ownership 不等于“直接套一个 Redis Lock”。

### Session Retention / Deletion

Session 也有生命周期：

```text
active
idle
archived
expired
deleted
```

需要定义：

- 保留多久；
- 是否允许用户删除；
- artifact 是否联动删除；
- trace / billing 是否有独立保留规则；
- Memory 是否跟 Session 一起删除。

这些不能都靠一个 Redis TTL 解决。

## 恢复推演：操作标识先于可重试的副作用

本表是教学协议，用来打开“工具成功、检查点失败”的窗口，并不宣称跨系统恰好一次交付。

| 崩溃位置 | 已知事实 | 恢复动作 |
|---|---|---|
| 动作意图尚未持久化 | 未建立可恢复操作身份 | 不声称已经提交；重新按任务状态决策 |
| 意图/幂等键已保存，尚未发送 | 知道逻辑动作和授权边界 | 重新校验前置条件后才发送 |
| 已发送，回执未知 | 可能已产生副作用 | 用同一operation_id/幂等键核对，不盲建新动作 |
| 外部成功，本地检查点失败 | 权威结果可能已存在 | 补齐本地状态与回执，不再次执行成功动作 |
| 无幂等接口且不能查询 | 系统没有足够证据判断 | 保留UNKNOWN并转人工/业务核对；补偿也可能有风险 |

事件、审批和产物记录同样有版本。恢复时还要区分**指令来源**与**已应用快照**：Fork可以继承某个快照，却不自动获得实时来源、凭证或原任务批准。`ThreadInstructionsProvider` 的warm/cold resume、fork及快照差别见[固定Codex索引第8节](../../research/agent-sources/codex-source-index.md)。这些是产品实现观察；本课程不把Run与Codex Turn强绑为一棵通用树。

## 本章自测

<details>
<summary>工具成功但检查点写入失败，恢复时先做什么？</summary>

核对已记录操作标识、幂等键和外部状态；确认已发生的副作用后再继续，不能盲重放写操作。

</details>

<details>
<summary>Fork 是否复制外部世界？</summary>

不会。分叉的是执行/交互状态及允许复制的引用；真实外部动作不能因分叉被假设撤销或重做。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>换worker后应沿用哪个ID核对已提交的动作？</summary>

沿用逻辑operation_id及对应幂等键/外部引用；attempt_id可以变化，但不得冒充新业务动作。

</details>

<details>
<summary>没有幂等也没有查询接口，怎样保证未知动作只执行一次？</summary>

不能凭空保证；保留UNKNOWN并采取业务核对/人工处理，不能把重试或补偿宣称恰好一次。

</details>

[本章面试练习与具体追问](../interview/README.md#chapter-07) · [综合复习](../review/README.md)

## 回到主线

现在应能独立说明：可恢复的状态机与副作用核对协议。下一章：[L2 运行层：多 Agent 协作与调度](08-MultiAgentCoordination.md)。

对应真人问题：`AGENT-017`、`AGENT-027`、`AGENT-029`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 06](06-MemoryLifecycle.md) · [Agent 主线](../README.md) · [08 →](08-MultiAgentCoordination.md)
