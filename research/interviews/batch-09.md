# Batch 09 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批继续严格执行统一准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 本轮继续按 `公司 × 岗位别名 × 月份 × 技术关键词` 搜索，并重点使用企业页 / 话题页、精确标题、精确轮次和作者时间线回溯。Batch 08 已出现泛搜索重复率上升，因此本批同时观察“新 HUMAN-A 数量”和“重复 / 答案型 / 低质量结果占比”。
>
> 去重继续固定使用三层：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。同一候选人的同一招聘流程多轮面试合并为一个来源；不同候选人的独立场次即使问题相似，也保留为独立真人命中。
>
> 问题只做研究所需的简洁转述，不复制第三方原文，也不把合理推导写成“面试官真实问过”。

---

## S169 百度｜Coding Agent / Agent 开发｜秋招一面 + 二面 + 三面｜2026-08-18 / 08-21 / 08-24｜HUMAN-A

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

## S170 字节跳动中国交易与广告｜Agent 后端开发｜秋招业务终面｜面试 2026-08-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1dd33c4b7bda453a82f7d645bde7f3ff

真人 / 第一人称证据：候选人说明暑期已拿该部门 Offer 但未入职，秋招由 HR 保留原流程、只增加一次业务终面；本轮围绕新增蚂蚁 Agent Infra 实习持续深挖，面后约两小时通过并等待后续通知，时间线非常明确。

高价值问题：

1. 蚂蚁实习中的 Agent Infra 从输入到执行的完整链路是什么？
2. Infra 为什么能提升 Agent 能力，真正的工程难点在哪里？
3. 平台做过哪些优化，哪一项最有挑战，收益怎样证明？
4. 探索型 Agent 项目具体解决什么问题，为什么值得做？
5. Agent Infra 与具体业务 Agent 的职责边界如何划分？
6. Go GMP 如何支撑高并发 Runtime？
7. Redis Cache 在 Agent Backend 中如何使用与治理？
8. Coding：课程表变体，除了判断可行还要输出一条合法路径。

---

## S171 字节跳动｜App Infra Agent 开发｜秋招一面｜发布 2026-08-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0bec32fbb3344ff98f16b97f47c7b857

真人 / 第一人称证据：作者明确记录面试官介绍 App Infra Agent 岗位，并保留自己 KV Cache 回答含糊、TCP 问题没答上、对算法题难度感到意外等现场状态。

高价值问题：

1. KV Cache 在 LLM 推理中解决什么问题，为什么能显著降低重复计算？
2. 浏览器点击请求到服务端返回页面的完整网络链路是什么？
3. TCP 三次握手 / 四次挥手的语义是什么，最后一次关闭确认是否可以省略？
4. MySQL 为什么使用 B+Tree，最左匹配如何影响联合索引？
5. Redis Cache Penetration / Breakdown / Avalanche 分别怎样治理？
6. 分布式系统如何生成全局唯一且趋势递增的 ID？
7. Coding：排序类现场实现与复杂度分析。

---

## S172 字节跳动 TikTok｜AI Agent 开发｜秋招一面｜面试 2026-08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7b1b40fda3244715a82bcb4a821ca887

真人 / 第一人称证据：作者记录明确日期、面试官交流体感和等待结果状态；问题由会议转写项目连续进入 RAG、长上下文、Multi-Agent 与 Coding，并有多个基于本人方案的追问。

高价值问题：

1. 会议音视频从输入到 ASR / 文本生成的完整链路是什么？
2. ASR Provider 为什么这样选，识别准确率如何评测和优化？
3. 视频通话中的隐私数据怎样保护？
4. 系统为什么采用中心化或去中心化架构，取舍是什么？
5. RAG Chunk Strategy 如何设计，Tokenization 对切分有什么影响？
6. Transformer Attention / QKV 如何解释，Lost in the Middle 为什么发生？
7. Context Window 受什么因素限制，长度增加有哪些计算和效果代价？
8. 为什么需要 Multi-Agent，中心化协调模式有什么优缺点？
9. Coding：树 / JSON 结构转换与 Zig-zag Traversal。

---

## S173 字节跳动｜AI Agent 日常实习｜一面 + 二面｜2026-08-13 / 08-16｜HUMAN-A

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

## S174 深信服｜AI 全栈开发｜二面｜面试 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7fd4389e0a0844faa4dce49ba5e5c3f1

