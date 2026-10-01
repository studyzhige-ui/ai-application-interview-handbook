# 12. 线程、进程、协程与 async/await

[← 上一章：内存管理与 GIL](11-内存管理-垃圾回收-GIL.md) · [模块主页](../README.md) · [下一章：数据结构与复杂度 →](13-常见数据结构与复杂度.md)

三个接口各需要等待一段时间，是一个个等，还是让它们在同一时间段推进？其中一个失败以后，其他任务怎么办？本章把并发理解为**安排执行、控制共享与容量、管理失败和结束**，而不只是记几个启动函数。

示例使用 Python 3.11+。多进程示例应保存成 `.py` 文件运行；异步脚本用 `asyncio.run(...)` 作为入口。Notebook 已有事件循环时，使用其顶层 `await` 入口，不在已有循环里再套 `asyncio.run`。

```text
任务主要在等待，还是在计算？
→ 是否有可异步等待的接口？
→ 需要共享内存，还是隔离？
→ 同时允许多少工作、排队多少工作？
→ 结果按什么顺序消费？
→ 超时／失败／取消怎样传播与收尾？
```

## 1. 并发与并行：同一时间段，还是同一时刻

**Concurrency（并发）** 让多个任务在同一时间段交替推进；**Parallelism（并行）** 让多个任务在同一时刻真正同时执行。

```text
顺序等待：A 发请求──等待──处理 → B 发请求──等待──处理
并发等待：A 发请求──等待────────处理
          B 发请求────等待──────处理
```

等待网络时，CPU 不必一直替这个请求做运算。一个线程里的事件循环可以利用等待间隙推进其他任务，但这不表示两个 Python 计算循环正在两个核上同时运行。真正的 CPU 并行还取决于解释器模式、进程与本地库实现，接上第 11 章的 GIL 边界。

## 2. 进程与线程：先看内存和调度边界

### 2.1 Process（进程）：独立执行环境，通信有成本

进程通常有独立地址空间。把工作放到不同解释器进程，可以在传统 GIL 模式下进行纯 Python 的 CPU 并行；但跨进程不能把普通变量当成自然共享的同一份对象。

```python
from multiprocessing import Process  # 标准库进程对象


def work(label):             # 子进程入口定义在模块顶层，方便被导入和序列化定位
    print("working", label)  # 在子进程中执行；不同进程打印先后不作保证

if __name__ == "__main__":   # 防止子进程导入模块时再次启动一批子进程
    workers = [Process(target=work, args=(i,)) for i in range(2)]  # target 传函数对象，args 传参数元组
    for process in workers:  # 先把工作进程都启动
        process.start()      # 启动新进程，而不是在本进程直接调用 work
    for process in workers:  # 再逐个等待结束
        process.join()       # 等待该子进程退出
```

`target=work` 不是 `target=work()`：前者交出待执行函数，后者提前执行了函数。`args=(i,)` 的逗号构成单元素元组。

进程提供较强内存隔离，一个工作进程崩溃不一定破坏另一个进程的内存；但启动、通信、数据转换和每个进程的独立状态都有成本。**IPC（Inter-process Communication，进程间通信）** 可能涉及序列化，大模型客户端、缓存、大对象在多个进程中也可能占用多份资源。

进程启动方式取决于平台与 Python 版本，不能把某个平台的默认方式当成永久规则。入口保护和可导入的顶层工作函数，是理解跨启动方式示例的基础。

### 2.2 Thread（线程）：共享内存，需要同步状态

```python
from threading import Thread  # 标准库线程对象


def work(label):             # 线程执行的函数
    print("working", label)  # 在线程里运行

threads = [Thread(target=work, args=(i,)) for i in range(2)]  # 创建两个线程对象
for thread in threads:       # 先全部启动
    thread.start()           # 交给操作系统调度
for thread in threads:       # 再等待全部结束
    thread.join()            # 等待当前这个线程结束
```

线程共享同一进程的大部分内存，适合阻塞网络 SDK、文件 I/O、没有异步接口的第三方库等场景。共享方便，也带来 **Race Condition（竞态条件）**、**Deadlock（死锁）**、状态污染和 **Thread Pool Saturation（线程池饱和）** 风险。

