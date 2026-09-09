# Batch 08 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批继续执行统一固定准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 本轮继续使用 `公司 × 岗位别名 × 月份 × 技术关键词` 回扫 2026 年历史缺口并追踪 9 月近期内容，同时强化三层去重：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。同一候选人的同一招聘流程多轮面试合并计为一个来源。
>
> 本批开始出现一个需要持续观测的信号：泛关键词搜索中的已收录来源、整理帖和答案帖比例明显上升，但精确公司 / 轮次搜索仍能找到新的独立 HUMAN-A，因此目前只能认为“重复率开始上升”，还不能判断来源已经饱和。
>
> 问题均为研究所需的简洁转述，不复制第三方正文；只写能够从原帖确认真实问到的内容，不把合理推导写成面试问题。

---

## S148 阿里 Token Foundry｜AI 应用研发｜一面 + 二面 + 三面｜2026-08-17 / 08-24 / 09-03｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/6a7fbdcf484a4b2bbe4b900b2dbd5750

二面来源：https://www.nowcoder.com/feed/main/detail/ed25d2f60ddc4436b0139a7c52e62a61

三面来源：https://www.nowcoder.com/feed/main/detail/bfd43b5c66784add8fbf5893c164697a

真人 / 第一人称证据：同一候选人连续发布三轮，项目、岗位和时间线一致；明确记录 8 月 17 日一面、8 月 24 日二面、9 月 3 日三面以及流程结束状态。多轮均围绕本人 DoVideoAI / Agent 实践持续深挖，并保留面试官追问与候选人的现场判断。

高价值问题：

1. 为什么项目不用纯 ReAct，而采用受控 Agent Workflow？“受控”具体体现在哪里？
2. Planner / Executor / Critic 如何分工，Critic 依据什么拒绝或放行，怎样避免反复循环？
3. 两次 Agent / Model 调用分别应该携带什么 Context，怎样控制历史信息增长？
4. 长任务运行期间用户又输入新指令时，Runtime 如何处理目标变化和状态迁移？
5. 长视频 ASR / OCR / 帧信息如何融合，分段与 Chunk 参数怎样用实验证明有效？
6. Keyword + Vector Retrieval 如何组合，如何区分知识缺失、解析错误和召回失败？
7. RAG 应分别如何评估 Retrieval 与最终回答，Bad Case 怎样归因？
8. Invalid JSON、Checkpoint、任务恢复等 Failure Case 如何处理？
9. Redisson Watchdog / 幂等控制在长任务里解决什么问题？
10. 项目中哪些设计和代码是本人完成，AI Coding 生成部分如何验证可交付？
11. Agent 出现 Idle Loop / Dead Loop 时怎样检测和终止？
12. 如何评价近期 Coding Agent / Claude Code 类产品的优缺点？

去重说明：三篇为同一候选人的同一招聘流程，合并计为一个来源，不按轮次虚增样本数。

---

## S149 阿里淘天｜AI 应用开发｜一面｜发布 2026-04-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e6bd714a536b4723b67f97631b174f60

真人 / 第一人称证据：作者以本人“淘天 AI 应用一面”发布，正文从面试官介绍部门、自我介绍进入 RAG / Harness / Agent / MCP / Sandbox，最后记录连续三道限时 AI Coding 的现场压力，并使用“发面经攒人品”标签。

高价值问题：

1. RAG 的完整技术链路如何解释？
2. Harness Engineering 是什么，与普通 Agent Logic / Framework 的边界在哪里？
3. Hermes Agent 一类系统如何做自我纠错 / 自我改进？
4. 模型自身知识与 RAG 检索证据冲突时应该怎样处理？
5. MCP 适合哪些使用场景？
6. Agent Sandbox 应隔离哪些文件、网络和执行风险？
7. 智能客服为什么选择 ReAct 或 Workflow，二者边界如何判断？
8. Agent 的主要局限是什么？
9. Prompt Injection 应怎样从工程层防护？
10. Multi-Agent 什么时候值得使用？
11. 项目是否部署、真实用户规模如何证明？
12. AI Coding：连续 3 道题，每题 15 分钟，如何在时限内交付可验证结果？

