# 11. Memory：提取、召回、更新、纠错与遗忘

Agent 一旦跨多轮、多任务运行，就会遇到一个经典问题：

> **哪些信息应该被“记住”，记多久，什么时候再取回来？**

如果回答只是：

> “把聊天记录存进 Vector DB。”

那还没有真正进入 Agent Memory（记忆） Engineering。

Memory 的核心不是“有个数据库”，而是：

```text
什么值得写？
写成什么形式？
什么时候召回？
怎样更新？
什么时候过期？
错误 Memory 怎么纠正？
```

[← 上一章](10-CompactionAndContinuation.md) · [Agent 目录](../README.md) · [下一章 →](12-StateHistoryAndPersistence.md)

---

<a id="section-1"></a>

## 1. 先把 Context / Memory / State / History 分开

<a id="legacy-11-01"></a>

用户说：“以后给我的报告先写结论，再写证据。”本次任务把这句话放进上下文就能执行，但下一次新任务未必还能看到。因此程序可以把它作为用户偏好保存，未来相关任务再读取。Memory（记忆）的目的就是**跨后续交互复用值得保留的信息**，不是给所有消息起一个新名字。

相比之下，“当前已读A、还没读B”主要是本次工作进度；“上传报告返回receipt7”是需要核对的操作结果。它们不能因为都要保存就叫长期记忆。存储持久不等于知识长期有效。

这是整个 Agent Runtime（运行时执行系统） 最重要的边界之一：

```text
Context
= 当前这一次模型调用能看到什么

Memory
= 为未来再次取回而保存的信息

State
= 程序用于决定下一步的当前工作情况，如进度、等待、预算和动作结果

History
= 已经发生的 message / event 记录

Checkpoint
= 可以恢复执行的位置与状态快照/引用
```

所以：

```text
Chat History ≠ Memory
Memory ≠ State
State ≠ Context
```

它们可以互相投影，但不是一个概念。

---

<a id="section-2"></a>

## 2. Memory 为什么不能“什么都存”

<a id="legacy-11-02"></a>

如果所有历史都永久保存：

```text
Token / Storage ↑
Noise ↑
Contradiction ↑
Retrieval Cost ↑
Stale Fact ↑
Privacy Risk ↑
```

最终会得到一个“信息坟场”。

Memory 需要一个生命周期：

```text
Observe
→ Decide whether to remember
→ Extract / Normalize
→ Validate
→ Store
→ Retrieve on demand
→ Update / Consolidate
→ Expire / Correct / Delete
```

---

<a id="section-3"></a>

## 3. Memory 可以怎样分层

<a id="legacy-11-03"></a>

下面按记忆的用途分类，不强制对应四张数据库表。产品有各自分类与实现，不可把教学分类图标成Claude或Codex实际目录。

课程层常见的实用划分：

### 3.1 Working Memory

当前任务正在使用的信息：

```text
current goal
current plan
active constraints
recent tool evidence
```

它通常更接近 Runtime State（状态） / Current Context。

### 3.2 Episodic Memory

发生过的事件：

```text
上次部署失败的原因
用户上一次确认过的选择
某次 incident 的处理结果
```

### 3.3 Semantic Memory

较稳定事实：

```text
用户偏好
项目架构
组织规范
领域知识摘要
```

### 3.4 Procedural Memory

“怎么做”的程序性知识：

```text
部署步骤
排障 SOP
代码修改规范
```

在某些系统里它更接近 Skill（技能包） / Instruction，而不是普通向量 Memory。

这只是课程抽象，不声称 Claude Code / Codex 使用完全相同的四类命名。

---

<a id="section-4"></a>

## 4. 什么时候应该写 Memory

<a id="legacy-11-04"></a>

不建议：

```text
每个 turn 结束
→ 把整段 conversation embedding 一遍
→ 永久存储
```

更合理的是定义 Write Policy：

