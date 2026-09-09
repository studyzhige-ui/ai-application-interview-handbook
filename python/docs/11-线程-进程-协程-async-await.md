# 11. 线程、进程、协程与 async/await

并发是 Python 面试里的高频进阶题。先记住一句话：

> **线程适合很多 I/O 等待，多进程适合纯 Python CPU 密集，协程适合大量可异步等待的 I/O 任务。**

这只是经验法则，真实选择还要结合任务、库支持、进程通信成本、部署方式等。

---

## 1. 进程 Process

进程是操作系统进行资源分配和隔离的重要单位之一。不同进程拥有各自独立的地址空间。

```python
from multiprocessing import Process

def work():
    print("working")

p = Process(target=work)
p.start()
p.join()
```

### 优点

- 进程之间隔离性较强；
- 在传统 CPython/GIL 模式下，可以通过多个进程利用多个 CPU 核执行纯 Python CPU 密集任务。

### 缺点

- 创建和切换成本通常高于线程；
- 数据不能像同一进程内线程那样直接共享；
- 进程间通信 IPC 有额外成本。

---

## 2. 线程 Thread

一个进程内部可以有多个线程，它们共享进程的大部分内存空间。

```python
from threading import Thread

def work():
    print("working")

t = Thread(target=work)
t.start()
t.join()
```

### 优点

- 共享数据方便；
- 通常比进程更轻量；
- 适合 I/O 密集任务。

### 风险

共享内存意味着可能发生：

- 竞态条件；
- 数据不一致；
- 死锁。

---

## 3. 为什么需要锁

```python
from threading import Lock

lock = Lock()
count = 0

def safe_inc():
    global count
    with lock:
        count += 1
```

锁保证一段临界区在同一时刻只允许特定数量的线程进入，从而保护共享状态。

⚠️ **有 GIL 不等于业务代码天然线程安全。**

不要因为 CPython 有 GIL 就认为多步骤共享状态操作一定安全。线程可能在操作之间切换，库函数也可能释放 GIL。

---

## 4. 进程 vs 线程

| 对比 | 进程 | 线程 |
|---|---|---|
| 内存空间 | 通常独立 | 同进程内共享 |
| 创建开销 | 较高 | 较低 |
| 数据共享 | 需要 IPC 等机制 | 相对方便 |
| 隔离性 | 更强 | 较弱 |
| CPU 密集 | 常用多进程 | 传统 GIL 下受限 |
| I/O 密集 | 可以 | 常见选择 |

---

# 5. 协程 Coroutine

💡 **新手理解**：协程可以理解为“任务主动在等待时让出执行权，等条件满足后再继续”。

它不像操作系统线程那样由 OS 直接调度，而通常由用户态事件循环来安排执行。

适合：

- 大量网络连接；
- 高并发 API 请求；
- WebSocket；
- 爬虫；
- 大量可异步的数据库/缓存操作。

---

## 6. `async def`

```python
async def fetch_data():
    return "data"
```

调用异步函数：

```python
coro = fetch_data()
```

通常得到的是**协程对象**，并不会像普通函数一样立即完整执行。

---

## 7. `await`

```python
import asyncio

async def task():
    await asyncio.sleep(1)
    return "done"
```

`await` 的核心作用：

> 当前协程等待另一个 awaitable 完成时，可以暂时让出控制权，让事件循环去执行其他可运行任务。

⚠️ `await` 不是“开启一个新线程”。

---

## 8. `asyncio.run`

```python
import asyncio

async def main():
    print("start")
    await asyncio.sleep(1)
    print("end")

asyncio.run(main())
```

`asyncio.run()` 是运行顶层异步入口的常见方式。

---

## 9. 并发执行多个协程

如果这样写：

```python
await task1()
await task2()
```

很多时候仍然是先等 task1，再运行 task2。

想让多个任务并发推进，可以使用 `asyncio.gather()` 或任务对象：

```python
async def main():
    result1, result2 = await asyncio.gather(
        task1(),
        task2(),
    )
```

---

## 10. 一个直观例子

```python
import asyncio

async def download(name, seconds):
    print(f"{name} start")
    await asyncio.sleep(seconds)
    print(f"{name} end")
    return name

async def main():
    results = await asyncio.gather(
        download("A", 2),
        download("B", 1),
    )
    print(results)

asyncio.run(main())
```

两项任务都在等待期间让出执行权，因此总耗时通常接近较慢任务的时间，而不是两者简单相加。

---

## 11. 为什么协程适合 I/O，不适合直接做重 CPU 计算

事件循环通常依赖任务主动在 `await` 点让出控制权。

如果你写：

```python
async def bad_task():
    total = 0
    for i in range(10**9):
        total += i
```

内部没有可让出的异步等待，而且 CPU 循环非常重，就可能长时间阻塞事件循环，其他协程也得不到执行机会。

因此 CPU 密集工作通常应该：

- 放到进程池；
- 使用适合的原生扩展/计算库；
- 或重新设计执行方式。

---

## 12. `async` 与 `await` 为什么经常一起出现

- `async def` 定义协程函数；
- 调用协程函数得到协程对象；
- `await` 用于在异步上下文中等待 awaitable，并允许当前协程挂起；
- 事件循环负责调度其他可运行任务。

🎯 **面试回答**：`async` 用于定义异步协程函数，`await` 用于在协程内部等待另一个可等待对象。当等待 I/O 时，当前协程可以挂起，把执行机会交给事件循环中的其他任务，从而实现单线程下的大量 I/O 并发。

---

## 13. 阻塞函数不能直接“变异步”

例如在异步函数里直接调用阻塞式函数：

```python
async def main():
    time.sleep(5)  # 阻塞事件循环
```

这里 `async def` 并不会自动把 `time.sleep` 变成非阻塞。

应该使用异步版本：

```python
await asyncio.sleep(5)
```

如果第三方库只有同步阻塞 API，可以考虑线程池等桥接方式。

---

## 14. ThreadPoolExecutor / ProcessPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
```

可以用统一风格管理线程池和进程池。

经验上：

- `ThreadPoolExecutor`：阻塞 I/O；
- `ProcessPoolExecutor`：CPU 密集。

---

## 15. 高频面试题

### Q1：线程、进程、协程区别？

🎯 推荐框架：

- 进程资源隔离强，适合 CPU 并行，但开销较高；
- 线程共享进程内存，通信方便，适合 I/O 并发，但需要处理共享状态和线程安全；
- 协程是用户态调度的轻量并发方式，通常通过事件循环在等待 I/O 时切换，非常适合大量异步 I/O。

### Q2：有 GIL 为什么还需要线程锁？

GIL 保护的是解释器执行层面的某些共享状态，并不等价于你的多步骤业务逻辑是原子的。多个线程仍可能交错执行并产生竞态，所以共享可变状态仍可能需要锁或其他同步机制。

### Q3：协程一定比线程快吗？

不是。它们适用场景不同。协程的优势主要在大量可异步 I/O 任务的调度开销和可扩展性；如果库没有异步接口，或者任务是 CPU 密集，协程未必合适。

下一章：[12. 常见数据结构与复杂度](12-常见数据结构与复杂度.md)
