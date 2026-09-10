# Knowledge Gap Analysis — Market Evidence × Curriculum Roadmap

更新日期：2026-09-11

> 本文件把冻结 `S001–S279` 真人面经形成的 **235 ACTIVE Canonical** 与 `roadmap/knowledge-map.md` 对照。目标不是让课程变成题库，而是区分四类情况：
>
> 1. **市场高频但课程缺失 / 表述过弱**：需要补；
> 2. **课程已有但模块边界与 Canonical 不一致**：需要重排；
> 3. **面试低频但属于必要知识前置**：保留，不因为低频删除；
> 4. **岗位 / 语言相关信号**：做 Optional / Role-dependent，而不是强塞主线。

## 1. 总结结论

当前课程主方向是对的，但存在一个 **P0 结构缺口** 和若干 **P1 内容缺口**：

- `roadmap/knowledge-map.md` 的正式主学习路线里**缺少 LLM Foundation（应用工程深度）一级模块**；
- Vector DB 路线仍把 Dense/Sparse、BM25、Hybrid、RRF、Rerank 混在 Vector DB 中，与最新 Primary Ownership 不一致；
- Agent Harness 路线尚未显式吸收 Phase 2B 新增的 Prompt Injection、Intent Routing、A2A、Framework Selection、AI-assisted Development Workflow；
- MySQL / Redis / RAG 的完整课程骨架已经覆盖大多数核心方向，但若按真人面试深度，需要强化 Failure / Scale / Evaluation；
- Python / FastAPI 的市场直接命中不高，但它们是完整 AI Application Engineering 的必要前置，不能按热度裁掉。

自动统计基线：

| Module | Canonical | Unique HUMAN-A Sources | >=10-source Qs | L4 Qs |
|---|---:|---:|---:|---:|
| Python | 15 | 15 | 0 | 0 |
| FastAPI | 4 | 3 | 0 | 1 |
| AI Backend Engineering | 39 | 125 | 12 | 16 |
| MySQL | 26 | 55 | 6 | 6 |
| Redis | 19 | 69 | 7 | 8 |
| Vector DB | 12 | 37 | 4 | 5 |
| LLM Foundation（应用工程深度） | 23 | 82 | 4 | 1 |
| RAG | 29 | 88 | 16 | 20 |
| Agent Harness / Runtime | 44 | 166 | 30 | 35 |
| System Design | 24 | 71 | 3 | 24 |

---

## 2. P0：Roadmap 缺少 LLM Foundation 一级模块

### 当前问题

`roadmap/knowledge-map.md` 当前总结构和推荐路线是：

```text
Python
→ FastAPI
→ AI Backend Engineering
→ MySQL
→ Redis
→ Vector Database
→ RAG
→ Agent Harness / Runtime
→ System Design
```

但正式 Canonical Schema 已经是十板块，并明确要求：

```text
Python
→ FastAPI
→ AI Backend Engineering
→ MySQL
→ Redis
→ Vector DB
→ LLM Foundation（应用工程深度）
→ RAG
→ Agent Harness / Runtime
→ System Design
```

### 为什么这是 P0，而不是“可选补充”

LLM Foundation 已有：

- **23** 道 Canonical；
- **82** 个独立 HUMAN-A 来源；
- Prompt Engineering：**30** 个来源；
- Hallucination / Factuality：**10**；
- Model Selection：**10**；
- Transformer Architecture：**10**；
- Fine-tuning：**9**；
- Post-training / Alignment：**8**；
- Context Window / QKV / Embedding Model 等也持续出现。

它不是训练算法岗的“模型理论课”，而是解释下面这些工程行为所必需的应用深度：

```text
Token / Context 为什么这样增长？
Attention / KV Cache 为什么影响延迟？
Temperature / Top-p 为什么改变行为？
Embedding 与 Reranker 为什么不是一类模型？
RAG 与 Fine-tuning 为什么有边界？
Prompt 为什么需要 Evaluation？
```

### 修复建议

在 Vector DB 与 RAG 之间正式新增：

```text
07 LLM Foundation（应用工程深度）
08 RAG
09 Agent Harness / Runtime
10 Production System Design
```

并把 Prompt Engineering 作为该模块的高优先级章节，而不是散落在 RAG / Agent 里。

---

## 3. P0：Vector DB 与 RAG 的课程边界仍旧混杂

### Roadmap 当前 Vector DB 主线包含

```text
Dense / Sparse
BM25
Hybrid Retrieval
RRF / Score Fusion
Reranker
```

### 最新 Canonical Ownership

这些能力如果问的是**完整 Retrieval Strategy**，Primary 已经统一归 RAG：

