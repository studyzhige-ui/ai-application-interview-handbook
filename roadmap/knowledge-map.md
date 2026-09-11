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

贯穿所有模块的横向能力：

```text
Evaluation / Verification
Reliability / Failure Recovery
Security / Permission
Observability
AI-assisted Development
Cost / Latency / Scale
```

---

# 2. Foundation

## Python ✅

入口：[`../python/README.md`](../python/README.md)

```text
对象模型 / 容器
→ 引用 / 可变性 / 拷贝
→ 函数 / 闭包
→ Iterator / Generator
→ Decorator / Context Manager
→ OOP / Exception / Import
→ GC / GIL
→ Thread / Process / Coroutine
→ asyncio
```

当前已有完整系统教材 + Review + Interview。

## FastAPI 🟡

入口：[`../fastapi/README.md`](../fastapi/README.md)

```text
HTTP
→ ASGI / Uvicorn
→ Routing / Pydantic
→ Dependency / Lifespan
→ async def / Event Loop
→ Streaming / SSE / WebSocket
→ Auth
→ DB / Redis / Provider
→ Timeout / Cancellation
→ Testing / Trace / Deployment
→ RAG / Agent API
```

当前：完整课程骨架，正文后续补齐。

## AI Backend Engineering 🟡

入口：[`../backend-engineering/README.md`](../backend-engineering/README.md)

```text
Network / HTTP
→ Concurrency / Connection Pool
→ Timeout / Retry / Circuit Breaker
→ Cancellation / Idempotency
→ Lock / Lease
→ MQ / Reliable Task / Backpressure
→ Cache / Rate Limit / Data Consistency
→ Large File Pipeline
→ Observability / Security
→ Deployment / Scaling
```

它是一条贯穿后续所有模块的横向主线。

---

# 3. Data

## MySQL ✅

入口：[`../mysql/README.md`](../mysql/README.md)

第一版完整：**23 章 + Review + Interview**。

```text
SQL / Execution
→ Index / B+Tree
→ Clustered / Secondary
→ Composite / Covering / ICP / Optimizer / EXPLAIN
→ ACID / Isolation / MVCC / Lock
→ redo / undo / binlog
→ Pagination / Schema
→ Replication / Sharding / CDC
→ Bulk Write
→ AI Application Data Modeling
→ MySQL + Redis Consistency Boundary
```

课程顺序以数据库知识依赖为主，Sharding / Cache Consistency 即使高频也不会提前到 Index / Transaction 之前。

## Redis ✅

入口：[`../redis/README.md`](../redis/README.md)

第一版完整：**27 章 + Review + Interview**。

```text
Role / Keyspace / Command
→ Core + Specialized Data Structures
→ Internal Encoding / Memory
→ Thread Model / Event Loop / I/O Multiplexing
→ TTL / Eviction
→ Cache Failure / BigKey / HotKey
→ RDB / AOF
→ Replication / Sentinel / Cluster
→ MULTI / WATCH / Pipeline / Lua
→ Distributed Lock / Lease / Fencing
→ Pub/Sub / Streams
→ Multi-level / Semantic Cache
→ Session / Conversation / Agent State Store
→ Rate Limit / Security / Troubleshooting
```

## Vector Database ✅

入口：[`../vector-db/README.md`](../vector-db/README.md)

第一版完整：**23 章 + Review + Interview**。

```text
Vector / Dimension / Normalization
→ Cosine / Dot / L2
→ Exact Search → ANN
→ HNSW / IVF / Quantization
→ Index Selection
→ Collection / Schema / Metadata
→ Filter / Tenant Isolation
→ Update / Delete / Compaction
→ Re-embedding / Rebuild / Version
→ Shard / Replica
→ Capacity / Troubleshooting
→ Product Selection / Graph DB Boundary
```

Primary Boundary：Vector DB 负责向量基础设施；Dense/Sparse、Hybrid、RRF、Rerank、Retrieval Evaluation 归 RAG。

---

# 4. Model Foundation

## LLM Foundation（应用工程深度） ✅

入口：[`../llm-foundation/README.md`](../llm-foundation/README.md)

第一版完整：**29 章 + Review + Interview**。

```text
Token / Tokenization
→ Context Window / Long Context
→ Transformer
→ QKV / Attention / Multi-Head / Causal Mask
→ FFN / Residual / Norm / RoPE
→ Autoregressive Generation / Sampling
→ KV Cache
→ Prefill / Decode
→ Continuous Batching / PagedAttention
→ TTFT / TPOT / Throughput / Cost
→ Precision / Quantization
→ Model API / Provider Adapter
→ Model Selection
→ Embedding / Reranker / Multimodal
→ Prompt Engineering
→ Hallucination / Factuality
→ Prompt vs RAG vs Fine-tuning
→ SFT / LoRA / Preference Optimization / Distillation
```

