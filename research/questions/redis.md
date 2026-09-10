# Redis Canonical Questions — S001–S279 全库纵向扫描 v1

更新日期：2026-09-10

> 本文件只提炼冻结 HUMAN-A 语料中的 Redis 真实考察信号。它不是 Redis 教材目录；后续课程仍会从数据结构、线程/I/O模型、持久化、高可用到 AI Runtime 场景完整建立知识体系。

## 1. 当前扫描结论

- Canonical Questions：**24** 道
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数，同一来源内同主题连续追问不重复计数
- 当前版本：`v1`；五大核心模块完成后做跨模块 Merge / Split 二次审计

### 高频信号

- **REDIS-012** · 25 个来源 · 🔥🔥🔥：Redis 分布式锁的基本实现是什么？正确性需要满足哪些条件？
- **REDIS-007** · 20 个来源 · 🔥🔥🔥：Cache Penetration、Breakdown / Stampede、Avalanche 分别是什么？怎样用 Bloom Filter、互斥、随机 TTL 等治理？
- **REDIS-015** · 20 个来源 · 🔥🔥🔥：Redis 与 MySQL 双写怎样保证最终一致性？Cache Aside、删除缓存、延迟双删和补偿怎样处理故障窗口？
- **REDIS-002** · 17 个来源 · 🔥🔥🔥：Redis 常见数据结构 String / Hash / List / Set / ZSet 各自适合什么场景，底层特性怎样影响选型？
- **REDIS-013** · 14 个来源 · 🔥🔥🔥：Redis Lock 的 Expire、Renewal / WatchDog、Owner 校验、Lua Release、RedLock 与故障窗口怎样处理？
- **REDIS-008** · 11 个来源 · 🔥🔥🔥：BigKey 与 HotKey 怎样发现、治理和拆分？迁移 / 删除过程中怎样避免阻塞与一致性问题？
- **REDIS-017** · 11 个来源 · 🔥🔥🔥：Redis 如何承载 Session / Conversation / Auth Cache？多实例下怎样保证会话一致、隔离和过期？
- **REDIS-001** · 10 个来源 · 🔥🔥🔥：MySQL 与 Redis 在 AI 应用中怎样分工？哪些数据应长期持久化，哪些适合 Cache / Session / Runtime State？
- **REDIS-014** · 10 个来源 · 🔥🔥🔥：Lua Script 为什么适合 Redis 原子业务？库存扣减、限流、锁释放等场景如何设计？
- **REDIS-010** · 8 个来源 · 🔥🔥：Redis Primary/Replica、Sentinel、Cluster 的职责和高可用边界分别是什么？
- **REDIS-019** · 8 个来源 · 🔥🔥：如何用 Redis 做 Rate Limit？Fixed Window、Sliding Window、Token Bucket / Leaky Bucket 怎样选？
- **REDIS-003** · 7 个来源 · 🔥🔥：Redis 为什么快？“单线程”到底指什么，命令执行、网络 I/O 与后台任务如何理解？

---

## 2. Canonical Questions

### REDIS-001 · MySQL 与 Redis 在 AI 应用中怎样分工？哪些数据应长期持久化，哪些适合 Cache / Session / Runtime State？

- **Topic**：Data Layering
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S090`, `S092`, `S097`, `S118`, `S178`, `S181`, `S194`, `S212`, `S214`, `S273`

**真实问法变体：**
- Redis 与 MySQL 分别适合存什么？
- Chat History / Session 为什么会同时涉及 Redis 和 MySQL？
- Agent / AI Backend 中 Cache、临时状态和长期业务事实怎样分层？

### REDIS-002 · Redis 常见数据结构 String / Hash / List / Set / ZSet 各自适合什么场景，底层特性怎样影响选型？

- **Topic**：Data Structures
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**17**
- **Evidence Sources**：`S010`, `S070`, `S079`, `S086`, `S100`, `S110`, `S131`, `S148`, `S154`, `S188`, `S191`, `S200`, `S201`, `S204`, `S234`, `S262`, `S273`

**真实问法变体：**
- Redis 有哪些常用数据结构？
- ZSet 底层和典型用途是什么？
- 业务场景应该怎样选择 Hash / Set / ZSet？

### REDIS-003 · Redis 为什么快？“单线程”到底指什么，命令执行、网络 I/O 与后台任务如何理解？

- **Topic**：Performance / Thread Model
- **Question Type**：Why / Concept
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S036`, `S112`, `S174`, `S188`, `S201`, `S234`, `S274`

