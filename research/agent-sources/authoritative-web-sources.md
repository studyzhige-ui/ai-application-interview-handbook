# Authoritative Web Sources — Agent / Harness / Runtime

更新日期：2026-09-11

> Evidence Tier C。只收官方工程文章、官方协议 / SDK 文档与原始论文。它们用于补齐课程知识边界和跨产品抽象；**不得反向修改 HUMAN-A Source Count**。

## 1. Agent / Workflow / Harness 基础

### Anthropic — Building effective agents

- URL: https://www.anthropic.com/engineering/building-effective-agents
- 价值：强调从简单、可组合 pattern 出发，区分 workflow 与更自主的 agent，不建议为了“Agent”标签过早引入复杂框架。
- 课程影响：Agent Boundary、Workflow vs Agent、Orchestration、Framework Selection。

### OpenAI — A practical guide to building agents

- URL: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- 价值：从模型、工具、instructions/orchestration 与安全控制解释生产 Agent 的基本组成。
- 课程影响：Agent Boundary、Tool、Guardrail、Orchestration、HITL。

### Anthropic — Trustworthy agents in practice

- URL: https://www.anthropic.com/research/trustworthy-agents
- 价值：把 Agent 行为理解为 model + harness + tools + environment 的共同结果，并把 human control、secure interactions、transparency、privacy 放进产品设计。
- 课程影响：Harness Boundary、Permission、Environment、Trust / Security。

## 2. Context Engineering / Long-running Harness

### Anthropic — Effective context engineering for AI agents

- URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 价值：Context 不等于 System Prompt；应管理 instructions、tools、MCP、external data、message history 等整个 inference state，并持续在有限 token budget 内做选择。
- 课程影响：Context Assembly、Budget、Compaction、Tool Result Management、Memory Boundary。

### Anthropic — Effective harnesses for long-running agents

- URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 价值：单纯 compaction 不足以保证长任务连续性；长任务还需要明确进度、环境状态和交接 artifacts。
- 课程影响：Long-running Task、Checkpoint、Resume、Progress Artifact、Verification。

### Anthropic — Harness design for long-running application development

- URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- 价值：展示 Harness Design 本身会显著影响 Agent 在长任务中的行为与产出质量。
- 课程影响：Harness Engineering、Task Decomposition、Verification、Long-horizon Control。

### Anthropic — Scaling Managed Agents: Decoupling the brain from the hands

- URL: https://www.anthropic.com/engineering/managed-agents
- 价值：将 brain/harness、hands/execution environments、durable session log 解耦；把 session 作为 context-window 外的可恢复事件存储，把 context selection 放回 harness。
- 课程影响：Runtime Architecture、Durable Session、Execution Environment、Tool Boundary、Horizontal Scale。

## 3. Tool / Skill / Capability Discovery

### Anthropic — Writing effective tools for agents — with agents

- URL: https://www.anthropic.com/engineering/writing-tools-for-agents
- 价值：Tool quality 需要通过真实 agent evaluation 迭代；清晰定义、节省 context、可组合性是核心。
- 课程影响：Tool Contract、Schema、Description、Evaluation、Tool Failure。

### Anthropic — Introducing advanced tool use

- URL: https://www.anthropic.com/engineering/advanced-tool-use
- 价值：大规模工具库不应把所有 schema 一次塞进 Context；Tool discovery 与按需加载是独立 Runtime 能力。
- 课程影响：Tool Registry、Discovery、Progressive Loading、Context Cost。

### Anthropic — Agent Skills

- URL: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- 价值：Skills 将 procedural knowledge、scripts、resources 打包成可发现 / 可加载能力；它和 Tool/MCP 不是同一抽象。
- 课程影响：Skill、Capability Abstraction、Progressive Loading。

## 4. MCP / A2A Protocol

### Model Context Protocol — Official Specification

- URL: https://modelcontextprotocol.io/specification/2025-06-18/server/index
- 价值：官方明确区分 Prompts、Resources、Tools，并给出 user-controlled / application-controlled / model-controlled 的控制边界。
- 课程影响：MCP Architecture、Tool vs Resource vs Prompt、Host/Client/Server Boundary。

### Agent2Agent Protocol — Official Specification

- URL: https://a2a-protocol.org/dev/specification/
- 价值：A2A 面向独立、可能内部不透明的 Agent 系统，支持 capability discovery、interaction modality negotiation、collaborative task management 与 secure information exchange。
- 课程影响：A2A、Agent-to-Agent Boundary、Task/Artifact Protocol、MCP vs A2A。

