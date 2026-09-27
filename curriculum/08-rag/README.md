# RAG｜从外部知识到有依据的回答

[← LLM Foundation](../07-llm-foundation/README.md) · [↑ Handbook](../../README.md) · [学习路线](../../guide/learning-path.md) · [Agent →](../09-agent/README.md)

RAG（检索增强生成）把外部知识中适用、允许读取且能够回溯的内容提供给模型，用于回答具体问题。本模块沿语料处理、检索、证据组装、评测和持续更新建立完整理解，面向 AI Application 与 Agent 工程岗位的学习和实践。

<a id="prerequisites"></a>
## 学习前提与模块边界

开始前需要理解文本、列表、函数和基本错误处理；了解 Embedding 把对象编码成向量，以及模型输入长度有限。可以从 [LLM Foundation 的 Embedding 与 Reranker](../07-llm-foundation/docs/09-Embedding与Reranker.md) 回看最小模型。正文会就地解释当前机制需要的前提，不要求先背完所有生产组件。

向量索引的内部结构、近似搜索和过滤执行在 [Vector DB](../06-vector-db/README.md) 深入学习；模型内部编码与训练归 LLM Foundation；跨步骤的工具执行、持久状态和恢复归 [Agent](../09-agent/README.md)。RAG 负责把这些能力围绕“得到适用证据并可靠回答”组合起来。完整企业部署取舍由 [System Design](../10-system-design/README.md) 承接。

全仓学习顺序以 [learning-order.json](../../guide/learning-order.json) 为准，目录前缀保留稳定身份，不等于必须按数字学习。本模块的实际正文顺序为下表顺序。

## 正文主线

各章使用同一组虚构北辰云政策，逐步回答“购买 10 天、已经开通专属资源的标准版订单，能否按普通规则退款”。先理解正常路径，再引入版本、例外、权限、失败和规模；数字、排名与政策均为教学假设。

| 顺序 | 知识章 | 这一章解决的问题 |
|---:|---|---|
| 01 | [RAG 职责与完整链路](docs/01-RAG职责与完整链路.md) | 为什么需要外部证据，RAG 与模型、数据库、业务动作怎样分工？ |
| 02 | [语料治理](docs/02-CorpusGovernance.md) | 哪份文档可信、有效、允许读取，重复与版本如何区分？ |
| 03 | [文档解析](docs/03-DocumentProcessing.md) | 页面外观怎样恢复成保留顺序、表格和来源的内容？ |
| 04 | [切分设计](docs/04-ChunkingDesign.md) | 怎样避免把规则、条件和例外切散，参数怎样验证？ |
| 05 | [块之间的关系](docs/05-AdvancedChunkStructure.md) | 小块如何找得准，又能补齐父块、邻居与上下文？ |
| 06 | [查询规划](docs/06-QueryPlanning.md) | 何时改写、拆解、澄清，哪些条件不能被改写掉？ |
| 07 | [多路检索与融合](docs/07-RetrievalStack.md) | 语义与词项如何互补，多路排名怎样实际融合？ |
| 08 | [重排与候选预算](docs/08-Rerank与CandidateBudget.md) | 重排为何可能变差，候选与上下文预算怎样区分？ |
| 09 | [证据交付](docs/09-EvidenceDelivery.md) | 怎样选择证据、分配输入长度，并检查引用支持？ |
| 10 | [检索评测](docs/10-RetrievalEvaluation.md) | Recall、MRR、NDCG 等指标的分母与边界是什么？ |
| 11 | [端到端质量](docs/11-EndToEndQualityEngineering.md) | 怎样定位第一处证据丢失，并证明优化有效？ |
| 12 | [更新、权限与回滚](docs/12-ProductionGovernance.md) | 如何避免旧任务覆盖新版本，回滚为何不能恢复旧授权？ |
| 13 | [规模、成本与可观测性](docs/13-ScaleCostObservability.md) | 怎样处理积压、配额、尾延迟、缓存、成本和追踪？ |
| 14 | [GraphRAG 与 Agentic RAG](docs/14-GraphRAG与AgenticRAG.md) | 何时需要图结构，何时需要受控地继续搜索？ |

## 学习、练习与回看

第一遍沿正文顺序阅读。每章先解释一个具体问题，再给机制、例子、边界与小结；面试回答用于组织已经理解的内容，自测任务在答案之外完整显示。先独立推导，再打开提示或答案。

| 入口 | 用途 |
|---|---|
| [机制实验](examples/README.md) | 用无外部依赖的确定性实验核对切分、排名、指标与版本状态；不冒充真实模型服务 |
| [Review 与综合自测](review/README.md) | 第二遍重新画出知识流、证据漏斗与失败定位过程 |
| [高频面试题](interview/高频面试题.md) | 沿连续追问练习有条件、有过程的表达 |
| [面试易错点](interview/面试易错点.md) | 纠正绝对化、混淆阶段与忽略失败边界的说法 |
| [面试前速查表](interview/面试前速查表.md) | 快速唤起机制，需要推导时返回正文 |
| [RAG 权威资料](../../references/rag/README.md) | 按具体问题查技术依据与适用版本 |

机制实验使用 Python 标准库，只是示例选择。本模块不绑定某个 RAG 框架、数据库或模型供应商；具体服务的 API、默认值与运行行为必须按部署版本另行验证。

## 面经与技术证据

[Canonical RAG](../../interview/canonical/rag.md) 保存正式面经的归一化问法与冻结统计；[Market](../../market/README.md) 保存持续收录的原始证据。它们用于校准问题、深度和边界，不替代技术事实，也不决定初学者的学习顺序。

阅读范围、正式条目去向、版本核验、已运行检查与未验证项集中记录在 [RAG 修订记录](../../guide/project/rag-reader-revision.md)。

下一环：[Agent](../09-agent/README.md)。
