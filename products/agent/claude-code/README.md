# Claude Code｜从私有源码镜像还原一个成熟 Coding Agent

[← Agent 产品源码学习](../README.md) · [↑ Products](../../README.md) · [Agent Curriculum](../../../curriculum/09-agent/README.md) · [Agent References](../../../references/agent/README.md)

> **源码镜像：** [studyzhige-ui/claude-code-source-private](https://github.com/studyzhige-ui/claude-code-source-private)  
> **固定源码快照：** [`58231dcce408f805c645cfbc352d2876b517223b`](https://github.com/studyzhige-ui/claude-code-source-private/tree/58231dcce408f805c645cfbc352d2876b517223b)  
> **快照性质：** 私有源码镜像的固定导入提交；仓库没有可用于核验官方 release 的 README / package 元数据，因此本文不虚构 Claude Code 官方版本号。  
> **核验日期：** 2026-09-21

## 0. 核心设计

固定镜像中的 Claude Code 可以先概括为：

> **以 `query() / queryLoop()` 为中心的持续执行 Runtime。每次模型调用前，系统都会重新计算这一轮需要保留的上下文、可见工具和可用能力，同时尽量维持 Prompt Cache 与会话恢复所需的稳定结构。**

“Query-loop 驱动的 Context / Cache / Capability 编排”是根据源码调用关系得到的工程抽象，不是官方架构名。它最有价值的地方，是把长期 Coding Session 中会互相影响的几件事放到同一个循环里处理：上下文预算、缓存前缀、Memory / Skill 预取、动态工具集合、工具执行和 Transcript 恢复。

```text
Interactive REPL          Headless / SDK
      │                         │
      └──────────┬──────────────┘
                 ↓
              query()
                 ↓
             queryLoop()
                 ↓
Tool Result Budget → Snip → Microcompact
→ Context Collapse → Auto Compact
→ Memory / Skill Prefetch
→ API-bound Messages + Visible Tools
                 ↓
              Model
                 ↓
         Tool Call / Answer
                 ↓
Validation → Hooks → Decision → Execution
                 ↓
Tool Result / Attachments / Memory / Skill State
                 ↓
          下一次 queryLoop
                 ↓
Transcript parentUuid chain + File / Worktree / replacement state
                 ↓
              Resume
```

最重要的几个不变量是：**本地 Transcript 不等于每次 API 真正看到的 Context；Context slimming 要尽量保护可复用前缀；Deferred Tool / Skill 先暴露少量 metadata，再按需展开；工具使用策略和实际执行环境是不同边界；Compaction / Snip 必须同时维护可恢复的 Transcript 链。**

因此 Claude Code 的架构中心不是一个复杂 Graph，而是：**在长会话、高工具量和持续代码操作中，不断计算一个成本可控、缓存友好、能力足够且可以恢复的 Model View。**

---

本组文档遵循同一项源码学习原则：**先读产品源码，再抽象 Agent 知识。**

Claude Code 的源码形态和 Codex 差异很大。如果先拿 Codex 的 Thread / Session / StepContext、Extension Registry、replacement-history checkpoint 等概念去套，很容易得到一份“看起来很统一、实际上不真实”的文档。

固定镜像呈现为一个大型 TypeScript 产品运行时：交互式 REPL（终端交互界面）在 `screens/REPL.tsx` 中组织本轮状态，Headless（无界面） / SDK（开发工具包）路径可以通过 `QueryEngine` 管理会话，而两条入口最终都汇入 `query.ts` 的 `query()` / `queryLoop()`。工具、MCP、Skills、Memory、权限、Subagent（子智能体）、Compaction（上下文压缩）、Transcript（会话记录）都围绕这一主循环协作。

所以本组文档首先回答：

> **用户在 Claude Code 输入一句任务以后，产品到底经过哪些真实对象和调用路径，才变成模型请求、工具执行、长期记忆、压缩与恢复？**

---

## 1. 先把 Claude Code 的真实产品入口看清楚

这个镜像并不是只有一个“Agent 类”。

最外层可以先看成三条入口。

### 交互式 CLI / REPL

`main.tsx` 负责完整 CLI 启动，交互式会话的核心 UI 与会话状态主要在：

- `screens/REPL.tsx`
- `components/`
- `hooks/`

REPL 在每次用户提交时会准备：

- 当前 Tool Pool（工具池）；
- MCP Client；
- `ToolUseContext`（工具使用上下文）；
-默认 System Prompt（系统提示）；
-`UserContext`（用户上下文）；
-`SystemContext`（系统上下文）。

随后直接调用：

```text
query({
  messages,
  systemPrompt,
  userContext,
  systemContext,
  canUseTool,
  toolUseContext,
  querySource
})
```

也就是说，交互式产品并不依赖 `QueryEngine` 才能工作。

### Headless / SDK 会话

`QueryEngine.ts` 为无 UI / SDK 场景封装了会话生命周期。

源码注释直接说明：一个 `QueryEngine` 对应一个 conversation（持续会话）；多次 `submitMessage()` 共用消息历史、File State Cache（文件状态缓存）和 Token 使用状态。

它最终同样调用 `query()`。

### 共享的 Agent 主循环

真正把两条入口汇合起来的是：

- `query.ts`

这里负责：

```text
当前消息
→ 上下文瘦身 / 压缩
→ 模型请求
→ 流式响应
→ Tool Call
→ 权限与执行
→ Tool Result
→ 附件 / Memory / Skill
→ 下一次模型请求
→ 直到结束
```

因此后面四篇文档都会把 `query.ts` 当成主干，而不是把某个 UI 组件或 `QueryEngine` 误写成“Claude Code Runtime 的唯一核心”。

---

## 2. Claude Code 自己的执行层级怎样理解

这里不要照搬 Codex 的 Thread / Session / Turn / StepContext。

对当前源码，更实用的理解是：

```text
Session / Conversation
一次持续的 Claude Code 会话
│
├─ 用户提交一次输入
│
│  └─ query()
│      │
│      ├─ queryLoop iteration #1
│      │   模型采样 → Tool Call → Tool Result
│      │
│      ├─ queryLoop iteration #2
│      │   再采样 → Tool Call → Tool Result
│      │
│      └─ 最终停止
│
└─ 下一次用户输入
```

源码内部也有 `turnCount`，但它是在 Tool Result 后继续递归采样时增加的内部计数，不能简单把它等同于“用户发了一条消息”。

这也是为什么本文会尽量说：

- “用户轮次”；
- “query loop iteration（查询循环迭代）”；
- “模型请求”；

而不会为了和别的产品对齐，把它们全部叫同一种 Turn。

---

## 3. 一次真实请求先讲成一个故事

假设用户输入：

> “修复这个测试失败，不要修改公开 API。”

REPL 会把新消息加入当前会话，然后准备当前 Tool Pool、Permission Context（权限上下文）、MCP、Agent Definition（智能体定义）和 System / User Context。

进入 `queryLoop` 后，Runtime 不会立刻发 API 请求。它会先处理当前 Context 的体积：

```text
Tool Result Budget
→ History Snip（历史片段裁剪，若启用）
→ Microcompact（微压缩）
→ Context Collapse（上下文折叠，若启用）
→ Auto Compact（自动全量压缩，若需要）
```

只有这些完成后，才把 System Prompt、User Context、Messages 和本轮可见 Tool Schema（工具模式定义）发送给模型。

模型如果返回 Tool Call，Claude Code 会：

1. 找到对应 Tool；
2. 校验 Zod input schema（输入模式）；
3. 执行 Tool 自己的 `validateInput`；
4. 运行 PreToolUse Hook（工具执行前钩子）；
5. 进入 permission decision（权限决策）；
6. 必要时弹批准 UI、走自动 classifier（分类器）或 headless hook；
7. 真正执行 Tool；
8. 跑 PostToolUse Hook；
9. 把 Tool Result 写回消息历史。

随后 `queryLoop` 带着新的结果继续下一次模型请求。

所以 Claude Code 的核心循环不是：

```text
Prompt → Model → Answer
```

而是：

```text
不断重算“模型此刻应该看到什么”
→ 模型决定
→ Runtime 受控执行
→ 现实结果重新进入 Context
```

---

## 4. 四篇正文分别追哪条真实生命周期

### [01｜Context Lifecycle：上下文怎样编排、缓存、瘦身和恢复](01-context-lifecycle.md)

从 REPL / QueryEngine 汇入 `query()` 开始，连续追：

- System Prompt、User Context、System Context 从哪里来；
- CLAUDE.md 怎样进入 Context；
-动态 nested instructions（嵌套指令）怎样因为文件访问而注入；
- Tool Result Budget、Snip、Microcompact、Context Collapse、Auto Compact 为什么按这个顺序运行；
- Prompt Cache 为什么要求 API-bound messages（即将发给 API 的消息）尽量保持字节稳定；
- Cached Microcompact（缓存微压缩）怎样只做服务端 cache editing 而不改本地 transcript；
- standard compact 怎样用 forked agent（分叉智能体）做摘要；
- compact boundary（压缩边界）怎样影响 transcript 和 Resume；
-为什么 discovered Tool 还要跨 Compaction 保存。

### [02｜Memory Lifecycle：项目指令、Session Memory 与长期 Auto Memory 怎样分层](02-memory-lifecycle.md)

Claude Code 源码里“Memory”不是一个系统，而是至少几层不同机制：

- CLAUDE.md / Rules：项目和用户指令；
- SessionMemory：当前会话内部的演进摘要；
- Auto Memory：跨 Session 的长期 Memory；
- Relevant Memory Recall：按当前问题选出少量长期记忆；
- Agent Memory：某些 Subagent 自己的 Memory scope。

正文会把它们严格拆开，再追：

```text
会话历史
→ stop hook 后提取 durable memory
→ 受限 forked agent 写 memory dir
→ AutoDream 跨 Session 整理
→ MEMORY.md 作为入口
→ 当前用户问题触发非阻塞 relevance prefetch
→ 最多选少量 topic memories
→ 注入主循环
→ 用户 / 主模型直接修改 Memory 时怎样和后台提取避免竞争
```

### [03｜Tool Lifecycle：从工具池到 Tool Search、MCP、Skill、权限和 Sandbox](03-tool-lifecycle.md)

重点追：

- `Tool` contract（工具契约）到底包含什么；
- `getAllBaseTools()` / 动态 Tool Pool 怎样形成；
- Tool Search 为什么根据 Context Window 和 Tool definition tokens 决定是否延迟加载；
- `tool_reference` 怎样让已发现 Tool 跨后续请求继续可用；
- MCP Server 怎样连接、`tools/list`、转换成普通 Claude Code Tool，再进入同一权限体系；
- Skill 为什么只在发现阶段加载 frontmatter，完整 `SKILL.md` 到调用时才展开；
- Skill 怎样 inline 或 `context: fork`；
- Tool input 怎样经过 validation、Hook、Permission、Sandbox、Execution、PostHook 和结果回填；
- Streaming Tool Execution（流式工具执行）为什么会让 API fallback 必须防双执行。

### [04｜Engineering & Evaluation：恢复、多 Agent、故障、规模化和评测](04-engineering-evaluation.md)

把产品级边界补齐：

- Transcript 为什么是 UUID / `parentUuid` 链，而不是 messages 数组 dump；
- Compaction / Snip 为什么必须同时维护恢复链；
- Resume 还要恢复 File History、Worktree、Agent、Context Collapse、Tool Result Replacement 等状态；
- AgentTool 怎样启动同步 / 异步 Subagent、独立工具池和 Worktree isolation；
- Team / SendMessage 的 mailbox（邮箱）和跨 Session 消息边界；
- API 529 / 429、auth、stale connection、model fallback 怎样分层恢复；
- Prompt Cache Break Detection 怎样定位 cache miss 来源；
-大 Context、大 Tool、大 Skill、大 Memory 的规模化策略；
-源码现有 telemetry / contract 能验证什么，以及真正的 Agent Eval 还需要怎样做。

---

## 5. 源码覆盖矩阵：哪些主干已经核到真实调用点

这张表用于证明“全面”来自源码覆盖，而不是标题数量。

| 系统边界 | 主要源码入口 | 已核实的职责 |
|---|---|---|
| CLI / 产品启动 | `main.tsx`、`replLauncher.tsx` | CLI 模式、REPL 启动、Resume / Fork / print 等产品入口 |
| 交互式运行 | `screens/REPL.tsx` | 构建 ToolUseContext、System/User Context，直接调用 `query()` |
| Headless / SDK | `QueryEngine.ts` | 会话级消息、缓存、使用量与 `submitMessage()` 生命周期 |
| Agent 主循环 | `query.ts` | 模型请求、Tool Loop、压缩、附件、Memory / Skill prefetch、重试恢复 |
| System / User Context | `context.ts`、`constants/prompts.ts`、`utils/systemPrompt.ts` | System Prompt、Git 状态、日期、CLAUDE.md 等上下文来源 |
| CLAUDE.md / Rules | `utils/claudemd.ts`、`utils/attachments.ts` | 分层项目指令、conditional rules、动态 nested memory/instruction |
| Context 压缩 | `services/compact/`、`query.ts` | Tool Result Budget、Snip、Microcompact、Auto Compact、Session Memory 接入 |
| Context Collapse | `query.ts`、`utils/sessionStorage.ts`、`utils/sessionRestore.ts` | 能核到调用与持久化接口；镜像未包含 `services/contextCollapse/*` 内部实现 |
| Prompt Cache | `services/api/claude.ts`、`services/api/promptCacheBreakDetection.ts` | cache_control、cache editing、cache read/create token 与 break diagnosis |
| Auto Memory | `memdir/`、`services/extractMemories/`、`services/autoDream/` | MEMORY.md、topic memories、提取、跨 Session 整理 |
| Session Memory | `services/SessionMemory/` | 当前 Session 内演进摘要与 compact support |
| Memory Recall | `memdir/findRelevantMemories.ts`、`utils/attachments.ts` | Sonnet side query 选相关 Memory、非阻塞预取、有界注入 |
| Tool contract | `Tool.ts`、`tools.ts` | Tool schema、并发、权限、defer、MCP metadata、结果预算 |
| Tool execution | `services/tools/toolExecution.ts`、`toolOrchestration.ts`、`StreamingToolExecutor.ts` | validation、Hook、permission、call、并发、streaming execution |
| Tool Search | `utils/toolSearch.ts`、`tools/ToolSearchTool/`、`services/api/claude.ts` | defer_loading、自动阈值、tool_reference、动态 schema 加载 |
| MCP | `services/mcp/client.ts`、`tools/MCPTool/` | 连接、tools/list、Tool 转换、权限、重连、elicitation |
| Skills | `skills/loadSkillsDir.ts`、`tools/SkillTool/` | SKILL.md、frontmatter、inline / fork、权限与模型覆盖 |
| Skill Search | `query.ts`、`SkillTool.ts` 的调用点 | 调用与 prefetch 接口可核；镜像未包含所引用的 `services/skillSearch/*` 内部实现 |
| Permission | `utils/permissions/`、`hooks/useCanUseTool.tsx` | allow / deny / ask、模式、classifier、interactive / headless 决策 |
| Sandbox | `utils/sandbox/sandbox-adapter.ts` | 文件 / 网络隔离、managed policy、escape 防护、平台可用性 |
| Subagent | `tools/AgentTool/`、`runAgent.ts` | Agent 定义、同步 / 异步、独立 Tool Pool、Worktree、sidechain |
| Agent Teams / 消息 | `tools/SendMessageTool/`、`utils/swarm/`、tasks | mailbox、broadcast、resume stopped agent、部分跨 Session 路径 |
| Transcript / Resume | `utils/sessionStorage.ts`、`utils/sessionRestore.ts` | parentUuid 链、Compact / Snip 恢复、Worktree、Agent、内容替换等 |
| API Retry | `services/api/withRetry.ts`、`claude.ts` | 429 / 529、auth refresh、stale connection、fallback、后台降载 |
| Observability | `services/analytics/`、`utils/queryProfiler.ts`、`utils/telemetry/` | Query / Tool / Cache / Memory 等运行证据 |

这张表里也明确标出了**镜像缺失实现**。源码文件被其他代码引用，不等于我们有权凭引用路径脑补里面的算法。

---

## 6. 这份私有镜像的证据边界

这个仓库和公开 Codex 不同：它没有可用的根 README、package manifest 或 release metadata 来证明官方发布版本；同时存在 feature-gated（功能开关控制）的内部 / ant-only 路径，也有少数被调用但没有包含在镜像里的目录。

因此文档统一遵守：

> **“Claude Code 当前私有源码镜像在 commit `58231dc` 中实现 / 调用了……”**

而不是：

> “Claude Code 官方某版本一定如此。”

对于缺失源码，只描述能在调用方直接观察到的 contract（契约）和数据流。例如我们可以确认 `query.ts` 启动 Skill discovery prefetch，但不能声称知道缺失的 `services/skillSearch/*` 使用什么具体检索模型或索引。

同样，feature gate 后的内部能力会标出“功能开关控制 / 内部路径”，不把所有源码分支都说成默认面向所有用户的产品行为。

---

## 7. 阅读这四篇时最值得抓住的 Claude Code 特征

读完以后，不应该只记住“Claude Code 也有 Context、Memory、Tool”。

更值得记住的是它和 Codex 的不同工程选择：

**Context 方面**，Claude Code 在完整 Auto Compact 之前有多层瘦身：Tool Result Budget、Snip、Microcompact、Context Collapse，并且 Cached Microcompact 可以利用服务端 cache editing 删除旧工具结果而不修改本地 transcript。

**Memory 方面**，项目 CLAUDE.md 指令、当前 Session Memory、跨 Session Auto Memory 和相关 Memory prefetch 是不同机制；不能把它们都叫“长期记忆”。

**Tool 方面**，Deferred Tool 不只是本地检索：Claude API 的 `defer_loading` 和 `tool_reference` 会参与动态 Tool schema 加载；已经发现的 Tool 还要跨 Compaction 保存 discovery state。

**Permission 方面**，Tool 自身的 permission check、配置规则、Hook、auto classifier、interactive UI、headless fallback 和 OS Sandbox 是多层控制，不是一个 Yes / No 弹窗。

**Persistence 方面**，Transcript 用 parent-linked message chain（父链消息结构）恢复；Compaction 和 Snip 必须同时维护这条链，否则 Resume 会复活已经被压缩或裁掉的历史。

这些才是源码对 Agent System Design（智能体系统设计）真正有价值的地方。

---

## 8. 推荐学习顺序

先读总览，再按完整数据流阅读：

```text
01 Context
用户这一轮，模型究竟看到了什么，为什么没有爆 Context

02 Memory
哪些信息跨 Session 留下来，哪些只是 CLAUDE.md / 当前会话状态

03 Tool
模型决定行动后，怎样发现能力并安全执行

04 Engineering & Evaluation
这些状态怎样恢复、怎样扩到多 Agent、怎样在故障和大规模下保持可控
```

读完以后，应该能够直接用 Claude Code 自己的源码对象解释：

1. REPL 和 QueryEngine 为什么不是同一入口，却汇合到同一个主循环；
2. `queryLoop` 为什么在 API 请求前先做多层 Context 瘦身；
3. Cached Microcompact 为什么能减少 Context 又尽量保 Prompt Cache；
4. CLAUDE.md 为什么不等于 Auto Memory；
5.长期 Memory 为什么既有后台提取，又有按用户问题的非阻塞 recall；
6. Tool Search 怎样让大规模 MCP Tool 不全部展开；
7. Skill 怎样只先暴露 metadata，调用时才展开完整正文；
8. Permission、Approval UI 与 Sandbox 为什么不能合成一层；
9. Subagent 为什么拥有自己的 Tool Pool、Transcript 和可能的 Worktree；
10. Resume 为什么需要修复 parentUuid 链，而不只是重新加载聊天文字。
