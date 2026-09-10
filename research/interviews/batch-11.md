# Batch 11 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批继续严格执行统一准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场痕迹 + AI Application / Agent 目标岗位 + 正文稳定可核验 + 非转载 / 非合集 / 非重复 = HUMAN-A**。
>
> **平台一视同仁。** 本轮主动搜索牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客与独立站；平台没有配额，也没有质量加成。最终能否进入正式 Batch，只由 HUMAN-A Gate 决定。
>
> 一旦来源和岗位通过 Gate，保留整场真实问题：Python、FastAPI、Backend Engineering、MySQL、Redis、Vector DB、LLM Foundation、RAG、Agent Harness、System Design，以及实际出现的 OS / Network / MQ / Concurrency / Coding / Security / Evaluation 均一视同仁，不只摘 Agent 名词。
>
> 去重继续固定使用三层：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。同一候选人同一招聘流程的多轮面试合并计数；问题只做研究所需的简洁转述，不把合理推导写成“面试官真实问过”。

---

## S226 小红书｜大模型平台 Agentic 全栈研发｜一面｜面试 2026-08-06，发布 08-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e5e9311a623940eead6ec98c65e7f9e8

真人 / 第一人称证据：作者明确记录 8 月 6 日本人一面、次日发现挂；写明面试官很耐心、会引导，自己 Java 八股忘了不少、某个 Query 判断问题没答好，并在反问中继续讨论真实业务技术选型。

高价值问题：

1. 业务 Agent 实际解决什么问题，是否真的帮助研发而不只是客服问答？
2. Agent 的写操作边界如何划分，哪些动作必须受控？
3. Harness Layer 包含哪些能力，与编排层是什么关系？
4. Agent Orchestration 怎样重构，节点 / 边如何组织？
5. 如何判断 Query 是明确还是模糊，并做 Intent Routing？
6. Skill 与 Tool 有什么区别，Skill 在什么阶段 Fetch？
7. 多模型接入时如何保证表现一致，日调用量上升到十几万次怎样扩容？
8. 为什么使用 SQLite，自研框架与 LangGraph 如何取舍？
9. Java 8→17、HashMap、MySQL B+Tree 与联合索引等基础怎样解释？
10. RAG 向量知识库在真实业务中的 Query 切分和检索技术选型如何做？

---

## S227 字节跳动｜大模型应用开发｜日常实习一面 1h｜发布 2026-03-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/95b8c6edf3ad46818b94605675a12089

真人 / 第一人称证据：作者明确以本人一面分享并写“给我面没招了，发点面经攒攒人品”；问题从两个项目一路进入 RAG、Milvus、FastAPI、Python 并发、Multi-Agent 和 Coding。

高价值问题：

1. Recursive Character Chunking 相比固定长度切片有什么优势？
2. Milvus 中需要按文档分类检索时，多个 Collection 与 Partition 如何选择？
3. Agent Reflection 怎样设计，如何让模型先检查回答语气 / 质量？
4. 工业图纸识别出现 Hallucination 时，Prompt 与后处理分别怎么治理？
5. Function Calling 从模型输出 JSON 到真实代码执行的完整链路是什么？
6. vLLM PagedAttention 为什么能改善 KV Cache 内存利用？
7. FastAPI Middleware 与 Dependency Injection 分别适合哪些业务逻辑？
8. Python multiprocessing / threading 如何组合；`asyncio.gather` 与 `as_completed` 如何选择并处理超时降级？
9. Context Overflow 除了截断还有哪些压缩 / 精简策略？
10. Multi-Agent 状态同步与 A2A 递归对话如何治理？
11. Coding：实现有复杂度要求的 LRU Cache。

---

## S228 美团｜AI 全栈开发｜一面 + 二面｜面试 2026-04-15 / 04-21，次日 Offer｜HUMAN-A

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

## S229 大疆创新｜AI Agent 开发｜一面｜面试 2026-08-11，发布 08-13｜HUMAN-A

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

## S230 字节跳动｜Agent 开发｜日常实习一面｜面试 2026-08-05，发布 08-09｜HUMAN-A

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

