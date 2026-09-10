# MySQL Canonical Questions — S001–S279 全库纵向扫描 v1

更新日期：2026-09-10

> 本文件不是 MySQL 教材目录，也不是网上题库。它只回答：在当前冻结的 279 个 HUMAN-A AI Application / Agent 真人招聘流程中，MySQL 实际被怎样问、问到什么深度。完整教材仍会从 0 建立知识体系。

## 1. 当前扫描结论

- Canonical Questions：**28** 道
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数，同一来源内连续追问不重复计数
- 当前版本：`v1`；五大模块完成后再做跨模块 Merge / Split 审计

### 高频信号

- **MYSQL-023** · 20 个来源 · 🔥🔥🔥：MySQL 与 Redis 双写时如何保证最终一致性？Cache Aside、删除缓存、延迟双删、补偿和故障窗口怎样理解？
- **MYSQL-012** · 14 个来源 · 🔥🔥🔥：四种事务隔离级别如何比较？Dirty Read、Non-repeatable Read、Phantom Read 分别如何产生和治理？
- **MYSQL-004** · 13 个来源 · 🔥🔥🔥：MySQL / InnoDB 索引为什么通常使用 B+Tree？相比 B-Tree、红黑树或 Hash 有什么优势？
- **MYSQL-003** · 11 个来源 · 🔥🔥🔥：线上出现 Slow SQL 时，怎样用 EXPLAIN、索引命中与执行计划系统定位并优化？
- **MYSQL-007** · 11 个来源 · 🔥🔥🔥：哪些写法会导致索引失效或优化器不使用索引？如何判断这是“真失效”还是成本选择？
- **MYSQL-006** · 10 个来源 · 🔥🔥🔥：联合索引如何工作？最左匹配原则、范围条件与列顺序怎样影响索引利用？
- **MYSQL-021** · 10 个来源 · 🔥🔥🔥：什么时候需要分库分表？Sharding Key 怎样选，怎样处理数据倾斜、扩容、跨分片查询和分页？
- **MYSQL-001** · 9 个来源 · 🔥🔥：MySQL 与 Redis 在 AI 应用中分别适合承载什么数据，怎样做数据分层？
- **MYSQL-013** · 9 个来源 · 🔥🔥：MVCC 如何工作？隐藏列、undo log、ReadView 与可见性判断怎样协作？
- **MYSQL-008** · 8 个来源 · 🔥🔥：什么是回表、覆盖索引和索引下推？怎样减少随机 I/O 与不必要的数据页访问？
- **MYSQL-014** · 6 个来源 · 🔥🔥：RR 下幻读如何处理？MVCC、记录锁、Gap Lock、Next-Key Lock 的边界是什么？
- **MYSQL-010** · 5 个来源 · 🔥🔥：深分页为什么会越来越慢？单表、分库分表场景分别怎样优化 Offset / 跳页 / 跨库聚合？

---

## 2. Canonical Questions

### MYSQL-001 · MySQL 与 Redis 在 AI 应用中分别适合承载什么数据，怎样做数据分层？

- **Topic**：Data Layering
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S090`, `S092`, `S097`, `S118`, `S178`, `S181`, `S212`, `S214`, `S273`

**真实问法变体：**
- Redis 与 MySQL 分别适合存什么？
- Chat History 为什么放 Redis / MySQL，持久化怎样做？
- Database 与 Cache 的数据一致性和职责边界怎么设计？

### MYSQL-002 · 一条 SQL 从进入 MySQL 到返回结果，解析、优化、执行大致经历什么过程？Optimizer 在做什么？

- **Topic**：SQL Execution
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S119`, `S191`

**真实问法变体：**
- SQL 的完整执行生命周期是什么？
- MySQL Optimizer 在查询执行中承担什么职责？

### MYSQL-003 · 线上出现 Slow SQL 时，怎样用 EXPLAIN、索引命中与执行计划系统定位并优化？

- **Topic**：Slow SQL / EXPLAIN
- **Question Type**：Troubleshoot
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S005`, `S011`, `S063`, `S111`, `S173`, `S183`, `S191`, `S232`, `S256`, `S273`, `S274`

**真实问法变体：**
- MySQL 出现慢查询怎么定位？
- 怎样判断索引是否命中？
- 表刚建时查询很快，数据增长后逐渐变慢，怎么排查？

### MYSQL-004 · MySQL / InnoDB 索引为什么通常使用 B+Tree？相比 B-Tree、红黑树或 Hash 有什么优势？

- **Topic**：B+Tree
- **Question Type**：Why / Comparison
- **Depth**：L2
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**13**
- **Evidence Sources**：`S004`, `S005`, `S013`, `S112`, `S133`, `S154`, `S172`, `S175`, `S191`, `S224`, `S234`, `S258`, `S273`

**真实问法变体：**
- 数据库索引底层为什么用 B+Tree？
- B+Tree 与 B-Tree 为什么在数据库场景表现不同？
- 为什么不用红黑树？

### MYSQL-005 · 聚簇索引与非聚簇 / 二级索引有什么区别？InnoDB 中数据和索引怎样组织？

- **Topic**：Clustered / Secondary Index
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S112`, `S240`, `S273`

