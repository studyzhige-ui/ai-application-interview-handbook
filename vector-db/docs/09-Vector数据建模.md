# 09｜Collection / Schema / Primary Key / Metadata

真正的 Vector DB 记录通常不是：

```text
[0.1, 0.2, ...]
```

而是：

```text
ID
Vector
Metadata
Version
Business Fields
```

这章开始从“ANN 算法”进入“数据库”。

---

## 1. 一个典型 Vector Record

```text
id:            chunk_9871
vector:        [0.12, -0.33, ...]
tenant_id:     42
doc_id:        doc_1001
chunk_index:   8
language:      zh
kb_id:         kb_7
version:       v3
created_at:    ...
```

Vector Search 只对 `vector` 做近邻搜索，但业务查询还需要其余字段。

---

# 2. Collection / Table 是什么

不同产品叫法不同：

```text
Collection
Index
Table
Namespace
```

但可以先抽象成：

> **一组共享 Vector Dimension、Metric、Schema 和 Index Policy 的记录集合。**

同一个 Collection 中最好不要混入互不兼容的：

```text
Embedding Model
Dimension
Metric
Normalization Policy
```

否则生命周期会非常混乱。

---

# 3. Primary Key 为什么重要

Vector Record 也需要稳定身份。

Primary Key 用于：

```text
Upsert
Delete
Dedup
Version Replacement
Source Mapping
```

例如：

```text
chunk_id = doc_id + content_version + chunk_index
```

或者使用稳定 UUID / Business ID。

关键不是格式，而是：

> **能不能准确找到“这一条向量对应的业务实体”。**

---

# 4. Metadata 是什么

Metadata 是不参与 Dense Distance 本身、但用于过滤、展示、路由和治理的结构化字段。

例如：

```text
tenant_id
user_id
doc_id
kb_id
language
source_type
permission_group
content_version
embedding_version
deleted
created_at
```

Metadata 不是“随便塞一点 JSON”。

它决定后续：

```text
Filter
Tenant Isolation
Version Governance
Incremental Update
Deletion
Audit
```

---

# 5. Vector DB 里要不要存原文

常见有三种思路。

## 5.1 只存 Vector + ID

原文回 MySQL / Object Store 取。

优点：

```text
Vector Store 更轻
Source of Truth 清晰
```

缺点：

```text
需要二次读取
```

## 5.2 Vector + Chunk Text 一起存

优点：

```text
Query 结果直接可用
减少一次 Hop
```

缺点：

```text
数据重复
版本同步更复杂
```

## 5.3 存一部分 Retrieval Metadata

折中方案。

没有统一答案，取决于：

```text
数据规模
延迟
Source of Truth
更新频率
产品限制
```

---

# 6. 为什么不要把 Vector DB 当唯一 Source of Truth

很多 Vector Index 都可以重建：

```text
Document Source
→ Chunk
→ Embedding
→ Vector Index
```

因此在很多系统里：

```text
MySQL / Object Storage
= Source of Truth

Vector DB
= Derived Retrieval Index
```

这会让：

```text
Index Corruption
Embedding Upgrade
Rebuild
```

更容易处理。

但某些产品也可以承载更完整的主数据，是否这么设计属于 System Design。

---

# 7. Schema 怎样围绕 Query Pattern 设计

不要先列字段，再问怎么查。

先列真实 Query：

```text
Q1: tenant=42, kb=7, current_version, semantic search
Q2: user can access these permission groups
Q3: only language=zh
Q4: delete all chunks of doc_1001
Q5: rebuild model_version=v2
```

再决定：

```text
哪些字段必须 Metadata Index
哪些字段适合 Partition
哪些字段只用于返回
```

这和关系数据库“从访问模式设计索引”的思想是相通的。

---

# 8. Version 字段为什么是一等公民

知识库不是静态的。

你可能有：

```text
Document Version
Chunking Version
Embedding Model Version
Index Version
```

如果不显式版本化：

```text
旧向量和新向量混搜
旧 Chunk 未删除
回滚困难
```

所以至少要能回答：

> 这条向量是由哪一版 Source、Chunk 策略和 Embedding 生成的？

---

# 9. 面试怎么答

## Q：Vector DB 的 Schema 应该怎么设计？

🎯 **建议回答**：

> 我会先固定向量契约，例如 dimension、metric、embedding version，再从实际 Query Pattern 设计 Primary Key 和 Metadata。常见字段包括 tenant_id、doc_id、chunk_id、kb_id、permission、content_version、embedding_version 等。Primary Key 必须支持 Upsert/Delete 和 Source Mapping；Version 字段要支持 re-embedding 和 rebuild。Vector DB 在很多 RAG 系统里更适合作为可重建的 Retrieval Index，而不是唯一 Source of Truth。

---

# 10. 高频易错点

⚠️ **Vector DB 只需要 id + vector。** Production 通常远远不够。

⚠️ **Metadata 全塞 JSON 就行。** Filter / Index / Partition 能力取决于产品和字段建模。

⚠️ **向量索引就是业务 Source of Truth。** 很多系统里它是 Derived Index。

---

# 11. 本章自测

<details><summary>1. 为什么 Primary Key 对 Vector DB 也很重要？</summary>

因为 Upsert、Delete、Dedup、版本替换和 Source Mapping 都依赖稳定身份。
</details>

<details><summary>2. 为什么 embedding_version 应该进入 Metadata / Schema？</summary>

因为模型升级后需要识别旧向量、控制混搜、增量重建、灰度切换和回滚。
</details>