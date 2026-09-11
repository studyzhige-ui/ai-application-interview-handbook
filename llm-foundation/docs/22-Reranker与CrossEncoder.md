# 22｜Bi-Encoder、Cross-Encoder 与 Reranker

## 1. 为什么有了 Embedding 还需要 Reranker

Bi-Encoder 的优势是快：

```text
Query → q vector
Document → d vector
sim(q, d)
```

但 Query 和 Document 在编码阶段彼此看不到。

这意味着它很适合大规模召回，却不一定最擅长做细粒度相关性判断。

Cross-Encoder 则让 Query 和 Document 一起进入模型：

```text
[Query, Document]
      ↓
Cross-Encoder
      ↓
Relevance Score
```

模型可以直接建模两者 Token-level 交互，因此通常更精确，但更贵。

---

## 2. 两种模型的根本差异

### Bi-Encoder

```text
encode(query) → q
encode(doc)   → d
score(q, d)
```

优点：

- 文档可预计算；
- 能建立 ANN Index；
- 扩展到百万 / 亿级文档。

缺点：

- Query / Doc 深度交互弱。

### Cross-Encoder

```text
encode(query, doc together)
→ score
```

优点：

- 相关性判断更精细。

缺点：

- 每个 Query-Doc Pair 都要跑模型；
- 无法直接预计算单独文档向量做 ANN。

---

## 3. 为什么常见 Pipeline 是 Retrieve → Rerank

典型流程：

```text
100 万 documents
      ↓
Bi-Encoder / ANN
      ↓
Top 50 candidates
      ↓
Cross-Encoder Rerank
      ↓
Top 5
```

这样把：

```text
高 Recall 的廉价召回
+
高 Precision 的昂贵排序
```

组合起来。

完整 Retrieval Strategy 在 RAG 模块展开；这一章只解释模型侧为什么两阶段合理。

---

## 4. Reranker 输出的分数是什么

通常是某种相关性分数或分类 / ranking score。

不要默认它能直接和 Vector Similarity 做数值比较。

例如：

```text
cosine = 0.83
rerank_score = 7.2
```

这两个分数来自不同模型和标度，不能直接线性混合而不校准。

RRF / Fusion 等属于 RAG Pipeline。

---

## 5. Rerank 为什么很贵

如果 Retriever 召回：

```text
Top 100
```

Cross-Encoder 就要对 100 个 Query-Doc Pair 做前向计算。

文档又很长时：

```text
100 × long sequence
```

成本会快速增长。

所以：

> Reranker 的 Candidate K 是 Latency / Cost / Quality 的关键参数。

---

## 6. Reranker 的 Failure Case

### 6.1 Candidate 根本没召回

如果正确文档不在 Retriever Top-K 里，Reranker 再强也没用。

所以：

```text
Retriever Recall
是 Reranker 的上限
```

### 6.2 Query / Document 截断

Cross-Encoder Context 有限，长文档可能被截断关键证据。

### 6.3 Domain Shift

通用 Reranker 在特殊领域可能排序不好。

### 6.4 Score Distribution 变化

模型升级后阈值可能需要重新标定。

---

## 7. Reranker 与 LLM-as-a-Judge

有时也会用强 LLM 给候选文档排序。

优点：

- 能理解复杂 Instruction；
- 可以给解释。

缺点：

- 延迟和成本更高；
- 稳定性和批量吞吐更差；
- Prompt / Position Bias 需要评估。

所以不能把通用 LLM Judge 当成默认 Reranker。

---

## 8. 🎯 面试怎么回答

> Bi-Encoder 把 Query 和 Document 分别编码成向量，因此文档能离线预计算并做 ANN，适合大规模高 Recall 召回；Cross-Encoder 让 Query 和 Document 联合编码，能做更细粒度 Token 交互，通常相关性更准但计算昂贵。因此 RAG 常先用 Bi-Encoder 召回较小候选集，再用 Cross-Encoder Reranker 精排。

---

## 9. ⚠️ 易错点

错误：

> Reranker 能弥补 Retriever 完全没召回正确文档。

不能。

错误：

> Reranker Score 和 Cosine Similarity 可以直接比较。

通常不能假设同一标度。

---

<details>
<summary>自测：为什么不能直接让 Cross-Encoder 对 100 万文档做检索？</summary>

因为每个 Query-Document Pair 都需要一次联合前向计算，计算量无法像 Bi-Encoder 那样通过预计算文档向量和 ANN 大幅降下来。

</details>
