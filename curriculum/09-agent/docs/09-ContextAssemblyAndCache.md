# 09. Context Assembly：上下文编排、缓存与结果外部化

Agent Runtime（运行时执行系统） 每次调用模型前都要回答一个问题：

> **这一次模型到底应该看到什么？**

这就是 Context Assembly。

如果把它理解成：

```text
System Prompt
+ 全部 Chat History
```

会很快在 Production（生产环境） 里遇到：

- Context Window 爆满；
- 旧信息污染当前任务；
- Tool Result 巨大；
- 权限和 Tenant（租户） 信息混入错误请求；
- Prompt Cache 命中率差；
- Context 成本不可控；
- 同一事实被重复注入。

所以成熟 Harness 的 Context 不是“聊天记录”，而是：

> **Runtime 为当前 Model Call 编译出来的一次性输入视图。**

[← 上一章](08-PlanningGoalAndControl.md) · [Agent 目录](../README.md) · [下一章 →](10-CompactionAndContinuation.md)

---

<a id="section-1"></a>

## 1. Context、Memory、State、History 先分清

<a id="legacy-09-01"></a>

Context（上下文）是一次模型请求可用的输入。程序即使在数据库里保存了一万条记录，只要这次没有把相关内容或可用读取方式提供给模型，模型就不会因此自动知道它。上下文编排就是**从已有信息里选择本次需要的部分，并编码成模型接口支持的请求**。

信息来源与发送位置是两个问题。用户资料、计划、工具结果是来源；`instructions/system`、`messages/input`、`tools`是不同API的载体，不能强行合成所有产品通用的八段字符串。工具说明可能独立放在`tools`参数，却仍占模型处理预算；只统计聊天文本不够。

```text
Context
= 当前这一次模型调用真正看见的内容

Memory
= 可以在未来被再次取回的信息

State
= 程序用于决定下一步的当前工作情况，如进度、等待、预算和动作结果

History
= 已经发生过的 message / event 记录
```

因此：

```text
History 很长
≠ Context 必须全部包含 History

Memory 存在
≠ 每次都注入全部 Memory

State 持久化
≠ 全部 State 都应该变成自然语言 Prompt
```

Context Assembly 的本质就是：

```text
从多种来源中选择
→ 排序
→ 去重
→ 裁剪
→ 编译成模型可消费输入
```

---

<a id="section-2"></a>

## 2. 一次 Agent Context 可能来自哪些 Source

<a id="legacy-09-02"></a>

常见来源：

```text
System / Runtime Instructions
User Request
Recent Conversation History
Current Goal / Plan / Constraints
Working State
Relevant Memory
RAG Evidence
Tool Schema
Loaded Skills / MCP Capability
Tool Result
Workspace / File Snapshot
Permission / Environment Metadata
```

但这些来源的优先级、稳定性和预算完全不同。

可以粗分：

```text
Stable Prefix
Dynamic Task Context
Ephemeral Observation
External Artifact Reference
```

---

<a id="section-3"></a>

## 3. Context Assembly 应该是“Compiler”，不是字符串拼接

<a id="legacy-09-03"></a>

推荐把每类输入建模成结构化单元：

```python
# 上下文条目示意：来源与成本用于选择；版本/失效时间只在需要复核时使用。
from dataclasses import dataclass

@dataclass
class ContextItem:
    kind: str
    content: str
    priority: int
    token_cost: int
    source_id: str
    version: str | None
    expires_at: float | None
```

然后：

```text
collect sources
→ normalize
→ permission filter
→ deduplicate
→ score priority
→ enforce budget
→ render provider-specific messages
```

这样 Runtime 才能回答：

```text
为什么这段内容被放进去？
为什么另一段被丢掉？
它来自哪个版本？
它什么时候过期？
```

---

<a id="section-4"></a>

## 4. 编排顺序、追加历史与计划更新怎样配合

<a id="legacy-09-04"></a>

以下是教学示意，角色名随API变化。P是相对稳定指令，T是当前允许的工具说明，U是用户消息，A是模型消息，R是工具结果。

```text
请求1：P + T + [U1：读取A/B并整理报告]
返回A1：update_plan(先读A、再读B、最后汇总)
宿主执行并追加R1：计划已更新

请求2：P + T + [U1, A1, R1]
返回A2：read_file(A)
宿主执行并追加R2：A的内容与来源

请求3：P + T + [U1, A1, R1, A2, R2]
返回A3：update_plan(A已完成、B受阻需澄清)
```

