# 04. Claude Code Engineering & Evaluation｜恢复、多 Agent、故障、规模化与评测

[← Tool](03-tool-lifecycle.md) · [Claude Code 总览](README.md) · [成熟产品源码学习](../README.md)

> **源码镜像基线：** `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`

前面三篇已经回答了：一次模型请求怎样获得 Context，信息怎样跨 Session 成为 Memory，模型决定动作以后 Tool 怎样真实执行。

这一篇看的是它们长期运行以后发生什么。

Claude Code 还要处理一条 Session 退出以后怎样恢复、Compaction / Snip 以后 transcript 怎样保持一致、Subagent 怎样有自己的 Context / Tool Pool / 文件隔离、Agent Teams 怎样传消息、API 429 / 529 和认证 / 网络连接怎样恢复、Streaming Tool 已经开始执行时 API fallback（降级）怎么避免副作用重复，以及最后怎样证明这些机制真的让任务更可靠。

---

## 1. Claude Code 的持久化核心不是“保存 messages 数组”

最值得读的文件之一是：

- `utils/sessionStorage.ts`

Claude Code 会给 transcript（会话记录）中的消息分配 UUID，并通过 `parentUuid` 建立父链。

因此它更像：

~~~text
message A
   ↓ parent
message B
   ↓ parent
message C
~~~

而不是：

~~~json
["A", "B", "C"]
~~~

为什么要这么复杂？

因为 Claude Code 支持 Compaction、History Snip、Fork Session、Subagent sidechain（子智能体侧链）、消息去重、部分历史恢复和 content replacement（内容替换）。

这些操作经常不是简单“在数组末尾 append”。

父链让 Runtime（运行时）能表达：

> **哪条消息在语义上接在哪条历史之后。**

---

## 2. `recordTranscript` 为什么专门处理 Compaction 后的旧 UUID

完整 Compaction 后，新的历史里可能包含：

~~~text
compact boundary
summary
messagesToKeep
new messages
~~~

其中 `messagesToKeep` 可能沿用了压缩前已经写过磁盘的 UUID。

如果 transcript writer 简单说：

> “这个 UUID 已经存在，那就跳过；同时把它当作当前最后 parent。”

会发生一个很隐蔽的错误：

~~~text
新 summary
        ↓
跳过的旧 message UUID 被当成 parent
        ↓
后续新消息又接回压缩前历史
~~~

结果就是 compact boundary 被绕过。

`recordTranscript` 的源码注释专门说明：已经记录过的消息只有在它们构成“新 slice 的前缀”时，才允许更新 `startingParentUuid`；如果旧 message 出现在新 compact boundary / summary 之后，就不能拿它重新当链尾。

这个细节说明：

> **Compaction 的正确性不仅是模型收到什么，还包括持久化链必须承认新的历史根。**

---

## 3. Snip 删除中间历史时，为什么还要重连 parent chain

History Snip 和完整 Compaction 不同。

Compaction 通常截断一个前缀；Snip 可以删除中间区间。

假设原来：

~~~text
A → B → C → D → E
~~~

Snip 删除：

~~~text
C → D
~~~

如果只把 C、D 从 Map 里删掉，E 的 `parentUuid` 仍然指向 D。

Resume 时沿 parent 链向前走：

~~~text
E → D
~~~

却找不到 D，于是更早的 A、B 可能变成孤立历史；或者如果磁盘旧记录仍然存在，又可能把被裁内容重新恢复。

源码因此会先记录被删除节点自己的 parent，再删除目标消息；随后对 surviving messages（幸存消息）的 dangling parent（悬空父指针）向后追，把 E 重新接到 B。

源码注释还记录了真实后果：如果不做这一步，Resume 会重建出完整未 Snip 的历史，甚至出现显示约 397K、实际恢复 1.65M 级别 Context 的情况。

这是非常典型的 Production lesson：

> **任何“只改内存 Context、不改恢复语义”的压缩，都只是暂时优化。**

