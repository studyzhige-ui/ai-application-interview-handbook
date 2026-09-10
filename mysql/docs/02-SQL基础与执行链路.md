# 02. SQL 基础与一条 SQL 的执行链路

这一章不追求把 SQL 语法大全背一遍，而是建立一个之后所有性能分析都会反复使用的模型：

> **一条 SQL 不会“直接去磁盘找数据”。它会先被 MySQL Server 理解、优化成执行计划，再通过 Storage Engine 真正访问数据。**

真实面试中的 `MYSQL-002` 就直接问：

> 一条 SQL 从进入 MySQL 到返回结果，解析、优化、执行大致经历什么过程？Optimizer 在做什么？

---

## 1. 先从最小 SQL 开始

假设有一张表：

```sql
CREATE TABLE agent_runs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    tenant_id BIGINT NOT NULL,
    status VARCHAR(32) NOT NULL,
    model_name VARCHAR(64) NOT NULL,
    created_at DATETIME NOT NULL,
    INDEX idx_tenant_user_created (tenant_id, user_id, created_at)
) ENGINE=InnoDB;
```

查询某个用户最近的 Agent Run：

```sql
SELECT id, status, model_name, created_at
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

初学时容易只看到 SQL 文本。

数据库真正要解决的却是一串决策：

```text
这句话语法对不对？
表和列是否存在？
有哪些 Index 可以用？
走哪个 Index？
要扫描多少 Row？
是否需要排序？
是否需要回表？
先读哪张表？
怎样从 InnoDB 取出数据？
```

---

# 2. 一张总图：SQL 大致怎样执行

先记住这个**简化但正确方向**的模型：

```text
Client
  ↓
Connection / Session
  ↓
Parser
  ↓
Optimizer
  ↓
Execution Plan
  ↓
Executor
  ↓
Storage Engine API
  ↓
InnoDB
  ↓
Buffer Pool / B+Tree / Data Page
  ↓
Rows
  ↓
Server 处理结果
  ↓
Client
```

⚠️ 这不是 MySQL 源码函数调用的逐行还原，而是面试和工程分析需要掌握的职责分层。

---

# 3. 第一步：Connection / Session

客户端先和 MySQL Server 建立连接。

一次连接中会有 Session 级状态，例如：

- 当前 Database；
- Character Set；
- Transaction Isolation；
- `autocommit`；
- Session Variable。

例如：

```sql
SELECT @@transaction_isolation;
SELECT @@autocommit;
```

💡 **新手理解**：

同一条 SQL 在不同 Session 环境下，不一定处于完全相同的事务语义。

这也是为什么排查问题时不能只拿到 SQL 文本，还要关心：

```text
在哪个数据库？
什么隔离级别？
是否在事务里？
参数值是什么？
```

---

# 4. 第二步：Parser——先确认“你在说什么”

SQL 是一种语言。

例如：

```sql
SELECT id
FROM agent_runs
WHERE user_id = 10001;
```

Server 需要先解析它的结构。

你可以把 Parser 先理解成：

```text
SQL Text
  ↓
词法 / 语法分析
  ↓
