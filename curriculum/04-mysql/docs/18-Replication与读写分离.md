# 18. Replication 与读写分离

前面所有内容默认都是：

```text
一个 MySQL 实例
```

但真实系统数据量、读取量和容灾要求上来以后，最自然的问题是：

> **能不能保留一个主要写入节点，再让多个 Replica 承担读请求、备份和异地分发？**

这就是 Replication。

---

## 1. 先讲人话：复制是在维护“同一份数据的多个副本”

最简单结构：

```text
             Write
Client ─────────────▶ Source
                       │
                       │ Binlog Events
                       ▼
                  Replica 1
                  Replica 2
                  Replica 3
```

Source 负责主要写入。

Replica 从 Source 获取变化并重放。

于是可以：

```text
写请求 → Source
读请求 → Replica
```

这就是常说的读写分离。

---

# 2. 为什么需要 Replication

Replication 不只是“提速”。

常见目标包括：

### Read Scale

```text
Source 专注写
多个 Replica 分担读
```

### Backup / Data Safety

可以在 Replica 上做一些备份工作，降低对 Source 的影响。

### Analytics

把分析读流量放到 Replica，减少 OLTP Source 压力。

### Geo Distribution

不同 Region / Site 有更近的数据副本。

### Failover 基础

Source 故障时，可以把合适的 Replica 提升为新的 Source。

注意：

> **Replication ≠ 自动高可用。**

真正 Failover 还需要检测、选主、流量切换和一致性策略。

---

# 3. Binlog 为什么是复制基础

上一章已经讲过：

```text
MySQL Source
  ↓
Binlog
  ↓
记录数据库变化 Event
```

Replica 要复制 Source，本质上需要知道：

> Source 提交了哪些变化？

所以经典复制链路是：

```text
Source Binlog
    ↓
Replica 获取 Event
    ↓
Relay / Apply
    ↓
Replica Local Data
```

这也是为什么 Binlog 不只是“备份日志”。

---

# 4. 异步复制的直觉

最常见的复制不是：

```text
Source COMMIT
必须等所有 Replica 全部 Apply 完
才返回客户端
```

而更接近：

```text
Source COMMIT
→ 返回
→ Replica 异步追赶
```

优点：

```text
Source 写延迟较低
```

代价：

```text
Replica 可能暂时落后
```

这就是 Replication Lag。

---

# 5. Replication Lag 为什么一定要认真理解

假设用户：

```text
1. POST 创建 Agent Run
2. 立刻 GET Run Detail
```

如果：

```text
POST 写 Source
GET 读 Replica
```

可能发生：

```text
Source 已经 COMMIT
Replica 还没 Apply
GET 返回 404 / 旧状态
```

这不是“数据库丢数据”，而是：

> **Read-after-write Consistency 被异步复制延迟打破。**

---

# 6. Read-after-write 怎么处理

没有一个万能方案，常见策略有：

## 6.1 刚写完的一段时间读 Source

```text
Write Session
→ Sticky to Source
```

简单直接。

## 6.2 关键读永远走 Source

比如：

```text
支付状态
刚创建订单
权限更新
```

## 6.3 等待 Replica 追到某个位置 / GTID

更严格，但实现复杂度更高。

## 6.4 接受 Eventual Consistency

很多：

```text
Feed
Analytics
非关键列表
```

允许几百毫秒或几秒延迟。

核心是：

> **先定义业务需要什么 Consistency，再决定读路由。**

---

# 7. “读写分离”不是把所有 SELECT 都丢给 Replica

下面查询可能必须走 Source：

```text
刚写后立刻读
需要最新库存
需要最新 Credits
事务内依赖最新状态
Locking Read
```

而下面更适合 Replica：

```text
历史报表
旧对话浏览
后台分析
允许轻微延迟的列表
```

所以读写分离的真正设计是：

```text
Query Consistency Requirement
→ Route to Source or Replica
```

不是简单按 SQL 类型分类。

---

# 8. Source 故障后会发生什么

如果 Source 挂了：

```text
Replica A lag 0.2s
Replica B lag 2s
Replica C lag 10s
```

该提升谁？

你需要考虑：

```text
谁的数据最完整？
谁健康？
谁能被提升？
旧 Source 恢复后怎么处理？
客户端如何切流？
```

所以高可用系统还要有：

- Health Check；
- Topology Manager；
- Promotion；
- Fencing；
- Connection / DNS / Proxy Routing；
- Split-brain Prevention。

这些部分属于 System Design / Database Operations 的扩展，不是本章必须全部手写实现。

---

# 9. 为什么会出现 Split Brain 风险

如果旧 Source 网络隔离，但其实还活着：

```text
Old Source 继续接受写
New Source 也开始接受写
```

就会出现两个写主：

```text
Source A → timeline A
Source B → timeline B
```

数据开始分叉。

所以 Failover 不能只是：

> “探测不到旧主，就把 Replica 提升。”

还要确保旧主被 Fencing，不能继续对外写入。

---

# 10. Semi-synchronous Replication 是什么直觉

异步复制：

