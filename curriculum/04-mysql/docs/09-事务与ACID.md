# 09｜事务：哪些修改必须一起成立

[← 读懂执行计划，找到查询真正慢在哪里](08-执行计划与慢查询.md) · [MySQL 目录](../README.md) · [并发读取：隔离级别与 MVCC →](10-隔离级别与MVCC.md)

启动一项付费任务，要从账户扣 30 点额度，并写一条使用流水。扣减成功而流水没写入，账户少了钱却查不到原因；只写流水、不扣额度，也不符合业务规则。

我们需要的不是两条“各自正确”的 SQL，而是**两项修改一起成立，或者一起不成立**。事务就是定义这组修改边界的机制。

## 1. COMMIT 确认整组修改，ROLLBACK 撤销当前整组

用一个账户和一张流水表观察：`accounts` 中账户 1 的 `credits` 初始为 100，`credit_events` 初始为空。完整建表留在[实验数据](../examples/seed.sql)，这里只需要知道余额列和流水的账户、金额对应关系。

<a id="sql-transaction_commit"></a>

<!-- mysql-example: transaction_commit -->
```sql
START TRANSACTION;
UPDATE accounts SET credits = credits - 30 WHERE id = 1;
INSERT INTO credit_events (id, account_id, amount) VALUES (1, 1, -30);
COMMIT;
SELECT credits FROM accounts WHERE id = 1;
SELECT id, amount FROM credit_events ORDER BY id;
```

START TRANSACTION 开始事务；中间两条语句扣减额度、增加流水；COMMIT 确认它们成立。后面的查询检查结果：余额是 70，流水有一条 `(1,-30)`。

**ROLLBACK 撤销的是当前尚未提交的事务，不是把数据库恢复到最初。** 在余额已经为 70 的基础上，再开始一次扣 20 点的操作，最后改为回滚：

<a id="sql-transaction_rollback"></a>

<!-- mysql-example: transaction_rollback -->
```sql
START TRANSACTION;
UPDATE accounts SET credits = credits - 20 WHERE id = 1;
INSERT INTO credit_events (id, account_id, amount) VALUES (2, 1, -20);
ROLLBACK;
SELECT credits FROM accounts WHERE id = 1;
SELECT id, amount FROM credit_events ORDER BY id;
```

结果仍为 70 和原来的一条流水。第二笔修改撤销了，第一笔已提交的历史还在。事务里面可以读到自己的修改，但那不等于其他事务已经可以依赖它。

