# 02｜Keyspace、Command 与 Redis 基本执行模型

学 Redis 时，最容易一上来就背：

```text
String
Hash
List
Set
ZSet
```

但在数据结构之前，应该先理解 Redis 的基本抽象：

> **Redis 是一个 Keyspace，Key 指向某种具体类型的 Value；客户端通过 Command 操作这个 Value。**

这决定了后面 TTL、原子性、Cluster、Lua、Pipeline 都怎么理解。

---

## 1. Redis 的最小模型

```text
Key                  Value Type
------------------   ----------
user:1001:name       String
user:1001:profile    Hash
online_users         Set
leaderboard          ZSet
queue:tasks          List / Stream
```

Redis 不是：

```text
Table → Row → Column
```

而是：

```text
Key → Value
```

Value 又带具体类型。

---

# 2. Key 是全局命名空间里的名字

一个 Redis Database 中：

```text
session:abc
session:def
user:1001
user:1002
```

都属于同一个逻辑 Keyspace。

所以 Key Design 非常重要。

推荐使用可读前缀：

```text
session:{tenant}:{session}
conversation:{tenant}:{conversation}
rate:{tenant}:{user}
```

而不是：

```text
1
2
abc
foo
```

💡 **Key 不只是“变量名”。**

它影响：

- 可读性；
- 多租户隔离；
- 运维定位；
- Cluster Hash Tag；
- 扫描/统计；
- BigKey / HotKey 分析。

---

# 3. Command 是 Redis 的操作语言

例如：

```text
SET user:1001:name Alice
GET user:1001:name
```

Hash：

```text
HSET user:1001:profile age 22 city Shanghai
HGET user:1001:profile city
```

Set：

```text
SADD online_users 1001
SISMEMBER online_users 1001
```

你可以把 Redis 理解成：

> **针对不同数据类型提供大量服务器端原子命令。**

这和“客户端 GET 出来改完再 SET 回去”有本质区别。

---

# 4. 为什么服务器端原子 Command 很重要

假设 Counter 初始是：

```text
count = 10
```

错误的 Read-Modify-Write：

```text
A: GET count → 10
B: GET count → 10
A: SET count 11
B: SET count 11
```

最终：

```text
11
```

但本来应该是：

```text
12
```

Redis 直接提供：

```text
INCR count
```

两个客户端分别执行一次 `INCR`，就不会出现这种丢更新。

🧠 这也是为什么学习 Redis 不能只背“它是 KV”。

真正重要的是：

> **Value Type + Rich Atomic Command。**

---

# 5. Redis 单个 Command 的原子性怎么理解

在经典 Redis 执行模型中，大多数命令在服务器主执行路径上串行处理，因此单条命令执行期间不会被另一个普通命令“插一半”。

例如：

```text
INCR
HINCRBY
SADD
ZADD
```

都是服务器端完整执行的命令。

但注意：

```text
GET
应用层计算
SET
```

是三个阶段。

即使每条 Redis 命令单独原子，**整个三阶段并不原子。**

后面要靠：

- 原生命令；
- `WATCH + MULTI + EXEC`；
- Lua / Functions；
- 或更高层并发控制。

---

# 6. Command Complexity 不能忽略

很多人说：

> “Redis 都是 O(1)。”

错误。

不同命令复杂度不同。

例如：

```text
GET            常见 O(1)
HGET           常见 O(1)
SISMEMBER      常见 O(1)
ZRANGE         取决于范围大小
KEYS *         O(N)
SMEMBERS       O(N)
LRANGE 0 -1    O(N)
```

即使 Redis 在内存里：

> **O(N) 还是 O(N)。**

而且 Redis 主执行线程被一个慢命令占住时，其他请求会一起等。

所以后面 BigKey / HotKey / Latency Troubleshooting 都会回到这里。

---

# 7. Key 是否存在、类型是什么

常见：

```text
EXISTS key
TYPE key
DEL key
UNLINK key
```

`DEL` 与 `UNLINK` 的直觉区别：

```text
DEL
→ 删除工作可能在当前路径完成

UNLINK
→ 逻辑解除 Key 关联
→ 实际内存释放可交给后台线程处理
```

对于很大的 Key，直接删除本身可能产生明显延迟，所以不能只会 `DEL`。

---

# 8. KEYS 为什么不适合生产遍历

```text
KEYS session:*
```

对小测试库很方便。

但生产大 Keyspace 上：

```text
扫描整个 Keyspace
→ 主线程工作量大
→ 可能导致延迟尖刺
```

更常见使用：

```text
SCAN cursor MATCH pattern COUNT n
```

`SCAN` 是增量式迭代思路。

⚠️ 但 `SCAN` 也不是“完全免费”：

- 仍有 CPU 成本；
- 结果可能分多轮；
- 遍历过程中 Keyspace 变化时有迭代语义细节。

---

# 9. Logical Database 要谨慎理解

Redis 可以存在逻辑 DB 编号，例如常见：

```text
SELECT 0
SELECT 1
```

但大型生产系统通常更倾向：

```text
明确实例 / Cluster
+
Key Namespace
+
Tenant Boundary
```

而不是把逻辑 DB 当成熟的多租户隔离机制。

尤其 Redis Cluster 对逻辑 DB 的支持边界与 standalone 不同，后面 Cluster 章节再展开。

---

# 10. AI Application 的 Key Design

建议先问四个问题：

```text
1. 谁拥有这个 Key？
2. 生命周期多久？
3. 最大可能多大？
4. 是否会成为热点？
```

例如：

```text
conversation:{tenant_id}:{conversation_id}
```

比：

```text
conversation:{conversation_id}
```

更容易看出租户边界。

Rate Limit：

```text
rate:{tenant}:{user}:{window}
```

Session：

```text
session:{tenant}:{session_id}
```

⚠️ Key 里不要直接塞敏感 Secret / Token 明文作为可观察名称。

---

# 11. 面试怎么答

## Q：Redis 单个命令为什么通常具有原子性？

🎯 **建议回答：**

> Redis 的核心命令执行路径通常由主线程串行处理，所以一条命令执行时不会被另一个普通命令插入中间；但多个命令组成的客户端 read-modify-write 不因此自动原子，需要原生命令、事务 WATCH/MULTI/EXEC 或 Lua 等机制。

## Q：为什么不要在生产上随便 KEYS *？

> 因为它需要遍历整个 Keyspace，大实例上会占用主执行线程并制造延迟。生产遍历通常使用增量 SCAN，并且仍要控制频率和成本。

---

# 12. 本章自测

<details>
<summary>1. Redis 的核心抽象为什么不只是 Key-Value？</summary>

因为 Value 有明确数据类型，而且 Redis 提供围绕类型设计的大量服务器端原子命令。真正重要的是 Key → Typed Value → Command。

</details>

<details>
<summary>2. 两个原子 GET/SET 为什么组合后不一定原子？</summary>

因为客户端在 GET 与 SET 之间存在并发窗口，另一个客户端可以修改同一 Key。原子性只属于单条命令，不自动扩展到多命令业务流程。

</details>

<details>
<summary>3. Key Design 最少应该考虑哪些维度？</summary>

归属/租户、生命周期、大小上界、访问热度，以及是否需要 Cluster Hash Tag 等。

</details>
