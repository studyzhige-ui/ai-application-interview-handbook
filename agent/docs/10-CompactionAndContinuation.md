# 10. Context Compaction：压缩、替代历史与继续执行

`AGENT-009` Context Compaction（上下文压缩） 是整个 Agent 真人面经里最强的信号之一。

但真正需要掌握的不是：

> “上下文太长就总结一下。”

而是：

> **当 Context 接近预算上限时，Runtime（运行时执行系统） 怎样压缩历史，同时保证当前任务仍然能正确继续？**

成熟Compaction不仅生成摘要，还要选择输入、安装替代历史、保存必要记录并继续执行；它不是天然的跨系统数据库事务。

[← 上一章](09-ContextAssemblyAndCache.md) · [Agent 目录](../README.md) · [下一章 →](11-MemoryLifecycle.md)

---

<a id="section-1"></a>

## 1. Compaction 为什么存在

<a id="legacy-10-01"></a>

Compaction（上下文压缩）为**接下来的模型调用**缩减输入。Summary（摘要）是压缩可能产生的文本；Resume（恢复执行）是把中断的工作继续起来，二者不是同一个词。长期Memory（记忆）则为未来任务保留可复用信息。把这三个目的分开，很多“为什么已经保存还要压缩”的疑惑就消失了。

报告任务读完几十次文件后，下一步只需要“哪些结论已确认、哪些证据缺失、用户禁止什么、产物在哪里”。它通常不需要每次重新读全部日志。但是原始证据或操作回执可能仍有用途，应留在适当存储里，不能随摘要一起误删。

随着 Agent 运行：

```text
User Message
Assistant Message
Tool Call
Tool Result
Plan
Memory
RAG Evidence
File Content
Error / Retry
```

不断累积。

如果不处理：

```text
Token ↑
Cost ↑
Latency ↑
Noise ↑
最终超过 Context Window
```

即使窗口足够大，也不代表应该无限保留：

> **Long Context Capacity ≠ 无限有效注意力 ≠ 免费存储。**

---

<a id="section-2"></a>

## 2. Compaction 与普通 Summary 的区别

<a id="legacy-10-02"></a>

普通 Summary 只关心：

```text
把长文本变短
```

Runtime Compaction 还必须关心：

```text
当前 Goal 还在吗？
约束还在吗？
已经完成什么？
哪些 Tool Side Effect 已发生？
当前 Workspace / Artifact 在哪里？
有哪些 unresolved problem？
哪些 approval 已经给过？
哪些状态不能重复执行？
```

所以正确抽象是：

```text
Compaction
= Select
+ Summarize / Project
+ Preserve Invariants
+ Build Replacement History
+ Persist
+ Recompute Budget
+ Trace / Validate
```

```text
旧模型输入：稳定指令 + 工具说明 + U1/A1/R1/.../U2/A2/R2
                          ↓ 选取需要处理的历史视图
摘要请求：历史视图 + 压缩指令（模型接口另有基础指令）
                          ↓
新模型输入：仍需的稳定指令与工具说明 + 保留的用户意图/摘要/近期项/附件
```

这是生命周期示意，不是两产品完全相同的消息数组。压缩关键不只是生成摘要，还包括**选择输入、检查结果、安装替代历史、补回仍需信息、重新计算预算、继续执行**。把摘要追加在旧历史后面并没有减少输入；只留下摘要则可能丢掉工具关联、当前约束或必要环境信息。

“System Prompt是不是绝对不参与压缩？”不能只答是或否：要区分**被替换的历史**与**摘要模型收到的完整请求**。基础指令通常仍独立提供，不应依赖有损摘要保存授权规则；但上下文中可能存在developer消息、CLAUDE.md合成用户消息及系统提醒，摘要模型可能看见它们。下面分别给出实际路径。

---

<a id="section-3"></a>

## 3. Compaction 什么时候触发

<a id="legacy-10-05"></a>

常见触发可以分：

### 3.1 Token Threshold

```text
estimated_context_tokens > soft_limit
```

提前压缩，而不是等 Provider（模型服务方） 报 `context_length_exceeded`。

### 3.2 Phase Boundary

例如：

```text
一个大 Task 完成
→ 切换到下一个阶段
```

此时适合把“旧阶段的过程细节”压成阶段结论。

### 3.3 Tool Result Pressure

大量日志 / 文件 / Search Result 造成 Context 激增。

这时优先：

```text
Offload / Reference
```

不一定马上压整个 Conversation。

---

<a id="section-4"></a>

## 4. 哪些信息必须保留

