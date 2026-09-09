# Batch 06 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 本批继续执行固定准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 本轮继续用 `公司 × 岗位别名 × 月份 × 技术关键词` 扩大 Recall，重点回扫 2026 年 3–8 月历史缺口，同时加入 9 月 9 日当天新发布内容。AI 自动面试、面经合集、付费答案专栏、题库 / 标准答案、同账号批量模板化内容、岗位越界和无法稳定核验的帖子全部保持零贡献。
>
> 问题均为研究所需的简洁转述，不复制第三方正文；只记录原帖中能够确认真实问到的内容，不把合理推导写成面试问题。

---

## S095 阿里淘天｜AI 应用开发 / Agent｜一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a0306a045d594b02b63fb0654d517901

真人 / 第一人称证据：作者明确以本人一面复盘发布并写“发面经攒人品”，问题从自己的 RAG 项目连续追到 Multi-Agent State、MCP、FastAPI / SSE、Checkpoint 和向量检索。

高价值问题：

1. BM25 与向量检索怎样组合，Hybrid Retrieval 为什么能提升效果？
2. 扫描 PDF 的 OCR、表格结构化抽取有哪些难点，准确率如何衡量？
3. Multi-Agent 的 State 如何全局管理，怎样处理执行中的状态竞争？
4. 业务接口封装为 MCP Tool 时，标准化输入输出与兼容问题如何处理？
5. MCP 出现之前模型如何调用外部能力，MCP 本身有哪些挑战？
6. 子任务失败或数据为空时，Workflow 如何重试或降级？
7. FastAPI + SSE 如何把 LangGraph Node 的中间结果实时推给前端？
8. Checkpoint 如何持久化，断线重连后怎样恢复之前状态？
9. Vector DB、Index、RRF 与精排模型如何选？

---

## S096 钉钉｜后端 AI 研发｜暑期一面 1h｜发布 2026-04-13｜HUMAN-A

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

## S097 携程｜AI 后端｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0514bdd618cf43ae9be9240bc483cc9a

真人 / 第一人称证据：作者明确写“发点面经攒攒人品”，整场围绕自己的 AI Coding、分库分表、缓存和订单项目连续追问，并包含现场 Coding。

高价值问题：

1. AI Coding 生成的代码质量怎样判断，能否直接投入生产？
2. 分片键为什么选业务核心 ID 而不是用户 ID，何时需要分库分表？
3. 分片后“我的评论”等跨分片查询、分页和全局排序怎么做？
4. 评论 / 多级回复表结构如何设计以减少 I/O？
5. Sharding-JDBC 在真实分库分表系统中如何使用？
6. Bloom Filter 为什么用于当前业务，为什么不用空值缓存？
7. Distributed Lock 解锁时怎样保证原子性、避免误删？
8. MySQL Optimistic Lock 如何处理并发更新？
9. 扣库存与生成订单如何用 Transaction 保证一致性？
10. Coding：LRU Cache 或 Merge K Sorted Lists。

---

## S098 字节跳动｜后端 AI 开发｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f46e1419b49c4fe6832a1180b344af23

真人 / 第一人称证据：候选人明确写自己面后感觉很难、还需要练习；问题从项目一路追到 WebSocket、Redis、ThreadLocal、TCP、OpenClaw 和 Coding，回答状态清晰。

高价值问题：

1. WebSocket 推送订单状态时，弱网断连后怎样补齐状态？
2. 订单 ID 如何生成，随机方案有没有碰撞风险？
3. Redis 多级缓存具体是什么，Distributed Lock 如何帮助处理秒杀并发？
4. ThreadLocal 为什么能线程隔离，ThreadLocalMap 存在哪里？
5. ThreadLocal 为什么可能导致 Memory Leak？
6. TCP 四次挥手为什么这样设计，为什么存在 2MSL？
7. SYN Attack 是什么，怎样检测或缓解？
8. OpenClaw 的实现原理了解多少，部署时用了什么模型？
9. 通义千问、DeepSeek 等模型如何比较？
10. Coding：SQL + Zig-zag Tree Traversal。

---

## S099 字节跳动｜AI 后端开发｜暑期二面｜发布 2026-04-10｜HUMAN-A

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

## S100 字节跳动｜后端 AI 开发｜实习一面 1h｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ab0601f3dbad49ab87ea870a00bb3691

