# AI Backend Engineering Canonical Questions — S001–S279 全库纵向扫描 v3

更新日期：2026-09-10

> 一级板块：**AI Backend Engineering**。这里承接 AI Application / Agent Service 的通用工程底座：Network / Protocol、Streaming、Concurrency、Async、MQ、Backpressure、Rate Limit、Retry、Idempotency、Auth、Session、Distributed Service、Linux / Docker / K8s、Observability 与 Backend Runtime。MySQL / Redis / Vector DB 的内部机制归各自模块；端到端场景题归 `System Design`。
>
> 本文件所有条目的 `Primary Module = AI Backend Engineering`；`Source Count` 只按冻结 HUMAN-A `S001–S279` 的独立招聘流程计算。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**39**
- 证据范围：仅 `S001–S279`
- 当前版本：`v3`（Global Merge / Split Audit）

### 高频信号

- `AIBE-020` · 20：Database + Cache Consistency
- `AIBE-006` · 13：SSE vs WebSocket
- `AIBE-004` / `005` · 12：TCP / UDP 与 TCP Reliability
- `AIBE-010` · 12：Thread Pool
- `AIBE-015` · 12：MQ Reliability
- `AIBE-014` · 11：为什么需要 MQ
- `AIBE-034` · 11：JVM / Class Loading / GC / OOM
- `AIBE-017` · 10：Rate Limit
- `AIBE-039` · 10：MySQL / Redis 数据分层

---

## 2. Network / Protocol / Streaming

### AIBE-001 · 从输入 URL 到服务返回，一次 HTTP 请求的 DNS、连接、协议与服务端处理链路怎样发生？
- **Topic**：HTTP Request Lifecycle
- **Question Type**：Concept / Deep Dive
- **Depth**：L2
- **Source Count**：**8**
- **Evidence Sources**：`S013`, `S020`, `S096`, `S117`, `S124`, `S129`, `S202`, `S273`

### AIBE-002 · HTTP 与 HTTPS 的核心差异是什么？TLS 握手、证书信任链、对称 / 非对称加密怎样协作？
- **Topic**：HTTPS / TLS
- **Question Type**：Concept / Why
- **Depth**：L3
- **Source Count**：**9**
- **Evidence Sources**：`S089`, `S096`, `S117`, `S137`, `S170`, `S200`, `S202`, `S251`, `S269`

### AIBE-003 · HTTP/1.1、HTTP/2、HTTP/3 与 QUIC 的核心差异是什么？AI Streaming Service 为什么关心这些差异？
- **Topic**：HTTP Versions / QUIC
- **Question Type**：Comparison / Why
- **Depth**：L2
- **Source Count**：**4**
- **Evidence Sources**：`S149`, `S156`, `S200`, `S224`

### AIBE-004 · TCP 与 UDP 有什么差异？可靠传输、顺序、连接语义和实时性怎样影响服务选型？
- **Topic**：TCP / UDP
- **Question Type**：Comparison
- **Depth**：L2
- **Source Count**：**12**
- **Evidence Sources**：`S021`, `S089`, `S110`, `S129`, `S133`, `S159`, `S170`, `S173`, `S229`, `S234`, `S251`, `S273`

### AIBE-005 · TCP 三次握手、四次挥手、重传与拥塞控制为什么这样设计？异常断连怎样被感知？
- **Topic**：TCP Reliability
- **Question Type**：Why / Deep Dive
- **Depth**：L3
- **Source Count**：**12**
- **Evidence Sources**：`S013`, `S089`, `S110`, `S129`, `S133`, `S170`, `S173`, `S175`, `S214`, `S229`, `S251`, `S273`

### AIBE-006 · SSE 与 WebSocket 的通信模型、方向、连接维护和适用场景有什么差异？
- **Topic**：SSE / WebSocket
- **Question Type**：Comparison / Trade-off
- **Depth**：L3
- **Source Count**：**13**
- **Evidence Sources**：`S033`, `S035`, `S066`, `S083`, `S087`, `S098`, `S156`, `S164`, `S170`, `S171`, `S181`, `S214`, `S240`
- **Related Modules**：FastAPI, Agent Harness / Runtime

