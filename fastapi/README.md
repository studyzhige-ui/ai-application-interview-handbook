# FastAPI｜AI 应用服务层

> **Status：✅ 第一版完整系统教材已完成。** 当前为 `16` 个连续知识小板块 + Review + Interview 三件套；4 道 FastAPI HUMAN-A Canonical 已完成 Coverage / Depth 映射。课程主干由 beginner-first Web/API 知识依赖决定，真人面经只校准真实问法、边界和追问深度。

FastAPI 在本手册中是一级模块，而不是 Python 的附录。

Python 解决：

```text
对象 / 类型 / 函数 / GIL / asyncio 怎么工作
```

FastAPI 解决：

```text
这些 Python Runtime 能力怎样变成一个可被客户端调用、可 Streaming、可验证、可部署的 AI Service
```

---

## 1. FastAPI 在总知识体系中的位置

```text
Python Foundation
        ↓
FastAPI
        ↓
AI Backend Engineering
        ↓
MySQL / Redis / Vector DB
        ↓
LLM / RAG / Agent Harness
        ↓
System Design
```

模块边界：

| 模块 | 主要回答的问题 |
|---|---|
| Python | Event Loop、Thread/Process、对象与语言 Runtime 怎样工作？ |
| **FastAPI** | HTTP/ASGI 请求怎样进入 Python Service；Validation、DI、Resource、Streaming 怎样组织？ |
| AI Backend Engineering | Timeout、Retry、Idempotency、MQ、Backpressure、跨服务可靠性怎样系统解决？ |
| Agent Harness | Loop、Tool、Context、Memory、Checkpoint、Permission 等 Agent Runtime 怎样工作？ |

---

## 2. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

FastAPI 当前只有 4 道 Primary Canonical，但不能因此只写四篇面试题；同样，旧 README 的 40 个小标题也不能机械变成 40 个文件。

最终教材粒度是：

```text
4 Canonical Questions
+ 完整 Web Service 前置
+ 官方 FastAPI / Starlette / Pydantic / Uvicorn 机制
↓
16 个完整知识小板块
```

---

## 3. 真人面经怎样影响本模块

冻结 `S001–S279` 中 FastAPI Primary Canonical：

```text
FASTAPI-001  ASGI / Request Lifecycle
FASTAPI-002  Middleware vs Dependency
FASTAPI-004  FastAPI + SSE / Agent Streaming
FASTAPI-005  Framework Boundary / Agent Service
```

它们没有决定教材顺序，但直接要求这些区域必须讲深：

- `01` 必须能解释 Uvicorn / ASGI / FastAPI 请求链；
- `04` 必须真正比较 Middleware / Dependency，而不是分别背定义；
- `07` 必须把 SSE 写成稳定 Event Protocol，并讲中途错误 / Disconnect；
- `16` 必须能解释为什么只会 CRUD 不足以承载 Production Agent Service。

Python async 的底层语义仍归 `PY-012`，FastAPI 只讲框架如何执行 `def / async def`。

---

## 4. 权威技术资料怎样使用

正式教材同时参考当前官方资料：

- FastAPI Tutorial / Advanced Guide / Reference；
- Starlette Web/ASGI primitives；
- Uvicorn ASGI / deployment docs；
- Pydantic current docs。

它们只负责校准当前框架机制和版本事实，**不增加 HUMAN-A Source Count**。

来源索引：[`../research/fastapi-sources/README.md`](../research/fastapi-sources/README.md)

特别提醒：FastAPI 的 `yield` Dependency cleanup timing、SSE API 等能力历史上有过版本演进，因此教材会区分“稳定概念”和“当前官方实现”。

---

# 5. 正式 16 个知识小板块

## Part A｜从 Python 到 ASGI Service

1. [FastAPI 的职责：HTTP → ASGI → Application Request Lifecycle](docs/01-FastAPI职责与ASGI请求链路.md)
2. [Routing、Request / Response 与 OpenAPI Contract](docs/02-Routing与APIContract.md)
3. [Pydantic、Validation、Serialization 与 Error Contract](docs/03-Pydantic与数据契约.md)
4. [Dependency Injection 与 Middleware](docs/04-Dependency与Middleware.md)
5. [Resource Lifecycle：yield Dependency、scope 与 Lifespan](docs/05-ResourceLifecycle.md)
6. [Async Execution：def / async def、Blocking Boundary 与并发保护](docs/06-AsyncExecution与BlockingBoundary.md)

