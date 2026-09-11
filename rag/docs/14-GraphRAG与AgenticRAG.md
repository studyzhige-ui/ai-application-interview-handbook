# 14｜GraphRAG、Agentic RAG 与 Production Architecture

## 1. 先讲人话

普通 RAG 常假设：

```text
Query
→ 一次 Retrieval
→ 一次 Generation
```

但现实问题有两类会超出这个模型：

1. 问题需要跨实体、跨关系、多跳推理；
2. Query 一次检索不够，需要根据中间 Evidence 决定继续搜什么。

前者催生 GraphRAG / Knowledge Graph Retrieval，后者走向 Agentic RAG。

---

## 2. GraphRAG 解决什么

Vector Retrieval 主要依据语义相似度。

Graph 更擅长表达显式关系：

```text
Person --works_at--> Company
Company --owns--> Product
Product --depends_on--> Service
```

当问题是：

> “哪些服务同时依赖 A，并由 B 团队维护？”

这种关系约束可能比纯语义近邻更适合图查询。

---

## 3. GraphRAG 的基本链路

一种常见抽象：

```text
Documents
→ Entity / Relation Extraction
→ Graph Build
→ Community / Subgraph / Path Retrieval
→ Text Evidence Linking
→ LLM
```

关键不是“有图就高级”，而是图中的 Entity / Relation 是否可靠。

---

## 4. GraphRAG 的成本和 Failure

- Entity Extraction 错；
- Relation Hallucination；
- Entity Resolution 错；
- Graph Update 滞后；
- Community Summary 失真；
- 构建成本高；
- Query Planner 复杂。

所以 GraphRAG 更适合关系结构确实重要的 Corpus，不应该替代所有 Vector RAG。

---

## 5. Agentic RAG 是什么

Agentic RAG 把 Retrieval 变成 Loop 中的能力：

```text
Observe Question
→ Decide whether to retrieve
→ Search
→ Inspect Evidence
→ Rewrite / Decompose
→ Search Again
→ Decide Stop
→ Answer
```

它的核心不是“用了 Agent 框架”，而是：

> **检索动作由运行时根据当前状态动态决定，而不是固定一次调用。**

---

## 6. Agentic RAG 什么时候有价值

- 多跳问题；
- 一次检索 Evidence 不足；
- 需要在多个知识源之间选择；
- Query 需要逐步澄清；
- 需要验证 / 反查证据。

简单 FAQ 不一定需要 Agentic Loop。

---

## 7. Agentic RAG 的 Failure

### Infinite Retrieval Loop

不断搜但没有新信息。

### Query Drift

每轮 Rewrite 越来越偏离用户问题。

### Cost Explosion

多次 Retrieval + Rerank + LLM 调用。

### Unsupported Stop

Evidence 仍不足，但 Agent 自己决定结束并回答。

因此需要：

```text
Max Steps
Budget
Evidence Sufficiency
No-new-evidence Detection
Stop / Refusal Policy
Trace
```

完整 Runtime 控制将在 Agent Harness 模块讲。

---

## 8. 一个 Production RAG 总架构

```text
                 Offline / Ingestion
Source
  ↓
Parse / Clean / Chunk
  ↓
Embedding + Sparse Index
  ↓
Vector DB / Search / Metadata
  ↓
Version / Snapshot

                 Online / Query
User Query
  ↓
Rewrite / Plan
  ↓
Dense + Sparse / Graph
  ↓
Fusion / Rerank
  ↓
Context / Citation
  ↓
LLM
  ↓
Answer

横向：Permission / Trace / Eval / Freshness / Cost
```

---

## 9. 模块边界

### RAG 负责

- Retrieval Strategy；
- Evidence Quality；
- Grounding；
- Retrieval Evaluation；
- Knowledge Freshness。

### Agent Harness 负责

- 控制循环；
- Tool Runtime；
- State；
- Context / Memory；
- Checkpoint / Resume；
- Retry / Cancellation；
- Step Budget。

所以 Agentic RAG 是两个模块的桥梁，但控制面的 Primary 属于 Agent Harness。

---

## 10. 🎯 面试怎么回答

> GraphRAG 主要用于显式实体关系和多跳关系检索，通过 Entity/Relation Graph 补充纯向量相似度；它的主要风险是抽取、消歧和图更新质量。Agentic RAG 则把 Retrieval 变成 Agent Loop 中的动态动作，让系统根据 Evidence 决定是否继续改写、搜索或停止，但需要 Step/Cost Budget、No-new-evidence、Refusal 和完整 Trace 防止死循环。简单知识问答不一定需要这两种复杂架构。

## 11. ⚠️ 易错点

- “GraphRAG 一定比 Vector RAG 好”；
- “用了 LangGraph 就叫 Agentic RAG”；
- Agentic RAG 没有停止条件；
- 图关系由 LLM 抽取后不做质量验证。

## 12. 🔍 继续追问

- GraphRAG 怎样做 Incremental Update？
- Agentic RAG 怎样判断 Evidence 足够？
- Vector / Graph / Keyword 怎样组合？

<details><summary>查看参考答案：什么时候不应该上 Agentic RAG？</summary>

当问题简单、知识源单一、一次 Retrieval 已能稳定覆盖证据时，固定 Pipeline 通常更低延迟、更便宜、更容易评估。只有动态决策确实带来可验证收益时，才值得引入 Agent Loop。

</details>
