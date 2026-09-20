# 01. Codex Context Lifecycle｜从输入、Prompt 编排到 Compaction、Cache 与 Resume

[← Codex 总览](README.md) · [Memory →](02-memory-lifecycle.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

这一篇只追一个对象：

> **某一条信息怎样进入 Codex，什么时候成为模型可见 Context，怎样随着 Tool Loop 增长，达到边界后怎样压缩，最后又怎样被持久化、恢复和继续使用？**

先给完整链路：

```text
Client / User Input
↓
Submission / TurnInput
↓
Turn 前置处理
  Guardian / hooks / pending input
  explicit plugin mentions
  required MCP servers
  pre-turn compaction
↓
Capture StepContext
  model + config + permissions + env + tool view
↓
Build / diff WorldState
↓
Context contributors
  developer policy / capabilities
  memory / skills / plugins / environment / model switch ...
↓
Record user input + injected items
↓
ContextManager canonical history
↓
normalize / truncate / for_prompt
↓
Prompt
  base_instructions
  + input/history
  + current model-visible tools
  + output schema / parallel setting
↓
ModelClientSession
  prompt_cache_key
  previous_response_id / WS incremental continuation
↓
Response stream
  assistant output / reasoning / tool calls
↓
Tool result becomes canonical history
↓
next Step / next sampling request
↓
token accounting
↓
threshold / hard limit
↓
local compaction / remote compaction / new token-budget window
↓
replacement_history checkpoint
↓
ThreadStore / rollout persistence
↓
resume / fork: newest valid checkpoint + surviving suffix replay
```

这是一条连续生命周期，不是“Prompt、Cache、Compaction 三个互不相关的功能”。

---

## 1. Context 在 Codex 里不是一个字符串

Codex 同时维护几类不同对象：

```text
Session State
程序内部长期状态

ContextManager / History
已进入 canonical conversation 的模型相关历史

WorldState
当前环境与运行条件的结构化快照

TurnContext / StepContext
这一次 Turn / Step 的配置与执行快照

BaseInstructions
请求级基础指令

ToolRouter.model_visible_specs()
本次请求可见的工具能力

Prompt
真正发送给模型的请求视图
```

因此不能把：

```text
context = system prompt + chat history
```

当成 Codex 的实现。

更准确的是：

> **Context 是 Session 中多种状态经过规则化投影后形成的“当前模型可见视图”。**

这也是为什么 Codex 源码把 Context、History、World State、Tool Specs、Memory、Persistence 分成不同 crate / module。

---

## 2. 生命周期第一步：用户输入怎样进入 Runtime

客户端不是直接调用 `run_turn`。

`SessionIo` 接受 submission；对 turn input，Runtime 使用带顺序语义的 `submit_turn_input`，把请求交给 Session Loop。

源码边界：

- `codex-rs/core/src/session/mod.rs`
- `SessionIo::submit`
- `SessionIo::submit_turn_input`
- submission loop
- `codex-rs/core/src/session/turn.rs::run_turn`

因此外部输入先成为**程序事件**，再成为模型输入。

这一层的意义是：

```text
客户端输入
≠
立刻写进 Prompt
```

在真正采样前，还要经过：

- turn routing；
- active turn / input queue；
- hook；
- Guardian；
- plugin / MCP dependency 处理；
- pre-turn compaction；
- step context capture。

---

## 3. Codex 的“意图理解”其实有两层

用户输入进入 `run_turn` 后，一部分意图会在**模型调用之前**被确定。

源码会从用户输入里收集：

- 显式 plugin mention；
- 显式 app / connector 相关引用；
- 需要启动的 MCP server；
- 显式 Skill invocation；
- turn settings / environment 等结构化要求。

这类意图不是让大模型自由猜：

```text
用户明确 @ 某能力
→ Runtime 解析
→ required_plugins / required_servers
→ StepContext 捕获前准备对应能力
```

另一部分开放语义，例如：

> “修掉这个测试失败，并尽量不要改 API。”

仍然由模型在完整 Context 中理解。

所以成熟 Agent 的 Intent 不一定是一个单独的“Intent Classifier”：

```text
确定性语义
显式引用、协议字段、权限、环境选择
→ Runtime 先解析

开放任务语义
目标、策略、代码理解、下一步动作
→ 交给模型结合完整 Context 推理
```

这比“先做一次统一意图分类，再把标签交给 Agent”更贴近 Codex 当前源码。

---

## 4. Turn 开始前，为什么先检查 Compaction

`run_turn` 一开始就可能执行 pre-sampling compaction，而且发生在新用户输入真正写入历史之前。

原因非常重要：

假设旧 Context 已经接近阈值：

```text
旧历史 115k
+ 新用户输入 8k
+ 新环境差异 4k
+ Tool / Skill 变化
→ 可能一开始就越界
```

如果先把新输入写死，再发现 Context 爆掉，恢复路径会复杂得多。

所以 Codex 的逻辑近似：

```text
Turn start
↓
检查旧窗口是否需要预压缩
↓
成功
  → 再处理新输入
失败
  → 仍要确保新输入被保留 / 正确发出错误
```

源码甚至专门注释：

> pre-turn compaction 在新输入记录之前运行，所以失败路径必须保护输入。

这是一个典型 Production 细节：**Compaction 不只是 Token 优化，还参与事务边界。**

---

## 5. StepContext：为什么一个 Turn 里还需要 Step

一个 Turn 可能有：

```text
sample #1
→ tool A
→ tool result
→ 用户 steer
→ MCP server ready
→ sample #2
→ tool B
→ ...
```

如果每次工具执行都去读“现在最新的全局配置”，就会出现时间错位：

```text
模型在 Step 1 看见 Tool A schema v1
↓
配置在 Step 2 更新
↓
Step 1 产生的 Tool A call 延迟执行
↓
错误使用 schema / permission v2
```

Codex 通过 `StepContext` 固化一次采样周围需要保持一致的：

- model settings；
- permission profile；
- environment selection；
- tool router；
- provider / context-window 信息；
- turn snapshot。

ToolCallRuntime 会保留产生 Tool Call 的 StepContext。

所以：

> **Step 是模型可见能力与真实执行能力的一致性边界。**

---

## 6. WorldState：Context 不应该每轮全部重发

Codex 有 `WorldState`，并且同时维护：

```text
full snapshot
+
subsequent merge/diff
```

`record_context_updates_and_set_reference_context_item` 的核心逻辑是：

### 第一次 / baseline 丢失

```text
reference_context_item == None
↓
build full WorldState
↓
build full initial context
↓
set world-state baseline
↓
record model-visible items
↓
persist full WorldState snapshot
↓
persist TurnContextItem
↓
set reference_context_item
```

### 稳态 Turn

```text
已有 reference baseline
↓
重新构造当前 WorldState
↓
与 baseline 比较
↓
只发 model-visible diff
↓
只持久化需要的 state patch
```

这与 Codex 根目录 `AGENTS.md` 的 Context 规则完全一致：

> 正常路径应该增量构建 Context，避免不断重写过去内容。

为什么？

因为这样同时改善：

- Token 成本；
- Prompt Cache 稳定性；
- 可解释性；
- Resume 的状态重放；
- “什么时候发生变化”的可追踪性。

---

## 7. 初始 Context 到底由哪些东西组成

`Session::build_initial_context_with_world_state` 是最值得读的函数之一。

它不是写死：

```text
system + developer + user
```

而是收集多种 typed fragments。

当前源码可见的来源包括：

### 7.1 Developer Instructions

Turn 自身的 developer instructions。

Guardian 子 Agent 有特殊处理：Guardian policy 会保持为独立顶层 developer message，便于审计，不和普通 developer bundle 混在一起。

### 7.2 Extension Thread Context

各 Extension 可以通过 `ContextContributor` 提供：

- `DeveloperPolicy`
- `DeveloperCapabilities`
- `ContextWindow`

不同 slot 决定 fragment 最终怎样进入模型可见输入。

Memory Extension 就通过这里把 memory summary 的 developer instructions 注入。

### 7.3 Extension Turn Context

Extension 还可以只针对当前 Turn 贡献 Context。

这说明 Codex 的 Prompt Architecture 不是一个中央巨大模板，而是：

```text
稳定 Core
+
受约束的 Extension contribution points
```

### 7.4 WorldState

WorldState 渲染出来的 fragment 可能包含：

- model switch instructions；
- managed developer instructions；
- multi-agent mode；
- role instructions；
- environment / permission / runtime 状态；
- 其他 model-visible world state。

### 7.5 Recommended Plugins

推荐插件可以作为 contextual user section 进入初始 Context。

### 7.6 Token Budget Context

启用 Token Budget 时，会携带当前 context-window identity 与可选 hints。

它甚至可能通过 notes MCP bridge 获取 thread hint，再组合到 Context Window 提示中。

这体现出一个非常重要的设计：

> **Context Window 本身也有运行时状态，不只是模型 API 的一个整数参数。**

---

## 8. 为什么要 typed Context Fragment

Codex 根 `AGENTS.md` 明确要求新增 model-context 注入最好使用：

`ContextualUserFragment`

源码里也确实把各种 Context 做成独立类型：

```text
base_instructions
developer_instructions
user_instructions
environment_context
environments_instructions
compaction_summary
current_time_reminder
token_budget_context
subagent_notification
guardian_*
world_state/*
...
```

Typed Fragment 的价值不是 Rust 代码更“优雅”，而是能附带：

- role；
- marker；
- content kind；
- stable identity；
- rendering policy；
- merge / replace 语义；
- telemetry / test 能力。

如果所有东西只是：

```rust
prompt.push_str(...)
```

就很难回答：

- 这段是谁加的？
- 应该覆盖还是追加？
- 什么时候需要刷新？
- 能不能被 diff？
- 它是不是 cache-stable？
- 它有多大？
- Resume 时该不该重建？

---

## 9. Prompt 的物理结构：Base Instructions 和 input/history 不是一层

Codex 最终模型请求可以抽象为：

```text
Prompt {
    base_instructions,
    input,
    tools,
    parallel_tool_calls,
    output_schema,
    ...
}
```

这里：

### Base Instructions

通过 `get_prompt_base_instructions` 取得。

它可以根据配置对请求副本做变换，但不会因此修改已经持久化或被 fork 继承的原始 instructions。

这是典型的：

```text
durable source state
≠
request-time rendered view
```

### input

来自 ContextManager 的 canonical history 经 normalize / truncate / provider adaptation 后得到。

### tools

来自当前 Step 的 `ToolRouter.model_visible_specs()`。

工具 schema 不一定以聊天文本的形式存在，但仍是模型请求 Context 的一部分，也会影响：

- token / request 大小；
- tool-selection ambiguity；
- prompt cache compatibility。

---

## 10. ContextManager：Canonical History 不是“所有事件日志”

Codex 的 ContextManager 管理模型对话历史。

它和 Rollout / Trace 不同：

```text
ContextManager
= 模型相关 canonical history

ThreadStore / Rollout
= 可恢复的持久化事实

Rollout Trace
= 诊断用原始运行证据
```

正常路径通过 record 方法增量追加。

`replace_annotated` 不是普通 Turn 的常规操作，主要用于：

- compaction replacement；
- reconstruction；
- reset 类边界。

这保证了：

> 正常历史尽量 append-only；只有明确的 Context Window 边界才重建历史基线。

---

## 11. Tool Result 怎样重新进入 Context

一次典型链：

```text
Prompt N
↓
model: function_call(call_id, name, args)
↓
ToolRouter 解析
↓
ToolCallRuntime 执行
↓
ResponseInputItem::FunctionCallOutput
↓
写入 canonical history
↓
Prompt N+1
↓
模型同时看到：
  原始 call
  对应 call_id 的 output
```

这也是为什么 Context normalization 必须处理 Tool Pairing。

如果历史里出现：

```text
有 tool call
但 output 丢了
```

下一次请求可能变成协议非法或模型难以理解的结构。

Codex 的 `context_manager/normalize.rs` 会修复这类结构：

- 为缺失的 function/tool-search/custom output 生成合成 aborted output；
- 删除 orphan output；
- 对当前模型不支持的 image / audio 做清理；
- 保证请求历史在协议上可消费。

更有意思的是，合成 ID 使用稳定的确定性策略，避免一次 Retry / Resume 后 ID 随机变化导致 Prompt Cache 失效。

---

## 12. Prompt Cache 不是“缓存 Agent 答案”

Codex 的 Prompt Cache 设计至少有三层要分开。

### 12.1 `prompt_cache_key`

ModelClient 会给请求一个稳定 cache-affinity key。

一般根 Session 使用 session identity；内部 Session 在有 parent thread 时，可以用：

```text
{internal_source}:{parent_thread_id}
```

让相关内部工作具有合适的缓存亲和性。

如果调用方明确提供 override，则使用 override。

### 12.2 Stable Prefix

Prompt Cache 能否真正命中，不只看 key。

如果前缀内容一直抖动：

```text
同一个 cache key
+
每次早期 Context 都变
→ 仍然很差
```

因此 Codex 的 Context 设计刻意：

- 初始 Context 稳定；
- 后续尽量 append；
- WorldState 用 diff；
- 自动注入有界；
- synthetic IDs 稳定；
- Tool / Skill 暴露受预算限制。

### 12.3 `previous_response_id` / WebSocket Incremental Continuation

`ModelClientSession` 是 **Turn-scoped**。

它缓存：

- WebSocket connection；
- previous full request；
- previous response；
- sticky `x-codex-turn-state`。

只有当前请求是前一请求的兼容增量时，才允许复用增量请求路径。

源码对兼容条件逐字段比较，包括：

- model；
- instructions；
- tools；
- tool choice；
- parallel setting；
- reasoning；
- service tier；
- prompt_cache_key；
- output text settings 等。

这说明：

> **Prompt Cache、previous response continuation、WS transport reuse 是相关但不同的机制。**

不能统一叫“缓存”。

---

## 13. 为什么 `ModelClientSession` 必须按 Turn 创建

源码明确写明：

> `ModelClientSession` 应该每个 Turn 新建。

因为它持有 `x-codex-turn-state` sticky routing token。

这个 token：

- 同一 Turn 的 retries / continuation 要继续发送；
- 不能跨 Turn 复用；
- auth owner 改变时也必须清掉。

如果错误跨 Turn 复用：

```text
Turn A routing state
↓
误带到 Turn B
↓
违反 client/server contract
↓
产生路由 bug
```

因此：

```text
ModelClient          Session-scoped
ModelClientSession   Turn-scoped
StepContext          Step-scoped
```

是三个清楚的时序层。

---

## 14. Token 计数不是一个“128k - 当前 tokens”

`session/context_window.rs` 会区分：

- active context tokens；
- model effective context window；
- auto-compact token limit；
- limit scope；
- full-context hard limit；
- body-after-prefix token count；
- server prefill baseline；
- buffered fallback limit；
- turn-end compaction threshold。

尤其 `AutoCompactTokenLimitScope` 可以区分：

```text
Total
整个请求范围

BodyAfterPrefix
只看稳定前缀之后的可增长 body
```

这非常重要。

如果稳定前缀已经很大，而 Compaction 的目标主要是压历史 body，那么按 total token 机械触发可能过早。

所以成熟 Context Budget 要问：

> **究竟预算哪一段？哪些部分可压缩？哪些稳定前缀必须保留？**

---

## 15. Codex 有三类 Compaction 路径

### 15.1 Local summarization compaction

`core/src/compact.rs`

近似链：

```text
clone current history
↓
加入 compact/summarization instruction
↓
发起模型请求
↓
得到 summary
↓
收集需要保留的用户消息 / retained context
↓
build_compacted_history
↓
形成 replacement_history
↓
替换 live ContextManager
↓
persist CompactedItem
```

关键不是 summary 文本，而是：

> **Compaction 要产出一个可作为未来恢复基线的 replacement history。**

### 15.2 Remote Compaction V2

Provider 支持时，可以走 Responses remote compaction。

它仍然接入同一套：

- trigger；
- reason；
- phase；
- analytics；
- pre/post compact lifecycle；
- Context replacement。

实现位置不同，但生命周期没有分裂。

### 15.3 Token-Budget new context window

`compact_token_budget.rs`

这个路径甚至不一定做摘要。

它可以：

```text
达到 budget
↓
开启新的 Context Window
↓
重新注入 full initial context
↓
重新建立 baseline
```

所以“Context Compression = 让模型总结历史”并不成立。

更准确：

> **Compaction 是 Context Window 迁移协议；摘要只是其中一种 replacement 策略。**

---

## 16. Pre-turn、Mid-turn、Post-turn Compaction 为什么语义不同

源码里可以看到不同注入策略。

### Pre-turn / Manual

新的用户消息还没进入本轮，压缩后下一个正常 Turn 会重新注入所需 Context。

因此通常：

`InitialContextInjection::DoNotInject`

### Mid-turn

当前用户任务已经在执行中，Tool Loop 还要继续。

压缩后模型必须立刻理解：

- 当前用户消息；
- 当前任务；
- 最新 runtime context。

因此 initial Context 要在正确位置重新插入，例如：

`BeforeLastUserMessage`

### Post-turn

如果 Turn 已经完成，可以在成功之后做压缩。

源码特别避免：

> Compaction 请求失败，却已经污染 live/persisted history。

所以 replacement 的 commit 时机本身也是一致性问题。

---

## 17. Compaction 为什么需要事件和 Analytics

Codex 对 compaction 记录的维度包括：

- trigger；
- reason；
- implementation；
- phase；
- strategy；
- status；
- error kind。

这让线上问题可以回答：

```text
为什么这次发生 compact？
是用户手动还是 ContextLimit？
在哪个 phase？
走 Local 还是 Remote？
成功、失败还是被中断？
失败属于哪种错误？
```

只记录“执行过 compact=true”不足以调试 Production Agent。

---

## 18. Compaction 和 Resume 怎样闭环

ThreadStore / rollout 会保存 `CompactedItem`。

现代路径里最关键的字段之一：

`replacement_history`

恢复时 `rollout_reconstruction.rs` 不会傻瓜式从第一条历史一直 replay。

它反向扫描：

```text
最新 rollout
↑
寻找最新仍然 surviving 的 replacement-history checkpoint
↑
同时寻找恢复所需的 TurnContext / WorldState / settings
```

一旦找到：

```text
replacement_history = 完整新基线
+
checkpoint 之后 surviving suffix
```

更老的数据不再影响模型历史重建。

然后再按时间正序 replay suffix。

因此长 Session 的恢复复杂度不必永远正比于“从创建以来全部历史长度”。

---

## 19. Fork、Rollback、WorldState 为什么使恢复更难

恢复不能只找最后一次 compaction。

还要处理：

### Rollback

语义是：

```text
删除最新 N 个真实 user turns
```

因此反向扫描时必须知道哪些 segment 真正包含 user boundary。

### Fork

新 Thread 可能只继承父 Thread 的某个截止点。

不能错误拿到 cutoff 之后的父状态。

### WorldState

WorldState 有：

```text
full snapshot
+
merge patches
```

Compaction 会使旧 baseline 失效。

因此 reconstruction 还要恢复：

- latest surviving baseline；
- 后续 patches；
- reference Context Item；
- context-window IDs；
- previous turn settings。

这说明：

> **Checkpoint/Resume 的本质是恢复“未来继续执行所需的最小一致状态”，不只是恢复聊天文本。**

---

## 20. ThreadStore 和 ContextManager 的边界

`codex-thread-store` 明确是 Codex Thread 的 storage boundary。

其中：

- `append_items` 保存 canonical history；
- metadata 更新走独立 API；
- active session 推荐通过 `LiveThread`；
- LocalThreadStore 使用 rollout JSONL；
- queryable metadata 可进入 SQLite state DB。

ContextManager 是运行时模型历史。

所以：

```text
record in memory
↓
persist canonical rollout item
↓
未来 resume 时 reconstruction
↓
恢复 ContextManager
```

这比“每轮直接 dump 一个完整 messages.json”更适合长期 Agent。

---

## 21. Context 的硬上限原则

Codex 根 `AGENTS.md` 对 model context 的源码开发规则非常值得背下来：

1. 普通流不要重写历史，应增量追加。
2. 不要频繁改变 Context，避免 Prompt Cache miss。
3. 自动注入内容必须有硬上限。
4. 单一 model-context item 必须受限制。
5. 大体积新 Context 项需要额外审查。
6. 新 Context fragment 应 typed。
7. Integration Test 要验证实际模型可见 payload。

这些规则在真实实现中的映射：

| 原则 | 源码机制 |
|---|---|
| 增量 | WorldState diff、history append |
| Cache 稳定 | stable prefix、stable IDs、incremental WS |
| 硬上限 | Skill budget、MCP spec budget、Memory summary cap |
| typed | `ContextualUserFragment`、`PromptFragment` |
| 大历史 | compaction + replacement checkpoint |
| 可测试 | prompt-cache / AGENTS / compaction / resume tests |

---

## 22. 常见错误路径

### 22.1 Context Window exceeded

处理不能只是返回错误。

Codex 会根据 phase / feature：

- preemptive compact；
- ContextLimit compact；
- Token Budget 新窗口；
- 必要时重试当前输入；
- hard full-window limit 仍会失败。

### 22.2 Compaction 本身失败

必须：

- 保住尚未记录的新用户输入；
- emit lifecycle error；
- 不把失败 replacement 当成功历史。

### 22.3 Tool history 不完整

Normalization 补 aborted result 或删除 orphan output，保持协议一致。

### 22.4 Model switch

新的 model-specific instructions 需要在 full context 重建时正确进入，不能沿用旧模型的隐含状态。

### 22.5 Extension Context 无限增长

Codex 的总体规则要求硬上限；Skills、Memory、MCP 分别实现自己的预算。

---

## 23. 大 Context 场景题：如果是 1M Token Window，还需要 Compaction 吗？

需要。

因为问题不仅是：

```text
会不会超过模型最大长度
```

还包括：

- latency；
- input token cost；
- attention dilution；
- cache invalidation；
- Tool Result 噪声；
- stale state；
-恢复成本；
-安全上下文长期残留。

Codex 当前架构给出的答案不是“窗口大就全部塞进去”，而是：

```text
typed + bounded sources
→ incremental diffs
→ stable prefix
→ budgeted body
→ context-window lifecycle
→ checkpointed compaction
```

Context Window 越大，通常只是阈值改变，不会让生命周期管理消失。

---

## 24. Prompt Cache 场景题：为什么每轮把时间戳放 Prompt 最前面很糟

因为：

```text
stable instruction prefix
↓
每轮最前面插入变化时间
↓
后续全部 token 的前缀身份改变
↓
Prompt Cache 复用空间下降
```

Codex 的 Context 规则强调：

> 变化内容尽量以有界、增量、位置稳定的方式进入，而不是持续改写早期 Context。

需要当前时间时，也应该用受控 typed fragment 和明确更新策略，而不是随便把整个系统 Prompt 重写。

---

## 25. 面试怎么解释 Codex Context Architecture

可以用这条因果链：

```text
Codex 不是每轮重新拼一份巨大 Prompt。
Session 保存 canonical history 和持久状态；
每个 Turn 创建 turn-scoped model session；
每次 sampling 捕获 StepContext，保证模型看到的工具、权限和真实执行一致。
初次 Context 由 developer / extension / world state 等 typed fragments 建立，
后续主要通过 WorldState diff 和历史追加增量更新。
模型请求还单独携带 base instructions 和本 Step 的 tool specs。
随着 Tool Loop，call/result 继续写入 canonical history。
Runtime 持续做 token accounting，到阈值后根据 provider 和 feature
选择 local summary、remote compaction 或开启新 token-budget window。
Compaction 不是只产一段摘要，而是生成 replacement-history checkpoint。
ThreadStore 把 checkpoint 和后续事件持久化；
Resume/Fork 从最新仍有效 checkpoint + suffix 重建，
因此长 Session 不需要永远从头 replay。
整个设计还刻意维持稳定前缀和 prompt_cache_key / previous-response continuation，
让 Context 正确性、成本、恢复和 Cache 命中一起成立。
```

---

## 26. 源码核验入口

固定快照下建议按下面顺序回读：

- [`AGENTS.md`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/AGENTS.md)：model-context 开发约束。
- [`core/src/session/turn.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/turn.rs)：一次 Turn 的完整 loop。
- [`core/src/session/mod.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/mod.rs)：initial context、WorldState diff、history/persistence。
- [`core/src/context/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/context)：typed Context items。
- [`context-fragments/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/context-fragments)：fragment 抽象。
- [`core/src/context_manager/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/context_manager)：history、normalize、updates。
- [`core/src/client.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/client.rs)：Prompt request、cache key、WS continuation。
- [`core/src/session/context_window.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/context_window.rs)：Context Window accounting。
- [`core/src/compact.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/compact.rs)：local compaction。
- [`core/src/compact_remote_v2.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/compact_remote_v2.rs)：remote compaction lifecycle。
- [`core/src/compact_token_budget.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/compact_token_budget.rs)：new context window。
- [`core/src/session/rollout_reconstruction.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/rollout_reconstruction.rs)：Resume / Fork reconstruction。
- [`thread-store/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/thread-store)：持久化边界。

下一篇：[Codex Memory Lifecycle →](02-memory-lifecycle.md)
