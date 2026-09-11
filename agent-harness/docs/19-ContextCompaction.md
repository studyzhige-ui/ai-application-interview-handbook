# 19｜Context Compaction

## 1. Compaction 解决什么

长任务里 history 持续增长：

```text
H0 + H1 + H2 + ... → context window pressure
```

Compaction 将旧执行轨迹转换为更短的 durable summary / state projection，再继续运行。

## 2. 什么时候触发

```text
manual
pre-turn threshold
mid-turn emergency
task boundary
model switch to smaller window
```

Codex `compact.rs` 已明确存在 manual/auto、pre-turn/mid-turn 等不同 phase，说明触发时机本身就是 Runtime 语义。

## 3. Compaction Pipeline

```text
Select history
→ build compaction request
→ summarize / extract state
→ construct replacement history
→ preserve invariants
→ persist
→ recompute token usage
→ continue
```

所以它不是“summary(history)”一行代码。

## 4. 应保留什么

- original goal；
- hard constraints；
- accepted decisions；
- completed work；
- unresolved blockers；
- important artifacts / IDs；
- verification status；
- next step。

## 5. 不该把什么当核心状态

大量可重查日志、重复 chat、已经 superseded 的试错过程。

## 🎯 面试

Context Compaction 是一次 Runtime state transformation：选择旧 history、生成摘要、构造 replacement history、保留不可丢 invariant、持久化并重新计算 token，再继续下一轮。触发时机和恢复语义与摘要算法同样重要。

<details><summary>自测：为什么 Compaction 后通常仍要保留 Goal？</summary>

因为摘要如果只保留最近操作，Agent 可能在长任务中逐渐偏离最初目标和不可违反的约束。
</details>
