# MySQL｜版本与技术事实资料索引

[MySQL 课程](../../curriculum/04-mysql/README.md) · [实验环境](../../curriculum/04-mysql/examples/README.md)

本索引用于核对 MySQL 与 InnoDB 的技术事实。真人面经决定需要检验哪些问题，不替代官方语义；实验能验证其执行范围，不能自动证明断电、多副本和生产负载下的行为。

## 1. 版本基线

**版本核验日期：2026-09-26；编排复核日期：2026-09-27。课程目标：MySQL Community 9.7 LTS / InnoDB。**

| 范围 | 本次核验结果 | 阅读时怎样使用 |
|---|---|---|
| LTS 与 Innovation | 官方分别维护长期支持与创新系列 | 不能把版本号最大理解为唯一适合教学或生产的版本。 |
| 9.7 通用服务器维护版 | 9.7.2，2026-07-28 发布 | 正文使用 9.7 手册并记录具体行为条件。 |
| 9.7.3 | 2026-08-18 发布；说明仅针对 Docker 镜像安全更新 | 不将这个镜像补丁宣称为所有平台的一次通用服务器发布。 |
| 创新系列 | 下载页列出 26.7.0 | 不为了追新把其新增接口都列为本课程必修。 |
| 实际运行验证 | 见维护记录；本修订尚无真实 MySQL 服务端执行结果 | 不将语句分割、Python 测试或其他数据库测试当作目标版本验证。 |