目标是解释模型行为与推理系统，不扩成训练 Infra 大全。

---

# 5. AI Application

## RAG ✅

入口：[`../rag/README.md`](../rag/README.md)

第一版完整：**34 章 + Review + Interview**。

```text
RAG Boundary
→ Corpus Audit / Source of Truth
→ Document Identity / Lineage / Version
→ Parse / OCR / Layout / Multimodal
→ Cleaning / Dedup
→ Chunk Principles / Strategy / Size / Overlap
→ Parent-child / Semantic Boundary / Chunk Data Model
→ Retrieval Request Lifecycle
→ Rewrite / Clarification / Decomposition / Multi-query / HyDE
→ No-hit / Refusal
→ Dense + Sparse / BM25
→ Hybrid / RRF
→ Rerank / Top-K / Candidate Budget
→ Context Construction
→ Grounding / Citation
→ Retrieval Metrics
→ Eval Dataset / LLM Judge
→ End-to-end Evaluation
→ Baseline / Ablation / Regression
→ Bad Case Attribution
→ Freshness / Version / Snapshot / Rollback
→ Permission / Tenant
→ Large-scale Ingestion / Cost / Cache / Observability
→ GraphRAG / Agentic RAG
```

真实追问已经稳定深入到 Evaluation / Failure Attribution / Production Governance，因此 Evaluation 是主干，不是附录。

RAG 与前置边界：

```text
LLM Foundation → Embedding / Reranker 模型原理
Vector DB      → ANN / Vector Storage / Filter
RAG            → Retrieval Strategy / Evidence / Eval / Knowledge Ops
```

---

# 6. Agent Runtime

## Agent Harness / Runtime 🚧 下一块正式系统教材

权威实现参考：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

入口原则：[`agent-authoritative-sources.md`](agent-authoritative-sources.md)

当前正式能力域至少包括：

```text
Agent Boundary / Why Agent
→ Harness / Runtime Boundary
→ Agent Loop / Planning / ReAct / Routing
→ Intent Recognition
→ Context Assembly / Budget / Compaction / Correctness
→ Memory
→ Tool Runtime / Tool Message / Schema Validation
→ Tool Discovery / Progressive Loading
→ MCP / Skill / Capability Boundary
→ A2A
→ Permission / Approval / Sandbox
→ Prompt Injection / Untrusted Context
→ Runtime Message / Event Model
→ State / Session / Persistence
→ Checkpoint / Resume
→ Cancellation
→ Retry / Idempotency / Compensation
→ Multi-Agent / Supervisor / Handoff
→ Filesystem / Workspace Conflict
→ Repository Understanding
→ AI-assisted Development Workflow
→ Coding Verification
→ Framework Selection
→ Model Provider / Routing / Failover
→ Trace / Replay / Observability
→ Evaluation / Benchmark
→ Cost / Latency / Production Runtime
```

正式教材采用：

```text
完整 Runtime 理论体系
        +
Frozen HUMAN-A 面经
        +
Claude Code / Codex 源码实现事实
        ↓
Agent Harness Curriculum
```

源码只用于补齐课程与成熟实现，不改变 HUMAN-A Source Count。

Framework（LangChain / LangGraph / Spring AI 等）只在 Runtime 理论之后作为实现映射。

---

# 7. System Design ⏳

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
└─ Memory / State → Redis

Business / History Data → MySQL

贯穿：Timeout / Retry / Idempotency / MQ
      Trace / Metrics / Security / Scaling
```

---

# 8. Bridge Labs

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

目标：避免十个模块学成十座孤岛。

---

# 9. Interview Reality

研究入口：[`../research/README.md`](../research/README.md)

```text
HUMAN-A：S001–S279（Frozen）
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
```

核心闭环：

```text
完整知识体系
→ 系统学习
→ 真实面经
→ 回答 / 验证
→ Gap
→ 补教材
```

面经决定“哪里高频、哪里追得深”，不决定“只学哪些知识”。

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
| Agent Harness / Runtime | 🚧 **下一块；Claude Code / Codex + HUMAN-A 双重校准** |
| System Design | ⏳ Agent 前置成熟后汇总 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |

下一正式模块：**Agent Harness / Runtime**。
