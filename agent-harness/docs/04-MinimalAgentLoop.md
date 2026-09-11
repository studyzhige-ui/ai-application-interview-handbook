# 04. Minimal Agent Loop：从一次 Model Call 到可执行 Agent

`AGENT-003` 在冻结 HUMAN-A 中有 **36 个独立来源**，是 Agent Harness 模块最高频问题之一。

这一章只做一件事：

> **把 Agent 最核心的循环真正跑通，并理解每一层为什么存在。**

先不要碰 Memory、Compaction、MCP、Multi-Agent。那些都建立在 Loop 之上。

---

# 1. 先讲人话：Agent 为什么需要 Loop

一次普通模型调用：

```text
User
  ↓
Model
  ↓
Answer
```

Agent 则需要：

```text
User Goal
   ↓
Model decides next action
   ↓
Runtime executes action
   ↓
Environment returns observation
   ↓
Model sees observation
   ↓
decides next action
   ↓
...
   ↓
Final Answer / Done
```

所以 Agent 的核心不是“有 Tool”，而是：

> **Model Decision → Runtime Action → Observation → Model Decision 的闭环。**

---

# 2. 最小 Loop 的五个对象

最小系统只需要先有：

```text
1. State
2. Context Builder
3. Model
4. Tool Executor
5. Stop Rule
```

关系：

```text
             ┌─────────────┐
             │ RuntimeState│
             └──────┬──────┘
                    │
                    ▼
              Build Context
                    │
                    ▼
                 Model
                    │
           ┌────────┴────────┐
           ▼                 ▼
      Final Answer         Tool Call
                                │
                                ▼
                          Tool Executor
                                │
                                ▼
                           Observation
                                │
                                └────→ State → next loop
```

---

# 3. 为什么不能只写 while True

很多 Demo：

```python
while True:
    response = call_model(messages)
    if response.tool_call:
        result = run_tool(response.tool_call)
        messages.append(result)
    else:
        return response.text
```

它能演示概念，但缺少：

- max step；
- cancellation；
- invalid tool；
- schema validation；
- timeout；
- duplicate call；
- permission；
- state persistence；
- event trace；
- final outcome verification。

Production Loop 必须是：

> **显式状态机，而不是无限 while。**

---

# 4. 一个更合理的最小实现

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RunStatus(str, Enum):
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RuntimeState:
    run_id: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    step_count: int = 0
    status: RunStatus = RunStatus.RUNNING
    final_output: str | None = None


async def run_agent(state, model, tool_registry, max_steps=20):
    while state.status == RunStatus.RUNNING:
        if state.step_count >= max_steps:
            state.status = RunStatus.FAILED
            raise RuntimeError("max steps exceeded")

        state.step_count += 1

        context = build_context(state, tool_registry)
        decision = await model.generate(context)

        if decision.kind == "final":
            state.final_output = decision.text
            state.status = RunStatus.SUCCEEDED
            break

        if decision.kind != "tool_call":
            raise RuntimeError(f"unsupported decision: {decision.kind}")

        tool = tool_registry.get(decision.tool_name)
        if tool is None:
            observation = {
                "ok": False,
                "error": "tool_not_found",
            }
        else:
            observation = await tool.execute(decision.arguments)

        state.messages.append(decision.to_message())
        state.messages.append(tool_result_message(
            call_id=decision.call_id,
            result=observation,
        ))

    return state
```

这仍然是教学代码，但已经把几个关键语义显式化：

```text
Run Status
Step Count
Final vs Tool Call
Tool Lookup Failure
Tool Call ID
Observation Feedback
```

---

# 5. 为什么 Tool Call 必须有 call_id

假设同一轮模型发两个 Tool：

```text
call_1 → read_file("a.py")
call_2 → read_file("b.py")
```

结果回来时需要知道：

```text
哪个 result 对应哪个 request？
```

所以需要 correlation：

```text
ToolCall.call_id
        ↕
ToolResult.call_id
```

尤其并行执行时更重要。

如果只按“消息顺序”匹配，重试、并发、Streaming 后很容易错位。

---

# 6. 一轮 Loop 到底发生什么

可以拆成八步：

```text
1. Load Runtime State
2. Assemble Context
3. Call Model
4. Normalize Model Output
5. Decide Final / Tool / Delegate / Pause
6. Execute Runtime Action
7. Persist Event / State
8. Decide Continue / Stop
```

其中第 7 步非常关键。

如果你：

```text
执行 Tool
→ 还没记录状态
→ 进程崩溃
```

Resume 时就会出现重复执行问题。

后面的 Checkpoint / Idempotency 会专门解决。

---

# 7. Agent Loop 不等于 Chain

Chain：

```text
A → B → C
```

Loop：

```text
Model
  ↓
