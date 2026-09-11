# 13｜Large-scale Ingestion、Latency / Cost、Cache 与 Observability

> Demo RAG 回答“能不能搜到”；Production RAG 还必须回答：**数据怎样持续进来、重建时怎样不停服、每个阶段能承受多少吞吐、成本花在哪、P99 为什么变坏、Bad Case 能不能重放。**

这一章把规模、可靠性、成本和可观测性放在一起，因为它们在生产环境中是同一条运行链。

---

## 1. 从 Demo 到 Production，问题发生了什么变化

Demo 常见：

```text
几百个文档
一次性 ingest
单用户
无权限
单版本 Index
```

Production 可能变成：

```text
100 GB / TB Corpus
持续更新
多 Tenant / ACL
多个 Embedding / Chunk Version
在线 Query 不允许停
每天都有失败 Ingestion
峰值流量明显
```

此时系统必须同时处理：

```text
Throughput
Backpressure
Idempotency
Freshness
Version Switch
Latency SLO
Cost Budget
Trace / Replay
Quality Monitoring
```

---

## 2. Ingestion 应该是可恢复 Pipeline，不是一段 for-loop

典型链路：

```text
Source Discovery
→ Snapshot / Change Detection
→ Download / Read
→ Parse / OCR
→ Clean / Dedup
→ Chunk
→ Embed
→ Index Write
→ Validate
→ Activate Generation
```

每一个阶段都可能：

```text
timeout
429
parser crash
OOM
partial batch failure
duplicate retry
worker restart
```

因此每个阶段最好有稳定任务身份：

```text
job_id
document_id
source_version
processing_version
stage
attempt
status
artifact_ref
```

这样 Worker Crash 后才能回答：

> “这一份文档到底处理到哪一步？”

---

## 3. Idempotency 要围绕“输入版本 + 处理版本”设计

简单：

```text
retry parse(document)
```

如果每次都产生新的随机 Chunk / Vector ID：

```text
重复执行
→ 重复 Chunk
→ 重复 Vector
→ Retrieval 污染
```

更稳定的键可以来自：

```text
document_id
+ source_version
+ parser_version
+ chunker_version
+ embedding_version
```

输出也要可定位：

```text
same logical input
→ same generation / replaceable artifact set
```

这和前面的 Corpus Lineage 是同一条 Production 设计。

---

## 4. Backpressure：为什么“加并发”经常让 Ingestion 更慢

不同阶段的瓶颈不同：

```text
OCR           → CPU / GPU
Embedding API → RPM / TPM / Provider Queue
Vector DB     → write throughput / compaction
Object Store  → bandwidth
Parser        → memory
```

如果上游无限生产：

```text
Discover 100k docs
→ 100k OCR tasks
→ 100k embedding calls
→ provider 429
→ retries
→ larger queue
→ retry storm
```

正确思路是：

```text
bounded queue
+ per-stage concurrency
+ provider quota
+ retry budget
+ queue lag metrics
```

而不是一条全局 `max_workers=1000`。

---

## 5. Ingestion State Machine

可以把文档处理显式成状态：

```text
DISCOVERED
→ FETCHED
→ PARSED
→ CHUNKED
→ EMBEDDED
→ INDEXED
→ VALIDATED
→ ACTIVE
```

失败：

```text
RETRYABLE_FAILED
FATAL_FAILED
QUARANTINED
```

这样才能做：

- 分阶段重试；
- 对账；
- Dead-letter；
- 运营面板；
- 自动重跑某一处理版本；
- 判断 Freshness Lag 在哪一层。

---

## 6. 大规模 Rebuild 怎样不停服

错误做法：

```text
删除旧 Index
→ 重建几小时
→ 用户等待
```

更常见的 Generation / Snapshot 思路：

```text
Generation A  ← current traffic

后台：
Source Snapshot
→ Build Generation B
→ Validate B
→ Catch up delta
→ Atomic / controlled switch A → B
→ Observe
→ Retire A later
```

这样同时得到：

```text
No-downtime rebuild
Rollback point
A/B comparison
Version traceability
```

关键是定义切换边界：

> Query 一次请求应该看到一个一致的 Corpus / Index Generation，而不是一半旧、一半新。

---

## 7. Delta Catch-up 为什么需要

如果 Generation B 构建 3 小时：

```text
T0 snapshot
→ build 3h
→ T3 ready
```

期间 Source 仍然发生：

```text
create / update / delete
```

如果直接切换 B：

```text
T0–T3 的变化丢失
```

所以需要：

```text
snapshot boundary
+ change log / CDC / incremental queue
→ catch up delta
→ switch
```

