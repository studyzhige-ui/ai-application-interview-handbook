# 12. 线程、进程、协程与 async/await

并发这一章是 Python Foundation 里和 AI Application 最直接相连的一章。

你最终要建立的不是“线程 / 进程 / 协程三个定义”，而是下面这条决策链：

```text
任务在等什么？
→ I/O 还是 CPU？
→ 能不能 await？
→ 是否需要共享内存？
→ 是否需要隔离？
→ 并发量有多大？
→ 失败 / Timeout / Cancellation 怎么传播？
```

---

## 1. Concurrency 和 Parallelism 先分清

### Concurrency

多个任务在同一时间段内交替推进。

### Parallelism

多个任务在同一时刻真正同时执行。

例如一个事件循环可以在单线程里管理大量 I/O 并发，但这不代表这些 Python 代码在多个 CPU 核上并行。

---

## 2. Process

进程通常拥有独立地址空间，隔离性强。

```python
from multiprocessing import Process


def work():
    print("working")

p = Process(target=work)
p.start()
p.join()
```

### 优点

- 隔离强；
- 传统 CPython/GIL 模式下可利用多个解释器进程做 CPU 并行；
- 某个 Worker 崩溃不一定破坏其它进程内存。

### 成本

- 创建成本高于线程；
- IPC 有成本；
- 大对象跨进程序列化昂贵；
- 每个进程可能复制大量 Runtime / Model Client / Cache 状态。

---

## 3. Thread

线程共享同一进程的大部分内存空间。

```python
from threading import Thread


def work():
    print("working")

t = Thread(target=work)
t.start()
t.join()
```

适合：

- 阻塞网络 SDK；
- 文件 I/O；
- 无异步接口的第三方库桥接。

风险：

- Race Condition；
- Deadlock；
- 共享状态污染；
- Thread Pool Saturation。

---

## 4. Lock、RLock、Semaphore 分别解决什么

### Lock

互斥进入临界区。

```python
from threading import Lock

lock = Lock()

with lock:
    update_shared_state()
```

适合保护一个不可并发修改的共享 invariant。

### RLock

可重入锁：同一个线程已经持有锁时，可以再次获取同一把锁。

```python
from threading import RLock

lock = RLock()
```

典型场景：

```text
method A acquires lock
→ calls method B
→ method B also needs same lock
```

如果普通 `Lock` 这样递归获取，可能自锁；`RLock` 允许同线程重入，但仍应避免把复杂锁依赖设计得难以理解。

### Semaphore

Semaphore 不是只允许 1 个进入，而是允许**最多 N 个并发进入**。

```python
from threading import Semaphore

sem = Semaphore(5)

with sem:
    call_provider()
```

它更适合“容量限制”：

```text
最多 10 个并发 OCR
最多 20 个同步 HTTP call
最多 4 个 GPU job
```

> Lock 主要保护共享状态；Semaphore 主要限制并发容量。不要混为一谈。

---

## 5. Coroutine

协程可以理解为：

> 当任务进入可等待状态时，主动把控制权交回 Event Loop，之后条件就绪再恢复。

```python
async def fetch_data():
    ...
```

调用协程函数：

```python
coro = fetch_data()
```

得到协程对象，并不代表它已经完整执行。

---

## 6. `await` 到底发生什么

```python
async def task():
    data = await client.get(...)
    return data
```

如果底层操作是真正可异步等待的 I/O，当前协程挂起后，Event Loop 可以运行其它就绪任务。

`await` 不等于：

```text
new thread
new process
background execution
```

它只是异步控制流里的挂起点。

---

## 7. Event Loop 的核心 Mental Model

```text
Ready Task A
→ run
→ await I/O
→ suspended

Ready Task B
→ run
→ await I/O
→ suspended

I/O A ready
→ resume A
```

因此 Event Loop 最怕一件事：

> **某个 Task 长时间不让出执行权。**

例如：