Action
  ↓
Observation
  └────→ Model
```

Chain 的下一步是预先固定的。

Agent Loop 的下一步由当前 Observation 影响。

这也是 Agent 产生灵活性的来源，同时也是不确定性的来源。

---

# 8. ReAct 为什么适合作为入门模型

ReAct 经典结构：

```text
Reason
→ Act
→ Observe
→ Reason
→ Act
→ Observe
```

它帮助我们理解：

> Agent 不是一次生成完整方案，而是在环境反馈中逐步调整。

但 Runtime 不需要暴露模型内部“思维文本”才能实现这个循环。

工程上真正需要记录的是：

```text
Decision / Action
Tool Call
Observation
State Transition
```

而不是依赖模型输出一大段可见 Chain-of-Thought。

原始论文：

https://arxiv.org/abs/2210.03629

---

# 9. Loop 的 Action 不只有 Tool

一个成熟 Runtime 的模型决策可能是：

```text
Final
ToolCall
Delegate
AskUser
RequestApproval
Wait
Replan
```

因此内部可以统一抽象：

```python
class RuntimeAction:
    ...
```

例如：

```text
Model Decision
   ├─ ToolAction
   ├─ HandoffAction
   ├─ PauseAction
   └─ FinalAction
```

这样 Runtime 不会被“Tool Calling”绑死。

---

# 10. 为什么 Loop 需要显式 State

假设任务：

```text
修复 5 个测试失败
```

Runtime State 可以有：

```python
{
  "goal": "fix failing tests",
  "step": 8,
  "failed_tests": ["test_a", "test_b"],
  "modified_files": ["src/a.py"],
  "last_test_exit_code": 1,
  "status": "running"
}
```

而 messages 只是：

```text
过去发生过什么
```

如果只靠模型从 100 条历史里自己重新推断“当前做到哪”，会：

- 浪费 Token；
- 容易误读；
- 不利于恢复；
- 不利于程序检查。

所以 Loop 应围绕 Runtime State 推进。

---

# 11. Loop 的三个 Stop Layer

## 11.1 Model Stop

模型输出 Final。

但这只是：

> “模型认为可以结束。”

## 11.2 Runtime Guard

例如：

```text
max_steps
max_budget
max_wall_time
cancel_requested
```

即使模型还想继续，Runtime 也可以停止。

## 11.3 Outcome Verification

模型说：

```text
“测试已通过。”
```

Runtime / Eval 还要检查真实 Test Result。

因此：

```text
Model says Done
≠
Task is Proven Done
```

---

# 12. Tool 失败后 Loop 怎么继续

错误不应该全部变成 Python Exception 把整个 Run 崩掉。

可以先分类：

```text
Recoverable Tool Error
→ turn into structured observation
→ model may repair

Fatal Runtime Error
→ fail run
```

例如：

```json
{
  "ok": false,
  "error_type": "file_not_found",
  "message": "src/foo.py does not exist"
}
```

模型下一轮可能决定：

```text
先 search_file
```

这就是 Agent 相比固定 Chain 的价值。

但：

> Retry / Repair 也必须有限制，否则会进入重复失败 Loop。

---

# 13. 为什么每一步都要产生 Event

例如：

```text
RunStarted
ModelRequested
ModelCompleted
ToolCallProposed
ToolStarted
ToolCompleted
StateUpdated
RunCompleted
```

好处：

- Debug；
- Streaming；
- Persistence；
- Replay；
- Metrics；
- Eval。

后面的 Message / Event Model 章节会详细讲。

---

# 14. Dynamic Instruction 怎么进入 Loop

真实用户可能在 Agent 执行时说：

```text
“先别改 database.py，改成只修 API 层。”
```

Runtime 需要把这个新输入安全地进入后续 State / Context。

不能简单：

```text
正在执行的旧 Tool 当没发生
```

要考虑：

- 当前 Tool 是否 interruptible；
- cancel or block；
- 新 instruction 从哪个 step 生效；
- 已完成副作用是否保留；
- Trace 怎样记录。

这对应 `AGENT-042` Dynamic Instruction / Steering。

---

# 15. Claude Code 的 Loop 证据

固定源码：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`QueryEngine.ts` 明确把：

```text
conversation
turn
messages
tools
agents
MCP
permission
abort controller
usage / budget
```

放在同一个 Query Lifecycle 中。

它还引入 `query.ts` 作为更底层的查询/执行路径。

课程抽象不是说“Claude Code 就等于这个伪代码”，而是：

> **成熟产品确实需要一个长期存在、跨 Turn 持有状态并协调 Tool / Permission / Context 的执行对象。**

---

# 16. Codex 的 Loop 证据

固定源码：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

已确认：

- `Session`；
- `TurnContext`；
- `StepContext`；
- Tool Router / Executor；
- `EventMsg`；
- Compaction；
- Sandbox；
- Rollout Trace。

这说明 Loop 并不是一个孤立的 `while`，而是绑定：

```text
Session State
Turn Context
Tool Action
Events
Context Lifecycle
```

的 Runtime 状态机。

---

# 17. 一个真实 Coding Agent Loop

用户：

```text
“修复 users API 的 flaky test。”
```

可能执行：

```text
Step 1
Model → run_test
Tool → failure log

