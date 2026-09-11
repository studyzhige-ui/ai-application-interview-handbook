# 09. Tool Registry / Router：Runtime 怎样管理和路由能力

Tool 一旦从 5 个增长到 50、500 个，问题就不再是：

> “怎么写 Function Calling？”

而是：

> **当前到底有哪些 Tool？哪些对模型可见？模型发来的 Tool Call 应路由到哪个 Runtime？重名、版本、动态接入、Deferred Tool 怎么处理？**

`AGENT-019` Tool Lifecycle 有 **10 个 HUMAN-A 来源**，`AGENT-021` Dynamic Tool Discovery / Progressive Loading 有 **20 个来源**，`AGENT-024` Capability Boundary 有 **34 个来源**。

Registry / Router 正是这些问题的中间层。

---

# 1. 先讲人话：Registry 是“能力目录”，Router 是“调用分发器”

可以先记：

```text
Tool Registry
= Runtime 当前知道哪些 Tool、每个 Tool 的 metadata / runtime 是什么

Tool Router
= 收到一个 Tool Call 后，怎样找到正确 Tool 并交给正确执行路径
```

最小图：

```text
Model
  │
  │ tool_call(name="search_code")
  ▼
Tool Router
  │
  ├─ lookup Registry
  │
  ├─ normalize namespace / alias
  │
  └─ dispatch
          │
          ▼
     Tool Runtime
```

Registry 不一定等于“把所有 Tool 都暴露给模型”。

这一点非常重要。

---

# 2. Registry 至少保存什么

一个生产级 Registry 可能管理：

```text
Tool Identity
Tool Namespace
Version
Description
Input / Output Schema
Executor / Runtime Adapter
Exposure Mode
Permission Metadata
Read / Write / Destructive
Parallel Safety
Readiness
Origin / Provider
Lifecycle Status
```

教学结构：

```python
from dataclasses import dataclass
from enum import Enum


class Exposure(str, Enum):
    VISIBLE = "visible"
    DEFERRED = "deferred"
    HIDDEN = "hidden"


@dataclass
class RegisteredTool:
    name: str
    namespace: str
    version: str
    spec: object
    executor: object
    exposure: Exposure
    origin: str
```

---

# 3. 为什么 Tool Name 不能只靠一个全局字符串

如果系统只有内置：

```text
read_file
write_file
run_test
```

很简单。

但接入多个 MCP Server / Plugin 后可能出现：

```text
github.search
notion.search
company_docs.search
web.search
```

如果都叫：

```text
search
```

就会 collision。

所以需要：

```text
namespace + name
```

例如：

```text
repo.search
jira.search
crm.search
```

Namespace 还能表达：

- origin；
- capability family；
- policy boundary。

---

# 4. Duplicate Tool 怎么办

坏设计：

```python
registry[name] = new_tool
```

后注册的静默覆盖旧 Tool。

危险点：

- 模型看到的 Schema 和实际执行器不一致；
- 外部 Tool 可覆盖内置高权限 Tool；
- debug 很困难。

更安全：

```text
Trusted Built-in Duplicate
→ fail fast

External Duplicate
→ reject / skip + warning

Reserved Name
→ reject external registration
```

这正是 Codex Registry 固定源码里可以直接看到的设计。

---

# 5. Codex Registry 的真实实现证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/core/src/tools/registry.rs` 当前明确区分：

```text
register_trusted
register_external
```

并且：

- trusted duplicate 会触发 error/panic 路径；
- external duplicate 会被跳过并记录 warning/collision；
- external tool 如果试图占用默认 namespace 的 `exec_command` / `shell_command` reserved name，会被拒绝；
- Registry 记录 `first_collision`。

这是非常值得吸收的安全原则：

> **外部扩展不能无条件覆盖核心能力。**

---

# 6. Exposure：注册了，不代表立即给模型看

Registry 里可能有 500 个 Tool。

模型本轮只需要 15 个。

因此要区分：

