# Canonical Question 重建进度

更新日期：2026-09-10

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 本轮目标：不再搜索新面经，只把冻结语料按正式学习路径归一化为可统计、可回溯的问题数据集

## 第一阶段正式口径

旧的“五大核心模块 + 支持模块”口径已经废弃。正式一级板块只有下面十个，并严格按学习路径组织：

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

`Coding / Debug / AI Coding` 只作为 `Question Type`，不再单独成为一级板块。

第一阶段完成标准：

1. 十个一级板块都对 `S001–S279` 完成全库纵向扫描；
2. 每一道 Canonical Question 只有一个 `Primary Module`；
3. 十个板块都完成跨模块 Merge / Move 归属审计，同一核心问题不靠复制进入多个板块；
4. 跨板块关系只通过 `Related Modules` 和 MOVED 映射表达。

---

## 全库读取状态

`S001–S279` 所在 26 个 Batch 已完成直接回读，并已按十板块完成一轮语义归一化与归属复核。

> Batch 文件中的历史“累计来源数 / 下一编号”等过程性统计按采集时口径保留；Canonical 重建只使用当前去重后的 `S001–S279` 正式编号。

## 十板块 v2 状态

| 顺序 | 一级板块 | 状态 | ACTIVE Canonical | MOVED |
|---:|---|---:|---:|---:|
| 1 | Python | ✅ v2 | 15 | 0 |
| 2 | FastAPI | ✅ v2 | 4 | 1 |
| 3 | AI Backend Engineering | ✅ v2 | 39 | 0 |
| 4 | MySQL | ✅ v2 | 26 | 2 |
| 5 | Redis | ✅ v2 | 19 | 5 |
| 6 | Vector DB | ✅ v2 | 13 | 10 |
| 7 | LLM Foundation（应用工程深度） | ✅ v2 | 22 | 0 |
| 8 | RAG | ✅ v2 | 30 | 0 |
| 9 | Agent Harness / Runtime | ✅ v2 | 38 | 4 |
| 10 | System Design | ✅ v2 | 24 | 0 |
|  | **合计** | **10 / 10** | **230 ACTIVE** | **22 MOVED** |

因此：**第一阶段现在才正式完成。**

`230` 是完成十板块 Primary Ownership 后的 ACTIVE 模块条目数。它仍不是最终发布版“全局独立问题数”，因为第二阶段还要对整个集合做 Global Merge / Split 与 Evidence 一致性审计。

---

## 第一阶段关键归属修正

### Python / FastAPI

```text
FastAPI async 调 LLM 时 await 期间 Event Loop / CPU / Thread 在做什么
        ↓
Primary = Python / PY-012
Related = FastAPI, AI Backend Engineering
```

因此旧 `FASTAPI-003` 已 MOVED，不再重复计一题。

### AI Backend / MySQL / Redis

```text
MySQL + Redis 双写一致性
        ↓
Primary = AI Backend Engineering / AIBE-020
Related = MySQL, Redis
```

数据库自身事务 / 索引 / 日志继续留 MySQL；Redis 自身数据结构 / Cluster / Lock / Lua 继续留 Redis。

### Vector DB / LLM / RAG

```text
Embedding / Rerank Model 原理 → LLM Foundation
ANN / HNSW / IVF / Vector Storage → Vector DB
Dense/Sparse / Hybrid / RRF / Rerank Pipeline / Top-K / Retrieval Eval → RAG
```

### LLM / Agent Harness

```text
Context Window / Lost in the Middle 的模型本体限制 → LLM Foundation
Context Assembly / Compaction / Memory / Tool Runtime → Agent Harness / Runtime
```

### Agent / AI Backend / System Design

```text
SSE / WebSocket 协议与通用 Streaming Reliability → AI Backend Engineering
Agent Event / State / Tool / Checkpoint 控制语义 → Agent Harness / Runtime
端到端 Production Agent Backend / Long-running Agent → System Design
```

---

## 第二阶段：Global Canonical Audit + Market Analysis

下一步从这 **230 个 ACTIVE** 出发，不再改一级分类，而是做全局问题层审计：

```text
230 Primary-owned Canonical
        ↓
Global Merge / Split Audit
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

第二阶段允许继续修正：

1. 两个不同 Primary Module 的条目如果核心知识模型实际上仍相同 → Merge；
2. 某个 Canonical 过宽、混了两个可独立追问能力 → Split；
3. Evidence Source 归属过宽 / 过窄 → 修正；
4. System Design 场景与底层能力建立关系，但不把场景频率重复计到底层问题上。

任何修正都必须保留可追溯 `Sxxx`，不能凭常识、搜索热度或其它题库虚增真人面试频率。

## Agent Harness 特殊规则

Agent Harness 的面经统计层只反映 `S001–S279` 真人面试已经问到的内容。

后续正式建设 Agent 教材时，还要单独研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

成熟源码属于课程实现证据，不能反向改变 HUMAN-A 的 `Source Count`。