真人 / 第一人称证据：作者以本人二面复盘发布，评论区继续许愿 HR 面；面试官沿三层缓存、Redis / MySQL 一致性、分布式锁和开源 Agent 子 Agent Token 统计持续追问，项目链完整。

高价值问题：

1. 三层 Cache Hierarchy 为什么这样设计，重启后如何恢复状态？
2. Redis 与 MySQL 不一致时如何修复，为什么某些链路选择先写 Redis？
3. Cache Hit Rate 等项目指标如何证明有效而不是拍脑袋？
4. 基于注解的锁封装如何避免通用性不足和 Deadlock？
5. OAuth2 改造如何落到真实服务边界？
6. Agent Token Accounting 为什么容易漏算 Sub-agent / Tool Call？
7. Main Agent 断连但 Child Agent 延迟退出时，如何做补偿和资源回收？
8. 多 Sub-agent 并行更新 Token / Usage 统计时怎样避免 Race Condition？
9. 主 Agent 与 Sub-agent 如何通信并保持 Task State 一致？
10. RAG Tool 加入后会给 Token Accounting / Context Tracking 带来哪些额外复杂度？

---

## S175 OPPO｜实际 Agent / AI 应用方向（岗位标题后端）｜两轮｜面试 2026-05-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/09fd6466f3f64e7dbfb5a09ed9d660a4

真人 / 第一人称证据：作者明确说明“与其说后端，更像 Agent 开发，两轮基本只问 AI”，一面后约两小时通过并立即二面，后续更新已 OC；实际面试内容通过 Role Scope Gate，不按岗位标题机械分类。

高价值问题：

1. Context Window 不够时有哪些治理方式？
2. 面对超长论文 / 需求文档，如何通过折叠、任务拆分或多 Agent 降低上下文压力？
3. MCP 与 Skill 的边界是什么，为什么不能互相完全替代？
4. 如果设计一个模仿特定人格的 Skill，需要哪些约束和数据？
5. Agent 之间有哪些协作拓扑，中央 Coordinator 与更扁平的协作方式如何选择？
6. 多 Agent 协作中如何防止重复工作、目标漂移和信息丢失？

---

## S176 腾讯 WXG｜Agent / Coding Agent 方向｜秋招一面｜发布 2026-08-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3ffc762437274543b6a8f5e2ea6fb535

真人 / 第一人称证据：候选人记录面试房间临时被占、现场大数乘法卡住很久、最终秒挂等细节；本人实习工作明确包含 Agent，问题集中在 Coding Agent Memory、Eval 和 Cloud Agent 状态恢复。

高价值问题：

1. Coding Agent 的 Memory 应该保存什么，如何更新与失效？
2. 自研 Agent 与 Claude Code / Codex 的架构差异是什么？
3. Agent Evaluation 怎样设计，如何判断一次版本改动真的变好？
4. Cloud Agent 的 Container 迁移或重启后，Context / Task State 如何恢复？
5. 恢复后怎样继续推进原目标，同时避免行为漂移？
6. 基础模型已经很强时，Agent 工程最值得优化的层是什么？
7. Lost in the Middle 对长上下文 Coding Agent 有什么影响？
8. Coding：大整数乘法等现场实现。

---

## S177 字节跳动｜AI 全栈工程师｜秋招一面 + 二面｜2026-09-01 / 09-08｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/034e6ed3a28f463abbc3465dd1e4ad2f

二面来源：https://www.nowcoder.com/feed/main/detail/0a926033572f4a68b8c537f20a013503

真人 / 第一人称证据：同一候选人一面后明确更新通过并约二面；二面 9 月 8 日前置 2 小时 AI 作业，随后对方案连续拷打约 20 分钟，并保留算法卡壳和面试官反馈。同招聘流程合并计一个来源。

高价值问题：

1. 缓存穿透 / 击穿 / 雪崩与 Redis / DB 一致性如何治理？
2. 库存少卖或扣减失败时如何根据订单状态补偿？
3. LLM 与 Agent 的本质区别是什么？
4. ReAct 与 Plan-and-Execute 分别适合什么任务？
5. AI 前置作业如何从模糊需求中自主梳理功能、边界和技术方案？
6. 面试中怎样解释 AI 辅助完成作业时本人真正负责的设计和验证？
7. Kafka Message Consistency 如何保证？
8. API Idempotency 怎样设计？
9. 如果设计一个 Notification Platform，怎样处理可靠投递、重试与去重？
10. Coding：随机链表复制、Tree Maximum Independent Set 等。

