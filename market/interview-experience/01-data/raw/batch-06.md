# Batch 06 一手面试流程

采集日期：2026-09-09

## S095 钉钉｜后端 AI 研发｜暑期一面 1h｜发布 2026-04-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/27171d436e7b4ee0a0c5ef3414c18d8b

真人 / 第一人称证据：候选人以本人暑期一面形式记录约 1 小时项目深挖，问题围绕自己做过的 OCR / 文档理解 / Retrieval 工程逐层展开，顺序具有真实面试流。

高价值问题：

1. 文件识别为什么采用 OCR，而不是只依赖 PDF / DOCX 解析 API？
2. OCR 如何处理文本和图表，识别 / 语义保真效果怎么评估？
3. Embedding 为什么使用当前向量维度，维度变化有什么权衡？
4. Embedding Model 的 Tokenization 与 Backbone 如何理解？
5. 模型参数规模与显存 / 推理资源有什么关系？
6. ES / BM25 与 Milvus 向量召回如何组合？
7. Rerank 的原理是什么，应该怎样评价重排效果？
8. Function Calling、MCP 与 Skill 的区别和使用场景是什么？

---

## S096 字节跳动｜AI 后端开发｜暑期二面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a7169bcbc4554deba204cac4349c6a43

真人 / 第一人称证据：作者以本人二面记录发布并写“发点面经攒人品”；面试官连续要求证明 QPS 指标、调试现场代码并解释方案优缺点，真人互动明显。

高价值问题：

1. 项目模拟的数据规模和 QPS 是多少？
2. 简历里的“高峰 QPS 提升 4 倍”具体怎样测出来？
3. 针对当前用户量级做了哪些性能优化？
4. 工程项目中遇到过什么真实问题？
5. Coding：用给定数字集合构造小于目标 N 的最大数，并写边界测试。
6. 测试失败后如何打印结果、定位并现场修改？
7. 怎样评价刚写程序的实现逻辑、优点和缺点？
8. HTTPS 的完整请求过程是什么？
9. 高流量分布式请求如何做 Load Balancing，DNS / Nginx 各有什么优缺点？

---

## S097 字节跳动｜后端 AI 开发｜实习一面 1h｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ab0601f3dbad49ab87ea870a00bb3691

真人 / 第一人称证据：作者 `想奋斗的柠檬精天天摸鱼` 明确写“27实习-字节后端ai开发一面 1h / 发点面经攒攒人品”。问题从 Smart Ops Agent 的真实含义、Spring AI Alibaba 覆盖边界、Planner/Executor/Supervisor 架构，连续追到 RAG / Fine-tuning、MySQL/Redis 和万级 Producer / Consumer 并发场景。

整场技术问题：

1. Agent 项目的核心功能是什么？
2. “智能运维助手”的运维具体指什么业务动作？
3. 系统有哪些主要组件，数据 / 控制流怎样走？
4. Spring AI Alibaba 覆盖了哪些部分，哪些 Runtime 能力仍需自己实现？
5. Planner / Executor / Supervisor Pattern 的优势是什么？
6. 三个 Agent 与一个 Agent 相比，关键收益和额外代价是什么？
7. RAG 的核心流程是什么？
8. Recall / Rerank 使用什么算法；如果没做 Rerank，为什么？
9. 为什么当前业务需要 RAG？
10. Model Response Bad Case 应怎样从 RAG 层优化，又在什么情况下考虑 Fine-tuning？
11. Fine-tuning 属于 Pre-train 还是 Post-train，应用工程师需要理解哪些边界？
12. MySQL 与 Redis 各自适合什么数据 / 访问模式，“Relational”是什么意思？
13. Redis 能否承担持久存储，而不仅是 Cache？
14. System Design：1 万 Producer、5 万 Consumer 的 Java 生产消费模型怎样做并发控制、队列、背压与资源治理？

去重：同作者 4 月还有其它公司独立招聘流程，可以分别计数；同作者 4/21 另有字节相关页面，但与 5/4 同公司、同招聘季且流程关系无法稳定拆分，本批只保留能独立成立、信息更完整的 5/4 一面，不对 4/21 另行编号或补题。历史字节样本没有当前“Spring AI Alibaba → 3-Agent vs 1-Agent → RAG/Fine-tuning → 万级 Producer/Consumer”连续链。

