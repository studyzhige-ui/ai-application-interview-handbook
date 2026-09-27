# 03. 工具生命周期｜从知道能力到确认动作完成

[← 记忆](02-memory-lifecycle.md) · [模块入口](README.md) · [恢复与验证 →](04-engineering-evaluation.md)

> 实现依据：本模块固定的私有源码快照。工具标识、路径和业务数据为教学示例；版本边界见 [README](README.md#学习对象与版本边界)。

## 1. 模型提出修改，谁真正动了文件

分页任务中，模型决定把偏移从 `page * size` 改成 `(page - 1) * size`。它可以提出 Edit 调用，但生成响应本身不会改写磁盘。

**工具是程序提供的可执行能力，模型生成的是调用请求。** 工具定义告诉模型名称、参数和用途；执行函数、权限与调度把获准请求变成真实动作。[工具接口][tool-type] 与 [执行入口][tool-execution]

例如模型提出调用 `edit_1`，其中包含文件路径、原文本和替换文本。程序必须找到 Edit，核对参数、操作条件与权限，执行修改，再返回与 `edit_1` 配对的结果。只知道工具名字，还没有完成这条链。

## 2. 工具很多时，先分清三个集合

除了本地 Read、Edit，系统还可以接入 MCP。MCP 是 Model Context Protocol（模型上下文协议），让客户端按约定连接外部工具、资源等能力；这里先把它理解为外部能力的接入方式。

外部服务可能提供大量工具。如果每次都给模型发送全部完整说明，会占用输入预算。于是需要区分：

| 集合 | 使用者 | 回答的问题 |
|---|---|---|
| 程序工具池 | 查找、授权、执行与发现逻辑 | 当前程序认识哪些工具？ |
| 本次请求的工具定义 | API 客户端与服务端 | 这次发送哪些定义和加载信息？ |
| 模型本轮可见说明 | 模型 | 本轮可以依据哪些说明选择？ |

工具注册在程序里，不代表完整说明每轮都进入模型上下文；模型看见一个名字，也不代表这次操作获准。

## 3. 按需发现怎样补上工具说明

Deferred Tool（延迟加载工具）不把完整说明无条件放进每轮模型输入。ToolSearch 是发现入口；能否启用取决于配置、能力支持及预算，连接 MCP 本身不等于启用搜索。

假设要读取外部缺陷系统里的分页问题，正常过程是：

1. 模型先看见常驻能力和搜索入口。
2. 模型按任务搜索缺陷读取工具。
3. ToolSearch 返回 `tool_reference`，即指向已知工具的结构化引用。
4. 后续请求从历史恢复已发现名称，纳入对应定义。
5. 模型依据参数说明提出实际调用，再进入校验与授权。

这个镜像的 API 层会过滤 `filteredTools`，保留非延迟工具、搜索入口及已发现工具，再生成请求定义。调用到来时仍以当前工具池查找实现。[发现状态][tool-search-state]、[搜索实现][tool-search] 与 [请求工具定义][api-tools]

<details><summary>源码细节：关键词搜索与两种延迟加载位置</summary>

镜像中的 `select:<tool_name>` 按名称选择。普通搜索检查精确名称、服务端前缀，并对名称组成部分、`searchHint` 和描述匹配评分；带 `+` 的词可以作为必须条件，名称中的精确组成部分通常比描述普通匹配权重更高。应在 `searchToolsWithKeywords()` 核对，它不是向量检索，也不是记忆篇的辅助模型选择。

[官方 Tool Search 文档][official-search] 还描述服务端内置搜索：延迟定义可以已发送给 API，但暂不进入模型可见上下文。它和本镜像的客户端筛选不是同一个步骤。判断时分别看程序工具池、实际请求和模型可见内容。

</details>

MCP 重连、目录变化或压缩以后，历史发现记录还可能存在，工具却已不可用或参数发生变化。发现记录帮助恢复连续性，不能替代当前连接与定义检查。工具说明中的名字、描述和输入结构是执行前提，不是永久有效的授权。

## 4. 一次调用怎样从参数走到执行

Schema（参数结构定义）先检查形状，例如路径是不是字符串；工具的 `validateInput()` 再检查这组值是否适合操作，例如待替换文本能否匹配。然后才处理执行前扩展和权限。

```text
模型提出 tool_use
  ↓
查找当前工具，检查取消状态
  ↓
参数结构解析与工具语义校验
  ↓
PreToolUse：执行前钩子
  ↓
权限判断与必要批准
  ↓
实际 tool.call()
  ↓
执行后处理与结果转换
  ↓
配对的 tool_result
```

Hook（钩子）是在指定阶段接入的程序逻辑，可提供上下文、阻止执行或明确改写参数。找不到工具、结构解析失败或语义校验失败，程序可以返回 `is_error` 的工具结果，而不是凭名称臆造实现。[解析与语义校验][input-validation]

### 参数被改写后，批准与执行针对的是哪一份

用一条正常的“钩子只改参数，不直接批准”的路径看清对象。设模型原本请求修改 `src/pagination.py`，钩子将目标改为 `sandbox/pagination.py`；其他必要参数一并保留，下面只展示路径。

| 时刻 | 路径或对象 | 本阶段确认什么 |
|---|---|---|
| 模型输入 | `src/pagination.py` | 原始调用意图 |
| 初始解析与 `validateInput()` | 原输入解析后的对象 | 这份输入的结构及工具条件 |
| 钩子返回 `updatedInput` | `sandbox/pagination.py` | 明确替换后续处理输入 |
| 正常权限处理 | 使用改写后的输入 | 改写后的操作是否允许 |
| 获准后实际调用 | 使用最终确定的 `callInput` | 对最终输入执行工具 |

这不是“早期校验全部自动重做一遍”。在 `checkPermissionsAndCallTool()` 的这条路径中，初始校验发生在钩子之前；透传改写更新 `processedInput`，权限返回后确定 `callInput`，进入 `tool.call()`，**没有统一跳回最前面的 `safeParse()` 和 `validateInput()`**。[改写与权限传递][input-hooks]、[最终输入选择][input-call]

因此，前面对旧路径的校验不能直接证明新路径的所有条件。权限回调或具体工具内部可能另有检查，必须按各自实现说明；本结论也不是宣称所有工具都存在绕过漏洞。

钩子直接返回允许时，`resolveHookPermissionDecision()` 仍处理需要用户交互或强制 `canUseTool` 的情况，并检查配置中的 deny/ask 规则。返回拒绝则停止；返回 ask 或没有权限决定时走正常权限流程。**Hook 的 allow 不是无条件越过已有拒绝规则。**[权限解析分支][hook-permission]

<details><summary>实现细节：观察用参数与调用参数为何可能不同</summary>

`backfillObservableInput` 在浅拷贝上补充观察字段。文件工具可能把相对路径展开，让钩子和权限更方便判断；`callInput` 初始保留调用参数，避免仅为显示而改动结果文本。

若之后没有真正替换输入，调用可继续使用原参数。若钩子或权限明确提供新对象，真实改动会传向调用；但新路径若只是等于之前的展开值，执行层会恢复模型原来的路径写法，同时保留其他改动。这个处理保护相同文件对象的表达稳定性，不把真正换到另一文件的路径恢复掉。[观察拷贝][input-hooks] 与 [最终输入分支][input-call]

</details>

> ⚠️ 注意：扩展工具或钩子时，核对“校验哪份输入、批准哪个对象、最终执行什么”。仅仅出现过权限函数，不能证明每次参数变化都被相同检查覆盖。

## 5. 权限、批准与沙箱分别限制什么

Permission（权限判断）决定操作是否允许；Approval（批准交互）在需要人决定时取得答复；Sandbox（沙箱）限制相应执行进程可以接触的文件系统和网络。

权限结果常见为 `allow`、`deny`、`ask`。`ask` 需要由当前交互入口处理；没有交互界面时，不能把未弹窗解释为用户默许。[权限规则][permissions] 与 [交互入口][permission-ui]

本地 Read/Edit/Write 使用自己的路径检查与权限系统，不是都先转换成 Bash，再统一经过 shell 沙箱。沙箱包裹的命令进程受该执行边界限制，远端 MCP 服务不自动在本机沙箱中。[官方沙箱说明][official-sandbox] 与 [镜像适配入口][sandbox]

> ⚠️ 注意：批准一次操作不授予所有后续操作；启用沙箱也不等于每种工具都受同一边界控制。判断权限时要知道谁执行、在哪里执行、批准范围是什么。

## 6. 接入 MCP 后，还要管理连接和结果

本地 MCP 服务可以通过 stdio（标准输入输出）与子进程交换消息；远端服务使用相应网络传输。连接后，客户端用 `tools/list` 取得清单，将服务端身份、名称与参数结构转换成程序工具。[客户端实现][mcp-client]

| 阶段 | 本次要确认的事实 |
|---|---|
| 配置与连接 | 服务地址、传输和凭据可用 |
| 清单与转换 | 工具名称能区分服务，参数结构可用 |
| 调用 | 当前连接、参数与权限满足要求 |
| 结果 | 正常返回、业务错误、协议错误或大结果得到对应处理 |
| 恢复与清理 | 按错误类别有限重试，结束时释放资源 |

多个服务可以部分成功。某个服务认证失败，应报告这个服务的状态，而不是把所有工具说成不可用。

<details><summary>连接边界：会话失效、认证与超时</summary>

`isMcpSessionExpiredError()` 同时检查 HTTP 404 和相应 JSON-RPC 信号，以免把错误地址当会话失效。镜像另有远端代理遇到 401 后刷新认证并再试一次的路径，两者职责不同。

默认工具调用等待参数为 `100_000_000` 毫秒，约 27.8 小时，可由环境变量改变。它是快照参数，不是推荐业务时限；连接超时、模型请求超时与用户任务预算另行决定，也不能由等待结束推导远端动作已停止。

通信恢复只恢复连接条件。上一笔写入是否已发生，仍要查业务状态，不能由一次重连获得通用的恰好一次保证。

</details>

Elicitation 是服务端请求用户补充信息的交互，例如填写表单或访问指定地址。客户端仍要处理接受、拒绝、取消和有限后续尝试，不能自动代替用户作出所有决定。[信息补充处理][elicitation]

## 7. Skill 不只返回文字，还可能改变后续执行条件

Skill（技能）组织一种任务做法，例如“先复现分页错误，再作最小修改，最后验证接口”。Tool 负责实际动作；MCP 负责接入外部能力。这三者可以组合，但不是一一对应。

`SKILL.md` 的头部配置影响发现与调用，正文提供指导。Inline（当前会话展开）把材料带入当前执行；fork（分叉执行）为子任务建立上下文，再交回结果。[技能加载][skill-loader] 与 [SkillTool][skill-tool]

### 用一个状态变化理解 `contextModifier`

`contextModifier` 是工具返回的“怎样更新后续执行上下文”的函数，与供模型阅读的消息分开。SkillTool 的正常结果可以同时包含：

| 返回部分 | 作用 | 本例中的结果 |
|---|---|---|
| `data` | 描述技能调用结果 | 哪个技能成功展开 |
| `newMessages` | 给模型的材料 | 分页审查步骤 |
| `contextModifier` | 改变后续程序执行条件 | 更新允许规则或主循环模型配置 |

设技能被允许展开，并提供 `allowedTools = ["Read"]`。消费其修改函数前，命令来源的允许规则为空；消费后，对应规则中新增 Read。**写入规则不会创建 Read 的实现，也不会移除其他既有规则，更不能被理解成“只允许 Read”的工具白名单。** 若技能指定模型，修改函数还会经 `resolveSkillModelOverride()` 更新 `options.mainLoopModel`；指定 effort 时会更新相应状态。[返回消息及上下文修改][skill-modifier]

由此可见，只收到“Launching skill”文字，不足以说明后续状态已经更新。调用方还必须真正消费 `newMessages` 和修改函数，模型材料与程序状态才会分别接上。

技能加载失败或约束没被遵守时，先查是否选中了技能、正文是否进入请求，再看输入冲突、权限与验收。不可信技能、动态命令或外部工具说明，也不能因为带有 Skill/MCP 标签就获得更高信任。

## 8. 多个工具怎样并发，而不越过状态依赖

读取互不依赖的源码和测试，可以在工具声明安全时重叠进行；随后编辑与测试则存在先后关系。调度器依赖工具针对输入给出的 `isConcurrencySafe()` 判断，不是自动理解所有业务依赖。[流式执行器][executor]

结构解析失败或并发判断抛错时，执行器按不安全处理。非并发工具需要独占，形成屏障。因此，在编辑被正确声明为非并发、调用按预期安排的情况下，后续测试不会越过编辑去测试旧文件；错误声明仍会破坏这项前提。

执行器还区分四个状态：

| 状态 | 含义 |
|---|---|
| `queued` | 调用已登记，等待调度 |
| `executing` | 正在执行 |
| `completed` | 结果已收集 |
| `yielded` | 结果已交付消费者 |

结果就绪与交付是两步。进度可及时交付，并发结果也不应一概写成严格按最初调用顺序返回；独占屏障与就绪结果处理是不同约束。[结果收集与交付][executor-results]

### 上下文修改为什么影响并发声明

这个快照收集各工具返回的修改函数，但只对非并发工具把它们应用到执行器的后续上下文。源码明确说明并发工具尚未得到同样支持。[修改函数消费][executor-results]

沿用上一节的状态例子：一个扩展工具准备增加 Read 允许规则。如果它声明并发安全，结果消息可能正常交付，而依赖的共享规则没有按该路径更新。此时问题不是“文件写冲突”，而是后续执行条件没有建立。

> ⚠️ 注意：既返回共享 `contextModifier` 又声明并发安全的扩展，不能只做无数据竞争测试。应先选择串行语义，或实现明确的合并与消费机制，再验证真实调用方。第三方的只读提示也不能单独证明并发安全。

## 9. 取消、失败与丢弃结果各改变哪一层

取消信号通过父子控制器传播，具体工具是否停止，取决于是否处理信号以及副作用发生时机。工具还可声明面对用户新输入时取消或阻塞，其行为不能一概而论。

流式执行器对部分失败作传播：该快照中 Bash 错误可以取消同批兄弟任务；Read/WebFetch 等失败不因此一律取消其他独立读取。[失败传播][executor-results]

`discard()` 用于旧尝试失效后隔离旧执行器结果。例如模型流失败并切换尝试，查询循环会丢弃旧执行器，避免旧调用标识的迟到结果混入新消息。[流失败切换][stream-fallback]

它不是回滚：Edit 已改好的文件不会自动恢复，远端已成功但响应丢失的写入也不会自动消失。继续之前必须区分：停止等待旧结果、请求工作停止、撤销已发生操作。不可安全重复的写入，需要查询确认或服务端幂等支持。

## 10. 回填结果，怎样成为下一次判断的证据

模型提出 `edit_1`，程序完成修改后返回的结果块可用下列教学形式表示：

```json
{
  "type": "tool_result",
  "tool_use_id": "edit_1",
  "content": "分页偏移已替换；尚未运行测试"
}
```

调用标识把结果对应到那次 Edit，而不是所有修改。若执行失败，结果可以带 `is_error: true`，再由后续模型请求决定改参数、补充材料或停止。[执行与结果处理][tool-execution]

“修改成功”支持文件变更已发生，不支持分页语义已正确。测试退出码为 0 也要结合实际命令、工作目录和未被削弱的断言。结果还会进入界面、持久记录及下一轮输入，过大内容受 [上下文预算](01-context-lifecycle.md) 处理。**最终验收需要文件差异和有效测试，不只是一条成功消息。**

## 本章小结

先发现和提供工具说明，再校验、授权、调度并执行，最后配对交付结果。参数改写需要追到最终输入，Skill 的消息与状态修改需要分别消费。权限、沙箱、连接恢复和结果丢弃各有职责，任务正确性仍要独立验收。

## 🎯 面试怎么回答

**问：Claude Code 怎样把模型意图变成受控工具操作？**

模型先依据可见定义提出调用，程序在当前工具池查找并校验，再经过钩子、权限和必要批准，调度实际执行。参数若改写，要确认最终批准及执行对象；结果按调用标识回填，状态修改还要由消费者应用。发现不授权、丢弃结果不回滚，最后以真实差异和测试确认任务，而不是把 JSON 或成功文本当作交付。

## ⚠️ 高频易错点

- 定义是否发送给 API，与是否进入模型上下文是不同问题。
- 旧输入校验通过，不能自动证明钩子改写后的输入通过同样检查。
- 技能的允许规则是程序状态，不是工具实现，也不是全部权限的替代品。
- 结果已就绪、已交付、业务已完成，需要分别确认。

## 本章自测

**任务一：参数换了。** Edit 的原路径已通过校验，透传钩子改成另一文件。怎样判断后续动作是否获准？能否假设语义校验统一重做？

<details><summary>参考答案与解释</summary>

看改写后的输入进入权限处理及最终调用的路径。此执行函数没有统一跳回初始解析和 `validateInput()`；具体权限或工具内部检查要分别核对，不能将旧输入通过的结论套到新对象。

</details>

**任务二：并发结果成功。** 一个扩展工具返回增加允许规则的 `contextModifier`，同时声明并发安全。结果显示成功，是否足以证明下一工具已具备该规则？

<details><summary>参考答案与解释</summary>

不足。此快照只对非并发工具应用收集到的上下文修改。应检查执行器的消费分支，采用串行方式或实现相应合并语义，再验证后续消费者状态；不能只回答“加锁”。

</details>

**任务三：恢复后的旧工具。** 发现记录仍有外部工具名，但 MCP 服务连接失败。可以直接调用吗？

<details><summary>参考答案与解释</summary>

不可以。先确认连接和认证、当前工具目录及参数定义，再进行调用校验与权限判断。历史发现只提供线索，不提供当前可用性。

</details>

**任务四：修改后断流。** Edit 已改文件，模型流失败后旧执行器被丢弃。再次执行前必须看什么？

<details><summary>参考答案与解释</summary>

看实际文件差异，以及原调用、结果和中断时序。丢弃表示旧结果不再正常交付，不表示文件已回滚；确认当前状态与操作可重复性后，再决定重试、跳过或修复。

</details>

## 知识回看与源码定位

- [Tool Contract 课程](../../../curriculum/09-agent/docs/04-ToolContractAndValidation.md)：回看参数结构、语义与结果职责。
- [初始校验][input-validation]、[钩子及权限][input-hooks]、[最终调用][input-call]：沿同一份输入读完整链。
- [Skill 状态生产][skill-modifier] 与 [执行器消费][executor-results]：核对状态修改为何不只是返回文字。

[下一篇：恢复、协作与工程验证 →](04-engineering-evaluation.md)

[tool-type]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/Tool.ts
[tool-execution]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts
[input-validation]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L606-L730
[input-hooks]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L755-L937
[input-call]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L1127-L1227
[hook-permission]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolHooks.ts#L319-L439
[tool-search-state]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolSearch.ts
[tool-search]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/ToolSearchTool/ToolSearchTool.ts
[api-tools]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts#L1207-L1257
[permissions]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/permissions/permissions.ts
[permission-ui]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/hooks/useCanUseTool.tsx
[sandbox]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sandbox/sandbox-adapter.ts
[mcp-client]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts
[elicitation]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/elicitationHandler.ts
[skill-loader]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/skills/loadSkillsDir.ts
[skill-tool]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SkillTool/SkillTool.ts
[skill-modifier]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SkillTool/SkillTool.ts#L766-L867
[executor]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/StreamingToolExecutor.ts
[executor-results]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/StreamingToolExecutor.ts#L263-L445
[stream-fallback]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L705-L743
[official-search]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
[official-sandbox]: https://code.claude.com/docs/en/sandboxing
