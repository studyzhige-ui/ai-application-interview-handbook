# Run 准入与模型循环｜先确定谁拥有这次运行

[← 产品入口](README.md) · [本产品目录](README.md) · [下一章 →](02-tools-and-resources.md)

修复支付页时，同一线程可能已有未结束请求，也可能刚从检查点恢复。先确定这次 Run 的身份和拥有者，再建立主智能体、输入状态与模型请求，后面的副作用和交付才有明确归属。

<a id="run-admission"></a>
## 请求先通过同线程准入，才取得一个 Run

Gateway 接到请求后，RunManager 先确定用户身份、thread_id、幂等键和多任务策略。幂等键命中时，只能复用同一用户、同一线程的运行；若对应另一个工作器持有的记录，返回只读式存储句柄，不把它登记成自己拥有的运行。否则旧的本地状态会挡住后续请求，甚至覆盖真正拥有者的状态。

同一线程已有 pending、running 或本地 finalizing 工作时，默认 reject 拒绝并发进入；interrupt/rollback 会先处理原运行。正在进行检查点写入时，不能把它当作普通模型 Run 任意打断。单进程锁覆盖本地检查、持久插入和本地登记；多个工作器的竞争还由存储中的活动运行唯一约束处理。[准入与复用](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/manager.py)

准入成功只得到 pending 身份。工作器开始后，装配当前配置、检查点、主模型、工具及中间件，运行才进入实际执行。部署启用运行所有权租约时，当前工作器持续表明自己仍拥有它；丢失租约后，旧工作器不能继续把自己的结果写成权威终态。

**重启分支。** 扫描发现孤立普通 Run 时，恢复者先原子取得接管资格，再把它收束为 error 并补必要交付记录；不会自动从中断的主模型调用原地续跑。批任务另有可重新领取机制，第四章会说明区别。

<a id="1-一次-run-至少涉及四类事实"></a>

## 先走通一个正常 Run

本例固定为：网关接纳用户 `u1` 在会话 `t1` 的请求，创建 `r1`；模型与工具配置有效；文件在可访问工作区内。为先理解运行边界，暂不加入崩溃或恢复。

```text
用户请求
   ↓
网关创建 r1，工作器组装主智能体
   ↓
主模型取得上下文 → 提出读取或修改调用
   ↑                         ↓
   └──────────── 工具检查、执行并回填
   ↓
主模型结束输出 → 工作器收尾与交付 → 持久终态
```

循环中某次工具还可以是 `task`，把一个自包含问题交给子智能体。先不把它视为第二个用户会话：从父模型看，它仍是一项有参数、有结果的工具。

### 同一次运行为什么有多份记录

| 对象 | 保存或反映什么 | 本例的问题 |
|---|---|---|
| Gateway 的 Run 记录 | 本次运行处于哪个阶段 | `r1` 已接纳、运行中还是结束？ |
| LangGraph Checkpoint | 智能体继续所需的状态 | 消息、摘要和扩展字段是什么？ |
| Run Journal / RunEventStore | 运行中产生的事件 | 哪次调用、什么结果、怎样展示？ |
| 工作区与外部服务 | 真实副作用 | 文件是否改变，外部消息是否发出？ |

长期记忆是另一条保存路径，可能还在后台排队。运行状态、继续状态、事件和真实文件各回答不同问题，不因为本轮结束就同时完成提交。[运行层约定][s3-runtime] · [工作器][s3-worker]

<a id="2-停止原因为什么不能都叫任务完成"></a>

### 正常结束与目标满足仍需分别检查

自然最终回答、长度耗尽、安全停止和重复循环都能让运行停止，但后续处理不同。安全终止需抑制不能执行的工具调用，输出截断不能继续执行残缺参数；空停止响应的有限恢复也不是无限重试。

子任务结果可能标为 `completed`，同时带 `token_capped`、`turn_capped` 或 `loop_capped`。因此先看停止原因与可用部分结果，再核对目标，不能只看状态单词。[子任务结果定义][s3-executor]

<details>
<summary>结束保护与错误处理的组装顺序</summary>

`after_model` 逆序分发时，安全处理要先清理不能执行的调用，再让统计与结束处理看到一致结果。主请求的有限模型边界恢复和最终无可见内容兜底，也由实际链路决定。[组装顺序][s3-assembly]

