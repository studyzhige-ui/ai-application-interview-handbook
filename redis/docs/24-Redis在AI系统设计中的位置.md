# 27. Redis in AI System Design

前 26 章分别学了：

```text
Data Structure
Runtime
TTL / Eviction
Cache
Persistence / HA / Cluster
Transaction / Lua
Lock
Session / Rate Limit
Security / Troubleshooting
```

最后一章要回答：

> **在一个真实 AI Application / Agent System 里，Redis 到底应该放在哪里，哪些数据应该放，哪些不该放？**

---

## 1. 一张总图

```text
                         Client
                           │
                           ▼
                     FastAPI / API
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          MySQL          Redis        Vector DB
             │             │             │
      Business Truth    Hot State     Semantic Search
             │             │             │
             └──────┬──────┴──────┬──────┘
                    ▼             ▼
                   RAG        Agent Harness
```

Redis 常位于：

> **Request Path 和 Durable Systems 之间，承担低延迟状态与缓存。**

---

# 2. 一类数据应该问五个问题

任何准备放进 Redis 的数据，先问：

```text
1. 谁是 Source of Truth？
2. 数据丢失能否重建？
3. 允许陈旧多久？
4. 生命周期多久？
5. 最大 Size / QPS / Hotspot 是多少？
```

答不出来，不应该急着创建 Key。

---

# 3. User / Tenant 数据怎么分

## MySQL

```text
user
organization
tenant_plan
billing
permission source-of-truth
```

## Redis

```text
session
auth cache
feature cache
rate limit
```

特别注意：

> Permission Cache 可以放 Redis，但权限真相通常仍在 Durable Store；撤权必须设计主动/快速失效。

---

# 4. Conversation 数据怎么分

## Durable History

```text
MySQL / document store
```

保存：

- 完整 Message；
- Audit；
- History；
- Billing / Token Usage。

## Redis Hot State

```text
recent window
stream cursor
summary cache
temporary generation state
```

不要把一个 Conversation 永久堆成一个超大 Redis List。

---

# 5. Agent Run 怎么分

## Durable

```text
run metadata
final status
checkpoint metadata
external side-effect record
usage / audit
```

## Redis

```text
current worker
lease
heartbeat
current step
stream position
short-lived progress
```

如果 Redis 丢失：

```text
能否从 durable checkpoint 恢复？
```

这是 Agent Harness 必须回答的，而不是 Redis 自己能保证的。

---

# 6. RAG 中 Redis 做什么

Redis 可以参与：

```text
Document metadata cache
Retrieval result cache
Embedding response cache
Rerank result cache
Query rewrite cache
Semantic cache
Rate limit
```

但核心语义向量检索：

```text
通常由 Vector DB / Search Engine 承担
```

不要因为 Redis 也有搜索/向量相关生态，就把课程边界混成“所有 Retrieval 都是 Redis”。

本 Handbook 的 Primary Boundary 仍然是：

```text
Redis → state/cache infrastructure
Vector DB → ANN/vector infrastructure
RAG → retrieval strategy / evaluation
```

---

# 7. Model Provider 调用怎么用 Redis

可以保存：

```text
rate limit
quota counter
provider health cache
model config cache
exact response cache
semantic cache
```

但不要把：

```text
provider API key
```

当普通 Cache Value 随意存放。

Secret 需要更严格的 Secret Boundary。

---

# 8. MySQL + Redis 一致性边界

最典型：

```text
MySQL = Source of Truth
Redis = Cache
```

常见读：

```text
Redis
→ miss
→ MySQL
→ fill Redis
```

常见写：

```text
Update MySQL
→ Invalidate Redis
```

但：

```text
DB 更新成功
Cache 删除失败
```

怎么办？

这已经进入：

- Retry；
- Outbox / CDC；
- Compensation；
- Failure Window；
- Eventual Consistency。

所以完整 Primary 在 **AI Backend Engineering**，不是 Redis 章节重复讲一遍分布式一致性。

---

# 9. Redis vs MQ

Redis 有：

```text
List
Pub/Sub
Streams
```

但如果需求是：

```text
长期 durable event log
大吞吐
多 consumer group replay
partition ordering
事件平台
```

应该比较 Kafka / MQ。

所以：

> 能实现队列 ≠ 就是最佳 MQ。

---

# 10. Redis vs Aerospike / Other KV

面经偶尔会问 KV Store 选型。

思考维度：

```text
Dataset 是否全内存？
单 Key / Value 大小？
持久化模型？
Cluster / Sharding？
延迟目标？
容量成本？
操作模型？
已有团队生态？
```

不要用：

