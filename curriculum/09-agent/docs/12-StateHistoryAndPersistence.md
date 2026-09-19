# 12. State / Persistence：程序怎样记住当前工作

Agent 系统一旦不再是“一次请求、一次回答”，就必须明确：

> **一次会话到底是什么？哪些状态跨 Turn 保存？哪些只是临时 Context？多用户之间怎样隔离？**

如果只写：

```text
conversation_id -> Redis
```

远远不够。

这一章的目标是建立 Runtime（运行时执行系统） State（状态） Plane 的最小模型。

[← 上一章](11-MemoryLifecycle.md) · [Agent 目录](../README.md) · [下一章 →](13-CheckpointResumeAndRecovery.md)

---

<a id="section-1"></a>

## 1. Session 是什么

<a id="legacy-12-01"></a>

你让助手读A、B、C并写报告。第一次调用读完A，下一次该读B还是重新读A？用户这时取消，程序该停止哪个正在等待的调用？报告已生成，但引用检查没通过，界面该显示完成吗？这些问题的答案就是程序的State（状态）：**继续或停止工作时，需要知道的当前情况。**

Plan（计划）是“准备先A后B”；状态还包含“A已成功、B正在等结果、当前不允许写原件、报告尚未验收”。因此“当前执行事实”不是让你背一个抽象名词，而是上述能驱动程序判断的信息。状态也包含`UNKNOWN`等认识边界——程序不知道结果，不应擅自把它写成失败。

Session 可以理解为：

> **一段连续交互的 Runtime 容器。**

至少通常会有：

```text
session_id
user / tenant / workspace identity
created_at
last_active_at
runtime config snapshot
history / event reference
current run state
memory namespace
permission context
```

Session 不等于一条聊天记录，也不等于一个 HTTP connection。

---

<a id="section-2"></a>

## 2. Run / Turn / Step 再复习

<a id="legacy-12-02"></a>

第03章使用的教学口径是：

```text
Session（持续会话）
└─ Run（一个目标的执行）
   └─ Turn（模型决策—动作—观察的反馈轮）
      └─ Step（其中具体步骤）
```

它帮助说明一个工具步骤失败不等于整个任务结束。Codex的Thread/Turn/Item是产品对象，一次Turn可跨多次推理和工具交互；Claude的submitMessage与内部循环计数也不应强制映射。本章只决定哪些状态跨交互、跨进程保存，不另造一套同名定义。

---

<a id="section-3"></a>

## 3. State 应该保存什么

<a id="legacy-12-03"></a>

| 当前情况 | 下一步如何受影响 | 是否一定需要跨重启保存 |
|---|---|---|
| 已读A，结果可以廉价重读 | 可以读B或重读A | 取决于恢复成本 |
| 正在等待一次报告上传的结果 | 不能直接再上传新副本 | 高风险，需操作身份和核对依据 |
| 用户取消任务 | 不应继续派发新动作 | 若任务跨进程运行，通常需要 |
| 当前HTTP连接的socket对象 | 用来推送界面消息 | 不宜原样存，重连时重新建立 |
| 临时Token估算 | 帮助本次预算检查 | 可重新计算，不必每次落盘 |
| 已确认交付报告的产物引用 | 让用户访问和核验 | 按业务交付期限保存 |

有了这些理由，再看一个**教学用最小记录**：

```json
{
  "run_id": "report-7",
  "status": "waiting_upload_result",
  "completed_reads": ["A", "B"],
  "pending_operation": "upload-7",
  "artifact_ref": "reports/draft-7"
}
```

它的意思是“这是report-7，A/B读完了，草稿存在，上传结果还没确定”。这不是生产必填Schema，也没要求保存每段日志。不同任务需要不同记录；能用它决定下一步，才说明字段有价值。

Runtime State 的目标不是“保存所有文本”，而是支持：

```text
下一步正确决策
恢复
取消
审计
并发控制
```

可以分几类。

### 3.1 Identity State

```text
session_id
run_id
turn_id
current_step_id
```

