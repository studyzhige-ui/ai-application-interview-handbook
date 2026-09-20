# 03. Claude Code Tool Lifecycle｜从能力目录到动态发现、权限和真实执行

[← Memory](02-memory-lifecycle.md) · [Claude Code 总览](README.md) · [Engineering & Evaluation →](04-engineering-evaluation.md)

> **源码镜像基线：** `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`

Claude Code 的 Tool（工具）系统真正解决的不是：

> “模型怎样返回一个函数名和 JSON 参数？”

而是更长的一条链：

~~~text
产品拥有很多能力
→ 当前会话组装 Tool Pool（工具池）
→ 决定哪些 Tool 立即给模型、哪些延迟发现
→ Claude API 收到 Tool Schema（工具模式定义）
→ 模型生成 tool_use
→ Runtime 校验输入
→ PreToolUse Hook
→ Permission Decision
→ 必要时用户 / classifier / headless hook 批准
→ Tool 真正执行
→ PostToolUse Hook
→ 结果截断 / 持久化
→ tool_result 写回消息
→ 下一次模型采样
~~~

MCP、Skill、Subagent、Bash、Read / Edit 等能力最后都要落到这条控制链上。

---

## 1. `Tool` 在 Claude Code 里不是一个普通函数

最核心的类型定义在：

- `Tool.ts`

一个 Tool 除了 `call()` 以外，还可以定义：

-输入 / 输出 schema；
-给模型看的 description / prompt；
-当前是否 enabled；
-是否允许并发；
-是否只读；
-是否 destructive（有破坏性）；
-是否 open-world（会访问开放外部世界）；
-是否需要用户交互；
-是否来自 MCP / LSP；
-是否应该 defer（延迟加载）；
-最大结果体积；
-自己的 permission check；
-额外输入校验；
-结果怎样映射回 Tool Result。

这里不需要背完整字段。

真正值得理解的是：

> **Claude Code 把“模型如何理解这个能力”“Runtime 怎样执行”“安全系统怎样判断它”放在同一个 Tool contract（工具契约）周围。**

如果模型看到的 schema 和真正执行函数完全由两个系统维护，很容易版本漂移。

---

## 2. Tool Pool 从哪里来：不是只有 Bash / Read / Write

`tools.ts::getAllBaseTools()` 是基础能力的重要入口。

从当前源码可以看到 Claude Code 可能拥有非常广的能力：

- Bash / PowerShell；
- Read / Edit / Write；
- Grep / Glob；
- Web Search / Web Fetch；
- Agent；
- Skill；
- Todo / Task；
- Worktree；
- MCP Resource；
- LSP；
- Team / SendMessage；
- REPL；
- Sleep / Cron；
-以及不同 feature gate 下的内部工具。

另外，AppState（应用状态）里还会不断加入 MCP Tool。

因此“Claude Code 有哪些 Tool”不是一个永远固定的数组。

它受：

-平台；
-feature gate；
-当前模式；
-用户配置；
-MCP 连接；
-Agent 类型；
-Permission mode；

共同影响。

也因为 Tool Set 会变化，源码非常关注一件事：

> **工具定义变化会破坏 Prompt Cache。**

`tools.ts` 的注释甚至提醒某些动态配置必须和 Tool 列表保持同步，以便跨用户稳定缓存 System Prompt / Tool definitions。

---

## 3. “系统里有 Tool”和“这一轮把完整 Tool Schema 发给模型”不是一回事

如果 MCP Server 很多，Tool 定义可能占掉非常大的 Context。

Claude Code 没有把解决办法写成：

> “Context Window 够大就全发。”

它有专门的 Deferred Tool（延迟工具）机制。

关键实现：

- `utils/toolSearch.ts`
- `tools/ToolSearchTool/`
- `services/api/claude.ts`

当 Tool Search 开启时，一部分 MCP Tool 或 `shouldDefer` Tool 会使用 Claude API 的：

`defer_loading: true`

这表示模型知道有动态 Tool discovery（工具发现）能力，但不需要一开始就加载所有完整 Tool Schema。

