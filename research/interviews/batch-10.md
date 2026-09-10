# Batch 10 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **15** 个正式来源。

---

## S176 Bilibili｜Coding Agent / Agent 开发｜日常实习一面｜发布 2026-08-28｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/53623f73e06e4c868a05f8f74dd5be4d

真人 / 第一人称证据：候选人围绕自己修过的开源 Coding Agent 逐层复盘，面试官多次要求“不要只讲概念，要讲代码实现”，追到具体命令、协议、权限和 Skill Progressive Disclosure。

高价值问题：

1. 给开源 Coding Agent 修过什么问题，为什么要改？
2. 为什么很多 Agent 工程使用 Python？
3. OpenAI-compatible API 与 Anthropic / Gemini Protocol 有哪些差异，Responses API 怎样理解？
4. ReAct / Plan-and-Execute 在代码里分别由哪些模块实现？
5. Code Search 实际使用 `ripgrep` 时命令与参数怎样组织？
6. 不依赖传统 RAG 时，Hybrid Code Retrieval 怎样做？
7. Search / Tool Architecture 怎样设计？
8. Shell Tool 的 Permission 与 Execution Environment 怎样隔离，Blacklist 实际怎样实现？
9. Skill Progressive Disclosure 在代码层怎样实现？
10. Skill Description 放在哪里，System Prompt / Context 的注入顺序是什么？
11. Coding：Merge Intervals。

---

## S177 第四范式｜Agent 开发实习生｜一面｜面试 2026-03-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/77a81a03b55143c89d1caf76833676d9

真人 / 第一人称证据：作者记录通过 BOSS 投递、HR 询问 Vibe Coding、真人技术面和后续通过结果；问题围绕本人 Agent 项目连续追到 LangGraph、MCP、RAG、Memory、模型路由和故障降级。

高价值问题：

1. Agent 项目是个人还是团队完成，是否有 Running URL，本人负责什么？
2. Go / Python Microservice 与 Vue / Flutter 怎样组成完整产品？
3. LangChain / LangGraph 怎样使用，MCP Adapter 放在哪一层？
4. ReAct 与 Database Interaction 怎样做，为什么修改类操作需要 Confirmation Node？
5. 常见 Agent Mode 如何选择？
6. RAG 在项目中解决什么问题？
7. Short-term Memory 与 Long-term Memory 怎样分层，Compaction 用规则还是 LLM？
8. Opus / Sonnet / Haiku 等不同能力模型怎样路由？
9. AI Coding / Spec-driven Development 怎样进入真实研发流程？
10. Tool Call 如何做 Circuit Breaker，Model Backend 失败如何 Failover？

---

## S178 科大讯飞｜Agent 开发｜一面｜面试 2026-03-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a28eee51435f46fdbd6df733ca02a21b

真人 / 第一人称证据：作者保留了现场 Merge K Lists 因 ListNode 构造卡住、向面试官要提示等状态，并明确记录面试语言与问题顺序，具有明显真人面试痕迹。

高价值问题：

1. RAG 的完整链路是什么？
2. Embedding 为什么能表示语义，Vector Space 怎样理解？
3. WebSocket 与 SSE 的差异是什么，HTTP 是否有状态？
4. Agent / RAG Evaluation 用什么指标，指标怎样证明有效？
5. Prompt 与 Chunk Strategy 怎样设计？
6. Kafka 在 Agent Backend 中为什么适合异步解耦？
7. File Upload Service 怎样设计？
8. Chat History 为什么放 Redis / MySQL，持久化怎样做？
9. Linux `kill -9` / `kill -15` 有何区别，怎样根据端口查进程？
10. Coding：Merge K Sorted Lists。

---

## S179 科大讯飞｜AI 应用 / Agent 方向｜技术面｜发布 2026-05-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1c425483516d4af1813d2dcdf98f4781

真人 / 第一人称证据：作者以本人面试复盘发布并更新当前已通过；面试官会围绕一个回答继续追单点，不是标准题单，问题从自动工单 Agent 进入 Tool Abstraction、Evaluation、Skill 与 AI Coding。

高价值问题：

