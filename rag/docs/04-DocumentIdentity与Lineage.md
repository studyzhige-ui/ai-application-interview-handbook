# 04｜Document Identity、Lineage、Version 与 Source of Truth

## 1. 为什么这是 Production 基础

Demo 常把一个 Chunk 只存：

```text
text
embedding
```

Production 至少还要回答：

> 这个 Chunk 从哪份原始文档、哪个版本、哪一页、哪个 Section 来？

否则你会失去：

- Citation；
- 精确更新 / 删除；
- 权限追踪；
- Bad Case 复现；
- Rollback。

---

## 2. 建议的数据身份层级

```text
Source
  ↓
Document
  ↓
Document Version
  ↓
Section / Element
  ↓
Chunk
```

例如：

```text
source_id     = confluence-space-A
document_id   = employee-handbook
version_id    = 2026-09-01
section_id    = leave-policy
chunk_id      = ...
```

Chunk ID 不应该是唯一保留的信息。

---

## 3. Stable ID 与 Content Hash

可以同时有：

### Stable Business ID

表达“同一份逻辑文档”。

### Version ID

表达“同一文档的某个版本”。

### Content Hash

用于：

- 判断内容是否变化；
- 去重；
- 幂等 Ingestion。

这样增量同步时不必全部重建。

---

## 4. Lineage 是什么

Lineage = 数据血缘。

一条最终 Citation 应该能反向追：

```text
Answer Claim
→ Context Chunk
→ Parsed Element
→ Document Version
→ Original Source
```

这条链是 Grounding 的基础。

---

## 5. Source of Truth

向量库通常不是业务 Source of Truth。

更常见：

```text
Confluence / DB / Object Storage
        ↓
Authoritative Source
        ↓
RAG Derived Index
```

Vector Index 是派生视图。

如果 Index 丢了，应能从源重新构建。

这和数据库里“物化视图 / 搜索索引”的思想很像。

---

## 6. Version 为什么必须显式

如果用户问：

> 当前差旅报销上限是多少？

系统不能同时拿：

```text
2025 policy
2026 policy
```

然后让 LLM 猜哪个新。

应该在 Retrieval / Filter 时就使用：

- effective_at；
- expires_at；
- status；
- version；

排除失效知识。

---

## 7. 删除为什么需要 Lineage

原始 Document 被删除后，要知道删除：

```text
哪些 Chunks
哪些 Embeddings
哪些 Metadata records
哪些 cache entries
```

如果没有 `document_id → chunk_ids` 映射，只能全库扫或留下幽灵数据。

---

## 8. Embedding Version

同一个 Chunk 还应记录：

```text
embedding_model
embedding_version
vector_dimension
index_version
```

因为模型升级后新旧 Vector Space 往往不能直接混用。

---

## 9. Parser / Chunk Version

同一文档也可能因为：

- Parser 修复；
- OCR 升级；
- Chunk Strategy 调整；

产生不同 Chunk。

所以建议记录：

```text
parser_version
chunker_version
```

Bad Case 才能真正重放。

---

## 10. 🎯 面试怎么回答

> Production RAG 我会把 Vector Index 当派生数据，而不是 Source of Truth。Document 要有稳定 document_id、version_id、content hash，Chunk 要保留 source / page / section / parent / parser / chunker / embedding version。这样 Citation 可以回源，增量更新能精确替换旧 Chunk，Embedding 升级能 Blue-Green，Bad Case 也能按历史版本复现。

---

## 11. ⚠️ 易错点

错误：

> Vector DB 里有 text + vector 就够了。

错误：

> 文档更新就直接插一份新的，不需要删旧的。

错误：

> Citation 可以让 LLM 自己生成一个 URL。

Citation 应来自真实 Lineage。

---

<details>
<summary>自测：为什么 Vector Index 更适合被看成“派生视图”？</summary>

因为它可以由原始权威文档经过 Parser、Chunk、Embedding 重新构建；真正需要长期治理的是源数据、版本、权限和血缘，而不是把索引当唯一事实来源。

</details>
