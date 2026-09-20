# 04. Codex Engineering & Evaluation｜边界、Failure、规模化、诊断与评测

[← Tool](03-tool-lifecycle.md) · [Codex 总览](README.md) · [成熟产品源码学习](../README.md)

> **源码基线：** openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f

前面三篇分别追了 Context、Memory、Tool。真正进入 Production 以后，它们不会独立运行：

~~~text
用户输入
↓
Session / Turn / Step
↓
Context 编译
↓
模型请求
↓
Tool / Memory / Multi-Agent 行为
↓
权限与执行
↓
新 observation 回到 Context
↓
持续增长
↓
Compaction / Retry / Recovery
↓
Persistence
↓
Trace / Metrics / Tests / Eval
~~~

这一篇回答的是：

> **当 Agent 长时间运行、网络不稳定、上下文不断增长、工具与 Skill 达到大规模、记忆可能过时、权限又必须受控时，Codex 怎样维持系统边界，并且怎样证明这些设计真的有效？**

---

## 1. 先建立 Production 边界图

Codex 的边界不能只画成“LLM + Tools”。

更接近源码的是：

~~~text
Client / App Server / TUI
        │
        ▼
Submission Boundary
        │
        ▼
Thread / Session
  ├─ durable identity
  ├─ ContextManager
  ├─ ThreadStore
  ├─ token / window state
  ├─ extensions
  ├─ MCP runtime
  ├─ permission runtime
  └─ ModelClient
        │
        ▼
Turn
  ├─ user goal
  ├─ turn settings
  ├─ ModelClientSession
  ├─ cancellation
  ├─ required plugins / MCP
  └─ telemetry
        │
        ▼
Step
  ├─ captured model settings
  ├─ world state
  ├─ permission snapshot
  ├─ environment
  └─ ToolRouter
        │
        ├───────────────┐
        ▼               ▼
Model Request       Tool Runtime
        │               │
        └───────┬───────┘
                ▼
       Canonical History
                │
        ┌───────┴────────┐
        ▼                ▼
 Compaction / Window   Persistence
        │                │
        └───────┬────────┘
                ▼
        Resume / Fork
                │
                ▼
      Trace / Analytics / Eval
~~~

每一层都对应不同 Failure Domain。

如果把所有失败统一成：

~~~text
Agent failed
~~~

就无法判断应该：

- retry；
- compact；
- 让模型修参数；
- 请求权限；
- 切 transport；
- 中止 Tool；
- 恢复 Thread；
- 还是直接 fail fast。

---

## 2. Session、Turn、Step、Context Window 是四个不同工程边界

### Session / Thread

负责长期身份、持久化、Memory 接入、当前 history、token state、services。

### Turn

负责一次用户目标推进，并拥有 turn-scoped ModelClientSession、sticky routing state、cancellation 和本轮 telemetry。

### Step

负责一次模型 sampling 周围的精确执行快照，保证模型看到的 Tool、Permission、Environment 与稍后执行一致。

### Context Window

负责模型可见历史的一个“连续工作窗口”。

它可以因为：

- local compaction；
- remote compaction；
- Token Budget 新窗口；

切换。

这四者不能混成“conversation”。

例如：

~~~text
一个 Session
可以有很多 Turn

一个 Turn
可以有很多 Step

一个 Session
可以跨多个 Context Window

一次 Compaction
可能发生在同一个 Turn 中间
~~~

理解这些边界，是解释 Retry、Cancel、Resume 和 Eval 的前提。

---

## 3. Codex 的错误分类为什么很细

protocol/src/error.rs 中的 CodexErrorDetails 已经把大量错误做了语义分类。

这不是为了 UI 显示漂亮，而是因为不同错误需要不同控制策略。

| 层 | 代表错误 | 更合理的控制动作 |
|---|---|---|
| 用户 / Turn | TurnAborted、Interrupted | 结束当前动作；必要时把中止结果回填，不伪装成功 |
| 预算 | SessionBudgetExceeded | 停止继续消耗共享预算 |
| Context | ContextWindowExceeded | 触发 / 建议 Compaction 或新窗口，而不是普通网络重试 |
| Stream | Stream、ResponseStreamFailed | 在允许范围内 reconnect / retry |
| Rate limit | RateLimitExceeded | 按 server retry delay / backoff |
| Transport | ConnectionFailed、RequestTimeout | retry；满足条件时 WS → HTTP fallback |
| Provider | ServerOverloaded、InternalServerError | 有限重试 / 换路径；不能无限循环 |
| Tool Contract | ToolCollision、InvalidRequest | 修 Registry / request；不是随机 retry |
| Tool Process | Timeout、Spawn、Interrupted | 产生明确 Tool failure / aborted semantics |
| Sandbox | Denied、Timeout、Signal、Landlock / seccomp | 按 policy 决定拒绝、请求批准或有限 escalation |
| Auth / Plan | RefreshTokenFailed、QuotaExceeded、UsageNotIncluded | 不能靠 retry 假装修好 |
| Policy | Cyber / Bio / Misalignment | 按政策终止相应行为 |
| Runtime invariant | InternalAgentDied、Fatal、TokioJoin | fail fast + 诊断，不包装成普通业务失败 |

