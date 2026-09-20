# 03. Codex Tool Lifecycle｜注册、发现、MCP / Skills、权限、执行与回填

[← Memory](02-memory-lifecycle.md) · [Codex 总览](README.md) · [Engineering & Evaluation →](04-engineering-evaluation.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

Codex 的 Tool 系统不是：

```python
tools = {
    "bash": bash,
    "read_file": read_file,
}
```

而是一条从“Host 有什么能力”到“某一次模型请求究竟能看到什么、调用后究竟允许执行什么”的完整生命周期：

```text
Tool implementation
↓
Tool contract / spec / runtime
↓
Registration
  built-in / MCP / extension / dynamic / hosted
↓
AllowedTools / policy / collision
↓
Exposure planning
  Direct
  Deferred
  DeferredModelOnly
  DirectModelOnly
  CodeModeOnly
  Hidden
↓
Step-specific ToolRouter
↓
model-visible tool specs
  + tool_search
  + Code Mode definitions
↓
Model tool call
↓
parse / normalize call
↓
payload type validation
↓
pre-tool hooks / optional input rewrite
↓
readiness
↓
approval / Guardian
↓
permission profile / network policy
↓
sandbox selection
↓
parallel / serial admission
↓
handler execution
↓
retry / escalation where allowed
↓
post-tool hooks
↓
normalize ToolOutput
↓
canonical call/output pair
↓
append history
↓
next model sampling
```

只有把这条链走完，才算真正理解 Codex Tool Runtime。

---

## 1. 先分清四个对象：Spec、Runtime、Registry、Router

### Tool Spec

给模型看的能力契约，例如：

- name；
- description；
- input schema；
- output schema；
- namespace；
- deferred-loading metadata。

### Tool Runtime / Executor

Host 内真正可执行的实现。

共享 `ToolExecutor` contract 负责：

- `tool_name()`；
- `spec()`；
- preferred exposure；
- search metadata；
- parallel support；
- `handle()`。

Core 再通过 `CoreToolRuntime` 增加 Codex 特有能力，例如：

- immutable spec；
- Code Mode definitions；
- readiness future；
- MCP server identity；
- payload matching；
- telemetry tags；
- result accepted callback；
- pre/post hook payload；
- hook input rewrite；
- streamed argument diff consumer。

### Tool Registry

当前 Step 可调度能力的完整注册目录。

它知道：

```text
name
→ executable runtime
→ exposure
```

但 Registry 中存在的工具**不等于**模型当前一定可见。

### Tool Router

`ToolRouter` 是当前 Step 已经 finalize 的执行计划：

```text
registry
+
model-visible specs
+
ToolMode
+
Code Mode names
+
namespace metadata
```

模型这一轮看到的是 Router 的投影，不是整个 Registry。

---

## 2. 为什么 Registry 和 Model-visible Set 必须分开

假设 Host 一共拥有：

```text
20 built-ins
+ 3,000 MCP tools
+ 5,000 app tools
+ 1,000 dynamic tools
+ 2,000 skills-related tools
```

如果：

```text
registered = model-visible
```

就会直接得到：

- Prompt / request 膨胀；
- Tool 选择混乱；
- Schema namespace 冲突；
- Prompt Cache prefix 变化；
- 安全能力过度暴露；
- 每个 Step 构造成本过高。

Codex 所以显式建模“暴露面”。

---

## 3. ToolExposure：一个工具可以存在，但不一定直接出现

当前共享 `codex-tools` 中的 `ToolExposure` 有：

### `Direct`

初始模型 Tool List 直接可见；启用 Code Mode 时也可在嵌套代码工具面使用。

### `Deferred`

不进入初始 Tool List。

可以通过 `tool_search` 发现，同时可参与 Code Mode。

### `DeferredModelOnly`

可被 Tool Search 发现，但不允许嵌套 Code Mode 使用。

### `DirectModelOnly`

只作为普通模型工具直接可见，不进入嵌套 Code Mode。

### `CodeModeOnly`

只允许 Code Mode 内部调用。

### `Hidden`

仍保留在 Host Registry，可用于内部 dispatch / runtime 逻辑，但不对模型暴露。

因此工具暴露不再是：

```text
visible = true / false
```

而是：

> **在哪一种模型交互 Surface 上可见。**

---

## 4. 一个 Step 的 ToolRouter 怎样构造

`core/src/tools/spec_plan.rs::build_tool_router` 是核心入口。

当前顺序大体是：

```text
1. register core tools
↓
2. append MCP tools
↓
3. apply MCP exposure policy
↓
4. append extension executors
↓
5. append dynamic tools
↓
6. append hosted model tool specs
↓
7. finalize_tool_router
```

Finalize 还会：

- 应用 `AllowedTools`；
- 确定 effective ToolMode；
-处理 direct / deferred / Code Mode；
-安装 `tool_search`；
-生成 namespace inventory；
-做 collision 检查；
-构造最终 `model_visible_specs`。

所以 Tool List 是**每个 Step 根据当前状态编译出来的**。

---

## 5. Tool Registration 为什么还要区分 Trusted / External

Registry 有 trusted 与 external registration。

External tool 不能随意覆盖保留能力。

当前源码会保护例如：

- `exec_command`
- `shell_command`

如果外部 MCP / extension 注册同名危险能力：

```text
external tool
name = exec_command
↓
不能静默覆盖 core executable
```

外部 duplicate：

- 默认可以记录 collision 并跳过；
-配置可以把 collision 升级为 hard error。

这解决典型 supply-chain 问题：

> **能力接入系统不能把“名字相同”当成“语义相同”。**

---

## 6. AllowedTools 是执行面，不只是 Prompt Filter

`AllowedTools` 在 Registry / final planning 中都参与过滤。

为什么不能只：

```text
从 prompt 里删掉不允许的工具
```

因为模型可能：

-历史里已经知道名字；
-被 prompt injection 诱导；
-通过 malformed call 猜名字；
-从其他 channel 得到工具名。

安全边界必须是：

```text
model visibility filter
+
runtime dispatch allowlist
```

而不是只靠“模型看不见”。

---

## 7. MCP 从 Server Tool 到 Codex Runtime 要经过哪些步骤

MCP Server 返回 tool catalog 之后，不会自动成为模型工具。

Codex 会先形成 `McpBinding` / `ToolInfo`，再由 `McpHandlerCache` 和 Tool Registry 接入。

生命周期：

```text
MCP server configured
↓
server startup / initialize
↓
list tools / refresh catalog
↓
ToolInfo
  server_name
  callable namespace
  description
  schema
  connector metadata
  annotations
↓
build McpHandler
↓
policy filter
↓
ToolExposure
↓
register external tool
↓
ToolRouter
```

Tool call 真正发生时：

```text
McpHandler
↓
wait_for_mcp_server
↓
prepare executed binding
↓
pre-tool hooks
↓
call MCP
↓
normalize result / truncation
↓
post hooks
↓
history
```

---

## 8. MCP Handler 为什么要绑定“执行时的 catalog snapshot”

MCP catalog 可能在 Session 中刷新。

假设：

```text
Step 1 模型看到 calendar.create_event v1
↓
Server catalog refresh 到 v2
↓
Step 1 call 现在才执行
```

不能让执行资格和 metadata 自动漂到 v2。

MCP handler / executed call 会尽量使用：

> **产生这次 call 时已经准备好的 binding / StepContext。**

这和整个 Tool Runtime 的 Step consistency 是同一个原则。

---

## 9. Apps / Connector Tool 还要额外做 Policy

Codex Apps MCP tools 与普通 MCP tools并不完全一样。

进入 Registry 前还会看：

- connector ID；
-配置 layer；
-tool name / title；
- `destructive_hint`；
- `open_world_hint`。

`AppToolPolicyEvaluator` 决定这个 App Tool 是否 enabled。

所以：

```text
MCP Server 说“我有这个 Tool”
≠
Codex 必须暴露它
```

Host 仍然拥有最终政策权。

---

## 10. 大量 MCP Tool 为什么不会全部塞进 Prompt

当前源码最直接的规模化设计：

如果 Tool Search 开启：

```text
MCP tools
→ default ToolExposure::Deferred
```

否则才默认：

```text
Direct
```

Deferred 意味着：

```text
Registry 里有
↓
初始 model-visible list 不展开
↓
tool_search 可查
↓
命中后把 LoadableToolSpec 返回给模型
```

这就是 Codex 对“大量工具”的主要答案之一。

---

## 11. Tool Search 不是向量数据库，而是当前源码中的 BM25

`handlers/tool_search.rs` 当前使用 BM25 Search Engine。

建立索引时：

```text
deferred tools
↓
ToolSearchInfo.search_text
↓
BM25 documents
↓
SearchEngine
```

一次 call：

```text
tool_search(query, limit)
↓
BM25 search
↓
匹配 ToolSearchEntry
↓
coalesce namespace specs
↓
返回 LoadableToolSpec
```

对 MCP，search text 会组合：

- flattened canonical tool name；
- callable name；
-server name；
-title；
-description；
-connector name；
-namespace description；
-plugin display names；
-schema property names。

所以 Tool Discovery 不是只搜 description。

---

## 12. 为什么 ToolSearchHandler 还要 Cache

每个 Step 都可能 rebuild ToolRouter。

如果每次都：

```text
几千 deferred tools
→ 重建 BM25
```

会产生无意义 CPU 成本。

`ToolSearchHandlerCache` 会区分：

### Immutable Runtime

通过 `Weak<dyn CoreToolRuntime>` identity 判断能否复用。

### Dynamic Tool

比较 `ToolSearchInfo` 内容。

只有：

- source listing 改变；
-runtime identity 改变；
-dynamic metadata 改变；

才需要重新构造 search handler。

这是一种：

> **catalog cache，而不是模型 Prompt Cache。**

---

## 13. 数万个工具还要做 Spec Budget，而不只是 Deferred

Agent-plugin MCP Tool 有非常明确的硬预算：

```text
单个 MCP model spec
<= 8,000 bytes

同类累计 model specs
<= 64,000 bytes
```

超过预算：

```text
ToolExposure::Hidden
```

不是“反正 Context Window 很大，再塞一点”。

这与根 `AGENTS.md` 的 model-context hard cap 原则一致。

规模化工具系统至少需要：

```text
catalog scale
+
discovery scale
+
model-visible spec scale
+
runtime dispatch scale
```

Deferred 只解决其中一部分。

---

## 14. Tool Search 能否解决 50,000 Tools？

它解决的是：

> **不要把 50,000 个完整 schema 全放入第一轮请求。**

但如果真实达到 50,000，还要继续考虑：

### Search Quality

BM25 搜索文本是否能正确命中？

### Namespace Hierarchy

能否先选 server / app / domain，再选具体 Tool？

### Candidate Limit

单次 `tool_search` 返回多少？

### Tool Similarity

大量同义名字会不会产生错误选择？

### Tenant / Policy Pre-filter

无权使用的 Tool 不应该进入搜索候选。

### Catalog Refresh Cost

动态 Tool metadata 变化会导致 search cache rebuild。

### Evaluation

必须测：

```text
discovery recall@k
selection precision
schema-load count
tool-search latency
wrong-tool rate
```

所以 Codex 已经给了正确架构骨架：

```text
Full Registry
→ filtered catalog
→ deferred retrieval
→ small model-visible candidate set
```

未来规模再大，主要扩展 search / routing，而不是退回“全部注入”。

---

## 15. Skills 和 Tool 的关系：Skill 不是另一个函数 Schema

Codex 的 Skills Extension 同时参与：

- Thread lifecycle；
- Config；
- Context；
- World State；
- Tool contribution；
- Skill invocation；
- Turn input。

Skill 的关键不是直接等于 Tool。

Skill 更像：

> **带选择说明、操作知识和 supporting resources 的能力包。**

它可能进一步告诉模型：

-什么时候使用某工具；
-怎样组合步骤；
-参考哪些文件；
-运行哪些脚本。

---

## 16. Skills 的 Progressive Disclosure

Codex 自带 skill-creator sample 明确采用分层加载：

```text
第 1 层
skill name + description
→ 用于发现

第 2 层
SKILL.md
→ Skill 真正被选中时加载

第 3 层
references / scripts / assets
→ 只有执行中需要时再读取或运行
```

为什么脚本很重要？

因为：

```text
运行一个 300 行 Python helper
≠
把 300 行 Python 全塞进模型 Context
```

这使 Skills 具备：

> **可执行但不必全部 model-visible。**

---

## 17. Skills Catalog 也有独立 Context Budget

`ext/skills/src/render.rs` 当前明确限制：

- 默认 metadata char budget：8,000 chars；
- 配置的 token budget 最高 10,000 tokens；
- 如果根据模型 Context Window 自动计算，则约取可用窗口的 2%；
- 单 Skill prompt bytes 也受硬限制；
-单条 description 有字符上限。

预算不够时：

### 能放所有 Skill

保留完整 description。

### 能放所有名字，但 description 太长

对 description 做公平分配 / truncation。

### 连名字都放不下

后面的 Skill 整条 omitted。

而且源码不是把剩余预算全给第一个 Skill，而是 round-robin 分 description chars，避免单个 Skill 吃掉全部空间。

---

## 18. Skills Budget 是可观测的

Codex 会记录：

- total enabled skills；
-kept skills；
-whether truncated；
-truncated description chars；
-catalog surface。

Catalog Surface 还区分：

- thread context；
-executor world state；
-orchestrator world state；
-host world state；
-turn input。

所以“Skill 太多导致效果差”可以从 telemetry 先确认：

> 到底有多少 Skill 被截掉了？

---

## 19. Tool Call 从模型输出怎样被解析

`ToolRouter::build_tool_call` 会把 Responses API 不同 call 类型统一成内部 ToolCall，例如：

- FunctionCall；
- ToolSearchCall；
- CustomToolCall。

统一对象包含：

```text
tool_name
call_id
ToolPayload
encrypted args（如有）
source
```

然后再 dispatch。

所以 Handler 不应该自己理解所有 Provider 原始 response shape。

---

## 20. Payload Validation 有两层

### 协议 /类型层

Router / Registry 先检查：

- call type；
-tool name；
-payload kind；
-arguments encoding。

例如：

```text
tool_search handler
收到 Function payload
→ Fatal / protocol mismatch
```

### 业务语义层

具体 handler 再验证：

-参数；
-path；
-command；
-server；
-environment；
-policy。

Tool Schema 只能解决第一部分。

---

## 21. PreToolUse Hook 能做什么

Registry dispatch 在真正 handler 前可以调用 hook。

Hook 能：

-观察 tool name / input；
-block；
-返回修改后的 input；
-记录审计。

Tool runtime 还可以实现 `with_updated_hook_input`。

MCP Handler 就支持把 hook 改写后的 JSON 再序列化为新的 MCP arguments。

所以 Hook 是真正的 runtime interception point，不只是日志回调。

---

## 22. Hook Input Rewrite 为什么必须重新校验

假设原模型生成：

```json
{"path": "a.txt"}
```

Hook 改成：

```json
{"path": "../../etc/passwd"}
```

如果：

```text
原参数校验通过
→ hook rewrite
→ 直接执行
```

就会绕过安全边界。

成熟 Tool Runtime 应把：

> **rewrite 后 payload 当成新的执行输入。**

Codex 的 runtime contract把 rewrite 显式建模，也就能在后续 handler / policy 中重新解释它。

---

## 23. Tool Readiness：注册存在不代表现在能执行

MCP Runtime 可能还在启动。

`CoreToolRuntime::wait_until_ready` 允许 runtime 暴露 readiness future。

`McpHandler` 会等待：

`session.wait_for_mcp_server(server_name)`

再真正执行。

因此：

```text
registered
≠
ready
```

但模型可以在 Step 中看到某能力时，Runtime 应保证最终执行对 readiness 有明确等待 / 失败语义。

---

## 24. Approval、Permission、Sandbox 是 Tool Execution 的中段

Tool 解析正确以后还不能直接执行。

`core/src/tools/orchestrator.rs` 把核心流程写成：

```text
approval
→ sandbox selection
→ attempt
→ sandbox-denial retry / escalation
```

这是 Tool 生命周期里最容易被初学者漏掉的一段。

---

## 25. Approval Policy 怎样决定是否问用户

Tool Runtime 会结合：

-当前 approval policy；
-tool requirement；
-Guardian / strict review；
-network need；
-sandbox constraint；
-previous approval cache；

得到类似：

```text
Skip
Forbidden
NeedsApproval
```

不是所有副作用 Tool 都简单：

> “每次弹一次 Yes / No”。

还要避免相同安全事实重复打扰用户。

---

## 26. Guardian 和普通 Approval 有什么区别

普通 approval 主要问：

> 用户是否授权这次能力。

Guardian / auto review 更像：

> 即使普通规则认为可以执行，是否还需要额外风险审查。

因此安全层级可能是：

```text
Model chose tool
↓
Tool contract valid
↓
Approval policy
↓
Guardian review
↓
Permission profile
↓
Sandbox / network enforcement
```

每层解决的问题不同。

---

## 27. Sandbox 为什么要在执行前动态选择

不同 Tool / Command 可能需要：

-只读 filesystem；
-workspace write；
-更宽本地访问；
-network；
-unsandboxed retry。

Orchestrator 根据：

- PermissionProfile；
- file-system sandbox policy；
- workspace roots；
-network policy；
-platform sandbox；

选择执行环境。

这比给整个 Agent 一个固定：

```text
sandbox=true
```

细得多。

---

## 28. Sandbox Denied 后为什么有时可以重试

第一次执行可能因为 sandbox 拒绝。

但：

```text
sandbox denied
≠
命令本身一定非法
```

可能是：

> 这项合法任务需要更高权限。

所以 Orchestrator 会判断：

-是否允许 escalation；
-approval policy；
-network approval；
-unsandboxed 是否可用；
-是否需要再次用户确认。

然后决定：

```text
deny final
or
ask approval
→ retry with escalated environment
```

这是“有限恢复”，不是无限重试。

---

## 29. Network Permission 为什么单独管理

网络是 Agent 最大副作用之一。

Codex 还可能使用 managed network proxy / policy decider。

因此网络安全不应该只靠：

```text
shell command 里有没有 curl
```

更合理：

```text
tool requirement
+
permission profile
+
managed network policy
+
runtime observation
```

这样 MCP / App / shell 等不同能力可以共享网络治理。

---

## 30. 并发 Tool Call 怎样保证不会互相踩

`ToolCallRuntime` 每个 Step 共享一个 `RwLock`。

逻辑：

### Tool 支持 parallel

获取 read lock。

多个 parallel-safe Tool 可以并发。

### Tool 不支持 parallel

获取 write lock。

它会等待其他并发调用结束，并阻止新的并发 Tool 进入。

因此：

```text
supports_parallel_tool_calls
```

不是只发给模型看的提示，而会改变真实 dispatch admission。

---

## 31. 为什么 Tool Call 要记住 StepContext

Tool Call 可能在模型 stream 完成后才被收集 / 执行。

如果后面 Step 已经更新：

- tool catalog；
-permission；
-model；
-environment；

旧 Tool Call 仍应该按照：

> **产生它时模型所看到的 Step。**

所以 `ToolCallRuntime` 保留 `Arc<StepContext>`。

这是避免 Time-of-check / Time-of-use 漂移的重要手段。

---

## 32. Tool Cancellation 怎样工作

每次 Tool Call 有 cancellation token。

执行任务被 `AbortOnDropHandle` 包住。

取消时：

### 已进入 terminal outcome / 已结束

等待正常结果。

### 仍可中止

```text
record aborted
↓
abort task
↓
生成结构化 AbortedToolOutput
↓
notify_tool_aborted
↓
产生 model-visible tool result
```

例如 `exec_command` 会把 wall time 和 “aborted by user” 变成输出。

为什么要生成 output？

因为历史里已经有：

```text
tool call(call_id)
```

如果取消后什么都不写，下一次模型请求就出现 dangling call。

---

## 33. Tool Failure 为什么分 Fatal 和 RespondToModel

`FunctionCallError` 不是所有错误都等价。

### RespondToModel

代表：

> 这次 Tool Call 失败，但 Agent Loop 可以继续，让模型看到错误并修正。

例如：

-参数非法；
-path 不存在；
-memory query empty；
-Tool 业务失败。

### Fatal

代表：

> Runtime / protocol 已经不可信，不能把它包装成普通工具结果继续装作没事。

例如：

- handler 收到不可能的 payload kind；
-tool task join failure；
-严重 I/O / internal invariant。

正确 Error Taxonomy 决定 Agent 能不能安全自愈。

---

## 34. Tool Result 怎样回到模型

正常 handler 返回 `ToolOutput`。

Runtime：

```text
handle result
↓
attach ToolResultMetadata
↓
post-tool hook
↓
record executed call / accepted result
↓
convert to Responses API output item
↓
record canonical history
↓
next sampling
```

失败但可恢复时也会转成：

- `FunctionCallOutput`
- `CustomToolCallOutput`
- `ToolSearchOutput`

并带：

```text
success = false
```

模型因此能在下一轮：

-改参数；
-换 Tool；
-解释失败；
-停止任务。

---

## 35. Tool Result 也必须 Truncate

Tool 输出可能极大：

```text
git diff
test log
MCP JSON
browser page
database rows
```

不能无界进入 Context。

MCP Handler 会根据：

-Tool 自己 output token limit；
-否则模型 truncation policy；

选择 presentation truncation。

这再次说明：

> **Tool Runtime 的结束不是“函数返回”，而是“形成可安全回填模型的有界 observation”。**

---

## 36. Code Mode 为什么也是 Tool Scale 策略

Direct model tool call 适合：

```text
模型
→ 一个工具
→ Runtime
```

但某些复杂任务需要很多细粒度 calls。

Code Mode 允许模型生成一段受控代码，在内部调用 nested tools。

好处可能包括：

-减少模型往返次数；
-把数据变换留在 runtime；
-不把每个中间结果都塞回 LLM；
-复用函数组合。

所以大量工具下有两条 scale path：

```text
Deferred Search
解决“先找到哪个工具”

Code Mode
解决“找到后如何高效组合多个工具”
```

它们不是互斥。

---

## 37. MCP 和 Skills 的关系

MCP：

> **能力协议 / Tool transport。**

Skills：

> **如何识别场景、使用能力、组合流程的知识包。**

可能出现：

```text
Skill:
“处理 GitHub PR review”

SKILL.md:
告诉 Agent 先看 changed files，
再读 diff，
再运行 tests，
最后如何组织 review。

底层能力：
GitHub MCP / shell / file tools
```

因此：

```text
MCP Tool
≠
Skill

Skill
可以引用 / 驱动 MCP Tool
```

---

## 38. 几万个 Skills 怎么办

不能：

```text
10,000 * 完整 SKILL.md
→ 每轮 Prompt
```

Codex 已经给出：

### Discovery layer

只暴露名字 / description / locator。

### Metadata budget

根据 Context Window 或 explicit max context tokens 严格限额。

### Fair truncation

description 公平缩短，必要时整条 Skill omitted。

### Progressive disclosure

真正选中以后再打开 SKILL.md。

### Resource on demand

references / scripts 继续延迟读取。

如果 Skill 数量进一步上升，下一步自然是：

```text
catalog pre-filter / search
→ top-K metadata
→ selected SKILL.md
→ selected resource
```

而不是取消预算。

---

## 39. Tool / Skill Explosion 的评测指标

工具多了以后，最重要的不是“能加载多少”，而是：

### Discovery

```text
Recall@K
MRR
top-K relevant-tool coverage
```

### Selection

```text
correct tool rate
unnecessary search count
wrong namespace rate
```

### Arguments

```text
schema-valid rate
semantic-valid rate
repair success rate
```

### Runtime

```text
execution success
approval latency
sandbox retry rate
cancel correctness
parallel speedup
```

### Context

```text
model-visible tool bytes
skills metadata tokens
catalog truncation rate
Prompt Cache effect
```

Codex 已经为其中很多维度提供了 telemetry 点。

---

## 40. 场景题：Agent 总是选错 Tool，怎么排查

不要先改 Tool description。

按生命周期：

```text
1. Registry 里是不是正确 Tool？
2. AllowedTools 有没有误过滤？
3. Exposure 是 Direct / Deferred / Hidden 哪个？
4. tool_search 的 search_text 是否能命中？
5. BM25 top-K 是否被相似 Tool 淹没？
6. namespace 是否冲突？
7. model-visible spec 是否被 budget 截断？
8. Tool description / schema 是否区分度不足？
9. 模型选对名字但 payload invalid？
10. Hook 是否改写了 input？
11. Policy / sandbox 是否把“执行失败”伪装成“选错工具”？
```

这才是 Tool Lifecycle Debug。

---

## 41. 场景题：为什么不把所有 Tool 做 Embedding Search

可以使用 embedding，但它不是完整答案。

还要处理：

-Exact name / namespace；
-schema field names；
-policy filter；
-dynamic refresh；
-collision；
-deferred loading；
-ToolResult lifecycle；
-permission。

Codex 当前 BM25 说明了一个现实：

> Tool discovery 更像结构化 catalog search，不一定需要先上复杂向量数据库。

什么时候 embedding 有价值？

- tool description 语义同义词很多；
-跨语言；
-大量自然语言 capability；
-BM25 recall 明显不足。

即使如此，也应该替换 / 增强 discovery 层，而不是绕过 Registry / Router / Policy。

---

## 42. 面试怎么完整解释 Codex Tool Architecture

可以这样回答：

```text
Codex 把 Tool Runtime 拆成 Spec、Executor、Registry 和每个 Step 的 Router。
工具可以来自 core、MCP、extensions、dynamic tools 和 hosted tools。
注册只代表 Host 知道怎么执行，不代表模型直接可见。
最终每个 Step 会经过 AllowedTools、policy 和 exposure planning，
把工具分成 Direct、Deferred、Code Mode 或 Hidden 等暴露面。

大量工具时，MCP 默认可以 Deferred，
初始 Prompt 只暴露 tool_search；
tool_search 对 deferred ToolSearchInfo 建 BM25 索引，
命中后才把 LoadableToolSpec 返回给模型。
Agent-plugin MCP spec 还有单项 8KB、累计 64KB 的硬预算。
Skills 也不是一次加载全文，而是 catalog metadata → SKILL.md → resources 的 progressive disclosure，
并且 catalog 有独立 token/char budget。

模型返回 call 后，Router 统一解析 payload；
Registry 先做 runtime/payload 检查和 pre-tool hook，
随后 Tool Orchestrator 处理 approval、Guardian、Permission、network 和 sandbox，
必要时只做有限的 privilege escalation retry。
ToolCallRuntime 用 StepContext 保证“模型看到什么”和“稍后执行什么”一致，
用读写锁控制 parallel-safe 与 serial Tool，
用 cancellation token 把中止也变成结构化 Tool Output。
最后 post hook、truncation、metadata 与结果一起回填 canonical history，
再进入下一次 sampling。
所以完整 Tool Lifecycle 是能力注册、按需发现、安全执行和结果回填的闭环，
不是一次 function call。
```

---

## 43. 源码核验入口

- [`tools/src/tool_executor.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/tools/src/tool_executor.rs)：共享 ToolExecutor / ToolExposure contract。
- [`core/src/tools/registry.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/registry.rs)：Core Registry。
- [`core/src/tools/router.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/router.rs)：ToolCall parsing / routing。
- [`core/src/tools/spec_plan.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/spec_plan.rs)：Step Tool Plan。
- [`core/src/tools/handlers/tool_search.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/handlers/tool_search.rs)：BM25 deferred discovery。
- [`core/src/mcp_tool_exposure.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/mcp_tool_exposure.rs)：MCP exposure / budget / app policy。
- [`core/src/tools/handlers/mcp.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/handlers/mcp.rs)：MCP Tool Runtime。
- [`core/src/tools/orchestrator.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/orchestrator.rs)：approval / sandbox / retry。
- [`core/src/tools/parallel.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/parallel.rs)：parallel gate / cancellation / result。
- [`ext/skills/src/extension.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/skills/src/extension.rs)：Skills 接入 Thread/Turn/Tool/Context。
- [`ext/skills/src/render.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/skills/src/render.rs)：catalog budget。
- [`ext/skills/src/render_observability.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/skills/src/render_observability.rs)：Skill catalog metrics。
- [Skill Creator sample](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md)：Progressive Disclosure 设计说明。

下一篇：[Codex Engineering & Evaluation →](04-engineering-evaluation.md)
