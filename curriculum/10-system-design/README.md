# System Design｜从需求推导容量、状态、协作与故障方案

[← Agent](../09-agent/README.md) · [课程目录](../README.md) · [Handbook](../../README.md)

从用户动作与完成条件建立方案，逐步推导容量、状态归属、数据流、可靠性与 AI 应用设计。

## 学习前提与目标

在前九个模块基础上练习整体取舍；按具体设计问题回看相关机制。

学完后应能从需求推导容量、状态、协作与故障方案。

## 学习顺序

1. [01｜系统设计：从用户的一次操作推导整套方案](docs/01-SystemDesign职责与答题框架.md)
2. [02｜需求与 SLO：怎样把“好用”变成可检查的承诺](docs/02-Requirement与SLO.md)
3. [03｜工作负载与容量：把请求换算成资源和费用](docs/03-Workload与CapacityEstimation.md)
4. [04｜API 与数据模型：谁拥有事实，谁可以改变它](docs/04-API数据模型与StateOwnership.md)
5. [05｜数据流与状态机：请求被接受以后，谁继续把它做完](docs/05-DataFlow与StateMachine.md)
6. [06｜缓存与热点：省下重复工作之后，怎样处理旧结果和回源](docs/06-Cache与HotPath.md)
7. [07｜分区、路由与聚合：数据拆开后，一次查询要找谁](docs/07-PartitionRouting与Fanout.md)
8. [08｜一致性与幂等：怎样守住不可破坏的业务条件](docs/08-Consistency与Idempotency.md)
9. [09｜队列与长任务：积压怎样形成，工作者怎样安全接管](docs/09-QueueBackpressure与LongRunningTask.md)
10. [10｜可靠性与过载：失败时怎样保护剩余的成功机会](docs/10-Reliability与Overload.md)
11. [11｜多租户与安全：同一套服务怎样守住不同用户的边界](docs/11-MultiTenancy与Security.md)
12. [12｜观测、评测与演进：怎样证明方案有效，怎样安全改变它](docs/12-ObservabilityEvaluation与Evolution.md)
13. [13｜高并发交易：让有限资源只被合法消耗一次](docs/13-HighConcurrencyTransactionalSystems.md)
14. [14｜实时读模型：怎样让用户看到正确的最近数据](docs/14-RealtimeReadHeavySystems.md)
15. [15｜大规模数据处理：让容量、查询与恢复共同成立](docs/15-LargeScaleDataProcessingSystems.md)
16. [16｜LLM 网关：把模型选择、交付和费用放进同一条请求链](docs/16-LLMGateway与MultiTenantAIPlatform.md)
17. [17｜企业 RAG：把知识更新、在线回答与权限治理组合起来](docs/17-EnterpriseRAGSystemDesign.md)
18. [18｜生产级 Agent 后端：让一次长任务跨越断线、重启与批准](docs/18-ProductionAgentBackend.md)
19. [19｜垂直 AI 系统：从领域规则推导证据、工具与验收](docs/19-VerticalAIAgentPatterns.md)

## 正文与复习

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界，再用章末自测检查能否独立解释。第二遍使用 [Review](review/README.md)重建关系，并改变条件验证结论。

面试准备集中在 [本知识域](../../interview/system-design/README.md)：[高频面试题](../../interview/system-design/01-高频面试题.md)、[易混易错点](../../interview/system-design/02-易混易错点.md)与[面试速查](../../interview/system-design/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

技术资料提供系统设计的进一步查证入口。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
