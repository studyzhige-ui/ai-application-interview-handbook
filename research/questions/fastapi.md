# FastAPI Canonical Questions — S001–S279 全库纵向扫描 v2

更新日期：2026-09-10

> 一级板块：**FastAPI**。本文件只记录 FastAPI / ASGI 框架层真人问题。HTTP / SSE / WebSocket 协议原理归 `AI Backend Engineering`；Python `asyncio` 语言与 Runtime 语义归 `Python`；Agent State / Tool / Checkpoint 归 `Agent`。
>
> 本文件所有 ACTIVE 条目的 `Primary Module = FastAPI`。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**4**
- MOVED：**1**（旧 `FASTAPI-003`）
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数
- 当前版本：`v2`（十板块归属审计版）

FastAPI 在冻结面经中的独立出现频率不高，但出现时并不是只问路由装饰器，而是直接下钻到 ASGI、Middleware / Dependency、异步调用边界和 Agent Streaming。

---

## 2. ACTIVE Canonical Questions

### FASTAPI-001 · FastAPI 的请求链路怎样工作？ASGI、Web Server 与 Application Framework 各自承担什么职责？

- **Primary Module**：FastAPI
- **Related Modules**：Python, AI Backend Engineering
- **Topic**：ASGI / Request Lifecycle
- **Question Type**：Concept / Deep Dive
- **Language / Ecosystem**：FastAPI / ASGI
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S238`

**真实问法变体：**
- FastAPI 底层 Web Server / ASGI 组件是什么？
- 一个请求从 Server 到 FastAPI Handler 的调用链怎样理解？

### FASTAPI-002 · FastAPI Middleware 与 Dependency Injection 有什么差异？认证、日志、公共上下文等横切逻辑应放在哪里？

- **Primary Module**：FastAPI
- **Related Modules**：AI Backend Engineering
- **Topic**：Middleware / Dependency
- **Question Type**：Comparison / Trade-off
- **Language / Ecosystem**：FastAPI
- **Depth**：L3
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S064`

### FASTAPI-004 · FastAPI + SSE 怎样把 Agent / LangGraph 的中间事件实时推送到前端？

- **Primary Module**：FastAPI
- **Related Modules**：AI Backend Engineering, Agent
- **Topic**：Streaming Endpoint
- **Question Type**：System Design / Implementation
- **Language / Ecosystem**：FastAPI / SSE / LangGraph
- **Depth**：L3
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S087`

### FASTAPI-005 · 只会 FastAPI GET / POST 为什么不足以构建 Claude Code 类 Agent Service？FastAPI 层还需要怎样承接 Streaming、Session 与 Runtime 状态？

- **Primary Module**：FastAPI
- **Related Modules**：AI Backend Engineering, Agent, System Design
- **Topic**：Framework Boundary
- **Question Type**：Comparison / System Design
- **Language / Ecosystem**：FastAPI
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S238`

---

## 3. MOVED：新十板块归属修正

| Legacy QID | 原问题 | 新 Primary Canonical |
|---|---|---|
| `FASTAPI-003` | FastAPI 异步调用 LLM 时，`await` 等待期间 Event Loop、CPU 和线程分别在做什么？ | `PY-012`（Python `asyncio` Runtime 语义）；FastAPI 仅作为 Related Module |

这类问题虽然出现在 FastAPI 面试语境中，但核心知识模型是 Python `asyncio` / Event Loop，因此不应在两个一级板块各维护一份 Canonical Question。

---

## 4. 对课程结构的直接信号

FastAPI 不应该被写成独立 Web 框架 API 手册。更合理的学习链是：

```text
Python async / iterator / context manager
        ↓
ASGI / FastAPI Request Lifecycle
        ↓
Middleware / Dependency / Validation
        ↓
Async LLM Call
        ↓
SSE / Streaming
        ↓
AI Backend Engineering
        ↓
Agent Runtime
```

也就是说，FastAPI 在新体系里承担“从 Python 语言进入 AI Service 工程”的桥梁角色。
