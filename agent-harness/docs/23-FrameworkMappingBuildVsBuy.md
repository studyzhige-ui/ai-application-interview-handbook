# 23｜Framework Mapping 与 Build-vs-Buy

> Framework 放在最后。目标不是教 LangChain / LangGraph / OpenAI Agents SDK API，而是把前 22 章的 Runtime Primitive 映射到不同框架，并判断什么时候应该自研、组合或直接购买平台能力。

## 1. 为什么 Framework 不能作为课程起点

如果先学：

```text
Node
Edge
Graph
Agent class
Tool decorator
```

很容易只会回答：

> “这个框架 API 怎么写？”

却不知道：

```text
Checkpoint 为什么存在？
Tool Failure 谁负责？
Context Compaction 放哪？
Side Effect 怎么幂等？
Permission 与 Sandbox 怎么分层？
```

正确顺序：

```text
Runtime Problem
→ Runtime Primitive
→ Trade-off / Failure
→ Framework Mapping
```

## 2. Framework 常提供哪些能力

典型：

```text
agent loop
workflow / graph
state
tool registration
structured output
handoff / subagent
checkpoint / session
MCP
tracing
guardrail / HITL
```

但不同框架覆盖深度非常不同。

## 3. LangChain / LangGraph 的工作边界

不把具体版本 API 写成永恒规则，稳定理解：

```text
LangChain
→ model/tool/retrieval 等高层组件抽象

LangGraph
→ 更强调 stateful graph / node-edge control / durable execution
```

什么时候需要 Graph：

- 业务状态和 transition 明确；
- 需要 pause/resume；
- 需要可视化控制流；
- Agentic Step 与 deterministic Node 混合。

什么时候普通代码更好：

- Loop 很简单；
- State 很小；
- 框架抽象反而增加 Debug 成本。

## 4. OpenAI Agents SDK 等 Runtime SDK

官方 SDK 当前会提供一组 Runtime primitives，例如：

```text
built-in loop
function tools
handoffs / agents-as-tools
guardrails
sessions
HITL
MCP
tracing
sandbox-related capability
```

课程使用方式是：

> 用它验证 / 映射我们已经学过的 primitive，而不是让 SDK class hierarchy 决定整个知识体系。

## 5. Build vs Buy 的判断维度

| 维度 | 更倾向 Framework / Platform | 更倾向自研 Runtime |
|---|---|---|
| Time-to-market | 高优先 | 可投入长期建设 |
| Workflow 标准化 | 高 | 高度定制 |
| State / Resume | 框架已满足 | 需要特殊语义 |
| Permission / Sandbox | 平台适配 | 强业务安全边界 |
| Tool Ecosystem | 标准工具多 | 内部能力复杂 |
| Observability | 通用即可 | 需要自定义 Trace/Eval |
| Lock-in | 可接受 | 必须多 Provider / 多环境 |
| Team Capability | 应用团队 | 有 Runtime/Infra 能力 |

## 6. 最常见的错误选择

### 为了简历“用了 LangGraph”而引入 Graph

如果系统只有：

```text
LLM → one tool → answer
```

Graph 可能只是增加复杂度。

### 因为框架不完美就全部自研

自研意味着你自己承担：

```text
state
checkpoint
stream
tool protocol
trace
security
version compatibility
```

成本很高。

### 把框架限制误认为 Agent 原理

例如某框架的 State Shape、Node 定义，不等于 Agent Runtime 的唯一正确模型。

## 7. 一个成熟策略：薄框架 + 自己的 Domain Runtime

```text
Domain Model / State / Policy
        ↓
Your Runtime Boundary
        ↓
Framework Adapter
        ↓
LLM / Tool / Checkpoint Provider
```

这样可以让业务 invariant 不被框架类型绑定。

## 8. HUMAN-A

`AGENT-047 Framework Selection` 有 27 个独立来源。

Verified Follow-up Chain 常见：

```text
为什么 LangGraph / LangChain？
→ Graph / State 解决什么？
→ State 怎样持久化？
→ Failure 后怎样 Resume？
→ Long-running 怎么稳定？
```

所以面试回答不能停在“我熟悉 API”。

## 9. 🎯 面试回答

> 我会先按 Runtime Problem 选框架，而不是先定框架再套业务。简单 Loop 可以直接代码实现；需要显式 State Graph、pause/resume、checkpoint 或复杂 deterministic+agentic 混合流程时，LangGraph 一类框架更有价值。框架适合承担通用 primitive，但业务 State、Permission、Side-effect invariant、Eval 和 Provider Boundary 最好保留自己的抽象，避免深度锁定。是否自研要按 time-to-market、可靠性、安全、可观测和团队维护成本综合判断。

## 10. 全模块最终检查

学完 23 个板块，应能不依赖框架名画出：

```text
Goal
→ Runtime State
→ Context
→ Model
→ Tool / Delegate
→ Permission / Sandbox
→ Event / Checkpoint
→ Trace / Eval
→ Stop / Resume
```

如果离开 LangGraph / LangChain API 就无法解释这张图，说明学到的是框架，不是 Harness。

<details><summary>自测：什么时候 State Graph 是真正的价值，而不是“为了用 LangGraph”？</summary>

当业务本身存在显式状态、条件 transition、pause/resume、checkpoint、deterministic 与 agentic node 混合，并且这些控制语义需要被测试和恢复时，State Graph 才有独立价值。
</details>