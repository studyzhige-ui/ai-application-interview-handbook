# 学习资源索引｜按实际内容导航

[← Handbook](../README.md) · [学习路线](learning-path.md) · [知识地图](knowledge-map.md)

模块顺序来自 `learning-order.json`，章节数量来自正式正文文件；同一正文的 Notebook、实验和渲染版本不重复计数。

## Curriculum：10 个模块，175 篇正文

| 学习顺序 | 模块 | 正文 | 回顾、面试与实践 |
|---:|---|---:|---|
| 01 | [Python](../curriculum/01-python/README.md) | 13 | [review](../curriculum/01-python/review/README.md) · [interview](../curriculum/01-python/interview) |
| 02 | [FastAPI](../curriculum/02-fastapi/README.md) | 16 | [review](../curriculum/02-fastapi/review/README.md) · [interview](../curriculum/02-fastapi/interview) · [examples](../curriculum/02-fastapi/examples/README.md) |
| 03 | [MySQL](../curriculum/04-mysql/README.md) | 19 | [review](../curriculum/04-mysql/review/README.md) · [interview](../curriculum/04-mysql/interview) · [examples](../curriculum/04-mysql/examples/README.md) |
| 04 | [Redis](../curriculum/05-redis/README.md) | 18 | [review](../curriculum/05-redis/review/README.md) · [interview](../curriculum/05-redis/interview) · [examples](../curriculum/05-redis/examples/README.md) |
| 05 | [Backend](../curriculum/03-backend-engineering/README.md) | 22 | [review](../curriculum/03-backend-engineering/review/README.md) · [interview](../curriculum/03-backend-engineering/interview) · [examples](../curriculum/03-backend-engineering/examples/README.md) |
| 06 | [Vector DB](../curriculum/06-vector-db/README.md) | 16 | [review](../curriculum/06-vector-db/review/README.md) · [interview](../curriculum/06-vector-db/interview) · [labs](../curriculum/06-vector-db/labs/README.md) |
| 07 | [LLM Foundation](../curriculum/07-llm-foundation/README.md) | 14 | [review](../curriculum/07-llm-foundation/review/README.md) · [interview](../curriculum/07-llm-foundation/interview) · [labs](../curriculum/07-llm-foundation/labs/README.md) |
| 08 | [RAG](../curriculum/08-rag/README.md) | 14 | [review](../curriculum/08-rag/review/README.md) · [interview](../curriculum/08-rag/interview) · [examples](../curriculum/08-rag/examples/README.md) |
| 09 | [Agent](../curriculum/09-agent/README.md) | 24 | [review](../curriculum/09-agent/review/README.md) · [interview](../curriculum/09-agent/interview) |
| 10 | [System Design](../curriculum/10-system-design/README.md) | 19 | [review](../curriculum/10-system-design/review/README.md) · [interview](../curriculum/10-system-design/interview) |

## Products：固定快照中的系统实践

| 模块 | 专题正文 | 来源边界 |
|---|---:|---|
| [Claude Code](../products/agent/claude-code/README.md) | 4 | 学习用私有镜像，需访问权限；不等同于官方完整仓库。 |
| [Codex](../products/agent/codex/README.md) | 4 | 固定源码快照；不代表全部环境已运行验证。 |
| [DeepSeek Harness](../products/agent/deepseek-harness/README.md) | 4 | 固定源码快照；不代表全部环境已运行验证。 |
| [DeerFlow 2.0](../products/agent/deer-flow/README.md) | 4 | 固定源码快照；不代表全部环境已运行验证。 |

## 正文标题与实际阅读顺序

顺序优先读取模块 README 的完整目录表；不会被更早的先修链接或文件名字典序改变。

<details>
<summary>Python · 13 篇</summary>

