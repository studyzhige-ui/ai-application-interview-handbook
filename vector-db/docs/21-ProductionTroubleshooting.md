# 21. Production Troubleshooting：慢、占内存、召回掉了怎么办

学完前面所有机制后，应该能开始回答 Production 问题：

> **Vector DB 查询突然变慢，内存暴涨，或者 Recall 掉了，应该从哪里查？**

排查最重要的是分层，不要看到“召回差”就立刻调 HNSW 参数。

---

## 1. 先把问题分成五类

```text
A. Query Latency
B. Recall / Result Quality
C. Memory / Storage
D. Write / Update / Build
E. Distributed / Availability
```

不同问题对应不同证据。

---

# 2. Query Latency 变慢

建议按路径拆：

```text
Client
→ Router / Coordinator
→ Metadata Filter
→ ANN Search
→ Shard Fan-out
→ Merge
→ Payload Fetch
```

观察：

```text
P50 / P95 / P99
CPU
Memory Bandwidth
Disk / SSD
Network
Queueing
Shard Latency
Filter Time
```

常见原因：

```text
HNSW efSearch 拉高
IVF nprobe 拉高
Filter Selectivity 变差
Hot Shard
Compaction / Rebuild 抢资源
Segment 太多
Cache Miss
```

---

# 3. Recall 变差先不要只怪 ANN

做四层对照：

```text
1. Exact + No Filter
2. Exact + Filter
3. ANN + No Filter
4. ANN + Filter
```

如果：

```text
Exact + No Filter 就找不到
```

更可能是：

```text
Embedding
Content / Chunk
Metric
Query
```

如果：

```text
Exact 能找到
ANN 找不到
```

才重点看：

```text
HNSW efSearch
IVF nprobe
Index Quality
Quantization
```

如果：

```text
No Filter 能找到
加 Filter 找不到
```

重点看：

```text
Filter Logic
Permission
Version
Pre/Post Filter Strategy
```

---

# 4. Memory 暴涨

先分：

```text
Raw Vector
ANN Index
Metadata
Replica
Cache
Maintenance
```

常见原因：

```text
Vector Count 增长
Dimension 升级
HNSW M 增大
Replica 增加
Tombstone 未 Compaction
新旧 Index Generation 同时存在
Metadata 膨胀
```

尤其在 Blue-Green Rebuild 时：

```text
v1 + v2 同时在线
```

内存 / 存储可能接近翻倍。

---

# 5. Disk / Index Size 一直增长

数据量没明显增长，但索引一直变大：

检查：

```text
Deleted Ratio
Tombstone
Old Version
Compaction Queue
Unused Collection
Old Index Generation
Replica
```

不要只看业务“活跃文档数”。

---

# 6. Write / Upsert 越来越慢

可能原因：

```text
HNSW Graph 越来越大
Segment Sealing / Build
Compaction
Disk / WAL Pressure
Shard Hotspot
Metadata Index Update
```

如果同时 Query 也抖：

```text
后台 Build / Compaction
```

可能与前台争抢资源。

---

# 7. Filter Query 特别慢

先看：

```text
Filter 字段是否有适合的 Payload / Scalar Index
Filter Selectivity
Pre-filter / Post-filter Strategy
Candidate Expansion
Partition Routing
```

如果：

```text
无 Filter 5ms
加 tenant + ACL 100ms
```

ANN 本身可能不是瓶颈。

---

# 8. 某一个 Tenant 特别慢

常见：

```text
Hot Tenant
Large Tenant
Skewed Shard
High-selectivity ACL
```

检查：

```text
Tenant Vector Count
Tenant QPS
Shard Placement
Partition Size
Replica Load
```

可能需要：

```text
Dedicated Partition / Collection
Re-shard
Rate Limit
```

---

# 9. Rebuild 后 Recall 突然变化

优先检查：

```text
Embedding Model Version
Dimension
Normalization
Metric
Chunk Version
Index Parameters
Filter Schema
```

尤其要防：

```text
新 Query Model
+
旧 Document Embedding
```

或者：

```text
Cosine 模型
+
IP Index 未 Normalize
```

这种 Contract mismatch。

---

# 10. Distributed Query 偶发超时

常见 Tail Latency：

```text
99 个 Shard 很快
1 个 Shard 很慢
→ Global Query 等最慢节点
```

排查：

```text
per-shard latency
hot shard
network
rebalance
replica health
segment count
GC / memory pressure
```

Scatter-Gather 系统经常被最慢分片拖累。

---

# 11. 一张排查树

```text
Vector Search Bad Case
│
├─ Quality Bad
│  ├─ Exact bad → Model / Chunk / Metric
│  ├─ ANN bad → Index / Parameter
│  └─ Filter bad → Filter / Version / ACL
│
├─ Latency Bad
│  ├─ Search work ↑
│  ├─ Filter ↑
│  ├─ Fan-out / Hot Shard
│  └─ Maintenance interference
│
├─ Memory Bad
│  ├─ Dimension / N
│  ├─ Graph / Replica
│  └─ Tombstone / dual generation
│
└─ Write Bad
   ├─ Index maintenance
   ├─ Compaction
   └─ skew / resource saturation
```

---

# 12. 面试怎么答

## Q：Vector DB Recall 下降怎么排查？

🎯 **建议回答**：

> 我会先把 Embedding/Retrieval 问题和 ANN 问题拆开，用 Exact Search 做基线。先跑 Exact+NoFilter，如果这一步已经找不到，优先查 embedding、metric、chunk 和 query；再比较 ANN+NoFilter 判断 index recall；最后比较有无 metadata filter，判断是不是权限、版本或 filter-aware search 导致。这样不会一上来盲调 efSearch。

## Q：Vector DB P99 突然变差怎么排查？

> 我会拆成 coordinator、filter、ANN、shard、merge 几段，并看 per-shard P99、CPU、memory、network、compaction/rebuild 和 segment 数。分布式 ANN 常见是 hot shard 或 background maintenance 把 tail latency 拉高。

---

# 13. 高频易错点

⚠️ **Recall 差就把 efSearch 拉高。** 可能根本是模型 / Filter 问题。

⚠️ **Memory 涨只因为向量数量涨。** Index / Replica / Tombstone / 双 generation 都可能造成。

⚠️ **Query P50 好就不用查 Shard。** P99 可能被单个慢 Shard 拖住。

---

# 14. 本章自测

<details><summary>1. 为什么 Exact Search 是排查 ANN Recall 的关键工具？</summary>

它能告诉你“向量空间里真正最近邻是否存在”。如果 Exact 都找不到，就不应该先责怪 ANN。
</details>

<details><summary>2. 为什么 Blue-Green Rebuild 期间容量可能突然接近翻倍？</summary>

因为旧 generation 继续服务，新 generation 同时构建和加载，两套向量 / 索引可能暂时共存。
</details>