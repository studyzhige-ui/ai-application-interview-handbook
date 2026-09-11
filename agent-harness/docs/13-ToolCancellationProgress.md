# 13. Tool Cancellation / Progress：长任务必须能停、能看见、能清理

`AGENT-026`（Timeout / Cancel / Interrupt / Resume）在冻结 HUMAN-A 中有 **10 个独立来源**，`AGENT-042` Dynamic Instruction / Steering 也直接涉及运行中修改需求。

短 Tool：

```text
read_file → 20ms
```

很少暴露取消问题。

长 Tool：

```text
跑完整测试 15 分钟
扫描大型仓库
浏览器自动化
远程 Agent Task
生成大批数据
```

如果 Runtime 只有：

```python
await tool()
```

用户会遇到三个问题：

```text
停不下来
不知道做到哪
停了也不知道资源有没有清干净
```

---

# 1. 先讲人话：Cancellation 不是“抛一个异常”

用户点击 Stop：

```text
UI sends cancel
```

真正需要传播：

```text
Client
→ API / Session
→ Run
→ Current Step
→ Tool Executor
→ subprocess / network request / child agent
```

最后还要：

```text
cleanup
→ update state
→ emit events
→ decide resumability
```

所以：

> **Cancellation 是一条跨 Runtime 层级传播的控制信号。**

---

# 2. Cancel、Timeout、Interrupt 不完全一样

## Cancel

通常来自：

```text
user / parent task / operator
```

意思：

> “不要继续这个执行。”

## Timeout

来自 Runtime Policy：

```text
deadline exceeded
```

意思：

> “执行超过允许时间。”

## Interrupt / Steering

用户可能不是要结束整个 Run，而是：

```text
“别继续这个方向，改成先查日志。”
```

这可能要求：

```text
cancel current tool
→ preserve state
→ inject new instruction
→ next step re-plan
```

---

# 3. Tool 必须声明 Interrupt Behavior

不是所有 Tool 都适合立即取消。

例如：

```text
read_file
→ cancel 没什么问题
```

但：

```text
正在写 Git commit
正在数据库 transaction commit
正在发外部 API 请求
```

强行在任意时刻打断可能留下半完成状态。

因此 Tool Contract 可以声明：

```text
cancel
or
block
```

Claude Code 固定源码里的 `Tool.ts` 就有：

```text
interruptBehavior?(): 'cancel' | 'block'
```

并说明当用户在 Tool 运行中提交新消息时：

```text
cancel → 停 Tool 并丢弃结果
block  → Tool 继续，新消息等待
```

这是非常具体的成熟 Runtime 语义。

---

# 4. Cancellation Token

一个常见设计：

```python
class CancellationToken:
    @property
    def cancelled(self) -> bool: ...

    async def wait(self): ...
```

Tool 执行：

```python
async def scan_repo(ctx):
    for path in paths:
        if ctx.cancel_token.cancelled:
            raise CancelledError()

        await scan(path)
```

对于支持取消的底层 API，则把 Token 继续传下去。

---

# 5. Cancellation 应该从 Parent 向 Child 传播

假设：

```text
Parent Agent
└─ Subagent A
   └─ Shell Tool
```

用户取消 Parent：

```text
Parent Cancel
→ Subagent Cancel
→ Shell Process Cancel
```

否则会出现：

```text
UI 显示任务已取消
但后台 Shell 还在跑 20 分钟
```

这不仅浪费资源，还可能继续产生副作用。

---

# 6. Claude Code 的 AbortController 证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`utils/abortController.ts` 当前提供：

```text
createAbortController()
createChildAbortController(parent)
```

子 Controller：

```text
parent abort → child abort
child abort ↛ parent abort
```

而且源码专门处理 listener cleanup / WeakRef，避免 abandoned child 被 parent listener 长期保留。

这是一个非常实际的工程点：

> **Cancellation Tree 自己也会产生资源生命周期问题。**

---

# 7. Codex Router 的 CancellationToken 证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/core/src/tools/router.rs` 的 dispatch 接口直接接收：

```text
CancellationToken
```

再放入 `ToolInvocation` 传给具体 Tool Runtime。

这说明 cancellation 是 Tool Invocation Contract 的一部分，而不是 UI 层特例。

---

# 8. Tool Cancel 后状态怎么记

不能只：

```text
future.cancel()
```

还要有 Runtime Event：

```text
ToolCancelRequested
ToolCancellationStarted
ToolCancelled
```

或者如果失败：

```text
ToolCancelFailed
```

Run State 可能变为：

```text
cancelled
```

或：

```text
running + current step interrupted
```

取决于是整个 Run Cancel 还是 Steering。

---

# 9. Cooperative vs Forced Cancellation

## Cooperative

Tool 主动检查 Token：

