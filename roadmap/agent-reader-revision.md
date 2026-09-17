# Agent 读者修订｜从看过术语到讲清过程

[← Handbook](../README.md) · [Agent 教材](../agent-harness/README.md) · [研究与源码核验](../research/agent-sources/README.md#reader-revision-20260917) · [历史终审](final-quality-audit.md)

## 1. 本轮范围和出发点

修订日期：2026-09-17。基线为main提交`37cbfd2b152c6a0aa5bbd8ca0c19820debc632b8`。只修订main的Agent23章及其学习、研究说明入口，不合并、不修改16章架构分支；路径、章节次序、184篇总正文与44道Agent研究能力不变。

读者已经认真读完，仍不理解注册、上下文具体顺序、状态、持久化与追踪，说明“文件存在、有术语、有自测”的旧验收不充分。这里记录实际写作修订，不把问题归因于只读过一遍，也不把历史PASS改写成读者理解已验证。

## 2. 将反馈归为七类并分别处理

| 问题类型 | 旧阅读障碍 | 本轮处理 |
|---|---|---|
| 主体未定义 | 一上来谈State字段，却不知道State是什么 | 先说明程序下一步需要知道什么，用同一份文件报告任务逐步演示 |
| 生命周期缺失 | 注册、发现、暴露、调用混成“加载工具” | 分开本地实现目录、模型Schema、按需发现和实际执行，给往返与运行小例子 |
| 抽象没有落地 | 只讲稳定前缀、总结，没有具体实现 | 正文先解释过程，再折叠展示固定Codex/Claude入口、触发、变更和输出 |
| 职责交叉与重复 | 校验、审批、沙箱、重试好像重复答案 | 说明每个门检查的不同问题；跨章只保留桥梁，链接回主责机制 |
| 数据保留过度 | 好像一切都要版本化、写Trace | 分开恢复记录、产物、诊断与授权调试快照；ID与版本分别解释，按需要保存 |
| 训练变弱 | 合并后章末题太少、答案像口号 | 每章就地保留面试回答、易错辨析和解释型折叠自测，不用集中入口替代 |
| 术语与来源不透明 | MCP/A2A/框架只有名词、英文默认懂 | 中文定义与维度表，按官方版本走完整协议/框架流程，明确源码功能开关 |

首次学习仍沿原有知识依赖；真人面经只校准代表问法和深度。没有为了热度重新排序，也不增加新的采集来源。

## 3. 读者的具体疑问在何处回答

| 疑问 | 主责章节及改进 |
|---|---|
| Harness、Runtime、Orchestrator、Workflow区别 | [01全貌](../agent-harness/docs/01-AgentHarness在AI应用中的职责.md)、[02边界](../agent-harness/docs/02-AgentWorkflowHarnessBoundary.md)：工作定义、责任表、同任务对比 |
| Session / Run / Turn / Step | [03执行层级](../agent-harness/docs/03-AgentLoopRuntimeState.md)：保留有声明口径的教学树，另列Codex Thread/Turn/Item，不能强制等同 |
| 工具怎么注册，元数据是否都给模型 | [04契约](../agent-harness/docs/04-ToolContractSchemaValidation.md)、[05注册发现](../agent-harness/docs/05-ToolRegistryRouterDiscovery.md)：目录、Schema投影、真实handler、按需加载 |
| 所有错误是否发给模型 | [06执行失败](../agent-harness/docs/06-ToolExecutionFailure.md)：按可行动性分别交模型、运行时、用户或诊断系统 |
| 取消为何传播，迟到成功怎么办 | [07并发取消](../agent-harness/docs/07-ToolSideEffectCancellation.md)：等待者与执行者不同，子任务清理和结果核对 |
| 运行中用户再发消息 | [03](../agent-harness/docs/03-AgentLoopRuntimeState.md)、[08控制](../agent-harness/docs/08-PlanningGoalStopBudget.md)：排队、调整约束、打断与安全边界；Claude队列在工具结果后处理 |
| 计划更新到底放哪儿 | [08](../agent-harness/docs/08-PlanningGoalStopBudget.md)、[09上下文](../agent-harness/docs/09-ContextAssemblyBudget.md)：当前计划视图与追加历史不同；产品计划工具和附件不是每轮改系统前缀 |
| Codex/Claude上下文顺序与缓存 | [09](../agent-harness/docs/09-ContextAssemblyBudget.md)：连续请求例子、base instructions / input / tools与system / messages / tools具体路径 |
| 压缩何时触发、几种方式、Prompt及范围 | [10压缩](../agent-harness/docs/10-ContextCompactionCorrectness.md)：本地/远程路径、配置阈值、保留/替换、Claude功能开关和附件重建；不承诺所有版本固定几层 |
| Memory提取、更新、长期化、纠错与冲突 | [11记忆](../agent-harness/docs/11-MemoryArchitectureLifecycle.md)：偏好例子的生命周期，Claude索引/主题文件与Codex两阶段整理分开 |
| State和Persistence想干什么 | [12状态持久化](../agent-harness/docs/12-SessionStatePersistence.md)：当前工作台与可跨重启记录、字段服务的决定、哪些不必保存 |
| 两次Checkpoint间崩溃 | [13恢复](../agent-harness/docs/13-CheckpointResumeReliability.md)：可重算、已确认、结果未知三种处理；下游无核对/幂等能力不能编造保证 |
| Resume是否摘要，Replay是否重做 | [13](../agent-harness/docs/13-CheckpointResumeReliability.md)：Resume恢复执行、Summary摘要；回看、重建状态、重跑模型与真实副作用分别说明 |
| Sandbox和Docker | [14权限隔离](../agent-harness/docs/14-PermissionApprovalSandbox.md)：安全目标与具体实现工具不同，挂载/网络/凭证等维度比较 |
| 相同工具为何还要校验/政策/批准/沙箱 | [04](../agent-harness/docs/04-ToolContractSchemaValidation.md)、[14](../agent-harness/docs/14-PermissionApprovalSandbox.md)、[15安全](../agent-harness/docs/15-GuardrailsInjectionContainment.md)：形状、业务约束、身份授权与环境强制不是重复检查 |
| MCP Host/Client/Server和原理 | [16协议扩展](../agent-harness/docs/16-MCPSkillsHooks.md)：官方定义、发现到调用的往返、版本差异与示例消息 |
| A2A原理，是否所有子Agent都用它 | [18协作](../agent-harness/docs/18-MultiAgentA2AWorkspace.md)：内部委派与独立系统互操作，AgentCard/Task/Message/Artifact及调用流程 |
| Trace是不是仍保存所有内容 | [19追踪](../agent-harness/docs/19-TraceReplayObservability.md)：轻量阶段定位到授权深查，诊断与恢复可靠性分离，不能保证重现外部世界 |
| 框架对比没有核心语义 | [23选型](../agent-harness/docs/23-FrameworkMappingBuildVsBuy.md)：官方SDK Agent/Runner/Session，LangGraph StateGraph/Checkpointer/Store/interrupt，LangChain create_agent的关系 |

17路由、20评测、21代码交付、22生产组合也按相同标准重写，而不只修复读者点名的章节。23章都保留章末三件套，其他章节对状态、取消和追踪的表述与主责章节一致。

## 4. 具体来源与诚实边界

Codex固定快照为`fc948f8c473e5d11e780ffcf1fd7f812a2020932`；Claude Code为用户提供的私有快照`58231dcce408f805c645cfbc352d2876b517223b`。本轮读取具体函数、调用点及相关模板；不从目录名推断算法，也不把私有快照中的实验开关当全体公开用户默认行为。完整核验入口见[来源索引](../research/agent-sources/README.md#reader-revision-20260917)。

MCP主要依据用户指定的官方2026-07-28文档，并明确对比2025-11-25生命周期；A2A按官方1.0命名区分旧0.3调用表示。两份产品快照与当前官方文档是不同证据，不拼成一个实际不存在的产品版本。未来版本变化必须重新核对。

通用文件报告、故障时间线、记录策略与练习均为教学设计，不冒充产品实现或真人面试原话。源码对照折叠可选，主文无需先读源码才能理解。

## 5. 训练与回归检查

本轮23章共101个“面试怎么答”、141个解释型自测、112条易错辨析；答案在本章默认折叠。集中面试页保留原有56个问题，更新对应答案与章节链接。Review保持第二遍复习角色，不另建一条学习路线。

复核命令：

```bash
python tools/validate_agent_readability.py
python tools/validate_agent_readability.py --run-examples
```

机械检查覆盖章节数/编号、章末结构与折叠、研究能力映射、普通仓库内文件链接、Python语法。显式标记的四个标准库教学例子分别测试反馈循环、工具注册投影、追加历史/计划视图、检查点间未知结果核对；无网络、真实模型、真实付款或外部副作用。

本轮在完整main快照上实际执行上述命令，输出为：

```text
Agent chapters: 23; curriculum: 184; Canonical: 44
Chapter interviews: 101; self-tests: 141; pitfall rows: 112
Inline local file links checked: 1182; errors: 0
Executed: minimal_feedback_loop, registry_projection, append_and_plan_view, recovery_window
Protected research files compared: 59; changed: 0
Pinned Codex source paths cited: 11; missing: 0
```

发布过程会在GitHub实际checkout上再次执行结构和四个教学例子检查，结果以工作流日志为准。测试通过只说明这些有限断言和文档结构成立；不等于所有外部链接或Markdown渲染器测试，不等于协议SDK集成测试，也不等于生产数据库崩溃恢复验证。

## 6. 完成与尚不可宣称的事情

写作修订不以“超过多少KB”判定完成。应人工检查概念是否定义、疑问是否在本章回答、例子是否走到结果、源码是否给出可核对路径、重复段是否有不同责任，以及章末答案是否解释原因。

本轮对上述反馈已提供对应正文与训练，并保留待真实读者验证的边界：不能替读者宣布第一次阅读一定全部理解，不能用增加题数证明消除了所有晦涩。后续出现具体卡点，应依据这张表定位正文并继续修订，不让用户先去外部猜出本章讲解主体。
