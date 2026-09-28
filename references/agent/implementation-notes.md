# Agent｜固定实现对照与选读

[← 技术资料](README.md) · [课程入口](../../curriculum/09-agent/README.md)

本页承接课程中的产品实现选读，首次学习不需要靠它补齐核心前提。各段保留原稿指定快照的实现范围；本轮没有重新核验这些仓库的全部上游变化，不将其视作当前发行版的默认保证。

课程旧实现对照主要使用 Codex `fc948f8c473e5d11e780ffcf1fd7f812a2020932` 与学习用 Claude Code 私有镜像 `58231dcce408f805c645cfbc352d2876b517223b`。Products 和当前源码索引有自己的版本，不跨快照拼接结论。官方协议与框架行为以课程末尾的明确版本和官方链接为准。

<a id="chapter-01"></a>
## 01. Agent 系统的全貌：模型之外，谁把任务做完

[回到课程](../../curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md)

<details>
<summary>成熟产品源码告诉我们的什么</summary>

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

<a id="chapter-02"></a>
## 02. Workflow 与 Agent：哪些决定交给模型

[回到课程](../../curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md)

<details>
<summary>源码证据：为什么成熟产品一定有 Runtime Layer</summary>

固定 Claude Code 快照中，`QueryEngine` 持有 Conversation / Turn 生命周期，并管理 Tools、Agents、MCP Clients、Permission（权限）、Budget（预算）、Abort、Usage、Memory（记忆） Prompt 与 Compact 相关能力。

固定 Codex 快照中能看到：

- Session / Turn / Step；
- Tool Router（路由器） / Registry（注册表）；
- Sandbox（沙箱） Policy；
- Context Compaction（上下文压缩）；
- Rollout Trace。

这些实现共同说明一个稳定事实：

> **成熟 Agent 产品的复杂度主要来自 Runtime，而不是一次 LLM API 调用。**

注意：这些源码是实现证据，不代表所有产品必须同构。

</details>

<details><summary>7. 框架提供 checkpoint，是不是自动保证外部写入不重复？</summary>

不是。框架保存的流程状态与外部系统写入未必原子，仍需业务操作标识、核对和幂等。第13章会用两个检查点之间的故障解释。

</details>

<details><summary>9. 怎样避免自己的工作定义和产品术语冲突？</summary>

先说明项目采用什么定义，再给产品映射。不要拿教材的 Run/Turn 分类替代 Codex 或 SDK 官方对象；名称相近时应核对作用域和生命周期。

</details>

<a id="chapter-03"></a>
## 03. Agent Loop：观察怎样改变下一步

[回到课程](../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md)

<details>
<summary>具体落点：Codex 的排队/steer 与 Claude Code 的循环输入</summary>

Codex App Server 对正在运行的 Turn 提供 `turn/steer`（追加引导输入），并用预期 Turn 标识避免把新输入送给已结束或被替换的一轮；`turn/interrupt`用于中断。固定源码的 `session/turn.rs`检查待处理输入，决定是否还有后续工作。这个接口语义不同于“开始第二个同时修改同一状态的执行”。

用户提供的 Claude Code 快照中，`query.ts`在工具调用完成后读取按优先级筛选的排队输入，将符合当前Agent范围的内容作为附件加入后续消息，避免把普通用户消息插进未完成的工具请求/结果之间。Slash命令不按普通文本在轮中取出，需走自己的命令处理入口；`Tool.ts`另外提供工具中断行为。官方工作过程也说明用户可随时中断以引导方向。但具体界面是否排队、立即打断，取决于入口和运行模式，不能承诺所有客户端完全一样。

</details>

<details>
<summary>源码证据：Claude Code</summary>

固定快照中 `QueryEngine`：

- 一个 conversation 拥有 query lifecycle / session state；
- 每次 `submitMessage()` 开启新的 turn；
- messages、file cache、usage 等跨 turn 保留；
- 配置显式存在 `maxTurns`、`maxBudgetUsd`、`abortController`、tools、agents 与 permission callback。

这支持一个稳定课程抽象：

```text
Conversation Runtime
= Turn Lifecycle
+ Persistent State
+ Capability Set
+ Budget
+ Cancellation
```

</details>

<details>
<summary>源码证据：Codex</summary>

固定 Codex 快照中，Context Compaction（上下文压缩） 相关代码直接引用：

```text
Session
StepContext
TurnContext
WorldState
EventMsg
```

Tool Router（路由器） 中 `ToolCall` 也携带 `call_id`，再构造带 Session / StepContext / CancellationToken 的 Invocation（调用实例）。

这说明成熟 Runtime 会显式区分：

```text
长期 Session
→ 当前 Turn
→ 当前 Step / Invocation
→ Event / Tool Call
```

而不是把一切折叠成 Chat History（历史记录）。

产品对照不能把同名词硬套教学树：Codex公开交互以Thread/Turn/Item表达，一次Turn可含多次推理和工具交互；Item的开始、增量、完成可以形成多个事件。

</details>

<details><summary>4. 一次 Codex Turn 可否读取文件三次？</summary>

可以。Turn 包含用户请求后的一段 Agent 工作，模型可多次请求工具。每个工具项目及其事件有各自身份；不能把三次调用解释成必然三个 Codex Turn。

</details>

<a id="chapter-04"></a>
## 04. 工具契约：模型提出什么，程序检查什么

[回到课程](../../curriculum/09-agent/docs/04-ToolContractAndValidation.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/04-ToolContractAndValidation.md)

<details>
<summary>源码证据：Claude Code</summary>

