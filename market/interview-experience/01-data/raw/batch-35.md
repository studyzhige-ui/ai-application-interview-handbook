# Batch 35 一手面试流程

采集日期：2026-09-24

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