**真实问法变体：**
- Clustered / Non-clustered Index 有什么区别？
- InnoDB 的主键索引和二级索引分别保存什么？

### MYSQL-006 · 联合索引如何工作？最左匹配原则、范围条件与列顺序怎样影响索引利用？

- **Topic**：Composite Index
- **Question Type**：Concept / Scenario
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S010`, `S013`, `S025`, `S069`, `S154`, `S175`, `S199`, `S214`, `S258`, `S273`

**真实问法变体：**
- 联合索引的最左匹配怎么理解？
- 联合索引 `(A,B,C,D)` 遇到 `A > 1 AND B = 0` 会怎样使用？
- LIKE / 范围条件下联合索引还能利用到哪些列？

### MYSQL-007 · 哪些写法会导致索引失效或优化器不使用索引？如何判断这是“真失效”还是成本选择？

- **Topic**：Index Invalidation
- **Question Type**：Troubleshoot / Why
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S005`, `S011`, `S018`, `S081`, `S173`, `S175`, `S187`, `S246`, `S256`, `S273`, `S274`

**真实问法变体：**
- 常见索引失效原因有哪些？
- LIKE 查询怎样设计索引？
- 为什么有索引但执行计划仍不走索引？

### MYSQL-008 · 什么是回表、覆盖索引和索引下推？怎样减少随机 I/O 与不必要的数据页访问？

- **Topic**：Covering / Back-to-table / ICP
- **Question Type**：Concept / Optimization
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S005`, `S010`, `S025`, `S070`, `S175`, `S214`, `S234`, `S273`

**真实问法变体：**
- 什么是回表？
- `SELECT *` 与只查索引列有什么差异？
- Covering Index 为什么能减少回表？

### MYSQL-009 · 为什么 InnoDB 主键常推荐短、单调递增？UUID / 随机主键会怎样影响 Page Split、局部性与写入性能？

- **Topic**：Primary Key Design
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S175`, `S247`, `S274`

**真实问法变体：**
- 为什么主键常用自增 ID？
- UUID 为什么通常不适合作为 InnoDB 主键？
- B+Tree Leaf Split 会带来什么代价？

### MYSQL-010 · 深分页为什么会越来越慢？单表、分库分表场景分别怎样优化 Offset / 跳页 / 跨库聚合？

- **Topic**：Deep Pagination
- **Question Type**：Troubleshoot / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S010`, `S025`, `S093`, `S131`, `S147`

**真实问法变体：**
- MySQL 深分页怎么优化？
- 分库分表后的深分页、跳页和跨库聚合怎么做？

### MYSQL-011 · 事务的 ACID 分别是什么？MySQL 通过哪些机制实现原子性、一致性、隔离性和持久性？

- **Topic**：ACID
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S154`, `S188`, `S201`, `S234`

**真实问法变体：**
- 事务 ACID 是什么？
- MySQL 的事务原理怎样解释？

### MYSQL-012 · 四种事务隔离级别如何比较？Dirty Read、Non-repeatable Read、Phantom Read 分别如何产生和治理？

- **Topic**：Isolation Levels
- **Question Type**：Concept / Scenario
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**14**
- **Evidence Sources**：`S010`, `S069`, `S090`, `S124`, `S134`, `S154`, `S173`, `S188`, `S191`, `S199`, `S201`, `S234`, `S240`, `S273`

**真实问法变体：**
- 四种隔离级别有什么区别？
- 脏读、不可重复读、幻读怎样产生？
- InnoDB 默认隔离级别是什么？

### MYSQL-013 · MVCC 如何工作？隐藏列、undo log、ReadView 与可见性判断怎样协作？

- **Topic**：MVCC / ReadView
- **Question Type**：Concept / Deep Dive
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S010`, `S069`, `S148`, `S174`, `S188`, `S191`, `S201`, `S240`, `S273`

**真实问法变体：**
- MVCC 原理是什么？
- Hidden Column、Undo Log、ReadView 怎样协作？
- ReadView 如何判断某个版本是否可见？

### MYSQL-014 · RR 下幻读如何处理？MVCC、记录锁、Gap Lock、Next-Key Lock 的边界是什么？

- **Topic**：Phantom Read / Locks
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S069`, `S148`, `S191`, `S201`, `S240`, `S273`

