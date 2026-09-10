# Agent Harness / Runtime Canonical Questions — S001–S279 全库纵向扫描 v1

更新日期：2026-09-10

> 本文件只记录冻结 HUMAN-A 面经中真实出现的 Agent Harness / Runtime 考察信号。它不是最终 Agent 课程目录。最终教材还必须用 `studyzhige-ui/claude-code-source-private` 与 `openai/codex` 的成熟实现校准完整能力边界；源码研究不能反向虚增本文件的“面试频率”。

## 1. 当前扫描结论

- Canonical Questions：**42** 道
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数；同一来源内连续追问只计一次
- 当前版本：`v1`；五大核心模块完成后做跨模块 Merge / Split 审计

### 高频信号

- **AGENT-009** · 33 个来源 · 🔥🔥🔥：Context Window 接近上限时，怎样 Trim / Summarize / Compact，同时保留当前任务关键状态？
- **AGENT-014** · 31 个来源 · 🔥🔥🔥：Short-term / Working / Long-term Memory 怎样分层、写入、召回、更新与失效？
- **AGENT-018** · 28 个来源 · 🔥🔥🔥：Tool / Function Calling 从 Schema 暴露、模型选择、Structured Call、Runtime 执行到 Result 回填的完整链路是什么？
- **AGENT-024** · 27 个来源 · 🔥🔥🔥：Skill、Tool、Function Calling、MCP、Rule / Prompt / Workflow 的职责边界是什么？
- **AGENT-001** · 25 个来源 · 🔥🔥🔥：Agent 与普通 LLM Call / Chatbot / Workflow 的本质区别是什么，什么任务值得 Agent 化？
- **AGENT-003** · 24 个来源 · 🔥🔥🔥：一个完整 Agent Loop / Runtime 从 User Input 到 Final Answer 怎样执行？
- **AGENT-020** · 22 个来源 · 🔥🔥🔥：Tool Failure / Invalid Call / Timeout / Permission Error 怎样分类、反馈、Retry、Fallback 与 Recovery？
- **AGENT-030** · 21 个来源 · 🔥🔥🔥：什么时候使用 Multi-Agent / Sub-agent，怎样分工、通信、共享 / 隔离 Context 与 State？
- **AGENT-034** · 19 个来源 · 🔥🔥🔥：Agent / Harness 怎样做 Evaluation，如何把 Final Result、Process、Tool、Routing、Cost 与 Regression 分层验证？
- **AGENT-005** · 18 个来源 · 🔥🔥🔥：ReAct、Plan-Execute-Replan、Planner / Executor / Critic 等范式怎样选择？
- **AGENT-021** · 17 个来源 · 🔥🔥🔥：Tool 数量持续增长时怎样 Dynamic Discovery / Progressive Loading，避免所有 Schema 挤占 Context？
- **AGENT-028** · 15 个来源 · 🔥🔥🔥：Permission、Approval、HITL、Sandbox 如何限制 Agent 的写操作、代码执行和高风险外部副作用？
- **AGENT-036** · 15 个来源 · 🔥🔥🔥：AI / Coding Agent 生成代码后，怎样用 Test、Diff、Regression、Review、Rollback 证明结果可交付？

---

## 2. Canonical Questions

### AGENT-001 · Agent 与普通 LLM Call / Chatbot / 固定 Workflow 的本质区别是什么？什么任务真正值得 Agent 化？

- **Topic**：Agent Boundary
- **Question Type**：Concept / Comparison
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**25**
- **Evidence Sources**：`S004`, `S014`, `S018`, `S019`, `S022`, `S026`, `S027`, `S031`, `S038`, `S041`, `S045`, `S048`, `S061`, `S073`, `S081`, `S087`, `S109`, `S145`, `S222`, `S227`, `S230`, `S233`, `S247`, `S257`, `S275`

**真实问法变体：**
- Agent 相比直接调用 LLM 多了什么？
- 为什么不是普通 Workflow？
- 什么复杂任务才值得引入 Agent？

