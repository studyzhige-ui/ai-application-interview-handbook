# 13｜Chunk ID、Metadata、Hierarchy 与可追溯数据模型

## 1. 先讲人话

很多 Demo 只存：

```text
text
embedding
```

但 Production RAG 需要回答更多问题：

- 这个 Chunk 来自哪份文档？
- 是哪个版本？
- 位于哪一章、哪一页？
- 用户有权限看吗？
- 上一块和下一块是谁？
- 旧版本更新后怎么删？
- Citation 怎么回源？

所以 Chunk 不是一段字符串，而是一个带身份、结构和血缘的 Retrieval Entity。

---

## 2. 一个推荐的数据模型

```text
chunk_id
source_id
document_id
document_version
parent_id
section_path
position
text
embedding_version
parser_version
chunker_version
acl / tenant_id
created_at
valid_from / valid_to
source_uri
content_hash
```

字段不一定全部放在 Vector DB，但这些语义必须在系统里可追溯。

---

## 3. 为什么 Chunk ID 必须稳定

如果每次 Re-index 都随机生成完全不同的 ID：

- 很难做增量更新；
- 很难精确删除；
- Bad Case Replay 无法复现；
- Citation 链路不稳定。

可以根据：

```text
document_id + version + section + position / content_hash
```

生成稳定或可解释的 Chunk Identity。

---

## 4. Metadata 的三类用途

### Retrieval Filter

例如：

```text
tenant_id = 42
product = "A"
language = "zh"
valid_at <= now
```

### Context Construction

标题、章节、页码等可以一起送给 LLM，帮助理解 Evidence。

### Operations

用于：

- 删除旧版本；
- 批量重建；
- 统计某个数据源质量；
- Debug 某个 Parser 版本。

---

## 5. Hierarchy

建议显式保存层级：

```text
Document
└── Section
    └── Parent Chunk
        ├── Child Chunk A
        └── Child Chunk B
```

这样 Parent-child Retrieval、Neighbor Expansion、Citation 和 Version Rollback 都容易很多。

---

## 6. Embedding Version 不能忽略

当 Embedding Model 从 v1 换到 v2：

```text
旧向量和新向量
不应该被假设处于同一个空间
```

因此要明确记录：

```text
embedding_model
embedding_version
dimension
metric
index_version
```

迁移时才能做 Blue-Green / Dual Read。

---

## 7. 权限是 Data Model 的一部分

如果企业 RAG 要做 Tenant / ACL：

> 权限不能只在生成答案前检查。

最好让权限 Metadata 在 Retrieval 阶段参与 Filter，避免无权内容进入候选集和 Context。

---

## 8. 🎯 面试怎么回答

> Production RAG 的 Chunk 不能只有 text 和 embedding。至少要有稳定 chunk_id、document_id、version、section/position、source、embedding/parser/chunker version，以及权限相关 metadata。这样才能支持 Parent-child、Citation、增量更新、精确删除、Bad Case Replay 和模型升级。Chunk Data Model 本质上是 Retrieval 的数据契约。

## 9. ⚠️ 易错点

- “Metadata 只是筛选标签”——还承担 Lineage、Debug、Version、Citation。
- “换 Embedding Model 直接覆盖向量”——会失去回滚和比较能力。
- “权限最后判断就行”——无权内容可能已被检索和泄露给模型。

## 10. 🔍 继续追问

- Chunk ID 用随机 UUID 还是内容 Hash？
- Embedding 模型升级怎样做无停机迁移？
- Metadata 放 MySQL 还是 Vector DB？

<details><summary>查看参考答案：Metadata 应全部放 Vector DB 吗？</summary>

不一定。高频 Retrieval Filter 需要靠近检索引擎；复杂业务关系、版本审计或强事务数据可能更适合 MySQL。关键是定义稳定的数据契约和同步关系，而不是强行把所有字段塞进一个系统。

</details>