<a id="legacy-10-06"></a>

保留在哪里也很重要：高风险回执、授权和取消状态应在程序可靠记录中；摘要保留影响后续决策的结论与引用。不是把所有事实的唯一副本都塞进一个大摘要。

建议至少定义一个 Compaction Invariant Set。

#### Goal / Acceptance

```text
当前主目标
完成标准
禁止事项 / Constraints
```

#### Runtime Progress

```text
已经完成的步骤
当前进行到哪里
下一步候选
Blocked 原因
```

#### Side-effect Ledger

```text
Tool X 已经写 DB
Tool Y 已经发送消息
Payment request 已提交 idempotency_key=...
```

这类信息丢失会导致 Resume 后重复副作用。

#### Artifact References

```text
修改过哪些文件
日志 artifact 在哪里
测试结果 path / id
```

#### Unresolved Evidence

```text
哪些假设未验证
哪些测试仍失败
哪些用户问题未回答
```

摘要优先保留会影响**下一步决策**的信息：当前目标、未决约束、已完成步骤、关键证据与待办。可重复获取的大文件只需有可解析引用；临时噪声和已过期猜测可以去掉。高风险动作回执应由程序保存，摘要可以写“操作op7已确认，见回执”，不应保存它的唯一副本。

计划从P1修订为P2时，摘要应说明P2是当前计划及为何受阻，而非把两个计划并列成同等有效事实。压缩后发现原文件变更，需要重新读取；即使摘要完全忠实，它描述的也只是当时信息，不会自动跟随外部世界更新。

---

<a id="section-5"></a>

## 5. 哪些内容适合压缩或外部化

<a id="legacy-10-07"></a>

例如：

```text
重复 Tool Schema
大量 raw log
已经完成阶段的逐步对话
旧搜索结果
可通过 artifact id 重新取回的文件
```

原则：

> **丢过程之前先确认能否重建。**

如果某个结果无法再次获取，又会影响后续决策，就不能只留一句模糊 Summary。

---

<a id="section-6"></a>

## 6. Replacement History 为什么重要

<a id="legacy-10-08"></a>

一种危险做法：

```text
old history
+ summary message
```

这样旧内容仍然占 Context，根本没有真正压缩。

另一种危险做法：

```text
history = [summary]
```

但 Summary 丢失了 System / Current User Goal / Tool Correlation。

更合理的是：

```text
Stable Instructions
+ Required Current State
+ Compact Summary
+ Recent High-value Events
+ Artifact References
```

形成新的 Replacement View。

这也解释了为什么 Codex `compact.rs` 会专门处理 replacement history，而不是只生成一个文本字段。

---

<a id="section-7"></a>

## 7. Compaction Correctness 怎样验证

<a id="legacy-10-09"></a>

`AGENT-010` 直接问：

> Summary 后如何验证信息没有丢坏？

至少可以分四层。

### 7.1 Structural Invariant

例如：

```text
current_goal exists
current_task_id exists
pending_steps preserved
side_effect_ledger preserved
artifact refs resolvable
```

### 7.2 Semantic Invariant

把压缩前关键事实做成 checklist：

```text
Constraint A still present?
Decision B still present?
Failure C still unresolved?
```

### 7.3 Continuation Test

同一个 Agent 从：

```text
Before Compaction Context
```

和：

```text
After Compaction Context
```

继续执行，检查关键下一步是否一致。

### 7.4 Regression Eval

建立长任务数据集：

```text
run without compaction
vs
run with compaction
```

比较：

```text
Task Success
Wrong Re-execution
Missed Constraint
Cost
Latency
```

| 检查层次 | 文件报告中的检查 | 局限 |
|---|---|---|
| 结构 | 当前目标、未决项、引用能找到 | 字段存在不保证含义正确 |
| 语义 | “不修改原件”没有被改成“允许修改” | 需要规则、人工或校准评审 |
| 继续执行 | 压缩后仍去补缺失证据，不重复已完成写入 | 模型存在随机性，不能要求逐字相同 |
| 回归 | 固定任务集对比成功率、漏约束、成本与时延 | 测试覆盖仍有限 |

通用工程建议是先构造候选、验证，再安装新的活动视图，并保留适当回退依据。它不意味着两个产品都恰好实现同一套“五步事务”。压缩失败时应明确失败、缩减可重取材料或等待处理，不可直接把唯一历史删掉。

---

<a id="section-8"></a>

## 8. Compaction 失败怎么办

<a id="legacy-10-10"></a>

Compaction 自己也可能失败：