版本证据：[发布策略](https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html)、[9.7.2 发布说明](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-2.html)、[9.7.3 发布说明](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-3.html)、[官方社区下载页](https://dev.mysql.com/downloads/mysql/)。下载页会变化，使用时再次核验。

## 2. 从操作到访问路径

| 要解决的疑问 | 一手资料 | 对应课程 |
|---|---|---|
| 如何创建数据库、表并读取数据？ | [创建和使用数据库](https://dev.mysql.com/doc/refman/9.7/en/database-use.html) | 01–02 |
| NULL 为什么不能按普通相等比较？ | [NULL 的使用](https://dev.mysql.com/doc/refman/9.7/en/working-with-null.html) | 03 |
| GROUP BY、JOIN 和结果顺序怎样表达？ | [SELECT](https://dev.mysql.com/doc/refman/9.7/en/select.html)、[JOIN](https://dev.mysql.com/doc/refman/9.7/en/join.html) | 04 |
| CHECK、UNIQUE、外键的保证有什么不同？ | [CHECK 约束](https://dev.mysql.com/doc/refman/9.7/en/create-table-check-constraints.html)、[外键约束](https://dev.mysql.com/doc/refman/9.7/en/create-table-foreign-keys.html) | 03、09、19 |
| 索引类型、主键和二级索引怎样组织？ | [索引使用](https://dev.mysql.com/doc/refman/9.7/en/mysql-indexes.html)、[聚簇与二级索引](https://dev.mysql.com/doc/refman/9.7/en/innodb-index-types.html) | 05–06 |
| 多列索引的范围由哪些条件决定？ | [多列索引](https://dev.mysql.com/doc/refman/9.7/en/multiple-column-indexes.html)、[范围优化](https://dev.mysql.com/doc/refman/9.7/en/range-optimization.html) | 07–08 |
| ICP 与覆盖索引省掉的读取相同吗？ | [索引条件下推](https://dev.mysql.com/doc/refman/9.7/en/index-condition-pushdown-optimization.html) | 07 |
| 执行计划的估算、实际行数和格式有什么区别？ | [EXPLAIN](https://dev.mysql.com/doc/refman/9.7/en/explain.html) | 08、13 |
| 索引如何安全观察和调整？ | [不可见索引](https://dev.mysql.com/doc/refman/9.7/en/invisible-indexes.html)、[在线 DDL](https://dev.mysql.com/doc/refman/9.7/en/innodb-online-ddl.html) | 14 |

`EXPLAIN` 的输出会受版本、格式设置、统计和数据分布影响。教材显式写出格式，不硬编码六行表必须命中某个索引。`EXPLAIN ANALYZE` 会实际执行支持的语句；JSON 格式的支持与 `explain_json_format_version` 有关，不跨版本照搬限制。

## 3. 事务、锁与恢复

| 要解决的疑问 | 一手资料 | 对应课程 |
|---|---|---|
| 什么时候真正提交，哪些语句会隐式提交？ | [自动提交、提交与回滚](https://dev.mysql.com/doc/refman/9.7/en/innodb-autocommit-commit-rollback.html)、[隐式提交](https://dev.mysql.com/doc/refman/9.7/en/implicit-commit.html) | 01、09 |
| 为什么选 InnoDB，其他引擎是否也有同样事务保证？ | [存储引擎](https://dev.mysql.com/doc/refman/9.7/en/storage-engines.html)、[InnoDB 与 ACID](https://dev.mysql.com/doc/refman/9.7/en/mysql-acid.html) | 09 |
| 同一个事务的两次读取为什么不同？ | [隔离级别](https://dev.mysql.com/doc/refman/9.7/en/innodb-transaction-isolation-levels.html)、[一致性读](https://dev.mysql.com/doc/refman/9.7/en/innodb-consistent-read.html) | 10 |
| 记录锁、间隙锁和锁定读分别保护什么？ | [InnoDB 锁](https://dev.mysql.com/doc/refman/9.7/en/innodb-locking.html)、[锁定读](https://dev.mysql.com/doc/refman/9.7/en/innodb-locking-reads.html) | 11 |
| 发生死锁或等待超时，回滚范围是否相同？ | [错误处理](https://dev.mysql.com/doc/refman/9.7/en/innodb-error-handling.html)、[死锁](https://dev.mysql.com/doc/refman/9.7/en/innodb-deadlocks.html) | 09、11 |
| Undo、Redo 和 Binlog 怎样分工？ | [Undo 日志](https://dev.mysql.com/doc/refman/9.7/en/innodb-undo-logs.html)、[Redo 日志](https://dev.mysql.com/doc/refman/9.7/en/innodb-redo-log.html)、[二进制日志](https://dev.mysql.com/doc/refman/9.7/en/binary-log.html) | 10、12 |
| 崩溃恢复与恢复到指定时间有什么区别？ | [InnoDB 恢复](https://dev.mysql.com/doc/refman/9.7/en/innodb-recovery.html)、[PITR](https://dev.mysql.com/doc/refman/9.7/en/point-in-time-recovery.html) | 12 |

双会话结论必须同时给出数据、隔离级别、索引、语句类型和执行顺序。旧快照可见性、写入冲突与业务成功是三个不同问题。

## 4. 扩展、同步与导入

- [复制](https://dev.mysql.com/doc/refman/9.7/en/replication.html)与[半同步复制](https://dev.mysql.com/doc/refman/9.7/en/replication-semisync.html)：核对接收、持久化和应用阶段，以及等待超时后的边界，对应第 16 章。
- [分区概述](https://dev.mysql.com/doc/refman/9.7/en/partitioning-overview.html)：区分一台服务器内的表分区与应用跨实例分片，对应第 18 章。
- [批量加载优化](https://dev.mysql.com/doc/refman/9.7/en/optimizing-innodb-bulk-data-loading.html)：理解批量大小、索引维护和导入成本，不将文档中的特殊加载设置直接用于在线业务，对应第 15 章。
- [LOAD DATA](https://dev.mysql.com/doc/refman/9.7/en/load-data.html)与[LOCAL 安全](https://dev.mysql.com/doc/refman/9.7/en/load-data-local-security.html)：区分客户端和服务器文件路径，检查权限及不可信服务器风险。
- [预处理语句](https://dev.mysql.com/doc/refman/9.7/en/sql-prepared-statements.html)：核对查询结构与参数值的区别。驱动的具体写法按所用语言查阅，对应第 04 章。

第 15–19 章中的批量写入、复制、CDC、分片与应用建模，部分会触及应用设计边界。正文只保留理解 MySQL 责任所需的前提，不把 checkpoint、cache consistency 或完整跨系统恢复平台写成 MySQL 自带能力。

自动验证脚本使用 [PyMySQL 官方安装说明](https://pymysql.readthedocs.io/en/latest/user/installation.html)中的 `rsa` 额外依赖，以支持 `caching_sha2_password` 等认证方式。安装成功和真实连接成功仍需分别验证。

## 5. 如何使用证据

正文足以理解核心概念，参考页用于核对规则与进一步阅读。面经来源和课程去向见[维护记录](../../guide/project/mysql-reader-revision-2026-09-27.md)，它们不修改官方语义，也不改变冻结来源计数。
