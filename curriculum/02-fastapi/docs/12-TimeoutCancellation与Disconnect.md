# 12｜超时、断开与取消：请求结束之后发生什么

[← 上一章](11-BackgroundTask与Upload.md) · [模块主页](../README.md) · [下一章 →](13-Testing.md)

接口等了三秒没有结果，返回超时。用户重新提交后却发现同一动作做了两次。原因可能并不在重试代码里，而是我们把“我不再等待”误解成“对方一定没做”。

本章先把超时、取消与连接断开分开，再用本地实验观察协程怎样清理。示例使用 Python 3.11+ 的 `asyncio.timeout`。

## 1. 先分清超时、取消与断开

| 情况 | 能确定什么 | 不能直接推出什么 |
|---|---|---|
| 超时 | 等待超过了设定预算 | 下游一定未执行 |
| 取消 | 已要求某个任务停止 | 任意同步函数或远端动作立刻停止 |
| 断开 | 当前传输连接已中断 | 业务任务也应该被取消 |

超时可以发生在一次下游读取，也可以发生在整个路由的总预算上。取消可以来自用户操作、超时处理或服务退出。它们之间怎样触发，需要代码明确安排。

## 2. 一个可观察的超时与清理实验

```python
# example: timeout_app
import asyncio
from fastapi import FastAPI, HTTPException

app = FastAPI()
app.state.events = []

async def slow_operation():
    app.state.events.append("started")
    try:
        await asyncio.sleep(1)
        return "完成"
    finally:
        app.state.events.append("cleaned")

@app.get("/slow")
async def slow():
    try:
        async with asyncio.timeout(0.02):
            result = await slow_operation()
        return {"result": result}
    except TimeoutError:
        raise HTTPException(504, "本次等待超时") from None
```

请求 `/slow` 应得到 504，记录中出现 `started` 和 `cleaned`。这说明在这个本地、可协作取消的等待中，超时触发了取消，协程执行了 finally。

它**没有**证明另一个服务器中的工作已经停止。若 slow_operation 已把创建工单请求发送出去，工单仍可能在远端成功创建。

## 3. CancelledError 为什么通常要继续抛出

取消是控制流程的一部分。代码可以在被取消时记录必要信息和清理资源，但通常应让取消继续传播，而不是伪装成正常结果。

```python
# example: cancellation_demo
import asyncio

async def main():
    entered = asyncio.Event()
    events = []

    async def work():
        try:
            entered.set()
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            events.append("cancelled")
            raise
        finally:
            events.append("cleaned")

    task = asyncio.create_task(work())
    await entered.wait()  # 确认已进入工作，再发取消，避免靠猜测等待时间
    task.cancel()
    try:
        await task       # 等待其处理取消并结束，不是发出cancel就不管了
    except asyncio.CancelledError:
        events.append("observed")
    return events

if __name__ == "__main__":
    print(asyncio.run(main()))  # ['cancelled', 'cleaned', 'observed']
```

