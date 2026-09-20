
# 03. DeerFlow Tool Lifecycle｜从能力组装、Deferred Discovery 到 Policy、Sandbox 与结果回填

[← Memory](02-memory-lifecycle.md) · [DeerFlow 总览](README.md) · [Engineering & Evaluation →](04-engineering-evaluation.md)

> **源码基线：** bytedance/deer-flow@1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe

DeerFlow 的 Tool（工具）系统不应该只理解成 LangChain BaseTool 列表。

同一个 Tool 在产品里要经过至少三层：

~~~text
Capability Assembly
系统当前有哪些能力

Model-visible Schema
这一轮模型能看见哪些 Tool Definition

Execution Policy
模型真的调用以后，Runtime 是否允许执行
~~~

随后才进入 Sandbox、MCP Session、真正 Tool Body、Result Budget、Receipt 和下一轮 Context。

因此一个完整 Tool Lifecycle 是：

~~~text
Config / Builtins / MCP / Memory / Subagent
→ candidate tools
→ deferred discovery
→ skill / auth policy
→ model binding
→ tool call
→ execution middleware
→ sandbox / external service
→ normalized ToolMessage
→ result budgeting / evidence
→ next model request
~~~

---

## 1. Tool 怎样进入 Agent 的能力面

### Tool Pool 不是固定数组，而是每个 Agent Build 的能力快照

主要入口：

backend/packages/harness/deerflow/tools/tools.py

get_available_tools() 会根据当前 AppConfig、Model 和 Runtime Feature 组装能力。

来源包括：

- config.yaml 中配置的 Tool
- DeerFlow Built-in Tools
- MCP Tools
- Memory Tools
- Subagent task / batch tools
- ACP Agent Tool（存在 ACP agent 配置时动态加入 `invoke_acp_agent`）
- Skill Evolution 管理工具
- Vision Tool
- Upload / Conversation Reader 等条件能力

这里的 ACP（Agent Client Protocol）入口也印证了同一个设计：外部 Agent 能力最终先被包装成普通 Tool，再进入 DeerFlow 统一的模型可见 Schema、Middleware Policy 和 Tool Result 生命周期，而不是绕开 Harness 单独建一条执行通道。

#### 为什么 Model 也会影响 Tool Pool

例如 view_image 只有当前模型 supports_vision 时才加入。

write_file 的 description 还会根据当前模型实际 max_tokens 增加单次输出预算提示。

而且源码会 clone Tool 再改 description，不修改 module-level singleton。

否则：

~~~text
Model A 有 8K output cap
→ 修改全局 write_file 描述

Model B 无这个 cap
→ 错误继承 A 的提示
~~~

Tool Description 本身就是 Context，因此也必须有生命周期。

#### Host Bash 为什么可能从候选集直接消失

使用 LocalSandboxProvider 时，DeerFlow 默认不暴露 Host Bash，除非安全配置明确允许。

这是一条很好的最小能力原则：

> 如果已经有 Sandbox Bash，就不要同时给模型另一条绕过 Sandbox 的 Host Shell。

---

### Tool 名字本身也是协议，不能 Config 一套、Runtime 一套

get_available_tools() 会检查：

~~~text
config name
vs
实际 BaseTool.name
~~~

如果不同，会记录 warning。

为什么这种小事会变成 Runtime Bug？

模型看到的 Tool Schema 是按实际 Tool name 绑定的，而某些 Router / Config / Policy 可能仍按配置名字判断。

最终可能出现：

> 模型正确调用一个名字，Runtime 却说 not a valid tool。

所以 Tool Identity（工具身份）必须在：

- Prompt Schema
- Router
- Policy
- Audit
- Execution

之间保持一致。

---

## 2. Deferred MCP：大量工具怎样按需暴露而不绕过执行边界

### 大量 MCP Tool：先只告诉模型“有什么名字”

当前 Deferred Tool（延迟工具）主要针对 MCP Tool。

实现：

- backend/packages/harness/deerflow/tools/builtins/tool_search.py
- DeferredToolFilterMiddleware
- McpRoutingMiddleware

如果启用 Tool Search：

