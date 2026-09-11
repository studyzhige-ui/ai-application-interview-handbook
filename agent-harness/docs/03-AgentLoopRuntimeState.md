# 03｜Agent Loop、Run / Turn / Step 与 Runtime Event Model

> 本章合并旧 `04-MinimalAgentLoop`、`05-RunTurnStep`、`06-RuntimeMessageEvent`。它们不是三个孤立知识点，而是同一个问题的三层视角：**Agent 怎样在时间上推进一次任务。**

## 1. 先讲人话：Agent 的核心不是“会调用 Tool”，而是会循环推进任务

最小 Agent Loop 可以画成：

```text
Goal / User Input
      ↓
Build Context
      ↓
Model Decision
      ↓
┌───────────────┬─────────────────┐
│ Final Answer  │ Tool / Delegate │
└──────┬────────┴────────┬────────┘
       │                 ↓
       │             Execute
       │                 ↓
       │            Observation
       │                 ↓
       └──────────── Continue Loop
```

普通 LLM Call 到 `Model Output` 就结束；Agent Runtime 还要解释：

```text
输出是不是 Tool Call？
要不要执行？
执行结果如何变成下一轮 Observation？
State 怎样更新？
什么时候结束？
```

因此 Loop 是 Harness 的控制骨架。

## 2. 一个最小可运行的 Agent Loop

伪代码：

```python
async def run_agent(goal, runtime):
    state = runtime.start(goal)

    while True:
        context = runtime.build_context(state)
        decision = await runtime.call_model(context)

        if decision.type == "final":
            return runtime.finish(state, decision)

        if decision.type == "tool_call":
            result = await runtime.execute_tool(decision, state)
            runtime.record_observation(state, decision, result)
            continue

        raise RuntimeError("unsupported model decision")
```

这段代码只展示骨架。Production 版本还需要：

- max step / budget；
- permission；
- cancellation；
- tool failure；
- context compaction；
- checkpoint；
- trace；
- model / provider fallback。

## 3. 为什么要分 Run / Turn / Step

如果所有执行都叫 `session` 或 `message`，后面几乎无法精确表达状态。

一个实用分层：

```text
Session / Thread
└─ Run
   ├─ Turn 1
   │  ├─ Step A: model request
   │  ├─ Step B: tool call
   │  └─ Step C: observation
   └─ Turn 2
      └─ ...
```

课程使用以下工作定义。

### Session / Thread

跨多个用户交互持续存在的长期容器。

例如：一个持续数小时的 coding thread。

### Run

为某个 Goal 启动的一次可追踪执行。

Run 应至少有：

```text
run_id
status
started_at
ended_at
goal
budget
current_state
```

### Turn

一次用户输入或一次可归因的模型交互周期。

### Step

Run 内部更细的执行动作：

```text
model call
tool call
state transition
checkpoint
human approval
```

不同产品命名可能不同，重要的是**分层职责**。

## 4. 为什么这个分层对 Failure 很重要

假设：

```text
Run = 修复 issue #123
Turn = 用户说“继续”
Step = run_tests
```

如果测试超时：

```text
Step failed
```

不代表：

```text
Run failed
```

Runtime 可以：

```text
Step Failure
→ retry / repair / alternate tool
→ continue same Run
```

这就是为什么错误语义必须有执行层级。

## 5. Runtime 不是只有 Message，还需要 Event

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

## 6. Event 为什么最好是结构化的

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

## 7. Correlation ID 为什么关键

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

## 8. State Machine：Loop 不只是 while True

一个 Run 可以显式建成状态机：

```text
CREATED
  ↓
RUNNING
  ├─→ WAITING_TOOL
  ├─→ WAITING_APPROVAL
  ├─→ PAUSED
  └─→ RUNNING
        ↓
   COMPLETED / FAILED / CANCELLED
```

状态机的价值是：

```text
允许哪些 Transition？
Crash 后在哪恢复？
取消时清理什么？
Approval 后回到哪里？
```

如果没有明确状态机，长任务常出现“数据库里 status 是 running，但 worker 已经死了”这类幽灵状态。

## 9. Runtime State 应该有什么

一个简化模型：

```python
from dataclasses import dataclass, field

@dataclass
class RunState:
    run_id: str
    goal: str
    status: str = "running"
    step_count: int = 0
    last_tool_call_id: str | None = None
    artifacts: list[str] = field(default_factory=list)
    unresolved_errors: list[str] = field(default_factory=list)
```

这不是 Memory。

它描述：

> **现在执行到哪里、已经发生了什么、接下来还能做什么。**

## 10. 新用户指令怎样进入正在运行的 Agent

这是 `AGENT-042 Dynamic Instruction / Steering` 的核心。

