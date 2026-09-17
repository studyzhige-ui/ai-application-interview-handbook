# 20. Trace / Replay：记录必要证据，定位具体问题

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

所以 Production（生产环境） Agent 需要的不只是普通日志，而是：

> **能关联模型调用、工具结果与状态变化，先定位阶段，再按问题取得必要证据的执行轨迹。**

[← 上一章](19-MultiAgentAndA2A.md) · [Agent 目录](../README.md) · [下一章 →](21-EvaluationBenchmarkAndImprovement.md)

---

<a id="section-1"></a>

## 1. Log、Metric、Trace 各解决什么

<a id="legacy-19-01"></a>

报告两分钟没完成，先分清在排队、等模型、等工具还是等批准。Trace（执行追踪）先帮助定位阶段，不要求一开始复制全部文件和Prompt。

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

<a id="section-2"></a>

## 2. Trace Identity

<a id="legacy-19-02"></a>

ID按实际对象选用。小系统先用运行与操作ID即可，有并行和跨服务才增加相应关系；一个运行的配置可以引用一次，不必各事件重复正文。

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

<a id="section-3"></a>

## 3. 一个 Agent Span 可按诊断需要记录什么

<a id="legacy-19-03"></a>

| 数据类别 | 为什么保存 | 通常怎样保留 | 丢失会怎样 |
|---|---|---|---|
| 恢复与业务记录 | 知道取消、待定操作、成功回执 | 按业务可靠性保存，关键写入不可依赖诊断采样 | 可能重复或错误执行 |
| 产物与证据 | 用户取回报告、核验引用 | 内容存一份，按权限/期限提供引用 | 交付或验证受阻 |
| Trace / Log（追踪/日志） | 定位阶段、耗时与错误 | 结构化摘要、采样、脱敏、保留期限 | 诊断信息减少，通常不应改变业务状态 |
| Debug snapshot（调试快照） | 深查特定坏案例 | 明确授权、短期、有限原始输入 | 不应作为所有任务默认前提 |

同一个operation_id可以把Trace关联到可靠回执，而不是把完整回执、Prompt、文件和密钥重复存每个Span。关键安全审计若有不可丢要求，应单独定义审计通道与可靠性，不能把一般诊断Trace改名后就满足要求。

不同 Span 类型字段不同。

### Model Span

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

### Tool Span

```text
tool name
argument fingerprint
permission decision
start/end
result status
external ref
side-effect class
```

### Context Span

```text
context source counts
selected tokens
compaction generation
cache hit
memory/retrieval refs
```

### State Span

```text
from_status
to_status
state_version
checkpoint_id
```

以上字段是诊断菜单而非默认全量Schema。排查工具延迟未必需要客户原文；排查模型选错才进一步取得经授权的相关输入。关键回执独立可靠保存，不依赖诊断采样。

---

<a id="section-4"></a>

## 4. OpenAI Agents SDK Tracing 给出的证据

<a id="legacy-19-05"></a>

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

这说明成熟 Agent Framework 会把 Trace 设计成 Runtime（运行时执行系统） 一等能力，而不是应用自行 print。

课程不要求使用某个 SDK，但要掌握这个层次模型。

SDK的敏感数据收集、导出和保留配置需要实际检查；Tracing不是业务会话存储或事务账本。

---

<a id="section-5"></a>

## 5. 为什么要记录“模型看到什么”

<a id="legacy-19-06"></a>

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

```text
用户：报告一直显示处理中
→ 查询权威任务状态：waiting_tool(op7)
→ Trace定位：上传Span等待很久，重试次数已达预算
→ 操作记录显示：已提交，无回执
→ 查询下游：report42已存在
→ 补齐业务状态，停止重复上传
→ 调查为何回执写入失败，构造回归用例
```

这里Trace负责指路，下游与操作记录负责确认事实。若Trace丢了一段，仍应能安全核对op7；若关键回执只存在被采样丢掉的Trace，数据设计就错了。

模型选错工具则不同：先看当时可见工具集合及配置引用，再在授权范围内调取输入片段，比较描述是否歧义、候选是否缺失。**不同问题需要不同证据，不需要每次默认保存所有东西。**

