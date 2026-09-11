# 13｜Tool Cancellation、Progress 与 Streaming

## 1. 用户说“停”时发生什么

复杂 Tool 可能正在：

- 跑 shell；
- 下载文件；
- 远程 API job；
- 启动 subagent。

Cancellation 必须从 Run 向下传播：

```text
Run cancel signal
→ current turn
→ active tool/task
→ child process / remote request
```

Claude Code Tool contract 甚至显式区分新消息到来时 Tool 是 `cancel` 还是 `block`。

## 2. Cancellation 是协议

正确设计不是只有 `future.cancel()`：

```text
request cancellation
→ tool acknowledges
→ cleanup
→ terminal event
```

远程 Tool 可能根本不能真正取消，此时 Runtime 要明确“已停止等待，但远端可能继续”。

## 3. Progress 为什么是一等事件

长 Tool 如果 3 分钟无事件：

- 用户以为卡死；
- Runtime 不知道是否健康；
- watchdog 难判断。

Progress 应包含可机器读的阶段：

```text
queued
cloning
running_tests
uploading
```

而不是刷随机日志。

## 4. Streaming 和 Final Result

Streaming event 可以增量展示，但最终仍要产生 terminal result，作为下一轮 Observation 和持久化事实。

## 🎯 面试

Cancellation 要做成从 Run 到 Tool/child task 的传播协议；Progress 是独立 Runtime event；Streaming 只是交付方式，不能替代最终 terminal result。无法真正取消的远程副作用还要在状态里显式标记不确定性。

<details><summary>自测：取消 HTTP 请求后，服务端动作一定没发生吗？</summary>

不一定。客户端断开只代表不再等待响应。对外部副作用仍需要幂等键、查询状态或补偿机制。
</details>
