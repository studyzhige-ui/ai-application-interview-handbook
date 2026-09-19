# 16. Deep Pagination 与查询优化

这一章开始从“数据库机制”转向“数据量增长后真实查询为什么会慢”。

最经典的入口就是：

```sql
SELECT *
FROM agent_runs
ORDER BY id
LIMIT 20 OFFSET 100000;
```

很多初学者会认为：

> 有 `LIMIT 20`，MySQL 只需要读 20 行。

实际上，大 Offset 往往意味着数据库必须先找到并跳过大量前置记录。

---

## 1. 先讲人话：OFFSET 不是“瞬移”

假设你要：

```text
第 5001 页
每页 20 条
```

SQL：

```sql
LIMIT 20 OFFSET 100000
```

数据库不能凭空跳到“第 100001 条业务结果”。

它必须沿访问路径先找到前面的候选结果，再丢掉前 100000 条，只返回后面 20 条。

所以 Deep Pagination 的核心问题是：

```text
返回很少
≠
扫描很少
```

---

# 2. 为什么 Offset 越大越慢

简化理解：

```text
OFFSET 0
→ 找前 20 条

OFFSET 1000
→ 找前 1020 条，再丢 1000

OFFSET 100000
→ 找前 100020 条，再丢 100000
```

数据量越大，浪费越明显。

如果查询还需要：

- 回表；
- filesort；
- 复杂过滤；
- Join；

成本会进一步放大。

---

# 3. `ORDER BY` 是否走索引非常关键

比如：

```sql
SELECT id, status, created_at
FROM agent_runs
WHERE tenant_id = 10
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;
```

如果有合适索引：

```text
(tenant_id, created_at)
```

MySQL 可以按索引顺序扫描。

如果没有：

```text
先过滤大量记录
→ filesort
→ 再做 LIMIT / OFFSET
```

所以 Deep Pagination 不是孤立技巧，它建立在前面章节的：

```text
Composite Index
Covering Index
EXPLAIN
```

之上。

---

# 4. 第一类优化：让“跳过”发生在更轻的数据结构上

如果原查询：

```sql
SELECT *
FROM agent_runs
ORDER BY id
LIMIT 100000, 20;
```

可能需要大量二级索引扫描 + 回表。

可以考虑先只在覆盖索引里定位主键：

```sql
SELECT a.*
FROM agent_runs a
JOIN (
    SELECT id
    FROM agent_runs
    ORDER BY id
    LIMIT 100000, 20
) x ON a.id = x.id;
```

思路是：

```text
前 100000 条的“跳过”
尽量只扫描窄索引
      ↓
最后 20 个 id
      ↓
再回表 20 次
```

这类优化不是万能模板，但体现一个重要思想：

> **尽量减少大 Offset 阶段携带的列和回表成本。**

---

# 5. 更好的长期方案：Keyset / Seek Pagination

如果业务允许“下一页”语义，通常更好的方式是记住上一页最后一条排序 Key。

第一页：

```sql
SELECT id, status, created_at
FROM agent_runs
WHERE tenant_id = 10
ORDER BY id
LIMIT 20;
```

假设最后一条：

```text
id = 5000
```

下一页：

```sql
SELECT id, status, created_at
FROM agent_runs
WHERE tenant_id = 10
  AND id > 5000
ORDER BY id
LIMIT 20;
```

这叫：

```text
Keyset Pagination
或 Seek Pagination
```

数据库可以直接从 B+Tree 某个 Key 附近继续向后扫描，而不是从头跳过十万条。

---

# 6. 为什么 Seek Pagination 更稳定

Offset Pagination 的成本随着页码增长：

```text
Page 1     → 小
Page 100   → 更大
Page 10000 → 很大
```

Seek Pagination：

```text
根据 last_key 定位
→ 继续扫描固定数量
```

每页成本通常更接近稳定。

因此特别适合：

- Feed；
- Timeline；
- Conversation History；
- Agent Run History；
- Log / Event 浏览；

这类“持续向后翻”的产品。

---

# 7. 多列排序怎么办

如果排序：

```sql
ORDER BY created_at DESC, id DESC
```

不能只记：

```text
last_created_at
```

因为同一秒可能有很多记录。

更稳妥是使用稳定唯一 Tie-breaker：

```text
(created_at, id)
```

下一页条件例如：

