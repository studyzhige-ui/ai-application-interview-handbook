# Vector Database Canonical Questions — S001–S279 全库纵向扫描 v1

更新日期：2026-09-10

> 本文件只记录冻结 HUMAN-A 面经中能够直接回溯的 Vector DB / Retrieval 核心问题。它不是向量数据库教材目录；Embedding、ANN、索引参数、存储生命周期等未被高频直接问到的基础仍由完整知识体系补齐。

## 1. 当前扫描结论

- Canonical Questions：**23** 道
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数；同一来源里的连续追问不重复加权
- 当前版本：`v1`；RAG / Agent 完成后做跨模块二次审计

### 高频信号

- **VDB-013** · 24 个来源 · 🔥🔥🔥：为什么要做 Dense + Sparse / BM25 Hybrid Retrieval？两路召回怎样融合？
- **VDB-016** · 20 个来源 · 🔥🔥🔥：为什么 Retrieval 后还需要 Rerank？Bi-Encoder / Cross-Encoder 的成本与精度怎样权衡？
- **VDB-001** · 18 个来源 · 🔥🔥🔥：Embedding 在检索里表示什么，文本如何变成向量，模型怎样选？
- **VDB-019** · 17 个来源 · 🔥🔥🔥：怎样用 Recall / Precision / Hit Rate / Latency 等指标证明 Retrieval 真的变好？
- **VDB-010** · 15 个来源 · 🔥🔥🔥：Vector DB / Index 怎样选型？Milvus、FAISS、pgvector、ES 等边界是什么？
- **VDB-005** · 11 个来源 · 🔥🔥🔥：HNSW 的基本图搜索机制是什么，适合什么规模与读写模式？
- **VDB-007** · 10 个来源 · 🔥🔥🔥：HNSW 与 IVF 怎样比较，Recall / Latency / Memory / Update 的取舍是什么？
- **VDB-015** · 10 个来源 · 🔥🔥🔥：RRF 为什么常用于多路召回融合？为什么不简单线性加权，参数怎样验证？
- **VDB-017** · 10 个来源 · 🔥🔥🔥：Retriever Top-K / Rerank Top-K 应怎样设置，如何用实验验证？
- **VDB-009** · 8 个来源 · 🔥🔥：为什么需要真正的 Vector DB，而不只用 MySQL/PostgreSQL 或本地 FAISS？
- **VDB-020** · 8 个来源 · 🔥🔥：Embedding / Index 升级后怎样处理重建、增量更新、旧向量兼容与新鲜度？

---

## 2. Canonical Questions

### VDB-001 · Embedding 在语义检索里表示什么？文本 / 图片怎样变成向量，Embedding Model 应怎样选？

- **Topic**：Embedding Basics / Model Selection
- **Question Type**：Concept / Project
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**18**
- **Evidence Sources**：`S040`, `S054`, `S062`, `S074`, `S095`, `S101`, `S109`, `S140`, `S178`, `S184`, `S199`, `S206`, `S212`, `S217`, `S248`, `S249`, `S258`, `S272`

**真实问法变体：**
- Embedding 到底表示什么，文本向量化过程怎样解释？
- 项目为什么选择当前 Embedding Model？
- 多模态图片如何预处理并进入向量检索？

### VDB-002 · Cosine Similarity、Dot Product / Inner Product、L2 Distance 有什么区别？不同向量归一化方式怎样影响结果？

- **Topic**：Similarity Metrics
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S062`, `S178`, `S184`, `S199`, `S210`, `S217`

**真实问法变体：**
- Similarity 如何计算？
- Cosine 与 L2 有什么差异？
- Vector Distance 是否来自 Embedding Model？

### VDB-003 · 为什么大规模向量检索不能总做暴力 Exact Search？ANN 牺牲了什么、换来了什么？

- **Topic**：Exact Search vs ANN
- **Question Type**：Why / Trade-off
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S054`, `S180`, `S211`, `S258`

**真实问法变体：**
- 向量规模变大后为什么需要 ANN？
- Vector Index 的核心优化目标是什么？

