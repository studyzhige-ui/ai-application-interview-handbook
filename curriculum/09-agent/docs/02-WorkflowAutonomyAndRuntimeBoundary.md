# 02. Workflow、Agent 与自主权：执行角色的边界

“我的流程里用了大模型，所以它就是Agent吗？”

> 先不看框架名字，看中间结果变化时，谁有权决定下一步。

同一个任务可以用固定流程，也可以交给模型动态推进。这一章要学会选择，而不是给技术排高低。

[← 上一章](01-AgentSystemAndResponsibilities.md) · [Agent 目录](../README.md) · [下一章 →](03-AgentLoopAndExecutionScopes.md)

---

<a id="section-1"></a>

## 1. 先讲人话：Agent 化的本质是什么

<a id="legacy-02-01"></a>

先问“中间结果与预想不一样时，谁决定下一步？”程序预先写好分支是流程控制；模型根据新证据选择查询、工具或停止，是把部分决策权交出去。两种控制可以出现在同一个应用里。

不是“用了 LLM”就叫 Agent。

```text
固定 Pipeline
上传 → OCR → Chunk → Embedding → 入库
```

这是 Workflow。

```text
固定 Workflow + LLM 节点
输入 → LLM 分类 → 固定 Branch → 固定动作
```

依然主要是 Workflow。

真正的 Agent 更接近：

```text
Goal
 ↓
Model 根据当前 Context / State 决定下一步
 ↓
Tool / Delegate / Answer
 ↓
Observation
 ↓
再次决定
```

核心差异是：

> **Workflow 的主要控制流由开发者预先编码；Agent 允许模型在运行时根据 Observation（观察结果） 动态决定下一步 Action。**

它不是二元开关，而是一条连续谱：

```text
Deterministic Program
→ Workflow + LLM Node
→ Dynamic Router
→ Agent Loop + Tools
→ Long-running Autonomous Agent
```

---

<a id="section-2"></a>

## 2. 为什么“更 Agent”不等于“更高级”

<a id="legacy-02-02"></a>

把控制权交给模型，会换来动态性，也会引入：

- 非确定性；
- 更高 Token / Latency（时延） / Cost；
- Tool 选择错误；
- Dead Loop / Goal Drift；
- Side Effect 风险；
- 更难测试；
- 更复杂的 Trace（执行追踪） / Eval / Recovery。

因此第一条工程原则是：

> **能用普通程序解决，不先上 Agent；能用固定 Workflow 解决，不先上开放 Loop。**

Anthropic `Building effective agents` 也强调从简单、可组合的模式开始，再按任务需要增加 autonomy。

---

<a id="section-3"></a>

## 3. 什么任务更值得 Agent 化

<a id="legacy-02-03"></a>

一个实用判断矩阵：

| 维度 | Workflow 更合适 | Agent 更合适 |
|---|---|---|
| 控制流 | 稳定、可预定义 | 中间 Observation 决定下一步 |
| 输入 | 结构化 | 非结构化 / 开放 |
| Tool 选择 | 固定 | 动态 |
| 任务 | 短、重复 | 探索、多步、长任务 |
| 错误成本 | 极高且不可容错 | 可隔离、可验证、可回退 |
| 验证 | 单测 / 状态机 | Outcome Eval / Trace / Verification |

例如：

```text
CRUD / 支付主链路
→ Workflow

未知线上故障排查
→ Agent-assisted Investigation

大型仓库 Bug 修复
→ Coding Agent

高风险退款 / 删除
→ Workflow + HITL，不应让 Agent 自由提交副作用
```

| 维度 | 单次模型调用 | 含模型节点的工作流 | 受控 Agent 循环 |
|---|---|---|---|
| 输入与路径 | 输入就绪，一次生成 | 主要阶段预定义 | 路径随观察调整 |
| 适合任务 | 已给材料的摘要、分类 | 固定审核/抽取流水线 | 调查、探索、反复试验 |
| 主要测试对象 | 输出质量与格式 | 节点、分支和整个流程 | 动作选择、工具结果、停止及结果 |
| 新增代价 | 相对有限 | 更多流程状态 | 不确定路径、累积成本与动作风险 |
| 完成依据 | 输出契约 | 流程与结果契约 | 同样需要结果契约，不能只信自评 |

