
# 04. DeerFlow Engineering & Evaluation｜Checkpoint、Run Journal、Subagent、Recovery 与评测

[← Tool](03-tool-lifecycle.md) · [DeerFlow 总览](README.md) · [成熟产品源码学习](../README.md)

> **源码基线：** bytedance/deer-flow@1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe

DeerFlow 2.0 进入 Production（生产环境）以后，不只是一个 LangGraph Agent。

同一次用户任务至少存在四类不同事实：

~~~text
LangGraph Checkpoint
Agent 下一步怎样继续

Run Journal / RunEventStore
这次 Run 发生了什么

Sandbox / Workspace
外部世界现在变成什么样

Gateway Run Row
这次产品级运行现在是什么状态
~~~

如果把这些都叫“历史”，就很难解释：

- 为什么取消 Run 可以回滚 Agent State，却不一定能倒转外部副作用；
- 为什么 UI History 不直接从 Checkpoint 读；
- 为什么 Subagent 不用 Parent Checkpointer，但它的步骤仍然能被 UI 回看；
- 为什么 Branch 老 Turn 时不能复制今天的 Workspace 文件；
- 为什么 Replay 正确性必须同时检查 Checkpoint lineage 和 Run event feed。

这一篇就沿这条可靠性主线展开。

---

## 1. Checkpoint、Rollback、Branch：Agent State 怎样可靠地回到过去

### LangGraph Checkpoint 回答“Agent 下一步怎么继续”

DeerFlow Lead Agent 可以挂载 LangGraph Checkpointer。

Checkpoint 保存 ThreadState，包括：

- messages
- summary_text
- delegations
- skill_context
- promoted tools
- todos / goal / task state
- sandbox identity
- middleware contributed channels

它是：

> **Agent continuation state（智能体续跑状态）。**

#### 为什么不能绕开 CheckpointStateAccessor

DeerFlow 自己封装：

CheckpointStateAccessor

原因是当前支持：

- full checkpoint mode
- delta checkpoint mode
- cached history
- custom middleware state schema
- compatibility marker

Delta Mode 下 raw checkpoint 甚至不保证直接包含 materialized messages。

所以任何需要：

- read state
- history
- update state
- rollback
- manual compact

的代码，都应该经过 Accessor。

否则一段看似简单的：

~~~text
checkpointer.get_tuple()
~~~

可能拿到 Delta sentinel，或者漏掉 Extension / Middleware 自定义 Channel。

---

### 为什么 Wholesale State Replacement 必须使用 Mutation Graph + Overwrite

LangGraph Channel 往往有 reducer。

例如 messages 默认是 add_messages。

如果 rollback 想恢复：

~~~text
[A, B, C]
~~~

却普通 update：

~~~text
messages = [A, B, C]
~~~

Reducer 可能把它解释成：

> 在当前 history 后面再 merge 一次 A B C。

所以 DeerFlow 需要：

- Overwrite
- build_state_mutation_graph

这条 mutation graph 没有真正 Agent Node，只借用和 Agent Graph 相同的：

- state schema
- channel versions
- checkpoint metadata
- checkpointer machinery

然后写一个新的 idle checkpoint。

为什么还要使用**当前 Agent 的真实 state schema**？

因为自定义 Agent Middleware 可以贡献额外 Channel。

如果 rollback 只用 Base ThreadState：

> 恢复时这些 extension channels 会静默消失。

因此 Restore / Compact 本身也必须知道当时 Agent Assembly。

---

### Full 和 Delta Mode 为什么需要不同 Rollback 算法

Run 开始前，Worker 可以捕获一个完整 RollbackPoint（回滚点）：

- pre-run materialized state
- checkpoint config
- pending_writes

如果捕获失败：

> rollback disabled，不能拿半份 state 冒充可靠恢复点。

#### Full Mode

取消并选择 rollback 时，可以从 pre-run checkpoint fork 一个新 head。

Parent checkpoint 没被原地改写。

未显式替换的 Channel 可以自然继承 Parent blobs。

#### Delta Mode

情况更复杂。

当前 Run 可能已经在 pre-run checkpoint 上追加 sibling delta writes。

直接 Fork pre-run checkpoint：

> 可能让新 head 和被取消分支共享不安全的 delta ancestry。

