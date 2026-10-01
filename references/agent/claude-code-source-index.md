# Claude Code 源码索引｜机制证据与版本边界

[← 产品阅读入口](../../products/agent/claude-code/README.md) · [Agent 资料](README.md)

固定对象：studyzhige-ui/claude-code-source-private，master 学习快照 58231dcce408f805c645cfbc352d2876b517223b；版本核验日期 2026-10-01。这是授权可读的私有学习快照，不是官方完整公开仓库，也没有确定的官方发行号映射。链接需要相应仓库读取权限。

## 怎样使用证据

正文已经解释对象、条件、消费者与失败去向；这里提供固定提交的核对入口。按范围阅读过一个函数，不等于全面审核该文件、整个仓库或底层服务。工具接口还含输入结构、并发、只读/破坏性、取消/阻塞、进度、结果和上下文修改等合同，不能缩成普通的 `function(args) → value`。

- 输入和循环：对应第一章的输入分流、流中派发、续轮与终止
- 执行和扩展：对应第二、三章的工具池、改写、批准、调度与协议适配
- 子任务：对应第四章的指定创建、同步转后台、消息恢复和清理路径
- 连续性：对应第五至七章的预算、压缩、摘要、自动记忆及恢复
- 观察：对应第八章的工具事件和 SDK 结果生产，不代表内置通用业务验收器

## 已知核验边界

- 未构建该私有快照，未运行真实产品、远端 MCP 或生产故障实验
- reactiveCompact 内部文件未取得；只说明 query 可见的调用顺序与保护条件
- History Snip、Context Collapse、动态技能激活、团队/跨进程路由只按已核验入口说明，不补造未展开的内部算法
- 沙箱只核验适配层及 Bash 接入；未把它当作底层 OS 强制隔离的全面审计
- 子任务的特定同步转后台收尾顺序，不外推为所有后台任务的统一合同
- MCP 只按所列工具适配、调用和结果范围解释，不宣称全面审核传输或认证实现
- 官方文档链接属于公开使用背景，其更新不能修改固定快照的源码结论

## 固定源码锚点

### agent-background

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/AgentTool.tsx#L948-L1049)

### agent-cleanup

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/runAgent.ts#L695-L850)

### agent-context

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/runAgent.ts#L368-L556)

### agent-create

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/AgentTool.tsx#L650-L815)

### agent-resume

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SendMessageTool/SendMessageTool.ts#L799-L878)

### agent-tool

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/AgentTool.tsx)

### api-normalize

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts#L1230-L1399)

### api-request

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts#L1698-L1728)

### api-tools

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts#L1207-L1257)

### attachments

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/attachments.ts#L269-L292)；[核对实现 2](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/attachments.ts#L2196-L2429)

### auto-compact

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/autoCompact.ts)

### auto-dream

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/autoDream/autoDream.ts#L55-L270)

### bash-sandbox

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/BashTool/BashTool.tsx#L860-L920)

### budget-algorithm

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolResultStorage.ts#L575-L907)

### budget-replay

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolResultStorage.ts#L938-L1018)

### budget-state

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolResultStorage.ts#L373-L469)

### cache-diagnosis

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/promptCacheBreakDetection.ts)

### compact-build

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts)

### compact-contract

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L299-L634)

### compact-fallback

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L1136-L1400)

### compact-files

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L122-L130)；[核对实现 2](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L1415-L1468)；[核对实现 3](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L1610-L1706)

### compact-format

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/prompt.ts#L311-L375)

### compact-gates

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/autoCompact.ts#L156-L352)

### compact-prompt

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/prompt.ts#L12-L140)

### compact-reinject

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L1470-L1605)

### compact-retry

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts#L227-L291)

### compact-threshold

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/autoCompact.ts#L29-L91)

### context-source

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/context.ts#L153-L190)

### context-wrap

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/api.ts#L437-L475)

### elicitation

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/elicitationHandler.ts)

### engine-boundary

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/QueryEngine.ts#L687-L735)

### engine-input

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/QueryEngine.ts#L397-L640)

