# 状态与恢复｜压缩、检查点和历史分支

[← 上一章](05-delivery-and-goals.md) · [本产品目录](README.md) · [下一章 →](07-memory-pipeline.md)

前几章建立了 Run、消息、工具结果和委派。现在看哪些状态要为下一请求保留，哪些能压缩，以及怎样从过去的检查点形成新的可继续状态。

## 历史缩短后，工作线索怎样继续存在

只留最后几条消息，可能忘记“子任务已经查过这份日志”或“刚才用过哪个技能”。保留全部旧消息又不能解决长度压力。不同线索因此有不同保存方式。

| 状态 | 保留什么 | 不保留什么 |
|---|---|---|
| `summary_text` | 旧历史的语义摘要 | 不承诺逐字还原历史 |
| `delegations` | 子任务类型、状态、有界结果引用 | 不复制完整子对话 |
| `skill_context` | 技能名、路径与简述 | 不长期复制完整 `SKILL.md` |

`DurableContextMiddleware` 在旧消息仍在时捕获线索，在请求时把这些状态重新表示为历史数据。描述如何使用历史的规则可以是系统指令，但摘要、子任务结果与工具文本不能因此获得系统权威。过去网页里的一句“忽略规则”不能经摘要变成新命令。[捕获与投影][s0-durable]

技能引用留下后，真正应用技能时仍应读取当前文件，避免使用过时正文。子任务账本还需要同时区分运行身份和工具调用 ID，因为调用 ID 可能跨 Run 重复。任务笔记、`task_history`、工具产物句柄等扩展状态按开关接入，字段存在不代表本次已启用。[状态合并][s0-state]

> ⚠️ 读取标记随对应工具消息保存。压缩删掉那条消息，先读后写的依据也会失效。重新读取是恢复成本，不应让模型已经忘掉内容，却仍永久持有“读过当前版本”的资格。[读取标记][s0-read-write]

## 摘要压缩怎样同时保留语义和协议

### 先确认启用，再确认触发条件

**历史变长不会自动使所有 DeerFlow 运行进入摘要。** 先看实际加载的配置，再看是否成功构造中间件、是否有可用阈值。[配置类][s0-summary-config] · [摘要工厂][s0-summary]

| 条件 | 自动路径的结果 |
|---|---|
| 配置未启用摘要 | 工厂不安装摘要中间件 |
| 已启用，但无法构造可用运行预算模型 | 本次组装没有可用摘要中间件，并记录警告 |
| 已启用且构造成功，但 `trigger=None` | 可以有中间件，但不会按阈值自动触发 |
| 有可用触发条件且达到阈值 | 尝试压缩；仍要检查可压缩历史、保护消息并成功生成摘要 |

该快照的**配置类默认值**是 `enabled=False`、`trigger=None`、保留最近 20 条消息。部署加载的配置可以覆盖它们，因此不能把类默认值说成所有部署的实际行为。

下面只是教学配置片段，不是完整部署配置：

```yaml
summarization:
  enabled: true
  trigger:
    type: messages
    value: 8
  keep:
    type: messages
    value: 4
```

`trigger` 回答“什么时候开始尝试”，`keep` 回答“希望保留多少近期原消息”。假设检查时计数为 7，不满足这个触发条件；达到 8 时具备触发资格。它不意味着把每组八条固定砍成四条，更不意味着已经腾出某个精确 token 空间：工具配对、当前用户请求等仍受保护；没有可压缩历史时，也不能硬删。

多个触发条件采用“任一满足”。按 token 判断时已有摘要也要计入。比例条件依赖当前运行模型的可用输入窗口；`0.8` 表示八成，不是 `80`。缺少窗口时，工厂警告并去掉不可用比例条件，绝对阈值可继续生效；所有触发项都失效时不自动触发，但构造成功的手动压缩路径仍可工作。比例保留量无法计算时回退到消息保留默认值。[阈值适配与手动路径][s0-summary]

摘要生成模型与容量依据分开：专用摘要模型可以负责写摘要，但触发比例与保留比例按下一次实际接收请求的运行模型窗口计算，不能拿大窗口摘要模型替小窗口主模型决定何时压缩。构造专用模型失败时，本中间件实例固定回退运行模型，不在首次压缩时偷偷再构造一次；配置要求必须推理的模型按其合同开启推理，不能一律强行关闭。

### 达到阈值以后，哪些消息留下

固定为已经启用并成功触发、且存在可压缩历史的运行。处理过程是：

1. 选择旧历史，同时保留近期消息、系统消息、程序动态提醒和最新真实用户请求。
2. 用已有摘要与待压缩历史生成替代摘要。
3. 摘要成功后，调用删除前钩子，再形成消息与 `summary_text` 的状态更新。
4. 下一次请求重新加入摘要及必要工作引用，模型据此继续。

