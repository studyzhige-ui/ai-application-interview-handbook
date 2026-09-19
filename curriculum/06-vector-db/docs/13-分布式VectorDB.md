# 13｜Shard / Replica / Segment：分布式 Vector DB 基础

当一个 Vector Index 放不进单机内存，或者单机 QPS / 容量不够时，就会进入分布式问题。

这章不学某个产品架构图，而先学稳定抽象：

```text
Shard
Replica
Segment
Query Fan-out
Merge
Rebalance
```

---

## 1. 为什么要 Shard

假设：

```text
5 亿条向量
× 1536 dim
```

单机可能面临：

```text
Memory 不够
Index 不够
QPS 不够
Build 太慢
```

于是把数据水平拆到多个节点：

```text
Shard 1
Shard 2
Shard 3
...
```

这和普通分布式数据库的 Horizontal Sharding 思想相通。

---

# 2. Query 为什么需要 Fan-out

如果 Query 不知道真正最近邻在哪个 Shard：

```text
Query
├─ Shard A → local Top-K
├─ Shard B → local Top-K
└─ Shard C → local Top-K
        ↓
Coordinator Merge
        ↓
Global Top-K
```

这就是 Scatter-Gather。

Shard 越多：

```text
Fan-out
Network
Merge Cost
Tail Latency
```

都可能上升。

所以 Sharding 不是“节点越多越快”。

---

# 3. Partition Routing 能减少 Fan-out

如果 Query 明确：

```text
tenant_id = 42
```

而 tenant 42 已被路由到固定 Shard / Partition：

```text
Query 只访问部分节点
```

就能减少 Scatter-Gather。

所以前面的：

```text
Partition / Tenant Isolation
```

和分布式 Scale 是连在一起的。

---

# 4. Replica 解决什么

Replica 常见目的：

```text
High Availability
Read Scale
Fault Tolerance
```

例如：

```text
Shard 1
├─ Replica A
└─ Replica B
```

A 挂了：

```text
B 可以继续服务
```

或者两副本分担查询。

但 Replica 会增加：

```text
Storage
Memory
Replication Traffic
Update Consistency Complexity
```

---

# 5. Replica 不等于 Backup

和 MySQL 一样：

```text
错误 Delete
```

可能被同步到所有 Replica。

所以：

```text
Replica
≠
Backup
```

Vector Index 很多时候可重建，因此 Source of Truth 与 Rebuild Strategy 可能比传统 Backup 更重要。

---

# 6. Segment 是什么

很多 Vector DB 内部还会把一个 Shard 拆成多个 Segment：

```text
Shard
├─ Segment 1
├─ Segment 2
└─ Segment 3
```

原因可能包括：

```text
Incremental Write
Index Build
Compaction
Lifecycle
Parallel Query
```

Query 可能在多个 Segment 上搜索，再 Merge。

这也是为什么 Segment 数量过多可能影响性能。

---

# 7. Shard Key 怎么选

常见考虑：

```text
数据是否均匀
Query 能否路由
Tenant / KB 是否局部
热点是否会倾斜
后续是否容易扩容
```

如果简单：

```text
hash(id) % N
```

可能分布均匀，但业务 Query 每次都需要搜索所有 Shard。

如果按 tenant：

```text
Query 路由很好
```

但大 Tenant 可能造成 Hot Shard。

所以是典型 Trade-off。

---

# 8. Rebalance 是什么

新增节点后：

```text
旧 Shard 分布
```

可能不均匀。

需要：

```text
Move Segment / Partition
Rebuild Replica
Update Routing
```

这就是 Rebalance。

Rebalance 会占用：

```text
Network
Disk
CPU
Memory
```

并可能影响 Query P99。

---

# 9. Distributed Top-K 为什么有误差 / 成本问题

如果每个 Shard 只返回：

```text
local Top10
```

Coordinator 再合并 Global Top10，通常足够吗？

在很多相似度可直接比较且各 Shard Search 足够准确的情况下可以工作，但实际系统还会遇到：

```text
ANN Recall Loss per shard
Score Calibration
Filter
Shard Data Skew
```

所以需要对分布式查询链整体 Benchmark。

---

# 10. 一个节点挂了会发生什么

要区分：

```text
Shard 有 Replica
→ failover / reroute

Shard 无 Replica
→ 部分数据不可搜索
```

如果 Coordinator 选择：

```text
partial result
```

还需要明确：

```text
结果是否允许降级？
是否标记 incomplete？
是否重试？
```

这些属于 Vector DB 与 Backend Reliability 的交叉。

---

# 11. 面试怎么答

## Q：分布式 Vector DB 怎么扩展查询？

🎯 **建议回答**：

> 通常把数据水平拆成 Shard，每个 Shard 本地做 ANN Top-K，Coordinator fan-out 查询后合并成 Global Top-K。Replica 用于高可用和读扩展，Segment 则常用于增量写入、索引构建和 compaction。真正难点不是“多加机器”，而是控制 fan-out、tail latency、hot shard、rebalance 成本，以及 Filter / Tenant Routing 是否能把 Query 限制在少数 Shard。

---

# 12. 高频易错点

⚠️ **Shard 越多 Query 越快。** Fan-out 和 Tail Latency 可能更差。

⚠️ **Replica 就是 Backup。** 不是。

⚠️ **Partition = Shard = Segment。** 三者是不同抽象层次。

⚠️ **hash(id) 最均匀，所以一定是最佳 Shard Key。** Query Routing 可能变差。

---

# 13. 本章自测

<details><summary>1. 为什么 Partition / Tenant Routing 能降低分布式 Vector Search 成本？</summary>

因为它可以让 Query 只访问相关 Shard，而不是对所有节点做 Scatter-Gather。
</details>

<details><summary>2. Replica 主要解决什么，不解决什么？</summary>

主要解决可用性和读扩展；它不是历史备份，错误操作也可能同步到所有副本。
</details>