---

## S098 字节跳动｜AI Agent｜实习二面｜发布 2026-03-22｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/d31969d954a94f1cb1bb06abc3196fe9

真人 / 第一人称证据：作者以本人二面复盘发布并写“攒攒人品”，问题从自己的多模态 / Agent 项目继续追到 Memory、Multi-Agent、SSE、RAG Evaluation 和 MCP。

高价值问题：

1. 多模态大模型在项目里如何使用？
2. Agent Skill 是什么，项目中如何使用？
3. Agent Memory 能力不足时可以怎样增强？
4. Multi-Agent 如何选择和切换不同执行策略？
5. SSE 有什么限制？
6. RAG Knowledge Base 动态更新怎么做？
7. 复杂任务的 Agent 准确率怎样评价？
8. 多轮对话如何处理历史上下文？
9. RAG Evaluation 怎样做？
10. MCP 与 Function Calling 有什么区别？

---

## S099 小红书｜Agent 后端开发｜日常实习二面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/be9b14f9b1cf4fe09111b856c4f89608

真人 / 第一人称证据：作者明确以本人二面分享并写“攒人品”，问题数量不多但持续围绕实习项目中的 Prompt、Agent、RAG、多模态与 OpenClaw，并有现场 Coding。

高价值问题：

1. 项目里的 Prompt Engineering 结构怎样设计？
2. 常见 Agent 范式有哪些？
3. RAG 流程可以从哪些环节优化？
4. 多模态对齐流程怎样理解？
5. 如何看待 OpenClaw 一类 Agent 产品？
6. Coding：分批淘汰类算法问题。

---

## S100 腾讯｜AI 后台开发｜日常实习一面｜发布 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/793e6ceb32c74c2ea1137106f661ae2e

真人 / 第一人称证据：候选人明确以同岗本人一面分享并邀请同岗交流；问题从自己的 Kafka / Redis / TDengine 项目进入 Coding、Agent 基础和安全设计。

高价值问题：

1. Kafka 怎样保证消息尽量不丢？
2. Redis 删除某 Key 与另一个并发写入该 Key 同时发生时怎么处理？
3. TDengine 的底层数据结构是什么，为什么适合时序数据？
4. 如何快速排查代码运行问题？
5. Coding：实现支持扩容的 HashMap，包括 Put / Get / Remove / Resize。
6. LLM、RAG、Agent、Skill 等概念怎样区分？
7. Prompt 应如何设计？
8. 登录业务怎样保证通信和数据安全？
9. 为什么 MD5 本身不够安全，怎样完善？

---

## S101 美团｜后端 AI 开发｜暑期一面｜发布 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4a18e41893f1491fae094650eda78d6d

真人 / 第一人称证据：作者以本人同岗一面分享，问题从 RAG 项目一路追到 Tool Failure、Agent Interrupt、隐私、AI Coding 大仓库和模型基础，属于目标 AI Backend 场次。

高价值问题：

1. RAG 如何构建，Vector DB 为什么这样选？
2. Metadata Filter、Hybrid Retrieval、Rerank 怎样使用？
3. Retrieval Recall / Evaluation 怎样做？
4. Tool 调用失败或存在顺序依赖时怎么处理？
5. Agent 如何支持中断？
6. 用户规模上升时 Agent Service 会遇到什么问题？
7. 十万级文档的 RAG 如何处理隐私和 Hallucination？
8. AI Coding 面对超大 Repo、Token 不够时怎样选择相关代码？
9. Transformer 除了 QKV 还应该理解哪些机制？
10. Skill、Tool、MCP、OpenClaw 等概念如何区分？

---

## S102 腾讯｜AI 后端开发｜二面 50min｜发布 2026-04-01｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f0e993c94c17476180e1a0185a6662f2

真人 / 第一人称证据：作者以本人腾讯 AI 后端二面复盘发布并写“攒人品”，问题从项目 / 论文进入 Transformer、LLM Application、Agent 与系统设计，面试时长明确为 50 分钟。