```text
Source COMMIT
不等 Replica 确认
```

Semi-sync 会加强：

```text
Source 在提交返回前
至少等待一个 Replica 确认已经收到并记录事务事件
```

注意：

> “Replica 收到 / 持久化日志”不等于“Replica 已经 Apply 并对查询可见”。

所以 Semi-sync 能缩小某些数据丢失窗口，但不等于所有 Replica 强同步。

---

# 11. Replication 与 Backup 不是一回事

非常重要。

如果应用误执行：

```sql
DELETE FROM users;
```

Source 会删。

Replica 也会复制删除事件。

所以 Replication 不能替代：

```text
Backup
PITR
Delayed Replica
Recovery Drill
```

因为：

> **复制会忠实复制“错误”。**

---

# 12. Delayed Replica 为什么有价值

可以让某个 Replica 故意延迟一段时间：

```text
Source 发生误删
普通 Replica 很快也删了
Delayed Replica 还停留在更早状态
```

这为人为错误提供额外恢复窗口。

但它同样不是完整 Backup 策略的替代品。

---

# 13. Replication Format 和并行 Apply

大型系统里 Replica Lag 可能不是网络问题，而是：

```text
Source 提交速度
>
Replica Apply 速度
```

可以关注：

- Binlog Event Format；
- Parallel Replication；
- Transaction Dependency；
- Large Transaction；
- Hot Row / Hot Table；
- Disk I/O。

例如一个超大事务：

```text
Source 提交一次
Replica 要重放很久
```

可能造成明显 Lag Spike。

---

# 14. GTID 是什么层级的知识

GTID = Global Transaction Identifier。

初学阶段不需要背所有格式，先理解它解决：

> **用全局事务身份标识复制过哪些事务，而不只是手工依赖某个 Binlog File + Position。**

这使：

- Failover；
- Repoint Replica；
- 判断事务集合；

更容易管理。

---

# 15. AI Application 场景

假设：

```text
Source
→ Agent Run / Billing / Permission 写入

Replica
→ Conversation History Browse
→ Admin Analytics
→ Evaluation Dashboard
```

但：

```text
刚扣完 Credits
立刻检查 Credits
```

通常不能盲目读延迟 Replica。

类似地：

```text
用户刚修改 Knowledge Base 权限
```

如果授权检查读到旧 Replica，可能产生安全风险。

所以：

> **Consistency Requirement 是路由的一部分。**

---

# 16. 面试怎么答

## Q：MySQL 主从复制怎么工作？

🎯 推荐回答：

> Source 把已提交的数据变化写入 Binary Log，Replica 获取这些 Binlog Event 并在本地重放，从而维护数据副本。复制常见是异步的，因此 Source 写成功后 Replica 可能暂时没有 Apply，产生 Replication Lag。读写分离必须根据业务一致性要求决定哪些读能走 Replica，刚写后读、权限或余额等强一致场景通常要读 Source 或等待 Replica 追上。

## Q：Replication 能不能当 Backup？

> 不能。误删和错误写入也会被复制到 Replica。Backup、PITR、Delayed Replica 与 Replication 解决的是不同问题。

---

# 17. 高频易错点

⚠️ **有 Replica 就一定高可用。**  
还需要 Failover、Fencing 和 Routing。

⚠️ **Replica 收到 Binlog 就等于查询已经能看到。**  
收到、持久化、Apply 是不同阶段。

⚠️ **所有 SELECT 都能读 Replica。**  
要看 Read-after-write / Freshness 要求。

⚠️ **Replication = Backup。**  
错误。

⚠️ **Semi-sync = 强同步多副本。**  
过度简化。

---

# 18. 本章自测

<details>
<summary>1. 为什么异步复制会破坏 Read-after-write？</summary>

Source 已经提交并返回客户端，但 Replica 可能还没收到或 Apply 对应事件；如果后续读被路由到 Replica，就可能看到旧状态。

</details>

<details>
<summary>2. 哪些查询更适合读 Source？</summary>

刚写后的强一致读取、余额/额度、权限、锁定读或其它必须看到最新状态的关键路径通常更适合读 Source，或采用能够保证 Replica 已追上的机制。

</details>

<details>
<summary>3. 为什么 Failover 需要 Fencing？</summary>

因为旧 Source 可能只是网络隔离而没有真正停止。如果新 Replica 被提升后旧 Source 仍接受写，会形成双主分叉，需要确保旧写节点失去写权限或被隔离。

</details>

---

## 继续学习

Replication 主要解决：

```text
读扩展 + 副本 + 容灾基础
```

如果真正的问题是：

```text
单个 Source 的写入容量 / 单表规模也不够了
```

下一步才轮到：**Sharding。**

---

## 官方参考

- MySQL 8.4 Replication：<https://dev.mysql.com/doc/refman/8.4/en/replication.html>
- Binary Log Replication Overview：<https://dev.mysql.com/doc/refman/8.4/en/binlog-replication-configuration-overview.html>
- Semisynchronous Replication：<https://dev.mysql.com/doc/refman/8.4/en/replication-semisync.html>
