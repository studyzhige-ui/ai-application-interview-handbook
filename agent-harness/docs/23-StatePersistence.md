# 23｜State Persistence 与 Event Log

## 1. 为什么 Agent State 必须持久化

只存在内存：

```text
process crash → task disappears
```

长任务、审批等待、远程 Tool 都要求 durable state。

## 2. Snapshot vs Event Log

### Snapshot

直接存当前状态：恢复快。

### Event Log

存发生过的事件：可 replay / audit。

Production 常组合：

```text
Event Log = truth/history
Snapshot = fast restore point
```

## 3. 写入边界

每个 Tool Step 可以：

```text
persist intent
→ execute
→ persist result
```

但外部副作用与 DB 写入无法天然原子，需要后续幂等/补偿。

## 4. State Schema Version

Runtime 升级后旧 checkpoint 仍可能 resume。

因此要考虑：

```text
state_version
migration
backward compatibility
```

## 5. Storage Choice

MySQL / Postgres、event log、object store、Redis 各有角色，不要因为“Agent State”就全放 Redis。

## 🎯 面试

长任务 State 要 durable。常见设计是 append event + periodic snapshot：event 提供审计/replay，snapshot 提供快速恢复；同时给 State schema 做 versioning。外部副作用不能假设和 checkpoint 原子提交，需要幂等/ledger。

<details><summary>自测：为什么只存最后 messages 不够 Resume？</summary>

缺少结构化任务状态、Tool side-effect status、approval、artifact/version 等 Runtime truth，模型可能无法判断哪些动作已真实完成。
</details>
