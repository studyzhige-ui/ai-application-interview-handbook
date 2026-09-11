# Vector Database｜AI 应用开发秋招系统手册

> Vector DB 是这套 Handbook 的第 6 个正式一级模块。
>
> 目标不是从某个数据库 SDK 开始，而是从 0 建立：**Vector Space → Similarity → Exact Search → ANN → HNSW / IVF / Quantization → Data Model / Filter → Index Lifecycle → Distributed / Production → Product Boundary**。
>
> **Granularity Audit：✅ 已完成。** 原 23 章按知识闭环收敛为 **16 个正式知识小板块**；当前 `docs/` 已重新连续编号为 `01–16`，文件编号与正式学习顺序一致。
>
> **Content Depth Audit：✅ 通过。** 已对 16 个正文文件做全量结构扫描，并人工复核 ANN 谱系、IVF、PQ、Schema、Metadata Filter、Tenant Isolation、Distributed Vector DB 等相对较短章节；它们虽比 HNSW / Lifecycle / Production Diagnosis 更短，但已经各自形成“机制 → Trade-off / Failure → Production 边界 → 面试 → 自测”的独立闭环，不为追求字数机械扩写。

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

所以把 Normalization、HNSW 参数、Compaction 等子机制重新并回它们所属的知识块，而不是一机制一文件。

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

## 4. 23 → 16 的结构调整

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

这些主题共享同一个“为什么 → 机制 → Failure → Trade-off → 验证”闭环。

IVF、PQ、Metadata Filter、Tenant Isolation、Distributed Vector DB 等仍独立，因为它们有不同机制和 Failure Model。

---

## 5. 正式 16 个知识小板块

1. [Vector DB 在 AI Application 中负责什么](docs/01-VectorDB在AI应用中的职责.md)
2. [Vector Space & Similarity：Dimension、Normalization、Cosine / Dot / L2](docs/02-VectorSpace与Similarity.md)
3. [Exact Search vs ANN：Top-K Ground Truth 与 Recall / Latency](docs/03-ExactSearch与ANN.md)
4. [ANN Index 谱系：Graph、Partition、Quantization](docs/04-ANN索引谱系.md)
5. [HNSW：机制、M、efConstruction、efSearch 与调优](docs/05-HNSW机制与调优.md)
6. [IVF：Coarse Quantizer、nlist 与 nprobe](docs/06-IVF原理.md)
7. [Quantization：SQ / PQ 与压缩检索](docs/07-Quantization与PQ.md)
8. [HNSW vs IVF 与 Index Selection](docs/08-IndexSelection.md)
9. [Collection / Schema / Primary Key / Metadata](docs/09-Vector数据建模.md)
10. [Metadata Filter、Pre-filter 与 Post-filter](docs/10-MetadataFilter.md)
11. [Partition / Namespace / Tenant Isolation](docs/11-Partition与TenantIsolation.md)
12. [Vector Index Lifecycle：写入、删除、Compaction、Re-embedding 与 Rebuild](docs/12-VectorIndex生命周期.md)
13. [Shard / Replica / Segment：分布式 Vector DB](docs/13-分布式VectorDB.md)
14. [Performance、Capacity 与 Production Diagnosis](docs/14-性能容量与Production诊断.md)
15. [FAISS / pgvector / Elasticsearch / Milvus / Qdrant 架构选型](docs/15-产品与架构选型.md)
16. [Graph DB vs Vector DB 与系统位置](docs/16-GraphDB边界与系统设计.md)

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

按 `docs/01 → 16` 连续学习，重点理解下一章为什么自然出现。

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
