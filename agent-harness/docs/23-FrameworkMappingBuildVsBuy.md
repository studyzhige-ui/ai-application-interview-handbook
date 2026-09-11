# 23. Framework Mapping 与 Build-vs-Buy

学完 Agent Harness 最后一章，才开始看框架。

这是刻意安排的。

如果一开始从：

```text
LangChain class
LangGraph node
OpenAI Agents SDK agent
```

出发，你很容易把：

> **某个 Framework 的 API 结构**

误认为：

> **Agent Runtime 本身的知识结构。**

正确顺序应该是：

```text
先知道 Runtime Problem
→ 再知道需要哪些 Primitive
→ 最后把 Primitive 映射到 Framework
```

---

## 1. 先写自己的 Requirement Matrix

在选框架前列：

```text
Agent Loop
Tool Contract
Structured Output
Streaming
Session
Checkpoint / Resume
HITL
Memory
MCP
Sandbox
Multi-Agent
Trace
Eval
Provider Adapter
Deployment
```

然后问：

```text
哪些必须有？
哪些自己已有？
哪些希望交给框架？
```

否则“框架选型”会变成品牌偏好。

---

# 2. Framework 提供的价值通常是什么

框架常帮你解决：

```text
boilerplate
common integration
state / graph abstraction
tool binding
streaming
session persistence
trace hooks
MCP integration
```

好处：

```text
更快开发
少造通用轮子
生态多
```

代价：

```text
abstraction lock-in
hidden runtime semantics
upgrade cost
debug difficulty
```

所以没有“永远用框架”或“永远自研”。

---

# 3. OpenAI Agents SDK 怎样映射

Tier C 官方入口公开的 Runtime Primitive 包括：

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

映射到课程：

```text
Loop           → 03
Tool            → 04–07
Handoff         → 18
Guardrail       → 15
Session / HITL  → 12–14
MCP             → 16
Trace           → 19
Sandbox         → 14
```

这正说明课程 Primitive 可以映射框架，而不需要反过来重建课程目录。

---

# 4. LangGraph 适合解决什么类型问题

当你的 Agent 明显需要：

```text
State Graph
explicit node/edge
branch
pause/resume
human approval
workflow-like determinism
```

Graph abstraction 很有价值。

例如：

```text
classify
→ retrieve
→ if low confidence ask user
→ generate
→ verify
```

用 State Graph 表达清楚。

但如果只是：

```text
LLM ↔ Tool simple loop
```

不一定需要复杂 Graph。

---

# 5. LangChain 适合什么

LangChain 长期价值更多在：

```text
model/tool/retriever integration
common abstractions
ecosystem
```

但生产 Runtime 的：

```text
state correctness
permission
sandbox
checkpoint semantics
idempotency
```

仍然需要你自己理解。

不能回答：

> “用了 LangChain，所以这些问题框架都处理了。”

---

# 6. 什么时候自研 Runtime

可能适合自研：

```text
产品有独特 execution semantics
严格 permission / sandbox
极强 long-running state
高性能 / 极低 overhead
特殊 multi-agent scheduler
强审计 / 合规
现有平台已有很多基础设施
```

但“自研”也不等于：

```text
一切从 socket 开始写
```

可以：

```text
自研 control plane
+ 使用成熟 provider SDK
+ 使用 MCP
+ 使用标准 storage / tracing
```

---

# 7. Build-vs-Buy Matrix

| 维度 | 偏 Framework | 偏自研 |
|---|---|---|
| 上线速度 | ✅ | |
| 常见 Integration | ✅ | |
| 特殊 Runtime Semantics | | ✅ |
| 强权限/隔离 | 视框架 | ✅ |
| Long-running Recovery | 看成熟度 | ✅/混合 |
| 可观测性 | 生态可提供 | 自己控制 |
| 团队维护能力 | 低 | 高 |
| Lock-in 敏感 | | ✅ |

真实决策通常是：

```text
Hybrid
```

---

# 8. Framework Selection 的错误方法

## 8.1 只看 Star

```text
GitHub Star 多
→ 选它
```

不能说明适合你的 Failure Model。

## 8.2 只看 Demo

Demo 很难暴露：

```text
checkpoint corruption
provider failover
permission
multi-tenant state
trace cost
```

## 8.3 只看 Feature Checklist

两个框架都写：

```text
supports memory
```

但 Memory 的：

```text
write policy
version
correctness
```

可能完全不同。

---

# 9. Framework Evaluation 应该用真实 Workload

建立一个小基准：

```text
1. Tool Calling Task
2. Long-running Resume Task
3. HITL Task
4. Multi-agent Task
5. Context Compaction Task
6. Failure / Retry Task
```

对每个 Framework 看：

```text
实现复杂度
可控性
debuggability
latency
state persistence
trace
failure behavior
```

这样选型证据比“团队觉得 API 好看”强。

---

