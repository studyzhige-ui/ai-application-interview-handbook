# 14. Metadata Filter、Pre-filter 与 Post-filter

真实 Vector Search 很少只有：

```text
给我最相似的 20 条
```

更常见的是：

```text
给我最相似的 20 条
AND tenant_id = 42
AND language = 'zh'
AND permission_group IN (...)
AND current_version = true
```

这就是 Metadata Filter。

---

## 1. Filter 为什么是 Vector DB 的核心能力

如果没有 Filter：

```text
ANN 找到全局最相似结果
```

但业务可能要求：

```text
只能查当前租户
只能查当前知识库
只能查用户有权限的文档
只能查当前版本
```

所以：

> **相似度只是第一维约束，业务合法性通常来自 Metadata Filter。**

---

# 2. Pre-filter 是什么

直觉：

```text
先根据 Metadata 缩小合法候选集
→ 再在合法候选中做 Vector Search
```

优点：

```text
不会先找到一堆非法候选
```

但难点是：

```text
ANN Index 如何在被过滤后的稀疏子集里仍然高效导航？
```

如果 Filter 选择性极高，例如：

```text
1 亿条中只剩 1000 条
```

算法行为可能与无过滤情况完全不同。

---

# 3. Post-filter 是什么

直觉：

```text
先做 ANN Top-N
→ 再按 Metadata 删除不符合条件的结果
```

例如：

```text
先取 100 个
过滤后剩 7 个
```

问题：

```text
最终需要 Top20
但只剩 7 个
```

如果简单 Post-filter，就可能：

```text
结果数量不足
Recall 下降
```

需要：

```text
oversampling
iterative search
```

等策略补救。

具体实现依产品而定。

---

# 4. Pre-filter 和 Post-filter 不是简单二选一

现代 Vector DB 可能采用更复杂的：

```text
Filter-aware ANN
Bitmap / Inverted Index + ANN
Dynamic Candidate Expansion
Iterative Filtering
Partition Pruning
```

所以面试不要说：

> “Vector DB 都是先过滤再搜索。”

或者：

> “都只能搜索后过滤。”

正确表达：

> **不同产品、不同索引会有不同的 Filter Execution Strategy。**

---

# 5. Filter Selectivity 是什么

假设原数据 1 亿条。

Filter 后：

```text
5000 万 → selectivity 50%
100 万   → 1%
1 万     → 0.01%
```

选择性不同会直接影响：

```text
候选规模
ANN 导航
Latency
Recall
```

因此 Production Benchmark 必须包含真实 Filter 分布。

---

# 6. Tenant Filter 为什么不能只是应用层约定

错误模式：

```text
先全局 ANN
→ 应用层看 tenant_id
→ 不对就丢掉
```

这可能带来：

```text
跨租户数据泄漏风险
结果不足
额外开销
```

Tenant Isolation 应在：

```text
数据模型
Partition / Namespace
Metadata Filter
Authorization
```

多层共同保证。

安全不能只靠 Prompt。

---

# 7. Permission Filter 的难点

权限可能不是简单：

```text
owner_id = user_id
```

而是：

```text
user
→ role
→ team
→ document ACL
```

如果每个 Query 都构造一个超长：

```text
doc_id IN (...)
```

可能很昂贵。

因此需要考虑：

```text
permission group / ACL token
partitioning
precomputed access group
query-time filter complexity
```

完整授权模型属于 System Design / Backend Security，但 Vector DB 必须支持有效过滤边界。

---

# 8. Filter 与 ANN Recall 怎么分层排查

如果 Query 没召回：

先做：

```text
Exact + No Filter
Exact + Filter
ANN + No Filter
ANN + Filter
```

四组对照。

这样可以判断：

```text
Embedding / Corpus 问题？
Filter 太严格？
ANN Recall Loss？
ANN + Filter 组合问题？
```

这是非常实用的 Troubleshooting 方法。

---

# 9. Filter 字段也需要设计

如果经常过滤：

```text
tenant_id
kb_id
language
version
```

就应该确认产品是否对这些字段建立适合的 Scalar / Payload Index。

否则：

```text
Vector ANN 很快
但 Metadata Filter 很慢
```

整体 Query 仍然慢。

---

# 10. 面试怎么答

## Q：Vector Search 的 Metadata Filter 怎么做？

🎯 **建议回答**：

> Metadata Filter 会把语义近邻搜索和 tenant、permission、version 等结构化约束结合。实现上可能是 pre-filter、post-filter，或者 filter-aware ANN。Pre-filter 能保证候选先满足约束，但高选择性过滤会改变 ANN 导航；简单 post-filter 可能导致 Top-K 不足和 Recall 下降。所以我会把 Filter Selectivity 纳入 Benchmark，并分别对 Exact/ANN、有无 Filter 做对照，判断问题来自 Embedding、Filter 还是 ANN。

---

# 11. 高频易错点

⚠️ **Post-filter 只会变慢，不影响 Recall。** 可能导致结果不足或漏掉过滤后真正的 Top-K。

⚠️ **Tenant Filter 放应用层就够了。** 存在安全和质量风险。

⚠️ **ANN Benchmark 不需要带 Filter。** Production 结论可能完全失真。

---

# 12. 本章自测

<details><summary>1. 为什么简单 Post-filter 可能导致返回结果不足？</summary>

因为 ANN 先取出的候选中可能有大量不满足 Metadata 条件，过滤后剩余数量少于目标 Top-K。
</details>

<details><summary>2. 怎样区分 ANN Recall Loss 和 Filter 问题？</summary>

分别跑 Exact/ANN 与有无 Filter 的组合对照，观察丢失从哪一步开始。
</details>