旧历史不一定每次都存成一份新副本，但API最终必须得到符合协议的视图。**“每次编排”不等于“每次重新排序所有旧消息”。** 可以保留稳定前缀与已有次序，只追加新观察和变化说明。消息调用与结果要保持关联，不能为了把最新计划放前面，随意拆散工具请求/结果。

用户下一次发U2及新计划P2，通常也是尾部新增。若旧计划已结束，它仍可存在历史中，但程序当前计划视图必须清楚指向新任务。上下文压缩后，旧过程会变成摘要，当前目标和计划按实现保留或重新载入。读者应该能分别指出“当前程序状态在哪里”“模型在这次请求如何得知它”。



信息优先级与API物理位置是两回事。不要为把最新计划移到最前面而拆散旧工具调用和结果；当前计划视图变化，通常可以由新增调用、结果或明确的更新告知模型。

---

<a id="section-5"></a>

## 5. Token Budget 要分区，而不是统一“还剩多少”

<a id="legacy-09-05"></a>

假设 Model Context = 128k。

不能简单：

```text
把东西一直塞到 128k
```

因为还要为输出、Tool Result、后续 Turn 和 Compaction（上下文压缩） 留空间。

可以按类别设置软预算：

```text
Instructions       8k
Goal / State       6k
Recent History    20k
Memory / RAG      24k
Tool Definitions  14k
Tool Results      28k
---------------------
Input subtotal   100k
Reserve Output    20k
Safety Margin      8k
Total window     128k
```

数字只是示意，真正值要结合模型和任务。

重要思想：

> **不同 Context Source 应有不同 Budget（预算） 和退化策略。**

上表为教学预算：输入100k、输出20k、余量8k，总计128k。数字不是产品推荐默认值。软预算可调整，但最终真实请求必须满足总限制；不能为某类配额挤掉用户关键约束。

---

<a id="section-6"></a>

## 6. Large Tool Result 为什么不能直接塞回 Context

<a id="legacy-09-07"></a>

例如：

```text
cat 5MB log
run test → 30,000 lines
search repository → 5,000 matches
```

如果 Tool Result 原样回填：

```text
Context 爆炸
→ 成本上升
→ Noise 上升
→ Compaction 提前触发
→ 甚至把真正重要状态挤掉
```

更成熟的策略：

```text
Tool produces artifact
        ↓
Runtime persists full result externally
        ↓
Context only keeps:
- summary
- artifact id/path
- metadata
- selected relevant excerpt
```

Claude Code 的 `utils/toolResultStorage.ts` 索引明确用于：

> 持久化 large tool results，而不是不可逆地直接截断。

因此课程抽象是：

```text
Large Result
→ Offload
→ Reference
→ Selective Rehydrate
```

---

<a id="section-7"></a>

## 7. Offloading 和 Truncation 有什么区别

<a id="legacy-09-08"></a>

错误做法：

```text
result[:5000]
```

问题：

```text
后面重要错误被直接丢掉
而且无法恢复
```

更好的做法：

```text
Full Artifact 保存
+ Context 中放摘要 / 索引 / 指针
```

如果后续需要：

```text
read artifact range
search artifact
load relevant section
```

这就是可恢复的 Context Offloading。

---

<a id="section-8"></a>

## 8. Prompt / Context Cache 应该缓存什么

<a id="legacy-09-09"></a>

Prompt cache（提示前缀缓存）通常复用重复输入前缀的部分计算，不是返回以前的最终答案。向尾部追加消息有利于保留相同前缀，但不是缓存命中的充分条件：模型、缓存有效期、工具序列化、系统指令以及服务端路由均可能影响复用。

不要为了省缓存而让过期事实继续占据权威位置。原文件变更后，追加“刚才A版本已失效，这是重新读取的结果”，比偷偷改写历史既更可解释，也更适合复用此前不变部分。真正必要的指令修改或压缩仍会改变前缀，要在正确性和成本之间明确取舍。

| 容易混淆的缓存 | 保存或复用什么 | 不能保证什么 |
|---|---|---|
| 模型前缀缓存 | 相同前缀的计算 | 不保证回答正确，也不保存业务状态 |
| 宿主工具Schema缓存 | 同一说明的稳定序列化结果 | 不等于工具权限永久有效 |
| 应用回答/检索缓存 | 某请求结果 | 要自行定义权限、时效与失效条件 |

