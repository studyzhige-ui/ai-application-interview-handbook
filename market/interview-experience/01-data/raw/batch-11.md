# Batch 11 一手面试流程

采集日期：2026-09-10

## S191 美团｜AI 全栈开发｜一面 + 二面｜面试 2026-04-15 / 04-21，次日 Offer｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/2e22607a78cd4c488df0d8bf68982c22

真人 / 第一人称证据：作者后续身份显示为美团 AI 全栈实习员工，完整记录 4/15 一面、4/21 二面以及次日 Offer；两轮从 RAG/Streaming 一路追到 MySQL/Redis/ThreadLocal/System Design/Coding。

高价值问题：

1. RAG Retrieval 完整流程是什么，文件上传如何从约 8 秒优化到 2 秒？
2. 为什么采用两阶段检索、为什么选 ES？
3. WebSocket 与 SSE 如何选择，HTTPS 通信过程是什么？
4. Redis 主从同步与常见数据结构底层如何实现，ZipList 为什么可能发生连锁更新？
5. 线程池核心参数和拒绝策略如何设计？
6. 一亿条数据怎样快速写入 MySQL？
7. 类微博 Feed 如何让用户快速看到关注博主的新内容？
8. 二面深追 MySQL Deadlock、MVCC、Optimizer、B+Tree、Isolation、Memory Model、Logs 与 SQL Tuning。
9. ThreadLocal 为什么可能 Memory Leak？MySQL 能否实现分布式锁？
10. AI Coding：如何让 AI 自动提交员工周报并保证业务正确性？

---

## S192 大疆创新｜AI Agent 开发｜一面｜面试 2026-08-11，发布 08-13｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/bbd8f778c65e4401a53de3d7417e6f77

真人 / 第一人称证据：作者明确记录本人 8 月 11 日面试、发布时仍在等待结果，并概括“前半 Agent、后半传统后端基础”；问题从 Agent Runtime 连续进入 Java ThreadPool、JVM 与 MySQL Logs。

高价值问题：

1. 从零搭 Agent System 需要哪些核心组件？
2. Short-term / Long-term Memory 怎样设计？
3. Tool / API 异常、超时如何容错和恢复？
4. 是否让 LLM 参与异常检测与自修复，这样做有什么风险？
5. Hallucination、Prompt、Token 爆涨和 Context Compression 分别怎样治理？
6. Skill 从设计、实现到 Evaluation 应考虑什么？
7. Spec Coding 与 Harness 怎样理解，为什么 Harness 能提高复杂任务完成率？
8. Java ThreadPool 的参数和任务执行流程是什么，如果重做线程池会关注什么？
9. JVM Class Loading 完整流程是什么？
10. MySQL undo / redo / binlog 各自作用是什么，为什么需要两阶段提交？
11. Coding：合并两个有序数组。

---

## S193 字节跳动｜Agent 开发｜日常实习一面｜面试 2026-08-05，发布 08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/577bbe48f8f846159c5b4400c4f10204

真人 / 第一人称证据：作者明确是第一次面试，时长约 1 小时，记录自己“答得一塌糊涂”、锁升级答得不好、Coding 与面试官先讨论但最终没写完，现场状态很强。

高价值问题：

1. Token 是什么？
2. LangGraph 在项目中承担什么作用，State 保存哪些字段？
3. JVM 为什么区分 Young / Old Generation？
4. Spring Boot 项目的亮点是什么，秒杀异步削峰怎样实现？
5. Java 常见锁有哪些，Synchronized 的 Lock Upgrade 如何理解？
6. OS Paging 与 Segmentation 分别解决什么问题，两者如何协作？
7. HTTP 与 HTTPS 的区别是什么？
8. Coding：删除字符串重复字符，同时保持相对顺序并获得最小字典序结果。

---

## S194 大麦｜Agent 开发｜实习一面｜发布 2026-04-22，已挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/15554ab5435b41938096ca97ec6d6d79