因此：

~~~text
Full Tool Pool
        ↓
判断哪些 Tool 可延迟
        ↓
首轮 API 只发送常驻 Tool + ToolSearch
        ↓
模型需要某类能力
        ↓
ToolSearch 返回 tool_reference
        ↓
后续请求只加载已经发现的 Tool Schema
~~~

这和 Codex Deferred Tool 的整体目标相似，但 Claude Code 直接利用了 Claude API 的 dynamic tool loading（动态工具加载）协议。

---

## 4. Tool Search 什么时候启用：甚至会看 Tool 定义占了多少 Context

`utils/toolSearch.ts` 当前支持多种模式。

最值得学习的是 auto mode（自动模式）。

源码会估算 Deferred Tool definitions（延迟工具定义）的 Token 总量，再把它和当前模型 Context Window 比较。

默认自动阈值约为 Context Window 的 10%，并允许通过配置调整。

如果 Token counting API（Token 计数接口）不可用，还会退回字符估算。

这代表一个很成熟的设计：

> **是否需要 Tool Search，不应该只看“工具数量”，而要看这些工具实际会吃掉多少模型上下文。**

20 个 schema 极复杂的 Tool，可能比 200 个很小的 Tool 更值得延迟加载。

因此规模指标应该是：

~~~text
tool definition tokens
~~~

而不只是：

~~~text
tool count
~~~

---

## 5. ToolSearchTool 怎样让模型找到具体工具

`tools/ToolSearchTool/ToolSearchTool.ts` 是模型可调用的搜索入口。

当前实现支持：

-普通关键词搜索；
-`select:<tool-name>` 这种精确选择；
-有界返回，默认只返回少量候选。

它的搜索逻辑会更重视 Tool name（工具名）和名字组成部分，同时也利用 `searchHint`（搜索提示）和 description。

因此它不是一个“随便对 description 做 contains”。

搜索结果会形成 `tool_reference`。

模型拿到 reference 后，Claude API 在后续请求中可以把对应完整 Tool definition 展开。

### 为什么不是搜索完就直接执行

Tool Search 只解决：

> “这个能力叫什么、schema 是什么？”

真正执行仍然要经过：

-模型下一步选择；
-input validation；
-Permission；
-Tool execution。

Discovery（发现）和 Execution（执行）是两个不同安全边界。

---

## 6. 为什么 discovered Tool 要写进消息历史

动态 Tool Loading 有一个容易忽略的问题。

如果 Runtime 只在进程内维护：

~~~text
discoveredTools = Set(...)
~~~

那么：

- Compaction 后可能丢；
- Resume 后一定丢；
-模型请求和持久化 transcript 之间不一致。

Claude Code 让 `tool_reference` 进入消息历史，再通过：

`extractDiscoveredToolNames(messages)`

恢复“哪些 Deferred Tool 已经被发现”。

完整 Compaction 又会把 pre-compact discovered set 写进 compact boundary metadata。

因此 Tool discovery state（工具发现状态）本身也是 Context State（上下文状态）。

这说明“上下文”不仅包括自然语言消息，还包括会改变后续 API 能力面的协议状态。

---

## 7. Deferred Tool Pool 变化时怎样通知模型

MCP Server 可以中途连接 / 断开。

Tool Pool 因此不是只在 Session 启动时确定一次。

Claude Code 的 query loop 会在 Tool Result 后 refresh tools（刷新工具），让刚连接的 MCP Server 能在后续 iteration 出现。

`utils/toolSearch.ts` 还维护 deferred tools delta（延迟工具目录差异），用于表示：

-新增了哪些延迟 Tool；
-移除了哪些 Tool。

如果目录变化时完全重发一大份列表，不仅浪费 Context，也更容易破坏 Prompt Cache。

因此动态工具系统同样在做“增量状态同步”。

---

## 8. MCP Tool 是怎样进入 Claude Code 普通 Tool 系统的

MCP 主实现之一：

- `services/mcp/client.ts`

Server 连接成功后，Claude Code 会发：

