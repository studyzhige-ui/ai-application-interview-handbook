# 18｜Multi-Agent、Subagent、Handoff、A2A 与 Workspace Concurrency

> 本章合并旧 `MultiAgentPatterns`、`SubagentHandoff`、`A2A`、`WorkspaceConcurrency`。它们共同回答：**什么时候值得把一个 Agent 拆成多个执行主体，以及拆开以后怎样分工、交接、隔离和避免互相破坏。**

## 1. Multi-Agent 不是默认升级

单 Agent 能完成时，多 Agent 会额外引入：

```text
更多 Token
更多 Coordination
更难 Eval
Context Duplication
Task Ownership Confusion
Shared Resource Conflict
Recursive Delegation
```

只有当任务具备：

```text
高并行性
专业角色差异
独立上下文有价值
任务可清晰切分
```

才更值得拆。

## 2. 常见模式

### Manager / Specialist

```text
Manager
├─ Research Agent
├─ Coding Agent
└─ Verification Agent
```

### Agents-as-Tools

主 Agent 把 Subagent 当一个有输入输出 Contract 的能力。

### Handoff

把任务 ownership 转移给另一个 Agent。

关键区别：

```text
Subagent call
→ parent still owns task

Handoff
→ ownership changes
```

## 3. Context Isolation

Subagent 不应该默认继承全部 Parent Context。

应按任务传：

```text
goal subset
relevant artifacts
constraints
permission scope
budget
```

这样减少：

- Token；
- Secret 泄露；
- unrelated memory pollution；
- role confusion。

## 4. Task Ownership

每个 Task 应明确：

```text
task_id
owner_agent
parent_task
status
inputs
expected artifact
acceptance criteria
budget
```

没有 ownership，多个 Agent 很容易重复劳动或都以为对方会处理。

## 5. Shared Workspace Conflict

两个 Coding Agent 并行：

```text
A edits service.py
B edits service.py
```

风险：

- race；
- lost update；
- test 与 patch 版本错配；
- merge conflict。

策略：

```text
workspace per agent
branch / worktree isolation
file ownership / lease
optimistic version check
merge/review boundary
serialized high-conflict operations
```

## 6. A2A 与 MCP 的边界

```text
MCP
= Agent Host 连接 Tool / Resource / Prompt

A2A
= 独立 Agent 系统之间做 capability discovery、task interaction、artifact exchange
```

A2A 不是内部函数调用的替代品。

如果两个模块在同一进程里，普通 typed API 可能更简单。

## 7. 防递归失控

Agent A → Agent B → Agent A 可能无限互调。

需要：

```text
delegation depth
visited agent/task chain
budget inheritance
ownership rules
loop detection
```

## 8. Aggregation

多个 Subagent 输出不能简单拼接。

需要：

```text
normalize artifact
→ conflict detection
→ evidence / provenance
→ verifier / manager aggregate
→ acceptance check
```

## 9. HUMAN-A / 权威资料

- `AGENT-030` Multi-Agent：29 来源；
- `AGENT-031` Shared Workspace Concurrency：7 来源；
- `AGENT-046` A2A：6 来源。

Anthropic 的 Multi-Agent Research 工程文章也强调：多 Agent 对可并行开放探索任务有价值，但成本和协调复杂度显著上升。

A2A 官方规范则更适合解释独立 Agent 系统之间的协议边界。

## 10. 🎯 面试回答

> Multi-Agent 只有在任务可并行、角色专业化或独立 Context 明显有价值时才值得引入。设计上要明确 Task Ownership、Context/Permission Isolation、Budget 和 Acceptance Criteria；共享 Workspace 最好用 branch/worktree、资源 ownership 或版本检查隔离冲突。MCP 连接 Tool/Context，A2A 面向独立 Agent 系统之间的任务和 Artifact 协作，两者不是同一层协议。

<details><summary>自测：为什么“把 Agent 拆得更多”不一定更好？</summary>

因为 Delegation、Context 复制、结果聚合、共享资源冲突和 Eval 都会增加成本；如果任务不可独立切分，多 Agent 只是在制造协调开销。
</details>