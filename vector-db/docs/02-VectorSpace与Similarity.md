# 02. Vector Space & Similarity：Dimension、Normalization 与距离度量

这一章把三个原本分开的前置知识合成一个完整问题：

> **Vector DB 实际存的向量是什么？它们为什么能比较？Dimension、Normalization、Cosine / Dot / L2 又分别影响什么？**

---

## 1. Vector 最直观的样子

```text
[0.12, -0.33, 0.98, 0.04]
```

这是一个 4 维向量。

实际 Embedding 常见是几百到几千维：

```text
D = 768
D = 1024
D = 1536
...
```

同一个 Vector Field 中通常要求 Dimension 固定，因为 Query Vector 和 Stored Vector 必须能在同一个向量空间中比较。

---

## 2. Dimension 不只是数组长度

如果：

```text
v = [x1, x2, ..., xd]
```

那么 `d` 就是 Dimension。

它会直接影响：

```text
Raw Storage
Distance Compute Cost
Index Size
Memory
Network Transfer
Cache Locality
```

例如 float32：

```text
1536 × 4 bytes ≈ 6 KB / vector
```

一亿条向量的 Raw Data 就已经约 600GB，还没算：

- ID / Metadata；
- ANN Index；
- HNSW Graph Edge；
- Replica；
- Allocator / Cache；
- Segment / Storage Engine 开销。

所以 Dimension 会直接进入容量规划。

---

## 3. 同维度不代表同一个向量空间

这是最重要的工程边界之一。

```text
Model A → 768 dim
Model B → 768 dim
```

不能因为都是 768 维，就把它们直接混进同一个索引。

因为：

```text
Dimension 相同
≠
Embedding Space 相同
```

新旧模型升级时，常见做法是：

```text
new model
→ re-embedding
→ new index generation
→ validation
→ traffic switch
```

而不是新 Query 用 v2、旧 Document 仍保留 v1。

---

## 4. 向量的方向与长度

假设：

```text
A = [3, 4]
||A|| = 5
```

做 L2 Normalization：

```text
A' = A / ||A|| = [0.6, 0.8]
```

归一化后：

```text
||A'|| = 1
```

方向不变，长度变成 1。

这很重要，因为不同距离函数对“方向”和“长度”的关注不同。

---

## 5. Cosine / Dot Product / L2 到底在比较什么

### Cosine Similarity

```text
cos(A, B) = (A · B) / (||A|| ||B||)
```

更关注方向是否一致。

### Dot Product / Inner Product

```text
A · B = Σ ai * bi
```

同时受：

```text
方向 + Norm / Magnitude
```

影响。

### L2 / Euclidean Distance

```text
L2(A, B) = sqrt(Σ(ai-bi)²)
```

关注空间里的绝对距离。

通常：

```text
Cosine / IP → 越大越近
L2 → 越小越近
```

但具体数据库 API 可能返回 similarity 或 distance，所以不要假设所有 `score` 都是“越大越好”。

---

## 6. Normalized Vector 上三种 Metric 的关系

如果：

```text
||A|| = ||B|| = 1
```

那么：

```text
Cosine(A,B) = A · B
```

而且：

```text
||A-B||² = 2 - 2cos(A,B)
```

因此单位向量上：

```text
Cosine 越大
↔ Squared L2 越小
```

近邻排序可以形成单调对应关系。

注意：

> 这不意味着所有数据库的 API 数值完全一样，也不意味着任何模型都应该先 Normalize。

---

## 7. 为什么不能无脑 Normalize

是否 Normalize 必须服从 Embedding Model 的契约。

有些模型明确要求：

```text
normalize embeddings
```

有些模型可能让 Norm 本身包含信息。

正确链路应该是：

```text
Embedding Model Contract
→ Recommended Metric
→ Normalization Policy
→ Vector DB Index Metric
```

而不是写一个全局：

```python
vector = vector / norm(vector)
```

对所有模型都处理。

---

## 8. Metric 选错会发生什么

如果模型按 Cosine 空间训练，但你把未归一化向量直接按 Inner Product 排序，可能出现：

```text
Norm 较大的 Vector
→ Dot Product 被放大
→ Ranking 偏离模型训练目标
```

这时不是 Vector DB “索引不准”，而是：

> **Embedding / Normalization / Metric Contract 不一致。**

Metric 通常还是 Index Schema 的一部分，不能期待一个已经按某种 Metric 建好的 ANN Index 查询时任意切换另一种 Metric。

---

## 9. 一个简单例子

```text
A = [1,0]
B = [10,0]
C = [0.8,0.6]
```

Cosine：

```text
cos(A,B)=1
cos(A,C)=0.8
```

按方向 B 更接近 A。

但 L2：

```text
L2(A,B)=9
L2(A,C)≈0.632
```

按绝对距离 C 更近。

所以：

> **Metric 不是实现细节，而是在定义“相似”本身。**

---

## 10. Score Threshold 为什么不能抄固定值

常见错误：

```text
score > 0.8 → relevant
```

但 Score Distribution 会受：

- Model；
- Domain；
- Query Length；
- Normalization；
- Metric；
- Corpus Distribution；

影响。

所以阈值必须通过真实数据验证。

RAG 层会进一步讨论 Retrieval Threshold / No-hit，但 Vector DB 层至少要知道：

> 相似度分数没有跨模型、跨系统统一绝对语义。

---

## 11. Vector Record 应记录哪些契约

推荐至少追踪：

```text
record_id
source_id
embedding_model
embedding_version
dimension
normalized
metric
content_version
index_generation
updated_at
```

这样模型、Chunk、Metric 或 Index 升级时，才知道哪些数据需要迁移。

---

## 12. 高频易错点

- Dimension 越高一定越好：错误。
- 两个 768 维模型可以直接混搜：错误。
- Cosine 和 Dot 永远相等：只有单位向量条件下成立。
- 所有 score 都越大越好：错误。
- Normalize 一定提升检索质量：错误。
- 0.8 是通用相似度阈值：错误。

---

## 13. 面试怎么答

### Q：Cosine、Dot Product、L2 怎么选？

> Cosine 更关注方向，Inner Product 同时受方向和向量长度影响，L2 表示欧氏距离。单位向量上 Cosine 等于 Dot Product，Squared L2 与 Cosine 之间也有单调关系。实际选型应该服从 Embedding Model 的训练契约，并确保 Normalization 和 Vector Index Metric 一致，而不是固定认为文本检索永远用 Cosine。

### Q：Dimension 对系统有什么影响？

> Dimension 会影响 Raw Storage、距离计算、索引大小、内存和网络成本；而且相同维度不代表相同 embedding space，因此模型升级通常需要版本化和重新 Embedding。

---

## 14. 自测

<details><summary>1. 为什么相同 Dimension 不代表新旧模型可以混搜？</summary>
因为 Dimension 只表示数组长度，不保证两个模型学习出的空间坐标和距离关系兼容。
</details>

<details><summary>2. 为什么单位向量上 Cosine 和 Dot 等价？</summary>
因为 Cosine 的分母 `||A||||B||` 等于 1。
</details>

<details><summary>3. Metric 选错为什么会表现成“召回变差”？</summary>
因为近邻排序本身被改变，检索目标和 Embedding 模型训练目标不一致。
</details>
