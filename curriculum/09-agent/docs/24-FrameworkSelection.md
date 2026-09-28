# 24. 框架选型：先问要保证什么，再看谁能实现

[← 上一章](23-ProductionRuntime.md) · [Agent 目录](../README.md) · [综合复习 →](../review/README.md)

一个助手只有两个只读工具，另一个要等待用户批准、跨重启继续并协调多个子任务。它们都叫 Agent，却未必需要同一套框架结构。

学到这里，已经可以用循环、状态、工具、恢复与验收解释需求。现在比较框架，是看它怎样承担这些责任，而不是把 API 名字反过来当知识体系。

<a id="1-先写自己的-requirement-matrix"></a>
<a id="12-自研最小-runtime-到底需要什么"></a>
<a id="legacy-23-01"></a>
<a id="legacy-23-12"></a>
<a id="section-1"></a>
<a id="section-12"></a>
<a id="core-1"></a>

## 1. 把需求写成能验证的问题

先明确哪些是当前必需、哪些已有实现、哪些希望交给框架。例如：

| 需求 | 要验证什么 | 不足够的表述 |
|---|---|---|
| 工具调用 | 参数校验、结果关联、错误处理 | 支持 tools |
| 等待批准 | 保存哪次动作，怎样恢复和复核 | 支持 HITL |
| 跨重启继续 | 从哪里重做，外部动作怎样避免重复 | 支持 checkpoint |
| 多用户 | 状态、凭证与产物怎样隔离 | 支持 session |
| 未来迁移 | 能否导出状态并替换关键执行策略 | 扩展性很好 |

简单只读循环不必为了假想需求先建设全部组件。但当前必须的权限和验收，不能因为选了轻量实现就省略。

<a id="3-openai-agents-sdk-怎样映射"></a>
<a id="legacy-23-03"></a>
<a id="section-3"></a>
<a id="core-2"></a>

## 2. Agents SDK：配置 Agent，由 Runner 推进

