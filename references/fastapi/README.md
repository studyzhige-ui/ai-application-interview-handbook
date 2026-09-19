# FastAPI｜官方技术资料索引

[← FastAPI](../../curriculum/02-fastapi/README.md) · [↑ Handbook 总目录](../../README.md) · [Market 首页](../../market/README.md)

> **用途：技术事实校准。** 官方资料只说明当前框架机制，不改变 HUMAN-A 面试频率。

---

更新日期：2026-09-11

> 本索引只负责 FastAPI 教材的**技术事实与版本校准**。市场频率仍只来自冻结 `S001–S279` HUMAN-A；官方文档不会创建 Canonical，也不会增加 Source Count。

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

当前需要特别注意的版本事实：

- 带 `yield` 的 Dependency 当前支持 `scope="function"` 与 `scope="request"`；
- 默认 request scope 围绕 Request/Response 生命周期；
- 相关 cleanup timing 历史上多次演进，因此教材不把旧版本行为写成永久规律。

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

当前官方 SSE 能力：

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
- ASGI concepts / server docs 以官方当前页面为准。

用于校准：

```text
ASGI Server role
Process / Worker boundary
Network ↔ ASGI Application
```

---

## 4. Pydantic

- Current Docs：https://docs.pydantic.dev/latest/

教材使用现代 Pydantic 心智模型：

```text
model_validate
model_dump
Runtime Validation
Serialization
JSON Schema
```

历史 Pydantic v1 API 只在兼容性语境出现，不作为当前唯一写法。

---

## 5. HUMAN-A 与权威资料怎样分工

```text
HUMAN-A FastAPI Canonical
→ 市场真实问法 / 追问深度

FastAPI / Starlette / Uvicorn / Pydantic Official Docs
→ 当前框架机制 / 版本事实

Curriculum
→ beginner-first 0→1 知识主干
```

三层不能混用。
