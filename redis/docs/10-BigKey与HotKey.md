# 12. BigKey 与 HotKey

BigKey 和 HotKey 经常一起出现，但它们不是一个问题。

一句话先区分：

```text
BigKey = 一个 Key 太大
HotKey = 一个 Key 太热
```

一个 Key 可以：

- 大但不热；
- 热但不大；
- 又大又热。

最后一种最危险。

---

## 1. 什么叫 BigKey

没有一个适用于所有业务的固定字节阈值。

更实用的定义是：

> **一个 Key 的 Value 大到明显影响网络、命令执行、删除、迁移、复制或内存管理。**

例如：

```text
String 20MB
Hash 500 万 Field
Set 1000 万 Member
List 1000 万元素
```

都可能是 BigKey。

---

# 2. BigKey 为什么危险

## 2.1 大响应

```text
GET huge_string
```

会产生：

- 服务器拷贝；
- 网络传输；
- 客户端内存；
- 序列化/反序列化成本。

## 2.2 高复杂度命令

```text
HGETALL huge_hash
SMEMBERS huge_set
LRANGE 0 -1
```

可能长时间占用主线程。

## 2.3 删除成本

```text
DEL huge_key
```

释放海量对象可能制造延迟。

可以考虑：

```text
UNLINK
```

把实际内存回收更多交给后台线程。

## 2.4 Replication / Migration

BigKey 复制给 Replica、迁移 Slot、RDB/AOF 处理时都会更重。

---

# 3. BigKey 怎么发现

思路包括：

- `MEMORY USAGE key`；
- `redis-cli --bigkeys` 等工具；
- Slowlog / latency；
- 业务 Schema 审计；
- Command / Response Size 监控。

不要只等线上卡住再查。

设计阶段就应该给：

```text
Value Size Limit
Collection Cardinality Limit
```

---

# 4. BigKey 怎么拆

## 4.1 大 Hash 按桶拆

原来：

```text
all_users
```

拆成：

```text
users:0
users:1
...
```

或更常见：

```text
user:{id}
```

按实体拆。

## 4.2 大时间序列按时间分桶

```text
events:2026-09-11:00
events:2026-09-11:01
```

## 4.3 大 List / ZSet 按业务维度拆

但拆分会带来：

```text
聚合查询更复杂
跨 Key 操作增加
Cluster Slot 约束
```

所以不是“越碎越好”。

---

# 5. 什么叫 HotKey

HotKey 是访问流量高度集中。

例如：

```text
config:global
```

只有 1KB，却有：

```text
500k QPS
```

它不是 BigKey，但可能把单节点打满。

另一个例子：

```text
celebrity:profile:1
```

突发热点时读流量全部集中到一个 Slot / Node。

---

# 6. HotKey 为什么会破坏 Cluster 的均衡

Redis Cluster 按 Key 分 Slot。

如果总流量：

```text
1 亿 QPS
```

但其中：

```text
50% 都访问一个 Key
```

这个 Key 只能属于一个 Slot，Slot 由一个 Primary 服务。

所以即使 Cluster 有很多节点：

```text
其它节点很闲
热点节点爆满
```

这就是：

> **容量均匀 ≠ 流量均匀。**

---

# 7. HotKey 怎么发现

方法包括：

- Keyspace / command traffic metrics；
- Redis hotkeys tooling（需结合配置/采样）；
- Client-side metrics；
- Proxy / Gateway 统计；
- CPU / Network 节点倾斜；
- Slowlog 与业务 Trace。

很多 HotKey 是业务事件造成的，因此需要应用指标和 Redis 指标一起看。

---

# 8. HotKey 怎么治理

## 8.1 Local Cache

极热点只读配置：

```text
App Local Cache
→ Redis
```

把大量 QPS 截在进程内。

代价：

```text
本地副本一致性
```

## 8.2 Replica Read

某些读场景可以分担到 Replica。

但要接受：

```text
Replication Lag / Stale Read
```

## 8.3 Key Sharding

Counter：

```text
counter:0
counter:1
...
counter:15
```

写入随机分片，读取时聚合。

代价：

```text
读取变复杂
强实时总数更难
```

## 8.4 Request Coalescing

大量并发对同一 Key Miss：

```text
SingleFlight
```

避免重复回源。

---

# 9. 大 Key 迁移为什么要小心

Cluster Reshard 时：

```text
移动 Slot
→ 移动其中 Key
```

一个超大 Key：

```text
网络传输时间长
→ Node Pressure
→ Migration Tail Latency
```

所以 BigKey 也是 Cluster 运维问题。

---

# 10. AI Application 典型风险

## Conversation 全塞一个 List

```text
conversation:{id}
→ 10 万条 message
```

可能成为 BigKey。

长期消息更适合：

```text
MySQL / durable store
```

Redis 只保存：

```text
最近窗口 / Hot State
```

## Global Model Config

```text
model:config:default
```

很小但所有请求都读，可能是 HotKey。

可以：

```text
Local Cache + Pub/Sub Invalidate
```

## Agent Tool Schema

把所有 Tool Schema 塞一个超大 Key：

```text
tool_registry:all
```

可能同时形成大对象和热点。

更适合按 Tool / Namespace 拆分，并做 Progressive Discovery。

---

# 11. 面试怎么答

## Q：BigKey 和 HotKey 有什么区别？

🎯 **建议回答：**

> BigKey 是 Value 本身过大，例如巨大 String 或包含海量元素的 Hash/Set；风险在命令复杂度、网络、删除、复制和迁移。HotKey 是访问流量高度集中，即使 Key 很小也可能把单个 Redis 节点打满。治理 BigKey 常靠拆 Key、限制对象大小、渐进扫描/删除；治理 HotKey 常靠本地缓存、读扩散、Key Sharding、SingleFlight 等。

## Q：为什么 Cluster 不能自动解决 HotKey？

> 因为一个 Key 只属于一个 Hash Slot，单个热点 Key 的流量仍集中在负责该 Slot 的节点上。Cluster 能分散 Keyspace，不会自动把一个 Key 拆到多节点并行执行。

---

# 12. 高频易错点

⚠️ **BigKey = Key 名字很长。**  
错误，主要指 Value / Collection 规模大。

⚠️ **加 Redis Cluster 就没有 HotKey。**  
错误。

⚠️ **删除 BigKey 直接 DEL 就行。**  
需要评估释放成本，可能使用 UNLINK / 分批删除。

⚠️ **HotKey 只影响 CPU。**  
也可能影响网络、连接、内存带宽和下游回源。

---

# 13. 本章自测

<details>
<summary>1. 一个 1KB Key 能是 HotKey 吗？</summary>

可以。如果访问 QPS 极高，它仍然会让负责该 Key 的节点成为瓶颈。

</details>

<details>
<summary>2. 为什么一个包含几百万成员的 Set 即使元素很小也算 BigKey？</summary>

因为全量操作、删除、复制、迁移和内存占用都可能很大，风险来自整个 Value 的规模。

</details>

<details>
<summary>3. Key Sharding 解决 Hot Counter 的代价是什么？</summary>

写入能分散，但读取总数需要聚合多个分片，实时一致性和实现复杂度都会增加。

</details>
