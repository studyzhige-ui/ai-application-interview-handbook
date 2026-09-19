# 24. Framework Mapping：按核心语义比较框架与自研

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

> **Agent Runtime（运行时执行系统） 本身的知识结构。**

正确顺序应该是：

```text
先知道 Runtime Problem
→ 再知道需要哪些 Primitive
→ 最后把 Primitive 映射到 Framework
```

[← 上一章](23-ProductionRuntime.md) · [Agent 目录](../README.md) · [综合复习 →](../review/README.md)

---

<a id="section-1"></a>

## 1. 先写自己的 Requirement Matrix

<a id="legacy-23-01"></a>

OpenAI Agents SDK、LangGraph和LangChain提供开发抽象；Codex与Claude Code是具体Agent产品及其实现参考；自研Loop是你自己承担实现责任的选择。不能把它们放在一张“谁更高级”的排行榜里。

本章依据核验时官方Python文档解释核心语义，不把未来版本能力或某份源码全部推广为永恒标准。先看任务契约，再看框架是否能表达你的状态、工具、恢复与验收。

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

<a id="section-2"></a>

## 2. Framework 提供的价值通常是什么

<a id="legacy-23-02"></a>

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

<a id="section-3"></a>

## 3. OpenAI Agents SDK 怎样映射

<a id="legacy-23-03"></a>

Agent对象主要定义指令、模型、工具、handoffs和输出约束；Runner驱动运行：请求当前Agent模型，执行工具或交接，继续循环，直到满足最终输出或停止/错误条件。`function_tool`把Python函数包装为可调用工具并生成相应Schema，但不替业务定义权限和幂等。

| 官方抽象 | 负责什么 | 不能误认为 |
|---|---|---|
| Agent | 一组执行配置与能力 | 一个已运行且永久持久化的任务 |
| Runner | 推进模型、工具、交接的循环 | 自动恢复所有外部副作用 |
| Handoff（控制权交接） | 将当前控制转给另一Agent | 与agents-as-tools完全同义 |
| Session | 调用前取历史、结束后更新会话历史等 | 任意业务工作流的事务检查点 |
| RunState/人工参与机制 | 保存中断运行所需状态并继续 | 与所有存储、版本天然兼容 |
| Tracing | 记录执行过程的诊断 | 默认权威业务账本 |

<details>
<summary>官方生命周期对照：有历史的两次调用不等于事务工作流</summary>

根据官方Running agents、Sessions与Human-in-the-loop文档：应用建立Agent与Runner，选用Session时运行前取相关历史、运行后保存新交互；一次执行内部可有多轮模型与工具。需要批准的工具让运行产生中断，应用可获取运行状态，提交批准或拒绝后继续。

Sessions的主要语义是会话项管理，RunState用于暂停执行；即使同一应用使用两者，也要明确保存什么、谁授权恢复以及外部工具执行是否已经发生。不可把“用了SQLiteSession”直接回答成“任意节点都能恰好一次恢复”。具体API以所安装版本为准，本章不把示意流程当完整可运行代码。

</details>

---

<a id="section-4"></a>

## 4. LangGraph 适合解决什么类型问题

<a id="legacy-23-04"></a>

LangGraph用StateGraph描述状态如何在Node（节点）和Edge（边）之间流动。Node读取状态并返回更新；Reducer（合并规则）决定多个更新如何合并。图可以包含模型、普通函数、工具或子图，不是每个节点都必须是Agent。

Checkpointer按执行调度边界保存快照，通常通过thread_id关联；Store用于跨线程的持久数据等用途，与当前执行检查点不同。`interrupt()`暂停等待外部输入，使用相应Command恢复；节点恢复可能从头执行，中断前副作用需幂等。事件驱动、分支并发与pending writes的语义都应按官方Persistence（持久化）文档理解。

<details>
<summary>官方生命周期对照：State、Checkpointer、Store各在什么时候用</summary>

先声明状态与合并规则，再加入节点和边，编译图时提供需要的Checkpointer。调用图时给输入和thread_id，节点按调度轮次运行，检查点记录状态。某节点中断后，应用保存并展示待办，用户回应再用原线程上下文恢复；不是新建一个完全无关任务。

跨会话用户偏好可以放Store，在节点需要时读取。它不自动成为当前图状态，也不因检查点而自动校验正确性。并行节点失败时框架可保留已完成节点写入，但恢复单位仍由框架定义，不能恢复任意Python指令位置。

</details>

---

<a id="section-5"></a>

## 5. LangChain 适合什么

<a id="legacy-23-05"></a>

官方当前`create_agent`提供更高层Agent入口，并以LangGraph作为运行基础；工具、中间件、模型和结构化输出等集成减少样板代码。这与“LangChain只是旧式线性Chain，LangGraph才可以做Agent”的陈旧说法不同。

更高层默认行为适合快速实现常见任务；当控制流、状态合并和中断点需要精细设计时，可以使用底层图能力。两者不是必须二选一的竞争关系，但应确认版本和你用的具体接口，不能把早期教程与当前create_agent混为一谈。

---

