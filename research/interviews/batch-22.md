# Batch 22 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **11** 个正式来源。

---

## S256 滴滴｜后端开发（实际 AI Agent / RAG 为主体）｜一面｜发布 2026-03-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/83dc6d39457e4f2db80ad62d82ae8e5b

真人 / 第一人称证据：作者 `要睡觉💤` 明确写“周五面的”，保留自己 AI 能力不足、担心挂掉的面后状态；评论区多人追问具体岗位和项目。虽然标题只写“滴滴一面”，但正文几乎全程围绕 OpenClaw、Agent 扩容、Context、RAG、Streaming、ES Vector 与 AI Coding，反问时面试官还明确说明团队正在整体转向 AI，实际职责通过 AI Backend / Agent Role Scope。

整场技术问题：

1. OpenClaw 在项目中具体用来做什么？
2. 当前需求为什么适合由 Agent 完成，普通固定流程能否替代？
3. 现在 Agent 调用量很小时架构可运行；调用量突然变大后会暴露哪些瓶颈，怎样扩展？
4. Context Compression 怎样做，哪些信息必须保留？
5. 超大且非常杂乱的 Context 会造成什么问题，怎样快速找到当前任务真正需要的信息？
6. RAG 的作用是什么，项目中的完整实现链路怎样组织？
7. Streaming Response 怎样实现，为什么选择 WebFlux，还有哪些替代方案？
8. Retrieval Precision 不够时，可以从哪些层面继续优化？
9. Elasticsearch 怎样存储和检索 Vector？
10. 日常怎样使用 AI Coding？
11. AI 生成代码不符合预期时，怎样迭代而不是无限重复追问，并兼顾效率？
12. 实习经历中本人真正负责什么？
13. Slow SQL 怎样定位和优化，Index Invalid 常见原因是什么？

去重：URL、作者、3 月滴滴流程和“OpenClaw → Agent 高并发 → Context 压缩 / 杂乱检索 → WebFlux Streaming → ES Vector → AI Coding → Slow SQL”连续题序均未在 `S001–S255` 形成同场重复。

---

## S257 快手｜后端日常实习（实际全程 AI Agent 项目）｜一面｜面试 2026-04-03，发布 04-04｜HUMAN-A

来源：https://www.nowcoder.com/discuss/869995757783347200

真人 / 第一人称证据：作者 `孟之梦` 明确写“无八股，全程都在聊 AI 项目”，并记录现场手撕 LC15；评论区继续追问二面、部门和项目来源。整场不是泛 Agent 八股，而是反复要求候选人用指标证明 RAG / Agent 方案、比较强模型替代方案、解释 MCP Client/Server，并复盘 AI Coding 的真实失败案例。

整场技术问题：

1. 当前 AI Agent 模式与 Cline / Code 类模式相比，效果差异是什么？
2. 怎样设计量化指标比较不同 Agent 实现，而不是只凭主观体验？
3. RAG 的真实价值是什么，与普通本地 Knowledge Base 有什么区别？
4. 项目引入 RAG 后具体优化了什么指标，提升幅度怎样测？
5. 如果把 Agent 对外提供服务，RAG Accuracy / Interception 等线上指标怎样定义？
6. 不使用 RAG、直接换成更强 Online Model 是否可能更好，怎样做对照实验？
7. 是否做过 Fine-tuning，调参数时使用什么评价标准？
8. 当前优化是否主要改善 TTFT，如何确认瓶颈？
9. 模型怎样支持 Multimodal Input，图文输入链路如何实现？
10. MCP 是自行实现还是复用已有 Server？
11. MCP 与 Skill 的职责边界是什么，Skill 怎样被发现和调用？
12. MCP 从一次对话开始到真实执行的完整机制是什么？
13. MCP Client 与 Server 怎样协作？
14. 日常是否使用 AI Coding，Web Coding 与传统编程有什么区别？
15. AI Coding 犯过的最大错误是什么，候选人怎样修复并沉淀方法？
16. AI 编程背景下，Software Engineering、工程素养和 Architecture 能力是否仍然重要？
17. Coding：3Sum / LeetCode 15。

去重：历史快手来源很多，但未出现本作者和“Agent 模式量化对照 → RAG 指标提升 / 强模型替代 → TTFT / 多模态 → MCP Client-Server → AI Coding 最大失败 → 软件工程价值”的长链，确认独立。

---

