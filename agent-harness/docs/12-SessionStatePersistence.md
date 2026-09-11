# 12. Session、State、History、Persistence 与 Tenant Isolation

Agent 系统一旦不再是“一次请求、一次回答”，就必须明确：

> **一次会话到底是什么？哪些状态跨 Turn 保存？哪些只是临时 Context？多用户之间怎样隔离？**

如果只写：

```text
conversation_id -> Redis
```

远远不够。

这一章的目标是建立 Runtime State Plane 的最小模型。

---

## 1. Session 是什么

Session 可以理解为：

> **一段连续交互的 Runtime 容器。**

至少通常会有：

```text
session_id
user / tenant / workspace identity
created_at
last_active_at
runtime config snapshot
history / event reference
current run state
memory namespace
permission context
```

Session 不等于一条聊天记录，也不等于一个 HTTP connection。

---

# 2. Run / Turn / Step 再复习

建议保持分层：

```text
Session
└─ Run
   └─ Turn
      └─ Step / Model / Tool Interaction
```

不同产品具体命名会不同，但课程需要保持“层级事实”。

Claude Code Source Index 明确说明：

- 一个 conversation 一个 `QueryEngine`；
- `submitMessage()` 开启新 turn；
- messages、file cache、usage 等状态跨 turn 保留。

Codex Source Index 也确认：

```text
Session
└─ Turn
   └─ Step / Model Request / Tool Interaction
```

这说明“Session / Turn / Step”不是纯教学想象，而是成熟 Runtime 中真实存在的状态层级。

---

# 3. State 应该保存什么

Runtime State 的目标不是“保存所有文本”，而是支持：

```text
下一步正确决策
恢复
取消
审计
并发控制
```

可以分几类。

## 3.1 Identity State

```text
session_id
run_id
turn_id
current_step_id
```

## 3.2 Control State

```text
status
current_goal
plan
budget
retry_count
active_tool_call
```

## 3.3 Environment State Reference

```text
workspace_id
sandbox_id
artifact ids
file generation
```

## 3.4 Safety State

```text
permission mode
approved action ids
policy version
```

## 3.5 Progress State

```text
completed steps
pending steps
blocked reason
```

---

# 4. History 应该是事件流，而不是“一个超长字符串”

更稳妥的模型：

```text
Event 1: UserMessage
Event 2: ModelOutput
Event 3: ToolCall
Event 4: ToolResult
Event 5: Approval
Event 6: StateTransition
```

每条事件有：

```text
event_id
session_id
run_id
turn_id
timestamp
type
payload
correlation_id
```

这样 Trace、Replay、Checkpoint 才有可靠基础。

---

# 5. Snapshot 与 Event Log 怎么配合

如果每次恢复都从第 1 条 Event 重放：

```text
session 越长
→ replay 越慢
```

一种常见设计是：

```text
Durable Event Log
+
Periodic State Snapshot
```

恢复时：

```text
load latest snapshot
→ replay newer events
```

这里是通用架构模式，不声称 Claude Code / Codex 一定使用同样的数据存储实现。

---

# 6. Persistence 不等于把 Context 存下来

错误思维：

```text
把当前 prompt JSON 存 DB
→ resume 时再发给模型
```

问题是 Prompt 只是 State 的一个投影。

真正需要持久化的可能还有：

```text
side effects
artifact refs
tool call correlation
approval
budget
workspace version
pending task
```

因此：

> **Context 是可重新编译的 View；State 才是 Runtime 的事实。**

---

# 7. Session Store 选什么

不能只问：

> Redis 还是 MySQL？

要先问数据语义。

### Redis 适合

```text
高频 transient state
TTL session cache
lease / heartbeat
fast coordination
```

### MySQL / Durable DB 适合

```text
long-term session metadata
durable run record
billing / ownership
high-value audit facts
```

### Object / Artifact Store

适合：

```text
large logs
file snapshots
model/tool artifact
```

最终通常是组合，而不是一库包办。

---

# 8. Tenant Isolation 为什么必须进入 State Schema

多租户系统不能只是：

```text
WHERE user_id = ?
```

在一个业务代码分支里“记得加”。

建议所有核心 State Object 自带：

```text
tenant_id
workspace_id
user_id
```

并在：

```text
storage key
query filter
cache key
tool permission
artifact path
trace scope
```

都显式传播。

对应 HUMAN-A `AGENT-017 Multi-tenant State Isolation`。

---

