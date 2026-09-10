# Batch 01 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **13** 个正式来源。

---

## S001 阿里云｜Agent 开发｜一面｜2026-08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/42ba29ab006d4bb793112eb263d18f6a

真人 / 第一人称证据：作者明确记录自己被再次捞起后参加 Agent 开发面试，描述面试结果，并记录现场 AI Coding。

高价值问题：

1. 平时如何使用 AI 辅助编码，是否形成稳定工作流？
2. 常用 Skill 有哪些，不同 Skill 的结构和职责有什么差异？
3. 是否自己写过 Skill，设计 Skill 时最需要约束什么？
4. 对近期 Agent 产品的理解到什么程度？
5. Claude Code 与其他 Harness 产品在系统设计上有什么区别？
6. 是否真正读过成熟 Agent / Harness 源码？
7. 一个可靠 Harness 至少需要哪些核心能力？
8. Agent Tool Calling 有哪些实现方式？
9. 如何保证大量 Tool 按需发现、按需调用，而不是全部塞入 Context？
10. 为什么需要 Sub-agent，什么任务才值得拆成 Agent？
11. Agent 间通信如何组织？
12. 从零设计 Agent Loop 时需要考虑哪些 Runtime 问题？

---

## S002 字节跳动 TikTok｜AI Agent 开发｜秋招一面｜2026-08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7b1b40fda3244715a82bcb4a821ca887

真人 / 第一人称证据：候选人明确记录面试日期、现场互动感受和后续等待状态。

高价值问题：

1. 会议转写从音视频输入到文本、摘要的完整工程链路是什么？
2. ASR 服务为什么这样选，识别准确率如何评估与优化？
3. 实时音视频中的用户隐私数据如何保护？
4. 系统为什么采用中心化或去中心化架构？
5. RAG Chunk Size / Chunk Strategy 如何根据数据和评测确定？
6. Tokenization 为什么会把一个词拆成多个 Token？为什么 LLM 使用 Token 而不是字符 / 单词？
7. Transformer / QKV / Attention 的核心过程如何解释到应用工程需要的深度？
8. Lost in the Middle 为什么发生，长 Context 为什么不是越大越好？
9. Context Window 的能力边界由什么决定？
10. SFT / PPO / DPO / GRPO 等方法分别解决什么问题，应用工程师需要理解到什么程度？
11. 为什么选 Multi-Agent，为什么还需要中心化编排？
12. 数据结构 Coding：List → Tree、Zig-zag Tree Traversal。

---

## S003 影石创新｜AI Agent｜一面｜2026-08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b406c87436a54864bfc0cf4a20299f62

真人 / 第一人称证据：作者明确写出面试日期、次日得知失败，并逐题记录现场问题。

高价值问题：

1. Spec Coding 与 Harness 如何理解，Harness 为什么能提升复杂任务完成能力？
2. 从零设计 Agent 系统需要哪些模块？
3. Tool / API 超时、异常应该由 Runtime 如何分类、重试、降级？
4. 是否应该让 LLM 参与错误分析和自动恢复？模型与确定性 Runtime 的边界在哪里？
5. 短期 / 长期 Memory 如何设计？
6. Context 为什么需要压缩，压缩后的信息损失如何检测与恢复？
7. Prompt 优化除了增加规则约束还能做什么？
8. Agent 幻觉与 Token 消耗异常如何定位？
9. 一个 Skill 从设计、上线到效果验证的生命周期是什么？
10. Java 线程池如何运行，如果重新设计线程池会考虑哪些约束？
11. MySQL undo / redo / binlog 分别做什么？
12. redo log 与 binlog 的两阶段提交为什么需要存在？

---

## S004 小红书｜大模型平台 Agentic 全栈研发｜一面｜2026-08-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e5e9311a623940eead6ec98c65e7f9e8

真人 / 第一人称证据：候选人明确记录面试日期、结果、面试官引导与反问讨论，并指出自己没有答好的具体问题。

高价值问题：

1. Agent 在真实研发业务里到底解决什么问题，为什么不是普通客服 / Workflow？
2. Agent 的写操作边界如何划分？
3. Harness 层包含哪些职责？
4. 编排层如何重构，节点 / 边 / 状态如何组织？
5. 意图分流如何保证清晰，怎么识别 Query 是模糊还是明确？
6. Skill 和 Tool 的职责区别是什么？Skill 何时 Fetch / Load？
7. 不同基础模型表现不一致时，应用层如何做适配与稳定性治理？
8. 5000～6000 用户、十几万日请求量下 Agent 服务如何扩容？
9. 为什么选择 SQLite 或其他存储，什么时候需要迁移到更完整的数据层？
10. 为什么自研 Agent Runtime，而不是直接使用 LangGraph 等框架？
11. HashMap、MySQL B+Tree、联合索引等基础如何解释？
12. RAG / Vector Knowledge Base 在真实业务里如何做技术选型？