1. 自动工单 Agent 的完整 Workflow 是什么？
2. 为什么选择 ReAct，而不是 Plan-and-Solve 或固定 Workflow？
3. OCR 漏字段时怎样 Fallback？
4. Agent Evaluation 应覆盖哪些维度？
5. Tool 怎样分层抽象并支持 Dynamic Discovery？
6. ORM / Business API 直接封成 Tool 时怎样处理 Schema Drift？
7. LangChain 与 LangGraph 在当前项目里如何比较？
8. 好 Prompt 怎样定义，Prompt Evaluation 怎样做？
9. Skill 与 Prompt / Shared Abstraction 的边界是什么？
10. Claude Code / Codex / Vibe Coding 在真实研发中怎样使用？

---

## S180 字节跳动｜AI 应用开发｜一面 + 二面面试官合并场｜发布 2026-04-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c5947496fc29440883611173478dc257

真人 / 第一人称证据：作者明确说明 HR 为加快流程让一面、二面面试官同场，吐槽其中一位面试官同时戴两副耳机；评论里还说明自己没有录音、记忆力一般，所以面经不全，现场痕迹很强。

高价值问题：

1. DAG Orchestration 是怎样实现的，每个 Agent 分别承担什么职责？
2. LangGraph 怎样编排 Graph？
3. Agent / RAG Evaluation 怎样做，Dataset 如何构建？
4. Semantic Chunking 如何实现？
5. Fine-tuning 与 Reinforcement Learning 分别适合什么场景？
6. HNSW Index 如何构建？
7. Multi-file Knowledge Input 怎样处理？
8. ThreadLocal 解决什么问题？
9. LangChain Checkpoint 如何工作？
10. Agent Harness 怎样理解？
11. 项目里的 Perception / Scheduling 如何实现？
12. Coding：Ugly Number；另有现场逻辑题。

---

## S181 Moka｜AI 后端开发｜二面｜发布 2026-04-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/22d4ec9147f94b34b2f009808e31c4cb

真人 / 第一人称证据：作者明确描述自己被一个 Redis 设计问题“带偏”，后面被面试官沿着 Hash Layout、TTL、异步持久化和 Agent Session 连续追问，问题流自然。

高价值问题：

1. Video Progress 为什么放 Redis，并定时异步刷回数据库？
2. 怎样 Scan / 统计 Redis 中相关 Progress 数据？
3. Redis Hash 应怎样设计 Field / Value？
4. Hash 内不同 Field 能否独立 TTL，若不能怎样重构？
5. 用户未看完视频就离开时怎样判断和保存进度？
6. Redis / Async Persistence 异常时怎样避免 Progress 丢失？
7. RabbitMQ Delay Queue 如何使用？
8. Agent Tool 怎样组织？
9. Multi-turn Memory 怎样保存，是否每次从 MySQL 加载全部历史？
10. MCP Local 与 Remote / SSE 模式有什么差异？
11. 多节点 Agent Backend 中 SSE 与 WebSocket 怎样选？
12. Agent 是否应尽量 Stateless，Session Routing 怎么做？

---

## S182 钉学科技｜FDE 实习｜技术面｜面试 2026-08-13，发布 08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c837307a81854e208eea037766f0bdcf

真人 / 第一人称证据：作者以本人 8 月 13 日 FDE 实习面试记录发布，末尾写“面试官说答得还可以，但是三天了还没有推进后续”；评论区有人质疑“这更像 AI 应用开发”，恰好反向说明岗位实际技术职责集中在 Agent / RAG / Workflow，符合本库 FDE / Applied AI Role Scope，而不是传统售前或纯方案岗。

整场技术问题：

