# Phase 2B Market Analysis Summary

更新日期：2026-09-11

> 本目录是冻结 `S001–S279` HUMAN-A 面经的统计与人工研究层。自动统计描述真实市场信号；人工层负责核验 Follow-up Chain 并把市场证据与完整课程路线对照。这里**不使用外部资料增加 HUMAN-A Source Count**。

## Baseline

- HUMAN-A：**279**
- ACTIVE Canonical：**235**
- 至少进入一个 Canonical 的来源：**278**
- `VALID-UNMAPPED`：**1**（`S271`）
- 三星高频题（>=10 sources）：**82**
- L4 Production / Failure / System Design Canonical：**116**

最终一致性校验见 [`source-coverage-validation.md`](source-coverage-validation.md)：`279/279` Frozen HUMAN-A、`235/235` ACTIVE、0 unexpected uncovered、0 Source Count mismatch。

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

## 自动统计层

- [`global-question-index.md`](global-question-index.md) / [`global-question-index.csv`](global-question-index.csv)：235 道 Canonical 全局索引。
- [`frequency-ranking.md`](frequency-ranking.md)：按独立 HUMAN-A Source Count 排名。
- [`market-coverage.md`](market-coverage.md)：公司、岗位、轮次与模块覆盖。
- [`depth-and-types.md`](depth-and-types.md)：L2/L3/L4 与 Question Type 分布。
- [`cooccurrence.md`](cooccurrence.md)：同一招聘流程中的 Canonical 共现；**无顺序信息**。
- [`curriculum-evidence-matrix.md`](curriculum-evidence-matrix.md)：Topic × Frequency × Max Depth 市场证据矩阵。
- [`module-metrics.csv`](module-metrics.csv)：模块级可复算指标。

## 人工核验层

- [`follow-up-chains.md`](follow-up-chains.md)：回到原始 Batch 后核验的真实递进链；不会把共现误写成固定追问顺序。
- [`knowledge-gap-analysis.md`](knowledge-gap-analysis.md)：市场证据 × `roadmap/knowledge-map.md` 的课程缺口分析。

已确认的高价值递进包括：

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

## Phase 2B 对课程的主要反哺

1. `LLM Foundation（应用工程深度）` 正式补为一级学习模块；
2. Vector DB 只保留 ANN / Index / Storage 基础设施，Dense/Sparse、Hybrid、RRF、Rerank Pipeline 统一归 RAG；
3. Agent Harness 显式加入 Prompt Injection、Intent Routing、A2A、Framework Selection、AI-assisted Development Workflow；
4. MySQL / Redis / RAG 章节必须覆盖 Failure / Scale / Evaluation，而不是只讲定义；
5. 教材重点统一采用：`Concept → Mechanism → Trade-off → Failure → Scale → Evaluation / Verification`。

## 下一阶段

**Phase 2B 已完成。** 下一阶段是 Phase 3：Curriculum Build / Remediation。

当前正式建设顺序：

```text
MySQL
→ Redis
→ Vector DB
→ LLM Foundation
→ RAG
→ Agent Harness / Runtime
→ System Design
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有课程骨架。下一块从 **MySQL 正式系统教材**开始。