## S258 阿里云｜Agent Infra｜暑期实习一面｜发布 2026-04-01，后续未通过｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d1fd4cd344bc4d928e708c3e69c8f59c

真人 / 第一人称证据：作者 `猪脚饭之王` 的主页可以串起本人多家公司连续求职 Timeline；本帖明确为阿里云 Agent Infra 暑期一面并更新“后续：挂”。问题从 Go / Java、Spring、gRPC、TCP、MySQL、Redis 一路进入 Rerank、Embedding、Transformer、HNSW、LLM Generation、RAG 与 Claude Code，符合 Agent Infra 对系统底座和 LLM 工程同时验真的特点。

整场技术问题：

1. Go 与 Java 在服务端 / Agent Infra 中的主要差异是什么？
2. Spring Bean 是什么，完整生命周期怎样理解？
3. gRPC 为什么使用二进制编码，Protocol / Serialization 怎样工作？
4. TCP 的核心可靠传输机制是什么？
5. MySQL Index 使用什么数据结构，Composite Index 如何工作？
6. Redis Distributed Lock 怎样实现，真实场景有哪些边界问题？
7. Rerank Model 的原理与作用是什么？
8. Embedding Model 与 Rerank Model 在目标和推理方式上有什么区别？
9. Transformer 中 Q / K 怎样计算并参与 Attention？
10. HNSW Index 的核心图搜索机制是什么？
11. 从输入 Prompt 到模型生成 Token，一次 LLM Generation 的底层路径怎样完整描述？
12. 现场从简历项目某个模块继续追真实源码与 Class Data Structure，怎样证明本人实现？
13. RAG Chunk Strategy 怎样选择？
14. 上一段实习最有价值的工作是什么，具体贡献怎样证明？
15. Cursor / Claude Code 平时怎样进入真实开发流程？

去重：URL、作者的该阿里云流程以及“系统基础 → Rerank / Embedding → Transformer QK → HNSW → 完整 LLM Generation → 源码验真”的连续题序未在历史阿里云样本出现。

---

## S259 小红书｜AI 全栈｜暑期一面 + 二面（同一候选人同流程合并）｜发布 2026-04-06 / 04-08｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/58cf212916c142d88a197f09b65de1a8

二面来源：https://www.nowcoder.com/feed/main/detail/ce5e745958124432a47aaebb0aa0ad45

真人 / 第一人称证据：两篇均由 `猪脚饭之王` 发布；一面末尾明确更新“第二天约二面”，二面两天后发布并更新“后续挂”，作者、公司、方向和时间线完整闭环，因此合并为一个 `Sxxx`。两轮覆盖 MCP / Tool、GMP、RAG、Skill、Go Sync / Gin、AI Coding 质量和现场 Coding。

整场技术问题：

### 一面

1. 实习中本人主要负责什么？
2. MCP Architecture 中 Tools、Resources、Prompts 分别承担什么职责？
3. Agent Application 中 Tool 应怎样设计？
4. MCP 怎样接入 Agent Runtime？
5. Go GMP Scheduler 怎样工作；G 阻塞后 Runtime 会发生什么？
6. Coding / 场景题：对比两个 JSON Object，判断中间经历了哪些操作或变化。
7. Coding：Binary Tree Level-order Traversal。

### 二面

8. 分别介绍实习内容的业务背景、开发过程和后续迭代。
9. RAG 的完整 Pipeline 是什么？
10. Go `sync` Package 常用哪些能力，在真实代码里怎样使用，底层原理是什么？
11. 自己怎样构建 Skill，方案如何组织？
12. 除公司业务外，日常生活中怎样用 AI 提效？
13. Gin Framework 的核心机制怎样理解？
14. 怎样使用 AI Coding 从 Requirement 走到完整 Implementation？
15. 如何防止 AI 写出 Bad Code，Testing / Review 怎样建立？
16. Coding：固定 Push 顺序下判断 / 构造合法 Pop 顺序，使用 Backtracking。

去重：两 URL 均未在历史来源出现；同作者同公司明确合并。历史小红书样本没有“MCP Tools/Resources/Prompts → GMP Blocking → JSON Diff Coding → Go Sync/Gin → AI Coding Bad Code Testing”的完整题序。

---

## S260 阿里灵犀互娱｜AI 应用开发｜暑期二面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3dbec664147348d685f3e2b8b50288f8

