# MySQL｜AI 应用开发秋招系统手册

> MySQL 是这套 Handbook 的第 4 个正式一级模块。
>
> 目标不是学成 DBA，也不是背一份“数据库八股题库”，而是建立一条从 0→1 的完整认知主线：**一条 SQL 怎样执行 → 索引为什么快 → 查询为什么会慢 → 事务并发如何保证正确 → 数据量增长后怎样扩展 → MySQL 怎样进入真实 AI Application / Agent Backend。**

## 1. 最重要的课程原则

本模块固定遵守：

> **知识体系演进顺序优先，真实面经只用于调整复习权重、补充真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

因此，即使 Sharding、Cache Consistency 在真人面经里很高频，也不会提前到 B+Tree、Transaction、MVCC 之前。

正确关系是：

```text
完整 MySQL 知识体系
        ↓
从 0 建立因果链
        ↓
真实面经校准哪里更高频、会追多深
        ↓
再用真人问题验收
```

而不是：

```text
别人问什么
→ 我们就只学什么
```

---

## 2. 为什么 AI Application / Agent 岗仍然需要系统学 MySQL

AI Demo 可能只有：

```text
User
 ↓
LLM / RAG / Agent
```

真正上线以后会出现：

```text
User / Tenant
Conversation / Message
Agent Run / Task
Tool Execution
Knowledge Base Metadata
Document / Permission
Billing / Usage
Evaluation Result
Business State
```

其中大量数据天然适合关系数据库。

冻结 `S001–S279` HUMAN-A 研究中，MySQL 有 **26 道 Canonical、55 个独立招聘流程**提供证据。

高频市场信号包括：

| Topic | HUMAN-A Sources |
|---|---:|
| Isolation Levels | 14 |
| B+Tree | 13 |
| Slow SQL / EXPLAIN | 11 |
| Index Invalidation | 11 |
| Composite Index | 10 |
| Sharding | 10 |
| MVCC / ReadView | 9 |
| Covering / Back-to-table / ICP | 8 |
| Phantom / Locks | 6 |
| Logs | 5 |
| Schema Design | 5 |
| CDC / Data Sync | 4 |
| Deep Pagination | 4 |

> **Interview Heat ≠ Knowledge Importance。** Storage Engine、SQL 基础、Deadlock、Bulk Write 等即使出现次数较少，只要是知识体系必要节点，仍然保留。

---

## 3. 版本口径

正文以现代 **MySQL + InnoDB** 为主，核心机制以 MySQL 8.4 LTS Reference Manual 作为稳定事实基线。

- 不把旧版本实现细节写成永恒规则；
- 面试默认优先解释 InnoDB；
- 当前版本变化不会反向修改冻结 HUMAN-A Source Count。

官方入口：

- <https://dev.mysql.com/doc/refman/8.4/en/>
- <https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html>
- <https://dev.mysql.com/doc/refman/8.4/en/optimization.html>
- <https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-transaction-model.html>

---

## 4. 三条核心主线

### 主线 A｜查询性能

```text
SQL
→ Optimizer
→ Index
→ B+Tree
→ Clustered / Secondary
→ Composite Index
→ Covering / ICP
→ EXPLAIN
→ Slow SQL
→ Pagination / Index Lifecycle
```

### 主线 B｜并发正确性

```text
Transaction
→ ACID
→ Isolation
→ MVCC / ReadView
→ Record / Gap / Next-Key Lock
→ Deadlock
→ Undo / Redo / Binlog
→ Crash Recovery
```

### 主线 C｜生产扩展

```text
Schema
→ Replication
→ Sharding
→ CDC
→ Bulk Write
→ AI Application Data Modeling
→ MySQL + Redis Integration Boundary
```

这三条线不是按面经频率排序，而是按知识依赖顺序建立。

---

## 5. 完整 23 章

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

### Part C｜数据量增长后的自然演进

16. [Deep Pagination 与查询优化](docs/16-DeepPagination与查询优化.md)
17. [Schema Design：从访问模式设计表](docs/17-SchemaDesign.md)
18. [Replication 与读写分离](docs/18-Replication与读写分离.md)
19. [Sharding：什么时候才需要分库分表](docs/19-Sharding.md)
20. [CDC / Data Sync](docs/20-CDC与数据同步.md)
21. [Bulk Write 与 MySQL Write Path](docs/21-BulkWrite与写入路径.md)