所以 Delta rollback 会在**当前 head**上，把捕获到的每一个 Channel 全量恢复。

Reducer channel 使用 Overwrite。

只存在于 current head、却不在 RollbackPoint 的 Channel 还要重置到 schema default / None。

这也是为什么 Delta Mode 不能只理解成“少存一点 Messages”。

它会改变恢复算法。

---

### Edit Replay 失败以后为什么也必须回滚

DeerFlow 支持：

- Regenerate（重新生成）
- Edit and rerun（编辑后重跑）

Edit Replay 会先让 Thread 暂时进入：

> “假设用户当时说的是新文本。”

如果新的 Run：

- failed
- timed out
- interrupted

但不把 pre-run state 恢复：

> 用户 UI 会停留在一个并没有成功生成替代答案的临时分支。

所以 Edit Replay 的失败路径会恢复 pre-run Checkpoint，并在 stream 结束前重新发布 restored values。

产品语义是：

> **只有新 Run 成功，编辑后的历史才真正成为新主线。**

---

### Branch / Regenerate 为什么必须沿 Checkpoint Parent Lineage 查找

LangGraph 一个 Thread 里可能有 sibling branches（兄弟分支）。

如果用户从中间历史 Regenerate，单纯按 created_at：

> “找到目标消息之前最近的 checkpoint”

可能选到另一个 sibling branch。

DeerFlow 因此从当前 Head 沿：

parent_config

向前走。

找到真正包含目标 Turn 的同一 lineage checkpoint。

#### Legacy fallback

旧导入历史可能没有完整 parent links。

这时可以有限 chronological fallback。

但不能把：

> “找不到正确 checkpoint”

当成：

> “随便挑一个差不多的。”

Storage / checkpoint-mode error 仍然 fail closed。

---

### Workspace 为什么不能像 Checkpoint 一样历史回放

LangGraph Checkpoint 保存的是 Agent State。

但真实文件系统：

/mnt/user-data/workspace

不是每个 Turn 都做版本化 snapshot。

所以 Branch 一个**历史旧 Turn**时：

> 不能把当前 Workspace 直接复制过去。

因为当前 Workspace 可能包含之后很多 Turn 才产生的文件。

这会让过去分支“提前看到未来”。

DeerFlow 的策略是：

#### 从最新 Turn Branch

可以 best-effort copy 当前 Workspace。

因为 Branch 点就是现在。

#### 从历史 Turn Branch

跳过 Workspace clone。

只恢复 Message / Checkpoint History。

这是非常重要的因果一致性：

> **没有被时间版本化的外部状态，不能伪装成可历史回放。**

---

## 2. Run Journal：产品事件历史为什么不能等同于 Checkpoint

### Run Journal 回答的是另一件事：“产品里到底发生了什么”

核心：

backend/packages/harness/deerflow/runtime/journal.py

RunJournal 是 LangChain Callback Handler。

它把 Runtime callback 规范成：

RunEvent

写进 pluggable RunEventStore。

典型事件包括：

- run.start / run.end / run.error
- llm.human.input
- llm.ai.response
- llm.tool.result
- memory.context
- middleware events
- token usage / latency
- artifact delivery
- Subagent step events

它不等于 Checkpoint。

#### 为什么不记录每个 LLM token

RunJournal 刻意不实现 on_llm_new_token。

Streaming Token 是高频 transient（瞬态）UI 数据。

持久 Feed 主要记录：

> 完整 AIMessage。

否则一个长回答可能产生几千个 Event Row，Replay / History 成本巨大。

所以：

~~~text
Live SSE
适合瞬态 chunk

Run Event Store
适合可重放语义事件
~~~

---

### Run Journal 为什么还要做 LLM Response Coalescing

某些 Provider / Callback 链可能对同一个 LangChain run id 多次触发 on_llm_end。

第一次可能没有完整 usage。

如果 Journal 每次都直接写一条 Assistant：

> UI History 会出现重复答案，Token 也重复计费。

所以 RunJournal 会临时 coalesce（合并）同一个 LLM response，再形成最终 Event。

同时有 counted run ids 等集合防重复 Token accounting。

这是 Observability（可观测性）反过来保护产品正确性的例子。

---

### 为什么 Journal 不能跨到 Subagent 的隔离事件循环

RunJournal 自己标记：

deerflow_loop_bound = True

因为它持有：