成熟 Agent 的 Failure Handling 不是：

~~~text
try:
    run()
except:
    retry()
~~~

而是：

> **先判断“失败属于哪一层”，再决定这个层是否拥有恢复权。**

---

## 4. 为什么 UI 错误消息还有 2KB 上限

错误本身也可能非常大：

- server response；
- Tool stderr；
- malformed JSON；
- stack / protocol details。

如果直接把全部错误：

~~~text
进入 UI
进入下一轮 Context
进入 telemetry
~~~

可能造成：

- Context 污染；
- 隐私泄露；
- 日志成本；
- 终端不可读。

Codex 对 UI error message 做有界截断。

这个小细节代表同一个全局原则：

> **任何可能进入用户界面或模型 Context 的自动生成内容都应该有体积边界。**

---

## 5. 模型流中断后怎样 Retry

core/src/responses_retry.rs 把普通 sampling 和 Remote Compaction 的 response retry 逻辑集中起来。

典型链：

~~~text
发送 request
↓
stream 已建立
↓
尚未 response.completed 就断开
↓
CodexErrorDetails::Stream
↓
判断 retry budget
↓
计算 delay
  server advice / backoff
↓
向用户发 Reconnecting 状态
↓
同一个 Turn 重试
~~~

注意：

- Retry 是 Turn 内行为；
- 不会因此创建新的用户 Turn；
- 同一 Turn 的 sticky routing state 仍应保持；
- 不能把一次 stream failure 当成 Tool failure。

---

## 6. Retry 为什么必须有 Budget

如果网络持续坏：

~~~text
retry
→ retry
→ retry
→ ...
~~~

Agent 会：

- 一直占用用户时间；
- 重复消耗请求；
- 产生不可预测成本；
- 掩盖真正 outage。

因此 Codex 有有限 retry budget。

源码还区分某些允许更长 connection retry 的路径，但仍通过 backoff 和专门条件控制。

原则：

> **Retry 不是“失败了再试一次”，而是带错误类别、次数、延迟和作用域的恢复协议。**

---

## 7. WebSocket 失败后为什么可以切 HTTP

ModelClientSession 可以优先走 Responses WebSocket。

当 WS retry 达到条件后，Codex 可以：

~~~text
WebSocket retries exhausted
↓
try_switch_fallback_transport()
↓
HTTP
↓
reset retry counter
↓
继续同一 Turn
~~~

core/tests/suite/websocket_fallback.rs 对这类行为有集成测试。

工程意义：

> **Transport 是实现细节，不应该轻易升级成“Agent 整体任务失败”。**

只要语义请求仍能安全重放，就可以切备用 transport。

---

## 8. 为什么 Retry Advice 必须绑定 Turn

Retry / reconnect 的状态不能泄漏给另一个内部任务。

例如：

~~~text
用户 Turn A
发生 stream retry

同时启动 Guardian Review Turn B
~~~

如果共享一个“最近 retry reason”：

~~~text
B 可能错误继承 A 的网络状态
~~~

源码因此把 retry advice / state 放在合适的 turn-scoped 边界。

这和：

- ModelClientSession turn-scoped；
- StepContext step-scoped；

是同一种时序隔离思想。

---

## 9. Ctrl-C / Cancel 为什么不能等于 Crash

用户中止一个 Tool 或 Turn 是正常交互，不是程序崩溃。

Tool runtime 中：

~~~text
CancellationToken fired
↓
如果调用已经不可安全中断 / 已到 terminal outcome
  → 等待结果
否则
  → abort task
  → 生成 AbortedToolOutput
  → notify abort lifecycle
  → 让 call/output pairing 完整
~~~

顶层还有 Interrupted / TurnAborted 等语义。

因此：

> **Cancellation 也必须产生可恢复的历史。**

如果只 kill future 而不补 Tool Result，下一轮 Context 就会留下 dangling tool call。

---

## 10. Tool Timeout、Sandbox Denied、Model Timeout 为什么不是同一个 Timeout

三者恢复权不同。

### Tool Timeout

某个本地 / 外部动作太久。

可以：

- 返回 Tool failure；
- 模型换策略；
- 用户取消。

### Sandbox Timeout / Denied

说明执行环境限制。

可能：

- 最终拒绝；
- 请求 approval；
- 有限 escalation 到更宽 sandbox。

### Model Request Timeout

模型请求没完成。

可能：

- transport retry；
- fallback。

所以监控上也不能只有：

