# 16｜Context Assembly

## 1. Context 到底是什么

不是只有 Prompt：

```text
System / Policy Instructions
Task Goal
User Input
Repository / Environment Instructions
Memory
Conversation History
Tool Definitions
Retrieved Evidence
Tool Results
Runtime State
```

Anthropic 的 Context Engineering 强调的正是“当前 inference 时模型实际拿到的全部 token”。

## 2. Assembly 是每轮 Runtime 工作

```python
context = assemble(
    instructions,
    task_state,
    selected_history,
    relevant_memory,
    available_tools,
    current_observations,
)
```

它不是 session 初始化时做一次就结束。

## 3. 顺序也有语义

需要明确：

- 长期 instruction 与临时 user message 谁优先；
- Tool Result 应放在对应 call 后；
- Memory 是事实还是建议；
- Retrieved untrusted content 是否加边界标签。

## 4. Source of Truth 与 Projection

Context 是 Runtime Truth 的投影，不应成为唯一状态存储。

例如任务已创建远端资源，不能只靠历史 message 记住 resource id，应存 state，再决定本轮是否注入 Context。

## 5. 最小 Context 原则

目标不是“能塞多少塞多少”，而是：

> 在有限 Token 中保留当前决策最有价值、最新、可信的状态。

## 🎯 面试

Context Assembly 是每轮把 instruction、goal、state、history、memory、tools 和 observations 选择性投影给模型。Context 不是数据库，也不是越长越好；Runtime Truth 应独立持久化，然后按当前决策需要组装。

<details><summary>自测：为什么 Memory 不应无条件全部注入？</summary>

可能过期、不相关、冲突，也会挤占当前任务 token。Memory 需要检索、可信度和生命周期管理。
</details>