不要在创建一个线程后立刻 join，再创建下一个，误以为这样已经让全部工作并发启动；先启动一组、再等待，是上面代码分两轮的原因。

## 3. 共享状态与并发容量：三种同步工具别混用

### 3.1 Lock：保护不可交错的临界区

```python
from threading import Lock, Thread  # 锁与线程

count = 0                    # 多个线程共同更新的计数
lock = Lock()                # 保护这个共享计数的同一把锁


def increment():             # 每个线程增加一千次
    global count             # 重新绑定模块级 count
    for _ in range(1000):    # 重复执行
        with lock:           # 获取锁；正常或异常离开时释放
            count += 1       # 把读、加一、写回作为受保护的整体

threads = [Thread(target=increment) for _ in range(2)]  # 两个执行者
for thread in threads:       # 启动全部线程
    thread.start()           # 运行 increment
for thread in threads:       # 等待全部完成
    thread.join()            # 等待对应线程
print(count)                 # 2000
```

**Lock（互斥锁）** 使所有遵守同一锁约定的执行者不能同时进入临界区。GIL 或某个容器的内部锁，不能替代一段多步骤业务操作的整体保护。

### 3.2 RLock：允许同一个线程重入同一把锁

```python
from threading import RLock  # 可重入锁

lock = RLock()               # 创建一把可由同一线程再次获取的锁


def inner():                 # 内层功能自己也保护共享状态
    with lock:               # 当前线程可以再次获取已经持有的 RLock
        return "done"        # 返回结果，退出时释放本层获取


def outer():                 # 外层功能先获取同一把锁
    with lock:               # 第一次获取
        return inner()       # 内部再次获取同一把锁

print(outer())               # done
```

**Reentrant Lock（可重入锁）** 每次获取都需要相应释放，嵌套 with 会配对完成。换成普通 Lock，同一个线程可能把自己卡住；但 RLock 不能自动解决多把锁之间的循环等待，也不能弥补混乱的锁顺序设计。

### 3.3 Semaphore：限制同时进入的人数

```python
from threading import Semaphore  # 线程使用的计数信号量

sem = Semaphore(5)                # 最多允许五个执行者同时持有许可


def limited_call(job):            # job 是要执行的同步函数
    with sem:                     # 取得许可；不足时等待
        return job()              # 执行同步工作，退出时归还许可
```

**Semaphore（信号量）** 管理容量，适合“最多十个 OCR”“最多二十个同步请求”“最多四个 GPU 作业”。Lock 通常保护共享条件，Semaphore 通常限制同时在途的数量。

**并发数限制不等于每秒请求数限制。** 五个许可下，如果每个请求极快，一秒内仍可能发出很多请求；按时间的 Rate Limit（速率限制）需要额外设计。

## 4. 协程与事件循环：不靠新线程来表达等待

### 4.1 不含 yield 的 async def 定义协程函数，调用先得到协程对象

```python
import asyncio               # 标准库异步调度工具

async def fetch_data():      # 定义协程函数
    await asyncio.sleep(0.01)  # 模拟可异步等待的 I/O，让出等待期间的执行机会
    return "data"            # 等待结束后返回结果

coro = fetch_data()          # 得到协程对象，不是已经得到字符串 'data'
result = asyncio.run(coro)   # 脚本入口创建事件循环，驱动协程执行到结束
print(result)                # data
```

**Coroutine（协程）** 可以在等待点挂起，并在条件就绪后恢复。调用普通协程函数得到的对象还需要 await 或被调度，否则不能把它当成已经完成的业务结果。

### 4.2 await 既不是新线程，也不保证每次都切换

`await operation` 表示等待一个 **Awaitable（可等待对象）** 的完成。在确实需要等待时，当前任务可以挂起，让事件循环推进其他就绪任务；如果被等待操作已经可以立刻完成，不一定发生实际切换。

```text
Ready（就绪）的任务 A → 执行 → await 未完成 I/O → Suspended（挂起）
Ready（就绪）的任务 B → 执行 → await 未完成 I/O → Suspended（挂起）
A 的 I/O 就绪 → Resume（恢复）A → 继续执行
```

**Event Loop（事件循环）** 管理这些就绪与恢复机会。`await` 不表示创建线程、创建进程或获得可靠后台执行能力。

