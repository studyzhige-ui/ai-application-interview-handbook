## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 01. Agent Harness 在 AI 应用中的职责

`AGENT-002` 在冻结 HUMAN-A 中有 **25 个独立来源**，`AGENT-003` 的完整 Agent Loop 有 **36 个独立来源**。这说明企业并不满足于“会调模型 API”，而是在追问：

> **模型之外，到底是谁负责让一个 Agent 安全、连续、可恢复、可评测地完成任务？**

这一章先把整套 Agent Harness / Runtime 课程的总图搭起来。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 1. 先讲人话：Model 很聪明，但它不会替你经营一次“执行”

```text
“阅读这个仓库，找到 Bug，修改代码，运行测试，失败就修，最后给我可交付结果。”
```

```text
理解 Goal
→ 读仓库
→ 决定下一步
→ 调搜索 / 文件 / Shell Tool
→ 接收 Tool Result
→ 更新状态
→ 再次决策
→ 修改文件
→ 跑 Test
→ 失败
→ 判断是否 Retry / 改路
→ 继续
→ 验证 Done
→ 输出结果
```

模型只负责其中一部分：**根据当前上下文做推理和决策。**

这个围绕模型、工具、状态、上下文和执行环境建立起来的系统，就是本课程所说的：

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 2. 一个实用定义

> **Agent Harness / Runtime 是模型之外，负责组织 Context、维护执行 State、驱动 Agent Loop、暴露和执行 Tools、实施 Permission / Sandbox、处理失败与恢复，并记录 Trace / Eval Evidence 的运行时系统。**

```text
                         User / Goal
                              │
                              ▼
                    ┌───────────────────┐
                    │ Agent Harness     │
                    │ / Runtime         │
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼────────────────────┐
          ▼                   ▼                    ▼
       Context              State                Policy
          │                   │                    │
          └──────────┬────────┴──────────┬─────────┘
                     ▼                   ▼
                   Model              Tools
                     │                   │
                     └─────── Loop ──────┘
                              │
                              ▼
                    Event / Trace / Eval
```

```text
Model ≠ Agent Harness
Agent Framework ≠ Agent 本身
Tool Calling ≠ 完整 Agent Runtime
Memory ≠ 所有 State
```

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 3. 为什么“Model + API”还不够

```python
response = client.responses.create(
    model="some-model",
    input=user_input,
)
```

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 3.1 下一步由谁驱动？

```text
我要调用 read_file(path="src/app.py")
```

- 解析这次 Tool Call；
- 找到真实 Tool；
- 校验参数；
- 判断权限；
- 执行；
- 把结果回填给模型；
- 决定是否继续下一轮？

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 3.2 Context 越来越长怎么办？

```text
user message
assistant reasoning / decision
tool call
tool result
new file content
new error log
new test output
...
```

```text
history ↑
context tokens ↑
latency ↑
cost ↑
noise ↑
最终撞 Context Window
```

- Context Assembly；
- Token Budget；
- Tool Result Offloading；
- Compaction；
- Memory Retrieval；
- stale context 控制。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 3.3 Tool 有副作用怎么办？

```text
read_file
vs
rm -rf
vs
send_email
vs
transfer_money
```

```text
Capability Selection
Permission Decision
Human Approval
Sandbox Enforcement
```

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 3.4 中途崩了怎么办？

```text
创建工单成功
↓
Checkpoint 写失败
↓
服务崩溃
↓
Resume 后再次创建工单？
```

- Checkpoint；
- Resume；
- Idempotency；
- Side-effect Ledger；
- Compensation。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 3.5 Agent 说“完成了”，真的完成了吗？

```text
Test Result
Diff
Exit Code
Artifact
Environment Outcome
Trace
Eval
```

这也是为什么 Coding Agent 的质量不能只看最终自然语言回答。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 4. Harness 的八个工程平面

为了后面学习不混乱，可以把 Runtime 拆成八个 Plane。

| Plane | 核心职责 | 典型问题 |
|---|---|---|
| Control Plane | 驱动 Loop / Step / Stop | 下一步是什么？何时停止？ |
| Context Plane | 组装模型本轮看到的信息 | 哪些 history / tool / memory 放进去？ |
| State Plane | 保存当前执行事实 | 任务做到哪？哪些 artifact 已生成？ |
| Capability Plane | 管理 Tool / Skill / MCP / Agent | 当前有哪些能力？怎样发现？ |
| Execution Plane | 真正执行命令 / API / Tool | 在哪里跑？超时怎么办？ |
| Safety Plane | Permission / Approval / Sandbox | 这次动作可不可以做？能碰什么资源？ |
| Coordination Plane | Subagent / Handoff / Ownership | 谁负责哪个子任务？怎样避免冲突？ |
| Observability & Eval Plane | Trace / Replay / Outcome | 为什么失败？真的做对了吗？ |

> Model 更像“决策器”；Harness 更像“操作系统 + 调度器 + 安全层 + 记录系统”的组合。

这不是说 Harness 真的是 OS，而是强调：**它负责把模型决策变成受控执行。**

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 5. 一个最小 Runtime 长什么样

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    messages: list[dict[str, Any]] = field(default_factory=list)
    step: int = 0
    done: bool = False

def run_agent(user_input: str, model, tools: dict[str, callable]):
    state = AgentState(
        messages=[{"role": "user", "content": user_input}]
    )

while not state.done:
        state.step += 1

if state.step > 20:
            raise RuntimeError("max steps exceeded")

response = model.generate(
            messages=state.messages,
            tools=list(tools.keys()),
        )

if response.type == "final":
            state.done = True
            return response.text

if response.type == "tool_call":
            tool = tools[response.name]
            result = tool(**response.arguments)

state.messages.append(response.as_message())
            state.messages.append({
                "role": "tool",
                "tool_call_id": response.call_id,
                "content": str(result),
            })
```

```text
State
Loop
Tool Registry
Tool Dispatch
Result Feedback
Stop Condition
Max Step Guard
```

- schema validation；
- permission；
- sandbox；
- timeout；
- retry；
- cancellation；
- streaming；
- checkpoint；
- context budget；
- compaction；
- trace；
- evaluation；
- idempotency；
- multi-tenant isolation。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 6. Model 和 Harness 到底各负责什么

| 问题 | 更偏 Model | 更偏 Harness |
|---|---:|---:|
| 理解自然语言目标 | ✅ | 提供上下文 |
| 推理下一步行动 | ✅ | 控制可选能力 |
| 生成 Tool Call | ✅ | 校验与执行 |
| Tool 是否有权限执行 | ❌ | ✅ |
| 命令是否在 Sandbox 中 | ❌ | ✅ |
| 保存 Session State | ❌ | ✅ |
| Context 如何裁剪 | 可协助摘要 | ✅ 决定策略 |
| Crash 后如何 Resume | ❌ | ✅ |
| 外部副作用是否重复 | ❌ | ✅ |
| 记录完整 Trace | ❌ | ✅ |
| 判断最终 Outcome | 可参与 Judge | ✅ 组织证据 |

> “Agent 的 Memory、Tool、Loop 都是模型能力。”

> **Tool 能否被调用、如何执行、调用结果如何进入下一轮、失败后怎样恢复，是 Runtime 的实现责任。**

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 7. 成熟产品源码告诉我们的什么

```text
Claude Code
commit = 58231dcce408f805c645cfbc352d2876b517223b

OpenAI Codex
commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 7.1 Claude Code：QueryEngine 明确拥有 Conversation Runtime

固定快照中的 `QueryEngine.ts` 直接写明：

- 一个 conversation 对应一个 `QueryEngine`；
- 每次 `submitMessage()` 开启一个新 turn；
- messages、file cache、usage 等状态跨 turn 保留；
- Runtime 配置中存在 tools、MCP clients、agents、`canUseTool`、`maxTurns`、`maxBudgetUsd`、fallback model 和 `AbortController`。

这说明成熟 Agent 产品不会把“会调用 Tool 的模型”当作全部 Runtime。

