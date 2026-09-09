# Batch 10 — AI Application / Agent 高质量面经（基础工程 + Runtime 纵深批）

采集日期：2026-09-09

> 本批继续同时执行两道门槛：
>
> 1. **Source Quality Gate**：优先第一人称、技术问题具体、可核验的真实面试；过滤水短视频、SEO 标准答案、模拟题库和无法追溯原场次的二次拼接。
> 2. **Role Scope Gate**：只收 AI 应用开发、Agent 开发、AI 全栈、大模型应用、AI 后端、Agent Runtime 等目标方向；不使用传统数据分析 / BI / 纯推荐算法 / 纯训练 Infra / 普通后端来补题量。
>
> 本轮同时检索了牛客之外的技术社区、知乎、短视频/视频平台等公开索引结果，但高排名结果中存在较多“完整答案 / 面试题库 / 深度解析 / 资源导流”类二次内容，未达到正式样本门槛，因此正式 Batch 仍以可稳定核验的第一人称面经为主。
>
> 对通过岗位准入的 AI 岗，仍保留整场真实问到的 Python、FastAPI、MySQL、Redis、MQ、网络、Vector DB、RAG、Agent、System Design 等问题，而不是只摘 Agent 题。

---

## S115 阿里｜AI 全栈秋招一面｜2026-08-28 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/556b3a764a614931bc5bb8a96e4f5f3f

高价值问题：

1. 项目中的 Agent 解决什么业务问题，整体架构如何拆？
2. 常见 Agent 范式如何理解，Workflow 与 ReAct 如何选？
3. Agent 效果应该用哪些指标和评测集验证，而不是只做 Demo？
4. Agent 稳定性 / Reliability 如何衡量和优化？
5. 短期记忆与长期记忆如何组织？
6. KV Cache 在大模型推理中解决什么问题，对应用端延迟和显存意味着什么？
7. Skill 很多时为什么需要渐进式加载，而不是全部注入 Context？
8. AI 全栈岗位为什么仍然要求扎实后端基础？

价值：同时强化 **Agent Architecture / Evaluation / Memory / Skill Loading**，并出现了应用工程师层面的 KV Cache 追问，进一步支持补充 LLM Runtime Foundation。

---

## S116 上海某独角兽｜AI 全栈开发｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/6468c9ab07664b15901a3470fad6115f

高价值问题：

1. 向量检索从 Query 到 TopK 的完整过程是什么？
2. Cosine、Inner Product、L2 等相似度如何选？
3. Retrieval 中 Recall / Precision / F1 应该如何理解和权衡？
4. IVF 与 HNSW 的索引思想、适用场景和调参方向是什么？
5. FAISS 索引和数据库原生向量索引如何选？
6. Bi-Encoder 与 Cross-Encoder 为什么通常分别用于召回与 Rerank？复杂度差在哪里？
7. BM25 + Vector + RRF + Rerank 的完整 Hybrid Retrieval 链路怎么设计？
8. Context 扩张如何控制，Memory 引入后如何证明真的改善效果？
9. 为什么业务要使用 Multi-Agent，而不是简单 RAG？
10. Agent 评测集和 Trace 如何帮助定位 Bad Case？

价值：Vector DB / Retrieval 密度非常高，而且从“会用索引”继续追到 **Encoder Architecture + Retrieval Metrics + Hybrid Pipeline**。

---

## S117 阿里平头哥｜AI 应用研发工程师｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/51f34fe0d0cf4b918bd45dd4ec8824a9

高价值问题：

1. AI 应用里 Redis 与 MySQL 分别存什么，如何做数据分层？
2. 缓存如何预热，服务重启后如何恢复热点数据？
3. MySQL 与 Redis 双写时如何处理一致性问题？
4. ReAct 的执行循环是什么？
5. 为什么项目选择手写 Agent 流程而不是直接依赖 LangChain？
6. RAG 从建库、检索到生成的完整链路如何解释？

价值：非常直接地说明目标 AI 应用岗位仍会把 **Redis / MySQL 数据分层与一致性** 和 Agent / RAG 放在同一场面试里。

