# 04. Codex Engineering & Evaluation｜把 Context、Memory、Tool 放回完整产品里看

[← Tool](03-tool-lifecycle.md) · [Codex 总览](README.md)

> **源码基线：** `openai/codex@75db67bbc6a18200b52698c8870adaedd7746dea`

前面三篇分别沿 Context（上下文）、Memory（长期记忆）和 Tool（工具）追了一条完整生命周期。

但真实 Codex 不是三个模块并排摆着。它们都依附在同一个 Session（运行实例）上，和 App Server、Extension Registry（扩展注册表）、Multi-Agent（多智能体）、Code Mode（代码模式）、Exec Server（执行服务器）、Thread Store（线程存储）、State DB（状态数据库）以及 Rollout Trace（运行追踪）共同工作。

所以这一篇不再增加一堆新名词，而是回答一个更实际的问题：

> **如果 Codex 已经运行几十轮、连接了很多能力、拉起了子 Agent、经历过网络断开和 Context Compaction（上下文压缩），它靠什么保证还能继续运行、还能恢复、还能解释“刚才到底发生了什么”？**

---

## 1. 先看 Session 里到底装着什么

理解整个系统最直接的源码之一是：

- `codex-rs/core/src/state/service.rs`

`SessionServices` 不是为了让我们背字段，而是揭示了一条 Thread 在 Core 运行时真正依赖哪些长期服务。

可以把它分成几组来理解。

### 模型与推理

Session 持有一个 session-scoped `ModelClient`（会话级模型客户端）。每个 Turn 又会从它创建 turn-scoped `ModelClientSession`。

这保证长期认证、Provider（模型提供方）和连接策略可以复用，但 Turn 的 sticky routing state（粘性路由状态）不会泄漏到下一轮。

### 能力系统

Session 同时持有：

- MCP Runtime；
- Plugins Manager（插件管理器）；
- Skills Service（技能服务）；
- Extension Registry；
- Tool Search Cache；
- Code Mode Service。

也就是说，模型可调用能力不是在 `run_turn` 里临时硬编码出来的，而是 Session 长期维护能力来源，每个 Step 再根据当时状态投影出一份 Tool Router。

### 执行与安全

Session 还持有：

- Exec Policy Manager（执行策略管理器）；
- Approval Store（批准记录）；
- Network Approval Service（网络批准服务）；
- Unified Exec Process Manager（统一进程执行管理器）；
-当前 Environment 集合。

所以“模型决定运行命令”只占很小一段，真正的可执行性由 Runtime 长期服务共同决定。

### 持久化与诊断

Session 还有：

- LiveThread；
- ThreadStore；
- State DB；
- Session Telemetry；
- Analytics Client；
- Rollout Trace Context。

这说明 Codex 的一条 Thread 从一开始就是“可持久化、可观测、可恢复”的运行对象，而不是先做一个聊天循环，之后再补日志。

---

## 2. Extension Registry 是怎样把 Memory、Skills、MCP 接进来的

之前三篇里我们已经看到 Memory Extension、Skills Extension，但如果只分别看它们，很容易误以为这是几个互不相关的特例。

真正的总入口之一在：

- `codex-rs/app-server/src/extensions.rs`
- `codex-rs/ext/extension-api/`

App Server 会建立 `ExtensionRegistryBuilder`，再依次安装 Queue、History Notes、Goal、Git Attribution、Guardian、Memories、MCP、Web Search、Image Generation、Skills 等扩展。

Extension API 允许一个扩展参与很多生命周期，而不是只能“注册一个 Tool”。

例如扩展可以监听：

```text
Thread Start / Resume / Stop
Turn Start / Stop / Abort / Error
Context contribution
World State contribution
Tool contribution
Tool Start / Finish
Token usage
Skill invocation
MCP server contribution
```

这解释了为什么 Codex 的 Memory 能同时做到：

- Thread 启动时准备自己的状态；
-向 Context 注入 summary；
-注册 search / read / note Tool；
-记录使用情况。

也解释了 Skills 为什么既会影响 Context，又会贡献 Tool 和 World State。

因此真正稳定的架构不是：

```text
Core 里写 memory if
Core 里写 skills if
Core 里写 mcp if
```

