# Batch 07 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **29** 个正式来源。

---

## S115 腾讯｜AI 应用开发｜二面｜发布 2026-03-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e066e1295b46447b8224a59c5a4e8ac5

真人 / 第一人称证据：候选人以本人二面复盘发布，明确说明没有录音、只记录记得的问题，并保留“这个问题答得不太好”等现场自评；问题围绕自己的 Coding Agent / 软件工程实践连续追问。

高价值问题：

1. 即使模型拥有近乎无限 Context，为什么仍不应该把所有信息无差别塞入上下文？
2. 超长需求文档应怎样 Chunk，哪些信息必须长期保留？
3. 多个 Agent 独立修改代码时，如何用 Git Worktree 与接口约束隔离工作区并避免冲突？
4. Cursor 与 Claude Code 等 Coding Agent 在 Context / Worktree 使用方式上有什么差异？
5. Spec-driven Coding Agent 如何把需求、实现和验收串起来？
6. Context Compaction 为什么会保留近期消息、压缩更早历史，初始需求怎样防止被压丢？
7. OpenClaw 一类 Agent 的 `memory_search` / `memory_get` 思路如何理解？
8. Embedding Retrieval 后为什么不直接把所有候选都交给大模型做 Rerank？如何权衡 Context、Latency 与 Cost？
9. AI 驱动软件工程未来最重要的工程能力是什么，Evaluation 为什么重要？

---

## S116 嘉为科技｜AI 应用开发｜技术面｜面试 2026-07-15，发布 07-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fb4da04c8f2846b19060315fd05a2e4b

真人 / 第一人称证据：作者以本人 7 月 15 日面试发布“发面经攒人品”，25 个问题中持续保留“我说了什么 / 当时如何回答”的第一人称括注，问题从真实项目一路追到 Redis、Spring AI、JVM、并发与 Claude Code，具有自然面试流而非标准化题单。

高价值问题：

1. 项目里为什么使用 `CompletableFuture`，为什么需要自定义线程池？
2. 项目真实部署过吗，常见部署方式分别怎样选择？
3. Bloom Filter 的原理和适用场景是什么？
4. Redisson 可重入锁、Watchdog 如何实现，无限续期怎样避免演变成死锁？
5. Redis Cluster 与 Sentinel 的边界是什么？
6. Spring AI 中 Memory 如何实现，直接使用模型 SDK 与 Spring AI 的取舍是什么？
7. 批量导入同一券 / 卡密时如何处理并发、加密和重复发券重试？
8. 实习项目里的状态机如何保证消息重试后不重复执行？
9. Claude Code 在真实实习开发里怎么使用，哪些工作由人负责兜底？
10. MyBatis 接口代理、Bean 生命周期、Java 对象头与锁升级机制如何解释？

去重：URL 与标题均未在现有 Batch 命中；题序与项目链路未发现现有同场复制。

---

## S117 阿里千问事业群｜AI 应用研发工程师｜一面｜发布 2026-04-29｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4a666d0e366f4bd5899bdd219047ea60

真人 / 第一人称证据：作者为 AI 实习生，以本人面试记录发布，问题围绕自己的 Multi-Agent 平台连续追问；末尾还记录了面试官对其编程基础的直接反馈。

高价值问题：

1. Multi-Agent 平台的业务目标、系统链路和本人职责是什么？
2. 项目中最困难的问题如何定位并解决？
3. 平时使用 Vibe Coding 还是手写，模型怎样选？
4. 如何用 TDD、Brainstorming Skill 和测试约束 AI 完成任务？
5. Java 多态如何实现，为什么没有传统意义上的类多继承？
6. HashMap 扩容机制是什么？
7. Singleton 的实现方式有哪些，Double-Checked Locking 为什么要两次判空？
8. ConcurrentHashMap 如何支持并发访问，与 Fail-fast 迭代有什么关系？
9. HTTPS 传输 Body 主要使用对称还是非对称加密？
10. TLS 1.2 与 TLS 1.3 的主要工程差异是什么？

---

## S118 阿里平头哥｜AI 应用研发工程师｜暑期一面｜面试 2026-04-28，发布 05-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/51f34fe0d0cf4b918bd45dd4ec8824a9

真人 / 第一人称证据：作者明确给出公司、岗位、约一小时面试，并记录面试官很有耐心、会引导；问题从本人项目一路进入 Redis / MySQL、一致性、ReAct 与 RAG。

高价值问题：

