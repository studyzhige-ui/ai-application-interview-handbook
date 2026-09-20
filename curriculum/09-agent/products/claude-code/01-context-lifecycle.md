# 01. Claude Code Context Lifecycle｜模型每一轮到底看见什么

[← Claude Code 总览](README.md) · [Memory →](02-memory-lifecycle.md)

> **源码镜像基线：** `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`

Claude Code 的 Context（上下文）不能理解成“System Prompt + 全部聊天记录”。

真正进入模型请求之前，Runtime（运行时）会把很多来源合起来：System Prompt（系统提示）、CLAUDE.md、当前 Git / Environment 状态、用户输入、历史 Tool Result（工具结果）、动态加载的项目规则、Memory、Skill、MCP Tool，以及当前已经通过 Tool Search 发现的工具。与此同时，它还会不断把过大的历史结果裁小、删除、折叠或总结。

因此源码真正回答的问题是：

> **怎样让模型在每一次采样时看到“足够继续任务、又没有无限增长”的当前工作视图，同时尽量保持 Prompt Cache（提示缓存）稳定？**

---

## 1. 两条产品入口最后都汇入同一个 `query()`

交互式 CLI 和 Headless（无界面） / SDK（开发工具包）的入口并不一样。

交互式 REPL 在 `screens/REPL.tsx` 中维护 UI 与会话状态。用户提交以后，它会拿到最新的 Tool、MCP Client、Permission Context（权限上下文），并发读取默认 System Prompt、User Context（用户上下文）和 System Context（系统上下文），最后调用：

~~~text
query({
  messages,
  systemPrompt,
  userContext,
  systemContext,
  canUseTool,
  toolUseContext,
  querySource,
})
~~~

`QueryEngine.ts` 则是无 UI / SDK 会话包装器。它长期保存 conversation messages（会话消息）、File State Cache（文件状态缓存）和 usage（用量），每次 `submitMessage()` 也会进入同一个 `query()`。

所以 Context 生命周期真正共享的核心不是 REPL 或 QueryEngine，而是：

- `query.ts`
- `services/api/claude.ts`

前者决定“这一轮送什么”，后者决定“怎样把这些内容编码成 Claude API 请求”。

---

## 2. System Prompt、User Context、System Context 为什么分三路

REPL 源码会分别调用：

~~~text
getSystemPrompt(...)
getUserContext()
getSystemContext()
~~~

最后再通过 `buildEffectiveSystemPrompt` 和 `appendSystemContext` 等函数组合。

这几份 Context 的职责并不相同。

### System Prompt：长期的 Agent 行为规则

System Prompt 主要描述 Claude Code 的角色、工作方法、可用能力与行为边界。它会受到默认产品 Prompt、custom system prompt、append system prompt 和当前 main-thread agent definition（主线程智能体定义）的共同影响。

因为 System Prompt 位于 Prompt Cache 的高价值稳定前缀，所以源码对它的变化非常敏感。后面会看到 Claude Code 甚至专门记录 System Prompt hash（哈希）来解释 cache break（缓存断裂）。

### User Context：和用户 / 项目相关但不是普通聊天消息的内容

`context.ts::getUserContext()` 会加载 CLAUDE.md 相关内容，并加入当前日期等用户级上下文。

这类信息的特点是：它影响本次模型工作，但不应该被误解成用户刚刚说的一条聊天消息。

### System Context：当前环境状态

`getSystemContext()` 可以包含 Git status（Git 状态）等环境快照。

它表示的是**当前工作区现在是什么状态**。这和“过去发生过什么”的 Transcript History（会话历史）属于不同信息类型。

---

## 3. CLAUDE.md 是 Context 指令系统，不等于长期 Auto Memory

Claude Code 的 `context.ts` 会通过 `getMemoryFiles()`、`filterInjectedMemoryFiles()` 等路径加载 CLAUDE.md。

源码沿用了 “memory file” 这个历史命名，但教学上必须把语义说清楚：

> **CLAUDE.md 主要是项目 / 用户指令系统，而不是“模型从聊天中自动学习出的长期个人记忆”。**

例如项目里写：

~~~markdown
所有 Python 命令统一用 uv。
修改 API 后必须运行 integration tests。
~~~

它更像 repository instructions（仓库指令）。它的可信来源是项目文件，不是过去对话的记忆提取。

这和后面 Memory 篇中的 `memdir/MEMORY.md`、`extractMemories`、`autoDream` 是不同系统。

---

## 4. CLAUDE.md 不是只在会话开始时加载一次

Claude Code 还有一层更动态的 nested memory / instructions（嵌套指令）。

实现主要在：

- `utils/attachments.ts`
- `utils/claudemd.ts`

