# 11. ACID 与事务

很多面试题把 ACID 当成四个英文单词默写：

```text
Atomicity
Consistency
Isolation
Durability
```

如果只背到这里，后面 MVCC、Lock、redo / undo 全都会变成孤立名词。

这一章要建立的是：

> **事务为什么存在，以及 InnoDB 用哪些机制分别支撑“要么全成、并发互不乱、提交后不丢”。**

---

## 1. 先讲人话：事务是在保护“一个业务动作的边界”

假设 Agent 平台有 Credits：

```text
用户启动一次 Agent Run
  ↓
扣减 100 credits
  ↓
创建 agent_runs 记录
```

如果只执行成功一半：

```text
Credits 已扣
但 Run 没创建
```

业务状态就坏了。

我们希望：

```text
两步都成功
OR
两步都失败
```

这就是 Transaction Boundary 最直观的价值。

---

# 2. 最小事务语法

```sql
START TRANSACTION;

UPDATE accounts
SET credits = credits - 100
WHERE user_id = 10001;

INSERT INTO agent_runs(user_id, status)
VALUES (10001, 'PENDING');

COMMIT;
```

如果中间发现错误：

```sql
ROLLBACK;
```

💡 **新手理解**：

事务不是“让 SQL 更安全”的魔法开关，而是：

> **明确一组数据库操作应该作为一个逻辑单元提交或回滚。**

---

# 3. Autocommit 是什么

MySQL 默认常见行为是 `autocommit=1`。

意味着：

```sql
UPDATE ...;
```

如果没有显式放进更大的事务，通常这个语句本身就是一个事务边界。

可以查看：

```sql
SELECT @@autocommit;
```

显式：

```sql
START TRANSACTION;
```

以后，多条语句才进入同一个事务上下文，直到：

```sql
COMMIT;
```

或：

```sql
ROLLBACK;
```

⚠️ **面试易错点**：

不要以为“不开 START TRANSACTION 就没有事务”。Autocommit 下每条 DML 仍然有事务语义。

---

# 4. Atomicity：原子性

Atomicity 回答：

> **一个事务内部的修改，要么整体提交，要么失败后能回滚。**

例如：

```text
扣 Credits
+
创建 Run
```

不能长期停在半成功状态。

InnoDB 支撑 Atomicity 的关键包括：

- Transaction Boundary；
- `COMMIT / ROLLBACK`；
- Undo 信息用于回滚修改。

⚠️ 不要说：

> “Atomicity 就是 redo log 保证的。”

更常见的理解：

- Undo 支持撤销未提交修改；
- Redo 更直接服务 Crash Recovery / Durability；
- 真正事务实现是多个机制协作。

---

# 5. Consistency：一致性到底是什么

这是 ACID 里最容易被说空的一项。

常见回答：

> “事务前后数据库保持一致。”

问题是：什么叫“一致”？

## 5.1 数据库内部约束

例如：

```text
Primary Key 唯一
Foreign Key 合法
NOT NULL 满足
数据格式满足约束
```

## 5.2 业务不变量

例如：

```text
credits >= 0
库存不能超卖
订单状态不能从 CANCELLED 跳回 PAID
```

数据库不会自动理解所有业务规则。

如果你写：

```sql
UPDATE accounts
SET credits = -999999;
```

Schema 没有限制时，MySQL 并不知道这个业务值“荒谬”。

所以更准确地说：

> **Consistency 是最终目标；Atomicity、Isolation、Durability，加上 Schema Constraint 与正确应用逻辑，共同帮助系统维持定义好的数据不变量。**

🎯 这是比“C 就是数据库不会错”成熟很多的回答。

---

# 6. Isolation：隔离性

Isolation 回答：

> **多个事务并发运行时，一个事务能看到另一个事务什么状态，彼此的读写如何互相影响。**

例如：

```text
Transaction A                    Transaction B
-------------                    -------------
读取 credits=100
                                 扣减 80
                                 COMMIT
再次读取 credits=?
```

A 第二次读到：

```text
100？
20？
```

取决于：

- Isolation Level；
- 是普通 Consistent Read 还是 Locking Read；
- Transaction Snapshot；
- Lock。

这就是后面两章的主角。

---

# 7. Durability：持久性

Durability 回答：

> **事务一旦向客户端确认提交成功，系统应该能够在崩溃等情况下恢复出已提交结果。**

这不等于：

> “每个 Row 修改都在 COMMIT 前直接随机写进最终 Data Page。”

InnoDB 会利用 Redo Log / WAL 思想：

```text
修改内存中的 Page
+
记录足够的 Redo
→ COMMIT durability boundary
→ 后台再逐步 Flush Dirty Page
```

崩溃后：

```text
Data Page 还没完全落盘
但 Redo 已持久化
→ Crash Recovery 重放必要修改
```

这让随机数据页写入不必全部阻塞在每次事务提交路径上。

---

# 8. ACID 与 InnoDB 机制怎样对应

先建立粗略映射：

| ACID | 主要相关机制 |
|---|---|
| Atomicity | Transaction、Undo、Rollback |
| Consistency | A/I/D + Constraint + 正确业务逻辑 + Recovery |
| Isolation | Isolation Level、MVCC、Lock |
| Durability | Redo Log、Flush Policy、Doublewrite / Crash Recovery 等 |

⚠️ 这不是“一对一实现表”。

例如 Undo 既服务 Rollback，也服务 MVCC Historical Version；Lock 既影响 Isolation，也影响业务并发正确性。

---

# 9. Transaction 越大越好吗

不是。

一个超大 Transaction：