### 4.3 事件循环最怕长时间不让出执行权

```python
async def bad():             # 错误设计：名字是异步，内部却一直做同步计算
    total = 0                # 累计变量
    for i in range(10**9):   # 很长的纯 Python 计算循环
        total += i           # 没有可等待操作，不给其他协程推进的机会
    return total             # 可能很久后才结束；这里只定义，不运行这个反例
```

正确方向是将适合的 CPU 工作交给进程池等执行模型；同步阻塞 I/O 则可以移到线程池。仅仅加上 `async def` 不会把同步代码变成非阻塞，也不要把 `time.sleep()` 当成 `await asyncio.sleep()`。

### 4.4 async for：等待下一项，而不是等待整个列表

普通 `for` 调用 `iter/next`；异步数据源可能要等待网络才能给出下一项，因此使用 `__aiter__/__anext__`。`__aiter__` 返回异步迭代器；`__anext__` 返回可等待对象，完成后得到一项，结束时以 `StopAsyncIteration` 报告。

```python
import asyncio

async def chunks():              # 含 yield 的 async def 是异步生成器函数
    for text in ["你", "好"]:
        await asyncio.sleep(0)    # 模拟每一项到来前的异步等待
        yield text               # 产出这一项，并暂停在这里

async def main():
    stream = chunks()            # 得到异步生成器；不是协程返回值
    async for text in stream:    # 逐次等待下一项
        print(text)              # 依次输出 你、好

asyncio.run(main())
```

时间线是“请求下一项 → 等待 → yield 你 → 循环体消费 → 再请求 → yield 好 → 再请求 → 结束”。`async for` 本身不创建一批并行任务；消费者通常逐项推动生产者。不能对异步生成器直接 `await chunks()`，也不能用普通 `list(stream)` 消费它。提前退出时，如果生成器持有资源，应使用 `contextlib.aclosing(stream)` 等明确关闭范围，让 `finally` 有确定的收尾机会。

`async with` 对应可等待的 `__aenter__/__aexit__`。第 07 章的“一次 yield 划分获取与清理”也能用 `@contextlib.asynccontextmanager` 表达：获取和清理都可以 await。FastAPI 的异步资源依赖正是接在这两项语言基础上。

## 5. 多任务调度：按输入顺序收集，还是谁先完成先处理

### 5.1 Task 是被事件循环管理的执行单元

`asyncio.create_task(coro)` 把协程组织成 **Task（异步任务）** 并交给事件循环调度。调用者应保留必要引用，管理它的结果、异常与结束；不要只启动一批任务就忘记它们。

下面的完整示例同时演示两种结果消费模式：

```python
import asyncio                       # 异步运行与调度

async def fetch(label, delay):        # 用延迟模拟不同数据源
    await asyncio.sleep(delay)       # 非阻塞地等待
    return label                     # 返回数据源标签

async def main():                    # 一次异步程序的入口
    results = await asyncio.gather(  # 并发调度这些协程，成功时统一得到结果
        fetch("slow", 0.03),         # 第一个输入较慢
        fetch("fast", 0.01),         # 第二个输入较快
    )
    print(results)                   # ['slow', 'fast']：按输入顺序排列，不是完成顺序

    tasks = [                        # 再创建一组独立的演示任务
        asyncio.create_task(fetch("slow", 0.03)),  # 显式创建较慢任务
        asyncio.create_task(fetch("fast", 0.01)),  # 显式创建较快任务
    ]
    for pending in asyncio.as_completed(tasks):    # 按完成进度逐个提供可等待结果
        result = await pending                    # 取得这一次完成的结果
        print(result)                             # 本例通常先 fast，再 slow

asyncio.run(main())                  # 在普通脚本中启动并等待全部演示结束
```

### 5.2 gather：统一收集不代表自动处理所有失败

**gather（聚合等待）** 在全部成功时按输入顺序返回结果。默认情况下，一个子任务抛异常可以让等待者立即收到该异常，但其他子任务不会因此自动全部取消；不要把它当成“失败即停止整组”的保证。

`return_exceptions=True` 会把异常作为结果收集，调用方必须检查，不能把异常对象当业务成功结果。gather 也不自动限制请求数量。

### 5.3 as_completed：消费模式不同，不是“天然更快”