当模型打开或操作某个文件时，Runtime 可以沿文件所在路径加载与这个目录相关的 CLAUDE.md 和 conditional rules（条件规则）。

源码明确维护加载顺序：

~~~text
Managed / User 条件规则
        ↓
从 CWD 向目标文件逐层目录：
CLAUDE.md + 无条件规则 + 条件规则
        ↓
CWD 以上层级：
只处理相应条件规则
~~~

而且只有目标路径在当前允许工作区内时才会注入。

为什么要动态加载？假设一个大型 monorepo：

~~~text
/
├── CLAUDE.md
├── backend/
│   └── CLAUDE.md
└── ios/
    └── CLAUDE.md
~~~

用户只改 backend 时，没有必要一开始就把 iOS 的全部约束塞给模型。真正访问 backend 文件后，再把相关局部规则引入 Context，信息密度更高。

### 为什么还要单独记录 `loadedNestedMemoryPaths`

Claude Code 的 File State Cache 是有界 LRU（最近最少使用缓存）。如果只靠它判断“某个 CLAUDE.md 是否已经加载”，缓存淘汰以后同一指令可能被重复注入。

源码因此增加一个不会因为 LRU 淘汰而丢失的 path set（路径集合）专门去重。

这个细节很能说明成熟 Context 系统的特点：

> **Context 注入不仅要考虑“读什么”，还要考虑“怎样避免同一事实因为缓存机制反复进入模型”。**

---

## 5. 进入 `queryLoop` 后，先瘦身历史，再发模型请求

`query.ts` 中最值得学习的一段，是每次循环进入 API 调用前的处理顺序。

当前源码近似：

~~~text
已有 messages
        ↓
取 compact boundary 之后仍然有效的历史
        ↓
Tool Result Budget
        ↓
History Snip（若启用）
        ↓
Microcompact
        ↓
Context Collapse（若启用）
        ↓
Auto Compact
        ↓
拼 System / User Context
        ↓
构造 Claude API request
~~~

这里没有一个单一的“压缩算法”。

Claude Code 更像在不同成本层级上逐步处理 Context：

> **能局部删的先局部删；能保留结构的先保留结构；只有仍然过大时才做更重的全量摘要。**

---

## 6. Tool Result Budget：先处理最容易膨胀的东西

Coding Agent 的 Context 中，最容易突然变大的通常不是用户聊天，而是 Tool Result。

例如测试输出几万行、Grep 找到大量匹配、Web / MCP 返回超大 JSON，或者 shell 输出完整构建日志。

`query.ts` 在 Microcompact 前先调用 `applyToolResultBudget`。

原因是：

> 如果一个单独 Tool Result 已经异常巨大，就没必要先让更复杂的 Compaction 机制为它付费。

这层处理还可以把替换记录持久化，保证 Resume 后看到的仍然是经过相同 content replacement（内容替换）的历史，而不是重新把原始超大结果塞回来。

因此 Tool Result Budget 既是 Context 优化，也是持久化语义的一部分。

---

## 7. Snip 和 Microcompact：不是每次都需要“总结整段对话”

### History Snip：直接裁掉不再需要的中间历史

History Snip（历史裁剪）是 feature-gated（功能开关控制）的路径。

它可以删除历史中间的部分，而不是从头到某个点全部摘要。

这对工具密集型长任务很有价值：有些早期 Observation（观察结果）已经完全被后面的状态覆盖，继续保存意义不大。

但删除中间段会给 Resume 带来麻烦：后文 Engineering 篇会看到，Claude Code 的 transcript 是 `parentUuid` 链，Snip 必须把被删除区间两侧重新接起来，否则恢复会沿旧父链把被裁掉内容找回来，甚至把后续消息变成孤链。

### Microcompact：优先清理旧 Tool Result

`services/compact/microCompact.ts` 专门针对可以局部压缩的 Tool output。

源码列出的典型可处理对象包括 Read、shell、Grep / Glob、Web Search / Fetch、Edit / Write 等。

它的目标不是生成一个“整个会话摘要”，而是把已经失去高价值的旧工具细节从 Context 中拿掉。

这符合 Coding Agent 的信息衰减规律：

~~~text
最初：
测试有 47 个失败

后来：
只剩 1 个失败
~~~

到了后期，最初那 47 个失败的完整堆栈通常不再值得继续占用大量 Context。

---

## 8. Cached Microcompact：Claude Code 对 Prompt Cache 的一个关键优化

普通 Microcompact 会修改要发送的 Context。

但源码中还有 Cached Microcompact（缓存微压缩），用于支持 cache editing（缓存编辑）的模型路径。

这里最值得理解的是：

> **它可以请求服务端删除旧的缓存 Tool Result，而本地 messages 不发生同样的内容改写。**