1. [01. Python 基础、对象模型与语言选择](../curriculum/01-python/docs/01-python基础与对象模型.md)
2. [02. 核心数据类型、容器、Hash 与切片成本](../curriculum/01-python/docs/02-核心数据类型与容器.md)
3. [03. 可变对象、对象身份与深浅拷贝](../curriculum/01-python/docs/03-可变对象-对象身份-深浅拷贝.md)
4. [04. 函数、参数、作用域与闭包](../curriculum/01-python/docs/04-函数-参数-作用域-闭包.md)
5. [05. Lambda、推导式与常用内置函数](../curriculum/01-python/docs/05-lambda-推导式-常用内置函数.md)
6. [06. 迭代器、生成器与 yield](../curriculum/01-python/docs/06-迭代器-生成器-yield.md)
7. [07. 装饰器与上下文管理器](../curriculum/01-python/docs/07-装饰器-上下文管理器.md)
8. [08. 面向对象、Duck Typing、Protocol 与魔术方法](../curriculum/01-python/docs/08-面向对象-魔术方法.md)
9. [09. 异常、文件、模块与导入](../curriculum/01-python/docs/09-异常-文件-模块与导入.md)
10. [10. 结构化数据、JSON 与校验](../curriculum/01-python/docs/10-结构化数据-JSON与校验.md)
11. [11. 内存管理、垃圾回收与 GIL](../curriculum/01-python/docs/11-内存管理-垃圾回收-GIL.md)
12. [12. 线程、进程、协程与 async/await](../curriculum/01-python/docs/12-线程-进程-协程-async-await.md)
13. [13. 常见数据结构与复杂度](../curriculum/01-python/docs/13-常见数据结构与复杂度.md)

配套：[review](../curriculum/01-python/review/README.md)

配套：[interview](../curriculum/01-python/interview)

</details>

<details>
<summary>FastAPI · 16 篇</summary>

1. [01｜从一个可访问的接口理解请求与响应](../curriculum/02-fastapi/docs/01-FastAPI职责与ASGI请求链路.md)
2. [02｜路由与参数：请求怎样变成函数输入](../curriculum/02-fastapi/docs/02-Routing与APIContract.md)
3. [03｜数据契约：校验输入、限制输出、解释错误](../curriculum/02-fastapi/docs/03-Pydantic与数据契约.md)
4. [04｜依赖与中间件：复用前提，不隐藏执行过程](../curriculum/02-fastapi/docs/04-Dependency与Middleware.md)
5. [05｜资源生命周期：何时取得，何时归还](../curriculum/02-fastapi/docs/05-ResourceLifecycle.md)
6. [06｜异步与并发：等待时谁在继续工作](../curriculum/02-fastapi/docs/06-AsyncExecution与BlockingBoundary.md)
7. [07｜流式响应：逐步交付结果与 SSE 事件](../curriculum/02-fastapi/docs/07-Streaming与SSE.md)
8. [08｜WebSocket：让双方在连接中持续交流](../curriculum/02-fastapi/docs/08-WebSocket与EventProtocol.md)
9. [09｜认证、授权与租户：让访问范围可信](../curriculum/02-fastapi/docs/09-Security与TenantContext.md)
10. [10｜连接外部服务：客户端、业务与协议适配](../curriculum/02-fastapi/docs/10-ExternalResourceIntegration.md)
11. [11｜上传与后台任务：接收完成不等于处理完成](../curriculum/02-fastapi/docs/11-BackgroundTask与Upload.md)
12. [12｜超时、断开与取消：请求结束之后发生什么](../curriculum/02-fastapi/docs/12-TimeoutCancellation与Disconnect.md)
13. [13｜测试：让成功、拒绝与失败都有证据](../curriculum/02-fastapi/docs/13-Testing.md)
14. [14｜观测与性能：把慢请求拆成可定位的时间](../curriculum/02-fastapi/docs/14-Observability与Performance.md)
15. [15｜部署与退出：从一个进程到多个实例](../curriculum/02-fastapi/docs/15-Deployment与GracefulShutdown.md)
16. [16｜综合实作：把问答与执行任务接成可验证 API](../curriculum/02-fastapi/docs/16-AIServicePatterns.md)

配套：[review](../curriculum/02-fastapi/review/README.md)

配套：[interview](../curriculum/02-fastapi/interview)

配套：[examples](../curriculum/02-fastapi/examples/README.md)

</details>

<details>
<summary>MySQL · 19 篇</summary>

