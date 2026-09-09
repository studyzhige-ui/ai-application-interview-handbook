# Batch 06 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 本批继续执行固定准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 本轮继续用 `公司 × 岗位别名 × 月份 × 技术关键词` 扩大 Recall，重点回扫 2026 年 3–8 月历史缺口，同时加入 9 月 9 日当天新发布内容。搜索结果中的 AI 自动面试、面经合集、付费答案专栏、题库 / 标准答案、同账号批量模板化发布、岗位越界和无法稳定核验的内容均不进入正式来源，也不贡献任何 Canonical Question。
>
> 问题均为研究所需的简洁转述，不复制第三方正文。

---

## S095 阿里淘天｜AI 应用开发 / Agent｜一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a0306a045d594b02b63fb0654d517901

真人 / 第一人称证据：作者明确以本人一面复盘发布并写“发面经攒人品”，问题从自己的 RAG 项目连续追到 Multi-Agent State、MCP、FastAPI / SSE、Checkpoint 和向量检索，具有非常清晰的现场追问链。

高价值问题：

1. BM25 与向量检索怎样组合，Hybrid Retrieval 为什么能提升效果？
2. 扫描 PDF 的 OCR、表格结构化抽取有哪些工程难点，准确率如何验证？
3. Multi-Agent 的 State 如何全局管理，如何避免并发执行中的状态竞争？
4. 将业务接口封装为 MCP Tool 时，Schema、输入输出和兼容层如何设计？
5. MCP 出现之前，模型调用外部能力的完整链路是什么，MCP 又带来哪些新问题？
6. 子任务失败或数据为空时，Workflow 如何 Retry、Fallback 或 Degrade？
7. FastAPI + SSE 如何把 LangGraph 各 Node 的中间结果实时推送到前端？
8. Checkpoint 如何持久化，连接断开后怎样恢复之前的 Agent State？
9. Vector DB / Index / RRF / Rerank 如何选型并验证收益？

---

## S096 钉钉｜后端 AI 研发｜暑期一面 1h｜发布 2026-04-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/27171d436e7b4ee0a0c5ef3414c18d8b

真人 / 第一人称证据：候选人以本人暑期一面形式记录约 1 小时连续项目深挖，问题围绕自己做过的 OCR / 文档理解 / RAG 工程逐层展开，并保留明显的真实面试顺序而非题库分类。

高价值问题：

1. 文件解析为什么使用 OCR，而不是只依赖 PDF / DOCX 结构化 API？
2. OCR 如何同时处理文本、图表和语义结构，识别质量用什么指标衡量？
3. Embedding 为什么选择当前维度，维度变化会带来什么效果和资源权衡？
4. Embedding Model 的 Tokenization、Backbone 与向量生成过程如何解释？
5. LLM 参数规模和显存 / 推理资源之间是什么关系？
6. ES / BM25 与 Milvus 向量召回如何做 Hybrid Retrieval？
7. Rerank 的核心原理是什么，应该用什么指标证明重排真的有效？
8. Function Calling、MCP 与 Skill 的职责和适用场景如何区分？

---

## S097 携程｜AI 后端｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0514bdd618cf43ae9be9240bc483cc9a

真人 / 第一人称证据：作者明确写“发点面经攒攒人品”，整场围绕自己的 AI Coding、分库分表、缓存和订单项目连续追问，并包含现场 Coding。

高价值问题：

1. AI Coding 生成的代码达到什么条件才能进入生产？
2. 分片键为什么选择业务核心 ID 而不是用户 ID，触发分库分表的阈值是什么？
3. 分片后“我的评论”等跨分片查询、全局排序和分页如何实现？
4. 评论 / 多级回复表结构如何设计，怎样减少查询 I/O？
5. Sharding-JDBC 在真实分库分表系统中承担什么职责？
6. Bloom Filter、Null Cache 与 Distributed Lock 分别解决哪些缓存 / 并发问题？
7. Distributed Lock 解锁时如何保证原子性并避免误删其他请求的锁？
8. MySQL Optimistic Lock 如何处理并发更新？
9. 扣库存与生成订单如何通过 Transaction 保证一致性？
10. Coding：LRU Cache 或 Merge K Sorted Lists。

---

