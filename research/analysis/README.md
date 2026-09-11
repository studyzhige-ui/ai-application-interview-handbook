# Phase 2B Market Analysis Summary

更新日期：2026-09-11

> 本目录是冻结 `S001–S279` HUMAN-A 面经的统计与人工研究层。统计结果只描述真实市场信号；完整课程知识体系仍由各模块的 0→1 认知依赖决定。外部资料和教材建设不会反向增加 HUMAN-A Source Count。

## Baseline

- HUMAN-A：**279**
- ACTIVE Canonical：**235**
- 至少进入一个 Canonical 的来源：**278**
- `VALID-UNMAPPED`：**1（S271）**
- 三星高频题（>=10 sources）：**82**
- L4 Production / Failure / System Design Canonical：**116**

最终一致性校验见 [`source-coverage-validation.md`](source-coverage-validation.md)。

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

## 已完成研究产物

自动统计层：

- [`global-question-index.md`](global-question-index.md) / [`global-question-index.csv`](global-question-index.csv)
- [`frequency-ranking.md`](frequency-ranking.md)
- [`market-coverage.md`](market-coverage.md)
- [`depth-and-types.md`](depth-and-types.md)
- [`cooccurrence.md`](cooccurrence.md)
- [`curriculum-evidence-matrix.md`](curriculum-evidence-matrix.md)
- [`module-metrics.csv`](module-metrics.csv)
- [`source-coverage-validation.md`](source-coverage-validation.md)

人工核验层：

- [`follow-up-chains.md`](follow-up-chains.md)：真实追问递进，不把同场共现误写成固定顺序。
- [`knowledge-gap-analysis.md`](knowledge-gap-analysis.md)：市场证据 × 最新课程地图。

高价值递进包括：

```text
RAG Pipeline
→ Chunk
→ Hybrid Retrieval
→ Rerank
→ Evaluation / Bad Case

Agent Boundary / Harness
→ Loop
→ Tool / Skill
→ Context / Memory
→ Failure / Resume
→ Evaluation

Context Assembly
→ Compaction
→ Correctness
→ Memory Pollution
→ Resume

AI Coding
→ Requirement / Context
→ Repo Understanding / Modification
→ Test / Review
→ Verification / Delivery
```

---

## Phase 3：Curriculum Build / Remediation

固定原则：

> **知识体系与初学者 0→1 的认知依赖决定教材主干；面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度，不能按频率重排教材。**

当前建设状态：

| 模块 | 状态 |
|---|---|
| MySQL | ✅ 第一版完成：23 章 + Review + Interview |
| Redis | ✅ 第一版完成：27 章 + Review + Interview |
| Vector DB | ✅ 第一版完成：23 章 + Review + Interview |
| LLM Foundation | 🚧 当前正在建设 |
| RAG | ⏳ LLM Foundation 后建设 |
| Agent Harness / Runtime | ⏳ RAG 后建设；额外研究 Claude Code / Codex |
| System Design | ⏳ 最后汇总 |

```text
MySQL ✅
→ Redis ✅
→ Vector DB ✅
→ LLM Foundation 🚧
→ RAG
→ Agent Harness / Runtime
→ System Design
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架，后续通过正文和 Bridge Labs 继续补齐。

### 模块收尾同步规则

每完成一个一级模块，必须同步检查：

1. 模块自身 `README.md`；
2. 根 `README.md`；
3. `roadmap/knowledge-map.md`；
4. `research/questions/progress.md`；
5. 本文件；
6. 所有仍写着“下一块 / 待建设”的关联入口；
7. `docs / review / interview` 的数量、链接与连续编号。
