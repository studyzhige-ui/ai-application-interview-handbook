# 01. Codex Context Lifecycle｜一次模型请求到底是怎样被“编译”出来的

[← Codex 总览](README.md) · [Memory →](02-memory-lifecycle.md)

> **源码基线：** `openai/codex@75db67bbc6a18200b52698c8870adaedd7746dea`

如果只看最终发给模型的 HTTP / WebSocket 请求，很容易误以为 Codex 的上下文管理就是：

```text
instructions
+ messages
+ tools
```

源码真正复杂的地方恰好发生在这之前。

Codex 要先回答很多运行时问题：这条 Thread（线程，会话容器）之前有没有历史？当前是什么模型？工作目录和权限有没有变化？AGENTS.md 是否变了？本轮显式提到了哪个 Plugin（插件）或 Skill（技能）？某个 MCP Server 是否已经启动？过去 Memory（长期记忆）是否应该注入？这次采样能看到哪些 Tool（工具）？旧历史离 Context Window（上下文窗口）上限还有多远？

因此更准确的说法是：

> **Codex 不是“拼 Prompt”，而是在每一次模型采样前，把 Session（运行实例）中分散的状态编译成一个当下有效的模型视图。**

下面就沿这条真实生命周期往下走。

---

## 1. 一条用户输入先进入 Turn，而不是直接进入 Prompt

对 App Server 来说，客户端先通过协议发起 `TurnStart`。对 Core 来说，真正推进 Agent 工作的是 `run_turn`。

关键源码：

- `codex-rs/app-server-protocol/src/protocol/v2/turn.rs`
- `codex-rs/app-server/src/request_processors/turn_processor.rs`
- `codex-rs/core/src/session/turn.rs`

这里有一个初学者很容易误解的地方：Codex 的 Turn（轮次）不是“一次模型 API 调用”。

一次 Turn 可能长这样：

```text
用户：修复测试失败
        ↓
模型第一次采样：先运行测试
        ↓
exec_command
        ↓
工具结果：3 个测试失败
        ↓
模型第二次采样：读取相关文件
        ↓
文件工具结果
        ↓
模型第三次采样：修改代码并再次测试
        ↓
最终回答
```

这些采样和工具交互仍然属于同一个 Turn。

这也解释了为什么 `run_turn` 很长：它既要接收最初用户输入，也要处理工具回填、用户中途 steer（追加指令）、网络重试和中途上下文压缩。

### Turn 开始时先做什么

`run_turn` 并不会第一行就把用户文字塞进历史。

它先处理一批“如果不提前做，后面会破坏一致性”的事情，例如：

- 处理上一轮异步 Hook（钩子）留下的结果；
- 检查是否需要在新输入进入前先压缩旧上下文；
- 从用户输入里找显式 Plugin / MCP / Skill 依赖；
- 确定本轮需要等待哪些 MCP Server；
- 捕获本轮第一份 StepContext。

这里最值得理解的是 pre-turn compaction（轮次开始前压缩）。

假设旧历史已经接近模型上限。如果先把新用户消息写进去，再发现“装不下”，Runtime 就需要撤销刚刚写入的状态。Codex 选择先检查旧窗口，在必要时先压缩，再继续记录新输入。

因此源码里对失败路径有专门处理：即使压缩失败，也不能把用户刚提交的输入弄丢。

这不是 Prompt 技巧，而是状态一致性问题。

---

## 2. StepContext 为什么存在：它把“模型看到的世界”冻结下来

一条 Turn 可能执行很久。期间很多东西会变化：

- MCP Server 从未启动变成 ready；
- Tool Catalog（工具目录）刷新；
- 用户切换环境；
- Permission Profile（权限配置）变化；
- Plugin / Skill 选择变化；
- 用户追加新的 steer 输入。

如果 Codex 每次真正执行 Tool 时都去读取“此刻最新配置”，会出现一个很危险的时间差：

```text
模型在 10:00 看到了 Tool schema v1
        ↓
10:00:02 配置刷新成 v2
        ↓
10:00:03 模型刚才生成的 Tool Call 才开始执行
        ↓
如果直接读最新配置，它会按 v2 执行
```

