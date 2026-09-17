# 13. 检查点与恢复：两次保存之间崩溃怎么办

[← 上一章](12-SessionStatePersistence.md) · [模块目录](../README.md) · [下一章 →](14-PermissionApprovalSandbox.md)

> 本章要解决：清楚区分Resume、Compaction、Replay；在“工具已成功但本地不知道”的窗口里做正确决定。

## 1. Checkpoint是可继续的存档点，不是时间机器

Checkpoint（检查点）记录一个可以恢复工作的位置及必要状态。Resume（恢复执行）是读取这些记录，把任务继续下去。英文résumé可以指简历，但本章resume是动词“继续”，不是summary（摘要）。Compaction缩减模型输入，与恢复相关但不是同一操作。

报告任务在“已读A/B、尚未上传”保存检查点C1；随后上传报告，服务崩溃。新进程读C1只知道当时没上传，**不知道之后上传是否已成功**。检查点不会让外部世界自动退回C1，这正是恢复难点。

## 2. 两次检查点之间的工作分三类

| 中间动作 | 重启时的策略 | 必要依据 |
|---|---|---|
| 纯计算/可重读 | 允许从旧点重做 | 重算成本和当前输入适用性 |
| 已有可靠成功回执的写入 | 补齐当前状态，不重复做 | 操作身份和真实回执 |
| 可能已发生但没有确定结果 | 先核对，不能盲重试 | 下游幂等键、可查询对象或人工处理 |

所以不是“每秒检查点才安全”。关键动作可以有**独立的可靠操作记录**，检查点是阶段性状态视图，两者不必同一频率。即使每步检查点，外部写入与本地保存之间仍可能存在故障窗口。

## 3. 一次上传怎样获得可核对的结果

```text
C1：文件已处理，待上传
→ 可靠记录操作意图op7（目标、必要参数或引用、稳定幂等键）
→ 请求下游执行op7
→ 下游成功创建report42
→ 本地记录op7的回执report42
→ C2：已上传，可交付
```

若在请求前崩溃，可从意图继续；若请求后回执前崩溃，向下游查询op7，或在其幂等契约有效期内使用同一键重试。若下游不支持查询或去重，程序可能无法安全判定，应进入待核对/人工处理，而不是生成新键再上传。

`call_id`关联一次模型工具请求，`operation_id`表示一个业务逻辑动作，`attempt_id`表示某次网络尝试。重试次数增长不该制造新业务动作。究竟使用哪些ID由接口决定，不必为了这三个名字复制三个完全相同字段。

### 补偿不是把世界退回过去

Compensation（补偿）是新增一项业务操作来缓解已发生结果，例如撤销尚未处理的工单。邮件已经被收件人阅读就不能真正“回滚成没看过”。补偿本身可能失败、需要授权，并且应关联原操作，不是任何错误后都自动补偿。无法确定原动作是否发生时，先核对，避免未发生也做反向操作。

检查点频率因此是重算成本、保存开销和风险的取舍。廉价只读步骤可以粗粒度保存；批准、取消或不可重复写入的关键事实按更严格时机保存。不能把所有步骤都提升为必须永久保存的高风险事件。

## 4. 一个无网络的恢复演练

下面用内存字典模拟“已可靠保存”的两个独立系统，仅用于验证判断逻辑；它**不是磁盘耐久性或真实崩溃测试**。

```python
# runnable-example: recovery_window
from copy import deepcopy

checkpoint = {"done": False, "operation_id": "upload-7"}
remote_receipts: dict[str, str] = {}

def upload_once(operation_id: str) -> str:
    # 模拟下游幂等接口：相同逻辑动作总返回同一个对象。
    if operation_id not in remote_receipts:
        remote_receipts[operation_id] = f"report-{len(remote_receipts) + 1}"
    return remote_receipts[operation_id]

# 模拟“远端成功、本地C2尚未保存”后旧进程消失。
first_receipt = upload_once(checkpoint["operation_id"])
restored = deepcopy(checkpoint)
assert restored["done"] is False
# 恢复先用原操作ID核对/幂等取得回执，而不是新建动作。
receipt = upload_once(restored["operation_id"])
restored.update(done=True, receipt=receipt)
assert receipt == first_receipt
assert len(remote_receipts) == 1
# 反例：新ID不再代表同一动作，会创建第二份报告。
upload_once("upload-7-retry-as-new-operation")
assert len(remote_receipts) == 2
print("recovery-window: assertions passed")
```

这个例子说明正确性来自双方的操作契约，不是“有个checkpoint字段”。实际系统还要处理并发、键有效期、同键不同参数、权限变化以及下游查询失败。

## 5. Resume、Fork、Replay分别改变什么

| 操作 | 目的 | 不能假设 |
|---|---|---|
| Resume（恢复） | 同一任务在明确位置继续 | 摘要就是完整状态 |
| Fork（分叉） | 从某个状态创建另一条探索分支 | 外部数据库和已发邮件也被复制或撤销 |
| State replay（状态重建） | 用已保存事件重建程序状态 | 自动重做真实工具 |
| Model replay（模型重演） | 用选定输入重新请求模型做比较 | 同样输入必得同样答案 |
| Side-effect replay（动作重放） | 再次执行外部动作 | 安全、幂等和环境不变 |

先加载身份与取消状态，检查配置/状态兼容，核对未决操作，恢复必要产物引用与环境，重建模型上下文，再继续执行。Cold resume（冷恢复）要在新进程建立环境；Warm resume（热恢复）可能复用仍存的资源，但都不应省略关键核对。

暂停审批需要记录具体待批动作；取消后旧检查点不能自动让任务重新开始。Worker lease（执行租约）用来协调谁可推进任务，租约过期不代表旧Worker物理停止；Fencing（隔离旧写者）需由实际写入边界检查代次或令牌。

