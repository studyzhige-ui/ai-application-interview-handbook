# Batch 14 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S277` 继续编号，仍只接受：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场痕迹 + AI Application / Agent 目标岗位 + 正文稳定可核验 + 非转载 / 非合集 / 非重复 = HUMAN-A**。
>
> 本轮继续同时追 2026-09 最新内容与 2026-03～08 历史缺口，并沿作者主页补同候选人的后续轮次。搜索摘要只用于发现；正文、作者和招聘流程不能稳定核验的结果继续零贡献。
>
> 通过 Role Scope 后保留整场真实问题。Agent / RAG / Harness 与 Python / Java、MySQL、Redis、MQ、Network、Concurrency、Frontend、Coding、Security、Evaluation、AI Coding、System Design 一视同仁。
>
> 去重固定执行：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。同候选人同公司同流程多轮合并为一个 `Sxxx`；同一候选人面不同公司属于独立招聘流程，可以分别计数。

---

## S277 名创优品｜Agent 开发实习｜一面｜发布 2026-08-26，已通过｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f844a4ac20be44bc9b3f756bd0ebb84c

真人 / 第一人称证据：作者主页是连续的本人实习 / 秋招时间线，身份、学校和 Agent 实习背景一致；本帖记录名创优品 Agent 一面并在面后更新“已过，等待后续测评和流程”，问题围绕本人自动拆题 / Agent 项目连续追问，不是内容账号式题单。

高价值问题：

1. 自动拆题为什么把 OCR、COA、可用性检查拆成不同 Subgraph，边界如何确定？
2. Subgraph 与 Main Graph 之间怎样传递 State，如何避免状态污染？
3. 外部任务已经成功，但服务在写 Checkpoint 前崩溃，恢复后如何避免重复提交副作用？
4. Skill 的 Bad Case / Memory 如何避免被错误反馈或 Prompt 污染？
5. ReAct 与 Plan-and-Solve 在同一 Agent 中怎样分工？
6. Multi-Agent Context 丢失时如何定位，Workflow Orchestration 与自主 Multi-Agent 怎样取舍？
7. Agent 间传大数据 / 大订单时如何做 Message Passing，哪些数据不应直接塞进 Context？
8. Token 因循环调用快速膨胀时，怎样检测并阻断异常 Loop？
9. ReAct 执行方向偏离目标后，如何把 Agent 拉回原任务？
10. Tool Result 很大时怎样压缩，同时保留关键信息并处理 Permission / Injection / Validation？
11. 如何理解 DeepSeek Harness；Claude Code / Codex 在真实开发中怎样使用？

去重：URL 未在 `S001–S276` 出现；独特的“外部副作用已成功 + Checkpoint 前崩溃”恢复题序、作者与名创流程均未在正式来源命中。

---

## S278 深信服｜Agent 开发实习生｜一面 + 二面（同一候选人同流程合并）｜发布 2026-09-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/14b2c379ae434062a009aefea9fc5df9

真人 / 第一人称证据：与 `S277` 为同一真实候选人，但属于不同公司独立招聘流程。本帖完整记录深信服一面、二面及面后 HR 时间线：面试官介绍 AI Agent 平台 / Harness 工程方向，作者随后被告知通过、等待 HR，之后又收到感谢信，现场与结果链路完整。

高价值问题：

1. 实习中跨团队接口协作真正遇到过什么问题，如何解决？
2. Agent Tool / API 数量越来越多时，当前架构暴露了什么问题？
3. Agent 效果与准确率怎样 Evaluation，谁构建数据集？
4. 自动拆题 Agent 从业务输入到输出的完整技术链路是什么？
5. 公司在 Production 中如何使用 AI Coding，怎样保证生成代码质量？
6. 二面继续追：项目最核心、最有业务价值的工作是什么？
7. Dynamic Tool Registry 怎样设计；动态注入与 MCP / LangChain Tool / Skill 有何边界？
8. 当 Tool 超过 100 个时，模型怎样发现正确 API，是否需要 Tool Retrieval / Lazy Loading？
9. 目标 Tool 临时不可用时，Agent 如何 Fallback 或向用户暴露失败？
10. Tool Registry 的 Schema / Metadata / Version / Permission 管理难点是什么？
11. Multi-Agent 架构与 AutoGen / CrewAI 等方案如何比较？
12. Coding：最长无重复子串。

