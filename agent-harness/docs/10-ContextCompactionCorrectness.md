# 10. Context Compaction、Correctness 与 Stale Context

`AGENT-009 Context Compaction` 是整个 Agent 真人面经里最强的信号之一。

但真正需要掌握的不是：

> “上下文太长就总结一下。”

而是：

> **当 Context 接近预算上限时，Runtime 怎样压缩历史，同时保证当前任务仍然能正确继续？**

成熟 Compaction 更接近一次 Runtime Transaction，而不是一次普通 Summary。

---

## 1. Compaction 为什么存在

随着 Agent 运行：

```text
User Message
Assistant Message
Tool Call
Tool Result
Plan
Memory
RAG Evidence
File Content
Error / Retry
```

不断累积。

如果不处理：

```text
Token ↑
Cost ↑
Latency ↑
Noise ↑
最终超过 Context Window
```

即使窗口足够大，也不代表应该无限保留：

> **Long Context Capacity ≠ 无限有效注意力 ≠ 免费存储。**

---

# 2. Compaction 与普通 Summary 的区别

普通 Summary 只关心：

```text
把长文本变短
```

Runtime Compaction 还必须关心：

```text
当前 Goal 还在吗？
约束还在吗？
已经完成什么？
哪些 Tool Side Effect 已发生？
当前 Workspace / Artifact 在哪里？
有哪些 unresolved problem？
哪些 approval 已经给过？
哪些状态不能重复执行？
```

所以正确抽象是：

```text
Compaction
= Select
+ Summarize / Project
+ Preserve Invariants
+ Build Replacement History
+ Persist
+ Recompute Budget
+ Trace / Validate
```

---

# 3. Codex `compact.rs` 给出的实现证据

固定源码索引已经核验 `codex-rs/core/src/compact.rs` 存在：

- manual / auto compaction；
- pre-turn / mid-turn / standalone phase；
- pre / post compact hooks；
- context-window-exceeded 处理；
- replacement history；
- compact metadata / window id；
- token usage recomputation；
- compaction analytics；
- compact 后长线程准确率风险 warning；
- live / persisted history 一致性相关逻辑。

这说明 Compaction 在成熟 Runtime 里并不是：

```text
history = summarize(history)
```

而是一个有阶段、有持久化、有可观测性、有恢复语义的状态转换。

这里我们只使用索引已经确认的事实，不推断未读取到的具体算法细节。

---

# 4. Claude Code 侧提供了什么证据

固定索引确认 Claude Code Runtime 存在：

```text
services/compact/*
snipCompact
snipProjection
CompactProgressEvent
memory re-injection
tool-result content replacement state
```

课程层稳定抽象是：

> **Context Compression 需要和 Projection、Memory、Tool Result Budget 共同设计。**

不是简单在 History 末尾追加一段“之前对话摘要”。

---

# 5. Compaction 什么时候触发

常见触发可以分：

## 5.1 Token Threshold

```text
estimated_context_tokens > soft_limit
```

提前压缩，而不是等 Provider 报 `context_length_exceeded`。

## 5.2 Phase Boundary

例如：

```text
一个大 Task 完成
→ 切换到下一个阶段
```

此时适合把“旧阶段的过程细节”压成阶段结论。

## 5.3 Tool Result Pressure

大量日志 / 文件 / Search Result 造成 Context 激增。

这时优先：

```text
Offload / Reference
```

不一定马上压整个 Conversation。

---

# 6. 哪些信息必须保留

建议至少定义一个 Compaction Invariant Set。

### Goal / Acceptance

```text
当前主目标
完成标准
禁止事项 / Constraints
```

### Runtime Progress

```text
已经完成的步骤
当前进行到哪里
下一步候选
Blocked 原因
```

### Side-effect Ledger

```text
Tool X 已经写 DB
Tool Y 已经发送消息
Payment request 已提交 idempotency_key=...
```

这类信息丢失会导致 Resume 后重复副作用。

### Artifact References

```text
修改过哪些文件
日志 artifact 在哪里
测试结果 path / id
```

### Unresolved Evidence

```text
哪些假设未验证
哪些测试仍失败
哪些用户问题未回答
```

---

# 7. 哪些内容适合压缩或外部化

例如：

```text
重复 Tool Schema
大量 raw log
已经完成阶段的逐步对话
旧搜索结果
可通过 artifact id 重新取回的文件
```

原则：

> **丢过程之前先确认能否重建。**

如果某个结果无法再次获取，又会影响后续决策，就不能只留一句模糊 Summary。

---

# 8. Replacement History 为什么重要

一种危险做法：

```text
old history
+ summary message
```

这样旧内容仍然占 Context，根本没有真正压缩。

另一种危险做法：

```text
history = [summary]
```

但 Summary 丢失了 System / Current User Goal / Tool Correlation。

更合理的是：

```text
Stable Instructions
+ Required Current State
+ Compact Summary
+ Recent High-value Events
+ Artifact References
```

形成新的 Replacement View。

这也解释了为什么 Codex `compact.rs` 会专门处理 replacement history，而不是只生成一个文本字段。

