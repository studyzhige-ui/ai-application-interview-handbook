# Batch 04 — 规范化问题增量

只记录 Batch 04 相比前三批 **新出现，或已经细化到值得单独成为 canonical question** 的问题。已有问题只是增加来源时，放在文末“已有问题得到强化”中，不重复造新 ID。

## Agent Harness / Runtime

### A061 长程 Agent 任务出现明显 Latency Regression 时，如何做端到端瓶颈归因？
- 来源：S035
- 标签：Agent Harness / Performance / Trace / Latency
- 核心拆解：模型推理、Context 膨胀、Tool 延迟、检索、网络、队列、并发资源、重试、循环步数分别如何观测和定位。

### A062 Agent 长任务如何实现 Cooperative Cancellation，并正确清理状态与外部副作用？
- 来源：S039
- 标签：Agent Runtime / Cancellation / Side Effect / Lifecycle
- 核心拆解：Cancel Token、Tool 中断、正在进行的 IO、子任务传播、事务/补偿、最终状态如何定义。

### A063 Agent Runtime 的消息 / 事件模型应该有哪些类型，为什么不能把所有交互都当普通 Chat Message？
- 来源：S039, S045
- 标签：Agent Runtime / Message Protocol / Tool Event / State Event
- 核心拆解：User / Assistant / Tool Call / Tool Result / System Event / State Update / Error / Progress 等消息语义与持久化边界。

### A064 多用户、多任务 Agent 如何同时隔离 Context、Runtime State、资源配额和执行生命周期？
- 来源：S042
- 标签：Agent Runtime / Isolation / Multi-tenant / Resource
- 与 A032 区别：A032 重点是会话 Context/Session 串话；本题进一步覆盖任务级资源、运行时和生命周期隔离。

### A065 什么时候应该自研 Agent Runtime / Harness，什么时候应该基于 LangGraph 等框架扩展？
- 来源：S037, S042
- 标签：Agent Harness / Build vs Buy / Architecture / Framework
- 核心拆解：控制力、可观测性、可靠性、协议兼容、迭代成本、生态与团队能力。

### A066 MCP 与传统 API Gateway / RPC 接入层的职责边界是什么？
- 来源：S043
- 标签：MCP / API Gateway / Protocol / Architecture
- 核心拆解：MCP 面向模型/Agent 的能力描述、发现、上下文和 Tool 协议；API Gateway 面向服务流量、路由、鉴权、限流等基础设施职责。

### A067 Skill Registry 如何支持动态注册、版本、权限、灰度、依赖和历史任务兼容？
- 来源：S043
- 标签：Skills / Registry / Versioning / Permission / Lifecycle
- 核心拆解：Skill 元数据、Schema、版本锁定、发布/回滚、历史 Run 可复现。

### A068 Agent Loop 的 Early Stop / Budget / Max Step 应如何设计，避免无限循环又不误杀有效长任务？
- 来源：S044
- 标签：Agent Runtime / Early Stop / Budget / Control Loop
- 与 A005 区别：A005 更侧重“已经出现死循环/路径震荡如何检测”；本题侧重运行前和运行中的预算控制机制。

### A069 如何把模型能力与 Harness 能力拆开评测，并对 Bad Case 做责任归因？
- 来源：S036
- 标签：Agent Evaluation / Harness Evaluation / Attribution
- 与 A026 区别：A026 是宏观评价 Agent；本题要求实验设计能区分 Base Model、Prompt、Context、Tool Runtime、Memory、Planner、Recovery 各层贡献。

### A070 面试中被要求“解释 Codex / Claude Code 是怎么实现的”时，应该从哪些 Runtime 维度拆解成熟 Agent 产品？
- 来源：S036, S037, S038
- 标签：Agent Harness / Product Architecture / Codex / Claude Code
- 核心拆解：Agent Loop、Context Assembly/Compaction、Tool Runtime、Sandbox/Permission、State/Session、Memory、Checkpoint、Protocol、Observability、Verification。
- 课程约束：该题的权威实现材料以 `openai/codex` 和 `studyzhige-ui/claude-code-source-private` 源码为准，不用二手教程替代源码事实。

## RAG / Retrieval

### R028 600GB～TB 级企业知识库从解析、分块、Embedding、索引到在线检索应如何整体设计？
- 来源：S041
- 标签：RAG / Large Scale / Data Pipeline / System Design
- 与 R015 区别：R015 以“一万个长文档”作为规模问题；本题进一步进入 TB 级数据工程、成本和批处理架构。

### R029 电子 PDF、扫描 PDF、表格和跨页内容混合时，RAG Ingestion 如何做 OCR、版面恢复和跨页语义 Chunk？
- 来源：S041
- 标签：RAG / PDF / OCR / Layout / Chunking
- 核心拆解：文本层检测、OCR、Layout Parsing、表格结构、页眉页脚、跨页段落、质量评分与人工兜底。

