# FastAPI｜AI 应用服务层

> **Status：⏳ 课程骨架已完成，正式教材尚未撰写。** 当前仓库只有本 README/课程蓝图，尚无 `docs/`、`review/`、`interview/`。System Design 完成后回到 Foundation，FastAPI 是第一项正式补齐工作。详见 [`../roadmap/foundation-status-audit.md`](../roadmap/foundation-status-audit.md)。

> **FastAPI 在本手册中是一级模块，而不是 Python 的一个小附录。**
>
> 原因很简单：对 AI 应用 / Agent 开发岗位来说，Python 解决“语言怎么运行”，FastAPI 解决“怎样把模型、RAG、Agent、数据库和外部工具真正做成一个可被用户调用的服务”。

## 1. 这个模块到底要解决什么

学完 Python 后，很多人会卡在这里：

```text
会 Python
  ↓
会调 LLM API
  ↓
会写一个 RAG Demo
  ↓
？？？
  ↓
怎么做成真正的后端服务？
```

FastAPI 模块就是填上这个空白。

最终你应该能解释并实现：

```text
Client
  ↓ HTTP / SSE / WebSocket
FastAPI
  ↓
Request Validation
  ↓
Authentication / Dependency
  ↓
Service Layer
  ├─ LLM Provider
  ├─ RAG
  ├─ Agent Runtime
  ├─ MySQL
  ├─ Redis
  └─ Vector DB
  ↓
Streaming / JSON Response
```

但目标不是只背 FastAPI API，而是理解：

> **HTTP 请求进入 Python AI 服务后，到底经历了什么？为什么这里应该 async？为什么那里不能直接 BackgroundTasks？数据库连接什么时候创建和释放？LLM 流式输出怎么传给前端？客户端断开时任务怎么办？**

---

# 2. FastAPI 在总知识体系中的位置

```text
Python Foundation
        ↓
      FastAPI
        ↓
AI Backend Engineering
        ↓
┌────────┼─────────┐
↓        ↓         ↓
MySQL   Redis   Vector DB
│        │         │
└────────┼─────────┘
         ↓
        RAG
         ↓
   Agent Harness
```

三个容易混淆的模块要分清：

| 模块 | 主要回答的问题 |
|---|---|
| Python | 语言、对象、GIL、线程/进程/协程如何工作？ |
| FastAPI | 一个 Python HTTP/API 服务如何接收请求、校验、依赖注入、流式响应和部署？ |
| Backend Engineering | Timeout、Retry、Idempotency、MQ、Backpressure、Observability 等生产工程问题如何跨框架解决？ |
| Agent Harness | Agent Loop、Tool Runtime、Context、Memory、State、Permission、Checkpoint 等 Agent 专属运行时怎么设计？ |

---

# 3. 学习原则

FastAPI 也沿用整套手册的写法：

> **先讲人话 → HTTP/ASGI 原理 → 最小代码 → 请求生命周期 → 为什么 → AI 场景 → 生产边界 → 面试怎么答 → 真实面经 → 自测**

并坚持两个原则：

1. **先学 Web/Runtime 原理，再学装饰器 API。** 不能只会 `@app.get()`。
2. **FastAPI 只负责它该负责的层。** MQ、分布式任务、幂等、服务治理等问题会链接到 `backend-engineering/`，不强行说成 FastAPI 特性。

---

# 4. 第一版完整章节地图

## Part A｜从 Python 到 Web 服务

### 01. FastAPI 在 AI Application 中负责什么 ⭐⭐⭐⭐⭐

- API Service 是什么？
- 为什么 AI Demo 和 AI Service 是两回事？
- FastAPI、Starlette、ASGI Server 的关系先建立直觉
- 一个 `/chat` 请求从用户到 LLM 再返回经历什么？
- FastAPI 不负责什么？

### 02. HTTP 基础：Request / Response / Method / Status Code ⭐⭐⭐⭐⭐

- HTTP 请求结构
- GET / POST / PUT / PATCH / DELETE
- Header / Cookie / Body / Query / Path
- JSON
- 常见状态码
- REST API 基本设计
- AI 接口为什么常见 POST

