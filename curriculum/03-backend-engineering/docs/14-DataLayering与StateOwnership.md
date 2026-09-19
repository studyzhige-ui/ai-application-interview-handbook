# 14. Data Layering 与 State Ownership：MySQL / Redis / Session / Runtime State

> 这一章解决一个经常被低估的问题：**状态应该放哪里？谁才是最终事实？**

## 1. 不同存储不是“谁快用谁”

常见系统：

```text
MySQL
Redis
Object Storage
Vector DB
MQ
Agent Runtime Store
```

每个系统应该承担不同角色。

---

## 2. Source of Truth

Source of Truth 是出现冲突时最终应该相信的事实来源。

例如用户余额：

```text
MySQL = durable business truth
Redis = cache
```

如果二者不一致，通常应以 MySQL 为准，再修复 Cache。

如果角色没定义，就会出现：

```text
DB says A
Redis says B
Which one wins?
```

---

## 3. MySQL 适合什么

典型：

- durable business entity；
- transaction；
- audit trail；
- relational constraint；
- source of truth。

例如：

```text
user
order
subscription
task metadata
billing record
```

MySQL 章节负责 Index / Transaction / Lock 等内部机制。

---

## 4. Redis 适合什么

典型：

- cache；
- short-lived state；
- session；
- quota / rate limit；
- ephemeral coordination；
- hot progress；
- distributed lock 辅助。

但 Redis 快不代表：

> 所有状态都应该扔 Redis。

如果一个状态丢失后无法从其它地方恢复，就必须认真评估 durability 和 audit requirement。

---

## 5. Session State

Session 可能包含：

```text
login session
shopping flow
chat session metadata
agent session pointer
```

多实例服务不能把它只存在进程内：

```text
request 1 → instance A
request 2 → instance B
```

如果只有 A 内存有状态，B 无法继续。

常见方案：

- external session store；
- signed token 中携带有限状态；
- sticky session（谨慎）；
- durable DB + hot Redis。

---

## 6. Sticky Session 的边界

Load Balancer 让同一用户尽量回到同一实例。

优点：

- 减少外部 Session Store 访问；
- 某些长连接场景简单。

缺点：

- 实例故障状态丢失；
- 扩容/缩容不平衡；
- failover 麻烦；
- 不利于真正 Stateless。

因此 Sticky Session 不应该成为“把重要状态留在内存”的借口。

---

## 7. Runtime State vs Business State

Agent 场景尤其要区分。

### Business State

```text
order created
payment success
ticket opened
```

通常需要 durable source of truth。

### Runtime State

```text
current step
pending tool
last event cursor
context snapshot
```

可能由 Agent Runtime / Checkpoint Store 管理。

不要把 Runtime Checkpoint 当作业务数据库。

---

## 8. Cache State

Cache 应该满足：

> 丢了可以从 Source of Truth 重建。

如果 Cache 丢失会让业务永久丢数据，那它已经不是“仅 Cache”。

这是判断某个 Redis Key 是否设计合理的一个很好问题。

---

## 9. Derived State

很多系统保存派生状态：

```text
search index
vector index
materialized view
cache
analytics projection
```

它们应该记录：

- source identity；
- source version；
- processing version；
- rebuild strategy。

RAG 章节已经用 Document Lineage / Generation 深入讲过。

---

## 10. State Lifetime

状态不仅有“放哪里”，还有“活多久”。

| 状态 | 常见生命周期 |
|---|---|
| Auth Access Token | 短 |
| Login Session | 小时/天 |
| Cache | 秒/分钟/小时 |
| Job Progress | 任务期间 |
| Audit Record | 长期 |
| Agent Event | 根据 Replay / Audit 需求 |

TTL 是业务语义，不只是省内存。

---

## 11. Multi-tenant Key Design

任何共享存储都要问：

```text
tenant_id 在哪里？
```

例如 Redis：

```text
tenant:{tenant_id}:session:{session_id}
```

DB：

```text
tenant_id column / schema / database boundary
```

Vector DB：

```text
tenant filter / collection / partition
```

不能只在 API 层校验 Tenant，然后下层查询忘记过滤。

---

## 12. Data Layering Example

AI SaaS：

```text
MySQL
├─ user / tenant
├─ kb metadata
├─ run/task durable status
└─ billing

Redis
├─ session
├─ hot cache
├─ rate limit
├─ short progress
└─ coordination

Object Storage
└─ uploaded source files

Vector DB
└─ retrieval index

Agent Checkpoint Store
└─ runtime execution state
```

这个分层比“MySQL + Redis + Vector DB 都会用”更重要。

---

## 13. Failure Recovery

问每种状态：

```text
Redis flush 以后怎么恢复？
DB backup restore 以后 derived index 怎么重建？
Vector index rebuild 时新数据怎么办？
Agent checkpoint 丢失是否影响业务事实？
```

能回答这些，才真正知道 State Ownership。

---

## 14. 🎯 面试怎么答

**问：MySQL 和 Redis 怎么分工？**

可以回答：

> 我不会按“慢/快”简单区分。MySQL 更适合 durable 业务事实、事务和审计；Redis 更适合 Cache、Session、Rate Limit、短期状态和协调。关键是先定义 Source of Truth：Cache 丢失后应该能从 Durable State 重建。对于 Agent，还要把 Business State 和 Runtime Checkpoint 分开，不能用 Redis/Checkpoint 随意替代业务事实库。

---

## 15. ⚠️ 易错点

- Redis 快 ≠ 所有状态都放 Redis；
- Session ≠ 必须 Sticky；
- Agent Checkpoint ≠ Business DB；
- Cache 丢失无法恢复时，它已经不是普通 Cache；
- Tenant Isolation 不能只在 API 层做一次。

---

## 16. 本章自测

<details>
<summary>1. 如何判断一个 Redis Key 是 Cache 还是 Source of Truth？</summary>

问它丢失后是否可以从其它 Durable Source 重建。如果无法重建且业务永久丢失，它就承担了事实存储职责，需要按 durability / backup / audit 标准设计。

</details>

<details>
<summary>2. 为什么 Agent Checkpoint 不应该直接当业务订单状态？</summary>

Checkpoint 记录执行 Runtime，可能被压缩、清理或按 Run 生命周期管理；订单属于长期业务事实，需要独立事务、审计和一致性语义。

</details>

<details>
<summary>3. Multi-tenant Isolation 为什么要贯穿存储层？</summary>

如果只有 API 层检查 Tenant，下层某个 Query / Cache Key / Vector Filter 漏掉 tenant_id，就可能产生跨租户数据泄漏。

</details>