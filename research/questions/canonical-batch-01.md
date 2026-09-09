# Batch 01 — 规范化问题库（初版）

> 说明：这里的“命中来源数”是 Batch 01 中多少个 `Sxxx` 来源出现了同一核心问题，并不等于最终真实面试出现次数。后续会随着更多原始面经加入持续重算。

## Agent Harness / Runtime

### A001 一个完整的 Agent 系统通常包含哪些核心模块？
- 标签：Agent Harness / Architecture / Basic
- 来源：S003, S005, S007, S012, S014, S015
- 命中来源数：6
- 常见变体：完整流程、整体架构、核心能力、系统拆解。

### A002 Harness、Orchestrator、Workflow、Agent Runtime 的职责边界是什么？
- 标签：Agent Harness / Architecture / Comparison
- 来源：S005, S007, S008
- 命中来源数：3

### A003 ReAct 与 Plan-and-Execute / Plan 模式有什么区别，如何选型？
- 标签：Agent Harness / Planning / Comparison
- 来源：S003, S005, S006, S007, S012
- 命中来源数：5

### A004 Planning 应该由模型、框架还是显式工作流承担？
- 标签：Agent Harness / Planning / Design
- 来源：S005, S007
- 命中来源数：2

### A005 Agent 如何避免路径震荡、死循环或无效重复执行？
- 标签：Agent Harness / Runtime / Reliability
- 来源：S005, S010, S013
- 命中来源数：3

### A006 Tool 的设计原则是什么？Tool Schema / 参数约束如何设计？
- 标签：Agent Harness / Tool Runtime / Design
- 来源：S003, S007, S009, S012
- 命中来源数：4

### A007 Agent 如何判断何时需要调用 Tool，以及调用哪个 Tool？
- 标签：Agent Harness / Tool Routing / Principle
- 来源：S005, S006, S007
- 命中来源数：3

### A008 Tool 返回结果为什么需要独立消息类型？
- 标签：Agent Harness / Tool Runtime / Protocol
- 来源：S012
- 命中来源数：1

### A009 Tool/Function Call 返回 JSON 不合法或参数被模型捏造时如何处理？
- 标签：Agent Harness / Tool Runtime / Reliability
- 来源：S003, S009
- 命中来源数：2

### A010 工具数量过多、工具描述占满 Prompt 时如何扩展？
- 标签：Agent Harness / Tool Discovery / Context
- 来源：S005
- 命中来源数：1

### A011 MCP 解决什么问题？与 Function Calling、Skills、Agent 的关系是什么？
- 标签：Agent Harness / MCP / Comparison
- 来源：S002, S004, S005, S006, S013
- 命中来源数：5

### A012 MCP 如何承载业务 SOP 或企业流程？
- 标签：Agent Harness / MCP / Business Integration
- 来源：S004
- 命中来源数：1

### A013 Skill 应该如何分层、路由、沉淀和评测？
- 标签：Agent Harness / Skills / Architecture
- 来源：S005, S006, S007
- 命中来源数：3

### A014 Context、Chat History、Working Memory、Long-term Memory 有什么区别？
- 标签：Agent Harness / Context / Memory / Comparison
- 来源：S003, S005, S006, S007, S012, S014
- 命中来源数：6

### A015 短期记忆与长期记忆分别如何实现，什么信息应该长期保存？
- 标签：Agent Harness / Memory / Design
- 来源：S003, S005, S006, S007, S012, S014
- 命中来源数：6

### A016 多用户、多轮、多会话情况下 Memory/State 如何隔离和持久化？
- 标签：Agent Harness / State / Memory / Design
- 来源：S003
- 命中来源数：1

### A017 Agent Context 接近或超过 Context Window 时如何设计压缩？
- 标签：Agent Harness / Context / Compaction
- 来源：S001, S005, S006, S008
- 命中来源数：4

### A018 如何发现上下文压缩过度导致信息损失，并恢复质量？
- 标签：Agent Harness / Context / Compaction / Evaluation
- 来源：S006
- 命中来源数：1

### A019 Prompt 通常由哪些上下文部分组成，如何动态构建？
- 标签：Agent Harness / Prompt Assembly / Context
- 来源：S006
- 命中来源数：1

### A020 Multi-Agent 常见协作模式有哪些，什么时候不应该使用 Multi-Agent？
- 标签：Agent Harness / Multi-Agent / Comparison
- 来源：S003, S004, S007, S010, S012
- 命中来源数：5