去重：同作者不同公司流程，不能与 `S277` 合并；一面与二面属于同公司连续流程，因此合并为一个 `Sxxx`。URL、题序与既有深信服样本均不构成同场重复。

---

## S279 九号公司｜Agent 开发实习｜一面｜发布 2026-08-31，约 90min，已 OC｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c0b53fdd38e041d2bc779753d04ee2ce

真人 / 第一人称证据：作者与 `S277 / S278` 同属一个可核验候选人时间线，但九号是独立公司流程。作者记录约 90 分钟面试、项目深挖和当前 OC 状态，面试官不断追问真实业务指标、团队分工与失败案例，现场结构明显区别于标准题单。

高价值问题：

1. 实习 Agent 的真实业务目标、上下游、团队分工和本人职责是什么？
2. LangGraph 自动拆题里每个 Node 的输入 / 输出和完整数据流是什么？
3. 项目宣称提高效率，具体提升了多少、怎样测，原先人工痛点是什么？
4. OCR 批处理失败时怎样恢复，识别质量怎样优化？
5. 候选人本人是否参与数据清洗 / 模型训练，项目边界在哪里？
6. 电商 Agent 如何做订单自动处理和任务编排？
7. “准确率 90%+”的数据来源是什么，剩余 10% 是哪些 Failure Case？
8. Tool Registry 为什么拆接口 / 能力 / 实现层，Dynamic Loading 怎样工作？
9. 长任务如何形成闭环并把反馈 / 交付状态返回给用户？
10. PI Agent、DeepSeek Harness 分别怎样理解；Agent 岗为什么仍强调工程能力？

去重：URL 与九号公司招聘流程未在旧 Batch 出现；同作者其它公司面试属于独立流程，分别计数。

---

## S280 字节跳动中国交易与广告｜AI 应用开发｜一面｜面试 2026-08-27，约 90min，后续未通过｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b34f6902e8544fe2953696ed52e49dba

真人 / 第一人称证据：候选人明确记录 8 月 27 日、约 1.5 小时一面和一周后未通过结果；问题从 Agent Runtime 直接进入 Java / Redis / MQ / NIO / 配置中心与现场 Coding，是“目标 AI 岗完整工程能力”非常典型的真人样本。

高价值问题：

1. 一个最小 Agent Loop 怎样实现，ReAct 在循环里承担什么作用？
2. Long-running Agent 任务如何 Cancel，是否真正实现 / 测过取消？
3. Agent Message 有哪些类型，Short-term / Long-term Memory 与 Context Window 怎样配合？
4. ThreadLocal 为什么可能发生泄漏，在线程池环境下怎样治理？
5. Redis Distributed Lock 怎样续期，异常退出时如何保证锁最终释放？
6. RocketMQ Delayed Message 如何实现，还有哪些延迟任务方案？
7. Redis 高 QPS 下线程模型怎样工作，什么时候瓶颈不在 Redis 本身？
8. IO Multiplexing、NIO、Reactor 的关系是什么？
9. Configuration Center 多来源优先级、动态刷新、Listener 失败与中心宕机 Fallback 怎样设计？
10. SQL：求各部门最高薪员工。
11. Coding：Trapping Rain Water II；设计 Keyed Executor，使同 Key 串行、不同 Key 并行且线程安全。

去重：URL、日期和“Agent Cancel → Redis/MQ/NIO/Config Center → Keyed Executor”的题序均未在正式来源命中。