1. [01｜数据库、MySQL 与关系表](../curriculum/04-mysql/docs/01-数据库与关系表.md)
2. [02｜用 SQL 查询、增加、修改和删除记录](../curriculum/04-mysql/docs/02-单表查询与增删改.md)
3. [03｜字段、约束与表之间的关系](../curriculum/04-mysql/docs/03-数据类型约束与表关系.md)
4. [04｜把多张表查在一起，把多条记录汇总起来](../curriculum/04-mysql/docs/04-关联查询与分组统计.md)
5. [05｜从查对结果到少做工作：执行计划与索引](../curriculum/04-mysql/docs/05-SQL执行与索引基础.md)
6. [06｜B+ 树怎样组织数据：聚簇索引与二级索引](../curriculum/04-mysql/docs/06-B+树与数据组织.md)
7. [07｜联合索引怎样定位、排序和减少回表](../curriculum/04-mysql/docs/07-联合索引覆盖与下推.md)
8. [08｜读懂执行计划，找到查询真正慢在哪里](../curriculum/04-mysql/docs/08-执行计划与慢查询.md)
9. [09｜事务：哪些修改必须一起成立](../curriculum/04-mysql/docs/09-事务与ACID.md)
10. [10｜并发读取：隔离级别与 MVCC](../curriculum/04-mysql/docs/10-隔离级别与MVCC.md)
11. [11｜并发修改：条件更新、锁与死锁](../curriculum/04-mysql/docs/11-并发修改锁与死锁.md)
12. [12｜日志、提交与故障恢复](../curriculum/04-mysql/docs/12-日志提交与恢复.md)
13. [13｜分页：先跳过，还是从上次的位置继续](../curriculum/04-mysql/docs/13-分页与查询成本.md)
14. [14｜数据增长以后，怎样维护主键、索引和表结构](../curriculum/04-mysql/docs/14-主键索引与表结构演进.md)
15. [15｜批量写入：Batch、事务与写入成本](../curriculum/04-mysql/docs/15-批量写入与写入成本.md)
16. [16｜复制与读写分离：多份数据何时一致](../curriculum/04-mysql/docs/16-复制与读写分离.md)
17. [17｜CDC：把已提交的变化可靠地交给下游](../curriculum/04-mysql/docs/17-CDC与下游同步.md)
18. [18｜分片：确认单机边界之后再拆数据](../curriculum/04-mysql/docs/18-分片与扩容.md)
19. [19｜把数据库知识用在 AI 应用的数据模型中](../curriculum/04-mysql/docs/19-AI应用数据建模.md)

配套：[review](../curriculum/04-mysql/review/README.md)

配套：[interview](../curriculum/04-mysql/interview)

配套：[examples](../curriculum/04-mysql/examples/README.md)

</details>

<details>
<summary>Redis · 18 篇</summary>

1. [01｜Redis 是什么，为什么系统里还需要它](../curriculum/05-redis/docs/01-Redis是什么.md)
2. [02｜同一份数据，怎样保存才方便使用](../curriculum/05-redis/docs/02-键与常用数据类型.md)
3. [03｜数据什么时候应该消失](../curriculum/05-redis/docs/03-过期与内存淘汰.md)
4. [04｜把 Redis 用作缓存：读与更新怎样配合](../curriculum/05-redis/docs/04-缓存读取与更新.md)
5. [05｜缓存帮不上忙时，怎样保护数据来源](../curriculum/05-redis/docs/05-缓存故障与流量保护.md)
6. [06｜本地缓存与 AI 结果缓存：什么可以复用](../curriculum/05-redis/docs/06-多级缓存与结果复用.md)
7. [07｜Redis 为什么快，请求又为什么会慢](../curriculum/05-redis/docs/07-执行模型与Pipeline.md)
8. [08｜内存怎样花出去：编码、大小与数据表示](../curriculum/05-redis/docs/08-内部编码与数据规模.md)
9. [09｜多步修改怎样避免互相干扰](../curriculum/05-redis/docs/09-事务与服务端逻辑.md)
10. [10｜服务重启后，数据从哪里回来](../curriculum/05-redis/docs/10-持久化与恢复.md)
11. [11｜有了副本，故障时怎样接替服务](../curriculum/05-redis/docs/11-复制与Sentinel.md)
12. [12｜一台装不下以后，数据怎样分到多台](../curriculum/05-redis/docs/12-Cluster与分片.md)
13. [13｜锁过期了，旧工作者为什么还可能继续](../curriculum/05-redis/docs/13-分布式锁.md)
14. [14｜消息发出以后，怎样知道还有什么没做](../curriculum/05-redis/docs/14-通知与Streams.md)
15. [15｜多个服务怎样共同守住一份限额](../curriculum/05-redis/docs/15-共享限流.md)
16. [16｜登录、最近消息和任务进度应该怎样保存](../curriculum/05-redis/docs/16-会话与运行状态.md)
17. [17｜出问题时，从哪里找到证据](../curriculum/05-redis/docs/17-安全与问题定位.md)
18. [18｜从需求出发，完成一份 Redis 设计](../curriculum/05-redis/docs/18-综合设计与回顾.md)

