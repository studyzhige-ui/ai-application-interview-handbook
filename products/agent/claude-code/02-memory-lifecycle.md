# 02. Claude Code Memory Lifecycle｜CLAUDE.md、Session Memory 与长期 Auto Memory 怎样分工

[← Context](01-context-lifecycle.md) · [Claude Code 总览](README.md) · [Tool →](03-tool-lifecycle.md)

> **源码镜像基线：** `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`

Claude Code 是最不适合用一句“它有 Memory”概括的产品之一。

当前源码里至少可以看到四种容易被混淆的长期 / 半长期信息机制：

~~~text
CLAUDE.md / Rules
项目和用户明确写下的指令

Session Memory
当前 Session 内为长任务维护的演进摘要

Auto Memory
从过去 Session 自动提取、跨 Session 保存的长期记忆

Relevant Memory Recall
面对当前新问题，从长期 Memory 中再挑少量真正相关内容
~~~

另外，Subagent（子智能体）定义还可以拥有独立 Memory scope（记忆范围）。

如果把这些都叫“Memory 文件”，就会失去最重要的设计边界：**谁写、保存多久、什么时候进 Context、谁有权修改、过期以后怎样维护。**

---

## 1. 先把 CLAUDE.md 从“长期记忆”里拿出来

Claude Code 源码历史上把 CLAUDE.md 一类内容放在 memory file 相关函数中，但语义上它更像 instructions（指令）。

用户或项目维护者明确写：

~~~markdown
这个仓库使用 pnpm。
改数据库 migration 前必须先阅读 docs/db.md。
~~~

它的来源是当前文件系统，作用范围通常和目录、项目或用户配置绑定。

这和“Claude 从以前对话中观察到用户长期偏好 pnpm”是完全不同的证据。

前者是明确项目规范，后者才更接近自动长期 Memory。

所以学习 Claude Code 时，最好固定这条区分：

~~~text
CLAUDE.md
= author-written instructions

Auto Memory
= conversation-derived durable knowledge
~~~

Context 篇已经讲过 CLAUDE.md 会按目录动态加载。这里不重复它的 Context 细节，只强调：**它不是 Auto Memory 的写入结果。**

---

## 2. Auto Memory 的磁盘结构从 `MEMORY.md` 开始

长期 Auto Memory 的核心实现主要在：

- `memdir/`
- `services/extractMemories/`
- `services/autoDream/`

`memdir/memdir.ts` 把 `MEMORY.md` 作为长期 Memory 的入口文件。

但它不会允许这个入口无限增长。当前源码对入口读取有明确的行数和字节上限，例如大约前 200 行、25KB 级别的限制。

原因很重要：

> **Memory 的存储容量可以很大，但默认注入模型的 Memory 入口必须很小。**

否则 Auto Memory 越用越久，最终又会退化成：

~~~text
所有过去信息
→ 每轮全部注入
→ Context 爆炸
~~~

因此 `MEMORY.md` 更像长期 Memory 的“导航和高密度摘要”，更具体的信息可以放到其他 topic memory（主题记忆）文件。

---

## 3. Claude Code 想记住什么，而不是什么都记

`memdir` 中的 Memory Prompt 对长期信息类型有明确约束。

可以看到类似下面的分类思想：

- user：用户长期偏好、工作习惯；
- feedback：用户对 Claude 行为的纠正；
- project：难以从当前仓库直接重建、但未来仍有价值的项目事实；
- reference：长期可复用参考信息。

其中有一个很值得注意的原则：

> **如果事实可以很容易从当前 Repo 重新读出来，就不应该因为“见过一次”而永久复制进 Memory。**

比如：

~~~text
src/auth/index.ts 里现在有函数 foo()
~~~

这是当前仓库内容，未来可能变化，而且随时可以重新 Read。

把它永久写进 Memory 反而容易形成 stale knowledge（陈旧知识）。

而下面的信息更适合长期保存：

~~~text
用户多次明确要求：
“写解释时先给结论，再展开证据。”