- Dense vs Sparse / BM25 → `RAG-012`
- Hybrid Retrieval → `RAG-013`
- RRF / Fusion → `RAG-014`
- Reranking Pipeline → `RAG-015`
- Top-K → `RAG-016`
- Retrieval Metrics → `RAG-020`

Vector DB 应集中在：

```text
Vector Space / Similarity
Exact vs ANN
HNSW / IVF
Index Selection
Index Parameters
Metadata Filtering
Vector Data Modeling
Index Lifecycle / Freshness
Product / Architecture Selection
```

### 修复建议

Roadmap 中把“检索策略”从 Vector DB 移到 RAG；Vector DB 只保留**向量基础设施与 ANN Index**。这样教材不会重复讲同一个知识模型，也和 `module-index.md` 一致。

---

## 4. P1：Prompt Engineering 必须成为明确章节

Phase 2B 补漏后，`LLM-023` 有 **30 个独立 HUMAN-A**，排名全库第 8。

真实面试不只问“Prompt 怎么写”，而会追：

```text
目标是什么？
Role / Instruction 怎样组织？
Context 怎样拼？
Few-shot / Positive / Negative Example 什么时候用？
Tool / Output Contract 怎样声明？
模型换了以后 Prompt 是否要适配？
怎样做 Regression / Evaluation？
```

### 课程动作

新增完整章节：

```text
Prompt Anatomy
→ Instruction Hierarchy
→ Context / Example
→ Structured Output / Tool Contract
→ Prompt Versioning
→ Evaluation / Regression
→ Failure / Injection Boundary
```

Prompt Injection 的安全部分不放在这里讲完，转入 Agent Harness 的 Untrusted Context / Permission 模块继续深化。

---

## 5. P1：Agent Harness 需要吸收 Phase 2B 新增五个能力域

最新 Agent Harness：**44 Canonical / 166 独立来源 / 35 个 L4**，是整个市场证据最重的模块。

现有 roadmap 已经有 Loop、Planning、Context、Memory、Tool、MCP、Permission、Checkpoint、Multi-Agent、Evaluation 等主骨架，但下面五块需要显式进入正式目录：

### 5.1 Prompt Injection / Untrusted Context Security

`AGENT-044`：8 个来源。

不能只写一个泛化的 `Security` 节点，应明确：

```text
System Prompt Leakage
Untrusted Retrieved Content
Tool-result Injection
Sensitive Data Exfiltration
High-risk Write / Execute
Permission / Approval / Sandbox
```

### 5.2 Intent Recognition / Routing

`AGENT-045`：11 个来源。

应放进 Planning / Routing 之前：

```text
Rule
→ Small Model
→ LLM Classification
→ Tool-schema / Capability Routing
→ Routing Evaluation
```

### 5.3 A2A / Agent Communication Protocol

`AGENT-046`：6 个来源。

Multi-Agent 不能只讲“多个 Agent 怎么分工”，还要讲：

```text
Sub-agent 内部调用
vs A2A Protocol
vs MCP
vs 普通 RPC / Message
```

以及递归互调、状态传播和失败隔离。

### 5.4 Agent Framework Selection

`AGENT-047`：27 个来源，全库第 15。

LangChain / LangGraph / Spring AI 等不应该成为课程起点，而应该在讲完 Runtime 理论后作为实现映射：

```text
什么时候需要 State Graph？
什么时候普通 Workflow 足够？
什么时候 Framework 抽象反而限制 Production Runtime？
什么时候值得自研？
```

### 5.5 AI-assisted Development Workflow

`AGENT-048`：37 个来源，全库第 3。

这是当前 roadmap 最明显低估的新市场信号之一。需要独立成域：

```text
Requirement
→ Spec / Context
→ Repo Understanding
→ Generation / Modification
→ Test
→ Diff / Review
→ Verification
→ Acceptance / Delivery
```

它与 `AGENT-036 Code Verification` 不是重复：一个管完整人机研发流程，一个专门管生成代码如何证明可交付。

---

## 6. P1：Agent 教材需要强化“Context Correctness”，不只是 Context Length

全库最高频是 `AGENT-009 Context Compaction`：**41** 个来源。

但真实追问已经明显从：

> Context 太长怎么办？

升级到：

```text
System / History / Memory / Tool Result 怎样排序？
什么时机 Compaction？
哪些字段不能压？
Summary 错了怎么发现？
过时 File Summary / Memory 怎样污染后续任务？
Checkpoint / Resume 如何保持 Goal？
```

### 课程动作

Agent Context 至少拆成：

1. Context Assembly
2. Context Budgeting
3. Compaction Strategy
4. Compaction Correctness
5. Large Tool Result / Offloading
6. Memory Interaction
7. Session / Checkpoint Resume