配套：[review](../curriculum/05-redis/review/README.md)

配套：[interview](../curriculum/05-redis/interview)

配套：[examples](../curriculum/05-redis/examples/README.md)

</details>

<details>
<summary>Backend · 22 篇</summary>

1. [一次请求完成了什么，后端负责到哪里](../curriculum/03-backend-engineering/docs/01-AIBackend职责与RequestPath.md)
2. [哪些状态必须保存，恢复时相信哪一份](../curriculum/03-backend-engineering/docs/14-DataLayering与StateOwnership.md)
3. [从字节到安全请求：TCP、TLS 与 HTTP](../curriculum/03-backend-engineering/docs/02-TCPTLS与HTTPVersions.md)
4. [怎样传递结果，断线后怎样继续](../curriculum/03-backend-engineering/docs/03-ServiceCommunication与StreamingReliability.md)
5. [并发工作由谁执行，等待放在哪里](../curriculum/03-backend-engineering/docs/04-Concurrency与ThreadPool.md)
6. [连接怎样复用，容量怎样计算](../curriculum/03-backend-engineering/docs/05-ConnectionPool与ResourceCapacity.md)
7. [到达速度超过处理能力时怎么办](../curriculum/03-backend-engineering/docs/06-Backpressure与RateLimit.md)
8. [等多久，超时之后还发生什么](../curriculum/03-backend-engineering/docs/07-TimeoutDeadline与ErrorTaxonomy.md)
9. [怎样识别同一次操作，避免重复副作用](../curriculum/03-backend-engineering/docs/09-APIIdempotency与SideEffect.md)
10. [什么时候值得再试，怎样防止故障放大](../curriculum/03-backend-engineering/docs/08-RetryCircuitBreaker与Failover.md)
11. [消息怎样交付，确认到底确认了什么](../curriculum/03-backend-engineering/docs/10-MQ与DeliverySemantics.md)
12. [Kafka 怎样分工、保序与恢复消费](../curriculum/03-backend-engineering/docs/11-KafkaPartition与Backlog.md)
13. [进程重启后，任务怎样继续推进](../curriculum/03-backend-engineering/docs/12-ReliableAsyncTask.md)
14. [多份数据不一致时，怎样恢复业务正确性](../curriculum/03-backend-engineering/docs/13-Consistency与Compensation.md)
15. [谁能访问什么，权限怎样贯穿请求与任务](../curriculum/03-backend-engineering/docs/15-AuthSession与TenantBoundary.md)
16. [不可信输入怎样被限制在安全边界内](../curriculum/03-backend-engineering/docs/21-BackendSecurity.md)
17. [多个服务实例怎样被找到和选中](../curriculum/03-backend-engineering/docs/16-ServiceDiscovery与LoadBalancing.md)
18. [从慢请求的证据定位瓶颈](../curriculum/03-backend-engineering/docs/17-Observability与PerformanceDiagnosis.md)
19. [把应用故障追到 Linux 资源](../curriculum/03-backend-engineering/docs/18-LinuxTroubleshooting.md)
20. [部署、探针与停机怎样配合应用](../curriculum/03-backend-engineering/docs/19-ContainerK8s与Deployment.md)
21. [配置和版本怎样安全改变](../curriculum/03-backend-engineering/docs/20-ConfigRelease与ServiceEvolution.md)
22. [把通用机制映射到 Java、Spring 与 Go](../curriculum/03-backend-engineering/docs/22-CrossLanguageRuntimeMapping.md)

配套：[review](../curriculum/03-backend-engineering/review/README.md)

配套：[interview](../curriculum/03-backend-engineering/interview)

配套：[examples](../curriculum/03-backend-engineering/examples/README.md)

</details>

<details>
<summary>Vector DB · 16 篇</summary>

