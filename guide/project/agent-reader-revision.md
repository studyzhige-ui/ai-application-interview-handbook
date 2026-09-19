# Agent 内容保留、教学修订与发布记录

[← Agent教材](../../curriculum/09-curriculum/09-agent/README.md) · [Handbook](../../README.md) · [历史终审](../audits/final-quality-audit.md)

## 1. 这次的底稿和边界

以用户认可的丰富旧main `37cbfd2b152c6a0aa5bbd8ca0c19820debc632b8`为教学底稿，以`83a3b96c10d8a3feb2c87d8fa2e59c02b8e8f178`为发布前基线。不再把压缩版当主要底稿，也不合并16章架构分支。

原23章调整为24章：MCP完整协议生命周期与Skill/Hook/Plugin扩展生命周期分别讲清；其余知识范围保留，在章内组织定义、过程、例子、失败与实现对照。章节数是边界判断结果，不是预设目标。

## 2. 保留的教学过程与明确修正

原编号小节的机制、例子、错误与失败推演逐项记录去向。不能用一个全局“重试/降级”清单替代某机制独有的故障窗口。章末保持HUMAN-A信号、可见的Q与🎯回答、⚠️易错提醒、题目可点击的折叠自测四种形式。源码对照可选折叠，面试答案不隐藏。

不是逐字保留错误：损坏缩进的旧循环代码换成有注释的教学例子；Session/Run/Turn/Step声明本书口径并与产品对象分别解释；128k预算表修正算术；工具调用不等于跨系统原子事务；前缀缓存与回答缓存分开；Trace与必要恢复记录分别留存；协议和框架按官方核心语义展开。这些改动的原因在下表标明。

## 3. 重点核对的失败机制

工具结构/语义错误、拒绝授权、临时故障、超时、未知/部分副作用；并发资源冲突、取消传播和迟到回执；重复行动、计划偏离；大结果、过期上下文、摘要遗漏与压缩失败；记忆错误/冲突/过期；检查点间崩溃、恢复核对、租约和分叉；批准对象变化、注入、凭证与外传；扩展失效和版本不兼容、供应商降级；子任务失败、循环委派、共享工作区；诊断不足、评测回归遗漏、代码验证与交付、生产故障域及框架升级迁移。

它们仍在对应主责章节，不是因主题重复出现就删除。需要重复的桥梁会说明各责任检查什么，避免多章都给同一段万能答案。

## 4. 原小节去向

下面是内容组织的可检查记录，不把锚点存在或文本命中率等同于技术质量。原章末形式合并回本章；源码实现放回可选对照。

<details>
<summary>展开原23章的编号小节与新位置</summary>

