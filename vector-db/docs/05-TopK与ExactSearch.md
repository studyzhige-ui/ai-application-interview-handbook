# 05. Top-K Nearest Neighbor 与 Exact Search

前面已经知道了“怎样定义近”，现在进入真正的搜索问题：

> **给一个 Query Vector，怎样找出最接近的 K 个向量？**

这就是 Nearest Neighbor Search。

---

## 1. Top-K 是什么

假设数据库里有：

```text
v1
v2
v3
...
vN
```

Query：

```text
q
```

我们想要：

```text
距离最近 / 相似度最高的 K 个向量
```

例如：

```text
TopK = 5
```

得到：

```text
v91
v7
v201
v13
v88
```

这一步只是在 Vector DB 层找候选。

最终 RAG 用几个、是否 Rerank、是否融合 BM25，不属于这一章。

---

# 2. Exact Search 最简单怎么做

最直接：

```text
for each vector v:
    score = distance(q, v)

排序
取 Top-K
```

复杂度粗略看：

```text
O(N × D)
```

其中：

```text
N = 向量数
D = Dimension
```

如果 N 很小，这个方法其实很好：

- 简单；
- 精确；
- 没有 ANN Recall Loss；
- 没有 Index Build；
- 很适合 Ground Truth / Evaluation Baseline。

---

# 3. 为什么 Exact Search 是重要基线

ANN 会返回“近似”的结果。

那你怎么知道它损失了多少 Recall？

最常见做法之一：

```text
在一批 Evaluation Query 上
用 Exact Search 得到 Ground Truth Top-K
↓
再和 ANN Top-K 比较
```

例如：

```text
Exact Top10:
A B C D E F G H I J

ANN Top10:
A B C D E F X Y H I
```

可以计算 ANN Recall。

所以：

> **Exact Search 不只是“小数据才用的笨办法”，还是 ANN 调优和验证的重要真值基线。**

---

# 4. Exact Search 为什么会贵

如果：

```text
N = 100,000,000
D = 1536
```

每次 Query 都扫全部向量：

```text
1 亿 × 1536 个数值比较
```

还涉及：

- Memory Bandwidth；
- Cache Miss；
- CPU / SIMD / GPU；
- 并发 QPS；
- 数据分片后的 Fan-out。

真正瓶颈不只是“大 O”，还包括硬件数据移动成本。

---

# 5. Top-K 本身怎样选出来

最简单可以：

```text
计算所有 score
→ 完整排序
```

但完整排序是：

```text
O(N log N)
```

如果只要 K 个，可以：

```text
维护一个大小为 K 的 Heap
```

把排序部分降成：

```text
O(N log K)
```

但注意：

> 这并没有解决“所有 N 个向量都要算距离”的核心问题。

ANN 真正优化的是：

```text
不要访问全部向量
```

---

# 6. 为什么 GPU / SIMD 不能替代 ANN

FAISS 等系统可以极大优化 Exact Search：

```text
SIMD
GPU
Batch Search
Memory Layout
```

所以 Exact Search 的实际性能可能非常强。

但是：

```text
硬件加速
```

和：

```text
减少候选访问量
```

是两条不同路线。

规模再大时，ANN 仍然具有价值。

正确思维：

```text
Algorithm
×
Data Layout
×
Hardware
×
Scale
```

共同决定性能。

---

# 7. 什么时候 Exact Search 可能就够了

例如：

```text
数据量不大
QPS 不高
Latency Budget 宽松
需要最高精度
硬件足够
```

这时：

> 不需要为了“看起来高级”强行上 HNSW。

尤其在 Evaluation、离线 Ground Truth、模型对比中，Exact Search 非常有价值。

---

# 8. Exact Search 和 ANN 的真正关系

```text
Exact Search
优点：100% exact nearest neighbor
缺点：规模大时访问成本高

ANN
优点：大幅减少搜索工作量
缺点：可能漏掉真正近邻，需要 Recall / Latency Trade-off
```

所以后面的核心问题变成：

> **能不能只看一小部分候选，却大概率找到真正的近邻？**

这就是 ANN。

---

# 9. 面试怎么答

## Q：为什么不能一直用暴力 Vector Search？

🎯 **建议回答**：

> Exact Search 需要对 Query 和大量甚至全部向量计算距离，核心成本大致随向量数量 N 和维度 D 增长。小规模时它很简单也很准确，甚至适合作为 ANN 的 Ground Truth；但在千万、亿级向量和高 QPS 下，扫描成本、内存带宽和并发压力会变得很高，所以会使用 ANN Index，用少量 Recall Loss 换取更低 Latency 和更高吞吐。

---

# 10. 高频易错点

⚠️ **Exact Search 一定很慢。** 过度绝对。小数据、GPU、Batch 场景可能很快。

⚠️ **Top-K Heap 解决了 ANN 问题。** 没有，它只优化结果选择，仍可能扫描全部向量。

⚠️ **ANN 比 Exact 更准。** 一般不是；Exact 是精确基线。

---

# 11. 本章自测

<details><summary>1. 为什么 Exact Search 常被用来评估 ANN？</summary>

因为 Exact Search 能给出真正的最近邻 Top-K，可作为 Ground Truth，用于测 ANN 是否漏掉了真实近邻。
</details>

<details><summary>2. Heap 优化了什么，没有优化什么？</summary>

它避免对全部 N 个结果完整排序，但仍可能需要计算 Query 到所有 N 个向量的距离。
</details>