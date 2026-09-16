# Canonical Ownership & Curriculum Module Index

> **2026-09-16更新：** Agent为16章分层重构版，全仓库177篇正文。旧版深度与终局审计为历史记录；本次验证范围为结构、链接、迁移覆盖和证据不变性，详见既有质量记录。


[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Progress](progress.md)

> Canonical 数量描述面试能力粒度；Curriculum Blocks 描述教材认知闭环，两者不会机械相等。

> **v1.0 Final Quality Audit：✅ PASS。** 十板块跨模块 Ownership、术语边界与旧版184个 Curriculum Markdown 的历史结论见 [`../../roadmap/final-quality-audit.md`](../../roadmap/final-quality-audit.md)。

| # | Module | Canonical File | ACTIVE | Curriculum | Curriculum Entry | Status |
|---:|---|---|---:|---:|---|---|
| 01 | Python Foundation | [python.md](python.md) | 15 | 13 | [README](../../python/README.md) | ✅ |
| 02 | FastAPI | [fastapi.md](fastapi.md) | 4 | 16 | [README](../../fastapi/README.md) | ✅ |
| 03 | AI Backend Engineering | [ai-backend-engineering.md](ai-backend-engineering.md) | 39 | 22 | [README](../../backend-engineering/README.md) | ✅ |
| 04 | MySQL | [mysql.md](mysql.md) | 26 | 23 | [README](../../mysql/README.md) | ✅ |
| 05 | Redis | [redis.md](redis.md) | 19 | 24 | [README](../../redis/README.md) | ✅ |
| 06 | Vector Database | [vector-db.md](vector-db.md) | 12 | 16 | [README](../../vector-db/README.md) | ✅ |
| 07 | LLM Foundation（应用工程深度） | [llm-foundation.md](llm-foundation.md) | 23 | 14 | [README](../../llm-foundation/README.md) | ✅ |
| 08 | RAG | [rag.md](rag.md) | 29 | 14 | [README](../../rag/README.md) | ✅ |
| 09 | Agent | [agent-harness.md](agent-harness.md) | 44 | 16 | [README](../../agent/README.md) | ✅ |
| 10 | System Design | [system-design.md](system-design.md) | 24 | 19 | [README](../../system-design/README.md) | ✅ |

**ACTIVE total = 235. Legacy MOVED = 24.**

## 主要 Ownership 边界

- FastAPI async Runtime 本体 → Python；
- DB + Cache 一致性 / 通用 Rate Limit / Retry / MQ → AI Backend Engineering；
- Dense / Sparse / Hybrid / RRF / Rerank / Retrieval Eval → RAG；
- Embedding / Reranker 模型内部原理 → LLM Foundation；
- Agent Tool / Context / Memory / Checkpoint → Agent Harness；
- 端到端组合与 Scenario Trade-off → System Design。

## 研究事实不随教材重组改变

HUMAN-A、Source Count、Primary Ownership、Verified Follow-up Chain 与 Frequency Ranking 均保持 Frozen Research 层独立维护。
