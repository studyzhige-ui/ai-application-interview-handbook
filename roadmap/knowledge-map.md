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

AI 应用重点：

- dict / hash
- GIL
- async / await
- 线程 / 进程 / 协程
- 生成器
- 上下文管理
- 大文件流式处理

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

真实面经里 FastAPI 直接命中较少，但 ASGI、Streaming 与 Runtime Boundary 都是后续 Agent Service 的必要桥梁，因此保持完整课程地位。

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

这一层负责回答面试最常见的工程追问：

> 挂了怎么办？
> 量大怎么办？
> 慢了怎么办？
> 重复怎么办？
> 下游不可用怎么办？
> 谁来恢复？
> 怎么知道哪里出错？

真实面经还稳定出现 JVM / Java Concurrency / ThreadLocal / Go GMP 等跨语言信号。它们后续采用 **Role-dependent Backend Bridge** 形式补充，不把主线扩成全语言后端大全。

---

# 7. 模块四：MySQL

当前状态：**✅ 第一版 0→1 系统教材已完成。**

入口：[`../mysql/README.md`](../mysql/README.md)

主线严格按知识依赖而不是面经热度组织：

```text
01 MySQL 在 AI 应用里的职责
02 SQL 基础 / SQL Execution
03 Index 基础
04 B+Tree
05 Clustered / Secondary Index
06 Composite Index / Leftmost Prefix
07 Covering Index / Back Table / ICP
08 Index Invalidation / Optimizer
09 EXPLAIN / Slow SQL
10 Primary Key / Index Lifecycle
11 ACID
12 Isolation Level
13 MVCC / Undo / Read View
14 Record / Gap / Next-key Lock / Deadlock
15 redo / undo / binlog / Two-phase Commit
16 Deep Pagination
17 Schema Design
18 Replication
19 Sharding
20 CDC / Data Sync
21 Bulk Write / Write Path
22 AI Application Data Modeling
23 MySQL + Redis Consistency Boundary
```

这里特别固定一条课程规则：

> **真实面经只能提高某些章节的复习优先级、补充项目场景和追问深度，不能因为 Sharding / Cache Consistency 更高频就把它们提前到 B+Tree、Transaction、MVCC 之前。**

`MySQL + Redis Consistency` 的完整系统语义 Primary 在 AI Backend Engineering，因此故意放在 MySQL 最后一章作为跨模块桥梁；MySQL 主体先完整闭环自己的 SQL / Index / Transaction / Log / Scale / Data Modeling。

当前配套已经包括：

```text
23 章正文
+ 每章折叠自测
+ Review 图解总入口
+ 高频面试题
+ 面试易错点
+ 面试前速查表
```

---

# 8. 模块五：Redis

计划主线：

```text
01 Redis 为什么存在
02 String / Hash / List / Set / ZSet
03 Redis 为什么快
04 Thread Model / IO Multiplexing
05 TTL / Expiration
06 Eviction
07 Cache Penetration / Breakdown / Avalanche
08 BigKey / HotKey
09 RDB / AOF
10 Primary / Replica / Sentinel
11 Cluster / Hash Slot / Reshard
12 Distributed Lock / Lease / WatchDog
13 Lock Correctness / Owner / Lua Release
14 Lua / Atomicity
15 Cache Consistency Boundary
16 Multi-level Cache
17 Session / Conversation
18 Semantic / Result Cache
19 Agent Short-term State
20 Rate Limit
21 Security Boundary
22 Redis in AI System Design
```

Agent Checkpoint / Runtime State 的**执行语义**归 Agent Harness；Redis 这里只解释作为 State Store 时的数据结构、持久化与一致性能力。

Redis 也将遵循和 MySQL 相同的 0→1 原则：先建立数据结构和 Runtime 基础，再进入缓存、分布式锁、集群与 AI 场景；面经只校准重点，不打乱主干。

---

# 9. 模块六：Vector Database

计划从原理开始，而不是从 Milvus API 开始。最新 Primary Ownership 已明确把完整 Retrieval Strategy 归到 RAG，因此 Vector DB 只负责向量基础设施与 ANN Index：