~~~text
完整 MCP Tool 仍注册在 ToolNode
        ↓
但完整 schema 不进入 ModelRequest
        ↓
System Prompt 只列 deferred tool names
        ↓
模型需要时调用 tool_search
        ↓
promotion state 写入 LangGraph ThreadState
        ↓
下一轮 ModelRequest 才暴露完整 schema
~~~

这解决一个常见扩展问题：

> MCP Server 越多，不等于 System Prompt / tool schema 应该线性增长。

---

### Deferred Catalog 为什么需要 catalog_hash

DeferredToolCatalog 会对：

- Tool name
- canonical OpenAI schema

排序后生成 hash。

ThreadState.promoted 保存：

~~~text
catalog_hash
names
~~~

为什么不能只保存：

~~~text
["mcp__foo__write"]
~~~

因为未来：

- MCP Server 升级
- Schema 改了
- 同名 Tool 被替换

旧 Checkpoint 中的 promotion 可能错误授权一个已经变化的 Tool。

当前 Reducer 规则是：

> catalog hash 改变时，promotion names 整体换代。

这避免“同名即同能力”的错误假设。

---

### tool_search 做的是 Discovery，不是 Authorization

Tool Search 支持几种 Query：

~~~text
select:a,b
精确取指定 Tool

+slack send
名字必须包含 slack，再按剩余关键词排序

普通 regex / keyword
匹配 name + description，最多返回少量候选
~~~

返回：

- matched Tool 的完整 schema
- promoted names

写进 LangGraph Command / state。

但：

> **发现一个 Tool ≠ 获得执行权限。**

后面还有 Skill Tool Policy、Guardrail / Authorization、Sandbox 等独立边界。

---

### 为什么 DeferredToolFilter 同时管 Schema 和 Execution

这是一个非常重要的纵深防御。

DeferredToolFilterMiddleware 在 wrap_model_call 时：

> 从 request.tools 中隐藏尚未 promoted 的 MCP schema。

但它还在 wrap_tool_call 时检查：

> 模型有没有直接猜 Tool 名绕过 tool_search。

如果 Tool 仍是 deferred：

~~~text
Error:
Tool is deferred and has not been promoted.
Call tool_search first.
~~~

这样不能靠：

> “模型虽然没看见 schema，但我知道名字。”

绕过 discovery contract。

所以 promotion state 同时约束：

- Model Visibility
- Execution Routing

---

### MCP Routing 为什么可以自动 promote，但仍然不执行 Tool

有些 MCP Tool 带 routing metadata：

- keywords
- priority
- prefer
- top_k

McpRoutingMiddleware 在 before_model 读取最新 genuine user message。

如果用户请求命中关键词：

> 自动把最相关的一小批 Deferred Tool 标为 promoted。

例如：

~~~text
用户：
查 Slack 里昨天的发布讨论

routing keyword:
slack

→ promote mcp__slack__search_messages
~~~

它做的只是：

> **减少模型先调一次 tool_search 的交互成本。**

真正 Tool Call 仍要走后面的 Policy / Execution。

而且源码有显式 assertion：

> McpRoutingMiddleware 必须排在 DeferredToolFilterMiddleware 前面。

Middleware Order 本身就是协议。

---

## 3. Skill：发现、激活、Tool Policy 与 Secret Authority

### Skill Activation：启用 Skill 不等于自动获得它声明的权限

Skills 是 DeerFlow Tool System 最重要的一层。

Skill 可以在 SKILL.md frontmatter 声明：

- description
- allowed-tools
- required secrets
- autonomous secret policy
-其他 metadata

但：

> **Skill 安装 / enable 只代表可发现。**

真正让 allowed-tools policy 生效，需要：

- 用户显式 /skill-name 激活
- 或模型真实 Read 了这个 SKILL.md，并进入 skill_context

这防止一个“只是存在于磁盘上的 Skill”自动收窄 / 扩大当前 Tool Authority。

---

### Slash Skill 和被动加载 Skill 为什么权限语义不同

SkillToolPolicyMiddleware 维护 Active Policy Source：

~~~text
slash
用户显式激活

skill_context
模型之前真实加载过

passive
没有活动 Skill Policy
~~~