选择方式是先用简单方案建立基线，再看它具体失败在哪里。固定方案找不到未知位置的资料，可能需要动态检索；只是模型漏了一个字段，先改输出校验，不要立刻升级为多 Agent。

---

<a id="section-4"></a>

## 4. Production 往往是 Hybrid

<a id="legacy-02-04"></a>

真实系统通常不是“全 Agent”：

```text
API / Auth / Validation / Transaction
            ↓
     Deterministic Boundary
            ↓
       Agentic Region
   Understand / Search / Plan
            ↓
  High-risk Action Boundary
            ↓
   Approval + Deterministic Commit
```

这意味着 Agent 是系统中的一种执行模式，而不是系统的全部。

---

<a id="section-5"></a>

## 5. 为什么 Model + API 还不够

<a id="legacy-02-05"></a>

假设只有：

```python
# 一次普通模型调用的示意，不等于完整Agent执行系统。
response = llm(prompt)
```

它可以生成文本，但没有稳定机制回答：

```text
这一轮属于哪个 Run？
当前已经完成哪些 Step？
有哪些 Tool 可用？
Tool 参数谁校验？
高风险动作谁授权？
Context 超限怎么办？
任务中途 Crash 怎么恢复？
如何取消正在运行的 Tool？
怎样证明任务完成？
```

这些都不是“模型更聪明”就自动解决的问题。

所以需要 Harness / Runtime（运行时执行系统）。

---

<a id="section-6"></a>

## 6. Harness / Runtime 到底是什么

<a id="legacy-02-06"></a>

Harness与Runtime在Agent文章里经常重叠，**没有全行业统一而互斥的定义**。本书这样使用：Harness强调模型外围的工具、上下文、限制和验证等配套；Runtime强调这些配套运行时怎样推进循环、维护状态、处理事件。二者通常是同一执行系统的两个观察角度，不必硬拆成两个服务。

Orchestrator（编排器）强调任务如何分配与协调；Workflow Engine强调怎样执行预定义流程。Eval Harness则是准备测试环境、运行试验并评分的设施，与被测Agent执行系统不同，第21章具体解释。

---

<a id="section-7"></a>

## 7. Harness、Runtime、Orchestrator、Workflow Engine 怎么区分

<a id="legacy-02-07"></a>

**Runtime（运行时）**回答执行正在怎样发生；**Harness（执行支撑系统）**回答用哪些支撑能力约束并兑现模型行为；**Orchestrator（编排器）**回答步骤、模型或角色之间怎样协调；**Workflow Engine（工作流引擎）**通常提供预定义图或流程的执行、调度和状态能力。

| 概念 | 典型输入和输出 | 不保证的事情 |
|---|---|---|
| Model（模型） | 当前上下文 → 文本或动作候选 | 不自动取得授权，不替程序执行 |
| Orchestrator（编排器） | 当前进展 → 下一节点/角色/停止决策 | 不天然提供数据库、工具隔离 |
| Runtime（运行时） | 执行配置和输入 → 事件、动作结果及终态 | 不替用户决定业务验收标准 |
| Harness（执行支撑系统） | 模型与能力配置 → 可受控完成任务的执行组合 | 名称本身不代表完善或安全 |
| Workflow Engine（工作流引擎） | 图/流程和状态 → 执行推进 | 不保证每个节点都是 Agent |
| Framework（框架） | 开发者配置与扩展代码 → 上述能力的实现 | 不保证业务正确性或供应商兼容 |

一个框架可以同时提供编排和运行能力，一个 Harness 也可以内部使用工作流引擎。因此这些不是必须互斥的六层。不应把产品用词硬改成我们偏好的层次；需要先识别它的实际控制职责。

---

<a id="section-8"></a>

## 8. 三个经常混淆的边界

<a id="legacy-02-08"></a>

### Prompt Engineering

```text
解决：单次 Model Call 如何被指令约束
```

### Context Engineering

```text
解决：这一轮 inference 到底给模型哪些信息
```

### Harness Engineering

```text
解决：跨多轮、多 Tool、多 State 的任务怎样运行
```

因此：

```text
Prompt ⊂ Context
Context 是 Harness 的一个 Plane
Harness 不等于“更长的 Prompt”
```

---

<a id="section-9"></a>

## 9. Agent 化之后立刻新增哪些工程问题

<a id="legacy-02-10"></a>

