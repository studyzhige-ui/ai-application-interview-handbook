# Curriculum｜十个正式知识模块

[↑ Handbook](../README.md) · [学习路线](../guide/learning-path.md) · [知识地图](../guide/knowledge-map.md) · [成熟系统源码](../products/README.md)

课程从Python语言能力开始，逐步进入接口、数据、后端可靠性和AI应用。目标是能理解机制、观察行为并独立组合，而不是背一张工具清单。

## 推荐学习顺序

**Python → FastAPI → MySQL → Redis → Backend → Vector DB → LLM Foundation → RAG → Agent → System Design**

目录中的数字是稳定标识，不要求按文件浏览器的字典序学习。模块职责与知识覆盖保持独立；学习先后可根据前置关系调整。完整进度安排见学习路线。

| 学习顺序 | 模块 | 本阶段建立的能力 |
|---:|---|---|
| 01 | [Python](01-python/README.md) | 理解名字、对象、函数、资源与并发执行。 |
| 02 | [FastAPI](02-fastapi/README.md) | 把Python能力变成可校验、可观测的网络接口。 |
| 03 | [MySQL](04-mysql/README.md) | 理解表、查询、约束、事务与持久事实。 |
| 04 | [Redis](05-redis/README.md) | 理解命令、缓存、短期状态及其边界。 |
| 05 | [Backend](03-backend-engineering/README.md) | 在数据库与缓存基础上组合幂等、可靠任务和跨系统恢复。 |
| 06 | [Vector DB](06-vector-db/README.md) | 理解相似度、精确检索、近似索引与生命周期。 |
| 07 | [LLM Foundation](07-llm-foundation/README.md) | 理解模型输入、注意力、生成、推理成本与适配。 |
| 08 | [RAG](08-rag/README.md) | 把外部材料变成可追溯、可评价的回答证据。 |
| 09 | [Agent](09-agent/README.md) | 组织动态执行、工具、上下文、记忆与恢复。 |
| 10 | [System Design](10-system-design/README.md) | 从需求和约束推导完整系统方案并验证取舍。 |

Backend置于MySQL、Redis之后，让事务、唯一约束、缓存与命令原子性先成为已知概念，再进入Outbox、幂等、任务恢复和一致性组合。FastAPI中的外部服务例子先用可替换的测试实现，不要求读者提前掌握这些内部机制。

进入Vector DB前，可先阅读[Embedding与Reranker的基础说明](07-llm-foundation/docs/09-Embedding与Reranker.md)中编码输入与向量表示的部分。理解“文档和查询如何变成可比较向量”即可，不要求先学习全部模型训练。遇到评测指标等尚未建立的扩展内容，可以按该模块正文的具体需求回看，不把它们当作此处额外门槛。

## 正文、回顾与实践分别负责什么

```text
README.md   模块任务、学习主线、入口和边界
docs/       首次系统学习的展开式正文
review/     第二遍总图与综合自测
interview/  口述、追问、易错点和速查
```

[Practice](../practice/README.md)与课程并行，让学习转成写代码、运行和调试。 [Products](../products/README.md)沿固定源码快照理解成熟系统，不作为第11个课程模块，也不以某个产品实现替代通用机制。

技术事实由[References](../references/README.md)支撑；[Market](../market/README.md)与[Interview](../interview/README.md)提供真实问法和复习权重。它们校准学习深度，不以热度替代必要前置。
