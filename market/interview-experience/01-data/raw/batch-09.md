# Batch 09 一手面试流程

采集日期：2026-09-10

## S160 字节跳动中国交易与广告｜Agent 后端开发｜秋招业务终面｜面试 2026-08-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1dd33c4b7bda453a82f7d645bde7f3ff

真人 / 第一人称证据：候选人说明暑期已拿该部门 Offer 但未入职，秋招由 HR 保留原流程、只增加一次业务终面；本轮围绕新增蚂蚁 Agent Infra 实习持续深挖，面后约两小时通过并等待后续通知，时间线非常明确。

高价值问题：

1. 蚂蚁实习中的 Agent Infra 从输入到执行的完整链路是什么？
2. Infra 为什么能提升 Agent 能力，真正的工程难点在哪里？
3. 平台做过哪些优化，哪一项最有挑战，收益怎样证明？
4. 探索型 Agent 项目具体解决什么问题，为什么值得做？
5. Go GMP 如何支撑高并发 Runtime？
6. Redis Cache 在 Agent Backend 中如何使用与治理？
7. Coding：课程表变体，除了判断可行还要输出一条合法路径。

---

## S161 字节跳动｜AI 全栈工程师｜秋招一面 + 二面｜2026-09-01 / 09-08｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/034e6ed3a28f463abbc3465dd1e4ad2f

二面来源：https://www.nowcoder.com/feed/main/detail/0a926033572f4a68b8c537f20a013503

真人 / 第一人称证据：同一候选人一面后明确更新通过并约二面；二面 9 月 8 日前置 2 小时 AI 作业，随后对方案连续拷打约 20 分钟，并保留算法卡壳和面试官反馈。同招聘流程合并计一个来源。

高价值问题：

1. 缓存穿透 / 击穿 / 雪崩与 Redis / DB 一致性如何治理？
2. 库存少卖或扣减失败时如何根据订单状态补偿？
3. LLM 与 Agent 的本质区别是什么？
4. ReAct 与 Plan-and-Execute 分别适合什么任务？
5. AI 前置作业如何从模糊需求中自主梳理功能、边界和技术方案？
6. 面试中怎样解释 AI 辅助完成作业时本人真正负责的设计和验证？
7. Kafka Message Consistency 如何保证？
8. API Idempotency 怎样设计？
9. 如果设计一个 Notification Platform，怎样处理可靠投递、重试与去重？
10. Coding：随机链表复制、Tree Maximum Independent Set 等。

---

## S162 蚂蚁｜AI 应用开发｜暑期二面 65min｜发布 2026-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/601233a9e7c54235895bdd09fb449eca

真人 / 第一人称证据：作者记录约 65 分钟二面，围绕本人文档解析 / RAG / Agent 实习与论文持续追问，并明确复盘“面试很难、很多地方需要继续练习”。

高价值问题：

1. MinerU 等文档解析方案如何保持跨页表格语义完整？
2. RAGAS / Answer Relevance 等指标出现问题时如何定位到底是 Retrieval 还是 Generation？
3. LangGraph State 如何定义和传递，Node 很多时怎样避免 State Object 膨胀甚至 OOM？
4. Long-term Memory 中结构化用户画像如何设计、更新和失效？
5. Chunk Overlap 过大 / 过小分别有什么副作用？
6. GraphRAG、Self-Reflection、CoT 分别解决什么问题？
7. Tool Parameter Hallucination / 格式错误如何自动校验和修复？
8. Multi-Agent 中央协调与 P2P 协作怎样取舍？
9. 支付等高风险操作中 Human-in-the-loop 应放在哪里？
10. Skill 与 MCP 如何分工，OpenClaw 类 Agent 的文件系统 / 环境 / 权限如何治理？
11. Context Cache 怎样减少重复 System Instruction 成本？

---

## S163 阿里高德｜AI 应用开发｜一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/87f26b7a710b4314a89134bf032ed58f

真人 / 第一人称证据：作者以本人同岗面经发布并“攒人品”，问题围绕其代码理解 / RAG 项目从 AST、Schema、Retrieval 一路追到 Skill、Memory 和 Agent Loop。

高价值问题：

1. 如何从 Requirement Document 判断某项功能在代码库中是否已经实现？
2. AST 的核心思想是什么，源码到 AST 的转换怎样工作？
3. Code RAG 中代码、注释、文件 / Symbol Metadata 应怎样建模？
4. Single-round 与 Multi-round Retrieval 分别适合什么代码检索场景？
5. RRF 为什么适合融合多路召回，权重 / 参数如何调？
6. Coarse-to-fine Rerank 如何减少成本同时保持 Recall？
7. Markdown / PDF 与代码文件应该采用怎样不同的 Chunk 策略？
8. Long-context Agent 还能否直接用普通 Chunking，什么时候要改成任务导向的检索？
9. Skill 与 MCP、Memory 与 Short-term Context 如何区分？
10. ReAct 与通用 Agent Loop 的关系是什么？

