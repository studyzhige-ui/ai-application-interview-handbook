# 08｜Planning / ReAct、Goal Control、Stop Condition 与 Budget

> 本章合并旧 `14-PlanningReAct`、`15-StopLoopGuardBudget`，并纳入 Goal Drift 与 Dynamic Steering。它们共同回答：**Agent 怎样决定下一步、怎样不走偏、怎样知道该停。**

## 1. Planning 不是必须的“先写完整计划”

常见执行范式：

```text
ReAct
Reason → Act → Observe → Replan

Plan-Execute
先生成计划 → 执行 → 必要时重规划

Planner / Executor
一个组件拆任务，另一个组件执行

State Graph
显式 Node / Edge / State 推进
```

选择依据不是“哪个更高级”，而是任务结构：

- 步骤短、Observation 强：ReAct；
- 长任务、依赖多：Plan-Execute；
- 强确定性流程：Workflow / State Graph；
- 复杂开放探索：Agent Loop + 动态 Replan。

## 2. Goal Control

Agent 每轮都可能被最新 Observation 牵走，所以 Runtime 应持续保留：

```text
Original Goal
Hard Constraints
Current Subgoal
Completed Work
Open Blockers
Acceptance Criteria
```

不要只把“最近几条消息”当任务状态。

Goal Drift 常见信号：

```text
重复做已完成步骤
不断扩大任务范围
工具调用与目标无关
忽略用户硬约束
局部优化破坏最终验收条件
```

## 3. Stop Condition

停止不能只靠模型说“done”。

至少考虑：

```text
Model proposes final answer
+ task-specific acceptance check
+ unresolved blocker check
+ budget / step limit
+ repeated-action detection
```

例如 Coding Agent：

```text
模型说修好了
≠
测试通过
```

## 4. Dead Loop / Oscillation

典型模式：

```text
search A → read B → search A → read B → ...
```

可检测：

- repeated tool-call signature；
- repeated error；
- no state progress；
- same plan re-generated；
- token/cost growth without new artifact。

Runtime 可以：

```text
warn model
→ force reflection / alternate route
→ reduce remaining budget
→ ask user
→ terminate
```

## 5. Budget 是控制面，不只是成本统计

常见 Budget：

```text
max_steps
max_turns
max_tool_calls
max_tokens
max_cost_usd
deadline
per-tool retry budget
```

Budget 决定 Runtime 的可控性。

## 6. Dynamic Steering

用户中途追加要求：

```text
“不要改数据库，只修 API。”
```

应进入 Runtime State：

```text
new instruction event
→ evaluate current step interruptibility
→ update constraint snapshot
→ invalidate incompatible plan
→ next planning boundary takes effect
```

而不是无脑追加到聊天尾部。

## 7. HUMAN-A

- `AGENT-005` Agent Paradigm：31 来源；
- `AGENT-006` Stop / Dead Loop：15 来源；
- `AGENT-007` Goal Drift；
- `AGENT-042` Dynamic Instruction / Steering。

## 8. 🎯 面试回答

> Agent 的控制循环应该把 Planning、Goal State、Stop Condition 和 Budget 放在一起设计。模型可以动态 ReAct 或 Replan，但 Runtime 必须保留原始目标和硬约束，检测无进展循环，并用 step/token/cost/deadline 限制执行。最终停止最好由模型声明与任务验收共同决定，而不是只相信“我完成了”。

<details><summary>自测：为什么 Max Step 不是完整 Stop Condition？</summary>

Max Step 只是安全上限，不能证明任务已完成；真正停止还需要任务 Outcome / Acceptance Criteria。
</details>