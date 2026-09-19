# 09｜Queue、Backpressure 与 Long-running Task

> **本章定位：System Design 组合层。** 这里训练 Queue / Worker / Long-running Task 怎样进入整体架构。Backpressure、MQ Delivery 与 Durable Task 的完整机制分别回到 [AIBE Backpressure](../../03-backend-engineering/docs/06-Backpressure与RateLimit.md)、[AIBE MQ](../../03-backend-engineering/docs/10-MQ与DeliverySemantics.md) 和 [AIBE Reliable Async Task](../../03-backend-engineering/docs/12-ReliableAsyncTask.md)。

异步系统最常见的误区是：

> **有 MQ = 系统就能扛住高峰。**

实际上 Queue 只是把“处理不过来”从同步调用链搬到了缓冲区。真正的问题是：

> **上游持续快于下游时，怎样不让 Queue 无限增长、Worker 重复执行、任务长期卡死？**

---

## 1. Queue 解决什么

常见价值：

```text
Decouple
Buffer Burst
Async Work
Retry Boundary
Fan-out
```

例如文档 Ingestion：

```text
Upload
→ enqueue document_id
→ Parse Worker
→ Embed Worker
→ Index Writer
```

用户不需要同步等几分钟。

---

# 2. Queue 不能创造处理能力

如果：

```text
arrival rate = 1000 tasks/s
service rate = 600 tasks/s
```

Queue 每秒净增长：

```text
400 tasks
```

不管 Queue 多大，迟早会爆。

所以必须监控：

```text
Queue Depth
Queue Age
Arrival Rate
Completion Rate
Retry Rate
```

其中 Queue Age 往往比 Depth 更有业务意义。

---

# 3. Backpressure 是什么

Backpressure = 下游能力不足时，上游必须感知并减速。

可以：

```text
Block
Reject
Rate Limit
Reduce Concurrency
Pause Consumer / Producer
Drop Low-priority Work
Degrade Feature
```

而不是继续无限排队。

---

# 4. Concurrency Limit 是容量契约

例如 LLM Provider：

```text
最多 100 concurrent calls
```

如果 Worker 开 1000 并发：

```text
429
→ Retry
→ 更大流量
→ Retry Storm
```

因此：

```text
Queue
→ Worker
→ Semaphore / Concurrency Limit
→ Downstream
```

才是真正受控的消费模型。

---

# 5. At-least-once Delivery 下要接受 Duplicate

消息系统常见：

```text
Worker receives
→ executes side effect
→ crashes before ACK
→ message redelivered
```

所以 Consumer 要：

```text
idempotent
or
state-aware
```

不能假设“一条消息只来一次”。

---

# 6. Lease / Heartbeat：长任务怎么 Claim

对于耗时任务：

```text
READY
→ RUNNING(worker-7, lease_until=t)
```

Worker 定期 Heartbeat：

```text
extend lease
```

如果 Worker 崩溃：

```text
lease expires
→ another worker may reclaim
```

这比“从 Queue 拿出来就永久属于这个 Worker”更可靠。

---

# 7. Reclaim 会引入重复执行

旧 Worker 可能只是网络分区，实际上还在跑。

Lease 到期后：

```text
Worker A continues
Worker B reclaims
```

于是两个 Worker 同时执行。

所以还需要：

```text
idempotency
fencing / version
compare-and-set state transition
```

Long-running 可靠性不能只靠 Heartbeat。

---

# 8. Task API 的标准形态

提交：

```http
POST /jobs
→ 202 Accepted
→ {job_id}
```

查询：

```http
GET /jobs/{id}
```

返回：

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

可选：

```text
progress
current_step
retry_count
artifact_url
error_code
```

---

# 9. Cancellation 要定义到 Step

用户点击 Cancel：

```text
CANCEL_REQUESTED
```

Worker 在安全点检查：

```text
before new step
before side effect
between chunks
```

如果已经进入不可逆动作：

```text
不能假装立刻停止
```

需要：

```text
complete current side effect
or compensate
```

---

# 10. Priority Queue / Fair Scheduling

多租户系统里，一个大 Tenant 可能塞满 Queue。

如果纯 FIFO：

```text
Tenant A 100K jobs
→ Tenant B 的 1 个 job 等几小时
```

可考虑：

```text
per-tenant queue
weighted fair scheduling
priority class
quota
```

否则 Queue 会成为资源隔离漏洞。

---

# 11. Dead-letter / Poison Task

某任务每次都失败：

```text
retry 10000 times
```

只会浪费资源。

需要：

```text
max_attempt
error classification
DLQ / failed state
manual / automated remediation
```

Permanent Error 不应该继续重试。

---

# 12. Queue 的 Ordering 要按业务定义

不是所有任务都需要全局顺序。

例如：

```text
同一 account 的操作要有序
不同 account 可以并行
```

可以用：

```text
partition key = account_id
```

避免为了“有序”把整个系统变成单线程。

---

# 13. 🎯 面试怎么答

> Queue 解决解耦和短期 Burst，但不会创造处理能力。我会同时设计 arrival/service rate、Queue Age、Worker Concurrency 和下游容量，通过 Backpressure、Rate Limit 或 Load Shedding 保持稳定。长任务会用 Durable Task State + Lease/Heartbeat 支持 Worker Crash Recovery，同时用 Idempotency/Fencing 防止 Reclaim 后重复副作用。多租户还要做 Fair Scheduling，Poison Task 则进入 Failed/DLQ，而不是无限 Retry。

---

# 14. 本章自测

<details><summary>1. 为什么 Queue Depth 下降不一定代表系统健康？</summary>
可能是任务被大量丢弃或消费者异常跳过；需要结合 Queue Age、Completion Rate、Error Rate 等判断。
</details>

<details><summary>2. 为什么 Lease + Heartbeat 仍不能保证任务只执行一次？</summary>
旧 Worker 可能只是失联但仍在执行，Lease 过期后新 Worker 会 Reclaim，形成并发重复执行。
</details>

<details><summary>3. 为什么多租户 Queue 需要 Fairness？</summary>
否则单个大租户可以占满队列和 Worker，使其他租户长期饥饿，破坏资源隔离和 SLO。
</details>
