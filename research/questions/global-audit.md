# Global Canonical Question Merge / Split Audit

更新日期：2026-09-10

本文件记录冻结语料 `S001–S279` 在十个正式一级板块完成 Primary Ownership 后的**全局问题级审计**。

> 工作口径以仓库当前 `README.md`、`schema.md`、`progress.md`、`module-index.md` 的最新描述为准。聊天中的历史总结、旧的“五大核心模块”等口径一律不能覆盖仓库最新规则。

## 1. 审计输入

正式一级板块：

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
Agent
  ↓
System Design
```

审计输入为第一阶段的 **230 个 Primary-owned ACTIVE Canonical Questions**。

审计依据只有：

1. `S001–S279` 冻结 HUMAN-A 真人面经；
2. `schema.md` 的 Merge / Split、Primary Module、Related Modules 与频率规则；
3. 当前十板块边界。

没有使用搜索引擎热度、题库频率或模型常识给 Source Count 加权。

---

## 2. 审计方法

对 230 个 ACTIVE 条目做跨文件比较，重点检查：

- 标题不同但核心知识模型相同；
- 一个 Canonical 同时塞入单机 / 分布式、正常路径 / Failure、实现 / Evaluation 等应拆能力；
- 同一 `Sxxx` 是否因为跨模块重复建题而被重复解释成两种能力；
- System Design Scenario 是否只是把底层 Canonical 换标题复制；
- Related Module 是否足够表达交叉，而无需再建立第二个 Primary；
- Source Count 是否等于列出的唯一 Evidence Sources 数量。

对可疑项回到对应 `batch-xx.md` 原始面经核验，不只依据 Canonical 标题相似度判断。

---

## 3. 本轮真正执行的 MERGE

### M-001 · `VDB-010` → `VDB-009`

旧问题：

- `VDB-009`：为什么需要独立 Vector DB？MySQL / PostgreSQL + pgvector、本地 FAISS 与专用 Vector DB 怎样选？
- `VDB-010`：Milvus、FAISS、pgvector、Elasticsearch Vector 等产品怎样选？

判断：**合并。**

二者共享同一个核心知识模型：Vector Storage 的架构边界 / 产品选型。继续分开会把“为什么需要某类 Vector Storage”与“选哪个 Vector Storage 产品”人为拆成两个高度重叠的 Canonical。

新 `VDB-009` 对证据取唯一并集：

`S004`, `S022`, `S054`, `S064`, `S095`, `S101`, `S109`, `S125`, `S136`, `S184`, `S211`, `S212`, `S249`, `S251`, `S255`, `S267`, `S275`, `S277`

**Source Count = 18**。

结果：Vector DB ACTIVE `13 → 12`；`VDB-010` 变为 MOVED legacy mapping。

### M-002 · `RAG-030` → `AGENT-037`

旧问题：

- `RAG-030`：Code RAG / Repository QA 与 AST、LSP、ripgrep、Filesystem Search 怎样分工？
- `AGENT-037`：Coding Agent 怎样理解大型 Repository？Vector RAG、AST/LSP、ripgrep、Dependency Graph 各适合什么？

判断：**合并。**

`RAG-030` 的 Evidence Sources：

`S038`, `S059`, `S132`, `S145`, `S218`

全部已经包含在 `AGENT-037` 的：

`S008`, `S038`, `S059`, `S132`, `S145`, `S218`, `S231`, `S236`, `S248`

两题本质都在考 Coding Agent 的 Repository Understanding / Retrieval Architecture，不应因其中一种手段叫 RAG 就重复建题。

结果：RAG ACTIVE `30 → 29`；`RAG-030` 变为 MOVED；`AGENT-037` 保持 Source Count 9。

---

## 4. 本轮真正执行的 SPLIT / NARROW

### S-001 · `MYSQL-010`：单表 Deep Pagination 与跨 Shard Pagination 拆开

旧 `MYSQL-010` 同时包含：

- 单表 / 单分片 Offset Deep Pagination；
- 分库分表后的跨 Shard 查询、跳页、全局排序。

原始 HUMAN-A 核验后：

- `S093`, `S147` 明确是分库分表后的跨 Shard / 跨库聚合问题，归 `MYSQL-021` Sharding；
- `S010`, `S025`, `S131`, `S148` 支撑单表 / 单分片 Deep Pagination。

因此新 `MYSQL-010` Source Count = **4**，只讨论单表 / 单分片访问路径；跨分片问题由 `MYSQL-021` 承接。

### S-002 · `MYSQL-022`：MySQL 写入路径与通用批处理系统设计拆开

旧 `MYSQL-022` 同时包含：

- “一亿条数据怎样快速写入 MySQL”这种 MySQL Write Path；
- 大批量读取 / 数据迁移 / 分页 / 并发 / Backpressure / 断点恢复等端到端 Batch Processing。

审计后：

- `MYSQL-022` 只保留 `S191` 的 MySQL-specific Bulk Write，Source Count = **1**；
- `S094`, `S207`, `S232`, `S244` 继续由 `SD-007` 承接通用批处理 / 数据迁移系统设计。

### S-003 · `AIBE-029`：Backend Observability 与 Agent Execution Trace 拆开

旧 `AIBE-029` 把两类能力混在一起：

1. Production Backend 的 Metrics / Log / Trace；
2. Agent Runtime 的 step / model / tool / state 级执行轨迹。

审计后：

- `AIBE-029` 只保留通用 Backend Observability：`S066`, `S108`, `S109`, `S156`, `S183`，Source Count = **5**；
- 新建 `AGENT-043`：Agent Execution Trace / Observability，Evidence Sources = `S034`, `S129`, `S146`, `S240`, `S242`，Source Count = **5**。

这不是同一问题“换板块”，而是把通用服务可观测性与 Agent 执行语义拆成两个可以被独立追问的知识模型。

---

## 5. Evidence 修正

### E-001 · `AGENT-028` 补入 `S254`

`S254` 明确追问：Agent Code Execution Boundary、Tool Calling Security、OpenClaw Permission Model、Reverse Shell、Docker Escape 等安全边界。

因此 `AGENT-028`（Permission / Approval / HITL / Sandbox）Evidence Sources 补入 `S254`，Source Count `15 → 16`。

---

## 6. 明确审计过但 KEEP SEPARATE 的高相似问题

这些条目词面相似，但核心知识模型不同，因此**不合并**：

| Canonical A | Canonical B | 为什么不合并 |
|---|---|---|
| `PY-012` Python asyncio | `AIBE-012` Async Service | 前者是语言 / Event Loop 语义，后者是服务架构取舍 |
| `FASTAPI-004` FastAPI + SSE | `AIBE-006` SSE vs WebSocket | 前者是框架实现，后者是协议与通信模型 |
| `AIBE-018` 通用 Resilience | `AGENT-038` Agent Runtime Resilience | 前者是通用服务熔断/降级，后者是模型/Tool错误语义驱动的 Runtime Policy |
| `AIBE-019` 通用 Idempotency | `AGENT-029` Checkpoint + External Side Effect | 后者专门考察 Agent Resume 与已发生外部副作用之间的 Exactly-once-like 问题 |
| `AIBE-023` Distributed Session Routing | `REDIS-017` Redis Session | 通用多实例路由 vs Redis-specific 实现 |
| `AIBE-023` Distributed Session Routing | `AGENT-017` Agent State Isolation | 服务路由 vs 多用户 Agent Memory / Context / Permission 隔离 |
| `VDB-020` Vector Index Lifecycle | `RAG-024` KB Freshness | 向量 / 索引版本迁移 vs 整个知识库内容新鲜度和版本治理 |
| `LLM-022` Hallucination / Factuality | `RAG-019` RAG Bad-case Attribution | 模型本体局限边界 vs RAG Pipeline 故障归因 |
| `RAG-020` Retrieval Metrics | `RAG-021` E2E RAG Evaluation | 检索层指标 vs 系统最终质量分层评估 |
| `RAG-026` Large-scale RAG | `SD-017` 600GB–1TB Vertical RAG | 通用能力 vs 明确容量约束的端到端 Scenario |
| `RAG-002` RAG Pipeline | `SD-016` Enterprise RAG Design | 流程机制 vs 企业级端到端系统设计 |
| `AGENT-026/027/029` Runtime primitives | `SD-022` Long-running Agent Design | 单项 Runtime 机制 vs 多约束组合场景 |
| `AGENT-032` Runtime Model Adapter | `SD-013` LLM Gateway | Agent 内部 Provider Adapter vs 独立 Gateway 服务架构 |
| `AGENT-003` Agent Loop | `SD-021` Production Agent Backend | 内部执行循环 vs 端到端生产服务架构 |
| `AGENT-020` Tool Call Failure | `AGENT-038` Runtime Resilience | 单次调用错误反馈 / Repair vs 跨依赖 Retry / Backoff / Circuit Breaker / Failover Policy |

---

## 7. 审计后全局数量

| 一级板块 | ACTIVE |
|---|---:|
| Python | 15 |
| FastAPI | 4 |
| AI Backend Engineering | 39 |
| MySQL | 26 |
| Redis | 19 |
| Vector DB | 12 |
| LLM Foundation（应用工程深度） | 22 |
| RAG | 29 |
| Agent | 39 |
| System Design | 24 |
| **合计** | **229** |

Legacy MOVED 映射：**24**。

从 Phase 1 的 230 ACTIVE 到本轮 229 ACTIVE：

```text
230
- 1  VDB-010 → VDB-009
- 1  RAG-030 → AGENT-037
+ 1  新建 AGENT-043（由 AIBE-029 拆出）
= 229
```

`MYSQL-010` / `MYSQL-022` 属于 Narrow / Evidence Reassignment，没有改变 Canonical 数量。

---

## 8. 本轮不做的事情

本文件只完成 **Global Merge / Split / Ownership / Evidence Audit**，不提前混入下一阶段市场统计。

下一阶段单独产出：

```text
Global Canonical Question Index
→ Frequency Ranking
→ Company / Role / Round Coverage
→ Interview Depth
→ Follow-up Chain
→ Curriculum Coverage Matrix
→ Knowledge Gap Analysis
```

Agent Harness 的课程知识边界仍将在教材阶段使用 Claude Code / Codex 源码校准；源码不参与本轮 229 道 HUMAN-A Canonical 的频率统计。