内部可处理的语法结构
```

如果写：

```sql
SELEC id FROM agent_runs;
```

语法都无法通过，就不会进入正常的查询优化。

但请注意：

> “Parser 做语法分析”只是第一步。真正决定“怎么查”的核心还在 Optimizer。

---

# 5. 第三步：Optimizer——不是看到索引就用索引

这是本章最重要的一点。

假设：

```sql
SELECT *
FROM agent_runs
WHERE status = 'RUNNING';
```

而表上有：

```sql
INDEX idx_status (status)
```

很多初学者会说：

> “WHERE 用到了 status，所以一定走 idx_status。”

不一定。

Optimizer 会比较可行的执行方式，目标是选择它估计成本更低的计划。

它可能考虑：

```text
全表扫描？
走哪个索引？
索引扫描后要不要大量回表？
过滤条件选择性怎么样？
Join 顺序怎么安排？
需不需要额外排序？
统计信息认为大概会命中多少行？
```

官方文档把 Optimizer 选择出来的操作集合称为 **Query Execution Plan**。

### 一个非常重要的表达

```text
“索引失效”
```

在面试中经常被说得过于粗糙。

更准确要区分：

```text
A. 当前条件根本无法利用某个索引做有效 Lookup
B. 当前条件理论上能使用索引
C. 但 Optimizer 根据成本估算选择了别的 Access Path
```

后面第 8 章会专门拆这个区别。

---

# 6. 什么叫 Execution Plan

执行计划可以理解成：

> **Optimizer 给 Executor 制定的“这条 SQL 打算怎么做”的方案。**

比如一个 Join：

```sql
SELECT u.id, r.status
FROM users u
JOIN agent_runs r ON r.user_id = u.id
WHERE u.email = 'a@example.com';
```

数据库要决定：

```text
先找 users？
还是先扫描 agent_runs？
users 用哪个 Index？
找到 user_id 后 agent_runs 怎么查？
每一步预计多少 Rows？
```

这个计划可以通过 `EXPLAIN` 查看。

```sql
EXPLAIN
SELECT ...;
```

后面还会用：

```sql
EXPLAIN ANALYZE
SELECT ...;
```

⚠️ `EXPLAIN` 与 `EXPLAIN ANALYZE` 不要混为一谈。

粗略理解：

- `EXPLAIN`：看 Optimizer 的执行计划信息；
- `EXPLAIN ANALYZE`：实际执行查询，并展示执行过程的测量信息，因此对生产环境使用要更谨慎。

---

# 7. 第四步：Executor——按计划真正执行

Optimizer 决定：

> “我准备这样查。”

Executor 才负责真正驱动执行。

粗略过程可以想象为：

```text
Execution Plan
  ↓
Executor 请求某种 Access
  ↓
通过 Storage Engine 接口访问 InnoDB
  ↓
InnoDB 查 Index / Page / Row
  ↓
返回记录
  ↓
继续 Filter / Join / Aggregate / Sort 等处理
```

这里需要特别建立两个边界：

### Server 层关心

- SQL 语义；
- Optimizer；
- Execution Plan；
- Join 等查询执行逻辑。

### InnoDB 关心

- B+Tree Index；
- Buffer Pool；
- Data Page；
- Transaction；
- MVCC；
- Lock；
- Redo / Undo。

真实执行当然比这张表复杂，但这个职责模型足够支撑后面的面试分析。

---

# 8. InnoDB 读数据，不代表每次都去磁盘

这是一个非常常见的新手误区：

> “数据库查询 = 去磁盘查 B+Tree。”

InnoDB 有 Buffer Pool。

简化理解：

```text
Executor
  ↓
InnoDB 需要某个 Page
  ↓
Buffer Pool 中有？
  ├─ 有 → 内存访问
  └─ 没有 → 从存储加载到 Buffer Pool
