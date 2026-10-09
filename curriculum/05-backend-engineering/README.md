# AI Backend Engineering｜组合幂等、可靠任务、容量控制和跨系统恢复

[← Redis](../04-redis/README.md) · [课程目录](../README.md) · [Handbook](../../README.md) · [LLM Foundation →](../06-llm-foundation/README.md)

沿一次请求、文档修改和长期任务，解释状态由谁负责、资源如何限制、故障后怎样继续。

## 学习前提与目标

建议先完成 Python、FastAPI、MySQL 与 Redis，理解 HTTP、事务、唯一约束和缓存。

学完后应能组合幂等、可靠任务、容量控制和跨系统恢复。

## 学习顺序

按下列顺序阅读。章节文件编号用于定位；状态归属先于网络与可靠性组合建立。

1. [一次请求完成了什么，后端负责到哪里](docs/01-AIBackend职责与RequestPath.md)
2. [哪些状态必须保存，恢复时相信哪一份](docs/14-DataLayering与StateOwnership.md)
3. [从字节到安全请求：TCP、TLS 与 HTTP](docs/02-TCPTLS与HTTPVersions.md)
4. [怎样传递结果，断线后怎样继续](docs/03-ServiceCommunication与StreamingReliability.md)
5. [并发工作由谁执行，等待放在哪里](docs/04-Concurrency与ThreadPool.md)
6. [连接怎样复用，容量怎样计算](docs/05-ConnectionPool与ResourceCapacity.md)
7. [到达速度超过处理能力时怎么办](docs/06-Backpressure与RateLimit.md)
8. [等多久，超时之后还发生什么](docs/07-TimeoutDeadline与ErrorTaxonomy.md)
9. [怎样识别同一次操作，避免重复副作用](docs/09-APIIdempotency与SideEffect.md)
10. [什么时候值得再试，怎样防止故障放大](docs/08-RetryCircuitBreaker与Failover.md)
11. [消息怎样交付，确认到底确认了什么](docs/10-MQ与DeliverySemantics.md)
12. [Kafka 怎样分工、保序与恢复消费](docs/11-KafkaPartition与Backlog.md)
13. [进程重启后，任务怎样继续推进](docs/12-ReliableAsyncTask.md)
14. [多份数据不一致时，怎样恢复业务正确性](docs/13-Consistency与Compensation.md)
15. [谁能访问什么，权限怎样贯穿请求与任务](docs/15-AuthSession与TenantBoundary.md)
16. [不可信输入怎样被限制在安全边界内](docs/21-BackendSecurity.md)
17. [多个服务实例怎样被找到和选中](docs/16-ServiceDiscovery与LoadBalancing.md)
18. [从慢请求的证据定位瓶颈](docs/17-Observability与PerformanceDiagnosis.md)
19. [把应用故障追到 Linux 资源](docs/18-LinuxTroubleshooting.md)
20. [部署、探针与停机怎样配合应用](docs/19-ContainerK8s与Deployment.md)
21. [配置和版本怎样安全改变](docs/20-ConfigRelease与ServiceEvolution.md)
22. [把通用机制映射到 Java、Spring 与 Go](docs/22-CrossLanguageRuntimeMapping.md)

## 正文与复习

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界，再用章末自测检查能否独立解释。第二遍使用 [Review](review/README.md)重建关系，并改变条件验证结论。

面试准备集中在 [本知识域](../../interview/backend-engineering/README.md)：[高频面试题](../../interview/backend-engineering/01-高频面试题.md)、[易混易错点](../../interview/backend-engineering/02-易混易错点.md)与[面试速查](../../interview/backend-engineering/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
