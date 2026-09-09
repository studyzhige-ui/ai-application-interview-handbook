# Batch 03 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 本批继续执行固定准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 本轮重点扩大企业页、话题页、搜索索引和近期帖子召回，并对清洗前见过但未进入当前干净基线的来源重新从原帖核验。合集、标准答案、自动面试、AI 测开、传统后端仅顺带问 AI、无法验证正文的平台线索仍全部排除。
>
> 问题均为简洁转述，只保存面试研究所需信息，不复制第三方正文。

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

## S033 小红书｜Agent 服务端开发实习｜一面｜面试 2026-09-08｜HUMAN-A

来源：https://www.nowcoder.com/discuss/926917172448759808

真人 / 第一人称证据：作者明确写明 9 月 8 日面试及“已挂”，记录自我介绍、实习/项目拷打、场景题、手撕与反问，并在评论区说明“发面经攒人品”。

高价值问题：

1. SSE 与 Streamable HTTP 的通信语义和适用场景有什么区别？
2. Agent / MCP 服务如何同时适配 stdio、HTTP、SSE 与 Streamable HTTP？
3. MCP 不同版本之间如何设计兼容层和升级策略？
4. 类 ChatGPT 对话 Agent 的 Session 表应该保存哪些核心字段？
5. Message 表如何建模角色、顺序、状态、Tool Call / Tool Result 等数据？
6. Coding：最长递增子序列。

---

## S034 百度｜Agent 开发日常实习｜一面｜面试 2026-09-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60

真人 / 第一人称证据：作者明确写明 9 月 7 日面试，记录第一次大厂日常实习面试、约面速度、45 分钟时长、自己没做 Observability、Hard 题没写出等现场状态。

高价值问题：

1. Hybrid Retrieval 实际由哪些检索方式组合？
2. RAG 文档 Chunk 粒度如何通过数据或评测确定？
3. 自研 Coding Agent 相比开源 Agent 的优势应该如何证明？
4. Tool Layer 的“兜底”具体做什么，Tool Executor 的职责如何拆？
5. Long-term Memory 如何实现和维护？
6. MCP stdio 与 Streamable HTTP 如何实现，二者如何选？
7. Agent 执行到一半中断后如何恢复继续运行？
8. 如何通过日志 / Trace 知道 Agent 当前执行到哪里、卡在哪里？
9. Multi-Agent 的职责和协作方式如何设计？

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

## S036 字节跳动｜AI 应用开发（中国交易与广告）｜一面｜面试 2026-08-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b34f6902e8544fe2953696ed52e49dba

真人 / 第一人称证据：候选人明确记录 1.5 小时真人面试、部门方向和最终一周后挂掉的状态；问题按 Agent → Java / Redis / MQ / 网络 → SQL / 并发自然展开。

高价值问题：

1. 最小 Agent Loop 如何描述？
2. 长时间运行的 Agent 如何支持用户主动 Cancel，并正确停止后续副作用？
3. Agent Runtime 中常见 Message 类型应该怎样组织？
4. Short-term / Long-term Memory 与 Context Window 如何分层？
5. Redis 分布式锁如何实现安全续租？
6. RocketMQ Delay Message 适合哪些异步任务场景？
7. Redis 单线程执行模型、I/O 多路复用、NIO / Reactor 应如何联系起来？
8. 配置中心如何动态刷新，配置中心不可用时怎样回退？
9. 同一个 Key 的任务串行、不同 Key 并行的 Executor 如何设计？
10. SQL 与后端并发基础如何与 Agent Runtime 连接？

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

## S042 MINISO 名创优品｜Agent 开发实习｜一面｜发布 2026-08-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f844a4ac20be44bc9b3f756bd0ebb84c

真人 / 第一人称证据：候选人以实习面试记录发布，并明确更新“一面已过、等待后续”；问题围绕本人 Multi-Agent / Workflow 项目持续追问。

高价值问题：

1. 为什么把复杂 Workflow 拆成多个 Subgraph，State 如何在主图 / 子图之间流动？
2. 外部任务已成功但写 Checkpoint 前宕机，恢复后怎样避免重复副作用？
3. Skill 从 Bad Case 学习时，如何防止错误经验污染后续任务？
4. ReAct 与 Plan-and-Solve 如何在同一 Agent 中分工？
5. 流程编排型与自主规划型 Multi-Agent 有何差异？
6. 大量信息在 Agent 之间传递时怎样防止 Context 丢失与 Token 爆炸？
7. ReAct 执行发生偏移时如何纠正？
8. Tool Result 如何压缩，同时保留权限、注入防护和校验所需信息？

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

## S044 字节跳动抖音｜AI 全栈开发｜一面｜面试 2026-05-27｜HUMAN-A

来源：https://www.nowcoder.com/discuss/894189820371554304

