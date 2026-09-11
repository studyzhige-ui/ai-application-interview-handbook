# 12｜Timeout、Cancellation、Client Disconnect 与 Cleanup

AI Service 的一个典型错误心智模型是：

> “客户端关掉页面，后端自然就停了。”

实际系统没有这么简单。

你需要区分：

```text
Client Disconnect
Request Timeout
Coroutine Cancellation
Downstream Timeout
Business Cancel
Durable Task Cancel
```

它们不是一回事。

---

## 1. Timeout 是“等待边界”，不是“世界停止”

假设：

```text
FastAPI
→ LLM Provider
→ Tool
→ Payment API
```

如果你的调用方 10 秒超时：

```text
caller stops waiting
```

不代表：

```text
provider definitely stopped
side effect definitely did not happen
```

这就是为什么 Timeout 必须和 Cancellation / Idempotency 一起理解。

---

## 2. Client Disconnect 是 Transport 事件

例如用户关闭浏览器：

```text
Browser connection gone
```

FastAPI/Starlette 层可以感知连接断开，但接下来应该做什么取决于业务：

### 短 LLM 生成

```text
cancel generation
→ release connection
```

### Durable Agent Run

```text
UI disconnected
→ run continues
→ user reconnects by run_id
```

因此：

> Transport Disconnect ≠ Business Cancellation。

---

## 3. Streaming Generator 的取消

一个良好的 Stream Generator 要有 Cleanup：

```python
import asyncio

async def event_stream():
    try:
        async for event in runtime.events():
            yield event
    except asyncio.CancelledError:
        await runtime.cancel_if_ephemeral()
        raise
    finally:
        await runtime.detach_stream()
```

重点是：

- 不吞 `CancelledError`；
- finally 释放资源；
- 是否取消业务 Run 由策略决定。

---

## 4. 不要把 CancelledError 当普通业务异常吞掉

坏模式：

```python
try:
    ...
except Exception:
    return {"error": "failed"}
```

这可能破坏取消传播。

更好的原则：

> 取消是控制流信号，不应被无脑转换成普通业务失败。

具体异常层级和 asyncio 版本行为要按当前 Python Runtime 核实。

---

## 5. `request.is_disconnected()` 的用途

Starlette Request 提供检测客户端是否断开的能力。

在长时间 Poll/Stream 中可以周期性检查。

但不要形成忙轮询：

```text
while True:
    is_disconnected()
```

应该结合你的异步事件循环和实际工作节奏。

---

## 6. Timeout 应该分层

常见：

```text
Connect Timeout
Read Timeout
Provider Request Timeout
Route / Request Deadline
Gateway Timeout
```

不要把所有层都设成 30 秒。

更合理：

```text
End-to-end Deadline
→ 给子调用分预算
```

完整 Timeout Budget 在 AI Backend Engineering 深讲。

---

## 7. Downstream Cancellation 不一定存在

有些 Provider API 支持显式 cancel；有些没有。

即使本地 Coroutine cancel：

```text
local coroutine stopped
```

远端服务器可能已经收到请求并继续运行。

因此必须知道下游协议的真实语义。

---

## 8. 副作用 Tool 最危险

例子：

```text
调用支付 Tool
→ 8 秒没收到响应
→ FastAPI timeout
→ 客户端重试
```

但第一次请求可能已经成功扣款。

这不是 FastAPI 框架问题，而是：

```text
Timeout + Side Effect + Idempotency
```

API 层至少要携带稳定 Idempotency Key / Operation ID，真正语义在 Backend/Agent Runtime 实现。

---

## 9. Cleanup 要考虑哪些资源

Request 取消时常见需要清理：

- DB Session / Transaction；
- HTTP Stream；
- File Handle；
- Subscription；
- per-request Task；
- temporary buffer。

但 Application-scoped Client/Pool 不应该因为单个请求取消就整体关闭。

---

## 10. Shield 要谨慎

有时某段清理动作需要在取消时尽量完成，比如：

```text
写最终状态
释放 Lease
flush audit event
```

可以考虑 shield 类机制，但不能滥用。

如果所有任务都 shield：

```text
cancel loses meaning
shutdown hangs
```

---

## 11. Graceful Shutdown 也是 Cancellation 问题

服务关闭时：

```text
stop accepting new requests
→ wait / cancel inflight
→ stop stream
→ flush state
→ close pool
```

这和第 15 章 Deployment 会重新组合。

---

## 12. Failure Timeline

### Case：用户关闭 Agent Chat 页面

```text
Client disconnect
→ SSE generator cancelled
→ FastAPI stream closes
→ Agent run is durable
→ Runtime keeps executing
→ user returns later
→ GET run state / resume stream
```

另一种业务也可能：

```text
Client disconnect
→ generation cancel
→ provider request cancel
→ run marked CANCELLED
```

关键是**预先定义语义**。

---

## 13. 🎯 面试怎么回答

> 我会把客户端断开、Request Timeout 和业务取消分开。FastAPI Streaming Endpoint 被取消时要让 Coroutine 正确传播 CancelledError 并在 finally 清理 request-scoped resource；但是否取消 Agent Run 要看 Run 是否 durable。Timeout 只说明本地不再等结果，不代表远端副作用停止，所以有写操作时还必须结合 Idempotency / Operation ID。

---

## 14. 易错点

- ❌ Client disconnect = 下游任务一定停止。
- ❌ Timeout = 请求没有执行成功。
- ❌ catch Exception 后返回 error 就能处理 Cancellation。
- ❌ `finally` 可以省略。
- ❌ Durable Agent Run 必须绑定浏览器连接生命周期。

---

## 15. 本章自测

<details>
<summary>1. Timeout 与 Cancellation 的区别是什么？</summary>

Timeout 是超过等待预算；Cancellation 是显式请求停止某个执行单元。Timeout 可能触发 cancellation，但远端是否真的停止取决于协议实现。

</details>

<details>
<summary>2. 为什么支付类 Tool 的 Timeout 特别危险？</summary>

因为超时只代表没有收到结果，副作用可能已经发生；盲目重试会重复扣款，因此需要 Idempotency 和明确操作状态。

</details>

<details>
<summary>3. 为什么 Durable Agent 不应该和 SSE 连接生命周期强绑定？</summary>

用户断网或关闭页面不一定意味着要停止长任务；Run 可以持久化并在之后重新连接查看状态。

</details>
