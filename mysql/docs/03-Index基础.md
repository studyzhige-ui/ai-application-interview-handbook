# 03. Index 基础：索引到底在优化什么

很多 MySQL 面试答案从一句话开始：

> “索引就是为了加快查询。”

这句话没错，但几乎没有解释力。

真正需要理解的是：

> **索引通过额外的数据结构和维护成本，帮助数据库缩小需要访问的数据范围，并尽可能减少昂贵的数据页访问、排序、扫描与回表。**

索引不是魔法，也不是“越多越好”。

---

## 1. 没有合适索引时发生什么

假设 `agent_runs` 有 5000 万行：

```sql
SELECT id, status, created_at
FROM agent_runs
WHERE user_id = 10001;
```

如果没有任何能帮助定位 `user_id` 的索引，数据库可能不得不检查大量记录，才能判断：

```text
这行 user_id 是不是 10001？
下一行呢？
下一页呢？
……
```

这就是为什么大表扫描会贵。

💡 **新手理解**：

一本 1000 页的字典，如果没有目录，而你想找某个词，可能要翻很多页；索引相当于额外维护了一套更适合“定位”的结构。

但这个类比只帮助理解“缩小查找范围”。数据库索引还涉及页、排序、树结构、回表、缓存和写入维护，不能只停留在书目录类比。

---

# 2. 索引优化的不是“SQL 字符串”，而是 Access Path

看两个 SQL：

```sql
SELECT *
FROM agent_runs
WHERE id = 123;
```

和：

```sql
SELECT *
FROM agent_runs
WHERE status = 'RUNNING';
```

假设：

- `id` 是 Primary Key；
- 80% 的行状态都是 `RUNNING`。

虽然两者都有可能对应索引，但访问成本完全不同。

第一条：

```text
通过高度选择性的主键
→ 很快定位极少记录
```

第二条：

```text
即使 status 有索引
→ 可能命中几千万条
→ 如果 SELECT * 还需要大量回表
→ Index 路径未必划算
```

所以索引真正要问的是：

```text
它能把候选范围缩小多少？
需要访问多少 Index Page？
需要取多少 Row？
是否还要回表？
结果是否已经有序？
写入时维护它要付出多少成本？
```

---

# 3. Cardinality / Selectivity 先建立直觉

假设有两个字段：

```text
user_id：5000 万行里有 1000 万个不同值
status：只有 PENDING/RUNNING/SUCCEEDED/FAILED 四种值
```

通常：

```text
user_id = 10001
```

比：

```text
status = 'SUCCEEDED'
```

更能快速缩小范围。

可以先把 **选择性（Selectivity）** 直观理解成：

> 一个条件能把原始数据缩小到多小。

不是说低基数字段永远不能建索引，而是：

- 单独使用时可能选择性差；
- 和其他字段组成 Composite Index 时可能仍很有价值；
- 如果查询需要排序 / Covering，也可能有额外收益；
- 是否使用最终由 Optimizer 成本模型决定。

⚠️ **易错点**：

不要背：

> “性别 / status 这种低基数字段一定不能建索引。”

应该说：

> “低选择性字段单独作为过滤索引往往收益有限，但是否值得建要结合数据分布、联合索引、排序、覆盖查询和真实访问模式。”

---

# 4. MySQL / InnoDB 常见索引先怎么分类

从学习角度，可以先分三层。

## 4.1 按业务约束

### Primary Key

```sql
PRIMARY KEY (id)
```

唯一且非空。

在 InnoDB 中，它还非常特殊：通常作为 Clustered Index。

---

### Unique Index

```sql
UNIQUE KEY uk_email (email)
```

用于保证唯一性，同时也可以用于查找。

---

### Non-unique Secondary Index

```sql
INDEX idx_user_created (user_id, created_at)
```

不要求值唯一。

---

## 4.2 按列数

单列：

```sql
INDEX idx_user (user_id)
```

联合：

```sql
INDEX idx_tenant_user_created (
    tenant_id,
    user_id,
    created_at
)
```

联合索引不是三个独立单列索引打包在一起，它有自己的排序结构。

这一点第 6 章会专门展开。

---

## 4.3 按 InnoDB 数据组织

最重要的是：

```text
Clustered Index
vs
Secondary Index
```

它们的叶子节点保存的东西不同，会直接决定：

- 什么是回表；
- 为什么主键大小影响所有 Secondary Index；
- 为什么 UUID 可能带来写入与空间问题。

第 5 章专门讲。

---