~~~text
timeout_count
~~~

应该带：

- layer；
- tool / model；
- turn；
- retry count；
- sandbox；
- provider；
- duration。

---

## 11. Compaction Failure 为什么要和普通模型失败分开

Compaction 本身也是一次模型 / runtime 操作。

如果 Compaction 失败：

~~~text
不能：
先替换 live history
→ 再发现 summary request 失败
~~~

否则会丢掉原历史。

正确语义是：

~~~text
准备 compact input
↓
执行 compact
↓
成功得到 replacement
↓
验证 / 构造 CompactedItem
↓
commit live Context replacement
↓
persist checkpoint
~~~

失败则保留旧基线。

Codex analytics 还为 Compaction 单独记录：

- trigger；
- reason；
- implementation；
- phase；
- strategy；
- status；
- Codex error kind。

这使“Agent 失败”可以进一步回答：

> 是 Pre-turn ContextLimit 的 Remote Compaction 失败，还是 Manual Local Compaction 失败？

---

## 12. Persistence 的目标不是“日志尽量多”

ThreadStore 保存的是：

> **未来恢复 Thread 所需要的 canonical history + metadata boundary。**

它与诊断 Trace 的职责不同。

### ThreadStore / Rollout

目标：

- resume；
- fork；
- query thread metadata；
- rebuild Context；
- 恢复 token / settings。

### Rollout Trace

目标：

- 深度诊断；
- 重建 runtime semantic graph；
- 看 inference / tool / terminal / compaction 关系。

不能拿一个替代另一个。

---

## 13. Resume 为什么不是从 JSONL 第一行永远重放

长 Session 可能非常大。

如果每次启动都：

~~~text
从第一条 rollout
→ replay 几十万 event
~~~

冷启动会越来越慢。

Codex reconstruction 会反向寻找：

> **最新仍有效的 replacement-history checkpoint。**

链：

~~~text
从 rollout 尾部向前
↓
找到 surviving CompactedItem
  with replacement_history
↓
该 replacement_history
成为完整 Context base
↓
只 replay 之后的 surviving suffix
~~~

老于 checkpoint 的历史不再需要重新参与模型 Context 重建。

这正是 Compaction 和 Persistence 真正闭环的地方。

---

## 14. 为什么 Rollback / Fork 让恢复变复杂

### Rollback

不是删除最后 N 行。

语义通常是：

> 删除最后 N 个真实用户 Turn 及其派生执行。

所以需要识别 user-turn boundary。

### Fork

Child Thread 只继承 Parent 到某个 cutoff。

因此不能错误恢复 cutoff 之后：

- 新 Tool Result；
- 新 WorldState；
- 新 permission；
- 新 context checkpoint。

### Compaction

会重置 Context baseline。

### WorldState

又有 full snapshot + patches。

因此恢复算法真正重建的是：

~~~text
History base
+
surviving suffix
+
Turn settings
+
WorldState baseline / patches
+
Context-window IDs
+
token information
~~~

而不是“把聊天消息读回来”。

---

## 15. 恢复正确性的核心 Invariant

一个成熟 Agent Resume 至少要满足：

~~~text
Resume 前最后一个可继续执行状态
≈
冷启动重建后的状态
~~~

这里的“≈”不是文本完全一样，而是未来行为所需语义一致：

- 模型看到同样有效的约束；
- tool call / output pairing 完整；
- current environment / permission 合法；
- context window identity 正确；
- compaction summary 没丢关键任务；
- token accounting 可继续；
- fork cutoff 没越界。

这可以称为：

> **Behavioral Resume Equivalence。**

---

## 16. Prompt Cache、Latency、Cost 是同一个工程问题的不同面

假设一个 100k-token Context：

~~~text
每轮都完整重写早期 instructions
↓
Prompt Cache miss
↓
更多 prefill
↓
latency ↑
cost ↑
~~~

所以 Codex 的一些看似“代码洁癖”的设计其实直接影响生产指标：

- append-only normal history；
- WorldState diff；
- stable synthetic IDs；
- bounded Skill catalog；
- Deferred Tool；
- prompt_cache_key；
- previous-response incremental continuation；
- compaction。

优化成本不能只做：

> “少写几个 Prompt 字。”

真正应该优化：

~~~text
stable prefix
+ useful context density
+ bounded dynamic injections
+ fewer unnecessary model round trips
+ less repeated Tool output
+ cache-friendly identity
~~~

---

## 17. 1M Context Window 时代还需要 Context Engineering 吗

需要，而且原因更多。

即使模型支持 1M：

### 成本

1M input 仍然有成本。

### Latency

Prefill 仍然需要时间。

### Attention Dilution

历史越多，不代表模型越能抓住真正约束。

### Stale State

旧 environment / permission / plan 继续存在，会污染当前任务。

### Security

Prompt injection / secret / irrelevant Tool Result 留得更久。

