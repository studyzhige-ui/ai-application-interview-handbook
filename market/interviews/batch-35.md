# Batch 35 — 2026-09-24 Daily HUMAN-A Continuous Monitoring

采集日期：2026-09-24

> 当天 10:00 / 17:00 / 22:00 三次最近 72 小时持续检索合并为一个正式日批次。正式归档前基于最新 `main` 再次逐个直接回读 `market/interviews/batch-01.md`～`batch-34.md` 全历史执行最终去重，确认归档前正式基线为 **34 Batch / 296 HUMAN-A / `S001–S296` / 下一 `S297`**。
>
> 本批正式新增 **1 个 HUMAN-A 独立招聘流程：`S297`**。新增只进入 Market Evidence；Frozen `interview/canonical/`、Frozen `market/analysis/` 与 Curriculum 不因单日新增自动调整。

---

## S297 字节跳动中国交易与广告｜AI 全栈开发工程师｜一面｜面试 2026-09-16，发布 2026-09-24｜HUMAN-A

作者：`牛客826994329号`

来源：https://www.nowcoder.com/discuss/932587389027962880?sourceSSR=dynamic

真人 / 第一人称证据：当天 Afternoon 对 post-specific URL 做精确回读时，可重复取得完整连续正文；作者明确记录本人正式一面，约 1h05min，并保留“面试官全程冷脸、讲实习时皱眉、自己需要继续复习项目”等现场状态。作者主页为南京工程学院 2027 届研发候选人，持续记录 PDD、字节、水滴、亚信安全、视源等本人投递 / 笔面流程，Candidate Timeline 连续，不是批量内容号。Evening 再复核时 post-specific 页面出现临时 Cache Miss，但作者页和当前牛客热榜仍能核验该帖标题 / 招聘时间线，且没有出现转载、镜像或复制链的新反证；因此不因一次抓取波动撤销当天已重复完成的 Stable Original 结论。

Role Scope：标题直接为 `AI全栈开发工程师`；反问明确团队属于字节中国区交易与广告业务，并负责业务的 Agent 相关能力建设。岗位强调借助 AI 完成端到端业务交付，同时要求保留大规模数据、实时 Backend、数据库 / 缓存、一致性与前后端工程判断，符合 AI Full-stack / AI Application 范围。

整场技术链（按当天稳定取得正文的连续语义保留）：

1. AI Pipeline 的业务目标是什么，整体链路怎样组织？
2. Pipeline 每个 Node 的 Accuracy 怎样定义与验证；Hallucination / Deviation 出现时怎样定位和治理？
3. 当前方案为什么这样设计，最终效果怎样 Evaluation；Code Generation Quality 与业务知识准确性分别怎样验证？
4. 大规模数据漏斗 / SQL 链路怎样设计和优化；为什么选择 Doris，而不是 Hive / Elasticsearch 等方案？
5. 面对亿级、十亿级乃至更大规模数据过滤时，Bottleneck 怎样定位；为什么引入 Inverted Index，还有哪些替代方案和继续优化空间？
6. System Design：使用 MQ 实时消息驱动用户隔离轮播时，怎样维护每个用户最近 20 条数据，并支撑持续更新？
7. Redis 与 MySQL 各承担什么职责；为什么仍需要持久化，Cache / Database Consistency 怎样保证？
8. MQ 出现 Duplicate Message 时怎样保证业务 Idempotency？
9. 实时更新场景中 WebSocket 与 Polling 怎样选择；Long Connection 的稳定性、断开和恢复怎样处理？
10. SQL Coding 与 Index Design：怎样根据查询模式设计索引并分析执行性能？
11. 反问：团队当前 Agent 能力建设具体落在哪里；AI 加持下的 Full-stack / Business Ownership 对工程师意味着什么？

最终去重：进入 Inbox 前和 22:00 Finalize 前均按规则直接回读全部正式 `batch-01.md`～`batch-34.md`，并核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义和连续独特题序。历史虽已有 `S036 / S160 / S214 / S246 / S269` 等字节中国交易与广告 / 抖音 AI Application / Agent / Full-stack 来源，但当前作者、9/16 招聘流程、post URL 与“AI Pipeline Quality → Doris / 超大数据优化 → 用户隔离 MQ 轮播 → Redis/MySQL 一致性 → WebSocket → SQL / Index”连续链均独立；未发现同候选人同字节流程或跨平台复制链。GitHub / Search 0 命中只作为辅助，不替代全历史正文回读。

