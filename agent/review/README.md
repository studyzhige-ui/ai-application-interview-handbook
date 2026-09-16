# Agent 复习｜用同一条主线重建系统

[← Agent](../README.md) · [Handbook](../../README.md) · [可选学习路线](../../roadmap/learning-path.md) · [面试训练](../interview/README.md)

这是第二遍复习，不是另一套教材。先闭卷回答，遇到缺口只回对应章节。

## 1. 从空白纸重建

```text
任务契约 → 能力与自主权 → L1 应用 → L2 运行 → L3 接入 → L4 资源
                       安全治理与质量运营贯穿全过程
```

画出一条输入到交付的执行路径，标出模型看见的信息、程序持有的状态、外部真实事实、每次写操作的授权与回执。再分别加入用户取消、模型失败、工具超时和进程重启。

## 机制局部图｜放大同一张四层图，不是另一套架构

吸收main原Review的七种机制图，按新版职责重新组织。先自行画，再展开对照；不把Memory当作权威事实，不把安全链路再命名为一套“架构四层”。

<details>
<summary>局部图1｜运行层怎样把候选决策变成闭环（04章）</summary>

```text
目标/约束 → Context → 模型候选
                      ├─ 行动 → 校验/授权 → 工具执行 → 观察/状态 → 继续
                      ├─ 缺输入/批准 → 暂停并持久化
                      └─ 完成候选 → 独立验收 → 交付或返回缺口
```

达到预算只是有原因的停止，不是成功。回到[04执行控制](../docs/04-AgentLoopAndControl.md)。

</details>

<details>
<summary>局部图2｜信息从哪里来，什么是事实、什么是投影（05–07章）</summary>

```text
任务契约/可信策略 + Runtime状态/回执 + 外部权威事实
                         ↓ 受控选择与版本核验
历史记录 + 相关Memory + 检索证据 + Tool结果/Artifact引用
                         ↓ 去重、预算、适配
                     当前模型Context
```

Memory可能有错，History记录的是过去，Context是本轮视图；三者都不能自动覆盖权威事实和当前授权。回到[05上下文](../docs/05-ContextEngineering.md)、[06记忆](../docs/06-MemoryLifecycle.md)、[07状态](../docs/07-StateAndRecovery.md)。

</details>

<details>
<summary>局部图3｜长任务在什么窗口会重复动作（07、11章）</summary>

```text
建立逻辑操作身份/保存意图
→ 校验授权与前置条件 → 提交外部动作
→ 取得回执 → 保存结果/检查点 → 继续

中途崩溃 → 读取恢复状态 → 核对未知操作
          → 已成功则补状态；安全可重放才重试；不可核对则UNKNOWN/人工
```

这是恢复协议示意，不是跨系统原子事务或exactly-once保证。回到[07恢复](../docs/07-StateAndRecovery.md)、[11副作用](../docs/11-ToolExecutionAndEffects.md)。

</details>

<details>
<summary>局部图4｜能力怎样被发现而不被过度暴露（09–12章）</summary>

```text
L2当前需求/预算
→ L3完整能力目录 → 权限/环境/任务筛选
→ 候选发现 → 按需加载完整契约 → 版本解析与调用
→ L4真实资源返回 → 结果校验 → L2后续决策
```

