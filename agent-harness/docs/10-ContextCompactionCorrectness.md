# 10. 上下文压缩：什么时候压、压什么、怎样继续

[← 上一章](09-ContextAssemblyBudget.md) · [模块目录](../README.md) · [下一章 →](11-MemoryArchitectureLifecycle.md)

> 本章要解决：回答Codex与Claude Code的真实触发、提示、输入范围和压缩后消息形态。

## 1. Compaction不是恢复任务，也不是长期记忆

Compaction（上下文压缩）为**接下来的模型调用**缩减输入。Summary（摘要）是压缩可能产生的文本；Resume（恢复执行）是把中断的工作继续起来，二者不是同一个词。长期Memory（记忆）则为未来任务保留可复用信息。把这三个目的分开，很多“为什么已经保存还要压缩”的疑惑就消失了。

报告任务读完几十次文件后，下一步只需要“哪些结论已确认、哪些证据缺失、用户禁止什么、产物在哪里”。它通常不需要每次重新读全部日志。但是原始证据或操作回执可能仍有用途，应留在适当存储里，不能随摘要一起误删。

## 2. 压缩前后究竟发生什么

```text
旧模型输入：稳定指令 + 工具说明 + U1/A1/R1/.../U2/A2/R2
                          ↓ 选取需要处理的历史视图
摘要请求：历史视图 + 压缩指令（模型接口另有基础指令）
                          ↓
新模型输入：仍需的稳定指令与工具说明 + 保留的用户意图/摘要/近期项/附件
```

这是生命周期示意，不是两产品完全相同的消息数组。压缩关键不只是生成摘要，还包括**选择输入、检查结果、安装替代历史、补回仍需信息、重新计算预算、继续执行**。把摘要追加在旧历史后面并没有减少输入；只留下摘要则可能丢掉工具关联、当前约束或必要环境信息。

“System Prompt是不是绝对不参与压缩？”不能只答是或否：要区分**被替换的历史**与**摘要模型收到的完整请求**。基础指令通常仍独立提供，不应依赖有损摘要保存授权规则；但上下文中可能存在developer消息、CLAUDE.md合成用户消息及系统提醒，摘要模型可能看见它们。下面分别给出实际路径。

## 3. Codex：本地压缩的完整落地点

<details>
<summary>固定源码：触发判定 → 摘要请求 → 替代历史 → 后续调用</summary>

**触发。** `session/turn.rs`在正常推理前检查是否需要自动压缩，推理后若仍需继续工具/输入循环，也会结合使用量检查。`session/context_window.rs`区分全窗口计数与扣除前缀的主体预算，还维护完整上下文上限；模型切换等路径有额外判定。因此不能写“Codex永远到90%就压缩”。手动请求另有独立入口。

**分支。** 该固定快照在`run_auto_compact`里按功能配置选择Token Budget管理、供应商支持的远端压缩或本地`compact.rs`。以下完整描述只针对本地摘要路径；远端输出与实现不能从本地提示推断。

**输入和提示。** `compact.rs`复制当前历史视图，加入压缩指令构造模型输入，基础指令单独提供，压缩请求不照搬正常工具执行循环。默认提示来自`codex-rs/prompts/templates/compact/prompt.md`，也允许配置覆盖。原文以“CONTEXT CHECKPOINT COMPACTION”标识这项交接任务。用中文概括，它要求为接替执行的模型写交接摘要，重点是：已做工作与决定、重要约束和偏好、剩余步骤、关键资料与引用，并要求简洁、有组织。它不是要求固定JSON Schema；局部小标题是结构化写作，不等于机器已校验字段。

**结果。** 本地路径提取助手返回的摘要字符串，添加summary prefix，并通过`build_compacted_history`组合选取的真实用户消息与摘要。源码有保留用户消息的预算上限；不能据此声称所有历史逐条不丢，也不能说输出就是原字段状态的无损备份。

