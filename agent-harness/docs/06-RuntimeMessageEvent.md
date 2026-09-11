# 06. Runtime Message / Event Model：模型看到什么，系统记录什么

`AGENT-004` 在冻结 HUMAN-A 中有 **8 个独立来源**；`AGENT-043` Execution Trace 还有 **7 个独立来源**。

这个问题看起来不如 Context Compaction 高频，但它是很多 Production 能力的底层：

```text
Streaming
Trace
Replay
Checkpoint
Tool Correlation
Approval
Evaluation
Multi-Agent
```

如果 Message / Event Model 一开始就设计错，后面会不断补丁。

---

# 1. 先讲人话：Message 和 Event 不是一回事

模型上下文里可能只有：

```text
User Message
Assistant Message
Tool Call
Tool Result
```

但 Runtime 真实发生的事情更多：

```text
RunStarted
TurnStarted
ModelRequestStarted
ModelTokenDelta
ModelCompleted
ToolCallProposed
ApprovalRequested
ApprovalGranted
ToolStarted
ToolProgress
ToolCompleted
CheckpointSaved
CompactionStarted
CompactionCompleted
RunCompleted
```

因此：

> **Model-visible Message 是 Runtime Event 的一个投影，不是全部事实。**

这是本章最重要的结论。

---

# 2. 为什么不能把所有 Event 都塞进 messages[]

假设 Tool 执行进度：

```text
download 10%
download 20%
download 30%
...
```

UI 需要显示。

Trace 也可能需要记录。

但模型下一轮 Context 不一定需要 100 条 Progress Message。

如果全塞进去：

```text
Context Noise ↑
Token Cost ↑
Model attention 被稀释
```

所以可以分层：

```text
Runtime Event Log = 完整执行事实
Model Projection   = 本轮真正需要给模型看的部分
UI Projection      = 用户界面需要展示的部分
Eval Projection    = 评测需要的证据
```

---

# 3. 最小 Message 类型

可以先定义：

```python
from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class UserMessage:
    content: str


@dataclass
class AssistantMessage:
    content: str


@dataclass
class ToolCallMessage:
    call_id: str
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class ToolResultMessage:
    call_id: str
    ok: bool
    result: Any
```

关键点：

```text
ToolCall.call_id
↕
ToolResult.call_id
```

这保证请求和结果可以稳定关联。

---

# 4. Runtime Event 要比 Message 更丰富

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RuntimeEvent:
    event_id: str
    run_id: str
    turn_id: str
    step_id: str | None
    type: str
    timestamp: datetime
    payload: dict[str, Any]
```

例如：

```json
{
  "event_id": "evt_1008",
  "run_id": "run_123",
  "turn_id": "turn_4",
  "step_id": "step_9",
  "type": "tool_completed",
  "payload": {
    "call_id": "call_88",
    "tool": "run_test",
    "exit_code": 1,
    "duration_ms": 18342
  }
}
```

这个 Event 可以服务：

- UI；
- Trace；
- Replay；
- Metrics；
- Eval；
- Audit。

---

# 5. Event 为什么应该是 Append，而不是反复覆盖

假设只保存当前状态：

```json
{
  "status": "running",
  "last_tool": "run_test"
}
```

你不知道：

```text
之前发生了什么？
为什么变成这个状态？
Tool 重试了几次？
哪个 Approval 导致执行？
```

如果有 Event Log：

```text
RunStarted
→ ModelCompleted
→ ToolCallProposed
→ ApprovalRequested
→ ApprovalGranted
→ ToolStarted
→ ToolCompleted
→ StateUpdated
```

就可以重建轨迹。

这不意味着一定要做严格 Event Sourcing，但“append-only execution evidence”是非常有价值的思想。

---

# 6. State 和 Event 的区别

```text
Event = 发生了什么
State = 现在是什么状态
```

例如：

```text
Event:
ApprovalGranted(call_88)

State:
approved_calls contains call_88
```

再比如：

```text
Event:
ToolCompleted(exit_code=0)

State:
last_test_passed = True
```

通常：

```text
Event Log
→ reducer / state transition
→ Current State
```

---

# 7. Model Context 是 Event 的 Projection

假设真实 Event：

```text
ToolStarted
ToolProgress 10%
ToolProgress 20%
ToolProgress 30%
ToolCompleted
```

给模型的 Context 可能只需要：

```text
Tool Result: completed, output=...
```

这叫 Projection。

因此可以设计：

```python
def event_to_model_message(event: RuntimeEvent):
    if event.type == "tool_completed":
        return make_tool_result_message(event)

    if event.type in {
        "tool_progress",
        "checkpoint_saved",
        "metrics_emitted",
    }:
        return None
