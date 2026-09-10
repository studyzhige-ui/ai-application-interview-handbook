# 21. Bulk Write 与 MySQL Write Path

这一章讨论一个很典型的 AI 数据工程问题：

> **一次要写入几百万、几千万甚至更多数据，为什么逐行 INSERT 很慢？怎样把吞吐提上去，同时不把事务、Redo、Binlog、索引和 Replica 压垮？**

这不是单纯记一个：

```sql
INSERT INTO ... VALUES (...), (...), (...)
```

真正要理解的是 MySQL 写路径上的成本来自哪里。

---

## 1. 先讲人话：每次写入不是“只改一行”

一条 INSERT 背后可能涉及：

```text
SQL Parse / Execute
→ Buffer Pool Page 修改
→ 聚簇索引维护
→ 多个二级索引维护
→ Undo
→ Redo
→ Binlog
→ Commit / fsync
→ Replica Apply
```

所以一亿次单行写入绝不是“一亿次简单赋值”。

---

# 2. 为什么单行 Autocommit 很贵

如果：

```text
INSERT 1 row
COMMIT
INSERT 1 row
COMMIT
...
```

每条记录都形成一个独立事务。

提交路径可能频繁触发：

```text
Redo / Binlog Flush
Transaction bookkeeping
Network round trip
```

吞吐很容易被：

```text
Commit Rate
```

卡住。

---

# 3. Batch Insert 是最基础优化

例如：

```sql
INSERT INTO messages(conversation_id, role, content)
VALUES
  (1, 'user', 'a'),
  (1, 'assistant', 'b'),
  (1, 'user', 'c');
```

相较逐行发送：

```text
减少 SQL Round Trip
减少 Parse / Execute 次数
减少 Commit 次数
提高 Group Commit 利用
```

但：

> Batch 不是越大越好。

---

# 4. Batch Size 为什么要控制

如果一次：

```text
INSERT 500 万行
```

放在一个超大事务中，可能造成：

- 超大 Undo；
- Redo / Binlog Burst；
- 长时间持锁；
- Replica Apply Lag；
- 回滚极慢；
- 单次失败重做成本高；
- 内存 / Packet 压力。

所以工程上通常需要：

```text
合理 Batch Size
+
合理 Transaction Size
```

而不是：

> “越大越省提交，直接一个事务做完。”

---

# 5. 一个更合理的 Bulk Pipeline

```text
Input Stream
   ↓
Read N rows
   ↓
Validate / Transform
   ↓
Batch INSERT
   ↓
COMMIT
   ↓
Checkpoint
   ↓
Next Batch
```

关键属性：

```text
Bounded Memory
Bounded Transaction
Recoverable
Observable
```

这已经开始与 Backend Engineering 的 Batch / Backpressure 思想相连。

---

# 6. Secondary Index 为什么会拖慢 Bulk Write

每写一行：

```text
Clustered Index
+
idx_a
+
idx_b
+
idx_c
```

都要维护对应 B+Tree。

如果有 10 个二级索引：

> 写入不是只维护一棵树，而是很多棵树。

因此批量导入前要问：

```text
这些 Index 都是必须的吗？
能否在离线新表加载完数据后再建部分 Index？
是否存在完全不用的冗余 Index？
```

⚠️ 生产已有表不能为了导入随便删关键索引，需要综合查询流量、锁和建索引时间评估。

---

# 7. 主键顺序对 Bulk Insert 的影响

如果使用：

```text
随机 UUID 作为 Clustered PK
```

大量新行可能随机插入 B+Tree 各处：

```text
Page Split
Random Page Touch
Lower Locality
```

如果主键更接近单调增长：

```text
新数据主要追加到 B+Tree 尾部区域
```

通常写局部性更好。

这就是第 10 章主键设计在 Bulk Load 场景里的实际价值。

---

# 8. Redo / Binlog 为什么会成为瓶颈

写入吞吐提升以后：

```text
SQL 本身可能已经不慢
```

瓶颈会转移到：

```text
Redo Generation
Binlog Generation
Disk Flush
Group Commit
```

需要看：

- Commit Latency；
- Redo Rate；
- Binlog Rate；
- Disk IOPS / Throughput；
- fsync；
- Checkpoint Pressure。

不能只盯：

```text
QPS
```

---

# 9. Buffer Pool 与 Dirty Page

Bulk Write 会快速制造 Dirty Page。

简化链路：

```text
INSERT / UPDATE
→ Buffer Pool Page Modified
→ Dirty Page 增加
→ 后台 Flush
```

如果写入速度长期大于磁盘可持续 Flush 能力：

```text
Dirty Page / Redo Pressure 上升
→ 系统开始更激进 Flush
→ Latency 抖动
```

所以 Bulk Load 要关心的是：

> **可持续吞吐，而不是前 10 秒的峰值吞吐。**

---

# 10. `LOAD DATA` 为什么可能更快

对于结构化文件导入，MySQL 提供专门批量加载能力，例如：

```sql
LOAD DATA ...
```

相较大量独立 INSERT，它可以减少客户端协议和 SQL 解析开销。

但要考虑：

- 数据格式；
- 权限；
- Validation；
- Error Handling；
- 生产环境安全；
- 是否是在线表。

所以它是 Bulk Load 工具，不是所有业务写入的替代品。

---

# 11. Update / Upsert 比纯 Insert 更重

如果批量写是：

```sql
INSERT ... ON DUPLICATE KEY UPDATE ...
```

数据库还要：

```text
检查 Unique Key
判断冲突
执行 Update
维护更多 Index / Undo
```

