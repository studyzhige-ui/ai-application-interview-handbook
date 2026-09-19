# 17. Skills / Hooks / Plugins：能力扩展与生命周期

工具解决“能做什么动作”，但还留下两个问题：

> 某类任务应该怎样组织步骤？到执行的某个时刻，怎样接入额外规则或处理？

前一个问题引出Skill（技能包），后一个引出Hook（生命周期钩子）。它们可以和MCP一起工作，却不是MCP或Tool的别名。这一章顺着发现、加载、触发、失败和升级讲清扩展的生命周期。

[← 上一章](16-MCPArchitectureAndLifecycle.md) · [Agent 目录](../README.md) · [下一章 →](18-RoutingAndProviderResilience.md)

---

<a id="section-1"></a>

## 1. 先给稳定边界

<a id="legacy-16-01"></a>

上一章已经完整解释MCP的协议往返。本章专门处理技能知识、钩子触发和插件交付；术语比较只是定位，不再把完整协议生命周期压成三个名词。

### Tool

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

### MCP

```text
外部能力 / Resource / Prompt 的标准连接协议
```

它定义 Host / Client / Server 等协议边界，不等于 Agent Loop。

### Skill

```text
可发现、可按需加载的程序性知识 / workflow / resource package
```

它通常描述“怎样完成某类任务”，可能引用 Tool，也可能包含 instruction / script / asset。

### Hook

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

Hook 不应该成为 Runtime（运行时执行系统） 主循环本身。

---

<a id="section-2"></a>

## 2. 为什么 Tool 太多会出问题

<a id="legacy-16-02"></a>

假设有 500 个 Tool。

如果每轮全部把：

```text
name
description
JSON schema
examples
```

塞进模型 Context：

```text
Token Cost ↑
Tool Selection Confusion ↑
Prompt Cache Stability ↓
Latency ↑
```

因此 Capability Discovery 本身应该成为 Runtime 能力。

HUMAN-A `AGENT-021` 有 20 个独立来源，直接追问 Dynamic Discovery / Progressive Loading。

---

<a id="section-3"></a>

## 3. Capability Catalog

<a id="legacy-16-03"></a>

可以先维护一个轻量目录：

```python
# 能力目录示意：先用轻量摘要发现，再按load_key加载必要知识或工具定义。
CapabilitySummary(
    id="github.search_code",
    kind="tool",
    short_description="Search code in a repository",
    tags=["code", "search", "github"],
    risk="read_only",
    load_key="github-tool-pack",
)
```

模型第一次只看到：

```text
少量 capability summary
```

真正需要时：

```text
select capability
→ load full schema / skill instructions
→ invoke
```

这就是 Progressive Disclosure。

---

<a id="section-4"></a>

## 4. Skill 与 Tool 的区别

<a id="legacy-16-08"></a>

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

一个报告Skill可以先只提供用途，选中后再加载引用格式、核查步骤和模板；读文件仍调用工具。技能包里的脚本同样需要受控执行，不因叫Skill就拥有特权。

---

<a id="section-5"></a>

## 5. Skill Progressive Disclosure

<a id="legacy-16-09"></a>

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

---

<a id="section-6"></a>

## 6. Hook 是什么

<a id="legacy-16-10"></a>

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

Hook由事件触发，Skill按任务相关性加载，Plugin负责打包分发。处理器若能改状态，必须声明修改边界；可选钩子不能悄悄承担唯一的安全门。

---

<a id="section-7"></a>

## 7. Codex Hooks 的实现证据

<a id="legacy-16-11"></a>

固定 Codex Source Index 已确认：

- `codex-rs/hooks/src/engine/mod.rs`；
- `codex-rs/config/src/hook_config.rs`；
- Hook handler 可以包括 command、MCP tool、prompt、agent；
- compaction 存在 pre/post hook。

这支持：

```text
Core Runtime
→ Lifecycle Event
→ Hook Policy
→ Extension Handler
```

Hook 是横切扩展点，不应该反过来定义整个 Runtime 生命周期。

---

<a id="section-8"></a>

## 8. Extension Failure 怎么处理

<a id="legacy-16-12"></a>

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

可选通知失败可以降级，必要前置检查失败应拒绝继续。技能文件缺失要报告能力不可用，不应改用任意Shell扩权补救。版本不兼容先回到已知基线或明确暂停，而不是所有异常统一忽略。

