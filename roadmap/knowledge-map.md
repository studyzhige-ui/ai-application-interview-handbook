# AI Application Engineer 求职知识总地图

> 这不是“把所有技术都学一遍”的清单，而是围绕 **AI 应用开发 / Agent 开发岗位**构建的一套从语言 → 服务 → 数据 → 模型基础 → 检索 → Agent Runtime → 生产系统的完整知识体系。
>
> 当前真实面经研究基线已冻结：`S001–S279` HUMAN-A，经过 Phase 2B 补漏后共有 **235 ACTIVE Canonical**。面经负责校准市场频率和追问深度，不反向限制完整知识体系。

## 1. 总体结构

```text
AI Application Engineer Knowledge System
│
├── Foundation
│   ├── Python
│   ├── FastAPI
│   └── AI Backend Engineering
│
├── Data
│   ├── MySQL
│   ├── Redis
│   └── Vector Database
│
├── Model Foundation
│   └── LLM Foundation（应用工程深度）
│
├── AI Application
│   └── RAG
│
├── Agent Runtime
│   └── Agent Harness / Runtime
│
├── Integration
│   └── System Design
│
└── Interview Reality
    └── 2026 HUMAN-A Frozen Research Baseline
```

---

# 2. 为什么 FastAPI 单独成为一级模块

原本可以把 FastAPI 塞进 “Python AI Engineering”，但这样会模糊三个不同层次：

```text
Python
回答：语言和运行时怎么工作？

FastAPI
回答：HTTP 请求怎样进入 Python AI 服务并得到响应？

Backend Engineering
回答：服务超时、重试、积压、重复执行、宕机、扩容时怎么办？
```

对于 AI 应用开发，FastAPI 正好是从“会 Python”跨到“会做 AI 服务”的桥梁，因此独立成环更合理。

---

# 3. 推荐主学习路线

```text
01 Python Foundation
        ↓
02 FastAPI / ASGI AI Service
        ↓
03 AI Backend Engineering
        ↓
04 MySQL
        ↓
05 Redis
        ↓
06 Vector Database / ANN Infrastructure
        ↓
07 LLM Foundation（应用工程深度）
        ↓
08 RAG Engineering
        ↓
09 Agent Harness / Runtime
        ↓
10 Production System Design
```

注意：`AI Backend Engineering` 不是第三阶段学完就结束，而是一条贯穿后续所有模块的横向主线。

例如：

```text
学习 Redis
  └─ 同时学习 Cache Consistency / HotKey / Rate Limit

学习 RAG
  └─ 同时学习 Async Ingestion / Large File / Queue / Observability

学习 Agent
  └─ 同时学习 Retry / Idempotency / Cancellation / Lease / Backpressure
```

横向还要持续贯穿：

```text
Evaluation / Verification
Reliability / Failure Recovery
Security / Permission
Observability
AI-assisted Development
```

---

# 4. 模块一：Python Foundation

当前状态：**主体已经完成并迁入总仓库。**

入口：[`../python/README.md`](../python/README.md)

核心体系：

```text
对象模型
→ 容器
→ 可变性 / 引用 / 拷贝
→ 函数 / 作用域 / 闭包
→ 迭代器 / 生成器
→ 装饰器 / 上下文管理器
→ OOP
→ 异常 / 文件 / import
→ GC / GIL
→ Thread / Process / Coroutine
→ async / await
→ 数据结构 / Top K
```

AI 应用重点：dict / hash、GIL、async / await、线程 / 进程 / 协程、生成器、上下文管理和大文件流式处理。

市场直接命中不高不等于知识重要度低。Python 是完整学习路径的基础层，Review 权重可以向 `asyncio / GIL / Decorator / Generator` 倾斜，但主体知识不能按面经频率裁掉。

---

# 5. 模块二：FastAPI

当前状态：**已建立一级模块和完整课程骨架。**

入口：[`../fastapi/README.md`](../fastapi/README.md)

主线：

```text
HTTP
→ ASGI / Uvicorn / FastAPI
→ Routing
→ Type Hint / Pydantic
→ Dependency Injection
→ Resource Lifecycle
→ async def vs def
→ Event Loop
→ StreamingResponse
→ SSE / WebSocket
→ Auth
→ DB / Redis / Provider Integration
→ Background Task Boundary
→ Timeout / Cancellation
→ Observability
→ Deployment
→ AI Chat / RAG / Agent API
```

最终目标：能从 0 设计和解释一个真实 AI API Service，而不只是会写路由装饰器。

