# Batch 07 — 2026 AI 应用 / Agent 高质量面经（基础能力校准批）

采集日期：2026-09-09

> 本批继续执行“宁缺毋滥”，但有意识修正前几批偏向 Harness / Runtime 深挖造成的采样偏差：在不降低来源质量的前提下，优先补充 **AI Agent / AI 应用岗位里同时考察 Python、MySQL、Redis、FastAPI、并发与传统后端能力** 的第一人称面经。
>
> 重要：这不是为了“凑数据库题”，而是为了判断这些基础能力在真实 AI 应用岗位中到底是否仍然被考察。

---

## S077 拼多多 PDD｜Agent 三面｜2026-08-31｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/9908477cdd4041fabacbfbf02febb13c

高价值问题：

1. Python 多线程与 Java 多线程的核心差异是什么？
2. GIL 为什么产生，对 Python 并发意味着什么？
3. FastAPI URL 路由底层如何把请求匹配到处理函数？
4. Qdrant 为什么适合项目中的向量检索，选型依据是什么？
5. HNSW 的搜索思想、优缺点以及与朴素向量检索的差异？
6. Agent 输出效果如何量化评估？
7. RAG 中存在图片等非文本内容时如何处理？

价值：**直接证明 Python 基础 / Web Runtime 并没有从 Agent 面试消失**，而是常与 Vector DB、RAG、Agent Eval 混合出现。

---

## S078 字节跳动｜Agent 开发一面｜2026-09-09 发布，面试日期未明确｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/612a1c20eea744a288b142f5b43f57e1

高价值问题：

1. Agent Token 与权限 Scope 如何关联，数据库层面如何建模？
2. SSE 如何做心跳、断线重连与任务续传？
3. Agent 重复下单如何通过幂等 Key 防止重复副作用？为什么幂等 Key 不能由 LLM 自由生成？
4. Redis Lua 如何实现多维度限流？
5. Redis 宕机或大量 Key 同时失效时，如何避免数据库被击穿？
6. 长任务为什么采用异步执行 + SSE，而不是同步 HTTP？
7. MySQL 在 Agent 系统中保存哪些持久化业务数据？
8. Python dict 的底层结构、插入/查询、哈希冲突与删除逻辑是什么？
9. LRU 与 Top-K 的复杂度和实现思路？

价值：一场面试同时覆盖 **Agent 权限 / 幂等 / Streaming + Redis + MySQL + Python dict 底层 + 数据结构**，非常适合作为“AI 应用本质仍然是工程系统”的高权重样本。

---

## S079 平安银行｜AI 开发一面（社招）｜2026-08-26 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/e72c4b75edc245349f79e20d44834301

高价值问题：

1. Redis ZSet 按什么排序，底层与典型场景是什么？
2. Redis 持久化和 Cluster 故障切换如何理解？
3. Python 多线程 / 线程池如何实现，生产中如何看待 Python 性能？
4. 多 Agent 如何通信、Leader 如何路由子 Agent？
5. Skill 的能力边界和底层组成是什么？
6. RAG 知识库频繁迭代时如何维护？
7. Agent 权限如何做更细粒度的数据隔离？
8. Kafka 分区、消费者重平衡和 MQ 选型如何解释？
9. DDD、微服务注册发现、心跳、gRPC/tRPC、事件驱动如何与 AI 平台工程结合？

价值：社招样本很明显地表明 AI 应用工程并不是只考 Agent；**Python、Redis、MQ、微服务和系统设计仍是主体能力**。

---

## S080 浦发银行｜AI 开发一面（社招）｜2026-08-26 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/c200fd35c881415086928e113028e4c8

高价值问题：

1. Agent 权限控制如何实现？
2. Retry 与 Degrade 如何根据错误类型选择？
3. Skill、知识库、MCP 返回内容冲突时，如何建立信任与裁决规则？
4. Skill 版本扩散后如何合并、发布和治理？
5. 用户级 Memory 如何设计？
6. Redis HotKey、缓存击穿 / 穿透 / 雪崩如何治理？
7. 分布式最终一致性如何保证？
8. RAG Embedding 效果不好如何优化？

价值：Agent / Memory / Skill 与 **Redis + 分布式一致性** 同场出现，说明中间件知识更多是在 AI 场景下被重新包装，而不是消失。

---

## S081 人马文化｜AI 开发实习生｜2026-08-03｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/6cbcf0d20d6d41738d331df41c8fc9e9

高价值问题：

1. Agent 架构和 ReAct Loop 怎么设计？
2. 意图路由与误诊断怎么处理？
3. Skill 自学习闭环怎么做？
4. 服务如何部署，CI/CD / Jenkins 如何接入？
5. MySQL 慢查询如何排查，慢查询日志如何使用？
6. Redis 常用数据类型怎么选？
7. FastAPI 在 AI 服务中承担什么职责？
8. Python 语言特性掌握到什么程度？

价值：非常典型的 **AI 应用实习岗 = Agent + Python/FastAPI + MySQL/Redis + 部署** 组合。

---

## S082 奇虎 360｜Agent 开发一、二面｜2026-02-12 / 02-27｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/f1381f5afdc94a0d899a61c707401c8e