`query.ts` 对这一点有非常明确的注释：cached microcompact 主要通过 `tool_use_id` 操作，并把 pending cache edits（待执行缓存编辑）交给 API 层。

这样做的价值是：

~~~text
本地 transcript 保留完整事件
        ↓
服务端缓存前缀只删除低价值旧 Tool Result
        ↓
尽量不重写剩余前缀
        ↓
减少 cache miss 风险
~~~

这和“先生成一段新摘要，然后把所有历史替换掉”是完全不同的工程路径。

因此 Prompt Cache 不是 Compaction 之后才考虑的性能指标，它直接影响 Claude Code 选择哪种压缩方式。

---

## 9. Context Collapse：能核实接口，但不能脑补缺失内部实现

当前镜像中的 `query.ts` 会在 Auto Compact 前调用 Context Collapse：

~~~text
contextCollapse.applyCollapsesIfNeeded(...)
~~~

Session Storage 还会持久化 Context Collapse commit 和 staged snapshot；Resume 时 `sessionRestore.ts` 会恢复这些记录。

这说明 Context Collapse 确实参与了：

~~~text
运行时 Context 投影
+
持久化
+
Resume
~~~

但本镜像没有包含被引用的 `services/contextCollapse/*` 具体实现文件。

因此我们能确定：

> 它是一个在 Auto Compact 前运行、支持持久化恢复的粒度化 Context 折叠层。

但不能声称知道缺失模块内部具体如何评分、如何生成 summary、如何调度 agent。文档到这里必须停在真实证据边界。

---

## 10. Auto Compact：当局部瘦身不够时，才进入完整摘要迁移

`services/compact/autoCompact.ts` 决定是否需要自动完整压缩。

它不只是一个 token threshold（Token 阈值）。

当前源码还会处理用户 / 配置是否禁用、当前 query source 是否允许、Context Collapse 是否已经负责主动 headroom（预留空间）、连续 Compaction failure（压缩失败），以及 Session Memory 是否可以先承担一部分压缩。

特别值得注意的是 circuit breaker（熔断器）。

源码记录连续失败次数，达到一定次数后不会在每个循环里继续疯狂尝试同样的 Auto Compact。注释明确提到，反复失败曾导致巨大的 API 浪费。

所以成熟 Compaction 控制器不仅要问：

> “现在够不够长？”

还要问：

> “这个恢复动作刚才已经失败几次了，继续尝试还有没有意义？”

---

## 11. Standard Compact：用 forked agent 做语义总结，再建立新的边界

标准 `compact.ts` 会启动一个 forked agent（分叉智能体）来总结历史。

这条路径非常依赖 Prompt Cache。

源码注释提到：Compaction fork 会显式共享 Prompt Cache；过去实验如果禁用共享，会出现非常高的 cache miss，并产生昂贵的新 cache creation（缓存创建）。

因此完整压缩流程不是简单：

~~~text
history → summary
~~~

更接近：

~~~text
当前历史
→ 选择需要总结 / 保留的部分
→ forked compact query
→ 得到 summary
→ buildPostCompactMessages
→ 产生 compact boundary
→ 后续 API 只看 boundary 后的新上下文
~~~

如果连 compact request 自己都 prompt-too-long，源码还会按 API round group（API 轮组）逐步截掉最老部分再重试，而不是直接崩溃。

---

## 12. Compact Boundary 为什么同时影响 UI、API 和 Resume

Compaction 成功后会产生 compact boundary message（压缩边界消息）。

它至少承担三种职责。

**对 API**，`query.ts` 每次都从最近有效 compact boundary 后取消息，因此旧历史不会继续发给模型。

**对 UI**，REPL 普通模式可以把当前消息列表重置到新边界；Fullscreen 模式为了 scrollback（回看）可以保留有限的压缩前历史，但源码仍然给这个 UI 历史设置上限，避免多天 Session 让 React 处理无限数组。

**对 Transcript**，`recordTranscript` 对 boundary 前后的 `parentUuid` 关系做特殊处理，确保 Resume 时新的消息链真正从 compact 后状态继续，而不是又连回旧历史。

所以 compact boundary 不是“UI 显示一条已压缩”。

它是：

> **模型历史、界面历史和持久化历史共同认可的一条语义边界。**

---

## 13. Tool Search discovery 为什么还要跨 Compaction 保存

Claude Code 的 Deferred Tool（延迟工具）使用 `tool_reference` 让模型动态发现工具。

问题是：

~~~text
模型已经通过 ToolSearch 找到 mcp__calendar__create_event
        ↓
后面发生完整 Compaction
        ↓
包含 tool_reference 的旧消息被摘要掉
        ↓
