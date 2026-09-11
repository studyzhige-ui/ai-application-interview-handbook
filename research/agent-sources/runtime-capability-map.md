# Agent Harness / Runtime Capability Map

更新日期：2026-09-11

> 这是最终课程目录之前的抽象层。它综合 Tier A（44 道 HUMAN-A Canonical + Verified Follow-up Chains）、Tier B（Claude Code / Codex 固定源码快照）与 Tier C（官方文章 / 协议 / 原始论文）。课程顺序仍由初学者 0→1 依赖决定。

## 1. 总结：Agent Harness 不是一个“框架”

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

核心问题：为什么这里是 Agent，而不是普通 LLM Call / deterministic workflow？

能力：

- Agent vs Workflow；
- Harness / Runtime vs Model；
- Turn / Step / Loop；
- stop condition；
- planning / ReAct / routing；
- loop guard / max turns / budget。

证据：

- HUMAN-A：Agent Boundary、Harness Boundary、Agent Loop、Agent Paradigm；
- Claude Code：`QueryEngine` 持有 turn lifecycle、max turns、budget、tools、agents；
- OpenAI Agents SDK：公开 built-in loop；
- ReAct：reason/action/observation 交替。

## B. Runtime Message / Event Model

核心问题：一次执行发生的事情怎样成为可持久化、可追踪、可恢复的数据？

能力：

- user / assistant / tool call / tool result；
- turn item / event；
- call id / correlation；
- progress / interruption / error；
- runtime event vs model-visible message。

证据：Codex `EventMsg` / `TurnItem` / rollout trace；Claude Code Message / ProgressMessage / SystemMessage / ToolResult。

## C. Tool Runtime

能力：

- schema / validation；
- registry / router；
- execution；
- result normalization；
- timeout / retry / error；
- side effect classification；
- concurrency safety；
- cancellation / interrupt behavior。

证据：Claude Code `Tool.ts`；Codex `codex-rs/tools/*` / router；HUMAN-A Tool Calling / Failure 高热度。

## D. Context Engineering

能力：

- context sources；
- assembly order；
- token budget；
- large tool-result management；
- compaction trigger / strategy；
- compaction correctness；
- context cache / stable prefix；
- stale context / pollution。

证据：HUMAN-A 全库最高信号之一；Codex `compact.rs`；Claude Code compact / nested memory / tool-result budget；Anthropic Context Engineering。

## E. Memory & Durable State

必须先区分：

```text
Context = 当前 model call 看见什么
Memory  = 可被未来再次取回的信息
State   = Runtime 当前执行事实
History = 过去事件 / message 记录
Checkpoint = 可恢复执行点
```

能力：session、memory lifecycle、state persistence、checkpoint、resume、fork、version。

证据：Claude Code QueryEngine/session/memdir；Codex Session/Turn/compacted persisted history；OpenAI Sessions/HITL RunState。

## F. Long-running Reliability

能力：

- cancellation；
- pause / resume；
- retry；
- idempotency；
- external side-effect ledger；
- compensation；
- progress artifact；
- task state machine；
- lease / worker failure / backpressure boundary。

证据：HUMAN-A Checkpoint/Resume/Failure；Claude Code Task state + AbortController；OpenAI HITL RunState；Anthropic long-running harness。

## G. Permission, Approval & Sandbox

必须拆成三层：

```text
Policy: 规则上可不可以？
Approval: 这一次要不要人确认？
Sandbox: 执行环境实际上能碰到什么？
```

再加：untrusted context / prompt injection、secret/data exfiltration、blast radius。

证据：Claude Code permission context；Codex SandboxPolicy；Anthropic sandbox/containment；OpenAI HITL/Guardrails。

## H. Capability Discovery / MCP / Skills

能力：

- tool registry；
- metadata / schema；
- discovery；
- progressive loading；
- MCP Host / Client / Server；
- Resource / Prompt / Tool；
- Skill procedural package；
- hook / plugin boundary。

关键边界：

```text
Tool = 可执行能力
MCP = 能力 / Context 的标准连接协议
Skill = 可发现、可加载的程序性知识包
Hook = Runtime 生命周期扩展点
```

