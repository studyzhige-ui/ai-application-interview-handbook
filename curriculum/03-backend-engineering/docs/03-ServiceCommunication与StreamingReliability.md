# 03. HTTP / RPC / MQ 与 Streaming Reliability

> 这一章回答：**服务之间到底应该同步调用、RPC，还是发消息？Streaming 断了以后又该怎么办？**

## 1. 三种通信不是互相替代

```text
HTTP / REST
RPC / gRPC
MQ / Event
```

它们解决的问题不同。

| 维度 | HTTP / REST | RPC / gRPC | MQ / Event |
|---|---|---|---|
| 交互 | 请求/响应 | 请求/响应 | 异步消息 |
| Schema | 通常较松 | 通常更强 | 事件契约 |
| 耦合 | 调用方知道服务 | 调用方知道服务/IDL | Producer/Consumer 可解耦 |
| 延迟 | 低到中 | 常偏低 | 有排队延迟 |
| Failure | 直接暴露 | 直接暴露 | 延迟暴露、重试/重复 |
| 适合 | 公共 API、服务调用 | 内部高性能服务 | 异步任务、削峰、事件传播 |

不要用一句“MQ 解耦，所以 MQ 最好”。

---

## 2. 同步调用什么时候最自然

例如：

```text
Chat API
→ Auth Service
→ Retrieval Service
→ LLM Provider
→ Response
```

用户正在等待结果，而且后续逻辑需要前一步返回值，此时同步 Request/Response 很自然。

优点：

- 调用链直观；
- Error 立即传播；
- 编程模型简单。

缺点：

- 下游慢会直接拖慢上游；
- 深调用链更容易 Timeout；
- Retry 可能层层放大；
- Availability 强耦合。

---

## 3. RPC / gRPC 为什么存在

RPC 让调用像函数：

```text
embedding_service.embed(request)
```

但实际上跨越网络。

成熟 RPC 往往强调：

- IDL / Schema；
- Code Generation；
- Deadline；
- Metadata；
- Streaming；
- Status Code。

优势是内部服务契约清晰、序列化高效。

代价是：

- 强 Schema Governance；
- 客户端/服务端版本兼容；
- Debug 与跨语言工具链复杂度。

---

## 4. 为什么需要 MQ

当调用方不必等待任务真正完成，或者需要吸收突发流量时：

```text
API
→ task record
→ MQ
→ Worker
→ result store
```

MQ 带来的不是“自动可靠”，而是：

- temporal decoupling；
- buffering；
- consumer scaling；
- replay / retry capability；
- producer 与 worker 生命周期解耦。

代价是：

- duplicate delivery；
- ordering；
- backlog；
- eventual consistency；
- observability 更难。

后面会专门讲 MQ Reliability。

---

## 5. Streaming Transport：SSE vs WebSocket

这部分 FastAPI 已经从框架实现角度讲过，这里只看通用通信语义。

### SSE

```text
Client → HTTP Request
Server → event stream → Client
```

适合：

- token streaming；
- agent progress；
- server push；
- 单向事件为主。

### WebSocket

```text
Client ⇄ Server
```

适合：

- voice realtime；
- 双向控制；
- interrupt / approval；
- interactive agent session。

选型核心不是“谁更新”，而是通信方向和状态模型。

---

## 6. Streaming Connection ≠ Durable Run

这是 AI Backend 很重要的一条边界。

错误模型：

```text
WebSocket connected = Agent running
WebSocket disconnected = Agent cancelled
```

Production 更常见：

```text
Durable Run State
      │
      ├─ SSE Client A
      ├─ SSE Client B
      └─ WebSocket Client C
```

Transport 可以断开、重连；Run State 不应该自动消失。

这与 Agent Harness 的 Checkpoint / Resume 对接。

---

## 7. Heartbeat 解决什么

长连接可能出现：

- NAT / Proxy idle timeout；
- Client 网络切换；
- Half-open connection；
- Server 进程异常。

Heartbeat 主要帮助：

