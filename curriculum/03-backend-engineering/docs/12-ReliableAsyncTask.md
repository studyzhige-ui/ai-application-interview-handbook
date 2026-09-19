# 12. Reliable Async Task：Outbox、Lease、Heartbeat、Worker Recovery 与 Long-running API

> 长任务的核心不是“放到后台”，而是：**任务状态可持久、Delivery 可恢复、Worker Crash 后可重新领取、重复执行可控、用户可以查询/取消。**

## 1. 为什么 Background Task 不够

如果只是：

```text
HTTP response
→ in-process background coroutine
```

进程重启：

```text
task disappears
```

对于：

- 文档解析；
- OCR；
- 大批量 Embedding；
- Agent 长任务；
- 数据迁移；

这种语义通常不够。

---

## 2. Reliable Task Pattern

经典结构：

```text
Client
→ API creates task record
→ MQ carries task_id
→ Worker claims task
→ heartbeat / lease
→ result persisted
→ user polls / subscribes
```

核心原则：

> **Task 的 durable state 不应该只存在 MQ 或 Worker Memory 中。**

---

## 3. Task State Machine

推荐显式：

```text
QUEUED
→ RUNNING
→ SUCCEEDED
   / FAILED_RETRYABLE
   / FAILED_FINAL
   / CANCEL_REQUESTED
   / CANCELLED
```

必要时增加：

```text
PAUSED
WAITING_EXTERNAL
```

State Machine 帮助回答：

- 什么时候允许 Retry；
- 什么状态可以 Cancel；
- Crash 后谁恢复；
- UI 应显示什么。

---

## 4. Task Record 至少保存什么

```text
task_id
kind
status
owner / tenant
input_ref
attempt
created_at
updated_at
worker_id
lease_until
progress
result_ref
error_code
version
```

大文件、大输出不要都塞任务表，可以保存 Object Storage 引用。

---

## 5. 为什么 MQ 只传 task_id 很常见

```text
DB task row = durable truth
MQ message = delivery signal
```

好处：

- Message 小；
- Retry 只传 ID；
- Worker 可重新读取最新任务状态；
- Schema 演进更简单。

---

## 6. Outbox Problem

经典双写：

```text
DB insert task
↓
MQ publish
```

如果 DB 成功、MQ 失败：

```text
task exists but no message
```

反过来先 MQ：

```text
message exists but DB task missing
```

Transactional Outbox 思路：

```text
DB transaction:
  insert business/task row
  insert outbox row
commit
↓
outbox relay publishes MQ
↓
mark published
```

这样把“业务状态 + 待发送事件”放在同一 DB Transaction Boundary 内。

注意：MQ publish 仍可能重复，因此 Consumer 仍需幂等。

---

## 7. Claim 与 Lease

Worker 领取任务：

```text
worker-A claims task-1
lease_until = now + 30s
```

Lease 表示：

> 这个 Worker 在一段时间内拥有执行权，但所有权会过期。

为什么不用永久锁？

Worker 可能：

- Crash；
- 网络断开；
- OOMKilled；
- Node 掉电。

永久 Owner 会让任务永远卡住。

---

## 8. Heartbeat

长任务持续续租：

```text
lease 30s
heartbeat every 10s
```

正常：

```text
heartbeat
→ extend lease
```

Worker Crash：

```text
no heartbeat
→ lease expires
→ another worker may reclaim
```

Heartbeat 只是 Liveness 信号，不能证明任务每一步都正确。

---

## 9. Reclaim 的重复执行问题

危险 Timeline：

```text
Worker A performs side effect
→ heartbeat lost
→ lease expires
→ Worker B reclaims
→ performs same side effect again
```

因此 Lease 必须和：

- Idempotency；
- Fencing / Version；
- durable checkpoint；
- status verification

一起设计。

---

## 10. Fencing Token 的直觉

每次重新领取任务分配递增 generation：

```text
A owns generation 7
lease expires
B owns generation 8
```

下游写入要求：

```text
only latest generation accepted
```

这样旧 Worker A 即使“复活”也不能继续覆盖新状态。

