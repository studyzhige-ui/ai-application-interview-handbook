# RAG｜检索增强生成工程

[← LLM Foundation（应用工程深度）](../llm-foundation/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [Agent →](../agent/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：14 个连续知识小板块** · **HUMAN-A Canonical：29** · **独立来源覆盖：88**  
> **质量：Granularity / Coverage / Content Depth 已验收**

把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。

---

## 1. 这个模块解决什么

把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。

学习目标不是记住一组名词，而是能稳定回答：

```text
为什么需要它？
→ 核心机制怎样工作？
→ 正常路径怎样流动？
→ Failure / Trade-off 在哪里？
→ Production 场景怎样验证与排障？
→ 面试官继续追问时怎样解释边界？
```

---

## 2. 在十板块中的位置

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → **RAG** → [Agent](../agent/README.md) → [System Design](../system-design/README.md)

当前模块角色：**AI Application / 把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。**

---

## 3. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

同时固定区分：

```text
Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 一个完整认知闭环
Section = 参数 / 变体 / Failure / 深挖追问
```

所以本模块是 **29 道 Canonical → 14 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Corpus Governance → Document Processing → Chunk Design → Query Planning → Dense / Sparse / Hybrid / Fusion → Rerank / Candidate Budget → Evidence / Grounding / Citation → Retrieval & E2E Evaluation → Production Governance / Scale → GraphRAG / Agentic RAG
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜Knowledge Ingestion

1. [RAG 的职责与 Production End-to-End Pipeline](docs/01-RAG职责与完整链路.md)
2. [Corpus Governance：Audit、Identity、Lineage、Version、Source of Truth](docs/02-CorpusGovernance.md)
3. [Document Processing：Parsing、OCR、Layout、Multimodal、Cleaning、Dedup](docs/03-DocumentProcessing.md)

### Part B｜Retrieval Unit

4. [Chunking Design：原则、Strategy、Size、Overlap](docs/04-ChunkingDesign.md)
5. [Advanced Chunk Structure：Parent-child、Neighbor、Boundary、Data Model](docs/05-AdvancedChunkStructure.md)

### Part C｜Query → Candidate → Evidence

6. [Query Understanding & Retrieval Planning](docs/06-QueryPlanning.md)
7. [Retrieval Stack：Dense、BM25、Hybrid、Fusion](docs/07-RetrievalStack.md)
8. [Rerank 与 Candidate Budget](docs/08-Rerank与CandidateBudget.md)
9. [Context Construction、Grounding 与 Citation](docs/09-EvidenceDelivery.md)

### Part D｜Quality Engineering

10. [Retrieval Evaluation：Metrics、Ground Truth、Dataset、Judge](docs/10-RetrievalEvaluation.md)
11. [End-to-End Evaluation、Ablation、Regression 与 Bad Case](docs/11-EndToEndQualityEngineering.md)

### Part E｜Production Governance 与 Advanced RAG

12. [Production Governance：Freshness、Version、Permission、Tenant、Rollback](docs/12-ProductionGovernance.md)
13. [Large-scale Ingestion、Latency / Cost、Cache 与 Observability](docs/13-ScaleCostObservability.md)
14. [GraphRAG、Agentic RAG 与 Production Architecture](docs/14-GraphRAG与AgenticRAG.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **29 道 Primary Canonical、88 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- End-to-end Pipeline
- Chunk Strategy
- Hybrid Retrieval
- Reranking
- End-to-end Evaluation
- Bad Case Attribution
- Query Transformation

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- Embedding / Reranker 内部原理归 LLM Foundation。
- ANN / HNSW / IVF / Filter 存储机制归 Vector DB。
- Agentic Retrieval 的控制循环归 Agent Harness；RAG 负责 Evidence Quality。

遇到跨模块问题时，正文会保留必要桥梁，但完整机制只在 Primary Module 维护一份。

---

## 8. Review、Interview 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |
| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |
| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |
| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |

研究与质量证据：

- [Canonical Questions](../research/questions/rag.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 14` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–14 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[Agent](../agent/README.md)。
