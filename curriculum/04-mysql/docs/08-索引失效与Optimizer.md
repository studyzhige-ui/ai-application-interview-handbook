# 08. 索引“失效”与 Optimizer 成本选择

`MYSQL-007` 有 **11 个独立 HUMAN-A**。

这一章最重要的目标，是把一句模糊的：

> “这个 SQL 索引失效了。”

拆成更准确的几类问题。

---

## 1. 先把“索引失效”拆成三种情况

### 情况 A：Predicate 无法形成有效 Index Lookup / Range

例如联合索引：

```sql
INDEX idx_abc (A, B, C)
```

只有：

```sql
WHERE B = 2;
```

传统 Leftmost Prefix 无法直接用 `(A,B,C)` 把 B=2 定位成一个连续 Key Range。

---

### 情况 B：可以使用 Index，但使用程度有限

例如：

```sql
WHERE A = 1
  AND B > 10
  AND C = 3;
```

A/B 可以构造 Range；C 可能不能继续收窄同一种连续范围，但仍可能用于 ICP。

不能一句“C 失效”把所有作用抹掉。

---

### 情况 C：Index technically 可用，但 Optimizer 认为别的方案更便宜

例如：

```sql
WHERE status = 'SUCCEEDED'
```

如果 90% Row 都是 `SUCCEEDED`，使用 Secondary Index 可能意味着：

```text
扫描巨大 Index Range
+
大量回表
```

Optimizer 可能判断 Table Scan 更便宜。

这不是 Index Structure 坏了，而是 **Cost Choice**。

💡 以后看到“不走索引”，先问：

```text
不能用？
能用一部分？
还是能用但不划算？
```

---

# 2. 对索引列做函数 / 表达式，为什么常出问题

有：

```sql
INDEX idx_created (created_at)
```

Query：

```sql
WHERE DATE(created_at) = '2026-09-11';
```

传统 B-tree Index 按原始 `created_at` 值排序。

现在 Predicate 变成：

```text
DATE(created_at)
```

数据库未必能直接把它转换成原始 Key 的连续 Range。

更友好的写法通常是：

```sql
WHERE created_at >= '2026-09-11 00:00:00'
  AND created_at <  '2026-09-12 00:00:00';
```

这样直接给出原始索引列上的 Range。

⚠️ 不要过度绝对化。

现代 MySQL 还有 Generated Column / Functional Index 等能力，某些表达式可以通过专门 Index 支持。面试回答应先说明“普通原始列索引”的语境。

---

# 3. 隐式类型转换为什么危险

假设：

```sql
phone VARCHAR(32)
INDEX idx_phone (phone)
```

如果 Query 把字符串列和数值常量混用：

```sql
WHERE phone = 13800138000;
```

数据库需要处理类型转换语义。

风险包括：

- 转换发生在 Indexed Column 侧；
- Index Range 无法按预期构造；
- 比较语义发生变化；
- Optimizer 计划不符合预期。

更好的做法是：

```sql
WHERE phone = '13800138000';
```

即：

> **应用参数类型尽量和 Schema 类型一致。**

这不只是性能问题，也是正确性问题。

---

# 4. `LIKE` 到底什么时候能利用 B-tree

假设：

```sql
INDEX idx_filename (filename)
```

### 前缀固定

```sql
WHERE filename LIKE 'report%';
```

可以对应一个前缀 Range，因此通常更容易利用 B-tree。

### 前导通配符

```sql
WHERE filename LIKE '%report';
```

或：

```sql
WHERE filename LIKE '%report%';
```

因为开头未知，很难按 B-tree Key 从某个明确起点快速定位。

所以经典结论：

> **Leading Wildcard 常让普通 B-tree 无法用于有效 Prefix Lookup。**

但如果业务核心是全文包含检索，本质上可能就应该考虑 Full-text / Search Engine，而不是逼普通 B-tree 做它不擅长的事。

---

# 5. `OR` 一定不走索引吗

不是。

错误口诀：

> “用了 OR 就索引失效。”

MySQL 存在 Index Merge 等优化，某些 `OR` 可以分别利用多个 Index 再合并结果。

例如：

```sql
WHERE user_id = 10001
   OR status = 'FAILED';
```

如果两侧有合适 Index，Optimizer 可能选择 Index Merge，也可能选择其他计划。

