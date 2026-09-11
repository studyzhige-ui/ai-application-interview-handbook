# System Design｜AI Application / Agent Production 终局模块

> **Status：✅ 第一版完整系统教材已完成。** 当前为 `19` 个连续知识小板块 + Review + Interview 三件套；24 道 System Design Canonical 已按场景/能力映射进入教材，而不是一题一章。

> System Design 是这套 Handbook 的最后一个正式一级模块。
>
> 它不再重新讲 MySQL、Redis、Vector DB、RAG 或 Agent Harness 的单点原理，而是回答：**面对一个真实需求，怎样把前面所有能力组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的系统。**

> **课程原则：知识体系演进顺序优先。** 冻结 `S001–S279` 中的 24 道 System Design Canonical 只用于校准真实场景、Failure、Scale、Trade-off 与追问深度；不会采用 `1 Canonical = 1 Markdown`。

---

## 1. 为什么 System Design 放在最后

前面九块分别教会你：

```text
Python / FastAPI / Backend
→ 服务怎样运行

MySQL / Redis / Vector DB
→ 状态怎样存、索引、缓存和扩展

LLM / RAG / Agent Harness
→ 模型、Evidence、Agent Runtime 怎样工作
```

System Design 需要把这些局部能力重新组合：

```text
Requirement
→ SLO / Constraint
→ Workload
→ API / Data / State
→ Data Flow
→ Scale
→ Consistency
→ Reliability
→ Security
→ Observability
→ Cost
→ Evolution
```

这也是为什么它不能从“秒杀系统标准答案”开始。

---

## 2. 真人面经怎样影响这一模块

当前冻结研究中：

- System Design：**24 道 Canonical**；
- **71 个**独立 HUMAN-A 来源覆盖；
- 24/24 都是 **L4**；
- 强信号包括 Production Agent Backend、Long-running Agent、Flash Sale / Inventory、Enterprise RAG、Multi-tenant AI Platform、大规模 Batch / Migration 等。

因此面经会影响：

```text
哪些 Failure 必须讲
哪些场景必须做综合 Case
面试官会怎样从正常路径追到 Scale / Failure / Verification
Review / Interview 的复习权重
```

但不会影响：

```text
Requirement 必须先于架构
Workload 必须先于容量方案
State Ownership 必须先于 Consistency
正常路径必须先于 Failure Handling
Evaluation 必须进入最终闭环
```

---

## 3. 外部权威资料的角色

System Design 还参考 AWS Builders' Library、Google SRE / Cloud Architecture、Stripe API 等官方资料中的稳定工程原则，例如：

- Timeout / Retry / Exponential Backoff / Jitter；
- Overload / Cascading Failure / Load Shedding；
- Failure Domain / Redundancy；
- Idempotency Key；
- SLO / Capacity / Degradation。

这些资料只补工程原则，**不计入 HUMAN-A Source Count**。

---

# 4. 正式 19 个知识小板块

## Part A｜先学“怎样设计”，再学“设计什么”

1. [System Design 的职责与完整答题框架](docs/01-SystemDesign职责与答题框架.md)
2. [Requirement、SLO、Constraint 与 Scope](docs/02-Requirement与SLO.md)
3. [Workload、Capacity、Hotspot 与数量级估算](docs/03-Workload与CapacityEstimation.md)
4. [API、Data Model 与 State Ownership](docs/04-API数据模型与StateOwnership.md)
5. [Sync / Async、Data Flow 与 State Machine](docs/05-DataFlow与StateMachine.md)
6. [Cache、Hot Path 与 Read / Write Path](docs/06-Cache与HotPath.md)
7. [Partition、Routing、Fan-out 与 Rebalance](docs/07-PartitionRouting与Fanout.md)
8. [Consistency、Idempotency、Transaction 与 Compensation](docs/08-Consistency与Idempotency.md)
9. [Queue、Backpressure 与 Long-running Task](docs/09-QueueBackpressure与LongRunningTask.md)
10. [Timeout、Retry、Failover、Degradation 与 Load Shedding](docs/10-Reliability与Overload.md)
11. [Multi-tenancy、Security、Permission 与 Isolation](docs/11-MultiTenancy与Security.md)
12. [Observability、Evaluation、Cost 与 Evolution](docs/12-ObservabilityEvaluation与Evolution.md)

