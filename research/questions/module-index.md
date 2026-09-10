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

## 1. 第一阶段最终 Primary-owned Canonical 数量

| 顺序 | 一级板块 | 文件 | ACTIVE Canonical | MOVED | 状态 |
|---:|---|---|---:|---:|---|
| 1 | Python | `python.md` | 15 | 0 | ✅ v2 |
| 2 | FastAPI | `fastapi.md` | 4 | 1 | ✅ v2 |
| 3 | AI Backend Engineering | `ai-backend-engineering.md` | 39 | 0 | ✅ v2 |
| 4 | MySQL | `mysql.md` | 26 | 2 | ✅ v2 |
| 5 | Redis | `redis.md` | 19 | 5 | ✅ v2 |
| 6 | Vector DB | `vector-db.md` | 13 | 10 | ✅ v2 |
| 7 | LLM Foundation（应用工程深度） | `llm-foundation.md` | 22 | 0 | ✅ v2 |
| 8 | RAG | `rag.md` | 30 | 0 | ✅ v2 |
| 9 | Agent Harness / Runtime | `agent-harness.md` | 38 | 4 | ✅ v2 |
| 10 | System Design | `system-design.md` | 24 | 0 | ✅ v2 |
|  | **合计** |  | **230** | **22** | **10 / 10** |

`230` 是第一阶段完成十板块 Primary Ownership 后的 ACTIVE 条目数，**还不是第二阶段最终发布版的全局独立问题数**。后续仍要做 Global Merge / Split 与 Evidence 审计。

## 2. 从旧分类中迁移的主要问题

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
- `VDB-023` Code Retrieval Boundary → `RAG-030` / `AGENT-037`

### Agent Harness → LLM / AI Backend / System Design

- `AGENT-013` Long-context 模型本体限制 → `LLM-002` / `LLM-003`
- `AGENT-033` SSE / WebSocket Transport → `AIBE-006` / `AIBE-007`; FastAPI 落地 → `FASTAPI-004`
- `AGENT-039` Concurrency / Backpressure / Quota → `AIBE-013` / `AIBE-017`
- `AGENT-040` Demo → Multi-instance Production Scale → `SD-021` + AI Backend Deployment

## 3. Primary Module 判断例子

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

## 4. Coding / Debug / AI Coding 的位置

它们不再单独作为一级板块。

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

`Question Type` 仍可标为 `Coding`, `Debug`, `AI Coding`, `Troubleshoot`, `System Design` 等。

## 5. 下一步

第一阶段十板块归属审计已经完成。下一步对这 230 个 ACTIVE 条目做第二阶段：

```text
Global Merge / Split Audit
→ Source Count / Evidence 一致性校验
→ Global Canonical Question Index
→ Frequency / Company / Role / Round 统计
→ Follow-up Chain / Depth
→ Curriculum Coverage Matrix
→ Knowledge Gap Analysis
```

第二阶段不会新增一级分类；任何 Merge / Split 都必须保留 `Sxxx` 可追溯证据。