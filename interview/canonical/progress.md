# Curriculum & Canonical Progress｜正式状态

[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Knowledge Map](../../guide/knowledge-map.md) · [Learning Path](../../guide/learning-path.md) · [Market](../../market/README.md)

> **Repository-first：当前仓库文件高于历史聊天、旧 PR 描述与阶段性摘要。**

## 1. Market 与 Canonical 使用不同时间口径

```text
Market HUMAN-A
= Continuous Monitoring
= 当前总量与下一 Source ID 以 market/README.md / monitoring/inbox.md 为准

Frozen Canonical Baseline
= S001–S279
= 235 ACTIVE Canonical
= 278 Mapped + 1 VALID-UNMAPPED（S271）

S280+
= 合法 Market Evidence
= 等待 periodic Canonical review
= 在 review 完成前不改变 Frozen Source Count / Frequency
```

截至 2026-09-19，Market 正式库已到 `S001–S288 / 29 Batch`；这一数字用于描述当前证据库，不等于 Canonical 已扩展到 S288。

## 2. Frozen Canonical Baseline ✅

```text
HUMAN-A in baseline        279 / 279
ACTIVE Canonical          235 / 235
Mapped Sources            278
VALID-UNMAPPED              1（S271）
Unexpected uncovered        0
Source Count mismatch       0
```

Phase 1 Canonicalization ✅ · Phase 2A Global Merge/Split ✅ · Phase 2B Frozen Market Analysis ✅

## 3. Curriculum Build ✅

| # | Module | Curriculum | Canonical | Status |
|---:|---|---:|---:|---|
| 01 | [Python Foundation](../../curriculum/01-python/README.md) | 13 | 15 | ✅ |
| 02 | [FastAPI](../../curriculum/02-fastapi/README.md) | 16 | 4 | ✅ |
| 03 | [AI Backend Engineering](../../curriculum/03-backend-engineering/README.md) | 22 | 39 | ✅ |
| 04 | [MySQL](../../curriculum/04-mysql/README.md) | 19 | 26 | ✅ |
| 05 | [Redis](../../curriculum/05-redis/README.md) | 18 | 19 | ✅ |
| 06 | [Vector Database](../../curriculum/06-vector-db/README.md) | 16 | 12 | ✅ |
| 07 | [LLM Foundation（应用工程深度）](../../curriculum/07-llm-foundation/README.md) | 14 | 23 | ✅ |
| 08 | [RAG](../../curriculum/08-rag/README.md) | 14 | 29 | ✅ |
| 09 | [Agent](../../curriculum/09-agent/README.md) | 24 | 44 | ✅ |
| 10 | [System Design](../../curriculum/10-system-design/README.md) | 19 | 24 | ✅ |

**Curriculum total：175 blocks。**

历史 v1.0 审计快照保留在 [Audits History](../../guide/audits/history/README.md)；当前质量状态以 [Final Quality Audit](../../guide/audits/final-quality-audit.md) 为准。Agent 23→24 的修订与核验范围见 [Agent Reader Revision](../../guide/project/agent-reader-revision.md)。

## 4. Learning & Interview Usage Layer

| Layer | Status | Entry |
|---|---|---|
| 正式学习路线 | ✅ | [13 周标准 / 8 周加速 / 14 天冲刺](../../guide/learning-path.md) |
| Coding / Tooling Practice | ✅ | [Practice](../../practice/README.md) |
| Bridge Labs | ⏳ | 待建设：把多个模块组合成真实工程任务 |
| Cross-module Mock Interview | ⏳ | 待建设：用真实连续追问训练跨模块迁移 |

第一次系统学习按 Curriculum 知识依赖顺序进行；HUMAN-A Heat 只调整 Review / Interview 权重。

## 5. 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度。**

> **Canonical / Capability / Curriculum Markdown 使用不同粒度。**

## 6. 强制同步清单

每次新增、重组或更新一个一级模块，至少核验：

1. 模块 `README.md`、`review/README.md` 与模块 Interview；
2. 根 `README.md`、`guide/knowledge-map.md`、`guide/learning-path.md`；
3. 本文件、`module-index.md`、`interview/canonical/README.md`；
4. `guide/documentation-style-guide.md` 与相关 Audits / Project Records；
5. 自动生成 `market/analysis/` 文件的**生成源**；
6. 本地 Markdown 链接、实际章节数量、Frozen / Current / Historical 时间语义；
7. 运行中的自动任务是否仍引用有效目录。

后续工作重点是使用层建设、Market 持续监测、periodic Canonical review 与质量维护；不存在未撰写的正式一级 Curriculum 模块。