Tool是动作接口，MCP是连接协议，Skill是知识/资源包，Hook是生命周期点；目录收录或模型可见都不等于实际授权。回到[10发现](../docs/10-ToolContractAndDiscovery.md)、[12扩展](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

<details>
<summary>局部图5｜多Agent怎样分工与收口（08章）</summary>

```text
父级任务契约/总预算
 ├─ 子A：范围/资源/截止时间 → 证据/产物/状态
 └─ 子B：范围/资源/截止时间 → 证据/产物/状态
                         ↓
           冲突核对 + 汇聚 + 最终验收
```

共享写入还需所有权、隔离或版本协调；子任务成功不能覆盖整体未完成，委派也不能放大权限。回到[08协作](../docs/08-MultiAgentCoordination.md)。

</details>

<details>
<summary>局部图6｜安全约束落在哪些执行点（13–14章）</summary>

```text
L1可信身份与明确确认范围
→ L2维护契约/审批状态，区分指令与不可信资料
→ L3每次调用校验参数、权限、版本与凭证范围
→ L4资源授权及适用的文件/网络/进程隔离
→ 输出/Artifact/Trace访问与外传控制
```

这是一条横跨既有四层的责任链，不是“安全四层”新架构。事后过滤不能撤销已发生的副作用。回到[13环境](../docs/13-ResourcesAndEnvironments.md)、[14安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<details>
<summary>局部图7｜生产部署与质量闭环（15–16章）</summary>

```text
任务入口 → Run服务/调度 → Harness Worker
                         ├─ 模型适配 → 模型服务
                         ├─ Tool接入 → 外部系统/执行环境
                         └─ 状态/产物接口 → 持久存储
各阶段事件/证据 → Trace定位 → 固定回归用例 → 修改/评测 → 受控发布/回滚
```

逻辑角色可以同进程实现；拆分要有规模、隔离或故障证据。图里的框不意味着全部都必须立即部署。回到[15观测评测](../docs/15-ObservabilityAndEvaluation.md)、[16生产演进](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

## 2. 逐章闭卷检查

### 01｜Agent 系统与任务契约

<details>
<summary>业务场景为什么不与 Memory 并列成模块？</summary>

场景是设计输入，决定目标、环境和验收；Memory 是根据复用需求选择的一项能力，类型不同。

回到[第01章](../docs/01-AgentSystemAndTaskContract.md)。

</details>

### 02｜能力设计与自主权分配

<details>
<summary>模型判断某动作安全，能直接执行吗？</summary>

不能。模型建议不建立身份、授权或业务合法性；可信程序与后端须实施相应控制。

回到[第02章](../docs/02-CapabilityAndAutonomy.md)。

</details>

### 03｜L1 应用层：任务、流程与用户交互

<details>
<summary>用户断线后任务应不应该取消？</summary>

由产品语义决定。连接生命周期与任务生命周期不同，必须明确定义继续、暂停、取消和重连补取状态的行为。

回到[第03章](../docs/03-ApplicationAndInteraction.md)。

</details>

### 04｜L2 运行层：执行循环与控制

<details>
<summary>Turn、模型调用、Item 是同一件事吗？</summary>

不是。Codex 的 Turn 包含一次请求及后续工作，可能包含多次推理和工具交互；Item 是有类型的输入输出单元。

回到[第04章](../docs/04-AgentLoopAndControl.md)。

</details>

### 05｜L2 运行层：上下文组装、预算与压缩

<details>
<summary>Compaction 为什么不能替代持久化？</summary>

它管理当前模型可见信息，可能有损；审批、回执、进度等恢复事实需要独立保存。

回到[第05章](../docs/05-ContextEngineering.md)。

</details>

### 06｜L2 运行层：记忆的选择、使用与维护

<details>
<summary>Memory 为什么不是把 History 全部存起来？</summary>

Memory 是为未来复用选择并维护的信息，具有来源、作用域、版本和失效策略；History 是发生过的记录。

回到[第06章](../docs/06-MemoryLifecycle.md)。

</details>

### 07｜L2 运行层：执行状态、持久化与恢复

<details>
<summary>工具成功但检查点写入失败，恢复时先做什么？</summary>

核对已记录操作标识、幂等键和外部状态；确认已发生的副作用后再继续，不能盲重放写操作。

回到[第07章](../docs/07-StateAndRecovery.md)。

</details>

### 08｜L2 运行层：多 Agent 协作与调度

<details>
<summary>子 Agent 分开上下文后，共享文件写入就安全了吗？</summary>

没有。信息隔离与资源并发是两件事，需要写入所有权、隔离工作区、锁或版本化合并。

回到[第08章](../docs/08-MultiAgentCoordination.md)。

</details>

### 09｜L3 接入层：模型适配、路由与容错

<details>
<summary>Adapter 是否应抹平所有供应商差异？</summary>

不应。必须保留能力差异和不支持情况，避免把不兼容的工具、多模态或状态协议静默伪装为支持。

回到[第09章](../docs/09-ModelAccessAndRouting.md)。

</details>

### 10｜L3 接入层：工具契约、注册与发现

<details>
<summary>Schema 合法为什么不等于操作合法？</summary>

Schema 主要检验形状，还需语义、身份、租户、权限、风险和业务约束检查。

回到[第10章](../docs/10-ToolContractAndDiscovery.md)。

</details>

### 11｜L3 接入层：工具执行、副作用与取消

<details>
<summary>超时是否说明动作没有发生？</summary>

不说明。调用方可能只是未收到响应，必须根据执行阶段与外部结果判断重试资格。

回到[第11章](../docs/11-ToolExecutionAndEffects.md)。

</details>

### 12｜L3 接入层：知识、记忆与扩展能力接入

<details>
<summary>RAG、MCP、Skill、Hook 是同一种抽象吗？</summary>

不是。RAG 是证据获取与使用方案，MCP 是协议，Skill 是程序性知识/资源包，Hook 是生命周期扩展机制。

回到[第12章](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

### 13｜L4 资源层：模型、数据与执行环境

<details>
<summary>只有受控 API 工具的 Agent 必须配代码沙箱吗？</summary>

不必须。没有任意代码执行需求时，不应为凑组件增加执行环境；API 仍需自身授权与隔离。

回到[第13章](../docs/13-ResourcesAndEnvironments.md)。

</details>

### 14｜横切治理：身份、权限、审批与安全

<details>
<summary>所有工具都弹确认框是否足够安全？</summary>

不够。还要有真实身份、最小权限、审批绑定、执行时校验、环境隔离、凭证和外传控制。

回到[第14章](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

### 15｜横切治理：观测、评测与持续改进

<details>
<summary>Trace 和 Eval 各回答什么？</summary>

Trace 记录过程及关联事实；Eval 依据任务和约束判断结果、过程、组件与安全资源指标。

回到[第15章](../docs/15-ObservabilityAndEvaluation.md)。

</details>

### 16｜系统收口：部署、成本、选型与演进

<details>
<summary>选框架前要有哪几项东西？</summary>

任务契约、控制权、四层职责、状态和副作用语义、失败测试及成本约束。

回到[第16章](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

## 3. 综合验收

能区分应用流程与 Agent Loop，能解释静态四层和动态状态如何对应；能把 Memory、RAG、Tool、Sandbox 等放回职责；能说明为什么某任务不需要某组件；能定位一次失败的责任边界，并提出验证而不是只换模型。

不要只检查能否复述术语。每个机制都应能回答：为什么存在、输入输出是什么、何时失效、如何测试。

## 综合推演｜把main的机制复习接回四层图

以下是教学压力测试，不是声称已发生的真人面试或已运行的真实系统实验。每题先画时间线，再说明责任、未知事实、下一步动作及如何验证。

<details>
<summary>1. 报告任务读不到一个关键文件：该加工具、扩大权限，还是请求澄清？</summary>

先回契约看缺口是否阻碍验收。L3报告拒绝，L2保留未决证据，L1请求澄清或按约定部分交付；不能通过新工具绕开资源权限。回到[01](../docs/01-AgentSystemAndTaskContract.md)、[03](../docs/03-ApplicationAndInteraction.md)、[14](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<details>
<summary>2. 50K token工具结果挤掉“不改原件”，压缩后模型提出写操作，故障在哪？</summary>

先查来源选择、预算、外部化和压缩不变量，再检查真实授权门是否拒绝；安全不应仅依赖这句话仍在Context。回到[05](../docs/05-ContextEngineering.md)、[11](../docs/11-ToolExecutionAndEffects.md)、[14](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<details>
<summary>3. 产物已经保存，检查点失败，用户同时取消，worker又重启，先做什么？</summary>

载入契约、状态和稳定动作身份，核对产物及迟到回执，补齐事实并停止后续动作。取消不是回滚；无法确认结果时保留UNKNOWN，不重复创建新动作。回到[07](../docs/07-StateAndRecovery.md)、[11](../docs/11-ToolExecutionAndEffects.md)、[13](../docs/13-ResourcesAndEnvironments.md)。

</details>

<details>
<summary>4. 两个子Agent给出冲突结论并同时更新一个文件，为什么“不同Context”没解决？</summary>

信息隔离与资源并发不同。用来源/版本判定结论冲突，writer所有权或隔离工作区处理写冲突，父级按验收汇聚而不是拼transcript。回到[06](../docs/06-MemoryLifecycle.md)、[08](../docs/08-MultiAgentCoordination.md)。

</details>

<details>
<summary>5. 模型切换后更便宜，但工具调用变错、总体完成率下降，应改哪一层？</summary>

先查L2能力要求、L3协议/schema兼容与上下文处理，再固定数据/工具/评分做回归；保留已有副作用，不因Provider故障重跑整个任务。回到[09](../docs/09-ModelAccessAndRouting.md)、[10](../docs/10-ToolContractAndDiscovery.md)、[15](../docs/15-ObservabilityAndEvaluation.md)。

</details>

<details>
<summary>6. Agent说代码改完、测试通过，但改了他人文件或测试没覆盖需求，怎样拒绝交付？</summary>

核对工作区基线、最小diff、真实测试回执及独立验收，区分“执行某项检查通过”和“任务完成”。回到[13](../docs/13-ResourcesAndEnvironments.md)、[15](../docs/15-ObservabilityAndEvaluation.md)、[16](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

## 自行验收，不绑定固定周数

能从契约画到四层并说明未采用组件的理由；能解释Context/Memory/State/History的不同生命周期；随机选上面的一个失败窗口，说明已知、未知、核对动作、停止/恢复和验证。薄弱处只回对应章，再用面试页的具体追问训练，不以“读过文件”代替掌握。
