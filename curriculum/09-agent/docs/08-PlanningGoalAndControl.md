# 08. Planning / ReAct：计划、目标、停止与预算

Agent 能调用 Tool 以后，很快就会遇到第二个问题：

> **它下一步应该做什么？什么时候应该继续，什么时候必须停？**

这一章把 Planning、ReAct、Goal Control、Stop Condition 和 Budget（预算） 放在同一个知识小板块，是因为它们共同解决一个问题：

> **怎样让 Agent 的控制循环朝目标推进，而不是无限行动、来回震荡或偏离任务。**

[← 上一章](07-ToolConcurrencyAndCancellation.md) · [Agent 目录](../README.md) · [下一章 →](09-ContextAssemblyAndCache.md)

---

<a id="section-1"></a>

## 1. 先讲人话：Planning 不是“先写一份超长计划”

<a id="legacy-08-01"></a>

Plan写“准备怎么做”，State（状态）写“现在实际怎样”。计划是先读A再读B，状态却可能是A已读、B无权限。计划必须跟随观察调整，而不是模型自己给自己的完成证明。

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

真正的 Runtime（运行时执行系统） 需要的是：

```text
Goal
+ Current State
+ Evidence
+ Constraints
+ Remaining Budget
→ Next Action / Replan / Stop
```

---

<a id="section-2"></a>

## 2. ReAct 解决什么问题

<a id="legacy-08-02"></a>

ReAct 的稳定抽象是：

```text
Reason / Decide
→ Act
→ Observe
→ Continue
```

它的价值不在于把模型的私有推理过程暴露出来，而在于说明：

> **Agent 的决策应该能使用环境返回的新 Observation（观察结果），而不是一次模型调用决定全部未来动作。**

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

<a id="section-3"></a>

## 3. Plan-Execute-Replan 什么时候更合适

<a id="legacy-08-03"></a>

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

<a id="section-4"></a>

## 4. Goal Control：Agent 怎么知道自己还在做原任务

<a id="legacy-08-04"></a>

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

这里要分两个视图。程序的“当前计划”可以被新版本清单替换；会话历史中的“模型曾提出计划P1，随后调整为P2”则是已经发生的记录。二者不矛盾。更新计划通常通过一条新消息或工具调用追加到历史，程序据此更新当前视图，而不是回头改写每一条旧消息。

```text
用户任务U1
→ 模型调用更新计划(P1)
→ 工具确认
→ 读取A获得新证据
→ 模型调用更新计划(P2：B受阻，先整理A)
→ 工具确认
→ 按P2继续
```

下一个任务U2可以产生P3。程序应把它关联新任务，清楚结束或替换旧计划；不能让旧任务未完成的条目无声混入新任务。历史怎样成为下一次输入、压缩以后怎样保留当前计划，见下一章与第10章。这里先掌握“**当前视图可更新，旧消息通常追加保留**”。

---

<a id="section-5"></a>

## 5. Stop Condition 不是只有 `max_steps`

<a id="legacy-08-05"></a>

一个成熟 Runtime 至少有三类停止条件。

### 5.1 成功停止

```text
Acceptance Criteria satisfied
→ produce final answer / artifact
```

### 5.2 无法继续

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

### 5.3 强制停止

```text
max_turns
max_tool_calls
max_cost
max_tokens
wall_clock_timeout
retry_budget
```

Claude Code 固定源码索引里，`QueryEngine` 配置明确存在 `maxTurns`、`maxBudgetUsd`、`fallbackModel`、`abortController` 等边界。课程抽象因此是：

> **Budget 属于 Runtime 控制面，不只是 Provider（模型服务方） billing。**

---

<a id="section-6"></a>

## 6. Budget 应该是多维的

<a id="legacy-08-06"></a>

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
# 控制示意：多维预算限制继续工作，耗尽预算不应被标成任务成功。
from dataclasses import dataclass

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

<a id="section-7"></a>

## 7. Dead Loop / Oscillation 怎么检测

<a id="legacy-08-07"></a>

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
# 控制示意：多维预算限制继续工作，耗尽预算不应被标成任务成功。
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

<a id="section-8"></a>

## 8. Dynamic Instruction / Steering 怎么进入当前 Run

<a id="legacy-08-08"></a>

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

如果当前 Tool 是 destructive operation，还可能需要先 Cancellation / Approval（批准）。

这对应 HUMAN-A `AGENT-042` Dynamic Instruction / Steering。

“顺便检查D”通常可以排队到安全边界，“不要发送报告”可能要求停止尚未开始的发送。先识别消息影响，既不每条消息都杀掉当前工具，也不无条件拖到整项任务结束。

---

<a id="section-9"></a>

## 9. Planning Failure Timeline

<a id="legacy-08-09"></a>

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

合法分页会反复调用同一工具，但游标和新结果在变化；参数变化却一直得到同类错误才可能是振荡。联合观察、状态进展和预算判定，而不是仅比较函数名。

---

<a id="section-10"></a>

## 10. Framework 不应该决定你的 Planning 模型

<a id="legacy-08-10"></a>

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

<a id="human-a"></a>

## 11. HUMAN-A 信号

#### HUMAN-A

本章主要承接：

- `AGENT-005`：ReAct / Plan-Execute-Replan / Planner-Executor（执行器）-Critic；
- `AGENT-006`：Stop Condition / Dead Loop；
- `AGENT-007`：Goal Drift；
- `AGENT-042`：Dynamic Steering。

#### Claude Code 固定源码快照

`QueryEngine` 索引确认存在：

```text
maxTurns
maxBudgetUsd
fallbackModel
abortController
```

这支持“控制循环 + Budget + Cancellation 是 Harness 一级能力”的实现事实。

#### Tier C

