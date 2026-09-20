# 04. Codex Engineering & Evaluation｜把入口、执行、持久化、故障和验证重新合成一个系统

[← Tool](03-tool-lifecycle.md) · [Codex 总览](README.md) · [成熟产品源码学习](../README.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

前面三篇故意把 Context（上下文）、Memory（记忆）和 Tool（工具）拆开，是为了看清各自的生命周期。真实 Codex 运行时不会这样分开工作。

一次网络断开可能发生在 Compaction 请求里；一个 Tool Call 可能因为 Guardian（自动风险审查）转给用户批准；一次 Fork（分叉）既要恢复 History（历史），又要恢复当时的设置和 World State（世界状态）；一个 Memory 后台任务还会另外创建内部 Agent。

所以最后一篇重新回到系统问题：

> **当一个 Coding Agent 连续运行很久、会修改真实文件、会接第三方能力、还能恢复和派生子 Agent 时，哪些状态必须由程序守住？出了问题怎样知道该在哪一层恢复？又怎样证明修改以后真的更好？**

---

## 1. 先用“故障属于哪一层”理解 Production Runtime

Codex 的错误类型很多，但没有必要背枚举。真正重要的是：不同故障拥有不同的恢复权。

一次 Stream（模型响应流）断开，通常还可以重试同一 Turn；一个 Tool 参数错误可以作为 observation 返回给模型修改；一个明确被 Permission Policy（权限策略）禁止的动作不能靠重试突破；State DB（状态数据库）损坏和 Internal Agent Died（内部 Agent 循环死亡）则属于更深的 Runtime 故障。

可以先把恢复思路分成四层：

| 故障层 | 典型问题 | 谁更适合决定下一步 |
|---|---|---|
| 模型通信 | Stream 中断、连接失败、Provider 临时过载 | Model Client / Retry Runtime |
| Agent 语义 | Context Window 满、Tool 参数错误、可恢复 Tool Failure | Turn / Compaction / 模型下一步 |
| 权限与执行 | Sandbox 拒绝、网络被策略拦截、用户未批准 | Permission / Approval / Tool Orchestrator |
| Runtime / 持久化 | Thread 不存在、内部 invariant 破坏、数据库 / 任务异常 | Host fail fast、恢复或人工诊断 |

这比统一写一个 `except: retry()` 可靠得多。

---

## 2. 模型 Stream 断开时，Codex 怎样尽量保住同一个 Turn

`responses_retry.rs` 把 Responses sampling（模型采样）和 Remote Compaction（远端压缩）的 Stream Retry（流重试）逻辑集中处理。

如果连接已经建立，但在 `response.completed` 之前断开，错误会先判断是否具有 retry delay（可重试延迟）。在 retry budget（重试预算）内，Codex 等待后重新发送，并向客户端发出 “Reconnecting...” 状态。

这里有两个重要边界。

第一，这是**同一个 Turn 内的通信恢复**，不应该因为一次网络抖动就制造一个新的用户 Turn。

第二，重试必须有次数 / 延迟边界。否则断网以后 Agent 可以无限占用前台，看起来像“还在努力”，实际上什么也没进展。

---

## 3. WebSocket 失败以后，Transport 可以降级但 Agent 语义不必重启

Model Client 支持 Responses WebSocket（响应 WebSocket）路径。如果有限次数的 WebSocket retry 用完，并且当前环境允许 fallback（降级），`ModelClientSession` 可以切到 HTTPS transport（HTTPS 传输）继续请求。

`core/tests/suite/websocket_fallback.rs` 直接覆盖了这个行为。

这说明成熟 Runtime 会把：

~~~text
“用什么网络传输”
~~~

和：

~~~text
“这是不是同一个 Agent Turn”
~~~

分开。

Transport 是实现手段；只要请求可以安全重放，底层通信方式改变不应该自动把整个任务判成失败。

---

## 4. 但不是所有错误都应该 Retry

`CodexErrorDetails` 同时包含 Context Window exceeded（上下文超限）、Tool collision（工具冲突）、Quota（配额）、Policy violation（策略违规）、Sandbox error、Fatal、Internal Agent Died 等类别。

它们的恢复动作完全不同。

Context Window 满应进入 Context Window / Compaction 生命周期；Tool 名冲突是 Registry 配置或能力组合问题，重发模型请求不会自动修好；Quota 用尽和登录失败需要外部状态改变；Policy 拒绝也不能靠增加 retry 次数绕过。

所以可以用一句话概括：

> **Retry 只属于“状态没有本质改变、同一动作再次尝试仍然可能合法成功”的故障。**

恢复权必须由错误语义决定，而不是由“有没有抛异常”决定。

---

## 5. 用户 Cancel（取消）和 Runtime Crash（崩溃）是不同事件

用户按下中断时，系统知道这是一个有意的控制输入。

Tool Runtime 会传播 Cancellation Token，尝试停止仍可安全中止的操作，并把 Aborted Tool Result（中止结果）写回模型历史。Turn 本身也有 Interrupted / Aborted（中断 / 终止）语义。

Runtime Crash 则可能在任意位置打断进程，没有机会优雅补齐所有内存状态。

为什么要区分？

因为 Cancel 可以主动把 History 收束到一个协议合法状态，而 Crash 只能依赖已经持久化的边界恢复。把两者都叫 “failed” 会让恢复算法不知道哪些清理动作已经完成。

---

## 6. Thread Store 解决“未来怎样继续”，不是为了替代所有数据库

`codex-thread-store` 自己把职责定义得很清楚：它是 Codex Thread 的 storage boundary（存储边界）。

对于活动 Thread，`LiveThread` 负责按 Rollout persistence policy（持久化策略）追加 canonical history，再通过明确的 metadata patch（元数据补丁）更新 Thread 元数据。Local Thread Store 用 JSONL Rollout 保存历史；有 State DB 时，查询友好的 Thread metadata 同时进入 SQLite。

`codex-state` 则承载另外一类结构化运行状态：可查询 Thread 元数据、Queue、Goal、Memory Job、部分关系等。

因此不要把架构理解成：

~~~text
JSONL 是旧实现
SQLite 是新实现
~~~

当前源码里它们承担的责任并不相同。

---

## 7. Compaction Checkpoint 是长 Thread 能高效恢复的关键

Context 篇已经解释过 replacement history（替代历史）。从工程角度再看一次：

如果一个 Thread 运行了数周，Rollout 可能非常长。每次 Resume 都从第一行重放，会让启动成本随着历史长度增长。

现代 reconstruction（重建）路径会从 Rollout 尾部反向查找最新仍有效的 CompactedItem（压缩项）。只要它携带 replacement history，就可以把这份历史当作新基线，再 replay（重放）后面的 surviving suffix（仍有效尾部）。

这相当于：

~~~text
很长的执行历史
↓
Compaction
↓
生成新的“可恢复历史基线”
↓
以后 Resume 只需要：
  基线 + 后续增量
~~~

所以 Compaction 同时是 Context 优化和持久化优化。

---

## 8. Resume 和 Fork 的正确性不只看“聊天内容一样”

恢复后的 Thread 还要继续工作，因此真正要恢复的是行为语义。

除了模型 History，重建代码还会处理 previous turn settings（之前的 Turn 设置）、World State baseline、Context Window ID、Token usage（Token 使用）以及 rollback / fork lineage（回滚 / 分叉谱系）等。

可以把正确性目标叫做 Behavioral Resume Equivalence（行为恢复等价）：

> **冷启动恢复以后，模型下一步应该拥有与中断前相容的约束、能力和历史，而不是只看 UI 上的聊天文本能不能显示出来。**

例如 Fork 截止在父 Thread 的第三个用户 Turn，那么第四个 Turn 才获得的 Tool Result 就不能“穿越”到子 Thread。

---

## 9. Queue 和 Goal 说明 Agent Runtime 还有“对话之外的任务状态”

App Server 的 Extension Registry 当前还安装 Queue Extension（队列扩展）和 Goal Extension（目标扩展）。

Queue 支持 durable user-message queue（持久化用户消息队列）和 idle dispatch（空闲时投递）。这让用户的新消息不必强行插进正在执行的 Tool Call 中，可以在合适的运行边界进入后续工作。

Goal Extension 则把更长期的目标状态与 Token accounting（Token 计量）等逻辑作为扩展接入。

这两个例子提醒我们：

> **一个长期 Agent Thread 不是“聊天消息数组 + 一个 while 循环”。**

真正运行时还需要排队、目标、环境、批准、子 Agent 等结构化状态，而且这些状态不一定全部成为自然语言 Prompt。

---

## 10. Multi-Agent 复用了 Thread / Fork / Agent Control，而不是另造第二套 Runtime

Codex 当前 Multi-Agent V2 不是另起一个“Agent 服务”。

`ThreadManager` 可以从父 Thread spawn subagent（派生子 Agent），`AgentRunner` 会在 forked context（分叉上下文）中启动新 Thread 并提交初始 Turn。Agent Control（智能体控制）再负责消息、等待、中断等协作操作。

这样做的一个明显好处是：子 Agent 可以复用已有的 Context、Tool、Permission、Persistence 和 Trace 机制。

代价也很真实。源码 Prompt 明确说明多个 Agent 共享同一目录和文件系统，因此两个 Agent 同时改同一文件并不会因为“它们是两个 Agent”就自动隔离。协作策略、Tool 并发和工作区管理仍然要处理冲突。

---

## 11. Extension Registry 让安全、Memory、Skills 等能力共享生命周期，但不混职责

App Server 当前安装 Guardian V2、Memories、MCP、Skills、Goal、Queue、Web Search、Image Generation 等多个扩展。

它们共享 Thread / Turn / Tool 的生命周期入口，但各自维护 private extension state（扩展私有状态）。比如 Guardian 参与 Approval Review，Memory 贡献 Context 和长期工具，Skills 贡献能力目录，Queue 在 Thread idle（空闲）时尝试派发消息。

这种设计的价值在于：

> **宿主提供稳定时序；扩展只在自己负责的时序点读写自己的状态。**

这比所有功能都直接拿一个全局 Session 对象任意修改，更容易控制依赖和恢复。

---

## 12. Observability（可观测性）有不同层，不能只看一份日志

Codex 同时有 Event、Analytics、OTEL Metrics 和 Rollout Trace。

### Event（事件）

主要服务产品协议和生命周期通知，例如 Turn 开始 / 结束、Tool 事件、Queue / Goal 更新等。客户端需要它们更新 UI 和状态。

### Analytics（分析事实）

把一些行为压成结构化事实。例如 Compaction 会记录 trigger（触发源）、reason（原因）、implementation（实现方式）、phase（阶段）、strategy（策略）、status（结果）和错误类别。

### OTEL / Metrics（OpenTelemetry / 指标）

更适合统计时延、次数、Token、Tool timing、Skill catalog truncation、Memory pipeline 等跨大量请求的数据。

### Rollout Trace（运行轨迹）

这是更重的、显式 opt-in（选择开启）的本地诊断路径。它可以保存模型请求 / 响应、Tool 输入输出、Terminal（终端）行为和多 Agent 边，再离线 reduction（归约）成 semantic graph（语义图）。

这四层分别回答：

~~~text
发生了什么产品事件？
整体指标怎样？
某类行为为什么变多？
这个具体 Bad Case 的真实因果链是什么？
~~~

一份 stdout 日志很难同时做好四件事。

---

## 13. Rollout Trace 的“先观察，后解释”为什么很成熟

`rollout-trace/README.md` 把核心设计概括成：

> observe first, interpret later（先记录事实，再解释语义）。

在线运行时只按顺序写 raw event（原始事件）和 payload reference（载荷引用），尽量不急着判断“这个 Terminal 操作最终属于哪次模型推理”。

之后 offline reducer（离线归约器）再把证据还原成：

- Agent Thread / Turn；
- model-visible Conversation Item（模型可见对话项）；
- Inference Call（模型推理调用）；
- Tool Call；
- Code Cell（代码模式执行单元）；
- Terminal Operation（终端操作）；
- Compaction；
- Multi-Agent interaction edge（多智能体交互边）。

为什么不在线直接构图？

因为 Runtime 里有并发和两个时钟：Tool 可能已经开始执行，但包含它的完整模型 response item 还没有最终写完；子 Agent 的事件也可能稍后才补齐上下文。先保存事实，离线统一解释，更不容易因为到达顺序写出错误关系。

---

## 14. Trace 为什么默认不能当普通 Telemetry 上传

Rollout Trace 可能包含 Prompt、Tool 参数、终端输出、路径和模型响应。这些信息非常适合深度排障，也同样可能敏感。

当前源码明确把它和普通 Telemetry 区分，并且只在配置了相应本地 Trace Root 时写 bundle（轨迹包）。Trace 写入还是 best effort（尽力而为）：诊断记录失败不能让主 Codex Session 因此失败。

这体现一个很实用的系统原则：

> **Observability 是主执行系统的辅助平面；辅助平面故障不能成为用户任务的新单点故障。**

---

## 15. 源码里的 Tests 能证明什么

Codex 的验证不是集中在一个 `evals/` 目录。

每个 crate 有自己的 unit / contract test（单元 / 契约测试），Core 和 App Server 又有大量 integration test（集成测试）。Context 还有 request/history snapshot（请求 / 历史快照），直接检查模型真正看到的内容；WebSocket fallback、Guardian review、Multi-Agent resume、Memory startup、Tool exposure 等都有专门测试。

这些测试非常重要，但要准确理解它们的证明范围：

> **它们主要证明 Runtime 实现符合定义好的协议和不变量，不自动证明“Agent 解决真实用户任务的成功率更高”。**

例如 Tool Search 单测通过，只说明 BM25 索引和返回 shape（结构）符合预期；它不能说明模型在真实一万个工具里一定能选对。

---

## 16. 产品级 Evaluation 需要在源码测试之上再加一层

下面这一节是**基于 Codex 当前源码生命周期设计的课程评测方案**，不是声称 OpenAI 仓库已经公开同名 Benchmark。

一个完整 Agent Eval（智能体评测）至少要同时看四类结果。

### Outcome（最终结果）

代码任务最重要的是环境最终状态：目标测试是否通过、行为是否满足要求、有没有 regression（回归）。最终回答里说“已经完成”不能当作 pass。

### Process（过程）

即使最后成功，也要看是不是重复读同一文件、反复调用失败工具、无意义触发多次 Compaction，或在网络故障时过度 Retry。

### Safety（安全）

是否绕过 Approval、越出 Sandbox、错误使用网络、把用户没有批准的副作用执行了。

### Resource（资源）

Input / cached tokens、模型调用次数、Tool Call 数、时延、TTFT（首 Token 延迟）、Memory 深读次数等。

四类指标共同解释“系统是不是变好”，而不是最后合成一个没有原因的总分。

---

## 17. Context 应该怎样做任务级评测

### 【源码已经提供的基础】

Context / Compaction / Resume 有大量 integration tests 和 snapshots，可以验证 History shape、Window 切换、请求设置、恢复等实现契约。

### 【课程评测推导】

进一步可以构造 Constraint Retention（约束保留）任务：在长任务开头写入“不能改公开 API”，经过多轮 Tool 和一次 Compaction 后检查最终代码是否仍遵守。

还可以做 Compaction Equivalence（压缩等价）：

~~~text
同一任务 A
不触发 Compaction

同一任务 B
在固定位置触发 Compaction
~~~

比较之后的最终行为，而不是比较摘要文字是否相同。

Resume Equivalence（恢复等价）则把同一任务分别连续运行和中途退出 / Resume，观察下一步 Tool、权限、最终结果是否仍相容。

这些评测直接对应源码里最容易出错的状态转换。

---

## 18. Memory 应该怎样做任务级评测

Memory 的 Recall Rate（召回率）高并不等于好。

更合理的测试要覆盖：

~~~text
Thread A：用户明确长期偏好
Thread B：应正确使用
Thread C：用户纠正
Thread D：旧偏好不得复活
~~~

然后区分：

- extraction precision（提取精确率）；
- over-generalization（过度泛化）；
- correction compliance（纠错遵从）；
- stale-memory failure（陈旧记忆导致的失败）；
- Memory ON / OFF 的任务效果差异。

如果一个系统每次都能“召回很多历史”，但频繁把一次性约束误当永久偏好，召回率越高可能反而越糟。

---

## 19. Tool / Skill 应该怎样做任务级评测

Tool 需要拆开看 discovery（发现）、selection（选择）、argument（参数）、execution（执行）和 result reuse（结果利用）。

例如 Deferred Tool Search 可以测 Recall@K：正确 Tool 是否进入前 K 个候选；模型真正选择后再测参数是否合法、Runtime 是否正确要求 approval、执行后模型有没有把失败结果误认为成功。

Skill 还多一个层级：正确 Skill 是否在 metadata catalog（元数据目录）中被模型识别；真正选中后，是否只读取必要的 `SKILL.md` 和 reference，而不是把所有 supporting resources 全塞进 Context。

这些测试应该随着 Tool / Skill catalog 规模增长逐步做压力实验，而不是只在两个工具的 Demo 上确认“Function Calling 能工作”。

---

## 20. 大 Context、数万 Tool、上万 Skill：哪些是源码事实，哪些是工程外推

上一版把这些场景和 Codex 当前实现写得太接近，容易产生“Codex 已经按这个规模部署”的误读。这里明确分开。

### 【当前源码事实】

Codex 已经存在：

- Context 增量更新和有界注入；
- 多种 Compaction / Context Window 路径；
- Prompt Cache 友好的稳定前缀设计；
- Deferred Tool + BM25 search；
- MCP Spec hard budget；
- Skill metadata budget + progressive disclosure；
- Memory top-N consolidation + bounded summary；
- checkpoint-based resume（基于检查点的恢复）。

这些机制都在控制“大量信息不能直接全给模型”的问题。

### 【工程推导】

如果未来面对 1M Token Context、五万个 Tool、一万个 Skill，可以继续沿这些机制扩展：更强的分层检索、索引缓存、Policy pre-filter、semantic rerank（语义重排）、更细的 Context budget 和压力评测。

但源码没有告诉我们“当前生产 Codex 就以五万个 Tool / 一万个 Skill 运行”，所以这里不把规模数字当产品事实。

---

## 21. 一个 Bad Case（真实失败案例）应该怎样从 Trace 走回改进

假设线上出现：

> Codex 连续三次运行同一个失败测试，最后还告诉用户“已经修复”。

先别急着改 Prompt。

用 Trace / Rollout 可以问：

第一次 Tool Result 是否真的记录了非零 exit code？第二次模型请求里是否看见？Tool 输出有没有被过度截断？模型是否误读了结果？是否存在 Goal / Plan 让它无条件继续 Retry？最终 Eval 为什么没有通过真实测试来判结果？

Root Cause（根因）可能分别在 Tool、Context、Planning 或 Eval Harness。

修复以后，再把这条真实 Bad Case 和几个相似变体放进 regression eval（回归评测）。

这样才形成：

~~~text
真实失败
→ Trace 找到因果链
→ 定向修复
→ 回归评测
→ 再发布
~~~

这比“感觉新 Prompt 更聪明”更接近成熟 Agent Engineering。

---

## 22. Codex 源码最值得带走的系统边界

把整个仓库重新读一遍以后，可以看到一个反复出现的模式：

需要概率语义判断的事情，Codex 可以交给模型，例如代码理解、下一步动作、Memory extraction、Memory consolidation 和某些 Compaction summary。

必须保持一致和安全的事情，则留给 Runtime，例如 Thread identity、Step snapshot、Tool Router、Permission、Sandbox、Job lease、Context checkpoint、Retry count、call/result pairing 和持久化。

可以用一句话概括：

> **模型负责“判断什么更合适”，Runtime 负责“哪些事实不能乱、哪些边界不能越、失败以后怎样知道自己还在哪”。**

这比“Agent = LLM + Tools”更接近当前 Codex 源码真正展示的系统。

---

## 23. 面试时怎样用源码解释，而不是背产品名词

如果面试官问“一个成熟 Coding Agent Runtime 怎样设计”，可以从真实链路回答：

~~~text
我会先把产品入口和 Agent Core 分开。
以当前 Codex 源码为例，TUI 通过 App Server 的类型化 RPC 创建或恢复 Thread，
ThreadManager 管长期 Thread，Turn 管一次用户任务，
每次模型采样前再捕获 StepContext，把当时的模型设置、环境、MCP 和 ToolRouter 固定在同一版本。

Context 不是每轮重拼全部历史，而是初始 full baseline + WorldState diff + canonical history；
长对话通过 Compaction 产生 replacement-history checkpoint，ThreadStore 持久化以后 Resume 从最新有效 checkpoint + suffix 重建。

Tool 也不是所有能力全塞模型。
Registry 保存 Host 能力，Router 决定 Direct / Deferred / CodeMode；
MCP 可以通过 BM25 tool_search 按需加载，真正执行还经过 Hook、Approval Review、Sandbox、Network 和并发控制。

Memory 是独立后台两阶段 pipeline：
先按 Thread 提取，再串行 consolidation；
新 Thread 先注入 bounded summary，需要证据时才深读历史；
显式纠错通过 append-only note 进入下一次 consolidation。

最后用 Events / Metrics / Rollout Trace 查运行事实，
源码测试验证协议和不变量，任务级 Eval 再验证真实代码结果、安全和成本。
~~~

这段回答有价值的地方不是“Codex 很先进”，而是每一步都能落回真实源码对象和时序。

---

## 24. 源码核验入口

- [`core/src/responses_retry.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/responses_retry.rs)：模型 Stream retry 与 transport fallback。
- [`protocol/src/error.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/protocol/src/error.rs)：Codex / Sandbox 错误语义。
- [`thread-store/README.md`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/thread-store/README.md)：Thread Store 的持久化责任。
- [`state/src/lib.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/state/src/lib.rs)：SQLite 状态层的责任边界。
- [`core/src/session/rollout_reconstruction.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/session/rollout_reconstruction.rs)：checkpoint、rollback 与 Resume 重建。
- [`thread-store/src/local/model_context.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/thread-store/src/local/model_context.rs)：Local Store 怎样反向扫描最新模型上下文。
- [`app-server/src/extensions.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/app-server/src/extensions.rs)：当前产品实际安装哪些运行时扩展。
- [`core/src/thread_manager.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/src/thread_manager.rs)：Thread 创建、恢复、Fork 与 Subagent。
- [`ext/agent/src/lib.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/agent/src/lib.rs)：派生 Agent 怎样启动自己的 Thread / Turn。
- [`rollout-trace/README.md`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/rollout-trace/README.md)：本地诊断 Trace 与离线语义图。
- [`analytics/src/facts.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/analytics/src/facts.rs)：结构化 Analytics facts。
- [`core/tests/suite/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/core/tests/suite) 与 [`app-server/tests/suite/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/app-server/tests/suite)：跨模块 Integration Tests。

回到：[Codex 系统总览](README.md)