---

## S150 阿里淘天用户运营技术｜AI 应用开发工程师｜日常实习一面｜发布 2026-08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/5dca9d9dd8284cc4aada23b9f0c20f15

真人 / 第一人称证据：作者明确记录一面约 30 多分钟，另有 60 分钟 Agent 在线笔试，并复盘自己“对 Agent 项目很不熟”的现场感受；问题从本人 Coding Agent 项目一路追到 RAG、Harness 与 Java Runtime。

高价值问题：

1. Coding Agent 从读代码库、修改文件到 Git 提交的完整链路是什么？
2. 一个新需求如何被 Agent 分析、拆成任务并逐步实现？
3. 模型第一次返回什么，之后怎样结合已有接口、策略和代码上下文继续行动？
4. 本地代码库应该构造成知识库，还是采用 Repo Search / Index 等其他方式？
5. RAG Chunk 召回不完整时怎样补救，还有哪些代码索引方式？
6. Harness 相比 MCP + ReAct 额外提供了哪些能力，为什么更稳定 / 更安全？
7. Java Class Loading 从字节码到内存经历什么过程？
8. 类加载后的数据分别存在哪些内存区域，类什么时候可以卸载？
9. Thread Pool 在核心线程 / 队列 / 最大线程之间怎样调度和复用线程？
10. Lock / ReadWriteLock、HashMap / Red-Black Tree 等基础如何解释？
11. 本地 Cache 与 CPU L1/L2/L3、Heap 之间的性能关系怎样理解？

---

## S151 阿里淘天｜Agent 开发｜二面 + 三面｜发布 2026-08-28 / 08-30｜HUMAN-A

二面来源：https://www.nowcoder.com/feed/main/detail/061b68e50121468ca1f882bef5c957f4

三面来源：https://www.nowcoder.com/feed/main/detail/b6b453976c2d4e43a872054d695c2fe2

真人 / 第一人称证据：同一作者连续记录二面“过了”和后续三面，候选人有两年工程经验；二面围绕 Agent 研发流程 / Skill / Observability / Long-running Task 深挖，三面继续进入平台重构、工程高可用、Agent 分层与部门知识沉淀，时间线连续。

高价值问题：

1. 如何把测试节点、代码评审、开发、预发验证、上线等研发环节 Agent 化？
2. Skill 与 Multi-Agent 执行分别解决什么问题？
3. Agent 分层除了防 Hallucination，对工程还有哪些收益？
4. 长任务失败为什么难归因，线程级 Trace / Observability 应怎么做？
5. 自动化工作流中人工应在哪些节点介入，中断后如何恢复？
6. Skill 在多人云端共享后怎样防止数量膨胀、错误沉淀与 Context 占用？
7. Skill 与 Memory 的沉淀边界是什么，怎样做调用量 / Token / Telemetry 治理？
8. Agent Loop 没有显式终止条件时怎样定义 Goal Completion？
9. Agent 平台怎样把 MCP / Skill / Knowledge Base / RAG 分层？
10. 为什么使用 Agent 而不是普通 Platform / API，效果如何验证？
11. 部门级 Memory / Knowledge 怎样沉淀，避免工程经验“随人走”？
12. 旧服务迁移到 Cloud Agent Platform 时如何保证可靠性和高可用？

去重说明：二、三面属于同一作者同一招聘流程，合并计为一个来源。

---

## S152 阿里淘天｜业务 + AI 全栈工程师｜一面｜发布 2026-09-07｜HUMAN-A

来源：https://www.nowcoder.com/discuss/926606679108521984

真人 / 第一人称证据：作者以完整一面过程记录实习确认 → RAG → Agent / AI Coding → MQ 幂等 / 限流 → 深分页 / 账单设计 → 反问；正文保留大量面试官连续追问和作者回答上下文，且反问阶段进一步核实团队确实同时做业务与 Agent。

高价值问题：

