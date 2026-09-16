# Temporary source comparison (not a quality verdict)

Main: 0266cbfa131ff4157cad9f4c18b75fe153c0b846

## New chapter outline

### 01-AgentSystemAndTaskContract.md (120 lines)

# 01. Agent 系统与任务契约
## 1. 先定义系统要对什么结果负责
## 2. 一张固定的职责图
## 3. 四层之间分别交接什么
## 4. 层、模块、机制、对象、协议与资源不要混排
## 5. 从契约推导能力，而不是由组件反推需求
## 本章自测
## 回到主线

### 02-CapabilityAndAutonomy.md (82 lines)

# 02. 能力设计与自主权分配
## 1. 先选择控制方式，再选择框架
## 2. 为每项能力分配决策权、执行权与验收权
## 3. 自主权不是一个全局开关
## 4. 从最小方案演进，避免提前堆模块
## 本章自测
## 回到主线

### 03-ApplicationAndInteraction.md (191 lines)

# 03. L1 应用层：任务、流程与用户交互
## 1. 应用层先把输入组织成任务
## 2. 业务流程与运行循环分别编排什么
## 3. 入口路由：决定请求交给谁
### Intent Recognition 可以有多种实现
### Router 也需要 Evaluation
## 4. 交互是执行协议的一部分
## 5. 交付、权限与本层的完成标准
## 本章自测
## 回到主线

### 04-AgentLoopAndControl.md (570 lines)

# 04. L2 运行层：执行循环与控制
## 1. 先把执行对象说清楚
## 2. 循环推进：模型提出候选，运行时决定怎样兑现
## 3. 用计划管理进度，而不是把计划当成功证明
### 先讲人话：Planning 不是“先写一份超长计划”
### ReAct 解决什么问题
### Plan-Execute-Replan 什么时候更合适
### Goal Control：Agent 怎么知道自己还在做原任务
## 4. 停止、预算、重复与方向修正
### Stop Condition 不是只有 `max_steps`
### Budget 应该是多维的
### Dead Loop / Oscillation 怎么检测
### Dynamic Instruction / Steering 怎么进入当前 Run
### Planning Failure Timeline
### Framework 不应该决定你的 Planning 模型
## 5. 事件把循环变成可解释的执行
### Runtime 不是只有 Message，还需要 Event
### Event 为什么最好是结构化的
### Correlation ID 为什么关键
## 本章自测
## 回到主线

### 05-ContextEngineering.md (743 lines)

# 05. L2 运行层：上下文组装、预算与压缩
## 1. Context Manager 管的是当前模型可见信息
## 2. 从来源到可调用的上下文
### 一次 Agent Context 可能来自哪些 Source
### Context Assembly 应该是“Compiler”，不是字符串拼接
### Assembly Order 为什么重要
### Token Budget 要分区，而不是统一“还剩多少”
### Context Dedup 为什么重要
## 3. 先处理增长，再考虑压缩
### Large Tool Result 为什么不能直接塞回 Context
### Offloading 和 Truncation 有什么区别
### Prompt / Context Cache 应该缓存什么
## 4. Compaction 是上下文管理机制
### Compaction 为什么存在
### Compaction 与普通 Summary 的区别
### Compaction 什么时候触发
### 哪些信息必须保留
### 哪些内容适合压缩或外部化
### Replacement History 为什么重要
## 5. 验证继续执行是否仍然正确
### Compaction Correctness 怎样验证
### Compaction 失败怎么办
### Stale Context 是另一类问题
### Summary Error 会产生“压缩后的错误记忆”
### Compaction 和 Memory 的边界
### Context Assembly Failure Timeline
## 本章自测
## 回到主线

### 06-MemoryLifecycle.md (437 lines)

# 06. L2 运行层：记忆的选择、使用与维护
## 1. 记忆策略属于运行层，记忆数据库不属于运行层
### 先把 Context / Memory / State / History 分开
### Memory 为什么不能“什么都存”
### Memory 可以怎样分层
## 2. 选择、提取、写入与按需召回
### 什么时候应该写 Memory
### Extraction：从对话变成 Memory Record
### Retrieval-on-demand 为什么比“全量注入”更重要
### Memory Consolidation 是什么
## 3. 纠错、冲突与失效是核心机制
### Memory Correctness：错误事实比“没有记住”更危险
### Memory Conflict 怎么处理
### Memory Staleness / Expiration
### Memory Failure Timeline
## 4. 记忆的安全与验收
### Privacy / Tenant Boundary
### 高频易错点
## 本章自测
## 回到主线

### 07-StateAndRecovery.md (753 lines)

# 07. L2 运行层：执行状态、持久化与恢复
## 1. 哪些状态必须独立于上下文存在
### State 应该保存什么
### History 应该是事件流，而不是“一个超长字符串”
### Snapshot 与 Event Log 怎么配合
### Persistence 不等于把 Context 存下来
## 2. 状态所有权、并发和租户边界
### Tenant Isolation 为什么必须进入 State Schema
### Session Hijack / Cross-tenant Pollution
### Concurrency：同一个 Session 同时来两个请求怎么办
### State Version 为什么重要
## 3. 检查点与恢复边界
### Checkpoint 不是“把聊天记录存一下”
### Checkpoint 应该发生在哪里
### Checkpoint Schema 一个示例
### Cold Resume 与 Warm Resume
## 4. 先核对副作用，再继续推理
### Resume 的第一步不是“继续调用模型”
### 最危险的问题：Tool 成功，但 Checkpoint 失败
### Idempotency 是第一道防线
### Side-effect Ledger
### Compensation 什么时候需要
## 5. 暂停、取消、分叉、重放和接管
### Long-running Task 的状态机
### Pause / Resume 与 HITL
### Cancellation 与 Resume 的关系
### Resume 和 Fork 不一样
### Replay 是什么
### Worker Lease 与 Ownership
### Session Retention / Deletion
## 本章自测
## 回到主线

### 08-MultiAgentCoordination.md (488 lines)

# 08. L2 运行层：多 Agent 协作与调度
## 1. 多 Agent 是运行拓扑，不是新的架构层
### 什么时候真的值得 Multi-Agent
### Subagent as Tool
### Handoff 模式
### Manager / Worker 模式
### Task Ownership 必须显式
## 2. 隔离上下文并协调共享资源
### Context Isolation 为什么很重要
### Workspace Concurrency 是 Coding Agent 的高风险点
### 共享 Workspace 的几种策略
### Shared State 也会 Race
## 3. 调度、取消、预算与死锁
### Multi-Agent Failure
### Budget Explosion
### Recursive Delegation / Deadlock
### Result Aggregation 不是“把所有答案拼起来”
## 4. 跨系统协作与内部子 Agent 不同
### A2A 解决什么
### A2A 和内部 Subagent 有什么区别
## 本章自测
## 回到主线

### 09-ModelAccessAndRouting.md (332 lines)

# 09. L3 接入层：模型适配、路由与容错
## 1. 先区分选择策略和供应商适配
### Model Routing 的目标是什么
### Provider Adapter 的接入职责
### Provider Adapter 应统一什么，不统一什么
## 2. 按错误语义恢复，而不是统一重试
### Runtime Resilience 先做 Error Classification
### Retry Eligibility 为什么比 Retry Count 更重要
### Model Failover 会不会改变结果语义
### Circuit Breaker 在 Agent Runtime 中怎么用
### Fallback 不应该静默
### Routing Failure Timeline
## 3. 路由与模型变更也需要验收
## 本章自测
## 回到主线

### 10-ToolContractAndDiscovery.md (562 lines)

