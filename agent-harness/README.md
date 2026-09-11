# Agent Harness / Runtime｜AI 应用开发秋招系统手册

> **当前状态：✅ 第一版 0→1 系统教材已完成。**
>
> 这一模块不是 LangChain / LangGraph API 教程，而是从 0 建立成熟 Agent 产品真正需要的 Runtime 心智模型：**Agent 为什么需要自循环 → Harness 为什么要独立于 Model → 一次 Run / Turn / Step 怎样推进 → Tool 怎样被描述、校验、授权和执行 → Context 怎样组装与压缩 → State 怎样持久化并恢复 → Permission / Sandbox 怎样控制副作用 → MCP / Skill / Multi-Agent 怎样扩展能力 → Trace / Eval 怎样证明任务真的完成 → Production 怎样扩展。**

## 1. 课程证据层

本模块采用四层证据：

```text
Tier A  44 道 Agent HUMAN-A Canonical + Verified Follow-up Chains
Tier B  Claude Code + OpenAI Codex 固定源码快照
Tier C  Anthropic / OpenAI 官方文章、MCP / A2A 规范、ReAct / SWE-bench
Tier D  初学者 0→1 的课程抽象
```

入口：[`../research/agent-sources/README.md`](../research/agent-sources/README.md)

源码固定快照：

```text
Claude Code commit = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

**只有 Tier A 决定真人面经频率。源码和外部权威资料只补完整知识边界。**

## 2. 最重要的课程原则

> **知识依赖决定顺序，面经热度决定复习权重。**

虽然 Context Compaction、Memory、Agent Loop、Tool Calling、Multi-Agent 在真人面经里非常热，但不能第一章就背“Context 压缩策略”。必须先理解：

```text
Agent 与 Workflow 的边界
→ Harness 是什么
→ Loop 怎样推进
→ Run / Turn / Step 是什么
→ Runtime Event 怎样记录
→ Tool Runtime 怎样工作
→ 才能理解 Context 为什么增长和怎样压缩
```

## 3. 这套课里的 Harness

Harness / Runtime 是模型之外、围绕模型建立的执行系统。一个实用抽象：

```text
                  User / Goal
                      │
                      ▼
              Agent Harness / Runtime
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     Context        State         Policy
        │             │             │
        └──────┬──────┴──────┬──────┘
               ▼             ▼
             Model         Tools
               │             │
               └───── Loop ──┘
                      │
                      ▼
          Event / Trace / Verification
