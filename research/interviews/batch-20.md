# Batch 20 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S332` 继续编号，并继续按用户要求把搜索预算集中在**热门公司**：字节、腾讯、美团、快手、小红书、拼多多、京东、滴滴、Bilibili、OPPO / vivo / 小米等。公司热度不构成质量加分，正式来源仍必须同时满足：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非重复 = HUMAN-A**。
>
> 分配编号前重新确认 `main` 为 Batch 19 基线 `S001–S331`，并直接回读最新 Batch 与相关历史 Batch，逐条核对 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、5～10 个连续题序特征和招聘 Timeline。Code Search 的 0 命中仍然只作辅助，不作为“未收录”证明。
>
> 本轮再次证明热门公司搜索中的复制 / 混编风险很高：OPPO 8/13 候选与历史 `S154` 几乎整段同序，因此撤出；滴滴 AI Agent Backend 后半段与快手原场形成长连续同序链，撤出；腾讯 4 月强候选只能稳定取得搜索缓存、原始正文无法完整打开，按稳定正文 Gate 排除；同一作者一分钟内发布两篇抖音电商场次且流程关系不清时，只保留能独立成立的 Agent 全栈原帖，不让相邻页面贡献问题。

---

## S332 字节跳动｜Agent 开发｜秋招一面｜面试 2026-08-12，发布 08-24，1h+｜HUMAN-A

来源：https://www.nowcoder.com/discuss/921444774287003648

真人 / 第一人称证据：作者以本人秋招面试记录发布，明确给出 8 月 12 日、Agent 开发与一小时以上时长；问题从候选人自己的三个项目中任选一个深挖，再进入 RAG、AI Coding、Streaming、高并发场景和现场 Coding。候选人记录了面试官对算法方案继续追问线程安全，具有自然现场互动，而不是答案型题单。

整场技术问题：

1. 三个项目中任选一个完整说明：业务目标、技术链路、本人职责和关键难点是什么？
2. 项目里是否真正做过 RAG，完整实现链路怎样组织？
3. 使用 AI Coding 时，怎样让生成代码达到更高质量，而不是只追求生成速度？
4. AI 生成代码怎样做正确性、可维护性和测试验证？
5. SSE 与 WebSocket 的通信模型、连接方向和适用场景有什么差异？
6. 数据库常见 Index 有哪些，索引为什么能够加速查询，选型时关注什么？
7. 场景题：实时更新一个高并发热门榜单，数据结构和存储层怎样设计？
8. 高并发排行榜中，排序更新、读取热点和持久化分别可能出现什么瓶颈？
9. Coding：使用两个 Stack 实现 Queue。
10. 在上一题基础上继续追：多线程并发访问时怎样保证线程安全？

去重：URL 未在 `S001–S331` 正式库出现；历史字节 Agent 来源虽然大量涉及 RAG / Context / Coding，但本场“项目任选深挖 → RAG → AI Coding 质量 → SSE/WebSocket → 高并发排行榜 → 两栈队列 + 线程安全”的连续题序、作者与 8/12 流程均独立。

---

## S333 快手｜Agent 开发｜日常实习一面｜发布 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ce1b038c57c44cc08464561a8cfa0434

真人 / 第一人称证据：作者 `等个消息橘子` 的主页只有极少个人求职内容，不是面经内容账号。本场面试官先连续验真候选人的 Agent 项目是否来自实习、是否真正上线、有没有真实用户和调用量；作者直接承认项目主要是个人 / 校园场景、没有生产业务流量。之后问题从 Memory / Context / ReAct 进入 Go、Redis 与后端系统设计，现场验真痕迹很强。

整场技术问题：

