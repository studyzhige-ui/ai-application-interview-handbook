# MySQL｜AI 应用开发秋招系统手册

> MySQL 是这套 Handbook 的第 4 个正式一级模块。
>
> 目标不是学成 DBA，也不是背一份“数据库八股题库”，而是建立一条足够完整的工程主线：**一条 SQL 怎样执行 → 索引为什么快 → 查询为什么会慢 → 事务并发如何保证正确 → 数据量增长后怎样扩展 → MySQL 怎样进入真实 AI Application / Agent Backend。**

## 1. 为什么 AI Application / Agent 岗仍然需要系统学 MySQL

很多 AI 应用项目一开始只是：

```text
User
  ↓
FastAPI
  ↓
LLM / RAG / Agent
```

一旦真正上线，马上会出现传统但无法绕开的数据问题：

```text
用户 / Tenant
Conversation / Message
Agent Run / Task
Tool Execution
Knowledge Base Metadata
Document / Permission
Billing / Usage
Evaluation Result
Business State
```

这些数据里，大量信息仍然天然适合关系数据库。

所以真实 AI Application / Agent 面试不会因为岗位里有“大模型”三个字就放弃数据库基础。冻结的 `S001–S279` HUMAN-A 研究里，MySQL 共有 **26 道 Canonical、55 个独立招聘流程**提供证据。

市场最强信号：

| Topic | 独立 HUMAN-A 来源 | 最高深度 |
|---|---:|---:|
| Isolation Levels | 14 | L3 |
| B+Tree | 13 | L2 |
| Slow SQL / EXPLAIN | 11 | L3 |
| Index Invalidation | 11 | L3 |
| Composite Index | 10 | L3 |
| Sharding | 10 | L4 |
| MVCC / ReadView | 9 | L2 |
| Covering / Back-to-table / ICP | 8 | L3 |
| Phantom Read / Locks | 6 | L3 |
| Logs | 5 | L2 |
| Schema Design | 5 | L4 |
| CDC / Data Sync | 4 | L4 |
| Deep Pagination | 4 | L3 |

> **Interview Heat ≠ Knowledge Importance。** SQL 基础、Storage Engine、Deadlock 等即使真人面经计数较低，只要是理解完整体系的必要前置，仍然保留。

---

## 2. 本模块采用什么 MySQL 版本口径

正文以现代 **MySQL + InnoDB** 为主，核心机制优先参考 MySQL 官方 Reference Manual。

为了让教材稳定、适合秋招复习：

- 核心机制主要以 **MySQL 8.4 LTS** 官方文档作为稳定基线；
- 版本相关行为会明确标注，不把某个旧版本实现细节讲成永恒规则；
- 当前更新的 MySQL LTS / Innovation 版本不会反向改变冻结 HUMAN-A 的 `Source Count`；
- 面试中如果只问“MySQL”，默认优先解释 InnoDB，因为它是现代 MySQL 的默认事务存储引擎。

官方资料入口：

- MySQL 8.4 Reference Manual：<https://dev.mysql.com/doc/refman/8.4/en/>
- MySQL Releases: Innovation and LTS：<https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html>
- InnoDB：<https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html>
- Optimization / Index：<https://dev.mysql.com/doc/refman/8.4/en/optimization.html>
- Transactions / Locking：<https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-transaction-model.html>

---

## 3. 推荐学习方法

沿用 Python 模块已经验证过的方式：

> **先讲人话 → 准确定义 → SQL / 示例 → 数据结构 / 执行路径 → 对比 → 为什么 → Failure Case → 面试怎么答 → 继续追问 → 自测**

学习时不要把 MySQL 拆成几十个孤立名词。始终追这三条主线：

```text
主线 A：查询性能
SQL → Optimizer → Index → B+Tree → EXPLAIN → Slow SQL → Scale

主线 B：并发正确性
Transaction → Isolation → MVCC → Lock → Deadlock → Recovery

主线 C：生产扩展
Schema → Replication → Sharding → CDC → Bulk Write → AI Data Modeling
```

### 推荐三遍法

1. **第一遍：建立地图。** 先知道每个机制解决什么问题，不要求背细节。
2. **第二遍：沿执行路径理解。** 自己画 B+Tree、回表、ReadView、Next-Key Lock、redo/binlog 流程图。
3. **第三遍：面试化。** 不再问“MVCC 是什么”，而是练“两个事务按这个顺序执行，会读到什么 / 锁住什么 / 为什么”。

---

## 4. 完整章节地图

### Part A｜一条查询为什么快或慢

1. [MySQL 在 AI Application 中负责什么](docs/01-MySQL在AI应用中的职责.md)
2. [SQL 基础与一条 SQL 的执行链路](docs/02-SQL基础与执行链路.md)
3. [Index 基础：索引到底在优化什么](docs/03-Index基础.md)
4. [为什么 InnoDB 使用 B+Tree](docs/04-B+Tree索引原理.md)
5. [聚簇索引与二级索引](docs/05-聚簇索引与二级索引.md)
6. [联合索引与最左前缀](docs/06-联合索引与最左前缀.md)
7. [覆盖索引、回表与 ICP](docs/07-覆盖索引-回表-ICP.md)
8. [索引失效与 Optimizer 成本选择](docs/08-索引失效与Optimizer.md)
9. [EXPLAIN 与 Slow SQL 排查](docs/09-EXPLAIN与SlowSQL.md)
10. [主键设计与索引生命周期](docs/10-主键设计与索引生命周期.md)

### Part B｜事务与并发正确性

11. [ACID 与事务边界](docs/11-ACID与事务.md)
12. [四种事务隔离级别](docs/12-事务隔离级别.md)
13. [MVCC、Undo 与 ReadView](docs/13-MVCC-Undo-ReadView.md)
14. [Record / Gap / Next-Key Lock 与 Deadlock](docs/14-锁与死锁.md)
15. [redo、undo、binlog 与两阶段提交](docs/15-日志与两阶段提交.md)

