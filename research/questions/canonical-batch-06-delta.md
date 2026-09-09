# Batch 06 — 规范化问题增量（高置信来源）

本文件只记录 Batch 06 相比 Batch 01–05 **真正新出现，或已经细化到值得独立成为知识点** 的问题。

> Batch 06 的一个重要变化是：新增 canonical question 原则上优先由 `原始/第一人称｜高置信` 来源支撑。二次创作不再为了“扩题量”而创建大量 ID。

## Agent Harness / Runtime

### A081 Tool Executor / Tool Runtime 为什么应该成为独立运行时层？它需要提供哪些统一语义？
- 来源：S065, S066, S075
- 标签：Agent Harness / Tool Runtime / Executor / Reliability
- 核心拆解：Schema Validation、Permission、Timeout、Cancellation、Concurrency、Error Taxonomy、Retry Policy、Result Normalization、Audit、Trace Hook、Sandbox。
- 与 A006 区别：A006 重点是 Tool 如何设计；A081 重点是**所有 Tool 共用的执行基础设施**。

### A082 Memory / Skill 从 Bad Case 或模型输出中持续学习时，如何防止错误经验写入造成长期污染？
- 来源：S069, S075
- 标签：Agent Memory / Skills / Write Policy / Poisoning / Provenance
- 核心拆解：Write Gate、Source Provenance、Confidence、Human Review、TTL、Version、Canary、Rollback、Negative Feedback、错误记忆修正。
- 与 A049 区别：A049 解决“新旧事实冲突”；A082 解决**一开始写进去的内容就是错的**。

### A083 外部副作用已经成功，但 Checkpoint 尚未持久化就宕机，Resume 如何避免重复执行？
- 来源：S069
- 标签：Agent Runtime / Checkpoint / Crash Window / Idempotency / External Side Effect
- 核心拆解：Idempotency Key、Operation Ledger、Outbox/Inbox、External Reconciliation、Write-ahead State、Exactly-once Illusion、Compensation。
- 与 A038 区别：A038 是一般性的恢复后状态一致性；本题聚焦一个非常具体且危险的 **Side-effect → Checkpoint Crash Window**。

### A084 Context Compaction 的“信息没有丢”应该如何量化评估？
- 来源：S068, S075
- 标签：Agent Context / Compaction / Evaluation / Information Preservation
- 核心拆解：Task Constraint Retention、Entity/Fact Recall、Pending Step Recall、Tool Dependency Preservation、Needle Cases、Before/After Task Success、Token Saving Ratio。
- 与 A018 区别：A018 关注发现压缩过度后的恢复；A084 关注**在上线前/回归中如何证明压缩方案可靠**。

### A085 Coding Agent 为什么不一定使用传统“代码切块 → Embedding → Vector RAG”读取代码库？成熟产品还有哪些 Repo Navigation 路径？
- 来源：S074, S076
- 标签：Coding Agent / Code Retrieval / Repository Navigation / RAG / Tool Use
- 核心拆解：grep/search、directory traversal、symbol/index、targeted read、git diff/history、language server、code graph、on-demand context；以及什么时候 Code RAG 仍然有价值。
- 课程约束：后续必须对照 `openai/codex` 与 `claude-code-source-private` 的实际源码验证，不能只凭面经回答推断产品实现。

### A086 Multi-Agent 应该按什么粒度拆分？业务能力持续增长时如何避免 Agent Topology 无限膨胀？
- 来源：S071
- 标签：Multi-Agent / Granularity / Topology / Architecture Governance
- 核心拆解：Agent vs Skill vs Tool vs Workflow Node、领域边界、共享能力抽取、动态路由、Agent Registry、版本演进、协作成本。
- 与 A020 区别：A020 关注“什么时候用 Multi-Agent”；A086 进一步关注**用了以后如何治理规模**。

### A087 Agent Debugging 中 Trace、Log、State Snapshot 各提供什么证据？如果日志本身写错，如何避免 Agent 被错误观测信息误导？
- 来源：S065, S066, S071
- 标签：Agent Observability / Trace / Log / Evidence / Debugging
- 核心拆解：Trace Causality、Structured Event、Log Reliability、State Snapshot、Tool Result、Source Priority、Cross-validation、Telemetry Quality。
- 与 A034 区别：A034 解决“如何记录 Trace”；A087 解决**如何把可观测数据当证据使用，以及证据本身可能不可靠**。

### A088 Tool Result 很大时如何压缩，同时保留执行语义、来源、权限、安全标记和可验证性？
- 来源：S066, S069
- 标签：Agent Context / Tool Result / Compression / Provenance / Security
- 核心拆解：Raw Result Archive、Typed Result、Summary、Structured Fields、Truncation Policy、Taint/Trust Metadata、Citation/Source Pointer、Re-fetch Handle。
- 与普通 Context Summary 区别：Tool Result 可能是**不可信外部输入**，压缩时不能把安全边界和来源一起“总结掉”。

