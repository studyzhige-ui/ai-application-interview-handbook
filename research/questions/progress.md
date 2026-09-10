# Canonical Question 重建进度

更新日期：2026-09-10

## Repository-first 规则

> **后续所有工作都以仓库当前最新描述为准。** 每次继续研究前，先读取本目录的 `README.md`、`schema.md`、`progress.md`、`module-index.md` 与相关模块文件；聊天中的历史总结、旧分类、旧计数只能作为背景，不能覆盖仓库最新状态。

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 不继续搜索新面经，除非用户明确重新开启采集

## 正式十板块

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

`Coding / Debug / AI Coding` 只作为 `Question Type`，不作为一级板块。

---

## Phase 1：十板块纵向 Canonicalization ✅

已完成：

1. `S001–S279` 全库直接回读；
2. 十个一级板块分别纵向扫描；
3. 每道 Canonical 建立唯一 `Primary Module`；
4. 第一轮跨模块 Merge / Move 归属审计。

Phase 1 结束时共有 **230 ACTIVE Canonical / 22 MOVED**。

---

## Phase 2A：Global Merge / Split Audit ✅

已对 Phase 1 的 230 个 Primary-owned ACTIVE 条目做全局问题级复核，并对可疑项回到原始 `batch-xx.md` 核验。

### 审计后状态

| 顺序 | 一级板块 | 当前版本 | ACTIVE | MOVED |
|---:|---|---:|---:|---:|
| 1 | Python | v2 | 15 | 0 |
| 2 | FastAPI | v2 | 4 | 1 |
| 3 | AI Backend Engineering | v3 | 39 | 0 |
| 4 | MySQL | v3 | 26 | 2 |
| 5 | Redis | v2 | 19 | 5 |
| 6 | Vector DB | v3 | 12 | 11 |
| 7 | LLM Foundation（应用工程深度） | v2 | 22 | 0 |
| 8 | RAG | v3 | 29 | 1 |
| 9 | Agent Harness / Runtime | v3 | 39 | 4 |
| 10 | System Design | v2 | 24 | 0 |
|  | **合计** |  | **229 ACTIVE** | **24 MOVED** |

完整审计决策见 `global-audit.md`。

### 本轮主要变化

- `VDB-010` 产品选型 → MERGED 到 `VDB-009`；
- `RAG-030` Code RAG / Repo Search → MERGED 到 `AGENT-037`；
- `MYSQL-010` 拆清单表 Deep Pagination 与跨 Shard Pagination；
- `MYSQL-022` 拆清 MySQL Bulk Write 与通用 Batch / Migration System Design；
- `AIBE-029` 拆清通用 Backend Observability 与 Agent Execution Trace；
- 新建 `AGENT-043` Execution Trace / Observability；
- `AGENT-028` 补入 `S254` Permission / Sandbox 安全证据；
- 明确一批词面相似但核心知识模型不同的 KEEP-SEPARATE 对。

### 数量变化

```text
230
- 1  VDB-010 → VDB-009
- 1  RAG-030 → AGENT-037
+ 1  AIBE-029 拆出 AGENT-043
= 229 ACTIVE
```

MySQL 两项属于 Narrow / Evidence Reassignment，不改变 Canonical 数量。

---

## Phase 2B：Global Index + Market Analysis ⏳ 下一步

从当前 **229 个 ACTIVE Canonical** 出发，下一步生成真正的全局可分析视图：

```text
Global Canonical Question Index
        ↓
Evidence / Source Count 一致性复核
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

这一阶段不再随意调整一级分类。如果发现新的 Merge / Split 问题，必须先记录到 `global-audit.md`，回到 HUMAN-A 原始来源核验后再修改 Canonical。

---

## Agent Harness 特殊规则

Agent Harness 的**面经统计层**只反映 `S001–S279` 真人面试已经问到的内容。

正式建设 Agent 教材时，还必须额外研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

成熟源码属于课程权威实现证据，用于补齐完整 Harness / Runtime 知识边界；**不得**反向改变 HUMAN-A `Source Count`。