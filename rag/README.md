# RAG｜AI 应用开发秋招系统手册

> **当前状态：🚧 第一版系统教材建设中。**
>
> RAG 是这套 Handbook 的第 8 个正式一级模块。目标不是“会 LangChain Retriever + Vector DB”，而是从 0 建立一条可验证、可维护、可上线的 Retrieval-Augmented Generation 因果链：**为什么需要 RAG → 知识怎样进入系统 → 文档怎样解析 / 切分 → Query 怎样被理解 → 多路 Retrieval 怎样召回 → Fusion / Rerank 怎样收窄 → Evidence 怎样进入 Context → Answer 怎样 Ground → 质量怎样测 → Bad Case 怎样归因 → 知识怎样持续更新和安全运营。**

## 1. 固定课程原则

继续固定遵守：

> **知识体系演进顺序优先，真实面经只用于调整复习权重、补充真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

冻结 `S001–S279` 中，Production RAG Pipeline、Chunk、Hybrid Retrieval、Rerank、Evaluation 都非常高频，但课程仍然先从“为什么 RAG、Corpus 从哪里来、Document 怎样成为可检索证据”开始。

```text
Why RAG
→ Corpus
→ Ingestion / Parse
→ Chunk
→ Retrieval Data Model
→ Query Transformation
→ Dense / Sparse
→ Hybrid / Fusion
→ Rerank / Top-K
→ Context Construction
→ Grounding / Citation
→ Evaluation
→ Bad Case Attribution
→ Freshness / Permission / Scale
→ GraphRAG / Agentic RAG
```

---

## 2. 与前后模块的边界

前置已经学过：

```text
LLM Foundation
→ Embedding / Reranker 的模型原理

Vector DB
→ Vector / Similarity / ANN / HNSW / IVF
→ Metadata Filter / Index Lifecycle
```

所以 RAG 不重复讲 HNSW 内部结构，也不重新推导 Transformer。

本模块负责的是：

```text
Corpus / Ingestion / Parsing
Chunking
Query Transformation
Dense / Sparse Retrieval Strategy
Hybrid / RRF / Fusion
Rerank Pipeline
Top-K / Threshold / Candidate Budget
Context Construction
Grounding / Citation
Retrieval / End-to-end Evaluation
Experiment / Regression
Bad Case Attribution
Freshness / Permission / Version
Large-scale Ingestion
Latency / Cost / Cache / Observability
GraphRAG
Agentic RAG Boundary
```

| 问题 | Primary Module |
|---|---|
| Embedding / Reranker 模型内部原理 | LLM Foundation |
| HNSW / IVF / ANN / Vector Storage | Vector DB |
| Parser → Chunk → Retrieval → Generation 全链 | RAG |
| Hybrid / RRF / Retrieval Top-K / Retrieval Eval | RAG |
| Agent 是否继续检索、何时调用 Retriever | Agent Harness / Runtime 控制面；RAG 讲检索策略接口 |
| Queue / Retry / Backpressure / Async Worker | AI Backend Engineering |
| 多租户 AI 平台整体架构 | System Design |

一句话：

> **Vector DB 解决“怎样高效找近邻”；RAG 解决“怎样把真实知识转成可检索证据，并证明最终回答真的因此变好”。**

---

## 3. 真人面经信号

当前 RAG 有 **29 道 Primary Canonical、88 个独立 HUMAN-A 来源**覆盖，其中 **20 道达到 L4**。

| Topic | HUMAN-A Sources | 深度 |
|---|---:|---:|
| End-to-end Pipeline | 38 | L3 |
| Chunk Strategy | 30 | L3 |
| Hybrid Retrieval | 25 | L4 |
| Reranking | 22 | L4 |
| End-to-end Evaluation | 21 | L4 |
| Bad Case Attribution | 19 | L4 |
| Query Transformation | 18 | L4 |
| Retrieval Metrics | 16 | L3 |
| Chunking Principles | 15 | L3 |
| Dense vs Sparse / BM25 | 15 | L3 |
| Parsing / OCR / Layout | 13 | L4 |
| Incremental Update / Freshness | 13 | L4 |
| RAG Boundary | 12 | L4 |
| Chunk Parameters | 12 | L3 |
| Fusion / RRF | 10 | L3 |
| Top-K | 10 | L3 |
| Evaluation Dataset / Judge | 9 | L4 |
| Multimodal / Table Parsing | 9 | L4 |
| Experiment Design | 8 | L4 |
| Latency / Cost | 8 | L4 |
| GraphRAG | 8 | L4 |