1. Redis 与 MySQL 在同一 AI 应用中怎样做数据分层？
2. Cache Prewarm / Reload 如何实现？
3. Redis + MySQL Dual Write 怎样保证一致性，Transaction 是否足够？
4. 项目是否真正服务过用户，如何区分 Production 与练手 Demo？
5. ReAct 在项目中怎样实现？
6. 为什么不用 LangChain 完整承载链路，而选择部分能力自研？
7. RAG Retrieval 链路怎样设计？
8. AI 应用开发与传统 Java Backend 的能力边界如何理解？
9. Coding：真正交换链表节点，而不是只交换值。

---

## S119 小红书｜存储云平台·数据库智能化 / Agent｜日常实习一面 + 二面｜面试 2026-07-29 / 08-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4823889d98114bcba7e55eace6242353

真人 / 第一人称证据：作者给出 7 月投递、7 月 29 日一面、8 月 3 日二面的完整 Timeline，后续明确更新“二面已挂”；还对两位面试官的引导程度和现场体验作了个人复盘。

高价值问题：

1. OAuth 2.0 在真实服务里怎样实现？
2. Nginx 做负载均衡时能否同时承担限流，QPS 暴涨怎样保护系统？
3. MySQL 一条 SQL 从进入 Server 到返回结果经历什么？
4. 主流 Agent 的 Context Management Strategy 有哪些，Claude Code 为什么这样设计？
5. 群聊 Agent 如何处理权限、上下文和并行请求？
6. TCP 与 UDP 有什么差异，TCP 怎样保证可靠？
7. 进程与线程如何区分？
8. Model API 很慢时，产品和系统层怎样降低用户感知延迟？
9. OpenAI Chat Completion Request 常见字段怎样组织？
10. AI Coding 工具的 Context Management 有哪些差异？
11. Coding：层序遍历、有效括号、最长递增子序列。

---

## S120 米哈游｜Agent 开发｜提前批一面｜面试 2026-08-01，发布 08-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7b13b3c9e42745819ad822397a115812

真人 / 第一人称证据：作者明确写出 8 月 1 日面试与“已经凉凉”，并说明项目深挖占比很高、面试官围绕 Agent 实际流程继续向下追问。

高价值问题：

1. AI Coding 在日常研发中如何使用？
2. 如何验证 AI Coding 生成代码质量？
3. LLM Hallucination 为什么产生？
4. DeepSeek / OpenAI 等 Model API 常见接口如何理解？
5. Factuality / Faithfulness 怎样发现并治理？
6. Skill 与 MCP 有什么区别？
7. Skill 的核心特性是什么？
8. 个人 Agent 项目的完整流程、真实困难和优化点是什么？
9. Coding：Python Logging Decorator 或按业务约束过滤数据。

---

## S121 阿里｜Agent 开发暑期实习｜一面｜发布 2026-08-05，已 GG｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3181217280144ee0ab47fe979dc28ff1

真人 / 第一人称证据：作者以本人暑期 Agent 开发一面复盘发布，并明确更新已 GG；问题沿个人项目持续进入 Agent 架构、Vector Search、LangGraph、Memory、异常容错与 Coding，不包含标准答案扩写。

高价值问题：

1. 项目整体架构和技术栈是什么，Agent 在其中承担什么角色？
2. 从用户输入到 Agent 最终输出的完整执行链路是什么？
3. 项目做过哪些真实优化，收益如何验证？
4. 给定业务场景时，怎样从零拆 Agent / Workflow？
5. Semantic Search / Vector Database 在项目中怎样使用？
6. LangChain 与 LangGraph 分别负责什么，为什么这样选？
7. 模型输出怎样约束为结构化格式，并处理格式失败？
8. Memory 与 Multi-session Memory 怎样设计，如何避免不同会话串数据？
9. Tool / Model 异常时如何 Retry、Fallback 与恢复 Context？
10. Context 太长时如何优化？
11. Coding：贪心类现场题。

去重：URL 未在 `S001–S212` 收录；项目链与现有阿里 / 淘天 / 阿里云 Agent 来源不属于同一候选流程。

---

## S122 哔哩哔哩｜AI 应用岗 Agent 开发｜一面｜面试 2026-08-16，发布 08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0df78025653d492d86cc7b7273c2a0c2

真人 / 第一人称证据：作者明确写“8 月 16 号面的、给我面麻了”，直接以本人一面问题清单发布；正文没有标准答案，后续出现的“含完整答案”二次整理不计入本来源。

高价值问题：

1. 一个完整 Agent System 包含哪些模块，与普通 LLM Chatbot 的本质差异是什么？
2. Planning、Memory、Tool Use、Execution 各自承担什么职责？
3. Intent Recognition 用 Rule、Small Model、LLM Classification 时怎样选？
4. Zero-shot / Few-shot Intent Classification 分别适合什么数据条件？
5. 标注数据少时怎样提升 Intent Classification Stability？
6. RAG Offline Knowledge Construction 与 Online Retrieval / Generation 的完整流程是什么？

