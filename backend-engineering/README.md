# AI Backend Engineering｜AI 应用后端工程基础

> **Status：✅ 第一版完整系统教材已完成。** 当前为 `22` 个连续知识小板块 + Review + Interview 三件套；39 道 AI Backend Engineering HUMAN-A Canonical 已完成 Coverage / Depth 映射。课程主干由 beginner-first 的 Backend Engineering 知识依赖决定，真人面经只校准市场权重、真实问法、Failure / Scale / Troubleshooting 深度。

AI Backend Engineering 是整套 Handbook 的**横向 Production 工程主线**。

FastAPI 解决：

```text
一个 Python Web / AI Service 怎样接收请求、校验、Streaming、部署
```

AI Backend Engineering 解决：

```text
当这个 Service 开始依赖 DB / Redis / MQ / LLM / RAG / Tool / 多实例以后，
怎样让网络、并发、任务、状态、错误、部署和可观测性仍然保持可控？
```

---

## 1. 在总知识体系中的位置

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL / Redis / Vector DB
  ↓
LLM / RAG / Agent Harness
  ↓
System Design
```

模块边界：

| 模块 | 主要回答的问题 |
|---|---|
| Python | Thread / Process / Coroutine / GIL / asyncio 等语言与 Runtime 语义 |
| FastAPI | HTTP / ASGI 请求怎样进入 Python Service；DI、Streaming、Lifecycle 怎样组织 |
| **AI Backend Engineering** | Network、Pool、Backpressure、Timeout、Retry、MQ、Idempotency、Consistency、Auth、Deployment、Observability 等跨框架机制 |
| MySQL / Redis / Vector DB | 各自存储系统内部机制 |
| Agent Harness | Agent Loop、Tool、Context、Memory、Checkpoint、Permission 等 Agent 专属 Runtime |
| System Design | 把所有局部机制组合成完整系统 |

---

## 2. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

当前 AIBE 有 39 道 Primary Canonical，但不能写成 39 个文件；旧 README 又有 55 个左右的细粒度 Topic，也不能机械变成 55 个文件。

最终粒度是：

```text
39 HUMAN-A Canonical
+ 完整 Backend Engineering 前置
+ Google SRE / AWS / Stripe / Kafka / Kubernetes / OpenTelemetry / OAuth / OWASP 等权威工程资料
↓
22 个完整认知闭环
```

---

## 3. 真人面经怎样影响本模块

冻结 `S001–S279` 中，AIBE 是一个强市场信号模块：

- 39 道 ACTIVE Canonical；
- 125 个独立 HUMAN-A 来源覆盖；
- 16 道 L4；
- 高频包括 DB+Cache Consistency、SSE vs WebSocket、TCP/TCP Reliability、Thread Pool、MQ Reliability、为什么需要 MQ、JVM、Rate Limit、MySQL / Redis 数据分层。

面经没有决定目录顺序，但直接要求下面这些地方不能只讲定义：

```text
Network
→ 必须追到 TCP Reliability / TLS / HTTP Version / Streaming Disconnect

Concurrency
→ 必须追到 Thread Pool / Pool Saturation / Backpressure / Concurrency Limit

Reliability
→ 必须追到 Timeout Budget / Retry Storm / Idempotency / Failover

Messaging
→ 必须追到 Producer-Broker-Consumer Failure / Duplicate / Backlog / Ordering

Data
→ 必须追到 Cache Consistency / State Ownership / Compensation