于是模型作决定时看到的能力，和 Runtime 真正执行的能力，不再是同一个世界。

Codex 用 `StepContext` 解决这个问题。

源码位置：

- `codex-rs/core/src/session/step_context.rs`
- `codex-rs/core/src/session/turn.rs`
- `codex-rs/core/src/tools/parallel.rs`

可以把它理解成：

> **一次模型采样以及这次采样派生出的工具调用，共享同一张运行时快照。**

快照里会绑定这次采样真正使用的模型设置、Environment（执行环境）、Permission（权限）和 `ToolRouter`（工具路由器）。

后面 Tool Call 即使稍晚执行，也会拿着产生它的那个 `StepContext`，而不是随意读取新配置。

这也是为什么本文不会把 `StepContext` 简单翻译成“Agent 的一个步骤”。它的核心作用不是表示业务进度，而是保证 **time-of-decision（模型决策时刻）和 time-of-execution（工具执行时刻）的一致性**。

---

## 3. 初始上下文从哪里来：不是一份巨大的 System Prompt

真正组装初始模型上下文的关键函数之一是：

`Session::build_initial_context_with_world_state`

源码位置：

- `codex-rs/core/src/session/mod.rs`

这个函数最能说明 Codex 的 Context Architecture（上下文架构）为什么不是字符串拼接。

它会从多个生产者收集 Rendered Fragment（渲染片段），再根据角色和语义合并成模型消息。下面按“这些信息为什么存在”解释，而不是按字段罗列。

### 基础指令：模型本身应该怎样工作

`BaseInstructions` 是请求级基础指令。它和历史消息分开存在。

源码里还有 `get_prompt_base_instructions`：有些配置只改变“这一请求如何渲染基础指令”，却不修改已经持久化、也不修改 Fork（分叉）继承的原始指令。

这体现了一个重要边界：

> **持久状态是什么，和这一请求怎样呈现它，是两件事。**

### Developer Instructions：当前产品或任务额外规定什么

Turn 可以带 Developer Instructions（开发者指令）。

普通情况下，它们会进入开发者消息。Guardian（安全审查 Agent）等特殊内部 Session 会把某些 policy（策略）单独放成一条 developer message（开发者消息），方便审计，也避免和其他能力说明揉成一块。

### Extension Context：Memory、Skills 等扩展怎样进来

Codex 的 Extension API（扩展接口）允许扩展提供 Context。

例如 Skills Extension 和 Memories Extension 都实现了 `ContextContributor`。

它们可以向三个不同位置贡献内容：

- DeveloperPolicy：开发者策略；
- DeveloperCapabilities：开发者能力说明；
- ContextWindow：上下文窗口相关提示。

因此 Memory 和 Skills 不是 Core 里几个特判的 `if memory {...}`。它们通过正式扩展点加入 Context 编译流程。

### WorldState：当前运行环境发生了什么

`WorldState`（世界状态）保存那些“会变化、而模型有时需要知道”的运行环境信息。

例如模型切换、多 Agent 模式、运行环境与其他扩展生成的状态，都可以通过 World State 渲染为模型可见片段。

它和普通聊天历史最大的不同是：

> 聊天历史描述“发生过什么”，World State 描述“现在是什么状态”。

这两类信息更新方式也不同。

---

## 4. 为什么 Codex 不会每轮把 World State 全部重发

如果每次采样都重新生成一份完整“当前世界说明”，会有两个问题。

第一，浪费 Token。第二，也是更隐蔽的问题：Prompt Cache（提示缓存）会变得很差，因为早期上下文不断变化。

Codex 因此维护 reference context（参考上下文基线）和 World State baseline（世界状态基线）。

关键源码：

- `Session::record_context_updates_and_set_reference_context_item`
- `codex-rs/core/src/context/world_state/`
- `codex-rs/core/src/context_manager/updates.rs`

第一次真正建立模型上下文时，没有旧基线：

