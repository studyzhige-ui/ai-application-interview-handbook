# 08. HNSW：分层小世界图

HNSW 是当前 Vector DB 面试最常见的 ANN Index 之一。

不要先背参数，先回答：

> **为什么把向量连成图，就能少看很多点还找到近邻？**

HNSW = Hierarchical Navigable Small World。

---

## 1. 从普通近邻图开始

假设每个向量是一个节点：

```text
A —— B —— C
|    |     |
D —— E —— F
```

如果 Query 和 F 很近，我们不需要把所有节点都算一遍。

可以从 A 开始：

```text
A
→ B
→ E
→ F
```

每一步都走向更接近 Query 的邻居。

这就是 Graph Navigation 的核心直觉。

---

# 2. 普通近邻图的问题

如果图只有“局部边”：

```text
每次只能走很短一步
```

当数据很多时，从一端走到另一端仍然会很慢。

我们希望同时拥有：

```text
长距离跳跃
+
局部精细搜索
```

于是引入多层结构。

---

# 3. Hierarchical：为什么分层

可以把 HNSW 想象成：

```text
Layer 2:       A ----------- Z
                \          /
Layer 1:       A ---- H --- N ---- Z
                \   /       \    /
Layer 0:       A-B-C-D-E-F-G-H-I-J-...-Z
```

高层：

```text
节点少
边跨度大
负责快速接近目标区域
```

底层：

```text
节点最多
邻接更细
负责精确局部搜索
```

像交通系统：

```text
高速公路
→ 城市主干道
→ 小区道路
```

---

# 4. 查询过程

粗略流程：

```text
从最高层 Entry Point 开始
        ↓
寻找更接近 Query 的邻居
        ↓
无法继续改进时下降一层
        ↓
继续搜索
        ↓
到底层维护候选集合
        ↓
返回 Top-K
```

高层常以较贪心的方式导航，底层会维护更宽的候选集合。

---

# 5. Small World 在说什么

Small-world 网络直觉是：

> 大量局部连接 + 少量能跨区域的连接，可以让任意两个区域之间通过较少跳数到达。

HNSW 利用这种结构让 Query：

```text
快速跳到大致区域
再局部搜索
```

而不是全量扫描。

---

# 6. HNSW 为什么是 Approximate

因为搜索不会访问所有节点。

假设真正最近邻藏在：

```text
某个没有被当前导航路径探索到的局部区域
```

搜索就可能错过它。

提高搜索宽度可以降低这种概率，但成本也会上升。

所以：

```text
Recall ↑
通常意味着
Search Work ↑
```

---

# 7. 构建索引在做什么

新节点插入时，大致要：

```text
决定它最高出现在哪一层
→ 从高层开始找候选邻居
→ 在各层选择连接
→ 建立图边
```

因此 HNSW Build 不是简单把 Vector 写进数组。

Build Cost 会受：

```text
数据量
Dimension
M
efConstruction
```

等影响。

---

# 8. 为什么图会占很多内存

除了原始向量：

```text
Vector Data
```

还要保存：

```text
Node Metadata
Neighbor IDs
Multiple Layers
Graph Links
```

所以 HNSW 常见 Trade-off：

> 用额外内存换低延迟和高 Recall。

这也是为什么不能只说：

> “HNSW 快，所以永远选 HNSW。”

---

# 9. HNSW 与 Update / Delete

插入相对自然，因为可以把新节点接进图。

Delete / Update 更复杂：

```text
节点已经被其它节点连接
```

很多产品会采用：

```text
logical delete / tombstone
→ background cleanup / compaction / rebuild
```

具体行为取决于产品实现。

因此 Index Lifecycle 必须单独学习。

---

# 10. HNSW 不解决什么

HNSW 只解决 ANN Infrastructure 的一部分。

它不会自动解决：

```text
Embedding 模型是否合适
Chunk 是否合理
Hybrid Retrieval
Rerank
权限模型
RAG Evaluation
```

所以项目里说：

> “我们用了 HNSW，因此 RAG Recall 很高。”

证据是不够的。

---

# 11. 面试怎么答

## Q：HNSW 为什么能做高效 ANN？

🎯 **建议回答**：

> HNSW 把向量构造成分层近邻图。高层节点更稀疏，用于长距离快速导航；逐层下降后在底层做更细的局部候选搜索，因此不需要访问全部向量。它的代价是额外图结构内存、较重的构建和维护成本，而且搜索宽度有限时可能错过真实最近邻，所以本质仍然是 Recall 与 Latency 的 Trade-off。

---

# 12. 高频易错点

⚠️ **HNSW 就是一棵树。** 不是，它是分层图。

⚠️ **高层保存所有节点。** 通常不是，高层更稀疏。

⚠️ **HNSW 100% 找到 Exact Nearest Neighbor。** 不保证。

⚠️ **用了 HNSW 就不需要评估 Recall。** 错误。

---

# 13. 本章自测

<details><summary>1. HNSW 为什么要分层？</summary>

高层负责用较少节点做长距离导航，底层负责局部精细搜索，从而同时兼顾全局跳转和局部近邻查找。
</details>

<details><summary>2. HNSW 为什么内存通常比 Flat 更重？</summary>

除了原始向量，还要保存图节点、多层邻接关系和相关索引元数据。
</details>