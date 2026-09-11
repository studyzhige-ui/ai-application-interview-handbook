# 17｜Intent / Model Routing、Provider Adapter 与 Runtime Resilience

> 本章合并旧 `IntentRouting`、`ModelRouting`，并纳入 `AGENT-038 Runtime Resilience Policy`。核心问题是：**请求进入 Runtime 后，怎样选择能力 / 模型 / Provider，并在依赖失败时换路而不是把所有逻辑交给一个 LLM。**

## 1. Routing 有三个层次

```text
Intent Routing
→ 这是什么任务？

Capability Routing
→ 应该调用哪类 Tool / Skill / Agent？

Model Routing
→ 用哪个模型 / Provider 完成这一阶段？
```

这三层不要混成一个大 Prompt。

## 2. Intent Recognition 怎么做

可选：

```text
rule
small classifier
embedding / nearest intent
LLM classification
hybrid
```

如果业务类别稳定且风险高，Rule/Classifier 往往比大模型自由路由更可控。

## 3. Model Routing 的维度

```text
quality
latency
cost
context window
tool capability
modality
region / compliance
availability
```

例如：

```text
simple classify → small fast model
repo planning   → stronger reasoning model
vision task     → multimodal model
long context    → model with enough window
```

## 4. Provider Adapter

不同 Provider 的差异不只在 API URL：

```text
message format
tool protocol
stream event
error code
usage accounting
reasoning control
context limit
structured output
```

Runtime 应做 normalization：

```text
Internal Request
→ Provider Adapter
→ Provider API
→ normalize response/error/event
→ Internal Runtime
```

## 5. Resilience Policy

不要写成统一 `retry 3 times`。

要判断：

```text
error class
retry eligibility
idempotency
remaining deadline
provider health
fallback quality floor
```

策略组合：

```text
Retry + Backoff
Circuit Breaker
Provider Fallback
Model Downgrade / Upgrade
Capability Fallback
Fail Fast
```

## 6. Tool Failure 与 Runtime Resilience 的边界

```text
Tool Chapter
= 一次 Invocation 的错误语义

本章
= 跨 Tool / Model / Provider 的整体恢复策略
```

例如单次 Provider 429：

```text
classify transient
→ retry with jitter
→ repeated failure
→ circuit open
→ fallback provider/model
```

## 7. Routing 也需要 Evaluation

指标：

```text
route accuracy
task success
fallback rate
cost per successful task
p95 latency
quality delta after fallback
wrong-capability rate
```

不要只看分类 Accuracy。

## 8. HUMAN-A

- `AGENT-032` Model Routing / Runtime Adapter：9 来源；
- `AGENT-038` Runtime Resilience：15 来源；
- `AGENT-045` Intent Recognition / Routing：11 来源。

## 9. 🎯 面试回答

> Routing 最好拆成 Intent、Capability、Model 三层。稳定业务可以先用 Rule/Classifier 缩小范围，再让模型做更难的动态选择；Provider Adapter 统一不同 Tool Protocol、Streaming 和 Error Semantics。恢复策略不能全局统一 Retry，而要按错误类型、幂等性、deadline 和 provider health 决定 Retry、Circuit Breaker、Fallback 或 Fail Fast，并用任务成功率、成本和延迟验证路由策略。

<details><summary>自测：为什么“模型选型”不能只按 benchmark 排名？</summary>

因为 Runtime 还受延迟、价格、上下文、Tool/Multimodal 能力、合规、可用性和 fallback 语义影响，最终要优化具体任务的成功率与成本。
</details>