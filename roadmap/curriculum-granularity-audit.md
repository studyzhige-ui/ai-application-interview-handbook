# Curriculum Granularity Audit

更新日期：2026-09-11

> 本文件解决一个长期问题：**研究粒度、面试题粒度、能力粒度、教材文件粒度不是同一个层级。**

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

不再使用 `1 Canonical ≈ 1 Capability ≈ 1 Markdown` 作为默认映射。

---

## 2. 独立成文件的判断标准

一个主题至少应满足以下大部分条件，才适合作为单独 Markdown：

1. 能回答一个独立“大问题”；
2. 有自己的前置知识和输出心智模型；
3. 有区别于相邻主题的 Failure Model / Trade-off；
4. 学完后可以独立画出流程图、状态机或数据结构；
5. 可以形成“为什么 → 怎么工作 → 哪里会坏 → 怎么验证”的闭环；
6. 与相邻文件合并后不会只是机械变长，而会形成更自然的因果关系。

优先合并的信号：

- 一个文件只是另一个文件的参数或变体；
- 必须读下一篇才能回答当前篇的“为什么”；
- 大量重复相同背景；
- 单文件长期只有短提纲；
- 只是因为面试官可以分别追问而拆开。

文件大小只是审计信号，不是硬指标。

---

# 3. 最终整改结果

## MySQL — PASS：23 → 23

MySQL 的 B+Tree、Composite Index、MVCC、Lock、Replication、Sharding 等本身有独立数据结构、执行机制和 Failure Model，因此不为统一数字机械合并。

## Redis — COMPLETE：27 → 24

实际阅读正文后，对最初审计做了修正。

真正合并：

```text
Redis 为什么快
+ I/O Multiplexing / Event Loop
→ Redis Runtime & Performance Model

Cache / Key Design
+ Penetration / Breakdown / Avalanche
→ Cache Design & Failure Patterns

Distributed Lock Basics
+ Lock Correctness
→ Acquire / Owner / Lease / Renewal / Failover / Fencing
```

保留独立：

```text
MULTI / WATCH
Pipeline
Lua / Functions
```

因为三者分别解决执行连续性/乐观并发、网络 RTT、服务器端原子逻辑，Failure Model 不同。

**结论：24 是比预估 23 更合理的结构。**

## Vector DB — COMPLETE：23 → 16

已完成核心合并：

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

Insert / Update / Delete
+ Tombstone / Compaction
+ Re-embedding / Rebuild
→ Vector Index Lifecycle

Performance Metrics / Capacity
+ Production Troubleshooting
→ Performance & Production Diagnosis
```

保留 ANN Taxonomy、IVF、Quantization、Index Selection、Metadata Filter、Tenant Isolation、Distributed Vector DB、Product Selection 等独立闭环。

## LLM Foundation — COMPLETE：29 → 14

已按机制链收敛：

```text
Tokenization + Context Budget + Long Context
Transformer Architecture + FFN / Residual / Norm
Attention / QKV + Multi-head / Causal + RoPE
Autoregressive Generation + Logits + Sampling
KV Cache + Prefill / Decode
Continuous Batching + PagedAttention + Latency / Cost + Precision
Model API + Model Selection
Embedding + Reranker
Multimodal
Prompt Engineering
Hallucination + Prompt/RAG/Fine-tuning Boundary
SFT + LoRA / PEFT
Post-training / Alignment / Distillation
```

课程不再把 Logits、Sampling、Prefill、PagedAttention 等子机制默认拆成独立文件。

## RAG — COMPLETE：34 → 14

最终按 Production 子系统组织：

```text
01 RAG Role & End-to-End Pipeline
02 Corpus Governance
03 Document Processing
04 Chunking Design
05 Advanced Chunk Structure & Data Model
06 Query Understanding & Retrieval Planning
07 Retrieval Stack: Dense / Sparse / Hybrid / Fusion
08 Rerank & Candidate Budget
09 Evidence Delivery: Context / Grounding / Citation
10 Retrieval Evaluation
11 End-to-End Quality Engineering
12 Production Governance: Freshness / Version / Permission
13 Scale / Cost / Cache / Observability
14 GraphRAG / Agentic RAG
```

29 道 RAG Canonical 和 40 道面试题仍保持更细粒度，不跟教材文件数量绑定。

## Agent Harness / Runtime — STRUCTURE COMPLETE：47 → 23

旧 47 章主要沿 Capability Primitive 切分，已完成物理迁移为 23 个知识小板块；旧碎片文件删除。

当前剩余任务不是继续缩章，而是**正文深度验收**：部分由旧短稿合并来的 08–23 仍需提升到 MySQL / RAG 同级教学深度。

正式主线：

```text
Agent / Workflow / Harness
→ Loop / Run / Turn / Step / Event
→ Tool Runtime
→ Planning / Goal / Stop / Budget
→ Context Assembly / Compaction
→ Memory / State / Long-running Reliability
→ Permission / Sandbox / Injection / Containment
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping
```

---

# 4. 当前教材结构总览

| 模块 | 原结构 | 当前结构 | 粒度状态 |
|---|---:|---:|---|
| MySQL | 23 | 23 | ✅ PASS |
| Redis | 27 | 24 | ✅ COMPLETE |
| Vector DB | 23 | 16 | ✅ COMPLETE |
| LLM Foundation | 29 | 14 | ✅ COMPLETE |
| RAG | 34 | 14 | ✅ COMPLETE |
| Agent Harness | 47 | 23 | ✅ STRUCTURE COMPLETE；🚧 深度验收 |

这些数字是结果，不是目标。不同模块保留不同文件数量是正常现象。

---

# 5. 重组不改变研究事实

任何教材 Merge / Rename 都不得改变：

- HUMAN-A `S001–S279`；
- 235 ACTIVE Canonical；
- Primary Module Ownership；
- Source Count；
- Verified Follow-up Chain；
- Frequency Ranking。

教材重组只回答：

> **这些知识最适合放进几个教学文件？**

---

# 6. System Design 的固定规则

System Design 开始前直接使用这套方法：

```text
先画知识依赖与子系统边界
→ 确定知识小板块
→ 再决定 Markdown 文件
→ 最后映射 24 道 System Design Canonical 和真实追问
```

禁止再先按问题清单生成几十个 Markdown，再事后合并。
