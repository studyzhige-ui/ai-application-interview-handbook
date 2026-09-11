# 17｜Enterprise / Large-scale RAG System Design

这一章不是重新讲 Chunk / Hybrid / Rerank，而是回答：

> **企业知识问答从 Source 到 Evidence 到答案，怎样同时满足权限、Freshness、规模、成本、可评估和可回滚。**

对应真人 Scenario：

```text
SD-016 Enterprise Knowledge-base QA
SD-017 600GB–1TB PDF / Scan Vertical RAG
```

---

## 1. 先定义 Scope

企业 RAG 不是“上传文件后问问题”这么简单。

先问：

```text
Source 有哪些？
PDF / Wiki / DB / Ticket / Email？
更新频率？
权限模型？
Corpus 多大？
答案需要 Citation 吗？
允许旧多久？
是否多语言 / 多模态？
```

这些问题直接决定架构。

---

# 2. Offline / Online 两条主线

```text
Offline
Source
→ Audit
→ Parse / OCR
→ Clean / Chunk
→ Embed / Sparse Index
→ Validate
→ Activate Generation

Online
Query
→ Permission / Rewrite
→ Dense + Sparse
→ Fusion / Rerank
→ Context / Citation
→ LLM
→ Answer
```

横向：

```text
Version
Trace
Evaluation
Cost
Freshness
```

---

# 3. Source of Truth 与 Retrieval Index

企业知识常来自：

```text
Document System
Wiki
Object Storage
Business DB
```

这些才是 Source of Truth。

Vector / Search Index 是：

```text
Derived Retrieval State
```

这样 Embedding / Chunk / Index 升级时才能安全 Rebuild。

---

# 4. 600GB–1TB Corpus 首先是 Data Pipeline 问题

不能：

```text
一个进程
→ 读所有 PDF
→ 调 Embedding
```

需要：

```text
Source Partition
→ Durable Ingestion Job
→ Parse Worker
→ Chunk Worker
→ Embedding Batch
→ Index Writer
→ Validation
```

每阶段：

```text
checkpoint
idempotency
retry
backpressure
rate limit
```

---

# 5. OCR / Parsing 是第一大 Failure Source

扫描 PDF：

```text
Image
→ OCR
→ Layout / Table
```

电子 PDF：

```text
Text layer
→ parser
```

最终最好统一成：

```text
Document Model
├─ page
├─ block
├─ text
├─ table
├─ image
└─ lineage
```

这样后续 Chunk 和 Citation 才可追溯。

---

# 6. Permission 必须进入 Retrieval

错误：

```text
retrieve global topK
→ answer
→ UI hide forbidden source
```

正确方向：

```text
user / group / tenant auth
→ permission filter / namespace
→ retrieval
```

并让 Chunk 继承 Source ACL。

Permission 变化也要触发索引/缓存失效。

---

# 7. Large-scale Index 的版本策略

Embedding 或 Chunk 升级时，不推荐在线原地混改：

```text
Generation V1 serving
↓
build V2 offline
↓
catch delta
↓
quality / count / permission validation
↓
canary V2
↓
switch
↓
keep V1 rollback window
```

这是大规模 RAG 稳定演进的核心。

---

# 8. Incremental Update

如果每次文档变化都全量 Rebuild：

```text
成本高
Freshness 差
```

所以维护：

```text
document_id
source_version
content_hash
parse_version
chunk_version
embedding_version
```

只处理受影响文档。

但大版本升级仍可能需要 Full Rebuild。

---

# 9. Online Retrieval Path

典型：

```text
Query
→ classify / rewrite
→ permission scope
→ dense + BM25
→ fusion
→ candidate budget
→ rerank
→ context build
→ generate
```

每一步都要有：

```text
latency budget
trace
fallback
```

例如 Reranker 超时：

```text
can fallback to fusion ranking
```

而不是整条请求 500。

---

# 10. No-hit / Insufficient Evidence

Enterprise 场景最危险是：

```text
没证据
→ 模型仍给出确定答案
```

需要：

```text
retrieval confidence
coverage
citation support
business risk
```

