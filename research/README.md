# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-09）

- 当前活跃来源：**94 个 HUMAN-A 真人高质量第一人称样本（S001–S094）**。
- 当前正式批次：[`Batch 01`](./interviews/batch-01.md) + [`Batch 02`](./interviews/batch-02.md) + [`Batch 03`](./interviews/batch-03.md) + [`Batch 04`](./interviews/batch-04.md) + [`Batch 05`](./interviews/batch-05.md)。
- Batch 01：`S001–S013`，13 个干净基线来源。
- Batch 02：`S014–S031`，新增 18 个 HUMAN-A。
- Batch 03：`S032–S051`，新增 20 个 HUMAN-A。
- Batch 04：`S052–S074`，新增 23 个 HUMAN-A。
- Batch 05：`S075–S094`，新增 **20 个 HUMAN-A**。
- Canonical Question 层已在历史清洗时归零，只允许从当前 HUMAN-A 来源重新累计，不继承清洗前的题目 ID 或频率。
- 当前仍远未达到来源饱和；每批数量不设目标，唯一目标是继续扩大**独立、高质量、可核验的真人目标岗位面经**。
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

# Batch 05 后的信号

当前 94 个 HUMAN-A 已经稳定覆盖整条路线，而不是只覆盖 Agent 名词：

```text
Python / OS / Network
        ↓
FastAPI / Async / Streaming / Service Runtime
        ↓
MySQL / Redis / MQ / Concurrency / Sharding
        ↓
Vector DB / RAG
        ↓
LLM Foundation / Context
        ↓
Agent / Harness / Tool / MCP / Skill
        ↓
Production / Security / Evaluation / System Design
```

Batch 05 进一步强化了几个真人面试趋势：

- **Harness / Runtime 正在从术语进入执行语义**：Tool Discovery / Dynamic Registry、Task Isolation、Long-running Latency、执行幻觉、Compaction、Self-evolution、自动交付可靠性已经出现在真人一二面 / Leader 面。
- **Agent 越来越像分布式后端系统**：RPC、Async、MQ、Checkpoint、Retry / Fallback、SSE、Rate Limit、Idempotency、Cache、Observability 与 Capacity 是同一套 Production 问题。
- **RAG 更强调可证明的实验依据**：父子索引、BM25 + Vector + Rerank、OCR / Table、Index Update、RRF、Top-K、Evaluation 都要求解释选择原因和收益验证。
- **MySQL / Redis / Network / Concurrency 是明确 AI 岗的真实主线**：AI 应用 / AI 后端真人场次会长时间追事务、日志、缓存、锁、分库分表、ThreadLocal、TCP、WebSocket，而不是只问 Agent 名词。
- **项目验真继续升级**：面试官会追本人贡献、业务量、真实指标、失败恢复、AI 代码能否进生产、为什么不用 Workflow / Script，以及平台能力能否规模化复用。

当前判断仍然明确：**高质量真人来源远未饱和。** 后续继续扩大独立 HUMAN-A 样本，优先补 2026 年 3–9 月未覆盖公司 / 轮次和最新发布内容，直到公司、岗位、轮次和问题分布本身逐步趋于饱和，而不是人为限制 Batch 数量。