---

## 4. Resume 恢复的也远不只是聊天文字

`utils/sessionRestore.ts` 显示了 Resume 真正要恢复的状态。

除了 messages，还包括：

- File History Snapshot（文件历史快照）；
- Attribution（归因）状态；
- Content Replacement（内容替换）；
- Context Collapse commit / snapshot；
- Todo / Task 状态；
- Agent definition；
- Session mode；
- Worktree；
- cost state；
- session metadata。

例如恢复 Worktree 时，Runtime 会重新 `chdir` 到对应目录；如果目录已经不存在，则清除 stale worktree state（陈旧工作树状态）。

而且 CWD 改变以后还要清理 Memory file caches、System Prompt sections cache 和 plans directory cache。

为什么？

因为这些缓存很多都依赖当前目录。

这说明成熟 Resume 的目标是：

> **恢复“下一步继续执行所需要的环境语义”，不是把 UI 聊天记录重新画出来。**

---

## 5. Subagent 本质上仍然复用同一套 `query()` Runtime

Claude Code 的 Subagent 主要围绕：

- `tools/AgentTool/AgentTool.tsx`
- `tools/AgentTool/runAgent.ts`

AgentTool 先选择 Agent Definition，然后构建该 Agent 的 System Prompt、model、permission mode、Tool Pool 和初始 messages。

最终 `runAgent` 仍然进入同一个 `query()` 主循环。

这意味着 Subagent 并不是另一套完全独立的 Agent Runtime。

它复用 Context / Compact、Tool execution、Permission、API 和 Transcript，但拥有不同的执行配置和消息侧链。

这种复用很重要：如果主 Agent 和 Subagent 各自实现一套 Tool / Compact / Permission，很快就会产生两套行为不一致的系统。

---

## 6. Subagent 的 Tool Pool 为什么不直接复制父 Agent

AgentTool 当前源码明确：

> worker tools are assembled independently of the parent's.

Subagent 会根据自己的 Permission Mode 和当前 MCP Tool 重新 `assembleToolPool`。

因此：

~~~text
父 Agent 能用哪些 Tool
≠
子 Agent 必须完全一样
~~~

Agent Definition 可以限制 Tool；Permission rule 也可以单独 deny 某个 `Agent(agentType)`。

为什么要这样？

因为 Subagent 是职责边界。例如 Explore Agent（探索智能体）可能只需要搜索和读文件；一个部署 Agent 才需要更高副作用能力。

如果所有 Child Agent 都无条件继承 Root 的最大权限，Agent decomposition（任务拆分）会扩大攻击面。

---

## 7. Worktree Isolation：Subagent 还可以有独立文件工作空间

AgentTool 支持 `isolation: worktree` 一类执行路径。

创建 Subagent 时，Runtime 可以为它创建独立 Git Worktree（Git 工作树）。

价值很直观：

~~~text
Main Agent 修改 A
Subagent 修改 B
~~~

如果两者在同一个 working tree（工作目录）并发写，很容易覆盖文件、互相看到未完成状态，或者产生 Git index 冲突。

Worktree isolation 把文件系统状态也变成 Agent 边界的一部分。

这说明 Multi-Agent（多智能体）真正需要隔离的不只是 Prompt：

> **Context、Tool Permission、执行进程、文件工作区都可能需要独立。**

---

## 8. 同步 Subagent 为什么可以中途转后台

AgentTool 支持同步和异步 Subagent。

同步 Agent 运行时，父级原本会等待它完成。

但如果执行时间较长，Claude Code 可以把 foreground task（前台任务）转换成 background task（后台任务），让主会话继续接受工作。

源码为这个过程维护 stable agent id、Task Registry（任务注册表）、background signal、progress tracker、output file 和 summarization。

这个设计解决的是：

> **长 Subagent 不应该永久占住主线程用户交互。**

也因此结果交付不能只靠函数 return；后台 Agent 完成后需要另一个 notification / task result 通道把结果送回。

