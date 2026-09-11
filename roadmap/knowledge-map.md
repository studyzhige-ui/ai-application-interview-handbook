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

---

# 3. Foundation

## Python ✅
入口：[`../python/README.md`](../python/README.md) — 完整系统教材 + Review + Interview。

## FastAPI 🟡
入口：[`../fastapi/README.md`](../fastapi/README.md) — 完整课程骨架，正文后续补齐。

## AI Backend Engineering 🟡
入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 完整课程骨架，是贯穿后续模块的横向 Production 主线。

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

# 8. System Design ⏳

System Design 是第 10 个正式一级模块，也是当前下一阶段。

开始前直接应用已验证的教材粒度规则：

```text
先画知识依赖与系统子域
→ 确定知识小板块
→ 决定 Markdown 文件
→ 最后映射 24 道 System Design Canonical 与真实追问
```

禁止再从“一题一章”开始。

未来重点：企业知识库 RAG、大规模文档 RAG、多租户 AI Chat / Agent Platform、Coding Agent Backend、Long-running Agent Platform、Multi-Agent Workflow、AI Customer Service、Data / Analytical Agent。

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

| 模块 | 当前状态 |
|---|---|
| Python | ✅ 完整教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 23 blocks |
| Redis | ✅ 24 blocks |
| Vector DB | ✅ 16 blocks |
| LLM Foundation | ✅ 14 blocks |
| RAG | ✅ 14 blocks |
| Agent Harness / Runtime | ✅ 23 blocks；深度验收完成 |
| System Design | ⏳ 下一正式模块 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