高价值问题：

1. Transformer 的主要局限是什么，可以从哪些方向优化？
2. Transformer 与 Mamba 的适用场景如何比较？
3. LLM、Prompt Engineering、RAG、Agent 在真实项目里分别如何实现和优化？
4. Agent 有哪些真正值得落地的应用场景？
5. 怎样设计一个 Add / Delete 都为 O(1) 的定时任务触发器？
6. Consistent Hashing 的原理和适用场景是什么？
7. 怎样保证系统并发安全？
8. 项目遇到的真实工程难点如何定位和解决？
9. 如何快速学习并投入使用新的工程语言，例如 Go？

---

## S103 淘天｜AI 应用开发｜一面｜发布 2026-04-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e6bd714a536b4723b67f97631b174f60

真人 / 第一人称证据：作者以本人淘天 AI 应用一面发布“发面经攒人品”，并记录现场压力和多个 AI Coding 环节；问题从 RAG / Harness 连续进入 Agent 自纠错、Sandbox、Prompt Attack、Multi-Agent 与真实用户量，符合目标岗位且非答案型文章。

高价值问题：

1. RAG 的完整链路是什么，当前项目为什么需要它？
2. 如何理解 Agent Harness，它与 Agent Framework 的关系是什么？
3. Hermes 类 Agent 的 Self-correct / Self-evolve 怎样实现？
4. LLM 原有知识与 RAG 检索事实冲突时如何处理？
5. MCP 在 Tool Integration 中解决什么问题？
6. Agent Sandbox 怎样隔离代码 / Shell / 文件等高风险操作？
7. 智能客服里 ReAct 与固定 Workflow 怎样选择？
8. 当前 Agent 的主要限制和 Failure Case 是什么？
9. Prompt Attack / Prompt Injection 如何防护？
10. Multi-Agent 为什么需要，Agent 间如何协作？
11. 项目是否真实部署、用户量多少？
12. AI Coding：多轮现场编码任务，考察生成、修改和验证能力。

去重：URL、作者与题序未在旧来源出现；与其它阿里系来源为独立候选流程。

---

## S104 阿里国际｜AI 应用研发｜暑期一面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6d98fa8b5b8e4832a982c0c12a0fdc6d

真人 / 第一人称证据：作者 `励志搞钱大鹅` 以“发一下问题给大家参考，攒攒人品”记录本人流程；与 `S261` 是同一真实候选人，但公司不同、招聘流程独立，因此分别计数。本场从项目验真进入 Java / JVM / RabbitMQ / Redis，再回到 RAG、系统并发与现场 Coding，是典型 AI Backend / AI Application Engineering 组合。

整场技术问题：

1. 深挖项目业务和本人职责。
2. Java HashMap 底层结构是什么，JDK 8 做了哪些优化？
3. JVM Memory Area 有哪些，各自职责是什么？
4. 项目主要是本人手写还是借助 AI Coding，边界怎样证明？
5. 平时使用哪些 AI Coding Tool？
6. RabbitMQ 在项目中的完整 Consumption Flow 是什么，怎样保证 Message Reliability / No-loss？
7. Redis 在项目中使用在哪些场景？
8. ZSet 的底层数据结构是什么？
9. RAG 的整体流程是什么？
10. RAG Retrieval Quality 很差可能有哪些原因，应怎样分层解决？
11. 系统突然收到大量并发请求时，可能出现哪些瓶颈，怎样保护服务？
12. 如果重新设计当前系统，最值得优化哪些地方？
13. Coding：Merge Intervals。

去重：URL、作者的阿里国际流程与“HashMap/JVM → RabbitMQ Reliability → Redis/ZSet → RAG Failure Attribution → High Concurrency → Merge Intervals”题序未在历史阿里国际样本形成同场重复。

---

## S105 深信服｜AI 全栈开发｜二面｜面试 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7fd4389e0a0844faa4dce49ba5e5c3f1

