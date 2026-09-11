# Curriculum Content Depth Audit

更新日期：2026-09-11

> 本文件记录 Redis / Vector DB / LLM Foundation / RAG 的颗粒度整改后深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。

---

## 1. 验收原则

内容深度不按 KB 大小机械判断。

正式标准是一个知识块是否能覆盖大部分：

```text
为什么需要
→ 准确定义 / Mental Model
→ 机制 / 数据流 / 算法
→ 参数或关键设计
→ Failure / Trade-off
→ Production / AI Application 场景
→ 模块边界
→ 面试表达
→ 易错点 / 深挖
→ 折叠自测
```

文件大小、Section 数量只是用于发现异常候选，不是质量结论。

例如：

- `Pipeline` 本身是窄主题，5KB 左右也可以形成完整闭环；
- `Scale / Cost / Observability` 是大型 Production 子系统，如果只有 4KB 概览就明显不够。

---

## 2. 全量机械扫描

扫描范围：

```text
Redis          24 docs
Vector DB      16 docs
LLM Foundation 14 docs
RAG            14 docs
-------------------
Total          68 docs
```

扫描信号包括：

- 字节数；
- Section 数；
- Code / Diagram block；
- `<details>` 自测；
- 面试回答；
- Failure / Trade-off / 易错边界。

结果：

```text
Very-short (< 3.5KB)      0
Missing self-test          0
Missing interview answer   0
```

自动扫描曾产生 20 个 Warning，主要是旧正文大量使用 `# 2.` 而不是 `## 2.`，导致简单正则低估 Section 数；这些 Warning 只作为人工复核入口，不能直接判定不合格。

---

# 3. Redis — ✅ PASS

当前：**24 个连续知识小板块，`docs/01 → 24`。**

重点人工复核了相对较短或被扫描器标记的：

- `04-扩展数据结构.md`
- `07-TTL与过期删除.md`
- `12-Replication.md`
- `16-Pipeline.md`
- `19-PubSub与Streams.md`

结论：通过。

原因不是“文件够长”，而是主题本身边界较窄但闭环完整。

例如：

### TTL

已经包含：

```text
expire semantics
lazy / active expiry
timeout / jitter / sliding expiry
persistence / replication boundary
AI state use case
interview answer
self-test
```

### Pipeline

已经覆盖：

```text
RTT problem
pipeline mechanics
Pipeline ≠ Transaction
batch size / memory / error semantics
Cluster boundary
idempotency / backpressure
AI batch use case
interview / self-test
```

### Extended Data Structures

虽然扫描器没有匹配到英文 `Failure / Trade-off` 关键词，但正文实际已经明确：

- Bitfield 的可读性 / 调试代价；
- HyperLogLog 的近似误差与不可枚举成员；
- Stream 与 Kafka 的能力边界；
- 不同结构适用与不适用场景。

因此属于自动规则误报，不需要为了篇幅再扩写。

**最终结论：Redis Content Depth PASS。**

---

# 4. Vector DB — ✅ PASS

当前：**16 个连续知识小板块，`docs/01 → 16`。**

重点人工复核：

- `04-ANN索引谱系.md`
- `06-IVF原理.md`
- `07-Quantization与PQ.md`
- `09-Vector数据建模.md`
- `10-MetadataFilter.md`
- `11-Partition与TenantIsolation.md`
- `13-分布式VectorDB.md`

并结合本来就较深的：

- `05-HNSW机制与调优.md`
- `12-VectorIndex生命周期.md`
- `14-性能容量与Production诊断.md`
- `16-GraphDB边界与系统设计.md`

一起验收。

结论：通过。

### 为什么 4–5KB 的 IVF / PQ 仍可以通过

因为它们是边界明确的算法子系统，正文已经形成：

```text
为什么需要
→ 核心机制
→ 关键参数
→ Recall / Latency / Memory Trade-off
→ 与 HNSW / IVF-PQ 等组合关系
→ Production 选择
→ 面试 / 自测
```

### Metadata / Tenant / Distributed

已经覆盖：

```text
Schema / stable identity / version
Pre-filter vs Post-filter
filter selectivity
permission boundary
partition vs shard
fan-out / global Top-K
replica / rebalance
hot tenant / capacity
```

没有发现“合并后承担了大主题但仍只剩概览”的情况。

**最终结论：Vector DB Content Depth PASS。**

---

# 5. LLM Foundation — ✅ PASS after targeted remediation

当前：**14 个连续知识小板块，`docs/01 → 14`。**

全量机械扫描中 14/14 均具备：

- 自测；
- 面试表达；
- Failure / Trade-off；
- 足够的机制或工程说明。

人工复核重点：

- `10-MultimodalFoundation.md`
- `11-PromptEngineering.md`
- `14-PostTraining与Distillation.md`

### Prompt Engineering

本身已经是完整工程闭环：

```text
Prompt structure
→ role / priority boundary
→ few-shot
→ structured output
→ versioning
→ evaluation / regression
→ Prompt vs RAG / Fine-tuning / Runtime
```

无需为了字数继续扩写。

### Post-training

应用工程深度已经足够：