### Part C｜查询、数据模型与规模增长

16. [Deep Pagination 与查询优化](docs/16-DeepPagination与查询优化.md)
17. [Schema Design：从访问模式设计表](docs/17-SchemaDesign.md)
18. [Replication 与读写分离](docs/18-Replication与读写分离.md)
19. [Sharding：什么时候才需要分库分表](docs/19-Sharding.md)
20. [CDC / Data Sync](docs/20-CDC与数据同步.md)
21. [Bulk Write 与 MySQL Write Path](docs/21-BulkWrite与写入路径.md)

### Part D｜与 AI Backend 汇合

22. [MySQL + Redis Consistency 的边界](docs/22-MySQL-Redis一致性边界.md)
23. [AI Application Data Modeling](docs/23-AI应用数据建模.md)

---

## 5. 面试优先级

| 区域 | 优先级 | 为什么 |
|---|---:|---|
| B+Tree / 聚簇与二级索引 | ⭐⭐⭐⭐⭐ | 是后续回表、主键设计、Page Split 的基础 |
| 联合索引 / 最左前缀 / 范围 | ⭐⭐⭐⭐⭐ | 高频场景题，容易只背口诀不会分析 |
| EXPLAIN / Slow SQL | ⭐⭐⭐⭐⭐ | 真实工程追问比“索引定义”更重要 |
| Isolation / MVCC / Lock | ⭐⭐⭐⭐⭐ | 高频且非常容易混淆快照读、锁定读、幻读 |
| Redis + MySQL 一致性 | ⭐⭐⭐⭐⭐ | Primary 在 Backend，但 MySQL 机制必须懂 |
| Sharding | ⭐⭐⭐⭐⭐ | 10 个独立 HUMAN-A，直接进入 L4 System Design |
| redo / undo / binlog | ⭐⭐⭐⭐ | 事务、恢复、复制的共同底座 |
| Schema / Primary Key | ⭐⭐⭐⭐ | 项目验真和系统设计常继续追 |
| Replication / CDC | ⭐⭐⭐⭐ | AI 搜索索引、缓存、下游同步都需要 |
| SQL 基础 | ⭐⭐⭐⭐ | 不是最高频，但不会 SQL 就无法解释执行计划 |
| Bulk Write | ⭐⭐⭐ | 低频但属于大规模 ingestion 的真实能力 |

---

## 6. 一条贯穿全书的示例业务

为了避免每章都换一套背景，本手册会反复使用一个简化 AI Application 数据模型：

```sql
CREATE TABLE agent_runs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    tenant_id BIGINT NOT NULL,
    status VARCHAR(32) NOT NULL,
    model_name VARCHAR(64) NOT NULL,
    token_cost INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_tenant_user_created (tenant_id, user_id, created_at),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB;
```

后面会围绕它不断追问：

```text
为什么这样建主键？
联合索引列顺序为什么这样放？
查最近 100 条为什么快？
OFFSET 100000 为什么慢？
status 更新频繁会怎样影响索引？
两个 Worker 抢同一个 Run 怎么办？
事务隔离和锁如何影响并发？
数据量到十亿以后要不要分片？
binlog / CDC 怎样同步到搜索或分析系统？
```

同一个业务一路走到底，比背 20 个互不相关的例子更容易形成长期记忆。

---

## 7. 与其它模块的边界

| 问题 | Primary Module |
|---|---|
| InnoDB 索引、事务、MVCC、锁、日志 | MySQL |
| MySQL + Redis 双写最终一致性 | AI Backend Engineering |
| Redis Distributed Lock | Redis |
| 大规模跨服务可靠任务 | AI Backend Engineering / System Design |
| Agent Checkpoint 本身怎样恢复 | Agent Harness / Runtime |
| Agent Run / Message / Tool Event 表怎样设计 | MySQL + System Design 交叉 |
| RAG 文档 Metadata 存 MySQL 还是 Vector DB | System Design / Vector DB / MySQL 交叉 |

课程里会主动做链接，但不会为了“看起来完整”在多个一级模块复制同一知识模型。

---

## 8. 每章必须回答六类问题

```text
Concept：它是什么？
Mechanism：内部怎样工作？
Trade-off：为什么这样选？
Failure：什么时候会坏 / 慢 / 不正确？
Scale：数据量和并发上来后怎么办？
Verification：怎样用 SQL / EXPLAIN / 指标证明判断？
```

真实面试已经大量进入 L3 / L4。如果只会回答“B+Tree 是多叉平衡树”“MVCC 提高并发”，通常还不够。

---

## 9. 研究证据入口

市场证据不直接复制成教材答案，而用来校准重点和追问深度：

- [`../research/questions/mysql.md`](../research/questions/mysql.md)：26 道 MySQL Canonical；
- [`../research/analysis/curriculum-evidence-matrix.md`](../research/analysis/curriculum-evidence-matrix.md)：Topic 频率与深度；
- [`../research/analysis/follow-up-chains.md`](../research/analysis/follow-up-chains.md)：已回到原始 Batch 核验的真实递进；
- [`../research/analysis/frequency-ranking.md`](../research/analysis/frequency-ranking.md)：全局热度。

正式知识解释以官方 / 权威资料为事实基线；**HUMAN-A 只负责回答“市场在问什么、会追多深”。**

---

## 10. 下一环

MySQL 学完后进入：

> **Redis → Vector DB → LLM Foundation → RAG → Agent Harness / Runtime**

这时你会开始真正理解：为什么一个 AI Application 的数据层不能只靠“一个 Vector DB + 一个 JSON 文件”。
