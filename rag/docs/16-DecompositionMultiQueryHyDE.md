# 16｜Decomposition、Multi-query 与 HyDE

## 1. 先讲人话

有些 Query 本身就不是“一次 Search”能解决的问题。

例如：

> “比较 A 和 B 在 2025 年不同地区的退款规则差异，并说明哪些条款发生了变化。”

它至少包含：

- A 的规则；
- B 的规则；
- 时间版本；
- 地区；
- 差异比较。

这时需要把一个复杂 Query 变成多个 Retrieval 子任务。

---

## 2. Query Decomposition

把复杂问题拆成多个可检索子问题：

```text
Q
├── Q1
├── Q2
└── Q3
```

例如：

```text
Q1：A 在华东地区 2025 年退款规则
Q2：B 在华东地区 2025 年退款规则
Q3：两者规则变更历史
```

然后分别召回，再合并 Evidence。

---

## 3. Multi-query

Multi-query 不是拆逻辑步骤，而是对**同一意图生成多个表达**：

```text
“Redis 为什么快？”
→ Redis 高性能原因
→ Redis 单线程与 IO 多路复用
→ Redis 内存访问和数据结构优势
```

不同表达可能覆盖不同语义区域，提高 Recall。

代价是候选数、请求数和重复结果增加。

---

## 4. HyDE

HyDE 的典型思想是：

```text
Query
→ 生成一个“假想答案 / 假想文档”
→ 对假想文本做 Embedding
→ 用它去检索真实文档
```

为什么可能有效？

因为短 Query 与答案文档的表达风格差异可能很大。假想答案更接近“文档侧语言”。

但风险也明显：

- 假想答案可能带偏；
- 成本增加；
- 对精确 Keyword Query 未必适合。

---

## 5. 三者区别

| 方法 | 核心目标 |
|---|---|
| Rewrite | 改善同一个 Query 的表达 |
| Multi-query | 用多个表达扩大同一意图召回 |
| Decomposition | 把复杂问题拆成多个子问题 |
| HyDE | 生成更接近文档分布的假想文本再检索 |

---

## 6. Decomposition 的最大风险：信息合并

拆开容易，重新合并 Evidence 才难。

例如子问题 Q1 和 Q2 来自不同版本文档，最终比较时必须保留：

```text
source
version
subquery_id
```

否则 LLM 可能把不同来源的事实混起来。

---

## 7. 什么时候值得用

### 适合 Decomposition

- 多实体比较；
- 多跳问题；
- 一个 Query 含多个约束；
- 需要分别查不同知识域。

### 适合 Multi-query

- 用户表达短且模糊；
- Corpus 用词和 Query 风格差异大；
- Dense Recall 不稳定。

### 适合 HyDE 实验

- Query 很短；
- 文档表达更正式；
- 普通 Query Embedding Recall 较差。

---

## 8. 怎样评估

比较 Baseline：

```text
Raw Query Retrieval
vs Rewrite
vs Multi-query
vs Decomposition / HyDE
```

观察：

- Recall@K；
- Unique Relevant Docs；
- Duplicate Candidate Rate；
- Latency / Cost；
- End-to-end Answer Quality。

---

## 9. 🎯 面试怎么回答

> Rewrite、Multi-query、Decomposition 和 HyDE 解决的问题不同。Rewrite 改善表达，Multi-query 用多个等价表达扩大召回，Decomposition 把复杂问题拆成多个可检索子任务，HyDE 用假想答案/文档把 Query 映射到更接近语料的表示。它们都会增加复杂度和成本，因此需要在真实 Evaluation Dataset 上和 Raw Query Baseline 比较，而不是默认打开。

## 10. ⚠️ 易错点

- “复杂 Query 一律 Decompose”；
- Multi-query 只增加重复候选却没有去重；
- HyDE 生成内容被误当成真实 Evidence；
- 子查询结果合并时丢 Source / Version。

## 11. 🔍 继续追问

- Multi-query 怎样去重？
- Decomposition 怎样避免错误传播？
- HyDE 的假想答案为什么不能直接给用户？

<details><summary>查看参考答案：HyDE 生成的内容为什么不是 Evidence？</summary>

因为它是模型生成的假想文本，只用于改善检索表示，不来源于真实知识源。最终回答仍必须 Ground 在真实检索结果上。

</details>