系统会不会忘记这个 Tool 已经发现过？
~~~

`utils/toolSearch.ts::extractDiscoveredToolNames` 对这个问题有专门处理。

Compact boundary 的 metadata 会携带：

`preCompactDiscoveredTools`

恢复模型可见 Tool Set 时，会把 Compaction 前已经发现的 Tool 加回来。

这说明 Context Compaction 不能只保留自然语言“任务摘要”。

它还要保留那些**决定未来模型协议状态的结构化信息**。

---

## 14. Prompt Cache 不只是“命中率”，Claude Code 还会诊断为什么断了

Claude Code 对 Prompt Cache 有专门的两阶段诊断：

- `services/api/promptCacheBreakDetection.ts`

发请求前，`recordPromptState` 会记录影响缓存的可见状态，例如 System Prompt、Tool Schema、model、cache_control、beta headers、fast mode、effort 和其他 request body 状态。

这里不是要我们背字段，而是说明：

> **Claude Code 把“Prompt 为什么变了”做成了可观测状态。**

响应回来以后，`checkResponseForCacheBreak` 会比较本次和上次的 cache read tokens。

如果 cache read 明显下降，它会尝试解释：

- model 是否变了；
- System Prompt 是否变了；
- Tool Schema 是否增删 / 改动；
- cache scope / TTL 是否变化；
- beta 是否变化；
-还是客户端没有任何可见变化，更像服务端路由 / eviction（淘汰）。

Cached Microcompact 造成的预期 cache deletion 会被单独识别，不误报成 cache break。

这是一种非常成熟的 Context Observability（上下文可观测性）：

> 不只是看“缓存差了”，而是把缓存退化和具体 Prompt 状态变化关联起来。

---

## 15. 用一个任务把完整 Context 生命周期串起来

用户输入：

> “修复这个 flaky test，不能修改 API；如果相关目录有 CLAUDE.md，按里面的规则做。”

REPL 构建当前 ToolUseContext、System Prompt、User Context 和 System Context。顶层 CLAUDE.md 进入 User Context。

第一次 `queryLoop` 发现历史还很短，不需要 Auto Compact。模型看到测试工具，决定运行测试。

Tool Result 很大，但仍在预算内，写回 messages。

模型随后读取 `backend/payments/test_x.py`。这个文件路径触发 nested memory attachment，Runtime 发现 `backend/payments/CLAUDE.md`，把局部项目规则动态加入 Context，并记录已经加载过该路径。

任务继续很久，旧测试输出开始占大量 Context。Microcompact 清理了已经失去价值的 Tool Result；如果支持 Cached Microcompact，还可以通过 cache editing 删除缓存中的旧结果而保持本地 transcript 不变。

再继续增长时，Auto Compact 启动 forked agent 生成 summary，产生 compact boundary。Tool Search 已发现的 MCP Tool 集合被放进 boundary metadata，以免压缩后忘记。

进程退出以后 Resume，Transcript loader 根据 compact boundary 与 parent chain 重建“当前真正有效的历史”，而不是把压缩前所有消息重新送进 API。

最终正确性并不只是：

> “压缩成功了。”

而是：

> **经过动态规则加载、很多 Tool Result、局部压缩、完整压缩和 Resume，最初‘不能修改公开 API’以及真正相关的目录规则仍然影响模型后续行为。**

这才是 Context Lifecycle 应该评测的目标。

---

## 16. 源码锚点

建议按调用顺序回读：

1. [`screens/REPL.tsx`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/screens/REPL.tsx)：交互式请求怎样准备 Context 并进入 `query()`。
2. [`QueryEngine.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/QueryEngine.ts)：Headless / SDK 会话状态。
3. [`query.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)：完整 Context 瘦身与 Agent Loop。
4. [`context.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/context.ts)：System / User Context 和 CLAUDE.md 入口。
5. [`utils/attachments.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/attachments.ts)：动态 nested instructions、Memory / Skill attachments。
6. [`services/compact/microCompact.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts)：Microcompact / Cached Microcompact。
7. [`services/compact/autoCompact.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/autoCompact.ts)：Auto Compact 决策和失败熔断。
8. [`services/compact/compact.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts)：完整 summary compaction。
9. [`services/api/claude.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts)：真正 Claude API request、Tool Schema、cache_control、cache_edits。
10. [`services/api/promptCacheBreakDetection.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/promptCacheBreakDetection.ts)：Prompt Cache break 归因。
11. [`utils/sessionStorage.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts)：compact / snip 对持久化链的影响。
12. [`utils/toolSearch.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/toolSearch.ts)：discovered Tool 怎样跨 Compaction 保留。

下一篇：[Claude Code Memory Lifecycle →](02-memory-lifecycle.md)