---

## S281 阿里｜Agent 开发暑期实习｜一面｜发布 2026-08-05，已 GG｜HUMAN-A

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

去重：URL 未在 `S001–S276` 收录；项目链与现有阿里 / 淘天 / 阿里云 Agent 来源不属于同一候选流程。

---

## S282 字节跳动｜AI 应用开发｜一面 + 二面（同一候选人同流程合并）｜2026-05-12 / 05-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/61aa7e8d56ca4eb4a5a873512a72d616

真人 / 第一人称证据：作者记录 5 月 7 日 HR 联系、5 月 12 日一面、约半小时后约二面、5 月 15 日二面以及最终未通过但被其它部门捞起的时间线；二面多次记录自己没有答到点、指标被追问住和 Coding Bug，现场痕迹很强。

高价值问题：

1. 过去字节实习中数据库做过哪些优化，真实数据量和 Sharding 方案是什么？
2. MySQL Index Invalid / Slow Query 常见原因是什么，B+Tree 为什么适合数据库？
3. Redis Sentinel、Cluster、Master-Slave 分别解决什么问题？
4. AI / Vibe Coding 在真实研发中怎样使用，Skill 有什么价值？
5. 二面继续追：项目真正服务谁、业务价值是什么、性能指标怎么来的？
6. 候选人认为最难的工作是什么，为什么面试官认为“还不够难”？
7. “数据库性能提升 20%”具体怎样测；基线、压测环境和指标是什么？
8. Back-to-table 为什么可能引入 Random IO，怎样通过索引设计减少？
9. Coding：实现 Bounded Blocking Queue，并现场讨论实现中的并发 / 边界 Bug。
10. 为什么自己做 AI Assistant，而不是直接使用已有工具？

去重：同作者同公司的一、二面按时间线合并；URL 与独特“性能提升 20% 如何测”追问未在旧来源出现。

---

## S283 字节跳动｜AI 应用开发｜联合技术面（两位面试官）｜发布 2026-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c5947496fc29440883611173478dc257

真人 / 第一人称证据：候选人说明为加快流程，两位原本不同轮次的面试官一起进入同一场面试，并在评论中解释是 HR 安排；作者还说明自己没有录音、只能凭记忆复盘，因此部分问题未完整记录，具有自然现场痕迹。

高价值问题：

1. DAG Agent Orchestration 如何设计，每个 Agent / Node 分别负责什么？
2. LangGraph 在该架构里承担什么 State / Flow 职责？
3. Agent / RAG Evaluation 怎样设计 Dataset 与指标？
4. Semantic Chunking 相比固定切分有什么收益和代价？
5. Fine-tuning / RL 在 AI Application 岗应掌握到什么边界？
6. HNSW 基本原理和检索 Trade-off 是什么？
7. 多文件并发处理时如何组织任务、状态与失败恢复？
8. ThreadLocal 的使用场景与风险是什么？
9. LangChain Checkpoint 能保存什么，恢复语义是什么？
10. 如何理解 Agent Harness？
11. Coding：Ugly Number 等现场实现。

去重：URL 未入库；联合面试流程与现有字节样本作者、项目和题序均不同。

---

## S284 Bilibili｜Agent 开发｜一面 + 二面（同一候选人同流程合并）｜2026-08-11 / 08-13｜HUMAN-A

一面来源：https://www.nowcoder.com/discuss/919630453387063296

二面来源：https://www.nowcoder.com/discuss/919630524673458176

真人 / 第一人称证据：两篇由同一作者、同一身份连续发布；一面 8 月 11 日约 45 分钟，二面 8 月 13 日约 45 分钟。作者分别记录面试官风格、自身压力、对结果的判断和二面反馈，因此按同一招聘流程合并为一个来源。

高价值问题：

