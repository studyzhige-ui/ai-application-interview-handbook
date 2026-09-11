# AI Application Engineer 求职知识总地图

> 围绕 **AI 应用开发 / Agent 开发岗位**，从语言 → 服务 → 数据 → 模型基础 → 检索 → Agent Runtime → Production System 建立完整 0→1 能力链。
>
> 当前真人面经研究基线：`S001–S279` HUMAN-A（Frozen），**235 ACTIVE Canonical**。面经只校准市场频率、真实问法和追问深度，不反向限制完整知识体系。

## 1. 正式十板块

```text
01 Python
        ↓
02 FastAPI
        ↓
03 AI Backend Engineering
        ↓
04 MySQL
        ↓
05 Redis
        ↓
06 Vector DB
        ↓
07 LLM Foundation（应用工程深度）
        ↓
08 RAG
        ↓
09 Agent Harness / Runtime
        ↓
10 System Design
```

贯穿所有模块：Evaluation / Verification、Reliability / Failure Recovery、Security / Permission、Observability、AI-assisted Development、Cost / Latency / Scale。

---

# 2. Foundation

## Python ✅
入口：[`../python/README.md`](../python/README.md) — 完整系统教材 + Review + Interview。

## FastAPI 🟡
入口：[`../fastapi/README.md`](../fastapi/README.md) — 完整课程骨架，正文后续补齐。

## AI Backend Engineering 🟡
入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 完整课程骨架，是贯穿后续模块的横向主线。

---

# 3. Data

## MySQL ✅
入口：[`../mysql/README.md`](../mysql/README.md) — **23 章 + Review + Interview**。

## Redis ✅
入口：[`../redis/README.md`](../redis/README.md) — **27 章 + Review + Interview**。

## Vector Database ✅
入口：[`../vector-db/README.md`](../vector-db/README.md) — **23 章 + Review + Interview**。

Primary Boundary：Vector DB 负责向量基础设施；Dense/Sparse、Hybrid、RRF、Rerank、Retrieval Evaluation 归 RAG。

---

# 4. Model Foundation

## LLM Foundation（应用工程深度） ✅
入口：[`../llm-foundation/README.md`](../llm-foundation/README.md) — **29 章 + Review + Interview**。

```text
Token / Context
→ Transformer / Attention / RoPE
→ Generation / Sampling
→ KV Cache / Serving / Cost
→ Model API / Selection
→ Embedding / Reranker / Multimodal
→ Prompt / Hallucination
→ Fine-tuning / Alignment Boundary
```

---

# 5. AI Application

## RAG ✅
入口：[`../rag/README.md`](../rag/README.md) — **34 章 + Review + Interview**。

```text
Corpus / Lineage / Parse / Clean
→ Chunk
→ Query Transformation
→ Dense / Sparse / Hybrid / RRF / Rerank
→ Context / Grounding / Citation
→ Evaluation / Regression / Bad Case
→ Freshness / Permission / Scale
→ GraphRAG / Agentic RAG
```

---

# 6. Agent Runtime

## Agent Harness / Runtime ✅

入口：[`../agent-harness/README.md`](../agent-harness/README.md)

第一版完整：**47 章 + Review + Interview**。

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

证据入口：[`../research/agent-sources/README.md`](../research/agent-sources/README.md)

固定实现快照：

```text
Claude Code commit = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

正式 0→1 主线：

```text
Agent vs Workflow
→ Harness / Runtime Boundary
→ Loop / Run / Turn / Step / Event
→ Tool Contract / Validation / Routing / Execution / Failure
→ Planning / Stop / Budget
→ Context Assembly / Budget / Tool-result Offloading
→ Compaction / Correctness
→ Memory / Session / State / Persistence
→ Checkpoint / Resume / Fork / Cancellation
→ Idempotency / Side Effect / Compensation
→ Permission / Approval / Sandbox / Guardrails
→ Prompt Injection / Secret Containment
→ Tool Discovery / MCP / Skills / Hooks
→ Intent / Model Routing
→ Multi-Agent / Handoff / A2A / Workspace Concurrency
→ Trace / Replay / Evaluation
→ Coding Agent Workflow / Verification
→ Production Architecture
→ Framework Mapping / Build-vs-Buy
```

课程明确坚持：

> **先 Runtime Problem，再 Runtime Primitive，再看成熟源码实现，最后才映射 Framework。**

因此 LangGraph / LangChain / OpenAI Agents SDK 不作为课程起点。

---

# 7. System Design 🚧 下一块正式系统教材

前面所有模块最终在这里汇合。

典型系统：

- 企业知识库 RAG；
- 大规模文档 RAG；
- 多租户 AI Chat / Agent Platform；
- Coding Agent Backend；
- Long-running Agent Platform；
- Multi-Agent Workflow；
- AI Customer Service；
- Data / Analytical Agent。

```text
Client
  ↓
FastAPI / API
  ↓
Agent Harness
├─ Tools
├─ RAG → Vector DB
└─ Memory / State → Redis / Durable Store

Business / History Data → MySQL

横向：Timeout / Retry / Idempotency / MQ
      Trace / Metrics / Security / Scaling / Cost
```

System Design 的目标不是再重复前面模块，而是学习：需求澄清、容量估算、组件边界、数据流、failure domain、一致性、SLO、权限、多租户、扩容、降级、成本与验证。

---

# 8. Bridge Labs

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

---

# 9. Interview Reality

研究入口：[`../research/README.md`](../research/README.md)

```text
HUMAN-A：S001–S279（Frozen）
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
```

> 面经决定“哪里高频、哪里追得深”，不决定“只学哪些知识”。

---

# 10. 当前 Phase 3 状态

| 模块 | 当前状态 |
|---|---|
| Python | ✅ 完整教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 23 章 + Review + Interview |
| Redis | ✅ 27 章 + Review + Interview |
| Vector DB | ✅ 23 章 + Review + Interview |
| LLM Foundation | ✅ 29 章 + Review + Interview |
| RAG | ✅ 34 章 + Review + Interview |
| Agent Harness / Runtime | ✅ 47 章 + Review + Interview |
| System Design | 🚧 **下一块正式系统教材** |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |

下一正式模块：**System Design**。