`tools/list`

拿到远端 Tool 后，再把它们转换成普通 Claude Code `Tool`。

转换过程中会补上很多 Runtime 需要的信息。

例如：

-完全限定名通常是 `mcp__server__tool`；
-`mcpInfo` 保留真实 server / tool identity；
-远端 `searchHint` 会先清理换行和多余空白；
-`alwaysLoad` 可以来自 MCP metadata；
-description 有最大 Prompt 长度；
-readOnlyHint 会影响只读 / 并发判断；
-destructiveHint 和 openWorldHint 会进入安全语义；
-远端 input schema 会成为 Tool schema。

这里特别值得注意 `searchHint` 的清洗。

源码注释说明：远端 MCP metadata 是不可信输入；如果允许它带换行直接进入 Deferred Tool list，可能注入额外伪造行。

这就是 Prompt Injection 防护在 Tool Catalog 层的一个具体例子。

---

## 9. MCP 连接本身也有生命周期，不只是 `callTool()`

Claude Code 支持多种 MCP transport（传输方式），包括本地 stdio 和远端 HTTP / SSE 等。

`getMcpToolsCommandsAndResources` 会把本地 Server 和远端 Server 分成不同并发组。

原因很实际：

-本地 stdio 需要创建进程，过高并发会争抢机器资源；
-远端 Server 主要是网络连接，可以允许更高并发。

源码还会：

-直接跳过 disabled server；
-缓存 needs-auth 状态，避免每隔一段时间重复做注定失败的 OAuth probe（探测）；
-连接成功后并发获取 Tool、Command、Skill / Resource；
-连接出错后仍向 AppState 报告 failed / needs-auth 状态，而不是把所有 Server 启动当成一个全有或全无事务。

所以 MCP startup 本身也是一个有 partial success（部分成功）的能力发现过程。

---

## 10. MCP 断线以后怎样恢复

远端连接可能出现：

- ECONNRESET；
- ETIMEDOUT；
- EPIPE；
- SSE reconnect exhaustion；
- HTTP Session 过期。

源码不会只把当前 Promise 留在永远 pending。

当连续 terminal connection error 达到条件时，它会真正 close transport（关闭传输层），让所有 pending MCP request 明确 reject（拒绝），同时清理：

-connection cache；
-tool fetch cache；
-resource cache；
-command cache。

下一次调用才会拿一条新连接和新 Tool Catalog。

Tool call 本身遇到 MCP session expiry 时，还有一次受控的 session recovery retry（会话恢复重试）。

这说明：

> **连接重试必须同时刷新能力目录，否则新连接仍可能继续使用旧 Server 的 Tool metadata。**

---

## 11. URL Elicitation：有些 MCP Tool 执行中途还要用户完成外部步骤

MCP Tool 可能返回特定错误，要求用户打开 URL 完成授权 / 操作。

Claude Code 对这类 URL elicitation（URL 引导请求）有单独处理。

它可以先运行 Elicitation Hook；如果 Hook 已经自动解决，就无需 UI。

否则：

- REPL 可以进入交互流程；
- SDK / print mode 可以交给 structured callback；
-用户完成后再重试 MCP Tool。

重试次数有上限，不能因为外部授权一直失败而无限循环。

这类机制说明 Tool 生命周期有时并不是：

~~~text
call → result
~~~

而是：

~~~text
call
→ Runtime 请求额外交互
→ 用户 / Hook 决策
→ retry
→ result
~~~

---

## 12. Skill 为什么不是 MCP Tool 的另一个名字

Skills 主实现：

- `skills/loadSkillsDir.ts`
- `tools/SkillTool/`

本地 `/skills/` 采用：

~~~text
skill-name/
└── SKILL.md
~~~

目录格式。

`SKILL.md` 的 frontmatter（文件头元数据）可以定义：

- description；
-allowed-tools；
-when-to-use；
-model；
-effort；
-hooks；
-`context: fork`；
-agent；
-paths；
-是否允许用户直接调用；
-是否允许模型主动调用。