```text
stable fact?
future value?
user consent / privacy allowed?
already known?
confidence enough?
expires?
```

例如：

```text
“我今天有点累”
```

通常不应该自动晋升长期 Memory。

而：

```text
“这个项目所有 Python 服务统一用 uv 管理依赖”
```

可能更适合持久化。

```text
观察到信息 → 判断以后是否有用 → 提取清楚且有范围的陈述
→ 找已有记录以避免重复 → 写入可跨任务访问的位置
→ 后续任务按需读取 → 核对适用性 → 更新、合并、失效或删除
```

提取时机由系统决定：用户明确要求记住时可以立即处理；某项偏好得到确认后也可写；有的产品在会话空闲后离线提炼。**没有通用规定“第N轮转长期记忆”。** 长期化指它进入后续任务可读取的持久存储，并有合适生命周期，不是一个自动神奇升级。

| 阶段 | 报告偏好的具体变化 | 为什么需要 |
|---|---|---|
| 候选 | “这次报告先结论” | 可能只是当前任务要求，不立即泛化 |
| 确认范围 | 用户确认“以后给我的中文报告都这样” | 避免把局部要求推广到所有人 |
| 保存 | 保存偏好内容、所属用户、来源和适用条件 | 将来能知道何时用、为什么可信 |
| 使用 | 新报告开始，读取相关偏好 | 不把全部旧对话塞回上下文 |
| 修改 | 用户说“客户A需要证据在前” | 可以增加范围例外，不必粗暴覆盖全局 |
| 删除 | 用户不再希望保存 | 删除记录并失效相关索引/缓存 |

先理解每项信息的用途，再选择字段。小系统可能只需一个有范围的文本文件；大系统才需要更精细的来源、权限、删除追踪。不要求每条记忆都配复杂版本树。

---

<a id="section-5"></a>

## 5. Extraction：从对话变成 Memory Record

<a id="legacy-11-05"></a>

不要直接把自然语言聊天原文当长期 Memory 唯一结构。

可以抽成：

```python
# 记忆记录示意：MemoryRecord由应用定义；来源/范围支持核对，置信度不是事实保证。
MemoryRecord(
    id="mem_123",
    kind="project_fact",
    subject="dependency_manager",
    value="uv",
    source_event_id="evt_456",
    confidence=0.96,
    version=3,
    created_at=...,
    expires_at=None,
)
```

这样后续才容易：

```text
去重
更新
冲突检测
版本化
删除
审计来源
```

---

<a id="section-6"></a>

## 6. Retrieval-on-demand 为什么比“全量注入”更重要

<a id="legacy-11-06"></a>

Memory Store 可能有十万条记录。

每次都塞进 Context：

```text
不可行
```

因此：

```text
Current Task / Query
→ Memory Retrieval
→ Relevant Memory
→ Context Assembly
```

这和 RAG 有相似性，但对象不同：

```text
RAG 主要检索外部知识证据
Memory 主要检索 Agent / User / Task 历史沉淀
```

二者的权限、更新和正确性标准也可能不同。

---

<a id="section-7"></a>

## 7. Memory Consolidation 是什么

<a id="legacy-11-07"></a>

随着时间推移可能出现：

```text
mem1: 用户喜欢简洁回答
mem2: 用户偏好先给结论
mem3: 用户不希望长篇背景
```

可以合并成更稳定的 higher-level memory：

```text
response_style = concise / conclusion-first
```

但 Consolidation 不能把来源和版本完全抹掉，否则错误后无法追踪。

推荐保留：

```text
derived_from = [mem1, mem2, mem3]
```

整合能合并相同范围的重复记录，却不能把“这次用英文”扩大成“以后永远用英文”。先保留适用范围和来源，再减少冗余。

---

<a id="section-8"></a>

## 8. Memory Correctness：错误事实比“没有记住”更危险

<a id="legacy-11-08"></a>

`AGENT-016` 直接追问过期摘要、错误事实和冲突信息。

