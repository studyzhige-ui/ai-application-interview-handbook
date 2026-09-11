# 21｜RRF / Fusion：多路召回怎样合并

## 1. 先讲人话

Hybrid Retrieval 之后会得到多份排序列表：

```text
Dense Rank
Sparse Rank
可能还有 Metadata / Graph / FAQ Rank
```

Fusion 的任务是：

> **把不同检索器的候选合并成一个稳定排序，而不假设它们的原始分数天然可比。**

---

## 2. RRF 的核心思想

Reciprocal Rank Fusion 不直接比较原始 Score，而更关注候选在每一路的排名。

常见形式：

```text
RRF(d) = Σ 1 / (k + rank_i(d))
```

其中：

- `rank_i(d)`：文档 d 在第 i 路结果中的排名；
- `k`：平滑常数，控制前几名优势强度。

直觉：

> 在多路中都排得靠前的文档，会得到更高融合分。

---

## 3. 为什么 RRF 常比直接加分简单可靠

Dense Score 与 BM25 Score：

- 范围不同；
- 分布不同；
- 不同 Query 下尺度也可能变化。

RRF 绕开了“怎么把两个异构分数标定到同一尺度”的问题。

因此它是很实用的 Baseline。

---

## 4. RRF 的 Trade-off

优点：

- 简单；
- 对异构 Score 友好；
- 易解释；
- 不需要训练。

缺点：

- 丢失原始 Score 的绝对信息；
- 不理解 Query 类型；
- 很难表达“某一路对某类 Query 更可信”；
- `k` 和各路 Candidate Budget 仍需实验。

---

## 5. 其它 Fusion 思路

### Score Normalization + Weighted Sum

先把每路分数归一化，再加权。

问题：Normalization 本身需要稳定标定。

### Learned Fusion

用训练数据学习不同信号如何组合。

适合有大量 Ground Truth 的成熟系统，但复杂度更高。

### Reranker as Fusion

把多路 Candidate Union 之后交给 Cross-Encoder / LLM Reranker 排序。

常见 Production 方案：

```text
Dense + Sparse
→ RRF 粗融合
→ Rerank 精排
```

---

## 6. Candidate 去重

Fusion 前必须确保同一 Chunk 不被当成两个实体：

```text
chunk_id = stable identity
```

同时可以保留：

```text
retrieved_by: [dense, sparse]
dense_rank
sparse_rank
```

方便 Debug。

---

## 7. 怎样调 RRF

不要只盯 `k`。

还应一起观察：

- 每路 Top-N；
- 重复率；
- Recall@K；
- MRR/NDCG；
- Rerank 前 Candidate 数；
- P95 Latency；
- 不同 Query Slice。

有时真正影响效果的不是 `k`，而是 Sparse/Dense Candidate Budget。

---

## 8. 🎯 面试怎么回答

> RRF 是常见 Rank-based Fusion 方法。它不直接比较 Dense 和 BM25 的原始分数，而根据文档在各路结果中的排名累加倒数排名得分，因此适合异构检索器。优点是简单、稳定、无需训练，缺点是丢失绝对分数和 Query-specific 权重。实际要通过 Candidate Budget、k、Recall/NDCG 以及最终 Rerank 结果做实验。

## 9. ⚠️ 易错点

- “RRF 就是两个 Score 相加”；
- 只调 k，不看各路 Top-N；
- 同一个 Chunk 重复进入融合；
- RRF 后就不需要 Rerank。

## 10. 🔍 继续追问

- 为什么不直接 Min-Max Normalize 后相加？
- RRF 的 k 变大意味着什么？
- 哪些场景 Learned Fusion 更值得？

<details><summary>查看参考答案：RRF 为什么特别适合 Dense + BM25？</summary>

因为 Dense 与 BM25 的原始分数含义和尺度不同，RRF 只依赖相对排名，减少了分数标定问题，同时保留“多路一致认为重要”的信号。

</details>
