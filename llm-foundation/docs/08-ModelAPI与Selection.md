# 08｜Model API、Provider Adapter 与 Model Selection

应用工程师实际使用 LLM 时，接触到的不是裸 Transformer，而是一层 Provider API：

```text
Messages / Role
→ Model API
→ Provider Adapter
→ Model
→ Response / Usage / Tool Call
```

因此“怎样调用模型”和“怎样选择模型”应该在同一个工程闭环中学习。

---

## 1. Model API 在抽象什么

不同 Provider 的 API 形态不同，但常见输入都可以抽象为：

```text
model
messages / input
system / instruction
sampling config
tools / schemas
response format
streaming
max output
metadata
```

输出通常包含：

```text
text / content
structured output
tool call
finish reason
usage / token accounting
provider metadata
```

应用层不应该把业务逻辑直接绑死到某个 Provider 的字段名。

---

## 2. Message Role 为什么重要

常见逻辑角色包括：

```text
System / Developer Instruction
User Input
Assistant History
Tool Result
```

不同模型和 Provider 对 Role / Instruction 的实际支持与优先级可能不同。

课程要记的是：

> **Prompt 不只是一个字符串，而是有协议结构和信任层级的输入。**

Agent Harness 中还会进一步区分 Tool Protocol、Permission 和 Untrusted Content。

---

## 3. Provider Adapter 为什么存在

如果业务代码直接到处写：

```python
provider_a.chat(...)
provider_b.responses(...)
provider_c.generate(...)
```

会造成：

- 字段差异扩散；
- Streaming 逻辑重复；
- Error Mapping 混乱；
- Usage 统计不统一；
- Tool Call / Structured Output 难切换；
- Model Routing 困难。

所以通常需要内部统一契约：

```text
Internal Model Request
        ↓
Provider Adapter
        ↓
Provider-specific Request
```

返回也统一成内部 Response / Event Model。

---

## 4. Adapter 不应该过度抽象

错误做法是为了“统一”而把所有 Provider 能力压成最小公约数。

更好的结构是：

```text
Stable Common Core
+
Capability / Feature Flags
+
Provider-specific Extension Escape Hatch
```

例如：

```text
supports_tool_call
supports_json_schema
supports_reasoning_effort
supports_prompt_cache
supports_image_input
```

这样既能统一基础路径，又不丢掉重要能力。

---

## 5. Model Selection 不是“选最强模型”

真正选型至少看：

```text
Task Quality
Latency / TTFT / TPOT
Cost
Context Window
Output Limit
Tool Calling Reliability
Structured Output Reliability
Multimodal Capability
Safety / Compliance
Regional / Data Policy
Rate Limit / Capacity
Provider Reliability
```

“Benchmark 分数最高”只是一个输入。

---

## 6. 先按 Task 定义 Quality

不同任务的质量指标不同：

### Classification / Routing

```text
Accuracy
F1
Confusion Matrix
```

### Structured Extraction

```text
Schema Validity
Field Accuracy
Retry Rate
```

### Coding

```text
Tests Pass
Patch Acceptance
Regression
```

### RAG QA

```text
Groundedness
Answer Correctness
Citation
Retrieval Interaction
```

### Agent

```text
Task Success
Tool Correctness
Step Count
Cost
Recovery
```

因此 Model Selection 必须基于自己的 Task Eval。

---

## 7. Model Capability Matrix

可以维护一张内部表：

| Model | Quality | TTFT | Cost | Context | Tool | JSON | Vision |
|---|---:|---:|---:|---:|---|---|---|
| A | high | medium | high | large | yes | yes | yes |
| B | medium | low | low | medium | yes | yes | no |
| C | high | high | medium | large | no | yes | yes |

然后根据任务路由。

注意：这些值要由真实 Evaluation / Production Telemetry 更新，而不是永久硬编码。

---

## 8. Small Model vs Large Model

不是所有请求都值得用最大模型。

常见思路：

```text
cheap / fast model
→ simple routing / extraction / classification

stronger model
→ complex reasoning / difficult coding / ambiguous task
```

如果简单任务占大多数，分层路由可以显著降低成本和延迟。