**真实问法变体：**
- Redis 为什么快？
- Redis 真的是单线程吗？
- 单线程执行命令为什么仍然能支撑高吞吐？

### REDIS-004 · Redis 的 I/O Multiplexing / Event Loop 如何工作？它与 NIO / Reactor 的关系是什么？

- **Topic**：I/O Multiplexing
- **Question Type**：Concept / Deep Dive
- **Depth**：L3
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S036`

**真实问法变体：**
- Redis I/O 多路复用怎样理解？
- NIO / Reactor 与 Redis 网络模型有什么关系？

### REDIS-005 · Redis TTL、过期删除与 Lazy / Active Expiration 怎样工作？TTL 应怎样设置？

- **Topic**：TTL / Expiration
- **Question Type**：Concept / Trade-off
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S035`, `S081`, `S198`, `S225`, `S234`, `S262`, `S263`

**真实问法变体：**
- TTL 应该怎么设？
- 大量 Key 同时过期会发生什么？
- Lazy Refresh 与 TTL 有什么区别？

### REDIS-006 · Redis 内存不足时有哪些 Eviction Policy？LRU / LFU 等策略如何选择，淘汰后热点 Key 立即回流怎么办？

- **Topic**：Eviction
- **Question Type**：Concept / Scenario
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S131`, `S188`, `S200`, `S234`, `S262`

**真实问法变体：**
- Redis 淘汰策略有哪些？
- 内存不足时怎么选 Eviction Policy？
- 刚被 LRU 淘汰的 Key 又立刻被请求怎么办？

### REDIS-007 · Cache Penetration、Breakdown / Stampede、Avalanche 分别是什么？怎样用 Bloom Filter、互斥、随机 TTL 等治理？

- **Topic**：Cache Failure Patterns
- **Question Type**：Concept / Troubleshoot
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**20**
- **Evidence Sources**：`S013`, `S040`, `S084`, `S091`, `S093`, `S116`, `S131`, `S148`, `S154`, `S174`, `S194`, `S200`, `S203`, `S214`, `S225`, `S234`, `S254`, `S266`, `S267`, `S273`

**真实问法变体：**
- 缓存穿透 / 击穿 / 雪崩有什么区别？
- 热点 Key 过期时怎样避免请求瞬间压向数据库？
- Bloom Filter 有误判时，恶意不存在 ID 流量怎么处理？

### REDIS-008 · BigKey 与 HotKey 怎样发现、治理和拆分？迁移 / 删除过程中怎样避免阻塞与一致性问题？

- **Topic**：BigKey / HotKey
- **Question Type**：Troubleshoot / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S014`, `S049`, `S070`, `S094`, `S131`, `S148`, `S188`, `S204`, `S214`, `S262`, `S273`

**真实问法变体：**
- BigKey 是什么，怎么发现？
- HotKey 怎么治理？
- Hash BigKey 拆分 / 迁移时如何保证一致性？

### REDIS-009 · RDB 与 AOF 的原理、恢复特性和取舍是什么？Redis 故障后怎样恢复数据？

- **Topic**：Persistence
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S110`, `S188`, `S201`, `S251`

**真实问法变体：**
- Redis 有哪些持久化方式？
- RDB / AOF 各自优缺点是什么？
- Redis 节点故障后数据如何恢复？

### REDIS-010 · Redis Primary/Replica、Sentinel、Cluster 的职责和高可用边界分别是什么？

- **Topic**：High Availability
- **Question Type**：Concept / Comparison
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S005`, `S110`, `S116`, `S188`, `S195`, `S200`, `S234`, `S278`

**真实问法变体：**
- Sentinel 与 Cluster 有什么区别？
- 主从复制如何保证高可用？
- Redis 单节点、主从、Cluster 怎样选？

### REDIS-011 · Redis Cluster 的 Hash Slot、Sharding、扩缩容与数据迁移如何工作？Lua / Multi-key 操作为什么会受 Slot 约束？