并不是所有系统都需要 Fencing，但涉及并发旧 Owner 时要理解这个问题。

---

## 11. Long-running API

提交：

```http
POST /jobs
```

返回：

```http
202 Accepted
```

```json
{
  "task_id": "task_123",
  "status": "queued"
}
```

查询：

```http
GET /jobs/task_123
```

事件：

```http
GET /jobs/task_123/events
```

取消：

```http
POST /jobs/task_123/cancel
```

这个模型比保持一个 20 分钟 HTTP Request 更可靠。

---

## 12. Cancellation

Cancel 通常不是：

```text
kill process immediately
```

更安全：

```text
CANCEL_REQUESTED
→ worker observes
→ stop at safe point
→ cleanup / compensate
→ CANCELLED
```

外部 Tool 可能无法强制停止，所以还需要业务状态区分：

```text
cancel requested
but external operation may complete
```

---

## 13. Retry Strategy

任务 Retry 应持久化 attempt：

```text
attempt = 1
→ transient fail
→ next_run_at = now + backoff
→ attempt = 2
```

不要让 Worker 内存里 `for retry in range(100)`。

Worker Crash 后 Retry State 会丢。

---

## 14. Progress

长任务通常要暴露：

```text
stage
processed_items
total_items
percent?
last_heartbeat
```

但“百分比”不总是可计算。

Agent 任务更适合：

```text
current_step
last_event
tool state
```

而不是虚假的 73%。

---

## 15. 大文件 Ingestion

```text
Upload complete
→ task created
→ parse
→ OCR
→ chunk
→ embedding
→ index
```

每个 Stage 可以有独立状态和重试边界。

不要从 Stage 5 失败就重新 Upload + OCR 一遍，除非 Processing Version 发生变化。

---

## 16. Task Version / Processing Version

数据管道需要：

```text
source_version
parser_version
chunk_version
embedding_model_version
index_version
```

否则 Retry / Reprocess 很难知道旧产物是否还能复用。

---

## 17. Metrics

```text
queued_tasks
oldest_task_age
running_tasks
lease_expired_count
reclaim_count
attempt_distribution
success_rate
cancel_latency
stage_latency
```

其中：

> `oldest_task_age` 往往比单纯 Queue Length 更能体现用户体验。

---

## 18. 🎯 面试怎么答

**问：Worker 处理任务一半宕机怎么恢复？**

可以回答：

> 我会把任务状态持久化，不只依赖 MQ。Worker Claim 任务时获得有限 Lease，并周期 Heartbeat；Worker 宕机后 Lease 过期，其他 Worker 可以 Reclaim。为了防止旧 Worker 恢复或 Side Effect 已成功导致重复，还需要 Idempotency、Generation/Fencing 或 Checkpoint。Retry attempt 和 next_run_at 也应该持久化，而不是只存在 Worker 内存。

---

## 19. ⚠️ 易错点

- MQ 有消息 ≠ Task 状态完整；
- Heartbeat ≠ Checkpoint；
- Lease ≠ Idempotency；
- Reclaim ≠ 安全重复执行；
- Cancel Request ≠ External Side Effect 一定被撤销；
- Outbox ≠ Consumer exactly-once。

---

## 20. 本章自测

<details>
<summary>1. Outbox 解决了什么双写问题？</summary>

把业务状态与“待发送消息”记录放进同一数据库事务，避免业务状态已提交但 MQ publish 丢失。Relay 后续负责发布，消息仍可能重复，因此 Consumer 仍需幂等。

</details>

<details>
<summary>2. Lease 过期后为什么可能产生重复 Side Effect？</summary>

旧 Worker 可能已执行副作用但失联，新 Worker Reclaim 后无法知道结果，再执行一次。需要 Idempotency / Fencing / Status Verification。

</details>

<details>
<summary>3. 为什么 Retry attempt 应持久化？</summary>

Worker 本身可能 Crash；如果 Retry 状态只在内存，Crash 后会失去次数与 Backoff，导致无限重试或节奏失控。

</details>