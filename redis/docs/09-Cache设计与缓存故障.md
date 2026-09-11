# 09. Cache 设计与故障模式：Key、TTL、Cache Aside、穿透、击穿与雪崩

Redis 被放进业务架构后，最常见的角色之一就是 Cache。

但“把查询结果塞进 Redis”只是最开始。一个真正完整的 Cache 设计必须同时回答：

```text
缓存什么？
Key 怎么设计？
TTL 怎么定？
Miss 时怎么回源？
更新时怎么失效？
缓存失效后会不会把数据库打穿？
不存在的数据怎么办？
热点 Key 怎么保护？
Redis 故障时系统怎么降级？
```

所以这一章把原来的“Cache 基础”和“穿透/击穿/雪崩”合并成一个完整知识闭环：

> **Cache 的正常路径和 Failure Path 必须一起设计。**

---

## 1. 为什么需要 Cache

假设一个 AI Application 的用户配置、模型配置或会话元数据主要保存在 MySQL。

如果某些数据：

- 读取频率很高；
- 修改频率相对低；
- 对毫秒级延迟敏感；
- 可以接受短时间内的缓存副本；

就可以考虑：

```text
Application
    ↓
Redis Cache
    ↓ miss
MySQL Source of Truth
```

Cache 的核心价值不是“Redis 比 MySQL 高级”，而是：

> **用更便宜、更近、更快的副本吸收热点读取，减少 Source of Truth 的压力。**

---

## 2. 先区分 Source of Truth 和 Cache

典型业务中：

```text
MySQL = authoritative state
Redis = derived / rebuildable copy
```

这意味着 Redis 里的 Cache 通常应该满足：

```text
丢了可以重建
过期可以回源
短暂不一致有明确容忍边界
```

如果一份数据丢失后业务无法恢复，它可能已经不是普通 Cache，而是业务状态本身。

---

## 3. Cache Aside 是最常见心智模型

### Read Path

```text
GET cache:key
    ↓ hit
return

GET cache:key
    ↓ miss
query DB
    ↓
SET cache:key value EX ttl
    ↓
return
```

### Write Path

常见实践是：

```text
update DB
→ invalidate/delete cache
```

而不是简单认为：

```text
update DB
→ update cache
```

一定更好。

原因是“更新缓存”会引入更多双写窗口、并发覆盖和冷数据维护问题。

注意：跨 MySQL + Redis 的最终一致性完整问题属于 AI Backend Engineering；Redis 模块只理解 Cache 一侧的行为和 Failure。

---

## 4. Key Design 是 Cache Design 的一部分

一个 Key 最好让你一眼看出：

```text
namespace
entity
identity
version / tenant（如果需要）
```

例如：

```text
user_profile:{tenant_id}:{user_id}:v3
model_config:{model_id}
rag_query_cache:{tenant}:{hash}
```

避免：

```text
cache:1
foo
user
```

好的 Key Design 会直接影响：

- 可读性；
- Tenant Isolation；
- 批量失效；
- Cluster Slot；
- 监控；
- Key Collision；
- Schema Migration。

---

## 5. TTL 不是“随便设 30 分钟”

TTL 应该来自业务语义。

可以从几个问题倒推：

```text
数据多久变化一次？
允许旧多久？
回源代价多高？
这个 Key 有多热？
重建是否昂贵？
系统是否有主动失效机制？
```

### 高频、重建昂贵的数据

通常要避免同一时刻大量过期。

### 强时效数据

TTL 可能较短，但要同时考虑数据库压力。

### 低频数据

长 TTL 不一定有意义，因为它可能一直占内存。

TTL 是：

> **Freshness、Memory、Backend Load 之间的 Trade-off。**

---

## 6. Cache Penetration：查询的东西根本不存在

典型流程：

```text
Request nonexistent id
→ Redis miss
→ DB miss
→ next request repeats
→ Redis miss again
→ DB miss again
```

如果攻击者不断请求随机不存在 ID：

```text
Cache 永远帮不上忙
```

这就是穿透。

### 常见治理

#### 6.1 Negative Cache

把“不存在”也短暂缓存：

```text
key → NOT_FOUND, TTL=30s
```

优点：简单。

风险：真实数据刚创建时可能短暂看到旧的不存在结果。

#### 6.2 Bloom Filter

在访问 Cache/DB 前快速判断：

```text
ID definitely not exists?
→ reject / return empty
```

Bloom Filter 可能有 False Positive，但没有典型意义上的 False Negative（前提是构建和更新过程正确）。

#### 6.3 Input Validation / Rate Limit

如果请求 ID 本身明显非法，应在更上游拦掉，而不是靠数据库判断。

---

## 7. Cache Breakdown / Stampede：一个热点 Key 突然失效

场景：

```text
hot:key TTL expires
```

随后 5000 个请求同时：

```text
miss
→ all query DB
```

一个 Key 的过期造成瞬时回源洪峰。

### 治理思路

#### Mutex / Single Flight

只有一个请求负责重建：

```text
first request → rebuild
others → wait / retry / stale
```

#### Logical Expiration / Stale-while-revalidate

不立即让热点值消失：

```text
old value still available
→ one background refresh
```

#### Prewarm

已知超级热点可提前加载。

#### Longer / Adaptive TTL

对超热点配置更合理生命周期。

注意：

> 分布式锁本身不是 Cache Breakdown 的唯一答案。

单飞、后台刷新和允许短暂 Stale 往往更适合读缓存。

---

## 8. Cache Avalanche：大量缓存同时失效或缓存层整体不可用

典型原因：

### 8.1 大量 Key 同时过期

例如统一设置：

```text
TTL = exactly 3600 seconds
```

某个整点大量 Key 一起过期。

可以使用：

```text
base TTL + random jitter
```

把过期时间打散。

