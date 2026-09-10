# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-10）

- 当前活跃来源：**225 个 HUMAN-A 真人高质量第一人称样本（S001–S225）**。
- 当前正式批次：[`Batch 01`](./interviews/batch-01.md) + [`Batch 02`](./interviews/batch-02.md) + [`Batch 03`](./interviews/batch-03.md) + [`Batch 04`](./interviews/batch-04.md) + [`Batch 05`](./interviews/batch-05.md) + [`Batch 06`](./interviews/batch-06.md) + [`Batch 07`](./interviews/batch-07.md) + [`Batch 08`](./interviews/batch-08.md) + [`Batch 09`](./interviews/batch-09.md) + [`Batch 10`](./interviews/batch-10.md)。
- Batch 01：`S001–S013`，13 个。
- Batch 02：`S014–S031`，新增 18 个。
- Batch 03：`S032–S051`，新增 20 个。
- Batch 04：`S052–S074`，新增 23 个。
- Batch 05：`S075–S094`，新增 20 个。
- Batch 06：`S095–S117`，新增 23 个。
- Batch 07：`S118–S147`，新增 30 个。
- Batch 08：`S148–S168`，新增 21 个。
- Batch 09：`S169–S196`，新增 28 个。
- Batch 10：`S197–S225`，新增 **29 个 HUMAN-A**。
- Canonical Question 层只允许从当前 HUMAN-A 来源累计证据；低质量来源继续保持零贡献。
- 当前仍未达到来源饱和。泛关键词搜索重复率持续上升，但精确公司 / 岗位 / 月份 / 轮次、企业 / 话题页、作者时间线和跨平台原帖回溯仍能产生显著新增。

详细规则：

- [`quality/source-quality-policy.md`](./quality/source-quality-policy.md)：统一 HUMAN-A 来源标准。
- [`quality/role-scope-policy.md`](./quality/role-scope-policy.md)：目标岗位范围。

---

# 唯一正式来源标准：HUMAN-A

平台不是质量标准。牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客以及其他公开来源全部一视同仁。

正式来源必须同时满足：

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

任意一项不满足，都不进入正式 Batch、Canonical Question、频率统计和课程优先级分析。

平台只影响核验难度，不影响准入门槛。

---

# Role Scope

核心方向包括：

```text
AI 应用开发 / AI 应用研发
AI Agent / 智能体开发
RAG / 知识库应用开发
AI Backend / Agent Backend
AI Full-stack
Agent Harness / Runtime
Coding Agent
LLM Application
Applied AI / FDE（以大模型应用落地与系统集成为核心）
```

岗位名称不是唯一标准。标题即使叫“后端”，只要实际职责和整场真人面试明确围绕 Agent / RAG / LLM Service，同时考察 Backend / DB / Concurrency / System Design，也可以通过 Role Scope。

传统数据分析 / BI、普通后端、纯推荐 / 广告排序、纯训练 / CUDA / RLHF Infra、纯 CV / NLP 研究等默认不进入，除非实际岗位内容明确属于上述应用工程方向。

---

# 知识体系与面经的分工

本项目坚持：

> **知识体系是骨架，高质量真人面经是血肉。**

完整知识体系决定应该系统学习什么：

```text
Python
FastAPI
Backend Engineering
MySQL
Redis
Vector Database
LLM Foundation（应用工程深度）
RAG
Agent Harness / Runtime
System Design
```

并自然覆盖真人场次实际出现的：

```text
OS / Network / Concurrency
MQ / Kafka / Reliability
HTTP / SSE / WebSocket
Coding / Debug / Evaluation / Security
```

## 通过 Role Scope 后：整场真实问题全部保留

一旦确认是一场目标 AI Application / Agent 岗 HUMAN-A，就不只摘 Agent / RAG 问题。

Python、FastAPI、MySQL、Redis、MQ、OS、Network、Concurrency、Vector DB、LLM、RAG、Agent、Harness、System Design、Coding 等，只要是该场真人面试真实问到的，都一视同仁记录。

原因是本项目研究的是：

> **AI 应用工程师真实需要具备什么。**

而不是制造一个只有 Agent 名词的题库。

HUMAN-A 面经负责：

- 提供真人面试官真实问法；
- 校准不同模块真实出现频率；
- 观察公司 / 岗位 / 轮次的追问深度；
- 验证知识能否真正口述、设计、Debug 和 Coding；
- 反向校准完整知识体系的复习优先级。

低质量来源不会为了补知识点增加任何学习任务。

---

# 数据层

## 1. Interviews / Sources

每个正式来源至少记录：

- `source_id`
- 公司 / 岗位 / 日期 / 轮次
- 原始 URL
- 真人 / 第一人称证据
- 5～12 条左右高信息量问题的简洁转述；若一场问题更多但都很重要，可适度保留更多

第三方面经只保存研究所需元数据与问题转述，不复制全文。

同一候选人的同一招聘流程如果存在一面 / 二面 / 三面多篇帖子，在能够确认同源时合并计为一个来源，但各轮真实问题全部保留。

## 2. Canonical Questions

Canonical Question 是 HUMAN-A 面经的**语义去重层**，不是第二套知识体系。