### Recovery

巨量 history 冷启动 / replay 仍然昂贵。

所以 Codex 当前思路依然成立：

~~~text
typed sources
→ hard bounds
→ incremental update
→ stable prefix
→ compactable body
→ checkpointed window lifecycle
~~~

大 Context 主要改变阈值，不取消生命周期管理。

---

## 18. 5 万 Tool 怎么设计

Codex 已经给出可扩展骨架：

~~~text
Full Registry
↓
Tenant / Policy / Capability Filter
↓
Exposure Planning
↓
大多数 Deferred
↓
tool_search
↓
Top-K LoadableToolSpec
↓
模型选择
↓
runtime dispatch
~~~

如果真的上升到 50,000，还应继续演化 discovery：

### 18.1 分层索引

先：

~~~text
domain / server / app / namespace
~~~

再具体 Tool。

### 18.2 Hybrid Retrieval

当前 BM25 可以继续保留 exact / schema-key 能力，再补：

- semantic retrieval；
- query expansion；
- learning-to-rank。

### 18.3 Policy Before Retrieval

无权调用的 Tool 尽量不要进入候选索引。

### 18.4 Stable Catalog Cache

静态 Tool metadata 与动态 Tool 分开版本化，避免每个 Step rebuild 全量索引。

### 18.5 Evaluation

规模化 Tool Search 最终必须测：

- recall@K；
- MRR；
- wrong-tool rate；
- candidate count；
- search latency；
- schema bytes loaded；
- cache rebuild frequency。

“有 Tool Search”本身不是终点。

---

## 19. 1 万 Skill 怎么设计

Codex 当前 Skills 已经采用 Progressive Disclosure：

~~~text
catalog metadata
↓
selected SKILL.md
↓
selected references / scripts / assets
~~~

并对第一层 catalog 做：

- 默认 char budget；
- context-window 百分比预算；
- token hard max；
- description truncation；
- fair allocation；
- omission metrics。

如果 Skill 达到 10,000，合理下一步：

~~~text
full Skill registry
↓
scope / project / authority filter
↓
search / routing
↓
只渲染 top-K metadata
↓
selected SKILL.md
↓
selected resources
~~~

不能因为模型 Context 变大，就把 10,000 份 SKILL.md 全塞进去。

---

## 20. Memory 很多以后怎样避免“越记越差”

Memory 的规模问题本质不是 storage，而是：

> **未来 Context 里的有效信息密度。**

Codex 当前已经有：

- Stage1 bounded discovery；
- Phase2 top-N；
- usage_count；
- last_usage；
- max_unused_days；
- global consolidation；
- summary <10KB；
- progressive search / read；
- correction / pollution / prune。

因此 Memory 规模化的主线是：

~~~text
更多原始历史
≠
更多直接注入

更多历史
→ 更严格 extraction
→ 更强 consolidation
→ 更强 usage feedback
→ 更小高价值 summary
~~~

---

## 21. Observability 要同时看四种证据

### 21.1 Events

Session / Turn / Tool lifecycle event。

用于：

- UI；
- client protocol；
- basic state transitions。

### 21.2 Analytics

结构化事实，例如 Compaction：

- trigger；
- reason；
- implementation；
- phase；
- strategy；
- status；
- error kind。

### 21.3 OTEL / Metrics

例如：

- Tool timing；
- Skill catalog truncation；
- Memory pipeline；
- model token usage；
- request latency。

### 21.4 Rollout Trace

当普通 metrics 不够解释一个复杂 Bad Case 时，保留更完整的本地运行证据。

四种层次不能互相替代。

---

## 22. Rollout Trace 为什么采用“先观察，再解释”

rollout-trace/README.md 的核心思想可以概括成：

> **记录阶段尽量忠实保留事实，语义解释放到离线 reducer。**

为什么？

如果在线 recorder 一边运行一边下结论：

~~~text
看到 tool event
→ 立即认定它属于某 inference / 某 user turn
~~~

后面如果：

- child thread 才出现；
- call id 映射延迟；
- compaction 重建关系；
- terminal operation 异步结束；

早期推断可能错。

所以 Trace：

~~~text
raw event append
↓
payload store
↓
offline reduction
↓
semantic graph
~~~

graph 再建立：

- ConversationItem；
- InferenceCall；
- ToolCall；
- CodeCell；
- TerminalOperation；
- Compaction；
- multi-agent parent/child；
- interaction edges。

这是复杂 Agent 可解释性的一个成熟方向。

---

## 23. Rollout Trace 为什么不能默认全开

Trace bundle 可能包含：

- prompts；
- responses；
- tool inputs / outputs；
- terminal output；
- paths。

这是高敏感诊断数据。

所以当前是：

- 显式 opt-in；
- 本地 bundle；
- 不应让 trace failure 反过来导致 Codex Session 失败。

