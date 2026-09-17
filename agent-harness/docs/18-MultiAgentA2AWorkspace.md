# 18. 多Agent与A2A：分工、交接和跨系统任务

[← 上一章](17-RoutingProviderResilience.md) · [模块目录](../README.md) · [下一章 →](19-TraceReplayObservability.md)

> 本章要解决：什么时候确实需要协作？A2A如何发现、发起任务、取结果，而不只是“Agent互发消息”？

## 1. 多Agent首先增加了什么责任

一个Agent读文件并汇总，已有上下文、工具和停止规则。拆成两个后，还要决定谁读哪些资料、传多少上下文、谁能写共享文件、谁汇总、一个失败怎么办，以及总成本由谁负责。Multi-Agent（多智能体）不是必然升级，而是增加分工价值与协调成本的选择。

适合拆分的证据是子目标相对独立、上下文可隔离、可以并行、结果可验证。高度依赖同一工作区且反复互等的任务，单Agent或确定性并行工具可能更简单。

## 2. 三种协作关系，用控制权区分

| 关系 | 谁持有最终控制权 | 结果如何回来 |
|---|---|---|
| Agent-as-Tool（作为工具的子Agent） | 父Agent | 子任务返回结果，父继续 |
| Handoff（交接） | 接手Agent成为当前执行角色 | 对话/任务控制转给另一角色 |
| Manager/Worker（管理者/工作者） | 管理者协调任务 | 多个Worker提交证据，由管理者验收 |

名称会被框架实现映射。比如OpenAI Agents SDK的handoff是Runner中的控制转移，不自动意味着跨网络A2A；把另一个Agent包装成工具则保留调用者继续处理的控制流。不能只因它们都“调用另一个Agent”就认为一样。

## 3. 先定义子任务交接契约

报告中的Agent A负责资料事实，Agent B检查引用。父级应交给B目标、允许读取范围、待检查报告引用、预算及输出约定，而不是把自己的所有历史和凭证复制过去。B返回“哪条引用缺失、来源位置、检查范围”，比完整transcript更容易被父级验证。

Task ownership（任务所有权）回答谁负责推进哪个任务；Workspace ownership（工作区所有权）回答谁有权改哪个资源。两个上下文分开不会自动避免同时写同一文件。先单写者或独立工作区，确需并发时再加入锁、基线检查和合并验证。

父级取消要传给仍属于该任务的子工作，子任务超时不一定让父任务失败；可部分汇聚或请求补充，但必须披露缺口。递归委派需限制深度、总预算与相互等待，防止A等B、B又等A。

## 4. A2A的官方问题域

A2A（Agent2Agent，智能体间互操作协议）用于独立Agent系统之间协作，让调用方不用了解对方内部Prompt、工具和框架，也能发现能力、交换消息、跟踪任务与获取产物。本节按**核验时官方1.0规范**解释，0.3的接口名字不能不标版本直接混用。

A2A不是多Agent的唯一通信方式。一个进程中的子Agent可以用函数、队列或框架私有对象；独立组织和异构系统才更需要共同协议。

| 对象 | 含义 | 报告任务例子 |
|---|---|---|
| Agent Card（能力卡片） | 能做什么、支持哪些接口与认证方式 | 外部“引用审查Agent”的介绍与端点 |
| Message（消息） | 带类型内容的交互 | 提交报告及审查要求 |
| Task（任务） | 可被跟踪的执行对象 | 长时间引用审查的taskId与状态 |
| Artifact（产物） | 任务交付的结果材料 | 审查表、修改建议文件 |
| Context标识 | 关联交互上下文 | 后续补充某来源仍关联同次审查 |

这里的Task是A2A协议对象，不要求与自己内部Run一一相等；Message也不是对方全部模型上下文。能力卡片不能替代认证，更不能把卡片写的“可信”当授权证明。

## 5. 一次完整A2A委派

```text
发现并验证Agent Card → 选择共同支持的接口/版本与认证
→ SendMessage提交目标、输入与必要范围
→ 简单请求直接得到Message；长任务得到Task
→ 根据能力查询GetTask或订阅/流式接收状态与产物
→ 若需要输入，补充信息并关联原任务
→ 完成后取得Artifact并按自身验收检查
→ 取消时请求CancelTask，再确认实际终态与已有产物
```

在官方1.0 JSON-RPC绑定中方法名包含`SendMessage`，与旧版常见`message/send`不同；HTTP与gRPC绑定又有对应编码。先理解共同对象和生命周期，再按实际SDK版本写请求，不靠背一个URL认识协议。

`SendMessage`响应可以是Task或直接Message，不能假设每次都创建长任务。Streaming（流式更新）与Push（推送）是需确认支持的能力；断线后不应重新委派一个新任务，而应使用既有task身份查询。远端取消可能无法撤销已完成动作，Caller与远端系统都需说清部分结果和授权边界。

## 6. A2A与MCP怎么选，不用绝对化口号

| 比较 | MCP | A2A |
|---|---|---|
| 主要抽象 | AI应用接入工具、资源、模板 | 独立Agent系统委派与交付任务 |
| 典型发现对象 | Server能力及工具目录 | Agent Card与支持的接口/技能 |
| 调用者通常关心 | 某个能力的参数与返回 | 目标、任务进度和产物 |
| 内部Loop是否由协议规定 | 不规定 | 不规定远端内部规划/工具实现 |
| 是否绝对只能同步 | 不是，可有流式/长任务扩展 | 不是，可直接消息或长任务 |