### AGENT-002 · Harness、Runtime、Orchestrator / Workflow Engine 分别解决什么问题？为什么“模型 + API”还不够？

- **Topic**：Harness / Runtime Boundary
- **Question Type**：Concept / Why
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**13**
- **Evidence Sources**：`S001`, `S003`, `S004`, `S027`, `S032`, `S043`, `S135`, `S214`, `S233`, `S235`, `S236`, `S246`, `S265`

**真实问法变体：**
- Agent Harness 到底是什么？
- Harness 与 Orchestrator 有什么区别？
- 从零搭 Harness 至少要有哪些能力？

### AGENT-003 · 一个完整 Agent Loop / Runtime 从 User Input 到 Final Answer 怎样执行？Model、Tool、State、Context 各在哪一层？

- **Topic**：Agent Loop
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**24**
- **Evidence Sources**：`S001`, `S003`, `S012`, `S014`, `S015`, `S018`, `S021`, `S022`, `S026`, `S036`, `S038`, `S041`, `S043`, `S063`, `S073`, `S081`, `S087`, `S145`, `S214`, `S226`, `S231`, `S233`, `S266`, `S279`

**真实问法变体：**
- 最小 Agent Loop 怎么写？
- 模型是否真的直接执行 Tool？
- 上一轮 Tool Result 怎样进入下一轮？

### AGENT-004 · Agent Message / Event Model 应怎样设计？Assistant Text、Tool Call、Tool Result、System / User Message 为什么需要不同结构？

- **Topic**：Message / Event Model
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S012`, `S018`, `S033`, `S036`, `S063`, `S081`, `S214`, `S231`

### AGENT-005 · ReAct、Plan-Execute-Replan、Planner / Executor / Critic 等执行范式怎样选择？

- **Topic**：Agent Paradigm
- **Question Type**：Comparison / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**18**
- **Evidence Sources**：`S014`, `S017`, `S021`, `S026`, `S031`, `S038`, `S039`, `S042`, `S044`, `S049`, `S061`, `S065`, `S073`, `S145`, `S214`, `S227`, `S247`, `S279`

### AGENT-006 · Agent 怎样判断任务已经完成并可靠停止？Max Step、Stop Condition、Dead Loop / Oscillation 如何检测？

- **Topic**：Termination / Loop Detection
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**14**
- **Evidence Sources**：`S017`, `S021`, `S022`, `S036`, `S042`, `S043`, `S044`, `S061`, `S073`, `S081`, `S214`, `S228`, `S236`, `S274`

**真实问法变体：**
- 达到 Max Step 仍未完成怎么办？
- Agent 在两条执行路径之间来回震荡怎么处理？
- 如何识别反复读同一文件 / 重复调用 Tool？

### AGENT-007 · Agent Goal Drift / 执行方向偏离原始需求时，怎样发现并拉回主任务？

- **Topic**：Goal Control
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S042`, `S081`, `S214`

### AGENT-008 · 一次 Agent Context 到底包含什么？System / Developer / User、History、Memory、Retrieval、Tool Schema、Tool Result 怎样排序与组装？

- **Topic**：Context Assembly
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**12**
- **Evidence Sources**：`S015`, `S017`, `S026`, `S036`, `S063`, `S066`, `S081`, `S214`, `S227`, `S231`, `S240`, `S275`

### AGENT-009 · Context Window 接近上限时，怎样 Trim / Summarize / Compact，同时保留当前任务关键状态？

- **Topic**：Context Compaction
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**33**
- **Evidence Sources**：`S002`, `S003`, `S014`, `S016`, `S017`, `S026`, `S031`, `S032`, `S034`, `S037`, `S039`, `S043`, `S045`, `S048`, `S060`, `S063`, `S064`, `S066`, `S073`, `S081`, `S087`, `S109`, `S135`, `S145`, `S214`, `S227`, `S231`, `S236`, `S237`, `S240`, `S242`, `S250`, `S275`

