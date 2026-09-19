# 03. Agent Loop：Session、Run、Turn、Step 与执行事件

有了目标，工作并不会自己向前走。模型提议读文件、程序真的读到内容之后，还需要把结果送回去，让下一步随观察改变。

> 这条“判断—行动—观察—再判断”的反馈，才是我们要解释的执行循环。

[← 上一章](02-WorkflowAutonomyAndRuntimeBoundary.md) · [Agent 目录](../README.md) · [下一章 →](04-ToolContractAndValidation.md)

---

<a id="section-1"></a>

## 1. 先讲人话：Agent 的核心不是“会调用 Tool”，而是会循环推进任务

<a id="legacy-03-01"></a>

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

普通 LLM Call 到 `Model Output` 就结束；Agent Runtime（运行时执行系统） 还要解释：

```text
输出是不是 Tool Call？
要不要执行？
执行结果如何变成下一轮 Observation？
State 怎样更新？
什么时候结束？
```

因此 Loop 是 Harness 的控制骨架。

---

<a id="section-2"></a>

## 2. 一个最小可运行的 Agent Loop

<a id="legacy-03-02"></a>

下面是**标准库教学例子**：模型决定用固定函数模拟，不调用真实模型、不访问网络。目的只在于看清“观察回填以后，下一次决策才会改变”。

```python
# runnable-example: feedback_loop
# 只验证反馈与有限停止；不模拟生产授权、持久化或模型质量。
def decide(state):
    if not state['observations']:
        return {'kind': 'tool', 'name': 'read', 'doc': 'A'}
    return {'kind': 'final', 'text': state['observations'][-1]}

def run_report():
    state = {'goal': '读取A并交付内容', 'observations': []}
    documents = {'A': '发布日期待确认'}  # 已授权内存材料，替代真实文件
    for _ in range(3):                    # 明确上限，防止无限循环
        decision = decide(state)
        if decision['kind'] == 'tool':
            if decision['name'] != 'read' or decision['doc'] not in documents:
                raise ValueError('未知工具或未授权材料')
            # 结果不能只打印；后一次决策必须能读到它。
            state['observations'].append(documents[decision['doc']])
        elif decision['kind'] == 'final':
            # 本例只验证交付的是刚读取的内容，不证明任意报告语义正确。
            if state['observations'] and decision['text'] == state['observations'][-1]:
                return decision['text']
            raise ValueError('没有可核对的交付物')
        else:
            raise ValueError('未知决定类型')
    raise RuntimeError('预算耗尽，不等于成功')

assert run_report() == '发布日期待确认'
```

真实模型不是读取Python变量：程序还要把选中的观察编码成下一次请求。第09章解释状态怎样投影为上下文。

---

<a id="section-3"></a>

## 3. 为什么要分 Run / Turn / Step

<a id="legacy-03-03"></a>

为讲清故障发生在哪，本章先使用下列**自建运行时的工作约定**：Session 是连续会话，Run 是为一个目标启动的一次执行，Turn 是一次“模型决策—动作—观察”的循环轮次，Step 是其中的操作。用户输入称为“用户交互”，避免又叫同一种 Turn。

```text
Session：这个项目的持续会话
└─ Run：本次整理报告
   ├─ Turn 1：决定读 A → 读取 → 接收结果
   │  ├─ Step：模型请求
   │  └─ Step：工具调用与结果登记
   └─ Turn 2：发现日期冲突 → 读 B → 接收结果
```

这棵树让你能说“第二轮读取失败，但这次报告任务还可继续”，而不是所有问题都叫“会话失败”。**它不是全行业统一对象模型。** 业务的一次任务也可能暂停后继续同一 Run，或因用户明确要求从头做而创建新 Run；需项目自己定义。

### 对照产品语义，不强制一一对应