或：

“这个内部系统的部署入口在一个当前仓库里看不到的服务。”
~~~

这说明 Memory Write Policy（记忆写入策略）的目标不是“信息越多越好”，而是：

> **把未来不容易重新恢复、又确实能改善后续任务的信息留下。**

---

## 4. 一次 Session 怎样自动产生长期 Memory

长期 Memory 的自动提取主要在：

- `services/extractMemories/extractMemories.ts`

它不是每个 Tool Call 后都同步运行。

源码把它接成 complete query（完整查询结束）后的 stop hook（停止钩子）。换句话说，用户的一轮真实工作先完成，后台再考虑是否从这段会话中提取长期 Memory。

这样做有几个好处。

第一，不增加主任务每一次模型循环的延迟。

第二，等一轮工作走完以后，更容易判断哪些只是中间猜测、哪些最后被用户纠正、哪些结论真正成立。

第三，Memory 提取失败不会让用户正在做的编码任务也跟着失败。

这符合一个很重要的系统边界：

> **长期记忆是辅助平面，不应该成为主任务成功的同步依赖。**

---

## 5. Memory Extraction 为什么有 cursor，而不是每次重新总结整个 Session

`extractMemories` 会记录类似 `lastSummarizedMessageId` 的 cursor（游标）。

它的作用是：

~~~text
上次已经处理到这里
        ↓
这次只看后面新增、真正 model-visible 的消息
~~~

这避免一条很长 Session 每次结束都重新总结从第一句开始的全部历史。

如果提取成功，cursor 才前进。

如果提取失败，cursor 不前进。

因此下一次还有机会重新考虑这批消息。

这种语义很重要：

> **失败不能被误认为“已经处理过”。**

否则一次后台模型错误就会永久丢掉那一段 Memory 候选。

---

## 6. 为什么主 Agent 已经直接写 Memory 时，后台提取反而要跳过

Claude Code 主模型本身可以通过文件 Tool 修改 Auto Memory 目录。

如果用户明确说：

> “把这个记住。”

主 Agent 可能已经直接更新了对应 Memory 文件。

这时 complete-query 后的后台 extraction 如果再根据同一段 transcript 生成一次，很容易重复写、覆盖用户刚刚确认的版本，或用自动推断稀释显式修改。

源码因此会检查本轮是否已经有直接 Memory write（记忆写入）。

如果发现主 Agent 已经写过 Auto Memory，后台 extractor 会跳过这批内容并推进 cursor。

可以把这理解为一种 writer arbitration（写入者仲裁）：

~~~text
显式、在线写入
优先于
后台自动提取
~~~

这比“所有写路径最后互相覆盖”更稳定。

---

## 7. Memory Extractor 不是普通 Claude Code，它被锁在 Memory 目录里

自动提取使用 `runForkedAgent` 启动一个隔离的内部 Agent。

这个 Agent 的 Tool Permission（工具权限）很窄。

当前源码近似允许：

- Read / Grep / Glob 等只读能力；
-只读 Bash；
-对 Auto Memory 目录内使用 Edit / Write。

其他工具默认拒绝。

这条设计很值得学习。

Memory Extractor 需要语义理解能力，因此让模型参与很合理；但它并不需要访问任意网络、修改用户代码、运行高风险命令或调用所有 MCP 服务。

所以正确边界不是：

> “这是内部 Agent，可以全放开。”

而是：

> **给内部维护 Agent 完成这一职责所需的最小能力。**

---

## 8. Extraction 为什么采用 best-effort（尽力而为），还要合并并发触发

会话可能快速连续完成多个用户轮次。

如果每次 stop hook 都立刻启动一个 Memory Extractor，会产生并发竞争。

源码维护 in-progress 状态、节流和 pending coalesced context（待处理合并上下文）。

当一个提取正在运行，又来了新的触发，不是再开第二个并行 writer，而是把“还有新内容需要处理”记下来，当前结束以后再运行最新一批。

