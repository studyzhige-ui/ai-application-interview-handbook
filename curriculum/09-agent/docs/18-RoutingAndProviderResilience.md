# 18. Routing：意图、模型适配与供应商容错

Agent Runtime（运行时执行系统） 往往不是：

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

这一章把 Intent Routing、Model Routing、Provider（模型服务方） Adapter 和 Resilience 放在一起，是因为它们共同决定：

> **一次 Agent Run 选择哪条执行路径，并在模型/Provider 失败时怎样保持语义一致。**

[← 上一章](17-SkillsHooksAndExtensions.md) · [Agent 目录](../README.md) · [下一章 →](19-MultiAgentAndA2A.md)

---

<a id="section-1"></a>

## 1. Routing 至少有三层

<a id="legacy-17-01"></a>

路由就是决定交给谁，但这个谁可能是业务流程、工具或模型服务。三个候选集合、错误后果和验证方式不同，先区分对象，再选规则、分类器或模型。

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

<a id="section-2"></a>

## 2. Intent Recognition 可以有多种实现

<a id="legacy-17-02"></a>

HUMAN-A `AGENT-045` 直接比较：

```text
Rule
Small Model
LLM Classification
Tool-schema autonomous selection
```

没有一种方案永远最好。

### Rule

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

### Small Classifier

适合：

```text
标签稳定
数据充足
需要低延迟
```

### LLM Router

适合：

```text
意图开放
语言复杂
需要语义理解
```

但成本和不确定性更高。

### Agent 自主 Tool Selection

当 Tool Schema 已经足够表达能力时，模型可以直接选择 Tool，不一定需要独立 intent classifier。

---

<a id="section-3"></a>

## 3. Router 也需要 Evaluation

<a id="legacy-17-03"></a>

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

<a id="section-4"></a>

## 4. Model Routing 的目标是什么

<a id="legacy-17-04"></a>

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

Capability compatibility（能力兼容）包括工具调用格式、结构化输出、图片/文件、上下文限制和所需推理能力。先剔除不满足硬约束的候选，再比较任务质量、时延和费用。Provider adapter（供应商适配器）统一请求/响应边界，但不能假装所有差异都不存在。

例如模型A返回一组工具调用，模型B只支持文本。把同一消息原样发B不叫可靠降级，应转换到经过验证的可用流程或显式失败；不能静默把关键功能丢掉后仍宣称任务成功。模型版本变更需要代表任务回归，但不必把全部Schema每条日志复制一次，可记录所用配置引用。

---

<a id="section-5"></a>

## 5. Provider Adapter 为什么是 Runtime 能力

<a id="legacy-17-05"></a>

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

<a id="section-6"></a>

## 6. Provider Adapter 应统一什么，不统一什么

<a id="legacy-17-06"></a>

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

<a id="section-7"></a>

## 7. Claude Code 的实现信号

<a id="legacy-17-07"></a>

固定 Source Index 确认 `QueryEngine` 配置存在：

```text
fallbackModel
```

这支持一个实现事实：

> 成熟 Runtime 会把 Model / Provider Failure 后的 fallback 纳入 Harness 控制面。

但具体 fallback 条件不能仅凭这一字段推断，本章只使用这个已核验边界。

---

<a id="section-8"></a>

## 8. Runtime Resilience 先做 Error Classification

<a id="legacy-17-08"></a>

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

这对应 HUMAN-A `AGENT-038` Runtime Resilience Policy。

此处处理依赖故障和供应商差异；第06章已处理单次工具错误。不能因为模型服务失败，就从头重跑已经产生外部动作的整个任务。

---

<a id="section-9"></a>

## 9. Retry Eligibility 为什么比 Retry Count 更重要

<a id="legacy-17-09"></a>

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

<a id="section-10"></a>

## 10. Model Failover 会不会改变结果语义

