# AI Backend Engineering｜权威工程资料索引

[← AI Backend Engineering](../../curriculum/03-backend-engineering/README.md) · [↑ Handbook 总目录](../../README.md) · [Research 首页](../../market/README.md)

> **用途：Production Engineering 技术事实校准。** Google SRE / AWS / Kafka / K8s / OTel / OAuth / OWASP 等不计入 HUMAN-A Source Count。

---

更新日期：2026-09-11

> 本目录只用于校准通用后端工程机制与当前平台语义，**不计入 HUMAN-A Source Count**。市场频率仍然只来自冻结 `S001–S279`。

## 1. Reliability / Overload / Retry

### Google SRE

- Service Best Practices：容量、过载、降级、Load Shedding、Retry 风险
  - https://sre.google/sre-book/service-best-practices/
- Handling Overload：Client-side Throttling、Retry Budget、Overload Error
  - https://sre.google/sre-book/handling-overload/
- Addressing Cascading Failures：过载、队列、级联故障、Retry 放大
  - https://sre.google/sre-book/addressing-cascading-failures/

### AWS Builders' Library / Architecture

- Timeouts, Retries and Backoff with Jitter
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- Exponential Backoff and Jitter
  - https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/

课程使用：Timeout Budget、Retry、Backoff、Jitter、Retry Storm、Load Shedding、Degradation。

---

## 2. Idempotency / API Side Effect

### Stripe API

- Idempotent Requests
  - https://docs.stripe.com/api/idempotent_requests

课程使用：Idempotency-Key、重复请求结果复用、参数一致性、未知执行结果后的安全重试。

> Stripe 的具体保留时间/实现是产品语义，不应写成所有系统的统一标准。

---

## 3. Messaging / Kafka

### Apache Kafka

- Design
  - https://kafka.apache.org/design/
- Documentation
  - https://kafka.apache.org/documentation/

课程使用：Partition、Consumer Group、Per-partition Ordering、Offset / Replay、Backlog 与消费者扩展。

> Kafka 的机制用于解释一个成熟日志型消息系统；“所有 MQ 都这样”是错误表达。

---

## 4. Deployment / Health / Graceful Lifecycle

### Kubernetes

- Liveness / Readiness / Startup Probes
  - https://kubernetes.io/docs/concepts/workloads/pods/probes/
- Pod Lifecycle / Termination
  - https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/

课程使用：Startup/Liveness/Readiness 区别、流量摘除、Restart、Graceful Termination。

---

## 5. Observability

### OpenTelemetry

- Concepts
  - https://opentelemetry.io/docs/concepts/
- Signals
  - https://opentelemetry.io/docs/concepts/signals/
- Observability Primer
  - https://opentelemetry.io/docs/concepts/observability-primer/

课程使用：Trace / Metric / Log / Baggage、Context Propagation、跨服务请求定位。

---

## 6. Authentication / OAuth Security

### IETF / OAuth

- OAuth 2.0 Security Best Current Practice（RFC 9700）
  - https://www.rfc-editor.org/rfc/rfc9700.html
- OAuth 2.1 overview / ongoing consolidation
  - https://oauth.net/2.1/

课程使用：Authentication / Authorization 边界、Authorization Code + PKCE、Refresh Token 安全边界。

> OAuth 2.1 仍是规范演进工作，教材不会把草案状态写成已经取代所有 OAuth 2.0 部署的绝对事实。

---

## 7. Web / Backend Security

### OWASP Cheat Sheet Series

- SSRF Prevention
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- SQL Injection Prevention
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- Cross Site Scripting Prevention
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- CSRF Prevention
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- Secrets Management
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

课程使用：Trust Boundary、输入/输出编码、网络 Egress、Secret 生命周期、Least Privilege。

---

## 8. 证据分层

```text
Tier A：S001–S279 HUMAN-A Canonical
→ 市场频率 / 真实问法 / 追问深度

Tier B：官方标准 / 官方工程资料
→ 稳定机制 / 当前平台事实 / Failure Principle

Tier C：课程抽象
→ beginner-first 的 0→1 知识顺序
```

重要规则：

1. 官方资料不能增加 HUMAN-A Source Count；
2. 某个平台有独立机制，不等于自动拆成一个教材文件；
3. 产品特定语义必须标出边界，不能写成通用定律；
4. 课程仍以 Python AI Backend 为主线，Java / Go 来源只用于跨语言映射。