1. Agent 项目是不是实习项目，是否真正上线？
2. 有没有真实用户、真实调用量或生产业务数据，如何证明项目不是 Demo？
3. 为什么设计 Long-term Memory 与 Short-term Memory，两者各自解决什么问题？
4. 哪些信息应该进入长期记忆，哪些只保留在当前会话 / 短期状态？
5. Context Window 不够时，截断、摘要和 Retrieval 分别有什么代价，怎样选？
6. 当前 Agent 使用 ReAct 还是 Workflow，为什么这样设计？
7. Tool Call 失败、超时或返回异常时怎样处理？
8. Retrieval 返回互相矛盾的证据时，模型应该信谁，如何做冲突消解和 Verification？
9. Go Channel 是否线程安全，它与 Mutex 分别适合什么并发场景？
10. GMP 调度怎样理解；当前 P 的本地队列为空时如何继续获取任务？
11. Redis 为什么快，常见数据结构和典型场景有哪些？
12. System Design：实现类似淘宝搜索框的实时模糊联想 / 自动补全。
13. 二维码登录从生成二维码、扫码确认到 Web 端登录完成的完整链路是什么？
14. Service Registration / Discovery 如何工作，Nacos / Consul 的 Heartbeat 与实例失效怎样处理？
15. Coding / 并发题：有 100 个任务 ID，最多只允许 3 个任务同时调用外部 API，怎样实现并发控制？

去重：另发现 `bec7cc3ac12c464eaa2361f99040ed1a` 明确以招聘账号“转 @等个消息橘子：快手 Agent 开发一面”的方式复用本帖，只作为转载证据、零贡献。当前原帖的“生产验真 → Memory / Context → ReAct → Tool Failure → Go Channel / GMP → Redis → 模糊搜索 → 二维码登录 → 服务发现 → 限并发”题序未在历史快手来源出现。

---

## S334 小红书｜AI 后端开发｜秋招一面｜面试 2026-08-13，发布 08-20，75min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/169b2d8f7a134843b114b820ee692186

真人 / 第一人称证据：作者明确记录 8 月 13 日约 75 分钟 AI 后端一面，现场一开始就做算法，随后被长时间追秒杀、RocketMQ、Redis、MySQL，再进入实习平台、Agent 与 RAG。面后作者记录面试官反馈“多数能答，但缺少更深入思考”，具有强候选人现场状态。虽然基础后端问题占比很高，但后半场明确围绕 Agent Architecture / Memory / Intent / RAG / Evaluation，符合 AI Backend Role Scope；因此按规则保留整场技术问题。

整场技术问题：

1. Coding：实现 LRU Cache。
2. 为什么 LRU 通常使用 HashMap + Doubly Linked List，为什么不是单链表？
3. 除 LRU 外还了解哪些 Cache Eviction Policy，业务中怎样选择？
4. 秒杀 / 抢购场景最容易出现哪些并发与一致性问题，整体方案怎样设计？
5. RocketMQ Transactional Message 如何工作？
6. 为什么部分原子业务逻辑使用 Redis Lua？
7. Lua 为什么能在 Redis 中保证当前脚本执行的原子性？
8. MQ 在秒杀链路中承担削峰、异步和解耦中的哪些职责？
9. Redis 扣库存成功后，用户怎样最终获知数据库侧订单成功或失败？
10. Redis 预扣成功但 DB 写入失败时，一致性怎样恢复？
11. Optimistic Lock 的核心机制是什么，在库存更新中怎样实现？
12. Redis Set 的底层编码 / 数据结构怎样理解？
13. Redis 常见数据结构分别适合什么场景？
14. ZSet 使用 SkipList 时查询 / 插入复杂度怎样分析？
15. MySQL MVCC 的基本机制是什么？
16. MVCC 主要解决什么并发读写问题？
17. MySQL 四种 Isolation Level 分别是什么，适用场景和现象有什么差异？
18. 针对给定 SQL 怎样设计 Composite Index；如果查询不再使用 `user_id`，原索引还能否有效利用？
19. 联合索引中出现 Range Condition 后，后续字段为什么可能无法继续用于完整索引定位？
20. MySQL Index 的底层结构是什么，什么叫 Back-to-table Lookup？
21. 三层 B+Tree 大致能容纳多少行数据，估算依据是什么？
22. B+Tree 查询复杂度怎样理解？
23. 为什么数据库索引更常使用 B+Tree，而不是普通 B-Tree？
24. 大 Offset 的 `LIMIT` 为什么慢，怎样优化 Deep Pagination？
25. 使用子查询 / 覆盖索引优化深分页后为什么可能更快？
26. 当前秒杀方案是否已经完整解决问题，还有哪些边界和替代方案？
27. 实习中的 Coda 平台项目背景、工作原理、业务价值和本人职责是什么？
28. 怎样理解 Agent，一套完整 Agent Design 至少有哪些关键阶段？
29. Agent Memory 在什么时候写、什么时候读、一次应该取多少？
30. 了解哪些 Agent Execution Mode，不同模式怎样选择？
31. Agent Intent Recognition 不准确时，可以从哪些层优化？
32. RAG 是否真正落地过，知识来源、Retrieval 和 Generation 怎样组织？
33. 怎样评价 RAG 质量以及 Agent / Model 的整体效果？
34. RAG 不准确时，Parsing、Chunk、Embedding、Recall、Rerank、Prompt 分别怎样排查和优化？

