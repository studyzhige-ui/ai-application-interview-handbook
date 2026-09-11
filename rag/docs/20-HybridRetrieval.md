# 20｜Hybrid Retrieval：为什么组合 Dense + Sparse

## 1. 先讲人话

Dense 擅长语义，Sparse 擅长精确词项。Hybrid Retrieval 的核心不是“把两个组件都打开”，而是：

> **让不同检索信号互补，再通过可验证的融合策略形成更稳定的候选集。**

---

## 2. 一个典型流程

```text
Query
├── Dense Retrieval → Top-N
└── Sparse / BM25  → Top-N
          ↓
      Candidate Union
          ↓
        Fusion
          ↓
       Rerank
          ↓
       Final Top-K
```

---

## 3. 为什么 Hybrid 有价值

真实 Query 分布往往混合：

- 自然语言语义问题；
- 产品编号；
- 错误码；
- 专有名词；
- 短 Query；
- 模糊表达。

单一路线通常会在某些 Slice 上明显失分。

Hybrid 的目标是提高整体 Robustness，而不是追求“每次两个检索器都贡献一半”。

---

## 4. Candidate Union 的问题

如果 Dense Top-50 + Sparse Top-50，最多得到 100 个候选，但实际可能：

- 大量重叠；
- 分数尺度不同；
- 某一路结果数量异常；
- 某一路被噪声占满。

所以需要统一 `chunk_id` 去重，并保留 route：

```text
retrieved_by = [dense, sparse]
```

这对后续 Debug 很重要。

---

## 5. 分数为什么不能直接相加

Dense Cosine Score 和 BM25 Score 的数值含义、分布和范围通常不同。

直接：

```text
0.8 + 12.4
```

没有自然的可比意义。

常见策略：

- Rank-based Fusion，例如 RRF；
- Score Normalize 后加权；
- Learned Fusion；
- 先 Union，再交给 Reranker。

---

## 6. Hybrid 不是免费收益

代价包括：

- 多路检索 Latency；
- 更多 Candidate；
- 更高 Rerank Cost；
- 更复杂 Trace；
- 更多参数。

所以应该先证明 Baseline 的 Dense / Sparse 各自在哪些 Query Slice 失败，再引入 Hybrid。

---

## 7. 怎样证明 Hybrid 真有效

至少比较：

```text
Dense only
Sparse only
Hybrid
Hybrid + Rerank
```

指标：

- Recall@K；
- MRR / NDCG；
- Exact-term Slice；
- Semantic Slice；
- End-to-end Correctness；
- P95 Latency / Cost。

最重要的是看 Slice，而不只是总平均值。

---

## 8. Failure Case

### Sparse 噪声过强

用户 Query 中某个常见词命中大量无关文档，Union 变大。

### Dense 召回泛化过头

语义相关但产品版本不对。

### Hybrid Recall 升了，最终答案反而差

更多 Candidate 进入后，Reranker 或 Context Budget 处理不好，Noise 增加。

---

## 9. 🎯 面试怎么回答

> Hybrid Retrieval 组合 Dense 的语义泛化和 Sparse/BM25 的精确词项能力。Production 中通常分别生成候选，按 chunk_id 去重，再通过 RRF、归一化打分或 Reranker 融合。因为两路分数尺度不同，不能直接相加。是否值得 Hybrid 要通过 Dense-only、Sparse-only、Hybrid 的 Ablation 和 Query Slice 指标验证，同时考虑额外 Latency 和 Rerank Cost。

## 10. ⚠️ 易错点

- “Hybrid 就是 Dense Score + BM25 Score”；
- 不保留 candidate route；
- 只看 Recall，不看最终 Answer 和 Latency；
- Candidate Union 无限扩大。

## 11. 🔍 继续追问

- RRF 为什么常用于 Hybrid？
- Hybrid 的 Dense / Sparse Top-N 应该相同吗？
- 哪些 Query 可以动态只走一路？

<details><summary>查看参考答案：Hybrid 一定要并行跑两路吗？</summary>

不一定。可以根据 Query Intent / Type 动态路由，例如错误码优先 Sparse、语义问答优先 Dense；也可以默认并行以追求 Recall。是否动态路由取决于质量、延迟和复杂度目标。

</details>
