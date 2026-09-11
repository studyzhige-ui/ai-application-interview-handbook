# MySQL｜关系型数据、事务与查询工程

[← AI Backend Engineering](../backend-engineering/README.md) · [↑ Handbook 总目录](../README.md) · [Redis →](../redis/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：23 个连续知识小板块** · **HUMAN-A Canonical：26** · **独立来源覆盖：55**  
> **质量：Granularity / Coverage / Content Depth 已验收**

理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。

---

## 1. 这个模块解决什么

理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。

学习目标不是记住一组名词，而是能稳定回答：

```text
为什么需要它？
→ 核心机制怎样工作？
→ 正常路径怎样流动？
→ Failure / Trade-off 在哪里？
→ Production 场景怎样验证与排障？
→ 面试官继续追问时怎样解释边界？
```

---

## 2. 在十板块中的位置

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → **MySQL** → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent Harness / Runtime](../agent-harness/README.md) → [System Design](../system-design/README.md)

当前模块角色：**Data / 理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。**

---

## 3. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

同时固定区分：

```text
Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 一个完整认知闭环
Section = 参数 / 变体 / Failure / 深挖追问
```

所以本模块是 **26 道 Canonical → 23 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
SQL Execution → Index / B+Tree / Optimizer / EXPLAIN → Transaction / Isolation / MVCC / Lock / Log → Pagination / Schema → Replication / Sharding / CDC / Bulk Write → AI Data Modeling / Cache Boundary
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜查询与索引

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

### Part C｜数据增长与生产扩展

16. [Deep Pagination 与查询优化](docs/16-DeepPagination与查询优化.md)
17. [Schema Design：从访问模式设计表](docs/17-SchemaDesign.md)
18. [Replication 与读写分离](docs/18-Replication与读写分离.md)
19. [Sharding：什么时候才需要分库分表](docs/19-Sharding.md)
20. [CDC / Data Sync](docs/20-CDC与数据同步.md)
21. [Bulk Write 与 MySQL Write Path](docs/21-BulkWrite与写入路径.md)

### Part D｜AI Application 数据层边界

22. [AI Application Data Modeling](docs/22-AI应用数据建模.md)
23. [MySQL + Redis Consistency 的边界](docs/23-MySQL-Redis一致性边界.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **26 道 Primary Canonical、55 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- Isolation Levels
- B+Tree
- Slow SQL / EXPLAIN
- Index Invalidation / Composite Index
- Sharding
- MVCC / Lock

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- InnoDB 索引、事务、MVCC、锁与日志归 MySQL。
- DB + Cache 最终一致性的完整机制归 AI Backend Engineering。
- Redis Lock、TTL、Cluster 归 Redis；跨组件架构选择归 System Design。

遇到跨模块问题时，正文会保留必要桥梁，但完整机制只在 Primary Module 维护一份。

---

## 8. Review、Interview 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |
| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |
| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |
| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |

研究与质量证据：

- [Canonical Questions](../research/questions/mysql.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

1. **第一遍：建立因果链。** 按 `docs/01 → 23` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–23 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[Redis](../redis/README.md)。
