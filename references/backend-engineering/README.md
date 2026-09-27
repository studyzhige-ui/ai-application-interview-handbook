# Backend Engineering｜按问题查找技术依据

[返回课程](../../curriculum/03-backend-engineering/README.md) · [维护与验证记录](../../guide/project/backend-reader-revision-2026-09-27.md)

先在课程中建立对象和状态变化，再按下面的问题回到规范或官方实现。规范说明协议保证，框架文档说明特定实现，业务上的保留时间、失败策略和容量参数仍需要自己确定。面经不能替代这些技术依据。

## 版本与运行范围

核验日期为 2026-09-27。目标资料版本不等于已在相应系统中执行过实验。

| 对象 | 课程依据 | 本轮实际执行 |
|---|---|---|
| Python | 3.13 文档，显式说明 GIL 构建与任务取消边界 | CPython 3.13.5，标准库实验与测试 |
| 数据库 | 本地实验是 SQLite 方言；数据库前置的目标为 MySQL 9.7 / InnoDB | SQLite 3.46.1；未运行 MySQL |
| HTTP、TLS、SSE | RFC 9110/9113/9114、9293、8446 与 WHATWG 滚动规范 | 未运行真实多客户端网络故障实验 |
| HTTPX、gRPC | 官方在线接口与截止时间说明，按核验日读取；不虚构已安装版本 | 未安装并验收对应网络服务 |
| 消息系统 | Kafka 4.2；RabbitMQ 4.3 的确认语义 | 未启动消息代理或验证复制故障 |
| Kubernetes | 核验日的官方滚动概念文档，不将站点版本导航当作部署版本 | 未启动 Kubernetes 集群 |
| Java、Spring、Go | Java SE 21；Spring Framework 7.0 系列；Go 1.26 及官方运行时说明 | 未执行对应语言程序 |
| 安全 | RFC 9700、RFC 8725、OIDC Core 与 OWASP 官方指南 | 只核验机制说明；未做真实部署安全审计 |

SQLite 的显式事务、多连接竞争和跨进程读取只证明本实验对象的行为。单元测试中的外部供应商与缓存反例使用模拟对象，不能上升为真实外部系统保证。

## 按当前要回答的问题查资料

### 一次请求完成了什么，后端负责到哪里

[课程正文](../../curriculum/03-backend-engineering/docs/01-AIBackend职责与RequestPath.md)。 对照：[HTTP 202 语义](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3)。

### 哪些状态必须保存，恢复时相信哪一份

[课程正文](../../curriculum/03-backend-engineering/docs/14-DataLayering与StateOwnership.md)。这是应用设计与本地实验推导；与之组合的协议、事务、授权事实应回到相邻章节列出的依据，不把业务策略写成产品默认保证。

### 从字节到安全请求：TCP、TLS 与 HTTP

