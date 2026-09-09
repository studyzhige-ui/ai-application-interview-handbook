# Batch 03 — 规范化问题增量

只记录 Batch 03 相比前两批 **新出现，或已经细化到值得单独成为 canonical question** 的问题。已有问题只是增加来源时，放在文末“已有问题得到强化”中，不重复造新 ID。

## Agent Harness / Runtime

### A045 Agent Harness 如何实现可复现、可审计的 Deterministic Replay？
- 来源：S032
- 标签：Agent Harness / Replay / Observability / State

### A046 Prompt、Runtime State、RAG Evidence、Tool Result 应如何建立信任层级，避免低可信内容覆盖系统规则？
- 来源：S032
- 标签：Context Engineering / Trust Boundary / Prompt Injection

### A047 MCP Host、Client、Server 的职责、信任边界以及能力协商生命周期是什么？
- 来源：S026, S032
- 标签：MCP / Protocol / Capability Negotiation / Trust

### A048 MCP Server 能力变化后，客户端如何实时发现、刷新 Tool 列表并处理兼容性？
- 来源：S026
- 标签：MCP / Tool Discovery / Dynamic Capability

### A049 Agent Memory 中新事实与旧事实冲突时，如何决定覆盖、并存、降权或拒绝写入？
- 来源：S026, S032
- 标签：Memory / Conflict Resolution / Temporal Semantics

### A050 多 Agent / 多 Worker 并发修改共享 Task State 时，如何防止 Lost Update、状态分叉和覆盖？
- 来源：S022, S032
- 标签：State / Concurrency / Optimistic Lock / Consistency

### A051 Coding Agent 如何把文件修改设计成可审计、可回放、可回滚的 Workspace Transaction？
- 来源：S032
- 标签：Coding Agent / Filesystem / Audit / Transaction

### A052 Shell / Code Execution Tool 的沙箱边界如何覆盖文件系统、网络、系统调用、资源配额和超时？
- 来源：S022, S032
- 标签：Tool Runtime / Sandbox / Security

### A053 Multi-Agent 拆任务时如何显式处理依赖关系，避免子任务重复、遗漏和循环依赖？
- 来源：S022, S032
- 标签：Multi-Agent / Planning / Dependency Graph

### A054 MCP / Tool Governance 应治理哪些对象：注册、权限、Schema、审计、版本、风险和运行策略？
- 来源：S028
- 标签：MCP / Tool Governance / Security / Audit

### A055 Agent 安全路由 / 意图路由的准确率应该如何定义、构造数据集并评测？
- 来源：S028
- 标签：Routing / Evaluation / Safety

### A056 如何抽象 Model Provider Adapter，统一不同模型的消息格式、Tool Call、流式事件和错误语义？
- 来源：S022
- 标签：Model Runtime / Adapter / Portability

### A057 AI/Coding Agent 生成代码后，如何通过测试、静态检查、沙箱执行和验收条件自动验证？
- 来源：S022, S023, S030
- 标签：Coding Agent / Verification / Testing

### A058 Agent Runtime 与 Go/Java 等业务服务之间如何设计高吞吐、可取消、可流式的双向通信？
- 来源：S032
- 标签：Runtime / Backend Integration / Streaming / Protocol

### A059 用户新请求与旧请求发生语义冲突时，Memory / Task State 如何基于时序、优先级和确认机制决定当前有效目标？
- 来源：S026
- 标签：Memory / Task State / Temporal Priority

### A060 Agent 系统能否形成“发现 Bad Case → 生成候选策略 → 离线验证 → 灰度 → 自动回滚”的自优化闭环？
- 来源：S027
- 标签：Agent Ops / Evaluation / Continuous Improvement / Rollback

## RAG / Retrieval

### R018 知识库持续更新时，如何让一次 RAG 查询看到快照一致的数据版本？
- 来源：S032
- 标签：RAG / Consistency / Snapshot / Production

### R019 BM25、Dense Vector、Graph Retrieval 等多路召回分数不在同一尺度时，如何校准和融合？
- 来源：S024, S032
- 标签：Hybrid Retrieval / Score Calibration / Fusion

### R020 如何为向量索引设计 Version Filter / Time-travel Query，以支持历史版本和可复现检索？
- 来源：S032
- 标签：Vector Index / Versioning / Time Travel

### R021 RAG 证据送入模型前，如何避免 Citation Drift、错误拼接和“答案有引用但引用不支持结论”？
- 来源：S032
- 标签：RAG / Evidence / Citation / Grounding

### R022 Agentic Retrieval 如何决定“继续检索 / 改写 Query / 换检索器 / 终止检索”？
- 来源：S032
- 标签：Agentic RAG / Retrieval Control Loop

### R023 BGE-M3 的 Dense、Sparse、Multi-vector 三种检索表示分别解决什么问题，如何组合？
- 来源：S024
- 标签：Retrieval / Dense / Sparse / Multi-vector / BGE-M3

### R024 BM25 的词频饱和、IDF 与长度归一化分别解决什么问题？
- 来源：S024
- 标签：Sparse Retrieval / BM25 / Principle

### R025 RRF 为什么可以在不校准原始分数的情况下融合多个检索器？它丢失了什么信息？
- 来源：S024
- 标签：Hybrid Retrieval / RRF / Rank Fusion