去重说明：后续检索到“2026-08-18 哔哩哔哩 AI 应用岗 Agent 开发一面（含完整答案）”等二次整理，只作为重复 / 教学内容排除，不贡献任何新增问题。

---

## S123 小红书｜AI 全栈开发｜业务交叉面 + 二面（同一候选人同流程合并）｜发布 2026-06-25 / 07-01｜HUMAN-A

业务交叉面来源：https://www.nowcoder.com/feed/main/detail/45d2815e4dc54a2fa9161273f6046c97

二面来源：https://www.nowcoder.com/feed/main/detail/b0aba5ebac994002a27bf0892b8991f9

真人 / 第一人称证据：两个页面均由同一作者 `Recall_15` 发布，岗位均为小红书 AI 全栈开发；首轮约 40 分钟，作者记录面试官对业务、AI Coding 和系统上线的具体追问，二面再次约 40 分钟并写“问很细、95% 答上来、希望能过”等现场状态，因此合并为一个招聘流程来源。

高价值问题：

1. 实习里的 AI 开发到底难在哪里，哪些部分是候选人独立完成？
2. 一个功能从 Task 到 Production Release 的完整流程是什么，上线看哪些正 / 负向指标？
3. 从零做一个 AI 产品，前端、后端、部署和运维分别要承担什么？
4. 大模型流量突然上涨时，如何监控、扩容、降级和回滚？
5. AI Coding 生成的低质量代码有哪些典型问题，怎样人工兜底？
6. 给一个模糊需求，如何快速做多平台 Prototype / MVP，并定义验收时间和标准？
7. 视频编辑 Agent 的核心难点是什么，Tool Call / Memory / Prompt Orchestration 怎样组织？
8. 文本 → 编辑脚本 → 视频的完整链路怎样设计，视频质量如何 Evaluation？
9. 如何把生成 / 编辑延迟从约 30 分钟降到约 5 分钟，并证明优化有效？
10. 音视频同步、分辨率、字幕等工程问题如何保证稳定性？
11. LangGraph 在这类 Agent 中承担什么关键职责？
12. 多模态知识库怎样做可验证 Retrieval，关键帧如何选择？

去重：两条 URL 为同一作者、同公司、同岗位连续轮次，主动合并为一个 `Sxxx`；现有正式来源未出现该作者和视频编辑 Agent 项目链。

---

## S124 字节跳动财经｜AI 应用开发后端｜日常实习一面｜发布 2026-05-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/09fac7f955d34c1d8fc50f9a25fce714

真人 / 第一人称证据：作者明确写“分享面经攒 RP”，记录面试官先介绍业务、再从项目连续追到 Agent 与 Backend Foundation，并保留自己对项目挑战回答不好的状态。

高价值问题：

1. Transformer 的核心执行流程如何解释？
2. MCP、RAG、Skill 分别解决什么问题？
3. 为什么使用 LangGraph 而不是直接原生编排？
4. Context 太多时如何治理？
5. ReAct 如何工作？
6. 数据库事务隔离级别有哪些，底层如何实现？
7. OS Deadlock 的条件是什么？
8. 浏览器访问 URL 时 DNS / HTTP 链路怎样发生？
9. Coding：输出树中路径和为 K 的路径。

---

## S125 京东｜AI 应用开发｜实习一面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d8dae532f7e4479d8e3fa71e6ca24631

真人 / 第一人称证据：作者以本人同岗一面形式发布并邀请交流；面试官要求现场展示项目代码，随后沿 RAG、Vector DB、Multi-Agent、Redis / MQ、Thread Pool 与 JVM 继续追问，具有明显项目验真特征。

高价值问题：

1. RAG 的原理、项目用法与实际收益是什么？
2. Vector DB 的作用和基本索引思想是什么？
3. 为什么使用 Multi-Agent，而不是 Single-Agent？
4. 项目代码能否现场展示，如何证明不是 Demo 包装？
5. Redis ZSet 在业务中怎样使用？
6. MQ 在项目中解决什么问题？
7. 多线程与 Thread Pool 怎样用于真实任务？
8. JVM Memory Model / Runtime Memory Area 怎样理解？
9. Garbage Collection 的主要机制是什么？
10. Coding：Longest Common Prefix。

---

## S126 阿里灵犀｜AI 应用｜暑期一面｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/26012e0bdf7c493e824b1e29913ff9d4

真人 / 第一人称证据：作者以明确的阿里灵犀 AI 应用暑期一面问题记录发布，问题从个人实习进入 RAG / LangGraph / LLM Foundation 与业务算法，不是标准答案或合集。

