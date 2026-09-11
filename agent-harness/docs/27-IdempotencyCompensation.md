# 27｜Idempotency、External Side Effect 与 Compensation

## 1. Agent 最危险的恢复问题

```text
Tool succeeded externally
→ Runtime crashed before recording success
→ Resume sees pending
→ Tool runs again
```

这不是 LLM 问题，是分布式系统正确性问题。

## 2. Idempotency Key

可以用：

```text
run_id + logical_action_id
```

而不是每次 retry 生成新的随机 request ID。

外部服务支持时，把同一个 idempotency key 带过去。

## 3. Side-effect State Machine

```text
PLANNED
→ STARTED
→ SUCCEEDED / FAILED / UNKNOWN
```

`UNKNOWN` 很重要：网络断开后不知道服务端有没有成功。

## 4. Reconciliation

UNKNOWN 时先查询外部状态，而不是盲重放。

```text
lookup by idempotency key / resource id
→ decide already_done / retry / human review
```

## 5. Compensation

不是所有动作可回滚。可以设计 Saga 风格补偿：

```text
create reservation
→ payment fails
→ cancel reservation
```

但补偿本身也可能失败，要进入 state/trace。

## 🎯 面试

Checkpoint 与外部副作用无法天然原子。我会给 logical action 稳定 idempotency key，记录 side-effect state，Crash 后先 reconcile；不可幂等动作则要人工确认或 compensation，而不是简单 retry。

<details><summary>自测：为什么“Tool 返回成功后再写 checkpoint”仍有问题？</summary>

因为 Tool 成功和 checkpoint 写入之间仍有 crash window。恢复时必须能识别该动作是否已完成。
</details>
