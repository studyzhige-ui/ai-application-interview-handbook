# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-09）

- 当前活跃来源：**13 个 HUMAN-A 真人高质量第一人称样本（S001–S013）**。
- 当前正式批次：[`interviews/batch-01.md`](./interviews/batch-01.md)。
- Canonical Question 层已经完成清空并重新建立干净基线，当前从 HUMAN-A 来源重新累计，不沿用任何清洗前的问题 ID 或统计数字。
- 当前仍远未达到来源饱和，后续继续扩展高质量真人样本。
- 所有平台执行同一套固定标准：平台可以是牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、个人博客或其他公开来源，但**平台本身不提供任何质量加成**。

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

两者职责严格分开。

## 完整知识体系负责

决定一个 AI Application Engineer 应该系统学习什么：

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

课程完整性不依赖面经题量。

## HUMAN-A 面经负责

- 提供真人面试官的真实问法；
- 校准哪些知识更常被问；
- 观察不同公司 / 岗位 / 轮次的追问深度；
- 验证知识能否真正口述、设计和 Coding；
- 帮助安排复习优先级。

低质量来源不会为了“补知识点”额外增加学习任务。

---

# 数据层

## 1. Interviews / Sources

每个正式来源至少记录：

- `source_id`
- 公司 / 岗位 / 日期 / 轮次
- 原始 URL
- 真人面试证据
- 第一人称证据
- 5～12 条高信息量问题的简洁转述

第三方面经只保留研究所需的元数据与问题转述，不复制全文。

## 2. Canonical Questions

Canonical Question 只是 HUMAN-A 面经的**语义去重层**，不是第二套知识体系。

例如多个独立真人来源分别问：

```text
Context 满了怎么办？
长任务上下文怎么压缩？
Compaction 怎么避免关键信息丢失？
```

如果核心能力相同，可以归一化为一个 Canonical Question，同时记录每个独立真人来源的命中。

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

# 平台原则

搜索范围不设平台偏好：

- 牛客
- 小红书
- 知乎
- 脉脉公开内容
- CSDN / 掘金 / 个人技术博客
- Bilibili / 抖音
- 其他可公开访问的平台

但任何来源都必须实际验证正文、候选人第一人称、真人面试属性、岗位范围和信息密度。

如果只能看到标题、截图、摘要、二次转述或标准答案，直接放弃，不进入研究库。

---

# 研究工作流

```text
公开平台搜索
      ↓
HUMAN-A Gate
      ↓
岗位范围校验
      ↓
原帖核验
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

# 当前判断

当前只有 13 个严格 HUMAN-A 样本，这是有意为之。

我们宁可从一个较小但干净的数据集重新向外扩展，也不会为了恢复旧数量重新引入无法确认质量的材料。

接下来的目标是持续扩大 **独立、真人、第一人称、高信息密度、岗位方向正确** 的 2026 AI Application / Agent 面经，直到新增来源在问题分布、公司覆盖和轮次覆盖上逐步趋于饱和。