# 22｜Session、State、History 的区别

## 1. 四个最容易混的词

```text
Session  执行作用域 / identity
State    当前执行事实
History  过去事件 / message
Memory   可跨未来任务检索的信息
```

## 2. 一个例子

Coding Agent：

```text
Session = issue #123 本次修复运行
State = branch=fix-123, tests=2 failed, step=debug
History = 已经读过哪些文件、模型说了什么、Tool Call
Memory = repo build command 是 `pnpm test`
```

它们不能只用一个 `messages` 表代替。

## 3. State 的要求

State 最好：

- schema 明确；
- versioned；
- serializable；
- 有 owner；
- 能从 durable store 恢复。

## 4. Session 生命周期

```text
create
→ active
→ paused
→ resumed
→ completed / cancelled
→ archived
```

OpenAI Agents SDK 把 session 作为持久对话上下文；Codex / Claude Code 也有 conversation/session 状态边界。

## 🎯 面试

Session 是运行身份与作用域；State 是当前真相；History 是过去轨迹；Memory 是未来可复用信息。分清后 Checkpoint、Resume、Compaction 和长期 Memory 才不会互相污染。

<details><summary>自测：Compaction 应直接删除 History 吗？</summary>

模型可见 History 可以替换为摘要，但审计/Replay 所需的 durable event/history 未必应该删除；两者是不同投影。
</details>
