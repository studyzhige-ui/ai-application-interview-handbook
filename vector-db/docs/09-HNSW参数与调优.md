# 09. HNSW 参数：M / efConstruction / efSearch

HNSW 面试很容易掉进“背参数”的陷阱。

真正应该理解的是：

> **这些参数分别在控制图的连接密度、构建质量和查询搜索宽度。**

---

## 1. 先看三个核心参数

常见 HNSW 实现会暴露类似：

```text
M
efConstruction
efSearch
```

它们名字可能在不同产品中略有差异，但核心语义非常稳定。

---

# 2. M：每个节点连接多少邻居

直觉：

```text
M 小
→ 图更稀疏
→ 内存更低
→ Build 较轻
→ 可能更容易错过路径

M 大
→ 图更密
→ 路径选择更多
→ Recall 潜力更高
→ Memory / Build Cost 更高
```

所以 M 主要影响：

```text
Graph Degree
Memory
Build
Search Quality
```

不能简单理解成：

> M 越大越好。

---

# 3. efConstruction：建图时搜多宽

构建一个新节点时，需要在已有图中找到合适邻居。

如果只看非常少的候选：

```text
建图快
但邻接质量可能差
```

如果搜索更宽：

```text
找到更好的邻居
图质量更高
但 Build 更慢
```

这就是 `efConstruction` 的核心 Trade-off。

它主要影响：

```text
Index Build Time
Index Quality
后续 Recall 上限
```

一旦图建得很差，仅靠 Query 阶段把 `efSearch` 拉很大，也未必完全补回来。

---

# 4. efSearch：查询时保留多大的候选集合

Query 时，如果只沿非常窄的路径搜索：

```text
Latency 低
但可能早早走错方向
```

如果保留更多候选：

```text
探索更充分
Recall 往往更高
但计算更多
Latency / CPU 更高
```

所以 `efSearch` 是最典型的在线调优旋钮：

```text
efSearch ↑
→ Recall 通常 ↑
→ Latency / CPU 通常 ↑
```

---

# 5. efSearch 和 Top-K 不是一回事

假设最终要：

```text
TopK = 10
```

不代表：

```text
efSearch = 10
```

`TopK` 是最终要返回多少结果。

`efSearch` 更像：

> Query 过程中愿意维护 / 探索多宽的候选集合。

一般需要：

```text
efSearch >= K
```

但具体合理值依实现和数据而定。

---

# 6. 为什么不能只调 efSearch

HNSW 质量是构建与查询共同决定的：

```text
M
+
efConstruction
→ Graph Quality / Density

Query efSearch
→ Search Effort
```

如果：

```text
M 太小
图连通和局部选择能力弱
```

或者：

```text
efConstruction 太小
图本身邻接质量差
```

Query 再努力也会受 Index Quality 限制。

---

# 7. 参数调优的正确方法

不要：

```text
网上看到 M=16, ef=64
→ 直接抄
```

应该：

```text
Representative Corpus
        ↓
Representative Query
        ↓
Exact Ground Truth
        ↓
Sweep M / efConstruction / efSearch
        ↓
Measure
Recall
P50 / P95 / P99 Latency
QPS
Index Build Time
Memory
Index Size
        ↓
Choose Operating Point
```

而且要带真实 Filter 测试。

---

# 8. 为什么 Filter 会改变最佳 efSearch

如果 Query 还有：

```text
tenant_id = 42
```

ANN 导航过程可能因为大量候选被过滤掉，导致有效候选不足。

不同产品对 Filter 的执行方式不同：

```text
pre-filter
post-filter
filter-aware traversal
```

因此同一个 `efSearch` 在无 Filter 和高选择性 Filter 下可能表现不同。

---

# 9. 数据变化后参数还一定合适吗

不一定。

如果：

```text
数据从 100 万涨到 1 亿
分布发生变化
Dimension 变化
Embedding Model 变化
Filter 变复杂
```

原参数的 Recall / Latency 曲线可能变化。

所以 ANN 参数不是“一次配置永久有效”。

---

# 10. 面试怎么答

## Q：HNSW 的 M、efConstruction、efSearch 分别是什么？

🎯 **建议回答**：

> M 主要控制图中每个节点的连接密度，越大通常 Recall 潜力更高，但内存和构建成本也更高；efConstruction 控制建图时搜索候选的宽度，影响索引构建时间和图质量；efSearch 控制查询时搜索宽度，是在线 Recall / Latency 的主要调节参数。参数不能靠固定经验值，需要用 Exact Ground Truth 和真实 Query/Filter 做 Benchmark。

---

# 11. 高频易错点

⚠️ **efSearch 就是 TopK。** 错误。

⚠️ **M 越大越好。** 会显著增加内存和 Build Cost。

⚠️ **只要把 efSearch 拉很高就能补救任何差索引。** 不能保证。

⚠️ **一套 HNSW 参数适用于所有数据规模。** 错误。

---

# 12. 本章自测

<details><summary>1. efConstruction 和 efSearch 的本质区别是什么？</summary>

前者主要控制建图阶段的候选搜索宽度和图质量；后者控制查询阶段的搜索宽度和 Recall / Latency Trade-off。
</details>

<details><summary>2. 为什么 HNSW 参数必须用 Exact Ground Truth 调？</summary>

因为 ANN 本质上可能漏近邻，没有 Exact 基线就无法量化 Recall 损失，只看 Latency 不知道结果质量是否已经下降。
</details>