```

这样 Runtime 的可观测性不会直接污染 Context。

---

# 8. UI Event 也不一定等于 Model Message

用户界面可能希望显示：

```text
正在搜索仓库...
找到 18 个文件
正在运行测试...
测试失败，继续修复...
```

这些是产品体验。

但如果每一条都当 System Message 塞给模型，模型会看到大量 UI 文本。

因此：

> **UI Representation 和 Model Context 要解耦。**

Claude Code `ToolUseContext` 中甚至有 UI-only system message 相关注释，强调某类消息会在 normalize-to-API 边界被剥离。这正是这种边界的产品实现例子。

---

# 9. Error 也应该是结构化 Event

坏设计：

```text
"something went wrong"
```

更好的：

```json
{
  "type": "tool_failed",
  "error_type": "timeout",
  "retryable": true,
  "tool": "web_search",
  "call_id": "call_9",
  "attempt": 2,
  "message": "deadline exceeded"
}
```

Runtime 可以基于字段决定：

```text
retry
fallback
return observation to model
fail run
```

而不是解析错误字符串。

---

# 10. Streaming Event 怎么设计

模型流式输出时，可能产生：

```text
ModelStarted
TextDelta
TextDelta
ToolCallDelta
ModelCompleted
```

Tool 也可能：

```text
ToolStarted
ToolProgress
ToolProgress
ToolCompleted
```

客户端连接断开时：

```text
Runtime 不应该因为 SSE 断开就丢失 Run State
```

这就是：

```text
Execution lifecycle
≠ Client transport lifecycle
```

SSE / WebSocket 的通用 transport 原理属于 AI Backend Engineering，但 Agent Runtime 必须定义“要流哪些 Event”。

---

# 11. Correlation ID 是核心

至少常见：

```text
run_id
turn_id
step_id
request_id
call_id
agent_id
parent_run_id
```

例如 Multi-Agent：

```text
run_parent
├─ agent_A / child_run_1
│  └─ call_1
└─ agent_B / child_run_2
   └─ call_2
```

没有这些 ID：

- Tool Result 对不上；
- Trace 无法聚合；
- Subagent 难以关联；
- Replay 困难。

---

# 12. Event Version 为什么要考虑

Agent Runtime 会升级。

今天：

```json
{"type":"tool_completed","output":"..."}
```

以后可能变成：

```json
{
  "type":"tool_completed",
  "version":2,
  "result":{"text":"..."},
  "metadata":{}
}
```

如果要持久化长期 Run/Trace，最好考虑：

- schema version；
- backward compatibility；
- migration；
- unknown event handling。

否则旧 Session 很难 Resume。

---

# 13. Event Log 与 Checkpoint 的关系

两个常见策略：

## 13.1 全量 Replay

```text
从 RunStarted replay 所有 Event
→ 重建 State
```

优点：完整。

缺点：长任务成本高。

## 13.2 Snapshot + Tail Events

```text
Checkpoint Snapshot at event 500
+ replay event 501...
```

这更常见于长任务。

后面 Checkpoint 章节会深入。

---

# 14. Event 与 Trace 的区别

可以把：

```text
Event = 业务/运行时发生的离散事实
Trace = 把这些事实按执行层次组织起来的观察结构
```

例如：

```text
Trace
└─ Turn Span
   ├─ Model Span
   ├─ Tool Span
   └─ Verification Span
```

底层可能引用同一批 Event / IDs。

---

# 15. Codex Rollout Trace 的启发

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/rollout-trace/README.md` 区分了：

- raw payloads：exact evidence；
- ConversationItem：模型实际看到什么；
- ToolCall：Runtime Tool Boundary；
- CodeCell / TerminalOperation；
- InteractionEdge：information flow。

这是一个很好的提醒：

> Production Trace 不应该只有“日志字符串”，而应该能回答模型看到了什么、调用了什么、环境发生了什么、信息怎样流动。

---

# 16. Claude Code Message Model 的启发

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`Tool.ts` 的 `ToolUseContext` 直接涉及：

- `AssistantMessage`；
- `UserMessage`；
- `SystemMessage`；
- `ProgressMessage`；
- Tool progress；
- MCP progress；
- Agent progress；
- Hook progress。

同时还区分 UI-only message 与 API normalize boundary。

这说明成熟产品确实需要：

```text
Model Message
UI Message
Runtime Progress
Tool Result
```

等不同语义。

---

# 17. 一个 Event-driven Runtime 示例

```python
async def execute_step(state, event_bus):
    await event_bus.emit("step_started", state.ids())

    context = build_context(state)

    await event_bus.emit("model_request_started", state.ids())
    decision = await model.generate(context)
    await event_bus.emit(
        "model_completed",
        {**state.ids(), "decision_type": decision.kind},
    )

    if decision.kind == "tool_call":
        await event_bus.emit(
            "tool_started",
            {**state.ids(), "call_id": decision.call_id},
        )

        result = await execute_tool(decision)

        await event_bus.emit(
            "tool_completed",
            {
                **state.ids(),
                "call_id": decision.call_id,
                "ok": result.ok,
            },
        )
```

