# Agent｜从任务契约到生产级 Agent 系统

[← RAG](../rag/README.md) · [↑ Handbook](../README.md) · [学习路线](../roadmap/learning-path.md) · [System Design →](../system-design/README.md)

> **状态：分层增强版｜教学与训练补强完成** · **16 章连续主线** · **44 道 ACTIVE Canonical**
>
> 主线从任务设计开始，沿四层职责展开，再以安全、质量和生产演进收口。Harness 是运行层中的执行系统，不再代指整个 Agent 模块。

## 1. 这个模块解决什么

从任务契约与自主权出发，沿应用、运行、接入、资源四层组织 Agent，并贯通安全、质量与生产演进。

学习完成后，应该能从任务推导必要能力，解释每项机制的位置、输入输出、失败和验证，并把它们组合成可交付系统，而不是只会解释单个名词。

## 2. 在十板块中的位置

Python → FastAPI → AI Backend Engineering → MySQL / Redis / Vector DB → LLM Foundation → RAG → **Agent** → System Design。

本模块提供 Agent 专属的系统认知与执行机制。通用网络、数据库、事务、队列和容量算法回到对应基础模块；System Design 继续负责跨领域组合与完整场景训练。

## 3. 固定课程原则

**先目标，后职责；先整体，后机制；先单个执行单元，后协作；先逻辑边界，后部署选型。** 真人面经只校准复习权重、真实问法与追问深度，不打乱第一次学习顺序。

业务场景是设计输入，不是软件模块；四层是逻辑职责，不是四个微服务；层、模块、机制、对象、协议和资源是不同类型。这里的架构 L1–L4 与研究题库的 Depth L1–L4 无关。

## 4. 唯一正式学习主线

```text
设计输入：业务场景
    ↓
任务契约：为谁做什么、允许做什么、怎样算完成
    ↓
能力与自主权：哪些交给模型判断，哪些必须由程序控制
    ↓
L1 应用层：任务入口、业务流程、用户交互、结果交付、人工接管
    ↓ 使用
L2 运行层：执行循环、上下文、记忆策略、执行状态、调度与恢复
    ↓ 通过稳定接口使用
L3 接入层：模型适配、工具接口、检索接口、状态与记忆存取接口
    ↓ 连接
L4 资源层：模型服务、知识与数据库、外部系统、文件与执行环境

贯穿四层：安全治理（身份、权限、审批、隔离、审计）
贯穿四层：质量运营（观测、评测、成本、可靠性、持续改进）
```

第一遍按下面01→16阅读，不需要另读总纲或项目案例。前两章用同一个通用文件报告推导契约与控制权；后续先解释黑盒输入输出，再逐步展开实现。长章有分段提示，代码/源码对照用于核验机制，不构成第二条课程。

## 5. 正式课程目录

### 起点｜任务与控制权

1. [Agent 系统与任务契约](docs/01-AgentSystemAndTaskContract.md)
2. [能力设计与自主权分配](docs/02-CapabilityAndAutonomy.md)

### L1｜应用如何承接和交付任务

3. [L1 应用层：任务、流程与用户交互](docs/03-ApplicationAndInteraction.md)

### L2｜运行时怎样持续推进任务

4. [L2 运行层：执行循环与控制](docs/04-AgentLoopAndControl.md)
5. [L2 运行层：上下文组装、预算与压缩](docs/05-ContextEngineering.md)
6. [L2 运行层：记忆的选择、使用与维护](docs/06-MemoryLifecycle.md)
7. [L2 运行层：执行状态、持久化与恢复](docs/07-StateAndRecovery.md)
8. [L2 运行层：多 Agent 协作与调度](docs/08-MultiAgentCoordination.md)

### L3｜外部能力怎样被稳定接入

9. [L3 接入层：模型适配、路由与容错](docs/09-ModelAccessAndRouting.md)
10. [L3 接入层：工具契约、注册与发现](docs/10-ToolContractAndDiscovery.md)
11. [L3 接入层：工具执行、副作用与取消](docs/11-ToolExecutionAndEffects.md)
12. [L3 接入层：知识、记忆与扩展能力接入](docs/12-KnowledgeAndCapabilityAccess.md)

### L4｜真实能力、事实与行动在哪里

