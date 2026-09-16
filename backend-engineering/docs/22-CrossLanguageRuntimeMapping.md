# 22. Spring / JVM / Java Concurrency / Go Runtime：跨语言 Backend Primitive 映射

> AIBE 的 39 道真人 Canonical 中，有一组明显来自 Java / Spring / Go 面试。它们必须保留市场信号，但我们的主线仍然是 Python AI Backend。本章目标不是临时学一遍 Java/Go，而是把这些题**映射回已经掌握的通用 Backend Primitive**。

## 1. 为什么单独放一章，而不是散到主线里

真实市场会问：

```text
Spring Bean Lifecycle
AOP / Proxy
synchronized / ReentrantLock / CAS / AQS
JVM Memory / GC / OOM
HashMap / ConcurrentHashMap
ThreadLocal
Go Goroutine / GMP / Channel
```

如果把这些生态细节穿插到 Python 主线，会破坏 beginner-first 结构。

更合理：

```text
先学通用 Primitive
→ 再看不同生态怎样实现/命名
```

---

## 2. Dependency Injection：FastAPI Depends vs Spring DI

通用问题：

> 一个组件如何声明并获得依赖？依赖的生命周期由谁管理？

FastAPI：

```text
Depends
→ dependency graph
→ request/application resource
```

Spring：

```text
Bean definition
→ container creates / wires
→ lifecycle callbacks
→ proxy / scope
```

概念共性：

- dependency graph；
- lifecycle；
- scope；
- inversion of control。

差异在具体 Container 和 Runtime。

---

## 3. Spring Bean Lifecycle 的面试层次

不需要背所有 callback 顺序，但至少理解：

```text
definition
→ instantiate
→ inject dependencies
→ post-process
→ initialize
→ usable bean
→ destroy
```

为什么重要？

因为：

- DB Client 何时建立；
- Proxy 何时包装；
- Lifecycle Hook 何时执行；
- Circular Dependency 为什么麻烦。

和 FastAPI Lifespan / Dependency Scope 属于同类资源生命周期问题。

---

## 4. AOP / Proxy 映射到什么

AOP 常做横切逻辑：

```text
transaction
logging
metrics
auth
retry
```

它和 Middleware / Decorator 都在解决 Cross-cutting Concern，但执行边界不同。

典型陷阱：

> Spring AOP Proxy 只有经过 Proxy 调用才能拦截，自调用可能绕开预期 Proxy 行为。

不需要在 Python 主线记这个细节，但面试如果问 Spring 要知道它是 Proxy-based 的实现问题。

---

## 5. Java `synchronized` / ReentrantLock / CAS

映射到通用并发问题：

```text
Mutual Exclusion
Lock Ownership
Blocking / Wakeup
Optimistic Update
Contention
```

### synchronized

语言/VM 层 monitor 语义。

### ReentrantLock

显式 Lock API，支持更多控制能力，如可中断获取、Condition 等。

### CAS

```text
read expected value
→ compare
→ atomically swap
```

属于 Optimistic Concurrency Primitive。

---

## 6. AQS 的学习边界

AQS 是 Java 并发包中很多同步器的基础框架。

面试可以理解：

```text
state
+ queue of waiters
+ acquire/release protocol
```

不要为了 AI Backend 求职去背所有源码字段，但要知道：

> Java 的 Lock/Semaphore 等高级同步器背后也需要管理竞争状态与等待队列。

这与我们前面的 Semaphore / Backpressure 思想能对应。

---

## 7. Concurrent Collection

普通 HashMap 在并发写下不能假设安全。

ConcurrentHashMap 的核心目标是：

```text
concurrent access
+ correctness
+ reduce global contention
```

具体实现随 JDK 版本演进，不应把某个历史版本的 segment 数量当成永恒事实。

面试时明确版本边界比死背更重要。

---

## 8. HashMap：为什么和 Python dict 不能完全类比

共同点：

- hash-based mapping；
- collision；
- resize；
- average O(1)。

Java HashMap 常见追问：

- bucket；
- linked list / treeification；
- resize；
- load factor。

Python dict 有自己的实现策略。

课程只做概念映射，**不能把 Java HashMap 的桶/红黑树机制说成 Python dict 底层。**

---

## 9. ThreadLocal

通用目标：

```text
每个线程维护自己的 Context
```

常用于：

- request context；
- transaction context；
- trace metadata。

危险在 Thread Pool：

```text
thread reused
→ old ThreadLocal value remains
→ next request sees stale context
```

因此必须在 `finally` 清理。

这与 Python `contextvars` / request-scoped context 解决的是类似问题，但实现不同。

---

## 10. JVM Memory Area

面试基础层次可区分：

- Heap：对象主要区域；
- Thread Stack：调用帧 / 局部状态；
- Metaspace：类元数据等；
- Native / Direct Memory 等。

不要把“JVM Memory”简化成“Heap + Stack”后就结束，因为 OOM 也可能发生在其它区域。

---

## 11. GC

通用问题和 Python GC 相似：

```text
哪些对象还可达？
什么时候回收？
暂停多久？
吞吐与延迟怎么权衡？
```

