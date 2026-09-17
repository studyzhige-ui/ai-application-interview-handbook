# Agent Harness / Runtime｜Review 与综合自测

[← 模块主页](../README.md) · [Handbook](../../README.md) · [可选学习路线](../../roadmap/learning-path.md) · [面试训练](../interview/高频面试题.md)

本页用于第二遍闭卷重建。先尝试画出过程再展开图和答案；学习节奏自行安排。每章自己的“面试怎么答、易错点、自测”仍完整保留，本页不替代它们。

## 1. 七张局部图：不是七套架构

<details>
<summary>执行循环</summary>

```text
目标与约束 → 当前输入 → 模型候选
                         ├─ 工具 → 校验/授权 → 执行 → 观察 → 继续
                         ├─ 缺输入 → 等待
                         └─ 完成候选 → 核验 → 成功或返回缺口
```

</details>

<details>
<summary>上下文与程序状态</summary>

```text
程序当前状态/资料/历史/记忆
           ↓ 选择本次需要的信息
模型请求：指令 + 工具说明 + 消息视图
           ↓ 新调用/观察通常追加
超限时选择/外部化/压缩，不把全部持久记录每次发送
```

</details>

<details>
<summary>关键动作与检查点</summary>

```text
检查点C1 → 保存必要操作意图op7 → 外部执行
          → 确认回执 → 检查点C2
中间崩溃 → 从C1及操作记录核对op7 → 安全继续或保留未知
```

</details>

<details>
<summary>工具门的不同责任</summary>

```text
参数形状 → 业务含义 → 身份/权限 → 必要批准 → 受限执行环境
 格式对      含义对     允许做       这次同意     实际可触及范围
不是检查一次JSON就得到全部保证
```

</details>

<details>
<summary>能力发现</summary>

```text
完整目录（处理器/连接/宿主元数据）
         ↓ 任务和权限筛选，必要时渐进搜索
模型可见说明（名称/用途/参数）
         ↓ 模型候选
路由到真实实现，不下载源码到模型
```

</details>

<details>
<summary>协作</summary>

```text
父级目标 → 子目标/授权范围/输入引用
         → 子Agent的局部上下文与受限动作
         → 结果与证据 → 父级验收
控制权交接与作为工具返回不同；工作区隔离另处理
```

</details>

<details>
<summary>恢复数据与诊断数据</summary>

```text
可靠状态/操作回执 → 用于继续或停止执行
产物与证据       → 用于交付和核验
有限Trace/指标   → 用于定位阶段与异常
受权调试快照     → 用于特定深查，可采样/脱敏/过期
用必要ID关联，不是每个事件复制全部输入
```

</details>

## 2. 逐章回忆

### 01｜Agent 系统的全貌：先知道谁在做什么

<details>
<summary>三份文件已全在输入里，必须循环吗？</summary>

不必须。若一次生成与校验已满足要求，固定流程更容易测试。只有读取选择或后续动作确实取决于中间观察时，才有理由比较动态循环。

回到[本章正文与完整自测](../docs/01-AgentHarness在AI应用中的职责.md)。

</details>

### 02｜Workflow、Agent 与 Harness 的边界

<details>
<summary>审批流程里有20个步骤，它必然是 Agent 吗？</summary>

不是。20步都预先编排依然是工作流。关键在于是否把某段下一步选择交给模型，以及这种选择是否依据中间观察。

回到[本章正文与完整自测](../docs/02-AgentWorkflowHarnessBoundary.md)。

</details>

### 03｜Agent 循环、执行层级与新消息

<details>
<summary>一次 Codex Turn 可否读取文件三次？</summary>

可以。Turn 包含用户请求后的一段 Agent 工作，模型可多次请求工具。每个工具项目及其事件有各自身份；不能把三次调用解释成必然三个 Codex Turn。

回到[本章正文与完整自测](../docs/03-AgentLoopRuntimeState.md)。

</details>

### 04｜工具契约：模型可以请求什么，程序必须检查什么

<details>
<summary>ID类型正确但不存在，属于哪类问题？</summary>

主要属于语义或业务有效性问题，而非JSON结构错误。应返回“对象不存在/不可访问”等合适信息，并避免向无权用户泄露对象是否存在。

回到[本章正文与完整自测](../docs/04-ToolContractSchemaValidation.md)。

</details>

### 05｜工具注册、模型可见说明与按需发现

<details>
<summary>示例里handler为何不出现在visible_specs？</summary>

