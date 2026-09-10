# 20. CDC / Data Sync：把 MySQL 变化同步到下游

前一章解决“数据放到哪个 Shard”。这一章解决另一类生产问题：

> **MySQL 里的业务事实发生变化后，Search、Analytics、Cache、Vector Index 等下游怎样知道？**

如果每个业务写请求都手工：

```text
写 MySQL
→ 写 Elasticsearch
→ 写 Redis
→ 发 MQ
→ 更新 Analytics
```

很快就会出现大量 Dual-write Failure Window。

CDC 提供另一条思路：

```text
MySQL Commit
→ Binlog
→ Change Data Capture
→ 下游消费
```

---

## 1. CDC 是什么

CDC = Change Data Capture。

它关心：

> **数据库里哪些数据发生了新增、修改、删除，并把这些变化变成可消费的事件。**

对于 MySQL，最常见基础就是：

```text
Binary Log
```

因为 Binlog 已经记录了数据库变化。

---

# 2. 为什么 CDC 比应用层 Dual Write 更自然

假设：

```text
UPDATE documents SET status='READY'
```

应用层 Dual Write：

```text
1. MySQL UPDATE 成功
2. Search Index 更新失败
```

或者：

```text
1. Search 更新成功
2. MySQL ROLLBACK
```

两个系统开始不一致。

CDC 方式：

```text
先让 MySQL 成为 Source of Truth
      ↓
事务成功后进入 Binlog
      ↓
下游异步消费变化
```

它把：

```text
业务写入正确性
```

和：

```text
下游同步
```

解耦了。

---

# 3. 一个典型链路

```text
Application
   │
   ▼
 MySQL
   │
   ▼
 Binlog
   │
   ▼
 CDC Connector
   │
   ├──▶ Kafka
   ├──▶ Elasticsearch
   ├──▶ Analytics
   └──▶ Vector Index Pipeline
```

常见工具 / 思路包括：

- Canal；
- Debezium；
- 自研 Binlog Consumer；
- 云数据库提供的 CDC Service。

教材重点不是背 API，而是理解数据一致性语义。

---

# 4. CDC Event 至少需要什么

一个变化事件通常会包含或关联：

```text
Table
Primary Key
Operation Type
Before / After Value
Transaction / Position
Timestamp
```

例如：

```json
{
  "table": "documents",
  "op": "UPDATE",
  "id": 123,
  "before": {"status": "PROCESSING"},
  "after": {"status": "READY"}
}
```

真实格式取决于工具，但核心问题类似：

> 下游能否知道“什么变了”以及“这个变化在什么顺序里发生”。

---

# 5. CDC 最大误区：有 Event 就 Exactly-once

现实中更常见的是：

```text
At-least-once Delivery
```

也就是说某个 Event 可能重复到达。

比如：

```text
Consumer 已更新 Search
但还没提交 Offset 就 Crash
重启后重新消费
```

同一 Event 再来一次。

所以 Consumer 必须考虑：

```text
Idempotency
```

---

# 6. Idempotent Consumer

假设事件带：

```text
record_id=123
version=42
```

下游可以做到：

```text
只有 event.version > current.version
才应用
```

或者以：

```text
Primary Key + Event Position
```

作为去重基础。

核心思想：

> **重复事件不能把下游状态弄坏。**

这和 Backend Engineering 的 Idempotency 是同一类思想。

---

# 7. 顺序问题

假设同一行发生：

```text
v1 PENDING
→ v2 RUNNING
→ v3 SUCCESS
```

如果下游乱序应用：

```text
先 v3 SUCCESS
后 v2 RUNNING
```

最终状态倒退。

所以 CDC 设计要问：

```text
顺序保证到什么粒度？
全局顺序？
单表顺序？
单 Primary Key 顺序？
同 Partition 顺序？
```

很多系统不需要全局总顺序，只需要：

> **同一业务 Key 的变化顺序正确。**

---

# 8. Transaction Boundary

一个 MySQL Transaction 可能修改多行：

```text
UPDATE A
INSERT B
UPDATE C
COMMIT
```

下游是否必须把它们看成一个原子 Unit？

这取决于业务。

例如 Analytics 可能接受逐条最终一致。

但某些 Materialized View 可能要求：

```text
同一事务的一组变化一起应用
```

所以 CDC 不只是“读 Binlog”，还要定义：

```text
Transaction Semantics
```

---

# 9. Schema Change 怎么办

今天事件是：

```json
{"id":1,"status":"RUNNING"}
```

明天表新增：

```text
priority
```

Consumer 如果写死旧 Schema，可能失败。

因此 CDC Pipeline 要处理：

```text
Schema Evolution
Backward Compatibility
New Column Default
DDL Event
Consumer Rollout
```

这也是为什么 Data Pipeline 需要版本化，不是简单脚本。

---

# 10. Bootstrap：第一次全量数据从哪里来

CDC 天然擅长：

```text
增量变化
```

但如果 Search Index 是新建的，它还没有历史数据。

通常需要：

```text
Full Snapshot / Backfill
        ↓
记录 Binlog Position / GTID
        ↓
切换到 Incremental CDC
```

难点是：

> 全量扫描期间数据库还在继续写。

所以必须保证：

```text
Snapshot
+
Incremental Catch-up
```

没有 Gap。

---

# 11. CDC Lag