### VDB-004 · Vector Index 怎样根据数据规模、更新频率、Recall、Latency、Memory 与 QPS 选择？

- **Topic**：Index Selection
- **Question Type**：Trade-off / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S022`, `S054`, `S101`, `S125`, `S136`, `S180`, `S211`, `S251`, `S258`, `S277`

**真实问法变体：**
- 项目为什么选这个 Index？
- 不同 Vector Index 的优缺点是什么？
- Vector DB / Index 如何按规模选型？

### VDB-005 · HNSW 的基本图搜索机制是什么？它为什么能在高维空间做近似最近邻搜索？

- **Topic**：HNSW
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S054`, `S101`, `S125`, `S136`, `S180`, `S184`, `S211`, `S224`, `S251`, `S258`, `S277`

**真实问法变体：**
- HNSW Index 的核心图搜索机制是什么？
- 项目为什么使用 HNSW？

### VDB-006 · IVF / IVF_FLAT 的基本思想是什么？Cluster / List 划分与搜索候选范围如何影响 Recall 和 Latency？

- **Topic**：IVF
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S037`, `S054`, `S211`, `S224`, `S251`

**真实问法变体：**
- IVF_FLAT 的索引思想是什么？
- IVF Index 适合什么场景？

### VDB-007 · HNSW 与 IVF 怎样比较？Recall、Latency、Memory、Build Cost、Update Pattern 应怎样权衡？

- **Topic**：HNSW vs IVF
- **Question Type**：Comparison / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S037`, `S054`, `S101`, `S136`, `S180`, `S211`, `S224`, `S251`, `S258`, `S277`

**真实问法变体：**
- IVF 和 HNSW 怎么选？
- 两种 ANN Index 在速度、内存和准确率上怎样取舍？

### VDB-008 · Metadata Filter / Partition / Tenant Filter 怎样与向量检索结合？先过滤还是后过滤，怎样保证权限和 Recall？

- **Topic**：Metadata Filtering
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S037`, `S064`, `S101`, `S136`, `S206`, `S275`

**真实问法变体：**
- Milvus Collection / Partition / Metadata Filter 怎样使用？
- 企业知识库怎样避免跨 Tenant / 权限越界检索？

### VDB-009 · 为什么需要真正的 Vector DB，而不只用 MySQL / PostgreSQL / pgvector 或本地 FAISS？

- **Topic**：Storage Selection
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S022`, `S101`, `S136`, `S211`, `S212`, `S249`, `S267`, `S275`

**真实问法变体：**
- Vector DB 与 MySQL / PostgreSQL 分别适合什么？
- FAISS 与数据库自带 Vector Index 怎样选择？
- pgvector 什么时候够用，什么时候需要独立 Vector DB？

### VDB-010 · Milvus、FAISS、pgvector、Elasticsearch Vector 等方案怎样选？Library、Database、Search Engine 的边界是什么？

- **Topic**：Product / Architecture Selection
- **Question Type**：Comparison / Project
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**15**
- **Evidence Sources**：`S004`, `S022`, `S054`, `S064`, `S095`, `S101`, `S109`, `S125`, `S136`, `S184`, `S211`, `S212`, `S251`, `S255`, `S277`

**真实问法变体：**
- 为什么选 Milvus / FAISS / pgvector？
- ES 与 Milvus 的 Vector Retrieval 怎样比较？
- 是否调研过其它方案？

### VDB-011 · Vector Database 的 Collection / Partition / Schema / Primary Key / Metadata 应怎样建模？

