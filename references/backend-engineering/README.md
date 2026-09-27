# Backend Engineering｜按问题查找技术依据

[返回课程](../../curriculum/03-backend-engineering/README.md) · [原始版本与证据记录](../../guide/project/backend-reader-revision-2026-09-27.md) · [讲解与分层验证](../../guide/audits/backend-clarity-refinement-2026-09-28.md)

先在课程中建立对象与状态变化，再按问题回到规范或官方实现。协议保证、框架行为与业务策略分别判断；面经用于校准学习深度，不证明技术答案正确。

## 版本与运行范围

课程版本基线继承 2026-09-27 的模块记录；2026-09-28 精修对新增解释所依赖的关键规则再次核验。保留时间、容量参数和版本化缓存方案是教学设计，不是产品默认保证。

| 对象 | 课程依据 | 本地执行边界 |
|---|---|---|
| Python | 3.13 文档；区分 GIL 构建、Future 与协程取消 | CPython 3.13.5：线程、标准库和测试 |
| 数据库 | SQLite 实验；前置 MySQL 9.7 / InnoDB | SQLite 3.46.1：事务、多连接与正常进程退出后读取；未运行 MySQL |
| HTTP、TLS、SSE | RFC 9110/9113/9114、9293、8446 与 WHATWG | 未执行真实网络故障实验 |
| HTTPX、gRPC | 官方接口与截止时间文档 | 未安装并验收对应网络服务 |
| 消息系统 | Kafka 4.2；RabbitMQ 确认文档 | 未启动消息代理；传统组与共享组分开讲解 |
| Kubernetes | 官方概念文档；文档版本不代表部署版本 | 未启动集群 |
| Java、Spring、Go | Java SE 21、Spring Framework 7.0 系列、Go 1.26 语境 | 未执行相应语言程序 |
| 安全 | RFC 7636、9700、8725、OIDC Core 与 OWASP | 验证 PKCE 的 S256 转换，不等于 OAuth 流程或部署安全审计 |
| 版本缓存与哈希 | 正文明确假设下的应用协议和算法 | 确定性内存模型；不是 Redis 并发、复制或迁移集成 |
| Linux | Linux man-pages、内核与工具文档 | 正文输出为教学数据，不是生产故障实测 |

## 按当前问题查资料

### 一次请求完成了什么，后端负责到哪里

[课程正文](../../curriculum/03-backend-engineering/docs/01-AIBackend职责与RequestPath.md)。

- [HTTP 202](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3)：区分已接受与已完成。

### 哪些状态必须保存，恢复时相信哪一份

[课程正文](../../curriculum/03-backend-engineering/docs/14-DataLayering与StateOwnership.md)。

这是应用设计与实验推导。与之组合的事务、协议和授权行为，回到相关主责章的官方依据；不把业务策略写成产品默认保证。

### 从字节到安全请求：TCP、TLS 与 HTTP

[课程正文](../../curriculum/03-backend-engineering/docs/02-TCPTLS与HTTPVersions.md)。

