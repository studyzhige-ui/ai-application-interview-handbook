# 27｜Evaluation Dataset、Ground Truth 与 LLM Judge

## 1. 先讲人话

没有代表真实业务的 Evaluation Dataset，所有“优化”都很容易变成：

> 只在几个自己挑的 Case 上看起来更好。

RAG Evaluation 的第一生产资料不是某个指标公式，而是：

```text
真实 Query
+ 可接受 Evidence
+ 可接受 Answer / Rubric
+ Should-answer / Should-refuse 标签
```

---

## 2. Dataset 从哪里来

常见来源：

- 线上真实 Query；
- 客服 / 搜索日志；
- 历史 Bad Case；
- 业务专家整理；
- 产品核心任务；
- 合成数据作为补充。

优先级通常是：

> **真实业务分布 > 人工想象的漂亮问题。**

---

## 3. Ground Truth 不只是标准答案

Retrieval Ground Truth 可以是：

```text
query
→ relevant document / chunk set
```

End-to-end Ground Truth 可以是：

```text
expected facts
forbidden claims
acceptable variants
required citations
should_refuse
```

这样比单一字符串 Exact Match 更适合生成式系统。

---

## 4. Dataset 要覆盖 Failure Slice

不能只放“容易答对”的问题。

至少包含：

- Exact Term；
- Semantic Query；
- Multi-hop；
- 长 Query；
- 模糊 Query；
- No-hit；
- 旧版本；
- 权限隔离；
- 冲突文档；
- 表格 / 多模态。

---

## 5. LLM Judge 能做什么

LLM Judge 很适合评估：

- Answer Relevance；
- Faithfulness；
- Correctness Rubric；
- Citation Support；
- 风格 / 格式。

但它不是绝对真值。

---

## 6. LLM Judge 的风险

- Position Bias；
- Verbosity Bias；
- 对某些模型 / 风格偏好；
- Judge 本身会 Hallucinate；
- Prompt 改动会改变评估标准；
- 被待评答案中的文本影响。

因此需要：

```text
Judge Prompt Version
Judge Model Version
Human Calibration Set
Agreement Check
```

---

## 7. Human Calibration

先抽一批 Case 由业务专家 / 人类标注，然后比较：

```text
LLM Judge
vs Human Label
```

观察一致率和主要分歧，再决定是否能把 Judge 用于大规模 Regression。

---

## 8. Dataset Versioning

Evaluation Dataset 也需要版本：

```text
dataset_v1
→ 加入线上新 Bad Case
→ dataset_v2
```

否则不同实验使用不同问题集，就无法公平比较。

---

## 9. 防止“对测试集过拟合”

如果每次看到 Eval 失败就针对固定问题写特例，最终系统可能只会刷榜。

建议保留：

- Development Set；
- Regression Set；
- Holdout Set；
- 新鲜线上抽样。

---

## 10. 🎯 面试怎么回答

> RAG Evaluation 的核心是先建立代表真实业务分布的数据集，包含 Query、Relevant Evidence、Answer Rubric、Should-refuse 等标签，并覆盖 Exact、Semantic、No-hit、Multi-hop、权限和版本等 Slice。LLM Judge 可以扩展评估规模，但需要固定 Judge Model/Prompt，并和人工标注做 Calibration，因为 Judge 自身也有偏差。Dataset 也必须版本化，用于长期 Regression。

## 11. ⚠️ 易错点

- 只用模型自动生成 Query 做全部评测；
- 把 LLM Judge 当绝对真值；
- 每次实验换 Dataset；
- Eval 集没有 No-hit / Permission 等困难 Case。

<details><summary>查看参考答案：为什么线上 Query 对 Evaluation 很重要？</summary>

因为真实用户的表达、歧义、长尾实体和失败分布通常和开发者人工构造的问题差异很大。没有真实分布，离线指标可能很好，上线仍大量失败。

</details>
