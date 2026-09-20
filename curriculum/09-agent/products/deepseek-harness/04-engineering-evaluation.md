# 04. DeepSeek Harness Engineering & Evaluation｜Crash Recovery、Retry、Subagent 与验证体系

[← Tool](03-tool-lifecycle.md) · [DeepSeek Harness 总览](README.md) · [成熟产品源码学习](../README.md)

> **源码基线：** `deepseek-ai/deepseek-harness@ddefc45fbc7f8e46dd73185e68295696d1297887`

前面三篇解决的是“正常运行时怎样工作”。

这一篇关心另一类问题：

> **进程可能崩，网络可能断，模型可能 429 / timeout，Tool 可能已经产生副作用，Child Agent 可能在后台继续跑，Session 格式还会升级。DeepSeek Harness 怎样让这些事情仍然可恢复、可解释、可验证？**

这里最值得抓住的一条线是：

> **Runtime 中重要的异步动作，尽量先形成 durable evidence（持久证据），再进入等待或副作用。**

这就是为什么源码里反复出现：

~~~text
先 append event
→ 再 await
~~~

---

## 1. Session 为什么能在 Crash 后继续

### 1. JSONL 不是“聊天导出格式”，而是 Session Event Store

默认持久化实现：

- `packages/session/session-persistence-jsonl/`

Base bundle 默认挂载：

`dsh-session-persistence-jsonl`

它保存的不是已经投影好的 Chat Messages，而是完整 Session Event Stream（会话事件流）。

物理上默认使用：

- JSONL logical records；
- Zstandard checksummed frames。

也可以关闭 compression，写原始 newline-delimited JSONL。

为什么保存 Event，而不是 `messages[]`？

因为 Resume 需要恢复的不只是 User、Assistant、Tool Result，还包括 Turn / Step boundary、Request Header、Compaction replacement、Permission state、Sandbox mode、Subagent descriptor / lineage、Retry bookkeeping 和 Inbox mutations。

如果只保存 Model Messages：

> 很多运行时状态只能重新猜。

#### Session File 为什么采用不可变 Format Generation

当前格式使用类似：

~~~text
session.jsonl.zstd
session.v1.jsonl.zstd
session.v2.jsonl.zstd
session.v3.jsonl.zstd
...
~~~

的 canonical generation（规范代际）。

当旧格式需要迁移，源 generation 不会原地改写。Write open 会读取旧版本、迁移成当前 logical events、编码新的临时 generation、验证、确认 source revision 没漂移，再发布新的 current generation。

旧路径仍保持 byte-identical（字节不变）。

如果原地升级时写到一半 crash，一个原本可读的 Session 可能直接变成不可读。Immutable generation（不可变代际）让升级更像“发布一个新版本”，而不是给原文件做手术。

#### 为什么最高版本不可读时不能偷偷回退旧版本

Persistence 会选择 numerically highest canonical generation（编号最高的规范代）。

如果最高代是未来格式、当前 Build 不支持，就明确 refusal（拒绝），不会说“那我读前一个老版本吧”。

旧 generation 可能缺少后来发生的 Session Events，回退读取会制造：

> **看似成功，但悄悄丢历史。**

所以在这里：

~~~text
Unsupported
优于
Silent stale fallback
~~~

---

### 2. 持久化正确性从“一个 Writer”开始

Persistence Service 对 write handle 做 single-writer ownership（单写者所有权）。

同一 Session 已经被一个 Runtime 持有写权限时：

`open(id, 'write')`

会拒绝第二个 Writer。

底层还使用进程 / OS 级 lease（租约）机制。

原因很直接：如果两个 Agent Process 同时 append：

~~~text
step/start
tool/result
compaction/start
~~~

Event Seq 和协议配对会失去单一真源。

Read-only Observer 可以并发读取，但 authoritative write path（权威写路径）必须唯一。

#### 每次 append 为什么要有明确 Durability Barrier