---

## 9. Agent Teams 和普通 Subagent 不是同一层

AgentTool 中还能看到 feature-gated 的 Agent Teams / Swarm 路径。

当 Team 模式启用时，可以 spawn teammate（创建队友），甚至使用 in-process 或 tmux 等不同后台。

源码对 Team 有自己的约束，例如 Team roster（成员表）是扁平的、teammate 不能继续 spawn teammate、某些 in-process teammate 不能再启动 background agent、不同消息类型有明确路由。

这些代码存在于镜像，但很多属于 feature-gated / 内部能力。

因此文档能确认它们的 Runtime 语义，却不能说“所有 Claude Code 用户默认都处于 Team 架构”。

---

## 10. SendMessage 为什么不只是“Agent A 给 Agent B 一句话”

`tools/SendMessageTool/SendMessageTool.ts` 支持：

- 对指定 teammate 发文本；
- broadcast；
- shutdown request / response；
- plan approval response；
- 向正在运行的 in-process agent queue message；
- 目标 Agent 停止时尝试自动 Resume；
- 部分 feature gate 下的 UDS / bridge 跨 Session 消息。

尤其有两个成熟边界值得学习。

### 消息可以只排队，不要求立刻中断目标 Agent

运行中的 Agent 可以在下一次 Tool round（工具轮次）接收 pending message。

这样不会在它正在执行一个关键 Tool 时强行插入新的模型输入。

### 跨机器消息需要更高安全门槛

feature-gated bridge 路径允许向 Remote Control session 发文本，但源码明确把它标成需要显式用户 consent（同意），不能由普通 bypass / classifier 静默放行，而且 structured control message（结构化控制消息）不能跨 Session。

因为跨机器消息实际等价于：

> **向另一条 Claude Session 注入用户 Prompt。**

它的安全风险比同进程 teammate mailbox 高得多。

---

## 11. API Retry 为什么按 query source 区分前台和后台

模型 API 的恢复核心在：

- `services/api/withRetry.ts`

默认 retry 数是有限的，并且对 529 overload（过载）有单独处理。

很有意思的是，Claude Code 不让所有后台请求都和用户主请求一样反复重试。

源码维护一组 foreground query sources（前台查询来源），例如 REPL 主线程、SDK、Agent、Compaction 和一些安全 classifier。

用户真的在等待这些结果，所以可以在预算内 retry。

而一些后台标题、建议、辅助任务在 529 capacity cascade（容量雪崩）时会尽早放弃。

源码注释解释了原因：

> 后台任务反复 retry 会把一次平台容量问题放大成 3–10 倍 gateway amplification（网关放大），而用户甚至看不到这些后台结果。

这是 Production Retry 很重要的原则：

> **是否重试，不只由错误类型决定，还由这个请求对用户任务的重要性决定。**

---

## 12. 认证、连接和模型 fallback 也是不同恢复路径

`withRetry` 还会区分 API 401、OAuth token revoked、Bedrock / Vertex auth error、ECONNRESET / EPIPE stale connection（陈旧连接）、429 / 529、fast mode 不可用和 model fallback。

例如 stale keep-alive connection 可能先关闭复用，再重新创建 Client。

认证错误会刷新 credential，而不是指数退避十次同一个失效 token。

Fast Mode 遇到短 `retry-after` 可以等一下保留同模型和 Prompt Cache；如果延迟很长，则进入 cooldown（冷却），切回标准速度，避免反复 cache thrashing（缓存抖动）。

所以成熟 Retry 必须回答：

~~~text
失败的是认证？
连接？
容量？
模型能力？
还是用户主动取消？
~~~

不同层不能共享一个万能 `retry()`。

---

## 13. Streaming fallback 为什么最怕 Tool 双执行

Context / Tool 篇已经提到 Streaming Tool Executor。

模型还在 streaming（流式输出）时，一些 Tool 可能已经开始执行。