## S098 字节跳动｜后端 AI 开发｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f46e1419b49c4fe6832a1180b344af23

真人 / 第一人称证据：候选人明确写自己面后感觉很难、还需要多练习；问题从项目现场一路追到 WebSocket、Redis、ThreadLocal、TCP、OpenClaw 和 Coding，真实回答状态明显。

高价值问题：

1. WebSocket 推送订单状态时，弱网断连后如何发现缺失事件并补偿？
2. 订单 ID 如何生成，随机方案如何分析碰撞风险？
3. Redis 多级缓存具体缓存什么，秒杀零超卖为什么还需要 Distributed Lock？
4. ThreadLocal 为什么能做到线程隔离，ThreadLocalMap 存在哪里？
5. ThreadLocal 为什么可能产生 Memory Leak，生产代码如何规避？
6. TCP 四次挥手为什么需要分阶段，TIME_WAIT 为什么常用 2MSL？
7. SYN Flood 如何检测与缓解？
8. OpenClaw 的实现机制和模型 Backend 如何理解？
9. 不同 LLM 的能力 / 参数如何比较并用于应用侧选型？
10. Coding：SQL + Zig-zag Tree Traversal。

---

## S099 字节跳动｜AI 后端开发｜暑期二面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a7169bcbc4554deba204cac4349c6a43

真人 / 第一人称证据：作者以本人二面记录发布并写“发点面经攒人品”；面试官连续要求其证明 QPS 指标、调试现场代码、解释实现优缺点，真人互动非常明显。

高价值问题：

1. 项目模拟的数据规模和 QPS 如何确定？
2. 简历中的“高峰 QPS 提升 4 倍”是怎样测出来的，Benchmark 是否可信？
3. 针对目标用户规模，具体做过哪些性能优化？
4. 工程实现过程中遇到的真实失败和瓶颈是什么？
5. Coding：用给定数字集合构造小于目标 N 的最大数，并补齐边界 Test Case。
6. 测试失败时如何打印和定位错误，并现场修改代码？
7. 如何评价自己刚写代码的复杂度、优点和缺陷？
8. HTTPS 从 DNS / TCP / TLS 到 HTTP 的完整请求链路是什么？
9. 高流量分布式请求如何做 Load Balancing，DNS 与 Nginx 各有什么边界？

---

## S100 字节跳动｜后端 AI 开发｜实习一面 1h｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ab0601f3dbad49ab87ea870a00bb3691

真人 / 第一人称证据：候选人明确记录一小时真人一面，问题以自己的 Agent 项目为主线，从系统目标一直追到 Planner / Executor / Supervisor、RAG 和 Java 并发。

高价值问题：

1. Agent 项目的核心业务目标和系统组成是什么？
2. Spring AI Alibaba 在项目中真正承担了哪些能力？
3. Planner / Executor / Supervisor 架构为什么比一个大 Agent 更合适？
4. 为什么拆成三个 Agent，Single-Agent 会出现什么问题？
5. RAG 的完整链路是什么，Retrieval 与 Rerank 各有哪些实现方式？
6. 如果不做 Rerank，最终生成质量会怎样变化？
7. 回答质量差时，应优先优化 RAG、Prompt 还是 Fine-tuning？
8. MySQL 与 Redis 在应用中的职责如何划分，Redis 能否承担主存储？
9. 大量 Producer / Consumer 并发任务在 Java 中怎样设计线程模型？

---

## S101 字节跳动｜AI Agent｜实习二面｜发布 2026-03-22｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/d31969d954a94f1cb1bb06abc3196fe9

真人 / 第一人称证据：作者以本人二面复盘发布并写“攒攒人品”，问题从自己的多模态 / Agent 项目继续追到 Memory、Multi-Agent、SSE、RAG Evaluation 和 MCP。

高价值问题：

1. 多模态 LLM 在应用系统中如何接入并组织输入？
2. Agent Skill 应如何设计和使用？
3. Agent Memory 不够可靠时从哪些层面增强？
4. Multi-Agent 如何在不同执行策略之间选择和切换？
5. SSE 在长连接 / Streaming 场景有哪些限制？
6. RAG Knowledge Base 动态更新时如何保证新旧索引一致？
7. Complex Task 的 Agent Accuracy / Success Rate 如何定义和评估？
8. 多轮对话如何治理 Context 与历史信息？
9. RAG Evaluation 应分别评 Retrieval 和 Generation 哪些指标？
10. MCP 与 Function Calling 的核心区别是什么？

