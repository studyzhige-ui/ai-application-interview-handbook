# 06. 为什么需要 ANN：用 Recall 换 Latency

前一章的 Exact Search 很准确，但规模大时太贵。

ANN 的核心问题是：

> **能不能不看所有向量，也大概率找到真正的近邻？**

ANN = Approximate Nearest Neighbor。

---

## 1. Approximate 到底近似什么

它不是说：

```text
距离函数算错了
```

而是说：

> **搜索过程可能没有访问到所有候选，所以返回结果不保证和 Exact Top-K 完全一致。**

例如 Exact Top5：

```text
A B C D E
```

ANN 返回：

```text
A B C X D
```

它漏掉了 E。

这就是 Recall Loss。

---

# 2. Recall 怎么理解

如果 Exact Top10 中有 10 个真实近邻，而 ANN 找回其中 9 个：

```text
Recall@10 = 0.9
```

这里我们只建立 ANN Index 评估直觉。

完整 Retrieval Evaluation 仍然属于 RAG，因为最终 RAG 还要评估：

- 是否召回相关文档；
- 排序是否合理；
- Answer 是否正确；
- Rerank 是否改善；

而 Vector DB 层更关心：

> **ANN 相对 Exact Ground Truth 丢了多少近邻。**

---

# 3. ANN 的本质 Trade-off

```text
更多搜索工作量
→ 更高 Recall
→ 更高 Latency / CPU

更少搜索工作量
→ 更低 Latency
→ 可能更低 Recall
```

所以 ANN 没有一个“最优参数”。

正确目标是：

```text
在业务可接受 Recall 下
把 Latency / QPS / Memory 控制在目标范围
```

---

# 4. ANN 为什么能比 Exact 少看很多数据

主流思路大致有三类。

## 4.1 Graph-based

例如：

```text
HNSW
```

把向量连接成近邻图，然后：

```text
从入口开始
→ 沿越来越近的节点导航
→ 不访问全库
```

## 4.2 Partition-based

例如：

```text
IVF
```

先把空间划成多个区域：

```text
Query
→ 找最接近的几个区域
→ 只搜索这些区域
```

## 4.3 Compression / Quantization

例如：

```text
PQ / SQ
```

把向量压缩，让：

- 内存更小；
- 距离估计更快；

代价是精度损失。

实际系统还会组合这些方法。

---

# 5. 为什么高维空间特别需要 ANN

传统数据库习惯：

```text
B+Tree
Hash
```

这些结构非常适合：

```text
排序键
精确 Key
范围
```

但高维向量没有一个简单的一维排序可以同时保持所有邻近关系。

因此现代向量搜索会发展出：

```text
Graph Navigation
Clustering / Partition
Quantization
```

这样的专用索引路线。

---

# 6. ANN Index 自己也有成本

不能只看到查询更快。

ANN 通常会引入：

```text
Build Time
Extra Memory
Index Storage
Insert / Update Cost
Delete Complexity
Rebuild / Compaction
```

例如 HNSW：

```text
图边越多
→ 搜索可能更好
→ Memory 越大
→ Build 越贵
```

IVF：

```text
Partition 越细
→ 候选范围可更小
→ 训练 / 参数与数据分布更敏感
```

所以：

> ANN 不是“免费加速器”。

---

# 7. ANN 参数应该怎么调

不要先背：

```text
efSearch = 64
nprobe = 10
```

正确流程：

```text
Representative Query Set
        ↓
Exact Ground Truth
        ↓
Build ANN Index
        ↓
Sweep Parameters
        ↓
Measure Recall / P95 Latency / QPS / Memory
        ↓
Choose Operating Point
```

这才是工程化调优。

---

# 8. ANN 召回掉了，一定是 Index 的错吗

不一定。

如果最终业务“没召回到相关文档”，可能是：

```text
Embedding 不适合
Chunk 不对
Query Rewrite 错
Metric 错
Filter 太严格
ANN Recall Loss
```

因此排查时要分层：

```text
Exact Vector Search 也找不到
→ 更可能是 Embedding / Corpus / Query 问题

Exact 能找到，ANN 找不到
→ 更像 ANN Index / Parameter 问题
```

这个诊断思路非常重要。

---

# 9. 面试怎么答

## Q：ANN 牺牲了什么，换来了什么？

🎯 **建议回答**：

> ANN 主要牺牲“返回结果和 Exact Nearest Neighbor 完全一致”的保证，换取更少的候选访问、更低延迟和更高吞吐。工程上不会只追求最高 Recall，而是用 Exact Search 建 Ground Truth，再在代表性 Query 上调参数，找到 Recall、P95 Latency、QPS、Memory 和 Build Cost 的平衡点。

## Q：RAG 召回差怎么判断是不是 ANN 导致的？

> 可以先对同一批 Query 用 Exact Search 对比。如果 Exact 也找不到相关向量，问题更可能在 Embedding、Chunk、Query 或 Filter；如果 Exact 能找到而 ANN 丢失，才重点检查 ANN Index 和参数。

---

# 10. 高频易错点

⚠️ **ANN 是距离计算的近似公式。** 不准确，核心通常是近似搜索过程 / 候选选择。

⚠️ **ANN Recall 越高越好，直接拉满参数。** 会带来 Latency / CPU / Memory 成本。

⚠️ **RAG Recall 低就是 Vector DB Recall 低。** 错误，RAG 是更大的系统。

---

# 11. 本章自测

<details><summary>1. ANN 的 Approximate 主要体现在哪里？</summary>

搜索过程不会访问所有向量，因此不保证返回结果与 Exact Top-K 完全一致。
</details>

<details><summary>2. 怎样证明某组 ANN 参数合适？</summary>

用代表性 Query 和 Exact Ground Truth，测不同参数下的 Recall、Latency、QPS、Memory 等指标，选择满足业务约束的 operating point。
</details>