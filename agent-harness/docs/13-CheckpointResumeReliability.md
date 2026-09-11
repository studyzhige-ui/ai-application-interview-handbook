# 13｜Checkpoint / Resume / Fork / Replay 与 Long-running Reliability

> 本章合并旧 `CheckpointResume`、`ForkBranchReplay`、`RuntimeCancellation`、`IdempotencyCompensation`。这些都属于同一个长任务问题：**任务跨时间、跨 Worker、跨故障继续运行时，怎样不丢状态，也不重复副作用。**

## 1. Checkpoint 保存什么

不是简单保存 Messages，而是保存可继续执行所需的 Runtime Snapshot：

```text
run / step position
goal / constraints
state version
pending tool / approval
artifact references
budget usage
capability / policy snapshot
side-effect ledger
```

## 2. Resume 的基本流程

```text
load checkpoint
→ validate schema / policy / workspace version
→ reconcile pending operations
→ rebuild current context
→ restore cancellation / approval boundary
→ continue from safe point
```

Resume 不是“把历史重新发给模型”。

## 3. 最危险的 Failure Window

```text
Tool external side effect succeeds
→ process crashes
→ checkpoint not written
→ resume from old checkpoint
→ tool executes again
```

这就是 `AGENT-029` 的经典问题。

## 4. Side-effect Ledger

高风险操作可以先创建稳定 operation id：

```text
operation_id = run_id + logical_step
```

执行前/后记录：

```text
PENDING
IN_FLIGHT
COMMITTED
FAILED
UNKNOWN
```

Resume 时先查 ledger / external system，再决定是否重试。

## 5. Idempotency 与 Compensation

### Idempotency

同一 operation 重复提交只产生一次效果。

### Compensation

无法真正回滚时，用反向动作补偿。

例如：

```text
create reservation
→ downstream failure
→ cancel reservation
```

两者不是一回事。

## 6. Fork / Branch

Fork 用于：

- 探索不同方案；
- 让 Subagent 从某个 Context Snapshot 开始；
- Eval 对比两个策略；
- Debug 复现。

必须定义继承边界：

```text
history snapshot?
state?
workspace?
permission?
provider config?
external side-effect ledger?
```

不能默认“复制所有东西”。

## 7. Replay

真正 Replay 需要区分：

```text
Deterministic Event Replay
vs
Re-run Model / Tool
```

重新调用模型不保证得到同样结果。

因此 Debug Replay 往往使用已记录的 model/tool evidence 重建执行轨迹，而不是重新请求所有外部依赖。

## 8. Cancellation 与 Resume

Cancel 后是否可 Resume 需要显式状态：

```text
CANCELLED_FINAL
PAUSED_USER
INTERRUPTED_RECOVERABLE
```

不要所有中断都写成同一个 `cancelled`。

## 9. 源码证据

Claude Code 固定快照的 Task 对象有 pending/running/completed/failed/killed 等状态和 abort/kill semantics。

Codex 固定快照明确讨论 warm resume、cold resume、fork 时 instruction snapshot / provider 的继承规则。这很好地说明：

> Resume / Fork 的关键是“继承什么、重新加载什么”，必须成为协议。

## 10. HUMAN-A

- `AGENT-026` Long-running Cancel/Resume：10 来源；
- `AGENT-027` Checkpoint / Resume：12 来源；
- `AGENT-029` External Side Effect：6 来源。

## 11. 🎯 面试回答

> Checkpoint 应保存可恢复的 Runtime State，而不只是聊天历史。Resume 时先验证版本并 reconcile 未知副作用，再从安全点继续。最危险的是外部 Tool 已成功但 checkpoint 没落盘，恢复后重复执行，因此高风险操作需要稳定 operation id、idempotency key 或 side-effect ledger；无法幂等时还要设计 compensation。Fork / Replay 也必须明确哪些 State、Permission 和 Workspace 被继承。

<details><summary>自测：为什么“Tool 返回成功后再写 Checkpoint”仍有重复执行窗口？</summary>

因为 Tool 成功和 Checkpoint Durable Commit 之间仍可能 Crash。恢复只能看到旧 Checkpoint，因此需要独立 operation ledger / idempotency 来识别外部副作用已经发生。
</details>