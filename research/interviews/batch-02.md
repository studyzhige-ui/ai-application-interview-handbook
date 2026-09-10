# Batch 02 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **18** 个正式来源。

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

## S015 百度｜Coding Agent / Agent 开发｜秋招一面 + 二面 + 三面｜2026-08-18 / 08-21 / 08-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b9521e2b51e04afeac0a3a32e13f4da9

真人 / 第一人称证据：作者完整记录三轮 Coding Agent 面试，明确一面结束后电话秒约二面、二面自评一般、三面因 408 / OS 基础发挥差且一周后被横向淘汰；每轮都保留面试官追问、候选人现场状态和连续技术链。

高价值问题：

1. Python 与 Java 做 Agent 工程时的差异在哪里？
2. Agent 整体架构、ReAct、Tool Calling、Context 和 System Prompt 分别如何设计？
3. Agent Workflow 某个场景线上出错时，如何定位和恢复？
4. 如果从零设计 Claude Code / Codex 类 Coding Agent，应拆哪些核心模块？
5. 两个相似 Skill 容易误选时，如何做 Skill Selection 与错误恢复？
6. Skill 从匹配、动态参数适配到执行的完整生命周期是什么？
7. 多任务之间如何隔离 Context，页面结构变化导致 Skill 失效时如何治理？
8. Agent 并发为什么要受控，如何避免执行过程中泄露密钥或敏感数据？
9. HTTPS / URL 到页面完整链路与 Agent Backend 的安全边界如何解释？
10. 三面继续追进程 / 线程 / 协程、上下文切换、虚拟内存、缺页、页面置换等 OS 基础。
11. Coding：访问日志最近访问排序、多线程交替打印且线程退出不能永久阻塞、最长有效括号。

---

## S016 字节跳动｜Agent 开发｜日常实习一面｜发布 2026-09-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d2cf5165d1184b59879eff5793b7b453

真人 / 第一人称证据：作者围绕本人 Coding Agent / Business Agent 项目复盘，问题连续追 Context Token、Compaction Prompt、Skill Loading、Sub-agent，再落到 OS、MySQL、Linux 和 Coding。

高价值问题：

1. Business Agent 的 Prompt 怎样设计？
2. Coding Agent Session 怎样组织？
3. Context Token 怎样计算，什么时候触发 Compaction？
4. Compaction Prompt 怎样写，如何验证模型真的完成了有效压缩？
5. Skill 怎样管理与按需加载？
6. 什么场景使用 Sub-agent，Single / Multi-Agent 怎样取舍？
7. Process 与 Thread 的区别是什么？
8. URL 请求到页面的完整链路是什么？
9. MySQL 怎样做 Duplicate Removal，`ROW_NUMBER` 等方法如何使用？
10. Linux 怎样查 Process / Port？
11. Array / List / Hash Collision 等基础结构怎样理解？
12. Coding：按类型合并 Nested JSON。

---

## S017 字节跳动｜AI Agent 日常实习｜一面 + 二面｜2026-08-13 / 08-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8a553bb6ea8445d0b0abe11e87614cea

真人 / 第一人称证据：作者明确记录 8 月 13 日一面、8 月 16 日二面，并以本人日常实习 Agent 方向流程持续更新；问题围绕其 Coding Agent 深入到 Compaction、Memory、MCP、Tool Result 和 Multi-Agent 冲突。

高价值问题：

1. Coding Agent 的核心架构是什么，ReAct 与 Plan 模式怎样选择？
2. Context 超窗时如何做 Compaction，哪些信息必须保留？
3. 压缩后如何确保没有忘掉用户初始需求和关键约束？
4. Agent 在两个执行路径之间来回震荡的原因是什么，怎样检测和终止？
5. Context 与 Long-term Memory 的边界是什么，Memory 如何提取、存储和召回？
6. 为什么 Memory Extraction / Compaction 可以使用较小模型，风险在哪里？
7. MCP Tool Call 的完整流程是什么，Tool 描述太多时如何做选择？
8. Tool Result 太大时如何处理，既省 Token 又不丢任务关键事实？
9. Multi-Agent 如何分工和通信，多个 Agent 修改同一文件怎样避免冲突？
10. Prompt Cache 怎样提高命中率并降低重复上下文成本？

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

## S021 腾讯｜Agent 开发｜实习一面｜发布 2026-03-30｜HUMAN-A

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