它还需要一个长期存在的 conversation execution object。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 7.2 Claude Code：Tool 不是普通函数

`Tool.ts` 中的 Tool Contract 还显式包含：

- input schema；
- permission callback；
- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior()`；
- progress / result；
- context impact。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 7.3 Codex：Context / Session / Tool / Sandbox 都是独立 Runtime 对象

- `Session`、`TurnContext`、`StepContext`；
- `EventMsg`、`TurnItem`；
- Tool router / executor；
- `SandboxPolicy`；
- compaction lifecycle；
- rollout trace。

> **成熟 Agent Runtime 的复杂度来自“执行系统”，而不只是 Prompt。**

> Claude Code / Codex 的具体实现是产品实现证据，不是所有 Agent 必须复制的唯一标准。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 8. 官方资料为什么也强调 Harness，而不是只强调模型

Anthropic 的 `Building effective agents` 把 Workflow 和更自主的 Agent 区分开，并强调从简单、可组合的结构开始，而不是为了“Agent”标签无脑上复杂框架。

OpenAI 的 `A practical guide to building agents` 也把 Agent 看成由 Model、Tools、Instructions / Orchestration 和 Guardrail 等部分共同组成的系统。

Anthropic 后续的 Context Engineering、Long-running Harness、Managed Agents、Containment 等文章进一步把问题推到：

```text
Context
Session
Execution Environment
Safety Boundary
Long-running Progress
Verification
```

这正好和真实面经、Claude Code / Codex 源码形成三侧交叉验证。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: # 9. 一个 AI 应用场景：企业知识库 Agent

```text
“检查最近一周所有高优先级客户工单，找出重复问题，生成修复建议，并为确认的问题创建 Jira。”
```

```text
模型不知道去哪里查工单
模型不能真正创建 Jira
模型无法知道已经创建了哪些 Jira
模型不能保证重复执行不会创建重复工单
```

```text
1. 建立 Run
2. 装载用户 / tenant / permission
3. 暴露 ticket_search / jira_create 等 Tool
4. 组装 Context
5. 调 Model
6. 执行搜索 Tool
7. 记录结果
8. 如果要创建 Jira，触发 Approval
9. 执行有副作用 Tool
10. 记录 idempotency key / external id
11. Checkpoint
12. 验证最终输出
13. 写 Trace / Eval Evidence
```

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## Harness vs 普通 Backend

- DB；
- Cache；
- Queue；
- Retry；
- Auth；
- Observability。

Agent Harness 复用这些基础设施，但它多了一套 Model-in-the-loop 的执行语义：

```text
Model Decision
→ Runtime Action
→ Environment Observation
→ Model 再决策
```

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## Harness vs Agent Framework

LangGraph、OpenAI Agents SDK、Claude Agent SDK 等可以帮助你实现 Runtime Primitive。

```text
Harness Problem
≠ 某一个 Framework API
```

- State；
- Loop；
- Tool；
- Context；
- Permission；
- Checkpoint；
- Trace；

再学框架，你才能判断框架帮你解决了什么、没解决什么。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## Level 1｜30 秒

> Agent Harness / Runtime 是模型之外的执行系统。模型负责理解和决策，Harness 负责把决策变成可控执行，包括 Context Assembly、Agent Loop、Tool Registry/Execution、Session/State、Permission/Sandbox、Checkpoint/Resume、Trace/Eval 等。成熟 Agent 的难点通常不是“会不会调模型”，而是多步任务中的状态、失败、副作用、安全和可验证性。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## Level 2｜2–3 分钟

```text
1. 先区分 Model 和 Runtime
2. 解释一个完整 Loop
3. 说明 Context / State / Tool 三个核心面
4. 补 Failure / Safety / Recovery
5. 用 Claude Code / Codex 或项目例子落地
```

> 模型给出 Tool Call 以后，Runtime 不能直接执行。它需要校验 schema、查 registry、做 permission、必要时 human approval，再在 sandbox 中执行；Tool Result 要进入 event/state，再经过 context budget 组装回下一轮。长任务还要处理 checkpoint、resume 和外部副作用幂等。最终结果不能只看模型说“完成”，还要看 test、artifact、environment outcome 和 trace。

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## Level 3｜继续深挖

- Agent vs Workflow 怎么判断？
- Loop 怎样停止？
- Tool 失败怎样 Repair / Retry？
- Context 爆了怎么 Compact？
- Memory 和 State 有什么区别？
- Checkpoint 后怎样 Resume？
- Permission 和 Sandbox 怎么分？
- Multi-Agent 怎么避免冲突？
- Agent Evaluation 怎么做？

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## Claude Code 源码

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

- `QueryEngine.ts`
- `Tool.ts`
- `Task.ts`
- `query.ts`
- `utils/queryContext.ts`
- `utils/sessionStorage.ts`

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## OpenAI Codex 源码

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

- `codex-rs/core/src/compact.rs`
- `codex-rs/tools/`
- `codex-rs/core/src/tools/router.rs`
- `codex-rs/sandboxing/`
- `codex-rs/rollout-trace/`

## agent-harness/docs/01-AgentHarness在AI应用中的职责.md :: ## 外部权威资料

- Anthropic — Building effective agents  
  https://www.anthropic.com/engineering/building-effective-agents
- OpenAI — A practical guide to building agents  
  https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- Anthropic — Effective context engineering for AI agents  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: # 02｜Agent vs Workflow，以及 Harness / Runtime / Orchestrator 的边界

> 本章合并旧 `02-AgentVsWorkflow` 与 `03-HarnessRuntimeBoundary`。目标不是背术语，而是先建立 Agent 系统最重要的边界：**什么任务值得把下一步决策交给模型，以及模型之外为什么还必须有 Harness。**

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 1. 先讲人话：Agent 化的本质是什么

```text
固定 Pipeline
上传 → OCR → Chunk → Embedding → 入库
```

```text
固定 Workflow + LLM 节点
输入 → LLM 分类 → 固定 Branch → 固定动作
```

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

> **Workflow 的主要控制流由开发者预先编码；Agent 允许模型在运行时根据 Observation 动态决定下一步 Action。**

```text
Deterministic Program
→ Workflow + LLM Node
→ Dynamic Router
→ Agent Loop + Tools
→ Long-running Autonomous Agent
```

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 2. 为什么“更 Agent”不等于“更高级”

- 非确定性；
- 更高 Token / Latency / Cost；
- Tool 选择错误；
- Dead Loop / Goal Drift；
- Side Effect 风险；
- 更难测试；
- 更复杂的 Trace / Eval / Recovery。

> **能用普通程序解决，不先上 Agent；能用固定 Workflow 解决，不先上开放 Loop。**

Anthropic `Building effective agents` 也强调从简单、可组合的模式开始，再按任务需要增加 autonomy。

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 3. 什么任务更值得 Agent 化

| 维度 | Workflow 更合适 | Agent 更合适 |
|---|---|---|
| 控制流 | 稳定、可预定义 | 中间 Observation 决定下一步 |
| 输入 | 结构化 | 非结构化 / 开放 |
| Tool 选择 | 固定 | 动态 |
| 任务 | 短、重复 | 探索、多步、长任务 |
| 错误成本 | 极高且不可容错 | 可隔离、可验证、可回退 |
| 验证 | 单测 / 状态机 | Outcome Eval / Trace / Verification |

未知线上故障排查
→ Agent-assisted Investigation

高风险退款 / 删除
→ Workflow + HITL，不应让 Agent 自由提交副作用
```

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 4. Production 往往是 Hybrid

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

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 5. 为什么 Model + API 还不够

```python
response = llm(prompt)
```

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

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 6. Harness / Runtime 到底是什么

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

- Model 看见什么；
- 可以调用什么；
- Tool 如何验证、授权和执行；
- State 怎样变化；
- Loop 何时继续 / 暂停 / 停止；
- Failure 怎样恢复；
- 执行怎样被 Trace 和 Eval。