# 10. L3 接入层：工具契约、注册与发现
## 1. 工具是模型与执行系统之间的正式契约
### 先讲人话：为什么 Tool 不能只写成一个 Python 函数
### Tool Contract 的最小结构
### Schema 解决两个完全不同的问题
### 结构校验 vs 语义校验
### Tool Description 也是协议的一部分
### Structured Result 也应该有 Contract
### Tool Arguments 出错时怎么处理
### Repair 不能无限循环
### Side-effect Metadata 为什么应该靠 Runtime 保存
## 2. 注册目录与本轮可见集合
### Registry 解决什么
### Registry 与 Model-visible Tool Set 必须分开
### Router 做什么
### 为什么需要 Namespace
### Tool Exposure 不应该只有“注册 / 未注册”
## 3. 发现、加载与版本生命周期
### Progressive Discovery 的核心
### Tool Discovery 可以怎么做
### Discovery 的 Evaluation
### Tool Unavailable 怎么办
### Registry 更新与版本问题
### 版本升级怎么办
## 本章自测
## 回到主线

### 11-ToolExecutionAndEffects.md (647 lines)

# 11. L3 接入层：工具执行、副作用与取消
## 1. 从调用请求到可接受结果
### 一次完整 Tool Execution
### Executor 为什么不应该直接暴露原始函数
### Tool Result 不是一段字符串
### 为什么日志、模型输出、Host Metadata 应分层
### Result Validation
## 2. 错误分类与有限恢复
### Failure Classification
### Repair、Retry、Fallback、Fail 不是一回事
### Retry Eligibility 必须先判断幂等与副作用
### Timeout 也不是一种简单失败
### 错误反馈给模型应该“可行动”
### Pre / Post Tool Hook 为什么很有用
## 3. 并发必须围绕资源与副作用
### 为什么 Tool 不能默认并发
### Tool Side Effect 分类
### Concurrency Safety 应是 Tool Contract 的一部分
### Resource Key 比“Tool Name”更准确
## 4. 取消、进度和最终结果
### 用户取消为什么必须传播
### Cancellation 是协议，不是一个布尔值
### Parent / Child Cancellation
### Progress 为什么是 Runtime Primitive
### Streaming Result 与 Final Result 要分开
### Side Effect + Cancellation 的危险窗口
## 本章自测
## 回到主线

### 12-KnowledgeAndCapabilityAccess.md (467 lines)

# 12. L3 接入层：知识、记忆与扩展能力接入
## 1. 把信息需求连接到可信来源
## 2. 工具、协议、技能与钩子各负责什么
### 先给稳定边界
### MCP 解决什么标准化问题
### Tool / Resource / Prompt 为什么要分开
### Transport 不是 MCP 的核心价值
### Skill 与 Tool 的区别
### Skill Progressive Disclosure
### Hook 是什么
## 3. 能力扩展的失败、版本和安全
### Extension Failure 怎么处理
### Capability Versioning
### Security Boundary
## 4. 用代码资源检索检查接口是否足够表达需求
### Repository Understanding 不等于 Vector RAG
### Repo Understanding 的搜索漏斗
## 本章自测
## 回到主线

### 13-ResourcesAndEnvironments.md (343 lines)

# 13. L4 资源层：模型、数据与执行环境
## 1. 资源层保存事实并提供真实能力
## 2. 存储选择服从状态语义
### Session Store 选什么
## 3. 执行环境与隔离
### Sandbox 解决的是另一层问题
### Filesystem Sandbox
### Network Sandbox
### Sandbox 不是“绝对安全”
### Execution Sandbox Pool
## 4. 环境生命周期、工作区与产物
### Workspace State 必须可控
### Patch Application 要有前置版本
### Command Execution 的风险
### Rollback / Delivery
## 本章自测
## 回到主线

### 14-IdentityPermissionsAndSafety.md (673 lines)

# 14. 横切治理：身份、权限、审批与安全
## 1. 安全是每层的责任，不是最后插入的过滤器
### 三种安全责任：Policy、Approval 与 Sandbox
### 为什么“全部弹确认框”不是好安全设计
### Risk Classification 可以看什么
### Permission Context 应该结构化
### Approval 为什么必须和 RunState 结合
### Approval Record 应保存什么
## 2. 先明确威胁与信任边界
### Threat Model：先问“攻击者想让 Agent 做什么”
### Instruction 与 Data 必须在 Runtime 概念上分层
### Guardrail 应该分生命周期，而不是一个总开关
### Prompt Injection 为什么不能靠“检测一句恶意文本”解决
## 3. 约束秘密、能力与外传路径
### Secret 不应该直接进入模型 Context
### Tool Capability 要最小化
### Containment：重点不是“永不犯错”
### Untrusted Tool Result 也可能继续攻击下一轮
### RAG / MCP 的 Injection Surface
### Memory Poisoning
### Output Leakage
## 4. 用失败链检验安全设计
### Permission 与 Prompt Injection 的关系
### Permission Failure Timeline
### Security Incident Timeline
## 本章自测
## 回到主线

### 15-ObservabilityAndEvaluation.md (810 lines)

# 15. 横切治理：观测、评测与持续改进
## 1. 观测回答发生了什么，评测回答做得怎样
### Log、Metric、Trace 各解决什么
### Trace Identity
### 一个 Agent Span 应该记录什么
### 为什么要记录“模型看到什么”
### Trace 与 Privacy 冲突
## 2. 可解释地回放、诊断与定位
### Replay 有三种不同含义
### Trace 如何定位“Agent 卡住”
### Token / Cost 异常怎么定位
### Context Management 自己也需要 Observability
### Agent Trace Schema 示例
### Observability 不应该和 Evaluation 混为一谈
## 3. 从任务契约推导验证对象
### 先分清 Agent Harness 和 Eval Harness
### 最终结果比“模型说完成了”更重要
### 评测的四个验证视角（不是架构层）
### Eval Dataset 从哪里来
### Dataset 要分层采样
### Ground Truth 不一定是一个字符串
### LLM Judge 什么时候适合
### Process Metric 为什么也重要
### Tool / Routing Eval
## 4. 评测推动修改，而不是只生成分数
### Agent Eval 与 Trace 的关系
### Regression 为什么必须自动化
### SWE-bench 为什么是重要参考
### Benchmark Contamination / Overfitting
### Data Flywheel
### Online Validation
### Evaluation Failure Timeline
## 本章自测
## 回到主线

### 16-ProductionArchitectureAndEvolution.md (1076 lines)

# 16. 系统收口：部署、成本、选型与演进
## 1. 把逻辑职责落成部署与故障边界
### 先看一个单机 Demo
### 一个通用 Production Agent Runtime
### Brain / Hands / Durable Session 分离
### Harness Worker 应尽量可替换
### Scheduler / Queue 为什么重要
## 2. 规模、成本、可靠性与升级
### 多租户隔离
### Long-running Agent 如何跨 Worker
### Streaming 和 Durable State 不要混
### Deployment / Scaling 的核心指标
### Cost Governance
### Failure Domain
### 一个 Production Failure Timeline
### Observability / Eval Plane
### Brain / Hands 分离不是唯一正确架构
## 3. 框架选型是职责匹配，不是架构起点
### 先写自己的 Requirement Matrix
### Framework 提供的价值通常是什么
### OpenAI Agents SDK 怎样映射
### LangGraph 适合解决什么类型问题
### LangChain 适合什么
### 什么时候自研 Runtime
### Build-vs-Buy Matrix
### Framework Selection 的错误方法
### Framework Evaluation 应该用真实 Workload
### Escape Hatch 很重要
### Framework Upgrade 风险
### 自研最小 Runtime 到底需要什么
### Framework 不会替你解决业务正确性
### Framework Migration
## 4. 以 Codex 类工作过程检验交付闭环
### Coding Agent 最大的问题不是生成，而是理解和验证
### Patch 应尽量小
### Test 是 Outcome Verification，不是装饰
### Test Failure 怎么处理
### Diff Review 是另一道防线
### Acceptance Criteria 必须独立于 Agent 自评
### Verification Pyramid
### AI-assisted Development 中人的责任
### Coding Agent Failure Timeline
## 5. 最终设计与讲解顺序
## 本章自测
## 回到主线

