# Batch 03 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **20** 个正式来源。

---

## S032 百度｜Agent Harness 研发工程师｜秋招一面｜面试 2026-09-08｜HUMAN-A

来源：https://www.nowcoder.com/discuss/926928449204129792

真人 / 第一人称证据：候选人明确给出 9 月 8 日一面，正文保留“某种工程方案自己没听明白”等现场状态，问题连续围绕本人代码修复 Agent 项目深挖，并有现场代码修改题。

高价值问题：

1. Agent Harness 应如何理解，它与模型、Agent 和普通框架的边界是什么？
2. Coding Agent 的代码修复结果应该从哪些维度判定正确？
3. 多 Agent 并行修改同一个文件时，冲突、文件锁和工作区隔离如何处理？
4. Claude Code 对代码规范、并行修改与冲突控制有哪些可借鉴机制？
5. Claude Code 的 Sandbox 主要解决哪些风险？
6. 日志预处理用于降低 Token 时，如何防止根因信息被压掉？
7. 多模型参与同一任务时，如何保持上下文和输出协议连续？
8. 没有显式错误日志时，Coding Agent 如何继续定位缺陷？
9. Python 装饰器、生成器、上下文管理器和 async I/O 在 Runtime 中分别适合什么场景？

---

## S033 小红书｜Agent 服务端开发｜秋招一面｜面试 2026-09-08｜HUMAN-A

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

## S034 百度｜Agent 开发｜日常实习一面｜面试 2026-09-07｜HUMAN-A

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

## S035 字节跳动｜AI Agent 开发｜一面｜发布 2026-09-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/612a1c20eea744a288b142f5b43f57e1

真人 / 第一人称证据：问题高度绑定候选人的量化 AI Agent 项目和具体权限模型，存在项目连续追问；楼主在面后评论中直接记录自己的现场崩溃感受。

高价值问题：

1. Agent Token / 权限 Scope 如何建模，并如何在数据库层落地？
2. 高风险下单权限如何继续限制标的、金额等细粒度条件？
3. SSE 断连、心跳和重连后断点续传如何设计？
4. Agent 超时重试时如何通过 Idempotency Key 防止重复下单？
5. 为什么幂等 Key 不应该交给 LLM 自己生成？
6. Redis Lua 如何实现多维限流，Redis 故障时如何保护数据库？
7. 大量 Key 同时过期造成缓存压力时如何治理？
8. 长耗时任务为什么更适合异步执行 + SSE，而不是同步 HTTP？
9. Python dict 的 Hash、冲突处理和删除机制如何解释？
10. Coding：LRU 与 Top-K 高频元素。

---

## S036 字节跳动中国交易与广告｜AI 应用开发｜一面｜面试 2026-08-27，约 90min，后续未通过｜HUMAN-A

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

## S037 超参｜Agent 开发｜社招一面｜发布 2026-08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8e77c295f6cb4cd4b709d14804afb987

真人 / 第一人称证据：作者明确写“面完就挂了”和“感觉是想招 0-1 干的”，并以社招面试记录发布；问题集中在自己的 RAG / Agent Production 能力。

高价值问题：

1. RAG Chunk、Rerank 与噪声控制如何协同优化？
2. Hybrid Search、Metadata Filter、GraphRAG 分别解决什么问题？
3. IVF_FLAT 的索引思想与适用边界是什么？
4. Agent 之间如何通信？
5. 跨机器 Agent 如何做容灾调度和 Retry？
6. Context Compaction 如何实现？
7. 分布式 MQ、Kubernetes 与容器化如何支撑 Agent 服务？
8. tRPC 等 RPC 方案如何选型？
9. 如何阻止 Agent 越权访问其他目录？

---

## S038 字节跳动抖音｜Agent 开发｜一面｜发布 2026-04-28｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f5d39c2e78ff4cf9bdcd41977f50b038

真人 / 第一人称证据：候选人以“一面凉经 / 发面经攒人品”发布，明确记录第一次面字节被连续深挖，并有现场 Coding 设计题。

高价值问题：

1. Agent 项目采用什么执行流程，为什么这样选？
2. 模型与 Agent 的核心区别是什么？
3. Local Tool、MCP Tool、Skill 三者分别适合承担什么职责？
4. 已经有 MCP 后，为什么成熟 Coding Agent 仍会引入 Skill / Instruction 类能力？
5. Claude Code 的 Memory / Context 应如何区分？
6. 为什么 Coding Agent 读取代码库不一定依赖传统 Code RAG，而会大量使用 Repo Search / grep / Read？
7. 前沿 Memory 设计主要在解决什么问题？
8. Coding：设计 Skill 注册、发现与执行系统，读取目录配置与脚本。