固定快照的 `Tool.ts` 显示 Tool Contract 不只包含 Schema 和 `call()`，还包含：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior()`；
- Permission Context；
- Progress Callback；
- Result / Context Modifier；
- Tool Result Budget / Dynamic Discovery 相关状态。

这非常适合说明：

> Production Tool 是 Runtime Contract，不是 Function Signature。

</details>

<details>
<summary>源码证据：Codex</summary>

固定 Codex 快照中的 `ToolExecutor` 把：

```text
tool_name
spec
exposure
search_info
supports_parallel_tool_calls
handle(invocation)
```

放在同一个执行契约中。

`ToolOutput` 又把：

- model-facing response；
- logging projection；
- host-only metadata；
- external context 标记；

分开表达。

这说明 Tool Input / Output 都应被 Runtime 当成正式协议对象。

</details>

<a id="chapter-05"></a>
## 05. 工具注册与发现：程序有的，不一定都给模型看

[回到课程](../../curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md)

<details>
<summary>源码证据：Codex</summary>

固定快照中的 `ToolRouter` 明确区分：

- full registry；
- `model_visible_specs`；
- deferred tool search；
- namespace；
- code-mode tool identity。

`ToolExposure` 还能表达：

```text
Direct
Deferred
DeferredModelOnly
DirectModelOnly
CodeModeOnly
Hidden
```

这直接证明：

> 注册能力与本轮向模型暴露能力是两件事。

### Codex 固定源码：注册表与 model_visible_specs 的真实连接

`codex-rs/core/src/tools/router.rs`中的`ToolRouter`同时保存`registry: ToolRegistry`和`model_visible_specs`。`session/turn.rs::build_prompt`把`tool_router.model_visible_specs()`放进模型请求的`tools`字段；真实工具执行则由Registry和处理器承担。

可以直接跟一项工具：`tools/handlers/plan.rs`的`PlanHandler`定义名字`update_plan`，`spec()`返回说明，`handle()`解析参数并调用内部处理流程。模型看见的是规格，程序保留处理器；计划更新后还会发出`PlanUpdate`事件。这比“工具注册到LLM里”更精确。

该快照还支持不同暴露/延迟发现路径。是否全部直接暴露取决于配置与工具类型，不能把某条路径说成所有Codex调用都使用的唯一机制。

</details>

<details>
<summary>源码证据：Claude Code</summary>

固定快照的 `Tool.ts` 中存在 `searchHint`，`ToolUseContext` 还包含 dynamic skill discovery / discovered skill names 等状态。


### Claude Code 用户快照：getTools → toolToAPISchema → tool result

`tools.ts::getAllBaseTools()`列出内置工具对象；`getTools()`依据模式、开关和deny规则选择工具。外部MCP工具有自己的连接与合并流程，不在这个内置函数里凭空变成代码。

`utils/api.ts::toolToAPISchema`取工具的名字、`prompt()`生成的描述、输入JSON Schema或由Zod转换的模式，再按能力增加严格模式、延迟加载和缓存等API字段。它使用稳定基础Schema缓存及每请求的覆盖字段，避免无必要地改变请求字节。

`query.ts`把工具对象交给模型调用封装，也交给工具执行器。模型返回`tool_use`后运行时找到实际对象；`TodoWriteTool.ts`说明内部还可更新应用状态，并用单独的结果映射方法生成`tool_result`。这条路径清楚展示“宿主对象”和“模型可见表示”不是同一份数据。

</details>

<a id="chapter-06"></a>
## 06. 工具结果与失败：谁来修，怎样继续

[回到课程](../../curriculum/09-agent/docs/06-ToolExecutionAndFailure.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/06-ToolExecutionAndFailure.md)

<details>
<summary>源码证据：Codex</summary>

固定快照中：

- `ToolRouter` 把 `ResponseItem` 规范化成带 `tool_name / call_id / payload` 的 `ToolCall`；
- `ToolRegistry` 负责 dispatch；
- `CoreToolRuntime` / `ToolExecutor` 提供统一执行接口；
- `FunctionCallError` 至少区分 `RespondToModel` 与 `Fatal`；
- Registry（注册表） 执行链有 pre/post tool hooks、telemetry、tool lifecycle notification；
- `ToolOutput` 区分 log representation、model-facing response 与 host metadata。

这些实现非常清楚地表明：

> Tool Execution 是一个受控调用生命周期，而不是函数调用语法糖；它不天然提供跨系统原子事务。

</details>

<a id="chapter-07"></a>
## 07. 工具并发与取消：快一点，不等于可以乱序

[回到课程](../../curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md)

<details>
<summary>源码证据：Claude Code</summary>

固定快照的 `Tool.ts` 有：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior(): cancel | block`；
- progress callback。

`utils/abortController.ts` 还实现 Parent → Child AbortController 传播，并处理 listener 清理。

这些实现直接说明：

> Concurrency / Cancellation 属于 Tool Runtime Contract，而不是 UI 细节。

</details>

<details>
<summary>源码证据：Codex</summary>

固定快照的 `ToolRouter` / Invocation（调用实例） 会携带 `CancellationToken`，Registry（注册表） 还能查询 Tool 是否支持 parallel calls。

这支持同样的稳定抽象：

```text
Tool Scheduler
需要知道 parallel capability + cancellation token
```

</details>

<a id="chapter-08"></a>
## 08. 计划与停止：让每一步朝目标推进

[回到课程](../../curriculum/09-agent/docs/08-PlanningGoalAndControl.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/08-PlanningGoalAndControl.md)

<details><summary>9. Codex update_plan返回确认，模型还能知道清单内容吗？</summary>

它刚提交的工具调用包含计划参数，历史中有这段信息；确认结果不必重复整个清单。不能从短确认推断计划丢了，也不能推断它被固定在System Prompt。

