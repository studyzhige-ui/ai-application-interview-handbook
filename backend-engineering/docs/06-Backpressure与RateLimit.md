# 06. Backpressure、Concurrency Limit、Rate Limit 与 Load Shedding

> 这一章回答一个核心问题：**当上游比下游快时，系统怎样避免把自己撑爆？**

## 1. Backpressure 是什么

想象：

```text
Producer 1000 req/s
        ↓
Consumer 200 req/s
```

如果没有控制：

```text
Queue Depth ↑
Memory ↑
Latency ↑
Timeout ↑
Retry ↑
```

最终系统不是“慢一点”，而是进入级联故障。

Backpressure 的本质是：

> **让上游感知下游处理能力有限，并减慢、拒绝、降级或排队。**

---

## 2. 四种最常见的手段

### Bound Queue

只允许有限等待：

```text
Queue capacity = 1000
```

满后必须有明确策略。

### Concurrency Limit

控制同时执行任务数：

```python
sem = asyncio.Semaphore(20)
```

### Rate Limit

控制单位时间进入量：

```text
100 req/s
1000 tokens/min
```

### Load Shedding

系统超载时主动拒绝一部分工作：

```text
503 / 429
skip optional work
degrade quality
```

它们解决的问题相关，但不是同一个概念。

---

## 3. Concurrency Limit vs Rate Limit

### Concurrency Limit

约束：

```text
同时在跑多少个
```

适合保护：

- DB Connection；
- Provider Concurrent Streams；
- Tool Calls；
- CPU-heavy jobs。

### Rate Limit

约束：

```text
单位时间允许多少个
```

适合：

- API quota；
- user limit；
- model token budget；
- external vendor limit。

例子：

```text
20 concurrent calls
但每分钟最多 100 calls
```

两个约束可以同时存在。

---

## 4. Fixed Window

```text
12:00:00 ~ 12:00:59
最多 100 次
```

简单，但窗口边界可能产生突刺：

```text
12:00:59 100 次
12:01:00 100 次
```

短时间可能出现 200 次。

---

## 5. Sliding Window

关注最近一段真实时间范围。

优点：比 Fixed Window 平滑。

代价：状态和计算更复杂。

实现可能使用：

- sorted set；
- approximate counters；
- bucket aggregation。

Redis 章节负责具体数据结构实现，这里关注算法语义。

---

## 6. Token Bucket

抽象：

```text
tokens 按固定速度补充
request 消耗 token
```

允许一定 Burst：

```text
bucket capacity = 100
refill = 10/s
```

很适合 API Rate Limit。

AI 系统还可以把一个请求按成本消耗多个 token：

```text
small model call = 1 quota unit
large model call = 5 quota units
```

甚至直接基于模型 Token 做预算。

---

## 7. Leaky Bucket

更强调以稳定速率向下游排出请求。

可以理解：

```text
burst input
→ buffer
→ fixed drain rate
```

适合平滑流量，但 Queue 仍然必须有界。

---

## 8. Multi-tenant Rate Limit

AI SaaS 不能只做 global limit。

常见维度：

```text
Global
Tenant
User
API Key
Model
Endpoint
Tool
Token Budget
```

例如：

```text
Global LLM concurrency = 500
Tenant A = 50
User = 5
Expensive Model = 100 req/min
```

否则一个大租户可能耗尽所有容量。

---

## 9. Queue 应该有多长

不是越长越好。

假设：

```text
worker throughput = 100 req/s
queue depth = 10000
```

队尾任务理论上可能等约 100 秒。

如果用户 Deadline 只有 10 秒，这些任务进入 Queue 的那一刻已经注定失败。

因此 Queue Capacity 应和：

- processing rate；
- deadline；
- acceptable wait；
- memory；
- burst duration

一起设计。

---

## 10. Load Shedding 为什么是保护机制

很多人把拒绝请求看成“服务失败”。

但过载时：