真实系统还要做：

- durable append；
- order；
- idempotent consumer；
- schema version；
- privacy / redaction。

---

# 18. 安全：Trace 不是越详细越好

Event 可能包含：

- User Data；
- Prompt；
- Tool Arguments；
- Secret；
- File Content；
- PII。

所以 Observability 还需要：

```text
Redaction
Access Control
Retention
Tenant Isolation
Secret Filtering
```

不能为了 Debug 把所有 Secret 永久写日志。

---

# 19. Evaluation 为什么依赖 Event Model

假设 Agent 最终失败。

你想知道：

```text
是检索错了？
Tool 选错了？
参数错了？
Tool 失败了？
Context 丢了？
模型误判 Done？
```

如果只有 Final Answer，无法归因。

有 Step/Event Trace 后，可以做：

```text
Tool Selection Accuracy
Tool Argument Accuracy
Retry Count
Latency Breakdown
Context Token Usage
Outcome Success
```

所以 Event Model 是 Eval Harness 的数据基础。

---

# 20. 高频易错点

⚠️ **messages[] = 完整 Runtime History**  
不对。Runtime Event 比模型 Message 更丰富。

⚠️ **UI Progress 要全部塞给模型**  
不需要，应该做不同 Projection。

⚠️ **错误只存 message 字符串**  
应该结构化 error_type、retryable、call_id 等。

⚠️ **Trace 只要 print log**  
复杂 Agent 需要 run/turn/step/tool 层级和关联 ID。

⚠️ **记录越多越安全**  
Trace 可能泄露敏感数据，必须做 redaction 和 access control。

---

# 21. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> 我会区分 Model-visible Message 和 Runtime Event。Message 是本轮模型需要看到的 User/Assistant/Tool Call/Tool Result；Event 则记录完整执行事实，例如 Run/Step、Tool Progress、Approval、Checkpoint、Compaction。Runtime Event 可以投影成模型 Context、UI Streaming、Trace 和 Eval 数据。这样既保留可追踪性，又不会把所有运行时噪声塞进 Context。

## Level 2｜2–3 分钟

> Event 我会至少带 event_id、run_id、turn_id、step_id、timestamp 和 payload；Tool Call/Result 用 call_id 关联。State 是当前状态，Event 是发生过的事实。长任务可以用 Checkpoint Snapshot + Tail Event 恢复。Trace 按 Turn/Model/Tool Span 组织。Error 也结构化，不能只存字符串。最后要做 schema version、redaction 和 tenant isolation。

## Level 3｜继续追问

🔍 **Event Sourcing 是必须的吗？**  
不是。课程强调 append-only evidence 与 projection 思想，不要求所有系统严格采用 Event Sourcing。

🔍 **为什么 Tool Progress 不一定进 Model Context？**  
它对 UI/Trace 有价值，但对下一轮决策可能是噪声。

🔍 **Replay 时为什么需要版本？**  
旧 Event Schema 可能和新 Runtime 不兼容，需要 schema version / migration。

---

# 22. 本章证据

## HUMAN-A

- `AGENT-004` Message / Event Model：8 sources；
- `AGENT-043` Execution Trace / Observability：7 sources。

## Claude Code

- `Tool.ts`
- message / progress types
- `ToolUseContext`

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

## OpenAI Codex

- protocol `EventMsg`
- `TurnItem`
- `codex-rs/rollout-trace/README.md`

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

## 官方资料

OpenAI Agents SDK Tracing：

https://openai.github.io/openai-agents-js/guides/tracing/

---

# 23. 自测

<details><summary>1. Message 和 Event 最核心的区别是什么？</summary>

Message 是模型交互语义的一部分；Event 是 Runtime 发生的完整执行事实。Event 可以投影为 Message，但不是所有 Event 都应该进入模型 Context。
</details>

<details><summary>2. 为什么 Tool Call/Result 要用 call_id？</summary>

为了在并发、重试、流式执行中稳定关联请求和结果，不能依赖数组顺序。
</details>

<details><summary>3. State 和 Event 有什么区别？</summary>

Event 表示“发生了什么”，State 表示“现在是什么”。State 可以由 Event reducer 计算，也可以通过 Snapshot + Event Tail 恢复。
</details>

<details><summary>4. 为什么完整 Trace 不应该全部进入模型 Context？</summary>

Trace 面向 Debug/Eval/Audit，需要保留很多运行时细节；模型 Context 有有限 Token Budget，只应选取与下一步决策有关的信息，否则会增加成本和噪声。
</details>
