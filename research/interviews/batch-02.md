# Batch 02 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 本批继续执行统一固定标准：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 这次主动扩大了搜索召回，而没有降低质量门槛：除了直接关键词检索，也沿着牛客话题页、企业页、搜索索引、候选人个人博客和跨平台原帖回溯。搜索过程中发现的大量“含完整答案 / 高频题 / 帮粉丝复盘 / 资源导流 / 二次整理”内容均未进入本批。
>
> 本文件只保存来源元数据、真人/第一人称证据与问题的简洁转述，不复制第三方正文。

---

## S014 阿里云｜AI Agent 平台研发工程师｜一面｜2026-04-28 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/476de2514a3c457c8be774623549f4b1

真人 / 第一人称证据：作者明确写出“面完后第二天挂”，并记录自己多个问题不会、被面试官继续追问以及反问业务内容。

高价值问题：

1. ReAct 与 Plan-Execute-Replan 分别适合什么场景，本质区别是什么？
2. 如何在不明显损伤 Agent 效果的前提下降低 Token 消耗？
3. Function Calling、MCP、Skill 分别解决什么问题？
4. Skills 与 Rules 有什么区别？
5. Temperature 与 Top-K 如何影响模型生成？
6. Redis Hash BigKey 如何治理，迁移后如何兼容老数据和老业务？
7. 为什么生产业务需要谨慎使用 ThreadLocal？
8. 事务的核心性质是什么？
9. TCP 如何保证可靠传输，拥塞控制如何工作？

---

## S015 百度｜Coding Agent｜秋招一面 + 二面 + 三面｜2026-08-18 / 08-21 / 08-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b9521e2b51e04afeac0a3a32e13f4da9

真人 / 第一人称证据：作者给出三轮具体日期，一面后电话秒约二面，二面后继续约三面，最终明确记录“三面挂”；正文大量保留被问住、感觉不匹配、答得一般等现场状态。

高价值问题：

1. Python 与 Java 做工程项目时的主要差异是什么？
2. Coding Agent 的整体架构、ReAct、Tool Calling 和 Context 应如何设计？
3. Agent 流程一定优于单次 LLM 调用吗，如何证明方案选择合理？
4. 如何从零设计类似 Claude Code / Codex 的 Coding Agent？
5. 相似 Skill 被错误路由、单 Skill 被错误执行时如何检测和恢复？
6. Skill 的注册、选择、动态入参与完整执行流程如何设计？
7. 多任务 Context 如何隔离，如何控制 Agent 并发与 Secret 泄露？
8. 云端 Agent 容器重启 / 迁移时如何保留会话与任务状态？
9. MySQL MVCC、线程池、AOP/JVM 等 Backend Foundation 如何解释？
10. 进程 / 线程 / 协程、用户态 / 内核态、缺页中断和页面置换等 OS 基础如何联系起来？

---

## S016 字节跳动｜Agent 开发日常实习｜一面｜2026-08-27 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d2cf5165d1184b59879eff5793b7b453

真人 / 第一人称证据：候选人按“项目拷打 → 八股 → 聊天 → 手撕”的真实面试顺序记录问题，Coding Agent 项目存在连续深入追问，并附具体现场 Coding 题。

高价值问题：

1. Coding Agent 如何做 Session / Conversation 管理？
2. Context 中 Token 如何计算，为什么这样计算？
3. Context Compaction 如何实现，压缩 Prompt 如何设计？
4. 压缩结束后如何确认 LLM 真的完成了正确压缩，而不是仅口头宣称完成？
5. Skills 如何管理与按需加载？
6. Single-Agent 和 Multi-Agent 如何选，是否需要 Sub-agent？
7. 进程与线程是什么关系？
8. 浏览器输入 URL 到页面展示经历了什么？
9. MySQL 如何做去重，`ROW_NUMBER()` 如何使用？
10. 手撕：按不同数据类型规则递归合并嵌套 JSON，且不能修改原对象。

---

## S017 字节跳动｜AI Agent 日常实习｜一面 / 二面记录｜2026-08-13 / 08-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8a553bb6ea8445d0b0abe11e87614cea

