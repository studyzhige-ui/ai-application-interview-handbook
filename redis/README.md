# Redis｜AI 应用开发秋招系统手册

> Redis 是这套 Handbook 的第 5 个正式一级模块。
>
> 目标不是背“Redis 五种数据结构 + 缓存三兄弟 + 分布式锁”，而是从 0 建立一条完整因果链：**Redis 为什么存在 → 数据怎样组织 → Runtime 为什么快 → 内存什么时候过期/淘汰 → 怎样持久化与高可用 → 怎样做原子并发控制 → 怎样把 Redis 放进 Cache、Session、Rate Limit 和 AI Runtime。**

> **Granularity Audit：✅ 已完成。** 原 27 章经过教材粒度审计后收敛为 **24 个知识小板块**。合并依据不是章节数量，而是“一个文件是否形成完整认知闭环”。研究层的 19 道 Redis Canonical、Source Count 和真人面经频率没有变化。

---

## 1. 最重要的课程原则

本模块固定遵守：

> **知识体系演进顺序优先，真实面经只用于调整复习权重、补充真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

冻结 `S001–S279` HUMAN-A 中，分布式锁是 Redis 最强面试信号之一；但课程仍然不会一上来就讲锁。

因为真正的依赖关系是：

```text
Key / Value 怎么组织
→ Command 怎么执行
→ TTL / Eviction 怎么工作
→ Persistence / Replication / Failover 有什么语义
→ MULTI / WATCH / Lua 能保证什么
→ 才能讨论 Distributed Lock 的正确性
```

所以面经决定“锁这一块必须讲到 Failure / Fencing”，却不能决定“把锁移到数据结构前面”。

---

## 2. 这次为什么从 27 调整到 24

之前有三组边界偏细：

### 2.1 Redis 为什么快 + Event Loop

原来拆成：

```text
Redis 为什么快
I/O Multiplexing / Event Loop
```

但“为什么快”本身就必须解释 Event Loop / I/O Multiplexing，否则答案不闭环。

现在合并为：

```text
Redis Runtime & Performance Model
```

### 2.2 Cache 基础 + 缓存故障

原来拆成：

```text
Cache / Key Design
穿透 / 击穿 / 雪崩
```

但穿透、击穿、雪崩本质上就是 Cache Design 的 Failure Model，应该和 TTL、回源、重建一起学习。

现在合并为：

```text
Cache Design & Failure Patterns
```

### 2.3 Distributed Lock 基础 + Correctness

只学 `SET NX PX` 而不继续学 Owner、Lease、Renewal、Failover、Fencing，会得到一个危险的“半知识”。

现在合并为：

```text
Distributed Lock：Acquire → Lease → Renewal → Failover → Fencing
```

### 2.4 为什么没有合并 Transaction / Pipeline / Lua

这三者虽然连续，但解决的问题不同：

| 机制 | 主要解决什么 |
|---|---|
| MULTI / WATCH | 连续执行 + 乐观并发控制 |
| Pipeline | 降低网络 RTT |
| Lua / Functions | 服务器端原子业务逻辑 |

它们各自有不同 Failure Model，因此继续保留独立文件。

---

## 3. Redis 在 AI Application 里的位置

```text
                 FastAPI / Agent Service
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
      MySQL             Redis           Vector DB
        │                 │                 │
   业务事实 / SoT    热点/短状态/协调     语义检索
```

Redis 常被用在：

- 高频读取 Cache；
- Session / Conversation；
- TTL 临时状态；
- Rate Limit / Quota；
- 幂等/去重辅助状态；
- Hot Runtime State；
- 分布式协调；
- 某些 Agent Runtime State Store。

Redis 不是“更快的 MySQL”，也不应该成为“所有状态的默认垃圾桶”。

---

## 4. 真人面经只校准重点

冻结研究中 Redis 当前有 **19 道 Primary Canonical、69 个独立 HUMAN-A 来源**覆盖。

高频信号包括：

- Distributed Lock Basics；
- Distributed Lock Correctness；
- Cache Penetration / Breakdown / Avalanche；
- Core Data Structures；
- BigKey / HotKey；
- Session / Conversation；
- Lua / Atomicity；
- Rate Limit；
- HA / Cluster；
- TTL / Eviction；
- Runtime Performance Model。

但：

> **Interview Heat ≠ Knowledge Importance。**

Transaction/WATCH、Pipeline、Pub/Sub/Streams、底层编码等即使面经不是最高频，也属于完整 Redis 体系。

---

## 5. 五条知识主线

### 主线 A｜数据模型与 Runtime

```text
Redis Role
→ Keyspace / Command
→ Core Data Types
→ Specialized Structures
→ Internal Encoding
→ Runtime / Event Loop / I/O Multiplexing
```

### 主线 B｜内存生命周期与 Cache

