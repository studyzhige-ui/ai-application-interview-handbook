# Phase 2B Source Coverage Audit

更新日期：2026-09-11

> 本文件记录首次自动校验发现的 28 个零映射 HUMAN-A 来源如何处理。原则：优先补已有 Canonical 的 Evidence；只有出现独立知识模型才新增 Canonical；确无十板块可归一化技术题的来源允许显式 `VALID-UNMAPPED`，绝不为追求 279/279 强行造题。

## 补漏结果

- 重新映射来源：**27**
- VALID-UNMAPPED：**1**
- 本轮新增 Canonical：**6**
- 审计后预期 ACTIVE：**235**

## 新增 Canonical

| QID | Module | Topic | HUMAN-A Sources |
|---|---|---|---:|
| `LLM-023` | LLM Foundation（应用工程深度） | Prompt Engineering | 30 |
| `AGENT-044` | Agent Harness / Runtime | Prompt Injection / Untrusted Context Security | 8 |
| `AGENT-045` | Agent Harness / Runtime | Intent Recognition / Routing | 11 |
| `AGENT-046` | Agent Harness / Runtime | A2A / Agent Communication Protocol | 6 |
| `AGENT-047` | Agent Harness / Runtime | Agent Framework Selection | 24 |
| `AGENT-048` | Agent Harness / Runtime | AI-assisted Development Workflow | 36 |

## 原零映射来源处理

| Source | Decision | QIDs |
|---|---|---|
| `S076` | MAPPED | `RAG-002`, `AGENT-002`, `AGENT-043`, `AGENT-022`, `AGENT-009`, `AGENT-010` |
| `S077` | MAPPED | `AGENT-021`, `AGENT-034`, `AGENT-035`, `AGENT-003`, `AGENT-036`, `AGENT-019`, `AGENT-024`, `AGENT-020`, `AGENT-028`, `AGENT-030`, `AGENT-047`, `AGENT-048` |
| `S078` | MAPPED | `AGENT-017`, `AGENT-034`, `AGENT-035`, `AGENT-003`, `AGENT-005`, `AGENT-002`, `AGENT-047` |
| `S082` | MAPPED | `AGENT-043`, `AGENT-041`, `AGENT-002`, `SD-021` |
| `S085` | MAPPED | `AGENT-001`, `AGENT-002`, `AGENT-018`, `AGENT-014`, `LLM-022`, `AGENT-005`, `AGENT-006`, `AGENT-028`, `AGENT-020`, `SD-021`, `AGENT-030` |
| `S099` | MAPPED | `LLM-023`, `AGENT-005`, `RAG-002`, `LLM-010` |
| `S103` | MAPPED | `RAG-002`, `AGENT-002`, `AGENT-041`, `LLM-022`, `AGENT-023`, `AGENT-044`, `AGENT-028`, `AGENT-005`, `AGENT-020`, `AGENT-030`, `AGENT-036`, `AGENT-048` |
| `S113` | MAPPED | `AIBE-018`, `RAG-002`, `RAG-010`, `VDB-009`, `AGENT-048` |
| `S121` | MAPPED | `AGENT-003`, `AGENT-034`, `AGENT-005`, `VDB-009`, `AGENT-022`, `AGENT-017`, `AGENT-038`, `AGENT-009`, `AGENT-047` |
| `S128` | MAPPED | `AGENT-036`, `AGENT-024`, `AGENT-048` |
| `S141` | MAPPED | `AGENT-003`, `RAG-001`, `LLM-018`, `RAG-007`, `RAG-009`, `AGENT-005`, `LLM-020`, `LLM-006` |
| `S142` | MAPPED | `RAG-002`, `AIBE-011`, `SD-002`, `AGENT-048` |
| `S143` | MAPPED | `AGENT-003`, `AGENT-034`, `AGENT-007`, `AGENT-002`, `AGENT-014`, `AGENT-009`, `AGENT-048` |
| `S153` | MAPPED | `AGENT-030`, `AGENT-005`, `RAG-002`, `RAG-016`, `AGENT-020`, `AGENT-008`, `RAG-020`, `RAG-027` |
| `S155` | MAPPED | `AGENT-025`, `AGENT-021`, `AGENT-008`, `AGENT-009`, `AGENT-005`, `AGENT-030`, `AGENT-002`, `AGENT-047` |
| `S157` | MAPPED | `AGENT-003`, `AGENT-030`, `AGENT-031`, `RAG-013`, `RAG-019`, `AGENT-022`, `AGENT-023`, `AGENT-020`, `AGENT-008`, `AGENT-036`, `AGENT-048` |
| `S160` | MAPPED | `AGENT-003`, `AGENT-002`, `AGENT-034`, `AIBE-037`, `AIBE-039` |
| `S186` | MAPPED | `AGENT-001`, `AGENT-005`, `AGENT-003`, `AGENT-038`, `AGENT-024`, `AGENT-034`, `AGENT-036`, `AGENT-002`, `AGENT-047`, `AGENT-048` |
| `S190` | MAPPED | `AGENT-001`, `AGENT-002`, `AGENT-003`, `AGENT-030`, `AIBE-013`, `AGENT-014`, `AGENT-005`, `AGENT-009`, `REDIS-002`, `AIBE-034` |
| `S196` | MAPPED | `LLM-022`, `AGENT-028`, `AGENT-024`, `AGENT-005`, `AGENT-036`, `AGENT-048` |
| `S197` | MAPPED | `AGENT-005`, `AGENT-030`, `LLM-021`, `AGENT-001`, `AGENT-024`, `AGENT-009`, `AGENT-014`, `AGENT-003` |
| `S213` | MAPPED | `AGENT-003`, `AGENT-034`, `AGENT-035`, `RAG-004`, `AGENT-019`, `AGENT-021`, `AGENT-026`, `AGENT-002` |
| `S215` | MAPPED | `AGENT-036`, `AGENT-048` |
| `S219` | MAPPED | `AGENT-009`, `AGENT-008`, `AGENT-014`, `AGENT-005`, `AGENT-041`, `AGENT-024` |
| `S221` | MAPPED | `AIBE-027`, `AIBE-029`, `AIBE-038`, `RAG-002`, `AGENT-003`, `AGENT-036`, `VDB-020`, `SD-021`, `LLM-017`, `AGENT-009`, `AGENT-010`, `AGENT-034`, `AGENT-047`, `AGENT-048`, `LLM-023` |
| `S239` | MAPPED | `AGENT-038`, `SD-021`, `AGENT-002`, `AGENT-001` |
| `S261` | MAPPED | `AGENT-024`, `AGENT-036`, `AGENT-048` |
| `S271` | VALID-UNMAPPED | 该 HUMAN-A 流程被招聘方明确纳入 Agent 工程师大池，但本轮可核验技术题全部是 React Hook、JavaScript 类型与版本号 Coding；没有可安全归入当前十板块 Canonical 的 AI / Backend 技术问题。保留来源覆盖信号，但不为追求 279/279 强行造题。 |

## 关键补漏解释

这轮不是为了把覆盖率做成 100% 而机械挂 Evidence。全语料候选扫描暴露出 Phase 1 真正遗漏的独立能力：Prompt Engineering、Prompt Injection / Untrusted Context Security、Intent Recognition / Routing、A2A、Agent Framework Selection、AI-assisted Development Workflow。它们均由 HUMAN-A 原始技术问题支持，因此正式新增 Canonical。

`S271` 保留为 VALID-UNMAPPED：招聘流程明确属于 Agent 工程师大池，但当前可核验技术题是 React Hook / JavaScript / 版本号 Coding，不能安全归入现有十板块的 AI / Backend Canonical。
