# 01. Agent Harness 在 AI 应用中的职责

`AGENT-002` 在冻结 HUMAN-A 中有 **25 个独立来源**，`AGENT-003` 的完整 Agent Loop 有 **36 个独立来源**。这说明企业并不满足于“会调模型 API”，而是在追问：

> **模型之外，到底是谁负责让一个 Agent 安全、连续、可恢复、可评测地完成任务？**

这一章先把整套 Agent Harness / Runtime 课程的总图搭起来。

---

# 1. 先讲人话：Model 很聪明，但它不会替你经营一次“执行”

一次普通 LLM Call 很像：

```text
Input
  ↓
Model
  ↓
Output
```

如果只是：

- 总结一段文本；
- 分类；
- 改写；
- 生成一个短答案；

这个模型调用本身可能已经够了。

但一个 Agent 任务可能是：

```text
“阅读这个仓库，找到 Bug，修改代码，运行测试，失败就修，最后给我可交付结果。”
```

这时真正发生的是：

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

其它事情必须由软件系统负责。

这个围绕模型、工具、状态、上下文和执行环境建立起来的系统，就是本课程所说的：

> **Agent Harness / Runtime。**

---

# 2. 一个实用定义

不要把 Harness 记成某个框架名。

本课程使用这个工程定义：

> **Agent Harness / Runtime 是模型之外，负责组织 Context、维护执行 State、驱动 Agent Loop、暴露和执行 Tools、实施 Permission / Sandbox、处理失败与恢复，并记录 Trace / Eval Evidence 的运行时系统。**

可以画成：

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

注意：

```text
Model ≠ Agent Harness
Agent Framework ≠ Agent 本身
Tool Calling ≠ 完整 Agent Runtime
Memory ≠ 所有 State
```

这些边界后面会逐章拆开。

---

# 3. 为什么“Model + API”还不够

假设你直接写：

```python
response = client.responses.create(
    model="some-model",
    input=user_input,
)
```

这只是一次 inference。

一旦任务进入多步执行，就会出现一组新的工程问题。

## 3.1 下一步由谁驱动？

模型说：

```text
我要调用 read_file(path="src/app.py")
```

谁来：

- 解析这次 Tool Call；
- 找到真实 Tool；
- 校验参数；
- 判断权限；
- 执行；
- 把结果回填给模型；
- 决定是否继续下一轮？

答案不是模型，而是 Runtime。

---

## 3.2 Context 越来越长怎么办？

Agent 每做一步都会生成新信息：

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

如果全部无限追加：

```text
history ↑
context tokens ↑
latency ↑
cost ↑
noise ↑
最终撞 Context Window
```

因此 Harness 必须承担：

- Context Assembly；
- Token Budget；
- Tool Result Offloading；
- Compaction；
- Memory Retrieval；
- stale context 控制。

---

## 3.3 Tool 有副作用怎么办？

读文件和删生产数据不是一个风险等级：

```text
read_file
vs
rm -rf
vs
send_email
vs
transfer_money
```

成熟 Runtime 必须把：

```text
Capability Selection
Permission Decision
Human Approval
Sandbox Enforcement
```

分开处理。

---

## 3.4 中途崩了怎么办？

长任务可能运行几十分钟甚至几小时。

如果进程在第 37 步崩溃：

```text
重新从第 1 步开始？
```

通常不可接受。

尤其如果第 20 步已经发出外部副作用：

```text
创建工单成功
↓
Checkpoint 写失败
↓
服务崩溃
↓
Resume 后再次创建工单？
```

这会直接引出：

- Checkpoint；
- Resume；
- Idempotency；
- Side-effect Ledger；
- Compensation。

这些都属于 Runtime 问题。

---

## 3.5 Agent 说“完成了”，真的完成了吗？

Agent 输出：

```text
“修复完成，所有测试通过。”
```

不能直接当作事实。

Harness 还需要建立：

```text
Test Result
Diff
Exit Code
Artifact
Environment Outcome
Trace
Eval
```

去验证它真的完成了任务。

这也是为什么 Coding Agent 的质量不能只看最终自然语言回答。

---

# 4. Harness 的八个工程平面

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

💡 **新手理解**：

> Model 更像“决策器”；Harness 更像“操作系统 + 调度器 + 安全层 + 记录系统”的组合。

