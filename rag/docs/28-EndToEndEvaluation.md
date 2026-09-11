# 28｜End-to-end RAG Evaluation

## 1. 先讲人话

Retrieval 指标告诉你“有没有找对证据”，但用户最终看到的是答案。

所以 RAG Evaluation 必须至少分两层：

```text
Retrieval Quality
        ↓
Generation / Answer Quality
```

End-to-end Evaluation 负责回答：

> **整个系统最后有没有基于正确证据，给出正确、相关、可引用的答案。**

---

## 2. 常见评估维度

### Correctness

事实是否正确。

### Faithfulness / Groundedness

答案中的 Claim 是否被 Context 支持。

### Answer Relevance

是否真正回答用户问题，而不是说了一堆相关背景。

### Citation Quality

引用是否支持对应 Claim。

### Completeness

多条件 / 多跳问题是否覆盖关键要点。

### Refusal Quality

该拒答时是否拒答，该回答时是否没有过度拒答。

---

## 3. 分层评估为什么重要

假设最终答案错了：

```text
可能 Retrieval Miss
可能 Rerank 错
可能 Context Build 丢证据
可能 Prompt 错
可能 LLM Hallucinate
```

如果只有一个“总分”，无法知道应该优化哪一层。

因此建议同时记录：

```text
Retrieval Metrics
Context Evidence
Answer Metrics
```

---

## 4. Faithfulness 与 Correctness 不一样

答案可能：

### Faithful but Wrong

知识库本身是错的 / 旧的，模型忠实引用了错误文档。

### Correct but Ungrounded

模型凭自身参数知识答对了，但 Retrieved Evidence 并不支持。

Production RAG 一般希望两者都满足。

---

## 5. Offline 与 Online

### Offline

使用固定 Eval Dataset 做：

- Retrieval；
- Answer；
- Citation；
- Regression。

### Online

观察：

- 用户反馈；
- Reformulation Rate；
- Escalation；
- Click / Citation Usage；
- Latency；
- Cost；
- No-hit / Refusal。

线上指标不能完全替代离线 Ground Truth，两者互补。

---

## 6. 一个推荐 Scorecard

```text
Retrieval Recall@K
MRR / NDCG
Faithfulness
Correctness
Answer Relevance
Citation Correctness
Should-refuse Accuracy
P95 Latency
Cost / Query
```

不要只用一个综合分掩盖各层退化。

---

## 7. 🎯 面试怎么回答

> End-to-end RAG Evaluation 要同时看 Retrieval 和最终 Answer。常见维度包括 Correctness、Faithfulness、Answer Relevance、Citation、Completeness 和 Refusal。分层很重要，因为最终答案错可能来自 Parsing、Retrieval、Rerank、Context 或 Generation。Offline 用固定 Dataset 做可复现 Regression，Online 再结合用户反馈、No-hit、Latency 和 Cost 观察真实效果。

## 8. ⚠️ 易错点

- “RAGAS 一个总分就够了”；
- Retrieval 指标高就等于答案好；
- Correctness 和 Faithfulness 混为一谈；
- 只做 Offline，不看线上分布。

## 9. 🔍 继续追问

- Faithful but Wrong 怎么处理？
- Online 指标没有 Ground Truth 怎么办？
- Evaluation 如何覆盖多轮对话？

<details><summary>查看参考答案：为什么 Correctness 和 Faithfulness 必须分开？</summary>

因为 RAG 的目标不仅是“碰巧答对”，还要证明答案受知识源支持。模型可能凭参数知识答对但没有 Ground，也可能忠实引用一份过期错误文档。分开评估才能定位 Knowledge 与 Generation 的问题。

</details>