| 原章/节 | 原小节 | 新位置 | 处理 |
|---|---|---|---|
| 01/01 | 先讲人话：Model 很聪明，但它不会替你经营一次“执行” | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-01) | 保留并增补解释 |
| 01/02 | 一个实用定义 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-02) | 保留并增补解释 |
| 01/03 | 为什么“Model + API”还不够 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-03) | 保留并增补解释 |
| 01/04 | Harness 的八个工程平面 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-04) | 保留并增补解释 |
| 01/05 | 一个最小 Runtime 长什么样 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-05) | 明确修正后讲解：修复旧示意代码的损坏缩进；保留所有循环责任，并把可运行小例子放到03 |
| 01/06 | Model 和 Harness 到底各负责什么 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-06) | 保留并增补解释 |
| 01/07 | 成熟产品源码告诉我们的什么 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-07) | 保留到章内来源对照 |
| 01/08 | 官方资料为什么也强调 Harness，而不是只强调模型 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-08) | 保留到章内来源对照 |
| 01/09 | 一个 AI 应用场景：企业知识库 Agent | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-09) | 保留并增补解释 |
| 01/10 | Harness、Backend、Framework 不要混在一起 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#legacy-01-10) | 保留并增补解释 |
| 01/11 | 高频易错点 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#pitfalls) | 易错辨析 |
| 01/12 | 面试怎么回答 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#interview) | 面试回答 |
| 01/13 | 本章证据边界 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#human-a) | HUMAN-A |
| 01/14 | 自测 | [01](../../curriculum/09-curriculum/09-agent/docs/01-AgentSystemAndResponsibilities.md#self-test) | 自测 |
| 02/01 | 先讲人话：Agent 化的本质是什么 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-01) | 保留并增补解释 |
| 02/02 | 为什么“更 Agent”不等于“更高级” | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-02) | 保留并增补解释 |
| 02/03 | 什么任务更值得 Agent 化 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-03) | 保留并增补解释 |
| 02/04 | Production 往往是 Hybrid | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-04) | 保留并增补解释 |
| 02/05 | 为什么 Model + API 还不够 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-05) | 保留并增补解释 |
| 02/06 | Harness / Runtime 到底是什么 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-06) | 明确修正后讲解：明确术语重叠和本书工作定义，避免虚构行业统一边界 |
| 02/07 | Harness、Runtime、Orchestrator、Workflow Engine 怎么区分 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-07) | 明确修正后讲解：保留四种角色，改成同维度职责比较 |
| 02/08 | 三个经常混淆的边界 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-08) | 保留并增补解释 |
| 02/09 | 源码证据：为什么成熟产品一定有 Runtime Layer | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-09) | 保留到章内来源对照 |
| 02/10 | Agent 化之后立刻新增哪些工程问题 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#legacy-02-10) | 保留并增补解释 |
| 02/11 | HUMAN-A 为什么高频追这个边界 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#human-a) | HUMAN-A |
| 02/12 | 🎯 30 秒回答 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#interview) | 面试回答 |
| 02/13 | 🎯 2–3 分钟回答框架 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#interview) | 面试回答 |
| 02/14 | ⚠️ 易错点 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#pitfalls) | 易错辨析 |
| 02/15 | 🔍 面试官继续追问 | [02](../../curriculum/09-curriculum/09-agent/docs/02-WorkflowAutonomyAndRuntimeBoundary.md#interview) | 追问 |
| 03/01 | 先讲人话：Agent 的核心不是“会调用 Tool”，而是会循环推进任务 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-01) | 保留并增补解释 |
| 03/02 | 一个最小可运行的 Agent Loop | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-02) | 明确修正后讲解：原代码缩进损坏；保留state/model/tool/observation/stop，换成有注释的有限教学测试 |
| 03/03 | 为什么要分 Run / Turn / Step | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-03) | 明确修正后讲解：保留Session→Run→Turn→Step教学树，声明Turn含义并与产品对象分别映射 |
| 03/04 | 为什么这个分层对 Failure 很重要 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-04) | 明确修正后讲解：统一教学Turn口径，保留Step失败与Run失败的区别 |
| 03/05 | Runtime 不是只有 Message，还需要 Event | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-05) | 保留并增补解释 |
| 03/06 | Event 为什么最好是结构化的 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-06) | 保留并增补解释 |
| 03/07 | Correlation ID 为什么关键 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-07) | 保留并增补解释 |
| 03/08 | State Machine：Loop 不只是 while True | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-08) | 保留并增补解释 |
| 03/09 | Runtime State 应该有什么 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-09) | 保留并增补解释 |
| 03/10 | 新用户指令怎样进入正在运行的 Agent | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-10) | 保留并增补解释 |
| 03/11 | 源码证据：Claude Code | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-11) | 保留到章内来源对照 |
| 03/12 | 源码证据：Codex | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-12) | 保留到章内来源对照 |
| 03/13 | Loop 什么时候继续，什么时候停止 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#legacy-03-13) | 保留并增补解释 |
| 03/14 | HUMAN-A 对应 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#human-a) | HUMAN-A |
| 03/15 | 🎯 30 秒回答 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#interview) | 面试回答 |
| 03/16 | ⚠️ 易错点 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#pitfalls) | 易错辨析 |
| 03/17 | 🔍 继续追问 | [03](../../curriculum/09-curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md#interview) | 追问 |
| 04/01 | 先讲人话：为什么 Tool 不能只写成一个 Python 函数 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-01) | 保留并增补解释 |
| 04/02 | Tool Contract 的最小结构 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-02) | 保留并增补解释 |
| 04/03 | Schema 解决两个完全不同的问题 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-03) | 保留并增补解释 |
| 04/04 | 结构校验 vs 语义校验 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-04) | 保留并增补解释 |
| 04/05 | Tool Description 也是协议的一部分 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-05) | 保留并增补解释 |
| 04/06 | Structured Result 也应该有 Contract | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-06) | 保留并增补解释 |
| 04/07 | Tool Arguments 出错时怎么处理 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-07) | 保留并增补解释 |
| 04/08 | Repair 不能无限循环 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-08) | 保留并增补解释 |
| 04/09 | Side-effect Metadata 为什么应该靠 Runtime 保存 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-09) | 保留并增补解释 |
| 04/10 | 源码证据：Claude Code | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-10) | 保留到章内来源对照 |
| 04/11 | 源码证据：Codex | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-11) | 保留到章内来源对照 |
| 04/12 | 版本升级怎么办 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#legacy-04-12) | 保留并增补解释 |
| 04/13 | HUMAN-A 对应 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#human-a) | HUMAN-A |
| 04/14 | 🎯 30 秒回答 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#interview) | 面试回答 |
| 04/15 | ⚠️ 易错点 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#pitfalls) | 易错辨析 |
| 04/16 | 🔍 继续追问 | [04](../../curriculum/09-curriculum/09-agent/docs/04-ToolContractAndValidation.md#interview) | 追问 |
| 05/01 | Registry 解决什么 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-01) | 保留并增补解释 |
| 05/02 | Registry 与 Model-visible Tool Set 必须分开 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-02) | 保留并增补解释 |
| 05/03 | Router 做什么 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-03) | 保留并增补解释 |
| 05/04 | 为什么需要 Namespace | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-04) | 保留并增补解释 |
| 05/05 | Tool Exposure 不应该只有“注册 / 未注册” | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-05) | 保留并增补解释 |
| 05/06 | Progressive Discovery 的核心 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-06) | 保留并增补解释 |
| 05/07 | Tool Discovery 可以怎么做 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-07) | 保留并增补解释 |
| 05/08 | Discovery 的 Evaluation | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-08) | 保留并增补解释 |
| 05/09 | Tool Unavailable 怎么办 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-09) | 保留并增补解释 |
| 05/10 | 源码证据：Codex | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-10) | 保留到章内来源对照 |
| 05/11 | 源码证据：Claude Code | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-11) | 保留到章内来源对照 |
| 05/12 | Registry 更新与版本问题 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#legacy-05-12) | 保留并增补解释 |
| 05/13 | HUMAN-A 对应 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#human-a) | HUMAN-A |
| 05/14 | 🎯 30 秒回答 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#interview) | 面试回答 |
| 05/15 | ⚠️ 易错点 | [05](../../curriculum/09-curriculum/09-agent/docs/05-ToolRegistrationAndDiscovery.md#pitfalls) | 易错辨析 |
| 06/01 | 一次完整 Tool Execution | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-01) | 保留并增补解释 |
| 06/02 | Executor 为什么不应该直接暴露原始函数 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-02) | 保留并增补解释 |
| 06/03 | Tool Result 不是一段字符串 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-03) | 保留并增补解释 |
| 06/04 | 为什么日志、模型输出、Host Metadata 应分层 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-04) | 保留并增补解释 |
| 06/05 | Failure Classification | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-05) | 保留并增补解释 |
| 06/06 | Repair、Retry、Fallback、Fail 不是一回事 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-06) | 保留并增补解释 |
| 06/07 | Retry Eligibility 必须先判断幂等与副作用 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-07) | 保留并增补解释 |
| 06/08 | Timeout 也不是一种简单失败 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-08) | 保留并增补解释 |
| 06/09 | 错误反馈给模型应该“可行动” | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-09) | 保留并增补解释 |
| 06/10 | Result Validation | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-10) | 保留并增补解释 |
| 06/11 | Pre / Post Tool Hook 为什么很有用 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-11) | 保留并增补解释 |
| 06/12 | 源码证据：Codex | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#legacy-06-12) | 保留到章内来源对照 |
| 06/13 | HUMAN-A 对应 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#human-a) | HUMAN-A |
| 06/14 | 🎯 30 秒回答 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#interview) | 面试回答 |
| 06/15 | ⚠️ 易错点 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#pitfalls) | 易错辨析 |
| 06/16 | 🔍 继续追问 | [06](../../curriculum/09-curriculum/09-agent/docs/06-ToolExecutionAndFailure.md#interview) | 追问 |
| 07/01 | 为什么 Tool 不能默认并发 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-01) | 保留并增补解释 |
| 07/02 | Tool Side Effect 分类 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-02) | 保留并增补解释 |
| 07/03 | Concurrency Safety 应是 Tool Contract 的一部分 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-03) | 保留并增补解释 |
| 07/04 | Resource Key 比“Tool Name”更准确 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-04) | 保留并增补解释 |
| 07/05 | 用户取消为什么必须传播 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-05) | 保留并增补解释 |
| 07/06 | Cancellation 是协议，不是一个布尔值 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-06) | 保留并增补解释 |
| 07/07 | Parent / Child Cancellation | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-07) | 保留并增补解释 |
| 07/08 | Progress 为什么是 Runtime Primitive | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-08) | 保留并增补解释 |
| 07/09 | Streaming Result 与 Final Result 要分开 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-09) | 保留并增补解释 |
| 07/10 | 源码证据：Claude Code | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-10) | 保留到章内来源对照 |
| 07/11 | 源码证据：Codex | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-11) | 保留到章内来源对照 |
| 07/12 | Side Effect + Cancellation 的危险窗口 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#legacy-07-12) | 保留并增补解释 |
| 07/13 | HUMAN-A 对应 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#human-a) | HUMAN-A |
| 07/14 | 🎯 30 秒回答 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#interview) | 面试回答 |
| 07/15 | ⚠️ 易错点 | [07](../../curriculum/09-curriculum/09-agent/docs/07-ToolConcurrencyAndCancellation.md#pitfalls) | 易错辨析 |
| 08/01 | 先讲人话：Planning 不是“先写一份超长计划” | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-01) | 保留并增补解释 |
| 08/02 | ReAct 解决什么问题 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-02) | 保留并增补解释 |
| 08/03 | Plan-Execute-Replan 什么时候更合适 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-03) | 保留并增补解释 |
| 08/04 | Goal Control：Agent 怎么知道自己还在做原任务 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-04) | 保留并增补解释 |
| 08/05 | Stop Condition 不是只有 `max_steps` | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-05) | 保留并增补解释 |
| 08/06 | Budget 应该是多维的 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-06) | 保留并增补解释 |
| 08/07 | Dead Loop / Oscillation 怎么检测 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-07) | 保留并增补解释 |
| 08/08 | Dynamic Instruction / Steering 怎么进入当前 Run | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-08) | 保留并增补解释 |
| 08/09 | Planning Failure Timeline | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-09) | 保留并增补解释 |
| 08/10 | Framework 不应该决定你的 Planning 模型 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#legacy-08-10) | 保留并增补解释 |
| 08/11 | 证据分层 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#human-a) | HUMAN-A |
| 08/12 | 面试怎么答 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#interview) | 面试回答 |
| 08/13 | 高频易错点 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#pitfalls) | 易错辨析 |
| 08/14 | 本章自测 | [08](../../curriculum/09-curriculum/09-agent/docs/08-PlanningGoalAndControl.md#self-test) | 自测 |
| 09/01 | Context、Memory、State、History 先分清 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-01) | 保留并增补解释 |
| 09/02 | 一次 Agent Context 可能来自哪些 Source | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-02) | 保留并增补解释 |
| 09/03 | Context Assembly 应该是“Compiler”，不是字符串拼接 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-03) | 保留并增补解释 |
| 09/04 | Assembly Order 为什么重要 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-04) | 明确修正后讲解：保留顺序/稳定前缀原则，补连续请求与计划更新；不把抽象八段当每轮重排规则 |
| 09/05 | Token Budget 要分区，而不是统一“还剩多少” | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-05) | 保留并增补解释 |
| 09/06 | Claude Code 源码提供了什么实现证据 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-06) | 保留到章内来源对照 |
| 09/07 | Large Tool Result 为什么不能直接塞回 Context | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-07) | 保留并增补解释 |
| 09/08 | Offloading 和 Truncation 有什么区别 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-08) | 保留并增补解释 |
| 09/09 | Prompt / Context Cache 应该缓存什么 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-09) | 明确修正后讲解：区分前缀计算缓存、工具说明缓存、应用结果缓存，纠正旧混用 |
| 09/10 | Context Pollution / Stale Context | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-10) | 保留并增补解释 |
| 09/11 | Context Dedup 为什么重要 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-11) | 保留并增补解释 |
| 09/12 | Context Assembly Failure Timeline | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#legacy-09-12) | 保留并增补解释 |
| 09/13 | HUMAN-A 信号 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#human-a) | HUMAN-A |
| 09/14 | 面试怎么答 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#interview) | 面试回答 |
| 09/15 | 高频易错点 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#pitfalls) | 易错辨析 |
| 09/16 | 本章自测 | [09](../../curriculum/09-curriculum/09-agent/docs/09-ContextAssemblyAndCache.md#self-test) | 自测 |
| 10/01 | Compaction 为什么存在 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-01) | 保留并增补解释 |
| 10/02 | Compaction 与普通 Summary 的区别 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-02) | 保留并增补解释 |
| 10/03 | Codex `compact.rs` 给出的实现证据 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-03) | 明确修正后讲解：保留旧实现主题，展开固定Codex触发、prompt、范围、输出、替换与继续 |
| 10/04 | Claude Code 侧提供了什么证据 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-04) | 明确修正后讲解：保留旧实现主题，展开Claude条件路径、阈值、摘要和附件重建；不假定所有构建相同 |
| 10/05 | Compaction 什么时候触发 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-05) | 保留并增补解释 |
| 10/06 | 哪些信息必须保留 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-06) | 保留并增补解释 |
| 10/07 | 哪些内容适合压缩或外部化 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-07) | 保留并增补解释 |
| 10/08 | Replacement History 为什么重要 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-08) | 保留并增补解释 |
| 10/09 | Compaction Correctness 怎样验证 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-09) | 保留并增补解释 |
| 10/10 | Compaction 失败怎么办 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-10) | 保留并增补解释 |
| 10/11 | Stale Context 是另一类问题 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-11) | 保留并增补解释 |
| 10/12 | Summary Error 会产生“压缩后的错误记忆” | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-12) | 保留并增补解释 |
| 10/13 | Compaction 和 Memory 的边界 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#legacy-10-13) | 保留并增补解释 |
| 10/14 | HUMAN-A 信号 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#human-a) | HUMAN-A |
| 10/15 | 面试怎么答 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#interview) | 面试回答 |
| 10/16 | 高频易错点 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#pitfalls) | 易错辨析 |
| 10/17 | 本章自测 | [10](../../curriculum/09-curriculum/09-agent/docs/10-CompactionAndContinuation.md#self-test) | 自测 |
| 11/01 | 先把 Context / Memory / State / History 分开 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-01) | 保留并增补解释 |
| 11/02 | Memory 为什么不能“什么都存” | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-02) | 保留并增补解释 |
| 11/03 | Memory 可以怎样分层 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-03) | 保留并增补解释 |
| 11/04 | 什么时候应该写 Memory | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-04) | 保留并增补解释 |
| 11/05 | Extraction：从对话变成 Memory Record | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-05) | 保留并增补解释 |
| 11/06 | Retrieval-on-demand 为什么比“全量注入”更重要 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-06) | 保留并增补解释 |
| 11/07 | Memory Consolidation 是什么 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-07) | 保留并增补解释 |
| 11/08 | Memory Correctness：错误事实比“没有记住”更危险 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-08) | 保留并增补解释 |
| 11/09 | Memory Conflict 怎么处理 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-09) | 保留并增补解释 |
| 11/10 | Memory Staleness / Expiration | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-10) | 保留并增补解释 |
| 11/11 | Privacy / Tenant Boundary | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-11) | 保留并增补解释 |
| 11/12 | Claude Code 固定源码侧的证据 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-12) | 明确修正后讲解：保留源码证据并展开Claude文件型记忆与Codex两阶段流水线，和Compaction分开 |
| 11/13 | HUMAN-A 信号 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#human-a) | HUMAN-A |
| 11/14 | Memory Failure Timeline | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#legacy-11-14) | 保留并增补解释 |
| 11/15 | 面试怎么答 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#interview) | 面试回答 |
| 11/16 | 高频易错点 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#pitfalls) | 易错辨析 |
| 11/17 | 本章自测 | [11](../../curriculum/09-curriculum/09-agent/docs/11-MemoryLifecycle.md#self-test) | 自测 |
| 12/01 | Session 是什么 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-01) | 保留并增补解释 |
| 12/02 | Run / Turn / Step 再复习 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-02) | 明确修正后讲解：保留层级与产品差异，消除旧章对Turn的相互冲突定义 |
| 12/03 | State 应该保存什么 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-03) | 保留并增补解释 |
| 12/04 | History 应该是事件流，而不是“一个超长字符串” | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-04) | 保留并增补解释 |
| 12/05 | Snapshot 与 Event Log 怎么配合 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-05) | 保留并增补解释 |
| 12/06 | Persistence 不等于把 Context 存下来 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-06) | 保留并增补解释 |
| 12/07 | Session Store 选什么 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-07) | 保留并增补解释 |
| 12/08 | Tenant Isolation 为什么必须进入 State Schema | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-08) | 保留并增补解释 |
| 12/09 | Session Hijack / Cross-tenant Pollution | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-09) | 保留并增补解释 |
| 12/10 | Concurrency：同一个 Session 同时来两个请求怎么办 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-10) | 保留并增补解释 |
| 12/11 | State Version 为什么重要 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-11) | 保留并增补解释 |
| 12/12 | Cold Resume 与 Warm Resume | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-12) | 保留并增补解释 |
| 12/13 | Session Retention / Deletion | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#legacy-12-13) | 保留并增补解释 |
| 12/14 | HUMAN-A 信号 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#human-a) | HUMAN-A |
| 12/15 | 面试怎么答 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#interview) | 面试回答 |
| 12/16 | 高频易错点 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#pitfalls) | 易错辨析 |
| 12/17 | 本章自测 | [12](../../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md#self-test) | 自测 |
| 13/01 | Checkpoint 不是“把聊天记录存一下” | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-01) | 保留并增补解释 |
| 13/02 | Checkpoint 应该发生在哪里 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-02) | 保留并增补解释 |
| 13/03 | Long-running Task 的状态机 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-03) | 保留并增补解释 |
| 13/04 | Resume 的第一步不是“继续调用模型” | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-04) | 保留并增补解释 |
| 13/05 | 最危险的问题：Tool 成功，但 Checkpoint 失败 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-05) | 保留并增补解释 |
| 13/06 | Idempotency 是第一道防线 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-06) | 保留并增补解释 |
| 13/07 | Side-effect Ledger | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-07) | 保留并增补解释 |
| 13/08 | Compensation 什么时候需要 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-08) | 保留并增补解释 |
| 13/09 | Pause / Resume 与 HITL | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-09) | 保留并增补解释 |
| 13/10 | Cancellation 与 Resume 的关系 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-10) | 保留并增补解释 |
| 13/11 | Resume 和 Fork 不一样 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-11) | 保留并增补解释 |
| 13/12 | Replay 是什么 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-12) | 保留并增补解释 |
| 13/13 | Worker Lease 与 Ownership | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-13) | 保留并增补解释 |
| 13/14 | Checkpoint Schema 一个示例 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#legacy-13-14) | 保留并增补解释 |
| 13/15 | HUMAN-A 信号 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#human-a) | HUMAN-A |
| 13/16 | 面试怎么答 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#interview) | 面试回答 |
| 13/17 | 高频易错点 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#pitfalls) | 易错辨析 |
| 13/18 | 本章自测 | [13](../../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md#self-test) | 自测 |
| 14/01 | 三层边界 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-01) | 保留并增补解释 |
| 14/02 | 为什么“全部弹确认框”不是好安全设计 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-02) | 保留并增补解释 |
| 14/03 | Risk Classification 可以看什么 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-03) | 保留并增补解释 |
| 14/04 | Permission Context 应该结构化 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-04) | 保留并增补解释 |
| 14/05 | Approval 为什么必须和 RunState 结合 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-05) | 保留并增补解释 |
| 14/06 | Approval Record 应保存什么 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-06) | 保留并增补解释 |
| 14/07 | Sandbox 解决的是另一层问题 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-07) | 保留并增补解释 |
| 14/08 | Filesystem Sandbox | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-08) | 保留并增补解释 |
| 14/09 | Network Sandbox | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-09) | 保留并增补解释 |
| 14/10 | Sandbox 不是“绝对安全” | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-10) | 保留并增补解释 |
| 14/11 | Permission 与 Prompt Injection 的关系 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-11) | 保留并增补解释 |
| 14/12 | Permission Failure Timeline | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#legacy-14-12) | 保留并增补解释 |
| 14/13 | HUMAN-A 信号 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#human-a) | HUMAN-A |
| 14/14 | 面试怎么答 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#interview) | 面试回答 |
| 14/15 | 高频易错点 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#pitfalls) | 易错辨析 |
| 14/16 | 本章自测 | [14](../../curriculum/09-curriculum/09-agent/docs/14-PermissionApprovalAndSandbox.md#self-test) | 自测 |
| 15/01 | Threat Model：先问“攻击者想让 Agent 做什么” | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-01) | 保留并增补解释 |
| 15/02 | Instruction 与 Data 必须在 Runtime 概念上分层 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-02) | 保留并增补解释 |
| 15/03 | Guardrail 应该分生命周期，而不是一个总开关 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-03) | 保留并增补解释 |
| 15/04 | Prompt Injection 为什么不能靠“检测一句恶意文本”解决 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-04) | 保留并增补解释 |
| 15/05 | Secret 不应该直接进入模型 Context | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-05) | 保留并增补解释 |
| 15/06 | Tool Capability 要最小化 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-06) | 保留并增补解释 |
| 15/07 | Containment：重点不是“永不犯错” | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-07) | 保留并增补解释 |
| 15/08 | Untrusted Tool Result 也可能继续攻击下一轮 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-08) | 保留并增补解释 |
| 15/09 | RAG / MCP 的 Injection Surface | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-09) | 保留并增补解释 |
| 15/10 | Memory Poisoning | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-10) | 保留并增补解释 |
| 15/11 | Output Leakage | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-11) | 保留并增补解释 |
| 15/12 | Security Incident Timeline | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-12) | 保留并增补解释 |
| 15/13 | HUMAN-A 信号 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#human-a) | HUMAN-A |
| 15/14 | Tier C 官方证据 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#legacy-15-14) | 保留到章内来源对照 |
| 15/15 | 面试怎么答 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#interview) | 面试回答 |
| 15/16 | 高频易错点 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#pitfalls) | 易错辨析 |
| 15/17 | 本章自测 | [15](../../curriculum/09-curriculum/09-agent/docs/15-InjectionAndContainment.md#self-test) | 自测 |
| 16/01 | 先给稳定边界 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-01) | 保留并增补解释 |
| 16/02 | 为什么 Tool 太多会出问题 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-02) | 保留并增补解释 |
| 16/03 | Capability Catalog | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-03) | 保留并增补解释 |
| 16/04 | Claude Code 源码侧的 Progressive Loading 证据 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-04) | 保留到章内来源对照 |
| 16/05 | MCP 解决什么标准化问题 | [16](../../curriculum/09-curriculum/09-agent/docs/16-MCPArchitectureAndLifecycle.md#legacy-16-05) | 完整协议章：MCP原标准化、三原语与传输边界移到完整协议章节 |
| 16/06 | Tool / Resource / Prompt 为什么要分开 | [16](../../curriculum/09-curriculum/09-agent/docs/16-MCPArchitectureAndLifecycle.md#legacy-16-06) | 完整协议章：MCP原标准化、三原语与传输边界移到完整协议章节 |
| 16/07 | Transport 不是 MCP 的核心价值 | [16](../../curriculum/09-curriculum/09-agent/docs/16-MCPArchitectureAndLifecycle.md#legacy-16-07) | 完整协议章：MCP原标准化、三原语与传输边界移到完整协议章节 |
| 16/08 | Skill 与 Tool 的区别 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-08) | 保留并增补解释 |
| 16/09 | Skill Progressive Disclosure | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-09) | 保留并增补解释 |
| 16/10 | Hook 是什么 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-10) | 保留并增补解释 |
| 16/11 | Codex Hooks 的实现证据 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-11) | 保留并增补解释 |
| 16/12 | Extension Failure 怎么处理 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-12) | 保留并增补解释 |
| 16/13 | Capability Versioning | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-13) | 保留并增补解释 |
| 16/14 | Security Boundary | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#legacy-16-14) | 保留并增补解释 |
| 16/15 | HUMAN-A 信号 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#human-a) | HUMAN-A |
| 16/16 | 面试怎么答 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#interview) | 面试回答 |
| 16/17 | 高频易错点 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#pitfalls) | 易错辨析 |
| 16/18 | 本章自测 | [17](../../curriculum/09-curriculum/09-agent/docs/17-SkillsHooksAndExtensions.md#self-test) | 自测 |
| 17/01 | Routing 至少有三层 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-01) | 保留并增补解释 |
| 17/02 | Intent Recognition 可以有多种实现 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-02) | 保留并增补解释 |
| 17/03 | Router 也需要 Evaluation | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-03) | 保留并增补解释 |
| 17/04 | Model Routing 的目标是什么 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-04) | 保留并增补解释 |
| 17/05 | Provider Adapter 为什么是 Runtime 能力 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-05) | 保留并增补解释 |
| 17/06 | Provider Adapter 应统一什么，不统一什么 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-06) | 保留并增补解释 |
| 17/07 | Claude Code 的实现信号 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-07) | 保留并增补解释 |
| 17/08 | Runtime Resilience 先做 Error Classification | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-08) | 保留并增补解释 |
| 17/09 | Retry Eligibility 为什么比 Retry Count 更重要 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-09) | 保留并增补解释 |
| 17/10 | Model Failover 会不会改变结果语义 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-10) | 保留并增补解释 |
| 17/11 | Circuit Breaker 在 Agent Runtime 中怎么用 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-11) | 保留并增补解释 |
| 17/12 | Fallback 不应该静默 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-12) | 保留并增补解释 |
| 17/13 | Routing Failure Timeline | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#legacy-17-13) | 保留并增补解释 |
| 17/14 | HUMAN-A 信号 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#human-a) | HUMAN-A |
| 17/15 | 面试怎么答 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#interview) | 面试回答 |
| 17/16 | 高频易错点 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#pitfalls) | 易错辨析 |
| 17/17 | 本章自测 | [18](../../curriculum/09-curriculum/09-agent/docs/18-RoutingAndProviderResilience.md#self-test) | 自测 |
| 18/01 | 什么时候真的值得 Multi-Agent | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-01) | 保留并增补解释 |
| 18/02 | Subagent as Tool | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-02) | 保留并增补解释 |
| 18/03 | Handoff 模式 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-03) | 保留并增补解释 |
| 18/04 | Manager / Worker 模式 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-04) | 保留并增补解释 |
| 18/05 | Task Ownership 必须显式 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-05) | 保留并增补解释 |
| 18/06 | Context Isolation 为什么很重要 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-06) | 保留并增补解释 |
| 18/07 | Claude Code `Task.ts` 提供的实现信号 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-07) | 保留并增补解释 |
| 18/08 | Workspace Concurrency 是 Coding Agent 的高风险点 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-08) | 保留并增补解释 |
| 18/09 | 共享 Workspace 的几种策略 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-09) | 保留并增补解释 |
| 18/10 | Shared State 也会 Race | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-10) | 保留并增补解释 |
| 18/11 | Multi-Agent Failure | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-11) | 保留并增补解释 |
| 18/12 | Budget Explosion | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-12) | 保留并增补解释 |
| 18/13 | Recursive Delegation / Deadlock | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-13) | 保留并增补解释 |
| 18/14 | A2A 解决什么 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-14) | 明确修正后讲解：保留A2A核心范围，补官方对象、消息/任务/产物往返及版本区别 |
| 18/15 | A2A 和内部 Subagent 有什么区别 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-15) | 明确修正后讲解：保留内部协作与异构系统互操作边界，不用MCP永无任务状态的错误绝对化说法 |
| 18/16 | Result Aggregation 不是“把所有答案拼起来” | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#legacy-18-16) | 保留并增补解释 |
| 18/17 | HUMAN-A 信号 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#human-a) | HUMAN-A |
| 18/18 | 面试怎么答 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#interview) | 面试回答 |
| 18/19 | 高频易错点 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#pitfalls) | 易错辨析 |
| 18/20 | 本章自测 | [19](../../curriculum/09-curriculum/09-agent/docs/19-MultiAgentAndA2A.md#self-test) | 自测 |
| 19/01 | Log、Metric、Trace 各解决什么 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-01) | 保留并增补解释 |
| 19/02 | Trace Identity | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-02) | 保留并增补解释 |
| 19/03 | 一个 Agent Span 应该记录什么 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-03) | 保留并增补解释 |
| 19/04 | Codex Rollout Trace 的源码证据 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-04) | 保留到章内来源对照 |
| 19/05 | OpenAI Agents SDK Tracing 给出的证据 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-05) | 保留并增补解释 |
| 19/06 | 为什么要记录“模型看到什么” | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-06) | 保留并增补解释 |
| 19/07 | Trace 与 Privacy 冲突 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-07) | 保留并增补解释 |
| 19/08 | Replay 有三种不同含义 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-08) | 保留并增补解释 |
| 19/09 | Trace 如何定位“Agent 卡住” | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-09) | 保留并增补解释 |
| 19/10 | Token / Cost 异常怎么定位 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-10) | 保留并增补解释 |
| 19/11 | Context Management 自己也需要 Observability | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-11) | 保留并增补解释 |
| 19/12 | Agent Trace Schema 示例 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-12) | 保留并增补解释 |
| 19/13 | Observability 不应该和 Evaluation 混为一谈 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#legacy-19-13) | 保留并增补解释 |
| 19/14 | HUMAN-A 信号 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#human-a) | HUMAN-A |
| 19/15 | 面试怎么答 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#interview) | 面试回答 |
| 19/16 | 高频易错点 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#pitfalls) | 易错辨析 |
| 19/17 | 本章自测 | [20](../../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md#self-test) | 自测 |
| 20/01 | 先分清 Agent Harness 和 Eval Harness | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-01) | 保留并增补解释 |
| 20/02 | 最终结果比“模型说完成了”更重要 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-02) | 保留并增补解释 |
| 20/03 | Eval 分四层 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-03) | 保留并增补解释 |
| 20/04 | Eval Dataset 从哪里来 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-04) | 保留并增补解释 |
| 20/05 | Dataset 要分层采样 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-05) | 保留并增补解释 |
| 20/06 | Ground Truth 不一定是一个字符串 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-06) | 保留并增补解释 |
| 20/07 | LLM Judge 什么时候适合 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-07) | 保留并增补解释 |
| 20/08 | Process Metric 为什么也重要 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-08) | 保留并增补解释 |
| 20/09 | Tool / Routing Eval | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-09) | 保留并增补解释 |
| 20/10 | Agent Eval 与 Trace 的关系 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-10) | 保留并增补解释 |
| 20/11 | Regression 为什么必须自动化 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-11) | 保留并增补解释 |
| 20/12 | SWE-bench 为什么是重要参考 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-12) | 保留并增补解释 |
| 20/13 | Benchmark Contamination / Overfitting | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-13) | 保留并增补解释 |
| 20/14 | Data Flywheel | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-14) | 保留并增补解释 |
| 20/15 | Online Validation | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-15) | 保留并增补解释 |
| 20/16 | Evaluation Failure Timeline | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#legacy-20-16) | 保留并增补解释 |
| 20/17 | HUMAN-A 信号 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#human-a) | HUMAN-A |
| 20/18 | 面试怎么答 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#interview) | 面试回答 |
| 20/19 | 高频易错点 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#pitfalls) | 易错辨析 |
| 20/20 | 本章自测 | [21](../../curriculum/09-curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md#self-test) | 自测 |
| 21/01 | Coding Agent 最大的问题不是生成，而是理解和验证 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-01) | 保留并增补解释 |
| 21/02 | Repository Understanding 不等于 Vector RAG | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-02) | 保留并增补解释 |
| 21/03 | Repo Understanding 的搜索漏斗 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-03) | 保留并增补解释 |
| 21/04 | Patch 应尽量小 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-04) | 保留并增补解释 |
| 21/05 | Workspace State 必须可控 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-05) | 保留并增补解释 |
| 21/06 | Patch Application 要有前置版本 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-06) | 保留并增补解释 |
| 21/07 | Test 是 Outcome Verification，不是装饰 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-07) | 保留并增补解释 |
| 21/08 | Test Failure 怎么处理 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-08) | 保留并增补解释 |
| 21/09 | Diff Review 是另一道防线 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-09) | 保留并增补解释 |
| 21/10 | Acceptance Criteria 必须独立于 Agent 自评 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-10) | 保留并增补解释 |
| 21/11 | Verification Pyramid | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-11) | 保留并增补解释 |
| 21/12 | Command Execution 的风险 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-12) | 保留并增补解释 |
| 21/13 | AI-assisted Development 中人的责任 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-13) | 保留并增补解释 |
| 21/14 | Rollback / Delivery | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-14) | 保留并增补解释 |
| 21/15 | Claude Code / Codex 为什么是重要实现参考 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-15) | 保留并增补解释 |
| 21/16 | Coding Agent Failure Timeline | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#legacy-21-16) | 保留并增补解释 |
| 21/17 | HUMAN-A 信号 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#human-a) | HUMAN-A |
| 21/18 | 面试怎么答 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#interview) | 面试回答 |
| 21/19 | 高频易错点 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#pitfalls) | 易错辨析 |
| 21/20 | 本章自测 | [22](../../curriculum/09-curriculum/09-agent/docs/22-CodingAgentDelivery.md#self-test) | 自测 |
| 22/01 | 先看一个单机 Demo | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-01) | 保留并增补解释 |
| 22/02 | 一个通用 Production Agent Runtime | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-02) | 保留并增补解释 |
| 22/03 | Brain / Hands / Durable Session 分离 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-03) | 保留并增补解释 |
| 22/04 | API / Streaming Gateway | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-04) | 保留并增补解释 |
| 22/05 | Harness Worker 应尽量可替换 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-05) | 保留并增补解释 |
| 22/06 | Scheduler / Queue 为什么重要 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-06) | 保留并增补解释 |
| 22/07 | Execution Sandbox Pool | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-07) | 保留并增补解释 |
| 22/08 | Tool Gateway | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-08) | 保留并增补解释 |
| 22/09 | Model Provider Gateway | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-09) | 保留并增补解释 |
| 22/10 | Durable Event / State Store | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-10) | 保留并增补解释 |
| 22/11 | 多租户隔离 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-11) | 保留并增补解释 |
| 22/12 | Long-running Agent 如何跨 Worker | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-12) | 保留并增补解释 |
| 22/13 | Streaming 和 Durable State 不要混 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-13) | 保留并增补解释 |
| 22/14 | Deployment / Scaling 的核心指标 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-14) | 保留并增补解释 |
| 22/15 | Cost Governance | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-15) | 保留并增补解释 |
| 22/16 | Failure Domain | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-16) | 保留并增补解释 |
| 22/17 | 一个 Production Failure Timeline | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-17) | 保留并增补解释 |
| 22/18 | Observability / Eval Plane | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-18) | 保留并增补解释 |
| 22/19 | Brain / Hands 分离不是唯一正确架构 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#legacy-22-19) | 保留并增补解释 |
| 22/20 | HUMAN-A 与 Tier C | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#human-a) | HUMAN-A |
| 22/21 | 面试怎么答 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#interview) | 面试回答 |
| 22/22 | 高频易错点 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#pitfalls) | 易错辨析 |
| 22/23 | 本章自测 | [23](../../curriculum/09-curriculum/09-agent/docs/23-ProductionRuntime.md#self-test) | 自测 |
| 23/01 | 先写自己的 Requirement Matrix | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-01) | 保留并增补解释 |
| 23/02 | Framework 提供的价值通常是什么 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-02) | 保留并增补解释 |
| 23/03 | OpenAI Agents SDK 怎样映射 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-03) | 明确修正后讲解：用官方Agent/Runner/Session/RunState/Handoff核心语义替代模糊框架标签 |
| 23/04 | LangGraph 适合解决什么类型问题 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-04) | 明确修正后讲解：用官方StateGraph/Reducer/Checkpointer/Store/interrupt说明图执行与恢复 |
| 23/05 | LangChain 适合什么 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-05) | 明确修正后讲解：按官方create_agent与LangGraph关系更新，不沿用过时线性Chain概括 |
| 23/06 | 什么时候自研 Runtime | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-06) | 保留并增补解释 |
| 23/07 | Build-vs-Buy Matrix | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-07) | 保留并增补解释 |
| 23/08 | Framework Selection 的错误方法 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-08) | 保留并增补解释 |
| 23/09 | Framework Evaluation 应该用真实 Workload | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-09) | 保留并增补解释 |
| 23/10 | Escape Hatch 很重要 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-10) | 保留并增补解释 |
| 23/11 | Framework Upgrade 风险 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-11) | 保留并增补解释 |
| 23/12 | 自研最小 Runtime 到底需要什么 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-12) | 保留并增补解释 |
| 23/13 | Anthropic `Building effective agents` 的重要启发 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-13) | 保留到章内来源对照 |
| 23/14 | Framework 不会替你解决业务正确性 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-14) | 保留并增补解释 |
| 23/15 | HUMAN-A 信号 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#human-a) | HUMAN-A |
| 23/16 | 一个选型回答模板 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#interview) | 面试回答 |
| 23/17 | Framework Migration | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#legacy-23-17) | 保留并增补解释 |
| 23/18 | 面试怎么答 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#interview) | 面试回答 |
| 23/19 | 高频易错点 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#pitfalls) | 易错辨析 |
| 23/20 | 本章自测 | [24](../../curriculum/09-curriculum/09-agent/docs/24-FrameworkSelection.md#self-test) | 自测 |

</details>

## 5. 训练与检查范围

当前24章共130个章内问答、210个自测、224条易错辨析。集中56题保留，44道Agent研究能力不变。题数不证明读者已经理解。

运行`python tools/validate_agent_readability.py --run-examples`检查编号、四种章末结构、旧小节去向、44题覆盖、代码围栏、普通本地链接以及标记教学例子。源码对照使用原固定提交，MCP/A2A和框架按注明官方版本；教学补充不是新面经。

机械通过不等于所有外部URL/渲染器都验证，也不是模型、真实工具或生产数据库故障实验。只有实际执行的教学断言可声称通过。人工逐节对照和读者理解仍是不同质量维度，不能用大文件或旧PASS替代。

## 6. 发布与恢复

本轮发布目标是main，正式入口`curriculum/09-agent/README.md`，全库185篇。原版备份`backup/agent-original-main-37cbfd2`及修订前备份`backup/agent-before-style-repair-83a3b96`保留。可仅恢复Agent及其必要导航，不需强制回退整仓库或新研究数据。16章架构分支不在本轮修改范围。