## Part B｜把通用方法迁移到真人高频场景

13. [High-concurrency Transactional Systems：秒杀、库存、Rate Limit、Token Refresh](docs/13-HighConcurrencyTransactionalSystems.md)
14. [Realtime Read-heavy Systems：排行榜、Feed、Autocomplete、Notification](docs/14-RealtimeReadHeavySystems.md)
15. [Large-scale Data & Processing：10TB Storage、Migration、Dedup、Large-file](docs/15-LargeScaleDataProcessingSystems.md)
16. [LLM Gateway 与 Multi-tenant AI Platform](docs/16-LLMGateway与MultiTenantAIPlatform.md)
17. [Enterprise / Large-scale RAG System Design](docs/17-EnterpriseRAGSystemDesign.md)
18. [Production Agent Backend 与 Long-running Agent](docs/18-ProductionAgentBackend.md)
19. [Vertical AI Agent Patterns：Analysis、Customer Service、Multimodal、Game、Content](docs/19-VerticalAIAgentPatterns.md)

---

## 5. 24 道 Canonical 怎样进入 19 个板块

Canonical 不和教材文件一一对应，而主要作为 Part B 的 Case / Drill：

```text
SD-001 / 009 / 010 / 011
→ 13 High-concurrency Transactional

SD-002 / 003 / 004 / 005
→ 14 Realtime Read-heavy

SD-006 / 007 / 008 / 012 / 015
→ 15 Large-scale Data & Processing

SD-013 / 014
→ 16 LLM Gateway / Multi-tenant AI Platform

SD-016 / 017
→ 17 Enterprise / Large-scale RAG

SD-021 / 022
→ 18 Production / Long-running Agent Backend

SD-018 / 019 / 020 / 023 / 024
→ 19 Vertical AI Agent Patterns
```

同一个 Scenario 还会反向链接 Part A。例如“秒杀”不是背一个固定架构，而是用它训练：

```text
Requirement
→ Capacity
→ Hot Path
→ Consistency
→ Idempotency
→ Queue
→ Failure
→ Observability
```

---

## 6. System Design 面试默认六层追问

根据已核验真人追问链，面试通常不是连续定义题，而是：

```text
你设计什么？
→ 为什么这样设计？
→ 内部机制是什么？
→ 失败怎么办？
→ 量大 / 热点 / 多租户怎么办？
→ 怎么证明它真的工作？
```

因此每章默认训练：

```text
Concept
→ Mechanism
→ Trade-off
→ Failure
→ Scale
→ Verification
```

---

## 7. 模块边界

System Design 负责**组合与决策**，不重复基础模块完整原理：

| 问题 | Primary |
|---|---|
| B+Tree / MVCC / Lock | MySQL |
| Redis TTL / Cluster / Lock 实现 | Redis |
| HNSW / IVF | Vector DB |
| KV Cache / Sampling | LLM Foundation |
| Chunk / Hybrid / Rerank | RAG |
| Agent Loop / Tool / Context / Checkpoint | Agent Harness |
| Timeout / Retry / Queue / Backpressure 的通用机制 | AI Backend Engineering |
| 上述能力怎样组合成完整系统 | **System Design** |

System Design 章节会提供必要摘要，但会明确链接到 Primary Module。

---

## 8. 推荐三遍学习法

第一遍按 `01 → 12` 学设计方法；第二遍读 `13 → 19`，每个 Case 先自己画再看正文；第三遍进入：

- [`review/README.md`](review/README.md)
- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

最终目标不是背架构图，而是面对陌生题也能稳定走完：

```text
Clarify
→ Quantify
→ Model State
→ Draw Flow
→ Find Bottleneck
→ Choose Trade-off
→ Break It
→ Verify It
```
