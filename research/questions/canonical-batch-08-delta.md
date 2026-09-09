# Batch 08 — 规范化问题增量（AI Application 全链路）

本文件只记录 Batch 08 相比 Batch 01–07 **真正新出现，或已经细化到值得单独建模** 的问题。大量 MySQL / Redis / RAG / Agent 重复题只增加来源，不重复造 ID。

> 从本批起同时应用两道门槛：`source-quality-policy.md` 保证来源质量，`role-scope-policy.md` 保证岗位确实属于 AI Application / Agent 方向。

## Python / FastAPI

### P004 FastAPI Middleware 与 Dependency Injection 的职责边界是什么？横切逻辑、请求级资源和业务依赖分别应该放在哪里？
- 来源：S087
- 标签：FastAPI / Middleware / Dependency Injection / Request Lifecycle
- 核心拆解：Request/Response 横切处理、Auth Context、Tracing、DB Session、LLM Client、Feature Dependency、作用域、异常传播、测试替换。
- 与 P003 区别：P003 关注 Routing / Async Runtime；P004 聚焦 **服务组件的职责划分**。

### P005 `asyncio.gather` 与 `asyncio.as_completed` 在并发调用多个模型/检索服务时如何选？部分超时、部分成功时如何做 Deadline 与降级？
- 来源：S087
- 标签：Python / asyncio / Fan-out / Timeout / Partial Failure
- 核心拆解：结果顺序、先完成先消费、Exception Handling、Global Deadline、Per-call Timeout、Cancellation、Fallback、Partial Result。
- 课程意义：AI Service 很常见“一次请求 fan-out 到多个模型/Retriever”，这比只会 `await` 更接近真实工程。

### P006 FastAPI、Starlette、ASGI、Uvicorn 分别处在哪一层？一个 HTTP 请求从 Socket 到 Endpoint 大致经历什么？
- 来源：S088
- 标签：FastAPI / ASGI / Uvicorn / Starlette / Web Runtime
- 核心拆解：Server、Protocol、Framework、Routing、Middleware、Dependency、Endpoint、Response。
- 课程约束：FastAPI 必须作为独立模块系统学习，不能只背装饰器 API。

### P007 Python 的 Thread / Process / Asyncio 能否组合使用？AI 服务中如何把阻塞 I/O、异步 I/O 与 CPU-heavy 工作放到正确执行资源？
- 来源：S087, S095
- 标签：Python / Thread / Process / Asyncio / Executor / AI Backend
- 核心拆解：Event Loop、Thread Pool Bridge、Process Pool、GIL、C Extension、Backpressure、Worker Model。
- 与 P002 区别：P002 偏概念比较；P007 聚焦 **同一个生产服务中的组合架构**。

## MySQL / Backend

### M012 UUID 作为 MySQL 聚簇索引主键会带来哪些写入局部性、页分裂、索引体积和缓存命中问题？什么时候仍然值得使用？
- 来源：S092
- 标签：MySQL / Primary Key / UUID / B+Tree / Write Pattern
- 核心拆解：Random Insert、Page Split、Secondary Index PK Payload、Storage Size、Distributed ID、UUIDv7/有序 ID 思路。

### B017 AI 服务 / Agent Runtime 出现 OOM 时应该如何从进程、容器、对象生命周期、缓存、并发和流量维度系统排查？
- 来源：S098
- 标签：Backend / OOM / Debugging / Memory / Production
- 核心拆解：RSS/Heap、Container Limit、Request Concurrency、Large Payload、Context/Tool Result、Cache、Leak、Heap Profile、Restart 只是止血不是根因修复。

### B018 Kafka / MQ 以 User ID 等业务 Key 分区时，如何避免热点分区、负载倾斜与扩缩容后的顺序/迁移问题？
- 来源：S100
- 标签：Backend / Kafka / Partition / Hotspot / Ordering
- 核心拆解：Ordering Scope、Key Skew、Heavy User、Partition Count、Repartition、Virtual Shard / Hash Salting 的取舍。

## Vector Database

### V001 向量库需要按租户/类别隔离检索时，应如何选择 Collection、Partition、Metadata Filter 或独立实例？
- 来源：S087
- 标签：Vector DB / Milvus / Collection / Partition / Metadata Filter / Multi-tenant
- 核心拆解：Isolation、Index Build、Filter Selectivity、Operational Cost、Schema Evolution、Tenant Count、Hot Partition。
- 课程意义：向量数据库不能只学 HNSW/IVF，还要学 **真实业务数据组织方式**。

### V002 pgvector / Vector DB 中“文本最终是怎么存进去的”？Embedding、Vector Dimension、Metadata 与原文之间是什么关系？
- 来源：S089, S097
- 标签：Vector DB / Embedding / pgvector / Storage Model / Metadata
- 核心拆解：Text → Encoder → Dense Vector、原文/Chunk ID/Metadata、Dimension 与 Model 绑定、Update/Re-embedding、向量不是文本本身。

## RAG / Evaluation