1. 企业 RAG Knowledge Base 的组织 / Team 权限应如何建模？
2. Markdown 与非 Markdown 文档分别适合哪些 Chunk Strategy？
3. Top-K 为什么选 6 / 8 而不是 3，怎样用 Evaluation 证明参数合理？
4. 多 Query / Query Decomposition 会把召回扩到很多片段，如何控制噪声和 Hallucination？
5. 原始文档质量差、结构不稳定时，Parsing 与 Retrieval 应如何治理？
6. 怎样证明 RAG 优化真的提升，No-answer 场景又应该怎样评测？
7. ReAct、Spring AI Tool Calling 与 MCP 如何组合？
8. AI Coding 如何获得项目规范、模块边界、业务 Wiki 等高质量 Context？
9. MQ Consumer 在分布式并发下如何保证业务 Idempotency？
10. 生产 1 万 QPS、下游只能承受 100 QPS 时，Rate Limit 怎样与 MQ Pull / Push 模式结合？
11. 分库分表后的商家账单深分页、跳页、跨库聚合应如何设计？
12. 买家 / 卖家双写表如何处理分布式事务和一致性？

---

## S153 小红书｜AI 后端开发｜一面｜发布 2026-08-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e07702037462474596f83b57f0d0ce72

真人 / 第一人称证据：作者明确记录面试超过 1 小时，面试官多次认为回答“没有到点上”，最终 LRU 因面试过长只要求口述思路；楼主在评论区继续更新“约二面 / 后续判断”。整场由高并发缓存、数据库逐步进入 Agent / RAG。

高价值问题：

1. 5000 万商品缓存怎样设计，TTL 如何设置？
2. 10 万 QPS 爆款商品引发 Cache Breakdown 时怎样保护 MySQL？
3. HotKey 怎样检测和治理，Redis Key Expiry / Eviction 怎样工作？
4. DB 与 Cache 一致性怎样保证？
5. 不依赖 Redisson 时，Redis Distributed Lock 的 NX / EX / Unlock / Watchdog 怎样正确设计？
6. ZSet 为什么使用 SkipList，复杂度和退化情况是什么？
7. `user_id + create_time` 订单查询怎样设计 Composite Index，`ORDER BY` 与 Deep Pagination 怎样优化？
8. MVCC 与 Isolation Level 如何联系，Phantom Read 为什么不是一句“MVCC 已解决”就结束？
9. Agent 与 Chatbot 的边界是什么，一个 Agent 应包含哪些模块？
10. ReAct 与 Plan-and-Solve 的流程、优缺点和场景如何比较？
11. RAG 的 Chunk / Ranking / Evaluation / Dataset / Benchmark 应怎样设计？
12. Agent Memory 应在什么时机写入 / 触发？

---

## S154 OPPO｜AI 全栈｜一面｜面试 2026-08-23｜HUMAN-A

来源：https://www.nowcoder.com/discuss/920830730643443712

真人 / 第一人称证据：候选人明确记录一面日期、面试时长不到半小时，面试官开场介绍这是新的 AI 全栈方向，并在第二天更新失败结果；作者复盘自己虽然基本答到，但组织表达不好。

高价值问题：

1. 平时使用哪些 AI Coding / Development Tool，实际如何进入工作流？
2. AI 生成代码质量不好时怎样发现和修正？
3. 使用过哪些 Skill，怎样评价一个 Skill 是否真正有帮助？
4. 短 Instruction / Skill 为什么有时能约束复杂任务？
5. 项目中本人负责哪些模块，如何部署和交付？
6. 团队协作出现冲突时如何处理？
7. Array 与 Linked List 的底层差异和适用场景是什么？
8. Stack / Queue 分别适合什么问题，BFS 为什么通常使用 Queue？

---

## S155 字节跳动抖音｜AI 全栈工程师实习｜一面 + 二面｜发布 2026-03-19｜HUMAN-A

来源：https://www.nowcoder.com/discuss/861892975133986816

真人 / 第一人称证据：候选人明确记录一面、二面各约 1 小时，一面当晚过，次日二面后失败；两轮都有两个面试官，正文保留现场难度感受、实习项目追问和算法题。