```text
没有 reference context
        ↓
构造完整 World State
        ↓
渲染完整初始 Context
        ↓
把这份 World State 记成 baseline
        ↓
记录 TurnContextItem
```

后续 Turn 再开始时：

```text
重新计算当前 World State
        ↓
和 baseline 比较
        ↓
只生成变化部分
        ↓
把差异追加进模型历史
```

所以正常路径是“增量追加”，不是“重新写一遍过去”。

这一点不是我们的教材推导。Codex 仓库根目录自己的 `AGENTS.md` 就明确要求：model-visible context（模型可见上下文）应尽量增量构建，避免不必要改写导致 cache miss（缓存失效），而自动注入的内容必须有硬上限。

换句话说，Prompt Cache 不是最后再加的一项性能优化，它反过来影响了 Context 的数据结构。

---

## 5. History 是怎样进入下一次模型请求的

Codex 用 `ContextManager` 管理模型相关的 canonical history（规范历史）。

关键源码：

- `codex-rs/core/src/context_manager/`
- `codex-rs/history/`

这里要和两样东西区分开。

`ThreadStore / Rollout` 是持久化边界，负责以后能恢复；`Rollout Trace` 是诊断证据；`ContextManager` 才是 Runtime 当前真正拿来构造模型历史的对象。

普通情况下，历史是追加的：

```text
用户消息
→ 模型 Tool Call
→ Tool Result
→ 模型下一次输出
→ ...
```

只有明确的 Context Window 重置、Compaction 或恢复重建，才会走 `replace_annotated` 这类替换路径。

### 为什么还需要 normalize（规范化）

真实 Agent 历史可能出现不完整结构。

例如模型已经产生了 Function Call（函数调用），用户却马上取消；或者旧 Provider（模型提供方）留下了当前模型不支持的媒体项。

如果下一次请求直接把这些不完整对象发送出去，Responses API 可能拒绝，模型也可能错误理解。

因此 `context_manager/normalize.rs` 会修复历史协议结构，例如：

- 给缺失的 Tool Result 补一个结构化 aborted output（中止结果）；
- 去掉找不到对应 Tool Call 的孤立 output；
- 处理当前模型不支持的媒体内容。

这说明 Context 管理不仅是“删旧消息”，还要维护 **对话协议本身的结构合法性**。

---

## 6. Tool Result 为什么也是 Context 的一部分

很多初学者把 Tool System 和 Context System 分开学，容易漏掉最关键的一步：

> 工具执行结束以后，结果必须重新进入模型可见历史，否则下一次模型根本不知道现实世界发生了什么。

真实链路是：

```text
模型请求 N
    ↓
模型返回 function_call(call_id = c1)
    ↓
ToolRouter 找到执行器
    ↓
Runtime 执行
    ↓
生成 FunctionCallOutput(call_id = c1)
    ↓
记录到 ContextManager
    ↓
模型请求 N+1
```

所以 Tool Call 的 `call_id`（调用标识）不仅是日志字段，它是上下文协议里把“动作”和“观察结果”连起来的关联键。

取消也必须产生结果，原因也是一样：如果留下一个只有 Call、没有 Output 的历史，下次模型就面对一个未闭合动作。

Tool Lifecycle 那篇会继续讲执行细节；这里先记住一件事：

> **Agent 的 Context 是不断被现实执行结果改写的，不是用户和模型之间的纯文本聊天记录。**

---

## 7. Prompt Cache 到底缓存什么：不要和历史持久化混在一起

Codex 源码里至少有三件经常被一起叫“缓存”的机制，但它们其实不同。

### Prompt Cache Key：给服务端稳定的缓存亲和键

`ModelClient::prompt_cache_key` 会为请求选择稳定 key（键）。

普通根 Session 通常和当前 session identity（会话身份）绑定；一些内部 Session 会结合内部来源和 parent thread（父线程）来形成 key。

它解决的是：

> 这些请求应该尽量落到同一个 Prompt Cache 亲和范围里。

但同一个 key 不保证缓存一定命中。如果前缀文本每次都变，服务端仍然无法复用大量 prefill（前缀计算）。