函数对象不是模型API需要的JSON说明，真实代码在宿主执行。显式挑字段让边界清晰，也避免把内部配置和敏感信息误序列化。

回到[本章正文与完整自测](../docs/05-ToolRegistryRouterDiscovery.md)。

</details>

### 06｜工具结果与错误：哪些告诉模型，哪些由程序处理

<details>
<summary>参数缺失和HTTP临时断连，为什么处理不同？</summary>

缺参需要改变候选；临时断连可能重试原请求。把缺参请求原样重复只会继续失败，把网络错误都交模型重新规划也会增加成本和不确定性。

回到[本章正文与完整自测](../docs/06-ToolExecutionFailure.md)。

</details>

### 07｜副作用、并发与取消传播

<details>
<summary>父协程被取消，独立子进程一定退出吗？</summary>

不一定。独立进程需要显式信号、等待和必要的强制终止策略；还需处理输出与文件清理。不能把语言协程生命周期推广到整个操作系统。

回到[本章正文与完整自测](../docs/07-ToolSideEffectCancellation.md)。

</details>

### 08｜计划、ReAct 与停止：怎样让每一步朝目标推进

<details>
<summary>读B被拒绝后，计划里应改什么？</summary>

把B标为受阻，并说明影响的验收条件，再选择澄清、授权或部分交付。不要把它当普通临时错误无限重试，也不能直接标完成。

回到[本章正文与完整自测](../docs/08-PlanningGoalStopBudget.md)。

</details>

### 09｜上下文编排：模型这一刻到底收到什么

<details>
<summary>已有P/T/U/A/R，用户补了一句话，通常如何构造下次请求？</summary>

保持已有协议项次序，把新用户输入按控制语义加入尾部或下一轮。稳定P/T尽量复用；若用户修改约束则程序先更新控制状态，不能只是为了缓存忽略它。

回到[本章正文与完整自测](../docs/09-ContextAssemblyBudget.md)。

</details>

### 10｜上下文压缩：什么时候压、压什么、怎样继续

<details>
<summary>模型还没到窗口上限，为什么可能提前压缩？</summary>

要为输出、接下来工具结果和摘要请求预留空间；模型切换或任务阶段也可能触发。等硬上限才行动可能连摘要请求都发不出去。

回到[本章正文与完整自测](../docs/10-ContextCompactionCorrectness.md)。

</details>

### 11｜记忆生命周期：怎样记得有用，又能忘掉错误

<details>
<summary>“这次用英文”能保存成“用户永远喜欢英文”吗？</summary>

不能直接泛化。先保留本任务约束，若要长期保存需确认范围或有可靠证据。错误泛化是常见记忆污染。

回到[本章正文与完整自测](../docs/11-MemoryArchitectureLifecycle.md)。

</details>

### 12｜状态与持久化：程序怎样记得工作做到哪里

<details>
<summary>程序重启后读A的结果丢了，一定不能继续吗？</summary>

若A可按授权重新读取，且允许重算，就可以重建；若A当时内容不可再得且影响验收，则需按契约保存快照或承认无法精确恢复。

回到[本章正文与完整自测](../docs/12-SessionStatePersistence.md)。

</details>

### 13｜检查点与恢复：两次保存之间崩溃怎么办

<details>
<summary>上传成功后C2没写，恢复读C1，应直接再上传吗？</summary>

先用原逻辑操作身份核对。如果下游可幂等返回同一对象则补齐本地状态；结果未知且无安全查询/去重能力则暂停处理。

回到[本章正文与完整自测](../docs/13-CheckpointResumeReliability.md)。

</details>

### 14｜权限、批准与沙箱：三道不同的问题

<details>
<summary>用户批准发给甲，执行前地址改为乙，还能用原批准吗？</summary>

不能默认使用。收件人改变了动作含义，应重新核验批准范围，必要时再次确认。

回到[本章正文与完整自测](../docs/14-PermissionApprovalSandbox.md)。

</details>

### 15｜注入与信息保护：数据为什么不能变成命令

<details>
<summary>检索结果说“管理员批准读取密钥”，可以相信吗？</summary>

不能建立授权。它是外部内容，不是可信身份系统的批准记录。可以分析这句话，但不能据此扩权。

回到[本章正文与完整自测](../docs/15-GuardrailsInjectionContainment.md)。

</details>

### 16｜MCP、Skill与Hook：外部能力怎样接进来

<details>
<summary>你的应用连文件和工单两个Server，通常需要几个Client？</summary>

