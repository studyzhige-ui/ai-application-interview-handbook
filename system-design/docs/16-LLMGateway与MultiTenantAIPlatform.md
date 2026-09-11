# 16｜LLM Gateway 与 Multi-tenant AI Platform

这一章对应两个非常典型的 AI-native System Design 场景：

```text
SD-013 Unified Model / LLM Gateway
SD-014 Multi-tenant AI / Agent Platform
```

核心问题是：

> **怎样把多个模型 Provider、多个租户、多个 Agent / Application 接到一个统一入口，同时治理 Routing、Streaming、Quota、Cost、Failover 与权限。**

---

## 1. 为什么需要 LLM Gateway

如果每个业务服务都直接接：

```text
OpenAI
Anthropic
Gemini
Azure
Private Model
```

会重复实现：

```text
Auth
Schema Adapter
Retry
Streaming
Rate Limit
Cost
Logging
Fallback
```

Gateway 的价值是提供稳定内部 Contract。

---

# 2. Gateway 的核心分层

```text
Client / Agent / RAG
        ↓
Unified LLM API
        ↓
Auth / Tenant / Quota
        ↓
Request Normalization
        ↓
Routing Policy
        ↓
Provider Adapter
        ↓
Model Provider
```

横向：

```text
Trace
Cost
Rate Limit
Fallback
Safety Policy
```

---

# 3. Unified Schema 不等于“所有 Provider 都一样”

可以统一：

```text
messages
model capability request
stream
max_tokens
temperature
metadata
```

但 Provider 可能差异：

```text
tool schema
reasoning control
multimodal format
structured output
usage reporting
finish reason
```

所以内部 Contract 要有：

```text
common core
+
capability / provider extension
```

而不是把所有差异硬压平。

---

# 4. Routing Policy

Routing 可以看：

```text
quality
latency
cost
context size
tool calling
multimodal
region / compliance
availability
```

例如：

```text
simple classification → small model
coding → code-capable model
image → multimodal model
provider A 429 → provider B
```

但 Model Switch 可能改变行为，因此不能只看 HTTP Success。

---

# 5. Failover 的语义风险

如果 Provider A 超时后切 B：

```text
Prompt / Tool Schema / Sampling
```

在 B 上不一定完全等价。

所以 Failover 前要定义：

```text
capability compatible?
output schema compatible?
quality acceptable?
```

对于高风险操作，可以宁可失败也不自动换一个行为差异很大的模型。

---

# 6. Streaming Gateway

Streaming 链路：

```text
Provider stream
→ Gateway normalize events
→ Client SSE / WebSocket
```

需要处理：

```text
client disconnect
provider cancel
usage finalization
partial output
trace close
```

不能只把字节透传。

---

# 7. Tenant Quota

多租户 AI Platform 常限制：

```text
requests/min
tokens/min
concurrent runs
monthly cost
specific model access
tool permission
```

Quota 不应只在月底 Billing 发现超支。

应该在 Admission 时判断：

```text
request estimated cost
+ current usage
+ reserved capacity
```

---

# 8. Token Quota 比 QPS 更接近真实成本

两次请求：

```text
Request A: 100 tokens
Request B: 100K tokens
```

都算 1 QPS，但资源成本完全不同。

所以 Gateway 常要统计：

```text
input tokens
output tokens
context size
model
latency
cost
```

并做 per-tenant attribution。

---

# 9. Multi-tenant Resource Isolation

不仅是数据：

```text
Model concurrency
Queue
Agent workers
Vector DB namespace
Redis state
Tool credentials
```

都需要 Tenant Scope。

Noisy Neighbor 可能通过：

```text
huge context
long agent run
expensive tool
```

耗尽共享资源。

---

# 10. Workspace / Permission Model

一个 AI Platform 常有：

```text
Tenant
└─ Workspace
   ├─ Users / Roles
   ├─ Knowledge Base
   ├─ Agent
   ├─ Tool Credential
   └─ Usage / Budget
```

权限至少区分：

```text
view agent
edit prompt
attach knowledge
use tool
approve destructive action
view trace
manage credential
```

不能只做一个 `admin/user`。

---

# 11. Agent Routing

Platform 不一定每个请求都进入同一个 Agent。

可能：

```text
Intent / Policy
→ FAQ workflow
→ RAG agent
→ coding agent
→ human support
```

Routing 本身也需要：

```text
evaluation
fallback
trace
```

而不是让大模型随便选。

---

# 12. Cost Control

可以从：

```text
Model Routing
Context Compression
Cache
Candidate Budget
Max Agent Steps
Tool Budget
Quota
```

共同治理。

如果只在财务账单层面看成本，已经太晚。

---

# 13. Observability

每次调用至少关联：

```text
tenant_id
workspace_id
request_id / run_id
model requested
model routed
provider
latency
TTFT
input/output token
cost
retry/fallback
error
```

Agent 还需要：

```text
step/tool/context/checkpoint trace
```

---

# 14. Security

Gateway 是高价值安全边界：

- Provider Credential 不下发给业务；
- Tenant Model Allowlist；
- PII / Secret Redaction；
- Region / Compliance Routing；
- Prompt / Trace Access Control；
- Tool Credential Scope。

---

# 15. Failure Walkthrough

## Provider 429

→ Queue / Rate Limit / Backoff，不要立即无界 Retry。

## Provider A outage

→ compatible model failover or graceful failure。

## Streaming client disconnect

→ propagate cancel where safe；finalize trace / usage。

## Tenant runaway Agent

→ step/concurrency/cost budget terminates run。

## Usage service temporarily down

→ decide whether fail-open / reserved quota / local buffer；不能默认无限放行。

---

# 16. 真人面经影响

`SD-014` Multi-tenant AI Platform 有 5 个独立来源，`SD-013` LLM Gateway 有 3 个。

因此本章特别强调：

```text
Provider Schema
Routing
Streaming
Rate Limit
Cost
Failover
Tenant Isolation
Agent Routing
```

而不是停在“做一个 OpenAI Proxy”。

---

# 17. 🎯 面试怎么答

> 我会把 LLM Gateway 设计成稳定内部 Contract + Provider Adapter，统一 Auth、Quota、Routing、Streaming、Trace 和 Cost，但保留 Provider Capability 差异。Routing 按 quality/latency/cost/context/tool/multimodal 等约束决策，Failover 也要先验证能力兼容。多租户平台则从 Workspace、Permission、Quota、Credential 和 Resource Isolation 建模，并把 token、concurrency、agent step 和 cost 作为 Admission Control 的一部分，避免 Noisy Neighbor。

---

# 18. 本章自测

<details><summary>1. 为什么 LLM Gateway 不能只统一 HTTP Schema？</summary>
真正复杂的是能力差异、Routing、Quota、Streaming、Error、Cost、Failover 和 Observability，只改字段名无法解决这些问题。
</details>

<details><summary>2. 为什么 Model Failover 可能影响正确性？</summary>
不同模型的 Tool Calling、Structured Output、Context、Safety 和生成行为不完全一致，成功响应不代表业务语义等价。
</details>

<details><summary>3. 为什么 AI Platform 只做 QPS Limit 不够？</summary>
请求成本受 Token、模型、Context、Agent Steps 和 Tool 等影响，同样 QPS 的资源消耗可以相差几个数量级。
</details>
