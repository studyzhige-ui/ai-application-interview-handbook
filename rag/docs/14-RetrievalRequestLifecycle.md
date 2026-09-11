# 14｜一次 Retrieval Request 怎样执行

## 1. 先讲人话

真正的 Retrieval 不是一句：

```text
vector_db.search(query)
```

而是一条有输入契约、过滤、候选生成、排序、预算和日志的执行链。

一个典型请求可以展开为：

```text
User Query
→ Normalize
→ Intent / Rewrite
→ Metadata / Permission Filter
→ Dense / Sparse Candidate Generation
→ Fusion
→ Rerank
→ Top-K / Threshold
→ Context Expansion
→ Evidence Package
```

---

## 2. Query Normalize

常见处理：

- 去除无意义空白；
- 语言检测；
- 标准化日期 / 单位 / 产品名；
- 保留原 Query，避免不可逆改写。

原则：

> **Normalize 是让查询更稳定，不是擅自改变用户意图。**

---

## 3. Retrieval Plan

Query 不一定都走同一条路径。

例如：

```text
精确编号 / 错误码
→ Sparse / Keyword 权重更高

自然语言概念问题
→ Dense

复杂多跳问题
→ Decomposition / Multi-query

Query 信息不足
→ Clarification
```

这说明 Retrieval 可以有 Plan，而不是固定 Pipeline。

---

## 4. Filter 应尽早参与

Tenant、Permission、Version、Language、Product 等 Filter 如果太晚才做：

- 候选池会被无权 / 无效内容占满；
- Post-filter 后可能没有足够结果；
- 甚至存在安全泄露风险。

因此 Filter 的位置是 Retrieval Design 的核心之一。

---

## 5. Candidate Budget

每一层都需要预算：

```text
Dense Top-50
Sparse Top-50
↓
Fusion Top-40
↓
Rerank Top-20
↓
Final Top-5
```

预算决定：

- Recall；
- Latency；
- Rerank Cost；
- Context Token。

---

## 6. Retrieval Result 不是只有 text

推荐返回：

```text
chunk_id
text
source
section
retrieval_score
retrieval_route
fusion_rank
rerank_score
metadata
version
```

这样 Evaluation 和 Trace 才能解释“为什么这个 Chunk 被选中”。

---

## 7. Observability 前置

一次 Retrieval 至少应可记录：

```text
raw_query
rewritten_query
filters
retrieval_routes
candidate_ids + scores
fusion
rerank
final_ids
latency
index_version
```

否则遇到 Bad Case 时只能猜。

---

## 8. 🎯 面试怎么回答

> Production Retrieval Request 通常包含 Query Normalize、Rewrite/Intent、Permission/Metadata Filter、多路 Candidate Generation、Fusion、Rerank、Top-K/Threshold 和 Context Expansion。每一层都有 Candidate Budget 与 Latency/Cost Trade-off。Result 还要保留 route、score、source、version 等 Trace 信息，才能做 Evaluation 和 Bad Case Attribution。

## 9. ⚠️ 易错点

- “Retrieval 就是向量库 Top-K”；
- Filter 放到生成答案后才处理；
- 不记录候选和分数，只保留最终答案；
- 所有 Query 强制走同一个固定策略。

## 10. 🔍 继续追问

- 哪些 Query 应该跳过 Dense Retrieval？
- Candidate Budget 怎样定？
- Filter 在 ANN 前后分别有什么问题？

<details><summary>查看参考答案：为什么要保留原 Query 和 Rewrite 后 Query？</summary>

因为 Rewrite 本身可能出错。保留两者才能判断 Retrieval 失败是用户问题本身难，还是改写改变了意图；也方便离线回放和 Regression。

</details>
