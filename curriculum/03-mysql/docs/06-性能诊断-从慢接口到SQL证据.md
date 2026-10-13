# 06｜性能诊断：从慢接口到 SQL 证据

> [!TIP]
> **🎯 本章目标**
>
> 建立严谨的线上性能排障与调优工程闭环：线上接口响应变慢时，能够利用 APM、Trace 与链路指标逐层定界，准确区分应用自身、下游 RPC、连接池等待、网络 RTT、锁等待与 SQL 自身执行耗时；在确认 SQL 自身执行慢后，能通过执行计划看清访问路径、扫描行数与额外开销，并熟练使用 `EXPLAIN ANALYZE` 抓出优化器选错计划的证据；掌握深度分页（Deep Pagination）的物理成因与优化方案，并在统一基准下完成调优闭环证明。

## 0. 接口 P99 飙升，第一反应抓慢 SQL 为什么经常走弯路？

线上一个核心查询接口的 P99 延迟突然从 50ms 飙升至 2.5s。很多工程师的第一反应是立即登录数据库查看 Slow Query Log，或者把接口里的主 SQL 复制到客户端工具执行，结果却发现该 SQL 单独运行只要 3ms。

这是典型的“排障定界错位”。线上一次 HTTP 请求变慢，可能发生在链路上的任何环节：
- 应用进程自身发生频繁 Full GC、内存抖动或 CPU 争抢，导致应用线程暂停；
- 下游第三方支付、外部鉴权或微服务 RPC 响应缓慢，拖垮了整个调用链路；
- 应用数据库连接池（Connection Pool）最大连接数耗尽，业务线程在本地排队等待空闲连接；
- 事务未提交持有了行排他锁，该 SQL 在 MySQL 内部陷入了长达数秒的锁等待（Lock Wait）；
- SQL 自身在某些特定参数、高并发或数据倾斜下，确实触发了全表扫描与大范围数据页搬迁。

如果不经定界就一头扎进 SQL 文本改写或盲目加索引，往往不仅无法解决问题，还会引入额外的索引维护开销。

> [!IMPORTANT]
> **💡 核心认知：性能排障必须遵循“证据链逐层下钻”原则——先用全链路监控证明“瓶颈确实在数据库访问”，再区分“是连接等待/锁阻塞还是 SQL 执行慢”，最后针对慢 SQL 分析执行计划并验证优化效果。**

---

## 🗺️ 本章知识图

```text
线上接口变慢后，怎样逐层排查并调优？
│
├── 1. 线上接口变慢，怎样判断是不是数据库问题？
│   ├── 分布式链路追踪 (APM / Trace / Span 时间线)
│   ├── 服务端核心指标 (P95/P99 延迟、QPS、错误率)
│   └── 快速定界：隔离应用业务逻辑、外部 RPC 与数据库调用
│
├── 2. 数据库链路慢，怎样进一步定位瓶颈在哪里？
│   ├── 客户端排队：连接池耗尽 (Pool Pending / Timeout)
│   ├── 传输与实例开销：网络 RTT 与 MySQL 实例负载 (CPU / IOPS)
│   ├── 事务阻塞：行锁/元数据锁等待 (Lock Wait) vs 纯执行耗时
│   └── 定位慢 SQL：Slow Query Log 关键行与 sys / Performance Schema
│
├── 3. 如何排查慢 SQL？怎样通过执行计划定位性能瓶颈？
│   ├── 排查三步法：看访问类型 → 看扫描过滤行数 → 看 Extra 额外操作
│   ├── 驱动表与访问路径：驱动表确定与 type 等级判定
│   ├── 键长推导与扫描基数：key_len 与 rows * (1 - filtered) 无效扫描
│   └── Extra 关键信息：Using filesort、Using temporary 与 Covering
│
├── 4. 执行计划看着正常但实际很慢，怎样用 EXPLAIN ANALYZE 抓出误判证据？
│   ├── Iterator 执行模型：actual time (单次循环)、rows (单次循环平均行数) 与 loops
│   └── 识别计划选错：统计信息失真与基数估算巨大偏差
│
├── 5. SQL 调优后，怎样证明优化真正有效，而不是碰巧跑得快？
│   ├── 调优闭环四步法：基线采集 → 假设验证 → 控制变量修改 → 结果对照
│   └── 验证指标：Handler_read 计数与真实扫描行数对比
│
└── 6. 为什么深分页越翻越慢，有哪些标准工程解法？
    ├── LIMIT offset, N 的物理本质：全量检索后在 Server 层丢弃
    ├── 延迟关联 (Delayed Join)：利用覆盖索引轻量跳过 offset
    └── 游标寻址 (Keyset Pagination)：消除 offset 位移，化偏移扫描为索引定位
```