而是：

> **Core 提供生命周期插槽，能力模块通过 Extension Registry 接入。**

这是当前源码里非常重要的一层，也是上一版文档没有充分讲清楚的地方。

---

## 3. Multi-Agent 在 Codex 里不是“两个模型互相发 A2A 消息”

Codex 当前 Multi-Agent V2 有自己的内部 Agent Control（Agent 控制）抽象。

关键源码：

- `codex-rs/core/src/agent/api.rs`
- `codex-rs/core/src/agent/types.rs`
- `codex-rs/core/src/tools/handlers/multi_agents_v2.rs`
- `codex-rs/core/src/tools/multi_agent_tool.rs`

`AgentControl` 管的是一棵 Agent Tree（智能体树），操作包括：

- spawn：创建子 Agent；
- resume：恢复；
- send：发送任务或消息；
- interrupt：中断当前工作；
- close：关闭 Agent 及其后代；
- inspect / list / watch：查询状态；
- admit_turn：控制树级并发容量；
- record_usage：记录共享预算；
- turn_finished：把完成结果送回父级和任务发起者。

这里最值得注意的注释是：

> 这些 Rust contract（Rust 契约）本身不定义 wire protocol（线协议）。

也就是说，Codex 内部多 Agent 协作不是简单等价于“使用某个 A2A 标准协议”。

它先定义 Host 内部的控制语义：成员关系、调用权限、恢复、任务投递、预算和完成通知。不同 Host 可以再决定这些操作怎样跨进程或跨服务运输。

### 子 Agent 本质上仍然是 Thread

Spawn 出来的 Agent 有自己的 Thread ID、Agent Path（Agent 路径）、角色和状态。

它可以从父级 Fork 一部分历史，也可以继承环境、角色指令和共享设置。

所以多 Agent 不是：

```text
一个 Prompt 里写：
“你现在有三个专家”
```

而是 Runtime 真正维护多条 Thread 及其父子关系。

---

## 4. Agent Message 为什么区分 QueueOnly 和 TriggerTurn

多 Agent 通信还有一个很有意思的细节。

`MessageDeliveryMode` 区分：

- `QueueOnly`：只把消息放进目标 Agent 的 mailbox（邮箱），不会唤醒空闲 Agent；
- `TriggerTurn`：如果需要，可以启动目标 Agent 的工作。

为什么需要这个区分？

因为：

> “收到一条信息”和“立刻开始一次新的模型推理”不是同一件事。

如果任何子 Agent 消息都自动触发模型 Turn，多 Agent 系统很容易形成互相唤醒的消息风暴。

这也是生产多 Agent 和 Demo 最大的差异之一：Runtime 必须明确消息的 delivery semantics（投递语义），而不是只有 send_message()。

---

## 5. Code Mode 为什么不是“另一个模型”

Codex 还有 Code Mode。

相关源码：

- `codex-rs/code-mode/`
- `codex-rs/code-mode-runtime/`
- `codex-rs/core/src/tools/code_mode/`

模型可以生成一段受控脚本，由 Code Mode Runtime 执行。脚本内部还能继续调用 nested Tool（嵌套工具）。

但这些嵌套工具并不会绕开前面 Tool Lifecycle 讲过的 Runtime。

源码中的 `submit_nested_tool` 会重新构造内部 `ToolCall`，并通过 `ToolCallRuntime.handle_tool_call_with_source` 进入同一套 Tool Router / Handler 流程，只是 `ToolCallSource` 标记为 Code Mode。

所以：

> **Code Mode 改变的是模型如何组合工具，不是取消 Tool Runtime 的权限和执行边界。**

为什么需要它？

假设任务需要连续做很多小数据处理：

```text
读列表
→ 调 Tool A
→ 过滤结果
→ 调 Tool B
→ 再做本地转换
```

如果每一个微小步骤都重新回模型采样，往返次数和 Context 都会增加。

Code Mode 可以把一部分确定性组合放在受控 Runtime 里执行，只把最终有价值的结果返回模型。

---

## 6. Exec Server 为什么说明 Codex 已经不只是“本机 shell Agent”

Workspace 里还存在完整的：