去重：历史 `S153 / S200` 是另一条 8/7 小红书 AI 后端同 URL，重点为 HotKey / Watchdog / Deep Pagination → Agent / RAG；当前来源为不同日期、作者和招聘流程，并具有“秒杀 → RocketMQ Transactional Message → Lua → Optimistic Lock → MySQL 全链 → Coda 实习 → Agent / RAG”的独立题序。历史 `S260` 的 OpenManus / Harness 流程也与本场不同。

---

## S335 Bilibili｜Agent 开发｜一面 + 二面（同一候选人同流程合并）｜面试 2026-08-11 / 08-13，发布 08-19｜HUMAN-A

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

去重：历史 `S201` 为另一候选人的开源 Coding Agent 修复 / `ripgrep` / Sandbox / Skill Progressive Disclosure；`S202` 为另一候选人的 AIGC Video + Network / Redis / Dify / Tooling 场次。当前作者、项目、8/11→8/13 Timeline 和“cGroup / A2A / Compaction → Deterministic Verification / Hook Validation / Bad Case Attribution”题序均独立。

---

## S336 字节跳动抖音电商｜Agent 全栈开发工程师｜秋招一面｜发布 2026-09-03｜HUMAN-A

来源：https://www.nowcoder.com/discuss/925066865183858688

真人 / 第一人称证据：作者 `月野a` 以本人抖音电商 Agent 全栈一面记录发布，问题持续围绕自己在百度参与的 Knowledge Graph / GraphRAG 与 AI Engineering 工作深挖，面试官多次追“本人真正做了什么、指标怎样提升、不同数据与模型为什么这样选”，并有现场 Coding。作者同一分钟附近还发布了另一条抖音电商“后端一面”，但两篇招聘流程关系无法稳定确认；本库不猜同场 / 不同场，只把本页能独立核验的问题作为一个来源，另一页不计数也不贡献题目。

整场技术问题：

