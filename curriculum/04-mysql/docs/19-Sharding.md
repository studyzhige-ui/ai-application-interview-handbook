# 19. Sharding：什么时候才需要分库分表

到这里我们已经完成了：

```text
单实例查询优化
→ Schema Design
→ Replication / 读扩展
```

接下来才进入一个经常被过早学习的概念：

> **Sharding。**

很多面试资料一上来就讲：

```text
按 user_id % 16 分 16 个库
```

但对初学者来说，最重要的问题其实是：

> **为什么单库单表不够？什么时候才值得付出分片的复杂度？**

---

## 1. 先讲人话：Sharding 是“把一份大数据拆开”

假设 `messages` 表增长到：

```text
几十亿行
```

单个 MySQL Instance 开始面临：

- Storage 太大；
- 单机 Write QPS 到瓶颈；
- Index 过大；
- Backup / DDL / Recovery 时间过长；
- Hot Data 集中；

这时可以把数据按规则拆到多个 Shard：

```text
Shard 0
Shard 1
Shard 2
Shard 3
```

每个 Shard 只存一部分数据。

---

# 2. Sharding 解决什么，不解决什么

它主要解决：

```text
单节点容量上限
单节点写吞吐上限
单表规模过大
```

它不会自动解决：

```text
慢 SQL
错误索引
不合理 Schema
热点 Key
业务模型混乱
```

如果一条 SQL 本来就写得很差，分成 32 个 Shard 可能只是：

> **让 32 个 Shard 一起慢。**

---

# 3. 为什么不能太早 Sharding

单库单表最大的优势是：

```text
简单
```

你天然拥有：

- 单库 Transaction；
- Join；
- Unique Constraint；
- ORDER BY；
- COUNT；
- Secondary Index；
- Operational Tooling。

一旦 Sharding：

```text
一次 Query 可能要打多个 Shard
```

于是复杂度爆炸。

所以更合理的演进通常是：

```text
Schema / Index 优化
→ 读写分离
→ 归档 / 冷热分层
→ 纵向扩容
→ 确认单节点真成为瓶颈
→ 才考虑 Sharding
```

---

# 4. Sharding Key 是最核心的设计

假设按：

```text
user_id
```

分片。

常见简单规则：

```text
shard = hash(user_id) % N
```

优点：

```text
同一个 user 的数据集中到一个 Shard
按 user 查询很方便
分布通常比较均匀
```

但如果查询是：

```text
按 tenant_id 汇总整个企业数据
```

就可能需要跨很多 Shard。

所以 Sharding Key 本质上是：

> **把最重要的访问路径编码进数据物理分布。**

---

# 5. 一个 AI SaaS 的例子

假设 Messages：

```text
tenant_id
user_id
conversation_id
```

你可能选择：

```text
按 tenant_id Shard
```

好处：

```text
同 Tenant 数据集中
权限 / 企业级查询方便
```

坏处：

```text
超级大客户会形成 Hot Shard
```

如果按：

```text
conversation_id hash
```

数据更均匀，但：

```text
Tenant 级汇总
User 级查询
```

更容易 Fan-out。

所以没有“最好 Sharding Key”，只有：

```text
更匹配你的访问模式
```

---

# 6. 数据均匀 ≠ 访问均匀

假设每个 Shard 数据量一样：

```text
Shard A 100GB
Shard B 100GB
Shard C 100GB
Shard D 100GB
```

但 80% 流量来自某个热门 Tenant：

```text
全部落在 Shard A
```

那么还是 Hot Shard。

所以分片设计要同时看：

```text
Data Distribution
+
Traffic Distribution
```

---

# 7. Range Sharding vs Hash Sharding

## Range

例如：

```text
user_id 1~1M → Shard 0
1M~2M → Shard 1
```

优点：

- 范围查询自然；
- 数据迁移边界直观。

缺点：

- 新数据可能集中到最后一个 Shard；
- 容易产生 Hotspot。

## Hash

```text
hash(user_id) % N
```

优点：

- 更容易分布均匀。

缺点：

- 范围查询困难；
- 直接扩 N 时数据重映射严重。

---

# 8. Consistent Hash 是否能解决所有扩容问题

不能。

Consistent Hash 可以减少节点增删时的重映射范围，但数据库 Sharding 仍要处理：

```text
真实数据搬迁
双写 / 路由切换
Migration Checkpoint
流量切换
一致性校验
Rollback
```

所以：

> **路由算法只是 Re-sharding 的一部分。**

---

# 9. 跨 Shard Query 为什么麻烦

单库：

```sql
SELECT *
FROM orders
ORDER BY created_at DESC
LIMIT 20;
```

分片后：

```text
Shard 0 的 Top 20
Shard 1 的 Top 20
Shard 2 的 Top 20
...
      ↓
Application / Proxy Merge Sort
      ↓
Global Top 20
```

如果还要：

```text
OFFSET 100000
```

问题更严重。

这就是为什么上一章特意把：

```text
单分片 Deep Pagination
```

和：

```text
跨 Shard Global Pagination
```

分开。

---

# 10. Global Pagination 为什么难

要拿全局：

```text
第 100001~100020 条
```

你可能需要从每个 Shard 拉取大量候选，再做 Merge。

这会造成：

```text
Fan-out
Network Cost
Memory Merge
Latency 放大
```

更常见的工程设计会倾向：

- Global Cursor；
- Time / ID based Seek；
- Search / Analytics System；
- 避免产品提供极深随机页码。

---

# 11. Join 怎么办

如果：

```text
users 在 Shard A
orders 在 Shard B
```

跨 Shard Join 会复杂很多。

常见思路：