### R030 大规模 Embedding 初始化与增量更新时，如何优化计算、存储和重复内容成本？
- 来源：S041
- 标签：RAG / Embedding / Cost / Incremental Index
- 核心拆解：批处理、并发、内容 Hash、去重、缓存、增量 Diff、冷热分层、量化与重建策略。

### R031 Graph / GraphRAG 的图结构如何从原始文档构建，它与 Dense / Sparse Retrieval 的职责有什么不同？
- 来源：S047
- 标签：RAG / GraphRAG / Knowledge Graph / Retrieval

## Redis

### D011 Redis 分布式锁的 Lease / WatchDog 自动续期如何实现，续期失败或业务进程死亡时如何保证安全？
- 来源：S039
- 标签：Redis / Distributed Lock / Lease / WatchDog

### D012 HotKey 与 BigKey 有什么区别？热点读写导致缓存、锁或数据库冲突时如何治理？
- 来源：S040
- 标签：Redis / HotKey / Contention / Production
- 与 D002 区别：D002 是“大对象/大集合”的 BigKey；本题是访问频率和竞争造成的 HotKey。

## Backend / Production

### B010 Agent 异步任务如何用“数据库状态机 + MQ + 幂等 Token”实现可靠调度？
- 来源：S040
- 标签：Backend / Async Task / MQ / State Machine / Idempotency
- 核心拆解：为什么 MQ 只传 ID、状态写库顺序、Outbox/事务边界、重复消息、Worker 抢占与结果落库。

### B011 长任务的 Lease / Heartbeat / Worker Recovery 如何设计，使实例宕机后任务能够安全接管？
- 来源：S040
- 标签：Backend / Distributed Task / Lease / Heartbeat / Recovery
- 与 Agent Checkpoint 的关系：Checkpoint 保存“做到了哪里”，Lease/Recovery 决定“谁有权继续做”。

### B012 Kafka / MQ 的可靠性应该如何从 Producer、Broker、Consumer 三端共同证明？
- 来源：S040
- 标签：Backend / Kafka / Reliability / Ack / Offset
- 核心拆解：acks、副本、ISR、幂等生产、Offset 提交时机、至少一次与重复消费。

### B013 如何实现“相同 Key 的任务严格串行，不同 Key 可并行”的线程安全执行器？
- 来源：S039
- 标签：Backend / Concurrency / Executor / Per-key Serialization
- AI 场景：同一 conversation/task/resource 的修改顺序必须串行，但不同会话需要并发扩展。

### B014 动态配置中心如何保证配置刷新、失败回退和应用内存状态的一致性？
- 来源：S039
- 标签：Backend / Config Center / Dynamic Refresh / Availability

### B015 几十 GB 级文件如何在有限内存下实现流式解析、去重、分块处理与结果导出？
- 来源：S040
- 标签：Backend / Large File / Streaming / External Memory Algorithm
- 与 RAG 关系：这是大规模文档 Ingestion Pipeline 的通用工程基础，而不仅是算法题。

## 已有 canonical questions 得到显著强化

- `A006/A009` Tool Schema、参数校验与非法 Tool Call 恢复：S035, S045
- `A014/A015` Context、短期 Memory、长期 Memory：S038, S039, S043, S045
- `A017/A018` Context Compaction 与信息损失检测/恢复：S035, S037, S038
- `A020/A021` Multi-Agent 拆分、通信与子 Agent 故障：S043, S045
- `A026/A027` Agent / Harness 评测与测试集：S036, S042
- `A052` Code / Shell Sandbox：S037（现场 AI Coding 进一步强化验证与安全需求）
- `A057` AI 生成代码验证：S037, S047
- `R001` RAG 离线入库 + 在线检索完整链路：S035, S039, S047
- `R007/R019` Hybrid Retrieval 与多路检索融合：S041
- `V002` Vector DB 选型：S047
- `D007/D008` Redis 线程模型和过期删除：S039, S040
- `M007` 并发状态更新、乐观锁与一致性：S040, S043
- `B005/B006` 并发 Tool/异步任务与不同失败类型处理：S039, S040

## Batch 04 对课程设计的新约束

1. **Agent Runtime 必须有 Lifecycle 章节**：Start → Run → Progress → Cancel → Timeout → Retry → Complete / Fail → Cleanup。
2. **Harness Performance 不能只讲“优化 Token”**：需要可观测的延迟分解、循环步数、Tool/Model/Retrieval Span 与 Regression Debugging。
3. **Agent Protocol 必须讲 Message / Event Model**：Tool Call/Result、状态、错误、进度和用户消息不能混为一种 Chat Message。
4. **Codex / Claude Code 源码研究升级为核心主线**：成熟产品实现不是“延伸阅读”，而是 Agent Harness 模块的权威实现证据。
5. **RAG Ingestion 要进入真实企业数据工程**：OCR、Layout、表格、跨页、TB 规模、Embedding 成本、增量更新都要系统覆盖。
6. **长任务可靠性与后端基础需要与 Agent State 联动学习**：MQ、Lease、Idempotency、Redis Lock、CAS、Recovery 不能作为孤立八股。
