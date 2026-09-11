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

Phase 2B 已完成：

- 全局 Canonical Index；
- Frequency Ranking；
- Company / Role / Round Coverage；
- Depth / Question Type；
- Co-occurrence；
- Verified Follow-up Chains；
- Curriculum Evidence Matrix；
- Knowledge Gap Analysis。

研究结果见 [`research/analysis/`](research/analysis/README.md)。

---

# 总知识地图

完整地图：[`roadmap/knowledge-map.md`](roadmap/knowledge-map.md)

## Foundation

### [Python Foundation](python/README.md) ✅

完整 12 章系统正文 + Review + Interview。

承担：对象模型、容器、GIL、线程 / 进程 / 协程、asyncio、生成器、上下文管理等 AI Backend Runtime 基础。

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

主干严格按知识依赖：

```text
SQL / Execution
→ Index / B+Tree
→ Clustered / Secondary
→ Composite / Covering / Optimizer / EXPLAIN
→ ACID / Isolation / MVCC / Lock
→ Redo / Undo / Binlog / Recovery
→ Pagination / Schema
→ Replication
→ Sharding
→ CDC
→ Bulk Write
→ AI Application Data Modeling
→ MySQL + Redis Integration Boundary
```

### [Redis](redis/README.md) ✅

第一版系统教材已完成：**27 章正文 + 每章折叠自测 + Review 总图 + 35 道面试题 + 45 个易错点 + 面试前速查。**

主干继续按 0→1 认知依赖：

```text
Redis Role / Keyspace / Command
→ Core + Specialized Data Structures
→ Internal Encoding
→ Thread Model / Event Loop / I/O Multiplexing
→ TTL / Expiration / Eviction
→ Cache Failure / BigKey / HotKey
→ RDB / AOF
→ Replication / Sentinel / Cluster
→ MULTI / WATCH / Pipeline / Lua
→ Distributed Lock / Lease / Fencing
→ Pub/Sub / Streams
→ Multi-level / Semantic Cache
→ Session / Conversation / Agent State Store
→ Rate Limit
→ Security / Troubleshooting
→ Redis in AI System Design
```

高频面经中的分布式锁、缓存故障会讲到更深，但不会被提前到数据结构、Runtime、TTL、Persistence 这些必要前置之前。

### Vector Database ⏳

下一块正式系统教材。Primary 聚焦向量基础设施：

```text
Vector / Distance
→ Exact Search vs ANN
→ HNSW / IVF
→ Metadata Filter
→ Index Trade-off / Lifecycle
→ Product Selection
```

Dense / Sparse、Hybrid、RRF、Rerank、Top-K 与 Retrieval Evaluation 统一归 RAG 主线。

---

## Model Foundation

### LLM Foundation（应用工程深度） 🆕

```text
Tokenization
→ Context Window
→ Transformer / Attention
→ KV Cache / Prefill / Decode
→ Serving / Latency / Cost
→ Model API / Sampling / Selection
→ Embedding / Rerank
→ Prompt Engineering
→ Hallucination Boundary
→ Fine-tuning / Alignment 使用边界
```

目标是理解会直接改变 AI Application / RAG / Agent 行为的模型机制，不扩展成训练 Infra 大全。

---

## AI Application

### RAG ⏳

```text
Parse / OCR / Layout
→ Chunk
→ Embedding / Index Boundary
→ Query Rewrite
→ Dense / Sparse / Hybrid
→ RRF / Rerank / Top-K
→ Context Build / Grounding
→ Evaluation / Bad Case Attribution
→ Permission / Version / Freshness
→ Incremental Update
→ Agentic RAG
```

真实面试已经稳定进入 Evaluation、Failure Attribution 和 Production Governance，不只问组件名词。

---

## Agent Runtime

### Agent Harness / Runtime 🔬

重点覆盖：

- Agent Boundary / Loop / Planning / Routing；
- Context Assembly / Compaction / Correctness；
- Memory；
- Tool Runtime / Discovery / Progressive Loading；
- MCP / Skill / A2A；
- Permission / Approval / Sandbox；
- Prompt Injection / Untrusted Context；
- State / Persistence / Checkpoint / Resume；
- Cancellation / Retry / Idempotency / Compensation；
- Multi-Agent；
- Repository Understanding / Coding Verification；
- AI-assisted Development Workflow；
- Trace / Replay / Evaluation / Benchmark；
- Model Routing / Cost / Latency / Production Reliability。

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

> **先讲人话 → 准确定义 → 代码 / SQL / 图解 → 原理 → 对比 → Failure Case → AI 实际场景 → 易错点 → 面试怎么答 → 深入追问 → 真人面经 → 折叠自测**

最终让每个知识点达到：

> **定义能说、代码能写、为什么能解释、工程边界能判断、真人追问能接。**

---

# 当前建设状态

| 模块 | 状态 |
|---|---|
| Python | ✅ 完整系统教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 第一版完整系统教材 |
| Redis | ✅ 第一版完整系统教材 |
| Vector DB | ⏳ 下一块正式系统教材 |
| LLM Foundation | 🆕 已纳入一级体系 |
| RAG | ⏳ 待建设 |
| Agent Harness / Runtime | 🔬 源码 + 面经校准中 |
| System Design | ⏳ 随前置模块汇总 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