### 03. WSGI、ASGI、Uvicorn 与 FastAPI 的关系 ⭐⭐⭐⭐⭐

- Web Server / Application / Protocol 分层
- 为什么现代异步 Python Web 常讨论 ASGI
- Uvicorn 做什么
- FastAPI 与 Starlette 的关系
- Request 生命周期的第一张总图

---

## Part B｜FastAPI 基础能力

### 04. App、Router 与 Path Operation ⭐⭐⭐⭐⭐

- `FastAPI()`
- `@app.get()` / `@app.post()`
- Router 拆分
- Path / Query / Header / Cookie
- 路由匹配的基本理解
- 大项目如何组织 Router

### 05. Python Type Hint 到请求参数校验 ⭐⭐⭐⭐⭐

- 类型注解为什么不只是 IDE 提示
- 请求参数提取
- Optional / Union / Annotated
- 校验错误
- OpenAPI / API Docs

### 06. Pydantic：AI 后端 Schema 的核心 ⭐⭐⭐⭐⭐

- `BaseModel`
- Request Model / Response Model
- Validation
- Nested Model
- 默认值与 Optional
- 自定义校验
- Serialization
- Tool Schema / Structured Output 为什么也离不开数据模型思想

### 07. Response Model 与序列化 ⭐⭐⭐⭐

- Python 对象怎么变成 HTTP Response
- response model 的意义
- 数据过滤
- JSON serialization
- 自定义 Response 什么时候需要

### 08. Exception Handling ⭐⭐⭐⭐

- HTTPException
- 业务异常与 HTTP 异常分层
- 全局异常处理
- Validation Error
- 不要把 Python 异常栈直接暴露给客户端
- AI Provider Error 如何映射成稳定 API Error

---

## Part C｜依赖注入与资源生命周期

### 09. Dependency Injection：`Depends` 到底解决什么 ⭐⭐⭐⭐⭐

- 依赖是什么
- Dependency Tree
- Sub-dependency
- Request-scoped resource
- 认证、数据库 Session、Service 如何复用
- 为什么 DI 不等于“为了高级而高级”

### 10. `yield` Dependency 与资源清理 ⭐⭐⭐⭐⭐

- 进入与退出
- `try/finally`
- 数据库 Session
- HTTP Client
- Trace Context
- Python 上下文管理器知识如何在这里重新出现

### 11. Application Lifespan ⭐⭐⭐⭐⭐

- 启动时初始化哪些资源
- 关闭时释放哪些资源
- DB Pool / Redis Pool / HTTP Client / Model Client
- 为什么不能每个 Request 都创建一个昂贵 Client
- Graceful Shutdown 的接口层基础

---

## Part D｜FastAPI 最重要的并发部分

### 12. `def` vs `async def` ⭐⭐⭐⭐⭐

这是 AI 应用岗非常重要的一章。

- `async def` 不是“自动更快”
- 可 await 的 I/O
- 同步阻塞库
- Thread Pool
- Event Loop
- FastAPI 中两种函数如何共存
- 如何识别 Blocking Call

### 13. asyncio Event Loop 再理解 ⭐⭐⭐⭐⭐

把 Python 模块的 asyncio 知识真正落到 Web 请求：

```text
Request A → await LLM
             ↓
Event Loop → Request B → await Redis
             ↓
Event Loop → Request C ...
```

- Task
- `create_task`
- `gather`
- Structured Concurrency 思想
- Exception Propagation
- Cancellation

### 14. Blocking I/O 与 CPU-bound 任务 ⭐⭐⭐⭐⭐

- `time.sleep()` 为什么会卡住 async endpoint
- 同步 SDK 怎么桥接
- CPU 密集 PDF/OCR/解析为什么可能拖死 Event Loop
- Thread Pool vs Process Pool
- 什么应该下沉到 Worker / MQ

### 15. 并发限制与资源保护 ⭐⭐⭐⭐⭐

- Semaphore
- Provider 并发限制
- DB Pool Size
- Redis / Vector DB Client Pool
- 防止“一次并发调用 100 个 Tool”
- Backpressure 的入口认识

---

## Part E｜AI 应用必须掌握的 Streaming