而不是一个“Context Window 管理”章节全部带过。

---

## 7. P1：Evaluation 应成为横向主线

市场证据：

- `AGENT-034 Agent Evaluation`：27
- `AGENT-035 Benchmark Engineering`：12
- `RAG-021 RAG Evaluation`：21
- `RAG-020 Retrieval Metrics`：16
- Prompt Engineering 也反复追 Regression / Evaluation

这说明 Evaluation 不应该只在 RAG 或 Agent 末尾出现一次。

### 建议统一教学模板

每个核心 AI 模块都使用：

```text
Metric 是什么？
Dataset 从哪里来？
Offline 怎么测？
Online 怎么观测？
Bad Case 怎么归因？
改动如何 Regression？
什么指标可能被“优化作弊”？
```

---

## 8. P1：MySQL Roadmap 需要补齐 Scale / Lifecycle

当前 MySQL 主线对 Index / Transaction / MVCC 覆盖很好，但市场还稳定出现：

| Topic | Sources |
|---|---:|
| Isolation Levels | 14 |
| B+Tree | 13 |
| Index Invalidation | 11 |
| Slow SQL / EXPLAIN | 11 |
| Composite Index | 10 |
| Sharding | 10 |
| MVCC | 9 |
| Covering / Back-to-table / ICP | 8 |
| Phantom Read / Locks | 6 |
| Logs | 5 |
| Schema Design | 5 |
| CDC / Data Sync | 4 |
| Deep Pagination | 4 |
| Replication | 3 |
| Primary Key Design | 3 |

### 建议扩展

现有 16 章之后至少增加：

```text
Index Invalidation / Lifecycle
Primary Key Design
Replication
Sharding
CDC / Data Sync
Bulk Write
Deadlock / Concurrent Transaction Case
```

MySQL + Redis Consistency 的完整系统语义仍以 `AI Backend Engineering / AIBE-020` 为 Primary，MySQL 章节只讲自己那部分机制。

---

## 9. P1：Redis Roadmap 已接近完整，但应加入 HA / Cluster / Multi-level Cache

市场高频：

- Distributed Lock Basics：25
- Cache Failure Patterns：20
- Data Structures：18
- Lock Correctness：14
- BigKey / HotKey：11
- Session / Conversation：11
- Lua / Atomicity：10
- High Availability：8
- Rate Limit Implementation：8
- Performance / Thread Model：7
- TTL：7
- Multi-level Cache：6
- Cluster / Hash Slot：5

### 课程动作

现有主线基础上显式补：

```text
Primary / Replica / Sentinel / Cluster
Hash Slot / Reshard
Multi-level Cache
Semantic / Result Cache
Security Boundary
```

其中 Agent Checkpoint 的 Runtime 语义仍归 Agent Harness；Redis 只解释作为 State Store 时的存储与一致性机制。

---

## 10. P1：RAG Roadmap 需要更明确的 Failure / Evaluation 路径

现有 RAG 路线整体已经正确，但真实面试深度很高：29 道里 **20 道是 L4**。

建议把现有主线明确扩成：

```text
Parse / OCR / Layout
→ Chunk Strategy / Parameter
→ Query Rewrite / Clarification
→ No-hit / Refusal Boundary
→ Dense / Sparse / Hybrid
→ RRF / Fusion
→ Rerank / Top-K
→ Retrieval Metrics
→ End-to-end Evaluation
→ Bad Case Attribution
→ Citation / Grounding
→ Permission / Freshness / Version
→ Incremental Update
→ Agentic RAG
```

特别不能漏掉：

- “Rerank 反而变差”怎样定位；
- Retrieval Miss 何时拒答 / 澄清；
- Parsing / Chunk / Retrieval / Prompt / Generation 怎么分层归因；
- 参数为什么这样设，是否有 Dataset / Experiment 证明。

---

## 11. P2：AI Backend 的 Java / Go 信号应做 Role-dependent Bridge

AI Backend Engineering 有 **125** 个独立来源，是第二大的工程底座。

真人面经里出现：

- JVM Runtime：12
- Java Concurrency：8
- ThreadLocal：8
- Java Collection：7
- Java / Spring：6
- Go Runtime：8

但用户主学习体系仍以 Python / AI Application 为中心，因此不建议把完整 Java / Go 教材硬塞进核心路线。

### 推荐做法

增加一个：

```text
Role-dependent Backend Bridge
├── Java/JVM 面试最小闭环
├── Spring / ThreadPool / Concurrent Collection
└── Go GMP / Channel / Mutex
```

目标是能读懂、能解释 AI Backend 面试中的跨语言基础，不把主线变成“全语言后端大全”。

