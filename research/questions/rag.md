# RAG Canonical Questions — S001–S279 全库纵向扫描 v3

更新日期：2026-09-10

> 一级板块：**RAG**。本文件负责完整 Retrieval-Augmented Generation 工程链：Corpus → Parse → Chunk → Query Transformation → Retrieval → Fusion → Rerank → Context → Generate → Evaluate → Operate。Vector DB 的 ANN / Index / Storage 归 `Vector DB`；Embedding / Rerank 模型内部原理归 `LLM Foundation`；Agentic orchestration 控制面归 `Agent Harness / Runtime`。
>
> 本文件所有 ACTIVE 条目的 `Primary Module = RAG`。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**29**
- MOVED：**1**（旧 `RAG-030`）
- 证据范围：仅 `S001–S279`
- 当前版本：`v3`（Global Merge / Split Audit）

### 高频信号

- `RAG-002` · 31：Production RAG 完整链路
- `RAG-007` · 29：Chunk Strategy
- `RAG-013` · 24：Hybrid Retrieval
- `RAG-015` · 22：Rerank
- `RAG-021` · 21：RAG End-to-end Evaluation
- `RAG-019` · 18：Bad Case Attribution
- `RAG-010` · 17：Query Rewrite / Decomposition / Clarification
- `RAG-024` · 13：Incremental Update / Freshness
- `RAG-004` / `008` · 12：Parsing 与 Chunk 参数实验

---

## 2. Boundary / Corpus / Parsing

### RAG-001 · 为什么需要 RAG？什么时候 Long Context、文件搜索、更强模型或 Fine-tuning 更合适？
- **Topic**：RAG Boundary
- **Question Type**：Why / Comparison
- **Depth**：L4
- **Source Count**：**11**
- **Evidence Sources**：`S023`, `S031`, `S045`, `S068`, `S145`, `S218`, `S222`, `S249`, `S257`, `S267`, `S275`
- **Related Modules**：LLM Foundation（应用工程深度）, Agent Harness / Runtime

### RAG-002 · Production RAG 从 Ingestion / Parse / Chunk / Embedding / Index 到 Retrieve / Rerank / Context / LLM 的完整链路是什么？
- **Topic**：End-to-end Pipeline
- **Question Type**：Concept / Project
- **Depth**：L3
- **Source Count**：**31**
- **Evidence Sources**：`S006`, `S021`, `S024`, `S026`, `S029`, `S031`, `S040`, `S053`, `S063`, `S068`, `S071`, `S074`, `S081`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S163`, `S184`, `S200`, `S211`, `S217`, `S240`, `S249`, `S251`, `S262`, `S275`, `S277`

### RAG-003 · 建 RAG 前怎样审计 Corpus：数据来源、质量、重复、版本、权限和真实规模如何影响方案？
- **Topic**：Corpus / Data Audit
- **Question Type**：Project / System Design
- **Depth**：L4
- **Source Count**：**7**
- **Evidence Sources**：`S052`, `S056`, `S058`, `S217`, `S246`, `S248`, `S275`

### RAG-004 · PDF / OCR / Layout / Markdown / HTML 等异构文档怎样可靠解析？电子 PDF 与扫描 PDF 如何统一处理？
- **Topic**：Parsing / OCR / Layout
- **Question Type**：System Design / Project
- **Depth**：L4
- **Source Count**：**12**
- **Evidence Sources**：`S024`, `S029`, `S052`, `S058`, `S074`, `S095`, `S162`, `S184`, `S217`, `S240`, `S253`, `S275`

### RAG-005 · 表格、图片与多模态内容怎样保留结构和引用关系？Cross-page Table 被切断时如何恢复语义？
- **Topic**：Multimodal / Table Parsing
- **Question Type**：Failure Analysis / System Design
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S024`, `S052`, `S058`, `S074`, `S162`, `S217`, `S240`, `S253`, `S275`
- **Related Modules**：LLM Foundation（应用工程深度）

---

## 3. Chunking

