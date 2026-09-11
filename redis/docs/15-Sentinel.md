# 15. Sentinel 与自动 Failover

上一章已经有：

```text
Primary
+
Replica
```

但如果 Primary 挂了，还缺三个问题：

```text
谁来发现？
谁来选新 Primary？
客户端怎么知道新地址？
```

Sentinel 就是为**非 Cluster Redis**提供高可用协调的一层。

---

## 1. Sentinel 做什么

Redis 官方把 Sentinel 能力概括为：

- Monitoring；
- Notification；
- Automatic Failover；
- Configuration Provider。

直觉：

```text
Sentinel
  ├─ 盯着 Primary / Replica
  ├─ 判断故障
  ├─ 协调 Failover
  ├─ 提拔 Replica
  └─ 告诉客户端新 Primary
```

---

# 2. 为什么不能只跑一个 Sentinel

如果只有一个 Sentinel：

```text
Sentinel 自己挂了怎么办？
网络分区时它的判断可靠吗？
```

因此生产通常部署多个 Sentinel，通过多个观察者和 Quorum 思想降低单点误判。

---

# 3. 主观下线与客观下线的直觉

一个 Sentinel 发现 Primary 长时间没响应，可以先认为：

```text
Subjectively Down
```

但自动 Failover 是更高风险动作，因此需要多个 Sentinel 对故障形成足够共识，再进入：

```text
Objectively Down
```

核心思想：

> **“我觉得它挂了”不等于“系统已经足够确定，可以改拓扑”。**

---

# 4. Failover 大致发生什么

简化：

```text
1. Sentinel 发现 Primary 故障
2. 多 Sentinel 达成足够判断
3. 选举一个 Sentinel 负责 Failover
4. 从 Replica 中选择候选
5. Promote 为新 Primary
6. 其它 Replica 改为跟随新 Primary
7. 客户端获得新 Primary 地址
```

具体选举和 epoch 细节不要求初学者一开始背完，但要理解它是**协调状态机**，不是一个简单 shell script。

---

# 5. Failover 为什么不等于零数据丢失

因为底层 Replication 默认仍是异步。

```text
旧 Primary 回复 OK
→ 写还没复制到候选 Replica
→ 旧 Primary 故障
→ Replica 被提升
```

这条写可能没有出现在新 Primary。

所以：

> Sentinel 提高 Availability，不会把 Redis 自动变成强一致数据库。

---

# 6. Client 为什么必须 Sentinel-aware

应用不能把地址永久写死成：

```text
10.0.0.1:6379
```

Failover 后 Primary 已经变了。

支持 Sentinel 的客户端通常会：

```text
向 Sentinel 查询当前 Primary
→ 建立连接
→ Failover 后重新发现
```

所以高可用不仅是服务器部署问题，也是 Client Integration 问题。

---

# 7. Sentinel 和 Cluster 的根本区别

Sentinel：

```text
一个完整 Keyspace
→ 一个 Primary 服务
→ Replica 做副本
→ Sentinel 做 Failover
```

Cluster：

```text
Keyspace 被拆成多个 Hash Slot
→ 多个 Primary 各管一部分
→ 每个 Primary 可有 Replica
→ 同时解决 Sharding + HA
```

所以：

```text
Sentinel = 非分片 HA
Cluster = 分片 + HA
```

---

# 8. 什么时候 Sentinel 足够

如果：

- 单实例容量足够；
- 单 Primary 吞吐足够；
- 主要目标是 HA；
- 不想引入 Cluster 分片复杂度；

Sentinel 可以很合适。

当你遇到：

```text
单实例 Memory 不够
或
单节点吞吐不够
```

才自然进入 Cluster。

这就是知识顺序：

```text
Replication
→ Sentinel
→ Cluster
```

而不是因为 Cluster 听起来更高级就先学。

---

# 9. Split Brain / Network Partition 的风险直觉

分布式系统里，节点“看不到对方”不代表对方真的死了。

网络分区可能让：

```text
旧 Primary 仍接受部分客户端写
另一侧已经 Promote 新 Primary
```

系统必须通过 Quorum、配置 epoch、客户端路由和部署策略降低双主窗口。

但 Redis HA 不应该被描述成：

> “绝对不会出现任何脑裂或写丢失。”

---

# 10. AI Application 的 Failover 设计

即使 Sentinel 能在数秒内切主，应用仍要考虑：

```text
Redis 连接短暂失败
→ API 怎么办？
```

不同数据：

## Cache

```text
可以回源 DB
```

## Session

```text
可能短暂登录失败
```

## Rate Limit

```text
Fail-open 还是 Fail-closed？
```

## Agent Lease

```text
错误 Fail-open 可能导致双 Worker 执行
```

所以 HA 必须和业务降级语义一起设计。

---

# 11. 面试怎么答

## Q：Sentinel 解决什么问题？

🎯 **建议回答：**

> Sentinel 为非 Cluster 的 Redis Primary/Replica 部署提供监控、故障判断、自动 Failover 和配置发现。Primary 故障后，它协调选择 Replica 提升为新 Primary，并让其他 Replica 与客户端切换。但因为底层复制通常异步，Sentinel 主要提升可用性，不保证零数据丢失或强一致。

## Q：Sentinel 和 Cluster 怎么选？

> 单实例容量和吞吐够，只需要高可用时 Sentinel 更简单；需要水平分片 Keyspace、突破单节点容量或吞吐时才进入 Cluster。

---

# 12. 本章自测

<details>
<summary>1. 为什么 Sentinel 不能只有一个实例？</summary>

单 Sentinel 自身会成为故障和判断单点；多个 Sentinel 可以通过 Quorum/选举提高故障判断和 Failover 协调可靠性。

</details>

<details>
<summary>2. Sentinel Failover 为什么仍可能丢最近写？</summary>

因为 Primary 到 Replica 通常异步复制，旧 Primary 已确认但尚未复制的写在故障后可能不存在于被提升的 Replica。

</details>

<details>
<summary>3. Sentinel 与 Cluster 最大区别是什么？</summary>

Sentinel 主要给完整 Keyspace 的单 Primary 架构提供 HA；Cluster 还把 Keyspace 分成 Hash Slot，由多个 Primary 水平分片。

</details>
