# 06｜Query Understanding & Retrieval Planning：Lifecycle、Rewrite、Clarification、Decomposition、HyDE 与 No-hit

RAG 在线链路不能把用户原句直接当作唯一检索 Query。

一个成熟 Retrieval Request 需要回答：

```text
用户到底在问什么？
要不要改写？
问题是否需要拆分？
是否应该生成多个 Query？
是不是缺少必要信息？
什么时候应该拒绝检索结果并说“证据不足”？
```

所以 Request Lifecycle、Rewrite、Clarification、Decomposition、Multi-query、HyDE 和 No-hit 都属于同一个 Query Planning 子系统。

---

## 1. 一次 Retrieval Request 的完整入口

可以抽象为：

```text
Raw User Query
→ Normalize
→ Context / Intent Analysis
→ Permission / Tenant Scope
→ Query Plan
→ Retrieval
→ Candidate Validation
→ Evidence / No-hit Decision
```

Query Planning 的目标不是“让句子更漂亮”，而是生成更适合知识库检索的查询计划。

---

## 2. Query Normalization

基础处理可以包括：

- Unicode / whitespace normalization；
- 语言检测；
- 拼写/格式修复；
- 去掉明显无关 wrapper；
- 保留 ID、Code、数字等精确信号。

不要做会破坏业务语义的过度 Normalize。

例如：

```text
ErrorCode E1042
```

不能为了“语义化”变成泛泛的“系统报错”。

---

## 3. Query Rewrite 解决什么

用户 Query 可能：

```text
太口语
缺少实体全称
包含代词
依赖聊天历史
与知识库术语不一致
```

Rewrite 可以把：

```text
“它多久过期？”
```

结合上下文改写成：

```text
“Enterprise Trial Token 的有效期是多少？”
```

这样 Retriever 更容易命中正确文档。

---

## 4. Rewrite 最大风险：Query Drift

模型可能把原意改掉：

```text
user asks A
rewrite becomes A+B or C
```

所以要保留：

```text
original_query
rewritten_query
rewrite_reason / trace
```

并在 Eval 中单独分析：

```text
Original Search vs Rewritten Search
```

Rewrite 不是天然提升。

---

## 5. Clarification：信息不足时不要猜

例如：

```text
“怎么配置？”
```

但系统不知道用户问：

```text
Redis?
Model API?
Agent Tool?
```

与其生成一个自作主张 Query，不如：

```text
ask clarification
```

这属于 Retrieval Planning 的一部分。

判断标准是：

> 缺失信息是否会显著改变检索空间或答案。

---

## 6. Query Decomposition

复杂问题可能包含多个独立事实：

```text
“比较 A 和 B 的价格、权限模式和部署方式。”
```

可以拆成：

```text
A price vs B price
A/B permission model
A/B deployment model
```

分别检索，再在上层组合 Evidence。

适合：

- Multi-hop；
- Comparison；
- 多实体；
- 多约束问题。

但分解越多，Latency / Cost / Fusion 也会上升。

---

## 7. Multi-query

同一个意图可以生成多个检索表达：

```text
“如何处理缓存雪崩？”
→ cache avalanche mitigation
→ redis mass expiration protection
→ cache layer outage fallback
```

多路召回后合并候选。

价值：

```text
提高 Query Coverage
```

风险：

```text
Candidate Explosion
Latency
重复结果
Query Drift
```

所以需要 Fusion / Dedup 和 Candidate Budget。

---

## 8. HyDE 的直觉

HyDE = Hypothetical Document Embeddings。

它先让模型生成一个“可能的答案/文档”，再对这段假设文本做 Embedding：

```text
Query
→ hypothetical answer/document
→ embedding
→ dense retrieval
```

直觉是让 Query Representation 更像知识库中的 Document Representation。

但风险包括：

- 模型假设错误；
- 把错误细节写进 Query Representation；
- 增加一次模型调用；
- 对某些领域没有收益。

必须通过 Eval 决定是否使用。

---

## 9. History-aware Query

多轮对话中：

```text
User: 什么是 HNSW？
User: 那 M 调大有什么影响？
```

第二问需要引用第一轮实体。