---

## S005 字节跳动｜AI 应用开发｜一面 + 二面（同一候选人同流程合并）｜2026-05-12 / 05-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/61aa7e8d56ca4eb4a5a873512a72d616

真人 / 第一人称证据：作者给出完整时间线：5 月 7 日 HR 联系、5 月 12 日一面后约 20–30 分钟约二面、5 月 15 日二面后挂并被其它部门捞。二面记录面试官迟到、Coding 中途离开、自己多处回答未戳中技术价值、现场代码出现 Bug 且和面试官一起排查未果，现场痕迹非常强。

高价值问题：

1. 实习中的 Database Optimization 具体怎么做，数据量级和是否 Sharding？
2. MySQL Index 为什么快、什么时候失效、用了索引为什么仍可能很慢？
3. Slow Query 如何定位和解决，B+Tree 为什么适合数据库索引？
4. Redis 的 Sentinel、Cluster、Master-Replica 怎样提供高可用 / 高性能？
5. Redis 与 MySQL 混合使用时怎样考虑数据一致性？
6. Vibe Coding、Skill 和其它 AI Coding 范式怎样理解？
7. Coding：按头尾交替规则重排单链表，并满足 `O(n)` / `O(1)`。
8. 二面项目验真：业务流程、本人负责部分、上下游问题和真实技术价值分别是什么？
9. 简历写“数据库优化提升 20%”时，具体怎样测；为什么真的提升？
10. Back-to-table Query 为什么涉及 Sequential IO / Random IO，当前场景怎样优化？
11. Coding：实现有最大容量的 Blocking Queue；现场出现 Bug 时如何 Debug？
12. 平时怎样使用 AI，为什么想做 AI Assistant，AI 提效的真实预期是什么？

去重：检索到另一个入口 URL 指向同一正文，按同场只保留当前稳定原帖；该候选人的 5/12–5/15 流程未在正式来源中出现。

---

## S006 阿里国际 / Lazada 交易｜Agent 开发实习｜一面 + 二面 + HR｜2026-04-22 / 04-27 / 05-07｜HUMAN-A

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

本批新增 `S004–S006` 共 **29 个 HUMAN-A 来源**，当前干净核心样本达到 **254 个**。

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

---

## S007 唯品会｜Agent 开发｜社招一面｜2026-08-28 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/64c0631bfa1d4dfa9be3d5956f8a3b97

真人 / 第一人称证据：作者以个人社招面试记录形式发布，问题围绕自己的生产故障、项目规模、历史重构与团队推动展开。

高价值问题：

1. 最近一次线上故障如何定位与处理？
2. 设计一个测试 Agent，真正需要交付哪些能力和验收指标？
3. Agent 的 DAU、数据量、任务量如何影响架构？
4. Agent 自动任务分配与调用链如何设计？
5. Agent 失败时如何兜底？Leader Agent 挂掉后 Multi-Agent 怎么恢复？
6. MCP 框架如何选，Transport Protocol 如何选？
7. Agent Bad Case 如何 Debug？
8. Text-to-SQL 的边界与风险是什么？
9. gRPC / tRPC、服务发现、负载均衡如何支撑 Agent Backend？
10. GMP / GC STW 等 Runtime 基础为什么在 AI Backend 仍然重要？
11. 回滚、A/B Test、流量分桶和统计显著性如何用于 AI 功能发布？
12. 异步队列如何防止消息丢失？

---

## S008 字节跳动抖音基础架构｜Agent 开发｜一面 90min｜2026-04-09 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/91c5394e57c14927841d7a86bfe427c2

真人 / 第一人称证据：作者明确记录 90 分钟一面和问题顺序，内容围绕自己的实习和项目逐层展开。

高价值问题：

1. Prompt Template 如何构建？
2. 为什么使用 Single Agent / Multi-Agent，Sub-agent 分别承担什么任务？
3. 代码生成系统如何统计 Branch Coverage，Code Instrumentation 如何实现？
4. AST / LSP 无法覆盖的代码如何提前识别和过滤？
5. Mock 如何实现，如何影响 AI 生成测试的有效性？
6. 多维 Query Rewrite 与需要用户补充信息的查询如何实现？
7. Intent Classification 为什么需要并行化？
8. Retrieval Pipeline 如何实现？
9. Context Engineering / To-do List 为什么能帮助模型聚焦？
10. Skill 的原理和实现是什么？
11. Self-Attention / QKV 为什么这样设计？
12. Python GIL、Lock / RLock、Semaphore 的机制与使用场景？

---