JVM 有多种 GC Collector，具体机制与版本很多。

AI Application Engineer 面试更重要的是：

- allocation rate；
- heap pressure；
- pause；
- memory leak；
- GC log / heap dump 分析思路。

而不是背所有 Collector 参数。

---

## 12. JVM OOM / Memory Leak 排查

思路仍然是：

```text
memory rising?
→ which region?
→ which object/type?
→ still referenced by whom?
→ workload or leak?
```

常见工具方向：

- GC Log；
- Heap Dump；
- profiler；
- thread dump；
- container memory metrics。

核心和 Linux / Observability 章节完全相通。

---

## 13. Go Goroutine

Goroutine 是 Go Runtime 管理的轻量并发执行单元。

不要简单等同 OS Thread。

大量 Goroutine 由 Go Scheduler 映射到有限 OS Thread。

这和 Python Coroutine 都体现：

> 用户态/Runtime 调度大量任务，而不是一任务一 OS Thread。

但调度模型和执行语义不同。

---

## 14. GMP 的直觉

Go Scheduler 常用 G/M/P 来描述：

```text
G = goroutine
M = OS thread
P = scheduling resource / execution context
```

目标是高效把大量 G 调度到有限 M 上运行。

初学者重点理解：

- goroutine 很轻；
- 仍然需要 OS Thread 执行；
- CPU parallelism 受可用 P / core 等约束；
- blocking syscall 需要 Runtime 调度处理。

---

## 15. Channel

Channel 提供 Goroutine 间通信/同步：

```text
producer
→ channel
→ consumer
```

可以是 buffered / unbuffered。

它和 MQ 有相似 Producer/Consumer 外形，但边界完全不同：

```text
Channel = process/runtime 内 concurrency primitive
MQ = distributed durable messaging system
```

不能混为一谈。

---

## 16. Go Mutex vs Channel

经典误区：

> Go 有 Channel，所以不需要 Lock。

不是。

共享内存保护适合 Mutex；
Ownership Transfer / Pipeline 适合 Channel。

选择取决于 State Model，而不是口号。

---

## 17. Cross-language Mapping Table

| 通用问题 | Python / FastAPI | Java / Spring | Go |
|---|---|---|---|
| DI | Depends / explicit wiring | Spring Container | explicit wiring / libs |
| Request context | contextvars / Dependency | ThreadLocal / request scope | context.Context |
| Async I/O | asyncio | thread/reactive runtimes | goroutine + netpoll |
| Lock | Lock / RLock | synchronized / ReentrantLock | sync.Mutex |
| Semaphore | asyncio/thread semaphore | Semaphore / AQS | buffered channel / semaphore patterns |
| Memory runtime | refcount + cyclic GC | JVM GC | Go GC |
| Service lifecycle | Lifespan | Bean/App lifecycle | explicit startup/shutdown |

表格只做概念映射，不表示行为等价。

---

## 18. 为什么这组市场信号仍要保留

冻结面经里：

- JVM 有 12 个独立来源；
- Java Concurrency / ThreadLocal / Go Runtime 等也反复出现。

这说明 AI Application 岗并不总是纯 Python Interview。

但课程仍坚持：

```text
通用 Backend Primitive first
→ ecosystem mapping second
```

而不是把 Foundation 变成三门语言大全。

---

## 19. 🎯 面试怎么答

**问：Python asyncio 和 Go Goroutine 有什么区别？**

可以回答：

> 两者都能让大量并发任务不等于一任务一线程，但 Runtime 模型不同。Python asyncio 的协程通常在 Event Loop 中通过 `await` 协作式挂起，CPU-bound 代码会阻塞该执行线程；Go Goroutine 由 Go Scheduler 把大量 G 调度到多个 OS Thread 上，可以利用多个核并由 Runtime 处理调度。具体 Blocking、Memory 和 Cancellation 语义也不同，不能只说“都是轻量线程”。

---

## 20. ⚠️ 易错点

- Spring DI ≠ FastAPI Depends 完全等价；
- Java HashMap ≠ Python dict 同实现；
- ThreadLocal 在线程池里不会自动清理；
- JVM OOM ≠ 只有 Heap OOM；
- Goroutine ≠ OS Thread；
- Channel ≠ Distributed MQ。

---

## 21. 本章自测

<details>
<summary>1. 为什么把所有 Java/Go Canonical 拆成独立核心章会破坏课程？</summary>

因为这些题大多是同一 Backend Primitive 在不同生态的实现映射。主线应先建立并发、生命周期、内存、Context 等通用心智模型，再做跨语言映射。

</details>

<details>
<summary>2. ThreadLocal 在线程池中为什么容易泄漏 Context？</summary>

线程会被后续请求复用，如果任务结束没有清理 ThreadLocal，新请求可能读取旧值或长期保持对象引用，因此应在 finally 中 remove/clear。

</details>

<details>
<summary>3. Go Channel 为什么不能替代 Kafka？</summary>

Channel 是单进程 Runtime 内的并发通信原语，没有 Kafka 的跨进程持久化、Consumer Group、Replay、Partition 等分布式消息语义。

</details>