# 9. Session Hijack / Cross-tenant Pollution

经典事故：

```text
cache key = session:{session_id}
```

如果 session_id 不是全局不可猜且查询没有 tenant boundary：

```text
Tenant A
→ 构造 B 的 session id
→ 读到 B state
```

更稳：

```text
session:{tenant_id}:{session_id}
```

但 Key 设计仍不能替代服务端授权检查。

---

# 10. Concurrency：同一个 Session 同时来两个请求怎么办

例如：

```text
Request A: “继续执行任务”
Request B: “先停止，改需求”
```

如果两个 Worker 同时修改 State：

```text
Lost Update
Out-of-order Event
Duplicate Tool
```

可以使用：

```text
optimistic version
single owner lease
serialized event append
per-run queue
```

关键是：

> **同一 Run 的 State Transition 必须有并发协议。**

---

# 11. State Version 为什么重要

伪代码：

```text
read state version=42
compute update
write where version=42
→ success: version=43
→ fail: someone else updated
```

这样可以发现 Lost Update。

对于长任务还可以维护：

```text
state_generation
checkpoint_generation
instruction_generation
```

后面 Resume 时很重要。

---

# 12. Cold Resume 与 Warm Resume

可以区分：

## Warm Resume

```text
worker 还在
in-memory objects 还在
```

## Cold Resume

```text
进程已经重启
只剩 durable state
```

如果系统只支持 Warm Resume：

```text
真正 crash 后仍恢复不了
```

所以 Production 设计要问：

> **哪些运行事实只在内存，哪些必须 durable？**

Codex Source Index 对 Thread Instructions 也明确区分 warm resume、cold resume / offline fork、live fork 的 instruction snapshot/provider 继承边界，这说明 Resume 不是简单“重新加载聊天”。

---

# 13. Session Retention / Deletion

Session 也有生命周期：

```text
active
idle
archived
expired
deleted
```

需要定义：

- 保留多久；
- 是否允许用户删除；
- artifact 是否联动删除；
- trace / billing 是否有独立保留规则；
- Memory 是否跟 Session 一起删除。

这些不能都靠一个 Redis TTL 解决。

---

# 14. HUMAN-A 信号

本章主要承接：

- `AGENT-017`：多用户 / 多 Tenant 的 Memory、Context、Session 与权限隔离；
- `AGENT-027` 的前置：Checkpoint / Persistence / Resume；
- `AGENT-004` 的 Event Model 基础。

真实面试中常见追问：

```text
Session 存哪？
多实例怎么恢复？
多个用户怎么隔离？
Context 和 State 是一回事吗？
```

---

# 15. 面试怎么答

## Q：Agent Session / State 怎么设计？

🎯 **30 秒回答**：

> 我会把 Session 当作一段连续交互的 Runtime 容器，而不是聊天文本。State 保存当前 goal、status、budget、active tool、progress、workspace 和 permission 等执行事实；History 用结构化 event 记录已发生事情；Context 是从这些持久状态和其它来源编译出来的 model view。多实例场景要支持 durable persistence、版本控制和 cold resume，多租户要让 tenant/workspace identity 贯穿存储 key、query、tool permission、artifact 和 trace，而不是只靠 Prompt 隔离。

---

# 16. 高频易错点

⚠️ **Session = Chat History。** Session 还包含 Runtime State / Config / Ownership。

⚠️ **Context 存下来就是 Checkpoint。** Context 只是 View，不足以恢复外部副作用和执行位置。

⚠️ **多租户隔离靠 Prompt。** 必须由 Storage / Permission enforce。

⚠️ **同一个 Session 并发请求自动安全。** 需要版本或 Owner 协议。

---

# 17. 本章自测

<details><summary>1. 为什么 History 更适合做结构化 Event Log？</summary>

因为 ToolCall、ToolResult、Approval、StateTransition 等事件需要独立身份和关联关系，才能支持 Trace、Replay、Debug 与 Checkpoint。
</details>

<details><summary>2. Cold Resume 需要比 Warm Resume 多保存什么？</summary>

进程内对象全部丢失，所以必须有足够 durable state 来重建运行：执行位置、状态、artifact、side effect、approval、instruction/context source version 等。
</details>

<details><summary>3. 为什么 Context 不应该作为唯一 Source of Truth？</summary>

Context 会裁剪、压缩、重排，是模型输入视图；Runtime 正确性依赖结构化 State 和 History，不能只依赖自然语言 Prompt。
</details>
