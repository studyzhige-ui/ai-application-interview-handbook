# Canonical Question 重建进度

更新日期：2026-09-10

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 本轮目标：不再搜索新面经，只把冻结语料归一化为正式问题数据集

## 全库读取状态

`S001–S279` 所在 26 个 Batch 已完成一轮直接回读，用于建立统一归一化标准。

> 注意：Batch 文件中的历史“累计来源数 / 下一编号”等过程性统计按采集时口径保留；Canonical 重建只使用当前去重后的 `S001–S279` 正式编号。

## 五大核心模块纵向扫描

| 模块 | 状态 | Canonical 条目数 | 说明 |
|---|---:|---:|---|
| MySQL | ✅ v1 完成 | 28 | 索引、事务、MVCC、锁、日志、Sharding、DB-Cache Consistency 等 |
| Redis | ✅ v1 完成 | 24 | 数据结构、缓存、BigKey/HotKey、锁、Cluster、Session、Agent State 等 |
| Vector DB | ✅ v1 完成 | 23 | Embedding、ANN、HNSW/IVF、Hybrid、RRF、Rerank、Evaluation 等 |
| RAG | ✅ v1 完成 | 30 | Parse、Chunk、Retrieval、Rerank、Evaluation、Freshness、Production 等 |
| Agent Harness / Runtime | ✅ v1 完成 | 42 | Loop、Context、Memory、Tool、MCP/Skill、Checkpoint、Permission、Eval 等 |

当前五大核心模块共形成 **147 个“模块内 Canonical 条目”**。这个数字**不是全局独立问题数**：

- `MySQL + Redis Consistency` 同时属于 MySQL / Redis；
- `Hybrid Retrieval / RRF / Rerank` 同时属于 Vector DB / RAG；
- `RAG Context / Agent Context`、`Redis Checkpoint / Agent Checkpoint` 等存在跨模块交叉。

因此下一步必须做跨模块审计，建立全局能力视图，而不能直接把 147 当成“147 道独立面试题”。

## 下一步：Cross-module Audit + Market Analysis

当前开始进入第二阶段：

```text
五大模块 v1
    ↓
Cross-module Merge / Split Audit
    ↓
全局 Capability / Question Index
    ↓
Frequency Ranking
    ↓
Interview Depth / Follow-up Chain
    ↓
Curriculum Coverage Matrix
    ↓
Knowledge Gap Analysis
```

随后再处理支持模块：

| 模块 | 状态 |
|---|---|
| FastAPI | ⏳ |
| Backend Engineering | ⏳ |
| LLM Foundation | ⏳ |
| System Design | ⏳ |
| Coding / Debug / AI Coding | ⏳ |

这些支持模块并不会阻塞 MySQL 教材启动；但在最终“全市场画像”发布前仍应补齐，因为 HUMAN-A 中大量真实考察正是 AI + Backend Foundation 混合型。

## 质量状态

所有 v1 文件中的 `Source Count` 都必须等于对应条目列出的唯一 `Sxxx` 数量，并且只使用冻结后的正式 HUMAN-A。

当前仍允许两类修正：

1. 某个问题更适合被拆成两个 Canonical Question；
2. 某个跨模块问题需要合并到同一个 Global Capability，或增加 / 移动证据来源。

任何修正都必须保留可追溯的 `Sxxx`，不能凭常识、搜索热度或其它题库虚增“面试频率”。

## Agent Harness 特殊规则

Agent Harness 的**面经统计层**已经完成 v1；它只反映 2026 HUMAN-A 实际问到的能力。

后续做 Agent 课程时，还必须单独研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

用两套成熟产品源码补齐完整 Runtime / Harness 知识体系。源码研究属于“课程权威实现证据”，不能反向改变 HUMAN-A 的 Source Count。