```python
async def bad():
    total = 0
    for i in range(10**9):
        total += i
```

这虽然写成 `async def`，但没有真正 await 的 I/O 点，会长时间阻塞事件循环。

---

## 8. `gather`：我需要全部结果

```python
results = await asyncio.gather(
    fetch_user(),
    fetch_order(),
    fetch_profile(),
)
```

适合：

```text
多个任务可以并发开始
最终需要等它们都完成
结果顺序通常与输入顺序对应
```

AI 场景：

```text
并行查 Redis
并行查 DB
并行查多个检索源
最后一起构造 Context
```

---

## 9. `as_completed`：谁先完成先处理谁

```python
tasks = [
    asyncio.create_task(call_source(x))
    for x in sources
]

for future in asyncio.as_completed(tasks):
    result = await future
    handle(result)
```

和 `gather` 的关键区别不是“谁更快”，而是**消费模式不同**。

```text
gather
→ 等一组任务
→ 统一拿结果

as_completed
→ 每个任务完成后立即产出
→ 可以先处理最快结果
```

适合：

- 多 Provider / 多 Search Source；
- First useful result；
- Progressive aggregation；
- 某些 speculative / fallback 场景。

---

## 10. Timeout：不能无限等下游

现代 Python 可以使用超时上下文或 `wait_for` 等方式表达 deadline。

例如：

```python
result = await asyncio.wait_for(
    call_provider(),
    timeout=2.0,
)
```

Timeout 的意义不是“2 秒后报一个错”这么简单，而是给系统一个边界：

```text
调用者最多愿意等多久
→ 子调用应该拿多少预算
→ Timeout 后是否 Cancel
→ 是否 Fallback
```

完整 Deadline Budget 属于 AI Backend Engineering；Python 这里掌握异步控制语义。

---

## 11. Fallback：失败后走替代路径

```python
try:
    result = await asyncio.wait_for(primary(), timeout=2)
except TimeoutError:
    result = await fallback()
```

但要先问：

- Primary Timeout 后真的停止了吗？
- Fallback 会不会产生重复副作用？
- 两条路径是否可能同时完成？
- 结果是否需要版本或来源标记？

如果调用是“查天气”，重复通常问题小；如果调用是“扣款/退款”，就不能把 Retry/Fallback 当普通函数调用。

---

## 12. Cancellation：取消不是自动消失

```python
async def work():
    try:
        await long_call()
    finally:
        cleanup()
```

异步任务被取消时，需要考虑：

```text
连接是否关闭
文件是否释放
child task 是否一起取消
下游请求是否支持取消
已经发生的副作用怎么办
```

这也是为什么 `try/finally`、Context Manager 和异步资源生命周期很重要。

---

## 13. `create_task` 不是“可靠后台任务”

```python
task = asyncio.create_task(do_work())
```

它只是把协程调度成 Event Loop Task。

它不自动保证：

- 进程崩溃后恢复；
- Task 被持久化；
- 至少一次执行；
- 跨实例接管；
- 长任务可靠状态。

所以 FastAPI / Backend 后面还会进一步区分：

```text
in-process async task
vs
reliable distributed task
```

---

## 14. 同步阻塞库怎样接到 asyncio

如果第三方 SDK 只有阻塞接口，不要直接在 Event Loop 线程里调用耗时阻塞函数。

常见做法：

```text
async application
→ thread pool offload blocking I/O
```

而纯 Python CPU-heavy 更常考虑 Process Pool。

注意：

> Offload 只是把阻塞搬走，不代表无限开线程不会出问题。

仍然要考虑 Pool Size、Queue、Backpressure。

---

## 15. ThreadPoolExecutor vs ProcessPoolExecutor

| 场景 | 常见选择 |
|---|---|
| Blocking HTTP / SDK | ThreadPool |
| 文件 I/O | ThreadPool |
| 纯 Python CPU-heavy | ProcessPool |
| C 扩展计算 | 取决于是否释放 GIL / 库实现 |

