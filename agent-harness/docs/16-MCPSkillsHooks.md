# 16｜MCP、Skills、Hooks 与 Capability Extension

> 本章合并旧 `MCP`、`SkillsCapability`、`HooksPlugins`，并纳入 Progressive Loading。目标是把几种经常被混成“插件”的机制真正分开。

## 1. 四个概念先分清

```text
Tool
= 一次可执行能力

MCP
= Host 与外部 Tool / Resource / Prompt 的标准连接协议

Skill
= 可发现、可按需加载的程序性知识 / 资源 / 脚本包

Hook
= Runtime 生命周期扩展点
```

它们可以组合，但不是同一个抽象。

## 2. MCP 的 Host / Client / Server

```text
Agent Host
└─ MCP Client
   ↔ MCP Server
      ├─ Tools
      ├─ Resources
      └─ Prompts
```

官方规范强调三类 Primitive 的控制边界：

```text
Prompt     user-controlled
Resource   application-controlled
Tool       model-controlled request
```

进入 Host 后，MCP Tool 仍然要经过本地：

```text
normalize
→ registry
→ permission
→ approval
→ sandbox
→ trace
```

MCP 不绕过 Runtime Policy。

## 3. Skill 是什么

Skill 更像：

```text
instructions
+ examples
+ scripts
+ references
+ assets
```

它表达“怎样完成某类工作”的程序性能力。

Skill 可以调用 Tool，也可以包含 Prompt/资源；但它不是 Tool Protocol。

## 4. Progressive Disclosure

大量 Skill / Tool 时：

```text
只加载名称 / summary
→ 根据任务发现候选 capability
→ 再加载详细 instructions / schema / asset
```

这能避免所有能力一次性占满 Context。

## 5. Hook

Hook 是：

```text
Runtime Event
→ Extension Handler
```

例如：

```text
pre_tool_use
post_tool_use
pre_compact
post_compact
run_started
run_finished
```

用途：

- audit；
- policy；
- telemetry；
- input rewrite；
- custom context；
- integration。

Hook 不应该反过来成为主 Loop。

## 6. Plugin 是产品包装词

Plugin 在不同产品里可能打包：

```text
Tool + MCP Server + Skill + Hook + UI
```

因此面试里不要把“Plugin”当稳定底层协议，而要拆出具体 primitive。

## 7. 源码证据

Claude Code 固定快照有 MCP connections、dynamic skill discovery、Tool `searchHint` 等；Codex 固定快照中 MCP catalog 与 Hook handler 可以进入 extension runtime，Hook handler kind 也不仅限于 command。

稳定抽象是：

```text
Capability Catalog
→ Discovery
→ Progressive Loading
→ Runtime Policy
→ Invocation
```

## 8. HUMAN-A

- `AGENT-023` MCP：20 来源；
- `AGENT-024` Skill / Tool / MCP / Workflow 边界：34 来源；
- `AGENT-025` Skill Progressive Disclosure：10 来源。

## 9. 🎯 面试回答

> MCP 是 Host/Client/Server 协议，用于标准化 Tools、Resources、Prompts 的外部接入；Tool 是一次可执行能力；Skill 是可发现、可加载的程序性知识包；Hook 是 Runtime 生命周期扩展点。Tool/Skill 数量大时应做 Progressive Discovery/Loading，而不是全部注入 Context。外部 MCP Tool 进入 Host 后仍然必须经过本地 Permission、Sandbox 和 Trace。

<details><summary>自测：MCP Server 声明某 Tool 后，为什么 Host 仍需要 Permission？</summary>

因为 MCP 负责能力协议，不负责当前用户/tenant 是否有权执行，也不定义本地高风险动作审批和 Sandbox Policy。
</details>