---

## S178 蚂蚁｜AI 应用开发｜暑期二面 65min｜发布 2026-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/601233a9e7c54235895bdd09fb449eca

真人 / 第一人称证据：作者记录约 65 分钟二面，围绕本人文档解析 / RAG / Agent 实习与论文持续追问，并明确复盘“面试很难、很多地方需要继续练习”。

高价值问题：

1. MinerU 等文档解析方案如何保持跨页表格语义完整？
2. RAGAS / Answer Relevance 等指标出现问题时如何定位到底是 Retrieval 还是 Generation？
3. LangGraph State 如何定义和传递，Node 很多时怎样避免 State Object 膨胀甚至 OOM？
4. Long-term Memory 中结构化用户画像如何设计、更新和失效？
5. Chunk Overlap 过大 / 过小分别有什么副作用？
6. GraphRAG、Self-Reflection、CoT 分别解决什么问题？
7. Tool Parameter Hallucination / 格式错误如何自动校验和修复？
8. Multi-Agent 中央协调与 P2P 协作怎样取舍？
9. 支付等高风险操作中 Human-in-the-loop 应放在哪里？
10. Skill 与 MCP 如何分工，OpenClaw 类 Agent 的文件系统 / 环境 / 权限如何治理？
11. Context Cache 怎样减少重复 System Instruction 成本？

---

## S179 阿里高德｜AI 应用开发｜一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/87f26b7a710b4314a89134bf032ed58f

真人 / 第一人称证据：作者以本人同岗面经发布并“攒人品”，问题围绕其代码理解 / RAG 项目从 AST、Schema、Retrieval 一路追到 Skill、Memory 和 Agent Loop。

高价值问题：

1. 如何从 Requirement Document 判断某项功能在代码库中是否已经实现？
2. AST 的核心思想是什么，源码到 AST 的转换怎样工作？
3. Code RAG 中代码、注释、文件 / Symbol Metadata 应怎样建模？
4. Single-round 与 Multi-round Retrieval 分别适合什么代码检索场景？
5. RRF 为什么适合融合多路召回，权重 / 参数如何调？
6. Coarse-to-fine Rerank 如何减少成本同时保持 Recall？
7. Markdown / PDF 与代码文件应该采用怎样不同的 Chunk 策略？
8. Long-context Agent 还能否直接用普通 Chunking，什么时候要改成任务导向的检索？
9. Skill 与 MCP、Memory 与 Short-term Context 如何区分？
10. ReAct 与通用 Agent Loop 的关系是什么？

---

## S180 字节跳动｜Agent 后端开发｜日常实习二面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c1cac9b1d1e14fafa6b25afb177e7c17

真人 / 第一人称证据：作者明确记录本轮为二面并更新被横向淘汰；题目从 MQ / Streaming / Auth 连续进入 Agent、RAG、Context、Skill 与 Redis，另有一篇高度同题版本按重复处理，不重复计数。

高价值问题：

1. MQ 中如何把异步处理结果准确关联回原请求？
2. 为什么某些异步链路选择 MQ 而不是直接通过数据库传状态？
3. Agent 前端 Streaming 输出怎样实现，身份认证放在哪一层？
4. LangChain / LangGraph 分别提供什么能力，工程边界在哪里？
5. ReAct、Tool Call 与 Multi-Agent Collaboration 如何串成完整执行链？
6. Context Engineering 与 RAG / Persistent Memory 的边界是什么？
7. CoT 在 Agent 中有什么价值和限制？
8. Rules / Instructions、MCP、Skill 分别解决什么问题？
9. SSE 与普通 HTTP / 其他传输方案怎样比较？
10. Redis Rate Limit 如何实现，Redis 为什么适合高频状态与限流？

---

## S181 阿里｜AI 应用开发｜一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6cf457434a6a4cd9b1b9951cf1b6b513

真人 / 第一人称证据：作者以本人 AI 应用一面发布并邀请同岗交流；问题从文档 RAG 连续进入 LangGraph、Kafka Backlog、Text-to-SQL 和 AI Tool 使用，具有自然项目追问流。

高价值问题：