具体 CDC 机制属于 Backend / Data Engineering，但 RAG 必须明确知识版本正确性。

---

## 8. 在线 Query Latency 必须按 Stage 拆

端到端：

```text
API Queue
→ Query Rewrite
→ Dense / Sparse Retrieval
→ Fusion
→ Rerank
→ Context Build
→ LLM Prefill / TTFT
→ Decode
```

只监控：

```text
/api/chat P95 = 4.2s
```

几乎不能定位问题。

至少要能得到：

| Stage | 指标例子 |
|---|---|
| Rewrite | latency / model / fallback |
| Dense Retrieval | latency / candidate count |
| Sparse | latency / no-hit |
| Rerank | latency / candidates in/out |
| Context | tokens / chunk count |
| LLM | TTFT / output tokens / total latency |

---

## 9. Tail Latency 比平均值更重要

假设：

```text
Retrieval P50 = 30ms
Retrieval P99 = 1.5s
```

平均值看起来很好，真实用户却经常遇到卡顿。

常见 P99 来源：

- Hot Shard；
- Vector DB compaction；
- Cold Cache；
- Rerank batch queue；
- Provider congestion；
- 大 Context；
- 极端 Filter；
- 多路 Retrieval 某一路慢。

所以 Production 优化不只问“平均快不快”，还要问：

> **谁在拖慢最慢的那 1%？**

---

## 10. SLO 应该和用户体验对应

可以拆：

```text
Retrieval SLO
Rerank SLO
TTFT SLO
End-to-end SLO
Freshness SLO
```

例如企业知识库可能关心：

```text
P95 TTFT
P99 Retrieval
Index freshness < 10 min
Citation coverage
```

SLO 不是指标列表，而是：

> 超过什么边界就算系统没有履行承诺。

---

## 11. 成本要分 Offline 和 Online

### Offline / Ingestion

```text
OCR
Parsing
Embedding
Index Build
Vector Storage
Replica
Rebuild
```

### Online

```text
Query Rewrite Model
Dense / Sparse Retrieval
Reranker
LLM Input Tokens
LLM Output Tokens
Tool / Graph retrieval
```

可以统一成：

```text
cost_per_ingested_document
cost_per_1k_chunks
cost_per_query
cost_per_successful_answer
```

最后一个尤其重要：

> 便宜但答错，不是真正低成本。

---

## 12. Candidate Budget 是成本控制点

比如：

```text
Dense Top50
Sparse Top50
→ Fusion 70
→ Rerank 40
→ Context 6
```

每扩大一层都会增加：

```text
retrieval compute
rerank cost
context tokens
LLM prefill
```

因此 Top-K 不是纯质量参数，也属于成本预算。

真正优化应画：

```text
Quality
vs Latency
vs Cost
```

Pareto Curve，而不是单独追最高 Recall。

---

## 13. Cache 可以放在哪里

### Embedding Cache

Key 至少考虑：

```text
content hash
+ embedding model/version
+ preprocessing version
```

### Retrieval Cache

必须考虑：

```text
normalized query
+ index generation
+ filter
+ permission scope
+ retrieval config
```

否则旧 Generation / 其它权限域的结果可能被错误复用。

### Rerank Cache

可以基于：

```text
query
+ candidate ids/version
+ reranker version
```

### Answer Cache

风险最高，因为答案还依赖：

```text
Knowledge Version
Permission
Prompt
Model
Conversation Context
Tool State
```

所以不是“相同问题就复用答案”。

---

## 14. Cache Invalidation 应该跟 Version 走

Production 最容易维护的思路通常不是逐条猜哪些 Cache 失效，而是：

```text
Index Generation changes
→ old retrieval cache namespace becomes unreachable
```

类似：

```text
cache key includes generation_id
```

这样 Rollback 时也可以回到旧命名空间。

---

## 15. Production Trace 要保存什么

一条 Query 最少希望重建：

```text
request_id
user / tenant / permission scope
raw query
rewritten / decomposed query
filters
retrieval route
candidate ids + scores
fusion rank
rerank score
final context ids
corpus/index generation
prompt version
model version
answer
citations
stage latency
stage cost
```

这不是为了日志好看，而是为了：

```text
Bad Case Replay
Latency Attribution
Cost Attribution
Security Audit
Regression Dataset
```

---

## 16. Trace 和 Log 不一样

普通 Log：

```text
retrieval succeeded
```

对于 RAG 几乎没法 Debug。

Trace 应该表现因果链：

```text
Query
→ Rewrite
→ Candidate Set
→ Rerank
→ Final Context
→ Generation
```

并保留关键 Artifact ID，而不是把整份原文复制进日志导致隐私和存储问题。

---

