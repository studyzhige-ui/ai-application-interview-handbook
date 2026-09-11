# 22. Rerank 与 Candidate Budget：从高 Recall 候选到高 Precision Evidence

Retriever 的目标通常是：

```text
尽量别漏相关文档
```

但最终送给 LLM 的 Evidence 目标是：

```text
少、准、互补、可解释
```

因此 Rerank 和 Top-K / Threshold / Candidate Budget 本质上属于同一个 Funnel：

```text
Broad Recall
→ Candidate Set
→ Precise Rerank
→ Evidence Budget
```

---

## 1. 为什么第一阶段不直接追求最终 Top5

如果 Retriever 只召回 5 个：

```text
相关文档一旦排到第 6
→ 永远无法被后续 Reranker 救回
```

所以常见策略是：

```text
Retriever Top50
→ Reranker
→ Top5 / Top10
```

第一阶段偏 Recall，第二阶段偏 Precision。

具体数字不是模板，要通过 Eval 选。

---

## 2. Reranker 为什么更精确

Cross-Encoder 类 Reranker 将：

```text
Query + Candidate Text
```

一起输入模型，让二者在 Token 级共同建模。

相比 Bi-Encoder 只比较独立向量，它通常能捕捉更细的：

- 条件关系；
- 实体对应；
- 否定；
- 细粒度语义。

代价是每个 Pair 都要推理，所以只能用于较小候选集。

---

## 3. Candidate Budget 是什么

整个 Retrieval Funnel 有一个隐含预算：

```text
Dense returns N1
Sparse returns N2
Fusion keeps N3
Reranker scores N4
Final context keeps N5
```

这些 N 不能无限增大。

Candidate 越多：

```text
Recall Potential ↑
Rerank Cost ↑
Latency ↑
Duplicate ↑
Context Selection Complexity ↑
```

所以需要 Candidate Budget。

---

## 4. Top-K 应该在哪里定义

不同阶段有不同 K：

```text
retrieval_k
fusion_k
rerank_k
context_k
```

不要只有一个全局 `top_k=5`。

例如：

```text
Dense 30
Sparse 30
Fusion 40 unique
Rerank 40
Context 6
```

只是示意，不是推荐固定值。

---

## 5. Reranker Score 能直接设通用 Threshold 吗

不建议跨模型/领域抄固定值。

Score Distribution 会受：

- Reranker Model；
- Domain；
- Query Type；
- Candidate Length；
- Calibration；

影响。

Threshold 应根据真实 Label / Eval 校准。

---

## 6. 为什么加 Reranker 可能反而变差

常见原因：

### Candidate 根本没召回 Ground Truth

Reranker 无法创造不存在的候选。

### Domain mismatch

通用 Reranker 对专业领域相关性判断错误。

### Input Truncation

Chunk 太长，真正 Evidence 被截断。

### Query Rewrite Drift

Reranker 收到的是偏移后的 Query。

### Candidate Duplicate

Top Results 都是同一文档近重复片段。

### Score Calibration / Top-K 不合适

相关但互补的证据被过度挤掉。

所以必须做 Ablation：

```text
Retriever only
vs
Retriever + Reranker
```

---

## 7. Rerank 的输入应该是什么

不一定只是裸 Chunk Text。

可以加入：

```text
section title
parent heading
source type
```

帮助判断语义。

但 Metadata 太多也会占长度并干扰模型。

要通过 Eval 选择。

---

## 8. Diversity 为什么重要

假设 Top5：

```text
same paragraph v1
same paragraph v2
same paragraph duplicated
same paragraph overlap
another relevant fact
```

即使前四条 score 很高，Context 信息量也很低。

可以在 Rerank / Context Selection 后做：

- Document Dedup；
- Parent Merge；
- MMR / diversity heuristic；
- Evidence coverage optimization。

目标不是“每条独立最高分”，而是：

> **在有限 Context Budget 下覆盖回答所需 Evidence。**

---

## 9. Multi-hop 问题需要什么

有些问题需要两份不同 Evidence：

```text
A 的政策是什么？
为什么它和 B 冲突？
```

单纯按每个 Chunk 独立 relevance 排序，可能只返回 A 的多个片段。

需要在 Query Decomposition / Evidence Selection 中考虑：

```text
coverage across subquestions
```

这再次说明 Final Context 不应只是 `reranked[:K]`。

---

## 10. Rerank Latency 怎么控制

Rerank 成本近似随：

```text
candidate count
× candidate length
× model cost
```

增加。

优化方向：

- 更好的 first-stage Recall，减少候选；
- Batch scoring；
- smaller reranker；
- early filtering；
- cached score（只在安全条件下）；
- route hard queries to expensive rerank。

---

## 11. Top-K 为什么必须和 Context Budget 联动

如果最终每个 Chunk 1000 Token：

```text
TopK=20
→ 20K Token
```

如果每个 Chunk 200 Token：

```text
TopK=20
→ 4K Token
```

所以 K 本身没有绝对意义。

真正约束是：

```text
Evidence Coverage
within
Context Token Budget
```

---

## 12. No-hit 和 Reranker 的关系

Reranker 可以帮助判断 Candidate 是否真正相关。

如果最高结果仍低于经过 Eval 校准的可靠边界：

```text
No Hit
→ clarify / refuse / alternate route
```

但不能用未经校准的统一阈值。

---

## 13. Eval 应怎样验证 Candidate Funnel

至少分层记录：

```text
Ground Truth in Retriever TopN?
Ground Truth rank after Fusion?
Ground Truth rank after Rerank?
Ground Truth included in Context?
```

这样才能知道优化到底作用在哪一层。

---

## 14. 常见错误

- Reranker 可以救回没召回的文档：不能。
- TopK 越大越保险：会增加噪声/成本。
- Reranker Score 有通用阈值：错误。
- Rerank 后直接 `[:5]` 就是最佳 Context：可能缺 Diversity/Coverage。
- 加 Reranker 一定提升：必须做 Ablation。
- Candidate Count 只影响 Latency，不影响质量：也会改变 Recall 和 Diversity。

---

## 15. 面试怎么答

### Q：为什么常见 Top20 再 Rerank Top5？

> 第一阶段 Retriever 要保证 Recall，因此先保留较宽候选；Cross-Encoder Reranker 精度高但每个 Query-Document Pair 都要推理，只适合小候选集，再从中挑有限 Evidence。20/5 不是固定参数，要同时看 Recall、Rerank Quality、Latency、Token Budget 和 Answer Eval。

### Q：Rerank 后效果反而变差怎么排查？

> 先确认 Ground Truth 是否进入 Candidate Set，再看 Reranker 是否发生 Domain mismatch、输入截断、Query Drift、重复候选或 Top-K/Candidate Budget 不合理，用 Retriever-only vs Retriever+Reranker 的 Ablation 定位。

---

## 16. 自测

<details><summary>1. 为什么 Retriever Top-K 和 Context Top-K 要分开？</summary>
前者为了候选 Recall，后者受 Context Budget、Diversity 和 Evidence Coverage 约束。
</details>

<details><summary>2. Reranker 最重要的前置条件是什么？</summary>
相关文档必须已经进入 Candidate Set。
</details>

<details><summary>3. 为什么最终选择要考虑 Diversity？</summary>
多个高分近重复 Chunk 会浪费 Context，可能不如覆盖不同必要 Evidence。
</details>
