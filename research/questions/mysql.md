# MySQL Canonical Questions — S001–S279 全库纵向扫描 v3

更新日期：2026-09-10

> 一级板块：**MySQL**。本文件只保留 MySQL / InnoDB 自身的 SQL、索引、事务、日志、复制与 Sharding 问题。跨存储的 `MySQL + Redis` 数据分层与 Cache Consistency 已迁移到 `AI Backend Engineering`，端到端业务场景归 `System Design`。
>
> 本文件所有 ACTIVE 条目的 `Primary Module = MySQL`；`Source Count` 只按冻结 HUMAN-A `S001–S279` 的独立招聘流程计算。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**26**
- MOVED：**2**（旧 `MYSQL-001`, `MYSQL-023`）
- 证据范围：仅 `S001–S279`
- 当前版本：`v3`（Global Merge / Split Audit）

### 高频信号

- `MYSQL-012` · 14：事务隔离级别与 Dirty / Non-repeatable / Phantom Read
- `MYSQL-004` · 13：为什么 InnoDB 索引使用 B+Tree
- `MYSQL-003` · 11：Slow SQL / EXPLAIN / 执行计划
- `MYSQL-007` · 11：索引失效与 Optimizer 不选索引
- `MYSQL-006` · 10：联合索引 / 最左匹配 / Range
- `MYSQL-021` · 10：分库分表 / Sharding Key / 跨分片查询
- `MYSQL-013` · 9：MVCC / undo / ReadView
- `MYSQL-008` · 8：回表 / 覆盖索引 / ICP

---

## 2. ACTIVE Canonical Questions

### MYSQL-002 · 一条 SQL 从进入 MySQL 到返回结果，解析、优化、执行大致经历什么过程？Optimizer 在做什么？
- **Topic**：SQL Execution
- **Question Type**：Concept / Why
- **Depth**：L2
- **Source Count**：**2**
- **Evidence Sources**：`S119`, `S191`

### MYSQL-003 · 线上出现 Slow SQL 时，怎样用 EXPLAIN、索引命中与执行计划系统定位并优化？
- **Topic**：Slow SQL / EXPLAIN
- **Question Type**：Troubleshoot
- **Depth**：L3
- **Source Count**：**11**
- **Evidence Sources**：`S005`, `S011`, `S063`, `S111`, `S173`, `S183`, `S191`, `S232`, `S256`, `S273`, `S274`

### MYSQL-004 · MySQL / InnoDB 索引为什么通常使用 B+Tree？相比 B-Tree、红黑树或 Hash 有什么优势？
- **Topic**：B+Tree
- **Question Type**：Why / Comparison
- **Depth**：L2
- **Source Count**：**13**
- **Evidence Sources**：`S004`, `S005`, `S013`, `S112`, `S133`, `S154`, `S172`, `S175`, `S191`, `S224`, `S234`, `S258`, `S273`

### MYSQL-005 · 聚簇索引与二级索引有什么区别？InnoDB 中数据和索引怎样组织？
- **Topic**：Clustered / Secondary Index
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**3**
- **Evidence Sources**：`S112`, `S240`, `S273`

### MYSQL-006 · 联合索引如何工作？最左匹配、范围条件与列顺序怎样影响索引利用？
- **Topic**：Composite Index
- **Question Type**：Concept / Scenario
- **Depth**：L3
- **Source Count**：**10**
- **Evidence Sources**：`S010`, `S013`, `S025`, `S069`, `S154`, `S175`, `S199`, `S214`, `S258`, `S273`

### MYSQL-007 · 哪些写法会导致索引失效或 Optimizer 不使用索引？怎样区分真正失效与成本选择？
- **Topic**：Index Invalidation
- **Question Type**：Troubleshoot / Why
- **Depth**：L3
- **Source Count**：**11**
- **Evidence Sources**：`S005`, `S011`, `S018`, `S081`, `S173`, `S175`, `S187`, `S246`, `S256`, `S273`, `S274`