## 17. Quality Monitoring 不能只靠线上用户投诉

在线可以持续采样：

```text
no-hit rate
candidate count
citation coverage
context utilization
retrieval score distribution
rerank score distribution
refusal rate
user correction / regeneration
```

再把样本进入：

```text
human review / judge
→ labeled bad case
→ regression set
```

注意：这些 Online Proxy 不等于最终质量，仍要配合离线 Ground Truth。

---

## 18. Freshness Observability 是 RAG 特有核心指标

要区分：

```text
Source Updated At
Ingestion Detected At
Indexed At
Activated At
```

于是可以计算：

```text
source_to_active_lag
```

如果用户问“为什么新政策还搜不到”，你应该能明确知道：

```text
Source 没同步？
Parser 队列堵？
Embedding 429？
Index Write 延迟？
Generation 还没切？
```

---

## 19. Degradation / Load Shedding

系统超载时不要只等超时。

可以有受控降级：

```text
skip expensive query rewrite
reduce rerank candidate count
use smaller reranker
reduce multi-query branches
shorten context
fallback to sparse/dense single route
refuse noncritical expensive mode
```

但必须评估：

> 降级后质量下降到什么程度？哪些用户/请求允许？

Degradation Policy 应成为可测试配置，而不是事故时临时写 if。

---

## 20. 三个典型 Failure Timeline

### 20.1 Embedding Provider 429

```text
queue grows
→ retry immediately
→ more 429
→ retry storm
```

正确方向：

```text
rate-aware concurrency
+ exponential backoff / jitter
+ queue limit
+ failure state
```

### 20.2 Rebuild 切换后质量暴跌

```text
Generation B active
→ no-hit ↑
→ citation ↓
```

需要：

```text
versioned trace
→ compare A/B
→ rollback alias to A
```

### 20.3 Vector DB P99 抖动

不能立刻“换数据库”。先定位：

```text
filter selectivity
hot shard
compaction
candidate size
network
cache
```

再决定索引 / 容量 / 路由优化。

---

## 21. 🎯 30 秒回答

> 大规模 RAG 我会把 Ingestion 做成可恢复、幂等、带版本的异步状态机，并对 OCR、Embedding、Index Write 分别做并发控制和 Backpressure。Rebuild 用新 Generation 后台构建、校验、追 Delta，再原子切换，避免停服。在线请求按 Rewrite、Retrieval、Rerank、Context、LLM 拆 Stage latency / cost，并保留候选、分数、版本和最终 Context 的 Trace。Cache Key 必须包含 Knowledge Version 和 Permission Scope。除了 P95/P99，还要监控 Freshness Lag、No-hit、Citation、Queue Lag 和 Cost/Query，才能真正定位质量、延迟和成本问题。

---

## 22. ⚠️ 易错点

- **“加线程就能提升 Ingestion。”** 上游并发可能放大下游 429 / OOM。
- **“重建索引要先删旧索引。”** Production 更适合 Generation / Snapshot 切换。
- **“只看接口总耗时。”** 无法做 Stage Attribution。
- **“Answer Cache 只按 Query 做 Key。”** 会产生版本和权限错误。
- **“P50 很低说明性能很好。”** P99 可能已经不可用。
- **“Online score 高就等于回答质量高。”** Proxy 不能替代 Ground Truth Eval。

---

## 23. 🔍 深挖追问

```text
TB 级语料重建怎样不中断 Query？
Snapshot 构建期间新数据怎样 Catch-up？
Embedding Provider 限流怎样做 Backpressure？
如何制定 Retrieval / TTFT / Freshness SLO？
哪些 Cache 最安全？
怎样定位 P99 而不是平均延迟？
如何从 Production Trace 自动回流 Regression Dataset？
```

---

<details>
<summary>自测 1：为什么新 Generation 构建完成后不能直接切流量？</summary>

因为构建期间 Source 可能继续变化。需要验证新 Generation，并补齐 Snapshot 之后的 Delta；否则切换后会丢失这段时间的新增、更新或删除。
</details>

<details>
<summary>自测 2：为什么 Retrieval Cache Key 必须包含 Permission Scope 和 Index Generation？</summary>

否则不同权限用户可能共享不该看到的候选，或者新知识版本仍命中旧索引结果，造成安全和 Freshness 错误。
</details>

<details>
<summary>自测 3：为什么 Retrieval Trace 是 Production RAG 的核心基础设施？</summary>

因为最终回答由 Query 处理、候选召回、Fusion、Rerank、Context 和 Generation 多阶段共同决定。只有保留每层的输入、输出、版本与延迟，才能复现 Bad Case 并进行质量、成本和延迟归因。
</details>
