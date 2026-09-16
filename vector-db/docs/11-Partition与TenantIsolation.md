# 11｜Partition / Namespace / Tenant Isolation

Metadata Filter 解决“查询时筛选”，但当数据规模和租户数量继续增长时，还会自然出现另一个问题：

> **要不要从物理或逻辑上先把数据分开？**

这就是 Partition / Namespace / Tenant Isolation。

---

## 1. 为什么需要 Partition

假设一个 SaaS AI 平台有：

```text
10,000 tenants
100 million vectors
```

每次 Query 都是：

```text
tenant_id = X
```

如果所有租户完全混在一起：

```text
全局 ANN
+
tenant filter
```

可能带来：

- Filter Selectivity 极低；
- ANN 搜索浪费；
- 安全边界更复杂；
- 运维 / 删除 / 迁移困难。

因此可能希望：

```text
先路由到某个 Partition / Namespace
→ 再做 ANN
```

---

# 2. Partition 和 Metadata Filter 的区别

可以先建立直觉：

```text
Metadata Filter
= Query-time 条件

Partition / Namespace
= 更粗粒度的数据组织 / 路由边界
```

例如：

```text
Partition by tenant group
Filter by language / version
```

或：

```text
Namespace per tenant
```

具体能力取决于产品。

---

# 3. 每个 Tenant 一个 Collection 好吗

不一定。

优点：

```text
隔离直观
删除方便
配置独立
```

但如果：

```text
100,000 tenants
→ 100,000 collections
```

可能带来：

```text
Metadata 管理开销
Index 数量爆炸
小索引碎片化
运维复杂
```

所以多租户常见策略有：

```text
Shared Collection + tenant_id Filter
Partition / Namespace by tenant group
Large Tenant Dedicated Collection
```

需要按规模设计。

---

# 4. Tenant Isolation 不只是性能问题

它首先也是安全问题。

必须保证：

```text
Tenant A
绝不能看到 Tenant B 的向量 / Chunk
```

所以隔离通常需要多层：

```text
Auth / Authorization
→ Query 构造
→ Vector DB Filter / Namespace
→ Result Validation / Audit
```

不要把安全只交给：

```text
LLM Prompt
```

---

# 5. Partition Key 怎么选

好的 Partition Key 通常希望：

```text
Query 常携带
数据分布较均匀
能显著减少搜索范围
生命周期相对独立
```

例如：

```text
tenant_group
region
knowledge_base
```

但如果按一个高度倾斜字段分：

```text
99% 数据都在一个 Partition
```

就失去扩展价值。

---

# 6. Partition 太细会怎样

过细 Partition 可能带来：

```text
很多小索引
Build / Metadata overhead
Query fan-out
资源碎片
难以平衡
```

所以：

> Partition 是为了让 Query / Lifecycle 更简单，而不是越细越好。

---

# 7. 跨 Partition Query 怎么办

如果 Query 需要：

```text
搜索多个 tenant group
多个知识库
```

可能发生：

```text
fan-out to N partitions
→ 每个 partition Top-K
→ merge global Top-K
```

Fan-out 越大：

```text
Latency
Network
CPU
Merge Cost
```

都会上升。

这和普通分布式数据库的 Scatter-Gather 很类似。

---

# 8. Partition 与 Shard 的区别

容易混淆。

可以先这样理解：

```text
Partition / Namespace
偏逻辑数据组织 / Query Routing

Shard
偏底层水平扩展 / 数据分布到不同节点
```

一个 Partition 可能跨 Shard，一个 Shard 也可能承载多个逻辑 Partition。

具体映射取决于产品。

---

# 9. 多租户容量规划

不能只看总数据量。

要看：

```text
Tenant Size Distribution
Hot Tenant QPS
Filter Selectivity
Per-tenant Growth
Deletion / Rebuild Pattern
```

如果一个超大客户占：

```text
50% QPS
40% vectors
```

就可能需要：

```text
dedicated capacity / partition
```

而不是继续和长尾小租户完全混布。

---

# 10. 面试怎么答

## Q：多租户 Vector DB 怎么设计？

🎯 **建议回答**：

> 我会先把 Tenant Isolation 当成安全边界，再考虑性能。小到中等规模可以共享 Collection，用 tenant_id 做强制 Filter；规模扩大后，可以按 tenant group / knowledge base 做 Namespace 或 Partition，让 Query 先路由再 ANN。超大租户可能独立 Collection 或 Capacity。关键是避免 collection-per-tenant 无限膨胀，同时也避免所有租户完全混在一个巨大索引里导致 Filter Selectivity 和热点问题。

---

# 11. 高频易错点

⚠️ **Partition = Shard。** 不一定，逻辑组织和物理分片是两个层次。

⚠️ **每 Tenant 一个 Collection 最安全，所以永远最好。** 大量小 Collection 可能带来严重运维成本。

⚠️ **多租户隔离只靠 tenant_id Filter 就绝对安全。** 还需要 Auth、Query Construction、Audit 等多层保证。

---

# 12. 本章自测

<details><summary>1. 为什么 collection-per-tenant 在大量长尾租户下可能不合适？</summary>

因为会产生大量小索引和元数据对象，带来资源碎片、索引管理和运维复杂度。
</details>

<details><summary>2. Partition 和 Shard 最核心的区别是什么？</summary>

Partition 更偏逻辑数据组织和查询路由；Shard 更偏底层水平扩展和节点间数据分布。
</details>
