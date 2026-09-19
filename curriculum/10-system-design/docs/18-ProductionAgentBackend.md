# 18｜Production Agent Backend 与 Long-running Agent

这是 System Design 中最重要的 AI-native 场景之一，对应：

```text
SD-021 Production Agent Backend
SD-022 Long-running Agent Runtime
```

真人面经信号也最强：Production Agent Backend 13 个独立来源，Long-running Agent 10 个。

但本章不重复 Agent Harness 单点原理，而是回答：

> **怎样把 Agent Loop、State、Tool、Checkpoint、Streaming、Auth、Worker、Queue、Observability 和 Scale 组合成一个真正可运营的后端。**

---

## 1. 先定义 Run 是什么

Production Agent 最核心的业务实体不是“Chat Message”，而通常是：

```text
AgentRun
```

它有：

```text
run_id
tenant_id
user_id
agent_id
status
input
goal
current_step
checkpoint
budget
created_at
updated_at
```

Run 是跨多轮 Model / Tool 的 Durable Boundary。

---

# 2. 一张 Production Agent 总图

```text
Client
  ↓
API / Auth / Admission
  ↓
Run Service
  ↓
Scheduler / Queue
  ↓
Agent Worker / Runtime
  ├─ Model Gateway
  ├─ Tool Gateway
  ├─ RAG / Memory
  └─ Sandbox
  ↓
Durable State / Checkpoint / Artifact
  ↓
Trace / Eval / Usage
```

Streaming 通常从 Runtime Event 转发给 Client，但 Durable State 不能只存在连接内。

---

# 3. 为什么不能把 Run 绑死在 HTTP Request

Agent 可能执行：

```text
10 秒
10 分钟
10 小时
```

如果生命周期完全等于：

```text
HTTP connection
```

会面临：

- Client disconnect；
- Proxy timeout；
- deploy/restart；
- worker crash；
- network change。

所以长任务通常是：

```text
POST /runs
→ create durable run
→ return run_id / stream endpoint
```

Run 可以独立于连接继续或被明确 Cancel。

---

# 4. Run State Machine

```text
CREATED
→ QUEUED
→ RUNNING
→ WAITING_APPROVAL
→ RUNNING
→ SUCCEEDED
```

失败：

```text
RETRYABLE
FAILED
CANCEL_REQUESTED
CANCELLED
```

长任务甚至可能：

```text
PAUSED
→ RESUMED
```

状态必须 Durably Persist。

---

# 5. Run / Turn / Step / ToolCall

建议把执行层级拆开：

```text
Run
└─ Turn / Iteration
   └─ Step
      ├─ Model Call
      └─ Tool Call
```

这样 Trace 才能回答：

```text
第几轮开始偏？
哪个 Tool 失败？
Context 在哪一轮爆？
哪个 Step 产生副作用？
```

---

# 6. Event Model 与 Streaming

Runtime 产生：

```text
run_started
step_started
model_delta
tool_call_started
tool_call_result
approval_requested
checkpoint_saved
run_completed
```

API 层可以转成：

```text
SSE / WebSocket
```

但要区分：

```text
Transient UI Event
vs
Durable Execution Event
```

不是所有 Token Delta 都需要永久存储，但关键 State Transition / Tool Side Effect 应可审计。

---

# 7. Checkpoint 是什么

Checkpoint 不是简单：

```text
messages.json
```

它至少要恢复：

```text
Goal / Constraint
Current Plan / Step
Durable State
Relevant Context / Summary
Tool Side-effect Record
Budget
Permission / Approval State
Version
```

否则 Resume 后可能“恢复聊天”，却恢复不了任务正确性。

---

# 8. 最危险的 Failure：Tool 成功，Checkpoint 失败

时间线：

```text
1. Agent calls create_ticket
2. External system created ticket #123
3. Runtime crashes before checkpoint
4. Resume from old checkpoint
5. Agent calls create_ticket again
```

结果：

```text
duplicate ticket
```

所以 Long-running Agent 必须设计：

```text
operation_id
idempotency
external result lookup
step state
compensation
```

这正是 `SD-022` 的核心 Production 深度。

---

# 9. Worker Lease

Scheduler 分配：

```text
run_id → worker-A
lease_until=t
```

Worker Heartbeat。

如果崩溃：

```text
lease expires
→ run can be reclaimed
```

但旧 Worker 可能还活着，所以 State Transition 需要 Version / Fencing，避免两个 Worker 同时推进同一个 Run。

---

# 10. Context 与 Artifact 分离

长任务会产生：

