# 14. Planning / ReAct / Plan-and-Execute：Agent 怎样决定下一步

`AGENT-005` 在冻结 HUMAN-A 中有 **31 个独立来源**，是 Agent Harness 的高频核心问题。

常见问法包括：

```text
ReAct 是什么？
Agent 为什么要 Planning？
Plan-and-Execute 和 ReAct 有什么区别？
Planner / Executor / Critic 怎么分工？
什么时候先计划，什么时候边做边想？
```

面试里最容易犯的错误是把这些模式背成名词表。

真正要理解的是：

> **Agent 的控制策略如何在“先规划”和“边观察边决策”之间权衡。**

---

# 1. 先讲人话：Planning 解决“下一步做什么”

Agent Loop 已经有：

```text
State
→ Model
→ Action
→ Observation
→ State
```

其中最关键的决策就是：

```text
下一步 Action 是什么？
```

简单任务：

```text
“读这个文件并总结”
```

几乎不需要复杂 Planning。

复杂任务：

```text
“把这个旧支付模块迁到新 API，保持兼容并补测试。”
```

可能需要：

```text
理解仓库
→ 找入口
→ 找依赖
→ 制定迁移顺序
→ 修改
→ 测试
→ 修复回归
```

这时 Planning 才真正有价值。

---

# 2. ReAct 的核心不是“把思维过程打印出来”

ReAct 原始思想可以简化成：

```text
Reason about current state
→ Act
→ Observe environment
→ update reasoning
→ Act again
```

论文：

https://arxiv.org/abs/2210.03629

最重要的是：

> **推理和环境交互交替进行。**

工程上不需要、也不应该依赖展示模型私有 Chain-of-Thought。

Runtime 只需要可靠捕获：

```text
Action
Observation
State Transition
```

然后让模型基于新的 Context 做下一步决策。

---

# 3. ReAct 适合什么任务

适合：

```text
信息不完整
中间 Observation 会强烈改变下一步
Tool 调用成本不高
路径难以提前写死
```

例如 Debug：

```text
先跑测试
→ 看错误
→ 决定读哪个文件
→ 再决定是否修改
```

如果一开始就要求模型生成 20 步完整计划，后面很可能：

```text
第 2 步 Observation 已经推翻第 8 步假设
```

所以这类任务适合边做边调整。

---

# 4. Plan-and-Execute

另一种模式：

```text
Goal
→ Planner 生成较高层 Plan
→ Executor 按 Plan 执行
→ 必要时 Replan
```

例如：

```text
1. 找认证入口
2. 梳理 token lifecycle
3. 修改 refresh 逻辑
4. 更新 tests
5. 运行 regression
```

它的价值：

- 给长任务结构；
- 减少局部 Tool Thrashing；
- 更容易做 progress；
- 可以分配给 Subagent；
- 便于验证里程碑。

但风险：

```text
Plan 可能很快过期
```

因此 Plan 不应该被当成不可变脚本。

---

# 5. ReAct vs Plan-and-Execute

| 维度 | ReAct | Plan-and-Execute |
|---|---|---|
| 控制方式 | 每轮观察后决定 | 先生成高层计划 |
| 适合 | 探索、不确定 | 长任务、有明显阶段 |
| 优点 | 灵活 | 结构清楚 |
| 缺点 | 容易局部游走 | Plan 可能陈旧 |
| Replan | 自然发生 | 需要显式触发 |
| Trace | Action 链 | Plan + Action 链 |

Production 常用 Hybrid：

```text
High-level Plan
+ Each Step uses ReAct
+ periodic replan
```

---

# 6. Planner / Executor 分离

可以逻辑分：

```text
Planner
→ 只决定任务结构

Executor
→ 完成当前子目标
```

例如：

```python
plan = [
    "inspect auth flow",
    "identify bug",
    "implement fix",
    "run regression tests",
]
```

Executor 当前只看：

```text
current_goal = inspect auth flow
```

好处：

- Context 更聚焦；
- 容易 checkpoint；
- 可以换不同模型；
- 可以让 Subagent 执行。

---

# 7. Critic / Verifier 不应该只是“再问一次模型”

常见架构：

```text
Planner
→ Executor
→ Critic
```

但如果 Critic 只是：

```text
“你觉得刚才做得对吗？”
```

同一个模型可能重复同样错误。

更有价值的是引入外部证据：

```text
Test
Static Check
Diff
Environment State
Business Rule
```

例如 Coding Agent：

```text
Executor: 修了代码
Critic: 不是只读答案，而是检查 test/diff
```

所以：

> **Verifier 的价值来自独立证据，不只是角色名。**

---

# 8. Planning State 要结构化

不要只在聊天历史里写：

```text
“我的计划是 1、2、3……”
```

更适合：

```python
from dataclasses import dataclass


@dataclass
class PlanStep:
    id: str
    goal: str
    status: str  # pending/running/done/blocked
    evidence: list[str]


@dataclass
class PlanState:
    version: int
    steps: list[PlanStep]
    current_step_id: str | None
```