这就是为什么前面 World State 要做增量更新。

### WebSocket continuation：同一 Turn 内复用上一次 Responses 状态

`ModelClientSession` 是 Turn-scoped（轮次级）的模型会话对象。

源码位置：

- `codex-rs/core/src/client.rs`

它会保存上一份完整 request、上一份 response 和 `x-codex-turn-state`。如果下一次请求只是上一请求的兼容增量，就可以使用 continuation（续写）能力，避免重新发送不必要的部分。

源码会逐项比较模型、instructions、tools、reasoning、service tier 等属性，确认当前请求仍与上一请求兼容。

### ThreadStore：完全不是 Prompt Cache

ThreadStore 保存的是以后 Resume / Fork 所需的长期状态。

因此：

```text
Prompt Cache
= 服务模型推理效率

WebSocket continuation
= 服务同一 Turn 内增量请求

ThreadStore
= 服务长期恢复
```

三者不能混成“Codex 有缓存”。

---

## 8. Context Window 变大以后，Codex 怎样决定要不要压缩

`session/context_window.rs` 并不是简单计算：

```text
模型上限 - 当前 tokens
```

源码还会考虑：

- model effective context window（模型有效窗口）；
- auto compact limit（自动压缩阈值）；
-阈值按 Total 还是 BodyAfterPrefix 计算；
- server prefill；
- hard full-window limit；
-当前 context window identity。

为什么会有 `BodyAfterPrefix` 这种概念？

因为一部分前缀是稳定且不适合压缩的，例如长期 instructions 和固定能力说明。真正不断增长的是后面的历史 body（主体）。

如果每次都按总 Token 数触发，就可能因为稳定前缀本身较大而过早压缩。

因此成熟 Context Budget（上下文预算）真正要问的是：

> **哪些部分是稳定前缀？哪些部分会增长？哪些部分允许被压缩？**

---

## 9. Compaction 不是只有“让模型写摘要”这一种实现

Codex 当前源码至少有三条相关路径。

### Local Compaction：本地编排摘要压缩

`codex-rs/core/src/compact.rs`

Runtime 会复制当前历史，加入专门的压缩请求，让模型生成 summary（摘要），再把需要保留的用户上下文与摘要重新组成一份 replacement history（替代历史）。

关键产物不是那段 summary 本身，而是：

> **一份以后可以直接作为新上下文基线的 replacement history。**

### Remote Compaction V2：由模型服务提供远端压缩

`codex-rs/core/src/compact_remote_v2.rs`

Provider 支持时，Codex 可以调用专门的 Responses Compaction 能力。

虽然实现位置不同，但它仍然进入同一套生命周期：有 trigger（触发原因）、phase（发生阶段）、analytics（分析事件）和最后的 history replacement（历史替换）。

### Token Budget：直接开始新的上下文窗口

`codex-rs/core/src/compact_token_budget.rs`

某些情况下并不要求先生成一段文本摘要，而是创建新的 Context Window，再重新注入当前需要的初始上下文。

所以更准确的定义是：

> **Compaction 是“从旧上下文窗口迁移到一个更小、仍可继续工作的模型状态”的过程。摘要只是其中一种迁移手段。**

---

## 10. 为什么压缩以后还能 Resume：因为它被做成了 Checkpoint

如果 Compaction 只修改内存里的 `ContextManager`，进程一退出，这次压缩就没有长期意义。

因此成功压缩还会持久化 `CompactedItem`，现代路径可以保存 `replacement_history`。

恢复逻辑在：

- `codex-rs/core/src/session/rollout_reconstruction.rs`
- `codex-rs/thread-store/src/local/model_context.rs`

Resume（恢复）时，Codex 不会永远从第一条 Rollout JSONL 开始重放。

它会从尾部向前寻找最新、仍然有效的 replacement-history checkpoint（替代历史检查点）。找到以后：

```text
replacement_history
= 新历史基线

checkpoint 之后仍然存活的 rollout suffix
= 需要继续重放的增量
```

