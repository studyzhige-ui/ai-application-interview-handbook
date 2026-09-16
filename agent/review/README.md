# Agent 复习｜用同一条主线重建系统

[← Agent](../README.md) · [Handbook](../../README.md) · [面试训练](../interview/README.md)

这是第二遍复习，不是另一套教材。先闭卷回答，遇到缺口只回对应章节。

## 1. 从空白纸重建

```text
任务契约 → 能力与自主权 → L1 应用 → L2 运行 → L3 接入 → L4 资源
                       安全治理与质量运营贯穿全过程
```

画出一条输入到交付的执行路径，标出模型看见的信息、程序持有的状态、外部真实事实、每次写操作的授权与回执。再分别加入用户取消、模型失败、工具超时和进程重启。

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
