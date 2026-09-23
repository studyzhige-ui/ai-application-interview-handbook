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

2026-09-23 Morning 在任何候选进入 Inbox 前，已基于当前 `main` **逐个直接回读 `market/interviews/batch-01.md`～`batch-33.md` 全历史**，并核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义与连续题序。正式基线确认如下：

- 正式 Batch：`batch-01.md` ～ `batch-33.md`，共 **33** 个；
- HUMAN-A：`S001–S295`，共 **295** 个；
- 最大编号：`S295`；
- 下一保留编号：**`S296`**；
- 当前 Inbox：**1**；
- Morning 不分配 `Sxxx`、不创建 Batch；
- `interview/canonical/` Frozen Canonical、`market/analysis/` Frozen 统计与 Curriculum 本轮均不修改。

## 当前 Inbox

### 2026-09-23 Morning — 上海联蔚数科｜AI 工程实习生 / Agent｜技术面｜发布 2026-09-21 18:59｜pending Evening Finalize

作者：`牛客488100460号`

来源：https://www.nowcoder.com/feed/main/detail/97ee6dec31b14d12a1f800b709e21a4c

真人 / 第一人称证据：post-specific 原帖可稳定直接回读。作者明确写 `ai工程实习生 25mins`，连续记录本人技术面问题，并保留“面试官没开摄像头”“面试基本问八股”“早知道说做过知识库了”等现场状态。作者主页显示桂林电子科技大学、2026、后端工程师；公开发布目前只有该面经，未出现批量面经 / 订阅 / 标准答案内容账号特征。

Role Scope：标题为上海联蔚数科 Agent 面经，岗位正文直接写 `ai工程实习生`；反问中面试官说明团队当前做 Knowledge Base / Agent，入职后会做调研和 Agent 相关工作。技术主体连续覆盖 Agent Framework、Harness、Skill / MCP、Knowledge Base、Coding Agent、Context Compression、Memory 与 Multi-Agent，明确属于目标 AI Application / Agent 范围。

连续技术问题：

1. 自我介绍。
2. 现在主要使用哪些 AI Tool？
3. 使用过哪些 Agent Development Framework？
4. 怎样理解 Agent？
5. 什么是 Harness？
6. Skill 与 MCP 的区别是什么？
7. 是否自己做过 Skill？
8. Skill / MCP 数量过多时怎样解决 Discovery / Context 压力？
9. 是否做过 Knowledge Base？
10. Coding Agent 怎样做出来的？
11. Coding Agent 有哪些 Tool？
12. Coding Agent 没使用 Framework 时，怎样自己实现 Context Compression 与 Memory Processing？
13. Multi-Agent 怎样实现？
14. 平时怎样学习这些技术？
15. 反问：团队做 Knowledge Base / Agent；实习工作会做调研和 Agent 相关工作。

全历史去重：准入前已直接回读 `batch-01.md`～`batch-33.md` 全历史；未发现当前 URL、作者、上海联蔚数科同招聘流程，也未发现“Agent Framework → Harness → Skill / MCP 数量膨胀 → Knowledge Base → Coding Agent Tool → 无框架 Context Compression / Memory → Multi-Agent”的连续同场来源。GitHub 对 exact URL 与公司名的 0 命中仅作辅助，不替代全历史正文回读。

Morning 处理：**只进入 Inbox，不分配 `S296`，不创建 `batch-34.md`。** 22:00 Finalize 前必须再次直接回读全部正式 Batch 并复核 Stable Original / 作者 provenance / 复制链。