### 3.2 Control State

```text
status
current_goal
plan
budget
retry_count
active_tool_call
```

### 3.3 Environment State Reference

```text
workspace_id
sandbox_id
artifact ids
file generation
```

### 3.4 Safety State

```text
permission mode
approved action ids
policy version
```

### 3.5 Progress State

```text
completed steps
pending steps
blocked reason
```

这些分类是检查遗漏的菜单，不是每个Agent必须存的表。先定义重启后还承诺继续什么，再确定必要事实。短暂只读问答与会持续发邮件的长任务，保存要求显然不同。

---

<a id="section-4"></a>

## 4. History 应该是事件流，而不是“一个超长字符串”

<a id="legacy-12-04"></a>

更稳妥的模型：

```text
Event 1: UserMessage
Event 2: ModelOutput
Event 3: ToolCall
Event 4: ToolResult
Event 5: Approval
Event 6: StateTransition
```

每条事件有：

```text
event_id
session_id
run_id
turn_id
timestamp
type
payload
correlation_id
```

这样 Trace（执行追踪）、Replay（重放）、Checkpoint（检查点） 才有可靠基础。

这里不是要求所有应用都做完整事件溯源。简单应用可以保存当前状态与必要交互；需要由事件重建时才定义可靠事件流。诊断Trace不能成为关键回执唯一来源。

---

<a id="section-5"></a>

## 5. Snapshot 与 Event Log 怎么配合

<a id="legacy-12-05"></a>

如果每次恢复都从第 1 条 Event 重放：

```text
session 越长
→ replay 越慢
```

一种常见设计是：

```text
Durable Event Log
+
Periodic State Snapshot
```

恢复时：

```text
load latest snapshot
→ replay newer events
```

这里是通用架构模式，不声称 Claude Code / Codex 一定使用同样的数据存储实现。

---

<a id="section-6"></a>

## 6. Persistence 不等于把 Context 存下来

<a id="legacy-12-06"></a>

Persistence（持久化）就是把需要跨进程或机器故障保留的数据写入具有相应可靠性保证的存储。Python变量只在进程内；程序重启变量会消失。写文件、事务提交到数据库或保存对象都是可能方式，但要理解实际写入成功、同步和备份策略，而不是认为调用`save()`便永不丢。

状态是**内容是什么**，持久化是**怎么让部分内容活过重启**。并非所有状态都应持久化：连接、锁对象和协程不能靠JSON原样恢复；可以保存“等待operation7”并在新进程建立新连接核对结果。

| 载体 | 适合承担 | 要检查的边界 |
|---|---|---|
| 进程内存 | 活动连接与可重建缓存 | 进程结束就丢 |
| 本地文件/SQLite | 单机历史与任务记录 | 原子写、并发、磁盘与备份 |
| 事务数据库 | 多Worker任务状态和操作账本 | 事务边界与并发更新 |
| 对象/产物存储 | 大文件、报告、日志产物 | 权限、保留期限和引用可解析性 |
| Redis | 快速短期状态或配置得当的持久用途 | TTL、淘汰、持久化与故障丢失窗口 |

不是所有Agent都需要数据库。不能承诺跨重启恢复的小工具可以从头开始；需要长任务恢复时再明确保存责任。

错误思维：

```text
把当前 prompt JSON 存 DB
→ resume 时再发给模型
```

问题是 Prompt 只是 State 的一个投影。

真正需要持久化的可能还有：

```text
side effects
artifact refs
tool call correlation
approval
budget
workspace version
pending task
```

因此：

> **Context 是可重新编译的 View；State 才是 Runtime 的事实。**

History（历史）记录发生过的交互；State是从这些交互及外部结果得到的当前视图。Checkpoint（检查点）是某个可继续的状态快照及引用。Trace（执行追踪）用来诊断耗时和失败路径，不是默认恢复输入。相同事件可以服务多个用途，但可靠性、保留和权限要求不同。

