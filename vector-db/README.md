# Vector Database｜AI 应用开发秋招系统手册

> Vector DB 是这套 Handbook 的第 6 个正式一级模块。
>
> 目标不是从某个数据库 SDK 开始，而是从 0 建立：**Vector Space → Similarity → Exact Search → ANN → HNSW / IVF / Quantization → Data Model / Filter → Index Lifecycle → Distributed / Production → Product Boundary**。

> **Granularity Audit：✅ 已完成。** 原 23 章内容经过知识闭环审计后收敛为 **16 个正式知识小板块**。教材文件减少不改变 Vector DB 的 12 道 Canonical、HUMAN-A Source Count 或与 RAG / LLM Foundation 的 Primary Boundary。

---

## 1. 课程原则

> **知识依赖决定学习顺序；真人面经只决定讲多深、哪些 Failure / Trade-off 必须覆盖。**

因此课程不会从 HNSW 参数开始，而必须先理解：

```text
Vector / Dimension
→ Normalization / Metric
→ Top-K Exact Search
→ Scale Cost
→ ANN
→ ANN Index
→ Production Lifecycle
```

另一个正式原则是：

> **Canonical / Capability 可以很细，但一个 Markdown 文件必须形成完整认知闭环。**

所以这次把“Normalization”“HNSW 参数”“Compaction”等子机制重新并回它们所属的知识块。

---

## 2. 模块边界

Vector DB 负责：

```text
Vector Storage
Similarity / Distance
Exact vs ANN
ANN Index
HNSW / IVF / Quantization
Schema / Metadata / Filter
Write / Delete / Compaction / Rebuild
Shard / Replica
Recall / Latency / Memory / QPS
Vector Storage Product Selection
```

明确不重复：

| 问题 | Primary Module |
|---|---|
| Embedding Model 原理 / 选型 | LLM Foundation |
| Dense vs Sparse / BM25 | RAG |
| Hybrid / RRF / Fusion | RAG |
| Rerank / Retrieval Top-K | RAG |
| Retrieval Evaluation | RAG |
| Chunk / Query Rewrite / Grounding | RAG |
| MySQL / Redis / Vector DB 整体组合 | System Design |

一句话：

> **Vector DB 解决“怎样高效、可靠、可维护地存和找向量”；RAG 解决“整个 Retrieval System 怎样设计并证明有效”。**

---

## 3. 真人面经只校准重点

冻结研究中 Vector DB 有 **12 道 Primary Canonical**。高价值信号包括：

- Vector Storage / Architecture Selection；
- HNSW；
- Index Selection；
- HNSW vs IVF；
- Index Lifecycle / Rebuild / Incremental Update；
- Graph DB vs Vector DB；
- Similarity Metric；
- Metadata Filter；
- IVF；
- Exact vs ANN；
- Index Parameter；
- Vector Data Modeling。

Quantization、Tombstone/Compaction、Shard/Replica 等即使面经直接频率更低，仍属于 Production 知识骨架。

---

## 4. 这次 23 → 16 合并了什么

```text
Vector + Dimension
+ Normalization
+ Cosine / Dot / L2
→ Vector Space & Similarity

Top-K Exact Search
+ Why ANN
→ Exact Search vs ANN

HNSW Principle
+ M / efConstruction / efSearch
→ HNSW Mechanism & Tuning

Insert / Upsert / Delete
+ Tombstone / Compaction
+ Re-embedding / Version / Rebuild
→ Vector Index Lifecycle

Performance / Capacity
+ Production Troubleshooting
→ Performance, Capacity & Diagnosis
```

这些合并后的主题共享同一个“为什么 → 机制 → Failure → Trade-off → 验证”闭环。

IVF、PQ、Metadata Filter、Tenant Isolation、Distributed Vector DB 等仍保留独立文件，因为它们有自己不同的机制和 Failure Model。

> 为避免纯编号重构造成大量成熟正文无意义改写，本轮保留合并后最早的历史文件编号。正式学习顺序以本 README 为准；文件数量已经物理收敛为 16。

---

## 5. 正式 16 个知识小板块

1. [Vector DB 在 AI Application 中负责什么](docs/01-VectorDB在AI应用中的职责.md)
2. [Vector Space & Similarity：Dimension、Normalization、Cosine / Dot / L2](docs/02-VectorSpace与Similarity.md)
3. [Exact Search vs ANN：Top-K Ground Truth 与 Recall / Latency](docs/05-ExactSearch与ANN.md)
4. [ANN Index 谱系：Graph、Partition、Quantization](docs/07-ANN索引谱系.md)
5. [HNSW：机制、M、efConstruction、efSearch 与调优](docs/08-HNSW机制与调优.md)
6. [IVF：Coarse Quantizer、nlist 与 nprobe](docs/10-IVF原理.md)
7. [Quantization：SQ / PQ 与压缩检索](docs/11-Quantization与PQ.md)
8. [HNSW vs IVF 与 Index Selection](docs/12-IndexSelection.md)
9. [Collection / Schema / Primary Key / Metadata](docs/13-Vector数据建模.md)
10. [Metadata Filter、Pre-filter 与 Post-filter](docs/14-MetadataFilter.md)
11. [Partition / Namespace / Tenant Isolation](docs/15-Partition与TenantIsolation.md)
12. [Vector Index Lifecycle：写入、删除、Compaction、Re-embedding 与 Rebuild](docs/16-VectorIndex生命周期.md)
13. [Shard / Replica / Segment：分布式 Vector DB](docs/19-分布式VectorDB.md)
14. [Performance、Capacity 与 Production Diagnosis](docs/20-性能容量与Production诊断.md)
15. [FAISS / pgvector / Elasticsearch / Milvus / Qdrant 架构选型](docs/22-产品与架构选型.md)
16. [Graph DB vs Vector DB 与系统位置](docs/23-GraphDB边界与系统设计.md)

---

## 6. 五条主线

### A｜Vector Space

```text
Vector / Dimension
→ Normalization
→ Similarity Metric
→ Exact Top-K
→ ANN Trade-off
```

### B｜ANN Index

```text
ANN Taxonomy
→ HNSW
→ IVF
→ Quantization
→ Index Selection
```

### C｜Data Model / Filter

```text
Collection / Schema
→ Metadata
→ Filter
→ Partition / Tenant
```

### D｜Lifecycle / Production

```text
Insert / Update / Delete
→ Tombstone / Compaction
→ Re-embedding / Rebuild
→ Distributed Shard / Replica
→ Capacity / Troubleshooting
```

### E｜Architecture Boundary

```text
Library
vs Relational Extension
vs Search Engine
vs Dedicated Vector DB
→ Graph DB Boundary
```

---

## 7. 推荐学习方式

### 第一遍

按上面的 **16-block 顺序**学习，不按文件编号大小猜顺序。

### 第二遍

进入 [`review/README.md`](review/README.md)，从空白纸画：

```text
Vector
→ Exact
→ ANN
→ HNSW / IVF
→ Filter
→ Lifecycle
→ Distributed / Production
```

### 第三遍

使用：

- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

目标不是背“Milvus API”，而是能回答：

> **为什么需要近似检索、索引如何工作、什么时候会坏、怎样验证 Recall/Latency、数据更新后怎样维护、最后为什么选择某种架构。**
