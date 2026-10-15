# RAG｜把外部材料组织为可追溯、可评价的回答证据

[← Vector Database](../07-vector-db/README.md) · [课程目录](../README.md) · [Handbook](../../README.md) · [Agent →](../09-agent/README.md)

从完整证据链进入语料、切分、查询、召回、重排、证据交付、评测与生产治理。

<a id="prerequisites"></a>
## 学习前提与目标

先理解模型、Embedding、重排和向量检索；本模块组合这些能力，评估端到端证据质量。

学完后应能把外部材料组织为可追溯、可评价的回答证据。

## 学习顺序

1. [01｜RAG 职责与完整链路：把外部事实变成有依据的回答](docs/01-RAG职责与完整链路.md)
2. [02｜语料治理：先确定哪些知识可信、有效、可见](docs/02-CorpusGovernance.md)
3. [03｜文档解析：从页面外观恢复可检索的内容](docs/03-DocumentProcessing.md)
4. [04｜切分设计：怎样保留一个问题需要的完整语义](docs/04-ChunkingDesign.md)
5. [05｜块之间的关系：小块检索，大块补全](docs/05-AdvancedChunkStructure.md)
6. [06｜查询规划：把用户的话变成可执行的检索请求](docs/06-QueryPlanning.md)
7. [07｜多路检索与融合：让语义和词项互相补位](docs/07-RetrievalStack.md)
8. [08｜重排与候选预算：把有限算力用在值得阅读的证据上](docs/08-Rerank与CandidateBudget.md)
9. [09｜证据交付：从候选片段到可追溯的答案](docs/09-EvidenceDelivery.md)
10. [10｜检索评测：分数到底衡量了什么](docs/10-RetrievalEvaluation.md)
11. [11｜端到端质量：用证据定位失败，再证明改动有效](docs/11-EndToEndQualityEngineering.md)
12. [12｜更新、权限与回滚：让用户看到正确版本的合法知识](docs/12-ProductionGovernance.md)
13. [13｜规模、成本与可观测性：让链路能持续运行](docs/13-ScaleCostObservability.md)
14. [14｜GraphRAG 与 Agentic RAG：何时需要结构，何时需要继续搜索](docs/14-GraphRAG与AgenticRAG.md)

## 学习与面试

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界；完成每章后，使用章末总结与自测检查是否能独立解释和推导。

面试准备集中在 [本知识域](../../interview/08-rag/README.md)：[高频面试题](../../interview/08-rag/01-高频面试题.md)、[易混易错点](../../interview/08-rag/02-易混易错点.md)与[面试速查](../../interview/08-rag/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