1. [01｜向量数据库究竟负责什么](../curriculum/06-vector-db/docs/01-VectorDB在AI应用中的职责.md)
2. [02｜向量空间与相似度：先把“近”说清楚](../curriculum/06-vector-db/docs/02-VectorSpace与Similarity.md)
3. [03｜精确搜索与 ANN：先建立可核对的答案](../curriculum/06-vector-db/docs/03-ExactSearch与ANN.md)
4. [04｜索引谱系：近似究竟发生在哪里](../curriculum/06-vector-db/docs/04-ANN索引谱系.md)
5. [05｜HNSW：沿着图寻找近邻](../curriculum/06-vector-db/docs/05-HNSW机制与调优.md)
6. [06｜IVF：先选区域，再找向量](../curriculum/06-vector-db/docs/06-IVF原理.md)
7. [07｜量化与 PQ：用短编码近似距离](../curriculum/06-vector-db/docs/07-Quantization与PQ.md)
8. [08｜索引选择：把机制放回工作负载](../curriculum/06-vector-db/docs/08-IndexSelection.md)
9. [09｜向量数据建模：让结果找得到来源](../curriculum/06-vector-db/docs/09-Vector数据建模.md)
10. [10｜元数据过滤：在允许的范围内找近邻](../curriculum/06-vector-db/docs/10-MetadataFilter.md)
11. [11｜分区与多租户：数据放在哪，谁可以读](../curriculum/06-vector-db/docs/11-Partition与TenantIsolation.md)
12. [12｜索引生命周期：写入、更新、删除与重建](../curriculum/06-vector-db/docs/12-VectorIndex生命周期.md)
13. [13｜分布式检索：局部结果怎样组成全局答案](../curriculum/06-vector-db/docs/13-分布式VectorDB.md)
14. [14｜性能与容量：用证据定位瓶颈](../curriculum/06-vector-db/docs/14-性能容量与Production诊断.md)
15. [15｜产品与架构选择：先决定需要哪类能力](../curriculum/06-vector-db/docs/15-产品与架构选型.md)
16. [16｜图数据库边界：相似、关系与完整系统](../curriculum/06-vector-db/docs/16-GraphDB边界与系统设计.md)

配套：[review](../curriculum/06-vector-db/review/README.md)

配套：[interview](../curriculum/06-vector-db/interview)

配套：[labs](../curriculum/06-vector-db/labs/README.md)

</details>

<details>
<summary>LLM Foundation · 14 篇</summary>

1. [01｜模型在 AI 应用中负责什么](../curriculum/07-llm-foundation/docs/01-LLMFoundation在AI应用中的职责.md)
2. [02｜Token、上下文与长文本：先确定模型实际读到了什么](../curriculum/07-llm-foundation/docs/02-TokenContext与LongContext.md)
3. [03｜Transformer 怎样把 Token 序列变成候选分数](../curriculum/07-llm-foundation/docs/03-TransformerBlock.md)
4. [04｜Attention 与位置信息：算一次信息怎样汇入当前位置](../curriculum/07-llm-foundation/docs/04-Attention与Position.md)
5. [05｜从候选分数到一段回答：生成与解码](../curriculum/07-llm-foundation/docs/05-Generation与Decoding.md)
6. [06｜KV Cache 与 Prefill、Decode：为什么少算了，却更占显存](../curriculum/07-llm-foundation/docs/06-KVCache与PrefillDecode.md)
7. [07｜模型服务与性能：把等待、吞吐和显存分开判断](../curriculum/07-llm-foundation/docs/07-ServingEngine与性能.md)
8. [08｜模型 API 与选型：接口调用成功以后，还要验证什么](../curriculum/07-llm-foundation/docs/08-ModelAPI与Selection.md)
9. [09｜Embedding 与 Reranker：一段文字怎样成为可检索的向量](../curriculum/07-llm-foundation/docs/09-Embedding与Reranker.md)
10. [10｜多模态基础：从看见一张图到给出可验证答案](../curriculum/07-llm-foundation/docs/10-MultimodalFoundation.md)
11. [11｜Prompt Engineering：把任务写成可检查的输入](../curriculum/07-llm-foundation/docs/11-PromptEngineering.md)
12. [12｜事实错误与干预边界：什么时候改 Prompt，什么时候需要别的机制](../curriculum/07-llm-foundation/docs/12-Hallucination与干预边界.md)
13. [13｜SFT 与 LoRA：模型究竟学了什么，少训练哪些参数](../curriculum/07-llm-foundation/docs/13-FineTuning与LoRA.md)
14. [14｜后训练与蒸馏：示范、偏好和奖励分别在教什么](../curriculum/07-llm-foundation/docs/14-PostTraining与Distillation.md)

