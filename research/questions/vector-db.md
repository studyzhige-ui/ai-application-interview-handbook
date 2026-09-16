# Vector DB Canonical Questions — S001–S279 全库纵向扫描 v3

更新日期：2026-09-10

> 一级板块：**Vector DB**。本文件只保留向量存储与 ANN 基础设施：Similarity、Exact vs ANN、HNSW / IVF、Index / Product Selection、Schema / Metadata、Index Lifecycle。Dense/Sparse、Hybrid、RRF、Rerank、Top-K、Retrieval Evaluation 等属于 **RAG Retrieval Pipeline**；Embedding / Rerank Model 原理属于 **LLM Foundation**。
>
> 本文件所有 ACTIVE 条目的 `Primary Module = Vector DB`。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**12**
- MOVED：**11**
- 证据范围：仅 `S001–S279`
- 当前版本：`v3`（Global Merge / Split Audit）

### 高频信号

- `VDB-009` · 18：Vector Storage / Product / Architecture Selection
- `VDB-005` · 11：HNSW 原理
- `VDB-004` · 10：Vector Index 选型
- `VDB-007` · 10：HNSW vs IVF
- `VDB-020` · 8：Index Lifecycle / Rebuild / Incremental Update

---

## 2. ACTIVE Canonical Questions

### VDB-002 · Cosine Similarity、Dot Product / Inner Product、L2 Distance 有什么区别？归一化怎样影响结果？
- **Topic**：Similarity Metrics
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**6**
- **Evidence Sources**：`S062`, `S178`, `S184`, `S199`, `S210`, `S217`
- **Related Modules**：LLM Foundation（应用工程深度）, RAG

### VDB-003 · 为什么大规模向量检索不能总做暴力 Exact Search？ANN 牺牲什么、换来什么？
- **Topic**：Exact Search vs ANN
- **Question Type**：Why / Trade-off
- **Depth**：L2
- **Source Count**：**4**
- **Evidence Sources**：`S054`, `S180`, `S211`, `S258`

### VDB-004 · Vector Index 怎样根据数据规模、更新频率、Recall、Latency、Memory 与 QPS 选择？
- **Topic**：Index Selection
- **Question Type**：Trade-off / System Design
- **Depth**：L4
- **Source Count**：**10**
- **Evidence Sources**：`S022`, `S054`, `S101`, `S125`, `S136`, `S180`, `S211`, `S251`, `S258`, `S277`

### VDB-005 · HNSW 的基本图搜索机制是什么？为什么能在高维空间做近似最近邻搜索？
- **Topic**：HNSW
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Source Count**：**11**
- **Evidence Sources**：`S054`, `S101`, `S125`, `S136`, `S180`, `S184`, `S211`, `S224`, `S251`, `S258`, `S277`

### VDB-006 · IVF / IVF_FLAT 的基本思想是什么？Cluster / List 划分与候选范围怎样影响 Recall 和 Latency？
- **Topic**：IVF
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Source Count**：**5**
- **Evidence Sources**：`S037`, `S054`, `S211`, `S224`, `S251`

### VDB-007 · HNSW 与 IVF 怎样比较？Recall、Latency、Memory、Build Cost、Update Pattern 如何权衡？
- **Topic**：HNSW vs IVF
- **Question Type**：Comparison / Trade-off
- **Depth**：L3
- **Source Count**：**10**
- **Evidence Sources**：`S037`, `S054`, `S101`, `S136`, `S180`, `S211`, `S224`, `S251`, `S258`, `S277`