```

所以谈查询性能时，不能只说：

> “树高 3 层，所以固定 3 次磁盘 I/O。”

这是过度简化。

真实性能还受到：

- Page 是否已缓存；
- 随机 / 顺序访问；
- 返回行数；
- 回表次数；
- Buffer Pool 命中；
- Storage 性能；
- 并发；
- CPU / Sorting / Join；

等多种因素影响。

⚠️ **面试易错点**：

B+Tree 的高度有助于理解“为什么索引访问层级少”，但不能机械等价成“每层一定一次物理磁盘读取”。

---

# 9. SQL 的四类基本操作先建立框架

## 9.1 `SELECT`

读数据：

```sql
SELECT id, status
FROM agent_runs
WHERE user_id = 10001;
```

后续重点：

- Access Path；
- Index；
- Join；
- Sort；
- Aggregate；
- Locking Read / Consistent Read。

---

## 9.2 `INSERT`

```sql
INSERT INTO agent_runs (
    user_id, tenant_id, status, model_name, created_at
) VALUES (
    10001, 7, 'PENDING', 'gpt', NOW()
);
```

不仅是“加一行”。

后面会涉及：

- Clustered Index 插入；
- Secondary Index 维护；
- Page Split；
- Redo；
- Undo；
- Transaction；
- Constraint。

---

## 9.3 `UPDATE`

```sql
UPDATE agent_runs
SET status = 'RUNNING'
WHERE id = 123;
```

后面会进入：

- 如何定位 Row；
- 当前事务看到哪个版本；
- 锁谁；
- Undo 如何支持旧版本 / Rollback；
- 修改索引列时 Secondary Index 怎样变化。

---

## 9.4 `DELETE`

```sql
DELETE FROM agent_runs
WHERE id = 123;
```

也不要简单理解成“立刻从磁盘抹掉这一行”。

InnoDB 的多版本与 Purge 机制意味着删除背后还有事务可见性与后续清理。

这会在 MVCC 章节重新展开。

---

# 10. WHERE、ORDER BY、LIMIT 为什么会直接影响执行计划

看三个查询。

### Query A

```sql
SELECT *
FROM agent_runs
WHERE tenant_id = 7;
```

### Query B

```sql
SELECT *
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001;
```

### Query C

```sql
SELECT id, status, created_at
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

如果有：

```sql
INDEX idx_tenant_user_created (
    tenant_id,
    user_id,
    created_at
)
```

这三个查询对 Index 的利用方式可能不完全一样。

后面会逐层解释：

```text
联合索引排序规则
→ Leftmost Prefix
→ Range
→ ORDER BY
→ Covering Index
→ LIMIT
```

所以 SQL 优化不是：

> “WHERE 后面的字段都建一个 Index。”

而是：

> **根据真实 Query Pattern 设计 Access Path。**

---

# 11. SELECT * 为什么经常被面试官追问

很多回答只会说：

> “`SELECT *` 网络传输数据多，所以不好。”

这只是一个角度。

还有一个非常重要的索引角度。

假设二级索引已经包含：

```text
tenant_id
user_id
created_at
+ Primary Key
```

查询：

```sql
SELECT id, created_at
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001;
```

有机会只从索引拿到所需列。

但如果：

```sql
SELECT *
```

需要 `model_name`、`status`、`token_cost` 等索引里没有的列，就可能需要额外回到 Clustered Index 获取整行。

这就是后面的：

> **Covering Index vs Back-to-table。**

---

# 12. Query Cache？不要背旧资料

历史 MySQL 面试资料经常出现：

```text
Client
→ Connector
→ Query Cache
→ Parser
→ Optimizer
→ Executor
```

如果你看到这种图，必须先问：

> 这是哪个 MySQL 版本？

现代 MySQL 主线里，不应继续把旧的 Server Query Cache 当成查询执行链的固定环节来背。

⚠️ 这是学习旧八股材料最容易踩的坑之一。

本手册会尽量避免把旧版本历史行为偷偷写成现代 MySQL 事实。

---

# 13. Optimizer 为什么会判断错

Optimizer 不可能提前真正执行所有可能方案再比较。

它要依赖：

- Statistics；
- Cardinality；
- Cost Model；
- Index 情况；
- Predicate；
- Join 信息。

如果统计信息与真实数据分布偏差很大，就可能出现：

```text
Optimizer 估计：只会命中 100 行
实际：命中 500 万行
```

最终导致计划不理想。

所以“为什么没有走我想要的索引”不能只回答：

> “索引失效了。”

还要检查：

```text
能不能用？
估计会返回多少？
选择性怎样？
回表成本多大？
统计信息是否合理？
Optimizer 为什么觉得另一个方案便宜？
```

---

# 14. 一条 Slow SQL 应怎样开始分析

先给一个我们后面会不断完善的最小思路：