- **Topic**：Vector Data Modeling
- **Question Type**：System Design
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S064`, `S101`, `S206`

**真实问法变体：**
- Milvus Collection 和 Partition 怎样组织？
- 结构化商户数据做 Embedding 后，Metadata 怎么保留？

### VDB-012 · Dense Retrieval 与 Sparse / Keyword Retrieval 分别擅长什么？专有名词、短 Query、长 Chunk 等场景为何会失配？

- **Topic**：Dense vs Sparse
- **Question Type**：Comparison / Failure Analysis
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**14**
- **Evidence Sources**：`S018`, `S031`, `S034`, `S037`, `S066`, `S072`, `S081`, `S095`, `S150`, `S184`, `S200`, `S217`, `S218`, `S251`

**真实问法变体：**
- 为什么纯向量检索对专有名词可能较差？
- BM25 与 Vector Retrieval 分别补什么短板？
- 短 Query 和长 Chunk 的匹配问题怎样处理？

### VDB-013 · 为什么要做 Dense + Sparse / BM25 Hybrid Retrieval？两路或多路召回怎样融合？

- **Topic**：Hybrid Retrieval
- **Question Type**：Why / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**24**
- **Evidence Sources**：`S018`, `S031`, `S034`, `S037`, `S040`, `S058`, `S066`, `S072`, `S081`, `S084`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S184`, `S200`, `S211`, `S217`, `S218`, `S240`, `S251`

**真实问法变体：**
- Keyword + Vector Hybrid Retrieval 怎样组合？
- Multi-way Retrieval 为什么需要，多路结果怎样 Fusion？
- Hybrid 相比纯 Vector 的收益如何证明？

### VDB-014 · BM25 的核心机制是什么？TF / IDF 为什么能帮助 Keyword Retrieval？

- **Topic**：BM25
- **Question Type**：Concept / Deep Dive
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S018`, `S081`, `S200`, `S217`, `S233`, `S275`

**真实问法变体：**
- BM25 的核心机制是什么？
- IDF 在 BM25 中起什么作用？

### VDB-015 · RRF 怎样融合多个排序结果？为什么不简单线性加权，RRF 常数 / 参数应如何验证？

- **Topic**：RRF / Fusion
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S072`, `S087`, `S095`, `S132`, `S163`, `S211`, `S224`, `S240`, `S249`, `S251`

**真实问法变体：**
- 为什么用 RRF 而不是线性权重？
- RRF 的 `k` 怎么调？
- 多路 Retrieval 结果如何 Fusion？

### VDB-016 · 为什么 Retrieval 后还需要 Rerank？Bi-Encoder / Cross-Encoder 的成本与精度怎样权衡？

- **Topic**：Reranking
- **Question Type**：Why / Comparison
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**20**
- **Evidence Sources**：`S021`, `S037`, `S054`, `S069`, `S081`, `S084`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S163`, `S184`, `S211`, `S212`, `S240`, `S249`, `S258`

**真实问法变体：**
- 为什么 Vector Recall 后还要 Rerank？
- Bi-Encoder 与 Cross-Encoder 有什么差异？
- Rerank 加上去反而变差，怎么定位？

### VDB-017 · Retriever Top-K / Rerank Top-K 应怎样设置？K 值如何在 Recall、Context Noise、Latency 与 Cost 之间取舍？

- **Topic**：Top-K Tuning
- **Question Type**：Trade-off / Evaluation
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S021`, `S069`, `S081`, `S084`, `S095`, `S101`, `S109`, `S148`, `S184`, `S240`

**真实问法变体：**
- Rerank 后 Top-K 如何选？
- 为什么不是 Top100？
- K 值怎样通过实验验证？

### VDB-018 · Embedding Dimension / Vector Normalization / Index Metric 等参数怎样影响质量、内存与检索成本？

- **Topic**：Embedding / Index Parameters
- **Question Type**：Trade-off
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S095`, `S199`, `S211`

**真实问法变体：**
- Embedding 维度为什么这样选？
- Vector Dimension 变化对存储和检索有什么影响？

### VDB-019 · 怎样用 Recall / Precision / Hit Rate / F1 / Latency 等指标证明 Retrieval 真的变好？

- **Topic**：Retrieval Evaluation
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**17**
- **Evidence Sources**：`S021`, `S022`, `S037`, `S052`, `S055`, `S058`, `S065`, `S095`, `S101`, `S109`, `S132`, `S184`, `S211`, `S218`, `S240`, `S248`, `S277`

**真实问法变体：**
- Retrieval Recall / Precision 怎么算？
- Hybrid 相比纯 Vector 的收益怎么证明？
- Recall 和 Precision 冲突时按业务怎样取舍？

### VDB-020 · Embedding Model / Index 升级后怎样处理 Re-embedding、索引重建、增量更新、旧向量兼容与知识新鲜度？

- **Topic**：Index Lifecycle / Freshness
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S068`, `S095`, `S101`, `S109`, `S140`, `S217`, `S246`, `S277`