例如“上传已成功”是不能因诊断采样而丢的业务回执；“模型调用花了812毫秒”通常是可采样诊断信息。把它们塞进同一个日志字符串，再期待重启时猜出状态，是危险的职责混淆。

Snapshot（快照）加Event Log（事件日志）是一种恢复设计，不是强制架构。简洁事务表也能表达当前状态。如果选事件重建，就要明确哪些事件被可靠记录、顺序怎样确定、快照后如何接续；不是所有调试日志自动成为事件源。

---

<a id="section-7"></a>

## 7. Session Store 选什么

<a id="legacy-12-07"></a>

不能只问：

> Redis 还是 MySQL？

要先问数据语义。

#### Redis 适合

```text
高频 transient state
TTL session cache
lease / heartbeat
fast coordination
```

#### MySQL / Durable DB 适合

```text
long-term session metadata
durable run record
billing / ownership
high-value audit facts
```

#### Object / Artifact Store

适合：

```text
large logs
file snapshots
model/tool artifact
```

最终通常是组合，而不是一库包办。

---

<a id="section-8"></a>

## 8. Tenant Isolation 为什么必须进入 State Schema

<a id="legacy-12-08"></a>

多租户系统不能只是：

```text
WHERE user_id = ?
```

在一个业务代码分支里“记得加”。

建议所有核心 State Object 自带：

```text
tenant_id
workspace_id
user_id
```

并在：

```text
storage key
query filter
cache key
tool permission
artifact path
trace scope
```

都显式传播。

对应 HUMAN-A `AGENT-017` Multi-tenant State Isolation。

---

<a id="section-9"></a>

## 9. Session Hijack / Cross-tenant Pollution

<a id="legacy-12-09"></a>

经典事故：

```text
cache key = session:{session_id}
```

如果 session_id 不是全局不可猜且查询没有 tenant boundary：

```text
Tenant A
→ 构造 B 的 session id
→ 读到 B state
```

更稳：

```text
session:{tenant_id}:{session_id}
```

但 Key 设计仍不能替代服务端授权检查。

---

<a id="section-10"></a>

## 10. Concurrency：同一个 Session 同时来两个请求怎么办

<a id="legacy-12-10"></a>

例如：

```text
Request A: “继续执行任务”
Request B: “先停止，改需求”
```

如果两个 Worker 同时修改 State：

```text
Lost Update
Out-of-order Event
Duplicate Tool
```

可以使用：

```text
optimistic version
single owner lease
serialized event append
per-run queue
```

关键是：

> **同一 Run 的 State Transition 必须有并发协议。**

---

<a id="section-11"></a>

## 11. State Version 为什么重要

<a id="legacy-12-11"></a>

伪代码：

```text
read state version=42
compute update
write where version=42
→ success: version=43
→ fail: someone else updated
```

这样可以发现 Lost Update。

对于长任务还可以维护：

```text
state_generation
checkpoint_generation
instruction_generation
```

后面 Resume（恢复执行） 时很重要。

ID（标识）回答“这是哪个对象”：run7、operation7、artifact7。Version（版本）回答“它是不是已经改变”：并发Worker读到状态版本4，提交时发现变5，就不能覆盖别人的更新。两者不同。

只有存在变化和兼容性风险时才加相应版本。例如一次Run可引用一份不可变配置快照；不必在每条Trace重复整段Prompt和所有工具Schema。状态并发用revision，文件读取用必要的内容标识；事件本身通常只需唯一ID和类型，未必都需要业务版本。不能因“将来可能排查”就保存全部原始输入。

多租户更重要的是可信身份及授权查询：知道session_id不等于有权访问；模型生成的tenant_id不能当认证来源。两个请求更新同一会话时可排队、拒绝并发或做版本检查，先用最简单符合产品语义的方式。

<details>
<summary>两个产品怎样体现“持久记录不等于全部运行内存”</summary>