> **Model 提供智能，Harness 把智能约束成可执行、可恢复、可审计的系统。**

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 7. Harness、Runtime、Orchestrator、Workflow Engine 怎么区分

这些词在业界并没有唯一标准，但课程使用下面的工作定义：

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ### Harness / Runtime

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

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ### Orchestrator

```text
Agent A
→ Agent B
→ Tool C
→ Human Review
```

Orchestration 可以是 Harness 的一部分，也可以是平台外层。

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ### Workflow Engine

更强调预定义 State / Node / Edge 与可靠推进：

```text
Node A → Node B → Conditional Node C
```

它可以承载 Agent Step，但不等于 Agent Harness。

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ### Prompt Engineering

```text
解决：单次 Model Call 如何被指令约束
```

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ### Context Engineering

```text
解决：这一轮 inference 到底给模型哪些信息
```

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ### Harness Engineering

```text
解决：跨多轮、多 Tool、多 State 的任务怎样运行
```

```text
Prompt ⊂ Context
Context 是 Harness 的一个 Plane
Harness 不等于“更长的 Prompt”
```

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 9. 源码证据：为什么成熟产品一定有 Runtime Layer

固定 Claude Code 快照中，`QueryEngine` 持有 Conversation / Turn 生命周期，并管理 Tools、Agents、MCP Clients、Permission、Budget、Abort、Usage、Memory Prompt 与 Compact 相关能力。

- Session / Turn / Step；
- Tool Router / Registry；
- Sandbox Policy；
- Context Compaction；
- Rollout Trace。

> **成熟 Agent 产品的复杂度主要来自 Runtime，而不是一次 LLM API 调用。**

注意：这些源码是实现证据，不代表所有产品必须同构。

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 10. Agent 化之后立刻新增哪些工程问题

```text
Model → Action → Observation → Model → ...
```

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

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 12. 🎯 30 秒回答

> Workflow 的主要控制流由程序预先定义；Agent 把部分下一步决策交给模型，根据当前 Context、State 和 Observation 动态选择 Tool 或 Action。Agent 适合步骤无法提前写死、需要探索和多轮环境反馈的任务，但会引入非确定性、成本、安全和恢复问题。Harness / Runtime 就是模型之外负责 Loop、Tool、Context、State、Permission、Recovery 和 Trace 的执行系统，因此 Model + API 本身并不足以构成 Production Agent。

## agent-harness/docs/02-AgentWorkflowHarnessBoundary.md :: ## 13. 🎯 2–3 分钟回答框架

```text
1. 控制权：Workflow vs Agent
2. 适用场景：动态探索 vs 确定性流程
3. 新成本：Failure / Cost / Security / Eval
4. Harness：把模型决策变成可控 Runtime
```

> Production 通常是 Hybrid，把不确定性限制在真正需要 Agent 的区域，高风险提交仍由确定性系统和 Approval 控制。

## agent-harness/docs/03-AgentLoopRuntimeState.md :: # 03｜Agent Loop、Run / Turn / Step 与 Runtime Event Model

> 本章合并旧 `04-MinimalAgentLoop`、`05-RunTurnStep`、`06-RuntimeMessageEvent`。它们不是三个孤立知识点，而是同一个问题的三层视角：**Agent 怎样在时间上推进一次任务。**

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 1. 先讲人话：Agent 的核心不是“会调用 Tool”，而是会循环推进任务

```text
Goal / User Input
      ↓
Build Context
      ↓
Model Decision
      ↓
┌───────────────┬─────────────────┐
│ Final Answer  │ Tool / Delegate │
└──────┬────────┴────────┬────────┘
       │                 ↓
       │             Execute
       │                 ↓
       │            Observation
       │                 ↓
       └──────────── Continue Loop
```

普通 LLM Call 到 `Model Output` 就结束；Agent Runtime 还要解释：

```text
输出是不是 Tool Call？
要不要执行？
执行结果如何变成下一轮 Observation？
State 怎样更新？
什么时候结束？
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 2. 一个最小可运行的 Agent Loop

```python
async def run_agent(goal, runtime):
    state = runtime.start(goal)

while True:
        context = runtime.build_context(state)
        decision = await runtime.call_model(context)

if decision.type == "final":
            return runtime.finish(state, decision)

if decision.type == "tool_call":
            result = await runtime.execute_tool(decision, state)
            runtime.record_observation(state, decision, result)
            continue

raise RuntimeError("unsupported model decision")
```

这段代码只展示骨架。Production 版本还需要：

- max step / budget；
- permission；
- cancellation；
- tool failure；
- context compaction；
- checkpoint；
- trace；
- model / provider fallback。

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 3. 为什么要分 Run / Turn / Step

如果所有执行都叫 `session` 或 `message`，后面几乎无法精确表达状态。

```text
Session / Thread
└─ Run
   ├─ Turn 1
   │  ├─ Step A: model request
   │  ├─ Step B: tool call
   │  └─ Step C: observation
   └─ Turn 2
      └─ ...
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ### Run

```text
run_id
status
started_at
ended_at
goal
budget
current_state
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ### Step

```text
model call
tool call
state transition
checkpoint
human approval
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 4. 为什么这个分层对 Failure 很重要

```text
Run = 修复 issue #123
Turn = 用户说“继续”
Step = run_tests
```

```text
Step Failure
→ retry / repair / alternate tool
→ continue same Run
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 8. State Machine：Loop 不只是 while True

```text
CREATED
  ↓
RUNNING
  ├─→ WAITING_TOOL
  ├─→ WAITING_APPROVAL
  ├─→ PAUSED
  └─→ RUNNING
        ↓
   COMPLETED / FAILED / CANCELLED
```

```text
允许哪些 Transition？
Crash 后在哪恢复？
取消时清理什么？
Approval 后回到哪里？
```

如果没有明确状态机，长任务常出现“数据库里 status 是 running，但 worker 已经死了”这类幽灵状态。

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 9. Runtime State 应该有什么

```python
from dataclasses import dataclass, field

@dataclass
class RunState:
    run_id: str
    goal: str
    status: str = "running"
    step_count: int = 0
    last_tool_call_id: str | None = None
    artifacts: list[str] = field(default_factory=list)
    unresolved_errors: list[str] = field(default_factory=list)
```

> **现在执行到哪里、已经发生了什么、接下来还能做什么。**

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 10. 新用户指令怎样进入正在运行的 Agent

这是 `AGENT-042 Dynamic Instruction / Steering` 的核心。

```text
用户追加一句话
→ 直接塞到当前 Model Call 尾部
→ 希望模型自己理解优先级
```

```text
New User Instruction
→ Runtime Event
→ 判断当前 Step 是否可中断
→ 更新 Goal / Constraint Snapshot
→ 取消或完成当前 Tool
→ 下一 Planning Boundary 生效
```

> 新指令不仅是 Message，也是 State Transition 输入。

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 11. 源码证据：Claude Code

- 一个 conversation 拥有 query lifecycle / session state；
- 每次 `submitMessage()` 开启新的 turn；
- messages、file cache、usage 等跨 turn 保留；
- 配置显式存在 `maxTurns`、`maxBudgetUsd`、`abortController`、tools、agents 与 permission callback。

```text
Conversation Runtime
= Turn Lifecycle
+ Persistent State
+ Capability Set
+ Budget
+ Cancellation
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 12. 源码证据：Codex

固定 Codex 快照中，Context Compaction 相关代码直接引用：

```text
Session
StepContext
TurnContext
WorldState
EventMsg
```

Tool Router 中 `ToolCall` 也携带 `call_id`，再构造带 Session / StepContext / CancellationToken 的 Invocation。

```text
长期 Session
→ 当前 Turn
→ 当前 Step / Invocation
→ Event / Tool Call
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 13. Loop 什么时候继续，什么时候停止

```text
Model Final Answer
→ 可能停止

Recoverable Failure
→ 修复 / 重试 / 换路后继续

Human Approval Required
→ Pause

“可能停止”是因为 Final Answer 本身还可能需要 Outcome Verification。

```text
tests_passed?
diff_exists?
requested_file_changed?
acceptance_criteria_met?
```

