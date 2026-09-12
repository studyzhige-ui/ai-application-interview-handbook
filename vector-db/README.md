# Vector Database｜向量检索与索引系统

[← Redis](../redis/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [LLM Foundation（应用工程深度） →](../llm-foundation/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：16 个连续知识小板块** · **HUMAN-A Canonical：12** · **独立来源覆盖：37**  
> **质量：Granularity / Coverage / Content Depth 已验收**

理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。

---

## 1. 这个模块解决什么

理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。

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

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → **Vector Database** → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent Harness / Runtime](../agent-harness/README.md) → [System Design](../system-design/README.md)

当前模块角色：**Data / 理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。**

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

所以本模块是 **12 道 Canonical → 16 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Vector Space / Similarity → Exact vs ANN → HNSW / IVF / Quantization / Index Selection → Schema / Filter / Tenant → Index Lifecycle / Distributed → Performance Diagnosis / Product Boundary
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜Vector Space 与 ANN 基础

1. [Vector DB 在 AI Application 中负责什么](docs/01-VectorDB在AI应用中的职责.md)
2. [Vector Space & Similarity：Dimension、Normalization、Cosine / Dot / L2](docs/02-VectorSpace与Similarity.md)
3. [Exact Search vs ANN：Top-K Ground Truth 与 Recall / Latency](docs/03-ExactSearch与ANN.md)

### Part B｜ANN Index

4. [ANN Index 谱系：Graph、Partition、Quantization](docs/04-ANN索引谱系.md)
5. [HNSW：机制、M、efConstruction、efSearch 与调优](docs/05-HNSW机制与调优.md)
6. [IVF：Coarse Quantizer、nlist 与 nprobe](docs/06-IVF原理.md)
7. [Quantization：SQ / PQ 与压缩检索](docs/07-Quantization与PQ.md)
8. [HNSW vs IVF 与 Index Selection](docs/08-IndexSelection.md)

### Part C｜Data Model、Filter 与 Lifecycle

9. [Collection / Schema / Primary Key / Metadata](docs/09-Vector数据建模.md)
10. [Metadata Filter、Pre-filter 与 Post-filter](docs/10-MetadataFilter.md)
11. [Partition / Namespace / Tenant Isolation](docs/11-Partition与TenantIsolation.md)
12. [Vector Index Lifecycle：写入、删除、Compaction、Re-embedding 与 Rebuild](docs/12-VectorIndex生命周期.md)
13. [Shard / Replica / Segment：分布式 Vector DB](docs/13-分布式VectorDB.md)

### Part D｜Production 与 Architecture Boundary

14. [Performance、Capacity 与 Production Diagnosis](docs/14-性能容量与Production诊断.md)
15. [FAISS / pgvector / Elasticsearch / Milvus / Qdrant 架构选型](docs/15-产品与架构选型.md)
16. [Graph DB vs Vector DB 与系统位置](docs/16-GraphDB边界与系统设计.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **12 道 Primary Canonical、37 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- Vector Storage / Architecture Selection
- HNSW 与参数
- HNSW vs IVF / Index Selection
- Index Lifecycle / Rebuild
- Metadata Filter
- Graph DB vs Vector DB

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- Embedding / Reranker 模型原理归 LLM Foundation。
- Dense / Sparse / Hybrid / RRF / Retrieval Eval 归 RAG。
- Vector DB 负责高效可靠地存和找向量，不负责完整 Retrieval Pipeline。

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

- [Canonical Questions](../research/questions/vector-db.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 16` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–16 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[LLM Foundation（应用工程深度）](../llm-foundation/README.md)。
