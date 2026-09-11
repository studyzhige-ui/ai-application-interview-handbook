# AI Backend Engineering｜AI 应用后端工程基础

> **Status：⏳ 课程骨架已完成，正式教材尚未撰写。** 当前仓库只有本 README/课程蓝图，尚无 `docs/`、`review/`、`interview/`。System Design 已完成，后续在 FastAPI 正文之后正式建设这一横向 Production 主线。详见 [`../roadmap/foundation-status-audit.md`](../roadmap/foundation-status-audit.md)。

> 这是整套手册里的**横向工程主线**。
>
> FastAPI 教你如何把 Python 程序做成服务；MySQL / Redis / Vector DB 教你不同数据系统；RAG / Agent Harness 教你 AI 应用层能力。**AI Backend Engineering 负责把这些东西在生产环境里可靠地连接起来。**

## 1. 为什么必须单独有这一环

很多 AI 项目 Demo 是这样的：

```text
用户请求
  ↓
FastAPI
  ↓
LLM
  ↓
返回答案
```

真实系统则更像：

```text
                         ┌──────── MySQL
                         │
Client → Gateway/API → Service → Redis
            │            │
            │            ├──────── Vector DB
            │            │
            │            ├──────── LLM Provider
            │            │
            │            └──────── External Tools
            │
            ├─ Timeout
            ├─ Retry
            ├─ Rate Limit
            ├─ Auth
            ├─ Idempotency
            ├─ Queue / Backpressure
            ├─ Trace / Metrics
            └─ Cancellation
```

面试官问“挂了怎么办、量大怎么办、超时怎么办、重复执行怎么办”时，真正考的往往就是这一层。

---

# 2. 与其他模块的边界

| 模块 | 核心职责 |
|---|---|
| Python | 语言与运行时基础 |
| FastAPI | HTTP / ASGI 服务框架与请求生命周期 |
| MySQL | 结构化持久化、事务、索引、锁 |
| Redis | 缓存、短期状态、高频访问数据 |
| Vector DB | 向量检索与 ANN |
| RAG | 知识检索与生成链路 |
| Agent Harness | Agent Loop、Tool、Context、Memory、State 等 Agent 专属 Runtime |
| **AI Backend Engineering** | 可靠性、并发、异步任务、网络、队列、限流、幂等、可观测性、部署等跨模块工程能力 |

它不是“另一本后端八股”，而是专门围绕 AI 服务的真实工程问题组织。

---

# 3. 第一版完整章节地图

## Part A｜网络与服务基础

### 01. 一个 AI 后端请求到底经历什么 ⭐⭐⭐⭐⭐
- Client / DNS / TCP / TLS / HTTP
- Reverse Proxy / Gateway
- Application Server
- Service / Data / Model
- Response / Streaming

### 02. HTTP / REST API 设计 ⭐⭐⭐⭐⭐
- Method / Status Code
- Header / Body
- Idempotent Method 的概念
- API Version
- Pagination
- Error Contract

### 03. TCP、连接与 Keep-Alive ⭐⭐⭐⭐
- 为什么连接建立有成本
- Connection Reuse
- Long-lived Connection
- AI Streaming 对连接生命周期的影响

### 04. SSE / WebSocket /普通 HTTP 如何选 ⭐⭐⭐⭐⭐
- 单向流 / 双向流
- AI Chat
- Realtime Agent
- Disconnect / Resume

---

## Part B｜并发与资源模型

### 05. Concurrency vs Parallelism ⭐⭐⭐⭐⭐
- I/O-bound
- CPU-bound
- Thread / Process / Coroutine
- 为什么“并发高”不等于“线程越多越好”

### 06. Event Loop 与 Blocking Call ⭐⭐⭐⭐⭐
- async Runtime
- 阻塞污染
- Event Loop Lag
- 同步 SDK 桥接

### 07. Thread Pool / Process Pool ⭐⭐⭐⭐⭐
- Blocking I/O offload
- CPU-heavy parsing
- Process serialization cost
- Pool saturation

### 08. Connection Pool ⭐⭐⭐⭐⭐
- DB Pool
- HTTP Pool
- Redis Pool
- Pool Size
- Pool Exhaustion
- Connection Leak

### 09. Concurrency Limit / Semaphore ⭐⭐⭐⭐⭐
- 为什么不能无限并发调 LLM / Tool
- Provider Rate Limit
- DB Capacity
- Per-tenant Limit

### 10. Backpressure ⭐⭐⭐⭐⭐
- 上游快、下游慢
- Queue Growth
- Reject / Shed / Buffer
- Streaming Backpressure

---

## Part C｜Timeout、Retry 与错误语义

