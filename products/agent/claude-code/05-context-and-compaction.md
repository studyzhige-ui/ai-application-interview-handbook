# 05. 上下文与压缩｜每次请求怎样保留继续条件

[← 上一章](04-subagents-and-task-ownership.md) · [本产品目录](README.md) · [下一章 →](06-session-and-auto-memory.md)

> 本章依据[私有学习快照及核验边界](README.md#学习对象与版本边界)。示例对象、数字与时间线为教学推演，不是产品运行记录。

<a id="2-先把四种状态分开"></a>
## 1. 先把四种状态分开

Context（上下文）在这里指一次模型请求能够使用的信息。它与保存过的信息、已经发生的动作有联系，但职责不同。

| 对象 | 分页任务中的内容 | 改变它意味着什么 |
|---|---|---|
| 程序持有的会话消息 | 用户要求、工具调用、工具结果与内部事件 | 改变后续执行可用的材料 |
| 本次请求的模型输入 | 指令、选中的历史、工具定义与结果 | 改变模型这一轮据以判断的内容 |
| Transcript，会话持久记录 | 磁盘上的消息及恢复关系 | 改变退出后能够重建的历史 |
| 文件与外部系统状态 | 修改后的函数、远端已创建的记录 | 真实动作已经发生 |

例如，测试输出从本次请求中移除以后，日志文件仍可能存在；函数改好以后，最新代码也未必一直留在模型输入中。**消息消失不撤销文件修改，磁盘有记录也不保证本轮发送了它。**

源码中，`messagesForQuery` 从压缩边界后的历史构造；磁盘会话记录由另一组存储逻辑维护。可以分别核对 [查询循环][query-history] 与 [会话存储][session-storage]，不要把它们当作同一个数组的不同名字。

<a id="4-同一份材料怎样变成请求中的具体字段"></a>
## 2. 同一份材料，怎样变成请求中的具体字段

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

<a id="5-请求变长先辨认压力来自哪里"></a>
## 3. 请求变长，先辨认压力来自哪里

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

例如把重复日志替换为确定性的原文预览和读取位置，减轻的是模型输入负担。原文件是否仍可读，要另行确认；这与下一节直接清除旧结果内容的路径也不同。

History Snip（历史裁剪）处理选中的历史区间；Context Collapse（局部折叠）把部分历史投影成更短的视图。前者受 `HISTORY_SNIP` 控制，后者受 `CONTEXT_COLLAPSE` 控制。可见调用表明它们在何处参与，不足以补出未展开的内部选择算法。[微压缩及折叠调用][query-compact]

> ⚠️ 注意：把大结果移到文件后，引用失效就可能失去精确证据。关键错误行不足以继续判断时，应重新取得材料，而不是依据“之前看过”猜测内容。


### 聚合预算为什么不能每轮重新挑最大的历史结果

预算按 **API 级用户消息组**计算。多个本地工具结果消息在 API 规范化时可能合并为一条用户消息，所以不能只看各条都低于预算；进度、附件也不随意切组。同一个 assistant ID 的流片段归并关系必须保持，否则会漏掉真正超限的组合。[分组和选择][budget-algorithm]

每个会话的 `ContentReplacementState` 保存 `seenIds` 和 `replacements`，将候选结果分成三类：

| 状态 | 本轮动作 | 原因 |
|---|---|---|
| 已替换 | 逐字重放保存的替换文本 | 保持已经发送过的前缀稳定 |
| 已见但未替换 | 冻结原文，不再入选 | 不事后改写先前已缓存的证据 |
| 首次出现 | 按大小降序选择落盘 | 只对新材料作本次预算决定 |

例如同一 API 组有旧结果 A（已替换）、B（已见且保留），又加入新结果 C、D。A 用原有替换文本，B 原文不动；即使 B 比 C 更大，也不能重新挑 B。仅 C、D 按体积排序选择。若冻结部分自身已经超过预算，代码接受这次超额，后续压力交给其他机制处理，而不是破坏冻结规则。

给一组可计算的教学数值：冻结 B 占 50 个预算单位，新 C 占 90、D 占 20，限制是 100。选择阶段合计 160，先选最大的 C，剩余估算为 70；B 即使很旧也不改。若 C 落盘失败，继续使用其原文并记录已见状态，下一轮不能为了同一超额再无限重复落盘。单位只示意算法，实际限制由配置决定。

被选中的结果落盘后，返回的是确定性的原文预览及读取入口，**这一步不调用模型生成语义摘要**。选择时按移除原结果大小估算，不等于保证最终加上预览后恰好不超一个字节；声明 Infinity 合同的 Read 等结果另行跳过。落盘失败就保留原文，并冻结这次决定，避免下一轮无限尝试同一替换。[替换状态][budget-state]

恢复时逐字加载已有 replacement，fork 时复制状态，子 agent 恢复也要补回相关映射。这样恢复前后不因重新生成预览而改变旧前缀；只有文件仍可读，引用才继续提供精确内容。[恢复与复制][budget-replay]
<a id="6-微压缩怎样选择分支为什么与提示缓存有关"></a>
## 4. 微压缩怎样选择分支，为什么与提示缓存有关

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

此快照的直接内容清理由时间条件触发，不存在无条件执行的普通微压缩层。

时间清理改变了请求前缀，还会重置缓存编辑状态，避免下一次按旧登记删除已失效的工具引用。缓存编辑则维护待发送与已固定位置的编辑信息，并延后读取实际用量。这里只说明客户端可见动作，服务端命中仍需相应证据。

`promptCacheBreakDetection.ts` 比较系统提示、工具定义及模型设置等客户端状态。它能帮助缩小缓存失效原因，不能单独定位不可见的服务端路由或淘汰。[缓存诊断][cache-diagnosis]

</details>


<a id="7-主动压缩什么时候触发哪些路径不会同时走"></a>
## 5. 主动压缩什么时候触发，哪些路径不会同时走

这里先算判断使用的窗口，再看功能条件。固定快照的有效窗口是：模型窗口与有效环境覆盖值取较小者，再减去“模型最大输出与 20,000 的较小者”。默认主动压缩阈值再从有效窗口减 13,000；百分比覆盖只能把触发提前，不能放宽到比默认更晚。[阈值计算][compact-threshold]

假设模型窗口 200,000，环境覆盖 180,000，最大输出 32,000，则有效窗口为 `180,000 - 20,000 = 160,000`，默认阈值为 `147,000`。若百分比设为 80%，阈值取 `min(128,000, 147,000) = 128,000`。消息估算还会减去历史裁剪已释放的 `snipTokensFreed`；例如估算 131,000、已释放 5,000，比较值是 126,000，不能只看前一个数字就认定需要压缩。这是公式演算，不是某个线上模型的实测容量。

| 条件 | 对主动压缩的影响 |
|---|---|
| 自动压缩关闭 | 不进入该路径 |
| query 来源是 compact 或 session_memory | 递归保护，避免摘要再给自己摘要 |
| 适用的 reactive-only 模式 | 抑制主动压缩，等相应反应式路径处理 |
| Context Collapse 实际启用 | 由折叠路径处理主动空间压力，不和普通主动压缩争抢 |
| 连续自动压缩失败达到 3 次 | 熔断本段连续失败，避免无限摘要 |

警告、阻塞、手动压缩和自动压缩有不同阈值与入口，不能把它们画成每轮必然依次执行的五层。反应式压缩的可见调用也不等于已审到其内部算法。[开关、互斥与失败状态][compact-gates]

<a id="8-完整压缩产出的是替代历史不是一段随意总结"></a>
<a id="7-完整压缩保留的是继续执行所需的状态"></a>
## 6. 完整压缩产出的是替代历史，不是一段随意总结

触发后会先尝试适用的 Session Memory 路径，失败或不适用时再做普通完整压缩；第六章解释前一种生产与消费合同。普通压缩先取得 PreCompact Hook 的补充要求，用户自定义要求排在前，Hook 要求排在后。

摘要提示要求保留请求意图、技术概念、文件与代码、错误和修复、问题解决、非工具用户消息、待办、当前工作和受最新要求约束的下一步。摘要 agent 不允许调用工具。这是提示层面的结构要求，不是程序逐字段验证摘要必定正确。[摘要合同][compact-prompt]

用已经发生的消息演算一次：

| 压缩前材料 | 摘要需要保留的意义 |
|---|---|
| U1：修复分页，不改接口，不删原测试 | 目标、约束与原始用户要求 |
| R1：读到错误偏移 | 相关文件、原因与必要代码信息 |
| E1：偏移已修改 | 已完成动作，不能再当待执行计划 |
| U2：还要核对空列表 | 最新要求，决定下一步 |
| T1：测试已启动但尚无完成结果 | 当前状态和待确认事项，不能写成通过 |

格式化阶段移除草拟分析块、提取摘要，再加上继续会话的包装与原 transcript 读取路径；自动压缩还给出直接继续任务的提示。原始记录路径提供回查入口，不表示原文又全部进入了当前请求。[摘要包装][compact-format]

返回对象分为 `boundaryMarker`、`summaryMessages`、`messagesToKeep`、`attachments` 和 `hookResults`，构建顺序是：

```text
新边界 → 摘要消息 → 保留消息 → 重建附件 → Hook 结果
```

例如新边界 B、摘要 S、保留的 U2/T1 和附件 A，不是“把 S 插在所有旧历史前面”，而是用这组结构组成继续执行的有效历史。边界还承载恢复时接链所需的元数据，第七章会解释为什么不能直接重写旧消息父指针。[结构与构建顺序][compact-contract]

<a id="9-压缩后怎样重新取得继续工作的材料"></a>
## 7. 压缩后怎样重新取得继续工作的材料

摘要成功后，程序先快照读取状态，再清空读取缓存及 `loadedNestedMemoryPaths`，让后续读取和嵌套指令可重新建立，不能沿用“模型仍看过完整旧文件”的假设。

按最近访问选择重读文件时，快照限制最多 5 个、单文件约 5,000 估算 token、总计 50,000；计划和已知记忆路径不走这一普通文件恢复分支。保留尾部记录过 Read 的路径会参与去重；已知未变更 stub 对应的调用不计入该集合。这里按调用和 stub 标识判断，不额外证明每条历史 Read 都成功。[文件恢复规则][compact-files]

设压缩前读过普通文件 F1…F6，F6 最近、F1 最早；F6 的 Read 已在保留消息内，且不是上述 stub，其余均符合条件且未超预算。程序不必再次注入 F6，而从仍需恢复的候选中按新近程度选取。若另有计划文件 P，它走计划恢复路径；把它算成“第七个普通文件”会错误理解预算。

其他恢复材料也按责任分别生产：

- 运行中或完成未领取的子任务及输出位置，提醒继续收结果
- 计划文件与 plan mode，恢复任务组织状态
- 当前 agent 已调用的技能，按最近调用排序，单技能约 5,000、总计 25,000 估算 token
- 延迟工具发现、agent 列表及 MCP 指令增量，恢复可用能力线索
- SessionStart(compact) Hook 产物，进入压缩后的启动材料

完整压缩从空历史计算这些增量；局部压缩对 `messagesToKeep` 做差，不把保留尾部已经包含的材料全部再复制一次。若已有两项技能、一项未领取子任务，恢复的是有限预算内的技能材料与结果入口，不是把所有子任务探索历史一起塞回来。[状态重注入][compact-reinject]

<a id="10-摘要自身也可能失败失败不能伪造新边界"></a>
## 8. 摘要自身也可能失败，失败不能伪造新边界

普通摘要先走共享缓存的 fork 路径，限制单次轮次且禁工具；失败后才走常规流式回退。媒体替换、特定附件过滤、专用 system prompt、关闭 thinking 等处理属于该回退路径，不能说所有摘要一开始都做了同样预处理。[摘要请求与回退][compact-fallback]

摘要请求仍过长时，程序按 API round 分组裁掉最旧组：能解析 token 差额则据此裁，解析失败约裁 20%，至少留一组，并限制 prompt-too-long 重试次数为 3。需要时加入用户标记并同步 fork 上下文，避免用于摘要的输入与分叉基线分离。[过长输入重试][compact-retry]、[压缩主流程][compact-contract]

摘要失败与主任务工具失败不是同一层。不能把失败摘要当成功替代历史，也不能因为重新做摘要而重执行早已完成的 Edit。主循环保存失败状态，连续失败熔断，真实文件仍需按它已经发生的变化理解。
<a id="8-恢复为什么还依赖消息关系和工具发现状态"></a>
## 9. 恢复为什么还依赖消息关系和工具发现状态

假设原历史为 `A → B → C`，压缩后用摘要 `S` 加保留消息 `C` 继续，随后产生 `D`。持久记录需要表达新历史怎样接续。若 `D` 接回错误父链，重启后可能重新引入应被排除的旧历史。**摘要内容与恢复关系要一起维护。**[会话存储][session-storage]

工具发现也有结构化状态：先前搜索到的工具名称会影响后续定义加载。压缩若只保留自然语言而丢了发现信息，后续工具可见集合可能改变。源码从消息与压缩边界元数据恢复已发现集合。[工具发现状态][tool-search-state]

<a id="9-沿信息消失的位置排查"></a>
## 10. 沿信息消失的位置排查

分页任务压缩后改坏了接口，依次检查：

1. 原始约束来自哪里，是否在有效作用域内加载。
2. 压缩前的实际请求是否包含它。
3. 摘要及后续请求是否仍包含它；若仅重启后消失，再查恢复关系。
4. 若约束一直可见，检查模型提出的动作、权限处理与最终文件差异。

约束从未加载、摘要丢失、请求未发送和模型未遵守，是不同原因。找到第一次消失的位置，比直接更换摘要提示词更有依据。

## 本章小结

用户任务通过多次请求推进。程序把不同来源的材料组织成 `system`、`messages` 与 `tools`，按条件处理过大结果和历史压力。微压缩有明确分支，完整压缩保留继续工作的条件；持久记录与真实文件另有状态。

<a id="面试怎么回答"></a>
## 🎯 面试怎么回答

**问：Claude Code 怎样处理长任务上下文？**

它先形成每轮实际请求，而不是把界面历史原样发送。大工具结果先受预算控制，再按条件裁剪、清理或折叠；这个快照的微压缩先尝试时间清理，再判断缓存编辑，都不适用就原样返回。必要时完整压缩。验收要看任务约束、工具发现与恢复关系是否保留，最后确认任务结果，不能只比较文本长度。

<a id="高频易错点"></a>
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

[← 上一章](04-subagents-and-task-ownership.md) · [本产品目录](README.md) · [下一章 →](06-session-and-auto-memory.md)

[api-normalize]: ../../../references/agent/claude-code-source-index.md#api-normalize
[api-request]: ../../../references/agent/claude-code-source-index.md#api-request
[attachments]: ../../../references/agent/claude-code-source-index.md#attachments
[budget-algorithm]: ../../../references/agent/claude-code-source-index.md#budget-algorithm
[budget-replay]: ../../../references/agent/claude-code-source-index.md#budget-replay
[budget-state]: ../../../references/agent/claude-code-source-index.md#budget-state
[cache-diagnosis]: ../../../references/agent/claude-code-source-index.md#cache-diagnosis
[compact-contract]: ../../../references/agent/claude-code-source-index.md#compact-contract
[compact-fallback]: ../../../references/agent/claude-code-source-index.md#compact-fallback
[compact-files]: ../../../references/agent/claude-code-source-index.md#compact-files
[compact-format]: ../../../references/agent/claude-code-source-index.md#compact-format
[compact-gates]: ../../../references/agent/claude-code-source-index.md#compact-gates
[compact-prompt]: ../../../references/agent/claude-code-source-index.md#compact-prompt
[compact-reinject]: ../../../references/agent/claude-code-source-index.md#compact-reinject
[compact-retry]: ../../../references/agent/claude-code-source-index.md#compact-retry
[compact-threshold]: ../../../references/agent/claude-code-source-index.md#compact-threshold
[context-source]: ../../../references/agent/claude-code-source-index.md#context-source
[context-wrap]: ../../../references/agent/claude-code-source-index.md#context-wrap
[micro-branches]: ../../../references/agent/claude-code-source-index.md#micro-branches
[micro-cache]: ../../../references/agent/claude-code-source-index.md#micro-cache
[micro-time]: ../../../references/agent/claude-code-source-index.md#micro-time
[official-memory]: ../../../references/agent/claude-code-source-index.md#official-memory
[query-compact]: ../../../references/agent/claude-code-source-index.md#query-compact
[query-history]: ../../../references/agent/claude-code-source-index.md#query-history
[result-budget]: ../../../references/agent/claude-code-source-index.md#result-budget
[session-storage]: ../../../references/agent/claude-code-source-index.md#session-storage
[tool-search-state]: ../../../references/agent/claude-code-source-index.md#tool-search-state