一旦从：

```text
step1 → step2 → step3
```

变成：

```text
Model → Action → Observation → Model → ...
```

就必须继续回答：

```text
选错 Tool 怎么办？
Schema 错怎么办？
Tool 有副作用怎么办？
Context 膨胀怎么办？
Goal Drift 怎么发现？
中途 Crash 怎么 Resume？
怎样限制权限？
怎样证明 Final Result 真的正确？
```

后续知识板块，本质上都在回答这些问题。

这组问题在后面依次回答：03循环；04–07工具；08–10控制和输入；11–13记忆与恢复；14以后安全、协议、协作与验证。不是要求读者现在自行猜出答案，而是让你知道后续每章打开的是哪个执行责任。

---

<a id="section-10"></a>

## 10. 产品实现与官方资料对照（按需展开）

<details>
<summary>源码证据：为什么成熟产品一定有 Runtime Layer</summary>

<a id="legacy-02-09"></a>

固定 Claude Code 快照中，`QueryEngine` 持有 Conversation / Turn 生命周期，并管理 Tools、Agents、MCP Clients、Permission（权限）、Budget（预算）、Abort、Usage、Memory（记忆） Prompt 与 Compact 相关能力。

固定 Codex 快照中能看到：

- Session / Turn / Step；
- Tool Router（路由器） / Registry（注册表）；
- Sandbox（沙箱） Policy；
- Context Compaction（上下文压缩）；
- Rollout Trace。

这些实现共同说明一个稳定事实：

> **成熟 Agent 产品的复杂度主要来自 Runtime，而不是一次 LLM API 调用。**

