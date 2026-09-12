# AI Backend Engineering｜Production 后端工程底座

[← FastAPI](../fastapi/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [MySQL →](../mysql/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：22 个连续知识小板块** · **HUMAN-A Canonical：39** · **独立来源覆盖：125**  
> **质量：Granularity / Coverage / Content Depth 已验收**

把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。

---

## 1. 这个模块解决什么

把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。

学习目标不是记住一组名词，而是能稳定回答：

```text
为什么需要它？
→ 核心机制怎样工作？
→ 正常路径怎样流动？
→ Failure / Trade-off 在哪里？
→ Production 场景怎样验证与排障？
→ 面试官继续追问时怎样解释边界？
```

---

## 2. 在十板块中的位置

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → **AI Backend Engineering** → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent Harness / Runtime](../agent-harness/README.md) → [System Design](../system-design/README.md)

当前模块角色：**Foundation / 把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。**

---

## 3. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

同时固定区分：

```text
Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 一个完整认知闭环
Section = 参数 / 变体 / Failure / 深挖追问
```

所以本模块是 **39 道 Canonical → 22 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Request / Network → Concurrency / Pool / Backpressure → Timeout / Retry / Idempotency → MQ / Kafka / Durable Task → Consistency / State / Auth → Discovery / Observability / Linux / K8s → Config / Security → Cross-language Runtime Mapping
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜Network 与 Service Communication

1. [AI Backend 的职责与一次请求的完整链路](docs/01-AIBackend职责与RequestPath.md)
2. [TCP、TLS 与 HTTP/1.1 / HTTP/2 / HTTP/3](docs/02-TCPTLS与HTTPVersions.md)
3. [HTTP / RPC / MQ 与 Streaming Reliability](docs/03-ServiceCommunication与StreamingReliability.md)

### Part B｜Concurrency、Capacity 与 Overload

4. [Concurrency Execution Model：Process / Thread / Coroutine / Thread Pool](docs/04-Concurrency与ThreadPool.md)
5. [Connection Pool 与 Resource Capacity](docs/05-ConnectionPool与ResourceCapacity.md)
6. [Backpressure、Concurrency Limit、Rate Limit 与 Load Shedding](docs/06-Backpressure与RateLimit.md)

### Part C｜Timeout、Retry 与 Side-effect Safety

7. [Timeout、Deadline 与 Error Taxonomy](docs/07-TimeoutDeadline与ErrorTaxonomy.md)
8. [Retry、Backoff、Circuit Breaker、Degradation 与 Failover](docs/08-RetryCircuitBreaker与Failover.md)
9. [Production API、Idempotency 与 Side Effect Safety](docs/09-APIIdempotency与SideEffect.md)

### Part D｜Messaging 与 Long-running Task

10. [为什么需要 MQ：Delivery Semantics 与 Failure Model](docs/10-MQ与DeliverySemantics.md)
11. [Kafka：Partition、Consumer Group、Ordering 与 Backlog](docs/11-KafkaPartition与Backlog.md)
12. [Reliable Async Task：Outbox、Lease、Heartbeat、Worker Recovery 与 Long-running API](docs/12-ReliableAsyncTask.md)

### Part E｜Consistency、State 与 Permission

13. [最终一致性、DB + Cache、Outbox、Saga 与 Compensation](docs/13-Consistency与Compensation.md)
14. [Data Layering 与 State Ownership：MySQL / Redis / Session / Runtime State](docs/14-DataLayering与StateOwnership.md)
15. [Authentication、Authorization、Session 与 Multi-tenant Boundary](docs/15-AuthSession与TenantBoundary.md)
16. [Service Discovery、Load Balancing、Stateless Routing 与 Distributed ID](docs/16-ServiceDiscovery与LoadBalancing.md)

### Part F｜Operations 与 Production Runtime

17. [Observability、SLO 与 Performance Diagnosis](docs/17-Observability与PerformanceDiagnosis.md)
18. [Linux Process / CPU / Memory / Disk / Port Troubleshooting](docs/18-LinuxTroubleshooting.md)
19. [Docker、Kubernetes、Health Check、Graceful Shutdown 与 Horizontal Scaling](docs/19-ContainerK8s与Deployment.md)
20. [Configuration、Feature Flag、Gray Release 与 Microservice Evolution](docs/20-ConfigRelease与ServiceEvolution.md)
21. [Backend Security：SSRF / CSRF / SQLi / XSS / Secret / Trust Boundary](docs/21-BackendSecurity.md)

### Part G｜跨语言 Runtime 映射

22. [Spring / JVM / Java Concurrency / Go Runtime：把生态题映射回通用 Backend Primitive](docs/22-CrossLanguageRuntimeMapping.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **39 道 Primary Canonical、125 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- DB + Cache Consistency
- TCP / Streaming Reliability
- Thread Pool / Backpressure
- MQ Reliability / Kafka
- Rate Limit / Retry / Idempotency
- MySQL / Redis State Layering

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- FastAPI 负责框架请求生命周期；AIBE 负责跨框架 Production Primitive。
- MySQL / Redis / Vector DB 的内部机制仍归各自数据模块。
- 完整端到端架构组合与容量方案进入 System Design。

遇到跨模块问题时，正文会保留必要桥梁，但完整机制只在 Primary Module 维护一份。

---

## 8. Review、Interview 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |
| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |
| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |
| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |

研究与质量证据：

- [Canonical Questions](../research/questions/ai-backend-engineering.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [权威技术 / 源码资料索引](../research/backend-sources/README.md)：只校准技术事实，不改变 HUMAN-A 频率；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 22` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–22 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[MySQL](../mysql/README.md)。
