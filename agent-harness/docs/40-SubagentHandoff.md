# 40｜Subagent、Handoff、Context Isolation 与 Task Ownership

## 1. Subagent ≠ 复制主 Agent

Spawn 子 Agent 前要决定：

```text
Goal
Input context
Tools
Permissions
Workspace
Budget
Expected output
```

默认只给最小必要信息。

## 2. Context Isolation

好处：

- child 有独立 context window；
- 降低主 Context 污染；
- 权限更窄。

代价：parent 的隐含信息不会自动存在，需要明确 task contract。

## 3. Task Ownership

每个 subagent 应拥有明确 deliverable：

```text
research findings
patch in branch
artifact
structured answer
```

而不是“去看看”。

## 4. Handoff vs Agent-as-Tool

```text
Agent-as-Tool：控制权仍在 manager，child 返回结果
Handoff：后续对话/任务控制权转移
```

这两种语义在 Runtime 中不同。

## 5. Child Failure

Parent 应拿到结构化：

```text
completed / failed / cancelled
artifacts
evidence
retryability
```

而不是只能从 child 最后一段自然语言猜。

## 🎯 面试

Subagent 要有最小 Context、Tool、Permission、Budget 和明确 deliverable。Manager-style child call 与 handoff 的控制权不同；child 的 terminal state 和 artifact 应结构化回 parent，避免把完整 transcript 全拼回主 Context。

<details><summary>自测：为什么 Subagent 返回完整 History 通常不好？</summary>

会吞噬 parent Context，并把大量探索噪音带回来。更适合返回结果、证据与 artifact reference。
</details>
