# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-10）

- 当前活跃来源：**196 个 HUMAN-A 真人高质量第一人称样本（S001–S196）**。
- 当前正式批次：[`Batch 01`](./interviews/batch-01.md) + [`Batch 02`](./interviews/batch-02.md) + [`Batch 03`](./interviews/batch-03.md) + [`Batch 04`](./interviews/batch-04.md) + [`Batch 05`](./interviews/batch-05.md) + [`Batch 06`](./interviews/batch-06.md) + [`Batch 07`](./interviews/batch-07.md) + [`Batch 08`](./interviews/batch-08.md) + [`Batch 09`](./interviews/batch-09.md)。
- Batch 01：`S001–S013`，13 个干净基线来源。
- Batch 02：`S014–S031`，新增 18 个 HUMAN-A。
- Batch 03：`S032–S051`，新增 20 个 HUMAN-A。
- Batch 04：`S052–S074`，新增 23 个 HUMAN-A。
- Batch 05：`S075–S094`，新增 20 个 HUMAN-A。
- Batch 06：`S095–S117`，新增 23 个 HUMAN-A。
- Batch 07：`S118–S147`，新增 30 个 HUMAN-A。
- Batch 08：`S148–S168`，新增 21 个 HUMAN-A。
- Batch 09：`S169–S196`，新增 **28 个 HUMAN-A**。
- Canonical Question 层只允许从当前 HUMAN-A 来源累计证据；低质量来源继续保持零贡献。
- 当前仍未达到来源饱和。Batch 08 起泛搜索重复率明显上升，Batch 09 这一趋势继续，但精确公司 / 岗位 / 月份 / 轮次、企业 / 话题页、作者时间线和跨平台原帖回溯仍一次找到 28 个新的独立 HUMAN-A。
- 平台没有质量加成：牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、个人博客或其他公开来源全部执行同一 HUMAN-A 标准。

详细准入规则：

- [`quality/source-quality-policy.md`](./quality/source-quality-policy.md)：统一 HUMAN-A 来源标准。
- [`quality/role-scope-policy.md`](./quality/role-scope-policy.md)：目标岗位范围。

---

# 唯一正式来源标准：HUMAN-A

正式面经必须同时满足：

```text
真人面试官
   +
候选人本人第一人称复盘
   +
高信息密度与真实现场痕迹
   +
AI Application / Agent 目标岗位
   +
正文可稳定核验
   +
非转载 / 非合集 / 非同场重复
   ↓
HUMAN-A
```

不满足任一条件的内容都不进入正式研究，也不贡献任何 Canonical Question、频率或课程优先级。

---

# 知识体系与面经的分工

本项目坚持：

> **知识体系是骨架，高质量真人面经是血肉。**

完整知识体系决定一个 AI Application Engineer 应该系统学习什么：

```text
Python
FastAPI
AI Backend Engineering
MySQL
Redis
Vector Database
LLM Foundation（应用工程深度）
RAG
Agent Harness / Runtime
System Design
```

HUMAN-A 面经负责提供：

- 真人面试官的真实问法；
- 不同知识模块的真实出现频率；
- 不同公司 / 岗位 / 轮次的追问深度；
- 口述、System Design、Debug、Coding 和项目验真的真实要求；
- 对完整知识体系复习优先级的现实校准。

低质量来源不会为了“补知识点”增加任何学习任务。

---

# 数据层

## 1. Interviews / Sources

每个正式来源至少记录：

- `source_id`
- 公司 / 岗位 / 日期 / 轮次
- 原始 URL
- 真人 / 第一人称证据
- 5～12 条高信息量问题的简洁转述

同一候选人的同一招聘流程如果存在一面 / 二面 / 三面多篇帖子，在能够确认同源时合并计为一个来源，避免人为抬高样本量；不同候选人即使同公司、同日、题目相近，也按独立真人场次分别判断。

第三方面经只保存研究所需元数据与问题转述，不复制全文。

## 2. Canonical Questions

Canonical Question 只是 HUMAN-A 面经的**语义去重层**，不是第二套知识体系。

多个独立真人来源语义相同的问题可以归并成一个 Capability，同时分别记录 HUMAN-A 命中。没有 HUMAN-A 证据的问题不能进入这一层。

规则见：[`questions/README.md`](./questions/README.md)。

---

# 搜索范围

## Lane A — Agent / Harness Frontier

```text
Harness / Runtime / Agent Loop
Context / Memory / Compaction
Tool / MCP / Skill
Permission / Sandbox / Security
Checkpoint / Resume / Cancel
Multi-Agent / Sub-agent
Coding Agent / Claude Code / Codex
Evaluation / Trace / Cost / Reliability
```

## Lane B — AI Application Foundation

```text
Python / GIL / asyncio
FastAPI / ASGI / SSE
MySQL / Index / MVCC / Lock / Log
Redis / Cache / Cluster / Lock
MQ / Network / Concurrency
Vector DB / RAG
LLM Foundation
System Design
```

两条 Lane 都只从通过 HUMAN-A 的目标 AI 岗真人面试中取证。