1. Knowledge Construction 与 Graph Extraction 的完整链路是什么？
2. 文档来源是全量 Crawl、业务同步还是用户 Upload，各自怎样进入 Knowledge Pipeline？
3. Knowledge Base 更新是否每天全量重建，为什么？
4. 单篇文档发生更新时，Entity Extraction、Relationship Linking 和 Index Update 怎样局部执行？
5. 数据更新后如何避免旧 Entity / Edge 与新版本产生冲突？
6. Retrieval 做过哪些真实优化，如何证明收益？
7. Graph Database 与 Vector Database 分别适合什么 Query / Retrieval 场景？
8. 日常主要使用什么 Programming Language，为什么？
9. AI Coding 在真实工作中的代码占比大概怎样，人负责哪些 Review / Verification？
10. 当模型生成 Field Description、API Design 或其它工程结构时，完整协作 Workflow 怎样组织？
11. 与 Model 交互时 Message / Dialogue Format 怎样设计，常用哪些 Tool？
12. MCP 应怎样理解，它是否只是普通 Middleware，真正的协议价值是什么？
13. MySQL Primary-Replica Replication 怎样工作？
14. Read Request 是否应该走 Replica，怎样处理延迟和一致性？
15. 系统是否一定需要 Multi-DC / Multi-machine / Multi-database，怎样按规模判断？
16. 实际做过哪些 Index Design，常见 Index Invalid / Not-used 原因是什么？
17. 不同业务场景为什么选择不同基础模型，Model Selection 看哪些效果 / Latency / Cost 信号？
18. Long-context Model 能缓解什么问题，又不能替代哪些 Context Engineering？
19. 第 11 轮对话时，前 10 轮 History 应怎样裁剪、摘要或检索后重新注入？
20. 怎样理解 Harness Engineering？
21. 随着基础模型能力增强，Harness 应该变薄还是变厚，哪些确定性能力不能交回模型？
22. 在百度做过最难、最成功的工程工作是什么？
23. Graph Construction 中哪些部分是本人实现，哪些来自团队已有框架 / Open Source？
24. Graph Extraction 做过哪些多轮调优？
25. GraphRAG 相比 Pure RAG 的指标提升是多少，Dataset、Baseline 与 Metric 怎样定义？
26. 让 LLM Judge 评价检索 / 回答时，具体给 Judge 什么 Input，怎样避免评测失真？
27. 哪些问题真正适合 Graph DB，而不是 Vector Retrieval？
28. Coding：给定可用数字集合 A，构造严格小于 N 的最大整数。

去重：历史字节 / 抖音来源中存在 GraphRAG、RAG 与 Harness 相关问题，但本作者、页面和“Knowledge 增量更新 → Graph DB vs Vector DB → MySQL 主从 / 索引 → Model Selection → Long-context / Harness → GraphRAG 指标验真 → 数字集合 Coding”连续链未构成历史同场。相邻同作者抖音电商后端页因流程归属不清，主动排除，不为 `S336` 补题。

---

## S337 京东｜AI 后台开发｜实习一面｜发布 2026-04-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/cab1b416e74f43de936c8c41d51c011e

真人 / 第一人称证据：作者以本人京东 AI 后台开发一面复盘发布，结尾直接写“感觉面完人都通透了，还是太菜了，下去沉淀”，具有明显候选人状态；问题从项目继续进入 MySQL、Redis，再转向 Agent 范式、Context Engineering、Skill / MCP / Rule 与行为可靠性，属于目标 AI Backend 场次而非普通后台顺带问 AI。

整场技术问题：

1. 围绕简历项目做技术深挖：本人负责什么、关键链路如何工作？（原帖未展开具体项目题序，不做额外推断。）
2. 为什么 MySQL Primary Key 通常适合 Auto-increment，这对 B+Tree / Page Split 有什么影响？
3. 秒杀量级很大、Single-node Redis 扛不住时，可以怎样扩展？
4. Redis Cluster 模式下执行 Lua Script 会遇到哪些 Key Slot / Consistency 问题，怎样处理？
5. 怎样看 Agent 的演进方向，它未来真正能替代 / 完成哪些工作？
6. 常见 Agent Execution Pattern 有哪些，ReAct 的完整循环是什么？
7. 什么场景值得使用 SubAgent，而不是继续堆一个主 Agent？
8. 复杂工程规则很多时，怎样约束 AI 遵守项目规范和业务限制？
9. Context Engineering、Skill、MCP、Rule 分别解决什么问题，边界怎样划分？
10. Skill 被写进系统后，能否保证 100% 被模型正确触发？如果不能，工程上怎样增强可靠性？

去重：历史 `S056` 为 4/14 京东 AI 应用开发，围绕真实部署、企业 Knowledge Base、Model Selection、指标和 Query Decomposition；当前作者与流程不同，题序为“MySQL Auto-increment → Redis Cluster / Lua → Agent Pattern / ReAct / SubAgent → Context Engineering / Skill / MCP / Rule → Skill Trigger Reliability”，确认独立。

---

## 本批典型排除 / 重复案例

