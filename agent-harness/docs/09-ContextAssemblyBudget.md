# 09. 上下文编排：模型这一刻到底收到什么

[← 上一章](08-PlanningGoalStopBudget.md) · [模块目录](../README.md) · [下一章 →](10-ContextCompactionCorrectness.md)

> 本章要解决：把真实消息顺序、计划更新、工具说明与前缀缓存放到同一条时间线上。

## 1. 上下文不是一个自动知道所有事情的脑袋

Context（上下文）是一次模型请求可用的输入。程序即使在数据库里保存了一万条记录，只要这次没有把相关内容或可用读取方式提供给模型，模型就不会因此自动知道它。上下文编排就是**从已有信息里选择本次需要的部分，并编码成模型接口支持的请求**。

信息来源与发送位置是两个问题。用户资料、计划、工具结果是来源；`instructions/system`、`messages/input`、`tools`是不同API的载体，不能强行合成所有产品通用的八段字符串。工具说明可能独立放在`tools`参数，却仍占模型处理预算；只统计聊天文本不够。

## 2. 用连续三次请求看清追加与编排

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

### 自己验证“追加不等于覆盖”

下面只验证消息列表关系，不测试任何供应商的真实缓存，也不表示所有API按这组字段接收数据。

```python
# runnable-example: append_and_plan_view
from copy import deepcopy
history = [{"role": "user", "content": "报告任务"}]
history += [{"type": "plan_call", "plan": ["读A", "读B"]}, {"type": "plan_result", "ok": True}]
prefix = deepcopy(history)
current_plan = ["A已读", "B待确认"]
history += [{"type": "plan_call", "plan": deepcopy(current_plan)}, {"type": "plan_result", "ok": True}]
assert history[:len(prefix)] == prefix
assert history[1]["plan"] == ["读A", "读B"]
assert history[-2]["plan"] == ["A已读", "B待确认"]
# 当前视图变化不意味着旧消息被原地修改。
current_plan[1] = "B已获授权，待读取"
assert history[-2]["plan"][1] == "B待确认"
```

新的状态变化若要让模型知道，仍需在后续请求中显式提供，例如追加一条更新；程序变量变化不会通过魔法改变已经发送过的请求。

## 3. 缓存到底复用了什么

Prompt cache（提示前缀缓存）通常复用重复输入前缀的部分计算，不是返回以前的最终答案。向尾部追加消息有利于保留相同前缀，但不是缓存命中的充分条件：模型、缓存有效期、工具序列化、系统指令以及服务端路由均可能影响复用。

不要为了省缓存而让过期事实继续占据权威位置。原文件变更后，追加“刚才A版本已失效，这是重新读取的结果”，比偷偷改写历史既更可解释，也更适合复用此前不变部分。真正必要的指令修改或压缩仍会改变前缀，要在正确性和成本之间明确取舍。

| 容易混淆的缓存 | 保存或复用什么 | 不能保证什么 |
|---|---|---|
| 模型前缀缓存 | 相同前缀的计算 | 不保证回答正确，也不保存业务状态 |
| 宿主工具Schema缓存 | 同一说明的稳定序列化结果 | 不等于工具权限永久有效 |
| 应用回答/检索缓存 | 某请求结果 | 要自行定义权限、时效与失效条件 |

## 4. 为什么需要选择、预算与外部化

“读取日志”可能返回几万行，但模型当前只需错误所在片段。Offloading（外部化）是把完整结果存到可读取位置，在上下文留摘要、定位与必要片段；Truncation（截断）是裁掉内容，两者不等价。可重新读取也有权限和保留期限，引用失效会使后续调查受阻。

预算要在**实际请求**上检查。假设窗口128k，示意输入上限100k、输出预留20k、安全余量8k；100k输入再分给工具说明、指令、历史和证据。分类软预算可以调整，但最终总量必须满足限制。为分类列数字不是目的，目的是说明超额时先删重复说明、缩减无关证据、外部化大结果，再决定压缩，而不是碰运气塞满。

去重可按来源ID或内容摘要完成；选择还要检查权限、适用范围和新鲜度。不要把来自文件的指令性句子提升为System规则；相关性高不等于可信度高。

## 5. Codex 的真实请求怎样形成

<details>
<summary>固定源码路径：初始上下文、消息追加、工具说明、计划更新与压缩后重建</summary>

依据固定Codex的`session/mod.rs`和`session/turn.rs`，可以沿以下顺序理解，**不是声称所有开关都输出同一串文字**：

1. `build_initial_context_with_world_state`收集开发者指令、扩展提供的线程/当前轮信息和环境状态。按片段角色聚合，普通路径先形成开发者消息，再放需要单独保留的开发者片段和模式信息，然后形成上下文用户消息。Guardian等分支另有独立指令位置。
2. 初次进入或压缩后的新上下文窗口需要完整注入；日常执行通过上下文更新与参考状态生成必要变化，不应每步无条件重建全部前缀。
3. 用户输入、模型输出、函数调用与函数结果进入执行历史。`build_prompt`把历史投影作为`input`，工具来自`tool_router.model_visible_specs()`，`base_instructions`另行传入，输出约束也独立。最终API序列化还在供应商适配层。
4. `update_plan`调用参数本身写明计划，处理器发出`PlanUpdate`事件，回填确认；新计划更新继续走调用/结果链，不要求每次移到最前面。
5. 压缩会换一个历史视图。前轮/手动路径与当前轮中压缩的初始信息重注入不同，下一章给出完整过程。

