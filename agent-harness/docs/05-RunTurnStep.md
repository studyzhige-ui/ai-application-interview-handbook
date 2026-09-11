# 05. Run / Turn / Step：把 Agent 执行拆成可管理的状态机

很多 Agent 项目一开始只有一个模糊词：

```text
session
```

然后把：

- 用户会话；
- 一次任务；
- 一轮输入；
- 一次模型调用；
- 一次 Tool Call；

全部都塞进同一个概念。

短 Demo 还能跑，一旦需要 Trace、Resume、Retry、Streaming、Multi-Agent，就会开始混乱。

这一章建立一个稳定的执行层次：

```text
Session / Conversation
└─ Run
   └─ Turn
      └─ Step
         └─ Model Call / Tool Interaction
```

不同产品命名可能不同，但**执行层级必须清楚**。

---

# 1. 先讲人话

假设你和 Coding Agent 对话：

```text
你：修复登录 Bug
Agent：开始读代码、修改、测试……
Agent：完成

你：顺便把相关测试补一下
Agent：继续工作……
```

可以理解成：

```text
Conversation / Session
├─ Turn 1：修复登录 Bug
│   ├─ Step 1：Model → search
│   ├─ Step 2：Model → read
│   ├─ Step 3：Model → patch
│   └─ Step 4：Model → test
│
└─ Turn 2：补测试
    ├─ Step 1
    └─ Step 2
```

如果这是一个后台长任务，还可以再包一层 `Run`：

```text
Run = 一次有明确生命周期、可成功/失败/暂停/取消的执行实例
```

---

# 2. 为什么需要分层

因为不同层的生命周期不同。

例如：

```text
一次 Model API Retry
```

不应该变成：

```text
新的用户 Turn
```

一次 Tool Call Timeout：

```text
可以在当前 Step 内重试
```

用户又发了一条新消息：

```text
可能形成新 Turn，或 Steering 当前 Run
```

服务进程崩溃：

```text
Run 仍然应该能 Resume
```

如果不区分层级，所有 retry/resume/trace 都会失去语义。

---

# 3. Session / Conversation

Session 表示一个较长期的交互容器。

典型包含：

```text
session_id
user / tenant
conversation metadata
history reference
memory reference
created_at
last_active_at
```

它可以跨多个 Turn。

例如：

```text
Session S1
├─ “帮我看这个仓库”
├─ “刚才那个 Bug 再解释一下”
└─ “把测试也补了”
```

⚠️ Session 不等于 Memory。

Session 是交互生命周期；Memory 是未来可召回的信息。

---

# 4. Run

本课程用 `Run` 表示：

> **一次可以被启动、暂停、恢复、成功、失败或取消的任务执行实例。**

例如：

```text
run_id = run_123
status = running
started_at = ...
current_turn = turn_7
budget = ...
```

Run 很适合承载：

- status；
- budget；
- checkpoint version；
- cancellation；
- approval；
- external side effects；
- final outcome。

一个 Session 可以有多个 Run，也可以一个 Run 跨多个 Turn。

具体产品可以不同，但要把“长期交互”和“一次执行实例”分清。

---

# 5. Turn

Turn 通常对应一轮用户输入推动的交互周期。

```text
User Input
→ Agent executes zero or more steps
→ Agent produces response / pause / result
```

例如：

```text
Turn 8
user: “不要改数据库层”
```

Runtime 需要知道：

- 这个输入属于哪个 Session；
- 影响哪个 Run；
- 在哪个执行阶段进入；
- 是否需要取消当前 Tool。

Turn 是非常重要的 Context / Trace 边界。

---

# 6. Step

Step 是 Agent Loop 中一次较小的状态推进。

一个 Step 可能包含：

```text
Build Context
→ Model Request
→ Model Decision
→ Tool Call
→ Tool Result
→ State Transition
```

也可以把 Model Request 和 Tool Interaction 再拆得更细。

关键不是唯一命名，而是：

> **每个 Step 必须能被标识、追踪和解释。**

---

# 7. 为什么“Model Call”不能等同于 Step

假设模型请求失败：

```text
API 500
→ retry #1
→ retry #2
→ success
```

业务语义上可能仍然只是：

```text
Step 5
```