- Parent loop 上的 async tasks
- Event Store / connection pool
- buffer flush state

SubagentExecutor 会把 Subagent 工作放到独立 persistent asyncio loop。

它会复制 Parent ContextVars，但过滤：

> deerflow_loop_bound callback。

否则 Parent RunJournal 在另一个 Event Loop 被调用，可能：

- Future attached to different loop
- 重复 token accounting
- 重复 event rows

同时它又不能简单清空所有 callbacks，因为 LangGraph 的 stream callback 需要保留，才能把 Child token frame 正确 namespaced 回 Parent Stream。

所以跨 Agent Context Propagation 需要：

> **保留可跨 Loop 的语义，移除 Loop-owned Resource。**

---

## 3. Subagent：Context Isolation、Step Evidence 与 Capacity

### Subagent 为什么 checkpointer=False

DeerFlow 的 native Subagent 是 one-shot delegation（一次性委派）。

Executor 创建 Child Agent 时显式：

checkpointer=False

原因是：

> 它不需要像 Lead Thread 一样跨用户 Turn Resume。

如果直接继承 Parent Checkpointer：

- Child State 可能写进 Parent Namespace
- Child Message 可能污染 Parent stream
- Parent checkpoint lineage 可能被子图改变

因此 Child 有自己的 in-memory ThreadState 生命周期。

但：

> 不持久 Child Checkpoint ≠ 不记录 Child Execution Evidence。

---

### Subagent Step 怎样被产品 UI 回看

SubagentExecutor 会流式观察 Child graph 的 values。

Step Capture 不只是拿：

messages[-1]

因为一个 LangGraph ToolNode super-step 可能一次 append 多个 ToolMessage。

它会扫描自上次 cursor 以后所有新增消息，捕获：

- AIMessage
- ToolMessage

形成 Subagent Step Event。

Runtime Run Worker 再把这些：

~~~text
task_start
task_step
task_end
~~~

转成 RunEventStore：

- subagent.start
- subagent.step
- subagent.end

而且 category 单独是 subagent。

这样主 Thread 的普通 Message Feed 不被 Child 中间步骤淹没；前端展开 Subagent Card 时，再按 task_id + after_seq 分页读取。

---

### Summarization 为什么会影响 Subagent Step Capture

Step Capture 原本假设：

> Messages 长度只增加。

但 Child 也可以使用 SummarizationMiddleware。

压缩后：

~~~text
len(messages)
突然变小
~~~

如果 cursor 仍指向压缩前的旧长度：

> 后面新产生的 Child Step 会一直被当成“还没超过旧 cursor”，永远不记录。

所以检测到：

total < processed_count

时，Capture Cursor 重置到新 tail。

同时用 message id / content dedup 防止重复发旧 Step。

这是一个非常典型的跨组件 invariant：

> **Context Compression 改变了 Observability 的索引假设。**

---

### Parent Context Snapshot 为什么不能原样复制父 ThreadState

Subagent 支持 context_mode：

- isolated
- snapshot

#### isolated

默认更安全。

Delegation Prompt 必须自包含。

Child 不自动获得 Parent 对话。

#### snapshot

需要更多上下文时，ParentContextSnapshot 可以捕获：

- parent summary_text
- genuine user messages
- visible assistant messages
-已完成 Tool Call + Result 的文本化表示
-支持序列化的 media

但是不会传：

- Parent System Prompt
- hidden framework messages
- Runtime state
- artifacts metadata
- Secret / authorization
-未完成 Tool Calls

整个 Snapshot 还会被标记为：

> historical data, not instructions.

#### 为什么 Tool Call 变成 inert text

如果直接把 Parent AI tool_call block + ToolMessage 复制给 Child：

> Provider 可能认为这些是 Child 自己过去执行过的 Tool Protocol。

Child 甚至可能把 Parent 的外部副作用当成：

> “我已经做过。”

所以 Parent Tool Calls 只作为历史文本描述，而且必须有 retained result 才算 completed。

---

### Snapshot 为什么是 dispatch-time immutable

ParentContextSnapshot 在 task dispatch 前捕获并序列化。

Child 执行期间 Parent 继续收到新消息：

> 不会动态更新 Snapshot。

原因和 Fork 一样。

否则：