### R036 医疗、政企等离线/私有环境如何部署 RAG，并同时解决模型、向量库、镜像、权限、日志脱敏与版本升级？
- 来源：S095
- 标签：RAG / Private Deployment / Offline / Security / Operations
- 核心拆解：Offline Image、Local Model、Private Vector DB、Artifact Registry、Dependency Pinning、Permission、Audit、PII Masking、Upgrade/Rollback。
- 与普通 RAG 部署区别：这是 **受限网络 + 敏感数据 + 可维护性** 的完整 Production 约束。

### R037 人工评测者对同一 AI 回答分歧很大时，如何判断 Evaluation Rubric 是否可靠并建立更稳定的人评基线？
- 来源：S096
- 标签：Evaluation / Human Eval / Inter-rater Agreement / Rubric
- 核心拆解：Rubric Clarity、Calibration Set、Pairwise vs Absolute、Multiple Raters、Adjudication、Agreement、Segmented Error Taxonomy。
- 课程意义：不能把“人工评测”当成天然 Ground Truth。

## Agent / AI Architecture

### A091 Prompt、RAG、Fine-tuning、Workflow、Agent 之间如何建立问题驱动的技术选型框架，而不是复杂问题默认上 Agent？
- 来源：S090
- 标签：AI Application / Architecture Decision / RAG / Fine-tune / Workflow / Agent
- 核心拆解：Knowledge Freshness、Determinism、Tool Need、Statefulness、Error Cost、Latency、Cost、Maintainability、Evaluation Difficulty。
- 意义：这是整套 Handbook 顶层必须具备的 **什么时候不用 Agent** 判断能力。

### A092 Prompt、Model、Retrieval Index、Tool/Workflow 配置共同组成 AI 应用版本时，如何做发布、Canary、回滚与可复现？
- 来源：S090
- 标签：AI Production / Versioning / Rollback / Prompt / Model / Retrieval
- 核心拆解：Version Bundle、Config Snapshot、Eval Gate、Canary、Feature Flag、Index Version、Model Provider Version、Trace Replay。
- 与单一模型版本区别：AI Application 的行为由多个可变组件共同决定。

### A093 A2A / Multi-Agent 通信如何防止递归对话、Ping-pong、无效委派和无限任务扩散？
- 来源：S087
- 标签：Multi-Agent / A2A / Loop Prevention / Budget / Routing
- 核心拆解：Hop Limit、Visited/Lineage、Task Ownership、Stop Condition、Delegation Budget、Cycle Detection、Supervisor、Idempotent Message。

### A094 Skill / Harness 从 Bad Case 中持续迭代时，如何治理“自我改进”的生成、评测、发布、回滚和权限边界？
- 来源：S094
- 标签：Agent Harness / Skill / Self-improvement / Evaluation / Governance
- 核心拆解：Proposal vs Auto-apply、Offline Eval、Sandbox、Human Approval、Version、Canary、Rollback、Provenance、No Self-modification by Default。
- 与 A082 区别：A082 聚焦错误 Memory/Skill 写入污染；A094 聚焦 **运行时能力定义自身的迭代发布流程**。

---

## 已有 canonical questions 得到显著强化

- `P001/P002/P003` Python dict / GIL / FastAPI Runtime：S087, S088, S091, S095
- `M001–M011` 索引、隔离、MVCC、慢 SQL、Redis-MySQL 一致性：S089, S091, S092, S097, S100
- `D001–D014` Redis 数据职责、淘汰/过期、BigKey、缓存问题：S089, S091, S092, S097
- `R001–R035` Chunk、Hybrid Retrieval、OCR/Layout、Rerank、GraphRAG、Evaluation：S087, S089, S093, S095, S096, S097
- `A006/A081/A088` Tool Schema / Tool Runtime / Tool Result：S087, S092, S099
- `A017/A071/A084/A090` Context Compaction 与派生上下文生命周期：S087, S090, S094, S099
- `A020/A021/A086` Multi-Agent 编排、通信与粒度治理：S087, S093, S098
- `A026/A069/A089` Agent Evaluation / Coding Verification：S092, S094, S096, S098
- `A037/A038/A083` Checkpoint / Resume / Crash Window：S093
- `A070/A085` Coding Agent / Harness 产品级实现研究：S088, S094, S099

## Batch 08 对课程设计的新约束

1. **FastAPI 必须一级成章**：Middleware/DI、ASGI/Uvicorn、Async Runtime、SSE、Lifespan、Client/Pool、Timeout/Cancellation 都是 AI Service 基础。
2. **Python 并发要从‘三者区别’升级到‘组合架构’**：Event Loop + Thread Pool + Process Pool 的边界需要真正会设计。
3. **Vector DB 要学 Data Organization**：Collection / Partition / Metadata Filter / Multi-tenant 不是 API 细节，而是生产选型。
4. **RAG 要覆盖私有化部署与评测可信度**：不仅是 Chunk → Embed → Retrieve。
5. **Agent 课程第一章就要会回答‘什么时候不该用 Agent’**。
6. **AI 应用需要整体版本管理**：Prompt、Model、Index、Tool、Config 必须能一起被复现和回滚。
7. **持续学习不能等于运行时自我修改**：Skill / Harness 的迭代必须通过 Eval、权限、发布和回滚治理。

本批新增 **14 道 canonical questions**。按当前工作口径，累计约 **191 道**。