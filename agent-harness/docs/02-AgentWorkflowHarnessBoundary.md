# 02｜Agent vs Workflow，以及 Harness / Runtime / Orchestrator 的边界

> 本章合并旧 `02-AgentVsWorkflow` 与 `03-HarnessRuntimeBoundary`。目标不是背术语，而是先建立 Agent 系统最重要的边界：**什么任务值得把下一步决策交给模型，以及模型之外为什么还必须有 Harness。**

## 1. 先讲人话：Agent 化的本质是什么

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

> **Workflow 的主要控制流由开发者预先编码；Agent 允许模型在运行时根据 Observation 动态决定下一步 Action。**

它不是二元开关，而是一条连续谱：

```text
Deterministic Program
→ Workflow + LLM Node
→ Dynamic Router
→ Agent Loop + Tools
→ Long-running Autonomous Agent
```

## 2. 为什么“更 Agent”不等于“更高级”

把控制权交给模型，会换来动态性，也会引入：

- 非确定性；
- 更高 Token / Latency / Cost；
- Tool 选择错误；
- Dead Loop / Goal Drift；
- Side Effect 风险；
- 更难测试；
- 更复杂的 Trace / Eval / Recovery。

因此第一条工程原则是：

> **能用普通程序解决，不先上 Agent；能用固定 Workflow 解决，不先上开放 Loop。**

Anthropic `Building effective agents` 也强调从简单、可组合的模式开始，再按任务需要增加 autonomy。

## 3. 什么任务更值得 Agent 化

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

## 4. Production 往往是 Hybrid

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

## 5. 为什么 Model + API 还不够

假设只有：

```python
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

所以需要 Harness / Runtime。

## 6. Harness / Runtime 到底是什么

一个稳定抽象：

```text
                    Goal / User
                        │
                        ▼
                Harness / Runtime
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
    Context           State            Policy
       │                │                │
       └─────────┬──────┴──────┬─────────┘
                 ▼             ▼
               Model         Tools
                 │             │
                 └──── Loop ───┘
                        │
                        ▼
               Event / Trace / Eval
```

Model 负责推理与生成候选决策。

Harness 负责：

- Model 看见什么；
- 可以调用什么；
- Tool 如何验证、授权和执行；
- State 怎样变化；
- Loop 何时继续 / 暂停 / 停止；
- Failure 怎样恢复；
- 执行怎样被 Trace 和 Eval。

一句话：

> **Model 提供智能，Harness 把智能约束成可执行、可恢复、可审计的系统。**

## 7. Harness、Runtime、Orchestrator、Workflow Engine 怎么区分

这些词在业界并没有唯一标准，但课程使用下面的工作定义：

### Harness / Runtime

关注 Agent 执行本身：

```text
Loop
Tool Runtime
Context
State
Permission
Cancellation
Checkpoint
Trace
```

### Orchestrator

更强调“谁调用谁、任务怎样编排”：

```text
Agent A
→ Agent B
→ Tool C
→ Human Review
```

Orchestration 可以是 Harness 的一部分，也可以是平台外层。

### Workflow Engine

更强调预定义 State / Node / Edge 与可靠推进：

```text
Node A → Node B → Conditional Node C
```

它可以承载 Agent Step，但不等于 Agent Harness。

## 8. 三个经常混淆的边界

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

## 9. 源码证据：为什么成熟产品一定有 Runtime Layer

固定 Claude Code 快照中，`QueryEngine` 持有 Conversation / Turn 生命周期，并管理 Tools、Agents、MCP Clients、Permission、Budget、Abort、Usage、Memory Prompt 与 Compact 相关能力。

固定 Codex 快照中能看到：

- Session / Turn / Step；
- Tool Router / Registry；
- Sandbox Policy；
- Context Compaction；
- Rollout Trace。

这些实现共同说明一个稳定事实：

> **成熟 Agent 产品的复杂度主要来自 Runtime，而不是一次 LLM API 调用。**

注意：这些源码是实现证据，不代表所有产品必须同构。

## 10. Agent 化之后立刻新增哪些工程问题

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

后续 21 个知识板块，本质上都在回答这些问题。

## 11. HUMAN-A 为什么高频追这个边界

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

## 12. 🎯 30 秒回答

> Workflow 的主要控制流由程序预先定义；Agent 把部分下一步决策交给模型，根据当前 Context、State 和 Observation 动态选择 Tool 或 Action。Agent 适合步骤无法提前写死、需要探索和多轮环境反馈的任务，但会引入非确定性、成本、安全和恢复问题。Harness / Runtime 就是模型之外负责 Loop、Tool、Context、State、Permission、Recovery 和 Trace 的执行系统，因此 Model + API 本身并不足以构成 Production Agent。

## 13. 🎯 2–3 分钟回答框架

按四层展开：

```text
1. 控制权：Workflow vs Agent
2. 适用场景：动态探索 vs 确定性流程
3. 新成本：Failure / Cost / Security / Eval
4. Harness：把模型决策变成可控 Runtime
```

最后补一句：

> Production 通常是 Hybrid，把不确定性限制在真正需要 Agent 的区域，高风险提交仍由确定性系统和 Approval 控制。

## 14. ⚠️ 易错点

- “用了 LLM 就是 Agent”——错。
- “Agent 一定比 Workflow 高级”——错。
- “Harness = Prompt Template”——错。
- “Orchestrator = Agent Runtime 的唯一标准名称”——错，术语需先给工作定义。
- “模型足够强就不需要 Runtime”——错，副作用、权限、持久化和恢复属于系统问题。

## 15. 🔍 面试官继续追问

```text
一个 Agent Loop 到底怎样推进？
Run / Turn / Step 为什么要分层？
Tool Calling 为什么不只是函数调用？
Context 与 Memory 有什么区别？
什么时候需要 Checkpoint？
怎样定义完成条件？
```

这些直接进入下一章。

<details><summary>自测 1：一个固定 DAG 中每个 Node 都调用 LLM，它一定是 Agent 吗？</summary>

不一定。关键不是有没有 LLM，而是谁拥有运行时控制流。如果 Node / Edge 基本由程序预定义，它仍然更接近 LLM-enhanced Workflow。
</details>

<details><summary>自测 2：为什么支付主链路通常不应该完全 Agent 化？</summary>

因为步骤稳定、错误成本高、事务与权限要求强，确定性状态机更容易验证和约束。可以让 Agent 负责理解、建议或异常诊断，但关键提交应保留确定性边界。
</details>

<details><summary>自测 3：Harness 最核心的一句话定义是什么？</summary>

模型之外、围绕模型建立的执行系统：控制它看见什么、能做什么、怎样循环、怎样失败和恢复，以及怎样被审计与评估。
</details>