JSONL backend 会按 batch append、`fsync`，成功后才 resolve append。如果 write / sync 失败，会尽量回滚到 append 前的文件长度。

另外：

`flush()`

是明确 Durability Barrier（持久性屏障）。

Base bundle 还安装：

- `dsh-session-checkpoint-policy`

用于在关键 Model / Top-level Dispatch 边界前确保 Session durability。

所以“Event 已经在内存数组里”不等于：

> crash 后一定恢复。

Persistence API 对这个差异有明确 contract。

---

### 3. Crash Recovery 必须先区分“文件坏了”还是“协议没闭合”

这是 Persistence 设计里很容易混淆的一点。

#### Torn Physical Tail

例如写 JSONL / Zstd frame 时进程突然没了。

最后一条 physical record 不完整。

这属于 Storage Layer。

JSONL backend 会：

- 只返回完整、连续、验证通过的 prefix；
- 丢掉 incomplete raw line；
- 对 torn Zstd frame 尽量恢复完整 decoded records；
- Write Handle 在首次新 append 前修正物理尾部。

#### Interrupted Semantic Turn

但也可能所有 Event 都已经完整落盘：

~~~text
turn/start
step/start
assistant/message
tool/call
<进程崩溃>
~~~

文件一点没坏。

只是 Agent Protocol 没闭合。

这属于 Agent / Session Semantic Layer。

两种 failure 不应该由同一层处理。

---

### 4. Resume 怎样修复 Interrupted Turn

核心函数：

- `packages/core/session/src/repair.ts::interruptedTurnClosers()`

Agent Loop Resume 时会：

1. 先以 write ownership 打开 Session；
2. 读取 physically valid log；
3. 计算需要补哪些 synthetic closer；
4. 把这些 closer 作为正常 Event Batch append 回去；
5. 再发布 Live Agent。

可能需要补：

- missing tool result；
- `step/end`；
- `turn/end { interrupted }`。

#### 为什么 Tool Repair 有两种不同错误

源码定义：

- `TOOL_NOT_STARTED`
- `TOOL_OUTCOME_UNKNOWN`

如果 Assistant Request 存在，但 Tool Call 还没 durable commit，可以明确：

> Tool 没有开始。

如果已经有 durable `tool/call`，但没有 `tool/result`，就不能假装 Tool 没执行。

它可能执行成功后 crash、执行一半、远端副作用已经发生，或者根本没真正 dispatch。

所以 Repair 给模型的指导是：

> 只读 / 幂等操作可以谨慎 retry；有副作用的操作先验证外部状态或询问用户，不要盲目重放。

这比“所有未完成 Tool 自动重试”安全得多。

---

## 2. Retry 为什么必须建立在 durable progress 上

### 5. LLM Retry 也遵守“durable before wait”

默认 Base bundle 安装：

- `dsh-llm-retry`

它挂在：

`agent/request-error`

waterfall 上。

一次 transient model failure（瞬态模型失败）如果符合 Provider Retry Policy，Runtime 先 append：

`llm/retry`

记录 provider、policy key、failure、retry number 和 delay。

然后才真正等待 backoff。

Wait 完成以后再 append：

`llm/retry-started`

最后返回：

`{ kind: 'retry' }`

让 Agent Loop 重新跑失败 Step。

如果先 sleep 30 秒、然后才记录 retry，第 10 秒 crash 时日志完全不知道 Runtime 当时在等什么。当前顺序让待重试状态成为可解释的 Session Fact。

#### Retry 为什么放在 Agent Step Boundary，而不是包住任意 LLM Stream

`llm-retry` 的 README 很明确：

> 直接 `ctx.llm.stream()` 的调用不自动获得这套 retry。

Raw streaming consumer（原始流消费者）很难判断哪些 chunk 已经被外界看到、哪些副作用已经从中触发、重试后怎样避免重复。

Agent Loop 有明确 Step boundary。失败 Assistant Attempt 先 settlement，再由 `agent/request-error` 决定是否重建同一个 Step。

所以可靠 Retry 的边界是：