---

## 1. 线上接口变慢，怎样判断是不是数据库问题？

排障的第一步是**全局视角的时间线切分（Time Budgeting）**。标准接口调用的总耗时由应用本地处理、下游 RPC 依赖与数据库交互三部分构成：

$$\text{Total Duration} = \text{App Time} + \sum \text{RPC Time} + \sum \text{DB Time}$$

```text
HTTP Request (总耗时 2500ms)
├── App Local: 参数校验与业务计算 (10ms)
├── RPC Call:  用户中心鉴权 (30ms)
└── DB Access: 数据库交互 (2460ms) ← 瓶颈锁定在数据库链路
```

工业界标准的做法是依赖 **APM（应用性能监控，如 SkyWalking、OpenTelemetry、Datadog）** 提取完整的分布式调用链（Trace）。每个 Trace 内部由层级嵌套的 Span 构成，每个 Span 记录了自身操作的起始时间与持续时间。

只有当 APM 或监控指标明确显示数据库 Span 的 P95/P99 耗时占据了整个接口响应时间的大头时，才能将排查方向收敛至数据库链路；若 Span 表明耗时发生在外部 HTTP 调用或本地序列化，应立即终止 SQL 调优，避免误诊。

---

## 2. 数据库链路慢，怎样进一步定位瓶颈在哪里？

数据库链路耗时增加不能直接等同于“SQL 本身慢”，必须沿着调用生命周期逐层定界三个核心环节：排查应用客户端是否在连接池获取连接（`getConnection()`）处耗尽排队；排查 SQL 进入实例后是否因行锁或元数据锁陷入等待；排查存储引擎内部是否产生了海量物理数据页扫描，最终借助慢日志与 Performance Schema 锁定目标 SQL。

从应用发出一句 SQL 到拿到结果，物理上跨越的阶段如下：

```text
应用线程 → [1. 连接池获取连接] → [2. 网络发送] → [3. MySQL 实例排队/等锁] → [4. 引擎执行扫描] → [5. 结果网络回传]
```

---

### 2.1 区分连接池排队、锁等待与 SQL 自身执行

- **连接池排队（Connection Pool Pending）**：应用程序通常使用 HikariCP 或 Druid 等连接池。若连接池最大连接数偏小，或并发请求激增，大量线程会阻塞在 `getConnection()` 上。此时应用侧统计到的“数据库调用耗时”可能高达数秒，但在 MySQL 内部该 SQL 的实际执行耗时可能只有 1ms。排查时应先观察应用连接池监控中的活跃连接数（Active Connections）与等待线程数（Pending Threads），并配置合理的获取连接超时阈值（`connectionTimeout`，如 1~2s）以实现快速失败，防止上游线程池被全量耗尽。
- **锁等待（Lock Wait）**：SQL 进入 MySQL 后，由于与其他未提交的事务争抢同一行数据的行排他锁（X 锁），或触发了元数据锁（MDL），SQL 处于阻塞挂起状态。可通过查询 `sys.innodb_lock_waits` 确认当前是否存在严重的锁等待链条。
- **纯执行耗时（Execution Time）**：SQL 在存储引擎内部确实进行了大量的逻辑页寻道与全表物理扫描。

---

### 2.2 捕获慢 SQL 的核心武器：Slow Log 与 Performance Schema

要找出生产环境中真正耗费资源的 SQL，主要依赖两大系统工具：

#### 1. Slow Query Log（慢查询日志）
由 `slow_query_log=ON` 开启，阈值由 `long_query_time` 控制。生产环境典型的慢日志样本如下：

```text
# Time: 2026-10-12T14:32:01.102345Z
# User@Host: app_user[app] @ [10.0.1.25]  Id:  10482
# Query_time: 2.341200  Lock_time: 0.000120  Rows_sent: 20  Rows_examined: 1000020
SET timestamp=1791815521;
SELECT id, title, content FROM tasks WHERE tenant_id = 10 ORDER BY id LIMIT 1000000, 20;
```

重点提取四项关键证据：
- `Query_time`（总耗时 2.34s）与 `Lock_time`（等锁 0.12ms）：对比可瞬间确认该 SQL **不是被锁卡住，而是纯执行慢**；
- `Rows_sent`（实际返回 20 行）与 **`Rows_examined`（引擎实际检查了 100 万行）**：两者极其悬殊，直接证实底层发生了海量无效扫描。

