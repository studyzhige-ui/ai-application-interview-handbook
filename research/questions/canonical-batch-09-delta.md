# Batch 09 — 规范化问题增量（全链路继续扩展）

本文件只记录 Batch 09 相比 Batch 01–08 **真正新出现，或细化到值得独立建模** 的问题。大量已有 Python / MySQL / Redis / Vector DB / RAG / Agent 问题只增加来源，不重复造 ID。

本批继续应用：

- `source-quality-policy.md`：保证来源质量；
- `role-scope-policy.md`：保证岗位属于 AI Application / Agent 目标方向。

---

## LLM Foundation

### L001 AI 应用工程师需要把 Transformer / Self-Attention / Multi-Head Attention 理解到什么程度，才能解释模型推理与应用层行为？
- 来源：S114
- 标签：LLM Foundation / Transformer / Attention / Inference
- 核心拆解：Token/Embedding、Attention、Q/K/V、Multi-Head、FFN、Residual/Norm、Autoregressive Decode、KV Cache 的应用层意义。
- 课程边界：理解**推理和应用行为**即可，不把主线扩展成 CUDA Kernel、分布式训练或研究型算法岗课程。

### L002 Temperature / Top-p 等解码参数如何影响随机性、稳定性与任务类型？生产 AI 应用应该如何调参与评测？
- 来源：S102
- 标签：LLM Foundation / Decoding / Temperature / Top-p / Production
- 核心拆解：Deterministic-ish Task、Creative Task、Sampling、Reproducibility、Eval Set、模型差异、不要只靠主观“感觉更好”。

---

## RAG / Knowledge System

### R038 当知识库中根本没有用户所需证据时，RAG 如何识别 Knowledge Gap，并在拒答、澄清、外部检索、人工升级和知识补录之间选择？
- 来源：S104
- 标签：RAG / Knowledge Gap / Abstention / Escalation / Grounding
- 核心拆解：No-evidence Detection、Retrieval Confidence、Unknown Handling、Ask User、External Source、Human Escalation、Knowledge Backfill、避免“没检索到也继续生成”。
- 与普通“降低幻觉”区别：本题聚焦 **Ground Truth 本身不存在于当前知识库**。

### R039 企业 RAG 正式建库前应该如何做 Corpus Discovery / Data Audit，而不是拿到文档就直接 Chunk + Embed？
- 来源：S104, S114
- 标签：RAG / Ingestion / Data Audit / Corpus Discovery / Enterprise
- 核心拆解：文件类型、扫描件/OCR、编码、表格/布局、重复文档、版本/时效、权限、Owner、更新频率、数据质量抽样、失败清单、容量/Embedding 成本估算。
- 课程意义：RAG 的第一步不是 Splitter，而是**理解数据资产和约束**。

---

## Agent Harness / Runtime

### A095 `AGENTS.md` / Project Rules / Repository Instructions 一类规则文件应该保存什么？如何设计作用域、优先级、继承、冲突和版本管理？
- 来源：S105
- 标签：Coding Agent / Agent Harness / Project Rules / Instruction Hierarchy
- 核心拆解：Coding Standard、Allowed Commands、Test Contract、Security Boundary、Directory Scope、Nested Rules、Override Priority、Versioning、Context Injection、Auditable Change。
- 课程约束：后续必须对照 `openai/codex` 与 `claude-code-source-private` 的真实实现研究，不把规则文件当成“一段长 Prompt”。

### A096 Agent 如何建立 Execution Truth，避免模型“声称工具已执行/文件已修改/订单已提交”但外部世界实际上没有发生动作？
- 来源：S110
- 标签：Agent Runtime / Tool Execution / Truth / Receipt / State
- 核心拆解：Tool Executor 为唯一执行入口、Typed Result、Execution Receipt、Operation ID、State Transition、Read-after-write / Reconciliation、模型文本不能作为 Side-effect Success 的事实来源。
- 与 Hallucination 区别：这是 **Action Grounding / External World Consistency**，不是普通回答事实错误。