```sql
WHERE tenant_id = 10
  AND (
       created_at < :last_created_at
       OR (created_at = :last_created_at AND id < :last_id)
  )
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

并建立对应联合索引：

```text
(tenant_id, created_at, id)
```

---

# 8. 为什么分页一定要有稳定排序

下面这种：

```sql
SELECT *
FROM agent_runs
LIMIT 20 OFFSET 100;
```

没有明确 `ORDER BY`。

问题是：

> SQL 结果没有义务保持某个稳定业务顺序。

尤其在执行计划变化、并发写入时，很容易出现：

```text
重复项
漏项
页面抖动
```

所以分页设计应先回答：

> **业务的稳定排序 Key 是什么？**

---

# 9. Offset Pagination 什么时候仍然可以用

不要把它妖魔化。

以下场景完全可以：

- 数据量小；
- 页数浅；
- 后台管理系统；
- 用户确实需要“跳到第 37 页”；
- 查询频率低；

工程优化不是为了消灭所有 OFFSET，而是：

> **在真正出现成本问题时选择更合适的数据访问模型。**

---

# 10. Count(*) 与“总页数”也是成本

传统分页 UI 喜欢：

```text
共 12,483,922 条
第 1 / 624,197 页
```

这通常意味着：

```sql
SELECT COUNT(*) ...;
```

复杂条件或超大表下，总数统计本身也可能很重。

很多现代产品会改成：

```text
has_more
next_cursor
```

而不是每次都给精确总页数。

这其实是：

> 产品交互与数据库成本一起设计。

---

# 11. Cursor Pagination 是 API 层的表达

对外 API 常见：

```json
{
  "items": [...],
  "next_cursor": "..."
}
```

Cursor 内部可以编码：

```text
last_created_at
last_id
```

下一次请求带回来。

所以链路是：

```text
Keyset / Seek Pagination
        ↓
Backend 封装排序位置
        ↓
Cursor Pagination API
```

这会在 FastAPI / Backend 模块重新出现。

---

# 12. 不要只看 SQL，要看业务访问模式

如果需求是：

> 查询用户最近 100 个 Agent Run。

最自然设计：

```sql
WHERE tenant_id=? AND user_id=?
ORDER BY created_at DESC, id DESC
LIMIT 100;
```

索引：

```text
(tenant_id, user_id, created_at, id)
```

如果产品从一开始就采用 Cursor，那么根本不需要等到“上线后 OFFSET 100000 很慢”才救火。

这说明：

> Schema / Index / API Pagination 应该一起设计。

---

# 13. Deep Pagination 和 Sharding 不是同一个问题

本章只讨论：

```text
单表 / 单分片内部的 Deep Pagination
```

如果已经分库分表，查询：

```text
全局第 100001～100020 条
```

还会多出：

```text
每个 Shard 拉多少？
怎么 Merge Sort？
如何做 Global Cursor？
```

这属于第 19 章 Sharding。

不要把两个问题混成一句“分页优化”。

---

# 14. AI Application 场景

典型列表：

```text
Conversation List
Message History
Agent Run History
Tool Execution History
Evaluation Cases
Billing Records
Audit Events
```

其中：

- 对话历史：非常适合 Cursor；
- 管理后台：浅 Offset 也可能足够；
- Audit / Event：通常按 `(created_at, id)` Seek；
- 复杂报表：可能应该进入 Analytics System，而不是无限压 OLTP MySQL。

---

# 15. 面试怎么答

## Q：为什么 `LIMIT 100000,20` 会慢？

🎯 推荐回答：

> LIMIT 只限制最终返回数量，不代表数据库只扫描 20 条。大 OFFSET 需要先沿执行路径找到并丢弃前 100000 条，如果还伴随回表或 filesort，成本更高。可以通过覆盖索引减少跳过阶段的 I/O，更根本的方案是用 Keyset / Seek Pagination，根据上一页最后一个稳定排序 Key 继续扫描。

## Q：Cursor Pagination 的缺点？

> 它非常适合连续向前/向后翻页，但不擅长随机跳到任意页；Cursor 设计还必须保证排序稳定、处理相同排序值、数据插入删除以及 Cursor 的编码和安全性。

---

# 16. 高频易错点

⚠️ **LIMIT 20 就只扫描 20 行。**  
错误。

⚠️ **所有分页都应该改 Cursor。**  
小数据 / 浅分页没必要过度工程化。

⚠️ **只用 created_at 作为 Cursor 一定安全。**  
如果不唯一，可能出现重复 / 漏数据，应加稳定 Tie-breaker。

⚠️ **分页慢只需要加索引。**  
大 OFFSET 的跳过成本仍然存在。

---

# 17. 本章自测

<details>
<summary>1. Deep Pagination 的根本浪费是什么？</summary>

数据库为了返回很少的后段记录，仍然需要定位并跳过大量前置候选记录，可能同时产生大量回表和排序成本。

</details>

<details>
<summary>2. Seek Pagination 为什么通常比大 Offset 更稳定？</summary>

因为它根据上一次最后一个排序 Key 直接定位到 B+Tree 的后续位置，再扫描固定数量，而不是从结果起点重新跳过越来越多的数据。

</details>

<details>
<summary>3. 为什么多列排序的 Cursor 要保留 Tie-breaker？</summary>

因为主排序列可能重复。只有保存 `(created_at,id)` 之类稳定且最终唯一的排序位置，才能避免下一页边界上的重复或遗漏。

</details>

---

## 继续学习

下一章进入更基础也更重要的设计问题：

> **不是 SQL 慢了以后怎么救，而是表一开始应该怎样设计。**

下一章：**Schema Design：从访问模式设计表。**

---

## 官方参考

- LIMIT Query Optimization：<https://dev.mysql.com/doc/refman/8.4/en/limit-optimization.html>
- ORDER BY Optimization：<https://dev.mysql.com/doc/refman/8.4/en/order-by-optimization.html>