高价值问题：

1. 弱网下上传 1GB 视频，如何做分片、重试与断点续传？
2. JavaScript 怎样实现 100 个任务、最大并发 5 的并发池？
3. HTTP/3 与 QUIC 解决了哪些 HTTP/2 / TCP 问题？
4. LLM 调用数据库 Tool 的完整链路是什么？
5. React Hook 如何封装 WebSocket 并在多个页面复用连接？
6. Promise 与 async / await 的语义差异是什么？
7. MCP 的价值和长期边界是什么，Function Calling 如何工作？
8. 多 Agent 的通信与 State Management 怎样设计？
9. Coding Agent / IDE 从设计稿到生产代码会遇到哪些 Verification 与工程问题？
10. Codebase Retrieval 怎样实现，业务接入成本怎样降低？
11. 项目“查询准确率 95%”、SEO / 首屏速度等指标怎样测量而不是口头宣称？

---

## S156 腾讯｜AI 后端开发｜二面 50min｜发布 2026-04-01｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f0e993c94c17476180e1a0185a6662f2

真人 / 第一人称证据：作者以本人腾讯 AI 后端二面复盘发布并写“攒人品”，问题从项目 / 论文进入 Transformer、LLM Application、Agent 与系统设计，面试时长明确为 50 分钟。

高价值问题：

1. Transformer 的主要局限是什么，可以从哪些方向优化？
2. Transformer 与 Mamba 的适用场景如何比较？
3. LLM、Prompt Engineering、RAG、Agent 在真实项目里分别如何实现和优化？
4. Agent 有哪些真正值得落地的应用场景？
5. 怎样设计一个 Add / Delete 都为 O(1) 的定时任务触发器？
6. Consistent Hashing 的原理和适用场景是什么？
7. 怎样保证系统并发安全？
8. 项目遇到的真实工程难点如何定位和解决？
9. 如何快速学习并投入使用新的工程语言，例如 Go？

---

## S157 字节跳动｜后端 Agent 开发｜二面｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d9c10e9ec1294800990b6388a8bb9229

真人 / 第一人称证据：作者明确以本人“后端 Agent 开发二面”发布，开头写面试很难并“攒人品”；问题从实习持续进入 Prompt、RAG、LLM Foundation、Java Reflection 和高并发 System Design。

高价值问题：

1. Prompt 调优有哪些真实经验，能否让 AI 反过来帮助优化 Prompt？
2. ReAct 与 Plan-and-Execute 的优缺点如何比较？
3. RAG 从 Chunk 到 Generation 的完整流程是什么？
4. Multi-way Retrieval 为什么同时需要 Vector 与 Keyword，Rerank 解决什么？
5. RAG 与 Fine-tuning 的适用边界是什么？
6. Multi-hop Query / 多次 RAG 应怎样优化？
7. RAG 的 Permission Isolation 与 Freshness 如何实现？
8. Transformer 的 QKV、Position Encoding、Multi-head Attention 与 Residual Connection 如何解释？
9. Java Reflection 的原理、AOP 场景、性能 / 安全代价是什么？
10. 10 万 QPS 系统如何实时统计最近 1 小时 Top-10 IP，并在分布式实例间汇总？
11. Coding：用给定数字集合构造小于 N 的最大数。

---

## S158 阿里淘天｜AI 应用开发｜二面 80min｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b7ee06d162f34f2fa15bd90b8b07b100

真人 / 第一人称证据：作者明确记录二面约 80 分钟并以本人复盘“攒人品”；前半围绕真实 AI 项目和 Multi-Agent 设计追问，后续继续聊模型选择、Fine-tuning、指标和 AI Coding。

高价值问题：

