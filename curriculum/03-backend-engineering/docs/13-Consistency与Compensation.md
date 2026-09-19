# 13. 最终一致性、DB + Cache、Outbox、Saga 与 Compensation

> 分布式系统里最难的问题之一不是“怎么写”，而是：**一个操作跨多个系统部分成功后，怎样让最终状态重新一致？**

## 1. 为什么会有最终一致性

单个数据库事务可以在一个事务边界内提供较强原子性。

但真实 Backend 往往跨：

```text
MySQL
Redis
MQ
Payment API
Search Index
Vector DB
External Tool
```

你无法假设这些系统共享一个事务。

所以必须面对：

```text
Partial Success
```

---

## 2. DB + Cache 的经典问题

读取：

```text
read cache
→ hit: return
→ miss: read DB
→ write cache
```

这就是常见 Cache Aside Read Path。

写入时麻烦开始：

```text
update DB
then invalidate cache
```

如果 DB 成功、删除 Cache 失败：

```text
DB = new
Cache = old
```

出现短暂不一致。

---

## 3. 为什么“先删 Cache 再写 DB”也不完美

Timeline：

```text
Writer deletes cache
↓
Reader cache miss
↓
Reader reads old DB value
↓
Reader writes old value back to cache
↓
Writer updates DB
```

最终：

```text
DB = new
Cache = old
```

所以“先删还是先写”不是一道背结论题，而要画 Failure Window。

---

## 4. 常见策略：DB 先写，Cache 后删

```text
DB transaction commit
↓
cache invalidate
```

这让数据库继续做 Source of Truth。

但删 Cache 仍可能失败。

所以需要进一步设计：

- retry invalidation；
- event / CDC；
- short TTL；
- reconciliation；
- versioned cache。

---

## 5. 延迟双删为什么不是万能答案

常见技巧：

```text
delete cache
update DB
wait
again delete cache
```

它试图覆盖并发读回填旧值的窗口。

问题：

- delay 很难精确；
- process crash；
- 第二次 delete 失败；
- 高并发 timing 不可控。

可以作为某些系统的补充策略，但不能当成“一致性标准答案”。

---

## 6. Event-driven Invalidation

更系统：

```text
DB update
→ Outbox / CDC Event
→ Consumer invalidates cache
```

优点：

- 业务 Commit 与 Event Source 更接近；
- Consumer 可以 Retry；
- 可观测；
- 可重放。

代价：

- Eventual Consistency；
- duplicate event；
- consumer lag；
- schema evolution。

---

## 7. Versioned Cache

Cache Value 带版本：

```json
{
  "version": 42,
  "value": {...}
}
```

更新时只接受更高版本。

可以减少乱序 Event 把 Cache 回滚到旧状态。

这种思想也常用于：

- RAG generation；
- config version；
- session state。

---

## 8. 最终一致性不是“迟早会一致”

要明确：

```text
Convergence Mechanism
```

也就是到底**靠什么**最终修复。

可能是：

- TTL；
- Retry；
- MQ redelivery；
- CDC；
- Periodic reconciliation；
- user read repair。

如果没有收敛机制，只是“希望它之后一致”，不叫可靠设计。

---

## 9. Compensation

跨服务事务如果已经产生外部副作用，通常不能真的 Rollback。

例如：

```text
reserve inventory succeeded
payment succeeded
email failed
```

你不能简单把所有世界回滚。

Compensating Action 是一个**新的业务操作**：

```text
refund payment
release inventory
send cancellation event
```

它本身也可能失败。

---

## 10. Saga 思想

把长业务拆成多个局部事务：

```text
T1 → T2 → T3
```

失败后：

```text
C2 → C1
```

其中 C 是补偿。

两种常见协调思路：

- Orchestration：有中心协调者；
- Choreography：服务通过 Event 协作。

本课程不要求记所有术语，而要理解：

> 每个 Step 都要定义 forward action + compensation / reconciliation。

---

## 11. Compensation 不是反向 SQL

比如：

```text
send email
```

没有真正的“撤回世界”。

补偿可能是：

```text
send correction email
```

支付补偿是 Refund，不是“数据库 UPDATE 回原值”。

所以 Saga 是业务语义，不只是技术事务。

---

## 12. Agent Tool 的部分成功

Agent Workflow：

```text
create ticket
→ send email
→ update CRM
```

如果 CRM 失败：

- Ticket 是否删除？
- Email 已发无法收回怎么办？
- 是否人工接管？

这就是 Agent Runtime Side Effect 与 Backend Compensation 的交叉边界。

---

## 13. Reconciliation

当线上链路无法保证每个瞬间一致时，需要后台对账：

```text
scan source of truth
vs derived state
→ detect divergence
→ repair
```

例如：

```text
DB order status
vs Redis cache
vs search index
vs external payment state
```

Reconciliation 是最终一致性的重要“兜底闭环”。

---

## 14. Cache Consistency 的验证

不要只单元测试正常路径。

应该模拟：

```text
DB success + cache delete fail
cache delete success + DB rollback
consumer duplicate
consumer delay
out-of-order event
cache node restart
```

只有 Failure Injection 才能验证设计。

---

## 15. Metrics

```text
cache_stale_detected
invalidation_failures
cdc_lag
outbox_pending
reconciliation_mismatch
compensation_attempts
compensation_failures
```

这些比单纯 Cache Hit Rate 更接近正确性。

---

## 16. 🎯 面试怎么答

**问：DB 和 Redis 双写怎么保证一致性？**

可以回答：

> 我会先把 DB 作为 Source of Truth，Cache 是派生状态。常见路径是先提交 DB，再失效 Cache，但必须考虑 Cache 删除失败窗口。生产系统会配合 Retry、TTL、Outbox/CDC Event、版本号和 Reconciliation，让错误状态最终收敛。不能只背“先删缓存还是先写 DB”，要画具体 Failure Window。

---

## 17. ⚠️ 易错点

- 最终一致性 ≠ 没有一致性设计；
- 延迟双删 ≠ 万能；
- Compensation ≠ 真正 Rollback；
- MQ Event ≠ 自动顺序正确；
- Cache 是 Derived State 时不要反过来成为唯一事实来源。

---

## 18. 本章自测

<details>
<summary>1. 什么才叫“最终会一致”？</summary>

必须存在明确 Convergence Mechanism，例如 Retry、CDC、TTL、Reconciliation 等，而不是只是相信系统以后会自己恢复。

</details>

<details>
<summary>2. Compensation 为什么不能简单理解成 Rollback？</summary>

外部副作用往往无法物理撤销，补偿是新的业务操作，例如退款、释放库存、发纠正通知，并且补偿本身也可能失败。

</details>

<details>
<summary>3. 为什么 Cache Invalidation 可以用 Version 防乱序？</summary>

Event 可能延迟或乱序，带版本后 Consumer 可以拒绝比当前更旧的更新，避免旧 Event 把新状态覆盖掉。

</details>