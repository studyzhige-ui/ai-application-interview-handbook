# 12. 状态与持久化：程序怎样知道工作做到哪里

[← 上一章](11-MemoryLifecycle.md) · [Agent 目录](../README.md) · [下一章 →](13-CheckpointResumeAndRecovery.md)

报告任务已读完 A、B，正在等上传回执。页面断线了，程序重启了，另一个请求又要求取消。新的处理者需要知道什么，才能不重传、不漏掉取消，也不把未完成的报告交出去？

先确定这些会影响下一步的信息，再决定保存在哪里。这比一开始问“Session 放 Redis 还是 MySQL”更有用。

<a id="1-session-是什么"></a>
<a id="legacy-12-01"></a>
<a id="section-1"></a>
<a id="core-1"></a>

## 1. 状态是当前情况，不是所有字段的集合

**State（状态）** 是程序继续、停止或判断结果时需要知道的当前情况。计划只是一部分：它写准备怎么做，状态还要包含已经发生的结果和仍不知道的事情。

```json
{
  "run_id": "report-7",
  "status": "waiting_upload_result",
  "completed_reads": ["A", "B"],
  "pending_operation": "upload-7",
  "artifact_ref": "reports/draft-7"
}
```

这份教学记录表示：A、B 已读，草稿存在，上传结果尚未确定。它不代表通用生产 Schema；真正的字段由任务承诺决定。

`UNKNOWN` 也可以是合法状态，表示程序不知道外部结果。把未知写成失败并重新上传，会丢掉这个重要认识边界。

<a id="3-state-应该保存什么"></a>
<a id="31-identity-state"></a>
<a id="32-control-state"></a>
<a id="33-environment-state-reference"></a>
<a id="34-safety-state"></a>
<a id="35-progress-state"></a>
<a id="6-persistence-不等于把-context-存下来"></a>
<a id="legacy-12-03"></a>
<a id="legacy-12-06"></a>
<a id="section-3"></a>
<a id="section-6"></a>
<a id="core-2"></a>

## 2. 哪些信息需要活过重启

**Persistence（持久化）** 回答如何把必要信息保存到具有相应可靠性保证的存储。状态是内容，持久化是保存方式；不能把所有内存对象原样存成 JSON，就认为程序可以从原指令继续运行。

| 当前信息 | 重启后为何需要 | 常见处理 |
|---|---|---|
| 上传操作身份与回执 | 避免重复创建报告 | 可靠保存并可核对 |
| 用户取消意图 | 防止恢复后继续已取消工作 | 跨进程任务通常需要持久保存 |
| 报告产物引用 | 用户仍要访问与验收 | 按交付期限保存 |
| 可廉价重读的资料 | 恢复时可能重取 | 取决于版本与重算承诺 |
| 活动 socket、协程、进程对象 | 不能原样在新进程使用 | 重建连接与环境 |
| 临时 Token 估算 | 可重新计算 | 未必逐次落盘 |

存储返回成功也有明确条件，要理解事务、同步和备份策略。已经学过的数据库与 Redis 可靠性知识，决定这里实际能够承诺多少恢复能力。

<a id="2-run--turn--step-再复习"></a>
<a id="4-history-应该是事件流而不是一个超长字符串"></a>
<a id="legacy-12-02"></a>
<a id="legacy-12-04"></a>
<a id="section-2"></a>
<a id="section-4"></a>
<a id="core-3"></a>

## 3. Session 不等于连接，History 不等于状态

Session 是一段持续交互的容器，可以关联用户、工作区与多次 Run。HTTP 连接断开，Session 和已经接受的长任务不必因此结束；能否继续由产品约定，而不是网络连接寿命决定。

History 记录过去的消息和事件；State 表示当前情况。历史可以写“曾提出计划 P1，后来改成 P2”，状态只指向当前有效的 P2。上下文再选择模型这次需要的部分，三者不是三个必须各存全文的数据库。

还要区分**诊断记录** 与**业务恢复记录**。“上传成功，回执 report42”不能因诊断采样而丢失；“模型请求耗时 812 毫秒”通常只是排障信息。两者可以通过同一操作标识关联，但可靠性和保留期限不同。

<a id="5-snapshot-与-event-log-怎么配合"></a>
<a id="legacy-12-05"></a>
<a id="section-5"></a>
<a id="core-4"></a>

## 4. 保存当前视图，还是用事件重建

小应用可以用事务表保存当前任务状态和必要交互。另一种设计是维护可靠事件流，并定期保存快照：

```text
快照：已处理事件 100 时的状态
后续：事件 101、102、103
恢复：加载快照 → 按规定顺序应用 101—103
```

这种 Snapshot + Event Log 设计减少从头重建的成本，但要求事件不会漏、顺序有定义、处理可重复。普通调试日志并不会自动满足这些条件。

选择取决于审计、恢复与运维需求，不是“所有 Agent History 必须事件溯源”。无论采用哪一种，外部上传与本地状态仍不是天然同一事务；恢复边界在下一章继续分析。

<a id="10-concurrency同一个-session-同时来两个请求怎么办"></a>
<a id="11-state-version-为什么重要"></a>
<a id="legacy-12-10"></a>
<a id="legacy-12-11"></a>
<a id="section-10"></a>
<a id="section-11"></a>
<a id="core-5"></a>

## 5. 多个请求同时更新，需要防止覆盖

A 读到状态版本 4，准备继续；B 也读到版本 4，并提交取消，状态变成版本 5。A 如果不检查就把自己计算出的结果写回，可能覆盖取消。

可以使用条件更新：只在当前版本仍为 4 时提交 A 的更新。失败说明有并发变化，应重新读取并判断，而不是强制覆盖。也可以按 Run 排队或采用单处理者协议；先选择符合交互需要的最简单方案。