---

# 6. 模块三：AI Backend Engineering

当前状态：**已建立一级模块和完整课程骨架。**

入口：[`../backend-engineering/README.md`](../backend-engineering/README.md)

主线：

```text
Network / HTTP
→ Concurrency
→ Connection Pool
→ Timeout
→ Retry
→ Circuit Breaker
→ Cancellation
→ Idempotency
→ Lock / Lease
→ MQ / Reliable Task
→ Backpressure
→ Cache / Rate Limit
→ Data Consistency
→ Large File Pipeline
→ Observability
→ Security
→ Deployment / Scaling
```

这一层负责回答：挂了怎么办、量大怎么办、慢了怎么办、重复怎么办、下游不可用怎么办、谁来恢复、怎么知道哪里出错。

---

# 7. 模块四：MySQL

当前状态：**✅ 第一版 0→1 系统教材已完成。**

入口：[`../mysql/README.md`](../mysql/README.md)

主线严格按知识依赖而不是面经热度组织：

```text
SQL / Execution
→ Index / B+Tree
→ Clustered / Secondary
→ Composite / Covering / Optimizer / EXPLAIN
→ ACID / Isolation / MVCC / Lock
→ redo / undo / binlog / Recovery
→ Pagination / Schema
→ Replication
→ Sharding
→ CDC
→ Bulk Write
→ AI Application Data Modeling
→ MySQL + Redis Consistency Boundary
```

当前配套：23 章正文 + 每章折叠自测 + Review + 高频面试题 + 易错点 + 面试前速查表。

---

# 8. 模块五：Redis

当前状态：**✅ 第一版 0→1 系统教材已完成。**

入口：[`../redis/README.md`](../redis/README.md)

虽然 Distributed Lock 是当前最强面试信号之一，但仍然放在 Transaction / Lua / HA 之后。

```text
Redis Role / Keyspace / Command
→ Core + Specialized Data Structures
→ Internal Encoding / Memory Model
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
→ Rate Limit
→ Security / Troubleshooting
→ Redis in AI System Design
```

当前配套：27 章正文 + 每章折叠自测 + Review + 35 道面试题 + 45 个易错点 + 面试前速查表。

---

# 9. 模块六：Vector Database

当前状态：**✅ 第一版 0→1 系统教材已完成。**

入口：[`../vector-db/README.md`](../vector-db/README.md)

```text
Vector / Dimension / Normalization
→ Cosine / Dot / L2
→ Top-K / Exact Search
→ ANN
→ HNSW / IVF / Quantization
→ Index Selection
→ Collection / Schema / Metadata
→ Metadata Filter / Tenant Isolation
→ Insert / Update / Delete / Compaction
→ Re-embedding / Version / Rebuild
→ Shard / Replica / Segment
→ Recall / Latency / Memory / QPS
→ Production Troubleshooting
→ Product / Architecture Selection
→ Graph DB Boundary / AI System Position
```

Primary Boundary：Vector DB 负责 Vector Storage / Similarity / ANN / Filter / Lifecycle / Scale；Dense / Sparse、Hybrid、RRF、Rerank、Top-K Strategy 和 Retrieval Evaluation 统一归 RAG。

当前配套：23 章正文 + 每章折叠自测 + Review + 31 道面试题 + 45 个易错点 + 面试前速查表。

---

# 10. 模块七：LLM Foundation（应用工程深度）

当前状态：**✅ 第一版 0→1 系统教材已完成。**

入口：[`../llm-foundation/README.md`](../llm-foundation/README.md)

目标不是学成训练算法工程师，而是理解会直接改变 AI Application / RAG / Agent 行为的模型机制。

```text
Token / Tokenization
→ Context Window / Long Context
→ Transformer Architecture
→ Self-Attention / QKV
→ Multi-Head / Causal Mask
→ FFN / Residual / Norm / RoPE
→ Autoregressive Generation
→ Logits / Decoding / Sampling
→ KV Cache
→ Prefill / Decode
→ Continuous Batching
→ PagedAttention / Serving Engine
→ TTFT / TPOT / Throughput / Cost
→ Precision / Quantization
→ Model API / Provider Adapter
→ Model Selection
→ Embedding Model
→ Reranker / Cross-Encoder
→ Multimodal Foundation
→ Prompt Engineering
→ Hallucination / Factuality
→ Prompt vs RAG vs Fine-tuning
→ SFT / LoRA / Preference Optimization / Distillation
```

