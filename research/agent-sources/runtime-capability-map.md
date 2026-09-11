# Agent Harness / Runtime Capability Map

更新日期：2026-09-11

> 这是研究能力层，不等于教材目录。它综合 Tier A（44 道 HUMAN-A Canonical + Verified Follow-up Chains）、Tier B（Claude Code / Codex 固定源码快照）与 Tier C（官方文章 / 协议 / 原始论文），再由 beginner-first 认知依赖映射到教材层。
>
> **Capability 可以比教材章节更细。当前教材已经稳定为 23 个知识小板块，不再按一个 Capability / Canonical 一个文件。**

## 1. Agent Harness 不是一个“框架”

成熟 Agent Runtime 需要解决的不是单一 `while(tool_call)`：

```text
Goal / User Input
      ↓
Instructions + Context + State
      ↓
Model Decision
      ↓
Tool / Delegate / Answer
      ↓
Runtime validates + authorizes + executes
      ↓
Observation / Event / State Transition
      ↓
Loop / Stop / Pause / Resume
```

整个系统同时承担：

```text
Control Plane
Context Plane
Capability Plane
State Plane
Execution Plane
Safety Plane
Coordination Plane
Observability / Evaluation Plane
```

---

# 2. Capability Domains

## A. Agent Boundary & Control Loop

能力：Agent vs Workflow、Harness / Runtime vs Model、Run / Turn / Step / Loop、stop condition、planning / ReAct / routing、loop guard、budget。

证据：HUMAN-A Agent Boundary / Harness / Loop；Claude Code `QueryEngine`；OpenAI Agents SDK built-in loop；ReAct。

## B. Runtime Message / Event Model

能力：user / assistant / tool call / result、turn item / event、call id / correlation、progress / interruption / error、runtime event vs model-visible message。

证据：Codex Event / Turn / rollout trace；Claude Code Message / Progress / ToolResult。

## C. Tool Runtime

能力：schema / validation、registry / router、execution、result normalization、timeout / retry / error、side-effect classification、concurrency safety、cancellation / progress。

证据：Claude Code `Tool.ts`；Codex tools/router/executor；HUMAN-A Tool Calling / Failure。

## D. Context Engineering

能力：context source、assembly order、token budget、large result offloading、cache、compaction trigger / replacement、correctness、stale context。

证据：HUMAN-A Context / Compaction；Codex `compact.rs`；Claude Code compact / tool-result storage；Anthropic Context Engineering。

## E. Memory & Durable State

稳定边界：

```text
Context = 当前 model call 看见什么
Memory = 可被未来再次取回的信息
State = Runtime 当前执行事实
History = 已发生事件 / message
Checkpoint = 可恢复执行点
```

能力：session、memory write/retrieve/consolidate/invalidate、state persistence、tenant isolation、version。

## F. Long-running Reliability

能力：checkpoint、resume、fork、cancellation、retry、idempotency、external side-effect ledger、compensation、task state machine、lease / fencing / worker takeover。

## G. Permission / Approval / Sandbox / Security

三层必须分开：

```text
Policy: 规则上能不能做
Approval: 这一次是否要人确认
Sandbox: 执行环境实际允许碰什么
```

再加 Guardrail、Prompt Injection、Secret Isolation、Egress、Containment。

## H. Capability Discovery / MCP / Skills / Hooks

能力：registry、discovery、progressive loading、MCP Host/Client/Server、Tool/Resource/Prompt、Skill package、Hook lifecycle extension。

边界：

```text
Tool = 可执行能力
MCP = 外部能力 / Context 标准连接协议
Skill = 可发现、可加载的程序性知识包
Hook = Runtime 生命周期扩展点
```

## I. Intent / Model Routing & Provider Resilience

能力：intent recognition、capability route、model/provider selection、adapter、error classification、retry eligibility、fallback、circuit breaker、route evaluation。

## J. Multi-Agent / Delegation / A2A

能力：subagent as tool、manager/specialist、handoff、context isolation、task ownership、shared workspace concurrency、aggregation、A2A、partial failure、recursive delegation、budget。

## K. Trace / Replay / Evaluation

能力：trace/span/event、model-visible evidence、tool call/result、state transition、replay、outcome verification、eval dataset、grader、benchmark、regression、data flywheel。

