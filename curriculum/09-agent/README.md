# Agent｜从任务到可验证的执行

[← RAG](../08-rag/README.md) · [Handbook](../../README.md) · [学习路线](../../guide/learning-path.md) · [System Design →](../10-system-design/README.md)

模型可以提出下一步，但程序必须把允许的动作做出来，把结果带回来，并判断任务是否真的完成。本模块沿这一条反馈主线，学习工具、上下文、记忆、状态、安全、恢复和评测。

适合已经理解模型基本输入输出、接口与权限、数据库和缓存基本用途的学习者。进入时不要求掌握 Agent 框架；概念不绑定某种编程语言，两段 Python 标准库例子只是可选的可观察实验。

## 学习主线

```text
任务与自主权 → 反馈循环 → 工具说明、发现与执行
→ 计划和模型输入 → 记忆、状态与恢复
→ 权限、协议与扩展 → 协作 → 诊断、评测与交付
```

## 正式章节

### A｜先走通一项任务

| 章 | 要理解的问题 |
|---:|---|
| 01 | [Agent 系统的全貌：模型之外，谁把任务做完](docs/01-AgentSystemAndResponsibilities.md) |
| 02 | [Workflow 与 Agent：哪些决定交给模型](docs/02-WorkflowAutonomyAndRuntimeBoundary.md) |
| 03 | [Agent Loop：观察怎样改变下一步](docs/03-AgentLoopAndExecutionScopes.md) |

### B｜把工具调用变成受控执行

| 章 | 要理解的问题 |
|---:|---|
| 04 | [工具契约：模型提出什么，程序检查什么](docs/04-ToolContractAndValidation.md) |
| 05 | [工具注册与发现：程序有的，不一定都给模型看](docs/05-ToolRegistrationAndDiscovery.md) |
| 06 | [工具结果与失败：谁来修，怎样继续](docs/06-ToolExecutionAndFailure.md) |
| 07 | [工具并发与取消：快一点，不等于可以乱序](docs/07-ToolConcurrencyAndCancellation.md) |

### C｜选择下一步及模型所需信息

| 章 | 要理解的问题 |
|---:|---|
| 08 | [计划与停止：让每一步朝目标推进](docs/08-PlanningGoalAndControl.md) |
| 09 | [上下文编排：模型这一刻到底收到什么](docs/09-ContextAssemblyAndCache.md) |
| 10 | [上下文压缩：缩短输入以后，怎样继续做对](docs/10-CompactionAndContinuation.md) |
| 11 | [记忆：把有用经验带到以后，也能纠错和忘记](docs/11-MemoryLifecycle.md) |

### D｜保存与恢复工作

| 章 | 要理解的问题 |
|---:|---|
| 12 | [状态与持久化：程序怎样知道工作做到哪里](docs/12-StateHistoryAndPersistence.md) |
| 13 | [检查点与恢复：保存之后、崩溃之前发生了什么](docs/13-CheckpointResumeAndRecovery.md) |

### E｜安全接入与协作

| 章 | 要理解的问题 |
|---:|---|
| 14 | [权限、批准与沙箱：一次动作要过几道不同的门](docs/14-PermissionApprovalAndSandbox.md) |
| 15 | [提示注入与信息保护：资料为什么不能变成命令](docs/15-InjectionAndContainment.md) |
| 16 | [MCP：从 Host / Client / Server 到完整协议往返](docs/16-MCPArchitectureAndLifecycle.md) |
| 17 | [Skills、Hooks 与 Plugins：知识怎样加载，规则怎样触发](docs/17-SkillsHooksAndExtensions.md) |
| 18 | [路由与模型适配：换一条路径，不能丢掉任务保证](docs/18-RoutingAndProviderResilience.md) |
| 19 | [多 Agent 协作：交出去的是任务，不是全部控制权](docs/19-MultiAgentAndA2A.md) |

### F｜验证、交付与实现选择

| 章 | 要理解的问题 |
|---:|---|
| 20 | [执行追踪：先定位卡在哪，再取需要的证据](docs/20-TraceReplayAndDiagnosis.md) |
| 21 | [Agent 评测：怎样证明修改真的更好](docs/21-EvaluationBenchmarkAndImprovement.md) |
| 22 | [Coding Agent：从理解仓库到交付可验证修改](docs/22-CodingAgentDelivery.md) |
| 23 | [生产运行：从任务承诺推导部署，而不是先画微服务](docs/23-ProductionRuntime.md) |
| 24 | [框架选型：先问要保证什么，再看谁能实现](docs/24-FrameworkSelection.md) |

## 怎样学习与回看

第一遍沿主线理解每个动作及结果，用章末自测检查能否推导。第二遍用 Review 重建关系，再用集中问题训练口述；产品源码用于对照真实实现，不作为首次理解的隐藏前提。

| 入口 | 用途 |
|---|---|
| [综合复习](review/README.md) | 用任务和失败重建机制关系 |
| [面试表达](interview/高频面试题.md) | 逐题练习判断、原因和边界 |
| [易错点](interview/面试易错点.md) | 从各章同一来源回顾误区 |
| [回顾卡](interview/面试前速查表.md) | 临时唤醒已学知识 |
| [Agent Products](../../products/agent/README.md) | 进入固定源码中的完整系统 |
| [技术资料](../../references/agent/README.md) | 核对版本与事实，选择实现选读 |

## 模块边界

模型生成机制由 LLM Foundation 讲解，检索证据质量由 RAG 讲解；Agent 负责它们如何参与反馈执行。通用事务、队列与幂等机制在 Backend 维护，本模块解释模型与工具执行带来的状态、恢复和授权边界。需要的最小前提仍在使用处说明。

MCP 采用明确的 2026-07-28 学习基线并对照旧版生命周期，A2A 对照 1.0.0 发布规范。框架网站、安装版本和产品源码快照分别核对；不因存在配置项就保证所有环境行为相同。

<a id="1-这个模块解决什么"></a>
<a id="10-教材状态"></a>
<a id="2-在十板块中的位置"></a>
<a id="3-固定课程原则"></a>
<a id="4-正式学习主线"></a>
<a id="5-正式课程目录"></a>
<a id="6-真人面经怎样影响本模块"></a>
<a id="7-模块边界"></a>
<a id="8-reviewinterviewproducts-与证据入口"></a>
<a id="9-推荐学习方式"></a>
<a id="agent从任务到可解释可验证的执行系统"></a>
<a id="a先认识任务与执行系统"></a>
<a id="b工具调用怎样受控完成"></a>
<a id="c控制方向与模型可见信息"></a>
<a id="d执行状态与跨中断恢复"></a>
<a id="e安全能力接入与协作"></a>
<a id="f诊断评测与工程落地"></a>

## 维护与验证依据

本模块包含 24 篇正文。可运行小例子只验证本地反馈与工具映射，不代表已运行真实模型、网络工具或生产恢复实验。

[精修范围与验证记录](../../guide/project/agent-clarity-refinement-2026-09-28.md)说明基线、保留迁移与实际检查；[证据及兼容映射](../../guide/project/agent-clarity-mapping-2026-09-28.json)用于持续维护，不在正文重复来源统计。

维护生成配套时运行 `python tools/sync_agent_materials.py --check`；结构、内部引用和两个本地例子通过 `python tools/validate_agent_readability.py --run-examples` 检查。自动检查不代替读者验收。