真人 / 第一人称证据：作者明确记录一面、二面日期与“日常实习、Agent 方向”，问题围绕自己的 Coding Agent 项目连续展开，并记录后续等待状态。

高价值问题：

1. Coding Agent 的整体架构如何设计？
2. ReAct 与 Plan 模式适合什么任务？
3. Context 超过模型窗口时有哪些治理方式？
4. Compaction 应保留哪些事实、约束和未完成状态，如何避免忘记历史需求？
5. Agent 发生路径震荡 / 重复尝试时如何检测和优化？
6. Memory 的提取、存储、检索与长期 / 短期边界如何设计？
7. MCP Tool 的调用链路是什么？
8. Tool 数量过多导致 Prompt 膨胀、Tool Result 过大时怎么办？
9. Prompt Cache 如何工作，怎样提高命中率？
10. Multi-Agent 如何分工、通信并避免多个 Agent 同时修改文件产生冲突？

---

## S018 字节跳动｜AI Agent｜秋招一面｜面试 2026-07-21｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/8b2fdbdf61184235bc4210760250663e

真人 / 第一人称证据：候选人明确给出面试日期，并写到即使提前准备仍不断被追问，带有明显个人现场感受和“发面经攒人品”记录。

高价值问题：

1. MySQL 索引在什么情况下失效，LIKE 模糊查询如何影响索引？
2. MQ 在 AI Agent 系统中承担什么职责，为什么不直接通过数据库通信？
3. Redis 在 Agent 系统里有哪些使用场景，缓存策略如何设计？
4. RAG 为什么会引入父子索引？BM25 与向量检索如何融合？
5. ReAct 的工程实现与 Message Format 应如何设计？
6. Tool Response 应以什么消息角色返回，为什么？
7. Agent Memory 如何做短期 / 长期分层？
8. 多模态模型的视觉编码器与语言模型如何连接？
9. Agentic CPT、SFT、RL 等训练阶段在应用侧需要理解到什么程度？

---

## S019 拼多多｜Agent｜一面｜面试 2026-08-23｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/ee971b755cbd475a91ef62cee38cdac8

真人 / 第一人称证据：候选人给出明确一面日期、岗位主题与秋招面试记录标签，问题围绕自己的服务和 Agent 项目连续展开，并记录现场手撕。

高价值问题：

1. 服务端宕机时如何实现用户无感恢复，并保证业务不中断、数据不丢？
2. 服务迁移时如何做到用户无感，网关如何路由到真实后端？
3. Agent 项目到底解决什么痛点，固定规则是否足够？
4. Skill 中如何防止业务数据和核心脚本泄露？
5. MCP 是什么，为什么项目选择自行封装而不是 MCP？
6. Skill 与 MCP 的核心差异是什么？
7. 为什么一些 Agent 产品从“所有能力 MCP 化”转向 Skill / Instruction 类能力封装？
8. 手撕：Word Search II。

---

## S020 腾讯｜后端 Agent 开发实习｜一面｜2026-04-27 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e97f7836e506423fb750561ce054926f

真人 / 第一人称证据：候选人以个人实习面经形式发布并写明“攒人品”，问题从实习经历连续进入并发、MySQL 日志、事务和 Agent Skills。

高价值问题：

1. Java 线程创建过程与生命周期如何解释？
2. 一条 HTTP 请求的完整过程是什么？
3. 读方法与自增方法并存时如何实现并发安全？
4. redo / undo / binlog 分别做什么，为什么 MySQL 需要这些日志？
5. `UPDATE ... t=t+1 WHERE id=?` 的执行链路是什么？是否可能引发索引页变化？
6. Spring `@Transactional` 在内部调用与异常场景下如何回滚？
7. 平时如何使用 AI Coding？
8. Skills 与 Rules 的联系和区别是什么？
9. 使用 Skills 是否真的能降低 Token，为什么？

---

## S021 腾讯｜Agent 开发实习｜一面｜2026-03-30 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/86c7a1d799984400905ce219c818515f

真人 / 第一人称证据：作者明确以自己的实习 Agent 面试复盘发布，并写到“给我面没招了，发点面经攒人品”，问题呈现项目 → RAG → Agent → Streaming 的自然链路。

