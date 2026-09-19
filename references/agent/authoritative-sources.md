# Agent Harness｜Authoritative Source Strategy

[← Agent Harness](../../curriculum/09-curriculum/09-agent/README.md) · [↑ Handbook 总目录](../../README.md) · [Agent Source Index](README.md)

> **用途：技术证据策略。** HUMAN-A 决定市场频率；源码 / 官方资料只补成熟 Runtime 事实与工程边界。

---

更新日期：2026-09-11

本项目的 Agent 模块不以单一框架教程为最高标准，而采用四层证据体系：

```text
Tier A  HUMAN-A 真人面经
Tier B  Claude Code / OpenAI Codex 成熟产品源码
Tier C  官方工程文章 / 协议 / SDK 文档 / 原始论文
Tier D  基于 A+B+C 的课程抽象
```

完整 Evidence Base：[`../references/curriculum/09-agent/README.md`](README.md)

> **只有 Tier A 可以贡献真人面试 Source Count。源码和网上权威文章用于补齐完整 Runtime 知识边界，绝不反向虚增面经频率。**

---

## 1. 一级源码参考

### Claude Code

仓库：`studyzhige-ui/claude-code-source-private`（私有）

本轮固定快照：

```text
branch = master
commit = 58231dcce408f805c645cfbc352d2876b517223b
```

已确认的重要 Runtime 入口：

- `QueryEngine.ts`：Conversation / Turn lifecycle 与跨 Turn session state；
- `Tool.ts`：Tool schema、execution context、permission、concurrency、destructive / read-only、interrupt behavior、MCP / Skill / nested memory 等；
- `Task.ts`：local/remote agent、workflow、bash、MCP monitor 等 Task type 与 terminal state；
- `query.ts`：主 Query execution 导航；
- `services/compact/`：Context compact / projection；
- `tools/AgentTool/`：Subagent；
- `types/permissions.ts` / `utils/permissions/`：Permission；
- `services/mcp/`：MCP；
- `memdir/`：Memory；
- `utils/sessionStorage.ts`：Transcript / Session persistence；
- `utils/toolResultStorage.ts`：Tool result context budget。

详细索引：[`../references/agent/claude-code-source-index.md`](claude-code-source-index.md)

### OpenAI Codex

仓库：`openai/codex`

本轮固定快照：

```text
branch = main
commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
tree   = 346154dca409158a441d2afe05604f6fa6bed5d6
```

已确认的重要 Runtime 入口：

- `codex-rs/core/src/compact.rs`：manual/auto compaction、pre/mid-turn phase、replacement history、persistence、retry、hooks、analytics；
- `codex-rs/tools/`：ToolCall / ToolExecutor / ToolOutput 共享 contract；
- `codex-rs/core/src/tools/router.rs`：Tool routing；
- `codex-rs/core/README.md` + `codex-rs/sandboxing/`：Sandbox boundary；
- `codex-rs/app-server-protocol/.../SandboxPolicy.ts`：Sandbox protocol；
- `codex-rs/app-server-protocol/src/protocol/v2/mcp.rs`：MCP catalog；
- `codex-rs/hooks/`：Lifecycle hook runtime；
- `codex-rs/rollout-trace/README.md`：Conversation / Tool / Terminal / Interaction trace evidence；
- `codex-rs/core/src/session/`：Session / Turn / Step 导航。

详细索引：[`../references/agent/codex-source-index.md`](codex-source-index.md)

---

## 2. 官方文章 / 规范 / 原始论文

不能只看两份代码库，因为源码擅长回答“这个产品怎样实现”，但完整课程还需要回答“哪些抽象跨产品成立”。

当前 Tier C 主来源包括：

### Anthropic

- Building effective agents
- Effective context engineering for AI agents
- Effective harnesses for long-running agents
- Harness design for long-running application development
- Scaling Managed Agents: Decoupling the brain from the hands
- Writing effective tools for agents
- Advanced tool use / Tool discovery
- Agent Skills
- Multi-agent research system
- Claude Code sandboxing / containment
- Demystifying evals for AI agents

### OpenAI

- A practical guide to building agents
- OpenAI Agents SDK official docs：Agent Loop / Tools / Sessions / Handoffs / HITL / Guardrails / Tracing / Sandbox

### Protocol / Papers

- Model Context Protocol official specification
- Agent2Agent Protocol official specification
- ReAct original paper
- SWE-bench original paper

完整 URL 与课程影响：[`../references/agent/authoritative-web-sources.md`](authoritative-web-sources.md)

---

## 3. 当前 Runtime Capability Map

综合 A+B+C 后，正式课程至少要覆盖：

1. Agent / Workflow / Harness Boundary
2. Agent Loop / Turn / Step / Stop
3. Runtime Message / Event Model
4. Tool Schema / Registry / Router / Executor
5. Tool Result / Failure / Side Effect / Cancellation
6. Planning / ReAct / Intent / Routing
7. Context Assembly / Token Budget / Tool Result Budget
8. Compaction / Correctness / Stale Context
9. Memory / Session / Durable State
10. Checkpoint / Resume / Fork / Cancellation
11. Retry / Idempotency / Compensation
12. Permission / Approval / Sandbox / Guardrail
13. Prompt Injection / Untrusted Context / Secret Boundary
14. Capability Discovery / Progressive Loading
15. MCP / Resources / Prompts / Tools
16. Skills / Hooks / Plugins
17. Multi-Agent / Subagent / Handoff / A2A
18. Workspace / Shared-resource Concurrency
19. Model Provider / Routing / Fallback
20. Trace / Replay / Observability
21. Evaluation / Benchmark / Outcome Verification
22. Repository Understanding / Code Verification
23. AI-assisted Development Workflow
24. Production Deployment / Tenant / Queue / Backpressure / Cost
25. Framework Mapping / Build-vs-Buy

详细映射：[`../references/agent/runtime-capability-map.md`](runtime-capability-map.md)

---

## 4. 课程设计原则

### 4.1 初学者知识依赖决定主干

即使 Context Compaction 是当前市场最强信号之一，也必须先学习：

```text
Agent Boundary
→ Harness
→ Loop
→ Runtime Event
→ Tool Runtime
→ Context Assembly
→ 才到 Compaction
```

### 4.2 Framework 最后讲

LangChain / LangGraph / OpenAI Agents SDK 等作为 Runtime 理论的实现映射，不作为课程起点。

### 4.3 产品实现不是宇宙真理

源码章节采用：

```text
具体路径 / Symbol
→ 它解决的 Runtime Problem
→ 抽象成稳定概念
→ 比较其它实现
→ Trade-off
```

而不是照搬代码结构当教材目录。

### 4.4 Production Failure 必须是一等公民

Agent Harness 最终必须能回答：

> Context 满了怎么办？Tool 失败怎么办？Tool 已成功产生外部副作用但 Checkpoint 失败怎么办？用户取消时正在运行的命令怎么办？Agent 怎样暂停等待审批再恢复？Subagent 抢同一个文件怎么办？怎样证明任务真的完成？

这才是 Runtime 教材，而不是 Agent Demo 教程。