错误做法：

```text
用户追加一句话
→ 直接塞到当前 Model Call 尾部
→ 希望模型自己理解优先级
```

更稳妥：

```text
New User Instruction
→ Runtime Event
→ 判断当前 Step 是否可中断
→ 更新 Goal / Constraint Snapshot
→ 取消或完成当前 Tool
→ 下一 Planning Boundary 生效
```

关键在于：

> 新指令不仅是 Message，也是 State Transition 输入。

## 11. 源码证据：Claude Code

固定快照中 `QueryEngine`：

- 一个 conversation 拥有 query lifecycle / session state；
- 每次 `submitMessage()` 开启新的 turn；
- messages、file cache、usage 等跨 turn 保留；
- 配置显式存在 `maxTurns`、`maxBudgetUsd`、`abortController`、tools、agents 与 permission callback。

这支持一个稳定课程抽象：

```text
Conversation Runtime
= Turn Lifecycle
+ Persistent State
+ Capability Set
+ Budget
+ Cancellation
```

## 12. 源码证据：Codex

固定 Codex 快照中，Context Compaction 相关代码直接引用：

```text
Session
StepContext
TurnContext
WorldState
EventMsg
```

Tool Router 中 `ToolCall` 也携带 `call_id`，再构造带 Session / StepContext / CancellationToken 的 Invocation。

这说明成熟 Runtime 会显式区分：

```text
长期 Session
→ 当前 Turn
→ 当前 Step / Invocation
→ Event / Tool Call
```

而不是把一切折叠成 Chat History。

## 13. Loop 什么时候继续，什么时候停止

最小规则：

```text
Model Final Answer
→ 可能停止

Tool Call
→ 执行后继续

Recoverable Failure
→ 修复 / 重试 / 换路后继续

Fatal Failure
→ 停止

Human Approval Required
→ Pause

Cancel Requested
→ Cancel
```

“可能停止”是因为 Final Answer 本身还可能需要 Outcome Verification。

例如 Coding Agent 说：

> “已经修复。”

Runtime 不应该只信它的文字，而要检查：

```text
tests_passed?
diff_exists?
requested_file_changed?
acceptance_criteria_met?
```

## 14. HUMAN-A 对应

高频 Canonical：

- `AGENT-003` Agent Loop / Runtime：36 来源；
- `AGENT-004` Message / Event Model：8 来源；
- `AGENT-006` Stop / Dead Loop：15 来源；
- `AGENT-042` Dynamic Instruction / Steering：1 个高价值完整流程。

真实追问通常是：

```text
Loop 怎么跑？
→ Tool Result 怎么回来？
→ State 放哪？
→ Dead Loop 怎么停？
→ 中途追加指令怎么办？
→ 怎样恢复 / Eval？
```

## 15. 🎯 30 秒回答

> Agent Loop 是 Goal 驱动的多步控制循环：Runtime 组装 Context，请模型决定 Final Answer、Tool 或 Delegate，执行动作后把 Observation 和 State Transition 记录下来，再进入下一轮。Production 里还要把 Session、Run、Turn、Step 分层，并用结构化 Event 和 correlation id 表达 Tool、Approval、Checkpoint、Cancel 等事实，这样才能做恢复、Trace 和 Eval。

## 16. ⚠️ 易错点

- 把 Run / Session / Message 全叫 Memory；
- 把 Chat History 当作 Runtime State；
- Tool Result 没有 call id；
- 只有字符串日志，没有结构化 Event；
- `while True` 没有 Stop / Budget / Cancel；
- Agent 说完成就直接标记 Run Completed。

## 17. 🔍 继续追问

```text
Tool Contract 为什么必须独立设计？
Tool Schema 谁校验？
并发 Tool Call 怎样相关联？
Step Failure 和 Run Failure 怎样区分？
怎样用 Event Log 做 Replay？
```

下一章正式进入 Tool Runtime。

<details><summary>自测 1：为什么 Tool Result 不是普通 Assistant Message？</summary>

因为它有明确的 Tool Call 来源、call_id、执行状态和 Runtime 语义，需要与具体 Invocation 相关联；模型可见表示只是其中一个 projection。
</details>

<details><summary>自测 2：为什么 Run / Step 分层对重试很重要？</summary>

因为一个 Step 的可恢复失败不应自动把整个 Run 判死。Runtime 需要知道失败发生在哪一层，才能决定 Retry、Repair、Fallback 或终止。
</details>

<details><summary>自测 3：Runtime Event 与 Message 最大区别是什么？</summary>

Message 主要服务模型输入输出；Event 记录系统真实发生的执行事实，包含很多模型不必看见但恢复、审计、指标和 Replay 必须知道的信息。
</details>