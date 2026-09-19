# 03｜Workload、Capacity、Hotspot 与数量级估算

System Design 不要求你做财务级精确预测，但要求你能判断：

> **这是单机问题、分片问题，还是整个架构层级都要改变的问题？**

这靠数量级估算，而不是凭感觉。

---

## 1. 先把“高并发”翻译成数字

不要说：

> QPS 很高。

要问：

```text
DAU / MAU？
平均 QPS？
Peak / Average Ratio？
Read / Write Ratio？
Payload Size？
Burst Duration？
```

例如：

```text
1 亿 DAU
每人每天 20 次读取
→ 20 亿 reads/day
→ 平均约 23K QPS
→ Peak × 5
→ 约 115K QPS
```

这已经和 1000 QPS 是完全不同的问题。

---

# 2. 存储估算先看“每天增量”

例如日志系统每天写入：

```text
2B events/day
× 500 bytes
≈ 1 TB/day raw
```

再考虑：

```text
Index
Replica
Compression
Retention
Metadata
```

如果 90 天：

```text
90 TB raw before overhead
```

于是自然会出现：

- Hot / Cold Tier；
- Object Storage；
- Time Partition；
- TTL / Retention；
- Query Index。

---

# 3. 带宽估算

如果接口：

```text
10K QPS
× 100KB response
```

就是：

```text
~1 GB/s application payload
```

此时瓶颈可能不是 CPU，而是：

```text
Network
Egress Cost
Serialization
Client Download
```

System Design 不能只算数据库容量。

---

# 4. LLM / RAG 系统还要算 Token 与模型调用成本

例如：

```text
100 QPS
× 3000 input tokens
× 500 output tokens
```

每天 Token 量非常大。

于是你需要继续问：

```text
能否 Cache？
能否缩短 Context？
是否所有请求都需要大模型？
能否 Route 到小模型？
Rerank Candidate 是否过多？
```

AI System Design 的 Capacity 不只是 CPU / RAM。

---

# 5. Working Set 比总数据量更重要

系统总数据可能 100TB，但真正热点只有：

```text
最近 24h
Top 1% items
active sessions
```

这决定：

```text
多少数据必须放 Memory / SSD
多少可以 Cold Storage
Cache 是否有价值
```

不要因为总数据大就默认所有东西都要分布式内存化。

---

# 6. Hotspot：平均值会骗人

假设：

```text
100K QPS
1000 shards
```

平均每 Shard：

```text
100 QPS
```

看起来很轻松。

但如果 30% 流量都打一个 Celebrity / Hot Product：

```text
30K QPS → one key / partition
```

系统仍然会崩。

所以必须看：

```text
Key Distribution
Tenant Distribution
Hot Item Distribution
Time Burst
```

这就是为什么真人面试经常从 QPS 继续追 HotKey。

---

# 7. Capacity Planning 的四个维度

## Compute

```text
CPU
GPU
Thread / Coroutine
Worker
```

## Memory

```text
Cache
Index
Buffer
Queue
KV Cache
```

## Storage

```text
Primary Data
Replica
Index
Log
Snapshot
Backup
```

## Network

```text
Ingress
Egress
Cross-zone
Fan-out
Replication
```

只算其中一个维度通常会漏掉真正瓶颈。

---

# 8. Capacity ≠ Throughput

例如 Worker：

```text
Concurrency = 100
每任务平均 10s
```

理论吞吐约：

```text
10 tasks/s
```

如果上游每秒进 20 个：

```text
arrival > service rate
→ Queue 会持续增长
```

这就是 Backpressure 章节要解决的问题。

---

# 9. Headroom 为什么必要

如果系统平时就跑在：

```text
95% CPU
95% DB connections
95% Provider quota
```

任何：

```text
Retry
Failover
Burst
Rebalance
```

都可能让系统跨过崩溃点。

生产通常需要：

> **正常负载下保留 Failure / Burst Headroom。**

这也是 Google SRE 一直强调过载保护的原因。

---

# 10. 压测比“理论 QPS”更可信

估算只是设计起点。

最终 Capacity 需要：

```text
Load Test
→ Saturation Point
→ P95/P99
→ Error Rate
→ CPU/Memory/Connection
→ Downstream Pressure
```

测试还要覆盖：

```text
steady state
burst
one dependency slow
one node down
retry enabled
```

否则只能证明 Happy Path。

---

# 11. AI 系统的特殊 Hotspot

除了普通 HotKey，还可能有：

```text
某个大型 Tenant
某个热门 Knowledge Base
某个昂贵 Model
某个慢 Tool
某个超长 Prompt
某个巨型 PDF
```

因此 Capacity Metric 应带维度：

```text
tenant_id
model
route
tool
kb_id
```

否则总平均值会掩盖问题。

---

# 12. 🎯 面试怎么答

> 我不会一上来报一个拍脑袋 QPS，而会从用户规模、操作频率、Peak Factor、Read/Write Ratio 和 Payload 算数量级；存储则看每天增量、Retention、Replica 和 Index。然后单独检查 HotKey、Hot Tenant 与 Working Set，因为平均值经常掩盖热点。AI 系统还要把 Token、Model QPS、Context Length 和 Provider Quota 放进容量模型。最后所有估算都要通过 Load Test 找到真实 Saturation Point 和 P99，而不是把理论值当事实。

---

# 13. 本章自测

<details><summary>1. 为什么平均 QPS 不能直接用于 Shard Capacity？</summary>
因为流量可能高度倾斜到少数 Key/Tenant/Partition，真正瓶颈由 Hotspot 决定。
</details>

<details><summary>2. Queue 长度持续增长说明什么？</summary>
长期看 arrival rate 高于 service rate，系统没有稳定状态，需要扩容、降载、限流或降低单任务成本。
</details>

<details><summary>3. AI Gateway 容量为什么不能只看 HTTP QPS？</summary>
因为不同 Model、Token 长度和 Streaming Duration 的资源成本差异巨大，同样 1 QPS 的成本可能完全不同。
</details>