### RAG-006 · 文档切分为什么是 RAG 核心环节？Chunk Granularity 怎样影响 Recall、Precision、Context Noise 与 Generation？
- **Topic**：Chunking Principles
- **Question Type**：Why / Deep Dive
- **Depth**：L3
- **Source Count**：**15**
- **Evidence Sources**：`S002`, `S022`, `S024`, `S026`, `S037`, `S040`, `S054`, `S058`, `S062`, `S072`, `S074`, `S217`, `S240`, `S253`, `S275`

### RAG-007 · Chunk Strategy 怎样选择？Fixed、Recursive、Semantic、Parent-child、Structure-aware 分别适合什么数据？
- **Topic**：Chunk Strategy
- **Question Type**：Comparison / Project
- **Depth**：L3
- **Source Count**：**29**
- **Evidence Sources**：`S002`, `S018`, `S021`, `S022`, `S024`, `S026`, `S029`, `S031`, `S037`, `S040`, `S054`, `S055`, `S058`, `S064`, `S068`, `S072`, `S074`, `S081`, `S084`, `S095`, `S101`, `S109`, `S162`, `S184`, `S217`, `S240`, `S249`, `S253`, `S275`

### RAG-008 · Chunk Size / Overlap 如何设置？参数怎样通过 Dataset / Experiment 验证，而不是照抄默认值？
- **Topic**：Chunk Parameters
- **Question Type**：Trade-off / Evaluation
- **Depth**：L3
- **Source Count**：**12**
- **Evidence Sources**：`S002`, `S022`, `S054`, `S062`, `S065`, `S072`, `S074`, `S109`, `S217`, `S240`, `S253`, `S275`

### RAG-009 · Chunk 把强逻辑关系、充分必要条件或跨块上下文切断时，怎样修复 Semantic Boundary Failure？
- **Topic**：Semantic Boundary Failure
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S024`, `S058`, `S162`, `S218`, `S240`, `S253`

---

## 4. Query Transformation / Retrieval

### RAG-010 · Query Rewrite / Decomposition / Multi-query / Intent / Clarification 怎样改善 Retrieval？什么时候应该先向用户追问？
- **Topic**：Query Transformation
- **Question Type**：System Design / Comparison
- **Depth**：L4
- **Source Count**：**17**
- **Evidence Sources**：`S008`, `S024`, `S040`, `S055`, `S056`, `S057`, `S066`, `S072`, `S081`, `S095`, `S101`, `S132`, `S148`, `S150`, `S240`, `S249`, `S250`

### RAG-011 · Retrieval Miss / No-hit 如何定义？阈值怎样设置，何时拒答、澄清或走 Fallback？
- **Topic**：No-hit / Refusal
- **Question Type**：Failure Analysis / Trade-off
- **Depth**：L3
- **Source Count**：**6**
- **Evidence Sources**：`S052`, `S055`, `S067`, `S081`, `S109`, `S240`

### RAG-012 · Dense Retrieval 与 Keyword / BM25 Sparse Retrieval 各擅长什么？为什么专有名词、短 Query、精确条款会暴露纯向量短板？
- **Topic**：Dense vs Sparse / BM25
- **Question Type**：Comparison / Failure Analysis
- **Depth**：L3
- **Source Count**：**15**
- **Evidence Sources**：`S018`, `S031`, `S034`, `S037`, `S066`, `S072`, `S081`, `S095`, `S150`, `S184`, `S200`, `S217`, `S218`, `S251`, `S275`
- **Related Modules**：Vector DB

### RAG-013 · 为什么要做 Hybrid Retrieval？Dense / Sparse / Multi-way Retrieval 的结果怎样融合并验证收益？
- **Topic**：Hybrid Retrieval
- **Question Type**：Why / System Design
- **Depth**：L4
- **Source Count**：**24**
- **Evidence Sources**：`S018`, `S031`, `S034`, `S037`, `S040`, `S058`, `S066`, `S072`, `S081`, `S084`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S184`, `S200`, `S211`, `S217`, `S218`, `S240`, `S251`
- **Related Modules**：Vector DB