```text
summary model timeout
summary too long
provider context error
persistence failure
hook failure
```

不应该：

```text
原 history 已删
→ compaction failed
→ session destroyed
```

更稳的流程：

```text
1. Build compact candidate
2. Validate candidate
3. Persist replacement / metadata
4. Atomically switch active view
5. Keep prior generation for rollback
```

这是课程层的通用设计建议，不声称 Claude Code / Codex 恰好按这个五步实现。

候选摘要失败时先保留仍可核对的旧视图。缩减可重新读取的材料或有限重试后仍不满足要求，就明确暂停；不能直接清空唯一历史。HTTP成功和摘要语义正确也不是同一检查。

---

<a id="section-9"></a>

## 9. Stale Context 是另一类问题

<a id="legacy-10-11"></a>

Context 不超限，也可能坏。

例如：

```text
文件已经修改
但 Context 里还是旧文件内容
```

或者：

```text
用户已撤销某个约束
旧 Summary 仍说“必须遵守”
```

所以 Context Item / Summary 最好携带：

```text
source
version
timestamp / generation
```

当底层事实更新：

```text
invalidate / refresh / rehydrate
```

---

<a id="section-10"></a>

## 10. Summary Error 会产生“压缩后的错误记忆”

<a id="legacy-10-12"></a>

错误摘要很危险，因为它会变成新的高权重事实。

例如原始 History（历史记录）：

```text
User: 不要改数据库
Agent: 好的
```

Summary 错写：

```text
用户允许修改数据库 schema
```

后续模型可能稳定执行错误行为。

因此高风险 Constraint 应尽量：

```text
结构化持久化
```

而不是只存在自然语言 Summary。

---

<a id="section-11"></a>

## 11. Compaction 和 Memory 的边界

<a id="legacy-10-13"></a>

不要把两者混成：

```text
Compaction Summary = Long-term Memory
```

Compaction 目标：

```text
让当前 Run 在有限 Context 内继续
```

Memory 目标：

```text
让未来 Run / Future Turn 可以重新取回有价值信息
```

二者可以共享提取结果，但生命周期、写入标准和失效标准不同。

下一章进入 Memory。

---

<a id="section-12"></a>

## 12. 产品实现与官方资料对照（按需展开）

<details>
<summary>Codex `compact.rs` 给出的实现证据</summary>

<a id="legacy-10-03"></a>

### 固定源码：触发判定 → 摘要请求 → 替代历史 → 后续调用

**触发。** `session/turn.rs`在正常推理前检查是否需要自动压缩，推理后若仍需继续工具/输入循环，也会结合使用量检查。`session/context_window.rs`区分全窗口计数与扣除前缀的主体预算，还维护完整上下文上限；模型切换等路径有额外判定。因此不能写“Codex永远到90%就压缩”。手动请求另有独立入口。

**分支。** 该固定快照在`run_auto_compact`里按功能配置选择Token Budget（预算）管理、供应商支持的远端压缩或本地`compact.rs`。以下完整描述只针对本地摘要路径；远端输出与实现不能从本地提示推断。

**输入和提示。** `compact.rs`复制当前历史视图，加入压缩指令构造模型输入，基础指令单独提供，压缩请求不照搬正常工具执行循环。默认提示来自`codex-rs/prompts/templates/compact/prompt.md`，也允许配置覆盖。原文以“CONTEXT CHECKPOINT COMPACTION”标识这项交接任务。用中文概括，它要求为接替执行的模型写交接摘要，重点是：已做工作与决定、重要约束和偏好、剩余步骤、关键资料与引用，并要求简洁、有组织。它不是要求固定JSON Schema；局部小标题是结构化写作，不等于机器已校验字段。

**结果。** 本地路径提取助手返回的摘要字符串，添加summary prefix，并通过`build_compacted_history`组合选取的真实用户消息与摘要。源码有保留用户消息的预算上限；不能据此声称所有历史逐条不丢，也不能说输出就是原字段状态的无损备份。

**安装。** `replace_compacted_history`更新执行中的历史并记录压缩项，重新计算使用量。前轮/手动压缩使用`DoNotInject`，清掉初始上下文参考，使后续正常轮重新注入；轮中压缩使用`BeforeLastUserMessage`，把初始上下文放到最后真实用户消息之前，让摘要位于规定位置。两种路径不能画成同一个无条件顺序。

**失败。** 摘要请求本身过长时有移除旧项后再试的处理；短暂故障有有限退避。技术上能继续不代表摘要语义完整，仍需要长任务回归。此处没有承诺整个外部世界与替代历史构成原子事务。