真人 / 第一人称证据：作者以本人二面复盘发布，评论区继续许愿 HR 面；面试官沿三层缓存、Redis / MySQL 一致性、分布式锁和开源 Agent 子 Agent Token 统计持续追问，项目链完整。

高价值问题：

1. 三层 Cache Hierarchy 为什么这样设计，重启后如何恢复状态？
2. Redis 与 MySQL 不一致时如何修复，为什么某些链路选择先写 Redis？
3. Cache Hit Rate 等项目指标如何证明有效而不是拍脑袋？
4. 基于注解的锁封装如何避免通用性不足和 Deadlock？
5. OAuth2 改造如何落到真实服务边界？
6. Agent Token Accounting 为什么容易漏算 Sub-agent / Tool Call？
7. Main Agent 断连但 Child Agent 延迟退出时，如何做补偿和资源回收？
8. 多 Sub-agent 并行更新 Token / Usage 统计时怎样避免 Race Condition？
9. 主 Agent 与 Sub-agent 如何通信并保持 Task State 一致？
10. RAG Tool 加入后会给 Token Accounting / Context Tracking 带来哪些额外复杂度？

---

## S106 OPPO｜后端开发（实际 Agent 方向）｜两轮技术面｜面试 2026-05-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/09fd6466f3f64e7dbfb5a09ed9d660a4

真人 / 第一人称证据：作者明确写最终 OC，并特别说明“与其说后端，更像 Agent 开发，基本只问 AI 相关”；两轮均围绕 Agent 技术和项目取舍，符合 Role Scope 的实际内容优先原则。

高价值问题：

1. Context Window 不够时怎样处理？
2. 长论文、算法说明和知识检索一起造成巨大 Context 时如何拆任务？
3. MCP 与 Skill 有什么区别？
4. 怎样设计一个 Skill 去约束模型角色与行为？
5. Multi-Agent 的协作方式可以怎样设计？
6. Leader Agent 模式与平级协作模式怎样取舍？
7. 多 Agent 之间如何传递上下文与任务信息？
8. 怎样证明 Agent 项目中的关键设计是本人真正做过的？

---

## S107 字节跳动｜Agent 开发｜实习一面 + 二面（同一候选人同流程合并）｜发布 2026-06-17 / 06-23｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/075c06bf50a143a785c039f9951624f6

二面来源：https://www.nowcoder.com/feed/main/detail/675f834ce9fa4a29b2c413d87241e6bb

真人 / 第一人称证据：两篇均由作者 `Ariasu` 发布，作者主页只有这两篇求职记录；公司、岗位、项目和时间线连续，一面 6/17，二面 6/23，明确属于同一字节 Agent 招聘流程，因此只计一个 `Sxxx`。一面持续追 Context 三层压缩、会话恢复、Skill / Tool、Multi-Agent 与 RAG 增量知识，二面继续追 Memory 生长、Token 成本、GraphRAG 与 SFT / DPO / GRPO。

整场技术问题：

### 一面

1. Claude Code 与 Codex 各自有什么特点？
2. 一次请求给模型的 Prompt / Context 由哪些部分组成，哪些必须注入？
3. 自己的 Coding Agent 与 Claude Code / Codex 的本质差异是什么？
4. Context Compression 怎样做？为什么采用三层压缩策略？
5. 三层压缩各自压什么、在什么条件触发？
6. 怎样发现“压缩过度已经伤害任务效果”，如何恢复？
7. 用户在旧任务上继续加功能时，怎样恢复 Session，哪些状态必须重新注入？
8. Tool Calling 完整链路是什么，Skill 能否替代 Tool？
9. Skill 体系怎样设计，模型实际调用 Tool / Skill 的次数怎样观测？
10. 复杂任务的 Planning 怎样生成和更新？
11. Multi-Agent Orchestration 怎样实现，各 SubAgent 有何区别？
12. SubAgent 是否应该共享全部 Tools，为什么？
13. 第二个 RAG 项目的数据源是什么，入库前怎样清洗冗余噪声？
14. PDF 各种结构怎样解析，是否做 Knowledge Extraction？
15. Knowledge Base 增量更新怎样实现？
16. 多文档内容冲突怎样解决，如何做版本控制和错误文档 Rollback？
17. Coding：0/1 Grid 中判断左上到右下是否存在可行路径。