真人 / 第一人称证据：作者同为 `猪脚饭之王`，属于其个人求职 Timeline 中另一家公司独立流程。本页明确是灵犀互娱 AI 应用开发暑期二面，问题集中在 AI Coding、游戏智能客服、Intent Small Model、Multi-Agent、多平台数据源、Context 与 Memory；后续同步页显示该候选人继续进入 HR 流程。

整场技术问题：

1. 日常怎样使用 AI Coding，如何保证生成结果满足 Requirement？
2. 从零设计一个 Game Intelligent Customer Service Agent，整体 Architecture 怎样拆？
3. Intent Recognition Small Model 怎样训练，Dataset 怎样构造？
4. 什么情况下选择 Single-Agent，什么情况下使用 Multi-Agent，依据是什么？
5. Agent 怎样打通多个平台 / 系统的数据源访问？
6. 如果同一 Conversation 中每句话都是彼此独立的问题，Context Management 应怎样设计？
7. 设计 Game Assistant Agent 时，Memory System 怎样实现？
8. 自动挂机 Agent 与传统确定性脚本相比有什么优势和风险？
9. 游戏角色的 State 应怎样定义并提供给 Agent？

最终正文稳定性处理：同作者 04-03 的灵犀一面页在最后复核阶段再次无法稳定打开，因此本来源**只使用 04-10 二面原页**；04-03 页面零贡献。另有 05-06 不同作者页面复刻一面题序，只作为后发复制信号，零贡献。

去重：当前二面 URL、作者 / 公司流程与“游戏客服 → Intent Small Model → 多平台 Data Access → 独立消息 Context → Game Assistant Memory → Auto-play Agent”题序均未在历史正式来源形成同场重复。

---

## S261 美团｜AI 全栈开发｜日常实习二面 1h｜发布 2026-04-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7a81aedcc9d14863a6c2bfd7a309603d

真人 / 第一人称证据：作者 `励志搞钱大鹅` 以本人“AI 全栈开发日常实习二面 1h”发布。题目数量不多，但现场证据很强：面试官要求共享屏幕，直接用本地 AI Coding 工具完成需求，并继续演示面试前准备的 AI Coding 项目和真实效果；这比标准概念题更能反映 AI Application 岗的项目验真方式。

整场技术问题：

1. 深挖实习经历，本人实际负责什么？
2. 深挖个人项目，哪些模块和决策是候选人亲自完成？
3. 平时怎样使用 Cursor？
4. 是否自己写过 Skill，实际解决什么问题？
5. 一个新需求到来时，怎样决定使用 MCP 还是 Skill？
6. 现场 AI Coding：共享屏幕，使用本地 AI Coding Tool 直接实现一个简单需求，并解释过程和验证方式。
7. 展示面试前完成的 AI Coding Project：如何利用工具构建、内部如何实现、最终效果怎样？

去重：历史美团 AI Full-stack / Agent 来源未出现该作者与“Skill/MCP 选型 → 屏幕共享本地 AI Coding 实现 → 现场演示预先项目效果”的同场验证链，确认为独立流程。

---

## S262 京东物流｜后端开发（实际 Agent 项目为核心）｜一面 + 二面（同一候选人同流程合并）｜发布 2026-04-08 / 04-14｜HUMAN-A

一面来源：https://www.nowcoder.com/discuss/871056191454048256

二面来源：https://www.nowcoder.com/feed/main/detail/bed0467d91c2473e821509cd89229954

真人 / 第一人称证据：两篇均由 `纯马牛马牛🐮` 发布，学校、方向、公司和时间线一致。一面不到 30 分钟、无 Coding，作者直言像 KPI 面；6 天后二面约 35 分钟，明确写“主要拷打 Agent 项目，传统后端八股没咋问”。反问还核实团队已经用 Spring AI 在小场景做 Agent，并准备继续探索核心物流业务，因此 Role Scope 清晰，合并为一个招聘流程来源。

整场技术问题：

### 一面