如果用户显式 slash 激活一个 Skill：

> 这条 run-scoped policy 优先。

模型随后被动 Read 第二个 Skill：

> 不能偷偷扩大 slash Skill 的 allowed-tools。

这是显式用户意图优先于模型自主扩权。

---

### Skill allowed-tools 为什么同时过滤 Schema 和真实 Tool Call

和 Deferred Tool 一样，DeerFlow 做双重检查。

#### Model Request

SkillToolPolicyMiddleware 从 request.tools 过滤不允许 Tool。

模型根本看不到其 schema。

#### Tool Execution

wrap_tool_call 再检查名字。

即使模型：

- 从历史知道 Tool 名
- 猜出 Tool 名
- tool_search 返回异常 schema

仍然不能执行 denied Tool。

#### tool_search 本身也必须被过滤

这是一个容易漏掉的边界。

如果 active Skill 只允许 Tool A，但 tool_search 可以返回 Tool B 完整 schema：

> Discovery 就成了权限绕过。

所以 Middleware 会检查 tool_search 的 Command：

- promoted names
- returned schemas

只留下 active skill policy 允许的工具。

---

### Skill Secrets 为什么不从 Host Environment 自动继承

Skill 可以声明 required secrets。

但 DeerFlow 不允许 Skill 自己读取：

> Host 进程全部环境变量。

真正秘密值必须由 Caller 放进 request runtime context。

每次模型调用，SkillActivationMiddleware 会重新计算：

- 当前 slash Skill
- 当前 skill_context
- Skill 是否仍 enabled
- 是否在 agent allowlist
- secrets-autonomous 是否允许
-当前 request 提供哪些 secret names

然后只注入声明过的值。

Secret values 不写日志，Audit 只记：

- Skill names
- Secret names
- Missing names

这样 Skill 无法利用“曾经启用过”永久持有 secret。

---

## 4. 一次真实 Tool Call 的执行安全链

### Tool Call 进入执行阶段以后，先经过 Policy Stack

DeerFlow Tool 执行使用 LangChain wrap_tool_call Middleware。

重要层包括：

- Guardrail / Authorization
- SkillToolPolicy
- DeferredToolFilter
- Sandbox Audit / Sandbox Authorization
- ReadBeforeWrite
- Clarification
- ToolErrorHandling
- ToolProgress
- ToolReceipt
- ToolOutputBudget

不需要死记完整顺序，但要理解不同层解决的问题。

#### Guardrail 与 Authorization

DeerFlow 没有单独复制一套 AuthorizationMiddleware。

Pluggable Authorization Provider 会通过 Adapter 复用 GuardrailMiddleware 的 fail-closed / audit / error semantics。

Authorization 解决：

> 当前用户 / principal 对这个能力有没有资格。

#### Skill Policy

解决：

> 当前主动 Skill 是否允许这个 Tool。

#### Sandbox

解决：

> 即使逻辑允许执行，这个文件 / 命令在什么实际隔离环境里运行。

这三层不是一回事。

---

### Sandbox 不只是 Tool Wrapper，它是 Run 级资源

SandboxMiddleware 在 before_agent 获取 Sandbox，在 after_agent 释放。

ThreadDataMiddleware 必须在它之前，因为 Sandbox 需要当前 Thread 的：

- workspace path
- uploads path
- outputs path

Sandbox Provider 可以是：

- Local
- AIO / remote
- E2B
- OpenSandbox
-其他实现

ThreadState 只保存 sandbox identity / metadata，不把 Provider 对象持久化。

这让 Checkpoint 能恢复“我属于哪个隔离环境”，而 Runtime 实例仍由 Provider 管理。

---

### Authorization 和 Sandbox 为什么还要一起检查

用户有写文件权限，不等于：

> 任意路径都能写。

Sandbox Authorization 会结合：

- principal
- thread / run context
- target operation
- sandbox policy

判断某个 Sandbox 行为是否允许。

这就是：

~~~text
Product Authorization
→ 你能不能用这类能力

Sandbox Boundary
→ 这次具体副作用能发生在哪里
~~~

两个层级。

---

### Read-before-write：为什么修改现有文件前必须看过“当前版本”