Production
→ 必须追到 Linux / Container / K8s / Metrics-Log-Trace / Config Evolution
```

---

## 4. 权威资料怎样使用

正式教材额外参考：

- Google SRE：Overload / Cascading Failure / Retry Budget / Load Shedding；
- AWS Builders' Library：Timeout / Retry / Backoff / Jitter；
- Stripe：Idempotency-Key 的成熟 API 实践；
- Apache Kafka：Partition / Consumer Group / Ordering / Replay；
- Kubernetes：Startup / Liveness / Readiness / Termination；
- OpenTelemetry：Trace / Metric / Log / Context Propagation；
- OAuth / RFC 9700：OAuth Security BCP；
- OWASP：SSRF / CSRF / SQLi / XSS / Secrets。

来源索引：[`../research/backend-sources/README.md`](../research/backend-sources/README.md)

这些资料只校准机制和 Production Principle，**不能增加 HUMAN-A Source Count**。

---

# 5. 正式 22 个知识小板块

## Part A｜Network 与 Service Communication

1. [AI Backend 的职责与一次请求的完整链路](docs/01-AIBackend职责与RequestPath.md)
2. [TCP、TLS 与 HTTP/1.1 / HTTP/2 / HTTP/3](docs/02-TCPTLS与HTTPVersions.md)
3. [HTTP / RPC / MQ 与 Streaming Reliability](docs/03-ServiceCommunication与StreamingReliability.md)

## Part B｜Concurrency、Capacity 与 Overload

4. [Concurrency Execution Model：Process / Thread / Coroutine / Thread Pool](docs/04-Concurrency与ThreadPool.md)
5. [Connection Pool 与 Resource Capacity](docs/05-ConnectionPool与ResourceCapacity.md)
6. [Backpressure、Concurrency Limit、Rate Limit 与 Load Shedding](docs/06-Backpressure与RateLimit.md)

## Part C｜Timeout、Retry 与 Side Effect Safety

7. [Timeout、Deadline 与 Error Taxonomy](docs/07-TimeoutDeadline与ErrorTaxonomy.md)
8. [Retry、Backoff、Circuit Breaker、Degradation 与 Failover](docs/08-RetryCircuitBreaker与Failover.md)
9. [Production API、Idempotency 与 Side Effect Safety](docs/09-APIIdempotency与SideEffect.md)

## Part D｜Messaging 与 Long-running Task

10. [为什么需要 MQ：Delivery Semantics 与 Failure Model](docs/10-MQ与DeliverySemantics.md)
11. [Kafka：Partition、Consumer Group、Ordering 与 Backlog](docs/11-KafkaPartition与Backlog.md)
12. [Reliable Async Task：Outbox、Lease、Heartbeat、Worker Recovery 与 Long-running API](docs/12-ReliableAsyncTask.md)

## Part E｜Consistency、State 与 Permission

13. [最终一致性、DB + Cache、Outbox、Saga 与 Compensation](docs/13-Consistency与Compensation.md)
14. [Data Layering 与 State Ownership：MySQL / Redis / Session / Runtime State](docs/14-DataLayering与StateOwnership.md)
15. [Authentication、Authorization、Session 与 Multi-tenant Boundary](docs/15-AuthSession与TenantBoundary.md)
16. [Service Discovery、Load Balancing、Stateless Routing 与 Distributed ID](docs/16-ServiceDiscovery与LoadBalancing.md)

## Part F｜Operations 与 Production Runtime

17. [Observability、SLO 与 Performance Diagnosis](docs/17-Observability与PerformanceDiagnosis.md)
18. [Linux Process / CPU / Memory / Disk / Port Troubleshooting](docs/18-LinuxTroubleshooting.md)
19. [Docker、Kubernetes、Health Check、Graceful Shutdown 与 Horizontal Scaling](docs/19-ContainerK8s与Deployment.md)
20. [Configuration、Feature Flag、Gray Release 与 Microservice Evolution](docs/20-ConfigRelease与ServiceEvolution.md)
21. [Backend Security：SSRF / CSRF / SQLi / XSS / Secret / Trust Boundary](docs/21-BackendSecurity.md)

## Part G｜跨语言市场信号映射

22. [Spring / JVM / Java Concurrency / Go Runtime：把生态题映射回通用 Backend Primitive](docs/22-CrossLanguageRuntimeMapping.md)

---

## 6. 39 道 Canonical → 22-block 映射

```text
AIBE-001 HTTP Request Lifecycle                    → 01 / 02
AIBE-002 HTTPS / TLS                              → 02
AIBE-003 HTTP Versions / QUIC                     → 02
AIBE-004 TCP vs UDP                               → 02
AIBE-005 TCP Reliability                          → 02
AIBE-006 SSE vs WebSocket                         → 03
AIBE-007 Streaming Reliability                    → 03
AIBE-008 HTTP / RPC / MQ                          → 03 / 10