## Main mechanism retention candidates

### agent-harness/docs/01-AgentHarness在AI应用中的职责.md

# 01. Agent Harness 在 AI 应用中的职责 | exact normalized paragraphs 0/3

# 1. 先讲人话：Model 很聪明，但它不会替你经营一次“执行” | exact normalized paragraphs 0/4

# 2. 一个实用定义 | exact normalized paragraphs 0/3

# 3. 为什么“Model + API”还不够 | exact normalized paragraphs 0/1

## 3.1 下一步由谁驱动？ | exact normalized paragraphs 0/2

## 3.2 Context 越来越长怎么办？ | exact normalized paragraphs 0/3

## 3.3 Tool 有副作用怎么办？ | exact normalized paragraphs 0/2

## 3.4 中途崩了怎么办？ | exact normalized paragraphs 0/2

## 3.5 Agent 说“完成了”，真的完成了吗？ | exact normalized paragraphs 0/2

# 4. Harness 的八个工程平面 | exact normalized paragraphs 0/4

# 5. 一个最小 Runtime 长什么样 | exact normalized paragraphs 0/11

# 6. Model 和 Harness 到底各负责什么 | exact normalized paragraphs 0/3

# 7. 成熟产品源码告诉我们的什么 | exact normalized paragraphs 0/2

## 7.1 Claude Code：QueryEngine 明确拥有 Conversation Runtime | exact normalized paragraphs 0/4

## 7.2 Claude Code：Tool 不是普通函数 | exact normalized paragraphs 0/2

## 7.3 Codex：Context / Session / Tool / Sandbox 都是独立 Runtime 对象 | exact normalized paragraphs 0/3

# 8. 官方资料为什么也强调 Harness，而不是只强调模型 | exact normalized paragraphs 0/5

# 9. 一个 AI 应用场景：企业知识库 Agent | exact normalized paragraphs 0/3

# 10. Harness、Backend、Framework 不要混在一起 | exact normalized paragraphs 0/0

## Harness vs 普通 Backend | exact normalized paragraphs 0/3

## Harness vs Agent Framework | exact normalized paragraphs 0/4

# 11. 高频易错点 | exact normalized paragraphs 0/6

# 12. 面试怎么回答 | exact normalized paragraphs 0/0

## Level 1｜30 秒 | exact normalized paragraphs 0/1

## Level 2｜2–3 分钟 | exact normalized paragraphs 0/2

## Level 3｜继续深挖 | exact normalized paragraphs 0/1

# 13. 本章证据边界 | exact normalized paragraphs 0/0

## HUMAN-A | exact normalized paragraphs 0/1

## Claude Code 源码 | exact normalized paragraphs 0/2

## OpenAI Codex 源码 | exact normalized paragraphs 0/2

## 外部权威资料 | exact normalized paragraphs 0/1

# 14. 自测 | exact normalized paragraphs 0/4

### agent-harness/docs/02-AgentWorkflowHarnessBoundary.md

# 02｜Agent vs Workflow，以及 Harness / Runtime / Orchestrator 的边界 | exact normalized paragraphs 0/1

## 1. 先讲人话：Agent 化的本质是什么 | exact normalized paragraphs 0/5

## 2. 为什么“更 Agent”不等于“更高级” | exact normalized paragraphs 0/3

## 3. 什么任务更值得 Agent 化 | exact normalized paragraphs 0/3

## 4. Production 往往是 Hybrid | exact normalized paragraphs 0/2

## 5. 为什么 Model + API 还不够 | exact normalized paragraphs 0/2

## 6. Harness / Runtime 到底是什么 | exact normalized paragraphs 0/3

## 7. Harness、Runtime、Orchestrator、Workflow Engine 怎么区分 | exact normalized paragraphs 0/1

### Harness / Runtime | exact normalized paragraphs 0/1

### Orchestrator | exact normalized paragraphs 0/2

### Workflow Engine | exact normalized paragraphs 0/3

## 8. 三个经常混淆的边界 | exact normalized paragraphs 0/0

### Prompt Engineering | exact normalized paragraphs 0/1

### Context Engineering | exact normalized paragraphs 0/1

### Harness Engineering | exact normalized paragraphs 0/2

## 9. 源码证据：为什么成熟产品一定有 Runtime Layer | exact normalized paragraphs 0/4

## 10. Agent 化之后立刻新增哪些工程问题 | exact normalized paragraphs 0/2

## 11. HUMAN-A 为什么高频追这个边界 | exact normalized paragraphs 0/3

## 12. 🎯 30 秒回答 | exact normalized paragraphs 0/1

## 13. 🎯 2–3 分钟回答框架 | exact normalized paragraphs 0/2

## 14. ⚠️ 易错点 | exact normalized paragraphs 0/1

## 15. 🔍 面试官继续追问 | exact normalized paragraphs 0/4

### agent-harness/docs/03-AgentLoopRuntimeState.md

# 03｜Agent Loop、Run / Turn / Step 与 Runtime Event Model | exact normalized paragraphs 0/1

## 1. 先讲人话：Agent 的核心不是“会调用 Tool”，而是会循环推进任务 | exact normalized paragraphs 0/3

## 2. 一个最小可运行的 Agent Loop | exact normalized paragraphs 0/7

## 3. 为什么要分 Run / Turn / Step | exact normalized paragraphs 0/2

### Session / Thread | exact normalized paragraphs 0/0

### Run | exact normalized paragraphs 0/1

### Turn | exact normalized paragraphs 0/0

### Step | exact normalized paragraphs 0/1

## 4. 为什么这个分层对 Failure 很重要 | exact normalized paragraphs 0/2

## 5. Runtime 不是只有 Message，还需要 Event | exact normalized paragraphs 3/3

## 6. Event 为什么最好是结构化的 | exact normalized paragraphs 2/2

## 7. Correlation ID 为什么关键 | exact normalized paragraphs 3/3

## 8. State Machine：Loop 不只是 while True | exact normalized paragraphs 0/3

## 9. Runtime State 应该有什么 | exact normalized paragraphs 0/3

## 10. 新用户指令怎样进入正在运行的 Agent | exact normalized paragraphs 0/4

## 11. 源码证据：Claude Code | exact normalized paragraphs 0/2

## 12. 源码证据：Codex | exact normalized paragraphs 0/4

## 13. Loop 什么时候继续，什么时候停止 | exact normalized paragraphs 0/5

## 14. HUMAN-A 对应 | exact normalized paragraphs 0/2

## 15. 🎯 30 秒回答 | exact normalized paragraphs 0/1

## 16. ⚠️ 易错点 | exact normalized paragraphs 0/1

## 17. 🔍 继续追问 | exact normalized paragraphs 0/4

### agent-harness/docs/04-ToolContractSchemaValidation.md

# 04｜Tool Contract、Schema 与 Validation | exact normalized paragraphs 0/1

## 1. 先讲人话：为什么 Tool 不能只写成一个 Python 函数 | exact normalized paragraphs 3/3

## 2. Tool Contract 的最小结构 | exact normalized paragraphs 3/3

