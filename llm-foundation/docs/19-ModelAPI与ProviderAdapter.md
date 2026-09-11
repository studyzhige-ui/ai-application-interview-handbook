# 19｜Messages、Role、Model API 与 Provider Adapter

## 1. 为什么 Model API 也值得单独学

很多人第一次接触 LLM 是：

```python
client.chat(...)
```

于是容易把“模型能力”和“某家 API 格式”混在一起。

真正稳定的知识应该是：

```text
Application Message Model
→ Provider Adapter
→ Provider-specific Request
→ Model
→ Provider-specific Response
→ Normalized Response
```

这样换模型、换 Provider、接自部署 Serving 时才不会把业务代码绑死。

---

## 2. Chat API 的核心语义

常见抽象包括：

```text
model
messages / input
role
content
max output
sampling
structured output
streaming
usage
```

不同 Provider 字段名、能力和限制可能变化，但应用层通常都要表达这些概念。

---

## 3. Role 到底是什么

典型角色可能有：

```text
system / developer
user
assistant
```

工具调用系统还可能包含 Tool Message。

重要的是：

> Role 是对不同来源和优先级信息的结构化表达，不等于模型内部真的存在三段完全隔离的“内存”。

最终 Provider 会把这些消息按模型对应模板序列化成 Token 序列。

---

## 4. Chat Template

同样的：

```text
system
user
assistant
```

不同模型可能需要不同特殊 Token 和格式。

因此应用不要自己假设：

```text
"System: ... User: ... Assistant: ..."
```

永远等价于官方 Chat Template。

自部署开源模型时尤其要使用模型匹配的 Template。

---

## 5. Provider Adapter 为什么重要

如果业务代码到处写：

```text
OpenAI field A
Provider B field C
Provider C error code D
```

后面很难切换。

可以抽象：

```text
LLMRequest
├─ messages
├─ model
├─ temperature
├─ max_tokens
├─ response_schema
└─ stream

LLMResponse
├─ text
├─ tool_calls
├─ finish_reason
├─ usage
└─ provider_metadata
```

Adapter 再负责映射各家 API。

---

## 6. 不要过度抽象

不同 Provider 真的可能有不同能力：

- Structured Output；
- Prompt Cache；
- Reasoning Effort；
- Tool Calling；
- Context Length；
- Multimodal Input；
- Logprobs；
- Batch API。

如果强行只取最小公共子集，会丢失重要能力。

更合理的是：

```text
Common Core
+
Provider Capabilities
```

---

## 7. Streaming Response

Provider Streaming 往往返回增量事件：

```text
text delta
reasoning / metadata delta
usage
finish
error
```

应用 Backend 再转换成 SSE / WebSocket 给客户端。

需要区分：

```text
Model Provider Stream
≠
Client Transport Protocol
```

后者属于 FastAPI / Backend。

---

## 8. Structured Output

Production 不应该只写 Prompt：

> “请一定输出合法 JSON。”

更可靠方式包括：

- Provider Schema；
- Grammar-constrained decoding；
- JSON Schema；
- Application Validation；
- Retry / Repair。

即使 Provider 声称 Structured Output，也仍需要验证业务语义。

---

## 9. Usage 与 Cost Accounting

Adapter 最好统一保留：

```text
input_tokens
output_tokens
cached_tokens
model
provider
request_id
latency
finish_reason
```

因为后面：

- Billing；
- Cost Attribution；
- Trace；
- Evaluation；
- Model Routing；

都需要这些信息。

---

## 10. 🎯 面试怎么回答

> 我会把 Model API 分成稳定应用语义和 Provider-specific 能力两层。上层统一 Message、Model、Sampling、Structured Output、Streaming 和 Usage；下层 Provider Adapter 负责不同 API 格式、错误码和能力映射。同时不会过度抽象掉各 Provider 的独特能力。这样业务代码能切换模型，又能保留 Prompt Cache、Tool Calling 等差异化特性。

---

## 11. ⚠️ 易错点

错误：

> Chat Messages 就是直接字符串拼接。

错误：

> 有统一 Adapter 后所有模型行为就一致。

Adapter 只能统一接口，不能统一模型能力。

---

<details>
<summary>自测：为什么 Provider Adapter 既不能太少，也不能太抽象？</summary>

不做 Adapter 会让业务代码绑死具体 Provider；但只保留最小公共子集又会丢掉 Structured Output、Prompt Cache、Reasoning 等关键差异化能力。因此通常需要 Common Core + Capability Extension。

</details>
