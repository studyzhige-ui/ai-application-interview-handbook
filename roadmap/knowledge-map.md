# AI Application Engineer｜十板块知识地图

[← Handbook 总目录](../README.md) · [正式学习路线](learning-path.md) · [v1.0 终局质量审计](final-quality-audit.md) · [跨模块术语表](terminology-glossary.md) · [课程进度](../research/questions/progress.md) · [Canonical Index](../research/questions/module-index.md)

> 十个一级模块已经全部完成第一版系统教材。这里强调**模块职责、知识依赖与边界**；章节细节进入各模块 README，实际每天怎样学习见 [Learning Path](learning-path.md)。

## 总路线

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent Harness / Runtime](../agent-harness/README.md) → [System Design](../system-design/README.md)

## 总览

| # | 模块 | Blocks | Canonical | 核心角色 |
|---:|---|---:|---:|---|
| 01 | [Python Foundation](../python/README.md) | 13 | 15 | 建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。 |
| 02 | [FastAPI](../fastapi/README.md) | 16 | 4 | 把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。 |
| 03 | [AI Backend Engineering](../backend-engineering/README.md) | 22 | 39 | 把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。 |
| 04 | [MySQL](../mysql/README.md) | 23 | 26 | 理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。 |
| 05 | [Redis](../redis/README.md) | 24 | 19 | 掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。 |
| 06 | [Vector Database](../vector-db/README.md) | 16 | 12 | 理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。 |
| 07 | [LLM Foundation（应用工程深度）](../llm-foundation/README.md) | 14 | 23 | 以应用工程深度理解 Token、Transformer、Generation、KV Cache、Serving、模型选择与 Prompt / Fine-tuning 的边界。 |
| 08 | [RAG](../rag/README.md) | 14 | 29 | 把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。 |
| 09 | [Agent Harness / Runtime](../agent-harness/README.md) | 23 | 44 | 从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。 |
| 10 | [System Design](../system-design/README.md) | 19 | 24 | 把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。 |

---

## 01. [Python Foundation](../python/README.md) ✅ — 13 blocks

建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。

```text
Object Model / Containers → Function / Scope → Iterator / Context Manager → OOP / Protocol → Structured Data → Memory / GIL → Thread / Process / asyncio → Data Structure
```

市场校准：**15 Canonical / 15 independent HUMAN-A flows**。

## 02. [FastAPI](../fastapi/README.md) ✅ — 16 blocks

把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。

```text
ASGI Request Lifecycle → API Contract / Validation → DI / Middleware / Resource Lifecycle → Async Boundary → SSE / WebSocket → Security / External Resource → Cancellation → Testing / Observability / Deployment → AI Service Patterns
```

市场校准：**4 Canonical / 3 independent HUMAN-A flows**。

## 03. [AI Backend Engineering](../backend-engineering/README.md) ✅ — 22 blocks

把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。

```text
Request / Network → Concurrency / Pool / Backpressure → Timeout / Retry / Idempotency → MQ / Kafka / Durable Task → Consistency / State / Auth → Discovery / Observability / Linux / K8s → Config / Security → Cross-language Runtime Mapping
```

市场校准：**39 Canonical / 125 independent HUMAN-A flows**。

## 04. [MySQL](../mysql/README.md) ✅ — 23 blocks

理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。

```text
SQL Execution → Index / B+Tree / Optimizer / EXPLAIN → Transaction / Isolation / MVCC / Lock / Log → Pagination / Schema → Replication / Sharding / CDC / Bulk Write → AI Data Modeling / Cache Boundary
```

市场校准：**26 Canonical / 55 independent HUMAN-A flows**。

## 05. [Redis](../redis/README.md) ✅ — 24 blocks

掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。

```text
Key / Data Structure / Encoding → Runtime / TTL / Eviction → Cache Failure / HotKey → RDB / AOF / Replication / Sentinel / Cluster → Transaction / Pipeline / Lua / Distributed Lock → Streams / Session / Rate Limit / Troubleshooting
```

市场校准：**19 Canonical / 69 independent HUMAN-A flows**。

## 06. [Vector Database](../vector-db/README.md) ✅ — 16 blocks

理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。

```text
Vector Space / Similarity → Exact vs ANN → HNSW / IVF / Quantization / Index Selection → Schema / Filter / Tenant → Index Lifecycle / Distributed → Performance Diagnosis / Product Boundary
```

市场校准：**12 Canonical / 37 independent HUMAN-A flows**。

## 07. [LLM Foundation（应用工程深度）](../llm-foundation/README.md) ✅ — 14 blocks

以应用工程深度理解 Token、Transformer、Generation、KV Cache、Serving、模型选择与 Prompt / Fine-tuning 的边界。

```text
Token / Context → Transformer / Attention / Position → Generation / Decoding → KV Cache / Prefill / Decode → Serving → Model API / Selection → Embedding / Reranker / Multimodal → Prompt / Factuality → Fine-tuning / Post-training
```

市场校准：**23 Canonical / 82 independent HUMAN-A flows**。

## 08. [RAG](../rag/README.md) ✅ — 14 blocks

把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。

```text
Corpus Governance → Document Processing → Chunk Design → Query Planning → Dense / Sparse / Hybrid / Fusion → Rerank / Candidate Budget → Evidence / Grounding / Citation → Retrieval & E2E Evaluation → Production Governance / Scale → GraphRAG / Agentic RAG
```

市场校准：**29 Canonical / 88 independent HUMAN-A flows**。

## 09. [Agent Harness / Runtime](../agent-harness/README.md) ✅ — 23 blocks

从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。

```text
Agent Boundary / Loop → Tool Runtime → Planning / Control → Context Assembly / Compaction → Memory / Session / Checkpoint → Permission / Sandbox / Injection → MCP / Skills / Hooks / Routing → Multi-Agent / A2A → Trace / Eval / Coding Agent → Production Runtime / Framework Mapping
```

市场校准：**44 Canonical / 166 independent HUMAN-A flows**。

## 10. [System Design](../system-design/README.md) ✅ — 19 blocks

把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。

```text
Requirement / SLO → Workload / Capacity → API / Data / State → Flow / Cache / Partition → Consistency / Queue → Reliability / Security → Observability / Evaluation / Cost / Evolution → High-concurrency / Realtime / Data Processing / LLM Gateway / Enterprise RAG / Production Agent Cases
```

市场校准：**24 Canonical / 71 independent HUMAN-A flows**。

---

## 使用规则

- 学习顺序由知识依赖决定，不按面经频率重排；
- 真人面经只调整复习权重、真实问法和追问深度；
- 跨模块问题只在 Primary Module 维护完整机制；
- 章节数是认知闭环的结果，不是统一 KPI；
- 第一次完整学习使用 [Learning Path](learning-path.md) 的 Curriculum → Review → Interview 三遍法；
- 当前粒度与深度状态见 [Granularity Audit](curriculum-granularity-audit.md) 与 [Content Depth Audit](content-depth-audit.md)；
- v1.0 全仓库最终结论见 [Final Quality Audit](final-quality-audit.md)；跨模块同名概念统一以 [Terminology Glossary](terminology-glossary.md) 为工作定义。
