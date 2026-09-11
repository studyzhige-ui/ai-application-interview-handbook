# 05. Exact Search vs ANN：从 Top-K Ground Truth 到 Recall / Latency Trade-off

上一章定义了“什么叫近”，这一章解决真正的检索问题：

> **给定一个 Query Vector，怎样找到最接近的 K 个向量？为什么小规模时可以 Exact Search，大规模时却需要 ANN？**

这一章把原来的 `Top-K / Exact Search` 和 `为什么需要 ANN` 合成一个完整因果链。

---

## 1. Top-K Nearest Neighbor 是什么

数据库里有：

```text
v1, v2, ... vN
```

查询向量：

```text
q
```

目标是根据某个 Metric 找：

```text
Top-K nearest vectors
```

例如：

```text
K = 5
```

得到 5 个最接近的候选。

注意：

> Vector DB 这里只负责“找候选”；最终 RAG 用几个、是否 Hybrid、是否 Rerank，属于上层 Retrieval Pipeline。

---

## 2. Exact Search 最直接怎么做

最简单的算法：

```text
for every vector v:
    score = distance(q, v)

select Top-K
```

距离计算部分粗略是：

```text
O(N × D)
```

其中：

- `N`：向量数量；
- `D`：Dimension。

如果 N 不大，这个方法其实非常合理：

- 实现简单；
- 结果精确；
- 没有 ANN Recall Loss；
- 不需要复杂 Index Build；
- 非常适合作为 Evaluation Ground Truth。

---

## 3. Top-K Selection 本身怎么优化

计算完所有 Score 后，如果只需要 K 个结果，不一定要对 N 个结果全部排序。

可以维护大小为 K 的 Heap：

```text
full sort: O(N log N)
heap select: O(N log K)
```

但要注意：

> Heap 只优化“结果选择”，并没有解决“所有 N 个向量都要算距离”的问题。

ANN 真正要优化的是：

```text
不要访问全部向量
```

---

## 4. Exact Search 为什么是 ANN 的 Ground Truth

ANN 返回的是近似近邻。

那怎么知道 ANN 漏了多少？

常见方法：

```text
Representative Query Set
        ↓
Exact Search
        ↓
Ground Truth Top-K
        ↓
ANN Search
        ↓
Compare Results
```

例如：

```text
Exact Top10: A B C D E F G H I J
ANN Top10:   A B C D E F X Y H I
```

ANN 找回 8 个真实 Top10：

```text
Recall@10 = 0.8
```

所以 Exact Search 不只是“没索引时的笨办法”，还是：

> **ANN 调优、回归测试和故障定位的重要基线。**

---

## 5. 为什么规模上来以后 Exact 会变贵

假设：

```text
N = 100,000,000
D = 1536
```

每次 Query 都扫描全部向量意味着巨大的：

- Distance Compute；
- Memory Bandwidth；
- Cache Miss；
- CPU / GPU Work；
- Distributed Fan-out；
- 并发 QPS 压力。

瓶颈并不只是理论 Big-O，还包括：

> **把大量向量从内存/设备中搬出来并参与计算的成本。**

---

## 6. GPU / SIMD 为什么不能完全替代 ANN

FAISS 等系统可以通过：

```text
SIMD
GPU
Batch Search
Memory Layout
```

把 Exact Search 做得很快。

但：

```text
硬件加速所有候选
```

和：

```text
算法上减少需要访问的候选
```

是两条不同路线。

真实性能由：

```text
Algorithm × Data Layout × Hardware × Scale
```

共同决定。

所以小规模时 Exact 可能足够；千万、亿级和高 QPS 时 ANN 才更有价值。

---

## 7. ANN 的 Approximate 到底近似什么

ANN = Approximate Nearest Neighbor。

“Approximate”通常不是说距离函数算错，而是：

> **搜索没有访问全部数据，因此不保证结果和 Exact Top-K 完全一致。**

例如：

```text
Exact Top5: A B C D E
ANN Top5:   A B C X D
```

ANN 漏掉了 E。

这就是 Recall Loss。

---

## 8. ANN 的核心 Trade-off

可以先记住最重要的一条：

```text
Search Work ↑
→ Recall 通常 ↑
→ Latency / CPU ↑

Search Work ↓
→ Latency 通常 ↓
→ Recall 可能 ↓
```

所以没有一个“最好”的 ANN 参数。

真正目标是：