```text
Registered
vs
Model-visible
```

一种抽象：

```text
Visible
→ Schema 直接进入当前 Model Request

Deferred
→ Registry 知道，但需要 Tool Search / Discovery 后才加载

Hidden
→ Runtime 可用，但模型不能直接调用
```

Codex 固定源码中的 `ToolExposure`、`model_visible_specs`、deferred tool search 正体现了这种分层。

---

# 7. Codex ToolRouter：Model-visible Specs 与 Registry 是分开的

`codex-rs/core/src/tools/router.rs` 的 `ToolRouter` 同时持有：

```text
registry
model_visible_specs
code_mode_tool_names
tool_namespaces_info
```

也就是说：

> **Runtime 全部可执行 Tool 集合 ≠ 当前请求暴露给模型的 Tool Spec 集合。**

`exposes_tool()` 还会检查：

- direct visible specs；
- namespace tool；
- code mode nested tool；
- deferred tool search。

这和后面的 Progressive Loading 高度一致。

---

# 8. Router 为什么要先 Normalize Provider Output

不同 Provider 可能产生：

```text
FunctionCall
CustomToolCall
ToolSearchCall
```

Runtime 最好先统一成内部类型：

```python
@dataclass
class ToolCall:
    tool_name: ToolName
    call_id: str
    payload: ToolPayload
```

然后 Router 后面只处理内部协议。

这样：

```text
Provider-specific protocol
→ Adapter / Normalize
→ Internal ToolCall
→ Router
```

而不是每个 Tool Handler 都理解所有 Provider 格式。

Codex `ToolRouter.build_tool_call()` 正是在做这件事。

---

# 9. 为什么 Router 不应该只做 dictionary lookup

真实 Router 还可能决定：

```text
local executor
remote executor
MCP executor
browser worker
sandbox worker
subagent control tool
code-mode worker
```

例如：

```text
read_file
→ local workspace executor

mcp.github.create_issue
→ MCP client runtime

run_shell
→ sandbox executor
```

所以 Router 本质上连接：

```text
Capability Identity
→ Execution Runtime
```

---

# 10. Readiness：Tool 注册了也可能还没准备好

动态 Tool 可能：

- MCP Server 还在连接；
- Remote Worker 正在启动；
- Credentials 正在刷新；
- Plugin 尚未初始化。

因此 Registry 可能需要：

```text
registered
but
not ready
```

Codex `CoreToolRuntime` 就有可选：

```text
wait_until_ready(...)
```

这说明 Tool Lifecycle 里除了 registered/unregistered，还存在 readiness 状态。

---

# 11. Tool Lifecycle

一个 Tool 可以经历：

```text
Declared
→ Registered
→ Initialized
→ Ready
→ Visible / Deferred
→ Invoked
→ Deprecated
→ Disabled / Removed
```

如果是 MCP：

```text
Server connected
→ tools/list
→ normalize specs
→ register
→ server disconnect
→ mark unavailable / remove
```

Runtime 必须处理 Capability Set 变化。

---

# 12. Registry Snapshot vs Live Registry

一个非常容易忽视的问题：

```text
Step 开始时模型看到了 Tool A / B / C
```

但执行过程中 Registry 动态变成：

```text
A / B / D
```

模型之前可能已经发出：

```text
call C
```

因此需要明确：

> 一次 Turn/Step 使用的是 live registry，还是一个 capability snapshot？

常见思路：

```text
Turn Start
→ freeze / derive Tool Plan
→ model sees plan
→ Router 用同一个 plan 执行
```

这样可以避免：

```text
模型看到了一个 Tool，但执行时它突然消失
```

当然外部 Tool 仍可能真实断线，所以还要 Failure Handling。

---

# 13. Alias 与 Rename

Claude Code `Tool.ts` 当前支持：

```text
aliases?: string[]
```

并有 `toolMatchesName()`：

```text
primary name
or alias
```

这用于：