```text
SFT limit
→ RLHF / Reward
→ DPO / GRPO boundary
→ reward hacking
→ distillation / synthetic data
→ when application team should care
```

没有必要扩成算法岗 PPO / RL 数学课。

### Multimodal Foundation — 已补强

原稿更像 4KB 概览，因此进行了实质扩写，目前加入：

```text
Perception / Alignment / Reasoning 分层
Visual Token / Resolution / Cost Budget
OCR / Layout / Direct Vision boundary
Document Layout
Audio / Video temporal complexity
Multimodal retrieval vs generation
Production failure attribution
Evaluation dataset / metrics
Privacy / data governance
RAG / Agent module boundary
```

补强后已经和其它核心 LLM 章节处于同一教学深度。

**最终结论：LLM Foundation Content Depth PASS。**

---

# 6. RAG — ✅ PASS after targeted remediation

当前：**14 个连续 Production RAG 子系统，`docs/01 → 14`。**

原 01–12 已经普遍具备较完整的：

```text
Pipeline / Data Model
Failure Attribution
Evaluation
Production Boundary
Interview / Self-test
```

重点复核发现两个大主题原稿偏薄：

- `13-ScaleCostObservability.md`
- `14-GraphRAG与AgenticRAG.md`

两章已完成实质补强。

### 13 Scale / Cost / Observability

新增并深化：

```text
Ingestion state machine
idempotency by source + processing version
per-stage backpressure
Generation / Snapshot rebuild
Delta catch-up
stage-level latency / SLO
P99 attribution
Offline / Online cost model
Candidate Budget
Cache versioning
Production Trace
Freshness Lag
Quality monitoring
Degradation / Load Shedding
Failure timelines
```

现在它真正承担 Production RAG 运行子系统，而不是监控指标清单。

### 14 GraphRAG / Agentic RAG

新增并深化：

```text
Entity extraction / resolution
Relation provenance
Graph retrieval patterns
Vector + Keyword + Graph composition
Incremental graph update
Graph quality evaluation
Agentic Runtime State
Evidence Sufficiency
No-new-evidence detection
Query Drift
Step / Cost Budget
Multi-source routing
Agentic RAG evaluation
Production architecture
```

并明确：GraphRAG / Agentic RAG 不是默认升级路线，必须用 Baseline + Evaluation 证明收益。

**最终结论：RAG Content Depth PASS。**

---

# 7. System Design — ✅ PASS

当前：**19 个连续知识小板块，`docs/01 → 19`，并包含 Review + Interview 三件套。**

System Design 从一开始就按当前粒度规则建设，没有经历“24 道 Canonical → 24 个文件”的机械映射。正文分成：

```text
01–12  通用设计方法
13–19  综合 Scenario Pattern
```

完成后重点核验了：

- `01-SystemDesign职责与答题框架.md`：是否先教 Clarify / SLO / Capacity / State / Failure / Verify；
- `13-HighConcurrencyTransactionalSystems.md`：是否从业务 invariant 进入库存 / Rate Limit / Token Refresh，而不是背组件；
- `17-EnterpriseRAGSystemDesign.md`：是否覆盖 Ingestion / Permission / Generation / Evaluation / Freshness / Cost；
- `18-ProductionAgentBackend.md`：是否覆盖 Durable Run、Checkpoint、Tool Side Effect、Lease、Cancellation、Trace / Eval；
- `19-VerticalAIAgentPatterns.md`：是否能把同一套方法迁移到 Analysis / Customer Service / Multimodal / Game / Content，而不是五套模板。

19 章统一具备：

```text
Why / Requirement
→ Mental Model / Data Flow
→ Trade-off / Failure
→ Scale / Security / Reliability（按主题）
→ Verification / Observability
→ 面试回答
→ 折叠自测
```

并额外提供 6 张 Review 总图、36 道 Interview Drill、60 个易错点和面试前速查表。

**最终结论：System Design Content Depth PASS。**

---

# 7. 最终验收状态

| 模块 | Blocks | Numbering | Depth |
|---|---:|---|---|
| Redis | 24 | ✅ `01–24` 连续 | ✅ PASS |
| Vector DB | 16 | ✅ `01–16` 连续 | ✅ PASS |
| LLM Foundation | 14 | ✅ `01–14` 连续 | ✅ PASS |
| RAG | 14 | ✅ `01–14` 连续 | ✅ PASS |
| System Design | 19 | ✅ `01–19` 连续 | ✅ PASS |

同时已验证：

- README 正文链接指向实际文件；
- Review / Interview 中旧文件名引用已更新；
- 代表性旧路径已不存在；
- 编号和 H1 标题一致；
- 四模块共 68 篇正文没有“极短占位稿”、没有缺失自测或面试回答的文件。

---

# 8. 后续规则

System Design 及未来新增模块继续使用同一标准：

```text
先定知识闭环
→ 再定 Markdown
→ 写完整机制 / Failure / Trade-off / Production
→ 自动 QA 找异常
→ 人工深度验收
→ 最后才标记完成
```

自动检查永远只是异常发现器，不能替代人工判断内容是否真正形成认知闭环。
