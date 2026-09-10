# Batch 10 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批继续严格执行统一准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场痕迹 + AI Application / Agent 目标岗位 + 正文稳定可核验 + 非转载 / 非合集 / 非重复 = HUMAN-A**。
>
> **平台一视同仁。** 牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客或其他公开来源都执行同一门槛；平台只影响核验难度，不影响准入标准。
>
> 一旦来源与岗位通过 Gate，就保留整场真实问题。Python、FastAPI、Backend Engineering、MySQL、Redis、Vector DB、LLM Foundation、RAG、Agent Harness、System Design 以及实际出现的 OS / Network / MQ / Concurrency / Coding 均一视同仁，不只摘 Agent 名词。
>
> 去重固定使用三层：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。问题只做研究所需的简洁转述，不复制第三方正文，也不把合理推导写成“面试官真实问过”。

---

## S197 百度｜Agent 开发｜日常实习一面｜面试 2026-09-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60

真人 / 第一人称证据：作者说明前一晚投递、第二天早上即约面，整场约 45 分钟；明确记录自己尚未做完整 Observability、LC297 现场没写出来等状态，问题围绕本人 Agent / RAG 项目连续追问。

高价值问题：

1. Hybrid Retrieval 怎样组合稀疏 / 稠密召回，RAG Chunk Granularity 如何定？
2. Coding Agent 是完全自研还是基于开源框架，核心改动在哪里？
3. Tool Layer 的 Executor / Fallback 怎样设计？
4. 项目中最难的工程问题是什么，最后怎样解决？
5. Long-term Memory 怎样存储、更新和召回？
6. MCP `stdio` 与 Streamable HTTP 的差异是什么，音视频等流式场景是否适合？
7. Agent Task 被中断后怎样 Resume？
8. 黑盒 Agent 卡住时怎样通过日志 / Trace / 状态判断停在哪里？
9. Multi-Agent 为什么需要，以及怎样分工？
10. Coding：二叉树序列化 / 反序列化。

---

## S198 美团｜AI 后端开发｜一面｜面试 2026-09-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/9b94f595d15148869e0334029b5ddb67

真人 / 第一人称证据：作者以本人一面复盘发布，明确写有两处问题被问住，并记录面试官指出其项目若干细节考虑不够；问题从 Agent / RAG 项目继续追到 MySQL、支付幂等、AI Coding 与算法。

高价值问题：

1. PHP API 迁移到 Java 后，怎样验证行为和数据一致？
2. Agent 项目整体架构是什么，数据库和 RAG 分别承担什么职责？
3. Tool Registry 为什么做 Singleton，Singleton 在当前场景解决了什么问题？
4. MySQL Slow Query 怎样排查，Full Scan / Index Invalid 常见原因是什么？
5. 支付请求被 Replay / Duplicate 时如何保证幂等？
6. AI Coding 生成订单详情页时，怎样约束生成结果并验证可上线？
7. Coding：数组第 K 大及复杂度分析。

---

## S199 小红书｜Agent 服务端开发｜秋招一面｜面试 2026-09-08｜HUMAN-A

来源：https://www.nowcoder.com/discuss/926917172448759808

真人 / 第一人称证据：作者明确记录 9 月 8 日本人一面、没有充分准备以及后续失败结果，并以“发面经攒人品”发布；问题包含 MCP Protocol、Agent Conversation Schema 和现场 Coding。

高价值问题：

1. SSE 与 Streamable HTTP 的核心差异是什么？
2. 一个 Agent Backend 如何同时适配 `stdio`、HTTP、SSE、Streamable HTTP 等 Tool / MCP Transport？
3. MCP 不同版本之间如何做兼容？
4. ChatGPT / Agent 类产品怎样设计 Conversation 与 Message 数据模型？
5. Agent Session 中哪些状态应落库，哪些适合缓存？
6. Coding：Longest Increasing Subsequence。

---

## S200 小红书｜AI 后端开发｜一面｜面试 2026-08-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e07702037462474596f83b57f0d0ce72

真人 / 第一人称证据：作者记录约 1 小时一面，多次写到面试官指出回答“没答到点”，LRU 因时间不足只讲思路，评论区后续更新已约二面。整场从高并发缓存一路进入 Agent / RAG，基础与 AI 项目同场深问。

