# 并发工作由谁执行，等待放在哪里

[← 怎样传递结果，断线后怎样继续](03-ServiceCommunication与StreamingReliability.md) · [模块主页](../README.md) · [连接怎样复用，容量怎样计算 →](05-ConnectionPool与ResourceCapacity.md)

处理一份文档时，服务大部分时间可能在等网络模型返回。只服务一个用户会浪费等待时间；同时接受十万项工作又会挤满内存。并发设计要回答的不是“能开多少协程”，而是哪些工作可以交错进行、由谁执行、排队有多长、何时释放资源。

## 1. 先区分同时推进与同时计算

一份文档等待模型响应时，服务可以开始处理另一份文档。两项工作在同一段时间内都有进展，这叫 **并发** 。如果两个 CPU 核此刻分别处理一项计算，则还发生了 **并行** 。利用等待间隙，不等于增加了计算核心。

再看工作由谁承载。它们不是三个可以直接互换的名字：

| 承载方式 | 保存什么，谁来调度 | 怎样理解本例 |
|---|---|---|
| 进程 | 通常有独立地址空间，由操作系统管理执行资源 | 两个服务进程不能直接用同一个普通变量交换文档 |
| 线程 | 同一进程内的执行路径，由操作系统调度，通常共享进程内存 | 一个线程等待模型，其他线程仍可能获得执行机会 |
| 协程 | 保存可暂停函数的执行位置，由相应运行时调度 | 等待期间暂停这项工作，让执行线程处理其他就绪工作 |

多个进程需要交换数据时，可以用管道、套接字传消息，或显式使用共享内存。后者仍需协调同时读写。这类 **IPC（进程间通信）** 不等于持久消息队列：进程退出后，尚未保存的工作仍可能消失。

## 2. 异步等待什么时候能让出执行权

以 Python asyncio 为例， **事件循环** 负责运行已经就绪的任务，并等待 I/O 事件。协程遇到需要等待、且支持异步的操作时，可以暂停；事件循环便有机会运行其他任务。`await` 不是“每次都必定切换”，等待对象已经就绪时也可能直接继续。

```text
协程 A 发出请求 → 等待响应时暂停
                     ↓
同一事件循环线程执行已就绪的协程 B
                     ↓
A 的响应就绪 → A 获得调度后继续
```

若 A 直接调用阻塞的同步 SDK，执行这个调用的线程会被占住。函数名里有 `async`，也不能让事件循环自动绕过它。可选择真正的异步接口，或把合适的阻塞工作交给其他执行线程；后一种方式仍会消耗线程与下游资源。