```text
UPDATE 5000 万行
→ 长时间持锁
→ Undo 增长
→ History List / Purge 压力
→ Replica Apply 压力
→ Rollback 很重
→ 其它请求等待
```

所以 Transaction Size 是工程设计的一部分。

例如批量 Ingestion：

```text
一次 5000 万行一个事务
```

通常比：

```text
合理 Batch 分批提交
+
Checkpoint / Idempotency
```

风险更高。

这会在 Bulk Write 章节继续讲。

---

# 10. Transaction 越小越好吗

也不是。

如果每插一行都：

```text
BEGIN
INSERT 1 row
COMMIT
```

可能产生非常高的 Commit / Log Sync 开销。

所以要权衡：

```text
Atomicity Boundary
vs
Lock Duration
vs
Log / Commit Overhead
vs
Failure Recovery Granularity
```

---

# 11. 本地事务不能解决哪些问题

这点对 AI Backend 特别重要。

假设：

```text
MySQL Transaction
  ↓
扣款成功
  ↓
调用外部 Payment API
  ↓
发送 MQ
  ↓
写 Redis
```

一个本地 InnoDB Transaction 不能自动把这些外部系统都纳入同一个原子提交。

因此：

```text
MySQL ACID
≠
Distributed Transaction 自动完成
≠
MySQL + Redis 自动一致
≠
Tool Side Effect 自动 exactly-once
```

跨系统会进入：

- Idempotency；
- Outbox；
- MQ；
- Compensation；
- Retry；
- Saga / Distributed Transaction 等。

这些 Primary 在 AI Backend Engineering / System Design。

---

# 12. 一个并发扣减例子

错误代码思路：

```text
SELECT credits
如果 >= 100
UPDATE credits = credits - 100
```

如果两个请求同时：

```text
A 读 100
B 读 100
A 判断够
B 判断够
A 扣 100
B 也扣 100
```

如果处理不当，就可能违反业务不变量。

一种更原子的 SQL 思路：

```sql
UPDATE accounts
SET credits = credits - 100
WHERE user_id = 10001
  AND credits >= 100;
```

然后检查 affected rows。

这比：

```text
先读
→ 应用层判断
→ 再写
```

减少了 Race Window。

💡 **重要**：

事务存在，不代表应用层随便写“read-modify-write”就自然并发安全。

---

# 13. 为什么长事务危险

长事务常带来：

```text
Lock 持有更久
Undo 版本保留更久
Purge 无法及时清理历史版本
Replica / Log 压力
Connection 占用
故障回滚成本高
```

所以生产中需要观察：

- Long-running Transaction；
- Transaction Age；
- Lock Wait；
- Undo / Purge；
- Rows Modified。

这是“事务”从八股到 Production 的第一步。

---

# 14. 面试怎么答

## Q：ACID 分别是什么？MySQL 怎么实现？

🎯 **建议回答**：

> Atomicity 是事务内修改整体提交或回滚，InnoDB 通过事务机制和 Undo 等支持；Isolation 决定并发事务之间的可见性和读写冲突，主要由隔离级别、MVCC 和 Lock 协作；Durability 表示提交成功后的修改在崩溃后仍可恢复，Redo Log 和 Crash Recovery 是关键机制。Consistency 更像最终目标，它不仅依赖数据库机制，也依赖 Constraint 和应用业务不变量，不应该简单对应某一个日志。

## Q：事务能保证业务绝对正确吗？

> 不能。事务提供原子、隔离和持久等机制，但业务必须正确定义事务边界和并发操作。例如 read-modify-write 如果没有合适 Lock / Conditional Update，仍可能出现 Race；跨 MySQL、Redis、MQ、外部 API 时更不能只靠本地事务。

---

# 15. 高频易错点

⚠️ **Consistency 对应某一个 Log。**  
过度简化。

⚠️ **有 Transaction 就并发安全。**  
错误，仍要看 Isolation、Lock 和 SQL Pattern。

⚠️ **COMMIT 就等于所有 Data Page 已经立即落到最终位置。**  
InnoDB 通过 WAL / Redo 实现更高效的持久性。

⚠️ **Transaction 越大越保证一致性。**  
边界应该服从业务原子性，超大事务会带来明显运行风险。

⚠️ **MySQL ACID 能自动解决 Redis / MQ / External API 一致性。**  
错误。

---

# 16. 本章自测

<details>
<summary>1. Consistency 为什么不能只对应某一个 MySQL 内部机制？</summary>

因为一致性描述的是系统必须满足的数据不变量。Atomicity / Isolation / Durability、Schema Constraint 与应用业务逻辑都参与维持它，数据库无法自动理解所有业务规则。

</details>

<details>
<summary>2. 为什么有事务仍可能发生超扣？</summary>

如果应用使用不安全的 read-modify-write，两次并发事务可能都基于旧状态做决策。需要合适的 Isolation / Lock / Atomic Conditional Update 才能保护具体业务不变量。

</details>

<details>
<summary>3. 为什么超大事务有风险？</summary>

会延长锁持有时间、增加 Undo / Purge 压力、占用连接和日志资源、放大复制与回滚成本。

</details>

---

# 17. 官方资料

- MySQL 8.4 — InnoDB and the ACID Model  
  <https://dev.mysql.com/doc/refman/8.4/en/mysql-acid.html>
- MySQL 8.4 — autocommit, Commit, and Rollback  
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-autocommit-commit-rollback.html>
- MySQL 8.4 — InnoDB Transaction Model  
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-model.html>

下一章进入 MySQL 模块最高频问题：

> **四种 Isolation Level 到底改变了什么？Dirty / Non-repeatable / Phantom Read 怎样理解？**