### 二面

18. Coding Agent 从输入到执行的完整 Chain 是什么？
19. Skill 分层体系怎样实现，用户输入怎样匹配相关 Skill？
20. Skill 是否可以从执行轨迹自动沉淀，还是只能人工构造？
21. Long-term / Short-term Memory 怎样设计；为什么还区分 Static / Dynamic Long-term Memory？
22. 每轮都可能写 Memory 时，怎样避免长期记忆快速膨胀？
23. LLM 怎样决定是否 Recall 某条长期记忆？
24. Context Compaction 的 Token Window / Trigger Threshold 怎样定，为什么？
25. Dynamic Prompt 与 Static Prompt 有何区别？
26. 模型底座如何选；生成约 1000 行代码需要多少 Token / Cost，是否真正量化过？
27. 为什么 Agent Cost 会达到当前水平，哪些环节最耗 Token？
28. 为什么当前项目需要 GraphRAG，而不是纯 Vector Retrieval？
29. 什么问题才算 Multi-hop / Reasoning Query？
30. Llama3、SFT、DPO、GRPO 等训练 / 对齐方法在当前项目里理解到什么深度，Data 与 Evaluation 怎样设计？

去重：两 URL 均未在 `S001–S247` 出现；同作者同公司同项目明确合并。独特的“三层 Context Compression → 压缩质量检测 / Session 恢复 → Skill 调用次数 → RAG 版本回滚 → 二面 Memory Growth / Token Cost → GraphRAG → Alignment 方法”连续链未在历史字节来源出现。

---

## S108 懂车帝｜Agent 开发｜一面｜发布 2026-08-13｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/8d84590d7efe4c78943b28708b4395f2

真人 / 第一人称证据：作者明确记录“已挂”，并疑惑“不匹配为什么还面了一个小时”；问题高度场景化地围绕生产 Agent 的 Trace、日志、Multi-Agent 切分和 Regression 展开。

高价值问题：

1. 用户描述模糊时 Agent 怎么优化？
2. Leader Agent 怎样判断问题位于调用链的哪个位置？
3. Trace ID 在 Agent 定位链路问题时如何使用？
4. 不同 Case 走不同链路时，怎样识别对应配置和处理路径？
5. 查问题只依赖 Trace 还是也需要日志？
6. 上游错误日志级别不准确时，会不会误导 Agent？
7. Multi-Agent 承担什么工作，按什么粒度拆分？
8. 不同业务线不断增加 Agent 会不会导致 Agent 数量失控？
9. 模块增删后怎样同步维护 Agent，并保证代码修复没有破坏其他 Case？
10. Coding：LRU Cache。

---

## S109 字节跳动｜AI 应用开发｜一面｜面试 2026-08-06，发布 08-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/15af3788a038477bba99f2f9d94b2cef

真人 / 第一人称证据：作者明确记录面试日期并描述面试官根据项目细节不断追问，整场从 Agent / RAG 项目进入 Failure、Cost 和 Observability，具有自然真人面试流。

高价值问题：

1. 一个 Agent 系统真正需要哪些核心模块？
2. Tool Schema、错误码和调用失败应该如何设计？
3. Memory 有哪些类型，分别如何存储、过期和去重？
4. ReAct 与 Plan-Execute 怎样选，如何防止循环和任务不断下推？
5. Multi-Agent 怎样通信与同步 State？
6. RAG 的完整 Offline / Online 链路是什么？
7. Chunk Size / Overlap 应怎样通过实验确定？
8. Vector Recall 不准时，Hybrid Retrieval 与 Rerank 怎样继续优化？
9. RAG 与 Fine-tuning 的边界是什么？
10. 模型超时 / 异常、Latency、Cost 与 Observability 怎样治理？

---

## S110 快手｜Agent 开发｜日常实习一面｜发布 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ce1b038c57c44cc08464561a8cfa0434

