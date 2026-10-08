# Curriculum｜通用工程课程

[Handbook](../README.md) · [优秀产品学习](../products/README.md) · [编程与开发实践](../practice/README.md) · [面试准备](../interview/README.md)

从零建立最小完整的工程知识模型，再用真实问题决定学习深度。十个知识域按前置关系编号；课程正文承载连续主线，Review 帮助压缩回忆与迁移应用。

## 推荐学习顺序

Python → FastAPI → MySQL → Redis → Backend Engineering → LLM Foundation → Vector DB → RAG → Agent → System Design

| 顺序 | 入口 | 核心能力 |
|---|---|---|
| 01 | [Python](01-python/README.md) | 理解名字、对象、函数、资源与并发执行。 |
| 02 | [FastAPI](02-fastapi/README.md) | 把 Python 能力变成可校验、可观测的网络接口。 |
| 03 | [MySQL](03-mysql/README.md) | 理解关系表、查询、约束、索引、事务与持久事实。 |
| 04 | [Redis](04-redis/README.md) | 理解命令、缓存、短期状态、并发与恢复边界。 |
| 05 | [AI Backend Engineering](05-backend-engineering/README.md) | 组合幂等、可靠任务、容量控制和跨系统恢复。 |
| 06 | [LLM Foundation](06-llm-foundation/README.md) | 理解模型输入、注意力、生成、推理成本与模型适配。 |
| 07 | [Vector Database](07-vector-db/README.md) | 理解相似度、精确检索、近似索引与数据生命周期。 |
| 08 | [RAG](08-rag/README.md) | 把外部材料组织为可追溯、可评价的回答证据。 |
| 09 | [Agent](09-agent/README.md) | 组织模型判断、程序行动、状态恢复与交付验证。 |
| 10 | [System Design](10-system-design/README.md) | 从需求推导容量、状态、协作与故障方案。 |

MySQL 与 Redis 先建立事务、约束、缓存和命令原子性，Backend Engineering 再组合可靠任务与跨系统恢复。LLM Foundation 先解释 Embedding 的表示机制，Vector DB 再解释如何比较与检索这些向量，随后进入 RAG 与 Agent。

## 怎样使用

- 每个模块的 README 说明目标、前提与阅读入口。
- docs 保存首次系统学习的完整课程；先理解规则、过程与边界，再做自测。
- review 保存有实质内容的压缩复习与综合判断，和正文同步使用。
- [Practice](../practice/README.md)与课程并行，把理解转成独立实现和调试。
- [Products](../products/README.md)沿真实产品学习机制组合，不替代通用课程。
- [Market](../market/README.md)提供真实岗位与面试证据；[Interview](../interview/README.md)提供按知识域整理的面试学习材料。