```text
TTL
→ Eviction
→ Cache Design
→ Penetration / Breakdown / Avalanche
→ BigKey / HotKey
```

### 主线 C｜可靠性与扩展

```text
RDB / AOF
→ Replication
→ Sentinel
→ Cluster / Hash Slot / Reshard
```

### 主线 D｜原子性与并发

```text
Atomic Command
→ MULTI / WATCH
→ Pipeline
→ Lua / Functions
→ Distributed Lock Correctness
```

### 主线 E｜应用层落地

```text
Pub/Sub / Streams
→ Multi-level / Semantic Cache
→ Session / Agent State Store
→ Rate Limit
→ Security / Troubleshooting
→ Redis in AI System Design
```

---

## 6. 正式 24 章

### Part A｜从 Key 到 Runtime

1. [Redis 在 AI Application 中负责什么](docs/01-Redis在AI应用中的职责.md)
2. [Keyspace、Command 与基本执行模型](docs/02-Keyspace与Command模型.md)
3. [String / Hash / List / Set / ZSet](docs/03-核心数据结构.md)
4. [Bitmap / Bitfield / HyperLogLog / Geo / Stream](docs/04-扩展数据结构.md)
5. [底层编码与内存模型](docs/05-底层编码与内存模型.md)
6. [Redis Runtime 与性能模型：为什么快、Event Loop 与阻塞边界](docs/06-RedisRuntime与性能模型.md)

### Part B｜内存生命周期与 Cache

7. [TTL 与过期删除](docs/07-TTL与过期删除.md)
8. [maxmemory、Eviction 与内存压力](docs/08-Eviction与内存管理.md)
9. [Cache 设计与故障模式：Key、TTL、穿透、击穿与雪崩](docs/09-Cache设计与缓存故障.md)
10. [BigKey 与 HotKey](docs/10-BigKey与HotKey.md)

### Part C｜Persistence、HA 与 Scale

11. [RDB 与 AOF](docs/11-RDB与AOF.md)
12. [Replication：Primary / Replica](docs/12-Replication.md)
13. [Sentinel 与自动 Failover](docs/13-Sentinel.md)
14. [Redis Cluster、Hash Slot 与 Reshard](docs/14-Cluster与HashSlot.md)

### Part D｜原子性与分布式协调

15. [Transaction：MULTI / EXEC / WATCH](docs/15-Transaction与WATCH.md)
16. [Pipeline：降低 RTT，不等于 Transaction](docs/16-Pipeline.md)
17. [Lua / Redis Functions 与服务器端原子逻辑](docs/17-Lua与Functions.md)
18. [Redis 分布式锁：Acquire、Lease、Renewal、Failover 与 Fencing](docs/18-分布式锁与正确性.md)

### Part E｜Backend / AI 场景

19. [Pub/Sub、Streams 与消息边界](docs/19-PubSub与Streams.md)
20. [Multi-level Cache 与 Semantic / Result Cache](docs/20-多级缓存与语义缓存.md)
21. [Session、Conversation 与 Agent State Store 边界](docs/21-Session与AgentState.md)
22. [Redis 实现 Rate Limit](docs/22-Redis限流.md)
23. [Security、Latency 与 Production Troubleshooting](docs/23-Security与Troubleshooting.md)
24. [Redis in AI System Design](docs/24-Redis在AI系统设计中的位置.md)

---

## 7. 模块边界

| 问题 | Primary Module |
|---|---|
| Redis Data Structure / TTL / Eviction / RDB / AOF | Redis |
| Redis Replication / Sentinel / Cluster | Redis |
| Redis Lock 的具体实现与 Failure | Redis |
| DB + Cache 最终一致性 | AI Backend Engineering |
| 通用 Rate Limit 算法选择 | AI Backend Engineering |
| Redis 上怎样实现 Sliding Window / Token Bucket | Redis |
| Redis vs Kafka / MQ 的系统选型 | AI Backend Engineering |
| Agent Checkpoint / Resume 的执行语义 | Agent Harness / Runtime |
| Redis 作为 Agent State Store 时怎样建 Key / TTL | Redis |
| 多租户系统如何组合 MySQL / Redis / Vector DB | System Design |

---

## 8. 推荐三遍学习法

### 第一遍：建立体系

按 `01 → 24` 阅读，重点理解为什么下一章自然出现。

### 第二遍：用 Review 重新画图

进入 [`review/README.md`](review/README.md)，尽量不看答案，把五条主线重新画出来。

### 第三遍：面试化

使用：

- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

最终目标不是背 Redis 命令，而是能解释：

```text
数据怎么存
→ Runtime 怎么执行
→ Memory 怎么失效
→ Failure 怎么传播
→ HA / Scale 怎么做
→ 原子性边界在哪里
→ Redis 在 AI 系统里应该承担什么、不该承担什么
```