高价值问题：

1. 热门商品单 Key 面临十万级 QPS 时，怎样设计 Cache Architecture？
2. Cache Penetration / Breakdown / HotKey 分别怎样发现和治理？
3. Redis 与 MySQL 的 Cache Consistency 怎样处理？
4. Redis TTL / Eviction Policy 怎样选？
5. Distributed Lock 的 NX / EX、Watchdog、Lock TTL 分别解决什么问题？
6. Redis ZSet / SkipList 的底层结构与复杂度是什么？
7. MySQL Composite Index 在 `user_id + ORDER BY create_time` 场景怎样设计，Deep Pagination 怎样优化？
8. MVCC、Isolation Level 与 Phantom Read 怎样理解？
9. Agent 与普通 Chatbot 的差异是什么，核心模块有哪些？
10. ReAct 与 Plan-and-Solve 怎样取舍？
11. RAG 的 Chunk / Retrieval / Reorder / Evaluation 与 Dataset 怎样设计？
12. Agent Memory 在什么时机写入和召回？

---

## S201 Bilibili｜Coding Agent / Agent 开发｜日常实习一面｜发布 2026-08-28｜HUMAN-A

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

## S202 Bilibili｜Agent 开发｜技术二面｜2026 年秋招 / 实习季｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/794d53d2d5b4437eb47cb606910c8fa1

真人 / 第一人称证据：作者明确记录本人二面已通过、面试官交流友好、整场约 30 分钟；问题从 AIGC / 前后端继续进入网络、Redis、Agent Architecture、Skill、MCP 与 Coding Agent Tooling。

高价值问题：

1. AIGC Video Product 的完整业务流是什么？
2. 前端 / Mobile 与 AI Backend 怎样协作？
3. Python 是否能胜任当前 Agent 工程，语言取舍是什么？
4. TCP / HTTP 抓包怎样分析，UDP 与 TCP 的差异是什么？
5. SQL Index 在什么情况下会生效 / 失效？
6. Redis HotKey / BigKey 怎样定位和治理？
7. Git Merge 与 Rebase 的差异是什么？
8. Agent Architecture 怎样拆模块，Dify / LangChain 二次开发有什么边界？
9. AI Coding Agent 常用哪些 Tool？
10. ReAct 与 Plan 模式怎样选择？
11. 好的 Skill / Prompt 怎样设计？
12. MCP 与 Function Calling 的区别是什么，FastMCP 怎样使用？

---

## S203 第四范式｜Agent 开发实习生｜一面｜面试 2026-03-13｜HUMAN-A

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

## S204 科大讯飞｜Agent 开发｜一面｜面试 2026-03-04｜HUMAN-A

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

## S205 科大讯飞｜AI 应用 / Agent 方向｜技术面｜发布 2026-05-14｜HUMAN-A

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

## S206 字节跳动｜AI 应用开发｜一面 + 二面合并场｜面试 2026-04-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c5947496fc29440883611173478dc257

真人 / 第一人称证据：HR 为加快流程把一面、二面面试官安排在同一场；作者还记录面试官现场设备、评论区解释自己没有录音、只能凭记忆复盘等非常具体的现场痕迹。

高价值问题：

1. DAG Orchestration 怎样设计？
2. 多个 Agent / Model 在 DAG 中分别承担什么职责？
3. LangGraph 怎样建 Graph / State？
4. Agent / RAG Evaluation 与 Dataset 怎样构建？
5. Semantic Chunk 怎样实现？
6. Fine-tuning / RL 在什么情况下才值得用？
7. HNSW 的核心检索思想是什么？
8. 多文件输入怎样组织？
9. ThreadLocal 怎样工作？
10. LangChain / LangGraph Checkpoint 解决什么问题？
11. Agent Harness 应如何理解？
12. Coding：Water Jug、Ugly Number 等现场题。

---

## S207 字节跳动｜Agent Full-stack｜一面｜发布 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b62416eaa3764a9ba46269c0058019fd

真人 / 第一人称证据：作者面后次日以“凉经 +1”复盘；问题从生成模型 / SQL 进入 Tool Calling、MCP、Context、RAG、Memory、Multi-Agent 和 Coding，整场高度贴合 AI Full-stack。

高价值问题：