从 Python 3.8 起，`asyncio.CancelledError` 继承 `BaseException`，**普通 `except Exception` 不会捕获它**。真正会把它截住的是显式捕获 CancelledError、捕获 BaseException 或裸 except 等写法。这一点以 [Python 官方异常文档](https://docs.python.org/3/library/asyncio-exceptions.html)为准。

> ⚠️ finally 不是断电保障。进程被直接杀死、机器掉电，或者异步清理又被取消时，清理可能不能完成。需要持久恢复的业务不能只依赖内存里的 finally。

## 4. 同时启动的其他任务，谁负责收尾

`gather` 的结果顺序与输入一致，但默认一个子任务报错时，不保证其他所有子任务立即被取消。调用者需要知道是否允许剩余工作继续。

例如同时查资料和读取配置：资料查询失败后，若已经无法回答，应停止不再需要的配置查询，并等待清理结束；若配置仍有独立用途，则要明确由谁继续管理。

`TaskGroup` 可以管理需要一起结束的子任务。这里先掌握“谁启动、谁决定失败后的去留、谁等待收尾”；处理异常组的具体语法属于 Python 并发用法。

<details>
<summary>按需实验：TaskGroup 与 except* 怎样落实共同收尾</summary>

```python
# example: taskgroup_demo
import asyncio

async def main():
    entered = asyncio.Event()
    events = []

    async def slow():
        try:
            entered.set()
            await asyncio.sleep(60)
        finally:
            events.append("slow cleaned")

    async def fail():
        await entered.wait()
        raise ValueError("模拟下游失败")

    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(slow())
            group.create_task(fail())
    except* ValueError:
        events.append("failure observed")
    return events

if __name__ == "__main__":
    print(asyncio.run(main()))  # ['slow cleaned', 'failure observed']
```

`except*` 用于处理异常组中的匹配异常，这里处理任务组收集的 ValueError。它不是把所有失败默认为可忽略。任务组负责本地子任务的生命周期，也不能撤销已经提交给外部系统的动作。

</details>

## 5. 浏览器断开，不要猜业务策略

临时生成可以随连接中断而停止；已被接受的长任务可以继续，把连接视为一个可重新建立的观察窗口。应先选择业务语义，再连接到框架断开信号。

Starlette 的 `request.is_disconnected()` 可用于检查断开状态，但不要做无等待的忙轮询，也不要让多个消费者争抢原始请求接收流。复杂流式实现的断开通知、发送失败与取消路径应按实际框架版本验证。

```text
传输断开
  ├─ 临时工作：请求停止生成 → 清理本次资源
  └─ 持久任务：解除订阅 → 任务按自身状态继续
```

## 6. 对哪些东西可以取消，必须有现实预期

协程在可取消的等待点有机会响应。在线程中已经执行的同步函数，通常不能通过取消等待它的协程就安全强杀。远端调用则取决于供应商是否有取消协议以及动作是否已经提交。

当有副作用且结果未知时，后续应使用稳定操作标识查询状态、核对结果或走补偿流程。不要因为没有响应，就立刻用新标识再执行一次。

## 7. 清理只清理自己拥有的资源

单次请求结束可能释放文件、临时订阅、借出的会话和本次创建的子任务；不应顺便关闭所有请求共用的 HTTP 客户端或连接池。

需要异步等待的清理也可能再次被取消。确有必要保护清理时，可以设置有限的屏蔽范围和超时；不要把全部业务都设为不可取消。具体写法取决于 asyncio 或 AnyIO 的取消模型，见[取消与清理说明](https://anyio.readthedocs.io/en/stable/cancellation.html)。

## 8. 失败实验怎样写才有用

分别测试：等待超时、主动取消、流发到一半失败、客户端关闭连接、服务停止。每个实验应观察其具体边界，而不是只断言“请求没有成功”。

上面两个 asyncio 实验只验证本地任务，不能代替真实流式断开测试。代理超时、供应商取消和外部动作查询需要对应集成环境。

**取消反例推导：** cancellation_demo 若捕获 CancelledError 后去掉 raise，work 会经 finally 正常返回 None；调用方的 await 不再进入取消异常分支，events 中也没有 observed。调用方可能把停止误当正常完成，这就是保留取消传播的意义。

---

## 本章小结

超时表示等待预算，取消是本地控制请求，断开是传输事件。清理需要明确所有权，结果未知的外部动作需要核对，不能把任何一个信号当成“世界已经停止”。

## 🎯 面试怎么回答

**except Exception 会吞掉现代 asyncio 的取消异常吗？**

> 不会。CancelledError 自 Python3.8 起继承 BaseException。仍应避免显式捕获后不再抛出，或用过宽的 BaseException 捕获把取消转成成功。

**超时后为什么不能直接重试有副作用操作？**

> 远端可能已执行但响应丢失，需要稳定操作标识与状态查询、幂等或核对流程；不能将等待超时当成未执行证明。

## ⚠️ 易错点

> ⚠️ task.cancel()是发出请求，仍需等待和观察任务结束。

> ⚠️ 本地 finally 执行通过，不代表远端动作已撤销或进程崩溃能自动恢复。


## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. 调用 task.cancel() 后，为什么还要 await 这个任务？</summary>

cancel 只是发出取消请求。等待任务结束，才能观察取消结果，并让它完成相应清理；不能发出请求后就假定工作已经停止。

</details>

<details>
<summary>2. 为什么超时实验中 cleaned 出现仍不能证明付款未发生？</summary>

cleaned 只记录本地资源清理，远端付款有自己的提交与返回过程。

</details>

<details>
<summary>3. 用户关闭页面后，为什么不一定把 run 状态改成 CANCELLED？</summary>

断开不等于业务取消，持久任务可能继续；只有明确请求并确认停止语义后才能按契约更新状态。

</details>

## 知识回看与权威资料

- [asyncio 异常层级](https://docs.python.org/3/library/asyncio-exceptions.html)：核对 CancelledError 的继承与传播。
- [任务、超时与任务组](https://docs.python.org/3/library/asyncio-task.html)：核对 cancel、gather、TaskGroup、timeout。
- [请求断开](https://starlette.dev/requests/)：核对 is_disconnected。
- [AnyIO 取消](https://anyio.readthedocs.io/en/stable/cancellation.html)：理解有限清理与取消作用域。