---

## S118 深信服｜AI 全栈二面｜2026-06-23｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/7fd4389e0a0844faa4dce49ba5e5c3f1

高价值问题：

1. 多级缓存为什么这样设计，命中率、淘汰和重启恢复如何处理？
2. Redis 与 MySQL 数据冲突时，哪一层是 Source of Truth？如何恢复一致？
3. 缓存与锁的抽象如何避免复杂业务中的死锁？
4. OAuth2 / 鉴权等基础如何进入 AI 服务？
5. Agent 统计 Token Usage 时，为什么容易漏掉 Sub-agent / Tool / 子模型调用？
6. 父 Agent 连接已断开，但 Sub-agent 晚完成时，Token 与任务状态如何记账？
7. 多个 Sub-agent 并发执行时，如何避免 Usage 重复计算或漏算？
8. Token / Cost 的埋点应该放在 Model Provider、Tool Runtime、Agent Runtime 哪些层？
9. 多模型 Provider 的 Reasoning / Usage 字段不一致时如何适配？
10. RAG / Tool 调用引入的额外 Token 如何进入统一成本核算？

价值：除了缓存一致性，这份面经首次把 **层级 Agent 的 Token / Cost Accounting** 追到了生命周期、并发与 Provider Adapter 级别，是 Harness Observability 的重要新方向。

---

## S119 去哪儿旅行｜AI 全栈方向 AI 面｜2026｜原始候选人记录 / 自动化面试官｜B

来源：https://www.nowcoder.com/feed/main/detail/9cf516b3c2404100baeac52564e40709

interviewer_type：`automated`

高价值问题：

1. Java / TypeScript 等语言在 AI 全栈服务里如何选？
2. GC、三色标记、STW 等 Runtime 基础如何理解？
3. 如何让模型稳定输出满足 Schema 的 JSON？
4. Agent 场景如何从业务需求拆成 Tool / Workflow / State？
5. 长期 Memory 如何筛选、保存和召回？
6. 新旧 Memory 冲突时，时间、来源和权威级别如何排序？
7. Critic / Evaluator 如何评价 Agent 输出？
8. 幻觉如何从 Context、Grounding、Tool、Validation 等层治理？
9. Project Rules / Hooks / Code Review 等机制如何约束 Coding Agent？

价值：题目本身很有价值，但面试官为自动化 AI 系统。后续频率统计应把 `interviewer_type=human / automated` 分层，避免自动化题库结构对“真人面试高频”产生同等权重影响。

---

## S120 小红书｜PE / AI 全栈一面｜2026-03-31｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/ca5c689da55241a184b39ed4b8f04e63

高价值问题：

1. Bloom Filter 如何用于缓存穿透治理？
2. AI Coding 如何真正进入前端 / 全栈开发流程，而不是简单生成代码？
3. 如果把现有电商能力 MCP 化，Tool / Resource / 权限应该如何设计？
4. 用户画像或语义信息为什么可能需要 Vector DB，而不是全部放 MySQL？
5. pgvector / PostgreSQL 同时承载结构化数据和向量检索有什么优缺点？
6. Embedding 层在整个 AI 应用里承担什么职责？
7. Agent 是否应该直接连接数据库并执行 SQL？为什么？
8. 如果不允许模型直接碰数据库，应该如何通过受控 Tool / Service Layer 提供数据能力？
9. Function Calling、Skill、MCP 的职责如何区分？

价值：出现了一个非常重要的 Production 边界：**Agent Data Access 不应等同于“给模型数据库账号”**，需要把 AuthZ、租户隔离、审计和 SQL 安全放到 Runtime / Service 层。

---

## S121 小红书｜AI 后端开发一面｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/e07702037462474596f83b57f0d0ce72

高价值问题：