---

## S102 小红书｜Agent 后端开发｜日常实习二面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/be9b14f9b1cf4fe09111b856c4f89608

真人 / 第一人称证据：作者明确以本人二面分享并写“攒人品”，问题虽数量不多，但持续围绕实习项目中的 Prompt、Agent、RAG、多模态与 OpenClaw 深挖，并有现场 Coding。

高价值问题：

1. 真实项目中的 Prompt Engineering 应如何分层和组织？
2. 常见 Agent Execution Paradigm 有哪些，各自适用什么场景？
3. RAG 效果差时可以从哪些环节优化？
4. 多模态对齐从视觉 / 文本表示到 LLM 输入大致如何完成？
5. 如何评价 OpenClaw 一类 Agent 产品的架构和工程取舍？
6. Coding：分批淘汰类算法问题。

---

## S103 腾讯｜AI 后台开发｜日常实习一面｜发布 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/793e6ceb32c74c2ea1137106f661ae2e

真人 / 第一人称证据：候选人明确以同岗本人一面分享并邀请同岗交流；问题从自己的 Kafka / Redis / TDengine 项目进入 Coding、Agent 基础和安全设计，顺序自然且信息密度高。

高价值问题：

1. Kafka 怎样从 Producer、Broker、Consumer 各层降低消息丢失风险？
2. 一个线程删除 Redis Key、另一个线程同时向该 Key 写数据时如何保证正确性？
3. TDengine 为什么适合时序数据，底层存储结构如何理解？
4. 如何快速定位运行中代码问题，日志 / Debug / Trace 的排查顺序是什么？
5. Coding：实现支持 Resize 的 HashMap，包括 Put / Get / Remove。
6. LLM、RAG、Agent、Skill 的职责边界分别是什么？
7. 一个高质量 Prompt 应怎样设计？
8. 登录系统如何同时保证通信安全和数据安全？
9. 为什么单纯 MD5 不足以保护密码，应该怎样改进？

---

## S104 美团｜后端 AI 开发｜暑期一面｜发布 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4a18e41893f1491fae094650eda78d6d

真人 / 第一人称证据：作者以本人同岗一面分享，问题从 RAG 项目一路追到 Tool Failure、Agent Interrupt、隐私、AI Coding 大仓库和模型基础，属于完整 AI Backend 技术面。

高价值问题：

1. RAG 从文档处理、Embedding、Vector DB 到 Retrieval / Generation 如何构建？
2. Metadata Filter、Hybrid Retrieval、Rerank 分别解决什么问题？
3. Retrieval Recall 和最终回答质量怎样建立可量化 Evaluation？
4. Tool 调用失败、乱序或长期卡住时 Runtime 如何恢复？
5. Agent 如何支持用户主动 Interrupt / Cancel，并阻止后续副作用继续发生？
6. 大量用户并发使用 Agent 时，服务端最容易出现哪些瓶颈？
7. 十万级文档知识库如何处理权限、隐私和 Hallucination？
8. AI Coding 面对超大 Repo、Context 不够时如何选择相关代码？
9. Transformer 在应用工程面试中需要理解到哪些关键机制？
10. Skill、Tool、MCP、OpenClaw 等能力如何区分？

---

## S105 腾讯｜AI 后端开发｜二面 50min｜发布 2026-04-01｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f0e993c94c17476180e1a0185a6662f2

真人 / 第一人称证据：作者明确记录 50 分钟二面并写“攒人品中”，问题从本人项目 / 论文进入 Transformer、LLM / RAG / Agent、定时任务和并发系统设计。

高价值问题：

1. Transformer 的主要局限是什么，Mamba 与 Transformer 分别适合什么场景？
2. LLM、Prompt、RAG、Agent 在真实系统中分别有哪些实现与优化点？
3. 什么业务场景真正适合 Agent，而不是普通 Workflow？
4. 如何设计新增和删除都为 O(1) 的 Timer / Scheduled Task Trigger？
5. Consistent Hashing 的原理和应用场景是什么？
6. 高并发服务如何保证共享状态正确？
7. 工程项目中真正最难的问题是什么，如何定位并解决？
8. 如何快速学习 Go 等新语言并达到工程可用程度？