</details>

<details>
<summary>补充：Stop Condition 不是只有 `max_steps`</summary>

### Stop Condition 不是只有 `max_steps`

一个成熟 Runtime 至少有三类停止条件。

### 5.1 成功停止

```text
Acceptance Criteria satisfied
→ produce final answer / artifact
```

### 5.2 无法继续

例如：

```text
缺权限
缺关键输入
外部服务持续失败
用户必须确认高风险动作
```

此时应该：

```text
Pause / Ask / Escalate
```

而不是继续随机尝试。

### 5.3 强制停止

```text
max_turns
max_tool_calls
max_cost
max_tokens
wall_clock_timeout
retry_budget
```

Claude Code 固定源码索引里，`QueryEngine` 配置明确存在 `maxTurns`、`maxBudgetUsd`、`fallbackModel`、`abortController` 等边界。课程抽象因此是：

> **Budget 属于 Runtime 控制面，不只是 Provider（模型服务方） billing。**

---

</details>

<a id="chapter-09"></a>
## 09. 上下文编排：模型这一刻到底收到什么

[回到课程](../../curriculum/09-agent/docs/09-ContextAssemblyAndCache.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/09-ContextAssemblyAndCache.md)

<details>
<summary>Claude Code 源码提供了什么实现证据</summary>

固定源码索引里，`QueryEngine.ts` 会加载：

- memory prompt；
- session storage；
- system prompt parts；
- file history；
- plugin / skill 相关状态；
- compact / snip 相关能力。

`ToolUseContext` 还显式维护：

```text
loadedNestedMemoryPaths
tool-result budget
content replacement state
dynamic skill discovery
permission decision
```

这支持一个成熟 Runtime 的稳定抽象：

```text
Context
≠ transcript concatenation

Context
= selected runtime projection
```

这里我们只引用索引已核验的源码事实，不把 Claude Code 的具体排序当成所有 Agent 的通用标准。

### 固定源码路径：初始上下文、消息追加、工具说明、计划更新与压缩后重建

依据固定Codex的`session/mod.rs`和`session/turn.rs`，可以沿以下顺序理解，**不是声称所有开关都输出同一串文字**：

1. `build_initial_context_with_world_state`收集开发者指令、扩展提供的线程/当前轮信息和环境状态。按片段角色聚合，普通路径先形成开发者消息，再放需要单独保留的开发者片段和模式信息，然后形成上下文用户消息。Guardian等分支另有独立指令位置。
2. 初次进入或压缩后的新上下文窗口需要完整注入；日常执行通过上下文更新与参考状态生成必要变化，不应每步无条件重建全部前缀。
3. 用户输入、模型输出、函数调用与函数结果进入执行历史。`build_prompt`把历史投影作为`input`，工具来自`tool_router.model_visible_specs()`，`base_instructions`另行传入，输出约束也独立。最终API序列化还在供应商适配层。
4. `update_plan`调用参数本身写明计划，处理器发出`PlanUpdate`事件，回填确认；新计划更新继续走调用/结果链，不要求每次移到最前面。
5. 压缩会换一个历史视图。前轮/手动路径与当前轮中压缩的初始信息重注入不同，下一章给出完整过程。

你可以据此描述一条实在的链：**初始上下文与环境信息→追加用户/模型/工具项→选当前可见工具说明→独立基础指令→模型请求**。这比“系统、计划、记忆总是固定按某八个位置摆放”更接近该快照。



### 用户提供的固定源码路径：query.ts → utils/api.ts → 模型适配

`query.ts`把`systemPrompt`、`userContext`、`systemContext`与`messages`分开接收。循环内先取最近压缩边界之后的消息，再应用工具结果预算、可选历史裁剪、微压缩、可选局部上下文折叠以及自动压缩。特性开关会改变经过哪些分支。

模型调用前可以直接看到：

```text
systemPrompt = appendSystemContext(systemPrompt, systemContext)
messages = prependUserContext(messagesForQuery, userContext)
tools = toolUseContext.options.tools
signal = toolUseContext.abortController.signal
```

`appendSystemContext`把环境键值块接到系统指令块后；`prependUserContext`在非空时创建一条含`system-reminder`的合成用户消息放到消息列表前面，供CLAUDE.md等上下文使用。模型工具随后经过`toolToAPISchema`投影为API支持字段，宿主的完整Tool对象不会原样进入模型。

因此示意请求是**独立system块、独立tools、合成user-context消息+既有消息视图**，不是所有信息都每次按新优先级重排。`utils/api.ts`还区分系统静态/动态边界；`query.ts`在给界面补充工具字段时刻意复制消息，保留送回API的原始参数字节，以减少无意缓存变化。

TodoWrite更新程序清单并回填确认，清单内容仍能由历史工具调用得知；计划模式文件不是相同对象。`compact.ts`压缩后会按需重新附加当前计划。不能把这些实现简化成“每轮把最新Plan插入固定前缀”。

</details>

<details><summary>9. 两产品折叠案例为何不写一份绝对固定的完整系统提示？</summary>

固定源码会按模型、模式、插件与特性分支形成不同内容。本章给出实际函数与组装顺序，不能把某一配置的文本误称所有用户都收到的统一提示。

</details>

<a id="chapter-10"></a>
## 10. 上下文压缩：缩短输入以后，怎样继续做对

[回到课程](../../curriculum/09-agent/docs/10-CompactionAndContinuation.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/10-CompactionAndContinuation.md)

<details>
<summary>Codex `compact.rs` 给出的实现证据</summary>

### 固定源码：触发判定 → 摘要请求 → 替代历史 → 后续调用

