# 03. Harness / Runtime 与 Model、Workflow Engine、Backend 的边界

`AGENT-002` 在冻结 HUMAN-A 中有 **25 个独立来源**。这是一个很容易“概念糊成一团”的问题：

```text
Model
Agent
Harness
Runtime
Orchestrator
Workflow Engine
Backend
Framework
```

如果这些词不分清，后面学 Context、State、Tool、Checkpoint 时会一直混乱。

这一章的目标不是争论术语，而是建立一个**可用于设计系统的责任边界**。

---

# 1. 先给结论

本课程采用下面的实用分层：

```text
Product / Application
        │
        ▼
Agent Harness / Runtime
        │
   ┌────┴────┐
   ▼         ▼
 Model     Execution Environment / Tools
        │
        ▼
Backend Infrastructure
```

其中：

- **Model**：推理、生成、选择动作；
- **Harness / Runtime**：驱动多步执行、管理 Context / State / Tool / Policy / Recovery；
- **Workflow / Orchestrator**：更强调任务编排和控制流；
- **Execution Environment**：真正运行命令、文件操作、浏览器、容器等；
- **Backend Infrastructure**：DB、Redis、Queue、API Gateway、Observability、Auth 等通用底座；
- **Framework**：帮助你实现其中一些 Runtime Primitive 的软件库。

这几个东西可以集成在一个进程里，但**职责不是同一个东西**。

---

# 2. Model 的边界

模型接收：

```text
Instructions
+ User Input
+ Context
+ Tool Schema
+ 当前 Observation
```

然后输出：

```text
Text
or
Structured Output
or
Tool Call
or
Plan / Decision
```

它擅长：

- 语言理解；
- 推理；
- 规划；
- 代码生成；
- 选择 Tool；
- 生成结构化动作。

但它通常不直接拥有：

- durable session storage；
- filesystem permission；
- process cancellation；
- sandbox enforcement；
- external idempotency state；
- retry ledger；
- trace store；
- checkpoint transaction。

💡 **新手理解**：

> Model 是“决策器”，不是完整的“执行操作系统”。

---

# 3. Harness / Runtime 的边界

Harness 负责把“模型的一个建议”变成“系统中的一次合法状态转移”。

例如模型输出：

```json
{
  "tool": "write_file",
  "arguments": {
    "path": "src/config.py",
    "content": "..."
  }
}
```

Runtime 不应该直接 `write()`。

更完整的链路应该是：

```text
Model Tool Call
      ↓
Parse / Normalize
      ↓
Schema Validation
      ↓
Tool Registry Lookup
      ↓
Policy / Permission
      ↓
Human Approval? 
      ↓
Sandbox / Execution Environment
      ↓
Execute
      ↓
Normalize Result / Error
      ↓
Persist Event / State
      ↓
Assemble next Context
```

这整条链路属于 Runtime。

---

# 4. Orchestrator / Workflow Engine 与 Harness 有什么区别

这两个概念有重叠，但关注点不同。

## 4.1 Workflow Engine 更关注“任务怎样按定义推进”

典型能力：

- DAG / State Machine；
- Task Scheduling；
- Retry；
- Timeout；
- Durable Execution；
- Compensation；
- Worker；
- Timer / Signal。

例如：

```text
A
→ B
→ C
```

或者：

```text
pending
→ approved
→ running
→ completed
```

## 4.2 Agent Harness 更关注“模型在循环里怎样与环境交互”

典型能力：

- Context Assembly；
- Model Call；
- Tool Calling；
- Memory；
- Compaction；
- Dynamic Capability Discovery；
- Permission / Sandbox；
- Agent Evaluation。

因此可以出现：

```text
Durable Workflow Engine
        │
        └─ 某个 Step 运行 Agent Harness
```

也可以：

```text
Agent Harness 自己实现轻量的 checkpoint / retry
```

所以：

> **二者不是互斥产品名，而是不同关注面的运行时能力。**

---

# 5. 为什么 Agent Harness 不能完全等同于 Orchestrator

如果只用普通 Workflow Engine 思维，你可能会设计：

```text
Step1 -> Step2 -> Step3
```

但 Agent 的下一步可能是模型动态决定的：

```text
Step N
  ↓
Model decides
  ├─ call search
  ├─ call read_file
  ├─ call test
  ├─ delegate subagent
  └─ finish
```

它需要一种“模型参与控制流”的 Runtime。

与此同时，Agent Harness 还要处理：

- Tool Schema 在 Context 中怎样暴露；
- Tool Result 怎样回填；
- Token Budget；
- Context Compaction；
- Memory Retrieval；

这些不是传统 Workflow Engine 的核心语义。

---

# 6. Harness 与普通 Backend 的边界

一个 Agent 服务最终仍然是 Backend。

