# 16. Redis Cluster、Hash Slot 与 Reshard

Sentinel 解决的是：

```text
单 Primary Keyspace 的高可用
```

当单节点容量或吞吐不够时，真正的问题变成：

> **怎样把 Keyspace 水平拆到多个 Primary？**

Redis Cluster 就是在做：

```text
Sharding
+
Replication
+
Failover
```

---

## 1. Redis Cluster 不使用“Key 直接 hash 到节点”

核心中间层：

```text
Key
 ↓
Hash Slot
 ↓
Node
```

Redis Cluster 有：

```text
16384 Hash Slots
```

基本映射：

```text
CRC16(key) mod 16384
```

每个 Primary 负责其中一部分 Slot。

---

# 2. 为什么要多一层 Slot

假设直接：

```text
hash(key) mod node_count
```

从 3 个节点扩到 4 个节点：

```text
大量 Key 的目标节点都会改变
```

有了 Slot：

```text
Key → Slot 关系稳定
```

扩容时只需要：

```text
把一部分 Slot 从旧节点迁到新节点
```

而不是重新定义所有 Key 的 Hash 算法。

---

# 3. 三个节点示意

```text
Node A: slot 0     ~ 5460
Node B: slot 5461  ~ 10922
Node C: slot 10923 ~ 16383
```

新增 Node D：

```text
从 A / B / C 各迁部分 Slot
→ D
```

这就是 Reshard / Rebalance 的核心。

---

# 4. Slot 迁移时到底迁什么

Slot 本身不是独立文件。

迁移一个 Slot，实际上要：

```text
找到属于该 Slot 的 Keys
→ 将 Keys 从 Source Node 迁到 Target Node
```

所以一个 Slot 里如果有超大 BigKey：

```text
Migration 可能很重
```

这也是 BigKey 会反过来影响 Cluster 运维的原因。

---

# 5. MOVED 与 ASK 的直觉

客户端请求发错节点时，Cluster 会告诉它：

```text
这个 Slot 不在我这里
```

稳定拓扑下常见：

```text
MOVED
```

表示新的 Slot Owner。

迁移过程中可能出现：

```text
ASK
```

表示当前这次请求应临时去目标节点处理。

成熟 Redis Cluster Client 会维护：

```text
slot → node map
```

并处理重定向。

所以 Cluster-aware Client 是必要的。

---

# 6. Hash Tag：为什么 Key 里会出现 `{}`

默认：

```text
user:1:profile
user:1:settings
```

可能落在不同 Slot。

如果写成：

```text
user:{1}:profile
user:{1}:settings
```

Redis Cluster 只对 `{1}` 部分计算 Slot，因此两者落到同一 Slot。

这叫 Hash Tag。

用途：

```text
需要 Multi-key Command
Transaction
Lua Script
```

涉及多个 Key 时，让它们满足同 Slot 约束。

---

# 7. 为什么 Multi-key 会受 Slot 限制

如果：

```text
Key A 在 Node 1
Key B 在 Node 2
```

一个原子 Lua Script 想同时改 A 和 B：

```text
谁来拥有这个原子执行边界？
```

Redis Cluster 不做任意跨节点分布式事务。

所以很多 Multi-key Command / Transaction / Script 要求：

```text
所有相关 Key 在同一 Slot
```

Hash Tag 就是显式控制这一点。

---

# 8. Cluster 的高可用

每个 Primary 可以有 Replica：

```text
Primary A → Replica A1
Primary B → Replica B1
Primary C → Replica C1
```

某个 Primary 故障：

```text
Replica 被提升
→ 接管对应 Slot
```

所以 Cluster 同时处理：

- Sharding；
- Failover。

---

# 9. Cluster 是强一致吗

不是。

官方 Cluster 设计明确使用异步复制，目标之一是可接受程度的 Write Safety，而不是严格强一致。

因此网络分区、Failover 等情况下仍存在已确认写丢失窗口。

所以不要回答：

> “Redis Cluster 之后就数据绝对不丢。”

---

# 10. 为什么 Cluster 不能解决单 HotKey

假设：

```text
hot:key → slot 8888 → Node B
```

无论 Cluster 有 3 个还是 30 个节点：

```text
这个 Key 仍在一个 Slot
```

所有请求仍打 Node B。

所以 Cluster 解决：

```text
Keyspace / Capacity / Aggregate Throughput
```

不自动解决：

```text
Single HotKey
```

---

# 11. Cluster 扩容不是“无成本”

官方支持在线迁移 Slot，理论上不需要全系统停机。

但生产仍要考虑：

- 迁移带宽；
- CPU；
- BigKey；
- Client Redirect；
- Node Load；
- P99 Latency；
- Slot Distribution；
- HotKey Distribution。

所以：

> “在线 Reshard”不等于“零性能影响”。

---

# 12. AI Application Key Design 与 Hash Tag

例如 Agent Run：

```text
run:{r1}:meta
run:{r1}:steps
run:{r1}:lease
```

如果确实需要同一个 Lua Script 操作它们：

```text
{r1}
```

让它们共 Slot。

但副作用：

```text
同一 run 全部集中一个节点
```

如果一个 Run 极热，也可能形成热点。

所以 Hash Tag 不是越多越好。

---

# 13. 面试怎么答

## Q：Redis Cluster 为什么是 16384 个 Slot？

🎯 **建议回答重点不在背设计历史，而在模型：**

> Cluster 不是把 Key 直接绑定 Node，而是先映射到固定的 16384 个 Hash Slot，再由各 Primary 负责一组 Slot。扩缩容时迁移 Slot 即可，客户端维护 Slot 到 Node 的映射并处理 MOVED/ASK。固定 Slot 层把 Key 分布和节点拓扑变化解耦。

## Q：为什么 Lua 多 Key 要同 Slot？

> Redis Cluster 不提供任意跨节点分布式原子事务；一个 Script 的 Key 如果跨节点，就无法在单个 Redis 执行上下文内保证原子性，因此相关 Key 要落同 Slot，常用 Hash Tag 实现。

---

# 14. 高频易错点

⚠️ **Redis Cluster 用一致性 Hash。**  
官方 Cluster 核心是 16384 Hash Slot，不是经典一致性 Hash 环。

⚠️ **Cluster 自动解决 HotKey。**  
错误。

⚠️ **Hash Tag 越多越好。**  
会牺牲分片均衡。

⚠️ **在线 Reshard 完全无影响。**  
迁移仍消耗网络、CPU，并受 BigKey 影响。

---

# 15. 本章自测

<details>
<summary>1. 为什么 Redis Cluster 要引入 Slot 层？</summary>

把 Key 到固定 Slot 的映射与 Slot 到 Node 的映射分开，使节点扩缩容主要通过迁移 Slot 完成，而不需要改变每个 Key 的分片规则。

</details>

<details>
<summary>2. Hash Tag 有什么用？</summary>

让多个相关 Key 使用 `{...}` 中相同内容计算 Slot，从而落到同一 Slot，满足 Multi-key / Transaction / Lua 等同节点约束。

</details>

<details>
<summary>3. 为什么 Cluster 仍可能丢最近写？</summary>

底层复制通常异步，Primary 已确认但 Replica 尚未同步的写在故障 Failover 后可能不存在于新 Primary。

</details>
