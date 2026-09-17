# 16. MCP、Skill与Hook：外部能力怎样接进来

[← 上一章](15-GuardrailsInjectionContainment.md) · [模块目录](../README.md) · [下一章 →](17-RoutingProviderResilience.md)

> 本章要解决：从官方定义、参与者和一次完整消息往返理解MCP，不把协议、工具与插件混在一起。

## 1. MCP先给清楚定义

MCP（Model Context Protocol，模型上下文协议）是连接AI应用与外部系统的开放标准。它规定参与者怎样发现能力、请求工具、读取资源和获取提示模板，**不规定Agent应该怎样规划、使用记忆或管理整个任务**。本章主要依据用户指定的官方`2026-07-28`架构文档，旧协议差异单独标明。

没有MCP，你也能写`read_file()`或调用企业HTTP API；只是每个应用与每个外部系统可能各写一套接入。MCP把公共交互格式标准化，让应用不必为每个服务器重新发明发现与调用协议。业务API本身、真实授权和Agent Loop并没有因此消失。

## 2. Host、Client、Server究竟是谁

| 参与者 | 中文和职责 | 在文件报告任务中 |
|---|---|---|
| Host | 宿主AI应用，管理客户端并决定如何使用能力 | 你使用的Agent程序或Claude Code |
| Client | 宿主中的MCP连接/协议组件 | 连接文件服务的客户端对象 |
| Server | 提供能力的程序，可本地也可远程 | 提供文件读取或企业资料查询的服务 |
| LLM | 被宿主调用的模型，不是以上三者的同义词 | 选择读A并生成工具参数 |

```text
用户 ↔ Host（任务、模型调用与授权）
          ├─ MCP Client A ↔ 文件 Server
          └─ MCP Client B ↔ 工单 Server
```

Host通常为每个Server建立对应Client。Client不是“使用这个产品的人”，Server不是“模型服务”的别称。Server可以作为本机子进程运行，也可以服务多个远程Client；看它提供的协议职责，不看机器放在哪里。

## 3. Tools、Resources、Prompts各提供什么

| 原语 | 核心含义 | 例子 | 常用交互 |
|---|---|---|---|
| Tool（工具） | 可请求执行的能力 | 读取文件、查询订单 | `tools/list`发现，`tools/call`调用 |
| Resource（资源） | 可供应用读取的上下文材料 | 文件内容、数据库Schema | `resources/list`及`resources/read`等 |
| Prompt（提示模板） | 可复用的交互模板 | 带引用的报告提示模板 | `prompts/list`、`prompts/get` |

“资源”不意味着信息已经自动进入模型；“工具”不保证一定有副作用；“提示模板”不自动拥有系统指令权。宿主仍决定何时读取、哪些可见、如何编排、哪些动作要批准。模型生成的函数调用与MCP的`tools/call`也是两层：前者是模型API表示，后者是Host通过Client发出的协议请求。

## 4. 一次完整工具调用：发现不是执行

以`read_document(doc_id)`为教学工具名：

```text
Host连接Server并检查协议兼容与认证
→ Client获取工具目录tools/list
→ Host把允许的工具说明转换成模型API的tools格式
→ 模型返回read_document及参数A
→ Host进行结构/语义/权限检查
→ Client发送tools/call(name, arguments)
→ Server校验请求、使用自身权限访问文件
→ Server返回内容或错误
→ Host投影结果、关联模型call_id，回填给模型
→ 模型基于资料继续任务
```

MCP目录包含说明和输入Schema，不是把服务器函数源码下载到模型。即使Server已经做参数检查，Host仍要负责自己任务边界；即使Host批准，Server仍要验证其资源权限。

