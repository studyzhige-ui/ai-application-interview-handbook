# Agent Harness / Runtime｜AI 应用开发秋招系统手册

> **当前状态：🚧 23 个知识小板块重组 + 深度重写中。**
>
> 本模块不再按 Canonical Question / Runtime Primitive 一题一文件。研究层仍保留 44 道 Agent Canonical 和更细 Capability Map；教材层改为 **23 个能够独立形成认知闭环的知识小板块**。

## 1. 为什么从旧 47 章重组为 23 章

旧 47 章的问题不是知识点错，而是粒度错：

```text
Canonical / Capability Primitive
        ↓  旧版几乎直接映射
Markdown File
```

这会导致：

- 一个概念刚建立背景就切文件；
- 相邻文件反复解释同一 Runtime；
- 参数 / failure / variant 被误当成独立知识板块；
- 学完容易得到“47 个名词”，而不是 Agent Runtime 心智模型。

现在统一为：

```text
Canonical Question        = 可独立追问的面试能力
Capability Primitive      = Runtime 最小机制
教材文件                  = 一个完整知识小板块
文件内 Section            = 参数 / 变体 / Failure / 追问
```

仓库级粒度规则见：[`../roadmap/curriculum-granularity-audit.md`](../roadmap/curriculum-granularity-audit.md)。

---

## 2. 课程证据层

```text
Tier A  44 道 Agent HUMAN-A Canonical + Verified Follow-up Chains
Tier B  Claude Code + OpenAI Codex 固定源码快照
Tier C  Anthropic / OpenAI 官方工程资料 + MCP / A2A 规范 + 原始论文
Tier D  Beginner-first Runtime Curriculum
```

研究入口：[`../research/agent-sources/README.md`](../research/agent-sources/README.md)

固定源码快照：

```text
Claude Code commit = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

**只有 Tier A 决定市场频率。Tier B/C 负责课程完整性与实现证据，不改变 Source Count。**

---

## 3. 课程顺序原则

> **知识依赖决定顺序，面经热度决定复习权重。**

正确顺序：

```text
Agent Boundary
→ Loop / Runtime State
→ Tool Runtime
→ Planning / Control
→ Context
→ Memory / Durable State
→ Long-running Reliability
→ Security
→ Capability Extension
→ Routing / Multi-Agent
→ Trace / Evaluation
→ Coding Agent
→ Production / Framework Mapping
```

不会因为 Context Compaction 有 41 个真人来源，就在初学者理解 Context Assembly 之前先讲 Summary。

---

# 4. 正式 23 个知识小板块

## Part A｜Agent 与 Runtime 基础

1. [Agent Harness 在 AI 应用中的职责](docs/01-AgentHarness在AI应用中的职责.md)
2. [Agent vs Workflow，以及 Harness / Runtime / Orchestrator 的边界](docs/02-AgentWorkflowHarnessBoundary.md)
3. [Agent Loop、Run / Turn / Step 与 Runtime Event Model](docs/03-AgentLoopRuntimeState.md)

## Part B｜Tool Runtime

4. [Tool Contract、Schema 与 Validation](docs/04-ToolContractSchemaValidation.md)
5. [Tool Registry、Router 与 Progressive Discovery](docs/05-ToolRegistryRouterDiscovery.md)
6. [Tool Execution、Result 与 Failure Semantics](docs/06-ToolExecutionFailure.md)
7. [Tool Side Effect、Concurrency、Cancellation 与 Progress](docs/07-ToolSideEffectCancellation.md)

## Part C｜Planning 与控制循环

8. [Planning / ReAct、Goal Control、Stop Condition 与 Budget](docs/08-PlanningGoalStopBudget.md)

## Part D｜Context Engineering

9. [Context Assembly、Budget、Cache 与 Tool Result Offloading](docs/09-ContextAssemblyBudget.md)
10. [Context Compaction、Correctness 与 Stale Context](docs/10-ContextCompactionCorrectness.md)

## Part E｜Memory、State 与长任务

11. [Memory Architecture、Lifecycle 与 Correctness](docs/11-MemoryArchitectureLifecycle.md)
12. [Session / State / History / Persistence 与 Tenant Isolation](docs/12-SessionStatePersistence.md)
13. [Checkpoint / Resume / Fork / Replay 与 Long-running Reliability](docs/13-CheckpointResumeReliability.md)

## Part F｜安全执行边界

14. [Permission、Approval、HITL 与 Sandbox](docs/14-PermissionApprovalSandbox.md)
15. [Guardrails、Prompt Injection、Secrets 与 Containment](docs/15-GuardrailsInjectionContainment.md)

## Part G｜能力扩展与路由

16. [MCP、Skills、Hooks 与 Capability Extension](docs/16-MCPSkillsHooks.md)
17. [Intent / Model Routing、Provider Adapter 与 Runtime Resilience](docs/17-RoutingProviderResilience.md)

## Part H｜Multi-Agent Coordination

18. [Multi-Agent、Subagent、Handoff、A2A 与 Workspace Concurrency](docs/18-MultiAgentA2AWorkspace.md)

## Part I｜可观测、评测与 Coding Agent

19. [Trace、Replay 与 Observability](docs/19-TraceReplayObservability.md)
20. [Agent Evaluation、Benchmark 与 Data Flywheel](docs/20-AgentEvaluationBenchmark.md)
21. [Coding Agent：Repo Understanding → Patch → Test → Verify](docs/21-CodingAgentWorkflow.md)

## Part J｜Production 与框架映射

22. [Production Agent Runtime Architecture](docs/22-ProductionAgentRuntime.md)
23. [Framework Mapping 与 Build-vs-Buy](docs/23-FrameworkMappingBuildVsBuy.md)

---

## 5. 旧 47 章怎样迁移

```text
旧 01                         → 新 01
旧 02 + 03                    → 新 02
旧 04 + 05 + 06               → 新 03
旧 07 + 08                    → 新 04
旧 09 + 33                    → 新 05
旧 10 + 11                    → 新 06
旧 12 + 13                    → 新 07
旧 14 + 15 + Goal Drift/Steering → 新 08
旧 16 + 17 + 18 + Context Cache → 新 09
旧 19 + 20                    → 新 10
旧 21 + Memory Lifecycle/Correctness → 新 11
旧 22 + 23 + Tenant Isolation → 新 12
旧 24 + 25 + 26 + 27          → 新 13
旧 28 + 29                    → 新 14
旧 30 + 31 + 32               → 新 15
旧 34 + 35 + 36 + Progressive Loading → 新 16
旧 37 + 38 + Runtime Resilience → 新 17
旧 39 + 40 + 41 + 42          → 新 18
旧 43                         → 新 19
旧 44 + Benchmark + Flywheel  → 新 20
旧 45 + Repo Understanding + AI-assisted Workflow → 新 21
旧 46                         → 新 22
旧 47                         → 新 23
```

这个 Merge **不改变**任何 Canonical、Source Count、Primary Ownership 或 Follow-up Chain。

---

## 6. 三个特别重要的边界

### Prompt / Context / Harness

```text
Prompt Engineering
= 单次模型行为约束