**触发。** `session/turn.rs`在正常推理前检查是否需要自动压缩，推理后若仍需继续工具/输入循环，也会结合使用量检查。`session/context_window.rs`区分全窗口计数与扣除前缀的主体预算，还维护完整上下文上限；模型切换等路径有额外判定。因此不能写“Codex永远到90%就压缩”。手动请求另有独立入口。

**分支。** 该固定快照在`run_auto_compact`里按功能配置选择Token Budget（预算）管理、供应商支持的远端压缩或本地`compact.rs`。以下完整描述只针对本地摘要路径；远端输出与实现不能从本地提示推断。

**输入和提示。** `compact.rs`复制当前历史视图，加入压缩指令构造模型输入，基础指令单独提供，压缩请求不照搬正常工具执行循环。默认提示来自`codex-rs/prompts/templates/compact/prompt.md`，也允许配置覆盖。原文以“CONTEXT CHECKPOINT COMPACTION”标识这项交接任务。用中文概括，它要求为接替执行的模型写交接摘要，重点是：已做工作与决定、重要约束和偏好、剩余步骤、关键资料与引用，并要求简洁、有组织。它不是要求固定JSON Schema；局部小标题是结构化写作，不等于机器已校验字段。

**结果。** 本地路径提取助手返回的摘要字符串，添加summary prefix，并通过`build_compacted_history`组合选取的真实用户消息与摘要。源码有保留用户消息的预算上限；不能据此声称所有历史逐条不丢，也不能说输出就是原字段状态的无损备份。

**安装。** `replace_compacted_history`更新执行中的历史并记录压缩项，重新计算使用量。前轮/手动压缩使用`DoNotInject`，清掉初始上下文参考，使后续正常轮重新注入；轮中压缩使用`BeforeLastUserMessage`，把初始上下文放到最后真实用户消息之前，让摘要位于规定位置。两种路径不能画成同一个无条件顺序。

**失败。** 摘要请求本身过长时有移除旧项后再试的处理；短暂故障有有限退避。技术上能继续不代表摘要语义完整，仍需要长任务回归。此处没有承诺整个外部世界与替代历史构成原子事务。

</details>

<details>
<summary>Claude Code 侧提供了什么证据</summary>

### 用户固定快照：消息预算与多种压缩机制如何协作

`query.ts`可直接追踪到如下处理次序：取最近压缩边界后的消息→大工具结果预算/外部化→可选历史裁剪（snip）→微压缩（microcompact）→可选上下文局部折叠→自动压缩检查→发送模型请求。部分路径由编译或运行开关控制，**源码包含不等于所有公开构建同时启用**。

| 机制 | 改变什么 | 与摘要的区别 |
|---|---|---|
| 工具结果预算 | 将过大结果替成有限视图或产物引用 | 不一定调用模型 |
| 微压缩 | 清理符合条件的旧工具结果；某些构建支持缓存编辑 | 不等于总结整段对话 |
| snip/局部折叠 | 按功能开关裁剪或投影历史区段 | 与全量摘要可能相互协调 |
| 自动/手动完整压缩 | 生成交接摘要并重建后续消息 | 是本文主要摘要路径 |
| reactive压缩 | 某些开关下收到真实超长错误后补救 | 不能假设始终是默认策略 |

`autoCompact.ts`的普通自动路径先计算有效窗口：模型上下文窗口减去`min(模型最大输出, 20,000)`的摘要输出预留，再减去`13,000`余量作为阈值。环境覆盖和特性开关可改变判定；snip释放量会影响估算。**这些数字只属于该快照，不是教学建议。** 压缩/会话记忆子请求有递归保护；连续失败达到限制会停止无效尝试。

达到条件后，先尝试实验性的session-memory压缩路径，未采用时进入`compactConversation`。这条session-memory路径与跨会话auto memory文件不是同一概念。

`compactConversation`执行前置Hook（生命周期钩子），生成`getCompactPrompt`的摘要请求，调用摘要模型。它会对图片/文档等材料做适用处理，遇到摘要请求过长时可能按API轮组裁剪头部重试。摘要从助手文本提取，并检查空结果和API错误；不是自动得到一个经过Schema验证的恢复对象。

成功后按需恢复近期文件、异步任务、计划文件/规划模式、已调用技能、已发现工具和MCP说明等附件。`buildPostCompactMessages`明确顺序为：**压缩边界标记→摘要消息→需保留消息→附件→Hook结果**。下一次调用仍按第09章路径提供systemPrompt/userContext/tools，摘要不承担替代所有系统规则的责任。

</details>

<details><summary>6. 本地Codex摘要结构清楚，能当检查点直接恢复吗？</summary>

不够。它主要支撑后续推理，活动操作、回执和环境状态有独立语义；自然语言摘要不保证外部写入一次且仅一次。

</details>

<a id="chapter-11"></a>
## 11. 记忆：把有用经验带到以后，也能纠错和忘记

[回到课程](../../curriculum/09-agent/docs/11-MemoryLifecycle.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/11-MemoryLifecycle.md)

<details>
<summary>Claude Code 固定源码侧的证据</summary>

### Claude Code：文件型auto memory与CLAUDE.md有何不同

官方Memory文档区分：`CLAUDE.md`是人维护的项目指令；auto memory是Claude为未来会话保存的有用记录，不是每次对话全文自动备份。`MEMORY.md`是简短索引，启动时加载有限部分，详细主题文件按需读取；用户可查看、修改或删除。

用户固定快照`memdir/memdir.ts`提供保存指导：先查有无可更新记录，把具体记忆写入主题文件，再在MEMORY.md增加指针；发现错误或过期时更新/删除。这里“何时提取”部分通过模型行为指令表达，不是读到一个统一强制后台定时提取器。代码还区分system里的记忆行为指导与user context中的内容注入。