所以：

> `OR` 不是语法层面的“禁用索引开关”。

真正要看：

- 每个分支能否利用 Index；
- Selectivity；
- 合并成本；
- 返回规模；
- Optimizer Plan。

---

# 6. `!=` / `<>` / `NOT IN` 一定不走索引吗

也不是绝对。

例如：

```sql
WHERE id != 100;
```

从逻辑上可以拆成：

```text
id < 100
OR
id > 100
```

理论上存在 Range Access 可能。

但如果几乎整张表都满足条件，那么走索引是否划算又是另一个问题。

所以面试中不要背：

> “`!=` 一定索引失效。”

更准确：

> 否定条件往往选择性差、命中范围大，可能让 Index Access 收益变小；是否使用由具体 Range 和成本决定。

---

# 7. `IS NULL` 一定不走索引吗

也不是。

MySQL B-tree Index 可以处理 `NULL` 相关查找；是否使用仍要看：

- Index；
- Data Distribution；
- Cost；
- Query。

所以“`IS NULL` 索引失效”同样属于旧式绝对口诀。

---

# 8. 联合索引中间缺列

Index：

```sql
INDEX idx_abc (A, B, C)
```

Query：

```sql
WHERE A = 1
  AND C = 3;
```

准确描述：

```text
A=1
→ 可以形成 Index Range

B 未知
→ C=3 不能像连续 Leftmost Prefix 那样继续收窄传统 Lookup Range

C 在 Index Record 中
→ 仍可能参与过滤 / Covering
```

所以不是“整个 Index 失效”。

---

# 9. 为什么低选择性会让 Optimizer 放弃 Index

假设：

```sql
INDEX idx_status(status)
```

数据：

```text
SUCCEEDED  45,000,000
FAILED      2,000,000
RUNNING     2,500,000
PENDING       500,000
```

Query：

```sql
SELECT *
FROM agent_runs
WHERE status = 'SUCCEEDED';
```

如果走 Secondary Index：

```text
查 4500 万 Index Records
+
大量 Primary Key 回表
```

可能比：

```text
顺序扫描大量 Data Page
```

更贵。

于是 Optimizer 可能不选 `idx_status`。

这不叫“status 索引坏了”。

---

# 10. Statistics / Cardinality 为什么重要

Optimizer 依赖统计信息估算：

```text
这个条件大概命中多少？
这个 Index 的基数怎样？
这个 Join 顺序预计多贵？
```

如果估计偏差很大：

```text
Estimated Rows: 100
Actual Rows: 1,000,000
```

计划就可能不理想。

MySQL 还支持 Histogram 等统计机制，帮助描述某些列的数据分布。

因此排查：

> “为什么这个 Index 明明很好却没选？”

要看：

```text
SHOW INDEX
ANALYZE TABLE
Statistics / Cardinality
EXPLAIN
EXPLAIN ANALYZE
```

而不是第一反应 `FORCE INDEX`。

---

# 11. FORCE INDEX 为什么不应该是第一步

如果 Optimizer 没选你想要的 Index，直接：

```sql
FORCE INDEX (idx_xxx)
```

看似解决问题，但可能只是把判断写死。

数据分布以后变化：

```text
今天这个 Index 最优
半年后可能不是
```

更合理的排查：

```text
1. Query 本身是否合理？
2. Index 是否匹配 Query Pattern？
3. Statistics 是否准确？
4. Cardinality 是否异常？
5. 返回规模是不是太大？
6. Covering / 回表成本怎样？
7. Plan 为什么这样选？
8. 最后才考虑 Hint 是否真有必要
```

---

# 12. 一个典型“看起来索引失效”的 Case

有：

```sql
INDEX idx_user_created(user_id, created_at)
```

Query：

```sql
SELECT *
FROM agent_runs
WHERE user_id = 10001
  AND created_at >= '2026-01-01';
```

如果这个用户有 3000 万条历史记录，Query 本身要求返回 3000 万整行。

这时即使 Index Lookup 能快速定位范围，整个请求仍然很慢。

问题本质不是：

> “索引有没有生效？”

而是：

> **你要求数据库返回的数据量本来就巨大。**

需要从业务上考虑：

- Pagination；
- Limit；
- Aggregate；
- Archive；
- Query Shape；
- 数据生命周期。