Codex固定`Session`保存历史与上下文参考，`persist_rollout_items`把选定RolloutItem交给持久线程记录；模型请求则从历史投影构建。其App Server通过Thread提供跨交互会话语义。这个事实并不承诺自定义外部工具的副作用都有业务事务记录，接入方仍要设计它。

Claude Code用户快照的QueryEngine负责会话生命周期，`query.ts`有消息、工具上下文、重试/压缩跟踪等活动状态；`utils/sessionStorage.ts`承担记录路径。`compact.ts`通过边界和保留消息关系支持压缩后加载，而非序列化所有协程、网络连接和内存缓存。官方支持会话恢复，也不意味着恢复任意外部业务交易。

</details>

---

<a id="section-12"></a>

## 12. Cold Resume 与 Warm Resume

<a id="legacy-12-12"></a>

可以区分：

### Warm Resume

```text
worker 还在
in-memory objects 还在
```

### Cold Resume

```text
进程已经重启
只剩 durable state
```

如果系统只支持 Warm Resume：

```text
真正 crash 后仍恢复不了
```

所以 Production（生产环境） 设计要问：

> **哪些运行事实只在内存，哪些必须 durable？**

Codex Source Index 对 Thread Instructions 也明确区分 warm resume、cold resume / offline fork、live fork 的 instruction snapshot/provider 继承边界，这说明 Resume 不是简单“重新加载聊天”。

---

<a id="section-13"></a>

## 13. Session Retention / Deletion

<a id="legacy-12-13"></a>

Session 也有生命周期：

```text
active
idle
archived
expired
deleted
```

需要定义：

- 保留多久；
- 是否允许用户删除；
- artifact 是否联动删除；
- trace / billing 是否有独立保留规则；
- Memory（记忆） 是否跟 Session 一起删除。

这些不能都靠一个 Redis TTL 解决。

留存期限服务用途：用户仍需下载的产物、业务要求保留的操作回执、可以清理的大工具结果、必须尽快删除的调试输入，不应统一永久保存。

---

<a id="human-a"></a>

执行状态与历史持久化还对应`AGENT-016`、`AGENT-017`，见研究题库。

## 14. HUMAN-A 信号

本章主要承接：

- `AGENT-017`：多用户 / 多 Tenant（租户） 的 Memory、Context、Session 与权限隔离；
- `AGENT-027` 的前置：Checkpoint / Persistence / Resume；
- `AGENT-004` 的 Event Model 基础。

真实面试中常见追问：

```text
Session 存哪？
多实例怎么恢复？
多个用户怎么隔离？
Context 和 State 是一回事吗？
```

---

<a id="interview"></a>

## 15. 面试怎么答

### Q：Agent Session / State 怎么设计？

🎯 **建议回答**：

> 我会把 Session 当作一段连续交互的 Runtime 容器，而不是聊天文本。State 保存当前 goal、status、budget、active tool、progress、workspace 和 permission 等执行事实；History 用结构化 event 记录已发生事情；Context 是从这些持久状态和其它来源编译出来的 model view。多实例场景要支持 durable persistence、版本控制和 cold resume，多租户要让 tenant/workspace identity 贯穿存储 key、query、tool permission、artifact 和 trace，而不是只靠 Prompt 隔离。

### Q：Agent State究竟是什么？

🎯 **30 秒回答**：

> 它是程序为了继续、停止和判断结果需要知道的当前情况，例如目标、已完成读取、待定工具、取消意图、产物和审批。计划只是其中的未来步骤视图。State不等于全部聊天，也不等于模型上下文；可以包含结果未知，以免程序把不确定当失败重试。

### Q：State和Persistence有什么区别？

🎯 **30 秒回答**：

> State讲保存什么当前情况；Persistence讲其中哪些写到能跨重启保留的存储。进程内连接等可以丢弃重建，但上传操作身份和回执可能必须持久化。是否保存取决于恢复契约、风险和成本，不要求把运行内存全部备份。

### Q：为什么不把Trace作为恢复数据库？

🎯 **30 秒回答**：

