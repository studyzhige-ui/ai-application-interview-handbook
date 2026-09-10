# Canonical Question 重建进度

更新日期：2026-09-10

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 本轮目标：不再搜索新面经，只把冻结语料归一化为正式问题数据集

## 重要修正：第一阶段按十板块重新定义

此前把 MySQL / Redis / Vector DB / RAG / Agent Harness 视为“五大核心模块”，这是旧分类，不足以覆盖已经确定的新学习路线。

现在唯一正式一级板块为：

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用工程深度）
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

`Coding / Debug / AI Coding` 不再作为一级板块，只作为 Question Type。

---

## 第一阶段：十板块全库纵向扫描

`S001–S279` 所在 26 个 Batch 已完成直接回读。十个一级板块现在都已经建立全库纵向 Canonical Question，并完成第一轮 Primary Module 归属修正。

| 顺序 | 模块 | 状态 | ACTIVE Canonical | 文件 |
|---:|---|---:|---:|---|
| 1 | Python | ✅ v1 | 15 | `python.md` |
| 2 | FastAPI | ✅ v1 | 5 | `fastapi.md` |
| 3 | AI Backend Engineering | ✅ v2 | 39 | `ai-backend-engineering.md` |
| 4 | MySQL | ✅ v2 | 26 | `mysql.md` |
| 5 | Redis | ✅ v2 | 19 | `redis.md` |
| 6 | Vector DB | ✅ v2 | 13 | `vector-db.md` |
| 7 | LLM Foundation（应用工程深度） | ✅ v1 | 22 | `llm-foundation.md` |
| 8 | RAG | ✅ v2 | 30 | `rag.md` |
| 9 | Agent Harness / Runtime | ✅ v2 | 38 | `agent-harness.md` |
| 10 | System Design | ✅ v1 | 24 | `system-design.md` |
|  | **Primary-owned ACTIVE 合计** |  | **231** |  |

因此：**第一阶段现在才算按新十板块完成。**

`231` 不是最终发布版的“全局独立问题数”。它表示当前每个 ACTIVE Canonical 都已经有一个 Primary Module；下一阶段仍需做全局 Merge / Split 与 Evidence Audit。

完整迁移记录见 `module-index.md`。

---

## 本次归属修正解决的主要旧分类问题

旧结构中存在大量“同一道核心能力在两个模块各建一题”的现象，例如：

```text
MySQL + Redis Consistency
```

过去同时存在于 MySQL / Redis；现在 Primary = `AI Backend Engineering`，MySQL / Redis 仅作为 Related Modules。

```text
Dense + Sparse → RRF → Rerank → Top-K
```

过去大量同时存在于 Vector DB / RAG；现在 Retrieval Pipeline 的 Primary = `RAG`，Vector DB 只保留 ANN / Index / Storage。

```text
SSE / WebSocket / Backpressure / Quota
```

过去部分放在 Agent Harness；现在通用 Transport / Flow Control 的 Primary = `AI Backend Engineering`，Agent 只保留 Runtime 控制语义。

```text
Lost in the Middle / Context Window 本体限制
```

现在 Primary = `LLM Foundation`；Agent Harness 保留 Context Assembly / Compaction / Memory 等应用运行时问题。

---

## 第二阶段：Cross-module Audit + Global Market Analysis

下一步从 `231` 个 Primary-owned ACTIVE 条目出发：

```text
十板块 Canonical v1/v2
        ↓
Cross-module Merge / Split Audit
        ↓
Source Count / Evidence 一致性校验
        ↓
Global Canonical Question Index
        ↓
Frequency Ranking
        ↓
Company / Role / Round Coverage
        ↓
Interview Depth / Follow-up Chain
        ↓
Curriculum Coverage Matrix
        ↓
Knowledge Gap Analysis
```

这一步会继续允许：

1. 两个模块虽然 Primary 不同，但核心知识模型仍实际相同 → Merge；
2. 某个 Canonical 过宽、混了两个可独立追问能力 → Split；
3. Source Evidence 归属过宽 / 过窄 → 修正；
4. System Design 场景与底层原理建立关联，但不重复计频。

任何修正都必须保留可追溯 `Sxxx`，不能凭常识、搜索热度或其它题库虚增真人面试频率。

---

## Agent Harness 特殊规则

Agent Harness 的面经统计层只反映 `S001–S279` 真人面试已经问到的内容。

后续正式建设 Agent 教材时，还要单独研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

用成熟实现补齐完整 Runtime / Harness 能力边界。源码属于课程实现证据，不能改变 HUMAN-A 的 `Source Count`。
