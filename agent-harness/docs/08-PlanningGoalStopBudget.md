# 08. Planning / ReAct、Goal Control、Stop Condition 与 Budget

Agent 能调用 Tool 以后，很快就会遇到第二个问题：

> **它下一步应该做什么？什么时候应该继续，什么时候必须停？**

这一章把 Planning、ReAct、Goal Control、Stop Condition 和 Budget 放在同一个知识小板块，是因为它们共同解决一个问题：

> **怎样让 Agent 的控制循环朝目标推进，而不是无限行动、来回震荡或偏离任务。**

---

## 1. 先讲人话：Planning 不是“先写一份超长计划”

最小 Agent Loop 已经是：

```text
Observe current state
→ Model decides next action
→ Runtime executes
→ New observation
→ Decide again
```

Planning 只是让“下一步决策”更有结构。

有的任务适合：

```text
边观察边行动
```

有的任务适合：

```text
先拆目标
→ 再按阶段执行
→ 中途根据新证据重规划
```

所以不要把 Planning 理解成：

> Agent 一开始必须生成一个十步计划，然后一字不改地照着执行。

真正的 Runtime 需要的是：

```text
Goal
+ Current State
+ Evidence
+ Constraints
+ Remaining Budget
→ Next Action / Replan / Stop
```

---

# 2. ReAct 解决什么问题

ReAct 的稳定抽象是：

```text
Reason / Decide
→ Act
→ Observe
→ Continue
```

它的价值不在于把模型的私有推理过程暴露出来，而在于说明：

> **Agent 的决策应该能使用环境返回的新 Observation，而不是一次模型调用决定全部未来动作。**

例如查线上故障：

```text
先查日志
→ 日志显示 DB timeout
→ 再查 DB metrics
→ metrics 显示 connection pool exhausted
→ 再检查 pool / concurrency
```

第二步取决于第一步结果。

这类任务天然适合迭代式 Agent Loop。

Tier C 中 ReAct 原始论文和 Anthropic `Building effective agents` 都支持这种“行动—观察—继续决策”的课程抽象。

---

# 3. Plan-Execute-Replan 什么时候更合适

如果任务具有明显阶段：

```text
理解需求
→ 修改 5 个文件
→ 跑 Test
→ 修复失败
→ 最终总结
```

可以让 Runtime 维护显式计划：

```text
PlanItem
- id
- description
- status: pending/running/done/blocked
- evidence
```

执行过程中：

```text
Plan
→ Execute one step
→ Observe
→ Update state
→ Replan if needed
```

这比“计划一次，然后永不更新”更适合动态环境。

---

# 4. Goal Control：Agent 怎么知道自己还在做原任务

Long-running Agent 很容易出现 Goal Drift：

```text
原目标：修复登录超时

中途：发现日志系统有问题
→ 开始重构日志模块
→ 又发现依赖版本旧
→ 开始升级依赖
→ 原任务被遗忘
```

Runtime 可以把 Goal 拆成三层：

```text
Primary Goal
Acceptance Criteria
Constraints / Non-goals
```

例如：

```text
Primary Goal:
修复登录接口 P99 timeout

Acceptance Criteria:
- 原有测试通过
- 新增超时回归测试
- P99 降到目标范围

Non-goal:
- 不重构整个认证系统
```

这样每次重新规划时都能问：

```text
这个动作是否直接推进 Acceptance Criteria？
```

---

# 5. Stop Condition 不是只有 `max_steps`

一个成熟 Runtime 至少有三类停止条件。

## 5.1 成功停止

```text
Acceptance Criteria satisfied
→ produce final answer / artifact
```

## 5.2 无法继续

例如：

```text
缺权限
缺关键输入
外部服务持续失败
用户必须确认高风险动作
```

此时应该：

```text
Pause / Ask / Escalate
```

而不是继续随机尝试。

## 5.3 强制停止

```text
max_turns
max_tool_calls
max_cost
max_tokens
wall_clock_timeout
retry_budget
```

Claude Code 固定源码索引里，`QueryEngine` 配置明确存在 `maxTurns`、`maxBudgetUsd`、`fallbackModel`、`abortController` 等边界。课程抽象因此是：

> **Budget 属于 Runtime 控制面，不只是 Provider billing。**

---

# 6. Budget 应该是多维的

不要只有：

```text
max_steps = 20
```

更完整的预算可以是：

```text
Turn Budget
Tool-call Budget
Token Budget
Cost Budget
Time Budget
Retry Budget
Sub-agent Budget
```

伪代码：

```python
@dataclass
class RunBudget:
    max_turns: int
    max_tool_calls: int
    max_cost_usd: float
    deadline: float
    max_retries: int
```

每次行动前：

```text
check budget
→ allowed: continue
→ near limit: prefer cheaper / shorter path
→ exhausted: stop with explicit reason
```

---

# 7. Dead Loop / Oscillation 怎么检测

真人面经 `AGENT-006` 直接追问 Dead Loop / Oscillation。

常见模式：

```text
Tool A fails
→ model calls Tool B
→ B says use A
→ model calls A again
→ repeat
```

