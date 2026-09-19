# 14｜GraphRAG、Agentic RAG 与 Production Architecture

> 普通 RAG 的默认范式是：**一次 Query → 一次 Retrieval → 一次 Generation**。当问题变成“关系型多跳检索”或“必须根据中间 Evidence 动态决定下一步搜什么”时，系统才自然进入 GraphRAG 和 Agentic RAG。
>
> 本章重点不是追逐名词，而是判断：**什么问题真的需要图？什么问题真的需要 Loop？新增复杂度怎样评估、限制和运维？**

---

## 1. 先把三种问题分开

### 普通 Retrieval 问题

```text
“退款政策是什么？”
```

一次 Hybrid Retrieval + Rerank 可能已经足够。

### Relation / Multi-hop 问题

```text
“哪些服务依赖组件 A，且负责人属于团队 B？”
```

这里需要显式关系约束。

### Dynamic Retrieval 问题

```text
“先找出异常服务，再根据它们的 owner 查询最近变更，并判断最可能原因。”
```

下一步查什么取决于前一步 Evidence。

对应：

```text
Simple RAG
Relation-aware / Graph RAG
Agentic / Iterative RAG
```

不要把三个层级混成“更高级 RAG”。

---

## 2. GraphRAG 解决什么

Vector Retrieval 擅长：

```text
semantic similarity
```

Graph 擅长：

```text
explicit entity / relation / path constraints
```

例如：

```text
Service A --depends_on--> DB X
Service A --owned_by--> Team M
Team M --belongs_to--> Business Y
```

Query：

> “Business Y 中依赖 DB X 的服务有哪些？”

纯向量可以召回相关描述，但 Graph Query 更适合表达：

```text
Entity
→ Relation
→ Constraint
→ Path
```

---

## 3. GraphRAG 不是“把 Chunk 全转成图”这么简单

一条可运营的 Graph Pipeline 至少要考虑：

```text
Document
→ Entity Extraction
→ Entity Resolution / Canonicalization
→ Relation Extraction
→ Provenance Linking
→ Graph Write
→ Validation
→ Version / Update
```

最容易被忽略的是：

```text
Entity Resolution
```

例如：

```text
OpenAI
Open AI
OpenAI Inc.
该公司
```

如果被建成 4 个 Entity，Graph 很快就失真。

反过来，错误 Merge 两个同名实体也同样危险。

---

## 4. Graph 中的 Relation 也需要 Provenance

不要只保存：

```text
A --depends_on--> B
```

还应能回答：

```text
这条 Relation 从哪份文档抽出来？
哪个版本？
哪段 Evidence？
是谁 / 什么模型生成？
置信度多少？
```

可以理解成：

```text
edge
+ source_document_id
+ source_version
+ evidence_chunk_id
+ extraction_version
```

否则 Graph 中一条错误关系会很难审计和回滚。

---

## 5. Graph Retrieval 常见模式

GraphRAG 并不只有一种 Query。

### 5.1 Neighbor Expansion

```text
Entity A
→ 1-hop / 2-hop neighbors
```

适合局部关系探索。

### 5.2 Path Query

```text
A → ? → ? → B
```

适合依赖链、组织关系、供应链等问题。

### 5.3 Constraint Query

```text
service.depends_on = DB-X
AND service.owner.team = Team-B
```

适合结构化关系过滤。

### 5.4 Community / Cluster Summary

先把大图组织成社区或主题，再对群组进行摘要和检索。

更适合：

```text
全局主题 / 跨文档关系问题
```

但 Summary 本身也可能成为新的信息损失层。

---

## 6. Graph Retrieval 最后仍要回到 Evidence

Graph Node / Edge 本身不应该自动成为回答依据。

更安全的链路：

```text
Graph 找到 Entity / Path
→ resolve source evidence
→ retrieve original text / table / record
→ build grounded context
→ answer + citation
```

也就是说：

> **Graph 更像 Retrieval Planner / Structural Index，最终回答仍应尽量回到可验证 Evidence。**

---

## 7. Vector + Keyword + Graph 怎样组合

不是三选一。

例如：

```text
Query
→ Intent / Entity Detection
→ Vector Retrieval 找语义候选
→ Keyword 保证 exact term
→ Graph Expansion 找相关实体 / Path
→ Merge / Rerank
→ Evidence
```

另一种：

```text
Graph 先定位 Entity Set
→ Vector Search 只在该集合相关文档中进行
```

选型由问题结构决定，而不是“Graph 比 Vector 高级”。

---

## 8. GraphRAG 的更新为什么难

普通 Chunk Index 更新可以：

```text
Document v1 delete
→ Document v2 insert
```

Graph 更新还会影响：

```text
Entity
Relation
Alias
Community
Path
Derived Summary
```

例如 Source 删除一条关系：

```text
Edge 是否还有其它 Source 支持？
```

如果有：

```text
不能直接删 Edge
```

因此成熟设计需要：

