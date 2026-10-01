# Curriculum｜十个正式知识模块

[↑ Handbook](../README.md) · [学习路线](../guide/learning-path.md) · [知识地图](../guide/knowledge-map.md) · [成熟系统源码](../products/README.md)

课程从Python语言能力开始，逐步进入接口、数据、后端可靠性和AI应用。目标是能理解机制、观察行为并独立组合，而不是背一张工具清单。

## 推荐学习顺序

**Python → FastAPI → MySQL → Redis → Backend → LLM Foundation → Vector DB → RAG → Agent → System Design**

目录编号、正文阅读顺序与前后导航保持一致。默认代码环境已就绪；示例用于解释知识，可选阅读建议集中在学习路线。

| 学习顺序 | 模块 | 本阶段建立的能力 |
|---:|---|---|
| 01 | [Python](01-python/README.md) | 理解名字、对象、函数、资源与并发执行。 |
| 02 | [FastAPI](02-fastapi/README.md) | 把Python能力变成可校验、可观测的网络接口。 |
| 03 | [MySQL](03-mysql/README.md) | 理解表、查询、约束、事务与持久事实。 |
| 04 | [Redis](04-redis/README.md) | 理解命令、缓存、短期状态及其边界。 |
| 05 | [Backend](05-backend-engineering/README.md) | 在数据库与缓存基础上组合幂等、可靠任务和跨系统恢复。 |
| 06 | [LLM Foundation](06-llm-foundation/README.md) | 理解模型输入、注意力、生成、推理成本与适配。 |
| 07 | [Vector DB](07-vector-db/README.md) | 理解相似度、精确检索、近似索引与生命周期。 |
| 08 | [RAG](08-rag/README.md) | 把外部材料变成可追溯、可评价的回答证据。 |
| 09 | [Agent](09-agent/README.md) | 沿模型判断、程序行动、结果回填与验收组织工具、信息、安全和恢复。 |
| 10 | [System Design](10-system-design/README.md) | 从用户动作与完成条件推导容量、状态和协作，并在条件变化后修正方案。 |

Backend置于MySQL、Redis之后，让事务、唯一约束、缓存与命令原子性先成为已知概念，再进入Outbox、幂等、任务恢复和一致性组合。FastAPI中的外部服务例子先用可替换的测试实现，不要求读者提前掌握这些内部机制。

LLM 先建立模型计算与 Embedding 表示，Vector DB 再讲向量的比较、索引和维护，RAG 随后组合检索与回答。每个模块在自身范围内完整解释必要概念。

## 正文、回顾与实践分别负责什么

```text
README.md   模块任务、学习主线、入口和边界
docs/       首次系统学习的展开式正文
review/     第二遍总图与综合自测
interview/  口述、追问、易错点和速查
```

[Practice](../practice/README.md)与课程并行，让学习转成写代码、运行和调试。 [Products](../products/README.md)沿固定源码快照理解成熟系统，不作为第11个课程模块，也不以某个产品实现替代通用机制。

Agent Review 从任务过程回看工具、取消和恢复；System Design Review 从整体方案回看容量、状态和取舍。已有推演和例子均可按需参考，不承担课程结业验收。

技术事实由[References](../references/README.md)支撑；[Market](../market/README.md)与[Interview](../interview/README.md)提供真实问法和复习权重。它们校准学习深度，不以热度替代必要前置。