## S022 腾讯｜Agent 开发｜暑期实习一面｜发布 2026-04-05｜HUMAN-A

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

## S024 小鹏汽车｜AI 全栈产品研发培训生｜一面 13min｜发布 / 更新 2026-09-02，已挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ff967cd4e7384b26b38823025297450b

真人 / 第一人称证据：与 `S012` 为同一真实候选人，但小鹏是完全独立的公司招聘流程。作者明确记录飞书面试只有约 13 分钟、无法确认对方是否开摄像头、体验一般，并于 9/2 更新已挂；问题集中在本人 LangChain / RAG 能力和“Chunk 切断逻辑关系”的具体失败场景。

高价值问题：

1. AI 方向做过哪些真实项目 / 技术尝试，个人最擅长哪一块？
2. LangChain 在项目里具体做了什么，而不是只调用过哪些 API？
3. RAG 的完整实现链路是什么？
4. LLM 如何处理模糊 Intent Recognition，其工程机制怎样理解？
5. RAG 常见 Text / Semantic Chunking 方式有哪些？
6. Fixed Chunk 把强逻辑关系切到不同块时会产生什么问题？
7. 例如“A 是 B 的充分必要条件”恰好被切开，Retrieval / Generation 是否还能保持逻辑完整？
8. 如何通过 Parent-child Chunk、Overlap、Semantic Chunking、Metadata / Neighbor Expansion 等方式修复 Context / Semantic Loss？
9. 怎样理解 AI Full-stack Engineer，前端 / Backend / Model / Agent 的边界怎样协作？

去重：同作者 `S012` 为启云方流程，本场是小鹏独立招聘流程；URL、公司、日期和“充分必要条件被 Chunk 切断”场景均未在旧库命中。

---

## S025 京东｜后端 Agent 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c3342cd7584d4882acfa28fe875ef21d

真人 / 第一人称证据：作者以本人后端 Agent 一面发布并“攒人品”；问题明确从金融 Agent 的高风险执行边界切入，再追 Java Concurrency、Redis Lock、MySQL 大表和 Agent Hallucination Production 化。

高价值问题：

1. 金融系统为什么不能让 Agent 自主执行真实资金操作，怎样设计 Human Approval / Permission Boundary？
2. 高并发服务写代码时要考虑哪些 Race / Lock / Resource 问题？
3. ReentrantLock 的底层机制是什么，Concurrent HashMap 为什么不能直接用普通 HashMap 替代？
4. Redis 在 Agent Backend 中适合承担哪些职责？
5. 用 SETNX 做 Distributed Lock 有哪些正确性问题？
6. MySQL Tuning 应从哪些维度排查，`EXPLAIN` 重点看什么？
7. 5000 万行表如何做 Deep Pagination，Back-to-table 如何降低？
8. Composite Index 只给部分条件时 SQL 怎样执行？
9. 需要读取很多列时，Covering Index 不再成立后怎样继续优化？
10. LLM Hallucination 是否意味着 Agent 无法工程落地，系统层应该怎样约束？

---

## S026 美团｜Agent 开发｜一面｜面试 2026-08-23，08-25 通知未通过｜HUMAN-A

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

## S027 小红书｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-12 / 08-17，发布 09-02｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/f1ed02bfdae04730837753b62e0d58b9

二面来源：https://www.nowcoder.com/feed/main/detail/9f7361c709f4413396988b4f334a0d6f

真人 / 第一人称证据：两篇均由同一作者发布，作者展示身份与项目时间线一致。一面作者写自己第一次正式面 Agent、几乎没准备，晚饭后即收到二面邀请；二面明确面试时间 8 月 17 日，记录“被问得很凶”、面试官技术很强、自己复盘感觉一般，但仍被约三面。属于同一候选人同一小红书 Agent 秋招流程，因此合并为一个来源。

高价值问题：