## 5. Permission / Sandbox / Human-in-the-loop

### Anthropic — Beyond permission prompts: making Claude Code more secure and autonomous

- URL: https://www.anthropic.com/engineering/claude-code-sandboxing
- 价值：把 filesystem / network isolation 与 permission prompt 分离；安全边界做好后可以减少不必要审批，同时控制 blast radius。
- 课程影响：Permission vs Sandbox、Filesystem / Network Policy、Autonomy Boundary。

### Anthropic — How we contain Claude across products

- URL: https://www.anthropic.com/engineering/how-we-contain-claude
- 价值：Agent 越强，重点不仅是降低错误概率，也要限制单次错误可能造成的 blast radius。
- 课程影响：Containment、Least Privilege、Environment Boundary、Production Security。

### OpenAI Agents SDK — Human-in-the-loop

- URL: https://openai.github.io/openai-agents-python/human_in_the_loop/
- 价值：敏感 Tool Call 可以形成 interruption，RunState 可序列化暂停状态并在审批后 resume；审批跨 handoff / nested agent 传播。
- 课程影响：Approval、Pause / Resume、Run State、Sensitive Side Effect。

### OpenAI Agents SDK — Guardrails

- URL: https://openai.github.io/openai-agents-python/guardrails/
- 价值：区分 Input、Output、Tool Guardrail；说明安全/校验是不同生命周期边界上的 Runtime primitive。
- 课程影响：Guardrail、Validation、Failure Boundary。

## 6. Agent Loop / Multi-Agent

### ReAct — Synergizing Reasoning and Acting in Language Models

- URL: https://arxiv.org/abs/2210.03629
- 价值：原始论文用 interleaved reasoning/action 说明模型如何通过环境 observation 持续更新行动。
- 课程影响：Agent Loop、Reason/Act/Observe、Planning Boundary。

### Anthropic — How we built our multi-agent research system

- URL: https://www.anthropic.com/engineering/multi-agent-research-system
- 价值：Multi-Agent 对高并行、开放探索任务可能有效，但带来更高 token 成本、协调和评估复杂度；不是默认优于 Single Agent。
- 课程影响：Subagent、Parallelism、Delegation、Context Isolation、Cost / Eval。

## 7. Trace / Evaluation / Verification

### OpenAI Agents SDK — Tracing

- URL: https://openai.github.io/openai-agents-js/guides/tracing/
- 价值：Trace 层级覆盖 task / agent / turn / generation / tool / guardrail / handoff；便于 Debug、Monitoring 与 Evaluation。
- 课程影响：Runtime Event Model、Trace / Span、Replay / Debug。

### Anthropic — Demystifying evals for AI agents

- URL: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 价值：明确区分 transcript、environment outcome、evaluation harness、agent harness 与 evaluation suite；最终结果不能只看 Agent 自己说“完成了”。
- 课程影响：Agent Evaluation、Outcome Verification、Eval Harness、Dataset。

### SWE-bench — Can Language Models Resolve Real-World GitHub Issues?

- URL: https://arxiv.org/abs/2310.06770
- 价值：用真实 GitHub issue + repository environment 评估代码修改是否真正解决问题，强调跨文件理解、环境交互与可验证结果。
- 课程影响：Coding Agent Evaluation、Repository Understanding、Patch Verification。

## 8. OpenAI Agents SDK 作为 Framework Mapping，而非课程起点

官方入口：

- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/agents/
- https://openai.github.io/openai-agents-python/running_agents/

SDK 当前公开的 Runtime primitives 包括：

```text
built-in agent loop
function tools
handoffs / agents-as-tools
guardrails
sessions
HITL
MCP
tracing
sandbox agents
```

课程使用方式：先学对应 Runtime Problem，再把这些 primitives 作为一种实现映射；不倒过来用 SDK class hierarchy 定义整个知识体系。

---

## 9. 取舍原则

不纳入主证据层的内容：

- SEO Agent 教程；
- 单纯框架快速上手；
- 无实现 / 无实验的“十大 Agent 架构”；
- 只画概念图、不定义 failure semantics 的二次文章；
- 无法区分 model capability 与 harness capability 的营销材料。

Tier C 的目标不是“链接越多越好”，而是给每个稳定 Runtime 概念找到尽量接近第一方 / 原始来源的定义与工程证据。
