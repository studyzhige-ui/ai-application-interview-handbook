# 2026 AI 应用 / Agent 真人面经研究

这里不是“面试题大全”，而是整套 AI Application / Agent 求职知识体系的 **真人招聘现实校准层**。

## 当前进度（2026-09-10）

- 当前活跃来源：**254 个 HUMAN-A 真人高质量第一人称样本（S001–S254）**。
- 当前正式批次：[`Batch 01`](./interviews/batch-01.md) + [`Batch 02`](./interviews/batch-02.md) + [`Batch 03`](./interviews/batch-03.md) + [`Batch 04`](./interviews/batch-04.md) + [`Batch 05`](./interviews/batch-05.md) + [`Batch 06`](./interviews/batch-06.md) + [`Batch 07`](./interviews/batch-07.md) + [`Batch 08`](./interviews/batch-08.md) + [`Batch 09`](./interviews/batch-09.md) + [`Batch 10`](./interviews/batch-10.md) + [`Batch 11`](./interviews/batch-11.md)。
- Batch 01：`S001–S013`，13 个。
- Batch 02：`S014–S031`，新增 18 个。
- Batch 03：`S032–S051`，新增 20 个。
- Batch 04：`S052–S074`，新增 23 个。
- Batch 05：`S075–S094`，新增 20 个。
- Batch 06：`S095–S117`，新增 23 个。
- Batch 07：`S118–S147`，新增 30 个。
- Batch 08：`S148–S168`，新增 21 个。
- Batch 09：`S169–S196`，新增 28 个。
- Batch 10：`S197–S225`，新增 29 个。
- Batch 11：`S226–S254`，新增 **29 个 HUMAN-A**。
- Canonical Question 只允许从当前 HUMAN-A 来源累计证据；低质量来源继续保持零贡献。
- 当前仍未达到来源饱和：泛搜索重复率持续升高，但精确公司 / 岗位 / 月份 / 轮次、企业 / 话题页、作者时间线和跨平台原帖回溯仍持续产生新 HUMAN-A。

详细准入规则：

- [`quality/source-quality-policy.md`](./quality/source-quality-policy.md)：统一 HUMAN-A 来源标准。
- [`quality/role-scope-policy.md`](./quality/role-scope-policy.md)：目标岗位范围。

---

# 唯一正式来源标准：HUMAN-A

**平台不是质量标准。** 牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客以及其他公开来源全部一视同仁。

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

任意一项不满足，都不进入正式 Batch、Canonical Question、频率统计和课程优先级分析。平台只影响核验难度，不影响门槛，也不设平台入库配额。

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

传统数据分析 / BI、普通后端、纯推荐 / 广告排序、纯训练 / CUDA / RLHF Infra、纯 CV / NLP 研究等默认不进入，不能为了补基础题混入统计。

---

# 知识体系与面经的分工

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

Python、FastAPI、Backend、MySQL、Redis、MQ、OS、Network、Concurrency、Vector DB、LLM、RAG、Agent、Harness、System Design、Coding 等，只要是该场真人面试真实问到的，都一视同仁记录。

这意味着像 Batch 11 中阿里云后端 Agent 几乎全问 OS / MySQL / Redis，滴滴 AI Backend 几乎全问数据库和限流，也依然是非常重要的目标岗位证据；不需要引入普通后端面经人为补基础频率。

HUMAN-A 面经负责：

- 提供真人面试官真实问法；
- 校准不同模块真实出现频率；
- 观察公司 / 岗位 / 轮次的追问深度；
- 验证知识能否真正口述、设计、Debug 和 Coding；
- 反向校准完整知识体系的复习优先级。

低质量来源不会为了补知识点增加任何学习任务。

---

# 数据与去重

每个正式来源至少记录：

- `source_id`；
- 公司 / 岗位 / 日期 / 轮次；
- 原始 URL；
- 真人 / 第一人称 / 现场证据；
- 5～12 条左右高信息量问题的简洁转述；
- 去重结论。

同一候选人的同一招聘流程存在一面 / 二面 / 三面多篇帖子时，在能够确认同源后合并为一个来源，但保留各轮真实问题。

固定三层去重：

```text
URL 精确去重
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
```