- Tool 重命名；
- backward compatibility；
- 旧 transcript / call；
- transition window。

但 Alias 不应该无限保留，否则 Registry 会越来越难维护。

---

# 14. 为什么 Registry 还需要 Tool Metadata

Dynamic Discovery 不能只搜索 Tool Name。

可能需要：

```text
name
search hint
description
namespace
keywords
risk level
cost
latency
input type
```

Claude Code `Tool.ts` 中的 `searchHint` 就是：

> 用于 ToolSearch keyword matching 的一行 capability phrase。

这说明 Registry 也是 Capability Search Index 的数据源。

---

# 15. Tool Router 和 Intent Router 不一样

容易混：

```text
Intent Router
→ 决定这个用户任务去哪个系统 / Agent / Model / capability family

Tool Router
→ 已经有具体 Tool Call 后，找到对应执行 Runtime
```

例如：

```text
用户：查订单
↓
Intent / Capability Router
→ order_agent
↓
Model emits get_order
↓
Tool Router
→ OrderServiceToolExecutor
```

第 37 章会讲 Intent Routing。

---

# 16. Tool Discovery 和 Tool Routing 也不一样

```text
Discovery
= 模型当前应该知道哪些能力？

Routing
= 一个已确定的 Tool Call 要交给谁执行？
```

流程：

```text
Huge Registry
→ Discovery
→ Selected Tool Specs
→ Model Tool Call
→ Router
→ Executor
```

这条链是 Tool 能力规模化的核心。

---

# 17. 一个最小 Registry / Router 实现

```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        key = (tool.namespace, tool.name)
        if key in self._tools:
            raise ValueError(f"duplicate tool: {key}")
        self._tools[key] = tool

    def get(self, namespace, name):
        return self._tools.get((namespace, name))


class ToolRouter:
    def __init__(self, registry):
        self.registry = registry

    async def dispatch(self, call, ctx):
        tool = self.registry.get(
            call.tool_name.namespace,
            call.tool_name.name,
        )

        if tool is None:
            return {
                "ok": False,
                "error_type": "unsupported_tool",
                "repairable": True,
            }

        return await tool.execute(call.arguments, ctx)
```

Production 还需要补：

- exposure；
- schema；
- permission；
- readiness；
- hooks；
- trace；
- cancellation；
- concurrency；
- result normalization。

---

# 18. Unsupported Tool 为什么不一定 Fatal

模型可能调用：

```text
old_tool_name
```

Runtime Registry 没有。

这可能只是模型 hallucination 或 capability snapshot 变化。

Codex Registry 对 unsupported tool call 会构造：

```text
FunctionCallError::RespondToModel(...)
```

也就是：

> 允许模型看到这个错误并改路。

这和“Runtime 自己的 Registry invariant 损坏”不同。

---

# 19. External Tool Trust Boundary

外部 MCP / Plugin Tool 接入时，Registry 应考虑：

```text
origin
trust level
namespace
reserved names
schema validation
permission defaults
```

尤其不能：

```text
external tool declares name="shell_command"
→ 静默替换 built-in shell
```

Codex 对 reserved external tool name 的显式拒绝，就是成熟产品对 Capability Supply Chain 风险的处理例子。

---

# 20. Registry 与 Permission 的关系

Registry 只回答：

```text
这个能力存在吗？
执行器是谁？
metadata 是什么？
```

Permission 回答：

```text
这个用户 / 这次调用可以执行吗？
```

所以：

```text
Registered ≠ Authorized
Visible ≠ Allowed
```

即使模型看见 Tool，也可能在具体参数下被拒绝。

---

# 21. AI 应用场景：企业 Agent Tool Hub

假设一个企业 Agent 平台有：

```text
GitHub 80 tools
Jira 40 tools
Slack 30 tools
CRM 60 tools
Internal DB 50 tools
```

总共 260 个。

合理链路：