### A097 Agent / AI 应用在上线前和真实流量中如何做 Release Validation、Canary、A/B Test 与效果回归？
- 来源：S111
- 标签：Agent Production / Release / A-B Test / Evaluation / Canary
- 核心拆解：Offline Eval Gate、Pre-production Scenario Test、Shadow Traffic、Canary、A/B、Success Metric、Guardrail Metric、Latency/Cost、Rollback Trigger、版本可复现。
- 与 A092 区别：A092 关注版本 Bundle 与回滚；A097 关注**如何证明一个新版本值得放量**。

### A098 Agent Memory 的“完整历史存储”与“当前模型可见上下文”为什么必须分离？Local / Cloud / DB 存储边界如何选择？
- 来源：S106
- 标签：Agent Memory / Transcript / Context / Persistence / Privacy
- 核心拆解：Immutable/Append-only Transcript、Visible Working Context、Summary/Compaction、Rehydration、Retention、TTL、Local-first、Cloud Sync、Multi-device、Privacy、Tenant Isolation。
- 与 A017/A071 区别：已有问题侧重 Context 压缩生命周期；本题聚焦 **Storage Truth 与 Model-visible Context 是两层系统**。

---

## AI Backend Engineering

### B019 一次 Agent 请求需要并发调用大量 Tool / Model / Retriever 时，如何实现 Bounded Concurrency，而不是无限创建任务？
- 来源：S112
- 标签：Backend / Concurrency / Semaphore / Tool Runtime / Backpressure
- 核心拆解：Semaphore、Worker Pool、Queue、Per-tenant Limit、Global Limit、Fairness、Deadline、Cancellation、Rate Limit vs Concurrency Limit、Backpressure、Partial Failure。
- 课程意义：这应进入 FastAPI / AI Backend Engineering，并与 Tool Runtime 双向链接。

---

## 已有 canonical questions 得到显著强化

- `P001–P007` Python / FastAPI / Async Runtime：S106, S109, S112
- `M001–M012` MySQL 索引、治理、一致性、分表：S103, S109
- `D001–D014` Redis BigKey、数据结构、分布式锁、缓存一致性：S103, S109, S112
- `V001/V002` Vector DB 组织与存储模型，以及 HNSW/IVF/选型：S104, S106, S113, S114
- `R001–R037` Chunk、Hybrid Retrieval、Rerank、Evaluation、OCR/Layout、大规模 RAG：S101, S104, S105, S108, S109, S113, S114
- `A020/A021/A086/A093` Multi-Agent 选型、通信、Topology、循环治理：S102, S105, S108, S110
- `A017/A071/A084/A090` Context Compaction / Summary Lifecycle：S101, S103, S106, S112
- `A081/A083/A088/A089` Tool Runtime、Failure、Side Effect、Coding Verification：S101, S102, S105, S110
- `A082/A094` Skill / Memory 持续学习与发布治理：S105, S110
- `B016–B018` Cache Failure、Rate Limit、MQ/Partition：S109, S112

---

# Batch 09 对课程设计的新约束

1. **需要补一个轻量但系统的 LLM Foundation 层**：Transformer、Attention、Sampling/Decoding、Token/KV Cache、模型调用与能力边界；深度服务于应用工程，不滑向训练 Infra。
2. **RAG 的第一章不能从 Chunk 开始**：真实企业项目应该先做 Corpus Discovery / Data Audit。
3. **RAG 必须会处理“知识库根本没有答案”**：Abstention、Escalation、Knowledge Backfill 是生产链路的一部分。
4. **Coding Agent 必须有 Project Rules / Instruction Hierarchy**，并以后用 Codex / Claude Code 源码校验。
5. **模型的自然语言自述不能成为执行事实**：外部动作必须由 Tool Runtime 的执行回执和状态转换证明。
6. **上线评测要从 Offline Eval 扩展到 Pre-prod / Shadow / Canary / A-B / Rollback**。
7. **并发不仅是 `asyncio.gather`**：Agent Tool Fan-out 必须有 Bounded Concurrency 和 Backpressure。
8. **Memory Persistence 与 Context Window 是两层系统**：完整 Transcript 可以长期存在，但模型只看到经过选择/压缩的 Working Context。

本批新增 **9 道 canonical questions**。按当前工作口径，累计约 **200 道**。