这和数据库后台 compaction 很像：

> **Memory maintenance 允许延迟，但不能同时让多个 writer 争抢同一份长期状态。**

---

## 9. AutoDream：为什么提取之后还需要跨 Session 整理

即使每条 Session 都能生成不错的 Memory，长期使用以后仍会出现同一个偏好重复多次、用户后来改变想法、旧项目事实过期、主题文件越来越碎等问题。

所以源码还有：

- `services/autoDream/autoDream.ts`

AutoDream（自动记忆整理）是比 per-session extraction 更慢的一层跨 Session 的 Consolidation（整合）。

它不会每次都跑。

当前代码会考虑距离上次 consolidation 的时间、新增 Session 数、后台扫描节流、跨进程 lock（锁）、当前是不是 remote / 特殊模式，以及 feature gate。

默认策略中能看到“小时 / 天”和“若干 Session”级别的维护节奏，而不是每一轮立刻重整全部 Memory。

原因是 consolidation 本身有成本，而且长期 Memory 的结构不需要因为一句普通新消息就重写。

---

## 10. AutoDream 也使用受限 Agent，而且失败后允许未来重试

AutoDream 同样通过 forked agent 操作 Memory 目录，沿用受限写权限。

执行成功后，系统可以把结果以类似“Improved memories”的 system surface（系统提示面）反馈给会话。

如果失败，源码会处理 lock / mtime（修改时间）状态，让未来还能重新尝试，而不是把失败误标成“本周期已经成功维护过”。

这里和 Extraction cursor 的思想是一致的：

> **后台 Memory job 的完成状态必须反映真实成功，否则会形成静默数据丢失。**

---

## 11. 新问题来了以后，不会把整个 Memory 目录全部塞进 Prompt

`MEMORY.md` 是入口，但 topic memories 可能很多。

Claude Code 因此还有 Relevant Memory Recall（相关记忆召回）：

- `memdir/findRelevantMemories.ts`
- `utils/attachments.ts`

它的运行方式很有特点。

### 先用一个 side query 选候选

`findRelevantMemories` 会扫描 Memory manifest（清单），然后用一个轻量 side query（侧查询）根据当前用户问题判断哪些 Memory 文件真正有帮助。

当前实现最多选择少量候选，源码中可以看到上限约 5 个。

这不是“相似度越高越全部拿回来”，而是 Prompt 直接要求：只有明确能帮助当前任务的 Memory 才应该选择。

### `MEMORY.md` 不重复进候选

入口 summary 已经在 Context 中，就不应该再次通过 relevance search 重复注入。

这体现了 Memory 系统的去重意识：

~~~text
全局入口
≠
按需证据
~~~

---

## 12. Recall 为什么是非阻塞 Prefetch，而不是让用户等一次额外模型请求

这部分是 Claude Code Memory 很值得学习的设计。

`startRelevantMemoryPrefetch` 会在用户轮次开始时异步启动 relevant memory search。

但主模型不会等它。

代码注释非常明确：

> prefetch runs while the main model streams and tools execute。

也就是说：

~~~text
用户请求
├─→ 主模型开始工作
│
└─→ Memory relevance side query 并行运行
~~~

等 Tool 执行结束、主循环准备下一次采样时：

- 如果 Memory prefetch 已经完成，就消费结果；
-如果还没完成，**零等待跳过**；
-下一次 loop iteration 再检查；
-如果整个用户轮次结束都没赶上，就不为了 Memory 单独阻塞。

这是一种非常现实的 latency trade-off（延迟权衡）：

> **长期 Memory 有帮助，但不能为了“也许有帮助”强制给每个用户轮次增加一段串行延迟。**

---

## 13. Relevant Memory 怎样控制噪声和重复

Recall 不只是 top-5，它还做多层过滤。

### 已经出现在当前 Session 的 Memory 不再重复

`collectSurfacedMemories` 会扫描当前 messages 中过去注入的 relevant memory attachments（相关记忆附件），收集 path 和累计 bytes。

