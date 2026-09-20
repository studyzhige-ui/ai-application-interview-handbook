# 02. Codex Memory Lifecycle｜过去的 Thread 怎样变成未来可用的长期记忆

[← Context](01-context-lifecycle.md) · [Codex 总览](README.md) · [Tool →](03-tool-lifecycle.md)

> **源码基线：** `openai/codex@5c5308fc9a9ee789049d646ef11e5400384b9c6f`

如果把 Memory（长期记忆）理解成“把聊天记录存起来，以后做向量检索”，会完全看不懂 Codex 当前源码。

Codex 已经把长期 Memory 做成了独立子系统。它不是 Thread History（线程历史）的别名，也不是 Context（当前模型上下文）的另一种叫法。

先看三块最核心的代码：

- `codex-rs/memories/write/`：负责从旧 Thread 生成和整理长期记忆；
- `codex-rs/memories/read/`：负责读取、引用和使用情况统计；
- `codex-rs/ext/memories/`：把 Memory 接入 Codex Runtime，让模型真正能看到和查询这些记忆。

再加上：

- `codex-rs/state/src/runtime/memories.rs`：保存 Memory job（记忆任务）、阶段产物、使用次数和保留状态。

所以 Codex 的 Memory 生命周期更接近：

```text
过去的 Thread
→ 判断是否值得进入记忆提取
→ 单 Thread 提取
→ 全局整理
→ 生成有界长期摘要
→ 新 Session 注入
→ 按需继续搜索证据
→ 记录哪些记忆真的被用到
→ 用户纠正 / 遗忘
→ 下一轮整理更新长期基线
```

下面沿这条链讲。

---

## 1. 为什么 History 不能直接当 Memory

假设用户过去有 300 条 Codex Thread。

如果下一次新任务开始时，把 300 条 Thread 的完整历史都重新塞进 Context，会立刻遇到几个问题：

- 大量过去任务与当前问题无关；
- 同一个偏好可能被重复表达很多次；
- 旧事实可能已经过期；
- 用户后来可能纠正过前面的说法；
- Tool Log（工具日志）和中间失败会占用大量 Token；
- Prompt Injection（提示注入）甚至可能被长期带进新任务。

因此 Codex 把“原始历史”和“未来可复用知识”分开。

可以这样理解：

```text
Thread History
= 当时发生过什么

Memory
= 从过去历史中提炼出的、未来可能仍有价值的信息
```

Thread History 主要服务 Resume（恢复）、Fork（分叉）和审计；Memory 主要服务跨 Thread 的复用。

这两个系统可能引用同一段过去事实，但它们的目的不同。

---

## 2. Memory 什么时候开始工作：先选候选 Thread，而不是先叫模型总结

Memory write pipeline（记忆写入流水线）不会在每次 Turn 结束后立刻总结。

启动逻辑主要在：

- `codex-rs/memories/write/src/start.rs`
- `codex-rs/state/src/runtime/memories.rs`

当前源码会先判断这个 Session 是否适合做 Memory 工作。例如普通 root session（根会话）和 durable session（可持久化会话）才有意义；临时 Session 或普通子 Agent 不应该随便把自己的过程写进长期用户记忆。

接着，State DB（状态数据库）会从历史 Thread 中挑候选。

这里最重要的不是某个 SQL 字段，而是它解决了三个工程问题。

### 第一，不能每次全库扫描

如果用户已经有很多 Thread，Memory startup（记忆启动任务）不能每次都遍历所有历史。

所以源码有 scan limit（扫描上限）和 max claimed（最多领取任务数），先把候选范围限制住。

### 第二，刚结束的 Thread 不一定适合马上总结

代码会考虑 Thread 的更新时间和 idle（空闲）时间。

原因很自然：一个还在频繁变化的 Thread，今天总结一次，几分钟后又变了，会造成重复提取。

### 第三，同一份历史不能被多个 worker 重复总结

Memory job 有 ownership token / lease（所有权令牌 / 租约）。

如果多个 Codex 进程同时启动，都发现 Thread A 需要生成记忆，没有 lease 就会同时调用模型做同一份工作。

因此真正流程是：

