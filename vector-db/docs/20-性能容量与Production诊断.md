# 20. Performance、Capacity 与 Production Diagnosis

Vector DB 到 Production 后，不能再用一句：

> “查询很快。”

来描述性能。

真正需要同时回答：

```text
Recall 够不够？
P95 / P99 多高？
并发上来后 QPS 与尾延迟怎么变化？
Memory / Storage 需要多少？
Index Build 多久？
Update / Delete 成本多大？
Filter 会不会把 ANN 拖慢？
Recall 突然掉了怎么定位？
某个 Shard 为什么特别慢？
```

因此“容量规划”和“Production Troubleshooting”应该放在同一知识块里：

> **先建立指标模型，再用同一套指标做故障定位。**

---

## 1. Vector DB 的性能不是单指标

至少同时关注：

```text
Quality
├── ANN Recall vs Exact
└── Filter 后有效候选质量

Latency
├── P50
├── P95
└── P99

Throughput
└── QPS / concurrent queries

Resource
├── Memory
├── Storage
├── CPU / GPU
└── Network

Lifecycle
├── Build Time
├── Insert / Upsert TPS
├── Delete / Compaction
└── Rebuild Cost
```

如果只说“我们 5ms”，信息是不完整的。

---

## 2. Recall：先分清 Index Recall 和业务 Recall

Vector DB 层常用 Exact Search 做 Ground Truth：

```text
Exact Top-K
vs
ANN Top-K
```

例如 Exact Top10 中，ANN 找回 9 个：

```text
ANN Recall@10 = 0.9
```

这回答的是：

> ANN Index 相对 Exact Nearest Neighbor 丢了多少。

它不等于 RAG 的业务 Retrieval Recall，因为上层还受：

- Embedding；
- Chunk；
- Query Rewrite；
- Hybrid Retrieval；
- Rerank；
- Permission / Filter；

影响。

所以故障排查时必须先分层。

---

## 3. Latency 不要只看 Average

至少看：

```text
P50
P95
P99
```

一次分布式 Vector Query 可能经过：

```text
Client
→ Router / Coordinator
→ Metadata Filter
→ ANN Search
→ Shard Fan-out
→ Result Merge
→ Payload Fetch
```

Average 很好，不代表 Tail Latency 好。

一个 Hot Shard、Compaction、Network Spike 或高选择性 Filter 都可能把 P99 拉高。

---

## 4. QPS 和 Latency 必须一起看

单请求 5ms 并不代表：

```text
1000 QPS 下仍然 5ms
```

并发升高后会出现：

- CPU Saturation；
- Memory Bandwidth；
- Queueing；
- Network Saturation；
- Hot Shard；
- Cache Thrash。

更有意义的 Benchmark 是：

```text
QPS
→ P95 / P99 Latency Curve
→ Recall
```

也就是说：

> 吞吐、延迟和质量要一起测。

---

## 5. Memory 怎么估

最基础 Raw Vector：

```text
N × D × bytes_per_element
```

例如：

```text
100M × 1536 × 4 bytes
≈ 614 GB
```

但 Production Memory 还要加：

```text
ANN Index
HNSW Graph Links
Metadata / Scalar Index
ID / Allocator
Cache
Replica
Old + New Generation during rebuild
Headroom
```

所以：

> `N × D × 4` 只是下界，不是最终容量。

---

## 6. HNSW 为什么要单独算 Graph Overhead

HNSW 每个节点还需要保存邻居关系。

粗略可以想：

```text
N × average_degree × neighbor_id_size
```

还没包含：

- 多层结构；
- allocator；
- metadata；
- node header。

这也是 HNSW “用 Memory 换 Query Performance”的真实成本。

---

## 7. Build Cost 为什么是一等指标

一个 Index 可能需要数小时甚至更久构建。

要关注：

```text
Build Throughput
CPU / GPU
Memory Peak
Temporary Storage
Network
```

如果系统每天都必须 Rebuild，而一次构建就需要 12 小时，说明：

```text
Index / Lifecycle Design
```

