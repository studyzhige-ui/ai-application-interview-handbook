# Agent Harness / Runtime Canonical Questions — S001–S279 全库纵向扫描 v3

更新日期：2026-09-10

> 一级板块：**Agent Harness / Runtime**。本文件只保留 Agent 控制面与执行运行时：Loop、State、Context Assembly / Compaction、Memory、Tool / MCP / Skill、Checkpoint / Resume、Permission / Sandbox、Multi-Agent、Execution Trace、Evaluation、Coding Agent Runtime 等。通用 Network / Streaming Transport、Rate Limit / Backpressure、服务扩容与普通 Backend Observability 归 `AI Backend Engineering`；Long-context 模型本体限制归 `LLM Foundation`；端到端 Agent Backend 架构题归 `System Design`。
>
> 本文件所有 ACTIVE 条目的 `Primary Module = Agent Harness / Runtime`。正式课程还要额外研究 Claude Code / Codex 源码，但源码不能反向改变 HUMAN-A Source Count。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**39**
- MOVED：**4**（旧 `AGENT-013`, `033`, `039`, `040`）
- 证据范围：仅 `S001–S279`
- 当前版本：`v3`（Global Merge / Split Audit）

### 高频信号

- `AGENT-009` · 33：Context Compaction
- `AGENT-014` · 31：Memory Architecture
- `AGENT-018` · 28：Tool / Function Calling 完整链路
- `AGENT-024` · 27：Skill / Tool / Function / MCP / Rule / Workflow 边界
- `AGENT-001` · 25：Agent vs LLM / Chatbot / Workflow
- `AGENT-003` · 24：Agent Loop / Runtime
- `AGENT-020` · 22：Tool Call Failure Handling
- `AGENT-030` · 21：Multi-Agent / Sub-agent
- `AGENT-034` · 19：Agent Evaluation
- `AGENT-005` · 18：Agent Paradigm
- `AGENT-021` · 17：Dynamic Tool Discovery / Progressive Loading
- `AGENT-028` · 16：Permission / HITL / Sandbox
- `AGENT-036` · 15：Code Verification

---

## 2. ACTIVE Canonical Questions

### AGENT-001 · Agent 与普通 LLM Call / Chatbot / 固定 Workflow 的本质区别是什么？什么任务真正值得 Agent 化？
- **Topic**：Agent Boundary
- **Question Type**：Concept / Comparison
- **Depth**：L3
- **Source Count**：**25**
- **Evidence Sources**：`S004`, `S014`, `S018`, `S019`, `S022`, `S026`, `S027`, `S031`, `S038`, `S041`, `S045`, `S048`, `S061`, `S073`, `S081`, `S087`, `S109`, `S145`, `S222`, `S227`, `S230`, `S233`, `S247`, `S257`, `S275`

### AGENT-002 · Harness、Runtime、Orchestrator / Workflow Engine 分别解决什么问题？为什么“模型 + API”还不够？
- **Topic**：Harness / Runtime Boundary
- **Question Type**：Concept / Why
- **Depth**：L3
- **Source Count**：**13**
- **Evidence Sources**：`S001`, `S003`, `S004`, `S027`, `S032`, `S043`, `S135`, `S214`, `S233`, `S235`, `S236`, `S246`, `S265`

### AGENT-003 · 一个完整 Agent Loop / Runtime 从 User Input 到 Final Answer 怎样执行？Model、Tool、State、Context 各在哪一层？
- **Topic**：Agent Loop
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**24**
- **Evidence Sources**：`S001`, `S003`, `S012`, `S014`, `S015`, `S018`, `S021`, `S022`, `S026`, `S036`, `S038`, `S041`, `S043`, `S063`, `S073`, `S081`, `S087`, `S145`, `S214`, `S226`, `S231`, `S233`, `S266`, `S279`

### AGENT-004 · Agent Message / Event Model 应怎样设计？Assistant Text、Tool Call、Tool Result、System / User Message 为什么需要不同结构？
- **Topic**：Message / Event Model
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**8**
- **Evidence Sources**：`S012`, `S018`, `S033`, `S036`, `S063`, `S081`, `S214`, `S231`

### AGENT-005 · ReAct、Plan-Execute-Replan、Planner / Executor / Critic 等执行范式怎样选择？
- **Topic**：Agent Paradigm
- **Question Type**：Comparison / Trade-off
- **Depth**：L3
- **Source Count**：**18**
- **Evidence Sources**：`S014`, `S017`, `S021`, `S026`, `S031`, `S038`, `S039`, `S042`, `S044`, `S049`, `S061`, `S065`, `S073`, `S145`, `S214`, `S227`, `S247`, `S279`

