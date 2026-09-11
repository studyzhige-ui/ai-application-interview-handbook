# 18. Re-embedding、Version、Incremental Update 与 Rebuild

Vector DB 最容易被低估的一件事是：

> **Embedding Model 和 Index 都会升级。**

一旦升级，旧向量不是自动兼容的新向量。

这一章解决：

```text
模型变了怎么办？
Chunk 变了怎么办？
Index 参数变了怎么办？
能不能不停机切换？
```

---

## 1. 哪些变化会触发生命周期问题

至少包括：

```text
Embedding Model 升级
Dimension 改变
Normalization Policy 改变
Metric 改变
Chunk Strategy 改变
Metadata Schema 改变
ANN Index Type / Parameter 改变
Document 大量更新
```

其中有些只是：

```text
rebuild index
```

有些必须：

```text
re-embedding entire corpus
```

---

# 2. Embedding Model 升级为什么通常要 Re-embedding

假设：

```text
Model v1 → 768 dim
Model v2 → 768 dim
```

即使维度一样：

```text
Embedding Space 也未必相同
```

所以不能安全假设：

```text
query 用 v2
文档还用 v1
```

能得到正确距离。

通常需要：

```text
Corpus
→ Model v2
→ New Vector Generation
```

再建立新索引。

---

# 3. Dimension 变化时更明显

如果：

```text
v1 = 768 dim
v2 = 1536 dim
```

旧新向量连数组长度都不同。

这时基本只能：

```text
new vector field / new collection / new index generation
```

不能直接混入同一个固定维度字段。

---

# 4. Blue-Green Index 思想

一种稳健升级方式：

```text
Current Index: generation_v1
        │
        ├─ 正常服务 Query
        │
Source of Truth
        ↓
Re-embed / Build
        ↓
New Index: generation_v2
        ↓
Validation
        ↓
Small Traffic / Shadow Test
        ↓
Switch Alias / Routing
        ↓
Keep v1 for rollback
        ↓
Retire v1
```

这和普通服务的 Blue-Green Deployment 思想很像。

---

# 5. 为什么不要“边重建边直接覆盖旧索引”

如果直接：

```text
old vector → replace with new vector
```

长时间重建过程中会出现：

```text
部分 v1
部分 v2
```

而 Query 使用哪一版模型？

如果没有版本隔离：

```text
语义空间混合
结果不可解释
回滚困难
```

所以 Generation / Version 是生命周期核心。

---

# 6. Incremental Update 怎么接住重建期间的新数据

假设全量 Re-embedding 需要 8 小时。

这 8 小时内业务仍在新增文档。

如果只做：

```text
T0 snapshot
→ build 8h
→ switch
```

会漏掉 T0 之后的新数据。

常见思路：

```text
1. 记录 Snapshot Boundary
2. Full Build 基于 Snapshot
3. 同时捕获 T0 之后 Change Log / CDC
4. Full Build 完成后 Replay Delta
5. Catch Up
6. Validate
7. Switch
```

这和搜索索引重建、数据库迁移非常相似。

---

# 7. Index 参数变化是否需要 Re-embedding

不一定。

如果只把：

```text
HNSW M=16 → M=32
```

原始向量没变。

可能只需要：

```text
rebuild ANN index
```

而不需要重新调用 Embedding Model。

所以必须区分：

```text
Vector Generation Lifecycle
vs
Index Structure Lifecycle
```

---

# 8. Chunk Strategy 变化为什么也会触发全量重建

假设：

```text
512-token fixed chunk
```

改成：

```text
semantic / parent-child chunk
```

原始检索单位已经变化。

那就必须：

```text
重新切 Chunk
→ 重新生成 IDs
→ 重新 Embedding
→ 重建 Index
```

所以 Vector Index Version 不只和模型版本有关。

---

# 9. 怎样验证新 Index

至少分两层。

## Infrastructure Layer

```text
ANN Recall vs Exact
Latency
QPS
Memory
Build Time
Filter Performance
```

## Retrieval / RAG Layer

```text
Relevant Document Recall
MRR / NDCG
Rerank
Answer Quality
Bad Case Regression
```

第二层 Primary 属于 RAG，但 Vector DB 升级不能完全脱离端到端验证。

---

# 10. Rollback 怎么做

如果新模型上线后：

```text
某类 Query Recall 暴跌
```

必须能：

```text
traffic → v1 index
```

快速回退。

所以不要提前删除：

```text
old index generation
old embedding config
```

直到新版本稳定。

---

# 11. 面试怎么答

## Q：Embedding 模型升级后 Vector DB 怎么迁移？

🎯 **建议回答**：

> 我不会把新旧模型向量直接混在同一个索引里，因为维度即使相同也不代表 embedding space 兼容。更稳妥的是建立新的 index generation：从 Source of Truth 做全量 re-embedding，同时记录 snapshot boundary，用 CDC / change log 补齐构建期间的增量；新索引完成后做 ANN 和 Retrieval 两层验证，再通过 alias / routing 灰度切流，保留旧 generation 一段时间用于 rollback。

---

# 12. 高频易错点

⚠️ **模型维度相同就不用 Re-embedding。** 错误。

⚠️ **改 HNSW 参数一定要重新调用 Embedding API。** 通常不需要，可能只需 Rebuild Index。

⚠️ **全量 Build 完成就可以切，不用处理期间新增数据。** 会产生 Missing Delta。

⚠️ **新 Index 验证只测 QPS。** 还必须验证 Recall 与端到端质量。

---

# 13. 本章自测

<details><summary>1. 为什么要区分 Vector Generation Version 和 Index Version？</summary>

Embedding / Chunk 改变会生成新的向量内容；HNSW/IVF 参数变化可能只改变索引结构。两者生命周期不同。
</details>

<details><summary>2. 全量 Re-embedding 很慢时怎样避免漏掉期间新增数据？</summary>

基于 Snapshot 做全量构建，同时捕获 snapshot 之后的增量 Change Log / CDC，完成后 replay delta 并追平再切换。
</details>