可以用MCP工具封装一次A2A委派，也可以让A2A服务内部调用MCP。选择取决于你的公共接口是“调用这项能力”还是“把工作交给另一个独立Agent系统”，而不是看到多Agent就强上A2A。

<details>
<summary>Codex、Claude与框架中的内部子Agent，不应硬套A2A</summary>

Claude用户固定`Task.ts`区分本地命令、本地/远程Agent等任务类型，维护状态和输出位置；这些是产品内部对象，不足以证明它们统一走A2A。Codex固定源码里的子Agent路径和上下文继承同样应按自己的运行时契约理解。

OpenAI Agents SDK官方用handoffs和agents-as-tools区分控制转移与返回；LangGraph可以把子图作为复杂状态流程的一部分。以上都可以表达多Agent，但并不要求每个内部调用通过A2A网络协议。只有读到具体适配器和协议请求，才应声称某个产品采用了某版A2A。

</details>

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. 多Agent什么时候值得？

<details>
<summary>参考答案</summary>

当子任务独立、可并行、上下文可隔离且结果可验证时，分工可能有收益；还需计算Token、协调、错误和汇聚成本。强依赖同一工作区、反复互等时，单Agent或简单工具并行可能更好，应与基线比较。

</details>

### 2. Handoff与Agent-as-Tool有什么区别？

<details>
<summary>参考答案</summary>

Agent-as-Tool通常保留父级控制，子任务返回结果后父级继续；Handoff把当前处理权交给另一个Agent。Manager/Worker还要负责多任务调度和最终验收。它们是控制关系，不自动决定通信协议或部署进程。

</details>

### 3. A2A原理与完整生命周期是什么？

<details>
<summary>参考答案</summary>

先用Agent Card发现能力、接口版本和认证，发送消息发起或继续工作，简单请求可直接回Message，长任务用Task跟踪状态与Artifact。调用方查询、订阅或补充输入，最终独立验收；取消需确认终态，不等于外部动作回滚。协议不规定远端内部Loop。

</details>

### 4. MCP和A2A如何区分？

<details>
<summary>参考答案</summary>

MCP主要标准化AI应用到工具、资源和模板的能力接入；A2A主要标准化独立Agent系统间的任务委派和产物交付。都有异步或长任务可能，不要用是否能返回Task作绝对区分。内部子Agent也可以不用两者。

</details>

### 5. 两个Agent同时改文件怎么办？

<details>
<summary>参考答案</summary>

分开Context只隔离信息，不隔离资源。应明确写入所有权，采用单写者、独立工作区或版本检查加合并验证。结果汇聚验证来源与冲突，而不是把两个答案拼起来当成功。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| 多Agent必定更强 | 收益需覆盖协调成本和新的失败模式。 |
| A2A就是Agent互相发字符串 | 它定义发现、消息、任务、产物与交互语义。 |
| 用了Subagent就一定走A2A | 内部控制可以用私有接口。 |
| Agent Card等于认证 | 它声明信息，身份和访问授权另验证。 |
| 取消Task等于撤销远端动作 | 已有结果和副作用仍要核对。 |
| MCP绝不支持长任务 | 当前规范可有任务扩展，需按版本比较。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：父级把所有历史与密钥交给检查Agent有什么问题？

<details>
<summary>查看参考答案</summary>

扩大泄漏和上下文噪声，并可能跨权限边界。只传目标、必要证据、授权范围和输出契约，由可信程序管理凭证。

</details>

### 自测 2：为什么子任务成功不等于父任务成功？

<details>
<summary>查看参考答案</summary>

子任务只满足局部目标，父级仍要检查覆盖、冲突、全局约束和最终交付。

</details>

### 自测 3：A2A请求直接返回Message，是否违反协议？

<details>
<summary>查看参考答案</summary>

不违反。官方1.0允许简单请求直接返回消息，不必每次生成持久Task。

</details>

### 自测 4：网络断开后直接重新SendMessage创建任务有何风险？

<details>
<summary>查看参考答案</summary>

可能重复委派工作和副作用。应保留原任务身份并查询或重新订阅状态，按服务契约决定重试。

</details>

### 自测 5：A等B而B又委派回A，怎样防？

<details>
<summary>查看参考答案</summary>

明确任务依赖、委派深度与预算，检测循环等待并停止或重规划；仅有协议消息传输不会自动解决调度死锁。

</details>

### 自测 6：两个Agent用了独立文件副本，最后合并还要检查什么？

<details>
<summary>查看参考答案</summary>

基线是否一致、修改是否冲突、最终文件是否满足约束与测试。隔离避免直接覆盖，但不保证合并语义正确。

</details>

### 自测 7：怎样证明某产品的多Agent用了A2A？

<details>
<summary>查看参考答案</summary>

需要读取实际协议适配与请求实现，或对应官方支持说明；仅看到remote_agent、handoff或task字段不能推出协议。

</details>

## 资料与下一步

官方：[A2A 1.0规范入口](https://a2a-protocol.org/latest/specification/)、[OpenAI Agents SDK Handoffs](https://openai.github.io/openai-agents-python/handoffs/)、[Agents as tools](https://openai.github.io/openai-agents-python/tools/)。固定产品对象：[Task.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/Task.ts)；Codex源码索引见本章资料总入口。下一章将诊断数据与业务恢复数据彻底分开。

本章对应研究能力：`AGENT-030`、`AGENT-031`、`AGENT-046`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](17-RoutingProviderResilience.md) · [模块目录](../README.md) · [下一章 →](19-TraceReplayObservability.md)
