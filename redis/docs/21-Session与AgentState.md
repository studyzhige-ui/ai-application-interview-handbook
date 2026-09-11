# 21｜Session、Conversation 与 Agent State Store 边界

Redis 在 AI 应用里非常常见的一类用途是：

```text
Session
Conversation Hot State
Agent Runtime State
```

这三者看起来都叫“状态”，但可靠性要求和生命周期并不一样。

---

## 1. Session：共享登录状态

多实例 FastAPI：

```text
Client
 ↓
Load Balancer
 ├─ API-1
 ├─ API-2
 └─ API-3
```

如果 Session 只存在 API-1 内存：

```text
下一次请求打 API-2
→ 找不到 Session
```

Redis 让 Session 变成共享状态：

```text
session:{tenant}:{session_id}
```

常见字段：

```text
user_id
roles
created_at
last_seen
csrf/state
```

再配 TTL。

---

# 2. Session TTL 怎么设计

通常有：

```text
Absolute Expiration
Sliding Expiration
```

例如：

```text
最多 7 天
+
30 分钟不活跃失效
```

如果每次请求都刷新 TTL：

- 读变写；
- Redis 写 QPS 上升；
- Hot Session 更热。

所以可做：

```text
每隔 N 分钟才刷新
```

而不是每个 HTTP Request 都改 TTL。

---

# 3. Auth Cache 要特别谨慎

例如：

```text
user → roles / permissions
```

缓存后权限发生变更：

```text
管理员撤销权限
但 Redis 里还是旧权限
```

这不是普通“页面显示旧昵称”的问题，而可能是安全问题。

所以 Auth Cache 需要：

- 较短 TTL；
- Version / revoke signal；
- Source of Truth；
- Fail-closed/Fail-open 设计。

---

# 4. Conversation Hot State

完整聊天历史可能很长。

不建议：

```text
conversation:{id}
→ 一个 List 永久塞所有 Message
```

因为会形成 BigKey。

更合理：

```text
MySQL / Durable Store
→ 保存完整历史

Redis
→ 最近窗口 / Hot Metadata / Cursor
```

例如：

```text
conversation:{id}:recent
conversation:{id}:summary
conversation:{id}:cursor
```

---

# 5. Agent Runtime State

一次 Agent Run 可能有：

```text
status
current_step
worker_owner
heartbeat
lease
retry_count
stream_cursor
```

Redis 很适合做：

```text
Hot Mutable State
```

因为更新频繁，且多个 Worker / API 需要共享。

---

# 6. Agent State Store ≠ Agent Memory

这是面试很容易混的概念。

## Runtime State

回答：

```text
这个 Run 现在执行到哪？
谁在处理？
当前 step 是什么？
```

## Memory

回答：

```text
Agent 应该记住什么用户事实？
过去任务经验怎样召回？
```

Redis 可以作为两者的 Storage Backend，但：

> **存储介质不等于上层语义。**

Memory Architecture Primary 属于 Agent Harness。

---

# 7. Redis State 能不能作为唯一 Checkpoint

要先问恢复目标。

如果：

```text
Redis 故障
→ 允许 Run 失败重跑
```

可以更激进。

如果：

```text
Agent 已执行昂贵 Tool / 外部副作用
→ 必须精确 Resume
```

仅靠普通 Redis 临时状态可能不够。

你要考虑：

- Persistence；
- Replication loss window；
- Durable Checkpoint；
- Side-effect Idempotency；
- Version / State Machine。

这些执行语义归 Agent Harness / System Design。

---

# 8. 多租户隔离

Key 必须包含 Tenant Boundary：

```text
session:{tenant}:{sid}
conversation:{tenant}:{cid}
agent_run:{tenant}:{run_id}
```

但 Key Namespace 只是第一层。

仍然需要：

```text
AuthN/AuthZ
→ 应用校验 tenant ownership
```

不能认为：

> “Key 里有 tenant_id 就安全。”

---

# 9. Serialization 怎么选

常见：

```text
String JSON
Hash fields
MessagePack / binary
```

Trade-off：

| 方案 | 优点 | 缺点 |
|---|---|---|
| JSON String | 简单、跨语言 | 整体改写、体积较大 |
| Hash | 字段级更新 | Schema/Field 管理更复杂 |
| Binary | 紧凑 | 可读性/调试差 |

不要为了“性能”过早选难维护的编码。

---

# 10. Session / State 失效时系统怎么降级

## Session

Redis 不可用：

```text
可以短暂拒绝登录态请求
或回到 Token 自包含认证
```

## Conversation Hot State

```text
回源 Durable History
```

## Agent Runtime State

可能：

```text
Run 暂停
→ 等 Redis 恢复
```

而不是默认继续执行，避免双 Worker / 状态错乱。

所以不同 Key Namespace 应该有不同 Failure Policy。

---

# 11. 面试怎么答

## Q：为什么 Redis 常用于 Session？

🎯 **建议回答：**

> 多实例服务不能依赖单进程本地 Session，Redis 提供低延迟共享状态和 TTL，很适合作为 Session Store。但要设计 Sliding/Absolute TTL、多租户隔离、权限变更失效，以及 Redis 故障时的登录降级策略。

## Q：Redis 里的 Agent State 和 Agent Memory 是一回事吗？

> 不是。Agent State 更偏一次 Run 的执行状态，例如 step、owner、lease、retry；Memory 是跨轮/跨任务保留和召回的信息语义。Redis 只是可能的 Storage Backend，真正的 Memory Lifecycle 属于 Agent Harness。

---

# 12. 本章自测

<details>
<summary>1. 为什么完整 Conversation History 不适合无限塞一个 Redis List？</summary>

会形成 BigKey，带来内存、全量读取、删除、复制和迁移风险；长期历史更适合 Durable Store，Redis 保存 Hot Window/Metadata。

</details>

<details>
<summary>2. Auth Cache 为什么比普通 Profile Cache 更敏感？</summary>

权限撤销如果被陈旧缓存延迟，会造成越权风险，因此 TTL、版本、主动失效和 Fail Policy 更严格。

</details>

<details>
<summary>3. 为什么 Redis Runtime State 不一定等于 Durable Checkpoint？</summary>

Redis 可能有 Failover/Replication/Persistence 窗口，且 Checkpoint 还要与外部 Side Effect、State Machine、Resume 一致性配合。

</details>