</details>

<details>
<summary>Claude Code 侧提供了什么证据</summary>

<a id="legacy-10-04"></a>

### 用户固定快照：消息预算与多种压缩机制如何协作

`query.ts`可直接追踪到如下处理次序：取最近压缩边界后的消息→大工具结果预算/外部化→可选历史裁剪（snip）→微压缩（microcompact）→可选上下文局部折叠→自动压缩检查→发送模型请求。部分路径由编译或运行开关控制，**源码包含不等于所有公开构建同时启用**。

| 机制 | 改变什么 | 与摘要的区别 |
|---|---|---|
| 工具结果预算 | 将过大结果替成有限视图或产物引用 | 不一定调用模型 |
| 微压缩 | 清理符合条件的旧工具结果；某些构建支持缓存编辑 | 不等于总结整段对话 |
| snip/局部折叠 | 按功能开关裁剪或投影历史区段 | 与全量摘要可能相互协调 |
| 自动/手动完整压缩 | 生成交接摘要并重建后续消息 | 是本文主要摘要路径 |
| reactive压缩 | 某些开关下收到真实超长错误后补救 | 不能假设始终是默认策略 |

`autoCompact.ts`的普通自动路径先计算有效窗口：模型上下文窗口减去`min(模型最大输出, 20,000)`的摘要输出预留，再减去`13,000`余量作为阈值。环境覆盖和特性开关可改变判定；snip释放量会影响估算。**这些数字只属于该快照，不是教学建议。** 压缩/会话记忆子请求有递归保护；连续失败达到限制会停止无效尝试。

达到条件后，先尝试实验性的session-memory压缩路径，未采用时进入`compactConversation`。这条session-memory路径与跨会话auto memory文件不是同一概念。

`compactConversation`执行前置Hook（生命周期钩子），生成`getCompactPrompt`的摘要请求，调用摘要模型。它会对图片/文档等材料做适用处理，遇到摘要请求过长时可能按API轮组裁剪头部重试。摘要从助手文本提取，并检查空结果和API错误；不是自动得到一个经过Schema验证的恢复对象。

成功后按需恢复近期文件、异步任务、计划文件/规划模式、已调用技能、已发现工具和MCP说明等附件。`buildPostCompactMessages`明确顺序为：**压缩边界标记→摘要消息→需保留消息→附件→Hook结果**。下一次调用仍按第09章路径提供systemPrompt/userContext/tools，摘要不承担替代所有系统规则的责任。

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 13. HUMAN-A 信号

本章主要承接：

- `AGENT-009` Context Compaction：41 个独立来源；
- `AGENT-010` Compaction Correctness：15 个独立来源。

真实面试已经明显从：

```text
Context 满了怎么办？
```

追到：

```text
哪些信息不能丢？
怎么证明没压坏？
错误 Summary 怎么纠正？
```

---

<a id="interview"></a>

## 14. 面试怎么答

### Q：Agent Context 快满了怎么办？

🎯 **建议回答**：

> 我不会简单删除最老消息。先把大 Tool Result 外部化，再按 Context Source 做预算；需要 compaction 时，把它当成一次 Runtime State（状态） Transition：选择需要压缩的 history，生成 summary / projection，同时强制保留 goal、constraints、progress、side-effect ledger 和 artifact refs，构造 replacement history，持久化并重新计算 token usage。压缩后要做 invariant 检查和长任务 regression，避免 summary 错误导致后续重复执行或 goal drift。

### Q：怎样验证 Compaction 没丢信息？

🎯 **30 秒回答**：

> 结构化验证必保字段，再用 continuation test 和长任务 eval 比较压缩前后的 task success、constraint violation、re-execution 和 cost，而不是只看 summary 读起来是否通顺。

### Q：Compaction完整流程是什么？

🎯 **30 秒回答**：

> 先根据预算、阶段或人工请求触发，选择历史视图并生成交接摘要，保留当前目标、约束、未决工作及必要引用，再构造替代历史、补回初始上下文或附件，重新计算预算并继续。压缩是管理模型输入，不是业务状态备份。需要对语义和继续执行效果做回归。

### Q：Codex压缩提示是什么，输出是否JSON？

🎯 **30 秒回答**：

> 固定本地路径使用prompts/templates/compact/prompt.md，要求面向接替模型总结进度、决定、约束、剩余步骤和关键资料，支持配置覆盖。它是有组织的自然语言摘要提示，不是JSON Schema保证；程序把摘要文本与选取的用户消息组合为替代历史。远端压缩路径不能从这段提示推断。