1. AI 项目真正解决什么业务问题？
2. Multi-Agent 为什么这样拆，每个 Agent 是否都需要调用 LLM？
3. 单 Agent / Multi-Agent 的 Trade-off 怎样证明？
4. 项目效果指标是什么，统计口径和跟踪方式怎样定义？
5. 半自动 Evaluation Pipeline 如何实现？
6. 输出不准确通常来自哪些层面，怎样定位？
7. 为什么选择 7B 而不是 32B 模型？
8. Fine-tuning 的完整流程和关键步骤是什么，本地部署需要考虑什么？
9. AI Coding 在真实工作中怎样使用，生成代码如何 Review / 验收？

---

## S159 阿里淘天｜AI 应用研发｜一面 2h｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/80058a5c487347b5bbf7c8e5d694377d

真人 / 第一人称证据：作者明确记录一面约 2 小时，以“给我面没招了”复盘；问题连续深挖两段实习、RAG、LangGraph、Kafka、Text-to-SQL，最后还有约 45 分钟 AI Coding System Design。

高价值问题：

1. RAG 文档怎样 Chunk，怎样发现错误召回导致的 Hallucination？
2. Vector DB 应按哪些维度选型？
3. LangGraph 的 State 怎样流转，与 LangChain 的职责差异是什么？
4. Kafka 高峰 Message Backlog 怎样处理？
5. 怎样区分“Broker 堆积”与“Consumer 能力不足”？
6. 遥测数据消费是否需要顺序一致，如何决定 Partition / Ordering 策略？
7. Text-to-SQL 如何服务非技术用户？
8. 自然语言歧义和 Multi-table Join 怎样保证字段 / 语义正确？
9. AI Coding：设计一个可扩展、并发安全且逻辑清晰的订单状态机引擎。

---

## S160 阿里淘天｜Agent 开发｜暑期一面｜发布 2026-04-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b05d3d5136984d8b8e0ed5183a28a5c6

真人 / 第一人称证据：候选人明确写“整体面试不错但是没后续”，问题按实习 / 项目 / Transformer / Java / Agent / Coding 自然流转，带有明确个人结果状态。

高价值问题：

1. Transformer 的关键结构与 Q / K / V 如何解释？
2. KV Cache 为什么能加速推理？
3. Transformer 为什么能够用于多模态建模？
4. Knowledge Distillation 是什么，应用侧需要理解到什么深度？
5. Java Memory Leak 常见原因和排查思路是什么？
6. Long Context 导致遗忘时怎样治理？
7. 除 Prompt 外，怎样减少 AI Coding 产生的冗长 / 复杂代码？
8. Agent Runtime 的基本执行流程是什么？
9. RAG Knowledge Base 与 Agent Skill 分别承担什么职责？
10. Coding：Binary Tree Traversal。

---

## S161 字节跳动｜后端 AI 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/684c3c18ca774b149ea859a14ca9c323

真人 / 第一人称证据：作者以“字节暑期后端 AI 开发一面”发布并保留明显的面后受挫状态；目标岗位明确为 AI Backend，问题以工程底座为主并穿插 AI 使用 / Agent 上下文实践。

高价值问题：

1. Gateway / Network Protocol 在服务链路里如何工作，TCP 如何保证可靠传输？
2. Redis 发生数据丢失时怎样分析 Persistence / Failure Window？
3. Jedis 与 Local Cache（如 Caffeine）分别适合什么场景？
4. `synchronized`、ReentrantLock、AQS 与 CAS 如何联系？
5. 工程开发中怎样实际使用 AI，并把业务约束准确传递给模型？
6. 多个 Agent Conversation 的状态与持久化如何隔离？
7. B-Tree 与 B+Tree 为什么适合不同的存储 / Index 场景？
8. Coding / Database 基础怎样在 AI Backend 面试中被现场验证？

---

## S162 字节跳动｜后端 Agent 开发｜暑期一面｜发布 2026-04-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fa55d9f475624bfb95d943a5c00a599f

真人 / 第一人称证据：作者明确以本人同岗一面分享并“攒人品”，整场围绕实际 Agent / RAG 项目做连续追问，问题从 Single / Multi-Agent 设计一路深入到失败恢复、结构化 Context 与 Latency / Quality 权衡，并附现场 Coding。

高价值问题：