这不是说 Harness 真的是 OS，而是强调：**它负责把模型决策变成受控执行。**

---

# 5. 一个最小 Runtime 长什么样

先写一个故意简化的版本：

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

这已经比一次 Model Call 多出了：

```text
State
Loop
Tool Registry
Tool Dispatch
Result Feedback
Stop Condition
Max Step Guard
```

但它仍然离 Production 很远，因为还没有：

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

后面 46 章就是把这个最小 Loop 一层层工程化。

---

# 6. Model 和 Harness 到底各负责什么

这是面试里非常重要的边界。

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

⚠️ **面试易错点**：

不要说：

> “Agent 的 Memory、Tool、Loop 都是模型能力。”

模型可能具备 Tool Use 能力，但：

> **Tool 能否被调用、如何执行、调用结果如何进入下一轮、失败后怎样恢复，是 Runtime 的实现责任。**

---

# 7. 成熟产品源码告诉我们的什么

本课程固定两份源码快照：

```text
Claude Code
commit = 58231dcce408f805c645cfbc352d2876b517223b

OpenAI Codex
commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

## 7.1 Claude Code：QueryEngine 明确拥有 Conversation Runtime

固定快照中的 `QueryEngine.ts` 直接写明：

- 一个 conversation 对应一个 `QueryEngine`；
- 每次 `submitMessage()` 开启一个新 turn；
- messages、file cache、usage 等状态跨 turn 保留；
- Runtime 配置中存在 tools、MCP clients、agents、`canUseTool`、`maxTurns`、`maxBudgetUsd`、fallback model 和 `AbortController`。

这说明成熟 Agent 产品不会把“会调用 Tool 的模型”当作全部 Runtime。

它还需要一个长期存在的 conversation execution object。

## 7.2 Claude Code：Tool 不是普通函数

`Tool.ts` 中的 Tool Contract 还显式包含：

- input schema；
- permission callback；
- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior()`；
- progress / result；
- context impact。

这会在 Tool Runtime 部分详细拆。

## 7.3 Codex：Context / Session / Tool / Sandbox 都是独立 Runtime 对象

固定 Codex 快照中已经可以直接看到：

- `Session`、`TurnContext`、`StepContext`；
- `EventMsg`、`TurnItem`；
- Tool router / executor；
- `SandboxPolicy`；
- compaction lifecycle；
- rollout trace。

这些对象本身就在告诉我们：

> **成熟 Agent Runtime 的复杂度来自“执行系统”，而不只是 Prompt。**

这里必须强调：

> Claude Code / Codex 的具体实现是产品实现证据，不是所有 Agent 必须复制的唯一标准。

我们学习的是它们暴露出的稳定工程问题。

---

# 8. 官方资料为什么也强调 Harness，而不是只强调模型

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

---

# 9. 一个 AI 应用场景：企业知识库 Agent

用户问：

```text
“检查最近一周所有高优先级客户工单，找出重复问题，生成修复建议，并为确认的问题创建 Jira。”
```

如果只靠 Model：

```text
模型不知道去哪里查工单
模型不能真正创建 Jira
模型无法知道已经创建了哪些 Jira
模型不能保证重复执行不会创建重复工单
```

Harness 需要负责：

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

这就是“AI 应用开发”真正进入工程系统的地方。

---

# 10. Harness、Backend、Framework 不要混在一起

## Harness vs 普通 Backend

普通 Backend 也会有：

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

## Harness vs Agent Framework

LangGraph、OpenAI Agents SDK、Claude Agent SDK 等可以帮助你实现 Runtime Primitive。

但：

```text
Harness Problem
≠ 某一个 Framework API
```

先理解：

- State；
- Loop；
- Tool；
- Context；
- Permission；
- Checkpoint；
- Trace；

再学框架，你才能判断框架帮你解决了什么、没解决什么。

---

# 11. 高频易错点

⚠️ **Agent = LLM + Tool**  
这是入门公式，但对 Production 不够。缺 State、Context、Failure、Permission、Recovery、Trace、Eval。

⚠️ **Harness = Prompt Template**  
Prompt 只是 Context 的一部分；Harness 负责跨多轮执行。

⚠️ **Tool Call 成功 = 任务成功**  
Tool 只是局部动作。最终还要验证 task outcome。