#### 2. Performance Schema 与 sys schema
慢日志基于单次静态耗时阈值，容易漏掉那些单次耗时只有 5ms、但每秒被高并发调用上万次从而把 CPU 彻底打满的高频 SQL。此时可查询 `sys.statement_analysis`（基于规范化 SQL 指纹 Digest 聚合统计），直接定位全局消耗总时间最长（`total_latency`）、扫描总行数最多（`rows_examined`）或单次平均扫描行数最多（`rows_examined_avg`）的核心 SQL。

---

## 3. 如何排查慢 SQL？怎样通过执行计划定位性能瓶颈？

排查慢 SQL 时，核心是通过 `EXPLAIN` 查看执行计划，搞清楚数据库到底是怎么查数据的，重点看三部分信息：
1. **看索引与访问类型（`table`、`type`、`key`）**：确认单表访问是否走了索引，是不是退化成了全表扫描（`ALL`）或全索引扫描（`index`）；多表关联时看驱动表选得对不对、被驱动表的关联列有没有建立索引；
2. **看预估扫描行数与过滤比例（`rows`、`filtered`）**：看优化器预估要扫多少行数据，经过条件过滤后能留下百分之几，判断是否存在大量无效扫描；
3. **看 Extra 里的额外操作**：重点关注是否出现了耗费资源的外部排序（`Using filesort`）或临时表（`Using temporary`），以及是否用上了覆盖索引（`Using index`）或索引条件下推（`Using index condition`）。

确认具体瓶颈后，再针对性地设计联合索引、消除无用字段查询或重写 SQL。

以一条典型的多租户任务查询为例，通过 `EXPLAIN` 分析上述三部分信息的过程如下：

```sql
EXPLAIN
SELECT t.id, t.title
FROM tasks AS t
WHERE t.tenant_id = 10 AND t.status = 'pending'
ORDER BY t.created_at DESC
LIMIT 20;
```

| id | select_type | table | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 | SIMPLE | t | ref | idx_tenant_status_created,idx_tenant | idx_tenant_status_created | 90 | const,const | 850 | 100.00 | Backward index scan |

---

### 3.1 步骤一：看驱动表与访问路径（table、type 与 key）

- **确认多表关联的驱动表（`table`）**：在多表关联的 EXPLAIN 报表中，**排在第一行的是驱动表（Driving Table）**，后续为被驱动表。驱动表决定了外层循环的轮次，驱动表选错会导致整个中间结果急剧膨胀。
- **判断单表访问类型（`type`）**：
  - `const / eq_ref`：主键或唯一索引等值点查，最多命中一行，单次寻道到达极致；
  - `ref`：普通二级索引等值匹配，锁定连续索引切片；
  - `range`：索引范围扫描（`>`、`<`、`BETWEEN`、`IN`）；
  - `index`：全索引扫描（Full Index Scan），虽然可能免回表，但仍需遍历整棵索引树的所有叶子页；
  - `ALL`：全表扫描（Full Table Scan），性能最差，必须逐个物理加载并遍历聚簇索引的所有数据页。
- **校验命中索引与键长（`key` 与 `key_len`）**：`key` 为 `NULL` 说明优化器完全放弃了索引；而通过 `key_len` 消耗的字节数，能精准推导联合索引到底被利用到了第几列（例如在 `utf8mb4` 下 `NOT NULL` 的 `tenant_id BIGINT(8B) + status VARCHAR(20)(20×4 + 2 = 82B) = 90B`，说明前两列成功用于等值定位）。

---

### 3.2 步骤二：看扫描行数与过滤效率（rows 与 filtered）

优化器预估的 `rows` 并不代表最终返回行数，而是**预计需要检查并加载的候选行数**。
- **计算无效扫描损耗**：$\text{预计浪费行数} = \text{rows} \times (1 - \text{filtered}\%)$。若 `rows = 100000` 且 `filtered = 0.1%`，意味着存储引擎加载并向 Server 递交了 10 万行数据，结果 99.9% 的数据全被 Server 层在内存中过滤抛弃。这明确证明当前过滤条件缺乏索引支撑，产生了大范围的无效扫描。

---

### 3.3 步骤三：看 Extra 里的额外操作

`Extra` 列记录了查询执行过程中的关键补充信息，往往暴露了最直接的性能损耗点：
- **`Using filesort`（高危）**：当前查询的排序无法直接借用索引的物理有序性，优化器不得不将记录调入内存（`sort_buffer`）甚至临时磁盘文件执行排序算法。在高并发场景下会显著推高 CPU 与内存开销。
- **`Using temporary`（高危）**：为了完成复杂的 `GROUP BY` 或跨表聚合，MySQL 在内存（或磁盘）中构建了内部临时表，开销极大。
- **`Using index condition`（收益）**：触发**索引下推（ICP）**，存储引擎在回表前先在二级索引叶子页就地过滤掉不符合条件的记录，显著遏制无效回表。
- **`Using index`（最佳）**：触发**覆盖索引**，查询所需的列全在当前二级索引树内，回表次数直接归零。