但这里不要又退回字段背诵。

最重要的设计是：

> **发现 Skill 时只需要很小的 metadata；真正调用以后才读取完整 Markdown。**

源码中的 `estimateSkillFrontmatterTokens` 甚至明确只估 name / description / whenToUse，因为 full content（完整内容）不应该在发现阶段进入 Prompt。

这就是 Progressive Disclosure（渐进式展开）。

---

## 13. Skill 调用以后，可以改变这一小段执行上下文

`SkillTool` 并不是只把 SKILL.md 文本返回给模型。

它执行 Skill 后，可以产生新的 messages，并通过 `contextModifier` 修改后续 ToolUseContext。

例如一个 Skill 的 frontmatter 指定：

~~~text
allowed-tools: ...
model: ...
effort: ...
~~~

那么调用以后，Runtime 可以：

-临时把这些 Tool 加到允许规则；
-覆盖当前模型；
-覆盖 effort。

模型覆盖还会保留类似 `[1m]` 的 Context Window suffix，避免一个 Skill 指定 `opus` 后意外把原本 1M Context 会话降回默认窗口。

这个细节说明 Skill 是一个真正的 Runtime extension（运行时扩展），不只是 Prompt 模板。

---

## 14. `context: fork` 的 Skill 为什么要拉起 Subagent

Skill 可以选择 inline execution（内联执行），也可以：

`context: fork`

此时 `SkillTool` 会走 `executeForkedSkill`，用 `runAgent` 在隔离的 Subagent 中执行 Skill。

价值在于：

-复杂 Skill 不必污染主 Context；
-可以有独立 Token Budget；
-可以有独立 Agent definition / model；
-执行完只把最终结果带回主会话。

这是一种 Context Isolation（上下文隔离）。

所以“Skill 的 progressive disclosure”不只是文件懒加载，还可以进一步做到：

> **连 Skill 的执行轨迹都不进入主线程全部历史。**

---

## 15. MCP Skill 为什么禁止在 Markdown 中执行内联 shell

`skills/loadSkillsDir.ts` 支持某些本地 Skill Prompt 中执行内联 shell command。

但对于 `loadedFrom === 'mcp'` 的 Skill，源码明确禁止从远端 Markdown body 中执行这种内联 shell。

理由非常直接：

> MCP Skill 是远端、不可信内容。

如果远端 Skill 的 Markdown 里写：

~~~text
!curl ...
!rm ...
~~~

而 Loader 在“加载 Prompt”阶段直接执行，就相当于把远端文本变成代码执行入口。

所以远端 Skill 和本地 Skill 即使最后都表现为 Skill，也有不同的 trust boundary（信任边界）。

---

## 16. 模型真正发出 Tool Call 后，第一步是输入校验

Tool execution 主要在：

- `services/tools/toolExecution.ts`

Claude 返回 `tool_use` 后，Runtime 会先找到 Tool，再做两层校验。

第一层是 Zod input schema（输入模式校验）。

第二层是 Tool 自己的 `validateInput`，处理 schema 无法表达的语义条件。

例如一个路径字段是 string，并不代表：

> 这个路径当前允许访问。

所以 schema-valid（结构合法）和 semantic-valid（语义合法）不能混成一层。

---

## 17. PreToolUse Hook 为什么在 Permission 前面

校验通过以后，Claude Code 会跑 PreToolUse Hook。

Hook 能：

-注入 additional context；
-修改 Tool input；
-直接拒绝；
-返回 permission decision；
-要求停止继续。

这意味着 Permission 不应该只检查模型原始输入。

如果 Hook 把：

~~~json
{"path":"./safe.txt"}
~~~

改成：

~~~json
{"path":"../secret.txt"}
~~~

后续 Permission 必须基于修改后的 input 决策。

Claude Code 的执行链允许 Hook result 进入后续 permission resolution，而不是把 Hook 当作纯日志 callback。

---

## 18. Permission 决策不是一个弹窗

真正的 Permission 核心在：

- `utils/permissions/permissions.ts`
- `hooks/useCanUseTool.tsx`

