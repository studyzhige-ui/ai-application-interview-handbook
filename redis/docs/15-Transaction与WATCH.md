# 15｜Transaction：MULTI / EXEC / WATCH

很多人知道 Redis 单个 Command 原子，就会自然问：

> “那多个 Command 怎么办？”

Redis 提供 Transaction：

```text
MULTI
...
EXEC
```

但它和关系数据库事务很不一样。

---

## 1. MULTI / EXEC 的基本语义

```text
MULTI
SET a 1
INCR counter
HSET user:1 status active
EXEC
```

`MULTI` 后的命令先排队。

`EXEC` 时：

```text
按顺序执行全部 queued commands
```

Redis 保证：

> 在这批命令执行期间，不会插入另一个客户端的普通命令。

所以它们形成一个连续执行区间。

---

# 2. Redis Transaction ≠ MySQL Transaction

最大区别之一：

> **Redis Transaction 不提供传统数据库意义上的自动 Rollback。**

例如某个命令运行时因为 Value 类型不对失败：

```text
前面已经成功的命令
不会因为后面错误自动全部回滚
```

因此不要回答：

> “Redis MULTI/EXEC 和 MySQL BEGIN/COMMIT 一样，只是更快。”

这是错误的。

---

# 3. 为什么 Redis 不做传统 Rollback

Redis 的设计哲学更强调：

```text
简单执行模型
+
服务器端原子命令
+
应用提前保证命令合法
```

运行时错误通常意味着：

```text
程序逻辑错误
```

而不是像关系数据库那样依赖 Undo Log 统一回滚所有修改。

---

# 4. 事务前的命令语法错误

如果命令在 Queue 阶段就有明显语法/参数错误，事务可能在 `EXEC` 时整体拒绝执行。

但运行时错误和 Queue-time Error 要分开理解。

面试重点不要求背所有错误类型，而是记住：

> **Redis Transaction 的失败语义不是“任何错误都整体 Rollback”。**

---

# 5. WATCH 解决什么问题

假设：

```text
GET balance → 100
应用计算 new = 90
SET balance 90
```

在 GET 和 SET 之间：

```text
另一个客户端可能已经改过 balance
```

`WATCH` 提供 Optimistic Locking：

```text
WATCH balance
GET balance
MULTI
SET balance 90
EXEC
```

如果从 WATCH 到 EXEC 期间 `balance` 被修改：

```text
EXEC abort
```

应用重新读取并重试。

---

# 6. WATCH 的本质

不是：

```text
把 Key 锁住，不让别人改
```

而是：

```text
我先观察版本
→ 别人可以继续改
→ 提交时检查有没有变化
→ 变了就放弃本次事务
```

这就是 Optimistic Concurrency Control 的思想。

---

# 7. 为什么 WATCH 适合低冲突场景

如果冲突很少：

```text
大部分 EXEC 一次成功
```

很高效。

如果热点 Key 上 1000 个并发都：

```text
WATCH
→ 冲突
→ 重试
→ 再冲突
```

可能产生 Retry Storm。

这时更适合：

- 原生原子命令；
- Lua / Function；
- 数据模型调整。

---

# 8. Redis 8.4 之后的 CAS 能力怎么理解

现代 Redis 新版本开始提供更直接的 Compare-and-set / Compare-and-delete 能力，某些 String 场景可以不用手写 WATCH 重试。

但为了兼容和理解原理：

> `WATCH + MULTI + EXEC` 仍然是理解 Redis Optimistic Lock 的核心模型。

版本相关 API 应单独确认，不要把最新命令当成所有生产环境都存在。

---

# 9. Transaction 和 Pipeline 的区别先预告

Transaction：

```text
关注执行隔离 / 连续性
```

Pipeline：

```text
关注减少网络 RTT
```

二者可以在某些客户端 API 中组合，但概念完全不同。

下一章专门讲。

---

# 10. Cluster 下的 Transaction

如果事务涉及多个 Key：

```text
Key A
Key B
```

在 Cluster 中通常要求：

```text
同一个 Hash Slot
```

因为 Redis Cluster 不提供任意跨节点分布式事务。

所以 Hash Tag 和 Transaction 会重新连起来。

---

# 11. AI 场景

## Session 滑动续期

```text
读取 session
→ 更新 last_seen
→ 刷新 TTL
```

如果需要依赖读取值做条件更新，可用 WATCH 思想。

## Agent Task Claim

如果能用：

```text
SET NX PX
```

一次原生命令解决，就不要为了“看起来高级”硬上 Transaction。

设计原则：

> **优先单条原子命令，其次服务器端 Lua/Function，再考虑多命令 Optimistic Transaction。**

---

# 12. 面试怎么答

## Q：Redis Transaction 能 Rollback 吗？

🎯 **建议回答：**

> Redis MULTI/EXEC 保证 queued commands 在 EXEC 时按顺序连续执行，不被其他客户端命令插入，但它不像 MySQL 事务那样对运行时错误提供通用 Rollback。某个命令运行失败时，之前成功执行的命令通常不会自动撤销。

## Q：WATCH 是悲观锁吗？

> 不是。WATCH 是 Optimistic Locking：不阻止别人修改，而是在 EXEC 时检查被观察的 Key 是否变化；变化就让本次事务失败，由客户端重试。

---

# 13. 高频易错点

⚠️ **MULTI/EXEC = MySQL Transaction。**  
错误。

⚠️ **WATCH 会把 Key 锁死。**  
错误，是乐观并发控制。

⚠️ **多个原子命令组合后自动原子。**  
错误。

⚠️ **Transaction 一定比 Lua 更适合多步骤逻辑。**  
取决于是否需要读取中间结果、冲突率、Cluster Slot 和脚本复杂度。

---

# 14. 本章自测

<details>
<summary>1. MULTI/EXEC 最核心的保证是什么？</summary>

EXEC 时 queued commands 按顺序连续执行，不被其他客户端普通命令插入中间。

</details>

<details>
<summary>2. WATCH 为什么叫 Optimistic Lock？</summary>

它不阻止其他客户端修改，只在提交时检测冲突；有冲突就 abort 并由应用重试。

</details>

<details>
<summary>3. 为什么热点 Key 上 WATCH 可能表现差？</summary>

冲突率高会导致大量事务 abort 和客户端重试，形成额外负载。

</details>
