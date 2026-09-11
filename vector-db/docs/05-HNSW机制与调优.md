# 08. HNSW：机制、M、efConstruction、efSearch 与调优

HNSW 是当前最常见的 ANN Index 之一。

真正应该形成的知识闭环不是“先学原理，下一篇再背参数”，而是：

```text
为什么图可以搜索近邻？
→ 为什么要分层？
→ Build 时发生什么？
→ M 控制什么？
→ efConstruction 为什么影响图质量？
→ efSearch 为什么控制 Recall / Latency？
→ 怎样用 Exact Ground Truth 调参？
```

HNSW = Hierarchical Navigable Small World。

---

## 1. 从普通近邻图开始

把每个向量看成一个节点：

```text
A —— B —— C
|    |     |
D —— E —— F
```

如果 Query 与 F 很近，可以从某个入口开始：

```text
A → B → E → F
```

每一步选择更接近 Query 的邻居。

这就是 Graph Navigation 的核心直觉：

> **不用访问所有向量，只沿图里的候选路径逐步逼近目标区域。**

---

## 2. 为什么普通近邻图还不够

如果图只有局部连接：

```text
每次只能走很短一步
```

跨越大范围空间仍然需要很多跳。

所以 HNSW 引入层级结构：

```text
Layer 2:      A -------- Z
               \        /
Layer 1:      A --- H --- N --- Z
               \ /       \ /
Layer 0:      A-B-C-D-E-F-G-H-I-...-Z
```

高层：

```text
节点少
边跨度大
负责快速导航到大致区域
```

底层：

```text
节点多
局部连接更丰富
负责精细搜索
```

可以类比：

```text
高速公路
→ 城市主干道
→ 小区道路
```

---

## 3. 查询过程

简化流程：

```text
从最高层 Entry Point 开始
        ↓
沿更接近 Query 的节点前进
        ↓
无法继续改进时下降一层
        ↓
重复导航
        ↓
到底层维护候选集合
        ↓
返回 Top-K
```

高层主要用于快速定位，底层搜索更宽。

---

## 4. 为什么叫 Small World

Small-world 网络的直觉是：

> 大量局部连接 + 少量跨区域连接，可以让任意两个区域之间通过较少跳数到达。

HNSW 借这个结构实现：

```text
快速跳到附近区域
→ 再局部精细搜索
```

而不是全库扫描。

---

## 5. HNSW 为什么仍然是 Approximate

搜索不会访问所有节点。

如果真正近邻在一个没有被当前路径充分探索到的局部区域，可能被漏掉。

所以：

```text
Search Work ↑
→ Recall 通常 ↑
→ Latency / CPU ↑
```

这就是后面参数的意义。

---

## 6. Build 时发生什么

插入一个新节点，大致会经历：

```text
决定它最高出现在哪一层
→ 从高层向下搜索候选邻居
→ 每层选择连接
→ 写入图边
```

因此 HNSW Build 不是简单 Append Vector。

Build Cost 与：

```text
N
D
M
efConstruction
```

等因素有关。

---

## 7. M：图连接密度

可以把 `M` 理解成每个节点连接多少邻居的主要控制量。

```text
M 小
→ 图更稀疏
→ Memory 低
→ Build 较轻
→ 搜索路径选择更少

M 大
→ 图更密
→ Recall 潜力更高
→ Memory / Build Cost 更高
```

所以 M 同时影响：

```text
Graph Degree
Memory
Build Cost
Search Quality
```

不能简单说：

> M 越大越好。

---

## 8. efConstruction：建图时搜多宽

插入新节点时，需要在已有图中寻找高质量邻居。

如果候选搜索很窄：

```text
Build 快
但 Neighbor Quality 可能差
```

如果搜索更宽：

```text
找到更好的邻居
图质量更高
但 Build 更慢
```

因此 `efConstruction` 主要控制：

```text
Build Time
Graph Quality
后续 Recall 上限
```

如果图本身建得很差，仅仅把 Query 阶段的 `efSearch` 拉高，不一定能完全补回来。

---

## 9. efSearch：查询时探索多宽

Query 时，如果候选集合很窄：

```text
Latency 低
但可能很早走错方向
```

如果维护更多候选：

```text
探索更充分
Recall 往往更高
CPU / Latency 更高
```

所以 `efSearch` 是典型在线调优旋钮：

```text
efSearch ↑
→ Recall 通常 ↑
→ Query Work ↑
→ Latency / CPU ↑
```

