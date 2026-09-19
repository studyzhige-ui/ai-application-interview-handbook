# 12｜Production Governance：Freshness、Version、Permission、Tenant、Snapshot 与 Rollback

RAG 从 Demo 走向 Production 后，最大的变化之一是：

> **知识不是静态文件集合，而是持续变化、受权限约束、需要可回滚的数据产品。**

因此 Freshness / Incremental Update 和 Permission / Tenant 不应该割裂：它们共同定义“某个用户此刻允许看到哪一个版本的哪些证据”。

---

## 1. Freshness 是 RAG 的系统属性

假设公司政策今天更新：

```text
Source v2 available at 10:00
```

用户 10:05 查询，RAG 仍返回 v1。

即使 Retriever/LLM 完全正确，也是在基于过期事实回答。

所以 RAG Quality 不只有：

```text
semantic relevance
```

还包括：

```text
freshness / validity
```

---

## 2. 先定义 Freshness SLA

不同 Source 需要不同 SLA：

```text
产品文档 → 小时级
政策 → 日级
价格 → 分钟级
库存 / 订单 → 秒级，可能不适合异步 RAG
```

如果要求近实时强一致，直接调用业务 DB / API 可能比异步 Embedding Pipeline 更合理。

---

## 3. 增量更新的基本链路

```text
Source Change
→ Detect
→ Parse affected document
→ Chunk
→ Embed
→ Write new version
→ Validate
→ Make visible
→ Retire old version
```

重点：

> 不要先删旧数据，再慢慢构建新数据。

否则更新过程中会产生知识空窗。

---

## 4. Blue-Green Knowledge Generation

更稳健：

```text
Index Generation v1 serving
        │
        ├─ build v2 in background
        ↓
validate v2
        ↓
canary / shadow
        ↓
switch alias / route
        ↓
keep v1 for rollback
```

适用于：

- Embedding Model 升级；
- Chunk Strategy 改变；
- 大规模 Parser 升级；
- Index Migration。

代价是短期双份存储。

---

## 5. Full Rebuild 为什么需要 Snapshot Boundary

假设 Rebuild 需要 6 小时。

如果直接：

```text
scan current source
→ build
```

构建期间 Source 继续变化，最终生成的 Index 可能是“多个时间点混合状态”。

因此要有：

```text
Snapshot T0
→ Full Build
→ Capture Delta after T0
→ Replay Delta
→ Catch Up
→ Switch
```

这和数据库迁移 / CDC 思路相似。

---

## 6. Version 应该存在哪些层

至少可以区分：

```text
document version
chunk version
embedding version
index generation
```

Query Trace 要记录它实际命中的版本。

否则用户说：

> “昨天为什么回答 30 天，今天回答 14 天？”

你无法知道两次请求分别用了哪一代知识。

---

## 7. Rollback 为什么必须保留旧 Generation

新 Index 可能：

- Recall 回归；
- Parser Bug；
- ACL 丢失；
- Embedding 不兼容；
- 延迟过高。

如果旧版本已经立即清掉，只能重新全量构建。

所以可以：

```text
switch v2
→ observe
→ retire v1 after safety window
```

---

## 8. Permission 不是最后的 Post-filter

多租户系统里：

```text
User A
```

只允许看到 Tenant A / 某些 Group 文档。

权限必须进入 Retrieval Scope：

```text
Query
+ tenant_id
+ permission_scope
+ version/time constraints
→ Retriever
```

而不是：

```text
retrieve everything
→ send to LLM
→ UI hides unauthorized citation
```

因为敏感内容一旦进入模型 Context，就已经暴露。

---

## 9. ACL 怎样传播到 Chunk

Source 可能有：

```text
document-level ACL
```

派生 Chunk 必须继承或计算自己的：

```text
tenant_id
owner
group_ids
classification
visibility
```

并在每次 Rebuild/Update 中保持一致。

这也是为什么 Lineage 和 Data Model 重要。

---

## 10. Permission Change 也需要增量同步

即使正文不变：

```text
user removed from group
```

RAG 可见性也必须变化。

