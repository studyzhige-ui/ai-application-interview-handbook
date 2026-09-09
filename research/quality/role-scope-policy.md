# 面经岗位范围准入规则（Role Scope Gate）

> 本研究库只服务于 **AI 应用开发 / AI Agent 开发** 求职，不追求所有 AI 岗位面经的覆盖率。

来源除了满足 `source-quality-policy.md` 的 HUMAN-A 质量标准，还必须通过本文件的岗位方向准入。

## 1. 核心收录范围

优先收录这些岗位，或实际职责与它们高度一致的真人面试：

- AI 应用开发 / AI 应用研发
- AI Agent 开发 / 智能体开发
- Agent Harness / Agent Runtime / Coding Agent
- 大模型应用开发 / LLM 应用开发
- RAG 开发 / 知识库应用开发
- AI 全栈（核心工作是 AI Service / RAG / Agent）
- AI 后端 / Agent 后端
- Applied AI Engineer
- FDE（工作内容以大模型应用落地、系统集成为主）

岗位名称不是唯一标准。若职位标题叫“后端开发”，但岗位职责和整场面试明确围绕 Agent / RAG / LLM Service，并同时考察 MySQL、Redis、FastAPI、并发与系统设计，也可以收录。

## 2. 明确排除

以下岗位默认不进入正式面经样本，即使名称也带“AI / 算法”：

- 传统数据分析师 / BI / 商业分析 / 数据运营；
- 以 SQL 报表、指标体系、商业分析为主体的岗位；
- 纯推荐 / 广告 / 搜索排序算法岗，且与 LLM Application / Agent 无明显关系；
- 纯大模型预训练 / SFT / RLHF / CUDA / 分布式训练 / 训练 Infra 岗；
- 纯 CV / NLP 算法研究岗，只有偶然一两个 RAG / Agent 问题；
- 传统后端岗位仅顺带问 AI Coding，但岗位本身不是 AI 应用方向。

这些岗位即使包含通用计算机知识，也不能用来推断我们目标岗位的面试频率。

## 3. 通过岗位准入后，完整保留真实基础问题

一旦确认这是一场目标 AI Application / Agent 岗位的 HUMAN-A 面试，面试中真实出现的基础工程问题都应该保留，而不是只摘 AI 题：

```text
Python / GIL / asyncio
FastAPI / ASGI / HTTP / SSE
MySQL / Index / MVCC / Lock / Log
Redis / Cache / Cluster / Lock
MQ / Kafka / Reliability
Network / Concurrency / OS
Vector DB
LLM Foundation
RAG
Agent / MCP / Context / Memory / Tool
System Design
Coding
```

原因是我们要研究的是：

> **AI 应用工程师真实需要具备什么。**

而不是人为制造一个只有 Agent 名词的题库。

## 4. 模型基础与训练相关问题如何处理

如果一个明确的 AI Application / Agent 岗位真人面试中实际问到：

- Transformer / Attention；
- Token / Context Window；
- Temperature / Top-p；
- Embedding；
- Fine-tuning 基本概念；
- KV Cache / 推理行为；

可以按原面试保留，因为它们确实属于该岗位真实考察。

但完整知识体系仍保持应用工程边界，不因为偶发问题扩展成 CUDA、RLHF 或大规模训练 Infra 手册。

## 5. 固定判断流程

```text
来源是否满足 HUMAN-A？
        │
        ├─ 否 → 直接排除
        │
        ▼
岗位是否属于 AI Application / Agent 方向？
        │
        ├─ 否 → 直接排除
        │
        ▼
是否与现有来源为同一场重复？
        │
        ├─ 是 → 不重复计数
        │
        ▼
保留整场真实问题
        │
        ▼
Canonical 语义去重 + 模块映射
```

## 6. 统计原则

- Python / FastAPI / MySQL / Redis 等基础问题的频率，只从通过岗位准入的 HUMAN-A 样本中统计；
- 不使用数据分析、传统后端、推荐算法等其他岗位人为抬高基础题频率；
- 不因为 Agent Harness 深挖岗位更前沿，就错误推断基础工程能力不重要；
- 最终按 **岗位类型 × 面试轮次 × 公司 × 知识模块 × 深度** 分层分析，而不是只看一个总频率。

`source-quality-policy.md` 与本文件共同构成正式样本的固定准入：

> **先确认这是一份高质量真人第一人称面经，再确认它确实是我们要准备的岗位。**