AIBE-009 Process / Thread / Coroutine             → 04
AIBE-010 Thread Pool                              → 04
AIBE-011 Producer / Consumer / Backpressure       → 06 / 10
AIBE-012 Async Service                            → 04 / 06
AIBE-013 Concurrency Control                      → 05 / 06

AIBE-014 Why MQ                                   → 10
AIBE-015 MQ Reliability                           → 10 / 12
AIBE-016 Kafka                                    → 11
AIBE-017 Rate Limit                               → 06
AIBE-018 Retry / Circuit / Degradation            → 08
AIBE-019 Idempotency                              → 09 / 12
AIBE-020 DB + Cache Consistency                   → 13 / 14

AIBE-021 Production REST API                      → 09
AIBE-022 Authentication / Authorization           → 15
AIBE-023 Session / Routing                        → 15 / 16
AIBE-024 Service Discovery / Load Balancing       → 16
AIBE-025 Global Unique ID                         → 16

AIBE-026 Linux Troubleshooting                    → 18
AIBE-027 Docker                                   → 19
AIBE-028 Kubernetes                               → 19
AIBE-029 Backend Observability                    → 17
AIBE-030 Configuration Center                     → 20
AIBE-031 Microservice / DDD                       → 20

AIBE-032 Spring                                   → 22
AIBE-033 Java Concurrency                         → 22
AIBE-034 JVM                                      → 22
AIBE-035 Java HashMap / ConcurrentHashMap         → 22
AIBE-036 ThreadLocal                              → 22
AIBE-037 Go Runtime                               → 22
AIBE-038 Backend Security                         → 21
AIBE-039 MySQL / Redis Data Layering              → 14
```

> 22 不是优化目标，而是当前知识闭环自然形成的结果。

---

## 7. 三条最重要的因果主线

### 主线 A｜请求为什么会从“能跑”走向“雪崩”

```text
Request Path
→ Connection / Pool
→ Concurrency
→ Queue / Backpressure
→ Timeout
→ Retry
→ Retry Amplification
→ Load Shedding / Degradation
```

### 主线 B｜为什么“重试一下”会变成正确性问题

```text
Unknown Outcome
→ Retry
→ Duplicate Side Effect
→ Idempotency
→ MQ Duplicate Delivery
→ Worker Crash
→ Lease / Recovery
→ Eventual Consistency / Reconciliation
```

### 主线 C｜一个服务怎样真正变成 Production Service

```text
State Ownership
→ Auth / Tenant
→ Service Discovery / Load Balancing
→ Observability
→ Container / K8s
→ Config / Gray Release
→ Security Boundary
```

---

## 8. 与已学模块的边界

- Python 已讲 GIL / asyncio / Lock；这里讲它们怎样组成**服务容量与并发模型**。
- FastAPI 已讲 request lifecycle / Streaming / deployment interface；这里讲**跨框架可靠性机制**。
- Redis 已讲具体缓存、锁、TTL、HA；这里讲 **Cache Consistency、Rate Limit、State Layering**。
- MySQL 已讲事务和锁；这里讲 **跨组件一致性与 Side Effect Safety**。
- Agent Harness 已讲 Agent Tool / Checkpoint / Cancellation；这里讲通用 **Task / MQ / Retry / Idempotency / Backend Runtime**。
- System Design 已讲完整场景组合；这里负责把这些 Production Primitive 本身讲透。

---

## 9. Review 与 Interview

- [`review/README.md`](review/README.md)：六张总图 + 综合自测；
- [`interview/高频面试题.md`](interview/高频面试题.md)：按真实问法练表达；
- [`interview/面试易错点.md`](interview/面试易错点.md)：避免把 Production 机制说成绝对规则；
- [`interview/面试前速查表.md`](interview/面试前速查表.md)：面试前快速回忆。

---

## 10. 学完以后应该能回答什么

不是只会列组件，而是能沿着下面这条线推理：

```text
这个请求是什么？
→ 依赖谁？
→ 哪个资源可能先饱和？
→ 能不能排队？
→ 排多久？
→ 什么时候超时？
→ 哪些错误能重试？
→ 重试会不会产生副作用？
→ 状态由谁拥有？
→ 故障后怎样恢复？
→ 怎么证明系统健康？
```

这才是 AI Application / Agent Backend 真正的 Production Engineering 能力。