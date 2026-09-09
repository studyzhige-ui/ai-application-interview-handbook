# Batch 11 — 规范化问题增量（HUMAN-A Only）

本文件只记录 Batch 11 相比 Batch 01–10 **真正新出现，或已经细化到值得独立建模** 的问题。

从本批开始，新增 canonical question 的正式证据只使用 **真人面试官 + A 级第一人称 HUMAN-A 来源**。绝大多数新来源都在强化已有 Python / MySQL / Redis / RAG / Agent Harness 问题，因此本批只新增 4 个 ID，不为了题量造题。

---

## LLM Foundation / Context

### L004 长 Context 为什么仍可能出现 Lost in the Middle？Context Window 变大为什么不等于有效信息利用能力线性提升？
- 来源：S130
- 标签：LLM Foundation / Long Context / Lost in the Middle / Attention / Context Engineering
- 核心拆解：Context Window Capacity、Position Bias、Relevant Evidence Placement、Long-context Retrieval、Attention Dilution、Prompt / Context Ordering、RAG vs Long Context、Evaluation。
- 课程边界：重点解释**应用工程中如何判断“模型放得下”与“模型用得好”是两回事**，不扩展成位置编码训练研究。
- 与 A017/A018 区别：A017/A018 聚焦 Harness 的 Context Compaction；L004 聚焦底层模型对长上下文的**有效利用限制**。

---

## Agent Harness / Tool Runtime

### A101 Tool / Function Calling 的真正执行边界是什么：模型生成结构化调用请求，还是模型自己执行 Tool？
- 来源：S140；S137 进一步强化
- 标签：Agent Harness / Tool Runtime / Function Calling / Protocol / Message Model
- 核心拆解：Tool Registration、Schema、Assistant Message、Structured Tool Call、Arguments Validation、Runtime Executor、Tool Result Message、Loop Continuation、Error Boundary。
- 核心判断：模型通常负责**决定并生成调用意图 / 结构化参数**；真正访问网络、文件、数据库或外部系统的是受控 Agent Runtime / Tool Executor。
- 与 A008/A009 区别：A008 关注 Tool Result 为什么是独立消息，A009 关注参数非法；A101 建模完整的 **Model ↔ Runtime Execution Boundary**。

---

## MySQL

### M013 MySQL redo log、undo log、binlog 分别解决什么问题？为什么 redo 与 binlog 需要两阶段提交来保持崩溃恢复一致性？
- 来源：S131
- 标签：MySQL / Redo Log / Undo Log / Binlog / Crash Recovery / Two-phase Commit
- 核心拆解：Atomicity / Durability、Rollback / MVCC、WAL、Redo Prepare / Commit、Binlog Write、Crash Point、Master-Slave / Point-in-time Recovery、InnoDB 与 Server Layer 边界。
- 课程意义：不能只背“三种日志定义”，需要能沿着**一次事务提交 + 不同宕机时刻**解释为什么会出现数据与 binlog 不一致，以及 2PC 如何约束这个窗口。

---

## Backend / Distributed System

### B020 多台机器如何生成全局唯一 ID？如果还要求趋势递增 / 有序，方案如何变化？
- 来源：S141
- 标签：Backend / Distributed ID / Snowflake / Database / Redis / Sequence / System Design
- 核心拆解：UUID、DB Auto Increment、Segment / Hi-Lo、Redis INCR、Snowflake-like ID、Clock Rollback、Worker ID、Monotonicity、Index Locality、Availability、Single-point Bottleneck。
- 与数据库主键问题联系：全局唯一只是一个要求；对 MySQL 主键还要考虑**有序性、页分裂、索引局部性和写入吞吐**。

---

# 已有 canonical questions 得到显著 HUMAN-A 强化

- `A001/A002/A003` Agent / Harness / Runtime / Agent Loop：S129, S131, S132, S140
- `A006–A010` Tool Schema / Discovery / Message / Validation：S129, S137, S140
- `A011/A013/A067` MCP / Skill / Registry / Progressive Loading：S129, S132, S135, S137
- `A014–A018` Context / Memory / Compaction：S130, S131, S132, S136
- `A020–A025` Multi-Agent / State / Reliability：S129, S130, S135
- `A026/A027/A034` Agent Evaluation / Bad Case / Trace：S129, S131, S135, S136
- `A083/A089/A099` Coding Verification / Cost / Production Harness：S131, S135, S137
- `L001–L003` Transformer / Sampling / KV Cache：S130, S134, S141
- `P002` Python GIL / Thread / Lock：S136
- `M001–M012` Index / Slow SQL / MVCC / Pagination / Cache Consistency：S132, S133, S138, S139, S141
- `D001–D015` Redis Data Structure / HA / Cache / Consistency：S133, S138, S141
- `B001–B019` Network / MQ / Idempotency / Reliability / Release：S131, S135, S138, S139, S141
- `R001–R040` Chunk / Retrieval / Evaluation / RAG Design：S130, S132, S134, S136, S138, S139

---

# Batch 11 对课程设计的新约束

1. **LLM Foundation 必须加入 Long-context Effectiveness**：Context Window 是容量，不等于有效利用率；Lost in the Middle 应与 RAG / Context Engineering 一起讲。
2. **Tool Runtime 要先纠正一个常见概念错误**：LLM 不是真正的执行器。模型输出结构化调用请求，Harness / Runtime 才承担权限、参数校验、副作用与执行事实。
3. **MySQL 日志不能停在八股定义**：AI Backend 面试已经会继续追到 redo/binlog 2PC 和 Crash Recovery。
4. **Backend Engineering 应包含 Distributed ID**：Agent / AI Service 仍然是分布式业务系统，需要处理 ID、索引局部性、幂等和状态关联。
5. **HUMAN-A 来源会让 canonical 增速下降**：这是质量门槛提升后的正常现象。后续更重要的是统计已有问题被多少独立真人面试反复命中。