**真实问法变体：**
- Context 满了怎么办？
- 1M Context 仍不够怎么办？
- 文件很大且每个字符都重要，不能直接截断怎么办？

### AGENT-010 · Compaction / Summary 后如何验证信息没有丢坏？哪些信息必须保留，错误摘要如何纠正？

- **Topic**：Compaction Correctness
- **Question Type**：Failure Analysis / Evaluation
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**13**
- **Evidence Sources**：`S003`, `S016`, `S017`, `S032`, `S039`, `S043`, `S048`, `S081`, `S214`, `S236`, `S237`, `S240`, `S275`

### AGENT-011 · Tool Result / 文件 / 日志过大时怎样压缩、引用、延迟加载或外部化，而不是全部塞进 Context？

- **Topic**：Large Tool Result / Context Offloading
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S017`, `S032`, `S042`, `S066`, `S081`, `S214`, `S231`, `S236`, `S240`, `S274`, `S275`

### AGENT-012 · Prompt Cache / Context Cache 如何提高命中率并降低重复 Token 成本？缓存哪些层，何时失效？

- **Topic**：Prompt / Context Cache
- **Question Type**：System Design / Cost
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S017`, `S081`, `S109`, `S214`, `S253`

### AGENT-013 · Long Context 为什么不等于无限可靠？Lost-in-the-middle、Noise、输出空间挤压与注意力稀释怎样影响 Agent？

- **Topic**：Long Context Limits
- **Question Type**：Why / Failure Analysis
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S002`, `S017`, `S060`, `S066`, `S227`, `S246`, `S250`

### AGENT-014 · Short-term / Working / Long-term Memory 怎样分层、写入、召回、更新与失效？

- **Topic**：Memory Architecture
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**31**
- **Evidence Sources**：`S003`, `S006`, `S017`, `S018`, `S027`, `S031`, `S034`, `S036`, `S038`, `S039`, `S044`, `S048`, `S050`, `S054`, `S060`, `S063`, `S065`, `S066`, `S073`, `S081`, `S087`, `S105`, `S145`, `S214`, `S227`, `S230`, `S236`, `S237`, `S241`, `S248`, `S253`

### AGENT-015 · Memory 什么时候从短期晋升长期？怎样做 Extraction / Consolidation / Retrieval-on-demand，而不是无限堆历史？

- **Topic**：Memory Lifecycle
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S017`, `S039`, `S044`, `S060`, `S081`, `S145`, `S214`, `S248`

### AGENT-016 · Long-term Memory 中过期摘要、错误事实或冲突信息如何发现、修正、版本化并避免污染后续决策？

- **Topic**：Memory Correctness / Staleness
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S042`, `S043`, `S081`, `S214`, `S236`, `S243`

### AGENT-017 · 多用户 / 多角色 / 多 Tenant 的 Memory、Context、Session 和权限怎样隔离？

- **Topic**：Multi-tenant State Isolation
- **Question Type**：System Design / Security
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S027`, `S033`, `S035`, `S060`, `S081`, `S194`, `S240`, `S276`

### AGENT-018 · Tool / Function Calling 从 Schema 暴露、模型选择、Structured Call、Runtime 执行到 Result 回填的完整链路是什么？

- **Topic**：Tool Calling Protocol
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**28**
- **Evidence Sources**：`S001`, `S009`, `S012`, `S015`, `S018`, `S021`, `S022`, `S023`, `S028`, `S038`, `S039`, `S041`, `S046`, `S049`, `S054`, `S057`, `S063`, `S064`, `S065`, `S068`, `S071`, `S081`, `S145`, `S214`, `S231`, `S233`, `S240`, `S277`

### AGENT-019 · 一个新 Tool 从定义、注册、Discovery、Schema Validation、调用到卸载 / 版本升级的生命周期怎样设计？

