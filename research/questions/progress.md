# Curriculum & Research Progress｜当前正式状态

[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Knowledge Map](../../roadmap/knowledge-map.md)

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
| 09 | [Agent Harness / Runtime](../../agent-harness/README.md) | 23 | 44 | ✅ |
| 10 | [System Design](../../system-design/README.md) | 19 | 24 | ✅ |

十个正式一级模块第一版系统教材全部完成；Foundation 也已完成。

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

后续工作进入**全仓库质量维护、复习路线与面试训练**，不再存在未撰写的一级模块。