原则：

> **Observability 是辅助平面，不能成为主执行平面的单点故障。**

---

## 24. Codex 的 Evaluation 不是一个单独 eval 文件夹

源码里的验证证据分布在多层。

### 24.1 Unit / Contract Tests

各 crate 验证：

- Tool contract；
- Memory read/write；
- Context fragments；
- state；
- sandbox；
- protocol。

### 24.2 Core Integration Tests

core/tests/suite 覆盖跨模块行为。

### 24.3 Request / History Snapshot Scenarios

Scenario snapshots 会直接检查：

> 模型真正看到的 Context / Tool shape 是否符合预期。

例如源码中可以看到 Astra 场景覆盖：

- plugin refresh 后不重启仍使用新 Skill / Code Mode MCP；
- disabled Skill 不应进入 Context；
- remote compaction 跨 window；
- Code Mode call timing；
- Tool shape；
- active-turn async question / answer；
- multi-agent catalog 参数。

这比只测试某个 helper return value 更接近 Agent Runtime 的真实契约。

### 24.4 Subsystem Metrics

Memory、Skill、Tool、Compaction 都有自己的 telemetry。

### 24.5 Rollout Trace

用于难以由单一 metric 解释的真实失败。

因此 Codex 的评测证据链可以理解为：

~~~text
unit correctness
→ integration contract
→ model-visible snapshot
→ runtime metrics
→ deep trace
→ task-level outcome eval
~~~

---

## 25. 但“测试都过了”不等于 Agent 真的更好

源码 Tests 主要能证明：

> **实现符合当前定义的 contract。**

例如：

~~~text
ToolSearch 能返回预期 schema
Compaction checkpoint 能重建
Memory summary 合法
WS 能 fallback HTTP
~~~

它们不能自动证明：

> “用户任务成功率更高。”

因此产品级 Eval 还要加：

~~~text
Task Dataset
↓
Agent Runtime
↓
Environment Outcome
↓
Grader
↓
Metrics
↓
Bad Case → Trace
~~~

这与通用课程里 Agent Harness / Eval Harness 的区分完全一致。

---

## 26. Agent 整体 Eval 应该分四层

### 26.1 Outcome

最重要：

- 代码是否真的修改正确；
- tests 是否通过；
- target behavior 是否满足；
- 是否引入 regression；
- 用户 acceptance criteria 是否满足。

不能因为最终回答写：

> “已完成。”

就判 pass。

### 26.2 Process

- 无效 Loop；
- 重复 Tool；
- 无意义重读；
- retry 次数；
- compaction 次数；
- recovery 是否成功。

### 26.3 Safety

- 是否越权；
- 是否绕过 approval；
- sandbox denial 是否正确；
- 网络权限是否符合 policy；
- 是否有 destructive side effect。

### 26.4 Resource

- token；
- cached input；
- latency；
- TTFT；
- tool calls；
- model calls；
- search calls；
- memory reads。

最终报告应同时展示，而不是压成一个总分。

---

## 27. Context 应该怎样 Eval

Context 是最容易“看起来没问题，实际上悄悄退化”的组件。

### 27.1 Constraint Retention

构造长任务：

~~~text
开始时给关键约束
↓
多轮 Tool
↓
触发 Compaction
↓
继续执行
~~~

检查：

- 约束是否仍可见；
- 是否被 summary 错改；
- 是否错误复活旧约束。

### 27.2 Compaction Equivalence

同一任务：

~~~text
A 不触发 compact
B 在指定点 compact
~~~

后续给同一 observation，看行为 / 最终 outcome 是否基本一致。

### 27.3 Resume Equivalence

~~~text
连续运行
vs
中途持久化 → 进程退出 → Resume
~~~

比较：

- 模型可见 Context；
- 下一步 Tool；
- 最终 task outcome；
- permission / environment；
- token/window state。

### 27.4 Cache Stability

跟踪：

- cached_input_tokens；
- prefix mutation；
- WS incremental reuse；
- prompt-cache hit proxy metrics；
- latency。

### 27.5 Context Efficiency

~~~text
task success
/
effective input tokens
~~~

或在 success 不下降条件下比较：

- Context size；
- Tool spec bytes；
- Skill metadata；
- Memory injection；
- latency。

---

## 28. Compaction 应该怎样 Eval

不要只测：

> “summary 是否语句通顺。”

至少要测：

### Retain

- 当前 goal；
- user constraints；
- 关键 file path；
- 已完成动作；
- Tool evidence；
- unresolved blocker；
- permission relevant state。

### Drop

- 重复 observation；
- 过时中间推测；
- 无用日志；
- 已经被新事实覆盖的旧信息。

### Structural Correctness

- Tool call/output pairing；
- Context fragment order；
- resume checkpoint；
- world-state baseline。

### Failure Recovery

Compaction request 失败后：

