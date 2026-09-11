# 13. RDB 与 AOF

Redis 是内存优先系统，但不代表：

> “进程一重启，数据一定全部丢失。”

Redis 提供 Persistence，把内存 Dataset 持久化到磁盘。

核心先分清：

```text
RDB = Snapshot
AOF = Write Log
```

---

## 1. RDB：某一时刻的数据快照

RDB 的直觉：

```text
Memory Dataset
   ↓ snapshot
RDB file
```

它保存的是某个时间点的数据状态。

优点：

- 文件紧凑；
- 适合备份；
- 重启加载通常较快；
- 对主进程日常写入路径影响较小。

代价：

> 如果两次 Snapshot 之间进程彻底丢失，最近一段写入可能无法从 RDB 恢复。

---

# 2. RDB 为什么常涉及 fork

生成 Snapshot 时，Redis 通常希望：

```text
主进程继续服务请求
+
后台生成一致快照
```

典型做法会利用：

```text
fork
+
Copy-on-write
```

子进程看到 fork 时刻的地址空间视图；父进程继续处理写入。

---

# 3. Copy-on-write 为什么可能造成内存峰值

fork 后：

```text
父子先共享物理页
```

父进程继续大量写：

```text
修改页面
→ COW 复制
```

大实例 + 高写入期间可能出现额外内存压力。

所以 RDB 风险不只在磁盘，还包括：

- fork latency；
- Page Table；
- COW Memory；
- Disk throughput。

---

# 4. AOF：记录写命令

AOF 的直觉：

```text
SET a 1
INCR counter
HSET user:1 name Alice
...
```

写操作被追加记录。

恢复时：

```text
Replay write operations
→ 重建 Dataset
```

它更像操作日志，而不是完整快照。

---

# 5. AOF fsync 策略

关键 Trade-off：

```text
数据安全
vs
写入延迟 / 磁盘开销
```

典型策略直觉：

```text
always
→ 每次写都强同步
→ 更安全、更慢

everysec
→ 常见折中
→ 理论上可能丢最近约一小段窗口

no
→ 交给 OS 决定 flush
```

具体行为依版本与配置而定，但核心就是：

> **什么时候认为日志真正持久化到稳定存储。**

---

# 6. AOF 为什么需要 Rewrite

如果一直追加：

```text
SET x 1
SET x 2
SET x 3
SET x 4
```

最终状态只需要：

```text
SET x 4
```

旧操作很多已经冗余。

AOF Rewrite 会生成更紧凑、能恢复当前 Dataset 的日志表示。

否则：

```text
文件无限增长
→ 启动 replay 越来越慢
```

---

# 7. RDB vs AOF

| 维度 | RDB | AOF |
|---|---|---|
| 核心模型 | Snapshot | Write Log |
| 文件 | 通常更紧凑 | 通常更大 |
| 恢复 | Load Snapshot | Replay Log |
| 数据丢失窗口 | 取决于 Snapshot 间隔 | 取决于 fsync 策略 |
| 后台成本 | fork / COW / 写文件 | append + rewrite |

Redis 也可以组合使用两者。

---

# 8. Persistence ≠ Backup

这是很重要的边界。

如果：

```text
应用误执行 FLUSHALL
```

这个错误可能被：

- AOF 记录；
- 复制到 Replica；
- 新 RDB Snapshot 固化。

所以高可用副本和 Persistence 并不等于独立 Backup。

真正备份通常还要：

- 独立保留历史 RDB/AOF；
- 异地/对象存储；
- Retention；
- Restore Drill。

---

# 9. Cache 场景是不是可以完全关闭 Persistence

有时可以。

如果 Redis 数据：

```text
全部可从 MySQL / 外部系统重建
```

而且重启后 Cold Cache 能接受，就可能关闭 Persistence。

但要考虑：

```text
Cache Warm-up Storm
```

以及 Replication 场景下官方明确提醒的危险配置：Primary 无持久化却自动重启为空 Dataset，Replica 可能跟随空 Primary，导致副本数据一起被覆盖。

所以不能只说：

> “Cache 不重要，Persistence 随便关。”

---

# 10. AI 场景怎么选

## 纯 Tool Result Cache

可重建：

```text
Persistence 可以弱化甚至关闭
```

## Session / 临时状态

需要评估：

```text
Redis 重启后用户是否全部掉线？
能否接受？
```

## Agent Runtime State

如果它是唯一状态副本：

```text
Persistence / Replication Failure 语义必须非常清楚
```

通常更稳的是：

```text
Redis = hot state
Durable checkpoint = separate durable store / explicit persistence design
```

---

# 11. 面试怎么答

## Q：RDB 和 AOF 有什么区别？

🎯 **建议回答：**

> RDB 是时间点 Snapshot，文件通常更紧凑、恢复快，但数据丢失窗口取决于快照频率；AOF 记录写操作，数据安全窗口取决于 fsync 策略，文件和恢复成本通常更大，因此需要 Rewrite。二者解决方式不同，也可以组合使用。

## Q：有 Replica 后还需要 Persistence 吗？

> Replication 和 Persistence 解决的问题不同。Replica 提供副本和 Failover，但错误写入也会复制；而且 Primary 无持久化自动空重启存在数据安全风险。是否开启持久化要根据数据是否可重建和恢复目标决定。

---

# 12. 高频易错点

⚠️ **RDB 每次都阻塞整个 Redis 直到写完。**  
典型实现会用后台子进程完成 Snapshot，但 fork/COW 仍可能带来压力。

⚠️ **AOF 不会丢数据。**  
仍取决于 fsync 策略和故障窗口。

⚠️ **Replica 就是 Backup。**  
错误操作也会复制。

⚠️ **Persistence 越强越好。**  
还要考虑延迟、I/O、成本和数据可重建性。

---

# 13. 本章自测

<details>
<summary>1. RDB 和 AOF 的根本差别是什么？</summary>

RDB 保存 Dataset 的时间点快照；AOF 保存写操作日志并在恢复时重放。

</details>

<details>
<summary>2. 为什么 RDB 期间可能出现额外内存压力？</summary>

fork 后父子依赖 Copy-on-write；高写入会复制更多页面，导致临时内存放大。

</details>

<details>
<summary>3. 为什么 Persistence 不能替代 Backup？</summary>

Persistence 会记录当前系统状态，逻辑误删除也可能被持久化；Backup 需要独立历史副本和恢复点。

</details>