## 3. Schema 解决两个完全不同的问题 | exact normalized paragraphs 0/0

### Model-facing Schema | exact normalized paragraphs 1/1

### Runtime Validation | exact normalized paragraphs 1/1

## 4. 结构校验 vs 语义校验 | exact normalized paragraphs 3/3

## 5. Tool Description 也是协议的一部分 | exact normalized paragraphs 3/3

## 6. Structured Result 也应该有 Contract | exact normalized paragraphs 2/2

## 7. Tool Arguments 出错时怎么处理 | exact normalized paragraphs 4/4

## 8. Repair 不能无限循环 | exact normalized paragraphs 2/2

## 9. Side-effect Metadata 为什么应该靠 Runtime 保存 | exact normalized paragraphs 3/3

## 10. 源码证据：Claude Code | exact normalized paragraphs 0/3

## 11. 源码证据：Codex | exact normalized paragraphs 0/4

## 12. 版本升级怎么办 | exact normalized paragraphs 2/2

## 13. HUMAN-A 对应 | exact normalized paragraphs 0/2

## 14. 🎯 30 秒回答 | exact normalized paragraphs 0/1

## 15. ⚠️ 易错点 | exact normalized paragraphs 0/1

## 16. 🔍 继续追问 | exact normalized paragraphs 0/3

### agent-harness/docs/05-ToolRegistryRouterDiscovery.md

# 05｜Tool Registry、Router 与 Progressive Discovery | exact normalized paragraphs 0/1

## 1. Registry 解决什么 | exact normalized paragraphs 3/3

## 2. Registry 与 Model-visible Tool Set 必须分开 | exact normalized paragraphs 3/3

## 3. Router 做什么 | exact normalized paragraphs 3/3

## 4. 为什么需要 Namespace | exact normalized paragraphs 2/2

## 5. Tool Exposure 不应该只有“注册 / 未注册” | exact normalized paragraphs 2/2

## 6. Progressive Discovery 的核心 | exact normalized paragraphs 1/1

## 7. Tool Discovery 可以怎么做 | exact normalized paragraphs 0/0

### Rule / Intent Filter | exact normalized paragraphs 1/1

### Embedding / Semantic Search | exact normalized paragraphs 1/1

### LLM Router | exact normalized paragraphs 1/1

### Hybrid | exact normalized paragraphs 1/1

## 8. Discovery 的 Evaluation | exact normalized paragraphs 2/2

## 9. Tool Unavailable 怎么办 | exact normalized paragraphs 3/3

## 10. 源码证据：Codex | exact normalized paragraphs 0/2

## 11. 源码证据：Claude Code | exact normalized paragraphs 0/2

## 12. Registry 更新与版本问题 | exact normalized paragraphs 3/3

## 13. HUMAN-A 对应 | exact normalized paragraphs 0/3

## 14. 🎯 30 秒回答 | exact normalized paragraphs 0/1

## 15. ⚠️ 易错点 | exact normalized paragraphs 0/2

### agent-harness/docs/06-ToolExecutionFailure.md

# 06｜Tool Execution、Result 与 Failure Semantics | exact normalized paragraphs 0/1

## 1. 一次完整 Tool Execution | exact normalized paragraphs 1/1

## 2. Executor 为什么不应该直接暴露原始函数 | exact normalized paragraphs 4/4

## 3. Tool Result 不是一段字符串 | exact normalized paragraphs 2/2

## 4. 为什么日志、模型输出、Host Metadata 应分层 | exact normalized paragraphs 4/4

## 5. Failure Classification | exact normalized paragraphs 1/1

## 6. Repair、Retry、Fallback、Fail 不是一回事 | exact normalized paragraphs 0/0

### Repair | exact normalized paragraphs 1/1

### Retry | exact normalized paragraphs 1/1

### Fallback | exact normalized paragraphs 1/1

### Fail | exact normalized paragraphs 1/1

## 7. Retry Eligibility 必须先判断幂等与副作用 | exact normalized paragraphs 3/3

## 8. Timeout 也不是一种简单失败 | exact normalized paragraphs 3/3

## 9. 错误反馈给模型应该“可行动” | exact normalized paragraphs 2/2

## 10. Result Validation | exact normalized paragraphs 2/2

## 11. Pre / Post Tool Hook 为什么很有用 | exact normalized paragraphs 4/4

## 12. 源码证据：Codex | exact normalized paragraphs 0/2

## 13. HUMAN-A 对应 | exact normalized paragraphs 0/3

## 14. 🎯 30 秒回答 | exact normalized paragraphs 0/1

## 15. ⚠️ 易错点 | exact normalized paragraphs 0/1

## 16. 🔍 继续追问 | exact normalized paragraphs 0/3

### agent-harness/docs/07-ToolSideEffectCancellation.md

# 07｜Tool Side Effect、Concurrency、Cancellation 与 Progress | exact normalized paragraphs 0/1

## 1. 为什么 Tool 不能默认并发 | exact normalized paragraphs 3/3

## 2. Tool Side Effect 分类 | exact normalized paragraphs 0/0

### Pure / Read-only | exact normalized paragraphs 1/1

### Local Mutable | exact normalized paragraphs 1/1

### External Reversible | exact normalized paragraphs 1/1

### External Irreversible / High Risk | exact normalized paragraphs 2/2

## 3. Concurrency Safety 应是 Tool Contract 的一部分 | exact normalized paragraphs 4/4

## 4. Resource Key 比“Tool Name”更准确 | exact normalized paragraphs 2/2

## 5. 用户取消为什么必须传播 | exact normalized paragraphs 2/2

## 6. Cancellation 是协议，不是一个布尔值 | exact normalized paragraphs 3/3

## 7. Parent / Child Cancellation | exact normalized paragraphs 3/3

## 8. Progress 为什么是 Runtime Primitive | exact normalized paragraphs 4/4

## 9. Streaming Result 与 Final Result 要分开 | exact normalized paragraphs 4/4

## 10. 源码证据：Claude Code | exact normalized paragraphs 0/3

## 11. 源码证据：Codex | exact normalized paragraphs 0/2

## 12. Side Effect + Cancellation 的危险窗口 | exact normalized paragraphs 3/3

## 13. HUMAN-A 对应 | exact normalized paragraphs 0/3

## 14. 🎯 30 秒回答 | exact normalized paragraphs 0/1

## 15. ⚠️ 易错点 | exact normalized paragraphs 0/2

### agent-harness/docs/08-PlanningGoalStopBudget.md

# 08. Planning / ReAct、Goal Control、Stop Condition 与 Budget | exact normalized paragraphs 0/4

## 1. 先讲人话：Planning 不是“先写一份超长计划” | exact normalized paragraphs 4/4

# 2. ReAct 解决什么问题 | exact normalized paragraphs 5/5

# 3. Plan-Execute-Replan 什么时候更合适 | exact normalized paragraphs 3/3

# 4. Goal Control：Agent 怎么知道自己还在做原任务 | exact normalized paragraphs 6/6

# 5. Stop Condition 不是只有 `max_steps` | exact normalized paragraphs 0/0

## 5.1 成功停止 | exact normalized paragraphs 1/1

## 5.2 无法继续 | exact normalized paragraphs 1/1

## 5.3 强制停止 | exact normalized paragraphs 3/3

# 6. Budget 应该是多维的 | exact normalized paragraphs 3/3

# 7. Dead Loop / Oscillation 怎么检测 | exact normalized paragraphs 6/6

# 8. Dynamic Instruction / Steering 怎么进入当前 Run | exact normalized paragraphs 5/5

# 9. Planning Failure Timeline | exact normalized paragraphs 3/3