注意：这些源码是实现证据，不代表所有产品必须同构。

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[Workflow与Agent的控制方式](https://www.anthropic.com/engineering/building-effective-agents)。

---

<a id="human-a"></a>

## 11. HUMAN-A 信号

当前 Agent Canonical 中：

- `AGENT-001`：Agent vs LLM / Chatbot / Workflow，30 个独立来源；
- `AGENT-002`：Harness / Runtime Boundary，25 个独立来源；
- `AGENT-003`：完整 Agent Loop，36 个独立来源。

真人追问常见方向是：

```text
为什么需要 Agent？
→ Harness 为什么独立？
→ Loop 怎么跑？
→ Tool / Context / Memory 怎么进来？
→ Failure / Evaluation 怎么办？
```

所以本章不是术语前言，而是整个 Agent Runtime 的第一道架构判断题。

---

<a id="interview"></a>

## 12. 面试怎么答

### Q：Workflow与Agent的本质区别是什么？

🎯 **30 秒回答**：

> Workflow 的主要控制流由程序预先定义；Agent 把部分下一步决策交给模型，根据当前 Context、State（状态） 和 Observation 动态选择 Tool 或 Action。Agent 适合步骤无法提前写死、需要探索和多轮环境反馈的任务，但会引入非确定性、成本、安全和恢复问题。Harness / Runtime 就是模型之外负责 Loop、Tool、Context、State、Permission、Recovery 和 Trace 的执行系统，因此 Model + API 本身并不足以构成 Production（生产环境） Agent。

### Q：Runtime 与编排器是同一个东西吗？

🎯 **30 秒回答**：

> 不必相同。编排器关注下一步、依赖和委派，运行时还要兑现调用、管理活动状态和取消等执行语义。框架可能把它们放在同一 Runner 或图引擎里，但这不消除职责差别。Harness 是围绕模型把这些支撑能力组织起来的系统名称，具体边界随产品而异。

### Q：什么时候不该用 Agent？

🎯 **30 秒回答**：

> 输入和路径已经稳定、错误代价高且输出能用固定规则完成时，先用确定性流程或单次模型调用。例如已知三份小资料的摘要不一定需要循环。只有基线暴露了动态调查或反馈决策的必要性，再增加相应能力，并用同一任务集比较收益与额外成本。

### Q：上下文工程和 Harness 工程各解决什么？

🎯 **30 秒回答**：

> 上下文工程决定这一轮模型看见什么，包括指令、历史、证据和工具说明；Harness 工程还负责模型给出候选后如何调用、怎样保存进展、如何限制副作用与恢复。上下文中写“不能修改”是沟通，真正禁止写入必须由工具或底层授权兑现。

### 继续展开时的回答结构

按四层展开：

```text
1. 控制权：Workflow vs Agent
2. 适用场景：动态探索 vs 确定性流程
3. 新成本：Failure / Cost / Security / Eval
4. Harness：把模型决策变成可控 Runtime
```

最后补一句：

> Production 通常是 Hybrid，把不确定性限制在真正需要 Agent 的区域，高风险提交仍由确定性系统和 Approval（批准） 控制。

### 🔍 继续追问与下一步

```text
一个 Agent Loop 到底怎样推进？
Run / Turn / Step 为什么要分层？
Tool Calling 为什么不只是函数调用？
Context 与 Memory 有什么区别？
什么时候需要 Checkpoint？
怎样定义完成条件？
```

这些直接进入下一章。

---

<a id="pitfalls"></a>

## 13. 高频易错点

⚠️ “用了 LLM 就是 Agent”——错。

⚠️ “Agent 一定比 Workflow 高级”——错。

⚠️ “Harness = Prompt Template”——错。

⚠️ “Orchestrator = Agent Runtime 的唯一标准名称”——错，术语需先给工作定义。

⚠️ “模型足够强就不需要 Runtime”——错，副作用、权限、持久化和恢复属于系统问题。

⚠️ **固定流程含一次 LLM 分类就是自主 Agent。** 主要控制路径仍可能完全由程序决定。

⚠️ **Orchestrator、Runtime、Harness 必须是独立服务。** 是职责词，不是强制部署单元。

⚠️ **模型能力强，程序就可以少做权限检查。** 更强推理不建立真实权限。

⚠️ **复杂框架等于生产成熟度。** 要测试任务状态、恢复、可观测性与退出能力，而非只看功能表。

---

<a id="self-test"></a>

## 14. 本章自测

<details><summary>1. 一个固定 DAG 中每个 Node 都调用 LLM，它一定是 Agent 吗？</summary>

不一定。关键不是有没有 LLM，而是谁拥有运行时控制流。如果 Node / Edge 基本由程序预定义，它仍然更接近 LLM-enhanced Workflow。

</details>

<details><summary>2. 为什么支付主链路通常不应该完全 Agent 化？</summary>

因为步骤稳定、错误成本高、事务与权限要求强，确定性状态机更容易验证和约束。可以让 Agent 负责理解、建议或异常诊断，但关键提交应保留确定性边界。

</details>

<details><summary>3. Harness 最核心的一句话定义是什么？</summary>

模型之外、围绕模型建立的执行系统：控制它看见什么、能做什么、怎样循环、怎样失败和恢复，以及怎样被审计与评估。

</details>

<details><summary>4. 审批流程里有20个步骤，它必然是 Agent 吗？</summary>

不是。20步都预先编排依然是工作流。关键在于是否把某段下一步选择交给模型，以及这种选择是否依据中间观察。

</details>

<details><summary>5. 报告总是漏引用，应先加规划器吗？</summary>

先定位缺陷。若资料已齐全，是输出契约或校验问题，就补引用生成与检查；只有证据获取方向需要动态调整时才考虑规划能力。

</details>

<details><summary>6. 允许自主读取，不允许自主提交合理吗？</summary>

合理。权限按动作分配。读取授权清单内资料的风险通常不同于修改原件或发送报告，探索阶段与提交阶段可以采用不同确认要求。

</details>

<details><summary>7. 框架提供 checkpoint，是不是自动保证外部写入不重复？</summary>

不是。框架保存的流程状态与外部系统写入未必原子，仍需业务操作标识、核对和幂等。第13章会用两个检查点之间的故障解释。

</details>

<details><summary>8. 请用一句话分别解释三个 engineering。</summary>

提示词设计改善指令；上下文工程选择当前模型输入；执行支撑工程把模型候选变成受控、可持续的行动。它们互相配合，不是只改名称的同一技能。

</details>

<details><summary>9. 怎样避免自己的工作定义和产品术语冲突？</summary>

先说明项目采用什么定义，再给产品映射。不要拿教材的 Run/Turn 分类替代 Codex 或 SDK 官方对象；名称相近时应核对作用域和生命周期。

</details>

---

[← 上一章](01-AgentSystemAndResponsibilities.md) · [Agent 目录](../README.md) · [下一章 →](03-AgentLoopAndExecutionScopes.md)
