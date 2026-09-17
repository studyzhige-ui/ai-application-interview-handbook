# 12. 状态与持久化：程序怎样记得工作做到哪里

[← 上一章](11-MemoryArchitectureLifecycle.md) · [模块目录](../README.md) · [下一章 →](13-CheckpointResumeReliability.md)

> 本章要解决：State不是一个神秘对象。先看程序需要记住的具体情况，再决定哪些值得落盘。

## 1. 程序为什么需要State

你让助手读A、B、C并写报告。第一次调用读完A，下一次该读B还是重新读A？用户这时取消，程序该停止哪个正在等待的调用？报告已生成，但引用检查没通过，界面该显示完成吗？这些问题的答案就是程序的State（状态）：**继续或停止工作时，需要知道的当前情况。**

Plan（计划）是“准备先A后B”；状态还包含“A已成功、B正在等结果、当前不允许写原件、报告尚未验收”。因此“当前执行事实”不是让你背一个抽象名词，而是上述能驱动程序判断的信息。状态也包含`UNKNOWN`等认识边界——程序不知道结果，不应擅自把它写成失败。

## 2. 先看工作台，再看字段

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

## 3. Persistence究竟是什么

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

## 4. History、Checkpoint、Trace与State的边界

History（历史）记录发生过的交互；State是从这些交互及外部结果得到的当前视图。Checkpoint（检查点）是某个可继续的状态快照及引用。Trace（执行追踪）用来诊断耗时和失败路径，不是默认恢复输入。相同事件可以服务多个用途，但可靠性、保留和权限要求不同。

例如“上传已成功”是不能因诊断采样而丢的业务回执；“模型调用花了812毫秒”通常是可采样诊断信息。把它们塞进同一个日志字符串，再期待重启时猜出状态，是危险的职责混淆。

Snapshot（快照）加Event Log（事件日志）是一种恢复设计，不是强制架构。简洁事务表也能表达当前状态。如果选事件重建，就要明确哪些事件被可靠记录、顺序怎样确定、快照后如何接续；不是所有调试日志自动成为事件源。

## 5. 身份与版本各有什么用，不需要处处版本化

ID（标识）回答“这是哪个对象”：run7、operation7、artifact7。Version（版本）回答“它是不是已经改变”：并发Worker读到状态版本4，提交时发现变5，就不能覆盖别人的更新。两者不同。

只有存在变化和兼容性风险时才加相应版本。例如一次Run可引用一份不可变配置快照；不必在每条Trace重复整段Prompt和所有工具Schema。状态并发用revision，文件读取用必要的内容标识；事件本身通常只需唯一ID和类型，未必都需要业务版本。不能因“将来可能排查”就保存全部原始输入。

多租户更重要的是可信身份及授权查询：知道session_id不等于有权访问；模型生成的tenant_id不能当认证来源。两个请求更新同一会话时可排队、拒绝并发或做版本检查，先用最简单符合产品语义的方式。

<details>
<summary>两个产品怎样体现“持久记录不等于全部运行内存”</summary>

Codex固定`Session`保存历史与上下文参考，`persist_rollout_items`把选定RolloutItem交给持久线程记录；模型请求则从历史投影构建。其App Server通过Thread提供跨交互会话语义。这个事实并不承诺自定义外部工具的副作用都有业务事务记录，接入方仍要设计它。

Claude Code用户快照的QueryEngine负责会话生命周期，`query.ts`有消息、工具上下文、重试/压缩跟踪等活动状态；`utils/sessionStorage.ts`承担记录路径。`compact.ts`通过边界和保留消息关系支持压缩后加载，而非序列化所有协程、网络连接和内存缓存。官方支持会话恢复，也不意味着恢复任意外部业务交易。

</details>

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. Agent State究竟是什么？

<details>
<summary>参考答案</summary>

