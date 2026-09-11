# 20｜Compaction Correctness 与 Stale Context

## 1. 压短不等于压对

最危险的不是 Token 超限，而是摘要看起来合理、其实丢了关键事实。

```text
original state
→ lossy summary
→ wrong future decision
```

真人面经已经稳定追问“压缩后怎样证明关键约束没丢”。

## 2. Correctness Invariants

可以显式定义必须保存：

```text
goal
hard constraints
external side effects
artifact identities
current task status
known failures
verification evidence
```

Compaction 后做 invariant check。

## 3. Stale Context

代码文件已经被修改，但历史 summary 仍写旧行为；Memory 也可能引用旧版本。

解决思路：

```text
artifact version / hash
summary derived_from version
read-on-use validation
invalidate stale projection
```

## 4. Summary 不是 Source of Truth

对可精确存储的结构化状态，例如：

```text
branch name
commit SHA
resource ID
approval decision
```

直接存 State，不要让 LLM Summary 重写。

## 5. Compaction Regression

准备长任务 eval，比较：

- 完成率；
- constraint violation；
- resume accuracy；
- redundant work；
- token savings。

## 🎯 面试

Compaction 最大风险是 silent information loss。我会把 Goal、hard constraints、side-effect ledger、artifact/version、当前任务状态等定义为 invariant，结构化状态直接持久化；summary 只压缩叙事历史，并通过版本和长任务 regression 检查 stale / loss。

<details><summary>自测：为什么“把所有历史交给更强模型总结”仍不够？</summary>

因为 summarization 本质有损，而且结构化执行事实不应依赖模型重述；还需要 invariant、version 和可恢复 source of truth。
</details>