- 同候选人同流程多轮 → 合并；
- 跨平台同步 / 镜像 / 后发近似复制 → 只保留更原始、更稳定、更有现场证据的一份；
- 两个独立候选人遇到相同问题 → 分别计为独立真人命中；
- 无法可靠确认原帖归属的逐题复制链 → 宁可整链排除，也不猜测原作者。

Canonical Question 是 HUMAN-A 的语义去重层，不是第二套知识体系。规则见 [`questions/README.md`](./questions/README.md)。

---

# 搜索范围与方法

持续使用：

```text
公司
×
岗位别名（AI应用开发 / Agent开发 / 智能体开发 / 大模型应用开发 /
LLM应用 / RAG开发 / AI后端 / AI全栈 / Applied AI / FDE / Coding Agent）
×
月份（重点 2026-03～09，同时追最新发布）
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

主动搜索牛客、小红书、知乎、脉脉、CSDN、掘金、Bilibili、抖音、个人博客和独立站。**平台多元化只用于提高 Recall，不用于凑来源数量。** 搜索摘要、App 跳转和聚合页只能用于发现；最终正文 / 作者 / 现场无法稳定核验，就不进入 HUMAN-A。

---

# Batch 11 后的信号

当前 254 个 HUMAN-A 已经反复验证完整能力路线：

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

Batch 11 进一步强化：

- **全知识链路不是理论假设，而是目标岗位真实面试结构。** 同一场经常混合 Python / FastAPI / OS / MySQL / Redis / MQ 与 RAG / Agent / Harness。
- **FastAPI / Python Service Engineering 继续得到独立真人命中。** Middleware vs Dependency、multiprocessing / threading、`asyncio.gather` vs `as_completed`、超时降级与 Multi-Agent / Milvus 同场出现。
- **Harness 越来越强调控制边界。** 写操作边界、Harness Layer、Intent Routing、Skill Fetch、Dead Loop、Checkpoint、Max Step、Structured Context Passing 等都进入真人追问。
- **AI Backend System Design 权重稳定。** 千万 QPS、大促 Capacity Planning、10TB/day Storage、Hot/Cold Separation、Redis Cluster Migration、MQ Backlog、Rate Limit、Cache Consistency 都来自目标 AI 岗。
- **RAG 越来越像可测量 Retrieval System。** Milvus Collection / Partition、BM25、Rerank、Query Rewrite、Top-K、HNSW、Recall Evaluation、Latency / Quality Trade-off 都被追问选择依据与证据。
- **项目验真仍然比框架名词更重要。** 日调用量、用户规模、本人职责、性能指标、业务价值、项目是否真正做过、为什么不是更简单方案，被持续追问。
- **多平台主动召回有必要，但正式入库平台分布不需要人为均衡。** 本批确实扩大了非牛客搜索，但大量外部结果仍属于教程、转载、模拟或低密度内容；它们因内容不合格被排除，不代表平台降权。
- **去重成本继续升高。** 本批发现京东后端 Agent 两个不同 URL 几乎逐题一致，且无法稳定确认原始候选人，因此整链排除；这比按“发布时间最早”猜原帖更保守。
- **仍未达到来源饱和。** 在已有 225 个 HUMAN-A 后，本批严格清洗仍新增 29 个独立来源。

---

# 什么时候停止继续搜？

停止条件从来不是某个 `Sxxx`、Batch 数或题目数，而是出现**来源饱和**。

持续同时观察：

```text
A. 新增 HUMAN-A 绝对数量
B. 新增 HUMAN-A / 全部候选结果 的比例
C. 已收录重复比例
D. 二次整理 / 低质量 / Role Scope 外比例
```

只有连续多轮扩大公司、岗位、月份、轮次和平台 Recall 后，同时出现以下信号，才进入收尾：

1. 新结果绝大多数已经是已收录同场、转载、合集、答案型内容、低质量来源或 Role Scope 外来源；
2. 新增 HUMAN-A 的数量与占比都持续接近零；
3. 精确公司 / 轮次 / 作者页 / 原帖回溯也很难发现新来源，而不是只有泛搜索变重复；
4. 新增来源的公司 / 岗位 / 轮次与知识模块、追问深度分布稳定收敛。

**当前 254 个样本仍未达到停止点：泛搜索重复率较高，但 Batch 11 在已有 225 个 HUMAN-A 后仍新增 29 个独立高质量来源。**
