# 36｜Hooks、Plugins 与 Extensibility

## 1. Hook 是什么

Hook 是 Runtime 生命周期上的扩展点：

```text
pre_tool
post_tool
pre_compact
post_compact
session_start
run_end
```

Codex 源码明确存在 pre/post compact hook，并支持 command、MCP tool、prompt、agent 等 handler 类型。

## 2. Hook 为什么有价值

核心 Runtime 不需要硬编码所有企业需求：

- audit；
- policy；
- telemetry；
- context enrichment；
- custom validation。

## 3. Hook 的风险

Hook 也是代码：

```text
slow hook → 整个 run 变慢
failed hook → 是否阻断？
recursive hook → loop
untrusted plugin → security
```

必须定义 execution mode、timeout、failure policy。

## 4. Plugin

Plugin 通常是更大的扩展包，可能注册：

```text
tools
hooks
skills
commands
resources
```

不要把 Plugin 与 Hook 等价。

## 5. Stable Core

好的 Runtime：

```text
small stable core
+ explicit extension interfaces
```

而不是每个新业务都 fork Harness。

## 🎯 面试

Hook 是生命周期扩展点，Plugin 是能力包。Hook 需要 timeout、failure policy、trust 和 recursion control；它能让审计、policy、context enrichment 等横切需求不侵入 Agent Loop 核心。

<details><summary>自测：pre_tool hook 可以替代 Permission Engine 吗？</summary>

不建议。Hook 可以补企业策略，但核心权限最好有稳定的一等模型，避免关键安全语义依赖可选扩展。
</details>