# 10. Framework 不应该决定你的 Planning 模型 | exact normalized paragraphs 3/3

# 11. 证据分层 | exact normalized paragraphs 0/0

### HUMAN-A | exact normalized paragraphs 0/1

### Claude Code 固定源码快照 | exact normalized paragraphs 0/2

### Tier C | exact normalized paragraphs 0/2

# 12. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent 怎样避免无限循环？ | exact normalized paragraphs 0/1

## Q：ReAct 和 Plan-Execute-Replan 怎么选？ | exact normalized paragraphs 0/1

# 13. 高频易错点 | exact normalized paragraphs 0/4

# 14. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/09-ContextAssemblyBudget.md

# 09. Context Assembly、Budget、Cache 与 Tool Result Offloading | exact normalized paragraphs 0/5

## 1. Context、Memory、State、History 先分清 | exact normalized paragraphs 0/5

# 2. 一次 Agent Context 可能来自哪些 Source | exact normalized paragraphs 2/2

# 3. Context Assembly 应该是“Compiler”，不是字符串拼接 | exact normalized paragraphs 3/3

# 4. Assembly Order 为什么重要 | exact normalized paragraphs 4/4

# 5. Token Budget 要分区，而不是统一“还剩多少” | exact normalized paragraphs 3/3

# 6. Claude Code 源码提供了什么实现证据 | exact normalized paragraphs 0/6

# 7. Large Tool Result 为什么不能直接塞回 Context | exact normalized paragraphs 6/6

# 8. Offloading 和 Truncation 有什么区别 | exact normalized paragraphs 3/3

# 9. Prompt / Context Cache 应该缓存什么 | exact normalized paragraphs 4/4

# 10. Context Pollution / Stale Context | exact normalized paragraphs 0/4

# 11. Context Dedup 为什么重要 | exact normalized paragraphs 4/4

# 12. Context Assembly Failure Timeline | exact normalized paragraphs 2/2

# 13. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 14. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Context 应该怎么组装？ | exact normalized paragraphs 0/1

## Q：Tool Result 太大怎么办？ | exact normalized paragraphs 0/1

# 15. 高频易错点 | exact normalized paragraphs 0/4

# 16. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/10-ContextCompactionCorrectness.md

# 10. Context Compaction、Correctness 与 Stale Context | exact normalized paragraphs 0/3

## 1. Compaction 为什么存在 | exact normalized paragraphs 3/3

# 2. Compaction 与普通 Summary 的区别 | exact normalized paragraphs 2/2

# 3. Codex `compact.rs` 给出的实现证据 | exact normalized paragraphs 0/6

# 4. Claude Code 侧提供了什么证据 | exact normalized paragraphs 0/4

# 5. Compaction 什么时候触发 | exact normalized paragraphs 0/0

## 5.1 Token Threshold | exact normalized paragraphs 2/2

## 5.2 Phase Boundary | exact normalized paragraphs 0/0

## 5.3 Tool Result Pressure | exact normalized paragraphs 1/1

# 6. 哪些信息必须保留 | exact normalized paragraphs 1/1

### Goal / Acceptance | exact normalized paragraphs 1/1

### Runtime Progress | exact normalized paragraphs 1/1

### Side-effect Ledger | exact normalized paragraphs 1/1

### Artifact References | exact normalized paragraphs 1/1

### Unresolved Evidence | exact normalized paragraphs 1/1

# 7. 哪些内容适合压缩或外部化 | exact normalized paragraphs 2/2

# 8. Replacement History 为什么重要 | exact normalized paragraphs 5/5

# 9. Compaction Correctness 怎样验证 | exact normalized paragraphs 0/0

## 9.1 Structural Invariant | exact normalized paragraphs 1/1

## 9.2 Semantic Invariant | exact normalized paragraphs 1/1

## 9.3 Continuation Test | exact normalized paragraphs 2/2

## 9.4 Regression Eval | exact normalized paragraphs 2/2

# 10. Compaction 失败怎么办 | exact normalized paragraphs 4/4

# 11. Stale Context 是另一类问题 | exact normalized paragraphs 5/5

# 12. Summary Error 会产生“压缩后的错误记忆” | exact normalized paragraphs 0/0

# 13. Compaction 和 Memory 的边界 | exact normalized paragraphs 3/3

# 14. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 15. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Context 快满了怎么办？ | exact normalized paragraphs 0/1

## Q：怎样验证 Compaction 没丢信息？ | exact normalized paragraphs 0/1

# 16. 高频易错点 | exact normalized paragraphs 0/4

# 17. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/11-MemoryArchitectureLifecycle.md

# 11. Memory Architecture、Lifecycle 与 Correctness | exact normalized paragraphs 0/4

## 1. 先把 Context / Memory / State / History 分开 | exact normalized paragraphs 5/5

# 2. Memory 为什么不能“什么都存” | exact normalized paragraphs 2/2

# 3. Memory 可以怎样分层 | exact normalized paragraphs 0/0

## 3.1 Working Memory | exact normalized paragraphs 2/2

## 3.2 Episodic Memory | exact normalized paragraphs 1/1

## 3.3 Semantic Memory | exact normalized paragraphs 0/0

## 3.4 Procedural Memory | exact normalized paragraphs 2/2

# 4. 什么时候应该写 Memory | exact normalized paragraphs 3/3

# 5. Extraction：从对话变成 Memory Record | exact normalized paragraphs 2/2

# 6. Retrieval-on-demand 为什么比“全量注入”更重要 | exact normalized paragraphs 2/2

# 7. Memory Consolidation 是什么 | exact normalized paragraphs 5/5

# 8. Memory Correctness：错误事实比“没有记住”更危险 | exact normalized paragraphs 4/4

# 9. Memory Conflict 怎么处理 | exact normalized paragraphs 2/2

# 10. Memory Staleness / Expiration | exact normalized paragraphs 3/3

# 11. Privacy / Tenant Boundary | exact normalized paragraphs 3/3

# 12. Claude Code 固定源码侧的证据 | exact normalized paragraphs 0/4

# 13. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 14. Memory Failure Timeline | exact normalized paragraphs 2/2

# 15. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Memory 怎么设计？ | exact normalized paragraphs 0/1

## Q：Memory 错了怎么办？ | exact normalized paragraphs 0/1

# 16. 高频易错点 | exact normalized paragraphs 4/4

# 17. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/12-SessionStatePersistence.md

# 12. Session、State、History、Persistence 与 Tenant Isolation | exact normalized paragraphs 0/4

## 1. Session 是什么 | exact normalized paragraphs 0/2

# 2. Run / Turn / Step 再复习 | exact normalized paragraphs 0/6

# 3. State 应该保存什么 | exact normalized paragraphs 1/1

## 3.1 Identity State | exact normalized paragraphs 1/1

## 3.2 Control State | exact normalized paragraphs 1/1

## 3.3 Environment State Reference | exact normalized paragraphs 1/1

## 3.4 Safety State | exact normalized paragraphs 1/1

## 3.5 Progress State | exact normalized paragraphs 1/1

# 4. History 应该是事件流，而不是“一个超长字符串” | exact normalized paragraphs 3/3

# 5. Snapshot 与 Event Log 怎么配合 | exact normalized paragraphs 3/3

# 6. Persistence 不等于把 Context 存下来 | exact normalized paragraphs 3/3

# 7. Session Store 选什么 | exact normalized paragraphs 0/0

### Redis 适合 | exact normalized paragraphs 1/1

### MySQL / Durable DB 适合 | exact normalized paragraphs 1/1

### Object / Artifact Store | exact normalized paragraphs 1/1

