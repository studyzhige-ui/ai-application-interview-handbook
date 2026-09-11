# 17. Intent / Model Routing、Provider Adapter 与 Runtime Resilience

Agent Runtime 往往不是：

```text
所有请求
→ 同一个模型
→ 同一个 Tool Set
```

而是需要决定：

```text
这是哪类任务？
需要哪种能力？
应该用哪个模型 / Provider？
失败后能不能换模型？
Tool Protocol 不一样怎么办？
```

这一章把 Intent Routing、Model Routing、Provider Adapter 和 Resilience 放在一起，是因为它们共同决定：

> **一次 Agent Run 选择哪条执行路径，并在模型/Provider 失败时怎样保持语义一致。**

---

## 1. Routing 至少有三层

### Intent Routing

```text
用户想做什么？
```

例如：

```text
Q&A
code edit
search
billing
support escalation
```

### Capability Routing

```text
这个任务需要哪些 Tool / Skill / Agent？
```

### Model / Provider Routing

```text
哪种模型足够完成任务？
```

可能考虑：

```text
quality
latency
cost
context length
tool support
multimodal
region/compliance
```

三者不要混成一个 `router_llm()`。

---

# 2. Intent Recognition 可以有多种实现

HUMAN-A `AGENT-045` 直接比较：

```text
Rule
Small Model
LLM Classification
Tool-schema autonomous selection
```

没有一种方案永远最好。

## Rule

优点：

```text
快
可解释
稳定
```

适合明确协议：

```text
/command
固定 route
明显 keyword / tenant policy
```

## Small Classifier

适合：

```text
标签稳定
数据充足
需要低延迟
```

## LLM Router

适合：

```text
意图开放
语言复杂
需要语义理解
```

但成本和不确定性更高。

## Agent 自主 Tool Selection

当 Tool Schema 已经足够表达能力时，模型可以直接选择 Tool，不一定需要独立 intent classifier。

---

# 3. Router 也需要 Evaluation

不要只说：

> “我们用 LLM 做 Intent，效果不错。”

至少建立：

```text
labeled routing dataset
confusion matrix
per-intent precision / recall
fallback rate
unknown rate
latency
cost
```

更重要的是：

```text
routing error 的 downstream impact
```

例如：

```text
普通问答错路由到 destructive agent
```

比：

```text
FAQ 被路由到 generic chat
```

风险高得多。

因此不同 intent 可以有不同 error cost。

---

# 4. Model Routing 的目标是什么

不是单纯：

```text
便宜任务用小模型
难任务用大模型
```

更完整的决策函数：

```text
Task Complexity
+ Required Capability
+ Risk
+ Context Length
+ Tool Compatibility
+ Latency SLO
+ Cost Budget
→ Model Route
```

例如：

```text
classification
→ small model

complex code refactor
→ stronger model

image understanding
→ multimodal model
```

---

# 5. Provider Adapter 为什么是 Runtime 能力

不同 Provider 可能在：

```text
message format
tool call shape
structured output
stream event
usage field
finish reason
error code
context limit
```

上不同。

如果业务代码到处直接写 Provider-specific 逻辑：

```text
Agent Loop 会被污染
```

更稳：

```text
Normalized Runtime Request
        ↓
Provider Adapter
        ↓
Provider API
        ↓
Normalized Runtime Event
```

---

# 6. Provider Adapter 应统一什么，不统一什么

应该统一：

```text
message / tool call semantic
usage
stream events
error category
cancellation
```

不应该强行抹平：

```text
某 Provider 独有 capability
不同上下文限制
不同 Tool 约束
不同 reasoning / caching feature
```

正确做法：

```text
Common Interface
+ Capability Metadata
```

而不是最低公分母 API。

---

# 7. Claude Code 的实现信号

固定 Source Index 确认 `QueryEngine` 配置存在：

```text
fallbackModel
```

这支持一个实现事实：

> 成熟 Runtime 会把 Model / Provider Failure 后的 fallback 纳入 Harness 控制面。

但具体 fallback 条件不能仅凭这一字段推断，本章只使用这个已核验边界。

---

# 8. Runtime Resilience 先做 Error Classification

Provider / Tool 失败不能全部：

```text
retry 3 times
```

至少区分：

```text
Transient
Rate Limited
Timeout
Context Too Large
Invalid Request
Auth / Permission
Provider Outage
Model Unsupported Capability
Content / Policy Rejection
```

然后定义：

```text
retryable?
backoff?
fallback?
rebuild context?
ask user?
fail run?
```

这对应 HUMAN-A `AGENT-038 Runtime Resilience Policy`。

---