### 11. Timeout Budget ⭐⭐⭐⭐⭐
- Connect Timeout
- Read Timeout
- Request Timeout
- End-to-end Deadline
- 子调用预算

### 12. Error Taxonomy ⭐⭐⭐⭐⭐
- Transient Error
- Permanent Error
- Validation Error
- Permission Error
- Business Rejection
- Rate Limit

### 13. Retry ⭐⭐⭐⭐⭐
- 什么错误能重试
- Exponential Backoff
- Jitter
- Retry Storm
- Retry Budget

### 14. Circuit Breaker / Degradation ⭐⭐⭐⭐⭐
- Open / Half-open / Closed
- Model Provider Failover
- Tool Failover
- Graceful Degradation

### 15. Cancellation Propagation ⭐⭐⭐⭐⭐
- 用户取消
- HTTP disconnect
- Child Task
- LLM Stream
- Tool / DB / External Request
- Cleanup

---

## Part D｜幂等与一致性

### 16. Idempotency ⭐⭐⭐⭐⭐
- 为什么 AI Tool 重试特别危险
- Idempotency Key
- Duplicate Request
- Duplicate Message
- Result Reuse

### 17. Optimistic / Pessimistic Concurrency Control ⭐⭐⭐⭐
- CAS
- Version
- Row Lock
- Redis Lock
- 什么时候不应该上分布式锁

### 18. Distributed Lock 与 Lease ⭐⭐⭐⭐⭐
- Lock Ownership
- TTL
- WatchDog
- Fencing Token
- 业务超时与锁超时

### 19. 最终一致性 ⭐⭐⭐⭐⭐
- Cache / DB
- Async Workflow
- Reconciliation
- Compensation

### 20. Saga / Compensation ⭐⭐⭐⭐⭐
- 跨 Tool 部分成功
- Rollback 为什么常常做不到
- Compensating Action
- Agent Workflow 的副作用语义

---

## Part E｜MQ 与可靠异步任务

### 21. 为什么需要消息队列 ⭐⭐⭐⭐⭐
- 解耦
- 削峰
- 异步
- Buffer
- 失败重试

### 22. Kafka / RabbitMQ / Redis Stream 的基础差异 ⭐⭐⭐⭐
- 持久化
- Consumer Model
- Ack / Offset
- Replay
- Ordering

### 23. Reliable Task Pattern ⭐⭐⭐⭐⭐

```text
DB Task Record
    ↓
MQ carries task_id
    ↓
Worker claims task
    ↓
Heartbeat / Lease
    ↓
Result persisted
```

- DB 状态机
- MQ
- Idempotency Token
- Outbox 思想

### 24. Lease / Heartbeat / Worker Recovery ⭐⭐⭐⭐⭐
- Worker 宕机
- Task Claim
- Lease Expiration
- Reclaim
- Duplicate Execution

### 25. Long-running Task API ⭐⭐⭐⭐⭐
- 202 Accepted
- task_id
- polling / SSE
- cancel
- resume
- status machine

---

## Part F｜缓存与限流

### 26. Cache Aside ⭐⭐⭐⭐⭐
- Read Path
- Write Path
- Cache Miss
- Invalidation

### 27. Cache Consistency ⭐⭐⭐⭐⭐
- 先删缓存还是先写 DB
- 延迟双删为什么不是万能答案
- CDC / Event-driven 思路

### 28. Cache Penetration / Breakdown / Avalanche ⭐⭐⭐⭐⭐
- 穿透
- 击穿
- 雪崩
- AI 场景中的 Semantic / Prompt Cache

### 29. HotKey / BigKey ⭐⭐⭐⭐⭐
- 热点访问
- 大 Value / 大 Collection
- Local Cache
- Sharding
- Request Coalescing

### 30. Rate Limiting ⭐⭐⭐⭐⭐
- Fixed Window
- Sliding Window
- Token Bucket
- Leaky Bucket
- Distributed Rate Limit
- User / Tenant / API Key / Model 限流

---

## Part G｜文件与数据管道

### 31. 大文件流式处理 ⭐⭐⭐⭐⭐
- 为什么不能一次 `read()`
- Stream
- Chunk
- Hash / Dedup
- Temp File
- Memory Bound

### 32. Multipart / Chunked Upload / Resume ⭐⭐⭐⭐
- Upload ID
- Part Number
- Checksum
- Merge
- Idempotency

### 33. AI Ingestion Pipeline ⭐⭐⭐⭐⭐
- Upload
- Parse
- OCR
- Chunk
- Embedding
- Index
- Async Status
- Failure Recovery

---

## Part H｜可观测性

### 34. Structured Logging ⭐⭐⭐⭐⭐
- JSON Log
- request_id
- user / tenant
- task_id
- error_type

