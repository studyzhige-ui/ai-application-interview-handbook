# Canonical Question 重建进度

更新日期：2026-09-10

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 本轮目标：不再搜索新面经，只把冻结语料按正式学习路径归一化为可统计、可回溯的问题数据集

## 第一阶段定义

第一阶段**不是**“先整理五大核心模块，再补支持模块”。旧口径废弃。

正式一级板块只有下面十个，并严格按这条学习路径组织：

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用工程深度）
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

`Coding / Debug / AI Coding` 只作为 `Question Type`，不再单独成为一级板块。

第一阶段只有同时满足下面三件事才算完成：

1. 十个一级板块都对 `S001–S279` 做完一轮全库纵向扫描；
2. 每一道 Canonical Question 完成 `Primary Module` 唯一归属；
3. 十个板块都通过跨模块 Merge / Move 审计，不能把同一个核心问题复制到多个一级板块。

因此，**只有“十板块文件都存在”并不代表第一阶段完成。**

---

## 全库读取状态

`S001–S279` 所在 26 个 Batch 已完成一轮直接回读，用于建立统一归一化标准。

> Batch 文件中的历史“累计来源数 / 下一编号”等过程性统计按采集时口径保留；Canonical 重建只使用当前去重后的 `S001–S279` 正式编号。

## 十板块纵向扫描 / 归属审计状态

| 顺序 | 一级板块 | 当前状态 | 当前条目 | 说明 |
|---:|---|---|---:|---|
| 1 | Python | 🟡 v1 扫描完成，待 v2 归属审计 | 15 | 语言 / Runtime；需与 FastAPI、AI Backend 再做边界复核 |
| 2 | FastAPI | ✅ v2 归属审计完成 | 4 ACTIVE + 1 MOVED | `await` / Event Loop 核心语义已迁回 Python `PY-012` |
| 3 | AI Backend Engineering | ✅ v2 归属审计完成 | 39 | Network、Streaming、Concurrency、MQ、Rate Limit、Retry、Auth、Session、Infra 等 |
| 4 | MySQL | ✅ v2 归属审计完成 | 26 ACTIVE + 2 MOVED | 跨存储一致性已迁移到 AI Backend Engineering |
| 5 | Redis | ✅ v2 归属审计完成 | 19 ACTIVE + 5 MOVED | 通用 Rate Limit / DB-Cache Consistency / Agent Checkpoint 等已迁出 |
| 6 | Vector DB | ✅ v2 归属审计完成 | 13 ACTIVE + 10 MOVED | Hybrid / RRF / Rerank 归 RAG；Embedding/Rerank 模型原理归 LLM Foundation |
| 7 | LLM Foundation（应用工程深度） | 🟡 v1 扫描完成，待 v2 归属审计 | 22 | Token、Transformer、Inference、Model API、Embedding/Rerank Model、Post-training |
| 8 | RAG | ✅ v2 归属审计完成 | 30 | Parse、Chunk、Retrieval、Fusion、Rerank、Evaluation、Freshness、Production |
| 9 | Agent Harness / Runtime | ✅ v2 归属审计完成 | 38 ACTIVE + 4 MOVED | 通用 Transport / Rate Limit / Scale 已迁到 AI Backend；端到端架构归 System Design |
| 10 | System Design | 🟡 v1 扫描完成，待 v2 归属审计 | 24 | 只保留端到端 Scenario，需继续检查是否误收底层单点问题 |

### 当前第一阶段状态

- 十板块文件：**10 / 10 已建立**
- 全库纵向扫描：**10 / 10 已有 v1**
- `Primary Module` / 跨模块去重审计：**7 / 10 完成 v2**
- 尚待完成 v2 的板块：`Python`、`LLM Foundation`、`System Design`
- 当前 ACTIVE 模块条目暂计：**230**；这仍不是最终全局独立问题数
- 结论：**第一阶段尚未完成。**

---

## 当前已执行的跨模块迁移原则

```text
MySQL + Redis 双写一致性
        ↓
Primary: AI Backend Engineering
Related: MySQL, Redis
```

```text
Vector + BM25 → RRF → Rerank
        ↓
如果问 RAG Retrieval Pipeline：Primary = RAG
如果问 HNSW / IVF / ANN Index：Primary = Vector DB
如果问 Embedding / Cross-Encoder 模型原理：Primary = LLM Foundation
```

```text
FastAPI async 调 LLM 时 await 期间 Event Loop / CPU / Thread 在做什么
        ↓
Primary: Python（asyncio Runtime）
Related: FastAPI, AI Backend Engineering
```

```text
Agent SSE / WebSocket
        ↓
协议与服务端传输：AI Backend Engineering
FastAPI 具体实现：FastAPI
Agent Event / State 如何进入流：Agent Harness / Runtime
端到端 Agent Backend：System Design
```

---

## 第一阶段接下来怎么做

继续完成剩余三个 v2 审计：

```text
Python
  ↓
LLM Foundation（应用工程深度）
  ↓
System Design
```

每完成一个板块，都检查：

- 是否与另外九个板块存在同一道核心问题的重复 Canonical；
- 是否应该 `MOVE` 而不是复制；
- `Source Count` 是否等于唯一 `Evidence Sources` 数量；
- `Primary Module` 是否只有一个；
- 真实问法是否仍然保留面经语境，而不是被抽象成普通教材目录。

只有这三个板块全部升级到 v2 后，才把第一阶段标为完成。

---

## 第二阶段（第一阶段完成后再开始）

```text
Global Canonical Question Index
        ↓
Frequency Ranking
        ↓
Company / Role / Round Coverage
        ↓
Interview Depth / Follow-up Chain
        ↓
Curriculum Coverage Matrix
        ↓
Knowledge Gap Analysis
```

任何修正都必须保留可追溯 `Sxxx`，不能凭常识、搜索热度或其它题库虚增真人面试频率。

## Agent Harness 特殊规则

Agent Harness 的面经统计层只反映 `S001–S279` 真人面试已经问到的内容。

后续正式建设 Agent 教材时，还要单独研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

成熟源码属于课程实现证据，不能反向改变 HUMAN-A 的 `Source Count`。