1. 为什么不在 Single Agent 里持续增加 Tool，而要拆 Multi-Agent？
2. 如果模型已经能自主决定调用什么 Tool，为什么还需要显式 Orchestration？
3. 业务 Knowledge Base RAG 怎样搭建，Vector Retrieval / Top-K 怎样工作？
4. 为什么同一业务领域不直接统一成一个 Agent + RPC Tools？
5. Retrieval / Recall 应看哪些评价指标？
6. Multi-Agent 局部失败 / 链路失败时如何恢复？
7. Agent 间 Context 为什么可能使用 JSON / Slot 等结构化形式？
8. Tool 能统一封装后，按业务拆 Agent 的真正收益是什么？
9. 线上怎样权衡 Latency 与回答 / 执行效果？
10. Coding：Word Break。

---

## S163 奇虎 360｜Agent 开发｜Leader 一面 + 技术二面｜2026-02-12 / 02-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f1381f5afdc94a0d899a61c707401c8e

真人 / 第一人称证据：作者完整记录 2 月 12 日产品 Leader 面和 2 月 27 日技术二面；一面被要求共享屏幕演示自己的 Agent Platform，二面继续追实际性能优化、长任务恢复、MCP、LLM Failure 与数据库基础，具有很强项目验真和多轮时间线。

高价值问题：

1. Agent Platform 做什么、用户画像和商业价值是什么？
2. 广告创意平台怎样用 Agent 赋能，而不是为了 AI 而 AI？
3. Multi-version Snapshot + Optimistic Lock 如何处理并发更新和安全回滚？
4. RT 从 150ms 降到 25ms 时，怎样拆 Core / Non-core Path 并验证优化？
5. Non-core Failure 怎样保证 Core Data Consistency？
6. 长任务关闭 / 服务重启时如何保证状态一致，并通过 Local Outbox 恢复？
7. MCP Gateway 的 Protocol Translation 解决什么问题？
8. LLM Provider 故障时怎样做 Circuit Breaker / Degrade？
9. Multi-hop / Cyclic Retrieval 怎样实现并防止无效循环？
10. MySQL B+Tree、Composite Index、Transaction / WAL / Isolation Level 如何解释？
11. Redis Data Structure 与 Ranking 场景如何选，MySQL / Redis Consistency 怎样做？

---

## S164 腾讯｜AI 应用开发｜暑期一面｜发布 2026-03-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f6657d973e064f8c8fa0865ac2d8af57

真人 / 第一人称证据：作者以本人同岗一面“发问题、攒人品”发布，项目追问围绕 Auto Deployer、Motion Graphic Agent、Skill / Context Engineering、Gemini CLI 与 Multi-Agent；后续搜索发现 03-21、03-23 存在题序高度一致的后发版本，本批只保留更早来源。

高价值问题：

1. Auto Deployer 的主要工程难点是什么？
2. Motion Graphic Agent 的整体架构怎样设计？
3. Skill 全塞 System Prompt 导致 Context 膨胀时怎么办？
4. Skill Description 相似导致错误加载时如何改进 Routing / Retrieval？
5. Context Engineering 最重要的约束是什么？
6. 主流 Agent Architecture 有哪些？
7. Gemini CLI 的关键设计是什么，还可以怎样优化？
8. Multi-Agent 常见实现方式有哪些？
9. Multi-Agent 之间怎样通信与传递状态？
10. Coding：Valid Parentheses。

去重说明：后续 03-21 / 03-23 高度相似帖子只作为重复信号，不新增来源计数。

---

## S165 腾讯元宝｜AI 应用开发｜一面｜发布 2026-03-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/5e38806012f94d5aa4bf0c7405f9aeb6

真人 / 第一人称证据：作者以“腾讯元宝 AI 应用开发一面（好难）”发布并写“攒人品”，问题覆盖真实 AI Chat / Agent Service 的前端、Streaming、Protocol 和 Production Debugging；评论区还有同岗位候选人交流。

高价值问题：

