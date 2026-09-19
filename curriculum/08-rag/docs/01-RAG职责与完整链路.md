# 01｜RAG 的职责与 Production End-to-End Pipeline

RAG = Retrieval-Augmented Generation。

它不是“Vector DB + Prompt”的同义词，而是一条完整证据链：

```text
Knowledge Source
→ Ingestion
→ Parse / Clean
→ Chunk / Metadata
→ Index
→ Query Understanding
→ Retrieval
→ Fusion / Rerank
→ Context Construction
→ Grounded Generation
→ Citation
→ Evaluation / Observability
```

这一章把“为什么需要 RAG”和“完整 Pipeline”合成一个入口：先知道系统要解决什么，再看到后面每个子系统为什么存在。

---

## 1. 为什么需要 RAG

LLM 参数里拥有的是训练阶段学到的统计知识，它天然存在几个边界：

- 私有企业知识不在公开训练数据中；
- 知识会过期；
- 用户/租户数据动态变化；
- 需要可追溯 Citation；
- 需要权限过滤；
- Context Window 不可能放下全部知识库。

RAG 的目标是：

> **在推理时，从外部知识源选出少量最相关、最新、允许访问的证据，再让模型基于这些证据回答。**

---

## 2. RAG 改变的不是模型参数

```text
Fine-tuning
→ change parameters

RAG
→ change inference-time evidence
```

所以当问题是：

```text
公司最新制度
内部产品文档
用户订单状态
```

通常更自然的是 RAG / Tool，而不是把事实持续训练进模型。

---

## 3. 一个 Production RAG 的两条主链

### Offline / Ingestion Plane

```text
Source
→ Fetch / Parse
→ Clean / Dedup
→ Identity / Version
→ Chunk
→ Metadata
→ Embedding / Sparse Index
→ Vector / Search Store
```

### Online / Query Plane

```text
User Query
→ Normalize / Rewrite / Route
→ Retrieve candidates
→ Fusion
→ Rerank
→ Context Budget
→ LLM
→ Citation
→ Trace / Eval
```

很多 Demo 只实现后半条的几步，Production 必须同时管理知识生命周期。

---

## 4. Source of Truth 在哪里

Vector DB 通常不应该是原始文档唯一 Source of Truth。

更稳妥的结构：

```text
Original Source / Object Store / DB
        ↓
Parsed Artifact
        ↓
Chunk / Embedding / Index
```

这样当：

- Embedding Model 升级；
- Chunk Strategy 变化；
- Index 损坏；
- 需要 Rollback；

都可以从 Source of Truth 重建。

---

## 5. RAG 的核心不是 Recall 单指标

一个回答正确需要：

```text
Source contains answer
AND Parser preserves it
AND Chunk keeps it coherent
AND Retriever recalls it
AND Reranker keeps it
AND Context includes it
AND Model uses it faithfully
```

任何一层失败都可能得到错误答案。

所以 RAG Debug 必须分层，而不能“召回差就换 Embedding”。

---

## 6. 为什么要 Dense + Sparse + Rerank

不同检索信号擅长不同问题：

```text
Dense → semantic similarity
Sparse/BM25 → exact term / ID / rare keyword
Reranker → fine-grained query-document relevance
```

Production RAG 往往是 Funnel：

```text
large corpus
→ cheap broad recall
→ candidate fusion
→ expensive precision rerank
→ small evidence set
```

后面会逐层展开。

---

## 7. Context Construction 不是简单拼接 Top-K

候选结果需要：

- 去重；
- 合并 Neighbor / Parent；
- 保留 Source Mapping；
- 控制 Token Budget；
- 按重要性排序；
- 避免互相冲突；
- 保留 Permission / Version。

所以：

```text
Retriever Top-K
≠ Final LLM Context
```

---

## 8. Grounding 与 Citation

一个可审计 RAG 应尽量保持：