**真实问法变体：**
- RR 下还会不会出现幻读？
- MVCC 是否一句话就能“解决幻读”？
- 不升 Serializable 如何治理幻读？

### MYSQL-015 · MySQL Deadlock 怎样产生、检测、定位和避免？

- **Topic**：Deadlock
- **Question Type**：Troubleshoot
- **Depth**：L3
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S191`

**真实问法变体：**
- MySQL Deadlock 怎么分析和处理？

### MYSQL-016 · redo log、undo log、binlog 分别解决什么问题？它们在事务、恢复和复制中怎样配合？

- **Topic**：Logs
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S020`, `S090`, `S173`, `S192`, `S240`

**真实问法变体：**
- undo / redo / binlog 各自作用是什么？
- binlog 与 redo log 的职责有什么不同？

### MYSQL-017 · 为什么需要 redo log 与 binlog 的两阶段提交？它要解决什么一致性问题？

- **Topic**：Two-phase Commit
- **Question Type**：Why / Deep Dive
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S192`

**真实问法变体：**
- 为什么 MySQL 需要两阶段提交？

### MYSQL-018 · MySQL 主从复制怎样工作？读请求走 Replica 时如何处理复制延迟与一致性？

- **Topic**：Replication
- **Question Type**：Concept / System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S090`, `S134`, `S246`

**真实问法变体：**
- MySQL Primary-Replica Replication 怎么工作？
- 读请求是否都应该走从库？
- 怎样处理主从延迟和读一致性？

### MYSQL-019 · 两个并发事务同时读写同一行时，不同隔离级别和锁下 SELECT / UPDATE / INSERT 会发生什么？

- **Topic**：Concurrent Transactions
- **Question Type**：Scenario / Deep Dive
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S195`

**真实问法变体：**
- 并发事务读写同一条数据时，每一步会发生什么？

### MYSQL-020 · 订单、评论、点赞、买卖双方账单等业务表应怎样建模？怎样处理热点字段、状态流转与查询模式？

- **Topic**：Schema Design
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S091`, `S093`, `S147`, `S189`, `S253`

**真实问法变体：**
- 评论表怎么设计？
- 点赞系统怎样设计表结构并处理 Hot Row？
- 买家 / 卖家账单双写表怎样建模？

### MYSQL-021 · 什么时候需要分库分表？Sharding Key 怎样选，怎样处理数据倾斜、扩容、跨分片查询和分页？

- **Topic**：Sharding
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S005`, `S093`, `S111`, `S127`, `S138`, `S147`, `S154`, `S189`, `S253`, `S273`

**真实问法变体：**
- 什么时候需要分库分表？
- Sharding Key 怎样选择？
- 跨分片查询 / 聚合 / 深分页怎样设计？

### MYSQL-022 · 大批量数据写入 / 导入 MySQL 时，怎样控制吞吐、事务大小、内存、失败重试和断点恢复？

- **Topic**：Bulk Write / Import
- **Question Type**：System Design / Troubleshoot
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S094`, `S191`, `S207`, `S232`, `S244`

**真实问法变体：**
- 一亿条数据怎样快速写入 MySQL？
- 20 万行 Excel 怎样批量导入并控制 DB 压力？
- 导入到一半失败怎样断点续跑且避免重复写？

### MYSQL-023 · MySQL 与 Redis 双写时如何保证最终一致性？Cache Aside、删除缓存、延迟双删、补偿和故障窗口怎样理解？

- **Topic**：DB-Cache Consistency
- **Question Type**：System Design / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**20**
- **Evidence Sources**：`S005`, `S046`, `S090`, `S093`, `S105`, `S118`, `S134`, `S148`, `S154`, `S161`, `S171`, `S188`, `S198`, `S201`, `S212`, `S214`, `S234`, `S264`, `S266`, `S273`

**真实问法变体：**
- 数据库与缓存怎样保证一致性？
- 为什么写操作更常选择删除缓存而不是直接更新缓存？
- Delayed Double Delete 中节点宕机会怎样？

### MYSQL-024 · 能否使用 MySQL 实现分布式锁？与 Redis / ZooKeeper 等方案相比边界在哪里？

- **Topic**：DB Lock as Distributed Lock
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S191`

**真实问法变体：**
- MySQL 能不能实现分布式锁？

### MYSQL-025 · MySQL / ORM 如何防止 SQL Injection？参数化查询、预编译与动态 SQL 有什么注意点？

- **Topic**：SQL Injection
- **Question Type**：Security
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S070`, `S232`, `S254`

