# 09. L3 接入层：模型适配、路由与容错

[← 08](08-MultiAgentCoordination.md) · [Agent 主线](../README.md) · [10 →](10-ToolContractAndDiscovery.md)

> 主线位置：**L3 接入层**。运行层的需求已经明确，开始设计它与外部能力的稳定接口。
>
> 本章产物：**模型能力矩阵、适配边界与恢复策略**。

[先区分选择策略和供应商适配](#part-1) → [按错误语义恢复，而不是统一重试](#part-2) → [路由与模型变更也需要验收](#part-3)

<a id="part-1"></a>

## 1. 先区分选择策略和供应商适配

L2 或平台策略决定选择什么模型，L3 把统一请求转换为具体供应商协议，L4 提供实际模型服务。本章放在 L3，是为了讲清调用边界，不是把全部路由决策从运行层搬走。

能力适配必须保留差异：模型可能不支持某种工具协议、多模态输入、上下文长度或结构化输出约束。不能把不支持伪装成支持。

### Model Routing 的目标是什么

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

### Provider Adapter 的接入职责

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

### Provider Adapter 应统一什么，不统一什么

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

<a id="part-2"></a>

## 2. 按错误语义恢复，而不是统一重试

模型失败、工具失败和状态保存失败具有不同后果。恢复策略与运行预算、动作幂等和当前生命周期状态共同决定。

### Runtime Resilience 先做 Error Classification

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

### Retry Eligibility 为什么比 Retry Count 更重要

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

### Model Failover 会不会改变结果语义

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

### Circuit Breaker 在 Agent Runtime 中怎么用

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

### Fallback 不应该静默

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

### Routing Failure Timeline

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

<a id="part-3"></a>

## 3. 路由与模型变更也需要验收

路由可以按任务能力、上下文、隐私边界、成本和可用性筛选，但必须记录实际选中的模型、协议版本和降级原因。比较路由方案要用同一任务集和同一成功标准。

失败时可以暂停、排队、降级或更换模型；每种选择都要说明其语义影响。切换模型不应重放已执行工具；未完整结束的流式工具参数不能被当作可执行请求。

模型选择与训练、Transformer、推理服务内部机制仍回到 [LLM Foundation](../../llm-foundation/README.md)。本模块负责它们在 Agent 调用链上的契约。

## 本章自测

<details>
<summary>Adapter 是否应抹平所有供应商差异？</summary>

不应。必须保留能力差异和不支持情况，避免把不兼容的工具、多模态或状态协议静默伪装为支持。

</details>

<details>
<summary>模型切换后可以把整个任务再跑一遍吗？</summary>

不能默认这样做。必须保留已执行动作与状态，重新验证协议兼容和恢复语义。

</details>

## 回到主线

现在应能独立说明：模型能力矩阵、适配边界与恢复策略。下一章：[L3 接入层：工具契约、注册与发现](10-ToolContractAndDiscovery.md)。

对应真人问题：`AGENT-032`、`AGENT-038`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 08](08-MultiAgentCoordination.md) · [Agent 主线](../README.md) · [10 →](10-ToolContractAndDiscovery.md)