如果随后流失败，API 层决定：

~~~text
streaming request
→ fallback to non-streaming
~~~

新请求可能重新产生相同 Tool Call。

如果 Runtime 没有识别旧流中已经启动的动作，就可能：

~~~text
第一次：删除记录
fallback
第二次：再次删除记录
~~~

这类副作用不是多花 Token，而是 correctness bug（正确性错误）。

因此 Claude Code 源码在 query fallback 路径会 tombstone partial assistant message，并丢弃对应 Streaming Tool Executor 的旧结果；API 层也有针对“开启 streaming tool execution 时避免危险 fallback”的逻辑。

这给 Agent Runtime 一个非常重要的面试答案：

> **模型请求是否可以 Retry，要看它是否已经触发不可重复的外部副作用。**

---

## 14. Prompt Cache Break Detection 为什么是 Production Agent 很少见但很重要的一层

Claude Code 不只记录：

~~~text
cache_read_input_tokens = N
~~~

它会建立上一请求的可见 Prompt 状态快照。

下一次 cache read 大幅下降时，Runtime 能关联 System Prompt 是否变了、Tool Schema 是否变了、model 是否变了、cache_control / beta / effort 是否变了。

如果所有客户端可见状态都没变，而且时间间隔又没超过 TTL，那么源码会把原因标得更接近：

> server-side routing / eviction（服务端路由或缓存淘汰）。

这避免工程师看到 cache miss 就盲目重构本地 Prompt。

评测 Context Cache 时也应该照这个思路：

> **先证明是客户端前缀变化，再优化客户端。**

---

## 15. 大 Context 怎么扩展：Claude Code 的答案不是“只用 1M 模型”

当前源码已经形成多层 Context Pressure Relief（上下文压力释放）：

~~~text
Tool Result Budget
→ Snip
→ Microcompact
→ Cached Microcompact
→ Context Collapse
→ Session Memory
→ Auto Compact
~~~

这些层解决的问题不同。

即使 Context Window 变成 1M，仍然有输入成本、prefill latency、Prompt Cache、旧 Observation 干扰、Resume 体积和 Tool Result 噪声。

所以大窗口主要会移动阈值，而不会让这些机制全部失去意义。

---

## 16. 几万个 Tool 怎么扩展：关键是“定义 Token”，不是数量

Claude Code 已经能按 Deferred Tool definition tokens / Context Window 决定 Tool Search。

当 Tool 数量进一步变大，当前架构自然可以继续扩展：

~~~text
Full Tool Pool
→ Permission / Mode 预过滤
→ deferred catalog
→ Tool Search
→ tool_reference top-K
→ 后续加载完整 schema
~~~

未来无论 search 内部升级成更强的 semantic retrieval（语义检索）还是分层 namespace，核心边界仍然成立：

> **模型不要一开始就看到 Host 拥有的全部能力。**

评测也不应该只测 Tool Search latency。

至少要看 relevant tool recall@K、wrong-tool rate、schema tokens actually loaded、发现后真正执行成功率，以及 Tool Catalog 变化是否破坏 Prompt Cache。

---

## 17. 几万个 Skill 怎么扩展：完整正文绝不能都进 Prompt

Claude Code 已经把 Skill 分成：

~~~text
frontmatter metadata
        ↓
Skill discovery
        ↓
选中 Skill
        ↓
加载完整 SKILL.md
        ↓
必要时 fork Subagent
~~~

源码对 Skill frontmatter 单独做 Token estimate，就是因为完整正文不属于目录发现阶段。

如果未来 Skill 数量非常大，合理扩展方向仍然是 scope / project / path 先过滤，再做 Skill Search，只暴露 top-K metadata，选中后读取正文，重 Skill 放 forked context。

这里和 Tool Scale 有共同原则：

> **Discovery representation（发现用表示）应该远小于 Execution representation（执行用表示）。**

---

## 18. Memory 很大以后为什么要把 Recall 放后台