1. UTBench / Model Evaluation 怎样判断生成模型效果？
2. SQL 多表查询与 Slow Query 怎样优化？
3. Tool Calling 的基本机制是什么，还有哪些外部能力接入方式？
4. Agent 怎样决定调用哪个 Tool，MCP 在其中承担什么职责？
5. Full Context 太大时如何裁剪 / Compaction？
6. RAG / Embedding / Vector Retrieval 怎样工作？
7. Agent Memory 怎样管理？
8. Multi-Agent 如何通信、共享 Context 与 Task State？
9. Multi-Agent Workflow / Generation Quality 怎样评估？
10. Coding：Merge Intervals、带 I/O 约束的 LRU。

---

## S208 Moka｜AI 后端开发｜二面｜发布 2026-04-02｜HUMAN-A

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

## S209 钉学科技｜FDE / Agent 应用开发实习生｜一面｜面试 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c837307a81854e208eea037766f0bdcf

真人 / 第一人称证据：作者记录面试官反馈尚可但数日没有后续；问题围绕 Supervisor + Sub-agent、Hybrid Retrieval、Checkpoint / HITL 与 MySQL / Redis State Consistency 深挖，实际职责通过 Role Scope Gate。

高价值问题：

1. Parallel Sub-agent 怎样分配 Prompt / Tool？
2. Supervisor 合并冲突结果时怎样确定 Priority？
3. Vector + BM25 的 Hybrid Retrieval 在真实 Case 中怎样工作？
4. Tool Retry 超过上限后怎样 Fallback？
5. LangGraph Checkpointer 需要保存哪些字段？
6. HITL 等待人工过久时怎样 Timeout / Resume？
7. MySQL 与 Redis 中 Task State 不一致时怎样修复？
8. Resume 后切换模型会不会破坏任务一致性？
9. MCP 与 Function Calling 的边界是什么？
10. LangChain 与 LangGraph 怎样选，Graph Node / Edge / State 分别是什么？

---

## S210 腾讯｜AI 应用开发｜一面｜面试 2026-07-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a02baa2ac6634904992561494a1746a4

真人 / 第一人称证据：作者本人面后发布、记录迟迟没有后续并判断可能失败；问题重点不在背名词，而在 Prompt / RAG / Fine-tuning / Workflow / Agent 的边界以及 Production Metrics、Cost 与 Rollback。

高价值问题：

1. Prompt、RAG、Fine-tuning、Workflow、Agent 分别解决什么问题？
2. 为什么很多业务不应该一上来 Fine-tune？
3. 为什么复杂任务也不一定都要用 Agent，什么时候固定 Workflow 更好？
4. Context Engineering / Trimming 怎样做？
5. AI Application 上线后看哪些 Production Metrics？
6. Model / Tool 异常怎样做 Degradation？
7. Cost 怎样控制？
8. Prompt / Model / Index 更新怎样 Rollback？
9. Agentic RAG 与 One-shot RAG 有什么差异，哪些场景固定 RAG 更合适？
10. Agentic RAG 常见 Bad Case 是什么？
11. 怎样给 Agent 设定 Latency / Cost Bound？

---

## S211 金山办公｜AI 全栈开发｜一面｜发布 2026-09-09｜HUMAN-A

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

## S212 字节跳动｜Agent 开发｜日常实习一面｜发布 2026-09-09｜HUMAN-A

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

## S213 字节跳动｜大模型应用开发｜日常实习二面｜发布 2026-03-21｜HUMAN-A

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

## S214 字节跳动｜大模型应用开发｜一面｜发布 2026-03-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/95b8c6edf3ad46818b94605675a12089

真人 / 第一人称证据：这是与 S213 不同候选人的独立场次；作者以本人项目为主线连续回答 RAG、Agent、FastAPI、Python Concurrency 与 Coding，信息密度很高。

高价值问题：