真人 / 第一人称证据：作者开头明确说明“被挂了，希望发出来对大家有帮助”，问题从本人 Redis 项目连续进入 Session、多级缓存、分布式锁，再转到 Agent Loop、Context、SSE 与 Evaluation。

高价值问题：

1. Redis + Token 怎样实现 Session，多节点部署如何保持会话一致性？
2. 高并发下怎样使用 Redis + Local Cache，如何维护多级缓存一致性？
3. Distributed Lock 怎样设计，本地缓存与分布式缓存并存时如何保持数据一致？
4. Redis 被打满时怎样降级并避免 Cache Avalanche？
5. Token / 请求链路怎样做异常 Retry？
6. Agent 如何检测并终止 Dead Loop？
7. Context Optimization 怎样做？
8. SSE Streaming 怎样设计？
9. Agent Project 的质量怎样 Evaluation？
10. 是否关注 Context Compression 等最新研究和工程落地？

---

## S195 字节跳动｜后台 Agent 开发｜实习二面｜发布 2026-05-01｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/558c941c4da641e193ca40a63296ea6a

真人 / 第一人称证据：作者明确以本人二面分享并“攒人品”；题目从 Process / Thread / Coroutine、Go GMP、Java ThreadPool、Redis Cluster 和 SQL Transaction 连到 Agent / RAG / MCP。

高价值问题：

1. Process、Thread、Coroutine 的区别是什么？
2. Go GMP Scheduling Model 如何工作？
3. Java ThreadPool 核心参数与典型并发场景是什么？
4. 项目里的 Distributed / Microservice Architecture 怎样组织？
5. Redis Cluster、Hash Slot、Sharding 与扩缩容迁移如何实现？
6. 两个并发事务读写同一条数据时，每一步 SELECT / UPDATE / INSERT 会发生什么？
7. Agent 项目的真实架构是什么？
8. RAG 的核心流程是什么？
9. Function Call 与 MCP 的区别是什么？
10. System Design：分析业务需要哪些接口以及完整处理链路。
11. Coding：Path Sum III。

---

## S196 美团｜后端 Agent 开发｜暑期一面｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8867a67221c94b41a1fd42c9ccdc9075

真人 / 第一人称证据：作者明确以本人美团后端 Agent 暑期一面发布并“发面经攒人品”，问题虽不多但沿项目直接追 Hallucination、Agent Constraint、Skill/MCP 以及 Coding-Agent 软件工程流程。

高价值问题：

1. LLM Hallucination 在工程中怎样治理？
2. Agent 开发中如何实现执行约束？
3. Skill 与 MCP 两种交互方式如何选择？
4. Autonomous Agent Development 与 Spec / Structured-document-driven Workflow 各有什么优缺点？
5. 企业内部结合 AI 的开发流程应怎样设计？
6. 是否使用 AI 做 Code Review，怎样建立边界？
7. AI 生成 Unit Test 时，怎样判断测试覆盖是否充分？

---

## S197 百度｜Coding Agent｜暑期实习技术面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d00b483e26214d92a3a455a362d93fbb

真人 / 第一人称证据：作者以本人 Coding Agent 暑期实习问题复盘发布并写“发一下问题给大家参考，攒攒人品”，问题高度集中在 Agent Planning / Context / Memory / Coding Agent Architecture。

高价值问题：

1. Planner 在 Agent 中适合哪些任务，Long Task 的长度如何衡量？
2. Main Model、Sub-agent 类型与 Context 内容怎样选择？
3. SFT 如何提升 Planning 能力？
4. Agent 的 Agency / 自主性从哪里来？
5. ReAct 的执行流程是什么？
6. 为什么 Agent Architecture 会拆 Host 与 Sub-agent？
7. Rule、MCP、Skill 有什么边界？
8. Long Context 如何 Summary，Coding 场景压缩时哪些信息必须保留？
9. Long-term Memory 存在哪里、如何 Retrieval？
10. 从零到一设计 Coding Agent 的核心模块是什么？