### VDB-008 · Metadata Filter / Partition / Tenant Filter 怎样与向量索引结合？Pre-filter / Post-filter 有什么边界？
- **Topic**：Metadata Filtering
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S037`, `S064`, `S101`, `S136`, `S206`, `S275`
- **Related Modules**：RAG

### VDB-009 · 为什么需要独立 Vector DB？Milvus、FAISS、pgvector、Elasticsearch Vector 等方案在 Library、DB Extension、Search Engine、专用 Vector DB 之间怎样选？
- **Topic**：Vector Storage / Product / Architecture Selection
- **Question Type**：Comparison / System Design / Project
- **Depth**：L4
- **Source Count**：**20**
- **Evidence Sources**：`S004`, `S022`, `S054`, `S064`, `S095`, `S101`, `S109`, `S113`, `S121`, `S125`, `S136`, `S184`, `S211`, `S212`, `S249`, `S251`, `S255`, `S267`, `S275`, `S277`

### VDB-011 · Vector Database 的 Collection / Partition / Schema / Primary Key / Metadata 应怎样建模？
- **Topic**：Vector Data Modeling
- **Question Type**：System Design
- **Depth**：L3
- **Source Count**：**3**
- **Evidence Sources**：`S064`, `S101`, `S206`

### VDB-018 · Vector Dimension、Normalization、Distance Metric 与 Index 参数怎样影响存储、内存和检索成本？
- **Topic**：Vector / Index Parameters
- **Question Type**：Trade-off
- **Depth**：L3
- **Source Count**：**3**
- **Evidence Sources**：`S095`, `S199`, `S211`
- **Related Modules**：LLM Foundation（应用工程深度）

### VDB-020 · Embedding / Index 版本升级后怎样处理 Re-embedding、Index Rebuild、Incremental Update 与旧向量兼容？
- **Topic**：Index Lifecycle / Freshness
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S068`, `S095`, `S101`, `S109`, `S140`, `S217`, `S221`, `S246`, `S277`
- **Related Modules**：RAG, LLM Foundation（应用工程深度）

### VDB-022 · Graph Database 与 Vector Database 的数据模型、查询能力和适用场景有什么差异？
- **Topic**：Graph DB vs Vector DB
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Source Count**：**7**
- **Evidence Sources**：`S037`, `S058`, `S072`, `S211`, `S246`, `S267`, `S272`
- **Related Modules**：RAG

---

## 3. MOVED：十板块 / Global Audit 归属修正

| Legacy QID | 原问题 | 新 Primary Canonical |
|---|---|---|
| `VDB-001` | Embedding 语义 / Model Selection | `LLM-018` |
| `VDB-010` | Milvus / FAISS / pgvector / ES Vector 产品选型 | **MERGED → `VDB-009`**；二者共享同一个“向量存储架构 / 产品边界”知识模型 |
| `VDB-012` | Dense vs Sparse | `RAG-012` |
| `VDB-013` | Hybrid Retrieval | `RAG-013` |
| `VDB-014` | BM25 | `RAG-012` / `RAG-013` 的 Keyword Retrieval 子主题 |
| `VDB-015` | RRF / Fusion | `RAG-014` |
| `VDB-016` | Rerank | `RAG-015`；Model 原理另见 `LLM-019` |
| `VDB-017` | Retrieval / Rerank Top-K | `RAG-016` |
| `VDB-019` | Retrieval Evaluation | `RAG-020`, `RAG-021` |
| `VDB-021` | Multimodal Retrieval | `RAG-005`；模型对齐另见 `LLM-010` |
| `VDB-023` | Codebase Retrieval Boundary | `RAG-030`, `AGENT-037`；Global Audit 后 `RAG-030` 再并入 `AGENT-037` |

---

## 4. Global Merge / Split Audit 结论

`VDB-009` 与旧 `VDB-010` 在核心知识模型、真实问法和证据来源上高度重叠：都在问“为什么需要某类 Vector Storage，以及 FAISS / pgvector / Milvus / ES Vector 如何按规模、能力和工程边界选型”。两者共有 `S022`, `S101`, `S136`, `S211`, `S212`，继续分成两题会虚增产品选型频率，因此合并并对证据取唯一并集，共 **18** 个独立 HUMAN-A。

这次归属修正后的核心原则仍是：**Vector DB 负责“怎么高效存和找向量”；RAG 负责“检索系统怎样设计并证明有效”。**
