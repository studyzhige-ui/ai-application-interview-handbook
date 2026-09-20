# DeerFlow 2.0｜从 Middleware Runtime 理解一个 Super Agent Harness

[← 成熟产品源码学习](../README.md) · [Agent 模块](../../README.md)

> **源码仓库：** [bytedance/deer-flow](https://github.com/bytedance/deer-flow)  
> **固定源码快照：** [`1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe`](https://github.com/bytedance/deer-flow/tree/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe)  
> **产品代际：** DeerFlow 2.0。仓库 README 明确说明 2.0 是 ground-up rewrite（完全重写），与 1.x 不共享实现；1.x 另在 `main-1.x` 维护。  
> **核验日期：** 2026-09-20

DeerFlow 2.0 自己把产品称为 **super agent harness（超级智能体运行框架）**，并把 Sub-Agent、Memory、Sandbox、Skills、Context Engineering 都放在核心能力里。

但如果只看 README，很容易把它理解成：

~~~text
LangGraph
+ 一些 Tool
+ Memory
+ Subagent
~~~

源码真正有价值的地方不是这些功能“有没有”，而是它们怎样一起进入一条产品运行链。

当前 2.0 的核心更接近：

~~~text
Gateway Run / Thread
        ↓
LangGraph Checkpoint State
        ↓
langchain.create_agent
        ↓
DeerFlow Middleware Chain
        ↓
Model Call ↔ Tool Call
        ↓
Sandbox / MCP / Skills / Memory / Subagent
        ↓
Checkpoint State + Run Journal
        ↓
SSE / History / Resume / Replay
~~~

因此这组文档不会先把 DeerFlow 按通用课程切成 Context / Memory / Tool，然后去源码里找同名文件。

正确顺序是：

> **先还原 DeerFlow 一次真实 Run 是怎样被组装、执行、持久化和恢复的；再从这条运行链中分别抽出 Context、Memory、Tool 和 Engineering 生命周期。**

---

## 1. 先建立 DeerFlow 自己的产品心智模型

### Gateway 是默认产品运行入口，不是裸 LangGraph Server

DeerFlow 2.0 后端架构文档把 Gateway 作为默认部署入口。

大体链路是：

~~~text
Frontend / API Client
        ↓
Gateway
  Thread / Run / Auth / SSE
        ↓
Run Worker
        ↓
assemble_lead_agent()
        ↓
LangGraph compiled graph
        ↓
Agent + Middleware
~~~

`langgraph.json` 仍然存在，可以服务 LangGraph Studio / 直接 LangGraph Server 等场景；但完整产品默认通过 Gateway 的 Thread / Run API 工作。

这点很重要，因为有些状态并不只存在于 LangGraph graph：

- Gateway Run Row；
- Run Event Store；
- Thread metadata；
- Project snapshot；
- Authenticated user identity；
- Run cancellation / rollback；
- Workspace diff；
- Delivery receipt。

所以“理解 DeerFlow”不能只读 Agent Graph。

### Lead Agent 最终仍然建立在 `langchain.create_agent`

源码的两个重要构造入口是：

- `backend/packages/harness/deerflow/agents/factory.py::create_deerflow_agent`
- `backend/packages/harness/deerflow/agents/lead_agent/agent.py::make_lead_agent / assemble_lead_agent`

底层最终调用：

`langchain.create_agent(...)`

DeerFlow 的差异不在于另写了一套模型循环，而在于：

> **用大量 Middleware、ThreadState、自定义 Tool、Sandbox、Subagent Runtime 和 Gateway 运行层，把 LangChain / LangGraph 的基础 Agent 变成产品级 Harness。**

---

### 真正的“Runtime”主要藏在 Middleware Chain 里

当前 Lead Agent 的 Middleware 数量很多，而且顺序本身就是协议。

不要背 30 多个名字。

先把它们按问题分组：

~~~text
输入与远端内容安全
Input Sanitization
Tool Result Sanitization
PII Redaction

Context 与状态
Thread Data
Uploads
Dynamic Context
Durable Context
Summarization
System Message Coalescing

执行与权限
Sandbox
Authorization / Guardrail
Sandbox Audit
Read Before Write

Tool 可靠性
Dangling Tool Call
Tool Error Handling
Tool Progress
Tool Receipt
Tool Output Budget

Skills / Deferred Tools
Skill Activation
Skill Tool Policy
MCP Routing
Deferred Tool Filter
Tool Promotion Audit

Agent 控制
Subagent Limit
Loop Detection
Token Budget
Todo / Title / Clarification

长期 Memory
Memory Middleware
~~~

同一个 Tool Call 会穿过其中多个层。

所以 DeerFlow 的 Agent System Design（智能体系统设计）首先是：

> **Middleware Composition（中间件组合）。**

---

## 2. 一次真实用户请求怎样跑完整条链

假设用户说：

> “分析这个仓库的支付故障，必要时调用监控 MCP；记住我不希望先做大重构。”

### Run Admission

Gateway 创建一个 Run。

这里会固定本次运行的一些 Server-owned Context（服务端拥有的上下文），例如：

- `thread_id`
- `run_id`
- effective user identity；
- Project Snapshot；
- Extensions Snapshot；
- Auth / Authorization Context。

客户端不能随便伪造这些保留字段。

### Agent Assembly

Run Worker 调用 Lead Agent factory。

这一步会解析：

-模型；
-thinking / reasoning；
-Custom Agent；
-Memory 是否启用；
-Subagent 是否启用；
-Skills；
-Tools；
-MCP；
-Authorization；
-Summarization；
-Token / Loop limits。

然后得到一份：

`LeadAgentAssembly`

其中不仅有 compiled graph，还有可选 Assembly Descriptor（组装描述符），用于描述：

-实际模型；
-Prompt hash；
-Tool schemas；
-Middleware 顺序；
-Deferred tools；
-enabled skills；
-effective policies。

也就是说，DeerFlow 会显式记录：

> **这一条运行实际组装出了什么 Agent。**

---

### Before Agent：先准备当前 Thread 的运行环境

Middleware 开始工作。

例如：

- ThreadDataMiddleware 创建当前用户 / Thread 的文件目录；
- SandboxMiddleware 获取或复用 Sandbox；
- DynamicContextMiddleware 处理日期和 Memory；
- UploadsMiddleware 处理本轮新上传文件。

这时还不是简单“把消息发给模型”。

Runtime 先把当前物理环境和上下文准备好。

---

### Model Request：不同 Context 有不同持久化语义

进入模型调用前，多个 Middleware 会重新构造真正的 `ModelRequest`。

例如：

- Project Context 是 request-only transient（仅当前请求临时存在）；
- View Image 的 base64 也是 request-only；
- Memory 可以被注入成隐藏 HumanMessage；
- `summary_text` 不直接存在于 `messages`，由 DurableContext 动态投影；
- Delegation ledger 和 Skill Context 也由 DurableContext 投影；
- Deferred MCP Tool 尚未 promoted 时，schema 会被 DeferredToolFilter 移除；
- Skill Policy 会进一步过滤当前 Tool Schema；
- SystemMessageCoalescing 最后把多个 SystemMessage 合并成一个 leading SystemMessage。

所以 DeerFlow 的 Context 不是：

~~~text
ThreadState.messages
~~~

而是：

> **ThreadState + Runtime Context + Middleware projection 共同生成的 ModelRequest。**

---

### Model 选择 Tool

假设模型需要监控 MCP。

如果这个 MCP Tool 是 Deferred（延迟暴露）的：

1. `McpRoutingMiddleware` 可能根据用户问题里的 routing hints 自动 promote；
2.否则模型先调用 `tool_search`；
3. promotion 写进 `ThreadState.promoted`；
4. 下一次 Model Call 才能看到完整 Tool Schema。

但 promotion 不等于授权。

`SkillToolPolicyMiddleware` 和 Authorization / Guardrail 仍然可以把这个 Tool 从 schema 或执行阶段拒绝。

---

### Tool Execution

真正 Tool Call 又会经过一条执行 Middleware 链。

例如文件写入：

~~~text
Tool Call
→ Authorization
→ Guardrail
→ Sandbox Audit
→ Read Before Write
→ Tool Progress
→ Tool Error Handling
→ Tool body
→ Tool Receipt
→ ToolMessage
~~~

如果结果很大：

`ToolOutputBudgetMiddleware`

可以只在模型请求里替换为短 synopsis + `read_file` reference。

原始 state / journal 仍可保留真实结果。

---

### Memory 更新

这次 Run 完成以后，如果使用默认：

`memory.mode: middleware`

`MemoryMiddleware.after_agent`

会把 conversation 交给 Memory Manager。

默认 DeerMem：

1.过滤为真正 User + final Assistant；
2.去掉 trivial acknowledgement；
3.检测 correction / reinforcement 等 signal；
4.进入 debounce queue；
5.后台调用 Memory Updater；
6.由 LLM 提取长期信息；
7.再经过 deterministic scope gate；
8.成功后写入长期 Memory。

这条 Memory 更新不是主 Agent Run 的同步成功条件。

---

### Persistence 与 Debug

与此同时：

- LangGraph Checkpointer 保存 Thread State；
- RunJournal 把执行证据写入 RunEventStore；
- Gateway Run Row 维护 Run lifecycle；
- Workspace scanner 可以记录输出文件变化；
- SSE 把 live stream 发给前端。

所以一条 DeerFlow Run 有至少两条不同的“历史”：

~~~text
LangGraph Checkpoint
用于恢复 Agent State

Run Journal
用于产品历史、调试、审计、UI 事件
~~~

这两者不能混成同一个 Persistence。

---

## 3. 五份文档分别追什么

### [01｜Context Lifecycle](01-context-lifecycle.md)

这篇不会只讲 Summarization，而是追一条模型请求从 Thread State 到最终 Provider Payload 的全过程：

- Gateway 怎样固定当前 Run Context；
- Static Prompt 和 Dynamic Context 为什么分开；
- Memory 为什么保持 user-role，而不是提升成 System；
- Project Context / View Image 为什么只存在于 request，不进入 checkpoint；
- `ThreadState.summary_text`、`delegations`、`skill_context` 为什么独立于 `messages`；
- DurableContext 怎样每轮重新投影；
- ToolOutputBudget 怎样先处理大 Tool Result；
- Summarization 怎样在 Context 压力下写 `summary_text`；
- Context 被压缩前为什么必须先 flush Memory；
- Checkpoint / Branch / Regenerate 怎样影响未来 Context。

### [02｜Memory Lifecycle](02-memory-lifecycle.md)

DeerFlow 当前确实有完整内建长期 Memory。

会连续追：

~~~text
Conversation
→ MemoryMiddleware
→ DeerMem preprocessing
→ Debounce Queue
→ Memory Updater LLM
→ deterministic scope / durability / authority gate
→ fact / summary persistence
→ Context injection / memory_search
→ correction / reinforcement
→ capacity / dedup / staleness / consolidation
→ clear / shutdown / migration
~~~

还会区分：

- 默认 Middleware Mode；
-显式 Tool Mode；
-DeerMem；
-Mem0 / OpenViking / Honcho 等可替换 Backend；
-user / agent scope。

---

### [03｜Tool Lifecycle](03-tool-lifecycle.md)

重点回答：

- `get_available_tools()` 怎样把 config / builtin / MCP / ACP / Subagent / Memory tools 合起来；
- Tool 名冲突怎样处理；
- Deferred MCP Tool 怎样只公开 metadata，不立刻塞完整 schema；
- `tool_search` 和 auto routing 怎样 promote；
-为什么 promotion 后还要经过 Skill Policy / Authorization；
-Skill 的 `allowed-tools` 怎样同时限制 schema 和 execution；
-Sandbox / Read-before-write / Guardrail / Receipt / Error Handling 怎样串在同一次 Tool Call；
-超大 Tool Result 怎样 externalize；
-MCP Session Pool / reconnect / output file mapping；
-大量 Tool / Skill 下怎样避免 Context 爆炸。

---

### [04｜Engineering & Evaluation](04-engineering-evaluation.md)

把长期运行和多 Agent 放回来：

- Gateway Run、LangGraph Checkpoint、Run Journal 分别是什么；
- interrupted Tool Call 怎样被 DanglingToolCallMiddleware 修复；
- LLM Error、Loop、Token limit、Safety finish 怎样分别停止；
- Branch / Regenerate 为什么必须沿 Checkpoint lineage；
-为什么旧 Turn branch 不能继承未来 Workspace 文件；
- Subagent 为什么使用 `checkpointer=False`；
- Parent Context Snapshot 怎样把历史降权成 untrusted data；
- Subagent capacity / per-run delegation cap；
- Sandbox Lease / provider / cross-instance ownership；
-测试怎样覆盖 Middleware order、Memory isolation、Replay、Run Event contract、Checkpoint mode、Subagent lineage。

---

## 4. 源码覆盖矩阵

| 系统边界 | 主要源码 | 当前快照中确认的职责 |
|---|---|---|
| 产品入口 | `backend/app/gateway/` | Thread / Run API、Auth、SSE、Replay、Artifacts |
| Agent factory | `agents/factory.py`、`agents/lead_agent/agent.py` | LangGraph Agent 创建、Tool / Middleware / Model 组装 |
| Agent state | `agents/thread_state.py` | messages、summary、delegations、skill context、promotion 等 Thread 状态 |
| Middleware chain | `agents/middlewares/` | Context、Tool、Safety、Memory、Skill、Recovery 核心运行时 |
| Dynamic Context | `dynamic_context_middleware.py` | 日期、Memory、Project Context 注入 |
| Durable Context | `durable_context_middleware.py` | summary / delegation / skill context 捕获与投影 |
| Summarization | `summarization_middleware.py` | Context compaction、summary_text、手动 / 自动压缩 |
| Tool Output Budget | `tool_output_budget_middleware.py` | 大 Tool Result externalization / model-view elision |
| Memory contract | `agents/memory/manager.py` | Pluggable MemoryManager |
| Default Memory | `agents/memory/backends/deermem/` | 文件事实、LLM extraction、retrieval、maintenance |
| Memory write | `memory_middleware.py`、`summarization_hook.py` | 普通异步更新 + compact 前 emergency flush |
| Memory tools | `agents/memory/tools.py` | search / add / update / delete |
| Tool assembly | `tools/tools.py` | config / builtin / MCP / ACP / Subagent 工具汇合 |
| Deferred Tools | `tools/builtins/tool_search.py` | MCP catalog、promotion、Tool Search |
| MCP | `mcp/` | Tool discovery、session pool、OAuth/interceptor、reconnect |
| Skills | `skills/` + Skill middlewares | SKILL.md、activation、allowed-tools、projection |
| Authorization | `authz/` + Guardrail middleware | assembly-time + execution-time capability checks |
| Sandbox | `sandbox/` | provider、lease、filesystem、network approval、skill projection |
| Subagents | `subagents/` | one-shot delegation、context snapshot、capacity、step events |
| Checkpoint | `runtime/checkpointer/` | LangGraph Thread State persistence |
| Run lifecycle | `runtime/runs/` | Run execution、cancel、rollback、finalization |
| Run Journal | `runtime/journal.py` + `runtime/events/` | append-only product execution evidence |
| Replay / Branch | Gateway checkpoint lineage + replay docs | branch、regenerate、edit replay |
| Tests | `backend/tests/` + frontend replay E2E | Middleware order、state、Memory、Sandbox、Run/Replay contracts |

---

## 5. 和前三个产品横向比较时，最值得抓住什么

### Context：DeerFlow 把“持久状态”和“请求时投影”分得很细

Codex 更强调 typed fragments、World State 和 Context Window。

Claude Code 更强调 query-loop 内多层 Context slimming。

DeepSeek Harness 更强调 Event Log → Surface Projection。

DeerFlow 则大量使用：

> **LangGraph ThreadState + request-time Middleware projection。**

例如：

- `summary_text` 持久，但不在 messages；
-Project Context request-only，不持久；
-Image base64 request-only；
-Memory 既可能成为 checkpointed hidden HumanMessage，也可能按配置关闭；
-Tool Result 原始内容可以留在 state，而模型只看 elided / externalized 版本。

---

### Memory：DeerFlow 是这四个产品里最显式的“可插拔 Memory Product”

当前源码不是一个简单 vector store。

它把：

~~~text
Write Policy
Storage
Extraction
Retrieval
Injection
CRUD
Eviction
Staleness
Consolidation
User / Agent Isolation
Remote Backend
~~~

都做成了真正的长期 Memory 子系统。

而且默认 DeerMem 仍然只是 `MemoryManager` 的一个 Backend。

---

### Tool：真正的核心不是 Tool Registry，而是 Middleware Policy Stack

DeerFlow 的 Tool Call 会被多层 wrapper 改写、拦截、审计和证明。

尤其值得学的是：

> **Schema visibility 和 Execution permission 都必须检查。**

Deferred Tool 即使被 `tool_search` promote，Skill Policy 仍然可以阻止它的 schema 和 execution。

---

### Engineering：Checkpoint 和 Journal 是两条不同事实通道

LangGraph Checkpoint 回答：

> Agent 下一步怎么继续。

Run Journal 回答：

> 这次 Run 到底发生了什么。

把两个问题拆开以后：

- UI History；
-Debug；
-Audit；
-Replay；
-State Recovery；

不必全部依赖同一份存储结构。

---

## 6. 推荐阅读顺序

~~~text
README
先建立 Gateway → LangGraph → Middleware → Persistence 的产品图

01 Context
理解“每次模型真正看到什么”

02 Memory
理解长期信息怎样写、存、取、纠正和维护

03 Tool
理解能力怎样发现、授权、执行和缩放

04 Engineering & Evaluation
理解 Checkpoint / Journal / Sandbox / Subagent / Recovery / Tests
~~~

读完以后，应该能直接回答：

1. DeerFlow 为什么不是“一个 LangGraph workflow”这么简单？
2. 为什么它要维护 `summary_text`，却不把 summary 直接写回 messages？
3. Memory 为什么以 HumanMessage 注入，而日期用 SystemMessage？
4. Project Context 为什么不进 Checkpoint？
5. Summarization 前为什么要先 emergency flush Memory？
6. 默认 DeerMem 怎样从 conversation 变成 durable fact？
7. Middleware Mode 和 Tool Mode 的 Memory 有什么根本区别？
8. `tool_search` promote 以后为什么还不能直接执行 MCP Tool？
9. Skill `allowed-tools` 为什么同时作用于 Tool Schema 和 Tool Execution？
10. Sandbox Audit 和真正 Sandbox Boundary 有什么区别？
11. Parent Conversation 为什么不能原样塞给 Subagent？
12. LangGraph Checkpoint 和 Run Journal 为什么必须分开？
13. Branch 老 Turn 时为什么不能复制当前 Workspace？
14. 怎样用 Replay E2E 防止“前后端单测都绿，但产品历史顺序错了”？

下一篇：[Context Lifecycle →](01-context-lifecycle.md)