### MYSQL-008 · 什么是回表、覆盖索引和索引下推？怎样减少随机 I/O 与不必要的数据页访问？
- **Topic**：Covering / Back-to-table / ICP
- **Question Type**：Concept / Optimization
- **Depth**：L3
- **Source Count**：**8**
- **Evidence Sources**：`S005`, `S010`, `S025`, `S070`, `S175`, `S214`, `S234`, `S273`

### MYSQL-009 · 为什么 InnoDB 主键常推荐短、单调递增？UUID / 随机主键怎样影响 Page Split、局部性与写入性能？
- **Topic**：Primary Key Design
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Source Count**：**3**
- **Evidence Sources**：`S175`, `S247`, `S274`

### MYSQL-010 · 单表或单分片内的 Deep Pagination 为什么随着 Offset 增大而变慢？怎样用覆盖索引、Seek / Keyset Pagination 等方法优化？
- **Topic**：Deep Pagination
- **Question Type**：Troubleshoot / Optimization
- **Depth**：L3
- **Source Count**：**4**
- **Evidence Sources**：`S010`, `S025`, `S131`, `S148`
- **Related Modules**：System Design

### MYSQL-011 · 事务的 ACID 分别是什么？MySQL 通过哪些机制实现原子性、隔离性和持久性？
- **Topic**：ACID
- **Question Type**：Concept / Why
- **Depth**：L2
- **Source Count**：**4**
- **Evidence Sources**：`S154`, `S188`, `S201`, `S234`

### MYSQL-012 · 四种事务隔离级别怎样比较？Dirty Read、Non-repeatable Read、Phantom Read 如何产生和治理？
- **Topic**：Isolation Levels
- **Question Type**：Concept / Scenario
- **Depth**：L3
- **Source Count**：**14**
- **Evidence Sources**：`S010`, `S069`, `S090`, `S124`, `S134`, `S154`, `S173`, `S188`, `S191`, `S199`, `S201`, `S234`, `S240`, `S273`

### MYSQL-013 · MVCC 如何工作？隐藏列、undo log、ReadView 与可见性判断怎样协作？
- **Topic**：MVCC / ReadView
- **Question Type**：Concept / Deep Dive
- **Depth**：L2
- **Source Count**：**9**
- **Evidence Sources**：`S010`, `S069`, `S148`, `S174`, `S188`, `S191`, `S201`, `S240`, `S273`

### MYSQL-014 · RR 下幻读如何处理？MVCC、Record Lock、Gap Lock、Next-Key Lock 的边界是什么？
- **Topic**：Phantom Read / Locks
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Source Count**：**6**
- **Evidence Sources**：`S069`, `S148`, `S191`, `S201`, `S240`, `S273`

### MYSQL-015 · MySQL Deadlock 怎样产生、检测、定位和避免？
- **Topic**：Deadlock
- **Question Type**：Troubleshoot
- **Depth**：L3
- **Source Count**：**1**
- **Evidence Sources**：`S191`

### MYSQL-016 · redo log、undo log、binlog 分别解决什么问题？在事务、恢复与复制中怎样配合？
- **Topic**：Logs
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**5**
- **Evidence Sources**：`S020`, `S090`, `S173`, `S192`, `S240`

### MYSQL-017 · 为什么需要 redo log 与 binlog 的两阶段提交？它解决什么一致性问题？
- **Topic**：Two-phase Commit
- **Question Type**：Why / Deep Dive
- **Depth**：L2
- **Source Count**：**1**
- **Evidence Sources**：`S192`