`LLM-023 Prompt Engineering` 有 30 个独立 HUMAN-A 信号，因此 Prompt 章节强化了 Evaluation / Regression；但课程仍然先从 Token / Context / Transformer 建立因果链。

当前配套：

```text
29 章正文
+ 每章折叠自测
+ 7 张 Review 总图
+ 30 道面试题
+ 55 个面试易错点
+ 面试前速查表
```

---

# 11. 模块八：RAG

当前状态：**⏳ 下一块正式系统教材。**

计划主线：

```text
Document
→ Parse / OCR / Layout
→ Corpus Audit
→ Chunk Principles / Strategy / Parameters
→ Embedding / Vector Index Boundary
→ Query Rewrite / Decomposition / Clarification
→ No-hit / Refusal Boundary
→ Dense / Sparse / BM25
→ Hybrid Retrieval
→ RRF / Fusion
→ Rerank / Top-K
→ Retrieval Metrics
→ Context Build
→ Grounding / Citation
→ End-to-end Evaluation
→ Bad Case Attribution
→ Permission / Freshness / Version Governance
→ Incremental Update
→ Agentic RAG
```

重点不仅是“怎么做”，还要学习“怎么知道它哪里做错了”。真实面试里 29 道 RAG Canonical 有 20 道达到 L4，因此核心章节都必须带参数依据、Failure Case、Evaluation 与 Regression。

---

# 12. 模块九：Agent Harness / Runtime

这是最终最深、最大的模块。

权威实现参考：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

入口原则：[`agent-authoritative-sources.md`](agent-authoritative-sources.md)

当前至少覆盖：Agent Boundary / Loop / Planning / Routing、Intent、Context Assembly / Compaction、Memory、Tool Runtime / Discovery、MCP / Skills / A2A、Permission / Sandbox、Prompt Injection、State / Checkpoint / Resume、Cancellation、Retry / Idempotency、Multi-Agent、Workspace / Repository Understanding、AI-assisted Development、Trace / Replay / Evaluation、Model Provider / Routing、Cost / Latency 与 Production Runtime。

Agent Framework 作为 Runtime 理论之后的实现映射，不作为课程起点。

---

# 13. 模块十：System Design

前面所有模块最终在这里汇合。

典型系统：企业知识库 RAG、大规模文档 RAG、多租户 AI Chat / Agent Platform、Coding Agent Backend、Long-running Agent、Multi-Agent Workflow、AI Customer Service、Data / Analytical Agent。

```text
Client
  ↓
FastAPI / API
  ↓
Agent Harness
├─ Tools
├─ RAG → Vector DB
└─ Memory → Redis

Business / History Data → MySQL

贯穿：Timeout / Retry / Idempotency / MQ / Trace / Security / Scaling
```

---

# 14. Bridge Labs：避免十个模块学成十座孤岛

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

---

# 15. Interview Reality：真实面经不是目录，而是验收标准

研究层：[`../research/README.md`](../research/README.md)

```text
HUMAN-A：S001–S279（Frozen）
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
主动采集：停止，除非用户明确重新开启
```

> **面经决定“哪里更高频、哪里缺了一块”，但不会决定“只学哪些知识”。**

真实追问通常沿：

```text
Concept
→ Mechanism
→ Trade-off
→ Failure
→ Scale
→ Evaluation / Verification
```

---

# 16. 当前建设状态

| 模块 | 当前状态 |
|---|---|
| Python | ✅ 已有完整 12 章 + Review + Interview |
| FastAPI | 🟡 已建立完整课程地图，正文后续补齐 |
| AI Backend Engineering | 🟡 已建立完整课程地图，后续按项目穿插建设 |
| MySQL | ✅ 第一版完整 23 章 + Review + Interview |
| Redis | ✅ 第一版完整 27 章 + Review + Interview |
| Vector DB | ✅ 第一版完整 23 章 + Review + Interview |
| LLM Foundation | ✅ 第一版完整 29 章 + Review + Interview |
| RAG | ⏳ **下一块正式系统教材** |
| Agent Harness / Runtime | 🔬 RAG 后，以 Claude Code / Codex + Frozen HUMAN-A 建设 |
| System Design | ⏳ 随前置模块成熟逐步汇总 |
| 真实面经研究 | ✅ `S001–S279` Frozen；235 Canonical / Phase 2B 完成 |

下一块正式系统教材进入 **RAG**。依然坚持：完整知识体系先按初学者 0→1 建立，再让真人面经校准复习权重、Failure 深度和 Evaluation 强度。
