# 08｜Consistency、Idempotency、Transaction 与 Compensation

分布式系统真正难的地方不是“写成功”，而是：

> **一个操作跨越多个状态系统时，部分成功、重复执行、网络超时和故障恢复怎样不把业务 invariant 弄坏。**

---

## 1. 先写业务 Invariant

不要先说：

> “这里要强一致。”

先写：

```text
库存不能被确认订单超卖
同一个支付请求不能重复扣款
同一 Agent Tool 副作用不能因 Retry 重复执行
同一通知至少不能无限重复发送
```

Invariant 比术语更接近业务正确性。

---

# 2. 单库 Transaction 能解决什么

如果状态都在同一个事务数据库里：

```text
BEGIN
UPDATE inventory
INSERT order
COMMIT
```

数据库事务能提供很强的局部原子性。

但一旦流程跨：

```text
DB
Redis
MQ
Payment Provider
LLM Tool
```

单库 Transaction 就不够了。

---

# 3. Idempotency 是 Retry 的前提

网络超时时，调用方常不知道：

```text
请求没到服务端？
服务端执行了但响应丢了？
```

所以创建/修改类操作需要：

```text
Idempotency Key
+
Request Fingerprint
+
Stored Result / State
```

典型语义：

```text
same key + same request
→ return same logical result

same key + different request
→ reject
```

Stripe 的公开 API 就使用这种模式安全支持 POST 重试。

---

# 4. Unique Constraint 是非常强的正确性工具

例如：

```text
UNIQUE(user_id, campaign_id)
```

可以从数据层保证：

```text
同一用户只能领取一次
```

这通常比：

```text
先 SELECT 再 INSERT
```

更可靠，因为并发下两次 SELECT 都可能看到“不存在”。

系统设计不要忽视数据库自身约束能力。

---

# 5. Optimistic Concurrency

例如：

```sql
UPDATE item
SET stock = stock - 1,
    version = version + 1
WHERE id = ?
  AND stock > 0
  AND version = ?;
```

核心：

```text
我只在状态仍是我看到的版本时更新
```

适合冲突不是极端频繁的场景。

---

# 6. Pessimistic Lock / Distributed Lock 什么时候考虑

如果多个执行者必须串行修改同一逻辑资源，可能需要锁。

但先问：

```text
能否用 DB constraint / CAS？
能否通过 partition single-writer？
能否把冲突转成 queue？
```

分布式锁引入：

```text
lease
owner
renewal
failover
stale holder
fencing
```

复杂度很高，不应作为默认答案。

---

# 7. Dual Write 是典型风险

例如：

```text
Update MySQL
→ Update Redis
```

可能：

```text
MySQL success
Redis fail
```

或者反过来。

所以先决定：

```text
谁是 SoT？
Cache 能否失效重建？
是否允许短暂 stale？
是否有 reconciliation？
```

对 Cache，很多时候：

```text
DB commit
→ invalidate cache
→ TTL / retry / repair
```

比追求跨 DB+Cache 原子提交更现实。

---

# 8. Eventual Consistency 不是“随便不一致”

它仍然需要定义：

```text
最终谁收敛到谁？
最大允许延迟多少？
失败怎样重试？
如何检测长期未收敛？
如何人工修复？
```

例如 Search Index：

```text
DB = SoT
Index lag < 30s
failed updates → retry queue
nightly reconciliation
```

这就是可运营的最终一致性。

---

# 9. Compensation：现实世界很多操作无法 Rollback

例如：

```text
发短信
调用外部支付
发送邮件
创建第三方工单
```

已经发生后，不能像数据库事务一样撤销。

只能设计补偿：

```text
Payment captured
→ later failure
→ issue refund
```

或者：

```text
Ticket created
→ mark cancelled
```

Compensation 是新的业务动作，不是真正时间倒流。

---

# 10. Saga 思想

长流程：

```text
Step A
→ Step B
→ Step C
```

每步都有：

```text
forward action
compensating action
```

如果 C 失败：

```text
compensate B
compensate A
```

但不是所有动作都可补偿，因此必须在业务设计阶段识别不可逆边界。

---

# 11. Reconciliation 是最后防线

即使有 Retry / Outbox / Idempotency，也可能存在长时间异常。

定期对账：

```text
orders vs payments
DB vs search index
source manifest vs vector index
agent run state vs external tool records
```

可以发现：

```text
stuck
missing
extra
diverged
```

真正可靠系统通常有“在线机制 + 离线修复”。

---

# 12. AI Agent 的副作用尤其要注意

Agent 可能自动：

```text
发邮件
改数据库
创建 PR
退款
删除文件
```

如果 Tool Timeout 后模型重试：

```text
第一次其实成功
第二次又执行
```

可能造成灾难。

所以 Tool Contract 应带：

```text
operation_id
idempotency
read-only / destructive metadata
approval
result lookup
```

这部分底层 Runtime 在 Agent Harness，System Design 负责把它组合到业务流程。

---

# 13. 🎯 面试怎么答

> 我会先写清业务 invariant，再决定需要哪一级一致性。单库状态优先使用数据库事务、唯一约束和 CAS；跨系统时不轻易追求全局事务，而是明确 Source of Truth，使用 Idempotency、Outbox、Retry、Version 和 Reconciliation。对不可逆外部副作用会设计 Compensation，并让 Retry 以业务 Operation ID 去重。最终一致性也必须有 Freshness SLO 和检测长期未收敛的方法。

---

# 14. 本章自测

<details><summary>1. 为什么 Timeout 后不能直接假设请求失败？</summary>
网络超时只表示客户端没拿到结果，服务端可能已经执行成功，因此重试前需要幂等或结果查询。
</details>

<details><summary>2. 为什么 Compensation 不等于 Rollback？</summary>
外部副作用已经真实发生，补偿只是执行一个新的反向业务动作，无法保证世界恢复到完全相同状态。
</details>

<details><summary>3. Eventual Consistency 需要哪些运营机制？</summary>
需要明确 SoT、收敛方向、Freshness SLA、Retry、Dead-letter/异常记录和 Reconciliation。
</details>
