# System Design｜AI Application / Agent Production 系统设计

[← Agent](../agent/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：19 个连续知识小板块** · **HUMAN-A Canonical：24** · **独立来源覆盖：71**  
> **质量：Granularity / Coverage / Content Depth 已验收**

把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。


---

## 1. 这个模块解决什么

把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。

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

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent](../agent/README.md) → **System Design**

当前模块角色：**Integration / 把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。**

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

所以本模块是 **24 道 Canonical → 19 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Requirement / SLO → Workload / Capacity → API / Data / State → Flow / Cache / Partition → Consistency / Queue → Reliability / Security → Observability / Evaluation / Cost / Evolution → High-concurrency / Realtime / Data Processing / LLM Gateway / Enterprise RAG / Production Agent Cases
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜通用 System Design 方法

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

### Part B｜真人高频 Scenario Patterns

13. [High-concurrency Transactional Systems：秒杀、库存、Rate Limit、Token Refresh](docs/13-HighConcurrencyTransactionalSystems.md)
14. [Realtime Read-heavy Systems：排行榜、Feed、Autocomplete、Notification](docs/14-RealtimeReadHeavySystems.md)
15. [Large-scale Data & Processing：10TB Storage、Migration、Dedup、Large-file](docs/15-LargeScaleDataProcessingSystems.md)
16. [LLM Gateway 与 Multi-tenant AI Platform](docs/16-LLMGateway与MultiTenantAIPlatform.md)
17. [Enterprise / Large-scale RAG System Design](docs/17-EnterpriseRAGSystemDesign.md)
18. [Production Agent Backend 与 Long-running Agent](docs/18-ProductionAgentBackend.md)
19. [Vertical AI Agent Patterns：Analysis、Customer Service、Multimodal、Game、Content](docs/19-VerticalAIAgentPatterns.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **24 道 Primary Canonical、71 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- Production / Long-running Agent Backend
- Flash Sale / Inventory
- Enterprise RAG
- Multi-tenant AI Platform
- Large-scale Data / Migration
- Vertical AI Agent Scenarios

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- System Design 负责组合与决策，不重复单点机制的完整原理。
- Timeout / Retry / Queue / Backpressure 的机制归 AIBE。
- MySQL / Redis / Vector / RAG / Agent 的内部机制回到对应 Primary Module。

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

- [Canonical Questions](../research/questions/system-design.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 19` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–19 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

整套十板块已学完，可以进入全局 Review / 面试训练。
