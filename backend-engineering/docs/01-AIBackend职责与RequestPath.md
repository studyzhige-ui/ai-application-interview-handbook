# 01. AI Backend Engineering 的职责与完整 Request Path

> 这一章先回答：**为什么学完 FastAPI 还需要 AI Backend Engineering？**

## 1. 从“一个接口”到“一个生产服务”

Demo 常常是：

```text
Client
→ FastAPI
→ LLM
→ Response
```

生产系统更接近：

```text
Client
  ↓
DNS / TCP / TLS
  ↓
CDN / LB / Gateway
  ↓
API Service
  ├─ MySQL
  ├─ Redis
  ├─ Vector DB
  ├─ LLM Provider
  ├─ MQ / Worker
  └─ External Tool
  ↓
Streaming / JSON / Task Status
```

真正困难的问题通常不再是“怎么调用 SDK”，而是：

- 哪个依赖先超时？
- 谁拥有最终状态？
- 连接池满了怎么办？
- Retry 会不会重复执行？
- 下游变慢时上游如何限流？
- Worker 崩溃后任务怎样恢复？
- 一个请求慢，到底慢在网络、DB、模型还是队列？

这些问题就是 AI Backend Engineering 的核心。

---

## 2. 一次请求到底经过哪些层

把浏览器调用 `/chat` 展开：

```text
URL
↓
DNS Resolve
↓
TCP / QUIC Connection
↓
TLS Handshake（HTTPS）
↓
HTTP Request
↓
Load Balancer / Gateway
↓
Application Process
↓
Authentication / Validation
↓
Business Service
↓
Downstream Calls
↓
Persistence / Cache / Model / Tool
↓
Response / Stream
```

任何一层都可能失败。

因此 Production 思维不是只问：

> “功能有没有实现？”

而要继续问：

> “这个链路中有哪些 Failure Boundary？”

---

## 3. 四类资源

一个后端服务最终都受有限资源约束。

### 3.1 Compute

- CPU；
- Python Worker / Thread；
- Process；
- GPU / External Model Capacity。

### 3.2 Memory

- Request Buffer；
- Queue；
- Cache；
- 大文件；
- Agent Context / Runtime State。

### 3.3 Connection

- DB Connection；
- HTTP Connection；
- Redis Connection；
- SSE / WebSocket 长连接。

### 3.4 Downstream Capacity

即使自己的服务还有资源，下游也可能只有：

```text
LLM Provider 100 concurrent requests
DB Pool 50 connections
Vector DB 200 QPS
Tool API 20 QPS
```

所以“自己还能接请求”不等于“系统还能安全处理请求”。

---

## 4. 三种工作类型

### 同步短请求

```text
request
→ query/cache/model
→ response
```

适合在 request lifecycle 内完成。

### Streaming 请求

```text
request
→ long-lived connection
→ event / token / state delta
→ finish
```

需要管理：

- disconnect；
- heartbeat；
- producer/consumer speed；
- cleanup。

### Long-running Task

```text
POST /jobs
→ 202 Accepted + task_id
→ queue / worker
→ persisted state
→ poll / SSE status
```

它不是“HTTP 请求等久一点”，而是另一种 Runtime Model。

---

## 5. State Ownership

设计任何 Backend 前都应先问：

> **最终事实到底存在哪里？**

例如 Agent Ingestion：

```text
MySQL: task metadata / durable status
Redis: hot progress / lease / ephemeral state
MQ: delivery
Vector DB: retrieval index
Object Storage: source file
```

如果把这些角色混在一起，恢复语义会很模糊。

### 一个常见反例

只把任务状态放 Redis：

```text
queued → running → done
```

Redis 重启、Key 过期或误删以后，任务是否真的完成就失去了可靠依据。

如果任务完成事实需要审计与恢复，通常应该有 durable source of truth。

---

## 6. Normal Path 之后必须画 Failure Path

正常路径：

```text
API
→ LLM
→ DB
→ Success
```

至少继续问：

```text
LLM timeout?
DB commit fail?
client disconnect?
retry?
worker crash?
partial success?
```

这就是后面 Timeout、Retry、Idempotency、MQ、Compensation 存在的原因。

---

## 7. AI Backend 的特殊点

AI Service 和普通 CRUD Backend 有共同工程基础，但也有几个更突出的特征：

### 长尾延迟明显

模型调用可能从几百毫秒到几十秒。

### Streaming 常见

连接持续时间更长，占用资源更久。

### 外部依赖多

一个请求可能同时依赖：

```text
LLM + Retrieval + Redis + Tool API + DB
```

### 成本本身是资源

除了 CPU / Memory，还需要关注：

```text
Token
Embedding
Rerank
Model Request
Tool Request
```

### Side Effect 更复杂

Agent 可能调用支付、邮件、工单、文件修改等有副作用 Tool。

所以 Retry / Cancellation 的正确性要求更高。

---

## 8. 最小 Production Checklist

面对任意 AI Backend，至少能回答：

```text
入口协议是什么？
状态在哪里？
并发上限在哪里？
连接池多大？
Timeout 多久？
Retry 哪些错误？
是否幂等？
Queue 会不会无限长？
如何取消？
如何恢复？
Trace 如何串起来？
如何扩容？
权限在哪里执行？
```

---

## 9. 🎯 面试怎么答

**问：AI Backend Engineering 和 FastAPI 有什么区别？**

可以回答：

> FastAPI 主要解决 HTTP/ASGI 框架层的请求、校验、依赖、Streaming 和应用生命周期；AI Backend Engineering 解决跨框架的 Production 问题，例如连接池、Backpressure、Timeout、Retry、Idempotency、MQ、缓存一致性、服务发现、部署和可观测性。它关注的是系统在故障、并发和规模扩大后仍然可控。

---

## 10. ⚠️ 易错点

- “加一个 Redis 就是生产化”——不是；
- “异步就能提高所有吞吐”——不是；
- “队列可以吸收无限流量”——不是；
- “Retry 是可靠性的默认增强”——可能反而造成雪崩；
- “多副本就自动高可用”——如果共享依赖先饱和，多副本也无效。

---

## 11. 本章自测

<details>
<summary>1. 为什么 Long-running Task 不应该理解成“HTTP 请求多等一会儿”？</summary>

因为长任务需要独立的持久状态、Queue/Worker、取消、恢复、重试、Lease 等生命周期语义。HTTP Connection 只是与用户交互的 Transport，不能承担任务本身的 durable execution。

</details>

<details>
<summary>2. 为什么“服务 CPU 还有余量”不代表系统还能继续接流量？</summary>

瓶颈可能在连接池、DB、LLM Provider、Queue、外部 Tool 等其它有限资源。Production Capacity 取决于整条依赖链，而不是单个进程 CPU。

</details>

<details>
<summary>3. State Ownership 为什么是后端设计的前置问题？</summary>

因为 Retry、恢复、一致性和审计都需要知道哪个系统保存最终事实。如果状态角色混乱，系统在 Partial Failure 后无法判断真正结果。

</details>
