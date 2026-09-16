# Agent 概念归位表｜层、模块、机制、对象与协议

[架构总纲](README.md) · [执行与状态](lifecycle-and-state.md) · [设计与自测](design-and-review.md) · [资料依据](sources.md)

> 使用方式：遇到概念，按“是什么类型 → 主要责任在哪 → 为什么需要 → 不负责什么 → 去哪里深入”的顺序定位。
>
> L1 应用层；L2 运行层；L3 接入层；L4 资源层。跨层项按责任拆开，而不是硬塞进一个框。下面是教材综合归位，不是任何厂商的官方分类。

## 1. 总体对象与控制模式

| 概念 | 类型与主要位置 | 解决的问题与边界 |
|---|---|---|
| Agent Application / Product | 系统，覆盖四层 | 承接任务、组织交互和执行、交付结果；不能只用模型配置代表整个产品 |
| Agent | 执行角色，主要由 L2 驱动 | 在目标与权限内动态选择下一步；不要求一个角色对应一个进程 |
| Model / LLM | 能力来源，L4，经 L3 调用 | 理解、生成、推理、提出动作；不直接承担持久化、授权和可靠执行 |
| Harness / Runtime | 执行系统，以 L2 为核心 | 组织循环、上下文、状态与工具；实现可以包含 L3 适配代码，术语边界因产品而异 |
| Agent Framework / SDK | 实现工具，可覆盖多层 | 提供可复用抽象；选了框架不等于完成了任务、安全和数据设计 |
| Orchestrator | 协调模块，L1 或 L2 | 业务阶段编排属于 L1；Agent、工具和子任务执行编排属于 L2；必须说清协调的对象 |
| Workflow | 控制模式，L1 / L2 | 用预定代码或图组织流程；其中可以包含模型节点和 Agent 子流程 |
| Agent Loop | 执行机制，L2 | 观察、决定、受控执行、接收反馈和继续；不等于整个生产系统 |
| ReAct | 行动与反馈交替的模式，L2 | 利用新观察调整动作；不应把“必须展示完整思维链”当成实现条件 |
| Planning / Decomposition | 能力与策略，L2 | 分解目标、维护依赖和中间验收；可以隐式实现，也可以维护显式计划 |
| Plan-and-execute / Replanning | 控制策略，L2 | 先形成计划再执行，并在证据变化后修改；计划是可修订假设，不是执行成功证明 |
| Reflection / Critic | 可选检查策略，L2 | 检查候选结果并改进；同一模型自评不自动构成独立验证 |
| Goal / Stop / Budget Control | 控制责任，L2 | 防止无限循环、目标漂移和资源失控；停止不一定意味着成功 |
| Intent Routing | 任务路由，L1 / L2 | 将输入送到正确流程或执行角色；不是模型供应商适配 |
| Model Routing | 选择策略，L2 或平台策略 | 按能力、延迟、成本和约束选择模型；L3 Adapter 负责实际接入 |