## S231 美团｜Agent 开发｜一面｜面试 2026-08-23，08-25 通知未通过｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/1d067ce539c64d3988eabb9b646ef8a0

真人 / 第一人称证据：作者明确记录 8 月 23 日面试、8 月 25 日收到凉信，以本人 Agent 项目为主线复盘并写“发面经攒人品”。

高价值问题：

1. Agent 项目的整体架构和真实业务目标是什么？
2. RAG 从 Chunk、Embedding、Retrieval 到 Generation 的流程怎么实现？
3. Chunk Strategy 如何选择，不同切分方式怎样影响效果？
4. Multi-Agent 如何分配任务、聚合结果并管理并行状态？
5. Agent Context 如何控制长度并做 Compression？
6. Agent Routing 怎样判断请求该交给哪个 Agent？
7. Java 与 Python 做 Agent 开发各有什么优势？
8. Concurrency 与 Async 有什么区别，异步任务常见实现方式有哪些？
9. Agent Engineering 中 Scheduling、Tool Call、State Management 的常见问题是什么？
10. Vibe Coding 的优缺点是什么；从零设计一个 Agent App 要考虑哪些维度？

---

## S232 大麦｜Agent 开发｜实习一面｜发布 2026-04-22，已挂｜HUMAN-A

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

## S233 阿里云｜后端 Agent 开发｜实习一面｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/10dc395d6a704e1ea22a8fbc0049c7da

真人 / 第一人称证据：作者以本人后端 Agent 实习一面发布并写“给我面没招了”；整场几乎都是系统 / 数据库 / Redis 基础，评论区甚至有人问“这问了 Agent 吗”，正是目标 Agent Backend 真实基础权重证据。

高价值问题：

1. Connect / Read / Write 等常见 Timeout 分别解决什么问题？
2. select / poll / epoll 的核心差异是什么？
3. Red-Black Tree 的特点是什么，OS 哪些机制会用到它？
4. CPU Load 与 CPU Usage 有什么区别；低利用率高 Load 如何排查？
5. `df` 显示磁盘满但找不到大文件可能是什么原因？
6. OS Memory Reclaim 怎么工作，阈值不合理会有什么后果？
7. MySQL Back-to-table 如何发生、如何避免；连接数打满怎样治理？
8. SQL Injection 如何避免；自增 ID 达到上限会怎样？
9. Redis + Lua 怎样保证秒杀扣减原子性，Logical Expire 与 Physical Expire 怎么选？
10. Redis Penetration、Redisson Lock、Sliding-window Rate Limit 怎样设计？

---

## S234 字节跳动｜后台 Agent 开发｜实习二面｜发布 2026-05-01｜HUMAN-A

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

## S235 腾讯｜AI 后端开发｜二面约 50min｜发布 2026-04-01｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f0e993c94c17476180e1a0185a6662f2

真人 / 第一人称证据：作者以本人腾讯 AI Backend 二面发布并写“攒人品”，问题从项目 / 论文进入 Transformer、LLM/RAG/Agent，再落到一致性哈希、并发安全和 Go 学习能力。

高价值问题：

1. Transformer 的弱点是什么，哪些场景下会考虑 Mamba 等架构？
2. LLM、Prompt Engineering、RAG、Agent 的现有实现与优化路径有哪些？
3. Agent 有哪些真正有价值的应用场景？
4. 怎样设计一个 Add / Delete 都为 O(1) 的定时任务触发器？
5. Consistent Hashing 是什么，适合哪些分布式场景？
6. 如何保证系统 Concurrency Safety？
7. 项目中遇到的核心工程难点是什么？
8. 如何快速学习并投入一门新语言，例如 Go？

---

## S236 字节跳动｜Agent 开发｜二面｜发布 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/675f834ce9fa4a29b2c413d87241e6bb

真人 / 第一人称证据：作者以本人 Agent 二面复盘并“发面经攒人品”，问题长期围绕自己的 Coding Agent / Agent Infra 项目，追到 Skill、Memory、Compression、GraphRAG、Training 与 Evaluation。

高价值问题：

