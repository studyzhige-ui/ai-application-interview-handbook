# Canonical Question 十板块 Ownership Index

更新日期：2026-09-11

> **Repository-first：** 本文件与 `README.md`、`schema.md`、`progress.md`、各模块最新文件共同构成当前正式口径；历史聊天总结或旧分类不能覆盖这里的最新状态。

本文件是 `S001–S279` 冻结 HUMAN-A 语料在正式学习路径下的一级归属索引。

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

## 1. Phase 2B 后的正式 Ownership

| 顺序 | 一级板块 | 文件 | ACTIVE | MOVED | 当前版本 |
|---:|---|---|---:|---:|---|
| 1 | Python | `python.md` | 15 | 0 | v2 |
| 2 | FastAPI | `fastapi.md` | 4 | 1 | v2 |
| 3 | AI Backend Engineering | `ai-backend-engineering.md` | 39 | 0 | v3 |
| 4 | MySQL | `mysql.md` | 26 | 2 | v3 |
| 5 | Redis | `redis.md` | 19 | 5 | v2 |
| 6 | Vector DB | `vector-db.md` | 12 | 11 | v3 |
| 7 | LLM Foundation（应用工程深度） | `llm-foundation.md` | 23 | 0 | v3 |
| 8 | RAG | `rag.md` | 29 | 1 | v3 |
| 9 | Agent Harness / Runtime | `agent-harness.md` | 44 | 4 | v4 |
| 10 | System Design | `system-design.md` | 24 | 0 | v2 |
|  | **合计** |  | **235** | **24** |  |

`235` 是当前经过 Phase 2A Global Merge / Split Audit + Phase 2B Coverage Gap Audit 后的 Primary-owned ACTIVE Canonical 数量。

---

## 2. Phase 1 / 2A 的主要归属修正

### FastAPI → Python

- `FASTAPI-003` `await` 期间 Event Loop / CPU / Thread 语义 → `PY-012`

### MySQL → AI Backend Engineering

- `MYSQL-001` 数据分层 → `AIBE-039`
- `MYSQL-023` DB + Cache Consistency → `AIBE-020`

### Redis → AI Backend / Agent / System Design

- `REDIS-001` 数据分层 → `AIBE-039`
- `REDIS-015` DB + Cache Consistency → `AIBE-020`
- `REDIS-018` Agent Checkpoint → `AGENT-027` / `AGENT-029` / `SD-022`
- `REDIS-020` Token Budget / Fair Queue → `AIBE-013` / `AIBE-017`
- `REDIS-023` Redis vs MQ → `AIBE-014`

### Vector DB → LLM Foundation / RAG / Agent

- `VDB-001` Embedding Model / semantic representation → `LLM-018`
- `VDB-012` Dense vs Sparse → `RAG-012`
- `VDB-013` Hybrid Retrieval → `RAG-013`
- `VDB-014` BM25 → `RAG-012` / `RAG-013`
- `VDB-015` RRF → `RAG-014`
- `VDB-016` Rerank Pipeline → `RAG-015`; Model 原理 → `LLM-019`
- `VDB-017` Top-K → `RAG-016`
- `VDB-019` Retrieval Evaluation → `RAG-020` / `RAG-021`
- `VDB-021` Multimodal Retrieval → `RAG-005`; 模型侧 → `LLM-010`
- `VDB-023` Code Retrieval Boundary → Global Audit 后统一到 `AGENT-037`

### Agent Harness → LLM / AI Backend / System Design

- `AGENT-013` Long-context 模型本体限制 → `LLM-002` / `LLM-003`
- `AGENT-033` SSE / WebSocket Transport → `AIBE-006` / `AIBE-007`; FastAPI 落地 → `FASTAPI-004`
- `AGENT-039` Concurrency / Backpressure / Quota → `AIBE-013` / `AIBE-017`
- `AGENT-040` Demo → Multi-instance Production Scale → `SD-021` + AI Backend Deployment

### Global Audit

- `VDB-010` → `VDB-009`：向量存储架构 / 产品选型合并。
- `RAG-030` → `AGENT-037`：Code RAG / Repo Search 统一到 Coding Agent Repository Understanding。
- `AIBE-029` → 拆出 `AGENT-043`：通用 Observability 与 Agent Execution Trace 分离。
- `MYSQL-010` Narrow：单表 Deep Pagination 与跨 Shard Pagination 分离。
- `MYSQL-022` Narrow：MySQL Bulk Write 与通用 Batch / Migration 分离。
- `AGENT-028`：补入 `S254` Permission / Sandbox 安全证据。