如果把每次 Provider Retry 都算成新 Step：

- progress metric 会虚高；
- trace 不好看；
- max step 容易误触发。

所以要区分：

```text
Semantic Step
vs
Infrastructure Attempt
```

同理：

```text
Tool Retry Attempt
```

也不一定是一个新的 Agent Decision Step。

---

# 8. 一个状态模型

```python
from dataclasses import dataclass
from enum import Enum


class RunStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    WAITING_USER = "waiting_user"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RunState:
    run_id: str
    session_id: str
    status: RunStatus
    turn_no: int
    step_no: int
    checkpoint_version: int
    cancel_requested: bool = False
```

状态转移：

```text
queued
  ↓
running
  ├─→ waiting_approval ──→ running
  ├─→ waiting_user ─────→ running
  ├─→ succeeded
  ├─→ failed
  └─→ cancelled
```

这比：

```python
is_running = True
```

更能表达真实 Agent 生命周期。

---

# 9. 为什么 Approval 应该是 Run State

假设 Agent 想：

```text
send_email(to="customer@...")
```

Runtime 不能阻塞一个进程等用户点按钮几小时。

更合理：

```text
Run Status = WAITING_APPROVAL
↓
serialize state
↓
worker release
↓
用户批准
↓
Run resume
```

这说明 HITL 并不是“弹一个确认框”这么简单，而是：

> **Run 的可持久暂停状态。**

OpenAI Agents SDK 的 HITL 文档明确支持 interruption + serializable `RunState` + resume，这个设计非常适合帮助理解这种状态语义。

来源：

https://openai.github.io/openai-agents-python/human_in_the_loop/

---

# 10. Turn 与 Dynamic Steering

用户可能在当前 Run 正在执行时追加：

```text
“先停一下，不要再改配置文件。”
```

Runtime 需要判断：

```text
当前 Tool 是 cancel 还是 block？
新消息立即生效还是下一 Step？
已经完成的副作用怎么办？
```

因此：

```text
User Message
≠ 一定等当前 Run 彻底结束后才处理
```

但必须有明确的 Turn / Event 语义。

Claude Code `Tool.ts` 的 `interruptBehavior(): cancel | block` 就展示了 Tool 层面需要明确这种行为。

---

# 11. Step ID 为什么必须稳定

Trace 中最好有：

```text
run_id
turn_id
step_id
model_request_id
tool_call_id
```

例如：

```text
run_123
└─ turn_4
   └─ step_9
      ├─ model_req_21
      └─ tool_call_88
```

这样定位问题时可以问：

```text
“run_123 的 turn_4 step_9 为什么 18 秒？”
```

而不是在日志里搜自然语言。

---

# 12. Checkpoint 应该在哪个层级发生

不是每次 token 都 checkpoint。

常见安全点：

```text
Turn Boundary
Tool Completed
External Side Effect Committed
Compaction Completed
Approval State Changed
```

具体取决于：

- 恢复成本；
- 写入成本；
- 副作用风险；
- 任务长度。

Checkpoint 章节会详细讲。

---

# 13. Session History 与 Run State 不要混在一个 JSON

坏设计：

```json
{
  "session": {
    "everything": "... massive blob ..."
  }
}
```

更好的逻辑分层：

```text
Session Metadata
Conversation History
Run State
Runtime Event Log
Memory Store
Artifacts
```

它们可以物理存同一个数据库，但语义上要分开。

原因：

- 生命周期不同；
- 查询方式不同；
- 版本化不同；
- Context 选择不同；
- 权限不同。

---

# 14. Claude Code 的证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`QueryEngine.ts` 的注释明确说明：

```text
One QueryEngine per conversation.
Each submitMessage() starts a new turn.
State persists across turns.
```

这直接支持：

```text
Conversation Runtime
→ multiple Turns
→ persistent state
```

`Task.ts` 还定义了 Task Status：

```text
pending
running
completed
failed
killed
```

说明后台任务本身也需要显式状态机。

---

# 15. Codex 的证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/core/src/compact.rs` 直接引用：

- `Session`；
- `StepContext`；
- `TurnContext`；
- `WorldState`；
- `EventMsg`。