> **Durable Agent Step。**

不是任意 Promise。

#### Retry Policy 为什么属于 Provider，而 Executor 独立

`dsh-llm-retry` 自己没有 retry config。

哪些错误 retry、最大次数、backoff、always / normal，都属于 Provider Route 的 `retryPolicy`。

Executor 只负责在正确 lifecycle seam 上执行、读 durable retry history、计算 delay、写 Event、等待，再返回 retry action。

于是 Provider-specific policy（提供方策略）和 Runtime recovery mechanics（运行时恢复机制）被分开。

---

### 6. Context Overflow Recovery 不是普通 Retry

LLM 返回 Context Window Exceeded 时，不应该：

~~~text
retry same request
retry same request
retry same request
~~~

Basic Compaction 同样监听：

`agent/request-error`

如果识别 Context Overflow，会先尝试 Tool Result Pruning / Compaction。

只有当：

`session.surface.replaceGeneration`

真的前进，说明 Model-visible Surface 已经发生 durable reduction（持久缩减），才返回 retry。

这是一条非常重要的恢复原则：

> **Retry 必须有 progress evidence（进展证据）。**

否则同一个超长请求无限重放没有意义。

---

## 3. Subagent 怎样继承 Context、隔离 Authority 并长期运行

### 7. Subagent 的两种 Context Contract：Spawn 与 Fork

默认 Base bundle 同时提供：

- `spawn`
- `fork`

两种 in-process provider。

#### Spawn：全新会话

Spawn Child 继承 cwd、lineage、默认 provider / model / effort 等 creation option，但**不继承 Parent Conversation**。

所以 Delegation Prompt 必须自包含。

#### Fork：继承已完成的 Parent 历史

Fork Child 的 Session seed 是：

> **Parent Session 到最后一个 completed `turn/end` 的完整前缀。**

当前正在执行的 Parent Turn 不进入 seed。

为什么？

因为正在 Tool Calling 的半个 Turn，不是一个可以独立 replay 的 balanced session prefix。

所以 Fork 不是复制“内存中的最新 messages”，而是复制：

> **已经 durable 完成的 Turn Prefix。**

#### Fork 为什么只捕获一次，不做 Live Shared Context

Fork 发生时计算一次 completed-turn prefix。

Child 之后拥有自己的 Session。Parent 后续的 Turn 不会自动出现在 Child。

否则 Child Resume 时要重新读取 Parent，Parent 修改历史还会改变 Child 过去 Context，两个 Session 就失去独立可恢复性。

Fork 是：

> **Snapshot inheritance（快照继承）。**

不是 Shared mutable conversation（共享可变会话）。

---

### 8. Subagent 不继承 Parent Tool Authority

Spawn / Fork in-process README 都强调：

> Child gets a fresh flat registration scope.

Parent Tool restrictions / authority 不会直接进口。

Child 可以有自己的 persona、tool filter 和 scoped registrations。

这避免：

> Parent 有高权限 → Child 自动扩大权限。

Delegated Subagent 的 runtime context 还明确告诉模型：Child scope 在启动时固定，无法从自己 Session 内扩大；需要更高权限时应该把限制告诉 Parent。

这把 Multi-Agent 的权限边界写进 Runtime Contract，而不是只靠 Prompt 礼貌约束。

---

### 9. Continuable Subagent 为什么远比“一次性 Agent Tool”复杂

`ctx.subagents` 支持两种 child shape：

- one-shot；
- continuable。

Continuable Child 有 durable Session、stable child id、process-local Activation、Inbox、cold resume、send message、interrupt 和 descendant discovery。

#### 消息仍然复用 Agent Inbox

Subagent Service 没有再造第二套 Mailbox。

Parent 向 direct continuable child 发消息时：

- Child 正在工作：Steer 到最近 Step；
- Child idle：启动新的 Turn；
- Direct Child 不在内存：可以从持久 Session cold resume 后再投递。

同一套 next-turn / next-step 语义继续成立。