所以 Upsert-heavy Pipeline 的吞吐通常不能直接套用纯 Append-only Insert 的预期。

---

# 12. 为什么“每 1000 条提交”不是固定答案

Batch Size 受很多因素影响：

```text
单行大小
Index 数量
磁盘能力
Replication
锁范围
网络延迟
失败恢复粒度
```

因此更正确的调优方式是：

```text
100
500
1000
5000
...
```

逐步 Benchmark：

```text
Throughput
P95 Commit Latency
Redo / Binlog Rate
Replica Lag
CPU / I/O
Failure Recovery Time
```

而不是背：

> “MySQL 批量写每 1000 条最优。”

---

# 13. Replication Lag 为什么容易被 Bulk Write 打爆

Source：

```text
一次快速提交大量变化
```

Replica：

```text
需要逐步 Apply
```

如果 Apply Capacity 低于 Source 产生速度：

```text
Lag 持续增加
```

所以导入时不能只看 Source 吞吐。

需要同时观察：

```text
Replica Delay
```

否则：

```text
主库导完很开心
从库落后 2 小时
```

读写分离请求就可能大量读旧数据。

---

# 14. Retry 为什么必须配 Idempotency

假设 Batch 17：

```text
客户端 Timeout
```

你不知道：

```text
MySQL 完全没收到？
已提交但响应丢了？
提交了一部分？
```

如果直接 Retry：

```text
可能重复数据
```

所以 Bulk Pipeline 常需要：

- Business Unique Key；
- Idempotent Upsert；
- Batch ID；
- Checkpoint；
- Import Job State。

这让失败可以安全重试。

---

# 15. Checkpoint 为什么重要

一亿行导入跑了 3 小时，在第 9000 万行失败。

如果没有 Checkpoint：

```text
从 0 重来
```

非常浪费。

更成熟：

```text
Batch 1 ✓
Batch 2 ✓
...
Batch 90000 ✓
Batch 90001 failed
```

恢复：

```text
从最近安全 Checkpoint 继续
```

注意：

> Checkpoint / Resume 的通用系统设计属于 Backend / System Design；本章只讲它为什么对 MySQL Bulk Write 必要。

---

# 16. Backpressure

如果上游能产生：

```text
100k rows/s
```

MySQL 只能稳定写：

```text
30k rows/s
```

如果没有 Backpressure：

```text
Queue / Memory 无限增长
→ OOM / Timeout / Retry Storm
```

所以生产 Pipeline 应让：

```text
Producer Rate
≈
Consumer Sustainable Capacity
```

这通常通过：

- Bounded Queue；
- Concurrency Limit；
- Rate Limit；
- Batch Dynamic Tuning；

实现。

---

# 17. AI Application 场景：Knowledge Base Metadata Import

假设企业一次导入：

```text
1000 万 documents metadata
```

一个合理流程：

```text
Object List
→ Stream Read
→ Validate
→ Batch Insert MySQL
→ Commit
→ Checkpoint
→ CDC / Queue
→ Async Parse / Embedding
```

不要：

```text
一次 HTTP Request
→ 读完 1000 万条到内存
→ 一个巨大 Transaction
→ 同步生成所有 Embedding
→ 最后 COMMIT
```

这是典型 Demo 思维，不是 Production Pipeline。

---

# 18. 面试怎么答

## Q：一亿条数据如何快速写入 MySQL？

🎯 推荐回答：

> 我会先确认是新表离线导入还是在线业务表。核心不是一个 SQL 技巧，而是控制写路径成本：使用 Multi-row Insert 或 LOAD DATA 减少 Round Trip 和 Parse；合理 Batch / Transaction Size 降低 Commit 次数但避免超大事务；检查二级索引、随机主键、Redo/Binlog 和磁盘 Flush；持续观察 Replica Lag；Pipeline 要有 Checkpoint、Idempotency、Retry 和 Backpressure。最终通过 Benchmark 找到可持续吞吐，而不是追求瞬时峰值。

---

# 19. 高频易错点

⚠️ **一个事务越大越快。**  
可能减少 Commit，但会放大 Undo、Log、Lock 和恢复成本。

⚠️ **Bulk Write 只看 Source QPS。**  
还要看 Disk、Redo、Binlog、Replica Lag。

⚠️ **Batch Size 有固定最佳值。**  
依赖 Workload 和硬件。

⚠️ **Retry 失败 Batch 一定安全。**  
如果没有 Idempotency，可能重复写。

---

# 20. 本章自测

<details>
<summary>1. 为什么逐行 Autocommit 往往比 Batch Transaction 慢？</summary>

因为每行都会产生独立事务和提交路径开销，包括网络、Redo/Binlog 和同步持久化等；合理批处理可以摊薄这些固定成本。

</details>

<details>
<summary>2. 为什么超大事务也不好？</summary>

会产生大量 Undo、Redo/Binlog Burst、长锁、长回滚、Replica Lag 和失败重做成本，降低系统可恢复性。

</details>

<details>
<summary>3. 为什么 Bulk Write 要配 Checkpoint 和 Idempotency？</summary>

长任务中间可能失败或超时。Checkpoint 让任务能从安全位置恢复，Idempotency 保证重放 Batch 不会产生重复或错误状态。

</details>

---

## 继续学习

到这里 MySQL 自身的核心机制、Scale 和 Data Pipeline 已经基本闭环。

下一章不再继续堆数据库八股，而是把这些机制放回我们的目标岗位：

> **AI Application 到底应该怎么在 MySQL 里建模？**

下一章：**AI Application Data Modeling。**