或者：

```text
search(query1)
→ no result
→ rewrite(query1)
→ search(query1)
→ no result
```

Runtime 可以维护：

```text
recent action signatures
state hash
no-progress counter
same-error counter
repeated tool-argument pattern
```

例如：

```python
if repeated_signature_count(tool_name, args_hash) >= 3:
    emit("loop_detected")
    force_replan_or_stop()
```

注意：

> Loop Detection 不是简单“同一个 Tool 不能调用两次”。

合法任务可能需要连续分页、重试或多次搜索。

真正应该检测的是：

```text
状态没有实质推进
+
动作模式重复
```

---

# 8. Dynamic Instruction / Steering 怎么进入当前 Run

用户可能在 Agent 执行中补一句：

> “别改数据库，只改应用层。”

新指令不能只是追加到聊天记录末尾，然后假设模型自然理解。

Runtime 需要决定：

```text
这是补充信息？
修改约束？
替换目标？
要求取消当前 Tool？
```

然后更新：

```text
Run State / Constraints
→ 后续 Planning
```

如果当前 Tool 是 destructive operation，还可能需要先 Cancellation / Approval。

这对应 HUMAN-A `AGENT-042 Dynamic Instruction / Steering`。

---

# 9. Planning Failure Timeline

一个典型失败：

```text
T0  Agent 制定计划：修改 A → B → C
T1  修改 A 后环境发生变化
T2  旧计划中的 B 已不再成立
T3  Runtime 仍机械执行 B
T4  产生无效甚至破坏性修改
```

真正的问题不是“LLM 不聪明”，而是：

```text
Plan 被当成 immutable script
```

更稳的设计：

```text
每个阶段完成
→ Observe new state
→ Validate next step precondition
→ continue / replan
```

---

# 10. Framework 不应该决定你的 Planning 模型

LangGraph、OpenAI Agents SDK 或其它框架都能表达某些控制流，但课程顺序应该反过来：

```text
先定义：
Goal / State / Stop / Budget / Replan semantics
        ↓
再选框架 primitive
```

而不是：

```text
框架有 Planner Node
→ 所以系统必须有 Planner Node
```

---

# 11. 证据分层

### HUMAN-A

本章主要承接：

- `AGENT-005`：ReAct / Plan-Execute-Replan / Planner-Executor-Critic；
- `AGENT-006`：Stop Condition / Dead Loop；
- `AGENT-007`：Goal Drift；
- `AGENT-042`：Dynamic Steering。

### Claude Code 固定源码快照

`QueryEngine` 索引确认存在：

```text
maxTurns
maxBudgetUsd
fallbackModel
abortController
```

这支持“控制循环 + Budget + Cancellation 是 Harness 一级能力”的实现事实。

### Tier C

- ReAct 原始论文：Reason/Act/Observation 交替；
- Anthropic `Building effective agents`：区分 workflow 与 agent，并强调从简单可组合模式开始。

这些证据用于课程设计，不改变 HUMAN-A Source Count。

---

# 12. 面试怎么答

## Q：Agent 怎样避免无限循环？

🎯 **30 秒回答**：

> 我不会只放一个 `max_steps`。Runtime 会同时维护明确 Goal 和 Acceptance Criteria，并设置 turn、tool、time、cost、retry 等硬预算；运行中记录最近动作、错误和状态变化，如果发现相同 Tool+Arguments 或同类错误反复出现但状态没有推进，就触发 loop detection，让模型 replan、向用户求助或停止。这样既有硬上限，也有 no-progress 的软检测。

## Q：ReAct 和 Plan-Execute-Replan 怎么选？

> ReAct 更适合下一步高度依赖环境 Observation 的任务；Plan-Execute-Replan 更适合有明显阶段、需要进度跟踪的长任务，但计划必须允许根据新状态重规划，而不是一次生成后机械执行。

---

# 13. 高频易错点

⚠️ **Planning = 一次生成完整计划。** 错，动态任务需要 Replan。

⚠️ **max_steps 就能解决 Loop。** 只能兜底，不能发现 no-progress。

⚠️ **模型自己说 done 就算完成。** 应由 Acceptance Criteria / Verification 判断。

⚠️ **Budget 只有 Token。** 还包括 Tool、时间、成本、Retry、Sub-agent 等。

---

# 14. 本章自测

<details><summary>1. 为什么 Stop Condition 和 Evaluation 有关系？</summary>

因为“是否完成”不能只靠模型自报，需要可验证 Acceptance Criteria。很多任务的停止其实依赖结果验证，而不是自然语言中的“完成了”。
</details>

<details><summary>2. Dead Loop 检测为什么不能简单禁止重复 Tool Call？</summary>

因为分页、分片搜索、Retry 等合法流程本来就可能多次调用同一 Tool。应该结合参数签名、状态变化和 no-progress 判断是否真正震荡。
</details>

<details><summary>3. 用户中途修改需求时 Runtime 应做什么？</summary>

先分类新指令是补充信息、约束变更、目标替换还是取消信号，再更新 Run State / Constraints，并决定是否需要取消当前动作或重新规划。
</details>