真人 / 第一人称证据：候选人明确记录一小时真人一面，问题以自己的 Agent 项目为主线，从系统目标追到 Planner / Executor / Supervisor、RAG 和 Java 并发。

高价值问题：

1. Agent 项目的核心功能和整体组件是什么？
2. Spring AI Alibaba 在项目里具体覆盖哪些能力？
3. Planner / Executor / Supervisor 架构的优势是什么？
4. 为什么拆成多个 Agent，而不是一个 Agent 完成？
5. RAG 的完整流程是什么，Retrieval / Rerank 怎么做？
6. 如果没有 Rerank 会怎样？
7. 回答质量差时，RAG 层和 Fine-tuning 分别能怎么优化？
8. MySQL 与 Redis 的职责差异是什么，Redis 能不能当主要存储？
9. 大量 Producer / Consumer 的并发场景在 Java 中如何设计？

---

## S101 字节跳动｜AI Agent｜实习二面｜发布 2026-03-22｜HUMAN-A

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

## S102 小红书｜Agent 后端开发｜日常实习二面｜发布 2026-04-03｜HUMAN-A

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

## S103 腾讯｜AI 后台开发｜日常实习一面｜发布 2026-04-27｜HUMAN-A

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

## S104 美团｜后端 AI 开发｜暑期一面｜发布 2026-04-27｜HUMAN-A

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

## S105 腾讯｜AI 后端开发｜二面 50min｜发布 2026-04-01｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f0e993c94c17476180e1a0185a6662f2

真人 / 第一人称证据：作者明确记录 50 分钟二面并写“攒人品中”，问题从本人项目 / 论文进入 Transformer、LLM / RAG / Agent、定时任务和并发系统设计。

高价值问题：

1. Transformer 的劣势是什么，Mamba 与 Transformer 各适合什么场景？
2. LLM、Prompt、RAG、Agent 的现有实现和优化方式有哪些？
3. Agent 有哪些真正适合的应用场景？
4. 怎样设计增加 / 删除任务都为 O(1) 的定时任务触发器？
5. Consistent Hashing 是什么，适合什么场景？
6. 如何保证系统并发安全？
7. 项目开发中最大的难点是什么？
8. 怎样快速学习 Go 等新语言并实际使用？

---

## S106 阿里淘天｜AI 应用开发｜一面｜面试 2026-04-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e6bd714a536b4723b67f97631b174f60

真人 / 第一人称证据：候选人明确记录本人 AI 应用一面，面试官介绍部门后围绕其 Agent 项目持续追问，最后安排多轮现场 AI Coding。

高价值问题：

1. RAG 在 Agent 项目中承担什么职责？
2. Harness Engineering 相比普通 Agent / ReAct 增加了什么？
3. Hermes 一类 Agent 的自我纠正 / 演化机制怎样理解？
4. LLM 内部知识与 Retrieval Evidence 冲突时应该怎么办？
5. MCP 在项目里的真实用途和限制是什么？
6. Sandbox 在 Agent 系统里解决什么风险？
7. 客服场景中的 ReAct 与 Workflow 怎样取舍？
8. Prompt Injection 怎样防？
9. Multi-Agent 怎样设计，什么时候不值得拆？
10. AI Coding：连续完成多轮限时需求实现。

---

## S107 阿里国际｜AI 应用研发｜一面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6d98fa8b5b8e4832a982c0c12a0fdc6d

真人 / 第一人称证据：作者明确以同岗本人一面分享并写“攒人品中”，问题从实习、Java / MQ / Redis 基础自然进入 RAG、Agent 和高流量系统设计。

高价值问题：

1. Java HashMap 在 JDK 8 中怎样实现？
2. JVM Memory Area 怎样理解？
3. AI Coding 生成代码时如何说明自己真正理解并验收过？
4. RabbitMQ 怎样提高消息可靠性？
5. Redis / ZSet 在项目里怎么用？
6. RAG 的整体流程是什么，检索效果差的原因有哪些？
7. Retrieval Poor 时可以从哪些层面优化？
8. 请求量暴增时系统可能出现哪些瓶颈？
9. 如果重新设计项目，会做哪些工程优化？
10. Coding：Merge Intervals。

---

## S108 深信服｜AI 全栈开发｜二面｜面试 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7fd4389e0a0844faa4dce49ba5e5c3f1