---

<a id="section-6"></a>

## 6. Trace 与 Privacy 冲突

<a id="legacy-19-07"></a>

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

一次Run可以记录一份配置引用（模型、指令、工具集合的适用版本），各Span引用同一配置；状态并发更新才使用revision，工具协议改变才记录契约版本。并非每个事件都要有独立版本，更不需要每条日志重复配置全文。

引用只能找到内容，不能保证内容永远存在。需要长期可验证的对象，应规定不可变快照或保留期限；不需要原样重演的诊断任务，可以保存脱敏摘要而不是原件。删除、用户隐私和组织合规可能比排障便利更重要，要明确数据目的。

---

<a id="section-7"></a>

## 7. Replay 有三种不同含义

<a id="legacy-19-08"></a>

#### Evidence Replay

重新查看：

```text
当时 Context / Tool / State 是什么
```

最安全。

#### Model Replay

使用相同输入重新调用模型。

问题：

```text
模型版本变了
sampling 非确定
provider behavior 变化
```

所以不一定完全复现。

#### Side-effect Replay

重新执行 Tool。

高风险：

```text
会再次发邮件 / 改 DB / 调付款
```

默认不能把 Replay（重放） 等同于“重跑整个 Agent”。

---

<a id="section-8"></a>

## 8. Trace 如何定位“Agent 卡住”

<a id="legacy-19-09"></a>

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

<a id="section-9"></a>

## 9. Token / Cost 异常怎么定位

<a id="legacy-19-10"></a>

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

<a id="section-10"></a>

## 10. Context Management 自己也需要 Observability

<a id="legacy-19-11"></a>

Codex `compact.rs` Source Index 已确认有 Compaction（上下文压缩） Analytics：

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

<a id="section-11"></a>

## 11. Agent Trace Schema 示例

<a id="legacy-19-12"></a>

下面是帮助理解关联的示意结构。按问题选择字段和保留范围，不作为每个事件永久全量记录的模板。