> “Redis 最流行，所以选 Redis。”

工具选型必须从 Workload 出发。

---

# 11. Redis Failure 是否应该拖垮整个 AI 系统

理想情况下，不同 Redis 用途应分级：

## L1 可绕过

```text
Semantic Cache
Tool Result Cache
```

Redis 挂：

```text
直接回源 / 调 LLM
```

## L2 可降级

```text
Session
Rate Limit
```

根据业务选择：

```text
Fail-open / Fail-closed / Local fallback
```

## L3 关键协调状态

```text
Agent Lease
Idempotency helper
Task ownership
```

Redis 挂时：

```text
宁可暂停
不要双执行
```

所以一个成熟设计会给不同 Redis Namespace 定义不同 SLO 和 Failure Policy。

---

# 12. 是否所有用途都放一个 Redis Cluster

不一定。

如果同一集群同时有：

```text
巨大 Semantic Cache
高 QPS Rate Limit
关键 Session
Agent Lease
```

问题：

- Eviction Policy 冲突；
- Persistence 要求不同；
- BigKey / HotKey 相互影响；
- 故障爆炸半径大；
- 安全权限难隔离。

成熟系统可能按用途拆：

```text
Cache Redis
Session Redis
Coordination Redis
```

是否拆实例由规模和可靠性驱动，而不是一开始过度架构。

---

# 13. 一个完整 Agent Backend 示例

```text
User Request
   ↓
FastAPI
   ↓
Auth
   ├─ MySQL user truth
   └─ Redis auth/session cache
   ↓
Rate Limit
   └─ Redis counter / Lua
   ↓
Agent Run Create
   └─ MySQL durable run
   ↓
Worker Claim
   ├─ DB state transition
   └─ Redis lease/heartbeat (optional)
   ↓
RAG
   ├─ Vector DB retrieval
   └─ Redis retrieval/result cache
   ↓
Tool Calls
   └─ Redis exact read-only result cache (where valid)
   ↓
Streaming
   └─ Redis may hold short-lived cursor/state
   ↓
Final Commit
   └─ MySQL durable history / billing
```

这张图是 Redis 模块真正学完后的能力。

---

# 14. 面试怎么答

## Q：为什么 Agent 项目里既有 Redis、MySQL、Vector DB？

🎯 **建议回答：**

> 三者承担不同数据语义。MySQL 保存结构化长期业务真相和事务数据；Redis 保存低延迟、频繁访问、带生命周期的 Cache/Session/Counter/临时 Runtime State；Vector DB 负责 Embedding 的 ANN 语义检索。设计时还要明确每类数据的 Source of Truth、TTL、可重建性和故障降级，而不是按“哪个更快”决定存储。

## Q：Agent State 为什么不能全部只放 Redis？

> 如果 Redis 只是 Hot State Store 没问题，但涉及长任务 Resume、外部 Side Effect 和审计时，需要更明确的 Durable Checkpoint 与状态机。Redis 的 Persistence/Replication 语义不能自动保证 Agent Runtime Exactly-once。

---

# 15. Redis 模块最终掌握标准

学完后，你应该能从：

```text
“Redis 是缓存。”
```

升级到：

```text
我知道 Key 怎样建模
我知道数据结构为什么这样选
我知道主线程什么时候会被拖慢
我知道 TTL / Eviction 的不同
我知道 RDB/AOF/Replication/Sentinel/Cluster 的边界
我知道 Pipeline / Transaction / Lua 为什么不同
我能分析 Lock Failure Timeline
我能设计 Session / Rate Limit / Cache
我知道 Redis 故障时每类业务该怎样降级
我知道 Redis 在 AI Backend 中不该负责什么
```

---

# 16. 本章自测

<details>
<summary>1. 为什么 Redis 不应该默认成为 Agent 全部状态的唯一 Source of Truth？</summary>

Agent 长任务涉及恢复、审计、Side Effect 和最终业务状态；Redis 更适合 Hot State，Durable Truth/Checkpoint 需要按可靠性目标设计。

</details>

<details>
<summary>2. 为什么不同 Redis 用途可能需要拆实例？</summary>

它们可能拥有不同 Eviction、Persistence、HA、安全和容量需求，混在一起会相互干扰并扩大故障爆炸半径。

</details>

<details>
<summary>3. Redis 在 RAG 中最典型的职责是什么？</summary>

缓存和短状态，例如 Retrieval/Embedding/Rerank/Query Rewrite 结果缓存、Rate Limit、Metadata Hot Cache；完整 Retrieval Strategy 仍归 RAG，ANN 基础设施归 Vector DB。

</details>
