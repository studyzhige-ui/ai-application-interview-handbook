# 20. Configuration、Feature Flag、Gray Release 与 Microservice Evolution

> Production 系统不只是“代码版本”，还有配置、Feature、模型、Prompt、依赖和服务边界的持续变化。真正稳定的系统必须把 **Change** 本身当作一等工程对象。

## 1. 为什么 Configuration 需要治理

配置可能包括：

```text
DB endpoint
model name
provider quota
feature switch
retry count
timeout
rate limit
prompt version
retrieval top_k
```

如果配置散落在代码和环境里：

- 谁改了不知道；
- 不同实例不一致；
- 无法快速回滚；
- Debug 无法复现。

---

## 2. Config Priority

常见来源：

```text
default
→ config file
→ env
→ remote config
→ runtime override
```

必须定义明确优先级。

否则同一个值到底来自哪里很难排查。

---

## 3. Dynamic Config

远程配置中心可以：

```text
publish new version
→ instances watch / poll
→ validate
→ apply
```

优势：

- 不发版即可调整；
- 快速止损；
- 多实例一致分发。

风险：

- 错配置瞬间全量扩散；
- watcher bug；
- config center outage；
- incompatible schema。

所以“动态”更需要治理。

---

## 4. Safe Config Update

推荐：

```text
fetch config
→ schema validate
→ semantic validate
→ stage
→ atomically swap
→ keep previous version
```

不要直接边读边修改一个全局 dict。

失败时：

```text
keep last-known-good config
```

---

## 5. Config Version

Trace / Log 中记录：

```text
config_version
```

否则 P99 变差以后无法判断：

> 是代码变了，还是 Timeout/Rate Limit 配置变了？

AI Service 还要记录：

```text
model_version
prompt_version
retrieval_config_version
```

---

## 6. Feature Flag

Feature Flag 把“代码已经部署”和“功能对谁生效”分离。

```text
code deployed
feature disabled
↓
enable 1%
↓
10%
↓
100%
```

用途：

- 灰度；
- A/B Test；
- emergency kill switch；
- tenant-specific feature。

---

## 7. Feature Flag 的 Debt

Flag 不能永远留着。

长期会产生：

```text
2^N code paths
```

应该有：

- owner；
- expiry；
- remove plan；
- audit。

否则测试复杂度爆炸。

---

## 8. Gray / Canary Release

```text
new version
→ 1% traffic
→ observe
→ 10%
→ 50%
→ 100%
```

监控：

- error rate；
- P95/P99；
- business metric；
- AI quality metric；
- cost；
- tenant-specific error。

如果只看 CPU 正常就继续放量，AI 行为可能已经 Regression。

---

## 9. Rollback 不是永远简单

Code 可以回滚，但：

```text
DB schema changed
Event schema changed
new data already written
model output format changed
```

旧代码可能无法读取新数据。

所以安全发布常要求：

- backward compatible schema；
- expand/contract migration；
- versioned event；
- dual-read / dual-write（谨慎）。

---

## 10. Monolith vs Microservice

Monolith 不是“落后架构”。

优点：

- local transaction；
- 简单部署；
- Debug 容易；
- 调用成本低。

Microservice 的价值可能是：

- 团队边界；
- 独立扩容；
- failure isolation；
- independent deploy；
- technology boundary。

代价：

- network failure；
- distributed transaction；
- observability；
- versioning；
- service discovery。

---

## 11. 什么时候拆服务

不要按数据库表拆。

更合理考虑：

```text
Business Capability
Ownership
Change Frequency
Scale Pattern
Failure Boundary
Data Ownership
```

例如：

```text
Billing
Ingestion
Inference Gateway
Agent Runtime
```

可能有不同扩容和故障模型。

---

## 12. DDD 的价值边界

DDD 在本课程只需要掌握：

- Bounded Context；
- Domain Boundary；
- Aggregate / Invariant 的直觉；
- ubiquitous language。

它不是“必须使用某套 Java 框架”。

核心价值是：

> 把服务边界和业务边界对齐，而不是按技术 Layer 乱拆。

---

## 13. Gateway

API Gateway 常负责：

- routing；
- auth entry；
- rate limit；
- request normalization；
- observability context。

不要把所有业务逻辑塞 Gateway。

否则 Gateway 会成为巨大单点逻辑层。

---

## 14. Microservice Communication

服务拆开以后需要选择：

```text
sync HTTP/RPC
vs
async Event/MQ
```

依据仍是前面第三章：

- 是否需要立即结果；
- Failure 怎样传播；
- 是否需要 Buffer；
- consistency requirement。

---

## 15. Distributed Transaction

拆服务前的本地 Transaction：

```text
one DB transaction
```

拆后：

```text
Service A DB
Service B DB
```

不能再假设本地 ACID 跨服务成立。

必须引入：

- Outbox；
- Saga；
- Compensation；
- Reconciliation。

这就是为什么 Microservice 不是免费的。

---

## 16. AI Config 特别容易造成 Silent Regression

例如只改：

```text
top_k: 20 → 5
model: large → small
max_steps: 10 → 4
```

服务可能没有任何 500，但质量下降。

所以 AI Config 需要同时监控：

```text
reliability metric
+ quality/eval metric
```

---

## 17. Kill Switch

高风险功能最好具备快速禁用开关：

```text
new tool
new provider
agent autonomous action
experimental reranker
```

事故时比等代码重新构建部署更快。

但 Kill Switch 本身也要有权限和审计。

---

## 18. 🎯 面试怎么答

**问：Monolith 什么时候应该拆 Microservice？**

可以回答：

> 我不会把 Microservice 当成熟度指标。先看是否出现清晰业务边界、独立团队 Ownership、不同 Scale Pattern、独立发布需求或 Failure Isolation 需求。拆分后会引入网络 Failure、分布式一致性、服务发现和可观测性成本，所以只有收益明显时才拆。服务边界应更接近 Business Capability / Data Ownership，而不是一张表一个服务。

---

## 19. ⚠️ 易错点

- Dynamic Config ≠ 随便热改；
- Feature Flag ≠ 永久 if/else；
- Rollback ≠ 数据一定可回滚；
- Microservice ≠ 一定更先进；
- DDD ≠ 只属于 Java；
- Canary 只看 Error Rate 不够，AI 还要看质量。

---

## 20. 本章自测

<details>
<summary>1. 为什么 Remote Config 更新最好原子替换而不是原地修改？</summary>

避免多个请求读到半更新状态；先完整校验新版本，再一次切换引用，可以让配置版本更明确，也便于保留 last-known-good 回滚。

</details>

<details>
<summary>2. 为什么 Microservice 会放大一致性难度？</summary>

原本一个数据库事务内的操作被拆到多个服务/数据库后，无法再依赖单个 ACID Transaction，需要事件、Saga、补偿和对账等机制。

</details>

<details>
<summary>3. AI Feature Gray Release 为什么要看质量指标？</summary>

Prompt/Model/Retrieval 配置可能不产生 HTTP Error，却显著降低答案质量；只看 CPU/5xx 无法发现 Silent Regression。

</details>