- Child 的过去 Context 会随着 Parent 改变
- Replay 无法证明 Child 当时看到什么
-Sibling Subagents 会互相通过 Parent 间接污染

因此：

> **Delegation Context 是不可变快照，不是共享聊天室。**

---

### Subagent 为什么还要独立 Capacity Budget

DeerFlow 同时限制：

- 每个 run 最多创建多少 Subagent
- 同时执行多少 Subagent
- 每个 Subagent 最大 turns / timeout
- batch service capacity

这些不是模型 Token Budget 的重复。

每个 Child 还会占：

- event loop work
- model requests
- tools
- MCP sessions
- sandbox
- RunEvent storage
- output artifacts

如果模型可以无限 task()：

> 一次用户请求就能变成无限 fan-out。

所以 Multi-Agent 必须有：

> **Delegation Budget + Execution Capacity。**

---

## 4. Runtime Ownership 与恢复：Sandbox、Dangling Calls、Rollback、Replay

### Sandbox Lease 为什么也是 Runtime Ownership

Sandbox 不是每个 Tool Call 临时 create / destroy。

SandboxMiddleware 会在 Run 开始 acquire，在结束 release。

不同入口：

- Run Worker
- upload sync
- artifact request
- MCP file bridging

都可能临时需要 Sandbox。

因此 Provider / Lease Manager 必须知道：

> 谁现在拥有这个 Sandbox。

取消过程中也不能过早释放：

~~~text
Run 正在 cancel
→ Child / Tool cleanup 还在运行
→ Sandbox 已 release
→ 后续清理访问失效
~~~

所以 Sandbox Lifecycle 和 Run Drain 必须同步。

---

### Dangling Tool Call 为什么还需要 Middleware 修复

真实历史可能因为：

- Provider output truncation
- interruption
- legacy history
- malformed tool call

出现：

~~~text
AIMessage:
  tool_call abc

但没有 ToolMessage abc
~~~

严格 Provider 下一轮可能直接拒绝请求。

DanglingToolCallMiddleware 会在模型调用前修复这种历史，使 Tool Call / Result 协议重新闭合。

注意这解决的是：

> **Model Protocol Consistency。**

并不意味着原 Tool 真正执行成功。

如果过去副作用未知，产品仍应该通过 Receipt / Journal / External State Verification 判断，而不是因为补了一条 Error ToolMessage 就说：

> “它没执行。”

---

### Run Cancel 为什么 State Rollback 和 Side-effect Rollback 是两回事

用户 Cancel 一个 Run，可以选择 rollback Agent State。

Checkpoint 可以恢复：

- messages
- summary
- todos
- promoted tools
- middleware channels

但如果这次 Run 已经：

- 发了 Slack 消息
- 修改了远端数据库
- 调了 MCP API
- 写了外部系统

LangGraph Checkpoint 没法让它自动倒转。

所以 Cancel with rollback 实际保证的是：

> **Thread continuation state 回到 pre-run。**

不是：

> 世界时间倒流。

这也是为什么 Tool Receipt、External Idempotency、Status Verification 很重要。

---

### Run Event Feed 为什么和 Checkpoint History 要互相对齐

DeerFlow UI 的 Thread Message Feed 主要来自 RunEventStore，而不是每次打开都直接把 Checkpoint messages 序列化出来。

这会产生一个工程问题：

#### Branch 新 Thread

新 Branch 已经继承 Parent Checkpoint History。

但它自己的 RunEventStore 还是空的。

如果不 seed：

> 第一轮 Run 以后 UI 只看到新消息，继承历史消失。

所以 Branch Creation 会把 Checkpoint 中可见 Messages 转成 synthetic run-event rows。

而且不是整段共用一个 run_id。

它会按每个 Human Turn 创建 synthetic run id。

为什么？

Regenerate 一个 inherited answer 时，Feed 会按 source run_id supersede（替换）那一轮。

如果所有 inherited history 共用一个 id：

> Regenerate 一轮会删掉整个继承历史。

这说明 UI History 和 Checkpoint 虽是两条存储，但必须共享稳定的 Turn Semantics。

---

### SSE Replay Gap 为什么需要 Full State Recovery

Live Run Event Stream 有 seq。

Client 断线重连时可以：

> after_seq 继续。

但 Event Store retention / gap 可能使请求的 seq 已经不存在。

这时不能假装：

> 从现有最早 Event 继续就行。