```text
provenance count / source set
versioned extraction
incremental recompute
```

---

## 9. GraphRAG 的主要 Failure

### Entity Extraction Error

漏实体或识别错误。

### Entity Resolution Error

同一实体被拆开，或不同实体被合并。

### Relation Hallucination

模型生成了原文并不支持的边。

### Stale Graph

文档已更新，Graph 仍是旧关系。

### Over-expansion

多跳之后候选呈指数增长：

```text
1-hop = 20
2-hop = 400
3-hop = 8000
```

### Summary Distortion

Community Summary 把细节压坏。

所以 GraphRAG 同样需要：

```text
Ground Truth
Precision / Recall
Provenance
Version
Cost / Latency
```

---

## 10. GraphRAG 怎样评估

至少分两层。

### Graph Construction Quality

```text
Entity Precision / Recall
Relation Precision / Recall
Entity Resolution Accuracy
Freshness Lag
```

### End-to-end QA

```text
Answer Correctness
Evidence Support
Path Relevance
Citation Correctness
Latency / Cost
```

不能只看：

> “Graph 看起来很丰富。”

如果 Relation Precision 很低，它只是在把错误结构化。

---

# 11. Agentic RAG 是什么

Agentic RAG 把 Retrieval 变成 Runtime 中可重复执行的能力：

```text
Question
→ inspect current state
→ decide retrieval action
→ retrieve
→ inspect evidence
→ rewrite / decompose / switch source
→ retrieve again
→ verify sufficiency
→ stop / refuse / answer
```

核心定义是：

> **下一次 Retrieval 是否发生、搜什么、搜哪个 Source，由当前 Evidence 和 State 动态决定。**

用了 LangGraph、LangChain 或某个 Agent SDK，本身不构成 Agentic RAG。

---

## 12. Agentic RAG 的 Runtime State

不要只保存 Chat History。

可以显式保存：

```text
original_query
current_subquestion
queries_already_tried
evidence_ids
sources_searched
unresolved_claims
step_count
cost_spent
no_new_evidence_count
```

这样才能实现：

```text
Loop Detection
Budget
Replay
Evaluation
```

---

## 13. Evidence Sufficiency：什么时候可以停止搜

最难的不是继续 Search，而是知道什么时候停。

可以从多个信号判断：

```text
required claims 是否都有 Evidence？
Evidence 是否来自允许 Source？
多个 Evidence 是否互相冲突？
Retriever 是否连续多轮没有新增信息？
answer 是否仍依赖 unsupported assumption？
```

一种稳定抽象：

```text
Question
→ Decompose into Claims / Subtasks
→ Evidence coverage per claim
→ all critical claims supported?
       ├─ yes → answer
       └─ no  → retrieve / clarify / refuse
```

而不是让模型凭一句：

> “我觉得信息够了。”

---

## 14. No-new-evidence Detection

Agent 最常见死循环之一：

```text
rewrite A
→ same docs
rewrite B
→ same docs
rewrite C
→ same docs
```

可以检测：

```text
candidate overlap
new evidence count
duplicate citation ids
query similarity
repeated tool route
```

若连续 N 轮没有信息增益：

```text
stop / clarify / refuse
```

这比只设 `max_steps=10` 更有语义。

---

## 15. Query Drift 怎样防

多轮 Rewrite 容易出现：

```text
Original Goal
→ rewritten query
→ rewritten again
→ increasingly different problem
```

因此 Runtime 应一直保留：

```text
original user goal
hard constraints
current subquestion
```

每轮 Retrieval Plan 都可以检查：

```text
current action still serves original goal?
```

这和 Agent Harness 的 Goal Control 是同一个控制思想。

---

## 16. Agentic RAG 的 Cost Budget

一次固定 RAG：

```text
1 rewrite
1 retrieval
1 rerank
1 answer
```

Agentic RAG 可能：

```text
5 planning calls
8 retrievals
4 reranks
2 verification calls
```

所以必须定义：

```text
max retrieval steps
max model calls
max rerank candidates
max token budget
max wall-clock time
```

否则“质量更高”可能只是用 10 倍成本换来的。

---

## 17. Multi-source Routing

Agentic RAG 的真正价值之一是动态选择 Source：

```text
policy docs → Search Index
real-time price → API
customer order → SQL Tool
incident logs → Log Search
service relation → Graph
```

此时 Retrieval 不再等于 Vector DB。

更准确：

```text
Evidence Acquisition
= Search / DB / API / Graph / Tool
```

这也是 RAG 与 Agent Harness 的桥梁。

---

## 18. Agentic RAG Failure Timeline

### Infinite Loop

不断搜索但没有新增 Evidence。

### Query Drift

逐轮偏离用户原问题。

### Cost Explosion

为了一个简单问题触发多次昂贵 Tool / Model。

### Unsupported Stop

Evidence 不足却自己宣布完成。

### Source Selection Error

