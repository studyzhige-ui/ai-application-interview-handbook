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

2026-09-24 22:00 Evening + Finalize 已基于最新 `main` **逐个直接回读 `market/interviews/batch-01.md`～`batch-34.md` 全历史**，完成 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、连续独特题序、招聘 Timeline 与复制链核验后，创建当天唯一正式 `batch-35.md`。

- 正式 Batch：`batch-01.md` ～ `batch-35.md`，共 **35** 个；
- HUMAN-A：`S001–S297`，共 **297** 个；
- 最大编号：`S297`；
- 下一保留编号：**`S298`**；
- 当前 Inbox：**0**；
- 2026-09-24 正式新增：**`S297` 字节跳动中国交易与广告｜AI 全栈开发工程师｜一面**；
- `interview/canonical/` Frozen Canonical、`market/analysis/` Frozen 统计与 Curriculum 本日均不修改。

## 当前 Inbox

**空。** 2026-09-24 的唯一通过候选已在 Evening Finalize 后归入 `market/interviews/batch-35.md / S297`；未通过 Stable Original、Candidate Provenance、Role Scope 或全历史去重 Gate 的近端线索不保留在 Inbox。
