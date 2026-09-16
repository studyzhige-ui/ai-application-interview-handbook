# 11. Kafka：Partition、Consumer Group、Ordering 与 Backlog

> 这一章不把 Kafka 讲成完整产品手册，而是掌握 AI Backend 面试最常追问的：**Partition、Consumer Group、Ordering、Offset、Rebalance 与 Backlog。**

## 1. Kafka 的核心抽象

可以先理解成：

```text
Topic
├─ Partition 0: record → record → record
├─ Partition 1: record → record → record
└─ Partition 2: record → record → record
```

Partition 是 Kafka 并行与顺序语义的核心边界之一。

---

## 2. 为什么需要 Partition

如果一个 Topic 只有一条单线程 Log：

```text
producer
→ one ordered log
→ one consumer path
```

吞吐和并行消费受限。

分区后：

```text
P0 → Consumer A
P1 → Consumer B
P2 → Consumer C
```

可以并行处理。

代价：

> **全局顺序被拆成 Partition 内顺序。**

---

## 3. Key 决定局部顺序

如果业务要求同一 `order_id` 的 Event 顺序：

```text
key = order_id
```

让相同 Key 稳定路由到同一 Partition。

这样：

```text
order-1 created
order-1 paid
order-1 shipped
```

可以在同一 Partition 中按顺序处理。

不要为了“顺序”把整个 Topic 只做一个 Partition，除非真的需要全局单序列。

---

## 4. Consumer Group

传统 Consumer Group 可以理解：

> 同一个 Group 中，Partition 会分配给组内 Consumer，实现并行消费与 Failover。

例如：

```text
Topic: 4 partitions
Group A:
  consumer-1 → P0, P1
  consumer-2 → P2, P3
```

如果再加到 4 个 Consumer，可以进一步并行。

但如果 Consumer 数量超过传统 Group 的 Partition 数，多出来的 Consumer 没有 Partition 可消费。

这就是为什么：

> 扩 Consumer 之前先看 Partition 数。

---

## 5. 不同 Consumer Group

```text
Topic
├─ Group: analytics
├─ Group: billing
└─ Group: notification
```

每个 Group 都可以独立消费同一 Topic。

因此 Kafka 同时支持：

- 同组内 Load Balance；
- 不同组之间 Pub/Sub。

---

## 6. Offset

Consumer 需要知道：

```text
这个 Partition 消费到哪里了？
```

Offset 就是记录位置。

消费语义与 Offset Commit 的时机强相关。

### 先 Commit Offset，再处理

Crash：可能丢工作。

### 先处理，再 Commit Offset

Crash 在处理后 Commit 前：可能重复。

所以仍然回到：

```text
At-least-once
+ Idempotent Consumer
```

---

## 7. Rebalance

当 Consumer：

- 加入；
- 离开；
- Crash；
- Group Membership 变化

Partition 可能重新分配。

这段过程可能影响延迟和正在处理的任务。

因此长时间处理一条消息的 Consumer 需要特别注意：

- heartbeat；
- processing model；
- offset commit；
- ownership change。

不要把 30 分钟任务直接理解成“Consumer 拿一条消息同步处理 30 分钟就好”。

---

## 8. Backlog / Consumer Lag

生产速度：

```text
10000 msg/s
```

消费能力：

```text
8000 msg/s
```

Lag 每秒增长：

```text
2000
```

短时间峰值可以由 Buffer 吸收；长期差额意味着系统容量不足。

---

## 9. Backlog 排查

不能只说“加 Consumer”。

依次看：

```text
Producer traffic increased?
↓
Partition distribution balanced?
↓
Consumer count < partition count?
↓
Single message processing slower?
↓
Downstream DB / API slow?
↓
Retry / poison message?
↓
Rebalance too frequent?
```

---

## 10. Hot Partition

如果 Key 分布不均：

```text
90% events → same tenant_id
```

可能让一个 Partition 特别热。