**真实问法变体：**
- MyBatis 如何避免 SQL Injection？
- SQL Injection 怎样防？

### MYSQL-026 · InnoDB 与其它 Storage Engine 的核心差异是什么？为什么 AI 应用业务表通常仍以 InnoDB 为主？

- **Topic**：Storage Engine / InnoDB
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S069`, `S240`

**真实问法变体：**
- MySQL Storage Engine 怎样选？
- InnoDB 的关键能力是什么？

### MYSQL-027 · 如何利用 binlog / Canal / CDC 做数据同步、索引更新或下游事件消费？怎样处理顺序、重复与恢复？

- **Topic**：CDC / Data Sync
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S127`, `S170`, `S244`, `S246`

**真实问法变体：**
- Canal 如何识别 DDL / DML 事件？
- MySQL 数据怎样同步到下游系统？
- 数据同步链路如何保证可恢复？

### MYSQL-028 · 当数据量增长后索引效果下降或写入成本上升，如何从基数、页分裂、表规模与访问模式重新评估索引？

- **Topic**：Index Lifecycle / Scale
- **Question Type**：Troubleshoot / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S175`, `S247`, `S274`

**真实问法变体：**
- 表数据增长后为什么变慢？
- Page Split 对写入和索引维护有什么影响？
- 索引设计是否需要随规模变化重新评估？

---

## 3. 从面经可以明确看到的 MySQL 追问链

### 3.1 Index 主线

```text
为什么需要 Index
→ 为什么是 B+Tree
→ Clustered / Secondary Index
→ Composite Index / Leftmost Prefix
→ Range / LIKE
→ Covering Index / Back-to-table
→ Index Invalid / Optimizer 不选索引
→ EXPLAIN / Slow SQL
→ Deep Pagination
→ 主键设计 / Page Split
```

这条链在 AI Backend / Agent Backend 场次中反复出现，说明 MySQL 不能只背“B+Tree 查询 O(logN)”。

### 3.2 Transaction 主线

```text
ACID
→ Isolation Level
→ Dirty / Non-repeatable / Phantom
→ MVCC
→ Undo + ReadView
→ Lock / Gap / Next-Key
→ Concurrent Transaction Scenario
→ Deadlock
→ redo / undo / binlog
→ Crash Recovery / Replication
```

真实面试经常从定义继续追到“两个并发事务逐句执行会发生什么”，因此教材必须加入时序图和事务场景推演。

### 3.3 AI Application 最重要的数据库工程主线

```text
MySQL 负责长期结构化业务事实
+
Redis 负责高频 / 临时 / Cache / Session
        ↓
DB + Cache Consistency
        ↓
Failure Window
        ↓
Retry / Idempotency / Compensation
        ↓
Scale
        ↓
Sharding / Bulk Write / CDC
```

当前 MySQL 证据里，`MYSQL-023` 的独立来源最多。对 AI Application 求职来说，这说明“数据库 + 缓存的一致性与失败恢复”应与索引 / MVCC 同级准备，而不是放在最后的附录。

---

## 4. 对后续 MySQL 教材目录的校准建议

这份面经数据**不会替代**完整知识体系，但已经足够决定章节权重。建议正式教材保留原来的系统路线，并做以下增强：

1. `SQL 基础` 后增加“一条 SQL 的执行路径 / Optimizer”作为从 SQL 到索引的桥梁；
2. Index 章节必须包含 **主键设计、Page Split、Optimizer 为什么可能不用索引**，不能只讲最左匹配；
3. Transaction 章节必须用多事务时间线解释 MVCC / Lock，而不是只有术语定义；
4. `redo / undo / binlog` 后加入 **2PC、Crash Recovery、Replication** 的关系图；
5. `MySQL + Redis Consistency` 升级为核心章节，并加入节点宕机、延迟双删失败、缓存重建和补偿；
6. `Schema Design` 加入订单 / 评论 / 点赞 / 账单等真实业务建模；
7. `Scale` 增加 Bulk Import、Sharding、CDC / Canal、Deep Pagination；
8. 每章最后映射本文件对应 QID，并保留真实问法作为章节验收题。

---

## 5. 不应被面经频率误导的内容

以下内容即使当前 HUMAN-A 直接命中较少，也仍可能是完整 MySQL 知识体系的必要部分：

- SQL 基本语法与 JOIN / GROUP BY / 子查询；
- 数据类型与 NULL 语义；
- DDL / DML 与基本约束；
- 索引创建与维护基础；
- 事务边界与连接生命周期；
- 常见 Schema 设计规范。

它们属于“从 0 学会 MySQL”的骨架，不会因为面经里常被当作默认前置而删除。