---

<a id="section-9"></a>

## 9. Capability Versioning

<a id="legacy-16-13"></a>

Tool / Skill / MCP Server 都会升级。

Runtime 应至少考虑：

```text
capability id
schema version
server version
instruction version
compatibility
```

否则 Session Resume（恢复执行） 后可能出现：

```text
旧 Context 中看到 tool schema v1
当前 Runtime 只有 v2
```

造成 invalid arguments 或行为漂移。

---

<a id="section-10"></a>

## 10. Security Boundary

<a id="legacy-16-14"></a>

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

所以 Capability Extension 必须和权限与提示注入章节的安全模型结合。

---

<a id="section-11"></a>

## 11. 产品实现与官方资料对照（按需展开）

<details>
<summary>Claude Code 源码侧的 Progressive Loading 证据</summary>

<a id="legacy-16-04"></a>

固定 Source Index 已确认 `ToolUseContext` 中存在：

```text
dynamicSkillDirTriggers
discoveredSkillNames
```

Tool 还存在：

```text
searchHint
```

用于 deferred tool discovery。

这支持课程抽象：

```text
Capability Catalog
→ Discovery
→ Selection
→ Progressive Loading
→ Invocation
```

而不是：

```text
All Tool Schemas
→ Every Context
```

</details>

具体实现以[固定源码与官方索引](../../../references/agent/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 12. HUMAN-A 信号

本章主要承接：

- `AGENT-021` Dynamic Tool Discovery；
- `AGENT-023` MCP Protocol：20 个来源；
- `AGENT-024` Skill / Tool / Function / MCP / Rule / Workflow 边界：34 个来源；
- `AGENT-025` Skill Progressive Disclosure：10 个来源。

这说明企业已经不满足于问：

> “MCP 是什么？”

而会追：

```text
为什么需要标准化？
Tool 太多怎么办？
Skill 和 Tool 区别？
按需加载怎么做？
```

---

<a id="interview"></a>

## 13. 面试怎么答

### Q：Tool、MCP、Skill、Hook 有什么区别？

🎯 **30 秒回答**：

> Tool 是一次可执行能力；MCP 是 Host/Client/Server 之间标准化暴露 Tool、Resource、Prompt 等能力的协议；Skill 更像可发现、按需加载的程序性知识/资源包，通常会组织多个 Tool 完成一种任务；Hook 是 Runtime 生命周期扩展点，用于审计、验证或扩展。它们不是同一层抽象，也不能全部叫插件。

### Q：Tool 太多怎么处理？

🎯 **30 秒回答**：

> 不把所有完整 schema 永久塞进 Context，而是建立 capability catalog，让模型先看到轻量 summary，通过 intent/search 发现候选，再按需加载完整 Tool/Skill 定义，并用 eval 验证 discovery recall 和 tool selection accuracy。

### Q：MCP是什么，解决什么？

🎯 **30 秒回答**：

> MCP是连接AI应用与外部系统的开放协议标准，定义能力发现、工具调用、资源读取和提示模板等交互。它减少重复接入代码，不规定Agent怎么规划，也不自动提供业务授权。Host仍负责把协议能力接到模型与执行循环。

### Q：Host、Client、Server怎么区分？

🎯 **30 秒回答**：

> Host是整个AI应用，Client是Host内连接某Server的协议组件，Server是提供工具、资源或模板的程序，可以本地或远程。模型通常由Host另外调用，不等于MCP Client或Server。一个Host可以有多个Client分别连接多个Server。

### Q：模型调用MCP工具的完整链路是什么？

🎯 **30 秒回答**：

> Client发现Server工具，Host把允许的说明转换成模型API格式；模型产生候选调用，Host校验与授权后让Client发送tools/call；Server执行并返回，Host把结果关联原模型调用并回填。发现返回Schema，不是下载函数源码或自动执行。

### Q：MCP原理为什么不能只背initialize？

🎯 **30 秒回答**：

> initialize属于明确版本的生命周期。2026-07-28官方架构强调请求自带版本能力元数据和可选Client调用server/discover，Server必须实现发现方法。教学要区分旧新版本，核心仍是协议兼容、能力发现和受控调用。不能拿旧教程当所有版本的唯一流程。

### Q：MCP工具太多时怎么办？

🎯 **30 秒回答**：

> Host可以维护完整目录而只向本轮模型暴露相关少量说明，先发现候选再加载具体Schema。兼顾候选召回、Token成本、版本与权限；Server目录存在不意味着所有工具都应对当前任务可见。

---

<a id="pitfalls"></a>

## 14. 高频易错点

⚠️ **MCP = Agent Framework。** MCP 不负责 Agent Loop。

⚠️ **Skill = Tool。** Skill 更接近程序性任务包。

⚠️ **Hook 可以随便改变 State（状态）。** 无约束 Hook 会制造隐藏控制流。

⚠️ **所有 Tool Schema 全量注入更稳。** 规模大时会增加 Context 和选择混乱。

⚠️ **MCP Client就是LLM。** 它是Host中的协议组件，LLM另由Host调用。

⚠️ **MCP Server只能远程部署。** 本地进程也可以提供MCP。

⚠️ **tools/list会运行所有工具。** 它发现说明，执行需tools/call。

⚠️ **clientInfo证明了用户身份。** 只是兼容/诊断元数据，认证另行处理。

⚠️ **MCP等于SSE。** 协议语义与传输机制不同。

⚠️ **协议无状态等于业务没有状态。** 资源与长任务可以有状态，不同抽象层。

⚠️ **Skill和Hook都是工具的一种名字。** 它们分别管理知识使用与生命周期扩展。

---

<a id="self-test"></a>

## 15. 本章自测

<details><summary>1. 为什么 Progressive Loading 是 Context Engineering 问题？</summary>

因为 Tool/Skill metadata 本身会占 Context；能力规模扩大后，需要只加载与当前任务相关的完整定义，避免成本和选择混乱。

</details>

<details><summary>2. MCP 的 Tool 与普通本地 Tool 最大差异是什么？</summary>

MCP Tool 通过标准协议由外部 Server 暴露，涉及连接生命周期、远程信任和协议兼容；但进入 Runtime 后仍需要相同的 schema、permission、failure、trace 等 Tool Contract。

</details>

<details><summary>3. 为什么 Hook 不应该替代 Runtime 主循环？</summary>

Hook 适合生命周期横切扩展；如果关键控制逻辑散落在 Hook 中，会让执行路径不可见、难恢复、难评测和难推理。

</details>

<details><summary>4. 你的应用连文件和工单两个Server，通常需要几个Client？</summary>

通常分别建立对应Client，由一个Host管理；用户和LLM不是这两个Client对象。

</details>

<details><summary>5. tools/list返回read_document Schema，模型立刻能执行Python函数吗？</summary>

不能。模型只生成调用请求，Host经授权路由到Client，Server才真正执行实现。函数代码留在执行端。

</details>

<details><summary>6. 为什么resources/read后还需要Host处理内容？</summary>

读取返回材料不等于自动编排进模型输入，Host需检查权限、相关性、预算与来源，并决定何时给模型使用。

</details>

<details><summary>7. 把MCP的RPC id用作跨重试业务幂等键一定够吗？</summary>

不一定。RPC id关联一次请求响应；逻辑动作身份和去重语义需由业务接口明确，网络重试可能使用不同RPC请求。

</details>

<details><summary>8. 2026文档写server/discover mandatory，Client是否每次都必须先调用？</summary>

Server必须实现它，Client调用是可选的兼容发现步骤；请求本身携带版本能力信息，不能把服务端实现要求误读成每次调用的强制握手。

</details>

<details><summary>9. 为什么两份旧源码不能证明当前所有MCP能力？</summary>

源码固定在具体提交，功能和协议版本可能不同。本章用它们说明Host接入责任，具体当前协议字段和方法以官方版本文档核验。

</details>

<details><summary>10. 插件里有一个可选Hook做审批，禁用插件后能直接执行吗？</summary>

不应。核心授权应是不可绕过的执行门，可选扩展不能决定是否存在基本安全机制。

</details>

<details><summary>11. MCP能处理长任务，所以A2A就没有意义了吗？</summary>

不等价。能力调用与独立Agent间委派/任务交付关注不同责任，协议功能有重叠时应按接口抽象、对象和交互需要比较，而不是按一个是否异步的特征选择。

</details>

---

[← 上一章](16-MCPArchitectureAndLifecycle.md) · [Agent 目录](../README.md) · [下一章 →](18-RoutingAndProviderResilience.md)