- ReAct 原始论文：Reason/Act/Observation 交替；
- Anthropic `Building effective agents`：区分 workflow 与 agent，并强调从简单可组合模式开始。

这些证据用于课程设计，不改变 HUMAN-A Source Count。

---

<a id="interview"></a>

## 12. 面试怎么答

### Q：Agent 怎样避免无限循环？

🎯 **30 秒回答**：

> 我不会只放一个 `max_steps`。Runtime 会同时维护明确 Goal 和 Acceptance Criteria，并设置 turn、tool、time、cost、retry 等硬预算；运行中记录最近动作、错误和状态变化，如果发现相同 Tool+Arguments 或同类错误反复出现但状态没有推进，就触发 loop detection，让模型 replan、向用户求助或停止。这样既有硬上限，也有 no-progress 的软检测。

### Q：ReAct 和 Plan-Execute-Replan 怎么选？

🎯 **30 秒回答**：

> ReAct 更适合下一步高度依赖环境 Observation 的任务；Plan-Execute-Replan 更适合有明显阶段、需要进度跟踪的长任务，但计划必须允许根据新状态重规划，而不是一次生成后机械执行。

### Q：计划更新会不会破坏Prompt Cache？

🎯 **30 秒回答**：

> 要区分更新当前计划视图和改写历史。常见做法把新计划作为新消息或工具调用追加到尾部，程序更新当前视图，尽量保留已有前缀；若把可变计划每轮重写在最前面则会影响前缀复用。实际还受工具集合、系统指令、压缩和供应商缓存规则影响。

### Q：怎样检测Agent死循环？

🎯 **30 秒回答**：

> 结合最近动作签名、相同错误和实际进展，而不是禁止重复工具。分页有新数据可以继续；反复同查询无结果应计为无进展，要求换策略、澄清或停止。总时间和费用预算兜底，但不能只加大步数掩盖循环。

### Q：计划说done了，为什么不能直接结束？

🎯 **30 秒回答**：

> done首先是声明。应检查报告、引用、测试或业务回执是否满足验收；如果没有证据，状态仍未完成。程序可以拒绝完成候选并把缺口反馈给模型，或在无法推进时结束为未完成而非伪造成功。

---

<a id="pitfalls"></a>

## 13. 高频易错点

⚠️ **Planning = 一次生成完整计划。** 错，动态任务需要 Replan。

⚠️ **max_steps 就能解决 Loop。** 只能兜底，不能发现 no-progress。

⚠️ **模型自己说 done 就算完成。** 应由 Acceptance Criteria / Verification 判断。

⚠️ **Budget 只有 Token。** 还包括 Tool、时间、成本、Retry（重试）、Sub-agent 等。

⚠️ **Plan等于全部State。** Plan只记录未来步骤与清单状态，不包含全部活动调用、结果和授权。

⚠️ **新计划必须覆盖旧模型消息。** 通常追加更新事件并替换当前视图，两者分开。

⚠️ **ReAct必须输出私有思考。** 关键是行动与观察反馈，不需要展示隐藏推理。

⚠️ **预算耗尽也是完成。** 它只是停止原因，应明确未完成状态。

⚠️ **每个Agent都需要独立Planner服务。** 简单任务可隐式规划，按任务需要选择。

---

<a id="self-test"></a>

## 14. 本章自测

<details><summary>1. 为什么 Stop Condition 和 Evaluation 有关系？</summary>

因为“是否完成”不能只靠模型自报，需要可验证 Acceptance Criteria。很多任务的停止其实依赖结果验证，而不是自然语言中的“完成了”。

</details>

<details><summary>2. Dead Loop 检测为什么不能简单禁止重复 Tool Call？</summary>

因为分页、分片搜索、Retry 等合法流程本来就可能多次调用同一 Tool。应该结合参数签名、状态变化和 no-progress 判断是否真正震荡。

</details>

<details><summary>3. 用户中途修改需求时 Runtime 应做什么？</summary>

先分类新指令是补充信息、约束变更、目标替换还是取消信号，再更新 Run State / Constraints，并决定是否需要取消当前动作或重新规划。

</details>

<details><summary>4. 读B被拒绝后，计划里应改什么？</summary>

把B标为受阻，并说明影响的验收条件，再选择澄清、授权或部分交付。不要把它当普通临时错误无限重试，也不能直接标完成。

</details>

<details><summary>5. 计划从P1改到P2，P1是否必须删除？</summary>

不必。当前计划视图指向P2，历史保留P1到P2的变化；上下文过长时才选择性压缩。保留历史不代表每轮必须注入全部历史。

</details>

<details><summary>6. 调用同一搜索工具五次是否一定是死循环？</summary>

不是。如果查询和证据不断推进，可能合理。要看无进展、重复输入和相同错误，而不是只统计工具名。

</details>

<details><summary>7. 多了模型规划，任务质量却不变而成本翻倍，怎么办？</summary>

与确定性基线比较，在没有质量或能力收益的范围移除不必要规划。Agent化不是越多越好。

</details>

<details><summary>8. 用户要求只读，计划中出现修改原件，谁来阻止？</summary>

模型可收到约束，但真正阻止需要工具权限和资源访问边界；规划检查及时发现问题，执行门不能依赖模型始终听话。

</details>

<details><summary>9. Codex update_plan返回确认，模型还能知道清单内容吗？</summary>

它刚提交的工具调用包含计划参数，历史中有这段信息；确认结果不必重复整个清单。不能从短确认推断计划丢了，也不能推断它被固定在System Prompt。

</details>

---

[← 上一章](07-ToolConcurrencyAndCancellation.md) · [Agent 目录](../README.md) · [下一章 →](09-ContextAssemblyAndCache.md)
