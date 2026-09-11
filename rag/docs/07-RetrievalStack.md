# 18. Retrieval Stack：Dense、BM25、Hybrid 与 Fusion

真正的 Retrieval System 很少只依赖一种信号。

这一章把原来的 Dense、Sparse/BM25、Hybrid、RRF/Fusion 合并成一个完整问题：

> **不同检索器擅长什么，为什么需要多路召回，以及多个 Ranking 怎样被稳定合并？**

---

## 1. Dense Retrieval 擅长什么

Dense Retriever：

```text
Query
→ Embedding
→ Vector Search
→ semantic candidates
```

它擅长：

- 同义表达；
- 概念语义；
- 不共享关键词但含义相近；
- 自然语言 Query。

但可能弱于：

- 精确 ID；
- SKU；
- Error Code；
- 极罕见专有词；
- 数字/字符串精确匹配。

---

## 2. Sparse / BM25 擅长什么

Sparse Retrieval 依赖词项匹配和权重。

BM25 的直觉：

```text
term appears in document
+
rare term gets higher value
+
document length normalization
```

它很适合：

```text
E1042
Product-X-7B
exact API name
rare legal clause
```

这类精确词。

---

## 3. Dense 和 Sparse 不是谁淘汰谁

看两个 Query：

### Query A

```text
“用户很久不操作后登录状态为什么消失？”
```

Dense 可能通过语义命中：

```text
session expiration / TTL
```

### Query B

```text
“E1042”
```

BM25 往往更稳定，因为精确 Token 本身就是关键信号。

所以二者是互补信号。

---

## 4. Hybrid Retrieval 是什么

同时运行多路 Retriever：

```text
Dense Top-N
+
Sparse Top-N
+
optional other routes
        ↓
Fusion
        ↓
Unified Candidates
```

目标是：

```text
提高 Candidate Recall / Robustness
```

而不是让每一路都返回最终答案。

---

## 5. 为什么不能直接比较 Dense Score 和 BM25 Score

Dense 可能返回：

```text
0.82
0.79
```

BM25 可能返回：

```text
14.3
8.7
```

分数量纲不同、分布不同。

直接：

```text
0.82 + 14.3
```

没有通用意义。

所以需要：

- score normalization；
- learned fusion；
- rank-based fusion；
- RRF。

---

## 6. RRF 的核心思想

RRF = Reciprocal Rank Fusion。

它主要使用各路候选的 Rank，而不是原始 Score：

```text
RRF(d) = Σ 1 / (k + rank_i(d))
```

直觉：

> 在多路 Retriever 中都排得靠前的文档，会获得更高融合分数。

优点：

- 不需要对不同 Score Scale 做复杂归一；
- 简单稳健；
- 很适合多个异构 Retriever。

---

## 7. RRF 参数 k 怎么理解

`k` 控制 Rank 差异的敏感程度。

较大 k：

```text
rank 1 vs rank 10 差距相对温和
```

较小 k：

```text
特别强调前排结果
```

不要死背某个默认值，仍应通过 Eval 选择。

---

## 8. Candidate Dedup

Dense 和 Sparse 可能返回同一 Chunk：

```text
Dense: A B C
Sparse: A D E
```

Fusion 必须以稳定 `chunk_id` / `document_id` 去重，而不是按 Text String 猜。

如果同一文档多个重叠 Chunk 入选，还可能需要：

```text
near-duplicate collapse
parent merge
neighbor merge
```

以提高候选多样性。

---

## 9. Hybrid 的成本不是免费

多路 Retrieval 意味着：

```text
更多查询
更多 Candidate
更多 Fusion
更大 Rerank Input
更高 Latency / Cost
```

所以应该有：

```text
Candidate Budget
```

而不是每路都随意 Top100。

---

## 10. Query Routing vs Always Hybrid

不是所有 Query 都需要全量 Hybrid。

例如：

```text
exact error code
```

可以更偏 Sparse。

纯自然语言概念问题可以更偏 Dense。

复杂系统可以：

```text
Query Type
→ select retrieval routes
```

但 Routing 错误也会丢 Recall，所以简单系统先做稳定 Hybrid Baseline 往往更容易。

---

## 11. Metadata Filter 应在哪一层

Tenant / Permission / Version 是硬约束。

理想情况下每一路 Retriever 都遵守：

```text
same retrieval scope
```

否则：

```text
Dense filtered
Sparse unfiltered
→ Fusion leaks unauthorized candidate
```

所以 Hybrid Pipeline 的安全边界必须一致。

---

## 12. Hybrid 为什么可能变差

可能原因：

- Sparse 噪声把相关 Dense Candidate 挤下去；
- Fusion 参数不合适；
- Candidate Budget 太小；
- Query Rewrite 丢失精确词；
- Duplicate 太多；
- 权限/版本不一致；
- Reranker Domain 不匹配。

因此“加 BM25”本身不是质量保证。

---

## 13. Exact Keyword / Identifier 的特殊处理

对：

```text
SKU
ticket id
error code
class name
function name
```

可以保留：

- Keyword Field；
- Exact Match Boost；
- N-gram / analyzer；
- Fielded Search。

不要让 Query Rewrite 把这些精确信号消失。

---

## 14. Retrieval 评估怎么比较方案

在同一 Dataset 上比较：

```text
Dense only
Sparse only
Hybrid
Hybrid + RRF
```

看：

- Recall@K；
- MRR / NDCG；
- Candidate Diversity；
- P95 / P99；
- Filter Slice；
- exact-term slice；
- semantic-paraphrase slice。

只有分 Slice，才能知道 Hybrid 真正改善了哪类 Query。

---

## 15. 常见错误

- Dense 已经有语义，所以 BM25 过时：错误。
- Dense Score 和 BM25 Score 可以直接相加：通常不行。
- RRF 越多路越好：候选和成本也会爆炸。
- Hybrid 一定优于单路：需要 Eval。
- Permission 只在 Fusion 后过滤：存在安全和有效候选不足风险。
- Rewrite 后可以丢掉 ID/Keyword：错误。

---

## 16. 面试怎么答

### Q：为什么 RAG 常用 Hybrid Search？

> Dense 对同义和语义表达强，Sparse/BM25 对精确词、ID、稀有术语强，两者 failure mode 互补。通常分别召回候选，再用 RRF 或其它 Fusion 合并并去重，之后再 Rerank。是否值得 Hybrid 要用 Query Slice 的 Recall、Ranking、Latency 和成本验证。

### Q：RRF 为什么适合 Dense + BM25？

> 因为两路 Score Scale 不可直接比较，RRF 基于各自 Ranking 的 reciprocal rank 做融合，不依赖原始分数量纲，简单且对异构 Retriever 比较稳健。

---

## 17. 自测

<details><summary>1. 为什么 BM25 对 Error Code 常比 Dense 稳？</summary>
因为 Error Code 是高价值精确 Token，Sparse Retrieval 能直接利用 exact term match，而 Dense 可能把它语义平均掉。
</details>

<details><summary>2. 为什么 Hybrid Pipeline 必须统一 Permission Scope？</summary>
任何一路召回无权限数据都可能在 Fusion/Rerank 中泄漏或影响有效候选，因此安全约束必须贯穿每路。
</details>

<details><summary>3. RRF 主要使用 Score 还是 Rank？</summary>
Rank。
</details>