### 8.2 Redis 整体故障

如果应用设计成：

```text
Redis error
→ 所有请求无条件打 DB
```

数据库很可能成为下一块倒下的组件。

所以 Production Cache 必须同时考虑：

- Circuit Breaker；
- Backend Rate Limit；
- Local Cache；
- Stale Data；
- Queue / Backpressure；
- Degrade Response。

这些通用韧性机制的系统设计归 AI Backend Engineering，但 Redis 使用者必须知道这个 Failure Path。

---

## 9. 三种故障怎么快速区分

| 问题 | 核心原因 | 典型现象 |
|---|---|---|
| Penetration | 数据本来不存在 | Cache 与 DB 持续 miss |
| Breakdown | 单个热点 Key 失效 | 热点请求瞬间并发回源 |
| Avalanche | 大量 Key / Cache Layer 同时失效 | 大范围请求压向下游 |

不要只背名词，要能从流量路径判断它们。

---

## 10. Cache Warmup 与 Rebuild

系统启动或缓存清空后：

```text
Cache cold
→ 所有请求 miss
```

如果数据量大，不能简单一次性全量预热。

可以：

```text
Top Hot Keys prewarm
+
Lazy Load
+
Concurrency Limit
+
Backpressure
```

重建过程本身也需要控制速率，否则“修缓存”可能把数据库压垮。

---

## 11. Multi-tenant Cache 的额外风险

AI Application 往往是多租户系统。

Key 必须考虑：

```text
tenant_id
user_id
permission scope
model/version
knowledge-base version
```

例如错误设计：

```text
answer_cache:{query_hash}
```

可能让 Tenant A 命中 Tenant B 的内容。

更安全的维度可能是：

```text
answer_cache:{tenant}:{kb_version}:{permission_scope}:{query_hash}
```

Semantic Cache 后面还会有更复杂的 False Hit 问题。

---

## 12. 缓存什么，不缓存什么

适合 Cache 的通常是：

- 热点读取；
- 可重建；
- 有明确过期或失效策略；
- Value 大小可控；
- Staleness 可定义。

不适合默认缓存：

- 大量从不重复读取的数据；
- 极大 Value；
- 无法定义一致性边界的敏感业务事实；
- 依赖权限但 Key 没有权限维度的数据；
- “反正 Redis 快”所以全部复制进去的数据。

---

## 13. AI Application 场景

### Model Configuration

```text
model routing config
provider metadata
```

可缓存，但配置变更必须有失效机制。

### User / Tenant Configuration

适合高频读取，但 Key 必须包含 Tenant Identity。

### RAG Result Cache

不能只看 Query String，还要考虑：

```text
knowledge version
permission
retrieval config
model version
```

### Tool Result Cache

要先判断 Tool 是否：

- deterministic；
- read-only；
- 有明确 freshness；
- 没有用户敏感副作用。

---

## 14. 常见错误

### 错误 1：Cache Hit Rate 越高越好

不一定。把大量低价值数据缓存起来可能提高 Hit Rate，却浪费内存和增加一致性复杂度。

### 错误 2：所有 Key 都设同一个 TTL

容易产生同时过期和 Avalanche 风险。

### 错误 3：缓存穿透只靠 Bloom Filter

Bloom Filter 只是一个工具，仍要考虑数据更新、误判、输入校验、Negative Cache 和流量治理。

### 错误 4：缓存击穿就加分布式锁

未必。读场景常可使用 Single Flight、Stale-while-revalidate 等更低成本方式。

### 错误 5：Redis 挂了就直接回源数据库

这可能把缓存故障升级成数据库故障。

---

## 15. 面试怎么答

### Q：缓存穿透、击穿、雪崩有什么区别？

> 穿透是请求的数据本身不存在，所以 Cache 和 DB 都持续 miss；击穿是某个热点 Key 失效后大量并发同时回源；雪崩则是大量 Key 同时过期或整个缓存层故障，造成大范围流量压向下游。治理方式分别偏向 Negative Cache/Bloom Filter、Single Flight/后台刷新，以及 TTL Jitter、降级、限流和多级缓存。

### Q：TTL 怎么设计？

> TTL 不应该拍脑袋，要根据更新频率、允许 Staleness、回源成本、热点程度和主动失效能力决定；大批 Key 还要通过 Jitter 避免同时过期。

### Q：Redis 故障后为什么不能无脑回源数据库？

> 因为 Cache 通常吸收了远高于数据库承载能力的读流量，Redis 一旦故障，如果所有请求直接打 DB，会产生级联故障，需要配合限流、熔断、Local Cache、Stale Data 或降级策略。

---

## 16. 章节自测

<details>
<summary>1. Cache 和 Source of Truth 最大区别是什么？</summary>

Cache 通常是可重建的派生副本，Source of Truth 则是业务权威状态。缓存丢失不应该意味着业务事实永久丢失。

</details>

<details>
<summary>2. 为什么 Cache Breakdown 和 Avalanche 不能混为一谈？</summary>

Breakdown 通常围绕单个或少量超级热点 Key；Avalanche 是大量 Key 同时失效或整个 Cache Layer 不可用，影响面更广。

</details>

<details>
<summary>3. 为什么热点缓存重建需要 Single Flight？</summary>

防止大量并发请求同时执行同一份昂贵回源和重建工作，把瞬时压力放大到数据库。

</details>

<details>
<summary>4. 为什么 Negative Cache 需要较短 TTL？</summary>

因为“不存在”状态未来可能变为存在，过长 TTL 会让新创建的数据长期不可见。

</details>

<details>
<summary>5. 多租户 Semantic Cache 为什么必须包含 Tenant / Permission 维度？</summary>

否则语义相近请求可能复用到另一个租户或权限域的结果，造成数据越权和错误答案。

</details>