1. 个人 Agent 项目为什么能被连续深挖 30 分钟以上，真正核心实现是什么？
2. Agent Service 如何部署到 Cloud，容器资源怎样用 cGroup 限制？
3. A2A 在什么场景适合 Agent-to-Agent 通信？
4. CI/CD 如何支撑 Agent 服务迭代？
5. Context Compaction 策略怎样设计，哪些信息不能被压掉？
6. 二面继续追：实习中最难的工程问题是什么？
7. Load Balancing 在 Agent Backend 中怎样做？
8. 不同 Agent System 的 Memory 机制有什么差异，什么值得自己实现？
9. 从零自研 Agent 与基于已有框架的边界是什么？
10. 如何验证 Agent 的非确定性输出，Hooks 能承担哪些验证工作？
11. Bad Case 应按哪些维度分类和回归？Workflow 与完整 Agent 怎么选？
12. Coding：Merge Intervals。

去重：一、二面同作者、同岗位且日期连续，合并一个 `Sxxx`；两条 URL 均未在 `S001–S276` 出现。

---

## S285 淘天｜AI 应用开发｜一面｜发布 2026-04-16｜HUMAN-A

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

## S286 阿里云｜Agent 开发｜一面｜面试 / 发布 2026-08-18，面后即挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/42ba29ab006d4bb793112eb263d18f6a

真人 / 第一人称证据：作者明确写自己是被捞到 Agent 开发、此前没有专门准备，因此整场几乎全是 Agent；同时记录这是秋招第七场、第五次失败，面完很快挂，招聘与候选人状态非常明确。

高价值问题：

1. 平时如何使用 AI Coding，哪些环节仍由人验证？
2. Skill 是什么，内部通常由哪些文件 / Metadata / Script / Resource 组成？
3. 是否真正写过自己的 Skill，加载与选择过程怎样实现？
4. 最近关注哪些 Agent 产品 / 工程方案？
5. Claude Code 与 DeepSeek Harness 的结构有什么差异？
6. 是否读过相关源码，Harness 最关键的能力边界是什么？
7. Tool Calling 有哪些形态，Agent 怎样按需选择而不是把所有工具都塞进 Prompt？
8. 为什么需要 Sub-agent，什么任务值得拆分？
9. Agent 之间如何通信、同步任务状态？
10. 如果从零设计 Agent Loop，会包含哪些核心控制机制？
11. 现场 AI Coding：使用 AI 完成指定开发任务并解释结果。

去重：URL 和作者时间线未在 `S001–S276` 命中；与已有阿里云 Agent 来源为不同候选人独立场次。

---

## S287 字节跳动中国交易与广告｜AI / Agent 应用方向｜一面 + 二面 + 三面（同一候选人同流程合并）｜2026-06-17 / 06-22 / 06-24，07-01 书面 Offer｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/ccba40c7281f4d9197b01fe9c140b13d

二面来源：https://www.nowcoder.com/feed/main/detail/3d3475963ac647c0ae7f43da487248ad

三面来源：https://www.nowcoder.com/feed/main/detail/7274018294c84a118e0854e64ea580aa

真人 / 第一人称证据：作者主页能完整串起 6/5 投递、6/17 一面、6/22 二面、6/24 三面、6/29 HR、7/1 书面 Offer / 背调；目前身份也显示字节后端实习。三轮都保留候选人被提示、回答被面试官否定、流程推进等现场细节，因此合并为一个高置信招聘流程来源。

高价值问题：

