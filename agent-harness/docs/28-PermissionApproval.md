# 28｜Human-in-the-loop、Permission 与 Approval

## 1. 三个概念

```text
Permission Policy  当前身份原则上能做什么
Approval           这一次动作是否需要人工确认
Sandbox            即使获批，环境物理允许做什么
```

本章先讲前两个。

## 2. Permission Context

Claude Code `ToolPermissionContext` 直接区分 allow / deny / ask rules 和 permission mode，是成熟 Runtime 很直观的实现证据。

Policy 可综合：

```text
user / tenant
resource
action
tool risk
arguments
environment
```

## 3. Approval 是可暂停的 Runtime State

OpenAI Agents SDK HITL 的模式很清晰：

```text
tool call requested
→ interruption
→ serialize RunState
→ human approve / reject
→ resume
```

这比“弹一个 confirm()”更接近长任务系统。

## 4. Approval Scope

要问：

- only this call？
- same tool for rest of run？
- same resource？
- permanent account permission？

默认越窄越安全。

## 5. Approval TOCTOU

用户批准的是：

```text
rm ./tmp/output.log
```

Resume 时参数不能悄悄变成别的 path。应绑定 call_id + normalized args hash。

## 🎯 面试

Permission 是 policy，Approval 是具体动作的人机决策。高风险 Tool 我会让 Runtime 进入 WAITING_APPROVAL，持久化 call ID 和参数，审批后 resume 原 Run；Approval 必须绑定实际参数，避免恢复后发生 TOCTOU。

<details><summary>自测：用户批准“这个 Tool”是否意味着之后所有参数都可自动执行？</summary>

不一定。批准范围应显式定义；高风险场景通常只批准当前 call 或受限资源范围。
</details>
