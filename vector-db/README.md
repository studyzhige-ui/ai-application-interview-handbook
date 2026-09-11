# Vector Database｜AI 应用开发秋招系统手册

> Vector DB 是这套 Handbook 的第 6 个正式一级模块。
>
> 目标不是从 Milvus / pgvector API 开始，而是从 0 建立一条完整因果链：**为什么语义信息能变成向量 → 向量怎样比较 → Exact Search 为什么会变贵 → ANN 用什么换什么 → HNSW / IVF / Quantization 怎样工作 → Vector DB 怎样组织、过滤、更新和扩展 → 最后才讨论产品选型。**

## 1. 最重要的课程原则

本模块继续固定遵守：

> **知识体系演进顺序优先，真实面经只用于调整复习权重、补充真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

冻结 `S001–S279` HUMAN-A 中，HNSW、Index Selection、HNSW vs IVF、产品选型都是明显市场信号，但课程不会第一章就问：

> “HNSW 的 `M` 和 `efSearch` 怎么调？”

因为必须先知道：

```text
Vector 是什么
→ Dimension 是什么
→ Similarity / Distance 在比较什么
→ Top-K Nearest Neighbor 是什么
→ Exact Search 为什么贵
→ ANN 为什么允许近似
→ 才能理解 HNSW / IVF 参数到底在调什么
```

所以面经决定某些章节要讲到 L3 / L4，却不决定教材顺序。

---

## 2. Vector DB 在整套体系中的边界

本模块只负责：

```text
Vector Storage
Similarity / Distance
Exact vs ANN
ANN Index
HNSW / IVF / Quantization
Schema / Metadata
Filter + ANN
Write / Update / Delete
Index Lifecycle
Shard / Replica / Segment
Recall / Latency / Memory / QPS
Vector Storage Product Selection
```

明确不把这些知识模型抢过来：

| 问题 | Primary Module |
|---|---|
| Embedding Model 为什么能表示语义、怎样训练 / 选模型 | LLM Foundation |
| Dense vs Sparse / BM25 | RAG |
| Hybrid Retrieval / RRF / Fusion | RAG |
| Reranker / Cross-Encoder Pipeline | RAG；模型原理在 LLM Foundation |
| Retrieval Top-K Strategy | RAG |
| Recall@K / MRR / NDCG / Retrieval Evaluation | RAG |
| 文档 Chunk / Query Rewrite / Grounding | RAG |
| 多租户 AI 系统怎样组合 MySQL / Redis / Vector DB | System Design |

一句话：

> **Vector DB 负责“怎样高效、可维护地存和找向量”；RAG 负责“整个检索系统怎样设计并证明有效”。**

---

## 3. 真人面经只校准重点

冻结研究中 Vector DB 当前有 **12 道 Primary Canonical**。

高价值信号包括：

| Topic | HUMAN-A Sources | 深度 |
|---|---:|---:|
| Vector Storage / Product / Architecture Selection | 20 | L4 |
| HNSW | 11 | L3 |
| Vector Index Selection | 10 | L4 |
| HNSW vs IVF | 10 | L3 |
| Index Lifecycle / Rebuild / Incremental Update | 9 | L4 |
| Graph DB vs Vector DB | 7 | L4 |
| Similarity Metrics | 6 | L2 |
| Metadata Filtering | 6 | L4 |
| IVF | 5 | L3 |
| Exact Search vs ANN | 4 | L2 |
| Vector / Index Parameters | 3 | L3 |
| Vector Data Modeling | 3 | L3 |

> **Interview Heat ≠ Knowledge Importance。** ANN 索引谱系、PQ / Quantization、Delete / Tombstone / Compaction、Shard / Replica 等即使当前直接面经不高，也属于理解 Vector DB Production 行为的必要知识，必须保留。

---

## 4. 事实与版本口径

本模块优先讲跨产品稳定的算法与数据库概念，再用产品实现做映射，不把某个 SDK 或版本 API 当成知识体系。

推荐权威资料入口：

- FAISS：<https://github.com/facebookresearch/faiss>
- pgvector：<https://github.com/pgvector/pgvector>
- Milvus Docs：<https://milvus.io/docs>
- Qdrant Docs：<https://qdrant.tech/documentation/>
- Elasticsearch Vector Search：<https://www.elastic.co/guide/en/elasticsearch/reference/current/dense-vector.html>
- HNSW Paper：<https://arxiv.org/abs/1603.09320>
- Product Quantization Paper：<https://ieeexplore.ieee.org/document/5432202>

涉及产品能力时优先写“当前实现示例”，而不是把产品特性讲成 Vector DB 的普遍定律。

---

## 5. 五条主线

### 主线 A｜从 Vector 到 Nearest Neighbor

```text
Vector Representation
→ Dimension / Normalization
→ Cosine / Dot / L2
→ Top-K Nearest Neighbor
→ Exact Search
→ Scale Cost
→ ANN
```

### 主线 B｜ANN Index

```text
ANN Taxonomy
→ Graph-based
→ HNSW
→ Partition-based
→ IVF
→ Compression / Quantization
→ PQ / SQ
→ HNSW vs IVF
→ Index Selection
```

### 主线 C｜Vector Database Data Model

```text
Collection / Table
→ Primary Key
→ Vector Field
→ Metadata
→ Partition / Namespace
→ Metadata Filter
→ Pre-filter / Post-filter
→ Tenant Isolation
```

### 主线 D｜Lifecycle 与 Production

```text
Insert / Upsert
→ Update / Delete
→ Tombstone / Compaction
→ Incremental Index
→ Re-embedding
→ Version / Rebuild
→ Shard / Replica
→ Recall / Latency / Memory / QPS
→ Troubleshooting
```

