# 12. L3 接入层：知识、记忆与扩展能力接入

[← 11](11-ToolExecutionAndEffects.md) · [Agent 主线](../README.md) · [13 →](13-ResourcesAndEnvironments.md)

> 主线位置：**L3 接入层**。通用工具边界明确后，再接入知识、记忆与可扩展能力。
>
> 本章产物：**检索/存取契约与 MCP、Skill、Hook 的责任边界**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 先学信息与状态存取接口，再区分 MCP / Skill / Hook，最后用代码搜索作接口对照。协议、程序性知识和生命周期扩展不属于同一种抽象。

[把信息需求连接到可信来源](#part-1) → [工具、协议、技能与钩子各负责什么](#part-2) → [能力扩展的失败、版本和安全](#part-3) → [用代码资源检索检查接口是否足够表达需求](#part-4)

<a id="part-1"></a>

## 1. 把信息需求连接到可信来源

L2 决定何时检索、怎样形成查询以及如何使用结果；L3 负责连接检索、数据读取与记忆存取服务；L4 保存文档、索引、记忆记录及业务事实。

一个检索结果应尽量包含内容、来源标识、版本或时间、作用域、定位信息与访问权限。分数不等于真实性，也不能跨数据源直接当统一置信度。检索时的权限过滤与使用时的适用性核对都不可少。

```text
信息缺口 → 受控查询 → 权限过滤 → 候选证据 → 排序/核验
→ 证据引用 → L2 上下文组装 → 后续决策
```

RAG 是获取和使用证据的方案，不是第五层。Agent 可以通过普通接口、全文搜索、结构化查询、文件读取或向量检索获取信息，不应默认所有问题都要向量化。

State Store 接口关注恢复、版本与一致性；Memory Store 接口关注作用域、来源、更新与删除；Artifact Store 接口关注大对象与可验证引用。可以使用同一种数据库，但不能混用语义和生命周期。

<a id="part-2"></a>

## 2. 工具、协议、技能与钩子各负责什么

这些概念跨越不同类型。协议接入主要在 L3；技能内容可以存于 L4；何时加载技能、何时运行钩子主要由 L2 控制。

### 先给稳定边界

#### Tool

```text
一次可执行能力
```

例如：

```text
read_file
run_tests
create_ticket
query_database
```

#### MCP

```text
外部能力 / Resource / Prompt 的标准连接协议
```

它定义 Host / Client / Server 等协议边界，不等于 Agent Loop。

#### Skill

```text
可发现、可按需加载的程序性知识 / workflow / resource package
```

它通常描述“怎样完成某类任务”，可能引用 Tool，也可能包含 instruction / script / asset。

#### Hook

```text
Runtime 生命周期扩展点
```

例如：

```text
before_tool
post_tool
pre_compact
post_compact
run_finished
```

Hook 不应该成为 Runtime 主循环本身。

### MCP 解决什么标准化问题

没有 MCP 时，Agent Host 接外部系统可能各写一套：

```text
GitHubAdapter
SlackAdapter
DatabaseAdapter
NotionAdapter
```

MCP 提供标准化协议边界。

官方规范明确区分：

```text
Prompts
Resources
Tools
```

并强调不同控制边界。

稳定心智模型：

```text
MCP Server
→ exposes capability / resource

MCP Client
→ maintains connection / protocol

MCP Host
→ Agent application / runtime using clients
```

### Tool / Resource / Prompt 为什么要分开

##### Tool

模型可以选择执行动作：

```text
query_database(...)
```

##### Resource

更接近可读取 Context：

```text
project://schema
```

##### Prompt

提供可复用 Prompt 模板 / interaction primitive。

如果全部叫 Tool：

```text
读数据
执行副作用
加载模板
```

权限和生命周期都难表达。

### Transport 不是 MCP 的核心价值

面试常问：

```text
stdio / SSE / Streamable HTTP
```

需要知道它们是连接方式，但不要把答案讲成：

> MCP 就是一种 HTTP 协议。

真正稳定的价值是：

```text
Capability Discovery
Schema / Resource Contract
Client / Server Boundary
Lifecycle
Standard Interop
```

Transport 可以演进。

### Skill 与 Tool 的区别

Tool：

```text
“我能做什么动作？”
```

Skill：

```text
“完成这种任务时，应该怎样组织步骤和资源？”
```

例如：

```text
Tool:
run_command
read_file
edit_file

Skill:
release-python-package
  - read pyproject
  - update version
  - run tests
  - build
  - verify artifact
```

Skill 可以引用多个 Tool。

Anthropic Agent Skills 官方资料正是把 procedural knowledge、scripts、resources 组织成可发现 / 可加载能力包。

### Skill Progressive Disclosure

一个 Skill 可能包含大量说明。

错误：

```text
所有 Skill 全量注入 System Prompt
```

正确思路：

```text
skill catalog
→ task match
→ load selected skill
→ use only needed resource
```

这与 Tool Progressive Loading 的动机相同：

```text
减少 Context 占用
降低选择混乱
提高可维护性
```

### Hook 是什么

Hook 是 Runtime 在生命周期节点提供的扩展接口。

例如：

```text
before_model
before_tool
post_tool
pre_compact
post_compact
run_complete
```

使用场景：

```text
审计
指标
策略注入
自定义验证
通知
Context enrichment
```

但 Hook 必须受控，否则会变成隐藏控制流。

<a id="part-3"></a>

## 3. 能力扩展的失败、版本和安全

接入协议提供互操作能力，不自动赋予权限，不替代数据可信度检查，也不保证所有扩展兼容当前运行环境。

### Extension Failure 怎么处理

如果 Hook / MCP / Skill 失败：

```text
是否阻断主任务？
是否 retry？
是否降级？
是否只是记录 warning？
```

需要按 Extension 类型定义。

例如：

```text
Audit Hook failure
→ 可能 fail-closed

Optional notification hook
→ 可以 warning + continue
```

不能全部 `except Exception: pass`。

### Capability Versioning

Tool / Skill / MCP Server 都会升级。

Runtime 应至少考虑：

```text
capability id
schema version
server version
instruction version
compatibility
```

否则 Session Resume 后可能出现：

```text
旧 Context 中看到 tool schema v1
当前 Runtime 只有 v2
```

造成 invalid arguments 或行为漂移。

### Security Boundary

第三方 MCP Server / Skill 不是天然可信。

需要：

```text
server allowlist
capability allowlist
schema validation
permission
sandbox
secret scope
network policy
trace
```

尤其：

```text
MCP Tool 可以有副作用
Skill 可以诱导调用高风险 Tool
Resource 可能包含 Prompt Injection
```

所以 Capability Extension 必须和前两章的 Security 模型结合。

<a id="part-4"></a>

## 4. 用代码资源检索检查接口是否足够表达需求

Codex 这类编码 Agent 提供一个实现观察窗口：结构化符号、路径、文本、语义与依赖信息应按需求组合。这是信息接入方法的对照，不另开一个项目学习支线。

### Repository Understanding 不等于 Vector RAG

HUMAN-A `AGENT-037` 直接比较：

```text
Vector RAG
AST / LSP
ripgrep / Filesystem Search
Dependency Graph
```

它们解决不同问题。

#### ripgrep / Text Search

适合：

```text
符号名
错误字符串
配置项
调用痕迹
```

优点：快、精确、成本低。

#### Filesystem Navigation

适合：

```text
项目结构
模块边界
配置文件位置
```

#### AST / LSP

适合：

```text
definition
reference
type
symbol relationship
```

#### Vector / Semantic Search

适合：

```text
不知道具体关键词
按语义找相关实现
```

#### Dependency Graph

适合：

```text
impact analysis
跨模块依赖
```

成熟 Coding Agent 通常组合，而不是只靠一种检索。

### Repo Understanding 的搜索漏斗

建议：

```text
1. Read task / issue
2. Inspect repo tree
3. Exact text / symbol search
4. Read local neighborhood
5. Follow references / dependency
6. Semantic search only when useful
7. Build small working set
```

不要一开始：

```text
把整个 repo 全塞 Context
```

Context Engineering 原则同样适用。

## 能力目录也有生命周期

目录可以保存稳定身份、版本、摘要、参数schema位置、来源/租户、可见条件、运行时handler及风险元数据；模型先拿少量候选，再按需加载完整契约。Skill可以先加载说明，真正需要脚本/资产时再读取，不等于永远全量塞入Prompt。

Claude Code索引里的 `searchHint`、`dynamicSkillDirTriggers`、`discoveredSkillNames`支持这种渐进加载观察；Codex索引记录了command、MCP tool、prompt、agent等Hook handler形式。**协议/扩展提供什么**和**运行层何时允许用它**仍是不同责任，详情见两个[固定源码索引](../../research/agent-sources/README.md)。

版本变化或插件卸载后，要让旧可见集合与当前执行目录一致。不要将安全门仅做成可被关闭的Hook；Hook失败策略依责任区分：诊断Hook可以受控降级，安全校验失败应拒绝或升级，而不能按普通日志错误忽略。

## 本章自测

<details>
<summary>RAG、MCP、Skill、Hook 是同一种抽象吗？</summary>

不是。RAG 是证据获取与使用方案，MCP 是协议，Skill 是程序性知识/资源包，Hook 是生命周期扩展机制。

</details>

<details>
<summary>为什么记忆策略与 Memory Store 接口分章？</summary>

前者决定保存和使用什么，后者兑现受控读写；分清职责能独立更换存储而保持运行语义。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>Hook失败可以统一忽略吗？</summary>

不可以；诊断与安全责任不同，安全关键检查失败应拒绝或升级，不能开放执行。

</details>

<details>
<summary>Skill包含脚本是否等于脚本自动获得执行许可？</summary>

不是；加载知识、读取资产、执行脚本是不同动作，各自受到权限与环境限制。

</details>

## 回到主线

现在应能独立说明：检索/存取契约与 MCP、Skill、Hook 的责任边界。下一章：[L4 资源层：模型、数据与执行环境](13-ResourcesAndEnvironments.md)。

对应真人问题：`AGENT-023`、`AGENT-024`、`AGENT-025`、`AGENT-037`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 11](11-ToolExecutionAndEffects.md) · [Agent 主线](../README.md) · [13 →](13-ResourcesAndEnvironments.md)