<a id="legacy-17-10"></a>

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
# 能力声明示意：路由先检查实际支持范围，不能只替换模型名。
ModelCapability(
    tool_calling=True,
    vision=False,
    max_context=128000,
    structured_output=True,
)
```

Retry（重试）针对有资格重试的短暂错误；Circuit breaker（熔断）在持续失败时暂时减少对故障依赖的调用；Fallback（后备方案）换一个可接受的路径。这些通用算法归AI Backend，本章关心它们对Agent语义的影响。

```text
一次模型请求失败
→ 判断是限流/临时网络还是参数/能力错误
→ 在总Deadline内有限重试，避免多层放大
→ 可用后备模型须满足当前能力与输入限制
→ 保留已经发生的工具动作，不从任务起点重跑
→ 记录降级及质量影响，无法满足要求则明确停止
```

熔断不是遇到一次失败就永久禁用，后备也不是无限嵌套供应商。重试预算、健康恢复探测和降级质量都应可观察，但执行过的写操作必须回到第13章核对。

<details>
<summary>实际产品中的选项与边界</summary>

Claude Code用户快照QueryEngine配置包含fallbackModel，`query.ts`在流式fallback时处理旧尝试留下的助手项与工具结果，避免把孤立结果混进新尝试。这个实现提醒我们：模型切换不仅改名字，还涉及历史关联与已经执行的工作；不能从配置字段推断所有业务动作都能安全重跑。

Codex固定`build_prompt`取当前模型/步骤设置与工具Router（路由器），`context_window.rs`按模型预算判断，模型变化时上下文处理可能不同。App Server与模型提供者适配层具有各自接口，不是“所有模型返回文本就能直接互换”。具体默认路由规则以产品配置和源码分支为准。

</details>

---

<a id="section-11"></a>

## 11. Circuit Breaker 在 Agent Runtime 中怎么用

<a id="legacy-17-11"></a>

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

<a id="section-12"></a>

## 12. Fallback 不应该静默

<a id="legacy-17-12"></a>

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

同时 Trace（执行追踪） 必须记录：

```text
requested model
actual model
fallback reason
```

---

<a id="section-13"></a>

## 13. Routing Failure Timeline

<a id="legacy-17-13"></a>

```text
T0 Intent Router 把“删除账号”识别成“查询账号”
T1 Runtime 加载 read-only tool set
T2 Agent 无法完成
T3 自动 fallback 到 generic agent
T4 generic agent 获得更宽 Tool Set
T5 高风险动作绕过原 route policy
```

说明：

> Routing 不只是 UX 分类，还会影响 Capability / Permission（权限） Boundary。

---

<a id="human-a"></a>

## 14. HUMAN-A 信号

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

<a id="interview"></a>

## 15. 面试怎么答

### Q：Agent Router 怎么设计？

🎯 **30 秒回答**：

> 我会先区分 intent、capability 和 model routing。稳定且高风险的规则优先 deterministic rule；开放语义可以用 classifier/LLM；如果 Tool schema 已足够表达能力，也可让模型直接选 Tool。Router 必须有 labeled eval、confusion matrix 和 fallback/unknown path。Model route 再结合质量、延迟、成本、context、tool support 和 risk，Provider 差异通过 adapter 归一化，但保留 capability metadata。

### Q：Provider 失败怎么 Fallback？

🎯 **30 秒回答**：

> 先分类 error，只有 transient/rate-limit 等 retryable failure 才 backoff；context overflow 应触发 compaction，不是重试；fallback 前检查 Tool/Context/Structured Output 等 capability compatibility，高风险任务不能静默降级，并在 Trace 记录实际模型和原因。

### Q：Agent路由至少分哪几类？

🎯 **30 秒回答**：

> 入口意图路由选择业务流程，模型路由选择满足能力与质量约束的模型，能力路由把请求分发到工具处理器。它们输入、输出和风险不同，应分别评估，不用一个LLM分类节点包办所有责任。

### Q：如何评估Router？

🎯 **30 秒回答**：

> 对意图用标注集、混淆矩阵、未知意图/澄清率及风险加权下游影响；对模型用代表性任务质量、能力兼容、延迟、费用和失败率；对工具路由检查处理器、权限和版本正确性。

### Q：为什么Adapter不应抹平全部供应商差异？

🎯 **30 秒回答**：

> 真正不支持的能力不能被包装成支持。适配器应统一能统一的结构，同时显式暴露限制和错误，让上层选择可用路径，否则静默降级会破坏任务语义。

---

<a id="pitfalls"></a>

## 16. 高频易错点

⚠️ **所有 Intent 都用 LLM Router。** Rule / classifier 可能更稳定便宜。

⚠️ **所有错误重试三次。** Invalid request / context error 需要修输入。

⚠️ **Model Fallback 只要 API 格式一样就行。** Capability 可能不兼容。

⚠️ **Provider Adapter 应把所有特性抹平。** 应保留 capability metadata。

⚠️ **Router一律用最大LLM。** 先规则与简单基线，有复杂语言需求再比较模型。

⚠️ **Fallback只是换模型名。** 上下文和能力契约可能不兼容。

⚠️ **模型错误就重启整个Agent。** 会重复已完成工具和副作用。

⚠️ **总体分类准确率高就够。** 高风险类别误路由与未知意图也需验证。

---

<a id="self-test"></a>

## 17. 本章自测

<details><summary>1. Intent Routing 和 Tool Selection 有什么区别？</summary>

Intent Routing 是把请求识别成任务类别或处理路径；Tool Selection 是在当前能力集中选择具体动作。某些场景模型可以直接 Tool Selection，不需要独立意图分类层。

</details>

<details><summary>2. 为什么 context_length_exceeded 不应该直接 Retry？</summary>

输入本身超限，重发不会改变条件。应该 trim/offload/compact 或换支持更长 Context 的兼容模型。

</details>

<details><summary>3. 为什么高风险任务的 Model Fallback 需要更谨慎？</summary>

模型能力、工具遵循和安全行为可能不同；静默降级可能改变执行风险和正确性，需要显式 policy 或人工确认。

</details>

<details><summary>4. 明确/report命令是否需要LLM路由？</summary>

通常规则更直接稳定。只有命令内部仍有语义不确定性时才需要进一步模型判断。

</details>

<details><summary>5. A支持工具，B不支持，B更便宜是否就可做后备？</summary>

不能直接替换。硬能力不满足，需经过验证的替代流程或明确失败。

</details>

<details><summary>6. 模型调用超时，之前已发送邮件，能重跑整段吗？</summary>

不能。之前的写入是独立事实，应保留并核对；恢复当前模型请求与重做所有任务不是一回事。

</details>

<details><summary>7. 熔断和权限拒绝可以同样自动恢复吗？</summary>

不同。熔断针对依赖健康可探测恢复；权限拒绝需授权依据变化，不能靠重试绕过。

</details>

<details><summary>8. 路由低置信度为什么允许澄清？</summary>

澄清可以降低错误动作风险，未知请求不应被强行塞入已知流程。需要把澄清成本与误路由代价一起评估。

</details>

<details><summary>9. 模型升级后只跑一个正常例子够吗？</summary>

不够，应覆盖工具格式、长上下文、结构化输出、错误和代表领域任务；升级可能改变质量与恢复边界。

</details>

---

[← 上一章](17-SkillsHooksAndExtensions.md) · [Agent 目录](../README.md) · [下一章 →](19-MultiAgentAndA2A.md)