# 5. InnoDB 普通索引为什么常说是 B+Tree

MySQL 官方文档更严格地描述：

> 除 Spatial Index 外，InnoDB Index 是 B-tree 数据结构；索引记录保存在叶子页，默认索引页大小通常为 16KB。

面试与教材语境里通常会具体讨论它接近 **B+Tree 风格的多路平衡树组织**。

所以“为什么用 B+Tree”真正要解释的是：

```text
为什么不是普通 Binary Search Tree？
为什么不是 Red-Black Tree？
为什么不是 Hash？
为什么叶子链表适合 Range Scan？
为什么高扇出降低树高？
```

这就是下一章。

---

# 6. 一个索引不是“只存字段值”

假设：

```sql
INDEX idx_status_created (status, created_at)
```

你不能把它理解成一个简单：

```text
status → row
```

它本质上要维护一套有序索引记录。

在 InnoDB 的 Secondary Index 中，记录还会包含 Primary Key，用来最终定位 Clustered Index 中的整行。

简化表示：

```text
Secondary Index Leaf
(status, created_at, primary_key)
```

例如：

```text
FAILED,    2026-09-10 08:00, 18
FAILED,    2026-09-10 09:00, 39
RUNNING,   2026-09-10 10:00, 12
SUCCEEDED, 2026-09-10 07:00, 20
```

这马上引出：

> 为什么 `SELECT id, created_at` 可能只查 Secondary Index 就够，而 `SELECT *` 可能还要根据 Primary Key 回表。

---

# 7. 索引可以帮助哪些操作

索引不只是 `WHERE`。

## 7.1 Filter

```sql
WHERE user_id = 10001
```

---

## 7.2 Range

```sql
WHERE created_at >= '2026-09-01'
  AND created_at < '2026-10-01'
```

---

## 7.3 Join Lookup

```sql
JOIN agent_runs r
  ON r.user_id = u.id
```

如果 Join Key 有合适索引，可以减少匹配成本。

---

## 7.4 ORDER BY

如果 Index 的有序性和查询要求匹配，有机会直接按索引顺序读取，减少额外排序。

例如：

```sql
SELECT id, created_at
FROM agent_runs
WHERE user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

若 Index 设计与访问模式匹配，数据库可以利用索引顺序。

---

## 7.5 Covering

如果查询需要的列都能从索引中获得，就有机会减少回表。

---

# 8. 为什么不能给所有字段都建索引

索引是典型的：

> **空间换时间，而且还会增加写入维护成本。**

每多一个索引，`INSERT / DELETE / UPDATE` 都可能需要额外维护。

### INSERT

```text
插入 Clustered Index
+
更新 Secondary Index A
+
更新 Secondary Index B
+
更新 Secondary Index C
```

### UPDATE

如果更新的是被索引列，还可能导致：

```text
旧 Secondary Index Record delete-mark
+
新 Secondary Index Record insert
```

### 额外成本

- Index Page 占空间；
- Buffer Pool 也需要缓存索引页；
- 写入放大；
- Page Split / Merge；
- Statistics / Maintenance；
- 优化器候选更多。

🎯 **面试怎么答**：

> 索引通过额外有序数据结构降低查询时需要扫描和访问的数据量，但要付出空间与写放大成本。设计索引应从真实 Query Pattern 出发，不是给每个 WHERE 字段都加索引。

---

# 9. 为什么 Index 很适合 `LIMIT N`

假设要查：

```sql
SELECT id, created_at
FROM agent_runs
WHERE user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

如果有合适的：

```sql
INDEX idx_user_created (user_id, created_at)
```

数据库有机会：

```text
定位 user_id = 10001 的索引范围
→ 按 created_at 有序读取
→ 拿到前 20 条
→ 提前停止
```

相比：

```text
扫描很多行
→ Filter
→ Sort
→ 再取 20
```

差异可能非常大。

这说明一个好 Index 的价值不仅是“查到了”，而是可以改变整个执行路径。

---

# 10. 什么是 Prefix Index

对于较长字符串，有时只索引前 N 个字符：

```sql
CREATE INDEX idx_name_prefix
ON documents(filename(32));
```

它的目标是缩小 Index Size。

但需要权衡：

```text
Prefix 太短
→ 大量重复
→ Selectivity 差

Prefix 太长
→ Index 更大
→ 节省空间收益降低
```

⚠️ Prefix Index 不是“联合索引的 Leftmost Prefix”。

两个“Prefix”含义不同：