### AGENT-006 · Agent 怎样判断任务已经完成并可靠停止？Max Step、Stop Condition、Dead Loop / Oscillation 如何检测？
- **Topic**：Termination / Loop Detection
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Source Count**：**14**
- **Evidence Sources**：`S017`, `S021`, `S022`, `S036`, `S042`, `S043`, `S044`, `S061`, `S073`, `S081`, `S214`, `S228`, `S236`, `S274`

### AGENT-007 · Agent Goal Drift / 执行方向偏离原始需求时，怎样发现并拉回主任务？
- **Topic**：Goal Control
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S042`, `S081`, `S214`

### AGENT-008 · 一次 Agent Context 包含什么？System / User、History、Memory、Retrieval、Tool Schema、Tool Result 怎样排序与组装？
- **Topic**：Context Assembly
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**12**
- **Evidence Sources**：`S015`, `S017`, `S026`, `S036`, `S063`, `S066`, `S081`, `S214`, `S227`, `S231`, `S240`, `S275`

### AGENT-009 · Context Window 接近上限时，怎样 Trim / Summarize / Compact，同时保留当前任务关键状态？
- **Topic**：Context Compaction
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**33**
- **Evidence Sources**：`S002`, `S003`, `S014`, `S016`, `S017`, `S026`, `S031`, `S032`, `S034`, `S037`, `S039`, `S043`, `S045`, `S048`, `S060`, `S063`, `S064`, `S066`, `S073`, `S081`, `S087`, `S109`, `S135`, `S145`, `S214`, `S227`, `S231`, `S236`, `S237`, `S240`, `S242`, `S250`, `S275`
- **Related Modules**：LLM Foundation（应用工程深度）

### AGENT-010 · Compaction / Summary 后如何验证信息没有丢坏？哪些状态必须保留，错误摘要如何纠正？
- **Topic**：Compaction Correctness
- **Question Type**：Failure Analysis / Evaluation
- **Depth**：L4
- **Source Count**：**13**
- **Evidence Sources**：`S003`, `S016`, `S017`, `S032`, `S039`, `S043`, `S048`, `S081`, `S214`, `S236`, `S237`, `S240`, `S275`

### AGENT-011 · Tool Result / 文件 / 日志过大时怎样压缩、引用、延迟加载或外部化，而不是全部塞进 Context？
- **Topic**：Large Tool Result / Context Offloading
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**11**
- **Evidence Sources**：`S017`, `S032`, `S042`, `S066`, `S081`, `S214`, `S231`, `S236`, `S240`, `S274`, `S275`

### AGENT-012 · Prompt Cache / Context Cache 如何降低重复 Token 成本？缓存哪些层，何时失效？
- **Topic**：Prompt / Context Cache
- **Question Type**：System Design / Cost
- **Depth**：L4
- **Source Count**：**5**
- **Evidence Sources**：`S017`, `S081`, `S109`, `S214`, `S253`

### AGENT-014 · Short-term / Working / Long-term Memory 怎样分层、写入、召回、更新与失效？
- **Topic**：Memory Architecture
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**31**
- **Evidence Sources**：`S003`, `S006`, `S017`, `S018`, `S027`, `S031`, `S034`, `S036`, `S038`, `S039`, `S044`, `S048`, `S050`, `S054`, `S060`, `S063`, `S065`, `S066`, `S073`, `S081`, `S087`, `S105`, `S145`, `S214`, `S227`, `S230`, `S236`, `S237`, `S241`, `S248`, `S253`

### AGENT-015 · Memory 什么时候从短期晋升长期？怎样做 Extraction / Consolidation / Retrieval-on-demand，而不是无限堆历史？
- **Topic**：Memory Lifecycle
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S017`, `S039`, `S044`, `S060`, `S081`, `S145`, `S214`, `S248`

### AGENT-016 · Long-term Memory 中过期摘要、错误事实或冲突信息如何发现、修正、版本化并避免污染后续决策？
- **Topic**：Memory Correctness / Staleness
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S042`, `S043`, `S081`, `S214`, `S236`, `S243`

### AGENT-017 · 多用户 / 多角色 / 多 Tenant 的 Memory、Context、Session 和权限怎样隔离？
- **Topic**：Multi-tenant State Isolation
- **Question Type**：System Design / Security
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S027`, `S033`, `S035`, `S060`, `S081`, `S194`, `S240`, `S276`