> Trace主要用于诊断，可能采样、脱敏或过期；恢复要有确定的状态和操作记录。关键业务回执不能随Trace采样丢掉，耗时日志却通常不必阻塞执行。可以关联同一ID，但应分别定义数据责任。

### Q：每个东西都必须记录版本吗？

🎯 **30 秒回答**：

> 不必须。ID识别对象，版本处理变更、并发或兼容问题。可以让Run引用一次不可变配置，状态更新用revision；不是每条事件都复制全部版本信息。先问这个变化会影响什么决策，再决定记录粒度。

---

<a id="pitfalls"></a>

## 16. 高频易错点

⚠️ **Session = Chat History。** Session 还包含 Runtime State / Config / Ownership。

⚠️ **Context 存下来就是 Checkpoint。** Context 只是 View，不足以恢复外部副作用和执行位置。

⚠️ **多租户隔离靠 Prompt。** 必须由 Storage / Permission（权限） enforce。

⚠️ **同一个 Session 并发请求自动安全。** 需要版本或 Owner 协议。

⚠️ **State就是Plan的pending/done。** 还包括等待的操作、取消、结果、权限与产物等当前情况。

⚠️ **持久化就是把全部内存存下来。** 保存可恢复的必要信息，连接与协程通常重建。

⚠️ **有Session ID就有访问权。** 身份与授权必须来自可信控制链。

⚠️ **Trace越全，恢复越可靠。** 诊断与恢复目标不同，关键事实需可靠存储。

⚠️ **任何事件必须版本号。** 唯一标识和变更版本不同，只为实际问题引入。

---

<a id="self-test"></a>

## 17. 本章自测

<details><summary>1. 为什么 History 更适合做结构化 Event Log？</summary>

因为 ToolCall、ToolResult、Approval（批准）、StateTransition 等事件需要独立身份和关联关系，才能支持 Trace、Replay、Debug 与 Checkpoint。

</details>

<details><summary>2. Cold Resume 需要比 Warm Resume 多保存什么？</summary>

进程内对象全部丢失，所以必须有足够 durable state 来重建运行：执行位置、状态、artifact、side effect、approval、instruction/context source version 等。

</details>

<details><summary>3. 为什么 Context 不应该作为唯一 Source of Truth？</summary>

Context 会裁剪、压缩、重排，是模型输入视图；Runtime 正确性依赖结构化 State 和 History，不能只依赖自然语言 Prompt。

</details>

<details><summary>4. 程序重启后读A的结果丢了，一定不能继续吗？</summary>

若A可按授权重新读取，且允许重算，就可以重建；若A当时内容不可再得且影响验收，则需按契约保存快照或承认无法精确恢复。

</details>

<details><summary>5. 一个活跃HTTP连接能直接存到JSON里下次恢复吗？</summary>

不能恢复原连接本身。可保存任务身份与事件位置，让重连建立新连接并查询权威状态。

</details>

<details><summary>6. “用户取消”为什么有时比日志耗时更需要持久化？</summary>

长任务可能被另一个Worker接手；取消意图丢失会继续执行不该执行的动作。耗时日志丢失通常只影响诊断，不改变业务授权。

</details>

<details><summary>7. 状态记录中的UNKNOWN是不是脏数据？</summary>

不是，它准确表达尚未确认的结果。必须核对才可变成成功或失败，保留未知比编造失败更安全。

</details>

<details><summary>8. 两Worker都读取revision4，一个先改到5，另一个怎么办？</summary>

提交时检查版本或锁，发现基线变化就拒绝覆盖并重读。版本用于防丢失更新，不是为了炫耀字段齐全。

</details>

<details><summary>9. 小型一次性报告程序可以不用持久数据库吗？</summary>

可以，前提是明确故障后从头开始及其可接受成本，没有不可重放副作用。不能一边不保存必要状态，一边承诺任意断点恢复。

</details>

---

[← 上一章](11-MemoryLifecycle.md) · [Agent 目录](../README.md) · [下一章 →](13-CheckpointResumeAndRecovery.md)