## agent-harness/docs/03-AgentLoopRuntimeState.md :: ## 15. 🎯 30 秒回答

> Agent Loop 是 Goal 驱动的多步控制循环：Runtime 组装 Context，请模型决定 Final Answer、Tool 或 Delegate，执行动作后把 Observation 和 State Transition 记录下来，再进入下一轮。Production 里还要把 Session、Run、Turn、Step 分层，并用结构化 Event 和 correlation id 表达 Tool、Approval、Checkpoint、Cancel 等事实，这样才能做恢复、Trace 和 Eval。

## agent-harness/docs/04-ToolContractSchemaValidation.md :: # 04｜Tool Contract、Schema 与 Validation

> 本章合并旧 `07-ToolContract` 与 `08-ToolSchemaValidation`。Tool 在 Production Agent 中不是一个普通函数，而是**模型与真实世界之间的协议边界**。

## agent-harness/docs/04-ToolContractSchemaValidation.md :: ## 10. 源码证据：Claude Code

固定快照的 `Tool.ts` 显示 Tool Contract 不只包含 Schema 和 `call()`，还包含：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior()`；
- Permission Context；
- Progress Callback；
- Result / Context Modifier；
- Tool Result Budget / Dynamic Discovery 相关状态。

> Production Tool 是 Runtime Contract，不是 Function Signature。

## agent-harness/docs/04-ToolContractSchemaValidation.md :: ## 11. 源码证据：Codex

固定 Codex 快照中的 `ToolExecutor` 把：

```text
tool_name
spec
exposure
search_info
supports_parallel_tool_calls
handle(invocation)
```

- model-facing response；
- logging projection；
- host-only metadata；
- external context 标记；

这说明 Tool Input / Output 都应被 Runtime 当成正式协议对象。

## agent-harness/docs/04-ToolContractSchemaValidation.md :: ## 14. 🎯 30 秒回答

> Production Tool 不只是一个函数。它应该有稳定的 name/description、输入 Schema、Runtime Validation、side-effect 和 concurrency metadata、permission/cancellation 语义以及结构化 Result Contract。模型生成的参数永远是不可信输入，必须经过 parse、schema、semantic 和 policy 校验；错误可以结构化反馈给模型做有限 Repair，但不能无限重试。

## agent-harness/docs/05-ToolRegistryRouterDiscovery.md :: # 05｜Tool Registry、Router 与 Progressive Discovery

> 本章把旧 `09-ToolRegistryRouter` 与旧 `33-ToolDiscovery` 合并。它们本来就是同一个能力规模化问题：**Runtime 有越来越多 Tool 后，怎样管理、暴露、发现和路由，而不是把所有 Schema 永久塞给模型。**

## agent-harness/docs/05-ToolRegistryRouterDiscovery.md :: ## 10. 源码证据：Codex

- full registry；
- `model_visible_specs`；
- deferred tool search；
- namespace；
- code-mode tool identity。

```text
Direct
Deferred
DeferredModelOnly
DirectModelOnly
CodeModeOnly
Hidden
```

## agent-harness/docs/05-ToolRegistryRouterDiscovery.md :: ## 11. 源码证据：Claude Code

固定快照的 `Tool.ts` 中存在 `searchHint`，`ToolUseContext` 还包含 dynamic skill discovery / discovered skill names 等状态。

这与 HUMAN-A 中“Tool/Skill > 100 后如何按需发现”高度呼应。

## agent-harness/docs/05-ToolRegistryRouterDiscovery.md :: ## 14. 🎯 30 秒回答

> Tool Registry 是完整能力目录，当前 Model-visible Tool Set 只是它经过 tenant、policy、task 和 discovery 筛选后的一个视图。Tool 数量大时不应该把所有 Schema 一次塞入 Context，而应通过 namespace、intent/rule、semantic tool search 或混合路由做 Progressive Discovery，再把少量候选 Tool 暴露给模型。Router 负责把模型 Tool Call 解析到具体 runtime handler，并做版本、exposure 和 policy 检查。

## agent-harness/docs/06-ToolExecutionFailure.md :: # 06｜Tool Execution、Result 与 Failure Semantics

> 本章合并旧 `10-ToolExecutionResult` 与 `11-ToolFailureTimeoutRetry`。Tool Call 真正困难的地方不是“调到函数”，而是**Runtime 怎样把一次调用从请求推进到可解释结果，并正确区分可修复失败、可重试失败和致命失败。**

## agent-harness/docs/06-ToolExecutionFailure.md :: ## 12. 源码证据：Codex

- `ToolRouter` 把 `ResponseItem` 规范化成带 `tool_name / call_id / payload` 的 `ToolCall`；
- `ToolRegistry` 负责 dispatch；
- `CoreToolRuntime` / `ToolExecutor` 提供统一执行接口；
- `FunctionCallError` 至少区分 `RespondToModel` 与 `Fatal`；
- Registry 执行链有 pre/post tool hooks、telemetry、tool lifecycle notification；
- `ToolOutput` 区分 log representation、model-facing response 与 host metadata。

> Tool Execution 是一个 Runtime Transaction，而不是函数调用语法糖。

## agent-harness/docs/06-ToolExecutionFailure.md :: ## 14. 🎯 30 秒回答

> 一次 Tool Call 应被 Runtime 当成完整 Invocation：解析、路由、参数校验、授权、执行、结果校验、Trace，再把规范化 Observation 回填给模型。失败要分类，Invalid Arguments 更适合 Repair，临时依赖故障才可能 Retry；涉及副作用时必须先判断幂等、执行是否已开始以及结果是否只是丢失，不能见异常就盲重试。

## agent-harness/docs/07-ToolSideEffectCancellation.md :: # 07｜Tool Side Effect、Concurrency、Cancellation 与 Progress

> 本章合并旧 `12-ToolSideEffectConcurrency` 与 `13-ToolCancellationProgress`。它们本来属于同一个执行控制问题：**Tool 在真实世界里会占资源、产生副作用、彼此冲突，还可能需要中途取消。**

## agent-harness/docs/07-ToolSideEffectCancellation.md :: ## 10. 源码证据：Claude Code

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior(): cancel | block`；
- progress callback。

`utils/abortController.ts` 还实现 Parent → Child AbortController 传播，并处理 listener 清理。

> Concurrency / Cancellation 属于 Tool Runtime Contract，而不是 UI 细节。

## agent-harness/docs/07-ToolSideEffectCancellation.md :: ## 11. 源码证据：Codex

固定快照的 `ToolRouter` / Invocation 会携带 `CancellationToken`，Registry 还能查询 Tool 是否支持 parallel calls。

```text
Tool Scheduler
需要知道 parallel capability + cancellation token
```

## agent-harness/docs/07-ToolSideEffectCancellation.md :: ## 14. 🎯 30 秒回答

> Tool Runtime 要显式管理副作用、并发和取消。并发不能只看 Tool Name，而应看 read/write semantics 和资源冲突；用户取消要从 Run 向 Tool、Subprocess、Subagent 传播，但副作用进入提交阶段后可能无法真正撤销，需要记录 unknown outcome 并做 reconcile。长 Tool 还应该产生结构化 progress，UI/Trace 和 Model Context 可以使用不同 projection。

## agent-harness/docs/08-PlanningGoalStopBudget.md :: # 08. Planning / ReAct、Goal Control、Stop Condition 与 Budget

Agent 能调用 Tool 以后，很快就会遇到第二个问题：

> **它下一步应该做什么？什么时候应该继续，什么时候必须停？**

这一章把 Planning、ReAct、Goal Control、Stop Condition 和 Budget 放在同一个知识小板块，是因为它们共同解决一个问题：

> **怎样让 Agent 的控制循环朝目标推进，而不是无限行动、来回震荡或偏离任务。**

## agent-harness/docs/08-PlanningGoalStopBudget.md :: ### Claude Code 固定源码快照

```text
maxTurns
maxBudgetUsd
fallbackModel
abortController
```