---

## 4. 执行计划看着正常但实际很慢，怎样用 EXPLAIN ANALYZE 抓出误判证据？

当一条 SQL 的执行计划看似正常（如走索引 `type=ref`）但生产运行严重超时时，根本原因通常是**采样统计信息失真，导致优化器的成本模型做出了严重误判**。

排查这类问题的核心武器是 MySQL 8.0 引入的 `EXPLAIN ANALYZE`。它会真正执行 SQL，并基于火山/迭代器（Iterator）模型输出树状的真实物理运行审计报表。抓取误判证据的核心是**比对同维度的静态预估行数与实际单次产出行数（estimated `rows` vs actual `rows`），并关注驱动循环次数（`loops`）与累计总行数（`actual rows * loops`）**：
一旦发现驱动表实际产出远超预估，导致外层循环次数（`loops`）暴增数万倍，被驱动表即便走索引也会被循环调用拖垮。通过比对这种倍率偏差，便能确凿证实优化器选错了执行计划。

典型执行分析如下：

```sql
EXPLAIN ANALYZE
SELECT m.name, t.title
FROM members AS m
JOIN tasks AS t ON t.owner_id = m.id
WHERE m.tenant_id = 10 AND t.status = 'pending';
```

执行报表解读：

```text
-> Nested loop inner join  (cost=1250.40 rows=850) (actual time=0.150..8.420 rows=320 loops=1)
    -> Filter: (m.tenant_id = 10)  (cost=105.20 rows=100) (actual time=0.080..0.950 rows=50 loops=1)
        -> Index scan on m using idx_members_tenant  (cost=105.20 rows=100) (actual time=0.075..0.910 rows=100 loops=1)
    -> Index lookup on t using idx_tasks_owner (owner_id=m.id), with index condition: (t.status = 'pending')  (cost=10.50 rows=8.5) (actual time=0.065..0.072 rows=6.4 loops=50)
```

### 迭代器执行树核心指标剖析：
1. **`actual time=0.065..0.072`**：该迭代器**单次循环（Per Loop）**的耗时统计。`0.065` 表示产出首行耗时，`0.072` 表示产出该循环全部匹配行耗时；
2. **`loops=50`**：被外层驱动循环调用的总次数。这里驱动表输出了 50 个成员，因此被驱动表查询循环了 50 次；
3. **`rows=6.4`**：该迭代器在每次循环中**单次平均产出**的行数（$6.4 \times 50 \approx 320$ 真实累计总行数）。

> [!TIP]
> **排查“选错索引”的神器与治理手段：** 重点比对静态估算 `(rows=...)` 与实际单次产出 `(actual ... rows=...)`。若优化器预估驱动表只返回 5 行，实际返回了 50,000 行，外层循环直接暴增 10,000 倍，被驱动表即便走索引也会被循环调用 5 万次而彻底拖垮。这直接证明了采样统计信息严重失真。在工程上，确认统计信息过期后，可执行 `ANALYZE TABLE 表名` 重新采样更新 InnoDB 持久化索引统计信息；若在数据剧烈倾斜下优化器依然误判，再配合索引重构或 Optimizer Hints（如 `JOIN_ORDER` 或 `FORCE INDEX`）进行显式干预。

---

## 5. SQL 调优后，怎样证明优化真正有效，而不是碰巧跑得快？

证明慢 SQL 优化真正有效的核心原则是：**必须在相同测试基线下，看扫描行数和读取操作有没有真正降下来，而不是单看单次执行耗时**。

因为单次耗时极易受到系统 CPU 负载波动和 Buffer Pool 缓存命中率（冷热数据）的干扰。在工程上，标准的验证方法主要看三项关键指标：
1. **执行计划路径升级**：`type` 从全表扫描 `ALL` 优化为索引精确定位 `ref` 或范围扫描 `range`，`Extra` 消除 `Using filesort` 并实现 `Using index` 覆盖；
2. **底层 Handler 读取计数骤降**：通过 `SHOW STATUS LIKE 'Handler_read%'` 验证，代表全表遍历的 `Handler_read_rnd_next` 归零，走索引定位的 `Handler_read_key` 成为主力；
3. **检查行数（Rows_examined）大幅下降**：实际读取与检查的数据行数实现数量级压缩。

标准的工程实验闭环流程如下：