### AIBE-007 · Streaming Connection 断开后怎样做 Heartbeat、Reconnect、Resume 与状态补偿？
- **Topic**：Streaming Reliability
- **Question Type**：Troubleshoot / System Design
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S035`, `S089`, `S156`
- **Related Modules**：Agent Harness / Runtime

### AIBE-008 · HTTP、RPC / gRPC 和 MQ 在跨服务通信中怎样选择？延迟、耦合、Schema、可靠性与演进成本分别是什么？
- **Topic**：Service Communication
- **Question Type**：Comparison / Trade-off
- **Depth**：L3
- **Source Count**：**5**
- **Evidence Sources**：`S088`, `S129`, `S185`, `S258`, `S273`

---

## 3. Concurrency / Async / Runtime

### AIBE-009 · Process、Thread、Coroutine 的核心区别是什么？上下文切换、资源隔离与并发模型怎样影响 AI Backend？
- **Topic**：Process / Thread / Coroutine
- **Question Type**：Comparison
- **Depth**：L2
- **Source Count**：**12**
- **Evidence Sources**：`S021`, `S064`, `S129`, `S131`, `S159`, `S166`, `S173`, `S175`, `S184`, `S195`, `S234`, `S269`
- **Related Modules**：Python

### AIBE-010 · Thread Pool 的核心参数、任务流转、拒绝策略和线程数应该怎样设计？
- **Topic**：Thread Pool
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**12**
- **Evidence Sources**：`S104`, `S116`, `S137`, `S145`, `S192`, `S193`, `S198`, `S202`, `S214`, `S216`, `S232`, `S277`

### AIBE-011 · 高并发 Producer / Consumer 或任务执行模型怎样设计 Queue、并发上限和 Backpressure？
- **Topic**：Producer / Consumer / Backpressure
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**4**
- **Evidence Sources**：`S097`, `S142`, `S214`, `S279`

### AIBE-012 · AI / LLM I/O 为什么适合异步非阻塞调用？同步 / 异步、Event Loop 与 Long-running Task 怎样取舍？
- **Topic**：Async Service
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Source Count**：**7**
- **Evidence Sources**：`S075`, `S086`, `S184`, `S205`, `S214`, `S241`, `S256`
- **Related Modules**：Python, FastAPI, Agent Harness / Runtime

### AIBE-013 · 如何限制并发调用外部 API，避免 Connection Pool、Downstream 或模型服务被打满？
- **Topic**：Concurrency Control
- **Question Type**：System Design / Reliability
- **Depth**：L4
- **Source Count**：**4**
- **Evidence Sources**：`S110`, `S190`, `S198`, `S209`

---

## 4. Messaging / Reliability / Flow Control

### AIBE-014 · MQ 在 AI Backend / Agent 异步链路中为什么存在？相比数据库传状态或同步 RPC，它解决什么问题？
- **Topic**：Message Queue
- **Question Type**：Why / Comparison
- **Depth**：L3
- **Source Count**：**11**
- **Evidence Sources**：`S018`, `S023`, `S081`, `S104`, `S138`, `S147`, `S164`, `S172`, `S195`, `S203`, `S277`

### AIBE-015 · MQ 怎样保证消息尽量不丢、避免重复消费，并处理 Producer / Broker / Consumer Failure？
- **Topic**：MQ Reliability
- **Question Type**：Troubleshoot / Reliability
- **Depth**：L4
- **Source Count**：**12**
- **Evidence Sources**：`S023`, `S079`, `S100`, `S104`, `S138`, `S147`, `S165`, `S199`, `S232`, `S262`, `S277`, `S279`

### AIBE-016 · Kafka Partition、Consumer Group、顺序性与 Backlog 怎样理解？积压时如何定位流量、分区和消费能力瓶颈？
- **Topic**：Kafka
- **Question Type**：Concept / Troubleshoot
- **Depth**：L4
- **Source Count**：**7**
- **Evidence Sources**：`S100`, `S136`, `S165`, `S199`, `S232`, `S274`, `S279`

### AIBE-017 · Rate Limit 常见算法怎样比较？Single-node、Distributed、User / Tenant / Token Budget 限流怎样设计？
- **Topic**：Rate Limiting
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Source Count**：**10**
- **Evidence Sources**：`S069`, `S079`, `S084`, `S198`, `S201`, `S209`, `S247`, `S270`, `S274`, `S276`
- **Related Modules**：Redis, Agent Harness / Runtime

### AIBE-018 · Retry、Circuit Breaker、Degradation 与 Fallback 分别解决什么问题？怎样避免重试风暴和级联故障？
- **Topic**：Resilience
- **Question Type**：Comparison / Reliability
- **Depth**：L4
- **Source Count**：**10**
- **Evidence Sources**：`S075`, `S079`, `S092`, `S109`, `S113`, `S144`, `S154`, `S174`, `S198`, `S276`
- **Related Modules**：Agent Harness / Runtime

### AIBE-019 · 有副作用的请求怎样设计 Idempotency？Retry / Timeout / Crash 后怎样避免重复扣款、下单或执行？
- **Topic**：Idempotency
- **Question Type**：System Design / Reliability
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S035`, `S091`, `S093`, `S147`, `S158`, `S165`, `S262`, `S279`
- **Related Modules**：MySQL, Redis, Agent Harness / Runtime