1. 大规模电商缓存体系如何设计？
2. HotKey 怎么发现，缓存与数据库一致性怎么处理？
3. Redis 过期策略、淘汰策略、分布式锁 / WatchDog、ZSet 分别如何理解？
4. MySQL 联合索引、ORDER BY、深分页如何优化？
5. MVCC、事务隔离与锁如何联系起来？
6. Agent 与 Chatbot 的核心区别是什么？
7. ReAct / Plan-and-Solve 等执行模式怎么选？
8. RAG 的完整流程、Chunk、召回、排序和评测如何设计？
9. Memory 在什么条件下写入 / 读取，而不是每轮都注入？
10. 手写 LRU 的核心结构与复杂度是什么？

价值：非常强的 **AI 后端 = Redis/MySQL 基础 + Agent/RAG** 样本，进一步证明基础工程知识不是偏题。

---

## S122 快手｜大模型应用开发实习一面｜面试 2026-08-17｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/756a5f6d2c914bf0a9edca5787bf6266

高价值问题：

1. Agent 完整流程和常见范式怎么解释？
2. Tool Call 如何落地，Tool 多时如何优化集成和选择？
3. Redis 分布式锁如何实现？
4. Kafka 如何保证消息可靠性和消费幂等？
5. SkillHub / Skill Registry 这类能力市场如何存储、审核和治理？
6. Agent 自动化运维 / 操作类系统应该如何做 Benchmark？
7. AI Coding / 浏览器扩展类应用如何验证产出质量？

价值：同时覆盖 Agent Tool/Skill、Redis、Kafka 和 Evaluation，是目标岗位非常典型的全链路面试。

---

## S123 京东｜AI 后端二面｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/cf38c74fc2eb487fac0f671da50c54a6

高价值问题：

1. Agent 项目的真实业务问题、个人贡献和技术难点是什么？
2. RAG 的切分、存储、检索和生成逻辑如何实现？
3. Spring AI 的核心结构是什么，为什么这样选？
4. 除 Java 生态外还了解哪些 Agent Framework，它们与自研 Runtime 的边界是什么？
5. 当前 Agent 项目还有哪些明显缺陷，如果继续做会优先补什么？
6. Context 如何组织和裁剪？
7. 短 / 中 / 长期 Memory 如何分层？
8. 不同任务如何做模型选型？
9. 使用 AI Coding 时如何保证生成代码质量？

价值：重点在“**项目不是完成了就结束，而要能说出它还缺什么**”，适合作为项目深挖与架构演进的验收样本。

---

## S124 谐云科技｜AI 后端开发｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/33f4503d73d4440c9df3728070153d17

高价值问题：

1. 平时使用哪些 AI Coding / Agent 工具，真正提高效率的部分是什么？
2. Skill 是什么，与 MCP 的职责有什么不同？
3. RAG 项目遇到过什么真实问题，如何定位？
4. 如何减少 Token 消耗？什么时候适合 Sub-agent / Swarm？
5. 线程池参数和任务队列如何设计？
6. `synchronized`、线程安全容器等并发基础如何理解？
7. MySQL MVCC 如何实现？

价值：又一份目标 AI 后端岗位中 **Agent + Java/Python 等服务并发 + MySQL** 同场出现的样本。

---

## S125 字节跳动 TikTok｜AI 后端开发｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/908fa7f0cda44569b919d23604419f14

高价值问题：

1. 一个完整 Agent 系统应包含哪些模块？
2. Spring AI Alibaba 等框架覆盖了哪些层，哪些 Production 能力仍需业务侧补？
3. Planner / Executor / Supervisor Multi-Agent 与单 Agent 怎么选？
4. RAG 完整链路、Recall / Rerank 分别解决什么问题？
5. RAG 与 Fine-tuning 如何取舍？
6. MySQL 与 Redis 在 AI 服务中如何分工？
7. Redis 能否作为某些状态的主存储，而不只是 Cache？边界在哪里？
8. 超大规模 Producer / Consumer 场景如何设计并发与背压？

价值：把 Agent / RAG 与 Redis 数据语义、超大并发模型结合得很紧，是 AI Backend Engineering 的高价值样本。

---

## S126 小红书｜AI 后端一面（28 届）｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/169b2d8f7a134843b114b820ee692186

高价值问题：

