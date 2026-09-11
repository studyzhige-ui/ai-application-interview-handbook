# 03. Normalization 与向量空间直觉

上一章知道了向量和 Dimension，这一章解决一个经常被忽略但会直接影响 Similarity 的问题：

> **向量的“方向”和“长度”分别在表达什么？为什么很多检索系统会做 Normalization？**

---

## 1. 先用二维空间建立直觉

假设：

```text
A = [3, 4]
```

它的长度：

```text
||A|| = 5
```

如果做 L2 Normalization：

```text
A' = A / ||A||
   = [0.6, 0.8]
```

归一化后：

```text
||A'|| = 1
```

方向不变，长度变成 1。

---

# 2. 为什么长度会影响 Dot Product

Dot Product：

```text
A · B = ||A|| ||B|| cos(theta)
```

所以它同时受：

```text
方向
+
向量长度
```

影响。

如果我们只想比较方向：

```text
Cosine Similarity = (A · B) / (||A|| ||B||)
```

就会把长度因素消掉。

---

# 3. Normalized Vector 上 Cosine 和 Dot 的关系

如果：

```text
||A|| = 1
||B|| = 1
```

那么：

```text
cosine(A, B) = A · B
```

因此很多系统在向量已经 L2 Normalized 时，可以用 Inner Product 来实现与 Cosine 等价的排序。

💡 这里说的是**排序 / 数值关系在单位向量条件下等价**，不是说所有系统 API 的距离值定义都完全相同。

---

# 4. Unit Vector 上 L2 与 Cosine 的关系

对于单位向量：

```text
||A - B||²
= ||A||² + ||B||² - 2A·B
= 2 - 2cos(theta)
```

因此：

```text
Cosine 越大
↔
Squared L2 越小
```

在所有向量都严格归一化时，它们的 Nearest Neighbor 排序可以对应起来。

---

# 5. 为什么不能盲目 Normalize

是否 Normalize 要服从 Embedding Model 的契约。

有些模型的推荐使用方式明确要求：

```text
normalize_embeddings = true
```

有些模型可能让向量 Norm 本身包含有用信息。

因此不能写一个通用函数：

```python
vector = vector / norm(vector)
```

然后对所有模型都这么做。

正确做法：

```text
Model Contract
→ Recommended Metric
→ Normalization Policy
→ Vector DB Index Metric
```

必须一致。

---

# 6. 为什么 Version Metadata 里要记录 Normalization

如果旧索引：

```text
Model A
not normalized
IP metric
```

新索引：

```text
Model B
normalized
Cosine metric
```

如果没有明确版本信息，很容易出现：

```text
数据看起来维度一样
但 Search Score 无法比较
```

所以建议记录：

```text
embedding_model
embedding_version
normalized: true/false
metric: cosine/ip/l2
```

---

# 7. Score 为什么不要跨系统生搬硬套

不同 Vector Store / Library 可能返回：

```text
similarity
```

或者：

```text
distance
```

甚至同一种 Metric 的输出定义也可能不同。

例如：

```text
Cosine Similarity 越大越近
L2 Distance 越小越近
```

所以业务代码不要假设：

```text
score > 0.8
```

在所有数据库和模型上都具有同样含义。

Threshold 必须经过：

```text
具体模型
+
具体 Metric
+
具体业务数据
```

验证。

---

# 8. 面试怎么答

## Q：为什么有些系统会先 Normalize Embedding？

🎯 **建议回答**：

> L2 Normalization 会把向量长度统一为 1，只保留方向。单位向量上 Cosine Similarity 等于 Dot Product，而且 Squared L2 与 Cosine 之间也存在单调关系，所以某些系统可以用更统一的距离计算方式。但是否应该 Normalize 取决于 Embedding Model 的推荐契约，不能对所有模型盲目处理。

---

# 9. 高频易错点

⚠️ **Cosine 和 Dot 永远相等。** 只有单位向量条件下成立。

⚠️ **Normalize 一定提高检索质量。** 不成立，要看模型训练与使用契约。

⚠️ **所有 Vector DB 返回的 score 都是越大越好。** 不一定，Distance 往往越小越近。

---

# 10. 本章自测

<details><summary>1. 单位向量上为什么 Cosine 等于 Dot Product？</summary>

因为 Cosine 的分母 `||A|| ||B||` 都等于 1。
</details>

<details><summary>2. 为什么不能对所有 Embedding 无脑做 Normalize？</summary>

因为不同模型的训练目标和推荐 Metric 不同，向量长度有时可能参与语义表达。应遵循具体模型契约。
</details>