---

## S164 字节跳动｜Agent 后端开发｜日常实习二面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c1cac9b1d1e14fafa6b25afb177e7c17

真人 / 第一人称证据：作者明确记录本轮为二面并更新被横向淘汰；题目从 MQ / Streaming / Auth 连续进入 Agent、RAG、Context、Skill 与 Redis，另有一篇高度同题版本按重复处理，不重复计数。

高价值问题：

1. MQ 中如何把异步处理结果准确关联回原请求？
2. 为什么某些异步链路选择 MQ 而不是直接通过数据库传状态？
3. Agent 前端 Streaming 输出怎样实现，身份认证放在哪一层？
4. LangChain / LangGraph 分别提供什么能力，工程边界在哪里？
5. ReAct、Tool Call 与 Multi-Agent Collaboration 如何串成完整执行链？
6. Context Engineering 与 RAG / Persistent Memory 的边界是什么？
7. CoT 在 Agent 中有什么价值和限制？
8. Rules / Instructions、MCP、Skill 分别解决什么问题？
9. SSE 与普通 HTTP / 其他传输方案怎样比较？
10. Redis Rate Limit 如何实现，Redis 为什么适合高频状态与限流？

---

## S165 阿里｜AI 应用开发｜一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6cf457434a6a4cd9b1b9951cf1b6b513

真人 / 第一人称证据：作者以本人 AI 应用一面发布并邀请同岗交流；问题从文档 RAG 连续进入 LangGraph、Kafka Backlog、Text-to-SQL 和 AI Tool 使用，具有自然项目追问流。

高价值问题：

1. 文档 Chunk 应如何设计并验证？
2. Hallucination 出现时怎样判断根因是不是 Retrieval 质量差？
3. Vector DB 如何选型？
4. LangGraph State 如何存储与流转，为什么选择 LangGraph 而不是 LangChain？
5. Kafka 出现 Backlog 时如何区分流量激增、Partition 不均或 Consumer 能力不足？
6. Telemetry / Event Consumption 怎样保证顺序和可恢复性？
7. Text-to-SQL 如何处理 Schema、Query Planning 和自然语言歧义？
8. 日常使用哪些 AI Coding / AI Tool，怎样验证生成结果？

---

## S166 同花顺｜Agent 开发｜实习一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e92546db48fd42e19ed312b21ec903c9

真人 / 第一人称证据：作者按实习提问、项目、八股、Coding、AI 闲聊分别记录时长，完整保留一面流程；企业页核验显示其与同日二面帖不是同一候选人，因此独立计数。

高价值问题：

1. C++ Destructor 为什么经常需要是 Virtual，空类编译器会生成哪些默认成员？
2. TCP/IP 分层如何理解，IP 与 UDP 分别解决什么问题？
3. Datagram 与 Stream Protocol 的语义差异是什么？
4. 什么场景适合 Process，什么场景适合 Thread？
5. 常见 IPC 方式有哪些？
6. Coding：Search a 2D Matrix II。
7. 日常开发使用 AI Coding 的深度如何证明？
8. MCP Service 未来还有哪些工程空间？
9. OpenClaw / Agent 产品的实际使用经验是什么？

---

## S167 同花顺｜Agent 开发｜实习二面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e13a1970daa84af988d2f7dda473f3f4

真人 / 第一人称证据：作者明确记录项目拷打约 30 分钟、场景题约 10 分钟、AI 工具交流约 10 分钟，并自评业务逻辑表达不好；企业页显示与 S166 账号 / 学校不同，是另一位独立候选人。

高价值问题：

1. 广告效果引擎从数据生产到在线使用的完整业务链是什么？
2. Forward Data 如何转换成 Inverted Index / Cache？
3. 为什么不用 Java BitSet，序列化超大对象时怎样降低反序列化成本？
4. 千万级广告库如何分片并支持 Horizontal Scaling？
5. Worker / Manager Heartbeat 模式中 Manager 故障怎样处理？
6. 自定义 TCP Protocol 如何解决 Sticky Packet / Half Packet？
7. 高并发股票搜索如何同时支持代码、名称、拼音首字母以及前 / 中 / 后匹配？
8. Trie 对中文与 Infix Search 的实现边界是什么？
9. 日常 AI Coding Workflow 如何组织？
10. OpenHands 类 Coding Agent 的架构了解多少，Skill 与 MCP 有什么区别？

