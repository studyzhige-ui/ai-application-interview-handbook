# HUMAN-A Monitoring Inbox

更新日期：2026-09-10

本文件只保存**已经满足 HUMAN-A、但尚未归入正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

## 固定准入标准

新的 Inbox 候选必须同时满足：

1. **真人面试官**：真人技术面 / Leader 面 / 项目深挖；
2. **候选人本人第一人称**：不是整理、搬运、代发、投稿或内容账号包装；
3. **高信息密度**：具体技术问题和追问足够丰富；
4. **真实现场痕迹**：答题状态、引导、打断、轮次、结果、Coding / Demo / 屏幕共享等可核验；
5. **Role Scope Gate**：AI Application、Agent、RAG、AI Backend、AI Full-stack、Applied AI、FDE、Agent Runtime / Harness / Coding Agent 等目标方向；
6. **正文稳定可核验**：原始正文和 URL 可实际访问；
7. **非重复**：不是转载、合集、跨平台同场、后发复制、换公司标题同序或不确定复制链。

```text
真人面试官
+
候选人本人第一人称
+
高信息密度
+
真实现场 / 招聘流程痕迹
+
目标 AI Application / Agent 岗位
+
正文稳定可核验
+
非转载 / 非合集 / 非内容账号 / 非答案帖 / 非重复
=
HUMAN-A
```

任意一项不满足都不进入 Inbox、正式 Batch、Canonical Question、频率统计或课程优先级。

## 通过岗位准入后：整场真实技术问题保留

```text
Python / FastAPI / ASGI / asyncio
Java / Spring / Go / JavaScript / React
MySQL / Redis / Vector Database
LLM Foundation / RAG
Agent / MCP / Skill / Tool / Memory
Agent Harness / Runtime
System Design
OS / Network / Concurrency
MQ / Kafka
HTTP / SSE / WebSocket
Coding / Debug / Security / Evaluation
AI Coding
```

不使用普通后端、普通前端、数据分析、推荐 / 广告算法等 Role Scope 外场次人为补基础题；但目标 Agent / AI Backend 流程真实出现的端侧 / 后端基础题必须保留。

## 默认排除

- AI 自动面试 / Mock Interview / 模拟题；
- 低信息密度第一人称；
- 合集 / 整理 / 搬运 / 帮转 / 投稿；
- 标准答案 / 高频题 / 面试宝典 / 完整解析；
- SEO、课程、资源导流、付费墙无法完整核验；
- 内容账号批量模板化真人叙事；
- 只有标题、截图、搜索摘要、公开索引或评论传言；
- 普通 Backend / Frontend 只顺带问 AI 项目，但岗位 Role Scope 无法确认；
- 数据分析 / BI、纯推荐 / 广告、纯训练 Infra、AI 测试等目标范围外岗位；
- 同作者同公司相邻多帖但招聘流程关系无法确认；
- 无法确认原作者归属的逐题复制链；
- 原始正文最终无法稳定访问、只能依赖 Search Cache / Snippet。

## 固定搜索方法

继续执行**热门公司优先 + 高搜索量 + 主动多平台召回**：

```text
字节 / 抖音 / 阿里系 / 腾讯 / 美团 / 快手 / 小红书 / 百度 / 蚂蚁 /
拼多多 / 京东 / 滴滴 / Bilibili / OPPO / vivo / 小米
×
岗位别名
×
最新 2026-08～09 + 补漏 2026-03～07
×
牛客 / 小红书 / 知乎 / 脉脉 / 博客 / 独立站 / 技术社区
×
技术关键词
×
作者 Timeline / 原始正文
```

岗位别名包括 AI 应用开发、AI 应用研发、Agent、智能体、大模型应用、LLM Application、RAG、AI Backend、Agent Backend、AI Full-stack、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

平台没有配额。搜索不能停在结果页或公开索引：继续追精确公司 + 岗位 + 日期 / 轮次、作者主页、候选人其它帖子、原始正文、评论区和跨平台复制关系。小红书 / 知乎 / 脉脉等若最终只能稳定取得标题、摘要或二次转载，仍然零贡献。

