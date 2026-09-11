# 17｜Retrieval Miss、Threshold、No-hit 与 Refusal

## 1. 先讲人话

RAG 最危险的行为之一是：

> **明明知识库没找到可靠证据，系统却继续让模型“像知道一样”回答。**

因此 Production RAG 必须显式设计 No-hit / Low-confidence 路径。

---

## 2. 什么叫 Retrieval Miss

不是只有“0 个结果”才叫 Miss。

至少包括：

- 没有候选；
- 候选分数低；
- 候选与 Query 主题不符；
- 有相关文档，但缺答案所需关键证据；
- 结果版本过期；
- 权限过滤后没有可用证据。

所以 Miss 更接近：

> **当前 Evidence 不足以支持可靠回答。**

---

## 3. Threshold 不是一个万能数字

相似度阈值受很多因素影响：

- Embedding Model；
- Distance Metric；
- Corpus 分布；
- Query 类型；
- ANN Index；
- Filter；
- 是否经过 Rerank。

因此不能把某个 `0.8` 当成跨系统标准答案。

---

## 4. 常见 No-hit 策略

### Refuse

高风险知识域中，没有可靠 Evidence 就明确拒答。

### Clarify

Query 缺少关键条件时先追问用户。

### Fallback Retrieval

例如：

```text
Dense Miss
→ Sparse / Keyword
→ Wider Filter / Alternate Index
```

但不能为了“必须回答”无限放宽安全边界。

### General Model Answer

只有业务允许、并且 UI 明确区分“知识库答案”与“模型一般知识”时才考虑。

---

## 5. Confidence 不应只看一个 Score

可以综合：

```text
retrieval_score
rerank_score
source_count
source_agreement
coverage
version / freshness
query_type
```

例如 Top-1 很高，但只有一条旧文档且缺关键字段，不一定可靠。

---

## 6. No-hit Evaluation

Evaluation Dataset 里应该专门包含：

- Corpus 外问题；
- 缺信息问题；
- 过期知识；
- 权限不可见知识；
- 恶意诱导问题。

指标不仅是“答对率”，还包括：

```text
Should Answer → Answer
Should Refuse → Refuse
```

可以把错误分成：

- False Refusal；
- Unsafe Answer。

---

## 7. AI 应用案例

企业政策问答中，用户问“今年出差补贴标准”，但知识库只有去年版本。

错误做法：

> 召回去年制度 → 模型直接回答。

更好的做法：

```text
发现 latest_valid_version 缺失
→ 标记 Freshness Risk
→ 返回无法确认最新标准
→ 提示用户查看权威来源
```

---

## 8. 🎯 面试怎么回答

> Retrieval Miss 不只是 Top-K 为空，而是当前证据不足以可靠支持答案。No-hit 设计通常结合 Retrieval/Rerank Score、Coverage、Source Agreement、Version 和 Query 类型，决定 Refuse、Clarify 或 Fallback。阈值不能照抄固定数字，需要在包含可回答与不可回答问题的 Evaluation Dataset 上校准，并同时关注 False Refusal 和 Unsafe Answer。

## 9. ⚠️ 易错点

- “向量分数低于 0.8 就拒答”；
- 有结果就一定回答；
- Fallback 不断放宽直到搜到东西；
- 只测试可回答问题，不测试 Should-refuse Case。

## 10. 🔍 继续追问

- No-hit 阈值怎样校准？
- Rerank Score 可以直接当概率吗？
- 高风险场景为什么要更保守？

<details><summary>查看参考答案：为什么 No-hit 不能只依赖 Top-1 Similarity？</summary>

因为 Similarity 只反映当前表示空间中的接近程度，不代表事实完整、版本有效、权限合法或足以回答。可靠性需要结合候选覆盖、来源、版本和任务风险判断。

</details>
