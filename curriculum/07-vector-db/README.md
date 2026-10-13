# Vector Database｜理解相似度、精确检索、近似索引与数据生命周期

[← LLM Foundation](../06-llm-foundation/README.md) · [课程目录](../README.md) · [Handbook](../../README.md) · [RAG →](../08-rag/README.md)

从向量比较和精确搜索开始，再讨论 ANN 索引、过滤、租户、分布式数据与生产取舍。

## 学习前提与目标

先了解 LLM Foundation 中的 Embedding 与 Reranker，区分向量产生与向量检索。

学完后应能理解相似度、精确检索、近似索引与数据生命周期。

## 学习顺序

1. [01｜向量数据库究竟负责什么](docs/01-VectorDB在AI应用中的职责.md)
2. [02｜向量空间与相似度：先把“近”说清楚](docs/02-VectorSpace与Similarity.md)
3. [03｜精确搜索与 ANN：先建立可核对的答案](docs/03-ExactSearch与ANN.md)
4. [04｜索引谱系：近似究竟发生在哪里](docs/04-ANN索引谱系.md)
5. [05｜HNSW：沿着图寻找近邻](docs/05-HNSW机制与调优.md)
6. [06｜IVF：先选区域，再找向量](docs/06-IVF原理.md)
7. [07｜量化与 PQ：用短编码近似距离](docs/07-Quantization与PQ.md)
8. [08｜索引选择：把机制放回工作负载](docs/08-IndexSelection.md)
9. [09｜向量数据建模：让结果找得到来源](docs/09-Vector数据建模.md)
10. [10｜元数据过滤：在允许的范围内找近邻](docs/10-MetadataFilter.md)
11. [11｜分区与多租户：数据放在哪，谁可以读](docs/11-Partition与TenantIsolation.md)
12. [12｜索引生命周期：写入、更新、删除与重建](docs/12-VectorIndex生命周期.md)
13. [13｜分布式检索：局部结果怎样组成全局答案](docs/13-分布式VectorDB.md)
14. [14｜性能与容量：用证据定位瓶颈](docs/14-性能容量与Production诊断.md)
15. [15｜产品与架构选择：先决定需要哪类能力](docs/15-产品与架构选型.md)
16. [16｜图数据库边界：相似、关系与完整系统](docs/16-GraphDB边界与系统设计.md)

## 学习与面试

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界；完成每章后，使用章末总结与自测检查是否能独立解释和推导。

面试准备集中在 [本知识域](../../interview/07-vector-db/README.md)：[高频面试题](../../interview/07-vector-db/01-高频面试题.md)、[易混易错点](../../interview/07-vector-db/02-易混易错点.md)与[面试速查](../../interview/07-vector-db/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
