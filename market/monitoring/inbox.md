# HUMAN-A Monitoring Inbox

更新日期：2026-09-24

本文件只保存**已经满足 HUMAN-A、但尚未归入当天正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

> **当前状态：🟢 Continuous Monitoring。** 每天三次搜最近 3 天的新面经；10:00 / 17:00 只暂存已通过 Gate 的候选，22:00 重新做全历史去重后再统一分配 `Sxxx`。

## 固定准入与去重

正式候选必须同时满足：

```text
真人面试官
+ 候选人本人第一人称
+ 高技术密度
+ 真实现场 / 招聘流程痕迹
+ AI Application / Agent Role Scope
+ 原始正文稳定可核验
+ 非转载 / 合集 / 内容号 / 答案帖 / AI 自动面试 / 重复
= HUMAN-A
```

通过岗位准入后，整场真实技术问题都保留；同候选人 + 同公司 + 同招聘流程多轮合并一个 Source，不按轮次虚增 Source Count。搜索 0 命中不能证明未收录，任何新增正式编号前必须直接回读全部历史 Batch。

## 当前正式基线

2026-09-24 17:00 Afternoon 在候选进入 Inbox 前，已基于最新 `main` **逐个直接回读 `market/interviews/batch-01.md`～`batch-34.md` 全历史**，并核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义与连续题序。

- 正式 Batch：`batch-01.md` ～ `batch-34.md`，共 **34** 个；
- HUMAN-A：`S001–S296`，共 **296** 个；
- 最大编号：`S296`；
- 下一保留编号：**`S297`**；
- 当前 Inbox：**1**；
- `interview/canonical/` Frozen Canonical、`market/analysis/` Frozen 统计与 Curriculum 本轮均不修改。

## 当前 Inbox

### 2026-09-24 Afternoon — 字节跳动中国交易与广告｜AI 全栈开发工程师｜一面｜pending Evening Finalize

作者：`牛客826994329号`

来源：https://www.nowcoder.com/discuss/932587389027962880?sourceSSR=dynamic

面试：2026-09-16；发布：2026-09-24；校招正式一面，约 1h05min。

HUMAN-A / Provenance：post-specific URL 在本轮精确检索中可重复取得完整连续正文；作者主页为南京工程学院 2027 届研发候选人，长期记录本人 PDD、字节、水滴、亚信安全、视源等投递 / 笔面流程，具有连续 Candidate Timeline，不是批量内容号。正文保留“面试官全程冷脸、讲实习时皱眉、自己需要继续复习项目”等现场状态。

Role Scope：标题直接为 `AI全栈开发工程师`；反问明确团队属于字节中国区交易与广告业务，并负责“业务的 Agent 相关能力建设”，公司对该岗位的定位是借助 AI 做端到端业务交付，同时要求保留底层工程判断能力，符合 AI Full-stack / AI Application 范围。

代表性技术链：

1. AI Pipeline 的业务目标、每个 Node 的准确性、Hallucination / Deviation 如何治理；
2. Pipeline 方案来源、最终效果怎样 Evaluation，Code Generation Quality 怎样验证，业务知识准确性怎样保证；
3. 大规模数据漏斗与 SQL 优化，为什么选择 Doris 而非 Hive / ES；
4. 亿级 / 十亿级乃至千亿级数据过滤时怎样定位 Bottleneck、为什么加 Inverted Index、替代方案与进一步优化是什么；
5. System Design：MQ 实时消息驱动的用户隔离轮播，如何维护每用户最近 20 条；
6. Redis + MySQL 的职责、为什么需要持久化、缓存 / 数据库一致性与 MQ 重复消息幂等；
7. WebSocket vs Polling，长连接稳定性如何处理；
8. SQL Coding 与 Index Design；
9. 反问确认团队 Agent 能力建设，以及 AI 加持下端到端 Full-stack / Business Ownership 的岗位预期。

全历史去重：进入 Inbox 前已直接回读 `batch-01.md`～`batch-34.md`。历史虽有 `S036 / S160 / S214 / S246 / S269` 等字节中国交易与广告 / 抖音 AI Application / Agent / Full-stack 来源，但当前作者、9/16 招聘流程、post URL 与“AI Pipeline Quality → Doris / 超大数据优化 → 用户隔离 MQ 轮播 → Redis/MySQL 一致性 → WebSocket → SQL / Index”连续题序均独立；未发现同候选人同字节流程。GitHub 对 exact URL、作者与罕见题序的 0 命中仅作为辅助，不替代全历史正文回读。

状态：**通过 Afternoon HUMAN-A + Role Scope + Stable Original + 全历史去重 Gate，等待 22:00 Finalize 再次回读全历史后决定是否分配当前真实下一 `Sxxx`。**