```text
① 基线采集 (Baseline)
   在相同测试参数、数据量与 Buffer Pool 状态下，记录当前执行计划与各读取指标
        ↓
② 形成调优假设 (Hypothesis)
   推导瓶颈：是发生了大量离散回表？还是排序列没有走索引引发了 filesort？
        ↓
③ 单一变量改写 (Controlled Modification)
   针对性建立精简联合索引，或重写查询语义（避免宽表 SELECT * 或消除无效 JOIN）
        ↓
④ 闭环证据对照 (Verification)
   验证改写后 EXPLAIN 的 type、key、Extra 是否符合预期；重点对比扫描与读取行数
```

### 优化前后指标对比

四步验证法在量化结果上的对照体现如下：

| 评估指标 | 优化前 (全表扫描 + filesort) | 优化后 (覆盖索引) | 物理含义与工程收益 |
|---|:---:|:---:|---|
| **EXPLAIN type** | `ALL` | `ref` / `range` | 访问路径从全表遍历升级为索引精确定位 |
| **EXPLAIN Extra** | `Using filesort` | `Using index` | 彻底消除临时内存排序，实现免回表直接交付 |
| **Handler_read_rnd_next** | 1,000,000 | 0 | 存储引擎顺序遍历整表数据行的次数**归零** |
| **Handler_read_key** | 0 | 1 | 存储引擎通过 B+Tree 索引发起精确定位的次数 |
| **Rows_examined** | 1,000,000 | 20 | 实际检查记录数压缩 50,000 倍 |

---

## 6. 为什么深分页越翻越慢，有哪些标准工程解法？

深度分页越翻越慢的物理本质是：**`LIMIT offset, N` 必须先从存储引擎全量检索并加载前 $offset + N$ 行记录，然后在 Server 层抛弃前 $offset$ 行，只保留最后的 $N$ 行**。当 $offset$ 达到数十万时，会引发数十万次无意义的数据页读取和随机回表 IO。

标准的工程解法主要有两种：
1. **延迟关联（Delayed Join）**：利用覆盖索引仅扫描主键 `id` 快速跳过 $offset$，再通过子查询与原表按主键关联查出所需列，将海量非主键列的回表开销压缩为仅剩最后 $N$ 行；
2. **游标寻址分页（Keyset / Seek Pagination）**：记录上一页最后一条记录的排序键值（如 `WHERE id > last_seen_id ORDER BY id ASC LIMIT N`），利用 B+Tree 索引直接定位起点并向后连续扫描 $N$ 行，彻底消除 $offset$ 带来的无效检索。

典型慢分页案例如下：

```sql
SELECT id, title, content
FROM tasks
WHERE tenant_id = 10
ORDER BY id
LIMIT 1000000, 20;
```

---

### 6.1 为什么越翻越慢？LIMIT offset, N 的物理本质

很多人误以为 `LIMIT 1000000, 20` 是“跳过前 100 万条，只读后面的 20 条”。在物理层完全相反：

存储引擎必须从第一条开始，**完整扫描并提取整整 1,000,020 条物理记录交付给 MySQL Server，Server 层在内存中丢弃前 1,000,000 条，最终只将最后 20 条回传给客户端。** 更严重的是，由于查询包含了未被二级索引覆盖的列（`title, content`），二级索引每扫过一条满足 `tenant_id = 10` 的索引项，都必须拿着主键回聚簇索引树加载一次完整数据页。翻到百万页深处时，系统实际付出了整整 100 万次离散随机回表 I/O 与反序列化开销，仅仅为了挑出最后 20 条。

---

### 6.2 方案一：延迟关联（Delayed Join）——让跳过变得更轻

若无法改变分页传参（前端强依赖页码跳转），可利用**覆盖索引**先快速完成位移，再通过主键关联取详情：

```sql
SELECT t.id, t.title, t.content
FROM tasks AS t
JOIN (
    -- 子查询仅在覆盖索引上完成 100 万行的轻量遍历，只提取主键 id，完全无需回表
    SELECT id
    FROM tasks
    WHERE tenant_id = 10
    ORDER BY id
    LIMIT 1000000, 20
) AS lim ON t.id = lim.id;
```

在子查询内部，引擎仅在紧凑的二级索引叶子页上高速跳过 100 万个轻量级主键；拿到最终 20 个主键后，外层主表仅需执行 20 次精确的聚簇索引回表。原本 100 万次沉重的数据页回表开销被直接压缩到了 20 次。

---

### 6.3 方案二：游标寻址（Keyset / Seek Pagination）——消除 OFFSET

在移动端无限滚动（Feed 流）或数据批量导出场景下，最彻底的方案是**摒弃 `OFFSET`，采用基于上一页游标的主键范围查找**：

```sql
-- 客户端携带上一页最后一条记录的主键 id (例如 1000000)
SELECT id, title, content
FROM tasks
WHERE tenant_id = 10
  AND id > 1000000
ORDER BY id ASC
LIMIT 20;
```

