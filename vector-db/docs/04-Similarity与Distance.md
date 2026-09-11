# 04. Cosine / Dot Product / L2：到底在比较什么

Vector Search 最核心的数学问题其实不复杂：

> **给定 Query Vector，怎样定义“谁更近”？**

常见三种：

```text
Cosine Similarity
Dot Product / Inner Product
L2 / Euclidean Distance
```

这一章只讲到足够支持工程判断的深度。

---

## 1. Cosine Similarity

定义：

```text
cos(A, B) = (A · B) / (||A|| ||B||)
```

直觉：

> 更关注两个向量的方向是否一致。

如果两个向量方向相同，即使长度不同，Cosine 仍然很高。

适合很多语义 Embedding 场景，因为“方向”常被用来表达语义接近程度。

---

# 2. Dot Product / Inner Product

```text
A · B = Σ ai * bi
```

它同时受到：

```text
方向
+
Magnitude / Norm
```

影响。

如果向量已经归一化：

```text
Dot Product = Cosine Similarity
```

否则不能这样说。

---

# 3. L2 / Euclidean Distance

```text
L2(A, B) = sqrt(Σ(ai - bi)²)
```

直觉：

> 两个点在空间里的直线距离。

L2 越小，通常认为越近。

为了节省计算，很多排序场景可以使用 Squared L2：

```text
Σ(ai - bi)²
```

因为 `sqrt` 是单调函数，不改变排序。

---

# 4. 三者怎样比较

| Metric | 越大/越小越近 | 是否看 Norm | 常见使用方式 |
|---|---|---|---|
| Cosine | 越大越近 | 消除 Norm | 语义方向相似 |
| Inner Product | 越大越近 | 看 Norm | 模型明确以 IP 训练 / 已 Normalize |
| L2 | 越小越近 | 看绝对位置 | Euclidean Space |

没有“Vector DB 永远应该用 Cosine”这种规则。

正确流程：

```text
Embedding Model Contract
→ Recommended Similarity
→ 是否 Normalize
→ Vector Index Metric
```

---

# 5. Metric 选错会怎样

假设模型是按 Cosine 语义训练的，但你把未归一化向量直接按 Inner Product 排序。

可能出现：

```text
某些 Norm 较大的向量
→ Dot Product 被放大
→ 排名偏离模型训练目标
```

这不是 Vector DB “索引不准”，而是 Metric Contract 错了。

---

# 6. 距离函数必须和 Index 一致

很多 ANN Index 在构建时就绑定了 Metric。

例如：

```text
HNSW(cosine)
```

不能期待查询时临时改成：

```text
L2
```

还得到完全正确的同一索引行为。

因此 Metric 是 Index Schema 的一部分，不只是一个查询参数。

---

# 7. Threshold 不要靠感觉

常见代码：

```text
if score > 0.8:
    accept
```

这个 `0.8` 如果没有 Evaluation，就是危险魔法数字。

因为 Score Distribution 会受：

- Model；
- Domain；
- Query Length；
- Normalization；
- Metric；
- 数据质量；

影响。

Threshold 应通过业务数据验证。

Threshold Strategy Primary 在 RAG Evaluation，但 Vector DB 这一层必须知道：

> Score 本身没有跨模型、跨数据库的统一绝对语义。

---

# 8. 一个简单例子

```text
A = [1, 0]
B = [10, 0]
C = [0.8, 0.6]
```

Cosine：

```text
cos(A, B) = 1
cos(A, C) = 0.8
```

按方向：

```text
B 比 C 更像 A
```

L2：

```text
L2(A, B) = 9
L2(A, C) ≈ 0.632
```

按绝对距离：

```text
C 比 B 更近
```

这说明：

> Metric 不是实现细节，而是在定义“相似”本身。

---

# 9. 面试怎么答

## Q：Cosine、Dot Product、L2 有什么区别？

🎯 **建议回答**：

> Cosine 主要比较方向，会除以两个向量的 Norm；Inner Product 既受方向也受长度影响；L2 比较空间中的欧氏距离。单位向量上 Cosine 等于 Dot Product，Squared L2 和 Cosine 之间也存在单调关系。实际选择不应凭喜好，而应该遵循 Embedding Model 的训练和推荐 Metric，并让数据库索引配置保持一致。

---

# 10. 高频易错点

⚠️ **Cosine 一定比 L2 更适合文本。** 不能绝对化，要看模型契约。

⚠️ **Similarity Score 越大永远越好。** Distance API 可能是越小越好。

⚠️ **同一个索引可以随便切换 Metric。** 通常不应该这样理解。

⚠️ **0.8 是通用的语义相似阈值。** 错误。

---

# 11. 本章自测

<details><summary>1. 为什么 Metric 选错可能导致检索质量下降？</summary>

因为 Metric 决定近邻排序，而 Embedding Model 的空间通常与某种相似度契约绑定。错误 Metric 可能让排序目标偏离模型训练目标。
</details>

<details><summary>2. 单位向量上为什么 L2 与 Cosine 的排序可以对应？</summary>

因为 `||A-B||² = 2 - 2cos(A,B)`，一个增大时另一个单调减小。
</details>