Tool Permission Context 会综合多来源规则：

- policy settings；
-user / project / local settings；
-CLI；
-command / Skill；
-session temporary rules。

规则可以：

- always allow；
-always deny；
-always ask。

MCP Tool 权限匹配还会坚持使用 fully-qualified identity（完全限定身份），即使 SDK 模式为了展示把名字前缀隐藏，也不能因此让一个远端 MCP `Write` 错误匹配内置 `Write` 的权限规则。

这体现出安全系统一个很重要的原则：

> **显示名可以变化，安全 identity 不能丢。**

---

## 19. ask 以后由谁决定：交互式、自动模式、Subagent 都不一样

当 Permission result 是 `ask` 时，不一定立刻弹 UI。

### Interactive REPL

`useCanUseTool` 可以：

-先等待自动检查；
-让 Coordinator 决策；
-让 Swarm worker 路径处理；
-利用 speculative Bash classifier（预判分类器）；
-最后才进入 Permission Dialog。

### Auto Mode

某些场景下可以用 AI classifier 判断是否自动批准。

但源码专门保护一些 safety check（安全检查）：如果标记为不能由 classifier 批准，那么即使 Auto Mode 也不能偷偷放行。

### Headless / Async Agent

无法显示 Permission UI 时，可以先运行 PermissionRequest Hook。

如果没有 Hook 给出明确许可，默认不能假装用户同意。

所以：

> **“ask”是一种权限状态，不等于“一定会出现一个弹窗”。**

不同 Host / Agent 类型对 ask 有不同 resolution path（解决路径）。

---

## 20. Sandbox 为什么又是 Permission 之外的一层

即使 Permission 允许某个 Bash Tool，进程实际执行时仍然可以进入 OS Sandbox（操作系统沙箱）。

相关实现：

- `utils/sandbox/sandbox-adapter.ts`

Sandbox 会把 Settings 转成真正的：

- filesystem allow / deny；
-network domains；
-workspace write；
-managed policy。

源码里有不少真实安全加固。

例如它会阻止 Sandbox 内写 Claude Code settings 文件，因为修改 settings 本身可能改变未来权限。

它还特别阻止写 `.claude/skills`，注释明确指出 Skills 会被自动发现 / 加载，拥有高能力，如果攻击者能在 Sandbox 内种植 Skill，就可能形成持久权限提升路径。

还有针对 bare Git repository + fsmonitor 等 sandbox escape（沙箱逃逸）风险的防护。

所以 Sandbox 不是“让 Bash 更安全”的泛化名词，而是第二道真正的 OS enforcement（系统强制执行）。

---

## 21. Tool 并发怎样决定

`services/tools/toolOrchestration.ts` 会依据：

`tool.isConcurrencySafe()`

决定哪些 Tool Call 可以并发运行。

例如只读 Tool 更可能安全并发，而共享状态写操作需要更谨慎。

对于 MCP Tool，远端 `readOnlyHint` 会映射到 Claude Code 的 read-only / concurrency 语义。

这让 MCP Server 自己的 annotations（注解）参与 Runtime 调度，但最终仍由 Host 决定如何解释。

---

## 22. Streaming Tool Execution：为什么工具可能在模型还没流完时就开始

Claude Code 还有 `StreamingToolExecutor`。

模型流式返回 `tool_use` 时，Runtime 不一定非要等整条 assistant message 完成才开始所有工具。

对长模型输出和慢工具，这可以降低总体 latency（延迟）。

但它带来一个严重工程问题：

> **如果模型 streaming request 失败，然后 API 层重新 fallback / retry，会不会把刚才已经启动的 Tool 再执行一次？**

`query.ts` 对 fallback 路径专门做保护：

- tombstone（墓碑标记）旧的 partial assistant message；
- discard streaming executor results；
-避免旧 response 的 Tool Result 和新 response 混在一起。

源码 API 层也有关于 streaming → non-streaming fallback 与 Tool double execution（双执行）风险的防护注释。