此时的物理执行路径变为：引擎直接通过多租户二级索引 `idx_tenant(tenant_id)`（叶子节点天然按 `(tenant_id, id)` 顺序排列）定位到 `(tenant_id=10, id=1000000)` 的叶子节点，随后沿着双向链表向后顺序扫描 20 条属于该租户的记录并精准回表 20 次即可立即返回。物理扫描行数不再随页码深度线性增长。

> [!NOTE]
> **Keyset 分页的工程适用边界：**  
> 1. **仅适用于连续流式翻页**：由于依赖上一页最后一条记录的锚点，Keyset 无法支持直接跳转到任意随机页码（如“直接跳转到第 15 页”）；  
> 2. **排序列必须保证唯一且单调**：若业务按非唯一列（如 `created_at`）排序，必须在排序列末尾追加主键构成复合游标 `(created_at, id)`，防止同一时间戳存在多条记录时在翻页边界发生漏读或重复。

---

## 本章总结

性能诊断绝非无序的试错，而是一场由表及里的证据调查。排障流程必须从全局 APM 与调用链监控出发，先将问题严格收敛在数据库层；进而剥离应用连接池排队与底层锁冲突，确认 SQL 自身的扫描开销。

`EXPLAIN` 是将逻辑 SQL 映射到物理成本的核心翻译器。通过分析访问路径 `type`、扫描基数 `rows` 与 `Extra` 中的下推/覆盖/排序标志，能够迅速洞悉物理开销的来源；配合现代 MySQL 的 `EXPLAIN ANALYZE`，能以迭代器级别的数据还原实际执行耗时并揪出估算偏差。

在面对深度分页等经典慢查询时，理解“全量扫描后丢弃”的物理本质是优化的前提；采用延迟关联降低回表密度，或使用 Keyset 游标化范围为点查，能彻底根治翻页性能崩溃。调优工作最终必须在严谨的控制变量下，以扫描行数与底层读取计数的实质下降作为验收依据。

<details>
<summary><strong>🗺️ 回看本章完整知识图</strong></summary>

```text
线上接口变慢后，怎样逐层排查并调优？
│
├── 1. 线上接口变慢，怎样判断是不是数据库问题？
│   ├── 分布式链路追踪 (APM / Trace / Span 时间线)
│   ├── 服务端核心指标 (P95/P99 延迟、QPS、错误率)
│   └── 快速定界：隔离应用业务逻辑、外部 RPC 与数据库调用
│
├── 2. 数据库链路慢，怎样进一步定位瓶颈在哪里？
│   ├── 客户端排队：连接池耗尽 (Pool Pending / Timeout)
│   ├── 传输与实例开销：网络 RTT 与 MySQL 实例负载 (CPU / IOPS)
│   ├── 事务阻塞：行锁/元数据锁等待 (Lock Wait) vs 纯执行耗时
│   └── 定位慢 SQL：Slow Query Log 关键行与 sys / Performance Schema
│
├── 3. 如何排查慢 SQL？怎样通过执行计划定位性能瓶颈？
│   ├── 排查三步法：看访问类型 → 看扫描过滤行数 → 看 Extra 额外操作
│   ├── 驱动表与访问路径：驱动表确定与 type 等级判定
│   ├── 键长推导与扫描基数：key_len 与 rows * (1 - filtered) 无效扫描
│   └── Extra 关键信息：Using filesort、Using temporary 与 Covering
│
├── 4. 执行计划看着正常但实际很慢，怎样用 EXPLAIN ANALYZE 抓出误判证据？
│   ├── Iterator 执行模型：actual time (单次循环)、rows (单次循环平均行数) 与 loops
│   └── 识别计划选错：统计信息失真与基数估算巨大偏差
│
├── 5. SQL 调优后，怎样证明优化真正有效，而不是碰巧跑得快？
│   ├── 调优闭环四步法：基线采集 → 假设验证 → 控制变量修改 → 结果对照
│   └── 验证指标：Handler_read 计数与真实扫描行数对比
│
└── 6. 为什么深分页越翻越慢，有哪些标准工程解法？
    ├── LIMIT offset, N 的物理本质：全量检索后在 Server 层丢弃
    ├── 延迟关联 (Delayed Join)：利用覆盖索引轻量跳过 offset
    └── 游标寻址 (Keyset Pagination)：消除 offset 位移，化偏移扫描为索引定位
```

</details>

---

## 🎯 面试怎么回答

### 线上接口变慢，你的完整排查思路是怎样的？

