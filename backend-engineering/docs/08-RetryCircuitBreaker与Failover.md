# 08. Retry、Backoff、Circuit Breaker、Degradation 与 Failover

> Retry 是最容易被误用的“可靠性机制”：**它既能恢复瞬时错误，也能把一个小故障放大成全站雪崩。**

## 1. 先问：这个错误值得 Retry 吗

不是所有失败都应该 Retry。

### 可能适合 Retry

- transient network error；
- temporary 503；
- provider overload；
- leader election 短暂切换；
- connection reset。

### 通常不应该 Retry

- invalid schema；
- permission denied；
- business rejection；
- unsupported model；
- malformed tool input。

Retry 的第一步不是写循环，而是先做 Error Taxonomy。

---

## 2. 为什么立即 Retry 很危险

下游已经过载：

```text
capacity = 1000 QPS
incoming = 1100 QPS
```

如果失败的 100 QPS 立即重试：

```text
load = 1200 QPS
```

更多失败继续 Retry：

```text
1200 → 1300 → 1400...
```

这就是 Retry Amplification。

Google SRE 的经验强调：Retry 可以直接放大 Overload，并触发 Cascading Failure。

---

## 3. Exponential Backoff

基本思路：

```text
attempt 1 → wait 100ms
attempt 2 → wait 200ms
attempt 3 → wait 400ms
...
```

目的：

> 给下游恢复时间，而不是持续轰炸。

但如果所有 Client 同时失败，它们仍可能在 100ms、200ms、400ms 时一起重试。

所以还需要 Jitter。

---

## 4. Jitter

把固定等待随机化：

```text
0 ~ 100ms
0 ~ 200ms
0 ~ 400ms
```

这样可以打散同步重试波峰。

AWS 的经典 Backoff + Jitter 资料就是在解决这一类同步竞争问题。

---

## 5. Retry Budget

即使每个请求只 Retry 3 次，系统整体仍可能产生大量额外流量。

因此成熟系统会考虑：

```text
Per-request attempt limit
+ Process / Service-wide retry budget
```

例如：

```text
正常 QPS = 1000
最多额外 10% retry traffic
```

Budget 用完就 Fail Fast / Degrade。

---

## 6. 只在一层 Retry

深调用链：

```text
Client
→ Gateway
→ Service A
→ Service B
→ DB
```

如果每层都 Retry 3 次：

```text
一次用户请求
可能被放大成多层乘法尝试
```

Google SRE 特别强调避免多层重复 Retry。

更合理：明确哪一层负责 Retry，并向上游返回清晰的 retriable / non-retriable 语义。

---

## 7. Retry 必须和 Idempotency 配合

对 GET 类无副作用操作，Retry 较简单。

对：

```text
create order
send email
charge money
modify file
execute tool
```

Retry 可能产生重复副作用。

因此：

```text
Retry Safety
= Error is retryable
+ Operation is idempotent or deduplicated
```

下一章会专门讲。

---

## 8. Circuit Breaker

当下游持续失败，继续发送请求没有意义。

经典状态：

```text
Closed
→ failures exceed threshold
→ Open
→ wait cooldown
→ Half-open probe
→ success → Closed
→ failure → Open
```

### Closed

正常放行。

### Open

快速失败，避免继续消耗下游和本地资源。

### Half-open

允许少量探测请求判断是否恢复。

---

## 9. Circuit Breaker 不是万能

如果错误原因是：

```text
all requests malformed
```

Circuit Breaker 没意义。

如果下游只是部分 Tenant / Region 故障，也需要更细粒度隔离。

Breaker 的 Key 可能按：

```text
provider
region
model
endpoint
```

而不是整个服务只有一个总开关。

---

## 10. Degradation

当完整能力不可用，提供更便宜或更简单的结果。

AI 例子：

```text
GPT-large → smaller model
RAG + rerank → retrieval only
agent → direct answer
live search → cached result
multi-tool → core tool only
```

降级需要提前定义 Quality Floor。

否则“降级”可能只是默默返回错误结果。

---

## 11. Fallback

Fallback 是替代路径：

```text
Primary Model
→ fail
→ Backup Model
```

它和 Retry 不同：

- Retry：再试同一个操作；
- Fallback：换一条执行路径。

Fallback 也可能失败，而且可能出现：

- schema 不兼容；
- quality 差异；
- cost 差异；
- semantic drift。

因此必须测试。

---

## 12. Failover

基础设施层 Failover：

```text
Region A
→ unavailable
→ Region B
```

Data Service：

```text
Primary
→ fail
→ Replica promoted
```

AI Provider：

```text
Provider A
→ timeout / outage
→ Provider B
```

关键不是“有备份”，而是：

```text
state compatibility
routing
health detection
capacity of backup
consistency
```

备份平时没有真实流量，故障时可能承受不了全部流量。

---

## 13. Hedged Request

对少量幂等 Read 请求，有些系统会：

```text
request A
→ too slow
→ request B to another replica
→ first success wins
```

可以降低长尾，但会增加额外负载。

不应该在已过载系统里无脑使用。

---

## 14. AI Provider Failure Chain

```text
Provider latency ↑
→ local requests accumulate
→ timeout ↑
→ retry ↑
→ provider load ↑
→ more timeout
```

更成熟的应对：

```text
deadline
→ retry budget
→ backoff + jitter
→ circuit open
→ fallback model
→ load shed / degrade
```

---

## 15. Metrics

至少观察：

```text
attempt_count
retry_rate
retry_success_rate
retry_budget_exhausted
circuit_state
fallback_rate
degradation_rate
provider_error_by_category
```

如果只看最终 Error Rate，会看不到系统是否靠大量 Retry 勉强维持成功率。

---

## 16. 🎯 面试怎么答

**问：Retry、Circuit Breaker、Fallback 有什么区别？**

可以回答：

> Retry 是对同一路径再次尝试，适合短暂错误，但需要 Backoff/Jitter/Budget 并确保幂等；Circuit Breaker 是当下游持续失败时快速停止调用，保护双方资源；Fallback 是切换到替代实现或降级路径。三者解决的阶段不同，通常组合使用，而不是互相替代。

---

## 17. ⚠️ 易错点

- Retry 次数有限 ≠ 没有 Retry Storm；
- Backoff 没 Jitter ≠ 足够；
- Circuit Open ≠ 下游恢复；
- Fallback ≠ 同等质量；
- Failover ≠ Backup Capacity 一定够；
- 非幂等副作用不能只靠 Retry。

---

## 18. 本章自测

<details>
<summary>1. 为什么多层 Retry 会造成乘法放大？</summary>

每一层都可能对下层做多次尝试，上层又把下层整组失败再次 Retry。多个 attempt 数相乘后，一个用户请求可能转化成几十次底层调用。

</details>

<details>
<summary>2. Circuit Breaker Open 状态的核心价值是什么？</summary>

快速失败，避免继续把已经没有成功可能的请求送给故障下游，同时释放本地线程、连接和 Deadline 预算。

</details>

<details>
<summary>3. Fallback Model 为什么需要单独评测？</summary>

模型能力、输出 Schema、成本、延迟和行为都可能不同。Failover 成功不代表业务语义仍正确，因此要做兼容与质量验证。

</details>