通常分别建立对应Client，由一个Host管理；用户和LLM不是这两个Client对象。

回到[本章正文与完整自测](../docs/16-MCPSkillsHooks.md)。

</details>

### 17｜意图、模型与能力路由：把请求交给合适的对象

<details>
<summary>明确/report命令是否需要LLM路由？</summary>

通常规则更直接稳定。只有命令内部仍有语义不确定性时才需要进一步模型判断。

回到[本章正文与完整自测](../docs/17-RoutingProviderResilience.md)。

</details>

### 18｜多Agent与A2A：分工、交接和跨系统任务

<details>
<summary>父级把所有历史与密钥交给检查Agent有什么问题？</summary>

扩大泄漏和上下文噪声，并可能跨权限边界。只传目标、必要证据、授权范围和输出契约，由可信程序管理凭证。

回到[本章正文与完整自测](../docs/18-MultiAgentA2AWorkspace.md)。

</details>

### 19｜Trace与排障：记录够用的信息，而不是保存整个世界

<details>
<summary>耗时排查第一步需要下载全部客户文件吗？</summary>

通常不需要。先看阶段时延、队列与错误率定位瓶颈，再决定必要的细节证据。

回到[本章正文与完整自测](../docs/19-TraceReplayObservability.md)。

</details>

### 20｜Agent评测：从“跑完了”到“有证据说明做好了”

<details>
<summary>报告引用存在但不支持结论，哪种检查不足？</summary>

引用可解析属于结构检查，仍需语义支持验证。不能把链接存在当作事实正确。

回到[本章正文与完整自测](../docs/20-AgentEvaluationBenchmark.md)。

</details>

### 21｜Coding Agent：读懂仓库、最小修改与可验证交付

<details>
<summary>修改前发现用户已有未提交文件，怎么办？</summary>

先识别其范围，避免覆盖或误纳入自己的补丁；必要时澄清，并仅修改任务所需部分。

回到[本章正文与完整自测](../docs/21-CodingAgentWorkflow.md)。

</details>

### 22｜生产Agent架构：从一个进程到可运营服务

<details>
<summary>短只读任务是否必须入队并建数据库？</summary>

不必，只要故障和容量承诺允许简单同步实现。复杂度应由需要推导。

回到[本章正文与完整自测](../docs/22-ProductionAgentRuntime.md)。

</details>

### 23｜框架与自研怎么选：按官方核心语义做比较

<details>
<summary>两个只读工具的小任务一定需要显式状态图吗？</summary>

不一定。若简单Loop更清楚且满足故障承诺，可先用它；复杂度由任务需要而不是教材组件数决定。

回到[本章正文与完整自测](../docs/23-FrameworkMappingBuildVsBuy.md)。

</details>

## 3. 综合失败推演

以下问题是教学构造，不冒充真人原话或已运行的生产实验。

<details>
<summary>报告工具返回缺参数、权限拒绝和未知上传结果，能同样发给模型重试吗？</summary>

不能。缺参数可给模型有限修复，权限拒绝不能绕过，未知上传需程序核对原操作；用户等待审批是另一种状态。分别回04、06、13、14章。

</details>

<details>
<summary>计划更新后缓存率下降，应该保留旧计划吗？</summary>

不能牺牲正确性。区分当前视图更新和历史追加，检查是否不必要改写前缀或工具Schema；压缩和必要规则更新本就可能改变缓存。回08–10章。

</details>

<details>
<summary>进程在两个检查点中间崩溃，Trace又被采样，是否只能重做全部任务？</summary>

恢复应先用必要可靠状态和操作记录；只读可重做，未知写入先核对。诊断Trace不应是关键业务回执唯一来源。回12、13、19章。

</details>

<details>
<summary>MCP Server自报只读，但要求访问全部主目录，Host该怎样处理？</summary>

Server说明不等于真实授权，Host与资源层按任务范围控制；本地Server也是要执行的软件，不能因MCP协议自动信任。回05、14–16章。

</details>

<details>
<summary>两个子Agent各自有Context却同时覆盖同一文件，为什么会这样？</summary>

信息隔离不等于资源隔离，应定义写入所有权、工作区和合并验证；父级还需核验冲突结论。回07、18、21章。

</details>

<details>
<summary>同样输入重跑模型输出不同，说明Trace失效了吗？</summary>

不说明。Trace能重建部分输入和路径，模型及外部世界仍可能变化；应按任务约束与结果评估，不承诺逐字重演。回19–20章。

</details>