1. Agent System 的技术选型应考虑哪些因素？
2. AI Chat 的 Streaming Rendering 怎样实现？
3. 为什么选择 SSE，Server 断开和 Client 断线重连怎样处理？
4. Markdown Stream 怎样分块渲染，解决什么性能问题？
5. 用户一次粘贴 1 万行 Markdown 并滚动卡顿时如何优化？
6. 前端调用不支持 OPTIONS 的后端接口时怎样设计 Proxy / CORS 方案？
7. Production White Screen / Function Error 应怎样快速定位？
8. HTTP/1、HTTP/2、HTTP/3 的主要差异是什么？
9. React Fiber / Vue 响应式与 Frontend Performance Optimization 怎样理解？
10. 常见 AI 产品有哪些优缺点，产品体验怎样反向影响 AI Application Engineering？

---

## S166 蚂蚁｜Agent 开发｜一面｜发布 2026-04-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7a0ddb8e077041d4b72ba9e5290ad36a

真人 / 第一人称证据：作者明确写“面完人都通透了、还需要沉淀”，以本人 Agent 实习项目为主线连续追问 Multi-Agent、RAG、MCP、Tool Failure、Context 和 AI Coding Quality，问题顺序自然且有明显现场复盘感。

高价值问题：

1. Agent 实习项目整体架构是什么？
2. 什么情况下用 Single Agent，什么情况下用 Multi-Agent？
3. Multi-Agent 之间怎样传输数据 / 通信？
4. 多个 Agent 并发操作数据库或文件时怎样保证正确性？
5. 异步 Agent Execution 应注意哪些竞态和状态问题？
6. Hybrid Retrieval 如何实现，怎样治理 RAG Hallucination？
7. Tool / Function API 返回缺字段、冗余字段时怎样做 Validation / Self-refine？
8. MCP 解决什么问题，Tool Call Failure 怎样恢复？
9. Agent Context 怎样管理？
10. AI Coding 是否形成方法论，上线前除了 Code Review 还怎样保证质量？
11. OpenSpec / Spec 类实践是怎样进入真实项目开发流程的？

---

## S167 腾讯｜AI 应用开发后端实习｜一面｜发布 2026-04-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/144c6ae334b24c0aa643ed43ccfebaac

真人 / 第一人称证据：作者明确记录项目深挖约 40 分钟、金融业务场景约 15 分钟，并以本人“攒人品”形式发布；问题紧扣真实 Multi-Agent / RAG 项目，再通过跨境汇款场景追 Agent Failure 与资金安全，最后有现场 Coding。

高价值问题：

1. 项目为什么没有正式上线 / 用户，怎样判断 Demo 与 Production 的差距？
2. Multi-Agent 怎样编排，完整执行 Flow 是什么？
3. Training Sample 从哪里来，是否做过 Model Tuning？
4. Agent Failure / Interrupt 如何处理，Retry 怎样避免重复副作用？
5. 跨境汇款 Agent 超时 / 失败时怎样保证资金安全？
6. RAG Knowledge Base 怎样 Hot Update 而不停服？
7. 真实 AI Backend 中 Design Pattern 如何支撑可扩展性？
8. Coding：Max Area of Island / DFS。

---

## S168 CVTE｜AI 应用开发｜一面｜发布 2026-08-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fe214e3233344c859ec79076179115f1

真人 / 第一人称证据：候选人明确写自己当时正在另一家公司实习，只能在楼梯间用手机参加面试；进行到 AI Live Coding 时因为没有电脑无法继续，面试官还安慰了作者。现场、设备、结果和互动痕迹非常明确。

高价值问题：

1. RAG Retrieval 的核心原理是什么？
2. Prompt Injection 怎样防御？
3. Agent Prompt 应怎样设计？
4. Context Compaction 怎样实现？
5. 文档有哪些 Chunk Strategy，Semantic Chunking 的原理是什么？
6. Semantic Chunk 是否仍需要 Hard Maximum Size？
7. Process 与 Thread 的区别是什么？
8. 多线程竞争同一资源除了 Lock 还有哪些解决思路？
9. JVM Memory Area 怎样划分？
10. AI Live Coding 如何在现场验证候选人的工程实现能力？