比这个 checkpoint 更早的原始历史，不再需要逐条参与模型上下文重建。

这就是为什么 Context Compaction 和 Persistence（持久化）不能分开理解：前者提供新的模型历史基线，后者让这份基线在进程退出后仍然可恢复。

### Fork 和 Rollback 为什么更难

Fork（分叉）要求子 Thread 只继承父 Thread 某个截止点；Rollback（回滚）则可能删除最近若干真实用户 Turn。

因此恢复时不仅要找“最新 checkpoint”，还要确认这个 checkpoint 是否仍属于 surviving segment（仍然有效的历史片段）。

同时 World State 还有 full snapshot（完整快照）和 merge patch（合并补丁），Compaction 又会让旧 baseline 失效。

所以恢复真正重建的是：

> **模型历史 + 当前 World State + Turn 设置 + Context Window 身份 + Token 状态。**

不是简单“把聊天记录读回来”。

---

## 11. 用一条完整例子把 Context 生命周期串起来

假设用户说：

> “修复支付模块的测试失败，不要改变公开 API。”

第一次采样前，Codex 先确认旧上下文是否需要压缩，然后捕获 StepContext。Session 从 Developer Instructions、项目 AGENTS.md、当前 Environment、Permission、Memory、Skills 等来源构建初始上下文；World State 建立 baseline；Tool Router 同时生成本轮模型可见工具。

模型决定先运行测试。Tool 执行后，失败日志以 Tool Result 的形式进入历史。

第二次采样时，Codex不会重新把所有环境说明和 AGENTS.md 从头拼一遍，而是沿着已有 history 追加新结果；只有 World State 或 TurnContext 真正发生变化时，才追加相应差异。

如果经过很多工具调用后 Context 太长，Runtime 会根据 Provider 与 Feature 选择 Local Compaction、Remote Compaction 或新的 Token-Budget Window。压缩成功后，新 replacement history 被安装进 ContextManager，同时作为 checkpoint 写入持久化记录。

进程退出后再 Resume，Runtime 从最近仍有效的 replacement-history checkpoint 加后续增量重建 Session。模型继续工作时，仍应知道最开始那个“不要改变公开 API”的约束。

这最后一句其实就是 Context 系统最重要的效果指标：

> **经过工具调用、压缩、进程退出和恢复以后，决定未来行为的关键约束仍然不能丢。**

这也是为什么 Context Evaluation（上下文评测）应该测约束保留和恢复等价性，而不是只看“摘要读起来顺不顺”。

---

## 12. 源码锚点与阅读建议

如果要自己回源码验证，建议按调用顺序读，而不是按文件夹随机浏览：

1. [`app-server-protocol/src/protocol/v2/turn.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/app-server-protocol/src/protocol/v2/turn.rs)：产品层 Turn 请求长什么样。
2. [`core/src/session/turn.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/session/turn.rs)：真正的 Agent Turn 循环。
3. [`core/src/session/mod.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/session/mod.rs)：初始 Context、World State 更新、历史持久化。
4. [`core/src/context/`](https://github.com/openai/codex/tree/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/context)：不同 Context Fragment 的真实类型。
5. [`ext/extension-api/src/contributors/`](https://github.com/openai/codex/tree/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/ext/extension-api/src/contributors)：扩展怎样参与 Context。
6. [`core/src/context_manager/`](https://github.com/openai/codex/tree/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/context_manager)：规范历史、差异和 normalize。
7. [`core/src/client.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/client.rs)：Prompt Cache、WebSocket continuation、请求发送。
8. [`core/src/session/context_window.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/session/context_window.rs)：Token 与窗口判断。
9. [`core/src/compact.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/compact.rs)、[`compact_remote_v2.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/compact_remote_v2.rs)、[`compact_token_budget.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/compact_token_budget.rs)：三类窗口迁移。
10. [`core/src/session/rollout_reconstruction.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/session/rollout_reconstruction.rs)：压缩后的恢复闭环。

下一篇：[Codex Memory Lifecycle →](02-memory-lifecycle.md)