---

## S106 阿里淘天｜AI 应用开发｜一面｜面试 2026-04-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e6bd714a536b4723b67f97631b174f60

真人 / 第一人称证据：候选人明确记录本人 AI 应用一面，面试官先介绍部门再围绕其 Agent 项目持续追问，最后安排多轮现场 AI Coding，具有明显真人交互过程。

高价值问题：

1. RAG 在 Agent 项目中负责什么，为什么不能只依赖模型内部知识？
2. Harness Engineering 相比 ReAct + MCP 多了哪些稳定性与安全能力？
3. Hermes 一类 Agent 的 Self-correction / Self-evolution 如何理解？
4. 模型已有知识与 Retrieval Evidence 冲突时，系统应如何决策？
5. MCP 在项目中的真实用途、代价和 Context 开销是什么？
6. Sandbox 应隔离哪些文件、命令、网络和 Secret 风险？
7. 客服类任务为什么可能更适合 ReAct，也可能更适合确定性 Workflow？
8. Prompt Injection 应如何从 Runtime / Permission / Data Boundary 层防护？
9. Multi-Agent 是否必要，应怎样证明拆分带来真实收益？
10. AI Coding：连续完成多轮限时需求实现与验证。

---

## S107 阿里国际｜AI 应用研发｜一面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6d98fa8b5b8e4832a982c0c12a0fdc6d

真人 / 第一人称证据：作者明确以同岗本人一面分享并写“攒人品中”，问题从实习、Java / MQ / Redis 基础自然进入 RAG、Agent 和高流量系统设计。

高价值问题：

1. Java HashMap 在 JDK 8 的结构和扩容机制是什么？
2. JVM Memory Area 与对象生命周期如何理解？
3. AI Coding 生成代码时怎样证明关键逻辑确实由本人理解和验收？
4. RabbitMQ 如何保证消息尽可能不丢，并处理重复投递？
5. Redis / ZSet 在项目中分别承担什么职责？
6. RAG 的完整执行链路是什么，Retrieval Poor 的常见原因有哪些？
7. 如果 Retrieval 效果差，应从 Chunk、Embedding、Query、Recall、Rerank 哪些层优化？
8. 请求量突然暴增时，AI Service 最可能出现哪些瓶颈？
9. 如果重新设计现有服务，会如何从 Cache、Async、Concurrency、DB 和 Model Call 层优化？
10. Coding：Merge Intervals。

---

## S108 深信服｜AI 全栈开发｜二面｜面试 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7fd4389e0a0844faa4dce49ba5e5c3f1

真人 / 第一人称证据：作者以“面试全部面试官问题汇总 / 发面经攒人品”记录本人 6 月 23 日二面；问题从后端缓存与锁一路深挖到开源 Agent 的 Token Accounting、Sub-agent 调度和容错。

高价值问题：

1. 三层 Cache 为什么这样分层，多级缓存一致性和淘汰如何设计？
2. Redis / MySQL 在宕机重启后不一致时如何做 Repair / Reconciliation？
3. 缓存命中率这类指标如何测量并证明设计有效？
4. 通用注解锁如何避免和业务逻辑过度耦合，重复加锁 / 释放怎样检测？
5. User Disconnect 或 Main Agent 提前退出后，Sub-agent 延迟结束造成的 Token 统计如何补偿？
6. Tool / Sub-agent 的 Token Usage 应在哪些 Runtime Event 做埋点？
7. 多个 Sub-agent 同时更新 Conversation Statistics 时怎样避免 Race Condition？
8. 主 / 子 Agent 的调度模式和通信机制如何设计？
9. 接入第三方 Model Backend 时如何适配不同 Reasoning / Response Format？
10. 如果再接 RAG Tool，Token Accounting 和 Context Accounting 会增加哪些复杂度？

---

## S109 OPPO｜后端开发（实际 Agent 方向）｜两轮技术面｜面试 2026-05-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/09fd6466f3f64e7dbfb5a09ed9d660a4

