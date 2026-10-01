# 会话与恢复｜事件、压缩和故障怎样衔接

[← 上一章](04-plans-goals-and-agents.md) · [本产品目录](README.md) · [下一章 →](06-cross-session-knowledge.md)

前几章已经产生消息、工具结果和任务状态。本章从这些记录的保存方式讲起，再解释如何缩小模型输入、补齐中断边界，以及恢复后还要核对哪些真实资源。

<a id="durability"></a>
## 哪些记录可以作为恢复依据

先建立可信日志这个前提。Session 在内存中追加事件，只说明程序记录了它；持久化后端完成写入，才有进程退出后的恢复依据。**检查点**是在关键动作前等待这些记录保存完成的边界。

基础组合装配 `session-checkpoint-policy`：带会话身份的模型流进入下游前等待刷写，带 Agent 的顶层工具业务执行前也等待刷写；下一次输入处理边界再刷写前一步已提交结果。[检查点源码][checkpoint]

```text
记录模型提出的工具调用
        ↓
flush 成功，记录具备相应持久化依据
        ↓
检查取消，再进入工具业务执行
        ↓
外部文件发生变化
        ↓
返回并记录结果，再完成相应持久化
```

刷写失败时，该受控路径不会继续启动下游模型适配器或工具业务函数。这缩小了“做过动作却完全没有依据”的窗口，但图中外部修改与结果保存之间仍可能中断，所以结果未知仍需外部核验。

> ⚠️ **保障依赖实际组合和入口。** 插件未装配或调用绕开它的链路时，不能套用这项保证。嵌套工具复用外层的持久化边界，不为每个子调用机械增加相同检查点。

模型请求也是同样的顺序：先记录准备发送的输入，再刷写，然后构造和消费下游模型流。刷写成功证明本地记录可依赖，不证明网络已送达。[检查点源码][checkpoint]

<a id="storage-recovery"></a>
## 日志文件损坏与历史格式不兼容，怎样处理

存储恢复首先回答“哪些记录可信”，不猜工具业务结果。末尾未写完与完整记录内部损坏不能混为一谈：可识别的撕裂尾部按规则恢复；完整帧的校验、解压或结构失败则拒绝读取，不能一律当作可忽略尾巴。[后端恢复规则][persistence]

格式升级也不能静默倒退。该快照的格式目录指定写入 V4，并提供相邻旧格式迁移链。若会话目录存在更高的规范代，而本构建无法解释，不能偷偷退回旧代后报告成功；新代可能包含后来发生的调用与结果。[格式目录][catalog]

**可信记录尚未取得时，先解决存储或版本问题；取得以后，才进行后文的语义恢复和外部核验。**

<details>
<summary>存储实现：JSONL、批量同步与尾部修复</summary>

JSONL 表示逻辑上每行一条 JSON 记录；默认物理编码使用带校验和的 Zstandard 压缩帧，不是可以直接用普通逐行文本读取器读取的裸文件。

`create(header)` 可先返回写句柄而不建文件。第一次追加连同头信息以不覆盖既有目标的方式发布并同步；显式 `flush()` 也可实体化只有头信息的会话。

后续事件分批追加，每批完成 `fsync`（请求操作系统同步文件数据）后确认追加；捕获写入或同步失败时尝试恢复此前文件长度。不是每个事件无条件单独刷盘。

末行或末帧撕裂时，后端保留可完整解码的记录，首次新追加前截去破损部分，并可靠重写可恢复记录。完整提交帧的内部损坏不能按同一方式忽略。[持久化与崩溃语义][persistence]

</details>

<details>
<summary>格式迁移与单写者：完整实现的适用范围</summary>

当前目录为 V4，装配 V0 至 V4 的相邻迁移链。只读旧格式时，在内存迁移并验证，不发布新文件；写入时准备当前代、验证、重新核对源文件版本，再不覆盖地发布，旧文件保持原样。物理压缩编码转换与逻辑事件格式迁移不同，后端不自动混用两种编码根目录。[生成目录][catalog]、[后端说明][persistence]

同一会话写句柄有进程内所有权和平台锁。它保护会话日志，不阻止两个不同 Session 的工具修改同一个文件。POSIX 路径依赖原生扩展、文件锁与硬链接等能力；网络文件系统锁可能不可靠；Windows 内核信号量名称又有登录会话范围。这不是已经验证的跨主机分布式锁。[平台限制][persistence]

</details>

<a id="compaction"></a>
## 历史过长时：缩减输入，不混淆记录与记忆

工具读出很长的测试日志，如果每一步都原样携带，后续请求会越来越大。先判断要缩减的对象：

| 动作 | 改变什么 | 后续怎样使用 | 代价 |
|---|---|---|---|
| 结果裁剪 | 过长工具内容的当前表示 | 直接读取保留的头尾 | 中间细节不再内联 |
| 摘要替换 | 可安全选择的旧历史区间 | 摘要加近期尾部进入请求 | 增加摘要请求，可能遗漏语义 |
| 外置或引用 | 大内容本体与可见表示 | 根据定位信息另行读取 | 原件必须仍存在且可访问 |