1. 文档 Chunk 应如何设计并验证？
2. Hallucination 出现时怎样判断根因是不是 Retrieval 质量差？
3. Vector DB 如何选型？
4. LangGraph State 如何存储与流转，为什么选择 LangGraph 而不是 LangChain？
5. Kafka 出现 Backlog 时如何区分流量激增、Partition 不均或 Consumer 能力不足？
6. Telemetry / Event Consumption 怎样保证顺序和可恢复性？
7. Text-to-SQL 如何处理 Schema、Query Planning 和自然语言歧义？
8. 日常使用哪些 AI Coding / AI Tool，怎样验证生成结果？

---

## S182 同花顺｜Agent 开发｜实习一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e92546db48fd42e19ed312b21ec903c9

真人 / 第一人称证据：作者按实习提问、项目、八股、Coding、AI 闲聊分别记录时长，完整保留一面流程；企业页核验显示其与同日二面帖不是同一候选人，因此独立计数。

高价值问题：

1. C++ Destructor 为什么经常需要是 Virtual，空类编译器会生成哪些默认成员？
2. TCP/IP 分层如何理解，IP 与 UDP 分别解决什么问题？
3. Datagram 与 Stream Protocol 的语义差异是什么？
4. 什么场景适合 Process，什么场景适合 Thread？
5. 常见 IPC 方式有哪些？
6. Coding：Search a 2D Matrix II。
7. 日常开发使用 AI Coding 的深度如何证明？
8. MCP Service 未来还有哪些工程空间？
9. OpenClaw / Agent 产品的实际使用经验是什么？

---

## S183 同花顺｜Agent 开发｜实习二面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e13a1970daa84af988d2f7dda473f3f4

真人 / 第一人称证据：作者明确记录项目拷打约 30 分钟、场景题约 10 分钟、AI 工具交流约 10 分钟，并自评业务逻辑表达不好；企业页显示与 S182 账号 / 学校不同，是另一位独立候选人。

高价值问题：

1. 广告效果引擎从数据生产到在线使用的完整业务链是什么？
2. Forward Data 如何转换成 Inverted Index / Cache？
3. 为什么不用 Java BitSet，序列化超大对象时怎样降低反序列化成本？
4. 千万级广告库如何分片并支持 Horizontal Scaling？
5. Worker / Manager Heartbeat 模式中 Manager 故障怎样处理？
6. 自定义 TCP Protocol 如何解决 Sticky Packet / Half Packet？
7. 高并发股票搜索如何同时支持代码、名称、拼音首字母以及前 / 中 / 后匹配？
8. Trie 对中文与 Infix Search 的实现边界是什么？
9. 日常 AI Coding Workflow 如何组织？
10. OpenHands 类 Coding Agent 的架构了解多少，Skill 与 MCP 有什么区别？

---

## S184 字节跳动｜Agent 后端开发｜实习一面 1h｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d73020680b3b42c3ac579e2f25721d90

真人 / 第一人称证据：作者以本人一面持续记录，问题高度绑定其 RAG 项目真实设计选择，并连续追到 Skill / Tool 边界和现场 Coding。

高价值问题：

1. 当前 RAG 相比标准 Pipeline 真正的创新 / 差异是什么？
2. RAG 效果如何评价，怎样做失败归因？
3. Summary 为什么可能让 Recall 变差？
4. 为什么某个方案只对 Title 做 Embedding 而不是对正文一起 Embedding？
5. Prompt Engineering 与 Context Engineering 的区别是什么？
6. Skill 是什么，和 Tool / Function Call 的核心边界是什么？
7. Skill 能否完全替代 Tool，为什么？
8. Skill 如果不直接依赖传统 Function Call，执行能力从哪里来？
9. Coding：非递归 Binary Tree Preorder Traversal。

---

## S185 蚂蚁｜后端 Agent 开发｜暑期一面｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/334690a445be4db3b5ac63207a507572

真人 / 第一人称证据：作者明确以本人“蚂蚁暑期后端 Agent 开发一面”发布，问题从项目和 Agent 认知继续进入单机锁到大规模分布式并发的逐层扩展。

高价值问题：

1. Agent 项目与 Backend 项目分别解决什么问题？
2. `synchronized` 用在业务方法上除了阻塞用户还有哪些问题？
3. 如果可以接受性能变慢，单机锁能否保证秒杀正确性，边界在哪里？
4. 同一业务扩展到上万台机器后，单机锁为什么失效？
5. Distributed Lock 应怎样设计 Key 粒度？
6. 锁的 Owner、TTL、Renewal 和 Unlock Atomicity 应如何保证？
7. Agent 服务在分布式部署后还需要额外处理哪些 Session / State 问题？