Gateway 会给出 replay gap signal，要求 Client：

> reload durable state。

因为缺失一段 reducer event 后继续增量应用，Frontend State 会错误。

这是标准 Event Streaming 原则：

~~~text
连续增量可用
→ replay delta

出现 gap
→ 回到 authoritative snapshot
~~~

---

## 5. Observability 与验证体系：怎样证明 Harness 没有跨层漂移

### Extension / Middleware Assembly 为什么也需要可观测 Fingerprint

DeerFlow Agent 的行为取决于：

- model
- System Prompt
- Tool Schemas
- Middleware order
- Skill set
- Deferred Tool Catalog
- Extension policy
- Context policy parameters

如果线上两个 Run 行为不同，只说：

> “都是 DeerFlow Agent。”

远远不够。

当前源码可以构建 AssemblyDescriptor，记录真正组装结果的 hashes / identities。

而且只在 Observer 真正需要时计算，因为：

> Tool schema serialization 和 middleware policy probe 本身有成本。

这是一种很成熟的 Observability trade-off：

> **可诊断，但不让诊断每次都拖慢运行。**

---

### DeerFlow 的测试体系为什么特别像“产品 Harness 验收”

backend/tests 当前有数百个测试。

和产品学习最相关的可以按不变量分类。

#### Context

- test_context_compaction.py
- test_summarization_middleware.py
- test_durable_context_middleware.py
- test_dynamic_context_middleware.py
- test_tool_output_budget_middleware.py
- checkpoint full / delta parity

#### Memory

- DeerMem extraction / retrieval / eviction
- OpenViking / Honcho backends
- memory scope
- benchmark scope isolation
- shutdown / gateway memory lifecycle

#### Tool / Skills / MCP

- deferred tool
- real LLM promotion
- skill policy
- skill secret
- MCP pool / OAuth / routing / timeouts
- read-before-write
- tool receipts / error handling

#### Sandbox

- Local / AIO / E2B / OpenSandbox
- authorization
- leases
- network proxy
- orphan reconciliation
- path confinement

#### Subagent

- context snapshot
- execution capacity
- turn / token budget
- checkpointer isolation
- step events
- receipt / acceptance
- persistence

#### Run / Replay

- run event store
- stream contract
- rollback
- recovery
- thread branch / regenerate
- replay golden
- frontend replay E2E

这不是只测试单函数。

它在锁：

> **跨层产品语义。**

---

### Replay E2E 为什么非常重要

一个 Agent 产品可能出现：

~~~text
Backend unit tests 全绿
Frontend unit tests 全绿
但真实 Replay 顺序错
~~~

因为问题发生在：

- SSE ordering
- checkpoint state
- RunEventStore
- reducer events
- UI reconstruction

之间。

DeerFlow 有 Replay Provider / Golden fixtures 和真实 E2E 来锁这条链。

例如可以重放：

- Model messages
- Tool results
- Run events
- checkpoint transitions

让前端收到确定性 Stream。

这种测试比“Mock API 返回 Hello”更接近 Agent Harness 的系统验证。

---

### Memory / Subagent / Context 为什么还要有 Benchmark

很多 Agent 机制不是“对 / 错”二值。

例如：

- Memory scope isolation
- Memory eviction
- Sandbox provider overhead
- checkpoint materialization
- concurrency
- tool result probe
- Context snapshot size

会随着数据规模退化。

所以仓库还有：

- bench tests
- performance tests
- dataset / report tests

最近的 DeerMem scope-isolation benchmark 就直接验证：

> 跨 User / Agent scope 的长期 Memory 不应该泄漏。

这类 benchmark 本质上既是性能验证，也是安全 / 质量评测。

---

## 6. 用场景和指标评价一个真正的 DeerFlow Run

### 四个场景把工程边界串起来

#### 场景一：Cancel Run 后，模型历史回滚了，但 Slack 消息已经发了

这是正常可能发生的。

Checkpoint rollback 只能恢复 Agent State。

解决外部副作用需要：

- Tool Receipt
- idempotency key
- external status check
- compensation logic

不能要求 Checkpointer 自动撤销世界。

#### 场景二：Branch 一个三天前 Turn，却看到今天生成的文件

这是 bug。

旧 Turn 的 Workspace 没有 version snapshot。

正确行为是：

