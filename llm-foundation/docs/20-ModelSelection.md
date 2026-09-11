# 20｜Model Selection：效果、Latency、Cost、Context 与风险

## 1. 选模型不是“谁榜单最高就用谁”

真实业务里，模型选型至少是一个多目标优化问题：

```text
Quality
Latency
Cost
Context
Tool Calling
Structured Output
Multimodal
Safety / Compliance
Availability
Provider Risk
```

最终目标不是“最强模型”，而是：

> **在目标任务、SLA 和预算下，选择最合适的模型。**

---

## 2. 先定义任务，再选模型

如果任务不同，最优模型可能完全不同。

### 信息抽取

重点：

- 稳定；
- Schema 遵循；
- 低成本；
- 高吞吐。

### Complex Reasoning

重点：

- 推理质量；
- 长上下文；
- 错误率。

### Coding Agent

重点：

- Repo Understanding；
- Tool Calling；
- Patch Quality；
- Long-running Reliability。

### Multimodal

还要看：

- Image / Audio / Video 输入；
- OCR；
- Visual Reasoning。

---

## 3. Model Size 不是唯一能力指标

参数更多常常意味着更强容量，但不能简单写成：

```text
参数更多 = 所有任务都更好
```

还要看：

- Training Data；
- Post-training；
- Architecture；
- Tool Calling 训练；
- Domain Specialization；
- Inference-time Reasoning；
- Context Training。

所以选型必须做任务级 Evaluation。

---

## 4. Context Window 也不是越大越好

更大的 Context 可能带来：

- 更高 Prefill 成本；
- 更大 KV Cache；
- 更高延迟；
- 更复杂的信息利用问题。

如果业务只需要 8k，有 1M Context 并不会自动产生价值。

---

## 5. Tool Calling / Structured Output

Agent / Workflow 场景还要验证：

```text
Tool Selection Accuracy
Argument Correctness
Schema Compliance
Invalid Call Rate
Recovery after Tool Error
```

一个聊天能力很强的模型，不一定就是 Tool Runtime 最稳定的模型。

---

## 6. Cost 不能只看单价

真实成本可能是：

```text
Token Price
× Token Volume
× Retry Rate
× Number of Calls
+ RAG / Tool / Backend Cost
```

如果更便宜的模型导致：

- 更多重试；
- 更长输出；
- 更低任务成功率；

端到端成本未必低。

---

## 7. Latency 也要拆

同一个模型可能：

```text
TTFT 很快
但 TPOT 很慢
```

或反过来。

对于客服 Chat，TTFT 可能最重要；对于离线报告，Throughput 更重要。

因此选型要按业务体验指标，而不是只看公开 benchmark。

---

## 8. Routing

Production 常见做法不是“一套系统一个模型”，而是按任务路由：

```text
Classification → Small Model
Simple QA      → Medium Model
Hard Reasoning → Strong Model
Fallback       → Backup Provider
```

但完整 Model Routing Runtime 还涉及：

- Failure；
- Fallback；
- Cost Budget；
- Evaluation；

在 Agent / System Design 再深化。

---

## 9. 怎样做 Evaluation

建立代表真实流量的数据集：

```text
Easy
Medium
Hard
Long Context
Tool Call
Structured Output
Safety Edge Cases
```

至少比较：

- Task Success；
- Accuracy / Judge Score；
- Tool Accuracy；
- Latency；
- Cost；
- Failure Rate。

不能只测 10 个“看起来不错”的 Demo。

---

## 10. 版本升级风险

Provider 更新模型版本后，可能发生：

- Prompt 行为变化；
- Structured Output 差异；
- Tool Selection 变化；
- Safety Policy 变化；
- Cost / Latency 变化。

所以模型升级也需要 Regression。

---

## 11. 🎯 面试怎么回答

> 模型选型我不会只看参数量或公开榜单，而会先定义业务任务和 SLA，再用真实 Evaluation Set 比较任务成功率、Tool / Structured Output 稳定性、Context、TTFT / TPOT、成本和 Provider 可靠性。如果不同任务差异大，可以做分层 Model Routing。最终目标是业务质量、延迟和成本的 Pareto 最优，而不是统一使用最强模型。

---

## 12. ⚠️ 易错点

错误：

> 最大模型一定最好。

错误：

> Context 最大的模型一定最适合 RAG。

错误：

> 只看 API 单价就能比较成本。

---

<details>
<summary>自测：为什么一个更贵的模型有时反而端到端成本更低？</summary>

如果它任务成功率更高、调用次数更少、重试更少、输出更短，最终每个成功任务的总成本可能低于便宜但不稳定的模型。

</details>
