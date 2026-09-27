# 01. 上下文生命周期｜模型这一轮究竟看见什么

[← 模块入口](README.md) · [记忆 →](02-memory-lifecycle.md)

> 实现依据：本模块固定的私有源码快照。图表和消息内容是教学示意；版本身份与功能开关边界见 [README](README.md#学习对象与版本边界)。

## 1. 从一个连续任务开始

假设分页函数把第一页算成了第二页。用户要求：

> 修复分页错误。公开函数的参数和返回类型不能改变；不要删除原测试；最后报告实际运行的测试。

输入是 `[10, 20, 30]`，每页两个元素，页码从 1 开始。第一页应返回 `[10, 20]`，第二页返回 `[30]`，第三页返回 `[]`。这个例子沿用 [AI Coding 分页任务](../../../practice/coding/docs/09-ai-coding.md)，这里观察的不是分页算法，而是代码、需求与测试结果怎样成为模型的判断依据。

第一次请求时，模型可能还不知道函数在哪个文件。它提出搜索和读取请求；程序执行工具，下一次请求才带上真实代码。测试日志很长时，程序又需要选择哪些内容继续携带。

**上下文管理的任务，是在每次模型判断之前组织足够的信息，而不是保存得越多越好。**

## 2. 先把四种状态分开

Context（上下文）在这里指一次模型请求能够使用的信息。它与保存过的信息、已经发生的动作有联系，但职责不同。

| 对象 | 分页任务中的内容 | 改变它意味着什么 |
|---|---|---|
| 程序持有的会话消息 | 用户要求、工具调用、工具结果与内部事件 | 改变后续执行可用的材料 |
| 本次请求的模型输入 | 指令、选中的历史、工具定义与结果 | 改变模型这一轮据以判断的内容 |
| Transcript，会话持久记录 | 磁盘上的消息及恢复关系 | 改变退出后能够重建的历史 |
| 文件与外部系统状态 | 修改后的函数、远端已创建的记录 | 真实动作已经发生 |

例如，测试输出从本次请求中移除以后，日志文件仍可能存在；函数改好以后，最新代码也未必一直留在模型输入中。**消息消失不撤销文件修改，磁盘有记录也不保证本轮发送了它。**

源码中，`messagesForQuery` 从压缩边界后的历史构造；磁盘会话记录由另一组存储逻辑维护。可以分别核对 [查询循环][query-history] 与 [会话存储][session-storage]，不要把它们当作同一个数组的不同名字。

## 3. 一轮用户任务，可以包含多次模型请求

REPL 是接收输入并显示结果的终端交互入口；`QueryEngine` 管理程序化会话。它们进入查询执行过程，`query()` 再委托 `queryLoop()` 循环推进。

先看一个不发生压缩的正常过程：

| 请求 | 本轮新获得的信息 | 模型提出什么 | 程序接下来做什么 |
|---|---|---|---|
| 第一次 | 修复目标与约束 | 读取分页实现 | 调用文件工具，取得代码 |
| 第二次 | 上一步真实代码 | 修改偏移计算 | 执行 Edit，记录结果 |
| 第三次 | 修改结果 | 运行原测试 | 执行测试，取得输出 |
| 第四次 | 测试结果 | 说明修改与验证范围 | 处理本轮结束条件 |

模型响应中的 `tool_use` 是调用请求；程序回填的 `tool_result` 是执行结果。二者通过调用标识配对，模型并不是生成了“读文件”三个字就拥有文件内容。

`query()` 是异步生成器，调用方可以陆续取得事件；真正反复推进的是 `queryLoop()` 中的 `while (true)`，不是每次工具返回都递归调用一次 `query()`。[循环入口][query-loop] 与 [模型调用及结果收集][query-call] 能看到这两层分工。

结束条件还受轮数、预算、取消和停止钩子影响。循环结束只表示这轮执行已停止；分页是否正确，要看文件差异和有效测试。

## 4. 同一份材料，怎样变成请求中的具体字段

先区分三个请求位置：`system` 放系统提示块；`messages` 放用户、助手及工具往返消息；`tools` 放本轮提供的工具定义。它们共同影响模型，但不是三份完整聊天记录。

固定快照中，材料经历以下转换：

| 程序里的材料 | 具体转换 | 到达的位置 |
|---|---|---|
| `systemPrompt` 与 `systemContext` | `appendSystemContext()` 把后者按键和值追加；API 层再生成系统提示块 | 请求的 `system` |
| `userContext`，其中可含 `claudeMd` | `prependUserContext()` 包装成带 `<system-reminder>` 文本的元信息用户消息，放到历史前面 | 请求的 `messages`，角色仍是 `user` |
| 用户要求、助手调用、工具结果 | 历史筛选后，由 API 层规范化并整理调用配对 | 请求的 `messages` |
| 程序工具池 | 筛选本次工具，再生成名称、描述和参数结构 | 请求的 `tools` |

这张表适用于相应材料已加载、路径已启用的情况。`userContext` 为空或 `NODE_ENV` 为 `test` 时，前置包装函数直接返回原消息。`getUserContext()` 本身有缓存，每次请求重新组装不等于每次重新扫描指令文件。[材料生产][context-source] → [上下文包装][context-wrap] → [API 规范化][api-normalize] → [最终请求参数][api-request] 构成可核对的链路。

下面只保留理解关系所需的请求字段。文字、标识和省略的工具结构是教学数据，**不是一份可直接发送的完整 API 请求**；相邻用户消息还可能在规范化时合并。

```json
{
  "system": [{"type": "text", "text": "代码助手的系统指令与环境信息"}],
  "messages": [
    {"role": "user", "content": "<system-reminder>项目约定：保留原测试</system-reminder>"},
    {"role": "user", "content": "修复分页错误，不改变公开接口"},
    {"role": "assistant", "content": [
      {"type": "tool_use", "id": "read_1", "name": "Read", "input": {"file_path": "src/pagination.py"}}
    ]},
    {"role": "user", "content": [
      {"type": "tool_result", "tool_use_id": "read_1", "content": "读取到的分页实现"}
    ]}
  ],
  "tools": [{"name": "Read", "description": "读取文件；参数结构在此示意中省略"}]
}
```

沿着它看：项目约定为任务提供背景，用户消息给出本次目标，`read_1` 把“请求读哪个文件”和“实际读到了什么”关联起来。下一次推理才有了代码证据。`<system-reminder>` 是文本包装，名字中有 system，并不会把 API 角色变成 `system`。

### 指令的作用域决定它什么时候能进入材料

`CLAUDE.md` 承载人工项目约定。根目录指令与子目录指令的适用范围不同，嵌套加载路径用 `loadedNestedMemoryPaths` 记录已经加载的指令，减少重复注入。它与普通文件读取缓存用途不同。[附件与嵌套指令入口][attachments]

排查某个子目录要求为何没被遵守，先看作用域和加载条件，再看实际请求是否包含内容。若根本没有加载，问题还没到模型遵从这一层。

> ⚠️ 注意：指令文本可以影响模型判断，却不强制阻止文件操作。“不得删除原测试”仍需要权限、受保护范围或交付检查配合。公开产品的指令使用方式见 [官方记忆文档][official-memory]；其更新不能反推成固定镜像的行为。

## 5. 请求变长，先辨认压力来自哪里

一条巨大测试日志与长期累积的历史，是不同问题。前者可能只需保留定位线索及原文入口；后者可能需要建立更短的工作历史。

查询循环中的顺序如下，每个阶段都可能不改变消息：

```text
取得压缩边界后的有效历史
  ↓
处理工具结果预算
  ↓
条件性的历史裁剪
  ↓
微压缩：选择适用分支
  ↓
条件性的局部折叠视图
  ↓
判断是否需要自动压缩
  ↓
组装本次模型请求
```

`applyToolResultBudget()` 先处理过大的工具结果；没有相应替换状态时可以不启用。需要恢复的主会话或子智能体路径会记录替换信息，临时辅助查询不必采用相同持久化策略。[预算调用位置][query-history] 与 [预算实现][result-budget] 说明了顺序及保存条件。

例如把重复日志替换为“错误摘要＋原输出位置”，减轻的是模型输入负担。原文件是否仍可读，要另行确认；这与下一节直接清除旧结果内容的路径也不同。

History Snip（历史裁剪）处理选中的历史区间；Context Collapse（局部折叠）把部分历史投影成更短的视图。前者受 `HISTORY_SNIP` 控制，后者受 `CONTEXT_COLLAPSE` 控制。可见调用表明它们在何处参与，不足以补出未展开的内部选择算法。[微压缩及折叠调用][query-compact]

> ⚠️ 注意：把大结果移到文件后，引用失效就可能失去精确证据。关键错误行不足以继续判断时，应重新取得材料，而不是依据“之前看过”猜测内容。

## 6. 微压缩怎样选择分支，为什么与提示缓存有关

Prompt Cache（提示缓存）复用稳定输入前缀的计算。它既不是直接返回旧答案，也不是长期记忆。例如连续两次请求的项目前缀和旧历史相同，只追加新测试结果，就有机会复用前缀；改动很早的历史则可能失去这种复用。

这个快照的 `microcompactMessages()` **先尝试按时间清理，再判断缓存编辑是否可用；都不适用就返回原消息。** 这才是理解本节的基本规则。[实际分支][micro-branches]

| 本次条件 | 采取的动作 | 本地消息内容 |
|---|---|---|
| 时间条件满足，且确有旧结果可清理 | 替换旧的可清理工具结果，保留最近一部分，直接返回 | 返回经过替换的消息 |
| 上述路径没有产生清理结果，缓存编辑条件满足 | 登记工具调用标识；需要删除时安排缓存编辑，由 API 层附加相关信息 | 此路径返回的消息内容不变 |
| 两者均不适用 | 原样返回；后续仍会判断自动压缩 | 不变 |

时间路径要求配置启用、明确的主线程查询来源，以及距最后助手消息足够长的间隔。触发后只处理可清理工具的结果；最近保留数量至少为 1。缓存编辑还检查构建开关、配置、模型支持和查询来源，进入分支也不代表每次都有待删除结果。

### 用四条工具结果看清改变了什么

假设旧结果按出现顺序为 `r1、r2、r3、r4`，都属于可清理工具；本次时间条件满足，配置保留最近两条。四条结果原本都有正常内容。

| 结果 | 处理前 | 时间清理后 |
|---|---|---|
| r1 | 较早的读取输出 | `[Old tool result content cleared]` |
| r2 | 较早的测试输出 | `[Old tool result content cleared]` |
| r3 | 最近的修改结果 | 保留原内容 |
| r4 | 最近的验证结果 | 保留原内容 |

**替换的是结果内容，不是执行历史中的调用身份，也不是磁盘文件。** 本例发生了清理，函数立即返回，不再在这一调用中继续缓存编辑。若只有两条结果且都应保留，就没有内容可清理，程序仍可继续判断下一分支。[时间触发与替换实现][micro-time]

缓存编辑路径则按调用标识安排删除，消息正文在本地保持不变；编辑信息在 API 层加入，后续用 API 返回的实际删除 token 用量计算效果。因此，本地文本长度不能单独证明服务端有效输入或实际节省量。[缓存编辑实现][micro-cache] 与 [请求参数][api-request]

<details><summary>源码边界：旧路径、缓存状态与诊断</summary>

这个快照已移除旧的 legacy 微压缩回退路径。当前的直接内容清理是基于时间的路径，不应再画出一个无条件执行的“普通微压缩层”。

时间清理改变了请求前缀，还会重置缓存编辑状态，避免下一次按旧登记删除已失效的工具引用。缓存编辑则维护待发送与已固定位置的编辑信息，并延后读取实际用量。这里只说明客户端可见动作，服务端命中仍需相应证据。

`promptCacheBreakDetection.ts` 比较系统提示、工具定义及模型设置等客户端状态。它能帮助缩小缓存失效原因，不能单独定位不可见的服务端路由或淘汰。[缓存诊断][cache-diagnosis]

</details>

## 7. 完整压缩保留的是继续执行所需的状态

较小范围处理以后仍有输入压力，自动压缩会考虑组织替代历史。触发判断涉及窗口、输出预留、配置和已有处理结果；失败计数与限制避免无限重复摘要请求。[自动压缩入口][auto-compact]

分页任务不能只缩成“讨论过分页”。一份可继续工作的教学摘要可以是：

> 目标：修复页码从 1 开始的分页，不改变公开接口，不删除原测试。已修改偏移计算；第一页与第二页预期为 `[10, 20]`、`[30]`。测试尚未确认完成。下一步先核查修改差异，再取得测试结果。

它保留了约束、目标结果、已做事项和未确认事项。若删除“测试尚未确认”，后续就可能把计划执行误当成验证通过。必要的工具发现信息与原材料读取线索也要保留；这是一项正确性要求，而不是对每次模型摘要质量的保证。

压缩结果由 `buildPostCompactMessages()` 组织成边界、摘要和保留材料。Session Memory（会话摘要）可能参与部分路径，服务的是当前任务连续性。[压缩结果构造][compact-build] 下一篇会区分它与跨会话记忆。

## 8. 恢复为什么还依赖消息关系和工具发现状态

假设原历史为 `A → B → C`，压缩后用摘要 `S` 加保留消息 `C` 继续，随后产生 `D`。持久记录需要表达新历史怎样接续。若 `D` 接回错误父链，重启后可能重新引入应被排除的旧历史。**摘要内容与恢复关系要一起维护。**[会话存储][session-storage]

工具发现也有结构化状态：先前搜索到的工具名称会影响后续定义加载。压缩若只保留自然语言而丢了发现信息，后续工具可见集合可能改变。源码从消息与压缩边界元数据恢复已发现集合。[工具发现状态][tool-search-state]

## 9. 沿信息消失的位置排查

分页任务压缩后改坏了接口，依次检查：

1. 原始约束来自哪里，是否在有效作用域内加载。
2. 压缩前的实际请求是否包含它。
3. 摘要及后续请求是否仍包含它；若仅重启后消失，再查恢复关系。
4. 若约束一直可见，检查模型提出的动作、权限处理与最终文件差异。

约束从未加载、摘要丢失、请求未发送和模型未遵守，是不同原因。找到第一次消失的位置，比直接更换摘要提示词更有依据。

## 本章小结

用户任务通过多次请求推进。程序把不同来源的材料组织成 `system`、`messages` 与 `tools`，按条件处理过大结果和历史压力。微压缩有明确分支，完整压缩保留继续工作的条件；持久记录与真实文件另有状态。

## 🎯 面试怎么回答

**问：Claude Code 怎样处理长任务上下文？**

它先形成每轮实际请求，而不是把界面历史原样发送。大工具结果先受预算控制，再按条件裁剪、清理或折叠；这个快照的微压缩先尝试时间清理，再判断缓存编辑，都不适用就原样返回。必要时完整压缩。验收要看任务约束、工具发现与恢复关系是否保留，最后确认任务结果，不能只比较文本长度。

## ⚠️ 高频易错点

- `userContext` 是程序命名，包装后的消息仍可以是 `user` 角色。
- 时间清理实际发生后会提前返回；未清理并不代表必定进入缓存编辑。
- 缓存编辑保持本地正文，不等于服务端有效输入完全不变。
- 指令存在、进入请求、被遵守和动作正确，是需要分别确认的事实。

## 本章自测

**任务一：预测分支。** 四条可清理结果中应保留最近两条，但本次没有达到时间条件，缓存编辑也不可用。微压缩返回什么？是否说明整个查询不会再压缩？

<details><summary>参考答案与解释</summary>

原样返回四条结果。这只说明微压缩没有改变消息，后续自动压缩仍可按自己的条件判断。不能仅因结果较旧就假定时间路径发生。

</details>

**任务二：恢复后丢约束。** 摘要保留“不改接口”，磁盘记录也在，但重启后的请求没有摘要。优先检查哪里？

<details><summary>参考答案与解释</summary>

先检查压缩边界、父链与恢复后的有效历史，再检查本次请求组装。现有证据不能支持“模型已看到约束却未理解”的判断。

</details>

**任务三：失效引用。** 一条大测试输出被替换为文件引用，之后文件被清理。继续任务必须知道精确错误行，怎么办？

<details><summary>参考答案与解释</summary>

先从保留的权威位置重新取得日志；若不可得且测试安全可重做，则重新运行并记录新执行条件。无需首先恢复整段聊天，也不能把新结果伪装成原结果。

</details>

## 知识回看与源码定位

- [Agent Loop 课程](../../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md)：回看用户轮次与模型请求的区别。
- [上下文包装函数][context-wrap]、[最终请求参数][api-request]：核对一份材料最终放在哪里。
- [微压缩分支][micro-branches]、[时间清理][micro-time]：核对条件、内容变换与提前返回。

[下一篇：记忆怎样跨轮次与会话发挥作用 →](02-memory-lifecycle.md)

[query-history]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L350-L410
[query-loop]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L219-L330
[query-call]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L650-L870
[context-source]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/context.ts#L113-L190
[context-wrap]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/api.ts#L437-L475
[api-normalize]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts#L1230-L1399
[api-request]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts#L1698-L1728
[query-compact]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L412-L535
[micro-branches]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts#L250-L294
[micro-cache]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts#L294-L398
[micro-time]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts#L421-L540
[attachments]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/attachments.ts
[result-budget]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolResultStorage.ts
[auto-compact]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/autoCompact.ts
[compact-build]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts
[session-storage]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts
[tool-search-state]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolSearch.ts
[cache-diagnosis]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/promptCacheBreakDetection.ts
[official-memory]: https://code.claude.com/docs/en/memory