---

## S186 腾讯｜后端 AI 开发｜日常实习一面 1h｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/77d7da4a1e234435a256a864dc861185

真人 / 第一人称证据：作者以本人同岗一面发布并邀请同岗交流，问题从 Canal / Event Processing 进入 SSE、RAG / Vector DB，再进入 Go / Network 与现场 Coding，信息链完整。

高价值问题：

1. Canal 如何配置，如何识别 DDL / DML / DCL 事件？
2. SSE 与普通 HTTP Request / Response 的语义有什么不同，SSE 是否单向？
3. RAG 项目整体架构是什么，为什么选择 Eino 等框架？
4. Vector DB Index 怎样设计，Retrieval 返回文档 ID 还是内容？
5. OSI 七层与 TCP/IP 四层如何对应？
6. TCP 三次握手与四次挥手为什么这样设计？
7. Go `error` 与 `panic` 怎样区分，`defer` / recover 如何配合？
8. Go Context 可以承担 Cancel / Deadline / Value 哪些职责？
9. Gin 与 Kratos 等 Web / Microservice Framework 怎样选型？
10. Coding：Linked List Cycle，并自行构造输入输出。

---

## S187 腾讯｜后端 AI 开发｜一面｜发布 2026-04-12｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/db9014c0dcad4d4d985427e330dc1461

真人 / 第一人称证据：作者明确写“给我面没招了”、自评面试困难；问题从 Agent / RAG 进入 Streaming、DDD、Redis Session、Auth、Cache Consistency 和 Coding，属于目标 AI Backend 场次。

高价值问题：

1. 从零构建 Agent Service 应有哪些核心模块？
2. Agent Failure 时怎样 Retry / Fallback / Degrade？
3. RAG 在项目中具体承担什么职责？
4. SSE 与 WebSocket 的差异是什么，各自适合什么 Streaming 场景？
5. DDD 在真实项目里如何划分 Domain / Application / Infrastructure？
6. 多实例服务怎样共享 Session，Redis 在其中怎样使用？
7. Access Token / Refresh Token 与 Authentication Flow 如何设计？
8. Cache Aside 与 Delayed Double Delete 怎样理解，延迟窗口如何确定？
9. Mutex、Bloom Filter 与 Redis Lua 分别适合解决什么一致性 / 原子性问题？
10. Coding：Maximum Subarray。

---

## S188 字节跳动 TikTok｜后端 AI 开发｜实习一面｜发布 2026-05-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/98deba451f18417990758d9136dae164

真人 / 第一人称证据：作者以本人一面继续分享近期流程，问题从 Agent 项目逐步进入 MCP / RAG、LLM API、DDD、Streaming、HashMap、B+Tree、RabbitMQ 与 Coding。

高价值问题：

1. Agent 项目解决什么问题，完整执行链怎样实现？
2. MCP 与 RAG 分别解决什么问题？
3. Application Backend 如何调用不同 LLM Provider？
4. DDD Architecture 怎样组织 AI Service？
5. 为什么 AI Response 常采用 Streaming？
6. 正常 LLM API Latency 大概由哪些阶段构成？
7. HashMap 与 B+Tree 的底层结构如何解释？
8. RabbitMQ 在异步 AI Backend 中适合承担哪些职责？
9. Coding：找到最短需要排序的连续子数组。

---

## S189 腾讯｜后端 AI 开发｜实习面经｜发布 2026-04-28｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a99d5b46ab7848f992d8ae48a60c009c

真人 / 第一人称证据：作者记录整体面试体验、最终没有后续，并保留“协程只了解携程”的现场自嘲；问题跨实习数据治理、RAG、Network / DB 和 Agent / MCP / Skill。

高价值问题：

1. 实习数据的 Accuracy 与 Timeliness 怎样保证？
2. Metadata / Data Lineage 如何构建并治理？
3. RAG 的完整链路是什么？
4. Process 与 Thread 怎样比较，线程是不是越多越好？
5. CPU 到 Memory 的访问链路怎样理解？
6. TCP 为什么要三次握手，Congestion Control 如何工作？
7. HTTPS 相比 HTTP 增加了哪些协议与安全机制？
8. SQL Slow Query / Index Hit 怎样判断，常见 Index Invalidation 有哪些？
9. Binlog / Redo Log 分别承担什么职责？
10. LLM 与 Agent、MCP 与 Function Calling、Skill 与 Prompt Engineering 如何区分？

