# 17. 意图、模型与能力路由：把请求交给合适的对象

[← 上一章](16-MCPSkillsHooks.md) · [模块目录](../README.md) · [下一章 →](18-MultiAgentA2AWorkspace.md)

> 本章要解决：先分清“选哪条业务流程”“选哪个模型”“选哪个工具”，再谈降级与容错。

## 1. Router不是一块包办所有选择的魔法模块

Router（路由器）根据输入和约束选择去向。文件报告任务中，入口可能先判断这是报告还是闲聊；报告流程内部选择能处理相应长度与工具调用的模型；模型再选择文件工具，程序映射到实际处理器。三个位置都可以叫路由，但输入与结果不同。

| 路由 | 选择对象 | 主要依据 | 错误例子 |
|---|---|---|---|
| Intent routing（意图路由） | 业务流程/角色 | 用户意图、身份、范围 | 普通查询进了写入流程 |
| Model routing（模型路由） | 模型/供应商 | 能力、质量、延迟、成本、可用性 | 换到不支持工具格式的模型 |
| Capability routing（能力路由） | 工具/服务处理器 | 名称、Schema、权限、环境 | 同名工具指向错误租户 |

工具发现与具体dispatch已在第05章讲透，本章重点是上层选择与模型兼容，避免重新列全部工具失败流程。

## 2. 意图识别先从简单可验证方案开始

固定命令可以用规则，稳定标签且有训练数据可用小分类器，开放语言任务可比较LLM分类或工具自主选择。并不是越大模型越正确：明确的`/report`命令没必要再用昂贵模型猜。

低置信度的正确动作可能是澄清，而不是随机选一个。标注样本要含未知意图和高风险边界；混淆矩阵及每类召回比单一accuracy更能解释问题。把闲聊错分为问答与错分为付款的代价不同，要看下游影响。

## 3. 模型路由先满足能力，再优化成本

Capability compatibility（能力兼容）包括工具调用格式、结构化输出、图片/文件、上下文限制和所需推理能力。先剔除不满足硬约束的候选，再比较任务质量、时延和费用。Provider adapter（供应商适配器）统一请求/响应边界，但不能假装所有差异都不存在。

例如模型A返回一组工具调用，模型B只支持文本。把同一消息原样发B不叫可靠降级，应转换到经过验证的可用流程或显式失败；不能静默把关键功能丢掉后仍宣称任务成功。模型版本变更需要代表任务回归，但不必把全部Schema每条日志复制一次，可记录所用配置引用。

## 4. Retry、Circuit Breaker、Fallback如何配合

Retry（重试）针对有资格重试的短暂错误；Circuit breaker（熔断）在持续失败时暂时减少对故障依赖的调用；Fallback（后备方案）换一个可接受的路径。这些通用算法归AI Backend，本章关心它们对Agent语义的影响。

```text
一次模型请求失败
→ 判断是限流/临时网络还是参数/能力错误
→ 在总Deadline内有限重试，避免多层放大
→ 可用后备模型须满足当前能力与输入限制
→ 保留已经发生的工具动作，不从任务起点重跑
→ 记录降级及质量影响，无法满足要求则明确停止
```

熔断不是遇到一次失败就永久禁用，后备也不是无限嵌套供应商。重试预算、健康恢复探测和降级质量都应可观察，但执行过的写操作必须回到第13章核对。

<details>
<summary>实际产品中的选项与边界</summary>

Claude Code用户快照QueryEngine配置包含fallbackModel，`query.ts`在流式fallback时处理旧尝试留下的助手项与工具结果，避免把孤立结果混进新尝试。这个实现提醒我们：模型切换不仅改名字，还涉及历史关联与已经执行的工作；不能从配置字段推断所有业务动作都能安全重跑。

Codex固定`build_prompt`取当前模型/步骤设置与工具Router，`context_window.rs`按模型预算判断，模型变化时上下文处理可能不同。App Server与模型提供者适配层具有各自接口，不是“所有模型返回文本就能直接互换”。具体默认路由规则以产品配置和源码分支为准。

</details>

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. Agent路由至少分哪几类？

<details>
<summary>参考答案</summary>

入口意图路由选择业务流程，模型路由选择满足能力与质量约束的模型，能力路由把请求分发到工具处理器。它们输入、输出和风险不同，应分别评估，不用一个LLM分类节点包办所有责任。

</details>

### 2. Provider失败怎样Fallback？

<details>
<summary>参考答案</summary>

先分类错误并限制重试和总时限，选择满足工具、上下文和输出契约的后备，保留现有历史与已执行动作。不能只换model name，也不能重跑整个任务。降级需可见并用回归任务确认质量边界。

</details>

### 3. 如何评估Router？

<details>
<summary>参考答案</summary>

对意图用标注集、混淆矩阵、未知意图/澄清率及风险加权下游影响；对模型用代表性任务质量、能力兼容、延迟、费用和失败率；对工具路由检查处理器、权限和版本正确性。

</details>

### 4. 为什么Adapter不应抹平全部供应商差异？

<details>
<summary>参考答案</summary>

真正不支持的能力不能被包装成支持。适配器应统一能统一的结构，同时显式暴露限制和错误，让上层选择可用路径，否则静默降级会破坏任务语义。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| Router一律用最大LLM | 先规则与简单基线，有复杂语言需求再比较模型。 |
| Fallback只是换模型名 | 上下文和能力契约可能不兼容。 |
| 模型错误就重启整个Agent | 会重复已完成工具和副作用。 |
| 总体分类准确率高就够 | 高风险类别误路由与未知意图也需验证。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：明确/report命令是否需要LLM路由？

<details>
<summary>查看参考答案</summary>

通常规则更直接稳定。只有命令内部仍有语义不确定性时才需要进一步模型判断。

</details>

### 自测 2：A支持工具，B不支持，B更便宜是否就可做后备？

<details>
<summary>查看参考答案</summary>

不能直接替换。硬能力不满足，需经过验证的替代流程或明确失败。

</details>

### 自测 3：模型调用超时，之前已发送邮件，能重跑整段吗？

<details>
<summary>查看参考答案</summary>

不能。之前的写入是独立事实，应保留并核对；恢复当前模型请求与重做所有任务不是一回事。

</details>

### 自测 4：熔断和权限拒绝可以同样自动恢复吗？

<details>
<summary>查看参考答案</summary>

不同。熔断针对依赖健康可探测恢复；权限拒绝需授权依据变化，不能靠重试绕过。

</details>

### 自测 5：路由低置信度为什么允许澄清？

<details>
<summary>查看参考答案</summary>

澄清可以降低错误动作风险，未知请求不应被强行塞入已知流程。需要把澄清成本与误路由代价一起评估。

</details>

### 自测 6：模型升级后只跑一个正常例子够吗？

<details>
<summary>查看参考答案</summary>

不够，应覆盖工具格式、长上下文、结构化输出、错误和代表领域任务；升级可能改变质量与恢复边界。

</details>

## 资料与下一步

官方：[OpenAI Agents SDK Models](https://openai.github.io/openai-agents-python/models/)、[LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)。固定源码：[query.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)、[codex-rs/core/src/session/turn.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/turn.rs)、[codex-rs/core/src/session/context_window.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/context_window.rs)。下一章把执行从一个Agent扩展到协作。

本章对应研究能力：`AGENT-032`、`AGENT-038`、`AGENT-045`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](16-MCPSkillsHooks.md) · [模块目录](../README.md) · [下一章 →](18-MultiAgentA2AWorkspace.md)