### Part D｜回到 AI Application 数据层

22. [AI Application Data Modeling](docs/22-AI应用数据建模.md)
23. [MySQL + Redis Consistency 的边界](docs/23-MySQL-Redis一致性边界.md)

为什么把 Cache Consistency 放最后？

因为它已经是**跨存储系统问题**。必须先理解 MySQL 的 Source of Truth、Transaction、Binlog、CDC 与业务数据模型，才能真正理解 Cache Aside、Failure Window 和最终一致性。

---

## 6. 推荐三遍学习法

### 第一遍：从 0 建立体系

严格按 `01 → 23` 阅读。

不要因为 `Sharding`、`Distributed Lock` 更像“高级八股”就跳着学。

### 第二遍：图解与推演

进入：

> [MySQL 图解复习与自测](review/README.md)

重点自己画：

- B+Tree / 回表；
- Composite Index Range；
- ReadView；
- Next-Key Lock；
- Redo / Binlog；
- Replication；
- Sharding；
- CDC。

### 第三遍：面试化

- [高频面试题](interview/高频面试题.md)
- [面试易错点](interview/面试易错点.md)
- [面试前速查表](interview/面试前速查表.md)

正确顺序始终是：

```text
先理解
→ 再口述
→ 再承受追问
```

不是先背 30 秒答案。

---

## 7. 每章统一写法

```text
先讲人话
→ 准确定义
→ SQL / 示例
→ 数据结构 / 执行路径
→ 对比
→ 为什么
→ Failure Case
→ AI 应用场景
→ 面试怎么答
→ 易错点
→ 继续追问
→ 折叠自测
```

常用标记：

- 💡 新手理解
- 🧠 为什么
- ⚠️ 面试易错点
- 🎯 面试怎么答
- 🔍 继续追问

---

## 8. 一条贯穿全书的业务

核心示例：

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

一路追问：

```text
为什么这样建主键？
为什么这样设计联合索引？
回表发生在哪里？
OFFSET 100000 为什么慢？
两个 Worker 抢同一个 Run 怎么办？
RR / MVCC / Lock 会发生什么？
COMMIT Crash 怎么恢复？
Replica 延迟怎么办？
十亿行后是否真的需要 Sharding？
Binlog / CDC 怎么更新下游？
Agent Run / Step / Tool Event 应怎样建模？
Redis Cache 和 MySQL 如何保持可控一致？
```

同一业务贯穿 23 章，帮助形成长期因果记忆。

---

## 9. 与其它一级模块的边界

| 问题 | Primary Module |
|---|---|
| InnoDB 索引、事务、MVCC、锁、日志 | MySQL |
| MySQL + Redis 双写最终一致性 | AI Backend Engineering |
| Redis Distributed Lock | Redis |
| Cache 穿透 / 击穿 / 雪崩 | Redis |
| Agent Checkpoint / Resume | Agent Harness / Runtime |
| 大规模可靠任务 / Backpressure | AI Backend Engineering / System Design |
| HNSW / IVF / Vector Index | Vector DB |
| RAG Retrieval / Rerank / Eval | RAG |

第 23 章只是 MySQL 学习结束时的“跨系统边界桥梁”，不会把 Backend 体系复制进 MySQL。

---

## 10. 研究证据入口

- [`../research/questions/mysql.md`](../research/questions/mysql.md)：26 道 MySQL Canonical；
- [`../research/analysis/curriculum-evidence-matrix.md`](../research/analysis/curriculum-evidence-matrix.md)：Topic 频率与深度；
- [`../research/analysis/follow-up-chains.md`](../research/analysis/follow-up-chains.md)：回到原始 Batch 核验的追问链；
- [`../research/analysis/frequency-ranking.md`](../research/analysis/frequency-ranking.md)：全局市场热度。

正式知识解释以官方 / 权威资料为事实基线；**HUMAN-A 只负责回答“市场在问什么、会追多深”。**

---

## 11. 当前状态

```text
MySQL docs 01–23            ✅
章节折叠自测                 ✅
Review 总入口与图解          ✅
高频面试题                   ✅
面试易错点                   ✅
面试前速查                   ✅
```

MySQL 第一版系统教材主体已经完成。

---

## 12. 下一环

下一模块：**Redis**。

仍然采用完全相同的原则：

> **从数据结构与 Runtime 原理开始，从 0→1 建体系；面经只校准重点，不决定知识骨架。**