## S009 蚂蚁国际｜Agent 开发｜一面｜2026-05-09 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1f6e9337fb534f8c81326e3b55001e49

真人 / 第一人称证据：候选人以个人“凉经”形式记录同岗真人一面，问题围绕自己的实习、项目、笔试交互和交付流程展开。

高价值问题：

1. 从 AI 写代码到真正上线交付，完整流程应该怎样组织？
2. 前后端 + 中间件 + AI 的完整系统架构如何讲清楚？
3. 多应用 / 多仓库需求变更时，AI 如何跨系统完成修改？
4. 项目真实用了多少 Token，成本如何度量？
5. 如何降低 Token 成本？
6. SDD / TDD 如何与 Agent Coding 结合？
7. Skill 有哪些创建方式和组织形态？
8. Function Calling 的完整机制是什么？
9. Function Calling 与 MCP 的职责边界是什么？
10. MCP Client / Server 有哪些通信方式，如何配置？
11. Tool Schema 如何告诉模型有哪些工具可用？
12. 如何验证 AI 写出的代码真的正确，而不是“模型说完成了”？

---

## S010 小红书｜AI 后端开发｜秋招一面｜面试 2026-08-13，发布 08-20，75min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/169b2d8f7a134843b114b820ee692186

真人 / 第一人称证据：作者明确记录 8 月 13 日约 75 分钟 AI 后端一面，现场一开始就做算法，随后被长时间追秒杀、RocketMQ、Redis、MySQL，再进入实习平台、Agent 与 RAG。面后作者记录面试官反馈“多数能答，但缺少更深入思考”，具有强候选人现场状态。虽然基础后端问题占比很高，但后半场明确围绕 Agent Architecture / Memory / Intent / RAG / Evaluation，符合 AI Backend Role Scope；因此按规则保留整场技术问题。

整场技术问题：

1. Coding：实现 LRU Cache。
2. 为什么 LRU 通常使用 HashMap + Doubly Linked List，为什么不是单链表？
3. 除 LRU 外还了解哪些 Cache Eviction Policy，业务中怎样选择？
4. 秒杀 / 抢购场景最容易出现哪些并发与一致性问题，整体方案怎样设计？
5. RocketMQ Transactional Message 如何工作？
6. 为什么部分原子业务逻辑使用 Redis Lua？
7. Lua 为什么能在 Redis 中保证当前脚本执行的原子性？
8. MQ 在秒杀链路中承担削峰、异步和解耦中的哪些职责？
9. Redis 扣库存成功后，用户怎样最终获知数据库侧订单成功或失败？
10. Redis 预扣成功但 DB 写入失败时，一致性怎样恢复？
11. Optimistic Lock 的核心机制是什么，在库存更新中怎样实现？
12. Redis Set 的底层编码 / 数据结构怎样理解？
13. Redis 常见数据结构分别适合什么场景？
14. ZSet 使用 SkipList 时查询 / 插入复杂度怎样分析？
15. MySQL MVCC 的基本机制是什么？
16. MVCC 主要解决什么并发读写问题？
17. MySQL 四种 Isolation Level 分别是什么，适用场景和现象有什么差异？
18. 针对给定 SQL 怎样设计 Composite Index；如果查询不再使用 `user_id`，原索引还能否有效利用？
19. 联合索引中出现 Range Condition 后，后续字段为什么可能无法继续用于完整索引定位？
20. MySQL Index 的底层结构是什么，什么叫 Back-to-table Lookup？
21. 三层 B+Tree 大致能容纳多少行数据，估算依据是什么？
22. B+Tree 查询复杂度怎样理解？
23. 为什么数据库索引更常使用 B+Tree，而不是普通 B-Tree？
24. 大 Offset 的 `LIMIT` 为什么慢，怎样优化 Deep Pagination？
25. 使用子查询 / 覆盖索引优化深分页后为什么可能更快？
26. 当前秒杀方案是否已经完整解决问题，还有哪些边界和替代方案？
27. 实习中的 Coda 平台项目背景、工作原理、业务价值和本人职责是什么？
28. 怎样理解 Agent，一套完整 Agent Design 至少有哪些关键阶段？
29. Agent Memory 在什么时候写、什么时候读、一次应该取多少？
30. 了解哪些 Agent Execution Mode，不同模式怎样选择？
31. Agent Intent Recognition 不准确时，可以从哪些层优化？
32. RAG 是否真正落地过，知识来源、Retrieval 和 Generation 怎样组织？
33. 怎样评价 RAG 质量以及 Agent / Model 的整体效果？
34. RAG 不准确时，Parsing、Chunk、Embedding、Recall、Rerank、Prompt 分别怎样排查和优化？