### A021 子 Agent 之间如何传递上下文与状态？
- 标签：Agent Harness / Multi-Agent / State
- 来源：S003, S004, S010
- 命中来源数：3

### A022 多个 Agent 同时修改共享资源/文件时如何避免冲突？
- 标签：Agent Harness / Concurrency / Filesystem
- 来源：S005
- 命中来源数：1

### A023 Agent 执行中断、异常或崩溃后如何恢复？
- 标签：Agent Harness / Failure Recovery / Reliability
- 来源：S003, S009, S010
- 命中来源数：3

### A024 Retry 如何做到安全、幂等，避免重复副作用？
- 标签：Agent Harness / Retry / Idempotency
- 来源：S010
- 命中来源数：1

### A025 多用户并发下 Agent 服务卡死时如何做限流、队列与资源隔离？
- 标签：Agent Harness / Concurrency / Production
- 来源：S003, S010
- 命中来源数：2

### A026 如何评价 Agent 本身的能力，而不是只评价底层模型？
- 标签：Agent Harness / Evaluation / Methodology
- 来源：S003, S005, S006
- 命中来源数：3

### A027 Agent 离线评测集如何构建和持续维护？
- 标签：Agent Harness / Evaluation / Dataset
- 来源：S005, S006
- 命中来源数：2

### A028 如何把海量线上日志转化为有限、高价值、可回归的离线评测集？
- 标签：Agent Harness / Evaluation / Production
- 来源：S006
- 命中来源数：1

### A029 不同模型受限时，如何针对模型特点优化 Agent Harness，而不是只换模型？
- 标签：Agent Harness / Model Adaptation / Design
- 来源：S001, S006
- 命中来源数：2

### A030 Agent 为什么会幻觉、乱调 Tool，工程上如何约束？
- 标签：Agent Harness / Reliability / Guardrails
- 来源：S003, S010
- 命中来源数：2

## RAG

### R001 从文档进入系统到最终回答，完整 RAG 链路是什么？
- 标签：RAG / Architecture / Basic
- 来源：S002, S005, S006, S008, S014
- 命中来源数：5

### R002 长文档 / 大规模文档如何做 Chunking 与索引构建？
- 标签：RAG / Chunking / Design
- 来源：S002, S003, S009
- 命中来源数：3

### R003 没有清晰标题或结构的 Markdown/PDF 如何切块？
- 标签：RAG / Chunking / Edge Case
- 来源：S009
- 命中来源数：1

### R004 RAG 召回结果不相关或召回不到正确内容时，如何系统排查？
- 标签：RAG / Retrieval / Debugging
- 来源：S005, S009
- 命中来源数：2

### R005 Query Rewrite 如何优化召回？
- 标签：RAG / Query Transformation / Design
- 来源：S006, S009
- 命中来源数：2

### R006 HyDE 的中间生成质量如何评估？
- 标签：RAG / HyDE / Evaluation
- 来源：S004
- 命中来源数：1

### R007 Multi-way / Hybrid Retrieval 是什么，为什么需要？
- 标签：RAG / Retrieval / Hybrid
- 来源：S006
- 命中来源数：1

### R008 Rerank 为什么存在，如何放在检索链路中？
- 标签：RAG / Rerank / Principle
- 来源：S006
- 命中来源数：1

### R009 父子索引为什么能改善 RAG？
- 标签：RAG / Indexing / Parent-child
- 来源：S005
- 命中来源数：1

### R010 多跳 / 多文档问题如何设计多次检索与推理？
- 标签：RAG / Multi-hop / Advanced
- 来源：S006
- 命中来源数：1

### R011 向量检索效果应该如何评估？
- 标签：RAG / Evaluation / Retrieval
- 来源：S004, S010
- 命中来源数：2

### R012 RAG 评测集应该如何构建，观测哪些指标？
- 标签：RAG / Evaluation / Dataset
- 来源：S001, S006
- 命中来源数：2

### R013 RAG 与 Fine-tuning 的适用边界是什么？
- 标签：RAG / Fine-tuning / Comparison
- 来源：S006
- 命中来源数：1

### R014 知识库如何不停服热更新或增量更新？
- 标签：RAG / Index Lifecycle / Production
- 来源：S010
- 命中来源数：1

