# 12｜Vector Index Lifecycle：写入、删除、Tombstone、Compaction、Re-embedding 与 Rebuild

Vector DB 在 Demo 里往往只有：

```text
insert
query
```

Production 一定会遇到：

```text
文档更新
Chunk 重切
Embedding Model 升级
权限撤销
删除数据
ANN 参数调整
索引重建
```

所以真正完整的问题是：

> **一个向量从写入，到更新、删除、Compaction，再到全量 Rebuild，整个生命周期怎样管理？**

---

## 1. Insert 不只是 Append

Flat Index 中新增向量相对直接。

但 ANN Index 可能还要：

```text
HNSW → 找邻居、建立图边
IVF  → 找最近 Centroid、进入 List
PQ   → 生成 Quantized Code
```

因此写入吞吐会直接受 Index Type 影响。

---

## 2. Upsert / Update 为什么比关系字段复杂

一个 Vector 从：

```text
v_old
```

变成：

```text
v_new
```

意味着它在向量空间中的位置改变。

于是：

```text
HNSW 邻接关系可能改变
IVF Cell 可能改变
Quantized Code 可能改变
```

所以 Vector Update 常常更接近：

```text
remove old index entry
+
insert new index entry
```

而不是简单原地改一个数组字段。

---

## 3. Metadata Update 和 Vector Update 要区分

如果只修改：

```text
permission_group
status
category
```

向量内容可能没变。

如果产品支持 Metadata-only Update，就不必重新 Embedding。

但如果：

```text
Chunk Content Changed
```

通常需要：

```text
re-chunk
→ re-embed
→ update vector
```

所以更新流程应该先判断：

```text
Content Changed?
Metadata Only?
Embedding Contract Changed?
```

---

## 4. Delete 为什么常用 Tombstone

ANN Index 维护成本较高。

如果每次删除都立即重写复杂图或分区结构，前台成本会很大。

因此常见思路是：

```text
Delete Request
→ logical delete / tombstone
→ Query path 跳过
→ background compaction / rebuild
```

这样：

```text
前台删除快
```

但代价是：

```text
旧记录仍暂时占空间
索引里可能残留无效节点
```

---

## 5. Tombstone 不能无限积累

假设：

```text
1 亿条记录
3000 万条已 deleted
```

即使查询不返回它们，也可能带来：

- Memory / Storage 浪费；
- Graph / Segment 碎片；
- 维护债务；
- Query Path 变长；
- Rebuild 成本累积。

因此需要 Maintenance。

---

## 6. Compaction 在做什么

可以把 Compaction 理解成：

```text
整理有效数据
→ 去掉 Tombstone / Stale Version
→ 合并小 Segment
→ 回收空间
→ 生成更干净的索引结构
```

具体实现随产品变化，但目标类似：

> **把在线增删改造成的碎片重新整理。**

---

## 7. Segment 为什么重要

很多 Vector DB 会把数据组织为多个 Segment，而不是一个无限大的单索引文件：

```text
Growing Segment
→ Seal
→ Build Index
→ Merge / Compact
```

这种模型能把在线写入与只读/优化查询结构分离。

但是 Segment 太碎会造成：

```text
更多 Fan-out
更多 Metadata
更多 Maintenance
更高 Tail Latency
```

---

## 8. Compaction 为什么会影响前台 SLA

Compaction / Rebuild 需要：

```text
CPU
Memory
Disk / SSD I/O
Network
Index Build Resource
```

太激进：

```text
Query P99 抖动
Write Latency 上升
```

太保守：

```text
Storage 膨胀
Tombstone 堆积
Segment 碎片
```

所以它是 Background Maintenance Trade-off。

---

## 9. Index Maintenance 不只是 Compaction

Production 还可能包括：

```text
Index Rebuild
Replica Repair
Rebalance
Segment Merge
Index Warmup
Cache Warmup
Statistics Refresh
```

这些长任务应该具备：

- 可观测；
- 可限速；
- 可取消/重试；
- 有进度；
- 不拖垮前台 Query。

---

## 10. 为什么 Embedding Model 升级通常要 Re-embedding

即使：

```text
Model v1 = 768 dim
Model v2 = 768 dim
```

也不代表两个向量空间兼容。

所以常见升级路径是：

```text
Source of Truth
→ Embedding Model v2
→ New Vector Generation
→ New Index Generation
```

而不是：

```text
Query 用 v2
Document 还用 v1
```

---

## 11. Vector Version 与 Index Version 要分开

如果改变：

```text
Embedding Model
Dimension
Normalization
Chunk Strategy
```

通常会改变 Vector Content，本质需要新的 Vector Generation。

如果只是：

```text
HNSW M=16 → 32
IVF nlist 改变
```

Vector 本身没变，可能只需 Rebuild ANN Index。

所以至少区分：

```text
Vector Generation Version
vs
Index Structure Version
```

---

## 12. Chunk Strategy 变化为什么也会触发 Rebuild

如果从：

```text
fixed 512-token chunk
```

切到：

```text
semantic / parent-child chunk
```

检索单位本身变了。

需要：

```text
re-chunk
→ new IDs
→ re-embed
→ rebuild index
```

