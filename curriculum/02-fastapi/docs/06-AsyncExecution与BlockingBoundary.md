# 06｜异步与并发：等待时谁在继续工作

[← 上一章](05-ResourceLifecycle.md) · [模块主页](../README.md) · [下一章 →](07-Streaming与SSE.md)

两个用户几乎同时访问接口，每个请求都要等待一小段时间。第一个请求等待时，第二个能不能继续？答案不取决于函数名前有没有 `async`，而取决于**代码在哪里执行，以及等待时有没有把执行机会交出去**。

Python 的协程、线程与进程已在语言基础模块建立。本章只研究它们进入 FastAPI 后的调用边界，不把“异步”当成性能魔法。

## 1. 先区分三种调用

| 写法 | 谁调用 | 主要执行位置 |
|---|---|---|
| `async def` 路由或依赖 | FastAPI | 事件循环，等待可异步操作时可让出执行机会 |
| 普通 `def` 路由或依赖 | FastAPI | 通过框架的线程池机制运行并等待结果 |
| 在 async 函数里直接调用普通 helper | 你的代码 | 普通函数调用，仍占用当前线程，除非明确转交 |

**框架不会扫描你的全部函数，然后自动把任何阻塞操作搬走。** 判断时必须找出“这一层究竟是谁发起调用”。[FastAPI 异步执行说明](https://fastapi.tiangolo.com/async/#very-technical-details)

## 2. 用三个接口观察等待位置

```python
# example: execution_app
import asyncio
import time
from threading import get_ident
from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

app = FastAPI()

def blocking_read():
    time.sleep(0.02)  # 模拟只有同步接口的阻塞读取
    return {"worker_thread": get_ident()}

@app.get("/async-wait")
async def async_wait():
    loop_thread = get_ident()
    await asyncio.sleep(0.02)  # 模拟可异步等待的 I/O
    return {"loop_thread": loop_thread}

@app.get("/sync-wait")
def sync_wait():
    return blocking_read()

@app.get("/offload")
async def offload():
    loop_thread = get_ident()
    result = await run_in_threadpool(blocking_read)
    return {"loop_thread": loop_thread, **result}
```

第三个接口中，`run_in_threadpool` 明确把阻塞函数交给线程执行；`await` 等它完成。结果中的两个线程编号通常不同。编号只是本次运行的观察值，不应写死到测试中。

下面则是**反例**，不要作为真实接口复制：

```python
async def bad_example():
    time.sleep(5)  # 当前事件循环线程被阻塞，async 这个名字不能改变它
```

若是很长的纯 Python 计算，改成线程调用也不等于获得理想的 CPU 并行。进程池、独立计算服务或任务系统各有成本，应按工作量选择。较短的普通计算不需要一律拆成远程任务。

## 3. 等待可以重叠，不代表时间凭空消失

```text
顺序：请求 A 等待并完成，再开始请求 B
并发：A 等待时推进 B，B 等待时再处理其他就绪任务
```

两个独立 I/O 操作可并发等待，因此总等待时间可能接近较慢的一项。但如果后一步必须用到前一步结果，就不能为了“并发”强行同时启动。

`asyncio.gather` 默认按输入顺序返回结果，并不保证哪个操作先完成。它也不是限流器，默认遇到某个子任务异常时，不会自动把所有兄弟任务都取消并收尾；需要一起结束的工作，必须明确安排其他子任务的取消和等待。[Python 任务组合](https://docs.python.org/3/library/asyncio-task.html)

## 4. 有限并发：先限制正在工作的数量

下面完整应用最多同时执行两个模拟调用。请求批量最多 8 项，避免先创建无限量等待任务。

```python
# example: bounded_app
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.slots = asyncio.Semaphore(2)
    app.state.active = 0
    app.state.peak = 0
    yield

app = FastAPI(lifespan=lifespan)

async def call_one(app, number):
    async with app.state.slots:
        app.state.active += 1
        app.state.peak = max(app.state.peak, app.state.active)
        try:
            await asyncio.sleep(0.01)
            return number * 2
        finally:
            app.state.active -= 1

@app.get("/batch")
async def batch(request: Request, size: int = Query(default=4, ge=1, le=8)):
    results = await asyncio.gather(*(call_one(request.app, i) for i in range(size)))
    return {"results": results, "peak": request.app.state.peak}
```

单独启动应用后请求 `/batch?size=4`，应得到 `[0,2,4,6]`，peak 不超过 2。四个任务已被创建，但同时持有许可、正在执行的最多两个；其余等待许可。

> ⚠️ Semaphore 限制的是正在持有许可的数量，不自动限制等待队列，也不限制一秒内总共发出多少请求。例子有批量上限；生产还应处理总请求数、排队上限和超时。进程内两个许可，也不是整个集群只有两个许可。

## 5. 线程池、连接池、下游能力要一起看

线程池是一组可重复使用的执行线程，连接池是一组可重复借用的连接；都不是无限资源。如果应用同时处理 100 个请求，而可用数据库连接只有 10 个，后面的请求就可能在等连接。增加 worker 可能增加请求处理能力，也会同时增加连接池和内存份数，未必减少等待。

| 正在等待什么 | 常见表现 | 首先要记录的量 |
|---|---|---|
| 事件循环被阻塞 | 多个无关异步接口一起变慢 | 事件循环延迟与阻塞调用 |
| 线程池空闲线程 | 同步路由排队 | 线程容量和等待时间 |
| 外部连接池 | SQL 或 HTTP 本身很快，但请求很慢 | 获取连接耗时 |
| 下游处理能力 | 请求已发出，响应迟迟不来 | 下游延迟、配额和错误率 |

Starlette 的同步执行会使用 AnyIO 的线程池容量机制；不要把某个默认容量数字当成所有版本、所有配置下都不变的保证。[Starlette 线程池](https://starlette.dev/threadpool/)

## 6. 怎样为一个真实接口选择执行方式

先问当前调用主要是在等待，还是在计算，再检查所用库的真实接口。

1. 有成熟的异步 I/O API，用 async 路由并 await。
2. 只有阻塞 I/O API，可用同步路由或明确线程转交，同时限制容量。
3. 持续的重计算，考虑进程或独立任务边界，避免占住请求事件循环。
4. 无论选哪种，都定义等待上限和结束后的清理。

这不是按“哪个关键词更先进”选方案。普通 `def` 也可能是合理选择，单个很小的 async 接口也不意味着需要复杂任务系统。

**练习：** 将 batch 的 size 设为 8，再设为 9。前者应完成，peak 仍不超过 2；后者应被输入约束拒绝。解释为什么“限制批量大小”和“限制同时调用”是两道不同的边界。

---

## 本章小结

并发的核心是安排等待与资源，不是给函数换一个前缀。框架执行同步路由与代码直接调用同步 helper 的路径不同。能同时推进多少工作，还受到线程、连接、下游配额和排队策略的共同限制。

## 🎯 面试怎么回答

**async def 中调用同步 SDK 会自动进线程池吗？**

> 不会。那是当前线程中的普通调用。FastAPI 对自己调用的同步路由和依赖有线程池处理，但不会自动转交它们内部的任意 helper。

**为什么并发限制不等于速率限制？**

> 并发限制控制同时在途的数量；请求很快时，同样两个许可一秒也能完成很多请求。速率限制还要约束时间窗口内的数量。

## ⚠️ 易错点

> ⚠️ await 不是新建线程，也不保证每次执行时都发生任务切换。

> ⚠️ 用 Semaphore 包住无限多任务，等待对象仍可能占满内存。

> ⚠️ 一次请求取消，不代表在线程里或远端执行的操作一定被停止。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 同步路由与 async 路由内直接 time.sleep 的差别是什么？</summary>

前者由框架转到线程执行，后者会阻塞事件循环线程。两者都消耗资源，但影响范围不同。

</details>

<details>
<summary>2. 四个 worker 各有两个 Semaphore 许可，是否实现全局最多两个调用？</summary>

没有。单看这项约束，四个进程合计可能同时放行八个调用；还需要考虑其他资源约束。

</details>

<details>
<summary>3. batch 结果是输入顺序，是否意味着实际执行也是严格顺序？</summary>

不是。gather 把结果按输入位置组织，执行可以交错。

</details>

## 知识回看与权威资料

- [FastAPI 异步语义](https://fastapi.tiangolo.com/async/)：区分路由、依赖和普通函数调用。
- [线程池容量](https://starlette.dev/threadpool/)：理解同步代码也有资源上限。
- [Python：并发与任务收尾](../../01-python/docs/12-线程-进程-协程-async-await.md)：回看事件循环、Task 和执行模型。