高价值问题：

1. Traditional ML / NLP 与 LLM Application 的核心差异是什么？
2. RAG 与 Fine-tuning 怎样取舍？
3. LangChain 与 LangGraph 的核心概念和工程边界是什么？
4. 多种游戏资源组合下如何设计最大收益算法？
5. Transformer Architecture 的主要模块是什么？
6. Multi-Head Attention 为什么存在？
7. AI Application Development 与传统 Application Development 的本质差异是什么？
8. FFN 在 Transformer 中承担什么作用？

去重说明：检索到后续高度相似的“27 暑期阿里灵犀 AI 应用开发一面”等版本，优先保留更早且正文稳定的本帖，不重复计数。

---

## S127 汇川技术｜AI 全栈开发工程师｜一面 + 二面｜面试 2026-08-27 / 08-28｜HUMAN-A

一面来源：https://www.nowcoder.com/discuss/925156092424749056

二面来源：https://www.nowcoder.com/discuss/925159879197630464

真人 / 第一人称证据：同一候选人连续记录两轮技术面，二面页面明确更新“已 OC”，并说明最终因实习安排放弃；问题紧贴本人实习、AI Refactor、OpenSpec、MySQL / Sharding 与 Full-stack 能力。

高价值问题：

1. 如何证明 AI Refactor 前后功能行为保持一致？
2. Java 21 / 新 JDK 相比 JDK 8 有哪些值得工程关注的变化？
3. OpenSpec / Superpower 等 AI Coding 方法解决什么问题？
4. MySQL Data Sync 怎样做？
5. 分库分表有哪些策略，什么时候横向 / 纵向拆分？
6. 水平分片怎样保证数据分布相对均衡？
7. 按时间范围查询时，Sharding Key 应如何设计？
8. 核心业务消息怎样做 Dedup / Idempotency？
9. AI Full-stack 岗如何平衡前端、后端和 AI Service 能力？

---

## S128 OPPO｜AI 全栈开发｜一面｜发布 2026-08-23，次日查看已挂｜HUMAN-A

来源：https://www.nowcoder.com/discuss/920830730643443712

真人 / 第一人称证据：候选人记录面试官开场介绍这是较新的 AI Full-stack 岗位，并说明面试不足 30 分钟；作者自评题基本答出但语言组织不佳，次日查看流程已挂。问题把 AI Coding / Skill 与项目上线、团队协作和基础数据结构放在同一场，现场与结果明确。

高价值问题：

1. 平时实际使用哪些 AI Development Tools，各自适合什么任务？
2. AI 生成代码质量差时怎样修正、测试和验证？
3. 怎样用 Skill 提升研发效率，什么能力值得沉淀成 Skill？
4. `grill-me` 类 Skill 为什么文本很短仍可能有效，核心约束在哪里？
5. 项目中本人担任什么角色，具体负责什么？
6. 项目真正上线了吗，如何验证使用效果？
7. 团队出现技术分歧时怎样处理？
8. Array / Linked List / Stack / Queue 的差异是什么，BFS 为什么通常使用 Queue？
9. AI 全栈岗位为什么仍要求能解释基础数据结构和完整产品实现？

去重：URL、岗位介绍和面后状态未在现有 OPPO AI 全栈样本中出现；与 `S106 / S067` 等为不同候选人独立流程。

---

# 本批清洗与研究观察

本批正式新增：**16 个 HUMAN-A（S042–S128）**。

---

## S129 深圳 Tuitti / 视界之外｜Coding Agent / AI Backend 实习｜一面｜发布 2026-09-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/9b1329caf4b64389a0ab666585bda045

真人 / 第一人称证据：岗位标题未直接写 Agent，但整场 60+ 个问题都围绕候选人的类 Claude Code Coding Agent、Checkpoint / Trace、上下文恢复、后端基础和多人多 Agent 平台展开，满足 Role Scope“实际职责优先于职位名”的规则；正文为原始一面问题记录，可稳定核验。

高价值问题：

1. 类 Claude Code Coding Agent 参考了哪些开源 / 闭源架构，技术选型依据是什么？
2. ReAct 与 Planner→DAG 的组合属于什么 Agent Paradigm？
3. Planner 把任务拆成带依赖和验收条件的 DAG 后，Runtime 怎样执行？
4. 用户中途退出或任务失败后，Graph 怎样 Resume？
5. Trace / Checkpoint 应保存哪些字段，怎样保证一致性并控制冗余？
6. Planning Summary 与 Session / Context 如何关联？
7. 恢复历史任务时模型应该看到 Summary、完整消息还是分层 Context？
8. Trace Replay 如何用于可靠性测试与 Debug？
9. 核心模块“90% Coverage”到底是什么口径，怎样证明？
10. HTTP / HTTPS、TCP/IP、Port / Process、Thread / Coroutine 等 Backend Foundation 如何解释？
11. Dependency Injection 与 Singleton / Dependency Inversion 的边界是什么？
12. 多用户各自选择不同 Agent 时，中立平台如何协调身份、偏好和跨设备协作？