# 8. Tenant Isolation 为什么必须进入 State Schema | exact normalized paragraphs 3/3

# 9. Session Hijack / Cross-tenant Pollution | exact normalized paragraphs 4/4

# 10. Concurrency：同一个 Session 同时来两个请求怎么办 | exact normalized paragraphs 4/4

# 11. State Version 为什么重要 | exact normalized paragraphs 2/2

# 12. Cold Resume 与 Warm Resume | exact normalized paragraphs 0/0

## Warm Resume | exact normalized paragraphs 1/1

## Cold Resume | exact normalized paragraphs 1/1

# 13. Session Retention / Deletion | exact normalized paragraphs 2/2

# 14. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 15. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Session / State 怎么设计？ | exact normalized paragraphs 0/1

# 16. 高频易错点 | exact normalized paragraphs 0/4

# 17. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/13-CheckpointResumeReliability.md

# 13. Checkpoint / Resume / Fork / Replay 与 Long-running Reliability | exact normalized paragraphs 0/3

## 1. Checkpoint 不是“把聊天记录存一下” | exact normalized paragraphs 1/1

# 2. Checkpoint 应该发生在哪里 | exact normalized paragraphs 3/3

# 3. Long-running Task 的状态机 | exact normalized paragraphs 4/4

# 4. Resume 的第一步不是“继续调用模型” | exact normalized paragraphs 2/2

# 5. 最危险的问题：Tool 成功，但 Checkpoint 失败 | exact normalized paragraphs 2/2

# 6. Idempotency 是第一道防线 | exact normalized paragraphs 4/4

# 7. Side-effect Ledger | exact normalized paragraphs 2/2

# 8. Compensation 什么时候需要 | exact normalized paragraphs 4/4

# 9. Pause / Resume 与 HITL | exact normalized paragraphs 4/4

# 10. Cancellation 与 Resume 的关系 | exact normalized paragraphs 3/3

# 11. Resume 和 Fork 不一样 | exact normalized paragraphs 0/0

## Resume | exact normalized paragraphs 0/0

## Fork | exact normalized paragraphs 4/4

# 12. Replay 是什么 | exact normalized paragraphs 0/0

## 12.1 State Replay | exact normalized paragraphs 1/1

## 12.2 Execution Replay | exact normalized paragraphs 3/3

# 13. Worker Lease 与 Ownership | exact normalized paragraphs 3/3

# 14. Checkpoint Schema 一个示例 | exact normalized paragraphs 2/2

# 15. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 16. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Checkpoint 应该保存什么？ | exact normalized paragraphs 0/1

## Q：Tool 成功但服务崩了，怎么避免重试两次？ | exact normalized paragraphs 0/1

# 17. 高频易错点 | exact normalized paragraphs 0/4

# 18. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/14-PermissionApprovalSandbox.md

# 14. Permission、Approval、HITL 与 Sandbox | exact normalized paragraphs 0/3

## 1. 三层边界 | exact normalized paragraphs 0/0

### Policy | exact normalized paragraphs 1/1

### Approval / HITL | exact normalized paragraphs 0/0

### Sandbox | exact normalized paragraphs 2/2

# 2. 为什么“全部弹确认框”不是好安全设计 | exact normalized paragraphs 5/5

# 3. Risk Classification 可以看什么 | exact normalized paragraphs 5/5

# 4. Permission Context 应该结构化 | exact normalized paragraphs 2/2

# 5. Approval 为什么必须和 RunState 结合 | exact normalized paragraphs 4/4

# 6. Approval Record 应保存什么 | exact normalized paragraphs 1/1

# 7. Sandbox 解决的是另一层问题 | exact normalized paragraphs 6/6

# 8. Filesystem Sandbox | exact normalized paragraphs 2/2

# 9. Network Sandbox | exact normalized paragraphs 3/3

# 10. Sandbox 不是“绝对安全” | exact normalized paragraphs 2/2

# 11. Permission 与 Prompt Injection 的关系 | exact normalized paragraphs 3/3

# 12. Permission Failure Timeline | exact normalized paragraphs 2/2

# 13. HUMAN-A 信号 | exact normalized paragraphs 0/4

# 14. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Permission、Approval、Sandbox 有什么区别？ | exact normalized paragraphs 0/1

## Q：审批为什么要持久化？ | exact normalized paragraphs 0/1

# 15. 高频易错点 | exact normalized paragraphs 0/4

# 16. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/15-GuardrailsInjectionContainment.md

# 15. Guardrails、Prompt Injection、Secrets 与 Containment | exact normalized paragraphs 0/5

## 1. Threat Model：先问“攻击者想让 Agent 做什么” | exact normalized paragraphs 3/3

# 2. Instruction 与 Data 必须在 Runtime 概念上分层 | exact normalized paragraphs 4/4

# 3. Guardrail 应该分生命周期，而不是一个总开关 | exact normalized paragraphs 1/1

## 3.1 Ingress Guardrail | exact normalized paragraphs 1/1

## 3.2 Context Guardrail | exact normalized paragraphs 2/2

## 3.3 Tool Guardrail | exact normalized paragraphs 1/1

## 3.4 Output / Egress Guardrail | exact normalized paragraphs 1/1

# 4. Prompt Injection 为什么不能靠“检测一句恶意文本”解决 | exact normalized paragraphs 3/3

# 5. Secret 不应该直接进入模型 Context | exact normalized paragraphs 3/3

# 6. Tool Capability 要最小化 | exact normalized paragraphs 3/3

# 7. Containment：重点不是“永不犯错” | exact normalized paragraphs 3/3

# 8. Untrusted Tool Result 也可能继续攻击下一轮 | exact normalized paragraphs 4/4

# 9. RAG / MCP 的 Injection Surface | exact normalized paragraphs 4/4

# 10. Memory Poisoning | exact normalized paragraphs 4/4

# 11. Output Leakage | exact normalized paragraphs 3/3

# 12. Security Incident Timeline | exact normalized paragraphs 4/4

# 13. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 14. Tier C 官方证据 | exact normalized paragraphs 0/0

### Anthropic — Beyond permission prompts | exact normalized paragraphs 0/2

### Anthropic — How we contain Claude across products | exact normalized paragraphs 0/0

### OpenAI Agents SDK — Guardrails | exact normalized paragraphs 0/1

# 15. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent 如何防 Prompt Injection？ | exact normalized paragraphs 0/1

# 16. 高频易错点 | exact normalized paragraphs 0/4

# 17. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/16-MCPSkillsHooks.md

# 16. MCP、Skills、Hooks 与 Capability Extension | exact normalized paragraphs 0/4

## 1. 先给稳定边界 | exact normalized paragraphs 0/0

### Tool | exact normalized paragraphs 1/1

### MCP | exact normalized paragraphs 2/2

### Skill | exact normalized paragraphs 2/2

### Hook | exact normalized paragraphs 1/1

# 2. 为什么 Tool 太多会出问题 | exact normalized paragraphs 0/4

# 3. Capability Catalog | exact normalized paragraphs 0/3

# 4. Claude Code 源码侧的 Progressive Loading 证据 | exact normalized paragraphs 0/4

# 5. MCP 解决什么标准化问题 | exact normalized paragraphs 6/6

# 6. Tool / Resource / Prompt 为什么要分开 | exact normalized paragraphs 0/0

### Tool | exact normalized paragraphs 0/0

### Resource | exact normalized paragraphs 0/0

### Prompt | exact normalized paragraphs 1/1

# 7. Transport 不是 MCP 的核心价值 | exact normalized paragraphs 2/2

# 8. Skill 与 Tool 的区别 | exact normalized paragraphs 4/4

