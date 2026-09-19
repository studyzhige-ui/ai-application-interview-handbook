# 16｜Pipeline：降低 RTT，不等于 Transaction

很多 Redis 性能问题并不发生在服务器执行命令本身，而发生在：

```text
Client ↔ Network ↔ Redis
```

如果连续执行 1000 条很快的命令，却每条都等待一次响应，网络往返时间会成为主要成本。

Pipeline 就是为这个问题服务的。

---

## 1. 没有 Pipeline 时

```text
send SET a
wait reply
send SET b
wait reply
send SET c
wait reply
```

总耗时里不断重复：

```text
RTT + Command + RTT + Command + ...
```

如果 Redis 与应用跨机器，RTT 可能远大于单个 `SET` 的执行时间。

---

# 2. Pipeline 的核心思想

```text
Client
  ↓ 一次批量发送
CMD1
CMD2
CMD3
...
  ↓
Redis 顺序处理
  ↓ 一批响应
R1
R2
R3
```

目标：

> **减少网络往返和系统调用开销，提高吞吐。**

---

# 3. Pipeline 不保证事务语义

这是最重要的边界。

Pipeline：

```text
性能优化
```

Transaction：

```text
执行隔离 / 连续性
```

概念上：

```text
Pipeline ≠ Transaction
```

某些客户端库的 `pipeline()` API 可能默认带 Transaction 行为，这是**客户端封装细节**，不能因此把两个概念混为一谈。

例如 redis-py 的 Pipeline API 默认可用 transaction 模式，但你也可以显式关闭事务。

---

# 4. Pipeline 为什么不能无限大

假设一次 Pipeline：

```text
100 万条命令
```

问题：

- 客户端要缓存请求；
- Redis 要处理大量命令；
- Reply Buffer 变大；
- 单批次延迟变长；
- 失败重试粒度巨大；
- 可能压垮连接或内存。

所以生产一般：

```text
合理 Batch Size
```

而不是“越多越快”。

---

# 5. Pipeline 和 MGET / MSET 怎么选

如果有原生命令：

```text
MGET k1 k2 k3
MSET k1 v1 k2 v2
```

通常优先考虑原生命令。

因为：

- 协议更直接；
- 服务器理解为一个命令；
- 语义更明确。

Pipeline 更适合：

```text
多个不同 Command
或
客户端批处理大量请求
```

---

# 6. Cluster 下 Pipeline 更复杂

如果一批 Key 分布在：

```text
Node A
Node B
Node C
```

Cluster Client 需要按 Slot / Node 拆批并路由。

因此：

```text
单实例 Pipeline
```

和：

```text
Cluster Pipeline
```

并不完全一样。

成熟 Client 通常会做分组，但你仍要理解：

> Pipeline 不会神奇地跨节点形成原子事务。

---

# 7. Pipeline 的错误处理

一批 Pipeline 里：

```text
第 3 条失败
```

不意味着其它命令一定整体 Rollback。

你需要：

- 按响应逐条检查；
- 定义 Retry；
- 考虑 Idempotency；
- 避免把批次失败误认为事务失败。

---

# 8. AI Application 的典型场景

## 批量写 Session 元数据

```text
HSET session:1 ...
EXPIRE session:1 ...
HSET session:2 ...
EXPIRE session:2 ...
```

可以 Pipeline 减少 RTT。

## 批量读取 Tool Cache

多个独立 Tool Key：

```text
GET cache:a
GET cache:b
GET cache:c
```

如果不能用一个 MGET，也可以 Pipeline。

## RAG Ingestion Metadata

大量 Document Metadata 回填 Redis 时也可以用 Batch / Pipeline。

但千万不要把一个百万级导入全部塞一个 Pipeline。

---

# 9. Pipeline 与 Backpressure

应用持续生产命令：

```text
Producer 速度
>
Redis / Network 消费速度
```

客户端缓冲会越来越大。

所以高吞吐 Pipeline 还要配：

```text
Batch Size
Concurrency Limit
Timeout
Queue Limit
Backpressure
```

这部分通用机制归 AI Backend Engineering。

---

# 10. 面试怎么答

## Q：Redis Pipeline 和 Transaction 有什么区别？

🎯 **建议回答：**

> Pipeline 主要为了性能，把多条命令批量发送和读取响应，减少 RTT；Transaction 的重点是 MULTI/EXEC 下的连续执行与 WATCH 乐观并发控制。Pipeline 本身不提供事务原子性，也不会因为一条命令失败就自动回滚其它命令。某些客户端把 pipeline 和 transaction API 组合只是库的封装。

## Q：Pipeline 越大越好吗？

> 不是。过大的 Pipeline 会增加客户端/服务器 Buffer、单批延迟、错误处理和重试成本，生产需要控制 Batch Size。

---

# 11. 本章自测

<details>
<summary>1. Pipeline 优化的主要成本是什么？</summary>

网络 RTT 和逐条请求/响应的系统调用、等待开销。

</details>

<details>
<summary>2. Pipeline 中第 5 条命令失败，前 4 条会自动回滚吗？</summary>

不会把 Pipeline 当事务理解。每条命令有自己的执行结果，除非另外使用 Transaction 等机制。

</details>

<details>
<summary>3. 为什么 Cluster Pipeline 需要 Client 额外处理？</summary>

不同 Key 可能属于不同 Slot/Node，客户端需要按节点路由/拆批，且跨节点 Pipeline 不形成全局原子事务。

</details>