所以 Incremental Update 不只有 Content Change，还有：

```text
ACL Change
Tenant Move
Status Change
Effective Date Change
```

Metadata-only Update 也可能是 Critical Freshness Event。

---

## 11. Pre-filter vs Post-filter 的安全边界

Post-filter 可能用于某些性能实现，但安全上必须保证：

```text
unauthorized text
```

不会进入后续模型 Context 或泄露给调用者。

更理想是：

```text
permission-aware retrieval
```

让无权限数据尽量不成为候选。

---

## 12. Cache 也会造成权限与 Freshness 问题

例如 Semantic Cache Key 只有：

```text
query_embedding
```

可能跨：

- Tenant；
- Permission；
- Knowledge Version；

复用旧答案。

Cache Key / Namespace 必须包含：

```text
security scope
knowledge generation
```

否则新 Index 上线后仍返回旧 Cache Answer。

---

## 13. Time-aware Retrieval

对于有生效期的政策：

```text
valid_from
valid_to
```

Query 可以带：

```text
as_of_time
```

检索当时有效版本。

这对：

- 审计；
- 历史问答；
- 金融/法律；

非常有价值。

---

## 14. Delete / Revocation 要定义传播时间

当用户撤权或文档删除：

```text
多久以后必须不可检索？
```

这也是 SLA。

链路可能包含：

```text
Source
→ Event
→ Index
→ Replica
→ Cache
```

任一层延迟都可能出现越权窗口。

高敏场景可能需要：

- 请求时实时授权；
- Central Authorization；
- Short Cache TTL；
- Revocation Push。

---

## 15. Production 对账

定期检查：

```text
source document count
vs
manifest
vs
chunk count
vs
index count
```

还可以检查：

```text
missing latest version
orphan chunk
unauthorized chunk
stale generation
```

不要等用户发现旧文档才知道同步任务失败。

---

## 16. 监控指标

可以关注：

```text
source-to-index lag
failed ingestion jobs
stale document count
index generation age
ACL sync lag
orphan chunk count
cache hit by generation
rollback count
```

RAG 的 Observability 不应该只记录 Query Latency。

---

## 17. 常见错误

- 文档更新就直接覆盖旧 Vector：会有空窗/不可回滚风险。
- Embedding Rebuild 不需要 Snapshot：会混合不同时间点状态。
- Permission 最后再过滤即可：敏感内容可能已进入 LLM。
- 正文没变就无需更新索引：ACL/有效期也会变。
- 新 Generation 上线后 Cache 自然正确：Cache 也要按版本失效。
- Delete 只删 Vector DB 就完成：还可能有 Cache/Replica/旧 Generation。

---

## 18. 面试怎么答

### Q：RAG 知识库怎么不停服更新？

> 对小增量用 stable document/version 做增量 Parse/Chunk/Embed 后原子切换可见版本；大规模模型/Chunk 迁移则构建新 Index Generation，以 Snapshot Boundary 做全量，再 Replay 增量追平，通过 Eval/Canary 后切 Alias，并保留旧 Generation 供 Rollback。Query Trace 记录实际知识版本。

### Q：多租户 RAG 权限怎么做？

> 权限从 Source 就作为数据契约传播到 Chunk/Index，Query 带 tenant/ACL scope 做 permission-aware retrieval，无权限内容不能进入 LLM Context。还要治理 ACL Change、Cache Key、Replica/Index 同步和撤权 SLA，不能只在 UI 最后隐藏结果。

---

## 19. 自测

<details><summary>1. 为什么 Full Rebuild 要捕获 Delta？</summary>
因为构建期间 Source 仍在变化，不追增量会让新 Generation 缺失 T0 之后的数据。
</details>

<details><summary>2. 为什么 ACL Change 也是 Freshness 问题？</summary>
因为数据内容没变，但谁能看到它发生了变化，旧权限状态同样属于 stale knowledge state。
</details>

<details><summary>3. 为什么 Cache Key 需要 Knowledge Generation？</summary>
否则新知识上线后可能继续命中旧版本生成的答案或检索结果。
</details>