这并不意味着我们的命名必须和 Codex 完全一致，但非常清楚地说明：

> **成熟 Agent Runtime 会区分不同生命周期的 Context / State 对象。**

固定 commit 本身的提交说明还讨论了：

- warm resume；
- cold resume；
- live fork；
- subagent inheritance。

这些都依赖“执行层次”清楚。

---

# 16. 一个 Trace 示例

```json
{
  "run_id": "run_123",
  "turn_id": "turn_4",
  "step_id": "step_9",
  "event": "tool_completed",
  "tool_call_id": "call_88",
  "tool": "run_test",
  "duration_ms": 18342,
  "success": false
}
```

如果后面发生：

```text
Step 10 → model sees failure
Step 11 → apply patch
Step 12 → test pass
```

我们就能完整重建执行轨迹。

这也是 Eval / Replay 的基础。

---

# 17. 多 Agent 时层级更重要

例如：

```text
Parent Run
├─ Subagent A Run
│  └─ turns / steps
└─ Subagent B Run
   └─ turns / steps
```

需要知道：

- child_run_id；
- parent_run_id；
- task ownership；
- budget inheritance；
- cancellation propagation；
- context inheritance。

如果只有一个全局 `messages[]`，Multi-Agent 很快会失控。

---

# 18. 面试易错点

⚠️ **Session = Memory**  
Session 是交互/生命周期容器，Memory 是可召回信息。

⚠️ **Turn = Model Call**  
一个 Turn 可能包含多个 Model/Tool Step。

⚠️ **Step = Retry Attempt**  
Provider Retry 是基础设施 attempt，不一定是新的语义 Step。

⚠️ **Run 状态只需要 running/done**  
真实系统还需要 waiting approval、waiting user、failed、cancelled 等。

⚠️ **所有 State 放 messages**  
会破坏恢复、校验、并发和审计。

---

# 19. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> 我会把 Agent 执行分成 Session/Conversation、Run、Turn、Step。Session 是长期交互容器；Run 是一次有状态生命周期的任务执行；Turn 通常由一轮用户输入触发；Step 是 Loop 中一次语义状态推进。这样 Retry、Approval、Checkpoint、Cancellation、Trace 和 Multi-Agent 才有清楚的作用域，不能把它们全部叫 session。

## Level 2｜2–3 分钟

> 比如一个 Turn 里模型可能连续 search、read、patch、test，这些是多个 Step；一次 Model API 500 重试两次仍可能属于同一个 Step。Run 可以从 running 进入 waiting_approval，持久化后释放 worker，用户批准再 resume。Trace 用 run_id/turn_id/step_id/tool_call_id 做关联。这样 crash/replay/eval 才能知道究竟在哪一层发生了什么。

## Level 3｜继续追问

🔍 **一个 Session 可以有多个 Run 吗？**  
可以，具体取决于产品语义；关键是长期交互和一次任务执行不要混为一谈。

🔍 **Approval 为什么是状态而不是同步阻塞？**  
因为等待可能很长，应该 durable pause / resume，而不是占住 worker。

🔍 **Retry 要不要增加 step_no？**  
如果只是同一语义动作的基础设施重试，通常不应该；如果模型基于错误重新决策，则是新 Step。

---

# 20. 自测

<details><summary>1. Turn 和 Step 的区别是什么？</summary>

Turn 通常表示一轮用户输入推动的交互周期，一个 Turn 内可以包含多个 Model/Tool Step；Step 是 Loop 中较小的一次语义状态推进。
</details>

<details><summary>2. 为什么 Run 需要 WAITING_APPROVAL？</summary>

高风险动作可能等待用户很久。Runtime 应把状态持久化并释放计算资源，审批完成后从同一 RunState Resume，而不是同步阻塞进程。
</details>

<details><summary>3. Provider Retry 为什么不一定是新 Step？</summary>

因为它可能只是同一语义动作的基础设施 attempt。把它算成新 Step 会污染 progress、max-step 和 trace 语义。
</details>

<details><summary>4. 为什么要有 run_id / turn_id / step_id / tool_call_id 多级 ID？</summary>

为了在并发、重试、Streaming、Subagent、Replay 中准确关联事件和结果，明确问题发生在哪个生命周期层级。
</details>
