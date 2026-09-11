# 01. Vector DB 在 AI Application 中负责什么

很多初学者第一次接触 Vector DB，是从一句话开始：

> “RAG 要把 Embedding 存进向量数据库。”

这句话没错，但太容易让人误以为：

> Vector DB = 一个能存 `list[float]` 的地方。

真正需要建立的理解是：

> **Vector DB 的核心职责，是在大量高维向量上提供可维护、可过滤、可扩展的近邻搜索基础设施。**

---

## 1. 先看一个 AI Knowledge Base

原始文档：

```text
Document
  ↓
Chunk
  ↓
Embedding Model
  ↓
Vector
```

例如：

```text
Chunk A → [0.12, -0.33, 0.98, ...]
Chunk B → [0.08, -0.28, 0.95, ...]
Chunk C → [-0.72, 0.19, 0.04, ...]
```

查询时：

```text
User Query
  ↓
Embedding
  ↓
Query Vector
  ↓
找最相近的 K 个 Chunk Vector
```

如果只有 100 条：

```text
逐个算距离
```

完全可以。

但如果变成：

```text
100 万
1000 万
10 亿
```

问题就不只是“存进去”了，而是：

```text
怎么找得快？
召回损失多少？
内存放得下吗？
怎么过滤 tenant_id？
更新文档后旧向量怎么办？
模型升级后要不要全部重算？
多个节点怎么分片？
索引什么时候 rebuild？
```

这些才是 Vector DB 的主体。

---

# 2. Vector DB 不是 Embedding Model

必须先分清两层。

## Embedding Model

负责：

```text
Text / Image / Code
→ Vector
```

它决定：

- 语义空间怎样形成；
- 哪些内容靠近；
- Dimension 多大；
- 是否需要 Normalization；
- Query / Document 是否使用同一编码方式。

这些 Primary 在 **LLM Foundation**。

## Vector DB

拿到已经生成的向量后负责：

```text
Store
Index
Search
Filter
Update
Delete
Scale
```

💡 可以理解为：

> Embedding Model 决定“坐标怎么生成”，Vector DB 决定“海量坐标怎么存和找”。

---

# 3. Vector DB 也不等于完整 RAG Retrieval

完整 Retrieval 可能包含：

```text
Dense Retrieval
+
BM25 / Sparse Retrieval
+
Hybrid Fusion
+
Rerank
+
Top-K / Context Budget
+
Evaluation
```

这些属于 RAG 的检索系统设计。

Vector DB 在其中通常只承担一部分：

```text
Dense Vector Storage
+
ANN Search
+
Metadata Filter
```

所以：

```text
Vector DB 好
≠
RAG 一定好
```

如果 Chunk 错、Embedding 不适合、Query Rewrite 错、Reranker 差，Vector DB 再快也救不了最终答案。

---

# 4. Vector DB 和普通关系数据库有什么不同

关系数据库常见查询：

```sql
WHERE tenant_id = 42
  AND status = 'ACTIVE'
ORDER BY created_at DESC
```

它在匹配：

```text
精确值
范围
排序
关系
```

Vector Search 更像：

> 给我最接近这个向量的 K 条记录。

形式上：

```text
arg topK similarity(query_vector, stored_vector)
```

核心问题变成：

```text
高维空间中的 Nearest Neighbor Search
```

这就是后续 ANN Index 的来源。

---

# 5. 一个 Vector Record 通常不只有 Vector

真实记录更像：

```text
id          chunk_9871
vector      [0.12, ...]
tenant_id   42
doc_id      doc_1001
version     v3
language    zh
created_at  ...
permission  team_a
```

所以查询可能是：

```text
找到最相似的 20 个向量
AND tenant_id = 42
AND version = current
AND permission 可访问
```

这就是为什么 Vector DB 还必须讨论：

- Metadata；
- Filter；
- Partition；
- Tenant Isolation；
- Version；
- Delete / Update。

---

# 6. 为什么不是所有项目都需要独立 Vector DB

如果只有：

```text
10 万条向量
低 QPS
已经有 PostgreSQL
简单 Filter
```

可能使用：

