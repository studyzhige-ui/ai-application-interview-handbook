# Batch 20 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **2** 个正式来源。

---

## S246 字节跳动抖音电商｜Agent 全栈开发工程师｜秋招一面｜发布 2026-09-03｜HUMAN-A

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

去重：历史字节 / 抖音来源中存在 GraphRAG、RAG 与 Harness 相关问题，但本作者、页面和“Knowledge 增量更新 → Graph DB vs Vector DB → MySQL 主从 / 索引 → Model Selection → Long-context / Harness → GraphRAG 指标验真 → 数字集合 Coding”连续链未构成历史同场。相邻同作者抖音电商后端页因流程归属不清，主动排除，不为 `S246` 补题。

---

## S247 京东｜AI 后台开发｜实习一面｜发布 2026-04-27｜HUMAN-A

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

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## 本批典型排除 / 重复案例

- **OPPO 历史语义重复**：8/13 `cf5a82411c1e473385d8fcae6c250a6e` 与历史 `S128` 的 `920830730643443712` 几乎整段同序，包括“段落切 Chunk → 证据不足拒答 → Multi-Agent → Long/Short Memory → HTTP Status Code → Hallucination → Frontend → 页面卡顿 → 首次面试”连续链；不论是同作者多 URL 还是复制链，都不新增。
- **小红书 OpenManus 高相似链**：8/9 `223fa82f...` 的“业务指标 → Agent 实际使用 → OpenManus → Harness → Multi-Agent 并发 → Long/Short Memory → ReAct Planner/Executor/Critic”与历史 `S027` 高度重合，无法证明独立，排除。
- **滴滴疑似复制 / 混编**：AI Agent Backend `17ee6ae95cc44ec19b9eefadb69da6b3` 后半段“Redis 单线程 / ZSet / Sentinel / BigKey → Channel vs Mutex → Go 调度 → 实时模糊搜索 → 二维码登录 → 服务发现”与 `S110` 快手原场形成长连续同序链，不能因为公司标题不同就视为独立，排除。
- **腾讯正文不稳定**：4 月 AI Backend `db9014c0dcad4d4d985427e330dc1461` 技术密度很高，但原始正文最终无法稳定完整打开，主要依赖 Search Cache；按硬 Gate 排除。
- **抖音电商同作者相邻双帖**：`925065999378829312` 与 `S246` 同作者、同公司 / 业务且发布时间仅相差约 1 分钟，但题序不同、流程关系无法确认。为避免错误合并或双计，本批只保留能独立成立的 `S246` 页面；相邻页零贡献。
- **内容账号 / 付费包装**：热门搜索中仍有同一账号短时间批量发布快手 / 美团 / PDD 等“完整面经”并伴随付费墙、答案化包装的结果，继续零贡献。
- **历史精确重复**：美团 9/2 AI 后端等结果已是旧库正式来源；热门结果重新出现不新增编号。

---

## Batch 20 信号

1. **热门公司 AI 岗越来越强调“先验真项目，再聊 Agent”。** 快手 `S110` 开场就问项目是不是实习、是否上线、有没有真实用户 / 调用量；候选人坦诚没有生产流量后才继续进入 Memory / Context / Runtime。
2. **AI Backend 仍然是 Backend + Agent 的一体化能力模型。** 小红书 `S010` 一场 75 分钟从 LRU、秒杀、RocketMQ、Redis、MVCC、Index、Deep Pagination 一路问到 Agent Architecture / Memory / RAG / Evaluation；京东 `S247` 也把 MySQL / Redis Cluster 与 Skill Trigger Reliability 放在同一场。
3. **Evaluation 正从 Final Answer 下钻到 Runtime 行为。** Bilibili `S048` 直接问 Deterministic Output 怎样验证、Hook 怎样验证、Bad Case 怎么归因优化，说明 Callback / Hook / Runtime 本身也进入可测试对象。
4. **AI Coding 的考法继续工程化。** 字节 `S083` 不只问“会不会用 AI”，而是追代码质量怎样保证；抖音 `S246` 则继续追 AI 生成 Field / API Design 后人如何 Review 和验收。
5. **GraphRAG 必须证明增益。** 抖音 `S246` 会追 Pure RAG Baseline、GraphRAG Metric、Judge Input，以及哪些 Query 真正需要 Graph DB；仅讲“用了知识图谱”已经不足以通过项目验真。
6. **Context / Memory 与行为可靠性正在合流。** 快手追 Retrieval 冲突与 Memory 分层，B站追 Compaction 后状态保真，京东直接问 Skill 能否 100% 触发；面试关注点从“有没有能力”转为“能力是否可预测、可验证”。
7. **热门公司 Provenance 成本继续上升。** 同场跨 URL、同作者一分钟双帖、换公司标题后大段同序、付费包装都真实出现；热门公司优先必须继续配套更严格的作者 Timeline 与题序核验。

本批新增 **6 个 HUMAN-A：`S083–S247`**。正式库累计 **337 个**，下一编号 **`S248`**。当前整体仍未达到来源饱和；热门公司仍能通过精确日期、作者 Timeline 和历史题序对照找到新独立场次，但普通热门结果页已经具有很高的重复 / 复制 / 包装噪声。
