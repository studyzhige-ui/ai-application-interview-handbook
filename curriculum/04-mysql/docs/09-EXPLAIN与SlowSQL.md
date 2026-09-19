# 09. EXPLAIN 与 Slow SQL 排查

`MYSQL-003` 有 **11 个独立 HUMAN-A**，而且它和 `MYSQL-007 Index Invalidation` 经常连续出现。

真正成熟的回答不是：

> “慢 SQL 就加索引。”

而是：

> **先确认慢在哪里，再用执行计划、实际数据分布和运行指标验证假设。**

---

## 1. EXPLAIN 到底是什么

MySQL 官方定义很直接：

> `EXPLAIN` 用来显示 Optimizer 为一条语句选择的执行计划信息。

例如：

```sql
EXPLAIN
SELECT id, status, created_at
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

它回答的是：

```text
准备按什么顺序读表？
准备使用什么 Access Type？
有哪些候选 Index？
最终选哪个 Index？
预计扫描多少 Row？
有哪些 Extra 操作？
```

⚠️ `EXPLAIN` 不是“性能评分器”，也不是看到 `key != NULL` 就说明 SQL 已经优化完了。

---

# 2. EXPLAIN ANALYZE 为什么更强，也更要小心

MySQL 8.4 支持：

```sql
EXPLAIN ANALYZE
SELECT ...;
```

它会**真正执行查询**并收集运行信息，用来比较：

```text
Estimated Rows
vs
Actual Rows

Estimated Cost
vs
真实执行行为
```

这对发现 Optimizer 估算偏差非常有价值。

但也因此：

⚠️ **不要把 `EXPLAIN ANALYZE` 当成无副作用的“看一下”。**

对昂贵 `SELECT`，它真的会执行；在高负载生产环境使用前要评估影响。

---

# 3. 传统 EXPLAIN 最值得先看的字段

不同 MySQL 版本 / FORMAT 输出不同。秋招最常见还是先理解传统表格格式里的核心字段。

例如：

```text
id
select_type
table
partitions
type
possible_keys
key
key_len
ref
rows
filtered
Extra
```

不需要把所有字段背成字典，重点建立读取顺序。

---

# 4. `type`：访问方式比“有没有 key”更重要

`type` 描述表的 Access Method。

常见可以从更精确到更宽泛建立直觉：

```text
system
const
eq_ref
ref
range
index
ALL
```

这不是一条“绝对性能排行榜”，但非常适合快速判断访问范围。

## `const`

例如：

```sql
WHERE id = 123
```

Primary / Unique Key 等值命中最多一行时，Optimizer 可以把它近似当常量处理。

---

## `eq_ref`

Join 场景中，对前表每一行，通过 Primary / Unique Index 在后表最多匹配一行。

---

## `ref`

通过 Non-unique Index 等值查找，可能匹配多行。

---

## `range`

扫描一个或多个 Index Range：

```sql
WHERE created_at >= ... AND created_at < ...
```

---

## `index`

通常表示扫描整个 Index Tree。

它不等于：

> “很好，走索引了！”

扫描整个 Index 仍然可能很贵，只是扫描的是 Index 而不是完整 Table Data。

---

## `ALL`

Full Table Scan。

看到 `ALL` 也不要条件反射认为一定错。

如果：

- 表很小；
- Query 本来就要大部分 Row；
- 合适 Index 不存在；
- Optimizer 判断全扫便宜；

Full Scan 可能合理。

🎯 面试应该说：

> `ALL` 是需要重点检查的信号，但是否有问题必须结合表规模、返回比例、Query Goal 和实际耗时。

---

# 5. `possible_keys` 和 `key`

### `possible_keys`

Optimizer 认为可能相关的候选 Index。

### `key`

最终执行计划选择的 Index。

常见情况：

```text
possible_keys = idx_user, idx_status
key = idx_user
```

说明两个候选都存在，但最终选 `idx_user`。

如果：

```text
possible_keys 有值
key = NULL
```

不要立刻说“索引失效”。

可能是：

> Index 可以考虑，但 Cost Model 认为其他方式更便宜。

---

# 6. `key_len` 能看什么

`key_len` 反映计划使用 Index Key 的字节长度信息。

它常被用来辅助判断：

> **联合索引到底利用到了哪些 Key Part。**

但不要只背固定数字。

长度受到：

- Data Type；
- Nullable；
- Character Set；
- Prefix；

等影响。

更好的做法是：

```text
Index 定义
+
Query Predicate
+
key_len
+
EXPLAIN FORMAT=TREE / JSON
```

一起判断。

---

# 7. `rows` 不是“实际扫描行数”

传统 `EXPLAIN` 中的 `rows` 主要是 **Optimizer Estimate**。

例如：

```text
rows = 100
```

不代表这次实际运行严格读了 100 行。

真正值得关注的是：

```text
估计是不是离真实情况很远？
```

例如：

```text
Estimated 100
Actual 1,000,000
```

可能意味着：

- Statistics 不准确；
- Data Distribution 倾斜；
- Predicate 相关性没被很好估计；
- Plan 可能因此选错。

这就是 `EXPLAIN ANALYZE` 的价值之一。

---

# 8. `filtered` 怎么理解

`filtered` 可以理解成 Optimizer 估算：

> 在当前访问得到的 Row 中，大约多少比例能通过剩余条件。

例如：

```text
rows = 100000
filtered = 1.0
```

粗略意味着：

```text
先访问约 10 万 Row
→ 估计只有约 1% 通过过滤
```

这可能提示：

> Access Path 取得的候选太宽。

但仍要结合完整计划，不把单一字段当最终结论。

---

# 9. `Extra` 最常见的信号

## `Using index`

通常和 Covering / Index-only Access 有关。

---

## `Using index condition`

通常表示 ICP。

---

## `Using where`

表示还需要应用 WHERE Filter。

这不是“坏事”，绝大多数查询本来就需要条件判断。

---

## `Using filesort`

说明结果排序不能完全直接按可用 Index Order 得到，需要额外排序阶段。

名字里有 `file` 不代表一定真的把排序写到磁盘文件。

⚠️ 不要回答：

> “Using filesort 就一定发生磁盘排序。”

---

## `Using temporary`

表示执行中需要内部临时表，常见于某些 GROUP BY / DISTINCT / ORDER 等场景。

这也是需要进一步检查成本的信号，而不是看到就说 SQL 必须重写。

---

# 10. EXPLAIN FORMAT=TREE / JSON 为什么值得会

传统 EXPLAIN 表格对复杂计划有时不够直观。

例如：

```sql
EXPLAIN FORMAT=TREE
SELECT ...;
```

可以更自然看：

```text
Limit
  ↓
