# 22. Pub/Sub、Streams 与消息边界

Redis 不只做 Cache，也提供消息相关能力。

但要先分清：

```text
Pub/Sub
≠
Streams
≠
专业 MQ / Event Platform
```

它们的消息语义完全不同。

---

## 1. Pub/Sub：在线广播

Publisher：

```text
PUBLISH model-config updated
```

Subscriber：

```text
SUBSCRIBE model-config
```

消息到达时，当前在线订阅者可以收到。

直觉：

```text
广播通知
```

而不是：

```text
可靠持久消息队列
```

---

# 2. Pub/Sub 最大边界：离线消息不会帮你长期保存

如果 Subscriber 当时不在线：

```text
消息发过了
→ 它后来上线
→ 不会自动 Replay 之前消息
```

因此 Pub/Sub 更适合：

- Cache Invalidation Signal；
- 配置变更通知；
- 在线事件广播；
- 非关键实时通知。

不适合：

```text
支付事件必须最终消费
```

---

# 3. Streams：可持久追加的消息结构

Redis Stream 更像：

```text
append-only event log
```

每条 Entry 有 ID：

```text
1700000000-0
1700000001-0
```

常见：

```text
XADD
XREAD
XREADGROUP
XACK
XPENDING
```

它比 Pub/Sub 更适合需要：

- 历史消息；
- Consumer Group；
- Pending；
- Ack；
- Replay / Resume。

---

# 4. Consumer Group 解决什么

假设 3 个 Worker：

```text
worker-1
worker-2
worker-3
```

一个 Consumer Group 可以让它们分摊 Stream Entry。

```text
entry-1 → worker-1
entry-2 → worker-2
entry-3 → worker-3
```

并跟踪：

```text
哪些已经交付
哪些还 Pending
哪些已 ACK
```

这已经具备一定可靠消息语义。

---

# 5. Pending 为什么重要

Worker 收到消息后崩溃：

```text
Message delivered
但未完成
```

如果没有 Pending/Ack：

```text
消息可能直接消失
```

Stream 可以保留：

```text
Pending Entries
```

让系统后续检查、Claim 或重新处理。

---

# 6. Streams 为什么仍不等价 Kafka

Redis Stream 可以做可靠流式消费，但 Kafka 的设计重点更偏：

- 大规模持久 Event Log；
- Partition；
- 长 Retention；
- 多 Consumer Group 独立 Replay；
- 高吞吐流平台生态。

Redis Stream 更适合：

- 已经使用 Redis；
- 中等规模；
- 低延迟；
- 想减少额外基础设施；
- 消息规模和 Retention 要求有限。

完整 `Redis vs MQ` 选型 Primary 在 AI Backend Engineering。

---

# 7. Pub/Sub 和 Stream 怎么选

| 场景 | 更合适 |
|---|---|
| 配置更新通知 | Pub/Sub |
| 本地缓存失效广播 | Pub/Sub |
| 消息不能因为消费者离线而丢 | Stream |
| Worker 需要 Ack / Pending | Stream |
| 长期事件平台 / 大吞吐 Replay | 专业 MQ 更常见 |

---

# 8. Cache Invalidation 示例

多实例应用：

```text
API-1 local cache
API-2 local cache
API-3 local cache
```

更新配置：

```text
DB / Redis update
→ PUBLISH invalidation
```

三个 API 实例收到：

```text
evict local cache
```

如果某个 API 当时离线：

```text
它错过消息
```

所以重连后仍需要：

- TTL；
- Version；
- Periodic refresh；

不能只靠 Pub/Sub 保证最终一致。

---

# 9. Agent Event 是否适合 Stream

例如：

```text
agent_run_started
step_started
tool_called
step_finished
run_finished
```

如果只是 UI 实时推送：

```text
SSE / PubSub 可能够
```

如果还需要：

```text
Worker 消费
失败重试
Pending
Replay
```

Stream 或专业 MQ 更合适。

关键仍然是消息语义，不是“哪个工具更流行”。

---

# 10. 面试怎么答

## Q：Redis Pub/Sub 和 Stream 有什么区别？

🎯 **建议回答：**

> Pub/Sub 更像在线广播，订阅者离线时不会自动保存和补发历史消息；Stream 是可追加持久结构，有 Entry ID、Consumer Group、Pending 和 Ack，更适合需要可靠消费和 Replay 的场景。但对于大规模长期事件平台，仍要和 Kafka 等专业 MQ 比较吞吐、Retention、分区和生态。

---

# 11. 高频易错点

⚠️ **Pub/Sub 可以做可靠任务队列。**  
离线消费者会漏消息。

⚠️ **Streams 有 Ack，所以就是 Kafka。**  
目标和规模边界仍不同。

⚠️ **用了 Pub/Sub 本地缓存就永远一致。**  
Subscriber 离线会错过 Invalidation，需要 TTL / Version 等兜底。

---

# 12. 本章自测

<details>
<summary>1. 为什么 Pub/Sub 适合 Cache Invalidation，却不适合关键支付事件？</summary>

Cache Invalidation 可以用 TTL/Version 兜底；支付事件若消费者离线不能丢，需要持久、Ack、Replay 等更强消息语义。

</details>

<details>
<summary>2. Stream Consumer Group 为什么需要 Pending？</summary>

记录已经投递但尚未 ACK 的消息，消费者崩溃后可以发现并重新处理。

</details>

<details>
<summary>3. 什么时候应该考虑专业 MQ 而不是 Redis Stream？</summary>

需要大吞吐、长 Retention、大规模 Partition、多消费组 Replay、成熟事件平台生态等能力时。

</details>
