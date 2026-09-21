# 03. Codex Tool Lifecycle｜一个模型动作怎样变成真实、受控的执行

[← Memory](02-memory-lifecycle.md) · [Codex 总览](README.md) · [Engineering & Evaluation →](04-engineering-evaluation.md)

> **源码基线：** `openai/codex@bb054a2b03f15787dcc2f9bd8ebfde713bc5b695`

Tool（工具）是 Coding Agent 最容易被低估的一部分。

从模型视角看，它似乎只做了一件事：

```text
调用 exec_command({"cmd": "pytest"})
```

但从 Codex Runtime（运行时）看，这个动作真正落地之前，至少要回答：

- 这个工具是谁注册的；
- 本轮模型为什么能看见它；
- 当前权限允许执行到什么范围；
- 参数有没有被 Hook（钩子）修改；
- MCP Server 是否已经 ready；
- 需要不需要 Approval（用户批准）；
- 应该进入哪个 Sandbox（沙箱）；
- 有没有网络权限；
- 能不能和其他 Tool 并发；
- 用户这时取消怎么办；
- 结果太大怎么办；
- 最终怎样让模型知道执行结果。

因此 Tool Lifecycle（工具生命周期）不是“函数调用”，而是一条完整的控制链。

---

## 1. 先把三个问题分开：系统有什么、模型看到什么、Runtime 允许什么

这是理解 Codex Tool System 最关键的一步。

### 系统有什么能力

Codex 会把可执行能力注册到 `ToolRegistry`（工具注册表）。

能力来源很多，例如：

- Core 内置工具；
- MCP Tool；
- Extension Tool（扩展工具）；
- Dynamic Tool（动态工具）；
- Hosted Model Tool（模型服务侧工具）；
- Code Mode（代码模式）需要的内部执行能力。

“注册了”只说明：

> **Host（宿主程序）知道这个工具是谁、它的 schema（参数结构）是什么、最后应该调用哪个执行器。**

### 模型这轮能看到什么

真正给模型的是 `ToolRouter.model_visible_specs()`。

这是一份经过当前 StepContext、Feature、Policy、Tool Mode 和 AllowedTools 共同筛选后的模型可见工具集。

所以：

```text
Registry 里存在
≠
模型这轮可见
```

### Runtime 最终允许什么

即使模型已经看见并选择了一个 Tool，也还没有获得“执行授权”。

真实执行还要经过：

- 参数与 payload（负载）检查；
- Hook；
- Approval；
- Guardian（安全审查）；
- Permission Profile（权限配置）；
- Sandbox；
- Network Policy（网络策略）。

因此更完整的三层结构是：

```text
Capability Registry
系统知道有哪些能力
        ↓
Model-visible Projection
这一轮告诉模型哪些能力
        ↓
Execution Authorization
模型选中以后，Runtime 再判断这次具体动作能否执行
```

这三层如果混在一起，就很容易出现“只要从 Prompt 里隐藏工具就安全”这种错误设计。

---

## 2. ToolExecutor 是什么：把“模型说明”和“真实执行器”绑在一起

共享 Tool 抽象主要在：

- `codex-rs/tools/src/tool_executor.rs`

`ToolExecutor`（工具执行器）并不只是一个函数指针。

它至少把几件事绑定到一起：

- 这个工具叫什么；
- 给模型看的 `ToolSpec`（工具说明）是什么；
- 它默认应该怎样暴露；
- 它是否支持并行调用；
- 真正的 `handle()` 实现是什么。

Core 又在此基础上增加 `CoreToolRuntime`，提供 Codex Runtime 特有能力，例如：

- 这个 spec 是否可以复用；
- MCP 工具属于哪个 server；
- 执行前是否需要等某个服务 ready；
- 怎样生成 Hook 输入；
- Hook 修改参数以后怎样重新构造调用；
- 怎样记录 telemetry（遥测）；
- 结果被接受后要不要额外登记。

为什么要把 spec 和 runtime 绑在一起？

因为一个很危险的系统结构是：

```text
A 表：给模型看的 tool schema
B 表：真正执行的函数
```

如果两边版本漂移，模型看到的参数契约和 Runtime 真正接受的参数可能不一致。

Codex 的 Tool Runtime 设计尽量让“说明”和“执行”属于同一个工具对象，再由 Router 在每次 Step 上做最终投影。