你可以据此描述一条实在的链：**初始上下文与环境信息→追加用户/模型/工具项→选当前可见工具说明→独立基础指令→模型请求**。这比“系统、计划、记忆总是固定按某八个位置摆放”更接近该快照。

</details>

## 6. Claude Code 的真实请求怎样形成

<details>
<summary>用户提供的固定源码路径：query.ts → utils/api.ts → 模型适配</summary>

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

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. Agent上下文怎样编排？

<details>
<summary>参考答案</summary>

先区分来源与API载体：稳定指令、用户目标、选定历史、证据和工具结果形成本次消息视图，工具Schema与基础指令可能独立传入。日常保持历史次序并追加变化，权限/新鲜度检查和总预算先于发送；大结果外部化，超限才按策略压缩。不能把编排理解为每轮重新排序整个对话。

</details>

### 2. 新的计划和修订计划放在哪里？

<details>
<summary>参考答案</summary>

可以作为新的模型说明或工具调用追加到历史，同时更新宿主当前计划视图。Codex update_plan提交清单并发事件、回确认；Claude TodoWrite也区分当前清单和历史记录。压缩后当前计划可由摘要或附件恢复，具体以产品路径为准，不应假设它总在System Prompt。

</details>

### 3. 为什么一直追加也不意味着永远命中Prompt Cache？

<details>
<summary>参考答案</summary>

追加只保留了部分输入前缀。工具说明、系统指令、模型、缓存有效期或服务端路由改变仍会影响命中。缓存复用的是计算而不是业务事实，必要的权限和内容更新不能为了缓存被忽略。

</details>

### 4. 工具结果很大时怎么处理？

<details>
<summary>参考答案</summary>

保存必要完整结果到有权限和保留策略的产物存储，模型只收到摘要、来源和相关片段，后续按需重读；可丢弃噪声才直接截断。接着检查输入总预算，而不是把所有日志反复附加或让摘要成为唯一证据。

</details>

### 5. Codex和Claude的编排顺序是一套吗？

<details>
<summary>参考答案</summary>

不是。Codex快照把初始环境/开发者上下文与历史input组织起来，并独立传基础指令和可见工具。Claude快照明确分systemPrompt、userContext、systemContext和messages，在query中处理消息视图，再前置合成userContext。共同原则是区分稳定配置、增量消息与宿主状态，不是统一固定八段模板。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| 编排就是每轮重排历史 | 编排可以仅做稳定投影与尾部追加。 |
| tools不在messages所以不占预算 | 模型使用的工具说明同样需要处理。 |
| 当前Plan被覆盖，历史Plan也应覆盖 | 当前视图与历史轨迹不同。 |
| 摘要能替代所有恢复数据 | 它可能有损，权威回执与必要状态另存。 |
| 保存全文到Trace就实现外部化 | 外部化需要可授权读取的产物；诊断日志不是默认产物库。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：已有P/T/U/A/R，用户补了一句话，通常如何构造下次请求？

<details>
<summary>查看参考答案</summary>

保持已有协议项次序，把新用户输入按控制语义加入尾部或下一轮。稳定P/T尽量复用；若用户修改约束则程序先更新控制状态，不能只是为了缓存忽略它。

</details>

### 自测 2：模型调用update_plan后只收到“已更新”，它为何仍知道计划？

<details>
<summary>查看参考答案</summary>

调用参数已经包含计划，模型自身输出和工具调用仍在历史；短确认减少重复。程序清单用于界面和执行管理，是另一个视图。

</details>

### 自测 3：128k窗口可以输入128k再期待20k输出吗？

<details>
<summary>查看参考答案</summary>

不能。需按接口的上下文/输出限制预留输出和余量，并核算工具等全部输入。分类软预算不替代最终总量检查。

</details>

### 自测 4：缓存命中率很高，但Agent使用了旧文件，是优化成功吗？

<details>
<summary>查看参考答案</summary>

不是。计算复用和事实新鲜度是两项指标，应重新读取变化文件并让当前决策使用正确版本。正确性优先于缓存率。

</details>

### 自测 5：为什么保留整个历史，但发送时只取压缩边界后消息不矛盾？

<details>
<summary>查看参考答案</summary>

持久记录用于回看，发送视图只管理本次模型输入。存储与上下文是两个生命周期，保存不等于全部注入。

</details>

### 自测 6：两产品折叠案例为何不写一份绝对固定的完整系统提示？

<details>
<summary>查看参考答案</summary>

固定源码会按模型、模式、插件与特性分支形成不同内容。本章给出实际函数与组装顺序，不能把某一配置的文本误称所有用户都收到的统一提示。

</details>

## 资料与下一步

固定源码：[codex-rs/core/src/session/mod.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/mod.rs)、[codex-rs/core/src/session/turn.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/turn.rs)、[codex-rs/core/src/tools/handlers/plan.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/tools/handlers/plan.rs)；[query.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)、[utils/api.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/api.ts)、[tools/TodoWriteTool/TodoWriteTool.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/TodoWriteTool/TodoWriteTool.ts)。下一章从这条时间线进入压缩前后。

本章对应研究能力：`AGENT-008`、`AGENT-011`、`AGENT-012`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](08-PlanningGoalStopBudget.md) · [模块目录](../README.md) · [下一章 →](10-ContextCompactionCorrectness.md)