<a id="section-6"></a>

## 6. 什么时候自研 Runtime

<a id="legacy-23-06"></a>

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

<a id="section-7"></a>

## 7. Build-vs-Buy Matrix

<a id="legacy-23-07"></a>

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

| 维度 | Agents SDK | LangGraph | LangChain高层Agent | 自研最小Loop |
|---|---|---|---|---|
| 起点 | Agent配置与Runner循环 | 显式状态图和调度 | create_agent及集成 | 自己定义状态与控制 |
| 控制流 | 工具、交接、运行选项 | 节点、边、条件、子图 | 默认循环与中间件扩展 | 完全可控但都要实现 |
| 持久语义 | Session与中断运行状态需分别理解 | Checkpointer、thread、pending writes、Store | 使用底层图能力时遵循其语义 | 自己实现并验证 |
| 工具接入 | 函数/托管工具及适配 | 工具节点或自定义节点 | 工具/模型生态与中间件 | 维护Schema、路由和执行 |
| 适合重点 | 较直接的Agent循环与角色交接 | 复杂状态、分支、中断与恢复设计 | 常见应用快速集成 | 范围小或需特殊控制 |
| 共同责任 | 业务权限、幂等、验收与部署不自动解决 | 同左 | 同左 | 全部由团队承担 |

“适合”是基于抽象匹配的工程判断，不是官方保证。若只需两个只读工具，轻量Loop可能最易讲清；若已有复杂人工审批和图恢复需求，成熟状态机制可能减少工作量。比较应使用相同任务和失败窗口，而不是只数功能项。

---

<a id="section-8"></a>

## 8. Framework Selection 的错误方法

<a id="legacy-23-08"></a>

### 8.1 只看 Star

```text
GitHub Star 多
→ 选它
```

不能说明适合你的 Failure Model。

### 8.2 只看 Demo

Demo 很难暴露：

```text
checkpoint corruption
provider failover
permission
multi-tenant state
trace cost
```

### 8.3 只看 Feature Checklist

两个框架都写：

```text
supports memory
```

但 Memory（记忆） 的：

```text
write policy
version
correctness
```

可能完全不同。

---

<a id="section-9"></a>

## 9. Framework Evaluation 应该用真实 Workload

<a id="legacy-23-09"></a>

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

用同一正常任务、格式错误、审批、重启、未知副作用和版本升级测试进行比较。未验证的能力如实标记，不把框架功能清单当本应用已通过的保证。

---

<a id="section-10"></a>

## 10. Escape Hatch 很重要

<a id="legacy-23-10"></a>

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

<a id="section-11"></a>

## 11. Framework Upgrade 风险

<a id="legacy-23-11"></a>

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

<a id="section-12"></a>

## 12. 自研最小 Runtime 到底需要什么

<a id="legacy-23-12"></a>

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

<a id="section-13"></a>

## 13. Framework 不会替你解决业务正确性

<a id="legacy-23-14"></a>

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

<a id="section-14"></a>

## 14. Framework Migration

<a id="legacy-23-17"></a>

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

<a id="section-15"></a>

## 15. 产品实现与官方资料对照（按需展开）

<details>
<summary>Anthropic `Building effective agents` 的重要启发</summary>

<a id="legacy-23-13"></a>

官方文章强调：

```text
从简单、可组合 pattern 开始
不要为了 Agent 标签过早引入复杂框架
```

这和本课程 Build-vs-Buy 原则一致：