因此 Vector Lifecycle 与 RAG Chunk Lifecycle 是有关联的，但 Primary 责任不同。

---

## 13. Blue-Green Index

更稳健的升级方式：

```text
Current generation v1
        │
        ├─ 继续正常服务
        │
Source of Truth
        ↓
Build generation v2
        ↓
Validation
        ↓
Shadow / Canary
        ↓
Switch Alias / Routing
        ↓
Keep v1 for rollback
        ↓
Retire old generation
```

好处：

- 不把新旧 Vector 混进一个 Index；
- 更容易验证；
- 更容易 Rollback；
- 切换边界清晰。

代价：

```text
短期双份存储 / 内存
```

---

## 14. 全量 Rebuild 期间的新数据怎么办

假设 Build 需要 8 小时。

如果只做：

```text
T0 snapshot
→ build 8h
→ switch
```

T0 之后的新写入会丢失。

常见思路：

```text
1. 记录 Snapshot Boundary
2. Full Build from Snapshot
3. 同时记录 Change Log / CDC
4. Build 完成后 Replay Delta
5. Catch Up
6. Validate
7. Switch
```

这和搜索索引、数据库迁移的思想非常接近。

---

## 15. Delete / Update 必须有 Source Mapping

一个文档可能对应很多 Chunk：

```text
doc_1001
├── chunk_0
├── chunk_1
└── ...
```

如果 Vector DB 只保存随机 Vector ID，就很难：

- 全量删除某文档；
- 查找当前版本；
- 回滚；
- 重建；
- 清理旧 Generation。

因此 Metadata 应保留：

```text
doc_id
chunk_id
content_version
embedding_version
index_generation
updated_at
```

---

## 16. Upsert 不自动解决并发一致性

多个 Worker 同时更新同一文档：

```text
A writes version 7
B writes version 8
```

如果 B 先完成、A 后到：

```text
旧版本可能覆盖新版本
```

所以还需要：

```text
version check
job generation
idempotency
source-of-truth state
```

这些属于 Vector Lifecycle 与 Backend Reliability 的交界。

---

## 17. Delete 成功后为什么仍可能搜到旧数据

可能原因：

- Replica Lag；
- Cache 没失效；
- Query 还在旧 Generation；
- Version Filter 缺失；
- 异步删除尚未传播；
- Logical Delete 与 Physical Reclaim 不同阶段。

所以：

> `DELETE API 200` 不等于全链路已经不可见。

---

## 18. 怎样验证一个新 Index Generation

### Infrastructure Layer

```text
ANN Recall vs Exact
Latency
QPS
Memory
Build Time
Filter Performance
```

### Retrieval / RAG Layer

```text
Relevant Document Recall
MRR / NDCG
Rerank Quality
Answer Quality
Bad Case Regression
```

第二层 Primary 属于 RAG，但 Vector DB 升级不能脱离端到端验收。

---

## 19. Maintenance 需要监控什么

可以关注：

```text
Deleted Ratio
Tombstone Count
Old Generation Count
Segment Count
Small Segment Count
Compaction Queue
Index Build Queue
Disk Amplification
Memory Growth
Query Latency Drift
```

数据量没明显增加，但 Index Size / P99 一直涨时，Maintenance Debt 是重要排查方向。

---

## 20. 常见错误

- Upsert 一定是原地修改 ANN Index：不一定。
- Delete 后空间会立即释放：不一定。
- 相同 Dimension 的新模型不需要 Re-embedding：错误。
- 改 HNSW 参数一定要重新 Embedding：通常不需要。
- Full Build 完成就直接切，不需要追增量：会漏 Delta。
- Logical Delete 和 Physical Reclaim 是同一时刻：错误。

---

## 21. 面试怎么答

### Q：Embedding 模型升级后怎么迁移 Vector DB？

> 我会建立新 Vector / Index Generation，而不是把新旧模型向量混在一起。基于 Source of Truth 做全量 Re-embedding，同时记录 Snapshot Boundary 和增量 Change Log，完成后追平 Delta，再做 ANN 与端到端 Retrieval 验证，通过 Alias/Route 灰度切换，并保留旧 Generation 供 Rollback。

### Q：Vector DB Delete 为什么还需要 Compaction？

> 很多 ANN Index 会先做 Logical Delete/Tombstone，让记录立即不可见，再由后台 Compaction/Rebuild 真正回收空间并整理索引结构。这样降低前台 Delete 成本，但必须控制 Tombstone/Segment Debt。

---

## 22. 自测

<details><summary>1. 为什么 Vector Update 通常比 Metadata Update 更重？</summary>
因为 Vector 位置改变会影响 ANN Index 结构，而 Metadata-only Update 不一定需要重建近邻关系。
</details>

<details><summary>2. 为什么要区分 Vector Generation 和 Index Version？</summary>
Embedding/Chunk 改变会改变向量本身；HNSW/IVF 参数变化可能只改变索引结构，两种迁移成本不同。
</details>

<details><summary>3. 为什么全量 Rebuild 要有 Delta Replay？</summary>
因为 Build 期间业务仍会新增/修改数据，不追增量会让新 Generation 缺数据。
</details>
