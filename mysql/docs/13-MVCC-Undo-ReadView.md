# 13. MVCC、Undo 与 ReadView

上一章讲了隔离级别，这一章回答一个更底层的问题：

> **InnoDB 为什么能让大量普通 SELECT 在不加行锁的情况下，仍然看到“自己应该看到的版本”？**

核心答案就是 MVCC。

但不要把 MVCC 背成：

> “多版本并发控制，通过版本号提高并发。”

这一章要真正建立：

```text
当前行
  ↓
隐藏事务信息
  ↓
Undo 历史版本
  ↓
ReadView
  ↓
可见性判断
```

---

## 1. 先讲人话：同一行可以有“历史版本”

假设：

```text
agent_runs.id = 1
status = RUNNING
```

Transaction B 修改：

```sql
UPDATE agent_runs
SET status='SUCCESS'
WHERE id=1;
```

如果 Transaction A 仍然需要按照自己的 Snapshot 看旧状态，就不能只保留：

```text
SUCCESS
```

还需要能够找到之前的：

```text
RUNNING
```

因此 InnoDB 不只是“覆盖掉旧值然后彻底忘掉”。

它会利用 Undo 信息保留恢复旧版本所需要的数据。

---

# 2. MVCC 是什么

MVCC = Multi-Version Concurrency Control。

直观目标：

> **让读取者在很多场景下通过读取合适的数据版本获得一致性视图，而不必和写事务互相阻塞。**

例如：

```text
Reader A 需要旧 Snapshot
Writer B 正在更新新版本
```

如果所有普通读取都必须：

```text
等 Writer 提交
```

读写并发会很差。

MVCC 让它变成：

```text
Writer 修改当前版本
Reader 根据自己的 ReadView 找历史可见版本
```

---

# 3. MVCC 不等于“没有锁”

这是第一大误区。

MVCC 主要解释：

```text
普通 Consistent Read
```

怎样读取版本。

但：

```sql
SELECT ... FOR UPDATE;
UPDATE ...;
DELETE ...;
INSERT ...;
```

仍然涉及锁。

所以：

```text
MVCC
≠
InnoDB 不需要 Lock
```

更准确的理解是：

> InnoDB 把多版本读取和传统锁机制结合起来。

---

# 4. Undo Log 为什么是 MVCC 的基础之一

Undo Log 不只服务：

```text
ROLLBACK
```

它还承担：

> **为一致性读取提供旧版本信息。**

例如当前值：

```text
status = SUCCESS
```

Undo 链可以让 InnoDB 逐步回到：

```text
SUCCESS
  ↓ previous version
RUNNING
  ↓ previous version
PENDING
```

这可以理解为一条历史版本链。

⚠️ 注意：

这里是为了建立正确概念模型，不要把它理解成“每次 UPDATE 都复制出一整行完整历史对象放在链表里”。真实 Undo Record 的物理结构更复杂。

---

# 5. 一行记录为什么知道“是谁改的”

InnoDB 聚簇记录内部还维护与事务 / Undo 有关的隐藏信息。

面试层面最重要的是理解：

```text
当前记录
├─ 当前业务列
├─ 修改它的事务信息
└─ 指向历史 Undo 版本的线索
```

于是读取时可以回答：

```text
这个版本是谁创建的？
对当前 ReadView 可见吗？
不可见的话，要不要沿 Undo 找更老版本？
```

---

# 6. ReadView 到底解决什么

历史版本可能很多。

问题是：

> **当前 Transaction 应该看哪一个？**

ReadView 可以理解成：

```text
“我创建这个一致性视图时，哪些事务还没结束？”
```

根据：

- 当前版本由哪个 Transaction 创建；
- 创建 ReadView 时活跃事务的范围；
- 当前事务自身身份；

InnoDB 可以判断某个版本：

```text
Visible
or
Invisible
```

如果不可见：

```text
沿 Undo Version Chain
→ 找更老版本
→ 再判断
```

---

# 7. 不需要死背四个变量，也要会解释规则

很多面试资料会让你死背：

```text
m_ids
min_trx_id
max_trx_id
creator_trx_id
```

这些概念可以帮助理解，但真正重要的是可见性直觉：

### 情况 1：是我自己事务写的

通常应该能看到自己的修改。

### 情况 2：在我的 Snapshot 建立前已经提交

通常可见。

