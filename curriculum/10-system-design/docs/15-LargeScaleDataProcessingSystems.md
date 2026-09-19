# 15｜Large-scale Data & Processing：10TB Storage、Migration、Dedup、Large-file

这一章训练另一类非常容易“Demo 化”的问题：

> **数据量一大，原来一次性读完、单事务写完、同步处理完的方案为什么会崩？怎样做分阶段、可恢复、可限速的数据处理系统？**

对应真人 Scenario：

```text
SD-006 10TB/day Storage + Time-range Query
SD-007 Large Batch / Migration
SD-008 Massive Whitelist / Dedup
SD-012 Large-file / Long-video Processing
SD-015 Resource-constrained Secure Compute
```

---

## 1. 第一原则：不要把整个数据集当一个任务

如果有：

```text
2000 万 rows
1TB PDF
100GB video
```

错误：

```text
one request
→ load all
→ process all
→ one commit
```

正确方向：

```text
Partition / Chunk
→ Durable Task
→ Checkpoint
→ Bounded Batch
→ Progress
→ Retry / Resume
```

---

# 2. 10TB/day Storage 先拆 Hot / Warm / Cold

假设：

```text
10TB/day
retention 1 year
```

全部放昂贵在线数据库通常不现实。

可以按访问模式：

```text
Hot: recent hours/days
Warm: recent weeks
Cold: object storage / archive
```

再问：

```text
查询时间范围？
聚合还是原始明细？
是否必须秒级？
```

存储层应该由 Query Pattern 驱动。

---

# 3. Time Partition 与 Retention

时序/日志类数据常天然按：

```text
date / hour
```

分区。

优势：

```text
range pruning
TTL / drop partition
cold migration
batch compaction
```

但当前时间分区可能是写热点，所以还可能需要：

```text
hash + time
```

的二级拆分。

---

# 4. Index 不能无限加

10TB/day 如果每个字段都建索引：

```text
write amplification
storage explosion
compaction cost
```

会非常高。

应该从 Query Pattern 选择：

```text
time
user / device / tenant
status
```

真正必要的索引。

冷数据甚至可以接受更高 Query Latency。

---

# 5. Batch Migration 为什么不能 OFFSET 翻到天荒地老

大表：

```text
OFFSET 10000000 LIMIT 1000
```

会越来越慢。

更常用：

```text
WHERE id > last_id
ORDER BY id
LIMIT batch
```

即 Keyset / Seek 思路。

还要记录：

```text
checkpoint / last_id
```

支持 Resume。

---

# 6. Batch Size 是 Trade-off

Batch 太小：

```text
round trip 多
commit 多
throughput 低
```

Batch 太大：

```text
memory 高
transaction 长
lock / log 压力大
retry 粒度大
```

所以 Batch Size 必须压测。

---

# 7. 数据迁移必须考虑 Source 在继续写

Snapshot 迁移期间：

```text
old DB still receiving writes
```

所以常见：

```text
Snapshot Copy
→ CDC / Delta Catch-up
→ Validate
→ Cutover
```

否则复制完时数据已经过期。

---

# 8. Validation：迁完不代表正确

至少：

```text
row count
checksum / sample hash
business aggregate
missing / extra keys
referential check
```

对于 TB 级数据不能逐条人工比较，需要分区对账。

---

# 9. Massive Set / Whitelist 的核心是 Memory Model

例如 10 亿 IP / ID：

先估：

```text
exact set memory
```

再判断：

```text
必须精确 membership？
允许 false positive？
需要 enumerate？
```

如果允许 False Positive：

```text
Bloom Filter
```

可以极大节省内存。

但 Bloom Filter：

```text
false positive possible
false negative normally no
```

不能拿来直接代替所有精确授权数据。

---

# 10. Dedup：Exact、Approximate、Time-window

去重也要问语义：

```text
全历史绝对去重？
24h 内去重？
近似重复？
内容相似？
```

不同需求对应：

```text
unique key
set / hash
Bloom
content hash
similarity
```

不要一看到“去重”就回答 Bloom Filter。

---

# 11. Large-file Upload：Data Plane 不应该绕 API Server

大文件如果：

```text
Client → API Server → Object Storage
```

API Server 会承担巨大 Bandwidth。

更常见：

```text
Client
→ request upload session
→ signed URL / multipart upload
→ Object Storage direct upload
→ finalize metadata
```

API 负责 Control Plane，不一定搬所有字节。

---

# 12. Multipart / Resume

大文件拆：

```text
part 1
part 2
...
```

每个 Part 有：

```text
part_number
checksum
status
```

失败只重传部分。

完成后：

```text
Complete Multipart
→ durable object
→ enqueue processing
```

---

# 13. 长视频 / PDF 处理状态机

```text
UPLOADED
→ VALIDATED
→ PARSING / TRANSCODING
→ EXTRACTING
→ INDEXING
→ COMPLETED
```

每个 Stage：

```text
bounded concurrency
checkpoint
retry policy
progress
```

用户查询 Job，而不是保持 HTTP 连接几小时。

---

# 14. Resource-constrained Compute

如果 SGX EPC / GPU Memory 等资源有限：

```text
Task admission
→ scheduler
→ resource reservation
→ execution
→ release
```

多租户要防：

```text
one tenant exhausts scarce memory
```

所以需要：

```text
quota
fair scheduling
isolation
backpressure
```

`SD-015` 虽然是单点真人信号，但它很好地验证了“容量估算 + 多租户隔离 + 调度”这条通用能力。

---

# 15. Failure Walkthrough

## Migration Worker 崩溃

→ 从 Checkpoint Resume，不从头重跑。

## Batch 重试

→ Upsert / Idempotent Transform，避免重复写。

## Upload 某 Part 丢失

→ 只重传该 Part。

## Processing 失败

→ durable status + retry / failed state。

## Source 继续更新

→ Delta Catch-up / CDC。

---

# 16. 🎯 面试怎么答

> 大规模数据问题我先把 Dataset 拆成 Partition / Chunk 和 Durable Job，不会一次性载入或一个大事务处理。Migration 用 Keyset Batch + Checkpoint，并考虑 Snapshot 期间的 Delta Catch-up；Storage 根据 Hot/Warm/Cold 和真实 Query Pattern 分层；大文件让 Object Storage 承担 Data Plane，用 Multipart + Resume，再把后处理异步化。所有流程都必须有限速、幂等、进度、对账和失败恢复。

---

# 17. 本章自测

<details><summary>1. 为什么 Migration 只做 Snapshot Copy 可能漏数据？</summary>
因为复制期间 Source 仍可能有新写入，需要 CDC / Delta Catch-up 或停写窗口才能收敛。
</details>

<details><summary>2. 为什么大文件最好直传 Object Storage？</summary>
避免应用服务器成为高带宽 Data Plane，降低内存、网络和连接压力。
</details>

<details><summary>3. Bloom Filter 为什么不适合直接做精确权限白名单的唯一真相？</summary>
因为它允许 False Positive，可能把不在集合中的元素判断为存在，权限场景可能造成越权风险。
</details>