例如历史里有两组已完成的调用：`A1(c1), T1(c1)` 与 `A2(c2), T2(c2)`。前一组若已进入摘要，后一组仍保留，那么下一次请求不能只留下 `A2(c2)` 却没有 `T2(c2)`。调用与结果配对是协议要求，不是文字摘要能替代的内容。[切分与消息保护][s0-summary]

最新用户要求也必须保留。早期已经完成的问题则不能只因 ID 带 `__user` 后缀就永久占据上下文。摘要应保住任务意义，但仍需检查实际内容；不能从安装了压缩器推导约束绝不会丢失。

<a id="71-摘要失败为什么不能删除原消息"></a>

### 摘要失败时，原消息为什么不能删除

新摘要没有生成成功，就没有足够依据用它替换旧历史。自动路径保留原状态；手动压缩应报告失败，不能把失败伪装成“无需压缩”。未配置专用摘要模型时使用本次运行实际模型；专用模型生成失败时，可尝试不同的运行模型。构造失败和生成失败是两个阶段。[模型选择、生成与失败处理][s0-summary]

摘要自身也是模型调用。输入中的旧摘要与旧消息做分区及 XML 转义，并考虑个人信息脱敏，因为这条辅助路径未必经过主请求的全部包装层。转义和角色分离是防护，不是绝无提示注入的证明。

<a id="72-紧急记忆-flush-到底保证了什么"></a>

### 删除前提交记忆，保证的是机会而不是落盘

自动记忆可能尚未处理即将删除的旧消息。因此摘要成功后、删除之前，`memory_flush_hook` 把这一批消息交给 `add_nowait`。默认 DeerMem 立即安排处理，绕过普通水位，并让紧急项与同会话正常待处理项共存。

```text
摘要生成成功
    ↓
紧急记忆更新入队      ← 到这里仍可能没有长期事实
    ↓
会话消息与摘要更新

后台另一条路径：提取 → 验证 → 存储提交
```

> ⚠️ 默认队列在进程内存里，钩子失败会被记录但不必阻止压缩。成功入队后崩溃，事实仍可能未保存。这不是“长期记忆提交成功以后才删除历史”的跨存储事务。[删除前钩子][s0-summary] · [队列][s0-queue]

### 摘要输入与下一请求的摘要投影，也各有预算

“将删除的历史”不等于“摘要模型收到的全部历史”。摘要准备先根据 `trim_tokens_to_summarize` 裁剪生成输入，默认上限 4000 token，可配置为空跳过该裁剪；输入值必须是正整数，不能用布尔值冒充。生成后保存的摘要在下一请求中还有自己的投影限制。因此即使摘要调用成功，仍要分别看选区、摘要输入和最终请求三个边界。

启用 task_continuity 时，归档历史通过与检查点可达批次绑定的搜索/读取工具补回，不能用任意旧分支的归档片段覆盖当前状态。引用入口让模型能补查细节，但读取失败或文件不可达时仍要保留不确定性。[摘要准备](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py)、[历史补读工具](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/task_continuity/tools.py)

## 手动压缩与恢复为什么经过检查点层

Checkpoint（检查点）保存让智能体以后继续的状态。手动压缩先通过 `CheckpointStateAccessor` 读出状态，再写入摘要和保留消息，形成新检查点。

此时不能直接把“只剩 A、B”当普通消息更新：按 ID 合并可能保留旧 C、D。`Overwrite` 表示用给定值整体替换，而不是再次合并。这与前面初次注入利用同 ID 更新，是两种不同目的。[手动压缩][s0-compact] · [访问器][s0-checkpoint]

允许向哪个智能体记忆桶提交历史，要看检查点里服务端记录的绑定。绑定缺少或无法确认时，可以允许上下文压缩，但跳过不能授权的记忆写入，不能相信客户端随意传来的 `agent_name`。

恢复状态以后还要重新组装请求。底层保存为完整状态还是增量，由访问器统一解释，不能直接把原始字段当完整消息。最终系统消息还要按供应商协议归并到请求头。[系统消息适配][s0-coalescing]

<a id="3-检查点保存状态但通道的更新语义仍然有效"></a>

## 检查点怎样保存“接下来从哪里继续”

### 保存状态以前，先明确怎样应用更新

**通道**是状态中的一个字段及其更新规则。例如消息按 ID 合并，某些引用去重追加。恢复不仅要知道新值，还要知道它会替换旧值还是与旧值合并。

假设当前消息 `[A, B, C, D]`，希望恢复为 `[A, B]`：

| 写入方式 | 可能得到什么 | 为什么 |
|---|---|---|
| 普通消息更新 `[A, B]` | `[A, B, C, D]` | 只更新同 ID 消息，没有删除 C、D |
| `Overwrite([A, B])` | `[A, B]` | 明确整体替换该通道 |