本身已经不适合业务节奏。

---

## 8. Dynamic Workload 还要测 Update Cost

如果数据每天：

```text
+20% insert
-10% delete
```

只测静态查询没有意义。

还要测：

```text
Insert TPS
Upsert TPS
Delete Latency
Compaction Debt
Index Maintenance
Query During Write
```

Index Selection 必须考虑读写比例，而不只是查询最快值。

---

## 9. Filter Cost 为什么经常被低估

同一个 ANN Index：

```text
No Filter P95 = 10ms
```

加入：

```text
tenant_id
permission_group
version
```

可能变成：

```text
P95 = 40ms
```

原因可能包括：

- Filter Evaluation；
- Scalar Index 缺失；
- Candidate 被大量过滤；
- ANN 需要扩大 Search Work；
- Partition Routing 不佳。

所以 Benchmark 必须使用真实 Filter Distribution。

---

## 10. 一份容量规划输入清单

至少收集：

```text
Vector Count N
Dimension D
Element Type
Metadata Size
Index Type / Parameters
Replica Count
Expected Growth
QPS / Concurrency
Filter Distribution
Recall Target
P99 SLA
Update TPS
Delete Rate
Rebuild Frequency
```

先做理论估算，再用真实 Benchmark 修正。

---

# 11. Troubleshooting：先分类，不要先调参数

Production 问题可以先分成：

```text
A. Query Latency
B. Recall / Result Quality
C. Memory / Storage
D. Write / Build / Maintenance
E. Distributed / Availability
```

不同问题要收不同证据。

---

## 12. Query Latency 突然变慢怎么查

按执行链拆：

```text
Client
→ Coordinator
→ Filter
→ ANN
→ Shard
→ Merge
→ Payload
```

同时观察：

```text
P50 / P95 / P99
CPU
Memory
Disk / SSD
Network
Queue
per-shard latency
filter time
compaction / rebuild activity
```

常见原因：

- `efSearch` / `nprobe` 提高；
- Filter Selectivity 改变；
- Hot Shard；
- Segment 太多；
- Compaction / Rebuild 抢资源；
- Cache Miss；
- Network Tail。

---

## 13. Recall 下降的四层对照法

不要看到 Recall 下降就直接调 HNSW。

做：

```text
1. Exact + No Filter
2. Exact + Filter
3. ANN + No Filter
4. ANN + Filter
```

### Exact + No Filter 都找不到

优先检查：

```text
Embedding
Content / Chunk
Metric
Normalization
Query
```

### Exact 能找到，ANN 找不到

重点检查：

```text
Index Quality
efSearch / nprobe
Quantization
Build Parameter
```

### No Filter 找得到，加 Filter 找不到

重点检查：

```text
Filter Logic
Tenant / ACL
Version
Pre/Post Filter Strategy
```

这套对照可以把“模型问题”“索引问题”“权限/过滤问题”分开。

---

## 14. Memory 暴涨怎么查

先拆来源：

```text
Raw Vector
ANN Index
Metadata
Replica
Cache
Tombstone
Dual Generation
Maintenance Buffer
```

常见原因：

```text
N 增长
Dimension 变化
HNSW M 增大
Replica 增加
Tombstone 未清理
Blue-Green v1/v2 同时存在
Metadata 膨胀
```

尤其新旧 Index Generation 共存期间，容量可能短期接近翻倍。

---

## 15. Index Size 一直涨但业务数据没涨

检查：

```text
Deleted Ratio
Tombstone
Old Version
Compaction Queue
Small Segment
Unused Collection
Old Generation
Replica Count
```

业务“活跃文档数”不等于物理 Index Size。

---

## 16. Write / Upsert 越来越慢

可能是：

```text
HNSW Graph 越来越大
Segment Seal / Build
Compaction
WAL / Disk Pressure
Hot Shard
Metadata Index Update
```

如果 Query P99 也同时抖动，应重点检查后台 Maintenance 是否和前台抢资源。

---

## 17. 某个 Tenant 特别慢

常见：