### AGENT-018 · Tool / Function Calling 从 Schema 暴露、模型选择、Structured Call、Runtime 执行到 Result 回填的完整链路是什么？
- **Topic**：Tool Calling Protocol
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**28**
- **Evidence Sources**：`S001`, `S009`, `S012`, `S015`, `S018`, `S021`, `S022`, `S023`, `S028`, `S038`, `S039`, `S041`, `S046`, `S049`, `S054`, `S057`, `S063`, `S064`, `S065`, `S068`, `S071`, `S081`, `S145`, `S214`, `S231`, `S233`, `S240`, `S277`

### AGENT-019 · 一个新 Tool 从定义、注册、Discovery、Schema Validation、调用到版本升级的生命周期怎样设计？
- **Topic**：Tool Lifecycle
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S001`, `S012`, `S022`, `S043`, `S057`, `S214`, `S236`, `S275`

### AGENT-020 · 单次 Tool Call 出现 Invalid Arguments / Invalid Schema / Permission / Execution / Timeout 等失败时，Runtime 怎样归一化错误、反馈给模型并决定 Repair / Retry / Fail？
- **Topic**：Tool Call Failure Semantics
- **Question Type**：Troubleshoot / Failure Analysis
- **Depth**：L4
- **Source Count**：**22**
- **Evidence Sources**：`S003`, `S015`, `S017`, `S021`, `S022`, `S034`, `S042`, `S043`, `S045`, `S050`, `S057`, `S060`, `S071`, `S073`, `S081`, `S145`, `S214`, `S236`, `S240`, `S245`, `S275`, `S277`
- **Related Modules**：AI Backend Engineering

### AGENT-021 · Tool 数量持续增长时怎样 Dynamic Discovery / Progressive Loading，避免所有 Schema 一次性挤占 Context？
- **Topic**：Tool Discovery / Progressive Loading
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**17**
- **Evidence Sources**：`S001`, `S017`, `S038`, `S039`, `S057`, `S081`, `S109`, `S135`, `S145`, `S214`, `S228`, `S231`, `S233`, `S252`, `S274`, `S275`, `S279`

### AGENT-022 · Structured Output / Tool Arguments 如何做 Schema Validation、Repair 与 Hallucination Handling？
- **Topic**：Structured Output / Validation
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Source Count**：**8**
- **Evidence Sources**：`S012`, `S018`, `S057`, `S071`, `S081`, `S214`, `S248`, `S253`

### AGENT-023 · MCP 解决什么标准化问题？Client / Server、Tools / Resources / Prompts 与 stdio / SSE / Streamable HTTP 怎样理解？
- **Topic**：MCP Protocol
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Source Count**：**18**
- **Evidence Sources**：`S009`, `S015`, `S017`, `S019`, `S021`, `S022`, `S023`, `S028`, `S033`, `S034`, `S038`, `S041`, `S049`, `S057`, `S214`, `S231`, `S238`, `S259`

### AGENT-024 · Skill、Tool、Function Calling、MCP、Rule / Prompt / Workflow 的职责边界是什么？
- **Topic**：Capability Abstraction Boundary
- **Question Type**：Comparison
- **Depth**：L4
- **Source Count**：**27**
- **Evidence Sources**：`S001`, `S009`, `S014`, `S018`, `S019`, `S020`, `S023`, `S028`, `S038`, `S039`, `S041`, `S049`, `S054`, `S055`, `S061`, `S081`, `S109`, `S214`, `S227`, `S228`, `S230`, `S231`, `S233`, `S238`, `S247`, `S252`, `S275`

### AGENT-025 · Skill 怎样做 Progressive Disclosure / Resource Loading？为什么不把所有 Instructions / Assets 一次性注入 Context？
- **Topic**：Skill Progressive Disclosure
- **Question Type**：Why / System Design
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S039`, `S081`, `S135`, `S214`, `S228`, `S231`, `S233`, `S252`, `S275`