DeerFlow 用只变更状态的图写新检查点。图中只有不执行业务的节点，沿用实际智能体的状态结构与检查点机制，不调度模型或工具。这让恢复后的头部处在空闲状态。

自定义中间件可贡献字段，因此必须使用线程实际智能体的完整状态结构；只用基础 `ThreadState`，可能丢掉扩展字段。它们虽没有出现在简化消息表中，仍属于要恢复的状态。[状态变更图与访问器][s3-checkpoint]

<a id="4-full-与-delta-不只是存储大小不同"></a>

### full 与 delta 怎样表示同一份历史

`full` 保存完整累积状态；`delta` 对适用累积通道保存新增写入，并周期保存快照。用只追加消息的算术模型理解：

| 步骤 | 此刻完整消息 | 每步全量保存 | 仅计每步新增 |
|---|---|---:|---:|
| 1 | A、B | 2 条 | 2 条 |
| 2 | A、B、C、D | 4 条 | 2 条 |
| 3 | A、B、C、D、E、F | 6 条 | 2 条 |
| 合计 | 最终仍是 6 条消息 | 12 条次 | 6 条次 |

“条次”计重复序列化，不是最终对话长度。这是教学估算，真实 delta 还含周期快照、元数据与后端开销，不能当成实测节省一半。

读取增量时，要从可用快照结合后续增量恢复完整状态，这叫**物化**。原始 saver（检查点存储器）返回的对象可能只有增量标记，不能直接当完整消息。`CheckpointStateAccessor` 负责选择正确状态结构、检查模式兼容并返回物化结果；只查元数据也要走保留兼容检查的入口。[模式约定][s3-runtime] · [统一读取][s3-checkpoint]

<a id="41-模式兼容不是双向对称"></a>

### 模式切换不是双向对称

该快照默认 `full`。模式与增量快照频率在进程内固定，改变需要重启；共享检查点数据库的进程也需一致解释。

`delta` 进程可把旧 `full` 检查点作为重建起点；`full` 进程不能把 delta 原始数据当完整状态，反向切换须先物化与转换。缺少消息字段不能默认成空列表继续，否则会掩盖模式错误。[兼容与迁移][s3-runtime]

<a id="checkpoint-recovery"></a>
<a id="5-取消编辑重跑和历史分支怎样保持一致"></a>

## 恢复：先选对过去，再写成可继续的状态

<a id="52-找旧检查点要沿亲缘关系不是只看时间"></a>

### 检查点有亲缘关系，不只是一串时间戳

假设 `C0` 保存用户问题，`C1` 保存旧回复。后来从 `C0` 重新回答，形成另一分支 `C2`：

```text
C0：用户问题
├─ C1：旧回复
└─ C2：重新生成的回复  ← 当前分支
```

`C0` 是两个分支的共同祖先，`C1` 与 `C2` 是兄弟。要找 `C2` 的历史，应沿其 `parent_config` 指向的父检查点回溯，不能因为 `C1` 时间接近就把它当祖先。

只有明确的旧数据缺少父链接等兼容条件，才允许有界时间顺序兜底。循环、悬空父节点、目标不匹配或存储错误，要作为错误处理，不能选一份“差不多”的状态。[亲缘查找][s3-lineage]

<a id="42-为什么-delta-的恢复不能随意从旧点分叉"></a>

### 为什么这个快照的 delta 恢复不直接另开分支

上图只说明亲缘关系，并不表示两种模式都采用同一种恢复算法。这个固定实现的 delta 重建会读取沿途祖先的待处理增量；共享祖先上可能还有写向被放弃分支的内容。例如从 `C0` 重答，本应得到“用户问题、新回复”，却可能把 `C1` 的旧回复也带进来。[具体限制与原因][s3-runtime]

DeerFlow 不另写一套祖先增量重放规则，而是在相应根会话恢复路径采取下面的办法：

```text
已有历史：C0 → C1 → C2（当前头部）
目标：回到 C0 的内容，再重新执行

1. 通过访问器，把 C0 读成完整状态
2. 不从 C0 另开一个兄弟分支
3. 在 C2 后写 C3，把全部通道恢复为所选状态
4. 从 C3 继续，产生新的运行结果

最终亲缘：C0 → C1 → C2 → C3 → 新结果
C3 的内容回到所选状态，但历史亲缘继续向前
```

这叫**线性恢复**：状态可以恢复为过去的值，检查点链却在当前头部继续增长。归并通道用 `Overwrite`，只存在于当前头部的较新字段按实际结构恢复默认值，不能构造默认值时用 `None`。旧运行仍在祖先历史中，不是删除所有过去。

