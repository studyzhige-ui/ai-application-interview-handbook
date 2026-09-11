# 11｜Memory Architecture、Lifecycle 与 Correctness

> 本章把 Memory Architecture、Lifecycle、Staleness/Correctness 放回同一个知识板块。Memory 不是“把历史存到 Vector DB”，而是**哪些信息值得跨未来请求保留，以及怎样写入、召回、更新、失效和纠错。**

## 1. 先区分五个词

```text
Context    当前一次 Model Call 看见什么
History    过去发生过什么
State      Runtime 当前执行事实
Memory     未来可能再次取回的信息
Checkpoint 可恢复执行点
```

这五个对象可以互相引用，但不能混成一个表。

## 2. Memory 分层

一个实用模型：

```text
Working Memory
→ 当前任务临时事实 / scratch

Session Memory
→ 本次 Thread 内长期有用的信息

Long-term Memory
→ 跨 Session 的用户偏好、稳定事实、经验
```

也可以按内容分：

```text
semantic facts
procedural knowledge
episodic experience
user preference
```

## 3. Write Policy 比 Storage 更重要

不是每条对话都值得写长期 Memory。

写入前可以判断：

```text
稳定吗？
未来会复用吗？
来源可靠吗？
是否有权限长期保存？
是否只是临时任务状态？
```

## 4. Promotion / Consolidation

短期信息晋升长期可以走：

```text
candidate extraction
→ dedup / conflict check
→ confidence / source
→ approval / policy
→ long-term store
```

不要让每次 Compaction Summary 自动升级成长期记忆。

## 5. Retrieval-on-demand

Long-term Memory 不应该每轮全部注入。

```text
current goal
→ retrieve relevant memory
→ freshness / tenant / permission filter
→ rank
→ inject only useful subset
```

否则 Memory 越多，Context 越差。

## 6. Memory Correctness

长期 Memory 会出现：

```text
expired
wrong
conflicting
superseded
source deleted
permission revoked
```

所以 Memory Entry 最好携带：

```text
memory_id
content
source
created_at
updated_at
confidence
valid_from / valid_to
version
scope / tenant
```

## 7. 冲突与纠错

不要简单覆盖：

```text
旧：用户喜欢 Python
新：用户现在主要用 Rust
```

更合理：

```text
version old fact
mark superseded
retain provenance
serve latest valid fact
```

这样能支持 Audit / Undo。

## 8. 源码证据

Claude Code 固定快照中，`QueryEngine` 会加载 memory prompt，`memdir/` 提供 memory 导航，Tool Context 还维护 nested memory paths，避免重复注入。

这说明成熟 Harness 的 Memory 问题包含：

```text
storage
+ selection
+ dedup
+ injection
+ lifecycle
```

而不是一个 `memory = []`。

## 9. HUMAN-A

- `AGENT-014` Memory Architecture：36 来源；
- `AGENT-015` Memory Lifecycle：8 来源；
- `AGENT-016` Memory Correctness / Staleness：6 来源。

## 10. 🎯 面试回答

> Memory 是可在未来再次召回的信息，不等于当前 Context、Chat History 或 Runtime State。Production Memory 要设计分层、写入策略、promotion、retrieval-on-demand、版本与失效；长期事实还要保存 provenance / confidence / scope，遇到过期或冲突时版本化纠正，而不是无限堆历史。

<details><summary>自测：为什么“把全部历史 Embedding 后检索”还不算完整 Memory Architecture？</summary>

因为它只解决存储和部分召回，没有解决什么值得写、如何更新/失效、冲突纠错、权限、版本和注入策略。
</details>