但 Model Routing 本身需要：

- Eval；
- Fallback；
- Route Error 监控；
- Provider Failure Handling。

完整 Runtime 路由在 Agent / Backend 模块继续学习。

---

## 9. Context Window 大不代表更适合任务

一个模型 Context 更大，但可能：

- 更贵；
- TTFT 更高；
- Tool Calling 较弱；
- 任务质量未提升；
- Long Context 利用并不稳定。

所以不能用：

```text
context length
```

作为模型“更高级”的单一指标。

---

## 10. Cost 怎么估

API 模型常按：

```text
Input Tokens
Output Tokens
Cached Tokens
```

或不同能力组合计费。

单请求预估可以抽象：

```text
cost ≈ input_tokens * input_price
     + output_tokens * output_price
     + optional tool / media / cache costs
```

Production 更重要的是：

```text
Cost per Successful Task
```

而不是只看每百万 Token 单价。

如果便宜模型重试三次，最终可能更贵。

---

## 11. Reliability 也是 Model Selection 指标

需要关注：

```text
Rate Limit
Timeout
5xx
Streaming Disconnect
Schema Failure
Tool Call Failure
Regional Availability
Version Change
```

模型质量再强，如果容量不稳定，也可能不适合核心在线路径。

---

## 12. Model Version 为什么要显式记录

Provider 可能更新底层模型或 Alias。

Production Eval 应记录：

```text
provider
model_id
model_version / snapshot if available
prompt_version
sampling_config
request trace
```

否则 Regression 出现后很难复现。

---

## 13. Streaming 的 Provider 差异

不同 Provider 可能把 Streaming Event 表示成：

- Text Delta；
- Tool Call Delta；
- Reasoning/Metadata Event；
- Usage Final Event；
- Error Event。

Adapter 应把这些转换成内部 Event Model，而不是让 UI / Agent Runtime 直接依赖厂商格式。

---

## 14. Fallback 与 Multi-provider

多 Provider 可以提高韧性，但不是简单：

```text
A error → B
```

还要处理：

- Prompt / Role 差异；
- Tool Schema 支持差异；
- Model Quality 差异；
- Context Limit；
- Output Format；
- Idempotency / Duplicate Request；
- Cost Accounting。

完整 Retry / Circuit Breaker 属于 AI Backend Engineering。

---

## 15. 常见错误

- Provider Adapter 就是把 API 名字改成一样：过于浅。
- 选最强模型就行：忽略成本、延迟、容量和协议可靠性。
- Benchmark 榜单能直接替代业务 Eval：错误。
- Context 最大的模型一定更好：错误。
- 每百万 Token 最便宜就最省钱：应看成功任务成本和重试。
- Model Alias 永远不变：错误，生产系统要记录版本与回归。

---

## 16. 面试怎么答

### Q：模型怎么选型？

> 我会先把业务任务定义成可评估指标，再同时比较质量、TTFT/TPOT、Cost、Context、Tool/Structured Output 能力、Multimodal、安全合规和 Provider Capacity。最终看 Cost per Successful Task，而不是只看模型排行榜或 Token 单价；简单任务可以用小模型，复杂任务路由到强模型，但路由本身也要做 Eval 和 Fallback。

### Q：为什么要做 Provider Adapter？

> 为了把业务/Agent Runtime 和厂商 API 字段、Streaming Event、Error、Usage、Tool Call 差异隔离，同时保留 capability flags 避免被最低公约数限制。这样模型替换、Fallback、Telemetry 和测试都更可控。

---

## 17. 自测

<details><summary>1. 为什么 Model Selection 必须先定义 Task Quality？</summary>
因为不同任务成功标准不同，不先定义指标就无法比较模型质量和成本。
</details>

<details><summary>2. 为什么 Adapter 不能只暴露“所有 Provider 都支持的最小集合”？</summary>
会丢失重要厂商能力，因此应有稳定公共核心 + Capability/Extension。
</details>

<details><summary>3. 为什么成本应看 Cost per Successful Task？</summary>
因为低单价模型如果错误率/重试率高，最终完成一个正确任务的总成本可能更高。
</details>