- 原 history 是否仍完整；
- 新用户输入是否保住；
- 下一次能否重试。

---

## 29. Memory 应该怎样 Eval

Memory 不能只测 Recall。

### 29.1 Extraction

Gold Thread 标注：

~~~text
应该记
不应该记
范围
provenance
是否一次性要求
~~~

指标：

- precision；
- recall；
- overgeneralization；
- unsupported preference；
- secret / injected-content retention。

### 29.2 Consolidation

检查：

- correction wins；
- no resurrection；
- dedup；
- contradiction handling；
- summary size；
- stale removal；
- provenance pointers。

### 29.3 Retrieval

- search recall@K；
- precision@K；
- read escalation rate；
- citation correctness；
- unnecessary deep reads。

### 29.4 Online Utility

Memory ON vs OFF：

- task success；
- 重复询问次数；
- 个性化正确率；
- stale-memory failure；
- token / latency；
- unsafe behavior。

### 29.5 Long-term Maintenance

模拟：

~~~text
偏好 A
→ 使用
→ 改成 B
→ forget
→ 多个旧 Thread 仍含 A
~~~

验证未来 Session 不 resurrect A。

---

## 30. Tool 应该怎样 Eval

### Discovery

- recall@K；
- MRR；
- wrong namespace；
- deferred search latency。

### Selection

- correct tool rate；
- unnecessary tool-search count；
- repeated wrong-tool loop。

### Argument

- schema-valid；
- semantic-valid；
- repair success；
- hook rewrite correctness。

### Permission / Safety

- dangerous tool true-positive；
- benign tool false-positive；
- approval bypass；
- sandbox escape；
- network violation。

### Execution

- success；
- timeout；
- cancel correctness；
- parallel speedup；
- serial conflict rate；
- result truncation usefulness。

### Result Reuse

Tool Result 回填后：

- 模型是否正确解释；
- 是否重复调用同一 Tool；
- 是否把 failure 当 success。

---

## 31. Skill 应该怎样 Eval

Skills 有自己独特的两个问题：

> **能不能发现？发现后能不能正确执行？**

因此分两段。

### Skill Discovery

给任务和大 catalog：

- 正确 Skill 是否在可见 metadata；
- 是否因 budget 被 omit；
- 选中率；
- 错误 Skill 干扰。

### Skill Execution

选中 Skill 后：

- 是否正确读 SKILL.md；
- 是否按需读 references；
- 是否运行 script 而不是把大脚本全塞 Context；
- 是否遵守 Skill 边界。

### Scale

逐步从：

~~~text
100
→ 1,000
→ 10,000 Skills
~~~

观察：

- catalog tokens；
- truncation；
- search latency；
- selection quality；
- task success。

---

## 32. 场景题：Compaction 后 Agent 忘记了“不能改 API”

按 Codex 生命周期排查：

~~~text
1. 原始约束是否真的进入 Context？
2. compact 输入是否包含它？
3. summary 是否保留？
4. build_compacted_history 是否把正确 user context 拼回？
5. mid-turn / pre-turn injection phase 是否正确？
6. replacement_history 是否持久化？
7. Resume 是否选到正确 checkpoint？
8. 新 model switch / world-state update 是否覆盖了它？
~~~

Eval：

- long-context constraint retention；
- compaction A/B；
- resume equivalence。

修复不能只说：

> “把 Prompt 写强一点。”

先定位约束在哪一阶段丢失。

---

## 33. 场景题：Memory 召回很多，但结果变差

排查：

~~~text
Phase1
有没有把一次性要求当永久偏好？

Phase2
有没有把旧 correction 合并错？

Selection
usage_count 高的旧信息是不是已经 stale？

Summary
是不是太长，压过当前目标？

Read
模型是否过度展开历史？

Citation
真正支持 claim 的 thread 是哪个？

Current Task
是否应该重新核验易变化事实？
~~~

Eval 应看：

- overgeneralization；
- correction compliance；
- stale memory failures；
- task-level Memory ON/OFF。

---

## 34. 场景题：一个 Connector Tool 标记为 destructive

不能只在 description 写：

> “危险，请谨慎。”

合理路径：

~~~text
MCP/App Tool metadata
↓
AppToolPolicyEvaluator
  destructive / open-world hints
↓
是否进入 Registry / Exposure
↓
模型产生 call
↓
pre-hook
↓
approval / Guardian
↓
Permission Profile
↓
sandbox / network
↓
execute
~~~

Eval 必须有 adversarial cases：

- injection 诱导；
- 用户未批准；
- 参数被 hook 改写；
- 同名 Tool collision；
- 权限刚刚变化。

---

## 35. 场景题：模型 Stream 在 Tool Call 前断开

如果还没有形成可接受的完整 response / terminal semantic outcome：