```text
安全点退出
```

优点：

- 能清理；
- 能保存进度；
- 状态更一致。

缺点：

- Tool 必须配合。

## Forced

例如：

```text
kill process
terminate container
revoke worker
```

优点：

- 对失控任务有效。

缺点：

- 可能留下部分副作用。

成熟系统通常：

```text
先 cooperative
→ grace period
→ forced termination
```

---

# 10. Cancellation 与 Side Effect

最难情况：

```text
Tool 正在 send_email
↓
Cancel arrives
```

你不能保证：

```text
邮件没发出去
```

所以 Cancel 的结果可能是：

```text
execution cancelled
but side effect status = unknown/committed
```

Runtime 需要：

- reconcile；
- query external status；
- record ledger；
- avoid blind replay。

所以 Cancellation 与 Idempotency 是相连的。

---

# 11. Timeout 也应该通过同一个 Cancellation Path

坏设计：

```text
用户 cancel → 一套逻辑
Timeout → 直接抛异常
Shutdown → 再一套逻辑
```

更好的思想：

```text
Cancel Reason
= user_cancelled
| timeout
| parent_cancelled
| shutdown
| superseded_by_new_instruction
```

底层统一传播 cancellation，只在上层保留 Reason。

这样 Tool Cleanup 更一致。

---

# 12. Progress 的第一作用：让用户知道 Agent 没死

长任务如果 3 分钟没输出：

用户无法区分：

```text
还在运行
卡住
死循环
网络断了
```

所以 Tool 可以发：

```text
started
10%
scanned 500/5000 files
running test shard 3/10
completed
```

这是产品体验，也是 Runtime Observability。

---

# 13. Progress 不一定是百分比

很多 Agent Tool 无法知道总工作量。

可以报告：

```text
Phase
Current Item
Count
Heartbeat
Artifact
```

例如：

```json
{
  "phase": "testing",
  "completed_suites": 18,
  "last_activity_at": "..."
}
```

不要硬造：

```text
83%
```

如果根本不知道总量。

---

# 14. Progress Event 与 Model Context 分开

Tool 每秒发：

```text
progress 1
progress 2
...
```

UI 可以显示。

模型没必要全部看。

最终只需要：

```text
Tool completed: scanned 12,493 files, found 18 matches
```

因此：

```text
Progress Event Stream
≠ Model-visible Tool Result
```

这与第 6 章 Runtime Event Model 完全一致。

---

# 15. Claude Code Progress 证据

`Tool.ts` 的 Tool Call 支持：

```text
onProgress?: ToolCallProgress
```

`ToolUseContext` 还引用多种 Progress 类型：

```text
BashProgress
MCPProgress
AgentToolProgress
SkillToolProgress
TaskOutputProgress
WebSearchProgress
HookProgress
```

这说明不同 Tool 的 progress payload 可以不同，但 Runtime 可以统一用 Event 机制承载。

---

# 16. Background Task 为什么需要独立 Output Artifact

Claude Code `Task.ts` 中 Task State 有：

```text
outputFile
outputOffset
```

这是一种很实用的长任务设计：

```text
大输出持续写 artifact
↓
Runtime 只保存 offset / ref
↓
UI / Agent 按需读取
```

好处：

- 不把大输出塞内存；
- 支持增量读取；
- 支持后台任务；
- 支持 resume / poll。

---

# 17. Progress 还能用于 Stall Detection

如果 Tool 正常每 5 秒有 heartbeat：

```text
last_progress_at = now
```

突然 2 分钟无任何 progress：

Runtime 可以判断：

```text
stalled?
```

然后：

- warning；
- health probe；
- timeout；
- cancel。

这比只设置一个超长固定 Timeout 更精细。

---

# 18. Cancel 之后 Cleanup 做什么

不同 Tool 不同：

### subprocess

```text
SIGTERM
→ grace period
→ SIGKILL
→ wait/reap process
```

### file writer

```text
remove temp file
avoid partial replace
```

### browser

```text
close page/session
```

### remote worker

```text
send cancel
release lease
```

### DB transaction

```text
rollback if still active
```

所以 Tool Contract 最好明确 Cleanup Responsibility。

---

# 19. Cancelled Result 能不能进入模型？

取决于场景。

如果用户完全取消 Run：

```text
可能不需要下一轮 Model
```

如果只是 Steering：

```text
Tool cancelled because user changed instruction
```

可以作为 Observation：

```json
{
  "error_type": "cancelled",
  "reason": "superseded_by_user_instruction"
}
```

然后把新用户指令一起加入下一轮 Context。

---

# 20. 新指令到来：Cancel 还是 Block？

这就是 `interruptBehavior` 的价值。

例如：

```text
Tool = search_code
→ cancel

Tool = commit_transaction
→ block until safe boundary
```