一条具体路径是：用户确认长期报告偏好→模型按指导写主题文件及索引→下次会话加载索引→需要报告时读详细文件→用户纠正时更新文件/索引。不是“所有Token经过向量库自动成为长期记忆”。功能开关、项目路径和官方版本会影响实际可用性。



### Codex：固定memories模块的两阶段离线提炼

固定源码`codex-rs/memories/README.md`描述另一种实现。非临时、启用记忆且状态数据库准备好的根会话启动时，可以异步启动流水线；它选择符合条件的**已空闲的旧会话记录**，不是把正在运行的每个步骤立刻整合。

第一阶段按资格、时间和租约领取旧会话，在限并发条件下提取原始记忆与会话摘要，执行敏感内容处理并保存阶段结果；无有用内容可不产出。第二阶段用全局任务租约选择提取结果，更新原始记忆材料、摘要文件并清理陈旧产物，再由受约束的整合子Agent维护MEMORY.md、memory_summary.md及相关知识文件。无输入变化可跳过模型工作；失败与重试受控。

这解释了“什么时候长期化”：在该流水线产物被写入后续读取路径时，而不是当前上下文刚做Compaction（上下文压缩）时。启动条件、资格筛选与两阶段职责是固定快照事实；不能把它套到Claude的文件写入路径，也不能声称仅有这份README就证明所有记忆语义永远正确。

</details>

<details><summary>9. Codex两阶段提炼为何不等于每步同步写记忆？</summary>

资格选择针对旧空闲会话，提取和整合异步受租约/并发控制，启动触发不等于所有当前事件立即成为记忆。

</details>

<a id="chapter-12"></a>
## 12. 状态与持久化：程序怎样知道工作做到哪里

[回到课程](../../curriculum/09-agent/docs/12-StateHistoryAndPersistence.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/12-StateHistoryAndPersistence.md)

<details>
<summary>两个产品怎样体现“持久记录不等于全部运行内存”</summary>

Codex固定`Session`保存历史与上下文参考，`persist_rollout_items`把选定RolloutItem交给持久线程记录；模型请求则从历史投影构建。其App Server通过Thread提供跨交互会话语义。这个事实并不承诺自定义外部工具的副作用都有业务事务记录，接入方仍要设计它。

Claude Code用户快照的QueryEngine负责会话生命周期，`query.ts`有消息、工具上下文、重试/压缩跟踪等活动状态；`utils/sessionStorage.ts`承担记录路径。`compact.ts`通过边界和保留消息关系支持压缩后加载，而非序列化所有协程、网络连接和内存缓存。官方支持会话恢复，也不意味着恢复任意外部业务交易。

</details>

<a id="chapter-13"></a>
## 13. 检查点与恢复：保存之后、崩溃之前发生了什么

[回到课程](../../curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md)

<details>
<summary>补充：Long-running Task 的状态机</summary>

### Long-running Task 的状态机

可以从：

```text
pending
running
paused
waiting_approval
waiting_external
completed
failed
cancelled
```

开始。

Claude Code Source Index 中 `Task.ts` 已确认有：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

这支持一个稳定抽象：

> **Task 应该是有身份、状态机、输出位置和终止语义的一等 Runtime 对象，而不是一个普通 async function。**

---

</details>

<details>
<summary>补充：Pause / Resume 与 HITL</summary>

### Pause / Resume 与 HITL

Approval（批准） 场景：

```text
Agent 想执行 delete_production_table
→ Runtime emits interruption
→ Persist RunState
→ user approves / rejects
→ Resume
```

OpenAI Agents SDK 的 HITL 官方文档明确支持：

- Tool Call interruption；
- 序列化 RunState；
- 审批后 resume；
- approval 在 handoff / nested agent 中传播。

这说明：

> **HITL 本身就是 Checkpoint / Resume 的一种具体 Runtime 场景。**

---

</details>

<details>
<summary>补充：Resume 和 Fork 不一样</summary>

### Resume 和 Fork 不一样

### Resume

```text
继续同一个 Run / lineage
```

### Fork

```text
从某个历史状态派生一个新 Run
```

Fork 需要回答：

```text
继承哪些 instructions？
继承哪些 memory？
继承 workspace snapshot 吗？
继承 side-effect ledger 吗？
新的 run_id 是什么？
```

Codex Source Index 中 Thread Instructions 的固定提交明确讨论：

- warm resume 保留 provider；
- cold resume / offline fork 重新提供；
- live fork / subagent 继承 applied snapshot，但不继承 source provider；
- refresh 要 cancellation-safe。

课程抽象：

> **Source Provider（模型服务方） 与 Applied Snapshot 要分开建模。**

---

</details>

<a id="chapter-14"></a>
## 14. 权限、批准与沙箱：一次动作要过几道不同的门

[回到课程](../../curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md)

本章主要建立通用职责与边界；具体实现可沿[源码及官方资料索引](README.md)选择，不额外复制正文或要求掌握产品私有类名。

<a id="chapter-15"></a>
## 15. 提示注入与信息保护：资料为什么不能变成命令

[回到课程](../../curriculum/09-agent/docs/15-InjectionAndContainment.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/15-InjectionAndContainment.md)

<details>
<summary>实现对照：产品安全文档怎样补充源码，而不是代替威胁分析</summary>

Claude Code官方Sandboxing说明文件和网络限制；Codex沙箱策略与执行管理代码说明可实施的边界。它们支持“限制行动范围”的设计，不证明输入文本已经无害。工具权限、环境限制和凭证最小化需要一起配置。

