# 01. Codex Context Lifecycle｜一条用户输入怎样变成模型真正看到的上下文

[← Codex 总览](README.md) · [Memory →](02-memory-lifecycle.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

Context（上下文）最容易被写成一张“字段清单”：system prompt、history、tools、memory……但这样学完以后，仍然不知道这些内容是谁加进去的、什么时候更新、为什么有些内容每轮都不重发。

这一篇换一个读法。假设用户在 Codex TUI 里说：

> “修掉这个失败测试，不要改公开 API，完成后运行相关测试。”

我们沿真实源码看，这句话怎样从客户端一路走到模型；模型调用工具以后，结果又怎样进入下一次请求；对话越来越长以后，Codex 怎样换 Context Window（上下文窗口），最后进程重启时又怎样恢复。

---

## 1. 上下文生命周期从 App Server 的输入边界开始

TUI 并不会直接调用模型。它通过 App Server Client（应用服务器客户端）发送类型化 JSON-RPC 请求。对于一次新的用户任务，重要入口之一是 `turn/start`，对应 `app-server/src/request_processors/turn_processor.rs`。

这里先做的是程序可以确定的校验，而不是把所有问题交给模型。例如源码会检查用户输入总长度，也会拒绝当前接口不允许的远程图片 URL。只有请求满足协议要求，App Server 才找到目标 Thread（线程 / 持续会话容器），把输入转换成 Core 能理解的操作。

所以第一层关系是：

~~~text
用户输入
→ 产品协议校验
→ 找到 Thread
→ 提交 Core Operation（核心操作）
→ 才进入 Agent Turn
~~~

这一步看似和“Prompt Engineering（提示工程）”无关，却决定了什么东西根本不应该进入 Prompt。输入格式、目标 Thread 是否存在、调用者是否允许直接输入，这些都是 Runtime（运行时）可以确定的事实，没有必要让模型猜。

---

## 2. Codex 的 Turn 不是“一次模型调用”

进入 Core 以后，`run_turn` 驱动一次 Codex Turn（一次用户任务推进）。

一个 Turn 可以发生很多次模型采样。模型第一次可能决定读文件，Runtime 执行后把结果加入历史；第二次模型看到文件内容，再决定运行测试；测试失败以后还可能继续修改代码。直到模型给出最终回答、用户中断、发生不可恢复错误，或者 Runtime 触发其他终止条件，这个 Turn 才结束。

可以把一次真实 Turn 理解为：

~~~text
用户任务
↓
模型采样 1
→ Tool Call（工具调用）
→ Tool Result（工具结果）
↓
模型采样 2
→ Tool Call
→ Tool Result
↓
模型采样 3
→ 最终回答
↓
Turn 结束
~~~

这也是为什么“Chat History（聊天历史）长度”等指标很容易误导。一个用户 Turn 里面就可能产生大量模型消息、工具调用和观察结果。

---

## 3. 为什么 Turn 里面还需要 Step Context

在同一个 Turn 里，运行环境并不是永远不变。

MCP Server（MCP 服务器）可能刚刚完成启动，插件目录可能刷新，用户可能在运行中追加一条 Steer（引导指令），某个远程执行环境也可能从“尚未就绪”变成“可用”。如果每次真正执行 Tool Call 时都读取“此刻最新”的全局状态，就会出现一个危险问题：

> 模型是根据旧能力做出的决定，执行时却偷偷换成了新能力。

Codex 用 `StepContext（步骤上下文）` 避免这种时间错位。

源码把它定义为**一次模型请求范围内的状态快照**。创建 Step Context 时，会把这一次采样需要共同保持一致的东西一起捕获：Resolved Step Settings（解析后的步骤设置）、Environment Snapshot（执行环境快照）、MCP Binding（MCP 连接与目录快照）、Tool Router（这一步最终可见和可执行的工具计划）、已经加载的 `AGENTS.md` 等。

其中最值得记住的不是字段名，而是这个不变量：

> **模型在这次 Step 看见的能力，与这次 Step 产生的 Tool Call 后续真正使用的能力，应来自同一份快照。**

所以 Step Context 是“模型可见世界”和“真实执行世界”之间的一致性边界。

---

## 4. 一次模型请求前，Codex 先重建当前 World State

Step Context 捕获完成以后，`Session::build_world_state_for_step` 会构建 World State（世界状态）。

这里的 “World” 不是一个虚构的游戏世界，而是：

> **这一刻会影响模型决策、并且需要以结构化方式投影给模型的运行条件。**

例如模型是否刚切换、当前是什么执行环境、审批和权限怎样约束命令、是否启用多 Agent、是否存在可发现但尚未展开的工具命名空间、`AGENTS.md` 当前内容是什么，这些都不是普通对话消息，但模型做正确决定时可能必须知道。

源码没有把这些东西拼成一个巨大字符串，而是拆成有稳定身份的 section（状态片段）。不同 section 可以比较旧值和新值，并决定是否需要生成新的 model-visible fragment（模型可见片段）。

这就是 World State 与普通 History（历史）的区别：

~~~text
History
记录“之前发生了什么”

World State
描述“当前运行条件是什么”
~~~

两者最后都可能进入模型请求，但更新方式不一样。

---

## 5. World State 里最重要的是关系，不是字段数量

直接看 `world_state.rs` 会看到很多类型名。如果逐个列出，只会把读者淹没。更适合从它们解决的问题来理解。

### 5.1 模型和长期指令有没有变化

`ModelInstructionsState` 负责当前模型对应的指令；`AgentsMdState` 记录当前环境里加载到的 `AGENTS.md`；受管理配置还可以贡献额外 developer instructions（开发者指令）。

为什么这些内容必须有状态身份？

因为模型切换、项目目录切换或管理配置变化以后，过去那份指令可能已经失效。Runtime 需要知道“这是同一份，还是需要向模型说明变化”，而不是每轮无脑重发整段文本。

### 5.2 当前允许模型做什么

权限相关 section 会把 Permission Profile（权限配置）、Approval Policy（批准策略）、执行策略等投影给模型。这样模型知道某个动作是否可能需要批准，但真正的安全边界仍然在 Runtime；模型看见“需要批准”并不等于模型自己获得了批准权。

### 5.3 当前在哪些环境工作

Environment（环境）相关 section 描述当前工作目录、执行环境和环境说明。多环境场景下，Tool Schema（工具模式）甚至可能需要显式带 environment ID，保证命令被送到正确执行端。

### 5.4 当前有哪些高级能力

Apps、Plugins、Deferred Tools（延迟加载工具）、Multi-Agent Mode（多智能体模式）等 section 负责让模型知道“有哪些能力类别存在”。这里通常只给必要的世界状态，不等于把每个具体 Tool Schema 全部塞进去。

这四组关系比背几十个 State 类型更重要：**指令、权限、环境、能力目录**共同定义模型这一刻所处的运行世界。

---

## 6. Extension 也能参与 Context，但入口是受控的

Memory、Skills、插件等能力不是随便在 Prompt 最前面插一段字符串。

`Extension API（扩展接口）` 提供 `ContextContributor（上下文贡献者）`。扩展可以贡献 thread-scoped context（线程级稳定上下文）、turn-scoped context（本 Turn 的上下文）以及 World State section。

例如 Memory Extension 会把经过整理和截断的 `memory_summary.md` 渲染成 developer-policy context（开发者策略上下文）；Skills Extension 会在预算允许范围内贡献可用 Skill 的目录信息。

这个设计有两个好处。

第一，Core 知道这些内容来自哪个生命周期。稳定的 Thread Context 不需要像瞬时 Turn 数据一样频繁变动。

第二，扩展产物仍然经过统一的 Prompt Fragment / World State 机制，而不是各自直接修改历史。这使增量更新、持久化和测试有共同边界。

---

## 7. 第一次进入一个 Context Window 时，Codex 会建立完整基线

`record_context_updates_and_set_reference_context_item` 是理解增量 Context 的另一个关键函数。

如果当前还没有 `reference_context_item（参考上下文项）`，说明 Runtime 没有可比较的持久基线。这时会：

~~~text
构造当前 World State
↓
生成完整 initial context（初始上下文）
↓
把 World State 保存为 full snapshot（完整快照）
↓
把模型可见内容写入 canonical history
↓
持久化 TurnContextItem
↓
把它设为后续比较的 reference
~~~

这里的重点不是“第一次 Prompt 特别长”，而是：

> **从这一刻开始，Runtime 有了一份“模型已经被告知过什么”的基准。**

后续 Turn 就不必每次重新打印整个世界。

---

## 8. 稳态运行时主要发送变化，而不是重写过去

已有 reference baseline（参考基线）以后，Codex 会重新构造当前 World State，并让 Context Manager 比较新旧 section。

如果某个环境、权限或能力状态没有变化，就不需要重复形成相同的上下文项；有变化时，才渲染对应 diff（差异）。

因此正常路径更接近：

~~~text
初始完整状态
+ 用户输入
+ Tool Call / Tool Result
+ 后续状态变化
+ 后续用户输入
...
~~~

而不是：

~~~text
每轮：
重新生成一份“当前所有规则 + 所有状态 + 所有历史”
~~~

Codex 根目录 `AGENTS.md` 甚至把这点写成源码开发约束：model-visible context（模型可见上下文）在普通流程里应该尽量增量追加，自动注入内容必须有硬上限，并且要避免频繁变化破坏 Prompt Cache（提示缓存）。

这不是纯性能技巧。增量历史还让我们能回答“这个状态是什么时候改变的”，对恢复和排障都更可靠。

---

## 9. 用户在运行中追加指令，为什么不能直接插进未完成的 Tool Pair

App Server 提供 `turn/steer`，允许用户在一个正在执行的 Turn 中继续补充信息。

Core 的 Turn Loop 会在安全的处理边界读取 pending input（待处理输入），把它按顺序记录进历史，再捕获新的 Step Context。这样新用户消息不会随意插到一个尚未完成的 Tool Call / Tool Result 中间。

原因可以用一个简单例子理解。

假设模型已经发出：

~~~text
call_id = c1
run_tests(...)
~~~

但结果还没回来。这时用户又说：

> “先别跑全量测试，只跑这个文件。”

如果 Runtime 直接把这句话塞到 Tool Call 与 Tool Result 之间，模型历史的协议结构就可能被破坏。更稳妥的做法是由 Runtime 决定当前动作是否可中断，并在下一次合法 sampling boundary（采样边界）让新输入生效。

---

## 10. Tool Result 回到 History 时，重点是保持因果配对

模型发出的 Function Call（函数调用）和 Runtime 返回的 Function Call Output（函数调用输出）通过 call ID 关联。

这不是排版细节。如果调用结果缺失，下一轮模型可能不知道某个副作用是否发生；如果结果错配到另一个 call ID，并发执行时甚至会形成错误事实。

因此 Context Manager 的 normalize（规范化）逻辑会处理异常历史，例如补充缺失调用的 aborted output（中止输出），或者移除孤立结果。它的目标是保证送给模型的 History 仍然满足协议和因果关系。

可以把这部分理解成：

> **History 不是“把日志按时间拼起来”，而是模型能继续推理的一份结构化因果记录。**

---

## 11. 真正发给模型的 Prompt 由不同物理部分组成

到了模型客户端，Codex 不会把所有内容统一塞进一个 system string。

抽象来看，请求里至少有：

~~~text
Base Instructions（基础指令）
+
Input / History（输入与规范化历史）
+
Tools（这一步模型可见的工具定义）
+
推理 / 输出等请求设置
~~~

`Base Instructions` 是请求级基础指令；History 来自 Context Manager；Tool definitions（工具定义）来自这一次 Step Context 中已经 finalize（定稿）的 Tool Router。

这也说明一个常见误解：

> **Tool Schema 虽然不一定出现在聊天消息文本里，但它仍然是模型请求上下文的一部分。**

工具过多时，成本和选择质量都会受到影响，所以 Tool Lifecycle 才需要 Deferred Discovery（延迟发现）。

---

## 12. Codex 里至少有三件不同的“缓存 / 续接”机制

上一版把它们放得太近，容易让人以为都是同一种 Prompt Cache。实际应分开理解。

### 12.1 `prompt_cache_key`：缓存亲和键

Model Client 会生成相对稳定的 `prompt_cache_key（提示缓存键）`。它帮助服务端识别适合复用的请求前缀，但一个 key 相同并不保证命中：如果前缀内容本身一直变化，缓存价值仍然会下降。

### 12.2 稳定前缀：Context 结构本身的缓存友好性

这不是一个 API 字段，而是整个上下文架构产生的效果。初始状态稳定、后续主要追加 diff、自动注入有界、Synthetic ID（合成标识）尽量稳定，这些都会减少早期 Context 无谓抖动。

### 12.3 `previous_response_id` / WebSocket continuation：同一 Turn 内的增量续接

`ModelClientSession（模型客户端会话）` 是 Turn-scoped（Turn 级）的。它会保存 WebSocket 连接、上一份请求和 sticky routing state（粘性路由状态）。只有新请求与上一请求在模型、指令、工具、推理设置等方面兼容，并且只是合法增量时，才可以使用 continuation（续接）路径。

所以：

~~~text
prompt_cache_key
≠
WebSocket 复用
≠
previous_response_id 续接
~~~

它们共同优化重复前缀和连续请求，但生命周期与判断条件不同。

---

## 13. 为什么 ModelClientSession 不能跨 Turn 随便复用

源码对这一点写得很明确。

Model Client（模型客户端）是 Session 级共享对象；`ModelClientSession` 则每个 Codex Turn 新建。后者保存 `x-codex-turn-state`，这是服务端在一次 Turn 中使用的 sticky routing token（粘性路由令牌）。

同一 Turn 的重试和后续请求需要继续携带它，但新的 Turn 不能继承上一 Turn 的 token。认证主体变化时也需要清理旧状态。

因此可以记住这三个层级：

~~~text
ModelClient
长期 Session 共享

ModelClientSession
一个 Codex Turn 内共享

StepContext
一次模型采样使用
~~~

它们分别解决“长期连接配置”“同一 Turn 连续请求”“单次采样一致性”。

---

## 14. Context Window 不是只有一个“剩余 Token”数字

随着 History 和 Tool Result 增长，Codex 会维护 Context Window（上下文窗口）状态。

当前源码不仅关心模型总窗口，还支持不同 auto-compaction scope（自动压缩计量范围）。例如某些配置可以只看 stable prefix（稳定前缀）之后持续增长的 body，而不是把不可压缩的前缀也同等算入触发阈值。

为什么要这样做？

假设固定系统指令和工具前缀已经占了很大一部分，但真正可以通过摘要减少的是后面的对话历史。单纯按“总 Token 达到 X”判断，很可能太早或太晚触发压缩。

所以 Context Budget（上下文预算）实际是在回答：

> **哪一部分在增长？哪一部分能被替换？为下一次模型输出和后续 Tool Result 要留多少空间？**

---

## 15. Codex 的 Compaction 不只有“让模型写摘要”

当前固定源码里可以看到三类不同路径，它们共享“切换 Context Window 基线”的目标，但实现不同。

### 15.1 Local Compaction（本地编排的摘要压缩）

`compact.rs` 会从当前历史构造压缩请求，让模型生成 summary（摘要），再把必要的用户消息、保留上下文和摘要组合成新的 replacement history（替代历史）。

重要产物不是那段 summary 本身，而是：

> **一份以后可以作为新 Context 基线继续运行的结构化历史。**

### 15.2 Remote Compaction V2（远端压缩）

支持的模型提供方可以使用 Responses 侧的 remote compaction。压缩发生位置不同，但它仍然进入 Codex 自己的 Compaction 生命周期：触发原因、阶段、事件、结果安装和持久化都要由 Runtime 管理。

### 15.3 Token Budget 的 New Context Window（新上下文窗口）

Token Budget 模式下，Codex 还可以直接开启新的 Context Window，重新注入完整初始 Context，而不是一定生成一段传统摘要。

因此更准确的说法是：

> **Compaction 是“如何把一个过大的模型工作窗口迁移到新的可继续执行基线”；摘要只是其中一种迁移策略。**

---

## 16. Pre-turn 和 Mid-turn Compaction 为什么不能完全一样

压缩发生的时机决定“压完以后模型接下来要继续什么”。

如果是 Turn 开始前，新的用户输入还没有进入当前 History，压缩失败时尤其要保证这条输入不会丢失。

如果是 Turn 中间，用户任务已经在执行，可能刚完成一个 Tool Call。压缩后下一次模型采样必须继续理解当前目标和刚发生的执行结果，而不是像新会话一样从零开始。

这也是为什么源码给 Compaction 记录 Phase（阶段），并根据阶段选择 initial context 是否以及在哪里重新注入。

---

## 17. Compaction 成功以后，为什么还要持久化 replacement history

如果压缩只改内存里的 Context Manager，当前进程也许还能继续；但一旦用户退出 Codex，再 Resume（恢复），系统就不知道压缩后的真实基线是什么。

因此 `CompactedItem` 会把 replacement history 和相关 Window metadata（窗口元数据）写入持久化历史。

这一步把：

~~~text
上下文压缩
~~~

从“当前请求的 Token 优化”升级成：

~~~text
长期会话的可恢复状态转换
~~~

---

## 18. Resume 不是重新播放整个聊天文件

Local Thread Store（本地线程存储）会保存 Rollout（运行记录）。如果一个 Thread 很长，每次 Resume 都从第一条 JSONL 重新重放，成本会随着会话寿命无限增长。

`rollout_reconstruction.rs` 的现代路径会从尾部反向扫描，寻找最新、仍然有效的 replacement-history checkpoint（替代历史检查点），同时收集恢复所需的 Turn settings、World State baseline 和 Context Window 标识。

找到后：

~~~text
replacement history
= 新的完整历史基线

checkpoint 之后仍然有效的 suffix
= 需要继续正向 replay 的尾部
~~~

更老的历史就不必再次参与模型 Context 的重建。

所以 Compaction 和 Resume 是一套机制的前后两半：**前者制造可恢复的新基线，后者利用它缩短恢复路径。**

---

## 19. Fork 比普通 Resume 更严格，因为它有历史截止点

Fork（分叉）不是复制“当前所有状态”这么简单。调用方可以要求只继承父 Thread 到某个历史位置。

这意味着恢复代码必须同时尊重：

- 父 Thread 的 checkpoint；
- Fork cutoff（分叉截止位置）；
- 已经回滚 / 中断的 Turn；
- World State snapshot 与后续 patch；
- 当前 Window 标识。

如果把 cutoff 之后的 Tool Result 或权限状态带进子 Thread，就会让子 Agent“知道未来”。

因此持久化层里看到的大量 replay / lineage（谱系）代码，并不是为了把实现写复杂，而是在守住“子会话只能继承允许的历史前缀”这个不变量。

---

## 20. 三个典型故障，用生命周期来排查

### 故障一：Compaction 后模型忘了“不能改公开 API”

不要先改 Prompt。先顺序问：

原始用户约束是否进入 canonical history？压缩输入是否包含它？压缩输出是否保留？replacement history 安装以后是否仍然可见？如果中途 Resume，恢复是否选择了正确 checkpoint？

这样才能定位信息在哪一环丢失。

### 故障二：Tool 已经执行，但下一次模型不知道

先检查 call / result pairing 是否完整，再看 Tool Result 是否成功记录进 History。若历史结构异常，Context normalization 是否补了 aborted output？这类问题本质是因果历史损坏，不是模型“记性差”。

### 故障三：同一个 Turn 连续请求突然无法续接缓存

检查 Step 之间是不是修改了模型、基础指令、工具集合、推理设置或其他 continuation compatibility（续接兼容性）字段；再看是不是错误跨 Turn 复用了 ModelClientSession。缓存问题要先查请求身份是否稳定，而不是只看 Token 数。

---

## 21. 这套 Context 架构真正想解决什么

把代码重新连起来，会发现 Codex Context Engineering（上下文工程）同时服务四个目标：

**正确性。** 模型看见的环境、权限、工具和真正执行时的状态要一致。

**成本与延迟。** 稳定内容尽量不反复变化，大量能力按需加载，长历史在必要时迁移窗口。

**恢复。** Context 的重要状态变化要能落到 Rollout，进程退出后可以重建。

**可解释性。** World State section、Tool Call、Compaction event 都保留结构，使系统能解释“模型当时为什么看见这些内容”。

如果只把 Context 理解成“Prompt 字符串”，这四个目标都会消失。

---

## 22. 源码核验入口

建议按调用关系阅读，而不是按文件名随机跳转：

1. [`app-server/src/request_processors/turn_processor.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/app-server/src/request_processors/turn_processor.rs)：外部 Turn 输入怎样进入 Core。
2. [`core/src/session/turn.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/turn.rs)：一个 Codex Turn 的模型—工具循环。
3. [`core/src/session/step_context.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/step_context.rs)：单次采样的不可混版本快照。
4. [`core/src/session/world_state.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/world_state.rs)：当前运行世界怎样形成 typed sections（类型化状态片段）。
5. [`ext/extension-api/src/contributors.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/extension-api/src/contributors.rs)：扩展怎样贡献 Context 与 World State。
6. [`core/src/session/mod.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/mod.rs)：initial context、reference baseline、World State diff 与持久化。
7. [`core/src/context_manager/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/context_manager)：History、normalize 与更新。
8. [`core/src/client.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/client.rs)：ModelClient、Prompt Cache 和 Turn-scoped continuation。
9. [`core/src/compact.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/compact.rs) 与 [`compact_remote_v2.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/compact_remote_v2.rs)：压缩路径。
10. [`core/src/session/rollout_reconstruction.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/rollout_reconstruction.rs)：Resume / Fork 的重建。

下一篇：[Codex Memory Lifecycle →](02-memory-lifecycle.md)