- **OPPO 历史语义重复**：8/13 `cf5a82411c1e473385d8fcae6c250a6e` 与历史 `S154` 的 `920830730643443712` 几乎整段同序，包括“段落切 Chunk → 证据不足拒答 → Multi-Agent → Long/Short Memory → HTTP Status Code → Hallucination → Frontend → 页面卡顿 → 首次面试”连续链；不论是同作者多 URL 还是复制链，都不新增。
- **小红书 OpenManus 高相似链**：8/9 `223fa82f...` 的“业务指标 → Agent 实际使用 → OpenManus → Harness → Multi-Agent 并发 → Long/Short Memory → ReAct Planner/Executor/Critic”与历史 `S260` 高度重合，无法证明独立，排除。
- **滴滴疑似复制 / 混编**：AI Agent Backend `17ee6ae95cc44ec19b9eefadb69da6b3` 后半段“Redis 单线程 / ZSet / Sentinel / BigKey → Channel vs Mutex → Go 调度 → 实时模糊搜索 → 二维码登录 → 服务发现”与 `S333` 快手原场形成长连续同序链，不能因为公司标题不同就视为独立，排除。
- **腾讯正文不稳定**：4 月 AI Backend `db9014c0dcad4d4d985427e330dc1461` 技术密度很高，但原始正文最终无法稳定完整打开，主要依赖 Search Cache；按硬 Gate 排除。
- **抖音电商同作者相邻双帖**：`925065999378829312` 与 `S336` 同作者、同公司 / 业务且发布时间仅相差约 1 分钟，但题序不同、流程关系无法确认。为避免错误合并或双计，本批只保留能独立成立的 `S336` 页面；相邻页零贡献。
- **内容账号 / 付费包装**：热门搜索中仍有同一账号短时间批量发布快手 / 美团 / PDD 等“完整面经”并伴随付费墙、答案化包装的结果，继续零贡献。
- **历史精确重复**：美团 9/2 AI 后端等结果已是旧库正式来源；热门结果重新出现不新增编号。

## Batch 20 信号

1. **热门公司 AI 岗越来越强调“先验真项目，再聊 Agent”。** 快手 `S333` 开场就问项目是不是实习、是否上线、有没有真实用户 / 调用量；候选人坦诚没有生产流量后才继续进入 Memory / Context / Runtime。
2. **AI Backend 仍然是 Backend + Agent 的一体化能力模型。** 小红书 `S334` 一场 75 分钟从 LRU、秒杀、RocketMQ、Redis、MVCC、Index、Deep Pagination 一路问到 Agent Architecture / Memory / RAG / Evaluation；京东 `S337` 也把 MySQL / Redis Cluster 与 Skill Trigger Reliability 放在同一场。
3. **Evaluation 正从 Final Answer 下钻到 Runtime 行为。** Bilibili `S335` 直接问 Deterministic Output 怎样验证、Hook 怎样验证、Bad Case 怎么归因优化，说明 Callback / Hook / Runtime 本身也进入可测试对象。
4. **AI Coding 的考法继续工程化。** 字节 `S332` 不只问“会不会用 AI”，而是追代码质量怎样保证；抖音 `S336` 则继续追 AI 生成 Field / API Design 后人如何 Review 和验收。
5. **GraphRAG 必须证明增益。** 抖音 `S336` 会追 Pure RAG Baseline、GraphRAG Metric、Judge Input，以及哪些 Query 真正需要 Graph DB；仅讲“用了知识图谱”已经不足以通过项目验真。
6. **Context / Memory 与行为可靠性正在合流。** 快手追 Retrieval 冲突与 Memory 分层，B站追 Compaction 后状态保真，京东直接问 Skill 能否 100% 触发；面试关注点从“有没有能力”转为“能力是否可预测、可验证”。
7. **热门公司 Provenance 成本继续上升。** 同场跨 URL、同作者一分钟双帖、换公司标题后大段同序、付费包装都真实出现；热门公司优先必须继续配套更严格的作者 Timeline 与题序核验。

本批新增 **6 个 HUMAN-A：`S332–S337`**。正式库累计 **337 个**，下一编号 **`S338`**。当前整体仍未达到来源饱和；热门公司仍能通过精确日期、作者 Timeline 和历史题序对照找到新独立场次，但普通热门结果页已经具有很高的重复 / 复制 / 包装噪声。