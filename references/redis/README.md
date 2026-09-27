# Redis 官方资料｜按需要核对机制与版本

[← Redis 课程](../../curriculum/05-redis/README.md) · [References](../README.md)

本索引用于核对课程中的具体结论，不要求读者先读完官方手册，也不规定使用哪一种应用语言的客户端。教程解释为什么使用和怎样观察，这里给出相应规则的权威依据。

## 1. 版本口径

课程固定 **Redis Open Source 8.10.2**，官方稳定版发布于 **2026-09-17**，前稿版本核验日期 **2026-09-26**；本轮保持该固定目标，不因写作重组改动版本。不要与 Redis Software、Cloud 的版本号混用，也不假设每种托管服务开放全部管理命令。

- [8.10.2 官方发布](https://github.com/redis/redis/releases/tag/8.10.2)：版本、修复与升级依据。
- [固定版本配置](https://github.com/redis/redis/blob/8.10.2/redis.conf)：核对实际默认值，而不只看最新在线页面。
- [官方安装](https://redis.io/docs/latest/operate/oss_and_stack/install/)：按平台和部署方式准备。

正文是目标版教材；当前交付是否实际运行该版本，应看[验证记录](../../guide/project/redis-reader-restructure-2026-09-27.md)，不能从本页固定版本推断已执行完所有实验。

## 2. 会影响旧答案的变化

| 内容 | 应怎样理解 | 依据 |
|---|---|---|
| `ZRANGE ... REV` | 6.2 起整合反向范围查询；ZREVRANGE 不推荐，不是已经不能运行 | [ZRANGE](https://redis.io/docs/latest/commands/zrange/)、[ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/) |
| Hash 字段期限 | 7.4 起支持字段级期限，不再绝对回答“只有整键 TTL” | [HEXPIRE](https://redis.io/docs/latest/commands/hexpire/) |
| Functions | 7 起的命名库管理，不是永不丢的 EVALSHA 缓存 | [Functions](https://redis.io/docs/latest/develop/programmability/functions-intro/) |
| 多段 AOF | 7 起应考虑基线、增量与清单，不随意复制一份旧式文件 | [Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) |
| 条件删除 | 8.4 起 `DELEX ... IFEQ` 可表达比较后删除；旧版本用经过校验的短 Lua | [DELEX](https://redis.io/docs/latest/commands/delex/) |
| Hash template | 8.10.2 配置中 `hash-min-template-entries` 为 0 时关闭自动转换；不是所有 Hash 必然使用 | [固定 redis.conf](https://github.com/redis/redis/blob/8.10.2/redis.conf) |
| 产品能力 | Redis 8 发行能力包含搜索、JSON 与向量等，教材模块职责不能用来否认产品功能 | [Redis 项目](https://github.com/redis/redis) |
| 安全修复 | 8.10.2 涉及 ACL 检查和 Cluster 总线安全等；新增选择不等于默认自动启用 | [Release](https://github.com/redis/redis/releases/tag/8.10.2) |

新特性只在能澄清实际行为的位置使用，没有把完整发布说明变成新的必修目录。

## 3. 命令与数据的直接依据

| 要核对的问题 | 官方入口 |
|---|---|
| SET 的条件、覆盖和期限 | [SET](https://redis.io/docs/latest/commands/set/) |
| 缺失、有效期限与修改影响 | [EXPIRE](https://redis.io/docs/latest/commands/expire/)、[GETEX](https://redis.io/docs/latest/commands/getex/) |
| 核心类型与各自操作 | [Data types](https://redis.io/docs/latest/develop/data-types/) |
| SCAN 完整遍历和重复边界 | [SCAN](https://redis.io/docs/latest/commands/scan/) |
| 同一逻辑类型的编码与内存 | [Memory optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/) |
| 内存候选和近似淘汰策略 | [Eviction](https://redis.io/docs/latest/develop/reference/eviction/) |
| 逻辑删除与释放的区别 | [UNLINK](https://redis.io/docs/latest/commands/unlink/) |

## 4. 多步骤、复制与恢复

- [Transactions](https://redis.io/docs/latest/develop/using-commands/transactions/)：队列错误、执行错误和 WATCH。
- [Pipelining](https://redis.io/docs/latest/develop/using-commands/pipelining/)：往返优化，不等于事务。
- [Lua 执行](https://redis.io/docs/latest/develop/programmability/eval-intro/)与[Lua API](https://redis.io/docs/latest/develop/programmability/lua-api/)：原子范围、错误和键声明。
- [Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)：快照、日志、同步、重写与恢复。
- [Replication](https://redis.io/docs/latest/operate/oss_and_stack/management/replication/)、[WAIT](https://redis.io/docs/latest/commands/wait/)、[WAITAOF](https://redis.io/docs/latest/commands/waitaof/)：确认对象与失败窗口。
- [Sentinel](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/)：检测、授权与选举。
- [Cluster specification](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/)：槽位、标签、重定向和多键限制。
- [Distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)：获取、归属、租期与时间假设。正文对外部副作用的谨慎取舍，不等于宣称一种锁适用于全部资源。

## 5. 应用、消息与排障

- [Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)、[XREADGROUP](https://redis.io/docs/latest/commands/xreadgroup/)、[XACK](https://redis.io/docs/latest/commands/xack/)、[XAUTOCLAIM](https://redis.io/docs/latest/commands/xautoclaim/)：在线广播、交付、确认与接管分别核对。
- [Client-side caching](https://redis.io/docs/latest/develop/reference/client-side-caching/)：跟踪与失效通知，不替代客户端恢复策略。
- [INCR](https://redis.io/docs/latest/commands/incr/)：计数与原子过期组合的动机；具体限流规则由课程明确声明。
- [Security](https://redis.io/docs/latest/operate/oss_and_stack/management/security/)、[ACL](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/)：网络、服务账户与权限。
- [Latency](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/)、[SLOWLOG](https://redis.io/docs/latest/commands/slowlog-get/)：计时范围和诊断成本。
- [Aerospike 存储](https://aerospike.com/docs/database/manage/planning/ssd)、[主索引配置](https://aerospike.com/docs/database/manage/namespace/primary-index/)：只用于选型问题所需的最小对照，不作无条件性能排名。

## 6. 来源与测试各证明什么

真人面经证明某类问题被问到，不证明候选人的所有解释正确。官方文档定义行为和适用条件，示例测试检验一份程序在具体环境中的表现；三者要配合，不能互相冒充。

没有运行的真实 Redis 用例必须标为未执行，不能拿 RESP 解析器单测或离线算术测试代替服务器结果。目标版本、单机、复制集群、托管服务和生产故障，也应分别记录。
