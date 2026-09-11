# Canonical Question 十板块 Ownership Index

更新日期：2026-09-11

> **Repository-first：** 本文件与 `README.md`、`schema.md`、`progress.md`、各模块最新文件共同构成当前正式口径；历史聊天总结或旧分类不能覆盖这里的最新状态。

## 1. 正式十板块与 Phase 2B Ownership

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

`235` 是 Phase 2A + Phase 2B 后的正式 Primary-owned ACTIVE Canonical 数量。

---

## 2. 主要跨模块迁移

- FastAPI async runtime 本体 → Python；
- MySQL / Redis 数据分层与 DB+Cache 一致性 → AI Backend Engineering；
- Dense/Sparse、Hybrid、RRF、Rerank Pipeline、Top-K、Retrieval Eval → RAG；
- Embedding / Reranker 模型内部原理 → LLM Foundation；
- Code RAG / Repo Search → Agent Harness Repository Understanding；
- SSE / WebSocket transport、通用 Concurrency / Backpressure → AI Backend；
- Agent Demo → Multi-instance Production Scale → System Design。

完整历史判断见 `global-audit.md`。

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

`S271` 为唯一 `VALID-UNMAPPED`。

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

## 5. 当前验证状态

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

## 6. Phase 3 Curriculum Build 状态

固定原则：

> **初学者 0→1 的知识依赖决定课程主干；真人面经只校准复习权重、真实问法和追问深度。**

当前建设状态：

```text
MySQL ✅ 23 章 + Review + Interview
→ Redis ✅ 27 章 + Review + Interview
→ Vector DB ✅ 23 章 + Review + Interview
→ LLM Foundation ✅ 29 章 + Review + Interview
→ RAG ✅ 34 章 + Review + Interview
→ Agent Harness / Runtime ✅ 47 章 + Review + Interview
→ System Design 🚧 下一块
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。

Agent Harness 的正式课程输入已扩展为：

```text
44 HUMAN-A Agent Canonical
+ Verified Follow-up Chains
+ Claude Code / Codex pinned source snapshots
+ official Agent / Harness engineering articles
+ MCP / A2A specifications
+ primary papers
```

这些 Tier B/C 证据只用于课程完整性，**不改变 HUMAN-A Source Count**。

Agent 研究索引：`../agent-sources/`。