> [!TIP]
> 遵循“由外向内、逐层定界”的原则：  
> 1. 全局定界：通过 APM 调用链（Trace）观察时间线分布，确认延迟主要消耗在业务计算、外部微服务 RPC 还是数据库访问；  
> 2. 区分数据库瓶颈类型：若瓶颈在 DB 链路，先查应用连接池监控，确认是否是连接池耗尽排队；再查数据库锁等待，确认是否为事务行锁/MDL 阻塞；  
> 3. 诊断慢查询：确认是纯执行慢后，通过慢查询日志或 Performance Schema 抓取目标 SQL，使用 `EXPLAIN` 分析访问路径（type）、命中索引与 Extra，必要时用 `EXPLAIN ANALYZE` 对比估算偏差；  
> 4. 优化闭环：通过重构索引、改写语义或重塑分页消除全表扫描与 filesort，以扫描行数与 Handler 读取计数的显著减少证明调优成效。

### 拿到一条慢 SQL，你如何通过 EXPLAIN 分析它的瓶颈？

> [!TIP]
> 重点看三部分核心信息：  
> 1. 访问路径（type & key）：排查是否退化为全表扫描（`ALL`）或全索引扫描（`index`），检查实际使用的索引与 `key_len` 验证联合索引是否被截断；  
> 2. 过滤代价（rows & filtered）：检查预估扫描行数 `rows` 是否庞大，结合 `filtered` 评估是否有大量数据被扫描出来后全被 Server 层在内存中过滤丢弃；  
> 3. Extra 里的额外操作：高度警惕 `Using filesort`（内存/磁盘临时排序）与 `Using temporary`（内存临时表），优先争取 `Using index`（覆盖索引免回表）与 `Using index condition`（索引下推减少回表）。

### EXPLAIN ANALYZE 和普通 EXPLAIN 有什么区别？

> [!TIP]
> 普通 `EXPLAIN` 仅输出优化器在执行前根据统计信息计算出的静态估算计划；`EXPLAIN ANALYZE` 则会真实执行 SQL，基于迭代器模型逐层打印实际消耗时间（`actual time`）、单次循环平均行数（`rows`）与总循环调用次数（`loops`）。注意 `actual time` 和 `rows` 均为单次循环（Per Loop）的平均值，算子累计总耗时为 actual time × loops，累计产出总行数为 rows × loops。它是验证优化器是否因统计信息失真而选错索引的核心实证工具。

### 为什么深分页（LIMIT 1000000, 20）会极慢？如何优化？

> [!TIP]
> 本质原因是存储引擎必须全量读取前 1000020 条完整数据交付给 Server 层，Server 丢弃前百万条仅保留最后 20 条，产生了百万次数据页 I/O 与反序列化开销。  
> 优化方案：  
> 1. 延迟关联（Delayed Join）：在子查询中利用覆盖索引快速扫描主键并跳过 offset，外层仅按这 20 个主键回表拉取详情；  
> 2. Keyset / 游标分页：改用 `WHERE id > last_seen_id ORDER BY id ASC LIMIT 20`，直接利用主键索引树进行范围点查，彻底消灭 offset，扫描量恒定为 20 行。

---

## ⚠️ 易错点

> [!WARNING]
> **切勿脱离应用监控盲目抓慢 SQL。** 接口变慢极常由应用 GC 暂停、线程池被打满或连接池排队引起，盲改 SQL 无法解决非 SQL 瓶颈。

> [!WARNING]
> **`type = index` 绝非高效索引查找。** 它代表遍历整棵二级索引树的所有叶子节点，本质依然是一种全量扫描。

> [!WARNING]
> **`rows` 只是静态估算，非真实读取行数。** 真实开销应结合 `EXPLAIN ANALYZE` 的 `actual rows` 或系统的 `Handler_read%` 状态变量共同判定。

> [!WARNING]
> **`Using filesort` 并非绝对写了磁盘文件。** 当排序数据量小于系统参数 `sort_buffer_size` 时在内存中完成，但高并发下依然会造成剧烈的 CPU 开销。

> [!WARNING]
> **延迟关联无法减少二级索引扫描量。** 延迟关联优化的是“聚簇索引回表取完整数据行的次数”，并没有减少在二级索引上跳过 offset 的遍历量。

---

## 🧩 本章自测

<details>
<summary><strong>1. APM 中显示某个 SQL 调用耗时 3 秒，但慢日志中该 SQL 的 Query_time 只有 5 毫秒，可能的原因是什么？</strong></summary>

大部分时间耗费在了客户端获取数据库连接的排队等待（连接池瓶颈）或网络通信延迟上，SQL 在 MySQL 服务端内部的真实执行时间极短。

</details>