### MYSQL-018 · MySQL 主从复制怎样工作？读请求走 Replica 时如何处理复制延迟与一致性？
- **Topic**：Replication
- **Question Type**：Concept / System Design
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S090`, `S134`, `S246`

### MYSQL-019 · 两个并发事务同时读写同一行时，不同隔离级别和锁下 SELECT / UPDATE / INSERT 会发生什么？
- **Topic**：Concurrent Transactions
- **Question Type**：Scenario / Deep Dive
- **Depth**：L4
- **Source Count**：**1**
- **Evidence Sources**：`S195`

### MYSQL-020 · 订单、评论、点赞、买卖双方账单等业务表怎样建模？如何处理热点字段、状态流转与查询模式？
- **Topic**：Schema Design
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**5**
- **Evidence Sources**：`S091`, `S093`, `S147`, `S189`, `S253`

### MYSQL-021 · 什么时候需要分库分表？Sharding Key 怎样选，如何处理数据倾斜、扩容、跨分片查询与分页？
- **Topic**：Sharding
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**10**
- **Evidence Sources**：`S005`, `S093`, `S111`, `S127`, `S138`, `S147`, `S154`, `S189`, `S253`, `S273`

### MYSQL-022 · 大批量写入 MySQL 时，怎样控制 Batch Size、Transaction Size、Index / Log 开销与写入吞吐？
- **Topic**：Bulk Write / MySQL Write Path
- **Question Type**：Optimization / Troubleshoot
- **Depth**：L3
- **Source Count**：**1**
- **Evidence Sources**：`S191`
- **Related Modules**：AI Backend Engineering, System Design

### MYSQL-024 · 能否使用 MySQL 实现分布式锁？与 Redis / ZooKeeper 等方案相比边界在哪里？
- **Topic**：DB Lock as Distributed Lock
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Source Count**：**1**
- **Evidence Sources**：`S191`
- **Related Modules**：Redis, AI Backend Engineering

### MYSQL-025 · MySQL / ORM 如何防止 SQL Injection？参数化查询、预编译与动态 SQL 有什么注意点？
- **Topic**：SQL Injection
- **Question Type**：Security
- **Depth**：L3
- **Source Count**：**3**
- **Evidence Sources**：`S070`, `S232`, `S254`
- **Related Modules**：AI Backend Engineering

### MYSQL-026 · InnoDB 与其它 Storage Engine 的核心差异是什么？为什么业务表通常仍以 InnoDB 为主？
- **Topic**：Storage Engine / InnoDB
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**2**
- **Evidence Sources**：`S069`, `S240`

### MYSQL-027 · 如何利用 binlog / Canal / CDC 做数据同步、索引更新或下游事件消费？怎样处理顺序、重复与恢复？
- **Topic**：CDC / Data Sync
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**4**
- **Evidence Sources**：`S127`, `S170`, `S244`, `S246`
- **Related Modules**：AI Backend Engineering

### MYSQL-028 · 数据量增长后索引效果下降或写入成本上升，怎样从基数、Page Split、表规模和访问模式重新评估索引？
- **Topic**：Index Lifecycle / Scale
- **Question Type**：Troubleshoot / Trade-off
- **Depth**：L3
- **Source Count**：**3**
- **Evidence Sources**：`S175`, `S247`, `S274`

---

## 3. MOVED：十板块归属修正

这些旧 QID 保留映射以避免引用失效，但不再计入 MySQL ACTIVE 数量。

| Legacy QID | 原问题 | 新 Primary Canonical |
|---|---|---|
| `MYSQL-001` | MySQL 与 Redis 的数据分层 | `AIBE-039`（AI Backend Engineering） |
| `MYSQL-023` | MySQL + Redis Cache Consistency | `AIBE-020`（AI Backend Engineering） |

---

## 4. Global Merge / Split Audit 修正

- `MYSQL-010` 不再把“单表 Offset 深分页”和“分库分表后的跨 Shard 分页 / 全局排序”揉成一题。`S093`, `S147` 的跨分片问题继续由 `MYSQL-021` 承接；`MYSQL-010` 只保留单表 / 单分片访问路径，并补入明确讨论 `ORDER BY + Deep Pagination` 的 `S148`。
- `MYSQL-022` 不再吸收通用“批处理 / 数据迁移 / 断点恢复”场景。`S094`, `S207`, `S232`, `S244` 的端到端批处理能力由 `SD-007` 承接；MySQL 本模块只保留 `S191` 中“一亿条数据怎样快速写入 MySQL”的存储引擎 / 写入路径问题。

`SD-001` 等 System Design 场景可以引用 MySQL 机制，但不会把场景题复制回本模块。
