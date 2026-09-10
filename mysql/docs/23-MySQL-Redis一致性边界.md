# 23. MySQL + Redis Consistency 的边界

这一章故意放在整个 MySQL 模块最后。

原因很重要：

> **先把 MySQL 自身的事务、索引、日志、复制、数据模型学清楚，再讨论“为什么还要加 Redis，以及两份数据如何协作”。**

如果一开始就学“延迟双删”“Cache Aside”，很容易变成背方案名，却不知道 Source of Truth、Transaction Boundary 和 Failure Window 到底是什么。

本章的 Primary 知识其实属于 **AI Backend Engineering**；放在 MySQL 模块末尾，是为了完成数据层认知闭环，而不是把跨系统一致性重新归到 MySQL 内部机制。

---

## 1. 先讲人话：为什么有 MySQL 还要 Redis

MySQL 擅长：

```text
关系数据
事务
持久化
约束
复杂查询
```

Redis 擅长：

```text
内存访问
低延迟
Cache
Session
Counter
Temporary State
```

所以常见架构：

```text
Client
  ↓
Application
  ├── Redis Cache
  └── MySQL Source of Truth
```

目标是：

> **大多数高频读取尽量命中 Redis，但最终业务事实仍以 MySQL 为准。**

---

# 2. 第一个原则：先明确谁是 Source of Truth

典型 Cache 场景里：

```text
MySQL = Source of Truth
Redis = Derived / Disposable Cache
```

意味着：

- Redis 丢了，可以从 MySQL 重建；
- Redis 和 MySQL 冲突时，最终以 MySQL 为准；
- 业务提交成功的边界首先由 MySQL Transaction 定义；
- Redis 不是靠“更快”就自动变成主数据源。

如果这个关系不清楚，后面所有一致性方案都会混乱。

---

# 3. Cache Aside 是什么

最常见模式：

## Read

```text
1. Read Redis
2. Hit → Return
3. Miss → Read MySQL
4. Write Cache
5. Return
```

## Write

常见思路：

```text
1. Update MySQL
2. Delete Cache
```

注意是：

```text
Delete Cache
```

而不是默认：

```text
Update MySQL + Update Cache
```

为什么？

因为直接双写两个存储会放大顺序和失败组合。

---

# 4. 为什么“更新数据库后删除缓存”很常见

假设旧值：

```text
MySQL = A
Redis = A
```

业务更新成 B：

```text
UPDATE MySQL → B
DELETE Redis
```

之后读取：

```text
Redis Miss
→ MySQL B
→ Cache B
```

这让 Cache 自然被新值重建。

它的核心思想是：

> **缓存只保存可失效的派生副本，不承担业务提交本身。**

---

# 5. 为什么不能说 Cache Aside“强一致”

考虑并发：

```text
Reader A: Cache Miss
Reader A: Read MySQL old=A

Writer B: Update MySQL B
Writer B: Delete Cache

Reader A: Write old=A back to Cache
```

最终可能出现：

```text
MySQL = B
Redis = A
```

直到：

```text
TTL 到期
下一次失效
补偿任务修复
```

所以即使采用经典顺序，也仍可能存在短暂 Failure / Race Window。

正确表述应该是：

> **Cache Aside 通常追求最终一致性，而不是跨 MySQL + Redis 的原子强一致。**

---

# 6. 先删 Cache，再更新 DB 为什么也有问题

流程：

```text
1. DELETE Cache
2. UPDATE MySQL
```

并发可能：

```text
Writer: Delete Cache
Reader: Cache Miss
Reader: Read old MySQL=A
Reader: Write A into Cache
Writer: Update MySQL=B
```

最终：

```text
MySQL=B
Redis=A
```

所以简单改变顺序并不能让问题消失。

---

# 7. “延迟双删”是什么思路

一种常见补偿思路：

```text
Delete Cache
→ Update DB
→ 等待一小段时间
→ Delete Cache again
```

目标是：

> 如果并发 Reader 在窗口中把旧值重新写入 Cache，第二次 Delete 尝试清掉它。

但它不是数学意义上的完美方案，因为：

- 延迟时间不好精确选；
- 第二次 Delete 也可能失败；
- 服务 Crash 会中断；
- 并发窗口仍然复杂。

所以它是：

```text
降低不一致窗口的工程技巧
```

不是：

> “加延迟双删就实现强一致。”

---

# 8. TTL 为什么是最后保险

Cache 通常应该有合理 TTL：

```text
即使删除失败
旧数据也不会永久存在
```

TTL 不是一致性主方案，但可以限定：

```text
Stale Data 最长生存时间
```

所以：

```text
主动 Invalidation
+
TTL
+
Monitoring / Repair
```

通常比只依赖单一机制更可靠。

---

# 9. 删除缓存失败怎么办

假设：

```text
MySQL UPDATE 成功
Redis DELETE 超时
```