### AGENT-026 · Agent 长耗时任务怎样 Timeout、Cancel、Interrupt、Resume？取消传播和资源清理怎样保证？
- **Topic**：Cancellation / Long-running Task
- **Question Type**：Failure Analysis / System Design
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S019`, `S034`, `S036`, `S047`, `S059`, `S081`, `S182`, `S214`, `S240`
- **Related Modules**：AI Backend Engineering, System Design

### AGENT-027 · Checkpoint / Persistence / Resume 应保存哪些 Runtime State？Crash 后怎样恢复到可继续执行状态？
- **Topic**：Checkpoint / Resume
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**12**
- **Evidence Sources**：`S034`, `S042`, `S059`, `S063`, `S081`, `S087`, `S105`, `S182`, `S209`, `S214`, `S241`, `S242`
- **Related Modules**：Redis, System Design

### AGENT-028 · Permission、Approval、HITL、Sandbox 如何限制 Agent 的写操作、代码执行和高风险外部副作用？
- **Topic**：Permission / Approval / Sandbox
- **Question Type**：Security / System Design
- **Depth**：L4
- **Source Count**：**16**
- **Evidence Sources**：`S015`, `S019`, `S025`, `S027`, `S030`, `S032`, `S037`, `S042`, `S059`, `S081`, `S214`, `S241`, `S245`, `S253`, `S254`, `S275`
- **Related Modules**：AI Backend Engineering

### AGENT-029 · Tool 已成功产生外部副作用，但 Checkpoint / DB 写失败或服务崩溃时，如何避免 Resume 后重复执行？
- **Topic**：Idempotency / External Side Effect
- **Question Type**：Failure Analysis / System Design
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S035`, `S042`, `S081`, `S182`, `S214`, `S242`
- **Related Modules**：AI Backend Engineering, System Design

### AGENT-030 · 什么时候使用 Multi-Agent / Sub-agent？怎样分工、通信、共享或隔离 Context / State？
- **Topic**：Multi-Agent Architecture
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Source Count**：**21**
- **Evidence Sources**：`S001`, `S002`, `S017`, `S026`, `S027`, `S028`, `S031`, `S034`, `S037`, `S042`, `S044`, `S058`, `S060`, `S061`, `S063`, `S064`, `S081`, `S145`, `S214`, `S228`, `S253`

### AGENT-031 · 多 Agent 并行修改同一文件 / Workspace 或共享资源时，如何避免 Conflict、Race、Lost Update？
- **Topic**：Workspace / Shared-resource Concurrency
- **Question Type**：System Design / Failure Analysis
- **Depth**：L4
- **Source Count**：**6**
- **Evidence Sources**：`S017`, `S027`, `S030`, `S032`, `S081`, `S214`

### AGENT-032 · Agent Runtime 怎样做 Model Routing？不同 Provider 的 Tool Protocol、Context 与错误语义如何适配？
- **Topic**：Model Routing / Runtime Adapter
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S032`, `S043`, `S044`, `S060`, `S081`, `S214`, `S236`, `S240`, `S246`
- **Related Modules**：LLM Foundation（应用工程深度）, System Design

### AGENT-034 · Agent / Harness 怎样做 Evaluation？如何把 Final Result、Process、Tool、Routing、Cost 与 Regression 分层验证？
- **Topic**：Agent Evaluation
- **Question Type**：Evaluation / System Design
- **Depth**：L4
- **Source Count**：**19**
- **Evidence Sources**：`S003`, `S007`, `S031`, `S041`, `S043`, `S048`, `S057`, `S058`, `S061`, `S063`, `S081`, `S214`, `S225`, `S228`, `S235`, `S236`, `S242`, `S243`, `S279`

### AGENT-035 · Agent Benchmark / Eval Dataset / Ground Truth 怎样构建？如何让 Offline Case 代表真实线上任务并用于 Regression？
- **Topic**：Benchmark Engineering
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S043`, `S057`, `S061`, `S081`, `S214`, `S225`, `S228`, `S236`, `S279`

### AGENT-036 · AI / Coding Agent 生成代码后，怎样用 Test、Diff、Regression、Review、Rollback 证明结果可交付？
- **Topic**：Code Verification
- **Question Type**：AI Coding / Verification
- **Depth**：L4
- **Source Count**：**15**
- **Evidence Sources**：`S003`, `S007`, `S009`, `S030`, `S032`, `S043`, `S046`, `S048`, `S061`, `S214`, `S226`, `S236`, `S245`, `S259`, `S279`

### AGENT-037 · Coding Agent 怎样理解大型 Repository？Vector RAG、AST / LSP、ripgrep / Filesystem Search、Dependency Graph 各适合什么？
- **Topic**：Repository Understanding
- **Question Type**：System Design / Comparison
- **Depth**：L4
- **Source Count**：**9**
- **Evidence Sources**：`S008`, `S038`, `S059`, `S132`, `S145`, `S218`, `S231`, `S236`, `S248`
- **Related Modules**：RAG