### 16. StreamingResponse ⭐⭐⭐⭐⭐

- 为什么不能等 LLM 全部生成后再返回
- Iterable / AsyncIterable
- `yield` 和流式 Response 的关系
- Chunked Streaming 的直觉
- 客户端断开
- Cancellation

### 17. Server-Sent Events（SSE）⭐⭐⭐⭐⭐

- SSE 是什么
- `text/event-stream`
- event / data / id / retry
- 为什么 AI Chat 特别适合 SSE
- 心跳
- 断线重连语义
- POST Streaming
- Token / Message / Tool Event 如何设计

### 18. WebSocket ⭐⭐⭐⭐

- 双向长连接
- SSE vs WebSocket
- Chat / Voice / Realtime / Agent Interaction
- Connection State
- Heartbeat
- 多实例部署后连接状态问题

### 19. AI Streaming Protocol Design ⭐⭐⭐⭐⭐

不是只会返回字符串，而是设计稳定事件：

```text
message_start
token_delta
tool_call_start
tool_call_delta
tool_result
state_update
error
message_end
```

这章会与 Agent Harness 的 Runtime Message Model 双向链接。

---

## Part F｜安全与认证

### 20. Middleware ⭐⭐⭐⭐

- Middleware 是什么
- Request/Response 横切逻辑
- Request ID
- Timing
- Access Log
- CORS
- Trace Context

### 21. Authentication ⭐⭐⭐⭐

- Identity
- Bearer Token
- JWT 基础
- Cookie Session 基础
- Current User Dependency

### 22. Authorization ⭐⭐⭐⭐⭐

- Authentication ≠ Authorization
- RBAC / Scope 基础
- Endpoint 权限
- Tenant Isolation
- Agent Tool Permission 为什么不能只靠 Prompt

### 23. CORS、输入安全与 Secret Boundary ⭐⭐⭐⭐

- CORS 到底解决什么
- 不可信输入
- Upload
- Secret / API Key
- 错误响应信息泄漏

---

## Part G｜数据库与外部系统

### 24. FastAPI + MySQL：Session / Pool / Transaction ⭐⭐⭐⭐⭐

这里不重复讲 B+Tree、MVCC；那些属于 `mysql/`。

这里只讲：

- Request 如何获得 DB Session
- Session 生命周期
- Connection Pool
- Transaction Boundary
- async DB Driver / sync Driver
- Timeout
- Rollback

### 25. FastAPI + Redis ⭐⭐⭐⭐⭐

- Redis Client 生命周期
- Cache
- Session
- Rate Limit
- Agent State
- Pub/Sub / Stream 的边界
- Redis 细节跳转 `redis/`

### 26. FastAPI + Vector DB / RAG ⭐⭐⭐⭐⭐

- Knowledge Base API
- Ingestion API
- Query API
- Retrieval Service
- Async Client
- Batch / Background Ingestion
- 大文件不能塞进普通 request lifecycle 做完

### 27. HTTP Client 与外部 LLM Provider ⭐⭐⭐⭐⭐

- 长连接 / Connection Pool
- Timeout
- Retry
- Streaming
- Provider Adapter
- API Key
- Rate Limit
- Client 生命周期

---

## Part H｜长任务、文件与生产边界

### 28. BackgroundTasks：能做什么，不能做什么 ⭐⭐⭐⭐⭐

- Response 后的小任务
- 为什么“后台”不等于可靠分布式任务
- 进程退出怎么办
- 重 CPU 任务怎么办
- 什么时候应该交给 MQ / Worker

### 29. 大文件 Upload 与流式处理 ⭐⭐⭐⭐

- Multipart
- UploadFile
- Streaming Read
- 内存风险
- 临时文件
- 分片上传
- RAG Ingestion

### 30. Timeout / Cancellation / Client Disconnect ⭐⭐⭐⭐⭐

- Request Timeout
- Downstream Timeout
- LLM Timeout
- Cancel Propagation
- Stream Disconnect
- Tool 取消
- 清理资源

### 31. Testing ⭐⭐⭐⭐

- API Test
- Dependency Override
- Mock Provider
- Async Test
- Streaming Test
- 错误路径
- Agent / RAG Integration Test

