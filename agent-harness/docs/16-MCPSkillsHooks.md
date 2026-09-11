# 16. MCP、Skills、Hooks 与 Capability Extension

Agent 能力越来越多以后，会出现一个新问题：

> **能力从哪里来？怎样发现？怎样按需加载？怎样扩展 Runtime，又不把所有东西都塞进 Context？**

这时经常会同时出现几个词：

```text
Tool
MCP
Skill
Hook
Plugin
Prompt / Rule
```

如果不先分边界，很容易全部叫成“插件”。

这一章把它们放在同一个知识小板块，是因为它们共同解决：

> **Agent Runtime 怎样获得、发现、加载和扩展能力。**

---

## 1. 先给稳定边界

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

Hook 不应该成为 Runtime 主循环本身。

---

# 2. 为什么 Tool 太多会出问题

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

# 3. Capability Catalog

可以先维护一个轻量目录：

```python
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

# 4. Claude Code 源码侧的 Progressive Loading 证据

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

---

# 5. MCP 解决什么标准化问题

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

---

# 6. Tool / Resource / Prompt 为什么要分开

### Tool

模型可以选择执行动作：

```text
query_database(...)
```

### Resource

更接近可读取 Context：

```text
project://schema
```

### Prompt

提供可复用 Prompt 模板 / interaction primitive。

如果全部叫 Tool：

```text
读数据
执行副作用
加载模板
```

权限和生命周期都难表达。

---

# 7. Transport 不是 MCP 的核心价值

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

---

# 8. Skill 与 Tool 的区别

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

---

# 9. Skill Progressive Disclosure

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

# 10. Hook 是什么

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

---

# 11. Codex Hooks 的实现证据

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

# 12. Extension Failure 怎么处理

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

---

# 13. Capability Versioning

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

---

# 14. Security Boundary

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

---

# 15. HUMAN-A 信号

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

# 16. 面试怎么答

## Q：Tool、MCP、Skill、Hook 有什么区别？

🎯 **30 秒回答**：

> Tool 是一次可执行能力；MCP 是 Host/Client/Server 之间标准化暴露 Tool、Resource、Prompt 等能力的协议；Skill 更像可发现、按需加载的程序性知识/资源包，通常会组织多个 Tool 完成一种任务；Hook 是 Runtime 生命周期扩展点，用于审计、验证或扩展。它们不是同一层抽象，也不能全部叫插件。

## Q：Tool 太多怎么处理？

> 不把所有完整 schema 永久塞进 Context，而是建立 capability catalog，让模型先看到轻量 summary，通过 intent/search 发现候选，再按需加载完整 Tool/Skill 定义，并用 eval 验证 discovery recall 和 tool selection accuracy。

---

# 17. 高频易错点

⚠️ **MCP = Agent Framework。** MCP 不负责 Agent Loop。

⚠️ **Skill = Tool。** Skill 更接近程序性任务包。

⚠️ **Hook 可以随便改变 State。** 无约束 Hook 会制造隐藏控制流。

⚠️ **所有 Tool Schema 全量注入更稳。** 规模大时会增加 Context 和选择混乱。

---

# 18. 本章自测

<details><summary>1. 为什么 Progressive Loading 是 Context Engineering 问题？</summary>

因为 Tool/Skill metadata 本身会占 Context；能力规模扩大后，需要只加载与当前任务相关的完整定义，避免成本和选择混乱。
</details>

<details><summary>2. MCP 的 Tool 与普通本地 Tool 最大差异是什么？</summary>

MCP Tool 通过标准协议由外部 Server 暴露，涉及连接生命周期、远程信任和协议兼容；但进入 Runtime 后仍需要相同的 schema、permission、failure、trace 等 Tool Contract。
</details>

<details><summary>3. 为什么 Hook 不应该替代 Runtime 主循环？</summary>

Hook 适合生命周期横切扩展；如果关键控制逻辑散落在 Hook 中，会让执行路径不可见、难恢复、难评测和难推理。
</details>