- `codex-rs/exec-server/`
- `codex-rs/exec-server-protocol/`
- `codex-rs/core/src/environment_selection.rs`

这意味着 Codex 的执行环境不是固定等于“当前 CLI 所在机器”。

Thread 可以有 Environment（环境）选择；工具执行时会带 `TurnEnvironment`，最终把文件系统、工作目录、Permission Profile 和网络能力解析到具体执行环境。

因此成熟 Agent 的工具调用模型更接近：

```text
Tool Intent
        ↓
选择 Environment
        ↓
解析该环境下的 workspace roots / permission
        ↓
在对应 Exec Backend 中执行
```

而不是：

```text
subprocess.run(command)
```

这也是为什么 StepContext 必须保存 Environment snapshot：环境也可能在 Turn 进行过程中变化。

---

## 7. Thread Store、Rollout 和 State DB 分别保存什么

这三者经常被混成“Codex 的数据库”。

源码职责其实很清楚。

### Thread Store：线程存储边界

`codex-rs/thread-store/README.md` 明确把 `ThreadStore` 定义成 Codex Thread 的 storage boundary（存储边界）。

活跃 Thread 一般通过 `LiveThread` 持久化。它负责有序追加 canonical history，并同步 metadata。

### Rollout：顺序历史记录

本地实现会把 canonical history 写成 Rollout JSONL。

它适合保存：

- Response Item；
- Turn lifecycle event；
- Context checkpoint；
- World State；
- Compaction；
- token usage；
-其他恢复所需顺序事实。

### State DB：可查询状态

SQLite State DB 更适合保存需要按条件查询的数据，例如：

- Thread metadata；
- Memory job；
-一些索引和状态。

所以：

```text
Rollout
更像“发生过什么”的顺序事实

State DB
更像“现在可查询什么”的结构化状态
```

两者可以互补。

这也是为什么 Thread Store README 特别强调：raw history append（原始历史追加）本身不应该偷偷推断 metadata。推断逻辑应该在更上层完成，再显式更新 store。

---

## 8. Resume 为什么是“恢复执行状态”，不是“重新显示聊天记录”

Context 篇已经讲过 replacement-history checkpoint。

放到完整产品里，Resume（恢复）还需要恢复更多东西。

`ThreadManager` 和 `Session::record_initial_history` 会区分 New、Resumed、Forked 等初始历史类型。

恢复时不仅重建 ContextManager，还会恢复：

- previous turn settings；
- token usage；
- Context Window identity；
- World State baseline；
- Thread metadata；
-必要的 Multi-Agent / Environment 状态。

这就是为什么“保存 messages 数组”无法实现同等级的 Resume。

真正目标应该是：

> **恢复以后，下一次模型采样的行为条件与中断前保持语义一致。**

可以称为 behavioral resume equivalence（行为恢复等价性）。

这比“UI 里历史消息都显示出来了”严格得多。

---

## 9. 网络断开以后，为什么 Agent 不应该立刻失败

模型请求也有自己的故障生命周期。

源码：

- `codex-rs/core/src/responses_retry.rs`
- `codex-rs/core/src/client.rs`
- `codex-rs/protocol/src/error.rs`

Responses Stream（响应流）如果在完成前断开，Runtime 会先看这个错误是否可重试，再结合 server retry advice（服务端重试建议）或 backoff（退避）等待后重连。

Retry（重试）有预算，不能无限循环。

如果 WebSocket（长连接）连续失败，满足条件时可以 fallback（降级）到 HTTP，再继续同一个 Turn。

这一层的关键原则是：

> **传输故障属于 transport layer（传输层），不应该轻易升级成“整个 Agent 任务失败”。**

但这只有在请求可以安全重放时才成立。涉及真实副作用的 Tool Call 则必须由 Tool 层自己保证不会因为模型 stream 重试而被重复执行。

---

## 10. Codex 为什么需要细粒度错误分类

`CodexErrorDetails` 中有很多错误类别，例如：

- ContextWindowExceeded；
- Stream；
- ConnectionFailed；
- RateLimitExceeded；
- ToolCollision；
- Sandbox；
- Interrupted；
- QuotaExceeded；
- InternalAgentDied；
- Fatal。

