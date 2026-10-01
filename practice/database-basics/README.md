# 数据库基础操作｜读懂输入、结果与状态变化

[← Practice](../README.md) · [MySQL](../../curriculum/03-mysql/README.md) · [Redis](../../curriculum/04-redis/README.md)

这里将数据库操作与 Python 语言小题、Coding 算法分开。默认已有相应代码或数据库环境；可以只对照正文中的输入与结果，也可在自己的独立测试数据上运行。操作示例不构成基础课程的额外完成门槛。

## MySQL：围绕表中的记录操作

| 想确认什么 | 正文与示例 |
|---|---|
| SELECT、INSERT、UPDATE、DELETE 改变什么，返回结果如何理解 | [单表基础操作](../../curriculum/03-mysql/docs/02-单表查询与增删改.md) |
| 字段类型、NULL、唯一约束和表关系如何影响合法输入 | [字段与约束](../../curriculum/03-mysql/docs/03-数据类型约束与表关系.md) |
| 多表关联与分组统计如何得到结果 | [关联与统计](../../curriculum/03-mysql/docs/04-关联查询与分组统计.md) |
| 示例有哪些初始数据、事务与运行边界 | [示例入口](../../curriculum/03-mysql/examples/README.md) · [实验说明](../../curriculum/03-mysql/examples/experiments.md) |

先区分“查询返回的行”“写入影响的行”和“事务已经提交的事实”。一次语句没有报错，不表示其他会话已经能观察到期望结果；事务与隔离的完整解释在 MySQL 正文中。

## Redis：围绕一个键的状态操作

| 想确认什么 | 正文与示例 |
|---|---|
| 字符串、Hash、List、Set、ZSet 各保存什么关系 | [数据类型与基本命令](../../curriculum/04-redis/docs/02-键与常用数据类型.md) |
| 覆盖值、原地更新和过期时间怎样相互影响 | [过期与淘汰](../../curriculum/04-redis/docs/03-过期与内存淘汰.md) |
| 同一条命令的返回值和状态变化为何不同 | [命令过程](../../curriculum/04-redis/examples/labs.md) |
| 哪些例子是离线模型，哪些需要真实服务 | [示例入口与边界](../../curriculum/04-redis/examples/README.md) |

例如命令返回 0，可能表示“没有新增字段”，不能一律理解为失败。逐条先确认命令语义，再看修改后的值、元素数和 TTL；几条命令放在一起也不自动变成一个原子业务操作。

## 与其他实践的关系

[Python 基础操作](../python-basics/README.md)练习语言与容器；[Coding](../coding/README.md)练习从题目推导程序。数据库操作关注查询、修改、事务与命令状态，不沿用算法题的解锁顺序。遇到跨数据库、缓存与消息协作的问题，再回到 [Backend](../../curriculum/05-backend-engineering/README.md)的系统机制。