- [TCP 服务模型](https://www.rfc-editor.org/rfc/rfc9293.html#section-2.2)：字节流保证。
- [建连](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.5)：序列状态协商。
- [关闭](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.6)：双向关闭与状态。
- [拥塞控制](https://www.rfc-editor.org/rfc/rfc5681.html)：与接收端流控区分。
- [TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html#section-2)：证书认证、密钥交换与 Finished。
- [HTTP/2](https://httpwg.org/specs/rfc9113.html)：流与 TCP 的层次。
- [HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html#section-2)：QUIC 承载。
- [重定向](https://httpwg.org/specs/rfc9110.html#status.301)：方法和目标变化。

### 怎样传递结果，断线后怎样继续

[课程正文](../../curriculum/03-backend-engineering/docs/03-ServiceCommunication与StreamingReliability.md)。

- [gRPC](https://grpc.io/docs/what-is-grpc/core-concepts/)：调用模型。
- [SSE](https://html.spec.whatwg.org/multipage/server-sent-events.html)：事件格式与重连。
- [WebSocket](https://www.rfc-editor.org/rfc/rfc6455.html#section-5.5)：控制帧。

### 并发工作由谁执行，等待放在哪里

[课程正文](../../curriculum/03-backend-engineering/docs/04-Concurrency与ThreadPool.md)。

- [Future 与执行器](https://docs.python.org/3.13/library/concurrent.futures.html)：结果、异常、完成回调、取消与关闭。
- [线程与 GIL](https://docs.python.org/3.13/library/threading.html#gil-and-performance-considerations)：Python 实现条件。
- [协程取消](https://docs.python.org/3.13/library/asyncio-task.html#task-cancellation)：取消与清理。
- [系统调用](https://man7.org/linux/man-pages/man2/syscalls.2.html)：用户程序与内核的边界。

### 连接怎样复用，容量怎样计算

[课程正文](../../curriculum/03-backend-engineering/docs/05-ConnectionPool与ResourceCapacity.md)。

- [HTTPX 异步客户端](https://www.python-httpx.org/async/)：流响应清理。
- [资源限制](https://www.python-httpx.org/advanced/resource-limits/)：池大小与复用。
- [HTTP/2](https://httpwg.org/specs/rfc9113.html)：连接数与流数的差别。

### 到达速度超过处理能力时怎么办

[课程正文](../../curriculum/03-backend-engineering/docs/06-Backpressure与RateLimit.md)。

- [级联故障](https://sre.google/sre-book/addressing-cascading-failures/)：过载传播。
- [处理过载](https://sre.google/sre-book/handling-overload/)：接纳与丢弃策略。

### 等多久，超时之后还发生什么

[课程正文](../../curriculum/03-backend-engineering/docs/07-TimeoutDeadline与ErrorTaxonomy.md)。

- [HTTPX 超时](https://www.python-httpx.org/advanced/timeouts/)：不同等待阶段。
- [gRPC 截止时间](https://grpc.io/docs/guides/deadlines/)：跨调用预算。
- [协程取消](https://docs.python.org/3.13/library/asyncio-task.html#task-cancellation)：清理责任。
- [HTTP 5xx](https://httpwg.org/specs/rfc9110.html#status.502)：代理观察与业务事实。

### 怎样识别同一次操作，避免重复副作用

[课程正文](../../curriculum/03-backend-engineering/docs/09-APIIdempotency与SideEffect.md)。

- [HTTP 幂等](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)：效果而非响应字节。
- [Stripe 幂等](https://docs.stripe.com/api/idempotent_requests)：供应商保留与重用规则示例。
- [InnoDB 提交回滚](https://dev.mysql.com/doc/refman/9.7/en/innodb-autocommit-commit-rollback.html)：本地事务边界。
- [UUIDv7](https://www.rfc-editor.org/rfc/rfc9562.html#section-5.7)：编号布局而非业务去重。

### 什么时候值得再试，怎样防止故障放大

[课程正文](../../curriculum/03-backend-engineering/docs/08-RetryCircuitBreaker与Failover.md)。

- [SRE 过载处理](https://sre.google/sre-book/handling-overload/)：分层重试放大。

### 消息怎样交付，确认到底确认了什么

[课程正文](../../curriculum/03-backend-engineering/docs/10-MQ与DeliverySemantics.md)。

- [RabbitMQ 确认](https://www.rabbitmq.com/docs/confirms)：生产与消费确认分开。
- [Kafka 交付](https://kafka.apache.org/42/design/design/#message-delivery-semantics)：交付范围。

### Kafka 怎样分工、保序与恢复消费

[课程正文](../../curriculum/03-backend-engineering/docs/11-KafkaPartition与Backlog.md)。

- [Kafka 4.2 设计](https://kafka.apache.org/42/design/)：分区、传统组与 share group。
- [KafkaConsumer](https://kafka.apache.org/42/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)：位置、线程安全与恢复。
- [消费者配置](https://kafka.apache.org/42/configuration/consumer-configs/)：心跳、poll 与成员模型。

### 进程重启后，任务怎样继续推进

[课程正文](../../curriculum/03-backend-engineering/docs/12-ReliableAsyncTask.md)。

这是应用设计与实验推导。与之组合的事务、协议和授权行为，回到相关主责章的官方依据；不把业务策略写成产品默认保证。

### 多份数据不一致时，怎样恢复业务正确性

[课程正文](../../curriculum/03-backend-engineering/docs/13-Consistency与Compensation.md)。

- [Redis 淘汰](https://redis.io/docs/latest/develop/reference/eviction/)：缓存中的版本依据也可能丢失。

### 谁能访问什么，权限怎样贯穿请求与任务

[课程正文](../../curriculum/03-backend-engineering/docs/15-AuthSession与TenantBoundary.md)。

- [JWT 安全](https://www.rfc-editor.org/rfc/rfc8725.html)：算法、密钥与令牌用途。
- [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html)：身份层与 ID Token。
- [PKCE](https://www.rfc-editor.org/rfc/rfc7636.html)：第 4 节绑定和验证；附录 B 为 S256 测试向量。
- [OAuth 安全](https://www.rfc-editor.org/rfc/rfc9700.html)：现代授权与刷新令牌防护。

### 不可信输入怎样被限制在安全边界内

[课程正文](../../curriculum/03-backend-engineering/docs/21-BackendSecurity.md)。

- [SQL 注入防护](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)：数据与语句结构。
- [SSRF 防护](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)：解析、跳转和出口。
- [CSRF 防护](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)：浏览器自动凭证。
- [XSS 防护](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)：输出上下文。
- [命令注入防护](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)：参数语义与最小权限。
- [Kubernetes 安全](https://kubernetes.io/docs/concepts/security/security-checklist/)：容器权限边界。
- [密钥管理](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)：保存、轮换与审计。

### 多个服务实例怎样被找到和选中

[课程正文](../../curriculum/03-backend-engineering/docs/16-ServiceDiscovery与LoadBalancing.md)。

- [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)：稳定入口与端点。
- [Envoy 哈希负载均衡](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers)：哈希映射与分布；正文小环不是 Envoy 配置实验。

### 从慢请求的证据定位瓶颈

[课程正文](../../curriculum/03-backend-engineering/docs/17-Observability与PerformanceDiagnosis.md)。

- [SRE 监控](https://sre.google/sre-book/monitoring-distributed-systems/)：症状和证据。
- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/)：信号职责。
- [Prometheus](https://prometheus.io/docs/practices/histograms/)：直方图与摘要。

### 把应用故障追到 Linux 资源

[课程正文](../../curriculum/03-backend-engineering/docs/18-LinuxTroubleshooting.md)。

- [ps](https://man7.org/linux/man-pages/man1/ps.1.html)：进程列与状态。
- [loadavg](https://man7.org/linux/man-pages/man5/proc_loadavg.5.html)：负载定义。
- [cgroup v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)：CPU 和内存限制。
- [进程 status](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)：驻留等线索。
- [进程 limits](https://man7.org/linux/man-pages/man5/proc_pid_limits.5.html)：实际软硬限制。
- [进程 fd](https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html)：打开描述符。
- [ss](https://man7.org/linux/man-pages/man8/ss.8.html)：套接字状态、进程关联与统计范围。

### 部署、探针与停机怎样配合应用

[课程正文](../../curriculum/03-backend-engineering/docs/19-ContainerK8s与Deployment.md)。

- [Docker 对象模型](https://docs.docker.com/get-started/docker-overview/)：镜像与容器。
- [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)：部署控制。
- [探针](https://kubernetes.io/docs/concepts/workloads/pods/probes/)：健康职责。
- [Pod 生命周期](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)：终止与宽限预算。
- [cgroup v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)：资源边界。

### 配置和版本怎样安全改变

[课程正文](../../curriculum/03-backend-engineering/docs/20-ConfigRelease与ServiceEvolution.md)。

- [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)：环境变量、普通卷、subPath 与应用重载的差别。

### 把通用机制映射到 Java、Spring 与 Go

[课程正文](../../curriculum/03-backend-engineering/docs/22-CrossLanguageRuntimeMapping.md)。

- [Spring IoC](https://docs.spring.io/spring-framework/reference/core/beans.html)：依赖装配。
- [Bean 作用域](https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html)：生命周期与销毁。
- [Spring 代理](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)：自调用边界。
- [ReentrantLock](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html)：获取、释放与重入。
- [AQS](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/AbstractQueuedSynchronizer.html)：选读同步器框架。
- [HashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)：哈希与容量。
- [ConcurrentHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)：原子操作范围。
- [ThreadLocal](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html)：线程局部值。
- [JVM 数据区](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html)：规范与实现区分。
- [ZGC 项目](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main)：低延迟与版本资料。
- [Go 运行时说明](https://go.dev/src/runtime/HACKING)：G/M/P。
- [Go runtime](https://pkg.go.dev/runtime)：GOMAXPROCS 等行为。
- [Go Channel](https://go.dev/ref/spec#Channel_types)：通信与关闭。
- [Go context](https://pkg.go.dev/context)：取消与资源释放。

## 如何使用这些证据

原始来源索引的保留，不等于每次精修都重读全部外链。新增解释的核验范围、实验环境与未执行事项见精修记录。ZGC 项目页在原始审查中直接读取失败；本次未重新完成该页全文核验，不据此增加具体默认参数或启动配置要求。

容量、时序与 Linux 输出是教学假设。版本化缓存模型验证明确条件下的推理，不证明数据库复制、缓存原子性或授权系统已部署。PKCE 转换值正确也不等于重定向、登录会话、令牌兑换和撤销流程均已验证。
