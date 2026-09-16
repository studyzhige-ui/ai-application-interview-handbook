# 06｜IVF：Coarse Quantizer、nlist 与 nprobe

IVF = Inverted File Index。

它的核心思想不是“建图”，而是：

> **先把向量空间划成很多区域，查询时只搜索最可能的少数区域。**

---

## 1. 从“全库扫描”到“先分区”

Exact Search：

```text
Query
→ 扫全部 N 个向量
```

IVF：

```text
先训练若干 Centroid
        ↓
每条向量归到最近 Centroid
        ↓
形成很多 Inverted List
        ↓
Query 先找最近的几个 Centroid
        ↓
只扫描对应 List
```

于是访问量从：

```text
全部数据
```

变成：

```text
少数 Cell 中的数据
```

---

# 2. Coarse Quantizer 是什么

IVF 先用一个粗粒度的聚类 / Quantizer 把空间分区。

可以建立直觉：

```text
Vector Space
├─ Cell 1
├─ Cell 2
├─ Cell 3
└─ ...
```

每个 Cell 有一个代表中心：

```text
Centroid
```

一条向量写入时：

```text
找到最近 Centroid
→ 放入对应 List
```

这就是 Inverted List 的来源。

---

# 3. nlist：分多少个区域

常见参数：

```text
nlist
```

可以理解成：

> 需要划分多少个 Cell / Inverted List。

如果 nlist 太小：

```text
每个 List 很大
→ Query 即使只搜少数 List
→ 候选仍很多
```

如果 nlist 太大：

```text
分区更细
→ 候选可能更少
但训练和路由更敏感
→ 某些真实近邻可能落在相邻 Cell
```

所以仍然不是越大越好。

---

# 4. nprobe：查询时搜多少个区域

Query 不应该只看一个 Cell。

因为真正最近邻可能在边界另一侧。

因此：

```text
nprobe = 搜索多少个最近的 Cell
```

典型 Trade-off：

```text
nprobe ↑
→ 候选更多
→ Recall 通常 ↑
→ Latency / CPU ↑
```

这与 HNSW 的 `efSearch` 类似：

> 都是用更多 Query Search Work 换更高 Recall，但内部机制不同。

---

# 5. 为什么 IVF 需要“训练”

HNSW 更像直接根据数据建立图。

IVF 通常需要先得到 Coarse Centroid。

例如：

```text
sample vectors
→ clustering
→ centroids
```

如果训练样本不代表真实数据分布：

```text
Cell 质量差
→ 数据倾斜
→ Recall / Latency 都可能变差
```

因此 IVF Index Build 不只是设置一个参数就完成。

---

# 6. IVF_FLAT 是什么

IVF_FLAT：

```text
IVF 用来缩小候选区域
+
Cell 内仍用原始向量做较精确距离计算
```

所以它的主要近似来自：

```text
没有搜索所有 Cell
```

如果再结合 PQ：

```text
IVF_PQ
```

则：

```text
候选区域缩小
+
向量自身也被压缩
```

会进一步降低 Memory / Compute，但也多一层量化误差。

---

# 7. Data Distribution 为什么重要

如果数据天然聚集得比较明显：

```text
IVF Partition
```

可能非常有效。

如果数据分布极不均匀：

```text
某些 Cell 巨大
某些 Cell 很小
```

就会出现：

```text
Latency Hotspot
候选量不稳定
```

所以需要观察：

- List Size Distribution；
- Query Probe Distribution；
- Filter Selectivity；
- Recall / Latency。

---

# 8. IVF 和 Metadata Partition 不是一回事

很容易混淆：

```text
IVF Cell
```

是向量空间里的算法分区。

而：

```text
tenant partition
language partition
business namespace
```

是业务数据分区。

两者可以同时存在，但目的不同。

---

# 9. 面试怎么答

## Q：IVF 是怎么做 ANN 的？

🎯 **建议回答**：

> IVF 先用 Coarse Quantizer 把向量空间划成多个 Cell，每个向量归到某个 Inverted List。Query 时先找到最接近的若干 Centroid，只扫描对应 List，而不是全库扫描。nlist 控制分区数量，nprobe 控制查询时搜索多少个 Cell；nprobe 越大 Recall 通常越高，但访问候选更多、延迟也更高。

## Q：IVF_FLAT 和 IVF_PQ 有什么区别？

> IVF_FLAT 在被选中的 List 内仍使用原始向量计算距离；IVF_PQ 还会把向量用 Product Quantization 压缩，因此内存和计算更省，但会额外引入量化误差。

---

# 10. 高频易错点

⚠️ **IVF 的 nlist 就是业务 Partition 数。** 错误。

⚠️ **nprobe=1 一定最快也够准。** Recall 可能明显下降。

⚠️ **IVF 不需要训练。** 通常需要训练 Coarse Quantizer / Centroid。

⚠️ **IVF_PQ 的近似只来自少搜 Cell。** 还包括 PQ 的量化误差。

---

# 11. 本章自测

<details><summary>1. nlist 和 nprobe 分别控制什么？</summary>

nlist 控制索引把向量空间划成多少个 Cell；nprobe 控制单次 Query 实际搜索多少个 Cell。
</details>

<details><summary>2. 为什么真正近邻可能不在 Query 最近的一个 Cell？</summary>

因为 Query 和近邻可能处在 Cell 边界两侧，所以只搜一个分区会有边界误差，需要探测多个相邻 Cell。
</details>