---

# 平台与访问限制

搜索不设平台偏好。登录态、App 跳转、动态加载和搜索索引不完整会让“直接能打开的帖子数”显著少于市场实际供给，因此提高 Recall 时继续组合使用：

```text
公司 × 岗位别名 × 月份 × 技术关键词
   +
企业 / 话题页回溯
   +
精确标题 / 精确轮次搜索
   +
候选人主页 / 个人博客核验
   +
跨平台查找同一作者原帖
```

这些方法只负责**发现来源**，不能降低 HUMAN-A 门槛。最终无法稳定核验原正文，就不入库。

去重不能只看 URL。当前固定使用：

```text
URL 精确去重
   +
问题题序 / 项目语义去重
   +
作者 / 招聘流程时间线去重
```

本项目也明确排除“为了平台多样性而收水内容”：标准答案、帮粉丝复盘、SEO 资料导流、内容营销账号、模板化“真人叙事”、AI 自动面试等，即使问题很多也不进入正式数据。

---

# 研究工作流

```text
公开平台扩大召回
      ↓
定位候选原帖
      ↓
HUMAN-A Gate
      ↓
Role Scope Gate
      ↓
原帖 / 作者 / 时间线核验
      ↓
URL + 题序 / 项目语义 + 作者流程三层去重
      ↓
来源归档
      ↓
问题简洁转述
      ↓
Canonical Question 语义去重
      ↓
公司 / 轮次 / 模块 / 深度 / 频率分析
      ↓
反向校准复习优先级
```

---

# Batch 09 后的信号

当前 196 个 HUMAN-A 已经稳定覆盖整条路线：

```text
Python / OS / Network
        ↓
FastAPI / Async / Streaming / Service Runtime
        ↓
MySQL / Redis / MQ / Concurrency / Sharding
        ↓
Vector DB / RAG / OCR / Retrieval Evaluation
        ↓
LLM Foundation / Context
        ↓
Agent / Harness / Tool / MCP / Skill
        ↓
Coding Agent / Spec / Worktree / Checkpoint / Trace
        ↓
Controlled Runtime / Resume / Interrupt / Evaluation
        ↓
Production / Security / System Design
```

Batch 09 进一步强化了这些真人面试趋势：

- **泛搜索重复率继续升高，但精确搜索仍有显著增量。** 企业 / 话题页、公司 × 岗位 × 月份 × 轮次、作者时间线继续找到 28 个新的独立 HUMAN-A，因此当前仍不能停止。
- **完整招聘流程比单篇题单更有研究价值。** 百度 Coding Agent 三轮、字节 AI 全栈一二面等样本能看到问题随轮次从项目 / Agent 深入到 OS / Backend / Coding；同流程合并计数但保留整场知识。
- **Coding Agent / Agent Runtime 已稳定进入“可控软件执行系统”层。** Skill Mis-selection、Dynamic Args、Context Isolation、Container Restart Resume、Secret Boundary、Sub-agent Token Accounting、Loop Oscillation、Compaction、Prompt Cache 等都有独立真人命中。
- **AI Backend Foundation 继续被目标岗位直接确认。** MySQL MVCC / Index / Deep Pagination、Redis Lock / Cache / HotKey、MQ Reliability、TCP / HTTPS、Go Context、Java Lock / ThreadPool 与 Agent / RAG 同场出现。
- **项目价值量化是越来越强的验真点。** QPS、DAU、Cache Hit Rate、节省人力、准确率、Latency、Cost、失败案例和本人贡献被持续追问。
- **跨平台原帖回溯开始产生实际增量。** Batch 09 找到候选人个人博客中的小红书 AI 应用原始面经；与此同时 CSDN / 51CTO 等大量搜索结果仍是转载、路线和营销内容，不能为了覆盖平台降低门槛。
- **作者身份和招聘流程时间线已经成为必要去重层。** 同公司同日不一定是同一候选人；同作者跨多个 URL 的一二三面则应合并。

## 什么时候停止继续搜？

停止条件从来不是达到某个 `Sxxx` 或某个 Batch 数，而是出现**来源饱和**。后续持续观察：

```text
A. 新增 HUMAN-A 的绝对数量
B. 新增 HUMAN-A / 全部候选结果 的比例
C. 精确搜索是否仍能找到新来源
D. 新增问题模块与追问深度是否继续变化
```

只有连续多轮跨公司、岗位、月份、轮次、平台扩大搜索后，同时出现以下信号，才进入收尾阶段：

1. 新结果绝大多数已经是已收录同场、转载、合集、答案型内容、低质量来源或 Role Scope 外来源；
2. 每轮新增 HUMAN-A 的绝对数量和比例都持续接近零；
3. 精确公司 / 轮次 / 作者页搜索也难以发现新来源，而不是只有泛关键词搜索变重复；
4. 新增来源的公司 / 岗位 / 轮次与问题模块、追问深度分布逐渐稳定。

**当前 196 个样本虽然重复率继续上升，但 Batch 09 仍新增 28 个独立 HUMAN-A，因此明显未达到停止点。**