1. 实习项目真正关注哪些业务 / 技术指标，数字如何获得、上下游和代码框架是什么？
2. Agent 在真实项目中到底用在哪里，而不是简历上只写一个框架名？
3. OpenManus 使用什么框架，怎样理解 Agent Harness？
4. Multi-Agent 并发会带来哪些资源竞争问题，如何限制并发量并隔离 Context / State？
5. Long-term / Short-term Memory 的底层实现方式是什么？
6. ReAct 与 Planner / Executor / Critic 的关系是什么，为什么当前项目不用另一种模式？
7. 二面继续追：实习 Agent 从输入到结果的完整架构与数据流是什么，结构化结论如何产生并校验？
8. 为什么选择 OpenManus，而不是 LangGraph 做编排？Workflow 与自主 Agent 的边界是什么？
9. Prompt Injection 如何泄露 System Prompt 或绕过指令，怎样建立防护边界？
10. Tool Call 如果没有次数 / 权限限制会带来哪些风险，怎样做 Permission、Quota 与高风险操作确认？
11. 如果把现有单 Agent 改成 Multi-Agent，会新增哪些冲突、共享资源和状态一致性风险？
12. System Design：本地 Agent + 云端 Agent 需要服务大量设备时，怎样做任务路由、状态同步与安全边界？

去重：一面与二面由同一作者、同公司、同岗位且招聘时间线连续，二面主动合并回 `S027`，不新增来源数量；与现有小红书其它候选人的题序、项目和作者均不同。

---

## S028 小红书｜AI 应用开发工程师｜技术面｜面试 2026-06-18 16:00｜HUMAN-A

来源：https://yuki-bloom.vercel.app/post/xiao-hong-shu-ai-ying-yong-kai-fa-gong-cheng-shi-mian-jing

交叉发现页：https://www.nowcoder.com/feed/main/detail/e213986f66684723a1e108a61d77a9d6

真人 / 第一人称证据：来源是候选人的个人博客原文，页面公开其 2026 年快手 / 百度 / Bilibili 等实习时间线，并给出小红书 AI 应用面试的精确时间；正文围绕本人快手实习、自研 MCP、业务量化、Skill / Sub-Agent 逐层追问，牛客页只用于回溯到原始博客。

高价值问题：

1. 快手实习中的低代码平台究竟节约多少运营 / 研发人力，指标如何量化？
2. 自研 MCP 的目标和架构是什么？
3. MCP 与传统 API 的边界是什么？
4. MCP 之前 LLM / Agent 是怎样调用外部工具的？
5. “降低产研沟通与代码维护成本”如何定义并用数据证明？
6. 为什么要做某项需求，怎样从“接需求”升级到判断业务价值？
7. Skill 与 MCP 有什么区别？
8. AST Static Analysis 与 Sub-Agent Isolation 如何配合？
9. 什么场景值得引入多个 Sub-Agent？
10. 公司已有 Workflow / Infrastructure 离开内部环境后，如何抽象成可迁移的方法和个人工具链？
11. AI Application Engineer 与传统前端 / 后端的职责差异是什么？

---

# 本轮明确排除 / 去重

Batch 09 搜索量继续扩大，但以下内容保持 **零贡献**：

- WeThinkIn / RockyDing、“三年面试五年模拟”、面灵 AI、卡码笔记、CSDN / 51CTO / 2048AI 等题库、答案、整理、路线或 SEO 内容；即使它们引用真实面经，也只能用来回溯候选人原帖，不能直接贡献问题；
- 同一份“5 年经验大模型应用开发、多家公司面试”在 CSDN、51CTO、AtomGit、财经站等处的大量跨站转载；
- “林小白zii”一类按公司聚合几十场面经的合集账号 / 汇总帖，只作索引，不作为候选人本人场次；
- 带“思路参考 / 完整答案 / 真题解析”的二次内容；
- 只有标准化问题列表、缺少面试日期 / 轮次 / 状态 / 互动等现场证据的帖子；
- AI 自动面试 / 模拟面试；
- 普通后端岗位仅因标题或一两个问题带 AI / Agent 字样，但无法证明实际 Role Scope 的场次；
- 同一候选人的字节 AI 全栈 9/1 一面与 9/8 二面合并为 S161，一个流程只计一次；
- 字节 Agent 后端 S164 存在题序高度相似的另一版本，只保留有明确二面与横向淘汰结果的来源；
- 同花顺 S166 / S167 经企业页核验为不同账号 / 学校的两位独立候选人，因此不错误合并；
- 小红书 S028 优先保留作者个人博客原文，牛客同步页只作为跨平台回溯证据。

# Batch 09 观察

本批新增 `S015–S028` 共 **28 个 HUMAN-A 来源**，当前干净核心样本达到 **196 个**。

本轮最值得记录的信号：