---

## S039 快手｜AI 应用开发｜一面｜面试 2026-04-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/daa06f995ea74445a13de42d67f66265

真人 / 第一人称证据：作者写明公司、日期和岗位，记录“无项目无实习，全场景拷打”，并保留面试官反问阶段给出的改进建议：加强 Context Engineering / Compaction。

高价值问题：

1. Multi-Agent 常见范式分别有什么优缺点？
2. MCP 与 Skill 的核心职责如何区分？
3. Skill 的 Progressive Disclosure 如何实现？
4. Skill 放进 Agent Sandbox 后，Agent 与 Sandbox 如何通信并跨文件系统按需披露？
5. Function Calling 如何工作，怎样减少 Tool Hallucination？
6. Context Compaction 有哪些触发机制？
7. 滑动窗口摘要应该与旧摘要合并还是分层保留，如何选择？
8. Short-term Memory 什么时候应晋升 Long-term Memory？
9. 如果从零设计三层 Memory，应如何定义存储和压缩策略？
10. Claude Code 的 Memory / Context 机制如何理解？

---

## S040 原力健康｜Agent 开发｜一面｜面试 2026-06-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/2220b8371b4a49ddb3c8d62008697ed8

真人 / 第一人称证据：作者以明确日期、公司和个人“凉经”标题发布；23 个问题围绕本人 RAG 项目连续追问，并自然切到 Redis、数据结构和 Coding 基础。

高价值问题：

1. 企业知识库从原始文档到 Retrieval 的完整链路是什么？
2. Chunk 阶段有哪些可验证的优化方式？
3. 文档解析是否需要专门模型，Embedding 模型如何选择？
4. Query Rewrite 有哪些做法，Retrieval Miss 时怎样兜底？
5. Multi-way Retrieval 应如何增加检索通道并验证收益？
6. 如果用 LangGraph 编排问答系统，Node 如何拆分？
7. Redis 分布式锁如何实现？
8. Cache Penetration / Breakdown / Avalanche 怎么治理，Redis 为什么快？
9. 数据结构、设计模式与基础算法仍会怎样被追问？

---

## S041 滴滴｜Agent 方向｜一面｜发布 2026-04-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/65cdcc618b0a4d2cac65e30e5c3d71f6

真人 / 第一人称证据：候选人明确记录“一面挂、OS 八股没怎么看、秒挂”，并在评论区补充“上周面的”；问题从知识图谱 / Agent 连续进入 OS 基础。

高价值问题：

1. Knowledge Graph / Ontology 在 Agent 场景中如何使用？
2. MCP 与 Skill 有什么区别，二者如何组合？
3. 模型如何感知当前有哪些 Tool 可用？
4. Agent Runtime 与 ReAct / Orchestration 如何实现？
5. 如何治理 Agent Hallucination？
6. Agent Evaluation 与 RAG Evaluation 分别看什么？
7. 进程、线程、协程及协程实际应用如何解释？
8. Docker Container、IPC、Zombie Process 等 OS 基础为什么会在 Agent 岗出现？

---

## S042 名创优品｜Agent 开发实习｜一面｜发布 2026-08-26，已通过｜HUMAN-A

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

去重：URL 未在 `S001–S212` 出现；独特的“外部副作用已成功 + Checkpoint 前崩溃”恢复题序、作者与名创流程均未在正式来源命中。

---

## S043 法本信息｜AI Agent 开发｜一面｜面试 2026-07-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d8f5de441b7a4f7ba32164ef37cce1fc

真人 / 第一人称证据：作者明确给出公司、面试日期、岗位及面试感想“学得还不够”，17 个问题围绕自己的本地 Coding Agent 连续深挖。

高价值问题：

1. 本地 Coding Agent 从任务输入到修改代码的完整 Runtime 链路是什么？
2. 多模型 Backend 如何统一请求 / 响应、错误码与 Retry？
3. 新 Tool 从定义、注册、发现到调用的生命周期如何设计？
4. 文件不存在、命令超时、权限不足等 Tool Failure 如何分类恢复？
5. Context 压缩后如何验证当前任务没有被破坏？
6. Task Summary / File Summary / Process Note 等压缩产物如何更新和失效？
7. Long-term Memory 中过期摘要或模型错误结论如何发现并纠正？
8. 如何检测反复读文件、重复 Tool Call 等无效循环？
9. Harness 与直接调用 LLM API 的系统差异是什么？
10. Benchmark / Case / Metric 如何判断 Agent 改动确实提升能力？
11. 错误 Patch 如何回滚、验证后再尝试？