这支持“控制循环 + Budget + Cancellation 是 Harness 一级能力”的实现事实。

## agent-harness/docs/08-PlanningGoalStopBudget.md :: ### Tier C

- ReAct 原始论文：Reason/Act/Observation 交替；
- Anthropic `Building effective agents`：区分 workflow 与 agent，并强调从简单可组合模式开始。

这些证据用于课程设计，不改变 HUMAN-A Source Count。

## agent-harness/docs/08-PlanningGoalStopBudget.md :: ## Q：Agent 怎样避免无限循环？

> 我不会只放一个 `max_steps`。Runtime 会同时维护明确 Goal 和 Acceptance Criteria，并设置 turn、tool、time、cost、retry 等硬预算；运行中记录最近动作、错误和状态变化，如果发现相同 Tool+Arguments 或同类错误反复出现但状态没有推进，就触发 loop detection，让模型 replan、向用户求助或停止。这样既有硬上限，也有 no-progress 的软检测。

## agent-harness/docs/08-PlanningGoalStopBudget.md :: ## Q：ReAct 和 Plan-Execute-Replan 怎么选？

> ReAct 更适合下一步高度依赖环境 Observation 的任务；Plan-Execute-Replan 更适合有明显阶段、需要进度跟踪的长任务，但计划必须允许根据新状态重规划，而不是一次生成后机械执行。

## agent-harness/docs/09-ContextAssemblyBudget.md :: # 09. Context Assembly、Budget、Cache 与 Tool Result Offloading

Agent Runtime 每次调用模型前都要回答一个问题：

```text
System Prompt
+ 全部 Chat History
```

- Context Window 爆满；
- 旧信息污染当前任务；
- Tool Result 巨大；
- 权限和 Tenant 信息混入错误请求；
- Prompt Cache 命中率差；
- Context 成本不可控；
- 同一事实被重复注入。

所以成熟 Harness 的 Context 不是“聊天记录”，而是：

> **Runtime 为当前 Model Call 编译出来的一次性输入视图。**

## agent-harness/docs/09-ContextAssemblyBudget.md :: ## 1. Context、Memory、State、History 先分清

```text
Context
= 当前这一次模型调用真正看见的内容

History
= 已经发生过的 message / event 记录
```

```text
History 很长
≠ Context 必须全部包含 History

State 持久化
≠ 全部 State 都应该变成自然语言 Prompt
```

```text
从多种来源中选择
→ 排序
→ 去重
→ 裁剪
→ 编译成模型可消费输入
```

## agent-harness/docs/09-ContextAssemblyBudget.md :: # 6. Claude Code 源码提供了什么实现证据

固定源码索引里，`QueryEngine.ts` 会加载：

- memory prompt；
- session storage；
- system prompt parts；
- file history；
- plugin / skill 相关状态；
- compact / snip 相关能力。

```text
loadedNestedMemoryPaths
tool-result budget
content replacement state
dynamic skill discovery
permission decision
```

```text
Context
≠ transcript concatenation

Context
= selected runtime projection
```

这里我们只引用索引已核验的源码事实，不把 Claude Code 的具体排序当成所有 Agent 的通用标准。

## agent-harness/docs/09-ContextAssemblyBudget.md :: # 10. Context Pollution / Stale Context

```text
早期 Plan: 修改 A.py
后面已经决定改 B.py

但旧 Plan 仍然在 Context 中高优先级出现
→ 模型反复回到 A.py
```

```text
旧 permission
旧 file content
旧 dependency version
旧 tool result
```

```text
Source?
Version?
Freshness?
Still relevant?
```

## agent-harness/docs/09-ContextAssemblyBudget.md :: ## Q：Agent Context 应该怎么组装？

> 我会把 Context 当成 Runtime 为当前 model call 编译出来的 view，而不是把全部聊天历史拼进去。来源通常包括 system/runtime instruction、当前目标与约束、最近 history、相关 memory/RAG、tool schema 和最新 tool result。每类来源设置优先级和 token budget，并记录 source/version/freshness；大 Tool Result 外部化成 artifact，只把摘要和引用放进 Context。这样 Context Assembly 才能做去重、过期控制、缓存和后续 compaction。

## agent-harness/docs/09-ContextAssemblyBudget.md :: ## Q：Tool Result 太大怎么办？

> 不优先做不可逆截断，而是完整结果持久化到 artifact store，在 Context 里保留摘要、metadata、引用和少量相关片段，后续需要时再按范围或检索 rehydrate。

## agent-harness/docs/10-ContextCompactionCorrectness.md :: # 10. Context Compaction、Correctness 与 Stale Context

`AGENT-009 Context Compaction` 是整个 Agent 真人面经里最强的信号之一。

> **当 Context 接近预算上限时，Runtime 怎样压缩历史，同时保证当前任务仍然能正确继续？**

成熟 Compaction 更接近一次 Runtime Transaction，而不是一次普通 Summary。

## agent-harness/docs/10-ContextCompactionCorrectness.md :: # 3. Codex `compact.rs` 给出的实现证据

固定源码索引已经核验 `codex-rs/core/src/compact.rs` 存在：

- manual / auto compaction；
- pre-turn / mid-turn / standalone phase；
- pre / post compact hooks；
- context-window-exceeded 处理；
- replacement history；
- compact metadata / window id；
- token usage recomputation；
- compaction analytics；
- compact 后长线程准确率风险 warning；
- live / persisted history 一致性相关逻辑。

这说明 Compaction 在成熟 Runtime 里并不是：

```text
history = summarize(history)
```

而是一个有阶段、有持久化、有可观测性、有恢复语义的状态转换。

这里我们只使用索引已经确认的事实，不推断未读取到的具体算法细节。

## agent-harness/docs/10-ContextCompactionCorrectness.md :: # 4. Claude Code 侧提供了什么证据

固定索引确认 Claude Code Runtime 存在：

```text
services/compact/*
snipCompact
snipProjection
CompactProgressEvent
memory re-injection
tool-result content replacement state
```

> **Context Compression 需要和 Projection、Memory、Tool Result Budget 共同设计。**

不是简单在 History 末尾追加一段“之前对话摘要”。

## agent-harness/docs/10-ContextCompactionCorrectness.md :: ## Q：Agent Context 快满了怎么办？

> 我不会简单删除最老消息。先把大 Tool Result 外部化，再按 Context Source 做预算；需要 compaction 时，把它当成一次 Runtime State Transition：选择需要压缩的 history，生成 summary / projection，同时强制保留 goal、constraints、progress、side-effect ledger 和 artifact refs，构造 replacement history，持久化并重新计算 token usage。压缩后要做 invariant 检查和长任务 regression，避免 summary 错误导致后续重复执行或 goal drift。

## agent-harness/docs/10-ContextCompactionCorrectness.md :: ## Q：怎样验证 Compaction 没丢信息？

> 结构化验证必保字段，再用 continuation test 和长任务 eval 比较压缩前后的 task success、constraint violation、re-execution 和 cost，而不是只看 summary 读起来是否通顺。

## agent-harness/docs/11-MemoryArchitectureLifecycle.md :: # 11. Memory Architecture、Lifecycle 与 Correctness

Agent 一旦跨多轮、多任务运行，就会遇到一个经典问题：

> **哪些信息应该被“记住”，记多久，什么时候再取回来？**

那还没有真正进入 Agent Memory Engineering。

```text
什么值得写？
写成什么形式？
什么时候召回？
怎样更新？
什么时候过期？
错误 Memory 怎么纠正？
```

## agent-harness/docs/11-MemoryArchitectureLifecycle.md :: # 12. Claude Code 固定源码侧的证据

Claude Code Source Index 已确认：

- `QueryEngine` 会加载 `memdir/memdir.ts` 的 memory prompt；
- Tool context 维护 `loadedNestedMemoryPaths`，避免 nested memory 重复注入；
- session / context / memory 是不同 Runtime 路径。

> **Memory 是 Context Source，但不等于整个 Context。**

