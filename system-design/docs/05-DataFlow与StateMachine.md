# 05｜Sync / Async、Data Flow 与 State Machine

系统设计的第三张核心图不是组件图，而是：

> **数据到底怎样流、哪些步骤同步等待、哪些步骤异步解耦、失败时状态停在哪里。**

---

## 1. Sync Path 解决“现在就要答案”

同步链路典型：

```text
Client
→ API
→ Validate
→ DB Read / Tool Call
→ Build Response
```

适合：

- 用户必须立即看到结果；
- 下游延迟可控；
- 操作链较短；
- 失败可以直接反馈调用方。

代价是：

```text
每多一个同步依赖
→ Tail Latency 变长
→ Failure Coupling 变强
```

---

# 2. Async Path 解决“可以稍后完成”

例如视频处理：

```text
POST /videos
→ persist task
→ enqueue
→ return 202 + task_id

Worker
→ transcode
→ extract metadata
→ save result
```

用户再：

```text
GET /tasks/{id}
```

或者接收 Webhook / SSE。

---

# 3. Async 不是“更快”，而是解耦等待

用户看到的提交延迟可能更低，但真实任务仍要执行。

异步带来的新问题：

```text
Queue
Retry
Duplicate Delivery
Out-of-order
Task State
Worker Crash
Backpressure
```

所以不能把“丢进 MQ”当完成设计。

---

# 4. 先画 Data Flow，再选 Queue

错误顺序：

```text
我们用 Kafka
→ 看能做什么
```

正确顺序：

```text
谁产生事件？
谁消费？
是否要 Replay？
是否要求 Ordering？
允许重复吗？
消息保留多久？
峰值多大？
```

再决定 MQ / Stream / Task Queue。

---

# 5. Event 和 Command 要区分

## Command

表达：

> 请某个能力执行动作。

例如：

```text
GenerateInvoice(order_id)
```

## Event

表达：

> 某件事已经发生。

例如：

```text
OrderPaid(order_id)
```

如果所有消息都叫“event”，很容易模糊 Ownership。

---

# 6. State Machine 是长流程的骨架

例如文件处理：

```text
UPLOADED
→ VALIDATING
→ PARSING
→ PROCESSING
→ COMPLETED
```

失败分支：

```text
VALIDATING_FAILED
PROCESSING_RETRYABLE
PROCESSING_FAILED
CANCELLED
```

State Machine 让：

- API 知道展示什么；
- Worker 知道能不能 Claim；
- Retry 知道从哪一步继续；
- 运维知道卡在哪里。

---

# 7. Exactly-once 通常不该轻易承诺

很多系统更现实的模式是：

```text
at-least-once delivery
+
idempotent consumer
+
durable state transition
```

因为：

```text
Worker 完成副作用
→ Ack 前崩溃
→ Message redelivery
```

如果 Consumer 不幂等，就重复执行。

---

# 8. Outbox 思想解决什么

经典问题：

```text
DB commit 成功
但 publish event 失败
```

于是业务状态已经变化，但下游永远不知道。

Outbox 思想：

```text
同一 DB Transaction
├─ write business row
└─ write outbox row

后续 Publisher
→ read outbox
→ publish
→ mark sent
```

它不等于全局强一致，但能减少“DB 成功 / Event 丢失”的双写窗口。

---

# 9. Fan-out / Fan-in

一个任务可能并行调用：

```text
Search A
Search B
Search C
```

然后合并：

```text
Fan-out
→ partial results
→ Fan-in
```

需要定义：

```text
全部成功才算成功？
允许 Partial？
Deadline 到了怎么办？
慢分支要不要 Cancel？
```

RAG Hybrid、Agent Multi-tool、聚合 API 都会遇到。

---

# 10. Cancellation 必须进入 Data Flow

用户断开不一定意味着：

```text
所有后台副作用都应该停止
```

例如：

```text
支付已经提交
```

不能因为 HTTP Disconnect 就随便回滚。

要区分：

```text
Cancelable Compute
Committed Side Effect
Durable Async Job
```

Cancellation 是业务语义，不只是 `task.cancel()`。

---

# 11. Workflow 的每一步要记录什么

Long-running Task 建议有：

```text
run_id
step_id
status
attempt
input_ref
output_ref
started_at
finished_at
error
lease_owner
version
```

否则任务跑几小时后失败，很难 Resume 或 Debug。

---

# 12. 🎯 面试怎么答

> 我会先把主流程画成同步和异步两部分：用户必须立刻知道的放 Sync Path，耗时、可延迟或需要削峰的工作进入 Durable Async Path。异步链路会显式设计任务状态机、幂等 Consumer、Retry、Lease 和 Backpressure，而不是只说“加 MQ”。如果业务状态和 Event 必须一起可靠地产生，我会考虑 Outbox 等模式。最后对 Fan-out、Partial Result 和 Cancellation 定义清楚语义。

---

# 13. 本章自测

<details><summary>1. 为什么 MQ 不能自动保证业务 Exactly-once？</summary>
消息可能重复投递，Consumer 可能在副作用成功后 Ack 前崩溃，因此业务层仍需要幂等和持久状态。
</details>

<details><summary>2. Outbox 主要修复什么窗口？</summary>
业务 DB 已提交但消息发布失败，导致下游永久漏事件的窗口。
</details>

<details><summary>3. 为什么 Cancellation 不能只绑定 HTTP 连接？</summary>
因为请求可能已经触发不可逆或需要完成的业务副作用，连接断开不等于这些工作可以安全取消。
</details>
