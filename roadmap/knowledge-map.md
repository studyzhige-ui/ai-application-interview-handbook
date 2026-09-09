# AI Application Engineer 求职知识总地图

> 这不是“把所有技术都学一遍”的清单，而是围绕 **AI 应用开发 / Agent 开发岗位**构建的一套从语言 → 服务 → 数据 → 检索 → Agent Runtime → 生产系统的完整知识体系。

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
├── AI Application
│   └── RAG
│
├── Agent Runtime
│   └── Agent Harness
│
├── Integration
│   └── System Design
│
└── Interview Reality
    └── 2026 高质量真实面经研究
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
02 FastAPI
        ↓
03 AI Backend Engineering 基础
        ↓
04 MySQL
        ↓
05 Redis
        ↓
06 Vector Database
        ↓
07 RAG
        ↓
08 Agent Harness / Runtime
        ↓
09 Production System Design
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

---

# 7. 模块四：MySQL

建设顺序：**下一阶段正式教材的第一块。**

计划主线：

```text
01 MySQL 在 AI 应用里的职责
02 SQL 基础
03 Index 基础
04 B+Tree
05 Composite Index / Leftmost Prefix
06 Covering Index / Back Table / ICP
07 EXPLAIN / Slow SQL
08 ACID
09 Isolation Level
10 MVCC / Undo / Read View
11 Lock / Gap / Next-key
12 redo / undo / binlog
13 Pagination / Query Optimization
14 Schema Design
15 MySQL + Redis Consistency
16 AI Application Data Modeling
```

原则：不学成 DBA，但要能设计 AI 产品的数据层，并解释性能与一致性。

---

# 8. 模块五：Redis

计划主线：

```text
01 Redis 为什么存在
02 String / Hash / List / Set / ZSet
03 Redis 为什么快
04 Thread Model
05 IO Multiplexing
06 TTL / Expiration
07 Eviction
08 Cache Penetration / Breakdown / Avalanche
09 BigKey / HotKey
10 RDB / AOF
11 Distributed Lock / Lease / WatchDog
12 Lua / Atomicity
13 Cache Consistency
14 Session / Conversation
15 Agent Short-term State
16 Checkpoint / Runtime State
17 Rate Limit
18 Redis in AI System Design
```

---

# 9. 模块六：Vector Database

计划从原理开始，而不是从 Milvus API 开始：

```text
Embedding
→ Vector Space
→ Cosine / IP / L2
→ TopK
→ Exact Search
→ ANN
→ HNSW
→ IVF
→ Index Trade-off
→ Metadata Filtering
→ Dense / Sparse
→ BM25
→ Hybrid Retrieval
→ RRF / Score Fusion
→ Reranker
→ Recall / Latency / Memory / QPS
→ Index Lifecycle
→ Milvus / Qdrant / pgvector Selection
```

---

# 10. 模块七：RAG

计划主线：

```text
Document
→ Parse / OCR / Layout
→ Chunk
→ Embedding
→ Index
→ Query Rewrite
→ Retrieval
→ Hybrid Search
→ Rerank
→ Context Build
→ Grounding / Citation
→ Generation
→ Evaluation
→ Observability
→ Version / Snapshot / Knowledge Governance
→ Incremental Update
→ Agentic RAG
```

重点不仅是“怎么做”，还要学习“怎么知道它哪里做错了”。

---

# 11. 模块八：Agent Harness / Runtime

这是最终最深、最大的模块。

权威实现参考：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

入口原则：[`agent-authoritative-sources.md`](agent-authoritative-sources.md)

当前根据高质量真实面经，Agent Harness 至少应形成这些大域：

```text
Agent Harness
│
├── Agent Loop / Control Loop
├── Planning / Routing / ReAct
├── Context Assembly
├── Context Compaction
├── Memory
├── Tool Runtime / Executor
├── MCP / Skills / Discovery
├── Permission / Approval / Sandbox
├── Runtime Message / Event Model
├── State / Persistence
├── Checkpoint / Resume
├── Cancellation
├── Retry / Idempotency / Compensation
├── Multi-Agent
├── Filesystem / Workspace Transaction
├── Coding Verification
├── Model Provider / Routing / Failover
├── Trace / Replay / Observability
├── Evaluation
├── Cost / Latency
├── Security
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

---

# 12. 模块九：System Design

前面所有模块最终在这里汇合。

典型系统：

- 企业知识库 RAG
- 多租户 AI Chat
- Agent 知识助手
- Coding Agent Backend
- Long-running Agent Platform
- Multi-Agent Workflow
- AI Customer Service
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

# 13. Interview Reality：真实面经不是目录，而是验收标准

研究层：[`../research/README.md`](../research/README.md)

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

这是整个 Handbook 最重要的设计原则。

---

# 14. 当前建设状态

| 模块 | 当前状态 |
|---|---|
| Python | ✅ 已有完整 12 章 + Review + Interview |
| FastAPI | 🟡 已建立完整课程地图，下一步写正文 |
| AI Backend Engineering | 🟡 已建立完整课程地图，后续按项目穿插建设 |
| MySQL | ⏳ 下一块正式系统教材 |
| Redis | ⏳ MySQL 之后 |
| Vector DB | ⏳ Redis 之后 |
| RAG | ⏳ Vector DB 之后 |
| Agent Harness | 🔬 持续用 Claude Code / Codex + 面经校准后建设 |
| System Design | ⏳ 随各模块成熟逐步汇总 |
| 真实面经研究 | 🔄 持续滚动采集与去重 |
