# 31｜Freshness、Incremental Update、Version、Snapshot 与 Rollback

## 1. 先讲人话

知识库不是建完一次就不变。

真实系统会持续发生：

```text
新增文档
修改文档
删除文档
权限变化
Embedding 模型升级
Parser / Chunker 升级
```

所以 Production RAG 必须解决：

> **如何让索引持续代表“当前有效知识”，同时还能回滚和复现历史。**

---

## 2. Incremental Update

理想路径不是每改一页就全库重建，而是：

```text
Detect Change
→ Identify Document
→ Parse New Version
→ Chunk
→ Diff / Delete Old Chunks
→ Embed New Chunks
→ Update Index
→ Mark Version Active
```

关键依赖前面已经学过的：

- stable document_id；
- chunk_id；
- version；
- content_hash；
- lineage。

---

## 3. Change Detection

常见手段：

- 文件更新时间；
- Content Hash；
- CDC / Event；
- Webhook；
- 定时扫描；
- Source API Version。

不能只依赖“文件名没变”，因为内容可能已修改。

---

## 4. Delete 是核心能力

文档删除 / 权限撤销后，旧 Chunk 不能继续被召回。

要处理：

```text
Metadata Store
Vector Index
Sparse Index
Cache
Parent-child Relation
```

多个系统更新不同步会出现“幽灵知识”。

---

## 5. Version / Snapshot

建议把一次可用知识状态定义为 Snapshot：

```text
corpus_version
parser_version
chunker_version
embedding_version
index_version
```

这样可以：

- 重现 Bad Case；
- 比较实验；
- 蓝绿切换；
- 快速 Rollback。

---

## 6. Blue-Green Index

大规模 Embedding / Chunk 策略升级时，常见做法：

```text
Current Index A serving
        ↓
Build New Index B offline
        ↓
Evaluate B
        ↓
Switch Traffic A → B
        ↓
Keep A for rollback window
```

比原地覆盖更安全。

---

## 7. Freshness SLO

不同业务需要不同目标：

```text
政策知识：小时级
新闻：分钟级
代码仓库：提交级
静态手册：天级
```

先定义 Freshness Requirement，再设计 Ingestion 架构。

---

## 8. Consistency Window

更新过程可能出现：

```text
MySQL metadata 已是 v2
Vector DB 仍有 v1
Cache 仍缓存旧答案
```

因此要明确：

- 切换顺序；
- Active Version；
- Cache Key 是否带 Version；
- 失败补偿；
- Reconciliation Job。

完整跨系统可靠性会在 Backend/System Design 中继续深化。

---

## 9. 🎯 面试怎么回答

> Production RAG 需要稳定 Document/Chunk Identity 支持增量更新。更新流程通常检测 Source Change，只重建受影响文档，并同步删除旧 Chunk。对于 Parser、Chunker、Embedding 的大版本升级，更适合构建新 Index 做 Evaluation 后 Blue-Green 切换。整个 Corpus/Index 需要 Version/Snapshot，才能支持 Bad Case Replay、Rollback 和 Freshness SLO。

## 10. ⚠️ 易错点

- 新版本写入后旧 Chunk 不删除；
- Embedding Model 原地混写；
- Cache 不带知识版本；
- 没有 Snapshot，实验不可复现。

## 11. 🔍 继续追问

- 文档更新时如何精确删除旧 Chunk？
- 多索引切换如何避免短暂混用？
- Freshness SLO 如何监控？

<details><summary>查看参考答案：为什么大版本升级推荐 Blue-Green Index？</summary>

因为新旧向量空间或 Chunk 结构可能不兼容。先离线构建和评测新版本，再原子切流，可以避免半新半旧状态，并保留快速回滚路径。

</details>
