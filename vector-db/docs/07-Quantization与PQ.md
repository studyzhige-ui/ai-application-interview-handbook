# 07｜Quantization：SQ / PQ 与压缩检索

当向量数量非常大时，一个现实问题会变得明显：

> **就算 ANN 能少搜很多候选，原始向量本身也可能太占内存。**

例如：

```text
1 亿条
× 1536 维
× float32 4 bytes
≈ 600 GB raw vectors
```

这还没算 Index 和 Replica。

Quantization 的目标就是：

> **用更紧凑的表示近似原始向量，降低 Memory / Storage / Distance Compute。**

---

## 1. Scalar Quantization 直觉

原始：

```text
float32
```

每个值 4 bytes。

一种思路：

```text
把连续浮点数映射到较低精度的离散值
```

例如：

```text
float32 → int8-like representation
```

那么每个维度占用可以明显降低。

代价：

```text
原值不能完全恢复
→ Quantization Error
```

---

# 2. Product Quantization 为什么叫 Product

PQ 不只是“每个 float 直接变 int8”。

它通常把一个高维向量拆成多个子向量：

```text
v = [subvector_1 | subvector_2 | ... | subvector_m]
```

然后每个子空间分别训练 Codebook：

```text
subvector
→ nearest codeword
→ code id
```

最终一个高维向量不再保存全部 float，而保存：

```text
code_1, code_2, ..., code_m
```

查询时利用 Codebook 近似计算距离。

---

# 3. 一个简化例子

假设 8 维向量：

```text
[a b c d | e f g h]
```

拆成 2 个子空间。

每个子空间都有 256 个 Codeword。

那么每个子空间只需要：

```text
1 byte code id
```

整条向量可能只需要：

```text
2 bytes code
```

而原始 float32：

```text
8 × 4 = 32 bytes
```

真实 PQ 参数更复杂，但这个例子足够建立压缩直觉。

---

# 4. 压缩为什么会影响 Recall

因为：

```text
Original Vector
→ Approximate Codeword Representation
```

距离不再完全基于原始数值。

因此：

```text
Compression ↑
→ Memory ↓
→ Distance Compute 可能更快
→ Quantization Error ↑
→ Ranking / Recall 可能下降
```

这就是典型 Trade-off。

---

# 5. IVF + PQ 为什么常见

IVF：

```text
减少需要搜索的区域
```

PQ：

```text
降低每个候选的存储和距离计算成本
```

组合：

```text
Query
→ nprobe 个 Cell
→ 对 Cell 内 PQ Code 做近似距离计算
```

因此：

```text
IVF_PQ
```

适合某些大规模、Memory-sensitive 场景。

---

# 6. Quantization 不一定只用于最终排序

一种常见系统设计思想是：

```text
Compressed Representation
→ 快速筛候选
→ 用 Original Vector 精排一小批候选
```

也就是：

```text
approximate first stage
→ exact / higher precision refinement
```

这样可以在性能和精度之间折中。

具体是否支持由产品实现决定。

---

# 7. PQ 参数在控制什么

不要求现在背产品参数名，但要理解：

```text
子空间划分数量
Codebook 大小
压缩码长度
```

都会影响：

```text
Compression Ratio
Quantization Error
Build Time
Memory
Distance Cost
```

所以 PQ 调优同样应该 Benchmark，而不是照抄固定值。

---

# 8. Quantization 与 Embedding Dimension 的关系

Dimension 越高：

```text
raw vector 越大
```

压缩价值通常也更明显。

但如果 Dimension 太小或者数据规模不大：

```text
引入 PQ 的复杂度
```

未必值得。

所以：

> Quantization 是规模问题的工具，不是所有 Vector DB 必选项。

---

# 9. 面试怎么答

## Q：PQ 解决什么问题？

🎯 **建议回答**：

> Product Quantization 主要解决高维向量在大规模场景下的内存和距离计算成本。它把向量拆成多个子空间，每个子空间用 Codebook 中的代表向量近似，并只保存 Code ID。这样能显著压缩表示，但会引入 Quantization Error，所以要在 Memory、Latency 和 Recall 之间做权衡。IVF+PQ 是常见组合，一个减少候选区域，一个压缩候选表示。

---

# 10. 高频易错点

⚠️ **PQ 是一种聚类分区，所以等于 IVF。** 错误，两者解决的问题不同。

⚠️ **压缩后完全不影响 Recall。** 不保证。

⚠️ **所有大模型 Embedding 都应该先 PQ。** 取决于规模与精度要求。

⚠️ **PQ 只节省磁盘，不影响内存/计算。** 它通常正是为了优化这些成本。

---

# 11. 本章自测

<details><summary>1. IVF 和 PQ 分别在减少什么？</summary>

IVF 主要减少一次 Query 要搜索的区域 / 候选量；PQ 主要压缩每条向量的表示并近似距离计算。
</details>

<details><summary>2. 为什么 PQ 会带来 Recall 风险？</summary>

因为 Query 距离是基于量化后的近似表示计算，不再完全等于原始向量的真实距离，排序可能发生变化。
</details>