13. [L4 资源层：模型、数据与执行环境](docs/13-ResourcesAndEnvironments.md)

### 横切治理｜安全与质量贯穿四层

14. [横切治理：身份、权限、审批与安全](docs/14-IdentityPermissionsAndSafety.md)
15. [横切治理：观测、评测与持续改进](docs/15-ObservabilityAndEvaluation.md)

### 系统收口｜从逻辑架构到工程实现

16. [系统收口：部署、成本、选型与演进](docs/16-ProductionArchitectureAndEvolution.md)

## 6. 真人面经怎样影响本模块

44 道 ACTIVE Canonical 和原有 Source Count 不因改名、合并章节或增加架构解释而变化。研究文件 `research/questions/agent-harness.md` 保留兼容标识，展示模块名统一为 Agent。

[真实问法与来源](../research/questions/agent-harness.md)只用来校准复习权重、问法与追问深度；本模块的完整设计责任不由面试频率决定。

## 7. 模块边界

RAG 负责证据获取与回答质量的完整工程链；这里讲何时需要信息、如何接入、如何进入执行。LLM Foundation 负责模型内部原理；这里讲模型在系统中的角色和调用契约。Backend Engineering 负责通用可靠性机制；这里讲 Run、Tool、Checkpoint 和副作用特有的执行语义。

<a id="concept-map"></a>

<details>
<summary>查找某个概念：按主责回到正式章节（不是第二条学习路线）</summary>

| 要查的内容 | 主责 / 章节 |
|---|---|
| Agent、Harness、层/模块/机制、任务契约 | 01–02 |
| 任务入口、业务编排、用户确认、人工接管、意图路由 | 03 |
| Thread / Turn / Item、Loop、Planning、ReAct、Stop、Budget、Steering | 04 |
| Prompt / Context、Compaction、Cache、Offloading | 05 |
| Memory、Write Policy、Consolidation、失效与纠错 | 06 |
| State、History、Checkpoint、Resume、Fork、Replay、幂等与动作核对 | 07 |
| Multi-Agent、Subagent、Handoff、A2A、共享工作区 | 08 |
| Model Routing、Provider Adapter、Failover | 09 |
| Tool Schema、Registry、Router、Discovery、版本 | 10 |
| Tool Execution、错误、副作用、并发、Cancel、Progress | 11 |
| RAG 接入、状态/记忆接口、MCP、Skills、Hooks、资源搜索 | 12 |
| 模型服务、数据库、文件、执行环境、Sandbox、Artifact | 13 |
| Auth、Permission、Approval、Guardrails、Injection、Secrets | 14 |
| Trace、Metrics、Replay、Evals、Benchmark、Data Flywheel | 15 |
| Deployment、Queue、Cost、Framework、Build-vs-Buy、代码验证 | 16 |

跨层能力按职责拆开，例如 Memory 的策略在06，存取接口在12，存储资源在13；不要把同一个词硬塞进唯一一层。

</details>

## 8. 复习、面试与资料入口

[复习与综合自测](review/README.md) · [面试训练](interview/README.md) · [官方资料](../roadmap/agent-authoritative-sources.md) · [源码索引](../research/agent-sources/README.md)。复习和面试页不复制正式教材：Review提供16章回忆检查与6个综合失败推演；Interview按同一主线保留main的56个细粒度练习，新增8个系统推导题，并在同一页提供86个易错辨析与速查。练习数量不等于真人Canonical数量。

## 9. 推荐学习方式

可按个人节奏学习，不绑定Week/Session。第一次沿01→16建立因果链。每章结束，能说明当前责任、输入输出、至少一个失败窗口和验证方式，再进入下一章。第二遍用复习页闭卷重建同一张图，第三遍再用真实问题练习口述与追问。

## 10. 完成状态与下一环

正文16章连续；复习与面试各一个入口。每章含阅读提示、至少4个折叠自测；第04章提供无网络、无真实副作用的最小循环练习。旧23章迁移关系、课程计数和本次检查记录维护在既有[粒度记录](../roadmap/curriculum-granularity-audit.md)与[质量记录](../roadmap/final-quality-audit.md)，不另开学习文档。

下一环：[System Design](../system-design/README.md)。