---

## S168 字节跳动｜后端 Agent 开发｜实习一面 1h｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d73020680b3b42c3ac579e2f25721d90

真人 / 第一人称证据：作者以本人“字节后端 Agent 开发实习一面 1h”发布，问题沿真实 RAG 项目连续追设计理由与失败案例，而不是背 RAG 流程；尤其会追候选人自己加的“小结”为什么反而降低 Recall、为什么只 Embedding 标题，以及 Skill 是否真能替代 Tool。最后有现场 Coding。

高价值问题：

1. 当前 RAG 与传统 RAG 有什么真正的 Innovation / 落地差异，还是只是把标准方案实现了一遍？
2. RAG 效果怎样 Evaluation，失败应如何 Attribution？
3. 给文档额外生成“小结”后反而导致召回率下降，可能的负向机制是什么？
4. 为什么只对标题做 Embedding，而不是对段落正文一起做 Embedding？这种策略的 Recall / Precision 代价是什么？
5. Prompt Engineering 与 Context Engineering 的本质区别是什么？
6. 当前热门的 Skill 概念到底解决什么问题？
7. Skill 与 Tool / Function Call 的职责边界是什么？
8. Skill 能否覆盖 Tool、从而完全不需要 Tool？为什么？
9. 所谓“Skill 替代 Function Call”在实现层究竟怎样发生，哪些执行仍必须由确定性 Runtime 完成？
10. Coding：非递归实现 Binary Tree Preorder Traversal。

去重：URL、作者和 4/19 字节流程未入库；“RAG 小结造成 Recall 下降 → 标题-only Embedding → Skill 是否覆盖 Tool / Function Call”连续题序未在历史来源发现。

---

## S169 蚂蚁｜后端 Agent 开发｜暑期一面｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/334690a445be4db3b5ac63207a507572

真人 / 第一人称证据：作者明确以本人“蚂蚁暑期后端 Agent 开发一面”发布，问题从项目和 Agent 认知继续进入单机锁到大规模分布式并发的逐层扩展。

高价值问题：

1. 介绍并深挖本人项目。
2. 对 Agent 的理解是什么？
3. 后端项目整体是怎样设计和实现的？
4. `synchronized` 用在业务方法上除了阻塞多用户访问，还有什么问题？
5. 如果可以接受性能变慢，单机 `synchronized` 能否保证秒杀场景的正确性？
6. 同一业务扩展到上万台机器后，原来的单机锁方案会发生什么变化？
7. Redis 分布式锁的 Key 应怎样设计？

---

## S170 腾讯｜后端 AI 开发｜日常实习一面 1h｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/77d7da4a1e234435a256a864dc861185

真人 / 第一人称证据：作者以本人同岗一面发布并邀请同岗交流，问题从 Canal / Event Processing 进入 SSE、RAG / Vector DB，再进入 Go / Network 与现场 Coding，信息链完整。

高价值问题：

1. Canal 如何配置，如何识别 DDL / DML / DCL 事件？
2. SSE 与普通 HTTP Request / Response 的语义有什么不同，SSE 是否单向？
3. RAG 项目整体架构是什么，为什么选择 Eino 等框架？
4. Vector DB Index 怎样设计，Retrieval 返回文档 ID 还是内容？
5. OSI 七层与 TCP/IP 四层如何对应？
6. TCP 三次握手与四次挥手为什么这样设计？
7. Go `error` 与 `panic` 怎样区分，`defer` / recover 如何配合？
8. Go Context 可以承担 Cancel / Deadline / Value 哪些职责？
9. Gin 与 Kratos 等 Web / Microservice Framework 怎样选型？
10. Coding：Linked List Cycle，并自行构造输入输出。

---

## S171 腾讯｜后端 AI 开发｜一面｜发布 2026-04-12｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/db9014c0dcad4d4d985427e330dc1461

真人 / 第一人称证据：作者明确写“给我面没招了”、自评面试困难；问题从 Agent / RAG 进入 Streaming、DDD、Redis Session、Auth、Cache Consistency 和 Coding，属于目标 AI Backend 场次。

高价值问题：

