# 19. Docker、Kubernetes、Health Check、Graceful Shutdown 与 Horizontal Scaling

> 这一章不把你训练成 Kubernetes 运维工程师，而是掌握 AI Backend 生产部署必须理解的 Runtime Boundary。

## 1. Container 解决什么

Container 主要把：

```text
application
+ runtime
+ dependency
+ filesystem view
```

打包为可重复运行的环境。

它依赖操作系统级隔离机制，例如 Namespace / cgroup 等。

Container 不是轻量虚拟机的完整等价物；它通常与 Host 共享内核。

---

## 2. Image 与 Container

Image：

```text
immutable-ish build artifact
```

Container：

```text
image + runtime process + writable layer + resource limits
```

生产部署应该保证：

- Image 可重建；
- 依赖版本明确；
- Secret 不 baked into image；
- runtime config 外置。

---

## 3. 一个 Container 里到底跑几个进程

对于 Python API：

```text
1 container
→ 1 or multiple worker processes
```

取决于部署模型。

Kubernetes 场景常倾向：

```text
Pod replica scaling
```

而不是每个 Container 内堆很多 Process。

但没有绝对规则。

关键是计算：

```text
worker count
× DB pool
× HTTP pool
× memory per process
```

---

## 4. Kubernetes 解决什么

Kubernetes 主要提供：

- Deployment / Replica management；
- Scheduling；
- Service Discovery；
- Health / Restart；
- Rolling Update；
- Resource Request/Limit；
- Config / Secret integration；
- Horizontal scaling primitives。

它不会自动解决：

- Idempotency；
- DB consistency；
- application backpressure；
- agent checkpoint correctness。

---

## 5. Pod / Deployment / Service

### Pod

一组紧密协作 Container 的调度单元。

### Deployment

声明：

```text
我要 N 个这样的 Pod
```

Controller 负责逼近期望状态。

### Service

为动态 Pod 集合提供稳定访问入口。

这和上一章 Service Discovery / LB 直接衔接。

---

## 6. Startup / Liveness / Readiness

Kubernetes 官方明确区分三类 Probe。

### Startup

```text
应用是否已经完成启动？
```

适合启动很慢的 AI Service，例如加载模型、Warm Cache。

### Liveness

```text
进程是否已经陷入无法恢复状态，需要 restart？
```

### Readiness

```text
现在是否应该接流量？
```

失败时通常先从 Service Endpoint 移除，而不是直接 Restart。

---

## 7. 为什么 Liveness 不能乱写

危险：

```text
DB temporarily slow
→ liveness fails
→ pod restarts
→ remaining pods receive more traffic
→ also fail
```

可能造成级联故障。

Liveness 应判断：

> “这个实例自身是否无法恢复？”

Readiness 更适合表达临时不能接流量。

---

## 8. Readiness 不应该无脑依赖所有下游

假设 API 依赖：

```text
DB
Redis
LLM A
LLM B
```

如果任何一个小依赖波动都让 Readiness false：

```text
all pods removed
```

可能比降级服务更糟。

要区分：

- hard dependency；
- optional dependency；
- degradable dependency。

---

## 9. Graceful Shutdown

收到终止信号后，理想流程：

```text
mark not ready
→ stop new traffic
→ drain in-flight requests
→ cancel / finish background work
→ flush / persist state
→ close pools
→ exit
```

而不是：

```text
SIGTERM
→ process immediately dies
```

Streaming / Long-running Task 尤其需要清晰策略。

---

## 10. Connection Draining

长连接：

```text
SSE 60s
WebSocket hours
```

Rolling Update 时怎么办？

可以：

- stop accepting new；
- give grace period；
- send reconnect hint；
- persist run state；
- client reconnect other replica。

所以 Transport 和 Durable State 必须分离。

---

## 11. Horizontal Scaling

增加 Replica：

```text
API pods 10 → 20
```

前提：

- state externalized；
- DB / Redis / Provider 有容量；
- LB/discovery 正常；
- session 不绑死；
- work partition 能扩展。

如果 DB 已经 100% CPU，加 API Pod 可能让 DB 更快崩。

---

## 12. HPA 的直觉

Horizontal Pod Autoscaler 可以根据 CPU 或其它指标扩缩副本。

但 AI Service 的真实瓶颈可能不是 CPU，而是：

- queue depth；
- active streams；
- model concurrency；
- provider rate limit。

所以 Autoscaling Metric 要和 Workload 对齐。

---

## 13. Resource Request / Limit

Request：Scheduler 用于资源规划。

Limit：Container 可使用上限之一。

CPU Limit 可能产生 throttling；Memory 超 Limit 可能 OOMKilled。

因此：

```text
P99 latency suddenly high
```

也要看 cgroup throttling，而不只是 Host CPU。

---

## 14. Rolling Update

典型：

```text
old pods + new pods coexist
```

需要考虑：

- API backward compatibility；
- DB schema compatibility；
- event schema；
- config version；
- model/prompt version；
- old/new worker 同时消费。

Deployment 能滚动，并不代表应用语义自动兼容。

---

## 15. AI 场景：Model Client Warmup

Pod 启动后可能需要：

```text
load tokenizer
initialize HTTP pools
fetch model config
warm retrieval client
```

此时进程已经 alive，但不应接流量。

Startup/Readiness 应表达这个状态。

---

## 16. AI 场景：Long-running Worker

Worker Pod 正在处理 20 分钟任务时收到缩容：

要定义：

```text
finish current?
checkpoint and release?
lease expires and reclaim?
force cancel?
```

这必须由 Task Runtime 设计决定，Kubernetes 只能给你 termination lifecycle。

---

## 17. Metrics

```text
pod_restarts
readiness_failures
liveness_failures
cpu_throttling
memory_working_set
oom_killed
termination_duration
inflight_requests
active_streams
```

部署层指标要和应用 Trace 对齐。

---

## 18. 🎯 面试怎么答

**问：Readiness 和 Liveness 有什么区别？**

可以回答：

> Readiness 表示当前实例是否应该接流量，失败时通常从 Service Endpoint 中移除；Liveness 表示进程是否已经处于无法恢复状态，需要重启。临时依赖慢更适合影响 Readiness 或降级，而不是轻易让 Liveness 失败，否则可能造成所有 Pod 连锁重启。

---

## 19. ⚠️ 易错点

- Container ≠ VM；
- Kubernetes ≠ 自动高可用；
- Liveness ≠ 所有依赖 Health；
- 多 Pod ≠ 下游容量增加；
- Rolling Update ≠ Schema 自动兼容；
- SIGTERM ≠ 可以忽略 In-flight / Lease / Stream。

---

## 20. 本章自测

<details>
<summary>1. 为什么 Readiness 比“Process exists”更接近能否接流量？</summary>

进程可能仍在初始化、连接池未建立或正在临时过载。Readiness 专门表达当前服务能力，而 Process 存活只说明程序还没退出。

</details>

<details>
<summary>2. 为什么 Horizontal Scaling 可能让 DB 更糟？</summary>

更多 API Replica 会产生更多并发连接和 Query，如果 DB 已饱和，只会增加压力。扩容必须看整条依赖链容量。

</details>

<details>
<summary>3. Graceful Shutdown 最重要的第一步通常是什么？</summary>

先停止接收新流量（例如变为 not ready），再 Drain 已有请求/连接/任务，最后释放资源并退出。

</details>