1. **泛搜索重复率继续上升，但精确搜索仍有显著新增，尚不能停止。** 泛关键词越来越容易返回前八批已收录样本、答案版和聚合页；但企业页 / 话题页 + 公司 / 岗位 / 月份 / 轮次精确搜索仍然一次新增 28 个 HUMAN-A。
2. **完整招聘流程的价值明显高于单篇题单。** 百度 Coding Agent 三轮、字节 AI 全栈一二面等来源让我们能看到问题从项目 / Agent 到 OS / Backend / Coding 随轮次怎样加深；同流程必须合并计数，但轮次内容全部保留。
3. **Coding Agent / Agent Runtime 已稳定进入“可控软件执行系统”层。** Skill Mis-selection、Dynamic Args、Context Isolation、Container Restart Resume、Secret / Sensitive Data Boundary、Sub-agent Token Accounting、Loop Oscillation、Compaction、Prompt Cache 等均有真人独立命中。
4. **AI Backend Foundation 继续被目标岗位直接确认。** MySQL MVCC / Index / Deep Pagination、Redis Lock / Cache / HotKey、MQ Reliability、TCP / HTTPS、Go Context、Java Lock / ThreadPool 等不是传统后端样本混入，而是 AI Backend / Agent Backend 同场真实考察。
5. **项目价值量化成为强验真信号。** 面试官越来越追 QPS、DAU、Cache Hit Rate、节省人力、准确率、Latency、Cost、失败案例与本人贡献，而不是只接受“用了 LangChain / RAG / MCP”。
6. **跨平台原帖回溯有实际收益。** 本轮通过搜索索引找到 Yuki 个人博客的原始小红书 AI 应用面经，证明牛客之外仍有稳定可验证的 HUMAN-A；与此同时，CSDN / 51CTO 等搜索结果大部分仍是转载和营销内容，不能为了平台覆盖率降低门槛。
7. **去重已经必须依赖作者身份与时间线。** 同公司同日并不意味着同一候选人（同花顺一面 / 二面即为不同账号）；相反，同作者跨多个 URL 的同一招聘流程应合并。后续继续坚持 URL + 题序 / 项目语义 + 作者流程三层去重。

停止条件不变：只有连续多轮跨公司、岗位、月份、轮次和平台扩大 Recall 后，**新增 HUMAN-A 的绝对数量与占比都持续接近零**，连精确公司 / 轮次 / 作者页搜索也难以找到新来源，同时新增问题模块和追问深度稳定收敛，才进入最终收尾。Batch 09 的重复率确实继续升高，但一次仍新增 28 个独立 HUMAN-A，因此当前仍明显未达到停止点。

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

## S031 多益网络｜AI 应用工程师｜一面 + 三面（同一候选人同流程合并）｜2026-08-20 / 08-28｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/f5f1a4daff104fcb8c48476ed9c99f39

三面来源：https://www.nowcoder.com/discuss/922801355649974272

真人 / 第一人称证据：两个页面由同一作者发布，三面正文明确链接一面为“前传”，因此按同一候选人同一招聘流程合并为一个来源。一面保留自己项目细节编得不扎实、没听清追问等状态；三面记录约 50 分钟、RAG 回答到一半被面试官切题、Coding 因边界条件导致死循环、面后自评以及评论区其他候选人的流程核验。

高价值问题：

1. 三级 Memory 如何实现，为什么能声称 20 轮后仍保留 90% 信息，怎样验证这个指标？
2. 为什么项目需要 RAG，它在完整用户请求链路中解决什么问题？
3. 项目真实团队如何分工，候选人本人负责哪些部分，项目指标是否真实？
4. Multi-Agent 项目为什么要做，协作触发和信息流转如何设计？
5. AI Coding 在项目中的实际编码占比与使用方式是什么，怎样做人工验证？
6. 三面深挖 `Router / WorkList / InvocationQueue / Session` 分别存什么、一次输入怎样流转？
7. Context Compression 策略怎样设计；把当前 Agent 架构做成分布式后要改哪些状态边界？
8. `InvocationQueue` 如何保证执行过程中信息不丢失？
9. 主流 Agent Architecture、RAG Dense / Sparse Retrieval 的作用与组合方式是什么？
10. MySQL Index 类型及优缺点、多线程与多进程怎样理解？
11. 给一个新功能，如何让 AI 参与需求、实现、测试与人工验收，而不是只生成代码？
12. Coding：合并有序数组；现场实现出现死循环时如何快速定位边界条件。

去重：一面与三面明确同作者 / 同岗位 / 同流程，主动合并，不拆成两个 HUMAN-A；两条 URL 均未在 `S001–S006` 收录。
