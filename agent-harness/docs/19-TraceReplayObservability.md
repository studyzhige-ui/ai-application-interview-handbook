# 19. Trace、Replay 与 Observability

Agent 出问题时，如果你只有：

```text
request failed
```

几乎没有办法定位。

因为一次 Agent Run 可能经历：

```text
Context Assembly
→ Model Call
→ Tool Selection
→ Permission
→ Tool Execution
→ Tool Result
→ State Transition
→ Compaction
→ Model Call
→ Subagent
→ Final Answer
```

所以 Production Agent 需要的不只是普通日志，而是：

> **能重建“模型看见了什么、决定了什么、Runtime 执行了什么、状态如何变化”的结构化执行轨迹。**

---

## 1. Log、Metric、Trace 各解决什么

### Log

```text
某个时刻发生了什么
```

例如：

```text
provider timeout
permission denied
```

### Metric

```text
整体系统趋势
```

例如：

```text
agent_success_rate
p95_tool_latency
context_compaction_rate
```

### Trace

```text
一次 Run 的因果执行链
```

例如：

```text
Run
└─ Turn
   ├─ Context Build
   ├─ Model Call
   ├─ Tool Call
   │  └─ Tool Execution
   └─ State Update
```

三者互补。

---

# 2. Trace Identity

建议保持层级 ID：

```text
session_id
run_id
turn_id
step_id
model_call_id
tool_call_id
subagent_run_id
```

以及：

```text
parent_span_id
correlation_id
```

这样才能把：

```text
Tool Result
```

准确连回：

```text
哪次 Tool Call
```

而不是靠字符串搜索。

---

# 3. 一个 Agent Span 应该记录什么

不同 Span 类型字段不同。

## Model Span

```text
model/provider
input token count
output token count
latency
finish reason
context generation
selected tools
cost
```

## Tool Span

```text
tool name
argument fingerprint
permission decision
start/end
result status
external ref
side-effect class
```

## Context Span

```text
context source counts
selected tokens
compaction generation
cache hit
memory/retrieval refs
```

## State Span

```text
from_status
to_status
state_version
checkpoint_id
```

---

# 4. Codex Rollout Trace 的源码证据

固定 Codex Source Index 中 `codex-rs/rollout-trace/README.md` 明确区分：

```text
exact raw payload evidence
ConversationItem
ToolCall
CodeCell / TerminalOperation
InteractionEdge
```

稳定课程抽象：

> Trace 应保留足够结构，能还原模型实际看到的输入、Tool Runtime Boundary 和信息流，而不是只有拼接后的日志文本。

这直接服务：

```text
Debug
Replay
Evaluation
Incident Analysis
```

---

# 5. OpenAI Agents SDK Tracing 给出的证据

官方 Tracing 文档覆盖：

```text
task
agent
turn
generation
tool
guardrail
handoff
```

这说明成熟 Agent Framework 会把 Trace 设计成 Runtime 一等能力，而不是应用自行 print。

课程不要求使用某个 SDK，但要掌握这个层次模型。

---

# 6. 为什么要记录“模型看到什么”

假设 Agent 错误调用 Tool：

```text
delete_file("prod.env")
```

只看 Tool Log：

```text
model called delete_file
```

你不知道：

```text
Context 是否被 injection？
旧 Summary 是否错误？
Tool Description 是否误导？
User 是否刚刚批准？
```

所以 Debug 需要：

```text
Model-visible Context Evidence
```

但不能因此把所有敏感 Prompt 永久明文存储。

---

# 7. Trace 与 Privacy 冲突

完整 Trace 可能含：

```text
PII
secret
private source code
customer document
tool arguments
```

因此 Observability 也要有安全设计：

```text
redaction
encryption
access control
retention
sampling
tenant isolation
```

可以同时保留：

```text
hash / metadata / structure
```

而不保存完整敏感内容。

---

# 8. Replay 有三种不同含义

### Evidence Replay

重新查看：

```text
当时 Context / Tool / State 是什么
```

最安全。

### Model Replay

使用相同输入重新调用模型。

问题：

```text
模型版本变了
sampling 非确定
provider behavior 变化
```