高价值问题：

1. Python 相比 Java 的优劣与 Agent 场景适配？
2. 多版本快照、乐观锁、回滚和重启恢复如何保证状态一致性？
3. LLM 熔断与降级怎么设计？
4. 多跳检索循环如何控制？
5. MySQL 为什么使用 B+Tree，联合索引如何设计、最左字段缺失为什么可能失效？
6. MySQL ACID、WAL、事务隔离如何联系起来？
7. Redis 数据结构如何选，排行榜为什么适合 ZSet？
8. MySQL 与 Redis 如何保证最终一致性？

价值：一面偏业务，二面转为 **Agent + 后端可靠性 + MySQL/Redis + Python**，非常适合观察岗位层级变化。

---

## S083 阿里云｜Agent 研发暑期实习一面｜2026-04-15｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/8b1311f48f584aaf9141fcc2b47beebb

高价值问题：

1. 秒杀不经过 Redis、直接打 MySQL 会出现什么瓶颈？
2. 行锁、悲观锁、乐观锁与 MVCC 如何选？
3. 本地缓存 + Redis + MySQL 三层数据不一致如何处理？
4. ZSet 做限流的瓶颈是什么？
5. 百万用户规模下内存与限流系统如何优化？
6. RAG 原理和向量数据库选型？
7. Planner / Executor / Supervisor 出现循环依赖或步骤失败如何处理？
8. Context 持续增长如何控制？
9. SSE 流式推送如何实现？
10. AI Coding：现场实现具备鉴权、限流、路由的网关。

价值：**数据库 / 缓存 / 限流与 Agent/RAG 同等重要**，说明“后端底座”不是附录。

---

## S084 快手｜AI Agent 开发实习生一二面｜2026-02｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/511a8021f28c46a0ad27c75a6e51b1a1

高价值问题：

1. 父子索引、BM25、Rerank、TopK 为什么这样设计，是否做过实验验证？
2. Context Engineering 与长短期 Memory 如何协同？
3. 分布式令牌桶、漏桶、滑动窗口限流如何实现，Redis 用什么结构？
4. LRU、Bloom Filter 等数据结构原理？
5. MySQL 索引失效、LIKE、隔离级别、MVCC、ReadView、锁如何解释？
6. 为什么项目同时选择 Python 与 Go，并发模型差异是什么？
7. RAG 评测数据集和指标如何构建？

价值：一面大量 **Redis/MySQL/数据结构/并发基础**，二面几乎全是 Agent/RAG，清楚展示了不同面试轮次的知识重心差异。

---

## S085 字节跳动｜AI 后台开发日常实习一面｜2026-04-18｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/74ab328107754298a097a7ab27bf53cd

高价值问题：

1. Agent 内部执行机制能否展开到具体模块？
2. MCP 与预置搜索工具 / 内部平台操作的边界？
3. Agent / RAG 如何做轨迹级和结果级评测？
4. Redis 缓存适合插在 AI 链路哪一层，为什么高并发性能好？
5. 多线程适合哪些场景？
6. Redis 与 MySQL 在 AI 应用中的职责如何分层？
7. B+Tree 为什么适合作为数据库索引？
8. ES 检索、向量检索和 RAG 的关系如何区分？

价值：这是非常直接的“**AI 后台**”岗位样本，Agent 能力与 Redis/MySQL/并发基础并列考察。

---

## S086 有赞｜后端 AI 开发一面｜2026-04-27｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/38dc5a92179b4331aa517fef3f9b63d7

高价值问题：

1. 线程池原理、参数与上下文传递？
2. MySQL 覆盖索引、分库分表、主从同步如何工作？
3. Redis 缓存击穿 / 穿透、HotKey 如何治理？
4. MQ 如何保证消息不丢和避免重复消费？
5. 分布式事务如何落地？
6. RAG 如何优化，图片类文档怎么处理？
7. 是否了解 Agent 集群 / 多实例架构？

价值：典型的“后端 AI 开发”画像：**传统后端基础是主干，AI/RAG 是上层业务能力**。

---

## Batch 07 结论

本批不是发现“基础知识突然回潮”，而是纠正了前几批的两种视觉偏差：

1. **去重偏差**：MySQL / Redis / Python 的很多问题早已建立 canonical question，后续重复出现时通常只被记为“强化”，不像新 Harness 题那样显眼。
2. **岗位采样偏差**：Batch 04–06 为寻找新知识边界，主动偏向 Agent Harness、Runtime、Coding Agent、二面/深挖轮次；这些岗位和轮次天然更少问基础八股。

真实情况更接近：

- **AI Agent / Harness 专项深挖轮次**：Agent Runtime、Context、Tool、Memory、RAG、Eval 比重更高；Python/MySQL/Redis 可能只点到关键工程点。
- **AI 应用开发 / AI 后台 / Agent 后端 / 一面**：Python、FastAPI、MySQL、Redis、并发、MQ、网络依然非常常见。
- **社招 / 工程平台岗位**：Redis、MQ、微服务、数据一致性、系统设计甚至可能比纯 Agent 概念更重。

因此后续课程不能根据“某几批新增 canonical 数量”降低 Python/MySQL/Redis 权重。