# 10. Escape Hatch 很重要

使用框架时要知道：

```text
能否获取 raw provider response?
能否自定义 state store?
能否接管 tool execution?
能否覆盖 retry?
能否插入 permission?
能否导出 trace?
```

如果所有关键路径都被封死：

```text
未来 Production Requirement 出现时很难扩展
```

---

# 11. Framework Upgrade 风险

Agent Framework 演进非常快。

升级可能改变：

```text
message schema
tool serialization
checkpoint format
state graph semantics
provider adapter
```

所以应用层应尽量隔离：

```text
Domain State
Tool Contract
Eval Dataset
```

不要全部绑死框架内部对象。

---

# 12. 自研最小 Runtime 到底需要什么

一个很小但完整的自研 Loop 可以只有：

```text
Run State
Context Builder
Model Adapter
Tool Registry
Tool Executor
Stop Policy
Event Log
```

然后逐步加入：

```text
checkpoint
permission
trace
MCP
multi-agent
```

这比一开始写“企业级 Agent Platform”更容易验证。

---

# 13. Anthropic `Building effective agents` 的重要启发

官方文章强调：

```text
从简单、可组合 pattern 开始
不要为了 Agent 标签过早引入复杂框架
```

这和本课程 Build-vs-Buy 原则一致：

> **先证明任务需要复杂 Runtime，再引入复杂 Runtime。**

---

# 14. Framework 不会替你解决业务正确性

即使框架提供：

```text
checkpoint
memory
retry
```

你仍然要决定：

```text
Tool 已成功但 checkpoint 失败怎么办？
Memory 过期怎么办？
哪个动作必须 approval？
什么算任务成功？
```

这些是业务/Runtime Contract，不是一个 API 开关。

---

# 15. HUMAN-A 信号

`AGENT-047 Agent Framework Selection` 有 27 个独立来源。

真实面试常问：

```text
为什么 LangGraph？
LangChain 和 LangGraph 区别？
为什么不自研？
State Graph 什么时候有价值？
框架哪里不够？
```

高质量回答不应该是产品宣传，而应该回到 Runtime Requirement。

---

# 16. 一个选型回答模板

假设面试官问：

> 为什么用 LangGraph？

不要只答：

> “它适合 Agent。”

更好：

```text
我们的任务需要：
- 显式 state
- branch
- pause/resume
- HITL
- 可追踪 node transition

因此 graph runtime 能自然表达这些 requirement。
简单 tool loop 仍保持轻量，不全部塞 graph。
```

这样体现的是工程判断。

---

# 17. Framework Migration

如果未来迁移框架，最重要的是把下面几层保持独立：

```text
Domain State
Tool Contract
Event / Trace Schema
Eval Dataset
Business Acceptance Criteria
```

如果这些都绑框架：

```text
迁移 = 重写整个 Agent 产品
```

反之可以：

```text
换 Orchestrator
但 Tool / State / Eval 不全部推倒
```

---

# 18. 面试怎么答

## Q：LangChain / LangGraph / 自研怎么选？

🎯 **30 秒回答**：

> 我不会从框架名出发，而先列 Runtime Requirement。只是模型+Tool 循环可以保持轻；如果有显式状态图、复杂分支、pause/resume、HITL，LangGraph 类 graph runtime 更合适；LangChain 更偏通用模型、Tool、Retriever integration。若产品有特殊 permission/sandbox、long-running reliability 或调度语义，可以自研 control plane，同时复用 Provider SDK、MCP、storage 等成熟组件。最终用真实 workload 和 failure case 做 POC，而不是按 Star 选。

---

# 19. 高频易错点

⚠️ **用了 Framework 就不用懂 Runtime。** 恰恰相反，Production 问题仍需要理解底层语义。

⚠️ **自研 = 所有东西自己写。** 可以只自研关键控制面。

⚠️ **LangGraph 更高级，所以所有 Agent 都用。** 简单任务可能过度设计。

⚠️ **Feature Checklist 一样就等价。** Failure / State / Trace 语义可能完全不同。

---

# 20. 本章自测

<details><summary>1. 为什么课程最后才讲 Framework Mapping？</summary>

因为 Runtime Problem 和 Primitive 比框架 API 更稳定。先理解 Context、Tool、State、Checkpoint、Permission，再看框架怎样实现，才能避免把某个 class hierarchy 当成 Agent 原理。
</details>

<details><summary>2. 什么情况下 State Graph 特别有价值？</summary>

当流程有显式状态、复杂 branch、pause/resume、HITL 或需要清晰可观测的 transition 时；简单 tool loop 不一定需要图模型。
</details>

<details><summary>3. Build-vs-Buy 最重要的评估方式是什么？</summary>

用自己的真实 workload 和 failure case 做 POC，评估 state、recovery、permission、trace、latency、维护成本，而不是只看 Demo 或 feature list。
</details>
