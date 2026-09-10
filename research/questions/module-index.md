# Canonical Question 十板块 Ownership Index

更新日期：2026-09-10

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

## 1. Global Merge / Split Audit 后的 Ownership

| 顺序 | 一级板块 | 文件 | ACTIVE | MOVED | 当前版本 |
|---:|---|---|---:|---:|---|
| 1 | Python | `python.md` | 15 | 0 | v2 |
| 2 | FastAPI | `fastapi.md` | 4 | 1 | v2 |
| 3 | AI Backend Engineering | `ai-backend-engineering.md` | 39 | 0 | v3 |
| 4 | MySQL | `mysql.md` | 26 | 2 | v3 |
| 5 | Redis | `redis.md` | 19 | 5 | v2 |
| 6 | Vector DB | `vector-db.md` | 12 | 11 | v3 |
| 7 | LLM Foundation（应用工程深度） | `llm-foundation.md` | 22 | 0 | v2 |
| 8 | RAG | `rag.md` | 29 | 1 | v3 |
| 9 | Agent Harness / Runtime | `agent-harness.md` | 39 | 4 | v3 |
| 10 | System Design | `system-design.md` | 24 | 0 | v2 |
|  | **合计** |  | **229** | **24** |  |

`229` 是当前经过 Global Merge / Split Audit 后的 Primary-owned ACTIVE Canonical 数量。

---

## 2. Phase 1 的主要迁移

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
- `VDB-023` Code Retrieval Boundary → 历史曾映射 `RAG-030` / `AGENT-037`；Global Audit 后统一到 `AGENT-037`

### Agent Harness → LLM / AI Backend / System Design

- `AGENT-013` Long-context 模型本体限制 → `LLM-002` / `LLM-003`
- `AGENT-033` SSE / WebSocket Transport → `AIBE-006` / `AIBE-007`; FastAPI 落地 → `FASTAPI-004`
- `AGENT-039` Concurrency / Backpressure / Quota → `AIBE-013` / `AIBE-017`
- `AGENT-040` Demo → Multi-instance Production Scale → `SD-021` + AI Backend Deployment

---

## 3. Phase 2A Global Audit 的新增修正

### `VDB-010` → `VDB-009`

Vector DB “为什么需要独立存储 / pgvector / FAISS / 专用 Vector DB”与“Milvus / FAISS / pgvector / ES Vector 产品选型”共享同一核心知识模型，合并到 `VDB-009`。合并后 Source Count = 18。

### `RAG-030` → `AGENT-037`

Code RAG / AST / LSP / ripgrep / Filesystem Search 与 Coding Agent Repository Understanding 是同一能力。`RAG-030` 的全部证据均已包含在 `AGENT-037`，因此统一 Primary = Agent Harness / Runtime。

### `AIBE-029` → 拆出 `AGENT-043`

通用 Backend Metrics / Log / Trace 留 `AIBE-029`；Agent step / model / tool / state 执行轨迹独立为 `AGENT-043`。

### `MYSQL-010` Narrow

单表 / 单分片 Deep Pagination 留 `MYSQL-010`；跨 Shard Pagination / Global Sort 由 `MYSQL-021` Sharding 承接。

### `MYSQL-022` Narrow

MySQL-specific Bulk Write 留 `MYSQL-022`；通用批处理 / 数据迁移 / Backpressure / Resume 由 `SD-007` 承接。

### `AGENT-028` Evidence 修正

补入 `S254` Agent Code Execution / Tool Permission / Sandbox 安全证据，Source Count 15 → 16。

完整判断依据与 KEEP-SEPARATE 清单见 `global-audit.md`。

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

## 6. 下一步

Phase 2A Global Merge / Split Audit 已完成。下一步从 **229 ACTIVE** 进入 Phase 2B：

```text
Global Canonical Question Index
→ Evidence / Source Count 一致性复核
→ Frequency / Company / Role / Round 统计
→ Follow-up Chain / Depth
→ Curriculum Coverage Matrix
→ Knowledge Gap Analysis
```

如果后续发现新的边界问题，不直接改分类：先回到 HUMAN-A 原始来源核验，并把决策追加到 `global-audit.md`。