## 6. 产品提供什么，接入者仍要补什么

<details>
<summary>Codex与Claude会话恢复，以及LangGraph检查点的官方边界</summary>

Codex的Thread/rollout记录和Claude Code会话存储可以保留交互、压缩边界和相关状态，支持恢复会话。但它们不能替一个外部邮件、付款或工单API自动建立幂等契约。本章op7账本是业务恢复设计，不应声称两个产品对所有工具默认实现这一账本。

LangGraph官方Persistence文档更明确提供Checkpointer（检查点存储接口），按super-step（调度轮次）保存图状态；同一轮部分节点成功时的pending writes可帮助恢复时不重复已完成节点。`interrupt`恢复时节点会从开头重新运行，因此中断前的副作用仍须幂等或独立封装。`thread_id`是检查点关联键，不等于拥有此ID就有权限，也不等于对所有外部动作提供exactly-once（恰好一次）保证。

</details>

## 7. 应保存多少，由故障后承诺决定

先列出重启后的承诺：不重复上传、保留取消、能取回报告、知道哪些证据未验证。由此决定必要状态和操作记录。然后单独决定诊断采样，不能倒过来“先把一切都记成Trace，再希望恢复时能拼出来”。保留期限和存储成本同样是契约的一部分。

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. Checkpoint的作用是什么，两点之间崩溃怎么办？

<details>
<summary>参考答案</summary>

检查点保存可继续的状态位置，不回滚外部世界。两点间的纯计算可重做；已知成功的写入凭可靠回执补齐；未知写入先靠稳定操作ID查询或按下游幂等契约重试。关键动作记录可以比检查点更细，没有可核对依据就承认未知并请人处理。

</details>

### 2. 为什么工具成功后立刻存检查点仍可能重复？

<details>
<summary>参考答案</summary>

外部成功与本地存档不是同一事务，仍有响应丢失或本地崩溃窗口。需要操作意图、下游幂等/查询以及回执来核对；不能只靠提高检查点频率，也不能每次重试换业务ID。

</details>

### 3. Resume和Compaction、Replay有什么区别？

<details>
<summary>参考答案</summary>

Resume恢复执行；Compaction缩减当前模型输入；Replay可能是用事件重建状态、重新请求模型或重做外部动作，三种风险不同。恢复可以使用摘要构建输入，但不能仅凭摘要决定是否重复写入。

</details>

### 4. Fork需要复制什么？

<details>
<summary>参考答案</summary>

复制允许继承的状态和引用，并明确身份、权限、预算、工作区及资源隔离。已经发生的外部动作不是可以deepcopy或回滚的世界。分叉后的新动作需要自己的权限与逻辑身份。

</details>

### 5. 框架有Checkpointer是否就不需要幂等？

<details>
<summary>参考答案</summary>

仍需要。框架主要恢复图或会话状态，节点重启、中断前代码重跑和外部响应丢失都可能重复副作用。应按框架明确的恢复单位包装动作，并用真实下游契约验证。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| 每秒检查点就没有故障窗口 | 跨系统副作用仍不与本地存档天然原子。 |
| 恢复先把旧Prompt再发一次 | 先核对当前状态、取消与未决副作用。 |
| 补偿等于数据库回滚 | 补偿是新业务动作，也会失败且未必可逆。 |
| 租约到期旧Worker一定停止 | 需在写入边界拒绝旧所有者，不靠时间想象。 |
| 保存全部Trace便能精确重现世界 | 模型、服务和外部事实都可能变化，重演有明确范围。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：上传成功后C2没写，恢复读C1，应直接再上传吗？

<details>
<summary>查看参考答案</summary>

先用原逻辑操作身份核对。如果下游可幂等返回同一对象则补齐本地状态；结果未知且无安全查询/去重能力则暂停处理。

</details>

### 自测 2：读取A的步骤没存检查点可以重做吗？

<details>
<summary>查看参考答案</summary>

若只读可重取且允许当前版本输入，可以重做；若要求当时快照则需要对应保存策略。不是所有步骤都必须完全不重做。

</details>

### 自测 3：事件重建时把所有历史Tool再执行一次有何问题？

<details>
<summary>查看参考答案</summary>

事件已描述动作发生过，再执行会重复副作用且环境可能已变。重建状态通常只应用记录，不执行真实动作。

</details>

### 自测 4：为什么取消意图可能需要独立保存？

<details>
<summary>查看参考答案</summary>

恢复若只读取消前检查点，会再次继续用户已停止的任务。新Worker必须从权威状态知道取消，而不是只看旧模型历史。

</details>

### 自测 5：示例代码证明了什么，没证明什么？

<details>
<summary>查看参考答案</summary>

证明稳定逻辑ID在模拟下游去重时避免重复对象；没证明磁盘耐久、并发安全、真实网络恢复或所有接口幂等。

</details>

### 自测 6：LangGraph中断后重跑节点，与恢复已保存状态矛盾吗？

<details>
<summary>查看参考答案</summary>

不矛盾。框架保存的是定义的图执行边界，不是任意CPU指令。节点代码可能从头运行，因此需要对中断前动作采取幂等或可独立恢复安排。

</details>

## 资料与下一步

官方：[LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Codex App Server](https://developers.openai.com/codex/app-server/)。固定源码：[codex-rs/core/src/session/mod.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/mod.rs)、[utils/sessionStorage.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts)。下一章集中解释授权、批准与沙箱；此处不再重复完整安全流程。

本章对应研究能力：`AGENT-017`、`AGENT-027`、`AGENT-028`、`AGENT-029`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](12-SessionStatePersistence.md) · [模块目录](../README.md) · [下一章 →](14-PermissionApprovalSandbox.md)