### AGENT-038 · Agent Runtime 如何制定跨 Model / Tool / Provider 的 Resilience Policy？Retry Eligibility、Backoff、Circuit Breaker、Fallback / Model Failover 应怎样组合？
- **Topic**：Agent Runtime Resilience Policy
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Source Count**：**12**
- **Evidence Sources**：`S003`, `S007`, `S019`, `S022`, `S045`, `S060`, `S073`, `S081`, `S214`, `S236`, `S240`, `S276`
- **Related Modules**：AI Backend Engineering

### AGENT-041 · Agent Self-evolution / Data Flywheel 怎样闭环？Bad Case、数据采集、Metric、上线验证与 Rollback 如何设计？
- **Topic**：Self-evolution / Data Flywheel
- **Question Type**：System Design / Evaluation
- **Depth**：L4
- **Source Count**：**3**
- **Evidence Sources**：`S243`, `S248`, `S265`

### AGENT-042 · Agent 正在执行时用户追加 / 修改需求，新指令怎样进入当前 State，并安全影响后续 Planning / Execution？
- **Topic**：Dynamic Instruction / Steering
- **Question Type**：System Design
- **Depth**：L4
- **Source Count**：**1**
- **Evidence Sources**：`S242`

### AGENT-043 · Agent Runtime 怎样建立 step / model / tool / state 级 Trace 与 Observability？如何用执行轨迹定位卡住、失败、延迟和 Token 异常，并支持 Replay / Debug？
- **Topic**：Execution Trace / Observability
- **Question Type**：Troubleshoot / System Design
- **Depth**：L4
- **Source Count**：**5**
- **Evidence Sources**：`S034`, `S129`, `S146`, `S240`, `S242`
- **Related Modules**：AI Backend Engineering

---

## 3. MOVED：十板块归属修正

| Legacy QID | 原问题 | 新 Primary Canonical |
|---|---|---|
| `AGENT-013` | Long Context / Lost-in-the-middle 等模型本体限制 | `LLM-002`, `LLM-003` |
| `AGENT-033` | SSE / WebSocket / HTTP Streaming Transport | `AIBE-006`, `AIBE-007`; FastAPI 实现另见 `FASTAPI-004` |
| `AGENT-039` | Concurrency / Backpressure / Fairness / Quota / Token Budget | `AIBE-013`, `AIBE-017` |
| `AGENT-040` | Agent Service 从 Demo 扩到多实例 / 多机器 | `SD-021`; 通用部署底座见 `AIBE-027`～`AIBE-031` |

---

## 4. Global Merge / Split Audit 修正

### Repository Understanding 统一 Primary

旧 `RAG-030` 与 `AGENT-037` 共享同一个核心知识模型，而且 `RAG-030` 的全部证据 `S038`, `S059`, `S132`, `S145`, `S218` 都已包含在 `AGENT-037` 中。Global Audit 后统一以 `AGENT-037` 为唯一 Primary；RAG 继续作为 Related Module。

### Backend Observability 与 Agent Execution Trace 拆分

旧 `AIBE-029` 同时混入了通用服务 Metrics / Log / Trace 和 Agent step / model / tool 执行轨迹。审计后：

- 通用 Backend Observability 留在 `AIBE-029`；
- Agent 执行轨迹单独建立 `AGENT-043`，来源 `S034`, `S129`, `S146`, `S240`, `S242`。

### Permission / Sandbox 证据补全

`S254` 明确追问 Agent Code Execution Boundary、Tool Calling Security、OpenClaw Permission Model、Reverse Shell / Docker Escape，因此加入 `AGENT-028`；Source Count 从 15 修正为 16。

### Tool Call Failure 与 Runtime Resilience 保持分离

`AGENT-020` 与 `AGENT-038` 词面相近，但不合并：

- `AGENT-020` 是**单次 Tool Call 的错误语义与反馈 / Repair**；
- `AGENT-038` 是**跨 Model / Tool / Provider 的 Runtime Resilience Policy**，关注 Retry Eligibility、Backoff、Circuit Breaker 和 Fallback。

这符合仓库 `schema.md` 的规则：正常调用 / 局部错误语义，与跨依赖恢复策略属于可以独立追问的能力。

---

## 5. Agent 课程的特殊证据规则

本文件的 Source Count 只代表 `S001–S279` HUMAN-A 市场证据。后续正式建设 Agent Harness / Runtime 教材时，还必须研究：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

两套成熟产品源码用于补齐课程知识边界、实现机制和工程 Trade-off，但**不能**反向增加任何 HUMAN-A Source Count。