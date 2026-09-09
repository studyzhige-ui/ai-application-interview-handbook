# Batch 10 — 规范化问题增量（基础工程 + Runtime 纵深）

本文件只记录 Batch 10 相比 Batch 01–09 **真正新出现，或已经细化到值得独立建模** 的问题。大量 Python / MySQL / Redis / Vector DB / RAG / Agent 重复题只增加来源，不重复造 ID。

本批继续应用：

- `source-quality-policy.md`：保证来源真实性和信息密度；
- `role-scope-policy.md`：保证岗位属于 AI Application / Agent 目标方向。

---

## LLM Foundation

### L003 KV Cache / Prefix Cache 在大模型推理中解决什么问题？AI 应用工程师需要理解到什么程度？
- 来源：S115
- 标签：LLM Foundation / Inference / KV Cache / Prefix Cache / Latency / Memory
- 核心拆解：Autoregressive Decode 为什么会重复计算历史 Token、K/V 如何复用、Context Length 对 Cache Memory 的影响、TTFT / Decode Latency、静态 Prompt Prefix 对缓存命中的意义、模型/Provider Cache 边界。
- 课程边界：重点理解 **应用延迟、显存/成本和 Context 组织的关系**，不扩展成 CUDA Kernel 实现课程。
- 与 L001/L002 区别：L001 是 Transformer / Attention 基础，L002 是 Sampling；L003 聚焦 **Inference Runtime**。

---

## RAG / Retrieval

### R040 Bi-Encoder 与 Cross-Encoder 为什么通常分别用于大规模召回和 Rerank？质量、计算量与延迟如何权衡？
- 来源：S116
- 标签：RAG / Retrieval / Bi-Encoder / Cross-Encoder / Rerank / Latency
- 核心拆解：Independent Encoding、Vector Index、Query-Document Joint Encoding、Candidate Size、Recall vs Precision、Latency Budget、Batching、TopK → Rerank TopN。
- 课程意义：Reranker 不能只理解成“第二个模型”；需要理解为什么**召回与精排采用不同模型结构**。

---

## Agent Harness / Runtime

### A099 层级 Agent / Multi-Agent 的 Token 与 Cost 应如何准确归因，避免 Sub-agent、Tool、取消和迟到结果造成漏算或重复计算？
- 来源：S118
- 标签：Agent Harness / Observability / Cost Accounting / Sub-agent / Token Usage
- 核心拆解：Request/Task/Agent/Model Call 层级 ID、Parent-Child Attribution、Concurrent Aggregation、Provider Usage Normalization、Tool/RAG Cost、Disconnect/Cancel、Late Completion、Idempotent Usage Event、Cost Ledger、Trace Correlation。
- 与普通“Token 优化”区别：本题不是怎么少用 Token，而是**系统如何知道自己到底用了多少，以及成本属于谁**。

### A100 Agent 为什么不应该默认直接访问数据库？数据库能力如何通过受治理的 Tool / Service Boundary 暴露给模型？
- 来源：S120
- 标签：Agent Harness / Data Access / Authorization / Tool Runtime / Database Security
- 核心拆解：Read/Write Separation、Allowlist、Parameterized Query、Tenant Isolation、Row/Column Scope、AuthZ、Audit、Rate Limit、Transaction Boundary、Sensitive Schema、SQL Injection、Side-effect Approval、Service API vs Direct DB。
- 与 A075 权限治理区别：A075 是一般 Tool / Agent Authorization；A100 专门聚焦 **Data Plane / Database Access Boundary**。

---

## Redis

### D015 Redis Lua / 多 Key 原子操作在 Cluster 下有哪些 Hash Slot 边界？Failover、迁槽和重试时如何保证业务语义？
- 来源：S128
- 标签：Redis / Lua / Cluster / Hash Slot / Atomicity / Reliability
- 核心拆解：Same-slot Requirement、Hash Tag、Cross-slot Operation、Script Atomicity Scope、MOVED/ASK、Retry、Idempotency、Failover、Resharding、什么时候应该把多 Key 原子逻辑上移到业务层或重新设计 Key。
- 与 D004 区别：D004 讨论 Lua 与普通原子命令怎么选；D015 聚焦 **Redis Cluster 条件下原子性的现实边界**。

---

## 已有 canonical questions 得到显著强化

- `L001/L002` LLM Foundation：S115, S119
- `P001–P007` Python / Runtime / FastAPI：S119, S121, S124, S127
- `M001–M012` MySQL 索引、MVCC、主键、分页、Cache Consistency：S117, S118, S121, S126, S127, S128
- `D001–D014` Redis 数据职责、BigKey、HotKey、锁、Cluster、一致性：S117, S118, S121, S122, S125, S126, S127, S128
- `V001–V005` Vector DB 职责、选型、Embedding / Similarity / TopK：S116, S120
- `R001–R039` RAG 链路、Hybrid Retrieval、RRF、Rerank、评测：S116, S117, S121, S123, S125, S126, S127
- `A001/A003/A020` Agent Architecture / ReAct / Multi-Agent：S115, S121, S122, S123, S125, S126, S128
- `A009` Structured Output / Tool 参数校验：S119
- `A010/A013/A067` Tool / Skill Progressive Discovery 与 Registry：S115, S122, S128
- `A014–A018/A049/A098` Context / Memory / Conflict / Transcript：S115, S119, S121, S123
- `A026/A027/A034/A087/A097` Evaluation / Trace / Release Validation：S115, S116, S119, S122
- `A046/A054/A075` Security / Tool Governance / Authorization：S120
- `B016–B019` Cache Failure、Rate Limit、MQ、Bounded Concurrency：S117, S118, S121, S122, S125, S126, S127

---

# Batch 10 对课程设计的新约束

1. **LLM Foundation 需要加入 Inference Runtime 视角**：KV Cache、Context Length、TTFT/Decode、Prefix Reuse 应服务于 AI 应用延迟和成本理解。
2. **RAG / Vector DB 要解释 Encoder 架构**：Bi-Encoder / Cross-Encoder 是理解“为什么先召回再精排”的关键。
3. **Agent Observability 必须包含 Cost Accounting**：Trace 只有链路还不够，还需要能够对父子 Agent、模型、Tool、RAG 和取消任务做准确成本归因。
4. **Agent Data Access 必须有受治理边界**：不要把“LLM 可以调 SQL”直接等价于“LLM 获得数据库连接”。
5. **Redis Lua 不能脱离 Cluster 学**：单机环境下的原子性结论需要补上 Hash Slot / Failover / Resharding 的生产边界。
6. **研究统计需要增加 `interviewer_type`**：真人面试与自动化 AI 面试可以共同提供岗位信号，但后续频率分析不应默认等权。

本批新增 **5 道 canonical questions**。按当前工作口径，累计约 **205 道**。