高价值问题：

1. 一个完整 RAG 系统由哪些核心部分组成？
2. 文档 Upload / Chunk 如何实现？
3. Vector Retrieval 单次耗时和 Rerank 是否测量过？
4. 如何评估召回结果与用户问题的匹配度？
5. Agent 包含哪些核心模块，ReAct 如何工作？
6. Agent Loop 通常多少 Step 能完成任务，达到 Max Step 仍未完成怎么办？
7. Tool 如何约定和约束调用参数？
8. Agent Streaming 是否使用 SSE，为什么？
9. Agent 编排里是否需要显式 Plan 阶段？

---

## S022 腾讯｜Agent 开发暑期实习｜一面｜2026-04-05 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/352203a181fc48d5ab172b6badd8148e

真人 / 第一人称证据：候选人以同岗暑期实习一面复盘发布并主动邀请同岗候选人交流，问题集中在真实项目中的模型失败、RAG 与 Agent Runtime。

高价值问题：

1. Agent 中模型输出失败可以分成哪些错误类型？
2. 不同 Failure Type 应如何 Retry / Fallback / Degrade？
3. RAG 如何构建 Vector Index，Chunk Size 如何权衡？
4. 为什么使用 Vector DB，与 MySQL / PostgreSQL 的职责如何区分？
5. Retrieval Recall 如何评估？
6. 如何检测并治理 LLM 输出死循环与重复内容？
7. Agent Architecture 如何支持 Tool 插拔与扩展？
8. Agent 与 LLM 本体的核心区别是什么？
9. MCP 解决什么工程问题？

---

## S023 腾讯｜后台 AI 开发暑期实习｜一面｜2026-04-27 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1b12310f0fad4594afb1df2fdcdb0738

真人 / 第一人称证据：作者以个人暑期实习一面分享发布，问题从实习 / 项目 / 论文连续进入 RAG、积分一致性、Redis Lock、Agent Framework、线程并发和 MQ，信息密度高。

高价值问题：

1. RAG 与传统搜索的区别是什么，为什么不直接关键词检索？
2. 检索效果从差到好做过哪些真实优化？
3. 积分等业务状态如何防止重复扣减 / 增加？
4. Redis 分布式锁、SETNX 与锁泄露如何处理？
5. Spring AI 的核心结构与 Agent 开发流程是什么？
6. Workflow Agent 中哪些步骤由模型决策，哪些应保持确定性？
7. 进程 / 线程、CAS、ThreadLocal 如何解释？
8. Kafka Partition 的意义是什么，为什么项目可能选择 RocketMQ？
9. Delay Queue 如何实现；如果不用 MQ，如何自己设计延迟任务？
10. MCP、Skills、Function Call 的边界是什么？

---

## S024 小鹏汽车｜AI 全栈产品研发培训生｜一面｜2026-09 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ff967cd4e7384b26b38823025297450b

真人 / 第一人称证据：作者明确记录 13 分钟飞书真人面试体验、问题顺序，并在 9 月 2 日更新结果为挂；内容围绕自己的 AI 项目和 RAG 能力展开。

高价值问题：

1. 在 AI 方向做过哪些真实项目和技术尝试？
2. 使用 LangChain 做过哪些具体工作？
3. 最擅长哪类 RAG 能力，完整实现链路是什么？
4. 大模型如何处理模糊 Intent？
5. RAG 有哪些文本 / 语义 Chunk Strategy？
6. 固定 Chunk 把强逻辑关系拆开会造成什么问题？
7. 如何缓解 Chunk 导致的语义丢失？
8. 如何理解“AI 全栈工程师”的职责边界？

---

## S025 京东｜后端 Agent 开发暑期实习｜一面｜2026-04-30 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c3342cd7584d4882acfa28fe875ef21d

真人 / 第一人称证据：候选人以个人暑期实习一面形式发布并写明“攒人品”，问题从金融 Agent 风险一路进入 Java 并发、Redis Lock、MySQL 大表优化。

高价值问题：