---

## S130 腾讯 WXG 微信读书｜Coding Agent / Agent 工程方向｜一面｜2026-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3ffc762437274543b6a8f5e2ea6fb535

真人 / 第一人称证据：作者以“27 届秋招一面（已挂）”发布，记录会议室、现场 Coding 没完全写完和“秒挂”等非常具体的现场状态；问题大量绑定自己的 Coding Agent 实习，因此按实际职责通过 Role Scope。

高价值问题：

1. Coding Agent Memory 应如何设计？
2. 自研 Agent 与 Claude Code / Codex 的差异是什么？
3. Agent Evaluation 应怎样构建？
4. Cloud Agent Container Restart / Migration 后怎样持久化 Context？
5. Task Goal 持久化后，怎样避免恢复执行产生 Behavioral Drift？
6. Model Backend 怎样选择和适配？
7. 当基础模型越来越强时，Agent Runtime 仍然最重要的工程价值是什么？
8. Lost in the Middle 为什么出现？
9. Coding：Big Integer Multiplication，并现场处理边界和实现问题。

---

## S131 小红书社区工程｜AI 与全栈｜一面｜面试 / 发布 2026-03-21｜HUMAN-A

来源：https://www.nowcoder.com/discuss/864966931239952384

真人 / 第一人称证据：作者主页身份与“小红书社区工程部 AI 与全栈实习员工”一致，并记录忘记录音、只复盘记得的问题以及“已约二面”；问题虽然大量是 Backend Foundation，但岗位本身明确是目标 AI / Full-stack。

高价值问题：

1. Coding：Longest Increasing Subsequence，现场不会时面试官如何切换题目？
2. Coding：Binary Tree Level-order Traversal。
3. Process / Thread 的区别是什么？
4. Heap / Stack 的内存特点是什么？
5. Redis Eviction 与 Expiration 有哪些机制？
6. MySQL Deep Pagination 为什么慢，怎样优化 SQL？
7. 项目为什么这样设计，真实来源和职责是什么？
8. 用户口语化 Query 导致 RAG Miss 时怎样治理？
9. Redis Set BigKey 有什么风险？
10. 平时如何使用 AI Coding Tool？

去重说明：4 月 2 日出现一篇题序几乎逐条一致的“小红书 AI 全栈日常实习”帖子；本批保留更早、作者身份与招聘时间线更强的 3 月 21 日来源，后发版本不重复计数。

---

## S132 阿里高德地图｜AI 应用开发｜一面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/eb2fe3c0e80549939c8bc55a621f449e

真人 / 第一人称证据：作者明确以同岗一面分享发布并写“攒人品、欢迎同岗交流”，题目围绕 Code RAG、Retrieval、Memory、Skill / MCP 和 Claude Code 主循环连续深入，没有附标准答案。

高价值问题：

1. Code RAG 为什么常用 AST 拆函数片段，从代码文本到 AST 的过程是什么？
2. 同时存 Code Chunk 与 Comment 时，Retrieval Schema 怎样设计？
3. RRF Fusion 如何工作，参数 / 权重怎样理解？
4. Coarse Rank 与 Fine Rank 分别解决什么问题？
5. RAG Single-turn 与 Multi-turn Retrieval 怎样选？
6. Markdown / PDF 怎样 Chunk？
7. Agent-based Chunking 遇到 Context Too Long 怎样处理？
8. Skill 与 MCP 的职责区别是什么？
9. Short-term Memory 怎样处理 Context Explosion？
10. ReAct 与 Agent Loop 的关系是什么？
11. Claude Code Query Inner Loop 与 Session Loop 分别做什么？

---

## S133 字节跳动｜后端 AI 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/684c3c18ca774b149ea859a14ca9c323

真人 / 第一人称证据：作者明确以本人“字节暑期后端 AI 开发一面”复盘发布并写“面完人都通透了”；整场真实地以网络、Redis、并发和 AI Coding / Agent 约束为主，属于目标 AI Backend Foundation 样本。

高价值问题：

