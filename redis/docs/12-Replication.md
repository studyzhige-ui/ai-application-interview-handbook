# 12｜Replication：Primary / Replica

Persistence 解决：

> **进程崩溃后，本机怎样恢复数据？**

Replication 解决另一个问题：

> **怎样把同一份 Dataset 复制到其它 Redis 实例？**

有了 Replica，系统才能进一步谈读扩展和 Failover。

---

## 1. 最基本拓扑

```text
        Primary
       /       \
  Replica-1  Replica-2
```

写请求通常发往 Primary。

Primary 把导致 Dataset 变化的操作复制给 Replica。

Replica 尽量保持和 Primary 一致的副本。

---

# 2. Redis Replication 默认是异步思路

这是非常重要的边界。

典型：

```text
Client write
   ↓
Primary apply
   ↓
Primary reply OK
   ↓
Replication stream → Replica
```

Primary 并不默认等所有 Replica 都确认完成才返回客户端。

所以存在：

```text
Primary 已回复成功
但 Replica 还没收到
Primary 此时故障
→ Failover 后最近写入可能丢失
```

这就是 Replication Lag / Write Safety Window。

---

# 3. WAIT 能做什么，不能做什么

Redis 提供 `WAIT`，客户端可以要求：

```text
等待至少 N 个 Replica
确认已经处理到某个 replication offset
```

这能降低写入丢失概率。

但官方明确提醒：

> **WAIT 不会把 Redis 复制变成一个严格 CP / 强一致系统。**

它提高副本确认程度，但 Failover、Persistence 和网络分区下仍存在边界。

---

# 4. Full Sync 与 Partial Resync

Replica 第一次连接或增量历史不够时，可能需要：

```text
Full Synchronization
```

大致直觉：

```text
Primary 生成当前 Dataset Snapshot
→ 发送给 Replica
→ 再补后续增量写
```

如果短暂断线后仍能找到共同 Replication History：

```text
Partial Resynchronization
```

只补缺失部分。

---

# 5. Replication ID + Offset 的意义

可以把：

```text
replication_id
+
offset
```

理解成：

> 某条 Dataset 历史上，Replica 已经追到哪里。

Replica 重连时带上之前状态，Primary 判断：

```text
还能不能从 backlog 增量补？
```

如果可以：

```text
Partial Resync
```

否则：

```text
Full Sync
```

---

# 6. Replica 可以分担读吗

可以，但必须接受：

```text
Replica Lag
```

例如：

```text
POST /update_profile
→ Primary 成功
→ 立即 GET /profile 走 Replica
```

可能读到旧值。

所以读写分离不是：

> “把 Read 都扔 Replica。”

而是要看业务是否允许 Stale Read。

---

# 7. AI Application 哪些读可以容忍旧数据

比较可能：

```text
热门配置
推荐候选
统计计数
非强一致 Cache
```

不一定可以：

```text
刚更新的权限
账户额度
关键 Session Security State
```

因此 Read Routing 是业务语义。

---

# 8. Replication Lag 怎么形成

常见原因：

- Primary 写入太快；
- Replica CPU 忙；
- 网络带宽不足；
- BigKey / Big Payload；
- Replica 磁盘 / Persistence 压力；
- Full Sync；
- 网络抖动。

所以 Replica Lag 不是只看 Redis 命令数量。

---

# 9. Primary 无持久化 + 自动重启为什么危险

官方文档强调一个典型 Failure：

```text
Primary persistence OFF
Replica B / C 跟随 A

A crash
→ A 自动重启
→ A 空 Dataset
→ B / C 继续复制 A
→ 副本也被清空
```

如果数据安全重要，这种组合非常危险。

这再次说明：

```text
Replication
≠
Persistence
≠
Backup
```

---

# 10. Replication 为什么不是自动高可用

只有：

```text
Primary + Replica
```

并不自动解决：

```text
Primary 挂了，谁决定提拔哪个 Replica？
客户端怎样找到新 Primary？
脑裂怎么办？
```

这些是 Sentinel / Cluster 的职责。

所以知识演进自然是：

```text
Replication
→ Failover Problem
→ Sentinel
```

---

# 11. 面试怎么答

## Q：Redis 主从复制是强一致吗？

🎯 **建议回答：**

> 默认不是。Redis Replication 主要采用异步复制，Primary 可以在 Replica 尚未完全同步时向客户端确认写入，因此 Failover 时存在最近写丢失窗口。WAIT 可以要求更多副本确认，降低风险，但官方也明确它不会让 Redis 变成严格强一致系统。

## Q：Replica 能不能做读扩展？

> 可以，但要接受复制延迟导致的 Stale Read。权限、额度等读后写强一致场景不能无脑走 Replica。

---

# 12. 高频易错点

⚠️ **有 Replica 就不会丢数据。**  
错误。

⚠️ **WAIT = 强一致。**  
错误。

⚠️ **Replication = Failover。**  
复制只是副本基础，自动故障转移需要 Sentinel / Cluster 等。

⚠️ **所有读都适合 Replica。**  
要看 stale tolerance。

---

# 13. 本章自测

<details>
<summary>1. 为什么异步复制会有 acknowledged write loss window？</summary>

Primary 可能已经回复客户端成功，但写入尚未到 Replica；此时 Primary 故障并发生 Failover，新 Primary 可能没有最近写入。

</details>

<details>
<summary>2. Partial Resync 的价值是什么？</summary>

短暂断线后只补缺失的复制流，而不重新传整个 Dataset，减少网络和恢复成本。

</details>

<details>
<summary>3. 为什么 Replication 不能替代 Backup？</summary>

错误删除和逻辑错误也会复制到 Replica；Backup 需要独立时间点和保留策略。

</details>
