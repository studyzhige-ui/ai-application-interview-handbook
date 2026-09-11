# AI Application Engineer 求职知识总地图

> 围绕 **AI 应用开发 / Agent 开发岗位**，从语言 → 服务 → 数据 → 模型基础 → 检索 → Agent Runtime → Production System 建立完整 0→1 能力链。
>
> 当前真人面经研究基线：`S001–S279` HUMAN-A（Frozen），**235 ACTIVE Canonical**。面经只校准市场频率、真实问法和追问深度，不反向限制完整知识体系。

## 1. 正式十板块

```text
01 Python
→ 02 FastAPI
→ 03 AI Backend Engineering
→ 04 MySQL
→ 05 Redis
→ 06 Vector DB
→ 07 LLM Foundation（应用工程深度）
→ 08 RAG
→ 09 Agent Harness / Runtime
→ 10 System Design
```

贯穿所有模块：Evaluation / Verification、Reliability / Failure Recovery、Security / Permission、Observability、AI-assisted Development、Cost / Latency / Scale。

---

# 2. 教材文件粒度规则

```text
Canonical Question = 可独立追问能力
Capability Primitive = 工程最小机制
教材文件 = 一个完整知识小板块 / 认知闭环
Section = 参数、变体、Failure、追问
```

章节数不追求统一。审计记录：[`curriculum-granularity-audit.md`](curriculum-granularity-audit.md)。
内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 均已通过。
Foundation 实际完成度：[`foundation-status-audit.md`](foundation-status-audit.md)。

---

# 3. Foundation

## Python ✅ — 13 blocks
入口：[`../python/README.md`](../python/README.md) — v1 已完成 current-standard Remediation；15 道 Python Canonical 已映射到 13 个 beginner-first 知识块，Review / Interview 同步完成。

## FastAPI ✅ — 16 blocks
入口：[`../fastapi/README.md`](../fastapi/README.md) — 已完成 `docs/01–16`、Review、Interview 与官方技术资料索引；4 道 FastAPI Canonical 已映射到 beginner-first Web/API 主干，Content Depth PASS。

## AI Backend Engineering ✅ — 22 blocks
入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 已完成 `docs/01–22`、Review、Interview 与权威工程资料索引；39 道 AIBE Canonical 已映射到 Python-first Backend Engineering 主干，Content Depth PASS。

**Foundation：✅ Python 13 + FastAPI 16 + AI Backend Engineering 22 全部完成。**

---

# 4. Data

## MySQL ✅ — 23 blocks
入口：[`../mysql/README.md`](../mysql/README.md)。

## Redis ✅ — 24 blocks
入口：[`../redis/README.md`](../redis/README.md)。已完成 **27 → 24** 的物理颗粒度整改。

## Vector Database ✅ — 16 blocks
入口：[`../vector-db/README.md`](../vector-db/README.md)。已完成 **23 → 16**。

---

# 5. Model Foundation

## LLM Foundation（应用工程深度） ✅ — 14 blocks
入口：[`../llm-foundation/README.md`](../llm-foundation/README.md)。已完成 **29 → 14**。

---

# 6. AI Application

## RAG ✅ — 14 blocks
入口：[`../rag/README.md`](../rag/README.md)。已完成 **34 → 14**。

正式子系统：

```text
RAG Role & Pipeline
→ Corpus Governance
→ Document Processing
→ Chunking Design
→ Advanced Chunk Structure
→ Query Planning
→ Retrieval Stack
→ Rerank & Candidate Budget
→ Evidence Delivery
→ Retrieval Evaluation
→ End-to-End Quality Engineering
→ Production Governance
→ Scale / Cost / Observability
→ GraphRAG / Agentic RAG
```

---

# 7. Agent Runtime

## Agent Harness / Runtime ✅ — 23 blocks

入口：[`../agent-harness/README.md`](../agent-harness/README.md)

旧 47 章已经物理迁移为 **23 个连续知识小板块**，并完成正文深度验收；旧碎片与 rewrite checkpoint 已清理。

证据体系：

```text
44 Agent HUMAN-A Canonical
+ Verified Follow-up Chains
+ Claude Code fixed source snapshot
+ OpenAI Codex fixed source snapshot
+ Anthropic / OpenAI official engineering materials
+ MCP / A2A official specifications
+ ReAct / SWE-bench primary papers
```

固定快照：

```text
Claude Code = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

主线：

```text
Agent / Workflow / Harness
→ Loop / Event / State
→ Tool Runtime
→ Planning / Stop / Budget
→ Context / Compaction
→ Memory / Session / Checkpoint
→ Permission / Sandbox / Injection
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping
```

课程坚持：**先 Runtime Problem，再 Runtime Primitive，再看成熟源码实现，最后映射 Framework。**

---

# 8. System Design ✅ — 19 blocks

入口：[`../system-design/README.md`](../system-design/README.md)。

24 道 System Design Canonical 全部为 L4，但教材没有一题一章，而是组织为：

```text
Part A：12 个通用设计能力
Requirement / SLO / Capacity / State / Flow
→ Cache / Partition / Consistency / Queue
→ Reliability / Multi-tenancy / Observability / Evaluation

Part B：7 类综合真人场景
High-concurrency Transactional
→ Realtime Read-heavy
→ Large-scale Data Processing
→ LLM Gateway / Multi-tenant AI Platform
→ Enterprise RAG
→ Production / Long-running Agent Backend
→ Vertical AI Agent Patterns
```

真人面经决定 Case、Failure、Scale 与 Verification 深度；通用知识依赖决定前 12 章主干。

---

# 9. Bridge Labs

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

---

# 10. Interview Reality

```text
HUMAN-A：S001–S279（Frozen）
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
```

> 面经决定“哪里高频、哪里追得深”，不决定“只学哪些知识”，也不决定“每一道题都独立成为一章”。

---

# 11. 当前 Phase 3 状态

**十板块第一版课程建设：✅ 完成。**


| 模块 | 当前状态 |
|---|---|
| Python | ✅ 13 blocks；Canonical Coverage / Depth PASS |
| FastAPI | ✅ 16 blocks；Canonical Coverage / Depth PASS |
| AI Backend Engineering | ✅ 22 blocks；Canonical Coverage / Depth PASS |
| MySQL | ✅ 23 blocks |
| Redis | ✅ 24 blocks |
| Vector DB | ✅ 16 blocks |
| LLM Foundation | ✅ 14 blocks |
| RAG | ✅ 14 blocks |
| Agent Harness / Runtime | ✅ 23 blocks；深度验收完成 |
| System Design | ✅ 19 blocks；Review / Interview 完成 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