这是 DeerFlow 很有代表性的 Coding Agent Safety / Correctness Middleware。

实现：

ReadBeforeWriteMiddleware

它要求：

> 修改一个已有文件之前，模型必须先 read_file 看到文件的当前版本。

不是因为“读一下更礼貌”，而是为了解决真实失败模式：

> Agent 连续 append 同一报告段落，却从不重新读取文件。

#### Read Mark 存在哪里

成功 read_file 后，ToolMessage metadata 里记录：

> 当前完整文件内容 SHA-256。

写入前重新检查真实文件 hash。

如果已经变化：

> 旧 read mark 失效，要求重新读取。

#### 为什么写操作不会自动更新 mark

一次 write 后文件内容已经变。

如果 write 自动刷新“我已经读过”：

> 下一次写可以继续基于旧模型认知。

所以每次真正修改后都必须重新 Read。

#### 同一 Turn 两个并发写为什么要串行 gate

LangGraph 可能并发执行一条 AIMessage 中的 Tool Calls。

如果两个 write 同时：

~~~text
都先检查旧 hash
都通过
然后一起写
~~~

Read-before-write 就失效。

所以 Gate + Tool Execution 对同一 scope/path 有 critical section。

---

### Guard / Read-before-write Block 后，为什么连历史 Tool Args 都要缩短

如果 write_file 带一个 70KB content，但因为没先 Read 被阻止：

- Tool 没真正执行
- 模型下一步必须重新 Read，再重新生成写入内容

保留那 70KB blocked payload 在每轮 Context 里没有价值。

ReadBeforeWriteMiddleware 会在**模型请求视图**里把 blocked Tool Call 的 content / old_str / new_str 参数替换成短 placeholder。

但是：

- ThreadState 原始消息
- Tool Receipt
- Run Journal

仍保留真实参数证据。

再次出现：

> **Model Context 和 Audit Evidence 可以不同。**

---

### ToolErrorHandling 为什么不能让所有异常炸穿 Graph

Tool 失败可能来自：

- ToolException
- MCP error
- timeout
- sandbox authorization
- file IO
-业务异常

ToolErrorHandlingMiddleware 会把可恢复 Tool Failure 规范成 ToolMessage，让模型下一轮看到并修正。

但 GraphBubbleUp / Interrupt 一类控制流不能被当普通 Error 吞掉。

成熟 Tool Runtime 必须区分：

~~~text
模型能修的执行失败
vs
Runtime control flow / cancellation
~~~

否则 Clarification、Interrupt、Graph navigation 都会被错误包装成“Tool failed”。

---

### Tool Receipt 为什么和 Tool Result 不一样

Tool Result 是模型的 Observation。

Tool Receipt（工具收据）更像产品侧的执行证据。

它可以记录：

- Tool identity
- args digest
- result metadata
- status
- artifact / reference
- execution evidence

后续 Subagent acceptance、Run Journal、Debug 可以引用。

所以：

~~~text
ToolMessage
回答模型：发生了什么

Receipt / Journal
回答系统：我们怎样证明它发生过
~~~

这是 Agent Runtime 可验证性的重要区别。

---

### ToolOutputBudget：大结果怎样变成可继续读取的引用

Context 篇讲过输出预算，这里从 Tool Lifecycle 角度再看一次。

Tool 真正返回完整结果以后：

~~~text
Tool Body
→ complete result

ToolOutputBudget
→ 过大？
   ├─ 能 externalize
   │  → 写文件
   │  → preview + virtual path
   └─ 不能
      → inline truncation
~~~

对远程 Sandbox，DeerFlow 不会假设 Host outputs path 在容器里一定可见。

如果 Provider 没有 thread-data mount，会直接在 Sandbox 内写虚拟 output file，再验证：

> 文件确实能被 read_file 看到。

只有成功才把引用交给模型。

---

## 5. MCP Session、Skill Context 与 Subagent Tool 如何接入同一 Runtime

### MCP Session 为什么按 user + thread 隔离

很多 MCP Server 是 stateful（有状态）的。

例如 Browser MCP：

~~~text
call 1:
打开页面

call 2:
点击按钮
~~~

