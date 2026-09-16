# 05. Connection Pool 与 Resource Capacity

> 很多“服务突然变慢”不是 CPU 不够，而是某个 Pool 先耗尽。

## 1. 为什么需要 Connection Pool

建立连接有成本：

```text
DNS
→ TCP / QUIC
→ TLS
→ Authentication
→ Session / Protocol State
```

数据库连接还可能有：

- Server Thread / Session；
- Transaction Context；
- Memory；
- Authentication；
- Network Socket。

如果每个请求都新建/关闭连接，延迟和资源成本会很高。

Pool 的基本思想：

```text
预先/按需创建有限连接
→ Request 借用
→ 使用
→ 归还
→ 后续复用
```

---

## 2. Pool 不只是“缓存连接”

它更重要的作用是：

> **把下游容量变成显式的并发边界。**

例如 DB 最多希望服务 50 个并发 Query：

```text
App concurrency = 500
DB Pool = 50
```

那么最多约 50 个请求同时占有 DB Connection，其余需要等待或失败。

这是一种 Capacity Isolation。

---

## 3. 常见 Pool

AI Backend 可能同时有：

```text
DB Pool
Redis Pool
HTTP Connection Pool
Thread Pool
Process Pool
GPU / Model Slot Pool
```

所以“Pool”是一种通用资源管理模式，而不是 DB 专属概念。

---

## 4. Pool 的几个关键参数

不同库名字不同，但常见概念包括：

```text
min / initial size
max size
acquire timeout
idle timeout
max lifetime
keepalive / health check
```

### Max Size

限制同时持有多少连接。

### Acquire Timeout

Pool 没空闲连接时，调用方最多等多久。

### Idle Timeout

长时间不用的连接是否回收。

### Max Lifetime

连接使用多久后强制替换，避免永久使用老连接。

---

## 5. Pool Size 不是越大越好

例如把 DB Pool 从 50 调到 500：

```text
更多并发 Query
→ DB CPU / Lock / Buffer Pressure
→ Query 更慢
→ Connection 持有更久
→ Pool 更容易满
```

甚至形成正反馈。

Pool 大小应该和下游真正的服务能力匹配，而不是和上游请求数匹配。

---

## 6. Little's Law 的直觉

不要求背公式推导，但可以建立直觉：

```text
系统中平均并发量
≈ 吞吐 × 平均停留时间
```

如果 DB Query 平均从 20ms 变成 200ms，哪怕 QPS 不变，所需并发连接也会显著上升。

所以 Pool Exhaustion 可能只是**下游变慢的结果**，而不是 Pool Size 太小。

---

## 7. Pool Exhaustion 的典型症状

```text
request latency ↑
acquire wait ↑
active connections = max
idle connections ≈ 0
DB query latency maybe ↑
```

排查顺序不能只看：

> “Pool 满了，调大。”

应该继续看：

```text
谁占连接最久？
Query 为什么慢？
Transaction 是否太长？
Connection 是否泄漏？
下游是否过载？
```

---

## 8. Connection Leak

典型：

```python
conn = pool.acquire()
do_work(conn)
# exception
# forgot release
```

随着请求增长：

```text
available connection ↓
→ Pool Exhaustion
→ all requests wait
```

正确方式通常借助：

- context manager；
- `try/finally`；
- framework-managed session；
- `yield` Dependency。

Python / FastAPI 前面学过的资源生命周期在这里真正落地。

---

## 9. HTTP Connection Pool

调用 LLM Provider 时同样需要 Pool。

合理复用：

```text
Service Process
→ shared HTTP Client
→ keep-alive connection pool
→ Provider
```

错误：

```python
async def handler():
    client = AsyncClient()
    await client.post(...)
    await client.aclose()
```

每次请求重新创建 Client，会失去复用收益。

---

## 10. HTTP Pool 还有一个特别风险

Streaming Request 长时间占用连接：

```text
normal request 300ms
stream request 30s
```

即使 QPS 不高，长连接也可能让：

```text
pool occupancy ↑
```

因此 Streaming Provider Client 的 Pool Size 与普通 API 的容量模型不同。

---

## 11. Pool Waiting vs Request Deadline

假设：

```text
request deadline = 2s
pool acquire timeout = 10s
```

这是不合理的。

请求可能在 Pool 里等到用户早已超时。

更合理：

```text
Pool Wait
+ Network Connect
+ Downstream Processing
+ Serialization
≤ End-to-End Deadline
```

这会自然引出下一章的 Timeout Budget。

---

## 12. 多 Worker 的 Pool Multiplication

部署：

```text
8 app processes
DB pool per process = 20
```

总潜在连接：

```text
8 × 20 = 160
```

再乘 Kubernetes replicas：

```text
10 pods × 8 processes × 20
= 1600 connections
```

如果 DB 最大承载只有 500，这个配置从数学上就不成立。

---

## 13. Pool 与 Semaphore 的区别

Pool 管具体资源实例：

```text
20 DB connections
```

Semaphore 只是逻辑许可：

```text
最多 20 个并发任务
```

两者可以一起使用，但不是同一个概念。

---

## 14. AI 场景：Provider Capacity

如果外部 Model Provider 限制：

```text
100 requests/min
20 concurrent streams
```

本地 HTTP Pool 100 并不能安全地产生 100 个并发。

你还需要：

- rate limiter；
- concurrency semaphore；
- retry budget；
- tenant quota。

Pool 只是连接容量的一层。

---

## 15. 🎯 面试怎么答

**问：Connection Pool 满了怎么办？**

可以回答：

> 先区分它是原因还是症状。我会看 active/idle、acquire wait、connection hold time 和 downstream latency。如果连接泄漏就修生命周期；如果 query 变慢，要先解决下游；如果容量模型本身太小，再结合实例数和 DB 最大连接数调 Pool。单纯把 Pool 调大可能只是把压力直接打到 DB。

---

## 16. ⚠️ 易错点

- Pool 越大 ≠ Throughput 越高；
- Pool 满 ≠ 一定 Pool 配小；
- HTTP Keep-Alive ≠ 无限复用；
- 多进程 / 多 Pod 下 Pool 是乘法；
- Pool Size ≠ Provider Rate Limit。

---

## 17. 本章自测

<details>
<summary>1. 为什么 DB Query 变慢会导致 Pool Exhaustion？</summary>

连接被每个请求持有更久，在相同吞吐下同时占用的连接数量会上升，最终所有连接都被占用。

</details>

<details>
<summary>2. 为什么 10 Pod × 每 Pod 8 Worker × Pool 20 需要特别警惕？</summary>

因为每个 Worker 通常都有自己的连接池，总潜在连接可能达到 1600。必须与数据库最大连接数和真实容量一起计算。

</details>

<details>
<summary>3. Pool 与 Semaphore 的本质区别？</summary>

Pool 管理可复用的具体资源对象；Semaphore 管逻辑并发许可。Semaphore 可以限制没有显式连接对象的外部操作。

</details>
