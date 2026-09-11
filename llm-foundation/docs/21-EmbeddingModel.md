# 21｜Embedding Model 为什么能表示语义

## 1. 先讲人话

Embedding Model 的目标不是生成文本，而是把输入映射成一个向量：

```text
Text / Image / Item
      ↓
Embedding Model
      ↓
[d1, d2, ..., dn]
```

这个向量应该满足：

> 语义越接近的输入，在向量空间里通常也越接近。

这就是 Vector DB 和 RAG 能工作的模型侧基础。

---

## 2. Embedding Model 与 Generation Model 的目标不同

### Generation Model

优化：

```text
P(next token | previous tokens)
```

用于：

- 对话；
- 生成；
- 推理；
- Tool Call。

### Embedding Model

优化：

> 让相关样本距离更近，不相关样本距离更远。

用于：

- Semantic Search；
- Clustering；
- Dedup；
- Recommendation Feature；
- RAG Retrieval。

所以不能说：

> “Embedding 就是让 Chat Model 输出 hidden state。”

有专门训练过的 Embedding Model，目标更适合检索。

---

## 3. Bi-Encoder 结构

经典检索 Embedding 常采用 Bi-Encoder：

```text
Query ──Encoder──> q vector
Doc   ──Encoder──> d vector
```

然后离线存文档向量，在线只计算 Query 向量：

```text
q
↓
ANN Search against precomputed d vectors
```

这就是它能大规模检索的关键。

---

## 4. Embedding 怎样训练

应用岗需要理解 Contrastive Learning 直觉。

给定：

```text
Query
Positive Document
Negative Documents
```

训练目标希望：

```text
sim(query, positive) ↑
sim(query, negative) ↓
```

Negative 的质量非常重要。

如果 Negative 太简单，模型学不到细粒度区分；如果有高质量 Hard Negative，通常更能逼模型理解真正语义边界。

---

## 5. Dimension 是怎么来的

Embedding 输出通常是固定维度向量。

维度更高可能提供更大表示容量，但也会增加：

- Vector Storage；
- Network；
- ANN Memory；
- Distance Compute；
- Index Build Cost。

所以：

> Dimension 是模型能力和基础设施成本的共同参数。

Vector DB 已经从存储侧讲过这一点，这里补模型侧。

---

## 6. Normalization 与 Similarity

一些 Embedding 模型推荐先 L2 Normalize，再用 Dot Product / Cosine。

如果：

```text
||q|| = ||d|| = 1
```

那么：

```text
cosine(q,d) = q · d
```

但是否需要 Normalize、该用哪种距离，应遵循模型训练与官方建议，不能随意替换。

---

## 7. Query / Document Instruction

某些检索模型对 Query 和 Document 使用不同前缀或 Prompt，例如表达：

```text
query: ...
passage: ...
```

因为训练时可能区分两类输入。

如果部署时漏掉预期 Instruction，检索效果可能下降。

所以 Embedding 并不是：

> “随便调用 encode(text) 就完事”。

---

## 8. Domain Shift

通用 Embedding 在企业领域可能遇到：

- 缩写；
- 法律术语；
- 医疗术语；
- 内部产品名；
- 代码符号；
- 表格 / OCR 噪声。

于是可能需要：

- 换 Domain Model；
- Fine-tune Embedding；
- 调整 Chunk；
- Hybrid Retrieval；
- Reranker。

不能看到 Recall 差就直接怪 Vector DB。

---

## 9. Embedding Model 升级为什么麻烦

新模型通常意味着：

```text
Vector Space 改变
Dimension 可能改变
Similarity Calibration 改变
```

旧向量和新向量往往不能安全混用。

因此需要：

```text
model_version
embedding_version
re-embedding
blue-green index
rollback
```

Vector DB 的生命周期章节已经讲过基础设施侧，这里说明根因来自模型空间变化。

---

## 10. 🎯 面试怎么回答

> Embedding Model 把输入编码成固定维度向量，并通过对比学习等目标，让相关样本更近、不相关样本更远。检索里常用 Bi-Encoder，因为文档向量能离线预计算，在线只计算 Query 向量，再交给 ANN 搜索。模型选型要看领域、语言、维度、训练目标和官方推荐的相似度；升级 Embedding Model 时通常需要版本化和重新向量化，不能默认新旧向量空间兼容。

---

## 11. ⚠️ 易错点

错误：

> 维度越高，Embedding 一定越好。

错误：

> Vector DB Recall 低一定是 HNSW 参数问题。

可能是模型、Chunk、Query、领域偏移或距离配置。

---

<details>
<summary>自测：为什么 Bi-Encoder 适合大规模 Retrieval？</summary>

因为 Query 和 Document 可以独立编码，Document 向量提前计算并建立 ANN Index，在线只需计算 Query 向量和做近邻搜索，不需要对每个 Query-Document Pair 都跑一次模型。

</details>