证据：Claude Code Tool searchHint / skill triggers / MCP；Codex MCP+Hooks；MCP spec；Anthropic Skills / Advanced Tool Use。

## I. Intent / Model Routing

能力：

- intent recognition；
- capability router；
- model selection / provider adapter；
- fallback；
- cost / latency / quality route；
- route evaluation。

注意：这不是把所有 request 都交给一个 LLM router。

## J. Multi-Agent / Delegation / A2A

能力：

- subagent as tool；
- manager / specialist；
- handoff；
- context isolation；
- shared resource conflicts；
- task ownership；
- aggregation；
- A2A protocol；
- failure / recursion / budget。

证据：HUMAN-A Multi-Agent；Claude Code Task/Agent；OpenAI agents-as-tools/handoffs；Anthropic multi-agent research；A2A spec。

## K. Coding Agent Runtime

能力：

- repo discovery；
- file/search/code navigation；
- workspace state；
- patch / command execution；
- test / lint / typecheck；
- diff / review；
- verification；
- acceptance / delivery。

证据：HUMAN-A Repository Understanding / Code Verification / AI-assisted Development；SWE-bench；Claude Code / Codex 产品源码。

## L. Trace / Replay / Evaluation

能力：

- trace / span / event；
- model input / output evidence；
- tool call / result；
- state transition；
- replay；
- task outcome verification；
- eval dataset；
- grader / environment outcome；
- cost / latency / success metrics；
- regression。

证据：Codex rollout trace；OpenAI Agents SDK tracing；Anthropic agent evals；HUMAN-A Evaluation / Benchmark。

## M. Production Runtime Architecture

能力：

- API / streaming；
- session service；
- stateless harness worker；
- durable event/state store；
- execution sandbox pool；
- tool gateway；
- tenant isolation；
- queue / quota / backpressure；
- model provider routing；
- secrets；
- deployment / scaling / cost。

Anthropic Managed Agents 的 brain / hands / session 分离提供了一个很好的成熟架构参考，但课程会把它抽象成通用组件，而不是复制产品拓扑。

---

# 3. 从 0→1 的课程依赖图

```text
Agent vs Workflow
        ↓
Harness / Runtime Boundary
        ↓
Minimal Agent Loop
        ↓
Runtime Message / Event
        ↓
Tool Contract / Execution / Failure
        ↓
Planning / Routing / Stop
        ↓
Context Assembly / Budget
        ↓
Compaction / Correctness
        ↓
Memory / State / Session
        ↓
Checkpoint / Resume / Cancellation
        ↓
Idempotency / Side Effects / Compensation
        ↓
Permission / Approval / Sandbox / Injection
        ↓
Tool Discovery / MCP / Skills / Hooks
        ↓
Multi-Agent / A2A / Shared Resource
        ↓
Trace / Replay / Evaluation
        ↓
Coding Agent Verification
        ↓
Production Architecture / Scale / Cost
        ↓
Framework Mapping
```

这条顺序故意没有按面经热度把 Context Compaction 放到最前面。

---

# 4. 课程决定：建议 42 章

最终正式教材建议拆为 42 章，避免把多个独立 failure model 塞进一章：

```text
01–05  Agent / Harness / Loop / Event 基础
06–11  Tool Runtime
12–17  Planning / Context / Compaction
18–23  Memory / State / Checkpoint / Reliability
24–28  Permission / Sandbox / Security
29–33  Discovery / MCP / Skill / Hook / Routing
34–37  Multi-Agent / A2A / Workspace
38–40  Trace / Evaluation / Coding Verification
41     Production Runtime Architecture
42     Framework Mapping & Build-vs-Buy
```

详细章节名写入 `agent-harness/README.md`。

---

# 5. 课程验收标准

学完不能只回答“Agent = LLM + Tools”。至少应该能从零设计：

```text
Run State Machine
Tool Contract
Context Assembly
Compaction Transaction
Permission + Sandbox
Pause / Resume
Side-effect Correctness
Capability Discovery
Multi-Agent Ownership
Trace / Eval
Production Deployment
```

并能解释为什么某个 Runtime 决策存在、失败时如何恢复、怎样验证它真的工作。