```text
connection liveness
+ idle keepalive
+ failure detection
```

它不是业务一致性协议。

---

## 8. Reconnect 与 Resume 是两件事

Reconnect：

```text
重新建立 Transport Connection
```

Resume：

```text
从上次已经确认的业务位置继续
```

例如 Event Protocol：

```json
{
  "event_id": 128,
  "run_id": "run_42",
  "type": "tool_result",
  "payload": {}
}
```

Client 记录：

```text
last_event_id = 128
```

重连：

```text
GET /runs/run_42/events?after=128
```

这才是应用层 Resume。

---

## 9. Resume 的前提：事件必须有稳定身份

只传：

```text
token A
token B
token C
```

很难可靠 Resume。

更成熟的是：

```text
Run ID
Event ID / Sequence
Event Type
Timestamp
Payload
```

必要时再有：

```text
Snapshot Version
Cursor
Ack
```

---

## 10. Ordering 问题

如果不同 Worker 并发产生 Event：

```text
Tool A finished
Tool B finished
Model delta
State update
```

“到达顺序”未必等于“业务顺序”。

因此要明确：

- 是否要求 global order；
- 只要求 per-run order；
- 是否允许 concurrent branch；
- UI 怎样 merge。

不要把 TCP 的字节顺序当成整个分布式系统的业务顺序。

---

## 11. Duplicate Event

重连、重放、MQ At-least-once 都可能让 Event 重复。

Client 可以利用：

```text
(run_id, event_id)
```

做去重。

Server 端副作用仍需要自己的 Idempotency Key。

---

## 12. Error Contract

Streaming 一旦开始，不能假设还能随意改 HTTP Status。

所以 Event Protocol 常需要：

```text
error
retryable
fatal
run_failed
run_cancelled
```

例如：

```json
{
  "type": "error",
  "code": "PROVIDER_TIMEOUT",
  "retryable": true,
  "message": "model provider timed out"
}
```

---

## 13. HTTP / RPC / MQ 如何一起用

真实系统经常不是三选一：

```text
Client
  ↓ HTTP
API Service
  ↓ RPC
Retrieval Service
  ↓
LLM Provider

API Service
  ↓ MQ
Async Ingestion Worker
```

选型依据应是：

```text
调用方是否必须同步拿结果？
是否要 Buffer？
是否需要 Replay？
Schema 耦合能否接受？
Failure 要怎样暴露？
```

---

## 14. 🎯 面试怎么答

**问：HTTP、RPC、MQ 怎么选？**

可以回答：

> 我先看交互语义。需要同步请求/响应且接口对外时 HTTP 最自然；内部服务强契约和低延迟调用可以考虑 RPC；任务不要求调用方同步等待、需要削峰、消费者独立扩展或故障后重放时更适合 MQ。MQ 不代表自动可靠，它会引入重复、顺序、积压和最终一致性问题，需要额外设计。

---

## 15. ⚠️ 易错点

- WebSocket ≠ Durable Session；
- Heartbeat ≠ Exactly-once；
- Reconnect ≠ Resume；
- MQ ≠ 不丢消息；
- RPC ≠ 没有网络 Failure；
- TCP order ≠ 分布式业务 global order。

---

## 16. 本章自测

<details>
<summary>1. 为什么 Agent 长任务不能把 WebSocket Connection 当作唯一状态？</summary>

连接是易失 Transport；网络切换、Proxy、客户端刷新都可能让连接中断。长任务应该有独立 durable run state，Connection 只是订阅/控制通道。

</details>

<details>
<summary>2. Reconnect 与 Resume 的区别是什么？</summary>

Reconnect 只是重新建连接；Resume 还需要知道上次消费到哪个业务 Event 或 Task State，并从该位置继续。

</details>

<details>
<summary>3. MQ 为什么可以削峰但不能无限吸收流量？</summary>

Queue 仍受磁盘、内存、Broker、Retention 和消费者吞吐限制。长期生产率大于消费率时 Backlog 必然持续增长，最终必须限流、扩容或降级。

</details>