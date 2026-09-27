# 01｜上下文：从会话状态到模型真正看到的内容

[← DeerFlow 总览](README.md) · [下一篇：记忆 →](02-memory-lifecycle.md)

修复支付页时，第一条用户消息只有几句话；查日志、读代码、试修复以后，历史可能已经很长。用户最初说过“不要发布”，模型还需要遵守，但没有必要在每轮重读整份日志。

问题因此不是简单的“提示词怎么拼”，而是：**下一次模型调用需要哪些信息，这些信息从哪里来，哪些能缩短，哪些必须保留原来的意义与权限等级？**

## 1. 保存下来的东西，不等于模型每次都要看见

先用具体对象区分三个位置。

| 内容 | 程序保存在哪里或从哪里取得 | 模型怎样使用 |
|---|---|---|
| 用户要求、模型响应、工具结果 | `ThreadState.messages`，可由检查点保存 | 构成近期工作历史；请求阶段仍可能再裁剪 |
| 已压缩的历史摘要 | 独立的 `summary_text` | 请求时重新组织成历史数据，不冒充新用户要求 |
| 子任务记录、加载过的技能引用 | `delegations`、`skill_context` | 提醒做过什么、结果或技能在哪里 |
| 本次项目配置及文档目录 | 网关在运行开始时固定的项目快照 | 临时加入本次请求，不反复写进消息历史 |
| 已查看图片 | 状态保存路径、大小、哈希等引用 | 请求模型时再读取图片字节 |
| 长期用户偏好 | 记忆后端 | 通过有预算的记忆文本进入会话；不是每轮全量搬入 |

