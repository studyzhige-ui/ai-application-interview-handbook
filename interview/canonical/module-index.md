# Canonical Ownership & Curriculum Module Index

[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [冻结覆盖](progress.md)

> Canonical 数量描述面试能力粒度；Curriculum Blocks 描述教材认知闭环，两者不会机械相等。

> 课程标题、数量与阅读顺序见[学习资源索引](../../guide/navigation-index.md)。本页只对应冻结能力归属与课程入口；目录编号不代表推荐学习顺序。

| 目录标识 | Module | Canonical File | ACTIVE | Curriculum Entry |
|---:|---|---|---:|---|
| 01 | Python Foundation | [python.md](python.md) | 15 | [README](../../curriculum/01-python/README.md) |
| 02 | FastAPI | [fastapi.md](fastapi.md) | 4 | [README](../../curriculum/02-fastapi/README.md) |
| 03 | AI Backend Engineering | [ai-backend-engineering.md](ai-backend-engineering.md) | 39 | [README](../../curriculum/03-backend-engineering/README.md) |
| 04 | MySQL | [mysql.md](mysql.md) | 26 | [README](../../curriculum/04-mysql/README.md) |
| 05 | Redis | [redis.md](redis.md) | 19 | [README](../../curriculum/05-redis/README.md) |
| 06 | Vector Database | [vector-db.md](vector-db.md) | 12 | [README](../../curriculum/06-vector-db/README.md) |
| 07 | LLM Foundation（应用工程深度） | [llm-foundation.md](llm-foundation.md) | 23 | [README](../../curriculum/07-llm-foundation/README.md) |
| 08 | RAG | [rag.md](rag.md) | 29 | [README](../../curriculum/08-rag/README.md) |
| 09 | Agent | [agent-harness.md](agent-harness.md) | 44 | [README](../../curriculum/09-agent/README.md) |
| 10 | System Design | [system-design.md](system-design.md) | 24 | [README](../../curriculum/10-system-design/README.md) |

**ACTIVE total = 235. Legacy MOVED = 24.**

## 主要 Ownership 边界

- FastAPI async Runtime 本体 → Python；
- DB + Cache 一致性 / 通用 Rate Limit / Retry / MQ → AI Backend Engineering；
- Dense / Sparse / Hybrid / RRF / Rerank / Retrieval Eval → RAG；
- Embedding / Reranker 模型内部原理 → LLM Foundation；
- Agent Tool / Context / Memory / Checkpoint → Agent；
- 端到端组合与 Scenario Trade-off → System Design。

## Frozen Canonical 事实不随教材重组改变

`S001–S279` 的 HUMAN-A Evidence、Source Count、Primary Ownership、Verified Follow-up Chain 与 Frequency Ranking 由 Frozen Canonical Evidence Layer 独立维护；Market 的 `S280+` 在 periodic review 前不改变这些统计。
