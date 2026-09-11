# 06. Redis 为什么快：Thread Model 与阻塞边界

面试常见一句话：

> “Redis 为什么快？”

如果只回答：

> “因为单线程 + 内存。”

既不完整，也容易讲错。

更准确的理解应该拆成：

```text
内存访问
+ 高效数据结构
+ 事件驱动 / I/O Multiplexing
+ 大多数命令执行路径短
+ 避免大量线程上下文切换和锁竞争
+ Pipeline / Batch 可进一步减少 RTT
```

---

## 1. 先讲人话：Redis 快，不代表所有操作都快

Redis 很多常见操作：

```text
GET
SET
HGET
INCR
SISMEMBER
```

都非常短。

但如果你执行：

```text
KEYS *
SMEMBERS 一个千万成员集合
删除超大 Key
超长 Lua Script
```

Redis 仍然可能出现明显延迟。

所以：

> **“Redis 快”是总体设计优势，不是每条 Command 都无条件低延迟。**

---

# 2. 第一个原因：Memory-first

Redis 的核心工作数据主要放在内存。

相比频繁随机磁盘访问：

```text
DRAM access
```

通常快很多。

但不要把它说成：

> “Redis 完全不碰磁盘。”

因为：

- RDB；
- AOF；
- Rewrite；
- Replication；
- Fork / Copy-on-write；

都可能和磁盘、OS 内存管理发生关系。

---

# 3. 第二个原因：Server-side Data Structures

很多业务逻辑可以直接用 Redis 命令完成：

```text
INCR
HINCRBY
ZADD
ZRANGE
SINTER
```

避免把大量数据拉回应用层再处理。

例如 Counter：

```text
INCR key
```

一次命令就完成原子增加。

---

# 4. 第三个原因：Mostly Single-threaded Command Execution

Redis 官方文档更稳妥的表述是：

> Redis 使用 **mostly single-threaded design**。

也就是：

- 核心客户端请求/命令执行路径长期以单线程串行为主要模型；
- 但 Redis 进程并不是“只有一个线程”；
- 后台 I/O、持久化相关工作以及现代版本的部分网络 I/O 可以使用其他线程。

所以不要回答：

> “Redis 整个进程只有一个线程。”

这是错误的。

---

# 5. 单线程为什么反而能很快

因为 Redis 常见命令本身很短：

```text
请求到达
→ 查数据结构
→ 修改/读取
→ 返回
```

主执行路径串行的好处：

- 少很多共享数据锁竞争；
- 少线程切换；
- 执行模型简单；
- 单条命令天然容易形成原子执行边界。

但是代价也很明确：

> **一条慢 Command 可能拖住后面的所有请求。**

所以“单线程”既是优点，也是延迟风险来源。

---

# 6. 第四个原因：不阻塞在一个连接上等 I/O

假设有 10000 个连接。

错误思路：

```text
一个连接一个线程
每个线程阻塞等待 socket
```

Redis 使用 Event Loop + I/O Multiplexing：

```text
大量 Socket
   ↓
OS 通知哪些 Ready
   ↓
Event Loop 处理 Ready Event
```

因此不需要给每个空闲连接都绑定一个重线程。

下一章专门讲。

---

# 7. 网络 RTT 可能比命令本身还贵

假设：

```text
INCR
```

服务器只需要几十微秒甚至更短的工作。

但客户端和 Redis 之间一次网络 RTT 可能更贵。

如果连续 100 次：

```text
send → wait
send → wait
send → wait
```

性能会被 RTT 放大。

Pipeline 可以：

```text
send 100 commands together
→ server processes
→ receive responses together
```

后面第 18 章讲。

---

# 8. Redis 最怕什么阻塞

## 8.1 高复杂度 Command

例如全量遍历。

## 8.2 BigKey

大对象：

```text
读取
序列化
网络发送
删除
复制
```

都可能拖慢。

## 8.3 长 Lua Script

Lua 执行具有原子性，但：

```text
脚本执行期间
→ 其他命令要等
```

所以原子不等于应该写 5 秒脚本。

## 8.4 Fork / Persistence Pressure

RDB / AOF Rewrite 可能触发 fork、Copy-on-write、磁盘 I/O。

大实例上需要关注。

## 8.5 Swap

Redis 数据被 OS swap 到磁盘，会严重破坏低延迟特性。

---

# 9. CPU 多核是不是完全没用

不能这么说。

即使核心命令执行主要串行：

- 后台任务可使用其他线程；
- 网络 I/O 可有多线程支持；
- 多实例 / Cluster 可以利用多个 Core；
- Persistence / OS 也会消耗 CPU。

如果单实例 CPU 成为瓶颈，Scale 手段可能是：

```text
优化命令
→ 减少 BigKey / Slow Command
→ Pipeline
→ Shard / Cluster
→ 多实例
```

而不是简单“给这个实例加 64 核就自动线性提升”。

---

# 10. 为什么不应该把 Redis CPU 打到 100% 才算利用充分

低延迟系统关心：

```text
P50
P95
P99
P999
```

当 Event Loop 持续满载：

```text
排队时间增长
→ Tail Latency 爆炸
```

所以生产系统通常要留 Headroom。

---

# 11. 面试怎么答

## Q：Redis 为什么快？

🎯 **建议回答：**

> 首先 Redis 的核心数据以内存访问为主，并针对不同数据结构提供高效服务器端命令。其次它长期采用 mostly single-threaded 的核心命令执行模型，避免了大量共享状态锁竞争和线程切换，再通过 Event Loop / I/O Multiplexing 同时管理大量连接。实际延迟还受命令复杂度、BigKey、网络 RTT、Persistence 和 CPU 饱和影响，所以不能简单概括成“单线程所以快”。

## Q：Redis 是单线程吗？

> 更准确地说，核心客户端命令执行路径主要是单线程串行模型，但 Redis 进程还有后台线程/进程相关工作，现代版本也可以在部分网络 I/O 上使用线程，因此“整个 Redis 只有一个线程”是错误说法。

---

# 12. 高频易错点

⚠️ **Redis 因为单线程所以快。**  
因果过度简化。

⚠️ **Redis 只有一个线程。**  
错误。

⚠️ **内存数据库就不会卡。**  
O(N)、BigKey、长 Lua、fork、Swap 都可能卡。

⚠️ **CPU 越高吞吐越健康。**  
低延迟服务还要关注 Queueing 和 Tail Latency。

---

# 13. 本章自测

<details>
<summary>1. Redis mostly single-threaded 的优势和代价分别是什么？</summary>

优势是执行模型简单、锁竞争和线程切换少；代价是一个慢命令可能阻塞后续客户端请求，因此慢命令和 BigKey 特别危险。

</details>

<details>
<summary>2. 为什么 Pipeline 能明显提高吞吐？</summary>

它减少逐条命令的网络往返和客户端等待，让多个命令批量发送与读取响应，降低 RTT 成本。

</details>

<details>
<summary>3. Redis 在内存里，为什么持久化仍可能导致延迟？</summary>

RDB/AOF Rewrite 会涉及 fork、Copy-on-write、磁盘 I/O 和 OS 调度，大实例下这些都可能制造延迟尖刺。

</details>