真人 / 第一人称证据：作者明确记录面试日期、42 分钟时长、一面当天约二面，并最终更新“三面已挂”；正文保留哪些细节忘了、哪些问题接住了等现场状态。

高价值问题：

1. ReAct 的执行流程是什么，Agent 为什么可能陷入死循环？
2. 三层防护机制 / 原子状态机分别解决怎样的 Runtime 风险？
3. 三层 Memory 为什么存在，Memory 怎样召回并避免错误注入？
4. Long-term Memory 应保存什么，边界如何定义？
5. Multi-model 如何组织和切换？
6. Java 类加载器、双亲委派与类加载完整过程如何解释？
7. AI 全栈岗位为什么会同时追 Agent Memory 与 JVM / JUC 基础？

---

## S045 腾讯｜AI 应用开发｜一面｜面试 2026-07-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a02baa2ac6634904992561494a1746a4

真人 / 第一人称证据：作者明确给出面试日期和岗位，并在正文更新“目前没消息、估计凉了 / 发面经攒人品”。

高价值问题：

1. Prompt、RAG、Fine-tuning、Workflow、Agent 应该依据什么选择？
2. 为什么复杂任务并不一定适合 Agent？Workflow 与 Agent 的边界是什么？
3. Token / Context Window 对应用工程意味着什么？
4. Context 被截断时优先如何恢复关键事实？
5. AI 应用上线前应该重点看哪些效果、延迟、成本和可靠性指标？
6. 如何设计 Degrade / Fallback？
7. Prompt、Model、Retrieval Index 变化后如何做版本回滚？
8. Agentic RAG 与固定单次 RAG 的边界是什么？
9. 如何限制多轮补检的 Latency 和 Cost？

---

## S046 阿里｜AI 应用开发｜实习一面｜发布 2026-05-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/038bad2882114c64bc6166eb716e5fce

真人 / 第一人称证据：候选人直接写“给我面没招了，发点面经攒人品”，问题从本人实习 / Agent 项目一路进入 AI Coding、Java 并发、Redis / MySQL 一致性。

高价值问题：

1. Agent Workflow 如何实现，框架编排和代码控制如何选？
2. Agent 的扩展性如何设计？
3. 图文 Retrieval / Semantic Store 如何实现？
4. Tool Calling 与 Memory Management 如何落地？
5. OpenClaw 等 Agent 产品与自研 Agent 有哪些系统差异？
6. AI Coding 从拿到需求到交付，哪些环节必须人工验收？
7. 如何给 AI 提供高质量 Context，并对生成代码做功能 / 安全 / 性能 Review？
8. 并发库存 / 订单类问题如何保证正确性？
9. Redis Session 与数据库如何保持一致？
10. ThreadLocal、MySQL Composite Index 等后端基础如何解释？

---

## S047 FOSHO｜AI 应用开发 / Agent 开发｜一面｜面试 2026-07-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d95927b94e994681beee22975766721e

真人 / 第一人称证据：作者明确写明公司、日期、AI 应用开发一面、30 分钟以及“零八股、全程问项目”，并以发面经攒人品形式发布。

高价值问题：

1. Go / Java / Python 的真实项目使用深度如何说明？
2. 长视频从上传、ASR / 转写、摘要到问答的完整异步链路如何设计？
3. 大文件与长视频如何做分片上传和断点续传？
4. 用户提问后如何 Retrieval 相关视频片段并构造 Prompt？
5. 当前单视频问答如何扩展成多视频知识库与跨视频 Retrieval？
6. Coding Agent 当前实现了哪些能力？
7. Coding Agent 的 Context Management 如何设计？
8. 为什么选择自研 Runtime 而不是现成 Agent Framework？
9. 为什么 Coding Agent 选择 Go，语言与 Runtime 需求如何匹配？

---

## S048 哔哩哔哩｜Agent 方向｜二面｜面试 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/discuss/919630524673458176

真人 / 第一人称证据：候选人明确给出二面日期、45 分钟时长，记录面试官压力感以及反问时对 A2A 项目价值的直接反馈。

高价值问题：

1. 实习项目中最有技术难度的问题是什么？
2. 负载均衡如何实现？
3. A2A 与当前项目的匹配度如何判断？
4. 不同 Agent 产品的 Memory 机制有哪些差异？
5. 在已有 Agent 上扩展与从零自研 Runtime 如何选择？
6. Coding 以外还有哪些场景值得使用 Agent？
7. 如何验证 Agent 的确定性结果？Hooks 在 Verification 中承担什么角色？
8. 存在 Bad Case 时如何确定 Agent 优化方向？
9. Workflow 与一个整体自治 Agent 的边界是什么？
10. Coding：合并区间。

---

