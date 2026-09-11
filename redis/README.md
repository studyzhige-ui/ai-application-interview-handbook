# Redis｜AI 应用开发秋招系统手册

> Redis 是这套 Handbook 的第 5 个正式一级模块。
>
> 目标不是背“Redis 五种数据结构 + 缓存三兄弟 + 分布式锁”，而是从 0 建立一条完整因果链：**Redis 为什么存在 → 数据怎样组织 → 为什么快 → 内存什么时候失效/淘汰 → 怎样持久化和高可用 → 怎样做原子并发操作 → 怎样安全地做缓存、锁、Session、限流与 AI Runtime 状态。**

> **Granularity Audit：🟠 Minor Remediation。** 当前 27 章正文内容已经完成，知识顺序正确；但少量文件边界偏细，后续会把 `Redis 为什么快 + I/O Multiplexing/Event Loop`、`MULTI/WATCH + Pipeline + Lua/Functions`、`Distributed Lock Basics + Lock Correctness` 等连续知识重新组合，目标约 **23 个知识小板块**。这只改变教材文件粒度，不改变 Redis 19 道 Canonical、Source Count 或面经频率。完整审计见 [`../roadmap/curriculum-granularity-audit.md`](../roadmap/curriculum-granularity-audit.md)。

## 1. 最重要的课程原则

本模块继续固定遵守：

> **知识体系演进顺序优先，真实面经只用于调整复习权重、补充真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

冻结 `S001–S279` HUMAN-A 中，分布式锁有 25 个独立来源，是 Redis 最强面试信号之一；但课程不会一上来就讲锁。

因为你必须先知道：

```text
Key / Value 怎样存
→ Command 怎样执行
→ TTL 怎样工作
→ 单个命令为什么原子
→ Lua / Transaction 能保证什么
→ 主从 / Failover 会发生什么
→ 才能真正讨论“锁是否正确”
```

所以面经决定“锁这一章要讲到 L4”，却不能决定“把锁挪到数据结构前面”。

---

## 2. Redis 在 AI Application 里为什么常见

MySQL 更适合：

```text
结构化
长期
可靠
可查询
业务 Source of Truth
```

Redis 更常被放在：

```text
高频读取
低延迟状态
有 TTL 的临时数据
Session / Conversation
Rate Limit
Cache
短期任务状态
幂等 / 去重辅助状态
热点数据
```

一个典型 AI Application：

```text
                 FastAPI
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      MySQL       Redis      Vector DB
        │           │           │
   长期业务数据   热点/短状态   语义检索
```

Redis 不是“更快的 MySQL”，也不是“什么都塞进去的内存数据库”。

---

## 3. 真人面经只校准重点

冻结研究中 Redis 当前有 **19 道 Primary Canonical、69 个独立 HUMAN-A 来源**覆盖。

| Topic | HUMAN-A Sources | 深度 |
|---|---:|---:|
| Distributed Lock Basics | 25 | L2 |
| Cache Penetration / Breakdown / Avalanche | 20 | L3 |
| Core Data Structures | 18 | L2 |
| Distributed Lock Correctness | 14 | L4 |
| BigKey / HotKey | 11 | L4 |
| Session / Conversation | 11 | L4 |
| Lua / Atomicity | 10 | L3 |
| Redis Rate Limit Implementation | 8 | L4 |
| High Availability | 8 | L2 |
| TTL / Expiration | 7 | L2 |
| Performance / Thread Model | 7 | L2 |
| Multi-level Cache | 6 | L4 |
| Cluster / Hash Slot | 5 | L4 |
| Eviction | 5 | L3 |
| Persistence | 4 | L2 |

> **Interview Heat ≠ Knowledge Importance。** Transaction/WATCH、Pipeline、Pub/Sub/Streams、底层编码等即使直接面经不高，也属于完整 Redis 体系，必须保留。

---

## 4. 版本与事实口径

正文以现代 Redis Open Source 官方文档为事实基线，不把“Redis 永远单线程”“Redis 只有五种数据结构”这种历史化口诀当成完整事实。

