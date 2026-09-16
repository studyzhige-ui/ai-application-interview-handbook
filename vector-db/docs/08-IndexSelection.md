# 08｜HNSW vs IVF 与 Index Selection

前面已经分别学了 HNSW、IVF 和 Quantization，现在才能认真回答面试里真正高频的问题：

> **这个项目为什么选 HNSW？为什么不用 IVF？**

正确答案不是“因为 HNSW 更快”。

---

## 1. 先看最核心的比较维度

| 维度 | HNSW | IVF |
|---|---|---|
| 核心思想 | 图导航 | 空间分区 |
| Recall | 常见高 | 依赖 nprobe / 分区质量 |
| Latency | 常见较低且稳定 | 依赖 probe 数与 List 分布 |
| Memory | 图边可能较重 | 可相对可控，配 PQ 更省 |
| Build | 建图较重 | 需要训练 Centroid / Build |
| Update | 插入相对自然，维护有成本 | 数据分布变化后需考虑重训 / rebuild |
| Filter | 依产品 filter-aware 实现 | 依产品过滤 / partition 结合方式 |
| Scale | Memory 是关键约束之一 | 常见于大规模 partition + compression 方案 |

这只是认知表，不是“产品性能排行榜”。

---

# 2. 为什么 HNSW 常被喜欢

在很多中大型 In-memory 场景里，HNSW 的优势常体现在：

```text
高 Recall
低 Query Latency
较少参数即可获得不错效果
```

但代价通常是：

```text
Graph Memory
Build Cost
Delete / Maintenance
```

如果数据规模巨大、Memory Budget 非常紧，单纯把所有数据做高密度 HNSW 可能很贵。

---

# 3. 为什么 IVF 仍然重要

IVF 的核心价值之一：

```text
通过空间分区减少候选
```

而且很容易和：

```text
PQ / Compression
```

组合。

所以在：

```text
大规模
Memory-sensitive
Batch-oriented
可接受训练 / Build
```

的场景中，IVF 系列仍然很有价值。

---

# 4. Index Selection 应先问什么

不要先问：

> “HNSW 还是 IVF？”

先列约束：

```text
N：多少向量？
D：多少维？
QPS？
P95 / P99 Latency？
Recall 目标？
Memory Budget？
Build Window？
Insert / Update Frequency？
Delete Frequency？
Filter Selectivity？
是否需要磁盘？
是否需要强 Tenant Isolation？
```

然后再比较 Index。

---

# 5. 一个场景例子

## 场景 A：500 万条知识库向量

要求：

```text
高 Recall
低延迟
内存可接受
增量写入较频繁
```

HNSW 可能是很自然的候选。

## 场景 B：5 亿条向量

要求：

```text
Memory 严格受限
允许离线训练索引
更新相对批量
```

可能会认真考虑：

```text
IVF + PQ
```

或其它磁盘 / 压缩路线。

这不是说两个场景只有唯一答案，而是展示决策因果链。

---

# 6. 真实 Filter 是选型的重要变量

如果 90% Query 都带：

```text
tenant_id
language
permission
```

那么无 Filter Benchmark 可能没有意义。

你需要测：

```text
Filter Selectivity 50%
10%
1%
0.1%
```

因为 ANN + Filter 的执行顺序可能改变：

```text
候选数量
Recall
Latency
```

所以 Product / Index Selection 都必须带真实过滤场景。

---

# 7. Update Pattern 会改变答案

静态离线数据：

```text
Build 一次
长期查询
```

和：

```text
每天持续新增 / 删除 / 更新
```

是两种完全不同的 Index Lifecycle。

需要考虑：

```text
Online Insert
Delete
Tombstone
Compaction
Rebuild
Rebalance
```

所以“Benchmark Query 快”只是选型的一部分。

---

# 8. 产品默认 Index 不代表项目最佳 Index

很多 Vector DB 会提供：

```text
默认 HNSW
默认参数
自动 Index
```

这降低了使用门槛，但不能替代工程判断。

真实 Production 应至少有：

```text
Baseline
Exact Ground Truth
Workload Benchmark
Capacity Estimate
Failure / Rebuild Plan
```

---

# 9. Index Selection 的标准回答模板

可以按：

```text
1. Data Scale
2. Query SLA
3. Recall Target
4. Memory / Disk Budget
5. Update / Delete Pattern
6. Metadata Filter
7. Build / Rebuild Window
8. Operational Complexity
```

逐项解释。

这样比：

> “HNSW Recall 高所以选 HNSW。”

成熟很多。

---

# 10. 面试怎么答

## Q：HNSW 和 IVF 怎么选？

🎯 **建议回答**：

> HNSW 是 Graph-based ANN，通过分层近邻图导航，常见特点是 Recall 高、Query Latency 低，但图结构会带来较高内存和构建维护成本。IVF 是 Partition-based ANN，先把空间划成 Cell，再通过 nprobe 控制搜索区域，容易和 PQ 结合做更大规模的内存压缩。实际选型不能只看算法名，要联合数据规模、Recall SLA、P95/P99、Memory、更新删除模式和 Metadata Filter 做 Benchmark。

---

# 11. 高频易错点

⚠️ **HNSW 全面优于 IVF。** 没有统一赢家。

⚠️ **IVF 只适合磁盘。** 过度简化，它是算法分区思想。

⚠️ **Product Selection = Index Selection。** 不是，一个产品可能支持多种 Index。

⚠️ **只测无过滤 Top-K 就能完成选型。** 真实业务常被 Filter 改变。

---

# 12. 本章自测

<details><summary>1. 为什么 Memory Budget 会明显影响 HNSW vs IVF 选择？</summary>

HNSW 需要保存额外图边和多层结构，Memory 开销可能较高；IVF 还可以进一步配合 PQ 等压缩路线，更适合某些 Memory-sensitive 大规模场景。
</details>

<details><summary>2. 为什么 Update / Delete Pattern 也属于 Index Selection？</summary>

因为索引不仅要查，还要长期维护。不同 Index 对增量插入、删除、重建和 compaction 的成本不同。
</details>