#### 为什么需要 Activation Capacity

默认 `maxActiveSubagents` 有有限值。

这是 process-local residency（进程内驻留）限制，不是历史总数限制。

Continuable Child 会占 Live Agent、Inbox、Ownership graph、可能的 Descendants 以及其他 Runtime resource。

如果 Parent 正等待 Child，而 Child 又在 capacity queue 里等待一个由 Parent 自己占住的 slot，容易形成死锁。

所以 capacity reached 时，新 child creation / cold resume 直接拒绝，不排队。

这说明 Multi-Agent Scaling 必须同时考虑：

> **Context Budget + Runtime Residency Budget。**

---

### 10. Multi-Agent 拓扑为什么也要持久化

成功创建本地 Child 后，Parent Session 会得到：

`subagent/catalog`

事实。

它记录 direct child identity / mode / label 等，让 UI、`list_agents`、Resume、descendant discovery 不必依赖“当前进程还记不记得曾经创建过 Child”。

Continuable Child 自己的 Session 里还有 durable descriptor，保存 provider / model / effort 等 cold-resume 所需身份。

Child Session Header 也会记录：

- `parentSession`
- `origin: 'subagent'`
- `delegationDepth`

因此 Multi-Agent topology（多智能体拓扑）并不是纯内存结构。

---

## 4. Plugin 生命周期与默认 Bundle 为什么决定真实产品

### 11. Cordis Plugin Lifecycle 为什么也是可靠性的一部分

DeepSeek Harness 的大多数注册——Tool、Prompt Section、Event Listener、Provider——都是 Cordis effect-scoped（生命周期作用域绑定）的。

Plugin unload 时，注册会自动 unwind（撤销）。

这直接影响：

- HMR；
- 配置 reload；
- MCP reconnect；
- Agent-scoped capability；
- Provider replacement。

一个重要原则是：

> **Removing Provider 阻止新工作进入，但不应该突然 revoke 已经接受、已经转移 ownership 的运行。**

Subagent Service 就明确区分 Provider Registration Lifetime 和 Accepted Run Lifetime。

这和成熟 Server 的 Job Executor / Connection Pool 是同一类 ownership 问题。

---

### 12. 为什么真正的产品架构要回到 Base Bundle

DeepSeek Harness 仓库 Package 很多。

真正理解“产品默认是什么”必须看：

- `packages/bundle/base/cordis.patch.yml`

这里能看到 shipped base 的真实 wiring（连接方式）。

例如：

~~~text
session
→ persistence
→ projections

sandbox
→ sandbox-policy
→ bash-sandbox
→ tool-bash

approval
→ permission-presets

tools
→ system-prompt
→ agent-loop

compaction
→ pruner
→ token-meter

subagent
→ spawn/fork providers
→ model-facing tools
~~~

所以“架构图”不应该从目录名猜出来。

应该回到 Product Composition（产品组合）。

---

## 5. 验证体系：从 Invariant 到真实 Provider E2E

### 13. 测试体系为什么特别适合这种 Plugin Harness

根 `package.json` 不只提供普通 Unit Test。

它还有：

- `test`
- `test:e2e`
- `test:bench`
- `test:snapshot`
- `test:web`
- `test:web:perf`
- `test:web:stress`
- `check:all`

以及大量 verifier scripts（验证脚本），覆盖：

- runtime closure；
- default product isolation；
- application entrypoints；
- package dependencies；
- tool catalog；
- config catalog；
- session format catalog；
- scoped events；
- persistence contract 等。

这反映出一个很重要的思想：

> **Agent Harness 的正确性，很大一部分是“跨 Package Contract 是否仍然成立”。**

不是某一个函数返回值对不对。

#### Invariant Companion 比普通单测多验证什么

很多 Package 有：

`invariant.ts`

它们验证 Session Event Stream 的跨事件关系，例如：

- Approval asked / decided 是否成对；
- Tool Call / Result 是否结构合法；
- Retry Started 是否有对应 scheduled retry；
- Turn / Step 是否平衡；
- Event identity 是否一致。