1. 实习什么时候能到岗，过去实习做了什么、持续多久？
2. Redis BigKey 是什么，怎样发现和优化？
3. Hash BigKey 拆分 / 删除旧版本后，怎样保证迁移过程的数据一致性？
4. Redis Memory 不足时怎样选择 Eviction Policy？
5. 使用 LRU 后，一个刚被淘汰的 Key 又立刻被请求时会发生什么，怎样治理？
6. 项目中 Distributed Lock 的真实使用场景和实现方案是什么？
7. ThreadLocal 为什么可能 Memory Leak，如何避免？
8. Business Logic 抛异常时怎样确保 `remove` 仍然执行？
9. Agent 项目是从开源项目二次开发还是自主实现？
10. Agent Memory 怎样做，Short / Mid / Long-term Memory 如何分层？
11. RAG Recall / Accuracy 是否测过，怎样保证结果可信？
12. MCP、Skill、OpenClaw 等概念在当前 Agent Architecture 中分别承担什么职责？
13. 是否使用 Coze 等 Agent Platform，平时是否使用 AI Programming？

### 二面

14. 历史业务正在重构时突然进入新需求，怎样兼顾迁移和交付？
15. 多人协作项目怎样分工，简历项目来源和个人贡献如何证明？
16. Agent 项目的完整链路是什么？
17. RAG 的拆分、存储和使用逻辑怎样设计？
18. Spring AI Framework 的整体结构是什么，为什么选择它？
19. 是否了解非 Java Agent Framework，怎样比较？
20. 当前 Agent 各层都搭好后，还缺哪些真正面向生产的能力？
21. Agent Context 怎样管理，Short / Mid / Long-term Memory 怎样协作？
22. Base Model 怎样选，是否实际比较过其它模型？
23. AI IDE / Model 平时写了哪些真实代码，生成代码质量怎样评价和提升？
24. 实习生进入真实落地项目后，怎样最快理解生产业务并开始承接需求？

去重：两条 URL 同作者、同公司、时间连续，主动合并不拆号；“Redis BigKey Migration → ThreadLocal finally → 三级 Memory → Spring AI → AI Code Quality → 快速上手真实物流业务”的连续链未在历史京东来源出现。

---

## S263 小红书｜AI 全栈开发｜暑期二面｜发布 2026-04-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4dbb7539b78a4d1ca3d48a837b4a83d8

真人 / 第一人称证据：作者 `静息狂想` 是已能通过其它公司求职记录核验的真实候选人；本页明确是本人“小红书暑期实习 AI 全栈开发二面”，评论区继续追问具体方向和部门。该候选人与历史百度 `S255` 为不同公司独立招聘流程，因此不能合并。

整场技术问题：

1. 常用 LLM 有哪些，怎样做应用侧选型？
2. NL2SQL Project 的完整 Pipeline 怎样组织？
3. Vector Retrieval 使用什么 Strategy？
4. 一个业务 Term 同时可能匹配多个 Field 时，Entity Mapping 怎样做？
5. Skill 与 MCP 的区别是什么？
6. MCP 开发 Update / Write Method 时怎样保证 Security？
7. 秒杀业务怎样避免 Oversell？
8. Prompt 日常怎样写，哪些细节最影响稳定性？
9. Workflow / Constraint 经常不被模型遵守时怎样治理？
10. 强制下游需要 JSON 时，怎样设计 Prompt / Structured Output Contract？
11. Redis TTL 与 Lazy Refresh 有什么区别？
12. 大量嵌套 `if` 怎样重构，改善可维护性？
13. Coding：Bracket Matching。

去重：URL 未入库；作者虽已在别家公司出现，但本场为独立小红书流程。“NL2SQL → Entity Mapping → MCP Update Security → Prompt Constraint / JSON → Redis Lazy Refresh → Nested-if Refactor”题序与历史小红书样本不同。

---

## S264 阿里云｜Agent 开发｜暑期一面｜发布 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/discuss/878263655001772032

真人 / 第一人称证据：作者 `总是难免` 明确以“阿里云 Agent 开发 一面 / 发面经攒人品”记录本人流程；问题从实习线上排查、设计模式、退避轮询和 Checkpoint 一路进入 DB/Cache、一致性、分布式锁、JVM、Agent Context / Memory 与现场 Coding，具有自然的工程追问链。

整场技术问题：