真人 / 第一人称证据：作者 `等个消息橘子` 的主页只有极少个人求职内容，不是面经内容账号。本场面试官先连续验真候选人的 Agent 项目是否来自实习、是否真正上线、有没有真实用户和调用量；作者直接承认项目主要是个人 / 校园场景、没有生产业务流量。之后问题从 Memory / Context / ReAct 进入 Go、Redis 与后端系统设计，现场验真痕迹很强。

整场技术问题：

1. Agent 项目是不是实习项目，是否真正上线？
2. 有没有真实用户、真实调用量或生产业务数据，如何证明项目不是 Demo？
3. 为什么设计 Long-term Memory 与 Short-term Memory，两者各自解决什么问题？
4. 哪些信息应该进入长期记忆，哪些只保留在当前会话 / 短期状态？
5. Context Window 不够时，截断、摘要和 Retrieval 分别有什么代价，怎样选？
6. 当前 Agent 使用 ReAct 还是 Workflow，为什么这样设计？
7. Tool Call 失败、超时或返回异常时怎样处理？
8. Retrieval 返回互相矛盾的证据时，模型应该信谁，如何做冲突消解和 Verification？
9. Go Channel 是否线程安全，它与 Mutex 分别适合什么并发场景？
10. GMP 调度怎样理解；当前 P 的本地队列为空时如何继续获取任务？
11. Redis 为什么快，常见数据结构和典型场景有哪些？
12. System Design：实现类似淘宝搜索框的实时模糊联想 / 自动补全。
13. 二维码登录从生成二维码、扫码确认到 Web 端登录完成的完整链路是什么？
14. Service Registration / Discovery 如何工作，Nacos / Consul 的 Heartbeat 与实例失效怎样处理？
15. Coding / 并发题：有 100 个任务 ID，最多只允许 3 个任务同时调用外部 API，怎样实现并发控制？

去重：另发现 `bec7cc3ac12c464eaa2361f99040ed1a` 明确以招聘账号“转 @等个消息橘子：快手 Agent 开发一面”的方式复用本帖，只作为转载证据、零贡献。当前原帖的“生产验真 → Memory / Context → ReAct → Tool Failure → Go Channel / GMP → Redis → 模糊搜索 → 二维码登录 → 服务发现 → 限并发”题序未在历史快手来源出现。

---

## S111 百度｜Agent Harness｜秋招一面｜面试 2026-07-18，发布 2026-08-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/878ede5477714cce9d6276e75e04ce0b

真人 / 第一人称证据：候选人明确记录第一次秋招面试、面试官交流和次日收到失败结果；岗位直接为 Harness，本轮主要通过 MySQL / 大数据与 Coding 验证底层工程能力。

高价值问题：

1. MySQL `EXPLAIN` 中不同 Access Type 怎么区分？
2. 大表为什么需要分库分表，真实项目如何选择分片方式？
3. 大量历史数据查询怎样通过预聚合等方式优化？
4. Harness 岗为什么仍会重点考数据库 / 后端底座？
5. Coding：合并两个有序数组。

---

## S112 成都晓多科技｜Agent 开发｜社招二面 + HR / 产品面｜发布 2026-08-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/46fb9f8bb8434687921f5363fe1db94f

真人 / 第一人称证据：作者完整记录自己的 Golang 社招多轮流程，明确更新“已接 Offer”，并保留多个当场答不上 / 答偏的细节；岗位为 Agent 开发，技术二面从 Go / Infra 深挖到 Model Gateway、RAG 与数据库。

高价值问题：

1. Fiber 为什么快，所谓低 / 零内存分配背后的机制是什么？
2. ETCD 为什么用 RAFT，为什么项目选择 ETCD 而不是 Redis，Service Discovery 怎么做？
3. Asynq 的底层如何实现，怎样减少任务丢失，与 MQ 有什么区别？
4. 项目性能提升 300% 具体怎么做到，为什么使用 `sync.Map`？
5. Go Memory Escape / Leak 怎样理解，PPROF 怎样用于定位性能问题？
6. Model Aggregation Gateway 怎样抽象不同 Provider 的 Schema、Streaming 和 Chat 接口？
7. Model Call 失败、厂商 Rate Limit 和 Token Cost 怎样处理 / 统计？
8. RAG 定期同步全站数据如何用 Checksum 做增量更新，Chunk / Top-K / Rerank 怎么设计？
9. MySQL Clustered / Secondary Index、Redis Thread Model 等底层基础怎样解释？
10. Coding：O(1) 额外空间原地去重有序数组。

