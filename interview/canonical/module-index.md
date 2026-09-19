# Canonical Ownership & Curriculum Module Index

[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Progress](progress.md)

> Canonical 数量描述面试能力粒度；Curriculum Blocks 描述教材认知闭环，两者不会机械相等。

> 旧184篇终审为历史记录；当前185篇中Agent24章的保留核对与实际检查见[修订记录](../../guide/project/agent-reader-revision.md)。研究兼容标识与题目频次保持不变。

| # | Module | Canonical File | ACTIVE | Curriculum | Curriculum Entry | Status |
|---:|---|---|---:|---:|---|---|
| 01 | Python Foundation | [python.md](python.md) | 15 | 13 | [README](../../curriculum/01-python/README.md) | ✅ |
| 02 | FastAPI | [fastapi.md](fastapi.md) | 4 | 16 | [README](../../curriculum/02-fastapi/README.md) | ✅ |
| 03 | AI Backend Engineering | [ai-backend-engineering.md](ai-backend-engineering.md) | 39 | 22 | [README](../../curriculum/03-backend-engineering/README.md) | ✅ |
| 04 | MySQL | [mysql.md](mysql.md) | 26 | 23 | [README](../../curriculum/04-mysql/README.md) | ✅ |
| 05 | Redis | [redis.md](redis.md) | 19 | 24 | [README](../../curriculum/05-redis/README.md) | ✅ |
| 06 | Vector Database | [vector-db.md](vector-db.md) | 12 | 16 | [README](../../curriculum/06-vector-db/README.md) | ✅ |
| 07 | LLM Foundation（应用工程深度） | [llm-foundation.md](llm-foundation.md) | 23 | 14 | [README](../../curriculum/07-llm-foundation/README.md) | ✅ |
| 08 | RAG | [rag.md](rag.md) | 29 | 14 | [README](../../curriculum/08-rag/README.md) | ✅ |
| 09 | Agent | [agent-harness.md](agent-harness.md) | 44 | 24 | [README](../../curriculum/09-agent/README.md) | ✅ |
| 10 | System Design | [system-design.md](system-design.md) | 24 | 19 | [README](../../curriculum/10-system-design/README.md) | ✅ |

**ACTIVE total = 235. Legacy MOVED = 24.**

## 主要 Ownership 边界

- FastAPI async Runtime 本体 → Python；
- DB + Cache 一致性 / 通用 Rate Limit / Retry / MQ → AI Backend Engineering；
- Dense / Sparse / Hybrid / RRF / Rerank / Retrieval Eval → RAG；
- Embedding / Reranker 模型内部原理 → LLM Foundation；
- Agent Tool / Context / Memory / Checkpoint → Agent；
- 端到端组合与 Scenario Trade-off → System Design。

## 研究事实不随教材重组改变

HUMAN-A、Source Count、Primary Ownership、Verified Follow-up Chain 与 Frequency Ranking 均保持 Frozen Research 层独立维护。