```text
pgvector
```

就足够。

如果是本地算法实验：

```text
FAISS
```

可能更直接。

如果已有搜索平台，还需要全文 + Vector：

```text
Elasticsearch / OpenSearch Vector
```

可能更自然。

如果规模、ANN、分片、过滤、生命周期都成为一等问题，才更像专用 Vector DB 的场景。

因此：

> **“RAG 就必须上某个独立 Vector DB”不是一个正确前提。**

后面产品选型章节会系统比较。

---

# 7. Vector DB 最核心的六个问题

整个模块都可以围绕这六个问题理解：

```text
1. 怎样表示？
   Dimension / Normalization

2. 怎样比较？
   Cosine / IP / L2

3. 怎样找？
   Exact / ANN / HNSW / IVF

4. 怎样约束？
   Metadata / Filter / Tenant

5. 怎样变化？
   Insert / Update / Delete / Rebuild

6. 怎样扩展？
   Memory / QPS / Shard / Replica / Product Selection
```

---

# 8. AI 应用中的典型数据分工

```text
MySQL
  └─ User / Tenant / Document / Business State

Redis
  └─ Cache / Session / Short-lived State

Vector DB
  └─ Embedding Vector + Retrieval Metadata

Object Storage
  └─ PDF / Image / Original File
```

这只是常见分工，不是硬规则。

例如：

- Metadata 可以同时存在 MySQL 与 Vector Store；
- pgvector 本身就在 PostgreSQL 里；
- Elasticsearch 可以同时承载 Keyword 与 Vector Search。

真正要问的是：

> **哪个系统是 Source of Truth？哪个只是可重建索引？**

---

# 9. 面试怎么答

## Q：Vector DB 是做什么的？

🎯 **30 秒回答**：

> Vector DB 主要解决大规模高维向量的存储和近邻搜索问题。相比单纯保存 float 数组，它通常还提供 ANN Index、Metadata Filter、更新删除、分片副本和索引生命周期等能力。在 RAG 中它通常承担 Dense Vector Retrieval Infrastructure，但 Embedding Model 原理、Hybrid Retrieval、Rerank 和 Retrieval Evaluation 分别属于模型和 RAG 系统层，不能把整个 RAG 都等同于 Vector DB。

## Q：为什么不用 MySQL 直接存 JSON 向量？

> 存本身并不难，关键是如何在大量高维向量上做高效 Top-K 相似搜索，并兼顾过滤、更新和扩展。普通 JSON/BLOB 存储没有自动解决 ANN Index 这件事。当然，如果使用支持 Vector Type 和 ANN Index 的数据库扩展，例如 pgvector，那么它已经不再是“普通 JSON 存储”的问题了。

---

# 10. 高频易错点

⚠️ **Vector DB = RAG。**  
错误。它只是 Retrieval Infrastructure 的一部分。

⚠️ **Vector DB 负责训练 Embedding。**  
通常错误。Embedding Model 和 Vector Store 是不同层。

⚠️ **用了 Vector DB 就一定比暴力搜索更准。**  
ANN 通常是在 Recall 与性能之间做 Trade-off，Exact Search 才是精确基线。

⚠️ **做 RAG 一定需要专用 Vector DB。**  
错误，要看规模、已有基础设施、过滤、更新与运维要求。

---

# 11. 本章自测

<details>
<summary>1. Vector DB 与 Embedding Model 的边界是什么？</summary>

Embedding Model 把输入映射成向量并决定语义空间；Vector DB 负责已有向量的存储、索引、近邻搜索、过滤、更新和扩展。

</details>

<details>
<summary>2. 为什么说 Vector DB 不是完整 RAG？</summary>

因为完整 RAG 还包含文档处理、Chunk、Query Transformation、Sparse / Hybrid Retrieval、Fusion、Rerank、Context Build、Grounding 与 Evaluation 等能力。

</details>

<details>
<summary>3. 为什么一个 Vector Record 通常还需要 Metadata？</summary>

因为真实查询往往既要求语义相似，又要求 tenant、权限、版本、文档类型等结构化约束。只存向量无法完成这些业务过滤。

</details>