真人 / 第一人称证据：作者明确写自己最终 OC，并特别说明“与其说后端，更像 Agent 开发，基本只问 AI 相关”；两轮均为真人面试，第二轮继续围绕 Agent 技术和项目取舍追问，符合 Role Scope 的“实际职责 / 面试内容优先”。

高价值问题：

1. Context Window 超限时有哪些治理方式，各自损失什么信息？
2. 长论文 + 算法说明 + Knowledge Retrieval 同时塞入 Context 时如何做 Task Decomposition？
3. MCP 与 Skill 的核心区别是什么？
4. 如何设计一个 Skill，使 Agent 稳定遵循特定角色、行为与任务约束？
5. Multi-Agent 协作采用 Leader / Worker 还是 Flat Peer 模式，应怎样选择？
6. Agent 之间怎样传递 Task State 与 Context，避免信息污染？
7. AI Project 中哪些能力属于 Runtime，哪些属于 Prompt / Model？
8. 两轮都以 Agent 项目为核心时，如何证明本人不是只会调用现成框架？

---

## S110 字节跳动｜Agent 开发｜二面｜面试 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/675f834ce9fa4a29b2c413d87241e6bb

真人 / 第一人称证据：作者以本人 Agent 二面复盘发布并标注“攒人品”，问题围绕 Coding Agent、Skill、Memory、Prompt、Cost、GraphRAG 与对齐方法连续展开。

高价值问题：

1. Coding Agent 从用户任务到最终 Patch 的完整执行链路是什么？
2. Skill 如何分层、匹配、加载并从执行经验中沉淀？
3. Short-term / Long-term Memory 如何区分，哪些 Memory 可以动态更新？
4. Long-term Memory 越积越多时如何做 Retrieval、淘汰和污染治理？
5. Context Compression 应在什么条件触发，如何根据 Token Budget 决定？
6. Dynamic Prompt 与 Static Prompt 分别适合保存什么？
7. Model / Token Cost 如何估算并纳入 Agent Runtime 约束？
8. GraphRAG 相比 Vector Retrieval 更适合哪些关系型问题？
9. 如何用具体 Query 证明 Graph Reasoning 的价值？
10. SFT / DPO / GRPO 在应用工程师视角分别需要理解什么？

---

## S111 懂车帝｜Agent 开发｜一面｜发布 2026-08-13｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/8d84590d7efe4c78943b28708b4395f2

真人 / 第一人称证据：作者明确记录自己已经挂掉，并疑惑“既然不匹配为什么还面了一个小时”；问题高度场景化地围绕生产 Agent 的 Trace、日志、Multi-Agent 切分和 Regression 展开，现场感很强。

高价值问题：

1. 用户描述模糊时，Agent 如何通过 Clarification / Intent Refinement 提高定位准确率？
2. Leader Agent 如何判断故障位于哪条调用链和哪个模块？
3. Trace ID、Structured Log 与 Execution Trace 应如何组合做 Agent Observability？
4. 不同业务 Case 走不同链路 / 配置时，如何快速识别当前实际执行路径？
5. 错误日志级别或误导性日志导致模型判断错误时怎么治理？
6. Multi-Agent 应按任务阶段、领域还是能力做 Granularity 切分？
7. 不同业务线不断增加 Agent 导致 Agent Explosion 时如何治理？
8. 底层模块改动后怎样保证所有 Agent 的 Regression 不被破坏？
9. Agent 自动修改代码后如何验证修复确实正确？
10. Coding：LRU Cache。

---

## S112 字节跳动｜AI 应用开发｜一面｜面试 2026-08-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/15af3788a038477bba99f2f9d94b2cef

真人 / 第一人称证据：作者明确记录 8 月 6 日真人一面和对面试官体验的评价；问题围绕自己的 Agent 学习、AI Coding、Tool / Memory / ReAct 设计连续展开。

高价值问题：

1. 为什么选择 AI Application / Agent 方向，学习路线如何建立？
2. 平时如何跟踪 Agent 前沿并实际使用 AI Coding？
3. 一个 Agent 的核心模块应该怎样拆？
4. Tool 应如何抽象能力，Schema、Error Code 和权限边界怎样定义？
5. Short-term / Long-term / Episodic 等 Memory 如何分类？
6. Memory 应存在哪里，怎样设置 Expiry、Dedup 和 Update Policy？
7. ReAct 与 Plan-Execute 分别适合什么任务？
8. Agent 如何避免无限 Loop、任务反复转交或提前宣称完成？