# 9. Retry Eligibility 为什么比 Retry Count 更重要

例如：

```text
429 Rate Limit
→ retry with backoff / alternate provider
```

而：

```text
400 invalid tool schema
→ retry 原请求没有意义
```

又例如：

```text
context_length_exceeded
→ 应 compact / trim / offload
```

不是：

```text
sleep 1s 再发一次
```

---

# 10. Model Failover 会不会改变结果语义

如果：

```text
Model A 支持 Tool X
Model B 不支持
```

简单 Failover 会破坏 Run。

所以 Route / Failover 前要检查：

```text
capability compatibility
context limit
structured output support
tool protocol
policy
```

可以维护：

```python
ModelCapability(
    tool_calling=True,
    vision=False,
    max_context=128000,
    structured_output=True,
)
```

---

# 11. Circuit Breaker 在 Agent Runtime 中怎么用

如果某 Provider 持续：

```text
timeout
5xx
```

继续每个 Run 都试一次：

```text
延迟累积
成本增加
线程/连接堆积
```

可以：

```text
Closed
→ failures threshold
→ Open
→ skip provider
→ Cooldown
→ Half-open probe
```

通用 Circuit Breaker 机制 Primary 在 AI Backend Engineering；这里关注它如何影响 Agent Routing / Run semantics。

---

# 12. Fallback 不应该静默

假设：

```text
强模型失败
→ 自动切弱模型
```

如果任务是：

```text
修改生产权限配置
```

风险可能不可接受。

因此 Route Policy 可以是：

```text
low-risk task → silent fallback allowed
high-risk task → require user / operator confirmation
```

同时 Trace 必须记录：

```text
requested model
actual model
fallback reason
```

---

# 13. Routing Failure Timeline

```text
T0 Intent Router 把“删除账号”识别成“查询账号”
T1 Runtime 加载 read-only tool set
T2 Agent 无法完成
T3 自动 fallback 到 generic agent
T4 generic agent 获得更宽 Tool Set
T5 高风险动作绕过原 route policy
```

说明：

> Routing 不只是 UX 分类，还会影响 Capability / Permission Boundary。

---

# 14. HUMAN-A 信号

本章主要承接：

- `AGENT-032` Model Routing / Runtime Adapter：9 个来源；
- `AGENT-038` Runtime Resilience Policy：15 个；
- `AGENT-045` Intent Recognition / Routing：11 个。

真实追问会从“怎么分类意图”继续到：

```text
准确率低怎么办？
数据少怎么办？
模型切换 Tool Protocol 怎么适配？
Provider 挂了怎么办？
```

---

# 15. 面试怎么答

## Q：Agent Router 怎么设计？

🎯 **30 秒回答**：

> 我会先区分 intent、capability 和 model routing。稳定且高风险的规则优先 deterministic rule；开放语义可以用 classifier/LLM；如果 Tool schema 已足够表达能力，也可让模型直接选 Tool。Router 必须有 labeled eval、confusion matrix 和 fallback/unknown path。Model route 再结合质量、延迟、成本、context、tool support 和 risk，Provider 差异通过 adapter 归一化，但保留 capability metadata。

## Q：Provider 失败怎么 Fallback？

> 先分类 error，只有 transient/rate-limit 等 retryable failure 才 backoff；context overflow 应触发 compaction，不是重试；fallback 前检查 Tool/Context/Structured Output 等 capability compatibility，高风险任务不能静默降级，并在 Trace 记录实际模型和原因。

---

# 16. 高频易错点

⚠️ **所有 Intent 都用 LLM Router。** Rule / classifier 可能更稳定便宜。

⚠️ **所有错误重试三次。** Invalid request / context error 需要修输入。

⚠️ **Model Fallback 只要 API 格式一样就行。** Capability 可能不兼容。

⚠️ **Provider Adapter 应把所有特性抹平。** 应保留 capability metadata。

---

# 17. 本章自测

<details><summary>1. Intent Routing 和 Tool Selection 有什么区别？</summary>

Intent Routing 是把请求识别成任务类别或处理路径；Tool Selection 是在当前能力集中选择具体动作。某些场景模型可以直接 Tool Selection，不需要独立意图分类层。
</details>

<details><summary>2. 为什么 context_length_exceeded 不应该直接 Retry？</summary>

输入本身超限，重发不会改变条件。应该 trim/offload/compact 或换支持更长 Context 的兼容模型。
</details>

<details><summary>3. 为什么高风险任务的 Model Fallback 需要更谨慎？</summary>

模型能力、工具遵循和安全行为可能不同；静默降级可能改变执行风险和正确性，需要显式 policy 或人工确认。
</details>