官方入口：

- Data types：<https://redis.io/docs/latest/develop/data-types/>
- Transactions：<https://redis.io/docs/latest/develop/using-commands/transactions/>
- Pipelining：<https://redis.io/docs/latest/develop/using-commands/pipelining/>
- Programmability / Lua / Functions：<https://redis.io/docs/latest/develop/programmability/>
- Persistence：<https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/>
- Replication：<https://redis.io/docs/latest/operate/oss_and_stack/management/replication/>
- Sentinel：<https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/>
- Cluster：<https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/>

课程会优先讲跨版本稳定的机制；遇到明显版本相关能力时单独标注。

---

## 5. 五条主线

### 主线 A｜数据模型与 Runtime

```text
Redis Why
→ Keyspace / Command
→ Core Data Types
→ Specialized Structures
→ Internal Encoding
→ Thread Model
→ Event Loop / I/O Multiplexing
```

### 主线 B｜内存生命周期与 Cache

```text
TTL
→ Expiration
→ maxmemory
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

### 主线 D｜并发与原子性

```text
Atomic Command
→ MULTI / EXEC / WATCH
→ Pipeline
→ Lua / Functions
→ Distributed Lock
→ Lock Correctness
```

### 主线 E｜应用层落地

```text
Pub/Sub / Streams
→ Multi-level / Semantic Cache
→ Session / Conversation / Agent State Store
→ Rate Limit
→ Security / Troubleshooting
→ Redis in AI System Design
```

---

## 6. 当前 27 章（内容完成，待 Minor Granularity Remediation）

> 下列文件目前仍可正常学习；后续合并只重新组织相邻内容，不删除知识点。

### Part A｜从 Key 到 Runtime

1. [Redis 在 AI Application 中负责什么](docs/01-Redis在AI应用中的职责.md)
2. [Keyspace、Command 与 Redis 基本执行模型](docs/02-Keyspace与Command模型.md)
3. [String / Hash / List / Set / ZSet](docs/03-核心数据结构.md)
4. [Bitmap / Bitfield / HyperLogLog / Geo / Stream](docs/04-扩展数据结构.md)
5. [底层编码与内存效率](docs/05-底层编码与内存模型.md)
6. [Redis 为什么快：Thread Model 与阻塞边界](docs/06-Redis为什么快.md)
7. [I/O Multiplexing、Event Loop 与连接模型](docs/07-IO多路复用与EventLoop.md)

### Part B｜内存生命周期与缓存

8. [TTL 与过期删除](docs/08-TTL与过期删除.md)
9. [maxmemory、Eviction 与内存压力](docs/09-Eviction与内存管理.md)
10. [Cache 基础、Key Design 与 Cache Aside 边界](docs/10-Cache基础与Key设计.md)
11. [Cache Penetration / Breakdown / Avalanche](docs/11-缓存穿透击穿雪崩.md)
12. [BigKey 与 HotKey](docs/12-BigKey与HotKey.md)

### Part C｜Persistence、HA 与 Scale

13. [RDB 与 AOF](docs/13-RDB与AOF.md)
14. [Replication：Primary / Replica](docs/14-Replication.md)
15. [Sentinel 与自动 Failover](docs/15-Sentinel.md)
16. [Redis Cluster、Hash Slot 与 Reshard](docs/16-Cluster与HashSlot.md)

### Part D｜原子性、批处理与分布式锁

17. [Transaction：MULTI / EXEC / WATCH](docs/17-Transaction与WATCH.md)
18. [Pipeline：降低 RTT，不等于 Transaction](docs/18-Pipeline.md)
19. [Lua / Redis Functions 与服务器端原子逻辑](docs/19-Lua与Functions.md)
20. [Distributed Lock：从 SET NX EX/PX 开始](docs/20-分布式锁基础.md)
21. [Lock Correctness：Owner、Lease、Renewal、Failover、Fencing](docs/21-分布式锁正确性.md)

### Part E｜真实 Backend / AI 场景

22. [Pub/Sub、Streams 与消息边界](docs/22-PubSub与Streams.md)
23. [Multi-level Cache 与 Semantic / Result Cache](docs/23-多级缓存与语义缓存.md)
24. [Session、Conversation 与 Agent State Store 边界](docs/24-Session与AgentState.md)
25. [Redis 实现 Rate Limit](docs/25-Redis限流.md)
26. [Security、Latency 与 Production Troubleshooting](docs/26-Security与Troubleshooting.md)
27. [Redis in AI System Design](docs/27-Redis在AI系统设计中的位置.md)

---

## 7. 为什么加入了面经之外的章节

例如 `Transaction/WATCH`、`Pipeline`、`Pub/Sub/Streams` 并不是当前最高频 Canonical，但如果不学：

- 你不知道“多个命令”为什么不天然原子；
- 会把 Pipeline 错说成 Transaction；
- 会把 Lua 当成“更高级的事务”；
- 会把 Redis Stream / PubSub 和 Kafka / MQ 混成一类；
- 分布式锁的 Race / Failover 也难真正理解。

所以它们属于知识骨架，不能因面经低频而删除。

---

## 8. 模块边界

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
| Redis 作为 Agent State Store 时如何建 Key / TTL | Redis |
| 多租户 AI 系统怎样组合 MySQL / Redis / Vector DB | System Design |

课程会主动交叉链接，但不会重复创建同一知识模型。

---

## 9. 推荐三遍学习法

### 第一遍：当前先严格按 01 → 27

粒度整改前，现有顺序仍然保持完整 0→1 依赖；合并后不会改变知识顺序。

### 第二遍：画关键流程

进入 [`review/README.md`](review/README.md)，重点能自己画：

```text
Event Loop
TTL + Eviction
RDB / AOF
Replication / Sentinel
Cluster Slot
WATCH / MULTI / EXEC
Lua Atomic Path
Distributed Lock Failure Timeline
```

### 第三遍：面试化

- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

顺序仍然是：

```text
理解机制
→ 能解释 Trade-off
→ 能分析 Failure
→ 最后才压缩成 30 秒答案
```

---

## 10. 贯穿全书的 AI Application 示例

后面反复使用：

```text
Tenant
  ├─ Session / Auth Cache
  ├─ Conversation Hot State
  ├─ Rate Limit
  ├─ Agent Run Temporary State
  ├─ Tool Result Cache
  └─ Semantic Query Cache