所以不一定完全复现。

### Side-effect Replay

重新执行 Tool。

高风险：

```text
会再次发邮件 / 改 DB / 调付款
```

默认不能把 Replay 等同于“重跑整个 Agent”。

---

# 9. Trace 如何定位“Agent 卡住”

典型症状：

```text
Run 20 分钟没结束
```

Trace 可以检查：

```text
Model latency?
Tool hanging?
Repeated tool calls?
Waiting approval?
Subagent unfinished?
Compaction loop?
Queue / provider throttling?
```

如果只有最终 request latency：

```text
无法判断卡在哪里
```

---

# 10. Token / Cost 异常怎么定位

例如：

```text
同类任务 token cost 突然 ×5
```

Trace 要能看到：

```text
context source tokens
history growth
memory injection
retrieval size
tool schema size
tool result size
compaction count
subagent count
```

这样才能知道：

```text
是模型变贵
还是 Context 膨胀
```

---

# 11. Context Management 自己也需要 Observability

Codex `compact.rs` Source Index 已确认有 Compaction Analytics：

```text
trigger
reason
phase
status
context tokens
summary tokens
latency
```

这支持一个重要原则：

> **Context Management 不是黑盒 preprocessing，它本身也要被 Trace / Metric。**

例如可以看：

```text
compaction_rate
post_compaction_failure_rate
context_tokens_before/after
```

---

# 12. Agent Trace Schema 示例

```python
TraceEvent(
    event_id="evt_1",
    run_id="run_1",
    turn_id="turn_3",
    step_id="step_7",
    type="tool_call",
    parent_id="model_6",
    timestamp=...,
    attributes={...},
)
```

核心目标：

```text
结构化
可关联
可查询
可采样
可脱敏
```

---

# 13. Observability 不应该和 Evaluation 混为一谈

Observability：

```text
告诉你发生了什么
```

Evaluation：

```text
判断结果好不好
```

Trace 是 Evaluation 的重要原始数据，但：

```text
有 Trace
≠ 有好 Eval
```

下一章进入 Evaluation。

---

# 14. HUMAN-A 信号

`AGENT-043 Execution Trace / Observability` 有 7 个独立来源，并且真实面试直接追：

```text
step/model/tool/state 级 Trace
卡住定位
失败定位
延迟
Token 异常
Replay / Debug
```

这说明 Agent Observability 已经从“锦上添花”进入 Production 必答。

---

# 15. 面试怎么答

## Q：Agent Trace 应该记录什么？

🎯 **30 秒回答**：

> 我会用 run/turn/step/model-call/tool-call 的层级 ID 做结构化 trace。至少记录模型实际看到的 context evidence、provider/model、tool call/result、permission、state transition、checkpoint/compaction、subagent relation、latency/token/cost。Trace 要能支持 debug 和 replay，但敏感 Prompt/Tool 参数要做 redaction、加密和 retention 控制。它和普通日志不同，重点是重建一条 Run 的因果执行链。

---

# 16. 高频易错点

⚠️ **Agent Observability = print Tool Call。** 缺 Context / State / Model / Correlation。

⚠️ **Trace 越完整越好。** 敏感数据和存储成本需要治理。

⚠️ **Replay 就是重新运行 Tool。** 外部副作用可能重复。

⚠️ **有 Trace 就有 Eval。** Trace 是证据，不是评价标准。

---

# 17. 本章自测

<details><summary>1. 为什么 Tool Call 必须有 correlation id？</summary>

因为异步、并行和 Multi-Agent 环境下 Tool Result 必须准确关联到产生它的 Call，不能只靠顺序或文本猜测。
</details>

<details><summary>2. 为什么要记录 Context Generation / Compaction Generation？</summary>

同一个 Run 在不同 compaction 后模型看到的上下文可能不同；记录 generation 才能解释某次错误决策使用了哪一版 Context。
</details>

<details><summary>3. 为什么 Side-effect Replay 风险最高？</summary>

它会真正再次执行外部动作，可能重复付款、消息、写入，因此 Debug Replay 应优先重放证据和状态，而不是默认重跑副作用。
</details>
