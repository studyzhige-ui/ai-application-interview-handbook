# 04. L2 运行层：执行循环与控制

[← 03](03-ApplicationAndInteraction.md) · [Agent 主线](../README.md) · [05 →](05-ContextEngineering.md)

> 主线位置：**L2 运行层**。应用已承接任务，现在展开负责推进它的运行层。
>
> 本章产物：**一次执行的闭环、对象与停止语义**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 先走完一次观察—行动—反馈，再理解对象和事件。模型适配与受控工具执行暂作黑盒：前者返回候选决策，后者返回成功、失败或结果未知；09–11章再展开内部实现。

[先把执行对象说清楚](#part-1) → [循环推进：模型提出候选，运行时决定怎样兑现](#part-2) → [用计划管理进度，而不是把计划当成功证明](#part-3) → [停止、预算、重复与方向修正](#part-4) → [事件把循环变成可解释的执行](#part-5)

<a id="part-1"></a>

## 1. 先把执行对象说清楚

本课程采用工作定义：Task 是目标与验收对象；Run 是一次受管理执行；Step 是运行时定义的推进单位；Model Invocation 是一次模型请求；Tool Call 是一次调用请求；Operation 是需要识别和核对的外部逻辑动作。

Codex App Server 的 Thread 是持续会话容器，Turn 是一次用户请求及后续 Agent 工作，Item 是有类型的输入输出单元。一次 Turn 可以含多次推理与工具交互；一个 Item 可以产生 started、delta、completed 等多个生命周期事件，但不同 Item 支持的事件并不完全相同。

```text
交互视图：Thread → Turn → Item → Event
业务/执行视图：Task → Run → Step / Operation
```

不要强制把两棵树拼成 `Session → Run → Turn` 的行业统一层级。关联方式由应用协议明确。Thread 也不是操作系统线程。

依据：[Codex App Server](https://developers.openai.com/codex/app-server)。

<a id="part-2"></a>

## 2. 循环推进：模型提出候选，运行时决定怎样兑现

```text
载入目标与执行状态 → 组装上下文 → 调用模型
→ 解析候选动作 → 校验范围、预算与权限
→ 执行工具 / 等待人工 / 提交完成候选
→ 记录结果与状态 → 核验进度 → 继续、暂停或终止
```

下面是控制骨架，不是可直接部署的完整代码：

```python
async def advance(run, runtime):
    while runtime.can_continue(run):
        runtime.apply_pending_instructions(run)
        context = await runtime.build_context(run)
        decision = await runtime.decide(context)
        if decision.kind == 'final':
            evidence = await runtime.verify_candidate(run, decision)
            if evidence.accepted:
                return await runtime.complete(run, evidence)
            await runtime.record_verification_failure(run, evidence)
        elif decision.kind == 'tool':
            outcome = await runtime.execute_controlled(run, decision)
            await runtime.record_and_checkpoint(run, outcome)
        elif decision.kind == 'ask':
            return await runtime.pause_for_input(run, decision)
        else:
            await runtime.record_invalid_decision(run, decision)
    return await runtime.stop_with_reason(run)
```

这里的 execute_controlled 包含调用校验与必要授权；record_and_checkpoint 也不意味着与外部副作用存在一个跨系统原子事务。完成、错误、暂停、取消必须具有不同语义。

<a id="part-3"></a>

## 3. 用计划管理进度，而不是把计划当成功证明

Planning、ReAct、Plan–Execute–Replan 和 Critic 是运行层可以采用的策略，不必各自变成独立服务。模型可以隐式规划，也可以维护显式计划。

### 先讲人话：Planning 不是“先写一份超长计划”

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

### ReAct 解决什么问题

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

### Plan-Execute-Replan 什么时候更合适

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

### Goal Control：Agent 怎么知道自己还在做原任务

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

<a id="part-4"></a>

## 4. 停止、预算、重复与方向修正

运行层必须同时回答“还能不能做”和“有没有必要继续做”。达到限制是有原因的停止，不代表任务成功。

### Stop Condition 不是只有 `max_steps`

一个成熟 Runtime 至少有三类停止条件。

#### 成功停止

```text
Acceptance Criteria satisfied
→ produce final answer / artifact
```

#### 无法继续

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

#### 强制停止

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

### Budget 应该是多维的

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

### Dead Loop / Oscillation 怎么检测

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

### Dynamic Instruction / Steering 怎么进入当前 Run

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

### Planning Failure Timeline

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

### Framework 不应该决定你的 Planning 模型

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

<a id="part-5"></a>

## 5. 事件把循环变成可解释的执行

模型消息是模型输入输出的表示；运行事件记录真实发生的调度、调用、批准、检查点与停止。记录可观察输入、动作、证据及结果，不要求暴露模型隐藏思维过程。

### Runtime 不是只有 Message，还需要 Event

Model-visible Message 常见：

```text
system
user
assistant
function/tool call
tool result
```

但 Runtime 还需要记录模型看不见的事实：

```text
run_started
tool_queued
permission_requested
permission_granted
tool_started
tool_progress
checkpoint_written
compaction_started
compaction_finished
cancel_requested
run_finished
```

所以应区分：

```text
Model Message
= 给模型看的输入 / 输出表示

Runtime Event
= 系统真实发生过的事实
```

二者可以相关，但不能等同。

### Event 为什么最好是结构化的

不要只记：

```text
"tool failed"
```

至少应保留：

```json
{
  "event_type": "tool_finished",
  "run_id": "r_123",
  "turn_id": "t_9",
  "step_id": "s_31",
  "tool_call_id": "call_7",
  "tool_name": "run_tests",
  "status": "failed",
  "error_kind": "timeout",
  "duration_ms": 30012
}
```

结构化 Event 才能支持：

- Trace；
- Replay；
- Debug；
- Metrics；
- Eval；
- Incident Analysis。

### Correlation ID 为什么关键

Model 发出：

```text
Tool Call A
Tool Call B
```

如果 Runtime 只把两个 Result 按时间塞回去，而没有 `call_id`，并发时很容易错配。

稳定关系应该是：

```text
ToolCall(call_id = c17)
        ↓
ToolStarted(c17)
        ↓
ToolProgress(c17)
        ↓
ToolResult(c17)
```

`call_id` 是 Tool protocol 的相关性键。

## 将黑盒接到状态机：一次失败不等于整个任务失败

最小执行状态可用 `RUNNING / WAITING_TOOL / WAITING_INPUT / STOPPED` 表达；STOPPED还要携带成功、失败、取消或预算耗尽的原因。名称是工作定义，关键是允许的状态转换、谁持有执行权、恢复后如何确定唯一下一步。

`call_id`关联模型的一次调用及结果；`operation_id`标识需要核对的逻辑动作；`attempt_id`区分重试尝试。一个逻辑动作可以有多次尝试，不能因为超时就把它伪装成新动作。07章打开恢复语义，11章打开工具执行语义。

<details>
<summary>动手：一个可运行的最小控制循环（Python 3.11+，无网络、无真实副作用）</summary>

这是对旧版最小Loop的教学重写，不是Codex或Claude Code源码。模型用预设决策序列替代，文件用字典替代；它只测试调度、白名单、相关性与引用可解析，**不证明报告语义真实，也不提供生产级幂等或持久化**。

<!-- runnable: report-loop -->
```python
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Decision:
    kind: str
    value: str = ""
    citations: tuple[str, ...] = ()

def run_report(decisions: Iterable[Decision], max_steps: int = 4):
    sources = {"intro.txt": "范围说明", "notes.txt": "已确认的记录"}
    observations: dict[str, str] = {}
    events: list[tuple[str, str, str]] = []
    iterator = iter(decisions)
    for step in range(1, max_steps + 1):
        decision = next(iterator, None)
        if decision is None:
            return "incomplete", events
        if decision.kind == "read":
            call_id = f"call-{step}"
            if decision.value not in sources:
                events.append((call_id, "denied", decision.value))
                return "blocked", events
            observations[decision.value] = sources[decision.value]
            events.append((call_id, "tool_result", decision.value))
        elif decision.kind == "final":
            refs = decision.citations
            resolvable = bool(refs) and all(r in observations for r in refs)
            if not decision.value or not resolvable:
                events.append((f"step-{step}", "verification_failed", "citations"))
                return "unverified", events
            events.append((f"step-{step}", "draft_verified", "reference-check-only"))
            return "completed_reference_check", events
        else:
            return "invalid_decision", events
    return "budget_exhausted", events

ok = [Decision("read", "intro.txt"), Decision("read", "notes.txt"),
      Decision("final", "报告草稿", ("intro.txt", "notes.txt"))]
status, events = run_report(ok)
assert status == "completed_reference_check"
assert [e[0] for e in events[:2]] == ["call-1", "call-2"]
assert run_report([Decision("read", "secret.txt")])[0] == "blocked"
assert run_report([Decision("final", "草稿", ("intro.txt",))])[0] == "unverified"
assert run_report([Decision("read", "intro.txt")] * 5)[0] == "budget_exhausted"
assert run_report([Decision("delete", "intro.txt")])[0] == "invalid_decision"
print("report-loop: 5 cases passed")
```

下一步不是增加更多模型，而是逐一打开Context、持久状态和Tool Executor黑盒。本例返回的完成状态特意叫 `completed_reference_check`：通过有限检查不能夸称整个报告质量已被证明。

</details>

## 本章自测

<details>
<summary>Turn、模型调用、Item 是同一件事吗？</summary>

不是。Codex 的 Turn 包含一次请求及后续工作，可能包含多次推理和工具交互；Item 是有类型的输入输出单元。

</details>

<details>
<summary>final 文本能否直接触发成功状态？</summary>

应先按契约验证完成证据；结束回复、达到预算和完成任务是不同语义。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>同一工具再次调用是否一定是死循环？</summary>

不一定；分页、合法重试和新输入查询都可重复。结合动作签名、状态进展和同类错误判断。

</details>

<details>
<summary>教学Loop的引用检查通过，能证明自然语言结论真实吗？</summary>

不能；它只证明示例校验覆盖的有限属性，语义真实性需要更强证据核验。

</details>

## 回到主线

现在应能独立说明：一次执行的闭环、对象与停止语义。下一章：[L2 运行层：上下文组装、预算与压缩](05-ContextEngineering.md)。

对应真人问题：`AGENT-003`、`AGENT-004`、`AGENT-005`、`AGENT-006`、`AGENT-007`、`AGENT-042`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 03](03-ApplicationAndInteraction.md) · [Agent 主线](../README.md) · [05 →](05-ContextEngineering.md)
