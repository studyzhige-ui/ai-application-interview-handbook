# 08. TTL 与过期删除

Redis 很重要的能力不是“快”，而是：

> **Key 可以自带生命周期。**

这让它天然适合 Session、验证码、Rate Limit Window、临时 Agent State、Cache 等。

---

## 1. TTL 是什么

```text
TTL = Time To Live
```

例如：

```text
SET session:abc payload EX 1800
```

表示这个 Key 30 分钟后过期。

常见：

```text
EXPIRE key seconds
PEXPIRE key milliseconds
TTL key
PTTL key
PERSIST key
```

---

# 2. 为什么不能“时间一到立刻扫描全库删除”

如果每毫秒都检查所有 Key：

```text
O(N) 全库扫描
→ CPU 浪费巨大
```

Redis 采用组合策略：

```text
Lazy Expiration
+
Active Expiration
```

---

# 3. Lazy Expiration

访问 Key 时发现：

```text
expire_at < now
```

就把它视为已过期并删除。

优点：

```text
不访问就不额外消耗 CPU
```

问题：

```text
如果永远没人访问
过期对象可能暂时继续占内存
```

所以只靠 Lazy 不够。

---

# 4. Active Expiration

Redis 会周期性抽样检查带 TTL 的 Key，并清理过期项。

目标不是：

```text
每个 Key 在过期时刻纳秒级立即物理释放
```

而是：

> **用受控 CPU 成本持续回收过期数据。**

所以 TTL 到点和物理内存释放之间不应该理解成严格实时定时器。

---

# 5. TTL 是数据语义，不只是清理机制

Session：

```text
30 min idle timeout
```

验证码：

```text
5 min validity
```

Rate Limit：

```text
60 sec window
```

Tool Result Cache：

```text
10 min stale tolerance
```

因此 TTL 应该来自业务新鲜度，而不是随便：

```text
“都设置 1 小时”
```

---

# 6. Cache TTL 怎样设计

先问：

```text
数据多久变化一次？
允许陈旧多久？
Miss 回源成本多大？
Key 访问热度怎样？
```

例如：

```text
用户昵称：5 min
模型价格配置：30 sec
静态配置：1 hour
实时余额：可能不适合纯 TTL Cache
```

不存在一个通用最佳值。

---

# 7. 为什么 TTL 加随机抖动

如果 100 万个 Key 同时：

```text
EX 3600
```

它们可能在同一时间段大量过期：

```text
大量 Miss
→ 同时回源 DB
→ Cache Avalanche
```

因此常见：

```text
base_ttl + random_jitter
```

例如：

```text
3600 + random(0, 600)
```

让过期时间分散。

---

# 8. Sliding Expiration vs Fixed Expiration

## Fixed

创建时：

```text
30 min 后一定过期
```

## Sliding

每次访问：

```text
刷新 TTL
```

Session 常见 Sliding，但要注意：

- 热 Session 可能一直不释放；
- 每次读都写 TTL 会增加写流量；
- 多客户端并发刷新需要原子语义。

---

# 9. TTL 和 Persistence 的关系

RDB/AOF 不应该让已经过期的数据在重启后“复活”。

Redis 的过期时间本身属于数据状态的一部分，恢复时会按时间语义处理。

但重要的是：

> TTL 不是 Persistence 的替代品。

TTL 回答：

```text
什么时候应该失效
```

Persistence 回答：

```text
进程崩溃后如何恢复未过期数据
```

---

# 10. Expiration 与 Replication

过期也会改变 Dataset。

Primary / Replica 需要维持一致的最终数据状态。

后面 Replication 章节会讲：

```text
过期 / 淘汰 / 写操作
```

都属于数据变化链路的一部分。

---

# 11. AI 场景

## Conversation Hot State

```text
conversation:{id}:hot
TTL = 24h
```

长期历史另落 MySQL。

## Agent Run Lease

```text
run:{id}:lease
TTL = 30s
```

Worker 定期续约。

但这里的 Lease 正确性已经进入分布式协调，不应只理解成“设置 TTL”。

## Semantic Cache

不同结果允许不同 TTL：

```text
静态 FAQ → 长
实时库存/价格 → 短或禁用
```

---

# 12. 面试怎么答

## Q：Redis 过期删除怎么实现？

🎯 **建议回答：**

> Redis 不会为每个 Key 都精确创建一个到点删除定时器，而是组合 Lazy Expiration 和 Active Expiration。访问 Key 时发现过期会懒删除，同时后台周期性抽样清理过期 Key，在 CPU 成本和内存回收之间做平衡。

## Q：为什么 Cache TTL 要加随机值？

> 为了避免大量 Key 同时过期形成缓存雪崩，让回源请求在时间上分散。

---

# 13. 本章自测

<details>
<summary>1. Lazy Expiration 的缺点是什么？</summary>

长期没人访问的过期 Key 可能暂时继续占用内存，因此需要 Active Expiration 配合。

</details>

<details>
<summary>2. TTL 到点是否意味着那一刻物理内存一定立即释放？</summary>

不能这样理解。Redis 在过期语义上会把 Key 视为失效，但实际清理采用 Lazy + Active 等机制，是受控的渐进回收。

</details>

<details>
<summary>3. Session 为什么可能用 Sliding Expiration？</summary>

希望活跃用户保持登录，空闲超过一定时间才失效；但刷新 TTL 会产生额外写入，也要考虑热 Session 和并发更新。

</details>
