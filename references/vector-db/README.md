# Vector Database｜权威资料与版本边界

[← 课程入口](../../curriculum/06-vector-db/README.md) · [实验](../../curriculum/06-vector-db/labs/README.md)

本索引用来回答“这条机制或接口结论依据什么”，不是产品功能清单。教学推导、业务策略和人工构造数值不伪装成官方测试结果；正式面经只证明问题曾被问及，不能充当技术答案的来源。

## 版本基线

课程版本基线记录日期：2026-09-27。版本表集中在本页，正文只在具体行为受版本影响时标注条件。右列保留初版交付的运行范围，本次精修的复验单独记在[维护记录](../../guide/project/vector-db-reader-revision.md)；文档核验不等于产品部署或兼容性认证。

| 对象 | 课程目标与核验依据 | 初版交付记录的实际运行 |
|---|---|---|
| 数值与状态实验 | Python 3.11+；标准库算法，不依赖某个向量产品 | Python 3.13.5；结果见维护记录 |
| Faiss | 1.15.1，2026-09-16 正式发布；[Release](https://github.com/facebookresearch/faiss/releases/tag/v1.15.1) | 未安装，真实库实验跳过 |
| pgvector | 0.8.6，2026-07-29；[固定标签文档](https://github.com/pgvector/pgvector/blob/v0.8.6/README.md)、[Changelog](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md)；0.8.7 标为未发布 | 未运行 PostgreSQL/扩展；没有声明某一 PostgreSQL 服务端组合已验证 |
| Qdrant | 1.19.1，2026-09-04；[Release](https://github.com/qdrant/qdrant/releases/tag/v1.19.1) | 未启动服务；REST 实验跳过，不用 Local Mode 替代 |
| Milvus | 3.0.2，2026-09-20；[Release Notes](https://milvus.io/docs/release_notes.md)；2.6 系列仍有维护发布，不能把 3.0 正式版与 beta 混同 | 未部署；3.0.2 服务端与 Python SDK 的对应见官方版本表，本文不借文档核验冒充实测 |
| Elasticsearch、Neo4j | 核验日官方文档用于能力边界；不作为本模块可运行实验的固定版本 | 未运行；未逐项认证版本兼容性 |

在线 Wiki 和 `current` 文档会继续更新；只有固定标签才固定该份文档。升级运行环境时，重新核对差异并记录实际版本，不把本表的日期替换后沿用旧验收结果。开源服务与托管产品的配额、部署和功能开放情况分别核对。

<a id="responsibility"></a>
## 谁负责生成表示，谁负责存储与服务？

Faiss 定位于相似性搜索；pgvector 是 PostgreSQL 的向量扩展。对比其职责，有助于区分算法库与数据库服务，而非给产品排名。

[Faiss 官方项目说明](https://github.com/facebookresearch/faiss) · [pgvector 0.8.6](https://github.com/pgvector/pgvector/tree/v0.8.6)

<a id="metrics"></a>
## “分数”究竟是哪一个数学量？

核对 Faiss 平方 L2、内积与归一化；核对 pgvector 的余弦距离和负内积算子。数学排序关系可由正文公式推导，接口命名不能代替返回值定义。

[Faiss：距离语义](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances) · [pgvector：Querying](https://github.com/pgvector/pgvector/blob/v0.8.6/README.md#querying)

<a id="exact-ann"></a>
## 什么结果能作为 ANN 的精确对照？

Flat 是适合建立基准的实现。本文的过滤范围、空目标与并列处理是明确声明的评测约定，不宣称所有平台都采用相同口径。

[Faiss：选择索引](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index) · [Faiss：索引类型](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)

<a id="index-family"></a>
## 搜索范围与向量表示分别怎样改变？

比较 Flat、HNSW、IVF 与 PQ 的组织方式。索引表中的内存公式依对应表示与实现而定，不能直接当整个数据库的容量。

[Faiss：索引表与说明](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) · [Faiss：FAQ](https://github.com/facebookresearch/faiss/wiki/FAQ)

<a id="hnsw"></a>
## 图怎样搜索，参数约束的是哪一步？

原论文提供算法来源；hnswlib 参数说明用于核对具体实现中 ef、M 与 ef_construction 的含义。正文手工图只演示候选搜索，不是对某个产品建图结果的复现。

[HNSW 原论文入口](https://arxiv.org/abs/1603.09320) · [hnswlib 参数说明](https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md) · [Faiss：重复数据等边界](https://github.com/facebookresearch/faiss/wiki/FAQ)

<a id="ivf"></a>
## 何时能因探测全部列表而恢复精确距离？

核对 IVF 训练、添加与搜索的不同阶段，以及 IVF_FLAT 与压缩表示的区别。正文先用 L2 K-means 的“分配到最近中心、按组取均值”解释中心学习，再用另一个给定中心的例子观察区域漏搜。手算不代表 Faiss 的实际训练结果；真实索引召回由库实验验证。

[Faiss：K-means 的分配与中心更新](https://github.com/facebookresearch/faiss/wiki/FAQ#why-k-means) · [Faiss：入门与 IVF](https://github.com/facebookresearch/faiss/wiki/Getting-started) · [Faiss：全探测与压缩误差](https://github.com/facebookresearch/faiss/wiki/FAQ)

<a id="quantization"></a>
## PQ 的短编码和近似距离从哪里来？

索引说明用于核对压缩表示；FAQ 说明 K-means 在 IVF 与 PQ 中的作用，并区分候选遗漏和压缩误差。正文把子空间码本学习接在 IVF 中心学习之后；共享码本摊销与查表数值仍是可独立核算的教学计算。

[Faiss：压缩与各类索引](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) · [Faiss：FAQ](https://github.com/facebookresearch/faiss/wiki/FAQ)

<a id="selection"></a>
## 怎样把索引参数变成可比较的选择？

索引指南提供候选方向，不是跨版本、跨硬件的永久排行榜。正文门槛与演示测量表是明确标注的假设工作负载。

[Faiss：选择索引的考虑因素](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)

<a id="data-model"></a>
## 记录主键、向量、元数据和更新如何对应？

核对 Qdrant point 的 ID、vector、payload 和操作语义；区分模型意义上的稳定 ID 与数据库 API 的具体主键约束。正文逻辑 ID 与代际设计是应用策略，不是所有数据库内置字段。

[Qdrant：Points](https://qdrant.tech/documentation/manage-data/points/) · [Qdrant REST：Query points](https://api.qdrant.tech/api-reference/search/query-points)

<a id="filtering"></a>
## 过滤进入搜索的哪个阶段？

pgvector 0.8.6 文档说明近似索引过滤与迭代扫描；Elasticsearch 文档区分 kNN 内部 filter 与其他位置的后过滤。物理计划依产品、索引和数据选择性而变，不能用“前过滤”推断必定新建小索引。

[pgvector：Filtering / Iterative Index Scans](https://github.com/pgvector/pgvector/blob/v0.8.6/README.md#filtering) · [Elasticsearch：kNN query](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-knn-query) · [Qdrant：Search](https://qdrant.tech/documentation/search/search/)

<a id="multitenancy"></a>
## 逻辑布局能否代替身份授权？

官方多租户文档讨论共享集合、payload 条件与分层分片；这些布局不证明应用的按 ID 读写、导出和缓存已经鉴权。具体租户策略必须经过自己的隔离测试。

[Qdrant：Multitenancy](https://qdrant.tech/documentation/manage-data/multitenancy/)

<a id="lifecycle"></a>
## 操作确认、查询可见、删除与恢复如何区别？

Qdrant Points 文档用于核对 wait、幂等及条件更新边界；Milvus 一致性文档用于核对查询视图。本文版本防覆盖、快照加增量与回滚流程是工程推导，未通过真实跨系统集成实验。

[Qdrant：Points 的更新和同步语义](https://qdrant.tech/documentation/manage-data/points/) · [Milvus：Consistency](https://milvus.io/docs/consistency.md) · [Milvus：Release Notes](https://milvus.io/docs/release_notes.md)

<a id="distributed"></a>
## 查询、增量与历史数据由哪些层协作？

正文第 13 章先解释新写入、历史查询、后台维护各自处理什么，再在[就地选读案例](../../curriculum/06-vector-db/docs/13-分布式VectorDB.md#milvus-example)中对应 Milvus 的组件。局部 Top-K 的证明是数学推导，不依赖记住某个产品的进程名称。

**产品边界选读：External Collection（外部集合）。** Milvus 3.0 发布线支持面向外部湖表的查询方式，可以为外部数据建立向量搜索入口，而不要求先将整份原始数据复制进内部集合。因此“数据库负责检索记录”是职责描述，不应扩写成“所有产品模式都必须自行保存原始数据”。是否需要这项能力取决于数据原本存放的位置；连接器、支持格式和刷新过程按官方版本核对，不作为分布式 Top-K 自测的前置。

[Milvus：Architecture Overview](https://milvus.io/docs/architecture_overview.md) · [Milvus：3.0 正式发布说明](https://milvus.io/docs/release_notes.md) · [Faiss：分片索引与压缩计分问题](https://github.com/facebookresearch/faiss/wiki/FAQ)

<a id="performance"></a>
## 容量公式算的是哪一份资源？

Faiss 索引表可以核对特定表示的存储组成；整库 RAM、缓存、构建峰值与集群副本必须按实际布局另外计算。正文时间和容量案例是单位明确的推导或模拟数据。

[Faiss：Index storage](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) · [Faiss：FAQ 的批量与线程边界](https://github.com/facebookresearch/faiss/wiki/FAQ)

<a id="products"></a>
## 怎样核验能力形态，而不是背品牌印象？

先查定位，再查具体版本和查询限制。SQL 可表达不代表必有高效计划；库能保存索引文件也不等于提供完整数据库耐久性。托管平台不自动与对应开源版功能相同。

[Faiss](https://github.com/facebookresearch/faiss) · [pgvector](https://github.com/pgvector/pgvector/tree/v0.8.6) · [Milvus](https://milvus.io/docs/architecture_overview.md) · [Qdrant](https://qdrant.tech/documentation/manage-data/points/) · [Elasticsearch 向量搜索](https://www.elastic.co/docs/solutions/search/vector/knn)

<a id="graph-boundary"></a>
## 相似性图和业务知识图有什么不同？

Neo4j 文档证明图产品也可提供向量索引，不能把存储产品能力与两种查询问题混同。本文实体关系案例用于解释建模边界，不是已验证的 GraphRAG 系统。

[Neo4j：Vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)

## 使用资料时的边界

官方文档可能同时存在旧示例、新能力和特定版本默认值。核验时先确认页面适用版本，再判断是否影响正文结论；新增功能不自动要求新增课程章节。技术事实附近保留引用，综合定位使用本索引。

[模块维护记录](../../guide/project/vector-db-reader-revision.md)单独记录本轮真实阅读、执行与未执行项，不借版本表或引用数量声明全部验收通过。