### RAG-014 · RRF / Fusion 为什么常用于多路召回？为什么不简单线性加权，参数怎样调？
- **Topic**：Fusion / RRF
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Source Count**：**10**
- **Evidence Sources**：`S072`, `S087`, `S095`, `S132`, `S163`, `S211`, `S224`, `S240`, `S249`, `S251`

### RAG-015 · 为什么需要 Rerank？如何平衡 Precision、Latency、Cost，并定位“Rerank 反而变差”？
- **Topic**：Reranking
- **Question Type**：Why / Troubleshoot / Trade-off
- **Depth**：L4
- **Source Count**：**22**
- **Evidence Sources**：`S021`, `S037`, `S054`, `S069`, `S081`, `S084`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S163`, `S184`, `S211`, `S212`, `S223`, `S240`, `S249`, `S258`, `S277`
- **Related Modules**：LLM Foundation（应用工程深度）

### RAG-016 · Retrieval / Rerank Top-K 怎样设置？K 在 Recall、Context Noise、Latency 与 Token Cost 之间如何取舍？
- **Topic**：Top-K
- **Question Type**：Trade-off / Evaluation
- **Depth**：L3
- **Source Count**：**9**
- **Evidence Sources**：`S021`, `S069`, `S081`, `S084`, `S095`, `S101`, `S109`, `S184`, `S240`

### RAG-017 · Retrieval Evidence 怎样组装进 LLM Context？标题、Metadata、邻居块、来源与排序怎样影响回答？
- **Topic**：Context Construction
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**7**
- **Evidence Sources**：`S024`, `S066`, `S095`, `S168`, `S218`, `S240`, `S275`
- **Related Modules**：LLM Foundation（应用工程深度）

### RAG-018 · 最终回答怎样做 Grounding / Citation / Reference Mapping，保证结论能回到真实证据？
- **Topic**：Grounding / Citation
- **Question Type**：System Design / Verification
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S052`, `S240`, `S275`

---

## 5. Evaluation / Troubleshooting

### RAG-019 · RAG Bad Case / Hallucination 出现时，怎样区分 Parsing、Chunk、Embedding、Retrieval、Rerank、Prompt、Generation、Runtime 问题？
- **Topic**：Bad Case Attribution
- **Question Type**：Troubleshoot
- **Depth**：L4
- **Source Count**：**18**
- **Evidence Sources**：`S010`, `S022`, `S037`, `S041`, `S045`, `S052`, `S055`, `S058`, `S061`, `S067`, `S081`, `S095`, `S109`, `S150`, `S218`, `S240`, `S249`, `S255`

### RAG-020 · 怎样定义 Retrieval Quality：Recall、Precision、Hit Rate、MRR / NDCG 等指标分别回答什么问题？
- **Topic**：Retrieval Metrics
- **Question Type**：Concept / Evaluation
- **Depth**：L3
- **Source Count**：**15**
- **Evidence Sources**：`S021`, `S022`, `S037`, `S052`, `S055`, `S058`, `S065`, `S095`, `S101`, `S109`, `S132`, `S184`, `S211`, `S240`, `S248`

### RAG-021 · RAG 质量怎样做 End-to-end Evaluation？Retrieval、Faithfulness、Answer Relevance / Correctness 怎样分层？
- **Topic**：RAG Evaluation
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Source Count**：**21**
- **Evidence Sources**：`S021`, `S022`, `S031`, `S037`, `S041`, `S052`, `S055`, `S057`, `S058`, `S061`, `S074`, `S095`, `S101`, `S109`, `S148`, `S184`, `S211`, `S218`, `S240`, `S253`, `S277`

### RAG-022 · Evaluation Dataset / Ground Truth 从哪里来？怎样代表线上真实 Query，并避免 LLM Judge 自身不可靠？
- **Topic**：Evaluation Dataset / Judge
- **Question Type**：Evaluation / Failure Analysis
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S052`, `S057`, `S058`, `S061`, `S095`, `S218`, `S240`, `S246`, `S253`

### RAG-023 · 怎样用 Baseline / Ablation / A-B Experiment 证明 Chunk、Hybrid、Rerank、GraphRAG 等优化的真实收益？
- **Topic**：Experiment Design
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S055`, `S057`, `S058`, `S072`, `S218`, `S240`, `S246`, `S257`