配套：[review](../curriculum/07-llm-foundation/review/README.md)

配套：[interview](../curriculum/07-llm-foundation/interview)

配套：[labs](../curriculum/07-llm-foundation/labs/README.md)

</details>

<details>
<summary>RAG · 14 篇</summary>

1. [01｜RAG 职责与完整链路：把外部事实变成有依据的回答](../curriculum/08-rag/docs/01-RAG职责与完整链路.md)
2. [02｜语料治理：先确定哪些知识可信、有效、可见](../curriculum/08-rag/docs/02-CorpusGovernance.md)
3. [03｜文档解析：从页面外观恢复可检索的内容](../curriculum/08-rag/docs/03-DocumentProcessing.md)
4. [04｜切分设计：怎样保留一个问题需要的完整语义](../curriculum/08-rag/docs/04-ChunkingDesign.md)
5. [05｜块之间的关系：小块检索，大块补全](../curriculum/08-rag/docs/05-AdvancedChunkStructure.md)
6. [06｜查询规划：把用户的话变成可执行的检索请求](../curriculum/08-rag/docs/06-QueryPlanning.md)
7. [07｜多路检索与融合：让语义和词项互相补位](../curriculum/08-rag/docs/07-RetrievalStack.md)
8. [08｜重排与候选预算：把有限算力用在值得阅读的证据上](../curriculum/08-rag/docs/08-Rerank与CandidateBudget.md)
9. [09｜证据交付：从候选片段到可追溯的答案](../curriculum/08-rag/docs/09-EvidenceDelivery.md)
10. [10｜检索评测：分数到底衡量了什么](../curriculum/08-rag/docs/10-RetrievalEvaluation.md)
11. [11｜端到端质量：用证据定位失败，再证明改动有效](../curriculum/08-rag/docs/11-EndToEndQualityEngineering.md)
12. [12｜更新、权限与回滚：让用户看到正确版本的合法知识](../curriculum/08-rag/docs/12-ProductionGovernance.md)
13. [13｜规模、成本与可观测性：让链路能持续运行](../curriculum/08-rag/docs/13-ScaleCostObservability.md)
14. [14｜GraphRAG 与 Agentic RAG：何时需要结构，何时需要继续搜索](../curriculum/08-rag/docs/14-GraphRAG与AgenticRAG.md)

配套：[review](../curriculum/08-rag/review/README.md)

配套：[interview](../curriculum/08-rag/interview)

配套：[examples](../curriculum/08-rag/examples/README.md)

</details>

<details>
<summary>Agent · 24 篇</summary>

1. [01. Agent 系统的全貌：模型之外，谁把任务做完](../curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md)
2. [02. Workflow、Agent 与自主权：执行角色的边界](../curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md)
3. [03. Agent Loop：Session、Run、Turn、Step 与执行事件](../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md)
4. [04. Tool Contract：工具说明、参数与语义校验](../curriculum/09-agent/docs/04-ToolContractAndValidation.md)
5. [05. Tool Registry：工具注册、模型可见说明与按需发现](../curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md)
6. [06. Tool Execution：结果回填、错误分类与有限恢复](../curriculum/09-agent/docs/06-ToolExecutionAndFailure.md)
7. [07. Tool Control：副作用、并发、取消与进度](../curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md)
8. [08. Planning / ReAct：计划、目标、停止与预算](../curriculum/09-agent/docs/08-PlanningGoalAndControl.md)
9. [09. Context Assembly：上下文编排、缓存与结果外部化](../curriculum/09-agent/docs/09-ContextAssemblyAndCache.md)
10. [10. Context Compaction：压缩、替代历史与继续执行](../curriculum/09-agent/docs/10-CompactionAndContinuation.md)
11. [11. Memory：提取、召回、更新、纠错与遗忘](../curriculum/09-agent/docs/11-MemoryLifecycle.md)
12. [12. State / Persistence：程序怎样记住当前工作](../curriculum/09-agent/docs/12-StateHistoryAndPersistence.md)
13. [13. Checkpoint / Resume：检查点、恢复、分叉与重放](../curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md)
14. [14. Permission / Approval / Sandbox：政策、批准与隔离](../curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md)
15. [15. Guardrails：提示注入、秘密保护与风险控制](../curriculum/09-agent/docs/15-InjectionAndContainment.md)
16. [16. MCP：从 Host / Client / Server 到完整协议往返](../curriculum/09-agent/docs/16-MCPArchitectureAndLifecycle.md)
17. [17. Skills / Hooks / Plugins：能力扩展与生命周期](../curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md)
18. [18. Routing：意图、模型适配与供应商容错](../curriculum/09-agent/docs/18-RoutingAndProviderResilience.md)
19. [19. Multi-Agent / A2A：内部协作与跨系统任务](../curriculum/09-agent/docs/19-MultiAgentAndA2A.md)
20. [20. Trace / Replay：记录必要证据，定位具体问题](../curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md)
21. [21. Agent Evaluation、Benchmark 与 Data Flywheel](../curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md)
22. [22. Coding Agent：Repo Understanding → Patch → Test → Verify](../curriculum/09-agent/docs/22-CodingAgentDelivery.md)
23. [23. Production Agent：从单进程到可运营执行系统](../curriculum/09-agent/docs/23-ProductionRuntime.md)
24. [24. Framework Mapping：按核心语义比较框架与自研](../curriculum/09-agent/docs/24-FrameworkSelection.md)