---

## S198 京东科技｜AI 后端开发｜二面｜发布 2026-04-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e791ff8b4ae94768af6fbdcdbd5fa963

真人 / 第一人称证据：作者以本人二面分享并“攒人品”，整场围绕 Redis Rate Limit / Distributed Lock / Cache Consistency、ThreadPool Availability 和 AI Coding 生产实践连续追问。

高价值问题：

1. Redis Token Bucket 怎样保证命令原子性和网络抖动下的可用性？
2. Lua Script 在限流中的具体作用是什么？
3. Token Bucket 与 Leaky Bucket 如何选择？
4. 多业务争抢分布式锁时，怎样避免 Deadlock / Lock Timeout？
5. Downstream Timeout 或 Connection Pool 打满时如何保护服务？
6. Redis TTL 应怎样设置？
7. Cache Double Delete 中 MySQL / Redis 节点宕机会造成什么问题？
8. ThreadPool 参数怎样根据业务负载设置，任务超载时如何保障可用性？
9. AI Coding 日常怎样使用，最大收益和典型坑是什么？
10. 如何区分 AI 辅助生成模块与本人独立开发模块，并保证最终质量？

---

## S199 字节跳动｜AI 全栈研发｜实习一面｜发布 2026-06-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/73f02711ba764ec096cfe2a5798a5048

真人 / 第一人称证据：作者发布本人字节 AI 全栈一面，结尾直接写“估计挂了”；整场把 MySQL/Redis/Kafka 与 RAG/Memory/Tool Calling/Coding 混合考察。

高价值问题：

1. MySQL Dirty Read / Non-repeatable Read / Phantom Read 如何出现和解决？
2. RAG System 是 Monolith 还是 Distributed，为什么？
3. Composite Index 与 `LIKE` 查询如何设计？
4. Redis Cache Breakdown 如何避免，Redis 适合存什么？
5. Knowledge Base 支持哪些格式，Storage / Retrieval Flow 怎样实现？
6. Chunk 怎么切、Embedding Dimension 为什么这样选？
7. RAG Accuracy 怎样优化，Retrieval 之后除了加权还能怎样做？
8. Kafka 如何保证消息一致性和尽量不丢失？
9. RAG Conversation Memory 如何实现？
10. LLM 怎样调用 Tool，工程上下文链路用了什么 Protocol？
11. Coding：二维 Maze 最短路径并输出路径。

---

## S200 腾讯｜AI 后端开发｜暑期二面｜发布 2026-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/770ace354631496db18ed50ac3a7e417

真人 / 第一人称证据：作者以“27 暑期实习 AI 后端开发二面”记录本人面试，从 AI/RAG 项目一路追 Redis High Availability、Sharding、HTTP/HTTPS/QUIC 与 Coding，属于明确目标 AI Backend 场次。

高价值问题：

1. 为什么在研发流程中引入 AI，底层 Model 为什么这样选？
2. Knowledge-base QA 的完整 Pipeline 是什么？
3. RAG Recall 怎样评估和优化？
4. BM25 怎样检索，Query Rewrite 怎样实现？
5. 最终给 LLM 的 Prompt 怎样构造？
6. Redis Data Type、Eviction Policy 与应用场景怎样匹配？
7. Redis Primary/Replica、Sentinel、Cluster 有什么区别？
8. Data Sharding 为什么需要，基本原理是什么？
9. HTTP 与 HTTPS 的交互过程是什么，QUIC 解决什么问题？
10. Coding：House Robber。

---

## S201 滴滴｜AI 后端开发｜日常实习一面 45min｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1c0d48dee35a428f9d3926f7c95b2faf

真人 / 第一人称证据：作者以本人滴滴 AI Backend 一面发布并写“攒人品中”，项目后集中深问 MySQL / Redis / Rate Limit，再进行 LRU Coding。

高价值问题：

