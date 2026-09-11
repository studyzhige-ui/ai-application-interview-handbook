# 03. Corpus Governance：Audit、Identity、Lineage、Version 与 Source of Truth

RAG 的第一份数据工程任务不是 Embedding，而是回答：

> **我们到底在检索哪些知识，它们来自哪里、哪个版本、是否重复、是否仍然有效？**

如果 Corpus 本身混乱，后面的 ANN、Rerank 和 Prompt 都只是在优化脏数据。

---

## 1. Corpus Audit 先回答什么

在设计 Retrieval 前先盘点：

```text
有哪些 Source？
文件格式是什么？
更新频率多高？
是否有重复/历史版本？
是否有权限域？
文档是否包含表格/图片/OCR？
谁是 Source of Truth？
需要多快同步？
删除/撤权如何传播？
```

这会直接决定 Parsing、Chunk、Index、Freshness 和权限架构。

---

## 2. Source of Truth 和 Retrieval Index 要分开

推荐：

```text
Authoritative Source
→ Ingestion Snapshot
→ Parsed Document
→ Chunk
→ Index
```

Index 是服务检索的派生数据，不应失去重建能力。

当 Embedding / Chunk / Schema 改变时：

```text
rebuild from source
```

比“在旧索引上打补丁”更可控。

---

## 3. Document Identity 为什么重要

每个文档需要稳定 ID：

```text
document_id
```

不要只使用随机 Vector ID。

稳定 ID 支撑：

- Update；
- Delete；
- Citation；
- Version；
- Dedup；
- Bad Case Replay；
- Permission；
- Rollback。

---

## 4. Version 要表达什么

一个文档可能经历：

```text
v1 → v2 → v3
```

需要区分：

```text
source version
content version
parse version
chunk version
embedding version
index generation
```

这些版本不是一定都要独立字段，但系统必须能回答：

> 当前检索结果来自哪一代数据处理链？

---

## 5. Lineage 是什么

Lineage 是从最终 Evidence 追溯到原始来源的链：

```text
chunk_id
→ parsed element
→ document version
→ source URI / record
```

回答 Citation、删除、权限和调试时都需要它。

---

## 6. 为什么 Chunk ID 也要稳定

如果每次 Rebuild 都给所有 Chunk 完全随机 ID：

- Diff 很难；
- Regression 难比较；
- Citation 历史失效；
- 增量更新难判断；
- Cache 难复用。

可以基于：

```text
document_id + version + logical position / content hash
```

建立稳定可追溯 ID。

---

## 7. Duplicate 与 Version Duplicate 不一样

常见重复：

```text
同一 PDF 上传两次
网页正文和打印版
同一政策多个历史版本
模板页大量重复 Boilerplate
```

要区分：

```text
Exact Duplicate
Near Duplicate
Historical Version
Legitimate Similar Document
```

如果把历史版本简单 Dedup 删除，可能失去审计能力；如果全混在一起，Retrieval 会返回多个互相冲突版本。

---

## 8. Corpus Freshness 要定义 SLA

不同知识更新要求不同：

```text
产品文档 → 小时级
公司制度 → 日级
用户订单 → 秒级甚至 Tool/DB 查询
```

不是所有数据都适合批量 RAG Index。

如果 Freshness 要求极高，直接查询业务 DB / API 可能比异步 Embedding 更合理。

---

## 9. Permission 是 Corpus Contract 的一部分

在入库时就应知道：

```text
tenant_id
owner
acl / group
classification
region
```

不要到 Query 最后一步才“想起来过滤”。

权限信息如果不随 Chunk 传播，会造成：

```text
Source protected
but derived chunk loses ACL
```

这是严重安全事故。

---

## 10. Delete / Right-to-be-forgotten

删除文档不仅是删 Vector：

```text
Source
Parsed Artifact
Chunk
Embedding / Sparse Index
Cache
Replica
Old Generation
Trace / Backup（按政策）
```

都要有生命周期策略。

逻辑不可检索和物理回收也可能是两个时间点。

---

## 11. Corpus Manifest

Production 可以维护一个 Manifest / Registry：

```text
document_id
source
version
checksum
last_modified
parse_status
chunk_count
embedding_version
index_generation
permission_scope
updated_at
```

它能帮助：

- 增量同步；
- 重建；
- 对账；
- 失败重试；
- Missing Document 检查。

---

## 12. Audit 最终产出什么

在真正写 Retriever 前，最好得到：

```text
Source Inventory
Format Distribution
Document Count / Size
Update Frequency
Permission Model
Duplicate Rate
Failure Samples
Freshness SLA
Rebuild Strategy
```

这份结果决定后面的技术选择。

---

## 13. 常见错误

- 先选 Vector DB，再看数据：顺序反了。
- Vector ID 能替代 Document ID：通常不够。
- Version 只记录一个 updated_at 就够：很多处理层也有版本。
- Dedup 越彻底越好：可能误删合法历史/相似文档。
- 权限可以只在 UI 做：错误，Retrieval 层必须有安全边界。

---

## 14. 面试怎么答

### Q：RAG 知识库怎样做增量更新？

> 我会先给 Source 建稳定 document_id / version 和 Manifest，检测 Source 变化后只重新 Parse/Chunk/Embed 受影响文档，同时保留内容、Embedding 和 Index Generation 的版本；写入新版本后再切换可见性并清理旧版本。大规模 Rebuild 还需要 Snapshot Boundary 和 Delta Catch-up。

### Q：为什么 RAG 需要 Lineage？

> 因为 Citation、权限、删除、Freshness、Bad Case Replay 和 Rollback 都需要从最终 Chunk 追溯到具体原文与版本，没有 Lineage 就无法可靠运营知识库。

---

## 15. 自测

<details><summary>1. Source of Truth 与 Vector Index 最大区别是什么？</summary>
Source of Truth 是权威原始状态，Index 是可重建的检索派生物。
</details>

<details><summary>2. 为什么历史版本不能简单当重复数据删除？</summary>
历史版本可能用于审计/回滚，但在线检索必须通过版本可见性避免新旧冲突。
</details>

<details><summary>3. Permission 为什么应该从 Source 传播到 Chunk？</summary>
因为检索返回的是 Chunk；如果派生数据丢失 ACL，就可能越权召回受保护内容。
</details>