长期 Memory 数量增长时，检索本身也会增加延迟。

Claude Code Relevant Memory Prefetch 的设计已经给出一个很实用的取舍：

~~~text
Memory selector
与
主模型第一步
并行
~~~

如果赶得上，就在后续 iteration 注入。

赶不上，就不阻塞用户。

规模越大，这个设计越重要，因为 Memory retrieval 不应该成为每个 turn 的固定 critical path（关键路径）。

后续优化可以关注 selector latency、manifest 规模、topic memory 质量、prefetch hit timing 和 Recall 的端到端收益，而不是只追“召回更多”。

---

## 19. Claude Code 源码现有验证能证明什么

这个私有镜像没有公开仓库那样清晰的完整测试目录 / release metadata，因此不能虚构“源码有一套完整 Eval Harness”。

我们能直接确认的是大量 Runtime instrumentation（运行时埋点）和 test-exported helper（为测试导出的辅助函数），以及源码中的 contract / defensive comments。

现有可观测证据包括：

- API success / error / retry；
- Token 和成本；
- Prompt Cache read / create / break cause；
- Tool execution；
- Skill invocation；
- Memory loaded / extraction；
- MCP connection；
- Agent progress；
- query profiler；
- session tracing。

这些能很好地回答：

> **系统内部发生了什么？**

但不能单独证明：

> **Claude Code 最终把用户任务做对了。**

因此真正的产品 Eval 还要在源码 Runtime 之上建立任务级验证。

---

## 20. Context、Memory、Tool 和 Multi-Agent 分别应该怎样评测

### Context

设计一个长任务：

~~~text
最开始：
“不能修改公开 API”

→ 多轮 Tool
→ Microcompact
→ Auto Compact
→ 退出进程
→ Resume
→ 继续修改
~~~

最终检查约束有没有保留。

还应 A/B Cached Microcompact on / off、不同 Auto Compact 阈值、Tool Search on / off，同时看任务成功和 cache read tokens，而不是只看摘要质量。

### Memory

要测 durable extraction precision、用户 correction、stale memory、relevant memory top-K、prefetch 是否及时赶上，以及 Memory ON / OFF 任务收益。

### Tool

要分 Discovery、Selection、Input validity、Permission correctness、Sandbox、Execution、Cancellation、Result reuse。尤其要故障注入 streaming fallback，验证副作用 Tool 不被执行两次。

### Multi-Agent

不能只看“子 Agent 返回了答案”。

还要测 delegation 是否必要、Subagent Tool / Permission isolation、Worktree 写冲突、background result delivery、agent resume、消息风暴，以及总 Token / latency 是否反而变差。

---

## 21. 场景题：Auto Compact 后模型忘了关键约束，怎么排查

不要第一反应说“换更强模型”。

按真实生命周期：

1. 约束最初来自 User message 还是 CLAUDE.md？
2. 动态 nested CLAUDE.md 是否真的注入？
3. Tool Result Budget / Snip 有没有错误删除相关上下文？
4. standard compact prompt 是否看见该约束？
5. `buildPostCompactMessages` 是否保留了必要 message？
6. compact boundary 后 API 是否只看到了正确新历史？
7. Resume 的 parentUuid 链是否又接回错误节点？
8. 如果是 Tool Search state，`preCompactDiscoveredTools` 是否保存？

这才是 Context Debug，不是只改 Summary Prompt。

---

## 22. 场景题：Tool Search 开启后 Agent 反而总找不到工具

排查顺序应该是：

~~~text
这个 Tool 是否在当前 Tool Pool？
        ↓
是否被判定为 deferred？
        ↓
Tool Search 当前模式是否启用？
        ↓
search hint / name / description 是否可检索？
        ↓
ToolSearch top-K 是否命中？
        ↓
返回的 tool_reference 是否写入历史？
        ↓
extractDiscoveredToolNames 是否恢复到已发现集合？
        ↓