如果当前 Session 已经注入过某个 topic memory，不再让 selector 把它重复选一次。

### 已经被文件 Tool 读过的 Memory 也不再重复

`readFileState` 会记录本轮 Read / Write / Edit 过的文件。

即使 relevance selector 选中了一个 Memory，如果主模型已经通过 Tool 自己打开过它，attachment 层会过滤掉。

### Session 有总 Memory 体积上限

当当前 Session 已经通过 relevant-memory attachment 注入足够多 Memory，Prefetch 可以停止继续追加。

这能防止“用户连续问相关问题 → 每轮再塞 5 个 → Context 迟早爆掉”。

---

## 14. 为什么 selector 还会看“最近哪些 Tool 已经工作正常”

`collectRecentSuccessfulTools` 会统计上一段工作中哪些 Tool 成功、哪些失败。

这组信息会交给 Memory relevance selector。

源码注释解释了目的：

> 如果某个 Tool 已经工作正常，就不要因为用户提到它而自动塞一堆“这个 Tool 怎么用”的 Memory 文档；那是噪声。

但如果 Tool 出错，相关 gotcha（注意事项）和排障经验仍然值得被选中。

这是一个很细但很成熟的 Retrieval Policy（检索策略）：

~~~text
“当前话题相关”
并不自动等于
“现在值得注入”
~~~

Context 中已经证明“工作正常”的能力，不需要 Memory 再重复教育模型。

---

## 15. 被选中的 Memory 仍然有行数和字节上限

Selector（筛选器）认为某个 Memory 很相关，也不能把整个超大文件无限注入。

`readMemoriesForSurfacing` 会使用 max lines 和 max bytes 读取候选文件。

如果被截断，Claude Code 不会假装内容完整，也不会直接把整份 Memory 丢弃。

它会注入前面有价值的部分，并加提示：

> 这个 Memory 被截断了，如需完整内容请用 Read Tool 打开对应路径。

这是一种很好的 progressive recall（渐进式召回）：

~~~text
先给足以判断是否有用的开头
→ 模型确认需要
→ 再主动 Read 完整文件
~~~

Memory Retrieval（记忆检索）因此和普通 Tool System 自然连接起来。

---

## 16. Agent Memory：Subagent 还能拥有自己的长期范围

`AgentTool` 加载的 Agent Definition（智能体定义）可以声明 Memory scope。

源码在启动 Subagent 时会记录对应 Memory loaded telemetry；Relevant Memory Prefetch 如果发现用户明确 @mention 某个有独立 Memory 的 Agent，还会把 relevance search 限制到这个 Agent 的 Memory 目录。

所以 Claude Code 的长期记忆并不一定只有一个“全用户全局库”。

它可以形成：

~~~text
main auto memory

agent A memory

agent B memory
~~~

不同 Agent 角色拥有不同工作知识。

这对专门化 Subagent 很合理，但也带来一个新的 Eval 问题：

> Agent A 的 Memory 是否会错误污染 Agent B？

后面的 Engineering 篇会把这种 isolation（隔离）列入 Memory 测试。

---

## 17. Session Memory 又是什么：它解决的是“这条长会话快装不下了”

`services/SessionMemory/sessionMemory.ts` 和 Auto Memory 完全不是同一个生命周期。

Auto Memory 面向**下一次、下一个 Session**。

Session Memory 面向**当前这条 Session 还要继续工作**。

它会观察当前 Session 的 Token 增长和自然边界，在达到条件时提取一份演进摘要，帮助 Context Compaction。

它也使用一个受限 forked agent，而且只允许写精确的 Session Memory 文件。

所以：

~~~text
Session Memory
≈ current-session working continuity

Auto Memory
≈ cross-session durable knowledge
~~~

如果面试时把二者都说成“长期记忆”，就会漏掉它们不同的失效时间和目标。

---

## 18. 用一个例子串完整 Memory 生命周期

