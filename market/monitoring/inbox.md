# HUMAN-A Monitoring Inbox

更新日期：2026-09-26

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

当前共有 **4 个**已通过 HUMAN-A + Role Scope + Stable Original + 全历史去重 Gate 的候选流程，均为 Morning 暂存；**不分配 S ID，不创建 Batch**。22:00 Finalize 前必须基于当时最新 main 再直接回读全部历史 Batch。

### Candidate A — 小红书 Product Engineer（AI 与全栈方向）｜社区工程一面

- 作者：`Harry00`
- 发布：2026-09-24 14:48；面试：2026-09-24；约 50min
- 原帖：https://www.nowcoder.com/feed/main/detail/70ad5ead2f784676b0b399eab877d3d4?sourceSSR=enterprise
- Role Scope：标题明确 Product Engineer（AI 与全栈方向）；整场主体为 RAG / Agent / AI Coding + Production Engineering。
- 关键题序：RAG 完整流程 → keyword / vector / hybrid retrieval 取舍 → Recall bad case → Chunk 粒度 / overlap → Agent vs Workflow / ReAct → AI Coding Skill / progressive loading → Redis Cache / 限流 / 异步任务。
- Provenance：post-specific 正文稳定；作者主页仅 3 条连续本人求职记录，非批量内容账号。
- 全历史去重：batch-01～35 未发现同 URL、作者、同小红书招聘流程或该连续题序。

### Candidate B — 迅雷 Agent｜一面

- 作者：`卷不动了w`
- 发布：2026-09-23 23:25；约 1h28min
- 原帖：https://api-cdn.nowcoder.com/discuss/932392798559432704?sourceSSR=post
- Role Scope：标题明确 Agent；项目追问与 RAG / Memory / Skill / MCP / AI Native Engineering 为主体。
- 关键题序：Intent Routing 如何量化 → 相似问法不同意图 → Memory 新旧方案冲突 → RAG / Reranker 底层 → Chunk 联系 → Skill → MCP / stdio → 多人 AI Native 开发规范 / CLAUDE.md 跨 Coding Agent 一致性 → Concurrent / Spring Bean。
- Provenance：第一人称现场痕迹强；作者主页连续记录百度、迅雷、华测、CVTE、蚂蚁、字节等本人招聘流程。
- 全历史去重：batch-01～35 未发现同 URL、作者、同迅雷流程或该连续题序。

### Candidate C — 百度搜索 AI 全栈（偏前端）｜一面

- 作者：`卑卑小狗`
- 发布：2026-09-23 15:34；约 1h
- 原帖：https://www.nowcoder.com/feed/main/detail/0e577bc8131748be85df948327830943?sourceSSR=enterprise
- Role Scope：标题明确 AI 全栈；React / Vue / Fiber 之后连续进入 Agent / MCP / Skill / RAG / Context / Model 选型，符合 AI Full-stack 范围。
- 关键题序：React/Vue/Fiber → Agent vs LLM → MCP 通信 → MCP / Tool / Skill 区别 → Skill 缺点 → RAG 流程 → Chunk 粒度 → Claude Context → Model 选择 → 实习深挖 → Coding。
- Provenance：post-specific 正文稳定；作者主页连续记录快手商业化 AI 全栈、百度搜索 AI 全栈等本人流程。
- 全历史去重：batch-01～35 未发现同 URL、作者、同百度流程或该连续题序。

### Candidate D — 字节 Agent 开发后端｜日常实习一面

- 作者：`溯洄之洲`
- 发布：2026-09-24 08:13；面试：2026-09-23
- 原帖：https://www.nowcoder.com/discuss/932295617999622144?sourceSSR=post
- Role Scope：标题明确 Agent 开发后端；整场围绕 Agent / RAG 技术选型与效果证明。
- 关键题序：LangGraph / Workflow → Eval Dataset 构造 → AI 合成数据质量 → Query ambiguity → Markdown/TXT/PDF Chunking → BM25 + Vector → RRF → Cross-Encoder Rerank → Domain Mismatch → Retrieval 方案差异 → 哪个指标真正证明系统达标 → Coding。
- Provenance：第一人称“9/23 刚面完”、面试官追问方式、次日流程终止均可核验；作者主页另有 Shopee 测开本人面试记录。
- 全历史去重：batch-01～35 未发现同 URL、作者、同字节流程或该连续题序。

### Morning 明确排除 / 不进入 Inbox

- vivo Agent 9/22：原帖质量合格，但发布 2026-09-22 21:00，已早于本次约 2026-09-23 09:43 的 72 小时发现窗口边界，不补录。
- 阿里淘天 9/23 23:02：第一人称外观较强，但正文显著混入逐题标准答案 / 事后教学解析与“建议收藏”式内容包装；按 Answer-post / Content-style 风险不升级 HUMAN-A。
- `林小白zii`、`AIGC小白入门记` 等批量面经 / 答案化内容链继续排除。
- 美团近期 AI 全栈：企业聚合页可见高密度问题，但本轮未闭环稳定候选人 post-specific 原帖与作者 provenance，不进 Inbox。
- 测开 / 普通 Backend / Frontend / Data 岗仅顺带深问 Agent / Skill / MCP：Role Scope 外，不用于目标岗位频率统计。