这些不是为了报错文字更丰富，而是因为不同错误的恢复权不同。

可以用三个例子理解。

### ContextWindowExceeded

这是上下文资源问题。更合理的方向是 Compaction / 新 Context Window，而不是盲目网络重试。

### Sandbox（沙箱）Denied（拒绝）

这是执行权限问题。Runtime 需要判断 Policy 是否允许更高权限；允许时才请求 Approval 或有限升级。

### ConnectionFailed

这是 transport 问题。可以在 retry budget 内重新连接，必要时换 HTTP。

成熟 Agent 的恢复逻辑应该先问：

> **这是谁的失败？这一层有没有权力修？**

而不是捕获所有 Exception 然后统一 retry。

---

## 11. Rollout Trace 为什么和普通日志不一样

最值得读的诊断文档之一是：

- `codex-rs/rollout-trace/README.md`

它自己总结的设计思想是：

> **observe first, interpret later —— 先记录，再解释。**

Runtime 在线执行时，只忠实记录原始事件和大 payload 的引用；离线 reducer（归约器）再把这些证据解释成 semantic graph（语义图）。

为什么不能在线直接构造最终图？

因为复杂 Agent 中有很多异步时序。

例如一个 Code Mode nested Tool 的 runtime start（运行开始）事件，可能先于包含该 Tool Call 的模型 response item 到达。如果在线 recorder 一看到事件就强行认定关系，容易连错。

所以 Trace 先保存：

- inference request / response；
- Tool dispatch；
- Code Cell；
- Terminal Operation；
- Compaction；
- Multi-Agent spawn / message / result；
-原始 payload。

离线再建立：

```text
ConversationItem
InferenceCall
ToolCall
CodeCell
TerminalOperation
Compaction
AgentThread
InteractionEdge
```

这比一条“tool failed”日志丰富得多。

---

## 12. 为什么 Trace 还要区分“模型看见的”和“Runtime 实际发生的”

这是调试 Agent 时最容易混乱的地方。

Code Mode 内部可能调用了很多 nested Tool，但模型可见 transcript（对话记录）里未必逐条出现这些底层 JSON。

同样，Terminal Runtime（终端运行时）可能执行了很多细节，但模型最终只看到经过整理的 Tool Result。

因此 Rollout Trace 明确区分：

```text
ConversationItem
= 真正进入模型请求 / 响应的内容

Runtime Objects
= Tool、Terminal、Code Mode 等真实执行对象
```

然后用 InteractionEdge（交互边）连接它们。

所以遇到 Bad Case 时可以问：

> Tool 明明执行成功了，模型为什么还不知道？

Trace 能帮助判断：

-执行本身是否发生；
-结果是否被 Runtime 接受；
-是否转成 model-visible output；
-是否进入下一次 inference request。

这比只看终端日志有效得多。

---

## 13. 多 Agent 的 Trace 为什么共享一个根证据图

Spawned child agent（被创建的子 Agent）并不是完全独立的产品会话。

Rollout Trace 会让子 Thread 继承 root trace writer（根追踪写入器），最终一个 trace bundle（追踪包）里可以同时看到父 Thread 和子 Thread。

于是 reducer 能恢复：

```text
root spawn_agent
        ↓
child 收到任务
        ↓
child 自己的模型与 Tool
        ↓
child 产出结果
        ↓
结果通知 root
```

这对于分析：

> “父 Agent 为什么最后拿到了这条错误信息？”

非常关键。

如果每个 Agent 只有独立日志，却没有跨 Thread interaction edge，就很难还原信息流。

---

## 14. 大 Context、大 Tool、大 Skill、大 Memory 应该怎样扩展

Codex 当前源码给出的方向非常一致：**不要因为容量变大，就取消分层和预算。**

### Context 很大

仍然做：

- stable prefix（稳定前缀）；
- World State diff；
- Compaction；
- checkpoint；
- cache-friendly append。

因为大 Context 仍然有延迟、成本、旧信息污染和恢复代价。

### Tool 很多

做：

```text
完整 Registry
→ Policy / Environment 筛选
→ Deferred
→ tool_search
→ 小候选集
→ 再加载 schema
```