---

## S190 小米｜后端 AI 开发｜实习一面 1h｜发布 2026-04-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d856bd790ee24a3c8274a9901c679963

真人 / 第一人称证据：作者以本人一小时 AI Backend 面试分享发布；问题按实习项目 → Redis / MQ → 高并发 → MySQL / Spring → AI Coding / SDD 自然展开。

高价值问题：

1. 为什么项目用 Redis Queue 而不是 RocketMQ，快速上线与可靠性如何权衡？
2. Redis Queue 消息可能丢失时，怎样通过持久化 / 扫描补偿兜底？
3. QPS 上升后读压力如何治理，Cache / WebSocket 等方案怎样选择？
4. Redis HotKey 怎样产生和治理？
5. Bloom Filter 的 False Positive 语义是什么？
6. MVCC 中 Hidden Column、Undo Log、ReadView 如何协作？
7. Spring Circular Dependency 为什么能通过三级缓存处理一部分场景？
8. 公司里怎样使用 AI Coding，同时保证代码规范？
9. SDD / Spec-driven Development 对 AI Coding 有什么工程价值？

---

## S191 美团｜AI 后端开发｜二面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/94492fe4332a4c4984982c315d4353f7

真人 / 第一人称证据：作者以本人 AI 后端二面“攒人品”发布并邀请同岗交流；问题连续围绕项目职责、技术选型、向量库、幂等、Prompt、Production 化、Agent Memory 与 Context 展开。

高价值问题：

1. 项目中本人真正负责哪些模块，技术选型为什么这样做？
2. 为什么使用 Redis，它在当前业务里的职责是什么？
3. Vector DB 在项目中解决什么问题？
4. Backend Storage 怎样设计 Idempotency？
5. Prompt Engineering 有哪些真实落地经验？
6. 单体 Demo 如果真正上线，需要增加哪些 Production 能力？
7. 怎样设计 Agent Memory System？
8. Short-term Context Window 不够时怎样节省 Token？
9. AI Coding 在日常研发中的使用边界是什么？

---

## S192 快手｜Agent 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/be29f78d1c174fe2ab2af85f89f6b792

真人 / 第一人称证据：作者以本人 Agent 一面“发面经攒人品”发布，问题从实习与 AI Coding 进入 Java Concurrency / JVM / HTTPS 基础，并有现场 Coding。

高价值问题：

1. AI Coding 未来可能发展到什么程度，目前最大不足是什么？
2. 什么场景值得使用 Multi-threading？
3. `synchronized` 与 `ReentrantLock` 的差异和适用边界是什么？
4. ThreadLocal 解决什么问题，又可能引入什么风险？
5. Thread Pool Worker 抛异常时会怎样，业务如何感知失败？
6. HTTPS 为什么安全，TLS 大致如何建立安全通道？
7. Java Thread State 怎样变化，线程怎样正确终止？
8. Reflection / Dynamic Proxy 如何实现，什么场景触发 Class Loading？
9. Coding：3Sum。

---

## S193 美团｜AI 全栈开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6d61c76b76ae4213a21b80de8d2c60d7

真人 / 第一人称证据：作者以本人 AI 全栈一面“攒人品”发布；问题从 Network / Process / DB Index 连续进入项目 Degrade 和 Claude Code / Skill / Hook / MCP。

高价值问题：

1. TCP 四次挥手最后一个 ACK 丢失会发生什么，对后续连接有什么影响？
2. Process、Thread、Coroutine 的核心区别是什么？
3. B+Tree 与 B-Tree 为什么在数据库场景表现不同，为什么不用 Red-Black Tree？
4. Optimistic Concurrency Control 如何理解，B+Tree Leaf Split 如何处理？
5. Index Invalidation、Covering Index、Back-to-table 如何联系起来？
6. 项目中的 Circuit Breaker / Degrade 怎样设计？
7. Claude Code 的核心机制、代码执行、Skill 和 Hook 如何理解？
8. MCP 与 Skill 的职责边界是什么？

---

## S194 京东｜后端 Agent 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A

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