1. 简历中的项目是否为本人核心参与，具体负责什么？
2. Code Review Workflow 中三个并行 SubAgent 在 Prompt 与 Tool Selection 上怎样区分职责？
3. Supervisor Agent 汇总多个 SubAgent 结果时，怎样处理 Conflict 与 Priority？
4. RAG 只做 Vector Retrieval 有什么缺陷，BM25 补了什么短板？
5. 两路 Retrieval 的结果怎样 Merge / Rank？
6. 给一个真实 Case，证明 Hybrid Retrieval 比单一路径更好？
7. SubAgent 循环 Retry 到上限后怎样终止、降级或转人工？
8. LangGraph Checkpointer / Workflow Persistence 应保存哪些 State 字段？
9. Human-in-the-loop 长时间不确认时，Timeout Policy 怎样设计？
10. Node State 同时落 MySQL 与 Redis 时，怎样处理一致性？
11. Workflow 中断后 Resume，如果用户已经切换 Model，旧状态如何兼容 / Migration？
12. MCP 与 Function Call 的区别是什么？
13. LangChain 与 LangGraph 分别适合什么场景？
14. 使用 LangGraph 编排 Workflow 时，Edge、Node、State 哪个最重要，为什么？

去重：URL 与钉学 FDE 招聘流程未在 `S001–S235` 出现；“三并行 Code Review SubAgent → Supervisor Conflict Merge → Hybrid Retrieval Case → Retry Upper Bound → Checkpointer 字段 → Human Timeout → MySQL/Redis State Consistency → Resume 后模型切换”的题序高度独特，未发现同场复制链。

---

## S183 金山办公｜AI 全栈开发｜一面｜发布 2026-09-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/10c05ff1d2044210bdc43c13ab2d8047

真人 / 第一人称证据：作者记录约 60 分钟一面和整体体验评分；整场从 MySQL / Frontend / Async / OS / Network / Spring 进入 Model API 与 RAG，符合真正 AI Full-stack 的全链路考察。

高价值问题：

1. MySQL 怎样排 Slow Query，什么时候考虑 NoSQL？
2. Vue / React Component 与 State Management 怎样理解？
3. `async/await` 的本质是什么，Event Loop 怎样工作？
4. Process / Thread / Coroutine 有什么区别？
5. 从 0 到 1 做过什么 Application，技术选型怎样决定？
6. Linux / Docker / Dockerfile 的常用能力是什么？
7. Server 出问题且不能依赖 AI 时，怎样手工排障？
8. TCP / UDP / HTTP / WebSocket 的适用场景分别是什么？
9. Git Reset / Revert / Conflict 怎样处理？
10. REST、Spring / Spring Boot、Design Pattern 怎样用于服务开发？
11. Model API 的 Temperature / Messages 等参数怎样影响行为？
12. RAG 客服系统从 Chunk、Embedding、Vector DB 到 Retrieval 的完整链路是什么？

---

## S184 字节跳动｜大模型应用开发｜日常实习二面｜发布 2026-03-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/30b6f37830414df5a32d851f2004df7a

真人 / 第一人称证据：候选人以本人二面复盘发布，整场以 RAG / Serving / Async Backend 为主线并包含现场 Coding，技术链连续而具体。

高价值问题：

1. Long Document 怎样切片，Overlap 为什么需要？
2. Dense / Sparse Vector 有什么区别？
3. Top-K 过大会带来什么问题？
4. Cosine Similarity 与 Euclidean Distance 怎样选择？
5. Rerank 为什么有效？
6. Knowledge Base Incremental Index 怎样更新？
7. No-answer Boundary 怎样通过 Prompt / Evaluation 控制？
8. HyDE 是什么，什么时候可能有效？
9. Long Context 与 RAG 怎样取舍？
10. SGLang 与 vLLM / PagedAttention 有什么差异？
11. `asyncio` 怎样支撑高并发 API？
12. 大量 PDF Processing 应选 Thread 还是 Process？
13. Structured JSON Extraction 怎样提高可靠性？
14. 多份手册互相冲突、存在时效性差异时怎样决定答案？
15. Coding：第 K 大。

---

## S185 京东｜AI Agent 开发实习生｜二面｜面试 2026-04-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7af26b7a99e54b29af671ac334b445b5

真人 / 第一人称证据：作者明确写自己没有 AI 项目，面试官因此很快结束项目环节；整场约 35 分钟且没有算法，作者甚至怀疑是 KPI 面，现场状态真实。岗位本身明确为 AI Agent，基础后端问题仍完整保留。