### Q：Claude Code有几层压缩，何时触发？

🎯 **30 秒回答**：

> 固定快照有工具结果预算、微压缩、可选历史裁剪/局部折叠、自动/手动摘要以及可选超长补救路径，不是所有用户固定启用三层。普通自动判定用有效窗口减余量，且受模型、环境和特性开关影响；完整摘要后重建边界、摘要、保留消息、附件与Hook结果。

### Q：System Prompt是否会被压缩掉？

🎯 **30 秒回答**：

> 应区分被替换的历史与摘要模型实际看见的请求。基础指令往往单独提供并在正常调用保留或重注入；历史中仍可能含开发者上下文或合成系统提醒。不能笼统说只压user/tool或system永远不进摘要输入；必须按对应产品路径说明。

### Q：怎么防止摘要丢掉关键约束？

🎯 **30 秒回答**：

> 关键授权和操作回执不能只存在有损摘要中，程序独立保存必要状态。摘要检查目标、约束和待办，引用必须可解析；再做压缩前后继续执行和长任务回归。文字通顺和Token变少都不是正确性的充分证据。

---

<a id="pitfalls"></a>

## 15. 高频易错点

⚠️ **Compaction = Summary。** 只说了一小部分。

⚠️ **最老 History 全删掉就行。** 可能删掉关键决策和副作用事实。

⚠️ **Summary 正确性靠人工感觉。** Production（生产环境） 应有 invariant / regression。

⚠️ **Context 变短就一定更好。** 可能变成更短但错误的 Context。

⚠️ **Resume就是摘要。** Resume是恢复执行，Summary才是摘要。

⚠️ **压缩就是摘要加到历史尾部。** 必须构造更短替代视图，否则仍然占原预算。

⚠️ **Claude固定三层所有版本一样。** 多种路径受快照和特性开关控制。

⚠️ **压缩Prompt要求structured所以一定JSON。** 有组织文本与机器Schema是两回事。

⚠️ **摘要中保存回执足够防重复。** 恢复应依赖可靠操作记录与外部核对。

---

<a id="self-test"></a>

## 16. 本章自测

<details><summary>1. 为什么 Compaction 更像 Runtime Transaction？</summary>

因为它不仅生成摘要，还会改变 active history / context view，需要保持状态不变量、持久化、重新计算预算，并在失败时避免破坏可恢复性。

</details>

<details><summary>2. Side-effect Ledger 为什么是 Compaction 必保信息？</summary>

如果外部动作已经成功但这个事实在压缩中丢失，Agent Resume 后可能再次执行支付、发送、写入等不可重复副作用。

</details>

<details><summary>3. Stale Context 和 Context Overflow 有什么区别？</summary>

Overflow 是容量问题；Stale Context 是事实版本失效问题。即使 Token 很少，旧文件、旧权限、旧约束仍会导致错误决策。

</details>

<details><summary>4. 模型还没到窗口上限，为什么可能提前压缩？</summary>

要为输出、接下来工具结果和摘要请求预留空间；模型切换或任务阶段也可能触发。等硬上限才行动可能连摘要请求都发不出去。

</details>

<details><summary>5. 压缩后最老计划仍说读B，但B已被禁止，怎么检查？</summary>

对照当前约束与计划主视图，检查摘要是否保留最新约束；执行权限仍应阻止B。不能用旧摘要覆盖真实授权。

</details>

<details><summary>6. 本地Codex摘要结构清楚，能当检查点直接恢复吗？</summary>

不够。它主要支撑后续推理，活动操作、回执和环境状态有独立语义；自然语言摘要不保证外部写入一次且仅一次。

</details>

<details><summary>7. 系统规则没在历史里，摘要模型能不能看到它？</summary>

可能通过API独立基础指令字段看到。历史数组范围和完整API请求不是同一个集合，要看具体代码。

</details>

<details><summary>8. 压缩前后回答不逐字一样，是否压缩失败？</summary>

不能据此判断。模型本身存在随机性，应比较关键约束、任务结果、重复动作和证据质量等，而不是逐字一致。

</details>

<details><summary>9. session-memory compaction是不是把会话永久写入长期记忆？</summary>

不是由名称就能得出。它在固定Claude快照中是一条帮助缩减当前会话的可选压缩路径；跨任务auto memory有自己的保存和读取过程。

</details>

---

[← 上一章](09-ContextAssemblyAndCache.md) · [Agent 目录](../README.md) · [下一章 →](11-MemoryLifecycle.md)
