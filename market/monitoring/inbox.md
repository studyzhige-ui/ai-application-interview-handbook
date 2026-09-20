# HUMAN-A Monitoring Inbox

更新日期：2026-09-20

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

2026-09-20 17:00 Afternoon Search 写入前已再次逐个直接回读 `market/interviews/batch-01.md` ～ `batch-30.md` 全历史，并确认：

- 正式 Batch：`batch-01.md` ～ `batch-30.md`，共 **30** 个；
- HUMAN-A：`S001–S289`，共 **289** 个；
- 最大编号：`S289`；
- 下一保留编号：**`S290`**；
- Afternoon 不分配 `Sxxx`、不创建 Batch；
- `interview/canonical/` Frozen Canonical、`market/analysis/` Frozen 统计与 Curriculum 本轮均不修改。

## 当前 Inbox

### Candidate A — 小红书｜AI 全栈开发实习｜一面｜面试 2026-08-25，发布 2026-09-18 15:43｜HUMAN-A

作者：`中二的西红柿起床了`

来源：https://www.nowcoder.com/feed/main/detail/c712eda7fbf44ba69835b6dd2ff7fc4c?sourceSSR=enterprise

真人 / 第一人称证据：post-specific 原始正文可稳定直接回读。作者明确写“回忆一下”“大部分时间都在问项目”，保留“面试官不断提问让我说服他”“我终于投降了”“一面挂”等本人现场状态；同一账号还存在长期个人求职 / 学业记录和本周 Shopee 本人面经，个人候选人 Timeline 成立，不是批量内容号。

Role Scope：标题直接标注 `小红书实习 AI全栈开发实习一面`；40 分钟主体持续围绕 Multi-Agent、Skill、RAG / Vector DB、Harness 与 Evaluation / Outcome 验真，明确属于 AI Full-stack / Agent 应用范围。

代表性技术链：

1. 项目做什么、为什么要做成 Multi-Agent、怎样编排？
2. 面试官持续追问为什么 Multi-Agent 真有必要，要求候选人证明 Architecture Choice，而不是只报框架名。
3. Skill 是什么，在项目中承担什么？
4. RAG 怎样实现、Vector Database 怎样使用？
5. 是否了解 Harness？
6. 继续验真项目：怎样评测、真实成果是什么、同事是否反馈、准确率怎样、是否做过指定功能；候选人对未覆盖部分明确承认没有想到。
7. 反问；无手撕、无传统八股，项目深挖约 40 分钟，一面未通过。

去重：进入 Inbox 前已逐个直接回读 `batch-01.md`～`batch-30.md`。未发现该 URL、作者，或“Multi-Agent 必要性反复论证 → Skill → RAG / Vector DB → Harness → Evaluation / 同事反馈 / 准确率验真”的连续同场来源。GitHub exact URL / 作者搜索 0 命中仅作辅助证据。

### Candidate B — Shopee｜Chatbot 研发实习｜一面｜面试 2026-09-18，发布 2026-09-19 16:25｜HUMAN-A

作者：`中二的西红柿起床了`

来源：https://www.nowcoder.com/feed/main/detail/9f02a7f8009d4aca9fc730a18b9f96cc

真人 / 第一人称证据：post-specific 原始正文可稳定直接回读。作者逐题记录本人回答、停顿和不会的状态：第 K 大先回答排序，被继续追 Quick Sort 复杂度 / 原理 / 手写，随后明确记录“不会”“发呆”，最后用 `sort` 两行完成；文末写全程 20 多分钟和面后自评，现场痕迹强。与 Candidate A 为同一候选人、但不同公司独立招聘流程，按规则可分别暂存。

Role Scope：岗位标题为 `chatbot研发实习`，技术主体连续覆盖 Agent、Function Call / Tool / MCP、RAG、AI Coding，再混合 Linux 与算法基础；实际面试职责明确属于 AI Application / Agent 类 Chatbot 研发，而非普通后端顺带问 AI。

代表性技术链：

1. 什么是 Agent？
2. Function Call、Tool、MCP 分别是什么、怎样区分？
3. 项目 RAG 怎样做，承载多大文档？
4. Linux 常用命令，怎样查看 Process？
5. Coding：数组第 K 大；从“排序后取第 K 个”继续追 Quick Sort 复杂度、排序机制与手写实现，再追其它方法。
6. 平时怎样 AI Coding，有什么实际方法？
7. 反问；整场 20 多分钟。

去重：进入 Inbox 前已直接回读全部 30 个正式 Batch。历史虽有 Shopee `S081` / `S239` 等 Agent 场次，但作者、月份 / 日期、岗位流程、项目与连续题序不同；当前 URL 和作者未在正式库出现，没有同场或复制链证据。GitHub exact URL 搜索 0 命中仅作辅助。

## 当前状态

Afternoon Search 结束后：**Inbox 共 2 个候选流程，尚未分配任何 `Sxxx`。** 22:00 Finalize 必须重新直接回读全部正式 Batch，并再次核验两个来源是否仍稳定、是否出现更早 canonical source / 同流程后续轮次 / 复制链，再决定是否从当前真实下一编号 `S290` 连续归档。
