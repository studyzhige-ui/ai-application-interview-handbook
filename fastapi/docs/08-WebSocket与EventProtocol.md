# 08｜WebSocket 与 AI Event Protocol

SSE 很适合“Server 持续推结果给 Client”，但有些 AI 场景是持续双向交互：

- Realtime Voice；
- 游戏 / Interactive Agent；
- 多人协作；
- 用户在生成过程中不断发送控制指令；
- 双向状态同步。

这时需要理解 WebSocket。

---

## 1. WebSocket 的核心模型

普通 HTTP 常见：

```text
Request
→ Response
→ connection may remain reusable
```

WebSocket 更像：

```text
Handshake
→ persistent bidirectional connection
→ client/server both send messages
→ disconnect
```

FastAPI / Starlette 会把底层 ASGI WebSocket 事件封装成 `WebSocket` 对象。

---

## 2. 最小 WebSocket Endpoint

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            message = await ws.receive_text()
            await ws.send_text(f"echo: {message}")
    except WebSocketDisconnect:
        pass
```

这只是协议入门，不是 Production 架构。

---

## 3. SSE vs WebSocket 怎么选

| 问题 | SSE | WebSocket |
|---|---|---|
| 主要方向 | Server → Client | 双向 |
| 协议复杂度 | 较低 | 更高 |
| 浏览器原生消费 | 很自然 | 很自然 |
| 普通 AI Chat Token | 很适合 | 能做但常没必要 |
| Realtime Voice / 控制 | 不适合强双向 | 更适合 |
| 重连语义 | HTTP/SSE 思维 | 需设计连接状态 |

选择标准应该是通信需求，不是“WebSocket 更酷”。

---

## 4. WebSocket Connection State 是什么

长连接会产生新的运行时问题：

```text
connection_id
user_id / tenant_id
session_id
last_seen
subscriptions
backpressure state
```

但不要把所有业务状态只存在当前 Python 进程内。

如果服务多实例：

```text
Client A → Worker 1
Client B → Worker 2
```

跨实例广播、Session State、Agent Run State 需要共享状态或消息层。

---

## 5. Connection Manager 的边界

Demo 常见：

```python
active_connections: list[WebSocket] = []
```

它可以帮助理解连接管理，但生产多实例下：

```text
Process-local List
≠
Global Connection Registry
```

重启、扩缩容、Worker 切换都会让本地状态失效。

---

## 6. AI Event Protocol 应该与 Transport 解耦

不要设计：

```text
SSE Event 一套业务语义
WebSocket Message 又一套业务语义
```

更稳：

```text
Runtime Event Model
        ↓
Transport Adapter
   ┌────┴────┐
   ↓         ↓
  SSE      WebSocket
```

例如统一 Event：

```json
{
  "type": "tool_result",
  "run_id": "run_123",
  "seq": 8,
  "payload": {
    "tool": "search_docs",
    "status": "success"
  }
}
```

Transport 只决定怎么发，不重新定义 Agent 业务状态。

---

## 7. Message Envelope 至少考虑什么

推荐思考：

```text
version
type
run_id / session_id
sequence
correlation_id
payload
error
```

为什么要 `sequence`？

因为重连、异步 Tool、并发事件时客户端需要知道顺序。

为什么要 `correlation_id`？

因为多个 Tool Call / User Action 可能并行，需要关联 Request 与 Result。

---

## 8. Heartbeat 为什么需要

长连接中：

```text
没有业务消息
≠
连接一定健康
```

Proxy、NAT、网络切换都可能让连接半失效。

需要设计：

```text
ping / pong
last_seen
idle timeout
reconnect
```

但具体策略依赖 Client/Proxy/Server，不存在一个所有环境都适用的固定秒数。

---

## 9. Backpressure 在 WebSocket 更明显

如果 Server 生成速度远高于 Client 消费：

```text
Producer fast
→ outbound queue grows
→ memory grows
→ latency grows
```

不能无限缓存。

需要决定：

- queue limit；
- drop policy；
- slow client disconnect；
- aggregation；
- producer pause。

详细 Backpressure 属于 AI Backend Engineering，但 FastAPI 层必须知道连接不是无限吞吐。

---

## 10. Auth 怎样做

WebSocket 没有“每个消息都天然重新走 HTTP Authorization Dependency”这种假设。

你需要明确：

```text
handshake authentication
→ bind user / tenant to connection
→ message-level authorization if action differs
```

高风险 Tool Action 仍要重新做 Policy / Approval，而不是“连接登录过一次就永远允许”。

---

## 11. Disconnect 时发生什么

至少清理：

```text
connection registry
subscriptions
pending send task
per-connection buffer
trace / metrics
```

但是否取消 Agent Run，要看业务语义：

```text
用户关浏览器
→ cancel generation?
→ continue durable task?
→ detach UI but keep run alive?
```

Transport Disconnect 和 Business Cancellation 不能简单画等号。

---

## 12. SSE / WebSocket 与 FASTAPI-005 的关系

“只会 GET / POST 为什么做不了 Claude Code 类 Agent Service？”

因为 Production Agent UI 需要：

```text
Run Lifecycle
Streaming Event
Tool Progress
User Interrupt
Permission Prompt
Reconnect
Session State
```

FastAPI 能提供 Transport / API Layer，但 Runtime State 本体仍在 Agent Harness。

---

## 13. 🎯 面试怎么回答

> 如果交互主要是服务端持续推 Agent/LLM 结果，我优先考虑 SSE；如果客户端也需要持续低延迟地发送控制、音频或交互事件，再考虑 WebSocket。我会把 Agent Event Model 与 Transport 解耦，让同一套 typed event 可以映射到 SSE 或 WebSocket。WebSocket 还要额外设计连接状态、心跳、重连、Backpressure、多实例路由和 Disconnect 后业务 Run 是否继续。

---

## 14. 本章自测

<details>
<summary>1. 为什么普通 AI Chat 不一定需要 WebSocket？</summary>

如果主要是用户发一次请求、服务端持续推 token/event，SSE 已能满足单向流需求，协议和运维复杂度更低。

</details>

<details>
<summary>2. 为什么不能只用进程内 list 管全局 WebSocket 连接？</summary>

多 Worker / 多实例时每个进程只能看到自己的连接；扩缩容和重启也会丢状态。跨实例能力需要共享消息/状态设计。

</details>

<details>
<summary>3. Client Disconnect 是否等于 Agent Run Cancellation？</summary>

不一定。短生成可以取消；Durable Long-running Run 可能继续执行，只是前端暂时断开。两者需要显式业务语义。

</details>