```text
从 State DB 找到候选 Thread
        ↓
确认它比已有 Memory 更新
        ↓
领取带 lease 的 Phase 1 job
        ↓
只有成功拿到 ownership 的 worker 才继续
```

这已经说明 Codex Memory 不是“调用一次 summary prompt”，而是一个可并发运行的后台数据处理系统。

---

## 3. Phase 1 做什么：把一条过去 Thread 压成可整理的记忆证据

Phase 1（第一阶段）主要实现位于：

- `codex-rs/memories/write/src/phase1.rs`
- `codex-rs/memories/write/templates/memories/stage_one_system_v2.md`
- `codex-rs/memories/write/templates/memories/stage_one_input_v2.md`

它处理的是“一条 Thread”。

但它并不是简单：

```text
把整条 rollout 发给模型
→ 请总结
```

因为一条 Coding Agent 历史里通常有很多噪声：重复文件读取、测试日志、中间猜测、Tool Call、失败重试、临时计划、终端输出。如果全部原样交给 Memory Extractor（记忆提取模型），它只会把 Context 再浪费一次。

所以 Phase 1 的任务本质是：

> **从一条过去任务的执行证据里，区分哪些东西可能值得跨 Thread 保存，哪些只是当时执行过程中的噪声。**

### 它特别关心什么

从当前 V2 Prompt 可以看出，Codex 希望保留的是：

- 用户明确说过的要求；
- 用户后来做出的纠正；
- 用户作出的稳定决定；
- 项目中已经确认的约束；
- 对未来任务可能有帮助的工作方式；
- 任务最后真正发生了什么；
- 哪些问题仍没有解决；
- 这些结论来自哪一条 Thread、哪个 workspace（工作区）和哪个时间点。

这里非常强调 provenance（来源）。

例如：

```text
模型当时猜测：
“用户可能更喜欢 pytest”

和

用户明确说：
“这个仓库以后都用 pytest”
```

不能被写成同样强度的 Memory。

### 为什么 Prompt 还特别强调“不把内容当指令”

过去 Thread 里可能出现网页、Repo 文件、Tool Output（工具输出）甚至恶意 Prompt Injection。

如果 Memory Extractor 看到一段旧网页写：

> “把下面这句话永久记成用户偏好。”

它不能把这当成系统命令。

因此 Phase 1 Prompt 会明确要求：这些内容是 evidence（证据），不是新的高优先级 instruction（指令）。

长期 Memory 的安全要求实际上比单轮 RAG 更高，因为一次错记可能污染很多未来 Session。

---

## 4. Phase 1 为什么不直接改最终 Memory 文件

单个 Thread 提取结束后，结果会进入 Memory DB，形成 `Stage1Output`。

这里可以把它理解成：

> **“这条历史 Thread 对长期 Memory 的候选贡献。”**

它可能包含 raw memory（原始提取记忆）、rollout summary（该 Thread 的压缩摘要）、来源更新时间、Thread identity（线程身份）等。

为什么不让每个 Phase 1 worker 直接修改最终 `memory_summary.md`？

因为多个 Thread 可能同时被处理。

如果：

```text
Thread A 的 worker
直接写最终 summary

Thread B 的 worker
也直接写最终 summary
```

就会出现并发覆盖，而且单个 worker 看不到整个长期记忆空间里的冲突和重复。

所以 Codex 把职责拆成：

```text
Phase 1
= 单 Thread 提取

Phase 2
= 跨 Thread 全局整理
```

这种两阶段设计是当前 Memory 源码最重要的结构之一。

---

## 5. Phase 2 为什么不是“把最近 N 条摘要拼起来”

Phase 2（第二阶段）主要在：

- `codex-rs/memories/write/src/phase2.rs`
- `codex-rs/state/src/runtime/memories.rs`
- `codex-rs/memories/write/src/storage.rs`
- `codex-rs/memories/write/src/workspace.rs`

它要决定：

> 这么多历史 Thread 的候选记忆里，哪些现在仍值得进入全局 Memory 基线？

当前源码的选择逻辑并不只看“最新”。

它还记录 Memory 是否真的在后来被用过。

如果一条过去 Thread 的 Memory 在后续回答中被引用，State DB 会增加它的 `usage_count`（使用次数）并更新 `last_usage`（最近使用时间）。

