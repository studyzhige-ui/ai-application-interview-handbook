# 面经岗位范围准入规则（Role Scope Gate）

> 本研究库服务于 **AI 应用开发 / AI Agent 开发** 求职，不追求“所有 AI 岗位面经”的覆盖率。

从 Batch 08 起，来源除了满足 `source-quality-policy.md` 的真实性与信息密度要求，还必须通过本文件的 **岗位方向准入**。

## 1. 核心收录范围

优先收录这些岗位或实质职责高度一致的真实面试：

- AI 应用开发 / AI 应用研发
- AI Agent 开发 / 智能体开发
- Agent Harness / Agent Runtime / Coding Agent
- 大模型应用开发 / LLM 应用开发
- RAG 开发 / 知识库应用开发
- AI 全栈（核心工作是 AI Service / RAG / Agent）
- AI 后端 / Agent 后端
- Applied AI Engineer
- FDE（工作内容以大模型应用落地、系统集成为主）

岗位名称不是唯一标准。若标题叫“后端开发”，但整场面试和实际职责明确围绕 Agent / RAG / LLM Service，并同时考察 MySQL、Redis、FastAPI、并发与系统设计，也可以收录。

## 2. 明确排除

以下内容默认不进入正式面经样本，即使它们也带“AI / 算法”标签：

- 传统数据分析师 / BI / 商业分析 / 数据运营；
- 以 SQL 报表、指标体系、A/B 分析为主体的岗位；
- 纯推荐 / 广告 / 搜索排序算法岗，且与 LLM Application / Agent 无明显关系；
- 纯大模型预训练 / SFT / RLHF / CUDA / 分布式训练 / 推理引擎 Infra 岗；
- 纯 CV / NLP 算法研究岗，只有偶然一两个 RAG/Agent 问题；
- 传统后端岗位仅顺带问“你平时用不用 AI Coding”，但岗位本身并非 AI 应用方向。

这些岗位的问题可能有知识价值，但不能用来推断 **AI Application / Agent 求职** 的面试频率。

## 3. 允许出现的“基础能力”

通过岗位准入后，整场面试中的基础工程问题都应该保留，而不是只摘 AI 题：

```text
Python / GIL / asyncio
FastAPI / ASGI / HTTP / SSE
MySQL / Index / MVCC / Lock
Redis / Cache / Cluster / Lock
MQ / Kafka / Reliability
Network / Concurrency / OS
Vector DB
RAG
Agent / MCP / Context / Memory / Tool
System Design
Coding
```

原因是：我们要研究的是“AI 应用工程师真实需要具备什么”，而不是人为制造一个只有 Agent 八股的样本集。

## 4. 模型基础与训练问题如何处理

如果一个明确的 AI 应用 / Agent 岗位面试中问到：

- Transformer / Attention；
- Temperature / Top-p；
- Embedding；
- Fine-tuning；
- vLLM / 推理；

可以保留，因为它们确实属于该岗位的真实追问。

但不会因为这些题出现，就把课程扩展成“大模型算法训练手册”。是否进入主知识路线取决于：

1. 是否反复出现在 AI 应用岗位；
2. 是否直接影响应用工程决策；
3. 是否是解释 RAG / Agent / Serving 所必需的基础。

## 5. 两级判断流程

正式收录一份来源前依次判断：

```text
来源真实性 / 信息密度合格？
        │
        ├─ 否 → 排除 / Leads
        │
        ▼
岗位是否属于 AI Application / Agent 方向？
        │
        ├─ 否 → 不进入正式样本
        │
        ▼
保留整场与岗位相关的问题
        │
        ▼
Canonical 去重 + 模块映射
```

## 6. 统计原则

- “Python / MySQL / Redis 出现频率”只在通过岗位准入的 AI 应用 / Agent 样本内统计。
- 不用数据分析师、传统后端、推荐算法岗位去人为抬高数据库/算法题频率。
- 不用 Harness 专项岗的深挖比例去错误推断“Python / MySQL / Redis 已经不重要”。
- 最终按 **岗位类型 × 面试轮次 × 公司 × 知识模块** 分层分析，而不是只看一个总频率。

这个 Role Scope Gate 与 `source-quality-policy.md` 共同构成正式样本的双重门槛：

> **先保证是真的，再保证它真的是我们要找的岗位。**