### engine-result

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/QueryEngine.ts#L1060-L1155)

### entrypoint

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/memdir/memdir.ts#L38-L104)

### executor

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/StreamingToolExecutor.ts)

### executor-results

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/StreamingToolExecutor.ts#L263-L445)

### extract-write-check

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/extractMemories/extractMemories.ts#L117-L165)

### extractor

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/extractMemories/extractMemories.ts)

### hook-permission

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolHooks.ts#L319-L439)

### input-accept

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/processUserInput/processUserInput.ts#L85-L267)

### input-call

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L1127-L1227)

### input-hooks

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L755-L937)

### input-normalize

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/processUserInput/processUserInput.ts#L281-L591)

### input-validation

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L606-L730)

### mcp-adapt

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts#L1740-L2000)

### mcp-call

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts#L1740-L2000)；[核对实现 2](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts#L3029-L3245)

### mcp-client

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts)

### mcp-content

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/mcp/client.ts#L2662-L2812)

### memory-build

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/memdir/memdir.ts#L268-L350)

### memory-rules

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/memdir/memdir.ts#L185-L265)

### memory-select

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/memdir/findRelevantMemories.ts#L18-L147)

### micro-branches

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts#L250-L294)

### micro-cache

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts#L294-L398)

### micro-time

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts#L421-L540)

### official-memory

[查看对应来源](https://code.claude.com/docs/en/memory)

### official-sandbox

[查看对应来源](https://code.claude.com/docs/en/sandboxing)

### official-search

[查看对应来源](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

### permission-order

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/permissions/permissions.ts#L1158-L1318)

### permission-race

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/hooks/toolPermission/handlers/interactiveHandler.ts#L120-L239)

### permission-ui

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/hooks/useCanUseTool.tsx)

### permissions

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/permissions/permissions.ts)

### prefetch-start

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L289-L307)

### query-call

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L650-L870)

### query-compact

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L412-L535)

### query-continue

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L1360-L1730)

### query-deps

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query/deps.ts)

### query-history

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L350-L410)

### query-loop

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L219-L330)

### query-stop

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L1010-L1305)

### query-stream

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L650-L899)

### restore

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionRestore.ts)

### restore-chain

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts#L1824-L1957)

### restore-environment

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionRestore.ts#L332-L552)

### result-budget

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolResultStorage.ts)

### retry

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/withRetry.ts)

### run-agent

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/runAgent.ts)

### sandbox

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sandbox/sandbox-adapter.ts)

### sandbox-lifecycle

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sandbox/sandbox-adapter.ts#L695-L817)

### send-message

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SendMessageTool/SendMessageTool.ts)

### session-boundary

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/sessionMemoryCompact.ts#L506-L631)

### session-consume

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/sessionMemoryCompact.ts#L238-L393)

### session-memory

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/SessionMemory/sessionMemory.ts)

### session-produce

[核对实现 1](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/SessionMemory/sessionMemory.ts#L140-L192)；[核对实现 2](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/SessionMemory/sessionMemory.ts#L285-L496)

### session-storage

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts)

### skill-catalog

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/skills/loadSkillsDir.ts#L638-L800)

### skill-config

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/skills/loadSkillsDir.ts#L175-L269)

### skill-loader

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/skills/loadSkillsDir.ts)

### skill-modifier

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SkillTool/SkillTool.ts#L766-L867)

### skill-run

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SkillTool/SkillTool.ts#L432-L840)

### skill-tool

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SkillTool/SkillTool.ts)

### stop-hook

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query/stopHooks.ts#L65-L170)

### storage

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts)

### stream-fallback

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L705-L743)

### tool-execution

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts)

### tool-map

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts#L1227-L1590)

### tool-pool

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools.ts#L212-L390)

### tool-search

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/ToolSearchTool/ToolSearchTool.ts)

### tool-search-state

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolSearch.ts)

### tool-type

[查看对应来源](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/Tool.ts)

### engine-events

[SDK 事件记录](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/QueryEngine.ts#L765-L835)；[存储的链节点及临时进度分类](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts#L145-L195)