<details>
<summary><strong>2. 慢查询日志中的 Rows_examined 与 Rows_sent 有何诊断意义？</strong></summary>

`Rows_examined` 代表存储引擎实际扫描的记录行数，`Rows_sent` 代表最终交付给客户端的行数。若二者比值极为悬殊（如扫了 10 万行只返回 1 行），说明查询缺乏精确的索引收敛，存在巨大的无效过滤。

</details>

<details>
<summary><strong>3. 解释 EXPLAIN 输出中 key_len 的作用。</strong></summary>

`key_len` 表示优化器在命中联合索引时，实际使用了该索引的多少个字节长度。通过与各列类型的物理字节数比对，能准确判定联合索引到底被利用到了第几列。

</details>

<details>
<summary><strong>4. 在多表连接的 EXPLAIN 报表中，排在第一行的是什么表？</strong></summary>

是驱动表（Outer Table / Driving Table）。MySQL 会首先全量或按索引扫描该表，并以其输出作为外层循环去匹配后续的被驱动表。

</details>

<details>
<summary><strong>5. Extra 中出现 Using index 与 Using where 并存代表什么？</strong></summary>

代表查询所需的所有列均已被该索引覆盖（免回表），同时 Server 层依然利用索引列上的某些条件进行了解析过滤。

</details>

<details>
<summary><strong>6. 为什么说 EXPLAIN ANALYZE 会对生产数据库带来副作用？</strong></summary>

普通 `EXPLAIN` 只做静态模拟分析不产生实际运行，而 `EXPLAIN ANALYZE` 会真正把 SQL 在存储引擎中执行完毕，若分析的是包含全表扫描的慢写或慢查，会在生产环境造成真实的 I/O 与锁压力。

</details>

<details>
<summary><strong>7. 为什么延迟关联（Delayed Join）能够优化深分页？</strong></summary>

因为子查询只在二级索引上提取主键，避免了对前 offset 行数据进行沉重的聚簇数据页读取与整行解析；只有最终切出的 N 条数据才会真正触发回表。

</details>

<details>
<summary><strong>8. Keyset 分页（WHERE id > ? LIMIT N）的局限性是什么？</strong></summary>

它依赖排序列具有严格单调有序且唯一的物理特征，且不支持随机跳转到特定页码（如“直接跳到第 15 页”），仅适用于上下滚动或批量流式拉取。

</details>

<details>
<summary><strong>9. 怎样验证 SQL 调优确实减少了工作量，而非偶发性网络提速？</strong></summary>

通过监测 `Handler_read_rnd_next`（全表顺序扫描计数）是否显著下降，以及 `Handler_read_key`（索引精确寻道计数）的提升情况，考核底层物理操作计数而非脆弱的绝对耗时。

</details>

<details>
<summary><strong>10. 连接池的 Connection Timeout 通常应该怎样设置？</strong></summary>

应严格设置为较短的阈值（如 500ms~2s），快速失败，防止应用线程全量堆积在连接排队上引发线程池耗尽，进而拖垮整个服务的上游调用链路。

</details>

---

## 📌 本章最终要留下的六句话

1. **排障始于全链路定界，APM 证实瓶颈在 DB 前切勿盲改 SQL。**
2. **区分连接池排队、网络 RTT、事务锁阻塞与引擎纯执行耗时。**
3. **排查慢 SQL 看三件事：看访问类型、看扫描过滤行数、看 Extra 额外操作。**
4. **`EXPLAIN ANALYZE` 用真实运行指标检验静态预估，揪出统计偏差。**
5. **深分页慢在全量读取后丢弃，延迟关联控回表，Keyset 终结位移。**
6. **调优闭环以扫描行数与 Handler 读取计数的实质减少为最终依据。**

## 📚 权威资料

- [MySQL 9.7：Optimizing Queries with EXPLAIN](https://dev.mysql.com/doc/refman/9.7/en/using-explain.html)
- [MySQL 9.7：EXPLAIN Statement](https://dev.mysql.com/doc/refman/9.7/en/explain.html)
- [MySQL 9.7：The Slow Query Log](https://dev.mysql.com/doc/refman/9.7/en/slow-query-log.html)
- [MySQL 9.7：Performance Schema Overview](https://dev.mysql.com/doc/refman/9.7/en/performance-schema.html)
- [MySQL 9.7：sys Schema Overview](https://dev.mysql.com/doc/refman/9.7/en/sys-schema.html)
- [MySQL 9.7：Understanding the Query Execution Plan](https://dev.mysql.com/doc/refman/9.7/en/execution-plan-information.html)
- [MySQL 9.7：Server Status Variables (Handler_*)](https://dev.mysql.com/doc/refman/9.7/en/server-status-variables.html)