决定：

```text
answer
clarify
fallback to tool
human handoff
refuse
```

---

# 11. Citation 不是 UI 装饰

最终 Claim 应能追：

```text
answer span
→ context chunk
→ document version
→ source
```

否则：

- 无法审计；
- 权限变化难处理；
- Bad Case 无法回放；
- 文档更新后 Citation 可能悬空。

---

# 12. Evaluation 架构

必须分层：

```text
Parsing Quality
Chunk Coverage
Retrieval Recall / NDCG
Rerank
Faithfulness
Answer Correctness
Citation
Latency
Cost
```

如果 End-to-end 变差，只看一个总分无法定位。

---

# 13. Evaluation Dataset 从哪里来

可以结合：

```text
production queries
support tickets
expert questions
known bad cases
edge cases
permission cases
freshness cases
```

并固定：

```text
ground truth / evidence
expected refusal
permission scope
```

LLM Judge 可以辅助，但不能是唯一真相。

---

# 14. Cost Model

Offline：

```text
OCR
Embedding
Index Build
Storage
Rebuild
```

Online：

```text
Rewrite
Retrieval
Rerank
LLM input/output
```

1TB Corpus 如果频繁全量 Re-embed，成本会非常可观。

因此 Version / Incremental Update 本身就是成本架构。

---

# 15. Cache

可以缓存：

```text
parsed document
embedding
retrieval result
rerank result
answer
```

但在线 Cache Key 至少考虑：

```text
query
index generation
permission scope
model / prompt version
```

否则容易陈旧或越权。

---

# 16. Observability

每个 Query Trace：

```text
raw query
rewrite
permission filter
candidate ids/scores
fusion rank
rerank score
context ids
index generation
answer / citation
stage latency
cost
```

离线：

```text
parse failure
embedding throughput
queue age
freshness lag
index activation status
```

---

# 17. Failure Walkthrough

## Embedding Provider 429

→ ingestion backpressure，不要无限 retry。

## New Generation 构建一半失败

→ V1 继续 serving；V2 durable resume。

## ACL 改了

→ Derived Chunk / Cache 必须失效或重新授权。

## Rerank down

→ fallback to fused retrieval if acceptable。

## Vector DB partial shard failure

→ retry / degrade / mark incomplete，不能悄悄假装完整答案。

---

# 18. 真人面经影响

Enterprise RAG 有 6 个独立来源，大规模 600GB–1TB RAG 虽是单点信号，但把很多 Production 追问集中在同一题：

```text
Parsing
Embedding Cost
Index Scale
Hybrid
Incremental Update
```

因此本章专门把“规模与运营”做成系统设计闭环，而不是重复 RAG 算法定义。

---

# 19. 🎯 面试怎么答

> 企业 RAG 我会拆 Offline Ingestion 和 Online Query 两条链。Source 是权威数据，Index 是可重建派生物；文档带稳定 ID、Version、Lineage 和 ACL。大规模语料用分阶段 Durable Pipeline + Backpressure，Embedding/Chunk 升级构建新 Generation，通过 Delta Catch-up、Evaluation、Canary 后切换。在线 Query 在 Permission Scope 内做 Hybrid/Rerank，并对 No-hit、Rerank Failure、Partial Index 明确 Fallback。最终用 Retrieval Trace、分层 Eval、Freshness 和 Cost 证明系统可运营。

---

# 20. 本章自测

<details><summary>1. 为什么大规模 RAG 应构建新 Index Generation，而不是原地全量覆盖？</summary>
可以让旧版本持续服务，新版本独立构建和验证，并提供可控 Cutover 与 Rollback。
</details>

<details><summary>2. 为什么 Permission 必须进入 Retriever？</summary>
如果先召回受限内容再过滤，内容可能已经进入模型 Context，形成真实数据泄漏。
</details>

<details><summary>3. 为什么只看 Answer Correctness 不够定位 RAG Bad Case？</summary>
错误可能来自 Parsing、Chunk、Retrieval、Rerank、Context 或 Generation，需要分层指标和 Trace 才能归因。
</details>
