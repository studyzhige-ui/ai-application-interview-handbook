# HUMAN-A Monitoring Inbox

更新日期：2026-09-19

本文件只保存**已经满足 HUMAN-A、但尚未归入当天正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

> **当前状态：🟢 Continuous Monitoring。** 每天三次搜最近 3 天的新面经；当天三次检索只形成一个日批次。10:00 / 17:00 只暂存已通过 Gate 的候选，22:00 重新做全历史去重后再统一分配 `Sxxx`。

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

通过岗位准入后，整场真实技术问题都保留，包括 Python / Java / Go、FastAPI、MySQL、Redis、MQ、Network、Concurrency、Vector DB、LLM、RAG、Agent、MCP / Skill / Memory / Harness、AI Coding、System Design 等；不使用普通后端 / 普通前端 / 纯训练 Infra 面经人为补频率。

任何候选进入 Inbox 或分配 `Sxxx` 前，都必须直接回读全部历史 Batch，并同时核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、至少 5–10 个连续独特题序、招聘 Timeline、跨平台镜像与复制链。GitHub / Search 的 0 命中不能证明未收录。

- 同候选人同公司同招聘流程多轮 → 合并一个来源；
- 同候选人不同公司 / 独立流程 → 可以分别计数；
- 不同 URL 但题序 / 项目语义高度一致 → 继续追源；
- 复制链原场不确定 → 整链排除；
- 原文不能稳定打开 → 零贡献。

## 当前正式基线

2026-09-19 22:00 Finalize 后：

- 正式 Batch：`batch-01.md` ～ `batch-30.md`，共 **30** 个；
- HUMAN-A：`S001–S289`，共 **289** 个；
- 最大编号：`S289`；
- 下一保留编号：**`S290`**；
- 最近正式新增：`S289`，共 **1** 个；
- `S280–S289` 的 Canonical 映射留待 periodic review，不因单日热点修改 Curriculum。

## 当前 Inbox

**空。** 2026-09-19 当日候选已完成 22:00 Finalize；未通过稳定原帖 / 作者归属 / Role Scope / 技术密度 / 去重 Gate 的线索不在此文件暂存。

## 最近一次已归档

2026-09-19 Afternoon 暂存的阳光电源 AI 应用开发工程师一面已在 22:00 再次直接回读全部历史 Batch 并完成最终去重，归入 `batch-30.md`：

`S289` 阳光电源｜AI 应用开发工程师｜一面（作者 `小红不是绿`）。

未通过稳定原帖 / 作者归属 / Role Scope / 技术密度 / 去重 Gate 的高密度线索继续不进入 Inbox；如后续补齐证据，必须从头重新执行 HUMAN-A 与全历史去重，而不是沿用旧搜索摘要直接升级。
