# Batch 05 — 规范化问题增量

只记录 Batch 05 相比前四批 **新出现，或已经细化到值得单独成为 canonical question** 的问题。

> 特别说明：本批首次大量引入抖音 / B 站 / 小红书线索。若来源类型是 `面试题信号/二次创作`，该题可以作为课程边界和系统设计训练题，但 **不计入真实面经频率**；只有 `原始/第一人称` 或可核实真实面试来源才进入频率统计。

## Agent Harness / Runtime

### A071 Context Compaction 应如何设计触发水位、异步准备、增量摘要和原始历史持久化？
- 来源：S048
- 标签：Agent Harness / Context / Compaction / Lifecycle
- 核心拆解：Soft Watermark、Hard Watermark、Token Growth、异步 Summary、增量合并、原始历史归档、Atomic Swap。
- 与 A017/A018 区别：A017 关注“窗口满了怎么压缩”，A018 关注“压缩过度如何发现和恢复”；本题进一步要求完整的 **Compaction Runtime Lifecycle**。

### A072 Long-term Memory 应该在什么时机检索和注入，而不是每一轮都塞进 Context？
- 来源：S048
- 标签：Agent Harness / Memory / Retrieval Gating / Context Budget
- 核心拆解：用户意图、Task 依赖、相关性阈值、时间衰减、重复抑制、Token 成本、错误记忆放大风险。

### A073 Agent 的 Human-in-the-loop / Approval 如何按风险分级，而不是“所有 Tool 都确认”或“全部自动执行”？
- 来源：S052（面试题信号/二次创作）
- 标签：Agent Harness / HITL / Approval / Risk / Safety
- 核心拆解：动作影响范围、可逆性、权限 Scope、意图明确度、金额/资源阈值、用户确认、审计。
- 频率规则：本题作为课程与系统设计信号，不增加真实公司面经命中次数。

### A074 用户在 Agent 执行中途改变目标时，如何进行 Goal Versioning、Plan Invalidation 与 Replanning？
- 来源：S053（面试题信号/二次创作）
- 标签：Agent Runtime / Goal / Planning / Versioning / Invalidation
- 核心拆解：Goal Version、Subtask Dependency、待执行步骤失效、已产生副作用、Context 中旧目标降权、再次确认。
- 频率规则：课程信号，不计真实面经频率。

### A075 Tool 权限为什么不能交给 LLM 自己判断？Agent Runtime 应如何实现 Authentication / Authorization / Scope / Revocation？
- 来源：S054（面试题信号/二次创作）, S062
- 标签：Agent Security / Authorization / Capability / Least Privilege
- 核心拆解：身份认证、RBAC/ABAC/Capability、Read/Write/Execute Scope、委托、动态授权、撤销、审批、审计。
- 与 A046/A054 区别：A046 是 Context 信任层级，A054 是 Tool Governance；本题专门讲 **执行权限的强制 Enforcement Point**。

### A076 Agent Workflow 中部分 Tool 已成功、部分失败时，如何选择 Retry、Rollback、Compensation 或继续降级？
- 来源：S057（面试题信号/二次创作）
- 标签：Agent Runtime / Tool / Retry / Compensation / Saga / Side Effect
- 核心拆解：错误分类、幂等性、外部副作用、可逆性、补偿动作、部分成功状态、最终一致性。
- 与 B006 区别：B006 关注超时/脏数据/重复执行三类失败；本题聚焦 **跨 Tool Workflow 的部分成功语义**。

### A077 Agent 跨会话 Resume 前，为什么必须与外部系统重新对账，而不能直接相信旧 Checkpoint？
- 来源：S056（面试题信号/二次创作）
- 标签：Agent Runtime / Resume / External State / Reconciliation / Versioning
- 核心拆解：订单、权限、库存、文件等外部状态漂移；Checkpoint Version；Revalidation；Stale State；人工确认。
- 与 A037/A038 区别：A037/A038 解决 Checkpoint/Resume 与内部一致性，本题专门补充 **外部世界已经变化** 的恢复问题。

### A078 MCP Client 如何统一适配 stdio、HTTP、SSE、Streamable HTTP，并处理协议版本兼容？
- 来源：S061
- 标签：MCP / Transport / Adapter / Version Compatibility / Streaming
- 核心拆解：Transport Adapter、连接生命周期、双向/单向流、断线、取消、版本协商、能力兼容与降级。
- 与 A047/A048 区别：A047 是 Host/Client/Server 与能力协商，A048 是动态 Tool 刷新；本题深入 **Transport 与 Protocol Version**。

