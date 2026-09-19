# 13. Checkpoint / Resume：检查点、恢复、分叉与重放

短任务失败了可以让用户重试。

长任务不行。

如果 Agent 已经运行 40 分钟、修改了 12 个文件、执行了 3 个外部 Tool，并且刚完成一半：

> **服务崩溃后还能不能继续？继续时会不会重复执行副作用？**

这就是 Checkpoint（检查点） / Resume（恢复执行） / Long-running Reliability 要解决的问题。

[← 上一章](12-StateHistoryAndPersistence.md) · [Agent 目录](../README.md) · [下一章 →](14-PermissionApprovalAndSandbox.md)

---

<a id="section-1"></a>

## 1. Checkpoint 不是“把聊天记录存一下”

<a id="legacy-13-01"></a>

Checkpoint（检查点）记录一个可以恢复工作的位置及必要状态。Resume（恢复执行）是读取这些记录，把任务继续下去。英文résumé可以指简历，但本章resume是动词“继续”，不是summary（摘要）。Compaction（上下文压缩）缩减模型输入，与恢复相关但不是同一操作。

报告任务在“已读A/B、尚未上传”保存检查点C1；随后上传报告，服务崩溃。新进程读C1只知道当时没上传，**不知道之后上传是否已成功**。检查点不会让外部世界自动退回C1，这正是恢复难点。

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

但 Runtime（运行时执行系统） 不知道：

```text
哪一步已经真正成功执行
```

这会导致重复副作用。

---

<a id="section-2"></a>

## 2. Checkpoint 应该发生在哪里

<a id="legacy-13-02"></a>

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

| 中间动作 | 重启时的策略 | 必要依据 |
|---|---|---|
| 纯计算/可重读 | 允许从旧点重做 | 重算成本和当前输入适用性 |
| 已有可靠成功回执的写入 | 补齐当前状态，不重复做 | 操作身份和真实回执 |
| 可能已发生但没有确定结果 | 先核对，不能盲重试 | 下游幂等键、可查询对象或人工处理 |

所以不是“每秒检查点才安全”。关键动作可以有**独立的可靠操作记录**，检查点是阶段性状态视图，两者不必同一频率。即使每步检查点，外部写入与本地保存之间仍可能存在故障窗口。

---

<a id="section-3"></a>

## 3. Long-running Task 的状态机

<a id="legacy-13-03"></a>

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

<a id="section-4"></a>

## 4. Resume 的第一步不是“继续调用模型”

<a id="legacy-13-04"></a>

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

<a id="section-5"></a>

## 5. 最危险的问题：Tool 成功，但 Checkpoint 失败

<a id="legacy-13-05"></a>

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

> **Agent Reliability 最难的不是模型，而是 Side Effect 与 State（状态） Persistence（持久化） 的一致性。**

```text
C1：文件已处理，待上传
→ 可靠记录操作意图op7（目标、必要参数或引用、稳定幂等键）
→ 请求下游执行op7
→ 下游成功创建report42
→ 本地记录op7的回执report42
→ C2：已上传，可交付
```

若在请求前崩溃，可从意图继续；若请求后回执前崩溃，向下游查询op7，或在其幂等契约有效期内使用同一键重试。若下游不支持查询或去重，程序可能无法安全判定，应进入待核对/人工处理，而不是生成新键再上传。

`call_id`关联一次模型工具请求，`operation_id`表示一个业务逻辑动作，`attempt_id`表示某次网络尝试。重试次数增长不该制造新业务动作。究竟使用哪些ID由接口决定，不必为了这三个名字复制三个完全相同字段。

### 补偿不是把世界退回过去

Compensation（补偿）是新增一项业务操作来缓解已发生结果，例如撤销尚未处理的工单。邮件已经被收件人阅读就不能真正“回滚成没看过”。补偿本身可能失败、需要授权，并且应关联原操作，不是任何错误后都自动补偿。无法确定原动作是否发生时，先核对，避免未发生也做反向操作。

检查点频率因此是重算成本、保存开销和风险的取舍。廉价只读步骤可以粗粒度保存；批准、取消或不可重复写入的关键事实按更严格时机保存。不能把所有步骤都提升为必须永久保存的高风险事件。

---

<a id="section-6"></a>

## 6. Idempotency 是第一道防线

<a id="legacy-13-06"></a>

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

<a id="section-7"></a>

## 7. Side-effect Ledger

<a id="legacy-13-07"></a>

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

Ledger（操作记录）不等于保存所有日志。对不能盲重做的动作，记录哪个逻辑操作、是否发出、回执或未知结果即可；大内容用授权产物引用关联。

---

<a id="section-8"></a>

## 8. Compensation 什么时候需要

<a id="legacy-13-08"></a>

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

下游既不能查询又没有幂等接口时，不存在靠多存几个版本号就保证恰好一次的方法。限制自动重试，明确待确认并设计人工核对。补偿也是可能失败的新动作，不一定恢复到从未执行的世界。