下面是`2026-07-28`请求形态的**教学改写**，省略传输认证等环境配置，不是可直接运行的SDK代码：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_document",
    "arguments": {"doc_id": "A"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {"name": "report-host", "version": "1.0"}
    }
  }
}
```

`id`关联本次RPC请求与响应；它不自动等于业务幂等键。`name/arguments`定位工具和输入；`_meta`声明协议版本与客户端能力，clientInfo只是软件身份元数据，**不是证明用户身份的令牌**。响应内容还要由Host转成模型能理解的工具结果，不是MCP Server直接推动整个Agent循环。

## 5. 不要混写2025与2026生命周期

| 主题 | 官方2025-11-25 | 官方2026-07-28 |
|---|---|---|
| 初始化/兼容 | `initialize`协商，随后initialized通知 | 请求自带版本/能力元数据；Server实现`server/discover`，Client可选先调用 |
| 协议状态 | 有明确初始化生命周期 | 请求可独立解释的无状态设计 |
| 工具目录 | tools/list及调用 | 核心发现/调用仍在，增加相应响应/缓存语义 |
| 变更通知 | 协商能力后的通知模式 | 用`subscriptions/listen`显式订阅所需通知 |
| Sampling | 可由Server请求Client侧模型采样 | 官方标为弃用，不能作为新实现默认主线 |

“无状态”不等于工具不能读写数据库，也不等于长任务没有状态；它指协议请求解释方式。官方还有可选Tasks扩展，因此不能用“MCP一定没有长任务”来区分A2A。

工具目录变化后，按能力通知或重新查询刷新；不把网络断开等同于远端动作失败。SDK具体支持哪个版本需检查所安装版本，固定Codex/Claude快照也不能自动视作支持今天所有新规范。

## 6. 传输是什么，安全又是什么

Stdio（标准输入输出）通常连接本地子进程；Streamable HTTP（可流式HTTP）用于HTTP请求及可选事件流。JSON-RPC规定消息的含义，传输负责搬运。SSE（服务器发送事件）是可能使用的流式机制，不是MCP本身。启动本地Server意味着运行软件，仍要审查来源和权限；远程访问还要处理认证、TLS与令牌范围。

目录发现和模型可见筛选可独立：工具少时直接提供允许的说明；工具多时用第05章的按需发现机制。不是每次会话都必须把全部Server的完整Schema塞给模型。

### 需要更多输入、出错和目录过期时怎么办

在2026-07-28工具规范中，服务端可用`input_required`结果请求用户补充信息，宿主把回答交回原请求上下文，而不是让模型猜出用户凭证。普通工具失败、协议格式错误和需要输入是不同结果，调用方应按具体版本及错误类别处理。用户拒绝提供信息时，要停止或澄清，不能把拒绝当临时网络故障。

目录应缓存得有边界：授权不同，允许的工具集合可能不同；工具列表变化通知是刷新线索，不应当永久可靠的业务事件流。执行时工具已下线或参数格式改变，就刷新目录或给出明确错误，不能把同名请求静默送给另一个能力。

## 7. Skill、Hook、Plugin不是MCP的别名

| 概念 | 回答的问题 | 生命周期 |
|---|---|---|
| Skill（技能包） | 某类任务怎样做，需要哪些指引/资源 | 发现简述→相关时加载详情→使用资源或工具 |
| Hook（生命周期钩子） | 到某事件时补充执行什么逻辑 | 注册处理器→事件触发→处理结果/错误 |
| Plugin（插件包） | 如何交付一组扩展 | 安装/启用→暴露工具、技能或钩子→升级/禁用 |
| MCP | 外部能力怎样以标准协议交互 | 协议兼容→发现→调用/读取→结果与刷新 |

技能说明可以保存在文件，钩子可以调用MCP工具，但它们仍有不同职责。核心权限不能只放在可选Hook；技能包也可能含不可信脚本，不因名称叫“Skill”就获得执行特权。

### 技能与钩子的错误不要扩散成整个系统的隐式行为

例如报告Skill先提供一句用途描述，选中后加载详细步骤和模板，需要执行脚本时仍通过受控工具。Skill失效要告诉调用方，而不是改成任意Shell去“补齐能力”。Hook应声明是辅助提示、观测还是必要规则：辅助日志失败可以按策略降级，必要前置校验失败则不可放行。更新插件时只需跟踪影响契约的变化，不为每次Hook触发复制所有配置。

<details>
<summary>产品接入对照：如何把协议放回实际Host，而不是虚构统一实现</summary>

Claude Code用户快照的Tool、QueryEngine与MCP连接类型共同说明：MCP客户端拿到的外部能力最终进入Host工具目录与调用体系，再经过API Schema转换和权限门。Codex固定工具层也包含MCP/dynamic转换与ToolRouter，模型调用与外部Server通信在不同边界处理。

这支持“Client发现→Host注册/筛选→模型候选→Host执行门→Client调用”的生命周期。但本文没有用两份快照宣称它们已经实现2026-07-28所有新方法；协议原理以官方版本为准，产品能力以对应实际版本验证。

</details>

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. MCP是什么，解决什么？

<details>
<summary>参考答案</summary>

MCP是连接AI应用与外部系统的开放协议标准，定义能力发现、工具调用、资源读取和提示模板等交互。它减少重复接入代码，不规定Agent怎么规划，也不自动提供业务授权。Host仍负责把协议能力接到模型与执行循环。

</details>

### 2. Host、Client、Server怎么区分？

<details>
<summary>参考答案</summary>

Host是整个AI应用，Client是Host内连接某Server的协议组件，Server是提供工具、资源或模板的程序，可以本地或远程。模型通常由Host另外调用，不等于MCP Client或Server。一个Host可以有多个Client分别连接多个Server。

</details>

### 3. 模型调用MCP工具的完整链路是什么？

<details>
<summary>参考答案</summary>

Client发现Server工具，Host把允许的说明转换成模型API格式；模型产生候选调用，Host校验与授权后让Client发送tools/call；Server执行并返回，Host把结果关联原模型调用并回填。发现返回Schema，不是下载函数源码或自动执行。

</details>

### 4. MCP原理为什么不能只背initialize？

<details>
<summary>参考答案</summary>

initialize属于明确版本的生命周期。2026-07-28官方架构强调请求自带版本能力元数据和可选Client调用server/discover，Server必须实现发现方法。教学要区分旧新版本，核心仍是协议兼容、能力发现和受控调用。不能拿旧教程当所有版本的唯一流程。

</details>

### 5. MCP、Tool、Skill和Hook有什么区别？

<details>
<summary>参考答案</summary>

Tool是可执行能力契约，MCP标准化外部能力连接，Skill提供程序性知识与资源，Hook在生命周期事件触发扩展逻辑。它们可以组合，但工具授权、技能加载、协议请求和Hook失败分别有自己的控制责任。

</details>

### 6. MCP工具太多时怎么办？

<details>
<summary>参考答案</summary>

Host可以维护完整目录而只向本轮模型暴露相关少量说明，先发现候选再加载具体Schema。兼顾候选召回、Token成本、版本与权限；Server目录存在不意味着所有工具都应对当前任务可见。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| MCP Client就是LLM | 它是Host中的协议组件，LLM另由Host调用。 |
| MCP Server只能远程部署 | 本地进程也可以提供MCP。 |
| tools/list会运行所有工具 | 它发现说明，执行需tools/call。 |
| clientInfo证明了用户身份 | 只是兼容/诊断元数据，认证另行处理。 |
| MCP等于SSE | 协议语义与传输机制不同。 |
| 协议无状态等于业务没有状态 | 资源与长任务可以有状态，不同抽象层。 |
| Skill和Hook都是工具的一种名字 | 它们分别管理知识使用与生命周期扩展。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：你的应用连文件和工单两个Server，通常需要几个Client？

<details>
<summary>查看参考答案</summary>

通常分别建立对应Client，由一个Host管理；用户和LLM不是这两个Client对象。

</details>

### 自测 2：tools/list返回read_document Schema，模型立刻能执行Python函数吗？

<details>
<summary>查看参考答案</summary>

不能。模型只生成调用请求，Host经授权路由到Client，Server才真正执行实现。函数代码留在执行端。

</details>

### 自测 3：为什么resources/read后还需要Host处理内容？

<details>
<summary>查看参考答案</summary>

读取返回材料不等于自动编排进模型输入，Host需检查权限、相关性、预算与来源，并决定何时给模型使用。

</details>

### 自测 4：把MCP的RPC id用作跨重试业务幂等键一定够吗？

<details>
<summary>查看参考答案</summary>

不一定。RPC id关联一次请求响应；逻辑动作身份和去重语义需由业务接口明确，网络重试可能使用不同RPC请求。

</details>

### 自测 5：2026文档写server/discover mandatory，Client是否每次都必须先调用？

<details>
<summary>查看参考答案</summary>

Server必须实现它，Client调用是可选的兼容发现步骤；请求本身携带版本能力信息，不能把服务端实现要求误读成每次调用的强制握手。

</details>

### 自测 6：为什么两份旧源码不能证明当前所有MCP能力？

<details>
<summary>查看参考答案</summary>

源码固定在具体提交，功能和协议版本可能不同。本章用它们说明Host接入责任，具体当前协议字段和方法以官方版本文档核验。

</details>

### 自测 7：插件里有一个可选Hook做审批，禁用插件后能直接执行吗？

<details>
<summary>查看参考答案</summary>

不应。核心授权应是不可绕过的执行门，可选扩展不能决定是否存在基本安全机制。

</details>

### 自测 8：MCP能处理长任务，所以A2A就没有意义了吗？

<details>
<summary>查看参考答案</summary>

不等价。能力调用与独立Agent间委派/任务交付关注不同责任，协议功能有重叠时应按接口抽象、对象和交互需要比较，而不是按一个是否异步的特征选择。

</details>

## 资料与下一步

官方：[Tools规范](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)、[Resources规范](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)、[Prompts规范](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)；[MCP 2026-07-28架构](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)、[2025-11-25生命周期对照](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)。固定产品接入：[Tool.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/Tool.ts)、[utils/api.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/api.ts)、[codex-rs/core/src/tools/router.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/tools/router.rs)。下一章解释不同类型的路由，而不是继续增加协议名词。

本章对应研究能力：`AGENT-021`、`AGENT-023`、`AGENT-024`、`AGENT-025`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](15-GuardrailsInjectionContainment.md) · [模块目录](../README.md) · [下一章 →](17-RoutingProviderResilience.md)