> **在业务可以接受的 Recall 下，把 P95/P99 Latency、QPS、Memory 和 Cost 控制在目标范围。**

---

## 9. ANN 为什么能少看很多向量

主流路线大致可以分成：

### Graph-based

例如 HNSW：

```text
把向量连接成图
→ 从入口沿更近的邻居导航
→ 不扫描全库
```

### Partition-based

例如 IVF：

```text
先把空间分区
→ Query 找最近的几个 Cell
→ 只搜索这些 Cell
```

### Compression / Quantization

例如 PQ / SQ：

```text
压缩 Vector
→ 更少 Memory
→ 更快近似距离
```

真实系统经常组合这些方法。

---

## 10. ANN 不是免费加速器

它会引入新的成本：

```text
Index Build
Extra Memory
Index Storage
Insert / Update Cost
Delete / Tombstone
Compaction / Rebuild
Parameter Tuning
```

例如 HNSW：

```text
图更密
→ Recall Potential ↑
→ Memory / Build Cost ↑
```

IVF：

```text
分区更细
→ 可减少搜索范围
→ 训练、分布和 nprobe 更敏感
```

因此 Index Selection 本质是系统权衡。

---

## 11. ANN 参数应该怎么调

不要先背：

```text
efSearch = 64
nprobe = 10
```

工程化过程应该是：

```text
Representative Corpus
        ↓
Representative Queries
        ↓
Exact Ground Truth
        ↓
Build ANN
        ↓
Sweep Parameters
        ↓
Recall / P95 / P99 / QPS / Memory
        ↓
Choose Operating Point
```

这也是为什么 Exact Search 是 ANN 课程里的必要前置。

---

## 12. RAG 召回差，怎么判断是不是 ANN 导致

不要看到最终“相关文档没召回”就立刻调 `efSearch`。

可以先做分层对照：

```text
Exact Vector Search 也找不到
→ 更像 Embedding / Chunk / Query / Metric 问题

Exact 能找到，ANN 找不到
→ 更像 ANN Index / Parameter 问题
```

后面再加入 Filter 对照：

```text
No Filter 找得到
Filter 后找不到
→ 检查 Metadata / Permission / Filter Strategy
```

这是 Production Troubleshooting 非常重要的思维。

---

## 13. 什么时候 Exact Search 就够了

例如：

- 数据量较小；
- QPS 不高；
- Latency Budget 宽松；
- 必须保证精确近邻；
- GPU / SIMD 资源足够；
- 离线 Evaluation / Ground Truth。

所以不要为了“架构高级”强行上 HNSW。

---

## 14. 常见错误

- Exact Search 一定很慢：过度绝对。
- ANN 比 Exact 更准：错误。
- Heap Top-K 就解决了 ANN 问题：错误。
- ANN 是距离公式的近似：不准确，通常是搜索路径/候选访问的近似。
- Recall 越高越好，直接拉满参数：忽略 Latency / CPU / Cost。
- RAG Recall 低就是 Vector DB Recall 低：错误。

---

## 15. 面试怎么答

### Q：为什么不能一直用暴力 Vector Search？

> Exact Search 需要对 Query 和大量甚至全部向量计算距离，成本随 N 和 D 增长。小规模时它非常简单可靠，而且适合作为 ANN Ground Truth；但千万、亿级向量和高 QPS 下，Memory Bandwidth、计算和 Fan-out 会变贵，所以使用 ANN，通过允许少量近邻遗漏换更低 Latency 和更高吞吐。

### Q：ANN 牺牲什么换什么？

> 它牺牲和 Exact Top-K 完全一致的保证，换取更少候选访问、更低查询成本。工程上用 Exact Search 建 Ground Truth，再选择满足业务 Recall 目标的 Operating Point，而不是只追求某一个参数值。

---

## 16. 自测

<details><summary>1. 为什么 Exact Search 是 ANN 的重要测试工具？</summary>
因为它能给出真正最近邻，用来量化 ANN 的 Recall Loss。
</details>

<details><summary>2. Top-K Heap 优化了什么，没有优化什么？</summary>
优化了结果选择/排序成本，但没有减少对所有候选做距离计算这一核心扫描成本。
</details>

<details><summary>3. 如果 Exact 能找到正确结果、ANN 找不到，应该优先查什么？</summary>
ANN Index 质量、参数、Quantization、Filter-aware search 等，而不是先怀疑 Embedding 本身。
</details>
