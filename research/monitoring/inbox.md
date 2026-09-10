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
Java / Spring / Go
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
技术关键词（Python / FastAPI / asyncio / Java / Spring / Go / MySQL / Redis /
Vector DB / RAG / MCP / Skill / Harness / Runtime / Context / Memory / Tool /
Benchmark / Coding）
```

搜索不能停在结果页：继续追企业 / 话题页、精确标题、公司 + 轮次、作者主页、候选人其他帖子、个人博客 / 独立站、原始正文、评论区和跨平台同步关系。

## 强化去重流程

**任何候选在分配 `Sxxx` 前必须先完成历史 Batch 直接回读。** GitHub Code Search / 搜索引擎的“0 命中”只能作为辅助，不是“未收录”的证明。

固定执行：

```text
直接回读 S001–当前最大编号所在 Batch
+
URL 精确去重
+
公司 / 岗位 / 日期 / 轮次比对
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
+
外部原帖 / 后发复制链核验
```

至少检查：URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特题序特征。

- 同候选人同公司同流程多轮 → 合并一个来源，保留各轮问题，不新增编号；
- 同一候选人不同公司招聘流程 → 可以分别计为独立真人命中；
- 不同 URL 但题序 / 项目语义高度一致 → 继续核验作者和时间线，不能直接视为新来源；
- 更早不同作者页面与候选页面几乎逐题同序、又无法证明候选页面独立 → 候选页面排除；
- 跨平台同步、镜像、后发近似复制 → 只保留能确认的原始候选人来源；
- 无法可靠确认原场次 → 整条不确定链排除；
- **正文最终无法稳定访问、只能依赖搜索摘要 → 不进入正式来源，即使初筛时已经进入强候选池；**
- 不同候选人独立遇到相同常见问题 → 分别计数。

Batch 17 的应用实例：快手 AI 应用服务端 8/26、9/1、9/9 三轮由同一作者连续发布，合并为 `S318`；灵犀互娱 8/31、9/2、9/7 三轮及 9/8 意向 Timeline 合并为 `S319`。两者虽然同一作者且都深挖 `CR Agent`，但公司与招聘流程独立，因此分别计数。另有一条某中厂 Agent 应用开发候选在最终复核时正文无法稳定打开，只能依赖 Search Snippet，因此编号前撤出。

## 当前基线

- 更新日期：2026-09-10
- 正式来源：`S001–S319`，共 **319 个 HUMAN-A**
- 当前正式批次：`batch-01.md` ～ `batch-17.md`
- 最新正式批次：Batch 17（`S309–S319`，新增 11 个）
- 当前最大来源编号：`S319`
- 下一条正式来源从 **`S320`** 开始
- Canonical Question：只从正式 HUMAN-A 累计；其他来源继续保持零贡献
- 当前停止判断：**仍未达到来源饱和，但已经进入高去重 / 高 Provenance 核验成本阶段。** 在 `S001–S308` 全历史重新直接回读后，本轮仍确认 11 个独立 HUMAN-A；同时内容账号、答案版、自动面、同序改写和正文不稳定候选比例继续上升。

## 下一轮搜索优先级

1. 从 `S320` 开始，但必须在分配编号前直接回读历史 Batch 做完整去重；
2. 持续追 2026-09 最新 AI Application / Agent 原帖，尤其是能沿作者 Timeline 闭环的多轮流程；
3. 沿 Batch 17 新增候选人的后续技术面 / Leader 面继续追踪，同公司同流程只合并；
4. 回扫 2026-03～09 未充分覆盖公司和岗位别名；
5. 深挖 Tool Calling / Agent Runtime：Structured Tool Call、Content Block、Executor、Tool Result、Retry / Failure；
6. 深挖 RAG 反例：Chunk Semantic Boundary、Summary-induced Recall Loss、Embedding Strategy、Retrieval Failure Attribution；
7. 深挖 Skill / Tool / Function Call 的实现边界与 Progressive Disclosure；
8. 继续补 Python / FastAPI / Async 与 Agent Runtime 同场真人样本；
9. 继续追 Long-running Agent：Cancel / Checkpoint / Resume / State / 外部副作用 Idempotence；
10. 继续寻找目标 AI 岗中 Java / Spring / Go / MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
11. 牛客外继续主动搜索个人博客 / 独立站 / 稳定原始正文，不设置平台配额；
12. 持续记录新增 HUMAN-A 数量、重复率、二次整理 / 内容账号比例、Role Scope 外比例与正文稳定核验失败率，判断是否真正接近饱和。

## 当前 Inbox

暂无待归档 HUMAN-A。