### AIBE-020 · Database + Cache 双写怎样保证最终一致性？Cache Aside、删除缓存、补偿和 Failure Window 怎样理解？
- **Topic**：Data Consistency / Cache Architecture
- **Question Type**：System Design / Troubleshoot
- **Depth**：L4
- **Source Count**：**20**
- **Evidence Sources**：`S010`, `S023`, `S090`, `S093`, `S105`, `S118`, `S134`, `S135`, `S147`, `S148`, `S154`, `S171`, `S191`, `S194`, `S198`, `S201`, `S212`, `S214`, `S262`, `S266`
- **Related Modules**：MySQL, Redis

---

## 5. API / Auth / Distributed Service

### AIBE-021 · 一个 Production REST API 应怎样设计 Method、Error、Idempotency、Versioning 与演进边界？
- **Topic**：API Design
- **Question Type**：System Design
- **Depth**：L3
- **Source Count**：**2**
- **Evidence Sources**：`S091`, `S203`

### AIBE-022 · Authentication 与 Authorization 怎样区分？Access Token / Refresh Token、Session、OAuth2 和服务端权限边界怎样设计？
- **Topic**：Auth / Permission
- **Question Type**：Concept / System Design
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S035`, `S105`, `S119`, `S171`, `S183`, `S206`, `S254`, `S268`
- **Related Modules**：Redis, Agent Harness / Runtime

### AIBE-023 · 多实例 Session / Token 状态怎样共享与路由？服务无状态化与 Sticky Session 怎样取舍？
- **Topic**：Session / Routing
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S171`, `S181`, `S229`
- **Related Modules**：Redis, Agent Harness / Runtime

### AIBE-024 · Service Discovery 与 Load Balancing 怎样工作？DNS / Nginx / Registry / Heartbeat 的边界是什么？
- **Topic**：Service Discovery / Load Balancing
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**5**
- **Evidence Sources**：`S096`, `S110`, `S112`, `S188`, `S229`

### AIBE-025 · Global Unique ID 怎样生成？Snowflake、自增 ID、随机 ID 的唯一性、趋势递增与可用性如何权衡？
- **Topic**：Distributed ID
- **Question Type**：System Design / Trade-off
- **Depth**：L3
- **Source Count**：**4**
- **Evidence Sources**：`S013`, `S086`, `S089`, `S253`
- **Related Modules**：MySQL

---

## 6. Deployment / Observability / Operations

### AIBE-026 · Linux 线上服务出现 CPU、Memory、Disk、Port / Process 异常时怎样系统排查？
- **Topic**：Linux Troubleshooting
- **Question Type**：Troubleshoot
- **Depth**：L3
- **Source Count**：**6**
- **Evidence Sources**：`S070`, `S129`, `S178`, `S183`, `S206`, `S241`

### AIBE-027 · Docker / Container 解决什么问题？Container 与 Host 的 Process、Network、Filesystem、Resource Isolation 有什么边界？
- **Topic**：Docker / Container
- **Question Type**：Concept / Comparison
- **Depth**：L3
- **Source Count**：**7**
- **Evidence Sources**：`S037`, `S183`, `S187`, `S206`, `S221`, `S241`, `S254`

### AIBE-028 · Kubernetes 在 AI Service / Agent Backend 中承担哪些 Deployment、Scaling、Isolation 与 Availability 能力？
- **Topic**：Kubernetes
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**3**
- **Evidence Sources**：`S037`, `S187`, `S241`

### AIBE-029 · Production Backend Observability 应如何组织 Metrics、Log、Trace，并从一次请求定位到具体服务 / 进程 /依赖故障？
- **Topic**：Backend Observability
- **Question Type**：Troubleshoot / System Design
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S066`, `S108`, `S109`, `S156`, `S183`, `S221`
- **Related Modules**：Agent Harness / Runtime

### AIBE-030 · Configuration Center / Dynamic Config 怎样实现优先级、热更新、监听、失败回退与版本治理？
- **Topic**：Configuration Management
- **Question Type**：System Design / Reliability
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S036`, `S051`, `S088`

### AIBE-031 · Monolith 到 Microservice 应怎样拆边界？DDD、Gateway、RPC / MQ、Config、Transaction 与 Observability 如何协同？
- **Topic**：Microservice / DDD
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**5**
- **Evidence Sources**：`S051`, `S053`, `S171`, `S172`, `S203`

---

## 7. Backend Ecosystem Signals

