# 04｜API、Data Model 与 State Ownership

一个系统设计如果说不清：

> **状态到底属于谁、谁能修改、谁只是缓存或派生副本？**

后面的 Consistency、Retry、Cache、Failover 基本都会乱。

---

## 1. API 先表达业务，不要先暴露存储细节

例如创建任务：

```http
POST /tasks
```

比：

```http
POST /mysql/task_table/insert
```

更合理。

API Contract 应围绕：

```text
Resource
Command
Status
Error
Idempotency
Pagination / Cursor
Version
```

设计。

---

# 2. 先画核心实体

例如 Long-running Agent：

```text
User
Workspace
AgentRun
AgentStep
ToolCall
Checkpoint
Artifact
```

再定义关系：

```text
Workspace owns AgentRun
AgentRun has many AgentStep
AgentStep may create ToolCall
AgentRun points to latest Checkpoint
```

这比直接说“用 Redis 存状态”更重要。

---

# 3. Source of Truth 是什么

可以把它理解成：

> **当多个副本冲突时，最终以谁为权威。**

例如 RAG：

```text
Object Storage / Business DB
= Source of Truth

Vector DB
= Derived Retrieval Index

Redis
= Cache / Hot State
```

如果 Source of Truth 不明确：

```text
Redis 有值
MySQL 也有值
Vector DB 还有版本
```

发生冲突时没人知道听谁的。

---

# 4. Primary State、Derived State、Ephemeral State

## Primary State

业务事实：

```text
订单
余额
权限
任务最终状态
```

## Derived State

可从 Primary 重建：

```text
Cache
Search Index
Vector Index
Materialized View
Ranking Snapshot
```

## Ephemeral State

短生命周期执行状态：

```text
Session
Lease
Progress
Temporary Buffer
```

不同状态的 Durability / Consistency 要求不同。

---

# 5. State Ownership 比“数据库选型”更重要

例如订单系统：

```text
Order Service
→ owns order lifecycle
```

Inventory Service：

```text
→ owns inventory
```

不要让两个服务都直接修改同一业务状态，否则：

```text
谁校验 invariant？
谁发事件？
谁补偿？
```

都会模糊。

---

# 6. 一个写请求要写清 State Transition

不要只画：

```text
API → DB
```

例如 Notification：

```text
CREATED
→ QUEUED
→ SENDING
→ SENT
       ↘ FAILED_RETRYABLE
       ↘ FAILED_FINAL
```

状态机能直接帮助回答：

- 重复 Worker 怎么办；
- Resume 从哪里开始；
- 哪些状态允许 Retry；
- 用户看到的状态是什么。

---

# 7. API 的 Idempotency Contract 要尽早定义

创建资源时：

```http
POST /orders
Idempotency-Key: abc
```

服务端需要决定：

```text
同一个 Key + 同参数
→ 返回同一结果

同一个 Key + 不同参数
→ Reject
```

Stripe 的公开 API 就使用这种思路来支持安全重试。

Idempotency 不是最后加一个 Redis Lock 就完成，而是 API Contract 的一部分。

---

# 8. Pagination 也属于 API/Data Model 联合设计

如果列表接口：

```http
GET /events?offset=1000000
```

随着数据增长可能越来越慢。

如果业务适合：

```text
cursor = (created_at, id)
```

可以使用 Keyset / Cursor Pagination。

这要求 API 与索引设计一起考虑。

---

# 9. Schema Version / API Version

长期系统一定会演进。

例如 Tool Result 从：

```json
{"text": "..."}
```

升级到：

```json
{"text": "...", "citations": [], "version": 2}
```

需要考虑：

```text
Old Client
Old Event
Old Checkpoint
Old Worker
```

是否还能读取。

System Design 不一定每题都展开 Migration，但成熟设计应该意识到 Version 是状态契约的一部分。

---

# 10. 多租户系统一定要把 Tenant 放进数据模型

不要只在 UI 层说：

> 当前登录用户属于 tenant A。

数据层至少要能回答：

```text
tenant_id 在哪里？
Partition / Index 是否带 tenant？
Unique Key 是全局还是 tenant-scoped？
Cache Key 是否隔离？
Trace 是否带 tenant？
```

否则很容易跨租户污染。

---

# 11. AI Application 的特殊状态

还要显式建模：

```text
model_version
prompt_version
embedding_version
index_generation
agent_run_id
checkpoint_version
permission_scope
```

因为 AI 系统的输出不仅依赖业务数据，也依赖模型和 Pipeline 版本。

Bad Case Replay 如果没有这些版本信息，很难复现。

---

# 12. 🎯 面试怎么答

> 我会先定义 API 和核心实体，再明确每类状态是 Primary、Derived 还是 Ephemeral，并指定唯一 State Owner。写路径用状态机表达，而不是只画“服务写数据库”。对于创建类 API，我会尽早定义 Idempotency Contract；多租户系统则让 tenant_id 进入 Primary Key、Cache Key、Filter 和 Trace。AI 系统还需要版本化 Model、Prompt、Embedding、Index 和 Checkpoint，否则无法回放和迁移。

---

# 13. 本章自测

<details><summary>1. 为什么 Cache 不应该默认成为 Source of Truth？</summary>
Cache 主要用于性能，通常允许失效、重建和淘汰；如果把它当权威状态，需要额外承担持久性、一致性和恢复责任。
</details>

<details><summary>2. 为什么状态机有助于 Retry？</summary>
它让系统知道当前执行到了哪个状态、哪些步骤已经产生副作用，从而决定重试、Resume 或补偿，而不是整条流程重新执行。
</details>

<details><summary>3. 为什么 AI Bad Case 需要记录版本？</summary>
相同 Query 在不同 Model、Prompt、Index、Embedding 版本下可能得到不同结果；没有版本就无法复现。
</details>