1. Gateway 为什么选择当前协议，如果自己设计为什么考虑 TCP？
2. TCP 怎样保证可靠传输？
3. TCP 三次握手、四次挥手分别解决什么问题？
4. Redis 丢数据时怎样恢复，持久化和高可用如何理解？
5. Java 如何控制并发，`synchronized` 与 `ReentrantLock` 怎样实现？
6. AQS / CAS 的核心机制是什么？
7. 平时怎样使用 AI Coding？
8. 怎样向 Agent 声明工程约束，并让约束跨会话 / 长任务持续有效？
9. Coding：数值格式化计数类场景题；追问 B-Tree / B+Tree 相等判断。

---

## S134 字节跳动｜后端 AI 开发｜暑期二面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/12cfda50776f482ba03bb775bb720238

真人 / 第一人称证据：作者明确以本人二面凉经发布并更新进入人才库；问题由项目和秒杀一致性继续进入 MySQL、Agent / RAG 与严格输入输出 Coding。

高价值问题：

1. Flash Sale 如何防止 Oversell / Undersell？
2. Redis 扣库存与数据库最终订单状态如何保持一致？
3. Redis 成功但 DB 失败时怎样 Compensation？
4. MySQL Replication、Transaction 和 Isolation 如何影响高并发订单正确性？
5. Agent 的核心组成是什么，为什么不是一次 LLM Call？
6. RAG 的 Retrieval → Generation 链路如何解释？
7. Coding：链表求和类变体，并严格处理输入输出与边界条件。

---

## S135 腾讯｜后台 AI 开发｜一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ae63356673914217b3d9c986e6de8814

真人 / 第一人称证据：作者直接以本人“后台 AI 开发一面凉经”发布并保留“还是太菜”的个人状态；面试从实习和项目真实性连续追到库存一致性、Redis Atomic Operation 与现场代码 Debug。

高价值问题：

1. 实习里怎样整合多个数据源生成业务日报？
2. 项目真正有价值的功能亮点是什么？
3. 秒杀怎样防止 Oversell？
4. 不用 Lua 时，Redis 自带哪些 Atomic Command 可以利用？
5. Redis 扣库存后宕机怎样保证最终业务正确？
6. Coding / Debug：给定一段 C++ 代码现场找错并解释原因。

---

## S136 阿里淘天｜AI 应用研发｜一面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/80058a5c487347b5bbf7c8e5d694377d

真人 / 第一人称证据：作者明确写“一面 2h 没招了、发面经攒人品”；问题从两个本人实习项目深挖到 RAG、LangGraph、Kafka、Text-to-SQL，最后还有约 45 分钟 AI Coding。

高价值问题：

1. RAG Document Chunking 怎样设计和维护？
2. 怎样发现 Retrieval Error 导致的 Hallucination，并定位问题？
3. Vector DB 怎样选型？
4. LangGraph State Machine 的 State 怎样流转？
5. LangGraph 与 LangChain 的差异和使用场景是什么？
6. Kafka 出现高峰 Message Backlog 时怎样治理？
7. 怎样区分 Message Backlog 是突发流量还是 Consumer Capacity 不足？
8. Telemetry 数据消费是否要求严格顺序，为什么？
9. Text-to-SQL 怎样处理自然语言歧义和 Multi-table Join Field Mapping？
10. AI Coding：设计可扩展且安全的订单状态机引擎。

---

## S137 快手｜Agent 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/be29f78d1c174fe2ab2af85f89f6b792

真人 / 第一人称证据：作者以本人 Agent 一面“发面经攒人品”发布，问题从实习与 AI Coding 进入 Java Concurrency / JVM / HTTPS 基础，并有现场 Coding。

高价值问题：

1. AI Coding 未来可能发展到什么程度，目前最大不足是什么？
2. 什么场景值得使用 Multi-threading？
3. `synchronized` 与 `ReentrantLock` 的差异和适用边界是什么？
4. ThreadLocal 解决什么问题，又可能引入什么风险？
5. Thread Pool Worker 抛异常时会怎样，业务如何感知失败？
6. HTTPS 为什么安全，TLS 大致如何建立安全通道？
7. Java Thread State 怎样变化，线程怎样正确终止？
8. Reflection / Dynamic Proxy 如何实现，什么场景触发 Class Loading？
9. Coding：3Sum。

---

## S138 虾皮｜后端 AI 开发｜二面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ad22a4b4908848519a72f8c94925c081

真人 / 第一人称证据：作者明确以本人“春招后端 AI 开发二面 1h”发布并写“攒攒人品”，约 30 分钟持续拷打实习，随后从 MQ Reliability 进入海量数据系统设计与 Coding。

高价值问题：