1. Coding Agent 的完整执行链路是什么？
2. Skill 如何分层、匹配和沉淀，怎样避免能力无限膨胀？
3. Long-term / Short-term Memory 的边界是什么？
4. LTM 动态更新与静态知识如何并存，Memory 变大后如何 Recall？
5. Context Compression 在什么阈值触发，Token Window 怎样管理？
6. Static Prompt 与 Dynamic Prompt 如何组合？
7. 不同模型选择如何影响 Token Cost 与整体性能？
8. GraphRAG 与普通 Vector Retrieval 的适用场景有什么差异？
9. SFT / DPO / GRPO 等方法分别解决什么问题？
10. Agent / Coding Agent Evaluation 怎样设计？

---

## S237 美团｜后端 Agent 开发｜暑期一面｜发布 2026-04-19｜HUMAN-A

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

## S238 百度｜Coding Agent｜暑期实习技术面｜发布 2026-04-17｜HUMAN-A

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

## S239 京东科技｜AI 后端开发｜二面｜发布 2026-04-06｜HUMAN-A

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

## S240 字节跳动｜AI 全栈研发｜实习一面｜发布 2026-06-05｜HUMAN-A

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

## S241 腾讯｜Agent 开发｜暑期实习一面｜发布 2026-04-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/352203a181fc48d5ab172b6badd8148e

真人 / 第一人称证据：作者以本人腾讯 Agent 暑期一面分享并邀请同岗候选人交流；问题围绕真实 Model Failure、RAG、Agent Loop、Tool Extension 与 MCP 连续展开。

高价值问题：

1. Model Output Failure 有哪些类型，工业界怎样做 Fallback？
2. RAG 数据怎样建立 Vector Index？
3. Chunk Length 怎样权衡？
4. 为什么用 Vector DB，它与 MySQL / PostgreSQL 的职责有什么差异？
5. RAG Recall 怎样 Evaluation？
6. Agent Dead Loop / Repeated Output 如何检测与兜底？
7. Agent Architecture 怎样支持可插拔 Tool？
8. Agent 与单纯 LLM Call 的核心区别是什么？
9. MCP 解决了什么标准化问题？

---

## S242 腾讯｜AI 后端开发｜暑期二面｜发布 2026-04｜HUMAN-A

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

## S243 字节跳动｜AI 应用开发｜一面 + 二面面试官合并场｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c5947496fc29440883611173478dc257

真人 / 第一人称证据：作者明确说明 HR 为加快流程让一面、二面面试官同场，吐槽其中一位面试官同时戴两副耳机；评论里还说明自己没有录音、记忆力一般，所以面经不全，现场痕迹很强。

高价值问题：

1. DAG Orchestration 是怎样实现的，每个 Agent 分别承担什么职责？
2. LangGraph 怎样编排 Graph？
3. Agent / RAG Evaluation 怎样做，Dataset 如何构建？
4. Semantic Chunking 如何实现？
5. Fine-tuning 与 Reinforcement Learning 分别适合什么场景？
6. HNSW Index 如何构建？
7. Multi-file Knowledge Input 怎样处理？
8. ThreadLocal 解决什么问题？
9. LangChain Checkpoint 如何工作？
10. Agent Harness 怎样理解？
11. 项目里的 Perception / Scheduling 如何实现？
12. Coding：Ugly Number；另有现场逻辑题。

---

## S244 滴滴｜AI 后端开发｜日常实习一面 45min｜发布 2026-04-03｜HUMAN-A

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

## S245 阿里巴巴｜AI 应用开发｜27 实习一面｜发布 2026-05-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/038bad2882114c64bc6166eb716e5fce

真人 / 第一人称证据：作者以本人一面分享并写“给我面没招了，发点面经攒攒人品”，问题从 Agent Workflow / Retrieval / Memory 进入 AI Coding 交付、Java Concurrency、Redis/MySQL。

高价值问题：