1. 实习中最难的问题是什么，怎样克服？是否有真实 Online Troubleshooting 经验？
2. Strategy、Factory、Template Method 在项目中分别怎样使用，边界有什么差异？
3. Exponential / Stepped Backoff Polling 的 Base 与 Cap 怎样确定？
4. Peak / High-frequency Request 下如何保证 SLA？
5. 系统 Checkpoint Rollback Mechanism 怎样实现，什么时候读取 Checkpoint？
6. Transaction 场景下怎样保证 Database 与 Cache Consistency？
7. Randomized / Sharded Distributed Lock 是什么，怎样设计？
8. Cache Breakdown / Avalanche 怎样治理？
9. JVM Memory 与 Garbage Collection 的基本机制是什么？
10. Agent 的基本执行机制怎样理解？
11. Agent Context Window 超过模型上限时有哪些处理方式？
12. Short-term / Long-term Memory 分别解决什么问题？
13. Coding：Binary Tree Level-order Traversal。
14. Coding：Median of Two Sorted Arrays，并分析复杂度。

去重：当前作者、4/27 阿里云流程与“Backoff SLA → Checkpoint Rollback → Transaction DB/Cache → Random Sharded Lock → JVM → Context Overflow / Memory”的组合未在历史阿里云来源出现。

---

## S265 快手｜AI 业务应用设计开发（产品 + 研发复合 Agent 岗）｜二面｜发布 / 编辑 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/cd439337596147bbaa51fcc8074fa923

真人 / 第一人称证据：作者 `zzzilik` 明确写“一面过后转岗被捞起来了直接从二面开始”；面试官现场介绍该岗是产品 + 研发复合岗位，实际业务是安全风控 PR 领域 Agent Application Exploration，研发内容包含 Skill 和 Harness Engineering。正文还保留到岗确认、反转链表和面试官对“AI 模糊传统岗位边界”的反馈，招聘现场痕迹完整。

整场技术问题：

1. 从业务视角解释过去实习：接到 Requirement 后怎样理解、设计并推进？
2. 实习工作使用哪些 Metric 衡量，Cold-start 0→1 怎样定义？
3. 上线后如何利用 User Feedback 构造 Data Flywheel？
4. 有哪些方法能从用户反馈中更完整、深入地发现真实 Pain Point，并反向指导开发？
5. AI 的出现会怎样改变 Programmer / Engineer 的工作？
6. Harness Engineering 是什么；如果从零搭建，会建设哪些能力？
7. 未来 Agent Architecture / Product 可能怎样演进？
8. 快手已有多个 AgentOS / AI Application Team 时，未来哪些基础能力仍值得重投入？可以从 Model、Framework、Skill 等层面判断。
9. 确认到岗时间和求职意向。
10. Coding：Reverse Linked List。

去重：历史 `zzzilik` 的字节样本属于不同公司招聘流程，可以独立计数；本场“转岗被捞 → 产品研发复合岗 → 安全风控 PR Agent → Data Flywheel → Harness → AgentOS 基建投资判断”的题序未在快手历史来源出现。

---

## S266 美团｜后端 Agent 开发｜实习一面｜发布 2026-04-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4e2aff1a23bd47b2a401a3526a89a20d

真人 / 第一人称证据：作者 `笔试轻松过关` 以本人“美团后端 Agent 开发一面-实习 / 发点面经攒攒人品”发布；评论区同期候选人继续确认没有手撕、追问 Redis Lock 场景。此前 `api-cdn` 入口曾报错，但最终校验时 canonical `www` 原页能够完整稳定读取作者、正文、7 个问题和评论，因此通过 Stable-body Gate。

整场技术问题：

1. Agent Loop / 循环执行流程怎样工作？
2. RAG Knowledge Base 使用什么 Model，是否调研比较过其它模型？
3. Redis 在什么场景需要 Distributed Lock？
4. Cache 与 Database 更新时怎样保证 Consistency？
5. Java 创建 Thread 有哪些方式，Thread State 有哪些；`sleep` 与 `wait` 有什么区别；Deadlock 需要哪些条件？
6. OSI / Network Layer 怎样理解；TCP 与 UDP 有什么区别，TCP 如何保证可靠传输？
7. 开放题：怎样看 AI Coding 对 Programmer 门槛、职责和工程能力要求的影响？

去重：虽然问题数量较少，但全部为明确技术主题，并处于目标 Agent Backend 实习流程；URL、作者和“Agent Loop / RAG → Redis Lock / Cache Consistency → Java Thread → TCP Reliability → AI Coding Impact”题序未与历史美团来源形成同场重复。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## Batch 22 最终校验中的典型排除 / 合并

