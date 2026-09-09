# Batch 07 — 规范化问题增量（Python / MySQL / Redis 基础校准）

本文件只新增此前尚未明确建模、且由高质量真实面经支持的问题。已有问题继续增加来源，不重复造 ID。

## Python / FastAPI

### P001 Python dict 的哈希表如何实现插入、查询、冲突处理与删除？
- 来源：S078
- 标签：Python / dict / Hash Table / Runtime
- 面试意义：AI Agent 岗仍可能直接追语言底层，而不只问 async/await 或框架 API。

### P002 Python 多线程与 Java/Go 多线程或协程的核心差异是什么？GIL 对 CPU-bound / IO-bound 任务分别意味着什么？
- 来源：S077, S079, S084
- 标签：Python / GIL / Thread / Concurrency / Comparison
- 课程关联：应与 `python-interview-handbook` 的 GIL、线程/进程/协程章节双向链接。

### P003 FastAPI 请求从进入服务到匹配路由处理函数的关键链路是什么？async endpoint 的并发边界在哪里？
- 来源：S077, S081
- 标签：Python / FastAPI / Routing / Async / Web Runtime
- 课程意义：AI 应用岗的 Python 不应只停留在语言语法；Web Runtime 是生产 Agent 服务的基础。

## MySQL

### M010 MySQL 慢查询应该如何通过 Slow Log、EXPLAIN、索引、锁等待、数据分布和资源指标系统定位？
- 来源：S081
- 标签：MySQL / Slow Query / EXPLAIN / Performance

### M011 本地缓存 + Redis + MySQL 多层数据体系如何设计一致性、失效、回源与故障降级？
- 来源：S082, S083, S085
- 标签：MySQL / Redis / Cache Consistency / Production
- 与已有一致性题区别：本题明确覆盖多级缓存、故障和数据源优先级，而非只问单次并发更新。

## Redis

### D013 Redis Cluster 的分片、主从、故障发现与 Failover 如何工作？节点异常时客户端和数据层分别会发生什么？
- 来源：S079
- 标签：Redis / Cluster / High Availability / Failover

### D014 ZSet 的排序与底层结构如何实现？用于排行榜、滑动窗口/限流时的时间与内存瓶颈是什么？
- 来源：S079, S082, S083, S084
- 标签：Redis / ZSet / Skiplist / Rate Limit / Complexity

## Backend / AI Application Foundation

### B016 AI 应用中的缓存故障如何避免“Redis 一挂，所有流量直冲 MySQL”的级联故障？
- 来源：S078, S080, S083, S086
- 标签：Backend / Redis / MySQL / Cache Failure / Degrade / Rate Limit
- 核心拆解：Fail-open vs Fail-closed、限流、降级、热点保护、空值/旧值兜底、恢复后的缓存重建与一致性校准。

---

## 已有 canonical questions 得到显著强化

- `M001` MySQL B+Tree / 索引原理：S082, S085
- `M002/M003` 隔离级别 / MVCC：S082, S083, S084
- `M007/M008/M009` 并发、联合索引、锁：S082, S083, S084, S086
- `D001/D003` Redis 在 AI 系统中的职责 / 数据结构：S079, S081, S082, S085
- `D006` RDB / AOF：S079
- `D011` 分布式锁 Lease / WatchDog：S083
- `D012` HotKey：S080, S086
- `A015/A016` Memory 与多用户状态：S079, S080, S084
- `A020/A021` Multi-Agent 编排与通信：S079, S084
- `A054/A075` Tool / Agent 权限治理：S078, S079, S080
- `R001/R004/R008` RAG 链路、召回与 Rerank：S077, S080, S083, S084, S085, S086

## Batch 07 对课程权重的校准

后续学习路线不按“新增 canonical 数量”决定重要性，而采用三层权重：

1. **知识体系必要性**：即使近期面经没问，也不能从课程删除。
2. **真实面试命中频率**：决定复习优先级和面试口述熟练度。
3. **岗位/轮次条件概率**：同一知识点在 Agent Harness 二面、AI 应用一面、AI 后端社招中的出现概率不同。

因此：

- Python 基础仍是必修，但要从“语法八股”升级到 `dict / GIL / async / FastAPI / 并发 / 工程化`。
- MySQL 仍是 AI 应用开发的长期业务数据底座，索引、事务、MVCC、锁、慢 SQL、缓存一致性都必须系统掌握。
- Redis 仍是 Session / Cache / State / Lock / Rate Limit / Queue 等低延迟工程能力的重要底座。
- Agent Harness 深挖不会替代这些基础，而是建立在这些基础之上。