下游同步不是瞬时的。

你需要观察：

```text
Source Commit Time
→ CDC Read Time
→ Queue Time
→ Consumer Apply Time
```

如果 Lag 持续增长：

```text
Producer Rate > Consumer Capacity
```

就需要：

- 扩 Consumer；
- 优化 Batch；
- 调整 Partition；
- 降低下游写成本；
- Backpressure / Rate Limit。

---

# 12. CDC 与 MQ 的关系

CDC 不一定等于 MQ。

```text
CDC
→ 捕获变化

MQ
→ 传输 / 缓冲事件
```

常见组合：

```text
MySQL Binlog
→ CDC Connector
→ Kafka
→ Many Consumers
```

这样 Kafka 提供：

- Buffer；
- Replay；
- Consumer Group；
- 多下游解耦。

但如果需求很简单，也可能 CDC 直接写目标系统。

---

# 13. CDC 与 Outbox Pattern 区别

CDC 捕获：

```text
数据库 Row Change
```

Outbox Pattern 则是应用在同一个本地事务中显式写：

```text
业务表
+
outbox_events
```

然后：

```text
Outbox Publisher
→ MQ
```

Outbox 的优势是事件语义由业务明确表达：

```text
AgentRunCompleted
CreditsCharged
```

而不是让下游从“某几列变化”猜业务事件。

两者甚至可以结合：

```text
写 Outbox
→ CDC 订阅 Outbox Table
→ Kafka
```

---

# 14. AI Application 场景：知识库索引同步

流程：

```text
Document Metadata 写 MySQL
        ↓
Transaction COMMIT
        ↓
CDC Event
        ↓
Ingestion Worker
        ↓
Parse / Chunk / Embedding
        ↓
Vector DB
```

这里要注意：

> MySQL Row 更新成功不代表 Vector Index 已经 READY。

因此业务状态应明确：

```text
UPLOADED
PROCESSING
READY
FAILED
```

用户查询时只使用：

```text
READY
```

的数据。

这比假装“跨系统瞬时一致”更诚实。

---

# 15. 删除怎么同步

删除尤其容易漏。

如果 MySQL：

```sql
DELETE FROM documents WHERE id=123;
```

Vector DB / Search 里也要删除对应内容。

CDC Event 必须携带足够 Key，让下游能执行：

```text
Delete by document_id
```

如果你采用 Soft Delete，则消费者要理解：

```text
deleted_at changed
→ downstream logical delete
```

---

# 16. Replay 与 Recovery

一个成熟 Pipeline 要能回答：

```text
Consumer 挂一天怎么办？
Search Index 被误删怎么办？
需要重新构建怎么办？
```

理想能力：

```text
从某个 Position / Offset Replay
```

或者：

```text
Full Rebuild + Incremental Catch-up
```

所以 Event Retention 和 Checkpoint 很关键。

---

# 17. 面试怎么答

## Q：CDC 是什么？

🎯 推荐回答：

> CDC 是 Change Data Capture，用于捕获数据库已经提交的数据变化并同步给下游。MySQL 常以 Binlog 作为变化来源，再通过 Canal、Debezium 或其它 Connector 传到 MQ、Search、Analytics 等系统。真正难点不只是读取 Binlog，而是重复消费、顺序、Schema Evolution、全量加增量切换、Lag、Replay 和下游幂等。

## Q：为什么不用应用代码直接同时写 MySQL 和 Elasticsearch？

> 直接 Dual Write 存在 Failure Window：一边成功另一边失败。更常见做法是先让 MySQL 成为 Source of Truth，事务提交后通过 Binlog CDC 异步更新下游，接受并显式管理最终一致性。

---

# 18. 高频易错点

⚠️ **CDC 天然 Exactly-once。**  
通常仍要按重复事件设计。

⚠️ **有 CDC 就不需要 Idempotency。**  
错误。

⚠️ **Binlog 顺序 = 所有业务场景需要全局顺序。**  
多数场景只需要定义关键粒度的顺序。

⚠️ **只做增量 CDC 就能创建新索引。**  
还需要 Bootstrap / Snapshot。

⚠️ **MySQL 已提交 = 下游已经更新。**  
CDC 通常是最终一致。

---

# 19. 本章自测

<details>
<summary>1. CDC 为什么能减少 Dual Write 问题？</summary>

因为业务先只保证 MySQL 本地事务正确提交，然后从 Binlog 这个已提交变化源异步驱动下游，不要求应用请求同时原子写多个独立系统。

</details>

<details>
<summary>2. 为什么 CDC Consumer 必须幂等？</summary>

Consumer 可能在 Apply 成功但 Offset 尚未提交时崩溃，重启后重复消费同一事件；如果操作不幂等，下游会被重复更新或污染。

</details>

<details>
<summary>3. 新建 Elasticsearch / Vector Index 时为什么不能只从当前 Binlog 开始？</summary>

因为历史数据不会自动重新产生变化事件。需要先 Full Snapshot / Backfill 历史数据，并记录一致的 Binlog Position / GTID，再继续消费后续增量。

</details>

---

## 继续学习

下一章讨论另一个写入侧问题：

> **一次要导入千万 / 亿级数据时，怎样让 MySQL 写得快又不把系统拖死？**

下一章：**Bulk Write 与 MySQL Write Path。**
