# 01. Redis 在 AI Application 中负责什么

很多人第一次学 Redis，会把它理解成：

> “一个特别快的数据库。”

这个说法太模糊。

真正应该先建立的是：

> **Redis 最擅长承载低延迟、频繁访问、通常可以设置生命周期的结构化状态。**

它经常和 MySQL、Vector DB 同时存在，因为三者解决的问题不同。

---

## 1. 先从一个真实 AI Application 看起

假设你在做一个多租户 Agent 平台。

系统里有：

```text
用户资料
租户配置
Conversation
Agent Run
Tool Result
知识库文档
Session
Rate Limit
临时任务状态
```

如果全部放 MySQL：

- 很多高频、短生命周期状态没必要每次查关系数据库；
- 大量 Session / TTL / Counter 场景实现起来不够直接；
- 热点读可能给 MySQL 带来额外压力。

如果全部放 Redis：

- 业务 Source of Truth、复杂查询、长期历史、强 Schema 都不合适；
- 内存成本高；
- Failover / Persistence 的语义也和关系数据库不同。

所以常见分层是：

```text
MySQL
├─ User
├─ Tenant
├─ Conversation Metadata
├─ Billing
├─ Agent Run History
└─ Business Source of Truth

Redis
├─ Session
├─ Hot Conversation State
├─ Rate Limit Counter
├─ Temporary Agent State
├─ Cache
└─ Dedup / Idempotency Helper State

Vector DB
└─ Embedding / Semantic Retrieval
```

---

# 2. Redis 不是“更快的 MySQL”

两者的数据模型就不同。

MySQL：

```text
Table
→ Row
→ Column
→ SQL
→ Index / Transaction
```

Redis：

```text
Key
→ Typed Value
→ Command
```

例如：

```text
user:1001:profile       → Hash
session:abc123          → Hash / String
rate:user:1001          → Counter
online_users            → Set
leaderboard             → ZSet
```

Redis 更像：

> **“带丰富数据结构和服务器端原子命令的内存 Key-Value / Data Structure Server”。**

---

# 3. 为什么 AI 系统特别喜欢 Redis

AI Application 有很多“短状态”。

例如一次 Agent Run：

```text
run_id = r_001
status = running
current_step = 7
last_heartbeat = ...
stream_cursor = ...
```

这些状态：

- 访问频繁；
- 生命周期可能只有几十分钟；
- 多个 API 实例需要共享；
- 通常要快速判断；
- 可以在任务结束后过期。

Redis 非常适合。

再比如限流：

```text
tenant_42 在 60 秒内已经请求多少次？
```

天然就是：

```text
Counter + TTL
```

---

# 4. Redis 的典型职责

## 4.1 Cache

```text
App
 ↓
Redis hit
 ↓
直接返回
```

Miss 时再回源 MySQL / Remote API。

## 4.2 Session

多实例 FastAPI：

```text
Client
  ↓
Load Balancer
 ├─ API-1
 ├─ API-2
 └─ API-3
```

Session 如果只放 API-1 本地内存，下一次请求到 API-2 就找不到。

Redis 可作为共享 Session Store。

## 4.3 Counter / Rate Limit

```text
INCR
EXPIRE
ZSET
Lua
```

可以组合出多种限流实现。

## 4.4 Temporary Runtime State

Agent：

```text
run:{id}:status
run:{id}:heartbeat
run:{id}:lease
```

适合做临时运行态。

但：

> Agent Checkpoint / Resume 的完整执行语义不属于 Redis 本身。

Redis 这里只负责“怎么存”。

## 4.5 Lock / Coordination Helper

利用：

```text
SET key value NX PX ttl
```

可以实现基本分布式锁。

但后面会看到：

> “能 SET NX”不等于“锁一定正确”。

---

# 5. Redis 不适合什么

## 5.1 长期唯一业务真相

例如：

```text
用户账单
支付结果
最终订单状态
```

通常不应该只存在 Redis。

## 5.2 大量冷数据