```

Key 可能类似：

```text
session:{tenant_id}:{session_id}
conversation:{tenant_id}:{conversation_id}
rate:{tenant_id}:{user_id}
agent_run:{tenant_id}:{run_id}
cache:tool:{tool_name}:{args_hash}
semantic_cache:{tenant_id}:{query_hash}
```

后面会持续追问：

```text
TTL 多久？
谁是 Source of Truth？
Key 会不会变成 BigKey？
HotKey 怎么治理？
Failover 会不会丢最近写入？
需要强一致吗？
Redis 挂了系统是降级还是不可用？
Agent State 能否只存在 Redis？
```

---

## 11. 研究证据入口

- [`../research/questions/redis.md`](../research/questions/redis.md)：Redis Primary Canonical；
- [`../research/analysis/curriculum-evidence-matrix.md`](../research/analysis/curriculum-evidence-matrix.md)：频率与深度；
- [`../research/analysis/follow-up-chains.md`](../research/analysis/follow-up-chains.md)：真实追问递进；
- [`../research/analysis/frequency-ranking.md`](../research/analysis/frequency-ranking.md)：全局热度。

HUMAN-A 负责“市场在问什么”；Redis 官方文档与稳定工程原理负责“机制是什么”。

---

## 12. 下一环

Redis 学完后进入：

> **Vector DB → LLM Foundation → RAG → Agent Harness / Runtime**

到那里你会清楚知道：Redis 解决的是低延迟结构化状态和缓存问题，而 Vector DB 解决的是语义近邻检索问题，两者不能因为都叫“数据库”就互相替代。