1. 金融系统为什么不能让 Agent 直接执行高风险真实操作，应如何设计确认与权限边界？
2. 高并发系统写代码时要考虑哪些问题？
3. ReentrantLock、HashMap 并发安全如何理解？
4. Redis 分布式锁与 SETNX 有哪些失败窗口？
5. MySQL 调优应看哪些层面，EXPLAIN 中关注哪些字段？
6. 5000 万行表如何做深分页？
7. 非聚簇索引、回表、联合索引在大表查询中如何影响执行成本？
8. 如果需要查询大量列，怎样从索引和 SQL 结构上继续优化？

---

## S026 美团｜Agent 开发｜一面｜面试 2026-08-23｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/1d067ce539c64d3988eabb9b646ef8a0

真人 / 第一人称证据：作者明确记录面试日期和收到失败通知后发布面经，问题从自身 Agent 项目沿着 RAG、Multi-Agent、State 和 Context 连续展开。

高价值问题：

1. Agent 项目整体架构如何设计，核心业务问题是什么？
2. RAG 从 Chunk、Embedding、Retrieval 到 Generation 如何实现？
3. Chunk Strategy 如何选择，不同方案如何影响召回和生成？
4. Multi-Agent 如何分配任务、并行执行并整合最终结果？
5. 多 Agent 并行时 State 如何管理？
6. Agent Context 如何治理，如何避免过长导致性能或效果下降？
7. 如何理解 Agent 与普通 LLM / Workflow 的边界？
8. 如果从零设计 Agent 应用，核心系统层如何拆分？

---

## S027 小红书｜Agent 开发｜一面｜面试 2026-08-12｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/f1ed02bfdae04730837753b62e0d58b9

真人 / 第一人称证据：作者明确记录自己正在转正和准备秋招、8 月 12 日面试、“吃饭秒约二面”，并留下对自己表达方式和面试内容的强烈个人复盘。

高价值问题：

1. 实习中的 Agent 具体用于什么业务，关注哪些量化指标？
2. OpenManus 使用什么框架，Harness 如何理解？
3. Multi-Agent 并发会产生哪些性能问题，如何限制并发量？
4. Long-term / Short-term Memory 底层如何实现？
5. ReAct、Planner、Executor、Critic 分别做什么，为什么选择该执行模式？
6. Context 如何拆分与管理？
7. Redis 常用数据结构及底层机制是什么？
8. 场景题：让 Agent 对广告投放策略持续自我迭代、选择并执行更优方案，系统如何设计？

---

## S028 小红书｜AI 应用开发工程师｜一面｜面试 2026-06-18｜HUMAN-A

来源：https://yuki-bloom.vercel.app/post/xiao-hong-shu-ai-ying-yong-kai-fa-gong-cheng-shi-mian-jing

交叉发布：https://www.nowcoder.com/feed/main/detail/e213986f66684723a1e108a61d77a9d6

真人 / 第一人称证据：候选人个人博客保留长期面试时间线和多家公司面经，正文明确记录 2026-06-18 16:00 面试、自己的快手实习项目以及面试官连续追问；牛客存在同一作者的交叉发布，可交叉核验。

高价值问题：

1. 一个 AI 项目到底节约了多少运营 / 研发成本，如何量化项目价值？
2. 自研 MCP 为什么存在，MCP 与传统 API 的区别是什么？
3. 在 MCP 之前，AI 调用外部能力通常如何实现？
4. Skill 与 MCP 的职责边界是什么？
5. AST Static Analysis 与 Sub-agent Isolation 如何组合？
6. 哪些场景真正需要多个 Sub-agent？
7. Workflow / 基础设施如何沉淀成可迁移的个人工程能力？
8. 如何理解 AI Application Engineer，而不只是“会调模型 API”？

---

## S029 阿里淘天｜AI Agent 开发｜二面｜2026-04-24 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/eba426555bf04cebb88b26d03b8d6e97

真人 / 第一人称证据：作者明确以个人“二面凉经”发布，写到“面完人都通透了”，问题围绕自己的两个实习项目、个人负责范围、Prompt 与业务数据连续深挖，并包含现场 Agent 场景设计。

高价值问题：