1. 引入 MQ 做 Data Sync 会产生哪些一致性和可靠性问题？
2. MQ 怎样尽可能避免 Message Loss？
3. 9 亿个 IP 地址怎样做 Dedup？
4. 去重后 8 亿个 IP 的 Whitelist Service 怎样设计？
5. 不同方案大概需要多少 Memory，怎样估算？
6. Coding：用两个 Stack 实现 Queue。

---

## S139 联想｜Agent 应用开发｜实习一面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1f425d6759cf4857ace42e56f14cb79f

真人 / 第一人称证据：作者明确以“联想 Agent 应用开发 27 实习面经”发布并保留明显的面后状态；问题围绕本人 ASR / Agent 项目、Context Compression、Evaluation、MCP / Skill 连续展开。

高价值问题：

1. ASR Model 怎样选型，Latency 怎样测量和优化？
2. Streaming / Non-streaming ASR 各有什么工程取舍？
3. Main Agent 的 Intent Recognition 怎样实现？
4. Main Agent / Sub-agent 怎样选模型，多需求怎样拆分？
5. Agent Evaluation Metric 怎样定义？
6. Context Compaction 的具体实现是什么？
7. 用户近期 Writing Style 怎样提取并使用？
8. 怎样评价一个开发 Agent 的好坏？
9. MCP Tool、Skill、Progressive Disclosure 怎样理解？
10. 模型怎样判断应该加载哪个 Skill？
11. OpenClaw / Vibe Coding 等产品和范式怎样理解？

---

## S140 阿里国际｜AI 应用研发｜二面｜发布 2026-04-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8610272cb5ea4e53a3281a3fbe0cc9a3

真人 / 第一人称证据：作者以本人二面分享发布并写“面完人都通透了”；问题直接围绕 Agent Project 的数据量、Vector DB、Evaluation、Scale、Inference Service 与 AI Coding 深挖。

高价值问题：

1. Agent Project 的数据规模、Vector DB 选型与完整执行流程是什么？
2. Embedding Model 升级后怎样保证 Index Vector 与 Query Vector 逻辑一致？
3. Agent Tuning 怎样评估，Evaluation Dataset 怎样构建？
4. 能否讲一两个真实优化后效果明显的 Case？
5. 数据量和 QPS 增长后，Agent Architecture 怎样扩展？
6. 对低 RT 要求如何部署和加速，GPU / Inference Resource 怎样估算？
7. 是否自己部署过 Inference Service，做过哪些 IO / Serving Optimization？
8. AI Coding Tool 对研发效率的真实提升怎样量化？

---

## S141 腾讯｜Agent 开发｜暑期一面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/427caf4cc5ec4192b64fdb6ea6698bef

真人 / 第一人称证据：作者以“暑期腾讯 Agent 开发一面、攒人品中”发布，整场从本人项目进入 RAG、ReAct、Embedding、Model Training Choice 和 Coding，信息链自然。

高价值问题：

1. 是否真实部署过 LLM，部署经验包含哪些层面？
2. 项目的 Conversation Flow 怎样运行？
3. 面试官与 AI 生成问题冲突时怎样处理？
4. 如何把当前系统升级成 Virtual Conversation / Simulation？
5. 哪些项目真正需要 RAG，数据怎样存？
6. Embedding Model 怎样选，Chunking 怎样做？
7. Hard Chunking 在实践里会造成哪些问题？
8. ReAct 在具体项目中怎样设计，实际表现如何？
9. 什么项目适合 Fine-tuning，什么项目适合 RAG？
10. Fine-tuning Dataset 从哪里来？
11. Coding：Self-Attention / Detection Model 相关现场实现。

---

## S142 阿里淘天｜AI 应用研发｜秋招一面 + AI Coding｜面试 2026-08-26，发布 08-27｜HUMAN-A

来源：https://www.nowcoder.com/discuss/922452114809376768

真人 / 第一人称证据：同为作者 `Florentino_73` 的本人求职记录，但这是 8 月 26 日淘天 AI 应用研发独立面试，和 8 月 31 日阿里云 Agent Infra 属于不同组织 / 岗位与独立招聘流程，因此不合并。正文记录约 30 分钟项目深挖、5 分钟业务数据结构题、约 30 分钟 AI Coding，并在反问中确认业务重点是把平台商家与用户场景 Agent 化，Role Scope 明确。

整场技术问题：

1. 约 30 分钟自我介绍和项目介绍，主要深挖华为项目中的模型调优与 RAG 相关问题。
2. 某个 URL 一秒内涌入大量需求，但系统只能处理 100 个时，适合使用什么数据结构？
3. 需要实时维护商品销量 Top 10，适合使用什么数据结构？
4. AI Coding：实现商品计价系统，优惠策略需要能够随时更新，例如会员价、满减等。
5. 围绕平时使用 AI Coding 的心得和实际遇到的问题继续交流。
6. 反问：团队主要把平台商家与用户场景做 Agent 化。