去重：历史 `S148 / S148` 是另一条 8/7 小红书 AI 后端同 URL，重点为 HotKey / Watchdog / Deep Pagination → Agent / RAG；当前来源为不同日期、作者和招聘流程，并具有“秒杀 → RocketMQ Transactional Message → Lua → Optimistic Lock → MySQL 全链 → Coda 实习 → Agent / RAG”的独立题序。历史 `S027` 的 OpenManus / Harness 流程也与本场不同。

---

## S011 美团零食杂售｜AI 后端开发｜一面｜2026-09-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/9b94f595d15148869e0334029b5ddb67

真人 / 第一人称证据：候选人明确记录部门、岗位、面试日期，并描述自己被追问卡住的具体问题和等待结果状态。

高价值问题：

1. 实习项目迁移 / 改造如何证明正确性？
2. Agent 项目本人做了什么？
3. RAG 如何落地？
4. Tool Registry 为什么采用 Singleton，生命周期应该如何管理？
5. MySQL Slow Query 如何定位？
6. 什么情况下 Optimizer 可能放弃索引走 Full Table Scan？
7. 常见 Index Invalidation 场景有哪些？
8. 支付重复请求如何设计 Idempotency？
9. AI Coding：根据少量需求直接实现订单详情页面，如何补足验收标准？
10. Coding：Top-K / 第 K 大并限制复杂度。

---

## S012 启云方｜AI Agent｜一面｜发布 2026-09-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fea2d18bd59a421da7d16fe16223d38c

真人 / 第一人称证据：作者 `评论是德国的` 主页只有少量本人求职记录，能串起小鹏、BIGO、宁波银行等流程，不是批量面经账号。本场前约 12 分钟问问题，之后约 40 分钟要求候选人手画执行流程并与面试官讨论；核心不是“会不会背 Function Calling”，而是追到 Model Structured Output 与外部 Agent Runtime 的真实边界。

高价值问题：

1. 日常使用哪些 AI Coding Tool，在 VS Code 中实际接过哪些 API？为什么选择 Codex / CoderX，和 DeepSeek 使用体验怎样比较？
2. 如果项目主要使用 TypeScript，是否能接受并快速迁移？
3. 怎样理解 Agent，Agent Developer 实际在开发哪些层？
4. “通过语言调用工具”到底是什么意思？以天气 Tool 为例，自然语言输入之后如何走到真实函数执行？
5. Tool 是否需要提前注册，需要提供 Name、Description、Schema、Permission 等哪些 Metadata？
6. Tool Selection 是关键词 / Rule / Intent Recognition，还是模型基于 Tool Schema 自主选择？
7. 模型决定 Tool Call 后，调用信息返回在哪里？是否只是普通文本再用 Regex 解析？
8. Tool Call 为什么通常是 Structured Output，JSON / 固定字段在协议中怎样表示？
9. Assistant Text 与 Tool Call 是否属于不同 Content Block / Message Data？
10. 模型究竟有没有“直接执行工具”，还是只生成结构化调用请求，由 Agent Loop / Runtime 负责执行和回填？
11. 手画 System Design：系统包含 Agent Loop、Model、Tool、Filesystem，用户说“帮我写一个贪吃蛇小游戏”后，完整执行路径怎样流转？

去重：全历史回读未发现启云方正式样本；URL、作者流程和“天气 Tool → Structured Tool Call → 手画 Agent Loop / Model / Tool / Filesystem 贪吃蛇执行链”均独立。

---

## S013 字节跳动 App Infra｜Agent 开发｜秋招一面｜2026-08-26 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0bec32fbb3344ff98f16b97f47c7b857

真人 / 第一人称证据：候选人记录面试官岗位介绍、项目追问、多个“答得含糊 / 没答上”的现场状态以及面后对二面的判断。

高价值问题：

1. KV Cache 为什么能加速 LLM 推理？
2. 浏览器点击到服务端返回，一次请求经历哪些网络层？
3. TCP 为什么三次握手 / 四次挥手，四次是否总是必要？
4. MySQL 为什么用 B+Tree，Leftmost Prefix 如何工作？
5. Redis Cache Penetration / Breakdown / Avalanche 如何治理？
6. 多机器如何生成 Unique ID？若还要求近似单调 / 自增怎么办？
7. 这些基础设施能力为什么会成为 App Infra Agent 开发的一面核心？
8. Coding：基础排序实现。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## 本批观察

- Harness / Tool / Skill 已经进入 Runtime 与源码理解层面。
- MySQL、Redis、MQ、网络、并发仍是 AI Application / Agent 岗的重要底座。
- LLM Foundation 需要掌握应用工程深度，包括 Token、Attention、Long Context、KV Cache 等。
- 新增来源的价值主要是校准真实问法与优先级，而不是无限扩张学习题库。
