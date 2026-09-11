# 14｜Realtime Read-heavy Systems：排行榜、Feed、Autocomplete、Notification

这一章训练另一类常见系统：

> **读远多于写，用户对延迟敏感，但允许一定 Freshness Lag；真正难点是热点、Fan-out、排序和实时更新成本。**

对应真人 Scenario：

```text
SD-002 Realtime Ranking
SD-003 Autocomplete / Fuzzy Search
SD-004 Feed / Following
SD-005 Notification Platform
```

---

## 1. 共同抽象：Read-heavy + Derived View

这些系统通常都有：

```text
Primary Data
→ Async / Incremental Processing
→ Derived Read Model
→ Very Fast Query
```

例如排行榜：

```text
score events
→ aggregate
→ ranking view
→ Top-N read
```

Feed：

```text
post
→ fan-out / index
→ user feed view
→ paginated read
```

Autocomplete：

```text
source entities
→ search index / prefix structure
→ low-latency suggestion
```

核心不是“Redis/ES 哪个更强”，而是读模型怎样维护。

---

# 2. 排行榜：ZSet 只是一个实现，不是全部设计

Redis ZSet 很适合：

```text
member + score
→ rank / top N
```

但系统设计还要问：

```text
分数从哪来？
允许多久延迟？
排行榜按全局 / region / category？
Top100 和个人 rank 都要吗？
历史榜单怎么保存？
```

---

# 3. Global Ranking 的 HotKey / Hot Shard

如果全世界都更新：

```text
global_ranking
```

一个 Key / Shard 可能成为热点。

可以考虑：

```text
sharded partial ranking
→ periodic merge
→ global snapshot
```

或者按：

```text
region / category
```

先分区。

代价是 global rank 不再每次都绝对实时。

---

# 4. Ranking 的 Freshness Trade-off

如果业务允许：

```text
5s stale
```

可以批量聚合减少写压力。

如果必须：

```text
每次分数变化立即全局准确
```

成本会显著上升。

所以先定义：

> 实时到底是 10ms、1s 还是 1min？

---

# 5. Feed：Fan-out on Write vs Fan-out on Read

## Fan-out on Write

作者发帖：

```text
Post
→ push to follower inbox / feed
```

优点：

```text
read fast
```

问题：

```text
celebrity with 100M followers
→ huge write amplification
```

## Fan-out on Read

用户打开 Feed：

```text
read followed authors
→ merge recent posts
```

优点：写轻。

问题：读时 Merge 重。

真实系统常 Hybrid：

```text
normal users → push
celebrity → pull
```

---

# 6. Feed Pagination

Offset 很深会越来越贵。

更适合：

```text
cursor = (timestamp, id)
```

但要考虑：

```text
新内容插入
删除
排序稳定性
```

Cursor 应和排序字段、索引设计一致。

---

# 7. Autocomplete 先明确搜索语义

面试里 `SD-003` 不只是 Prefix。

可能要求：

```text
code
name
pinyin
prefix
infix
fuzzy typo
```

这些能力对应不同 Index / Analyzer。

例如：

```text
prefix trie / completion index
n-gram
inverted index
pinyin field
```

不要把所有需求都塞一个 SQL LIKE `%keyword%`。

---

# 8. Autocomplete 的低延迟路径

典型：

```text
keystroke
→ debounce client
→ query service
→ in-memory / search index
→ TopK suggestions
```

需要控制：

```text
per-user request rate
cache hot prefix
result size
P99
```

因为一次用户输入可能产生很多请求。

---

# 9. Fuzzy Search 的成本

越宽松的匹配：

```text
recall ↑
compute ↑
noise ↑
```

所以常见：

```text
prefix first
→ fuzzy fallback
```

或不同字段权重。

真正要通过点击率/成功率/latency 验证，不是“支持越多匹配越好”。

---

# 10. Notification Platform 的 Read-heavy / Async 混合

通知系统不只是“发消息”。

可以拆：

```text
Create Notification
→ Template Resolve
→ Recipient Resolve
→ Channel Route
→ Async Delivery
→ Status / Retry
```

Channel：

```text
Email
SMS
Push
Webhook
```

每个 Provider 都有自己的：

```text
rate limit
error semantics
idempotency
```

---

# 11. Notification 的可靠投递

需要区分：

```text
accepted
sent to provider
delivered to user
read by user
```

这些状态不是同一回事。

如果 Provider Timeout：

```text
可能已接受但响应丢失
```

需要 provider message id / idempotency / status query。

---

# 12. Dedup 与 Preference

通知可能被重复事件触发。

可用：

```text
notification_key
= business_event + recipient + template/version
```

去重。

同时要处理：

```text
user opt-out
quiet hours
channel preference
tenant policy
```

这属于业务状态，不是 MQ 自己解决。

---

# 13. 这类系统的共同 Observability

重点：

```text
Read P99
Cache Hit Rate
Fan-out Size
Index Freshness
Hot Key / Hot Prefix
Delivery Success
Queue Age
Dedup Rate
```

不同系统还要加质量指标：

```text
Feed engagement
Autocomplete click / accept rate
Notification conversion / complaint
```

---

# 14. 真人面经怎样影响本章

排行榜、Autocomplete、Feed、Notification 的独立来源不算最高，但它们覆盖了四种典型 Read Model。

因此保留为综合 Pattern，而不是拆成四篇“标准答案”。

面试重点通常会从：

```text
正常路径
→ Hotspot / Fan-out
→ Freshness
→ Pagination
→ Failure
```

继续深入。

---

# 15. 🎯 面试怎么答

> Read-heavy 系统我会先区分 Primary State 和 Derived Read Model，再用允许的 Freshness 换取低延迟。排行榜关注 HotKey 和分片聚合；Feed 重点比较 fan-out on write/read，并对 Celebrity 做 Hybrid；Autocomplete 根据 prefix/infix/fuzzy 语义选择索引，并控制 keystroke QPS；Notification 则用 Durable Task State 管理多 Provider 投递、Retry 和 Dedup。共同点是必须监控 Derived View 的 Freshness 和热点，而不是只看数据库 QPS。

---

# 16. 本章自测

<details><summary>1. 为什么 Celebrity Feed 常用 Hybrid Fan-out？</summary>
对普通作者 push 能让读很快，但超大粉丝作者 push 会产生巨大写放大，因此可以对大作者在读时 pull。
</details>

<details><summary>2. Autocomplete 为什么适合 Client Debounce？</summary>
每个键盘输入都立即请求会产生高 QPS 和无效中间查询，Debounce 可以减少不必要请求。
</details>

<details><summary>3. Notification 的“发送成功”为什么要拆状态？</summary>
服务接收任务、Provider 接受、最终设备送达、用户阅读是不同阶段，需要不同证据和重试策略。
</details>
