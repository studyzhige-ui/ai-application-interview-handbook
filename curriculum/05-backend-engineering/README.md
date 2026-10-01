# AI Backend Engineering｜可靠的 AI 应用后端

[← Redis](../04-redis/README.md) · [课程目录](../README.md) · [学习路线](../../guide/learning-path.md) · [LLM Foundation →](../06-llm-foundation/README.md)

后端把一次用户操作连接到数据、模型与外部工具，并对执行过程承担责任：输入由谁授权，资源够不够，工作是否真的完成，重启后怎样恢复，发生故障时凭什么判断。

本模块通过文档更新、消息通知和长期任务建立这些共同机制。Python 用于可运行的小实验，不把通用的网络、事务、消息和容量原理绑定到某个 Web 框架。

## 学习前提与边界

推荐先完成 Python、FastAPI、MySQL 和 Redis。至少能理解函数与异常、HTTP 请求与响应、连接资源、唯一约束、事务、条件更新和缓存。每章仍解释当前问题所需的最小模型，不要求先搭建整套生产集群。

FastAPI 负责接口与框架使用；MySQL、Redis 负责各自存储机制；本模块负责把它们组合成可限制、可恢复、可诊断的服务。模型原理、检索策略和 Agent 决策分别由 LLM、RAG 和 Agent 承接，完整容量方案与跨系统架构权衡由 System Design 承接。

## 阅读顺序

先问“发生了什么、相信什么”，再讨论传输与执行资源；先说明副作用怎样防重，再决定是否重试；权限与不可信输入的边界建立之后，才进入多实例运行与发布。

```text
请求与持久状态
    ↓
网络、通信、并发与容量
    ↓
等待预算、幂等与受控重试
    ↓
消息、任务恢复与一致性
    ↓
身份、授权与安全边界
    ↓
服务发现、诊断、部署与演进
    ↓
Java / Spring / Go 的机制映射
```

文件编号、下表与章首的前后导航采用同一阅读顺序；机器可读顺序维护在 [chapter-order.json](chapter-order.json)。

<!-- chapter-list:start -->
| 阅读顺位 | 文件编号 | 章节 |
|---:|---:|---|
| 1 | 01 | [一次请求完成了什么，后端负责到哪里](docs/01-AIBackend职责与RequestPath.md) |
| 2 | 02 | [哪些状态必须保存，恢复时相信哪一份](docs/02-DataLayering与StateOwnership.md) |
| 3 | 03 | [从字节到安全请求：TCP、TLS 与 HTTP](docs/03-TCPTLS与HTTPVersions.md) |
| 4 | 04 | [怎样传递结果，断线后怎样继续](docs/04-ServiceCommunication与StreamingReliability.md) |
| 5 | 05 | [并发工作由谁执行，等待放在哪里](docs/05-Concurrency与ThreadPool.md) |
| 6 | 06 | [连接怎样复用，容量怎样计算](docs/06-ConnectionPool与ResourceCapacity.md) |
| 7 | 07 | [到达速度超过处理能力时怎么办](docs/07-Backpressure与RateLimit.md) |
| 8 | 08 | [等多久，超时之后还发生什么](docs/08-TimeoutDeadline与ErrorTaxonomy.md) |
| 9 | 09 | [怎样识别同一次操作，避免重复副作用](docs/09-APIIdempotency与SideEffect.md) |
| 10 | 10 | [什么时候值得再试，怎样防止故障放大](docs/10-RetryCircuitBreaker与Failover.md) |
| 11 | 11 | [消息怎样交付，确认到底确认了什么](docs/11-MQ与DeliverySemantics.md) |
| 12 | 12 | [Kafka 怎样分工、保序与恢复消费](docs/12-KafkaPartition与Backlog.md) |
| 13 | 13 | [进程重启后，任务怎样继续推进](docs/13-ReliableAsyncTask.md) |
| 14 | 14 | [多份数据不一致时，怎样恢复业务正确性](docs/14-Consistency与Compensation.md) |
| 15 | 15 | [谁能访问什么，权限怎样贯穿请求与任务](docs/15-AuthSession与TenantBoundary.md) |
| 16 | 16 | [不可信输入怎样被限制在安全边界内](docs/16-BackendSecurity.md) |
| 17 | 17 | [多个服务实例怎样被找到和选中](docs/17-ServiceDiscovery与LoadBalancing.md) |
| 18 | 18 | [从慢请求的证据定位瓶颈](docs/18-Observability与PerformanceDiagnosis.md) |
| 19 | 19 | [把应用故障追到 Linux 资源](docs/19-LinuxTroubleshooting.md) |
| 20 | 20 | [部署、探针与停机怎样配合应用](docs/20-ContainerK8s与Deployment.md) |
| 21 | 21 | [配置和版本怎样安全改变](docs/21-ConfigRelease与ServiceEvolution.md) |
| 22 | 22 | [把通用机制映射到 Java、Spring 与 Go](docs/22-CrossLanguageRuntimeMapping.md) |
<!-- chapter-list:end -->

跨语言章承担通用机制与生态实现的对应。它不是 Java 或 Go 的完整入门课；目标岗位使用这些技术时，需要结合官方资料完成对应语言实作，不能把“能做概念对照”当作已经掌握整个生态。

## 怎样完成一个学习单元

读完一个问题后，先不看答案，画出输入、状态变化与结果；再改变一个条件，例如响应丢失、连接耗尽或执行者过期，预测原结论是否仍成立。最后运行相关实验或完成手算，并用章末“🎯 面试怎么答”整理表达。

正文有完整机制与最小示例。初始化、清理和批量测试放在实验目录；章节引用的代码片段由统一实现导出，避免正文和测试各维护一份逻辑。

| 使用入口 | 用途 |
|---|---|
| [机制实验](examples/README.md) | 观察在途容量、事务防重、提交后的查询与代际校验 |
| [Review](review/README.md) | 从故障时间线重建各层关系，对照综合情境中的判断 |
| [高频面试题](interview/高频面试题.md) | 保留真实问法的重点，训练有条件的回答与连续追问 |
| [面试易错点](interview/面试易错点.md) | 校正状态、范围、版本和观察证据的混淆 |
| [面试前速查表](interview/面试前速查表.md) | 快速定位要回看的机制，不代替首次学习 |
| [技术参考](../../references/backend-engineering/README.md) | 按问题查找协议、官方行为与版本依据 |

## 教材、证据与验证

正式面经说明岗位问到了哪些问题，技术结论由规范、官方文档和适用范围支持。冻结能力归属见 [Canonical](../../interview/canonical/ai-backend-engineering.md)，本模块不重新计算其来源数量。

课程实验使用 Python 3.13 与 SQLite 方言，不能替代 MySQL、消息代理、Kubernetes 或外部供应商的实测。目标技术资料与实际运行环境、来源映射及验证范围记录在 [模块维护记录](../../guide/project/backend-reader-revision-2026-09-27.md)。