1. MySQL Index Structure 有哪些？
2. Transaction Isolation Level 与 Transaction Principle 如何解释？
3. RR 下仍可能出现怎样的 Phantom Read，不提升到 Serializable 如何治理？
4. MVCC 原理是什么？
5. Redis 常见 Data Structure 与 ZSet 底层怎样实现？
6. Redis Persistence 有哪些方式？
7. Redis Distributed Lock 实现要注意什么？
8. Redis 与 MySQL 如何保持数据一致性？
9. 分别从 Single-node、Distributed、Global 角度设计 API Rate Limit。
10. Coding：LRU Cache。

---

## S202 字节跳动｜AI 后端开发｜春招一面｜发布 2026-04-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/605da447826b48f8a521e4729eb0f892

真人 / 第一人称证据：作者以本人 AI Backend 一面发布并“攒人品”；从“AI 项目是企业项目还是自己做”开始，一路问 Network、Java Concurrency、Token、MCP、AI Code Review 与 Coding。

高价值问题：

1. 一次 HTTP Request 涉及哪些 Protocol Layer，输入 Domain 后发生什么？
2. DNS / ARP / HTTP Method / Packet Capture 怎样理解？
3. CAS 是什么？
4. Java ThreadPool 参数、场景与 Rejection Policy 怎样选择？
5. HashMap Expansion 为什么通常翻倍？
6. Token 是什么、如何 Tokenize？
7. MCP 是什么，不同 MCP Tool 的共同标准是什么？
8. AI 自动 Code Review 的规则、流程和 Prompt 怎样设计？
9. 怎样让 AI Code Review 更准确？
10. Coding：Binary Tree Path Sum。

---

## S203 携程｜AI 后端开发｜暑期一面 1h｜发布 2026-04-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6bf0a93fc22d486b97dd6037df621639

真人 / 第一人称证据：作者明确以本人携程 AI Backend 一面分享并写“给我面没招了”；虽然 AI 名词不多，但岗位明确，整场通过 Domain Design、Redis、Storage System、REST、ES、Virtual Thread、MQ 与压测考察 AI Backend 所需工程底座。

高价值问题：

1. Domain Layer 怎样拆分，DDD Boundary 的依据是什么？
2. Redis 怎样防止 Cache Penetration？
3. 每天约 10TB 数据的 Storage System 怎样设计？
4. 支持 1 分钟到 1 年 Time-range Query 的 RESTful API 怎样设计？
5. 所有检索是否都应走 ES？
6. Hot / Cold Data Separation 怎样设计？
7. Java 21 与 Java 8 有哪些关键差异，Virtual Thread 如何理解？
8. StackOverflow 与 OutOfMemory 如何定位和处理？
9. 是否做过 Stress Test，指标如何设计？
10. MQ Backlog / Message Accumulation 发生时怎样应急？
11. Coding：Josephus Circle 变体。

---

## S204 虾皮｜AI 后端开发｜日常实习一面｜发布 2026-04-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/bdce7791140e4f8e8497dd776584f4f3

真人 / 第一人称证据：作者以本人 AI Backend 一面发布并“攒人品”，说明还有十多个项目追问；公开问题覆盖千万级 QPS、大促稳定性、Cache Consistency、CPU Cache、OpenClaw / Role / Skill 与 Coding。

高价值问题：

1. 双十一/双十二上千万 QPS 的商品查询系统怎样支撑 Peak Traffic？
2. 高并发读场景怎样处理 Data Consistency？
3. 统一 TTL 为什么可能造成 Cache Avalanche / Penetration，怎样治理？
4. CPU L1 / L2 Cache 的设计差异是什么？
5. 大促前一个月如何从 System Stability 与业务热点 / 冷数据两侧做 Capacity Planning？
6. 大促结束后如何从 System Design 和业务筹备两个角度 Review？
7. 为什么 OpenClaw 受到关注，核心价值是什么？
8. Agent 中 Role 与 Skill 的核心区别是什么？
9. Coding：Binary Tree Level Order Traversal、Maximum Product Subarray。