| 对象体系 | 含义 | 与教学树的关系 |
|---|---|---|
| Codex Thread | 持续对话容器 | 类似会话作用域 |
| Codex Turn | 用户输入发起的一段 Agent 工作，可含多次推理和工具交互 | 常覆盖教学例子中的整个执行段，而非单次模型调用 |
| Codex Item | 消息、工具行动等有类型项目 | 不是每条生命周期事件；一个 Item 可产生多个事件 |
| Claude Code 快照的 conversation / `submitMessage()` | 会话对象持有跨调用数据，提交消息推进交互 | 内部循环次数不应直接当用户 Turn 数 |

面试时先说“在我的实现里 Turn 指……”，再对照产品。清楚的自定义树可以帮助理解，但错误映射会让后面的取消与恢复范围混乱。

Run需要能关联目标、状态、起止时间、预算及当前进度。这些信息服务任务控制，而不是要求每个字段都永远保存。

---

<a id="section-4"></a>

## 4. 为什么这个分层对 Failure 很重要

<a id="legacy-03-04"></a>

假设：

```text
Run = 修复 issue #123
Turn = 检查修复结果的反馈轮
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

---

<a id="section-5"></a>

## 5. Runtime 不是只有 Message，还需要 Event

<a id="legacy-03-05"></a>

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

---

<a id="section-6"></a>

## 6. Event 为什么最好是结构化的

<a id="legacy-03-06"></a>

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

- Trace（执行追踪）；
- Replay（重放）；
- Debug；
- Metrics；
- Eval；
- Incident Analysis。

---

<a id="section-7"></a>

## 7. Correlation ID 为什么关键

<a id="legacy-03-07"></a>

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

ID回答“是哪一件事”，版本回答“采用哪份定义或内容”。模型call_id关联调用与结果；operation_id可标识同一逻辑动作；attempt_id区分重试尝试。不是每个ID都要有复杂版本树。

---

<a id="section-8"></a>

## 8. State Machine：Loop 不只是 while True

<a id="legacy-03-08"></a>

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

---

<a id="section-9"></a>

## 9. Runtime State 应该有什么

<a id="legacy-03-09"></a>

State（状态）不是“所有字段的名字”。在报告例子里，程序需要知道任务是否继续、哪些文件已读、正等待什么、预算是否够用。这些影响下一步的当前情况就是状态，Plan只是其中可能包含的一部分。

一个简化模型：

```python
# 状态示意：只保存会影响下一步选择的信息，不代表全部字段都要永久持久化。
from dataclasses import dataclass, field

@dataclass
class RunState:
    run_id: str  # 关联这一次任务执行
    goal: str
    status: str = "running"
    step_count: int = 0  # 已推进步数，用于限制与诊断
    last_tool_call_id: str | None = None
    artifacts: list[str] = field(default_factory=list)
    unresolved_errors: list[str] = field(default_factory=list)