- 让强关联数据使用同一个 Sharding Key；
- 冗余必要字段；
- Application Join；
- Dedicated Read Model；
- Search / Analytics Engine。

这其实再次说明：

> **Sharding Key 是业务建模决策，不只是数据库运维参数。**

---

# 12. Unique Constraint 怎么办

单表里：

```sql
UNIQUE(email)
```

可以天然保证全局唯一。

但如果 Email 被分散到 32 个 Shard：

```text
每个 Shard 都 UNIQUE
```

只保证：

```text
Shard 内唯一
```

不保证：

```text
全局唯一
```

常见解决方法：

- 按这个唯一 Key 本身分片；
- Global Registry；
- 独立 Unique Service；
- Application-level Reservation。

复杂度显著提高。

---

# 13. Transaction 怎么办

单 Shard Transaction：

```text
仍然是普通 MySQL Transaction
```

跨 Shard Transaction：

```text
Shard A 扣款
Shard B 创建订单
```

本地 InnoDB Transaction 不再覆盖全部数据。

你可能需要：

- 调整数据分布让强事务落同 Shard；
- Saga；
- TCC / XA；
- Outbox + Eventual Consistency；
- Compensation。

这些已经超出 MySQL 本地事务边界，属于 Backend / System Design。

---

# 14. Re-sharding 是真正困难的部分之一

假设从：

```text
8 Shards
```

扩到：

```text
16 Shards
```

如果直接改变：

```text
hash(key) % N
```

大量 Key 会迁移。

真实过程可能是：

```text
建新 Shard
→ Backfill 历史数据
→ Catch-up 增量变化
→ Dual Read / Dual Write 或路由兼容
→ Verify
→ Cutover
→ Cleanup
```

这已经是一个完整 Data Migration System。

---

# 15. Directory / Routing Layer

应用不能把：

```text
user_id % 32
```

散落在所有业务代码里。

更成熟的系统会抽象：

```text
Shard Router
```

负责：

```text
Logical Key
→ Physical DB / Table
```

这样未来扩容和迁移不会要求所有业务改路由逻辑。

---

# 16. 分库 vs 分表

## 分表

```text
同一个 Database Instance
多张物理表
```

可以降低单表规模，但：

```text
总写吞吐仍受同一 Instance 限制
```

## 分库

```text
数据分到多个独立 MySQL Instance
```

可以同时扩：

```text
Storage
CPU
I/O
Write Capacity
```

工程中“分库分表”常一起讨论，但两者解决的瓶颈层级不同。

---

# 17. Vertical Partition 与 Horizontal Sharding

还要区分：

## Vertical

按业务 / 列拆：

```text
User DB
Billing DB
Conversation DB
```

## Horizontal

同一种业务数据按 Key 拆：

```text
messages_0
messages_1
...
```

初学者应该先完成业务域拆分，再讨论同一大表的水平分片。

---

# 18. AI Application 场景

例如 Conversation / Message：

```text
Tenant 数量：百万
Message 数量：百亿
```

可能设计：

```text
Tenant Directory
      ↓
Shard Group
      ↓
Conversation / Message
```

但知识库 Document Metadata 可能是另一套 Sharding Key。

Usage / Billing 又可能必须：

```text
按 tenant 聚合
```

所以：

> **不同实体不一定使用同一个 Sharding 方案。**

---

# 19. 面试怎么答

## Q：什么时候需要分库分表？

🎯 推荐回答：

> 我不会把 Sharding 当第一步优化。先通过 Schema、Index、读写分离、归档和单机扩容解决能解决的问题；当单实例的存储、写吞吐、单表维护或恢复成本确实成为瓶颈，才考虑水平分片。之后核心是选择 Sharding Key，使主要查询尽量单 Shard，同时处理数据倾斜、Hot Shard、跨分片查询、全局唯一、事务和扩容迁移。

## Q：Sharding Key 怎么选？

> 主要看高频访问路径和数据 / 流量分布。希望强关联数据尽量同 Shard，避免跨分片 Join 和 Transaction；同时要防止大客户或热点 Key 导致倾斜。它是业务建模问题，不只是 hash 算法问题。

---

# 20. 高频易错点

⚠️ **数据量大就应该分库分表。**  
先确认单节点真的成为瓶颈。

⚠️ **`hash % N` 就是 Sharding 的全部。**  
真正困难的是 Query、Transaction、Unique、Migration 和 Operations。

⚠️ **数据均匀就不会 Hot Shard。**  
访问流量仍可能极度不均。

⚠️ **跨 Shard 可以像单库一样随便 Join。**  
成本和一致性模型都不同。

---

# 21. 本章自测

<details>
<summary>1. 为什么 Sharding 应该晚于 Schema / Index / Replication 学习？</summary>

因为 Sharding 是用显著复杂度换容量和写扩展。很多问题其实可以在单库通过索引、Schema、归档、读写分离解决；只有明确单节点瓶颈后才值得承担跨分片查询、事务和迁移成本。

</details>

<details>
<summary>2. 为什么 `tenant_id` 作为 Sharding Key 可能产生 Hot Shard？</summary>

如果少数大型 Tenant 的数据量或流量远高于其它 Tenant，虽然逻辑分片清晰，但这些大客户会集中压某些 Shard，造成数据或访问倾斜。

</details>

<details>
<summary>3. 为什么跨 Shard Deep Pagination 特别贵？</summary>

每个 Shard 都可能需要返回大量候选，应用层再进行全局排序和丢弃，导致 Fan-out、网络、内存和排序成本成倍放大。

</details>

---

## 继续学习

分片解决“数据放在哪里”。

下一步会出现另一个生产问题：

> **MySQL 的变化怎样可靠同步到 Search、Cache、Analytics 或其它下游？**

下一章：**CDC / Data Sync。**
