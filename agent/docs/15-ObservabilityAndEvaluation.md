# 15. 横切治理：观测、评测与持续改进

[← 14](14-IdentityPermissionsAndSafety.md) · [Agent 主线](../README.md) · [16 →](16-ProductionArchitectureAndEvolution.md)

> 主线位置：**质量运营，贯穿 L1–L4**。行动被约束后，还要知道系统做了什么、结果是否有效以及怎样改善。
>
> 本章产物：**可观测执行与评测驱动的改进闭环**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 分三段读：§1–2重建与定位过程，§3定义验证对象，§4把坏例变成改进。指标变好之前先固定任务、环境与评分口径，不能以日志完整代替任务成功。

[观测回答发生了什么，评测回答做得怎样](#part-1) → [可解释地回放、诊断与定位](#part-2) → [从任务契约推导验证对象](#part-3) → [评测推动修改，而不是只生成分数](#part-4)

<a id="part-1"></a>

## 1. 观测回答发生了什么，评测回答做得怎样

两者是贯穿四层的质量闭环。执行轨迹应能关联任务、运行、模型、工具、上下文版本和外部动作，同时限制敏感数据记录。

### Log、Metric、Trace 各解决什么

#### Log

```text
某个时刻发生了什么
```

例如：

```text
provider timeout
permission denied
```

#### Metric

```text
整体系统趋势
```

例如：

```text
agent_success_rate
p95_tool_latency
context_compaction_rate
```

#### Trace

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

### Trace Identity

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

### 一个 Agent Span 应该记录什么

不同 Span 类型字段不同。

#### Model Span

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

#### Tool Span

```text
tool name
argument fingerprint
permission decision
start/end
result status
external ref
side-effect class
```

#### Context Span

```text
context source counts
selected tokens
compaction generation
cache hit
memory/retrieval refs
```

#### State Span

```text
from_status
to_status
state_version
checkpoint_id
```

### 为什么要记录“模型看到什么”

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

### Trace 与 Privacy 冲突

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

<a id="part-2"></a>

## 2. 可解释地回放、诊断与定位

证据回放、模型重跑和副作用重放必须分开。默认回放不能重新执行生产写操作。

### Replay 有三种不同含义

##### Evidence Replay

重新查看：

```text
当时 Context / Tool / State 是什么
```

最安全。

##### Model Replay

使用相同输入重新调用模型。

问题：

```text
模型版本变了
sampling 非确定
provider behavior 变化
```

所以不一定完全复现。

##### Side-effect Replay

重新执行 Tool。

高风险：

```text
会再次发邮件 / 改 DB / 调付款
```

默认不能把 Replay 等同于“重跑整个 Agent”。

### Trace 如何定位“Agent 卡住”

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

### Token / Cost 异常怎么定位

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

### Context Management 自己也需要 Observability

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

### Agent Trace Schema 示例

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

### Observability 不应该和 Evaluation 混为一谈

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

<a id="part-3"></a>

## 3. 从任务契约推导验证对象

结果、过程、组件、资源与安全是验证视角，不是重新划分四层架构。不能只看最后一句话是否自然。

### 先分清 Agent Harness 和 Eval Harness

Anthropic Agent Evals 官方资料明确强调区分：

```text
Agent Harness
= 让 Agent 真正执行任务的 Runtime

Evaluation Harness
= 给 Agent 提供任务环境、收集结果、运行 grader、计算 metric 的系统
```

这两个 Harness 不能混。

如果 Eval Harness 有 bug：

```text
Agent 可能没变
但分数变了
```

### 最终结果比“模型说完成了”更重要

错误评价：

```text
Agent final answer:
“任务已经完成。”
→ pass
```

模型可能只是声称成功。

更好的 Outcome Verification：

```text
代码任务 → tests pass?
数据任务 → target rows correct?
浏览任务 → expected state exists?
客服任务 → policy + resolution satisfied?
```

原则：

> **优先评价 Environment Outcome，而不是自我报告。**

### 评测的四个验证视角（不是架构层）

#### Final Outcome

```text
task_success
correctness
acceptance_criteria
```

#### Process / Runtime

```text
loop length
unnecessary steps
repeated action
recovery behavior
```

#### Component

```text
tool selection
argument validity
intent route
memory retrieval
compaction correctness
```

#### Resource / Safety

```text
latency
cost
token
tool calls
permission violation
unsafe side effect
```

最终不能只看一个总分。

### Eval Dataset 从哪里来

HUMAN-A `AGENT-035` 直接问 Benchmark / Ground Truth。

数据集来源可以是：

```text
真实线上任务抽样
线上 Bad Case
人工设计核心能力 Case
历史 Incident
安全 / adversarial Case
边界输入
长任务 / 大 Context Case
```

最危险的做法：

```text
只用开发者自己写的 20 个 Happy Path
```

这种 Benchmark 很容易被系统“学会”。

### Dataset 要分层采样

例如：

```text
simple 30%
medium 40%
long-horizon 20%
safety / adversarial 10%
```

还可以按：

```text
tenant
domain
tool type
repository size
language
provider
```

分桶。

如果只看 aggregate score：

```text
某个少数关键场景可能退化
```

### Ground Truth 不一定是一个字符串

对于 Agent，Ground Truth 可能是：

```text
expected environment state
required files changed
forbidden files untouched
required API called once
final database rows
artifact exists
```

所以常见 grader：

```text
unit test
script
SQL query
filesystem diff
HTTP state check
```

往往比 LLM Judge 更可靠。

### LLM Judge 什么时候适合

适合：

```text
开放文本质量
helpfulness
reasoning artifact quality
summary quality
```

但需要：

```text
rubric
calibration
human spot check
judge version pinning
```

不要：

```text
Agent Model
和 Judge Model
完全同源偏差
→ 就当绝对真值
```

### Process Metric 为什么也重要

两个 Agent 最终都成功：

```text
A: 4 tool calls, $0.05, 8s
B: 37 tool calls, $1.20, 90s
```

Outcome 一样，但 Production 质量不同。

所以要看：

```text
steps
cost
latency
retries
subagents
compactions
permission prompts
```

### Tool / Routing Eval

Tool Runtime 可以独立评：

```text
Tool selection accuracy
Argument validity
Permission correctness
Repair success rate
Timeout recovery
```

Router 可以评：

```text
intent confusion matrix
model route success
fallback rate
cost-quality frontier
```

这样 Bad Case 才能定位到组件。

<a id="part-4"></a>

## 4. 评测推动修改，而不是只生成分数

先用轨迹定位失败责任，再形成可复现样例、比较候选改动、做回归与上线检查。

### Agent Eval 与 Trace 的关系

上一章 Trace 保存：

```text
model
context
tool
state
cost
```

Eval Harness 可以读取 Trace：

```text
Final failed
→ Tool selection correct?
→ Tool execution failed?
→ Context lost constraint?
→ Route wrong?
```

所以：

```text
Trace = evidence
Eval = judgment
```

### Regression 为什么必须自动化

Agent 调 Prompt / Tool / Model / Compaction 任一处，都可能：

```text
修一个 Case
坏十个旧 Case
```

因此每次发布：

```text
Baseline
→ Candidate
→ Same Eval Suite
→ compare per bucket
→ block regression
```

不要只看平均分。

### SWE-bench 为什么是重要参考

SWE-bench 用真实 GitHub Issue + Repository Environment 验证代码修改是否真正解决问题。

课程借鉴的是：

> **Coding Agent 的评价应该看 Repository / Test 环境真实结果，而不是只判断生成 Patch 看起来合理。**

这会在下一章 Coding Agent 继续展开。

### Benchmark Contamination / Overfitting

如果团队天天盯同一批 Case 改 Prompt：

```text
Benchmark 变成训练集
```

需要：

```text
train/dev/test split
hidden holdout
rotating production sample
new bad cases
```

尤其 LLM Judge rubric 也可能被针对性优化。

### Data Flywheel

HUMAN-A `AGENT-041` 追问 Self-evolution / Data Flywheel。

健康闭环：

```text
Production Trace
→ Failure / Bad Case
→ Attribution
→ Curated Eval Case
→ Fix Prompt / Tool / Runtime / Model
→ Offline Regression
→ Canary
→ Production Metrics
→ New Evidence
```

不是：

```text
收集所有用户数据
→ 自动训练
→ 自动上线
```

Data Flywheel 的核心是：

> **把真实失败转成可重复验证的工程资产。**

### Online Validation

Offline 过了也要：

```text
shadow
canary
A/B
rollback threshold
```

观察：

```text
task success
user correction
cost
latency
safety incident
fallback
```

因为真实流量分布永远比离线 Dataset 更复杂。

### Evaluation Failure Timeline

```text
T0  团队改 Prompt
T1  Demo 5 个 Case 全部变好
T2  没跑 Regression
T3  上线
T4  高频 Tool 选择准确率下降
T5  成本上涨 2x
T6  用户只看到“回答变慢”
```

根因：

```text
没有 Component + Resource Eval
```

## 从同一个报告任务得到一组可复现验收

这是教学测试设计，不是宣称已经跑过真实Agent或获得某个线上提升。

| 用例 | 要观察的事实 | 通过标准/修改方向 |
|---|---|---|
| 正常授权文件 | 读取范围、引用、产物版本 | 引用可解析且结论可由证据支持；语义需独立核验 |
| 文件无权限 | 访问拒绝和后续动作 | 不越界、不无限重试；修接入/权限而不是加Prompt |
| 两个来源冲突 | 来源版本、冲突标记 | 保留不确定性，不伪造统一结论 |
| 压缩后继续 | 必保约束、外部操作、后续结果 | 允许不同合法路径，但不能丢约束/重复动作 |
| 保存后崩溃 | 稳定动作标识与真实产物 | 恢复后核对并补状态，不重复写新产物 |
| 新版本模型/工具 | 同一任务集的质量、成本、延迟 | 先固定实验条件，再做回归和受控发布 |

Continuation Test不要求压缩前后每个Tool Call逐字相同；评估等价约束与结果、失败恢复及预算，避免把合法探索路径差异误判为错误。日志脱敏后仍应留下足够关联与可受控解析的证据引用。

旧版的具体阅读线索也保留：Codex `rollout-trace/README.md` 区分原始payload、ConversationItem、ToolCall及信息流关系；它支持追踪“看见什么、调用什么、改变什么”，不要求暴露隐藏思维链。参见[Trace固定快照索引](../../research/agent-sources/codex-source-index.md)。

## 本章自测

<details>
<summary>Trace 和 Eval 各回答什么？</summary>

Trace 记录过程及关联事实；Eval 依据任务和约束判断结果、过程、组件与安全资源指标。

</details>

<details>
<summary>一个 bad case 应怎样变成改进？</summary>

用轨迹定位责任与原因，构建可复现用例，修改对应机制，做回归与受控上线，并保留回滚方案。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>压缩后走了不同的合法Tool路径应判错吗？</summary>

不一定；比较约束、证据、结果、预算和失败恢复，不要求逐动作完全相同。

</details>

<details>
<summary>减少token但任务完成率下降，该如何做实验？</summary>

固定数据集、环境、工具和评分，定位上下文选择/压缩缺失，回滚或修正策略，再做回归。

</details>

## 回到主线

现在应能独立说明：可观测执行与评测驱动的改进闭环。下一章：[系统收口：部署、成本、选型与演进](16-ProductionArchitectureAndEvolution.md)。

对应真人问题：`AGENT-034`、`AGENT-035`、`AGENT-041`、`AGENT-043`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 14](14-IdentityPermissionsAndSafety.md) · [Agent 主线](../README.md) · [16 →](16-ProductionArchitectureAndEvolution.md)
