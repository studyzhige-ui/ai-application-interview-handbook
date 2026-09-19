# 01. Agent 系统的全貌：模型之外，谁把任务做完

让模型回答一个问题，通常只需要一次请求。可当你说“读资料、找矛盾、补证据，最后交一份报告”时，事情就不一样了：

> 模型可以提出下一步，可是谁真正去做、检查结果，并把工作继续下去？

这一章先把这些角色放在同一张图上，之后再逐个打开工具、上下文、状态和安全机制，不急着背组件名单。

[Agent 目录](../README.md) · [下一章 →](02-WorkflowAutonomyAndRuntimeBoundary.md)

---

<a id="section-1"></a>

## 1. 先讲人话：Model 很聪明，但它不会替你经营一次“执行”

<a id="legacy-01-01"></a>

先把Agent想成一个正在工作的助手，而不是某个模型名字。读文件的是程序，推理下一步的是模型，显示进度和交付报告的是应用。**同一件工作由不同角色接力完成**，后面各章都从这条接力关系展开。

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

> **Agent Harness / Runtime（运行时执行系统）。**

---

<a id="section-2"></a>

## 2. 一个实用定义

<a id="legacy-01-02"></a>

不要把 Harness 记成某个框架名。

本课程使用这个工程定义：

> **Agent Harness / Runtime 是模型之外，负责组织 Context、维护执行 State（状态）、驱动 Agent Loop、暴露和执行 Tools、实施 Permission（权限） / Sandbox（沙箱）、处理失败与恢复，并记录 Trace（执行追踪） / Eval Evidence 的运行时系统。**

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

### 先有任务，再决定需要多少执行设施

例如“读取授权的A、B两份文件，写带引用的报告，不修改原件”。这已经包含三个问题：做什么、允许做什么、怎样算做好。

| 要求 | 谁落实 | 为什么模型一句话不够 |
|---|---|---|
| 读取授权材料 | 工具程序与文件权限 | 模型说能读不等于真实身份有权读 |
| 发现冲突后继续调查 | 模型提出方向，循环执行 | 一次回答不会自动取得后续证据 |
| 交付可下载报告 | 应用与产物存储 | “已保存”不等于文件存在 |
| 不修改原件 | 可用工具与执行隔离 | 不能只依赖模型记住一句禁止事项 |

如果一次读取就能生成合格结果，固定流程可能已足够。只有确实需要根据反馈选行动，才引入动态循环。长期记忆、多Agent、独立队列都不是凑齐才能叫Agent的必选配置。

---

<a id="section-3"></a>

## 3. 为什么“Model + API”还不够

<a id="legacy-01-03"></a>

假设你直接写：

```python
# 片段示意：只发起一次模型请求，尚未处理工具执行与反馈循环。
response = client.responses.create(
    model="some-model",
    input=user_input,
)
```

这只是一次 inference。

一旦任务进入多步执行，就会出现一组新的工程问题。

### 3.1 下一步由谁驱动？

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

### 3.2 Context 越来越长怎么办？

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
- Token Budget（预算）；
- Tool Result Offloading；
- Compaction（上下文压缩）；
- Memory（记忆） Retrieval；
- stale context 控制。

---

### 3.3 Tool 有副作用怎么办？

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

### 3.4 中途崩了怎么办？

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

- Checkpoint（检查点）；
- Resume（恢复执行）；
- Idempotency；
- Side-effect Ledger；
- Compensation。

这些都属于 Runtime 问题。

---

### 3.5 Agent 说“完成了”，真的完成了吗？

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

<a id="section-4"></a>

## 4. 八组执行责任：检查清单，不是八个必部署服务

<a id="legacy-01-04"></a>

下面的Plane是责任分组：应用承接任务，运行系统驱动执行，接口连接能力，资源承载事实与动作。几个分组可以由同一进程实现。这是一份防止遗漏责任的检查清单，不是要求再背一套八层架构。

