# 13｜High-concurrency Transactional Systems：秒杀、库存、Rate Limit、Token Refresh

这一章不是背“秒杀标准答案”，而是训练一类共同问题：

> **大量并发请求争夺有限资源，同时要求不能重复、不能越界，并且失败后还能恢复。**

对应真人 Scenario 主要包括：

```text
SD-001 Flash Sale / Inventory
SD-009 Distributed Rate Limiter
SD-010 Token Refresh Coordination
SD-011 QR Login
```

---

## 1. 共同抽象：Scarce Resource + Concurrent Contention

四个场景看起来不同：

```text
库存
配额
Access Token Refresh
二维码状态
```

但都可以抽象成：

```text
很多 Caller
→ 争夺 / 更新有限状态
→ 需要确定唯一结果
→ 要处理重复请求与超时
```

因此先复用 Part A：

```text
Invariant
→ State Owner
→ Idempotency
→ Atomic Update
→ Hot Path
→ Backpressure
→ Failure Recovery
```

---

# 2. 秒杀先写 Invariant

核心不是 Redis，而是：

```text
confirmed_orders <= sellable_stock
```

还要定义：

```text
同一用户是否限购？
下单占库存还是付款占库存？
未支付订单多久释放？
取消订单是否回补？
```

如果这些没说清，后面所有技术都是空的。

---

# 3. 秒杀的最小数据流

一种常见设计：

```text
Client
→ API / Admission
→ user/item validation
→ atomic stock reservation
→ create order intent
→ async order processing
→ persist final order
→ payment / timeout / release
```

这里“atomic stock reservation”可以有不同实现：

- DB conditional update；
- Redis Lua / atomic command；
- Single-writer / partitioned queue；

没有唯一标准答案。

选哪个取决于 QPS、正确性、恢复和运维复杂度。

---

# 4. Redis 预扣不代表库存事实自动一致

如果：

```text
Redis stock-- 成功
DB order 写失败
```

需要：

```text
Retry
or
Compensation
or
Reconciliation
```

反过来：

```text
DB order 成功
Redis 响应丢失
Client retry
```

需要 Idempotency 防重复订单。

所以真正系统必须有：

```text
operation_id
order state
reservation state
reconciliation
```

而不是只有一段 Lua。

---

# 5. Hot Product 怎么防止把 DB 打穿

秒杀最典型是：

```text
one item
→ huge traffic
```

可以：

```text
Admission Control
→ reject invalid / over-quota early
→ in-memory / Redis hot state
→ queue accepted work
→ DB only sees bounded throughput
```

这就是“削峰”的真正含义：

> 不是让总工作消失，而是让下游以稳定速率处理。

---

# 6. Distributed Rate Limiter 的系统问题

Rate Limit 不是只会写 Sliding Window。

System Design 需要回答：

```text
quota 是 global 还是 per-region？
允许多少误差？
Redis / limiter 挂了 fail-open 还是 fail-closed？
低延迟要求多高？
一个 hot tenant 怎么办？
```

## Strong Global Limit

如果所有 Region 都访问中央 Counter：

```text
准确
但 latency / availability 受中央依赖影响
```

## Local Token Allocation

中央配额拆成：

```text
region A gets 1000 tokens
region B gets 1000 tokens
```

本地判定很快，但会有：

```text
unused quota
rebalancing
short-term overshoot / underutilization
```

这是典型 Consistency vs Latency Trade-off。

---

# 7. Token Refresh Coordination

多实例服务同时发现：

```text
access token expired
```

如果每个实例都 refresh：

```text
Refresh Stampede
```

更合理：

```text
read cached token
→ near expiry
→ one owner refreshes
→ others wait / serve safe old token
→ publish new token/version
```

核心问题：

- refresh owner；
- lease timeout；
- old token 是否仍有效；
- refresh 失败怎么办；
- owner 崩溃怎么办。

这和 Cache Stampede + Distributed Lock 有共通模式。

---

# 8. 不一定需要“锁”

可以用：

```text
singleflight within process
Redis lock / lease
DB row / CAS
versioned token record
```

如果 Token Provider 自身允许重复 refresh 且返回稳定结果，锁需求会下降。

所以先看 Side Effect 语义，再选协调方式。

---

# 9. QR Login 的状态机

二维码登录看似前端题，实际上是状态设计题：

```text
CREATED
→ SCANNED
→ CONFIRMED
→ EXCHANGED
→ EXPIRED
```

PC 端：

```text
poll / SSE / websocket
```

手机端：

```text
authenticated user confirms qr_id
```

最终 PC 端才能换取 Session / Token。

---

# 10. QR Login 的安全边界

要防：

```text
二维码被复制
旧二维码重放
未登录手机伪确认
PC session 被错误绑定
```

常见约束：

```text
short TTL
one-time exchange
state transition CAS
bind device/session nonce
server-side auth
```

二维码本身不应该直接携带长期 Credential。

---

# 11. Failure Walkthrough：秒杀

主动演练：

### Redis 成功，DB 失败

→ reservation stuck / need compensation or retry。

### DB 成功，Response 丢失

→ Client retry，Idempotency 返回原订单。

### MQ 重复投递

→ order processor 按 order_id / operation_id 去重。

### Hot Key 过载

→ Admission / Local Cache / sharded counter / queue protection。

### Worker 全挂

→ Queue grows；Alert Queue Age；恢复后限速 Drain。

---

# 12. 怎样验证没有 Oversell

不是只压测吞吐。

测试必须校验 invariant：

```text
initial_stock = 10000
successful_confirmed_orders <= 10000
unique_user_constraint holds
no duplicated order for same operation
all reservations eventually settled/released
```

Chaos Test：

```text
kill worker
lose response
duplicate message
slow DB
restart Redis replica
```

再验证状态最终收敛。

---

# 13. 真人面经影响在哪里

`SD-001` 有 10 个独立来源，是 System Design 强信号之一。

因此这一章特别强化：

```text
Oversell / Undersell
Redis + DB consistency
Order state
Compensation
Hot traffic
Verification
```

但教材没有把“秒杀”放在第 1 章，而是在学完 Requirement / Capacity / State / Consistency 后才进入综合 Case。

---

# 14. 🎯 面试怎么答

> 这类高并发有限资源系统我会先定义业务 invariant，例如库存不能被确认订单超卖，并明确资源真正的 State Owner。入口先做 Admission / 限购，Hot Path 用原子操作或单写模型保护，再把后续订单处理异步化以保护 DB。所有创建类操作都有 operation/idempotency key，Redis、DB、MQ 之间的部分成功通过状态机、Retry、Compensation 和 Reconciliation 收敛。最后压测不仅看 QPS，还会验证库存、订单和 reservation invariant，并注入重复消息、响应丢失和 Worker Crash。

---

# 15. 本章自测

<details><summary>1. 为什么“Redis Lua 扣库存成功”还不能证明秒杀设计正确？</summary>
因为后续订单持久化、支付、消息和补偿仍可能部分失败，需要跨状态系统保持业务 invariant。
</details>

<details><summary>2. Distributed Rate Limiter 为什么可能允许短期误差？</summary>
如果追求跨 Region 每次都强同步，会增加延迟和单点依赖；部分系统会用本地配额换取低延迟与高可用。
</details>

<details><summary>3. QR Login 为什么适合状态机建模？</summary>
因为创建、扫描、确认、交换、过期是明确单向状态迁移，能防止重复确认和旧二维码重放。
</details>