## 强化去重流程

**任何候选在分配 `Sxxx` 前必须直接回读全部历史 Batch。** GitHub Code Search / 搜索引擎 0 命中只能辅助，不能作为未收录证明。

固定执行：

```text
全部历史 Batch 直接回读
+
URL 精确去重
+
公司 / 岗位 / 日期 / 轮次比对
+
题序 / 项目语义去重
+
作者 / 招聘流程 Timeline 去重
+
外部原帖 / 后发复制链 / 跨平台镜像核验
```

至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特连续题序。

- 同候选人同公司同流程多轮 → 合并一个来源；
- 同候选人不同公司 / BU、招聘流程独立 → 可以分别计数；
- 不同 URL / 不同平台但题序 / 项目语义高度一致 → 继续追源；
- 作者本人是真人也不能自动证明每一篇帖子都是本人原场；
- 无法确认复制链原场 → 整链排除；
- 正文最终不能稳定打开 → 零贡献；
- 不同候选人独立遇到相同常见问题 → 分别计数。

Batch 25 的应用：`lazy_learner` 4/6 腾讯 AI 后台短帖可追到 2025 年另一作者腾讯 IEG 后端几乎逐题同序，因此该短帖排除；同作者 4/2 腾讯 AI 后台长复盘独立核验后收为 `S372`。小红书索引中“淘天 AI Agent 一面问麻了”等标题与历史 `S095` 题序高度同构且原始正文不能稳定独立核验，零贡献。百度广告投放 / 大模型应用候选因同一轮日期 Timeline 冲突排除；9 月批量“真人叙事 + 付费答案”账号继续零贡献。

## 当前基线

- 更新日期：2026-09-10
- 正式来源：`S001–S373`，共 **373 个 HUMAN-A**
- 当前正式批次：`batch-01.md` ～ `batch-25.md`
- 最新正式批次：Batch 25（`S370–S373`，新增 4 个）
- 当前最大来源编号：`S373`
- 下一条正式来源从 **`S374`** 开始
- Canonical Question：只从正式 HUMAN-A 累计
- 当前停止判断：**8～9 月热门结果层高度局部饱和；全年热门公司仍未证明完全饱和。Batch 24 / 25 两轮完整扫描均新增 4 个，新增边际已明显下降，但 Batch 25 的 4 条全部来自 3～6 月长尾，说明历史 Timeline 仍有残余增量。非牛客平台当前主要瓶颈是原文和作者可验证性，而不是搜索覆盖不足。**

## 下一轮搜索优先级

1. 从 `S374` 开始，编号前直接回读 `S001–S373`；
2. 继续保持高搜索量，8～9 月最新层与 3～7 月历史长尾同时跑，但增加 3～6 月和作者 Timeline 的预算；
3. 热门公司优先：腾讯、字节 / 抖音、美团、快手、小红书、拼多多、京东、滴滴、B站、OPPO / vivo / 小米；百度 / 阿里 / 蚂蚁继续补长尾；
4. 主动搜索小红书、知乎、脉脉、个人博客、独立站、技术社区，必须追到稳定原始候选人正文后才可准入；
5. 沿已核验真人作者 Timeline 深挖，同公司同流程后续轮次只合并，不新增；不同公司 / BU 独立流程继续逐条验真；
6. 继续记录强候选数、最终放行数以及历史重复 / 跨平台镜像 / 跨年份复制链 / 内容账号 / 正文不稳定 / Timeline 冲突淘汰原因；
7. 深挖 Agent Runtime Verification、Context / Memory Correctness、RAG Evaluation、AI Coding Verification、Harness / AgentOS、Tool Discovery / Context Control；
8. 继续补 Java / Python / Go / JavaScript / React / FastAPI / MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
9. 内容账号、投稿 / 答案、付费专栏、后发扩写、流程不清、跨平台同序链继续零容忍；
10. 特别警惕“作者是真人但单篇帖子来自复制”的情况，必须同时核验作者 Timeline 与题序 Provenance。

## 当前 Inbox

暂无待归档 HUMAN-A。