Sort / Index Scan
  ↓
Nested Loop / Hash Join
  ↓
Index Lookup
```

官方文档还指出，`TREE` 能展示比 Traditional 更精确的一些处理信息，并且 `EXPLAIN ANALYZE` 使用 Tree 格式。

所以面试里如果你不仅会背传统 `type/key/rows`，还能说：

> “复杂计划我会看 Tree / Analyze，对比 Estimate 与 Actual。”

工程感会明显更强。

---

# 11. 一条 Slow SQL 的完整排查流程

## Step 1：先确认“慢”是真的慢

先拿到：

```text
P50 / P95 / P99
SQL Latency
调用频率
最近是否突然变化
是否只有某组参数慢
```

不要只凭一句：

> “用户说这个页面慢。”

---

## Step 2：拿完整 SQL + 参数

同一个 Prepared SQL：

```sql
WHERE tenant_id = ?
```

不同 Tenant 的数据量可能差几个数量级。

因此参数非常重要。

---

## Step 3：看 Table / Index / Data Distribution

```sql
SHOW CREATE TABLE agent_runs;
SHOW INDEX FROM agent_runs;
```

确认：

- Index 定义；
- Composite Column Order；
- Cardinality；
- Primary Key；
- Row Size；
- Data Volume。

---

## Step 4：EXPLAIN

```sql
EXPLAIN FORMAT=TREE
SELECT ...;
```

重点问：

```text
从哪里开始读？
Access Type 是什么？
用哪个 Index？
预计读多少？
Join 顺序怎样？
有没有 Sort / Temporary？
是否大量回表？
```

---

## Step 5：必要时 EXPLAIN ANALYZE

如果环境允许：

```sql
EXPLAIN ANALYZE
SELECT ...;
```

重点比较：

```text
Estimate vs Actual
哪一个 Operator 最耗时
Loop 次数
实际 Rows
```

---

## Step 6：确认是不是 Lock Wait

SQL 慢不一定是执行计划慢。

可能是：

```text
等待 Row Lock
等待 Metadata Lock
长事务阻塞
Deadlock Retry
```

如果只看 Index，方向会完全错。

---

## Step 7：确认是不是资源问题

例如：

```text
Buffer Pool Miss
Storage I/O
CPU
Memory Pressure
Connection Saturation
Temp Table
Large Sort
Network Result Transfer
```

---

## Step 8：修改后重新验证

可能修改：

```text
SQL
Index
Composite Column Order
Projection
Pagination
Schema
Statistics
Data Lifecycle
```

修改后必须再测：

```text
Plan 是否变化？
Actual Rows 是否下降？
Latency 是否下降？
Write Cost 是否增加？
其它 Query 是否受影响？
```

这一步叫 Verification。

---

# 12. Case：最近 20 条为什么突然变慢

Query：

```sql
SELECT *
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

已有：

```sql
INDEX idx_user (user_id)
```

可能计划：

```text
通过 user_id 找到大量 Row
→ 回表
→ Filter tenant_id
→ Sort created_at
→ LIMIT 20
```

改成：

```sql
INDEX idx_tenant_user_created (
    tenant_id,
    user_id,
    created_at
)
```

理想路径可能变成：

```text
直接定位 tenant + user Range
→ 利用 created_at Index Order
→ 拿前 20
→ 停止
```

这不是“加了一个 Index 所以快”，而是：