> **Interview Heat ≠ Knowledge Importance。** Document Identity / Lineage、Cleaning / Dedup、Chunk Data Model、Trace / Observability、Rollback / Snapshot 等即使不是独立 Canonical，也属于 Production RAG 的必要骨架。

---

## 4. 六条学习主线

### A｜知识怎样进入系统

```text
RAG Boundary
→ Corpus Audit
→ Source of Truth
→ Document Identity / Version
→ Parse / OCR / Layout
→ Table / Image / Multimodal
→ Cleaning / Dedup
```

### B｜知识怎样被切成可检索单元

```text
Chunk Principle
→ Fixed / Recursive / Structure-aware / Semantic
→ Size / Overlap
→ Parent-child / Neighbor Window
→ Semantic Boundary Failure
→ Metadata / Lineage
```

### C｜Query 怎样变成 Retrieval Plan

```text
Normalize
→ Intent / Rewrite
→ Clarify
→ Decompose / Multi-query / HyDE
→ No-hit / Refusal
```

### D｜怎样从候选中得到 Evidence

```text
Dense
+ Sparse / BM25
→ Hybrid
→ RRF / Fusion
→ Rerank
→ Top-K / Threshold
→ Context Construction
→ Grounding / Citation
```

### E｜怎样证明“变好了”

```text
Ground Truth
→ Recall / Precision / Hit Rate / MRR / NDCG
→ End-to-end Eval
→ Faithfulness / Correctness / Relevance
→ Judge Reliability
→ Baseline / Ablation / A-B
→ Regression
→ Bad Case Attribution
```

### F｜怎样长期运营

```text
Incremental Update
→ Freshness / Version / Snapshot / Rollback
→ Permission / Tenant
→ Large-scale Ingestion
→ Latency / Cost / Cache
→ Trace / Observability
→ GraphRAG
→ Agentic RAG
```

---

## 5. 完整 34 章

### Part A｜从“为什么 RAG”到可靠 Corpus

1. [RAG 在 AI Application 中负责什么](docs/01-RAG在AI应用中的职责.md)
2. [Production RAG End-to-end Pipeline](docs/02-RAG完整链路.md)
3. [Corpus Audit：先审计数据，再谈检索](docs/03-CorpusAudit.md)
4. [Document Identity、Lineage、Version 与 Source of Truth](docs/04-DocumentIdentity与Lineage.md)
5. [Parsing：PDF / Markdown / HTML / Office / OCR](docs/05-Parsing与OCR.md)
6. [Layout、Table、Image 与 Multimodal Document](docs/06-LayoutTableMultimodal.md)
7. [Cleaning、Normalization、Dedup 与 Boilerplate Removal](docs/07-Cleaning与Dedup.md)

### Part B｜Chunking：从文本变成 Retrieval Unit

8. [为什么 Chunking 是 RAG 核心](docs/08-ChunkingPrinciples.md)
9. [Fixed / Recursive / Structure-aware / Semantic Chunk](docs/09-ChunkStrategy.md)
10. [Chunk Size / Overlap 怎样实验](docs/10-ChunkSize与Overlap.md)
11. [Parent-child、Neighbor Window 与 Context Expansion](docs/11-ParentChild与Neighbor.md)
12. [Semantic Boundary Failure：被切断的逻辑怎样修](docs/12-SemanticBoundaryFailure.md)
13. [Chunk ID、Metadata、Hierarchy 与可追溯数据模型](docs/13-ChunkDataModel.md)

### Part C｜Query 到候选召回