### 情况 3：Snapshot 建立时事务还活着

它的修改不应该直接成为我的已提交快照的一部分。

### 情况 4：Snapshot 建立以后才启动的新事务

显然不属于这个旧 Snapshot。

只要这个逻辑建立起来，ReadView 就不再是四个变量口诀。

---

# 8. RR 与 RC 为什么行为不同

现在回到上一章。

## REPEATABLE READ

同一个事务中的普通 Consistent Read 通常复用同一个一致性视图。

于是：

```text
第一次看 RUNNING
B 提交 SUCCESS
第二次仍按旧 ReadView
→ RUNNING
```

## READ COMMITTED

每次 Consistent Read 可以重新建立新的 ReadView。

于是：

```text
第一次 RUNNING
B COMMIT SUCCESS
第二次建立新 ReadView
→ SUCCESS
```

所以 RC / RR 的差异现在不需要死背，它自然从 ReadView 生命周期推导出来。

---

# 9. MVCC 为什么能提高读写并发

如果没有 MVCC，想保证一致读取可能更依赖：

```text
Reader 加锁
Writer 等 Reader
Reader 等 Writer
```

MVCC 允许很多普通读取：

```text
读取历史可见版本
```

而不是去阻塞 Writer。

这使：

```text
Reader ↔ Writer
```

冲突减少。

但：

```text
Writer ↔ Writer
```

仍然通常需要锁协调。

这也是为什么：

> MVCC 主要解决读写并发，不是把所有并发冲突都消灭。

---

# 10. 一个完整例子

初始：

```text
status = PENDING
```

Transaction A：

```sql
START TRANSACTION;
SELECT status FROM agent_runs WHERE id=1;
-- PENDING
```

Transaction B：

```sql
UPDATE agent_runs
SET status='RUNNING'
WHERE id=1;
COMMIT;
```

现在数据库最新状态已经是：

```text
RUNNING
```

但 A 在 RR 下再次普通读取：

```sql
SELECT status FROM agent_runs WHERE id=1;
```

可能仍返回：

```text
PENDING
```

抽象过程：

```text
读到当前版本 RUNNING
      ↓
检查创建该版本的事务
      ↓
对 A 的 ReadView 不可见
      ↓
沿 Undo 找旧版本
      ↓
PENDING 对 A 可见
      ↓
返回 PENDING
```

这就是 MVCC 真正在做的事情。

---

# 11. 为什么长事务会让 Undo 压力变大

历史版本不能无限立刻删除。

如果仍有一个老事务需要：

```text
很久以前的 Snapshot
```

那么相关历史版本就不能随便清掉。

于是：

```text
Long-running Transaction
      ↓
Old ReadView 长期存在
      ↓
旧 Undo 版本需要保留
      ↓
Purge 不能及时清理
      ↓
History 增长
```

这就是为什么长事务不仅是“占一个 Connection 久一点”。

它还可能影响整个 MVCC 历史版本清理。

---

# 12. Purge 在做什么

当旧版本已经没有任何活跃 ReadView 需要时，后台 Purge 可以逐步清理对应历史信息。

所以你可以把生命周期理解成：

```text
UPDATE
  ↓
产生 Undo / Historical Version
  ↓
可能被旧 Snapshot 使用
  ↓
所有相关旧 Snapshot 消失
  ↓
Purge 最终清理
```

这也是生产中排查“Undo / History 越来越大”时要想到 Long Transaction 的原因。

---

# 13. MVCC 能避免 Lost Update 吗？

不能简单说：

> “有 MVCC 就不会 Lost Update。”

例如：

```text
A 读 credits=100
B 读 credits=100
A 应用层算出 50
B 应用层算出 70
A UPDATE credits=50
B UPDATE credits=70
```

最终某个修改可能覆盖另一个逻辑计算。

解决这类业务并发问题，常见方法是：

```text
原子条件 UPDATE
SELECT ... FOR UPDATE
Optimistic Lock / version column
业务 Idempotency
```

MVCC 解决的是版本可见性，不等于所有业务并发控制。

---

# 14. Snapshot Read 与 Current / Locking Read

面试里经常会问：

> 为什么普通 SELECT 和 UPDATE 看起来看到的数据不一样？

原因之一就是它们读取语义不同。

普通一致性读：

```text
根据 ReadView 读合适历史版本
```