```text
Hot Tenant
Large Tenant
Skewed Shard
Complex ACL
High-selectivity Filter
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

- Dedicated Partition / Collection；
- Re-shard；
- Rate Limit；
- 更合理 Tenant Routing。

---

## 18. Rebuild 后 Recall 突变

优先比对 Contract：

```text
Embedding Model Version
Dimension
Normalization
Metric
Chunk Version
Index Parameters
Filter Schema
```

典型事故包括：

```text
new Query Embedding + old Document Embedding
```

或：

```text
Cosine-trained Model + wrong IP/L2 setup
```

这不是单纯“ANN 参数不好”。

---

## 19. Distributed Query 偶发超时

Scatter-Gather 查询可能出现：

```text
99 个 Shard 很快
1 个 Shard 很慢
→ Global Query 等最慢 Shard
```

所以要看：

```text
per-shard P99
hot shard
network
rebalance
replica health
segment count
memory pressure
```

Tail Latency 常常由最慢分片决定。

---

## 20. 一张 Production 排查树

```text
Vector Search Incident
│
├─ Quality Bad
│  ├─ Exact bad → Model / Chunk / Metric
│  ├─ ANN bad → Index / Parameter
│  └─ Filter bad → ACL / Version / Filter Strategy
│
├─ Latency Bad
│  ├─ Search Work ↑
│  ├─ Filter Cost ↑
│  ├─ Fan-out / Hot Shard
│  └─ Maintenance Interference
│
├─ Memory Bad
│  ├─ N / D ↑
│  ├─ Graph / Replica ↑
│  └─ Tombstone / Dual Generation
│
└─ Write Bad
   ├─ Index Maintenance
   ├─ Compaction
   └─ Resource Saturation
```

---

## 21. 常见错误

- QPS 越高就代表系统越快：错，要同时看 Latency / Recall。
- Raw Vector Size 就是内存需求：严重低估。
- Benchmark 只测 Query：动态系统还要测 Build / Update / Delete。
- P50 好就说明用户体验稳定：P99 可能很差。
- Recall 差就拉高 `efSearch`：可能根本是 Embedding / Filter / Version 问题。
- Memory 涨只因为向量数量涨：Index / Replica / Tombstone / Dual Generation 都可能。

---

## 22. 面试怎么答

### Q：Vector DB 选型和压测看哪些指标？

> 我会先用 Exact Search 建 ANN Ground Truth，测 Recall；再测不同并发下的 P50/P95/P99、QPS、Memory、Index Size、Build Time、Update/Delete Cost。业务有 Tenant/Permission Filter 时必须用真实 Filter 压测。容量上先用 N×D×element size 估 Raw Vector，再加 Index、Metadata、Replica 和 Headroom。

### Q：Vector DB Recall 下降怎么排查？

> 先用 Exact+NoFilter 判断向量空间本身是否能找到，再比较 ANN+NoFilter 判断索引 Recall，最后比较有无 Filter 判断 ACL/Version/Filter Strategy。这样能避免一上来盲调 HNSW 参数。

### Q：P99 突然变差怎么查？

> 我会拆 Coordinator、Filter、ANN、Shard、Merge 等阶段，看 per-shard Tail Latency、CPU/Memory/Network、后台 Compaction/Rebuild 和 Segment 数，分布式检索常被 Hot Shard 或 Maintenance 拉高尾延迟。

---

## 23. 自测

<details><summary>1. 为什么 Recall、Latency、QPS 必须一起看？</summary>
因为增加搜索工作量可能提高 Recall 但降低吞吐、增加延迟，单独优化一个指标会隐藏代价。
</details>

<details><summary>2. 为什么容量不能只算 N×D×bytes？</summary>
因为还要加入 ANN Index、Graph、Metadata、Replica、Allocator、Cache、旧新 Generation 与运行 Headroom。
</details>

<details><summary>3. 为什么 Exact Search 是 Recall 故障定位的第一步？</summary>
它能区分“向量空间/模型本身就找不到”和“ANN 索引把本来能找到的近邻丢了”。
</details>