---

# 9. Compaction Correctness 怎样验证

`AGENT-010` 直接问：

> Summary 后如何验证信息没有丢坏？

至少可以分四层。

## 9.1 Structural Invariant

例如：

```text
current_goal exists
current_task_id exists
pending_steps preserved
side_effect_ledger preserved
artifact refs resolvable
```

## 9.2 Semantic Invariant

把压缩前关键事实做成 checklist：

```text
Constraint A still present?
Decision B still present?
Failure C still unresolved?
```

## 9.3 Continuation Test

同一个 Agent 从：

```text
Before Compaction Context
```

和：

```text
After Compaction Context
```

继续执行，检查关键下一步是否一致。

## 9.4 Regression Eval

建立长任务数据集：

```text
run without compaction
vs
run with compaction
```

比较：

```text
Task Success
Wrong Re-execution
Missed Constraint
Cost
Latency
```

---

# 10. Compaction 失败怎么办

Compaction 自己也可能失败：

```text
summary model timeout
summary too long
provider context error
persistence failure
hook failure
```

不应该：

```text
原 history 已删
→ compaction failed
→ session destroyed
```

更稳的流程：

```text
1. Build compact candidate
2. Validate candidate
3. Persist replacement / metadata
4. Atomically switch active view
5. Keep prior generation for rollback
```

这是课程层的通用设计建议，不声称 Claude Code / Codex 恰好按这个五步实现。

---

# 11. Stale Context 是另一类问题

Context 不超限，也可能坏。

例如：

```text
文件已经修改
但 Context 里还是旧文件内容
```

或者：

```text
用户已撤销某个约束
旧 Summary 仍说“必须遵守”
```

所以 Context Item / Summary 最好携带：

```text
source
version
timestamp / generation
```

当底层事实更新：

```text
invalidate / refresh / rehydrate
```

---

# 12. Summary Error 会产生“压缩后的错误记忆”

错误摘要很危险，因为它会变成新的高权重事实。

例如原始 History：

```text
User: 不要改数据库
Agent: 好的
```

Summary 错写：

```text
用户允许修改数据库 schema
```

后续模型可能稳定执行错误行为。

因此高风险 Constraint 应尽量：

```text
结构化持久化
```

而不是只存在自然语言 Summary。

---

# 13. Compaction 和 Memory 的边界

不要把两者混成：

```text
Compaction Summary = Long-term Memory
```

Compaction 目标：

```text
让当前 Run 在有限 Context 内继续
```

Memory 目标：

```text
让未来 Run / Future Turn 可以重新取回有价值信息
```

二者可以共享提取结果，但生命周期、写入标准和失效标准不同。

下一章进入 Memory。

---

# 14. HUMAN-A 信号

本章主要承接：

- `AGENT-009` Context Compaction：41 个独立来源；
- `AGENT-010` Compaction Correctness：15 个独立来源。

真实面试已经明显从：

```text
Context 满了怎么办？
```

追到：

```text
哪些信息不能丢？
怎么证明没压坏？
错误 Summary 怎么纠正？
```

---

# 15. 面试怎么答

## Q：Agent Context 快满了怎么办？

🎯 **30 秒回答**：

> 我不会简单删除最老消息。先把大 Tool Result 外部化，再按 Context Source 做预算；需要 compaction 时，把它当成一次 Runtime State Transition：选择需要压缩的 history，生成 summary / projection，同时强制保留 goal、constraints、progress、side-effect ledger 和 artifact refs，构造 replacement history，持久化并重新计算 token usage。压缩后要做 invariant 检查和长任务 regression，避免 summary 错误导致后续重复执行或 goal drift。

## Q：怎样验证 Compaction 没丢信息？

> 结构化验证必保字段，再用 continuation test 和长任务 eval 比较压缩前后的 task success、constraint violation、re-execution 和 cost，而不是只看 summary 读起来是否通顺。

---

# 16. 高频易错点

⚠️ **Compaction = Summary。** 只说了一小部分。

⚠️ **最老 History 全删掉就行。** 可能删掉关键决策和副作用事实。

⚠️ **Summary 正确性靠人工感觉。** Production 应有 invariant / regression。

⚠️ **Context 变短就一定更好。** 可能变成更短但错误的 Context。

---

# 17. 本章自测

<details><summary>1. 为什么 Compaction 更像 Runtime Transaction？</summary>

因为它不仅生成摘要，还会改变 active history / context view，需要保持状态不变量、持久化、重新计算预算，并在失败时避免破坏可恢复性。
</details>

<details><summary>2. Side-effect Ledger 为什么是 Compaction 必保信息？</summary>

如果外部动作已经成功但这个事实在压缩中丢失，Agent Resume 后可能再次执行支付、发送、写入等不可重复副作用。
</details>

<details><summary>3. Stale Context 和 Context Overflow 有什么区别？</summary>

Overflow 是容量问题；Stale Context 是事实版本失效问题。即使 Token 很少，旧文件、旧权限、旧约束仍会导致错误决策。
</details>