- **Topic**：Tool Lifecycle
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S001`, `S012`, `S022`, `S043`, `S057`, `S214`, `S236`, `S275`

### AGENT-020 · Tool Failure / Invalid Call / Timeout / Permission Error 怎样分类、反馈、Retry、Fallback 与 Recovery？

- **Topic**：Tool Failure Handling
- **Question Type**：Troubleshoot / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**22**
- **Evidence Sources**：`S003`, `S015`, `S017`, `S021`, `S022`, `S034`, `S042`, `S043`, `S045`, `S050`, `S057`, `S060`, `S071`, `S073`, `S081`, `S145`, `S214`, `S236`, `S240`, `S245`, `S275`, `S277`

### AGENT-021 · Tool 数量持续增长时怎样 Dynamic Discovery / Progressive Loading，避免所有 Schema 一次性挤占 Context？

- **Topic**：Tool Discovery / Progressive Loading
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**17**
- **Evidence Sources**：`S001`, `S017`, `S038`, `S039`, `S057`, `S081`, `S109`, `S135`, `S145`, `S214`, `S228`, `S231`, `S233`, `S252`, `S274`, `S275`, `S279`

### AGENT-022 · Structured Output / Tool Arguments 如何做 Schema Validation、Repair 与 Hallucination Handling？

- **Topic**：Structured Output / Validation
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S012`, `S018`, `S057`, `S071`, `S081`, `S214`, `S248`, `S253`

### AGENT-023 · MCP 解决什么标准化问题？Client / Server、Tools / Resources / Prompts 与 stdio / SSE / Streamable HTTP 怎样理解？

- **Topic**：MCP Protocol
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**18**
- **Evidence Sources**：`S009`, `S015`, `S017`, `S019`, `S021`, `S022`, `S023`, `S028`, `S033`, `S034`, `S038`, `S041`, `S049`, `S057`, `S214`, `S231`, `S238`, `S259`

### AGENT-024 · Skill、Tool、Function Calling、MCP、Rule / Prompt / Workflow 的职责边界是什么？

- **Topic**：Capability Abstraction Boundary
- **Question Type**：Comparison
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**27**
- **Evidence Sources**：`S001`, `S009`, `S014`, `S018`, `S019`, `S020`, `S023`, `S028`, `S038`, `S039`, `S041`, `S049`, `S054`, `S055`, `S061`, `S081`, `S109`, `S214`, `S227`, `S228`, `S230`, `S231`, `S233`, `S238`, `S247`, `S252`, `S275`

### AGENT-025 · Skill 怎样做 Progressive Disclosure / Resource Loading？为什么成熟 Agent 不把所有 Instructions / Assets 一次性注入 Context？

- **Topic**：Skill Progressive Disclosure
- **Question Type**：Why / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S039`, `S081`, `S135`, `S214`, `S228`, `S231`, `S233`, `S252`, `S275`

### AGENT-026 · Agent 长耗时任务怎样 Timeout、Cancel、Interrupt、Resume？取消传播和资源清理怎样保证？

- **Topic**：Cancellation / Long-running Task
- **Question Type**：Failure Analysis / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S019`, `S034`, `S036`, `S047`, `S059`, `S081`, `S182`, `S214`, `S240`

### AGENT-027 · Checkpoint / Persistence / Resume 应保存哪些 Runtime State？Crash 后怎样恢复到可继续执行的状态？

- **Topic**：Checkpoint / Resume
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**12**
- **Evidence Sources**：`S034`, `S042`, `S059`, `S063`, `S081`, `S087`, `S105`, `S182`, `S209`, `S214`, `S241`, `S242`

### AGENT-028 · Permission、Approval、HITL、Sandbox 如何限制 Agent 的写操作、代码执行和高风险外部副作用？

- **Topic**：Permission / Approval / Sandbox
- **Question Type**：Security / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**15**
- **Evidence Sources**：`S015`, `S019`, `S025`, `S027`, `S030`, `S032`, `S037`, `S042`, `S059`, `S081`, `S214`, `S241`, `S245`, `S253`, `S275`