例如：

```text
Memory v1: production DB = mysql-prod-a
后来迁移：production DB = mysql-prod-b
```

如果旧 Memory 仍被召回：

```text
Agent 可能操作错误环境
```

所以 Memory 必须支持：

```text
version
valid_from / valid_to
superseded_by
source
confidence
```

对于高风险事实，最好优先从 Source of Truth 重新验证，而不是只信长期 Memory。

---

<a id="section-9"></a>

## 9. Memory Conflict 怎么处理

<a id="legacy-11-09"></a>

假设：

```text
Memory A: deploy branch = main
Memory B: deploy branch = release
```

不能直接随机挑一个。

可以：

```text
compare timestamp
compare source authority
check project scope
ask user
query Source of Truth
```

Runtime 还应该能记录：

```text
conflict unresolved
```

而不是强行“总结成一个答案”。

错误是“记错了”：用户明明要求中文却存成英文。应根据原始来源纠正，并防止旧索引继续召回错误记录。冲突是“两条陈述不兼容”：先看用户、项目、时间和适用范围，可能是两个不同场景而非互相否定。过期是“以前对，现在不对”：如旧测试命令被项目配置替换，应回到当前仓库验证。

因此不能只按“最新的一条赢”。外部网页最近写了一句不能覆盖用户的稳定偏好；用户当前明确指令通常应优先于历史偏好。无法确定时保留不确定性、查询权威来源或澄清，不把猜测包装成事实。

Consolidation（整合）是合并重复、压缩经验、更新索引和删除无效内容，不等于无损备份。删掉重复文本之前要确保范围和来源没被合并错。版本或来源引用主要用于解释和失效，不是要求每次读取都生成新版本。

---

<a id="section-10"></a>

## 10. Memory Staleness / Expiration

<a id="legacy-11-10"></a>

有些 Memory 天生有 TTL：

```text
临时 feature flag
临时 incident status
短期用户任务偏好
```

有些是版本驱动：

```text
repository architecture
API contract
team policy
```

所以 Memory 失效策略可以包括：

```text
TTL
Source version mismatch
Explicit invalidation
Superseded-by
Low confidence decay
Manual correction
```

---

<a id="section-11"></a>

## 11. Privacy / Tenant Boundary

<a id="legacy-11-11"></a>

Memory 往往包含高敏感上下文：

```text
user preference
workspace information
internal project data
credential-related metadata
```

因此必须在 Key / Namespace / Query Filter 层绑定：

```text
tenant_id
user_id
workspace_id
agent_scope
```

不能只靠 Prompt 里写：

> “请不要读别人的 Memory。”

真正的隔离要在存储 / Query 层 enforce。

多租户 State 下一章继续。

---

<a id="section-12"></a>

## 12. Memory Failure Timeline

<a id="legacy-11-14"></a>

```text
T0  User 说：部署用 branch=main
T1  Runtime 写长期 Memory
T2  项目迁移到 release branch
T3  Source of Truth 更新
T4  Memory 没失效
T5  两周后 Agent 召回旧 Memory
T6  Agent 尝试操作 main
```

根因不是：

```text
Vector DB 召回不准
```

而是：

```text
Memory Lifecycle 缺少 Version / Invalidation
```

用相关后续任务比较开启/关闭记忆的效果：是否准确遵循偏好、是否减少重复询问、是否引入旧错误、是否跨用户泄露。再测试纠错与删除：存错偏好后修正，下一次是否仍召回旧值？删除后相关索引和缓存是否还暴露内容？质量检查应该覆盖“忘掉”，而不只是“记住”。

---

<a id="section-13"></a>

## 13. 产品实现与官方资料对照（按需展开）

<details>
<summary>Claude Code 固定源码侧的证据</summary>

<a id="legacy-11-12"></a>

### Claude Code：文件型auto memory与CLAUDE.md有何不同