这样 Runtime 可以：

- progress tracking；
- checkpoint；
- replan；
- subagent assignment；
- eval。

---

# 9. Plan Version 为什么重要

初始：

```text
Plan v1
1. fix parser
2. update tests
```

执行发现根因其实在 tokenizer：

```text
Plan v2
1. fix tokenizer
2. validate parser compatibility
3. update tests
```

如果只覆盖旧 Plan：

```text
不知道为什么改变
```

有 version / event：

```text
PlanCreated v1
ReplanTriggered(reason=...)
PlanCreated v2
```

Trace 更清楚。

---

# 10. 什么时候 Replan

常见触发：

```text
关键假设被推翻
Tool 连续失败
资源不存在
任务范围变化
用户追加指令
当前 Plan 没有 progress
Budget 快耗尽
Verifier 失败
```

不要每一 Step 都完整 Replan，否则：

- Token Cost 高；
- Plan 不稳定；
- 容易 oscillation。

---

# 11. Plan 不是 Task Success 的证据

Agent：

```text
Plan step 4 marked done
```

不代表真的 Done。

每个 Step 最好有：

```text
Completion Condition
Evidence
```

例如：

```text
Step: fix failing test
Completion: target test exits 0
Evidence: test run id / output
```

这样 Plan 从“待办清单”变成可验证状态机。

---

# 12. Planning 与 Tool Discovery 的关系

Plan 可能需要某种能力：

```text
“查 Jira 历史”
```

但 Tool 尚未加载。

Runtime 可以：

```text
Plan goal
→ capability discovery
→ load relevant Tool
→ execute
```

所以 Plan 不应绑定具体 Tool 名：

```text
step = call_jira_search_v2
```

更稳定的是：

```text
step goal = retrieve historical incidents
```

Executor 再选择当前可用 Tool。

---

# 13. Planning 与 Context 的关系

长计划本身也占 Context。

如果 Plan 有 100 个 Step，每轮全部塞进去：

```text
Token Waste
```

可以只注入：

```text
overall goal
current plan summary
current step
critical constraints
next few relevant steps
```

完整 Plan 留 Runtime State。

这就是：

> **State ≠ Context。**

---

# 14. Planning 与 Budget

规划不是越深越好。

如果任务只值 5 秒：

```text
花 10 秒生成完美计划
```

反而亏。

可以根据任务复杂度决定：

```text
simple → direct act
medium → short plan
complex → explicit plan + checkpoint + verifier
```

这是 Adaptive Planning。

---

# 15. Anthropic 的 Agent Pattern 启发

Anthropic `Building effective agents` 强调从简单、可组合的 pattern 开始，并介绍：

- prompt chaining；
- routing；
- parallelization；
- orchestrator-workers；
- evaluator-optimizer；
- autonomous agents。

它的核心启发不是“必须选一个 pattern”，而是：

> **控制结构应该匹配任务复杂度。**

来源：

https://www.anthropic.com/engineering/building-effective-agents

---

# 16. Claude Code / Codex 对 Planning 的启发

这里要非常谨慎：

> 我们不把某个源码里的具体 prompt 当作通用 Planning 标准。

但固定 Claude Code / Codex 源码都显示成熟 Coding Agent Runtime 有：

```text
Task / Subagent
Tool Loop
State
Budget
Cancellation
Verification
```

这些能力允许 Planning 不只是“模型写 TODO”，而是真正绑定 Runtime 生命周期。

Claude Code `Task.ts` 有 Task Status；QueryEngine 有 `maxTurns` / budget；Codex Router/Session 有 step context 和 child management capability。

课程抽象：

> **Plan 应最终映射到 Runtime 可追踪的 Task / Step，而不是只停在自然语言。**

---

# 17. Multi-Agent Orchestrator 也是 Planning 的一种外化

复杂任务：

```text
Research
Code
Test
Review
```

Planner 可以决定：

```text
Subagent A → research
Subagent B → implementation
Subagent C → verification
```

这时 Plan 变成：

```text
Task Graph / Ownership
```

但并不是：

> “Agent 越多 Planning 越好。”

Subagent 会引入：

- coordination；
- context transfer；
- workspace conflict；
- cost。

Multi-Agent 章节再深入。

---

# 18. Common Failure 1：Overplanning

任务：

```text
“读 config.py 找 timeout”
```

Agent：

```text
生成 12 步计划
创建 3 个 subagent
做两轮 review
```

这就是过度规划。

解决：

```text
complexity-aware planning
```

先问：

```text
是否真的需要多步未知决策？
```

---

# 19. Common Failure 2：Plan Lock-in

Agent 发现：

```text
原计划假设错误
```

但继续机械执行。

解决：

- Replan trigger；
- evidence-driven state；
- Plan version；
- current-step validation。

---

# 20. Common Failure 3：Plan Thrashing

每得到一点新信息：

```text
Plan v1
→ v2
→ v3
→ v4
```

计划不断变化，没有执行。

解决：

- replan threshold；
- minimum execution horizon；
- budget；
- progress metric。

