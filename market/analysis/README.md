# Market Analysis｜Frozen Canonical Baseline

[← Market 首页](../README.md) · [↑ Handbook 总目录](../../README.md) · [Canonical Questions →](../../interview/canonical/README.md)

> **数据范围：Frozen Canonical Baseline。** 本页只统计 `S001–S279 / 235 ACTIVE Canonical`；Market 的持续监测总量与 `S280+` 状态以 `market/README.md` 为准。

统计快照日期：2026-09-11

## Frozen Baseline

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

当前 Curriculum 状态以 `interview/canonical/progress.md` 与 `guide/knowledge-map.md` 为准；当前 Gap 见 `market/analysis/knowledge-gap-analysis.md`，Phase 2B 历史 Gap 见 `market/analysis/history/`。本自动生成 README 不重复维护易过期的 Market 总量或课程下一步。
