# Agent｜组织模型判断、程序行动、状态恢复与交付验证

[← RAG](../08-rag/README.md) · [课程目录](../README.md) · [Handbook](../../README.md) · [System Design →](../10-system-design/README.md)

从一项可验证任务建立循环，再理解工具、计划、上下文、记忆、权限、协作和生产运行。

## 学习前提与目标

先了解模型调用、应用接口与 RAG，能区分生成文字、工具执行和外部副作用。

学完后应能组织模型判断、程序行动、状态恢复与交付验证。

## 学习顺序

1. [01. Agent 系统的全貌：模型之外，谁把任务做完](docs/01-AgentSystemAndResponsibilities.md)
2. [02. Workflow 与 Agent：哪些决定交给模型](docs/02-WorkflowAutonomyAndRuntimeBoundary.md)
3. [03. Agent Loop：观察怎样改变下一步](docs/03-AgentLoopAndExecutionScopes.md)
4. [04. 工具契约：模型提出什么，程序检查什么](docs/04-ToolContractAndValidation.md)
5. [05. 工具注册与发现：程序有的，不一定都给模型看](docs/05-ToolRegistrationAndDiscovery.md)
6. [06. 工具结果与失败：谁来修，怎样继续](docs/06-ToolExecutionAndFailure.md)
7. [07. 工具并发与取消：快一点，不等于可以乱序](docs/07-ToolConcurrencyAndCancellation.md)
8. [08. 计划与停止：让每一步朝目标推进](docs/08-PlanningGoalAndControl.md)
9. [09. 上下文编排：模型这一刻到底收到什么](docs/09-ContextAssemblyAndCache.md)
10. [10. 上下文压缩：缩短输入以后，怎样继续做对](docs/10-CompactionAndContinuation.md)
11. [11. 记忆：把有用经验带到以后，也能纠错和忘记](docs/11-MemoryLifecycle.md)
12. [12. 状态与持久化：程序怎样知道工作做到哪里](docs/12-StateHistoryAndPersistence.md)
13. [13. 检查点与恢复：保存之后、崩溃之前发生了什么](docs/13-CheckpointResumeAndRecovery.md)
14. [14. 权限、批准与沙箱：一次动作要过几道不同的门](docs/14-PermissionApprovalAndSandbox.md)
15. [15. 提示注入与信息保护：资料为什么不能变成命令](docs/15-InjectionAndContainment.md)
16. [16. MCP：从 Host / Client / Server 到完整协议往返](docs/16-MCPArchitectureAndLifecycle.md)
17. [17. Skills、Hooks 与 Plugins：知识怎样加载，规则怎样触发](docs/17-SkillsHooksAndExtensions.md)
18. [18. 路由与模型适配：换一条路径，不能丢掉任务保证](docs/18-RoutingAndProviderResilience.md)
19. [19. 多 Agent 协作：交出去的是任务，不是全部控制权](docs/19-MultiAgentAndA2A.md)
20. [20. 执行追踪：先定位卡在哪，再取需要的证据](docs/20-TraceReplayAndDiagnosis.md)
21. [21. Agent 评测：怎样证明修改真的更好](docs/21-EvaluationBenchmarkAndImprovement.md)
22. [22. Coding Agent：从理解仓库到交付可验证修改](docs/22-CodingAgentDelivery.md)
23. [23. 生产运行：从任务承诺推导部署，而不是先画微服务](docs/23-ProductionRuntime.md)
24. [24. 框架选型：先问要保证什么，再看谁能实现](docs/24-FrameworkSelection.md)

## 正文与复习

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界，再用章末自测检查能否独立解释。第二遍使用 [Review](review/README.md)重建关系，并改变条件验证结论。

面试准备集中在 [本知识域](../../interview/09-agent/README.md)：[高频面试题](../../interview/09-agent/01-高频面试题.md)、[易混易错点](../../interview/09-agent/02-易混易错点.md)与[面试速查](../../interview/09-agent/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