事务属于一个连接，连接 A 开始的事务不能由连接 B 的 COMMIT 完成。默认自动提交连接在未显式开始事务时，会将成功的数据修改语句独立提交；因此“没写 BEGIN”不等于数据库完全没有事务。[自动提交与回滚](https://dev.mysql.com/doc/refman/9.7/en/innodb-autocommit-commit-rollback.html)。

## 2. ACID 描述四类要求，不是四个万能开关

| 特性 | 要回答的问题 | 扣额度例子 |
|---|---|---|
| 原子性 Atomicity | 哪些修改不能只成立一半 | 额度与流水共同提交或回滚 |
| 一致性 Consistency | 修改前后应保持什么规则 | 不出现负余额或不合法账户关系 |
| 隔离性 Isolation | 同时运行的事务怎样互相影响 | 别人何时看见扣减，两个扣减如何协调 |
| 持久性 Durability | 确认提交后怎样在故障中恢复 | 已确认的账务修改有恢复依据 |

“保持一致”不是保持所有值不变，而是保持预先定义的规则。如果业务禁止负余额，就要把这个要求写进约束和修改逻辑。事务不会因为名叫 ACID，就自动知道 30 点是否足够、操作人是否有权限。

实现上，撤销日志帮助回滚，多版本和锁参与并发协调，重做日志与持久化策略支持恢复。它们相互协作，不是每个字母对应一个独立文件。[InnoDB 的 ACID 说明](https://dev.mysql.com/doc/refman/9.7/en/mysql-acid.html)。

## 3. 修改没报错，为什么还要检查结果

假设余额只剩 70，却要求再扣 100。更安全的操作是把“余额足够”和“扣减”放进同一条更新条件，而不是先查询再在应用里判断：

<a id="sql-conditional_debit"></a>

<!-- mysql-example: conditional_debit -->
```sql
START TRANSACTION;
UPDATE accounts
SET credits = credits - 100
WHERE id = 1 AND credits >= 100;
SELECT ROW_COUNT() AS changed_rows;
ROLLBACK;
```

本例更新行数为 0，因为没有记录同时满足账户编号和额度条件。应用应该结束这次业务操作，**不能接着写一条“扣减成功”的流水**。这说明事务与条件更新各有职责：前者组合修改，后者限制这笔修改能否发生。

一条 SQL 报错，也不等于整个事务总会自动撤销。重复键等错误通常只撤销失败语句；前面成功的语句可能还留在当前事务里。业务必须整体失败时，应明确 ROLLBACK，不能吞掉异常又提交剩下的半组工作。死锁与超时另有不同回滚范围，锁章节会针对这种故障解释。[错误处理规则](https://dev.mysql.com/doc/refman/9.7/en/innodb-error-handling.html)。

> ⚠️ 本例 ROW_COUNT() 紧跟更新；实际驱动还需核对“匹配行数”和“改变行数”的选项。这里成功扣减必然改变余额，避免了值未改变时的歧义。

## 4. 事务边界不要扩大到它管不了的事情

同一个 InnoDB 事务可以保护本地表中的额度和流水，却不能让邮件、Redis 或外部支付接口一起回滚。事务里调用外部服务成功以后，即使数据库回滚，也不会自动撤回已经发出的邮件。

同样，不要在持有事务时等待模型生成或人工确认。长时间占用连接、锁和旧版本会影响其他请求，而远端动作仍不属于数据库原子性保证。合理边界是把必须共同成立的数据库修改包在短事务里，外部执行另有结果确认和恢复方案。

事务也不是越大越好。把整个导入放进一笔事务，会扩大日志、锁和失败回滚成本；每行都独立提交，又会增加固定提交开销。大小应先服从业务必须原子的范围，再结合负载选择。

<details>
<summary>相关概念回看：保存点与存储引擎</summary>

SAVEPOINT 可以在事务内标记局部撤销位置，但不是独立提交的子事务。只有业务允许保留其他部分时才使用。

上述例子使用 InnoDB。MyISAM 不提供同样的事务回滚，MEMORY 的行数据也不提供相同的重启持久性。服务器接受 START TRANSACTION，并不会让任意引擎获得同一套能力。比较引擎时看事务、锁和恢复要求，不先背所有引擎名称。

</details>

---

## 本章小结

事务把必须共同成立的修改放在一起。成功后提交，业务不能继续时回滚；约束、条件更新和应用检查负责具体规则，外部动作则需要另外的确认与恢复边界。

## 🎯 面试怎么回答

### 事务能保证业务一定正确吗？

不能。它提供整组提交、并发隔离与恢复机制，但仍需正确的 SQL、约束和成功判定。额度不足时必须检查条件更新没有成功，不能继续提交流水；外部系统也不自动属于本地事务。

## ⚠️ 易错点

> ⚠️ 一条语句失败不总是整个事务失败，业务收尾必须明确。

> ⚠️ ROLLBACK 不撤销过去已提交事务，也不撤销已经完成的外部动作。

## 本章自测

<details>
<summary>1. 为什么第二次回滚后仍是 70，而不是 100？</summary>

第一次扣 30 已提交。回滚只撤销第二个事务扣 20 和新增流水的修改。

</details>

<details>
<summary>2. 条件扣减返回 0，为什么不能插入成功流水？</summary>

因为扣减没有发生。事务能把语句组合起来，但不会替应用判断这笔业务是否满足条件。

</details>

<details>
<summary>3. 为了防错，能把整个模型调用期间都放进事务吗？</summary>

通常不应如此。它长期占用数据库资源，且模型服务不受本地事务回滚控制。

</details>

## 知识回看与权威资料

- [InnoDB 事务模型](https://dev.mysql.com/doc/refman/9.7/en/innodb-transaction-model.html)：了解事务与连接的关系。
- [存储引擎能力](https://dev.mysql.com/doc/refman/9.7/en/storage-engines.html)：不能把 InnoDB 实验结论套给任意引擎。
- [事务实验](../examples/experiments.md#lab-09)：运行提交、回滚与条件失败三种路径。
