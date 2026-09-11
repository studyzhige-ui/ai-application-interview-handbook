# 02. Vector、Embedding Storage Semantics 与 Dimension

这一章不讲 Embedding Model 怎么训练，而只回答 Vector DB 的第一个问题：

> **数据库实际拿到的“向量”是什么，它的维度为什么重要？**

---

## 1. Vector 最直观的样子

```text
[0.12, -0.33, 0.98, 0.04]
```

这是一个 4 维向量。

实际 Embedding 常见是数百到数千维，例如：

```text
D = 768
D = 1024
D = 1536
...
```

Vector DB 通常要求同一个 Vector Field 中的向量维度固定。

因为：

```text
query_vector
```

必须和：

```text
stored_vector
```

在同一个向量空间中比较。

---

# 2. Dimension 是什么

如果：

```text
v = [x1, x2, ..., xd]
```

那么：

```text
d = Dimension
```

Dimension 不是“越大越好”的质量分数。

它至少影响：

```text
单条向量存储大小
内存占用
距离计算成本
索引大小
网络传输
Cache Locality
```

例如 float32：

```text
1536 dimensions × 4 bytes
≈ 6144 bytes
≈ 6 KB / vector
```

如果有 1 亿条：

```text
约 600 GB raw vector data
```

这还没算：

- ID；
- Metadata；
- Index；
- Graph Edge；
- Replica；
- 内存管理开销。

所以 Dimension 会直接进入容量规划。

---

# 3. Vector DB 不应该随意理解坐标含义

很多人会问：

> 第 327 维到底表示“金融”还是“法律”？

对于常见 Dense Embedding，通常不能把单一维度解释成稳定的人类语义标签。

Vector DB 更关心：

```text
整体几何关系
```

例如：

```text
A 与 B 距离近
C 与 A 距离远
```

它不会理解“为什么”这个语义关系存在。

---

# 4. 同维度不代表同空间

这是非常重要的工程边界。

假设：

```text
Model A → 768 dim
Model B → 768 dim
```

不能因为维度相同，就把它们混进同一个索引然后比较。

因为它们可能学习出了完全不同的坐标空间。

正确理解：

```text
Dimension 相同
≠
Embedding Space 相同
```

所以 Embedding Model 升级时，常见做法是：

```text
new_model
→ re-embedding
→ new index / new collection
→ validation
→ traffic switch
```

而不是把新旧向量直接混用。

---

# 5. Query Vector 和 Document Vector 必须兼容

某些模型：

```text
query encoder
!=
document encoder
```

或者需要不同 prefix：

```text
query: ...
passage: ...
```

这属于 Embedding Model 的输入契约。

Vector DB 只负责存储结果，但必须把这些契约记录在：

```text
embedding_model_version
embedding_dimension
normalization
metric
index_version
```

否则长期维护会很危险。

---

# 6. 一条向量记录应该带哪些版本信息

推荐至少能追踪：

```text
record_id
source_id
embedding_model
embedding_version
dimension
metric
content_version
updated_at
```

如果知识库发生：

```text
模型升级
文档更新
Chunk 策略改变
```

就能判断哪些向量需要重建。

---

# 7. Dimension 越高，搜索一定越好吗

不是。

更高维可能带来更强表示能力，但也可能：

```text
存储更多
计算更贵
Index 更大
Memory 更高
```

而最终 Retrieval Quality 主要由：

- 模型训练；
- 数据域；
- Query / Document Contract；
- Chunk；
- Retrieval Pipeline；

共同决定。

所以 Vector DB 不能只看 Dimension 做模型选型。

---

# 8. Curse of Dimensionality 先建立直觉

高维空间中，一个常见问题是：

> 随着维度上升，距离分布会变得更难区分，传统低维空间中的索引结构未必仍然有效。

这也是为什么：

```text
B-Tree / KD-Tree
```

不能简单直接解决现代高维 Embedding 的大规模近邻搜索。

后面 ANN Index 会针对这个问题发展出：

```text
Graph-based Search
Partition / Quantization
```

等路线。

---

# 9. 面试怎么答

## Q：Vector Dimension 对系统有什么影响？

🎯 **建议回答**：

> Dimension 决定每个向量包含多少个数值，会直接影响 raw storage、距离计算、索引内存和网络成本。以 float32 为例，1536 维单条原始向量大约 6 KB，大规模数据下容量会非常明显。同时维度相同不代表来自同一个 embedding space，新旧模型即使都是 768 维也不能默认直接混搜，通常要做版本化和 re-embedding。

---

# 10. 高频易错点

⚠️ **维度越高模型一定越好。** 不是。

⚠️ **两个 768 维模型可以直接混用。** 错误。

⚠️ **Vector DB 能解释每一个维度的语义。** 通常不能。

⚠️ **只计算 raw vector 大小就等于系统总内存。** 错误，还要考虑 Index / Metadata / Replica 等。

---

# 11. 本章自测

<details><summary>1. 为什么同样 768 维的新旧 Embedding Model 不能直接混进同一个索引？</summary>

因为它们可能属于完全不同的表示空间；维度相同只说明数组长度相同，不保证坐标语义和距离关系兼容。
</details>

<details><summary>2. 1536 维 float32 向量单条 raw 大约多少？</summary>

1536 × 4 = 6144 bytes，大约 6 KB。实际系统总占用还要加索引、ID、Metadata、Replica 等。
</details>