### AIBE-032 · Spring / Spring Boot 的 Bean Lifecycle、Dependency Injection、AOP / Proxy 与 MVC Request Flow 怎样工作？
- **Topic**：Java / Spring
- **Question Type**：Concept / Deep Dive
- **Language / Ecosystem**：Java / Spring
- **Depth**：L2
- **Source Count**：**6**
- **Evidence Sources**：`S116`, `S172`, `S188`, `S191`, `S203`, `S232`

### AIBE-033 · Java 并发中的 `synchronized`、`ReentrantLock`、CAS / AQS 与 Concurrent Collection 怎样选择？
- **Topic**：Java Concurrency
- **Question Type**：Comparison / Deep Dive
- **Language / Ecosystem**：Java
- **Depth**：L3
- **Source Count**：**8**
- **Evidence Sources**：`S025`, `S116`, `S133`, `S137`, `S188`, `S192`, `S214`, `S232`

### AIBE-034 · JVM Memory Area、Class Loading 与 GC 怎样工作？OOM / Memory Leak 出现时如何定位？
- **Topic**：JVM Runtime
- **Question Type**：Concept / Troubleshoot
- **Language / Ecosystem**：Java / JVM
- **Depth**：L3
- **Source Count**：**12**
- **Evidence Sources**：`S104`, `S116`, `S125`, `S145`, `S152`, `S159`, `S174`, `S188`, `S190`, `S192`, `S216`, `S229`

### AIBE-035 · Java HashMap / ConcurrentHashMap 的底层结构、Resize、树化与并发安全怎样理解？
- **Topic**：Java Collection
- **Question Type**：Concept / Deep Dive
- **Language / Ecosystem**：Java
- **Depth**：L2
- **Source Count**：**7**
- **Evidence Sources**：`S117`, `S145`, `S188`, `S192`, `S202`, `S214`, `S232`

### AIBE-036 · ThreadLocal 的实现、生命周期和 Memory Leak 风险是什么？在线程池中怎样正确清理？
- **Topic**：ThreadLocal
- **Question Type**：Concept / Troubleshoot
- **Language / Ecosystem**：Java
- **Depth**：L3
- **Source Count**：**8**
- **Evidence Sources**：`S020`, `S089`, `S091`, `S137`, `S185`, `S191`, `S214`, `S232`

### AIBE-037 · Go Goroutine / GMP / Channel 与 Thread / Mutex 的核心差异是什么？Runtime 怎样调度大量并发任务？
- **Topic**：Go Runtime
- **Question Type**：Concept / Comparison
- **Language / Ecosystem**：Go
- **Depth**：L3
- **Source Count**：**8**
- **Evidence Sources**：`S110`, `S160`, `S166`, `S170`, `S188`, `S195`, `S214`, `S259`

### AIBE-038 · SSRF、CSRF、SQL Injection、XSS、Reverse Shell 与 Container Escape 等常见安全风险怎样理解和防护？
- **Topic**：Backend Security
- **Question Type**：Concept / Security / System Design
- **Depth**：L4
- **Source Count**：**4**
- **Evidence Sources**：`S089`, `S221`, `S254`, `S270`
- **Related Modules**：Agent Harness / Runtime

### AIBE-039 · 结构化业务事实、Cache、Session 与 Runtime State 应怎样在 MySQL / Redis 等存储之间分层？
- **Topic**：Data Layering
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Source Count**：**11**
- **Evidence Sources**：`S090`, `S092`, `S097`, `S118`, `S160`, `S178`, `S181`, `S194`, `S212`, `S214`, `S273`
- **Related Modules**：MySQL, Redis, Agent Harness / Runtime

---

## 8. Global Merge / Split Audit 修正

旧 `AIBE-029` 把“通用后端 Metrics / Log / Trace”和“Agent Runtime 的 step / tool / model 级执行 Trace”放在同一个 Canonical 中。全局审计后拆开：

- `AIBE-029` 只保留 Production Backend 的通用可观测性，证据为 `S066`, `S108`, `S109`, `S156`, `S183`；
- `S146`, `S240`, `S242` 明确追问 Agent 长任务 / 多层 Agent 的执行 Trace、节点故障与 Token Usage，迁入新建 `AGENT-043`；
- 另把 `S034`, `S129` 中明确的 Agent 卡住定位 / Trace Replay 证据一并归入 `AGENT-043`。

这两个 Canonical 允许互为 Related Module，但不再用同一个问题标题重复计算同一能力。

---

## 9. 新体系下的主干

```text
Protocol / Streaming
        ↓
Concurrency / Async / MQ
        ↓
Reliability / Idempotency / Rate Limit
        ↓
Data Layering / Cache Consistency
        ↓
Auth / Session / Distributed Service
        ↓
Deployment / Backend Observability / Operations
```

Java / Go 相关题作为真实市场信号保留；未来课程以 Python 主线讲通用工程原理，再用这些来源校准跨语言面试覆盖。