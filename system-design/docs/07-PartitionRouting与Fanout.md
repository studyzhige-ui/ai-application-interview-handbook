# 07｜Partition、Routing、Fan-out 与 Rebalance

当单机容量、QPS 或故障域不够时，系统会自然进入分布式数据问题。

但“分片”不是：

> **数据太大 → hash(id) % N。**

真正问题是：

> **怎样把数据和请求分到多个节点，同时控制热点、Fan-out、扩容迁移和查询复杂度？**

---

## 1. 为什么要 Partition / Shard

常见原因：

```text
单机存不下
单机写不动
单机读不动
需要故障隔离
需要租户隔离
```

不同原因会导致不同 Partition Key。

---

# 2. Partition Key 决定 Query Routing

例如按：

```text
user_id
```

如果查询总是：

```text
GET user/{id}
```

路由非常直接。

但如果经常：

```text
查询整个国家过去一小时的 Top100
```

就可能跨所有 Shard。

所以 Key 不能只追求“均匀”，还要看 Query Pattern。

---

# 3. Hash Partition

直觉：

```text
hash(key) → shard
```

优点：

- 分布通常较均匀；
- Point Query 容易路由。

缺点：

- Range Query 差；
- 扩容迁移复杂；
- 业务局部性可能丢失。

如果简单：

```text
hash(key) % N
```

N 改变后大量 Key 会重新映射。

所以真实系统会考虑更稳定的映射策略。

---

# 4. Range / Time Partition

例如：

```text
2026-09-01
2026-09-02
2026-09-03
```

适合：

- Time-range Query；
- Retention；
- Hot / Cold Tier；
- 批量删除旧数据。

但当前时间段可能成为写热点。

---

# 5. Tenant / Domain Partition

SaaS 常见：

```text
tenant_id → routing group
```

好处：

- Query 局部；
- 迁移租户方便；
- 安全边界清楚。

问题：

```text
一个超大 Tenant
≫ 其他 Tenant
```

会形成 Hot Partition。

所以常见：

```text
Small Tenant shared
Large Tenant dedicated / sub-sharded
```

---

# 6. Fan-out 为什么贵

如果 Query 不知道结果在哪：

```text
Query
→ Shard A
→ Shard B
→ Shard C
→ ...
→ Merge
```

成本包括：

```text
Network
CPU
Tail Latency
Partial Failure
Merge
```

Shard 越多，不代表 Query 越快。

尤其 Top-K：

```text
每个 Shard local Top-K
→ coordinator merge
```

需要考虑局部 Recall、Score 与 Oversampling。

---

# 7. Replica 与 Shard 不同

```text
Shard
→ 数据水平拆分

Replica
→ 同一份数据多个副本
```

Replica 可以：

- 提升可用性；
- 扩读；
- 降低单节点故障影响。

但会增加：

```text
Storage
Replication Lag
Failover Complexity
```

---

# 8. Rebalance：扩容不是“加一台机器”

新增节点后，需要：

```text
Move Partition
Update Routing
Warm Cache
Build Replica / Index
Limit Migration Rate
```

如果迁移抢占太多：

```text
Network / Disk / CPU
```

可能让在线 P99 恶化。

所以 Rebalance 本身是一个生产负载。

---

# 9. Dual Read / Dual Write Migration 要谨慎

迁移数据时可能：

```text
Old Shard
New Shard
```

短期共存。

如果做 Dual Write：

```text
写 old 成功
写 new 失败
```

就产生一致性窗口。

更稳的迁移通常需要：

```text
Snapshot / Copy
→ Delta Catch-up
→ Validation
→ Traffic Cutover
→ Old Read-only / Cleanup
```

具体方案取决于数据系统。

---

# 10. Hot Shard 怎么发现

不要只看：

```text
Cluster total QPS
```

要看：

```text
per-shard QPS
P99
CPU
Storage
Queue
Key Distribution
Tenant Distribution
```

平均值可能看起来非常健康。

---

# 11. Partition 与系统边界

同一系统可能同时有多种 Partition：

```text
MySQL shard by user
Redis cluster by hash slot
Vector DB route by tenant / shard
Kafka partition by key
Object storage by time prefix
```

它们的 Key 不必相同，因为服务的问题不同。

但跨系统 Workflow 要考虑：

```text
是否会导致跨分片事务？
是否产生热点联动？
```

---

# 12. 🎯 面试怎么答

> 我会先根据访问模式决定 Partition Key，而不是只追求 hash 均匀。好的 Key 要同时考虑数据分布、Query Routing、热点和生命周期。任何跨 Shard Query 都要算 Fan-out 和 Tail Latency；扩容则不只是加机器，还包括数据迁移、Routing 更新、Cache Warmup 和 Rebalance 对在线负载的影响。多租户场景还要专门处理大 Tenant，不能假设 tenant size 均匀。

---

# 13. 本章自测

<details><summary>1. 为什么 hash(id) 很均匀仍可能是坏 Shard Key？</summary>
因为真实 Query 可能无法按 id 定位，需要每次 Fan-out 到所有 Shard；均匀分布不等于高效访问。
</details>

<details><summary>2. 为什么扩容时 P99 可能变差？</summary>
Rebalance 会占用网络、磁盘和 CPU，并触发 Cache/Index Warmup，与在线请求争资源。
</details>

<details><summary>3. 为什么大 Tenant 可能需要独立容量？</summary>
它可能在数据量和 QPS 上远超长尾租户，继续共享会形成热点并影响其他租户的隔离与 SLO。
</details>