必须更新指令或压缩时，可以牺牲部分缓存命中，不能为缓存保留错误事实。

---

<a id="section-9"></a>

## 9. Context Pollution / Stale Context

<a id="legacy-09-10"></a>

一个常见失败不是“Context 不够”，而是：

> **Context 太多，而且包含了已经失效的信息。**

例如：

```text
早期 Plan: 修改 A.py
后面已经决定改 B.py

但旧 Plan 仍然在 Context 中高优先级出现
→ 模型反复回到 A.py
```

或者：

```text
旧 permission
旧 file content
旧 dependency version
旧 tool result
```

因此每个 Context Item 都最好能回答：

```text
Source?
Version?
Freshness?
Still relevant?
```

---

<a id="section-10"></a>

## 10. Context Dedup 为什么重要

<a id="legacy-09-11"></a>

相同信息可能同时存在于：

```text
System Prompt
Memory
RAG
Recent History
Tool Result
```

重复并不是免费：

- 增加 Token；
- 放大某些信息权重；
- 让模型误以为重复事实更重要；
- 降低 Cache 稳定性。

所以 Runtime 可以对：

```text
source_id
content hash
artifact id
memory id
```

做去重。

Claude Code 索引里 `loadedNestedMemoryPaths` 用来避免某些 nested memory 重复注入，也支持这个课程方向。

---

<a id="section-11"></a>

## 11. Context Assembly Failure Timeline

<a id="legacy-09-12"></a>

```text
T0  Tool 返回 100k tokens 日志
T1  Runtime 全量塞进 History
T2  下一轮 Context 接近窗口上限
T3  早期 Goal / Constraint 被裁掉
T4  模型仍看到大量日志噪声
T5  Agent Goal Drift
T6  自动 Compaction 生成不完整摘要
```

根因不是单纯：

```text
Context Window 太小
```

而是：

```text
Assembly / Budget / Offloading 没设计好
```

这里首先是模型收到的信息不合适，要查遗漏、过期、重复或预算裁剪。工具重试和权限检查不能替代上下文质量诊断。

---

<a id="section-12"></a>

## 12. 产品实现与官方资料对照（按需展开）

<details>
<summary>Claude Code 源码提供了什么实现证据</summary>

<a id="legacy-09-06"></a>

固定源码索引里，`QueryEngine.ts` 会加载：

- memory prompt；
- session storage；
- system prompt parts；
- file history；
- plugin / skill 相关状态；
- compact / snip 相关能力。

`ToolUseContext` 还显式维护：

```text
loadedNestedMemoryPaths
tool-result budget
content replacement state
dynamic skill discovery
permission decision
```

这支持一个成熟 Runtime 的稳定抽象：

```text
Context
≠ transcript concatenation

Context
= selected runtime projection
```

这里我们只引用索引已核验的源码事实，不把 Claude Code 的具体排序当成所有 Agent 的通用标准。

### 固定源码路径：初始上下文、消息追加、工具说明、计划更新与压缩后重建

依据固定Codex的`session/mod.rs`和`session/turn.rs`，可以沿以下顺序理解，**不是声称所有开关都输出同一串文字**：

1. `build_initial_context_with_world_state`收集开发者指令、扩展提供的线程/当前轮信息和环境状态。按片段角色聚合，普通路径先形成开发者消息，再放需要单独保留的开发者片段和模式信息，然后形成上下文用户消息。Guardian等分支另有独立指令位置。
2. 初次进入或压缩后的新上下文窗口需要完整注入；日常执行通过上下文更新与参考状态生成必要变化，不应每步无条件重建全部前缀。
3. 用户输入、模型输出、函数调用与函数结果进入执行历史。`build_prompt`把历史投影作为`input`，工具来自`tool_router.model_visible_specs()`，`base_instructions`另行传入，输出约束也独立。最终API序列化还在供应商适配层。
4. `update_plan`调用参数本身写明计划，处理器发出`PlanUpdate`事件，回填确认；新计划更新继续走调用/结果链，不要求每次移到最前面。
5. 压缩会换一个历史视图。前轮/手动路径与当前轮中压缩的初始信息重注入不同，下一章给出完整过程。