- **Topic**：Cluster / Hash Slot
- **Question Type**：Concept / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S005`, `S014`, `S195`, `S247`, `S278`

**真实问法变体：**
- Redis Cluster / Hash Slot 怎么工作？
- Cluster 扩缩容如何迁移数据？
- Cluster 下 Lua Script 的 Key Slot 问题怎么处理？

### REDIS-012 · Redis 分布式锁的基本实现是什么？正确性需要满足哪些条件？

- **Topic**：Distributed Lock Basics
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**25**
- **Evidence Sources**：`S023`, `S025`, `S035`, `S040`, `S070`, `S084`, `S091`, `S093`, `S105`, `S116`, `S148`, `S154`, `S169`, `S188`, `S198`, `S201`, `S212`, `S225`, `S234`, `S251`, `S262`, `S264`, `S266`, `S273`, `S279`

**真实问法变体：**
- Redis 分布式锁怎么实现？
- SETNX 就足够了吗？
- 什么业务场景需要分布式锁？

### REDIS-013 · Redis Lock 的 Expire、Renewal / WatchDog、Owner 校验、Lua Release、RedLock 与故障窗口怎样处理？

- **Topic**：Distributed Lock Correctness
- **Question Type**：Deep Dive / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**14**
- **Evidence Sources**：`S023`, `S035`, `S070`, `S093`, `S105`, `S116`, `S148`, `S169`, `S188`, `S198`, `S201`, `S212`, `S262`, `S264`

**真实问法变体：**
- 锁过期但业务没执行完怎么办？
- Redisson WatchDog 做什么？
- 解锁为什么要校验 Owner 并原子删除？
- RedLock 的风险边界是什么？

### REDIS-014 · Lua Script 为什么适合 Redis 原子业务？库存扣减、限流、锁释放等场景如何设计？

- **Topic**：Lua / Atomicity
- **Question Type**：Why / Scenario
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S010`, `S035`, `S070`, `S086`, `S114`, `S198`, `S214`, `S247`, `S277`, `S279`

**真实问法变体：**
- 为什么秒杀扣库存常用 Redis Lua？
- Lua 在 Token Bucket 中怎样保证原子性？
- 脚本变复杂后怎样控制风险？

### REDIS-015 · Redis 与 MySQL 双写怎样保证最终一致性？Cache Aside、删除缓存、延迟双删和补偿怎样处理故障窗口？

- **Topic**：Cache Consistency
- **Question Type**：System Design / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**20**
- **Evidence Sources**：`S005`, `S046`, `S090`, `S093`, `S105`, `S118`, `S134`, `S148`, `S154`, `S161`, `S171`, `S188`, `S198`, `S201`, `S212`, `S214`, `S234`, `S264`, `S266`, `S273`

**真实问法变体：**
- 缓存和数据库怎么保证一致性？
- 为什么更新数据库后更常删除 Cache？
- Delayed Double Delete 某一步失败怎么办？

### REDIS-016 · Local Cache + Redis 多级缓存怎样分工？如何处理一致性、热 Key、降级和缓存失效风暴？

- **Topic**：Multi-level Cache
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S094`, `S118`, `S194`, `S222`, `S276`, `S277`

**真实问法变体：**
- 什么时候在 Redis 之外再加 Local Cache？
- 两级缓存各存什么？
- Redis 被打满时本地缓存怎样参与降级？

### REDIS-017 · Redis 如何承载 Session / Conversation / Auth Cache？多实例下怎样保证会话一致、隔离和过期？

- **Topic**：Session / Conversation
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S033`, `S035`, `S081`, `S091`, `S105`, `S119`, `S171`, `S178`, `S194`, `S207`, `S262`

**真实问法变体：**
- Redis + Token 怎样实现 Session？
- 多实例部署怎样保持会话一致？
- 不同用户 / Tenant 的 Context 或状态怎样隔离？

### REDIS-018 · Agent Runtime State / Checkpoint 放 Redis 时应保存什么？Checkpoint 写失败、Resume 或服务迁移时如何保证正确性？

- **Topic**：Agent State / Checkpoint
- **Question Type**：System Design / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S042`, `S087`, `S105`, `S182`, `S209`, `S242`

**真实问法变体：**
- Redis Checkpoint 应保存哪些状态？
- Tool 已成功但 Checkpoint 写失败，恢复后如何避免重复执行？
- Agent 服务迁移 / Resume 时状态如何恢复？

### REDIS-019 · 如何用 Redis 做 Rate Limit？Fixed Window、Sliding Window、Token Bucket / Leaky Bucket 怎样选？

- **Topic**：Rate Limiting
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S035`, `S069`, `S084`, `S164`, `S174`, `S198`, `S209`, `S270`

