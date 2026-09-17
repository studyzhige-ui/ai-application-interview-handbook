# 23. 框架与自研怎么选：按官方核心语义做比较

[← 上一章](22-ProductionAgentRuntime.md) · [模块目录](../README.md) · [综合复习 →](../review/README.md)

> 本章要解决：用Agent、Runner、StateGraph、Checkpointer、Store等真实抽象理解框架，而不是空泛优缺点。

## 1. 先说明比较的不是同一种产品

OpenAI Agents SDK、LangGraph和LangChain提供开发抽象；Codex与Claude Code是具体Agent产品及其实现参考；自研Loop是你自己承担实现责任的选择。不能把它们放在一张“谁更高级”的排行榜里。

本章依据核验时官方Python文档解释核心语义，不把未来版本能力或某份源码全部推广为永恒标准。先看任务契约，再看框架是否能表达你的状态、工具、恢复与验收。

## 2. OpenAI Agents SDK：Agent配置与Runner循环

Agent对象主要定义指令、模型、工具、handoffs和输出约束；Runner驱动运行：请求当前Agent模型，执行工具或交接，继续循环，直到满足最终输出或停止/错误条件。`function_tool`把Python函数包装为可调用工具并生成相应Schema，但不替业务定义权限和幂等。

| 官方抽象 | 负责什么 | 不能误认为 |
|---|---|---|
| Agent | 一组执行配置与能力 | 一个已运行且永久持久化的任务 |
| Runner | 推进模型、工具、交接的循环 | 自动恢复所有外部副作用 |
| Handoff | 将当前控制转给另一Agent | 与agents-as-tools完全同义 |
| Session | 调用前取历史、结束后更新会话历史等 | 任意业务工作流的事务检查点 |
| RunState/人工参与机制 | 保存中断运行所需状态并继续 | 与所有存储、版本天然兼容 |
| Tracing | 记录执行过程的诊断 | 默认权威业务账本 |

<details>
<summary>官方生命周期对照：有历史的两次调用不等于事务工作流</summary>

根据官方Running agents、Sessions与Human-in-the-loop文档：应用建立Agent与Runner，选用Session时运行前取相关历史、运行后保存新交互；一次执行内部可有多轮模型与工具。需要批准的工具让运行产生中断，应用可获取运行状态，提交批准或拒绝后继续。

Sessions的主要语义是会话项管理，RunState用于暂停执行；即使同一应用使用两者，也要明确保存什么、谁授权恢复以及外部工具执行是否已经发生。不可把“用了SQLiteSession”直接回答成“任意节点都能恰好一次恢复”。具体API以所安装版本为准，本章不把示意流程当完整可运行代码。

</details>

## 3. LangGraph：显式状态图与检查点

LangGraph用StateGraph描述状态如何在Node（节点）和Edge（边）之间流动。Node读取状态并返回更新；Reducer（合并规则）决定多个更新如何合并。图可以包含模型、普通函数、工具或子图，不是每个节点都必须是Agent。

Checkpointer按执行调度边界保存快照，通常通过thread_id关联；Store用于跨线程的持久数据等用途，与当前执行检查点不同。`interrupt()`暂停等待外部输入，使用相应Command恢复；节点恢复可能从头执行，中断前副作用需幂等。事件驱动、分支并发与pending writes的语义都应按官方Persistence文档理解。

<details>
<summary>官方生命周期对照：State、Checkpointer、Store各在什么时候用</summary>

先声明状态与合并规则，再加入节点和边，编译图时提供需要的Checkpointer。调用图时给输入和thread_id，节点按调度轮次运行，检查点记录状态。某节点中断后，应用保存并展示待办，用户回应再用原线程上下文恢复；不是新建一个完全无关任务。

跨会话用户偏好可以放Store，在节点需要时读取。它不自动成为当前图状态，也不因检查点而自动校验正确性。并行节点失败时框架可保留已完成节点写入，但恢复单位仍由框架定义，不能恢复任意Python指令位置。