# 9. Skill Progressive Disclosure | exact normalized paragraphs 4/4

# 10. Hook 是什么 | exact normalized paragraphs 3/3

# 11. Codex Hooks 的实现证据 | exact normalized paragraphs 0/3

# 12. Extension Failure 怎么处理 | exact normalized paragraphs 4/4

# 13. Capability Versioning | exact normalized paragraphs 3/3

# 14. Security Boundary | exact normalized paragraphs 4/4

# 15. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 16. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Tool、MCP、Skill、Hook 有什么区别？ | exact normalized paragraphs 0/1

## Q：Tool 太多怎么处理？ | exact normalized paragraphs 0/1

# 17. 高频易错点 | exact normalized paragraphs 0/4

# 18. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/17-RoutingProviderResilience.md

# 17. Intent / Model Routing、Provider Adapter 与 Runtime Resilience | exact normalized paragraphs 0/4

## 1. Routing 至少有三层 | exact normalized paragraphs 0/0

### Intent Routing | exact normalized paragraphs 0/1

### Capability Routing | exact normalized paragraphs 0/1

### Model / Provider Routing | exact normalized paragraphs 0/1

# 2. Intent Recognition 可以有多种实现 | exact normalized paragraphs 1/1

## Rule | exact normalized paragraphs 1/1

## Small Classifier | exact normalized paragraphs 0/0

## LLM Router | exact normalized paragraphs 0/0

## Agent 自主 Tool Selection | exact normalized paragraphs 1/1

# 3. Router 也需要 Evaluation | exact normalized paragraphs 4/4

# 4. Model Routing 的目标是什么 | exact normalized paragraphs 4/4

# 5. Provider Adapter 为什么是 Runtime 能力 | exact normalized paragraphs 3/3

# 6. Provider Adapter 应统一什么，不统一什么 | exact normalized paragraphs 3/3

# 7. Claude Code 的实现信号 | exact normalized paragraphs 0/3

# 8. Runtime Resilience 先做 Error Classification | exact normalized paragraphs 3/3

# 9. Retry Eligibility 为什么比 Retry Count 更重要 | exact normalized paragraphs 3/3

# 10. Model Failover 会不会改变结果语义 | exact normalized paragraphs 3/3

# 11. Circuit Breaker 在 Agent Runtime 中怎么用 | exact normalized paragraphs 2/2

# 12. Fallback 不应该静默 | exact normalized paragraphs 2/2

# 13. Routing Failure Timeline | exact normalized paragraphs 2/2

# 14. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 15. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Router 怎么设计？ | exact normalized paragraphs 0/1

## Q：Provider 失败怎么 Fallback？ | exact normalized paragraphs 0/1

# 16. 高频易错点 | exact normalized paragraphs 0/4

# 17. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/18-MultiAgentA2AWorkspace.md

# 18. Multi-Agent、Subagent、Handoff、A2A 与 Workspace Concurrency | exact normalized paragraphs 0/4

## 1. 什么时候真的值得 Multi-Agent | exact normalized paragraphs 4/4

# 2. Subagent as Tool | exact normalized paragraphs 4/4

# 3. Handoff 模式 | exact normalized paragraphs 2/2

# 4. Manager / Worker 模式 | exact normalized paragraphs 2/2

# 5. Task Ownership 必须显式 | exact normalized paragraphs 3/3

# 6. Context Isolation 为什么很重要 | exact normalized paragraphs 3/3

# 7. Claude Code `Task.ts` 提供的实现信号 | exact normalized paragraphs 1/3

# 8. Workspace Concurrency 是 Coding Agent 的高风险点 | exact normalized paragraphs 3/3

# 9. 共享 Workspace 的几种策略 | exact normalized paragraphs 0/0

## 9.1 单 Writer | exact normalized paragraphs 1/1

## 9.2 Isolated Branch / Worktree | exact normalized paragraphs 1/1

## 9.3 Fine-grained Ownership | exact normalized paragraphs 1/1

## 9.4 Optimistic Merge | exact normalized paragraphs 0/0

# 10. Shared State 也会 Race | exact normalized paragraphs 2/2

# 11. Multi-Agent Failure | exact normalized paragraphs 3/3

# 12. Budget Explosion | exact normalized paragraphs 2/2

# 13. Recursive Delegation / Deadlock | exact normalized paragraphs 2/2

# 14. A2A 解决什么 | exact normalized paragraphs 4/4

# 15. A2A 和内部 Subagent 有什么区别 | exact normalized paragraphs 2/2

# 16. Result Aggregation 不是“把所有答案拼起来” | exact normalized paragraphs 3/3

# 17. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 18. 面试怎么答 | exact normalized paragraphs 0/0

## Q：什么时候用 Multi-Agent？ | exact normalized paragraphs 0/1

## Q：MCP 和 A2A 区别？ | exact normalized paragraphs 0/1

# 19. 高频易错点 | exact normalized paragraphs 0/4

# 20. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/19-TraceReplayObservability.md

# 19. Trace、Replay 与 Observability | exact normalized paragraphs 0/3

## 1. Log、Metric、Trace 各解决什么 | exact normalized paragraphs 0/0

### Log | exact normalized paragraphs 1/1

### Metric | exact normalized paragraphs 1/1

### Trace | exact normalized paragraphs 1/1

# 2. Trace Identity | exact normalized paragraphs 2/2

# 3. 一个 Agent Span 应该记录什么 | exact normalized paragraphs 0/0

## Model Span | exact normalized paragraphs 1/1

## Tool Span | exact normalized paragraphs 1/1

## Context Span | exact normalized paragraphs 1/1

## State Span | exact normalized paragraphs 1/1

# 4. Codex Rollout Trace 的源码证据 | exact normalized paragraphs 0/4

# 5. OpenAI Agents SDK Tracing 给出的证据 | exact normalized paragraphs 0/2

# 6. 为什么要记录“模型看到什么” | exact normalized paragraphs 4/4

# 7. Trace 与 Privacy 冲突 | exact normalized paragraphs 3/3

# 8. Replay 有三种不同含义 | exact normalized paragraphs 0/0

### Evidence Replay | exact normalized paragraphs 1/1

### Model Replay | exact normalized paragraphs 1/1

### Side-effect Replay | exact normalized paragraphs 1/1

# 9. Trace 如何定位“Agent 卡住” | exact normalized paragraphs 1/1

# 10. Token / Cost 异常怎么定位 | exact normalized paragraphs 1/1

# 11. Context Management 自己也需要 Observability | exact normalized paragraphs 4/4

# 12. Agent Trace Schema 示例 | exact normalized paragraphs 1/1

# 13. Observability 不应该和 Evaluation 混为一谈 | exact normalized paragraphs 1/1

# 14. HUMAN-A 信号 | exact normalized paragraphs 0/3

# 15. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent Trace 应该记录什么？ | exact normalized paragraphs 0/1

# 16. 高频易错点 | exact normalized paragraphs 0/4

# 17. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/20-AgentEvaluationBenchmark.md

# 20. Agent Evaluation、Benchmark 与 Data Flywheel | exact normalized paragraphs 0/2

## 1. 先分清 Agent Harness 和 Eval Harness | exact normalized paragraphs 3/3

# 2. 最终结果比“模型说完成了”更重要 | exact normalized paragraphs 3/3

# 3. Eval 分四层 | exact normalized paragraphs 0/0

## 3.1 Final Outcome | exact normalized paragraphs 1/1

## 3.2 Process / Runtime | exact normalized paragraphs 1/1

## 3.3 Component | exact normalized paragraphs 1/1

## 3.4 Resource / Safety | exact normalized paragraphs 1/1

