# 03. Skill、Hook 与 MCP｜扩展怎样进入执行并交回结果

[← 上一章](02-tool-execution-and-permissions.md) · [本产品目录](README.md) · [下一章 →](04-subagents-and-task-ownership.md)

> 本章依据[私有学习快照及核验边界](README.md#学习对象与版本边界)。示例对象、数字与时间线为教学推演，不是产品运行记录。

<a id="1-扩展要接入同一条运行链"></a>
## 1. 扩展要接入同一条运行链

上一章已有工具池、权限、调度与结果消费者。扩展能力应补入这些位置，而不是另开一条不受控制的执行通道：Skill 提供任务做法并可改变运行方式，Hook 在阶段边界产生反馈，MCP 把外部协议能力适配成工具。

下面先跟踪 Skill 从文件变成一次可消费的调用，再回到 Hook 的作用点，最后看远端工具如何经过同一套执行链。

<a id="2-技能从文件到可调用目录"></a>
## 2. 技能从文件到可调用目录

加载器从受设置与策略控制的目录发现技能，读取 `SKILL.md` 的头部与正文。描述决定发现信息；是否允许模型调用、`allowed-tools`、模型、effort、Hook 与 fork 配置则会影响后续执行。配置不能仅当作展示元数据。[技能配置][skill-config]

多来源合并按真实文件身份去重，避免同一文件通过不同路径重复出现。带路径触发条件的技能先登记为待激活，只有相关条件满足后才参与发现，不能把“已扫描目录”说成“模型本轮已看见全部技能”。[目录合并与激活入口][skill-catalog]

调用时仍要检查技能存在、可被该入口调用且通过权限。把一个技能名字放入提示词，不会自动创建它，也不能让标记不可由模型调用的技能绕过准入。
<a id="3-inline-让正文和状态在主会话中分别生效"></a>
<a id="7-skill-不只返回文字还可能改变后续执行条件"></a>
## 3. Inline 让正文和状态在主会话中分别生效

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


<a id="4-fork-把技能放入独立的子任务上下文"></a>
## 4. Fork 把技能放入独立的子任务上下文

fork 技能不只是把正文换个位置插入主历史。SkillTool 建立同步子 agent，使用技能定义和任务参数组织执行，等待其完成后汇总结果，再作为技能调用的结果交回主循环。子 agent 的技能状态有自己的作用域，`finally` 清理它，避免执行失败或提前退出后遗留状态。[inline 与 fork 执行][skill-run]

| 路径 | 直接消费技能正文的对象 | 主循环得到什么 | 收尾责任 |
|---|---|---|---|
| inline | 当前会话后续请求 | 展开消息及适用上下文修改 | 执行器消费消息和状态修改 |
| fork | 技能子 agent | 子任务汇总后的调用结果 | 清理该 agent 的技能状态 |

这并不保证 fork 有独立操作系统进程或独立工作树。它首先隔离任务上下文，文件、权限和取消还需看子任务构造。下一章会把这些边界单独讲完整。

<a id="5-hook-的名字必须和消费点一起读"></a>
## 5. Hook 的名字必须和消费点一起读

Hook 在不同阶段输出的内容，不具有同一种含义。关键是哪个消费者接受它、会改变什么：

| 时点 | 可产生的作用 | 由谁消费 |
|---|---|---|
| UserPromptSubmit | 附加背景、阻止输入继续 | 输入处理器决定是否 query |
| PreToolUse | 改参数、要求批准、拒绝或提出允许 | 工具执行层继续权限判断 |
| PostToolUse | 附加反馈；MCP 路径可改输出 | 结果映射与后续请求 |
| Stop / 子任务停止相关检查 | 阻塞结束并要求继续 | 查询循环决定下一次迭代 |
| PreCompact | 补充摘要要求 | 压缩请求生产者 |
| SessionStart(compact) | 压缩后的启动材料 | 替代历史构建器 |

Stop Hook 的阻塞反馈不是普通展示消息，它会进入后续输入，促成再迭代；循环同时维护防重复状态。API 错误不会无条件进入常规 Stop 评估，否则“错误→要求继续→更大请求→再次错误”可能持续扩大问题。[停止消费边界][stop-hook]、[循环中的停止分支][query-stop]

同样，PreToolUse 改了参数后不能只检查旧参数的校验记录；PostToolUse 的成功提示不能代替业务校验。Hook 能改变运行过程，但依然受对应阶段的权限及结果合同约束。
<a id="6-mcp-清单如何变成真正可调用的-tool"></a>
<a id="6-接入-mcp-后还要管理连接和结果"></a>
## 6. MCP 清单如何变成真正可调用的 Tool

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


### 远端能力适配后，共用本地执行链

连接声明支持 tools 能力时，客户端取得清单，把描述、输入结构和元数据转换为统一 Tool。服务器身份与远端工具名仍然保留，用于路由和权限判断；本地展示名称不能取代这两个身份。`readOnlyHint` 会影响并发声明，所以远端元数据实际进入了本地调度的信任边界，不能认为它只是文档装饰。[MCP 到 Tool 的适配][mcp-adapt]

工具被模型选中以后，仍经过上一章的当前池查找、结构检查、Hook、权限与调度。真正的协议调用取得当前连接，携带取消信号、超时和进度回调；会话失效时清理连接缓存并有限恢复，所审路径最多补一次会话恢复尝试。业务 `isError`、认证问题和会话过期有不同去向，不能统一当断网处理。[调用与会话恢复][mcp-call]

例如写入成功但响应丢失，重建连接只能恢复通信条件。它不知道服务端是否已写入；没有业务查询或幂等合同，就没有恰好一次保证。用户取消也不能单凭本地取消信号推定远端副作用被撤销。

<a id="7-协议返回到模型结果中间还要保留类型与大小边界"></a>
## 7. 协议返回到模型结果，中间还要保留类型与大小边界

返回转换优先识别旧 `toolResult`，然后是 `structuredContent`，再处理 `content` 数组。顺序决定同一个响应提供多种表示时采用哪条路径。文本、结构化对象、图片或资源块不能统一当成一条无限长字符串。[内容转换][mcp-content]

大结果按类型选择保留、落盘或截断；图片不能简单作为大 JSON 落盘来替代可用图像输入。保存失败时需要返回明确说明，而不是给模型一个不存在的文件路径。随后进入统一工具执行层，适用的 PostToolUse 可改变 MCP 输出，最后才形成与调用 ID 配对的 `tool_result`。

把这条链缩成一个例子：服务端返回结构化缺陷记录，适配器选择结构化内容；输出过大时保留可用预览和持久结果入口；执行层应用适用 Hook，再映射成模型结果；下一次请求才让模型据此修改代码。远端协议“返回了”只是中间状态，模型是否取得足够信息及任务是否正确仍需分别确认。

## 本章小结

Skill 经发现、准入后走 inline 或 fork，正文、消息与程序状态各有消费者。Hook 的效果取决于触发阶段。MCP 将外部清单适配为 Tool，共用校验、权限和调度，再把协议结果转换成模型可消费的结果。

## 🎯 面试怎么回答

**问：Skill、Hook、MCP 怎样协作？**

Skill 组织任务方法，配置可决定当前会话展开或子任务执行；Hook 在输入、工具、停止和压缩等阶段改变流程；MCP 把远端能力适配进统一工具系统。三者都要追到实际消费者：文字是否进请求，状态修改是否应用，协议返回是否映射，停止反馈是否触发续轮，不能仅以加载成功判断生效。

## ⚠️ 高频易错点

- 技能被扫描到，不等于路径条件已激活或本轮可调用
- `allowed-tools` 的规则增量不是全局白名单，也不会注册新实现
- fork 首先改变上下文作用域，不自动完成文件或进程隔离
- 只读提示会影响调度，却不能证明外部服务绝无副作用
- 重连成功与前一次写入是否发生，是两项不同事实

## 本章自测

**问题：** Skill 的正文已显示，“允许 Read”的修改函数也已返回，但工具被声明为并发安全。下一次调用能依赖新增规则吗？

<details><summary>参考答案</summary>
不能只凭返回确认。该快照执行器仅对非并发工具应用这类上下文修改。正文交付和程序规则生效有不同消费者，需要沿执行器分支检查。
</details>

**问题：** MCP 返回 `structuredContent` 和内容数组，且 PostToolUse 想修改输出。哪一层负责什么？

<details><summary>参考答案</summary>
MCP 适配器按返回优先级选择和规范化内容，再处理类型及大小；统一执行层在适用的 MCP 路径消费 Hook 输出，然后映射为模型的工具结果。不能直接拿最初协议包代表模型最终看到的内容。
</details>

[← 上一章](02-tool-execution-and-permissions.md) · [本产品目录](README.md) · [下一章 →](04-subagents-and-task-ownership.md)

[elicitation]: ../../../references/agent/claude-code-source-index.md#elicitation
[mcp-adapt]: ../../../references/agent/claude-code-source-index.md#mcp-adapt
[mcp-call]: ../../../references/agent/claude-code-source-index.md#mcp-call
[mcp-client]: ../../../references/agent/claude-code-source-index.md#mcp-client
[mcp-content]: ../../../references/agent/claude-code-source-index.md#mcp-content
[query-stop]: ../../../references/agent/claude-code-source-index.md#query-stop
[skill-catalog]: ../../../references/agent/claude-code-source-index.md#skill-catalog
[skill-config]: ../../../references/agent/claude-code-source-index.md#skill-config
[skill-loader]: ../../../references/agent/claude-code-source-index.md#skill-loader
[skill-modifier]: ../../../references/agent/claude-code-source-index.md#skill-modifier
[skill-run]: ../../../references/agent/claude-code-source-index.md#skill-run
[skill-tool]: ../../../references/agent/claude-code-source-index.md#skill-tool
[stop-hook]: ../../../references/agent/claude-code-source-index.md#stop-hook