⚠️ **Memory = History**  
History 是过去事件，Memory 是可被未来召回的信息，Runtime State 是当前执行事实。

⚠️ **Sandbox = Permission Prompt**  
Permission 是 policy/approval，Sandbox 是执行环境的硬边界。

⚠️ **用了 LangGraph 就有成熟 Harness**  
框架提供 Primitive，不自动替你定义业务状态、失败语义、安全边界与评测。

---

# 12. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Agent Harness / Runtime 是模型之外的执行系统。模型负责理解和决策，Harness 负责把决策变成可控执行，包括 Context Assembly、Agent Loop、Tool Registry/Execution、Session/State、Permission/Sandbox、Checkpoint/Resume、Trace/Eval 等。成熟 Agent 的难点通常不是“会不会调模型”，而是多步任务中的状态、失败、副作用、安全和可验证性。

## Level 2｜2–3 分钟

可以按五段回答：

```text
1. 先区分 Model 和 Runtime
2. 解释一个完整 Loop
3. 说明 Context / State / Tool 三个核心面
4. 补 Failure / Safety / Recovery
5. 用 Claude Code / Codex 或项目例子落地
```

例如：

> 模型给出 Tool Call 以后，Runtime 不能直接执行。它需要校验 schema、查 registry、做 permission、必要时 human approval，再在 sandbox 中执行；Tool Result 要进入 event/state，再经过 context budget 组装回下一轮。长任务还要处理 checkpoint、resume 和外部副作用幂等。最终结果不能只看模型说“完成”，还要看 test、artifact、environment outcome 和 trace。

## Level 3｜继续深挖

面试官通常会继续追：

- Agent vs Workflow 怎么判断？
- Loop 怎样停止？
- Tool 失败怎样 Repair / Retry？
- Context 爆了怎么 Compact？
- Memory 和 State 有什么区别？
- Checkpoint 后怎样 Resume？
- Permission 和 Sandbox 怎么分？
- Multi-Agent 怎么避免冲突？
- Agent Evaluation 怎么做？

后续章节会一条条拆开。

---

# 13. 本章证据边界

## HUMAN-A

- `AGENT-002` Harness / Runtime Boundary：25 个独立来源；
- `AGENT-003` Agent Loop / Runtime：36 个独立来源。

频率只由 HUMAN-A 决定。

## Claude Code 源码

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

主要入口：

- `QueryEngine.ts`
- `Tool.ts`
- `Task.ts`
- `query.ts`
- `utils/queryContext.ts`
- `utils/sessionStorage.ts`

## OpenAI Codex 源码

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

主要入口：

- `codex-rs/core/src/compact.rs`
- `codex-rs/tools/`
- `codex-rs/core/src/tools/router.rs`
- `codex-rs/sandboxing/`
- `codex-rs/rollout-trace/`

## 外部权威资料

- Anthropic — Building effective agents  
  https://www.anthropic.com/engineering/building-effective-agents
- OpenAI — A practical guide to building agents  
  https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- Anthropic — Effective context engineering for AI agents  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

# 14. 自测

<details><summary>1. 为什么“Tool Calling 能力”不等于“Agent Runtime”？</summary>

因为 Tool Calling 只解决模型如何表达“我想调用某个能力”。真正执行还需要 Runtime 完成 Tool Lookup、Schema Validation、Permission、Execution、Timeout、Result Normalization、State Update、Failure Handling 和下一轮 Context Assembly。
</details>

<details><summary>2. Model 和 Harness 最核心的分工是什么？</summary>

模型更偏理解、推理、生成决策；Harness 更偏组织上下文、维护状态、执行动作、控制风险、恢复失败、记录证据和验证结果。
</details>

<details><summary>3. 为什么 Agent Harness 课程不能从 LangGraph API 开始？</summary>

因为框架 API 是某一种实现。只有先理解 Loop、State、Context、Tool、Permission、Recovery、Trace 等 Runtime Problem，才能判断框架提供了哪些能力、哪些仍要自己设计，也不会把框架名词误当成通用原理。
</details>

<details><summary>4. 一个 Agent 输出“任务完成”，为什么不能直接结束？</summary>

因为自然语言自述不是可靠的任务完成证据。需要根据业务定义检查 artifact、external state、test、exit code、diff、metric 或 grader 等 outcome evidence，再决定是否真正进入 terminal state。
</details>