1. 从零构建 Agent Service 应有哪些核心模块？
2. Agent Failure 时怎样 Retry / Fallback / Degrade？
3. RAG 在项目中具体承担什么职责？
4. SSE 与 WebSocket 的差异是什么，各自适合什么 Streaming 场景？
5. DDD 在真实项目里如何划分 Domain / Application / Infrastructure？
6. 多实例服务怎样共享 Session，Redis 在其中怎样使用？
7. Access Token / Refresh Token 与 Authentication Flow 如何设计？
8. Cache Aside 与 Delayed Double Delete 怎样理解，延迟窗口如何确定？
9. Mutex、Bloom Filter 与 Redis Lua 分别适合解决什么一致性 / 原子性问题？
10. Coding：Maximum Subarray。

---

## S172 字节跳动 TikTok｜后端 AI 开发｜实习一面｜发布 2026-05-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/98deba451f18417990758d9136dae164

真人 / 第一人称证据：作者以本人一面继续分享近期流程，问题从 Agent 项目逐步进入 MCP / RAG、LLM API、DDD、Streaming、HashMap、B+Tree、RabbitMQ 与 Coding。

高价值问题：

1. Agent 项目解决什么问题，完整执行链怎样实现？
2. MCP 与 RAG 分别解决什么问题？
3. Application Backend 如何调用不同 LLM Provider？
4. DDD Architecture 怎样组织 AI Service？
5. 为什么 AI Response 常采用 Streaming？
6. 正常 LLM API Latency 大概由哪些阶段构成？
7. HashMap 与 B+Tree 的底层结构如何解释？
8. RabbitMQ 在异步 AI Backend 中适合承担哪些职责？
9. Coding：找到最短需要排序的连续子数组。

---

## S173 腾讯｜后端 AI 开发｜实习面经｜发布 2026-04-28｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a99d5b46ab7848f992d8ae48a60c009c

真人 / 第一人称证据：作者记录整体面试体验、最终没有后续，并保留“协程只了解携程”的现场自嘲；问题跨实习数据治理、RAG、Network / DB 和 Agent / MCP / Skill。

高价值问题：

1. 实习数据的 Accuracy 与 Timeliness 怎样保证？
2. Metadata / Data Lineage 如何构建并治理？
3. RAG 的完整链路是什么？
4. Process 与 Thread 怎样比较，线程是不是越多越好？
5. CPU 到 Memory 的访问链路怎样理解？
6. TCP 为什么要三次握手，Congestion Control 如何工作？
7. HTTPS 相比 HTTP 增加了哪些协议与安全机制？
8. SQL Slow Query / Index Hit 怎样判断，常见 Index Invalidation 有哪些？
9. Binlog / Redo Log 分别承担什么职责？
10. LLM 与 Agent、MCP 与 Function Calling、Skill 与 Prompt Engineering 如何区分？

---

## S174 小米｜后端 AI 开发｜实习一面 1h｜发布 2026-04-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d856bd790ee24a3c8274a9901c679963

真人 / 第一人称证据：作者以本人一小时 AI Backend 面试分享发布；问题按实习项目 → Redis / MQ → 高并发 → MySQL / Spring → AI Coding / SDD 自然展开。

高价值问题：

1. 为什么项目用 Redis Queue 而不是 RocketMQ，快速上线与可靠性如何权衡？
2. Redis Queue 消息可能丢失时，怎样通过持久化 / 扫描补偿兜底？
3. QPS 上升后读压力如何治理，Cache / WebSocket 等方案怎样选择？
4. Redis HotKey 怎样产生和治理？
5. Bloom Filter 的 False Positive 语义是什么？
6. MVCC 中 Hidden Column、Undo Log、ReadView 如何协作？
7. Spring Circular Dependency 为什么能通过三级缓存处理一部分场景？
8. 公司里怎样使用 AI Coding，同时保证代码规范？
9. SDD / Spec-driven Development 对 AI Coding 有什么工程价值？

---

## S175 美团｜AI 全栈开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6d61c76b76ae4213a21b80de8d2c60d7

真人 / 第一人称证据：作者以本人 AI 全栈一面“攒人品”发布；问题从 Network / Process / DB Index 连续进入项目 Degrade 和 Claude Code / Skill / Hook / MCP。

高价值问题：

1. TCP 四次挥手最后一个 ACK 丢失会发生什么，对后续连接有什么影响？
2. Process、Thread、Coroutine 的核心区别是什么？
3. B+Tree 与 B-Tree 为什么在数据库场景表现不同，为什么不用 Red-Black Tree？
4. Optimistic Concurrency Control 如何理解，B+Tree Leaf Split 如何处理？
5. Index Invalidation、Covering Index、Back-to-table 如何联系起来？
6. 项目中的 Circuit Breaker / Degrade 怎样设计？
7. Claude Code 的核心机制、代码执行、Skill 和 Hook 如何理解？
8. MCP 与 Skill 的职责边界是什么？