## L. Coding Agent Runtime

能力：repo discovery、text/symbol/AST/LSP/semantic navigation、workspace state、patch、command、test/lint/typecheck、diff/review、verification、acceptance/delivery。

## M. Production Runtime Architecture

能力：API / streaming、session/run service、scheduler/queue、replaceable harness worker、durable state/event store、sandbox pool、tool gateway、model gateway、artifact store、tenant isolation、quota/backpressure、deployment/scale/cost。

Anthropic Managed Agents 的 brain / hands / session 分离是成熟实现参考，不是所有系统必须复制的唯一拓扑。

---

# 3. 0→1 课程依赖图

```text
Agent vs Workflow
→ Harness / Runtime Boundary
→ Agent Loop / Event / State
→ Tool Contract / Discovery / Execution / Failure
→ Planning / Stop / Budget
→ Context Assembly / Compaction
→ Memory / Session / Durable State
→ Checkpoint / Resume / Side-effect Correctness
→ Permission / Approval / Sandbox / Injection
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Evaluation
→ Coding Agent Verification
→ Production Runtime Architecture
→ Framework Mapping
```

这条顺序故意不按面经热度把 Context Compaction、MCP 或 Multi-Agent 提到前面。

---

# 4. Capability → 23 个教材知识块

研究层保持以上 Capability Domain；教材层最终映射为：

```text
01 Agent Harness 在 AI 应用中的职责
02 Agent vs Workflow + Harness / Runtime / Orchestrator Boundary
03 Agent Loop + Run / Turn / Step + Event / State
04 Tool Contract + Schema + Validation
05 Tool Registry + Router + Progressive Discovery
06 Tool Execution + Result + Failure
07 Tool Side Effect + Concurrency + Cancellation + Progress
08 Planning / ReAct + Goal + Stop + Budget
09 Context Assembly + Budget + Cache + Tool-result Offloading
10 Context Compaction + Correctness + Stale Context
11 Memory Architecture + Lifecycle + Correctness
12 Session / State / History / Persistence + Tenant Isolation
13 Checkpoint / Resume / Fork / Replay + Long-running Reliability
14 Permission + Approval / HITL + Sandbox
15 Guardrails + Prompt Injection + Secrets + Containment
16 MCP + Skills + Hooks + Capability Extension
17 Intent / Model Routing + Provider Adapter + Runtime Resilience
18 Multi-Agent + Subagent + Handoff + A2A + Workspace Concurrency
19 Trace + Replay + Observability
20 Agent Evaluation + Benchmark + Data Flywheel
21 Coding Agent：Repo → Patch → Test → Verify
22 Production Agent Runtime Architecture
23 Framework Mapping + Build-vs-Buy
```

这里不是把 Capability 删除，而是把共享同一认知闭环的 Capability 放回同一个教材文件。

---

# 5. 为什么 23 比旧 42 / 47 更合理

旧目录接近：

```text
一个 interview capability
→ 一个 runtime primitive
→ 一个 Markdown
```

导致 Context、Tool、State、Evaluation 等连续机制被切成很多短文件。

现在采用：

```text
一个 Markdown
= 一个大问题
= 有完整前置与输出心智模型
= 有独立 Failure / Trade-off
= 能形成 Why → Mechanism → Failure → Validation 闭环
```

例如 Tool 研究层仍然能单独讨论 Schema、Registry、Failure、Cancellation，但教材层组织为 04–07 四个 Tool Runtime 子系统，而不是十几个碎章。

---

# 6. 课程验收标准

23-block 深度验收已经完成。正文不是“文件存在”即通过，而必须能支撑：

```text
为什么存在
→ Runtime Mental Model
→ 正常执行路径
→ State / Protocol / Data Structure
→ Failure Timeline
→ Cancellation / Recovery / Idempotency
→ Security / Permission Boundary
→ Observability / Evaluation
→ Claude Code / Codex 实现证据
→ HUMAN-A 追问
→ 面试回答 / 自测
```

学完至少应能从零设计并解释：

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
Trace / Eval
Production Deployment
```

并能说明为什么某个 Runtime 决策存在、失败时如何恢复、怎样验证它真的工作。