```

这不是 Memory（记忆）。

它描述：

> **现在执行到哪里、已经发生了什么、接下来还能做什么。**

---

<a id="section-10"></a>

## 10. 新用户指令怎样进入正在运行的 Agent

<a id="legacy-03-10"></a>

这是 `AGENT-042` Dynamic Instruction / Steering 的核心。

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

模型当前已发出的请求不能被客户端从中间随意修改。新输入应先由应用接收，再由运行时决定何时生效。

| 新输入意图 | 可采用的行为 | 用户应该看到什么 |
|---|---|---|
| 新增无关任务 | 排队到当前任务结束后新建执行 | 已排队，而非假装立即处理 |
| 补充当前任务信息 | 放入待处理输入，在下一次安全决策点追加 | 已接收，后续将使用 |
| 修改约束，例如“不要写文件” | 更新约束；按风险中断或等待当前动作结束 | 明确已经发生的动作和生效边界 |
| 明确取消 | 停止派发新动作并传播取消 | 取消中与真正结束分开 |

“安全决策点”通常是一次模型/工具阶段完成、控制权回到运行时的时刻。若写入已经提交，新约束不能倒流时间撤销它。07章详细讲传播和迟到结果。

<details>
<summary>具体落点：Codex 的排队/steer 与 Claude Code 的循环输入</summary>

Codex App Server 对正在运行的 Turn 提供 `turn/steer`（追加引导输入），并用预期 Turn 标识避免把新输入送给已结束或被替换的一轮；`turn/interrupt`用于中断。固定源码的 `session/turn.rs`检查待处理输入，决定是否还有后续工作。这个接口语义不同于“开始第二个同时修改同一状态的执行”。

用户提供的 Claude Code 快照中，`query.ts`在工具调用完成后读取按优先级筛选的排队输入，将符合当前Agent范围的内容作为附件加入后续消息，避免把普通用户消息插进未完成的工具请求/结果之间。Slash命令不按普通文本在轮中取出，需走自己的命令处理入口；`Tool.ts`另外提供工具中断行为。官方工作过程也说明用户可随时中断以引导方向。但具体界面是否排队、立即打断，取决于入口和运行模式，不能承诺所有客户端完全一样。

</details>

---

<a id="section-11"></a>

## 11. Loop 什么时候继续，什么时候停止

<a id="legacy-03-13"></a>

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

---

<a id="section-12"></a>

## 12. 产品实现与官方资料对照（按需展开）

<details>
<summary>源码证据：Claude Code</summary>

<a id="legacy-03-11"></a>

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

</details>

<details>
<summary>源码证据：Codex</summary>

<a id="legacy-03-12"></a>

固定 Codex 快照中，Context Compaction（上下文压缩） 相关代码直接引用：

```text
Session
StepContext
TurnContext
WorldState
EventMsg
```

Tool Router（路由器） 中 `ToolCall` 也携带 `call_id`，再构造带 Session / StepContext / CancellationToken 的 Invocation（调用实例）。

这说明成熟 Runtime 会显式区分：

```text
长期 Session
→ 当前 Turn
→ 当前 Step / Invocation
→ Event / Tool Call
```

而不是把一切折叠成 Chat History（历史记录）。

产品对照不能把同名词硬套教学树：Codex公开交互以Thread/Turn/Item表达，一次Turn可含多次推理和工具交互；Item的开始、增量、完成可以形成多个事件。

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 13. HUMAN-A 信号

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

---

<a id="interview"></a>

## 14. 面试怎么答

### Q：怎样解释一个完整Agent Loop？

🎯 **30 秒回答**：

> Agent Loop 是 Goal 驱动的多步控制循环：Runtime 组装 Context，请模型决定 Final Answer、Tool 或 Delegate，执行动作后把 Observation（观察结果） 和 State Transition 记录下来，再进入下一轮。Production（生产环境） 里还要把 Session、Run、Turn、Step 分层，并用结构化 Event 和 correlation id 表达 Tool、Approval（批准）、Checkpoint（检查点）、Cancel 等事实，这样才能做恢复、Trace 和 Eval。

### Q：怎样描述一个最小 Agent Loop？

🎯 **30 秒回答**：

> 程序构造上下文并调用模型，分辨工具、澄清或完成候选。工具经过受控执行后形成观察，更新进展再请求下一次决策；完成候选经过任务验收后才能成功。循环还应有停止原因，不能把等待用户、预算耗尽和成功都当作同一种 done。

### Q：Session、Run、Turn、Step 怎么区分？

🎯 **30 秒回答**：

> 我会先声明项目定义：Session 是会话，Run 是一次目标执行，Turn 可定义成一次决策反馈周期，Step 是内部操作。但 Codex 的 Turn 是一次用户请求及后续工作，可含多次模型调用，并使用 Item 表示类型化项目。应映射职责，不强制给所有产品套同一棵树。

### Q：Agent 运行中用户追加消息，能直接修改当前模型输入吗？

🎯 **30 秒回答**：

> 已发送请求通常不能原地插入。应用先接收输入，区分新任务、补充、约束变更或取消，再排队、在下一决策点追加，或中断。需要绑定目标执行身份，防止误送；已发生的副作用不会因为新消息自动撤销。

### Q：Message 和 Event 的区别为什么重要？

🎯 **30 秒回答**：

> 模型消息表达输入输出内容；运行事件还包括排队、授权、执行开始和检查点等程序事实。一个工具调用可能对应多个事件。用调用标识关联并发结果，而不是依赖文本或时间顺序；诊断事件也不必全部加入模型上下文。

### 🔍 继续追问与下一步

```text
Tool Contract 为什么必须独立设计？
Tool Schema 谁校验？
并发 Tool Call 怎样相关联？
Step Failure 和 Run Failure 怎样区分？
怎样用 Event Log 做 Replay？
```

下一章正式进入 Tool Runtime。

---

<a id="pitfalls"></a>

## 15. 高频易错点

⚠️ 把 Run / Session / Message 全叫 Memory；

⚠️ 把 Chat History 当作 Runtime State；

⚠️ Tool Result 没有 call id；

⚠️ 只有字符串日志，没有结构化 Event；

⚠️ `while True` 没有 Stop / Budget（预算） / Cancel；

⚠️ Agent 说完成就直接标记 Run Completed。

⚠️ **Turn 在所有产品里都等于一次模型调用。** 必须查看产品定义；Codex Turn可含多次推理与工具交互。

⚠️ **新消息总应立即打断所有动作。** 先识别意图和当前动作是否可安全中断。

⚠️ **循环 return 就是业务成功。** 可能等待、取消、耗尽预算；要有明确终态及验收。

⚠️ **事件越多，模型越懂运行过程。** 很多事件服务程序或排障，全部喂模型会制造噪声。

---

<a id="self-test"></a>

## 16. 本章自测

<details><summary>1. 为什么 Tool Result 不是普通 Assistant Message？</summary>

因为它有明确的 Tool Call 来源、call_id、执行状态和 Runtime 语义，需要与具体 Invocation 相关联；模型可见表示只是其中一个 projection。

</details>

<details><summary>2. 为什么 Run / Step 分层对重试很重要？</summary>

因为一个 Step 的可恢复失败不应自动把整个 Run 判死。Runtime 需要知道失败发生在哪一层，才能决定 Retry（重试）、Repair、Fallback（备用或降级路径） 或终止。

</details>

<details><summary>3. Runtime Event 与 Message 最大区别是什么？</summary>

Message 主要服务模型输入输出；Event 记录系统真实发生的执行事实，包含很多模型不必看见但恢复、审计、指标和 Replay 必须知道的信息。

</details>

<details><summary>4. 一次 Codex Turn 可否读取文件三次？</summary>

可以。Turn 包含用户请求后的一段 Agent 工作，模型可多次请求工具。每个工具项目及其事件有各自身份；不能把三次调用解释成必然三个 Codex Turn。

</details>

<details><summary>5. 两次读取先后反转返回，会混吗？</summary>

正确协议用调用标识匹配请求和结果，不靠返回顺序。若只按时间追加两段无标识文本，模型可能误以为 B 的结果属于 A。

</details>

<details><summary>6. 用户说“稍后再检查 D”，必须取消正在读 A 吗？</summary>

不必。若不改变当前安全边界，可以排队到合适的决策点。应用应明确接收与执行的差别，而不是让用户以为新任务已立即开始。

</details>

<details><summary>7. 用户说“别发送报告”，但发送已成功，应怎样显示？</summary>

停止后续发送，核对既有回执，并告知已发送这一事实；不能只显示已取消就暗示发送被撤回。是否有撤回或补救能力由外部系统决定。

</details>

<details><summary>8. 一次参数错误使 Step 失败，Run 一定失败吗？</summary>

不一定。可纠正错误能在预算内反馈后继续；不应重启整段任务或丢失已有进展。安全拒绝与系统损坏则有不同控制策略。

</details>

<details><summary>9. 需要保存模型的全部隐藏推理才能理解循环吗？</summary>

不需要，也不能假设能取得。应记录必要的可观察输入、候选动作、实际执行结果和停止原因，用它们解释程序路径。

</details>

---

[← 上一章](02-WorkflowAutonomyAndRuntimeBoundary.md) · [Agent 目录](../README.md) · [下一章 →](04-ToolContractAndValidation.md)
