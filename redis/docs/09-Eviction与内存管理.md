# 09. maxmemory、Eviction 与内存压力

TTL 回答的是：

> “这个 Key 什么时候按业务语义失效？”

Eviction 回答的是另一个问题：

> **“Redis 内存已经到上限了，新写入还要继续时，应该淘汰谁？”**

这两个机制经常被混在一起。

---

## 1. 为什么需要 maxmemory

Redis 主要以内存为核心资源。

如果不做容量边界：

```text
持续写入
→ 进程越来越大
→ OS 内存压力
→ Swap / OOM
→ 整个实例失控
```

所以生产 Redis 通常会设置内存上限，并选择 Eviction Policy。

---

# 2. Expiration ≠ Eviction

Expiration：

```text
业务定义 TTL 到了
→ Key 过期
```

Eviction：

```text
内存压力到达 maxmemory
→ 为腾空间主动淘汰 Key
```

一个完全没有 TTL 的 Key，也可能在 `allkeys-*` 策略下被淘汰。

一个有 TTL 的 Key，也不一定等到 TTL 到点才离开内存。

---

# 3. 常见 Eviction Policy

可以先按两大维度理解：

## 3.1 淘汰所有 Key

```text
allkeys-lru
allkeys-lfu
allkeys-random
```

## 3.2 只在带 TTL 的 Key 中淘汰

```text
volatile-lru
volatile-lfu
volatile-random
volatile-ttl
```

还有：

```text
noeviction
```

表示内存达到上限后，对需要分配更多内存的写操作返回错误，而不是主动淘汰业务 Key。

---

# 4. LRU 和 LFU 在表达什么

## LRU

```text
Least Recently Used
```

倾向淘汰：

> 最近很久没访问的 Key。

## LFU

```text
Least Frequently Used
```

倾向淘汰：

> 长期访问频率较低的 Key。

直觉：

```text
LRU 更关注“最近”
LFU 更关注“频率”
```

但 Redis 的实现并不是为了给每个 Key 维护一个完美全局排序，那样本身代价太高；实际实现采用近似算法和采样思想。

---

# 5. 怎么选 Policy

## 纯 Cache

如果 Key 都可重建：

```text
allkeys-lru / allkeys-lfu
```

通常更符合直觉。

## Redis 同时存 Cache + 关键非缓存状态

这时风险很大。

如果使用：

```text
allkeys-lru
```

关键状态也可能被淘汰。

所以更成熟的做法通常是：

- 不把不同可靠性等级的数据混在同一实例；
- 或使用更明确的 TTL/Policy 边界；
- 或拆实例。

> **Eviction Policy 是系统语义的一部分，不只是 Redis 配置项。**

---

# 6. 为什么 HotKey 可能刚淘汰又回来

假设某个 Key 很热，但因某种策略被淘汰：

```text
Key evicted
→ 下一批请求全部 Miss
→ 大量回源 DB
→ Key 立刻重新写回 Redis
```

这叫一种典型的 Cache Thrashing / 回流问题。

如果内存长期不足：

```text
淘汰
→ 回源
→ 重建
→ 再淘汰
```

系统会陷入高成本震荡。

真正解决方法不是：

> “把 TTL 调短一点。”

而可能是：

- 增大容量；
- 降低缓存对象大小；
- 调整 Policy；
- 拆热点；
- 控制 Cache Admission；
- 多级缓存。

---

# 7. Cache Admission：不是所有东西都值得缓存

很多初学者默认：

```text
Miss
→ 一定写 Cache
```

但如果是：

- 只访问一次的大对象；
- 长尾查询；
- 超大 Tool Result；

写进 Redis 可能挤掉真正热点。

所以成熟缓存系统会考虑：

```text
Should this item enter cache?
```

而不只是：

```text
How long should it stay?
```

---

# 8. 内存不足时只看 used_memory 够吗

不够。

还要关注：

```text
used_memory
RSS
fragmentation
maxmemory
allocator behavior
fork / COW peak
```

特别是 RDB/AOF Rewrite 等期间，Copy-on-write 可能临时放大内存需求。

所以不要把实例长期跑到：

```text
99% physical memory
```

再认为“还有 1% 就够”。

需要留安全余量。

---

# 9. 为什么 Swap 对 Redis 很危险

Redis 的低延迟建立在内存访问上。

如果 OS 把 Redis 页面换到 Swap：

```text
访问一个 Key
→ Page Fault
→ 磁盘换入
```

延迟可能突然从微秒/毫秒级变成非常难看的尾延迟。

因此生产 Redis 通常非常警惕 Swap。

---

# 10. 一个 AI Cache 例子

假设缓存 LLM Tool Result：

```text
cache:tool:weather:...
```

有两类：

```text
A. 高频小结果
B. 偶尔出现、每个 5MB 的大结果
```

如果 B 也无脑写入 Cache：

```text
大对象快速吃掉内存
→ 淘汰大量 A
→ A Miss 增多
```

所以必须同时设计：

```text
Size Limit
TTL
Admission
Eviction
```

---

# 11. 面试怎么答

## Q：Redis 内存淘汰策略有哪些？怎么选？

🎯 **建议回答：**

> 可以先分成 allkeys、volatile 和 noeviction。allkeys 会在所有 Key 中按 LRU/LFU/Random 等策略选，volatile 只在带 TTL 的 Key 中选，noeviction 则内存满后拒绝需要额外内存的写。纯缓存场景常考虑 allkeys-lru/lfu；如果实例混有不能被淘汰的状态，就要非常谨慎，通常应该从数据分层或拆实例解决，而不是只调一个 Policy。

## Q：LRU 和 LFU 有什么差别？

> LRU 更偏最近是否使用，LFU 更偏长期访问频率。Redis 实际使用近似/采样方式，不维护全局精确排序。

---

# 12. 高频易错点

⚠️ **TTL 到期和 Eviction 是一回事。**  
不是，一个是业务生命周期，一个是内存压力策略。

⚠️ **allkeys-lru 永远最好。**  
取决于数据是否都允许被淘汰。

⚠️ **内存满了就加机器。**  
先检查 BigKey、缓存价值、对象大小、Admission 和 Fragmentation。

⚠️ **Redis 在内存，所以 Swap 也没问题。**  
恰恰相反，Swap 会严重破坏延迟。

---

# 13. 本章自测

<details>
<summary>1. Expiration 和 Eviction 的触发条件有什么不同？</summary>

Expiration 由 Key 自己的 TTL 语义触发；Eviction 是实例达到 maxmemory 后为了继续分配内存而主动选择 Key 淘汰。

</details>

<details>
<summary>2. 为什么一个实例同时放 Cache 和关键状态会让 allkeys 策略危险？</summary>

因为 allkeys 策略可能把关键状态当成普通缓存一起淘汰，导致数据语义被破坏。

</details>

<details>
<summary>3. 什么是 Cache Admission？</summary>

决定一个 Miss 结果是否值得进入缓存，而不是默认所有结果都写入。它用于避免长尾或大对象污染有限缓存空间。

</details>