索引还明确建议后续阅读 `memdir/*` 继续研究具体生命周期；因此本章不会凭空宣称 Claude Code 的具体写入算法。

## agent-harness/docs/11-MemoryArchitectureLifecycle.md :: ## Q：Agent Memory 怎么设计？

> 我会先把 Memory 和 Context、State、History 分开。Memory 不是全量聊天记录，而是经过 write policy 选出的、未来有价值的信息。写入时做 extraction、去重、来源和版本记录；使用时按当前任务 retrieval-on-demand；长期还要支持 consolidation、TTL、supersede、conflict 和人工 correction。高风险事实不能只信 Memory，要能回 Source of Truth 验证。多用户场景还要在存储与查询层绑定 tenant/user/workspace 隔离。

## agent-harness/docs/11-MemoryArchitectureLifecycle.md :: ## Q：Memory 错了怎么办？

> Memory Record 要有 source、version、confidence、validity 和 superseded-by 之类元数据；发生冲突时按来源权威性和版本验证，必要时查询 Source of Truth 或让用户确认，并把旧 Memory 显式失效，而不是只在 Prompt 里追加一句“忽略之前的内容”。

## agent-harness/docs/12-SessionStatePersistence.md :: # 12. Session、State、History、Persistence 与 Tenant Isolation

Agent 系统一旦不再是“一次请求、一次回答”，就必须明确：

> **一次会话到底是什么？哪些状态跨 Turn 保存？哪些只是临时 Context？多用户之间怎样隔离？**

```text
conversation_id -> Redis
```

这一章的目标是建立 Runtime State Plane 的最小模型。

## agent-harness/docs/12-SessionStatePersistence.md :: ## 1. Session 是什么

```text
session_id
user / tenant / workspace identity
created_at
last_active_at
runtime config snapshot
history / event reference
current run state
memory namespace
permission context
```

Session 不等于一条聊天记录，也不等于一个 HTTP connection。

## agent-harness/docs/12-SessionStatePersistence.md :: # 2. Run / Turn / Step 再复习

```text
Session
└─ Run
   └─ Turn
      └─ Step / Model / Tool Interaction
```

不同产品具体命名会不同，但课程需要保持“层级事实”。

Claude Code Source Index 明确说明：

- 一个 conversation 一个 `QueryEngine`；
- `submitMessage()` 开启新 turn；
- messages、file cache、usage 等状态跨 turn 保留。

```text
Session
└─ Turn
   └─ Step / Model Request / Tool Interaction
```

这说明“Session / Turn / Step”不是纯教学想象，而是成熟 Runtime 中真实存在的状态层级。

## agent-harness/docs/12-SessionStatePersistence.md :: ## Q：Agent Session / State 怎么设计？

> 我会把 Session 当作一段连续交互的 Runtime 容器，而不是聊天文本。State 保存当前 goal、status、budget、active tool、progress、workspace 和 permission 等执行事实；History 用结构化 event 记录已发生事情；Context 是从这些持久状态和其它来源编译出来的 model view。多实例场景要支持 durable persistence、版本控制和 cold resume，多租户要让 tenant/workspace identity 贯穿存储 key、query、tool permission、artifact 和 trace，而不是只靠 Prompt 隔离。

## agent-harness/docs/13-CheckpointResumeReliability.md :: # 13. Checkpoint / Resume / Fork / Replay 与 Long-running Reliability

如果 Agent 已经运行 40 分钟、修改了 12 个文件、执行了 3 个外部 Tool，并且刚完成一半：

> **服务崩溃后还能不能继续？继续时会不会重复执行副作用？**

这就是 Checkpoint / Resume / Long-running Reliability 要解决的问题。

## agent-harness/docs/13-CheckpointResumeReliability.md :: ## Q：Agent Checkpoint 应该保存什么？

> 不能只存聊天历史。至少要能恢复 run identity、当前 step、goal/plan、pending work、artifact refs、tool correlation、side-effect ledger、approval、budget 和版本信息。Resume 时先 reconcile 不确定副作用，再重建 context 和执行环境，从 safe point 继续。对于支付、发消息这类外部副作用，要结合 idempotency key、external reference 或 compensation，避免 Tool 成功但 checkpoint 失败后重复执行。

## agent-harness/docs/13-CheckpointResumeReliability.md :: ## Q：Tool 成功但服务崩了，怎么避免重试两次？

> Runtime 要有 operation id / idempotency key 或 side-effect ledger。恢复后先向下游 reconcile；确认已成功则把状态补齐，不再执行。没有幂等能力的动作要设计 compensation 或人工确认，不能只靠“重试次数”。

## agent-harness/docs/14-PermissionApprovalSandbox.md :: # 14. Permission、Approval、HITL 与 Sandbox

```text
改文件
执行代码
发网络请求
写数据库
发送消息
调用付款
操作生产环境
```

> **Runtime 怎样限制它真正能做什么？哪些动作必须人工确认？即使模型越权，执行环境能否阻止？**

```text
Policy
Approval
Sandbox
```

## agent-harness/docs/14-PermissionApprovalSandbox.md :: ## Q：Permission、Approval、Sandbox 有什么区别？

> Permission/Policy 决定规则上某类动作是否允许；Approval/HITL 决定这一次敏感动作是否需要人工确认；Sandbox 是执行层的物理隔离，即使模型或策略层出错，也限制文件、网络、进程能触及的范围。生产 Agent 应把三层组合起来，而不是用弹窗替代 Sandbox，或靠 System Prompt 替代 Permission。

## agent-harness/docs/14-PermissionApprovalSandbox.md :: ## Q：审批为什么要持久化？

> 因为审批可能跨分钟甚至小时，Worker 会重启或迁移。Runtime 应把待审批 Tool Call 和完整 RunState 持久化，审批决定要绑定 Tool 参数和 policy version，之后从 checkpoint resume，而不是让一个进程内 coroutine 一直等待。

## agent-harness/docs/15-GuardrailsInjectionContainment.md :: # 15. Guardrails、Prompt Injection、Secrets 与 Containment

> “我在 System Prompt 里写了不要泄露秘密，所以安全。”

Production Agent 会接收大量**不可信输入**：

```text
用户输入
网页
PDF
邮件
代码仓库
Issue / PR
MCP Resource
Tool Result
外部 API Response
```

因此 Prompt Injection 不是单纯 Prompt 问题，而是：

> **不可信数据进入有执行能力的 Runtime 后，如何阻止它获得更高权限。**

## agent-harness/docs/15-GuardrailsInjectionContainment.md :: ### Anthropic — Beyond permission prompts

```text
Permission prompt
≠ Sandbox
```

Filesystem / Network isolation 可以降低不必要审批，同时控制 blast radius。

## agent-harness/docs/15-GuardrailsInjectionContainment.md :: ### OpenAI Agents SDK — Guardrails

课程使用：Input / Output / Tool Guardrail 是不同生命周期边界。

## agent-harness/docs/15-GuardrailsInjectionContainment.md :: ## Q：Agent 如何防 Prompt Injection？

> 我不会把它当成 Prompt 文案问题。首先区分 instruction 和 untrusted external data，并保留来源与 trust metadata；高风险 Tool 通过 schema validation、permission 和 HITL；执行环境再用 filesystem/network sandbox 和 least privilege 限制 blast radius；secret 不直接进入模型 context，而通过受控 Tool/credential broker 使用；输出侧再做 secret/PII redaction。这样即使 injection 检测漏掉，也不至于直接越权执行或数据外泄。

## agent-harness/docs/16-MCPSkillsHooks.md :: # 16. MCP、Skills、Hooks 与 Capability Extension

> **能力从哪里来？怎样发现？怎样按需加载？怎样扩展 Runtime，又不把所有东西都塞进 Context？**

```text
Tool
MCP
Skill
Hook
Plugin
Prompt / Rule
```

这一章把它们放在同一个知识小板块，是因为它们共同解决：

> **Agent Runtime 怎样获得、发现、加载和扩展能力。**

## agent-harness/docs/16-MCPSkillsHooks.md :: # 2. 为什么 Tool 太多会出问题