它可能依赖：

```text
FastAPI / HTTP
MySQL
Redis
Vector DB
Message Queue
Object Storage
Kubernetes
Metrics / Log / Trace
```

但这些属于更通用的 Backend 能力。

Harness 在这些基础设施之上形成新的业务运行时语义：

```text
Session
Turn
Step
Tool Call
Tool Result
Checkpoint
Compaction
Approval
Agent Trace
```

例如 Redis 里可以存 Agent Checkpoint。

但是：

```text
Redis 的 TTL / Replication / Persistence
→ Redis 模块

Checkpoint 需要保存哪些 Runtime State
→ Agent Harness 模块
```

这就是课程里 Primary Module 的划分方式。

---

# 7. Harness 与 Framework 的边界

## 7.1 Framework 是实现工具

例如 Framework 可能提供：

- Agent Loop；
- State Graph；
- Tool wrapper；
- Handoff；
- Guardrail；
- Session；
- Trace。

但 Framework 不会自动替你回答：

```text
业务里的 State 是什么？
什么动作需要 Approval？
Checkpoint 一致性怎么保证？
Tool 失败时 Retry 还是 Fail？
Final Outcome 怎么验证？
```

这些仍然是你的系统设计。

## 7.2 所以学习顺序应该是

```text
Runtime Problem
→ Runtime Primitive
→ 自己能画出最小实现
→ 看 Claude Code / Codex
→ 最后映射 Framework
```

而不是：

```text
记 Node / Edge API
→ 误以为学会 Agent Runtime
```

---

# 8. 四个最重要的 Runtime Boundary

## 8.1 Model Boundary

问题：

> 什么进入模型，什么留在 Runtime？

例如：

```text
Tool Registry 中有 500 个 Tool
```

不代表 500 个完整 Schema 都必须进入本轮 Context。

Runtime 可以做 Discovery / Progressive Loading。

---

## 8.2 Execution Boundary

问题：

> 模型请求的动作在哪里真正执行？

例如：

```text
run_shell("pytest")
```

可以运行在：

- 本机；
- container；
- remote worker；
- sandbox VM；
- managed execution environment。

模型无需知道所有底层实现，但 Harness 必须知道如何路由和控制。

---

## 8.3 State Boundary

问题：

> 哪些事实由 Runtime 保存，哪些信息只作为 Context 暂时展示给模型？

例如：

```text
current_step = 17
checkpoint_version = 5
jira_issue_id = "AI-231"
approved_tool_call_id = "call_abc"
```

这些不应该只存在于自然语言历史里。

它们是结构化 Runtime State。

---

## 8.4 Safety Boundary

问题：

> Model 想做 ≠ Runtime 必须允许做。

典型链路：

```text
Model requests action
→ Policy checks
→ Approval if needed
→ Sandbox limits
→ Execute
```

这也是为什么“模型遵守 System Prompt”不能替代安全边界。

---

# 9. State 应该由谁拥有

这是非常关键的设计题。

假设 Agent 正在修代码。

可能有：

| State | 更适合放哪里 |
|---|---|
| 原始用户 Goal | Durable Run State + Context |
| 当前 messages | Session / History Store |
| 当前 Tool Call ID | Runtime State |
| 已修改文件列表 | Runtime / Workspace State |
| Test Exit Code | Event / Verification State |
| 用户偏好 | Memory |
| Tool Schema | Capability Registry |
| Tool Permission | Policy Store |
| Sandbox Writable Roots | Execution Policy |

如果把所有东西都塞进：

```text
messages = [...]
```

后面很难：

- 恢复；
- 并发；
- 校验；
- 审计；
- 版本化。

---

# 10. 为什么 Runtime Event 和 Model-visible Message 也要分开

例如 Runtime 发生：

```text
ToolStarted
ToolProgress
ToolCompleted
CheckpointSaved
ApprovalRequested
ApprovalGranted
CompactionStarted
CompactionFinished
```

这些事件不一定全部需要原样塞给模型。

因此：

```text
Runtime Event Stream
≠ Model Context
```

Runtime 可以记录完整事实，同时只投影一部分给模型。

这会在第 6 章详细讲。

---

# 11. Claude Code 的源码边界

固定快照：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

## 11.1 `QueryEngine.ts`

文件中的注释明确表达：

- `QueryEngine` owns query lifecycle and session state for a conversation；
- 每个 conversation 一个 QueryEngine；
- `submitMessage()` 启动新 turn；
- State 跨 turn 持续。

这是一种非常清晰的 Runtime Ownership。

## 11.2 `Tool.ts`

Tool 执行不是独立函数，而依赖 `ToolUseContext`：

- AbortController；
- app state；
- MCP clients；
- agent definitions；
- permission context；
- tool decisions；
- content replacement state。