把实时事实错误地去向量知识库搜，或者本应文档检索却调用高风险业务 Tool。

### Permission Escalation

多 Source Query 中某一路没有正确应用 ACL。

因此必须同时有：

```text
Stop Policy
Budget
Permission
Trace
Evaluation
```

---

## 19. Agentic RAG 怎样评估

不能只看最终回答。

还应观察：

```text
Task Success
Evidence Support
Retrieval Steps
Useful Evidence Gain / Step
Duplicate Retrieval Rate
Source Routing Accuracy
Refusal Accuracy
Latency
Cost
```

可以比较：

```text
Fixed RAG Baseline
vs
Agentic RAG
```

如果最终质量只提高 1%，但成本增加 5 倍、P95 翻倍，未必值得。

---

## 20. 什么时候不应该用 GraphRAG / Agentic RAG

### 不需要 GraphRAG

如果问题主要是：

```text
语义查找某段政策 / FAQ
```

Graph Build 可能没有收益。

### 不需要 Agentic RAG

如果：

```text
一次 Hybrid + Rerank 已稳定覆盖 Evidence
```

固定 Pipeline 更：

```text
低延迟
低成本
易评估
易 Debug
```

系统复杂度必须有可验证收益才能引入。

---

## 21. Production Architecture

```text
                           ┌─ Vector / Sparse Search
                           ├─ Graph Retrieval
User Query                 ├─ SQL / API Tool
    ↓                      └─ External Search
Query / Task Planner                  ↑
    ↓                                 │
Evidence Acquisition Router ──────────┘
    ↓
Evidence Store / Runtime State
    ↓
Sufficiency / Verification
    ├─ insufficient → next retrieval action
    ├─ conflicting  → verify / clarify
    └─ sufficient   → grounded answer

横向：
Permission / Budget / Trace / Eval / Version
```

这里的 RAG 层负责：

```text
Evidence Quality
Retrieval Strategy
Grounding / Citation
Retrieval Evaluation
```

Agent Harness 负责：

```text
Loop
State
Tool Runtime
Budget
Checkpoint
Permission
Cancellation
```

---

## 22. 🎯 30 秒回答

> GraphRAG 适合显式关系和多跳约束，它把 Entity/Relation 当成结构化检索索引，但必须做 Entity Resolution、Relation Provenance、Version 和图构建质量评估，并最终回到原始 Evidence。Agentic RAG 则把 Retrieval 变成 Agent Loop 中的动态动作，运行时根据当前 Evidence 决定继续搜索、换 Source、停止或拒答。Production 中必须有 Evidence Sufficiency、No-new-evidence、Step/Cost Budget、Permission 和完整 Trace，并用固定 RAG 作为 Baseline 证明复杂度真的带来收益。

---

## 23. ⚠️ 易错点

- **“GraphRAG 一定比 Vector RAG 好。”** 只有关系结构真正重要时才有价值。
- **“Graph Edge 是 LLM 抽出来的，所以就是事实。”** 必须有 Provenance 与验证。
- **“用了 LangGraph 就是 Agentic RAG。”** Framework 不定义系统语义。
- **“Max Steps 能解决死循环。”** 只能硬截断，最好还检测信息增益。
- **“最终回答对就说明 Agentic Pipeline 好。”** 还要比较成本、步骤、路由和稳定性。
- **“多 Source Retrieval 自动继承相同权限。”** 每个 Source 都要应用自己的授权边界。

---

## 24. 🔍 深挖追问

```text
GraphRAG 怎样做 Incremental Update？
Edge 有多个 Source 支持时删除一个文档怎么办？
Entity Resolution 怎样评估？
Graph / Vector / BM25 怎样融合？
Agentic RAG 怎样定义 Evidence Sufficiency？
如何检测 No-new-evidence？
怎样证明 Agentic RAG 值得多花的成本？
```

---

<details>
<summary>自测 1：为什么 Graph Retrieval 之后仍应该回到原始 Evidence？</summary>

因为图中的 Entity / Relation 可能由抽取模型生成、版本可能过期。最终回答如果能回到具体 Source / Chunk，就可以 Citation、审计和验证，而不是把派生 Graph 当成不可质疑的事实库。
</details>

<details>
<summary>自测 2：为什么 Agentic RAG 只设置 Max Steps 仍不够？</summary>

Max Steps 只能防止无限运行，却无法判断多轮检索是否仍在获得新信息。还应追踪 Evidence 增益、重复候选、原始 Goal、成本和未支持 Claim，才能语义上决定停止、澄清或拒答。
</details>

<details>
<summary>自测 3：什么时候固定 RAG 比 Agentic RAG 更合理？</summary>

当问题类型稳定、知识源单一、一次 Hybrid/Rerank 已能可靠覆盖 Evidence 时，固定 Pipeline 通常更便宜、更快、更容易回归测试。只有动态检索在真实 Eval 上带来足够收益时才值得引入 Agent Loop。
</details>