Redis 主要以内存为核心资源。

把 TB 级冷历史全部塞进去，成本可能非常高。

## 5.3 复杂关系查询

例如：

```sql
JOIN
GROUP BY
复杂过滤
多维分析
```

MySQL / OLAP 系统更适合。

## 5.4 语义近邻搜索

```text
“找和这句话意思最相近的 20 个知识片段”
```

这是 Vector DB / Vector Search 的领域。

---

# 6. 一个重要概念：Source of Truth

假设：

```text
MySQL: user credits = 100
Redis: user credits = 100
```

如果两边变成：

```text
MySQL = 80
Redis = 100
```

谁说了算？

必须提前定义。

常见业务缓存里：

```text
MySQL = Source of Truth
Redis = Derived / Cached State
```

因此缓存可以：

```text
删除
过期
重建
```

而不会丢失最终业务事实。

🎯 **这条原则对 AI 系统非常重要。**

例如：

```text
Redis 中 Agent Run 的热状态
```

可以是临时加速；

而：

```text
最终 Run History / Billing
```

仍应可靠落到长期存储。

---

# 7. Redis 与 MySQL / Vector DB 的一张对比表

| 维度 | MySQL | Redis | Vector DB |
|---|---|---|---|
| 主模型 | Relation / Row | Key → Typed Value | Vector + Metadata |
| 主要资源 | Disk + Buffer | Memory-first | Memory / Disk Index |
| 擅长 | 业务事务 | Cache / State / Counter | Semantic Retrieval |
| TTL | 不是核心模型 | 核心能力 | 产品相关 |
| SQL / Join | 强 | 非核心 | 非核心 |
| 事务 | 完整关系事务 | 命令/事务语义不同 | 非重点 |
| ANN | 不擅长 | 非核心 | 核心 |
| 常见 AI 用法 | Source of Truth | Hot State / Cache | RAG Retrieval |

---

# 8. 面试怎么答

## Q：为什么 Agent 项目里同时有 MySQL 和 Redis？

🎯 **建议回答：**

> MySQL 主要承载长期、可靠、结构化的业务数据，是 Source of Truth；Redis 主要承载低延迟、高频、短生命周期的数据，例如 Session、Cache、Rate Limit、Conversation Hot State 或 Agent 临时运行状态。两者不是替代关系，而是数据生命周期和访问模式不同。

## Q：为什么不能全部放 Redis？

> Redis 的优势是低延迟和丰富内存数据结构，但内存成本、持久性/Failover 语义、复杂查询和长期业务数据治理与关系数据库不同。关键业务真相通常需要更适合的持久化系统。

---

# 9. 高频易错点

⚠️ **Redis 就是 Cache。**  
不完整。Redis 也是 Data Structure Server，可用于 Session、Counter、Stream、Coordination 等。

⚠️ **Redis 比 MySQL 快，所以都放 Redis。**  
忽略成本、查询、持久化和一致性语义。

⚠️ **有 RDB/AOF 后 Redis 就等价于 MySQL。**  
错误。数据模型、事务语义、HA、查询能力都不同。

⚠️ **Agent Memory 就等于 Redis。**  
错误。Memory 是 Agent 逻辑能力；Redis 只是潜在的 Storage Backend 之一。

---

# 10. 本章自测

<details>
<summary>1. Redis 最适合承载什么样的数据？</summary>

低延迟、高频访问、结构相对简单、常带生命周期或可重建属性的状态，例如 Cache、Session、Counter、Hot State。

</details>

<details>
<summary>2. Source of Truth 是什么意思？</summary>

当多个存储中存在同一业务事实时，必须明确哪个系统是最终权威来源。业务缓存场景中通常 MySQL 是 Source of Truth，Redis 是可过期、可重建的派生状态。

</details>

<details>
<summary>3. Redis 和 Vector DB 最核心的区别是什么？</summary>

Redis 主要按 Key 和原生数据结构访问；Vector DB 的核心是向量相似度和 ANN 语义检索。

</details>