## Part B｜AI Service Transport

7. [Streaming Fundamentals 与 Server-Sent Events（SSE）](docs/07-Streaming与SSE.md)
8. [WebSocket 与 AI Event Protocol](docs/08-WebSocket与EventProtocol.md)
9. [Authentication、Authorization、CORS 与 Tenant Context](docs/09-Security与TenantContext.md)

## Part C｜外部系统、任务与可靠请求生命周期

10. [DB、Redis、Vector DB 与 LLM Client 集成](docs/10-ExternalResourceIntegration.md)
11. [BackgroundTasks、文件上传与 Long-running Task Boundary](docs/11-BackgroundTask与Upload.md)
12. [Timeout、Cancellation、Client Disconnect 与 Cleanup](docs/12-TimeoutCancellation与Disconnect.md)

## Part D｜Production FastAPI

13. [Testing：Dependency Override、Streaming、WebSocket 与错误路径](docs/13-Testing.md)
14. [Logging、Trace、Metrics 与性能诊断](docs/14-Observability与Performance.md)
15. [Deployment：Worker、Health Check 与 Graceful Shutdown](docs/15-Deployment与GracefulShutdown.md)
16. [AI Service Patterns：Chat、RAG、Ingestion 与 Agent Run API](docs/16-AIServicePatterns.md)

---

## 6. 4 道 Canonical → 16-block 的映射

```text
FASTAPI-001  ASGI / Request Lifecycle       → 01 / 02 / 05
FASTAPI-002  Middleware vs Dependency       → 04 / 05 / 09
FASTAPI-004  SSE / Agent Streaming          → 07 / 08 / 12 / 16
FASTAPI-005  Agent Service Framework Boundary→ 05–16，重点 16
```

这不是 Coverage 凑数。FastAPI 的 4 道真人问题是**市场校准信号**，完整教材还必须保留 HTTP Contract、Validation、Testing、Deployment 等低频但必要的基础。

---

## 7. 三条最重要的知识主线

### 主线 A｜Request / Resource Lifecycle

```text
ASGI Server
→ Middleware
→ Router
→ Validation / Dependency
→ Handler
→ Response
→ Cleanup
```

### 主线 B｜Async / Streaming

```text
async def / def
→ Event Loop / Thread Pool
→ Blocking Boundary
→ StreamingResponse
→ SSE / WebSocket
→ Cancellation / Disconnect
```

### 主线 C｜AI Service Boundary

```text
FastAPI API Layer
→ Service Layer
→ RAG / Agent Runtime / Provider Adapter
→ Durable State / Queue / Worker
```

---

## 8. 本模块必须会回答的问题

学完后至少能清晰解释：

1. Uvicorn / Starlette / FastAPI / Pydantic 的职责边界；
2. 一个请求为什么会经过 Middleware / Dependency；
3. `yield` Dependency 和 Lifespan 管不同什么资源；
4. `def` 与 `async def` 在 FastAPI 中怎样执行；
5. 为什么同步 helper 会堵 async Endpoint；
6. SSE / WebSocket 怎样选；
7. Stream 中途失败和 Client Disconnect 怎么处理；
8. 为什么 BackgroundTasks 不能做 Durable RAG Ingestion；
9. DB/Redis/LLM Client 应该怎样管理生命周期；
10. 多 Worker 后为什么不能依赖进程全局 State；
11. 怎样测试 Dependency、Streaming 和 Provider Failure；
12. `/agent/runs` 为什么比一个 `/chat` 更接近 Production Agent Service。

---

## 9. 推荐学习方式

第一遍：按 `01 → 16` 建立因果链。

第二遍：进入 [`review/README.md`](review/README.md)，不看正文重新画六张总图。

第三遍：使用：

- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

目标不是“会写 FastAPI”，而是：

> **能把 Python Runtime 正确映射成 Production AI Service，同时知道哪些问题不属于 FastAPI。**

---

## 10. 下一环：AI Backend Engineering

FastAPI 完成后，下一层正式进入：

```text
Timeout Budget
Retry / Jitter
Idempotency
Backpressure
Queue / Worker
Cache Consistency
Rate Limit
Distributed Trace
Deployment Reliability
```

入口：[`../backend-engineering/README.md`](../backend-engineering/README.md)
