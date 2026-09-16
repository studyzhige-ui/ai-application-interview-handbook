# Curriculum & Research Progress｜当前正式状态

> **2026-09-16更新：** Agent为16章分层重构版，全仓库177篇正文。旧版深度与终局审计为历史记录；本次验证范围为结构、链接、迁移覆盖和证据不变性，详见既有质量记录。


[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Knowledge Map](../../roadmap/knowledge-map.md) · [Learning Path](../../roadmap/learning-path.md)

> **Repository-first：仓库当前文件高于历史聊天总结。**

## Frozen Research Baseline ✅

```text
HUMAN-A                    279 / 279
ACTIVE Canonical          235 / 235
Mapped Sources            278
VALID-UNMAPPED              1（S271）
Unexpected uncovered        0
Source Count mismatch       0
```

Phase 1 Canonicalization ✅ · Phase 2A Global Merge/Split ✅ · Phase 2B Market Analysis ✅

## Phase 3 Curriculum Build ✅

| # | Module | Curriculum | Canonical | Status |
|---:|---|---:|---:|---|
| 01 | [Python Foundation](../../python/README.md) | 13 | 15 | ✅ |
| 02 | [FastAPI](../../fastapi/README.md) | 16 | 4 | ✅ |
| 03 | [AI Backend Engineering](../../backend-engineering/README.md) | 22 | 39 | ✅ |
| 04 | [MySQL](../../mysql/README.md) | 23 | 26 | ✅ |
| 05 | [Redis](../../redis/README.md) | 24 | 19 | ✅ |
| 06 | [Vector Database](../../vector-db/README.md) | 16 | 12 | ✅ |
| 07 | [LLM Foundation（应用工程深度）](../../llm-foundation/README.md) | 14 | 23 | ✅ |
| 08 | [RAG](../../rag/README.md) | 14 | 29 | ✅ |
| 09 | [Agent](../../agent/README.md) | 16 | 44 | ✅ |
| 10 | [System Design](../../system-design/README.md) | 19 | 24 | ✅ |

十个正式一级模块第一版系统教材全部完成；Foundation 也已完成。

**v1.0 Final Quality Audit：✅ PASS。** 177/184 Curriculum Markdown、235/235 Canonical、仓库内链接、Mermaid、跨模块 Ownership、术语与版本敏感事实风险审计均已完成；详见 [`../../roadmap/final-quality-audit.md`](../../roadmap/final-quality-audit.md)。

## Phase 4 Learning & Interview Usage Layer

| Layer | Status | Entry |
|---|---|---|
| 正式学习路线 | ✅ | [13 周标准 / 8 周加速 / 14 天冲刺](../../roadmap/learning-path.md) |
| Bridge Labs | ⏳ | 下一阶段：把多个模块组合成真实工程任务 |
| Cross-module Mock Interview | ⏳ | 下一阶段：用真实连续追问训练跨模块迁移 |

学习路线仍遵守：第一次学习 100% 按 Curriculum 顺序；HUMAN-A Heat 只进入 Review / Interview 权重。

## 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度。**

> **Canonical / Capability / Curriculum Markdown 使用不同粒度。**

## 模块完成后的强制同步清单

每次新增、重组或更新一个一级模块，都必须同步核验：

1. 模块 `README.md`；
2. 模块 `review/README.md` 与 Interview 入口；
3. 根 `README.md`；
4. `roadmap/knowledge-map.md`；
5. 本文件与 `module-index.md`；
6. `research/questions/README.md`；
7. 自动生成 `research/analysis/README.md` 的生成源；
8. `roadmap/documentation-style-guide.md` 的统一格式；
9. README 本地链接、章节数量与旧状态描述。

后续工作进入**使用层建设与质量维护**；不再存在未撰写的一级模块。