```text
name
description
JSON schema
examples
```

```text
Token Cost ↑
Tool Selection Confusion ↑
Prompt Cache Stability ↓
Latency ↑
```

因此 Capability Discovery 本身应该成为 Runtime 能力。

HUMAN-A `AGENT-021` 有 20 个独立来源，直接追问 Dynamic Discovery / Progressive Loading。

## agent-harness/docs/16-MCPSkillsHooks.md :: # 3. Capability Catalog

```python
CapabilitySummary(
    id="github.search_code",
    kind="tool",
    short_description="Search code in a repository",
    tags=["code", "search", "github"],
    risk="read_only",
    load_key="github-tool-pack",
)
```

```text
select capability
→ load full schema / skill instructions
→ invoke
```

这就是 Progressive Disclosure。

## agent-harness/docs/16-MCPSkillsHooks.md :: # 4. Claude Code 源码侧的 Progressive Loading 证据

固定 Source Index 已确认 `ToolUseContext` 中存在：

```text
dynamicSkillDirTriggers
discoveredSkillNames
```

```text
Capability Catalog
→ Discovery
→ Selection
→ Progressive Loading
→ Invocation
```

```text
All Tool Schemas
→ Every Context
```

## agent-harness/docs/16-MCPSkillsHooks.md :: # 11. Codex Hooks 的实现证据

- `codex-rs/hooks/src/engine/mod.rs`；
- `codex-rs/config/src/hook_config.rs`；
- Hook handler 可以包括 command、MCP tool、prompt、agent；
- compaction 存在 pre/post hook。

```text
Core Runtime
→ Lifecycle Event
→ Hook Policy
→ Extension Handler
```

Hook 是横切扩展点，不应该反过来定义整个 Runtime 生命周期。

## agent-harness/docs/16-MCPSkillsHooks.md :: ## Q：Tool、MCP、Skill、Hook 有什么区别？

> Tool 是一次可执行能力；MCP 是 Host/Client/Server 之间标准化暴露 Tool、Resource、Prompt 等能力的协议；Skill 更像可发现、按需加载的程序性知识/资源包，通常会组织多个 Tool 完成一种任务；Hook 是 Runtime 生命周期扩展点，用于审计、验证或扩展。它们不是同一层抽象，也不能全部叫插件。

## agent-harness/docs/16-MCPSkillsHooks.md :: ## Q：Tool 太多怎么处理？

> 不把所有完整 schema 永久塞进 Context，而是建立 capability catalog，让模型先看到轻量 summary，通过 intent/search 发现候选，再按需加载完整 Tool/Skill 定义，并用 eval 验证 discovery recall 和 tool selection accuracy。

## agent-harness/docs/17-RoutingProviderResilience.md :: # 17. Intent / Model Routing、Provider Adapter 与 Runtime Resilience

```text
所有请求
→ 同一个模型
→ 同一个 Tool Set
```

```text
这是哪类任务？
需要哪种能力？
应该用哪个模型 / Provider？
失败后能不能换模型？
Tool Protocol 不一样怎么办？
```

这一章把 Intent Routing、Model Routing、Provider Adapter 和 Resilience 放在一起，是因为它们共同决定：

> **一次 Agent Run 选择哪条执行路径，并在模型/Provider 失败时怎样保持语义一致。**

## agent-harness/docs/17-RoutingProviderResilience.md :: ### Intent Routing

```text
Q&A
code edit
search
billing
support escalation
```

## agent-harness/docs/17-RoutingProviderResilience.md :: ### Capability Routing

```text
这个任务需要哪些 Tool / Skill / Agent？
```

## agent-harness/docs/17-RoutingProviderResilience.md :: ### Model / Provider Routing

```text
quality
latency
cost
context length
tool support
multimodal
region/compliance
```

## agent-harness/docs/17-RoutingProviderResilience.md :: # 7. Claude Code 的实现信号

固定 Source Index 确认 `QueryEngine` 配置存在：

> 成熟 Runtime 会把 Model / Provider Failure 后的 fallback 纳入 Harness 控制面。

但具体 fallback 条件不能仅凭这一字段推断，本章只使用这个已核验边界。

## agent-harness/docs/17-RoutingProviderResilience.md :: ## Q：Agent Router 怎么设计？

> 我会先区分 intent、capability 和 model routing。稳定且高风险的规则优先 deterministic rule；开放语义可以用 classifier/LLM；如果 Tool schema 已足够表达能力，也可让模型直接选 Tool。Router 必须有 labeled eval、confusion matrix 和 fallback/unknown path。Model route 再结合质量、延迟、成本、context、tool support 和 risk，Provider 差异通过 adapter 归一化，但保留 capability metadata。

## agent-harness/docs/17-RoutingProviderResilience.md :: ## Q：Provider 失败怎么 Fallback？

> 先分类 error，只有 transient/rate-limit 等 retryable failure 才 backoff；context overflow 应触发 compaction，不是重试；fallback 前检查 Tool/Context/Structured Output 等 capability compatibility，高风险任务不能静默降级，并在 Trace 记录实际模型和原因。

## agent-harness/docs/18-MultiAgentA2AWorkspace.md :: # 18. Multi-Agent、Subagent、Handoff、A2A 与 Workspace Concurrency

Multi-Agent 是 Agent 面试里非常容易“概念先行”的部分。

```text
什么时候值得拆？
谁拥有任务？
上下文怎样隔离？
如何避免重复工作？
多个 Agent 同时改一个 Workspace 怎么办？
失败一个如何收敛？
A2A 和 MCP 到底什么关系？
```

这一章的目标是把 Multi-Agent 从“角色扮演”还原成：

> **任务所有权、能力委托、上下文隔离、共享资源并发和结果聚合问题。**

## agent-harness/docs/18-MultiAgentA2AWorkspace.md :: # 7. Claude Code `Task.ts` 提供的实现信号

```text
local_bash
local_agent
remote_agent
in_process_teammate
local_workflow
monitor_mcp
dream
```

> Subagent / Background Task 应是有身份、状态机、输出位置、取消语义的一等 Runtime 对象。

## agent-harness/docs/18-MultiAgentA2AWorkspace.md :: ## Q：什么时候用 Multi-Agent？

> 我只在任务可并行拆分、不同子任务需要明显不同 Context/能力，或者单 Agent Context 已经过载时考虑 Multi-Agent。设计重点不是“多少角色”，而是 task ownership、context isolation、budget、partial failure、result aggregation 和 shared-resource concurrency。Coding 场景最好给不同 Agent 独立 branch/worktree 或单 writer，避免并行覆盖同一 workspace。

## agent-harness/docs/18-MultiAgentA2AWorkspace.md :: ## Q：MCP 和 A2A 区别？

> MCP 主要标准化 Agent Host 与 Tool/Resource/Prompt Server 的连接；A2A 面向独立 Agent System 之间的 capability discovery、task collaboration 和 artifact/status exchange。内部 Subagent 一般仍在同一 Runtime 控制域，和 A2A 对端的信任边界不同。

## agent-harness/docs/19-TraceReplayObservability.md :: # 19. Trace、Replay 与 Observability

```text
Context Assembly
→ Model Call
→ Tool Selection
→ Permission
→ Tool Execution
→ Tool Result
→ State Transition
→ Compaction
→ Model Call
→ Subagent
→ Final Answer
```

所以 Production Agent 需要的不只是普通日志，而是：

> **能重建“模型看见了什么、决定了什么、Runtime 执行了什么、状态如何变化”的结构化执行轨迹。**

## agent-harness/docs/19-TraceReplayObservability.md :: # 4. Codex Rollout Trace 的源码证据

固定 Codex Source Index 中 `codex-rs/rollout-trace/README.md` 明确区分：

```text
exact raw payload evidence
ConversationItem
ToolCall
CodeCell / TerminalOperation
InteractionEdge
```

> Trace 应保留足够结构，能还原模型实际看到的输入、Tool Runtime Boundary 和信息流，而不是只有拼接后的日志文本。