Process Pool 还要考虑：

- 参数能否序列化；
- 大对象复制成本；
- Worker 启动成本。

---

## 16. 一个 AI I/O 聚合例子

假设要并行访问三个搜索源，只要在 1.5 秒内拿到足够 Evidence 就可以回答。

```python
import asyncio

async def search_all(searchers, query):
    tasks = [
        asyncio.create_task(s(query))
        for s in searchers
    ]

    results = []

    try:
        async with asyncio.timeout(1.5):
            for task in asyncio.as_completed(tasks):
                result = await task
                results.append(result)
                if enough_evidence(results):
                    break
    except TimeoutError:
        pass
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

    return results
```

这个例子把真人面经里常追的几个点连起来：

```text
concurrent I/O
→ as_completed
→ timeout
→ early stop
→ cancellation
→ fallback / partial result
```

---

## 17. Failure / Trade-off

### 并发太少

- 延迟高；
- CPU / network 等待利用率低。

### 并发太多

- Provider 429；
- Socket / FD 耗尽；
- Thread Pool 饱和；
- Memory 上升；
- 下游被打爆。

所以“async 可以并发很多”不等于：

> 可以无限同时发请求。

Semaphore / Queue / Backpressure 仍然重要。

---

## 18. 🎯 面试怎么回答

### Thread / Process / Coroutine

> 线程共享进程内存，适合很多阻塞 I/O，但要处理共享状态；多进程隔离强，在传统 GIL 模式下适合纯 Python CPU 并行，但 IPC 和序列化成本更高；协程由 Event Loop 调度，适合大量可异步等待的 I/O，但 CPU-heavy 或同步阻塞调用会卡住事件循环。

### `gather` vs `as_completed`

> `gather` 适合并发启动一组任务并最终统一等待结果；`as_completed` 会按实际完成顺序逐个给出结果，适合谁先完成先处理、早停或 Progressive Aggregation。两者都不是“自动限流”，并发上限仍要额外控制。

### Lock / RLock / Semaphore

> `Lock` 保护互斥临界区；`RLock` 允许同一个线程重入同一把锁；`Semaphore` 更适合限制最多 N 个并发执行者。它们解决的问题不同。

---

## 19. ⚠️ 易错点

- `await` ≠ 新线程；
- `async def` ≠ 自动非阻塞；
- `gather` ≠ 自动限流；
- `create_task` ≠ 可靠后台任务；
- Timeout 后要考虑 Cancellation 和副作用；
- GIL ≠ 不需要 Lock；
- Semaphore 不是业务事务锁；
- ProcessPool 对大对象有 IPC / serialization cost；
- 线程池把阻塞移出 Event Loop，不代表线程可以无限增加。

---

## 20. 本章自测

<details>
<summary>1. `gather` 和 `as_completed` 最核心的区别是什么？</summary>

`gather` 更适合最终等待一组结果；`as_completed` 按任务实际完成顺序逐个返回结果，适合先完成先消费、早停或渐进聚合。

</details>

<details>
<summary>2. 为什么一个 `async def` 里执行长时间纯 Python 循环会拖慢所有请求？</summary>

因为 Event Loop 依赖任务在 await 等挂起点让出控制权；长 CPU 循环没有让出机会，会一直占用事件循环线程。

</details>

<details>
<summary>3. 为什么 Timeout 后还要考虑 Cancellation？</summary>

调用方停止等待不代表底层任务一定停止。如果任务继续运行，可能继续消耗资源或产生副作用，所以要明确取消、清理和幂等边界。

</details>

<details>
<summary>4. Lock 与 Semaphore 的目标有什么不同？</summary>

Lock 通常保护共享状态临界区，只允许一个执行者进入；Semaphore 允许最多 N 个并发执行者，更常用于容量控制和限流。

</details>

下一章：[13. 常见数据结构与复杂度](13-常见数据结构与复杂度.md)
