# Phase 2B Market Analysis Summary

更新日期：2026-09-11

> 自动统计层。这里不做课程知识补全，只描述冻结真人面经数据本身。

## Baseline

- HUMAN-A：**279**
- ACTIVE Canonical：**235**
- 至少进入一个 Canonical 的来源：**278**
- 三星高频题（>=10 sources）：**82**
- L4 Production / Failure / System Design Canonical：**116**

## Top 20 真人面试信号

| Rank | QID | Module | Sources | Topic |
|---:|---|---|---:|---|
| 1 | `AGENT-009` | Agent Harness / Runtime | 41 | Context Compaction |
| 2 | `RAG-002` | RAG | 38 | End-to-end Pipeline |
| 3 | `AGENT-048` | Agent Harness / Runtime | 37 | AI-assisted Development Workflow |
| 4 | `AGENT-003` | Agent Harness / Runtime | 36 | Agent Loop |
| 5 | `AGENT-014` | Agent Harness / Runtime | 36 | Memory Architecture |
| 6 | `AGENT-024` | Agent Harness / Runtime | 34 | Capability Abstraction Boundary |
| 7 | `AGENT-005` | Agent Harness / Runtime | 31 | Agent Paradigm |
| 8 | `LLM-023` | LLM Foundation（应用工程深度） | 30 | Prompt Engineering |
| 9 | `RAG-007` | RAG | 30 | Chunk Strategy |
| 10 | `AGENT-001` | Agent Harness / Runtime | 30 | Agent Boundary |
| 11 | `AGENT-018` | Agent Harness / Runtime | 29 | Tool Calling Protocol |
| 12 | `AGENT-030` | Agent Harness / Runtime | 29 | Multi-Agent Architecture |
| 13 | `AGENT-020` | Agent Harness / Runtime | 27 | Tool Call Failure Semantics |
| 14 | `AGENT-034` | Agent Harness / Runtime | 27 | Agent Evaluation |
| 15 | `AGENT-047` | Agent Harness / Runtime | 27 | Agent Framework Selection |
| 16 | `REDIS-012` | Redis | 25 | Distributed Lock Basics |
| 17 | `RAG-013` | RAG | 25 | Hybrid Retrieval |
| 18 | `AGENT-002` | Agent Harness / Runtime | 25 | Harness / Runtime Boundary |
| 19 | `AGENT-036` | Agent Harness / Runtime | 24 | Code Verification |
| 20 | `RAG-015` | RAG | 22 | Reranking |

## Module evidence footprint

| Module | Canonical | Unique Sources | Source×Question Incidences | >=10 Qs | L4 Qs |
|---|---:|---:|---:|---:|---:|
| Python | 15 | 15 | 25 | 0 | 0 |
| FastAPI | 4 | 3 | 4 | 0 | 1 |
| AI Backend Engineering | 39 | 125 | 299 | 12 | 16 |
| MySQL | 26 | 55 | 138 | 6 | 6 |
| Redis | 19 | 69 | 164 | 7 | 8 |
| Vector DB | 12 | 37 | 94 | 4 | 5 |
| LLM Foundation（应用工程深度） | 23 | 82 | 138 | 4 | 1 |
| RAG | 29 | 88 | 374 | 16 | 20 |
| Agent Harness / Runtime | 44 | 166 | 741 | 30 | 35 |
| System Design | 24 | 71 | 81 | 3 | 24 |

Phase 2B 自动统计与人工核验层均已完成。Phase 3 教材建设的实时状态以 `research/questions/progress.md` 与 `roadmap/knowledge-map.md` 为准；本自动生成文件不重复维护易过期的“下一模块”状态。
