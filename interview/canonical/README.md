# Canonical Questions｜真人面试能力归一化层

[← Market 首页](../../market/README.md) · [↑ Handbook 总目录](../../README.md) · [Module Index](module-index.md) · [冻结覆盖](progress.md)

> Canonical Question 只允许由 **HUMAN-A 真人高质量第一人称面经**产生市场证据。官方资料、源码、论文可以校准课程技术边界，但不能创建频率或提高 Source Count。

## 统计基线（Frozen Baseline）

```text
HUMAN-A            S001–S279
ACTIVE Canonical   235
Mapped Sources     278
VALID-UNMAPPED       1（S271）
```

## 十板块 Ownership（知识主责归属）

| Module | Canonical | Entry |
|---|---:|---|
| [Python Foundation](python.md) | 15 | [教材 README](../../curriculum/01-python/README.md) |
| [FastAPI](fastapi.md) | 4 | [教材 README](../../curriculum/02-fastapi/README.md) |
| [MySQL](mysql.md) | 26 | [教材 README](../../curriculum/03-mysql/README.md) |
| [Redis](redis.md) | 19 | [教材 README](../../curriculum/04-redis/README.md) |
| [AI Backend Engineering](ai-backend-engineering.md) | 39 | [教材 README](../../curriculum/05-backend-engineering/README.md) |
| [LLM Foundation（应用工程深度）](llm-foundation.md) | 23 | [教材 README](../../curriculum/06-llm-foundation/README.md) |
| [Vector Database](vector-db.md) | 12 | [教材 README](../../curriculum/07-vector-db/README.md) |
| [RAG](rag.md) | 29 | [教材 README](../../curriculum/08-rag/README.md) |
| [Agent](agent-harness.md) | 44 | [教材 README](../../curriculum/09-agent/README.md) |
| [System Design](system-design.md) | 24 | [教材 README](../../curriculum/10-system-design/README.md) |

## 四种粒度

```text
Canonical Question = 面试最小独立追问单元
Capability         = 更细工程机制
Curriculum Block   = 完整教材认知闭环
Interview Drill    = 训练时可以再次细分的真实问法
```

因此 Canonical 数量不能换算成正文数量；现有课程范围与推荐顺序见[学习资源索引](../../guide/navigation-index.md)。

## 质量与结构入口

- [Content Depth Audit](../../guide/audits/content-depth-audit.md)：正文深度与验收口径；
- [Final Quality Audit](../../guide/audits/final-quality-audit.md)：全仓库质量审计；
- [Terminology Glossary](../../guide/terminology-glossary.md)：跨模块术语与边界。

## 主要入口

- [schema.md](schema.md)：Canonical 字段与证据规则；
- [module-index.md](module-index.md)：Ownership ↔ Curriculum；
- [progress.md](progress.md)：冻结基线与覆盖记录；
- [global-audit.md](global-audit.md)：Merge / Split / Reassignment；
- [Market Analysis](../../market/analysis/README.md)：自动统计层；
- [Verified Follow-up Chains](../../market/analysis/follow-up-chains.md)：人工回读原始流程后的追问链。
