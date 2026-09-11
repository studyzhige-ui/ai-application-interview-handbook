# 10. 为什么需要 MQ：Delivery Semantics 与 Failure Model

> MQ 的价值不是“异步”两个字，而是把 Producer 与 Consumer 的时间、容量和失败生命周期解耦。

## 1. 没有 MQ 会怎样

同步链：

```text
API
→ OCR
→ Chunk
→ Embedding
→ Index
→ Response
```

问题：

- 请求时间过长；
- 任一环失败整条失败；
- 突发流量直接打到下游；
- Worker 无法独立扩容；
- Crash 后缺少可重放边界。

MQ 改成：

```text
API
→ create durable task
→ MQ(task_id)
→ Worker
→ durable result
```

用户不需要一直保持原 HTTP Connection。

---

## 2. MQ 提供什么能力

常见价值：

```text
Decoupling
Buffering
Async execution
Consumer scaling
Retry / Replay
Delivery tracking
```

但每个能力都有代价：

```text
Duplicate
Ordering
Backlog
Eventual Consistency
Operational Complexity
```

---

## 3. Producer / Broker / Consumer 三段 Failure

### Producer Failure

```text
send message
→ timeout
```

Producer 不知道 Broker 是否已经持久化。

如果 Retry，可能重复。

### Broker Failure

可能发生：

- message 尚未复制；
- leader 切换；
- disk failure；
- metadata unavailable。

### Consumer Failure

最经典：

```text
consume message
→ side effect succeeds
→ process crashes before ack
→ message redelivered
```

所以 Consumer 必须幂等。

---

## 4. At-most-once

```text
先 ack
→ 再处理
```

Crash 后可能不再重投。

优点：避免重复。

代价：可能丢业务工作。

适合可以接受丢失的非关键 Event。

---

## 5. At-least-once

```text
处理成功
→ ack
```

Crash 在处理后、Ack 前：

```text
message redelivered
```

因此可能重复。

这是很多任务系统更常见的语义：

> 宁可重复，也不要静默丢失；重复由 Idempotency 解决。

---

## 6. Exactly-once 为什么要说边界

某些 MQ / Stream 系统在自己的 Transaction / Processing Boundary 内可以提供 exactly-once semantics。

但跨系统：

```text
MQ
→ external payment
→ MySQL
→ email
```

不能因为 MQ 提供局部 exactly-once 就宣称整个业务链“一定只执行一次”。

课程里默认采用更保守的工程表达：

```text
At-least-once Delivery
+ Idempotent Consumer
+ Durable State
+ Reconciliation
```

---

## 7. Ack 是什么意思

Ack 的本质通常是：

> Consumer 告诉 Messaging System：这条消息在它负责的消费语义里已经处理到可以继续推进的位置。

它不自动证明：

- 外部副作用永久成功；
- DB 一定 Commit；
- 所有下游都一致。

Ack Timing 必须与 Side Effect / State Transition 配合。

---

## 8. Dead Letter Queue

反复失败的消息如果一直 Retry：

```text
poison message
→ retry
→ fail
→ retry
→ fail
```

会浪费大量消费能力。

DLQ / Parking Queue 可以把它移出主消费路径：

```text
max attempts reached
→ DLQ
→ alert / inspect / repair / replay
```

但 DLQ 不是“错误垃圾桶”。

必须有人处理：

- 为什么失败；
- 是否可以 Repair；
- 是否重新 Replay；
- 是否永久终止。

---

## 9. Ordering

很多业务并不需要全局严格顺序。

常见真正需要的是：

```text
same order_id ordered
same user ordered
same run_id ordered
```

按 Key Partition 可以获得局部顺序，同时保留跨 Key 并发。

如果要求全局单序列，吞吐通常会受明显限制。

---

## 10. Backlog

如果：

```text
producer rate > consumer capacity
```

Backlog 持续增长。

要监控：

```text
queue depth / lag
oldest message age
consumer throughput
processing latency
failure rate
retry rate
```

单看“MQ 还能写进去”毫无意义。

---

## 11. MQ vs Database Polling

有时系统会：

```text
DB task table
→ worker periodically SELECT pending rows
```

这可以工作，尤其规模不大时。

MQ 的优势常在：

- push-style consumption；
- consumer group；
- buffering；
- ordering / partition；
- replay；
- independent scaling。

但不要为了架构漂亮，所有异步任务都强制上 MQ。

---

## 12. MQ vs Redis Stream

Redis Stream 可以承担一部分可靠消息工作，但是否适合取决于：

- retention；
- replay；
- data volume；
- ecosystem；
- operational requirements；
- existing Redis pressure。

Redis 章节讲具体 Stream；这里讲消息语义。

---

## 13. AI 场景：Ingestion

```text
Upload
→ task_id persisted
→ MQ
→ parse worker
→ chunk worker
→ embedding worker
→ index
```

不要把完整文档内容反复塞进消息。

更常见：

```text
MQ carries task_id / object_key / version
```

大 Payload 放 Object Storage / DB。

---

## 14. AI 场景：Agent Tool Async Job

某个 Tool 需要 10 分钟：

```text
Agent Runtime
→ create external job
→ MQ / worker
→ durable job state
→ later event / poll
```

Agent Checkpoint 保存的是 Runtime State；MQ 负责工作 Delivery。两者职责不同。

---

## 15. Retry 谁负责

可能有：

```text
producer retry
broker redelivery
consumer retry
business retry
```

如果每层都独立 Retry，会非常混乱。

必须定义：

- transport retry；
- processing attempt；
- max attempts；
- backoff；
- DLQ；
- idempotency key。

---

## 16. 🎯 面试怎么答

**问：为什么需要 MQ？**

可以回答：

> MQ 的核心不是单纯异步，而是把 Producer 与 Consumer 的时间和容量解耦，提供 Buffer、消费扩展、重放等能力。例如长任务可以快速返回 task_id，再由 Worker 消费。但它也引入重复、顺序、积压和最终一致性问题，所以要配合 Ack、幂等 Consumer、Backlog 监控和 DLQ，而不是“上 MQ 就可靠”。

---

## 17. ⚠️ 易错点

- MQ ≠ 自动不丢消息；
- Ack ≠ 业务全链成功；
- At-least-once ≠ Exactly-once；
- DLQ ≠ 永久忽略；
- Queue 能写入 ≠ 系统健康；
- MQ ≠ 所有异步场景的默认答案。

---

## 18. 本章自测

<details>
<summary>1. Consumer 处理成功但 Ack 前 Crash，会发生什么？</summary>

在 At-least-once 语义下消息可能重新投递，因此 Consumer 需要幂等或去重，避免副作用重复。

</details>

<details>
<summary>2. 为什么 MQ 中最好传 task_id 而不是巨大文档内容？</summary>

消息系统更适合传递工作引用和事件。巨大 Payload 会增加 Broker 存储、复制、网络和 Retry 成本，大数据更适合放 Object Storage / DB。

</details>

<details>
<summary>3. DLQ 以后还需要做什么？</summary>

监控和人工/自动处置：分析 Root Cause、修复数据或代码、判断能否 Replay，不能把 DLQ 当成无人负责的垃圾桶。

</details>