业务已经提交，但 Cache 可能还是旧值。

不能把 MySQL Transaction ROLLBACK 来“自动回滚 Redis”，因为：

```text
Redis 不在这个本地事务里
```

常见处理：

- Retry；
- MQ / Outbox；
- CDC 驱动 Cache Invalidation；
- Background Repair；
- TTL。

这里开始正式进入 Backend Reliability。

---

# 10. 用 Binlog / CDC 做 Cache Invalidation

一种很自然的方案：

```text
Application
→ Commit MySQL
→ Binlog
→ CDC Consumer
→ Delete / Update Redis Cache
```

好处：

```text
只要 MySQL 事务成功
变化事实就进入 Binlog
```

Cache Invalidation 不再依赖请求线程必须同步完成。

但仍要处理：

```text
CDC Lag
Duplicate Event
Consumer Failure
Redis Failure
```

所以还是最终一致，不是魔法强一致。

---

# 11. Outbox + MQ

如果业务事件更明确，可以在 MySQL 本地事务中：

```text
UPDATE business table
+
INSERT outbox_event
```

同一个 Transaction COMMIT。

之后：

```text
Outbox Publisher
→ MQ
→ Cache Invalidation Consumer
```

这样可以保证：

> **业务写和“需要发布一个事件”这件事，至少在 MySQL 内部是同一个原子事务。**

后续 Event Delivery 仍然要：

- Retry；
- Idempotency；
- Dead Letter；
- Monitoring。

---

# 12. 为什么“双写 Redis + MySQL”更难

如果你要求：

```text
Write MySQL
+
Write Redis
```

两个都必须成功，组合状态有：

```text
MySQL success / Redis success
MySQL success / Redis fail
MySQL fail / Redis success
MySQL fail / Redis fail
```

再加上：

```text
Timeout but unknown outcome
```

状态更多。

因此 Cache 模式常更偏向：

```text
MySQL commit
→ Cache invalidate
```

而不是维护两个同时可写的主副本。

---

# 13. Write-through / Write-behind 是什么

为了建立完整地图，需要知道还有其它 Cache Pattern。

## Write-through

应用写 Cache Layer，由 Cache Layer 同步写底层 Store。

```text
App
→ Cache
→ DB
```

调用方看到一层统一接口。

## Write-behind / Write-back

先写 Cache，再异步刷 DB。

```text
App
→ Cache
→ later DB
```

吞吐高，但：

- Cache 故障可能丢数据；
- Durability 复杂；
- Recovery 复杂。

一般业务 MySQL + Redis 场景里，不能因为“快”就随便采用 Write-behind。

---

# 14. 热点数据更新频繁时怎么办

假设：

```text
某 Agent Marketplace 榜单
每秒更新几万次
```

如果每次：

```text
MySQL UPDATE
→ DELETE Cache
→ Reader 回源
```

可能造成大量 Cache Miss / DB 压力。

这时可能需要：

- Coalescing；
- Short TTL；
- Async Aggregate；
- Local Cache；
- Event-driven Update；
- Separate Read Model。

一致性方案必须结合 Read / Write Pattern，而不是固定套模板。

---

# 15. 缓存雪崩、击穿、穿透和一致性是什么关系

它们相关，但不是一回事。

```text
Consistency
→ DB 与 Cache 内容是否同步

Penetration
→ 查询不存在的数据，Cache 永远 Miss

Breakdown / Stampede
→ Hot Key 失效瞬间大量请求回源

Avalanche
→ 大量 Key 同时失效 / Cache 故障导致大量回源
```

这些会在 Redis 模块系统学习。

MySQL 这章只要求你清楚：

> Cache 失败最后经常会把压力打回 MySQL。

---

# 16. AI Application 场景：Tenant 配置

假设：

```text
Tenant Settings
Model Policy
Quota
Feature Flags
```

Source of Truth：

```text
MySQL
```

高频读：

```text
Redis Cache
```

更新：

```text
Admin UPDATE MySQL
→ Commit
→ Delete Cache / Publish Event
```

读取：

```text
Cache Hit → Return
Cache Miss → Read MySQL → Set Cache
```

但如果是：

```text
Security Permission
Billing Balance
```

你可能不能容忍太长 Stale Window。

所以 TTL 和读路由策略要更严格。

---

# 17. AI Application 场景：Agent Run 状态要不要缓存

如果 Run 状态每秒变化：

```text
QUEUED
RUNNING
WAITING_TOOL
RUNNING
DONE
```

前端每秒 Poll：

```text
GET /runs/123
```

可以 Cache，但要考虑：

```text
状态更新频率很高
Cache Invalidations 很频繁
Stale Status 用户是否能接受
```

很多系统可能直接：

- Redis 存 Current Ephemeral State；
- MySQL 存 Durable Run State / History；
- Streaming Push 最新事件；

这时已经不是简单 Cache Aside，而是 Agent Runtime Data Architecture。