如果真的达到数万 Tool，可以继续升级 discovery（发现）层，例如 namespace 分层、hybrid retrieval（混合检索）或 learning-to-rank（学习排序），而不是倒退回“全部展开”。

### Skill 很多

继续：

```text
元数据目录
→ 预算控制
→ 选择具体 Skill
→ 读取 SKILL.md
→ 按需读取 references / scripts
```

### Memory 很多

继续：

```text
原始历史越来越多
→ 提取与整理更严格
→ global summary 仍然有硬大小上限
→ 只有需要时追更深证据
```

这四条看似不同，其实都在贯彻同一个系统原则：

> **模型只应该看当前决策真正需要的信息，而不是 Host 已经拥有的全部信息。**

---

## 15. 源码 Tests 和 Metrics 能证明什么

Codex 没有一个单独文件叫“eval.py”就代表全部评测。

验证分散在不同层。

### Unit / Contract Test

每个 crate 会测试自己的局部契约，例如 Tool schema、Memory read、Sandbox、Protocol。

它们能证明：

> 这个实现满足我们写下的局部规则。

### Core Integration Test

`codex-rs/core/tests/suite/` 会跨模块验证真实流程。

例如 WebSocket fallback、MCP、Compaction、Sandbox、Multi-Agent 等。

### Model-visible Snapshot Test

很多 scenario snapshot（场景快照）直接检查模型请求里真正出现了什么。

这对 Context 很重要，因为单测某个 fragment “render 成功”，并不能证明它最后真的出现在正确位置。

### Metrics / Analytics

Memory、Skill、Tool、Compaction 都有结构化指标。

它们能回答：

- 某机制有没有发生；
- 发生了多少次；
- 花了多少时间 / Token；
- 哪类失败最多。

### Rollout Trace

当 metric 只告诉你“失败率升高”，Trace 帮你解释具体一条失败的因果链。

但这些东西加起来，仍然不自动等于“Codex 任务成功率变高”。

---

## 16. 真正的 Agent Eval 还需要任务级 Outcome

源码测试更擅长验证 Runtime contract（运行时契约）。

产品效果还要建立 Evaluation Harness（评测设施），让 Codex 在可重复环境里完成真实任务，再检查 Environment Outcome（环境最终结果）。

例如代码修复任务应该验证：

- 测试是否真的通过；
-目标 bug 是否消失；
-有没有破坏公开 API；
-有没有无关改动。

而不是只看 Codex 最后说：

> “修复完成。”

因此一个完整 Eval 可以分四层。

### Outcome：最后任务到底成没成功

这是最重要的一层。

### Process：过程是否退化

例如虽然成功，但重复读同一文件 20 次，或者无意义调用大量 Tool。

### Safety：成功是不是靠越权换来的

例如有没有绕过 Approval、写到工作区外、违反网络策略。

### Resource：成功的代价是否可接受

包括 Token、latency（延迟）、模型调用次数、Tool 调用次数、Compaction 次数等。

不能把这四类压成一个总分。

---

## 17. Context、Memory、Tool 分别应该怎样做效果评测

### Context

最关键的是“长时间以后关键约束是否仍然存在”。

可以构造：

```text
开头：
“不能修改公开 API”

→ 多轮 Tool
→ 触发 Compaction
→ 退出进程
→ Resume
→ 继续任务
```

最后检查 Agent 是否仍然遵守约束。

这同时测试了 Context retention（约束保留）、Compaction 和 Resume。

### Memory

不能只测“召回率”。

还要测：

- 一次性要求有没有被错记成永久偏好；
- 用户 correction 后旧事实是否复活；
- Memory ON / OFF 是否真的改善任务；
-过期 Memory 是否造成错误决策。

### Tool

至少分别测：

- Discovery：相关 Tool 能不能被搜到；
- Selection：模型有没有选对；
- Arguments：参数是否合法；
- Safety：权限是否正确；
- Execution：取消、超时、并发是否正确；
- Result Reuse：模型拿到结果以后有没有正确使用。

如果只统计“Tool 调用成功率”，会把很多选择错误和安全问题掩盖掉。

---

