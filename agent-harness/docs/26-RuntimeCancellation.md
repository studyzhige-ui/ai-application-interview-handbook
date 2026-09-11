# 26｜Runtime Cancellation

## 1. Cancellation 和 Failure 不同

Failure：系统想继续但动作失败。

Cancellation：用户或 Runtime 明确要求停止继续执行。

```text
RUNNING → CANCELLING → CANCELLED
```

最好不要直接 RUNNING → 消失。

## 2. 传播树

```text
Root Run
├─ active model request
├─ tool A
│  └─ child process
└─ subagent B
   └─ tool C
```

Cancel root 时，Runtime 要知道哪些 child 能取消、哪些只能 detach、哪些必须 cleanup。

## 3. Cancellation-safe State

取消过程中仍要：

- 写 terminal event；
- 保存已经发生的 side effects；
- 回收 lease / process；
- 不把半写状态标成 completed。

## 4. Late Result

请求已取消，但远程 Tool 后来返回成功：

```text
late completion event
→ reconcile state
```

不能直接丢掉，否则 Runtime truth 和外部世界分叉。

## 5. Cancellation 与 Resume

PAUSED 通常允许 resume；CANCELLED 是否允许 reopen 要单独定义，不能混用。

## 🎯 面试

Cancellation 是一条贯穿 Run→subagent→tool→child process 的控制信号。系统要有 CANCELLING 过渡态、cleanup 和 late-result reconciliation，并把已发生副作用持久化；不能把 cancel 当普通 exception。

<details><summary>自测：用户取消后为什么仍可能要继续处理事件？</summary>

因为外部调用可能已经无法撤回，后续 completion 仍决定真实世界状态，需要 reconcile 和审计。
</details>