> 历史 Branch 只继承 Checkpoint History，不复制当前 Workspace。

#### 场景三：Subagent 说“我已经执行了父 Agent 的 Tool”

检查 ParentContextSnapshot。

Parent Tool Call 应该只是 inert historical text，并明确：

> not executed by you。

如果 Child 把它当自己的 Receipt，Snapshot authority boundary 失败。

#### 场景四：Summarization 后 Subagent Step 从 UI 消失

检查 capture cursor。

Context Compression 缩短 Child messages 后，processed_count 是否 reset 到新 tail。

这就是 Context 与 Observability 互相影响的典型跨组件 bug。

---

### 应该怎样评测 DeerFlow 这个 Harness

#### Outcome

- 真实任务是否完成
- Tests 是否通过
- Artifact 是否正确
- Project goal 是否满足

#### Process

- Model calls
- Tool calls
- Subagent count
- Loop detection
- Summarization 次数
- Memory write / retrieval
- Retry / timeout

#### Safety

- Authorization bypass
- Skill policy bypass
- Cross-user Memory
- Sandbox path escape
- MCP auth leakage
- Subagent authority leakage
- Prompt Injection through Memory / Snapshot

#### Reliability

- Cancel / rollback
- Restart
- full / delta checkpoint parity
- SSE reconnect / replay gap
- MCP disconnect
- sandbox provider failure
- Memory backend failure

#### Resource

- Token
- latency
- Prompt cache
- Tool output bytes
- Memory LLM cost
- Subagent fanout
- Checkpoint / RunEvent storage

最后不能压成一个“总分”。

这些指标代表不同 Trade-off。

---

### 从 DeerFlow 源码能抽出的系统设计原则

**第一，Agent State 和 Product Evidence 应该分开。**  
Checkpoint 让 Agent 继续；Journal 让产品解释过去。

**第二，所有历史状态都要问“它真的能时间旅行吗？”**  
Messages 有 Checkpoint；Workspace 没有完整历史版本，所以旧 Branch 不复制当前文件。

**第三，压缩不是删除信息，而是改变未来模型需要携带的信息结构。**  
summary_text、delegation ledger、skill refs 都是对原历史的更稳定表示。

**第四，Subagent Context 必须降权。**  
过去父对话是数据，不是 Child System Authority。

**第五，副作用恢复不能只靠 Checkpoint。**  
Tool Receipt、Journal、External Verification 和 Idempotency 同样重要。

**第六，Middleware Order 本身就是协议。**  
Dynamic Context、Skill Policy、Deferred Filter、Summarization、Recovery 的先后改变行为。

**第七，成熟 Eval 应围绕跨层 invariant。**  
真正容易坏的是 Checkpoint ↔ Journal ↔ SSE ↔ UI、Memory ↔ Context、Subagent ↔ Parent，而不是某一个函数。

---

## 7. 源码锚点

1. [Runtime architecture](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/docs/ARCHITECTURE.md)
2. [Runtime notes / checkpoint invariants](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/runtime/AGENTS.md)
3. [Checkpoint state accessor](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/runtime/checkpoint_state.py)
4. [Checkpoint mode](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/runtime/checkpoint_mode.py)
5. [Run worker](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/runtime/runs/worker.py)
6. [Run Journal](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/runtime/journal.py)
7. [Checkpoint lineage](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/app/gateway/checkpoint_lineage.py)
8. [Thread lifecycle](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/docs/THREAD_LIFECYCLE.md)
9. [Checkpoint retention contract](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/docs/checkpoint-retention-contract.md)
10. [DanglingToolCallMiddleware](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/agents/middlewares/dangling_tool_call_middleware.py)
11. [Subagent context snapshot](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/subagents/context_snapshot.py)
12. [Subagent executor](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/subagents/executor.py)
13. [Subagent runtime notes](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/packages/harness/deerflow/subagents/AGENTS.md)
14. [Replay E2E guide](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/docs/REPLAY_E2E.md)
15. [Run event stream contract](https://github.com/bytedance/deer-flow/blob/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/docs/RUN_EVENT_STREAM.md)
16. [All backend tests](https://github.com/bytedance/deer-flow/tree/1e3bfa09d4e31e02d109ef2f4b41895dc89a78fe/backend/tests)

回到：[DeerFlow 系统总览](README.md)