它是程序为了继续、停止和判断结果需要知道的当前情况，例如目标、已完成读取、待定工具、取消意图、产物和审批。计划只是其中的未来步骤视图。State不等于全部聊天，也不等于模型上下文；可以包含结果未知，以免程序把不确定当失败重试。

</details>

### 2. State和Persistence有什么区别？

<details>
<summary>参考答案</summary>

State讲保存什么当前情况；Persistence讲其中哪些写到能跨重启保留的存储。进程内连接等可以丢弃重建，但上传操作身份和回执可能必须持久化。是否保存取决于恢复契约、风险和成本，不要求把运行内存全部备份。

</details>

### 3. 为什么不把Trace作为恢复数据库？

<details>
<summary>参考答案</summary>

Trace主要用于诊断，可能采样、脱敏或过期；恢复要有确定的状态和操作记录。关键业务回执不能随Trace采样丢掉，耗时日志却通常不必阻塞执行。可以关联同一ID，但应分别定义数据责任。

</details>

### 4. 每个东西都必须记录版本吗？

<details>
<summary>参考答案</summary>

不必须。ID识别对象，版本处理变更、并发或兼容问题。可以让Run引用一次不可变配置，状态更新用revision；不是每条事件都复制全部版本信息。先问这个变化会影响什么决策，再决定记录粒度。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| State就是Plan的pending/done | 还包括等待的操作、取消、结果、权限与产物等当前情况。 |
| 持久化就是把全部内存存下来 | 保存可恢复的必要信息，连接与协程通常重建。 |
| 有Session ID就有访问权 | 身份与授权必须来自可信控制链。 |
| Trace越全，恢复越可靠 | 诊断与恢复目标不同，关键事实需可靠存储。 |
| 任何事件必须版本号 | 唯一标识和变更版本不同，只为实际问题引入。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：程序重启后读A的结果丢了，一定不能继续吗？

<details>
<summary>查看参考答案</summary>

若A可按授权重新读取，且允许重算，就可以重建；若A当时内容不可再得且影响验收，则需按契约保存快照或承认无法精确恢复。

</details>

### 自测 2：一个活跃HTTP连接能直接存到JSON里下次恢复吗？

<details>
<summary>查看参考答案</summary>

不能恢复原连接本身。可保存任务身份与事件位置，让重连建立新连接并查询权威状态。

</details>

### 自测 3：“用户取消”为什么有时比日志耗时更需要持久化？

<details>
<summary>查看参考答案</summary>

长任务可能被另一个Worker接手；取消意图丢失会继续执行不该执行的动作。耗时日志丢失通常只影响诊断，不改变业务授权。

</details>

### 自测 4：状态记录中的UNKNOWN是不是脏数据？

<details>
<summary>查看参考答案</summary>

不是，它准确表达尚未确认的结果。必须核对才可变成成功或失败，保留未知比编造失败更安全。

</details>

### 自测 5：两Worker都读取revision4，一个先改到5，另一个怎么办？

<details>
<summary>查看参考答案</summary>

提交时检查版本或锁，发现基线变化就拒绝覆盖并重读。版本用于防丢失更新，不是为了炫耀字段齐全。

</details>

### 自测 6：小型一次性报告程序可以不用持久数据库吗？

<details>
<summary>查看参考答案</summary>

可以，前提是明确故障后从头开始及其可接受成本，没有不可重放副作用。不能一边不保存必要状态，一边承诺任意断点恢复。

</details>

## 资料与下一步

固定源码：[codex-rs/core/src/session/mod.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/mod.rs)；[QueryEngine.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/QueryEngine.ts)、[query.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)、[utils/sessionStorage.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts)。官方会话语义：[Codex App Server](https://developers.openai.com/codex/app-server/)。下一章讨论恢复边界和两次检查点之间的故障。

本章对应研究能力：`AGENT-004`、`AGENT-017`、`AGENT-027`、`AGENT-029`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](11-MemoryArchitectureLifecycle.md) · [模块目录](../README.md) · [下一章 →](13-CheckpointResumeReliability.md)