这说明：

> Tool execution 是 Runtime Context 中的一次受控操作。

## 11.3 `Task.ts`

Task 有：

```text
pending / running / completed / failed / killed
```

还包含 output file、start/end time、kill semantics。

这说明“Task”是 Runtime 一级对象，不是普通 async function。

---

# 12. Codex 的源码边界

固定快照：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

已确认的源码对象包括：

```text
Session
TurnContext
StepContext
WorldState
EventMsg
TurnItem
ToolCall
ToolExecutor
SandboxPolicy
Compaction
Rollout Trace
```

例如 `codex-rs/core/src/compact.rs` 并不是一个：

```python
summary = llm(history)
```

而是一个包含：

- Hook；
- Retry；
- Replacement History；
- Persistence；
- Token Recompute；
- Analytics；

的 Runtime Transaction。

这正体现 Model 和 Runtime 的边界。

---

# 13. 一个最小分层代码模型

可以先设计几个接口：

```python
from dataclasses import dataclass
from typing import Protocol, Any


class ModelAdapter(Protocol):
    async def generate(self, context: list[dict], tools: list[dict]): ...


class ToolExecutor(Protocol):
    async def execute(self, call, run_state): ...


class StateStore(Protocol):
    async def load(self, run_id: str): ...
    async def save(self, state): ...


class PolicyEngine(Protocol):
    async def authorize(self, call, state) -> bool: ...


@dataclass
class Runtime:
    model: ModelAdapter
    tool_executor: ToolExecutor
    state_store: StateStore
    policy: PolicyEngine
```

注意这里故意把：

```text
Model
Tool Execution
State
Policy
```

拆成不同依赖。

这让你以后更容易：

- 替换模型 Provider；
- 把 Tool 放到 Remote Worker；
- 更换 State Store；
- 加 Sandbox；
- 测试 Runtime。

---

# 14. Model Provider Adapter 为什么属于 Harness

如果系统要同时支持多个模型：

```text
OpenAI
Anthropic
Gemini
Local Model
```

不同 Provider 可能有不同：

- Tool Call Schema；
- Stop Reason；
- Streaming Event；
- Error Type；
- Context Window；
- Usage Metadata。

Runtime 通常需要归一化：

```text
Provider Response
→ Internal ModelEvent / ToolCall
```

业务层才不需要理解每个 Provider 的细节。

这会在 Model Routing 章节深入。

---

# 15. Failure Ownership 怎么判断

一个很实用的方法：问“这个失败应该由谁修？”

| Failure | 主要负责层 |
|---|---|
| 模型输出错误推理 | Model / Prompt / Context / Eval |
| Tool 参数 Schema 不合法 | Runtime Validation |
| Tool 没权限 | Policy / Approval |
| Shell 越界访问 | Sandbox |
| API 429 | Tool/Provider Resilience |
| Session 丢失 | State / Persistence |
| Crash 后重复发邮件 | Idempotency / Runtime |
| 用户网络断线 | Backend Transport |
| MySQL 慢查询 | Data Layer |

这样可以避免把所有问题都归成：

> “Prompt 不好。”

---

# 16. Harness 的边界为什么不是固定的

不同系统会有不同部署方式。

### 小型 Demo

```text
FastAPI process
├─ Agent Loop
├─ Tool
└─ in-memory state
```

### Production

```text
API Gateway
   ↓
Session Service
   ↓
Harness Worker
   ├─ Model Gateway
   ├─ Tool Gateway
   ├─ State Store
   └─ Trace
          ↓
Sandbox Worker Pool
```

逻辑边界稳定，但物理部署可以变化。

这也是为什么学习概念时不要把“一个 class”当成全部 Runtime。

---

# 17. 与 Anthropic Managed Agents 的关系

Anthropic 的 `Scaling Managed Agents: Decoupling the brain from the hands` 提出了一个非常有用的工程视角：

```text
brain / harness
≠
hands / execution environment
```

并强调 durable session log 与 execution environment 的解耦。

课程不会复制它的产品拓扑，但会抽象出：

> **推理控制面、持久状态、执行环境可以独立扩展。**

这对生产 Agent 非常重要。

来源：

https://www.anthropic.com/engineering/managed-agents

---

# 18. 常见术语对照

| 术语 | 本课程中的核心含义 |
|---|---|
| Agent | 能根据状态/环境动态行动的任务执行系统 |
| Harness | 围绕模型构建的运行时执行与控制层 |
| Runtime | 实际推进 run/turn/step/tool/state 的执行系统 |
| Orchestrator | 负责任务/角色/步骤编排的控制组件 |
| Workflow Engine | Durable DAG/State Machine/Task Execution |
| Model Adapter | 统一不同模型 Provider 接口 |
| Execution Environment | 命令、文件、浏览器等真正运行的位置 |
| Framework | 帮你实现上述部分能力的软件库 |

