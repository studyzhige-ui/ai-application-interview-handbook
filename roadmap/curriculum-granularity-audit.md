# Curriculum Granularity Audit

更新日期：2026-09-11

> 本文件解决一个长期问题：**研究粒度、面试题粒度、能力粒度、教材文件粒度不是同一个层级。**
>
> 后续所有一级模块都必须先决定“知识体系里的小板块”，再决定文件；不能因为 Canonical Question 可以独立追问，就自动拆成独立 Markdown。

## 1. 四种粒度必须分开

```text
HUMAN-A / Canonical Question
= 面试能力最小可独立追问单元

Capability Map
= Runtime / Backend / Data System 的能力 primitive

教材文件
= 一个可以独立学习、复习、画图、解释 failure/trade-off 的知识小板块

文件内 Section
= 机制、参数、变体、failure case、追问等更细知识点
```

因此：

> **Canonical 可以很细，Capability Map 可以更细，但教材文件必须按“认知闭环”组织。**

不能使用：

```text
1 Canonical Question
≈ 1 Capability
≈ 1 Markdown File
```

作为默认映射。

---

## 2. 一个知识点什么时候应该单独成文件

至少满足以下大部分条件：

1. 能回答一个独立的“大问题”；
2. 有自己的前置知识和输出心智模型；
3. 有区别于相邻主题的 failure model / trade-off；
4. 学完后可以独立画出流程图 / 状态机 / 数据结构；
5. 可以形成完整的“为什么 → 怎么工作 → 哪里会坏 → 怎么验证”；
6. 与相邻文件合并后不会只是机械变长，而会形成更自然的因果闭环。

反过来，如果两个文件满足下面任一情况，优先合并：

- A 文件几乎只是 B 文件的参数 / 变体；
- 必须读完下一文件才能回答当前文件的“为什么”；
- 两个文件大量重复同一背景与定义；
- 单文件长期只有约 3–5KB，内容主要是提纲而不是完整教学闭环；
- 只是因为真人面经可以分别追问而拆开。

> 文件大小不是硬指标，只是审计信号。复杂主题 15–25KB 很正常；真正重要的是认知闭环。

---

## 3. 已完成模块审计

### MySQL — PASS

当前：23 章。

特征：

- 正文章节普遍约 9–14KB；
- `B+Tree`、`Composite Index`、`MVCC`、`Lock`、`Replication`、`Sharding` 等都有独立数据结构 / failure model；
- 三条主线清晰：查询性能、并发正确性、生产扩展。

结论：**不因为其它模块缩章而机械改 MySQL。** 当前文件粒度基本符合“知识小板块”。

### Redis — MINOR REMEDIATION

当前：27 章，多数约 5–7KB。

明显可合并候选：

```text
06 Redis 为什么快
+ 07 I/O Multiplexing / Event Loop
→ Redis Runtime / Performance Model

17 MULTI / WATCH
+ 18 Pipeline
+ 19 Lua / Functions
→ Command Batching / Transaction / Atomic Programmability

20 Distributed Lock Basics
+ 21 Lock Correctness
→ Distributed Lock：从 Acquire 到 Lease / Renewal / Fencing
```

其它如 TTL vs Eviction、Replication vs Sentinel vs Cluster 仍有独立 failure model，应保留。

目标：**27 → 23 左右**，属于轻度整理，不推倒重写。

### Vector DB — MODERATE REMEDIATION

当前：23 章，多数约 4–5KB，存在明显“一个算法子概念一个文件”。

推荐合并：

```text
Vector + Dimension
+ Normalization
+ Similarity / Distance
→ Vector Space & Similarity

Top-K Exact Search
+ Why ANN
→ Exact Search vs ANN

HNSW Principle
+ HNSW Parameters
→ HNSW：Mechanism + Tuning

Insert/Update/Delete
+ Tombstone/Compaction
+ Re-embedding/Index Lifecycle
→ Vector Index Lifecycle

Performance Metrics/Capacity
+ Production Troubleshooting
→ Performance & Production Diagnosis
```

目标：**23 → 16–18**。

### LLM Foundation — MODERATE REMEDIATION

当前：29 章，多数约 3–6KB。知识顺序正确，但文件边界偏细。

推荐把机制链重新组合：

```text
Tokenization + Context Budget + Long Context
Transformer Block + FFN/Residual/Norm
Attention/QKV + Multi-head/Causal + RoPE
Autoregressive Generation + Logits + Sampling
KV Cache + Prefill/Decode
Continuous Batching + PagedAttention + Latency/Cost + Precision
Model API + Model Selection
Embedding + Reranker（Multimodal 可独立）
Hallucination + Prompt/RAG/Fine-tuning Boundary
SFT + LoRA + Post-training/Distillation
```

目标：**29 → 14–17**。

### RAG — MAJOR REMEDIATION

当前：34 章，多数约 2.6–4.6KB。知识体系顺序是对的，但文件明显接近 Canonical / mechanism 粒度。

推荐按 Pipeline 子系统组合：

```text
RAG Role + End-to-end Pipeline
Corpus Audit + Identity/Lineage
Parsing/OCR + Layout/Multimodal + Cleaning/Dedup
Chunking Principles + Strategy + Size/Overlap
Parent-child/Neighbor + Semantic Boundary + Chunk Data Model
Request Lifecycle + Rewrite/Clarification + Decomposition + No-hit
Dense + Sparse/BM25 + Hybrid + Fusion
Rerank + Top-K/Candidate Budget
Context Construction + Grounding/Citation
Retrieval Metrics + Eval Dataset/Judge
End-to-end Eval + Experiment/Regression + Bad Case Attribution
Freshness/Version + Permission/Tenant
Scale/Cost/Observability
GraphRAG/Agentic RAG
```

目标：**34 → 14–16**。

这里的整改只改变教材文件粒度，不改变 29 道 RAG Canonical、Source Count 或市场分析。

### Agent Harness / Runtime — MAJOR REMEDIATION NOW

旧目录：47 章。

问题最明显：目录基本沿 Capability Primitive 切分；旧短稿 19–47 只有约 1.4–1.8KB，说明很多更适合作为章节内 section。

正式目标：**23 个知识小板块**。

详见 `agent-harness/README.md`。

---

## 4. 整改优先级

```text
Agent Harness     P0  现在重组，继续正文前先解决
RAG               P1  Agent 完成后回头合并
LLM Foundation    P1  与 RAG 同批整理
Vector DB         P2  中度整理
Redis             P2  轻度整理
MySQL             PASS
```

原则：先修结构，再继续新增 System Design，避免把错误的文件粒度复制到最后一个模块。

---

## 5. 重组不改变研究事实

任何教材 Merge / Rename 都不得改变：

- HUMAN-A `S001–S279`；
- 235 ACTIVE Canonical；
- Primary Module Ownership；
- Source Count；
- Verified Follow-up Chain；
- Frequency Ranking。

它只改变：

```text
“这些知识应该放进几个教材文件里？”
```

而不改变：

```text
“市场问了哪些独立能力？”
```

---

## 6. 后续模块的固定规则

System Design 开始前必须先应用本规则：

> **先画知识依赖与子系统边界 → 再确定文件 → 最后才把 Canonical / 面经追问映射进去。**

不再先按问题清单建 30–50 个 Markdown，再事后合并。