Runtime 可以按 Tool Contract 决定：

```text
new user input
→ cancel current tool
or
queue message
```

而不是全局一个策略。

---

# 21. Cancellation 与 Checkpoint

如果 Tool 被取消后要 Resume：

Checkpoint 至少要知道：

```text
Tool 是否完成？
是否产生 partial artifact？
side effect 状态？
progress cursor？
```

不能只保存：

```text
step=12
```

否则恢复时不知道从哪开始。

---

# 22. 一个长文件扫描 Tool 示例

```python
async def scan_files(paths, ctx, on_progress):
    matches = []

    for i, path in enumerate(paths):
        if ctx.cancel_token.cancelled:
            raise ToolCancelled("user requested cancellation")

        matches.extend(await scan_one(path))

        if i % 100 == 0:
            await on_progress({
                "processed": i,
                "matches": len(matches),
            })

    return {
        "processed": len(paths),
        "matches": matches,
    }
```

Production 还要：

- output cap；
- artifact offload；
- checkpoint cursor；
- error handling。

---

# 23. 高频易错点

⚠️ **Cancel = future.cancel() 就结束**  
还要传播、cleanup、记录 state/event、副作用 reconciliation。

⚠️ **所有 Tool 都能立即取消**  
一些临界区必须 block 到安全点。

⚠️ **Progress 只给 UI 用**  
它也能做 watchdog、stall detection、trace。

⚠️ **Progress 全塞给模型**  
会污染 Context。

⚠️ **Timeout 与 Cancel 完全分开实现**  
底层可以统一为 cancellation propagation，保留不同 reason。

---

# 24. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> 长 Tool 要把 cancellation 和 progress 当成 Runtime Contract。Cancel 应从 Run/Parent 向当前 Step、Tool、subprocess/child agent 传播，并在安全点 cleanup；不同 Tool 可以声明 cancel 或 block。Progress 走独立 Runtime Event Stream，给 UI、watchdog、trace 使用，不必全部进入模型 Context。Timeout 也可以统一走 cancellation path，但保留 timeout reason。

## Level 2｜2–3 分钟

> 我会用 cancellation token 建 parent-child tree，parent cancel 自动传播到 child，但 child cancel 不反向杀 parent。Tool 如果能 cooperative cancel，就先优雅退出，超 grace period 再 forced kill。Cancel 后要记录 side-effect status 和 partial artifact；外部写操作不能因为 cancel 就假设没发生。Progress 用 phase/count/heartbeat，不强求百分比，还能用于 stall detection。Steering 时根据 Tool 的 interrupt behavior 决定 cancel 当前 Tool 还是 block 新消息。

## Level 3｜继续追问

🔍 **为什么 child cancel 不应该默认 cancel parent？**  
子任务失败/取消可能只是局部状态，Parent 还能 fallback 或继续其它分支。

🔍 **Cancel 正在进行的支付 Tool 怎么办？**  
不能假设回滚；查询外部 operation status，结合 idempotency/ledger reconciliation。

🔍 **进程 kill 后为什么还要 wait/reap？**  
避免 zombie process 和资源泄露。

---

# 25. 本章证据

## HUMAN-A

- `AGENT-026` Cancellation / Long-running Task：10 sources；
- `AGENT-042` Dynamic Instruction / Steering：1 source；
- `AGENT-027` Checkpoint / Resume：12 sources。

## Claude Code

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

- `Tool.ts`：`interruptBehavior()`、progress callback、AbortController context；
- `utils/abortController.ts`：parent → child abort propagation；
- `Task.ts`：kill、outputFile、outputOffset、task status。

## OpenAI Codex

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

- `codex-rs/core/src/tools/router.rs`：`CancellationToken` 进入 ToolInvocation。

---

# 26. 自测

<details><summary>1. Cancel、Timeout、Steering 有什么区别？</summary>

Cancel 是终止执行的请求；Timeout 是 Runtime 因 deadline 触发的取消原因；Steering 是新指令改变方向，可能只取消当前 Tool 后继续同一 Run。
</details>

<details><summary>2. 为什么 Cancellation 要做 parent-child propagation？</summary>

因为 Agent Run 会产生 Subagent、Tool、process 等子执行。只取消父状态而不传播会留下后台任务继续运行和产生副作用。
</details>

<details><summary>3. 为什么 Progress 不一定是百分比？</summary>

很多 Agent Tool 事先不知道总工作量，更可靠的是 phase、processed count、heartbeat、current item 等可验证进展。
</details>

<details><summary>4. Tool 被 Cancel 后为什么还要记录 side-effect status？</summary>

因为取消信号到达时外部动作可能已经提交。Resume 或 Retry 前需要知道副作用是否发生，避免重复执行。
</details>