- **腾讯 `Akhasi` 流程归属不清，整链排除。** 作者 04-19 同日存在“腾讯视频一面（过）”和“腾讯视频二面（横向挂）”，但 05-21 又发布另一条“腾讯二面”。无法可靠确认 05 月页面究竟是同一流程、重新被捞还是另一岗位，因此不猜、不合并、不编号。
- **阿里灵犀不稳定一面零贡献。** `猪脚饭之王` 的 04-03 灵犀一面页在最终复核时再次无法稳定打开，因此不使用其中任何题目；只保留能够稳定核验的 04-10 二面 `S260`。05-06 不同作者逐题复刻一面的问题只作为复制链证据。
- **京东物流两轮主动合并。** 04-08 一面与 04-14 二面均为 `纯马牛马牛🐮`，同公司同招聘流程，合并为 `S262`，不按轮次虚增。
- **小红书两轮主动合并。** `猪脚饭之王` 04-06 一面明确次日约二面，04-08 二面后续挂，两页合并为 `S259`。
- **美团 5 月复制链排除。** 一条看似很强的新候选向前追到 04-20 更早页面，出现“Fuzzy Query → RRF 参数 → 空教室 / 火锅场景 → Hallucination Chain → HTTP3 / V8”等长连续同序，原始归属无法可靠确认，整链不收。
- **阿里平头哥后续轮次不新增。** 04-29 二面可确认属于历史 `S118` 同候选同流程；遵循不修改历史 Batch 的当前指令，本批不另增编号。
- **近期百度整齐题单继续排除。** 同账号多日重复 / 扩写，正文称只问少量开放架构题却又整齐列出大量题目，内容包装风险高，未进入 HUMAN-A。
- **字节高密度题单因现场证据不足未放行。** 某 04-08 页面虽然问题多，但作者页面和正文不足以达到当前对真人现场 / 招聘交互的严格阈值；宁可不收。
- **快手大题单不因题量高自动升级。** 一条 4 月候选按知识域整齐覆盖大量问题，评论区也出现“真的会问这么多吗”的质疑；没有足够强的现场与作者证据前保持排除。

---

## Batch 22 现实信号 / 饱和度复核

1. **高搜索量继续有效。** 在 Batch 21 已经新增 11 个后，本批最终仍放行 12 个独立 HUMAN-A，说明热门公司全年真人来源整体尚未进入“扩量也几乎搜不到新来源”的饱和阶段。
2. **3～4 月长尾仍是主要增量区。** 本批大量新增来自腾讯 / 滴滴 / 快手 / 阿里系 / 小红书 / 美团 / 京东在春季实习阶段的原场，而不是 8～9 月热门第一页。
3. **去重与 Provenance 成本继续高于搜索成本。** 强候选池约 15 个流程，最后仍因为 Timeline 不清、复制链、正文稳定性等原因主动撤出；“发现候选”与“能成为 HUMAN-A”已经是两件不同的事。
4. **AI Application 面试进一步从概念转向现场工程验真。** 美团要求屏幕共享直接 AI Coding，快手追 AI Coding 最大失败，京东追 AI IDE 到底写过什么真实代码以及如何提升质量。
5. **Agent 与 Backend Foundation 继续高度融合。** 阿里云 Agent Infra 同时考 gRPC/TCP/MySQL/Redis 与 HNSW/LLM Generation；京东、美团、滴滴同样把 Redis、Thread、Network、SQL 与 Agent/RAG 放在一场。
6. **RAG / Agent 方案越来越需要量化证明。** 快手连续追 RAG 指标、提升幅度、强模型替代对照；京东直接问 Recall / Accuracy 是否真正测过；候选人只会复述 Pipeline 已经不够。
7. **Context / Memory 正从“知道概念”变成业务设计题。** 滴滴问超大杂乱 Context 怎样找到所需信息，京东问 Short/Mid/Long Memory，灵犀把 Memory 放到 Game Assistant / Auto-play Agent 的具体场景中。
8. **Harness / AgentOS 已进入业务岗位。** 快手复合岗不仅问 Harness 定义，还要求判断未来哪些 AgentOS / Framework / Skill 基建值得继续重投入。

---

## 本批统计

- 新增 HUMAN-A：**12 个**
- 编号范围：`S256–S266`
- 累计 HUMAN-A：**360 个**
- 当前最大编号：`S266`
- 下一条正式来源：**`S214`**
- Inbox：归档后为空
- 饱和度判断：**热门结果页局部饱和；热门公司全年真人来源整体仍未饱和。继续保持“最新层 + 3～7 月长尾 + 作者 Timeline”的高搜索量策略。**