### 32. Logging / Trace / Metrics ⭐⭐⭐⭐⭐

- Access Log vs Application Log
- Request ID / Trace ID
- Structured Log
- Latency Breakdown
- LLM / RAG / Tool Span
- Token / Cost
- OpenTelemetry 思想

### 33. Deployment：Process / Worker / Container ⭐⭐⭐⭐⭐

- Development Server vs Production Server
- Worker Process
- 多核利用
- 每进程内存
- Docker
- Kubernetes 下的进程/副本思路
- Graceful Shutdown
- Health Check

### 34. FastAPI Performance Debugging ⭐⭐⭐⭐⭐

- P50 / P95 / P99
- Event Loop Block
- Connection Pool Exhaustion
- Thread Pool Exhaustion
- DB / Redis / Provider Latency
- Serialization Cost
- Streaming 首 Token 延迟
- Queueing Delay

---

## Part I｜AI / Agent 综合实战

### 35. 设计 `/chat` LLM Streaming API ⭐⭐⭐⭐⭐

### 36. 设计 RAG Query API ⭐⭐⭐⭐⭐

### 37. 设计知识库 Ingestion API ⭐⭐⭐⭐⭐

### 38. 设计 Agent Run API ⭐⭐⭐⭐⭐

### 39. 设计 Agent SSE Event Protocol ⭐⭐⭐⭐⭐

### 40. 设计 Long-running Agent Task API ⭐⭐⭐⭐⭐

最终把：

```text
FastAPI
+ MySQL
+ Redis
+ Vector DB
+ RAG
+ Agent Harness
```

真正串起来。

---

# 5. FastAPI 与真实面试怎么结合

研究库已经出现以下类型问题：

- FastAPI URL Routing / Async Runtime；
- Python async 与 CPU-bound 隔离；
- SSE vs WebSocket；
- Agent Streaming；
- 多 Tool 并发；
- Timeout / Retry / Cancellation；
- Session / Message / State 持久化；
- 大文件流式处理；
- 多用户隔离；
- 200ms 级 SLA；
- LLM / Tool / RAG Trace。

因此 FastAPI 课程不会停在 CRUD Tutorial，而会一直走到 **AI Service Runtime**。

---

# 6. 官方资料基线

后续正式写章节时，以官方文档作为当前版本事实基线，并结合真实面经决定讲解优先级：

- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- Concurrency / async-await: https://fastapi.tiangolo.com/async/
- Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
- Streaming: https://fastapi.tiangolo.com/advanced/stream-data/
- SSE: https://fastapi.tiangolo.com/tutorial/server-sent-events/
- Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- Deployment / Workers: https://fastapi.tiangolo.com/deployment/server-workers/
- Pydantic: https://docs.pydantic.dev/latest/

> 具体 API 会随版本演进，因此教材正文不会把某个历史版本细节写成永久不变的框架规律。

---

# 7. 学完 FastAPI 后应该达到什么水平

不是：

> “我会写 `@app.post('/chat')`。”

而是能回答：

1. 一个请求进入 FastAPI 后经历什么？
2. `def` / `async def` 怎么选？
3. 为什么同步阻塞 SDK 会拖慢异步服务？
4. 如何做 LLM Streaming / SSE？
5. 客户端断开后 Agent 应不应该继续执行？
6. 数据库连接什么时候获取和释放？
7. 为什么不能每个请求创建一个新 HTTP Client？
8. BackgroundTasks 为什么不能代替可靠任务队列？
9. 大文件 / OCR / Embedding 为什么不能无脑塞在请求线程里？
10. 如何定位一个 FastAPI AI 服务 P99 突然变高？
11. Agent Runtime 和 FastAPI 的职责边界是什么？
12. 多用户 Agent 如何在 API、State、Redis、数据库层共同隔离？

当这些问题都能从原理、代码和工程权衡三个层次回答时，FastAPI 才真正学完。

## 下一层

FastAPI 学的是“服务框架”。接下来还需要：

> [AI Backend Engineering](../backend-engineering/README.md)

把可靠任务、Timeout、Retry、Idempotency、MQ、Backpressure、Observability 等跨框架生产能力补齐。
