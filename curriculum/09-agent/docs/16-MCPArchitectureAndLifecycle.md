# 16. MCP：从 Host / Client / Server 到完整协议往返

[← 上一章](15-InjectionAndContainment.md) · [Agent 目录](../README.md) · [下一章 →](17-SkillsHooksAndExtensions.md)

你已经会注册自己的工具了。可是每个AI应用都要接文件、工单和数据库，难道每一边都重新写一套通信约定？

> MCP标准化的是应用与外部能力之间发现、请求、结果返回的共同语言。

先看参与者和一次往返，再看版本、传输与出错处理。它不是新模型，也不是Agent主循环。



---

<a id="legacy-16-05"></a>
<a id="section-1"></a>
<a id="core-1"></a>

## 1. MCP先给清楚定义

MCP（Model Context Protocol，模型上下文协议）是连接AI应用与外部系统的开放标准。它规定参与者怎样发现能力、请求工具、读取资源和获取提示模板，**不规定Agent应该怎样规划、使用记忆或管理整个任务**。本章采用官方 `2026-07-28` 协议作为学习基线，关键行为核验于 2026-09-28，旧协议差异单独标明。

没有MCP，你也能写`read_file()`或调用企业HTTP API；只是每个应用与每个外部系统可能各写一套接入。MCP把公共交互格式标准化，让应用不必为每个服务器重新发明发现与调用协议。业务API本身、真实授权和Agent Loop并没有因此消失。


---

<a id="section-2"></a>
<a id="core-2"></a>

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

---

<a id="legacy-16-06"></a>
<a id="section-3"></a>
<a id="core-3"></a>

## 3. Tools、Resources、Prompts各提供什么

| 原语 | 核心含义 | 例子 | 常用交互 |
|---|---|---|---|
| Tool（工具） | 可请求执行的能力 | 读取文件、查询订单 | `tools/list`发现，`tools/call`调用 |
| Resource（资源） | 可供应用读取的上下文材料 | 文件内容、数据库Schema | `resources/list`及`resources/read`等 |
| Prompt（提示模板） | 可复用的交互模板 | 带引用的报告提示模板 | `prompts/list`、`prompts/get` |

“资源”不意味着信息已经自动进入模型；“工具”不保证一定有副作用；“提示模板”不自动拥有系统指令权。宿主仍决定何时读取、哪些可见、如何编排、哪些动作要批准。模型生成的函数调用与MCP的`tools/call`也是两层：前者是模型API表示，后者是Host通过Client发出的协议请求。

三者不能全部叫工具：读取资料、执行动作和加载模板的使用时机与权限不同；它们都不会自动成为可信系统指令。

---

<a id="section-4"></a>
<a id="core-4"></a>

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

<details>
<summary>展开一条协议请求：字段怎样对应上面的往返（不是SDK程序）</summary>

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

</details>

---

<a id="section-5"></a>
<a id="core-5"></a>

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

---

<a id="legacy-16-07"></a>
<a id="section-6"></a>
<a id="core-6"></a>

## 6. 传输是什么，安全又是什么

Stdio（标准输入输出）通常连接本地子进程；Streamable HTTP（可流式HTTP）用于HTTP请求及可选事件流。JSON-RPC规定消息的含义，传输负责搬运。SSE（服务器发送事件）是可能使用的流式机制，不是MCP本身。启动本地Server意味着运行软件，仍要审查来源和权限；远程访问还要处理认证、TLS与令牌范围。

目录发现和模型可见筛选可独立：工具少时直接提供允许的说明；工具多时用第05章的按需发现机制。不是每次会话都必须把全部Server的完整Schema塞给模型。

### 需要更多输入、出错和目录过期时怎么办

在2026-07-28工具规范中，服务端可用`input_required`结果请求用户补充信息，宿主把回答交回原请求上下文，而不是让模型猜出用户凭证。普通工具失败、协议格式错误和需要输入是不同结果，调用方应按具体版本及错误类别处理。用户拒绝提供信息时，要停止或澄清，不能把拒绝当临时网络故障。

目录应缓存得有边界：授权不同，允许的工具集合可能不同；工具列表变化通知是刷新线索，不应当永久可靠的业务事件流。执行时工具已下线或参数格式改变，就刷新目录或给出明确错误，不能把同名请求静默送给另一个能力。

真正稳定的价值是能力发现、工具/资源契约、参与者边界与互操作，不是只记住stdio、SSE或HTTP三个传输名词。

---

<a id="human-a"></a>
<a id="section-7"></a>
<a id="core-7"></a>