```text
Registry 保持完整 catalog
↓
根据 tenant / policy 过滤
↓
根据 task 做 discovery
↓
本轮只暴露 10–20 个 relevant specs
↓
模型产生 Tool Call
↓
Router 根据 namespace/origin 分发
↓
Permission + Executor
```

而不是：

```text
260 个完整 JSON Schema 全塞进每次 Context
```

---

# 22. 高频易错点

⚠️ **Registry = tools 字典**  
Demo 可以；Production 还需要 metadata、exposure、version、origin、readiness。

⚠️ **Registered = model visible**  
不一定，Tool 可以 deferred / hidden。

⚠️ **Router = LLM Intent Router**  
Tool Router 更偏已确定 Tool Call 的执行分发。

⚠️ **外部 Tool 重名就覆盖**  
会形成安全与一致性问题。

⚠️ **Tool Set 永远静态**  
MCP、plugin、remote capability 会动态上下线。

---

# 23. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Tool Registry 管理 Runtime 已知能力及其 spec、executor、version、exposure、origin 等 metadata；Tool Router 把模型产生的内部 ToolCall 路由到正确执行器。Registered Tool 不一定全部对模型可见，大规模系统要区分 visible/deferred/hidden，再结合 discovery 做按需暴露。外部 Tool 还要处理 namespace、duplicate、reserved name 和 trust boundary。

## Level 2｜2–3 分钟

> 我会先把 Provider Tool Call normalize 成内部 `{tool_name, call_id, payload}`，再用本 Turn 的 Tool Plan 路由。Registry 要检测 collision，trusted built-in duplicate fail fast，external duplicate/restricted name reject。Capability catalog 和 model-visible specs 分离，这样 500 个 Tool 不必全部进 Context。动态 MCP Tool 还要有 readiness/unavailable 生命周期。最终 Tool 存在不代表有权限，permission 是另一层。

## Level 3｜继续追问

🔍 **为什么要 freeze Tool Plan？**  
避免模型看到的 capability set 与执行时 Router 使用的集合不一致。

🔍 **Deferred Tool 怎么执行？**  
先通过 discovery/tool search 让 Runtime 把相关 Tool 加入当前可见/可路由计划，再调用。

🔍 **External Tool 为什么需要 namespace？**  
避免重名、表达 origin，并为 policy/audit 提供边界。

---

# 24. 本章证据

## HUMAN-A

- `AGENT-019` Tool Lifecycle：10 sources；
- `AGENT-021` Dynamic Tool Discovery：20 sources；
- `AGENT-024` Capability Boundary：34 sources。

## Claude Code

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

- `Tool.ts`：aliases、searchHint、toolMatchesName；
- `QueryEngine.ts`：tools / refreshTools / MCP capability context。

## OpenAI Codex

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

- `codex-rs/core/src/tools/registry.rs`
- `codex-rs/core/src/tools/router.rs`
- `codex-rs/tools/src/tool_executor.rs`

---

# 25. 自测

<details><summary>1. Registry 和 model-visible Tool List 为什么要分开？</summary>

Registry 可以保存完整能力目录，而模型本轮只需要相关 Tool。分开后才能做 deferred discovery、降低 Context Token、按 tenant/policy 过滤，并避免暴露不必要能力。
</details>

<details><summary>2. 为什么外部 Tool 不应该静默覆盖内置 Tool？</summary>

这会让模型看到的能力身份与实际执行逻辑被劫持，产生供应链和权限风险。应该做 namespace、reserved name、duplicate rejection。
</details>

<details><summary>3. Tool Router 与 Intent Router 有什么区别？</summary>

Intent Router 决定请求去哪个 Agent/能力域；Tool Router 在已经拿到具体 ToolCall 后，把它交给对应 Tool Runtime/Executor。
</details>

<details><summary>4. Tool 注册了但没 ready，Runtime 应怎么办？</summary>

显式等待 readiness、返回 unavailable/retryable error，或临时从可见 Tool Plan 中移除；不能假设 registered 就一定可执行。
</details>