---

<a id="section-9"></a>

## 9. Pause / Resume 与 HITL

<a id="legacy-13-09"></a>

Approval（批准） 场景：

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

<a id="section-10"></a>

## 10. Cancellation 与 Resume 的关系

<a id="legacy-13-10"></a>

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

<a id="section-11"></a>

## 11. Resume 和 Fork 不一样

<a id="legacy-13-11"></a>

### Resume

```text
继续同一个 Run / lineage
```

### Fork

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

> **Source Provider（模型服务方） 与 Applied Snapshot 要分开建模。**

---

<a id="section-12"></a>

## 12. Replay 是什么

<a id="legacy-13-12"></a>

Replay（重放） 至少有两种。

### 12.1 State Replay

```text
从 Event Log 重建 Runtime State
```

### 12.2 Execution Replay

```text
重新执行同样 Tool / Model Call
```

第二种很危险，因为外部环境可能已经变化，模型也不一定 deterministic。

所以 Production（生产环境） “Replay”常更适合：

```text
重放 evidence / events
→ 重建观察
→ Debug / Eval
```

而不是无脑再次触发副作用。

| 操作 | 目的 | 不能假设 |
|---|---|---|
| Resume（恢复） | 同一任务在明确位置继续 | 摘要就是完整状态 |
| Fork（分叉） | 从某个状态创建另一条探索分支 | 外部数据库和已发邮件也被复制或撤销 |
| State replay（状态重建） | 用已保存事件重建程序状态 | 自动重做真实工具 |
| Model replay（模型重演） | 用选定输入重新请求模型做比较 | 同样输入必得同样答案 |
| Side-effect replay（动作重放） | 再次执行外部动作 | 安全、幂等和环境不变 |

先加载身份与取消状态，检查配置/状态兼容，核对未决操作，恢复必要产物引用与环境，重建模型上下文，再继续执行。Cold resume（冷恢复）要在新进程建立环境；Warm resume（热恢复）可能复用仍存的资源，但都不应省略关键核对。

暂停审批需要记录具体待批动作；取消后旧检查点不能自动让任务重新开始。Worker lease（执行租约）用来协调谁可推进任务，租约过期不代表旧Worker物理停止；Fencing（隔离旧写者）需由实际写入边界检查代次或令牌。

---

<a id="section-13"></a>

## 13. Worker Lease 与 Ownership

<a id="legacy-13-13"></a>

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

<a id="section-14"></a>

## 14. Checkpoint Schema 一个示例

<a id="legacy-13-14"></a>

下面是较完整的示意菜单，不是每个应用强制Schema。先确定恢复位置、未知外部动作和需重新加载资源，再选字段与引用。