去重：已直接回读 `S001–S269`。历史阿里 / 淘天 AI Application 来源很多，但没有当前作者的 8/26 流程和“华为模型调优 / RAG → 单 URL 高并发容量 → 实时商品 Top10 → 动态优惠商品计价 AI Coding”连续题序。同作者 8/31 阿里云为独立招聘流程，按规则分别计数。

---

## S143 字节跳动｜Agent 开发｜暑期一面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d34ec2281429417eb546f160f181cdfa

真人 / 第一人称证据：作者明确记录约 40 分钟真人一面并写“发点面经攒攒人品”，问题围绕本人项目持续深挖，随后直接进入 OpenClaw、Claude Code Memory、AI Coding 与 Context Length。

高价值问题：

1. Agent Project 的完整流程和实现细节是什么？
2. 实习项目有哪些真实缺陷，若重做会怎样优化？
3. LLM Output 不遵循 Instruction 时，怎样通过具体 Case 定位和修复？
4. 对前沿 Agent 产品 / OpenClaw 的理解到什么深度？
5. Claude Code 的多层 Memory 为什么这样设计？
6. 日常怎样使用 AI Coding Tool？
7. Cursor / Coding Agent 在 Context 过长时为什么可能发生性能或效果下降？

---

# 本轮明确排除 / 去重

本批搜索量继续扩大，但以下内容仍然 **零贡献**：

- 2026-04-02 一篇与 03-21 小红书社区工程 AI 与全栈题序几乎逐条一致的后发帖子：按重复处理；
- 阿里灵犀同一套题的后续高度相似版本：只保留更早、正文稳定的 04-03 来源；
- 哔哩哔哩原帖之后出现的“含完整答案 / 三年面试五年模拟”二次整理与跨站搬运；
- 迅雷“服务端开发(AI)”等页面：虽然题目看起来很贴目标方向，但正文已混入答法 / 方法论，并位于“AI-Agent 面试实战”内容链，不能作为 HUMAN-A；
- 小米 / 月之暗面等付费或内容创作者型“面经”页面，正文无法稳定核验候选人本人和完整现场；
- 凌脉等技术问题覆盖很漂亮但正文过于模板化、候选人本人现场痕迹不足的帖子；
- AI 自动面试 / 模拟面试、题库、标准答案、SEO 聚合、粉丝投稿、课程导流；
- 字节剪映等只能从搜索列表看到标题 / 摘要，却没有稳定原帖 URL 的线索；
- Role Scope 外的普通后端、测试 / 测开、纯训练算法岗位，即使顺带出现 Agent 名词也不计。

# Batch 07 观察

本批新增 `S115–S143` 共 **30 个 HUMAN-A 来源**，当前干净核心样本达到 **147 个**。

本轮最重要的信号：

1. **来源仍明显未饱和。** 在已有 117 个 HUMAN-A 后，再次系统回扫仍能新增 30 个独立来源，说明常规搜索首页远不是供给上限。
2. **Coding Agent / Harness 开始进入“软件工程基础设施”层。** Worktree、Spec、DAG、Trace、Checkpoint、Resume、Compaction、Memory Search、Evaluation、AI Refactor Equivalence 都来自真人项目追问。
3. **AI Backend Foundation 的权重继续被独立来源确认。** MySQL Transaction / Sharding、Redis Atomicity / Consistency、MQ Reliability、Thread Pool、TCP / HTTPS、JVM、Nginx、Rate Limit 与 Agent / RAG 同场出现。
4. **RAG 的真实问法越来越偏实验和故障。** Chunk / RRF / Rerank / Hybrid Retrieval / Vector DB / Query Ambiguity / Dynamic Embedding Upgrade 不只问定义，而问选择依据、失败表现和验证方法。
5. **同一招聘流程需要保守计数。** 本轮主动把小红书 AI 全栈、汇川 AI 全栈的一二面合并为一个候选人来源，并抓出多个后发重复版本；后续继续用“URL 去重 + 题序 / 项目语义去重 + 作者时间线”三层去重。
6. **HUMAN-A 不能被“漂亮题目”绑架。** 答案型专栏、内容营销、付费页面、模板化帖子即使比真人原帖更完整，也继续保持零贡献。

停止条件不变：继续扩大跨公司、岗位、月份、轮次与平台 Recall；只有连续多轮搜索几乎不再出现新的独立 HUMAN-A，同时新增问题分布也稳定收敛，才进入收尾阶段。
