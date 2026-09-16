# 04｜ANN Index 谱系：Graph、Partition、Quantization

如果一上来只学 HNSW，很容易形成一个错觉：

> ANN = HNSW。

实际上 ANN 有多条典型技术路线，而且很多系统会把它们组合起来。

这一章先建立地图。

---

## 1. ANN Index 在解决什么

目标仍然是：

```text
Query Vector
→ 不访问全部 N 个向量
→ 找到大概率接近 Exact Top-K 的候选
```

不同 Index 的核心差别是：

> **怎样减少需要访问的候选。**

---

# 2. 路线一：Graph-based Search

代表：

```text
HNSW
NSG
DiskANN 等图路线
```

核心直觉：

```text
每个向量是一个节点
近邻之间连边
Query 从某个入口开始
沿“越来越近”的边走
```

像在地图里：

```text
不是把全国每个城市都算一遍
而是沿道路不断靠近目标区域
```

优点常见是：

- 高 Recall；
- 低延迟；
- Query 导航效果好。

代价常见是：

- 图边需要额外内存；
- Build 较重；
- Update / Delete / Compaction 复杂；
- 大规模内存规划重要。

---

# 3. 路线二：Partition / Inverted File

代表：

```text
IVF
```

核心直觉：

```text
先把向量空间分成很多区域
Query 只进入最可能的少数区域
```

例如：

```text
10000 个 Cell
只搜索最近的 20 个 Cell
```

这样：

```text
搜索候选量大幅下降
```

核心参数会变成：

```text
nlist  = 有多少个区域
nprobe = Query 搜多少个区域
```

---

# 4. 路线三：Quantization / Compression

代表：

```text
Scalar Quantization
Product Quantization
```

目标：

> **不是只减少候选，还要减少每个向量本身的存储和距离计算成本。**

例如把：

```text
float32 vector
```

压成：

```text
int8 / codebook code
```

于是：

- 内存更小；
- Cache 更友好；
- 距离可以近似计算。

代价是：

```text
Compression Error
→ Recall / Ranking 可能损失
```

---

# 5. Flat / Exact 也应该放进谱系里

索引选择不能只在 ANN 之间选。

完整地图先包括：

```text
Flat / Exact
Graph-based
Partition-based
Quantized
Hybrid Combination
```

例如某些方案会出现：

```text
IVF + PQ
```

先分区，再对向量压缩。

或者产品内部使用 Graph + Disk Layout 等组合。

---

# 6. 为什么没有“一种 Index 全赢”

因为优化目标不同：

```text
Recall
Latency
QPS
Memory
Disk
Build Time
Update Frequency
Filter
Dataset Size
```

例如：

```text
HNSW
可能 Recall / Latency 很优秀
但 Memory 很重

IVF
可能更适合某些大规模批量数据
但参数和数据分布影响明显

PQ
能显著压缩
但会引入量化误差
```

所以真正问题不是：

> HNSW 是不是最好？

而是：

> **我的约束是什么？**

---

# 7. In-memory 和 Disk-based 也会改变设计

如果数据和索引都放内存：

```text
随机访问延迟低
```

但成本高。

如果规模大到需要 SSD：

```text
访问模式
Batching
Graph Layout
Cache
```

都会成为重要问题。

所以“ANN 算法”与“存储介质”不能完全分开看。

本模块只建立应用工程层的直觉，不展开到存储引擎论文实现细节。

---

# 8. Filter 会改变 ANN 的效果

假设索引非常好，但 Query 加：

```text
tenant_id = 42
AND language = zh
```

如果过滤后只剩极少候选，ANN 导航可能发生变化。

因此 Production Index 不能只测试：

```text
无 Filter Benchmark
```

还要测试真实业务 Filter Selectivity。

这会在 Metadata Filter 章节继续讲。

---

# 9. ANN 选型的第一张表

| 路线 | 核心思想 | 主要换来的收益 | 主要代价 |
|---|---|---|---|
| Flat | 全量比较 | 精确 | 扫描成本 |
| Graph | 近邻图导航 | 高 Recall / 低访问量 | Memory / Build |
| IVF | 空间分区 | 少搜区域 | Partition Error / Parameter |
| Quantization | 压缩向量 | Memory / Compute | Quantization Error |

这张表只是认知地图，不能替代 Benchmark。

---

# 10. 面试怎么答

## Q：ANN 常见索引思路有哪些？

🎯 **建议回答**：

> 可以先按减少搜索成本的方式分成几类。Graph-based 例如 HNSW，把向量构成近邻图，通过图导航减少访问；Partition-based 例如 IVF，先把空间分成 Cell，只搜索部分区域；Quantization 例如 PQ，通过压缩表示降低内存和距离计算成本。实际系统还可能组合 IVF+PQ 或使用磁盘优化结构。选型不能只看算法名，要联合 Recall、Latency、Memory、Build、Update 和 Filter 约束。

---

# 11. 高频易错点

⚠️ **ANN 就是 HNSW。** 错误。

⚠️ **PQ 只是一个更快的 HNSW 参数。** 错误，它是压缩 / 量化思路。

⚠️ **Index Benchmark 不需要考虑 Filter。** Production 中 Filter 可能明显改变行为。

---

# 12. 本章自测

<details><summary>1. Graph-based 与 IVF 的核心差别是什么？</summary>

Graph-based 通过近邻关系导航到 Query 附近；IVF 先把空间划分成区域，再只搜索最相关的若干区域。
</details>

<details><summary>2. Quantization 主要优化什么？</summary>

主要压缩向量表示和距离计算成本，从而降低内存 / 存储并提高吞吐，但会引入近似误差。
</details>
