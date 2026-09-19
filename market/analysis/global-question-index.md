# Global Canonical Question Index

更新日期：2026-09-11

> 自动从十个正式 Canonical 文件生成；统计范围为 Frozen Canonical Baseline `S001–S279 / 235 ACTIVE`。本文件不创建新证据，只提供全局可排序视图。

| QID | Module | Topic | Depth | Sources | Heat | Canonical Question |
|---|---|---|---:|---:|---|---|
| `PY-001` | Python | Language Choice | L3 | 4 | 🔥🔥 | 为什么 AI Application / Agent 工程常使用 Python？与 Java / Go 相比，语言选择应依据什么？ |
| `PY-002` | Python | Built-in Containers | L2 | 1 | 单点真实信号 | Python `list` 与 `tuple` 的语义、可变性、典型使用场景和成本有什么差异？ |
| `PY-003` | Python | dict / Hash Table | L2 | 1 | 单点真实信号 | Python `dict` 的 Hash、冲突处理、删除与底层表结构怎样工作？ |
| `PY-004` | Python | Function Parameters | L2 | 1 | 单点真实信号 | Python Function Parameters 有哪些形式？位置参数、关键字参数、默认参数、`*args` / `**kwargs` 的绑定规则是什么？ |
| `PY-005` | Python | Dynamic Typing / Protocol Thinking | L2 | 1 | 单点真实信号 | Duck Typing 如何理解？它给接口设计、可替换性和错误暴露带来什么收益与风险？ |
| `PY-006` | Python | Iterator / Generator | L2 | 2 | 🔥 | Iterator 与 Generator 有什么区别？Generator 为什么能保存执行状态并按需产出数据？ |
| `PY-007` | Python | Decorator | L3 | 3 | 🔥 | Python Decorator 怎样工作？如何用它实现 Logging、Tracing 或横切逻辑？ |
| `PY-008` | Python | Context Manager | L2 | 1 | 单点真实信号 | Python Context Manager 的协议与资源生命周期怎样理解？什么时候应使用 `with` 管理资源？ |
| `PY-009` | Python | Slicing | L2 | 1 | 单点真实信号 | Python Slicing 的语义是什么？切片在时间、空间与对象复制上有什么成本？ |
| `PY-010` | Python | GIL | L3 | 2 | 🔥 | Python GIL 是什么？它怎样影响 CPU-bound 与 I/O-bound 并发设计？ |
| `PY-011` | Python | Threading / Multiprocessing | L3 | 2 | 🔥 | `threading` 与 `multiprocessing` 应怎样选择？大量 PDF / CPU 密集与 I/O 密集任务分别适合什么并发模型？ |
| `PY-012` | Python | asyncio | L3 | 3 | 🔥 | `asyncio` Event Loop 怎样工作？`gather`、`as_completed`、`await` 与 Timeout / Fallback 怎样组合高并发 I/O？ |
| `PY-013` | Python | Synchronization Primitives | L2 | 1 | 单点真实信号 | `Lock`、`RLock`、`Semaphore` 分别解决什么并发问题，什么时候使用？ |
| `PY-014` | Python | Structured Data Validation | L3 | 1 | 单点真实信号 | Python 中怎样解析、校验并约束 LLM 产生的 JSON / Structured Output？ |
| `PY-015` | Python | Closure | L2 | 1 | 单点真实信号 | Python Closure 是什么？闭包在真实项目中适合什么场景？ |
| `FASTAPI-001` | FastAPI | ASGI / Request Lifecycle | L2 | 1 | 单点真实信号 | FastAPI 的请求链路怎样工作？ASGI、Web Server 与 Application Framework 各自承担什么职责？ |
| `FASTAPI-002` | FastAPI | Middleware / Dependency | L3 | 1 | 单点真实信号 | FastAPI Middleware 与 Dependency Injection 有什么差异？认证、日志、公共上下文等横切逻辑应放在哪里？ |
| `FASTAPI-004` | FastAPI | Streaming Endpoint | L3 | 1 | 单点真实信号 | FastAPI + SSE 怎样把 Agent / LangGraph 的中间事件实时推送到前端？ |
| `FASTAPI-005` | FastAPI | Framework Boundary | L4 | 1 | 单点真实信号 | 只会 FastAPI GET / POST 为什么不足以构建 Claude Code 类 Agent Service？FastAPI 层还需要怎样承接 Streaming、Session 与 Runtime 状态？ |
| `AIBE-001` | AI Backend Engineering | HTTP Request Lifecycle | L2 | 8 | 🔥🔥 | 从输入 URL 到服务返回，一次 HTTP 请求的 DNS、连接、协议与服务端处理链路怎样发生？ |
| `AIBE-002` | AI Backend Engineering | HTTPS / TLS | L3 | 9 | 🔥🔥 | HTTP 与 HTTPS 的核心差异是什么？TLS 握手、证书信任链、对称 / 非对称加密怎样协作？ |
| `AIBE-003` | AI Backend Engineering | HTTP Versions / QUIC | L2 | 4 | 🔥🔥 | HTTP/1.1、HTTP/2、HTTP/3 与 QUIC 的核心差异是什么？AI Streaming Service 为什么关心这些差异？ |
| `AIBE-004` | AI Backend Engineering | TCP / UDP | L2 | 12 | 🔥🔥🔥 | TCP 与 UDP 有什么差异？可靠传输、顺序、连接语义和实时性怎样影响服务选型？ |
| `AIBE-005` | AI Backend Engineering | TCP Reliability | L3 | 12 | 🔥🔥🔥 | TCP 三次握手、四次挥手、重传与拥塞控制为什么这样设计？异常断连怎样被感知？ |
| `AIBE-006` | AI Backend Engineering | SSE / WebSocket | L3 | 13 | 🔥🔥🔥 | SSE 与 WebSocket 的通信模型、方向、连接维护和适用场景有什么差异？ |
| `AIBE-007` | AI Backend Engineering | Streaming Reliability | L4 | 3 | 🔥 | Streaming Connection 断开后怎样做 Heartbeat、Reconnect、Resume 与状态补偿？ |
| `AIBE-008` | AI Backend Engineering | Service Communication | L3 | 5 | 🔥🔥 | HTTP、RPC / gRPC 和 MQ 在跨服务通信中怎样选择？延迟、耦合、Schema、可靠性与演进成本分别是什么？ |
| `AIBE-009` | AI Backend Engineering | Process / Thread / Coroutine | L2 | 12 | 🔥🔥🔥 | Process、Thread、Coroutine 的核心区别是什么？上下文切换、资源隔离与并发模型怎样影响 AI Backend？ |
| `AIBE-010` | AI Backend Engineering | Thread Pool | L3 | 12 | 🔥🔥🔥 | Thread Pool 的核心参数、任务流转、拒绝策略和线程数应该怎样设计？ |
| `AIBE-011` | AI Backend Engineering | Producer / Consumer / Backpressure | L4 | 4 | 🔥🔥 | 高并发 Producer / Consumer 或任务执行模型怎样设计 Queue、并发上限和 Backpressure？ |
| `AIBE-012` | AI Backend Engineering | Async Service | L3 | 7 | 🔥🔥 | AI / LLM I/O 为什么适合异步非阻塞调用？同步 / 异步、Event Loop 与 Long-running Task 怎样取舍？ |
| `AIBE-013` | AI Backend Engineering | Concurrency Control | L4 | 4 | 🔥🔥 | 如何限制并发调用外部 API，避免 Connection Pool、Downstream 或模型服务被打满？ |
| `AIBE-014` | AI Backend Engineering | Message Queue | L3 | 11 | 🔥🔥🔥 | MQ 在 AI Backend / Agent 异步链路中为什么存在？相比数据库传状态或同步 RPC，它解决什么问题？ |
| `AIBE-015` | AI Backend Engineering | MQ Reliability | L4 | 12 | 🔥🔥🔥 | MQ 怎样保证消息尽量不丢、避免重复消费，并处理 Producer / Broker / Consumer Failure？ |
| `AIBE-016` | AI Backend Engineering | Kafka | L4 | 7 | 🔥🔥 | Kafka Partition、Consumer Group、顺序性与 Backlog 怎样理解？积压时如何定位流量、分区和消费能力瓶颈？ |
| `AIBE-017` | AI Backend Engineering | Rate Limiting | L4 | 10 | 🔥🔥🔥 | Rate Limit 常见算法怎样比较？Single-node、Distributed、User / Tenant / Token Budget 限流怎样设计？ |
| `AIBE-018` | AI Backend Engineering | Resilience | L4 | 10 | 🔥🔥🔥 | Retry、Circuit Breaker、Degradation 与 Fallback 分别解决什么问题？怎样避免重试风暴和级联故障？ |
| `AIBE-019` | AI Backend Engineering | Idempotency | L4 | 8 | 🔥🔥 | 有副作用的请求怎样设计 Idempotency？Retry / Timeout / Crash 后怎样避免重复扣款、下单或执行？ |
| `AIBE-020` | AI Backend Engineering | Data Consistency / Cache Architecture | L4 | 20 | 🔥🔥🔥 | Database + Cache 双写怎样保证最终一致性？Cache Aside、删除缓存、补偿和 Failure Window 怎样理解？ |
| `AIBE-021` | AI Backend Engineering | API Design | L3 | 2 | 🔥 | 一个 Production REST API 应怎样设计 Method、Error、Idempotency、Versioning 与演进边界？ |
| `AIBE-022` | AI Backend Engineering | Auth / Permission | L4 | 8 | 🔥🔥 | Authentication 与 Authorization 怎样区分？Access Token / Refresh Token、Session、OAuth2 和服务端权限边界怎样设计？ |
| `AIBE-023` | AI Backend Engineering | Session / Routing | L4 | 3 | 🔥 | 多实例 Session / Token 状态怎样共享与路由？服务无状态化与 Sticky Session 怎样取舍？ |
| `AIBE-024` | AI Backend Engineering | Service Discovery / Load Balancing | L3 | 5 | 🔥🔥 | Service Discovery 与 Load Balancing 怎样工作？DNS / Nginx / Registry / Heartbeat 的边界是什么？ |
| `AIBE-025` | AI Backend Engineering | Distributed ID | L3 | 4 | 🔥🔥 | Global Unique ID 怎样生成？Snowflake、自增 ID、随机 ID 的唯一性、趋势递增与可用性如何权衡？ |
| `AIBE-026` | AI Backend Engineering | Linux Troubleshooting | L3 | 6 | 🔥🔥 | Linux 线上服务出现 CPU、Memory、Disk、Port / Process 异常时怎样系统排查？ |
| `AIBE-027` | AI Backend Engineering | Docker / Container | L3 | 7 | 🔥🔥 | Docker / Container 解决什么问题？Container 与 Host 的 Process、Network、Filesystem、Resource Isolation 有什么边界？ |
| `AIBE-028` | AI Backend Engineering | Kubernetes | L3 | 3 | 🔥 | Kubernetes 在 AI Service / Agent Backend 中承担哪些 Deployment、Scaling、Isolation 与 Availability 能力？ |
| `AIBE-029` | AI Backend Engineering | Backend Observability | L4 | 6 | 🔥🔥 | Production Backend Observability 应如何组织 Metrics、Log、Trace，并从一次请求定位到具体服务 / 进程 /依赖故障？ |
| `AIBE-030` | AI Backend Engineering | Configuration Management | L4 | 3 | 🔥 | Configuration Center / Dynamic Config 怎样实现优先级、热更新、监听、失败回退与版本治理？ |
| `AIBE-031` | AI Backend Engineering | Microservice / DDD | L4 | 5 | 🔥🔥 | Monolith 到 Microservice 应怎样拆边界？DDD、Gateway、RPC / MQ、Config、Transaction 与 Observability 如何协同？ |
| `AIBE-032` | AI Backend Engineering | Java / Spring | L2 | 6 | 🔥🔥 | Spring / Spring Boot 的 Bean Lifecycle、Dependency Injection、AOP / Proxy 与 MVC Request Flow 怎样工作？ |
| `AIBE-033` | AI Backend Engineering | Java Concurrency | L3 | 8 | 🔥🔥 | Java 并发中的 `synchronized`、`ReentrantLock`、CAS / AQS 与 Concurrent Collection 怎样选择？ |
| `AIBE-034` | AI Backend Engineering | JVM Runtime | L3 | 12 | 🔥🔥🔥 | JVM Memory Area、Class Loading 与 GC 怎样工作？OOM / Memory Leak 出现时如何定位？ |
| `AIBE-035` | AI Backend Engineering | Java Collection | L2 | 7 | 🔥🔥 | Java HashMap / ConcurrentHashMap 的底层结构、Resize、树化与并发安全怎样理解？ |
| `AIBE-036` | AI Backend Engineering | ThreadLocal | L3 | 8 | 🔥🔥 | ThreadLocal 的实现、生命周期和 Memory Leak 风险是什么？在线程池中怎样正确清理？ |
| `AIBE-037` | AI Backend Engineering | Go Runtime | L3 | 8 | 🔥🔥 | Go Goroutine / GMP / Channel 与 Thread / Mutex 的核心差异是什么？Runtime 怎样调度大量并发任务？ |
| `AIBE-038` | AI Backend Engineering | Backend Security | L4 | 4 | 🔥🔥 | SSRF、CSRF、SQL Injection、XSS、Reverse Shell 与 Container Escape 等常见安全风险怎样理解和防护？ |
| `AIBE-039` | AI Backend Engineering | Data Layering | L4 | 11 | 🔥🔥🔥 | 结构化业务事实、Cache、Session 与 Runtime State 应怎样在 MySQL / Redis 等存储之间分层？ |
| `MYSQL-002` | MySQL | SQL Execution | L2 | 2 | 🔥 | 一条 SQL 从进入 MySQL 到返回结果，解析、优化、执行大致经历什么过程？Optimizer 在做什么？ |
| `MYSQL-003` | MySQL | Slow SQL / EXPLAIN | L3 | 11 | 🔥🔥🔥 | 线上出现 Slow SQL 时，怎样用 EXPLAIN、索引命中与执行计划系统定位并优化？ |
| `MYSQL-004` | MySQL | B+Tree | L2 | 13 | 🔥🔥🔥 | MySQL / InnoDB 索引为什么通常使用 B+Tree？相比 B-Tree、红黑树或 Hash 有什么优势？ |
| `MYSQL-005` | MySQL | Clustered / Secondary Index | L2 | 3 | 🔥 | 聚簇索引与二级索引有什么区别？InnoDB 中数据和索引怎样组织？ |
| `MYSQL-006` | MySQL | Composite Index | L3 | 10 | 🔥🔥🔥 | 联合索引如何工作？最左匹配、范围条件与列顺序怎样影响索引利用？ |
| `MYSQL-007` | MySQL | Index Invalidation | L3 | 11 | 🔥🔥🔥 | 哪些写法会导致索引失效或 Optimizer 不使用索引？怎样区分真正失效与成本选择？ |
| `MYSQL-008` | MySQL | Covering / Back-to-table / ICP | L3 | 8 | 🔥🔥 | 什么是回表、覆盖索引和索引下推？怎样减少随机 I/O 与不必要的数据页访问？ |
| `MYSQL-009` | MySQL | Primary Key Design | L3 | 3 | 🔥 | 为什么 InnoDB 主键常推荐短、单调递增？UUID / 随机主键怎样影响 Page Split、局部性与写入性能？ |
| `MYSQL-010` | MySQL | Deep Pagination | L3 | 4 | 🔥🔥 | 单表或单分片内的 Deep Pagination 为什么随着 Offset 增大而变慢？怎样用覆盖索引、Seek / Keyset Pagination 等方法优化？ |
| `MYSQL-011` | MySQL | ACID | L2 | 4 | 🔥🔥 | 事务的 ACID 分别是什么？MySQL 通过哪些机制实现原子性、隔离性和持久性？ |
| `MYSQL-012` | MySQL | Isolation Levels | L3 | 14 | 🔥🔥🔥 | 四种事务隔离级别怎样比较？Dirty Read、Non-repeatable Read、Phantom Read 如何产生和治理？ |
| `MYSQL-013` | MySQL | MVCC / ReadView | L2 | 9 | 🔥🔥 | MVCC 如何工作？隐藏列、undo log、ReadView 与可见性判断怎样协作？ |
| `MYSQL-014` | MySQL | Phantom Read / Locks | L3 | 6 | 🔥🔥 | RR 下幻读如何处理？MVCC、Record Lock、Gap Lock、Next-Key Lock 的边界是什么？ |
| `MYSQL-015` | MySQL | Deadlock | L3 | 1 | 单点真实信号 | MySQL Deadlock 怎样产生、检测、定位和避免？ |
| `MYSQL-016` | MySQL | Logs | L2 | 5 | 🔥🔥 | redo log、undo log、binlog 分别解决什么问题？在事务、恢复与复制中怎样配合？ |
| `MYSQL-017` | MySQL | Two-phase Commit | L2 | 1 | 单点真实信号 | 为什么需要 redo log 与 binlog 的两阶段提交？它解决什么一致性问题？ |
| `MYSQL-018` | MySQL | Replication | L4 | 3 | 🔥 | MySQL 主从复制怎样工作？读请求走 Replica 时如何处理复制延迟与一致性？ |
| `MYSQL-019` | MySQL | Concurrent Transactions | L4 | 1 | 单点真实信号 | 两个并发事务同时读写同一行时，不同隔离级别和锁下 SELECT / UPDATE / INSERT 会发生什么？ |
| `MYSQL-020` | MySQL | Schema Design | L4 | 5 | 🔥🔥 | 订单、评论、点赞、买卖双方账单等业务表怎样建模？如何处理热点字段、状态流转与查询模式？ |
| `MYSQL-021` | MySQL | Sharding | L4 | 10 | 🔥🔥🔥 | 什么时候需要分库分表？Sharding Key 怎样选，如何处理数据倾斜、扩容、跨分片查询与分页？ |
| `MYSQL-022` | MySQL | Bulk Write / MySQL Write Path | L3 | 1 | 单点真实信号 | 大批量写入 MySQL 时，怎样控制 Batch Size、Transaction Size、Index / Log 开销与写入吞吐？ |
| `MYSQL-024` | MySQL | DB Lock as Distributed Lock | L4 | 1 | 单点真实信号 | 能否使用 MySQL 实现分布式锁？与 Redis / ZooKeeper 等方案相比边界在哪里？ |
| `MYSQL-025` | MySQL | SQL Injection | L3 | 3 | 🔥 | MySQL / ORM 如何防止 SQL Injection？参数化查询、预编译与动态 SQL 有什么注意点？ |
| `MYSQL-026` | MySQL | Storage Engine / InnoDB | L2 | 2 | 🔥 | InnoDB 与其它 Storage Engine 的核心差异是什么？为什么业务表通常仍以 InnoDB 为主？ |
| `MYSQL-027` | MySQL | CDC / Data Sync | L4 | 4 | 🔥🔥 | 如何利用 binlog / Canal / CDC 做数据同步、索引更新或下游事件消费？怎样处理顺序、重复与恢复？ |
| `MYSQL-028` | MySQL | Index Lifecycle / Scale | L3 | 3 | 🔥 | 数据量增长后索引效果下降或写入成本上升，怎样从基数、Page Split、表规模和访问模式重新评估索引？ |
| `REDIS-002` | Redis | Data Structures | L2 | 18 | 🔥🔥🔥 | Redis 常见数据结构 String / Hash / List / Set / ZSet 各自适合什么场景，底层特性怎样影响选型？ |
| `REDIS-003` | Redis | Performance / Thread Model | L2 | 7 | 🔥🔥 | Redis 为什么快？“单线程”到底指什么，命令执行、网络 I/O 与后台任务怎样理解？ |
| `REDIS-004` | Redis | I/O Multiplexing | L3 | 1 | 单点真实信号 | Redis 的 I/O Multiplexing / Event Loop 如何工作？它与 NIO / Reactor 有什么关系？ |
| `REDIS-005` | Redis | TTL / Expiration | L2 | 7 | 🔥🔥 | Redis TTL、过期删除与 Lazy / Active Expiration 怎样工作？TTL 应怎样设置？ |
| `REDIS-006` | Redis | Eviction | L3 | 5 | 🔥🔥 | Redis 内存不足时有哪些 Eviction Policy？LRU / LFU 等策略怎样选择，淘汰后热点 Key 立即回流怎么办？ |
| `REDIS-007` | Redis | Cache Failure Patterns | L3 | 20 | 🔥🔥🔥 | Cache Penetration、Breakdown / Stampede、Avalanche 分别是什么？怎样用 Bloom Filter、互斥、随机 TTL 等治理？ |
| `REDIS-008` | Redis | BigKey / HotKey | L4 | 11 | 🔥🔥🔥 | BigKey 与 HotKey 怎样发现、治理和拆分？迁移 / 删除过程中怎样避免阻塞与一致性问题？ |
| `REDIS-009` | Redis | Persistence | L2 | 4 | 🔥🔥 | RDB 与 AOF 的原理、恢复特性和取舍是什么？Redis 故障后怎样恢复数据？ |
| `REDIS-010` | Redis | High Availability | L2 | 8 | 🔥🔥 | Redis Primary/Replica、Sentinel、Cluster 的职责和高可用边界分别是什么？ |
| `REDIS-011` | Redis | Cluster / Hash Slot | L4 | 5 | 🔥🔥 | Redis Cluster 的 Hash Slot、Sharding、扩缩容与数据迁移如何工作？Lua / Multi-key 为什么受 Slot 约束？ |
| `REDIS-012` | Redis | Distributed Lock Basics | L2 | 25 | 🔥🔥🔥 | Redis 分布式锁的基本实现是什么？正确性需要满足哪些条件？ |
| `REDIS-013` | Redis | Distributed Lock Correctness | L4 | 14 | 🔥🔥🔥 | Redis Lock 的 Expire、Renewal / WatchDog、Owner 校验、Lua Release、RedLock 与故障窗口怎样处理？ |
| `REDIS-014` | Redis | Lua / Atomicity | L3 | 10 | 🔥🔥🔥 | Lua Script 为什么适合 Redis 原子业务？库存扣减、限流、锁释放等场景如何设计？ |
| `REDIS-016` | Redis | Multi-level Cache | L4 | 6 | 🔥🔥 | Local Cache + Redis 多级缓存怎样分工？如何处理热 Key、失效风暴和缓存层级间的一致性？ |
| `REDIS-017` | Redis | Session / Conversation | L4 | 11 | 🔥🔥🔥 | Redis 如何承载 Session / Conversation / Auth Cache？多实例下怎样处理过期、隔离与共享？ |
| `REDIS-019` | Redis | Redis Rate Limit Implementation | L4 | 8 | 🔥🔥 | Redis 如何具体实现 Sliding Window / Token Bucket 等限流？ZSet / Counter / Lua / TTL 怎样保证原子性与性能？ |
| `REDIS-021` | Redis | Semantic / Result Cache | L4 | 2 | 🔥 | 语义缓存、查询结果缓存与普通业务 Cache 有什么不同？什么结果值得缓存，如何避免陈旧答案？ |
| `REDIS-022` | Redis | Security | L4 | 1 | 单点真实信号 | Redis 有哪些安全风险？无密码实例、越权访问与敏感状态怎样防护？ |
| `REDIS-024` | Redis | KV Store Selection | L2 | 1 | 单点真实信号 | Redis 与 Aerospike 等 KV Store 在存储模型、容量、延迟和业务场景上怎样选型？ |
| `VDB-002` | Vector DB | Similarity Metrics | L2 | 6 | 🔥🔥 | Cosine Similarity、Dot Product / Inner Product、L2 Distance 有什么区别？归一化怎样影响结果？ |
| `VDB-003` | Vector DB | Exact Search vs ANN | L2 | 4 | 🔥🔥 | 为什么大规模向量检索不能总做暴力 Exact Search？ANN 牺牲什么、换来什么？ |
| `VDB-004` | Vector DB | Index Selection | L4 | 10 | 🔥🔥🔥 | Vector Index 怎样根据数据规模、更新频率、Recall、Latency、Memory 与 QPS 选择？ |
| `VDB-005` | Vector DB | HNSW | L3 | 11 | 🔥🔥🔥 | HNSW 的基本图搜索机制是什么？为什么能在高维空间做近似最近邻搜索？ |
| `VDB-006` | Vector DB | IVF | L3 | 5 | 🔥🔥 | IVF / IVF_FLAT 的基本思想是什么？Cluster / List 划分与候选范围怎样影响 Recall 和 Latency？ |
| `VDB-007` | Vector DB | HNSW vs IVF | L3 | 10 | 🔥🔥🔥 | HNSW 与 IVF 怎样比较？Recall、Latency、Memory、Build Cost、Update Pattern 如何权衡？ |
| `VDB-008` | Vector DB | Metadata Filtering | L4 | 6 | 🔥🔥 | Metadata Filter / Partition / Tenant Filter 怎样与向量索引结合？Pre-filter / Post-filter 有什么边界？ |
| `VDB-009` | Vector DB | Vector Storage / Product / Architecture Selection | L4 | 20 | 🔥🔥🔥 | 为什么需要独立 Vector DB？Milvus、FAISS、pgvector、Elasticsearch Vector 等方案在 Library、DB Extension、Search Engine、专用 Vector DB 之间怎样选？ |
| `VDB-011` | Vector DB | Vector Data Modeling | L3 | 3 | 🔥 | Vector Database 的 Collection / Partition / Schema / Primary Key / Metadata 应怎样建模？ |
| `VDB-018` | Vector DB | Vector / Index Parameters | L3 | 3 | 🔥 | Vector Dimension、Normalization、Distance Metric 与 Index 参数怎样影响存储、内存和检索成本？ |
| `VDB-020` | Vector DB | Index Lifecycle / Freshness | L4 | 9 | 🔥🔥 | Embedding / Index 版本升级后怎样处理 Re-embedding、Index Rebuild、Incremental Update 与旧向量兼容？ |
| `VDB-022` | Vector DB | Graph DB vs Vector DB | L4 | 7 | 🔥🔥 | Graph Database 与 Vector Database 的数据模型、查询能力和适用场景有什么差异？ |
| `LLM-001` | LLM Foundation（应用工程深度） | Tokenization | L2 | 4 | 🔥🔥 | Token 是什么？Tokenizer 为什么把文本拆成 Token，而不是按字符或单词直接处理？ |
| `LLM-002` | LLM Foundation（应用工程深度） | Context Window | L3 | 7 | 🔥🔥 | Context Window 的能力边界由什么决定？为什么 Context 变大仍不能把所有信息无差别塞进去？ |
| `LLM-003` | LLM Foundation（应用工程深度） | Long-context Limitation | L2 | 2 | 🔥 | Lost in the Middle 为什么发生？长 Context 中信息位置会怎样影响模型利用率？ |
| `LLM-004` | LLM Foundation（应用工程深度） | Inference / Generation | L2 | 2 | 🔥 | 从 Prompt 输入到逐 Token 生成，一次 LLM Generation 的底层路径怎样解释？ |
| `LLM-005` | LLM Foundation（应用工程深度） | Transformer Architecture | L2 | 10 | 🔥🔥🔥 | Transformer 的整体 Architecture 是什么？Attention、FFN、Residual / Normalization 等模块怎样协作？ |
| `LLM-006` | LLM Foundation（应用工程深度） | QKV / Self-Attention | L2 | 7 | 🔥🔥 | Self-Attention 中 Q / K / V 怎样产生并计算？为什么这种结构能建模 Token 关系？ |
| `LLM-007` | LLM Foundation（应用工程深度） | Multi-Head Attention | L2 | 5 | 🔥🔥 | Multi-Head Attention 为什么需要多个 Head？不同 Head 带来什么表达能力？ |
| `LLM-008` | LLM Foundation（应用工程深度） | FFN | L2 | 1 | 单点真实信号 | FFN 在 Transformer 中承担什么作用？Attention 与 FFN 为什么都需要？ |
| `LLM-009` | LLM Foundation（应用工程深度） | Positional Encoding / RoPE | L2 | 1 | 单点真实信号 | RoPE / Rotary Positional Embedding 的核心思想是什么，位置关系怎样进入 Attention？ |
| `LLM-010` | LLM Foundation（应用工程深度） | Multimodal Foundation | L2 | 4 | 🔥🔥 | Transformer 为什么能够扩展到多模态？Visual Encoder 与 Language Model 怎样连接 / 对齐？ |
| `LLM-011` | LLM Foundation（应用工程深度） | KV Cache | L3 | 3 | 🔥 | KV Cache 为什么能加速 Autoregressive Generation？它怎样影响显存与并发？ |
| `LLM-012` | LLM Foundation（应用工程深度） | Prefill / Decode | L3 | 1 | 单点真实信号 | Prefill 与 Decode 分别是什么？为什么 Serving 会关注 Prefill / Decode 分离？ |
| `LLM-013` | LLM Foundation（应用工程深度） | Inference Engine | L3 | 4 | 🔥🔥 | PagedAttention 的核心思想是什么？vLLM / SGLang 等 Serving Engine 主要优化什么？ |
| `LLM-014` | LLM Foundation（应用工程深度） | Inference Latency | L3 | 3 | 🔥 | LLM API Latency 通常由哪些阶段构成？TTFT、生成速度、模型大小与并发怎样影响用户体验？ |
| `LLM-015` | LLM Foundation（应用工程深度） | Sampling Parameters | L2 | 3 | 🔥 | Temperature、Top-k、Top-p 等 Sampling 参数怎样影响生成？为什么 Temperature=0 仍不保证绝对确定？ |
| `LLM-016` | LLM Foundation（应用工程深度） | Model API | L3 | 5 | 🔥🔥 | Chat / Model API 中 Messages、Role、Model 与其它常见字段怎样组织？应用层如何适配不同 Provider？ |
| `LLM-017` | LLM Foundation（应用工程深度） | Model Selection | L4 | 10 | 🔥🔥🔥 | Base Model / Model Size 应怎样选？效果、Latency、Cost、Context、Tool Calling 与业务风险如何权衡？ |
| `LLM-018` | LLM Foundation（应用工程深度） | Embedding Model | L2 | 6 | 🔥🔥 | Embedding 为什么能表示语义？Embedding Model 怎样训练，Dimension / Backbone 变化带来什么权衡？ |
| `LLM-019` | LLM Foundation（应用工程深度） | Rerank Model | L3 | 3 | 🔥 | Embedding Model、Bi-Encoder 与 Cross-Encoder / Reranker 的目标、计算方式和成本有什么差异？ |
| `LLM-020` | LLM Foundation（应用工程深度） | Fine-tuning | L3 | 9 | 🔥🔥 | Fine-tuning 的基本流程是什么？应用工程师在 Dataset、Training、Evaluation 与 Deployment 上需要理解到什么深度？ |
| `LLM-021` | LLM Foundation（应用工程深度） | Post-training / Alignment | L3 | 8 | 🔥🔥 | SFT、LoRA、PPO、DPO、GRPO、Knowledge Distillation 分别解决什么问题，什么时候值得使用？ |
| `LLM-022` | LLM Foundation（应用工程深度） | Hallucination / Factuality | L3 | 10 | 🔥🔥🔥 | Hallucination / Factuality 问题为什么出现？哪些属于模型本身局限，哪些应由 RAG / Agent / Verification 层治理？ |
| `LLM-023` | LLM Foundation（应用工程深度） | Prompt Engineering | L3 | 30 | 🔥🔥🔥 | Prompt Engineering 应怎样从目标、角色、约束、Context、Example、Tool 与 Output Contract 组织并迭代？怎样用真实 Case / Evaluation 证明 Prompt 优化有效？ |
| `RAG-001` | RAG | RAG Boundary | L4 | 12 | 🔥🔥🔥 | 为什么需要 RAG？什么时候 Long Context、文件搜索、更强模型或 Fine-tuning 更合适？ |
| `RAG-002` | RAG | End-to-end Pipeline | L3 | 38 | 🔥🔥🔥 | Production RAG 从 Ingestion / Parse / Chunk / Embedding / Index 到 Retrieve / Rerank / Context / LLM 的完整链路是什么？ |
| `RAG-003` | RAG | Corpus / Data Audit | L4 | 7 | 🔥🔥 | 建 RAG 前怎样审计 Corpus：数据来源、质量、重复、版本、权限和真实规模如何影响方案？ |
| `RAG-004` | RAG | Parsing / OCR / Layout | L4 | 13 | 🔥🔥🔥 | PDF / OCR / Layout / Markdown / HTML 等异构文档怎样可靠解析？电子 PDF 与扫描 PDF 如何统一处理？ |
| `RAG-005` | RAG | Multimodal / Table Parsing | L4 | 9 | 🔥🔥 | 表格、图片与多模态内容怎样保留结构和引用关系？Cross-page Table 被切断时如何恢复语义？ |
| `RAG-006` | RAG | Chunking Principles | L3 | 15 | 🔥🔥🔥 | 文档切分为什么是 RAG 核心环节？Chunk Granularity 怎样影响 Recall、Precision、Context Noise 与 Generation？ |
| `RAG-007` | RAG | Chunk Strategy | L3 | 30 | 🔥🔥🔥 | Chunk Strategy 怎样选择？Fixed、Recursive、Semantic、Parent-child、Structure-aware 分别适合什么数据？ |
| `RAG-008` | RAG | Chunk Parameters | L3 | 12 | 🔥🔥🔥 | Chunk Size / Overlap 如何设置？参数怎样通过 Dataset / Experiment 验证，而不是照抄默认值？ |
| `RAG-009` | RAG | Semantic Boundary Failure | L4 | 7 | 🔥🔥 | Chunk 把强逻辑关系、充分必要条件或跨块上下文切断时，怎样修复 Semantic Boundary Failure？ |
| `RAG-010` | RAG | Query Transformation | L4 | 18 | 🔥🔥🔥 | Query Rewrite / Decomposition / Multi-query / Intent / Clarification 怎样改善 Retrieval？什么时候应该先向用户追问？ |
| `RAG-011` | RAG | No-hit / Refusal | L3 | 6 | 🔥🔥 | Retrieval Miss / No-hit 如何定义？阈值怎样设置，何时拒答、澄清或走 Fallback？ |
| `RAG-012` | RAG | Dense vs Sparse / BM25 | L3 | 15 | 🔥🔥🔥 | Dense Retrieval 与 Keyword / BM25 Sparse Retrieval 各擅长什么？为什么专有名词、短 Query、精确条款会暴露纯向量短板？ |
| `RAG-013` | RAG | Hybrid Retrieval | L4 | 25 | 🔥🔥🔥 | 为什么要做 Hybrid Retrieval？Dense / Sparse / Multi-way Retrieval 的结果怎样融合并验证收益？ |
| `RAG-014` | RAG | Fusion / RRF | L3 | 10 | 🔥🔥🔥 | RRF / Fusion 为什么常用于多路召回？为什么不简单线性加权，参数怎样调？ |
| `RAG-015` | RAG | Reranking | L4 | 22 | 🔥🔥🔥 | 为什么需要 Rerank？如何平衡 Precision、Latency、Cost，并定位“Rerank 反而变差”？ |
| `RAG-016` | RAG | Top-K | L3 | 10 | 🔥🔥🔥 | Retrieval / Rerank Top-K 怎样设置？K 在 Recall、Context Noise、Latency 与 Token Cost 之间如何取舍？ |
| `RAG-017` | RAG | Context Construction | L4 | 7 | 🔥🔥 | Retrieval Evidence 怎样组装进 LLM Context？标题、Metadata、邻居块、来源与排序怎样影响回答？ |
| `RAG-018` | RAG | Grounding / Citation | L4 | 3 | 🔥 | 最终回答怎样做 Grounding / Citation / Reference Mapping，保证结论能回到真实证据？ |
| `RAG-019` | RAG | Bad Case Attribution | L4 | 19 | 🔥🔥🔥 | RAG Bad Case / Hallucination 出现时，怎样区分 Parsing、Chunk、Embedding、Retrieval、Rerank、Prompt、Generation、Runtime 问题？ |
| `RAG-020` | RAG | Retrieval Metrics | L3 | 16 | 🔥🔥🔥 | 怎样定义 Retrieval Quality：Recall、Precision、Hit Rate、MRR / NDCG 等指标分别回答什么问题？ |
| `RAG-021` | RAG | RAG Evaluation | L4 | 21 | 🔥🔥🔥 | RAG 质量怎样做 End-to-end Evaluation？Retrieval、Faithfulness、Answer Relevance / Correctness 怎样分层？ |
| `RAG-022` | RAG | Evaluation Dataset / Judge | L4 | 9 | 🔥🔥 | Evaluation Dataset / Ground Truth 从哪里来？怎样代表线上真实 Query，并避免 LLM Judge 自身不可靠？ |
| `RAG-023` | RAG | Experiment Design | L4 | 8 | 🔥🔥 | 怎样用 Baseline / Ablation / A-B Experiment 证明 Chunk、Hybrid、Rerank、GraphRAG 等优化的真实收益？ |
| `RAG-024` | RAG | Incremental Update / Freshness | L4 | 13 | 🔥🔥🔥 | Knowledge Base 怎样做增量更新、版本管理、旧数据清理和在线新鲜度保障？ |
| `RAG-025` | RAG | Permission / Security | L4 | 3 | 🔥 | 企业 RAG 怎样做 Permission / Tenant Filtering，防止检索到用户无权读取的知识？ |
| `RAG-026` | RAG | Large-scale RAG | L4 | 4 | 🔥🔥 | 百 GB / TB 级语料怎样做 Ingestion、Embedding、Index Build、并行处理与成本控制？ |
| `RAG-027` | RAG | Latency / Cost | L4 | 8 | 🔥🔥 | RAG Latency / Cost 的主要瓶颈在哪里？Parse、Embedding、Retrieve、Rerank、LLM、Cache 各层怎样优化？ |
| `RAG-028` | RAG | GraphRAG | L4 | 8 | 🔥🔥 | GraphRAG / Knowledge Graph Retrieval 相比普通 Vector RAG 解决什么问题？Triple / Community / Graph Update 怎样保证质量？ |
| `RAG-029` | RAG | Agentic RAG | L4 | 6 | 🔥🔥 | Agentic RAG 与固定 One-shot RAG 有什么区别？什么时候让 Agent 主动决定检索、重写、继续检索或停止？ |
| `AGENT-001` | Agent Harness / Runtime | Agent Boundary | L3 | 30 | 🔥🔥🔥 | Agent 与普通 LLM Call / Chatbot / 固定 Workflow 的本质区别是什么？什么任务真正值得 Agent 化？ |
| `AGENT-002` | Agent Harness / Runtime | Harness / Runtime Boundary | L3 | 25 | 🔥🔥🔥 | Harness、Runtime、Orchestrator / Workflow Engine 分别解决什么问题？为什么“模型 + API”还不够？ |
| `AGENT-003` | Agent Harness / Runtime | Agent Loop | L3 | 36 | 🔥🔥🔥 | 一个完整 Agent Loop / Runtime 从 User Input 到 Final Answer 怎样执行？Model、Tool、State、Context 各在哪一层？ |
| `AGENT-004` | Agent Harness / Runtime | Message / Event Model | L3 | 8 | 🔥🔥 | Agent Message / Event Model 应怎样设计？Assistant Text、Tool Call、Tool Result、System / User Message 为什么需要不同结构？ |
| `AGENT-005` | Agent Harness / Runtime | Agent Paradigm | L3 | 31 | 🔥🔥🔥 | ReAct、Plan-Execute-Replan、Planner / Executor / Critic 等执行范式怎样选择？ |
| `AGENT-006` | Agent Harness / Runtime | Termination / Loop Detection | L4 | 15 | 🔥🔥🔥 | Agent 怎样判断任务已经完成并可靠停止？Max Step、Stop Condition、Dead Loop / Oscillation 如何检测？ |
| `AGENT-007` | Agent Harness / Runtime | Goal Control | L4 | 4 | 🔥🔥 | Agent Goal Drift / 执行方向偏离原始需求时，怎样发现并拉回主任务？ |
| `AGENT-008` | Agent Harness / Runtime | Context Assembly | L4 | 16 | 🔥🔥🔥 | 一次 Agent Context 包含什么？System / User、History、Memory、Retrieval、Tool Schema、Tool Result 怎样排序与组装？ |
| `AGENT-009` | Agent Harness / Runtime | Context Compaction | L4 | 41 | 🔥🔥🔥 | Context Window 接近上限时，怎样 Trim / Summarize / Compact，同时保留当前任务关键状态？ |
| `AGENT-010` | Agent Harness / Runtime | Compaction Correctness | L4 | 15 | 🔥🔥🔥 | Compaction / Summary 后如何验证信息没有丢坏？哪些状态必须保留，错误摘要如何纠正？ |
| `AGENT-011` | Agent Harness / Runtime | Large Tool Result / Context Offloading | L4 | 11 | 🔥🔥🔥 | Tool Result / 文件 / 日志过大时怎样压缩、引用、延迟加载或外部化，而不是全部塞进 Context？ |
| `AGENT-012` | Agent Harness / Runtime | Prompt / Context Cache | L4 | 5 | 🔥🔥 | Prompt Cache / Context Cache 如何降低重复 Token 成本？缓存哪些层，何时失效？ |
| `AGENT-014` | Agent Harness / Runtime | Memory Architecture | L4 | 36 | 🔥🔥🔥 | Short-term / Working / Long-term Memory 怎样分层、写入、召回、更新与失效？ |
| `AGENT-015` | Agent Harness / Runtime | Memory Lifecycle | L4 | 8 | 🔥🔥 | Memory 什么时候从短期晋升长期？怎样做 Extraction / Consolidation / Retrieval-on-demand，而不是无限堆历史？ |
| `AGENT-016` | Agent Harness / Runtime | Memory Correctness / Staleness | L4 | 6 | 🔥🔥 | Long-term Memory 中过期摘要、错误事实或冲突信息如何发现、修正、版本化并避免污染后续决策？ |
| `AGENT-017` | Agent Harness / Runtime | Multi-tenant State Isolation | L4 | 10 | 🔥🔥🔥 | 多用户 / 多角色 / 多 Tenant 的 Memory、Context、Session 和权限怎样隔离？ |
| `AGENT-018` | Agent Harness / Runtime | Tool Calling Protocol | L3 | 29 | 🔥🔥🔥 | Tool / Function Calling 从 Schema 暴露、模型选择、Structured Call、Runtime 执行到 Result 回填的完整链路是什么？ |
| `AGENT-019` | Agent Harness / Runtime | Tool Lifecycle | L4 | 10 | 🔥🔥🔥 | 一个新 Tool 从定义、注册、Discovery、Schema Validation、调用到版本升级的生命周期怎样设计？ |
| `AGENT-020` | Agent Harness / Runtime | Tool Call Failure Semantics | L4 | 27 | 🔥🔥🔥 | 单次 Tool Call 出现 Invalid Arguments / Invalid Schema / Permission / Execution / Timeout 等失败时，Runtime 怎样归一化错误、反馈给模型并决定 Repair / Retry / Fail？ |
| `AGENT-021` | Agent Harness / Runtime | Tool Discovery / Progressive Loading | L4 | 20 | 🔥🔥🔥 | Tool 数量持续增长时怎样 Dynamic Discovery / Progressive Loading，避免所有 Schema 一次性挤占 Context？ |
| `AGENT-022` | Agent Harness / Runtime | Structured Output / Validation | L4 | 11 | 🔥🔥🔥 | Structured Output / Tool Arguments 如何做 Schema Validation、Repair 与 Hallucination Handling？ |
| `AGENT-023` | Agent Harness / Runtime | MCP Protocol | L3 | 20 | 🔥🔥🔥 | MCP 解决什么标准化问题？Client / Server、Tools / Resources / Prompts 与 stdio / SSE / Streamable HTTP 怎样理解？ |
| `AGENT-024` | Agent Harness / Runtime | Capability Abstraction Boundary | L4 | 34 | 🔥🔥🔥 | Skill、Tool、Function Calling、MCP、Rule / Prompt / Workflow 的职责边界是什么？ |
| `AGENT-025` | Agent Harness / Runtime | Skill Progressive Disclosure | L4 | 10 | 🔥🔥🔥 | Skill 怎样做 Progressive Disclosure / Resource Loading？为什么不把所有 Instructions / Assets 一次性注入 Context？ |
| `AGENT-026` | Agent Harness / Runtime | Cancellation / Long-running Task | L4 | 10 | 🔥🔥🔥 | Agent 长耗时任务怎样 Timeout、Cancel、Interrupt、Resume？取消传播和资源清理怎样保证？ |
| `AGENT-027` | Agent Harness / Runtime | Checkpoint / Resume | L4 | 12 | 🔥🔥🔥 | Checkpoint / Persistence / Resume 应保存哪些 Runtime State？Crash 后怎样恢复到可继续执行状态？ |
| `AGENT-028` | Agent Harness / Runtime | Permission / Approval / Sandbox | L4 | 20 | 🔥🔥🔥 | Permission、Approval、HITL、Sandbox 如何限制 Agent 的写操作、代码执行和高风险外部副作用？ |
| `AGENT-029` | Agent Harness / Runtime | Idempotency / External Side Effect | L4 | 6 | 🔥🔥 | Tool 已成功产生外部副作用，但 Checkpoint / DB 写失败或服务崩溃时，如何避免 Resume 后重复执行？ |
| `AGENT-030` | Agent Harness / Runtime | Multi-Agent Architecture | L4 | 29 | 🔥🔥🔥 | 什么时候使用 Multi-Agent / Sub-agent？怎样分工、通信、共享或隔离 Context / State？ |
| `AGENT-031` | Agent Harness / Runtime | Workspace / Shared-resource Concurrency | L4 | 7 | 🔥🔥 | 多 Agent 并行修改同一文件 / Workspace 或共享资源时，如何避免 Conflict、Race、Lost Update？ |
| `AGENT-032` | Agent Harness / Runtime | Model Routing / Runtime Adapter | L4 | 9 | 🔥🔥 | Agent Runtime 怎样做 Model Routing？不同 Provider 的 Tool Protocol、Context 与错误语义如何适配？ |
| `AGENT-034` | Agent Harness / Runtime | Agent Evaluation | L4 | 27 | 🔥🔥🔥 | Agent / Harness 怎样做 Evaluation？如何把 Final Result、Process、Tool、Routing、Cost 与 Regression 分层验证？ |
| `AGENT-035` | Agent Harness / Runtime | Benchmark Engineering | L4 | 12 | 🔥🔥🔥 | Agent Benchmark / Eval Dataset / Ground Truth 怎样构建？如何让 Offline Case 代表真实线上任务并用于 Regression？ |
| `AGENT-036` | Agent Harness / Runtime | Code Verification | L4 | 24 | 🔥🔥🔥 | AI / Coding Agent 生成代码后，怎样用 Test、Diff、Regression、Review、Rollback 证明结果可交付？ |
| `AGENT-037` | Agent Harness / Runtime | Repository Understanding | L4 | 9 | 🔥🔥 | Coding Agent 怎样理解大型 Repository？Vector RAG、AST / LSP、ripgrep / Filesystem Search、Dependency Graph 各适合什么？ |
| `AGENT-038` | Agent Harness / Runtime | Agent Runtime Resilience Policy | L4 | 15 | 🔥🔥🔥 | Agent Runtime 如何制定跨 Model / Tool / Provider 的 Resilience Policy？Retry Eligibility、Backoff、Circuit Breaker、Fallback / Model Failover 应怎样组合？ |
| `AGENT-041` | Agent Harness / Runtime | Self-evolution / Data Flywheel | L4 | 6 | 🔥🔥 | Agent Self-evolution / Data Flywheel 怎样闭环？Bad Case、数据采集、Metric、上线验证与 Rollback 如何设计？ |
| `AGENT-042` | Agent Harness / Runtime | Dynamic Instruction / Steering | L4 | 1 | 单点真实信号 | Agent 正在执行时用户追加 / 修改需求，新指令怎样进入当前 State，并安全影响后续 Planning / Execution？ |
| `AGENT-043` | Agent Harness / Runtime | Execution Trace / Observability | L4 | 7 | 🔥🔥 | Agent Runtime 怎样建立 step / model / tool / state 级 Trace 与 Observability？如何用执行轨迹定位卡住、失败、延迟和 Token 异常，并支持 Replay / Debug？ |
| `AGENT-044` | Agent Harness / Runtime | Prompt Injection / Untrusted Context Security | L4 | 8 | 🔥🔥 | Agent 如何防 Prompt Injection / Prompt Attack 与 Untrusted Context 污染？System Prompt 泄露、Tool 诱导、敏感数据外泄和高风险写操作应怎样分层防护？ |
| `AGENT-045` | Agent Harness / Runtime | Intent Recognition / Routing | L4 | 11 | 🔥🔥🔥 | Agent 的 Intent Recognition / Router 怎样设计？Rule、Small Model、LLM Classification 与 Tool-schema 自主选择如何取舍，准确率低和标注数据少时怎样优化？ |
| `AGENT-046` | Agent Harness / Runtime | A2A / Agent Communication Protocol | L3 | 6 | 🔥🔥 | A2A / Agent-to-Agent Protocol 解决什么问题？它与 MCP、Sub-agent 内部调用和普通服务通信有什么边界，怎样避免递归互调与失控？ |
| `AGENT-047` | Agent Harness / Runtime | Agent Framework Selection | L3 | 27 | 🔥🔥🔥 | LangChain、LangGraph、Spring AI 等 Agent / Orchestration Framework 分别提供什么能力？什么时候需要 State Graph，什么时候应部分或完全自研 Runtime？ |
| `AGENT-048` | Agent Harness / Runtime | AI-assisted Development Workflow | L4 | 37 | 🔥🔥🔥 | AI-assisted / Vibe Coding 应怎样进入真实软件研发流程？从 Requirement、Context、生成与迭代到 Test、Review、Diff、验收和交付，人和 Coding Agent 的责任边界怎样划分？ |
| `SD-001` | System Design | Flash Sale / Inventory | L4 | 10 | 🔥🔥🔥 | 设计秒杀 / 抢购 / 库存系统：怎样防止 Oversell / Undersell，并处理 Redis、DB、订单和补偿的一致性？ |
| `SD-002` | System Design | Realtime Ranking | L4 | 2 | 🔥 | 设计高并发排行榜 / 热榜：实时更新、HotKey、排序、读取热点与持久化怎样拆？ |
| `SD-003` | System Design | Autocomplete / Fuzzy Search | L4 | 2 | 🔥 | 设计搜索框实时联想 / 模糊搜索：如何同时支持代码、名称、拼音 / Prefix / Infix，并控制实时交互成本？ |
| `SD-004` | System Design | Feed System | L4 | 1 | 单点真实信号 | 设计 Feed / 关注流：如何让用户快速看到关注对象的新内容，并处理 Fan-out、热点和分页？ |
| `SD-005` | System Design | Notification Platform | L4 | 1 | 单点真实信号 | 设计 Notification Platform：怎样处理可靠投递、Retry、Dedup、状态与多通道扩展？ |
| `SD-006` | System Design | Large-scale Storage | L4 | 1 | 单点真实信号 | 设计每天约 10TB 数据的 Storage + Time-range Query Service：Hot / Cold Data、Index、API 与容量怎样组织？ |
| `SD-007` | System Design | Batch Processing / Migration | L4 | 4 | 🔥🔥 | 设计大规模批处理 / 数据迁移：数千万行或 20 万行 Excel 怎样分页、流式、并发、断点恢复并限制 DB 压力？ |
| `SD-008` | System Design | Massive-set Processing | L4 | 1 | 单点真实信号 | 设计大规模 IP / ID Whitelist 或 Dedup Service：海量去重、Memory Estimation 与在线查询怎样权衡？ |
| `SD-009` | System Design | Distributed Rate Limiter | L4 | 2 | 🔥 | 设计 Distributed Rate Limiter：怎样处理全局配额、低延迟、一致性、故障与下游容量约束？ |
| `SD-010` | System Design | Token Refresh Coordination | L4 | 1 | 单点真实信号 | 设计多实例 Access Token / Refresh Token 缓存：怎样避免 Refresh Stampede，并处理失败、旧 Token 与实例崩溃？ |
| `SD-011` | System Design | QR Login | L4 | 2 | 🔥 | 设计二维码登录：二维码生成、手机确认、PC 状态同步、Token / Session 建立和安全边界怎样组织？ |
| `SD-012` | System Design | Large-file Processing | L4 | 3 | 🔥 | 设计大文件 / 长视频上传与处理系统：分片、断点续传、异步任务、状态查询和失败恢复怎样实现？ |
| `SD-013` | System Design | LLM Gateway | L4 | 3 | 🔥 | 设计统一 Model / LLM Gateway：多 Provider Schema、Routing、Streaming、Rate Limit、Cost、Failover 和 Observability 怎样组织？ |
| `SD-014` | System Design | Multi-tenant Agent Platform | L4 | 5 | 🔥🔥 | 设计多租户 AI / Agent Platform：用户、Workspace、Permission、Resource Isolation、Usage / Cost 与 Agent Routing 怎样治理？ |
| `SD-015` | System Design | Secure Multi-tenant Compute | L4 | 1 | 单点真实信号 | 设计受限资源的多租户计算平台：SGX / EPC 等资源不足时怎样做安全隔离、Scheduling 与性能治理？ |
| `SD-016` | System Design | Enterprise RAG | L4 | 6 | 🔥🔥 | 从零设计 Enterprise Knowledge-base QA / RAG Service：Ingestion、Permission、Retrieval、Generation、Evaluation 与 Update 怎样组织？ |
| `SD-017` | System Design | Large-scale Document RAG | L4 | 1 | 单点真实信号 | 面对 600GB–1TB PDF / 扫描件语料，怎样设计垂直 RAG：解析、Embedding 成本、Index、Hybrid Retrieval 与 Incremental Update 如何扩展？ |
| `SD-018` | System Design | Analytical Agent | L4 | 1 | 单点真实信号 | 设计 Financial / Data Analysis Agent：从自然语言问题到检索、计算、结论 Verification 与 Citation 怎样闭环？ |
| `SD-019` | System Design | Customer Service Agent | L4 | 4 | 🔥🔥 | 设计 AI Customer Service Agent：Intent、RAG、订单 / 业务 Tool、Memory、Human Handoff 与高风险操作怎样分层？ |
| `SD-020` | System Design | Multimodal Document Agent | L4 | 2 | 🔥 | 设计 Multi-modal Document / PDF → HTML Agent Workflow：文字、图片、表格、知识核对与图文输出怎样保持可追溯？ |
| `SD-021` | System Design | Agent Backend | L4 | 13 | 🔥🔥🔥 | 从零设计 Production Agent Backend：Loop、State、Tool、Memory、Checkpoint、Streaming、Auth、Observability 与 Scale 怎样组合？ |
| `SD-022` | System Design | Long-running Agent | L4 | 10 | 🔥🔥🔥 | 设计 Long-running Agent Runtime：数小时 / 数天任务怎样做 Checkpoint、Resume、Cancel、Idempotency、外部副作用和状态迁移？ |
| `SD-023` | System Design | Game Agent | L4 | 3 | 🔥 | 设计 Game / Interactive Agent：Goal、State、Action / Tool、Memory、Evaluation 与安全边界怎样映射具体游戏业务？ |
| `SD-024` | System Design | Content Creation Agent | L4 | 2 | 🔥 | 设计 AI 自动内容创作 / 视频编辑 Agent：Planning、SubAgent、素材状态、人物一致性、长任务和 Evaluation 怎样闭环？ |
