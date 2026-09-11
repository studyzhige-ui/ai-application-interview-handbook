# 24｜Checkpoint 与 Resume

## 1. Checkpoint 保存什么

不是“保存聊天记录”。一个可恢复 checkpoint 至少要知道：

```text
run/session identity
state version
current task / step
model-visible context reference
pending tool / approval
side-effect ledger
artifacts
budget
```

## 2. Checkpoint 时机

常见：

- Tool 完成后；
- 高风险副作用前后；
- Human approval pause；
- Compaction 后；
- Task boundary；
- 定期时间点。

## 3. Resume Pipeline

```text
load checkpoint
→ validate version / ownership
→ reconcile external effects
→ restore state
→ rebuild current context
→ continue from safe boundary
```

不是把旧 prompt 再发一遍。

## 4. Approval Resume

OpenAI Agents SDK 官方 HITL 明确支持暂停后把 RunState 序列化，再 approve/reject 后继续，是很好的通用心智模型。

## 5. Crash Window

最经典：

```text
Tool charge succeeded
↓ crash
checkpoint still says pending
↓ resume
```

如果没有幂等键 / external status reconciliation，就会重复扣款。

## 🎯 面试

Checkpoint 要保存 Runtime state，而非只保存 messages。Resume 前还要 reconcile 外部副作用和 pending approval，然后从安全 step boundary 继续。最大的正确性问题是 Tool 成功与 checkpoint 写入之间的 failure window。

<details><summary>自测：Checkpoint 越频繁越好吗？</summary>

不是。频繁 checkpoint 增加存储和延迟；太少则恢复时重复工作和副作用风险增加。应放在重要 side-effect/task boundary。
</details>