```text
fail 10% quickly
```

可能比：

```text
accept 100%
→ all wait
→ all timeout
→ system crash
```

更可靠。

Google SRE 强调服务过载时应具备 graceful degradation 和 load shedding，而不是无限接受所有工作。

---

## 11. Degradation

AI Service 的降级特别丰富：

```text
large model → small model
rerank → skip rerank
Top-K 50 → Top-K 10
agent 10 steps → 4 steps
realtime retrieval → cached result
multimodal → text-only
```

降级不是“随便变差”，而是提前定义：

```text
什么能力是核心？
什么是 optional？
什么可以降低成本？
```

---

## 12. Request Coalescing

HotKey 场景：

```text
1000 requests
→ same expensive result
```

可以把同一个 Key 的并发 Miss 合并：

```text
first request computes
others await same future
```

减少 downstream amplification。

这个思想也适合：

- model metadata；
- embedding cache miss；
- config reload；
- expensive RAG query cache。

---

## 13. Adaptive Concurrency

固定 100 并发不一定适合所有时刻。

更高级系统会根据：

- latency；
- error rate；
- queue time；
- downstream saturation

动态收缩或放大并发。

初学者不需要先实现复杂算法，但要理解：

> 并发上限的本质是保护服务曲线，而不是一个永恒常数。

---

## 14. Retry 与 Backpressure 的冲突

服务已经过载：

```text
new requests 1000/s
capacity 800/s
```

如果失败 200/s 全部立即 Retry：

```text
load → 1200/s
```

Retry 在过载时可能变成**负向 Backpressure**。

所以后面 Retry 必须配：

- backoff；
- jitter；
- retry budget；
- overload-aware errors。

---

## 15. AI 场景：Tool Fan-out

一个 Agent 同时调用：

```text
10 search tools
5 APIs
3 DB queries
```

如果 100 个 Agent 同时运行：

```text
1800 downstream operations
```

更成熟的控制：

```text
per-run semaphore
per-tool limit
per-tenant quota
global provider limit
queue / reject
```

---

## 16. Metrics

Backpressure 是否健康，要看：

```text
queue_depth
queue_wait_time
active_concurrency
rejected_requests
rate_limit_hits
downstream_latency
pool_utilization
```

只看 QPS 不够。

---

## 17. 🎯 面试怎么答

**问：怎样防止高并发把 LLM Provider 打满？**

可以回答：

> 我会同时做并发和速率两层控制。Semaphore 或 Worker Slot 限制同时在飞的请求，Token Bucket 等控制单位时间调用量；再按 Tenant/User 做公平配额。Queue 必须有界并受 Deadline 约束，超载时宁可 429/503 或降级，也不能无限排队。还要监控 Queue Wait、Active Concurrency、Reject Rate 和 Provider Latency。

---

## 18. ⚠️ 易错点

- Rate Limit ≠ Concurrency Limit；
- Queue ≠ 无限缓冲；
- 429 ≠ 系统一定设计失败；
- Retry ≠ Backpressure；
- Semaphore ≠ Distributed Rate Limit；
- Global Limit ≠ Multi-tenant Fairness。

---

## 19. 本章自测

<details>
<summary>1. 为什么 Queue 越长不一定越可靠？</summary>

长 Queue 会增加等待、内存和超时。如果等待时间已经超过任务 Deadline，继续排队只是把失败延迟发生。

</details>

<details>
<summary>2. Token Bucket 为什么允许 Burst？</summary>

Token 可以在空闲时积累到 Bucket Capacity，因此短时间可一次消耗多个 token；长期平均速率仍由 refill rate 约束。

</details>

<details>
<summary>3. 为什么过载时快速拒绝可能比全部接收更可靠？</summary>

快速拒绝可以保护剩余容量，让一部分请求成功；全部接收会导致 Queue、内存和延迟持续增长，最终可能让所有请求都超时并引发级联故障。

</details>
