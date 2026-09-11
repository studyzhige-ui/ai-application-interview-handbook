# Curriculum Granularity Audit

更新日期：2026-09-11

> 本文件解决一个长期问题：**研究粒度、面试题粒度、能力粒度、教材文件粒度不是同一个层级。**

## 1. 四种粒度必须分开

```text
HUMAN-A / Canonical Question = 面试能力最小可独立追问单元
Capability Map = Runtime / Backend / Data System 的能力 primitive
教材文件 = 一个可以独立学习、复习、画图、解释 failure/trade-off 的知识小板块
文件内 Section = 机制、参数、变体、failure case、追问等更细知识点
```

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

优先合并：只是参数/变体、背景大量重复、必须读下一篇才能解释当前篇、只有短提纲、或仅因面试官能分别追问而拆开。

文件大小只是审计信号，不是硬指标。

---

# 3. 最终整改结果


## Python — COMPLETE：12 → 13

Python v1 原 12 章 beginner-first 主干保持不变，只新增一个真正独立的 `Structured Data / JSON / Validation` 知识闭环；Language Choice、dict 底层、Slicing、Duck Typing、asyncio Failure / Synchronization 等最新 Canonical 通过加深原章节吸收。因此 **15 道 Canonical → 13 个教材知识块**，没有按题目机械增章。


## MySQL — PASS：23 → 23

B+Tree、Composite Index、MVCC、Lock、Replication、Sharding 等有独立数据结构、执行机制和 Failure Model，不为统一数字机械合并。

## Redis — COMPLETE：27 → 24

合并：

```text
Redis 为什么快 + Event Loop / I/O → Runtime & Performance Model
Cache / Key Design + 穿透/击穿/雪崩 → Cache Design & Failure Patterns
Distributed Lock Basics + Correctness → Acquire / Lease / Renewal / Failover / Fencing
```

保留 MULTI/WATCH、Pipeline、Lua / Functions 独立，因为三者解决执行连续性/乐观并发、网络 RTT、服务器端原子逻辑，Failure Model 不同。

## Vector DB — COMPLETE：23 → 16

```text
Vector + Normalization + Similarity → Vector Space & Similarity
Exact Search + Why ANN → Exact vs ANN
HNSW Principle + Parameters → HNSW Mechanism & Tuning
Write/Delete + Compaction + Re-embedding/Rebuild → Vector Index Lifecycle
Performance/Capacity + Troubleshooting → Performance & Production Diagnosis
```

## LLM Foundation — COMPLETE：29 → 14

机制链按 Token/Context、Transformer、Attention/Position、Generation、KV/Prefill/Decode、Serving、Model API/Selection、Embedding/Reranker、Multimodal、Prompt、Factuality、Fine-tuning、Post-training 等完整闭环组织。

## RAG — COMPLETE：34 → 14

最终按 Production 子系统组织：

```text
01 RAG Role & End-to-End Pipeline
02 Corpus Governance
03 Document Processing
04 Chunking Design
05 Advanced Chunk Structure & Data Model
06 Query Understanding & Retrieval Planning
07 Retrieval Stack
08 Rerank & Candidate Budget
09 Evidence Delivery
10 Retrieval Evaluation
11 End-to-End Quality Engineering
12 Production Governance
13 Scale / Cost / Cache / Observability
14 GraphRAG / Agentic RAG
```

## Agent Harness / Runtime — COMPLETE：47 → 23

旧 47 章主要沿 Capability Primitive 切分，已经物理迁移为 23 个知识小板块；旧碎片文件和 rewrite checkpoint 已删除。

随后又完成第二轮**正文深度验收**：旧短稿合并形成的 08–23 已全部重写，01–07 抽查通过。正式正文要求：

```text
为什么存在
→ Runtime Mental Model
→ 正常执行路径
→ State / Protocol / Data Structure
→ Failure Timeline
→ Recovery / Idempotency / Cancellation
→ Security / Permission
→ Observability / Evaluation
→ HUMAN-A / Source Evidence
→ 面试回答 / 自测
```

正式主线：

```text
Agent / Workflow / Harness
→ Loop / Event / State
→ Tool Runtime
→ Planning / Stop / Budget
→ Context Assembly / Compaction
→ Memory / State / Long-running Reliability
→ Permission / Sandbox / Injection / Containment
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping
```

## System Design — COMPLETE：24 Canonical → 19 curriculum blocks

System Design 的 24 道 Canonical 全部是 L4 Scenario，但没有采用 `24 题 = 24 文件`。最终结构是：

```text
12 个通用设计知识块
+ 7 个综合 Scenario Pattern
= 19 个教材文件
```

前 12 章按 `Requirement → SLO → Capacity → State → Flow → Scale → Correctness → Reliability → Security → Verification` 的知识依赖建立；后 7 章再把 Flash Sale、Feed、Migration、LLM Gateway、Enterprise RAG、Production Agent 等真人场景映射进去。

这验证了本审计的核心规则：**Scenario 可以很多，但教材应先教可迁移的方法，再用 Scenario 验证迁移能力。**

---

# 4. 当前教材结构总览

| 模块 | 原结构 | 当前结构 | 状态 |
|---|---:|---:|---|
| Python | 12 | 13 | ✅ COMPLETE |
| MySQL | 23 | 23 | ✅ PASS |
| Redis | 27 | 24 | ✅ COMPLETE |
| Vector DB | 23 | 16 | ✅ COMPLETE |
| LLM Foundation | 29 | 14 | ✅ COMPLETE |
| RAG | 34 | 14 | ✅ COMPLETE |
| Agent Harness | 47 | 23 | ✅ COMPLETE（结构 + 深度） |
| System Design | 24 Canonical | 19 | ✅ COMPLETE |

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

教材重组只回答：**这些知识最适合放进几个教学文件。**

---

# 6. System Design 验证结果

System Design 已按本轮规则完成，并验证这套方法可以直接用于 Scenario-heavy 模块：

```text
先画知识依赖与子系统边界
→ 12 个通用设计知识块
→ 7 个综合场景知识块
→ 最后映射 24 道 System Design Canonical 和真实追问
```

最终为 **19 blocks**，没有出现“一题一章”后再返工合并的问题。未来新增模块继续沿用同一方法。