[课程正文](../../curriculum/03-backend-engineering/docs/02-TCPTLS与HTTPVersions.md)。 对照：[TCP 的服务模型](https://www.rfc-editor.org/rfc/rfc9293.html#section-2.2)；[连接建立](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.5)；[关闭连接](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.6)；[拥塞控制基础](https://www.rfc-editor.org/rfc/rfc5681.html)；[TLS 1.3 握手与认证](https://www.rfc-editor.org/rfc/rfc8446.html#section-2)；[HTTP/2 标准](https://httpwg.org/specs/rfc9113.html)；[HTTP/3 与 QUIC](https://www.rfc-editor.org/rfc/rfc9114.html#section-2)；[HTTP 重定向语义](https://httpwg.org/specs/rfc9110.html#status.301)。

### 怎样传递结果，断线后怎样继续

[课程正文](../../curriculum/03-backend-engineering/docs/03-ServiceCommunication与StreamingReliability.md)。 对照：[gRPC 调用模型](https://grpc.io/docs/what-is-grpc/core-concepts/)；[SSE 的事件格式与重连](https://html.spec.whatwg.org/multipage/server-sent-events.html)；[WebSocket 控制帧](https://www.rfc-editor.org/rfc/rfc6455.html#section-5.5)。

### 并发工作由谁执行，等待放在哪里

[课程正文](../../curriculum/03-backend-engineering/docs/04-Concurrency与ThreadPool.md)。 对照：[Linux 系统调用接口](https://man7.org/linux/man-pages/man2/syscalls.2.html)；[Python 线程与 GIL](https://docs.python.org/3.13/library/threading.html#gil-and-performance-considerations)；[Future 取消与关闭语义](https://docs.python.org/3.13/library/concurrent.futures.html)；[asyncio 的任务取消](https://docs.python.org/3.13/library/asyncio-task.html#task-cancellation)。

### 连接怎样复用，容量怎样计算

[课程正文](../../curriculum/03-backend-engineering/docs/05-ConnectionPool与ResourceCapacity.md)。 对照：[HTTPX 异步客户端与流清理](https://www.python-httpx.org/async/)；[HTTPX 资源限制](https://www.python-httpx.org/advanced/resource-limits/)；[HTTP/2 多路复用](https://httpwg.org/specs/rfc9113.html)。

### 到达速度超过处理能力时怎么办

[课程正文](../../curriculum/03-backend-engineering/docs/06-Backpressure与RateLimit.md)。 对照：[过载与级联故障](https://sre.google/sre-book/addressing-cascading-failures/)；[SRE 的过载处理](https://sre.google/sre-book/handling-overload/)。

### 等多久，超时之后还发生什么

[课程正文](../../curriculum/03-backend-engineering/docs/07-TimeoutDeadline与ErrorTaxonomy.md)。 对照：[HTTPX 超时分类](https://www.python-httpx.org/advanced/timeouts/)；[gRPC 截止时间传播](https://grpc.io/docs/guides/deadlines/)；[asyncio 取消与清理](https://docs.python.org/3.13/library/asyncio-task.html#task-cancellation)；[HTTP 5xx 语义](https://httpwg.org/specs/rfc9110.html#status.502)。

### 怎样识别同一次操作，避免重复副作用

[课程正文](../../curriculum/03-backend-engineering/docs/09-APIIdempotency与SideEffect.md)。 对照：[HTTP 幂等方法](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)；[Stripe 的幂等请求规则示例](https://docs.stripe.com/api/idempotent_requests)；[InnoDB 提交与回滚](https://dev.mysql.com/doc/refman/9.7/en/innodb-autocommit-commit-rollback.html)；[UUID 类型与 v7](https://www.rfc-editor.org/rfc/rfc9562.html#section-5.7)。

### 什么时候值得再试，怎样防止故障放大

[课程正文](../../curriculum/03-backend-engineering/docs/08-RetryCircuitBreaker与Failover.md)。 对照：[SRE 对分层重试放大的分析](https://sre.google/sre-book/handling-overload/)。

### 消息怎样交付，确认到底确认了什么

[课程正文](../../curriculum/03-backend-engineering/docs/10-MQ与DeliverySemantics.md)。 对照：[RabbitMQ 4.3 确认边界](https://www.rabbitmq.com/docs/confirms)；[Kafka 的交付语义](https://kafka.apache.org/42/design/design/#message-delivery-semantics)。

### Kafka 怎样分工、保序与恢复消费

[课程正文](../../curriculum/03-backend-engineering/docs/11-KafkaPartition与Backlog.md)。 对照：[Kafka 日志与消费设计](https://kafka.apache.org/42/design/)；[KafkaConsumer 的位置语义](https://kafka.apache.org/42/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)；[Kafka 4.2 消费者配置](https://kafka.apache.org/42/configuration/consumer-configs/)；[Kafka share group 设计](https://kafka.apache.org/42/design/)。

### 进程重启后，任务怎样继续推进

[课程正文](../../curriculum/03-backend-engineering/docs/12-ReliableAsyncTask.md)。这是应用设计与本地实验推导；与之组合的协议、事务、授权事实应回到相邻章节列出的依据，不把业务策略写成产品默认保证。

### 多份数据不一致时，怎样恢复业务正确性

[课程正文](../../curriculum/03-backend-engineering/docs/13-Consistency与Compensation.md)。这是应用设计与本地实验推导；与之组合的协议、事务、授权事实应回到相邻章节列出的依据，不把业务策略写成产品默认保证。

### 谁能访问什么，权限怎样贯穿请求与任务

[课程正文](../../curriculum/03-backend-engineering/docs/15-AuthSession与TenantBoundary.md)。 对照：[JWT 安全规范](https://www.rfc-editor.org/rfc/rfc8725.html)；[OIDC Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)；[OAuth 安全最佳实践 RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)。

### 不可信输入怎样被限制在安全边界内

[课程正文](../../curriculum/03-backend-engineering/docs/21-BackendSecurity.md)。 对照：[OWASP SQL 注入防护](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)；[OWASP SSRF 防护](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)；[OWASP CSRF 防护](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)；[OWASP XSS 防护](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)；[OWASP 命令注入防护](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)；[Kubernetes 安全检查表](https://kubernetes.io/docs/concepts/security/security-checklist/)；[OWASP 密钥管理](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)。

### 多个服务实例怎样被找到和选中

[课程正文](../../curriculum/03-backend-engineering/docs/16-ServiceDiscovery与LoadBalancing.md)。 对照：[Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)。

### 从慢请求的证据定位瓶颈

[课程正文](../../curriculum/03-backend-engineering/docs/17-Observability与PerformanceDiagnosis.md)。 对照：[SRE 监控原则](https://sre.google/sre-book/monitoring-distributed-systems/)；[OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/)；[Prometheus 直方图与摘要](https://prometheus.io/docs/practices/histograms/)。

### 把应用故障追到 Linux 资源

[课程正文](../../curriculum/03-backend-engineering/docs/18-LinuxTroubleshooting.md)。 对照：[Linux loadavg](https://man7.org/linux/man-pages/man5/proc_loadavg.5.html)；[Linux cgroup v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)；[进程状态字段](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)；[目标进程 limits](https://man7.org/linux/man-pages/man5/proc_pid_limits.5.html)。

### 部署、探针与停机怎样配合应用

[课程正文](../../curriculum/03-backend-engineering/docs/19-ContainerK8s与Deployment.md)。 对照：[Docker 对象模型](https://docs.docker.com/get-started/docker-overview/)；[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)；[Kubernetes 探针](https://kubernetes.io/docs/concepts/workloads/pods/probes/)；[Pod 终止过程](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)；[cgroup v2 资源模型](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)。

### 配置和版本怎样安全改变

[课程正文](../../curriculum/03-backend-engineering/docs/20-ConfigRelease与ServiceEvolution.md)。 对照：[ConfigMap 更新语义](https://kubernetes.io/docs/concepts/configuration/configmap/)；[ConfigMap 更新边界](https://kubernetes.io/docs/concepts/configuration/configmap/)。

### 把通用机制映射到 Java、Spring 与 Go

[课程正文](../../curriculum/03-backend-engineering/docs/22-CrossLanguageRuntimeMapping.md)。 对照：[Spring IoC 容器](https://docs.spring.io/spring-framework/reference/core/beans.html)；[Bean 作用域](https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html)；[Spring 代理与自调用](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)；[ReentrantLock](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html)；[AQS API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/AbstractQueuedSynchronizer.html)；[Java HashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)；[ConcurrentHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)；[ThreadLocal API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html)；[JVM 运行数据区](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html)；[OpenJDK ZGC 项目资料](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main)；[Go 运行时开发说明](https://go.dev/src/runtime/HACKING)；[Go runtime](https://pkg.go.dev/runtime)；[Go 通道规范](https://go.dev/ref/spec#Channel_types)；[Go context](https://pkg.go.dev/context)。

## 使用参考资料时的边界

网络超时默认值要区分总时长、单次读写间隔和连接池等待。Kafka 的传统分区消费组与 share group（共享组）不是同一套分工模型。Kubernetes 的探针、路由传播与停机宽限也不是一条严格串行的时间线。上述区别均在正文就地解释，不要求读者从文档目录自行猜测。

ZGC 项目页的直接读取在本轮失败，官方搜索摘要能确认其低延迟与分代方向，但本轮不声称完成该页全文核验。课程因此不列具体版本的 ZGC 默认参数或把某个启动选项作为主线自测前提。其他链接的核验是对应结论所在段落，不等同于阅读全文或验证所有外链锚点。

容量和时序示例中的数值是教学假设，不是真实生产测量。令牌桶、租约时间和缓存乱序反例使用显式逻辑条件，换成分布式实现还需校验时间、原子性和故障传播。