| 名称 | 含义 |
|---|---|
| Index Prefix | 字符串列只索引前 N 个字符 |
| Leftmost Prefix | 联合索引 `(a,b,c)` 可利用 `(a)`、`(a,b)` 等左侧连续前缀 |

面试里很容易混。

---

# 11. Hash 为什么不是 InnoDB 主索引结构

Hash 的优势：

```text
Key → Hash → Bucket
```

在理想条件下特别适合 Equal Lookup。

但它天然不擅长：

```text
WHERE x BETWEEN ...
ORDER BY x
找下一个 / 上一个
Prefix / Range Scan
```

而关系数据库查询大量依赖范围和排序。

因此 InnoDB 主体索引使用 B-tree 系列结构，而不是把所有索引做成 Hash Table。

⚠️ 这并不表示 MySQL 世界里完全没有 Hash。比如 InnoDB 有 Adaptive Hash Index 等内部机制，但不要把它和用户创建的普通 InnoDB B-tree Index 混淆。

---

# 12. 一个索引到底“值不值”的判断框架

以后看到一个字段，不要问：

> “它能不能建索引？”

先问：

```text
1. 哪些 SQL 高频访问它？
2. 是 Equal / Range / Sort / Join 哪一类？
3. 条件选择性怎样？
4. 返回多少行？
5. 是否能组成 Composite Index？
6. 是否有 Covering 价值？
7. 字段更新是否频繁？
8. Index 大小怎样？
9. 写入 QPS 是否高？
10. EXPLAIN / Benchmark 真的证明它有收益吗？
```

这就是工程化 Index Design。

---

# 13. 面试怎么答

## Q：什么是索引？为什么能提高查询性能？

🎯 **建议回答**：

> 索引是数据库为特定列维护的额外数据结构。InnoDB 普通索引采用 B-tree 类有序结构，通过键值快速缩小候选记录范围，并利用有序性支持 Range、ORDER BY 等访问。它优化的本质是减少需要扫描、访问和排序的数据。但索引会增加存储与写入维护成本，因此要结合选择性、Query Pattern、回表和实际执行计划设计。

## Q：是不是 WHERE 字段都应该建索引？

> 不是。低选择性、返回大量记录、频繁更新或本身没有高频访问价值的字段，单独建索引可能收益很小甚至增加写入成本。更应该从真实 Query Pattern 判断是否需要单列 / 联合 / 覆盖索引，并用 EXPLAIN 和实际测量验证。

---

# 14. 高频易错点

⚠️ “索引查询一定是 O(log n)，所以一定比全表扫描快。”  
复杂度只是抽象的一部分，真实成本还取决于 I/O、回表、返回规模、缓存和顺序访问。

⚠️ “低基数字段绝对不能建索引。”  
要看联合索引、覆盖、排序和实际数据分布。

⚠️ “索引越多查询越快。”  
忽略写放大、空间、Page 维护和优化器成本。

⚠️ “Hash 一定比 B+Tree 快，所以数据库应该用 Hash。”  
忽略 Range / Sort / Ordered Scan。

---

# 15. 本章自测

<details>
<summary>1. 索引真正优化的是什么？</summary>

不是 SQL 字符串本身，而是数据访问路径：更快缩小候选范围、减少需要访问的数据页 / 行，利用有序性减少排序，并在 Covering 情况下避免额外回表。

</details>

<details>
<summary>2. 为什么 `status` 只有四个值时，单列索引不一定有明显收益？</summary>

因为一个条件可能命中大量记录，选择性低；如果还要 `SELECT *`，大量 Secondary Index Lookup + 回表可能比顺序扫描成本更高。最终需要看真实分布和 Optimizer 计划。

</details>

<details>
<summary>3. Index 的主要代价是什么？</summary>

占额外存储和缓存空间；INSERT/UPDATE/DELETE 时需要维护；可能增加 Page Split / 写放大；被索引字段频繁修改时成本更明显。

</details>

<details>
<summary>4. Prefix Index 和 Leftmost Prefix 是一个东西吗？</summary>

不是。前者是长字符串只索引前 N 个字符；后者描述 Composite Index 的左侧连续列可形成可利用的索引前缀。

</details>

---

# 16. 官方资料

- MySQL 8.4 — Optimization and Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html>
- MySQL 8.4 — How MySQL Uses Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html>
- MySQL 8.4 — InnoDB Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-indexes.html>
- MySQL 8.4 — Column Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/column-indexes.html>

下一章进入高频中的高频：

> **为什么 InnoDB 的索引组织适合 B+Tree，而不是二叉树、红黑树或 Hash。**