模型错误可能发生在工具提议之前，工具错误却可能已接触外部服务。是否重试要看错误类型、预算与副作用确定性，不能因为安装错误中间件，就认为所有模型、工具和后端共用故障切换政策。[模型错误][s3-llm-errors] · [工具错误][s3-tool-errors]

</details>

<a id="model-loop"></a>
## 主图怎样从一次模型响应走到下一次请求

组装后的图把状态交给模型节点，返回助手消息。正常工具提议进入工具节点，结果按调用 ID 写回消息；下一次模型请求读取更新后的状态，并经过当前中间件投影。这里的“图”是程序规定的节点与转移关系，不是模型任意决定跳进哪个内部函数。

`after_model` 还检查安全停止、输出截断、重复循环与预算。安全停止要先移除不能执行的调用；输出长度截断不能拿半份参数启动工具。无可见内容的普通停止仅有有限恢复机会，不能无限催促模型重来。循环允许停止后，工作器仍检查可交付内容和实际产物，进入第五章的收尾。

模型故障中间件先分类错误，再按全局、异常类型和原因预算的最紧限制重试；并非所有错误可重试。熔断器连续失败后暂时快失败，冷却后只放一个探测请求；旧一代请求的迟到成功不能错误地关闭新一代熔断。控制流中断不应算成提供方故障，探测资格需要释放。[模型错误与有限恢复](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/llm_error_handling_middleware.py)

这条链和工具错误不同：模型失败可能还没产生动作，工具返回错误却可能已经写过文件。持久化与重试不能替代副作用核对。

## 保存下来的东西，不等于模型每次都要看见

`ThreadState` 是程序继续工作时使用的会话状态。`ModelRequest` 是某一次真正发给模型的请求。前者可以保存很多工作线索，后者只取本次需要的内容，还可以临时加入项目说明。

| 内容 | 保存在哪里或从哪里取得 | 模型怎样使用 |
|---|---|---|
| 用户要求、模型响应、工具结果 | `ThreadState.messages`，可由检查点保存 | 近期工作历史；请求阶段仍可能裁剪 |
| 历史摘要 | 独立的 `summary_text` | 请求时作为历史数据加入，不冒充新用户要求 |
| 子任务记录、技能引用 | `delegations`、`skill_context` | 提醒做过什么、结果或技能在哪里 |
| 项目配置及文档目录 | 网关在本次运行开始时固定的快照 | 临时加入请求，不重复写进历史 |
| 已查看图片 | 状态中的路径、大小、哈希等引用 | 发送模型请求时再读取图片字节 |
| 长期用户偏好 | 记忆后端 | 读取有预算的背景，不是每轮全量搬入 |

从状态中选择并重新表示信息，本文称为**请求投影**。例如程序保存日志路径，模型先看摘要与路径，需要细节时再读文件。投影没有另造一份权威事实，也不意味着请求里有的内容都会写回检查点。[状态结构][s0-state]

> ⚠️ **路径不等于内容永远存在。** 引用可以保存下来，文件字节仍受沙箱寿命、同步和权限影响。恢复路径后还要核对文件可读。

<a id="run-trace"></a>

### 跟踪一次“读文件，再决定怎样修复”的运行

以下是教学轨迹，不是实测日志。固定条件：新会话 `t1`，本次 Run 为 `r1`；记忆允许注入且读取成功；项目已选定；`read_file` 可见并获准执行；文件存在。历史很短，本例不触发摘要。

用 `D`、`M`、`U` 分别缩写日期消息、记忆数据、用户原话。它们不是实际消息 ID；项目说明记为 `P`，基础系统指令记为 `S`。

| 时点 | 保存的消息或更新 | 模型看到什么、外部发生什么 |
|---|---|---|
| 用户提交 | 一条原始用户消息 | 文件尚未改变，也没有工具执行 |
| 运行开始的注入完成 | 消息成为 `[D, M, U]` | `M` 是此次读到的长期偏好副本，`U` 仍包含“不要发布” |
| 第一次模型调用 | 不因项目投影而增加历史消息 | 请求使用 `S`、上述消息、临时的 `P` 及当前工具说明；具体角色排列按供应商适配 |
| 模型提出读取 | 追加助手消息 `A1`，含 `read_file` 调用 `c1` | 参数指定支付页文件；**提出调用还没有读取文件** |
| 程序执行读取 | 追加工具结果 `T1`，其 `tool_call_id=c1` | 返回文件内容及适用的读取标记；读取没有修改文件 |
| 第二次模型调用 | 已有 `[D, M, U, A1, T1]` | 模型多看到了真实读取结果，可以判断怎样修复 |
| 后续修改与结束 | 按实际调用继续追加配对消息，最后形成回答 | 只有写工具真正执行后文件才可能改变；读回与测试仍需单独核对 |

