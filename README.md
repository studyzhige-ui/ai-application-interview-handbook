# AI Application Interview Handbook

> 面向 **AI 应用开发 / AI Agent 开发** 求职的一套系统化知识体系、工程手册与真人面经验收系统。

这不是一本“AI 八股题库”。目标是从 0 建立完整能力链：

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用工程深度）
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

## 核心原则

### 1. 知识体系决定主干，真人面经校准重点

所有模块都先按初学者认知依赖从 0→1 建立完整体系。

真人面经只负责：

- 调整复习优先级；
- 保留真实问法；
- 补充追问链；
- 检查 Failure / Scale / Evaluation 深度；
- 验收“学完能不能真的回答”。

**不会因为某个知识点真人面经更高频，就打乱模块本身的主要演进顺序。**

### 2. 从 Demo 能力走到 Production 能力

不仅学习“怎么调 API”，还要回答：

> 超时怎么办？重复执行怎么办？Context 满了怎么办？缓存不一致怎么办？RAG 召回不准怎么定位？Agent 如何取消、恢复和验证？

### 3. Agent Harness 以成熟产品源码为最高实现参考

首要权威实现参考：

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

面经告诉我们市场已经问到哪里；Claude Code / Codex 源码帮助补齐成熟 Harness / Runtime 实际必须解决的工程问题。

### 4. 正式面经只认 HUMAN-A

只有满足真人候选人第一人称、高质量现场证据、岗位范围符合、原文可核验且非转载 / 非同场重复的来源，才能进入正式研究并贡献频率。

详细规则：[`research/quality/source-quality-policy.md`](research/quality/source-quality-policy.md)

---

# 当前正式研究基线

入口：[`research/README.md`](research/README.md)

```text
HUMAN-A：S001–S279（Frozen）
正式 Batch：26
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
主动采集：已暂停
```

Phase 2B 已完成：Global Canonical Index、Frequency、Market Coverage、Depth / Question Type、Co-occurrence、Verified Follow-up Chains、Curriculum Evidence Matrix 与 Knowledge Gap Analysis。

研究结果见 [`research/analysis/`](research/analysis/README.md)。

---

# 总知识地图

完整地图：[`roadmap/knowledge-map.md`](roadmap/knowledge-map.md)

## Foundation

### [Python Foundation](python/README.md) ✅

完整 12 章系统正文 + Review + Interview。

### [FastAPI｜AI 应用服务层](fastapi/README.md) 🟡

已建立完整课程地图：

```text
HTTP / ASGI / Uvicorn
→ Routing / Pydantic
→ Dependency / Lifespan
→ async def / Event Loop
→ Streaming / SSE / WebSocket
→ Auth
→ DB / Redis / Provider Integration
→ Timeout / Cancellation
→ Testing / Trace / Deployment
→ RAG / Agent API Design
```

### [AI Backend Engineering](backend-engineering/README.md) 🟡

已建立完整课程地图：

```text
Network / HTTP
→ Concurrency
→ Connection Pool
→ Timeout / Retry / Circuit Breaker
→ Cancellation / Idempotency
→ MQ / Backpressure
→ Cache / Rate Limit / Data Consistency
→ Observability / Security
→ Deployment / Scaling
```

---

## Data

### [MySQL](mysql/README.md) ✅

第一版系统教材已完成：**23 章正文 + 每章折叠自测 + Review + 高频面试题 + 易错点 + 面试前速查。**

```text
SQL / Execution
→ Index / B+Tree
→ Clustered / Secondary
→ Composite / Covering / Optimizer / EXPLAIN
→ ACID / Isolation / MVCC / Lock
→ Redo / Undo / Binlog / Recovery
→ Pagination / Schema
→ Replication → Sharding → CDC
→ Bulk Write
→ AI Application Data Modeling
→ MySQL + Redis Integration Boundary
```

### [Redis](redis/README.md) ✅

第一版系统教材已完成：**27 章正文 + 每章折叠自测 + Review 总图 + 35 道面试题 + 45 个易错点 + 面试前速查。**