真人 / 第一人称证据：作者以“面试全部面试官问题汇总 / 发面经攒人品”记录本人 6 月 23 日二面；问题从后端缓存与锁一路深挖到开源 Agent 的 Token 统计、Sub-agent 调度和容错。

高价值问题：

1. 三层 Cache 为什么这样分层，多级缓存一致性怎样保证？
2. Redis / MySQL 重启后数据不一致时怎样兜底修复？
3. 缓存命中率如何测量，淘汰策略如何设计？
4. 通用注解锁怎样避免和业务逻辑耦合，重复上锁 / 释放怎么处理？
5. Main Agent 提前关闭、Sub-agent 延迟退出时 Token Usage 怎样补偿？
6. Tool / Sub-agent 的 Token 统计适合在哪些 Runtime Event 埋点？
7. 多个 Sub-agent 同时更新 Conversation Statistics 会不会存在竞争？
8. 主 / 子 Agent 的调度模式和通信机制是什么？
9. 第三方大模型如何适配不同思考模式？
10. 接入 RAG Tool 后 Token 统计会新增哪些问题？

---

## S109 OPPO｜后端开发（实际 Agent 方向）｜两轮技术面｜面试 2026-05-18｜HUMAN-A

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

## S110 字节跳动｜Agent 开发｜二面｜面试 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/675f834ce9fa4a29b2c413d87241e6bb

真人 / 第一人称证据：作者以本人 Agent 二面复盘发布并标注“攒人品”，问题围绕 Coding Agent、Skill、Memory、Prompt、Cost、GraphRAG 与训练基础连续展开。

高价值问题：

1. Coding Agent 的完整链路是什么？
2. Skill 如何分层、匹配和沉淀？
3. Long-term / Short-term Memory 怎样设计？
4. Memory 越积越多时如何处理？
5. 模型怎样决定什么时候检索 Memory？
6. Context Compression 在什么时候触发，Token Limit 怎样考虑？
7. Dynamic Prompt 与 Static Prompt 有什么区别？
8. 模型调用成本 / Token 怎样估算？
9. GraphRAG 与向量检索有什么差异，什么 Query 更适合图推理？
10. SFT / DPO / GRPO 等方法怎样理解？

---

## S111 懂车帝｜Agent 开发｜一面｜发布 2026-08-13｜HUMAN-A

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

## S112 字节跳动｜AI 应用开发｜一面｜面试 2026-08-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/15af3788a038477bba99f2f9d94b2cef

真人 / 第一人称证据：作者明确记录 8 月 6 日真人一面和面试体验；问题围绕自己的 Agent 学习、AI Coding、Tool / Memory / ReAct 设计连续展开。

高价值问题：

1. 为什么选择 AI Application / Agent 方向？
2. 最近怎样学习 Agent 前沿、使用 AI Coding？
3. 一个 Agent 的核心模块有哪些？
4. Tool 应怎样设计，能力抽象和 Schema 怎么定义？
5. Memory 有哪些类型，分别存什么？
6. Memory 存储、过期和去重怎样设计？
7. ReAct 与 Plan-Execute 怎样取舍？
8. Agent 怎样避免循环或任务反复传递？

---

## S113 快手｜Agent 开发｜日常实习一面｜发布 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ce1b038c57c44cc08464561a8cfa0434

真人 / 第一人称证据：作者明确记录自己本来以为重点问 Agent，实际一路被追到后端基础，并坦言练手项目没有真实业务流量、回答用户量和调用量时“有点虚”；现场真实性很强。

高价值问题：

1. Agent 项目是否真实上线，用户量和调用量是多少？
2. 为什么需要 Long-term / Short-term Memory，什么信息分别进入两层？
3. Context 不够时，截断、摘要压缩、Retrieval 怎样取舍？
4. 项目是 ReAct 还是 Workflow，为什么？
5. Tool 调用失败怎么处理？
6. Retrieval 结果互相矛盾时模型应该信谁？
7. Go Channel 与 Mutex、GMP Work Stealing 等并发基础怎样理解？
8. Redis 为什么快，怎样设计实时模糊搜索？
9. 扫码登录、Service Discovery、Nacos / Consul Heartbeat 怎样工作？
10. Coding：100 个任务限制最大并发为 3，模拟并发调用外部接口。

---