基础组合在压缩触发后先尝试裁剪过长工具结果；裁剪已使输入低于阈值时，可以不再请求摘要。它不是每次对话都无条件先剪短。[压缩流程][compaction]

### 先预留输出，再计算输入压力

模型窗口同时容纳输入和输出，还要留额外余量。压缩器通过统一 Token 计量服务计入消息、工具等请求成本：

```text
W：当前路由的上下文窗口，单位 Token
O：本次有效输出预留，单位 Token
B：额外安全余量，默认 65,536 Token

触发阈值 = floor(min(W × 0.8, W − O − B))
近期历史的比例预算 = (W − O) × 0.16
```

用教学数值 `W=128000`、`O=8000`、`B=65536` 代入，两个候选阈值是 `102400` 和 `54464`，取较小者；近期比例预算为 `19200 Token`。当前计量若是 `60000 Token`，已经超过阈值，不能只看总窗口还有多大。[预算规则][compaction]

> ⚠️ **先核对单位与容量。** AGENTS 的预算是字节，工具裁剪按字符，以上公式按 Token。若窗口为 32768、输出预留 4096，照搬默认余量会使可用预算非正，应调整路由配置，不是反复摘要就能解决。

### 选择合法区间，再生成能继续任务的摘要

区间选择先给近期尾部留 token 预算，从后往前累计；若切点拆开调用与结果，就移动边界，直到配对完整。最前方系统节点不进入普通压缩区间。压缩的输入是被选中的旧 Surface 节点与兼容请求条件，不等于把全部持久日志无差别发给摘要模型。

不可分的大调用也不能任意拆开；系统提示或工具定义本身太大时，要处理对应来源，单压缩聊天解决不了。

默认摘要指令要求保留八类关系：原始及演变后的目标、技术概念、文件与改动、错误及修复、未完成任务、当前工作、下一步、关键约束。它也要求合并仍然真实的旧摘要而非全文抄回。这是生成合同，不是程序对每项语义正确性的保证。[摘要输入与合同](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/compaction/compaction-basic/src/summarizer.ts)

摘要变短并不保证内容完整。分页任务中，应检查“页码从 1 开始”“不能修改测试”“哪些修改已做、哪些测试未验证”是否都保留下来。若摘要只记住公式，却丢了禁止修改测试的约束，仍会影响任务正确性。

### 验证、提交和失败恢复

提交顺序是验证区间 → 记 start → 异步生成 → 再核对区间稳定与缩减量 → 提交摘要及 Surface 替换 → 记 end → 需要时 flush。失败后尝试记录带错误的 end；连关闭也失败时，留下可检测的未配对 start。此前已完成的工具结果裁剪不会因后续摘要失败自动回滚。手动路径的 flush 失败也不能称为可持久恢复的压缩成功。[区间与提交过程](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/compaction/compaction-basic/src/region.ts)

<details>
<summary>裁剪参数、摘要输出与窗口溢出恢复</summary>

基础裁剪配置为 `thresholdChars=8192`、`headChars=4096`、`tailChars=1024`，描述字符量，不是 Token 预算。[基础组合][base]

摘要辅助请求复用兼容的系统提示、工具和选中历史，再附摘要指令。只有可继续工作的文本进入检查点；推理流、工具调用和不支持的图像输出不能混作摘要。

容量配置无效时，主动压缩警告并跳过，手动压力路径报配置错误；已确认的窗口溢出另有恢复路径。远端返回 `CONTEXT_WINDOW_EXCEEDED` 后，恢复尝试更大的安全头部缩减，并限制恢复次数。允许立即重试的关键是 Surface 的替换代数确实前进，不只是打印了“开始压缩”。

`/compact` 在合适的空闲边界主动压缩。运行轮次或已有压缩期间，不能任意并发改写历史；等待中的新任务仍有队列与唤醒规则。没有有效缩减，就不能无限重发同一超限请求。[自动、手动与溢出路径][compaction]

</details>

图片还有独立恢复路径：支持图片的路由明确返回 `IMAGE_OFFLOAD_REQUIRED` 时，选择最旧的可外置输入出现位置，记录 `image/offload`，随后各路由把这些位置投影为引用占位。真正改变 Surface 后才在同一步重试；不是每次模型失败都删除图片，也不消耗普通提供方重试计数。[图片外置](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/compaction/compaction-image-offload/src/index.ts)

<a id="live-step-repair"></a>
## 活跃步骤出错时，先补齐保守回执

`ToolCallRecovery` 同时用于活跃步骤失败、崩溃日志尾部和 fork 种子。它从助手工具请求开始跟踪调用身份，看到实际 `tool/call` 后记为已启动，看到同一步已提交的追加结果后移出待恢复集合。

