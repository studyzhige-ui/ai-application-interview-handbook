# 42｜Shared Workspace 与并发冲突

## 1. Multi-Agent 最大坑之一

两个 Agent 同时操作同一个 repo：

```text
A reads old file
B edits file
A writes based on old snapshot
→ B's change lost
```

这是经典并发控制，不是 Prompt 能解决的问题。

## 2. 隔离策略

### Separate Workspace / Branch

每个 Agent 独立 worktree / branch，最后 merge。

优点：强隔离；缺点：合并成本。

### Resource Lock

对 file/module/task 加锁。

优点：简单；缺点：降低并行度、死锁风险。

### Optimistic Version Check

写入前检查 hash/version：

```text
read(version=7)
→ modify
→ write only if version==7
```

## 3. Task Ownership

最便宜的并发控制常常是任务划分：

```text
Agent A owns frontend
Agent B owns docs
```

但跨模块依赖仍要协调。

## 4. Shell / Process Conflict

不只有文件：

- 同一 dev server port；
- 同一 DB migration；
- package install；
- git index；
- temp files。

## 🎯 面试

Multi-Agent 共享 workspace 要像并发系统一样设计。优先用任务 ownership + isolated worktree/branch；共享写入则用 version check/lock，并把 git、process、port、migration 等非文件资源也纳入冲突模型。

<details><summary>自测：为什么“让 Agent 互相发消息说我正在改”不够？</summary>

自然语言协调没有原子性，消息也可能延迟。真正共享资源需要 Runtime 可执行的 ownership/version/lock 机制。
</details>
