# 15｜Query Normalize / Rewrite / Intent / Clarification

## 1. 先讲人话

用户的原始 Query 不一定适合直接检索。

例如：

> “上次那个报错怎么处理？”

其中可能缺少对象、版本和上下文。Query Transformation 的目标是：

> **在不改变用户意图的前提下，把问题变成更适合检索的表达；如果信息不足，就先澄清，而不是强行猜。**

---

## 2. Query Normalize

这是最轻的一层：

- 统一大小写；
- 规范日期 / 单位 / 产品名；
- 去除明显噪声；
- 保留原始 Query。

Normalize 应尽量确定性，避免语义漂移。

---

## 3. Query Rewrite

Rewrite 常见用途：

- 把口语改成文档术语；
- 补充已知上下文；
- 去掉对话中的代词；
- 将问题改成更适合 Search 的表达。

例如：

```text
原问：这个模型为什么这么慢？
上下文：讨论的是 vLLM 服务
Rewrite：vLLM 推理服务 TTFT / TPOT 延迟高的常见原因
```

---

## 4. Intent Recognition

Intent 可以决定 Retrieval Plan：

```text
Definition
Troubleshooting
Policy Lookup
Exact Identifier Lookup
Comparison
Multi-hop Question
```

例如错误码、订单号等 Exact Lookup，可能更适合 Sparse / Keyword，而不是纯 Dense。

---

## 5. Clarification

最容易被忽略的一步。

如果 Query 存在关键歧义：

```text
“退款规则是什么？”
```

但系统同时有国内 / 海外、会员 / 非会员、不同地区规则，那么最可靠的动作可能是先问：

> “你指哪个地区 / 产品？”

这比检索一堆互相冲突的知识再让 LLM 猜更安全。

---

## 6. Rewrite 的风险

### Semantic Drift

LLM Rewrite 把用户真实意图改掉。

### Over-specification

Rewrite 自己添加了用户没说的条件。

### Loss of Exact Terms

专有名词、错误码、产品编号被“自然语言化”，反而伤害 Sparse Retrieval。

所以常见做法是：

```text
保留 Raw Query
+ Rewrite Query
必要时两者并行检索
```

---

## 7. 怎样评估 Rewrite

不要只看“Rewrite 看起来更漂亮”。至少比较：

- Recall@K；
- No-hit Rate；
- Query Drift Rate；
- End-to-end Correctness；
- Clarification Rate；
- Latency / Token Cost。

---

## 8. 🎯 面试怎么回答

> Query Transformation 包括 Normalize、Intent、Rewrite 和 Clarification。Rewrite 的目标不是把问题写得更长，而是让它更适合检索，同时保持用户意图。对于信息不足或歧义很大的 Query，应该先 Clarify，而不是盲目搜索。Production 中要保留 Raw Query，并通过 Recall、Drift 和最终 Answer Quality 验证 Rewrite 是否真的有效。

## 9. ⚠️ 易错点

- “所有 Query 都先用 LLM Rewrite”；
- Rewrite 后不保留原 Query；
- 错误码 / 专有名词被改写掉；
- Query 不完整时强行回答。

## 10. 🔍 继续追问

- Rewrite 和 Multi-query 有什么区别？
- Intent 用 Rule、小模型还是 LLM？
- 怎样检测 Rewrite Semantic Drift？

<details><summary>查看参考答案：什么时候应该 Clarify 而不是 Rewrite？</summary>

当缺失信息会直接决定检索范围或答案正确性，例如地区、产品、版本、时间范围时，应优先澄清。Rewrite 只能改善表达，不能可靠创造用户没有提供的关键事实。

</details>
