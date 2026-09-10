# HUMAN-A Monitoring Inbox

更新日期：2026-09-10

本文件只保存**已经满足 HUMAN-A，但尚未归入正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

## 固定准入标准

平台一视同仁。牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客及其他公开来源全部执行同一门槛，不设平台配额。

新的 Inbox 候选必须同时满足：

1. **真人面试官**：人与人进行的技术面 / Leader 面 / 项目深挖；
2. **候选人本人第一人称**：不是整理、搬运或二次转述；
3. **高信息密度**：具体技术问题足够丰富；
4. **真实现场痕迹**：追问、答题状态、轮次、结果、互动、Coding / Demo / 屏幕共享等可验证线索；
5. **Role Scope Gate**：AI 应用、Agent、LLM 应用、RAG、AI Backend、AI Full-stack、Applied AI、FDE、Agent Runtime / Harness / Coding Agent 等目标方向；
6. **正文稳定可核验**：原始正文与 URL 可以实际访问并验证；
7. **非重复**：不是转载、合集、跨平台同场重复或后发近似复制。

```text
真人面试官
+
候选人本人第一人称
+
高信息密度
+
真实现场痕迹
+
目标 AI Application / Agent 岗位
+
正文稳定可核验
+
非转载 / 非合集 / 非重复
=
HUMAN-A
```

任意一项不满足都不进入 Inbox、正式 Batch、Canonical Question、频率统计或课程优先级。

## 通过岗位准入后：整场全知识保留

确认是一场目标 AI 岗 HUMAN-A 后，真实出现的以下知识全部一视同仁记录：

```text
Python / FastAPI / Backend Engineering
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

**不使用普通后端、数据分析、BI、推荐算法等 Role Scope 外面经人为补基础题。**

## 默认排除

- AI 自动面试 / Mock Interview / 模拟题；
- 低信息密度第一人称；
- 合集 / 整理 / 搬运 / 后发近似复制；
- 标准答案 / 高频题 / 面试宝典 / 完整解析；
- SEO、课程、资源导流、付费墙无法完整核验正文；
- 内容账号批量模板化“真人叙事”，无法可靠确认候选人本人经历；
- 只有标题、截图、Search Snippet 或评论传言；
- 普通后端 / 前端、传统数据分析 / BI、纯推荐 / 纯训练 Infra、AI 测试等 Role Scope 外场次；
- 仅因标题或个别问题出现 AI / Agent 字样，但无法证明实际职责属于目标方向；
- 无法确认原作者归属的逐题复制链：宁可整链排除，不按发布时间猜原帖。

临时线索只用于寻找真正 HUMAN-A 原帖，线索本身零贡献。

## 固定搜索方法

```text
公司
×
岗位别名（AI应用开发 / Agent开发 / 智能体开发 / 大模型应用开发 /
LLM应用 / RAG开发 / AI后端 / AI全栈 / Applied AI / FDE / Coding Agent）
×
月份（重点回扫 2026-03～09，同时追最新发布）
×
技术关键词（Python / FastAPI / asyncio / MySQL / Redis / Vector DB /
RAG / MCP / Skill / Harness / Runtime / Context / Memory / Tool / Coding）
```

搜索不能停在结果页：继续追企业 / 话题页、精确标题、公司 + 轮次、作者主页、候选人其他帖子、个人博客 / 独立站、原始正文、评论区和跨平台同步关系。

## 三层去重

```text
URL 精确去重
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
```

- 同候选人同流程多轮 → 合并计为一个来源，但保留所有轮次真实问题；
- 跨平台同步、镜像、后发近似复制 → 只保留更原始、更稳定、更有现场证据的一份；
- 不同候选人独立遇到相同问题 → 分别计为独立 HUMAN-A 命中；
- 无法可靠确认谁是原场次的逐题复制链 → 整链排除。

## 当前基线

- 更新日期：2026-09-10
- 正式来源：`S001–S276`，共 **276 个 HUMAN-A**
- 当前正式批次：`batch-01.md` ～ `batch-13.md`
- 最新正式批次：Batch 13（`S265–S276`，新增 12 个）
- 本轮存量修正：小红书 `S260` 同一候选人的 8 月 17 日二面已合并回原来源，不新增 `Sxxx`
- 当前最大来源编号：`S276`
- 下一条正式来源从 **`S277`** 开始
- Canonical Question：只从正式 HUMAN-A 累计；其他来源继续保持零贡献
- 当前停止判断：**仍未达到来源饱和**。泛搜索污染率、内容账号与重复率继续上升，但精确公司 / 岗位 / 作者时间线与历史月份回扫仍能产生独立 HUMAN-A 和已收录候选人的新轮次。

## 下一轮搜索优先级

1. 持续追 2026-09 最新 AI Application / Agent 原帖；
2. 沿 Batch 13 新增候选人的作者主页回看二面 / 三面 / Leader 面，并按同一招聘流程合并；
3. 回扫 2026-03～09 未充分覆盖公司和岗位别名；
4. 优先补 Long-running Agent / Checkpoint / Resume / State、Tool Permission / Sandbox / Trace / Evaluation；
5. 继续观察 Token / Cost Budget、Rate Limit、并发预算预留等 AI Backend 新追问；
6. 深挖 Vector Retrieval / RAG Evaluation：HNSW / IVF / PGVector / BM25 / RRF / Rerank / Recall / Precision Trade-off；
7. 继续寻找 AI Backend / AI Full-stack 中 MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
8. 牛客外继续主动搜原始正文，但不设置平台配额；
9. 持续记录新增 HUMAN-A 数量、命中率、重复率、二次整理 / 内容账号比例和 Role Scope 外比例，判断是否真正接近饱和。

## 当前 Inbox

暂无待归档 HUMAN-A。