**ID 说明是哪个对象，版本说明对象是否变化。** run_id、operation_id 和 state_revision 的目的不同；不要求每条事件都记录一整套版本树。一次运行的配置可以引用一份固定快照，各处不必复制完整 Prompt 和工具说明。

<a id="12-cold-resume-与-warm-resume"></a>
<a id="13-session-retention--deletion"></a>
<a id="7-session-store-选什么"></a>
<a id="8-tenant-isolation-为什么必须进入-state-schema"></a>
<a id="9-session-hijack--cross-tenant-pollution"></a>
<a id="cold-resume"></a>
<a id="human-a"></a>
<a id="legacy-12-07"></a>
<a id="legacy-12-08"></a>
<a id="legacy-12-09"></a>
<a id="legacy-12-12"></a>
<a id="legacy-12-13"></a>
<a id="mysql--durable-db-适合"></a>
<a id="object--artifact-store"></a>
<a id="redis-适合"></a>
<a id="section-12"></a>
<a id="section-13"></a>
<a id="section-7"></a>
<a id="section-8"></a>
<a id="section-9"></a>
<a id="warm-resume"></a>
<a id="core-6"></a>

## 6. 隔离与留存要覆盖整个读取路径

知道 session_id 不代表有访问权。查询状态、读取产物、取得记忆和执行工具时，都要绑定可信身份与授权范围。把租户编号加进缓存键有助于避免冲突，但不能替代服务端授权。

| 存储选择 | 适合的用途 | 需要核对 |
|---|---|---|
| 进程内存 | 活动对象、可重建缓存 | 进程结束即丢失 |
| 文件或 SQLite | 单机历史和任务记录 | 原子写、并发、磁盘和备份 |
| 事务数据库 | 多处理者状态与操作记录 | 事务和并发更新边界 |
| 对象存储 | 报告、大日志和文件产物 | 权限、引用与保留期限 |
| Redis | 快速短期状态或配置适当的持久用途 | TTL、淘汰及持久化丢失窗口 |

Warm resume（热恢复）可以复用仍在运行进程中的部分对象；Cold resume（冷恢复）只能依靠可靠记录重新建立环境。不能只验证热恢复，就承诺进程崩溃也可恢复。

任务结束后的留存也按用途决定：报告、业务回执、诊断数据和记忆未必同期限。删除会话是否联动产物与记忆应明确，不能用一个 Redis TTL 代替所有删除责任。

<a id="summary"></a>

## 本章小结

从下一步需要知道什么，推导当前状态；从重启后承诺什么，推导持久化。会话、历史、模型输入和诊断各有用途。并发、权限与留存决定这些记录能否被正确使用。

<a id="15-面试怎么答"></a>
<a id="qagent-session--state-怎么设计"></a>
<a id="qagent-state究竟是什么"></a>
<a id="qstate和persistence有什么区别"></a>
<a id="q为什么不把trace作为恢复数据库"></a>
<a id="q每个东西都必须记录版本吗"></a>
<a id="interview"></a>

## 🎯 面试怎么回答

### State 和 Persistence 有什么区别？

State 是任务当前情况，Persistence 是让必要信息跨重启保留的机制。连接和协程通常重建，操作身份、取消和回执则可能必须保存。不是把全部内存序列化。

### 为什么不能靠 Trace 恢复业务？

Trace 主要服务诊断，可能采样、脱敏或过期。关键操作与取消要有可靠记录，不能随采样丢掉。可以通过 ID 关联，但要分别定义责任。

### 同一 Session 同时来继续和取消请求，怎么办？

按 Run 串行处理、条件版本更新或明确单所有者协议，防止旧视图覆盖新取消。先确定交互语义，再选并发机制；不能只依赖共享 JSON。

<a id="16-高频易错点"></a>
<a id="pitfalls"></a>

## ⚠️ 易错点

> ⚠️ Prompt 是状态的一个输入视图，保存 Prompt 不自动保存全部恢复依据。

> ⚠️ Session ID、租户缓存键和用户授权不是同一件事，访问必须重新校验。

> ⚠️ Snapshot 加事件流是可选设计，普通日志不自动成为可靠事件源。

<a id="17-本章自测"></a>
<a id="self-test"></a>

## 本章自测

<details><summary>1. A 读取版本 4，B 已提交版本 5 的取消，A 应直接覆盖吗？</summary>

不能。条件更新应失败，A 重新读取取消状态并按规则停止，不应把旧继续决定写回。

</details>

<details><summary>2. 重启以后原 socket 不能恢复，意味着任务一定丢失吗？</summary>

不一定。若必要任务状态、操作与产物可靠保存，新进程可以重建连接并核对后继续。

</details>

<details><summary>3. Trace 采样漏掉上传 Span，还能判断是否已上传吗？</summary>

应该能依靠可靠操作记录与下游核对。若只能靠该 Span 猜，说明诊断与业务事实混用了。

</details>

<a id="12-state--persistence程序怎样记住当前工作"></a>
<a id="14-human-a-信号"></a>
<a id="references"></a>

## 知识回看与权威资料

- [检查点与恢复](13-CheckpointResumeAndRecovery.md)：分析快照之间的外部动作窗口。
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)：对照一种明确的图状态持久化语义。
- [固定会话与持久化对照](../../../products/claude-code/04-engineering-evaluation.md#implementation-chapter-12)：区分被保存的交互与不可原样恢复的运行对象。


---

[← 上一章](11-MemoryLifecycle.md) · [Agent 目录](../README.md) · [下一章 →](13-CheckpointResumeAndRecovery.md)