多个独立真人来源语义相同的问题可以归并成一个 Capability，并分别记录独立 HUMAN-A 命中。没有 HUMAN-A 证据的问题不能进入这一层。

规则见：[`questions/README.md`](./questions/README.md)。

---

# 搜索范围与方法

持续使用：

```text
公司
×
岗位别名（AI应用开发 / Agent开发 / 智能体开发 / 大模型应用开发 /
LLM应用 / RAG开发 / AI后端 / AI全栈 / Applied AI / FDE / Coding Agent）
×
月份（重点 2026-03～09，同时持续追最新发布）
×
技术关键词（Python / FastAPI / asyncio / MySQL / Redis / Vector DB /
RAG / MCP / Skill / Harness / Runtime / Context / Memory / Tool / Coding）
```

并继续回溯：

```text
企业 / 话题页
→ 精确标题 / 精确轮次
→ 作者主页 / 个人博客
→ 原帖正文
→ 跨平台重复核验
```

牛客之外也持续搜索小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客等公开来源。平台多样性只用于提高 Recall，**不能用于降低质量门槛或凑来源数量**。

登录态、App 跳转、搜索摘要只允许作为发现线索；最终正文 / 作者 / 现场不能稳定核验，就不进入 HUMAN-A。

---

# 固定去重

URL 不同不代表独立来源。当前固定使用三层：

```text
URL 精确去重
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
```

- 同候选人同招聘流程多轮 → 合并为一个来源；
- 同一场跨平台同步 / 后发近似复制 → 只保留更原始、更可验证的一份；
- 两个独立候选人遇到相同问题 → 仍然是两个独立真人命中。

---

# Batch 10 后的信号

当前 225 个 HUMAN-A 已经反复验证完整路线，而不是只有 Agent 名词：

```text
Python / OS / Network
        ↓
FastAPI / Async / Streaming / Backend Runtime
        ↓
MySQL / Redis / MQ / Concurrency / Sharding
        ↓
Vector DB / RAG / Retrieval Evaluation
        ↓
LLM Foundation / Context / KV Cache
        ↓
Agent / Tool / MCP / Skill / Memory
        ↓
Harness / Runtime / Checkpoint / Resume / Permission
        ↓
Coding Agent / Spec / Worktree / Trace / Evaluation
        ↓
Production / Security / System Design
```

Batch 10 进一步强化：

- **基础工程与 Agent 是同一目标岗位的真实能力栈。** 小红书 AI 后端、滴滴 AI Agent 后端、字节 AI 应用、科大讯飞 Agent、金山 AI 全栈等真人场次都同时出现 MySQL / Redis / MQ / OS / Network / Concurrency 与 RAG / Agent / Harness。
- **Python / FastAPI / Async 是正式主线。** FastAPI Middleware vs Dependency、`asyncio.gather` vs `as_completed`、Process / Thread / Coroutine、PDF workload 并发模型选择等均来自目标岗位真人面试。
- **Harness / Runtime 深入可控执行。** Session / Transcript Resume、TodoStore、LTM Conflict、Skill Progressive Disclosure、Shell Permission、Compaction Verification、Multi-Pod Routing、Consistent Hashing 等开始稳定出现。
- **RAG 继续强调参数、故障与证据。** Milvus Collection / Partition、Dense / Sparse、Top-K、Rerank、Incremental Index、No-answer、HyDE、Hybrid Retrieval、Evaluation 都在被追问“为什么”和“怎么证明”。
- **项目验真持续加强。** Business Metric、上下游、本人职责、为什么 Agent 而不是 Script / Workflow、性能指标怎样测、AI Coding 代码怎样验收，比单纯框架名词更能区分深度。
- **语义去重成本继续上升。** 已出现不同 URL 但题序几乎逐条一致的后发版本，后续必须继续依赖作者 / 项目 / 时间线判断。
- **平台统一门槛继续成立。** Bilibili、CSDN、个人博客等都继续搜索；通过与否只由 HUMAN-A Gate 决定，而不是平台名。

---

# 什么时候停止继续搜？

停止条件从来不是某个 `Sxxx`、Batch 数或题目数，而是出现**来源饱和**。

后续持续同时观察：

```text
A. 新增 HUMAN-A 绝对数量
B. 新增 HUMAN-A / 全部候选结果 的比例
C. 已收录重复比例
D. 二次整理 / 低质量 / Role Scope 外比例
```

只有连续多轮扩大公司、岗位、月份、轮次和平台 Recall 后，同时满足以下条件，才进入收尾：

1. 新结果绝大多数已经是已收录同场、转载、合集、答案型内容、低质量来源或 Role Scope 外来源；
2. 新增 HUMAN-A 的数量与占比都持续接近零；
3. 精确公司 / 轮次 / 作者页 / 原帖回溯也很难发现新来源，而不是只有泛搜索变重复；
4. 新增来源的公司 / 岗位 / 轮次与知识模块、追问深度分布已经稳定收敛。

**当前 225 个样本仍未达到停止点：泛搜索重复率较高，但 Batch 10 在已有 196 个 HUMAN-A 后仍新增 29 个独立高质量来源。**