## 7. 从协议回到执行系统

MCP目录只提供能力说明。模型候选仍由宿主校验与授权，通过Client调用Server，结果再规范化回填。协议断线不保证远端动作没发生，按[工具错误](06-ToolExecutionAndFailure.md)和[恢复](13-CheckpointResumeAndRecovery.md)核对。

官方入口：[2026-07-28架构](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) · [工具规范](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) · [旧版初始化](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)。版本事实和教学例子分开。

---

<a id="summary"></a>

## 本章小结

MCP 规定 AI 应用与外部能力怎样发现、请求和返回。Host 决定任务和模型可见范围，Client 承担协议通信，Server 提供实际能力。模型调用表示与 MCP 请求是两层，发现不等于执行，版本和授权仍需分别核对。

<a id="9-面试怎么答"></a>
<a id="qhostclientserver怎么区分"></a>
<a id="qmcp原理为什么不能只背initialize"></a>
<a id="qmcp工具太多时怎么办"></a>
<a id="qmcp是什么解决什么"></a>
<a id="q模型调用mcp工具的完整链路是什么"></a>
<a id="interview"></a>

## 🎯 面试怎么回答

### MCP 是什么，为什么不是 Agent 框架？

它是 AI 应用连接外部工具、资源和提示模板的开放协议，减少重复接入约定。它不定义整个 Agent 的规划、状态和循环；Host 仍需决定如何把能力接入任务并控制授权。

### Host、Client、Server 怎样协作？

Host 是 AI 应用，内部 Client 与某个 Server 通信；Server 可本地或远程提供能力。Client 发现工具，Host 转为模型说明；模型提出候选后 Host 检查，再由 Client 发协议调用，结果回到 Host 并关联模型请求。

### 为什么不能把 initialize 写成所有版本的唯一流程？

2025-11-25 有初始化协商；本章的 2026-07-28 请求自带版本与能力元数据，Server 必须实现 server/discover，Client 可选择是否先调用。应先核对实际协议与 SDK 支持，再描述生命周期。

### MCP 连接断开，可以直接认为远端没执行吗？

不能。连接状态与业务结果不同。已发出的写操作仍要按原操作身份核对；JSON-RPC 请求 ID 用于关联请求响应，不自动提供业务幂等。

<a id="10-高频易错点"></a>
<a id="pitfalls"></a>

## ⚠️ 易错点

> ⚠️ Client 是宿主中的协议组件，不是使用产品的人，也不等于 LLM。

> ⚠️ tools/list 返回能力说明，真正执行需要 tools/call；目录存在不代表当前用户可以调用。

> ⚠️ clientInfo 是软件身份信息，不是用户认证凭证；Server 与 Host 都要落实各自授权。

> ⚠️ 协议无状态不等于业务无状态，长任务、资源和外部写入仍可能需要可靠状态。

<a id="11-本章自测"></a>
<a id="self-test"></a>

## 本章自测

<details><summary>1. 文件 Server 在本机子进程运行，它还是 MCP Server 吗？</summary>

是。角色由协议职责决定，不由是否远程部署决定；运行本地软件仍需审查来源和权限。

</details>

<details><summary>2. 模型返回 read_document(A)，为什么不能说它已经直接调用 MCP Server？</summary>

这是模型 API 的调用候选。宿主要校验与授权，再让 MCP Client 发送对应协议请求，Server 才实际执行。

</details>

<details><summary>3. 对 2026-07-28，Client 是否必须先调用 server/discover？</summary>

不必须先调用，但 Server 必须实现它。请求携带版本与相关能力，Client 也可以直接请求并处理不支持版本的错误。

</details>

<details><summary>4. 工具返回 input_required，用户拒绝提供信息，应当当作网络异常重试吗？</summary>

不应。它要求补充输入，不是短暂传输故障。应停止该动作或澄清，不能让模型猜凭证或绕过拒绝。

</details>

<a id="8-human-a-信号"></a>
<a id="references"></a>

## 知识回看与权威资料

- [MCP 2026-07-28 架构](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)：核对角色、请求元数据与发现。
- [工具规范](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)：核对目录、调用及结果语义。
- [2025-11-25 生命周期](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)：对照旧版初始化，而不混用两代流程。
- [工具发现](05-ToolRegistrationAndDiscovery.md)：协议目录取得以后，Host 怎样选择模型本轮可见工具。


---

[← 上一章](15-InjectionAndContainment.md) · [Agent 目录](../README.md) · [下一章 →](17-SkillsHooksAndExtensions.md)
