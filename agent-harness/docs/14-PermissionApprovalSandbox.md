# 14｜Permission、Approval、HITL 与 Sandbox

> 本章合并旧 `PermissionApproval` 与 `SandboxEnvironment`。必须先把四个概念拆开：**Capability Selection、Permission Policy、Human Approval、Sandbox Enforcement 不是一回事。**

## 1. 四层边界

```text
Capability
模型想用哪个 Tool？

Permission
规则上是否允许？

Approval / HITL
这一次是否必须让人确认？

Sandbox
即使代码恶意或出错，环境物理上能碰到什么？
```

一个动作被 Permission Allow，不代表它可以逃出 Sandbox。

## 2. Permission Policy

可以基于：

```text
tool
action
resource
tenant
user role
path
network domain
risk level
runtime mode
```

返回：

```text
allow
deny
ask
```

## 3. Approval 应用在哪些操作

典型高风险：

```text
生产写操作
删除
发送外部消息
发布
付款
修改权限
执行未知命令
访问敏感数据
```

Approval 是一次执行决策，不应该永久提升模型权限。

## 4. HITL = Pause / Resume Primitive

正确流程：

```text
Tool requested
→ Runtime detects approval required
→ persist interruption state
→ pause Run
→ human approves / rejects
→ resume from exact boundary
```

所以 HITL 不只是弹一个确认框，它依赖 Durable Run State。

## 5. Sandbox

Sandbox 约束执行环境：

```text
filesystem roots
network access
process privileges
syscalls
container / VM boundary
time / memory / CPU quota
```

目标不是保证 Agent 永远不犯错，而是缩小 blast radius。

## 6. Permission 与 Sandbox 为什么都需要

如果只做 Permission：

```text
批准 shell command
→ shell 能访问整个机器
```

风险仍很大。

如果只做 Sandbox：

```text
环境虽然被隔离
→ 但 Agent 仍可能删除 workspace 内重要文件
```

所以：

```text
Policy controls intent-level authority
Sandbox controls environment-level capability
```

## 7. Source Evidence

Claude Code 固定快照的 `useCanUseTool.tsx` 会根据 Permission Decision 处理 `allow / deny / ask`，并考虑 aborted state、interactive approval、automated checks 等。

Codex 固定快照的 `SandboxPolicy` 能表达 read-only、workspace-write、external sandbox、network access 等执行边界。

Anthropic 关于 Claude Code sandboxing 的官方工程文章也明确强调：Sandbox 与 Permission Prompt 是不同安全层。

## 8. HUMAN-A

`AGENT-028 Permission / HITL / Sandbox` 当前有 20 个独立来源，且经常与 Tool Failure、Long-running、Prompt Injection 一起追问。

## 9. 🎯 面试回答

> Permission 决定规则上能不能做，Approval 决定这一次是否需要人确认，Sandbox 决定执行环境实际上能访问什么。Production Agent 应把三层分开：高风险 Tool 先过 Policy，必要时把 Run Durable Pause 等待 HITL，真正执行仍放在最小权限的 Sandbox 里限制 filesystem、network、process 和资源配额。

<details><summary>自测：已经有 Docker 容器，为什么还需要 Permission？</summary>

容器只能限制执行环境范围，不能判断“用户是否允许删除这个 workspace 文件、是否允许发邮件或是否应该访问某个业务对象”。业务授权仍需要 Permission / Approval。
</details>