---

## S113 快手｜Agent 开发｜一面｜发布 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ce1b038c57c44cc08464561a8cfa0434

真人 / 第一人称证据：作者以本人的日常实习面试记录发布，明确写自己原本预期重点问 Agent，但实际还被追项目真实性、用户 / QPS 和后端基础，并坦言某些数据是练手项目无法真实回答，现场痕迹非常强。

高价值问题：

1. Agent 项目是否真实部署、有多少用户 / 调用量，如何诚实说明 Demo 与 Production 的差异？
2. Long-term / Short-term Memory 如何实现？
3. Context 超窗后，Truncation、Summary 与 Retrieval-based Memory 各有什么优缺点？
4. ReAct 与固定 Workflow 的边界是什么？
5. Tool 调用失败时，Agent 应怎样 Retry、Fallback、Clarify 或停止？
6. 如果项目没有真实 QPS，怎样设计可信的 Load Test 而不是虚构数字？
7. AI Application / Agent 岗为什么仍然会用后端并发、缓存和系统设计验证工程能力？
8. 面试中如何证明项目的本人贡献与真实性？

---

## S114 百度｜Agent Harness｜秋招一面｜面试 2026-07-18，发布 08-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/878ede5477714cce9d6276e75e04ce0b

真人 / 第一人称证据：候选人明确记录自己第一次秋招面试、面试官风格以及次日收到失败结果；岗位直接为 Harness，面试却重点用 MySQL / 大数据与 Coding 验证底层工程能力。

高价值问题：

1. MySQL `EXPLAIN` 中不同 Access Type 代表什么，怎样判断查询计划是否合理？
2. 大表为什么需要分库分表，真实项目如何确定 Sharding 策略和时机？
3. 大规模历史数据查询如何通过预聚合 / 汇总表降低在线查询成本？
4. Harness 岗为什么仍会重点检查数据库与后端基础，而不是只问 Agent 名词？
5. Coding：合并两个有序数组并分析复杂度与边界条件。

---

## S115 成都晓多科技｜Agent 开发｜社招二面 + HR / 产品面｜发布 2026-08-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/46fb9f8bb8434687921f5363fe1db94f

真人 / 第一人称证据：作者完整记录自己的 Golang 社招多轮流程、面试官交流和最终接受 Offer 的时间线；岗位明确为 Agent 开发，技术二面重点验证 Agent Backend 所需的 Go / Infra / Production 基础。

高价值问题：

1. Go Service 在 Agent Backend 中如何做 Context Cancellation 与优雅退出？
2. ETCD 的 Lease / Watch / Service Discovery 机制如何用于分布式服务？
3. Fiber 等 Go Web Framework 的并发模型和工程边界是什么？
4. Asynq / Redis Queue 一类异步任务系统如何处理 Retry、Delay 和 Failure？
5. Go PPROF 如何定位 CPU、Memory、Goroutine 等线上性能问题？
6. Kubernetes 中 Pod / Deployment / Service 如何支撑 Agent Service 部署？
7. 长任务 Agent Backend 如何做任务状态、异步执行和故障恢复？
8. Agent 产品团队为什么仍需要扎实的 Go Runtime / Cloud Native 基础？

---

## S116 商汤 SenseTime｜AI 后端开发｜暑期二面 + 三面｜发布 2026-03-15｜HUMAN-A

来源：https://www.nowcoder.com/discuss/862704816219328512

真人 / 第一人称证据：作者以“再战暑期实习”形式连续记录自己的二面与三面，问题围绕系统瓶颈、重试队列、RAG、并发 Coding 和 AI Coding 习惯展开，轮次清晰且有现场感。

高价值问题：

