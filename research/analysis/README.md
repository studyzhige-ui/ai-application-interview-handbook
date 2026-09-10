# Phase 2B Market Analysis Summary

更新日期：2026-09-11

> 自动统计层。这里不做课程知识补全，只描述冻结真人面经数据本身。

## Baseline

- HUMAN-A：**279**
- ACTIVE Canonical：**229**
- 至少进入一个 Canonical 的来源：**251**
- 三星高频题（>=10 sources）：**67**
- L4 Production / Failure / System Design Canonical：**113**

## Top 20 真人面试信号

| Rank | QID | Module | Sources | Topic |
|---:|---|---|---:|---|
| 1 | `AGENT-009` | Agent Harness / Runtime | 33 | Context Compaction |
| 2 | `RAG-002` | RAG | 31 | End-to-end Pipeline |
| 3 | `AGENT-014` | Agent Harness / Runtime | 31 | Memory Architecture |
| 4 | `RAG-007` | RAG | 29 | Chunk Strategy |
| 5 | `AGENT-018` | Agent Harness / Runtime | 28 | Tool Calling Protocol |
| 6 | `AGENT-024` | Agent Harness / Runtime | 27 | Capability Abstraction Boundary |
| 7 | `REDIS-012` | Redis | 25 | Distributed Lock Basics |
| 8 | `AGENT-001` | Agent Harness / Runtime | 25 | Agent Boundary |
| 9 | `RAG-013` | RAG | 24 | Hybrid Retrieval |
| 10 | `AGENT-003` | Agent Harness / Runtime | 24 | Agent Loop |
| 11 | `RAG-015` | RAG | 22 | Reranking |
| 12 | `AGENT-020` | Agent Harness / Runtime | 22 | Tool Call Failure Semantics |
| 13 | `RAG-021` | RAG | 21 | RAG Evaluation |
| 14 | `AGENT-030` | Agent Harness / Runtime | 21 | Multi-Agent Architecture |
| 15 | `AIBE-020` | AI Backend Engineering | 20 | Data Consistency / Cache Architecture |
| 16 | `REDIS-007` | Redis | 20 | Cache Failure Patterns |
| 17 | `AGENT-034` | Agent Harness / Runtime | 19 | Agent Evaluation |
| 18 | `VDB-009` | Vector DB | 18 | Vector Storage / Product / Architecture Selection |
| 19 | `RAG-019` | RAG | 18 | Bad Case Attribution |
| 20 | `AGENT-005` | Agent Harness / Runtime | 18 | Agent Paradigm |

## Module evidence footprint

| Module | Canonical | Unique Sources | Source×Question Incidences | >=10 Qs | L4 Qs |
|---|---:|---:|---:|---:|---:|
| Python | 15 | 15 | 25 | 0 | 0 |
| FastAPI | 4 | 3 | 4 | 0 | 1 |
| AI Backend Engineering | 39 | 120 | 290 | 11 | 16 |
| MySQL | 26 | 55 | 138 | 6 | 6 |
| Redis | 19 | 68 | 163 | 7 | 8 |
| Vector DB | 12 | 34 | 91 | 4 | 5 |
| LLM Foundation（应用工程深度） | 22 | 57 | 99 | 1 | 1 |
| RAG | 29 | 78 | 357 | 15 | 20 |
| Agent Harness / Runtime | 39 | 104 | 521 | 21 | 32 |
| System Design | 24 | 66 | 76 | 2 | 24 |

下一步人工研究层：基于 `cooccurrence.md` 回到原始 Batch 核验真正的 Follow-up Chain，并将 `curriculum-evidence-matrix.md` 与最新 `roadmap/knowledge-map.md` 对照，形成 Knowledge Gap Analysis。