### R015 一万个长文档规模下如何设计可扩展知识库流水线？
- 标签：RAG / Data Pipeline / System Design
- 来源：S003
- 命中来源数：1

## Vector DB / Retrieval

### V001 向量数据库在 RAG/Agent 系统中具体承担什么职责？
- 标签：Vector DB / Architecture / Basic
- 来源：S002, S003, S004, S005
- 命中来源数：4

### V002 向量数据库如何选型？
- 标签：Vector DB / Selection / Comparison
- 来源：S004
- 命中来源数：1

### V003 语义检索从 Embedding 到 TopK 的完整实现链路是什么？
- 标签：Vector DB / Semantic Retrieval / Principle
- 来源：S003, S004
- 命中来源数：2

### V004 短 Query 与长 Chunk 的向量表示差异如何影响召回？
- 标签：Vector DB / Embedding / Retrieval Quality
- 来源：S009
- 命中来源数：1

### V005 Qdrant 与 Redis 为什么承担不同的数据职责？
- 标签：Vector DB / Redis / Data Layering
- 来源：S002
- 命中来源数：1

## Redis

### D001 Redis 在 AI Agent 系统里有哪些典型职责？
- 标签：Redis / AI Architecture / Basic
- 来源：S001, S002, S005, S013
- 命中来源数：4

### D002 Redis BigKey 如何产生、发现和治理？
- 标签：Redis / Memory / Production
- 来源：S002
- 命中来源数：1

### D003 Redis 数据结构及适用场景如何解释？
- 标签：Redis / Data Types / Basic
- 来源：S005, S013
- 命中来源数：2

### D004 Redis Lua 与内置原子命令如何选择？
- 标签：Redis / Atomicity / Lua
- 来源：S011
- 命中来源数：1

### D005 Redis 在高并发业务中如何做原子控制和一致性？
- 标签：Redis / Concurrency / Consistency
- 来源：S011
- 命中来源数：1

## MySQL

### M001 MySQL 索引为什么快，底层数据结构是什么？
- 标签：MySQL / Index / Principle
- 来源：S003, S005, S008
- 命中来源数：3

### M002 MySQL 事务隔离级别及其解决的问题是什么？
- 标签：MySQL / Transaction / Basic
- 来源：S003, S011
- 命中来源数：2

### M003 MVCC 如何实现并发读写与隔离？
- 标签：MySQL / MVCC / Principle
- 来源：S003
- 命中来源数：1

### M004 分库分表以后跨库查询和分页怎么处理？
- 标签：MySQL / Sharding / System Design
- 来源：S011
- 命中来源数：1

### M005 深分页为什么慢，游标/书签分页如何优化？
- 标签：MySQL / Pagination / Performance
- 来源：S011
- 命中来源数：1

### M006 如何为真实业务表设计主键、索引与查询模式？
- 标签：MySQL / Schema Design / Project
- 来源：S008
- 命中来源数：1

## Backend / System Design

### B001 IO 多路复用解决什么问题，为什么高并发服务需要它？
- 来源：S001

### B002 SSE 与 WebSocket 在 Agent 流式输出中如何选？
- 来源：S010

### B003 消息队列在 Agent 系统中承担什么作用？
- 来源：S005, S011

### B004 外部 Tool 已成功但 checkpoint 尚未落盘就宕机，如何避免恢复后重复执行？
- 来源：S010（相关幂等/恢复问题），后续需补直接原始来源

## Batch 01 对课程目录的直接影响

这批问题说明 Agent 模块必须把以下内容提升为一级章节，而不能作为附录：

- Harness vs Orchestrator / Runtime
- Context Assembly 与 Context Compaction
- Tool Runtime / Tool Message / Schema Validation
- Skills 与 Tool Discovery
- Filesystem / Shared Resource Concurrency
- Retry / Idempotency / Failure Recovery
- Evaluation Pipeline / Log-to-Eval
- Model-adaptive Harness Optimization
- Production Concurrency / Queue / Resource Budget

RAG 模块则必须明确加入：

- 非结构化文档切块边界案例
- Retrieval Debugging 方法论
- Query Rewrite / HyDE / Multi-way Retrieval
- Parent-child Index
- Multi-hop Retrieval
- Index Lifecycle / Zero-downtime Update
- 大规模文档 ingestion pipeline
