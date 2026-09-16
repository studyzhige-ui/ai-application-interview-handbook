# Claude Code Source Index — Agent

更新日期：2026-09-11

固定快照：

```text
repo   = studyzhige-ui/claude-code-source-private
branch = master
commit = 58231dcce408f805c645cfbc352d2876b517223b
```

> 本索引记录“去哪里继续读源码”和当前已经能由源码直接支持的 Runtime 抽象。它不是 Claude Code 的完整逆向文档，也不把某个产品实现提升成通用标准。

## 1. Query / Conversation Runtime

### `QueryEngine.ts`

源码直接说明 `QueryEngine`：

- owns query lifecycle and session state for a conversation；
- 一个 conversation 一个 QueryEngine；
- 每次 `submitMessage()` 开启新 turn；
- messages、file cache、usage 等状态跨 turn 保留；
- 配置中显式存在 `maxTurns`、`maxBudgetUsd`、`fallbackModel`、`abortController`、MCP clients、agents、tools 与 `canUseTool`；
- 运行路径会读取 memory prompt、session storage、system prompt parts、file history、plugin cache 与 compact/snip 相关能力。

稳定课程抽象：

```text
Conversation Runtime
= Turn Lifecycle
+ Persistent Session State
+ Context Assembly
+ Tool / Agent Capability Set
+ Permission Gate
+ Cancellation
+ Usage / Cost Boundary
```

相关导航：

- `query.ts`
- `utils/queryContext.ts`
- `utils/processUserInput/processUserInput.ts`
- `utils/sessionStorage.ts`
- `memdir/`
- `services/compact/`

## 2. Tool Contract / Runtime Context

### `Tool.ts`

这是当前最重要的 Harness 类型文件之一。源码中可以直接看到：

- `Tool` 有输入 schema / JSON schema；
- `call()` 接收 ToolUseContext、permission callback、parent message 和 progress callback；
- Tool 有 `isConcurrencySafe()`、`isReadOnly()`、`isDestructive()`；
- `interruptBehavior()` 区分新用户消息到来时 `cancel` 或 `block`；
- ToolResult 可以返回新消息和 context modifier；
- ToolUseContext 持有 `AbortController`、MCP connection、agent definitions、session/tool state、file history、permission decision、tool-result budget、nested memory、skill discovery 等；
- Permission context 显式区分 allow / deny / ask rules 与 permission mode；
- Tool 搜索使用 `searchHint` 支持 deferred tool discovery；
- Context 中还存在 dynamic skill discovery 与 tool result content replacement state。

稳定课程抽象：

```text
Tool ≠ function(args) -> value

Production Tool Contract
= Schema
+ Execution
+ Permission
+ Side-effect Semantics
+ Concurrency Semantics
+ Cancellation Semantics
+ Progress / Result
+ Context Impact
```

后续定向阅读：

- `hooks/useCanUseTool.ts`
- `types/permissions.ts`
- `utils/permissions/`
- `utils/toolResultStorage.ts`
- `services/mcp/types.ts`

## 3. Task / Background Execution / Subagent

### `Task.ts`

源码明确区分：

```text
local_bash
local_agent
remote_agent
in_process_teammate
local_workflow
monitor_mcp
dream
```

Task state 包含：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

稳定课程抽象：

> Agent Runtime 中“任务”应是具有身份、状态机、输出位置、取消/终止语义的一级对象，而不是一个普通异步函数。

相关导航：

- `tools/AgentTool/`
- `utils/task/`
- `state/AppState.ts`

## 4. Context / Compaction / Memory

已确认导航：

- `QueryEngine.ts` 条件加载 `services/compact/snipCompact.ts` 与 `snipProjection.ts`；
- `ToolUseContext` 有 `CompactProgressEvent`；
- `QueryEngine` 会加载 `memdir/memdir.ts` 的 memory prompt；
- Tool context 显式维护 `loadedNestedMemoryPaths`，避免 CLAUDE.md 一类 nested memory 在繁忙 session 中被反复注入；
- tool-result budget 有 per-conversation content replacement state。

这说明成熟 Harness 的 Context 问题至少不是“把 history 拼起来”：

```text
Context Source
→ Selection / Dedup
→ Budget
→ Tool Result Offload / Replacement
→ Compaction
→ Projection / Replay
→ Memory Re-injection
```

后续章节必须继续读具体 compact implementation 后再声称算法细节。

## 5. Permission / Filesystem Boundary

已确认导航：

- `Tool.ts` 的 `ToolPermissionContext`；
- `QueryEngine.ts` 引入 `utils/permissions/filesystem.ts`；
- `CanUseToolFn` 是 Tool execution 的显式输入；
- Background / async agent 有“不能显示 UI 时避免 permission prompt”等语义。

稳定抽象：

```text
Capability Selection
≠ Permission Decision
≠ Sandbox Enforcement
```

三者必须在课程中分开。

## 6. MCP / Capability Extension

`Tool.ts` 直接引用 MCP SDK 类型、`MCPServerConnection`、`ServerResource`；QueryEngine 配置中 MCP clients 与普通 tools/agents 并列存在。

相关导航：

- `services/mcp/`
- MCP tool conversion / connection lifecycle
- commands / skills / plugin loader

课程抽象：MCP 是外部能力协议，不等于 Agent Loop，也不等于 Skill。

## 7. Skill / Progressive Capability Loading

`ToolUseContext` 中显式存在：

- `dynamicSkillDirTriggers`
- `discoveredSkillNames`
- Tool `searchHint`

这与真人面经中的“Tool/Skill 太多后如何动态发现和按需加载”形成实现侧呼应。

课程应讲：

```text
Capability Catalog
→ Discovery
→ Selection
→ Progressive Loading
→ Invocation
```

而不是把全部 Tool Schema 永久塞进 Context。

## 8. Cancellation / Interruptibility

源码中的两层信号：

- Conversation / turn 层：`AbortController`；
- Tool 层：`interruptBehavior(): cancel | block`。

因此 Cancellation 是贯穿 Runtime 和具体 Tool 的协议，不是简单 `task.cancel()`。

## 9. Source-study TODO

正式写对应深挖章节前继续读取：

1. `query.ts`：主 Agent Loop 与 model/tool 往返；
2. `services/compact/*`：触发、替换、projection；
3. `tools/AgentTool/*`：subagent lifecycle / context inheritance；
4. `utils/permissions/*`：approval / filesystem decision；
5. `services/mcp/*`：连接、tool/resource 转换；
6. `memdir/*`：memory 生命周期；
7. `utils/sessionStorage.ts`：transcript / persistence；
8. `utils/toolResultStorage.ts`：large tool-result context budget。

每次新增具体实现结论都应记录当前 pinned commit。
