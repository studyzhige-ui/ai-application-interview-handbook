# 18｜Dense Retrieval：什么时候语义向量擅长

## 1. 先讲人话

Dense Retrieval 把 Query 和文档都编码成稠密向量，再按 Cosine / Dot Product / L2 等相似度寻找近邻。

它擅长的是：

> **用户表达和文档表述不同，但语义相近。**

例如用户问：

> “离职以后还能继续用公司邮箱吗？”

文档写的是：

> “员工账户将在劳动关系终止后 24 小时内停用。”

Keyword 可能没有明显重合，但 Dense Embedding 有机会把它们拉近。

---

## 2. Dense Retrieval 的执行链

```text
Query
→ Embedding Model
→ Query Vector
→ Vector DB / ANN
→ Top-K Candidates
```

前一模块已经学习：

- Embedding Model 原理 → LLM Foundation；
- HNSW / IVF / ANN → Vector DB。

这里关注的是 Dense Retrieval 在 RAG Pipeline 中的使用边界。

---

## 3. Dense 擅长什么

- 同义改写；
- 自然语言概念查询；
- 问题与答案措辞不同；
- 多语言 / 跨表达检索（取决于模型）；
- 语义主题搜索。

---

## 4. Dense 的典型短板

### 精确字符串

例如：

```text
ERR_CONN_1042
SKU-AB-991
RFC 9110
```

这种 Query 的“精确词匹配”价值很高，Dense 不一定占优势。

### 稀有实体

Embedding 模型未充分学习的新产品名、内部缩写可能表示不稳定。

### 数字 / 版本 / 日期

`v1.7` 与 `v1.8` 在语义上很接近，但业务上可能完全不能混。

### 长 Chunk 语义稀释

一个 Chunk 包含多个主题时，向量会形成混合表示。

---

## 5. Dense Score 不能直接理解成“正确概率”

Cosine 0.82 不等于：

> “82% 概率答案正确。”

它只是当前 Embedding 空间和当前数据分布中的相似度。

Threshold 必须在自己的 Dataset 上校准。

---

## 6. Embedding Model 与 Corpus 必须匹配

要考虑：

- 语言；
- 领域；
- Query / Passage 是否使用不同前缀；
- 最大输入长度；
- Dimension；
- 是否为 Retrieval 专门训练。

换 Embedding Model 往往意味着整个 Index 的向量空间改变，需要版本化重建。

---

## 7. 怎样评估 Dense Retrieval

准备 `(query, relevant_doc/chunk)` Ground Truth，观察：

```text
Recall@K
MRR
Hit Rate
No-hit Rate
```

再按 Query 类型切 Slice：

- 概念问题；
- 精确编号；
- 专有名词；
- 短 Query；
- 长 Query。

通常会发现 Dense 在不同 Slice 上表现差异很大，这就是引入 Sparse / Hybrid 的依据。

---

## 8. 🎯 面试怎么回答

> Dense Retrieval 用 Embedding 把 Query 和文档映射到向量空间，擅长处理同义表达和语义相近但词面不同的问题。它的短板是精确编号、稀有实体、版本号、短关键词等，因此不能默认替代 Keyword Search。相似度分数也不是正确概率，需要在真实 Query Ground Truth 上做 Recall@K、MRR、Hit Rate 等评估，并根据 Query Slice 判断是否需要 Hybrid。

## 9. ⚠️ 易错点

- “向量搜索一定比 BM25 高级”；
- “Cosine 分数就是置信概率”；
- “Embedding Model 随便换，不影响旧 Index”；
- “ANN Recall = RAG Answer Quality”。

## 10. 🔍 继续追问

- 为什么短 Query 可能对 Dense 不友好？
- Query Prefix / Passage Prefix 有什么意义？
- 如何发现 Embedding Model 不适合自己的领域？

<details><summary>查看参考答案：为什么 Dense Retrieval 不能独立解决所有检索问题？</summary>

因为语义相似和精确匹配是两类不同信号。产品编号、错误码、版本号等任务往往要求词项级精确性，而 Dense 更擅长语义泛化，所以 Production 系统常通过 Sparse / Hybrid 补足。

</details>