---

## 3. 一个 Step 的 Tool Set 是怎样生成的

关键入口是：

- `codex-rs/core/src/tools/spec_plan.rs::build_tool_router`

一次 Step 捕获时，Runtime 会从多个来源收集工具。

先有 Core Tool，然后接入 MCP Tool，再接 Extension Tool 和 Dynamic Tool，最后把一些模型服务原生工具一起纳入计划。

这一步不是简单 concatenate（拼接数组）。中间还会处理：

- `AllowedTools`（允许工具集合）；
- 同名冲突；
-当前模型支持什么 Tool Mode；
-哪些 Tool 应直接暴露；
-哪些 Tool 应延迟发现；
-Code Mode 应该拿到哪些嵌套能力；
-App / Connector Policy。

最后得到一份 `ToolRouter`。

可以把它看成：

> **“这一份 StepContext 下，模型和 Runtime 对 Tool 世界的共同契约。”**

前一篇说过，Tool Call 后面会保留产生它的 `StepContext`。所以即使 Tool Catalog 后来刷新，旧调用也不会随便套用新 Router。

---

## 4. ToolExposure 为什么不是简单的 visible / hidden

Codex 当前源码中，工具暴露方式不止“看得见”和“看不见”。

共享 `ToolExposure` 包含 Direct、Deferred、DirectModelOnly、DeferredModelOnly、CodeModeOnly、Hidden 等形态。

不需要死记这些枚举。更重要的是理解它们在回答三个问题：

### 要不要一开始就把 schema 发给模型

Direct（直接暴露）的 Tool 会进入初始模型工具列表。

### 能不能以后通过搜索再发现

Deferred（延迟暴露）的 Tool 不一开始展开完整 schema，但可以通过 `tool_search` 找到。

### 能不能给 Code Mode 内部脚本调用

有些 Tool 适合普通模型调用，有些也允许 Code Mode 内嵌调用，有些只给其中一个 surface（暴露面）。

因此 ToolExposure 解决的是：

> **一个已经注册的能力，应该在哪个模型交互面上出现。**

这对大规模 Tool Catalog 尤其重要。

---

## 5. 为什么几千个 MCP Tool 不应该全部塞进首轮请求

MCP（Model Context Protocol，模型上下文协议）让外部 Server 提供 Tool。

Codex 会把 MCP Server 返回的工具转换成自己的 `ToolInfo` 和 `McpHandler`，再注册进 Tool Registry。

相关源码：

- `codex-rs/codex-mcp/`
- `codex-rs/core/src/mcp_tool_exposure.rs`
- `codex-rs/core/src/tools/handlers/mcp.rs`

如果一个用户连接了很多应用，一个 Server 又暴露很多 Tool，最直接的实现会变成：

```text
所有 MCP Tool schema
→ 每一轮全部发给模型
```

这会迅速增加 Context、破坏 Prompt Cache，并增加模型选错工具的概率。

所以当 Tool Search（工具搜索）开启时，Codex 可以把 MCP Tool 默认放到 Deferred 暴露面。

模型第一轮只需要知道存在 `tool_search`。

当它确实需要“日历”能力时：

```text
模型调用 tool_search("calendar create event")
        ↓
Runtime 在 deferred catalog 里检索
        ↓
返回少量匹配 Tool 的 LoadableToolSpec
        ↓
模型再选择具体工具
```

这才是“注册很多能力但不把全部 schema 一次塞进 Prompt”的真实实现。

---

## 6. tool_search 当前怎样找工具：BM25 只是实现，不是架构本身

当前固定快照中：

- `codex-rs/core/src/tools/handlers/tool_search.rs`

使用 BM25（基于词频与逆文档频率的稀疏检索算法）为 Deferred Tool 建索引。

它不会只索引一句 description（描述）。

以 MCP Tool 为例，search text（搜索文本）会组合：

- 工具规范名；
- callable name；
- MCP Server 名；
- title；
- description；
- Connector 名；
- namespace（命名空间）说明；
- Plugin display name；
- input schema 的字段名。

所以用户说“创建日历事件”时，搜索不必精确命中某一句描述。

### 为什么还有 ToolSearchHandlerCache