</details>

## 4. LangChain：高层Agent入口与集成

官方当前`create_agent`提供更高层Agent入口，并以LangGraph作为运行基础；工具、中间件、模型和结构化输出等集成减少样板代码。这与“LangChain只是旧式线性Chain，LangGraph才可以做Agent”的陈旧说法不同。

更高层默认行为适合快速实现常见任务；当控制流、状态合并和中断点需要精细设计时，可以使用底层图能力。两者不是必须二选一的竞争关系，但应确认版本和你用的具体接口，不能把早期教程与当前create_agent混为一谈。

## 5. 维度比较：选择由要求驱动

| 维度 | Agents SDK | LangGraph | LangChain高层Agent | 自研最小Loop |
|---|---|---|---|---|
| 起点 | Agent配置与Runner循环 | 显式状态图和调度 | create_agent及集成 | 自己定义状态与控制 |
| 控制流 | 工具、交接、运行选项 | 节点、边、条件、子图 | 默认循环与中间件扩展 | 完全可控但都要实现 |
| 持久语义 | Session与中断运行状态需分别理解 | Checkpointer、thread、pending writes、Store | 使用底层图能力时遵循其语义 | 自己实现并验证 |
| 工具接入 | 函数/托管工具及适配 | 工具节点或自定义节点 | 工具/模型生态与中间件 | 维护Schema、路由和执行 |
| 适合重点 | 较直接的Agent循环与角色交接 | 复杂状态、分支、中断与恢复设计 | 常见应用快速集成 | 范围小或需特殊控制 |
| 共同责任 | 业务权限、幂等、验收与部署不自动解决 | 同左 | 同左 | 全部由团队承担 |

“适合”是基于抽象匹配的工程判断，不是官方保证。若只需两个只读工具，轻量Loop可能最易讲清；若已有复杂人工审批和图恢复需求，成熟状态机制可能减少工作量。比较应使用相同任务和失败窗口，而不是只数功能项。

## 6. 怎样做一次有证据的选型

准备六类小验证：正常工具任务、长任务恢复、人工批准、上下文压缩、多Agent控制与工具未知结果。记录实现复杂度、调试能力、延迟成本、状态导出和版本升级影响。没有资源执行所有验证时，标明未验证项，不能用Demo成功覆盖生产承诺。

Escape hatch（逃生口/自定义扩展口）是能否接管关键路径：导出状态、替换工具执行、调整重试、插入权限、读取受控原始响应或导出Trace。迁移时最好保持领域状态、工具契约、验收集和必要事件格式独立，避免整个业务绑死某内部对象。

<details>
<summary>从Codex和Claude源码学习什么，不直接照搬什么</summary>

两份固定源码说明成熟执行系统怎样处理工具、上下文、会话与环境，它们是实现参考，不是供所有应用直接导入的通用框架。可以借鉴工具说明与执行元数据分离、压缩后重建、取消传播等机制；不能拿内部服务名和功能开关当你项目必须部署的架构。

采用SDK、图框架或自研，都应能用本书同一任务契约解释：模型建议什么，程序控制什么，状态怎样恢复，哪些结果仍未知。框架名不是面试答案，选择理由与可验证的边界才是。

</details>

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. Agents SDK、LangGraph、LangChain与自研怎么选？

<details>
<summary>参考答案</summary>

先定义任务状态、控制流、工具、人工参与、恢复和部署要求。Agents SDK以Agent与Runner循环为核心，LangGraph显式管理状态图与检查点，LangChain当前create_agent提供基于LangGraph的高层集成。自研适合范围小或特殊控制，但要承担可靠性。用相同任务和故障验证比较，而不是按热度选。

</details>

### 2. Session、Checkpointer和Store是一回事吗？

<details>
<summary>参考答案</summary>

不是。Session通常管理会话历史；Checkpointer管理定义执行边界的状态快照；Store可用于跨会话数据和记忆。具体以框架语义为准，它们不自动解决外部写操作的恰好一次问题。