### R026 Chunk Size / Overlap / Split Strategy 如何通过系统化实验自动选择，而不是固定经验值？
- 来源：S022, S032
- 标签：Chunking / Experiment / Auto Tuning

### R027 RAG 入库前如何做数据质量治理，防止错误、重复、过期或冲突内容污染知识库？
- 来源：S031
- 标签：RAG / Data Quality / Ingestion / Governance

## Vector DB

### V006 IVF_FLAT 与 HNSW 在召回率、延迟、内存、构建成本和动态更新方面如何取舍？
- 来源：S034
- 标签：Vector DB / ANN / IVF / HNSW

## Redis

### D006 RDB 与 AOF 分别记录什么，恢复速度、数据丢失窗口和写放大如何权衡？
- 来源：S022
- 标签：Redis / Persistence / RDB / AOF

### D007 Redis “核心命令单线程”为什么仍然快？Redis 6 的多线程主要加速哪些环节？
- 来源：S022
- 标签：Redis / Thread Model / IO

### D008 Redis 过期键删除策略如何在 CPU 时间与内存占用之间权衡？
- 来源：S026
- 标签：Redis / Expiration / Memory Management

### D009 Redis ZSet 在 AI/后端项目里有哪些适合的真实场景，为什么不用 List/Hash？
- 来源：S021
- 标签：Redis / ZSet / Data Structure / Project

### D010 Redis Stream、Pub/Sub 与 RabbitMQ 等消息队列在持久化、Ack、重放和消费模型上如何选？
- 来源：S030
- 标签：Redis / Stream / PubSub / MQ / Reliability

## MySQL

### M007 多个请求同时更新 MySQL 同一行时，事务、隔离级别、行锁、乐观锁分别解决什么问题？
- 来源：S030
- 标签：MySQL / Concurrency / Transaction / Lock

### M008 联合索引的最左匹配原则是什么？为什么范围查询可能影响后续列的索引利用？
- 来源：S030
- 标签：MySQL / Composite Index / Leftmost Prefix

### M009 主键索引、唯一索引、普通二级索引参与锁定读/更新时，锁范围如何分析？
- 来源：S025
- 标签：MySQL / Index / Lock / Next-key

## Backend / Production

### B007 大文件分片上传与断点续传如何设计：Upload ID、分片状态、幂等、校验、合并与失败恢复？
- 来源：S030
- 标签：Backend / File Upload / Resumable / Idempotency

### B008 AI 应用要求约 200ms 端到端 SLA 时，如何优化意图识别、外部 API、缓存、预计算和超时预算？
- 来源：S023
- 标签：Production / Latency / Cache / SLA

### B009 Python Async Agent Runtime 中混入 CPU 密集任务会发生什么？如何使用线程池、进程池或任务隔离？
- 来源：S032
- 标签：Python / Async / CPU-bound / Runtime

## 已有 canonical questions 得到显著强化

本批没有为以下主题重复创建新 ID，但其来源覆盖明显增加：

- `A003` ReAct vs Plan-and-Execute：S022, S028, S033
- `A005` 死循环 / 路径震荡：S022, S029
- `A006` Tool 设计原则与 Schema：S022
- `A010/A036` Tool 过多时按需发现与渐进式加载：S026
- `A014/A015` Context、短期/长期 Memory：S022, S026, S028, S031, S034
- `A020` 单 Agent vs Multi-Agent：S021, S027, S033
- `A023/A037/A038` 失败恢复、Checkpoint、Resume：S022, S024, S027
- `A026/A027` Agent 指标与评测集：S023, S025, S028
- `A042/A044` 模型路由与 Failover：S027
- `R001` RAG 完整链路：S021, S022, S030
- `R004` 召回不准排查：S022, S029
- `R007/R008` Hybrid Search 与 Rerank：S022, S024
- `R013` RAG vs Fine-tuning：S022, S023
- `V001/V002/V003` Vector DB 职责、选型、语义检索：S021, S027, S031, S034
- `M001/M002/M003` 索引、事务、MVCC：S025, S030

## 对课程设计的新约束

Batch 03 之后，后续教材目录必须明确覆盖：

1. **MCP Lifecycle**：Tool Discovery、动态刷新、版本、取消、恢复、信任边界。
2. **Agent Replay / Audit**：Checkpoint 不等于 Replay；要能重建当时模型输入、状态、Tool 结果与外部副作用。
3. **Workspace Transaction**：Coding Agent 文件修改不能只讲“write_file”，还要讲 diff、审计、冲突、回滚、验证。
4. **Memory Conflict Resolution**：长期记忆必须有写入策略、时效、冲突与来源可信度，而不是“全部向量化保存”。
5. **RAG Data Lifecycle**：数据质量、快照、版本、时间旅行、引用来源与一致性。
6. **Hybrid Retrieval 原理层**：不能只写“BM25 + Vector + Rerank”，必须讲 BM25、BGE-M3、RRF、分数校准等机制。
7. **AI Application Production Engineering**：SLA、文件流水线、MQ、MySQL 并发、Redis 生命周期、Async CPU 隔离仍是求职核心。