### AGENT-029 · Tool 已成功产生外部副作用，但 Checkpoint / DB 写失败或服务崩溃时，如何避免 Resume 后重复执行？

- **Topic**：Idempotency / External Side Effect
- **Question Type**：Failure Analysis / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S035`, `S042`, `S081`, `S182`, `S214`, `S242`

### AGENT-030 · 什么时候使用 Multi-Agent / Sub-agent？怎样分工、通信、共享或隔离 Context / State？

- **Topic**：Multi-Agent Architecture
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**21**
- **Evidence Sources**：`S001`, `S002`, `S017`, `S026`, `S027`, `S028`, `S031`, `S034`, `S037`, `S042`, `S044`, `S058`, `S060`, `S061`, `S063`, `S064`, `S081`, `S145`, `S214`, `S228`, `S253`

### AGENT-031 · 多 Agent 并行修改同一文件 / Workspace 或共享资源时，如何避免 Conflict、Race、Lost Update？

- **Topic**：Workspace / Shared-resource Concurrency
- **Question Type**：System Design / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S017`, `S027`, `S030`, `S032`, `S081`, `S214`

### AGENT-032 · 多模型 / Model Routing 怎样设计？不同 Provider 的请求、响应、错误码、Context 与 Tool Protocol 如何统一？

- **Topic**：Model Routing / Provider Abstraction
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S032`, `S043`, `S044`, `S060`, `S081`, `S214`, `S236`, `S240`, `S246`

### AGENT-033 · Agent Streaming 怎样实现？SSE、WebSocket、HTTP Streaming 的边界、断连、心跳、重连和续传如何处理？

- **Topic**：Streaming Transport
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S021`, `S033`, `S035`, `S047`, `S064`, `S066`, `S081`, `S214`, `S240`

### AGENT-034 · Agent / Harness 怎样做 Evaluation？如何把 Final Result、Process、Tool、Routing、Cost 与 Regression 分层验证？

- **Topic**：Agent Evaluation
- **Question Type**：Evaluation / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**19**
- **Evidence Sources**：`S003`, `S007`, `S031`, `S041`, `S043`, `S048`, `S057`, `S058`, `S061`, `S063`, `S081`, `S214`, `S225`, `S228`, `S235`, `S236`, `S242`, `S243`, `S279`

### AGENT-035 · Agent Benchmark / Eval Dataset / Ground Truth 怎样构建？怎样让 Offline Case 代表真实线上任务并用于 Regression？

- **Topic**：Benchmark Engineering
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S043`, `S057`, `S061`, `S081`, `S214`, `S225`, `S228`, `S236`, `S279`

### AGENT-036 · AI / Coding Agent 生成代码后，怎样用 Test、Diff、Regression、Review、Rollback 证明结果可交付？

- **Topic**：Code Verification
- **Question Type**：AI Coding / Verification
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**15**
- **Evidence Sources**：`S003`, `S007`, `S009`, `S030`, `S032`, `S043`, `S046`, `S048`, `S061`, `S214`, `S226`, `S236`, `S245`, `S259`, `S279`

### AGENT-037 · Coding Agent 怎样理解大型 Repository？Vector RAG、AST / LSP、ripgrep / Filesystem Search、Dependency Graph 各自适合什么？

- **Topic**：Repository Understanding
- **Question Type**：System Design / Comparison
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S008`, `S038`, `S059`, `S132`, `S145`, `S218`, `S231`, `S236`, `S248`

### AGENT-038 · Agent Runtime 的 Retry、Backoff、Circuit Breaker、Model / Tool Fallback 与 Degradation 怎样设计？哪些错误不该重试？

- **Topic**：Reliability / Retry / Fallback
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**12**
- **Evidence Sources**：`S003`, `S007`, `S019`, `S022`, `S045`, `S060`, `S073`, `S081`, `S214`, `S236`, `S240`, `S276`

