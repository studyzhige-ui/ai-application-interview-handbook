# Agent Harness / Runtime｜AI 应用开发秋招系统手册

> **当前状态：✅ 第一版完整系统教材已完成。**
>
> 旧 47 章已经按教材粒度重组为 **23 个知识小板块**，并完成正文深度验收。研究层仍保留 44 道 Agent Canonical 和更细 Runtime Capability Map；教材层按完整认知闭环组织，不再一题一文件。

---

## 1. 这一模块到底学什么

Agent Harness / Runtime 不是某个 Framework，也不是一段 System Prompt。

它解决的是：

```text
用户给出 Goal
→ Runtime 组装 Context / State
→ Model 决定 Answer / Tool / Delegate
→ Runtime 校验权限并执行
→ Tool / Environment 返回 Observation
→ State / Event 更新
→ Loop / Stop / Pause / Resume
```

成熟系统还必须处理：

```text
Tool Contract / Failure
Context Budget / Compaction
Memory / Session / Checkpoint
Side-effect Correctness
Permission / Sandbox / Prompt Injection
MCP / Skills / Hooks
Routing / Provider Failure
Multi-Agent / A2A / Workspace Conflict
Trace / Evaluation
Coding Agent Verification
Production Deployment
```

所以这套课程的目标不是背：

> `Agent = LLM + Tools`

而是能从零解释一个长期运行、可恢复、可审计、可控权限的 Agent Runtime 为什么这样设计。

---

## 2. 为什么从旧 47 章重组为 23 章

旧版的问题不是知识错误，而是教材粒度接近 Capability Primitive：

```text
Canonical Question
≈ Runtime Primitive
≈ Markdown File
```

容易导致：

- 同一 Runtime 背景在多个文件重复；
- 参数 / Failure / 变体被误当独立知识板块；
- 初学者频繁切文件，难形成大块心智模型；
- 学完记住几十个词，却不会设计完整系统。

现在正式区分：

```text
Canonical Question   = 可独立追问能力
Capability Primitive = 更细的工程机制
教材 Markdown        = 一个完整知识小板块
Section              = 参数 / 变体 / Failure / 深挖
```

仓库级规则：[`../roadmap/curriculum-granularity-audit.md`](../roadmap/curriculum-granularity-audit.md)。

---

## 3. 课程证据层

```text
Tier A  44 道 Agent HUMAN-A Canonical + Verified Follow-up Chains
Tier B  Claude Code + OpenAI Codex 固定源码快照
Tier C  Anthropic / OpenAI 官方工程资料 + MCP / A2A 规范 + 原始论文
Tier D  Beginner-first Runtime Curriculum
```

只有 Tier A 决定真实市场频率；Tier B/C 用于补齐成熟 Runtime 实现和稳定工程原则，**不改变 Source Count**。

研究入口：[`../research/agent-sources/README.md`](../research/agent-sources/README.md)

固定源码快照：

```text
Claude Code = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

重点证据：

- Claude Code：`QueryEngine`、`Tool.ts`、`Task.ts`、Context / Compact / Memory / Permission / ToolResultStorage；
- Codex：Tool Router / Executor / Output、`compact.rs`、Sandbox Policy、Hooks、Rollout Trace、Thread Instructions；
- Anthropic：Building Effective Agents、Context Engineering、Long-running Harness、Tool Design、Agent Skills、Sandbox / Containment、Multi-Agent、Agent Evals；
- OpenAI：Practical Guide、Agents SDK HITL / Guardrails / Tracing；
- MCP / A2A 官方规范；
- ReAct / SWE-bench 原始论文。

---

## 4. 课程顺序

> **知识依赖决定顺序，真人面经热度决定复习权重。**

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

例如 Context Compaction 虽然是最强真人面经信号之一，也必须先学 Context Assembly；MCP 再热门，也要先理解 Tool Runtime。

---

# 5. 正式 23 个知识小板块

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

## 6. 三个必须长期分清的边界

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
Tool  = 一次可执行能力
MCP   = 外部能力 / Context 的标准连接协议
Skill = 可发现、按需加载的程序性知识与资源包
Hook  = Runtime 生命周期扩展点
```

### Context / Memory / State / History

```text
Context    = 当前 Model Call 的输入视图
Memory     = 未来可再次取回的信息
State      = Runtime 当前执行事实
History    = 已发生 Event / Message
Checkpoint = 可恢复执行点
```

---

## 7. 正文深度验收标准

23 个正文现在均按同一标准验收：

```text
为什么存在
→ 准确定义 / Runtime Mental Model
→ 正常执行路径
→ State / Protocol / Data Structure
→ Failure Timeline
→ Recovery / Idempotency / Cancellation
→ Security / Permission Boundary
→ Observability / Evaluation
→ HUMAN-A 对应
→ Claude Code / Codex / 官方资料证据（适用时）
→ 30 秒 / 深挖回答
→ 易错点
→ 折叠自测
```

其中旧短稿合并形成的 08–23 已全部重写到完整教学深度；01–07 的既有深写稿也重新抽查通过。

当前 `docs/` 已实际核验为 **01–23 连续，无旧 47 章碎片文件残留**。

---

## 8. Review 与 Interview 使用不同粒度

第二遍：[`review/README.md`](review/README.md)

第三遍：

- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

这里不会为了 23 个教材文件，把 44 道 Canonical 或更细的 Interview Question 强行合并。

```text
23 curriculum blocks
≠ 44 Agent Canonical
≠ 更细的面试追问
```

---

## 9. 学完后的最终能力

你应该能从零设计并解释：

```text
Run State Machine
Tool Contract / Discovery / Failure
Context Assembly / Compaction
Memory / Durable State
Checkpoint / Resume
Side-effect Correctness
Permission / Approval / Sandbox
Prompt Injection / Containment
MCP / Skill / Hook
Routing / Provider Failure
Multi-Agent Ownership / A2A
Trace / Evaluation
Coding Agent Verification
Production Runtime
Framework Build-vs-Buy
```

并能回答：

> **为什么这个 Runtime 决策存在、正常路径怎样工作、失败窗口在哪里、怎样恢复、怎样验证它真的有效。**