完整判断依据见 `global-audit.md`。

---

## 3. Phase 2B Coverage Gap Audit 新增 Canonical

| QID | Primary Module | Topic | Source Count |
|---|---|---|---:|
| `LLM-023` | LLM Foundation（应用工程深度） | Prompt Engineering | 30 |
| `AGENT-044` | Agent Harness / Runtime | Prompt Injection / Untrusted Context Security | 8 |
| `AGENT-045` | Agent Harness / Runtime | Intent Recognition / Routing | 11 |
| `AGENT-046` | Agent Harness / Runtime | A2A / Agent Communication Protocol | 6 |
| `AGENT-047` | Agent Harness / Runtime | Agent Framework Selection | 27 |
| `AGENT-048` | Agent Harness / Runtime | AI-assisted Development Workflow | 37 |

因此：

```text
229
+ 6 reviewed independent knowledge models
= 235 ACTIVE
```

`S271` 为唯一 `VALID-UNMAPPED`。

详细记录：

- `source-coverage-audit.md`
- `../analysis/source-coverage-validation.md`
- `../../tools/phase2b_canonical_audit.json`

---

## 4. Primary Module 判断例子

```text
“RRF 为什么不用线性加权？”
Primary = RAG
Related = Vector DB
```

```text
“HNSW 为什么快，efSearch 怎样影响 Recall？”
Primary = Vector DB
Related = RAG
```

```text
“FastAPI async 调 LLM，await 期间 CPU / Event Loop / Thread 在做什么？”
Primary = Python
Related = FastAPI, AI Backend Engineering
```

```text
“Tool 已成功扣款，但 Checkpoint 写失败，恢复后怎么办？”
Primary = Agent Harness / Runtime
Related = AI Backend Engineering, System Design
```

```text
“Redis + MySQL 双写一致性怎样保证？”
Primary = AI Backend Engineering
Related = MySQL, Redis
```

```text
“Prompt 怎样从 Goal / Constraint / Context / Example / Output Contract 组织并做 Regression？”
Primary = LLM Foundation（应用工程深度）
Related = RAG, Agent Harness / Runtime
```

---

## 5. Coding / Debug / AI Coding 的位置

它们不是一级板块，而是 Question Type：

- Python Decorator 手写 → Python
- FastAPI Streaming / Middleware 实现 → FastAPI
- MQ / Linux / ThreadPool Troubleshoot → AI Backend Engineering
- SQL / Index Coding → MySQL
- Redis Lua Implementation → Redis
- ANN / Index 参数推演 → Vector DB
- Attention / RoPE 手写 → LLM Foundation
- Retrieval Evaluation / Chunk Failure → RAG
- Coding Agent Repo Modification / Verification → Agent Harness / Runtime
- 完整业务架构题 → System Design

---

## 6. 当前验证状态

```text
Frozen HUMAN-A              279 / 279
ACTIVE Canonical            235 / 235
Mapped to >=1 Canonical     278
VALID-UNMAPPED                1
Unexpected uncovered          0
Evidence outside baseline     0
Source Count mismatch         0
```

---

## 7. Phase 3 Curriculum Build 状态

Canonical Ownership 已稳定，当前工作重点已经从“题目归属”切换为“把研究结果反哺完整教材”。

固定原则：

> **初学者 0→1 的知识依赖决定课程主干；真人面经只校准复习权重、真实问法和追问深度。**

当前建设顺序与状态：

```text
MySQL ✅ 23 章 + Review + Interview
→ Redis ✅ 27 章 + Review + Interview
→ Vector DB ✅ 23 章 + Review + Interview
→ LLM Foundation ✅ 29 章 + Review + Interview
→ RAG 🚧 当前建设
→ Agent Harness / Runtime
→ System Design
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有课程骨架，后续按项目与 Bridge Lab 补齐正文。

每完成一个模块，必须同步：模块 README、根 `README.md`、`roadmap/knowledge-map.md`、`progress.md`、自动生成 Analysis 的源头/结果、`module-index.md`，以及所有仍写着“下一块 / 待建设”的入口。