14. [一次 Retrieval Request 怎样执行](docs/14-RetrievalRequestLifecycle.md)
15. [Query Normalize / Rewrite / Intent / Clarification](docs/15-QueryRewrite与Clarification.md)
16. [Decomposition、Multi-query 与 HyDE](docs/16-DecompositionMultiQueryHyDE.md)
17. [Retrieval Miss、Threshold、No-hit 与 Refusal](docs/17-NoHit与Refusal.md)
18. [Dense Retrieval：什么时候语义向量擅长](docs/18-DenseRetrieval.md)
19. [Sparse Retrieval / BM25：精确词为什么仍重要](docs/19-BM25与SparseRetrieval.md)
20. [Hybrid Retrieval：为什么组合 Dense + Sparse](docs/20-HybridRetrieval.md)
21. [RRF / Fusion：多路召回怎样合并](docs/21-RRF与Fusion.md)
22. [Rerank Pipeline：Precision、Latency 与 Failure](docs/22-RerankPipeline.md)
23. [Top-K、Threshold 与 Candidate Budget](docs/23-TopK与CandidateBudget.md)

### Part D｜Evidence 到最终回答

24. [Context Construction：证据怎样进入 LLM](docs/24-ContextConstruction.md)
25. [Grounding、Citation 与 Reference Mapping](docs/25-Grounding与Citation.md)

### Part E｜Evaluation 与 Bad Case

26. [Retrieval Metrics：Recall / Precision / Hit Rate / MRR / NDCG](docs/26-RetrievalMetrics.md)
27. [Evaluation Dataset、Ground Truth 与 LLM Judge](docs/27-EvaluationDataset与Judge.md)
28. [End-to-end RAG Evaluation](docs/28-EndToEndEvaluation.md)
29. [Baseline、Ablation、A-B 与 Regression](docs/29-Experiment与Regression.md)
30. [Bad Case Attribution：到底坏在哪一层](docs/30-BadCaseAttribution.md)

### Part F｜Production RAG

31. [Freshness、Incremental Update、Version、Snapshot 与 Rollback](docs/31-Freshness与Version.md)
32. [Permission、Tenant Filtering 与安全边界](docs/32-Permission与Tenant.md)
33. [Large-scale Ingestion、Latency / Cost、Cache 与 Observability](docs/33-ScaleCostObservability.md)
34. [GraphRAG、Agentic RAG 与 Production Architecture](docs/34-GraphRAG与AgenticRAG.md)

---

## 6. 为什么加入面经之外的章节

### Document Identity / Lineage

如果没有稳定 `document_id / version / source / chunk_id`：

- Citation 无法回源；
- 文档更新无法精确删除旧 Chunk；
- Embedding Model 升级无法做 Blue-Green；
- Bad Case 无法复现。

它不是“数据库小细节”，而是 Production RAG 的生命线。

### Cleaning / Dedup

Header、Footer、导航、重复 PDF、旧版本文档如果不清理，会污染 Chunk、Embedding 和 Retrieval。检索优化不能从脏 Corpus 上直接开始。

### Trace / Observability

只有记录：

```text
query
rewrite
retrieved ids + scores
fusion
rerank
final context
prompt/model
answer/citations
latency/version
```

Bad Case 才能复现和归因。

因此这些属于知识骨架，不因当前没有独立高频 Canonical 就删除。

---

## 7. 推荐三遍学习法

第一遍严格按 `01 → 34`，先建立因果链。

第二遍进入 `review/`，自己画：

- Ingestion → Index；
- Chunk Hierarchy；
- Dense / Sparse / Hybrid / RRF / Rerank；
- Context Construction；
- Retrieval / Generation Eval；
- Freshness / Version / Permission；
- Production Trace。

第三遍进入 `interview/`，练：

```text
为什么这样设计？
→ 指标怎么证明？
→ 变差时怎么归因？
→ 数据量扩大怎么办？
→ 权限 / 新鲜度 / 成本怎么办？
```

---

## 8. 下一环

RAG 完成后进入 **Agent Harness / Runtime**。

到时会把 RAG 暴露为一种可调用能力：

```text
Agent Loop
→ 判断是否需要 Retrieval
→ Query / Retrieval Tool
→ Inspect Evidence
→ 必要时改写 / 继续检索
→ Stop / Answer
```

RAG 负责检索与证据质量；Agent Harness 负责控制循环、Tool Runtime、Context、Memory、Checkpoint、Permission 与 Failure Recovery。
