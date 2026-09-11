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

> **Canonical 数量不等于教材章节数。** Canonical 是可独立追问能力；教材文件按完整知识小板块组织。

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
| `LLM-023` | LLM Foundation | Prompt Engineering | 30 |
| `AGENT-044` | Agent Harness | Prompt Injection / Untrusted Context Security | 8 |
| `AGENT-045` | Agent Harness | Intent Recognition / Routing | 11 |
| `AGENT-046` | Agent Harness | A2A / Agent Communication Protocol | 6 |
| `AGENT-047` | Agent Harness | Agent Framework Selection | 27 |
| `AGENT-048` | Agent Harness | AI-assisted Development Workflow | 37 |

`S271` 为唯一 `VALID-UNMAPPED`。

---

## 4. Phase 2B 验证状态

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

## 5. Phase 3 Curriculum Build

固定原则：

> **初学者 0→1 的知识依赖决定课程主干；真人面经只校准复习权重、真实问法和追问深度。研究 / Capability / 教材文件使用不同粒度。**

当前教材结构：

```text
MySQL ✅ 23 blocks；Granularity PASS
Redis ✅ 24 blocks；27→24 COMPLETE
Vector DB ✅ 16 blocks；23→16 COMPLETE
LLM Foundation ✅ 14 blocks；29→14 COMPLETE
RAG ✅ 14 blocks；34→14 COMPLETE
Agent Harness / Runtime 🚧 23 blocks；47→23 STRUCTURE COMPLETE，深度验收中
System Design ⏸️ Agent 深度验收后启动
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。

### 为什么教材文件数小于 Canonical 数量

例如：

```text
Agent Canonical = 44
Agent 教材 = 23 blocks

RAG Canonical = 29
RAG 教材 = 14 blocks
```

因为多个可独立追问能力可能属于同一个认知闭环。教材章节不应机械跟随题目数量。

### Agent Harness 的证据输入

```text
44 HUMAN-A Agent Canonical
+ Verified Follow-up Chains
+ Claude Code / Codex pinned source snapshots
+ official Agent / Harness engineering articles
+ MCP / A2A specifications
+ primary papers
```

Tier B/C 证据只用于课程完整性，**不改变 HUMAN-A Source Count**。