1. Agent Workflow 链路如何实现，框架控制还是自研代码控制？
2. Agent Extensibility 怎样设计？
3. Image-text Retrieval 与 Semantic Knowledge Base 怎样构建？
4. Tool Call 与 Memory Management 怎样实现？
5. OpenClaw 与自己做的 Agent 有什么差异？
6. Python / Java 如何选择，Cursor / Claude Code 在项目中怎样用？
7. 从需求交给 AI Tool 到最终 Delivery，哪些环节必须人工 Acceptance / Review？
8. AI Generated Code 如何做功能、安全、性能 Review 与 E2E Test？
9. Java HashMap、ReentrantLock、ArrayList Concurrent Write、Exception 应怎样解释？
10. Redis Session 与数据库怎样保持一致，ThreadLocal 用户上下文是否线程安全？
11. MySQL Composite Index 怎样设计？

---

## S246 FOSHO｜AI 应用 / Agent 开发｜一面 30min｜面试 2026-07-16，发布 07-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d95927b94e994681beee22975766721e

真人 / 第一人称证据：作者明确记录 7 月 16 日本人面试、时长约 30 分钟，并说明“零八股，全程问项目”；问题来自其长视频 AI QA 与 Mini Coding Agent 两个真实项目。

高价值问题：

1. Go / Java / Python 分别在哪些真实项目里使用过？
2. Long-video Understanding 从上传到 ASR / Summary / QA 的完整链路是什么？
3. 视频转写调用什么模型 / Service？
4. Long-running Task 怎样异步处理？
5. Large-file Upload、Chunk Upload 与 Resume-from-breakpoint 如何实现？
6. 用户问问题后怎样 Retrieval 相关视频片段并组装 Prompt？
7. 系统怎样从 Single-video QA 扩展成 Multi-video Knowledge Base？
8. Mini Coding Agent 已实现哪些能力？
9. Coding Agent Context Management 怎样设计？
10. 为什么不用现成 Agent Framework，而选择自研；为什么选 Go？

---

## S247 字节跳动｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3e22dc2df03d4227ab70ea9c2d896086

真人 / 第一人称证据：作者保留大量现场失败痕迹：承认项目来自网上、项目产出被面试官说没听懂、多个 Agent 问题“答得不好”、线程池设计答得差、死锁代码没写出来，最后总结自己从开场就觉得凉。

高价值问题：

1. Project Challenge 最大的是什么，怎样证明真实产出？
2. Hallucination 从 Prompt / Tool / RAG / Fine-tuning 哪些层面治理？
3. Prompt 具体怎样约束模型“不知道就不要编”？
4. Short-term / Long-term Memory 怎样实现？
5. 从零设计 Agent 需要哪些 Module？
6. API Timeout / Error 怎样恢复，是否可以让 LLM 自己参与处理？
7. Token Consumption 异常怎样排查？
8. Java ThreadPool 原理是什么，如果重新设计会怎样做？
9. JVM Class Loading 怎样完成？
10. MySQL undo / redo / binlog 与 Two-phase Commit 分别解决什么？
11. Coding：多线程 Deadlock、Singleton、Merge Sorted Arrays。

---

## S248 字节跳动｜Agent 开发｜二面｜面试 2026-07-18，发布 07-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/eccea78e38b447c9a3ae73570c5d00b6

真人 / 第一人称证据：作者明确记录 7 月 18 日、约 1 小时，描述“整体很轻松、基本在聊天”，并保留项目来源、Framework Choice、Memory 和 Coding 等真人对话链。

高价值问题：

1. 两个项目的来源和做项目的动机是什么？
2. Agent Framework 为什么这样选，除 LangChain 外还调研过什么？
3. Agent 包含哪些核心组件，Runtime Mechanism 是什么？
4. Planning 是框架负责还是模型负责，有哪些实现方法？
5. Long-term / Short-term Memory 区别是什么？
6. Function Call Result 是否需要写回 Short-term Memory，不写会怎样？
7. Tool 用自研代码还是 MCP，各有什么优势？
8. RAG Retrieval 参数实际调过哪些？
9. Python 基础能力如何？
10. Coding：合并两个有序数组。

---

## S249 字节跳动｜AI 后端开发｜春招一面｜发布 2026-04-05｜HUMAN-A

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

## S250 携程｜AI 后端开发｜暑期一面 1h｜发布 2026-04-08｜HUMAN-A

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

## S251 腾讯｜Agent 开发｜实习一面｜发布 2026-03-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/86c7a1d799984400905ce219c818515f