```text
large file
log
browser result
code diff
image
```

不应该全部塞进 Model Context。

常见：

```text
Artifact Store
→ persist large result
→ Context stores summary + reference
→ load on demand
```

这样控制 Token 和恢复成本。

---

# 11. Model Gateway / Tool Gateway

Agent Worker 不应该每种 Provider / Tool 都自己实现可靠性。

可以抽：

```text
Model Gateway
→ routing / retry / cost / stream

Tool Gateway / Registry
→ schema / auth / execute / audit
```

Agent Harness 负责 Loop 和选择，Gateway 负责稳定能力边界。

---

# 12. Permission / Approval

高风险 Tool：

```text
refund
send email
execute shell
delete resource
```

Agent Runtime 遇到：

```text
requires approval
```

Run 进入：

```text
WAITING_APPROVAL
```

用户确认后继续。

批准信息必须持久化，Resume 后不能丢。

---

# 13. Multi-tenant Resource Governance

Per Tenant：

```text
max concurrent runs
max model tokens
max steps
max tool calls
cost budget
priority
```

否则一个无限循环 Agent 可以耗尽全平台 Worker 和 Provider Quota。

---

# 14. Backpressure

如果：

```text
run arrival
>
worker capacity
```

Queue Age 增长。

系统应该：

```text
admission limit
queue quota
priority
scale workers
reject / schedule later
```

而不是无限接收。

---

# 15. Cancellation

用户 Cancel：

```text
Run → CANCEL_REQUESTED
```

Runtime：

- 停止新 Model / Tool Step；
- 传播 Cancel 到可取消子调用；
- 等待/处理已提交副作用；
- 保存最终 Checkpoint；
- 标记 CANCELLED。

如果外部 Tool 已不可逆完成，Cancellation 不能假装回滚。

---

# 16. Observability

一次 Run 至少能查：

```text
run timeline
step duration
model/token/cost
context size
tool input/result/error
retry
approval
checkpoint
state transition
worker / lease
```

以及 Outcome：

```text
success?
verified?
human accepted?
```

---

# 17. Evaluation

Production Agent 不能只看：

```text
final answer looks good
```

应评估：

```text
Task Success
Tool Selection
Tool Args
Step Count
Loop Rate
Recovery Success
Cost
Latency
Side-effect Correctness
Human Escalation
```

长任务还要测试：

```text
kill worker mid-step
resume
cancel
provider outage
duplicate event
```

---

# 18. Deployment / Upgrade

如果 Worker 正在跑 V1 Runtime，新版本 V2 发布：

要问：

```text
old checkpoint can V2 read?
run pinned to version?
canary new runs only?
how to drain workers?
```

Long-running 系统的 Deploy 不是简单滚动重启。

---

# 19. 真人面经如何改变深度

这两个 Canonical 都是全库 System Design 最强信号之一。

因此本章必须深入：

```text
Checkpoint / Resume
Cancellation
Idempotency
External Side Effect
State Migration
Worker Recovery
Streaming
Auth
Observability
Scale
```

而不是只画“LLM → Tool → Memory”。

---

# 20. 🎯 面试怎么答

> Production Agent 我会把一次执行建模成 Durable AgentRun，而不是绑定单个 HTTP 请求。入口负责 Auth/Admission，Run Service 持久化状态，Scheduler/Queue 分配 Worker，Runtime 调 Model/Tool/RAG，并把关键 Step、Side Effect、Checkpoint 和 Approval 写入 Durable State。Long-running Reliability 的重点是 Tool 成功但 Checkpoint 失败这类边界，所以所有外部副作用都要有 operation id / idempotency / result lookup。Worker 用 lease+version 支持 Reclaim，Context 与大 Artifact 分离，最后用 Trace/Eval 验证 Task Success、Recovery、Cost 和 Side-effect Correctness。

---

# 21. 本章自测

<details><summary>1. 为什么 AgentRun 不应该依赖 HTTP Connection 存活？</summary>
长任务可能跨分钟/小时和部署重启，连接只是交互通道，执行状态必须独立持久化。
</details>

<details><summary>2. Long-running Agent 最危险的重复副作用窗口是什么？</summary>
Tool 已成功产生外部副作用，但 Runtime 在保存 Checkpoint 前崩溃，Resume 后可能再次调用 Tool。
</details>

<details><summary>3. 为什么 Worker Lease 还需要 Version/Fencing？</summary>
Lease 过期不代表旧 Worker 一定停止；新旧 Worker 可能并发推进同一 Run，需要版本化状态写保护。
</details>
