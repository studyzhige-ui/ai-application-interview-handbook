# 13. Checkpoint / Resume / Fork / Replay 与 Long-running Reliability

短任务失败了可以让用户重试。

长任务不行。

如果 Agent 已经运行 40 分钟、修改了 12 个文件、执行了 3 个外部 Tool，并且刚完成一半：

> **服务崩溃后还能不能继续？继续时会不会重复执行副作用？**

这就是 Checkpoint / Resume / Long-running Reliability 要解决的问题。

---

## 1. Checkpoint 不是“把聊天记录存一下”

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

---

# 2. Checkpoint 应该发生在哪里

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

---

# 3. Long-running Task 的状态机

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

---

# 4. Resume 的第一步不是“继续调用模型”

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

---

# 5. 最危险的问题：Tool 成功，但 Checkpoint 失败

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

---

# 6. Idempotency 是第一道防线

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

---

# 7. Side-effect Ledger

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

---

# 8. Compensation 什么时候需要

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

---

# 9. Pause / Resume 与 HITL

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

---

# 10. Cancellation 与 Resume 的关系

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

---

# 11. Resume 和 Fork 不一样

## Resume

```text
继续同一个 Run / lineage
```

## Fork

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

---

# 12. Replay 是什么

Replay 至少有两种。

## 12.1 State Replay

```text
从 Event Log 重建 Runtime State
```

## 12.2 Execution Replay

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

---

# 13. Worker Lease 与 Ownership

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

---

# 14. Checkpoint Schema 一个示例

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

---

# 15. HUMAN-A 信号

本章主要承接：

- `AGENT-026`：Timeout / Cancel / Interrupt / Resume；
- `AGENT-027`：Checkpoint / Persistence / Resume；
- `AGENT-029`：Tool 成功但 Checkpoint 失败后的重复副作用。

这些都是 L4 Failure / System Design 问题。

---

# 16. 面试怎么答

## Q：Agent Checkpoint 应该保存什么？

🎯 **30 秒回答**：

> 不能只存聊天历史。至少要能恢复 run identity、当前 step、goal/plan、pending work、artifact refs、tool correlation、side-effect ledger、approval、budget 和版本信息。Resume 时先 reconcile 不确定副作用，再重建 context 和执行环境，从 safe point 继续。对于支付、发消息这类外部副作用，要结合 idempotency key、external reference 或 compensation，避免 Tool 成功但 checkpoint 失败后重复执行。

## Q：Tool 成功但服务崩了，怎么避免重试两次？

> Runtime 要有 operation id / idempotency key 或 side-effect ledger。恢复后先向下游 reconcile；确认已成功则把状态补齐，不再执行。没有幂等能力的动作要设计 compensation 或人工确认，不能只靠“重试次数”。

---

# 17. 高频易错点

⚠️ **Checkpoint = Messages Snapshot。** 不足以恢复执行正确性。

⚠️ **Retry 就能恢复所有 Tool。** 非幂等 Tool 可能制造重复副作用。

⚠️ **Cancel 只改 DB status。** 还要传播到 Tool / Process / Child Agent。

⚠️ **Replay = 再执行一遍。** 对真实副作用很危险。

---

# 18. 本章自测

<details><summary>1. 为什么 Checkpoint 最好发生在语义安全点？</summary>

因为如果记录发生在外部 Tool 已发送但结果未知的中间状态，恢复后很难判断是否应该重试，容易产生重复副作用。
</details>

<details><summary>2. Resume 和 Fork 最大区别是什么？</summary>

Resume 延续同一个执行 lineage；Fork 从某个历史状态派生新运行，因此必须显式定义继承哪些 snapshot / memory / workspace / instruction，以及哪些 ownership/side-effect 状态不能继承。
</details>

<details><summary>3. 为什么需要 Worker Lease / Fencing？</summary>

长任务接管时旧 Worker 可能恢复。没有 generation/fencing，两个 Worker 都可能继续推进同一 Run 并写入冲突状态。
</details>
