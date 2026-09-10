# Redis Canonical Questions — S001–S279 全库纵向扫描 v2

更新日期：2026-09-10

> 一级板块：**Redis**。本文件只保留 Redis 自身的数据结构、内存 / 过期、持久化、高可用、Cluster、分布式锁、Lua、Cache 与 Redis-specific Runtime 用法。通用的 DB+Cache Consistency、Rate Limit 算法、Agent Checkpoint、MQ 选型等已迁移到更合适的一级板块。
>
> 本文件所有 ACTIVE 条目的 `Primary Module = Redis`。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**19**
- MOVED：**5**（旧 `REDIS-001`, `015`, `018`, `020`, `023`）
- 证据范围：仅 `S001–S279`
- 当前版本：`v2`（十板块归属审计版）

### 高频信号

- `REDIS-012` · 25：Distributed Lock 基础与正确性
- `REDIS-007` · 20：Penetration / Breakdown / Avalanche
- `REDIS-002` · 17：Data Structures 与场景选型
- `REDIS-013` · 14：Lock Expire / Renewal / Owner / Lua / RedLock
- `REDIS-008` · 11：BigKey / HotKey
- `REDIS-017` · 11：Redis Session / Conversation / Auth Cache
- `REDIS-014` · 10：Lua / Atomicity
- `REDIS-010` · 8：Primary-Replica / Sentinel / Cluster

---

## 2. ACTIVE Canonical Questions

### REDIS-002 · Redis 常见数据结构 String / Hash / List / Set / ZSet 各自适合什么场景，底层特性怎样影响选型？
- **Topic**：Data Structures
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**18**
- **Evidence Sources**：`S010`, `S070`, `S079`, `S086`, `S100`, `S110`, `S131`, `S148`, `S154`, `S188`, `S190`, `S191`, `S200`, `S201`, `S204`, `S234`, `S262`, `S273`

### REDIS-003 · Redis 为什么快？“单线程”到底指什么，命令执行、网络 I/O 与后台任务怎样理解？
- **Topic**：Performance / Thread Model
- **Question Type**：Why / Concept
- **Depth**：L2
- **Source Count**：**7**
- **Evidence Sources**：`S036`, `S112`, `S174`, `S188`, `S201`, `S234`, `S274`

### REDIS-004 · Redis 的 I/O Multiplexing / Event Loop 如何工作？它与 NIO / Reactor 有什么关系？
- **Topic**：I/O Multiplexing
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Source Count**：**1**
- **Evidence Sources**：`S036`
- **Related Modules**：AI Backend Engineering

### REDIS-005 · Redis TTL、过期删除与 Lazy / Active Expiration 怎样工作？TTL 应怎样设置？
- **Topic**：TTL / Expiration
- **Question Type**：Concept / Trade-off
- **Depth**：L2
- **Source Count**：**7**
- **Evidence Sources**：`S035`, `S081`, `S198`, `S225`, `S234`, `S262`, `S263`

### REDIS-006 · Redis 内存不足时有哪些 Eviction Policy？LRU / LFU 等策略怎样选择，淘汰后热点 Key 立即回流怎么办？
- **Topic**：Eviction
- **Question Type**：Concept / Scenario
- **Depth**：L3
- **Source Count**：**5**
- **Evidence Sources**：`S131`, `S188`, `S200`, `S234`, `S262`

### REDIS-007 · Cache Penetration、Breakdown / Stampede、Avalanche 分别是什么？怎样用 Bloom Filter、互斥、随机 TTL 等治理？
- **Topic**：Cache Failure Patterns
- **Question Type**：Concept / Troubleshoot
- **Depth**：L3
- **Source Count**：**20**
- **Evidence Sources**：`S013`, `S040`, `S084`, `S091`, `S093`, `S116`, `S131`, `S148`, `S154`, `S174`, `S194`, `S200`, `S203`, `S214`, `S225`, `S234`, `S254`, `S266`, `S267`, `S273`

### REDIS-008 · BigKey 与 HotKey 怎样发现、治理和拆分？迁移 / 删除过程中怎样避免阻塞与一致性问题？
- **Topic**：BigKey / HotKey
- **Question Type**：Troubleshoot / System Design
- **Depth**：L4
- **Source Count**：**11**
- **Evidence Sources**：`S014`, `S049`, `S070`, `S094`, `S131`, `S148`, `S188`, `S204`, `S214`, `S262`, `S273`

### REDIS-009 · RDB 与 AOF 的原理、恢复特性和取舍是什么？Redis 故障后怎样恢复数据？
- **Topic**：Persistence
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**4**
- **Evidence Sources**：`S110`, `S188`, `S201`, `S251`

### REDIS-010 · Redis Primary/Replica、Sentinel、Cluster 的职责和高可用边界分别是什么？
- **Topic**：High Availability
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Source Count**：**8**
- **Evidence Sources**：`S005`, `S110`, `S116`, `S188`, `S195`, `S200`, `S234`, `S278`