---

## 6. Production RAG

### RAG-024 · Knowledge Base 怎样做增量更新、版本管理、旧数据清理和在线新鲜度保障？
- **Topic**：Incremental Update / Freshness
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**13**
- **Evidence Sources**：`S055`, `S068`, `S095`, `S101`, `S109`, `S127`, `S140`, `S170`, `S217`, `S240`, `S246`, `S275`, `S277`
- **Related Modules**：Vector DB

### RAG-025 · 企业 RAG 怎样做 Permission / Tenant Filtering，防止检索到用户无权读取的知识？
- **Topic**：Permission / Security
- **Question Type**：Security / System Design
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S059`, `S254`, `S275`
- **Related Modules**：Vector DB, Agent Harness / Runtime

### RAG-026 · 百 GB / TB 级语料怎样做 Ingestion、Embedding、Index Build、并行处理与成本控制？
- **Topic**：Large-scale RAG
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**4**
- **Evidence Sources**：`S056`, `S217`, `S240`, `S277`
- **Related Modules**：AI Backend Engineering, Vector DB

### RAG-027 · RAG Latency / Cost 的主要瓶颈在哪里？Parse、Embedding、Retrieve、Rerank、LLM、Cache 各层怎样优化？
- **Topic**：Latency / Cost
- **Question Type**：Troubleshoot / Trade-off
- **Depth**：L4
- **Source Count**：**7**
- **Evidence Sources**：`S021`, `S029`, `S045`, `S109`, `S217`, `S223`, `S257`
- **Related Modules**：AI Backend Engineering, LLM Foundation（应用工程深度）

### RAG-028 · GraphRAG / Knowledge Graph Retrieval 相比普通 Vector RAG 解决什么问题？Triple / Community / Graph Update 怎样保证质量？
- **Topic**：GraphRAG
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S037`, `S058`, `S072`, `S211`, `S246`, `S267`, `S272`, `S277`
- **Related Modules**：Vector DB

### RAG-029 · Agentic RAG 与固定 One-shot RAG 有什么区别？什么时候让 Agent 主动决定检索、重写、继续检索或停止？
- **Topic**：Agentic RAG
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S045`, `S081`, `S109`, `S150`, `S222`, `S277`
- **Related Modules**：Agent Harness / Runtime

---

## 7. MOVED：Global Merge / Split Audit

| Legacy QID | 原问题 | 新 Primary Canonical |
|---|---|---|
| `RAG-030` | Code RAG / Repository QA 与 AST、LSP、ripgrep、Filesystem Search 等 Tool-based Search 怎样分工？ | **MERGED → `AGENT-037`**（Agent Harness / Runtime） |

`RAG-030` 的全部证据 `S038`, `S059`, `S132`, `S145`, `S218` 都已经包含在 `AGENT-037` 的证据集合中，而且两题共享完全相同的核心知识模型：Coding Agent 如何理解 / 检索大型 Repository，以及 Vector RAG、AST/LSP、ripgrep / Filesystem Search 等机制如何分工。继续保留两题会重复计频，因此以 Agent Runtime 的 Repository Understanding 作为唯一 Primary。

---

## 8. 新体系下的 RAG 主干

```text
Corpus Audit / Parsing
        ↓
Chunking Principles / Strategy / Parameters
        ↓
Query Transformation
        ↓
Dense + Sparse / Hybrid / Fusion / Rerank / Top-K
        ↓
Context Construction / Grounding
        ↓
Retrieval + E2E Evaluation / Bad-case Attribution
        ↓
Freshness / Permission / Scale / Cost
        ↓
GraphRAG / Agentic RAG
```

Codebase Retrieval / Repository Understanding 的 Primary 已统一归 `Agent Harness / Runtime`，RAG 只作为其中的 Related Module。