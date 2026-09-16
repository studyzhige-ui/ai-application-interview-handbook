# Canonical Questions｜真人面试能力归一化层

[← Research 首页](../README.md) · [↑ Handbook 总目录](../../README.md) · [Module Index](module-index.md) · [Progress](progress.md)

> Canonical Question 只允许由 **HUMAN-A 真人高质量第一人称面经**产生市场证据。官方资料、源码、论文可以校准课程技术边界，但不能创建频率或提高 Source Count。

## Frozen Baseline

```text
HUMAN-A            S001–S279
ACTIVE Canonical   235
Mapped Sources     278
VALID-UNMAPPED       1（S271）
```

## 十板块 Ownership

| Module | Canonical | Curriculum | Entry |
|---|---:|---:|---|
| [Python Foundation](python.md) | 15 | 13 | [教材 README](../../python/README.md) |
| [FastAPI](fastapi.md) | 4 | 16 | [教材 README](../../fastapi/README.md) |
| [AI Backend Engineering](ai-backend-engineering.md) | 39 | 22 | [教材 README](../../backend-engineering/README.md) |
| [MySQL](mysql.md) | 26 | 23 | [教材 README](../../mysql/README.md) |
| [Redis](redis.md) | 19 | 24 | [教材 README](../../redis/README.md) |
| [Vector Database](vector-db.md) | 12 | 16 | [教材 README](../../vector-db/README.md) |
| [LLM Foundation（应用工程深度）](llm-foundation.md) | 23 | 14 | [教材 README](../../llm-foundation/README.md) |
| [RAG](rag.md) | 29 | 14 | [教材 README](../../rag/README.md) |
| [Agent](agent-harness.md) | 44 | 16 | [教材 README](../../agent/README.md) |
| [System Design](system-design.md) | 24 | 19 | [教材 README](../../system-design/README.md) |

## 四种粒度

```text
Canonical Question = 面试最小独立追问单元
Capability         = 更细工程机制
Curriculum Block   = 完整教材认知闭环
Interview Drill    = 训练时可以再次细分的真实问法
```

因此 235 道 Canonical 不等于 177 篇正文。

**v1.0 Final Quality Audit：✅ PASS。** 正文深度见 [`../../roadmap/content-depth-audit.md`](../../roadmap/content-depth-audit.md)，全仓库终局结论见 [`../../roadmap/final-quality-audit.md`](../../roadmap/final-quality-audit.md)，跨模块术语边界见 [`../../roadmap/terminology-glossary.md`](../../roadmap/terminology-glossary.md)。

## 主要入口

- [schema.md](schema.md)：Canonical 字段与证据规则；
- [module-index.md](module-index.md)：Ownership ↔ Curriculum；
- [progress.md](progress.md)：当前研究 / 教材状态；
- [global-audit.md](global-audit.md)：Merge / Split / Reassignment；
- [Market Analysis](../analysis/README.md)：自动统计层；
- [Verified Follow-up Chains](../analysis/follow-up-chains.md)：人工回读原始流程后的追问链。
