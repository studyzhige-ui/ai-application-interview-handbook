# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-09）

- 当前活跃来源：**147 个 HUMAN-A 真人高质量第一人称样本（S001–S147）**。
- 当前正式批次：[`Batch 01`](./interviews/batch-01.md) + [`Batch 02`](./interviews/batch-02.md) + [`Batch 03`](./interviews/batch-03.md) + [`Batch 04`](./interviews/batch-04.md) + [`Batch 05`](./interviews/batch-05.md) + [`Batch 06`](./interviews/batch-06.md) + [`Batch 07`](./interviews/batch-07.md)。
- Batch 01：`S001–S013`，13 个干净基线来源。
- Batch 02：`S014–S031`，新增 18 个 HUMAN-A。
- Batch 03：`S032–S051`，新增 20 个 HUMAN-A。
- Batch 04：`S052–S074`，新增 23 个 HUMAN-A。
- Batch 05：`S075–S094`，新增 20 个 HUMAN-A。
- Batch 06：`S095–S117`，新增 23 个 HUMAN-A。
- Batch 07：`S118–S147`，新增 **30 个 HUMAN-A**。
- Canonical Question 层已在历史清洗时归零，只允许从当前 HUMAN-A 来源重新累计，不继承清洗前的题目 ID 或频率。
- 当前仍未达到来源饱和；每批数量不设目标，唯一目标是继续扩大**独立、高质量、可核验的真人目标岗位面经**。
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

HUMAN-A 面经只负责：

- 提供真人面试官的真实问法；
- 校准哪些知识更常被问；
- 观察不同公司 / 岗位 / 轮次的追问深度；
- 验证知识能否真正口述、设计和 Coding；
- 帮助安排复习优先级。

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

搜索不设平台偏好。登录态、App 跳转、动态加载和搜索索引不完整会让“直接能打开的帖子数”显著少于市场实际供给，因此提高 Recall 时会组合使用：

```text
公司 × 岗位别名 × 月份 × 技术关键词
   +
企业 / 话题页回溯
   +
搜索索引定位标题
   +
候选人主页 / 个人博客核验
   +
跨平台查找同一作者原帖
```

这些方法只负责**发现来源**，不能降低 HUMAN-A 门槛。最终无法稳定核验原正文，就不入库。

本项目也明确排除“为了平台多样性而收水内容”：CSDN / 知乎 / 视频平台中的标准答案、帮粉丝复盘、SEO 资料导流等内容，即使问题很多也不进入正式数据。

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
跨平台 / 同场去重
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

# Batch 07 后的信号

当前 147 个 HUMAN-A 已经稳定覆盖整条路线：

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
Production / Security / Evaluation / System Design
```

Batch 07 进一步强化了这些真人面试趋势：

- **来源仍然没有饱和**：已有 117 个 HUMAN-A 后，再次做公司 × 岗位 × 月份 × 技术词回扫，仍新增 30 个独立来源。常规搜索首页显然不是市场供给上限。
- **Coding Agent / Harness 正进入软件工程基础设施层**：Git Worktree、Spec-driven Development、Planner→DAG、Trace / Checkpoint / Resume、Compaction、Memory Search、Regression / Evaluation、AI Refactor Equivalence 都出现了真人追问。
- **AI Backend Foundation 继续被独立来源确认**：MySQL Transaction / Sharding、Redis Consistency / Atomicity、MQ Reliability、Thread Pool、JVM、TCP / HTTPS、Nginx / Rate Limit 与 Agent / RAG 同场出现，不是混入传统后端导致的假频率。
- **RAG 面试越来越强调失败模式与实验依据**：AST Code RAG、RRF、Hybrid Retrieval、Rerank、Chunking、Query Ambiguity、Vector DB、Embedding Upgrade / Index Compatibility 都要求解释为什么和怎么验证。
- **同一候选人的多轮流程要保守计数**：小红书 AI 全栈、汇川 AI 全栈的一二面被合并计为一个来源；同时继续使用 URL、题序 / 项目语义、作者时间线三层去重。
- **HUMAN-A 不能被“题目漂亮”绑架**：答案型专栏、付费内容、模板化帖子、AI 自动面试和无法稳定打开的原帖仍全部零贡献。

## 什么时候停止继续搜？

停止条件从来不是达到某个 `Sxxx` 或某个 Batch 数，而是出现**来源饱和**：

1. 连续多轮按公司 × 岗位别名 × 月份 × 技术关键词扩大搜索；
2. 牛客之外也继续查公开平台、作者页、企业 / 话题页和跨平台原帖；
3. 新结果绝大多数变成已收录同场、转载、合集、低质量内容或 Role Scope 外来源；
4. 每轮几乎不再产生新的、独立、可稳定核验的 HUMAN-A；
5. 新增来源的公司 / 岗位 / 轮次与问题模块分布也逐渐稳定。

只有这些信号同时持续出现，才说明接近停止点。**目前 147 个样本仍没有出现这种饱和迹象。**