### REDIS-011 · Redis Cluster 的 Hash Slot、Sharding、扩缩容与数据迁移如何工作？Lua / Multi-key 为什么受 Slot 约束？
- **Topic**：Cluster / Hash Slot
- **Question Type**：Concept / System Design
- **Depth**：L4
- **Source Count**：**5**
- **Evidence Sources**：`S005`, `S014`, `S195`, `S247`, `S278`

### REDIS-012 · Redis 分布式锁的基本实现是什么？正确性需要满足哪些条件？
- **Topic**：Distributed Lock Basics
- **Question Type**：Concept / Why
- **Depth**：L2
- **Source Count**：**25**
- **Evidence Sources**：`S023`, `S025`, `S035`, `S040`, `S070`, `S084`, `S091`, `S093`, `S105`, `S116`, `S148`, `S154`, `S169`, `S188`, `S198`, `S201`, `S212`, `S225`, `S234`, `S251`, `S262`, `S264`, `S266`, `S273`, `S279`

### REDIS-013 · Redis Lock 的 Expire、Renewal / WatchDog、Owner 校验、Lua Release、RedLock 与故障窗口怎样处理？
- **Topic**：Distributed Lock Correctness
- **Question Type**：Deep Dive / Failure Analysis
- **Depth**：L4
- **Source Count**：**14**
- **Evidence Sources**：`S023`, `S035`, `S070`, `S093`, `S105`, `S116`, `S148`, `S169`, `S188`, `S198`, `S201`, `S212`, `S262`, `S264`

### REDIS-014 · Lua Script 为什么适合 Redis 原子业务？库存扣减、限流、锁释放等场景如何设计？
- **Topic**：Lua / Atomicity
- **Question Type**：Why / Scenario
- **Depth**：L3
- **Source Count**：**10**
- **Evidence Sources**：`S010`, `S035`, `S070`, `S086`, `S114`, `S198`, `S214`, `S247`, `S277`, `S279`

### REDIS-016 · Local Cache + Redis 多级缓存怎样分工？如何处理热 Key、失效风暴和缓存层级间的一致性？
- **Topic**：Multi-level Cache
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S094`, `S118`, `S194`, `S222`, `S276`, `S277`
- **Related Modules**：AI Backend Engineering

### REDIS-017 · Redis 如何承载 Session / Conversation / Auth Cache？多实例下怎样处理过期、隔离与共享？
- **Topic**：Session / Conversation
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**11**
- **Evidence Sources**：`S033`, `S035`, `S081`, `S091`, `S105`, `S119`, `S171`, `S178`, `S194`, `S207`, `S262`
- **Related Modules**：AI Backend Engineering, Agent Harness / Runtime

### REDIS-019 · Redis 如何具体实现 Sliding Window / Token Bucket 等限流？ZSet / Counter / Lua / TTL 怎样保证原子性与性能？
- **Topic**：Redis Rate Limit Implementation
- **Question Type**：System Design / Implementation
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S035`, `S069`, `S084`, `S164`, `S174`, `S198`, `S209`, `S270`
- **Related Modules**：AI Backend Engineering

### REDIS-021 · 语义缓存、查询结果缓存与普通业务 Cache 有什么不同？什么结果值得缓存，如何避免陈旧答案？
- **Topic**：Semantic / Result Cache
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**2**
- **Evidence Sources**：`S081`, `S250`
- **Related Modules**：RAG, Agent Harness / Runtime

### REDIS-022 · Redis 有哪些安全风险？无密码实例、越权访问与敏感状态怎样防护？
- **Topic**：Security
- **Question Type**：Security / System Design
- **Depth**：L4
- **Source Count**：**1**
- **Evidence Sources**：`S254`
- **Related Modules**：AI Backend Engineering

### REDIS-024 · Redis 与 Aerospike 等 KV Store 在存储模型、容量、延迟和业务场景上怎样选型？
- **Topic**：KV Store Selection
- **Question Type**：Comparison
- **Depth**：L2
- **Source Count**：**1**
- **Evidence Sources**：`S270`

---

## 3. MOVED：新十板块归属修正

| Legacy QID | 原问题 | 新 Primary Canonical |
|---|---|---|
| `REDIS-001` | MySQL / Redis 数据分层 | `AIBE-039` |
| `REDIS-015` | DB + Cache Consistency | `AIBE-020` |
| `REDIS-018` | Agent Runtime State / Checkpoint | `AGENT-027`, `AGENT-029`, `SD-022` |
| `REDIS-020` | Token Budget / Fair Queue | `AIBE-017`, `AIBE-013` |
| `REDIS-023` | Redis vs MQ | `AIBE-014` |

通用 Rate Limit 算法选择归 `AIBE-017`；本文件的 `REDIS-019` 只保留 Redis 具体实现层。