真人 / 第一人称证据：作者以本人腾讯 Agent 一面发布并写“给我面没招了”，问题从 RAG 延迟 / Evaluation 进入 Agent Loop / Tool / Plan，再问 Streaming Protocol、Go Concurrency、Lock、MCP/A2A 与 Claude Code。

高价值问题：

1. 完整 RAG System 包含哪些部分，Document Upload / Chunk 怎样实现？
2. Vector Retrieval 单次耗时多少，是否使用 Rerank？
3. Retrieval 与 Query Matching 怎样 Evaluation？
4. Agent 的核心 Module 与 ReAct 范式是什么？
5. Agent Loop 最大步数如何设置，达到 Max Step 仍未完成怎么办？
6. Tool Call 怎样约束模型参数和行为？
7. SSE / WebSocket / HTTP 从协议层如何比较？
8. Go Goroutine 与其他语言 Concurrency 有什么差异？
9. Local Lock / Distributed Lock 分别解决什么问题？
10. MCP、Function Call、A2A 如何区分；是否自己写过 MCP Server？
11. Claude Code / OpenClaw 的实现原理了解多少？

---

## S252 字节跳动｜后端 Agent 开发｜暑期一面｜发布 2026-04-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fa55d9f475624bfb95d943a5c00a599f

真人 / 第一人称证据：作者以本人同岗一面发布并邀请同岗候选人交流；问题围绕“为什么不是单 Agent + 更多 Tool”持续追问到 Multi-Agent、RAG、Structured Context、Failure Handling 与 Latency/Effect Trade-off。

高价值问题：

1. 为什么不在 Single Agent 中继续增加 Tool，而要拆 Multi-Agent？
2. 让模型完全自主选择 Tool / Action 有什么问题？
3. 如果 Agent 可以自主决定结束 ReAct Loop，为什么还需要额外 Orchestration？
4. 业务 Knowledge-base RAG 怎样构建？
5. Retrieval 是 Vector Similarity / Embedding 还是其他方式，Top-K 怎样理解？
6. 为什么不能把所有 Tool 统一 RPC 封装后交给一个 Agent？
7. Multi-Agent 拆分后局部失败怎样处理？
8. 为什么 Context Passing 要用 JSON / Slot 等结构化形式？
9. Retrieval / Recall 的 Evaluation Metric 是什么？
10. Online System 怎样权衡 Response Latency 与 Quality？
11. Coding：Word Break。

---

## S253 虾皮｜AI 后端开发｜日常实习一面｜发布 2026-04-08｜HUMAN-A

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

---

## S254 阿里国际 / Lazada 交易｜Agent 开发实习｜一面 + 二面 + HR｜2026-04-22 / 04-27 / 05-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/40ef1dff3eac4d5ba86bc78372376be3

真人 / 第一人称证据：作者后来实际成为阿里国际 Agent 开发实习员工，完整记录 Boss 内推、4/22 一面、4/27 二面、5/7 HR；入职后甚至发现一面面试官就坐在自己后面一排，招聘流程真实性非常强。

高价值问题：

1. Disk 如何持久化存储信息？
2. Process 与 Thread 的区别是什么？
3. Transformer 基本原理是什么？
4. Multi-head Attention 为什么需要多个 Head？
5. 实习 IM Project 中本人负责什么，具体怎样实现？
6. Agent Customer-service Project 的 RAG 与最终 Answer Generation 怎样实现？
7. 自己修改的 LangGraph Project 中 Memory System 怎样设计？
8. 二面继续追本科 / 科研 / 实习经历与项目 Owner 范围，如何证明本人真实贡献？
9. HR 面如何解释为什么选择 Agent 岗、未来就业方向、最大挫折与最有成就的事？

---

# 本轮明确排除 / 去重

Batch 11 主动扩大了平台和历史月份召回，但以下内容继续保持 **零贡献**：