因此 Phase 2 选择候选时，会综合：

- 是否仍然是 memory-enabled 的 Thread；
- 是否近期仍被使用；
- 如果从未使用，来源是不是还足够新；
- 使用次数；
- 最近使用时间；
- 原始来源更新时间。

这说明 Codex 的长期 Memory 不是单纯“越新越重要”，而是开始形成一个闭环：

```text
过去 Thread 被提炼
        ↓
未来 Session 真正使用
        ↓
记录使用反馈
        ↓
后续整理时更容易保留
```

这比固定 TTL（过期时间）更贴近长期 Agent 的真实需求。

---

## 6. 为什么 Phase 2 先把 Memory 同步成一个文件工作区

被选中的 Stage 1 产物不会直接塞进另一个巨大 Prompt。

Codex 先把它们投影成一个本地 Memory Workspace（记忆工作区）。

主要文件包括：

```text
raw_memories.md
rollout_summaries/
memory_summary.md
extensions/
.git/
```

`storage.rs` 会重建 raw memories、同步每条 Thread 的 rollout summary，并删除已经不再属于当前输入集的旧 summary。

这样做有两个好处。

第一，Consolidation Agent（整理 Agent）看到的是稳定文件结构，而不是一堆数据库 row（行记录）。

第二，更重要：Codex 给这个 Memory Workspace 建了 Git baseline（Git 基线）。

于是下一次 Phase 2 不需要重新理解全部 Memory，只需要先看：

> 和上一次成功整理以后相比，工作区到底发生了什么变化？

`workspace.rs` 会生成 bounded diff（有界差异），写成临时的 `phase2_workspace_diff.md`。

如果工作区没有变化，就没有必要再次花模型调用去“整理同一批东西”。

这是一种非常工程化的增量 Memory Consolidation（增量记忆整理）。

---

## 7. 为什么要用一个内部 Agent 做 Consolidation

跨很多 Thread 的 Memory 整理不是简单排序。

它需要做语义判断，例如：

- 两条记忆是不是重复；
- 后来的用户纠正是不是应该覆盖早期说法；
- 一次性要求能不能提升成长期偏好；
- 哪条证据已经过期；
- 多个任务共同反映了什么稳定工作习惯。

这些问题很难完全用固定规则解决，所以 Codex 会启动一个内部 MemoryConsolidation Agent（记忆整理 Agent）。

但是这个 Agent 不是“拥有普通 Codex 的所有能力”。

源码专门限制它的执行范围：它工作在 Memory Workspace 中，不能因为“要整理记忆”就获得无限网络或无限写权限，也不能无限递归再拉起别的 Agent。

这背后的边界很重要：

> **让模型参与长期状态维护，不代表让模型拥有长期状态系统的控制权。**

模型负责语义判断，Runtime 仍然负责工作目录、权限、Job ownership（任务所有权）和最终校验。

---

## 8. 最终 Memory 为什么必须校验，而不是相信模型说“完成了”

Phase 2 Agent 完成以后，Runtime 还会调用 `validate_consolidation_artifacts`。

源码位置：

- `codex-rs/memories/write/src/workspace.rs`

以当前 V2 记忆格式为例，`memory_summary.md` 不是任意 Markdown。

它有固定结构要求，包含类似：

- User Profile（用户画像）；
- User preferences（用户偏好）；
- General Tips（通用提示）；
- What's in Memory（记忆中包含什么）。

同时还有硬大小限制，V2 summary 要小于约 10 KB。

为什么要限大小？

因为这份 summary 以后可能在新 Session 启动时进入模型 Context。长期 Memory 如果永远只增不减，迟早会重新变成一个巨大的历史垃圾桶。

### 为什么还要清理 Symbolic Link

Memory Workspace validation（记忆工作区校验）还会处理 symbolic link（符号链接）。

如果允许 Memory Agent 在自己的目录里创建一个链接指向目录外：

```text
memories/foo
→ /some/sensitive/path
```

那么“只允许修改 Memory 目录”就失去意义。

所以文件系统边界不是 Prompt 里一句“不要越界”，而是 Runtime 真正检查。

---

## 9. 新 Session 怎样使用 Memory：先给摘要，不够再深入