官方Memory文档区分：`CLAUDE.md`是人维护的项目指令；auto memory是Claude为未来会话保存的有用记录，不是每次对话全文自动备份。`MEMORY.md`是简短索引，启动时加载有限部分，详细主题文件按需读取；用户可查看、修改或删除。

用户固定快照`memdir/memdir.ts`提供保存指导：先查有无可更新记录，把具体记忆写入主题文件，再在MEMORY.md增加指针；发现错误或过期时更新/删除。这里“何时提取”部分通过模型行为指令表达，不是读到一个统一强制后台定时提取器。代码还区分system里的记忆行为指导与user context中的内容注入。

一条具体路径是：用户确认长期报告偏好→模型按指导写主题文件及索引→下次会话加载索引→需要报告时读详细文件→用户纠正时更新文件/索引。不是“所有Token经过向量库自动成为长期记忆”。功能开关、项目路径和官方版本会影响实际可用性。



### Codex：固定memories模块的两阶段离线提炼

固定源码`codex-rs/memories/README.md`描述另一种实现。非临时、启用记忆且状态数据库准备好的根会话启动时，可以异步启动流水线；它选择符合条件的**已空闲的旧会话记录**，不是把正在运行的每个步骤立刻整合。

第一阶段按资格、时间和租约领取旧会话，在限并发条件下提取原始记忆与会话摘要，执行敏感内容处理并保存阶段结果；无有用内容可不产出。第二阶段用全局任务租约选择提取结果，更新原始记忆材料、摘要文件并清理陈旧产物，再由受约束的整合子Agent维护MEMORY.md、memory_summary.md及相关知识文件。无输入变化可跳过模型工作；失败与重试受控。

这解释了“什么时候长期化”：在该流水线产物被写入后续读取路径时，而不是当前上下文刚做Compaction（上下文压缩）时。启动条件、资格筛选与两阶段职责是固定快照事实；不能把它套到Claude的文件写入路径，也不能声称仅有这份README就证明所有记忆语义永远正确。

</details>