**as_completed（按完成顺序消费）** 适合先完成先处理、渐进聚合、First Useful Result（第一个有效结果）与早停。普通 for 迭代接口给出的对象用于 await 结果，不应在所有版本／用法中都假定它与原 Task 是同一对象。

如果提前 break，未完成任务不会因为你不读结果就自动消失；需要明确取消与收尾，完整例子在本章后面。

### 5.4 TaskGroup：把一组子任务的生命周期绑定在一起

Python 3.11+ 的 **TaskGroup（任务组）** 提供结构化并发管理：离开上下文前等待子任务；某个子任务出现非取消异常时，通常会取消同组其他任务并等待收尾，再报告相应异常组。

```python
import asyncio                       # 使用 Python 3.11+ 的 TaskGroup

async def fetch(label):               # 一个可等待的演示任务
    await asyncio.sleep(0.01)         # 模拟等待
    return label                     # 正常返回

async def main():                    # 管理一组相关子任务
    async with asyncio.TaskGroup() as group:  # 进入任务组生命周期
        a = group.create_task(fetch("A"))   # 创建并登记子任务 A
        b = group.create_task(fetch("B"))   # 创建并登记子任务 B
    print(a.result(), b.result())    # 正常离开时两个任务已完成，输出 A B

asyncio.run(main())                   # 脚本入口
```

`async with` 是可异步进入／退出的上下文管理协议，不会阻塞着持有普通线程锁去等待。TaskGroup 管任务关系，不自动提供限流、持久化或业务回滚。

### 5.5 异常组为什么不能只按一条异常理解

多个子任务可能在相近时间失败，任务组需要在等待它们收尾后保留多份错误。`ExceptionGroup` 把相关异常组织成一组，`except* ValueError` 可以处理其中匹配的子组；不匹配的部分继续传播。它不是把异常对象变成普通成功结果。

```python
try:
    raise ExceptionGroup("两个输入错误", [ValueError("A"), ValueError("B")])
except* ValueError as group:
    print(len(group.exceptions))  # 2
```

这段只展示分组处理语法。TaskGroup 的真实异常组可来自任务和退出过程；取消、KeyboardInterrupt、SystemExit 有专门传播规则，不应笼统说所有错误都变成同一种组。

## 6. 超时、取消、替代路径：把失败后发生什么讲完整

### 6.1 Timeout 是等待预算，不是物理强制终止

```python
import asyncio                       # 提供 wait_for

async def request():                 # 模拟一个慢操作
    await asyncio.sleep(1)           # 等待一秒
    return "ok"                      # 正常完成结果

async def main():                    # 调用方只愿意等待较短时间
    try:                             # 在预算边界处理超时
        result = await asyncio.wait_for(request(), timeout=0.01)  # 超时后请求取消内部操作
        print(result)                # 本例不会正常到达
    except TimeoutError:             # 超时作为明确失败被观察到
        print("超过等待预算")         # 不假装已经拿到成功结果

asyncio.run(main())                   # 运行演示
```

`wait_for` 超时后通常会取消被等待任务，并等待取消过程完成。因此实际耗时可能超过给定秒数；如果底层不合作或资源清理很慢，超时不是万能硬中断。

`asyncio.timeout(...)` 则把当前任务的一段异步工作放入预算范围，并在退出上下文时把自身触发的取消转换成 TimeoutError。通常在 `async with` 外面捕获这个超时。

### 6.2 Cancellation：请求取消，再让任务处理退出

```python
import asyncio                       # 提供任务调度与 CancelledError

async def work():                     # 一个需要清理的长任务
    try:                             # 保护资源使用范围
        await asyncio.sleep(10)      # 模拟可取消等待
    except asyncio.CancelledError:   # 明确观察取消请求
        print("收到取消")             # 可以记录必要信息
        raise                        # 不吞掉取消，继续传播
    finally:                         # 正常或取消退出都做清理
        print("cleanup：清理")        # 模拟关闭连接等工作

async def main():                    # 创建并管理子任务
    task = asyncio.create_task(work())  # 保留 Task 引用
    await asyncio.sleep(0)           # 给 work 一次开始执行的机会
    task.cancel()                    # 发出取消请求，不等于这一行已经完成全部清理
    try:                             # 等待子任务真正处理取消
        await task                   # 收尾完成后观察到 CancelledError
    except asyncio.CancelledError:   # 这里确认自己发出的取消已被处理
        print("任务已结束")           # 不把主动停止当意外业务失败

asyncio.run(main())                   # 运行演示
```