OpenAI Agents SDK的Guardrails文档说明输入、输出及工具相关检查的生命周期；某些检查的运行时机受Runner和配置影响。采用前要确认是否覆盖你真正关心的工具路径，不能把一个输出检查器当作执行前事务门。产品默认配置与本文教学示例分开，实际部署须按当前官方接口验证。

</details>

<details>
<summary>Tier C 官方证据</summary>

#### Anthropic — Beyond permission prompts

课程使用：

```text
Permission prompt
≠ Sandbox
```

Filesystem / Network isolation 可以降低不必要审批，同时控制 blast radius。

#### Anthropic — How we contain Claude across products

课程使用：

> 不只降低错误概率，还要限制错误影响范围。

#### OpenAI Agents SDK — Guardrails

课程使用：Input / Output / Tool Guardrail 是不同生命周期边界。

</details>

<a id="chapter-16"></a>
## 16. MCP：从 Host / Client / Server 到完整协议往返

[回到课程](../../curriculum/09-agent/docs/16-MCPArchitectureAndLifecycle.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/16-MCPArchitectureAndLifecycle.md)

<details><summary>6. 为什么两份旧源码不能证明当前所有MCP能力？</summary>

源码固定在具体提交，功能和协议版本可能不同。本章用它们说明Host接入责任，具体当前协议字段和方法以官方版本文档核验。

</details>

<a id="chapter-17"></a>
## 17. Skills、Hooks 与 Plugins：知识怎样加载，规则怎样触发

[回到课程](../../curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md)

<details>
<summary>Claude Code 源码侧的 Progressive Loading 证据</summary>

固定 Source Index 已确认 `ToolUseContext` 中存在：

```text
dynamicSkillDirTriggers
discoveredSkillNames
```

Tool 还存在：

```text
searchHint
```

用于 deferred tool discovery。

这支持课程抽象：

```text
Capability Catalog
→ Discovery
→ Selection
→ Progressive Loading
→ Invocation
```

而不是：

```text
All Tool Schemas
→ Every Context
```

</details>

<details><summary>9. 为什么两份旧源码不能证明当前所有MCP能力？</summary>

源码固定在具体提交，功能和协议版本可能不同。本章用它们说明Host接入责任，具体当前协议字段和方法以官方版本文档核验。

</details>

<details>
<summary>补充：Codex Hooks 的实现证据</summary>

### Codex Hooks 的实现证据

固定 Codex Source Index 已确认：

- `codex-rs/hooks/src/engine/mod.rs`；
- `codex-rs/config/src/hook_config.rs`；
- Hook handler 可以包括 command、MCP tool、prompt、agent；
- compaction 存在 pre/post hook。

这支持：

```text
Core Runtime
→ Lifecycle Event
→ Hook Policy
→ Extension Handler
```

Hook 是横切扩展点，不应该反过来定义整个 Runtime 生命周期。

---

</details>

<a id="chapter-18"></a>
## 18. 路由与模型适配：换一条路径，不能丢掉任务保证

[回到课程](../../curriculum/09-agent/docs/18-RoutingAndProviderResilience.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/18-RoutingAndProviderResilience.md)

<details>
<summary>实际产品中的选项与边界</summary>

Claude Code用户快照QueryEngine配置包含fallbackModel，`query.ts`在流式fallback时处理旧尝试留下的助手项与工具结果，避免把孤立结果混进新尝试。这个实现提醒我们：模型切换不仅改名字，还涉及历史关联与已经执行的工作；不能从配置字段推断所有业务动作都能安全重跑。

Codex固定`build_prompt`取当前模型/步骤设置与工具Router（路由器），`context_window.rs`按模型预算判断，模型变化时上下文处理可能不同。App Server与模型提供者适配层具有各自接口，不是“所有模型返回文本就能直接互换”。具体默认路由规则以产品配置和源码分支为准。

</details>

<details>
<summary>补充：Claude Code 的实现信号</summary>

### Claude Code 的实现信号

固定 Source Index 确认 `QueryEngine` 配置存在：

```text
fallbackModel
```

这支持一个实现事实：

> 成熟 Runtime 会把 Model / Provider Failure 后的 fallback 纳入 Harness 控制面。

但具体 fallback 条件不能仅凭这一字段推断，本章只使用这个已核验边界。

---

</details>

<a id="chapter-19"></a>
## 19. 多 Agent 协作：交出去的是任务，不是全部控制权

[回到课程](../../curriculum/09-agent/docs/19-MultiAgentAndA2A.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/19-MultiAgentAndA2A.md)

<details>
<summary>Codex、Claude与框架中的内部子Agent，不应硬套A2A</summary>

Claude用户固定`Task.ts`区分本地命令、本地/远程Agent等任务类型，维护状态和输出位置；这些是产品内部对象，不足以证明它们统一走A2A。Codex固定源码里的子Agent路径和上下文继承同样应按自己的运行时契约理解。

OpenAI Agents SDK官方用handoffs和agents-as-tools区分控制转移与返回；LangGraph可以把子图作为复杂状态流程的一部分。以上都可以表达多Agent，但并不要求每个内部调用通过A2A网络协议。只有读到具体适配器和协议请求，才应声称某个产品采用了某版A2A。

</details>

<details><summary>10. 怎样证明某产品的多Agent用了A2A？</summary>

需要读取实际协议适配与请求实现，或对应官方支持说明；仅看到remote_agent、handoff或task字段不能推出协议。

</details>

<details>
<summary>补充：Claude Code `Task.ts` 提供的实现信号</summary>

### Claude Code `Task.ts` 提供的实现信号

固定源码索引确认 Task 类型明确区分：

