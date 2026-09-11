# Canonical Question 重建与课程建设进度

更新日期：2026-09-11

## Repository-first 规则

> **后续所有工作都以仓库当前最新描述为准。** 每次继续研究或建设教材前，先读取本目录的 `README.md`、`schema.md`、`progress.md`、`module-index.md`、根 `README.md`、`roadmap/knowledge-map.md` 与相关模块文件；聊天中的历史总结、旧分类、旧计数只能作为背景，不能覆盖仓库最新状态。

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- ACTIVE Canonical：**235**
- Mapped Sources：**278**
- VALID-UNMAPPED：**1（S271）**

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

完成 `S001–S279` 全库回读、十板块纵向扫描、唯一 Primary Module 与第一轮跨模块归属审计。

Phase 1 结束：**230 ACTIVE / 22 MOVED**。

## Phase 2A：Global Merge / Split Audit ✅

完成全局问题级 Merge / Split / Narrow / Evidence Reassignment。

主要修正：

- `VDB-010` → `VDB-009`；
- `RAG-030` → `AGENT-037`；
- `MYSQL-010` 拆清单表 Deep Pagination 与跨 Shard Pagination；
- `MYSQL-022` 拆清 MySQL Bulk Write 与通用 Batch / Migration；
- `AIBE-029` 拆出 `AGENT-043` Execution Trace；
- `AGENT-028` 补入 Permission / Sandbox 安全证据。

Phase 2A 结束：**229 ACTIVE / 24 MOVED**。

## Phase 2B：Global Index + Market Analysis ✅

自动统计层与人工核验层均完成。

| Check | Result |
|---|---|
| Frozen HUMAN-A | ✅ 279 / 279 |
| ACTIVE Canonical | ✅ 235 / 235 |
| Mapped to >=1 Canonical | ✅ 278 |
| Documented VALID-UNMAPPED | ✅ 1 (`S271`) |
| Unexpected uncovered | ✅ 0 |
| Evidence outside S001–S279 | ✅ 0 |
| Source Count mismatch | ✅ 0 |

Phase 2B Coverage Gap Audit 新增 6 道独立能力：`LLM-023`、`AGENT-044` ～ `AGENT-048`。

最终 Ownership：

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

分析产物见 `research/analysis/`。

---

## Phase 3：Curriculum Build / Remediation 🚧

### 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度，不能反过来打乱模块本身的演进顺序。**

统一建设形态：

```text
模块 README
+ 系统正文 docs/
+ 每章折叠自测
+ review/ 图解与综合自测
+ interview/ 高频题
+ interview/ 易错点
+ interview/ 面试前速查
```

统一章节深度：

```text
Concept
→ Mechanism
→ Trade-off
→ Failure
→ Scale
→ Evaluation / Verification
```

### 当前正式建设状态

| 模块 | Phase 3 状态 |
|---|---|
| Python | ✅ 既有完整系统教材 |
| FastAPI | 🟡 已有完整课程骨架，正文后续补齐 |
| AI Backend Engineering | 🟡 已有完整课程骨架，按 Bridge / Production 主线持续补齐 |
| MySQL | ✅ 第一版完成：23 章 + Review + Interview |
| Redis | ✅ 第一版完成：27 章 + Review + Interview |
| Vector DB | ✅ 第一版完成：23 章 + Review + Interview |
| LLM Foundation | ✅ 第一版完成：29 章 + Review + Interview |
| RAG | 🚧 **当前下一块 / 正在建设** |
| Agent Harness / Runtime | ⏳ RAG 后建设；额外结合 Claude Code / Codex 源码 |
| System Design | ⏳ 随前置模块成熟汇总 |

正式顺序：

```text
MySQL ✅
→ Redis ✅
→ Vector DB ✅
→ LLM Foundation ✅
→ RAG 🚧
→ Agent Harness / Runtime
→ System Design
```

### 模块完成后的强制同步清单

以后每完成一个一级模块，必须同时检查并同步：

1. 模块自身 `README.md`；
2. 根 `README.md`；
3. `roadmap/knowledge-map.md`；
4. 本文件 `research/questions/progress.md`；
5. 自动生成的 `research/analysis/README.md` 与其生成 Workflow / Script 是否仍使用最新口径；
6. `research/questions/module-index.md`；
7. 任何仍写着“下一块 / 待建设”的关联入口；
8. 最后重新核验 `docs / review / interview` 文件数量、连续编号与链接。

---

## Agent Harness 特殊规则

Agent Harness 的**面经统计层**只反映 `S001–S279` HUMAN-A 市场证据。

正式建设 Agent 教材时，还必须额外研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

成熟源码属于课程权威实现证据，用于补齐完整 Harness / Runtime 知识边界；**不得**反向改变 HUMAN-A `Source Count`。