需要检查连接、文件、子任务、下游请求与已发生的副作用。`CancelledError` 属于 BaseException 分支，不应被随意吞掉。父任务取消也不自动意味着任意创建、未纳入管理的子任务一定被正确收尾。

### 6.3 Fallback：替代操作也需要预算和副作用边界

```python
import asyncio                       # 超时工具

async def with_fallback(primary, fallback):  # 输入是两个可调用的协程函数
    try:                             # 先尝试主路径
        return await asyncio.wait_for(primary(), timeout=2)  # 分配主路径预算
    except TimeoutError:             # 只在这类失败下尝试替代路径
        return await asyncio.wait_for(fallback(), timeout=1) # 替代路径也有自己的预算
```

**Fallback（替代路径）** 不是无限等待的出口。需要知道主路径是否真的停止、是否已产生副作用，两条路径会不会重复写入，以及结果是否需要标注来源或版本。外层还要分配整体 **Deadline Budget（截止时间预算）**；这是后续 Backend 模块的完整职责。

## 7. 把同步库接入异步程序：移动阻塞，不是消灭成本

### 7.1 线程池承接阻塞 I/O

```python
import asyncio                       # 异步入口与线程池桥接
import time                          # 用同步 sleep 模拟阻塞 SDK


def blocking_sdk():                  # 普通同步函数
    time.sleep(0.01)                 # 当前线程会阻塞等待
    return "sdk result"              # 模拟返回

async def main():                    # 事件循环中的任务
    result = await asyncio.to_thread(blocking_sdk)  # 将同步调用交给线程，不在事件循环线程直接阻塞
    print(result)                    # sdk result

asyncio.run(main())                   # 脚本入口
```

**Offload（转交执行）** 不等于无限创建线程，也不表示取消等待方就能强制停止已经运行的线程函数。线程池容量、排队长度、下游限制仍要管理。

### 7.2 ThreadPoolExecutor 与 ProcessPoolExecutor

| 工作 | 常见起点 | 主要代价／边界 |
|---|---|---|
| 阻塞 HTTP／同步 SDK、文件 I/O | ThreadPoolExecutor（线程池） | 共享状态、池饱和、运行中函数难强制终止 |
| 传统 GIL 下的纯 Python 重计算 | ProcessPoolExecutor（进程池） | 启动、参数序列化、进程间传输与多份状态 |
| 本地编译库计算 | 按库实现选择 | 是否释放 GIL、库内部是否已开线程 |

进程池接入异步等待的完整入口示例：

```python
import asyncio                       # 事件循环
from concurrent.futures import ProcessPoolExecutor  # 进程池


def cpu_work(n):                     # 顶层工作函数，便于子进程定位
    return sum(i * i for i in range(n))  # 演示纯 Python 计算

async def main(pool):                # 使用外部已管理的进程池
    loop = asyncio.get_running_loop()  # 取得当前运行的事件循环
    return await loop.run_in_executor(pool, cpu_work, 10000)  # 转交计算并异步等结果

if __name__ == "__main__":           # 保存为 .py 运行；保护进程入口
    with ProcessPoolExecutor(max_workers=2) as pool:  # 显式限制工作进程数量并管理退出
        print(asyncio.run(main(pool)))  # 等待结果，之后退出并关闭池
```

大对象传进传出可能抵消并行收益，不是“放进 ProcessPool 就一定更快”。本例规模只用于演示语义，不是性能基准。

## 8. 容量与可靠性：别把能启动当作能承受

### 8.1 协程使用适合自己的同步工具

在事件循环线程里等普通 `threading.Lock`，可能阻塞整个循环；尤其不要持有它跨越需要其他协程推进的 await。协程之间常用 `asyncio.Lock`、`asyncio.Semaphore` 与 `async with`。

信号量限制同时执行数，却不限制你提前创建多少 Task。一口气为百万项创建百万任务，即使只放行十个，也已经建立大量排队对象。大规模任务源更适合 **Bounded Queue（有界队列）** 与固定数量 Worker（工作协程）：生产者 `await queue.put(...)` 在队列满时等待，形成 **Backpressure（背压）**。

