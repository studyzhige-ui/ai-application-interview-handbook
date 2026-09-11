# 22｜Rerank Pipeline：Precision、Latency 与 Failure

## 1. 先讲人话

Retriever 的目标通常偏向：

> **不要漏掉相关候选。**

Reranker 的目标更偏向：

> **在已经召回的候选中，把真正最相关的排到前面。**

因此常见两阶段架构是：

```text
High Recall Retrieval
→ Smaller Candidate Set
→ High Precision Rerank
→ Final Evidence
```

---

## 2. 为什么需要 Rerank

Dense / Sparse Retrieval 常使用相对便宜的表示和索引，以保证大规模候选生成速度。

Cross-Encoder / Reranker 则可以直接联合看：

```text
Query + Passage
```

做更精细相关性判断，但计算成本更高。

所以它适合用于几十个候选，而不是百万级全库扫描。

---

## 3. 一个典型预算

```text
Dense Top-50
Sparse Top-50
↓
Fusion / Dedup → 60
↓
Reranker → Top-10
↓
Context Build → Top-5
```

这里每一层都在平衡：

```text
Recall
Precision
Latency
Cost
```

---

## 4. 为什么“加 Rerank 后反而变差”

这是非常重要的 Production 问题。

可能原因包括：

### Candidate 根本没召回正确答案

Reranker 不能把不存在的证据排出来。

### Reranker Domain Mismatch

模型在通用语义数据上训练，但你的场景是代码、法律、医学、内部缩写。

### Input Truncation

长 Chunk 被截断，真正相关部分没有进入 Reranker 输入。

### Query Rewrite 错了

Reranker 忠实地排了错误 Query 的候选。

### Score / Top-K 使用错误

错误阈值、错误排序方向或模型 API 用法。

### Candidate Diversity 降低

Reranker 把多个高度相似 Chunk 排到最前，导致最终 Evidence Coverage 下降。

---

## 5. Rerank 不是“越重越好”

可以选择：

- 轻量 Cross-Encoder；
- 专用 Reranker；
- LLM-as-Reranker；
- Rule + Model 混合。

越强的模型通常带来越高延迟和成本。

要看业务 SLO：

```text
Quality Gain / Added Latency / Added Cost
```

---

## 6. 怎样验证 Rerank

至少比较：

```text
Retriever-only
vs Retriever + Reranker
```

指标：

- MRR / NDCG；
- Recall@Final-K；
- End-to-end Correctness；
- P95 Latency；
- Cost / Query；
- Query Slice。

同时保存 Rerank 前后候选，才能 Debug 排序变化。

---

## 7. Rerank 与 Context Diversity

最终 Context 不一定要机械拿 Rerank Top-K。

可以考虑：

- 去重；
- Source Diversity；
- Parent 合并；
- 同一文档限制数量；
- 互补 Evidence。

否则 Top-5 可能全是同一个段落的相邻 Chunk。

---

## 8. 🎯 面试怎么回答

> Retriever 优先高 Recall，Reranker 在较小候选集上提高 Precision。常见架构是多路召回后先 Fusion，再用 Cross-Encoder 或专用 Reranker 精排。Rerank 变差时要先检查正确候选是否被召回、模型是否 Domain Mismatch、输入是否被截断、Query 是否被错误改写，以及最终 Top-K 是否缺乏 Diversity。收益必须通过排序指标、End-to-end Quality、Latency 和 Cost 一起验证。

## 9. ⚠️ 易错点

- “Rerank 能救回没有被召回的文档”；
- “模型越大越好”；
- 不保存 Rerank 前候选，出问题无法定位；
- 最终 Context 机械取 Top-K，不做去重与 Coverage。

## 10. 🔍 继续追问

- Cross-Encoder 为什么比 Bi-Encoder 慢？
- Rerank Candidate 数怎样定？
- LLM Rerank 什么时候值得？

<details><summary>查看参考答案：Rerank 变差时第一步查什么？</summary>

先检查 Ground Truth 是否出现在 Rerank 输入候选中。如果正确证据在 Retrieval 阶段就没召回，问题属于 Candidate Generation；只有候选已存在却被排低，才优先定位 Reranker。

</details>