**真实问法变体：**
- Redis Sliding Window 怎么做？
- Token Bucket 与 Leaky Bucket 怎样选？
- 分布式限流怎样保证性能和一致性？

### REDIS-020 · Token Budget / 用户级 Fair Queue 等 AI 服务配额如何用 Redis 设计，并避免并发超卖？

- **Topic**：AI Quota / Budget
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S209`, `S276`

**真实问法变体：**
- 每个 Key 每分钟 N 次请求和 Token Budget 怎样同时限制？
- 并发请求 Token 消耗未确定时如何预留预算避免超卖？
- 单个恶意用户怎样避免拖垮模型服务？

### REDIS-021 · 语义缓存、查询结果缓存与普通业务 Cache 有什么不同？什么结果值得缓存，如何避免陈旧答案？

- **Topic**：Semantic / Result Cache
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S081`, `S250`

**真实问法变体：**
- RAG / Agent 是否适合做 Semantic Cache？
- 中频 Search Query 应缓存还是 Online Generation？

### REDIS-022 · Redis 有哪些安全风险？无密码实例、越权访问、敏感数据与 Agent 场景应怎样防护？

- **Topic**：Security
- **Question Type**：Security / System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S254`

**真实问法变体：**
- Redis 无密码访问会带来什么攻击面？
- Agent / RAG 权限数据放 Redis 时怎样避免越权？

### REDIS-023 · Redis 作为 Queue / State Store 与 Kafka、RabbitMQ 等 MQ 的边界是什么？

- **Topic**：Redis vs MQ
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S174`, `S181`, `S209`, `S279`

**真实问法变体：**
- Redis Queue 和 RocketMQ / Kafka 该怎么选？
- 运行状态、任务队列和消息日志分别适合放哪里？

### REDIS-024 · Redis 与 Aerospike 等 KV Store 在存储模型、容量、延迟和业务场景上怎样选型？

- **Topic**：KV Store Selection
- **Question Type**：Comparison
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S270`

**真实问法变体：**
- Aerospike 与 Redis 有什么区别？
- 什么业务更适合 Redis，什么业务更适合 Aerospike？

---

## 3. 从真人面经中出现的 Redis 追问链

### 3.1 Cache 主线

```text
Redis 为什么快
→ Data Structure
→ TTL / Expiration
→ Eviction
→ Penetration / Breakdown / Avalanche
→ BigKey / HotKey
→ Multi-level Cache
→ DB + Cache Consistency
→ Failure / Compensation
```

### 3.2 Distributed Coordination 主线

```text
SETNX
→ Expire
→ Owner Token
→ Atomic Release
→ Lua
→ Renewal / WatchDog
→ Crash / Network Partition
→ RedLock 边界
→ Idempotency / Compensation
```

### 3.3 AI Application 特有主线

```text
Session / Conversation
→ Agent Runtime State
→ Checkpoint / Resume
→ Rate Limit
→ User / Tenant Quota
→ Token Budget Reservation
→ Semantic / Result Cache
```

这说明 Redis 在 AI Application 里不只是“加速数据库”，还经常承担会话状态、Agent Checkpoint、配额和流控等 Runtime 职责。

---

## 4. 对后续 Redis 教材的校准建议

完整课程仍保留从 0 的基础主线，但需要把以下内容提升为核心章节：

1. `Redis 为什么快` 必须连到 Event Loop / I/O Multiplexing，而不是只背“单线程”；
2. Data Structure 需要用真实业务选择题串联，而不是只列命令；
3. BigKey / HotKey、TTL、Eviction 必须和缓存故障模式放在同一工程链理解；
4. Distributed Lock 必须拆成“能加锁”和“锁正确”两层，加入过期、续租、Owner、Lua、Crash；
5. Cache Consistency 应与 MySQL 模块交叉链接，并用失败时间线解释；
6. Cluster 需要覆盖 Hash Slot、迁移以及 Lua / Multi-key 限制；
7. Agent 场景增加 Session、Checkpoint、Token Budget、User-level Rate Limit；
8. 每章用对应 `REDIS-xxx` 的真实问法和 Failure Case 做折叠自测。

面经没有高频覆盖的基础命令、编码细节、内存编码结构等内容，仍由完整知识体系决定是否进入课程，不能按频率删减。