Workflow 与动态 Agent 的区分参考 [S08](sources.md#s08)。以上具体归位是教材工作约定。

深入：[职责](../docs/01-AgentHarness在AI应用中的职责.md)、[边界](../docs/02-AgentWorkflowHarnessBoundary.md)、[Loop](../docs/03-AgentLoopRuntimeState.md)、[Planning](../docs/08-PlanningGoalStopBudget.md)、[框架选择](../docs/23-FrameworkMappingBuildVsBuy.md)。

## 2. 上下文、检索与记忆

这三类问题的主线是：**去哪里找信息 → 当前该给模型看什么 → 哪些信息值得以后复用。** 它们不是三个同义词。

| 概念 | 类型与主要位置 | 解决的问题与边界 |
|---|---|---|
| Prompt / Instructions | 输入与配置，L1 定义、L2 组织 | 表达目标、行为要求、格式和工具用法；提示文本不是底层权限控制 |
| Context Engineering | 持续信息组织责任，L2 | 在每一步选择足够、相关、可信且有预算的信息；不只是首次拼接 Prompt |
| Context Manager / Assembly | 模块，L2 | 组合指令、近期历史、任务进展、证据、工具定义与可用记忆 |
| Context Window / Token Budget | 模型约束与运行预算，L4 / L2 | 限定本次推理可处理的信息；不等于系统能保存的所有数据 |
| Truncation / Pruning | 信息裁剪机制，L2 | 删除不再需要的内容；需要保护关键约束与调用结果关联 |
| Compaction | 上下文压缩机制，L2 | 用更紧凑表示继续推理；可能丢失细节，不能替代执行状态或业务回执 |
| Tool Result Offloading | 信息外置机制，L2 + L3 / L4 | 大结果保存到文件或对象存储，上下文保留摘要和可再读取引用；必须管理权限和保留期 |
| Progressive Disclosure | 按需加载策略，L2 / L3 | 先提供目录或描述，相关时再加载工具、技能和资料；不能让关键能力永远不可发现 |
| Prompt Caching | 调用优化机制，L2 / L3 / 模型服务 | 尽量复用适合缓存的输入前缀；不等于任务记忆或推理正确性保障 |
| Retrieval | 信息获取能力，L3 调用 L4 | 找到候选证据；候选相关不等于事实正确或授权可见 |
| RAG | 跨层信息使用方案 | 数据准备与索引在离线路径，检索由 L3 暴露，L2 把证据提供给模型；不是固定的第五层 |
| Ingestion / Parsing / Chunking | 数据准备机制，L3 管道 + L4 | 把来源变成可检索内容，并保留来源、版本与访问范围；不是每次 Loop 都重新执行 |
| Embedding / Indexing | 表示与索引机制，L4，按接口接入 | 支持相似度查找；并不自动解决权限、时效或语义正确性 |
| Keyword / Dense / Hybrid Search | 检索策略，L3 / L4 | 用不同信号获得候选；根据任务和评测选择，而非固定要求全部使用 |
| Query Rewrite / Rerank | 检索辅助机制，L2 / L3 | 改善查询和候选排序；需要防止改变原问题或额外成本超过收益 |
| Agentic RAG | 控制与检索组合，L2 + L3 | Agent 动态决定何时检索、如何追问和继续；不是另一套完整系统分层 |
| Graph-based Retrieval | 信息组织和检索变体，L3 / L4 | 利用实体与关系处理相应问题；不意味着所有知识库都应改用图 |
| Memory | 信息保留与复用机制，跨 L2–L4 | L2 决定何时读写、L3 提供接口、L4 保存；不是所有状态的总称 |
| Working / Short-term Memory | 用法依框架而异 | 可能指近期上下文或线程状态；讨论前必须明确，不能直接等同于长期存储 |
| Semantic / Episodic / Procedural Memory | 内容组织方式 | 分别偏事实、经历、做法；这些是记忆内容类别，不是三种必选数据库 |
| Memory Write Pipeline | 生命周期机制，L2 + L3 | 候选提取、来源与授权检查、去重、冲突处理、写入、过期与删除 |
| Memory Retrieval | 选择机制，L2 + L3 | 按当前任务、身份、时效与来源取回信息；记忆不能自动覆盖新的权威事实 |
| Learning / Optimization | 改进闭环，质量面及相关实现层 | 经验可以推动 Prompt、工具、检索或训练更新；“保存了一段记忆”不等于模型权重已经学习 |

上下文的动态管理参考 [S05](sources.md#s05)。线程状态与跨线程存储的框架实例参考 [S09](sources.md#s09)。RAG 完整机制仍由 [RAG 模块](../../rag/README.md)维护。

深入：[Context Assembly](../docs/09-ContextAssemblyBudget.md)、[Compaction](../docs/10-ContextCompactionCorrectness.md)、[Memory Lifecycle](../docs/11-MemoryArchitectureLifecycle.md)、[Session / State](../docs/12-SessionStatePersistence.md)。

## 3. 工具、能力扩展与协议

| 概念 | 类型与主要位置 | 解决的问题与边界 |
|---|---|---|
| Tool / Function Calling | 模型与运行时的动作交互 | 模型提出调用；L2 负责控制；L3 映射接口；L4 真实执行；模型输出的 JSON 不是执行事实 |
| Tool Contract / Schema | 接口契约，L3 | 描述用途、参数、输出、限制和错误；Schema 合法不等于动作被授权 |
| Structured Output | 输出约束机制，L2 / L3 | 使下游能够解析约定结构；结构正确不保证事实正确 |
| Tool Registry | 能力目录模块，L3，供 L2 使用 | 维护可发现的工具及版本；“存在于目录”不代表当前 Run 有权调用 |
| Tool Router / Dispatcher | 分发模块，L2 / L3 | 将请求送到正确 Handler，并关联调用和结果；不能以字符串模糊匹配代替严格契约 |
| Tool Result / Error Contract | 执行结果契约，L3 | 区分成功、失败、待完成和结果未知；帮助 Runtime 决定是否重试、等待或改路 |
| Tool Gateway / Credential Broker | 接入与安全模块，L3 | 统一访问范围、凭证代理、速率和审计；不应把原始 Secret 放进模型上下文 |
| MCP | 接入协议，主要 L3 | 交换工具、资源、提示等能力信息；不规定宿主怎样规划和管理上下文 |
| Skills | 可加载能力包，L2 加载、L3 / L4 提供资源 | 提供任务做法、参考资料和可选脚本；不是模型权重，也不自动获得执行权限 |
| Hooks / Middleware | 生命周期扩展机制，L2 / L3 | 在约定事件前后执行校验、记录或转换；不要把固定 Hook 等同于自主 Agent |
| Plugin / Connector | 扩展封装，通常跨 L2–L4 | 把协议、工具、配置或技能打包；“装了插件”不等于完成安全和版本治理 |
| A2A | Agent 间协作协议，接入边界 | 交换 Agent 能力、消息、任务状态与产物；不是替系统决定最优分工的调度器 |
| Agent–Client Event Protocol | 应用与运行时接口，L1 / L2 边界 | 表达进度、输入请求、结果与生命周期；Codex App Server 是具体实例，不等于 MCP |

MCP、Skills 和 A2A 的原始定义分别见 [S10](sources.md#s10)、[S11](sources.md#s11)、[S12](sources.md#s12)。协议会演进：总纲维护职责边界，具体字段与兼容性必须回到版本化规范。

深入：[Schema](../docs/04-ToolContractSchemaValidation.md)、[Registry / Discovery](../docs/05-ToolRegistryRouterDiscovery.md)、[Failure](../docs/06-ToolExecutionFailure.md)、[MCP / Skills / Hooks](../docs/16-MCPSkillsHooks.md)。

## 4. 执行对象、持久化与可靠性

| 概念 | 类型与主要位置 | 解决的问题与边界 |
|---|---|---|
| Task | 业务工作对象，L1 | 表达要交付的结果和验收条件；不必等于一次聊天 |
| Run / Attempt | 执行对象，L2 | 表达一次受管理执行及其尝试；具体定义必须由系统约定 |
| Thread / Session | 会话对象，L1 / L2 | 组织持续交互和相关记录；不要与业务任务强行绑定为一一对应 |
| Turn | 工作轮次对象，L2 | 在 Codex 中对应一次用户输入触发的工作；不是一次模型调用 |
| Step | 运行步骤，L2 | 可以是图节点、模型轮次或其他调度单位，取决于框架 |
| Item | 类型化输入输出对象，L2 / L1 | Codex 用它表达消息、工具等工作单元；不等于单个 Token 或单条 Event |
| Event | 发生过的状态变化，L2 | 描述开始、进展、完成等；流式通知与持久事实需要明确不同保证 |
| Artifact | 可交付或中间产物，L1 / L2 引用、L4 保存 | 文件、报告、差异、执行日志等；引用需要权限、完整性和生命周期 |
| Checkpoint | 恢复数据，L2 经 L3 持久化 | 保存重新接管所需状态；不自动证明外部动作没有执行过 |
| Resume | 生命周期机制，L2 | 从可靠进度继续，而不是简单把历史重新喂给模型 |
| Fork | 分支机制，L2 | 从某个状态开始探索新分支；不自动复制或回滚外部世界 |
| Replay | 调试或重建机制，L2 / 质量面 | 可重放记录或重新执行；必须声明哪一种，避免重复副作用 |
| Retry / Backoff | 失败处理机制，L2 / L3 | 针对明确可重试错误重试；不能把超时一律当成未执行 |
| Idempotency / Operation Ledger | 动作可靠性机制，跨 L2–L4 | 用稳定操作标识关联重复请求和结果；效果依赖底层接口契约 |
| Reconciliation | 恢复机制，L2 + L3 / L4 | 对结果未知的外部动作核对真实状态，再决定下一步 |
| Compensation | 业务恢复动作，L1 定义、受控执行 | 尝试补救已发生副作用；不是保证成功的通用回滚按钮 |
| Lease / Fencing / State Version | 并发控制机制，L2 + L4 | 避免多个 Worker 同时推进同一执行，阻止过期执行者继续写入 |
| Cancellation / Timeout | 生命周期机制，L2 | 约束继续执行和等待；取消请求不等于已发生动作被撤销 |
| Scheduler / Queue / Backpressure | 调度与容量机制，L2 + 基础设施 | 控制任务、模型、工具和子 Agent 的并发；不属于模型的推理能力 |

对象的精确定义与失败时间线见[执行与状态](lifecycle-and-state.md)。通用分布式机制由 [AI Backend Engineering](../../backend-engineering/README.md)维护，Agent 特化见[副作用与取消](../docs/07-ToolSideEffectCancellation.md)、[恢复](../docs/13-CheckpointResumeReliability.md)。

## 5. 多 Agent、环境与模型资源

| 概念 | 类型与主要位置 | 解决的问题与边界 |
|---|---|---|
| Multi-agent | 协作拓扑，L2 驱动，L1 定义任务边界 | 对职责、上下文或能力进行分工；不是架构图外的一层 |
| Subagent / Delegation | 委派模式，L2 | 子执行单元处理限定任务并返回结果；需要上下文、预算和权限边界 |
| Manager-worker / Supervisor | 管理与分工模式，L2 | 一个控制单元分配任务并整合结果；不能默认解决冲突和质量验证 |
| Handoff | 控制权交接模式，L2 | 后续处理由另一个角色接管；区别于调用子任务后继续由原角色控制 |
| Parallel / Fan-out / Join | 并行与汇合机制，L2 | 处理可分离任务；需要合并标准、超时策略和总预算 |
| Workspace Concurrency | 环境一致性问题，L2 + L4 | 管理并发文件或资源修改；独立上下文不等于独立外部资源 |
| Sandbox | 隔离执行环境，L4；受安全策略控制 | 限制文件、进程、网络与计算资源；不是业务授权或事实核验器 |
| Workspace / File System | 工作资源，L4 | 保存任务工作文件、输入与产物；生命周期、共享范围和恢复规则要明确 |
| Shell / Code Execution / Browser Use | 行动能力，L3 接口 + L4 环境 | 通过命令、代码或界面产生动作；须处理观察时效和执行风险 |
| Computer Use / Multimodal | 输入与行动形态，跨层 | L1 收集交互，L2 使用观察，L3 适配，L4 提供模型和环境；不是新增层 |
| Realtime / Voice Agent | 时延与交互约束下的系统形态 | 在原框架上增加中断、音视频时序和低延迟要求；不能只理解为换一个模型 |
| Model Serving / KV Cache | 模型基础设施，L4 | 服务推理与计算复用；KV Cache 不等于用户长期记忆 |
| Local / Hosted / Hybrid | 部署选择 | 决定责任部署在哪、哪些由供应商承接；不改变任务责任必须有人拥有 |
| Managed Harness | 托管实现选择，覆盖部分 L2 / L3 / L4 | 转移部分运行与基础设施工作；不会自动定义你的业务验收与授权范围 |

多 Agent 实践与 Harness / 环境解耦分别参考 [S15](sources.md#s15)、[S04](sources.md#s04)。本表对实时、多模态和部署的归位是应用同一架构的推导，不指定某产品当前支持范围。

深入：[Multi-agent / A2A / Workspace](../docs/18-MultiAgentA2AWorkspace.md)、[Coding Agent 工作闭环](../docs/21-CodingAgentWorkflow.md)、[Production Runtime](../docs/22-ProductionAgentRuntime.md)、[模型基础](../../llm-foundation/README.md)。

## 6. 安全与质量：贯穿四层的责任

| 概念 | 核心责任 | 不能被什么替代 |
|---|---|---|
| Identity / Tenant Isolation | 谁代表谁，能访问哪些状态、数据、凭证和产物 | 只在一张表里添加 tenant_id |
| Authorization / Least Privilege | 每次实际动作是否在允许范围内 | 模型说它被允许，或工具已被列出 |
| Approval / HITL | 对具体行为进行确认、补充信息或接管 | 一次无范围、无期限的批准 |
| Guardrails / Prompt Injection Defense | 检测误导与风险，约束信任传播和损害范围 | 只靠 Prompt 告诫，或仅检查最终文本 |
| Secrets / Supply-chain Control | 凭证代理、插件与技能来源、版本和脚本权限 | 把敏感信息全交给模型或不可信环境 |
| Trace / Observability | 记录可观察的输入输出、调用、状态和资源用量 | 假定能读取模型全部内部推理 |
| Audit | 回答谁在什么权限下执行了什么 | 可随意采样丢弃的调试日志 |
| Online Verification | 判断当前结果是否满足验收条件 | 模型自我宣告完成 |
| Evaluation / Regression | 在代表性任务上检验质量、安全与变化 | 一个演示成功或单次主观观感 |
| LLM-as-Judge | 一种评分工具，需校准、抽检和限制 | 确定性的事实核验或独立权威 |
| Benchmark | 特定任务分布下的比较工具 | 自己业务中的真实成功率 |
| Cost / Latency / Capacity | 衡量整条任务路径及瓶颈 | 只看单次模型 Token 或 API QPS |
| Release / Rollback / Versioning | 管理模型、Prompt、工具、技能、策略与索引的变化 | 静默更新全部依赖 |
| Feedback / Data Flywheel | 从授权采集的失败证据形成可复现回归 | 自动把用户数据永久保存或直接用于训练 |

深入：[安全](../docs/15-GuardrailsInjectionContainment.md)、[Trace](../docs/19-TraceReplayObservability.md)、[Eval](../docs/20-AgentEvaluationBenchmark.md)、[模型适配与韧性](../docs/17-RoutingProviderResilience.md)、[生产架构](../docs/22-ProductionAgentRuntime.md)。

## 7. 哪些是基本责任，哪些是按需机制

**基本责任**是任务与约束、输入和输出、执行控制、状态与结束判定。对于真实生产动作，还需要与风险相匹配的授权、可靠性和可验证证据。即使某责任只用十几行代码实现，它仍然存在。

**按需求增加的机制**包括 RAG、长期记忆、独立 Planner、多 Agent、向量数据库、通用代码沙箱、复杂队列集群和专门的图检索。没有它们不代表系统不成熟；没有弄清它们为什么需要，反而可能引入无价值的复杂度。

**同一个模块可由不同机制实现。** Context Manager 可以先只做选择和预算，之后再加入 offloading 或 compaction。Memory Store 可以使用文件、关系数据库或其他合适存储，并不天然要求向量数据库。

## 8. 以后遇到新名词的记录模板

```text
名称与工作定义：
类型：能力 / 模块 / 机制 / 对象 / 模式 / 协议 / 资源 / 横切要求
主要责任：L1 / L2 / L3 / L4 / 贯穿
它解决的具体缺口：
输入、输出与依赖：
何时需要，何时不需要：
最关键的失败方式：
怎样验证收益与正确性：
正式机制章节与来源版本：
```

**知识地图的完整性，不是靠冻结一份永远增长的名词清单，而是让每个新概念都有稳定的归位规则。**