如果每次创建新 MCP Session：

> 第二次就丢掉浏览器状态。

DeerFlow 有 MCPSessionPool，按：

~~~text
(server_name, user_id:thread_id, event_loop)
~~~

复用 Session。

user_id 很重要。

如果只按 thread_id：

> 两个用户碰巧使用相同 thread id，可能共享同一个 stateful MCP Session。

这是跨用户隔离漏洞。

---

### MCP Session 为什么由 dedicated owner task 管整个生命周期

MCP ClientSession 建在 anyio cancel scope 上。

anyio 要求：

> 进入和退出 cancel scope 必须是同一个 Task。

如果：

- Call A 创建 session
- Call B 关闭 session

可能直接 RuntimeError。

所以 Session Pool 为每个连接建立 dedicated owner task：

~~~text
owner task
→ __aenter__
→ initialize
→ 原子注册到 pool
→ 等 close_event
→ __aexit__
~~~

其他 Caller 只：

- 获取引用
- signal close

不自己执行 __aexit__。

这是一种很典型的 async resource ownership（异步资源所有权）设计。

---

### MCP Pool 怎样避免重复连接和泄漏

同一个 key 同时有两个 Caller：

> 不能都开始创建 Session。

Pool 有 in-flight creation future。

第一个成为 Creator。

第二个 Join 同一 Future。

只有 Owner Task 完成 initialize 并**同时注册进 pool**以后 Future 才 resolve 成功。

因此 Caller 不会得到一个：

> “看起来创建成功，但其实还没人负责关闭。”

的 unmanaged session。

Pool 还有 LRU capacity，断线时只移除仍然是当前 entry 的 Session，防止旧连接 teardown 误杀新连接。

---

### Stdio MCP 的 cwd / temp 为什么要固定到 Thread Workspace

本地 MCP Server 可能生成文件：

- screenshot
- report
- export

如果 subprocess 默认在 Host cwd / OS temp 写文件：

> Sandbox 和 Artifact API 可能访问不到。

DeerFlow 启动 stdio MCP Session 时，会把：

- cwd
- TMPDIR / TMP / TEMP

固定到当前 Thread 的 mounted user-data tree。

Tool 返回 local path 后，还会把它改写成：

/mnt/user-data/...

这种模型和 Artifact API 能继续读取的虚拟路径。

因此 MCP Tool 的文件输出真正接进 DeerFlow 文件生命周期。

---

### Skills：目录元数据和完整正文也要分层

DeerFlow Skill System 遵循 Progressive Loading（渐进加载）。

System Prompt 可以只给模型：

- skill names
- descriptions
- locations
- disabled list

更大规模时还可以只给 compact skill index，再通过 describe_skill / Read 获取更多信息。

真正相关时：

> 模型 read_file 读取对应 SKILL.md。

Supporting resources 继续按需加载。

#### Slash Activation 为什么不同

用户显式：

/some-skill

Runtime 会通过 SkillActivationMiddleware 直接注入这个 Skill 的完整内容。

模型不用再重复 Read 主 SKILL.md。

这是：

> **用户明确选择能力。**

因此它还可以激活更严格的 run-scoped Tool Policy 和 Secret Binding。

---

### Skill Context 为什么压缩以后只保留“重读引用”

模型真实读过 SKILL.md 后，Skill Context Middleware 会捕获：

- path
- description
- name

进入 ThreadState.skill_context。

Summarization 把旧 ToolMessage 删除后，这些引用仍在。

下一次 DurableContext 只告诉模型：

> 这个 Skill 以前加载过，请重新 Read 当前文件再执行。

它不会永久保存旧 Skill Body。

原因是：

- Skill 可能升级
- Skill 可能 disabled
- allowed-tools 可能变化
- required secrets 可能变化

长期保存旧 Body 反而可能造成权限漂移。

---

### Subagent task 也是一个 Tool，但它启动的是另一套 Agent Runtime

Lead Agent 的 native Subagent 入口：

task

从父模型看只是 Tool Call。

但 Tool Body 会进入 SubagentExecutor：

