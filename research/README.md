# 2026 AI 应用 / Agent 面经研究

这里不是“面试题大全”，而是整套知识体系的 **招聘现实校准层**。

## 当前进度（2026-09-09）

- 历史 `Sxxx` 编号范围：**S001–S141**。
- 最新正式批次：[`interviews/batch-11.md`](./interviews/batch-11.md)。
- 当前规范化问题：约 **209 道 canonical questions**（工作去重口径）。
- 当前仍处于扩展召回阶段，**远未认为来源饱和**。
- **从 Batch 11 起，新的正式样本只接受 `HUMAN-A`：真人面试官 + 候选人本人高质量第一人称 + 目标 AI Application / Agent 岗位。**
- AI 自动面试、B 级低信息密度、合集、标准答案 / 题库、二次创作、SEO 博客和无法核验的跨平台线索，不再进入新的正式 Batch。
- 历史批次为了研究召回曾保存过 B/C/D/E 与 automated 信号，这些稳定 ID 暂时保留用于追溯，但**后续真人面试频率与课程优先级统计只认 HUMAN-A Core**。例如 Batch 10 的自动化面试样本 `S119` 不属于真人核心样本。

详细准入：

- [`quality/source-quality-policy.md`](./quality/source-quality-policy.md)：HUMAN-A 硬门槛。
- [`quality/role-scope-policy.md`](./quality/role-scope-policy.md)：岗位范围。
- [`analysis/foundation-signal-after-batch-07.md`](./analysis/foundation-signal-after-batch-07.md)：Python / MySQL / Redis 基础能力信号校准。

---

## 为什么只保留 HUMAN-A

我们最终想回答的是：

> **真实 AI 应用 / Agent 技术面里，真人面试官究竟在问什么？**

因此正式证据必须同时满足：

```text
真人技术面 / Leader 面
        +
候选人本人第一人称复盘
        +
足够具体的技术追问与现场痕迹
        +
AI Application / Agent 目标岗位
        ↓
HUMAN-A Core
```

自动化 AI 面试、整理账号和“含完整答案”内容即使题目本身有知识价值，也不能替代真人面试证据。

---

## 研究目标

- 尽可能覆盖 2026 年公开可访问的高质量 AI 应用开发、AI Agent、RAG、AI Backend、AI Full-stack、Applied AI、Agent Runtime 面经。
- 保留“原始来源层”和“Canonical Question 语义去重层”，避免归一化后丢掉面试官真实问法。
- 用真人面经反向验收：Python、FastAPI、AI Backend、MySQL、Redis、Vector DB、RAG、Agent Harness、LLM Foundation、System Design 是否有缺口。
- 不因为最近 Harness 问题更前沿就低估 Python / MySQL / Redis，也不为了补基础去混入传统后端 / 数据分析岗位。
- 最终按 **岗位类型 × 公司 × 面试轮次 × 知识模块 × 深度** 做分层统计。

---

## 数据层次

### 1. Interviews / Sources

每个 HUMAN-A 来源至少记录：

- `source_id`
- 公司 / 岗位 / 日期 / 轮次
- 原始 URL
- 真人面试证据
- 第一人称真实性证据
- 5～12 条最有信息量的问题转述
- 本场对知识体系的价值

第三方帖子只保存研究所需的事实性元数据和简洁问题转述，不复制全文。

### 2. Canonical Questions

语义相同的问题归并，例如：

```text
Context 满了怎么办？
长任务上下文怎么压缩？
Compaction 怎么避免关键信息丢失？
        ↓
一个 canonical capability
```

但不同真人来源仍然分别记录命中，以便后续做真实频率统计。

### 3. Taxonomy

一级模块持续覆盖：

```text
Python
FastAPI
AI Backend Engineering
MySQL
Redis
Vector DB
RAG
LLM Foundation
Agent Harness / Runtime
System Design
Project / Coding
```

问题继续标注 Definition / Principle / Comparison / Debugging / Design / Project Deep Dive / Coding，以及 Basic / Intermediate / Advanced。

---

## 搜索策略

### Lane A — Agent / Harness Frontier

```text
Harness / Runtime / Agent Loop
Context / Memory / Compaction
Tool / MCP / Skill
Permission / Sandbox / Security
Checkpoint / Resume / Cancel
Multi-Agent
Coding Agent / Claude Code / Codex
Evaluation / Trace / Cost / Reliability
```

### Lane B — AI Application Foundation

```text
Python / GIL / asyncio
FastAPI / ASGI / SSE
MySQL / Index / MVCC / Lock / Log
Redis / Cache / Cluster / Lock
MQ / Network / Concurrency
Vector DB / RAG
System Design
```

两条 Lane **都只从目标 AI 岗的真人 HUMAN-A 面试中取证**。

### 平台

搜索不局限于牛客，也会查看小红书、知乎、脉脉公开内容、CSDN、掘金、Bilibili、抖音等；但平台多样性不能降低门槛：正文、第一人称和真人属性无法稳定验证，就不进入正式样本。

---

## 批次

- **Batch 01–05**：建立召回框架并扩展来源、主题和跨平台线索。
- **Batch 06**：开始严格“宁缺毋滥”。
- **Batch 07**：基础工程能力校准，确认 Python / MySQL / Redis / 并发仍大量出现在 AI 岗。
- **Batch 08**：增加 Role Scope Gate，只研究我们的 AI Application / Agent 求职方向。
- **Batch 09**：开始明确 LLM Foundation 的应用工程深度。
- **Batch 10**：扩展到 KV Cache、Cost Accounting、Data Access Governance、Bi-Encoder / Cross-Encoder、Redis Cluster 原子性等 Production 问题；其中 automated 来源后续不进入 HUMAN-A Core。
- **Batch 11**：正式切换为 **HUMAN-A Only**，`S129–S141`，13 个全部为真人高质量第一人称目标岗位面经；新增 Long-context / Lost in the Middle、Tool Runtime Execution Boundary、MySQL redo/binlog 2PC、Distributed ID 等 canonical 能力。

---

## 当前判断

目前并不接近来源饱和。

真正发生变化的是：随着 canonical question 越来越完整，**新增 HUMAN-A 面经更常是在强化已有知识点，而不是每篇都创造新题**。这正是我们后续做频率、公司、轮次和模块权重分析所需要的数据。