```text
Redis Role / Keyspace / Command
→ Data Structures / Internal Encoding
→ Thread Model / Event Loop / I/O Multiplexing
→ TTL / Eviction / Cache Failure / BigKey / HotKey
→ RDB / AOF / Replication / Sentinel / Cluster
→ MULTI / WATCH / Pipeline / Lua
→ Distributed Lock / Lease / Fencing
→ Pub/Sub / Streams
→ Multi-level / Semantic Cache
→ Session / Conversation / Agent State Store
→ Rate Limit / Security / Troubleshooting
→ Redis in AI System Design
```

### [Vector Database](vector-db/README.md) ✅

第一版系统教材已完成：**23 章正文 + 每章折叠自测 + Review 图解总览 + 31 道面试题 + 45 个易错点 + 面试前速查。**

```text
Vector / Dimension / Normalization
→ Cosine / Dot / L2
→ Top-K Exact Search → ANN
→ HNSW / IVF / Quantization
→ Index Selection
→ Collection / Schema / Metadata
→ Metadata Filter / Tenant Isolation
→ Insert / Update / Delete / Compaction
→ Re-embedding / Rebuild / Version
→ Shard / Replica
→ Capacity / Troubleshooting
→ Product / Architecture Selection
→ Graph DB / RAG Boundary
```

Dense / Sparse、Hybrid、RRF、Rerank、Top-K Strategy 与 Retrieval Evaluation 统一留在 RAG。

---

## Model Foundation

### [LLM Foundation（应用工程深度）](llm-foundation/README.md) ✅

第一版系统教材已完成：**29 章正文 + 每章折叠自测 + 7 张 Review 总图 + 30 道面试题 + 55 个易错点 + 面试前速查。**

主干严格按应用工程师 0→1 认知依赖：

```text
Token / Tokenization
→ Context Window / Long Context
→ Transformer Architecture
→ QKV / Self-Attention / Multi-Head / Causal Mask
→ FFN / Residual / Norm / RoPE
→ Autoregressive Generation
→ Logits / Decoding / Sampling
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

这一层解释“模型为什么这样工作和这样表现”，不扩展成 CUDA / Distributed Training Infra 大全。

---

## AI Application

### RAG ⏳

**下一块正式系统教材。**

```text
Parse / OCR / Layout
→ Corpus Audit
→ Chunk Principles / Strategy / Parameters
→ Embedding / Index Boundary
→ Query Rewrite / Decomposition / Clarification
→ Dense / Sparse / BM25
→ Hybrid Retrieval / RRF
→ Rerank / Top-K
→ Retrieval Evaluation
→ Context Build / Grounding / Citation
→ End-to-end Evaluation / Bad Case Attribution
→ Permission / Version / Freshness
→ Incremental Update
→ Agentic RAG
```

真实面试已经稳定进入 Evaluation、Failure Attribution 和 Production Governance，不只问组件名词。

---

## Agent Runtime

### Agent Harness / Runtime 🔬

重点覆盖 Agent Boundary / Loop / Planning / Routing、Context Assembly / Compaction、Memory、Tool Runtime、MCP / Skill / A2A、Permission / Sandbox、State / Checkpoint / Resume、Cancellation / Retry / Idempotency、Multi-Agent、Repository Understanding、Trace / Evaluation、Model Routing、Cost 与 Production Reliability。

Framework（LangChain / LangGraph 等）作为 Runtime 理论之后的实现映射，不作为课程起点。

---

# 推荐学习顺序

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering 基础
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用层）
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

`AI Backend Engineering` 是横向主线，会在 MySQL / Redis / RAG / Agent 阶段反复加深。

---

# 写作风格

所有正式教材尽量遵循：

> **先讲人话 → 准确定义 → 代码 / 数学 / 图解 → 原理 → 对比 → Failure Case → AI 实际场景 → 易错点 → 面试怎么答 → 深入追问 → 真人面经 → 折叠自测**

最终让每个知识点达到：

> **定义能说、机制能解释、工程边界能判断、失败能定位、真人追问能接。**

---

# 当前建设状态

| 模块 | 状态 |
|---|---|
| Python | ✅ 完整系统教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 第一版完整系统教材 |
| Redis | ✅ 第一版完整系统教材 |
| Vector DB | ✅ 第一版完整系统教材 |
| LLM Foundation | ✅ 第一版完整系统教材 |
| RAG | ⏳ **下一块正式系统教材** |
| Agent Harness / Runtime | 🔬 源码 + 面经校准中 |
| System Design | ⏳ 随前置模块汇总 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