你可以据此描述一条实在的链：**初始上下文与环境信息→追加用户/模型/工具项→选当前可见工具说明→独立基础指令→模型请求**。这比“系统、计划、记忆总是固定按某八个位置摆放”更接近该快照。



### 用户提供的固定源码路径：query.ts → utils/api.ts → 模型适配

`query.ts`把`systemPrompt`、`userContext`、`systemContext`与`messages`分开接收。循环内先取最近压缩边界之后的消息，再应用工具结果预算、可选历史裁剪、微压缩、可选局部上下文折叠以及自动压缩。特性开关会改变经过哪些分支。

模型调用前可以直接看到：

```text
systemPrompt = appendSystemContext(systemPrompt, systemContext)
messages = prependUserContext(messagesForQuery, userContext)
tools = toolUseContext.options.tools
signal = toolUseContext.abortController.signal
```

`appendSystemContext`把环境键值块接到系统指令块后；`prependUserContext`在非空时创建一条含`system-reminder`的合成用户消息放到消息列表前面，供CLAUDE.md等上下文使用。模型工具随后经过`toolToAPISchema`投影为API支持字段，宿主的完整Tool对象不会原样进入模型。

因此示意请求是**独立system块、独立tools、合成user-context消息+既有消息视图**，不是所有信息都每次按新优先级重排。`utils/api.ts`还区分系统静态/动态边界；`query.ts`在给界面补充工具字段时刻意复制消息，保留送回API的原始参数字节，以减少无意缓存变化。

