# Batch 20 一手面试流程

采集日期：2026-09-10

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

