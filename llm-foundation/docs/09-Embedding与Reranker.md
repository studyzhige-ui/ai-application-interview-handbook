# 09｜Embedding 与 Reranker：Bi-Encoder / Cross-Encoder 的分工

Embedding Model 和 Reranker 经常一起出现在 RAG，但它们解决的是两个不同阶段的问题：

```text
Embedding / Bi-Encoder
→ 大规模快速召回

Cross-Encoder / Reranker
→ 小候选集精细排序
```

这一章只讲模型基础；Hybrid、RRF、Top-K Pipeline 和端到端 Retrieval Evaluation 仍属于 RAG。

---

## 1. Embedding Model 在做什么

Embedding Model 把文本、图片或其它对象映射到固定维向量：

```text
Object
→ Encoder
→ Vector
```

目标是让某种“语义相关关系”能在向量空间中通过距离/相似度表达。

它并不是把每个概念转换成可人工解释的独立坐标。

---

## 2. Bi-Encoder 为什么适合大规模检索

Query 和 Document 分别编码：

```text
q → Encoder → v_q

doc → Encoder → v_d
```

Document Vector 可以提前离线计算并存入 Vector DB。

在线 Query 只需：

```text
encode query once
→ ANN search existing vectors
```

因此可以扩展到大量文档。

这就是 Bi-Encoder 的最大工程优势：

> **Document 表示可预计算。**

---

## 3. Query Encoder 和 Document Encoder 不一定完全一样

有些模型使用共享 Encoder，但需要不同 Prefix：

```text
query: ...
passage: ...
```

有些体系可能使用不同参数的双塔。

所以必须遵循模型契约：

```text
Query Preprocess
Document Preprocess
Normalization
Metric
```

Vector DB 只负责存储和搜索，不知道你是否用错模型输入协议。

---

## 4. Embedding 质量怎么评估

不能只看：

```text
“感觉语义挺像”
```

应使用与你业务一致的数据：

```text
Query
Relevant Document / Pair Label
```

然后测：

- Recall@K；
- MRR / NDCG（具体归 RAG）；
- Domain Slice；
- Hard Negative；
- 多语言/长短 Query；
- 真实 Filter 场景。

Embedding Benchmark 和 ANN Recall 要分开：

```text
Exact Vector Search 质量
≠
ANN Index Recall
```

---

## 5. Embedding Model 选型看什么

至少关注：

```text
Retrieval Quality
Domain Fit
Language Coverage
Dimension
Input Length
Latency
Batch Throughput
Cost
Normalization / Metric Contract
Deployment / Privacy
```

Dimension 大并不自动表示质量更好。

---

## 6. 为什么 Dense Embedding 不是万能的

Dense Semantic Retrieval 擅长：

- 同义表达；
- 语义相似；
- 概念性 Query。

但可能在这些场景吃亏：

- 精确术语；
- ID / Code / Error Message；
- 人名 / SKU；
- 稀有 Keyword；
- 数字匹配。

因此 RAG 常结合 Sparse/BM25 与 Hybrid Retrieval。

---

## 7. Cross-Encoder 为什么更准但更贵

Bi-Encoder 分别编码 Query 和 Document：

```text
q → vector

D → vector
```

Cross-Encoder 则把两者一起输入模型：

```text
[q, document]
→ model jointly attends both
→ relevance score
```

它可以建模更细的 Token-to-Token 交互，因此通常排序精度更强。

但代价是：

> **每个 Query-Document Pair 都要重新 Forward。**

如果有 1 亿文档，不可能在线对全部做 Cross-Encoder。

---

## 8. Reranker 的典型位置

因此常见两阶段：

```text
Fast Retriever
→ Top 20 / 50 / 100 candidates
→ Reranker
→ Top 5 / 10
```

第一阶段追求：

```text
Recall
```

第二阶段追求：

```text
Precision / Ranking Quality
```

具体候选数、Top-K 和是否 Hybrid 属于 RAG Pipeline。

---

## 9. 为什么 Rerank 不能救回未召回的文档

如果正确文档根本没有进入 Candidate Set：

```text
Retriever misses relevant doc
→ Reranker never sees it
```

那么 Reranker 再强也无能为力。

所以 Debug 时要先问：

```text
Ground Truth in Candidate Set?
```

再判断 Ranking。

---

## 10. Reranker 输入长度与截断

Cross-Encoder 通常有输入长度限制。

如果候选文档很长：

```text
query + long chunk
→ truncate
```

可能把真正相关证据截掉。

因此 Chunk Size、Reranker Max Length、Candidate Content 之间要一起设计。

---

## 11. Reranker 也有 Domain Shift

一个通用 Reranker 在法律、医疗、代码等领域未必同样有效。

因此“加了 Rerank 就一定提升”是错误的。

需要验证：

```text
Baseline Retriever
vs
Retriever + Reranker
```

在真实 Query Set 上的变化。

---

## 12. Cross-Encoder 和 LLM Judge 的区别

Reranker 通常针对：

```text
Query-Document Relevance
```

做高效评分。

LLM Judge 可以评更复杂维度，但：

- 成本更高；
- Latency 更高；
- 稳定性/偏差不同。

不能把所有“模型打分”都混成同一个概念。

---

## 13. Embedding 与 Reranker 的版本治理

Production 应记录：

```text
embedding_model_version
reranker_version
preprocess_version
metric
normalization
```

Embedding Model 更新往往需要 Re-embedding / Index Generation；Reranker 更新通常不要求重建向量，但需要重新做 Ranking Regression。

---

## 14. 常见错误

- Embedding Dimension 越大质量一定越高：错。
- Vector DB 检索差就一定是 ANN 问题：可能是 Embedding。
- Cross-Encoder 可以直接搜全库：通常成本不可接受。
- 加 Reranker 一定更好：必须评估 Domain Fit。
- Reranker 能救回没召回的文档：不能。
- Embedding Model 和 Reranker 升级生命周期完全一样：不同。

---

## 15. 面试怎么答

### Q：Bi-Encoder 和 Cross-Encoder 区别？

> Bi-Encoder 分别编码 Query 和 Document，文档向量可以预计算，因此适合大规模 ANN Retrieval；Cross-Encoder 把 Query 和 Candidate 一起输入模型，能做更细粒度交互，排序通常更准但每个 Pair 都要重新推理，所以常用于小候选集 Rerank。

### Q：为什么先 Top20 再 Rerank Top5？

> 第一阶段用便宜 Retriever 保证候选 Recall，第二阶段用更贵但精细的 Reranker 提升排序 Precision。具体 20/5 不是固定答案，要通过 Recall、Ranking Quality、Latency 和 Cost Eval 决定。

---

## 16. 自测

<details><summary>1. 为什么 Bi-Encoder 可扩展到大规模文档？</summary>
因为 Document Embedding 可以离线预计算，在线只编码 Query 并搜索已有向量。
</details>

<details><summary>2. 为什么 Reranker 无法修复第一阶段漏召回？</summary>
因为它只能给已经进入 Candidate Set 的文档重新排序。
</details>

<details><summary>3. Embedding Model 升级和 Reranker 升级的主要运维差异是什么？</summary>
Embedding 变化通常需要重新生成文档向量和新索引；Reranker 变化主要影响在线排序模型和回归验证。
</details>