```python
# 检查点示意：记录可恢复位置与必要引用；不是所有应用必须照抄的完整Schema。
from dataclasses import dataclass

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

先列出重启后的承诺：不重复上传、保留取消、能取回报告、知道哪些证据未验证。由此决定必要状态和操作记录。然后单独决定诊断采样，不能倒过来“先把一切都记成Trace（执行追踪），再希望恢复时能拼出来”。保留期限和存储成本同样是契约的一部分。

---

<a id="human-a"></a>

## 15. HUMAN-A 信号

本章主要承接：

- `AGENT-026`：Timeout / Cancel / Interrupt / Resume；
- `AGENT-027`：Checkpoint / Persistence / Resume；
- `AGENT-029`：Tool 成功但 Checkpoint 失败后的重复副作用。

这些都是 L4 Failure / System Design 问题。

---

<a id="interview"></a>

## 16. 面试怎么答

### Q：Agent Checkpoint 应该保存什么？

🎯 **30 秒回答**：

> 不能只存聊天历史。至少要能恢复 run identity、当前 step、goal/plan、pending work、artifact refs、tool correlation、side-effect ledger、approval、budget 和版本信息。Resume 时先 reconcile 不确定副作用，再重建 context 和执行环境，从 safe point 继续。对于支付、发消息这类外部副作用，要结合 idempotency key、external reference 或 compensation，避免 Tool 成功但 checkpoint 失败后重复执行。

### Q：Tool 成功但服务崩了，怎么避免重试两次？

🎯 **30 秒回答**：

> Runtime 要有 operation id / idempotency key 或 side-effect ledger。恢复后先向下游 reconcile；确认已成功则把状态补齐，不再执行。没有幂等能力的动作要设计 compensation 或人工确认，不能只靠“重试次数”。

### Q：Checkpoint的作用是什么，两点之间崩溃怎么办？

🎯 **30 秒回答**：

> 检查点保存可继续的状态位置，不回滚外部世界。两点间的纯计算可重做；已知成功的写入凭可靠回执补齐；未知写入先靠稳定操作ID查询或按下游幂等契约重试。关键动作记录可以比检查点更细，没有可核对依据就承认未知并请人处理。

### Q：为什么工具成功后立刻存检查点仍可能重复？

🎯 **30 秒回答**：

> 外部成功与本地存档不是同一事务，仍有响应丢失或本地崩溃窗口。需要操作意图、下游幂等/查询以及回执来核对；不能只靠提高检查点频率，也不能每次重试换业务ID。

### Q：Resume和Compaction、Replay有什么区别？

🎯 **30 秒回答**：

> Resume恢复执行；Compaction缩减当前模型输入；Replay可能是用事件重建状态、重新请求模型或重做外部动作，三种风险不同。恢复可以使用摘要构建输入，但不能仅凭摘要决定是否重复写入。

### Q：Fork需要复制什么？

🎯 **30 秒回答**：

> 复制允许继承的状态和引用，并明确身份、权限、预算、工作区及资源隔离。已经发生的外部动作不是可以deepcopy或回滚的世界。分叉后的新动作需要自己的权限与逻辑身份。

### Q：框架有Checkpointer是否就不需要幂等？

🎯 **30 秒回答**：

> 仍需要。框架主要恢复图或会话状态，节点重启、中断前代码重跑和外部响应丢失都可能重复副作用。应按框架明确的恢复单位包装动作，并用真实下游契约验证。

---

<a id="pitfalls"></a>

## 17. 高频易错点

⚠️ **Checkpoint = Messages Snapshot。** 不足以恢复执行正确性。

⚠️ **Retry（重试） 就能恢复所有 Tool。** 非幂等 Tool 可能制造重复副作用。

⚠️ **Cancel 只改 DB status。** 还要传播到 Tool / Process / Child Agent。

⚠️ **Replay = 再执行一遍。** 对真实副作用很危险。

⚠️ **每秒检查点就没有故障窗口。** 跨系统副作用仍不与本地存档天然原子。

⚠️ **恢复先把旧Prompt再发一次。** 先核对当前状态、取消与未决副作用。

⚠️ **补偿等于数据库回滚。** 补偿是新业务动作，也会失败且未必可逆。

⚠️ **租约到期旧Worker一定停止。** 需在写入边界拒绝旧所有者，不靠时间想象。

⚠️ **保存全部Trace便能精确重现世界。** 模型、服务和外部事实都可能变化，重演有明确范围。

---

<a id="self-test"></a>

## 18. 本章自测

<details><summary>1. 为什么 Checkpoint 最好发生在语义安全点？</summary>

因为如果记录发生在外部 Tool 已发送但结果未知的中间状态，恢复后很难判断是否应该重试，容易产生重复副作用。

</details>

<details><summary>2. Resume 和 Fork 最大区别是什么？</summary>

Resume 延续同一个执行 lineage；Fork 从某个历史状态派生新运行，因此必须显式定义继承哪些 snapshot / memory / workspace / instruction，以及哪些 ownership/side-effect 状态不能继承。

</details>

<details><summary>3. 为什么需要 Worker Lease / Fencing？</summary>

长任务接管时旧 Worker 可能恢复。没有 generation/fencing，两个 Worker 都可能继续推进同一 Run 并写入冲突状态。

</details>

<details><summary>4. 上传成功后C2没写，恢复读C1，应直接再上传吗？</summary>

先用原逻辑操作身份核对。如果下游可幂等返回同一对象则补齐本地状态；结果未知且无安全查询/去重能力则暂停处理。

</details>

<details><summary>5. 读取A的步骤没存检查点可以重做吗？</summary>

若只读可重取且允许当前版本输入，可以重做；若要求当时快照则需要对应保存策略。不是所有步骤都必须完全不重做。

</details>

<details><summary>6. 事件重建时把所有历史Tool再执行一次有何问题？</summary>

事件已描述动作发生过，再执行会重复副作用且环境可能已变。重建状态通常只应用记录，不执行真实动作。

</details>

<details><summary>7. 为什么取消意图可能需要独立保存？</summary>

恢复若只读取消前检查点，会再次继续用户已停止的任务。新Worker必须从权威状态知道取消，而不是只看旧模型历史。

</details>

<details><summary>8. 示例代码证明了什么，没证明什么？</summary>

证明稳定逻辑ID在模拟下游去重时避免重复对象；没证明磁盘耐久、并发安全、真实网络恢复或所有接口幂等。

</details>

<details><summary>9. LangGraph中断后重跑节点，与恢复已保存状态矛盾吗？</summary>

不矛盾。框架保存的是定义的图执行边界，不是任意CPU指令。节点代码可能从头运行，因此需要对中断前动作采取幂等或可独立恢复安排。

</details>

---

[← 上一章](12-StateHistoryAndPersistence.md) · [Agent 目录](../README.md) · [下一章 →](14-PermissionApprovalAndSandbox.md)