这里有两个容易混淆的 ID：**消息 ID** 用于更新消息本身；**工具调用 ID** 用于把一次调用和它的返回结果配对。`A1` 是助手消息的教学标号，`c1` 标识它提出的那次工具调用，不是同一个对象。

检查点在执行过程中的相应位置保存继续状态，Journal 记录事件；启用自动记忆写入时，运行结束还会提交对话给记忆后端。它们不是等文件写完以后一起完成的一笔事务。本例的第二次模型调用仍属于 `r1`，也没有因此重新检索全部长期记忆。[主智能体组装][s0-assembly] · [动态注入][s0-inject] · [工具结果处理][s0-tool-errors]

## 中间件在什么时点改变了什么

中间件是插在执行流程中的处理程序。例如模型调用前加入项目说明，工具执行前检查权限。先认清时点，再看组件名。

| 时点 | 处理对象 | 本例中的作用 |
|---|---|---|
| `before_agent` | 本次运行的初始状态 | 准备目录、上传信息、日期与记忆注入 |
| `before_model` | 下一次模型调用前的状态 | 捕获工作线索，必要时压缩历史 |
| `wrap_model_call` | 本次模型请求 | 临时加入项目、展开摘要、筛选工具说明 |
| `after_model` | 模型刚返回的结果 | 处理安全终止、截断、重复循环与预算 |
| `wrap_tool_call` | 一次工具执行及结果 | 检查许可、规范错误、处理大结果 |
| `after_agent` | 运行结束后的状态 | 提交后台记忆更新及相应结束处理 |

“包装调用”可以用两个处理程序理解。假设按 A、B 注册，它们都继续调用内部处理器，过程是：

```text
A：进入时处理请求
  B：进入时处理请求
    模型或工具实际执行
  B：拿到结果，处理后返回
A：拿到结果，处理后返回
```

因此，**先注册的包装器在外层，进入顺序与返回顺序相反**。若 A 提前拒绝，B 和实际工具都不会运行。这是包装关系的示意，不代表所有钩子都按同一种顺序工作；该快照的 `after_model` 还存在逆序分发，要另外确认。

顺序为何重要？捕获技能引用必须发生在摘要删除旧消息之前；内层工具结果先规范成成功或错误，外层进度记录才能理解它。只列出组件而不看调用方向，无法确认行为。[实际组装与顺序][s0-assembly] · [共同工具构建器][s0-tool-errors]

## 稳定指令、日期和记忆为什么分开放

基础系统提示描述主智能体的行为、目录和工具规则，通常比较稳定。日期和用户记忆会变，把它们频繁插到系统提示开头，会改变本可复用的前缀。分开组织有利于前缀缓存，但是否命中仍取决于供应商与实际请求，不能据此承诺固定节省比例。

信息角色也不同：日期由程序提供；记忆来自过去对话，可能误解、过期或含不可信文本。**被保存过，不会使用户数据升级为系统指令。**

<a id="31-第一次注入怎样保留用户原话"></a>

### 先理解消息合并，再看第一次注入

程序返回的消息更新，不总是整份替换历史。这里使用的 `add_messages` 会按消息 ID 合并：同 ID 更新已有消息，新 ID 追加消息。专门的删除或整值替换是另一些操作。[框架消息合并规则][s0-graph-api]

`DynamicContextMiddleware` 利用这条规则：日期使用 `SystemMessage`（系统消息），记忆使用单独的 `HumanMessage`（用户级数据消息），用户原话也是另一条 `HumanMessage`。

```text
原状态：
  h1          HumanMessage：分析支付页……不要发布。

本次提交给合并器的更新：
  h1          SystemMessage：程序提供的日期
  h1__memory  HumanMessage：先解释风险，再给方案。
  h1__user    HumanMessage：分析支付页……不要发布。

合并结果：
  原位置的 h1 被日期消息替换
  两个新 ID 追加，记忆与用户原话各自保留
```