1. Recursive Character Splitter 与 Fixed Chunk 有什么差异？
2. Milvus Collection 与 Partition / Metadata Filter 怎样使用？
3. Counseling Agent 中 Reflection 怎样实现？
4. 工业图纸类 Hallucination 怎样通过 Prompt / Post-processing 控制？
5. Function Calling 从模型 JSON 到代码执行再回填结果的完整过程是什么？
6. vLLM PagedAttention 怎样理解？
7. FastAPI Middleware 与 Dependency Injection 的差异是什么？
8. `multiprocessing` 与 `threading` 怎样选择？
9. `asyncio.gather` 与 `as_completed` 有什么差异，Timeout / Fallback 怎样处理？
10. Context Overflow 除了直接 Truncate 还能怎样治理？
11. Multi-Agent State 怎样同步？
12. A2A Communication 怎样避免递归对话 / 无限互调？
13. Coding：LRU。

---

## S215 字节跳动｜AI 应用开发｜一面 + 二面｜2026-05-12 / 05-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/61aa7e8d56ca4eb4a5a873512a72d616

真人 / 第一人称证据：作者给出 5 月 7 日 HR、5 月 12 日一面、约 30 分钟后收到二面邀请、5 月 15 日二面、失败后又被其他部门捞起的完整时间线。目标 AI 应用岗里 MySQL / Redis 被连续深问，二面再进入业务价值与 AI 使用。

高价值问题：

1. Database 到什么规模需要做 Sharding，怎样优化？
2. MySQL Index 为什么会失效，为什么“用了 Index”仍可能很慢？
3. B+Tree 与 Slow Query 排查怎样解释？
4. Redis Master-Slave / Sentinel / Cluster 如何实现 High Availability？
5. Redis 与 MySQL 怎样协同？
6. Vibe Coding / Skill / Agent Paradigm 如何理解？
7. 二面如何解释真实业务 Flow、用户价值、风险和性能？
8. 简历中的 Index Optimization 约 20% 提升是怎样测出来的？
9. Back-to-table 为什么可能产生 Random I/O，怎样优化？
10. 怎样设计 Bounded Blocking Queue？
11. 现场代码出现 Bug 时怎样定位并讨论？
12. 日常怎样使用 AI Tool，效率提升如何量化？

---

## S216 字节跳动抖音｜AI 全栈开发｜多轮流程｜2026-05-27～06-09｜HUMAN-A

一面来源：https://www.nowcoder.com/discuss/894189820371554304

三面来源：https://www.nowcoder.com/discuss/894192244872257536

真人 / 第一人称证据：同一候选人持续更新招聘流程；三面 6 月 9 日约 1 小时 6 分钟，属于明显压力面，要求本地代码屏幕共享，次日 HR 通知失败。多轮从 ReAct / Memory 进入 Java / JUC 与真实代码检查。

高价值问题：

1. ReAct 的执行过程是什么，为什么容易 Dead Loop？
2. 如何用多层策略防止 Agent 无限循环？
3. Atomic State Machine 怎样约束 Agent 状态迁移？
4. Short / Working / Long-term Memory 怎样分层？
5. Memory Retrieval 怎样避免混淆和错误召回？
6. 多模型 / Model Routing 怎样设计？
7. Java ClassLoader / Parent Delegation 怎样工作？
8. JUC 常见并发原语怎样使用？
9. AI Tool / Agent 项目真正解决什么目标？
10. Knowledge Card / Short-term Memory 怎样抽取并注入 Final System Prompt？
11. Prompt 中为什么加入 Positive / Negative Example？
12. LLM Prediction Principle 怎样解释？
13. 项目最难的技术点是什么，代码层怎样证明本人贡献？

---

## S217 京东｜AI Agent 开发实习生｜二面｜面试 2026-04-09｜HUMAN-A

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

## S218 曹操出行｜Agent 开发实习生｜一面｜面试 / 发布 2026-08-17｜HUMAN-A

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

## S219 拼多多｜AI Agent｜提前批一面｜面试 2026-08-17，发布 08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/328260668ec94ebda5c84de205d13a58

真人 / 第一人称证据：作者写明前一天参加双机位一面并“攒人品”期待通过；问题从 LLM API Failure 连续追到 Memory / Context，再进入 Coding。

高价值问题：

1. LLM API Call 失败有哪些常见原因？
2. 怎样判断调用成功，以及怎样进一步定位失败在哪一层？
3. 除了 Rate Limit，还有哪些可能导致模型服务异常？
4. Agent Memory 不足时怎样扩展？
5. 多个 Role / Persona 的 Memory 怎样隔离？
6. User Memory 与 Role Memory 怎样区分？
7. Conversation History 与 Context Window 的关系是什么？
8. Coding：Same Tree 等现场算法题。

