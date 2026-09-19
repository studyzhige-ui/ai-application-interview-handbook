# FastAPI｜官方技术资料索引

[← FastAPI](../../curriculum/02-fastapi/README.md) · [↑ Handbook 总目录](../../README.md) · [Market 首页](../../market/README.md)

> **用途：技术事实与版本校准。** 官方资料说明框架机制与版本边界，不改变 HUMAN-A 面试频率。

---

资料核验日期：2026-09-11

> 本索引负责 FastAPI 教材的**技术事实与版本校准**。HUMAN-A 频率统计基线为 `S001–S279`；官方文档不会创建 Canonical，也不会增加 Source Count。

---

## 1. FastAPI 官方

### Request / Body / Validation

- Request Body：https://fastapi.tiangolo.com/tutorial/body/
- Response Model：https://fastapi.tiangolo.com/tutorial/response-model/
- Handling Errors：https://fastapi.tiangolo.com/tutorial/handling-errors/

用于校准：

```text
Pydantic Request Model
Runtime Validation
OpenAPI Schema
Response Validation / Filtering
RequestValidationError
```

### Dependency / Lifecycle

- Dependencies：https://fastapi.tiangolo.com/tutorial/dependencies/
- Dependencies with yield：https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- Advanced Dependencies：https://fastapi.tiangolo.com/advanced/advanced-dependencies/
- Lifespan Events：https://fastapi.tiangolo.com/advanced/events/

版本敏感事实：

- 在核验版本中，带 `yield` 的 Dependency 支持 `scope="function"` 与 `scope="request"`；
- 默认 request scope 围绕 Request/Response 生命周期；
- cleanup timing 属于版本敏感行为，教材不把单一版本行为写成永久规律。

### Async

- Concurrency and async / await：https://fastapi.tiangolo.com/async/

用于校准：

```text
async def path operation → directly awaited
normal def path operation / dependency → external thread pool
ordinary sync helper directly called inside async def → not automatically offloaded by FastAPI
```

### Streaming / SSE / WebSocket

- SSE Tutorial：https://fastapi.tiangolo.com/tutorial/server-sent-events/
- SSE Reference：https://fastapi.tiangolo.com/reference/sse/
- WebSockets：https://fastapi.tiangolo.com/advanced/websockets/

核验版本的官方 SSE 能力：

- `fastapi.sse.EventSourceResponse`
- `fastapi.sse.ServerSentEvent`
- SSE 可用于不同 HTTP 方法，包括 POST；
- 官方实现包含 keep-alive / cache / proxy buffering 相关最佳实践。

### Middleware / Background / Upload

- Middleware：https://fastapi.tiangolo.com/tutorial/middleware/
- Background Tasks：https://fastapi.tiangolo.com/tutorial/background-tasks/
- Request Files：https://fastapi.tiangolo.com/tutorial/request-files/

关键边界：

```text
BackgroundTasks = response 后的应用进程内任务
heavy / multi-process / multi-server background work → 更适合独立任务系统

bytes file → whole content in memory
UploadFile → spooled temporary file / file-like interface
```

### Testing

- Testing：https://fastapi.tiangolo.com/tutorial/testing/
- Testing Dependencies with Overrides：https://fastapi.tiangolo.com/advanced/testing-dependencies/
- Testing WebSockets：https://fastapi.tiangolo.com/advanced/testing-websockets/

用于校准：

```text
TestClient
app.dependency_overrides
WebSocket test
```

---

## 2. Starlette

FastAPI Web/ASGI 基础大量来自 Starlette：

- Documentation：https://www.starlette.io/
- Middleware：https://www.starlette.io/middleware/

主要用于理解：

```text
Request / Response
Routing
Middleware
WebSocket
Background Task
ASGI Web primitives
```

教材不会把 Starlette 内部所有实现细节复制成 FastAPI 课程。

---

## 3. Uvicorn

- Documentation：https://www.uvicorn.org/
- ASGI concepts / server 行为以对应版本的官方文档为准。

用于校准：

```text
ASGI Server role
Process / Worker boundary
Network ↔ ASGI Application
```

---

## 4. Pydantic

- Documentation：https://docs.pydantic.dev/latest/

教材使用现代 Pydantic 心智模型：

```text
model_validate
model_dump
Runtime Validation
Serialization
JSON Schema
```

Pydantic v1 API 只在兼容性语境出现，不作为默认教学写法。

---

## 5. HUMAN-A 与权威资料怎样分工

```text
HUMAN-A FastAPI Canonical
→ 市场真实问法 / 追问深度

FastAPI / Starlette / Uvicorn / Pydantic Official Docs
→ 框架机制 / 版本事实

Curriculum
→ beginner-first 0→1 知识主干
```

三层不能混用。