---

## S113 商汤 SenseTime｜AI 后端开发｜暑期二面 + 三面｜发布 2026-03-15｜HUMAN-A

来源：https://www.nowcoder.com/discuss/862704816219328512

真人 / 第一人称证据：作者以“再战暑期实习”形式连续记录自己的二面和三面，轮次清晰；二面深挖系统瓶颈、重试与 RAG，三面继续问职业规划、AI 认知和 AI Coding 实践。

高价值问题：

1. 如何定位一个系统的性能瓶颈并继续优化？
2. 为什么 Retry 要使用二级队列，具体怎么做？
3. RAG 整体链路怎样搭建？
4. Query Rewrite 怎样做？
5. Vector DB 怎样选型？
6. Coding：两个线程交替打印奇偶数。
7. 怎样看待 AI 方向的发展？
8. 平时怎样学习新技术？
9. AI Coding 在开发中怎样实践？

---

## S114 快手｜AI 应用服务端开发｜一面 + 二面 + 三面｜2026-08-26 / 09-01 / 09-09｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/1f6732ca32c74e17af502c71e77c8c59

二面来源：https://www.nowcoder.com/feed/main/detail/2892c62d66b24268959644260a7d7044

三面来源：https://www.nowcoder.com/feed/main/detail/ef8b41f126664ff2879337d43889a4ee

真人 / 第一人称证据：三篇均由候选人 `27备战秋招` 发布，个人主页是可连续核验的本人求职 Timeline，并明确记录快手 `AI应用服务端`：8 月 26 日一面、9 月 1 日二面、9 月 9 日三面。作者在二面保留“Coding 虽做出但过程不好、感觉面试官态度变化”“SDD 被继续挑战”等现场状态；三面又记录面试官交流体感、到岗时间和其它 Offer，属于连续真人招聘流程而非题单整理。

整场技术问题：

### 一面

1. CR Agent 项目的业务背景、完整链路和本人职责是什么？
2. Agent-to-Agent / A2A 与 MCP 分别解决什么问题，如何配合？
3. Java 常见 Design Pattern 在当前工程里怎样实际使用？
4. SDD / Spec-driven Development 怎样理解，怎样约束 AI Coding 或 Agent 开发？
5. Coding：现场算法实现与复杂度说明。
6. 日常写代码有多少使用 AI，形成了怎样的 AI-assisted Development 习惯？

### 二面

7. 继续深挖 CR Agent：真正的技术难点和业务价值是什么？
8. 微软实习中的 Backend 工作是什么，哪些能力能迁移到 Agent Service？
9. Coding：现场完成算法题；候选人自评最终写出，但过程不够顺畅。
10. SDD 在真实项目中具体怎样落地，为什么面试官会继续挑战方案细节？
11. 如何证明 Spec / Test / Review 确实约束了 AI 生成结果，而不是只加了一份文档？

### 三面

12. CR Agent 为什么需要 Distributed Architecture？
13. 多 Agent 之间怎样通信，Agent-to-Agent Message / State 应怎样组织？
14. 某个 Agent / Service 执行失败后，系统怎样保证整体 Stability 和恢复能力？
15. Redis Lua 如果封装了过多业务逻辑，会带来什么维护、演进和可测试性问题？
16. Coding：两道基础算法现场实现。
17. 反问 / 招聘：团队业务方向、候选人的业务兴趣、其它 Offer 和春节后实习到岗时间。

去重：已直接回读所有历史快手来源。本场独特的“CR Agent → A2A / MCP → Java Design Pattern → SDD → 二面微软 Backend + SDD 追问 → 三面 Distributed Agent / A2A Communication / Failure Stability / Lua 业务逻辑膨胀”的连续流程未在历史样本出现；三轮同作者同公司同岗位，主动合并。
