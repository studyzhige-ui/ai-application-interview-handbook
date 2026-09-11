# 37｜Intent Recognition 与 Capability Routing

## 1. Routing 不只有“选哪个 Agent”

一个请求可能先判断：

```text
普通聊天？
RAG？
需要写代码？
需要高风险 Tool？
需要人工澄清？
```

Routing 决定接下来暴露什么 capability / policy / model。

## 2. 实现层级

从简单到复杂：

```text
rules
keyword / metadata
small classifier
embedding
LLM classification
agentic discovery
```

不应默认用最大模型做每次 routing。

## 3. Router Output

最好结构化：

```json
{
  "route":"repo_agent",
  "confidence":0.86,
  "required_capabilities":["read_repo","test"]
}
```

低置信时可以 ask clarification。

## 4. Routing Eval

需要真实 request dataset，评估：

```text
route accuracy
false high-risk route
latency
cost
fallback rate
```

HUMAN-A 中 Intent Recognition / Routing 已形成独立能力信号，所以这一章不仅是系统设计附录。

## 🎯 面试

Routing 的目标是把 request 映射到 capability/policy/model，而不是无脑选一个 Agent。我会先用最简单可靠的方法，低置信时澄清，并用真实流量评测 route accuracy 和高风险误路由。

<details><summary>自测：为什么 Router 也可能成为单点故障？</summary>

如果第一步误判导致正确 Tool/Agent 根本不可见，后续再强也难恢复；因此需要 fallback 与 eval。
</details>
