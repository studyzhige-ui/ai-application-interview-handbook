# Agent Harness / Runtime｜Agent 执行系统

[← RAG](../rag/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [System Design →](../system-design/README.md)

> **状态：✅ 第一版系统教材完成**
> **教材：23 个连续知识小板块** · **HUMAN-A Canonical：44** · **独立来源覆盖：166**
> **质量：结构与研究基线保留；2026-09-17已按读者反馈逐章重写讲解与训练，核验范围见阅读修订记录**

从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。

---

## 1. 这个模块解决什么

从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。

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

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → **Agent Harness / Runtime** → [System Design](../system-design/README.md)

当前模块角色：**Agent Runtime / 从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。**

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

所以本模块是 **44 道 Canonical → 23 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Agent Boundary / Loop → Tool Runtime → Planning / Control → Context Assembly / Compaction → Memory / Session / Checkpoint → Permission / Sandbox / Injection → MCP / Skills / Hooks / Routing → Multi-Agent / A2A → Trace / Eval / Coding Agent → Production Runtime / Framework Mapping
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜Agent 与 Runtime 基础

1. [Agent 系统的全貌：先知道谁在做什么](docs/01-AgentHarness在AI应用中的职责.md)
2. [Workflow、Agent 与 Harness 的边界](docs/02-AgentWorkflowHarnessBoundary.md)
3. [Agent 循环、执行层级与新消息](docs/03-AgentLoopRuntimeState.md)

### Part B｜Tool Runtime

4. [工具契约：模型可以请求什么，程序必须检查什么](docs/04-ToolContractSchemaValidation.md)
5. [工具注册、模型可见说明与按需发现](docs/05-ToolRegistryRouterDiscovery.md)
6. [工具结果与错误：哪些告诉模型，哪些由程序处理](docs/06-ToolExecutionFailure.md)
7. [副作用、并发与取消传播](docs/07-ToolSideEffectCancellation.md)

### Part C｜Planning 与 Context

8. [计划、ReAct 与停止：怎样让每一步朝目标推进](docs/08-PlanningGoalStopBudget.md)
9. [上下文编排：模型这一刻到底收到什么](docs/09-ContextAssemblyBudget.md)
10. [上下文压缩：什么时候压、压什么、怎样继续](docs/10-ContextCompactionCorrectness.md)

### Part D｜Memory、State 与 Long-running Reliability

11. [记忆生命周期：怎样记得有用，又能忘掉错误](docs/11-MemoryArchitectureLifecycle.md)
12. [状态与持久化：程序怎样记得工作做到哪里](docs/12-SessionStatePersistence.md)
13. [检查点与恢复：两次保存之间崩溃怎么办](docs/13-CheckpointResumeReliability.md)

### Part E｜Security、Capability 与 Multi-Agent

14. [权限、批准与沙箱：三道不同的问题](docs/14-PermissionApprovalSandbox.md)
15. [注入与信息保护：数据为什么不能变成命令](docs/15-GuardrailsInjectionContainment.md)
16. [MCP、Skill与Hook：外部能力怎样接进来](docs/16-MCPSkillsHooks.md)
17. [意图、模型与能力路由：把请求交给合适的对象](docs/17-RoutingProviderResilience.md)
18. [多Agent与A2A：分工、交接和跨系统任务](docs/18-MultiAgentA2AWorkspace.md)

### Part F｜Observability、Evaluation 与 Production

19. [Trace与排障：记录够用的信息，而不是保存整个世界](docs/19-TraceReplayObservability.md)
20. [Agent评测：从“跑完了”到“有证据说明做好了”](docs/20-AgentEvaluationBenchmark.md)
21. [Coding Agent：读懂仓库、最小修改与可验证交付](docs/21-CodingAgentWorkflow.md)
22. [生产Agent架构：从一个进程到可运营服务](docs/22-ProductionAgentRuntime.md)
23. [框架与自研怎么选：按官方核心语义做比较](docs/23-FrameworkMappingBuildVsBuy.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **44 道 Primary Canonical、166 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- Context Compaction
- Agent Loop
- Memory Architecture
- Tool Calling / Failure
- Multi-Agent
- Agent Evaluation
- Framework Selection

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- Prompt Engineering 归 LLM Foundation；Harness 负责跨轮、跨 Tool、跨 State 的执行。
- RAG 负责 Evidence Quality；Agent Harness 决定何时检索、如何继续执行。
- 通用 MQ / Retry / Idempotency 归 AIBE；Agent 只讲其 Runtime 特化语义。

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

- [Canonical Questions](../research/questions/agent-harness.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [权威技术 / 源码资料索引](../research/agent-sources/README.md)：只校准技术事实，不改变 HUMAN-A 频率；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

每章先用中文和例子解释概念，再展开机制；产品实现放在可选折叠中。章末保留**面试怎么答、易错点、章节自测**，不是只链接到另一页。源码案例以固定提交为准，MCP/A2A与框架按明确官方版本讲解。

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 23` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–23 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Reader Revision     ✅ 已完成讲解与训练修订
Technical Validation 见限定范围，不替代真实产品集成测试
```

阅读修订：[本轮问题归类、对应章节与实际测试](../roadmap/agent-reader-revision.md)。

下一环：[System Design](../system-design/README.md)。