**安装。** `replace_compacted_history`更新执行中的历史并记录压缩项，重新计算使用量。前轮/手动压缩使用`DoNotInject`，清掉初始上下文参考，使后续正常轮重新注入；轮中压缩使用`BeforeLastUserMessage`，把初始上下文放到最后真实用户消息之前，让摘要位于规定位置。两种路径不能画成同一个无条件顺序。

**失败。** 摘要请求本身过长时有移除旧项后再试的处理；短暂故障有有限退避。技术上能继续不代表摘要语义完整，仍需要长任务回归。此处没有承诺整个外部世界与替代历史构成原子事务。

</details>

## 4. Claude Code：不能简单记成“固定三层压缩”

<details>
<summary>用户固定快照：消息预算与多种压缩机制如何协作</summary>

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

`compactConversation`执行前置Hook，生成`getCompactPrompt`的摘要请求，调用摘要模型。它会对图片/文档等材料做适用处理，遇到摘要请求过长时可能按API轮组裁剪头部重试。摘要从助手文本提取，并检查空结果和API错误；不是自动得到一个经过Schema验证的恢复对象。

成功后按需恢复近期文件、异步任务、计划文件/规划模式、已调用技能、已发现工具和MCP说明等附件。`buildPostCompactMessages`明确顺序为：**压缩边界标记→摘要消息→需保留消息→附件→Hook结果**。下一次调用仍按第09章路径提供systemPrompt/userContext/tools，摘要不承担替代所有系统规则的责任。

</details>

## 5. 到底该保留什么，不是“所有东西都保留”

摘要优先保留会影响**下一步决策**的信息：当前目标、未决约束、已完成步骤、关键证据与待办。可重复获取的大文件只需有可解析引用；临时噪声和已过期猜测可以去掉。高风险动作回执应由程序保存，摘要可以写“操作op7已确认，见回执”，不应保存它的唯一副本。

计划从P1修订为P2时，摘要应说明P2是当前计划及为何受阻，而非把两个计划并列成同等有效事实。压缩后发现原文件变更，需要重新读取；即使摘要完全忠实，它描述的也只是当时信息，不会自动跟随外部世界更新。

## 6. 怎样检验压缩没有把任务压坏

| 检查层次 | 文件报告中的检查 | 局限 |
|---|---|---|
| 结构 | 当前目标、未决项、引用能找到 | 字段存在不保证含义正确 |
| 语义 | “不修改原件”没有被改成“允许修改” | 需要规则、人工或校准评审 |
| 继续执行 | 压缩后仍去补缺失证据，不重复已完成写入 | 模型存在随机性，不能要求逐字相同 |
| 回归 | 固定任务集对比成功率、漏约束、成本与时延 | 测试覆盖仍有限 |

通用工程建议是先构造候选、验证，再安装新的活动视图，并保留适当回退依据。它不意味着两个产品都恰好实现同一套“五步事务”。压缩失败时应明确失败、缩减可重取材料或等待处理，不可直接把唯一历史删掉。

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. Compaction完整流程是什么？

<details>
<summary>参考答案</summary>

先根据预算、阶段或人工请求触发，选择历史视图并生成交接摘要，保留当前目标、约束、未决工作及必要引用，再构造替代历史、补回初始上下文或附件，重新计算预算并继续。压缩是管理模型输入，不是业务状态备份。需要对语义和继续执行效果做回归。

</details>

### 2. Codex压缩提示是什么，输出是否JSON？

<details>
<summary>参考答案</summary>

固定本地路径使用prompts/templates/compact/prompt.md，要求面向接替模型总结进度、决定、约束、剩余步骤和关键资料，支持配置覆盖。它是有组织的自然语言摘要提示，不是JSON Schema保证；程序把摘要文本与选取的用户消息组合为替代历史。远端压缩路径不能从这段提示推断。

</details>

### 3. Claude Code有几层压缩，何时触发？

<details>
<summary>参考答案</summary>

