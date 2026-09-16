# Agent Harness / Runtime｜Agent 执行系统

[← RAG](../rag/README.md) · [↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [System Design →](../system-design/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：23 个连续知识小板块** · **HUMAN-A Canonical：44** · **独立来源覆盖：166**  
> **质量：Granularity / Coverage / Content Depth 已验收**

从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。

> **先建立整体框架：** [Agent 系统架构总纲](architecture/README.md) → [执行与状态](architecture/lifecycle-and-state.md) → [概念归位表](architecture/concept-atlas.md)。这是跨模块前导视图；下方 23 章继续负责具体机制。

---

## 1. 这个模块解决什么

从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。

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

当前模块角色：**Agent Runtime / 从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。**

---

## 3. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法、追问深度，不能反过来打乱初学者从 0→1 的主干。**

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

1. [Agent Harness 在 AI 应用中的职责](docs/01-AgentHarness在AI应用中的职责.md)
2. [Agent vs Workflow，以及 Harness / Runtime / Orchestrator 的边界](docs/02-AgentWorkflowHarnessBoundary.md)
3. [Agent Loop、Run / Turn / Step 与 Runtime Event Model](docs/03-AgentLoopRuntimeState.md)

### Part B｜Tool Runtime

4. [Tool Contract、Schema 与 Validation](docs/04-ToolContractSchemaValidation.md)
5. [Tool Registry、Router 与 Progressive Discovery](docs/05-ToolRegistryRouterDiscovery.md)
6. [Tool Execution、Result 与 Failure Semantics](docs/06-ToolExecutionFailure.md)
7. [Tool Side Effect、Concurrency、Cancellation 与 Progress](docs/07-ToolSideEffectCancellation.md)

### Part C｜Planning 与 Context

8. [Planning / ReAct、Goal Control、Stop Condition 与 Budget](docs/08-PlanningGoalStopBudget.md)
9. [Context Assembly、Budget、Cache 与 Tool Result Offloading](docs/09-ContextAssemblyBudget.md)
10. [Context Compaction、Correctness 与 Stale Context](docs/10-ContextCompactionCorrectness.md)

### Part D｜Memory、State 与 Long-running Reliability

11. [Memory Architecture、Lifecycle 与 Correctness](docs/11-MemoryArchitectureLifecycle.md)
12. [Session / State / History / Persistence 与 Tenant Isolation](docs/12-SessionStatePersistence.md)
13. [Checkpoint / Resume / Fork / Replay 与 Long-running Reliability](docs/13-CheckpointResumeReliability.md)

### Part E｜Security、Capability 与 Multi-Agent

14. [Permission、Approval、HITL 与 Sandbox](docs/14-PermissionApprovalSandbox.md)
15. [Guardrails、Prompt Injection、Secrets 与 Containment](docs/15-GuardrailsInjectionContainment.md)
16. [MCP、Skills、Hooks 与 Capability Extension](docs/16-MCPSkillsHooks.md)
17. [Intent / Model Routing、Provider Adapter 与 Runtime Resilience](docs/17-RoutingProviderResilience.md)
18. [Multi-Agent、Subagent、Handoff、A2A 与 Workspace Concurrency](docs/18-MultiAgentA2AWorkspace.md)

### Part F｜Observability、Evaluation 与 Production

19. [Trace、Replay 与 Observability](docs/19-TraceReplayObservability.md)
20. [Agent Evaluation、Benchmark 与 Data Flywheel](docs/20-AgentEvaluationBenchmark.md)
21. [Coding Agent：Repo Understanding → Patch → Test → Verify](docs/21-CodingAgentWorkflow.md)
22. [Production Agent Runtime Architecture](docs/22-ProductionAgentRuntime.md)
23. [Framework Mapping 与 Build-vs-Buy](docs/23-FrameworkMappingBuildVsBuy.md)

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
Content Depth       ✅
```

下一环：[System Design](../system-design/README.md)。