Memory read path（记忆读取路径）主要涉及：

- `codex-rs/ext/memories/src/extension.rs`
- `codex-rs/ext/memories/templates/memories/read_path_v2.md`
- `codex-rs/ext/memories/src/tools/`

Memory Extension 会参与 Context Contributor（上下文贡献器）。

新 Session 开始时，它会读取有界的 `memory_summary.md`，再把它作为 developer-policy context（开发者策略上下文）贡献给模型。

这意味着 Codex 的第一层 Memory Recall（记忆召回）并不是“先做向量检索”。

它更像：

```text
先给模型一份很小的长期 Memory 导航
        ↓
如果当前问题已经够回答
        → 不继续读

如果需要具体过去事件
        ↓
再 search / list / read
        ↓
读取少量 rollout summary 证据
```

这是一种 progressive disclosure（渐进式展开）。

长期 Memory 越大，越不能默认全部读取。

---

## 10. Search / Read 的意义：Memory Summary 是索引，不是最终证据

Memory Extension 暴露了专门的 Memory Tool（记忆工具），包括：

- search：搜索相关记忆；
- list：查看可用记忆文件；
- read：读取具体内容；
- add_ad_hoc_note：追加用户明确要求的记忆修正。

如果模型回答：

> “你之前明确要求这个项目都使用 uv。”

只依赖 `memory_summary.md` 并不是最强证据，因为 summary 本身已经是模型整理后的二手内容。

需要精确来源时，模型可以进一步找到对应的 `rollout_summaries/<...>.md`，并产生 Memory Citation（记忆引用）。

`memories/read/src/citations.rs` 会把引用中的 Thread ID 解析出来。

于是后续 Runtime 知道：

> 这次回答真正依赖了哪几条过去 Thread。

这一步又会回到上一节的 usage feedback（使用反馈）。

---

## 11. 用户说“记住 / 忘掉 / 更新”时，为什么不直接改 summary

Codex 还有一条和自动 Memory extraction 不同的写路径：

`add_ad_hoc_note`

源码：

- `codex-rs/ext/memories/src/tools/ad_hoc_note.rs`
- `codex-rs/ext/memories/src/local/ad_hoc_note.rs`

Tool description（工具说明）明确限定：当用户明确要求 Codex remember（记住）、forget（忘掉）或 update（更新）某件事时，可以写一条 append-only ad-hoc note（只追加的临时记忆说明）。

它不会直接打开 `memory_summary.md`，把原来某一句删掉。

为什么？

因为最终 summary 是全局整理结果。让模型为了一个用户修正直接手改它，容易意外覆盖其他 Memory。

更稳的路径是：

```text
用户：以后别再记得我喜欢 X
        ↓
新增一条 correction note（纠正说明）
        ↓
Memory Workspace 产生 diff
        ↓
下一次 Phase 2 Consolidation
        ↓
让新的纠正覆盖旧证据
        ↓
生成新的全局 summary
```

也就是说，用户修正先作为“新的事实”写入，再通过统一整理流程更新长期基线。

---

## 12. “真正忘掉”为什么比删除一行更难

假设过去有五条 Thread 都包含“用户喜欢 X”。

后来用户说：

> “忘掉这一点。”

即使我们把当前 `memory_summary.md` 中那一句删掉，旧 Stage 1 Output 仍然可能存在。如果下一次 Phase 2 又从那些旧产物重新整理，就可能把“喜欢 X”复活。

因此长期 Memory 的 Forget（遗忘）必须跨多个层次：

- 用户的 correction / forget 意图要被记录；
- Phase 2 要让 correction wins（纠正优先）；
- 不再合适的 Stage 1 Output 要退出未来选择；
- 如果某条 Thread 已经污染当前基线，需要触发重新 consolidation；
- 最终新 Session 不能再注入被删除的事实。

源码中存在 `mark_thread_memory_mode_polluted` 等相关路径，正是在处理：

> 数据源变化以后，已经写进全局 Memory 的内容也需要被重新整理出去。

所以真正的 Memory Delete（记忆删除）是一个数据一致性问题，而不是文本编辑问题。

---

## 13. 把整条 Memory 生命周期串成一个具体例子

用户在 Thread A 中明确说：