高价值问题：

1. ThreadLocal 的底层机制是什么？
2. RPC 与 HTTP 有什么差异？
3. 常见 Rate Limiting 算法怎样选择？
4. RAG 解决什么问题？
5. RAG 与直接调用模型相比有什么收益？
6. Agent 与固定 Workflow 有什么区别？
7. 平时怎样使用 AI Coding？
8. AI 生成过哪些质量差的代码，怎样纠正并提升效率？

---

## S186 曹操出行｜Agent 开发实习生｜一面｜面试 / 发布 2026-08-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1650bd48a48644138ebf2362740abc86

真人 / 第一人称证据：候选人围绕本人实习产出和 LangGraph Agent 项目接受连续追问，问题重点是“为什么一定要 Agent、为什么不是脚本 / Workflow”，并追到长链路稳定性和 Evaluation。

高价值问题：

1. 实习项目的 Timeline、Business Flow 与实际 Output 是什么？
2. 为什么选择 LangGraph，而不是 Automation Script？
3. 某些 Hard-code 就能做的步骤为什么还要 Agent？
4. 为什么 Ticket Creation 要拆成 Subgraph / Agent？
5. LangGraph 相比其他框架的具体收益是什么？
6. Graph 中各 Node 怎样映射真实业务系统？
7. Long-chain Agent 怎样保证稳定执行？
8. Skill 怎样优化？
9. Agent Evaluation 怎样设计？
10. AI Coding Tool 有哪些真实 Pitfall，工程师如何控制质量？

---

## S187 Insta360｜Agent 开发｜一面｜面试 2026-03-11｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f9c5e9f04ded46508de4f14a76a3cdd3

真人 / 第一人称证据：作者明确描述面试官整体偏冷淡、项目没有深挖、约 20 多分钟，并认为可能是 KPI 面；时间过去较久所以部分记忆不完整，这类不完美记录反而具有真实候选人痕迹。

高价值问题：

1. 实习做了什么，核心 Output 是什么？
2. MySQL 使用什么版本，哪些字段不适合建 Index，Index 为什么可能失效？
3. MQ Backlog 怎样处理，Duplicate Consumption 怎样保证幂等？
4. Docker 常用命令、Container Info 和 Network Mode 怎样理解？
5. Kubernetes 基本使用经验是什么？
6. Go Map 是否 Thread-safe，怎样保护并发访问？
7. RAG / OpenClaw / Skill 分别是什么，有没有实际写过 Skill？
8. Coding：BFS Level Order Traversal。

---

## S188 滴滴｜AI Agent 后端｜两轮技术面，已挂｜2026 秋招 / 实习季｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/17ee6ae95cc44ec19b9eefadb69da6b3

真人 / 第一人称证据：作者明确以“滴滴 AI Agent 后端面经 / 两轮面经 / 已凉凉 / 发面经攒人品”发布。题目从本人 Agent 项目持续追到 Memory、Hallucination、Context Pollution，再大幅进入 Spring、Redis、Go Runtime、MySQL、WebSocket、扫码登录、Service Discovery 和 GC，能够很好代表 Agent Backend 的真实基础深度。

高价值问题：

1. 最近 Agent 项目是实习还是个人项目，本人具体负责哪些部分，最难的问题是什么、怎样解决？
2. Agent 的典型模块与常见设计范式有哪些？
3. Short-term / Long-term Memory 如何区分，Memory Compression 有哪些策略？
4. Agent 如何降低 Hallucination；放到工业场景时还需要哪些 Verification / Guardrail？
5. Multi-Agent / 多 Async Task 如何防止 Context Pollution？
6. 项目为什么选择 Spring 或 Socket，协议 / Framework 取舍是什么？
7. Spring AOP Proxy 在什么情况下失效；Circular Dependency 如何定位；Spring MVC 完整执行流程是什么？
8. Maven Transitive Dependency 会引入什么冲突，怎样处理？
9. Redis 支持哪些结构、为什么快、为何常说核心命令单线程；发生 Blocking 会有什么影响？
10. ZSet 底层结构与应用场景是什么；Sentinel 怎样工作；BigKey 对 Memory / Latency 有什么影响？
11. Go Channel 与 Mutex 在并发控制上的差异是什么；GMP 中 P 的 Local Queue 为空 / 非空时如何调度 G？
12. MQ 适合什么场景？Database Transaction ACID 与 MVCC 怎样实现？
13. Database Index 底层结构是什么，哪些写法会导致 Index Invalid？
14. 设计类似淘宝搜索框的实时商品名 Fuzzy Search；输入联想与点击搜索的技术差异是什么？实时交互为什么可能使用 WebSocket？
15. 微信扫码登录从 PC 二维码到手机授权、Token / Session 建立的完整流程是什么？
16. 微服务 Service Discovery / Load Balancing 怎样实现，Nacos / Consul 如何注册、保活与 Heartbeat？
17. JVM GC 基本机制和 CMS Collector 如何工作？
18. Coding：Reverse Linked List。