普通 Unit Test 说的是：

> “这个函数在这个例子里返回 X。”

Invariant 更像：

> **任何合法 Session Log 都必须满足这条协议。**

这对 Event-sourced Agent Runtime 特别重要。

#### Contract Suite 防 Provider 漂移

例如 Persistence Provider 有共享 contract tests。

任何 Backend 都要满足 append、flush、read、single writer、crash tail 和 ownership 等一致语义。

新增 Backend 不能只证明“看起来能存”。

#### Catalog Verifier 防公开能力面和源码脱节

DeepSeek Harness 自动生成：

- Tool Catalog；
- Config Catalog；
- Cordis API Surface；
- Session Format Catalog。

Verifier 会检查这些输出是否和源码同步。

插件很多的项目最容易先坏的，往往不是 Runtime，而是“文档说有哪些 Tool / Config / Event”和实际代码开始分叉。

---

### 14. Snapshot、Replay 与 With-key E2E 各自证明不同东西

#### Snapshot / Replay

Agent 系统常见 Bug 是：

> 本轮跑得对，但 Resume / Replay 不一样。

因此 Snapshot Test 不应只 snapshot UI。

更重要的是固定：

- Session Events；
- Surface；
- Model Request；
- Tool Pair；
- Compaction Result；
- Recovery Result。

仓库中的 LLM Replay / Session Snapshot 一类 test-support package，目的就是把 nondeterministic model runtime（非确定模型运行）尽量转成 deterministic runtime contract test（确定性运行时契约测试）。

#### With-key E2E

Mock Model 可以稳定测试 Event Order、Compaction Bracket、Tool Pipeline、Retry、Resume。

但它无法证明真实 Provider 接受这份 request、真实 Context Window / Tool Calling / Streaming surface 和模拟器完全一致。

Compaction 的实现记录明确提到 with-key e2e：用真实模型 + Bash，并降低限制，触发真正 Compaction，确认完整 `compaction/start…end`、Surface shrink 和最终任务完成。

这类测试不一定适合每个 PR 都昂贵运行，但它验证：

> **模拟协议与真实 Provider 没有整体偏离。**

---

## 6. 用故障场景检验系统是否真正闭环

### 15. 三个场景把恢复逻辑真正串起来

#### 场景一：Resume 后 Tool 又被执行了一次

按源码边界查：

~~~text
原 Session 是否有 tool/call？
        ↓
是否有 tool/result？
        ↓
Crash Repair 生成的是
TOOL_NOT_STARTED
还是
TOOL_OUTCOME_UNKNOWN？
        ↓
模型是否错误忽略了 unknown-outcome guidance？
        ↓
Tool 本身是否非幂等？
        ↓
是否应该先 Read / Verify 外部世界？
~~~

如果原日志连 `tool/call` 都没有，重试更安全。

如果已有 `tool/call` 但没有 result，Runtime 无法证明副作用没发生。

问题不是“Resume 太保守”，而是外部系统缺少 idempotency / status check。

#### 场景二：Context Overflow 一直重试

正确路径应该是：

~~~text
request error = context overflow
        ↓
compaction-basic 是否收到 agent/request-error
        ↓
tool result pruner 是否先有效缩减
        ↓
summary compaction 是否 commit
        ↓
session.surface.replaceGeneration 是否增加
        ↓
只有真正增加后才 retry
~~~

如果 `replaceGeneration` 没变却继续 retry，Recovery Progress Gate 失效。

如果变了但仍 overflow，Summary 可能仍太大，或 Retained Tail 太多。

增加 retry count 不是根因修复。

#### 场景三：Fork Subagent “没看到刚才 Parent 讨论的内容”

先确认：

> 那段 Parent Discussion 是否已经完成 `turn/end`？

如果 Parent 正处于：

~~~text
Assistant
→ Tool Call
→ Child Fork
~~~

当前 Turn 仍 open。

