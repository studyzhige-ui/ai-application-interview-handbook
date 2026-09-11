# 07. Timeout、Deadline 与 Error Taxonomy

> Timeout 不是“防止请求卡死”的一个数字，而是分布式系统里**资源预算与错误语义**的一部分。

## 1. 为什么所有远程调用都需要 Timeout

没有 Timeout：

```text
request
→ downstream hangs
→ connection occupied
→ coroutine/thread occupied
→ pool fills
→ upstream queue grows
```

一个缓慢依赖可以拖垮整个服务。

所以 Production Remote Call 应默认假设：

> 对方可能永远不返回。

---

## 2. Timeout 有很多层

常见：

```text
connect timeout
pool acquire timeout
read timeout
write timeout
request timeout
end-to-end deadline
```

### Connect Timeout

连接最多建立多久。

### Read Timeout

等待下一段数据多久。

Streaming 里它通常不是“整条 Stream 最多多久”。

### Pool Acquire Timeout

等空闲连接最多多久。

### End-to-End Deadline

用户愿意为整个业务请求等多久。

---

## 3. Timeout vs Deadline

Timeout 常表示：

```text
这个操作从现在起最多执行 2 秒
```

Deadline 表示：

```text
整个请求必须在 18:00:10 之前完成
```

分布式调用链更适合传播 Deadline。

例如总 Deadline 3s：

```text
Gateway 用掉 200ms
Service A 用掉 500ms
剩余 2.3s
↓
Service B 不应该再拿完整 3s
```

否则每一层各自 3s，最终总时延可能远超用户预算。

---

## 4. Timeout Budget

一个请求：

```text
Auth        100ms
Redis        50ms
Retrieval   400ms
LLM        1800ms
Serialize    50ms
Safety      100ms
```

不能简单把所有阶段都设置为 3 秒。

需要：

```text
End-to-End Budget
→ 分配到各 Downstream
→ 保留网络/调度余量
```

---

## 5. Streaming 的 Timeout 更复杂

LLM Stream 可能：

```text
TTFT = 800ms
then one chunk every 100ms
stream total = 30s
```

如果把 2s 当整个 Request Timeout，会错误取消正常 Stream。

通常要区分：

```text
connect timeout
first-byte / TTFT budget
idle read timeout
overall run deadline
```

---

## 6. Error Taxonomy 为什么比 Exception 名字重要

Backend 需要按“处理策略”分类错误。

### Transient

暂时错误：

- network reset；
- overload；
- 503；
- temporary broker unavailable。

可能 Retry。

### Permanent

持续重试也不会变好：

- invalid request；
- unsupported operation；
- invalid schema。

不要 Retry。

### Permission / Auth

- 401；
- 403；
- scope denied。

通常需要重新认证或拒绝，不应该自动反复重试。

### Business Rejection

例如：

```text
insufficient balance
order already closed
approval required
```

这不是 Infrastructure Error。

### Rate Limit / Overload

429 / 503 可能允许重试，但必须结合 Backoff / Retry-After / Budget。

---

## 7. Unknown Outcome

最危险的一类：

```text
Client request sent
↓
Server may have completed side effect
↓
connection lost
↓
Client timeout
```

调用方不知道：

```text
没执行？
执行一半？
执行成功但响应丢了？
```

这就是 Idempotency 必须存在的原因。

---

## 8. Timeout 不等于 Cancellation

调用方停止等待：

```text
client timeout
```

不代表下游工作一定停止。

可能：

```text
DB query continues
LLM generation continues
payment completes
worker continues
```

如果副作用重要，必须额外设计：

- Cancellation Propagation；
- Idempotency；
- Status Query；
- Reconciliation。

---

## 9. Timeout 过短也会制造事故

假设服务正常 P99 800ms，却设置：

```text
timeout = 500ms
```

会产生大量假失败：

```text
cancel / retry
→ more load
→ latency increases
→ more timeout
```

Timeout 必须基于真实 latency distribution，而不是拍脑袋。

---

## 10. Timeout 过长的代价

如果 Timeout 60s：

- Connection 持有更久；
- Queue 回收更慢；
- 用户等太久；
- Retry / Failover 太晚；
- 故障扩散时间更长。

所以 Timeout 是资源回收策略的一部分。

---

## 11. Error Contract

服务间不应该只返回：

```json
{"error": "failed"}
```

至少要能区分：

```text
code
category
retryable?
http/rpc status
request_id / trace_id
safe message
```

例如：

```json
{
  "code": "PROVIDER_OVERLOADED",
  "retryable": true,
  "request_id": "req_123"
}
```

这样上游才能做正确策略。

---

## 12. AI 场景：RAG 请求预算

```text
Client Deadline 4s
↓
Query Rewrite 300ms
Retrieval 500ms
Rerank 500ms
LLM first token 2s
Reserve 700ms
```

如果 Retrieval 已经耗了 3 秒，继续完整 Rerank + Large Model 可能不再有意义。

可以根据剩余 Budget 做：

- skip rerank；
- smaller model；
- cached result；
- partial answer。

---

## 13. Metrics

重点看：

```text
timeout_rate
connect_timeout_rate
pool_acquire_timeout
read_timeout
remaining_deadline
cancel_rate
late_completion
```

Late Completion 很重要：请求已经超时，但下游仍完成了副作用。

---

## 14. 🎯 面试怎么答

**问：为什么需要 Deadline，而不只是每个调用一个 Timeout？**

可以回答：

> 多层服务如果每一层都拿自己的完整 Timeout，会让总时延不断叠加。Deadline 表示整个用户请求的绝对时间预算，向下游传播后每一层只能使用剩余预算。这样可以避免请求已经没有业务价值还继续占资源，也方便做降级或 Fail Fast。

---

## 15. ⚠️ 易错点

- Timeout ≠ Cancellation；
- 429/503 ≠ 一定可以立即 Retry；
- Business Reject ≠ Infrastructure Failure；
- Streaming Read Timeout ≠ 整条 Stream 总时长；
- 每层 3s Timeout ≠ 全链路 3s。

---

## 16. 本章自测

<details>
<summary>1. 什么是 Unknown Outcome？</summary>

调用方超时或断连后，无法确定服务端副作用是否已经执行。它是重复执行风险的根源之一，需要 Idempotency / Status Query / Reconciliation 等机制解决。

</details>

<details>
<summary>2. 为什么 Timeout 太短会造成雪崩？</summary>

正常慢请求会被误判失败，触发取消和重试，增加系统负载；负载增加又进一步拉高延迟和超时率，形成正反馈。

</details>

<details>
<summary>3. Streaming 为什么需要区分 TTFT / Idle / Overall Deadline？</summary>

模型首 Token、连续流式间隔和整条任务总时长是不同阶段。用一个统一短 Timeout 会误杀正常 Stream，而完全没有 Overall Deadline 又会失去资源边界。

</details>