- 选择 Agent Definition
- 独立 Model
- 独立 Tool Filter
- 独立 Context Snapshot
- 独立 Run / Step tracking
- 独立 capacity budget

Child 结果最终再作为 task Tool Result 返回 Parent。

所以：

> **Multi-Agent 在 Lead Agent 的控制面上表现为 Tool；在执行面上却是一条独立 Agent Run。**

详细 Context isolation 和 capacity 在 Engineering 篇继续讲。

---

## 6. 把 Tool 生命周期串起来，并知道怎样评测

### 一个完整 Tool Lifecycle

用户说：

> “查监控 MCP，再根据 frontend skill 修复页面；修改前先确认当前文件。”

#### Agent Assembly

候选 Tool 包含：

- Read / Edit / Bash
- Deferred MCP Monitoring Tools
- task
- Tool Search
- Skill tooling

#### Model Call

Skill 还没 active，普通 Tool 可见。

Monitoring MCP schema 暂时隐藏，只在 prompt 里列名字 / routing hints。

#### Promotion

McpRoutingMiddleware 根据“监控”关键词自动 promote 一个 Tool，或者模型调用 tool_search。

ThreadState.promoted 写入 catalog hash + names。

#### Skill Activation

模型读取 frontend SKILL.md。

skill_context 更新。

下一次模型请求 SkillToolPolicy 根据 allowed-tools 进一步缩小 Tool Schema。

#### MCP Call

模型调用 monitoring MCP。

执行前仍经过 Skill Policy 和 Authorization。

MCP Pool 用 user + thread scope 获取 stateful session。

结果过大，被 ToolOutputBudget externalize。

#### File Edit

模型准备修改文件。

ReadBeforeWrite 检查是否读过当前版本。

没读：

> Block。

模型先 read_file。

再次 Edit：

> Gate 通过，在 Sandbox 中执行。

#### Result / Evidence

模型看到 ToolMessage。

Run Journal / Receipt 保存更完整执行证据。

下一轮继续。

这才是一条 DeerFlow Tool Lifecycle。

---

### Tool 应该怎样评测

至少分六层。

#### Assembly

- 正确 Tool 是否进入候选集
- host bash 是否在 Sandbox mode 被正确隐藏
- vision Tool 是否按 model capability 出现
- name mismatch 是否能被检测

#### Discovery

- deferred Tool recall@K
- routing auto-promotion precision
- stale catalog promotion 是否被 hash 清除
- 猜名字是否被执行侧拦截

#### Policy

- Skill allowed-tools
- Authorization
- Guardrail
- Sandbox Authorization
- Secret Binding

要分别测 schema filter 和 execution filter。

#### Execution

- MCP session reconnect
- concurrent Tool
- cancellation
- timeout
- Read-before-write
- remote Sandbox file path

#### Result

- Tool Error normalization
- Receipt
- Output externalization
- Artifact link
- Result sanitization

#### Task Utility

最终还是看：

> 更复杂的 Tool Harness 有没有真正提升任务成功、安全与成本。

一个什么都拒绝的系统，安全指标可能很好，但不是好 Agent。

---

## 7. 源码锚点

1. [Tool assembly](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/tools/tools.py)
2. [Deferred Tool Search](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/tools/builtins/tool_search.py)
3. [DeferredToolFilterMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/deferred_tool_filter_middleware.py)
4. [McpRoutingMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/mcp_routing_middleware.py)
5. [SkillToolPolicyMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/skill_tool_policy_middleware.py)
6. [SkillActivationMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/skill_activation_middleware.py)
7. [ReadBeforeWriteMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py)
8. [Guardrail / authorization middleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/guardrails/middleware.py)
9. [SandboxMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/sandbox/middleware.py)
10. [ToolErrorHandlingMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py)
11. [ToolReceiptMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/tool_receipt_middleware.py)
12. [ToolOutputBudgetMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/tool_output_budget_middleware.py)
13. [MCP Session Pool](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/mcp/session_pool.py)
14. [MCP tool bridge](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/mcp/tools.py)
15. [Skill context](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/skill_context.py)
16. [Subagent executor](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/subagents/executor.py)

下一篇：[DeerFlow Engineering & Evaluation →](04-engineering-evaluation.md)