这段 in-flight conversation 故意不进入 Child Seed。

如果 Child 需要这段信息，Delegation Prompt 应显式传入。

这不是 Context 丢失，而是 Fork Contract。

---

### 16. 应该怎样评价这个 Harness，而不只是评价模型

#### Protocol Correctness

检查：

- Event pairing；
- Turn / Step balance；
- Tool settlement；
- Approval audit；
- Compaction bracket；
- Resume repair。

#### Capability Correctness

检查 Tool、MCP、Skill、Sandbox、Subagent Provider 是否符合各自 Service Contract。

#### Runtime Reliability

做故障注入：

- crash；
- 429 / 500；
- MCP disconnect；
- Sandbox unavailable；
- Persistence fsync failure；
- Plugin unload；
- cancel。

看系统是否 fail closed、可 Resume、无孤儿 Tool Call、无 silent history corruption（静默历史损坏）。

#### Task Utility

最终仍然要回答：

> 这些架构复杂度有没有帮助 Agent 把真实任务做得更好？

所以还要测：

- 任务成功率；
- Token / Cost；
- latency；
- Tool 次数；
- Compaction 后约束保留；
- Subagent delegation 收益；
- 失败恢复后最终正确性。

Runtime Contract 全绿，但模型任务失败，也不能叫优秀 Agent Product。

---

### 17. 从源码能抽出的系统设计原则

**第一，持久化不是最后 dump state，而应该参与运行时语义。** Retry、Approval、Compaction、Subagent identity 都先考虑怎样留下 durable evidence。

**第二，Model Context 最好是 Projection，不必等于原始事实存储。** 这样可以压缩、裁剪、替换模型视图，而不删审计证据。

**第三，Crash Recovery 应该分 Physical Repair 和 Semantic Repair。** Torn file 是 Persistence 问题；Open Turn 是 Agent Protocol 问题。

**第四，Retry 必须建立在明确的幂等 / durable boundary 上。** Raw Stream 和 Durable Step 的可重试性不是一回事。

**第五，多 Agent 不只是 Prompt 分工。** 它还需要 Session lineage、scope isolation、depth / residency limits、continuation ownership。

**第六，Plugin Architecture 要靠 Contract Test 维持。** 没有 invariant / catalog / verifier，大量 extension seam 很快就会漂移。

---

## 7. 源码锚点

1. [`packages/session/session-persistence-jsonl/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/session/session-persistence-jsonl/README.md)：物理持久化、generation、crash tail。
2. [`docs/subsystems/persistence.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/docs/subsystems/persistence.md)：Backend-neutral persistence contract。
3. [`packages/core/session/src/repair.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/session/src/repair.ts)：Interrupted Turn repair。
4. [`packages/core/agent-loop/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/agent-loop/README.md)：Agent Loop 对 persistence write handle / resume 的 ownership。
5. [`packages/llm/llm-retry/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/llm/llm-retry/README.md)：durable-before-wait retry。
6. [`packages/llm/llm-retry/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/llm/llm-retry/src/index.ts)：request-error waterfall / backoff。
7. [`packages/subagent/subagent/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/subagent/subagent/README.md)：Subagent provider seam 与 continuation。
8. [`packages/subagent/subagent-spawn-in-process/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/subagent/subagent-spawn-in-process/README.md)：Fresh child contract。
9. [`packages/subagent/subagent-fork-in-process/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/subagent/subagent-fork-in-process/README.md)：Completed-turn prefix fork。
10. [`packages/subagent/tool-subagent-control/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/subagent/tool-subagent-control/README.md)：send / interrupt / list control surface。
11. [`packages/bundle/base/cordis.patch.yml`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/bundle/base/cordis.patch.yml)：默认产品 wiring。
12. [`package.json`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/package.json)：测试、E2E、benchmark、catalog / architecture gates。
13. [`docs/architecture.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/docs/architecture.md)：Plugin architecture 与事件域。

回到：[DeepSeek Harness 系统总览](README.md)