配套：[review](../curriculum/09-agent/review/README.md)

配套：[interview](../curriculum/09-agent/interview)

</details>

<details>
<summary>System Design · 19 篇</summary>

1. [01｜System Design 的职责与完整答题框架](../curriculum/10-system-design/docs/01-SystemDesign职责与答题框架.md)
2. [02｜Requirement、SLO、Constraint 与 Scope](../curriculum/10-system-design/docs/02-Requirement与SLO.md)
3. [03｜Workload、Capacity、Hotspot 与数量级估算](../curriculum/10-system-design/docs/03-Workload与CapacityEstimation.md)
4. [04｜API、Data Model 与 State Ownership](../curriculum/10-system-design/docs/04-API数据模型与StateOwnership.md)
5. [05｜Sync / Async、Data Flow 与 State Machine](../curriculum/10-system-design/docs/05-DataFlow与StateMachine.md)
6. [06｜Cache、Hot Path 与 Read / Write Path](../curriculum/10-system-design/docs/06-Cache与HotPath.md)
7. [07｜Partition、Routing、Fan-out 与 Rebalance](../curriculum/10-system-design/docs/07-PartitionRouting与Fanout.md)
8. [08｜Consistency、Idempotency、Transaction 与 Compensation](../curriculum/10-system-design/docs/08-Consistency与Idempotency.md)
9. [09｜Queue、Backpressure 与 Long-running Task](../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md)
10. [10｜Timeout、Retry、Failover、Degradation 与 Load Shedding](../curriculum/10-system-design/docs/10-Reliability与Overload.md)
11. [11｜Multi-tenancy、Security、Permission 与 Isolation](../curriculum/10-system-design/docs/11-MultiTenancy与Security.md)
12. [12｜Observability、Evaluation、Cost 与 Evolution](../curriculum/10-system-design/docs/12-ObservabilityEvaluation与Evolution.md)
13. [13｜High-concurrency Transactional Systems：秒杀、库存、Rate Limit、Token Refresh](../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md)
14. [14｜Realtime Read-heavy Systems：排行榜、Feed、Autocomplete、Notification](../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md)
15. [15｜Large-scale Data & Processing：10TB Storage、Migration、Dedup、Large-file](../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md)
16. [16｜LLM Gateway 与 Multi-tenant AI Platform](../curriculum/10-system-design/docs/16-LLMGateway与MultiTenantAIPlatform.md)
17. [17｜Enterprise / Large-scale RAG System Design](../curriculum/10-system-design/docs/17-EnterpriseRAGSystemDesign.md)
18. [18｜Production Agent Backend 与 Long-running Agent](../curriculum/10-system-design/docs/18-ProductionAgentBackend.md)
19. [19｜Vertical AI Agent Patterns：Analysis、Customer Service、Multimodal、Game、Content](../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md)

配套：[review](../curriculum/10-system-design/review/README.md)

配套：[interview](../curriculum/10-system-design/interview)

</details>

