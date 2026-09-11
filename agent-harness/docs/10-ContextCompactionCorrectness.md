# 10｜Context Compaction、Correctness 与 Stale Context

> 本章合并旧 `19-ContextCompaction` 与 `20-CompactionCorrectness`。Compaction 不是“让 LLM 总结历史”这么简单，而是一次**Runtime State Transformation**。

## 1. 为什么需要 Compaction

长任务会持续增长：

```text
History + Tool Results + Retrieved Context + Plans + File Summaries
→ Token Pressure
→ Latency / Cost 上升
→ Context Window 接近上限
```

最粗暴的做法是 Trim，但会丢失长期任务状态。

Compaction 的目标是：

> 用更短的可恢复表示替代一部分历史，同时保持任务继续执行所需的 invariant。

## 2. Compaction Pipeline

```text
Trigger
→ select history range
→ build compaction input
→ summarize / project durable state
→ construct replacement history
→ preserve goal / constraints / artifacts
→ persist
→ recompute token usage
→ continue
```

这就是为什么它不能缩成：

```python
history = summarize(history)
```

## 3. Trigger

可能有：

```text
manual
pre-turn threshold
mid-turn emergency
context-window-exceeded fallback
task boundary
model switch
```

触发过早浪费摘要成本；触发过晚可能已经无法构造有效请求。

## 4. 必须保留哪些 Invariant

至少考虑：

```text
Original Goal
Hard Constraints
Accepted Decisions
Completed Work
Current Plan / Subgoal
Unresolved Blockers
Important Artifact IDs
Permission / Environment Facts
Verification Status
Next Step
```

而重复日志、被 supersede 的尝试、可随时重查的信息更适合丢弃或转成引用。

## 5. Correctness 才是最难的地方

摘要可能：

- 漏掉约束；
- 把假设写成事实；
- 保留过时结论；
- 混淆已完成和待完成；
- 丢掉 Artifact / File Version；
- 错误归纳 Tool Failure。

所以 Compaction 后要验证：

```text
goal preserved?
constraints preserved?
state transition valid?
artifact references resolvable?
completed/open work consistent?
critical facts sourceable?
```

## 6. Stale Context 与 Summary Pollution

即使摘要当时正确，环境也可能变化：

```text
file changed
DB row changed
branch switched
permission changed
new user instruction arrived
```

因此 Summary 应携带：

```text
source version / snapshot
generated_at
scope
superseded status
```

需要时重新读取 Source of Truth。

## 7. Compaction 与 Memory 的边界

```text
Compaction
= 为当前长任务缩短 Runtime History

Memory
= 跨未来请求可再次召回的持久信息
```

Compaction Summary 不应该自动晋升为长期 Memory。

否则一次错误摘要会长期污染后续任务。

## 8. 源码证据：Codex

固定快照 `compact.rs` 明确存在：

- manual / auto；
- pre-turn / mid-turn / standalone phase；
- replacement history；
- compact metadata / window；
- token recomputation；
- pre/post hook；
- context-window-exceeded recovery；
- analytics。

这非常清楚地支持：

```text
Compaction = Runtime Transaction
```

## 9. 源码证据：Claude Code

固定快照 `services/compact/` 下存在 auto compact、micro compact、session memory compact、cleanup、prompt 等多个组件。

`autoCompact.ts` 还会：

- 为 summary output 预留空间；
- 计算阈值；
- 维护连续失败计数；
- 在重复失败后 Circuit Break，避免无限浪费 API 调用。

说明 Context Management 自己也需要 failure handling。

## 10. HUMAN-A

- `AGENT-009` Context Compaction：41 来源，是 Agent 全库最强信号之一；
- `AGENT-010` Compaction Correctness：15 来源。

Verified Chain：

```text
Context Assembly
→ Compaction
→ Correctness
→ Memory Pollution
→ Resume
```

## 11. 🎯 面试回答

> Compaction 是 Runtime 对历史状态的一次有损变换：达到阈值后选择旧历史，生成更短的 summary/state projection，构造 replacement history，显式保留 Goal、Constraint、已完成工作、Artifact、未解决问题等 invariant，持久化并重新计算 Token。真正难点不是总结算法，而是 correctness：要防止丢约束、保留过时事实和把错误摘要写进长期 Memory。

## 12. ⚠️ 易错点

- Context 超了才开始处理——太晚；
- Summary 越短越好——错；
- Compaction = Memory——错；
- Compaction 后不用验证——高风险；
- 只保留最近几轮——容易 Goal Drift。

<details><summary>自测：为什么 Compaction Summary 不应自动写入 Long-term Memory？</summary>

因为它是针对当前执行的有损状态投影，可能包含暂时假设和摘要误差。自动长期化会把一次压缩错误扩散到未来 Session。
</details>