```text
local_bash
local_agent
remote_agent
in_process_teammate
local_workflow
monitor_mcp
dream
```

并且 Task state 包含：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

这直接支持课程抽象：

> Subagent / Background Task 应是有身份、状态机、输出位置、取消语义的一等 Runtime（运行时执行系统） 对象。

---

</details>

<a id="chapter-20"></a>
## 20. 执行追踪：先定位卡在哪，再取需要的证据

[回到课程](../../curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md)

<details>
<summary>Codex Rollout Trace 的源码证据</summary>

固定 Codex Source Index 中 `codex-rs/rollout-trace/README.md` 明确区分：

```text
exact raw payload evidence
ConversationItem
ToolCall
CodeCell / TerminalOperation
InteractionEdge
```

稳定课程抽象：

> Trace应保留足够的关联结构来定位信息流；需要深查时按授权取得输入证据，不默认保存全部原文。

这直接服务：

```text
Debug
Replay
Evaluation
Incident Analysis
```

源码存在raw payload证据视图，不证明所有构建默认完整采集。学习其关联能力，不把产品可选调试设施当所有应用必须永久全存的要求。

</details>

<details>
<summary>补充：OpenAI Agents SDK Tracing 给出的证据</summary>

### OpenAI Agents SDK Tracing 给出的证据

官方 Tracing 文档覆盖：

```text
task
agent
turn
generation
tool
guardrail
handoff
```

这说明成熟 Agent Framework 会把 Trace 设计成 Runtime（运行时执行系统） 一等能力，而不是应用自行 print。

课程不要求使用某个 SDK，但要掌握这个层次模型。

SDK的敏感数据收集、导出和保留配置需要实际检查；Tracing不是业务会话存储或事务账本。

---

</details>

<details>
<summary>补充：Context Management 自己也需要 Observability</summary>

### Context Management 自己也需要 Observability

Codex `compact.rs` Source Index 已确认有 Compaction（上下文压缩） Analytics：

```text
trigger
reason
phase
status
context tokens
summary tokens
latency
```

这支持一个重要原则：

> **Context Management 不是黑盒 preprocessing，它本身也要被 Trace / Metric。**

例如可以看：

```text
compaction_rate
post_compaction_failure_rate
context_tokens_before/after
```

---

</details>

<a id="chapter-21"></a>
## 21. Agent 评测：怎样证明修改真的更好

[回到课程](../../curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md)

<details>
<summary>官方框架与Benchmark提供什么，不提供什么</summary>

OpenAI Agents SDK提供Tracing等执行证据入口，评测仍需自己定义任务验收。SWE-bench原论文及基准用真实仓库问题检验代码修复，强调运行环境与测试结果；分数受数据、环境、工具与评测流程影响，不能直接外推到你的企业报告Agent。

Codex/Claude的工具、工作区和测试调用能形成验证链，但“使用了同一个产品”不等于本项目已经通过相同评测。引用固定源码是解释实现，声称质量提升必须有自己的数据与实验。

</details>

<a id="chapter-22"></a>
## 22. Coding Agent：从理解仓库到交付可验证修改

[回到课程](../../curriculum/09-agent/docs/22-CodingAgentDelivery.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/22-CodingAgentDelivery.md)

<details>
<summary>产品落地点：Codex与Claude把读取、执行和验证接成循环</summary>

Codex固定ToolRouter将模型候选接到文件/命令等处理器；Claude用户快照的基本工具目录提供读取、编辑、写入、Shell以及可选搜索工具。工具结果回填后，模型可以观察编译或测试失败并调整下一步。这构成“读→改→测→观察→继续”的具体执行循环。

两者允许的执行环境由实际策略配置决定。不能仅因某产品支持Shell就说本轮已运行测试，也不能从最终自然语言声明推断命令输出。调用/产物记录可作证据，但验证覆盖仍需任务本身定义。

</details>

<a id="chapter-23"></a>
## 23. 生产运行：从任务承诺推导部署，而不是先画微服务

[回到课程](../../curriculum/09-agent/docs/23-ProductionRuntime.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/23-ProductionRuntime.md)

<details>
<summary>两个成熟产品怎样作为对照，而不是指定架构模板</summary>

Codex固定Session、工具Router（路由器）、执行环境与rollout记录提供可组合的职责实例；Claude Code QueryEngine、工具目录、会话存储和取消路径也是运行支撑实例。它们告诉我们模型之外需要处理哪些实际工作，不表示你的Web服务必须照抄内部目录或默认拓扑。

部署在CLI、开发机、云沙箱或企业后端时，连接寿命、资源访问和故障承诺不同。读产品源码应先还原其环境，再提取能迁移的机制。框架具体提供哪些API与持久语义，下一章用官方接口对照。

</details>

<details>
<summary>补充：Brain / Hands / Durable Session 分离</summary>

### Brain / Hands / Durable Session 分离

Anthropic `Scaling Managed Agents: Decoupling the brain from the hands` 提供了很有价值的成熟参考：

```text
brain / harness
hands / execution environment
durable session log
```

课程抽象：

```text
Harness Worker
= 决策与 Runtime 控制

Execution Environment
= 真正访问文件 / 进程 / 网络 / Tool 的“手”

Durable Session
= Context Window 之外可恢复的执行事实
```

分离后的好处：

- Harness 可以水平扩容；
- Sandbox 可以独立重建；
- Session 不绑某一个进程；
- Execution Risk 和 Model Runtime 分离；
- 长任务可以迁移 Worker。

---

</details>

<a id="chapter-24"></a>
## 24. 框架选型：先问要保证什么，再看谁能实现