<details>
<summary>Claude Code · 4 篇</summary>

1. [01. 上下文生命周期｜模型这一轮究竟看见什么](../products/agent/claude-code/01-context-lifecycle.md)
2. [02. 记忆生命周期｜什么值得留下，下一次怎样正确使用](../products/agent/claude-code/02-memory-lifecycle.md)
3. [03. 工具生命周期｜从知道能力到确认动作完成](../products/agent/claude-code/03-tool-lifecycle.md)
4. [04. 恢复、协作与验证｜怎样证明长任务做对了](../products/agent/claude-code/04-engineering-evaluation.md)

</details>

<details>
<summary>Codex · 4 篇</summary>

1. [上下文｜一次任务怎样变成连续的模型请求](../products/agent/codex/01-context-lifecycle.md)
2. [工具｜从模型提出动作，到受控执行与结果回填](../products/agent/codex/03-tool-lifecycle.md)
3. [记忆｜历史怎样变成可以复用、也可以纠正的经验](../products/agent/codex/02-memory-lifecycle.md)
4. [工程与评测｜任务怎样持续运行，怎样证明真的完成](../products/agent/codex/04-engineering-evaluation.md)

</details>

<details>
<summary>DeepSeek Harness · 4 篇</summary>

1. [01｜上下文生命周期：模型这一轮究竟看见什么](../products/agent/deepseek-harness/01-context-lifecycle.md)
2. [02｜记忆怎样跨过一轮对话，又在哪些地方失效](../products/agent/deepseek-harness/02-memory-lifecycle.md)
3. [03｜一次工具调用怎样从建议变成可检查的执行](../products/agent/deepseek-harness/03-tool-lifecycle.md)
4. [04｜中断以后怎样安全继续，又怎样证明任务真的完成](../products/agent/deepseek-harness/04-engineering-evaluation.md)

配套：[labs](../products/agent/deepseek-harness/labs/README.md)

</details>

<details>
<summary>DeerFlow 2.0 · 4 篇</summary>

1. [01｜上下文：从会话状态到模型真正看到的内容](../products/agent/deer-flow/01-context-lifecycle.md)
2. [02｜记忆：从一次对话到可维护的长期事实](../products/agent/deer-flow/02-memory-lifecycle.md)
3. [03｜工具：从可发现能力到受控副作用](../products/agent/deer-flow/03-tool-lifecycle.md)
4. [04｜工程与评测：怎样继续、恢复并证明结果](../products/agent/deer-flow/04-engineering-evaluation.md)

配套：[review](../products/agent/deer-flow/review/README.md)

配套：[labs](../products/agent/deer-flow/labs/README.md)

</details>

<details>
<summary>Coding · 正文顺序</summary>

1. [01｜程序基础：让 Python 一步一步替你做事](../practice/coding/docs/01-programming-fundamentals.md)
2. [02｜数据类型与容器：给数据选一个合适的组织方式](../practice/coding/docs/02-python-coding-basics.md)
3. [03｜基础练习：读题、实现、测试、解释](../practice/coding/docs/03-basic-exercises.md)
4. [04｜完整输入输出：把数据协议翻译成程序](../practice/coding/docs/04-acm-input-output.md)
5. [05｜数据结构：从操作需求到结构选择](../practice/coding/docs/05-data-structures.md)
6. [06｜算法推导：从正确做法到减少重复工作](../practice/coding/docs/06-problem-solving-and-algorithms.md)
7. [07｜Hot100 综合训练：把专题知识变成可调用能力](../practice/coding/docs/07-hot100.md)
8. [08｜在线笔试：把算法放进完整交付约束](../practice/coding/docs/08-online-assessment.md)
9. [09｜AI Coding：从可复现失败到可验证交付](../practice/coding/docs/09-ai-coding.md)

</details>

## Practice 与技术依据

- [Coding](../practice/coding/README.md)：9 篇正文，题单和练习由模块入口承接。
- [Git 与开发工作流](../practice/tooling/README.md)：操作指南，不计入课程章数。
- [References](../references/README.md)：8 个实际资料目录，技术事实与真人面经证据分开。
- [项目记录](project/README.md)与[审计记录](audits/README.md)：按记录的适用基线读取。

⚠️ 章节数量和入口可达仅证明文档范围与导航一致，不等于完成初学者阅读、真实服务或生产验证。