~~~text
Stream error
↓
responses_retry
↓
同 Turn retry
↓
必要时 WS → HTTP
~~~

不能：

~~~text
把半个 function call 当成真实 Tool Call 执行
~~~

评测应验证：

- partial stream 不产生幽灵副作用；
- retry 后 call id / history 合法；
- 不会执行两次 destructive action。

---

## 36. 场景题：Tool 执行成功，但结果没写进 History

这是严重一致性问题。

下一次模型可能：

- 不知道 Tool 已执行；
- 再次执行相同副作用；
- 看到 dangling call；
- 错误判断任务状态。

Codex 的应对机制包括：

- canonical call/output pairing；
- context normalization；
- missing output synthesis；
- executed-tool recording；
- Tool result accepted callback；
- Rollout / Trace evidence。

Eval 需要专门故障注入：

~~~text
handler success
↓
在 result-recording 之间注入异常
↓
确认不会静默继续成“未知状态”
~~~

---

## 37. 场景题：Tool schema 在模型看见后刷新了

靠 StepContext。

~~~text
Step 1
模型看到 schema v1
↓
catalog refresh
↓
Step 2 已经 v2
↓
Step 1 call 延迟执行
~~~

Step 1 的 ToolCallRuntime 仍保存产生它的 StepContext / binding。

这防止：

> time-of-advertisement 和 time-of-execution 不一致。

Eval：

- 动态 refresh；
- 延迟 Tool；
- 并行 Steps；
- 确认旧 call 仍按旧 binding 语义处理。

---

## 38. 场景题：Sandbox Denied，是不是直接失败

不一定。

先判断：

~~~text
这是 policy 明确禁止
还是
当前 sandbox 级别不足？
~~~

Codex Orchestrator：

~~~text
Denied
↓
检查 escalation eligibility
↓
需要用户批准？
↓
网络 / filesystem policy 是否允许？
↓
有限 retry with broader execution
~~~

如果 policy Forbidden，就不能通过 retry 绕过。

因此：

> **Retry 权限必须小于 Policy 权限。**

---

## 39. 场景题：Benchmark 很高，上线却表现很差

优先检查 Eval Harness 的覆盖，而不是先怪模型。

### Dataset Shift

离线任务太干净，线上有：

- 大 repo；
- 坏网络；
- 权限；
- 动态 Tool；
- 长 Session；
- stale Memory。

### Outcome Grader 太弱

只看最终文本，不验证：

- 文件；
- tests；
- external state；
- side effects。

### Process 没测

虽然最终成功，但：

- 多 10 倍 Tool；
- 多 5 次 retry；
- 频繁 compact；
- 延迟不可接受。

### Safety 没测

成功是靠越权实现的。

### Harness Drift

Tool schema、sandbox、model version、prompt、Memory baseline 与线上不同。

因此 Product Eval 要保存：

~~~text
task version
runtime version
model
tool catalog
permission profile
context / memory setup
environment snapshot
grader version
~~~

才能解释分数变化。

---

## 40. 怎样用 Rollout Trace 改 Agent

一个 Bad Case：

> Agent 重复三次运行同一个失败命令，最后还声称成功。

不要只看最终回答。

Trace Graph 可重建：

~~~text
InferenceCall #1
→ ToolCall exec
→ TerminalOperation exit=1

InferenceCall #2
→ ToolCall exec
→ TerminalOperation exit=1

InferenceCall #3
→ ToolCall exec
→ TerminalOperation exit=1

InferenceCall #4
→ final answer “done”
~~~

然后把问题分类：

- Tool Result 是否正确进入 Context？
- failure schema 是否明显？
- 模型是不是错误解释 exit code？
- Retry / planning 是否缺少 stop condition？
- 最终 Outcome Grader 是否只看文本？

修复后加入：

> 这个原始 Bad Case + 变体

进入 eval dataset。

这才形成：

~~~text
production bad case
→ trace
→ root cause
→ targeted change
→ regression eval
→ deploy
~~~

Data Flywheel。

---

## 41. Engineering Trade-off：为什么不把所有状态交给模型

模型推理灵活，但：

- 不确定；
- token expensive；
- 难做强一致性；
- 不能承担安全边界；
- 不能可靠持久化所有 runtime invariant。

所以 Codex 把：

### 适合程序确定的

- 权限；
- job lease；
- thread identity；
- tool routing；
- sandbox；
- token budget；
- checkpoint；
- protocol pairing；
- retry count；
- cache key。

放 Runtime。

### 适合模型判断的

- 任务语义；
- 代码理解；
- 下一步 Tool；
- Memory extraction；
- Memory consolidation；
- compaction summary；
- 复杂诊断 / editing strategy。

放模型。

成熟 Agent 的核心不是：

> “让模型越自主越好。”

而是：

> **把需要概率推理的部分交给模型，把必须保持一致和安全的部分留在 Runtime。**

---