锁定读 / DML：

```text
需要对当前可操作版本加锁并执行修改
```

因此在 RR 事务中混用：

```text
普通 SELECT
+
FOR UPDATE / UPDATE
```

时，要意识到它们观察世界的方式并不完全相同。

---

# 15. AI Application 场景：Conversation Snapshot

假设后台生成一份会话报告：

```text
BEGIN
读取 Conversation
读取 Messages
计算 Usage
生成 Report
COMMIT
```

如果整个过程希望看到一个相对一致的数据库 Snapshot，MVCC 提供了很重要的基础。

但如果中间还要：

```text
修改某些 Message 状态
Claim Agent Task
扣减 Credits
```

那就不能只靠 Snapshot Read，需要进一步考虑 Lock / Conditional Update。

所以：

```text
只读一致性
→ MVCC

并发抢占 / 修改正确性
→ Lock / Atomic SQL / Version
```

边界必须清楚。

---

# 16. 面试怎么答

## Q：MVCC 是什么？

🎯 推荐回答：

> MVCC 是 InnoDB 的多版本并发控制机制。更新记录时会留下能够恢复历史版本的 Undo 信息；普通一致性读会基于 ReadView 判断当前版本是否可见，如果不可见就沿 Undo 版本链查找更老的可见版本。这样很多普通读不需要与写事务互相加行锁，提高读写并发。RC 和 RR 的一个关键区别就是 ReadView 的生命周期不同。

## Q：Undo Log 只用于 Rollback 吗？

> 不是。Undo 一方面支持事务回滚，另一方面也为 MVCC 一致性读提供历史版本。旧版本在仍被 ReadView 需要时不能立刻清理，所以长事务可能造成 Undo / History 保留时间过长。

## Q：MVCC 为什么不能替代锁？

> MVCC 主要解决版本可见性和普通一致性读的读写并发；Writer 与 Writer 冲突、锁定读、范围更新、业务 Claim 等场景仍然需要 Lock 或其它并发控制。

---

# 17. 高频易错点

⚠️ **Undo 只负责 ROLLBACK。**  
还支撑 MVCC 历史版本。

⚠️ **MVCC 就是给每行存很多完整副本。**  
这是过度简化。

⚠️ **有 MVCC 就不需要锁。**  
错误。

⚠️ **ReadView 就是事务开始时间。**  
不是这么简单，要理解一致性读创建 / 使用 Snapshot 的语义。

⚠️ **MVCC 能自动解决 Lost Update。**  
不成立，仍需正确的写并发控制。

---

# 18. 本章自测

<details>
<summary>1. Undo Log 为什么和 MVCC 有关系？</summary>

因为一致性读可能需要访问当前记录之前的历史版本，而 Undo 记录提供了构造旧版本所需的信息；如果当前版本对 ReadView 不可见，InnoDB 可以沿历史版本找到可见版本。

</details>

<details>
<summary>2. RC 与 RR 的 MVCC 差异怎样用 ReadView 解释？</summary>

RC 的普通一致性读取可以每次建立新的 ReadView，因此更容易看到后来已提交的数据；RR 同一事务中的普通一致性读通常复用同一快照，因此重复读取保持一致。

</details>

<details>
<summary>3. 为什么长事务会影响 Purge？</summary>

因为老事务持有较老的 ReadView，历史 Undo 版本可能仍对它可见，Purge 不能提前清理这些版本，导致历史链和 Undo 空间保留更久。

</details>

<details>
<summary>4. MVCC 和锁分别主要解决什么？</summary>

MVCC 主要解决普通一致性读的版本可见性和读写并发；锁用于协调需要保护当前数据的并发读写、Writer-Writer 冲突以及范围插入等问题。

</details>

---

## 继续学习

下一章：**Record Lock、Gap Lock、Next-Key Lock 与 Deadlock**。

前一章回答“我应该看哪个版本”，下一章回答：

> **当我要修改当前世界时，谁必须等谁？**

---

## 官方参考

- MySQL 8.4 · InnoDB Multi-Versioning：<https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html>
- MySQL 8.4 · Undo Logs：<https://dev.mysql.com/doc/refman/8.4/en/innodb-undo-logs.html>
- MySQL 8.4 · Consistent Nonlocking Reads：<https://dev.mysql.com/doc/refman/8.4/en/innodb-consistent-read.html>
