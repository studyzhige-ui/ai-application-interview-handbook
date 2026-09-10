# Canonical Question 十板块 Ownership Index

更新日期：2026-09-10

本文件是 `S001–S279` 冻结 HUMAN-A 语料在新学习路径下的一级归属索引。

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

## 1. 当前 Primary-owned Canonical 数量（阶段一审计中）

| 顺序 | 一级板块 | 文件 | ACTIVE Canonical | 审计状态 |
|---:|---|---|---:|---|
| 1 | Python | `python.md` | 15 | 🟡 v1，待 v2 |
| 2 | FastAPI | `fastapi.md` | 4 | ✅ v2；另 1 MOVED |
| 3 | AI Backend Engineering | `ai-backend-engineering.md` | 39 | ✅ v2 |
| 4 | MySQL | `mysql.md` | 26 | ✅ v2；另 2 MOVED |
| 5 | Redis | `redis.md` | 19 | ✅ v2；另 5 MOVED |
| 6 | Vector DB | `vector-db.md` | 13 | ✅ v2；另 10 MOVED |
| 7 | LLM Foundation（应用工程深度） | `llm-foundation.md` | 22 | 🟡 v1，待 v2 |
| 8 | RAG | `rag.md` | 30 | ✅ v2 |
| 9 | Agent Harness / Runtime | `agent-harness.md` | 38 | ✅ v2；另 4 MOVED |
| 10 | System Design | `system-design.md` | 24 | 🟡 v1，待 v2 |
|  | **当前 ACTIVE 暂计** |  | **230** | **7 / 10 已完成 v2** |

`230` 仍然只是当前阶段的模块 ACTIVE 条目数，**不是最终发布版的全局独立问题数**。Python、LLM Foundation、System Design 仍需完成 v2 Primary Ownership / Merge-Move 审计，因此第一阶段尚未结束。

## 2. 已完成的主要归属迁移

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
- `VDB-023` Code Retrieval Boundary → `RAG-030` / `AGENT-037`

### Agent Harness → LLM / AI Backend / System Design

- `AGENT-013` Long-context 模型本体限制 → `LLM-002` / `LLM-003`
- `AGENT-033` SSE / WebSocket Transport → `AIBE-006` / `AIBE-007`; FastAPI 落地 → `FASTAPI-004`
- `AGENT-039` Concurrency / Backpressure / Quota → `AIBE-013` / `AIBE-017`
- `AGENT-040` Demo → Multi-instance Production Scale → `SD-021` + AI Backend Deployment

### FastAPI → Python

- `FASTAPI-003` `await` 期间 Event Loop / CPU / Thread 语义 → `PY-012`

这次迁移用于消除“因为问题出现在某框架语境，就在两个板块各建一题”的重复。

## 3. Primary Module 判断例子

```text
“RRF 为什么不用线性加权？”
Primary = RAG
Related = Vector DB
```

因为它问的是 Retrieval Pipeline 的多路融合，而不是 ANN Storage。

```text
“HNSW 为什么快，efSearch 怎样影响 Recall？”
Primary = Vector DB
Related = RAG
```

因为核心知识模型是 ANN Index。

```text
“FastAPI async 调 LLM，await 期间 CPU / Event Loop / Thread 在做什么？”
Primary = Python
Related = FastAPI, AI Backend Engineering
```

因为核心知识模型是 `asyncio` Runtime，而不是 FastAPI 路由 API。

```text
“Tool 已成功扣款，但 Checkpoint 写失败，恢复后怎么办？”
Primary = Agent Harness / Runtime
Related = AI Backend Engineering, System Design
```

因为它考察的是 Agent Runtime 的外部副作用与 Resume 语义，而不是一般 HTTP 幂等定义。

```text
“Redis + MySQL 双写一致性怎样保证？”
Primary = AI Backend Engineering
Related = MySQL, Redis
```

因为它是跨存储的数据一致性 / Cache Architecture，而不是某个单一数据库的内部机制。

## 4. Coding / Debug / AI Coding 的位置

它们不再单独作为一级板块。

- Python Decorator 手写 → Python
- FastAPI Async Endpoint / Streaming 实现 → FastAPI
- MQ / Linux / ThreadPool Troubleshoot → AI Backend Engineering
- SQL / Index Coding → MySQL
- Redis Lua Implementation → Redis
- ANN / Index 参数推演 → Vector DB
- Attention / RoPE 手写 → LLM Foundation
- Retrieval Evaluation / Chunk Failure → RAG
- Coding Agent Repo Modification / Verification → Agent Harness / Runtime
- 完整业务架构题 → System Design

`Question Type` 仍可标为 `Coding`, `Debug`, `AI Coding`, `Troubleshoot`, `System Design` 等。

## 5. 第一阶段剩余工作

当前不进入全局频率发布。先完成：

```text
Python v2 audit
→ LLM Foundation v2 audit
→ System Design v2 audit
→ 十板块最终 Primary Ownership consistency check
```

只有十个板块全部通过 v2 后，才开始：

```text
Global Merge / Split Audit
→ Source Count / Evidence 一致性校验
→ Global Canonical Question Index
→ Frequency / Company / Role / Round 统计
→ Follow-up Chain / Depth
→ Curriculum Coverage Matrix
→ Knowledge Gap Analysis
```
