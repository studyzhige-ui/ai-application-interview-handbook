# 23｜Top-K、Threshold 与 Candidate Budget

## 1. 先讲人话

RAG 里不是只有一个 K。

通常会同时存在：

```text
Dense Top-N
Sparse Top-N
Fusion Candidate Count
Rerank Top-N
Final Context Top-K
```

所以“Top-K 设多少”真正问的是：

> **每一层应该保留多少候选，才能在 Recall、Noise、Latency 和 Token Cost 之间取得平衡。**

---

## 2. K 太小的问题

- Relevant Evidence 可能没进入候选；
- Multi-hop 问题覆盖不足；
- Parent / Neighbor Expansion 没有足够起点。

表现为：

```text
Recall@K 低
No-hit 高
答案缺关键证据
```

---

## 3. K 太大的问题

- Rerank Cost 增加；
- Context Noise 增加；
- Token Cost 增加；
- 相似重复块增多；
- 延迟上升。

因此不能为了 Recall 无限增大 K。

---

## 4. Retrieval K 与 Final Context K 不一样

一个常见模式：

```text
Retrieval Top-50
→ Fusion 40
→ Rerank 20
→ Diversity / Expansion
→ Final Context 5–8
```

前面偏 Recall，后面偏 Precision 和 Token Budget。

---

## 5. Threshold 与 K 的关系

Top-K 是“最多取多少”；Threshold 是“最低质量要求”。

两者可以一起使用：

```text
Top-K = 10
且 score >= threshold
```

这样候选不足时可以少于 10，而不是为了凑数把弱相关内容也塞进 Context。

---

## 6. Candidate Budget 应按阶段分配

可以把整个 Pipeline 看成预算漏斗：

```text
Cheap Retrieval：宽
↓
Fusion：去重
↓
Expensive Rerank：窄
↓
LLM Context：更窄
```

贵的阶段应该处理更少 Candidate。

---

## 7. Query-adaptive K

并不是所有 Query 都需要相同 K。

例如：

- 单事实 Lookup：较小 K；
- 多实体比较：较大 K；
- 多跳问题：可能需要分解后分别检索；
- 高置信精确匹配：可以较早停止。

这就是动态 Candidate Budget。

---

## 8. 怎样调 K

建议画曲线：

```text
K
→ Recall@K
→ End-to-end Quality
→ P95 Latency
→ Context Token
→ Cost
```

当 Recall 已经趋于饱和，而 Latency / Token 继续增长时，就能看到边际收益变小。

---

## 9. 🎯 面试怎么回答

> RAG 中通常有多层 Candidate Budget，而不是一个 Top-K。Retrieval 阶段 K 偏大以保证 Recall，Fusion/Rerank 逐步缩小，最终 Context K 受 Token Budget 和 Noise 限制。Threshold 用来阻止弱相关候选为了凑 K 进入上下文。参数应通过 Recall、End-to-end Quality、Latency 和 Token Cost 曲线验证，也可以按 Query 类型动态调整。

## 10. ⚠️ 易错点

- “K 越大 Recall 越高，所以越好”；
- Retrieval K = Final Context K；
- 不设 Threshold，低质量候选强行进入 Context；
- 只看 Recall，不看最终 Answer 和成本。

## 11. 🔍 继续追问

- Multi-hop Query 如何分配 Candidate Budget？
- Rerank Top-N 太小会有什么问题？
- 如何判断 Recall 已经饱和？

<details><summary>查看参考答案：为什么最终 Context K 往往比 Retrieval K 小很多？</summary>

因为 Retrieval 阶段的目标是不要漏，而 LLM Context 的目标是只保留高价值、互补、可 Ground 的证据。直接把大量候选塞进 Context 会增加噪声和成本，并可能让模型更难使用真正关键的信息。

</details>