1. 自研 Agent 与 Claude Code / Codex / Hermes 的差异是什么，为什么要自己做？
2. Harness 的核心设计选择是什么，Tool Selection 怎样实现？
3. Tool 与 Skill 有何区别；Skill 的 `references / scripts / assets` 在什么时候 Lazy Load？
4. 三级 Memory 如何分层，Context Assembly / Compression / Checkpoint 怎样协作？
5. Tool 失败或反复失败时，Agent 如何停止 Loop 并 Recovery？
6. 候选人的 Agent 到底是自己写的还是 AI 生成的，怎样证明本人理解代码？
7. SSE 为什么适合当前 Streaming 场景，为什么不用 WebSocket？
8. RAG 与 Skill / MCP / Tool / Function Calling 的边界分别是什么？
9. Automated Evaluation System 怎样设计？
10. Java Thread / ThreadPool、HashMap / ConcurrentHashMap / ThreadLocal 怎样在项目语境里解释？
11. Redis + Lua 怎样完成库存预占；数据库索引、DB / Cache Consistency、HotKey Expiry 怎样治理？
12. 三面 System Design：世界杯预测系统、餐厅位置 / 检索系统如何拆需求、数据和服务？
13. 项目声称“结果导向”时，用什么指标证明；如果面试官认为指标不成立，如何重新定义 Evaluation？
14. Coding：数组平方去重计数、2 的幂、最长无重复子串等，部分题需要面试官提示。

去重：三条 URL 同作者、同业务线、同招聘时间线，合并一个 `Sxxx`；URL 与该完整 OC 流程此前未正式入库。

---

## S288 字节跳动｜Agent 开发｜一面 + 二面（同一候选人同流程合并）｜2026-06-17 / 06-23｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/075c06bf50a143a785c039f9951624f6

二面来源：https://www.nowcoder.com/feed/main/detail/675f834ce9fa4a29b2c413d87241e6bb

真人 / 第一人称证据：作者 `Ariasu` 主页只有两篇面经，正好是同一字节 Agent 流程的一面与二面，日期连续、学校和身份一致，评论区还核验了轮次间隔。比批量内容账号具有更强招聘时间线证据，因此两轮合并计一个来源。

高价值问题：

1. Claude Code 与 Codex 的主要 Agent Engineering 差异是什么？
2. Coding Agent Prompt / Context 由哪些部分构成？
3. Context Compression 为什么分层，触发阈值怎样设？
4. 如何检测 Over-compression，压掉关键约束后怎样恢复？
5. 用户中途修改原任务时，旧 Context / Checkpoint 怎样处理？
6. Tool 与 Skill 的边界是什么；Skill 怎样设计、匹配和统计使用效果？
7. Complex Task Planning 与 Multi-Agent Orchestration 如何协作？
8. Sub-agent 是否共享 Tool / Context，如何隔离？
9. RAG 文档清洗、PDF Extraction、Incremental Update 与文档冲突 / Version Control 怎样处理？
10. 二面继续追 Skill 分层 / 匹配 / 累积，Short-term / Long-term Memory 与 Static / Dynamic Memory 的边界。
11. Memory 不断增长时如何控制存储与 Recall；Compression Threshold 与 Token Cost 如何权衡？
12. GraphRAG 与普通 Vector Retrieval 在 Multi-hop 场景有何差别？
13. Coding：0/1 Grid Path。

去重：两条 URL 同作者同公司同流程，主动合并；均未在旧 Batch 命中。

---

## S289 小红书｜AI 应用开发工程师｜技术面｜发布 2026-06-18｜HUMAN-A

来源：https://yuki-bloom.vercel.app/post/xiao-hong-shu-ai-ying-yong-kai-fa-gong-cheng-shi-mian-jing

同步页：https://www.nowcoder.com/feed/main/detail/e213986f66684723a1e108a61d77a9d6

真人 / 第一人称证据：优先保留作者个人博客原文而非同步页。作者博客有连续实习 / 求职时间线，并将本场明确写为本人小红书 AI 应用开发面试；正文前半是现场问题，后半另有作者自己的复盘 / 学习扩展。本研究只抽取能够确认真实问到的问题，不把后续教学反思伪装成面试官追问。

高价值问题：