调度异常先停止新派发并收束已经启动的调用，再由拥有该步骤的 Agent 为仍缺结果的请求补错误回执。没有启动记录的写“未启动”，有启动记录但没有结果的写“结果未知”；按助手原调用次序提交后，才关闭 step。这补的是协议完整性，绝不伪造成功，也不证明已启动动作被撤销。若连恢复结果都无法提交，保留原错误和恢复错误一起报出。

已关闭步骤的既有历史仍不会被这个尾部机制任意重写。[活跃步骤消费点](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/agent-loop/src/agent.ts)、[恢复状态机](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/session/src/repair.ts)

<a id="semantic-recovery"></a>
## 已经改了文件，却没有结果，先检查什么

先假定存储层已读出可信日志，尾部停在一个尚未结束的 Turn。模型提出了编辑，但没有可靠的最终工具结果。恢复组件会补上用于解释中断的标记，使后续模型能读到结构完整的历史。[恢复源码][repair]

| 打开的执行尾部中留下什么 | 恢复标记 | 下一步判断 |
|---|---|---|
| 助手提出调用，但未记录对应 `tool/call` | `TOOL_NOT_STARTED` | 在该受控中断路径没有启动记录；仍按任务是否需要决定继续 |
| 已有调用记录，缺少对应 `tool/result` | `TOOL_OUTCOME_UNKNOWN` | 结果未知，先检查外部状态 |
| 调用与结果成对保存 | 保留原结果 | 根据结果与任务约束继续核验 |

这些补出的错误是**合成结果**，不是恢复程序重新执行工具取得的回执。`openTurnClosers()` 处理打开的尾部，并补步骤与轮次结束；它不随意修复所有已闭合历史里的缺失结果，也不替代存储损坏检测。

回到分页文件，安全的次序是：

1. 只读检查 `pagination.py` 的内容或差异，确认预期修改是否已经存在。
2. 若修改已存在，继续检查测试，而不是因为没有结果就重复编辑。
3. 若文件与预期不同，结合原任务、实际差异和授权决定补充修改；证据不足时保留未知。

远端创建记录则需要服务端查询、请求幂等键或业务对账。**幂等**指同一逻辑请求重复提交不产生额外业务效果，不是每次重试换个随机请求号。完整跨系统协议由[后端课程](../../../curriculum/05-backend-engineering/README.md)主讲。

> ⚠️ **没有结果不等于没有执行。** 自动重试有副作用的动作前，先证明未执行，或证明可安全重复；不能确定时请求核验或人工介入。本地会话日志与外部系统不是共同事务。

Inbox 也可从已保存增删事件恢复待处理输入，但“仍在队列”“已领取”“已进入请求历史”是不同阶段。恢复需要重建 Agent 活动对象，不能从进程停止的任意一行原地继续。输入调度本身见[第一章](01-boot-and-agent-loop.md#input)。

<details>
<summary>截取历史形成分叉时，为什么“未启动”也要查父会话</summary>

`openTurnClosers()` 支持中断与分叉两类原因。若分叉截取了父会话尚未结束的区间，子分支看不到调用记录，不代表父分支在截取后没有执行。因此分叉的恢复提示要求核验父历史和外部副作用。

这与下文进程内子 Agent 的 fork 提供方不同：后者专门选择父会话已完成 Turn 的前缀，不携带当前未完成轮次。不能因为都叫 fork，就合并两种截取规则。[修复原因分支][repair]、[子 Agent fork][fork]

</details>

<a id="retry"></a>
## 重试必须针对失败原因

| 失败层 | 下一次需要什么条件 | 为什么不能简单再来一次 |
|---|---|---|
| 模型暂时性请求失败 | 实际错误策略允许，预算与取消状态符合要求 | 不能重复注入相同用户输入 |
| 工具参数错误 | 修正不符合要求的参数 | 原样重试仍然错误 |
| 已确认窗口溢出 | 合法压缩真正改变当前历史 | 同一超限请求不会因重发自动变小 |
| 外部副作用结果未知 | 只读核验、幂等协议或对账依据 | 原操作可能已经完成 |

同一步模型重试保留组装结果，不重新执行 `preStep()`；错误链决定哪些失败可重试，具体策略由有效组合决定。窗口恢复要求有效历史替换前进；不可压缩的系统头或巨大单元仍可能使恢复失败。[主循环][loop]、[压缩恢复][compaction]

取消优先于重试。重试记录应能解释失败层、可重试理由、输入或状态变化和剩余预算，而不是把重试次数多当作恢复更好。

[← 上一章](04-plans-goals-and-agents.md) · [本产品目录](README.md) · [下一章 →](06-cross-session-knowledge.md)

[loop]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/agent-loop/src/agent.ts
[surface]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/session/src/surface.ts
[base]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/bundle/base/cordis.patch.yml
[compaction]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/compaction/compaction-basic/README.md
[persistence]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/session/session-persistence-jsonl/README.md
[repair]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/session/src/repair.ts
[checkpoint]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/session/session-checkpoint-policy/src/index.ts
[catalog]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/session/session-format-catalog/src/generated.ts
[fork]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/subagent/subagent-fork-in-process/README.md