具体实现以[固定源码与官方索引](../../../references/agent/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[Claude Code记忆](https://code.claude.com/docs/en/memory)。

---

<a id="human-a"></a>

## 14. HUMAN-A 信号

本章主要承接：

- `AGENT-014` Memory Architecture：36 个独立来源；
- `AGENT-015` Memory Lifecycle：8 个；
- `AGENT-016` Memory Correctness / Staleness：6 个。

真人面试已经从：

```text
“Memory 怎么做？”
```

深入到：

```text
什么时候晋升长期？
怎么更新？
错了怎么办？
过期怎么办？
```

---

<a id="interview"></a>

## 15. 面试怎么答

### Q：Agent Memory 怎么设计？

🎯 **30 秒回答**：

> 我会先把 Memory 和 Context、State、History（历史记录） 分开。Memory 不是全量聊天记录，而是经过 write policy 选出的、未来有价值的信息。写入时做 extraction、去重、来源和版本记录；使用时按当前任务 retrieval-on-demand；长期还要支持 consolidation、TTL、supersede、conflict 和人工 correction。高风险事实不能只信 Memory，要能回 Source of Truth 验证。多用户场景还要在存储与查询层绑定 tenant/user/workspace 隔离。

### Q：Memory 错了怎么办？

🎯 **30 秒回答**：

> Memory Record 要有 source、version、confidence、validity 和 superseded-by 之类元数据；发生冲突时按来源权威性和版本验证，必要时查询 Source of Truth 或让用户确认，并把旧 Memory 显式失效，而不是只在 Prompt 里追加一句“忽略之前的内容”。

### Q：什么时候提取，什么时候变长期记忆？

🎯 **30 秒回答**：

> 没有统一轮数。可在用户明确要求或确认信息时写，也可以在旧会话空闲后离线提炼。能在后续任务按规则读取的持久化记录才具有长期复用作用。Claude文件型auto memory与固定Codex两阶段流水线就是不同策略，不能混成一种生命周期。

### Q：记忆冲突或错误怎么办？

🎯 **30 秒回答**：

> 先查来源、范围与时间，区分真正冲突和不同场景。当前明确约束不能被旧偏好覆盖；错误记录应纠正并失效索引缓存，无法确定就澄清或回权威来源核对。不能仅按最新时间或者模型自评置信度自动决定。

### Q：怎么评估记忆不是在污染上下文？

🎯 **30 秒回答**：

> 比较开启和关闭记忆的后续任务，检查偏好命中、任务质量、错误召回、权限泄露和成本。再做纠错与删除测试，确认旧错误不会继续被索引或缓存召回。检索命中率高不等于记忆质量高。

---

<a id="pitfalls"></a>

## 16. 高频易错点

⚠️ **Memory = Vector DB。** Vector DB 只是可能的存储/检索组件。

⚠️ **Chat History 全存就是 Memory。** 这会制造噪声和陈旧事实。

⚠️ **Long-term Memory 永久有效。** Production（生产环境） 必须考虑失效和冲突。

⚠️ **Memory 召回结果默认可信。** 高风险事实应重新验证 Source of Truth。

⚠️ **所有聊天都值得长期保存。** 当前过程和噪声不一定有未来价值，且有隐私成本。

⚠️ **Compaction后就产生长期Memory。** 当前输入缩减与未来复用不同。

⚠️ **冲突记忆最新的总是正确。** 需比较来源和适用范围。

⚠️ **删除原记录就一定彻底忘记。** 索引、缓存、导出和备份需按保留政策处理。

⚠️ **记忆来自历史所以是权威事实。** 历史模型判断也可能错误，要能核对。

---

<a id="self-test"></a>

## 17. 本章自测

<details><summary>1. 为什么 Memory 不应该等于完整 History？</summary>

History 是发生过的事件记录；Memory 是为未来价值而选择、提取、维护的信息。两者生命周期和检索目标不同。

</details>

<details><summary>2. Memory Consolidation 为什么必须保留来源？</summary>

因为 higher-level memory 可能总结错误。保留 derived_from/source 才能审计、纠错和重新计算。

</details>

<details><summary>3. 为什么高风险事实不应该只依赖 Memory？</summary>

Memory 可能过期或错误；生产数据库、权限、付款状态等高风险事实应尽量回 Source of Truth 做实时验证。

</details>

<details><summary>4. “这次用英文”能保存成“用户永远喜欢英文”吗？</summary>

不能直接泛化。先保留本任务约束，若要长期保存需确认范围或有可靠证据。错误泛化是常见记忆污染。

</details>

<details><summary>5. 计划中A已读，应写成长期记忆吗？</summary>

通常是当前Run进度，不是跨任务偏好；应按恢复需要保存状态，不靠长期记忆决定是否重复执行。

</details>

<details><summary>6. 新项目的测试命令与旧记忆冲突，先信谁？</summary>

核对当前项目配置和文档。旧经验可提示调查方向，但当前权威环境更能说明实际命令。

</details>

<details><summary>7. 同一用户在两项目有不同风格，是否必须删掉旧偏好？</summary>

不必，可能分别适用于不同项目。把范围表达清楚，检索时按当前项目选择。

</details>

<details><summary>8. 为什么记忆索引应该短，详情另存？</summary>

索引帮助决定读哪个主题，减少启动输入；详情只在相关时加载。索引不是把所有记忆内容永久塞入前缀。

</details>

<details><summary>9. Codex两阶段提炼为何不等于每步同步写记忆？</summary>

资格选择针对旧空闲会话，提取和整合异步受租约/并发控制，启动触发不等于所有当前事件立即成为记忆。

</details>

---

[← 上一章](10-CompactionAndContinuation.md) · [Agent 目录](../README.md) · [下一章 →](12-StateHistoryAndPersistence.md)