增加 Consumer 无法把一个 Partition 同时交给多个传统 Consumer Group 成员处理。

需要重新考虑：

- partition key；
- hot tenant isolation；
- shard key；
- business ordering requirement。

---

## 11. Partition 数不是随便越多越好

增加 Partition 能增加并发，但也增加：

- metadata；
- file / replica management；
- rebalance cost；
- operational complexity。

真正设计要结合吞吐和 Broker 架构。

---

## 12. Ordering 与 Retry

消息失败后如果把它放回主队列尾部：

```text
A1 fail
A2 success
A3 success
A1 retry
```

同一 Key 的业务顺序可能被破坏。

需要根据业务选择：

- block partition；
- retry topic；
- per-key state machine；
- out-of-order tolerant processing。

没有统一答案。

---

## 13. Replay

Kafka Log 的一个重要优势是 Consumer 可以从历史 Offset 重新读取。

这适合：

- rebuild derived state；
- replay event processing；
- backfill；
- debugging。

但 Replay 旧 Event 仍可能触发副作用，所以 Handler 必须区分：

```text
recompute state
vs
external side effect
```

---

## 14. AI 场景：Embedding Pipeline

```text
document parsed
→ events partition by knowledge_base_id
→ embedding consumers
→ index writer
```

需要考虑：

- 同文档版本顺序；
- hot knowledge base；
- provider rate limit；
- backlog freshness lag；
- re-embedding replay。

所以 Kafka Lag 可能直接变成 RAG Freshness Lag。

---

## 15. 当前 Kafka 机制不要写死成旧版本

Apache Kafka 当前还在持续演进 Consumer 能力，例如官方设计中已经存在 Share Consumer / Share Group 等新模式。

因此课程只把传统 Consumer Group 的核心模型作为面试基础，不写成“Kafka 永远只有这一种消费模型”。

---

## 16. Metrics

```text
producer_rate
consumer_rate
consumer_lag
oldest_event_age
processing_latency
rebalance_count
partition_skew
retry_rate
```

AI 数据管道还要看：

```text
freshness_lag
embedding_qps
index_commit_latency
```

---

## 17. 🎯 面试怎么答

**问：Kafka Consumer Lag 很高怎么办？**

可以回答：

> 我先区分是流量突然增加还是消费能力下降。看 Producer Rate、各 Partition Lag、Consumer 数、单条处理耗时、下游 DB/API 延迟和 Rebalance。如果 Consumer 数还小于 Partition 数，可以扩 Consumer；如果是 Hot Partition，加 Consumer 没用，要调整 Partition Key；如果长期生产率大于消费率，还要扩 Partition/Consumer Capacity 或限流，而不是只等待 Queue 自己恢复。

---

## 18. ⚠️ 易错点

- Kafka Topic 有顺序 ≠ 全局顺序；
- Consumer 越多 ≠ 吞吐无限增加；
- Commit Offset ≠ Side Effect exactly-once；
- Lag 高 ≠ 一定 Broker 慢；
- Replay ≠ 可以安全重放所有外部副作用。

---

## 19. 本章自测

<details>
<summary>1. 为什么 Consumer 数超过 Partition 数后可能没有收益？</summary>

传统 Consumer Group 中一个 Partition 同一时刻通常分配给一个 Group Member，多出来的 Consumer 没有 Partition 可消费。

</details>

<details>
<summary>2. 为什么 Hot Partition 不能靠单纯加 Consumer 解决？</summary>

热点都集中在一个 Partition 时，该 Partition 的消费能力受单个 Partition Owner 限制，需要改变 Key/Partition Strategy 或业务顺序模型。

</details>

<details>
<summary>3. Kafka Replay 为什么对 External Side Effect 很危险？</summary>

重放历史 Event 可能再次触发邮件、扣款等副作用。需要幂等 Handler 或把重放限制在可重建 Derived State 的处理路径。

</details>