这说明“提前执行 Tool”不是纯性能优化。

任何 speculative / streaming execution（推测式 / 流式执行）都必须同时设计：

> **请求重试时如何保证副作用不重复。**

---

## 23. Tool Result 返回后还会发生什么

Tool `call()` 成功以后还没有结束。

Runtime 会：

1. 把输出映射成 Tool Result block；
2.必要时存储 / 替换超大结果；
3.运行 PostToolUse Hook；
4.某些 Hook 可以修改最终 Tool output；
5.把结果作为 user-side `tool_result` message 写入下一轮历史；
6.应用 Tool 返回的 `contextModifier`。

因此一个 Tool 甚至可以影响下一轮运行上下文，而不只是返回文本。

SkillTool 就会利用 contextModifier 修改 allowed tools / model / effort。

所以 Tool Result 是：

> **Observation + 可能的 Runtime State Transition（运行时状态变更）。**

---

## 24. 用一个完整例子串起来

用户说：

> “去日历里找下周的空闲时间，然后把结果写到项目计划里。”

当前连接了很多 MCP Server，Tool definitions 已经超过 Tool Search 自动阈值。

首轮模型不会看到几百个完整 MCP schema，只看到常驻 Tool + ToolSearch。

模型调用：

~~~text
ToolSearch("calendar availability")
~~~

结果包含相关 `tool_reference`。下一轮 API 请求才加载对应 Calendar MCP Tool 的完整 schema。

模型发出 Tool Call。Runtime 先做 schema / semantic validation，再跑 PreToolUse Hook。

MCP Tool 的默认 permission 是 passthrough（继续交给上层权限系统），最终权限规则发现这个 Server 尚未永久允许，于是进入 ask。

用户批准后，Claude Code 调用 MCP Server。如果远端 Session 已过期，Runtime 清理旧连接并允许一次 session recovery retry。

Calendar Tool 返回很大结果，Tool Result Storage / Budget 层把它控制在可用范围，再写回模型 Context。

模型随后调用本地 Edit Tool 修改项目计划。这个写操作再次经过自己的路径校验、Permission 和 Sandbox。

这条完整链说明：

~~~text
Tool discovery
≠
Tool authorization
≠
Tool execution
≠
Tool result delivery
~~~

四个阶段必须分别正确。

---

## 25. 源码锚点

1. [`Tool.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/Tool.ts)：Tool contract、ToolUseContext、Permission Context。
2. [`tools.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools.ts)：基础 Tool Pool。
3. [`utils/toolSearch.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolSearch.ts)：Deferred Tool、自动阈值、discovered state。
4. [`tools/ToolSearchTool/ToolSearchTool.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/ToolSearchTool/ToolSearchTool.ts)：搜索和 tool_reference。
5. [`services/api/claude.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts)：真正给 API 的 Tool Schema、defer_loading 和 cache。
6. [`services/mcp/client.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts)：MCP 连接、tools/list、转换、重连与 Tool 调用。
7. [`skills/loadSkillsDir.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/skills/loadSkillsDir.ts)：SKILL.md、frontmatter、来源和安全边界。
8. [`tools/SkillTool/SkillTool.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SkillTool/SkillTool.ts)：Skill 调用、inline / fork、contextModifier。
9. [`services/tools/toolExecution.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts)：validation → Hook → Permission → execution → PostHook → result。
10. [`services/tools/toolOrchestration.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolOrchestration.ts)：Tool 并发调度。
11. [`services/tools/StreamingToolExecutor.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/StreamingToolExecutor.ts)：流式 Tool 执行。
12. [`utils/permissions/permissions.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/permissions/permissions.ts) 与 [`hooks/useCanUseTool.tsx`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/hooks/useCanUseTool.tsx)：权限规则与不同 Host 的 ask 处理。
13. [`utils/sandbox/sandbox-adapter.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sandbox/sandbox-adapter.ts)：真正 OS Sandbox 和网络 / 文件系统边界。

下一篇：[Claude Code Engineering & Evaluation →](04-engineering-evaluation.md)