以容量为 2 的队列和一个工作协程为例，生产者按 A、B、C、D 提交：

```text
put A、put B 完成 → 队列 [A,B]
put C 等待       → 生产者暂停，不能继续无界积压
worker get A     → 队列 [B]，空出一个排队槽位
put C 完成       → 队列 [B,C]，worker 正在处理 A
put D 又等待     → 下游处理速度反过来约束上游
```

槽位在 `get` 取走元素时释放，不是等处理结束；`task_done()` 则表示这项工作已完成，配合 `join()` 等待所有登记工作收尾。队列容量限制的是排队项，实际驻留还包括工作协程正在处理的项。固定 W 个工作协程、队列容量 Q，常见在途上界约为 Q+W 项（另计生产者当前持有项）；每项大小若无界，总内存仍不一定有界。

### 8.2 create_task 不等于可靠后台任务

它只在当前进程的事件循环中调度工作，不自动提供崩溃后恢复、持久化、至少一次执行、跨实例接管或长期状态管理。

```text
In-process Task（进程内任务）
≠ Reliable Distributed Task（可靠分布式任务）
```

短任务也要有人观察异常、保存引用、安排关闭。需要跨进程故障恢复时，应在 Backend 层使用相应任务系统，不能仅换一个函数名。

### 8.3 太少与太多并发都有代价

并发太少，等待时间没有被利用，整体延迟可能高；并发太多，则可能遇到 Provider 429（服务方限流）、Socket / FD（连接／文件描述符）耗尽、线程池饱和、内存上升和下游超载。选择并发量要同时看活动任务、排队任务、单任务内存和外部容量。

## 9. 完整聚合例子：成功、部分失败、早停、超时、取消收尾

下面以有限数量的搜索源为输入。每个搜索源是“接收 query、返回可等待结果”的函数；示例把一次成功返回算作一份结果，真实 Evidence（证据）是否有效应有自己的业务判断。

```python
import asyncio                       # 全部调度在当前进程内完成

async def search_all(searchers, query, *, min_results=2, concurrency=3, timeout=1.5):
    if min_results < 1 or concurrency < 1 or timeout <= 0:  # 拒绝无效的示例配置
        raise ValueError("参数必须为正")  # 不建立零容量等待等无效流程
    gate = asyncio.Semaphore(concurrency)  # 控制同时访问下游的数量

    async def call_one(index, searcher):  # 为每个源附带编号与失败信息
        async with gate:                 # 等待并持有异步许可
            try:                         # 在单个源边界隔离普通失败
                data = await searcher(query)  # 调用这个搜索源
            except Exception as error:   # 本例将源失败归类返回；真实项目宜限定预期异常
                return "error", {"source": index, "error_type": type(error).__name__}
            return "ok", {"source": index, "data": data}  # 返回成功来源与内容

    tasks = [asyncio.create_task(call_one(i, s)) for i, s in enumerate(searchers)]  # 保存全部子任务引用
    results, errors = [], []             # 分别收集成功与失败，不把失败当成功
    timed_out = False                    # 标记是不是整体等待预算耗尽
    try:                                 # 管理消费与退出路径
        async with asyncio.timeout(timeout):  # 给聚合阶段一个等待预算
            for pending in asyncio.as_completed(tasks):  # 谁完成先消费谁
                kind, value = await pending             # 等待本次完成结果
                if kind == "error":                     # 单源失败
                    errors.append(value)                # 保留来源与错误类别
                else:                                   # 单源成功
                    results.append(value)               # 收集结果
                    if len(results) >= min_results:     # 已满足本例早停条件
                        break                           # 不再等待更多业务结果
    except TimeoutError:                 # 预算耗尽时保留已经得到的部分结果
        timed_out = True                 # 不把部分结果误标成完整成功
    finally:                             # 正常早停、超时、外部取消都经过收尾
        for task in tasks:               # 逐个检查尚未完成的子任务
            if not task.done():          # 已结束的任务不必再请求取消
                task.cancel()            # 先请求取消
        await asyncio.gather(*tasks, return_exceptions=True)  # 再等待子任务处理取消并回收结果／异常
    return {                             # 明确返回部分成功状态
        "results": results,              # 停止前消费到的成功结果
        "errors": errors,                # 停止前消费到的错误信息
        "timed_out": timed_out,          # 是否耗尽聚合预算
        "enough": len(results) >= min_results,  # 是否达到本例数量目标
    }

async def fast_source(query):            # 可独立运行的模拟数据源 A
    await asyncio.sleep(0.01)            # 模拟等待
    return f"A: {query}"                 # 返回文本

async def slow_source(query):            # 模拟数据源 B
    await asyncio.sleep(0.03)            # 等待稍长
    return f"B: {query}"                 # 返回文本

async def main():                        # 演示正常取得两份结果
    report = await search_all([fast_source, slow_source], "Python")  # 传函数对象，不提前调用
    print(report["enough"])              # True

asyncio.run(main())                       # 普通脚本入口
```