---

# 本轮明确排除 / 去重

本批扩大 Recall 时，以下内容继续保持 **零贡献**：

- 同一 AI 面经内容账号在短时间连续发布字节 / 阿里 / 快手 / 算法 / Infra 等大量“真人叙事”帖子，同时经营付费专栏 / 简历项目内容；即使单篇写了“挂 / 过”，跨帖模板化和商业内容链导致候选人本人真实性无法可靠确认；
- DeepSeek Harness、字节 Agent、得物 Agent 等带“思路参考 / 标准答案 / 完整回答”的内容型帖子；
- “三年面试五年模拟”、RockyDing / WeThinkIn、面经总结、企业题目聚合等二次整理；
- 宇树科技 Agent 等题目非常对口但正文几乎是标准化问题清单、缺少轮次互动 / 答题状态 / 结果时间线的帖子；
- CVTE 另一篇虽然现场感很强，但正文只记“项目追问 + Vibe Coding”等少量泛信息，具体技术问题密度不足，不进入正式库；
- AI 自动面试 / 模拟面试；
- 匿名公司、岗位无法稳定确认，或只有搜索摘要无法核验正文的线索；
- 普通后端 / 测开 / 纯训练算法岗位仅顺带问一两个 Agent / RAG 问题的场次；
- 腾讯 AI 应用 03-21、03-23 与 S164 题序高度相同的后发版本，只计重复信号；
- 同候选人的淘天二面 / 三面、Token Foundry 三轮均按一个招聘流程保守计数。

# Batch 08 观察

本批新增 `S148–S168` 共 **21 个 HUMAN-A 来源**，当前干净核心样本达到 **168 个**。

本轮出现了几个值得单独记录的信号：

1. **开始出现“重复率上升”，但仍未达到来源饱和。** 泛关键词搜索越来越多命中 S001–S147 已收录帖子、答案版、总结页和同题后发版本；但精确到公司 / 岗位 / 月份 / 轮次后，仍能稳定找到 20+ 个新 HUMAN-A。后续判断停止点时，应该同时记录“新来源数量”和“候选结果中的重复 / 低质量比例”。
2. **Agent Runtime 的真实面试已经进入受控执行与恢复语义。** Controlled Workflow、Planner / Executor / Critic、Long-running Task 新输入、Loop Termination、Checkpoint、Interrupt、Retry Safety、Human Intervention、Trace / Observability 都有独立真人命中。
3. **AI Coding 不再只问“你用不用 Cursor”。** 真实问题已经追到代码库理解、项目 Wiki / Spec、需求拆分、Git 工作流、质量验收、AI 生成代码能否进 Production、代码复杂度和在线 Coding System Design。
4. **RAG 继续强调“参数和效果必须可证明”。** Top-K 为什么是 6 / 8、Chunk 为什么这样切、Retrieval Miss 怎样归因、No-answer 怎样评估、Permission / Freshness 怎样处理、Vector / Keyword / Rerank 怎样组合，都在追实验和失败模式。
5. **AI Backend Foundation 仍然很重。** Redis HotKey / Lock / Watchdog、MySQL MVCC / Index / Transaction、MQ Idempotency / Rate Limit、Thread Pool / JVM、HTTP/3 / SSE、Consistent Hashing 与 Agent / RAG 在同一目标岗位出现。
6. **去重需要从 URL 升级到“作者 + 招聘流程 + 题序”。** 本批主动合并 Token Foundry 三轮和淘天 Agent 二 / 三面，并剔除腾讯 AI 应用的多份同题后发版本；只看 URL 会显著虚增样本数。

停止条件不变：继续扩大跨公司、岗位、月份、轮次和平台 Recall；只有连续多轮搜索中**新增 HUMAN-A 比例持续接近零**，新结果绝大多数都是重复 / 整理 / 低质量 / Role Scope 外来源，同时新增问题模块与深度分布也稳定收敛，才进入最终收尾。当前 168 个样本已经出现重复率上升的早期信号，但**仍未达到停止点**。