---

## S044 字节跳动抖音｜AI 全栈开发｜多轮流程｜2026-05-27～06-09｜HUMAN-A

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

## S045 腾讯｜AI 应用开发｜一面｜面试 2026-07-25｜HUMAN-A

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

## S046 阿里巴巴｜AI 应用开发｜27 实习一面｜发布 2026-05-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/038bad2882114c64bc6166eb716e5fce

真人 / 第一人称证据：作者以本人一面分享并写“给我面没招了，发点面经攒攒人品”，问题从 Agent Workflow / Retrieval / Memory 进入 AI Coding 交付、Java Concurrency、Redis/MySQL。

高价值问题：

1. Agent Workflow 链路如何实现，框架控制还是自研代码控制？
2. Agent Extensibility 怎样设计？
3. Image-text Retrieval 与 Semantic Knowledge Base 怎样构建？
4. Tool Call 与 Memory Management 怎样实现？
5. OpenClaw 与自己做的 Agent 有什么差异？
6. Python / Java 如何选择，Cursor / Claude Code 在项目中怎样用？
7. 从需求交给 AI Tool 到最终 Delivery，哪些环节必须人工 Acceptance / Review？
8. AI Generated Code 如何做功能、安全、性能 Review 与 E2E Test？
9. Java HashMap、ReentrantLock、ArrayList Concurrent Write、Exception 应怎样解释？
10. Redis Session 与数据库怎样保持一致，ThreadLocal 用户上下文是否线程安全？
11. MySQL Composite Index 怎样设计？

---

## S047 FOSHO｜AI 应用 / Agent 开发｜一面 30min｜面试 2026-07-16，发布 07-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d95927b94e994681beee22975766721e

真人 / 第一人称证据：作者明确记录 7 月 16 日本人面试、时长约 30 分钟，并说明“零八股，全程问项目”；问题来自其长视频 AI QA 与 Mini Coding Agent 两个真实项目。

高价值问题：

1. Go / Java / Python 分别在哪些真实项目里使用过？
2. Long-video Understanding 从上传到 ASR / Summary / QA 的完整链路是什么？
3. 视频转写调用什么模型 / Service？
4. Long-running Task 怎样异步处理？
5. Large-file Upload、Chunk Upload 与 Resume-from-breakpoint 如何实现？
6. 用户问问题后怎样 Retrieval 相关视频片段并组装 Prompt？
7. 系统怎样从 Single-video QA 扩展成 Multi-video Knowledge Base？
8. Mini Coding Agent 已实现哪些能力？
9. Coding Agent Context Management 怎样设计？
10. 为什么不用现成 Agent Framework，而选择自研；为什么选 Go？

---

## S048 Bilibili｜Agent 开发｜一面 + 二面（同一候选人同流程合并）｜面试 2026-08-11 / 08-13，发布 08-19｜HUMAN-A

一面来源：https://www.nowcoder.com/discuss/919630453387063296

二面来源：https://www.nowcoder.com/discuss/919630524673458176

真人 / 第一人称证据：两篇均由作者 `Bk7` 发布，学校、技术方向、岗位和时间线一致；一面为 8 月 11 日约 45 分钟，二面为 8 月 13 日约 45 分钟。作者记录一面面试官较友好、自己担心能否进入下一轮，二面又明确感受到项目价值被质疑，并记录对 A2A 等问题的现场反应。两轮属于同一候选人同一 Bilibili Agent 招聘流程，因此合并为一个 `Sxxx`。

整场技术问题：

### 一面

1. 从自己的 Agent 项目中挑一个核心设计，完整讲清业务目标、Architecture、本人职责和关键取舍。
2. 项目如何部署到 Cloud，运行环境和交付链路怎样组织？
3. Linux cGroup 解决什么资源隔离问题？
4. A2A Protocol 解决什么问题，适合怎样的 Agent Communication？
5. CI/CD 在 Agent / Backend 项目中怎样落地？
6. Context Compaction 使用什么 Strategy，压缩后怎样保证关键任务状态不丢？

### 二面

7. 实习中最有挑战的技术问题是什么，候选人具体怎样解决？
8. 实习项目中的 Load Balancing 怎样实现，为什么这样选？
9. A2A 是否真的适合当前项目，Protocol 与现有通信方式怎么比较？
10. 不同 Agent System 的 Memory 机制有什么差异，哪些信息需要持久化？
11. 面对已有 Agent，是在现有系统上扩展还是从零重做，判断标准是什么？
12. 除 Coding Agent 外，还有哪些 Agent 场景真正值得 Agent 化？
13. Agent 输出要求 Deterministic / 可验证时，怎样建立 Verification？
14. Runtime Hooks / Callback 的行为怎样测试，如何证明 Hook 正确触发且没有副作用？
15. Agent 出现 Bad Case 或整体效果下降时，怎样定位应该优化 Model、Prompt、Context、Tool、Memory 还是 Runtime？
16. 固定 Workflow 与更自主的完整 Agent 应怎样取舍？
17. Coding：Merge Intervals。