### 主线 E｜架构与产品边界

```text
Library
vs
Relational Extension
vs
Search Engine
vs
Dedicated Vector DB
→ Graph DB Boundary
→ Vector DB in AI System
```

---

## 6. 完整 23 章

### Part A｜从向量到最近邻

1. [Vector DB 在 AI Application 中负责什么](docs/01-VectorDB在AI应用中的职责.md)
2. [Vector、Embedding Storage Semantics 与 Dimension](docs/02-Vector与Dimension.md)
3. [Normalization 与向量空间直觉](docs/03-Normalization与向量空间.md)
4. [Cosine / Dot Product / L2](docs/04-Similarity与Distance.md)
5. [Top-K Nearest Neighbor 与 Exact Search](docs/05-TopK与ExactSearch.md)
6. [为什么需要 ANN：Recall 换 Latency](docs/06-为什么需要ANN.md)

### Part B｜ANN Index：从思想到参数

7. [ANN Index 谱系：Graph、Partition、Quantization](docs/07-ANN索引谱系.md)
8. [HNSW：分层小世界图](docs/08-HNSW原理.md)
9. [HNSW 参数：M / efConstruction / efSearch](docs/09-HNSW参数与调优.md)
10. [IVF：Coarse Quantizer、nlist 与 nprobe](docs/10-IVF原理.md)
11. [Quantization：SQ / PQ 与压缩检索](docs/11-Quantization与PQ.md)
12. [HNSW vs IVF 与 Index Selection](docs/12-IndexSelection.md)

### Part C｜Vector DB 怎样组织数据

13. [Collection / Schema / Primary Key / Metadata](docs/13-Vector数据建模.md)
14. [Metadata Filter、Pre-filter 与 Post-filter](docs/14-MetadataFilter.md)
15. [Partition / Namespace / Tenant Isolation](docs/15-Partition与TenantIsolation.md)

### Part D｜写入、更新与生命周期

16. [Insert / Upsert / Update / Delete](docs/16-写入更新与删除.md)
17. [Tombstone、Compaction 与 Index Maintenance](docs/17-Compaction与索引维护.md)
18. [Re-embedding、Version、Incremental Update 与 Rebuild](docs/18-Embedding与Index生命周期.md)
19. [Shard / Replica / Segment：分布式 Vector DB 基础](docs/19-分布式VectorDB.md)
20. [Recall / Latency / Memory / QPS / Build Cost](docs/20-性能指标与容量规划.md)
21. [Production Troubleshooting：慢、占内存、召回掉了怎么办](docs/21-ProductionTroubleshooting.md)

### Part E｜产品与系统边界

22. [FAISS / pgvector / Elasticsearch Vector / Milvus / Qdrant 怎样选](docs/22-产品与架构选型.md)
23. [Graph DB vs Vector DB，以及 Vector DB 在 AI 系统中的位置](docs/23-GraphDB边界与系统设计.md)

---

## 7. 为什么加入了面经之外的章节

### Quantization / PQ

如果只会 HNSW / IVF，你仍然很难回答：

> 10 亿条、1536 维 float32 向量为什么内存这么大？怎样压缩？压缩会损失什么？

它是“规模上来后怎么办”的自然下一步。

### Delete / Tombstone / Compaction

真实系统不是一次性建完索引永不修改。知识删除、权限撤销、文档更新都要求理解：

```text
Logical Delete
→ Index 中旧节点怎样处理
→ Compaction / Rebuild
→ Query 期间怎样避免返回旧版本
```

### Shard / Replica

产品选型不能只比较 API。到了 Production，必须知道：

```text
数据怎么拆
查询怎么 fan-out
副本解决什么
Filter 与 Partition 怎样影响路由
```

因此这些属于知识骨架，不因当前面经低频而删除。

---

## 8. 推荐三遍学习法

### 第一遍：严格按 01 → 23

先形成因果链，不追求一次背参数。

尤其不要直接跳到：

```text
M = ?
efSearch = ?
nprobe = ?
```

参数只有放回算法机制里才有意义。

### 第二遍：自己推演

重点能够画出：

- Exact Search 扫描路径；
- HNSW 多层图；
- IVF coarse partition；
- Pre-filter vs Post-filter；
- Re-embedding / Blue-Green Index；
- Shard / Replica Query Flow。

### 第三遍：面试化

进入：

- `review/`
- `interview/高频面试题.md`
- `interview/面试易错点.md`
- `interview/面试前速查表.md`

正确顺序仍然是：

```text
理解机制
→ 能解释 Trade-off
→ 能分析 Failure
→ 再练 30 秒表达
```

---

## 9. 每章统一写法

```text
先讲人话
→ 准确定义
→ 数学 / 小例子
→ 数据结构 / 执行路径
→ 为什么
→ Trade-off
→ Failure / Scale
→ AI 场景
→ 🎯 面试怎么答
→ ⚠️ 易错点
→ 🔍 继续追问
→ 折叠自测
```

数学只讲到支撑应用工程判断所需的深度，不把本模块扩成高维几何或统计学习理论课。

---

## 10. 下一环

Vector DB 完成后进入：

> **LLM Foundation（应用工程深度） → RAG → Agent Harness / Runtime**

这时会把 Vector DB 提供的“向量基础设施”真正接入：

```text
Embedding Model
→ Corpus / Chunk
→ Vector Store / ANN
→ Retrieval Strategy
→ Rerank
→ Context
→ LLM / Agent
```

其中“怎么检索、怎么评估检索”属于 RAG；Vector DB 主体到这里先把存储与 ANN Infrastructure 讲清楚。