```

Model 提供推理与决策能力；Harness 决定它看到什么、能做什么、如何循环、怎样失败、怎样恢复、怎样被审计。

## 4. 与其它模块的边界

| 问题 | Primary |
|---|---|
| Token / Context Window / KV Cache | LLM Foundation |
| RAG Retrieval / Rerank / Eval | RAG |
| Redis 作为状态存储的 TTL / HA | Redis |
| HTTP / MQ / Backpressure 通用原理 | AI Backend Engineering |
| Agent Context Assembly / Compaction | Agent Harness |
| Tool Calling Runtime / Permission / Sandbox | Agent Harness |
| Checkpoint / Resume / Side-effect correctness | Agent Harness |
| Multi-Agent / A2A / Task Ownership | Agent Harness |
| 整个平台跨组件架构 | System Design |

## 5. 十二条主线

```text
A  Agent Boundary / Harness / Loop
B  Run / Turn / Step / Event Model
C  Tool Contract / Router / Executor / Failure
D  Planning / Stop / Budget
E  Context Assembly / Budget / Compaction / Correctness
F  Memory / Session / State / Checkpoint / Resume
G  Cancellation / Idempotency / Compensation
H  Permission / Approval / Sandbox / Injection / Containment
I  Discovery / MCP / Skills / Hooks / Routing
J  Multi-Agent / Handoff / A2A / Workspace
K  Trace / Replay / Evaluation / Coding Verification
L  Production Architecture / Framework Mapping
```

## 6. 完整 47 章

### Part A｜从 LLM Call 到 Agent Runtime

1. [Agent Harness 在 AI 应用中的职责](docs/01-AgentHarness在AI应用中的职责.md)
2. [Agent vs Workflow：什么时候真的需要 Agent](docs/02-AgentVsWorkflow.md)
3. [Harness / Runtime 与 Model 的边界](docs/03-HarnessRuntimeBoundary.md)
4. [Minimal Agent Loop](docs/04-MinimalAgentLoop.md)
5. [Run / Turn / Step 与状态机](docs/05-RunTurnStep.md)
6. [Runtime Message / Event Model](docs/06-RuntimeMessageEvent.md)

### Part B｜Tool Runtime

7. [Tool Contract：不只是函数调用](docs/07-ToolContract.md)
8. [Tool Schema、Validation 与 Structured Result](docs/08-ToolSchemaValidation.md)
9. [Tool Registry、Router 与 Capability Catalog](docs/09-ToolRegistryRouter.md)
10. [Tool Executor 与 Result 回填](docs/10-ToolExecutionResult.md)
11. [Tool Failure、Timeout 与 Retry](docs/11-ToolFailureTimeoutRetry.md)
12. [Side Effect、Concurrency Safety 与 Destructive Tool](docs/12-ToolSideEffectConcurrency.md)
13. [Tool Cancellation、Progress 与 Streaming](docs/13-ToolCancellationProgress.md)

### Part C｜Planning 与控制循环

14. [Planning、ReAct 与 Execute-Observe](docs/14-PlanningReAct.md)
15. [Stop Condition、Loop Guard 与 Budget](docs/15-StopLoopGuardBudget.md)

### Part D｜Context Engineering

16. [Context Assembly](docs/16-ContextAssembly.md)
17. [Context Budget 与 Token Economics](docs/17-ContextBudget.md)
18. [Large Tool Result、Offloading 与 Reference](docs/18-ToolResultOffloading.md)
19. [Context Compaction](docs/19-ContextCompaction.md)
20. [Compaction Correctness 与 Stale Context](docs/20-CompactionCorrectness.md)

### Part E｜Memory、State 与长任务

21. [Memory Architecture 与生命周期](docs/21-MemoryArchitecture.md)
22. [Session、State、History 的区别](docs/22-SessionStateHistory.md)
23. [State Persistence 与 Event Log](docs/23-StatePersistence.md)
24. [Checkpoint 与 Resume](docs/24-CheckpointResume.md)
25. [Fork、Branch 与 Replay](docs/25-ForkBranchReplay.md)
26. [Runtime Cancellation](docs/26-RuntimeCancellation.md)
27. [Idempotency、External Side Effect 与 Compensation](docs/27-IdempotencyCompensation.md)

### Part F｜安全执行边界

28. [Human-in-the-loop、Permission 与 Approval](docs/28-PermissionApproval.md)
29. [Sandbox 与 Execution Environment](docs/29-SandboxEnvironment.md)
30. [Guardrails 与 Runtime Validation](docs/30-GuardrailsValidation.md)
31. [Prompt Injection 与 Untrusted Context](docs/31-PromptInjection.md)
32. [Secrets、Data Exfiltration 与 Containment](docs/32-SecretsContainment.md)

### Part G｜能力扩展

33. [Tool Discovery 与 Progressive Loading](docs/33-ToolDiscovery.md)
34. [MCP：Host / Client / Server / Tool / Resource / Prompt](docs/34-MCP.md)
35. [Skills、Commands 与 Reusable Capability](docs/35-SkillsCapability.md)
36. [Hooks、Plugins 与 Extensibility](docs/36-HooksPlugins.md)
37. [Intent Recognition 与 Capability Routing](docs/37-IntentRouting.md)
38. [Model Provider、Model Routing 与 Fallback](docs/38-ModelRouting.md)

### Part H｜Multi-Agent

39. [Multi-Agent：什么时候值得拆 Agent](docs/39-MultiAgentPatterns.md)
40. [Subagent、Handoff、Context Isolation 与 Task Ownership](docs/40-SubagentHandoff.md)
41. [A2A 与 Agent-to-Agent Protocol Boundary](docs/41-A2A.md)
42. [Shared Workspace 与并发冲突](docs/42-WorkspaceConcurrency.md)

### Part I｜可观测、评测与 Coding Agent

43. [Trace、Replay 与 Observability](docs/43-TraceReplayObservability.md)
44. [Agent Evaluation、Benchmark 与 Outcome Verification](docs/44-AgentEvaluation.md)
45. [Coding Agent：Repo Understanding → Patch → Test → Verify](docs/45-CodingAgentWorkflow.md)

### Part J｜Production 与框架映射

46. [Production Agent Runtime Architecture](docs/46-ProductionArchitecture.md)
47. [Framework Mapping 与 Build-vs-Buy](docs/47-FrameworkMapping.md)

## 7. Verified 真人追问主链

当前人工核验的高置信链包括：

```text
为什么 Agent
→ Harness
→ Loop
→ Tool / Skill / MCP
→ Context / Memory
→ Failure / Evaluation
```

以及：

```text
Context Assembly
→ Compaction
→ Correctness
→ Memory Pollution
→ Resume
```

```text
Tool Lifecycle
→ Discovery
→ Failure
→ Permission / Sandbox
```

这会影响章节内部追问顺序，但不替代上面的 0→1 主干。

## 8. 配套

完成正文后使用：

- [`review/README.md`](review/README.md)
- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

最终验收不是“会用框架”，而是：

> **能自己画出 Runtime、定义状态机、设计 Tool Contract、控制 Context、处理副作用、暂停恢复、做安全边界、追踪执行并用 Outcome 验证任务是否真的完成。**
