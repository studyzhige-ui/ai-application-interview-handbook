# 39｜Multi-Agent：什么时候值得拆 Agent

## 1. Multi-Agent 不是默认升级

拆 Agent 会增加：

```text
context duplication
token cost
coordination
state synchronization
failure surface
evaluation difficulty
```

Anthropic multi-agent research 的公开经验也指出它对高并行、开放探索问题更合适，同时成本显著更高。

## 2. 适合拆的信号

- 子任务相对独立；
- 可以并行；
- 需要不同 Tool/Permission；
- Context 可以隔离；
- 最终能明确聚合结果。

不适合：强顺序依赖、共享同一复杂 workspace、每步都要紧密同步。

## 3. Pattern

### Manager + Specialists

Lead 拆任务、收结果。

### Agents as Tools

一个 Agent 把 specialist 当 capability。

### Handoff

控制权转给另一个 Agent。

### Parallel Workers

并发探索独立方向。

## 4. 成本预算

Multi-Agent 需要全局：

```text
max subagents
max total tokens
max wall time
max tool calls
```

不能每个 child 都以为自己预算无限。

## 🎯 面试

只有当任务可并行、Context 可隔离、角色/工具差异明显且结果容易聚合时我才拆 Multi-Agent。否则单 Agent + Tools/Skills 通常更简单。Multi-Agent 的代价是 token、协调、共享状态和评测复杂度。

<details><summary>自测：为什么 Coding Task 往往比 Research 更难直接并行多 Agent？</summary>

多个 Agent 可能修改同一代码依赖和 workspace，任务之间耦合强，会产生合并/验证冲突。
</details>
