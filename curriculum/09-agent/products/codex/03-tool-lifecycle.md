# 03. Codex Tool Lifecycle｜模型看到一个工具之前和调用以后，Runtime 到底做了什么

[← Memory](02-memory-lifecycle.md) · [Codex 总览](README.md) · [Engineering & Evaluation →](04-engineering-evaluation.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

Tool（工具）是 Agent 最容易“看起来懂了”的部分：给模型一个 JSON Schema（JSON 参数模式），模型返回函数名和参数，程序执行，再把结果送回去。

Codex 当前源码真正复杂的地方，恰恰都在这三句话之间。

假设用户让 Codex：

> “看看这个仓库为什么测试失败，必要时读 GitHub 上的 issue，但不要做未经批准的外部写操作。”

为了完成它，Codex 可能需要 shell（命令执行）、文件操作、GitHub MCP、插件 Skill，甚至 Code Mode（代码模式）。我们沿源码看：这些能力怎样进入一个统一 Registry（注册表），模型为什么只看到其中一部分，真正执行前谁做审批和沙箱，最后结果怎样安全回到下一次模型请求。

---

## 1. 先分清“Host 有这个能力”和“模型现在能看见它”

Codex 的 Tool 系统至少要同时维护两个事实：

~~~text
Host 侧
我知道这个工具怎样执行

Model 侧
这次 Step 是否应该让模型看见 / 发现 / 调用它
~~~

如果把两者混成一个 `tools` 数组，那么只要 Runtime 注册了一个危险或庞大的工具，模型就会自动获得它的名字和 Schema。大规模系统也会因为工具数不断上涨，把越来越多请求预算浪费在 Tool Definition（工具定义）上。

因此 Codex 有几个不同对象。

`ToolExecutor（工具执行器）` 把“工具名、模型可见定义、搜索信息、是否支持并发、怎样执行”绑定在一起。

`ToolRegistry（工具注册表）` 保存当前 Step 内 Host 已经注册的执行器。

`ToolRouter（工具路由器）` 则是在这一步已经 finalize（定稿）的计划：哪些能力向模型直接展示，哪些只能搜索发现，哪些只允许 Code Mode 调用，以及模型真正收到的 Tool Specs（工具定义）。

最重要的关系是：

> **Registry 是 Host 的能力目录；Router 是一次模型采样的能力视图。**

---

## 2. 一个 Tool Router 是在每个 Step 里重新“编译”出来的

`build_tool_router` 不只读取一份静态配置。

它先加入 Core Tool（核心工具），再把这一次 Step 捕获到的 MCP Tool、Extension Tool（扩展工具）、Dynamic Tool（动态工具）以及 Hosted Model Tool（模型服务端工具）汇总到 Registry，随后应用 Allowlist（允许列表）、命名冲突、Tool Mode（工具模式）和 Exposure（暴露方式）等规则，最后才得到模型可见的 Tool Router。

为什么这个计划要属于 Step Context？

因为 MCP Catalog、插件、执行环境、权限甚至模型能力都可能在一个 Turn 内发生变化。模型在 Step A 看到什么，就应该让 Step A 产生的 Tool Call 用那一份计划解释。

所以 Tool Lifecycle 和上一章 Context Lifecycle 实际在这里汇合：

~~~text
StepContext
├─ World State：模型当前知道什么运行条件
└─ ToolRouter：模型当前知道什么可执行能力
~~~

---

## 3. Tool Exposure 不是一个布尔值

共享 `codex-tools` crate 里，Tool Exposure（工具暴露方式）有多种状态。这里不需要背枚举，但要理解为什么需要这些状态。

| 暴露方式 | 读者可以怎样理解 |
|---|---|
| Direct（直接暴露） | 一开始就出现在模型的工具列表里；符合条件时也可供 Code Mode 使用 |
| Deferred（延迟暴露） | Host 已注册，但初始请求不展开完整定义；模型先通过 Tool Search 找到它 |
| Direct Model Only（仅模型直接调用） | 只给模型正常 Tool Call 使用，不进入 Code Mode 嵌套工具面 |
| Deferred Model Only（仅模型延迟发现） | 可通过 Tool Search 找到，但不允许 Code Mode 内嵌调用 |
| Code Mode Only（仅代码模式） | 普通模型工具列表不展示，只给 Code Mode 的内部代码调用 |
| Hidden（隐藏） | Runtime 仍保留执行器，但不让模型获得调用能力 |

这些状态解决的不是“写法优雅”，而是**能力规模和权限面**。

同一个 Host 可以知道几千个 Tool，但当前模型请求只需要几十个直接工具和一个按需搜索入口。

---

## 4. Tool 名字冲突为什么必须在 Runtime 处理

Registry 有 trusted（宿主可信注册）和 external（外部注册）之分。

外部 MCP / Extension Tool 如果声明一个已经存在的名字，不能静默覆盖 Core Tool。源码还对 `exec_command`、`shell_command` 等保留名字做专门保护。

想象一下，如果第三方 MCP Server 注册了一个同名 `exec_command`：

~~~text
模型看到“exec_command”
↓
以为它是 Codex 自己受沙箱约束的命令工具
↓
实际却被第三方实现接管
~~~

这会直接破坏安全语义。

因此 namespace（命名空间）、collision detection（冲突检测）和 reserved name（保留名称）都属于 Tool Contract 的一部分，而不是代码整洁问题。

---

## 5. MCP Tool 怎样从远端目录变成 Codex 工具

MCP（Model Context Protocol，模型上下文协议）在 Codex 里不是一个单文件客户端。

`codex-mcp` 负责 Server Catalog（服务器目录）、连接绑定、Tool Catalog Cache（工具目录缓存）、Resource（资源）、授权 / Elicitation（交互请求）、插件来源等；`rmcp-client` 再负责 stdio、in-process（进程内）和 Streamable HTTP（可流式 HTTP）传输，以及 OAuth 等认证能力。

一次 MCP Tool 进入模型视野，大致会经历：

~~~text
配置 / 插件 / Connector 提供 MCP Server
↓
建立或复用连接
↓
获得 ToolInfo（工具元数据）
↓
构造 McpHandler（MCP 执行器）
↓
应用 Host Policy（宿主策略）
↓
注册到 ToolRegistry
↓
根据当前 Step 决定 Direct / Deferred / Hidden
↓
进入 ToolRouter
~~~

这里的 `ToolInfo` 不只是名字，还携带 server identity（服务器身份）、namespace、Schema、Connector / Plugin provenance（来源信息）等，后续审批、Trace 和扩展生命周期都可以使用这份来源。

---

## 6. “MCP Server 有这个 Tool”不代表 Codex 一定给模型

对于 Codex Apps / Connector（连接器）工具，Host 还会经过 `AppToolPolicyEvaluator`。

它可以结合 Connector 配置以及 Tool annotation（工具注解），例如 destructive hint（破坏性提示）和 open-world hint（开放世界访问提示），决定工具是否启用。

因此能力所有权是：

~~~text
MCP Server
声明“我提供什么”

Codex Host
决定“当前用户 / 配置是否允许把它变成 Agent 能力”
~~~

这条边界很重要。MCP 是能力协议，不是授权协议的替代品。

---

## 7. 大量 MCP Tool 时，Codex 不会默认把全部 Schema 展开

当前源码里，如果 Tool Search（工具搜索）可用，普通 MCP Tool 默认可以进入 Deferred（延迟暴露）模式。

这意味着模型初始看到的是一个更小的工具面。需要外部能力时，先调用 `tool_search`，Runtime 从 Deferred Catalog 中找到候选，再把匹配的 `LoadableToolSpec` 返回给模型。

当前 `ToolSearchHandler` 使用 BM25（基于词项相关性的经典文本检索算法），搜索文本会综合 Tool 名、Server、描述、Connector、命名空间和 Schema property（参数字段名）等信息。

所以当前事实是：

> **Codex 已经实现“完整能力目录 ≠ 每轮完整 Tool List”，并使用 BM25 做 Deferred Tool Discovery（延迟工具发现）。**

这和“Codex 已经针对五万个工具做过某种向量索引”不是一回事。后者如果没有源码证据，就只能作为工程推导。

---

## 8. Tool Search 自己为什么也需要缓存

如果 MCP 目录很大，而每次模型采样都重新构建 BM25 索引，Deferred Discovery 省下来的 Context 成本可能换成 Host CPU 开销。

`ToolSearchHandlerCache` 会检查 Deferred 来源是否真的发生变化。对于 immutable runtime（不可变运行时）可以利用 runtime identity（运行时身份）复用；Dynamic Tool 的搜索元数据变化时才重建对应 Handler。

这提醒我们，大规模工具系统要同时考虑两种成本：

~~~text
模型侧
Tool Schema 占多少 Context

Host 侧
目录构建、刷新和搜索花多少 CPU / 延迟
~~~

只优化其中一边并不完整。

---

## 9. Codex 还给某些 MCP Tool Spec 设置了硬字节预算

Agent-plugin MCP（Agent 插件提供的 MCP）有非常具体的 model spec budget（模型可见定义预算）：

~~~text
单个 spec 最大 8,000 bytes
同类累计最大 64,000 bytes
~~~

超过预算的工具会被设为 Hidden，而不是继续把定义塞入模型请求。

这和 Codex 根 `AGENTS.md` 的 Context 原则一致：自动注入模型上下文的内容必须有硬上限。

注意，这个数字是**当前源码里特定 Agent-plugin MCP spec 的限制**，不能外推成“所有 Codex Tool 一共最多 64KB”。

---

## 10. Skill 不是 Tool 的另一个名字

Codex 当前 App Server 会安装 Skills Extension（技能扩展），并给它 Executor、Orchestrator 和 Host 三种 provider（提供方）。

Skill 的作用更像：

> **告诉 Agent 在什么任务里应该怎样使用现有能力，以及需要时去哪里读取详细操作知识。**

一个 Skill 可能指导模型调用 shell、MCP、文件工具，也可能提供可执行脚本，但它本身不等于一个 Function Tool Schema（函数工具模式）。

这一区分能解释为什么 Skills 有自己的 discovery / context budget，而最终副作用仍然要经过 Tool Runtime。

---

## 11. Skill 的 Progressive Disclosure 是真实源码策略

Codex 自带的 skill-creator 示例把 Skill 内容分成三层：

~~~text
Name + Description（名称与描述）
用于选择 Skill

SKILL.md
真正决定使用 Skill 后加载主说明

references / scripts / assets
只在当前任务需要时继续读取或执行
~~~

这就是 Progressive Disclosure（渐进式展开）。

Skills Extension 对第一层目录还有自己的预算。当前源码默认 metadata char budget（元数据字符预算）为 8,000 字符；如果按模型 Context Window 自动计算，会取约 2%；显式 token budget 又有最大 10,000 tokens 的上限。单个 Skill prompt 和 description 也有边界。

预算不足时，源码会先公平缩短各 Skill description，而不是让排在最前面的一个 Skill 吃掉所有剩余空间；实在放不下时才整条 omit（省略），同时记录 truncation metrics（截断指标）。

因此 Skills 的规模控制不是“Context 够大就全加载全文”，而是从目录开始控制信息密度。

---

## 12. Code Mode 是第三种工具暴露面，不是简单“让模型写 Python”

Code Mode（代码模式）在当前 workspace 里有独立的 `code-mode`、`code-mode-runtime`、`code-mode-host` 和 protocol crate。Runtime 使用 V8 执行 JavaScript。

当 Tool Mode 允许 Code Mode 时，`register_code_mode_executors` 会遍历当前 Registry，只挑允许进入 Code Mode 的工具，给它们生成 normalized code-mode name（规范化代码模式名称），再构造 `CodeModeExecuteHandler` 和 `CodeModeWaitHandler`。

模型看到的 Code Mode `exec` 接受的是 raw JavaScript source（原始 JavaScript 源码）。代码内部的 nested tool call（嵌套工具调用）不是直接越过 Host 去调用外部系统；V8 Runtime 通过 callback（回调）把调用交还给 Codex Tool Runtime，再等待 Tool response（工具结果）返回。

因此：

> **Code Mode 改变了“模型怎样编排多个工具”，没有绕过 Tool Registry、权限和真实执行边界。**

它特别适合把一些中间数据变换留在代码运行时，而不是让每个细粒度结果都先变成一轮新的 LLM 请求。

---

## 13. Multi-Agent 协作工具故意不进入 Code Mode

Multi-Agent V2 有 `spawn_agent`、`send_message`、`followup_task`、`wait_agent`、`interrupt_agent`、`list_agents` 等协作工具。

当前模型指令明确告诉 Agent：这些 collaboration tools（协作工具）应作为 direct tool call（直接工具调用），故意不出现在 Code Mode 的 `tools.*` namespace 中。

这不是偶然遗漏。

子 Agent 的创建、消息投递和中断会改变整个 Agent Graph（智能体关系图），需要更清楚的模型可见边界和运行时事件；把它们藏在一段任意 JavaScript 深处，会让协作因果关系和审查更难理解。

所以“能否在 Code Mode 调用”本身也是 Tool Exposure 设计的一部分。

---

## 14. 模型返回 Tool Call 以后，Router 先把 Provider 形状统一成内部调用

Responses API 可以返回普通 Function Call、Tool Search Call、Custom Tool Call 等不同 item（项目）。

`ToolRouter::build_tool_call` 会先把这些外部形状统一成内部 `ToolCall`：

~~~text
ToolName
Call ID
Payload（参数载荷）
来源信息
~~~

之后的 Registry、Hook、审批和执行就不必每层重新理解 Provider response（模型服务方响应）格式。

这是一种很典型的 Runtime 边界：

> **先把外部协议归一化，再进入内部执行语义。**

---

## 15. Pre-tool Hook 能阻止调用，也能改写参数

在 Handler 真正执行之前，Registry 会运行 PreToolUse Hook（工具执行前钩子）。

Hook 可以：

- 继续执行；
- 阻止调用；
- 返回更新后的输入。

但“可以改写”不代表改写以后绕过校验。Runtime 会通过具体 Tool 的 `with_updated_hook_input` 重新构造调用，后续权限、Handler 解析和执行仍以最终输入为准。

MCP Handler 就会把改写后的 JSON 重新序列化为最终 arguments（参数）。

因此安全边界要理解成：

~~~text
模型生成参数
→ Hook 可能改写
→ 最终参数
→ 审批 / 权限 / Handler 执行
~~~

审查和日志真正关心的应该是**最终要执行什么**。

---

## 16. Extension Tool Lifecycle 看到的是“最终执行事实”

Extension API 还有 `ToolLifecycleContributor（工具生命周期贡献者）`。

它收到 Tool Start（工具开始）时，源码已经把 pre-tool hook 改写后的 finalized payload（最终参数）准备好；对于 MCP，还能看到 frozen provenance（冻结的工具来源），例如这个调用来自 Connector、配置、插件还是其他来源。

Tool Finish（工具结束）则区分 Completed（正常完成）、Blocked（被策略阻止）、Failed（失败）和 Aborted（中止）。

这个接口告诉我们：

> **Codex 不只是记录“模型想调用什么”，还单独记录“Host 最终尝试执行什么，以及结果属于哪一类”。**

对审计、Metrics 和 Trace 来说，这两者不能混。

---

## 17. Approval、Guardian 和 Sandbox 不是三个简单串行开关

上一版把 Guardian（自动风险审查）写成“普通 Approval 后面再加一层 Guardian”，这个说法太粗。

更准确的源码关系是：Tool Orchestrator（工具编排器）在需要 approval（批准）时形成 Approval Decision Input（批准决策输入）；Extension Registry 可以注册 `ApprovalReviewContributor（批准审查贡献者）`。Guardian V2 就是其中一个实现。

Guardian reviewer（审查器）可以根据当前审批策略、风险 category（风险类别）、已有异步 score（评分）和授权状态做几种决定：

~~~text
Allow
直接允许

AskUser
交给用户确认

Reviewed(...)
通过同步审查得到明确决定
~~~

它还会判断缓存评分是否过旧、当前授权状态是否已经变化，必要时放弃缓存并做 fresh review（新审查）。

所以 Guardian 的真实角色是：

> **参与“这次需要批准的动作应该怎样被裁决”的审批路由，而不是独立于审批系统之外的一道神秘模型闸门。**

---

## 18. Sandbox 才是真正约束副作用的执行边界之一

模型说“我只会在工作区写文件”并不是安全保证。

Tool Orchestrator 会根据 Permission Profile（权限配置）、filesystem policy（文件系统策略）、network policy（网络策略）、Tool 自己的权限需求以及平台能力选择 Sandbox Attempt（沙箱执行尝试）。

第一次执行如果被沙箱拒绝，不代表命令语义一定错误。Runtime 会进一步判断：

- 这个 Tool 是否允许 escalation（权限提升重试）；
- 当前 approval policy 是否允许询问用户；
- 网络是否是被策略拦住；
- unsandboxed execution（无沙箱执行）是否从根本上被禁止。

只有这些条件允许时，才可能在获得相应批准后做有限重试。

所以：

> **Retry 的权限永远不能高于 Policy 本身授予的权限。**

如果策略明确 Forbidden（禁止），反复 retry 不能把它“撞开”。

---

## 19. 网络批准和文件系统 Sandbox 是相互配合的两条边界

网络访问不能只靠“命令里有没有 curl”判断。一个 MCP Tool、Connector 或 shell 命令都可能通过不同方式产生外部网络副作用。

Tool Orchestrator 在准备一次 Sandbox Attempt（沙箱尝试）时，会同时计算 managed network（受管网络）是否生效，并在需要时通过 Network Approval（网络批准）路径建立对应的执行代理。源码中的 `begin_network_approval` / `finish_deferred_network_approval` 负责把一次网络授权和真正执行生命周期绑定起来。

如果第一次执行因为网络策略被拒绝，Sandbox error（沙箱错误）里还可以携带 network policy decision（网络策略决策）。Runtime 会区分：

~~~text
文件系统权限不足
和
网络访问被策略阻止
~~~

再决定有没有资格请求更高权限或新的网络批准。

这意味着一个命令即使仍然运行在 Sandbox 中，也可以只获得**经过批准的那部分网络能力**；反过来，允许某个网络域也不等于自动获得更宽的文件系统写权限。

所以 Permission（权限）不是一把从“只读”到“全权限”的单旋钮，而是文件系统、网络、执行环境和批准策略共同形成的执行约束。

---

## 21. Tool 并发不是模型想并行就直接并行

Tool Executor 可以声明 `supports_parallel_tool_calls`。

`ToolCallRuntime` 对同一个 Step 使用一个读写锁。支持并行的 Tool 拿 read lock（读锁），彼此可以同时执行；不支持并行的 Tool 拿 write lock（写锁），会等待当前并行调用结束，也会阻止新的并行调用进入。

这套机制真正约束的是 Host 执行，而不是只在 Prompt 里建议模型“请串行”。

因此：

~~~text
模型可以一次返回多个 Tool Call
≠
Runtime 必须把它们同时执行
~~~

最终并发权仍然属于 Tool Contract 和 Runtime。

---

## 21. 用户取消 Tool 时，历史仍然要闭合

每个 Tool Call 都带 Cancellation Token（取消令牌）。

如果用户取消时 Tool 已经到达不可安全回滚的 terminal outcome（终态），Runtime 会等待它真正结束；如果还可以中止，就 abort（终止）执行任务，并生成结构化 AbortedToolOutput（中止工具结果）。

为什么取消了还要有 Tool Result？

因为模型历史里已经有：

~~~text
call_id = c17
某个 Tool Call 已经发出
~~~

如果 Runtime 直接把任务杀掉却不补结果，下一轮模型会看到一个永远没有结局的调用。它可能误判副作用状态，甚至重复执行。

所以 Cancellation（取消）也是协议的一部分，不是一个简单 Boolean（布尔变量）。

---

## 22. Tool Failure 要区分“给模型修”还是“Runtime 已不可信”

`FunctionCallError` 的重要语义不是错误字符串，而是能不能继续 Agent Loop。

`RespondToModel` 表示这次 Tool Call 失败，但错误可以作为模型 observation（观察结果）返回，例如参数不合法、目标不存在、某个业务动作失败。模型下一轮还有机会修参数、换工具或停止。

`Fatal` 则表示 Runtime / protocol invariant（运行时或协议不变量）已经出问题，不能伪装成普通 Tool Failure 继续跑。

这就是为什么错误分类要在 Host 里完成。模型当然可以根据“文件不存在”调整计划，但模型不应该自行决定一个内部任务崩溃是否还能安全恢复。

---

## 23. Tool Result 回到模型前还会经过规范化和截断

工具函数“return”并不是生命周期结束。

Runtime 还要做 PostToolUse Hook（工具执行后钩子）、Tool Lifecycle 通知、Telemetry（遥测），再把结果转换成模型协议里的 Function Call Output / Custom Tool Output 等 item。

对于 MCP 等可能产生巨大结果的工具，还会根据 Tool 自己的 output token limit（输出 Token 上限）或模型 truncation policy（截断策略）限制模型可见内容。

因此真正的终点是：

~~~text
外部系统返回
↓
Host 接受 / 处理结果
↓
形成有界、协议合法的 model-visible Tool Result
↓
写入 canonical history
↓
下一次模型采样
~~~

工具执行成功但结果没有正确进入 History，同样属于严重故障。

---

## 24. “五万个工具怎么办”是工程推导，不是当前 Codex 规模声明

### 【源码事实】

当前 Codex 已经有：

- Registry 与 model-visible Router 分离；
- Direct / Deferred / Code Mode 等多种暴露面；
- BM25 Tool Search；
- Tool Search Handler Cache；
- MCP Tool Spec 硬预算；
- Skill metadata budget + progressive disclosure；
- Code Mode 作为另一种工具编排面。

这些都表明源码在主动控制能力规模和模型可见成本。

### 【基于源码的工程推导】

如果未来一个 Agent 真有数万甚至更多 Tool，可以沿当前架构继续做 namespace / provider 分层检索、Policy pre-filter（策略前置过滤）、BM25 + semantic retrieval（语义检索）混合召回，再只给模型 top-K 候选。

但这属于“从当前设计可以怎样扩展”，**不能写成当前 Codex 已经在五万个工具部署规模采用这些额外策略**。

这种事实与推导的边界，后面的工程篇也保持一致。

---

## 25. 用开头的任务把完整 Tool 生命周期串起来

用户说：

> “看看这个仓库为什么测试失败，必要时读 GitHub issue，但不要做未经批准的外部写操作。”

一次可能的真实路径是：

~~~text
StepContext 捕获当前环境 / MCP / ToolRouter
↓
模型先调用 exec_command 跑测试
↓
Registry / Hook 确认最终命令
↓
Approval / Sandbox 计算执行边界
↓
命令在选定 environment 中运行
↓
Tool Result 回填 History
↓
模型判断需要 GitHub 信息
↓
如果 GitHub MCP 是 Deferred：
  tool_search 找到相关 Tool
↓
模型发出 MCP Tool Call
↓
McpHandler 等待对应 Server ready
↓
使用这一步冻结的 MCP binding 执行
↓
Connector Policy / approval 继续约束副作用
↓
结果截断、记录并回填
↓
模型根据证据完成修复
~~~

看完整条链以后，就能理解为什么“会 Function Calling”还远远不等于“实现了成熟 Agent Tool Runtime”。

---

## 26. 源码核验入口

1. [`tools/src/tool_executor.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/tools/src/tool_executor.rs)：ToolExecutor 和 Exposure 的共享契约。
2. [`core/src/tools/spec_plan.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/spec_plan.rs)：不同来源 Tool 怎样汇总成当前 Step 的 Tool Router。
3. [`core/src/tools/registry.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/registry.rs)：注册、Hook、dispatch 与结果接受。
4. [`core/src/tools/router.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/router.rs)：模型 Tool Call 的归一化和路由。
5. [`core/src/tools/handlers/tool_search.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/handlers/tool_search.rs)：Deferred Tool 的 BM25 发现和缓存。
6. [`core/src/mcp_tool_exposure.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/mcp_tool_exposure.rs)：MCP 暴露、Connector Policy 和 spec budget。
7. [`codex-mcp/src/lib.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/codex-mcp/src/lib.rs) 与 [`rmcp-client/src/lib.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/rmcp-client/src/lib.rs)：MCP runtime / catalog / transport / auth。
8. [`ext/skills/src/extension.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/skills/src/extension.rs) 与 [`render.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/skills/src/render.rs)：Skill 接入和目录预算。
9. [`core/src/tools/code_mode/execute_handler.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/code_mode/execute_handler.rs) 与 [`code-mode-runtime`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/code-mode-runtime)：JavaScript Code Mode 和嵌套工具。
10. [`core/src/tools/orchestrator.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/orchestrator.rs)：批准、Sandbox 与受控 escalation。
11. [`ext/guardian-v2/src/async_scorer/approval.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/guardian-v2/src/async_scorer/approval.rs)：Guardian 怎样参与 Approval Review。
12. [`core/src/tools/parallel.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/parallel.rs)：并发 gate、取消和 Tool timing。
13. [`ext/extension-api/src/contributors/tool_lifecycle.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/extension-api/src/contributors/tool_lifecycle.rs)：扩展看到的最终 Tool 生命周期与 MCP provenance。

下一篇：[Codex Engineering & Evaluation →](04-engineering-evaluation.md)