Primary 会进入 Redis / Agent Harness / System Design。

---

# 18. 如何定义“一致到什么程度”

面试中最成熟的第一句话往往不是：

> “我们用延迟双删。”

而是：

> **先定义业务允许多长时间的不一致，以及错误方向能否接受。**

例如：

```text
商品详情 3 秒旧值
→ 可能接受

用户权限 3 秒旧值
→ 可能是安全漏洞

余额 3 秒旧值
→ 可能导致超额消费
```

所以 Consistency Level 是业务 Requirement，不只是技术方案。

---

# 19. 验证一致性不能只看代码

需要监控：

```text
Cache Hit Rate
Cache Miss Rate
DB Fallback QPS
Invalidation Failure
CDC Lag
Stale Read Sample
Hot Key
Redis Error Rate
```

还可以定期：

```text
抽样对比 Redis 与 MySQL
```

发现长时间不一致。

---

# 20. 面试怎么答

## Q：MySQL 和 Redis 如何保证一致性？

🎯 推荐回答：

> 我会先说明通常 MySQL 是 Source of Truth，Redis 是可重建 Cache，所以目标大多是可控的最终一致，而不是跨两个系统做强原子事务。常见 Cache Aside 写路径是先提交 MySQL，再删除 Cache；读时 Cache Miss 回源 MySQL 并重建。这个方案仍有并发回填旧值和删除失败等窗口，所以会结合 TTL、Retry、Outbox / MQ 或 Binlog CDC 做异步 Invalidation，并通过幂等和监控控制不一致窗口。对权限、余额等高一致性数据，还要根据业务要求选择读 Source 或更严格策略。

## Q：为什么更新 DB 后删 Cache，而不是同时更新 Cache？

> Cache 是派生副本，删除让下一次读取从 Source of Truth 重建，减少“数据库和缓存两个可写副本”之间的顺序组合。它仍不是绝对强一致，但故障模型更简单。

---

# 21. 高频易错点

⚠️ **Cache Aside 是强一致。**  
不是，仍有 Race / Failure Window。

⚠️ **延迟双删能彻底解决一致性。**  
不能，只是降低某些窗口。

⚠️ **MySQL Transaction 能回滚 Redis。**  
Redis 不在本地 InnoDB Transaction 里。

⚠️ **删 Cache 失败就让 DB Rollback。**  
跨系统结果和 Timeout 状态会让这种思路非常脆弱。

⚠️ **所有业务允许同样的 Stale Window。**  
权限、余额、普通列表要求完全不同。

---

# 22. 本章自测

<details>
<summary>1. 为什么 Cache Aside 常把 MySQL 作为 Source of Truth？</summary>

因为 MySQL 提供事务、持久化和业务约束，Cache 可以失效并由数据库重建；这样系统只有一个权威业务事实来源，Redis 只是性能层。

</details>

<details>
<summary>2. 为什么“先更新 DB，再删 Cache”仍可能出现旧 Cache？</summary>

并发 Reader 可能在 DB 更新前读取旧值，然后在 Writer 删除 Cache 之后才把旧值写回 Redis，形成短暂脏缓存，因此仍需 TTL、补偿或事件驱动失效等机制。

</details>

<details>
<summary>3. CDC 为什么适合做 Cache Invalidation？</summary>

MySQL 事务成功后变化会进入 Binlog，CDC 可以从已提交事实异步驱动 Cache 失效，减少请求线程同步双写失败窗口；但仍需处理 Lag、重复事件和 Consumer 故障。

</details>

<details>
<summary>4. 为什么权限数据和普通列表缓存不能使用同样的 TTL？</summary>

因为 Stale Data 的业务风险不同。普通列表短暂旧值可能可接受，而权限旧值可能造成越权，余额旧值可能造成超额消费，因此一致性预算必须按业务定义。

</details>

---

## MySQL 主体完成

到这里 MySQL 模块的知识体系形成了一条完整 0→1 主线：

```text
AI Application 为什么需要关系数据库
→ SQL / Execution
→ Index / B+Tree
→ Composite / Covering / Optimizer / EXPLAIN
→ Transaction / Isolation / MVCC / Lock
→ Redo / Undo / Binlog / Recovery
→ Pagination / Schema
→ Replication
→ Sharding
→ CDC
→ Bulk Write
→ AI Application Data Modeling
→ MySQL + Redis Integration Boundary
```

面经只决定哪些地方要标成高频、需要多加追问；这条主干本身按知识依赖顺序组织。

---

## 下一环

下一模块进入：**Redis**。

这时会把本章碰到但没有展开的：

```text
Data Structure
Thread Model
I/O Multiplexing
TTL / Eviction
Cache Penetration / Breakdown / Avalanche
BigKey / HotKey
Persistence
Distributed Lock
Lua
Session / Agent State
Rate Limit
```

从 0 系统建立起来。