后续 API request 是否真的加载对应 schema？
~~~

如果搜索命中了，但模型下一步仍选错，是 selection 问题。

如果 schema 根本没进入下一轮，是 dynamic loading / Context state 问题。

两者不能混。

---

## 23. 场景题：Memory Recall 很高，但任务结果下降

Claude Code 的架构给出几个很具体的排查点：

- `MEMORY.md` 是否已经太长；
- topic memory 是否重复；
- selector 是否把“相关”误当成“有用”；
- 已经成功工作的 Tool 文档是否没有被抑制；
- stale project fact 是否本应重新 Read；
- 同一 Memory 是否因为 attachment / Tool read 去重失效被重复注入；
- Agent-specific Memory 是否污染主 Agent。

最终用 Memory ON / OFF 任务结果验证，而不是把 recall rate 当目标函数。

---

## 24. 场景题：API Stream 失败，什么时候不能随便 Retry

关键问题是：

> **这个流已经产生了什么副作用？**

如果还只是模型文本，没有真实 Tool 开始，重试通常简单得多。

如果 Streaming Tool Executor 已经启动了 Bash / MCP / Write：

~~~text
旧 stream 已产生 side effect
        ↓
新 request 重新生成同一 tool_use
        ↓
重复执行风险
~~~

此时必须识别旧 partial response、tombstone / discard、保证旧执行与新 Tool Result 不混链，并对非幂等动作建立更严格的去重语义。

这比“网络失败指数退避”高一个层级。

---

## 25. 从 Claude Code 源码能抽出的几个系统原则

**第一，Context 压缩应该分层。** 先处理大 Tool Result，再局部裁剪，再做完整摘要；不要把所有压力都交给一个 Summary Agent。

**第二，Prompt Cache 是架构约束。** API-bound input 不要随便原地修改；Tool Schema、System Prompt、Compaction 都会影响缓存。

**第三，Memory 应按生命周期拆开。** 项目指令、当前 Session continuity、跨 Session durable memory 和当前问题 retrieval 不是一件事。

**第四，大能力目录要动态发现。** Tool / Skill 都应该用小的 discovery representation，再按需加载完整执行内容。

**第五，权限是多层决策。** Tool validation、Hook、配置规则、classifier、用户批准和 OS Sandbox 各自解决不同问题。

**第六，恢复语义必须跟着 Context 变换走。** Compact / Snip 修改模型历史以后，Transcript parent chain 也必须同步，否则优化只在当前进程里有效。

**第七，多 Agent 是资源与隔离问题，不只是 Prompt 协作。** Tool Pool、Permission、Worktree、后台任务和消息路由都要有边界。

---

## 26. 源码锚点

1. [`utils/sessionStorage.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts)：Transcript、parentUuid、Compaction / Snip 持久化。
2. [`utils/sessionRestore.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionRestore.ts)：Resume 状态恢复。
3. [`tools/AgentTool/AgentTool.tsx`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/AgentTool.tsx)：Subagent、异步执行、Worktree、Team 路径。
4. [`tools/AgentTool/runAgent.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/runAgent.ts)：Subagent 如何复用 query Runtime。
5. [`tools/SendMessageTool/SendMessageTool.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SendMessageTool/SendMessageTool.ts)：Agent / Team 消息、恢复和跨 Session 安全。
6. [`services/api/withRetry.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/withRetry.ts)：错误分类、前后台 retry、capacity handling。
7. [`services/api/claude.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/claude.ts)：streaming、fallback、Prompt Cache、Tool API request。
8. [`services/api/promptCacheBreakDetection.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/promptCacheBreakDetection.ts)：cache break attribution。
9. [`utils/sandbox/sandbox-adapter.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sandbox/sandbox-adapter.ts)：OS Sandbox 与安全加固。
10. [`query.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)：所有机制重新汇入主 Agent Loop 的地方。

回到：[Claude Code 系统总览](README.md)
