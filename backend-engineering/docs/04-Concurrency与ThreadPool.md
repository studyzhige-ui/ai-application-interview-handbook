# 04. Concurrency Execution Model：Process / Thread / Coroutine / Thread Pool

> Python 已经讲过这些 Runtime Primitive。本章不重复语言语义，而是回答：**一个 Backend Service 怎样把有限 CPU、Thread、Process 和 Coroutine 组织成可控的执行容量？**

## 1. Concurrency 与 Parallelism

### Concurrency

多个任务在同一时间段交错推进。

### Parallelism

多个任务真正同时执行。

```text
Concurrency = scheduling problem
Parallelism = execution capacity problem
```

AI Backend 常同时面对：

- 大量 I/O 并发；
- 少量 CPU-heavy parsing / OCR / compression；
- 外部 Provider 限流；
- 同步 SDK；
- Worker 数量与 Memory 约束。

---

## 2. Process、Thread、Coroutine 放到 Service 里看

### Process

优点：

- 隔离强；
- 多核 CPU；
- 单 Process 崩溃影响边界更清楚。

成本：

- Memory duplication；
- IPC；
- Pool / Client 每 Process 一份；
- 启动成本。

### Thread

适合：

- Blocking I/O；
- 同步 SDK bridge；
- 某些释放 GIL 的 Native Work。

风险：

- thread explosion；
- lock contention；
- context switch；
- ThreadLocal 泄漏。

### Coroutine

适合大量 awaitable I/O。

优势：

- 轻量；
- 单 Event Loop 可以管理大量等待任务。

风险：

- blocking call 会污染整个 Loop；
- task 数量仍然不能无限；
- downstream capacity 不会因为 coroutine 轻量而变大。

---

## 3. 为什么“10000 个 Coroutine”仍可能拖死系统

Coroutine 自己很轻，但它们最终可能同时：

```text
10000 HTTP requests
10000 DB waits
10000 LLM calls
10000 pending buffers
```

下游和连接池不可能无限承载。

因此 Async Service 必须继续设计：

- Semaphore；
- Connection Pool；
- Queue；
- Rate Limit；
- Backpressure。

---

## 4. Thread Pool 的核心模型

抽象：

```text
Submit Task
↓
Queue
↓
Worker Thread
↓
Run
↓
Result
```

三个关键资源：

```text
Worker Count
Queue Capacity
Task Runtime
```

### Queue 无限长有什么问题

如果输入速度持续大于消费速度：

```text
queue depth ↑
wait time ↑
memory ↑
timeout ↑
```

最终任务开始执行时可能已经没有业务价值。

所以 Thread Pool 不能只讨论线程数，还要讨论 Queue 与 Reject Policy。

---

## 5. Thread Pool Size 怎样思考

不要背：

> CPU 核数 × 2

这种单一公式。

先分类：

### CPU-heavy

线程再多也不会线性提升吞吐，甚至增加切换。

### I/O-heavy

线程大量时间等待，可以允许更多并发，但仍受：

- FD；
- DB / HTTP Pool；
- Memory；
- Downstream QPS。

真实调优应该通过 Load Test 找到：

```text
Throughput
Latency
CPU
Context Switch
Queue Depth
Downstream Saturation
```

的拐点。

---

## 6. Reject Policy 为什么重要

当 Pool + Queue 满：

```text
new task
↓
accept?
reject?
caller runs?
drop?
```

真正问题是：

> 系统过载时，要把压力放在哪里？

常见思路：

- fail fast；
- 429 / 503；
- degrade；
- caller throttling；
- bounded queue。

最危险的是：

> 无限 Queue，把 Overload 伪装成“暂时还没报错”。

---

## 7. Process Pool 的边界

CPU-heavy 任务：

```text
PDF parsing
OCR post-processing
large JSON transformation
compression
local ML inference
```

可以考虑 Process Pool 或独立 Worker。

但需要考虑：

- serialization；
- copy cost；
- process startup；
- memory；
- crash isolation；
- cancellation。

如果任务持续几十秒甚至几分钟，独立 Task Worker 往往比 Request 内 ProcessPool 更清晰。

---

## 8. Async + Sync SDK 怎样共存

AI Service 很常见：

```text
async endpoint
→ sync vendor SDK
```

错误做法：

```python
async def handler():
    result = blocking_sdk.call()
```

可能阻塞 Event Loop。

桥接方式：

```text
async request
→ thread pool offload
→ blocking SDK
```

但 Thread Pool 也要有容量上限。

如果所有请求都 offload：

```text
Thread Pool saturated
→ Queue
→ Request latency
→ Timeout
```

问题只是从 Event Loop 移到了 Thread Pool。

---

## 9. Worker Process 与 Pool 的乘法效应

例如：

```text
4 API workers
× 20 thread pool workers
= 最多 80 threads
```

如果每 Process 还创建：

```text
DB Pool 20
HTTP Pool 100
```

总资源也会乘上 Worker 数。

所以部署参数不能单独调。

---

## 10. AI 场景：并发调用多个 Tool

假设一个 Agent Step 同时有 20 个 Tool Call：

错误：

```python
await asyncio.gather(*all_tools)
```

如果 100 个用户同时跑：

```text
100 × 20 = 2000 tool calls
```

正确思路：

```text
Per-run concurrency
+ Global concurrency
+ Per-provider concurrency
+ Per-tenant concurrency
```

多层容量共同约束。

---

## 11. Failure Timeline

典型雪崩：

```text
Provider 变慢
→ Thread / Coroutine 持有时间增长
→ Pool Saturation
→ Queue 增长
→ Request Timeout
→ Client Retry
→ Load 更高
```

这条链会贯穿后面几章。

---

## 12. 🎯 面试怎么答

**问：Thread Pool 参数怎么设计？**

可以回答：

> 我不会只给固定公式。先看任务是 CPU 还是 I/O，再看 Task Runtime、输入速率、Queue 容量和 Downstream Capacity。Pool 大小要结合 Load Test 观察吞吐、P95/P99、CPU、Context Switch、Queue Depth 和下游饱和点。Queue 也应该有界，过载时需要 Reject / Backpressure，而不是无限堆积。

---

## 13. ⚠️ 易错点

- Coroutine 多 ≠ Downstream Capacity 变大；
- Thread Pool ≠ 无限线程；
- Process Pool ≠ 没有 IPC 成本；
- 多 Worker ≠ 参数线性增加；
- offload blocking call ≠ blocking 问题消失，只是换了资源池。

---

## 14. 本章自测

<details>
<summary>1. 为什么 Async Service 仍然需要并发上限？</summary>

Coroutine 轻量只减少等待任务的调度成本，下游连接、QPS、Memory、Provider Capacity 仍然有限。无限并发会把压力转移到 Pool、Queue 或 Downstream。

</details>

<details>
<summary>2. 为什么 Thread Pool Queue 不应该无限长？</summary>

持续过载时 Queue 会让等待时间和内存不断增长，任务真正开始时可能已超过 Deadline，并导致 Retry 和级联故障。

</details>

<details>
<summary>3. 4 个 Worker × DB Pool 20 意味着什么？</summary>

通常意味着每个 Worker 各自持有一个 Pool，理论总连接上限可能接近 80，而不是整个服务只有 20。部署时必须按总实例/进程数量计算依赖容量。

</details>