</details>

### 3. LangGraph interrupt恢复为什么还要考虑副作用？

<details>
<summary>参考答案</summary>

节点可能从开头重跑，中断前代码可能再执行。检查点恢复图状态不等于回到任意CPU指令，也不回滚外部世界。因此动作要幂等、独立包装或可核对。

</details>

### 4. LangChain和LangGraph应该对立选择吗？

<details>
<summary>参考答案</summary>

不必。当前LangChain create_agent建立在LangGraph运行基础上，提供更高层默认循环和集成；需要复杂状态图时可深入底层。必须说明实际版本和API，不能用旧Chain印象概括现在能力。

</details>

### 5. 怎样避免未来被框架绑定？

<details>
<summary>参考答案</summary>

保持业务状态、工具契约、验收用例和必要事件/产物格式独立，确认能导出状态、替换执行器与重试、接入权限和观测。迁移风险要实际验证，不只相信功能清单。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| 框架越重越Production | 抽象不匹配会增加复杂度。 |
| 自研Loop一定更专业 | 实现与维护可靠性也有成本。 |
| 有Session就是完整业务恢复 | 会话项与执行/副作用状态不同。 |
| LangChain永远只是线性Chain | 当前官方Agent入口基于LangGraph，需按版本说明。 |
| Node/Edge就是Agent的本质 | 它是实现控制流的一种抽象。 |
| 使用产品源码等于集成了产品所有保证 | 部署、配置、任务契约和验证仍由自己的系统负责。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：两个只读工具的小任务一定需要显式状态图吗？

<details>
<summary>查看参考答案</summary>

不一定。若简单Loop更清楚且满足故障承诺，可先用它；复杂度由任务需要而不是教材组件数决定。

</details>

### 自测 2：用了SQLiteSession后邮件会自动不重复吗？

<details>
<summary>查看参考答案</summary>

不能据此保证。会话历史保存不等于邮件API的幂等与结果核对，要检查实际执行恢复窗口。

</details>

### 自测 3：LangGraph Store里有用户偏好，模型会自动知道吗？

<details>
<summary>查看参考答案</summary>

不会仅因存着就知道。节点需读取相关信息并按规则编排入模型输入；Store与Context不是同一个对象。

</details>

### 自测 4：Handoff之后控制权变化和子Agent返回有何不同？

<details>
<summary>查看参考答案</summary>

交接让另一个Agent成为当前处理角色；agents-as-tools把子工作结果返回调用者，父级继续。框架API应准确匹配所需控制语义。

</details>

### 自测 5：选型表看起来全都支持恢复，怎样进一步验证？

<details>
<summary>查看参考答案</summary>

制造中断、部分节点成功、外部成功但回执丢失等具体窗口，观察恢复单位、重复动作和状态导出。功能名相同不代表语义相同。

</details>

### 自测 6：什么情况下不能宣布框架选型完成？

<details>
<summary>查看参考答案</summary>

关键权限、恢复或部署条件尚未验证，或测试只覆盖正常Demo。应列出已证实和待验证要求，而不是把疑问藏在“支持生产”里。

</details>

## 资料与下一步

官方：[Agents SDK Running agents](https://openai.github.io/openai-agents-python/running_agents/)、[Tools](https://openai.github.io/openai-agents-python/tools/)、[Handoffs](https://openai.github.io/openai-agents-python/handoffs/)、[Sessions](https://openai.github.io/openai-agents-python/sessions/)、[Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)、[Tracing](https://openai.github.io/openai-agents-python/tracing/)；[LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)。本章不把官方抽象与自己的选型判断混成官方排名。完成后进入综合复习，用同一个项目说明机制取舍。

本章对应研究能力：`AGENT-036`、`AGENT-047`、`AGENT-048`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](22-ProductionAgentRuntime.md) · [模块目录](../README.md) · [综合复习 →](../review/README.md)