这里固定为只有一条原始用户消息的初次注入。**ID 决定怎样合并，角色决定怎样解释内容。** 若只替换 `h1` 而不保存 `h1__user`，用户原话就丢了。源码还保留原用户消息的相关属性，不是把用户要求改写成程序指令。[消息构造与注入][s0-inject]

程序注入消息带有来源标记。不能只凭文本含 `<memory>` 或 `<system-reminder>` 就认定是程序生成；用户自己写的同名标签不能冒充这个标记。

<a id="32-记忆是冻结的会话快照不是每次-run-都重新召回"></a>

### 成功注入后，记忆怎样被复用

第一次注入用当前用户原文构造查询，最多取 1000 个字符；有上传说明时优先取保存的原始输入，避免查询被文件描述占满。这是该快照的具体界限，不是通用最佳值。

随后记忆文本作为会话里的冻结副本复用。同一天后端事实即使被修改，后续 Run 也不会仅因为再次调用模型而重新召回。跨日主要补日期提醒。因此要区分**后端最新事实、会话中已注入的副本、本次模型请求**。[查询与冻结分支][s0-inject]

<a id="33-注入超时与关闭记忆不是同一件事"></a>

<details>
<summary>注入失败、关闭记忆与日期时区怎样处理</summary>

前一次注入失败、历史已积累多轮时，补注入选择最后一条合适的用户输入，避免把早期问题追加到末尾，令模型误答旧问题。日期默认使用服务器本地时区，也可由 `DEER_FLOW_DATE_TIMEZONE` 指定 IANA 时区，例如 `Asia/Shanghai`，不是自动跟随浏览器。

异步注入把阻塞读取交给工作线程，调用方约等待 5 秒。允许降级时，本轮可缺少新的记忆与日期更新；要求必须读取记忆的后端则传播 `MemoryReadError`。超时后连失败策略都无法确认，也不能静默当成允许降级。等待超时不保证底层线程已停止。

关闭该智能体的记忆能力时，程序另行移除自己注入的冻结记忆，不把清理寄托在可能超时的读取上。移除会话里的副本，不是清空后端所有事实。[超时、清理与时区实现][s0-inject]

</details>

## 项目和图片为什么只在请求中展开

<a id="41-项目快照固定的是本次配置不是整个文档库的历史版本"></a>

### 项目快照固定的是本次配置

运行开始时，网关固定项目身份、配置和有预算的文档目录。中间件每次据此构造临时项目消息，不把它作为消息状态更新返回，所以检查点不会累积多份项目配置。

项目文字保持用户角色，不能越过系统规则或工具授权。目录固定也不意味着文件内容冻结：项目文档工具按固定项目身份读取实时文档状态。目录中曾有的文件若已被移入回收站，实际读取可以失败；不能用旧目录继续提供已移除内容。[项目边界][s0-architecture] · [请求构造][s0-inject]

<a id="42-图片保存可验证引用发送时读取字节"></a>

### 图片保存引用，发送时核对字节

每个检查点都保存整张 base64 图片，会反复复制大数据。DeerFlow 保存 MIME 类型、大小、路径、SHA-256 与来源沙箱标识；`ViewImageMiddleware` 在模型请求时读取活动沙箱，或核对同步副本的大小和哈希后使用。

这减少的是重复表示，不是撤销存储需求。若路径指向的字节变了，不能把新图悄悄当成上次看见的图。[图片引用][s0-state] · [图片展开][s0-image]

[← 产品入口](README.md) · [本产品目录](README.md) · [下一章 →](02-tools-and-resources.md)

[s0-state]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/thread_state.py
[s0-assembly]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/lead_agent/agent.py
[s0-inject]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/dynamic_context_middleware.py
[s0-tool-errors]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
[s0-graph-api]: https://docs.langchain.com/oss/python/langgraph/graph-api#working-with-messages-in-graph-state
[s0-architecture]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/docs/ARCHITECTURE.md
[s0-image]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/view_image_middleware.py
[s3-runtime]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/AGENTS.md
[s3-worker]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/runtime/runs/worker.py
[s3-executor]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/subagents/executor.py
[s3-assembly]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/lead_agent/agent.py
[s3-llm-errors]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/llm_error_handling_middleware.py
[s3-tool-errors]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
