# 09. Production API、Idempotency 与 Side Effect Safety

> Production API 最危险的不是“返回 500”，而是**调用方不知道到底执行没执行，于是 Retry 以后把副作用做了两次。**

## 1. 先区分 Read 与 Side Effect

Read：

```text
GET user profile
query order
retrieve document
```

重复执行通常问题较小。

Side Effect：

```text
create order
charge card
send email
create ticket
modify file
invoke tool
```

重复执行可能造成真实损失。

---

## 2. HTTP Method 的 Idempotent 语义

从协议语义看，某些 Method 设计为幂等，例如 GET / PUT / DELETE；POST 通常不保证。

但：

> HTTP Method 的规范语义不等于你的业务实现自动安全。

例如 DELETE 如果同时“扣积分”就破坏了预期语义。

API 设计必须让 Method 与业务行为匹配。

---

## 3. Idempotency 的核心定义

对同一个**业务操作**重复提交多次，最终效果与执行一次相同。

注意不是：

> “重复请求永远返回 200”。

而是：

```text
same logical operation
→ only one side effect
```

---

## 4. Idempotency Key

Client 为一个逻辑操作生成稳定 Key：

```text
Idempotency-Key: 8a0e...
```

Server 记录：

```text
key
request fingerprint
status
result
created_at
```

重复请求：

```text
same key + same request
→ return saved / current result
```

Stripe 的 API 是成熟实践之一：同一个 Idempotency Key 用于安全重试，并校验重复 Key 的参数一致性。

但具体保留时间等是产品策略，不能当成所有系统通用标准。

---

## 5. 为什么要校验 Request Fingerprint

错误场景：

```text
Key = abc
Request 1: charge $10
Request 2: charge $100
```

如果只按 Key 去重，第二个请求可能错误复用第一个结果。

所以通常需要比较：

```text
operation
resource
critical parameters
```

同 Key 不同参数应拒绝。

---

## 6. Idempotency Record 的状态机

不要只有：

```text
key exists / not exists
```

更完整：

```text
RECEIVED
→ PROCESSING
→ SUCCEEDED
→ FAILED_RETRYABLE / FAILED_FINAL
```

如果 Worker Crash 在 PROCESSING：

```text
下一次请求
→ 判断 Lease / timeout
→ reclaim or inspect side effect
```

否则可能永远卡住。

---

## 7. Idempotency 与并发重复请求

两个相同请求同时到达：

```text
A ---->
B ---->
```

如果都是：

```python
if not exists(key):
    execute()
```

会 Race。

需要原子 Claim：

```text
unique constraint
transaction
atomic insert
CAS
```

谁成功创建 Idempotency Record，谁获得执行权。

---

## 8. Exactly-once 为什么很难

跨网络、跨 DB、跨 MQ 时：

```text
execute side effect
→ persist dedupe state
```

两个步骤之间可能 Crash。

反过来：

```text
persist done
→ side effect
```

也可能 Crash。

因此现实系统常采用：

```text
at-least-once delivery
+ idempotent consumer
+ reconciliation
```

而不是宣称“真正 Exactly Once Everything”。

某些系统能在特定边界内提供 exactly-once semantics，但不能把局部语义推广成整个跨系统业务链的绝对保证。

---

## 9. Unknown Outcome 的处理

例如支付：

```text
request sent
→ timeout
```

不能立即假设失败。

更安全：

```text
query operation status by idempotency key / order id
→ if completed: reuse result
→ if not started: retry
→ if uncertain: reconcile
```

这也是为什么“查询接口”很重要。

---

## 10. Idempotency Key 谁生成

### Client-generated

适合用户操作：

```text
Create Order
```

Client Retry 时保持 Key。

### Server-generated Operation ID

适合系统先创建 Task：

```text
POST /jobs
→ job_id
```

后续所有执行围绕同一个 `job_id`。

不要每次 Retry 重新生成新 ID，否则服务端无法判断是同一逻辑操作。

---

## 11. API Versioning

Production API 会演进。

要考虑：

- Path / Header Version；
- Backward Compatibility；
- Schema Additive Change；
- Deprecation；
- Client Rollout；
- Event Schema Version。

不要一看到字段变化就做 `/v2`，但也不能无限破坏旧客户端。

---

## 12. Error Contract 与 Idempotency

重复请求如果第一次结果未知：

Server 最好能够返回：

```text
processing
succeeded
failed final
conflict
```

而不是每次都重新执行。

例如：

```json
{
  "operation_id": "op_123",
  "status": "processing"
}
```

---

## 13. Agent Tool Side Effect

Agent Tool 调用：

```text
send_email(to, content)
```

模型可能：

- Retry；
- Loop；
- Resume；
- duplicate tool call；
- timeout 后再调用。

Tool Runtime 应传递稳定 Operation Key：

```text
run_id + step_id + tool_call_id
```

后端再把它映射成业务幂等语义。

这与 Agent Harness 的 Tool Side Effect / Checkpoint 对接。

---

## 14. Idempotency 和 Distributed Lock 的区别

Lock：

```text
同一时刻谁能执行
```

Idempotency：

```text
同一个逻辑操作重复到来是否会产生重复效果
```

拿锁以后执行两次，仍可能重复副作用。

所以 Lock 不能替代 Idempotency。

---

## 15. Result Retention

Idempotency Record 不可能永远保存。

需要定义：

```text
业务重复窗口
数据保留期
存储成本
Key reuse rule
```

如果记录已经过期，再次收到旧 Key，要有清晰语义。

---

## 16. Metrics

```text
idempotency_hit_rate
in_progress_conflict
duplicate_prevented
unknown_outcome_count
reconciliation_needed
operation_latency
```

这些指标能直接反映 Retry 是否在产生重复风险。

---

## 17. 🎯 面试怎么答

**问：如何保证一个 POST 请求 Retry 时不重复下单？**

可以回答：

> Client 为一个逻辑下单操作使用稳定 Idempotency Key。Server 用唯一约束或原子写入 Claim 这个 Key，并保存请求指纹、执行状态和结果。重复 Key 且参数一致时复用原结果或返回当前状态，不再次执行副作用。还要处理执行成功但响应丢失、PROCESSING 时进程崩溃等 Unknown Outcome，通过状态查询、Lease 和 Reconciliation 恢复。

---

## 18. ⚠️ 易错点

- POST ≠ 天生不可能幂等；
- Lock ≠ Idempotency；
- Unique ID ≠ Idempotency Key；
- 同 Key 不校验参数有风险；
- Retry 生成新 Key 会破坏幂等；
- Exactly-once 不能轻易跨系统承诺。

---

## 19. 本章自测

<details>
<summary>1. 为什么 Idempotency Record 需要 PROCESSING 状态？</summary>

因为并发重复请求可能在第一个请求尚未完成时到达；状态机可以区分“已经成功”和“正在执行”，并支持 Crash 后 Reclaim / Reconciliation。

</details>

<details>
<summary>2. 为什么 Distributed Lock 不能替代 Idempotency？</summary>

锁只限制并发时谁先执行。锁释放后同一个操作仍可能再次执行；幂等关注重复逻辑请求的最终副作用是否只发生一次。

</details>

<details>
<summary>3. 服务端执行成功但响应丢失后该怎么办？</summary>

Client 用同一个 Idempotency Key 重试或查询 Operation Status，Server 返回已保存结果/状态，而不是直接再执行一次副作用。

</details>