1. 实习项目中本人具体负责什么，为什么值得做？
2. Low-code / AI Platform 到底节约了多少人力成本，数据怎么来的？
3. 是否真正负责过 MCP 相关能力，具体实现是什么？
4. MCP 与普通 API / Function Calling 的差异在哪里？
5. MCP 出现前，系统怎样让模型调用外部工具？
6. 产品、工程协作与代码维护真实成本是多少，如何量化？
7. Skill 与 MCP 的边界是什么？
8. AST Analysis 为什么需要 Sub-agent Isolation？
9. 为什么要拆多个 Sub-agent，而不是一个 Agent 全做？
10. 过去 Workflow 项目里遇到过什么限制，何时值得升级为 Agent？
11. 如果离开公司，怎样把依赖内部 Infra 的能力抽象成可迁移方案？
12. 你怎样定义 AI Application Engineer，如何理解广告商业化业务中的岗位价值？

去重：个人博客 URL与同步页均未在旧 Batch 收录；以更原始、更稳定的个人站正文作为正式来源，同步页仅用于交叉确认，不重复计数。

---

## S290 快手｜AI 全栈开发｜一面｜面试 2026-08-25｜HUMAN-A

来源：https://www.nowcoder.com/discuss/921807075905130496

真人 / 第一人称证据：作者明确记录快手 AI 全栈一面和本人实习项目深挖；Coding 时先用了不满足要求的 Heap，再根据复杂度要求回想 Quickselect 思路。面试官现场评价其表达组织不够清晰，作者也总结快手更看重 AI Coding，具有明显实时互动与反馈痕迹。

高价值问题：

1. 为什么做简历上的两个项目，真正难点分别是什么？
2. 实习业务具体做什么，本人负责哪些模块？
3. 开发过程中怎样使用 AI，所在公司是否有统一 AI Coding Practice？
4. AI 生成代码如何验证，不满足业务约束时怎样迭代？
5. Coding：数组第 K 大，要求 `O(N)` 级方案；为什么 Heap 不满足要求，Quickselect 怎样实现？
6. AI Coding 实操：实现“消费满 X 赠礼”页面，并解释需求理解和验证过程。
7. 面试官为什么认为候选人表达不够清晰，复杂项目怎样组织成可验证的技术叙述？

去重：URL 和 8/25 快手 AI 全栈流程未在正式来源出现；作者虽也面试过其它公司，但属于不同招聘流程。

---

## S291 快手｜AI 应用开发｜一面｜发布 2026-08-20，约 50min｜HUMAN-A

来源：https://www.nowcoder.com/discuss/919948330229071872

真人 / 第一人称证据：作者主页显示百度全栈实习背景，本帖明确岗位为快手 AI 应用开发、时长约 50 分钟。面试官围绕一个项目连续追问七八次，作者直接写“麻了”，之后继续进入线程池 / JVM 与 Coding，说明目标 AI 岗并不只考 AI 名词。

高价值问题：

1. 选择一个最熟悉项目，项目解决什么真实问题？
2. 为什么要实现当前功能，技术难点在哪里？
3. 围绕同一项目被连续追问七八次时，如何证明实现细节确实做过？
4. ThreadPool 核心参数如何设置，为什么要这样配置？
5. 常见线程池坑有哪些，为什么不直接使用默认 / 工厂线程池？
6. OOM 常见原因与排查路径是什么？
7. Java Memory Model 如何理解？
8. Coding：求最多可选的不重叠区间数量。
9. 反问中团队更看重毕业生哪些能力，岗位实际工作如何评价？

去重：URL、作者和“项目七八轮追问 → ThreadPool/JVM → 区间 Coding”的流程未在旧 Batch 命中。

---

## S292 OPPO｜AI 全栈开发｜一面｜发布 2026-08-23，次日查看已挂｜HUMAN-A

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

去重：URL、岗位介绍和面后状态未在现有 OPPO AI 全栈样本中出现；与 `S175 / S273` 等为不同候选人独立流程。

---

# 本批清洗与研究观察

本批正式新增：**16 个 HUMAN-A（S277–S292）**。