### AGENT-039 · 高并发 / 多租户 Agent 如何做 Concurrency Limit、Queue / Backpressure、Fairness、Quota 与 Token Budget？

- **Topic**：Concurrency / Backpressure / Quota
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S004`, `S027`, `S035`, `S073`, `S081`, `S194`, `S209`, `S240`, `S276`

### AGENT-040 · Agent Service 从单机 Demo 扩到多实例 / 多机器时，State、Session、Routing、Storage、Failover 与 Deployment 怎样变化？

- **Topic**：Production Scale / Deployment
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S004`, `S019`, `S027`, `S030`, `S037`, `S048`, `S063`, `S081`, `S243`

### AGENT-041 · Agent Self-evolution / Data Flywheel 怎样闭环？Bad Case、数据采集、Metric、上线验证与 Rollback 如何设计？

- **Topic**：Self-evolution / Data Flywheel
- **Question Type**：System Design / Evaluation
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S243`, `S248`, `S265`

### AGENT-042 · Agent 正在执行时用户追加 / 修改需求，新指令怎样进入当前 State，并安全影响后续 Planning / Execution？

- **Topic**：Dynamic Instruction / Steering
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S242`

---

## 3. 真人面经中最稳定的 Agent Runtime 追问链

### 3.1 从“会调 Tool”追到 Runtime

```text
Agent 与 LLM 有什么区别
→ Agent Loop 怎么跑
→ Tool Schema 怎么给模型
→ Model 返回 Text 还是 Structured Call
→ 谁真正执行 Tool
→ Result 怎么回填
→ Invalid Call / Timeout 怎么办
→ Tool 太多怎么办
→ Tool Result 太大怎么办
```

### 3.2 从“有上下文”追到长期任务

```text
Context 包含什么
→ Window 满了怎么办
→ Compaction 怎么做
→ 压缩后怎么证明没丢任务
→ Memory 怎么分层
→ 旧 Memory / 错 Memory 怎么处理
→ Checkpoint 存什么
→ Crash / Resume
→ 外部副作用已经成功但 Checkpoint 失败怎么办
```

### 3.3 从 Demo Agent 追到 Production Control Plane

```text
Permission / Approval
→ Sandbox
→ Secret / Prompt Injection
→ Timeout / Cancellation
→ Retry / Idempotency
→ Multi-Agent Conflict
→ Streaming / Reconnect
→ Trace
→ Eval / Regression
→ Concurrency / Quota / Cost
→ Multi-instance Deployment
```

---

## 4. 面经对 Agent Harness 课程提出的最低要求

仅从真实面经看，最终课程已经不能写成“LangChain / LangGraph API 教程”。至少要系统覆盖：

1. Agent Loop、Message / Event、State；
2. Context Assembly、Compaction、Context Cache；
3. Memory Lifecycle 与错误 / 过期 Memory 治理；
4. Structured Tool Call、Tool Lifecycle、Discovery、Progressive Loading；
5. MCP 与 Skill / Tool / Rule / Workflow 的能力边界；
6. Permission / Approval / Sandbox / Security；
7. Checkpoint、Resume、Cancellation、External Side-effect Idempotency；
8. Multi-Agent、Sub-agent、Workspace Conflict；
9. Streaming、Retry、Fallback、Circuit Breaker、Backpressure / Quota；
10. Trace、Benchmark、Evaluation、Regression；
11. Coding Agent 的 Repo Understanding 与 Code Verification；
12. Model Routing、Cost / Latency、Production Deployment。

但这仍只是“真实市场已经问到的最低覆盖”。最终 Agent Harness 知识体系下一阶段必须进一步对照 Claude Code 与 Codex 源码，把成熟产品已经解决、但面经尚未高频显式问出的 Runtime 能力补齐。源码补全属于课程证据层，不能改写上述 HUMAN-A 频率。