```text
Debug
Replay
Evaluation
Incident Analysis
```

## agent-harness/docs/19-TraceReplayObservability.md :: # 5. OpenAI Agents SDK Tracing 给出的证据

```text
task
agent
turn
generation
tool
guardrail
handoff
```

这说明成熟 Agent Framework 会把 Trace 设计成 Runtime 一等能力，而不是应用自行 print。

## agent-harness/docs/19-TraceReplayObservability.md :: ## Q：Agent Trace 应该记录什么？

> 我会用 run/turn/step/model-call/tool-call 的层级 ID 做结构化 trace。至少记录模型实际看到的 context evidence、provider/model、tool call/result、permission、state transition、checkpoint/compaction、subagent relation、latency/token/cost。Trace 要能支持 debug 和 replay，但敏感 Prompt/Tool 参数要做 redaction、加密和 retention 控制。它和普通日志不同，重点是重建一条 Run 的因果执行链。

## agent-harness/docs/20-AgentEvaluationBenchmark.md :: # 20. Agent Evaluation、Benchmark 与 Data Flywheel

> Demo 看起来更聪明了，但没有人能证明整体任务成功率真的提高。

```text
是否选对 Tool
是否调用成功
是否走对 Route
是否满足最终任务
是否产生错误副作用
用了多少 Token / Cost / Time
```

## agent-harness/docs/20-AgentEvaluationBenchmark.md :: ## Q：Agent 应该怎么评估？

> 我会把 eval 分成最终 outcome、process/runtime、component 和 resource/safety 四层。最终优先验证真实环境状态，例如测试、DB、文件或 API，而不是相信 Agent 自报成功；再看 tool selection、routing、compaction、cost、latency 等过程指标。Dataset 来自真实线上任务、Bad Case 和 adversarial case，并做 bucket/holdout。每次 Prompt/Tool/Model 改动都跑同一 regression suite，再用 canary 验证线上分布。

## agent-harness/docs/20-AgentEvaluationBenchmark.md :: ## Q：Data Flywheel 怎么做？

> Production trace 先做 failure attribution，把代表性失败人工/半自动整理成新的 eval case，修复后离线 regression，再灰度上线；重点是把真实失败转成可重复测试，而不是自动把所有用户数据拿去训练。

## agent-harness/docs/21-CodingAgentWorkflow.md :: # 21. Coding Agent：Repo Understanding → Patch → Test → Verify

```text
Understand Repository
→ Understand Task
→ Locate Relevant Code
→ Plan Minimal Change
→ Edit / Patch
→ Run Test / Lint / Typecheck
→ Inspect Diff
→ Fix Regression
→ Verify Acceptance Criteria
→ Deliver
```

HUMAN-A 中 `AGENT-048 AI-assisted Development Workflow` 有 37 个独立来源，说明企业已经把“AI Coding 怎么真正进入研发流程”当成核心能力，而不只是 Copilot 使用技巧。

## agent-harness/docs/21-CodingAgentWorkflow.md :: # 15. Claude Code / Codex 为什么是重要实现参考

这两个产品本身就是成熟 Coding Agent，因此我们从源码索引中抽象：

```text
filesystem / search / tool runtime
workspace / session
permission / sandbox
cancellation
trace
context management
```

> **一个 Coding Agent 要完成可交付代码修改，Runtime 必须提供哪些闭环能力。**

## agent-harness/docs/21-CodingAgentWorkflow.md :: ## Q：AI Coding 怎么保证质量？

> 我把 Coding Agent 看成完整工程循环，不是代码生成器。先通过 tree/ripgrep/symbol/AST/LSP/语义搜索建立最小相关工作集；Patch 尽量小并绑定 base version；修改后跑 compile/typecheck/targeted tests，再看 diff 和影响范围，必要时跑 integration/regression；最终按独立 Acceptance Criteria 验证，而不是相信 Agent 说“完成”。高风险命令还必须经过 sandbox/permission，所有 test/diff 证据进入 trace 方便 review 和 rollback。

## agent-harness/docs/22-ProductionAgentRuntime.md :: # 22. Production Agent Runtime Architecture

```text
Loop
Tool
Context
Memory
State
Checkpoint
Security
MCP
Multi-Agent
Trace
Eval
Coding Workflow
```

> **当一个 Agent 从单机 Demo 变成多用户、长任务、高并发、可恢复的平台后，Runtime 应怎样拆服务、保存状态、隔离执行环境并治理成本？**

## agent-harness/docs/22-ProductionAgentRuntime.md :: # 4. API / Streaming Gateway

```text
auth
tenant
request id
run create/resume/cancel
stream events
rate / quota boundary
```

GET /runs/{id}
POST /runs/{id}/cancel
STREAM /runs/{id}/events
```

Transport 细节 Primary 在 FastAPI / Backend；Agent 模块关心 Run Lifecycle。

## agent-harness/docs/22-ProductionAgentRuntime.md :: # 8. Tool Gateway

```text
auth / credential
policy
schema validation
rate limit
timeout
idempotency
trace
```

## agent-harness/docs/22-ProductionAgentRuntime.md :: # 9. Model Provider Gateway

```text
provider adapter
model routing
retry / fallback
usage / cost
stream normalization
quota
```

否则 Framework / Provider 细节会污染 Runtime 主线。

## agent-harness/docs/22-ProductionAgentRuntime.md :: # 10. Durable Event / State Store

```text
Session
Run
State Version
Event
Checkpoint
Approval
Side-effect Ledger
Artifact Reference
```

```text
log
file snapshot
browser output
```

可以独立进入 Object / Artifact Store。

## agent-harness/docs/22-ProductionAgentRuntime.md :: # 12. Long-running Agent 如何跨 Worker

这就是为什么 Production Architecture 必须放在最后：它是前面所有机制的汇合。

## agent-harness/docs/22-ProductionAgentRuntime.md :: ## Q：Production Agent Backend 怎么设计？

> 我会把 Agent 平台拆成 API/streaming gateway、durable session/run service、scheduler/queue、可替换 harness worker、model provider gateway、tool gateway、sandbox/execution pool、artifact store、durable state/event store 和 trace/eval plane。Run 状态不能只在 worker memory，要能 checkpoint/resume；Tool side effect 需要 idempotency/ledger；permission 与 sandbox 分层；tenant identity 贯穿 state、memory、artifact、credential 和 trace；并用 queue/quota/backpressure 控制 provider、tool 和 sandbox 资源。规模小时这些可以同进程实现，但边界要先设计清楚。

## agent-harness/docs/23-FrameworkMappingBuildVsBuy.md :: # 23. Framework Mapping 与 Build-vs-Buy

学完 Agent Harness 最后一章，才开始看框架。

```text
LangChain class
LangGraph node
OpenAI Agents SDK agent
```

```text
先知道 Runtime Problem
→ 再知道需要哪些 Primitive
→ 最后把 Primitive 映射到 Framework
```

## agent-harness/docs/23-FrameworkMappingBuildVsBuy.md :: # 13. Anthropic `Building effective agents` 的重要启发

```text
从简单、可组合 pattern 开始
不要为了 Agent 标签过早引入复杂框架
```

> **先证明任务需要复杂 Runtime，再引入复杂 Runtime。**

## agent-harness/docs/23-FrameworkMappingBuildVsBuy.md :: # 16. 一个选型回答模板

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

## agent-harness/docs/23-FrameworkMappingBuildVsBuy.md :: ## Q：LangChain / LangGraph / 自研怎么选？

> 我不会从框架名出发，而先列 Runtime Requirement。只是模型+Tool 循环可以保持轻；如果有显式状态图、复杂分支、pause/resume、HITL，LangGraph 类 graph runtime 更合适；LangChain 更偏通用模型、Tool、Retriever integration。若产品有特殊 permission/sandbox、long-running reliability 或调度语义，可以自研 control plane，同时复用 Provider SDK、MCP、storage 等成熟组件。最终用真实 workload 和 failure case 做 POC，而不是按 Star 选。