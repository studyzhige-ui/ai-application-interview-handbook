# Canonical Question 重建进度

更新日期：2026-09-11

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

### Phase 2A 主要变化

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

## Phase 2B：Global Index + Market Analysis ✅

Phase 2B 已完成自动统计层与人工核验层。

### 2B-1 自动统计与一致性验证

自动构建：

- `research/analysis/global-question-index.md`
- `research/analysis/global-question-index.csv`
- `research/analysis/frequency-ranking.md`
- `research/analysis/market-coverage.md`
- `research/analysis/depth-and-types.md`
- `research/analysis/cooccurrence.md`
- `research/analysis/curriculum-evidence-matrix.md`
- `research/analysis/module-metrics.csv`
- `research/analysis/source-coverage-validation.md`

最终硬校验：

| Check | Result |
|---|---|
| Frozen HUMAN-A | ✅ 279 / 279 |
| ACTIVE Canonical | ✅ 235 / 235 |
| Mapped to >=1 Canonical | ✅ 278 |
| Documented VALID-UNMAPPED | ✅ 1 (`S271`) |
| Unexpected uncovered | ✅ 0 |
| Evidence outside S001–S279 | ✅ 0 |
| Source Count mismatch | ✅ 0 |

### 2B-2 Coverage Gap Audit

首次自动校验发现 28 个零映射 HUMAN-A。回到原始 Batch 人工复核后：

- 27 个来源补入已有 / 新 Canonical；
- `S271` 明确保留 `VALID-UNMAPPED`，不为追求 279/279 强行造题；
- 新增 6 道真实独立能力 Canonical：
  - `LLM-023` Prompt Engineering
  - `AGENT-044` Prompt Injection / Untrusted Context Security
  - `AGENT-045` Intent Recognition / Routing
  - `AGENT-046` A2A / Agent Communication Protocol
  - `AGENT-047` Agent Framework Selection
  - `AGENT-048` AI-assisted Development Workflow

因此：

```text
229 ACTIVE
+ 6 Phase 2B reviewed gaps
= 235 ACTIVE
```

人工审计记录见 `source-coverage-audit.md` 与 `tools/phase2b_canonical_audit.json`。

### 2B-3 Verified Follow-up Chains

已从 `cooccurrence.md` 回到原始 Batch 核验真正有方向的追问链，见：

- `research/analysis/follow-up-chains.md`

高价值递进包括：

```text
RAG Pipeline
→ Chunk
→ Hybrid Retrieval
→ Rerank
→ Evaluation / Bad Case

Agent Boundary
→ Harness / Loop
→ Tool / Skill
→ Context / Memory
→ Failure / Resume
→ Evaluation

Context Assembly
→ Compaction
→ Correctness
→ Memory Pollution
→ Resume

AI Coding
→ Requirement / Context
→ Repo Modification
→ Test / Review
→ Verification / Delivery
```

### 2B-4 Knowledge Gap Analysis

已将市场证据矩阵与 `roadmap/knowledge-map.md` 对照，见：

- `research/analysis/knowledge-gap-analysis.md`

主要修正：

1. LLM Foundation 正式补成一级 Roadmap；
2. Vector DB / RAG Primary Boundary 对齐最新 Canonical；
3. Agent Harness 吸收 Phase 2B 新增能力域；
4. MySQL / Redis / RAG 按真实面试深度补 Failure / Scale / Evaluation；
5. 面经研究状态从“持续滚动采集”同步为 Frozen `S001–S279`。

---

## 当前正式 Ownership

| 顺序 | 一级板块 | ACTIVE |
|---:|---|---:|
| 1 | Python | 15 |
| 2 | FastAPI | 4 |
| 3 | AI Backend Engineering | 39 |
| 4 | MySQL | 26 |
| 5 | Redis | 19 |
| 6 | Vector DB | 12 |
| 7 | LLM Foundation（应用工程深度） | 23 |
| 8 | RAG | 29 |
| 9 | Agent Harness / Runtime | 44 |
| 10 | System Design | 24 |
|  | **合计** | **235** |

---

## Phase 3：Curriculum Build / Remediation ⏳ 下一步

Canonical 重建和市场分析已经足够稳定，下一阶段不再继续围绕题目数量做优化，而把结果反哺正式教材。

当前推荐顺序：

```text
P0 Roadmap 一致性修复 ✅ 已同步
        ↓
MySQL 正式系统教材
        ↓
Redis
        ↓
Vector DB
        ↓
LLM Foundation
        ↓
RAG
        ↓
Agent Harness / Runtime
        ↓
System Design
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有课程骨架，后续按项目和 Bridge Lab 逐步写正文。

每个新教材模块都应同时参考：

- 完整知识体系；
- `curriculum-evidence-matrix.md` 的市场信号；
- `follow-up-chains.md` 的真实递进；
- 对应 Canonical 的 Evidence Sources；
- 必要的官方 / 权威资料。

统一章节深度模板：

```text
Concept
→ Mechanism
→ Trade-off
→ Failure
→ Scale
→ Evaluation / Verification
```

---

## Agent Harness 特殊规则

Agent Harness 的**面经统计层**只反映 `S001–S279` HUMAN-A 市场证据。

正式建设 Agent 教材时，还必须额外研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

成熟源码属于课程权威实现证据，用于补齐完整 Harness / Runtime 知识边界；**不得**反向改变 HUMAN-A `Source Count`。