## 42. Engineering Trade-off：为什么 Memory / Compaction 也用模型

因为这些任务需要语义压缩：

- 哪些约束关键；
- 哪些历史重复；
- 哪些用户表达是可复用偏好；
- 哪些 correction 应覆盖旧事实。

硬规则无法覆盖全部自然语言。

但 Codex 不会让模型单独承担正确性。

它在模型外继续提供：

- bounded input；
- structured output；
- filesystem boundary；
- validation；
- job ownership；
- retention；
- provenance；
- checkpoint；
- metrics。

可以概括成：

> **LLM 负责语义变换，Runtime 负责边界与可验证性。**

---

## 43. 一套适合面试的 Codex Production 回答

~~~text
Codex 的 Production 边界不是简单的 LLM + Tools，而是 Session、Turn、Step 和 Context Window 四个生命周期叠加。
Session 保存长期状态和持久化，Turn 管一次用户目标与 turn-scoped model session，
Step 捕获当时的 Tool、Permission、Environment，Context Window 管模型历史基线和 Compaction。

错误首先按层分类。
Stream、Connection、Rate Limit 走有限 retry；
WebSocket 达到条件后可以 fallback HTTP；
ContextWindowExceeded 不做普通网络重试，而进入 Compaction / 新窗口；
Tool 参数类错误回给模型修复；
Sandbox Denied 只能在 Policy 允许时通过 approval 做有限 escalation；
Fatal / invariant 错误则 fail fast。

长期执行依赖 ThreadStore。
Compaction 成功后会持久化 replacement-history checkpoint；
Resume / Fork 从最新仍有效 checkpoint 加 suffix 重建，而不是永远从第一条 JSONL replay，
同时还要恢复 WorldState、Turn settings、Context window 和 token state。

规模化时也不是依赖超大 Context。
Tools 通过 Registry → policy filter → Deferred discovery → 小候选集，
Skills 用 metadata budget + progressive disclosure，
Memory 用 Phase1/Phase2 consolidation、usage feedback 和 bounded summary。

评测则分 Outcome、Process、Safety、Resource。
Codex 源码本身已经提供 unit/integration tests、model-visible snapshots、
Analytics/OTEL、Memory/Skill/Tool/Compaction metrics 和 opt-in Rollout Trace。
在这些证据上再构建任务级 Eval Harness，分别测 Context constraint retention / compaction equivalence、
Memory extraction / correction / retrieval、Tool discovery / permission / cancellation，
最后用真实 environment outcome 验证整个 Coding Agent，而不是看它有没有说“完成”。
~~~

---

## 44. 源码核验入口

- [protocol/src/error.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/protocol/src/error.rs)：Codex / Sandbox error taxonomy。
- [core/src/responses_retry.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/responses_retry.rs)：stream retry / reconnect / fallback。
- [core/src/client.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/client.rs)：ModelClient / turn-scoped ModelClientSession。
- [core/src/tools/orchestrator.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/orchestrator.rs)：approval / sandbox / escalation。
- [core/src/tools/parallel.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/tools/parallel.rs)：parallel gate / cancellation / timing。
- [thread-store/README.md](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/thread-store/README.md)：持久化边界。
- [core/src/session/rollout_reconstruction.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/rollout_reconstruction.rs)：Resume / Fork reconstruction。
- [thread-store/src/local/model_context.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/thread-store/src/local/model_context.rs)：local model-context checkpoint scanning。
- [analytics/src/facts.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/analytics/src/facts.rs)：structured analytics facts。
- [rollout-trace/README.md](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/rollout-trace/README.md)：深度诊断与 semantic graph。
- [core/tests/suite/](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/tests/suite)：核心集成测试。
- [core/tests/suite/websocket_fallback.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/tests/suite/websocket_fallback.rs)：WS → HTTP fallback。
- [core/tests/suite/scenarios.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/tests/suite/scenarios.rs)：跨能力场景测试。
- [core/tests/suite/snapshots/](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/tests/suite/snapshots)：model-visible request/history snapshots。
- [analytics/src/tests/suite/turns/compaction_tests.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/analytics/src/tests/suite/turns/compaction_tests.rs)：Compaction analytics contract。
- [memories/write/src/metrics.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/metrics.rs)：Memory pipeline metrics。
- [ext/skills/src/render_observability.rs](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/skills/src/render_observability.rs)：Skill catalog pressure metrics。

---

至此，Codex 的四条源码学习主线形成闭环：

~~~text
Context
模型这一次看见什么，以及怎样跨长 Session 继续

Memory
哪些过去信息值得跨 Session 保存、怎样召回和纠正

Tool
模型怎样获得并安全执行真实能力

Engineering & Evaluation
这些机制怎样在失败、规模化和长期运行下保持可恢复、可诊断、可验证
~~~

回到：[Codex 系统总览](README.md)