正确做法不是把完整聊天历史直接塞进 Retriever，而是提取/生成：

```text
standalone retrieval query
```

同时保留原 Query 供回答语气和上下文使用。

---

## 10. Query Planning 要考虑 Retriever 类型

Dense 更擅长语义表达；Sparse 更擅长精确词。

所以 Query Planner 可以决定：

```text
dense query text
sparse query terms
metadata filter
retrieval route
```

例如 ID 型 Query：

```text
“E1042”
```

不应该被 Rewrite 成只剩自然语言解释，把精确 Token 丢掉。

---

## 11. Metadata / Permission Scope 应先进入 Plan

Query Plan 不只是文本。

它还应带：

```text
tenant_id
permission_scope
document_type
time range
product
version
```

这些硬约束应该进入 Retrieval，而不是拿到结果后才做权限过滤。

---

## 12. No-hit 是正常结果，不是异常

如果知识库没有足够 Evidence，正确答案可能是：

```text
No reliable evidence found
```

而不是让模型凭参数知识补全。

所以需要定义：

- Candidate Threshold；
- Minimum Evidence；
- Required Source Count；
- Conflict Handling；
- Refusal Policy。

---

## 13. Threshold 为什么不能只看 Vector Score

相似度 Score 没有跨模型统一语义。

No-hit 判断可以综合：

```text
Dense Score
Sparse Match
Reranker Score
Metadata Match
Query Type
Historical Eval
```

一个固定 `cosine < 0.8 → no hit` 通常过于粗糙。

---

## 14. Conflict Evidence 怎么办

如果检索到：

```text
Policy v1: 30 days
Policy v2: 14 days
```

不能简单取最高 Score。

需要结合：

```text
Version
Effective Date
Authority
Source Priority
```

这正是 Corpus Governance 与 Query Planning 的连接点。

---

## 15. Query Plan 的可观测性

Trace 建议记录：

```text
original query
conversation context used
rewritten query
subqueries
HyDE text if any
filters
retrieval route
no-hit decision
```

否则 Bad Case 很难知道是“Retriever 差”还是“Planner 把 Query 改坏了”。

---

## 16. 常见错误

- 所有 Query 都先 Rewrite：可能引入 Drift。
- Multi-query 越多 Recall 越高越好：成本和噪声也上升。
- HyDE 是标准必选组件：必须 Eval。
- No-hit 是系统失败：它是重要安全输出。
- Clarification 会降低体验，所以永远不问：盲猜可能更差。
- Query Rewrite 应替代原 Query：原始输入必须保留用于 Trace/Eval。

---

## 17. 面试怎么答

### Q：Query Rewrite 为什么有用？

> 用户 Query 往往有代词、口语、缺实体或与知识库术语不一致，Rewrite 可以生成更独立的检索表达。但它也可能 Query Drift，所以要保留原 Query、记录 Rewrite，并用真实 Eval 对比是否真的提高 Retrieval。

### Q：什么时候做 Multi-query / HyDE？

> 当单一 Query 表达不足、语义空间不容易命中时可以作为 Recall 增强候选，但两者都会增加成本和噪声，必须受 Candidate Budget 和 Eval 约束，而不是默认开启。

### Q：RAG 没召回结果怎么办？

> 应把 No-hit 作为正常系统状态，根据历史 Eval 校准的 Evidence/Reranker 阈值、权限和版本判断是否有足够证据；证据不足就拒答或澄清，而不是让模型自由补全。

---

## 18. 自测

<details><summary>1. Rewrite 和 Clarification 的边界是什么？</summary>
能从已有上下文稳定恢复意图时可 Rewrite；关键信息缺失且不同选择会改变检索空间时应 Clarify。
</details>

<details><summary>2. Multi-query 最大的 Production 风险是什么？</summary>
候选量、Latency 和噪声成倍增长，需要 Dedup/Fusion/Candidate Budget 控制。
</details>

<details><summary>3. 为什么 No-hit 是可靠 RAG 的必要能力？</summary>
因为知识库不可能覆盖所有问题，强行生成会把“没有证据”转成 Hallucination 风险。
</details>