---

## S220 Insta360｜Agent 开发｜一面｜面试 2026-03-11｜HUMAN-A

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

## S221 滴滴｜AI Agent 后端｜一面 + 二面｜发布 2026-07-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/17ee6ae95cc44ec19b9eefadb69da6b3

真人 / 第一人称证据：作者完整记录两轮并更新“已凉凉”，问题从本人 Agent 项目一路进入 Spring、Redis、Go Runtime、MQ、MySQL、Network 与 Microservice，是真实目标 AI Backend 的完整工程链。

高价值问题：

1. Agent 项目本人负责什么，最难的点是什么？
2. Agent Core Modules / Paradigm 怎样理解？
3. Long / Short-term Memory 与 Compression 怎样设计？
4. Hallucination 怎样治理？
5. Multi-Agent Async Execution 为什么可能造成 Context Contamination？
6. Spring AOP 失效、Circular Dependency、Spring MVC、Maven Transitive Dependency 怎样处理？
7. Redis Data Structure、Single-thread Model、ZSet、Sentinel、BigKey 怎样理解？
8. Go Channel / Mutex 与 GMP Scheduling 怎样解释？
9. MQ 在系统中承担什么职责？
10. MySQL ACID / MVCC / Index 怎样工作？
11. Real-time Search、WebSocket、扫码登录怎样设计？
12. Microservice Service Discovery / Load Balancing、Nacos / Consul Heartbeat 怎样工作？

---

## S222 百度｜Go Backend / Agent 方向｜秋招一面｜发布 2026-08-28｜HUMAN-A

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

## S223 Bilibili｜AI 应用 / Agent｜一面｜面试 2026-08-16，发布 08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0df78025653d492d86cc7b7273c2a0c2

真人 / 第一人称证据：作者以本人一面复盘发布并直接写“被一面问麻了”；原帖稳定可确认其背景、Agent / RAG 连续追问与具体问法。只保留正文能够确认的真实问题，不根据上下文补写追问。

高价值问题：

1. 为什么选择 Agent 方向？
2. Agent 的 Core Modules 与普通 LLM Chatbot 有什么差异？
3. Planning / Memory / Tool / Execution 各自承担什么职责？
4. Intent Recognition 可以用 Rule、Small Model、LLM Classification 中哪些方法？
5. Zero-shot 与 Few-shot 有什么差异，Few-shot 样本较少时怎样提升稳定性？
6. RAG 的 Offline / Online 完整链路是什么？

---

## S224 小红书｜Agent 开发｜一面｜面试 2026-08-09，发布 08-13｜HUMAN-A

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

---

## S225 小红书｜AI 后端开发｜一面｜面试 2026-08-13，发布 08-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/169b2d8f7a134843b114b820ee692186

真人 / 第一人称证据：作者明确写整场被“拷打 75 分钟”、没想到从算法开始，并在失败复盘中感叹基础仍然非常重要；目标 AI Backend 场次对 LRU、秒杀、Redis、MQ、MVCC 连续深问，正好验证基础工程在 AI 岗中的真实权重。

高价值问题：

1. LRU 为什么采用 HashMap + Doubly Linked List，为什么不是单链表，还有哪些 Eviction Policy？
2. Flash Sale / 秒杀系统有哪些核心并发问题？
3. RocketMQ Transaction Message 怎样工作？
4. Redis Lua 为什么能保证一段逻辑原子执行？
5. MQ 在秒杀链路里承担什么职责？
6. Redis 扣减库存后，怎样把最终结果反馈给用户？
7. Redis 与 DB 怎样保持最终一致？
8. Optimistic Lock 怎样解决并发更新？
9. Redis Set / 常见 Data Structure 的底层实现是什么？
10. ZSet SkipList 的复杂度是什么？
11. MySQL MVCC 怎样实现并发读写？

---

# 本轮明确排除 / 去重

Batch 10 扩大搜索时，以下内容继续保持 **零贡献**：