在 OpenAI Agents SDK 中，Agent 主要配置指令、模型、工具、交接与输出要求；Runner 推进模型、工具和角色交接的循环。函数包装可以帮助生成工具说明，业务权限和幂等仍由应用明确。[Running agents](https://openai.github.io/openai-agents-python/running_agents/)说明实际运行流程。

**Session**管理跨运行的会话项；**RunState**承载中断运行所需状态，可以参与批准后继续。它们目的不同，不应从“用了 SQLiteSession”直接推导任意外部动作恰好一次。[Sessions](https://openai.github.io/openai-agents-python/sessions/)和[HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/)应分别核对。

SDK 还可能提供沙箱、更多集成和持久执行适配；具体能力按所安装版本和官方文档确认。这里讲的是核心对象职责，不把一份简表当成产品功能上限。

<a id="4-langgraph-适合解决什么类型问题"></a>
<a id="legacy-23-04"></a>
<a id="section-4"></a>
<a id="core-3"></a>

## 3. LangGraph：显式描述状态怎样流过步骤

LangGraph 用 **StateGraph（状态图）**描述 Node（节点）和 Edge（边）。节点读取状态并返回更新，边决定后续位置；**Reducer（合并规则）**规定并行或多次更新怎样组合。节点可以是普通程序、模型或工具，不是每个节点都必须是 Agent。

**Checkpointer**按图执行边界保存状态，通常由 thread_id 关联；**Store**可保存跨线程复用的数据，例如用户偏好。把偏好存进去，不代表模型自动知道，节点仍要读取并编排。

`interrupt()`暂停等待外部输入，恢复时可能从节点开头执行，而不是回到任意程序行。中断前发生的副作用仍要幂等或可核对。并行阶段还要按官方持久化语义理解已完成写入与失败部分的恢复。[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)与[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)是这类选择的重要核对入口。

<a id="5-langchain-适合什么"></a>
<a id="legacy-23-05"></a>
<a id="section-5"></a>
<a id="core-4"></a>

## 4. LangChain 高层 Agent 与底层图不是简单竞争关系

当前官方 `create_agent` 提供基于 LangGraph 的高层 Agent 入口，组合模型、工具、中间件和结构化输出等能力。[LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)说明了这层关系。

常见任务可以从高层入口开始，需要更细的状态、分支和恢复控制时，再判断底层图能力是否适合。不能沿用“LangChain 永远只是线性 Chain”的旧概括，也不能认为高层集成自动满足全部业务一致性。

框架 API 变化较快。对真实项目应记录安装版本与关键行为，不把最新网站说明与旧版本代码混用；本章不提供未经对应版本运行的完整 SDK 程序。

<a id="2-framework-提供的价值通常是什么"></a>
<a id="6-什么时候自研-runtime"></a>
<a id="7-build-vs-buy-matrix"></a>
<a id="legacy-23-02"></a>
<a id="legacy-23-06"></a>
<a id="legacy-23-07"></a>
<a id="section-2"></a>
<a id="section-6"></a>
<a id="section-7"></a>
<a id="core-5"></a>

## 5. 自研是承担责任，不是天然更专业

范围很小的只读循环，自己实现可能最容易理解；已有平台也可能只需自研特殊的控制或安全边界，同时复用模型 SDK、存储和协议组件。

但自研复杂恢复、隔离或协作，意味着测试和维护这些保证也由团队承担。不能因为要求严格，就自动断言自研一定优于成熟框架。

| 比较维度 | 应看什么 |
|---|---|
| 抽象匹配 | 任务更像工具循环，还是显式状态图与中断流程 |
| 实现成本 | 已提供多少真正适用的能力，剩余工作是什么 |
| 控制与诊断 | 能否查看实际请求、状态与失败，替换必要策略 |
| 恢复语义 | 重启、部分成功、批准恢复究竟从哪里继续 |
| 维护与迁移 | 升级兼容、数据导出、生态依赖和团队能力 |

框架减少通用工作，也会引入默认行为与升级成本；自研提高控制空间，也会增加可靠性责任。常见选择是组合，而不是二选一的价值判断。

<a id="10-escape-hatch-很重要"></a>
<a id="13-framework-不会替你解决业务正确性"></a>
<a id="8-framework-selection-的错误方法"></a>
<a id="81-只看-star"></a>
<a id="82-只看-demo"></a>
<a id="83-只看-feature-checklist"></a>
<a id="9-framework-evaluation-应该用真实-workload"></a>
<a id="legacy-23-08"></a>
<a id="legacy-23-09"></a>
<a id="legacy-23-10"></a>
<a id="legacy-23-14"></a>
<a id="section-10"></a>
<a id="section-13"></a>
<a id="section-8"></a>
<a id="section-9"></a>
<a id="core-6"></a>

## 6. 用同一任务和故障窗口做小范围验证

不要只数功能清单。对候选实现使用相同的正常任务，以及参数错误、等待批准、恢复、取消和外部成功但回执丢失等条件。

观察调用是否正确关联、批准对象是否变化、节点是否重跑、旧 Worker 是否仍能写入，以及能否导出恢复需要的状态。模型切换还要核对工具、输入模态和消息兼容。

**Escape hatch（接管或扩展入口）**指关键路径不符合需求时，应用能否替换执行器、重试、状态存储、权限或观测，而不是被迫绕过整个框架。不是每项能力都必须手写，但要知道真正需要接管时有没有可靠路径。

只有正常演示通过，不能宣称恢复和生产选型完成。未验证条件应写进决策记录，避免把“官方支持”当成本应用已验证。

<a id="11-framework-upgrade-风险"></a>
<a id="14-framework-migration"></a>
<a id="legacy-23-11"></a>
<a id="legacy-23-17"></a>
<a id="section-11"></a>
<a id="section-14"></a>
<a id="core-7"></a>

## 7. 升级与迁移，保持业务知识独立

尽量让业务状态、工具契约、验收用例与必要产物格式不完全绑死内部类。升级时检查消息序列化、检查点格式、节点恢复、供应商适配和权限行为；对尚在运行的旧任务明确兼容策略。

迁移编排器未必需要重写全部业务工具和测试。如果没有独立验收标准，换框架后就无法判断是实现改变还是业务要求丢失。

Codex、Claude Code 是具体产品实现参考，不应与 SDK 和自研循环混成“谁更高级”的榜单。读产品源码用于理解真实组合与边界，不能把使用其名字当成获得相同生产保证。

<a id="summary"></a>

## 本章小结

框架选型从可验证需求开始。理解 Runner、Session、状态图、检查点与 Store 各自语义，再比较实现、恢复、维护和迁移成本。官方功能存在与本应用已经通过验证，是两件事。

<a id="17-面试怎么答"></a>
<a id="qagents-sdklanggraphlangchain与自研怎么选"></a>
<a id="qlangchain--langgraph--自研怎么选"></a>
<a id="qlanggraph-interrupt恢复为什么还要考虑副作用"></a>
<a id="qsessioncheckpointer和store是一回事吗"></a>
<a id="q怎样完整说明框架选型的理由"></a>
<a id="q怎样避免未来被框架绑定"></a>
<a id="interview"></a>

## 🎯 面试怎么回答

### Agents SDK、LangGraph、LangChain 和自研怎样选择？

先明确控制流、状态、工具、人工参与和恢复需求。Agents SDK 提供 Agent 与 Runner 等执行抽象；LangGraph 显式管理状态图；LangChain 提供基于它的高层集成。自研适合小范围或特殊控制，但要承担可靠性。用相同任务与故障条件验证，而不是按热度排序。

### Session、Checkpointer 和 Store 是一回事吗？

不是。Session 主要管理会话项，Checkpointer 保存规定边界的执行状态，Store 可以支持跨线程数据。具体以框架定义为准，三者都不自动证明外部副作用恰好一次。

### 框架为什么不能替代业务正确性？

框架提供执行机制，但任务怎样算完成、当前用户能做什么、外部结果未知怎样核对，需要业务契约。检查点和重试开关不能替代这些判断。

<a id="18-高频易错点"></a>
<a id="pitfalls"></a>

## ⚠️ 易错点

> ⚠️ 支持恢复的功能名相同，不代表恢复单位、重复执行和状态格式相同。

> ⚠️ 自研不等于从零写所有基础设施，也不代表天然更安全可靠。

> ⚠️ 当前官方文档和本地旧 SDK 可能不同，发布前要验证实际安装版本。

<a id="19-本章自测"></a>
<a id="self-test"></a>

## 本章自测

<details><summary>1. 两个只读工具的短任务，必须先建立复杂状态图吗？</summary>

不必须。简单循环满足控制与故障承诺时可以保持轻量，不能仅因框架提供图就制造需求。

</details>

<details><summary>2. LangGraph 节点恢复会从开头运行，为什么中断前发送邮件需要特别处理？</summary>

那段代码可能再次执行。检查点不是任意指令快照，也不回滚外部邮件，需幂等、独立动作边界或可靠核对。

</details>

<details><summary>3. 框架表里都写支持 Memory，应进一步比较什么？</summary>

保存和读取时机、范围、更新纠错、删除与上下文注入责任，以及哪些由应用实现；不能只比较同一个功能词。

</details>

<details><summary>4. 未来更换框架，什么资产最应该保留独立？</summary>

业务状态与工具契约、验收用例和必要产物表示。它们帮助核对迁移后的行为，而不必跟随内部类全部重写。

</details>

<a id="15-产品实现与官方资料对照按需展开"></a>
<a id="16-human-a-信号"></a>
<a id="24-framework-mapping按核心语义比较框架与自研"></a>
<a id="human-a"></a>
<a id="legacy-23-13"></a>
<a id="section-15"></a>
<a id="references"></a>

## 知识回看与权威资料

- [Agents SDK running](https://openai.github.io/openai-agents-python/running_agents/)与[Sessions](https://openai.github.io/openai-agents-python/sessions/)：分别核对循环和会话项管理。
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)与[interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)：核对状态保存和节点重跑。
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)：核对高层入口与图运行基础。
- [综合复习](../review/README.md)：脱离框架名称，重新推导控制、状态、执行和验收责任。


---

[← 上一章](23-ProductionRuntime.md) · [Agent 目录](../README.md) · [综合复习 →](../review/README.md)