Step 2
Model → search_code("users")
Tool → file list

Step 3
Model → read_file("tests/test_users.py")
Tool → code

Step 4
Model → read_file("src/users.py")
Tool → code

Step 5
Model → apply_patch
Tool → patch result

Step 6
Model → run_test
Tool → still fails

Step 7
Model → inspect timing / retry
...

Step N
Model → final
Runtime → verify tests really pass
```

这里每一步都依赖上一轮 Observation。

这就是 Agent Loop。

---

# 18. Loop 的常见 Failure Mode

## 18.1 Dead Loop

```text
Tool A fail
→ model calls Tool A
→ fail
→ Tool A
→ ...
```

需要：

- repeated-action detection；
- retry budget；
- alternate route；
- stop condition。

## 18.2 Oscillation

```text
方案 A
→ 改成 B
→ 又改回 A
→ 又改成 B
```

## 18.3 Goal Drift

任务本来是：

```text
修 test
```

最后开始：

```text
重构整个项目
```

## 18.4 Tool Thrashing

不停搜索、读取，但不产生实质进展。

这些会在 Stop / Loop Guard 章节继续。

---

# 19. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Agent Loop 本质是 Model Decision → Runtime Action → Observation → 下一轮 Decision。Runtime 每轮从 State 组装 Context，调用 Model，解析 Final/Tool/Delegate 等 Action，执行 Tool 并把 Result 写回 State/Event，然后根据 Stop Condition 决定继续还是结束。Production 里还要加 max step、budget、permission、timeout、checkpoint、cancellation 和 outcome verification，不能只是 while True。

## Level 2｜2–3 分钟

可以再展开：

> 我会把 Loop 做成显式状态机。Run 有 status 和 step_count；每次 Step 先 build context，再 model generate；Tool Call 要有 call_id、schema validation 和 registry lookup；Tool Result 结构化回填。Recoverable Tool Error 可以变成 Observation 给模型修复，Fatal Error 才结束。Stop 不只看模型 Final，还要 Runtime Guard 和最终 Outcome Verification。

## Level 3｜继续追问

🔍 **模型说 Final 就一定结束吗？**  
不一定，要做 Runtime Guard 和 Outcome Verification。

🔍 **Tool Error 应该 raise 还是回填？**  
可恢复错误通常结构化回填；Runtime invariant broken 等不可恢复错误再 fail。

🔍 **如何避免死循环？**  
max step、重复 action 检测、retry budget、progress metric、fallback/stop。

---

# 20. HUMAN-A 真实追问链

Verified Chain 中反复出现：

```text
为什么 Agent
→ Harness
→ Agent Loop / Planning
→ Tool
→ Context / Memory
→ Failure / Evaluation
```

对应：

- `AGENT-003`：36 sources；
- `AGENT-005`：31 sources；
- `AGENT-006`：15 sources；
- `AGENT-020`：27 sources。

所以 Loop 不是孤立概念，而是后续所有 Runtime 能力的骨架。

---

# 21. 自测

<details><summary>1. 为什么 Agent Loop 不能只用 while True + tool_call？</summary>

因为 Production 需要显式状态、Step、Stop、Budget、Cancellation、Failure、Permission、Checkpoint、Trace、Outcome Verification。无限 while 既不可恢复，也不可审计。
</details>

<details><summary>2. Model Final 和 Task Success 有什么区别？</summary>

Model Final 只是模型声明不再请求动作；Task Success 需要 Runtime 根据业务 Outcome、Test、Artifact 或外部状态确认真的完成。
</details>

<details><summary>3. Tool Call 为什么需要 call_id？</summary>

用于把 Tool Result 与具体 Tool Request 关联，尤其在并发、重试和 Streaming 场景中，不能只靠消息顺序。
</details>

<details><summary>4. Recoverable Tool Error 为什么可以回填给模型？</summary>

因为 Agent 的价值之一就是根据 Observation 自我修正。例如 file_not_found 后模型可以先 search，而不是整个 Run 立即崩溃；但必须设置重试/循环上限。
</details>