每个 Step 都可能重新生成 Tool Router，但 Tool Catalog 很多时候并没有变化。

如果每次都为几千个 Tool 重建 BM25 索引，会浪费 CPU。

因此 `ToolSearchHandlerCache` 会复用稳定 Runtime 的索引；只有动态 Tool metadata（元数据）或候选来源真的变化时才重建。

这里要区分：

> Tool Search Cache 是本地目录索引缓存，不是 Prompt Cache。

### 不要把“BM25”泛化成 Codex 的永恒设计

源码事实是：这个固定 commit 当前使用 BM25。

工程层面真正稳定的设计思想是：

```text
完整 Tool Registry
→ 只给模型少量可见入口
→ 需要时检索候选工具
→ 再加载具体 schema
```

未来检索算法换成 hybrid retrieval（混合检索）也不会改变这个架构边界。

---

## 7. 为什么还要给 MCP spec 设置硬大小上限

Deferred 已经能减少首轮 Tool 数量，但还不够。

某些 Agent Plugin MCP spec 在当前源码里还有明确字节预算：

- 单个 spec 不能无限大；
- 一组相关 spec 的累计体积也不能无限增长；
- 超出预算的工具可以保持注册，但不进入模型可见面。

相关代码在：

- `codex-rs/core/src/mcp_tool_exposure.rs`

这和 Context 篇的原则完全一致：

> **任何自动进入 model-visible context 的内容都必须有硬上限。**

大 Context Window 并不是“可以不做预算”的理由。

---

## 8. Skill 为什么不是另一种 Tool

Codex 还有 Skills（技能）系统：

- `codex-rs/skills/`
- `codex-rs/ext/skills/`

Tool 回答的是：

> **Runtime 能执行什么动作？**

Skill 更接近：

> **在某类任务里，模型应该怎样组织动作、遵守哪些工作流程、什么时候读取哪些参考材料。**

例如一个“创建专业 PPT”的 Skill 可能告诉模型：

- 先读模板；
- 再分析内容结构；
- 用哪个脚本生成；
- 最后怎样检查版式。

真正执行文件、脚本或外部服务，仍然依赖 Tool。

因此：

```text
Skill
= 使用能力的方法与知识包

Tool
= Runtime 可以执行的动作接口
```

两者会配合，但不是一回事。

---

## 9. 大量 Skill 怎样避免吃光 Context

Codex 自带的 Skill Creator 说明和 `ext/skills/src/render.rs` 都明确采用 progressive disclosure（渐进式展开）。

模型不是一开始看到每个 Skill 的全部文件。

而是：

```text
第一层：name + description
用于发现这个 Skill 是否相关
        ↓
第二层：SKILL.md
真正决定使用以后才读取
        ↓
第三层：references / scripts / assets
执行过程中需要哪一份再读取哪一份
```

第一层 catalog（目录）本身也有预算。

当前源码会根据：

-显式配置的 token budget；
-模型 Context Window 的一定比例；
-默认字符预算；

决定最多展示多少 Skill metadata（技能元数据）。

当空间不够时，先缩短 description；再不够才省略部分 Skill。并且 description 预算是近似公平分配，不让第一个 Skill 把剩余空间全部占完。

这就是为什么“几千 Skill 怎么办”的答案不能是：

> “换一个 1M Context 的模型。”

成熟实现首先要做能力目录的渐进展开。

---

## 10. 模型发出 Tool Call 以后，真正执行前发生什么

模型输出会先被 `ToolRouter::build_tool_call` 转成 Codex 内部统一的 `ToolCall`。

无论 Responses API 返回的是 Function Call、Custom Tool Call 还是 Tool Search Call，Runtime 都会把它标准化成：

- tool name；
- call id；
- payload；
-必要的加密参数信息。

然后 Registry 开始真正 dispatch（分发）。

### 第一道门：这个 Tool 是否真的存在、payload 类型是否匹配

如果模型调用一个没有注册的工具，Runtime 不会靠名字猜。

如果一个只接受 Function payload 的 Handler 收到了完全不同类型的 payload，也不会继续“尽量执行”。

这种协议层不一致通常应该被视为严重错误。

### 第二道门：PreToolUse Hook

Tool 可以生成 Hook-facing input（面向钩子的输入）。

Hook 可以：

- 放行；
- 阻止；
- 甚至修改 Tool Input。

