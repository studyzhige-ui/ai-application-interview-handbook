# 26｜Retrieval Metrics：Recall / Precision / Hit Rate / MRR / NDCG

## 1. 先讲人话

如果没有 Retrieval 指标，你就无法回答：

> “这次优化真的让检索变好了吗？”

不同指标回答的问题不同，不能只记公式。

---

## 2. Recall@K

问题：

> Relevant Evidence 有没有进入前 K 个候选？

对于 RAG，Recall 很重要，因为正确 Evidence 没进入候选，后续 Rerank 和 LLM 都救不回来。

---

## 3. Precision@K

问题：

> 前 K 个候选里，有多少是真的相关？

Precision 低意味着候选 Noise 高，可能增加 Rerank 和 Context 成本。

---

## 4. Hit Rate

对于每个 Query，只关心：

> Top-K 中是否至少命中一个相关文档？

它比 Recall 更粗，但对单答案知识库很直观。

---

## 5. MRR

Mean Reciprocal Rank 关注**第一个相关结果出现得多靠前**。

例如：

```text
rank = 1 → 1
rank = 2 → 1/2
rank = 5 → 1/5
```

适合“一个主要正确结果应该尽量排前”的任务。

---

## 6. NDCG

NDCG 适合：

- 多个结果都可能相关；
- 相关性有等级；
- 越相关的应该越靠前。

它比单纯 Hit Rate 更能描述排序质量。

---

## 7. 指标必须和 Ground Truth 配套

如果 Ground Truth 本身只标了一份文档，但实际上有多个正确来源：

```text
Retriever 找到另一个正确来源
→ 指标却判错
```

所以 Evaluation Dataset 的质量和 Metric 一样重要。

---

## 8. 还要做 Query Slice

总平均值可能掩盖问题。

建议拆：

```text
Exact Term
Semantic Query
Long Query
Multi-hop
Rare Entity
No-hit
```

这样才能看到 Dense / Sparse / Hybrid 各自真正的优劣。

---

## 9. Retrieval Metric ≠ End-to-end Quality

Recall 提高后：

- Context 可能更吵；
- Rerank 可能错误排序；
- LLM 仍可能生成错误答案。

因此 Retrieval Evaluation 必须和 End-to-end Evaluation 分层。

---

## 10. 🎯 面试怎么回答

> Recall@K 关注相关 Evidence 是否被召回，Precision@K 关注候选纯度，Hit Rate 看是否至少命中一个相关结果，MRR 关注第一个相关结果的位置，NDCG 适合多个有等级相关性的结果。实际 RAG 应同时做 Retrieval Metric 和 End-to-end Evaluation，并按 Query 类型切 Slice，避免总平均值掩盖问题。

## 11. ⚠️ 易错点

- 只看 Recall；
- Ground Truth 不完整；
- 把 MRR 当成 Precision；
- Retrieval 指标上涨就宣称 RAG 效果上涨。

<details><summary>查看参考答案：为什么 Recall 对第一阶段 Retrieval 特别重要？</summary>

因为后续 Reranker 和 LLM 只能处理已经进入候选集的 Evidence。正确证据在第一阶段漏掉后，后面的精排无法凭空恢复，因此 Candidate Generation 通常优先保障 Recall。

</details>
