# 33｜Large-scale Ingestion、Latency / Cost、Cache 与 Observability

## 1. 先讲人话

Demo RAG 可能只有几百份文档；Production RAG 可能是百 GB、TB 级语料，并且持续更新。

规模上来以后，问题会从：

> “怎么检索？”

变成：

> “怎么可靠地摄取、重建、并发处理、控制成本，而且出错时知道坏在哪？”

---

## 2. Ingestion Pipeline

大规模 Ingestion 通常拆成异步阶段：

```text
Source Discovery
→ Download / Read
→ Parse / OCR
→ Clean
→ Chunk
→ Embed
→ Index Write
→ Validation
→ Activate Version
```

每个阶段都可能：

- 超时；
- 重试；
- 部分失败；
- 重复执行。

因此需要 Idempotency、Checkpoint、Retry 和 Dead-letter / Failure Queue。完整后端机制属于 AI Backend Engineering，这里关注它们在 RAG Pipeline 中的应用。

---

## 3. 并行不是越多越快

瓶颈可能在：

```text
OCR CPU/GPU
Embedding API Rate Limit
Vector DB Write Throughput
Object Storage Bandwidth
Parser Memory
```

盲目提高并发会导致：

- 429；
- OOM；
- Queue Backlog；
- 写入抖动；
- 成本失控。

所以要做阶段级 Backpressure。

---

## 4. 在线 Query Latency 分解

```text
Query Rewrite
+ Dense/Sparse Retrieval
+ Fusion
+ Rerank
+ Context Build
+ LLM TTFT / Decode
```

不要只看总 P95。必须知道每个阶段的耗时。

---

## 5. 成本分解

### Offline / Ingestion Cost

- OCR；
- Embedding；
- Index Build；
- Storage；
- Rebuild。

### Online Cost

- Query Rewrite Model；
- Retrieval；
- Reranker；
- LLM Input Token；
- LLM Output Token。

优化必须知道成本主要花在哪里。

---

## 6. Cache 可以放在哪里

### Embedding Cache

相同文本避免重复 Embedding。

### Retrieval Cache

相同 Query + Index Version + Permission Scope 可复用候选。

### Rerank Cache

Query + Candidate Set 稳定时可缓存。

### Answer Cache

风险最高，因为答案受：

- Knowledge Version；
- Permission；
- Model；
- Prompt；
- User Context

共同影响。

因此 Cache Key 和 Invalidation 必须非常明确。

---

## 7. Production Trace

每次 Query 建议保存：

```text
request_id
raw / rewritten query
filters
retrieval route
candidate ids + scores
fusion ranks
rerank scores
final context ids
corpus/index version
prompt/model version
answer/citations
stage latency
cost
```

这样才能做：

- Bad Case Replay；
- Latency Attribution；
- Cost Attribution；
- Regression Dataset 回流。

---

## 8. 核心 Observability

### Ingestion

- documents processed / failed；
- parse failure rate；
- embedding throughput；
- queue lag；
- index freshness lag。

### Online

- QPS；
- P50/P95/P99 stage latency；
- no-hit rate；
- rerank latency；
- context token；
- answer token；
- cost/query；
- retrieval quality sample。

---

## 9. 🎯 面试怎么回答

> 大规模 RAG 要把 Ingestion 拆成可重试、幂等、可 Checkpoint 的异步阶段，并对 OCR、Embedding、Index Write 等瓶颈做 Backpressure。在线请求要拆分 Query Rewrite、Retrieval、Rerank、Context 和 LLM 各阶段延迟与成本。Cache 必须带 Knowledge Version 和 Permission Scope。最关键的是保留完整 Retrieval Trace，才能做 Bad Case、Latency、Cost 和 Regression Attribution。

## 10. ⚠️ 易错点

- “加线程就能提高 Ingestion”；
- 只监控总接口耗时；
- Answer Cache 不带 Version / Permission；
- Index Freshness 没有指标。

## 11. 🔍 继续追问

- TB 级语料重建时怎样不中断查询？
- Embedding API 限流如何做 Backpressure？
- 哪些 Cache 最安全、收益最大？

<details><summary>查看参考答案：为什么 Retrieval Trace 是 Production RAG 的核心基础设施？</summary>

因为 RAG 的输出由多个阶段共同决定。没有 Query、候选、分数、版本和最终 Context 的完整轨迹，就无法复现 Bad Case，也无法知道延迟、成本或质量退化发生在哪一层。

</details>