MCP Handler 就支持把 Hook 改写后的 JSON 参数重新序列化，再进入后续执行。

但这也意味着：Hook 之后的参数仍然要经过真正 Handler 与权限系统，而不能因为“原参数已经检查过”就跳过安全边界。

---

## 11. Approval、Permission、Sandbox 为什么是三件不同的事

模型选择 Tool 以后，`ToolOrchestrator` 才真正决定怎样运行。

源码：

- `codex-rs/core/src/tools/orchestrator.rs`

这里容易把几个概念混在一起。

### Approval：用户愿不愿意让这次动作发生

例如某个命令需要扩大权限，Runtime 可能向用户请求批准。

Approval 解决的是：

> **用户授权。**

### Permission Profile：这个 Thread（线程） / Environment（环境） 最多允许什么

即使用户没有被弹窗询问，系统也有一份结构化权限范围，例如 workspace read/write、网络等。

Permission 解决的是：

> **系统能力上限。**

### Sandbox：这次进程实际上被怎样隔离

最终命令还要在某种沙箱里运行，例如 Linux / Windows 对应的隔离实现。

Sandbox 解决的是：

> **技术执行边界。**

所以一条安全链更接近：

```text
模型建议执行
→ Policy 判断是否允许
→ 必要时请求 Approval
→ 根据 Permission Profile 计算文件 / 网络能力
→ 选择 Sandbox
→ 真正启动进程
```

不能用 Prompt 里的“请谨慎操作”代替这些 Runtime 控制。

---

## 12. Sandbox Denied 为什么有时还会再试一次

第一次在受限 Sandbox 中执行失败，不一定说明用户请求本身非法。

可能只是当前命令需要访问一个被沙箱拦住、但用户确实可以授权的资源。

因此 `ToolOrchestrator` 会区分：

- Policy 明确禁止；
- 只是当前 Sandbox 权限不足。

只有后者，并且当前 approval policy（批准策略）允许时，Runtime 才可能请求更高权限，再做有限的 escalation retry（权限升级重试）。

这条原则非常重要：

> **Retry 能扩大执行环境，但不能扩大 Policy 本身。**

如果 Policy 已经说 Forbidden（禁止），不能通过多试几次把它绕过去。

---

## 13. 并发 Tool 是怎样控制的

`ToolCallRuntime` 在同一 Step 上共享一个读写锁。

源码：

- `codex-rs/core/src/tools/parallel.rs`

如果一个 Tool 声明支持 parallel tool calls（并行工具调用），它拿 read lock（读锁），多个并行安全 Tool 可以同时执行。

不支持并行的 Tool 拿 write lock（写锁），会等其他并发工作结束，并阻止新的并行调用进入。

所以 `supports_parallel_tool_calls` 不是一句给模型看的描述，它真正影响 Runtime 调度。

为什么不能所有 Tool 都并发？

因为有些工具会竞争同一个外部状态，例如：

- 同时修改同一个文件；
- 同时操作一个终端 Session；
- 同时改变共享环境。

并发安全是执行器的性质，不是模型自己猜出来的。

---

## 14. 用户取消以后，为什么还要生成 Tool Result

Tool Call 会绑定 CancellationToken（取消令牌）。

如果用户在执行过程中取消：

```text
Tool Call 已经写进模型历史
        ↓
Runtime 中止执行任务
        ↓
如果什么都不记录
        ↓
历史里只剩 Call，没有 Result
```

下一轮模型就会面对一个悬空动作。

因此 Codex 会尽量产生结构化 `AbortedToolOutput`（工具中止输出），并完成对应 call id 的结果。

对于 `exec_command`，结果甚至会带运行了多久以及“aborted by user”之类的信息。

这说明取消不是：

> “把 future kill 掉就完了。”

取消也必须维护 Context 协议一致性。

---

## 15. Tool 执行失败以后，为什么有些错误给模型看，有些直接终止

Codex Tool Error（工具错误）区分可反馈给模型的失败和 Runtime fatal（致命）失败。

如果只是：

- 参数错误；
- 文件不存在；
- 某个 Tool 业务执行失败；

模型仍然可能换参数或换方法继续任务，所以 Runtime 可以把错误包装成失败 Tool Result，再交给下一次采样。

但如果是：