1. 如何判断一个 AI Backend 系统当前瓶颈在 CPU、I/O、DB、Network 还是 Model Call？
2. 找到瓶颈后应如何按收益和风险排序优化？
3. 失败任务如何通过二级 / Retry Queue 做异步补偿？
4. RAG 从 Query 到 Retrieval、Rerank、Generation 的完整链路是什么？
5. Query Rewrite 什么时候有帮助，什么时候会改变用户原意？
6. Vector DB / Retrieval 方案选型应看哪些指标？
7. Coding：两个线程交替输出奇偶数，怎样保证同步正确？
8. 日常如何使用 AI Coding，同时保证自己理解和验证生成代码？
9. 如何理解 AI 应用工程方向未来的技术重点？

---

## S117 快手｜AI 应用服务端｜秋招三面｜面试 2026-09-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ef8b41f126664ff2879337d43889a4ee

真人 / 第一人称证据：作者在 9 月 9 日当天面完后立即发布，明确写面试约 30 多分钟、面试官交流感受、Offer / 实习时间讨论，并围绕自己的 CR Agent 项目继续追问，属于最新真人样本。

高价值问题：

1. CR / Code Review Agent 为什么需要分布式设计，单机方案的瓶颈在哪里？
2. 多个 Agent 之间如何通信和传递任务状态？
3. Agent 节点或服务出现异常后如何保证整体任务稳定性？
4. 分布式 Agent 需要怎样做 Retry、Failure Isolation 和 Recovery？
5. Redis Lua Script 如果包裹过长、过重的业务逻辑，会对单线程执行和延迟造成什么影响？
6. 如何判断某段逻辑应该放在 Lua 中保证原子性，还是拆回应用层？
7. Coding：两道基础算法题，重点考察现场实现正确性。

---

# 本轮明确排除

Batch 06 继续扩大搜索，但以下内容即使题目数量很多，也保持 **零贡献**：

- 去哪儿等公司的 AI 自动面试 / AI 面：没有真人面试官，直接不满足 HUMAN-A；
- “三年面试五年模拟”“面经合集”“含完整答案”“高频题解析”等专栏 / 二次整理；
- 同一账号短时间批量发布多家公司、结构和措辞高度模板化，无法可靠确认候选人本人经历的帖子；
- 与已有来源题序高度一致、只是替换公司 / 日期的疑似复制或再加工内容；
- 传统 Java / Go / 数据开发 / 算法岗位，只因最后顺带问一两个 Agent 问题的场次；
- AI 测试 / 测开、纯模型训练 / 算法、普通前后端等 Role Scope 外内容；
- 只有搜索摘要或聚合页、原正文无法稳定核验的线索。

# Batch 06 观察

本批新增 `S095–S117` 共 **23 个 HUMAN-A 来源**，当前干净核心样本达到 **117 个**。

这一轮有几个更稳定的信号：

1. **来源还没有饱和。** 在 S001–S094 之后继续做月份 × 公司 × 岗位 × 技术词回扫，仍能一次找到 20+ 个互不重复的 HUMAN-A，而且 9 月 9 日当天仍有新的目标岗位真人三面发布。
2. **AI Backend / Agent Backend 的基础工程权重非常高。** Sharding、Transaction、Redis Lock / Lua、Kafka、ThreadLocal、TCP / HTTPS、Load Balancing、Go Runtime、Kubernetes 与 Agent / RAG 同场出现，不是传统后端样本混入造成的假频率。
3. **Agent Runtime 更强调可恢复执行。** State Competition、Checkpoint Resume、Disconnect Recovery、Tool Failure、Cancel / Interrupt、Sub-agent Accounting、Race Condition、Distributed Agent Failure 都来自真人追问。
4. **RAG 继续从“会搭 Pipeline”转向“能做实验和验证”。** OCR / Table、Hybrid Retrieval、Rerank、Vector DB、RRF、Dynamic Update、Retrieval Evaluation 反复被要求解释选择依据和指标。
5. **项目验真已成为核心能力。** 面试官持续追“真实用户 / QPS 怎么来的、指标怎么测、代码是否能生产、本人究竟做了什么、失败怎么恢复”，练手 Demo 虚构数据很容易被追穿。

停止条件不变：继续扩大 Recall，直到跨公司、岗位、月份、轮次和平台的多轮搜索都几乎不再产生新的、互不重复且可稳定核验的 HUMAN-A，并且新增来源的问题分布也开始稳定收敛；**不是达到某个 S 编号或 Batch 数就停止。**