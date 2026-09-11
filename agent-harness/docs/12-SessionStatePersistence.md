# 12｜Session / State / History / Persistence 与 Tenant Isolation

> 本章合并旧 `SessionStateHistory` 与 `StatePersistence`，并纳入 Multi-tenant State Isolation。核心问题是：**Agent Runtime 的“执行事实”应该怎样保存，且不能和 Chat History / Memory 混在一起。**

## 1. 四个对象先分清

```text
Session / Thread
= 长期交互容器

State
= 当前执行事实

History
= 已发生 Event / Message 记录

Memory
= 未来可能被召回的信息
```

State 可能从 History 重建，但二者不是一回事。

## 2. State 最少应该包含什么

```text
run status
current goal / constraints
current step
selected artifacts
pending tool calls
approval state
budget usage
checkpoint/version
```

不要只保存一串 Messages。

## 3. Snapshot vs Event Log

### Snapshot

直接保存当前 State。

优点：恢复快。

### Event Log

保存：

```text
RunStarted
ToolCalled
ToolFinished
GoalUpdated
CheckpointCreated
...
```

优点：可审计、可 Replay。

成熟方案常是：

```text
Event Log + Periodic Snapshot
```

## 4. Persistence Boundary

哪些必须 Durable：

```text
user-visible task status
external side-effect ledger
checkpoint
approval decision
artifact reference
critical runtime event
```

哪些可以只放内存：

```text
short-lived cache
streaming buffer
local temporary computation
```

## 5. Multi-tenant Isolation

一个生产 Agent 平台必须让下面这些对象都带 Scope：

```text
tenant_id
user_id
session_id
run_id
```

隔离对象包括：

- Context；
- Memory；
- Tool Permission；
- Artifact；
- Checkpoint；
- Trace；
- Cache。

不能只在 API 入口鉴权一次，就默认后续 Tool / Memory 都安全。

## 6. Tenant 泄露常见路径

```text
shared vector memory missing tenant filter
artifact path 可猜
cache key 没带 tenant
resume 时加载错 session
subagent 继承过宽 permission
```

因此 Tenant Scope 应进入 Runtime Contract，而不是仅靠 Prompt 提醒模型。

## 7. Resume 之前为什么要验证 State Version

持久化几小时后：

- Tool Schema 变了；
- Model Provider 变了；
- Permission Policy 变了；
- Project branch 变了。

所以 State / Checkpoint 应带：

```text
schema_version
capability_snapshot
workspace_version
policy_version
```

恢复时先做兼容性检查。

## 8. HUMAN-A

- `AGENT-017` 多用户 / 多角色 / Tenant 隔离：10 来源；
- `AGENT-027` Checkpoint / Persistence / Resume：12 来源。

## 9. 🎯 面试回答

> Session 是长期交互容器，State 是当前执行事实，History 是过去事件，Memory 是未来可召回信息。生产 Runtime 不应该只存 Chat History，而应把关键 State、Approval、Artifact、Side-effect Ledger 和 Checkpoint Durable 化；最好结合 Event Log 与 Snapshot。多租户系统里这些对象都必须带 tenant/user scope，并在 Memory、Cache、Artifact、Tool Permission、Resume 每一层持续隔离。

<details><summary>自测：为什么只靠 `session_id` 不能保证多租户隔离？</summary>

因为 session_id 可能被误用、猜测或跨系统丢失；所有持久化对象与查询都应显式带 tenant scope，并由 Runtime/Storage Policy 强制过滤。
</details>