固定快照有工具结果预算、微压缩、可选历史裁剪/局部折叠、自动/手动摘要以及可选超长补救路径，不是所有用户固定启用三层。普通自动判定用有效窗口减余量，且受模型、环境和特性开关影响；完整摘要后重建边界、摘要、保留消息、附件与Hook结果。

</details>

### 4. System Prompt是否会被压缩掉？

<details>
<summary>参考答案</summary>

应区分被替换的历史与摘要模型实际看见的请求。基础指令往往单独提供并在正常调用保留或重注入；历史中仍可能含开发者上下文或合成系统提醒。不能笼统说只压user/tool或system永远不进摘要输入；必须按对应产品路径说明。

</details>

### 5. 怎么防止摘要丢掉关键约束？

<details>
<summary>参考答案</summary>

关键授权和操作回执不能只存在有损摘要中，程序独立保存必要状态。摘要检查目标、约束和待办，引用必须可解析；再做压缩前后继续执行和长任务回归。文字通顺和Token变少都不是正确性的充分证据。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| Resume就是摘要 | Resume是恢复执行，Summary才是摘要。 |
| 压缩就是摘要加到历史尾部 | 必须构造更短替代视图，否则仍然占原预算。 |
| Claude固定三层所有版本一样 | 多种路径受快照和特性开关控制。 |
| 压缩Prompt要求structured所以一定JSON | 有组织文本与机器Schema是两回事。 |
| 摘要中保存回执足够防重复 | 恢复应依赖可靠操作记录与外部核对。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：模型还没到窗口上限，为什么可能提前压缩？

<details>
<summary>查看参考答案</summary>

要为输出、接下来工具结果和摘要请求预留空间；模型切换或任务阶段也可能触发。等硬上限才行动可能连摘要请求都发不出去。

</details>

### 自测 2：压缩后最老计划仍说读B，但B已被禁止，怎么检查？

<details>
<summary>查看参考答案</summary>

对照当前约束与计划主视图，检查摘要是否保留最新约束；执行权限仍应阻止B。不能用旧摘要覆盖真实授权。

</details>

### 自测 3：本地Codex摘要结构清楚，能当检查点直接恢复吗？

<details>
<summary>查看参考答案</summary>

不够。它主要支撑后续推理，活动操作、回执和环境状态有独立语义；自然语言摘要不保证外部写入一次且仅一次。

</details>

### 自测 4：系统规则没在历史里，摘要模型能不能看到它？

<details>
<summary>查看参考答案</summary>

可能通过API独立基础指令字段看到。历史数组范围和完整API请求不是同一个集合，要看具体代码。

</details>

### 自测 5：压缩前后回答不逐字一样，是否压缩失败？

<details>
<summary>查看参考答案</summary>

不能据此判断。模型本身存在随机性，应比较关键约束、任务结果、重复动作和证据质量等，而不是逐字一致。

</details>

### 自测 6：session-memory compaction是不是把会话永久写入长期记忆？

<details>
<summary>查看参考答案</summary>

不是由名称就能得出。它在固定Claude快照中是一条帮助缩减当前会话的可选压缩路径；跨任务auto memory有自己的保存和读取过程。

</details>

## 资料与下一步

固定源码：[codex-rs/core/src/compact.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/compact.rs)、[codex-rs/core/src/session/context_window.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/context_window.rs)、[codex-rs/core/src/session/turn.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/turn.rs)、[codex-rs/prompts/templates/compact/prompt.md](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/prompts/templates/compact/prompt.md)；[query.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)、[services/compact/autoCompact.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/autoCompact.ts)、[services/compact/compact.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/compact.ts)、[services/compact/microCompact.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/compact/microCompact.ts)。完整提示请通过源文件查阅，本章解释用途，不把私有快照提示全文复制为通用规范。

本章对应研究能力：`AGENT-009`、`AGENT-010`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](09-ContextAssemblyBudget.md) · [模块目录](../README.md) · [下一章 →](11-MemoryArchitectureLifecycle.md)
