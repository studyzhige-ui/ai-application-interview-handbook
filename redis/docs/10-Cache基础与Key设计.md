# 10. Cache 基础、Key Design 与 Cache Aside 边界

Redis 最常见用途之一是 Cache。

但“加一层 Redis”并不会自动让系统变快。

真正的缓存设计要回答：

```text
缓存什么？
Key 怎么设计？
什么时候过期？
Miss 怎么回源？
谁是 Source of Truth？
怎么避免污染和穿透？
```

---

## 1. Cache 的本质

Cache 是：

> **用更快、通常更小、更靠近请求路径的一份数据副本，换取更低延迟和更低下游压力。**

所以 Cache 天生意味着：

```text
副本
→ 新鲜度问题
→ 一致性问题
→ 淘汰问题
```

不能只看“命中时快”。

---

# 2. 最常见的 Cache Aside

读路径：

```text
App
 ↓
GET Redis
 ├─ Hit  → return
 └─ Miss
      ↓
     DB
      ↓
   SET Redis
      ↓
   return
```

写路径常见思路：

```text
Update DB
→ Delete Cache
```

下一次读：

```text
Miss
→ 回源 DB
→ 重建 Cache
```

这就是 Cache Aside 的基本直觉。

---

# 3. 为什么通常“删除缓存”比“同步更新缓存”简单

如果写 DB 后还要立刻构造缓存：

```text
DB 更新成功
→ Cache 更新失败
```

或：

```text
并发两个写请求
→ Cache 更新顺序和 DB 提交顺序不同
```

会产生复杂 Race。

删除缓存让缓存变成：

```text
按需重建的 Derived State
```

但这不意味着：

> “Update DB + Delete Cache 自动强一致。”

中间仍然有 Failure Window。

完整一致性治理属于 AI Backend Engineering；Redis 本章只建立 Cache Side 的基础。

---

# 4. Key Design 为什么重要

一个缓存 Key 应尽可能表达：

```text
namespace
entity
identity
version / dimension
```

例如：

```text
user:profile:{user_id}
kb:meta:{tenant_id}:{kb_id}
model:config:{provider}:{model}
```

比：

```text
cache1
foo
123
```

更容易维护。

---

# 5. Key 太长和太短都不好

太短：

```text
u:1
```

不易排查。

太长：

```text
my_company_super_long_service_production_environment_user_profile_cache_key:...
```

大量 Key 下名字本身也消耗内存和网络。

所以需要平衡：

```text
可读性
vs
空间成本
```

---

# 6. 多租户 Key 一定要考虑隔离

AI SaaS：

```text
tenant A
user 1001
```

和：

```text
tenant B
user 1001
```

如果 Key 只写：

```text
user:1001
```

可能直接串租户。

更稳：

```text
user:{tenant_id}:{user_id}
```

并且权限校验不能只靠 Key 前缀，应用层仍要做授权。

---

# 7. Cache Value 放多大

假设 User Profile 有 100 个字段。

接口只需要 3 个：

```text
name
avatar
plan
```

如果每次缓存整个巨型对象：

```text
网络 Payload 大
序列化大
内存大
更新粒度粗
```

可以考虑：

- 更小 View Cache；
- Hash 字段；
- 按访问模式拆分。

但拆太细又会：

```text
Key 数暴涨
请求次数增加
```

所以仍是 Trade-off。

---

# 8. Cache Hit Rate 不是唯一指标

一个缓存：

```text
Hit Rate = 99%
```

听起来很好。

但如果剩下 1% Miss 都是：

```text
最重查询
```

数据库仍可能被压垮。

还要看：

```text
Hit Rate
Miss Cost
Saved Latency
Saved Downstream QPS
Object Size
Eviction Rate
P99
```

---

# 9. Negative Cache

假设恶意请求一直查：

```text
user_id = -999999
```

DB 每次都返回：

```text
not found
```

如果“不存在结果”也短 TTL 缓存：

```text
user:-999999 = NOT_FOUND
TTL 30s
```

可以减少穿透。

但 TTL 不宜太长，否则新创建对象可能长期被旧 Negative Cache 挡住。

---

# 10. Cache Warming

系统刚启动：

```text
Cache empty
```

大量请求同时进来：

```text
Miss Storm
→ DB 压力
```

可以对极热点数据：

- 预热；
- 灰度流量；
- 限速回填；
- SingleFlight / Mutex rebuild。

但不要“把所有 DB 数据都预热”，那可能只是复制整库到内存。

---

# 11. AI 场景的缓存分类

## Exact Cache

```text
相同 Key → 相同结果
```

如：

```text
model_config:{model}
```

## Tool Result Cache

```text
tool_name + normalized_args
```

需要考虑外部世界是否变化。

## Semantic Cache

不同 Query 但语义相近也可能复用结果。

这已经进入 Embedding / Similarity / Staleness 问题，后面单独讲。

---

# 12. 面试怎么答

## Q：什么是 Cache Aside？

🎯 **建议回答：**

> 读请求先查缓存，Hit 直接返回；Miss 再查 Source of Truth 并回填缓存。写请求通常先更新数据库，再删除缓存，让下次读按需重建。它实现简单、常用，但不是强一致协议，仍存在并发和失败窗口，完整一致性要结合重试、消息/CDC、补偿等机制设计。

## Q：缓存 Key 怎么设计？

> 至少考虑 namespace、实体 ID、租户、维度/版本、TTL、大小上界和 Cluster 分片需求，同时避免敏感信息直接出现在 Key 名。

---

# 13. 本章自测

<details>
<summary>1. Cache 为什么天然存在一致性问题？</summary>

因为它是 Source of Truth 的副本，原数据变化后副本可能暂时落后或更新失败。

</details>

<details>
<summary>2. Negative Cache 有什么风险？</summary>

如果 TTL 太长，新创建的数据可能仍被旧的 NOT_FOUND 缓存挡住，因此通常只做较短 TTL。

</details>

<details>
<summary>3. 为什么 99% Hit Rate 也不一定代表缓存健康？</summary>

还要看剩余 Miss 的成本、对象大小、Eviction、P99、DB 降压效果等；1% 重查询也可能压垮下游。

</details>