需要读懂的不是代码长度，而是职责链：**并发启动 → 容量限制 → 按完成消费 → 错误归类 → 预算／早停 → 取消 → 等待收尾 → 明确部分结果状态**。

本例不会吞掉外部的 CancelledError，它在收尾后继续传播；请求取消与真正结束也不是同一个时刻。下游不响应取消、线程工作继续运行、清理耗时或进程强杀等情况，仍需在具体系统中设计边界。返回前收尾也可能使实际耗时超过业务等待预算；这比错误承诺“1.5 秒时所有外部操作物理停止”准确。

本例会为有限输入建立全部 Task。大量或无限输入应改用有界队列与固定工作协程，不能仅调整 Semaphore 数值就宣称内存有界。

本章依据：[asyncio 协程与任务](https://docs.python.org/3.14/library/asyncio-task.html)、[线程同步](https://docs.python.org/3.14/library/threading.html)、[multiprocessing](https://docs.python.org/3.14/library/multiprocessing.html)、[concurrent.futures](https://docs.python.org/3.14/library/concurrent.futures.html)、[asyncio 同步原语](https://docs.python.org/3.14/library/asyncio-sync.html)。

---

## 10. 🎯 面试怎么回答

### Thread / Process / Coroutine

> 线程共享进程内存，适合很多阻塞 I/O，但要处理共享状态；多进程隔离强，在传统 GIL 模式下适合纯 Python CPU 并行，但 IPC 和序列化成本更高；协程由 Event Loop 调度，适合大量可异步等待的 I/O，但 CPU-heavy 或同步阻塞调用会卡住事件循环。

### `gather` vs `as_completed`

> `gather` 适合并发启动一组任务并最终统一等待结果；`as_completed` 会按实际完成顺序逐个给出结果，适合谁先完成先处理、早停或 Progressive Aggregation。两者都不是“自动限流”，并发上限仍要额外控制。

### Lock / RLock / Semaphore

> `Lock` 保护互斥临界区；`RLock` 允许同一个线程重入同一把锁；`Semaphore` 更适合限制最多 N 个并发执行者。它们解决的问题不同。

---

## 11. ⚠️ 易错点

- `await` ≠ 新线程；
  正确理解：在协程控制流中等待，真正挂起时才给其他就绪任务机会。
- `async def` ≠ 自动非阻塞；
  正确做法：把同步阻塞 I/O 或长 CPU 工作移交适合的执行模型。
- `gather` ≠ 自动限流；
  正确做法：额外限制活动数与排队数，并明确异常处理策略。
- `create_task` ≠ 可靠后台任务；
  正确理解：当前进程内调度，不自带持久化与故障接管。
- Timeout 后要考虑 Cancellation 和副作用；
  正确做法：取消、等待收尾，并确认下游动作是否已经发生。
- GIL ≠ 不需要 Lock；
  正确做法：用业务同步保护多步骤共享条件。
- Semaphore 不是业务事务锁；
  正确理解：主要控制同时进入数，也不等于固定每秒速率。
- ProcessPool 对大对象有 IPC / serialization cost；
  正确理解：进程间通信与序列化成本可能抵消并行收益。
- 线程池把阻塞移出 Event Loop，不代表线程可以无限增加。
  正确做法：限制池容量和队列，并给下游留出承载边界。

---

## 12. 本章自测

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