---

## 10. efSearch 和 Top-K 不是一个东西

假设最终返回：

```text
TopK = 10
```

不意味着：

```text
efSearch = 10
```

`TopK` 是最终返回结果数量。

`efSearch` 是搜索过程中愿意保留/探索多宽的候选集合。

通常会要求：

```text
efSearch >= K
```

但合理值必须由实际 Benchmark 决定。

---

## 11. 为什么 HNSW 很吃内存

除了原始向量，还要保存：

```text
Node Metadata
Neighbor IDs
Multi-layer Graph Links
```

所以 HNSW 常见 Trade-off：

> **用额外 Memory 和 Build Cost 换更低 Query Latency 与更高 Recall。**

这也是为什么它不是所有场景的唯一答案。

---

## 12. Filter 会改变最佳参数

加入：

```text
tenant_id = 42
permission_group in (...)
```

后，ANN 候选可能被大量过滤。

不同产品可能使用：

```text
pre-filter
post-filter
filter-aware traversal
```

同一个 `efSearch` 在无 Filter 和高选择性 Filter 下，Recall / Latency 表现可能完全不同。

所以 HNSW Benchmark 必须带真实 Filter Distribution。

---

## 13. 参数调优的正确流程

不要抄固定模板：

```text
M=16
efConstruction=200
efSearch=64
```

正确流程应该是：

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
- Recall
- P50 / P95 / P99
- QPS
- Memory
- Build Time
- Index Size
- Filter Performance
        ↓
Choose Operating Point
```

参数是数据、业务 SLA 和硬件共同决定的。

---

## 14. 数据变化后还要不要重新调

需要重新验证。

如果发生：

```text
N 从 100 万变 1 亿
Embedding Model 变化
Dimension 变化
Filter 复杂度变化
数据分布漂移
```

原来的 Recall / Latency 曲线都可能改变。

ANN 参数不是一次配置永久有效。

---

## 15. HNSW 的 Update / Delete 边界

Insert 相对自然，可以给新节点寻找邻居并接入图。

Delete / Update 更复杂，因为节点已经被其它节点引用。

很多产品可能采用：

```text
Tombstone
→ Background Cleanup
→ Compaction / Rebuild
```

具体实现不同，但这正是为什么后面需要独立学习 Index Lifecycle。

---

## 16. HNSW 不解决什么

HNSW 只解决 ANN 搜索基础设施的一部分。

它不会自动解决：

- Embedding 是否适合；
- Chunk 是否合理；
- Hybrid Retrieval；
- Rerank；
- Permission；
- RAG Evaluation。

因此：

> “用了 HNSW，所以 RAG Recall 高”不是充分证据。

---

## 17. 常见错误

- HNSW 是一棵树：错误，它是分层图。
- 高层保存所有节点：通常不是，高层更稀疏。
- HNSW 保证 100% Exact：错误。
- `M` 越大越好：忽略 Memory / Build Cost。
- `efSearch == TopK`：错误。
- 只要把 `efSearch` 拉高就能补救所有差索引：错误。
- 一组参数适合所有规模：错误。

---

## 18. 面试怎么答

### Q：HNSW 为什么高效？

> HNSW 把向量组织成分层近邻图，高层稀疏节点负责长距离快速导航，逐层下降后在底层做更宽的局部候选搜索，因此不必访问全部向量。它用额外图结构内存和较重的 Build Cost 换 Query Latency 与 Recall。

### Q：M、efConstruction、efSearch 分别控制什么？

> M 主要控制图连接密度；efConstruction 控制建图时候选搜索宽度，影响图质量与构建成本；efSearch 控制查询阶段探索宽度，是在线 Recall/Latency 的核心旋钮。参数应该用 Exact Ground Truth 和真实 Query/Filter Benchmark 调，而不是照抄固定值。

---

## 19. 自测

<details><summary>1. HNSW 为什么要分层？</summary>
高层负责长距离导航，底层负责局部精细搜索，减少访问节点数。
</details>

<details><summary>2. 为什么 efConstruction 影响后续 Recall 上限？</summary>
因为它影响建图时邻居选择质量；图结构本身差，查询阶段再扩大搜索也受到结构限制。
</details>

<details><summary>3. 为什么 Filter 会影响最佳 efSearch？</summary>
因为部分候选会被过滤，可能需要扩大搜索才能获得足够有效候选。
</details>