```text
Embedding Vector Storage Semantics
→ Vector Space
→ Cosine / IP / L2
→ Exact Search vs ANN
→ HNSW
→ IVF
→ Index Selection / Parameter Trade-off
→ Metadata Filtering
→ Vector Data Modeling
→ Recall / Latency / Memory / QPS
→ Index Lifecycle / Freshness
→ Graph DB vs Vector DB
→ Milvus / FAISS / pgvector / ES Vector Selection
```

以下内容**不再作为 Vector DB Primary**，统一在 RAG 讲完整 Retrieval Pipeline：

```text
Dense vs Sparse / BM25
Hybrid Retrieval
RRF / Fusion
Rerank Pipeline
Top-K Strategy
Retrieval Evaluation
```

---

# 10. 模块七：LLM Foundation（应用工程深度）

这是 Phase 2B 对 Roadmap 补出的正式一级模块。目标不是学成训练算法工程师，而是理解会直接改变 AI Application / RAG / Agent 行为的模型机制。

计划主线：

```text
01 Tokenization / Token Budget
02 Context Window / Long-context Limitation
03 Transformer Architecture
04 Self-Attention / QKV / Multi-Head Attention
05 FFN / Positional Encoding / RoPE
06 Inference / Generation
07 KV Cache
08 Prefill / Decode
09 Inference Engine / PagedAttention / vLLM / SGLang
10 Inference Latency / Cost
11 Model API / Sampling Parameters
12 Model Selection
13 Embedding Model
14 Reranker / Cross-Encoder
15 Prompt Engineering
16 Hallucination / Factuality Boundary
17 Fine-tuning
18 SFT / LoRA / DPO / GRPO / Distillation
19 Multimodal Foundation
```

### Prompt Engineering 必须单独成章

Phase 2B 中 `LLM-023` 有 30 个独立 HUMAN-A 信号。课程不能只讲“Prompt 写清楚一点”，而要形成：

```text
Goal / Role / Instruction
→ Context / Example
→ Tool / Output Contract
→ Versioning
→ Evaluation / Regression
→ Failure / Injection Boundary
```

Prompt Injection 的完整安全治理继续在 Agent Harness 的 Untrusted Context / Permission 中深化。

---

# 11. 模块八：RAG

计划主线：

```text
Document
→ Parse / OCR / Layout
→ Chunk Principles / Strategy / Parameters
→ Embedding / Index Boundary
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

重点不仅是“怎么做”，还要学习“怎么知道它哪里做错了”。

真实面试里 29 道 RAG Canonical 有 20 道达到 L4，因此每个核心章节都应该带：参数依据、Failure Case、Evaluation 与 Regression，而不是只解释组件名词。

---

# 12. 模块九：Agent Harness / Runtime

这是最终最深、最大的模块。

权威实现参考：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

入口原则：[`agent-authoritative-sources.md`](agent-authoritative-sources.md)

当前根据 235 道 Canonical 与高质量真实面经，Agent Harness 至少应形成这些大域：

```text
Agent Harness / Runtime
│
├── Agent Boundary / Why Agent
├── Agent Loop / Control Loop
├── Planning / ReAct / Routing
├── Intent Recognition / Router
├── Context Assembly
├── Context Budget / Compaction
├── Compaction Correctness
├── Memory
├── Tool Runtime / Executor
├── Tool Discovery / Progressive Loading
├── MCP / Skills / Capability Boundary
├── A2A / Agent Communication Protocol
├── Permission / Approval / Sandbox
├── Prompt Injection / Untrusted Context Security
├── Runtime Message / Event Model
├── State / Persistence
├── Checkpoint / Resume
├── Cancellation
├── Retry / Idempotency / Compensation
├── Multi-Agent
├── Filesystem / Workspace Transaction
├── Repository Understanding
├── AI-assisted Development Workflow
├── Coding Verification
├── Agent Framework Selection
├── Model Provider / Routing / Failover
├── Trace / Replay / Observability
├── Evaluation / Benchmark
├── Cost / Latency
└── Production Runtime
```

后续不是凭空写教材，而采用：

```text
真实面经问题
      +