## 典型排除

- **B 端小公司 Agent / 法本信息 AI Agent 复制链**：`5733bf8605d44262a596ad7ba738e737` 与后发法本页面的前十余题几乎逐题同序同措辞；虽然发布时间不同，但无法可靠确认真正原始候选人，按规则整链排除，不猜“更早就是原帖”。
- **阿里控股 9 月 AI 全栈内容账号链**：作者主页显示数百篇高频多公司发布、明显私域 / 订阅导流和批量面经生产特征；即使题目很前沿，也不能当独立候选人原始经历。
- **AIGC小白入门记 / NiceOffer / 面灵 AI / 各类面试宝典**：属于付费内容、二次整理、聚合、标准答案或内容化生产，继续零贡献。
- **去哪儿 AI 全栈 AI 自动面**：明确由 AI 面试官自动追问，即使包含 MCP / Memory / Harness，也不属于真人面试。
- **美团 9 月 AI 全栈付费墙页面**：只能稳定核验部分正文，剩余内容需订阅 / 单篇购买，无法完整验证上下文，因此排除。
- **快手 4/9 AI Agent 页面**：搜索结果能看到高质量题目和“已过”，但本轮无法稳定打开完整正文，按“摘要不能入 HUMAN-A”规则排除。
- **汇川 AI 全栈 8 月场次**：岗位匹配、题目也足够多，但正文更像标准化题序，候选人现场 / 结果痕迹弱于本批正式样本，暂不硬收。
- **同一作者多家公司合集帖**：即使作者本人可信，只要单页混合多家公司且无法干净划分独立场次，就不以合集形式正式计数。

## 本批新增信号

1. **Recovery 已经进入“外部副作用幂等”层。** 不再只问 Checkpoint 能不能恢复，而是直接问“外部任务已成功、Checkpoint 前进程崩溃，Resume 后怎样避免重复执行”。
2. **Long-running Agent 开始考真实 Cancel / Timeout / State，而不是只背概念。** 面试官会追“你真的实现过取消吗”、任务中断后状态怎么处理、异常 Loop 如何终止。
3. **Tool / Skill 规模化治理成为新重点。** 100+ Tool 如何 Registry、Retrieval、Lazy Load，Tool 不可用怎样 Fallback，Skill 资源怎样 Progressive Loading，都开始出现真人追问。
4. **Security 与 Runtime Boundary 正在合流。** Tool Result Compression、Permission、Prompt Injection、Sandbox、高风险写操作确认越来越常出现在同一条工程链路。
5. **AI Coding 继续从“会不会用”升级为“代码归属与质量验真”。** 面试官会直接问代码到底是候选人写的还是 AI 写的，并通过现场修改、复杂度约束、页面实操和测试过程验证本人能力。
6. **量化指标必须能被审计。** “准确率 90%+”“性能提升 20%”“节约多少人力”都会继续追基线、样本、测量方法和 Failure Case。
7. **AI Application / Agent 岗的 Backend 深度没有下降。** ThreadLocal、Redis Lock / HotKey、RocketMQ Delay、NIO / Reactor、配置中心动态刷新与故障降级、MySQL Index 与 DB / Cache Consistency 都与 Agent 同场出现。
8. **作者时间线价值继续上升。** 同一候选人多轮可合并，不同公司可作为独立招聘命中；作者主页也越来越重要地用于识别批量内容账号与真正求职者。

## 饱和判断

**仍未达到来源饱和。** 本轮在已有 276 个 HUMAN-A 的基线上仍找到 16 个独立高质量来源，且同时覆盖最新 8–9 月与 4–7 月历史缺口。泛搜索中的复制链、内容账号、付费墙和自动 AI 面污染继续上升，但精确公司 / 岗位、作者主页与历史月份回扫仍能稳定产生新 HUMAN-A，因此不满足停止条件。

下一条正式来源从 **`S293`** 开始。