为了后面学习不混乱，可以把 Runtime 拆成八个 Plane。

| Plane | 核心职责 | 典型问题 |
|---|---|---|
| Control Plane | 驱动 Loop / Step / Stop | 下一步是什么？何时停止？ |
| Context Plane | 组装模型本轮看到的信息 | 哪些 history / tool / memory 放进去？ |
| State Plane | 保存当前执行事实 | 任务做到哪？哪些 artifact 已生成？ |
| Capability Plane | 管理 Tool / Skill（技能包） / MCP / Agent | 当前有哪些能力？怎样发现？ |
| Execution Plane | 真正执行命令 / API / Tool | 在哪里跑？超时怎么办？ |
| Safety Plane | Permission / Approval（批准） / Sandbox | 这次动作可不可以做？能碰什么资源？ |
| Coordination Plane | Subagent（子Agent） / Handoff（控制权交接） / Ownership | 谁负责哪个子任务？怎样避免冲突？ |
| Observability & Eval Plane | Trace / Replay（重放） / Outcome | 为什么失败？真的做对了吗？ |

💡 **新手理解**：

> Model 更像“决策器”；Harness 更像“操作系统 + 调度器 + 安全层 + 记录系统”的组合。

这不是说 Harness 真的是 OS，而是强调：**它负责把模型决策变成受控执行。**

---

<a id="section-5"></a>

## 5. 一个最小 Runtime 长什么样

<a id="legacy-01-05"></a>

先看顺序，不急着读代码：

```text
接收任务 → 保存当前目标
            ↓
组织模型输入 → 模型建议下一步
            ↓
      ┌─────┴────────┐
    请求工具       提交答案
      ↓              ↓
校验并执行       按任务条件验收
      ↓              ↓
记录观察再循环    交付/补充/停止
```

这里已经有State（当前工作状态）、Loop（循环）、Registry（工具目录）、Dispatch（分发）、Observation（观察）和Stop（停止）。它仍不是生产系统：权限、超时、取消、结果过大、跨重启恢复与副作用正确性，还需要后面逐项展开。

第03章提供有注释的最小反馈循环。这里不再放一段省略大量保障、却声称生产可用的代码。

---

<a id="section-6"></a>

## 6. Model 和 Harness 到底各负责什么

<a id="legacy-01-06"></a>

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

表中的责任划分是建议与保证的区别：模型可以建议“值得重试”，真正重试仍由程序检查预算、权限以及动作是否已经发生。不同章节再次提到某个检查时，应先看它在阻止哪一种后果。

---

<a id="section-7"></a>

## 7. 一个 AI 应用场景：企业知识库 Agent

<a id="legacy-01-09"></a>

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

<a id="section-8"></a>

## 8. Harness、Backend、Framework 不要混在一起

<a id="legacy-01-10"></a>

### Harness vs 普通 Backend

普通 Backend 也会有：

- DB；
- Cache；
- Queue；
- Retry（重试）；
- Auth；
- Observability。

Agent Harness 复用这些基础设施，但它多了一套 Model-in-the-loop 的执行语义：

```text
Model Decision
→ Runtime Action
→ Environment Observation
→ Model 再决策
```

### Harness vs Agent Framework

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

<a id="section-9"></a>

## 9. 产品实现与官方资料对照（按需展开）

<details>
<summary>成熟产品源码告诉我们的什么</summary>

<a id="legacy-01-07"></a>

本课程固定两份源码快照：

