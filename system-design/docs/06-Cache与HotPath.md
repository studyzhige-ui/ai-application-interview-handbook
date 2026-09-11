# 06｜Cache、Hot Path 与 Read / Write Path

Cache 不是“系统慢了就加 Redis”，而是对**访问路径和状态语义**的重新设计。

真正的问题是：

> **什么数据值得缓存？谁是 Source of Truth？读写怎样经过 Cache？失效、热点和故障时系统怎么退化？**

---

## 1. 先找 Hot Path

Hot Path 是最频繁、最敏感的请求路径。

例如电商：

```text
商品详情 Read
≫ 商品编辑 Write
```

例如 AI Gateway：

```text
Model Invocation
≫ Model Config Update
```

例如 RAG：

```text
Online Query
≫ Corpus Rebuild
```

Cache 的价值通常来自：

```text
Repeated Read
+
Expensive Recompute / Remote Call
+
Acceptable Staleness
```

---

# 2. Cache 之前先定义 SoT

常见：

```text
MySQL = Source of Truth
Redis = Cache
```

或者：

```text
Object Store = Source
Vector Index = Derived Index
Redis = Result Cache
```

如果 Cache 和 SoT 冲突，必须知道谁最终胜出。

---

# 3. Cache Aside 的基本路径

读：

```text
Read Cache
→ Hit: Return
→ Miss: Read DB
       → Populate Cache
       → Return
```

写：

```text
Write DB
→ Invalidate Cache
```

它简单，但并不自动提供强一致。

---

# 4. 为什么“更新 DB 后删 Cache”仍有窗口

并发下可能出现：

```text
Reader miss
→ 读到旧 DB 值
Writer 更新 DB
→ delete cache
Reader 把旧值写回 cache
```

实际概率和具体流程有关，但核心结论是：

> Cache 与 DB 是两个状态系统，双写天然存在失败和竞态窗口。

所以设计要先问：

```text
允许旧多久？
错误影响多大？
能否靠 TTL / Version / Retry / Reconciliation？
是否需要直接绕过 Cache？
```

---

# 5. Cache 的三类 Failure

## Penetration

请求本来就不存在的数据：

```text
Cache miss
→ DB miss
→ 每次都打 DB
```

可考虑：

- Negative Cache；
- Bloom Filter；
- Input Validation。

## Breakdown / Stampede

一个 Hot Key 过期，大量请求同时回源。

可考虑：

- Request Coalescing；
- Mutex / Singleflight；
- Logical Expiry；
- Stale-while-revalidate。

## Avalanche

大量 Key 同期失效或整个 Cache Layer 不可用。

可考虑：

- TTL Jitter；
- Degradation；
- Rate Limit；
- DB Protection。

---

# 6. HotKey 不是平均 QPS 问题

假设：

```text
总 QPS 100K
```

如果一个明星商品承担：

```text
30K QPS
```

即使集群平均很轻，单 Key / 单 Shard 仍可能成为热点。

常见治理：

```text
Local Cache
Key Replication / Read Replica
Request Coalescing
Shard Hot Data
Rate Limit
Precompute
```

但每种方案都改变一致性和失效成本。

---

# 7. Multi-level Cache

例如：

```text
Process Local Cache
→ Redis
→ DB
```

优点：

- 本地读极快；
- Redis 压力降低。

代价：

```text
多一层失效
多一层版本
多实例一致性更难
```

所以本地 Cache 常需要：

```text
short TTL
version
pub/sub invalidation
periodic refresh
```

而不是永久相信广播一定送达。

---

# 8. Write Path 也可能需要 Cache / Buffer

高写入系统可能：

```text
Client
→ Memory / Log / Queue
→ Batch Flush
→ Durable Store
```

这已经不是普通 Read Cache，而是写缓冲。

此时要回答：

```text
进程崩溃会丢多少？
什么时候算写成功？
Buffer 满了怎么办？
Flush 失败怎么办？
```

所以不要把所有 Memory Layer 都叫“缓存”。

---

# 9. AI 系统的 Cache Key 更复杂

Answer / Retrieval Cache 可能依赖：

```text
normalized_query
model_version
prompt_version
index_generation
permission_scope
tenant_id
retrieval_config
```

如果只用：

```text
hash(query)
```

可能复用到：

- 旧知识；
- 错模型；
- 错权限；
- 错 Tenant。

---

# 10. 什么时候不要 Cache

如果数据：

```text
变化极快
错误代价极高
请求几乎不重复
回源本身很便宜
```

Cache 可能收益很小，反而增加一致性风险。

例如某些余额 / 权限判断，不应该为了几十毫秒盲目做长 TTL Cache。

---

# 11. Cache 故障时的设计

问：

```text
Redis 整体不可用
→ 所有流量直接打 DB？
```

如果答案是“是”，可能发生二次雪崩。

更成熟：

```text
Cache failure detected
→ Concurrency Limit
→ Rate Limit / Load Shed
→ Serve stale where safe
→ Bypass only critical paths
→ Recover gradually
```

Failure 不能只看 Cache 自己，还要看下游保护。

---

# 12. 🎯 面试怎么答

> 我会先找 Hot Path 和重复读，再确认 Cache 是否真的有收益，并明确 Source of Truth。设计时不仅画 Hit/Miss，还会定义 TTL、Version、Invalidation 和 Cache Failure 的下游保护。对 HotKey 会看实际 Key Distribution，而不是平均 QPS。AI 系统的 Cache Key 还要带 Model、Prompt、Index Generation、Tenant 和 Permission Scope，避免复用陈旧或越权结果。

---

# 13. 本章自测

<details><summary>1. 为什么 Cache Aside 不等于强一致？</summary>
因为 Cache 和数据库是两个独立状态系统，写入、删除、回填之间存在并发和失败窗口。
</details>

<details><summary>2. Redis 故障后为什么不能无脑全部回源 DB？</summary>
Cache 平时可能吸收了大量流量，全部回源可能让 DB 立刻过载，引发级联故障。
</details>

<details><summary>3. 为什么 Answer Cache 必须带 Permission Scope？</summary>
相同 Query 对不同用户可访问的知识不同，如果忽略权限维度，可能跨用户复用受保护答案。
</details>