这些术语在不同公司可能命名不同。

面试时重点不是：

> “哪个词的定义唯一正确？”

而是：

> **你能否把职责、状态和 failure boundary 讲清楚。**

---

# 19. 高频易错点

⚠️ **Orchestrator = Harness 的完整同义词**  
有重叠，但 Orchestration 更偏控制流和任务编排；Harness 还包含 Context、Tool Protocol、Permission、Compaction、Model Adapter 等。

⚠️ **Backend = Harness**  
Harness 建在 Backend 基础设施上，但有 Model-in-the-loop 的专门语义。

⚠️ **Framework = Runtime Problem**  
框架是实现，不是问题定义。

⚠️ **State 全放 Prompt**  
结构化执行事实应该由 Runtime 保存，不应该只靠自然语言历史。

⚠️ **Permission 和 Sandbox 合并**  
一个是 Policy/Approval，一个是执行环境 Enforcement。

---

# 20. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Model 负责理解和决策，Harness/Runtime 负责把决策放进多步执行系统里，包括 Context、State、Tool、Permission、Checkpoint、Trace 等。Orchestrator/Workflow Engine 更偏任务控制流和 durable execution，普通 Backend 提供 DB、Queue、Auth、Transport 等基础设施。它们可以组合，但责任边界不同。Framework 则只是实现这些 Runtime Primitive 的一种工具。

## Level 2｜2–3 分钟

可以用一次 Tool Call 解释：

> 模型输出 write_file，不应该直接写磁盘。Runtime 要做 schema validation、registry lookup、permission、可能的人审，再在 sandbox 里执行，然后把结果写入 event/state 并组装下一轮 context。如果中途 crash，还要依靠 checkpoint/resume。如果 Tool 已产生副作用，则要考虑 idempotency。所以 Model 只拥有决策，不拥有整个执行语义。

## Level 3｜继续追问

🔍 **Harness 和 Workflow Engine 能不能一起用？**  
可以。Workflow Engine 可负责 Durable Orchestration，某个 Step 内运行 Agent Harness。

🔍 **State 为什么不能全放 messages？**  
因为需要结构化恢复、并发、版本、审计和幂等。

🔍 **Tool Gateway 属于 Harness 还是 Backend？**  
物理上可能是 Backend 服务，逻辑上承担 Harness 的 Capability/Execution Boundary；要按职责解释。

---

# 21. 本章证据

## HUMAN-A

- `AGENT-002` Harness / Runtime / Orchestrator / Workflow Engine：25 个独立来源；
- Related：`AGENT-003` Agent Loop、`AGENT-032` Model Routing、`AGENT-043` Trace。

## Claude Code

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

- `QueryEngine.ts`
- `Tool.ts`
- `Task.ts`
- `utils/sessionStorage.ts`
- `utils/permissions/`

## OpenAI Codex

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

- `codex-rs/core/src/compact.rs`
- `codex-rs/tools/`
- `codex-rs/core/src/tools/router.rs`
- `codex-rs/sandboxing/`
- `codex-rs/rollout-trace/`

## 权威资料

- Anthropic — Building effective agents  
  https://www.anthropic.com/engineering/building-effective-agents
- Anthropic — Scaling Managed Agents: Decoupling the brain from the hands  
  https://www.anthropic.com/engineering/managed-agents
- OpenAI Agents SDK  
  https://openai.github.io/openai-agents-python/

---

# 22. 自测

<details><summary>1. 为什么 Tool 执行属于 Runtime，而不是 Model？</summary>

模型可以产生“调用哪个 Tool、传什么参数”的决策，但真实执行需要 Registry、Schema Validation、Permission、Sandbox、Timeout、Error Normalization、State Update 等软件机制，这些属于 Runtime。
</details>

<details><summary>2. Workflow Engine 和 Agent Harness 能否同时存在？</summary>

可以。Workflow Engine 负责 durable task orchestration，Agent Harness 可以作为其中一个动态执行 Step；反过来，小型 Harness 也可能自己实现轻量 retry/checkpoint。
</details>

<details><summary>3. 为什么 Runtime Event 不等于 Model Message？</summary>

Runtime 要记录完整执行事实，例如 ToolStarted、CheckpointSaved、ApprovalRequested；但模型本轮 Context 只需要其中一部分投影。把两者分开有利于持久化、审计和控制 Context Budget。
</details>

<details><summary>4. 怎么判断一个 Failure 属于哪一层？</summary>

看谁拥有修复它所需的状态和控制权。Schema 错是 Runtime Validation；越权执行是 Permission/Sandbox；MySQL 慢查询是 Data Layer；模型推理错误则要看 Model/Prompt/Context/Eval。
</details>