## S114 百度｜Agent Harness｜秋招一面｜面试 2026-07-18，发布 2026-08-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/878ede5477714cce9d6276e75e04ce0b

真人 / 第一人称证据：候选人明确记录第一次秋招面试、面试官交流和次日收到失败结果；岗位直接为 Harness，本轮主要通过 MySQL / 大数据与 Coding 验证底层工程能力。

高价值问题：

1. MySQL `EXPLAIN` 中不同 Access Type 怎么区分？
2. 大表为什么需要分库分表，真实项目如何选择分片方式？
3. 大量历史数据查询怎样通过预聚合等方式优化？
4. Harness 岗为什么仍会重点考数据库 / 后端底座？
5. Coding：合并两个有序数组。

---

## S115 成都晓多科技｜Agent 开发｜社招二面 + HR / 产品面｜发布 2026-08-23｜HUMAN-A

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

## S116 商汤 SenseTime｜AI 后端开发｜暑期二面 + 三面｜发布 2026-03-15｜HUMAN-A

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

## S117 快手｜AI 应用服务端｜秋招三面｜面试 2026-09-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ef8b41f126664ff2879337d43889a4ee

真人 / 第一人称证据：作者在 9 月 9 日当天面完后发布，明确写面试 30 多分钟、面试官体验和 Offer / 实习时间交流；技术问题围绕自己的 CR Agent 项目继续深挖。

高价值问题：

1. CR Agent 为什么要做分布式？
2. Agent 与 Agent 之间怎样通信？
3. 出现异常情况后怎样保障 Agent 系统稳定？
4. Redis Lua Script 如果包含过长的业务逻辑会发生什么？
5. 什么逻辑适合放进 Lua，什么逻辑不适合？
6. Coding：两道基础算法题，重点验证现场实现。

---

# 本轮明确排除

Batch 06 扩大搜索时，以下内容仍保持 **零贡献**：

- 去哪儿等公司的 AI 自动面试 / AI 面：没有真人面试官，直接不满足 HUMAN-A；
- “三年面试五年模拟”“面经合集”“含完整答案”“高频题解析”等专栏 / 二次整理；
- 同一账号短时间批量发布多家公司、结构和措辞高度模板化，无法可靠确认候选人本人经历的帖子；
- 与已有来源题序高度一致、只是替换公司 / 日期的疑似复制或再加工内容；
- 传统 Java / Go / 数据开发 / 算法岗位，只因最后顺带问一两个 Agent 问题的场次；
- AI 测试 / 测开、纯模型训练 / 算法、普通前后端等 Role Scope 外内容；
- 只有搜索摘要或聚合页、原正文无法稳定核验的线索。

# Batch 06 观察

本批新增 `S095–S117` 共 **23 个 HUMAN-A 来源**，当前干净核心样本达到 **117 个**。

这一轮出现了更稳定的信号：

1. **来源仍未饱和。** 在 S001–S094 后继续做月份 × 公司 × 岗位 × 技术词回扫，仍能找到 20+ 个独立 HUMAN-A，而且 9 月 9 日当天仍有新的目标岗位真人三面发布。
2. **AI Backend / Agent Backend 的基础工程权重很高。** Sharding、Transaction、Redis、Kafka、ThreadLocal、TCP / HTTPS、Go Runtime、Service Discovery 与 Agent / RAG 同场出现，不是传统后端样本混入造成的假频率。
3. **Agent Runtime 更强调可恢复执行。** State Competition、Checkpoint Resume、Disconnect Recovery、Tool Failure、Interrupt、Sub-agent Accounting、Race Condition、Distributed Agent Failure 都来自真人追问。
4. **RAG 继续从“会搭 Pipeline”转向“能解释选择并评估”。** OCR / Table、Hybrid Retrieval、Rerank、Vector DB、RRF、Dynamic Update、Retrieval Evaluation 反复出现。
5. **项目验真是核心能力。** 面试官持续追真实用户 / QPS、指标来源、代码能否生产、本人贡献和 Failure Case；练手 Demo 虚构数据非常容易被追穿。

停止条件不变：继续扩大 Recall，直到跨公司、岗位、月份、轮次和平台的多轮搜索都几乎不再产生新的、互不重复且可稳定核验的 HUMAN-A，并且新增来源的问题分布也开始稳定收敛；**不是达到某个 S 编号或 Batch 数就停止。**