# 02｜Requirement、SLO、Constraint 与 Scope

System Design 里最贵的错误通常不是“少画了一个组件”，而是：

> **你解决了一个并不存在的问题，或者根本没解决真正被要求的问题。**

所以第二章先训练需求与约束。

---

## 1. Functional Requirement：系统必须做什么

以 Notification Platform 为例：

```text
创建通知任务
→ 选择 Email / SMS / Push
→ 投递
→ 查询状态
```

这是功能。

但同一个“通知系统”，如果补充：

```text
金融 OTP 不能丢
营销消息允许延迟
单用户每天有配额
支持多租户模板
```

架构会完全不同。

---

# 2. Non-functional Requirement：做到什么程度

System Design 最常用的维度：

```text
Latency
Throughput
Availability
Durability
Consistency
Freshness
Ordering
Security
Cost
Operability
```

不要把这些全部说成“越高越好”。

例如：

```text
排行榜
→ 允许 1~5 秒 Freshness Lag

支付 / 库存
→ 正确性优先

Autocomplete
→ P99 Latency 极敏感

离线 Ingestion
→ Throughput 比单条 Latency 更重要
```

---

# 3. SLI / SLO / SLA 要分清

## SLI

实际测量值，例如：

```text
request_success_rate
P99 latency
index_freshness_lag
```

## SLO

内部目标，例如：

```text
99.9% requests < 300ms
99.95% success
```

## SLA

面向客户的承诺，通常还涉及合同与赔付。

面试不一定要求背术语，但需要有这种思维：

> “快”和“稳定”必须变成可测目标。

---

# 4. Consistency Requirement 不能只说“强一致”

先问业务语义：

```text
Read-your-write？
Monotonic Read？
库存不能负数？
余额不能错？
排行榜可以旧 2 秒？
RAG Knowledge 可以旧 10 分钟？
```

Consistency 应从**业务 invariant**定义。

例如库存真正要求的是：

```text
confirmed_order_count <= sellable_inventory
```

而不是抽象地说“我要 CP”。

---

# 5. Freshness 和 Consistency 不是一回事

RAG / Cache / Feed 很容易混淆。

```text
Consistency
→ 多个读写视图之间关系

Freshness
→ 看到的数据距离最新 Source 有多旧
```

一个系统可以：

```text
所有副本都一致
但一致地旧了 10 分钟
```

所以要单独定义 Freshness SLA。

---

# 6. Durability 与 Availability 也要分开

系统可用不代表数据不丢。

```text
Replica
→ 可以提升可用性

Backup / Durable Log
→ 更偏数据恢复
```

同样：

```text
服务暂时不可写
```

可能比：

```text
接受写入然后永久丢失
```

更符合某些业务。

---

# 7. Scope：面试时间有限，必须主动裁剪

面试题常故意很宽：

> 设计一个多租户 AI Platform。

你应该先声明 Scope，例如：

```text
本轮重点：
- Online Request Path
- Tenant Quota
- Model Routing
- Usage / Cost

暂不展开：
- Billing Settlement
- Region Compliance Detail
- Training Platform
```

这不是逃避，而是让讨论有边界。

---

# 8. Requirement Matrix

可以快速写：

| 维度 | 问题 | 示例 |
|---|---|---|
| Users | 谁使用？ | 10K tenants |
| Traffic | 峰值多少？ | 50K QPS |
| Latency | 多快？ | P99 300ms |
| Consistency | 哪些 invariant？ | 不重复扣库存 |
| Freshness | 可以旧多久？ | 5s |
| Durability | 能丢吗？ | 订单不可丢 |
| Availability | 故障时怎么办？ | 允许只读降级 |
| Security | 隔离什么？ | tenant / PII |
| Cost | 预算敏感吗？ | LLM token cost |

---

# 9. AI 系统需要额外问的约束

传统系统之外，AI Application 常加：

```text
Model Quality
Hallucination Risk
Prompt / Model Version
Token / GPU / API Cost
Provider Rate Limit
Evidence Freshness
Tool Side Effect
Human Approval
Evaluation Dataset
```

例如 Customer Service Agent：

```text
FAQ 可以自动回答
退款 > 1000 元必须人工批准
订单状态必须查实时 Tool
政策解释必须有 Citation
```

这些约束直接决定 RAG / Tool / HITL 分层。

---

# 10. 需求改变时，设计也应改变

如果面试官说：

> “现在 QPS 增加 100 倍。”

不要只回答“加机器”。

重新问：

```text
瓶颈在哪？
数据是否需要分片？
热点是否更严重？
下游容量是否同步增长？
Cost 是否还能接受？
```

System Design 是约束驱动，不是静态答案。

---

# 11. 🎯 面试怎么答

> 我会先把题目拆成 Functional Requirement 和 Non-functional Requirement，然后把“高并发、实时、可靠”这类模糊词变成 QPS、P99、Availability、Freshness、Durability 和业务一致性 invariant。对于 AI 系统还会明确模型质量、Provider 限流、Cost、Evidence Freshness 和高风险 Tool 的审批边界。最后主动声明本轮 Scope，避免在 40 分钟里把所有子系统都浅画一遍。

---

# 12. 本章自测

<details><summary>1. “库存强一致”为什么还不够准确？</summary>
应继续定义业务 invariant，例如确认订单数量不能超过可售库存、重复请求不能重复扣减，以及失败后哪一步允许补偿。
</details>

<details><summary>2. Freshness 与 Consistency 有什么区别？</summary>
Freshness 描述数据距离最新 Source 有多旧；Consistency 描述多个读写视图之间满足什么关系。
</details>

<details><summary>3. 为什么面试要主动声明 Scope？</summary>
因为时间有限，只有明确主问题和不展开的次要问题，才能把关键数据流、Failure 与 Trade-off 讲深。
</details>