```text
1. 明确 SQL + 参数
2. 明确表结构和 Index
3. 看数据量 / 数据分布
4. EXPLAIN / EXPLAIN ANALYZE
5. 看 Access Path
6. 看估计 Rows / 实际 Rows
7. 看 Filter / Join / Sort / Temporary
8. 看是否大量回表
9. 看 Lock / I/O / CPU / Resource
10. 修改后重新测量
```

🎯 这比“给 WHERE 字段加索引”成熟得多。

---

# 15. 面试怎么答

## Q：一条 SQL 从进入 MySQL 到返回，大致经历什么？

🎯 **30 秒版本**：

> 客户端通过连接把 SQL 发给 MySQL Server。Server 先解析 SQL，然后 Optimizer 根据表、索引、统计信息和成本模型选择执行计划。Executor 按计划执行，通过 Storage Engine 接口向 InnoDB 请求数据。InnoDB 再通过 Buffer Pool、B+Tree Index 和数据页完成实际记录访问，并受事务、MVCC、锁等机制约束，最后结果由 Server 返回客户端。

🎯 **继续追问版本**：

> 我会特别区分“有索引”和“Optimizer 最终选择索引”。执行计划是成本选择结果，所以排查没有走索引时，要同时看 Predicate 是否可利用索引、Cardinality / Statistics、预计扫描行数和回表成本，而不是统一叫索引失效。

---

# 16. 高频易错点

⚠️ **错误 1：Optimizer 负责真正读磁盘。**  
Optimizer 负责选择执行计划；实际访问数据由执行层与 Storage Engine 协作完成。

⚠️ **错误 2：有 Index 就一定使用。**  
Optimizer 会做成本选择。

⚠️ **错误 3：B+Tree 三层 = 必然三次物理磁盘 I/O。**  
忽略了 Buffer Pool 和缓存命中。

⚠️ **错误 4：把 MySQL Server 与 InnoDB 混成一层。**

⚠️ **错误 5：继续背已经属于旧版本历史的 Query Cache 固定执行链。**

---

# 17. 自测

<details>
<summary>1. Parser 与 Optimizer 的职责差异是什么？</summary>

Parser 负责理解 SQL 的词法 / 语法结构；Optimizer 面对合法的查询语义，评估可能的访问方式、索引、Join 顺序等，选择估计成本较低的执行计划。

</details>

<details>
<summary>2. 为什么“WHERE 字段有索引”仍然可能不走索引？</summary>

因为“可使用”不代表“成本最低”。如果命中比例高、大量回表、统计信息或成本估算认为全表扫描更便宜，Optimizer 可能选择其它访问路径。也可能因为表达式、类型转换、联合索引前缀等原因根本无法有效使用该索引。

</details>

<details>
<summary>3. 为什么 SQL 性能分析要关心参数，而不是只看 SQL 模板？</summary>

不同参数可能对应完全不同的数据分布和命中规模，从而改变选择性、扫描行数与最佳执行计划。

</details>

<details>
<summary>4. `SELECT *` 除了网络数据更多，还可能影响什么？</summary>

它更容易要求读取索引之外的列，从而失去 Covering Index 的机会并产生回表。也会增加 Row Materialization、网络与序列化成本。

</details>

---

# 18. 官方资料

- MySQL 8.4 — Understanding the Query Execution Plan  
  <https://dev.mysql.com/doc/refman/8.4/en/execution-plan-information.html>
- MySQL 8.4 — Optimizing Queries with EXPLAIN  
  <https://dev.mysql.com/doc/refman/8.4/en/using-explain.html>
- MySQL 8.4 — Optimizing SQL Statements  
  <https://dev.mysql.com/doc/refman/8.4/en/statement-optimization.html>
- MySQL 8.4 — Controlling the Query Optimizer  
  <https://dev.mysql.com/doc/refman/8.4/en/controlling-optimizer.html>

下一章进入整个 MySQL 性能体系的核心入口：

> **Index 到底是什么？它真正减少的成本是什么？**
