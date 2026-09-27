# 02｜记忆：从一次对话到可维护的长期事实

[← 上下文](01-context-lifecycle.md) · [DeerFlow 总览](README.md) · [下一篇：工具 →](03-tool-lifecycle.md)

用户在支付页任务中说了两种话：“这次只做最小修复”和“我的长期习惯是先解释风险，再给方案”。它们都值得当前模型注意，但不该拥有相同的保存期限。

前者是这次任务的约束；后者才可能适用于以后不相关的任务。长期记忆的难点不在于把一句话写进文件，而在于**判断它是否值得跨会话复用，并在写错、过期、冲突或删除时仍然保持可控**。

## 1. 先分清记忆接口、记忆实现与会话历史

DeerFlow 用 `MemoryManager` 定义主系统与记忆后端之间的接口。自动写入提交一段对话，默认注入读取一段可用于模型上下文的文本，主动搜索则返回检索结果。接口本身不要求后端必须采用向量数据库，甚至不要求每种后端都存“事实”对象。

默认实现 DeerMem 才负责对话过滤、后台队列、模型提取、事实存储、检索和维护。OpenViking、Honcho、Mem0、Noop 等后端可以通过同一接口接入，但能力不能仅凭名字推定一致。工具模式要求后端真正实现搜索；事实增删改属于可选能力，不支持时应返回明确错误，而不是假装操作成功。[后端接口与能力检查](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/manager.py#L112-L310)

会话历史则属于另一条路径：`messages` 和 `summary_text` 用于继续当前工作。把当前任务摘要存到检查点，不等于已经把它提取为跨会话的用户知识。第一篇中的冻结记忆消息，也只是某次读取结果的副本，不是记忆后端本身。

## 2. 谁的记忆，属于哪个智能体

记忆读写至少要明确用户和智能体两个维度。用户 `u1` 的偏好不能被 `u2` 召回；同一个用户用于通用工作与某个专用智能体的事实，也要按真实作用域组织。

默认 DeerMem 将用户级摘要与智能体级事实分开。用户摘要用于跨智能体的高层背景；具体事实存放在选定智能体的桶中。调用没有指定 `agent_name` 时，DeerMem 会解析到默认智能体桶，不能把接口里的 `None` 一概翻译成“对全部智能体事实做操作”。事实上，读取默认记忆与清空用户全部记忆，对 `None` 的具体处理就不同，必须看调用入口。[默认桶解析与注入](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py#L54-L65) · [管理操作](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py#L492-L585)

进入原始线程或计时器以后，不应重新从一个碰巧存在的全局变量猜用户身份。入队对象直接携带 `user_id`、`agent_name`、`thread_id` 和可用的追踪身份，使异步写入仍对应原来的用户与会话。[队列对象](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py#L47-L117)

## 3. 自动模式和工具模式，改变的是读写路径

`memory.enabled` 控制记忆机制，`memory.injection_enabled` 控制自动注入，`memory.mode` 选择运行方式。这几个开关不是同义词。该快照共享配置的默认模式是 `middleware`，但自定义智能体还可以关闭自己的记忆能力。[共享配置](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/config/memory_config.py#L54-L119)

| 模式 | 写入怎样触发 | 模型一般先看到什么 |
|---|---|---|
| `middleware`，自动模式 | 运行结束后由 MemoryMiddleware 提交对话，后端异步提取 | 在允许注入时，用户级摘要与选定智能体的有界事实 |
| `tool`，工具模式 | 模型显式调用 `memory_add`、`memory_update`、`memory_delete` 等 | DeerMem 默认注入用户摘要，详细事实留给 `memory_search` |

工具模式避免同一批详细事实既自动注入，又经搜索重复返回。但“工具模式绝不自动写”也不是普遍结论：某些依赖会话提取的后端通过 `requires_passive_writes_in_tool_mode` 声明仍需要被动写入。真正生效的链路由模式、后端能力和组装条件共同决定。[模式组装](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py#L644-L669) · [DeerMem 读取分工](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py#L296-L343)

## 4. 自动写入：先筛选，再排队，不让每次工具往返都提取记忆

主智能体完成一轮工作后，`MemoryMiddleware.after_agent` 提交消息给后端。DeerMem 不会把所有内部轨迹都送给记忆模型，而是先保留适合提取的用户与最终助手消息，过滤内部消息和无信息量的确认；若缺少用户或助手一方，也可能直接跳过。

接着识别偏好、纠正、确认等信号。这些信号用于队列接纳与提取提示，不是“已确认真相”。例如“好的”一般不值得单独提取；“以后一直先解释风险”更值得处理；“这次结果不错”则不应自动晋升为终身偏好。[预处理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py#L202-L295) · [自动写入入口](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/memory_middleware.py)

### 4.1 去抖合并的是哪一份输入

去抖（debounce）表示不在每次更新到来时立即处理，而是等待一个间隔，将连续更新合并。DeerMem 按 `(thread_id, user_id, agent_name)` 识别同一目标。正常更新到来时，用最新完整上下文替换该目标尚未处理的正常更新，并合并已经识别的信号。

设连续两次运行都提交了会话：第一次包含 A、B，第二次包含 A、B、C、D。若第一份仍在等待，处理最新完整输入比重复提取两份更合理。源码的计时器属于这条队列，不能从这个身份键进一步推断每个会话都有独立计时器。[去抖与接纳实现](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py#L97-L228)

队列达到普通深度限制时，可以拒绝新的无信号更新；相同键合并不增加深度，带信号和紧急更新仍会被接纳。因此配置的普通队列深度不是所有类型任务都绝不突破的内存硬上限。被拒绝的正常更新不会直接使主任务失败，后续会话重新提交且水位未前进时，还有再次提取的机会；用户不再继续或原消息已消失时，不能保证自动补回。

### 4.2 为什么水位不能只记“上次处理到第 20 条”

压缩会删掉历史开头。原来的第 20 条，可能在新列表中根本不是第 20 条。若仅保存数组索引，下一次就可能越过尚未提取的消息。

DeerMem 水位记录最后提取消息的身份，优先使用消息 ID，没有 ID 时才退回类型与内容。找到该身份，就处理其后的内容；找不到则重新提供完整列表，宁可重复判断，不静默跳过。水位保存在有界进程内缓存中，重启或淘汰会失去它，因此并不是跨进程的“精确一次”提取记录。[消息身份](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L822-L868) · [水位使用](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L1595-L1740)

### 4.3 紧急路径为什么与普通待处理项共存

压缩前提交的紧急消息，只是即将离开历史的一个子集。它不能替换仍在队列中的正常完整会话，否则尚未提取的尾部也可能丢失。因此队列还用 `bypass_watermark` 区分普通与紧急项，紧急提取不读取或推进正常水位。

但两类队列项都在进程内存里。`add_nowait` 的含义是立即安排处理，不是等待事实写完；它与 `shutdown_flush` 的尽力排空，均不把队列升级为持久任务系统。[紧急队列与处理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py#L1-L206)

## 5. 提取：模型判断语义，程序检查它提交的候选

真正的记忆模型结合对话和现有记忆，提出摘要变化、新事实、删除、确认或合并建议。程序随后验证输出结构，再应用更新。

这里要分清两个错误。“用户说的是一次性要求，模型却理解成长期偏好”是语义错误；“模型输出了半截 JSON 或非法置信度”是结构错误。修复后者不能自动解决前者。

### 5.1 一条候选事实怎样被挡下

自动提取的事实携带 `scope`（适用范围）、`durability`（是否适合长期保存）和 `authority`（信息角色）。下面保留该快照的实际门控函数；类型导入和常量一并给出，便于独立观察。它只返回拒绝原因或 `None`，**没有保存文件，也没有修改输入字典**。

<!-- source-example: fact_scope_gate -->
```python
from typing import Any

_FACT_CLASSIFICATION_FIELDS = ("scope", "durability", "authority")


def _normalize_gate_label(value: Any) -> str | None:
    """Normalize a model-produced scope-gate label without validating policy."""
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    return normalized or None


def _fact_scope_gate_reason(fact: dict[str, Any]) -> str | None:
    """Return the deterministic rejection reason for a model-extracted fact."""
    if any(_normalize_gate_label(fact.get(field)) is None for field in _FACT_CLASSIFICATION_FIELDS):
        return "missing"
    if _normalize_gate_label(fact.get("scope")) != "user":
        return "scope"
    if _normalize_gate_label(fact.get("durability")) != "durable":
        return "durability"
    if _normalize_gate_label(fact.get("authority")) != "descriptive":
        return "authority"
    return None
```

输入 `{"scope": "thread", "durability": "durable", "authority": "descriptive"}` 会返回 `"scope"`。输入三项分别为 `user`、`durable`、`descriptive` 时返回 `None`，表示**这一道分类检查**没有拒绝，不表示整条事实已经通过全部验证，更不表示已经持久化。[原函数](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L138-L167)

这种检查让“只属于本任务”“权限指令”等被正确分类的候选不能直接进入长期用户事实。但分类仍由模型产生：若模型错误标注，程序不会凭标签自动理解全部自然语言。记忆保持低权威角色，工具另有授权，是不能省掉的下一层保护。

### 5.2 删除和替换不能只执行一半

结构解析要求有效的更新对象。新事实为空、类型错误、置信度非法或替换项损坏时，需要拒绝对应变化；不能因为旧事实删除项格式完整，就在替代事实无效时先删掉旧内容。

程序还对摘要更新、矛盾删除等设置相应门控，不能把“新增事实有检查”误当成所有破坏性操作已经安全。输入给提取模型的既有记忆也做转义，不让旧记忆中的标签破坏数据分区。[结构规范化](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L138-L320) · [提取提示构造](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L1299-L1405)

自动提取的门控也不能不加说明地套到显式工具写入上。`memory_add` 是另一条用户或模型主动操作路径，需要按自己的参数、身份和存储校验判断，不是先虚构一段对话再经过完全相同的提取过程。

## 6. 保存：兼容 API 的 JSON 形状，不等于全部事实都在一个 JSON 文件

在该快照的默认文件存储中，用户级 `memory.json` 保存用户与历史摘要；智能体事实各自以 Markdown 文件保存。为了兼容调用者，`get_memory` 等接口仍可以返回带 `facts` 数组的文档形状。

因此，看见 API 返回 JSON，不能推出底层就是一个大 JSON 文件；看到搜索索引，也不能把它当作事实的唯一来源。事实文件与摘要是规范数据，索引可以重建。[存储定义](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/storage.py#L1-L96)

### 6.1 并发更新为什么要检查版本

设提取器读取了版本 10，准备合并两条偏好；与此同时，用户手工纠正了其中一条并提交为版本 11。提取器不能直接把基于版本 10 的整份结果覆盖回去。

DeerMem 区分共享清单版本冲突和事实版本冲突。对基于整份快照生成的提取决定，发生相应清单冲突后，会重新读取最新记忆，再把同一组提取建议应用到新快照，有限次重试；删除、合并、容量淘汰因此都重新基于新状态计算。这不是重新调用模型，亦不是任意冲突都无条件重试。[提取提交](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L1441-L1547)

显式新增也可能遇到两个调用同时检查“没有重复”，然后同时写入。工具层提前查重只能节省工作，存储提交路径仍须针对最新快照复核；不能把调用前检查当成并发保证。新增后若容量策略立刻淘汰了这条低优先级事实，也不能返回一个不存在的 ID 并声称“已记住”。[新增的复核与结果](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L1150-L1200)

### 6.2 旧配置和旧文件不是直接丢弃的理由

共享记忆配置只保留启用、模式、注入、退出预算和后端选择等公共字段。DeerMem 的容量、提取模型、去抖等参数放在 `memory.backend_config`。已知旧顶层字段有带警告的兼容迁移，不能把“已迁到后端配置”写成“旧键立即全部失效”。

尤其旧 `storage_path` 若指向 `.json` 文件，与新配置作为根目录的含义不同，程序会特殊处理并警告。迁移已有摘要遇到不能安全合并的冲突时，也不能把损坏或冲突数据当空记忆覆盖。[配置兼容](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/config/memory_config.py#L164-L247) · [存储冲突](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/storage.py#L51-L69)

## 7. 召回：自动注入和主动搜索有不同任务

`get_context` 回答“默认给模型多少长期背景”。DeerMem 在注入预算中组织摘要和事实；开启与查询相关的排序后，还可综合词项相关度、置信度及多样性。没有查询时保留对应的默认排序语义。这里的词项相关排序不是“已经调用语义向量模型”。

`search` 回答“现在需要进一步找哪些事实”。该快照中，开启相关性策略时走作用域内的确定性排序；否则尝试检索适配器，无结果或可降级的适配器故障时，再使用不区分大小写的子串匹配。它不是把所有策略无条件串成固定的三段流水线。[注入与检索分支](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py#L296-L474)

这也解释“索引坏了可以降级”的边界：只要规范事实还能安全读取，就有替代检索路径；如果规范存储自身已损坏，不能悄悄返回空数组并声称用户没有记忆。需要记忆才可执行的后端，还可以要求读取失败中止，而不是继续无记忆运行。[公开错误分类](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/manager.py#L112-L221)

## 8. 维护：纠正、确认、合并、过期和容量不是同一种操作

**纠正**处理冲突。用户说“以后不用先列风险，直接给方案”，可能需要替换原有长期偏好；但“这次直接给方案”只改变当前任务，不能据此删除普遍偏好。解释适用范围，比机械执行“最后一句覆盖前一句”更重要。

**再次确认**提高一条既有事实的稳定性。它可以更新最近确认时间和确认次数，不必新建同义事实。**去重和合并**则减少冗余：提取结果可以先做同类近重复判断，多条事实的归并还需要合法来源标识与适用条件。手工事实会在提取提示中标为较高信任，但这仍然不等于模型永远不能误解它。[确认与候选规范化](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L83-L320) · [手工事实与提取提示](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L1299-L1405)

**过期复查**不意味着一到日期就自动删除。事实可有预计有效天数，超过复查窗口后再成为候选；配置中的受保护类别、单次移除上限等约束继续生效。**容量淘汰**则由每个作用域的 `max_facts` 等配置触发，按所选策略考虑置信度、确认、访问等信息。访问热度属于辅助数据，写入失败不能反过来让已经查到的事实不可用。[过期与合并候选](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L680-L812) · [容量与辅助记录](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L886-L967)

上传事件还有独立的寿命问题。“用户本次上传了某路径的 PDF”通常是会话局部事件，文件以后可能不存在；“用户常处理 PDF”才可能成为跨任务背景。DeerMem 提取提交路径会清理上传相关的会话性描述，不能把临时路径当长期可靠证据。[提交清理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py#L1441-L1547)

## 9. 删除、清空和退出要追到队列与资源

工具模式下，修改或删除通常先搜索得到事实 ID，再调用相应工具。更新结果必须区分“没找到”“不支持”“版本冲突”和“已经持久化”，不能用统一成功文案掩盖差异。[记忆工具](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/tools.py)

清空作用域时，DeerMem 在清空前后取消相同作用域的待处理提取，减少旧计时器把已清事实写回的机会。这个可见调用链证明的是**待处理项取消**；是否还阻止所有已经在执行的写入，要继续检查存储与调用方的并发保证，不能仅凭两个取消调用作全局承诺。

正常退出会给 `shutdown_flush` 一个有上限的排空预算，已经在处理的工作也需计入。返回成功应意味着预算内真正排空；超时或进程被强制终止仍可能丢掉尾部。随后关闭派生检索资源。主任务完成、队列为空、后端关闭、全部事实已保存，是应分别观察的状态。[清空与退出](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deer_mem.py#L505-L585)

## 10. 怎样验证记忆有用，而不是只验证存得更多

本例至少需要覆盖以下判断：长期习惯被正确提取，一次性“不要发布”不被误当永久偏好；`u2` 搜不到 `u1` 的事实；更正后不继续召回冲突旧事实；检索适配器不可用时不谎报规范数据丢失；队列未提交时不宣称已记住。

还要观察最终任务：使用记忆是否减少无谓询问，是否引入过期偏好错误，以及额外输入、提取调用与时延是否值得。可设计相同任务在记忆开关前后的对照，但没有实测数据就不能给出提升比例。本组 [源码小实验](labs/README.md) 只运行上面的确定性门控函数，语义提取、多用户服务与真实模型效果需要另一层测试。

## 本章小结

DeerFlow 的记忆系统将主系统接口与默认 DeerMem 实现分开。一次对话先经过筛选和队列，再由模型提出更新、由程序验证并提交，之后才有可召回的长期事实。维护必须同时关心作用域、错误、冲突、寿命和删除；任何一步“已经调用”都不等于最终存储已经完成。

## 🎯 面试怎么回答

**Q：怎样设计短期到长期记忆的晋升？**

> 先区分当前任务状态和跨任务仍有价值的用户信息。DeerMem 会过滤对话，由模型提出长期事实，再检查范围、持久性和信息角色，经过存储版本检查后提交。以后按作用域与预算召回，还要支持更正、确认、合并和过期复查。自动提取会误判，所以不能把模型给出的分类标签当作语义真理，也不能让记忆成为权限来源。

**Q：使用后台队列后，记忆更新就可靠吗？**

> 要说明队列的介质与确认点。默认 DeerMem 是进程内去抖队列，接收不代表落盘；正常更新可能在后续轮次重新提交，紧急压缩路径则给即将删除的消息一次提取机会。正常退出可以限时排空，但崩溃仍可能丢队列。需要更强保证时，要另外设计持久接收、幂等与恢复，而不是把现有队列描述成精确一次。

## ⚠️ 高频易错点

- **把所有 `None` 都解释成全局。** 默认桶读取与清空所有智能体事实必须按入口分别确认。
- **把 JSON API 当成文件布局。** 兼容返回值与规范事实的存储形态可以不同。
- **把通过门控当成已保存。** 分类检查、完整验证和存储提交是三个不同阶段。

## 本章自测

**任务 A：** 输入候选 `{"scope":"user","durability":"temporary","authority":"descriptive"}`。预测本章函数的返回值，说明它是否修改输入、是否产生磁盘写入。随后把 `durability` 改为 `durable`，解释为何 `None` 也不能证明语义正确。可运行核对见源码小实验。

<details>
<summary>任务 A 提示</summary>

按条件的实际顺序读返回语句，再检查函数是否含存储调用。

</details>
<details>
<summary>任务 A 答案与解释</summary>

第一次返回 `durability`，不修改输入，也不写文件。第二次返回 `None`，仅表示该函数接受这组三项标签；模型可能错误分类原话，其他验证和提交也尚未发生。

</details>

**任务 B：** 自动提取读了版本 10，用户显式修改后存储成为版本 11。题设明确使用具备清单版本检查的提取提交路径。请说明发生冲突后哪些工作重做、哪些不应凭空宣称重做，并解释为什么不能把旧文件直接覆盖回去。

<details>
<summary>任务 B 提示</summary>

回看 `_finalize_update`：更新建议是在循环外解析，还是每次冲突重新调用模型？

</details>
<details>
<summary>任务 B 答案与解释</summary>

发生相应清单版本冲突后，重新读取最新记忆，重新应用同一组已解析的提取建议，有限次重试提交。不能宣称该循环重新调用了模型。直接写回旧快照会抹掉并发修改，尤其会让删除、合并和容量判断基于过期事实。

</details>

下一篇：[03｜工具生命周期 →](03-tool-lifecycle.md)