CPU 密集任务要另看并行能力。常规启用 GIL 的 CPython 限制多个线程同时执行纯 Python 字节码；原生扩展可能释放 GIL，自由线程构建又有不同条件。不能把“Python 线程永远没用”或“多开线程一定加速计算”当通用答案。[线程与 GIL](https://docs.python.org/3.13/library/threading.html#gil-and-performance-considerations)

<details>
<summary>需要区分系统调用时再看：用户态、内核态与线程切换</summary>

普通程序主要在用户态执行；访问文件、套接字等操作通过系统调用请求内核服务。进入内核态是执行权限变化，切换到另一个线程则是执行者变化。系统调用可能很快返回，也可能等待，不能把“进入内核”直接等同于“线程必定切走”。异步 I/O 的具体实现也需要操作系统与运行时配合。[Linux 系统调用接口](https://man7.org/linux/man-pages/man2/syscalls.2.html)

</details>

## 3. 线程池复用执行者，不承诺等待队列有界

**线程池** 保存一组可复用线程。提交的函数由空闲线程执行；没有空闲线程时，库可能将工作排队。不同库的扩容、排队和拒绝规则不同，不能把 Java 的全部池参数照搬到 Python。

教学设置：2 个工作线程，同时最多接纳 5 项尚未终结的工作。

| 状态 | 执行中 | 等待中 | 能否再接纳一项 |
|---|---:|---:|---|
| 最初两项已经开始 | 2 | 0 | 可以，总数为 2 |
| 又接收三项 | 2 | 3 | 不可以，总数已为 5 |
| 一项结束，下一项已经开始，尚无新提交 | 2 | 2 | 可以，总数降为 4 |

线程数限制 **同时执行的工作** ，接纳容量限制 **执行中加等待中的工作** 。只限制前者，队列仍可能无限增长。

**信号量（semaphore）** 维护可领取的名额，领取成功才进入受限范围，离开时归还。但如果先创建十万个任务，再让它们等待信号量，这十万个等待对象已经占了内存。因此入口必须在大量创建或提交之前作接纳判断。

## 4. 超时不等于线程已经停下

提交函数时，调用方拿到的不是函数结果，而是 **Future（未来结果对象）** 。它保存这项工作的状态，以及完成后的返回值或异常。这里指 `concurrent.futures.Future`，不要与 asyncio 的同名对象混用。

| 调用或状态 | 调用方可以知道什么 |
|---|---|
| `submit(fn, ...)` 返回 Future | 已提交一项工作，不表示工作成功 |
| `future.result()` | 等待结束后取得返回值；任务抛异常时，在这里重新抛出 |
| `future.done()` 为 True | 工作已返回、抛异常或被成功取消，不只表示成功 |
| `future.result(timeout=...)` 抛出等待超时 | 此次等待没及时得到结果，不表示工作已经停止 |
| `future.cancel()` | 尝试取消尚未开始的工作；已在运行时不能靠它强制停止 |

下面是可直接运行的 Python 3.13 示例。故意提交一次除零计算，观察异常从哪里被看见：

<!-- runnable-example: future_exception -->
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=1) as pool:
    future = pool.submit(lambda: 1 / 0)
    try:
        future.result()              # 在获取结果处重新抛出任务异常
    except ZeroDivisionError:
        print("观察到任务失败")       # 观察到任务失败
```
<!-- /runnable-example -->

线程里的异常不会仅因提交成功，就自动变成业务方已经处理的失败。提交者或指定的调度层必须收集结果、记录失败；不能丢掉 Future 后假定有人处理。完成回调也能承担收尾，但回调被调用不等于任务成功。[Future 的结果、异常与取消](https://docs.python.org/3.13/library/concurrent.futures.html#future-objects)

再回到容量。假设 5 项工作都未终结，其中一个调用方超时返回，但线程仍在等待远端：接纳数仍是 5。若此时提前归还名额，第六项就会进入，使实际在途数超过约定。名额应在 **本地受控工作真正终结** 后归还。

<details>
<summary>实现对照：名额怎样绑定到 Future 的终结</summary>

下面是关键实现片段，不是独立脚本；完整导入与异常定义需由所在程序提供。

<!-- snippet: bounded_executor -->
```python
class BoundedExecutor:
    """workers 限制执行线程；capacity 限制已接收但尚未终结的任务总数。"""

    def __init__(self, workers: int, capacity: int) -> None:
        if workers < 1 or capacity < workers:
            raise ValueError("需要 capacity >= workers >= 1")
        self._pool = ThreadPoolExecutor(max_workers=workers)
        self._slots = BoundedSemaphore(capacity)
        self._lock = Lock()
        self._closed = False

    def submit(self, fn: Callable[..., T], *args: object) -> Future[T]:
        with self._lock:
            if self._closed:
                raise RuntimeError("executor 已关闭")
            if not self._slots.acquire(blocking=False):
                raise Overloaded("执行中与等待中的任务总数已到上限")
            try:
                future = self._pool.submit(fn, *args)
            except BaseException:
                self._slots.release()
                raise
            future.add_done_callback(lambda _future: self._slots.release())
            return future

    def close(self) -> None:
        with self._lock:
            self._closed = True
        self._pool.shutdown(wait=True, cancel_futures=True)
```
<!-- /snippet -->

`add_done_callback` 注册终结回调：返回、抛异常、待运行任务取消成功，都使本地工作终结。提交本身失败时单独归还，防止名额泄漏。关闭时取消尚未开始的工作，等待已运行工作结束；这不是有限时间强杀方案。

</details>

这里选择“容量满立即拒绝”是教学策略，也可采用有截止时间的入口等待，但不能退回无限队列。

> ⚠️ 本地函数已经抛错，不一定证明远端动作也停止。上述名额约束的是本地执行器；要承诺远端实际并发，还需取消确认或远端状态协议。调用方退出等待更不能替代这些确认。

## 5. 同时修改共享数据，要保护完整动作

两个线程都读取计数 10，各自加一再写回 11，最终只增加一次。问题不在于单次读写是否合法，而在于“读、判断、改”被交错执行。需要用 **互斥锁** 保护这组动作，或让存储直接执行原子条件修改。

锁住的是相同数据上的必要操作，不应把无关请求也串行化。锁的边界越长，其他工作等得越久；持锁访问一个可能阻塞的外部服务，会把短暂保护变成不可控等待。

读取很多、修改很少时，可以考虑 **读写锁** ：多个只读者可以共同访问，写者需要排他。它不保证总比互斥锁快。读取者不能偷偷修改数据；先读后尝试改写时，要在相应保护下重新核对条件。持续读流量会不会让写者一直等，还取决于具体公平策略。

<a id="5-资源交叉等待还可能形成死锁"></a>

## 6. 资源交叉等待，还可能形成死锁

线程池只有一个线程。任务 A 占着它，提交任务 B 后同步等待 B 的结果：

```text
A 持有唯一线程 → 等 B 完成
B 等待空闲线程 → 线程正被 A 占用
```

增大超时不能消除等待环。可以直接在 A 内完成适合串行的步骤，或让调度层在 A 返回后安排 B，而不是让池内工作阻塞等待同一个耗尽的池。

数据库连接等资源也一样：持有连接等待模型，可能让其他请求始终拿不到连接。应缩短持有范围，把必须共同成立的修改留在短边界内。

多个并发分支失败时，调度者还要决定其余分支是否取消、等待清理或返回部分结果。取消请求需要各操作配合；谁关闭资源、谁核对已发生的副作用，都必须有人负责。[asyncio 任务取消](https://docs.python.org/3.13/library/asyncio-task.html#task-cancellation)

## 本章小结

并发让多项工作共同推进，并行使用多个执行单元。线程池复用执行者，接纳上限控制未终结工作，Future 让调用方观察结果与异常。停止等待不等于停止工作；共享修改与资源等待还需要正确的锁和释放边界。

## 🎯 面试怎么答

**线程池大小和拒绝策略应该怎样设计？**

> 先看计算与等待比例、下游容量和资源持有时间，分别限制执行线程与总在途数。容量满时拒绝或有界等待；提交后收集 Future 的结果与异常。调用方超时不必然停止工作，名额应绑定本地工作终结，远端是否停止还要另行确认。池内避免阻塞等待同一个耗尽池的新任务。

## ⚠️ 易错点

> ⚠️ async 函数中的阻塞调用仍可能占住事件循环线程。

> ⚠️ 限制运行区而无限创建等待任务，不是有界接纳。

> ⚠️ Future 已终结不等于成功；发出取消也不等于取消成功。

## 本章自测

### 1. 2 个线程、总接纳上限 5，已有 2 项运行和 3 项等待。一个运行任务的调用方超时，但线程仍阻塞。第六项能否进入？

<details>
<summary>提示</summary>

数未终结的工作，而不是还在等待响应的客户端。

</details>

<details>
<summary>参考答案与解释</summary>

不能，5 项仍未终结。任务返回、抛异常或待运行任务被成功取消后，才能归还相应本地名额；远端动作另按实际协议核对。

</details>

### 2. 单线程池中 A 提交 B 并同步等待 B。写出等待关系，再给出不依赖“加一个线程”的改法。

<details>
<summary>提示</summary>

谁占着 B 需要的执行者？

</details>

<details>
<summary>参考答案与解释</summary>

A 等 B，B 等 A 持有的唯一线程。可以串行完成适合直接调用的步骤，或由调度层在 A 返回后提交 B，避免池内等待环。

</details>

### 3. submit 已返回，任务随后抛出 ValueError，future.done() 为 True。谁应观察失败？

<details>
<summary>参考答案与解释</summary>

提交者或指定调度者调用 result() 时会得到该异常，也可用明确设计的结果收集机制处理。done() 只表明终结，不能据此登记成功。

</details>

## 知识回看与权威资料

- [连接池与容量](05-ConnectionPool与ResourceCapacity.md)：区分工作线程与实际借用的连接资源。
- [Python Future API](https://docs.python.org/3.13/library/concurrent.futures.html#future-objects)：核对结果、异常、取消和完成回调的精确行为。