因此可把一次 `ModelRequest` 理解为“根据保存的状态和本次运行条件，编排出的一次模型视图”。这里的**投影**不是另造一份权威事实，而是选择和表示已有信息。例如保存日志文件路径，模型只看摘要与路径；需要更多细节时，再调用读取工具。[状态结构](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py#L36-L360)

> ⚠️ **路径不等于内容永远存在。** 图片或文件引用可以持久，文件字节仍受沙箱生命周期、同步和权限影响。恢复了一条路径，不代表已经验证该文件可读。

## 2. 中间件在什么时点改变了什么

中间件是插在执行流程中的处理程序。要读懂它，不必先背类名，先看它是在“一次运行开始”“一次模型调用前”，还是“一次工具调用周围”工作。

| 时点 | 处理对象 | 本例中的作用 |
|---|---|---|
| `before_agent` | 这次运行的初始状态 | 准备会话目录、处理上传信息、执行日期与记忆注入 |
| `before_model` | 即将用于下一次模型调用的状态 | 捕获需要保留的工作线索，必要时压缩历史 |
| `wrap_model_call` | 真正送向模型的请求 | 临时加入项目、展开历史摘要、筛选工具说明 |
| `after_model` | 模型刚返回的结果 | 判断安全终止、输出截断、重复循环及预算等 |
| `wrap_tool_call` | 一次工具执行及其结果 | 检查是否允许执行，规范错误，处理大结果 |
| `after_agent` | 这次运行结束后的状态 | 提交后台记忆更新，执行相应结束处理 |

同一个组件可以参与多个时点，但并不是每个组件都拥有对称的前后处理。组合顺序也不是“清单从上往下运行一遍”：包装调用时，先注册者处在外层，调用向里进入、结果向外返回；`after_model` 的逆序分发又有不同影响。[实际组装与顺序说明](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py#L486-L770)

例如，需要在压缩前从消息捕获技能引用，那么捕获必须先于删除旧消息。工具结果要先带上规范状态，外层进度处理才知道这次是成功还是失败。不能只把几类中间件摆进架构图，就认为先后关系已经正确。[共同构建器](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py#L202-L420)

## 3. 稳定指令、日期和记忆为什么分开放

基础系统提示描述主智能体的行为、工作目录和工具使用规则。它相对稳定。当前日期和用户记忆会变化，若把这些数据频繁插到系统提示开头，就会改变本可复用的前缀。分开组织有利于提示前缀缓存，但**缓存是否命中仍取决于供应商及实际请求**，不能由这段设计直接推出固定的成本收益。

更重要的原因是权限等级不同。当前日期由程序提供；过去对话提炼出的记忆则可能包含误解、过期偏好甚至不可信文本。后者不能因为被保存过，就升级成系统指令。

### 3.1 第一次注入怎样保留用户原话

`DynamicContextMiddleware` 将日期放在 `SystemMessage`（系统消息），把记忆放在单独的 `HumanMessage`（用户级数据消息）。用户真正的输入仍是另一条 `HumanMessage`。其 ID 调整用于配合消息合并规则，不是修改用户要求的含义。

下面是身份示意，不是实际运行日志：

```text
注入前：
  id=h1              HumanMessage：分析支付页……不要发布。

注入后：
  id=h1              SystemMessage：程序提供的日期
  id=h1__memory      HumanMessage：长期偏好，若有可注入记忆
  id=h1__user        HumanMessage：分析支付页……不要发布。
```

原 ID 让日期消息替换原位置，带后缀的新 ID 保存用户原文。记忆和日期具有程序标记，识别时不能只凭文本中有没有 `<memory>` 或 `<system-reminder>`。否则用户自己写一个同名标签，就可能伪装成程序注入的内容。[消息构造与注入](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/dynamic_context_middleware.py#L416-L614)

### 3.2 记忆是冻结的会话快照，不是每次 Run 都重新召回

初次注入会根据当前用户原文构造有界查询，交给记忆后端；上传说明存在时，优先取保存的原始用户内容，避免文件描述占满查询预算。查询最多取 1000 个字符，这是该快照的具体界限，不是通用最佳值。

成功注入后，记忆文本通常随会话历史复用。同一天的后续运行不会因此每次刷新事实；跨日主要补日期提醒。假如前一次注入失败，补注入选择最后一条合适的用户输入，避免把早期问题挪到历史末尾，让模型错答旧问题。因此“每次运行都有自己的模型请求”不等于“每次运行都有新检索的长期记忆”。[查询与冻结条件](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/dynamic_context_middleware.py#L326-L614)

日期默认跟随服务器本地时区，也可由 `DEER_FLOW_DATE_TIMEZONE` 指定 IANA 时区，例如 `Asia/Shanghai`。不应把“当前日期”自动解释成浏览器用户的当地日期。[日期实现](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/dynamic_context_middleware.py#L107-L206)

### 3.3 注入超时与关闭记忆不是同一件事

异步注入把阻塞读取移到工作线程，并给调用方约 5 秒的等待界限。允许降级时，本轮可以没有新的记忆和日期更新；如果后端策略要求必须读取记忆，则传播 `MemoryReadError`。超时时策略仍无法确认，也不能静默当成允许降级。

这条超时不保证底层线程已经停止。关闭该智能体的记忆能力时，程序另行移除自己曾注入的冻结记忆消息，不把这项清理寄托在可能超时的读取上；它也不是清空记忆后端所有事实。[超时与清理分支](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/dynamic_context_middleware.py#L449-L699)

## 4. 项目和图片为什么只在请求中展开

### 4.1 项目快照固定的是本次配置，不是整个文档库的历史版本

运行开始时，网关固定项目身份、配置及有预算的文档目录。`DynamicContextMiddleware` 每次从这份快照构造一条临时项目消息，不把它作为状态更新返回。因此检查点里不会累积很多份过时项目配置。

项目文字仍处在用户角色：即使它是“本次有效项目设置”，也不能越过系统规则或工具授权。项目文档工具则按固定项目身份读取**实时文档状态**。目录快照里出现过的文件，若执行中被移入回收站，实际读取可能失败；不能据此认为项目快照损坏，更不能继续提供已移除的内容。[固定配置与实时读取边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/docs/ARCHITECTURE.md) · [请求构造](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/dynamic_context_middleware.py#L714-L817)

### 4.2 图片保存可验证引用，发送时读取字节

把一张图片转为 base64 放进每个检查点，会反复复制同一份大数据。DeerFlow 的图片状态保存 MIME 类型、大小、路径、SHA-256，以及来源沙箱标识等信息；`ViewImageMiddleware` 在模型请求时读取活动沙箱或经过大小与哈希核对的同步副本。

这样减少的是重复的输入表示，不是撤销图片的存储需求。若引用指向的字节已变，不能把新图片悄悄当成上次看见的那一张。[图片引用定义](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py#L51-L67) · [图片请求展开](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/view_image_middleware.py)

## 5. 历史缩短后，工作线索怎样继续存在

只留下最后几条消息，可能让模型忘记“某个子任务已经查过这份日志”或“先前用过哪个技能”。把所有旧消息都留下，又无法解决长度压力。DeerFlow 用不同状态保存不同线索。

`summary_text` 保存旧历史的语义摘要；`delegations` 保存子任务类型、状态及有界结果引用，不复制整段子对话；`skill_context` 保存技能的名称、路径和简述，不长期复制完整 `SKILL.md`。其中子任务记录需要区分运行身份与工具调用 ID，因为供应商的调用 ID 可能在后续运行中重复。[合并规则](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py#L164-L295)

`DurableContextMiddleware` 做两件事：旧消息还在时捕获重要线索；模型请求时把这些状态重新表示为历史数据。解释这些数据的规则可以是系统指令，但摘要、子任务结果和工具文本本身不能被提升为系统权威。过去网页里的一句“忽略规则”，不能经过摘要就成为新的命令。[捕获与请求投影](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/durable_context_middleware.py)

技能引用留下后，模型需要执行相关技能时仍应读取当前文件。这样既不会把旧正文一直塞进上下文，也避免用旧版技能内容覆盖更新后的文件。`task_history`、任务笔记和工具产物句柄等扩展状态，同样按实际开关接入；不能从 `ThreadState` 中存在字段，推断所有运行已经启用相应能力。

这里还有一个看似反直觉的边界：**文件读取标记随对应工具消息保存；压缩删除那条消息，先读后写标记也会失效。** 系统不能一边让模型忘掉文件内容，一边永久声称它仍了解文件当前版本。重新读取是合理的恢复成本。[先读后写不变量](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py#L1-L36)

## 6. 先处理大工具结果，再考虑历史摘要

### 6.1 工具返回时的外置，可能改变将要保存的 ToolMessage

假设监控工具返回一份很大的日志。`ToolOutputBudgetMiddleware` 可先把全文保存为文件，返回有类型的短摘要、局部预览和路径；无法保存时，再退化为有标记的头尾截断。远程沙箱没有宿主机目录挂载时，需要把结果写到沙箱可见的位置，并检查目标文件确实存在，不能交给模型一条仅宿主机可读的路径。

预算对象是该配置约束的**字符数**，不能直接当成 token 数或 UTF-8 字节数。例如 20000 个中文字符，并不意味着只有 20000 字节，也不保证恰好 20000 token。

重要的是，工具返回阶段会替换结果消息，替换后的 `ToolMessage` 可以进入状态。因此不能概括成“完整工具结果总留在检查点里，只有模型看短版”。全文能否找回，要看外置是否成功，以及收据、日志各自捕获了哪一阶段的内容。[结果替换](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_output_budget_middleware.py#L461-L581) · [远程外置校验](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_output_budget_middleware.py#L189-L234)

### 6.2 请求阶段的裁剪才是“原状态不变”的另一条路径

历史中仍可能有未预算的大结果，请求阶段会再做防御性检查。它还会缩短某些已经失去使用价值的写文件参数：一次 `write_file` 已成功，后来对同一路径又成功读取或修改，且不属于需要保留的近期写入时，可以在模型视图中省去旧的大 `content` 参数。

这个判断不能把同一条模型消息里的并发读取当成“后来已经读过”：调用并发执行时，读取可能发生在写入之前。源码按调用出现位置与对应结果配对，不只按工具调用 ID 全局查找。被先读后写拦住的写入参数则由对应中间件单独缩短。这两类请求改写都不原地修改保存的历史参数。[成功旧写入的省略条件](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_output_budget_middleware.py#L674-L730) · [被拦写入](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py#L345-L471)

## 7. 摘要压缩怎样同时保留语义和协议

工具结果外置以后，多轮历史仍可能接近模型输入界限。自动摘要的大体过程是：

1. 根据配置判断是否需要压缩，并把已有摘要计入触发判断。
2. 选出旧历史，保留近期工作消息、系统消息、程序动态提醒和最新真实用户请求。
3. 用旧摘要与待压缩消息生成替代摘要。
4. 只有摘要生成成功，才调用删除前钩子并形成状态更新。
5. 状态中的消息变成保留部分，新的历史摘要写入独立 `summary_text`。

模型工具调用与其结果必须配对。只剩一条“调用 `c1`”或只剩“`c1` 的结果”，可能让下一次请求违反供应商工具协议。最新真实用户请求也不能仅因为位于较早索引就被丢掉。相反，早期已经完成的用户问题不能因为用了 `__user` 后缀就永久保留。[切分与当前请求保留](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py#L554-L607) · [替换与必要消息保护](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py#L656-L862)

### 7.1 摘要失败为什么不能删除原消息

没有配置专用摘要模型时，工厂采用本次运行实际模型；配置了专用模型而它失败时，可以尝试不同的运行模型。仍然失败，自动路径保留原状态，等待后续处理；手动压缩则应报告失败，不能伪装成“没有需要压缩的内容”。若比例阈值缺少可用上下文窗口信息，还要按工厂逻辑去掉不可用条件或降级，不能自行猜一个窗口上限。[模型选择与失败](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py#L207-L260) · [阈值适配](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py#L865-L960)

摘要本身也是一次模型调用。源码对旧摘要和待压缩消息做结构化分区及 XML 转义，并在这条辅助路径考虑个人信息脱敏，因为它未必经过主请求全部包装层。转义与角色分离是防护的一部分，不是“模型绝不受注入影响”的证明。[摘要输入构造](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py#L454-L547)

### 7.2 紧急记忆 flush 到底保证了什么

旧消息要离开工作历史，自动记忆提取可能尚未处理它们。因此摘要成功之后、删除之前，`memory_flush_hook` 把这批消息交给 `add_nowait`。默认 DeerMem 绕过普通水位，立即调度处理，并让这批消息与同会话的普通待处理更新共存。

**这不是“先确保长期记忆落盘，再提交摘要”的跨存储事务。** 队列位于进程内存，钩子异常会被记录而不阻止压缩；即使成功入队，进程也可能在事实保存前退出。这条设计提供的是删除前的尽力提取机会，而不是零丢失承诺。[钩子调用与异常处理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py#L656-L862) · [紧急入队](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/queue.py#L1-L206)

## 8. 手动压缩与恢复为什么还要经过检查点层

手动压缩先通过 `CheckpointStateAccessor` 读取会话状态，得到摘要和保留消息后，再写一个新检查点。消息使用 `Overwrite`（替换而不是普通合并），否则通道的合并规则可能保留本该移除的旧历史。

允许把原会话送入哪个智能体的记忆桶，要看检查点里服务端记录的绑定。缺少或无法确认绑定时，可以继续允许上下文压缩，但应跳过不能授权的记忆写入。不能相信请求里随便带来的 `agent_name` 就把历史送往另一个长期记忆作用域。[手动压缩完整路径](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/context_compaction.py)

检查点恢复的是状态，随后仍需重新组装模型请求。`full` 与 `delta` 的保存方式及恢复限制由工程篇展开；这里先抓住一条共同规则：**读取会话状态通过访问器，不直接把底层检查点原始字段当成完整消息。** 最终系统消息还需要按供应商协议合并到请求头，避免框架能表示、供应商却不接受的角色排列。[访问器](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/runtime/checkpoint_state.py) · [系统消息归并](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/system_message_coalescing_middleware.py)

## 本章小结

上下文工程是在每次调用前建立合适的模型视图，不是无限堆积消息。保存状态、长期记忆、外置文件和临时请求各有不同生命周期。压缩既要保留任务意义，也要维持工具协议和权限等级；减少输入量不能以丢掉约束或错误宣称持久化为代价。

## 🎯 面试怎么回答

**Q：上下文快满了，怎样压缩而不影响继续执行？**

> 我会先区分当前必须执行的约束、近期工具往返和可外置的大数据。DeerFlow 先预算工具结果，把可继续读取的全文外置；历史仍长时，再把旧对话压成独立摘要，保留当前用户请求及必要消息配对。下一轮由中间件重新加入摘要和技能、委派引用。验收不能只看 token 下降，还要改变条件检查约束是否保留、工具协议是否完整、恢复后文件是否可读。

**Q：压缩前调用记忆 flush，就不会丢长期信息了吗？**

> 不能这样保证。该路径在摘要成功后把待删除消息交给紧急队列，但默认队列在进程内存里，入队与事实落盘是不同事件，钩子失败也不必阻止压缩。它减少遗漏机会，不等于持久消息队列或跨存储事务。业务要求强保证时，需要额外设计可确认的持久接收与恢复机制，不能把这种要求写成上游已有能力。

## ⚠️ 高频易错点

- **把模型视图当成检查点。** 请求中的项目或图片表示不一定持久；工具返回阶段的裁剪又可能直接进入状态。
- **把记忆当成授权。** 用户偏好或历史摘要只能提供背景，不能创建发布权限。
- **把自动降级当成手动成功。** 自动摘要失败保留旧状态，与手动压缩需要明确报错，是不同产品语义。

## 本章自测

**任务 A：** 会话第一轮成功注入“先解释风险”的记忆，第二轮后端该事实被修改，但日期未变、记忆能力仍开启。请预测第三轮是否必然读取新事实，并指出需要观察的对象。可检查结果应区分后端事实、冻结消息和本次请求，不能只回答“会”或“不会”。

<details>
<summary>任务 A 提示</summary>

追 `_inject` 的同日分支；不要把请求时项目投影误认成记忆重新检索。

</details>
<details>
<summary>任务 A 答案与解释</summary>

不必然读取新事实。按已成功注入的正常同日路径，冻结记忆消息继续复用。应分别比较后端事实版本、检查点中的 `__memory` 消息和实际请求，而不是只看最新记忆文件。新会话或其他明确刷新路径需要另行核验。

</details>

**任务 B：** 摘要已经生成，紧急记忆消息成功入队，旧消息从状态删除，随后进程突然退出，队列尚未开始提取。要求画出已完成与未完成的动作，并判断“长期偏好已保存”能否成立。

<details>
<summary>任务 B 提示</summary>

把“摘要状态更新”“队列接收”“记忆事实提交”拆成三个事件。

</details>
<details>
<summary>任务 B 答案与解释</summary>

摘要生成、入队和消息状态更新已经发生，事实提交没有发生。进程内队列会随退出丢失，因此不能宣称长期偏好已保存。历史或外部证据可能仍有其他副本，但这条队列路径没有给出自动恢复保证。

</details>

下一篇：[02｜记忆生命周期 →](02-memory-lifecycle.md)
