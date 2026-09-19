# 16. Service Discovery、Load Balancing、Stateless Routing 与 Distributed ID

> 当服务从 1 个实例变成 10 个、100 个实例以后，核心问题变成：**客户端怎样找到服务、请求怎样分配、状态怎样避免绑死实例、全局 ID 怎样生成。**

## 1. 单实例时代没有“发现”问题

```text
Client
→ 10.0.0.7:8080
```

但多实例：

```text
Service A
├─ instance-1
├─ instance-2
├─ instance-3
└─ instance-4
```

实例会：

- 启动；
- 下线；
- Crash；
- 扩容；
- IP 变化。

调用方不能硬编码地址。

---

## 2. Service Discovery 的基本问题

需要维护：

```text
service name
→ healthy instances
```

常见实现思路：

- DNS；
- Registry；
- Kubernetes Service；
- Proxy / Service Mesh。

它们都是在回答：

> 当前哪些实例可以接流量？

---

## 3. DNS Discovery

```text
api.internal
→ multiple addresses
```

优点：

- 通用；
- 简单；
- 各语言都支持。

边界：

- TTL / cache；
- 更新不一定瞬时；
- 健康信息表达能力有限。

所以 DNS 可以用于 Service Discovery，但不能假设它是毫秒级强一致 Registry。

---

## 4. Registry + Heartbeat

另一种模型：

```text
instance registers
→ heartbeat
→ registry
→ client / proxy watches
```

如果一段时间没 Heartbeat：

```text
mark unhealthy
```

问题仍然包括：

- false positive；
- network partition；
- stale registry data；
- recovery race。

---

## 5. Load Balancing

发现多个实例以后，需要决定请求发给谁。

常见策略：

- round robin；
- random；
- least connections；
- weighted；
- latency-aware；
- consistent hashing。

没有“永远最好”。

例如 Streaming Service 更关注 active connections，普通短请求可能更适合 round robin。

---

## 6. Client-side vs Server-side LB

### Server-side / Proxy

```text
Client
→ LB / Gateway
→ instances
```

客户端简单。

### Client-side

```text
Client gets instance list
→ chooses instance
```

少一跳，但客户端需要 Discovery / Health / Retry 逻辑。

---

## 7. Health 与 Routing

实例刚启动：

```text
process alive
```

不代表：

```text
model loaded
DB connected
cache warm
ready to receive traffic
```

所以 Discovery / LB 通常与 Readiness 概念结合。

Kubernetes 章节会继续展开。

---

## 8. Stateless Service

水平扩容最舒服的服务：

```text
request can hit any instance
```

关键状态外置：

```text
DB / Redis / Object Store / MQ / Checkpoint Store
```

这不意味着服务“完全没有内存状态”。

它仍可能有：

- connection pool；
- local cache；
- in-flight request；
- loaded model config。

Stateless 更准确是：

> 实例不是长期业务事实的唯一拥有者。

---

## 9. Sticky Session

有时 LB 按 Cookie / IP / Hash 把同用户固定到同一实例。

适合：

- WebSocket connection；
- local cache affinity；
- 某些 legacy session。

但要考虑：

- instance crash；
- rebalance；
- scale-in；
- unequal load。

因此 Sticky 可以优化，但不要成为 durable state 的唯一保障。

---

## 10. Consistent Hashing

适合把 Key 稳定映射到节点：

```text
key
→ hash ring
→ node
```

节点增删时，只迁移部分 Key。

常见于：

- cache sharding；
- state partition；
- routing affinity。

但 HotKey 仍可能让某节点特别热。

---

## 11. Global Unique ID 为什么不总用自增

单库自增简单，但分库分表 / 多 Region 后：

```text
DB A id=100
DB B id=100
```

会冲突。

需要全局 ID 策略。

---

## 12. UUID

优点：

- 无中心生成；
- 冲突概率极低；
- 适合分布式。

代价：

- 字符串/128-bit 存储；
- 随机写可能影响某些 B+Tree Locality；
- 不天然趋势递增；
- 可读性差。

MySQL 章节已经讨论随机主键对 InnoDB 的影响。

---

## 13. Snowflake 思想

典型组成：

```text
timestamp
+ worker / region bits
+ sequence
```

得到趋势递增且分布式生成的 ID。

需要解决：

- worker id 唯一；
- clock rollback；
- sequence exhaustion；
- bit allocation。

不要只背“64 位”。不同实现位数可以不同。

---

## 14. ID 的真正需求

先问：

```text
是否必须全局唯一？
是否需要趋势递增？
是否允许暴露业务量？
是否需要本地生成？
是否排序？
是否数据库主键？
```

没有一种 ID 适合所有场景。

---

## 15. AI 场景：Run ID / Event ID / Task ID

常见：

```text
run_id
step_id
tool_call_id
task_id
event_id
```

这些 ID 不只是数据库主键，还参与：

- trace correlation；
- idempotency；
- resume；
- event ordering；
- audit。

因此要定义稳定语义。

---

## 16. Failure Timeline

服务扩容：

```text
new instance starts
→ registered too early
→ traffic arrives
→ model/client pool not ready
→ errors
→ LB marks unhealthy
→ retry to other instances
→ load spike
```

所以 Readiness 比“进程启动成功”更重要。

---

## 17. 🎯 面试怎么答

**问：Service Discovery 和 Load Balancing 有什么区别？**

可以回答：

> Service Discovery 解决“当前有哪些可用实例”，Load Balancing 解决“这次请求选哪个实例”。DNS、Registry、Kubernetes Service 等都可以参与 Discovery；LB 再根据 round robin、least connections、weighted 等策略分配流量。两者都需要结合 Health / Readiness，否则可能持续把请求发给不可用实例。

---

## 18. ⚠️ 易错点

- Stateless ≠ 进程内完全没有状态；
- DNS ≠ 实时 Registry；
- Sticky Session ≠ 高可用；
- 加实例 ≠ 下游容量自动增加；
- Snowflake ≠ 所有实现固定同一 Bit Layout；
- UUID ≠ 永远不适合作主键，要结合 DB/索引与访问模式。

---

## 19. 本章自测

<details>
<summary>1. Service Discovery 与 Load Balancing 的输入输出分别是什么？</summary>

Discovery 输出可用实例集合；Load Balancing 基于这个集合和策略选择本次请求的目标实例。

</details>

<details>
<summary>2. 为什么 Stateless Service 更容易水平扩容？</summary>

因为任意实例都可以处理请求，业务事实不依赖某个实例内存。实例增删时不需要迁移唯一业务状态。

</details>

<details>
<summary>3. 选择 Distributed ID 前最重要的问题是什么？</summary>

先明确唯一性、排序、趋势递增、本地生成、隐私/业务量暴露和数据库索引等需求，再选 UUID、Snowflake、自增或其它方案。

</details>