- 不可能出现的 payload 类型；
- Tool task 本身崩坏；
- 核心协议 invariant（不变量）被破坏；

再把它伪装成“普通工具失败”会掩盖系统错误。

所以成熟 Agent 不是“所有 Exception 都塞给模型继续修”。

更准确的原则是：

> **模型只能修复它拥有决策权的错误；Runtime 自身已经失去可信状态时应该 fail fast（快速失败）。**

---

## 16. Tool Result 怎样完成生命周期

正常 Handler 返回的结果还要经过最后几步，才算真正结束。

Runtime 会：

-记录 Tool lifecycle；
-执行 PostToolUse Hook（工具执行后钩子）；
-补充 ToolResultMetadata（工具结果元数据）；
-根据输出策略做必要截断；
-转换成 Responses API 可消费的 output item；
-写入 canonical history；
-触发下一次模型采样。

这也是为什么“工具执行成功”不等于“Agent 已经知道成功”。

只有结果真正写回历史，下一轮模型才知道现实世界已经变化。

如果一个 destructive action（有副作用的动作）已经成功，但结果在进入历史前丢失，模型甚至可能重复执行同一动作。

所以 Tool Lifecycle 的最后一个工程边界不是 function return，而是：

> **结果安全地成为下一次模型决策的 Observation（观察）。**

---

## 17. 用一个例子串完整 Tool Lifecycle

用户说：

> “运行测试并修复失败，但如果需要访问工作区外文件先问我。”

模型第一轮看到 `exec_command`，决定运行测试。

这份 Tool Call 来自产生它的 StepContext。Router 把 Responses 输出解析成内部 ToolCall。Registry 确认工具存在、payload 合法。

PreToolUse Hook 如果配置了审查逻辑，可以先观察命令。

ToolOrchestrator 计算：当前命令只需要 workspace 内权限，所以不需要额外 Approval，使用当前 Permission Profile 对应的 Sandbox。

命令执行后，测试输出很长。Runtime 对结果进行有界处理，把关键内容变成 Tool Result，关联原 call id，写进历史。

下一次模型看到失败信息，决定读取工作区外的一份配置。Runtime 判断这超出当前权限，于是发起 Approval。用户拒绝后，这次工具调用以明确失败结果回填。

模型因此知道：

> 不是文件不存在，而是权限没有获批。

它可以改用工作区内信息继续，而不是无限重试。

这才是一个完整的 Tool Call：从“模型提出动作”一直到“动作结果成为新 Context”。

---

## 18. 源码锚点

建议按这条顺序验证：

1. [`tools/src/tool_executor.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/tools/src/tool_executor.rs)：ToolExecutor 与 ToolExposure 的共享契约。
2. [`core/src/tools/spec_plan.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/spec_plan.rs)：一次 Step 怎样汇总并筛选工具。
3. [`core/src/tools/registry.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/registry.rs)：注册、Hook、dispatch。
4. [`core/src/tools/router.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/router.rs)：模型 Tool Call 如何变成内部调用。
5. [`core/src/mcp_tool_exposure.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/mcp_tool_exposure.rs)：MCP Tool 的暴露策略和 spec 大小预算。
6. [`core/src/tools/handlers/tool_search.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/handlers/tool_search.rs)：Deferred Tool 的 BM25 搜索。
7. [`core/src/tools/handlers/mcp.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/handlers/mcp.rs)：MCP Handler、ready 等待和结果处理。
8. [`ext/skills/src/extension.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/ext/skills/src/extension.rs)：Skill 怎样同时参与 Context 与 Tool。
9. [`ext/skills/src/render.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/ext/skills/src/render.rs)：Skill Catalog 的上下文预算。
10. [`core/src/tools/orchestrator.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/orchestrator.rs)：Approval、Permission、Sandbox、Network 和 escalation。
11. [`core/src/tools/parallel.rs`](https://github.com/openai/codex/blob/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/core/src/tools/parallel.rs)：并发、取消、Tool Result。
12. [`exec-server/`](https://github.com/openai/codex/tree/bb054a2b03f15787dcc2f9bd8ebfde713bc5b695/codex-rs/exec-server)：真正的执行环境和文件系统隔离。

下一篇：[Codex Engineering & Evaluation →](04-engineering-evaluation.md)