## S049 哔哩哔哩｜Agent 开发｜二面｜发布 2026-08-28｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/794d53d2d5b4437eb47cb606910c8fa1

真人 / 第一人称证据：作者明确记录“过了”、面试官较随和、时长半小时以上；问题按语言 / 网络 / DB / Redis / Git → Agent / MCP / RAG → 手撕自然展开。

高价值问题：

1. Python 等语言的工程特点如何比较？
2. TCP / HTTP 抓包、UDP 特性与适用场景如何解释？
3. SQL 如何判断是否走索引？Redis HotKey / BigKey 如何治理？
4. Git merge 与 rebase 如何选择？
5. Agent 项目的整体架构和业务目标是什么？
6. Dify / LangChain 二次开发与自研 Agent Runtime 的边界是什么？
7. ReAct 与 Plan 如何选择？
8. 一个高质量 Skill / Prompt 最关键的约束是什么？
9. MCP 与 Function Calling / Tools 的职责边界是什么，MCP Server 如何实现？
10. RAG 如何 Chunk / Vectorize，什么场景应该使用？

---

## S050 字节跳动｜AI 应用开发｜一面｜面试 2026-07-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3e22dc2df03d4227ab70ea9c2d896086

真人 / 第一人称证据：候选人明确写“面试完来发面经”、日期和岗位，并逐题记录自己“没听懂产出 / 答得不好 / 想不到”等现场回答状态。

高价值问题：

1. 项目中最大挑战如何量化产出，而不是只描述技术动作？
2. Hallucination 如何从 Prompt、Tool、RAG、Fine-tuning 等层治理？
3. Agent Short-term / Long-term Memory 如何实现？
4. 从零设计 Agent 时应该拆哪些核心模块？
5. API Timeout / Error 如何分类 Retry、Fallback 或 Degrade？
6. 哪些失败可以让 LLM 自我修复，哪些必须由 Runtime 确定性处理？
7. Token 消耗异常时如何从 Context、Tool Result、循环步数和重复调用排查？

---

## S051 机械星球（要务科技）｜AI 应用开发｜一面｜面试 2026-07-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e07bd10a97f84ece9f2ce6298b2ca72c

真人 / 第一人称证据：作者明确给出 7 月 14 日 AI 应用开发一面，并以个人凉经发布；正文大量记录自己当场怎么答、哪些不会、哪里尴尬以及最后反问。

高价值问题：

1. 练手 AI 项目是否真实部署、是否有用户，如何证明项目不是 Demo？
2. RAG 项目的真实不足和质量优化难点是什么？
3. LangGraph / Multi-Agent 项目中信息传递与输出格式如何治理？
4. AI 全栈服务的跨域、Auth / Token 与 Controller 权限如何设计？
5. Nacos 注册发现、配置加载与热更新如何工作？
6. Linux / Cloud Server 的部署和监控能力如何说明？
7. 单体系统改造为微服务时，Service Discovery、Gateway、MQ、Cache、Thread Pool 与 SQL Optimization 如何组合？
8. 企业对 Agent / AI Coding 的真实使用边界是什么？

---

# 本轮明确排除

搜索过程中没有因为“题目看起来高级”而降低准入。明确排除了：

- 牛客整理专栏 / 面经总结页，只用来定位候选人原帖；
- CSDN 中“帮粉丝复盘 + 高分答案 + 资料导流”的二次文章；
- 与已有原帖高度一致但作者不一致、疑似转载的跨平台内容；
- AI 自动面试、测开岗位、纯训练 / 大模型算法岗位；
- 传统后端只因为简历有 Agent 项目而被问几道 AI 的场次；
- 只有搜索摘要、无法打开原正文或缺少第一人称现场痕迹的帖子。

# Batch 03 观察

本批新增 `S032–S051` 共 **20 个 HUMAN-A 来源**，当前干净核心样本达到 **51 个**。

这批最明显的信号是：

1. **Agent Harness / Runtime 继续快速变深**：Tool Executor、MCP Transport、Checkpoint Crash Window、Sandbox、Compaction Verification、Coding Verification、权限与越权访问都来自真人面试。
2. **基础工程并没有减少**：Python dict / async、MySQL Index / MVCC、Redis Lock / BigKey / Cache、MQ、HTTP / TCP、OS / Concurrency 仍与 Agent / RAG 同场出现。
3. **FastAPI / Service Runtime 类能力正在以协议与服务设计形式出现**：SSE、Streamable HTTP、Session / Message Schema、异步任务、断点续传、连接与流式协议需要单独系统学习。
4. **高质量来源数量仍未接近饱和**：仅一轮新的扩大召回就又找到 20 个互不重复的 HUMAN-A 样本，且公司、轮次和知识深度仍在扩展。

后续继续保持同一标准扩大 Recall，不以每批固定数量为目标。