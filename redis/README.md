# Redis｜缓存、短状态与分布式协调

[← MySQL](../mysql/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [Vector Database →](../vector-db/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：24 个连续知识小板块** · **HUMAN-A Canonical：19** · **独立来源覆盖：69**  
> **质量：Granularity / Coverage / Content Depth 已验收**

掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。

---

## 1. 这个模块解决什么

掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。

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

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → **Redis** → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent Harness / Runtime](../agent-harness/README.md) → [System Design](../system-design/README.md)

当前模块角色：**Data / 掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。**

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

所以本模块是 **19 道 Canonical → 24 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Key / Data Structure / Encoding → Runtime / TTL / Eviction → Cache Failure / HotKey → RDB / AOF / Replication / Sentinel / Cluster → Transaction / Pipeline / Lua / Distributed Lock → Streams / Session / Rate Limit / Troubleshooting
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜数据模型与 Runtime

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

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **19 道 Primary Canonical、69 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- Distributed Lock 与 Correctness
- Cache Penetration / Breakdown / Avalanche
- Core Data Structures
- BigKey / HotKey
- Lua / Atomicity
- HA / Cluster

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- Redis 数据结构、TTL、持久化、高可用与锁实现归 Redis。
- DB + Cache 一致性、通用 Rate Limit 与 MQ 选型归 AI Backend Engineering。
- Agent Checkpoint / Resume 的执行语义归 Agent Harness。

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

- [Canonical Questions](../research/questions/redis.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 24` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–24 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[Vector Database](../vector-db/README.md)。