> **整个 Access Path 变了。**

---

# 13. Case：明明加了 Index 还是慢

Query：

```sql
SELECT *
FROM agent_runs
WHERE status = 'SUCCEEDED';
```

Index：

```sql
INDEX idx_status(status)
```

如果 90% Row 都符合：

```text
Index 找到 4500 万
→ 4500 万次级别的 Row Access / 回表
→ 返回巨大结果
```

真正问题可能是：

```text
Query 本身要求太多数据
```

应改产品 / API：

- Pagination；
- Aggregate；
- Filter；
- Export Job；
- Offline Analytics。

不要继续堆 Index。

---

# 14. Case：Estimate 和 Actual 差很多

假设 `EXPLAIN ANALYZE` 看到：

```text
estimated rows = 500
actual rows = 800000
```

接下来要问：

```text
Statistics 是否过时？
Data Distribution 是否严重倾斜？
Predicate 是否高度相关？
Histogram 是否能帮助？
Index 设计是否匹配？
```

这比“Optimizer 很笨”更有工程意义。

---

# 15. 面试怎么答

## Q：你怎么排查 Slow SQL？

🎯 **推荐框架**：

> 我会先确认慢 SQL 的完整 SQL、参数、频率和延迟分位，然后看表结构、索引和数据分布。接着用 EXPLAIN 看 Access Type、候选 / 最终 Index、估算 Rows、Join 顺序、Sort / Temporary、Covering / ICP 等；环境允许时用 EXPLAIN ANALYZE 对比 Estimated 与 Actual。再判断瓶颈到底是扫描 / 回表 / 排序 / Join，还是 Lock Wait、I/O、Buffer Pool 或返回数据量。修改 SQL 或 Index 后必须重新看 Plan 和 Latency，避免只凭“加索引”猜。

## Q：看到 `type=ALL` 怎么办？

> 先看表规模和查询返回比例。大表上本来只需少量数据却 ALL，通常要重点检查 Index / Predicate；但小表或 Query 本来就要大部分数据时，Full Scan 可能是合理的 Cost Choice。

## Q：`rows` 是实际扫描行数吗？

> 传统 EXPLAIN 的 rows 主要是估算。要看实际运行，可以使用 EXPLAIN ANALYZE 等手段比较估计和实际。

---

# 16. 高频易错点

⚠️ **只看 `key`，不看扫描规模。**

⚠️ **`type=index` 就认为非常快。**  
可能是在全 Index Scan。

⚠️ **`ALL` 一定错误。**  
小表 / 大返回比例时可能合理。

⚠️ **`rows` 当实际值。**

⚠️ **`Using filesort` 一定落磁盘。**  
名字不能这样直译。

⚠️ **Slow SQL = Index 问题。**  
Lock、I/O、CPU、Network、结果集大小都可能是原因。

---

# 17. 本章自测

<details>
<summary>1. EXPLAIN 和 EXPLAIN ANALYZE 最大区别是什么？</summary>

EXPLAIN 主要展示 Optimizer 计划与估算；EXPLAIN ANALYZE 会实际执行并提供测量信息，可以用于比较 Estimated 和 Actual，因此使用时要考虑真实执行成本。

</details>

<details>
<summary>2. 为什么 `possible_keys` 有值但 `key=NULL` 不等于索引坏了？</summary>

说明 Optimizer 识别到候选 Index，但最终可能因为 Selectivity、回表或其它成本判断选择了不同访问方式。

</details>

<details>
<summary>3. `Using index` 与 `Using index condition` 有什么区别？</summary>

前者通常和 Covering / Index-only Access 有关；后者表示 ICP，即先在 Index Tuple 上判断可下推条件，减少完整 Row Access。

</details>

<details>
<summary>4. 为什么 Slow SQL 修复后还必须重新测？</summary>

因为一个看起来合理的 Index 可能没有改变最终 Plan，也可能改善读性能却显著增加写成本。必须验证实际 Plan、Rows、Latency 和对其它 Workload 的影响。

</details>

---

# 18. 官方资料

- MySQL 8.4 — Understanding the Query Execution Plan  
  <https://dev.mysql.com/doc/refman/8.4/en/execution-plan-information.html>
- MySQL 8.4 — Optimizing Queries with EXPLAIN  
  <https://dev.mysql.com/doc/refman/8.4/en/using-explain.html>
- MySQL 8.4 — EXPLAIN Statement  
  <https://dev.mysql.com/doc/refman/8.4/en/explain.html>
- MySQL 8.4 — EXPLAIN Output Format  
  <https://dev.mysql.com/doc/refman/8.4/en/explain-output.html>

到这里，**查询性能 Part A 的第一条完整链已经闭环**：

```text
SQL
→ Optimizer
→ Index
→ B+Tree
→ Clustered / Secondary
→ Composite
→ Covering / ICP
→ Index Cost Choice
→ EXPLAIN / Verification
```

下一章把 Index 继续推进到写入和长期演进：

> **Primary Key Design 与 Index Lifecycle。**
