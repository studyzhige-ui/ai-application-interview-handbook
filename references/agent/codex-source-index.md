# OpenAI Codex Source Index — Agent Harness / Runtime

> 阅读提示：本文件保留早期固定快照研究记录，不能把所有旧抽象当产品协议。最新的直接核验路径、教学/产品语义区分和版本范围见[2026-09-17读者修订核验](README.md#reader-revision-20260917)。
更新日期：2026-09-11

固定快照：

```text
repo   = openai/codex
branch = main
commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
tree   = 346154dca409158a441d2afe05604f6fa6bed5d6
```

> Codex main 会快速变化。这里所有实现侧结论都以该 commit 为基线；后续跟随新版本时必须重新 pin。

## 1. Session / Turn / Context State

`codex-rs/core/src/compact.rs` 直接依赖并串起：

- `Session`
- `StepContext`
- `TurnContext`
- `WorldState`
- protocol `EventMsg`
- persisted history / compacted item
- inference trace context

下面只作为早期内部对象关系的阅读线索；不由类名推导通用用户层级，Codex交互应明确Thread / Turn / Item：

```text
Session
└─ Turn
   └─ Step / Model Request / Tool Interaction
```

Agent 教材需要把这些执行层次讲清楚，不能把所有 state 都叫“memory”。

## 2. Context Compaction 是受管理的上下文状态转换

### `codex-rs/core/src/compact.rs`

源码明确存在：

- manual 与 auto compaction；
- pre-turn / mid-turn / standalone phase；
- pre/post compact hooks；
- retry / context-window-exceeded 处理；
- replacement history；
- compact metadata / window id；
- token usage recomputation；
- compaction analytics；
- compact 后对长线程准确率风险的 warning。

更关键的是，源码专门区分 initial context 是否在 replacement history 中重新注入，并强调 live / persisted history 一致。

稳定课程抽象：

```text
Compaction
≠ “调用 LLM 写一段摘要”

Compaction
= Trigger
+ Input Selection
+ Summary Generation
+ Replacement History Construction
+ Invariant Preservation
+ Persistence
+ Token Recompute
+ Hooks / Trace
+ Failure Recovery
```

这与 HUMAN-A 的 Context Compaction / Correctness 高频信号高度一致，但源码证据不增加面经频率。

## 3. Tool Runtime

已确认源码路径：

- `codex-rs/tools/README.md`
- `codex-rs/tools/src/tool_call.rs`
- `codex-rs/core/src/tools/router.rs`
- `codex-rs/tools/src/lib.rs`

`tools/README.md` 明确把以下内容抽为共享工具层：

```text
schema sanitization
MCP / dynamic conversion
code-mode augmentation
ToolExecutor
ToolCall
ToolOutput
```

稳定课程抽象：

```text
Model Tool Call
→ Parse / Normalize
→ Route
→ Execute
→ Emit Runtime Event
→ Return Tool Output
```

工具调用是协议边界与 Runtime boundary，而不是简单函数调用。

## 4. Sandbox / Filesystem / Network

已确认：

- `codex-rs/core/README.md`
- `codex-rs/app-server-protocol/schema/typescript/v2/SandboxPolicy.ts`
- `codex-rs/file-system/src/lib.rs`
- `codex-rs/sandboxing/src/manager.rs`
- `codex-rs/linux-sandbox/README.md`

当前协议层的 `SandboxPolicy` 至少表达：

```text
dangerFullAccess
readOnly
externalSandbox
workspaceWrite + writable roots + network access
```

稳定课程抽象：

> Permission/Approval 是“允不允许这次动作”；Sandbox 是“即使代码想越界，执行环境物理上允许到哪里”。二者必须独立设计。

## 5. MCP / Dynamic Capability

已确认：

- `codex-rs/app-server-protocol/src/protocol/v2/mcp.rs`
- `codex-rs/hooks/src/engine/mod.rs`
- `codex-rs/config/src/hook_config.rs`

协议中有 MCP server tool catalog，Hook handler 也可以是 `mcpTool`。这说明 MCP 不只是启动时静态注册，还可以进入扩展 / hook execution boundary。

课程应分别讲：

```text
Tool Contract
MCP Protocol
Hook / Extension Runtime
```

不要把三者合并为“插件”。

## 6. Hooks / Extensibility

已确认 Codex Hook 配置与运行时支持不同 handler kind，包括 command、MCP tool、prompt、agent；并且 compaction 本身也有 pre/post hook。

稳定课程抽象：

```text
Core Runtime
→ Lifecycle Event
→ Hook Policy
→ Extension Handler
```

Hook 是横切扩展点，不能反过来成为 Runtime 主循环本身。

## 7. Trace / Replay / Evidence

### `codex-rs/rollout-trace/README.md`

源码导航明确区分：

- exact raw payload evidence；
- ConversationItem：model 实际看到什么；
- ToolCall：runtime tool boundary；
- CodeCell / TerminalOperation；
- InteractionEdge：information flow。

稳定课程抽象：

> Production Agent Trace 不应该只有日志字符串，而应能重建“模型看到了什么、调用了什么、环境发生了什么、信息如何流动”。

这直接服务 Debug、Replay、Eval 和 Incident Analysis。

## 8. Thread Instructions / Resume / Fork

固定 commit 本身的提交说明新增了 `ThreadInstructionsProvider`，并明确讨论：

- startup 与 model-request boundary 刷新 instruction snapshot；
- 独立 token budget；
- warm resume 保留 provider；
- cold resume / offline fork 重新提供；
- live fork / subagent 继承 applied snapshot，但不继承 source provider；
- cancellation-safe refresh。

这一提交本身非常适合说明：

```text
Instruction Source
≠ Applied Context Snapshot
```

以及 Resume / Fork 时“继承什么、重新加载什么”必须成为明确协议。

## 9. Context / Runtime Analytics

`compact.rs` 中存在独立的 Compaction Analytics：trigger、reason、phase、status、context tokens、summary tokens、latency 等。

课程抽象：

> Context management 本身也应该可观测，而不是只有最终 Token Usage。

## 10. Source-study TODO

正式写深挖章节前继续读取：

1. `codex-rs/core/src/session/*`：Session / Turn lifecycle；
2. `codex-rs/core/src/tools/router.rs`：dispatch / failure semantics；
3. `codex-rs/tools/*`：tool contract；
4. permission / approval protocol；
5. `codex-rs/sandboxing/*`：policy → enforcement；
6. MCP manager / tool discovery；
7. fork / subagent / thread resume；
8. rollout trace reducer / replay；
9. memories extension；
10. hooks lifecycle。

后续任何“Codex 就是这样实现”的具体论断必须指向该 commit 下的文件或 symbol。