---

# 21. Common Failure 4：Plan 和 Reality 脱节

Plan 里说：

```text
测试已完成
```

但 Runtime 没有任何 Test Event。

因此 Plan Status 应由：

```text
Runtime evidence
```

更新，而不是只让模型自己宣称。

---

# 22. 一个 Hybrid Planning Loop

```python
async def run_with_plan(state):
    if state.plan is None:
        state.plan = await planner.create_plan(state.goal)

    while not state.done:
        current = state.plan.current_step()

        result = await executor.execute_goal(current.goal, state)
        current.evidence.extend(result.evidence)

        if verifier.is_complete(current, result):
            current.status = "done"
        elif should_replan(result, state):
            state.plan = await planner.replan(
                state.goal,
                state.plan,
                result,
            )
        else:
            current.status = "blocked"

        if state.plan.all_done():
            state.done = verifier.verify_final(state)
```

教学重点：

```text
Plan
+ Execution
+ Observation
+ Replan
+ Evidence-based completion
```

---

# 23. Coding Agent 示例

任务：

```text
“升级 authentication SDK，不能破坏旧 token flow。”
```

高层 Plan：

```text
1. map auth entry points
2. identify SDK API changes
3. implement compatibility adapter
4. update tests
5. run regression
```

Step 1 内部可以用 ReAct：

```text
search symbol
→ read file
→ follow imports
→ inspect config
```

如果发现项目根本没有目标 SDK：

```text
Replan
```

这就是 Hybrid。

---

# 24. 高频易错点

⚠️ **ReAct = 输出完整思维链**  
工程核心是 Action/Observation loop，不需要展示私有 CoT。

⚠️ **Plan 越详细越好**  
过细计划会快速过期并增加 Token。

⚠️ **Plan 一旦生成就不变**  
真实 Agent 必须支持 evidence-driven replan。

⚠️ **Critic = 同一个模型再夸/骂一遍**  
最好结合 Test、Diff、环境状态等独立证据。

⚠️ **Plan Status 由模型口头更新**  
应尽量由 Runtime Evidence 驱动。

---

# 25. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> ReAct 适合边执行边观察再调整，Plan-and-Execute 适合长任务先建立高层结构。Production 常用 Hybrid：高层 Plan 管目标和里程碑，当前 Step 内用 ReAct 处理不确定性，关键假设变化或连续失败时 Replan。Plan 应放在结构化 Runtime State，并用 Test/Artifact/Environment Evidence 更新完成状态，而不是只保存在自然语言里。

## Level 2｜2–3 分钟

> 我会根据任务复杂度做 adaptive planning。简单任务直接执行，中等任务短 plan，复杂任务用 versioned PlanState，每个 step 有 goal/status/completion condition/evidence。Replan 触发包括关键假设失效、tool failure、用户 steering、verifier failure。为了避免 plan thrashing，不是每个 observation 都重做整个 plan。Planner/Executor 可以分模型或分角色，但 Verifier 最好依赖独立外部证据。

## Level 3｜继续追问

🔍 **ReAct 和 Plan-and-Execute 怎么选？**  
看未知程度、任务长度、Tool 成本、是否有明显阶段；通常可以混合。

🔍 **Plan 如何支持 Resume？**  
结构化持久化 version/current step/status/evidence，和 checkpoint 一起恢复。

🔍 **为什么 Plan 不应写死 Tool Name？**  
Capability 会动态变化，Plan 更稳定地表达 goal，Executor 再绑定当前 Tool。

---

# 26. 本章证据

## HUMAN-A

- `AGENT-005` Execution Paradigm / Planning：31 sources；
- `AGENT-003` Agent Loop：36 sources；
- `AGENT-006` Stop / Loop：15 sources。

## 权威资料

- ReAct original paper  
  https://arxiv.org/abs/2210.03629
- Anthropic — Building effective agents  
  https://www.anthropic.com/engineering/building-effective-agents

## 源码实现参考

- Claude Code `QueryEngine.ts`, `Task.ts`
- Codex Session / Step Context / child-management Tool Runtime

源码只用于实现校准，不增加 HUMAN-A 频率。

---

# 27. 自测

<details><summary>1. ReAct 的核心是什么？</summary>

推理/决策与环境 Action/Observation 交替进行，让 Agent 根据新信息逐步调整，而不是一次性生成不可变完整方案。
</details>

<details><summary>2. 为什么 Production 常用 Hybrid Planning？</summary>

高层 Plan 提供长任务结构和进度，局部 ReAct 保留对未知环境的适应能力，两者分别解决结构与动态反馈。
</details>

<details><summary>3. Plan 为什么应该结构化持久化？</summary>

便于 checkpoint/resume、progress、replan、subagent ownership、eval，并避免只靠自然语言历史重新推断当前状态。
</details>

<details><summary>4. Critic 怎样才更可靠？</summary>

尽量使用独立证据，例如 Test、Diff、Static Check、业务状态，而不是只让同一个模型再次主观评价自己的答案。
</details>
