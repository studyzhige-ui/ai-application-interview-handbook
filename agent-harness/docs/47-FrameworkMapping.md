# 47｜Framework Mapping 与 Build-vs-Buy

## 1. 到这里才看 Framework

现在已经知道 Runtime Problem，才能正确理解框架抽象：

```text
Agent Loop
State
Tool
Handoff
Checkpoint
Trace
Guardrail
```

Framework 只是这些问题的一种实现。

## 2. 映射思路

### OpenAI Agents SDK

可以映射：

```text
Agent / Runner → Loop
Tools → Tool Runtime
Sessions → persisted conversation context
Handoffs / Agent-as-tool → delegation
Guardrails → validation boundary
HITL RunState → pause/approval/resume
Tracing → observability
Sandbox Agent → execution environment
```

### LangGraph

更适合把显式 state / node / transition 组织成 graph，尤其 deterministic + agentic mixed workflow。

### LangChain 等

提供 Model / Tool / Retriever 等大量 integration，但不要把 integration catalog 当 Runtime theory。

## 3. 什么时候自己写 Loop

适合：

- Runtime 很简单；
- 需要完全控制 state/tool semantics；
- 框架抽象反而复杂。

## 4. 什么时候需要框架

- checkpoint / graph / handoff 等成熟能力明显节省成本；
- 团队需要标准化；
- integration 丰富；
- observability / deployment ecosystem 合适。

## 5. Build-vs-Buy Checklist

```text
state model fit?
recovery semantics?
tool/permission fit?
trace visibility?
provider lock-in?
extensibility?
testing?
operational cost?
```

## 🎯 面试

我不会用“框架流行度”选型，而是先列 Runtime requirements：state、checkpoint、tool policy、streaming、multi-agent、trace、deployment，再看框架抽象是否匹配。简单场景自己写 loop 反而更透明；复杂状态图和恢复需求再引入 LangGraph/Agents SDK 等。

<details><summary>自测：为什么课程最后才讲 LangGraph？</summary>

否则容易把 Node/Edge API 当成 Agent 本质，无法解释离开框架后 Context、Tool Failure、Checkpoint、Permission 为什么仍然存在。
</details>