```text
Claude Code
commit = 58231dcce408f805c645cfbc352d2876b517223b

OpenAI Codex
commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

### 9.1 Claude Code：QueryEngine 明确拥有 Conversation Runtime

固定快照中的 `QueryEngine.ts` 直接写明：

- 一个 conversation 对应一个 `QueryEngine`；
- 每次 `submitMessage()` 开启一个新 turn；
- messages、file cache、usage 等状态跨 turn 保留；
- Runtime 配置中存在 tools、MCP clients、agents、`canUseTool`、`maxTurns`、`maxBudgetUsd`、fallback model 和 `AbortController`。

这说明成熟 Agent 产品不会把“会调用 Tool 的模型”当作全部 Runtime。

它还需要一个长期存在的 conversation execution object。

### 9.2 Claude Code：Tool 不是普通函数

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

### 9.3 Codex：Context / Session / Tool / Sandbox 都是独立 Runtime 对象

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

</details>

<details>
<summary>官方资料为什么也强调 Harness，而不是只强调模型</summary>

<a id="legacy-01-08"></a>

Anthropic 的 `Building effective agents` 把 Workflow 和更自主的 Agent 区分开，并强调从简单、可组合的结构开始，而不是为了“Agent”标签无脑上复杂框架。

OpenAI 的 `A practical guide to building agents` 也把 Agent 看成由 Model、Tools、Instructions / Orchestration 和 Guardrail 等部分共同组成的系统。

Anthropic 后续的 Context Engineering、Long-running Harness、Managed Agents、Containment（限制故障或攻击影响范围） 等文章进一步把问题推到：

```text
Context
Session
Execution Environment
Safety Boundary
Long-running Progress
Verification
```

这正好和真实面经、Claude Code / Codex 源码形成三侧交叉验证。

</details>

具体实现以[固定源码与官方索引](../../../references/agent/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 10. HUMAN-A 信号

### HUMAN-A

- `AGENT-002` Harness / Runtime Boundary：25 个独立来源；
- `AGENT-003` Agent Loop / Runtime：36 个独立来源。

频率只由 HUMAN-A 决定。

### Claude Code 源码

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

主要入口：

- `QueryEngine.ts`
- `Tool.ts`
- `Task.ts`
- `query.ts`
- `utils/queryContext.ts`
- `utils/sessionStorage.ts`

### OpenAI Codex 源码

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

主要入口：

- `codex-rs/core/src/compact.rs`
- `codex-rs/tools/`
- `codex-rs/core/src/tools/router.rs`
- `codex-rs/sandboxing/`
- `codex-rs/rollout-trace/`

### 外部权威资料

- Anthropic — Building effective agents
  https://www.anthropic.com/engineering/building-effective-agents
- OpenAI — A practical guide to building agents
  https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- Anthropic — Effective context engineering for AI agents
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

<a id="interview"></a>

## 11. 面试怎么答

### Q：什么是 Agent？为什么不等于“LLM 加几个工具”？

🎯 **30 秒回答**：

> Agent 的关键是允许模型依据中间观察动态选择后续行动，且这种选择受目标和约束限制。工具只是让动作能发生的一种方式；固定程序也能调用工具。要交付可靠系统，还需要程序负责执行、校验、停止和必要状态管理，但长期记忆、多 Agent 和代码沙箱不是身份必选项。

### Q：Harness 和 Runtime 究竟有没有区别？

🎯 **30 秒回答**：

> 二者在产品文档里可能重叠。本书把 Runtime 用于一次执行的运行机制，把 Harness 用于围绕模型组织运行、工具、上下文、安全与验证的支撑系统。编排器是决定调用谁和如何推进的一部分，框架是实现这些责任的代码库。回答时先说明采用的工作定义，再对照具体产品，不把自定义术语当行业标准。

### Q：设计一个 Agent 系统，最先决定什么？

🎯 **30 秒回答**：

> 先确定服务对象、目标、输入环境、允许动作、运行约束和完成证据，再判断哪段工作需要模型动态决策。报告任务的原件只读、授权清单和引用要求会直接决定工具与验收。若固定读取加一次生成已经满足要求，就保留简单流程，而不是为了 Agent 标签增加一整套组件。

### Q：模型说完成，为什么不能直接标记业务成功？

🎯 **30 秒回答**：

> 模型输出是完成候选，不是外部事实。报告可能缺来源，代码可能没测试，创建工单的请求可能尚无回执。程序应根据任务契约检查实际产物、返回状态及适用的内容标准，并区分成功、部分交付、失败、取消和预算停止。验证能力也有边界，不能把某项检查通过说成证明所有要求。

### 继续展开时的回答结构

### Level 1｜30 秒

🎯 **可以这样回答：**

> Agent Harness / Runtime 是模型之外的执行系统。模型负责理解和决策，Harness 负责把决策变成可控执行，包括 Context Assembly、Agent Loop、Tool Registry/Execution、Session/State、Permission/Sandbox、Checkpoint/Resume、Trace/Eval 等。成熟 Agent 的难点通常不是“会不会调模型”，而是多步任务中的状态、失败、副作用、安全和可验证性。

### Level 2｜2–3 分钟

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

### Level 3｜继续深挖

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

<a id="pitfalls"></a>

## 12. 高频易错点

⚠️ **Agent = LLM + Tool**
这是入门公式，但对 Production（生产环境） 不够。缺 State、Context、Failure、Permission、Recovery、Trace、Eval。

⚠️ **Harness = Prompt Template**
Prompt 只是 Context 的一部分；Harness 负责跨多轮执行。

⚠️ **Tool Call 成功 = 任务成功**
Tool 只是局部动作。最终还要验证 task outcome。

⚠️ **Memory = History（历史记录）**
History 是过去事件，Memory 是可被未来召回的信息，Runtime State 是当前执行事实。

⚠️ **Sandbox = Permission Prompt**
Permission 是 policy/approval，Sandbox 是执行环境的硬边界。

⚠️ **用了 LangGraph 就有成熟 Harness**
框架提供 Primitive，不自动替你定义业务状态、失败语义、安全边界与评测。

⚠️ **用了工具就是 Agent。** 固定流程也能使用工具；区别在后续路径的控制权。

⚠️ **Harness 只是 system prompt。** 文字不能替程序真正执行、保存、限制或终止动作。

⚠️ **每个 Agent 都需要长期记忆和向量库。** 需要由跨任务复用与检索需求推导，而不是凑组件。

⚠️ **架构图上的方框必须独立部署。** 方框首先表示责任，部署由规模与隔离要求决定。

---

<a id="self-test"></a>

## 13. 本章自测

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

<details><summary>5. 三份文件已全在输入里，必须循环吗？</summary>

不必须。若一次生成与校验已满足要求，固定流程更容易测试。只有读取选择或后续动作确实取决于中间观察时，才有理由比较动态循环。

</details>

<details><summary>6. “已经读了两份，第三份无权限”属于什么？</summary>

它首先是程序的当前执行状态。为了让模型决定下一步，程序可以把它的一部分放入上下文；为了重启后仍知道它，程序可能把它持久化。这是同一事实的不同用途，不是三个不同世界。

</details>

<details><summary>7. 原件只读要求应只放在哪里？</summary>

不能只放在提示词。任务描述应清楚告知模型，工具与文件身份还必须真正限制写入。描述负责沟通，程序和环境负责约束；两者不能互相替代。

</details>

<details><summary>8. 编排器是否等于整个 Harness？</summary>

不等于。编排器重点控制步骤和委派；Harness 还要组织工具接入、上下文、安全、状态和验证。一个小程序可由同一对象实现多项责任，但概念上仍应分清。

</details>

<details><summary>9. 怎样证明报告可交付？</summary>

至少检查产物可读、来源属于授权清单、引用可定位、原件未被修改，并核对结论是否被证据支持。机械检查和内容核验分别回答不同问题，结果中要披露尚未解决的缺口。

</details>

<details><summary>10. 后面章节都提到安全，是否一定重复？</summary>

不一定。参数是否为整数、当前用户是否能读文件、进程能否访问目录，分别属于输入契约、授权和执行隔离。同一动作经过多个不同判断才合理；重复完整的通用清单才应压缩。

</details>

---

[Agent 目录](../README.md) · [下一章 →](02-WorkflowAutonomyAndRuntimeBoundary.md)