去重：历史 `S176` 为另一候选人的开源 Coding Agent 修复 / `ripgrep` / Sandbox / Skill Progressive Disclosure；`S049` 为另一候选人的 AIGC Video + Network / Redis / Dify / Tooling 场次。当前作者、项目、8/11→8/13 Timeline 和“cGroup / A2A / Compaction → Deterministic Verification / Hook Validation / Bad Case Attribution”题序均独立。

---

## S049 Bilibili｜Agent 开发｜技术二面｜2026 年秋招 / 实习季｜HUMAN-A

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

## S050 字节跳动｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3e22dc2df03d4227ab70ea9c2d896086

真人 / 第一人称证据：作者保留大量现场失败痕迹：承认项目来自网上、项目产出被面试官说没听懂、多个 Agent 问题“答得不好”、线程池设计答得差、死锁代码没写出来，最后总结自己从开场就觉得凉。

高价值问题：

1. Project Challenge 最大的是什么，怎样证明真实产出？
2. Hallucination 从 Prompt / Tool / RAG / Fine-tuning 哪些层面治理？
3. Prompt 具体怎样约束模型“不知道就不要编”？
4. Short-term / Long-term Memory 怎样实现？
5. 从零设计 Agent 需要哪些 Module？
6. API Timeout / Error 怎样恢复，是否可以让 LLM 自己参与处理？
7. Token Consumption 异常怎样排查？
8. Java ThreadPool 原理是什么，如果重新设计会怎样做？
9. JVM Class Loading 怎样完成？
10. MySQL undo / redo / binlog 与 Two-phase Commit 分别解决什么？
11. Coding：多线程 Deadlock、Singleton、Merge Sorted Arrays。

---

## S051 机械星球（要务科技）｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-16，凉经｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e07bd10a97f84ece9f2ce6298b2ca72c

真人 / 第一人称证据：作者 `Luxlord` 直接以 7 月 14 日 AI 应用开发一面凉经发布，问题中保留大量即时反应：承认三个项目都是个人练手、真实用户只是舍友；Spring / Nacos 追问时“开始憋笑”“不敢再说学过 SpringCloud”；把 Shell 听成“xue”并在面后问 AI 才确认。属于难以模板化伪造的真实答题状态。

整场技术问题：

1. 三个项目是否都是个人练手，是否真实部署、是否有人实际使用？
2. RAG 项目真实用户反馈过哪些不足？
3. RAG 项目最难的部分是什么，Spring AI 编排和 RAG Quality 分别踩过什么坑？
4. LangGraph 项目最难的地方是什么，Multi-Agent 信息传递、格式与 Hallucination 怎样处理？
5. Full-stack 开发中的 CORS / Cross-origin 怎样解决？
6. Spring Boot 类 / Bean 加载顺序怎样控制？
7. Authentication 怎样做，Token 如何在前后端传递？
8. 不同 Controller 的 Authorization / Access Control 怎样实现？
9. Nacos 作为 Registration Center 怎样使用？
10. Spring Boot 启动后怎样加载 Nacos Configuration？
11. Nacos 配置更新后如何实现 Hot Reload / Dynamic Refresh？
12. 是否使用过 Linux，实际部署服务器是什么系统？
13. 本地怎样连接和操作云端 Linux？
14. 自己的项目如何部署，Production Monitoring 怎样做？
15. 是否写过 Shell Script；候选人现场没听清术语，面后才确认？
16. 给一个 Monolith Legacy Project，怎样拆成 Microservices？
17. 拆分后 Service Discovery、OpenFeign / MQ、Gateway Auth、Nginx / Sentinel、Distributed Transaction、Cache、Thread Pool、SQL Optimization 分别放在哪里？
18. 反问：公司真实业务是否做 Agent，以及团队如何看待 AI Coding？

去重：历史中虽有大量“AI 岗 + Java / Spring”样本，但本场“练手项目是否真有人用 → Spring AI / LangGraph → CORS / Auth → Spring Boot 加载顺序 → Nacos 配置热更 → 连 Linux 系统名都没注意 → Shell 听音失误 → Monolith 改微服务”的真人失败轨迹和题序独立，URL / 作者 / 公司流程均未命中。