**真实问法变体：**
- Embedding Model 升级后旧向量怎么办？
- 单篇文档更新时怎样局部更新 Index？
- Knowledge Base 怎样增量更新并保持新鲜度？

### VDB-021 · 多模态 Embedding / Retrieval 怎样处理图片、文本和图文关系？不同模态是否需要共享空间？

- **Topic**：Multimodal Retrieval
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S052`, `S058`, `S095`, `S184`, `S248`

**真实问法变体：**
- 图片如何预处理并向量化？
- 多模态 Knowledge Base 如何保持图文关联？

### VDB-022 · Graph DB / GraphRAG 与 Vector DB 的职责有什么不同？什么 Query 真正值得走图关系而不是向量召回？

- **Topic**：Graph vs Vector
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S037`, `S058`, `S072`, `S211`, `S246`, `S267`, `S272`

**真实问法变体：**
- Graph Database 与 Vector Database 各适合什么查询？
- 哪些问题真的需要 GraphRAG？

### VDB-023 · Codebase / Repository Retrieval 什么时候该用 Vector RAG，什么时候更适合 AST / LSP / ripgrep / 文件搜索等结构化工具？

- **Topic**：Code Retrieval Boundary
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S038`, `S059`, `S132`, `S145`, `S218`

**真实问法变体：**
- Coding Agent 为什么不一定依赖传统 Code RAG？
- 大型 Repo 怎样用 Dependency Graph / AST / Search 找到相关代码？
- RAG 与 Tool-based Repository Search 有什么差异？

---

## 3. 真人面经反复出现的追问链

### 3.1 从 Embedding 到 ANN

```text
Embedding 是什么
→ Similarity 怎么算
→ 为什么不能全量暴力比对
→ ANN
→ HNSW / IVF
→ Index 选型
→ Recall / Latency / Memory / Update Trade-off
```

### 3.2 从单路召回到多阶段检索

```text
Dense Retrieval
→ 专有名词 / Exact Term 失败
→ BM25 / Sparse
→ Hybrid Retrieval
→ RRF / Fusion
→ Rerank
→ Top-K
→ Context Noise / Latency
→ Evaluation
```

### 3.3 从 Demo 到 Production Vector Store

```text
FAISS / pgvector / Milvus / ES 选型
→ Collection / Metadata / Tenant Filter
→ Index Build
→ Incremental Update
→ Embedding Upgrade / Rebuild
→ Freshness
→ QPS / Latency / Recall
→ Permission / Multi-tenant
```

---

## 4. 对后续 Vector DB 教材的校准建议

1. 必须从 `Embedding → Similarity → Exact Search → ANN` 开始，而不是直接教 Milvus API；
2. HNSW / IVF 要讲“为什么”和 Trade-off，再进入参数；
3. `Dense vs Sparse → Hybrid → RRF → Rerank → Top-K` 应成为一条连续核心主线；
4. 产品选型要区分 **ANN Library、关系数据库扩展、Search Engine、独立 Vector DB**；
5. Production 章节必须加入 Metadata Filter、Multi-tenant、Incremental Update、Embedding Upgrade、Index Rebuild；
6. Retrieval Evaluation 与索引原理同级重要：项目声称“召回提高”必须能说明 Dataset / Baseline / Metric；
7. Code Retrieval 与 Graph Retrieval 应作为“Vector DB 不该包打天下”的边界章节；
8. HNSW `M / efConstruction / efSearch`、IVF `nlist / nprobe` 等即使没有在 HUMAN-A 中形成高频独立问法，也仍属于完整知识体系的必要参数层，后续教材应系统补齐，但不能冒充真实高频统计。
