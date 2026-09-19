# 10｜Timeout、Retry、Failover、Degradation 与 Load Shedding

> **本章定位：System Design 组合层。** 这里把 Deadline、Retry、Failover、Degradation、Load Shedding 组合成系统级 Failure Strategy；这些 Primitive 的完整机制与错误语义回到 [AIBE Timeout / Deadline](../../03-backend-engineering/docs/07-TimeoutDeadline与ErrorTaxonomy.md) 和 [AIBE Retry / Circuit Breaker / Failover](../../03-backend-engineering/docs/08-RetryCircuitBreaker与Failover.md)。

可靠系统不是“所有请求都成功”，而是：

> **在依赖变慢、部分节点故障、流量超载时，系统不会因为自我放大把小故障变成全站级联故障。**

Google SRE 对 Cascading Failure 的核心提醒就是：Overload、Retry 和资源争用会形成正反馈。

---

## 1. Timeout 是资源保护，不只是用户体验

如果没有 Timeout：

```text
Request
→ Slow Dependency
→ Worker / Connection 一直占用
→ Pool Exhaustion
→ 新请求也开始排队
```

所以每个外部调用都应有：

```text
Connect Timeout
Read Timeout
Overall Deadline
```

并和上层 SLO 对齐。

---

# 2. Deadline 要向下传播

假设 API 总预算：

```text
2s
```

不能让：

```text
DB 2s
LLM 10s
Tool 5s
```

各自独立。

更合理：

```text
request_deadline
→ child call receives remaining budget
```

否则上层已经超时，下游还在浪费资源。

---

# 3. Retry 什么时候有效

更适合：

```text
Transient Network Error
503
Connection Reset
Rate Limit with Retry-After
```

不适合：

```text
Invalid Input
Permission Denied
Business Rejection
Permanent Not Found
```

先做 Error Taxonomy，再决定 Retry。

---

# 4. Exponential Backoff + Jitter

如果 10000 个 Client 同时失败后：

```text
1 秒后同时重试
```

会形成同步重试洪峰。

因此常见：

```text
backoff = exponential delay + random jitter
```

目标不是“更慢”，而是：

> **让恢复流量分散，避免再次同时打爆依赖。**

---

# 5. Retry Budget

即使单次请求最多重试 3 次，系统级仍可能放大：

```text
Gateway retry
Service retry
SDK retry
Client retry
```

最坏可能指数放大。

所以要考虑：

```text
Only one layer retries
or
shared retry budget
```

避免多层同时重试。

---

# 6. Circuit Breaker

当依赖明显失败：

```text
Closed
→ failures exceed threshold
→ Open
→ fast fail
→ after cooldown Half-open
→ probe
```

价值：

```text
减少无意义调用
保护线程/连接
给下游恢复时间
```

但 Threshold 配错会误伤，因此不是万能开关。

---

# 7. Failover 不等于没有损失

Primary 故障切到 Replica：

```text
availability ↑
```

但可能面对：

```text
replication lag
recent write loss
cache cold
connection reconnect
route convergence
```

所以 Failover 需要明确：

```text
RTO
RPO
read/write consistency
```

---

# 8. Failure Domain

Google Cloud 的可靠性指南强调：

```text
resource
zone
region
```

可以看成不同 Failure Domain。

如果两份 Replica 都在同一故障域：

```text
同一故障可能一起失效
```

因此冗余必须结合业务 SLO 决定是否跨进程、机器、AZ、Region。

---

# 9. Graceful Degradation

系统过载时不一定要：

```text
100% feature
or
500 error
```

可以：

```text
关闭推荐
降低 Search Candidate
跳过昂贵 Rerank
降级小模型
返回 stale cache
只保核心功能
```

关键是提前定义：

> 哪些功能是 Must-have，哪些是 Best-effort。

---

# 10. Load Shedding

当容量已满，继续接所有请求会导致：

```text
Queue ↑
Latency ↑
Timeout ↑
Retry ↑
Load ↑
→ Cascading Failure
```

更合理是：

```text
reject low-priority / excess traffic early
```

保护一部分请求成功，而不是所有请求一起慢死。

Google SRE 也强调过载后应只接受当前能够处理的工作。

---

# 11. Admission Control

进入昂贵系统前先判断：

```text
quota
concurrency
priority
cost budget
tenant fairness
```

例如 LLM Gateway：

```text
request
→ auth
→ quota
→ concurrency admission
→ model call
```

而不是调用 Provider 后才发现超配额。

---

# 12. Bulkhead / Isolation

如果所有任务共享一个 Worker Pool：

```text
slow video processing
```

可能占满 Pool，让轻量请求也无法执行。

可以按：

```text
workload type
tenant
priority
model
```

分离资源池，降低故障传播。

---

# 13. Recovery 也要限速

依赖恢复后，如果：

```text
积压 Queue
+ Retry
+ Cache Miss
```

瞬间全部恢复流量，可能再次打崩。

所以需要：

```text
ramp-up
warm-up
retry rate limit
queue drain control
```

恢复本身也是一种高峰。

---

# 14. 🎯 面试怎么答

> 我会从 End-to-end Deadline 开始，把剩余时间向下游传播；Retry 只针对 transient error，并用 exponential backoff + jitter，同时防止多层 Retry 放大。依赖持续失败时可以 Circuit Break / Fast Fail。系统进入 Overload 后要优先 Admission Control 和 Load Shedding，而不是让 Queue、Timeout、Retry 形成正反馈。高可用还要按 Failure Domain 设计冗余，并明确 RTO/RPO 和 Failover 后的一致性边界。

---

# 15. 本章自测

<details><summary>1. 为什么 Retry 会导致级联故障？</summary>
下游变慢时重试会增加额外流量，使已经过载的依赖更忙，产生 Timeout→Retry→更高 Load 的正反馈。
</details>

<details><summary>2. 为什么恢复后也需要限速？</summary>
故障期间可能积压大量 Queue、Retry 和 Cache Miss，若一次性放开，会形成恢复洪峰再次击穿依赖。
</details>

<details><summary>3. Failover 为什么还要关心 RPO？</summary>
如果副本存在复制延迟，切换后可能缺少最近写入；RPO 描述可接受的数据损失范围。
</details>