假设用户在今天的 Session 中反复说明：

> “我做这个仓库时，希望 Claude 不要先重构；先做最小修改，通过测试以后再考虑清理。”

这条信息不是 CLAUDE.md，因为用户并没有修改项目指令文件。

Session 完成以后，`extractMemories` 的 stop hook 发现自上次 cursor 后有新 model-visible history，于是启动受限 forked agent。

Extractor 判断这是未来可能有帮助的工作偏好，把它写进 Auto Memory topic 文件，并维护 `MEMORY.md` 入口。如果主 Agent 本轮已经直接写过同一 Memory 目录，后台 extraction 会跳过，避免竞争。

过了若干 Session，AutoDream 发现达到跨 Session consolidation 条件，对重复或冲突的 Memory 做整理。

几天后用户又说：

> “帮我修一下这个回归。”

主请求立即开始；与此同时 relevant-memory prefetch 在后台根据“修回归”这一问题选择少量相关 Memory。

如果“先最小修改再清理”被判断确实有帮助，并且当前 Session 还没注入过，它会在某个后续 query iteration 作为 attachment 进入 Context。

用户随后明确说：

> “这个项目不用再遵守最小修改了，我现在希望优先重构。”

主 Agent 可以直接更新长期 Memory；下一次 background extractor 看到本轮已经有直接 Memory write，就不会再根据旧对话自动写一遍。

真正完整的 Memory 生命周期因此是：

~~~text
会话事实
→ 自动提取 / 显式写入
→ 持久 Memory 文件
→ 周期性 consolidation
→ 新任务非阻塞 relevance recall
→ 有界注入
→ 用户修正
→ 后续长期基线更新
~~~

---

## 19. Claude Code Memory 应该怎样评测

源码提供了许多 telemetry（遥测）和事件，但“后台任务运行成功”不代表 Memory 真有价值。

至少应该分四层。

**写入质量：** 给一段已标注历史，检查真正长期偏好有没有被提取、一次性要求有没有被误记、可以从 Repo 重建的易变事实有没有被多余持久化、用户纠正是否覆盖旧信息。

**Recall 质量：** 给当前任务 + 大量 Memory 文件，检查相关文件有没有进 top-5、不相关 Memory 是否被过滤、已经通过 Tool 读过的文件是否避免重复、正常工作的 Tool 文档是否被抑制。

**延迟与成本：** Relevant Memory Prefetch 的设计目标之一就是“不能阻塞主任务”，所以要测 prefetch 命中率、在第几个 query iteration 赶上、因为未完成而跳过的比例、额外 side-query Token / latency。

**End-to-End Utility（端到端效用）：** 最终还是比较 Memory ON vs Memory OFF 的任务成功率、重复询问用户次数、错误个性化、stale Memory 导致的失败和 Context Token 增量。

Memory recall 很高但任务变差，不是好系统。

---

## 20. 源码锚点

1. [`context.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/context.ts)：CLAUDE.md 与 User Context，理解“指令”和 Auto Memory 的边界。
2. [`memdir/memdir.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/memdir/memdir.ts)：MEMORY.md、Memory prompt 和入口预算。
3. [`memdir/findRelevantMemories.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/memdir/findRelevantMemories.ts)：按当前问题选择长期 Memory。
4. [`services/extractMemories/extractMemories.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/extractMemories/extractMemories.ts)：Session 结束后的长期 Memory 提取。
5. [`services/autoDream/autoDream.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/autoDream/autoDream.ts)：跨 Session consolidation。
6. [`services/SessionMemory/sessionMemory.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/SessionMemory/sessionMemory.ts)：当前 Session 的演进摘要。
7. [`utils/attachments.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/attachments.ts)：Relevant Memory Prefetch、有界注入和去重。
8. [`tools/AgentTool/AgentTool.tsx`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/AgentTool.tsx)：Agent Memory scope 与 Subagent 接入。

下一篇：[Claude Code Tool Lifecycle →](03-tool-lifecycle.md)
