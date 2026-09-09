# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-09）

- 当前活跃来源：**31 个 HUMAN-A 真人高质量第一人称样本（S001–S031）**。
- 当前正式批次：[`interviews/batch-01.md`](./interviews/batch-01.md) + [`interviews/batch-02.md`](./interviews/batch-02.md)。
- Batch 02 新增 `S014–S031` 共 **18 个 HUMAN-A**，证明清洗后的 13 个只是初始干净基线，不是公开市场供给上限。
- Canonical Question 层已经完成清空并重新建立干净基线，当前只允许从 HUMAN-A 来源重新累计，不沿用清洗前的问题 ID 或统计数字。
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

# 平台与访问限制

搜索范围不设平台偏好：

- 牛客
- 小红书
- 知乎
- 脉脉公开内容
- CSDN / 掘金 / 个人技术博客
- Bilibili / 抖音
- 其他可公开访问的平台

但任何来源都必须实际验证正文、候选人第一人称、真人面试属性、岗位范围和信息密度。

需要特别注意：**“搜索工具直接能打开多少篇”不等于“网上实际有多少篇”。** 一些平台存在登录态、App 跳转、动态加载、搜索引擎只索引摘要、帖子删除或跨平台同步等情况，因此直接搜索会系统性低估供给。

为提高 Recall，可以：

```text
关键词搜索
   +
企业 / 话题页回溯
   +
搜索引擎索引摘要定位标题
   +
候选人主页 / 个人博客交叉验证
   +
跨平台寻找同一作者原帖
```

但这些方法只负责**发现来源**，不能降低 HUMAN-A 准入标准。若最终仍无法稳定核验原正文，就不入库。

---

# 研究工作流

```text
公开平台扩大召回
      ↓
定位候选原帖
      ↓
HUMAN-A Gate
      ↓
岗位范围校验
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

# 当前判断

清洗后最初只保留 13 个 HUMAN-A，是因为当时采用了非常保守的“只继承已明确复核来源”策略，并不是判断公开市场只有十几篇。

Batch 02 在保持同一 HUMAN-A 标准的前提下，一次新增了 18 个合格来源，使当前核心样本达到 **31 个**。这验证了：只要扩大搜索入口、处理登录 / 索引限制并沿原作者回溯，仍然可以持续找到大量高质量真人面经。

当前明确判断：**距离来源饱和还很远。** 后续目标是继续扩大独立 HUMAN-A 样本，直到新增来源在公司、岗位、轮次与问题分布上逐步趋于饱和，而不是人为限制每批数量。