### 35. Distributed Trace ⭐⭐⭐⭐⭐
- Trace / Span
- Parent / Child
- Model Span
- Retrieval Span
- Tool Span
- DB Span

### 36. Metrics ⭐⭐⭐⭐⭐
- QPS
- Error Rate
- P50 / P95 / P99
- Queue Depth
- Pool Usage
- Token / Cost
- Time to First Token

### 37. AI-specific Observability ⭐⭐⭐⭐⭐
- Prompt / Model Version
- Retrieval Evidence
- Tool Trace
- Token Usage
- Cost
- User Feedback
- Bad Case

### 38. Performance Regression Debugging ⭐⭐⭐⭐⭐
- 为什么平均延迟不够
- Bottleneck Attribution
- Model / Tool / Retrieval / DB / Queue / Network

---

## Part I｜安全

### 39. Authentication / Authorization ⭐⭐⭐⭐⭐
- Identity
- Scope
- RBAC / ABAC
- Least Privilege

### 40. Multi-tenant Isolation ⭐⭐⭐⭐⭐
- Tenant ID
- Data Isolation
- Cache Key
- Agent State
- Vector Filter

### 41. Secret Management ⭐⭐⭐⭐
- API Key
- Environment
- Secret Store
- Log Redaction

### 42. Input / Output Boundary ⭐⭐⭐⭐⭐
- Prompt Injection 不只是 Prompt 问题
- Tool Input Validation
- Output Sanitization
- Sensitive Data

---

## Part J｜部署与运行

### 43. Process Model / Worker ⭐⭐⭐⭐⭐
- 一个服务几个进程
- 每进程资源
- 多核
- Memory Duplication

### 44. Docker 基础 ⭐⭐⭐⭐
- Image
- Container
- Env
- Volume
- Network
- Healthcheck

### 45. Graceful Shutdown ⭐⭐⭐⭐⭐
- 停止接新请求
- 等待 in-flight
- Cancel / Drain
- 关闭连接池
- Worker Termination

### 46. Health Check / Readiness / Liveness ⭐⭐⭐⭐

### 47. Horizontal Scaling ⭐⭐⭐⭐⭐
- Stateless API
- State externalization
- Session affinity 的边界
- Redis / DB / MQ 成为共享层

### 48. Config / Feature Flag / Gray Release ⭐⭐⭐⭐
- Dynamic Config
- Version
- Rollback
- Model / Prompt 灰度

---

## Part K｜AI Backend 综合系统设计

### 49. 高并发 LLM Gateway
### 50. RAG Service
### 51. Knowledge Ingestion Platform
### 52. Agent Task Platform
### 53. Multi-tenant AI SaaS
### 54. Model Provider Failover Gateway
### 55. AI Chat Streaming Backend

每个系统设计都要求回答：

```text
数据在哪里？
状态在哪里？
谁拥有事务？
什么可以重试？
什么不能重复？
哪里会阻塞？
哪里会积压？
怎么限流？
怎么超时？
怎么恢复？
怎么观测？
怎么扩容？
怎么保证权限？
```

---

# 4. 与真实面经的关系

目前 2026 高质量面经已经反复出现：

- SSE / WebSocket；
- async / thread / process；
- MQ 与可靠任务；
- Lease / Heartbeat；
- Redis Lock / HotKey；
- MySQL 并发与一致性；
- 200ms SLA；
- Timeout / Retry / Failover；
- 大文件流式处理；
- Agent 并发、取消、恢复；
- Trace / P95 / P99；
- 多租户 Context / State 隔离。

因此这一模块不是额外扩展，而是 AI 应用开发岗位真正的工程底座。

---

# 5. 怎么学习才不会变成另一本“后端大全”

推荐采用“纵向知识 + 横向项目”的方式：

```text
Python async
   ↓
FastAPI Streaming
   ↓
Timeout / Cancellation
   ↓
Redis State
   ↓
MQ Long Task
   ↓
Agent Runtime
```

每学一个主题，都放回一个 AI 项目里理解。

例如学 **Idempotency** 时，不只背定义，而是回答：

> Agent 调支付 Tool 超时，实际上支付成功了，但客户端没收到结果。Runtime 重试会不会扣两次钱？

学 **Backpressure** 时回答：

> 1000 个用户同时要求 Agent 并发调用 10 个 Tool，下游 Provider 只能承受 200 QPS，系统怎么退让？

这才是这个模块的目标。

## 相关模块

- [Python Foundation](../python/README.md)
- [FastAPI](../fastapi/README.md)
- MySQL（后续建设）
- Redis（后续建设）
- Vector DB（后续建设）
- RAG（后续建设）
- Agent Harness（后续建设）
