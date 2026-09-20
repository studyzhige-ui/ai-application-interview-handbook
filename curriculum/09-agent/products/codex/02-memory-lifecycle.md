# 02. Codex Memory Lifecycle｜过去的 Thread 怎样变成未来可用、可纠错的长期记忆

[← Context](01-context-lifecycle.md) · [Codex 总览](README.md) · [Tool →](03-tool-lifecycle.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

Memory（记忆）很容易被讲成“把对话做 Embedding（向量嵌入）后存进向量数据库”。Codex 当前源码并不是这条路线。

它把 Memory 做成一个独立的长期流水线：从旧 Thread 的 Rollout（运行记录）里挑候选，用模型做第一阶段提取；再把多个历史 Thread 的结果交给第二阶段做全局整理；新 Thread 只先看到一份有界 summary（摘要），真正需要证据时再去搜索和读取对应 rollout summary。用户如果明确说“记住”“忘掉”或“改正”，也不会让模型直接手改生成文件，而是追加一条 correction note（纠错备注），等待后续 consolidation（整合）统一吸收。

这一篇先从一个具体问题开始：

> 用户今天说“以后给我的技术总结先写结论，再写依据”。明天开启另一个 Thread，Codex 怎么可能还知道这件事？如果用户后天又改口，它又怎样避免继续使用旧偏好？

---

## 1. 先把 Thread History 和 Memory 分开

Codex 本来就能持久化 Thread History（线程历史）。如果“持久化历史 = 长期记忆”，那根本不需要独立 Memory 子系统。

区别在于用途。

Thread Store / Rollout 保存的是一次 Thread 中真正发生过的消息、工具调用、上下文转换等事实，主要服务 Resume（恢复）、Fork（分叉）和历史读取。

Memory 则要从很多过去的 Thread 中回答：

> **哪些内容值得在未来其他任务里继续影响模型？**

所以一个失败测试产生的几千行日志可以属于 History，却通常不应该直接成为长期 Memory。相反，用户明确纠正的长期工作偏好即使只出现一句话，也可能很值得保留。

这就是 Codex 为什么需要“提取 → 全局整理 → 有界召回”，而不是每次把所有旧 Thread 重放给新模型。

---

## 2. Memory 流水线真实从哪里触发

这里需要先修正上一版文档，也需要修正源码仓库自己一处已经滞后的 README。

`codex-rs/memories/README.md` 仍然写着 Phase 1 / Phase 2 的 orchestration（编排）位于 `codex-rs/core/src/memories/`。但本次固定 commit 的完整源码树里并没有这个目录。

当前真实调用点在：

`codex-rs/app-server/src/request_processors/turn_processor.rs`

在有用户输入的 Turn 成功启动以后，如果当前 Thread 已经配置 primary environment（主执行环境），App Server 会调用：

`codex_memories_write::start_memories_startup_task(...)`

进入这个函数以后还要再通过自己的 guard（门槛）：ephemeral session（临时会话）不会生成长期记忆，Memory feature 未启用不会运行，非 root agent（非根 Agent）也会跳过；State DB 不可用时同样停止。之后还会检查 Memory 根目录和速率限制。

所以准确的时序是：

~~~text
有输入的 Turn 成功开始
↓
App Server 尝试启动 Memory background task（后台任务）
↓
Memory 自己检查：
  是否临时会话？
  功能是否开启？
  是否根 Agent？
  State DB 是否可用？
  当前速率限制是否允许？
↓
通过后才执行 Phase 1 → Phase 2
~~~

它是**由真实用户工作顺带触发的异步后台生命周期**，而不是每个模型 Step 都同步跑一次，也不是“进程一启动就无条件总结所有历史”。

---

## 3. 为什么 Memory 要异步做，而不是阻塞当前回答

假设用户只是要修一个测试。如果 Codex 每次开始 Turn 都要先把过去几十个 Thread 重新总结一遍，用户等待时间和模型成本都会被 Memory 拖住。

当前实现把它放到独立后台 task（任务）里。Memory 失败也不应该让当前编码任务失败。

这体现了一个重要边界：

> **Memory 是长期质量增强平面，不是当前 Turn 正确执行的同步事务。**

当然，这也意味着 Memory 需要自己的 Job（作业）状态、重试、并发控制和持久化，不能靠“当前 Turn 内一个变量”管理。

---

## 4. Phase 1 先做候选选择，再调用模型

Phase 1（第一阶段）不是把整个用户历史库一股脑发给模型。

`MemoryStore::claim_stage1_jobs_for_startup` 会先从 State DB 中寻找值得处理的旧 Thread。源码要求候选 Thread 已启用 Memory，属于允许的交互来源，不是当前正在运行的 Thread，并且更新时间落在配置的年龄与 idle（空闲）窗口内。

还有两个非常现实的限制。

第一，扫描是有上限的。一次启动只检查和 claim（领取）有界数量的候选，避免历史越多、每次启动数据库扫描越重。

第二，每个候选要先拿 lease（租约 / 所有权令牌）。如果两个 Codex 进程几乎同时启动 Memory pipeline，它们不能重复花模型调用去总结同一份历史。

可以把 Phase 1 的前半段理解成：

~~~text
很多历史 Thread
↓
先用数据库规则过滤
↓
只留下“最近、有价值可能、已经空闲”的候选
↓
领取有限数量 Job
↓
真正进入模型提取
~~~

这比“每次都让 LLM 判断所有历史值不值得记”更便宜，也更可控。

---

## 5. Phase 1 的模型看到的也不是完整 Rollout

一个 Coding Agent 的 Rollout 里可能有：

- 多次文件读取；
- 大段终端输出；
- 工具参数；
- 中间错误；
- 重连事件；
- 无关运行元数据。

如果原封不动全塞给 Memory Extractor（记忆提取模型），Memory 会再次被运行噪声淹没。

Phase 1 会先读取 Rollout Item（运行记录项），再根据 Memory 版本做过滤和有界序列化。V2 路径还会根据模型信息计算 rollout token limit（历史输入 Token 上限），形成 tiered input（分层输入）。

因此这里已经出现第一层“记忆压缩”：

> **不是把过去所有字节保存得更久，而是先筛出适合做长期语义判断的证据。**

---

## 6. Phase 1 真正要提取的是什么

提取模型的职责不是写一段“这次会话聊了什么”的漂亮摘要，而是把一个 Thread 中未来可能复用的信息整理成结构化结果。

当前输出包括 detailed raw memory（详细原始记忆）、compact rollout summary（紧凑的会话摘要）以及可选 slug（短标识）。生成结果还会经过 secrets redaction（秘密信息脱敏），再写入 Memory DB 的 Stage 1 output（第一阶段输出）。

这里最容易犯的错误是**过度泛化**。

例如用户说：

> “这次修复不要动数据库。”

这句话当然是本次任务的重要约束，但不能自动升级成：

> “这个用户永远不允许修改数据库。”

因此 Memory Prompt 会强调 user instruction（用户指令）、assistant assumption（助手推测）、tool evidence（工具证据）等来源差异。长期偏好必须有真实用户证据和合适作用域。

---

## 7. Phase 1 为什么允许“成功但没有输出”

不是每个历史 Thread 都值得留下长期信息。

如果模型正常完成判断，但没有产生有价值的 raw memory，Codex 会把它记为 `succeeded_no_output（成功但无长期输出）`，而不是把它当系统错误。

这一点很重要。否则“Memory 功能已开启”会变成一种错误压力：

> 每次聊天都必须编出点东西存下来。

成熟 Memory 的质量很大程度取决于**敢不敢不记**。

真正的失败则会进入 Job 的 failure / retry backoff（失败与退避重试）机制，避免启动时不断热循环。

---

## 8. Phase 1 可以并行，Phase 2 为什么必须全局串行

不同历史 Thread 之间的提取相对独立，所以 Phase 1 使用有并发上限的 parallel sampling（并行采样）。这可以同时处理几份旧 Rollout。

Phase 2（第二阶段）做的事情完全不同：它要维护**全局 Memory workspace（记忆工作区）**。多个 worker 如果同时修改同一份 `memory_summary.md`、`rollout_summaries/` 和其他记忆文件，很容易互相覆盖。

所以 Phase 2 先领取一个 global job（全局作业）并持续 heartbeat（续租心跳）。只有一个 consolidation worker 能在同一时刻更新共享 Memory 基线。

这就是两阶段拆分的核心原因：

~~~text
Phase 1
很多 Thread 各自提炼
→ 适合并行

Phase 2
把这些结果合成同一份长期视图
→ 必须协调全局一致性
~~~

---

## 9. Phase 2 选哪些记忆，不只是看“最新”

Memory DB 会记录 Stage 1 output 的使用情况。

当后续回答真正引用某个过去 Thread 的 Memory 时，`record_stage1_output_usage` 会给对应记录：

~~~text
usage_count += 1
last_usage = 当前时间
~~~

Phase 2 选择全局输入时，会先排除已经太久没有使用、也不够新的记录，再优先考虑 usage count（使用次数）更高和 recency（近期性）更好的 Memory。

这里有一个需要按代码而不是 README 理解的细节：当前 `get_phase2_input_selection` 在 `last_usage` 为空时使用 `source_updated_at` 作为新鲜度依据。源码 README 的文字仍提到 `generated_at`，两者存在偏差；本教材采用当前执行代码的 `source_updated_at` 行为。

这条反馈链非常值得学习：

~~~text
过去 Thread
→ 被提炼成 Memory
→ 新任务真的用到了它
→ 记录 usage
→ 后续 consolidation 更愿意保留它
~~~

长期记忆因此不只是“写入时打一个重要性分数”，还会被真实使用反馈重新排序。

---

## 10. 为什么 Phase 2 要把数据库结果同步成文件工作区

Phase 2 不直接让 consolidation model（整合模型）读数据库表。

它会把当前选中的 Stage 1 outputs 同步成一套本地文件：

`raw_memories.md` 保存合并后的详细原始记忆，`rollout_summaries/` 为每个选中 Thread 保存一份摘要。已经不在当前 selection（选择集）里的旧摘要会被清理。

这样做的意义不是“Markdown 比 SQL 更高级”，而是为后续整理提供一个稳定、可检查、可做 diff（差异比较）的工作区。

更关键的是，这个 Memory 根目录本身还维护一个 Git baseline（Git 基线）。

---

## 11. Git 在 Memory 里不是版本管理 UI，而是“变化探测器”

Phase 2 每次把新的选择集同步到文件系统以后，会计算相对**上一次成功 consolidation** 的 Git-style diff（Git 风格差异），并写入 `phase2_workspace_diff.md`。

如果没有任何变化，就不需要再调用一个模型去“重新整理一遍同样的 Memory”，Job 可以直接成功结束。

如果有变化，才启动内部 consolidation Agent。

所以 Git baseline 解决的是：

> **“全局 Memory 从上一次成功状态到现在到底变了什么？”**

这比单看一个数据库 watermark（水位）更可靠，因为变化不只有“新增一条记录”。某条旧 Memory 可能被淘汰，某个 correction note 可能被加入，某个扩展资源也可能被删除；这些都能自然反映在文件 diff 里。

---

## 12. Phase 2 的内部 Agent 权限反而更窄

Consolidation 需要语义判断：重复信息怎样合并、用户纠正怎样覆盖旧结论、哪些工作经验值得留下。因此使用模型 / Agent 是合理的。

但“内部 Agent”不等于“系统自己人，所以全权限”。

当前实现会把它限制在 Memory 工作区：不走普通用户审批交互、不开放网络，只允许本地受限写入，还会关闭 collaboration（协作），避免 consolidation Agent 再递归创建更多子 Agent。运行期间 Job lease 还需要持续 heartbeat。

这里体现了 Codex 很稳定的一条设计思想：

> **LLM 负责需要语义判断的部分，Runtime 负责把它关在可验证的边界里。**

---

## 13. 模型说“整理完成”以后，Runtime 还会验收文件

Phase 2 成功不能只看 Agent 的最终自然语言回答。

`workspace.rs` 会验证 consolidation artifacts（整合产物）。例如会检查 Memory workspace 里不能留下 symbolic link（符号链接）绕过目录边界；对应 Memory 版本还要有规定的 summary artifact（摘要文件）和结构。

V2 的 `memory_summary.md` 当前还要求小于 10,000 bytes，并包含固定 section，例如 User Profile（用户概况）、User preferences（用户偏好）、General Tips（通用经验）和 What's in Memory（记忆索引）。

只有产物合法，新的工作区才会成为成功 baseline。

这与 Coding Agent 交付代码时“最终回答说测试通过”不能代替真的跑测试，是同一个原则。

---

## 14. 用户明确说“记住 / 忘掉 / 改正”时，不走普通自动提取

自动 Phase 1 适合从过去任务中提炼信息，但用户明确修改 Memory 时，信号强度更高。

Memory read prompt（记忆读取提示）明确规定：只有用户显式要求 remember（记住）、forget（忘掉）或 correction（纠正）时，才更新长期 Memory。V2 使用 append-only ad-hoc note（只追加的临时记忆备注），路径位于：

`extensions/ad_hoc/notes/`

例如用户说：

> “别再记我偏好 pytest；以后这个项目按仓库现有测试框架来。”

Runtime 不让模型直接打开 `memory_summary.md` 找一句话删掉，而是新增一条小 correction note。下一次 Phase 2 从 workspace diff 看到这条修改，再统一整合。

为什么绕一圈更安全？

因为直接编辑全局 summary 会让一次局部修改有机会误删其他无关 Memory。Append-only note 则保留了“用户什么时候提出了什么纠正”的来源，整合过程也有明确 diff。

---

## 15. 新 Thread 怎样真正“想起”过去

Memory Extension（记忆扩展）会在 Context assembly（上下文编排）阶段参与 Thread Context。

它读取对应 Memory root 下的 `memory_summary.md`，先做有界 truncation（截断），再把 summary 和 Memory 使用说明渲染成 developer-policy context。

所以新 Thread 的第一层 Recall（召回）不是：

~~~text
用户问一句
→ 立刻向量检索所有历史
~~~

而是：

~~~text
加载一份已经全局整理过的短 summary
→ 先用它理解用户长期偏好和过去工作范围
~~~

这让最常用的长期信息以低成本进入 Context。

---

## 16. Summary 不够时，才进入更深的 Evidence Recall

V2 read prompt 对这一点写得很清楚：

> 如果 rollout summary 中的额外证据、原话、时间顺序或不确定性可能改变答案，就读取匹配的 summary；否则不要为了“看看历史”而投机性检索。

Memory Extension 还提供 search / list / read（搜索 / 列表 / 读取）等工具。模型可以先搜索相关文件，再只打开必要行，而不是一次读完全部 Memory corpus（记忆语料）。

因此 Recall 更像分层展开：

~~~text
第 1 层：memory_summary
已经整理过的高密度长期上下文

第 2 层：search / list
定位可能相关的历史 Thread

第 3 层：read
只读取真正需要的证据窗口
~~~

这和 Skills 的 progressive disclosure（渐进式展开）是同一种 Context 控制思想。

---

## 17. Memory 不是当前事实数据库

read prompt 还有一句非常重要：

> Memory is not proof of current behavior.

也就是说，过去 Thread 里曾经成立的事实，不应因为进了 Memory 就永远当成当前事实。

例如 Memory 记录“项目 CI 使用 Python 3.12”，几个月后仓库可能已经升级到 3.14。对会变化、后果重要的事实，Agent 仍然应该根据核验成本和风险决定是否回到真实 source（来源）确认。

长期 Memory 更像：

> **帮助模型快速定位过去经验和用户长期意图的历史上下文。**

它不是替代 Git、配置文件、线上系统或外部 API 的权威状态库。

---

## 18. 为什么 Memory Citation 会反过来改变未来 Memory

当模型真正读取一个 rollout summary 并用它回答时，最终可以输出 Memory Citation（记忆引用），其中包含实际使用的文件行范围以及相关 rollout / thread ID。

`memories/read/src/citations.rs` 会解析这些 ID，之后 Memory Store 可以把对应 Stage 1 output 的 `usage_count` 和 `last_usage` 更新。

所以引用不只是给用户看的“出处装饰”。

它还形成一个产品反馈：

~~~text
模型使用了哪段过去经验
→ Runtime 能识别对应 Thread
→ 记录真实使用
→ 后续 Phase 2 selection 调整
~~~

这是一条从 Recall 回到 Retention（保留策略）的闭环。

---

## 19. 遗忘不是“删掉数据库一行”这么简单

如果某个 Stage 1 output 已经被 Phase 2 合并进当前 `memory_summary.md`，只删除数据库行并不会自动把 summary 中的结论擦掉。

源码因此存在多条维护路径。

长期未使用、又不在当前成功 baseline 中的 Stage 1 output 可以按 retention window（保留窗口）批量 prune（清理）。

删除某个 Thread 的 Memory 时，如果它曾参与当前 Phase 2 baseline，会重新 enqueue（入队）全局 consolidation，让生成文件有机会真正删除对应内容。

还有 `mark_thread_memory_mode_polluted` 等污染路径，用于在来源不再适合继续贡献 Memory 时触发后续整理。

所以正确理解是：

> **“从候选数据库移除”只是遗忘的一半；如果信息已经进入全局生成产物，还要让 consolidation 重写全局视图。**

---

## 20. Memory Version 和 Dual Write 说明它已经是持久数据系统

当前 `start_memories_startup_task` 支持不同 `MemoryVersion`，配置还可以开启 dual write（双写）。

为什么一个 Prompt 功能需要版本？

因为长期 Memory 一旦写到磁盘和数据库，升级数据布局、Prompt schema（提示结构）或读取规则就不能假设所有旧用户在同一秒重新生成全部历史。

版本和双写允许新旧路径在迁移期并存，观测新实现是否稳定，再逐步切换读取侧。

这说明 Codex Memory 已经不只是“当前请求的一段 Prompt 技巧”，而是一个需要数据迁移语义的长期状态系统。

---

## 21. Memory 安全风险主要来自“错误会跨 Thread 活很久”

普通 Prompt Injection（提示注入）也许只污染一次回答；错误 Memory 一旦被 consolidation 接纳，可能影响未来很多 Thread。

因此写侧和读侧都需要边界。

Phase 1 把 Rollout、Tool Output 和外部内容当 evidence（证据），而不是新的高优先级指令；生成字段还会做 secret redaction（秘密脱敏）。

Phase 2 的 Agent 被限制网络和写入范围，工作区还拒绝 symlink（符号链接）越界。

读侧又明确告诉模型 Memory 不是当前事实证明，只有用户显式要求时才更新长期 Memory。

这些机制共同解决的不是“模型会不会总结”，而是：

> **一个历史错误能不能被提升成长期权威。**

---

## 22. 源码已经提供哪些 Memory 可观测信号

Codex 已经有 Memory startup、Phase 1 / Phase 2 Job、耗时、Token 使用、存储规模等 metrics（指标），读侧也能分类模型是否读取了 summary、raw memories、rollout summaries 或 Memory Skills。

更重要的是，State DB 还有 `usage_count` / `last_usage` 这种与真实 Recall 绑定的反馈。

这些源码指标可以帮助回答：

- Memory pipeline 是否在正常运行？
- Phase 1 是否经常失败或没有输出？
- Phase 2 是否频繁运行但几乎没有变化？
- 模型是在只用 summary，还是大量深挖历史？
- 哪些过去 Thread 真的被后续任务反复使用？

但它们还不能自动证明“Memory 让用户任务更成功”。这属于产品级 Eval（评测），会在第 04 篇单独区分。

---

## 23. 基于源码设计评测时，哪些是事实，哪些是推导

### 【源码已有验证】

当前仓库有 Memory startup tests、Phase 1 / Phase 2 tests、workspace / sandbox tests、read path tests 和 metrics。它们验证 Job 协调、文件产物、权限边界、选择逻辑等实现 contract（实现契约）。

### 【课程基于源码的评测推导】

如果要评估 Memory 是否真的提升 Agent，应另外构造跨 Thread 任务：

~~~text
Thread A
用户明确一个长期偏好

Thread B
检查是否正确使用

Thread C
用户纠正偏好

Thread D
检查旧信息是否被遗忘
~~~

再测 extraction precision（提取精确率）、过度泛化、correction compliance（纠错遵从）、stale-memory failure（陈旧记忆导致的失败）、Memory ON/OFF 的任务成功率差异。

这些是根据源码生命周期设计的评测方法，**不是声称当前 Codex 仓库已经内置了这样一套公开 Benchmark（基准测试）**。

---

## 24. 用用户偏好的例子串起完整闭环

回到开头：

> “以后给我的技术总结先写结论，再写依据。”

可能经历：

~~~text
Thread A 中用户明确表达
↓
之后某次 Memory startup 选中 Thread A
↓
Phase 1 提取为有 provenance 的长期候选
↓
Phase 2 将它合入全局 memory_summary
↓
Thread B 启动，Memory Extension 注入 summary
↓
模型按偏好组织总结
↓
若需要确认来源，读取 Thread A rollout summary
↓
引用产生 usage feedback
~~~

几天后用户说：

> “改一下，以后代码审查报告先列问题，普通技术总结仍然先结论。”

则：

~~~text
显式 correction
↓
append-only ad-hoc note
↓
Phase 2 workspace diff
↓
Consolidation 重新整理作用域
↓
未来 Thread 使用新规则
~~~

这条链比“存进向量数据库 → 下次检索”多得多，但也正是长期 Memory 真正难的地方。

---

## 25. 源码核验入口

1. [`app-server/src/request_processors/turn_processor.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/app-server/src/request_processors/turn_processor.rs)：当前真实 Memory startup 调用点。
2. [`memories/write/src/start.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/start.rs)：eligibility gate、后台任务、版本与 Phase 顺序。
3. [`memories/write/src/phase1.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/phase1.rs)：候选 Job、并行提取、输出与失败。
4. [`state/src/runtime/memories.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/state/src/runtime/memories.rs)：lease、usage feedback、Phase 2 selection、retention 与删除。
5. [`memories/write/src/phase2.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/phase2.rs)：全局 consolidation 与 heartbeat。
6. [`memories/write/src/storage.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/storage.rs)：raw memories 与 rollout summaries 同步。
7. [`memories/write/src/workspace.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/workspace.rs)：Git baseline、workspace diff 和产物验证。
8. [`ext/memories/src/extension.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/memories/src/extension.rs)：Memory 怎样接入 Context 与 Tools。
9. [`ext/memories/templates/memories/read_path_v2.md`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/memories/templates/memories/read_path_v2.md)：当前 V2 Recall / citation / correction 规则。
10. [`memories/read/src/citations.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/read/src/citations.rs)：引用怎样映射回历史 Thread。

下一篇：[Codex Tool Lifecycle →](03-tool-lifecycle.md)