去重：URL 和两轮滴滴 AI Agent Backend 流程未在 `S001–S230` 出现；“Agent Memory / Context Pollution → Spring → Redis → Go GMP → 实时搜索 / WebSocket → 扫码登录 → Service Discovery → CMS”的长题序未发现同场复制。

---

## S189 百度｜Go Backend / Agent 方向｜秋招一面｜发布 2026-08-28｜HUMAN-A

来源：https://www.nowcoder.com/discuss/922907945363349504

真人 / 第一人称证据：作者明确写自己“答得不怎么好，追问一问就傻”，但一面结束后秒约二面；问题数量很多且紧扣本人 Red-team / Agent Project，从 Session Resume、TodoStore、Long-term Memory 追到多 Pod Routing、Evaluation 和数据库分片。

高价值问题：

1. Red-team Agent 的完整 Architecture 是什么？
2. SessionMessage / Transcript 怎样存储，任务怎样 Resume？
3. TodoStore 为什么需要 Update / Reminder，每 N 轮提醒为什么选这个 N，怎样决定指标？
4. Long-term Memory 怎样做 Vector Match，记忆互相冲突时怎样处理？
5. 什么场景适合 Agent、什么场景只是 Tool，Single / Multi-Agent 怎样选？
6. Reason Agent / Worker Agent 如何通信，哪些逻辑必须保持 Deterministic？
7. Agent Output Validation 失败时是否重新执行，怎样避免副作用？
8. Summary Compaction + Recent Messages 怎样组合？
9. Permission / Capability Boundary 怎样设计？
10. 多 Pod 部署下如何保持 Session / Task 路由，简单取模为什么不稳定，Consistent Hashing 怎样改善？
11. Agent Evaluation 如何同时评价最终结果和执行过程，LLM-as-Judge 怎样减少通用 Prompt 偏差？
12. 点赞系统怎样设计 DB Table、Atomicity、Hot Row 与 Sharding？

---

## S190 小红书｜Agent 开发｜一面｜面试 2026-08-09，发布 08-13｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/223fa82f976b4418b214894bd7d941fd

真人 / 第一人称证据：作者本人明确记录 8 月 9 日一面和失败状态，问题围绕实习项目、OpenManus、Harness、Multi-Agent、Memory、Redis 与 Java 连续展开。另发现一篇后发帖子题序几乎逐条一致，本批只保留这篇更早、现场证据更强的来源，后发版本按重复处理。

高价值问题：

1. 实习业务指标、上下游和本人职责是什么？
2. 为什么当前业务需要 Agent？
3. Agent 的技术框架 / Code Architecture 是什么？
4. OpenManus 怎样理解？
5. Agent Harness 是什么？
6. Multi-Agent 的性能瓶颈在哪里，Concurrency 怎样控制？
7. Short-term / Long-term Memory 怎样实现？
8. ReAct 怎样工作？
9. Planner / Executor / Critic 怎样分工，为什么 Critic 不直接并入 ReAct Loop？
10. Context 怎样切分 / Compaction？
11. Redis 常见 Data Structure 与底层实现是什么？
12. Java Class Loading 怎样工作？
13. Agent 如何做自动优化广告投放等闭环任务？