# 4. Eval Dataset 从哪里来 | exact normalized paragraphs 3/3

# 5. Dataset 要分层采样 | exact normalized paragraphs 2/2

# 6. Ground Truth 不一定是一个字符串 | exact normalized paragraphs 2/2

# 7. LLM Judge 什么时候适合 | exact normalized paragraphs 3/3

# 8. Process Metric 为什么也重要 | exact normalized paragraphs 3/3

# 9. Tool / Routing Eval | exact normalized paragraphs 2/2

# 10. Agent Eval 与 Trace 的关系 | exact normalized paragraphs 3/3

# 11. Regression 为什么必须自动化 | exact normalized paragraphs 2/2

# 12. SWE-bench 为什么是重要参考 | exact normalized paragraphs 2/2

# 13. Benchmark Contamination / Overfitting | exact normalized paragraphs 2/2

# 14. Data Flywheel | exact normalized paragraphs 2/2

# 15. Online Validation | exact normalized paragraphs 2/2

# 16. Evaluation Failure Timeline | exact normalized paragraphs 2/2

# 17. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 18. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Agent 应该怎么评估？ | exact normalized paragraphs 0/1

## Q：Data Flywheel 怎么做？ | exact normalized paragraphs 0/1

# 19. 高频易错点 | exact normalized paragraphs 0/4

# 20. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/21-CodingAgentWorkflow.md

# 21. Coding Agent：Repo Understanding → Patch → Test → Verify | exact normalized paragraphs 0/2

## 1. Coding Agent 最大的问题不是生成，而是理解和验证 | exact normalized paragraphs 3/3

# 2. Repository Understanding 不等于 Vector RAG | exact normalized paragraphs 1/1

## ripgrep / Text Search | exact normalized paragraphs 0/0

## Filesystem Navigation | exact normalized paragraphs 0/0

## AST / LSP | exact normalized paragraphs 1/1

## Vector / Semantic Search | exact normalized paragraphs 0/0

## Dependency Graph | exact normalized paragraphs 1/1

# 3. Repo Understanding 的搜索漏斗 | exact normalized paragraphs 2/2

# 4. Patch 应尽量小 | exact normalized paragraphs 2/2

# 5. Workspace State 必须可控 | exact normalized paragraphs 3/3

# 6. Patch Application 要有前置版本 | exact normalized paragraphs 1/1

# 7. Test 是 Outcome Verification，不是装饰 | exact normalized paragraphs 2/2

# 8. Test Failure 怎么处理 | exact normalized paragraphs 2/2

# 9. Diff Review 是另一道防线 | exact normalized paragraphs 3/3

# 10. Acceptance Criteria 必须独立于 Agent 自评 | exact normalized paragraphs 2/2

# 11. Verification Pyramid | exact normalized paragraphs 2/2

# 12. Command Execution 的风险 | exact normalized paragraphs 1/1

# 13. AI-assisted Development 中人的责任 | exact normalized paragraphs 2/2

# 14. Rollback / Delivery | exact normalized paragraphs 3/3

# 15. Claude Code / Codex 为什么是重要实现参考 | exact normalized paragraphs 0/3

# 16. Coding Agent Failure Timeline | exact normalized paragraphs 2/2

# 17. HUMAN-A 信号 | exact normalized paragraphs 0/2

# 18. 面试怎么答 | exact normalized paragraphs 0/0

## Q：AI Coding 怎么保证质量？ | exact normalized paragraphs 0/1

# 19. 高频易错点 | exact normalized paragraphs 0/4

# 20. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/22-ProductionAgentRuntime.md

# 22. Production Agent Runtime Architecture | exact normalized paragraphs 0/2

## 1. 先看一个单机 Demo | exact normalized paragraphs 2/2

# 2. 一个通用 Production Agent Runtime | exact normalized paragraphs 2/2

# 3. Brain / Hands / Durable Session 分离 | exact normalized paragraphs 6/6

# 4. API / Streaming Gateway | exact normalized paragraphs 0/3

# 5. Harness Worker 应尽量可替换 | exact normalized paragraphs 3/3

# 6. Scheduler / Queue 为什么重要 | exact normalized paragraphs 4/4

# 7. Execution Sandbox Pool | exact normalized paragraphs 4/4

# 8. Tool Gateway | exact normalized paragraphs 0/1

# 9. Model Provider Gateway | exact normalized paragraphs 0/2

# 10. Durable Event / State Store | exact normalized paragraphs 0/3

# 11. 多租户隔离 | exact normalized paragraphs 2/2

# 12. Long-running Agent 如何跨 Worker | exact normalized paragraphs 2/3

# 13. Streaming 和 Durable State 不要混 | exact normalized paragraphs 1/1

# 14. Deployment / Scaling 的核心指标 | exact normalized paragraphs 1/1

# 15. Cost Governance | exact normalized paragraphs 3/3

# 16. Failure Domain | exact normalized paragraphs 6/6

# 17. 一个 Production Failure Timeline | exact normalized paragraphs 3/3

# 18. Observability / Eval Plane | exact normalized paragraphs 3/3

# 19. Brain / Hands 分离不是唯一正确架构 | exact normalized paragraphs 2/2

# 20. HUMAN-A 与 Tier C | exact normalized paragraphs 0/4

# 21. 面试怎么答 | exact normalized paragraphs 0/0

## Q：Production Agent Backend 怎么设计？ | exact normalized paragraphs 0/1

# 22. 高频易错点 | exact normalized paragraphs 0/4

# 23. 本章自测 | exact normalized paragraphs 0/3

### agent-harness/docs/23-FrameworkMappingBuildVsBuy.md

# 23. Framework Mapping 与 Build-vs-Buy | exact normalized paragraphs 0/3

## 1. 先写自己的 Requirement Matrix | exact normalized paragraphs 2/2

# 2. Framework 提供的价值通常是什么 | exact normalized paragraphs 2/2

# 3. OpenAI Agents SDK 怎样映射 | exact normalized paragraphs 4/4

# 4. LangGraph 适合解决什么类型问题 | exact normalized paragraphs 2/2

# 5. LangChain 适合什么 | exact normalized paragraphs 3/3

# 6. 什么时候自研 Runtime | exact normalized paragraphs 2/2

# 7. Build-vs-Buy Matrix | exact normalized paragraphs 1/1

# 8. Framework Selection 的错误方法 | exact normalized paragraphs 0/0

## 8.1 只看 Star | exact normalized paragraphs 0/0

## 8.2 只看 Demo | exact normalized paragraphs 1/1

## 8.3 只看 Feature Checklist | exact normalized paragraphs 1/1

# 9. Framework Evaluation 应该用真实 Workload | exact normalized paragraphs 2/2

# 10. Escape Hatch 很重要 | exact normalized paragraphs 2/2

# 11. Framework Upgrade 风险 | exact normalized paragraphs 2/2

# 12. 自研最小 Runtime 到底需要什么 | exact normalized paragraphs 3/3

# 13. Anthropic `Building effective agents` 的重要启发 | exact normalized paragraphs 0/2

# 14. Framework 不会替你解决业务正确性 | exact normalized paragraphs 3/3

# 15. HUMAN-A 信号 | exact normalized paragraphs 0/3

# 16. 一个选型回答模板 | exact normalized paragraphs 0/2

# 17. Framework Migration | exact normalized paragraphs 2/2

# 18. 面试怎么答 | exact normalized paragraphs 0/0

## Q：LangChain / LangGraph / 自研怎么选？ | exact normalized paragraphs 0/1

# 19. 高频易错点 | exact normalized paragraphs 0/4

# 20. 本章自测 | exact normalized paragraphs 0/3