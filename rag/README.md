# RAG｜AI 应用开发秋招系统手册

> **Granularity Audit：✅ 已完成。** 原 34 章内容已按 Production RAG 子系统收敛为 **14 个正式知识小板块**；29 道 RAG Canonical、88 个 HUMAN-A 覆盖来源和所有 Source Count 保持不变。
>
> 目标是从 0 建立一条真正可上线、可评估、可维护的 Retrieval-Augmented Generation 因果链：**Knowledge Source → Document Processing → Chunk → Query Planning → Retrieval → Rerank → Evidence → Grounded Generation → Evaluation → Production Governance。**

---

## 1. 固定课程原则

> **知识体系演进顺序优先，真人面经只调整权重与追问深度。**

第二条正式规则：

> **Chunk Size、RRF、Top-K、NDCG 这些可以是独立面试题，但教材文件应该对应 Chunking、Retrieval、Evaluation 这样的完整子系统。**

因此这次 34→14 只改变教材组织，不删任何能力。

---

## 2. 与其它模块的边界

前置：

```text
LLM Foundation
→ Embedding / Reranker model foundation

Vector DB
→ Similarity / ANN / HNSW / IVF / Filter / Index Lifecycle
```

RAG 负责：

```text
Corpus / Ingestion / Parsing
Chunking / Data Model
Query Transformation
Dense / Sparse / Hybrid / Fusion
Rerank / Candidate Budget
Context / Grounding / Citation
Retrieval & End-to-end Evaluation
Bad Case Attribution
Freshness / Permission
Scale / Observability
GraphRAG / Agentic RAG
```

一句话：

> **Vector DB 解决怎样高效找近邻；RAG 解决怎样把知识变成可信 Evidence，并证明最终回答因此变好。**

---

## 3. 真人面经信号

当前 RAG 有 **29 道 Primary Canonical、88 个独立 HUMAN-A 来源**，其中 20 道达到 L4。

最强市场信号包括：

- End-to-end Pipeline；
- Chunk Strategy / Principles / Parameters；
- Hybrid Retrieval；
- Reranking；
- End-to-end Evaluation；
- Bad Case Attribution；
- Query Transformation；
- Retrieval Metrics；
- Dense vs Sparse / BM25；
- Parsing / OCR / Layout；
- Freshness / Incremental Update；
- Fusion / RRF / Top-K。

Document Identity、Cleaning、Chunk Data Model、Trace、Rollback 等即使不是最强独立面经信号，仍然属于 Production 骨架。

---

## 4. 为什么从 34 合并到 14

```text
RAG Boundary + End-to-end Pipeline
→ RAG Role & Pipeline

Corpus Audit + Identity/Lineage
→ Corpus Governance

Parsing/OCR + Layout/Multimodal + Cleaning/Dedup
→ Document Processing

Chunk Principle + Strategy + Size/Overlap
→ Chunking Design

Parent-child + Semantic Boundary + Chunk Data Model
→ Advanced Chunk Structure

Request Lifecycle + Rewrite + Decomposition/Multi-query/HyDE + No-hit
→ Query Understanding & Retrieval Planning

Dense + Sparse/BM25 + Hybrid + RRF/Fusion
→ Retrieval Stack

Rerank + Top-K/Candidate Budget
→ Candidate Funnel

Context Construction + Grounding/Citation
→ Evidence Delivery

Retrieval Metrics + Dataset/Judge
→ Retrieval Evaluation

End-to-end Eval + Experiment/Regression + Bad Case
→ Quality Engineering

Freshness/Version + Permission/Tenant
→ Production Governance
```

Scale/Cost/Observability 与 GraphRAG/Agentic RAG 已经是独立 Production / Architecture 边界，继续保留。


---

## 5. 正式 14 个知识小板块

1. [RAG 的职责与 Production End-to-End Pipeline](docs/01-RAG职责与完整链路.md)
2. [Corpus Governance：Audit、Identity、Lineage、Version、Source of Truth](docs/02-CorpusGovernance.md)
3. [Document Processing：Parsing、OCR、Layout、Multimodal、Cleaning、Dedup](docs/03-DocumentProcessing.md)
4. [Chunking Design：原则、Strategy、Size、Overlap](docs/04-ChunkingDesign.md)
5. [Advanced Chunk Structure：Parent-child、Neighbor、Boundary、Data Model](docs/05-AdvancedChunkStructure.md)
6. [Query Understanding & Retrieval Planning](docs/06-QueryPlanning.md)
7. [Retrieval Stack：Dense、BM25、Hybrid、Fusion](docs/07-RetrievalStack.md)
8. [Rerank 与 Candidate Budget](docs/08-Rerank与CandidateBudget.md)
9. [Context Construction、Grounding 与 Citation](docs/09-EvidenceDelivery.md)
10. [Retrieval Evaluation：Metrics、Ground Truth、Dataset、Judge](docs/10-RetrievalEvaluation.md)
11. [End-to-End Evaluation、Ablation、Regression 与 Bad Case](docs/11-EndToEndQualityEngineering.md)
12. [Production Governance：Freshness、Version、Permission、Tenant、Rollback](docs/12-ProductionGovernance.md)
13. [Large-scale Ingestion、Latency / Cost、Cache 与 Observability](docs/13-ScaleCostObservability.md)
14. [GraphRAG、Agentic RAG 与 Production Architecture](docs/14-GraphRAG与AgenticRAG.md)

---

## 6. 六条主线

### A｜Knowledge Ingestion

```text
RAG Boundary
→ Corpus Governance
→ Document Processing
```

### B｜Retrieval Unit

```text
Chunking Design
→ Advanced Chunk Structure / Data Model
```

### C｜Query → Candidate

```text
Query Planning
→ Dense / Sparse / Hybrid / Fusion
→ Rerank / Candidate Budget
```

### D｜Candidate → Evidence → Answer

```text
Context Construction
→ Grounding
→ Citation
```

### E｜Quality Engineering

```text
Ground Truth / Metrics
→ End-to-end Eval
→ Ablation / Regression
→ Bad Case Attribution
```

### F｜Production Governance

```text
Freshness / Permission
→ Scale / Observability
→ GraphRAG / Agentic RAG
```

---

## 7. 配套复习与面试材料

研究/面试层不做同样压缩：

- [`review/README.md`](review/README.md)：仍用总图和综合问题跨越多个子系统；
- [`interview/高频面试题.md`](interview/高频面试题.md)：40 道独立面试问题；
- [`interview/面试易错点.md`](interview/面试易错点.md)：60 个错误边界；
- [`interview/面试前速查表.md`](interview/面试前速查表.md)。

这正是不同层级不同粒度：

```text
14 curriculum blocks
≠ 29 Canonical Questions
≠ 40 interview prompts
```

---

## 8. 下一环：Agent Harness / Runtime

RAG 在 Agent 中成为一种 Capability：

```text
Agent Loop
→ decide whether retrieval needed
→ call retrieval tool
→ inspect evidence
→ continue / reformulate / stop
```

RAG 负责 Evidence Quality；Agent Harness 负责控制循环、Tool Runtime、Context、Memory、Checkpoint、Permission 和 Failure Recovery。