```python
# 诊断事件示意：按排障需要选择关联字段；不默认附带全部消息或秘密。
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

<a id="section-12"></a>

## 12. Observability 不应该和 Evaluation 混为一谈

<a id="legacy-19-13"></a>

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

<a id="section-13"></a>

## 13. 产品实现与官方资料对照（按需展开）

<details>
<summary>Codex Rollout Trace 的源码证据</summary>

<a id="legacy-19-04"></a>

固定 Codex Source Index 中 `codex-rs/rollout-trace/README.md` 明确区分：

```text
exact raw payload evidence
ConversationItem
ToolCall
CodeCell / TerminalOperation
InteractionEdge
```

稳定课程抽象：

> Trace应保留足够的关联结构来定位信息流；需要深查时按授权取得输入证据，不默认保存全部原文。

这直接服务：

```text
Debug
Replay
Evaluation
Incident Analysis
```

源码存在raw payload证据视图，不证明所有构建默认完整采集。学习其关联能力，不把产品可选调试设施当所有应用必须永久全存的要求。

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)。

---

<a id="human-a"></a>

## 14. HUMAN-A 信号

`AGENT-043` Execution Trace / Observability 有 7 个独立来源，并且真实面试直接追：

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

<a id="interview"></a>

## 15. 面试怎么答

### Q：Agent Trace 应该记录什么？

🎯 **30 秒回答**：

> 我会用 run/turn/step/model-call/tool-call 的层级 ID 做结构化 trace。先记录阶段、状态、耗时、错误类别及必要关联引用；按具体故障取得授权的输入和工具证据，不默认复制全部原始内容。Trace 要能支持 debug 和 replay，但敏感 Prompt/Tool 参数要做 redaction、加密和 retention 控制。它和普通日志不同，重点是重建一条 Run 的因果执行链。

### Q：Trace、History、Checkpoint如何区分？

🎯 **30 秒回答**：

> Trace解释执行路径与耗时，History（历史记录）记录交互，Checkpoint（检查点）保存可恢复的执行位置与状态引用。它们可共享标识但可靠性和保留目的不同。被采样的Trace不能是关键回执唯一来源，完整聊天也不自动等于恢复状态。

### Q：Agent卡住怎样排查？

🎯 **30 秒回答**：

> 先查权威任务状态和等待对象，再用Trace定位排队、模型、工具、审批或保存阶段。针对未知外部结果核对下游而不是直接重试；针对上下文问题再看受权输入快照。修复后把具体失败窗口做成回归测试。

### Q：为什么每个事件不需要自己的版本？

🎯 **30 秒回答**：

> 唯一ID标识事件，版本解决对象变化或兼容性。配置可在Run引用一次，状态revision用于并发，工具版本用于契约变化。应让字段服务具体判断，不因可能排障就每条事件复制所有内容。

### Q：保存原始请求能否保证重现？

🎯 **30 秒回答**：

> 只能重建部分输入条件。模型服务版本、采样、外部数据和执行环境可能变化；应说明重演范围，必要时固定数据和模拟工具。精确重现不是Trace自动承诺，且原始请求的隐私成本需要单独授权。

---

<a id="pitfalls"></a>

## 16. 高频易错点

⚠️ **Agent Observability = print Tool Call。** 缺 Context / State（状态） / Model / Correlation。

⚠️ **Trace 越完整越好。** 敏感数据和存储成本需要治理。

⚠️ **Replay 就是重新运行 Tool。** 外部副作用可能重复。

⚠️ **有 Trace 就有 Eval。** Trace 是证据，不是评价标准。

⚠️ **Trace是恢复数据库。** 它通常允许采样和过期，关键业务状态另存。

⚠️ **Context/Prompt必须每个Span全量记录。** 可以引用一次受控配置，深度快照按需要采集。

⚠️ **有完整日志就能重现外部世界。** 外部服务与模型有变化和不确定性。

⚠️ **所有数据保留越久越好。** 成本、隐私、权限与保留目的都需明确。

⚠️ **诊断日志失败应一律终止业务。** 通常不应；真正强制可靠的审计/回执需独立规定。

---

<a id="self-test"></a>

## 17. 本章自测

<details><summary>1. 为什么 Tool Call 必须有 correlation id？</summary>

因为异步、并行和 Multi-Agent 环境下 Tool Result 必须准确关联到产生它的 Call，不能只靠顺序或文本猜测。

</details>

<details><summary>2. 为什么要记录 Context Generation / Compaction Generation？</summary>

同一个 Run 在不同 compaction 后模型看到的上下文可能不同；记录 generation 才能解释某次错误决策使用了哪一版 Context。

</details>

<details><summary>3. 为什么 Side-effect Replay 风险最高？</summary>

它会真正再次执行外部动作，可能重复付款、消息、写入，因此 Debug Replay 应优先重放证据和状态，而不是默认重跑副作用。

</details>

<details><summary>4. 耗时排查第一步需要下载全部客户文件吗？</summary>

通常不需要。先看阶段时延、队列与错误率定位瓶颈，再决定必要的细节证据。

</details>

<details><summary>5. Trace采样丢了op7记录，还能安全恢复吗？</summary>

如果关键操作记录和回执另行可靠保存，可以；如果只有Trace保存，则恢复设计不合格。

</details>

<details><summary>6. 一个Run里模型配置没变，为什么不用每条日志复制全文？</summary>

保存一次不可变配置引用就能关联，重复全文增加费用与泄漏面，不增加等价信息。

</details>

<details><summary>7. 用户要求删除数据，调试快照也应检查吗？</summary>

应按数据治理范围处理，包括诊断快照、索引和导出；不能只删除业务表却在日志永久保留。

</details>

<details><summary>8. 模型重演应该用线上付款工具吗？</summary>

不应默认这样做。通常隔离或模拟副作用工具，真实行动必须有独立授权与幂等保证。

</details>

<details><summary>9. 只保存脱敏快照，是否不能做任何Debug？</summary>

仍能定位许多控制、结构和协议问题；部分语义问题可能需要更详细受权材料。要诚实说明诊断范围，而不是因此默认全量收集。

</details>

---

[← 上一章](19-MultiAgentAndA2A.md) · [Agent 目录](../README.md) · [下一章 →](21-EvaluationBenchmarkAndImprovement.md)