### A079 面向 ChatGPT / Agent 的 Session、Message、Tool Call、Tool Result、State、Checkpoint 应如何持久化建模？
- 来源：S061
- 标签：Agent Runtime / Persistence / Session / Message Model / Database Design
- 核心拆解：session_id、message_id、role/event_type、sequence、tool_call_id、parent/causality、tenant、run_id、checkpoint、idempotency、索引。
- 与 A063 区别：A063 定义运行时消息语义；本题把这些语义进一步落到 **持久化 Schema 与查询模型**。

### A080 本地 Agent / 设备端 Agent 与云端 Agent 大规模协作时，控制面、执行面、权限、状态和升级如何设计？
- 来源：S062
- 标签：Agent Harness / Edge Agent / Cloud Agent / Fleet / Distributed System
- 核心拆解：Local Capability、Cloud Orchestration、Identity、Device Registration、Offline、State Sync、Policy、Version/Upgrade、Telemetry。

## RAG / Retrieval

### R032 如何记录从 Query → Recall → Rerank → Final Context → Answer 的检索审计链路，区分召回、排序和生成问题？
- 来源：S048
- 标签：RAG / Observability / Retrieval Audit / Attribution
- 核心拆解：Query Version、Retriever、Doc/Chunk ID、Score、Rerank Score、Filter、Context Selection、Citation、Generation Trace。
- 与 A034 区别：A034 是 Agent 全链路 Trace；本题专门解决 RAG 检索质量的 **阶段归因**。

### R033 企业 RAG 同时召回多版本、互相冲突的知识时，如何做 Authority / Validity / Conflict Resolution 与可追溯回答？
- 来源：S055（面试题信号/二次创作）
- 标签：RAG / Knowledge Governance / Version / Conflict / Grounding
- 核心拆解：文档权威级别、有效期、版本、来源、冲突检测、拒答/澄清、引用、Bad Case 监控。
- 与 R018/R020/R021 区别：R018 是查询快照一致性，R020 是历史版本检索，R021 是引用漂移；本题关注 **多个同时有效或互相矛盾证据的裁决**。
- 频率规则：作为课程边界信号，不增加真实公司面经命中次数。

## 已有 canonical questions 得到显著强化

- `A003` ReAct vs Plan-and-Execute：S048
- `A006/A009` Tool Schema、参数验证和 Tool Error：S048, S062
- `A014/A015` Context、短期/长期 Memory：S048, S062, S063
- `A017/A018` Context Compaction 与信息保真：S048
- `A020/A021` 单/多 Agent、子图、状态传递：S062, S063
- `A030/A046` Prompt Injection 与不可信 Context：S062
- `A033/A054` Tool 安全边界与 Governance：S062
- `A057` AI 生成代码验证：S050, S063
- `A065` 自研 Runtime / Harness vs LangGraph：S062, S063
- `A067` Skill 生命周期：S063
- `R001` RAG 完整链路：S048
- `R004/R008` 召回问题与 Rerank：S048
- `M001/M007` B+Tree、行锁、乐观/悲观锁：S063

## Batch 05 对课程设计的新约束

1. **Context Compaction 必须从算法升级为 Runtime 生命周期**：Token 水位、后台 Summary、增量更新、历史归档、替换原子性和恢复都要讲。
2. **Memory 必须有 Retrieval Gating**：长期记忆不是“全部写进向量库、每轮全量检索”。
3. **MCP 必须进入 Transport / Version 层**：stdio、HTTP、SSE、Streamable HTTP、协议兼容、动态能力是工程必修，而不是附录。
4. **Agent Security 必须有强制权限层**：LLM 不能成为最终授权决策点；要讲 Identity、Scope、Capability、Approval、Sandbox、Audit、Revocation。
5. **Plan / Goal 要有版本与失效语义**：用户改目标、旧计划、已执行副作用、Context 中旧约束如何处理，是长程 Agent 的核心 Runtime 问题。
6. **Checkpoint 不等于恢复事实**：Resume 之前需要与外部世界 Reconcile。
7. **Tool Workflow 需要补偿语义**：现实 Agent 很难靠“失败就全局回滚”，必须学习 Idempotency、Compensation、Saga-like Workflow。
8. **RAG Observability 必须单独成章或子章**：没有逐阶段 Trace，就无法回答“召回不准到底是哪一层错”。