这就是性能工程里非常重要的：

> **不要把所有慢查询都归因到索引。**

---

# 13. 一个更完整的“不走索引”排查框架

```text
Step 1：确认 Index 存在且 Visible
Step 2：确认 Query Predicate 能否形成有效 Range
Step 3：检查 Composite Index Prefix
Step 4：检查 Function / Expression / Type Conversion
Step 5：检查 LIKE Leading Wildcard 等访问模式
Step 6：看 Query 返回规模和 Selectivity
Step 7：看是否大量回表
Step 8：看 Statistics / Cardinality
Step 9：看 EXPLAIN 计划
Step 10：必要时 EXPLAIN ANALYZE 对比估计与实际
Step 11：修改 SQL / Index 后重新测量
```

---

# 14. 面试怎么答

## Q：常见索引失效场景有哪些？

🎯 推荐不要背“十条口诀”，而这样答：

> 我会把“不走索引”分三类。第一类是条件本身无法形成有效 B-tree Access，例如联合索引缺失左侧前缀、普通索引列被不利表达式处理、前导通配 LIKE 等；第二类是只利用了部分 Key，例如 Range 后续列主要用于 ICP，而不是继续收窄 Range；第三类是 Index 可以用，但因为选择性低、大量回表或统计成本，Optimizer 主动选择全表扫描等其它计划。最终要用 EXPLAIN / EXPLAIN ANALYZE 和真实数据分布验证。

## Q：为什么低选择性字段可能不走索引？

> 如果条件命中大部分 Row，Secondary Index 需要扫描大量 Index Record，再进行大量 Clustered Lookup；这种随机回表成本可能高于顺序扫描，因此 Optimizer 可能选择 Table Scan。

---

# 15. 高频易错点

⚠️ “`OR` 一定失效。”  
不对，可能存在 Index Merge 等计划。

⚠️ “`!=` 一定失效。”  
不对，要看 Range 和成本。

⚠️ “`IS NULL` 一定失效。”  
不对。

⚠️ “Range 后所有列都没用了。”  
不对，后续列可能用于 ICP / Covering。

⚠️ “没走 Index 就 FORCE INDEX。”  
不应该是第一反应。

⚠️ “Query 慢 = Index 失效。”  
可能本来就返回巨大结果、Lock Wait、I/O、Join、Sort、Network 等。

---

# 16. 本章自测

<details>
<summary>1. “索引失效”为什么是个不够精确的词？</summary>

因为它可能指：Predicate 无法形成索引查找范围；只能利用部分 Index Key；或者 Index 可以使用但 Optimizer 认为成本更高而主动不选。这三类问题的解决方式不同。

</details>

<details>
<summary>2. `LIKE 'abc%'` 和 `LIKE '%abc'` 为什么不同？</summary>

前者有已知前缀，可以映射成 B-tree 的前缀范围；后者开头未知，无法从一个明确有序位置快速定位。

</details>

<details>
<summary>3. 为什么大量回表会让 Optimizer 可能更倾向全表扫描？</summary>

Secondary Index 命中大量记录后需要根据许多 Primary Key 再访问 Clustered Index，访问成本可能比顺序扫描整个表更高。

</details>

<details>
<summary>4. 为什么不建议一遇到计划不理想就 FORCE INDEX？</summary>

它可能掩盖 Query / Index / Statistics 问题，而且数据分布变化后强制计划可能变成更差选择。应该先理解 Optimizer 为什么这样估算。

</details>

---

# 17. 官方资料

- MySQL 8.4 — How MySQL Uses Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html>
- MySQL 8.4 — Multiple-Column Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/multiple-column-indexes.html>
- MySQL 8.4 — Index Merge Optimization  
  <https://dev.mysql.com/doc/refman/8.4/en/index-merge-optimization.html>
- MySQL 8.4 — Optimizer Statistics  
  <https://dev.mysql.com/doc/refman/8.4/en/optimizer-statistics.html>
- MySQL 8.4 — Controlling the Query Optimizer  
  <https://dev.mysql.com/doc/refman/8.4/en/controlling-optimizer.html>

下一章把所有判断真正落到工具上：

> **EXPLAIN / EXPLAIN ANALYZE 到底怎么看，一条 Slow SQL 应怎样系统排查。**
