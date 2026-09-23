# HUMAN-A Monitoring Inbox

更新日期：2026-09-23

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

2026-09-23 22:00 Finalize 前，已基于最新 `main` **逐个直接回读 `market/interviews/batch-01.md`～`batch-33.md` 全历史**，并核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义与连续题序；随后将当日唯一最终通过者归档到 `batch-34.md`。

- 正式 Batch：`batch-01.md` ～ `batch-34.md`，共 **34** 个；
- HUMAN-A：`S001–S296`，共 **296** 个；
- 最大编号：`S296`；
- 下一保留编号：**`S297`**；
- 当前 Inbox：**0**；
- `interview/canonical/` Frozen Canonical、`market/analysis/` Frozen 统计与 Curriculum 本轮均不修改。

## 当前 Inbox

当前为空。下一轮只把新通过 HUMAN-A + Role Scope + Stable Original + 全历史去重的候选暂存到这里；Morning / Afternoon 不分配新编号。