1. 大文本说明书有哪些 Chunk 方法，项目为何选择当前策略？
2. PDF、图片等异构文档如何解析、存储与检索？
3. 项目为什么采用当前 Retrieval / Ranking 方案？
4. 项目是否上线、每日访问量多少，如何验证方案真正有效？
5. 大量重复 / 相似 Query 如何缓存、聚合或复用答案以降低成本？
6. 标准 RAG 系统有哪些模块，用户 Query 的完整链路是什么？
7. 一个可靠 Prompt 应包含哪些部分，遵循度不好时如何调优？
8. 如果把现有业务重新设计为购物 Agent，应如何做能力编排和边界控制？

---

## S030 360｜Agent 开发｜社招二面｜2026-08-26 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c72671706e314ce08d3c371685d7f70b

真人 / 第一人称证据：作者明确记录“纯聊简历 1h”、面试官围绕自己项目持续追问，并在正文直接更新“过了”；属于典型真人社招项目深挖。

高价值问题：

1. 项目真实负责程度、QPS 和用户规模如何说明？
2. Agent Service 高可用如何保证？
3. 算法 / 模型能力如何工程化部署？
4. AI Sandbox 如何实现？
5. NFS 与 VPC 分别解决什么问题？
6. 多个 Pod 挂载同一存储时如何避免读写冲突？
7. 如何验证 AI 生成代码质量？
8. 单点依赖如何消除？
9. OpenSpec / Spec-driven Development 在 AI Coding 中解决什么问题？
10. AI 测试报告如何生成和验证？

---

## S031 多益网络｜AI 应用工程师｜一面｜面试 2026-08-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f5f1a4daff104fcb8c48476ed9c99f39

真人 / 第一人称证据：候选人给出公司、岗位、具体面试时间，并大量保留自己“没想过怎么验证 / 有点卡 / 临场编答案”等真实状态；正文包含完整面试感想和后续同岗轮次记录。

高价值问题：

1. 三级 Memory 架构如何实现，为什么这样分层？
2. 为什么项目需要 RAG，它解决了什么真实问题？
3. Memory 在 20 轮后“保留 90% 信息”这种指标如何定义和验证？
4. 团队规模、个人贡献与项目工作流如何证明？
5. 固定 Workflow 与 Agent Autonomy 如何平衡？
6. Multi-Agent 的协作触发、信息流转和失败点如何设计？
7. AI Coding 在项目中占多少比例，如何保证生成代码可验证？
8. Harness / Loop Engineering 最近有哪些值得关注的工程方向？
9. 内部代码使用 AI 时如何做模型隔离、权限与测试审查？

---

# 本轮明确排除

本轮搜索量显著扩大，但以下内容即使看起来“题很多”也没有进入正式 Batch：

- `含完整答案 / 三年面试五年模拟 / 高频题解析` 等二次整理；
- “帮粉丝复盘某厂面试”“陪跑营学员拿 Offer”但作者不是候选人本人的内容；
- CSDN / 知乎 / 视频平台中以领取资料、课程导流、标准答案为主体的文章；
- 只能通过搜索标题看到、但原正文无法稳定打开的小红书 / 抖音线索；
- 只有 1～3 个泛问题、缺少真人现场和连续追问的低密度第一人称；
- 岗位实际上属于传统后端、纯算法训练或普通数据分析，只因候选人简历里有 Agent 项目而被问几句 AI 的场次。

# Batch 02 观察

这批重新验证了一个重要事实：**13 个并不是市场上的供给上限，而只是清洗后的初始基线。** 通过扩大检索入口、使用搜索索引补足登录态限制、沿企业页 / 话题页回溯原帖，以及交叉验证候选人个人博客，可以在不降低 HUMAN-A 标准的情况下继续找到大量合格来源。

本批新增 `S014–S031` 共 **18 个 HUMAN-A 来源**，当前干净核心样本达到 **31 个**。

问题分布仍然覆盖整条路线：

```text
Python / Java / OS / Network
        ↓
MySQL / Redis / MQ / Concurrency
        ↓
Vector DB / RAG
        ↓
LLM Foundation / Context
        ↓
Agent / Harness / Tool / MCP / Skill
        ↓
Production / Security / Evaluation / System Design
```

因此后续应该继续扩量，而不是把严格标准误解为“只能留下十几篇”。