- 任何平台上的标准答案、题库、合集、SEO、课程导流、付费专栏、粉丝投稿和 AI 自动面试；
- CSDN / 51CTO / 聚合站上同一份“多年经验、多家公司大模型面经”的跨站复制内容；平台本身不被排除，但这些具体页面不满足候选人本人 / 非转载要求；
- Bilibili / CSDN 等平台中的“100 问”“全套面试题”“完整答案”等教学内容；
- 月之暗面 AI-Native Desktop 等岗位高度匹配但正文过度标准化、候选人现场状态不足的帖子；
- MiniMax 等只有很少问题、缺乏足够第一人称与现场链的边缘来源；
- 腾讯 WXG 某 Agent 帖经日期核验实际为 2025 年，排除出 2026 样本；
- 小红书一篇 8/12 / 9 月后发 Agent 帖与 S224 8/9 原帖题序几乎逐条一致，按后发近似复制处理；
- 字节 4 月存在多个问题序列高度一致的“AI 后端”版本，只保留能够确认更强现场 / 招聘流程证据的独立来源；
- 只有标题带“AI”、整场本质为普通后端且没有 AI Application / Agent 实际职责证据的面试；
- 只能通过 Search Snippet 看见问题、无法稳定核验正文 / 作者 / 时间线的线索；
- 同一候选人的同一招聘流程多轮继续合并计数，不按 URL 数量扩张样本。

# Batch 10 观察

本批新增 `S197–S225` 共 **29 个 HUMAN-A 来源**，当前干净核心样本达到 **225 个**。

本轮最重要的信号：

1. **“从 Python / Backend 到 Agent Harness 全链路一视同仁”得到更强真人证据。** 小红书 AI 后端、滴滴 AI Agent 后端、字节 AI 应用 / 大模型应用、科大讯飞 Agent、金山 AI 全栈等目标岗位都在同一场里混合考察 Redis / MySQL / MQ / OS / Network / Concurrency 与 RAG / Agent / Harness，不需要也不应该引入普通后端面经来“补基础题”。
2. **Python / FastAPI / Async 直接出现在目标岗位里。** FastAPI Middleware vs Dependency、`asyncio.gather` vs `as_completed`、Process / Thread / Coroutine、PDF I/O / CPU Workload 的并发模型选择等，说明 Python Service Engineering 是 AI Application Skeleton 的正式组成，而不是外围知识。
3. **Agent Harness / Runtime 越来越像可控软件执行系统。** Session / Transcript Resume、TodoStore Reminder、LTM Conflict、Skill Progressive Disclosure、Shell Permission、Context Compaction Verification、Multi-Pod Session Routing、Consistent Hashing、Sub-agent / Tool State 都是独立真人追问。
4. **RAG 继续从“会搭链路”走向参数、故障与证据。** Milvus Collection / Partition、Dense / Sparse、Top-K、Rerank、Incremental Index、No-answer Boundary、HyDE、Semantic Chunk、Hybrid Retrieval 与 Evaluation 被持续问到。
5. **项目验真仍然是最强区分度。** 面试官会追 Business Metric、上游 / 下游、本人职责、为什么用 Agent 而不是 Script / Workflow、性能指标怎样测、AI Coding 生成代码怎样验收；只背框架定义越来越难通过连续追问。
6. **语义去重的重要性继续上升。** 本批抓到小红书后发近似逐题复制、字节同题多版本；URL 不同远远不能证明是独立 HUMAN-A，必须继续依赖题序 / 项目语义和作者时间线。
7. **平台多元化与质量门槛不冲突。** 本轮继续搜索 Bilibili、CSDN、个人博客等公开来源；最终是否进入只由 HUMAN-A Gate 决定。某平台本轮通过的来源少，不代表平台被降权，而是当前可稳定核验的高质量真人原帖供给不同。
8. **仍未达到来源饱和。** 在已有 196 个 HUMAN-A 后，本批精确搜索仍新增 29 个独立来源；泛搜索重复 / 整理比例继续升高，但精确公司 / 岗位 / 月份 / 轮次和企业 / 话题页回溯仍有明显产出。

停止条件不变：只有连续多轮跨公司、岗位、月份、轮次和平台扩大 Recall 后，**新增 HUMAN-A 的绝对数量与占比都持续接近零**，连精确公司 / 轮次 / 作者页搜索也难以发现新来源，同时新增问题模块和追问深度稳定收敛，才进入最终收尾。当前 225 个样本仍未达到停止点。