---

# 当日最终清洗 / 明确排除

以下近期结果在 Evening Finalize 后仍然 **零贡献**，没有为了数量降低 Gate：

- **字节剪映 AI 前端一面｜发布 2026-09-22**：公开话题层可看到自研 Agent Framework、为什么不用 LangGraph、ReAct Loop、Tool Registry、`tool_call` JSON Schema、本地 Tool Execution 与 Context 回填等完整技术链；但 post-specific 原帖 / 作者 Timeline 与“AI 前端”实际工作是否属于本库 AI Application Role Scope 仍未同时稳定闭环，继续待追源，不进入 HUMAN-A。
- **携程近期 AI 面试复盘**：公开内容明确属于 AI 自动面试，不满足真人面试官 Gate。
- **`林小白zii`、`AIGC小白入门记` 等批量内容 / 付费面经链**：即使 Agent / Harness / RAG 题目密度很高，也不满足候选人本人原始招聘流程 provenance，排除。
- **近期算法 / SFT / RL / 模型训练岗位、Test / Data / 普通 Backend / Frontend 岗**：仅出现 Agent、MCP、Skill、AI Coding 等术语不能替代目标 Role Scope；不扩大统计边界。
- **宁德时代工业 Agent 近端线索**：招聘现场存在，但公开可核验技术内容过少、信息密度不足，不进入 HUMAN-A。
- **企业聚合、搜索摘要、JD、内推、题库、完整答案、二次整理、博客摘要**：只用于发现线索或市场旁证，不贡献正式来源。

# 2026-09-24 Final Summary

- Discovery window：运行时最近 72 小时，约覆盖 **2026-09-21 22:00 ～ 2026-09-24 22:00** 的新发布 / 更新。
- Morning search effort：**至少 75 组 Query / 变体，20+ 次验证 / 追源**。
- Afternoon search effort：**至少 80 组 Query / 变体，24+ 次验证 / 追源**。
- Evening search effort：**至少 100 组 Query / Query 变体，20+ 次显式原帖 / 作者页 / provenance 打开、回读或追源尝试**。
- Three-round total：**至少 255 组 Query / Query 变体，至少 64 次候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试**；这是工作量次数，不代表 64 个唯一 URL。
- Final additions：**1 个 HUMAN-A：`S297`**。
- Current formal Market library：**35 Batch / 297 HUMAN-A / `S001–S297`**。
- Next ID：**`S298`**。
- Inbox：归档后清空。
- Frozen Canonical / `market/analysis/` / Curriculum：**本日不修改**。

当日主要市场信号：

1. **AI Full-stack 正把 AI Pipeline Quality 与传统大规模系统工程合成同一套能力模型。** 面试不会停在 Agent / RAG 名词，而是继续追 Node Accuracy、Hallucination / Deviation、Code Generation Quality、大数据存储与检索、MQ、Cache / DB Consistency 和实时连接。
2. **Evaluation 越来越靠近业务链路。** “方案是否有效”要分别落到代码生成质量、业务知识准确性、节点质量与端到端结果，而不是只给一个整体准确率。
3. **大规模数据能力仍是 AI Application 的硬底座。** Doris / Hive / ES 选型、Inverted Index、超大规模过滤和 SQL / Index Design 与 Agent 能力建设在同一场出现。
4. **Realtime Backend 与 Agent 产品体验开始强耦合。** 用户隔离 MQ、最近 N 条状态、幂等、WebSocket / Polling 与长连接稳定性成为 AI 全栈的直接考察对象。
5. **Agent 术语继续跨岗位扩散，因此 Role Scope / Provenance Gate 需要继续收紧。** 剪映 AI 前端等新鲜线索技术上很强，但在岗位边界和稳定原始证据没有闭环前仍不能正式计数。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现 **局部饱和 + 高 provenance 成本**。牛客仍是最容易取得稳定第一人称线索的平台，但 post-specific Cache Miss、内容账号、答案化页面和普通岗位 AI 深挖占比很高；字节剪映 AI 前端仍是最值得继续追原帖 / 作者 Timeline 的近端线索。腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客渠道，在当前窗口内没有形成第二个同时满足 HUMAN-A + Role Scope + Stable Original + 全历史去重的新独立流程。继续补盲，但不降低 Gate。