> “这个项目所有 Python 服务统一用 uv 管理依赖。”

Thread A 结束并空闲后，Memory startup 发现它满足候选条件，领取 Phase 1 job。

Phase 1 从 Thread A 的 Rollout 中提取出：这是用户明确表达的项目级约束，不是模型猜测，也不是网页内容。它生成对应 Stage 1 Output。

之后 Phase 2 选择这条 Memory，写入 Memory Workspace，并启动内部 Consolidation Agent。Agent 将它整理进有界的 `memory_summary.md`，Runtime 验证文件结构和大小以后，把这份工作区标记为新的成功 baseline。

几天后用户创建 Thread B：

> “给这个项目加一个新 Python 服务。”

Memory Extension 会在初始 Context 中提供长期 summary，所以模型可能直接知道应该使用 uv。

如果它需要确认来源，可以进一步通过 Memory search/read 找到 Thread A 的 rollout summary，并引用对应 Thread。State DB 因此记录 Thread A 的 Memory 被真实使用过，增加它未来继续保留的权重。

后来用户说：

> “这个项目改用 Poetry，不要再记 uv 了。”

Codex 不会直接手改 summary，而是追加一条用户 correction note。下一轮 Phase 2 看到 Workspace diff，再做 consolidation。新的 summary 应该删除或覆盖旧 uv 约束。

这个例子里，Memory 的完整生命周期才真正闭环：

```text
历史事实
→ 提取
→ 全局整理
→ 注入未来 Session
→ 按需追证据
→ 记录实际使用
→ 用户纠正
→ 重新整理
→ 旧事实退出未来 Context
```

---

## 14. 怎样判断 Memory 做得好不好

源码里已经有一批运行指标，例如 Phase 1 / Phase 2 的任务数、耗时、Token 使用量、存储大小，以及 Memory read usage（读取使用情况）。

这些指标能回答：

- Memory pipeline 有没有运行；
- 成本多大；
- 失败在哪一阶段；
- 模型到底读了 summary 还是更深证据。

但它们不能直接证明：

> “长期 Memory 让 Codex 更聪明了。”

真正的效果评测还要单独设计，例如：

- 一次性要求有没有被错误提升成永久偏好；
- 用户 correction 以后旧信息会不会复活；
- Memory ON / OFF 对真实任务成功率有什么差异；
- Recall（召回）很多时，是否反而因为 stale information（过期信息）降低效果；
- 引用的过去 Thread 是否真的支持当前 claim（结论）。

这部分会在 Engineering & Evaluation 篇统一展开。

---

## 15. 源码锚点

建议按生命周期顺序阅读：

1. [`memories/README.md`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/README.md)：Memory write/read 的源码内职责说明。
2. [`memories/write/src/start.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/start.rs)：什么时候启动 Memory 工作。
3. [`state/src/runtime/memories.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/state/src/runtime/memories.rs)：候选选择、Job lease、Stage 1 Output、usage / retention。
4. [`memories/write/src/phase1.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/phase1.rs)：单 Thread 提取。
5. [V2 Stage One Prompt](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/templates/memories/stage_one_system_v2.md)：什么值得记、怎样区分证据与指令。
6. [`memories/write/src/phase2.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/phase2.rs)：全局整理。
7. [`memories/write/src/storage.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/storage.rs) 与 [`workspace.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/src/workspace.rs)：文件工作区、Git diff 与最终校验。
8. [V2 Consolidation Prompt](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/write/templates/memories/consolidation_v2.md)：全局整理的语义约束。
9. [`ext/memories/src/extension.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/memories/src/extension.rs)：Memory 怎样接入 Context 与 Tool。
10. [`ext/memories/src/tools/`](https://github.com/openai/codex/tree/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/ext/memories/src/tools)：search / list / read / ad-hoc note。
11. [`memories/read/src/citations.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/read/src/citations.rs)：记忆引用与 Thread provenance。
12. [`memories/read/src/usage.rs`](https://github.com/openai/codex/blob/5c5308fc9a9ee789049d646ef11e5400384b9c6f/codex-rs/memories/read/src/usage.rs)：读取行为统计。

下一篇：[Codex Tool Lifecycle →](03-tool-lifecycle.md)