该限制针对这里的 delta 根会话恢复路径，不是宣称所有增量存储都不能分支。`full` 不靠同样的祖先增量重放，可保留分叉语义。[工作器恢复实现][s3-worker]

<a id="51-回滚点必须是完整的运行前状态"></a>

### 取消回滚需要完整的运行前状态

工作器开始执行前捕获完整可物化状态、检查点位置与相应待处理写。捕获失败就禁用相应回滚能力，不能拿半份数据当安全恢复点。

取消并选择回滚时，`full` 可基于运行前检查点形成新头；`delta` 则在当前头部完整恢复捕获的通道，避免引入兄弟增量。实际智能体扩展字段与服务端绑定也要保留，不能从客户端任意字段重建授权。[捕获与回滚][s3-runtime] · [工作器][s3-worker]

编辑旧输入再运行，会先形成临时替代历史。新运行失败、超时或中断时，需要恢复运行前状态，并在流结束前通知客户端恢复值，否则界面会停留在没有成功完成的新历史。

<a id="53-为什么历史分支不能复制今天的工作区"></a>

### 消息回到过去，不代表文件也回到过去

假设第一轮还没有 `report.md`，第二轮才生成文件，第三轮又修改它。现在从第一轮分支，直接复制当前工作区会把未来文件带进去。

没有每轮完整文件快照时，DeerFlow 的历史轮次分支不复制当前工作区；最新轮次分支才可尽力复制当前文件。此时正确的结论是“消息可恢复，但没有依据还原完整历史文件”，而不是用当前文件冒充过去。[线程生命周期][s3-thread]

> ⚠️ **状态回滚不撤销外部世界。** 文件修改、已发送消息和远端数据库变化，需要另行核验，必要时做业务幂等或补偿。检查点、日志与长期记忆都不是副作用的自动逆操作。

<a id="6-日志与实时流为什么不能直接代替检查点"></a>

## 继续状态与历史界面怎样对齐

`RunJournal` 把模型、工具与运行回调组织成可持久事件；RunEventStore 为界面提供历史。实时 token 片段便于逐字显示，却不必全部成为永久消息记录。检查点回答怎样继续，事件回答发生过什么，两条路径必须使用一致的身份解释。[Journal][s3-journal]

<a id="61-同一次模型响应回调两次不能变成两条答案"></a>

### 同一次响应的两次回调，不是两条答案

供应商可能先回调模型响应，随后按同一模型运行 ID 补充用量。Journal 合并相邻的对应信息，保留首份响应内容与适用的用量补充，避免重复展示和统计。晚到回调不能任意改写已追加历史。

这是产品侧计量处理，不证明供应商实际收费两次。诊断时先区分“真调用两次”和“一次调用回调两次”。[响应合并约定][s3-runtime]

<a id="62-历史界面与检查点需要共享轮次身份"></a>

### 分支继承与断线续读都需要边界

分支继承检查点消息，却没有相应事件时，界面可能只显示新轮次。因此需要补齐继承历史对应事件，并为不同用户轮次提供适当运行身份，不能全部共用一个可被整体替换的 ID。[线程历史][s3-thread]

客户端断线后可按序号继续获取事件。所需区间已经丢失时，应报告重放缺口，让客户端重新读取持久状态，再建立一致视图，不能从最早剩余事件假装无缝继续。[事件流协议][s3-stream]

<a id="63-补齐悬空工具调用只修复了消息协议"></a>

### 补上工具结果消息，不证明动作没有发生

中断可能留下工具调用却没有配对结果。`DanglingToolCallMiddleware` 在后续模型调用前补齐相应协议表示，避免供应商拒绝请求。

但补出的错误只修复消息协议。如果外部服务已经接受操作，结果只是丢在返回途中，真实动作仍需查服务端或执行证据。这正是“模型可以继续”与“业务状态已经查清”的区别。[悬空调用处理][s3-dangling]

[← 上一章](05-delivery-and-goals.md) · [本产品目录](README.md) · [下一章 →](07-memory-pipeline.md)

[s0-state]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/thread_state.py
[s0-durable]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/durable_context_middleware.py
[s0-read-write]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py
[s0-summary-config]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/config/summarization_config.py
[s0-summary]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py
[s0-queue]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py
[s0-compact]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/context_compaction.py
[s0-checkpoint]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/checkpoint_state.py
[s0-coalescing]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/system_message_coalescing_middleware.py
[s3-runtime]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/AGENTS.md
[s3-worker]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/worker.py
[s3-checkpoint]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/checkpoint_state.py
[s3-lineage]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/app/gateway/checkpoint_lineage.py
[s3-thread]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/docs/THREAD_LIFECYCLE.md
[s3-journal]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/journal.py
[s3-stream]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/docs/RUN_EVENT_STREAM.md
[s3-dangling]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/dangling_tool_call_middleware.py
