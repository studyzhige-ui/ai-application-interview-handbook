# 07｜Tool Side Effect、Concurrency、Cancellation 与 Progress

> 本章合并旧 `12-ToolSideEffectConcurrency` 与 `13-ToolCancellationProgress`。它们本来属于同一个执行控制问题：**Tool 在真实世界里会占资源、产生副作用、彼此冲突，还可能需要中途取消。**

## 1. 为什么 Tool 不能默认并发

模型一次可能给出多个 Tool Call：

```text
read_file(A)
read_file(B)
run_tests()
```

看起来可以并发。

但如果是：

```text
edit_file(A)
run_tests()
```

并发可能产生：

```text
测试读取旧文件
测试读取写到一半的文件
结果对应未知版本
```

所以并发不是“async gather 全开”。

## 2. Tool Side Effect 分类

至少可以分：

### Pure / Read-only

```text
search
read_file
query snapshot
```

### Local Mutable

```text
edit workspace
write temp file
modify local cache
```

### External Reversible

```text
create draft issue
upload temporary artifact
```

### External Irreversible / High Risk

```text
send email
publish
charge
production delete
```

不同等级决定：

- 是否可并发；
- 是否需 Approval；
- 是否能 Retry；
- 是否需要 Compensation / Ledger。

## 3. Concurrency Safety 应是 Tool Contract 的一部分

不要让 Scheduler 猜。

可以有：

```python
class ToolRuntime:
    def is_read_only(self, args) -> bool: ...
    def is_concurrency_safe(self, args) -> bool: ...
    def resource_keys(self, args) -> list[str]: ...
```

例如：

```text
read_file(a.py) + read_file(b.py)
→ parallel okay

edit_file(a.py) + edit_file(a.py)
→ conflict

edit_file(a.py) + run_tests(repo)
→ ordering required
```

## 4. Resource Key 比“Tool Name”更准确

两个不同 Tool 也可能操作同一资源：

```text
apply_patch(path=a.py)
format_file(path=a.py)
```

因此冲突判断可以基于：

```text
workspace:file:a.py
repo:working-tree
customer:123
order:789
```

建立资源锁 / 调度约束。

## 5. 用户取消为什么必须传播

用户点击 Stop 时，不能只停止下一次模型调用。

取消应该沿执行树传播：

```text
Run Cancel
   ↓
Turn / Step Cancel
   ↓
Tool Invocation Cancel
   ↓
Subprocess / Network / Subagent Cancel
   ↓
Resource Cleanup
```

否则会出现：

```text
UI 显示 cancelled
但后台 shell 还在跑
```

## 6. Cancellation 是协议，不是一个布尔值

需要定义：

```text
谁发起？
什么时候可中断？
子任务是否继承？
正在执行副作用怎么办？
怎样清理？
结果还能否回填？
取消是否可 Resume？
```

某些 Tool 可以即时取消：

```text
search
read
```

某些操作进入 Commit Phase 后不能安全撤销：

```text
publish_release
```

这时 Runtime 更应该：

```text
mark cancel requested
→ wait for commit outcome
→ reconcile state
```

而不是假装强制取消成功。

## 7. Parent / Child Cancellation

长任务里常有：

```text
Run
└─ Subagent
   └─ Tool
      └─ subprocess
```

理想行为：

```text
Parent Abort
→ Child Abort
```

但：

```text
Child Abort
≠ 自动取消 Parent
```

否则一个局部 Tool 失败可能杀死整个 Run。

## 8. Progress 为什么是 Runtime Primitive

长 Tool 如果 5 分钟没有任何 Event，用户无法区分：

```text
正在工作
卡住
网络断了
worker 死了
```

所以长 Tool 可以输出：

```json
{
  "type": "tool_progress",
  "call_id": "c_17",
  "phase": "running_tests",
  "percent": 60,
  "message": "312/520 tests completed"
}
```

Progress 不一定全部进入 Model Context。

可以同时投影到：

```text
UI
Trace
Metrics
Model（必要时）
```

## 9. Streaming Result 与 Final Result 要分开

例如 Shell：

```text
stdout chunks
stderr chunks
exit code
final summary
```

不要把所有 streaming chunk 都永久写入 Model History。

更合理：

```text
live stream → UI / artifact
final compact result → model
full output → external artifact
```

这会在 Context Offloading 章节继续使用。

## 10. 源码证据：Claude Code

固定快照的 `Tool.ts` 有：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior(): cancel | block`；
- progress callback。

`utils/abortController.ts` 还实现 Parent → Child AbortController 传播，并处理 listener 清理。

这些实现直接说明：

> Concurrency / Cancellation 属于 Tool Runtime Contract，而不是 UI 细节。

## 11. 源码证据：Codex

固定快照的 `ToolRouter` / Invocation 会携带 `CancellationToken`，Registry 还能查询 Tool 是否支持 parallel calls。

这支持同样的稳定抽象：

```text
Tool Scheduler
需要知道 parallel capability + cancellation token
```

## 12. Side Effect + Cancellation 的危险窗口

最经典情况：

```text
Tool 开始写外部系统
→ 用户 Cancel
→ 外部系统提交成功
→ Runtime 没拿到结果
```

此时不能记录：

```text
cancelled = no effect
```

需要保存：

```text
operation_id
unknown outcome
reconciliation required
```

这会在 Checkpoint / Idempotency 章节进一步展开。

## 13. HUMAN-A 对应

- `AGENT-026` Timeout / Cancel / Interrupt / Resume：10 来源；
- `AGENT-029` 外部副作用 + Resume 重复执行：6 来源；
- `AGENT-031` 多 Agent 共享 Workspace 并发：7 来源。

真人面试通常不是单问 `asyncio.cancel()`，而是继续追：

```text
取消怎样传播？
Tool 正在写怎么办？
Worker 死了怎么办？
Resume 会不会重复写？
```

## 14. 🎯 30 秒回答

> Tool Runtime 要显式管理副作用、并发和取消。并发不能只看 Tool Name，而应看 read/write semantics 和资源冲突；用户取消要从 Run 向 Tool、Subprocess、Subagent 传播，但副作用进入提交阶段后可能无法真正撤销，需要记录 unknown outcome 并做 reconcile。长 Tool 还应该产生结构化 progress，UI/Trace 和 Model Context 可以使用不同 projection。

## 15. ⚠️ 易错点

- 所有只读 Tool 都绝对安全并发——仍可能依赖 shared mutable environment；
- `cancelled` = 没发生副作用——错；
- progress chunk 全塞 Chat History——会污染 Context；
- 子 Tool cancel 自动 kill 整个 Run——不一定；
- `async gather` = Agent concurrency strategy——远远不够。

<details><summary>自测：为什么 Resource Key 比 Tool Name 更适合并发冲突检测？</summary>

因为不同 Tool 可能修改同一个文件、Workspace 或业务对象；冲突来自共享资源，而不是来自函数名字是否相同。
</details>