Claude Code / Codex 源码事实
      +
完整 Runtime 理论体系
      ↓
Agent Harness 教材
```

Agent Framework（LangChain / LangGraph / Spring AI 等）应在 Runtime 理论之后作为**实现映射**，不作为课程起点。

AI-assisted Development 也不是“工具推荐”附录，而要覆盖 Requirement → Context → Repo Understanding → Generation → Test → Diff / Review → Verification → Delivery。

---

# 13. 模块十：System Design

前面所有模块最终在这里汇合。

典型系统：

- 企业知识库 RAG
- 大规模文档 RAG
- 多租户 AI Chat / Agent Platform
- Agent 知识助手
- Coding Agent Backend
- Long-running Agent Platform
- Multi-Agent Workflow
- AI Customer Service
- Data / Analytical Agent
- AI Interview / Learning Assistant

一张总图：

```text
                             Client
                               │
                               ▼
                         FastAPI / API
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
          Auth / Tenant     Streaming       Task API
                               │
                               ▼
                         Agent Harness
                  ┌────────────┼────────────┐
                  ▼            ▼            ▼
                Tools         RAG         Memory
                  │            │            │
                  │      ┌─────┴─────┐      │
                  │      ▼           ▼      ▼
                  │   Retriever   VectorDB Redis
                  │
                  ▼
            External APIs

                    Business / History Data
                              │
                              ▼
                            MySQL

        贯穿所有组件：Timeout / Retry / Idempotency / MQ
                      Trace / Metrics / Security / Scaling
```

---

# 14. Bridge Labs：避免十个模块学成十座孤岛

Phase 2B 的真实共现中，最高组合包括 RAG ↔ Agent Harness、AI Backend ↔ Agent Harness、AI Backend ↔ Redis、AI Backend ↔ MySQL、LLM Foundation ↔ Agent Harness。

因此正式课程增加四个桥接项目：

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

目标是让每个模块既能独立解释，也能在真实系统里串起来。

---

# 15. Interview Reality：真实面经不是目录，而是验收标准

研究层：[`../research/README.md`](../research/README.md)

当前正式研究口径：

```text
HUMAN-A：S001–S279（Frozen）
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
主动采集：停止，除非用户明确重新开启
```

核心闭环：

```text
完整知识体系
      ↓
系统学习
      ↓
真实 2026 面经
      ↓
能不能回答？
   ↙       ↘
  能        不能
  ↓          ↓
验证体系   发现知识 Gap
             ↓
          补充教材
```

因此：

> **面经决定“哪里更高频、哪里缺了一块”，但不会决定“只学哪些知识”。**

真实追问链还表明，高频面试通常沿：

```text
Concept
→ Mechanism
→ Trade-off
→ Failure
→ Scale
→ Evaluation / Verification
```

所以后续教材不能只增加更多定义题，而要把 Production 深度写进章节结构。

---

# 16. 当前建设状态

| 模块 | 当前状态 |
|---|---|
| Python | ✅ 已有完整 12 章 + Review + Interview |
| FastAPI | 🟡 已建立完整课程地图，下一步写正文 |
| AI Backend Engineering | 🟡 已建立完整课程地图，后续按项目穿插建设 |
| MySQL | ✅ 第一版完整 23 章 + Review + Interview 已完成 |
| Redis | ⏳ 下一块正式系统教材；课程边界已校准 |
| Vector DB | ⏳ Redis 之后；已与 RAG 重划 Primary Boundary |
| LLM Foundation | 🆕 已正式进入一级 Roadmap，后续建设应用工程深度教材 |
| RAG | ⏳ LLM Foundation 之后；按 Evaluation / Failure 深度建设 |
| Agent Harness / Runtime | 🔬 用 Claude Code / Codex + Frozen HUMAN-A 继续校准后建设 |
| System Design | ⏳ 随各模块成熟逐步汇总 |
| 真实面经研究 | ✅ `S001–S279` 已冻结；235 Canonical / Phase 2B 市场分析完成 |

下一块正式系统教材进入 **Redis**。依然坚持：完整知识体系先按初学者 0→1 建立，再让真人面经校准复习权重和追问深度。