## 18. 用一个 Bad Case 看怎样从 Trace 改系统

假设线上发现：

> Codex 连续三次运行同一个失败测试命令，最后还说任务完成。

先不要马上改 Prompt。

Rollout Trace 可以还原：

```text
Inference #1
→ exec_command
→ exit 1

Inference #2
→ exec_command
→ exit 1

Inference #3
→ exec_command
→ exit 1

Inference #4
→ final answer: done
```

然后继续问：

- Tool Result 有没有真的进入模型请求？
- exit code 是否在结果截断时丢了？
-模型是不是正确看到但错误理解？
- Planning / stopping policy 是否允许重复无效动作？
-最终 grader 是否只看回答文字，没有检查测试状态？

只有确认根因以后，才知道应该改：

- Tool Result formatting；
- Context assembly；
- Runtime stop condition；
-模型指令；
-还是 Eval grader。

修复以后，把这条线上 Bad Case 和它的变体加入回归集。

这样才形成真正的数据闭环：

```text
线上失败
→ Trace
→ 根因定位
→ 针对性修改
→ Regression Eval
→ 再上线
```

---

## 19. Codex 源码里最值得迁移的系统思想

把所有实现细节拿掉以后，当前源码最值得带走的不是某个 Rust 类型，而是几条边界。

**第一，模型只负责需要语义推理的部分。** 任务理解、代码分析、Memory consolidation、Compaction summary 可以交给模型。

**第二，必须一致的部分留在 Runtime。** 权限、Tool 路由、Job lease、Context checkpoint、retry count、call/result pairing、Thread identity 不能让模型自由决定。

**第三，长期系统一定要增量化。** Context 用 diff，Memory 用 workspace diff，Tool 用 deferred discovery，Resume 用 checkpoint + suffix。

**第四，模型可见信息必须有预算。** Tool spec、Skill metadata、Memory summary、Tool Result 都不能无限增长。

**第五，执行事实和模型视图必须分开记录。** Runtime 做了什么，不等于模型看见了什么；Rollout Trace 正是为这条边界服务。

这五点是从 Codex 当前源码里抽出来的工程结论，而不是先有教材框架再把源码往里面填。

---

## 20. 源码锚点

如果要自己核验全局结构，建议按下面顺序：

1. [`codex-rs/Cargo.toml`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/Cargo.toml)：完整 workspace，先确认产品真实包含哪些 crate。
2. [`cli/src/main.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/cli/src/main.rs)：产品入口和命令面。
3. [`app-server/src/extensions.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/app-server/src/extensions.rs)：Memory、Skills、MCP、Goal、Guardian 等怎样正式装进 Runtime。
4. [`ext/extension-api/src/lib.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/ext/extension-api/src/lib.rs)：扩展可以参与哪些生命周期。
5. [`core/src/thread_manager.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/thread_manager.rs)：Thread 创建、恢复、Fork 与运行实例。
6. [`core/src/state/service.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/state/service.rs)：一条 Session 真正持有哪些长期服务。
7. [`core/src/agent/api.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/agent/api.rs) 与 [`tools/handlers/multi_agents_v2.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/tools/handlers/multi_agents_v2.rs)：多 Agent 控制语义和 Tool 表面。
8. [`core/src/tools/code_mode/`](https://github.com/openai/codex/tree/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/tools/code_mode)：Code Mode 怎样继续走统一 Tool Runtime。
9. [`exec-server/`](https://github.com/openai/codex/tree/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/exec-server)：执行环境与远端 / 本地执行边界。
10. [`thread-store/README.md`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/thread-store/README.md)：Thread 持久化职责。
11. [`protocol/src/error.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/protocol/src/error.rs) 与 [`core/src/responses_retry.rs`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/src/responses_retry.rs)：错误分类与模型请求恢复。
12. [`rollout-trace/README.md`](https://github.com/openai/codex/blob/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/rollout-trace/README.md)：完整诊断证据模型。
13. [`core/tests/suite/`](https://github.com/openai/codex/tree/75db67bbc6a18200b52698c8870adaedd7746dea/codex-rs/core/tests/suite)：跨模块集成验证。

回到：[Codex 系统总览](README.md)