> **先证明任务需要复杂 Runtime，再引入复杂 Runtime。**

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[Agents SDK执行循环](https://openai.github.io/openai-agents-python/running_agents/) · [Sessions](https://openai.github.io/openai-agents-python/sessions/) · [LangGraph持久化](https://docs.langchain.com/oss/python/langgraph/persistence) · [LangGraph中断](https://docs.langchain.com/oss/python/langgraph/interrupts) · [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)。

---

<a id="human-a"></a>

## 16. HUMAN-A 信号

`AGENT-047` Agent Framework Selection 有 27 个独立来源。

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

<a id="interview"></a>

## 17. 面试怎么答

### Q：怎样完整说明框架选型的理由？

🎯 **30 秒回答**：

> 假设面试官问：
>
> 为什么用 LangGraph？
>
> 不要只答：
>
> “它适合 Agent。”
>
> 更好：
>
> ```text
> 我们的任务需要：
> - 显式 state
> - branch
> - pause/resume
> - HITL
> - 可追踪 node transition
>
> 因此 graph runtime 能自然表达这些 requirement。
> 简单 tool loop 仍保持轻量，不全部塞 graph。
> ```
>
> 这样体现的是工程判断。

### Q：LangChain / LangGraph / 自研怎么选？

🎯 **30 秒回答**：

> 我不会从框架名出发，而先列 Runtime Requirement。只是模型+Tool 循环可以保持轻；如果有显式状态图、复杂分支、pause/resume、HITL，LangGraph 类 graph runtime 更合适；LangChain 更偏通用模型、Tool、Retriever integration。若产品有特殊 permission/sandbox、long-running reliability 或调度语义，可以自研 control plane，同时复用 Provider（模型服务方） SDK、MCP、storage 等成熟组件。最终用真实 workload 和 failure case 做 POC，而不是按 Star 选。

### Q：Agents SDK、LangGraph、LangChain与自研怎么选？

🎯 **30 秒回答**：

> 先定义任务状态、控制流、工具、人工参与、恢复和部署要求。Agents SDK以Agent与Runner循环为核心，LangGraph显式管理状态图与检查点，LangChain当前create_agent提供基于LangGraph的高层集成。自研适合范围小或特殊控制，但要承担可靠性。用相同任务和故障验证比较，而不是按热度选。

### Q：Session、Checkpointer和Store是一回事吗？

🎯 **30 秒回答**：

> 不是。Session通常管理会话历史；Checkpointer管理定义执行边界的状态快照；Store可用于跨会话数据和记忆。具体以框架语义为准，它们不自动解决外部写操作的恰好一次问题。

### Q：LangGraph interrupt恢复为什么还要考虑副作用？

🎯 **30 秒回答**：

> 节点可能从开头重跑，中断前代码可能再执行。检查点恢复图状态不等于回到任意CPU指令，也不回滚外部世界。因此动作要幂等、独立包装或可核对。

### Q：怎样避免未来被框架绑定？

🎯 **30 秒回答**：

> 保持业务状态、工具契约、验收用例和必要事件/产物格式独立，确认能导出状态、替换执行器与重试、接入权限和观测。迁移风险要实际验证，不只相信功能清单。

---

<a id="pitfalls"></a>

## 18. 高频易错点

⚠️ **用了 Framework 就不用懂 Runtime。** 恰恰相反，Production（生产环境） 问题仍需要理解底层语义。

⚠️ **自研 = 所有东西自己写。** 可以只自研关键控制面。

⚠️ **LangGraph 更高级，所以所有 Agent 都用。** 简单任务可能过度设计。

⚠️ **Feature Checklist 一样就等价。** Failure / State（状态） / Trace（执行追踪） 语义可能完全不同。

⚠️ **框架越重越Production。** 抽象不匹配会增加复杂度。

⚠️ **自研Loop一定更专业。** 实现与维护可靠性也有成本。

⚠️ **有Session就是完整业务恢复。** 会话项与执行/副作用状态不同。

⚠️ **LangChain永远只是线性Chain。** 当前官方Agent入口基于LangGraph，需按版本说明。

⚠️ **Node/Edge就是Agent的本质。** 它是实现控制流的一种抽象。

⚠️ **使用产品源码等于集成了产品所有保证。** 部署、配置、任务契约和验证仍由自己的系统负责。

---

<a id="self-test"></a>

## 19. 本章自测

<details><summary>1. 为什么课程最后才讲 Framework Mapping？</summary>

因为 Runtime Problem 和 Primitive 比框架 API 更稳定。先理解 Context、Tool、State、Checkpoint（检查点）、Permission（权限），再看框架怎样实现，才能避免把某个 class hierarchy 当成 Agent 原理。

</details>

<details><summary>2. 什么情况下 State Graph 特别有价值？</summary>

当流程有显式状态、复杂 branch、pause/resume、HITL 或需要清晰可观测的 transition 时；简单 tool loop 不一定需要图模型。

</details>

<details><summary>3. Build-vs-Buy 最重要的评估方式是什么？</summary>

用自己的真实 workload 和 failure case 做 POC，评估 state、recovery、permission、trace、latency、维护成本，而不是只看 Demo 或 feature list。

</details>

<details><summary>4. 两个只读工具的小任务一定需要显式状态图吗？</summary>

不一定。若简单Loop更清楚且满足故障承诺，可先用它；复杂度由任务需要而不是教材组件数决定。

</details>

<details><summary>5. 用了SQLiteSession后邮件会自动不重复吗？</summary>

不能据此保证。会话历史保存不等于邮件API的幂等与结果核对，要检查实际执行恢复窗口。

</details>

<details><summary>6. LangGraph Store里有用户偏好，模型会自动知道吗？</summary>

不会仅因存着就知道。节点需读取相关信息并按规则编排入模型输入；Store与Context不是同一个对象。

</details>

<details><summary>7. Handoff之后控制权变化和子Agent返回有何不同？</summary>

交接让另一个Agent成为当前处理角色；agents-as-tools把子工作结果返回调用者，父级继续。框架API应准确匹配所需控制语义。

</details>

<details><summary>8. 选型表看起来全都支持恢复，怎样进一步验证？</summary>

制造中断、部分节点成功、外部成功但回执丢失等具体窗口，观察恢复单位、重复动作和状态导出。功能名相同不代表语义相同。

</details>

<details><summary>9. 什么情况下不能宣布框架选型完成？</summary>

关键权限、恢复或部署条件尚未验证，或测试只覆盖正常Demo。应列出已证实和待验证要求，而不是把疑问藏在“支持生产”里。

</details>

---

[← 上一章](23-ProductionRuntime.md) · [Agent 目录](../README.md) · [综合复习 →](../review/README.md)