---

## 12. P2：Python / FastAPI 低热度不代表可以删

直接市场证据：

- Python：15 个独立来源；
- FastAPI：3 个独立来源。

远低于 Agent / Backend / RAG，但这并不说明它们不重要。原因是面经通常把语言基础当作前置能力，只有部分场次会明确写出来。

所以继续坚持：

```text
Knowledge Importance != Interview Heat
```

Python 仍保留完整对象模型、函数、容器、迭代器、生成器、Decorator、Context Manager、GIL、asyncio 等；FastAPI 仍保留 ASGI、Dependency、Pydantic、Lifecycle、Streaming、Timeout / Cancellation 等完整 AI Service 路径。

市场数据只用来调整 Review 权重：Python 优先 `asyncio / GIL / Decorator / Generator`；FastAPI 优先 `ASGI / async / Streaming / Runtime Boundary`。

---

## 13. P0：Roadmap 的“真实面经研究状态”已经过时

`knowledge-map.md` 仍写：

> 真实面经研究：持续滚动采集与去重

当前正式口径已经变成：

```text
HUMAN-A S001–S279 已冻结
主动采集停止
235 ACTIVE Canonical
Phase 2B 市场分析完成后进入教材建设 / 知识 Gap 反哺
```

如果不修正，后续对话容易再次错误恢复“继续搜面经”。因此 roadmap 状态必须同步成 Frozen Research Baseline。

---

## 14. 跨模块结构 Gap：课程需要 Bridge Lab，而不是十门互不相干的课

Module 共现最高：

| Module Pair | Shared Flows |
|---|---:|
| RAG ↔ Agent Harness | 59 |
| AI Backend ↔ Agent Harness | 54 |
| AI Backend ↔ Redis | 53 |
| AI Backend ↔ MySQL | 46 |
| LLM Foundation ↔ Agent Harness | 45 |
| AI Backend ↔ System Design | 39 |
| Agent Harness ↔ System Design | 37 |
| LLM Foundation ↔ RAG | 35 |

### 建议在课程中增加 4 个桥接项目

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

这样学习顺序仍然清晰，但不会造成“每个模块单独会，放到真实系统不会串”的问题。

---

## 15. Depth Gap：教材模板必须从“知识解释”升级到“Production Interview”

235 道 Canonical 的 Depth：

- L2：44
- L3：75
- **L4：116**

按 Evidence 加权：

- L2：224
- L3：739
- **L4：1095**

因此几乎所有重点章节都应该使用统一六层模板：

```text
1. Concept：是什么
2. Mechanism：内部怎样工作
3. Trade-off：为什么选它
4. Failure：坏了怎么办
5. Scale：量大 / 多租户 / 长任务怎么办
6. Evaluation / Verification：怎样证明方案有效
```

这比简单增加更多“八股题”更重要。

---

## 16. 建议修订后的正式学习路线

```text
01 Python Foundation
        ↓
02 FastAPI / ASGI AI Service
        ↓
03 AI Backend Engineering
        ↓
04 MySQL
        ↓
05 Redis
        ↓
06 Vector Database / ANN Infrastructure
        ↓
07 LLM Foundation（应用工程深度）
        ↓
08 RAG Engineering
        ↓
09 Agent Harness / Runtime
        ↓
10 Production System Design
```

横向贯穿：

```text
Evaluation / Verification
Reliability / Failure Recovery
Security / Permission
Observability
AI-assisted Development
```

---

## 17. 下一步课程建设优先级

### P0 · 立即修 Roadmap

1. 把 LLM Foundation 补成正式一级模块；
2. 修正 Vector DB / RAG 边界；
3. 把真实面经状态改成 Frozen `S001–S279 / 235 Canonical`；
4. Agent Harness 增加五个 Phase 2B 新能力域。

### P1 · 下一块教材仍然从 MySQL 开始

这次市场分析**不推翻**原定教材建设顺序。Python 已有完整教材，FastAPI / Backend 已有骨架，因此下一块系统正文仍然适合从 MySQL 开始。

但写 MySQL 时要按市场证据重新调整重点：

```text
Index / B+Tree
→ Composite / Covering / Invalidation
→ Slow SQL / EXPLAIN
→ Isolation / MVCC / Lock
→ Deep Pagination
→ Sharding / Scale
→ Logs / Replication / CDC
→ AI Application Data Modeling
```

### P2 · 后续 Redis / Vector DB / LLM / RAG / Agent 顺序建设

每一块教材完成后，都用 `curriculum-evidence-matrix.md` 和 `follow-up-chains.md` 做一次 Coverage Review，保证“完整知识体系”与“真实面试深度”同时满足。
