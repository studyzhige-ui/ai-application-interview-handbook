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

Vector DB “为什么需要独立存储 / pgvector / FAISS / 专用 Vector DB”与“Milvus / FAISS / pgvector / ES Vector 产品选型”共享同一核心知识模型，合并到 `VDB-009`。

### `RAG-030` → `AGENT-037`

Code RAG / AST / LSP / ripgrep / Filesystem Search 与 Coding Agent Repository Understanding 是同一能力。`RAG-030` 的全部证据均已包含在 `AGENT-037`，因此统一 Primary = Agent Harness / Runtime。

### `AIBE-029` → 拆出 `AGENT-043`

通用 Backend Metrics / Log / Trace 留 `AIBE-029`；Agent step / model / tool / state 执行轨迹独立为 `AGENT-043`。

### `MYSQL-010` Narrow

单表 / 单分片 Deep Pagination 留 `MYSQL-010`；跨 Shard Pagination / Global Sort 由 `MYSQL-021` Sharding 承接。

### `MYSQL-022` Narrow

MySQL-specific Bulk Write 留 `MYSQL-022`；通用批处理 / 数据迁移 / Backpressure / Resume 由 `SD-007` 承接。

### `AGENT-028` Evidence 修正

补入 `S254` Agent Code Execution / Tool Permission / Sandbox 安全证据。

完整判断依据与 KEEP-SEPARATE 清单见 `global-audit.md`。

---

## 4. Phase 2B Coverage Gap Audit 新增 Canonical

首次全量 Source Coverage Validation 发现：229 道 Canonical 自身一致，但有 28 个 HUMAN-A 来源完全未映射。逐条回到原始 Batch 后确认其中既有 Evidence 漏挂，也有 Phase 1 真正漏掉的独立能力。

新增：

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

`S271` 为唯一 `VALID-UNMAPPED`：招聘流程明确属于 Agent 工程师大池，但本场可核验技术题全部是 React Hook / JavaScript / 版本号 Coding，不能安全归入十板块中的 AI / Backend Canonical，因此不强行造题。

详细记录：

- `source-coverage-audit.md`
- `../analysis/source-coverage-validation.md`
- `../../tools/phase2b_canonical_audit.json`

---

## 5. Primary Module 判断例子

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

```text
“LangGraph 为什么适合当前 Agent，什么时候应该不用 Framework 而自研 Runtime？”
Primary = Agent Harness / Runtime
Related = FastAPI, AI Backend Engineering
```

---

## 6. Coding / Debug / AI Coding 的位置

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

`AI-assisted Development Workflow` 虽然是 AI Coding 类型，但其核心知识模型是 Coding Agent / Human-AI Runtime Workflow，因此 Primary = Agent Harness / Runtime。

---

## 7. 当前验证状态

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

## 8. 下一步

Phase 2B 已完成：Global Index、Frequency、Company / Role / Round、Depth、Co-occurrence、Verified Follow-up Chain、Curriculum Evidence Matrix 与 Knowledge Gap Analysis 均已生成。

下一阶段进入 **Phase 3：Curriculum Build / Remediation**。

正式建设顺序：

```text
MySQL
→ Redis
→ Vector DB
→ LLM Foundation
→ RAG
→ Agent Harness / Runtime
→ System Design
```

每块教材同时以 `research/analysis/curriculum-evidence-matrix.md` 和 `research/analysis/follow-up-chains.md` 做市场验收，但课程边界仍由完整知识体系决定。