- 京东后端 Agent 的 04-30 与 05-08 两篇文章出现几乎逐题一致的 12 道问题，当前无法可靠确认哪一篇是真正候选人原场次，因此整条重复链均不进入正式库；
- 滴滴花小猪某 Agent 面经的评论区直接出现“复制粘贴别人的帖子”质疑，无法通过非转载 Gate；
- `AIGC小白入门记`、面经专栏、含“思路参考 / 标准答案 / 完整解析”的内容型页面；
- CSDN / 51CTO / Bilibili / 知乎等平台搜索到的题库、教程、路线、SEO、课程、跨站转载；排除的是具体页面，不是平台；
- Mock Interview / AI 自动面试 / 自动生成题库；
- 个人博客中的模拟面试、一般求职感想、低信息密度 Interview Reflection；即使作者真实，也不满足本项目高密度技术面标准；
- 普通后端 / 前端岗位仅顺带使用 AI Coding，无法证明实际职责属于 AI Application / Agent 的场次；
- 只有搜索摘要、标题或截图，无法稳定打开正文的线索；
- 字节 04-08 同时出现后端 Agent 一面 / 二面近似流程，但无法稳定确认作者关系，本批只保留证据更明确的一面，不擅自合并也不重复计数；
- 不同 URL 但题序 / 项目描述高度相同的后发版本继续按语义重复处理。

# Batch 11 观察

本批新增 `S226–S254` 共 **29 个 HUMAN-A 来源**，当前干净核心样本达到 **254 个**。

本轮最重要的信号：

1. **全知识链路原则继续得到强真人证据。** 阿里云后端 Agent 一面几乎全是 OS / I/O / CPU / Disk / MySQL / Redis；滴滴 AI Backend 几乎全是 MySQL / Redis / Rate Limit；但它们都是明确目标岗位，因此基础工程问题必须和 Harness / RAG 一样完整记录。
2. **Python / FastAPI 已被再次独立确认。** 字节大模型应用一面直接追 FastAPI Middleware vs Dependency、multiprocessing / threading、`asyncio.gather` vs `as_completed`、超时降级，并和 Milvus / RAG / Multi-Agent / A2A 同场出现。
3. **Agent Harness 的考察正在从名词走向控制边界。** 写操作边界、Harness Layer、Intent Routing、Skill Fetch、Tool/API Failure、Dead Loop、Context Compression、Checkpoint、Agent Loop Max Step、Structured Context Passing 都来自真人追问。
4. **AI Backend 的 System Design 权重非常稳定。** 千万 QPS、大促 Capacity Planning、10TB/day Storage、Hot/Cold Separation、Redis Cluster Migration、MQ Backlog、API Rate Limit、Feed Push、Cache Consistency 都在目标 AI 岗里出现。
5. **RAG 越来越像可测量的 Retrieval System。** Milvus Collection / Partition、Chunk、BM25、Rerank、Query Rewrite、Top-K、HNSW、Recall Evaluation、Latency / Quality Trade-off 被持续问“为什么”和“怎么证明”。
6. **项目验真仍是主线。** 面试官会追日调用量、真实用户、项目来源、本人负责范围、性能优化前后指标、业务价值、为什么不用更简单的 Script / Single Agent；候选人现场答不好这些问题往往比背错某个定义更致命。
7. **多平台主动召回是必要的，但不能变成平台配额。** 本轮实际搜索了牛客、小红书、知乎、脉脉、CSDN、B站、抖音、个人博客等；非牛客结果中大量仍是教程 / 转载 / 模拟 / 低密度内容，所以正式入库仍以能稳定核验的 HUMAN-A 为准。某平台本轮 0 入库不代表降权。
8. **去重难度继续升高。** 只按 URL 会把逐题复制链误当独立样本；评论区、作者身份、发布时间和招聘流程都必须继续纳入判断。
9. **仍未达到来源饱和。** 在已有 225 个 HUMAN-A 后，本批严格清洗仍新增 29 个独立来源；虽然泛搜索重复 / 整理率继续升高，精确公司 / 岗位 / 月份 / 轮次搜索仍有明显产出。

停止条件不变：只有连续多轮跨公司、岗位、月份、轮次、平台扩大 Recall 后，**新增 HUMAN-A 的绝对数量与占比都持续接近零**，精确公司 / 轮次 / 作者页 / 原始博客搜索也很难发现新来源，并且新增问题模块与追问深度稳定收敛，才进入最终收尾。当前 254 个样本仍未达到停止点。