Context Engineering
= 一次 inference 看见什么

Harness Engineering
= 跨多轮、多 Tool、多 State 的执行系统
```

### Tool / MCP / Skill / Hook

```text
Tool   = 一次可执行能力
MCP    = 外部能力 / Context 的标准连接协议
Skill  = 可发现、可加载的程序性知识与资源包
Hook   = Runtime 生命周期扩展点
```

### Context / Memory / State / History

```text
Context    = 当前 Model Call 的输入视图
Memory     = 可被未来再次取回的信息
State      = Runtime 当前执行事实
History    = 已发生事件 / Message 的记录
Checkpoint = 可恢复执行点
```

---

## 7. 每个文件的正式验收标准

一个知识小板块至少应包含：

```text
先讲人话
→ 准确定义
→ 为什么需要
→ Runtime 图 / 状态机 / 数据流
→ 最小实现 / 伪代码
→ Failure Semantics
→ Trade-off
→ HUMAN-A 真实追问
→ Claude Code / Codex 实现证据
→ 官方 / 规范 / 原始论文证据
→ AI 应用场景
→ 30 秒回答
→ 2–3 分钟回答
→ 深挖追问
→ 折叠自测
```

完成标准不是“文件存在”，而是能独立支撑学习和面试追问。

---

## 8. 当前迁移状态

当前旧 47 章文件仍在迁移中，因此以本 README 的 **23 章目录**为目标口径。

已经完成过深写的旧 01–18 内容不会丢失，会在 Merge 时去重并迁入对应新章；旧短稿 19–47 不再逐文件扩写。

迁移 checkpoint 见：[` .rewrite-in-progress.md`](.rewrite-in-progress.md)。

---

## 9. 最终验收

学完 Agent Harness，不是会背：

> Agent = LLM + Tools。

而是能够从零设计并解释：

```text
Run State Machine
Tool Contract / Failure
Context Assembly / Compaction
Memory / Durable State
Checkpoint / Resume
Side-effect Correctness
Permission / Sandbox
Capability Discovery
Multi-Agent Ownership
Trace / Evaluation
Production Runtime
```

并能说明：**为什么这个 Runtime 决策存在、失败时怎样恢复、怎样验证它真的工作。**