```text
Answer Claim
→ Context Evidence
→ Chunk ID
→ Document Version
→ Original Source
```

Citation 不只是 UI 装饰，而是：

- 用户核验；
- Bad Case Debug；
- 合规；
- Freshness；
- 来源责任边界。

---

## 9. RAG Evaluation 必须从第一天设计

如果没有 Eval，下面这些优化都无法证明：

```text
Chunk 512 → 1024
Dense → Hybrid
TopK 10 → 30
Add Reranker
Change Embedding
```

因此 Production RAG 需要：

```text
Evaluation Dataset
Ground Truth / Relevance Labels
Retrieval Metrics
Answer Metrics
Bad Case Slices
Regression
```

Evaluation 不是最后上线前的附录，而是整个 Retrieval Engineering 的反馈回路。

---

## 10. RAG 和 Vector DB 的边界

Vector DB 解决：

```text
store vector
ANN search
metadata filter
index lifecycle
scale
```

RAG 解决：

```text
怎样生成 Retrieval Unit
怎样理解 Query
怎样组合 Dense/Sparse
怎样 Rerank
怎样构造 Context
怎样 Ground / Cite
怎样评估和运营
```

所以学过 HNSW 后，RAG 不再重新从 HNSW 内部参数开始。

---

## 11. RAG 和 Agent 的边界

RAG 可以作为 Agent 的一个 Tool/Capability：

```text
Agent
→ decide retrieval needed?
→ call RAG
→ inspect evidence
→ maybe reformulate query
→ continue / answer
```

RAG 负责 Retrieval Quality；Agent Harness 负责控制循环、Tool Runtime、Context/Memory、Checkpoint 和 Permission。

---

## 12. 一条 Trace 应该能看到什么

Production Trace 至少可以关联：

```text
original query
rewritten query
retrieval config
candidate IDs / scores
fusion/rerank result
selected context
source version
model / prompt version
answer / citation
latency / cost
```

没有这条链，Bad Case 很难复现。

---

## 13. 常见错误

- RAG = Vector DB：错误。
- 加了 RAG 就不会 Hallucinate：错误。
- Top-K 候选直接全部塞给 LLM：不一定。
- 检索到相关 Chunk 就保证模型会用：错误。
- RAG 只需要在线 Query Pipeline：知识更新同样重要。
- 没有 Eval 也可以凭几个 Demo 调参数：不可持续。

---

## 14. 面试怎么答

### Q：RAG 完整链路是什么？

> 我会把 RAG 分成 Ingestion 和 Query 两个 Plane。离线侧从 Source of Truth 做解析、清洗、版本和 Chunk，再生成 Dense/Sparse Index；在线侧先做 Query Understanding，再多路召回、Fusion、Rerank，构造带 Provenance 的有限 Context，让 LLM Grounded Generation 并输出 Citation。整个链路要有 Eval、Trace、Freshness 和 Permission，而不是只调用 Vector DB Top-K。

### Q：为什么用了 RAG 仍然会答错？

> 因为失败可能发生在 Source、Parsing、Chunk、Query Rewrite、Retrieval、Rerank、Context Construction 或 Generation 任一层，需要沿证据链做 Attribution，不能简单归因于模型。

---

## 15. 自测

<details><summary>1. 为什么 Vector DB 不应该默认作为原文 Source of Truth？</summary>
因为向量/Chunk/Index 都是可重建派生物，模型或 Chunk 策略升级时需要从稳定原始来源重建。
</details>

<details><summary>2. RAG 为什么天然需要 Evaluation？</summary>
因为 Chunk、Retriever、Fusion、Rerank、Top-K 等所有改动都存在质量/成本权衡，没有 Ground Truth 和回归无法证明改善。
</details>

<details><summary>3. Candidate Top-K 和最终 Context 有什么区别？</summary>
Candidate 是召回/排序候选；最终 Context 还要去重、扩展、压缩、权限/版本检查并受 Token Budget 约束。
</details>