## S195 字节跳动｜后端 AI 开发｜暑期二面｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/12cfda50776f482ba03bb775bb720238

真人 / 第一人称证据：作者明确以本人二面凉经发布并更新进入人才库；问题由项目和秒杀一致性继续进入 MySQL、Agent / RAG 与严格输入输出 Coding。

高价值问题：

1. Flash Sale 如何防止 Oversell / Undersell？
2. Redis 扣库存与数据库最终订单状态如何保持一致？
3. Redis 成功但 DB 失败时怎样 Compensation？
4. MySQL Replication、Transaction 和 Isolation 如何影响高并发订单正确性？
5. Agent 的核心组成是什么，为什么不是一次 LLM Call？
6. RAG 的 Retrieval → Generation 链路如何解释？
7. AI Backend 中哪些失败适合 Runtime Deterministic Recovery，哪些可以交给 LLM？
8. Coding：链表求和类变体，并严格处理输入输出与边界条件。

---

## S196 小红书｜AI 应用开发工程师｜技术面｜面试 2026-06-18 16:00｜HUMAN-A

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
- 同一候选人的字节 AI 全栈 9/1 一面与 9/8 二面合并为 S177，一个流程只计一次；
- 字节 Agent 后端 S180 存在题序高度相似的另一版本，只保留有明确二面与横向淘汰结果的来源；
- 同花顺 S182 / S183 经企业页核验为不同账号 / 学校的两位独立候选人，因此不错误合并；
- 小红书 S196 优先保留作者个人博客原文，牛客同步页只作为跨平台回溯证据。

# Batch 09 观察

本批新增 `S169–S196` 共 **28 个 HUMAN-A 来源**，当前干净核心样本达到 **196 个**。

本轮最值得记录的信号：

1. **泛搜索重复率继续上升，但精确搜索仍有显著新增，尚不能停止。** 泛关键词越来越容易返回前八批已收录样本、答案版和聚合页；但企业页 / 话题页 + 公司 / 岗位 / 月份 / 轮次精确搜索仍然一次新增 28 个 HUMAN-A。
2. **完整招聘流程的价值明显高于单篇题单。** 百度 Coding Agent 三轮、字节 AI 全栈一二面等来源让我们能看到问题从项目 / Agent 到 OS / Backend / Coding 随轮次怎样加深；同流程必须合并计数，但轮次内容全部保留。
3. **Coding Agent / Agent Runtime 已稳定进入“可控软件执行系统”层。** Skill Mis-selection、Dynamic Args、Context Isolation、Container Restart Resume、Secret / Sensitive Data Boundary、Sub-agent Token Accounting、Loop Oscillation、Compaction、Prompt Cache 等均有真人独立命中。
4. **AI Backend Foundation 继续被目标岗位直接确认。** MySQL MVCC / Index / Deep Pagination、Redis Lock / Cache / HotKey、MQ Reliability、TCP / HTTPS、Go Context、Java Lock / ThreadPool 等不是传统后端样本混入，而是 AI Backend / Agent Backend 同场真实考察。
5. **项目价值量化成为强验真信号。** 面试官越来越追 QPS、DAU、Cache Hit Rate、节省人力、准确率、Latency、Cost、失败案例与本人贡献，而不是只接受“用了 LangChain / RAG / MCP”。
6. **跨平台原帖回溯有实际收益。** 本轮通过搜索索引找到 Yuki 个人博客的原始小红书 AI 应用面经，证明牛客之外仍有稳定可验证的 HUMAN-A；与此同时，CSDN / 51CTO 等搜索结果大部分仍是转载和营销内容，不能为了平台覆盖率降低门槛。
7. **去重已经必须依赖作者身份与时间线。** 同公司同日并不意味着同一候选人（同花顺一面 / 二面即为不同账号）；相反，同作者跨多个 URL 的同一招聘流程应合并。后续继续坚持 URL + 题序 / 项目语义 + 作者流程三层去重。

停止条件不变：只有连续多轮跨公司、岗位、月份、轮次和平台扩大 Recall 后，**新增 HUMAN-A 的绝对数量与占比都持续接近零**，连精确公司 / 轮次 / 作者页搜索也难以找到新来源，同时新增问题模块和追问深度稳定收敛，才进入最终收尾。Batch 09 的重复率确实继续升高，但一次仍新增 28 个独立 HUMAN-A，因此当前仍明显未达到停止点。