[回到课程](../../curriculum/09-agent/docs/24-FrameworkSelection.md) · [本次精修前的固定稿](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/a6b51b9f00bf3fe7910cfe4ca248e80545f566e3/curriculum/09-agent/docs/24-FrameworkSelection.md)

<details>
<summary>官方生命周期对照：有历史的两次调用不等于事务工作流</summary>

根据官方Running agents、Sessions与Human-in-the-loop文档：应用建立Agent与Runner，选用Session时运行前取相关历史、运行后保存新交互；一次执行内部可有多轮模型与工具。需要批准的工具让运行产生中断，应用可获取运行状态，提交批准或拒绝后继续。

Sessions的主要语义是会话项管理，RunState用于暂停执行；即使同一应用使用两者，也要明确保存什么、谁授权恢复以及外部工具执行是否已经发生。不可把“用了SQLiteSession”直接回答成“任意节点都能恰好一次恢复”。具体API以所安装版本为准，本章不把示意流程当完整可运行代码。

</details>

<details>
<summary>官方生命周期对照：State、Checkpointer、Store各在什么时候用</summary>

先声明状态与合并规则，再加入节点和边，编译图时提供需要的Checkpointer。调用图时给输入和thread_id，节点按调度轮次运行，检查点记录状态。某节点中断后，应用保存并展示待办，用户回应再用原线程上下文恢复；不是新建一个完全无关任务。

跨会话用户偏好可以放Store，在节点需要时读取。它不自动成为当前图状态，也不因检查点而自动校验正确性。并行节点失败时框架可保留已完成节点写入，但恢复单位仍由框架定义，不能恢复任意Python指令位置。

</details>

<details><summary>9. 什么情况下不能宣布框架选型完成？</summary>

关键权限、恢复或部署条件尚未验证，或测试只覆盖正常Demo。应列出已证实和待验证要求，而不是把疑问藏在“支持生产”里。

</details>

<details>
<summary>补充：OpenAI Agents SDK 怎样映射</summary>

### OpenAI Agents SDK 怎样映射

Agent对象主要定义指令、模型、工具、handoffs和输出约束；Runner驱动运行：请求当前Agent模型，执行工具或交接，继续循环，直到满足最终输出或停止/错误条件。`function_tool`把Python函数包装为可调用工具并生成相应Schema，但不替业务定义权限和幂等。

| 官方抽象 | 负责什么 | 不能误认为 |
|---|---|---|
| Agent | 一组执行配置与能力 | 一个已运行且永久持久化的任务 |
| Runner | 推进模型、工具、交接的循环 | 自动恢复所有外部副作用 |
| Handoff（控制权交接） | 将当前控制转给另一Agent | 与agents-as-tools完全同义 |
| Session | 调用前取历史、结束后更新会话历史等 | 任意业务工作流的事务检查点 |
| RunState/人工参与机制 | 保存中断运行所需状态并继续 | 与所有存储、版本天然兼容 |
| Tracing | 记录执行过程的诊断 | 默认权威业务账本 |

<details>
<summary>官方生命周期对照：有历史的两次调用不等于事务工作流</summary>

根据官方Running agents、Sessions与Human-in-the-loop文档：应用建立Agent与Runner，选用Session时运行前取相关历史、运行后保存新交互；一次执行内部可有多轮模型与工具。需要批准的工具让运行产生中断，应用可获取运行状态，提交批准或拒绝后继续。

Sessions的主要语义是会话项管理，RunState用于暂停执行；即使同一应用使用两者，也要明确保存什么、谁授权恢复以及外部工具执行是否已经发生。不可把“用了SQLiteSession”直接回答成“任意节点都能恰好一次恢复”。具体API以所安装版本为准，本章不把示意流程当完整可运行代码。

</details>

---

</details>

<details>
<summary>补充：LangGraph 适合解决什么类型问题</summary>

### LangGraph 适合解决什么类型问题

LangGraph用StateGraph描述状态如何在Node（节点）和Edge（边）之间流动。Node读取状态并返回更新；Reducer（合并规则）决定多个更新如何合并。图可以包含模型、普通函数、工具或子图，不是每个节点都必须是Agent。

Checkpointer按执行调度边界保存快照，通常通过thread_id关联；Store用于跨线程的持久数据等用途，与当前执行检查点不同。`interrupt()`暂停等待外部输入，使用相应Command恢复；节点恢复可能从头执行，中断前副作用需幂等。事件驱动、分支并发与pending writes的语义都应按官方Persistence（持久化）文档理解。

<details>
<summary>官方生命周期对照：State、Checkpointer、Store各在什么时候用</summary>

先声明状态与合并规则，再加入节点和边，编译图时提供需要的Checkpointer。调用图时给输入和thread_id，节点按调度轮次运行，检查点记录状态。某节点中断后，应用保存并展示待办，用户回应再用原线程上下文恢复；不是新建一个完全无关任务。

跨会话用户偏好可以放Store，在节点需要时读取。它不自动成为当前图状态，也不因检查点而自动校验正确性。并行节点失败时框架可保留已完成节点写入，但恢复单位仍由框架定义，不能恢复任意Python指令位置。

</details>

---

</details>

<details>
<summary>补充：LangChain 适合什么</summary>

### LangChain 适合什么

官方当前`create_agent`提供更高层Agent入口，并以LangGraph作为运行基础；工具、中间件、模型和结构化输出等集成减少样板代码。这与“LangChain只是旧式线性Chain，LangGraph才可以做Agent”的陈旧说法不同。

更高层默认行为适合快速实现常见任务；当控制流、状态合并和中断点需要精细设计时，可以使用底层图能力。两者不是必须二选一的竞争关系，但应确认版本和你用的具体接口，不能把早期教程与当前create_agent混为一谈。

---

</details>