TodoWrite更新程序清单并回填确认，清单内容仍能由历史工具调用得知；计划模式文件不是相同对象。`compact.ts`压缩后会按需重新附加当前计划。不能把这些实现简化成“每轮把最新Plan插入固定前缀”。

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[OpenAI前缀缓存](https://developers.openai.com/api/docs/guides/prompt-caching)。

---

<a id="human-a"></a>

## 13. HUMAN-A 信号

本章主要承接：

- `AGENT-008`：Context Assembly；
- `AGENT-011`：Large Tool Result / Offloading；
- `AGENT-012`：Prompt / Context Cache。

其中真人面经已经把 Context 问题追到 L4：不仅问“Context 包含什么”，还会追“顺序、预算、缓存、超限后怎么办”。

---

<a id="interview"></a>

## 14. 面试怎么答

### Q：Agent Context 应该怎么组装？

🎯 **30 秒回答**：

> 我会把 Context 当成 Runtime 为当前 model call 编译出来的 view，而不是把全部聊天历史拼进去。来源通常包括 system/runtime instruction、当前目标与约束、最近 history、相关 memory/RAG、tool schema 和最新 tool result。每类来源设置优先级和 token budget，并记录 source/version/freshness；大 Tool Result 外部化成 artifact，只把摘要和引用放进 Context。这样 Context Assembly 才能做去重、过期控制、缓存和后续 compaction。

### Q：Tool Result 太大怎么办？

🎯 **30 秒回答**：

> 不优先做不可逆截断，而是完整结果持久化到 artifact store，在 Context 里保留摘要、metadata、引用和少量相关片段，后续需要时再按范围或检索 rehydrate。

### Q：Agent上下文怎样编排？

🎯 **30 秒回答**：

> 先区分来源与API载体：稳定指令、用户目标、选定历史、证据和工具结果形成本次消息视图，工具Schema与基础指令可能独立传入。日常保持历史次序并追加变化，权限/新鲜度检查和总预算先于发送；大结果外部化，超限才按策略压缩。不能把编排理解为每轮重新排序整个对话。

### Q：新的计划和修订计划放在哪里？

🎯 **30 秒回答**：

> 可以作为新的模型说明或工具调用追加到历史，同时更新宿主当前计划视图。Codex update_plan提交清单并发事件、回确认；Claude TodoWrite也区分当前清单和历史记录。压缩后当前计划可由摘要或附件恢复，具体以产品路径为准，不应假设它总在System Prompt。

### Q：为什么一直追加也不意味着永远命中Prompt Cache？

🎯 **30 秒回答**：

> 追加只保留了部分输入前缀。工具说明、系统指令、模型、缓存有效期或服务端路由改变仍会影响命中。缓存复用的是计算而不是业务事实，必要的权限和内容更新不能为了缓存被忽略。

### Q：工具结果很大时怎么处理？

🎯 **30 秒回答**：

> 保存必要完整结果到有权限和保留策略的产物存储，模型只收到摘要、来源和相关片段，后续按需重读；可丢弃噪声才直接截断。接着检查输入总预算，而不是把所有日志反复附加或让摘要成为唯一证据。

### Q：Codex和Claude的编排顺序是一套吗？

🎯 **30 秒回答**：

> 不是。Codex快照把初始环境/开发者上下文与历史input组织起来，并独立传基础指令和可见工具。Claude快照明确分systemPrompt、userContext、systemContext和messages，在query中处理消息视图，再前置合成userContext。共同原则是区分稳定配置、增量消息与宿主状态，不是统一固定八段模板。

---

<a id="pitfalls"></a>

## 15. 高频易错点

⚠️ **Context = History（历史记录）。** 错，History 只是 Context Source 之一。

⚠️ **Context Window 有 1M，就可以全塞。** 成本、噪声、位置利用和 stale 信息仍然存在。

⚠️ **Tool Result 太大就截前 5k。** 可能不可逆丢失关键证据。

⚠️ **Prompt Cache 只看文本 hash。** 还要考虑模型、工具、策略、Tenant 等版本边界。

⚠️ **编排就是每轮重排历史。** 编排可以仅做稳定投影与尾部追加。

⚠️ **tools不在messages所以不占预算。** 模型使用的工具说明同样需要处理。

⚠️ **当前Plan被覆盖，历史Plan也应覆盖。** 当前视图与历史轨迹不同。

⚠️ **摘要能替代所有恢复数据。** 它可能有损，权威回执与必要状态另存。

⚠️ **保存全文到Trace（执行追踪）就实现外部化。** 外部化需要可授权读取的产物；诊断日志不是默认产物库。

---

<a id="self-test"></a>

## 16. 本章自测

<details><summary>1. 为什么 Context 应该被看作 compiled view？</summary>

因为 Runtime 需要从 instruction、history、memory、retrieval、tool、state 等不同来源中选择、排序、去重和预算，最终只生成当前调用需要的输入。

</details>

<details><summary>2. Context Offloading 和 Truncation 有什么区别？</summary>

Offloading 保留完整 artifact，只在 Context 中放摘要/引用，因此可以重新加载；Truncation 直接丢内容，通常不可恢复。

</details>

<details><summary>3. 为什么 Context Cache 需要版本信息？</summary>

因为 instruction、tool schema、policy、provider 都可能变化；没有版本边界会让旧 Prefix 在新运行中被错误复用。

</details>

<details><summary>4. 已有P/T/U/A/R，用户补了一句话，通常如何构造下次请求？</summary>

保持已有协议项次序，把新用户输入按控制语义加入尾部或下一轮。稳定P/T尽量复用；若用户修改约束则程序先更新控制状态，不能只是为了缓存忽略它。

</details>

<details><summary>5. 模型调用update_plan后只收到“已更新”，它为何仍知道计划？</summary>

调用参数已经包含计划，模型自身输出和工具调用仍在历史；短确认减少重复。程序清单用于界面和执行管理，是另一个视图。

</details>

<details><summary>6. 128k窗口可以输入128k再期待20k输出吗？</summary>

不能。需按接口的上下文/输出限制预留输出和余量，并核算工具等全部输入。分类软预算不替代最终总量检查。

</details>

<details><summary>7. 缓存命中率很高，但Agent使用了旧文件，是优化成功吗？</summary>

不是。计算复用和事实新鲜度是两项指标，应重新读取变化文件并让当前决策使用正确版本。正确性优先于缓存率。

</details>

<details><summary>8. 为什么保留整个历史，但发送时只取压缩边界后消息不矛盾？</summary>

持久记录用于回看，发送视图只管理本次模型输入。存储与上下文是两个生命周期，保存不等于全部注入。

</details>

<details><summary>9. 两产品折叠案例为何不写一份绝对固定的完整系统提示？</summary>

固定源码会按模型、模式、插件与特性分支形成不同内容。本章给出实际函数与组装顺序，不能把某一配置的文本误称所有用户都收到的统一提示。

</details>

---

[← 上一章](08-PlanningGoalAndControl.md) · [Agent 目录](../README.md) · [下一章 →](10-CompactionAndContinuation.md)