1. LRU 如何实现 O(1) get / put？
2. 秒杀 / 高并发交易系统如何设计？
3. RocketMQ 事务消息怎么理解？
4. Redis Lua 如何保证原子操作，缓存与数据库一致性如何处理？
5. 乐观锁适合什么场景？
6. Redis Set / ZSet 如何选？
7. MySQL MVCC、隔离级别、联合索引、B+Tree、回表、深分页如何解释？
8. Agent 的整体架构、Memory、执行模式和意图识别如何设计？
9. RAG 如何评测和优化？

价值：基础工程题密度非常高，但岗位明确是 AI 后端，因此非常适合校准我们的 **MySQL / Redis / Backend 必修深度**。

---

## S127 蚂蚁｜AI 后端开发一面｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/bb7184afd2144c6e99acc33108a064f5

高价值问题：

1. Agent / RAG 项目怎么介绍，真实收益如何证明？
2. Skill 与 MCP 分别解决什么问题？
3. Redis 分布式锁如何设计，Lua 在其中有什么作用？
4. CAS / 乐观锁有哪些边界和失败模式？
5. Redis 作为 MySQL Cache 时更新策略如何设计？
6. 用户在浏览器输入 URL 后发生什么？
7. Linux 环境、Shell 等工程基础为什么仍重要？
8. 短链系统如何设计？
9. Coding：如何检测环等基础算法问题？

价值：说明目标 AI 后端岗位依旧可能系统考察 **缓存、并发、网络、Linux、系统设计、算法**，而不只是 RAG / Agent。

---

## S128 京东｜AI 后端开发｜2026｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/6d24fc0f5a2c47209e172ed40d6bfcc4

高价值问题：

1. MySQL 为什么常使用自增 / 趋势递增主键？
2. Redis 单机容量不够时如何扩展到 Cluster？
3. Redis Lua / 多 Key 原子操作在 Cluster 下会遇到什么限制？
4. Agent 常见模式与 ReAct 如何理解？
5. 什么时候应该使用 Sub-agent？
6. Project Rules / Constraints 如何注入 Agent？
7. Context Engineering、Skill、MCP、Rule 之间分别解决什么问题？
8. Skill 激活是否可靠，如何评测路由命中和错误激活？

价值：除了 Agent Rules / Skill，还直接暴露了一个 Redis 生产细节：**Lua 的原子性不能脱离 Cluster / Hash Slot 边界讨论**。

---

# Batch 10 结论

本批新增 14 个来源（`S115–S128`），继续没有出现“基础工程能力退出 AI 面试”的迹象，反而进一步确认：

1. **MySQL / Redis / MQ / 并发仍是 AI 后端和 AI 全栈的一面主干**：只是在更深的 Agent 二面 / Harness 面里相对不显眼。
2. **LLM Foundation 正从 Attention / Sampling 向 Runtime 继续延伸**：KV Cache、Token Usage、Provider Usage 语义已经直接进入应用岗面试。
3. **Agent Observability 不只要 Trace，还要可核算成本**：父 Agent、Sub-agent、Tool、RAG、取消和断连都影响 Token / Cost Accounting。
4. **Agent 数据访问需要治理层**：Database / Internal Service 不应简单作为“模型可自由访问的资源”，而应经过 Tool Runtime / Service Boundary 做鉴权、租户隔离、审计和输入约束。
5. **Retrieval 深度继续提高**：Bi-Encoder / Cross-Encoder、IVF / HNSW、RRF / Rerank 已经形成一条完整的 Vector DB → RAG 课程链。
6. **自动化 AI 面试官需要单独统计**：以后来源元数据增加 `interviewer_type` 概念，避免自动生成/固定题库结构与真人面试同权统计。
7. **跨平台召回继续做，但正式库不为平台多样性牺牲质量**：本批扫描到的多个博客/问答/短视频高排名内容属于二次标准答案或资源导流，因此被过滤，没有为了“非牛客占比”强行收录。

当前仍未接近饱和。随着 canonical 新增速度下降，后续重点会逐渐从“发现完全新名词”转向：**独立来源命中频率、岗位/轮次条件概率，以及同一知识点被追问到的工程深度。**