### A089 Coding Agent 的“修复正确”应该如何定义和验证，而不是只看 Patch 能否应用或测试是否变绿？
- 来源：S064, S071, S075
- 标签：Coding Agent / Verification / Evaluation / Regression
- 核心拆解：Compilation、Target Test、Regression Test、Static Analysis、Lint/Policy、Behavioral Contract、Scope of Change、No New Failure、Human Acceptance。
- 与 A057 区别：A057 是自动验证工具链；A089 更关注**正确性的评价维度与验收标准**。

### A090 Task Summary、File Summary、Process Notes 等“派生上下文产物”应该如何生成、更新、失效和重建？
- 来源：S075
- 标签：Agent Context / Derived Artifact / Summary / Lifecycle
- 核心拆解：Source-of-truth、Version、Dependency、Invalidation、Incremental Update、Rebuild、Provenance、Staleness Detection。
- 意义：Context Engineering 不能把 Summary 当成一次性字符串，它们实际是需要生命周期管理的 Runtime Artifact。

## RAG / Retrieval

### R034 表格、章节结构和跨段关系为什么需要 Structure-preserving Ingestion，而不能一律转成纯文本 Chunk？
- 来源：S066
- 标签：RAG / Ingestion / Table / Structure / Layout
- 核心拆解：HTML/Markdown Table、Row/Column Semantics、Header Association、Parent Section、Cross-page Context、Structured Metadata。
- 与 R029 区别：R029 重点是 OCR/Layout 混合文档；R034 聚焦**解析后如何保住结构语义供检索和回答使用**。

### R035 Hybrid Retrieval 的收益应该如何通过消融实验量化，而不是只说“BM25 + Vector 更好”？
- 来源：S066
- 标签：RAG / Hybrid Retrieval / Evaluation / Ablation
- 核心拆解：Dense-only、Sparse-only、Hybrid、Rerank 的分阶段 Recall@K / MRR / NDCG / Answer Success；按 Query Type 分桶比较。
- 与 R016 区别：R016 主要验证 Chunk Strategy；R035 专门验证**检索组件增量价值**。

## Backend / Database

### B016 分布式限流中的 Token Bucket、Leaky Bucket、Sliding Window 各有什么行为差异，Agent 系统应如何分层使用？
- 来源：S073
- 标签：Backend / Rate Limit / Distributed System / Agent Production
- 核心拆解：Burst、Smooth Rate、Window Boundary、Redis/Lua 原子性、Tenant/User/Tool/Model 分层限额、Token Budget 与请求 QPS 的区别。

### M010 MySQL/关系型数据库中的“索引失效”应该如何从查询条件、联合索引顺序、函数/隐式转换和 LIKE 模式系统分析？
- 来源：S073
- 标签：MySQL / Index / Query Optimization / Basic
- 核心拆解：Leftmost Prefix、Range、Function、Type Conversion、Leading Wildcard、OR/Statistics/Optimizer；要求结合 EXPLAIN 验证，而不是背固定清单。

## 已有 canonical questions 得到显著强化

- `A002/A065` Harness 与框架、自研 Runtime 边界：S064, S065, S075
- `A006/A009/A081` Tool Schema、Error Taxonomy、Executor：S065, S066, S072, S075
- `A017/A018/A071` Context Compaction 生命周期：S068, S070, S072, S075
- `A020/A021/A039` Multi-Agent、共享 State、文件冲突：S064, S067, S069, S070, S072
- `A026/A027/A069` Agent/Harness Evaluation：S064, S067, S068, S072, S075
- `A037/A038/A077` Checkpoint / Resume / External Reconciliation：S065, S066, S067, S069
- `A046/A052/A075` Trust、Sandbox、Authorization：S064, S067, S069, S073
- `A056` Multi-model Provider Adapter：S064, S075
- `A070` Codex / Claude Code 源码级实现追问：S064, S074, S076
- `R007/R019/R025` Hybrid Retrieval / RRF：S065, S066, S073
- `R012/R016/R032` RAG Evaluation / Attribution：S066, S072, S073
- `M001/M002/M003/M008` MySQL 基础：S066, S073

## Batch 06 对课程设计的新约束

1. **Tool Runtime 必须单独成体系**：Tool 不只是 Schema；必须有 Executor、权限、超时、取消、错误分类、并发、Trace、Sandbox 和结果标准化。
2. **Memory/Skill 必须有 Write Safety**：读记忆前要防 Stale，写记忆前更要防错误知识长期污染。
3. **Checkpoint 必须讲 Crash Window**：特别是“外部动作成功、内部状态未落盘”的恢复语义。
4. **Context Compaction 必须能被评测**：Token 节省不是唯一指标，需要证明任务约束与关键事实仍然保留。
5. **Coding Agent Retrieval 必须回到成熟产品源码**：Repo Search / Read / Symbol / Diff / Index / RAG 的真实组合由 Codex / Claude Code 源码校验。
6. **Observability 要区分记录与证据质量**：有 Trace 不代表能正确 Debug；日志/遥测本身也会出错。
7. **Multi-Agent 要加入 Topology Governance**：避免“一个业务模块一个 Agent”无限膨胀。
8. **Coding Verification 要从‘跑测试’升级为验收体系**：范围、回归、静态规则、行为契约和用户目标都要覆盖。
