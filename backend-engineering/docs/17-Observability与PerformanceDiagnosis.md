# 17. Observability、SLO 与 Performance Diagnosis

> Monitoring 告诉你“已知指标是否异常”；Observability 更强调：**面对一个没预先写好 Dashboard 的新问题，能否从系统输出推断内部发生了什么。**

## 1. 三类核心 Signal

OpenTelemetry 的通用模型包括：

```text
Trace
Metric
Log
```

并通过 Context / Baggage 等关联上下文。

三者不是互相替代。

### Metric

适合趋势和告警：

```text
QPS
error_rate
P95 / P99
queue_depth
pool_utilization
```

### Log

适合离散事件与上下文：

```text
request failed
worker reclaimed task
cache invalidation failed
```

### Trace

适合跨服务时序和依赖定位：

```text
Gateway
→ API
→ Retrieval
→ LLM
→ Tool
```

---

## 2. Structured Logging

不要：

```text
something failed
```

更好：

```json
{
  "level": "ERROR",
  "request_id": "req_123",
  "tenant_id": "t_9",
  "task_id": "job_42",
  "error_type": "PROVIDER_TIMEOUT",
  "provider": "x",
  "latency_ms": 3200
}
```

关键是字段可以检索和聚合。

---

## 3. Request ID vs Trace ID

### Request ID

应用级一次入口请求的相关标识。

### Trace ID

分布式 Trace 的全链路标识。

一个用户动作也可能触发多个异步 Task，所以还可能有：

```text
run_id
task_id
message_id
```

不要把所有 ID 混成一个字符串。

---

## 4. Span

Trace 由 Span 组成：

```text
HTTP request span
├─ auth span
├─ DB span
├─ retrieval span
├─ LLM span
└─ tool span
```

每个 Span 可记录：

- start / end；
- status；
- attributes；
- events；
- parent-child relationship。

这样才能做 Bottleneck Attribution。

---

## 5. Metrics：平均值为什么不够

平均延迟 200ms 可能掩盖：

```text
95% = 50ms
5% = 3s
```

用户对尾延迟更敏感。

所以常看：

```text
P50
P95
P99
```

尤其 AI Service 长尾明显。

---

## 6. RED / USE 思想

服务入口常看 RED：

```text
Rate
Errors
Duration
```

资源常看 USE：

```text
Utilization
Saturation
Errors
```

例如 DB Pool：

```text
utilization = active / max
saturation = acquire wait / queue
errors = acquire timeout
```

---

## 7. AI-specific Metrics

除了普通 Backend：

```text
TTFT
TPOT / stream rate
input_tokens
output_tokens
model_cost
retrieval_latency
rerank_latency
tool_latency
agent_steps
```

还要记录版本：

```text
model_version
prompt_version
retrieval_version
agent_version
```

否则 Bad Case 无法复现。

---

## 8. SLI / SLO

### SLI

实际测量指标：

```text
request success rate
P95 latency
freshness lag
```

### SLO

期望目标：

```text
99.9% requests success
95% chat requests TTFT < 2s
```

SLO 帮助回答：

> 什么时候系统算“够好”？

没有目标的指标只是数据。

---

## 9. Error Budget

如果 SLO 是 99.9%，就允许有限失败窗口。

Error Budget 的工程意义是平衡：

```text
reliability
vs
release velocity
```

当预算消耗过快：

- 降低发布频率；
- 修可靠性；
- 限制高风险 Feature。

---

## 10. Performance Diagnosis：从总延迟拆阶段

不要看到：

```text
P99 = 8s
```

就说“模型慢”。

拆：

```text
Gateway        30ms
Queue Wait    900ms
DB             50ms
Retrieval     300ms
Rerank        500ms
LLM TTFT     1800ms
LLM stream   4000ms
Serialize      20ms
```

根因可能是 Queue，而不是模型。

---

## 11. Pool / Queue / Downstream 联动

典型 Timeline：

```text
DB latency ↑
→ connection hold time ↑
→ pool utilization ↑
→ acquire wait ↑
→ request P99 ↑
```

如果只看 API P99，无法知道原因。

所以 Metrics 设计必须覆盖关键资源。

---

## 12. Distributed Trace 的 Context Propagation

跨 HTTP/RPC：

```text
trace context header
→ downstream span
```

跨 MQ：

```text
message metadata
→ consumer creates child / linked span
```

如果 Trace Context 不传播，异步链会断掉。

---

## 13. Sampling

全量 Trace 可能成本太高。

可以：

- head sampling；
- tail sampling；
- error-biased sampling；
- tenant / route sampling。

但不要把所有异常都采样掉。

Production 调试最有价值的往往正是高延迟和失败 Trace。

---

## 14. Log 中不能放什么

禁止或谨慎：

- Password；
- Access Token；
- API Key；
- Secret；
- 完整隐私数据；
- 敏感 Prompt / Tool Payload。

Observability 不能成为数据泄漏通道。

---

## 15. Performance Regression

上线新版本后：

```text
P99 1.5s → 4s
```

诊断：

```text
compare version tag
↓
trace stage breakdown
↓
queue/pool/resource
↓
new code path
↓
rollback / fix
```

所以所有 Telemetry 最好带：

```text
service_version
config_version
model_version
```

---

## 16. AI Bad Case 与 Backend Trace

用户说“回答质量变差”时，可能是：

- retrieval stale；
- model fallback；
- timeout 导致 skip rerank；
- tool failure；
- context truncated；
- degraded mode。

因此 AI Evaluation 与 Backend Observability 必须能关联同一个 `run_id / trace_id`。

---

## 17. 🎯 面试怎么答

**问：线上接口突然变慢怎么排查？**

可以回答：

> 先确认是整体还是某 Route/Tenant/Version，再看 P50/P95/P99、Error Rate 和 QPS；随后用 Trace 拆 Gateway、Queue、DB、Cache、Retrieval、Model、Tool 各阶段。同步检查 Pool Utilization、Queue Depth、CPU/Memory、Downstream Latency 和 Retry Rate。最后结合版本/配置变更定位 Regression，而不是只盯应用 CPU。

---

## 18. ⚠️ 易错点

- Log 多 ≠ Observability 好；
- Average Latency ≠ 用户体验；
- Trace ID ≠ Task ID；
- SLO ≠ 所有请求必须 100% 成功；
- Sampling ≠ 随便丢数据；
- AI Quality Bad Case 不一定是模型问题。

---

## 19. 本章自测

<details>
<summary>1. Metrics、Logs、Traces 分别最擅长什么？</summary>

Metrics 看趋势和告警；Logs 看离散事件细节；Traces 看一次请求跨组件的时序与依赖。三者通过 Context 关联才能高效排障。

</details>

<details>
<summary>2. 为什么必须监控 Queue Wait 和 Pool Acquire Wait？</summary>

很多长尾延迟来自任务开始执行前的等待。如果只看 DB/Model 执行时间，会错过真正的 Saturation 点。

</details>

<details>
<summary>3. AI Service 为什么要记录 model/prompt/retrieval version？</summary>

没有版本信息就无法复现历史 Bad Case，也无法判断质量/延迟 Regression 是否由 Model、Prompt 或 Retrieval 变更引起。

</details>
