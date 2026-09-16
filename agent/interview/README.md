# Agent 面试训练｜先回答系统，再展开机制

[← Agent](../README.md) · [综合复习](../review/README.md) · [真人问题与来源](../../research/questions/agent-harness.md)

这是第三遍训练入口。正式解释只维护在01–16章；完整真实问法、Depth、Source Count 只维护在研究题库。答案默认折叠。

## 1. 开放性设计题的开场

<details>
<summary>从零设计一个 Agent 系统，你会先考虑什么？</summary>

我先明确任务目标、范围、环境、权限与验收，判断哪些部分应由程序确定控制、哪些需要模型根据反馈动态决策。然后按应用、运行、接入、资源四层设计：应用承接与交付任务，运行层管理循环、上下文、状态和恢复，接入层提供模型、工具和数据接口，资源层提供真实能力和事实。安全与质量贯穿执行，并通过副作用核对、故障测试和结果评测验证设计。最后再选择框架、部署形态及是否需要多 Agent。

</details>

## 2. 按主线展开追问

### 01｜Agent 系统与任务契约

<details>
<summary>四层是否意味着四个微服务？</summary>

不是。逻辑职责可以同进程实现，部署边界由隔离、规模、故障与运维需求决定。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第01章](../docs/01-AgentSystemAndTaskContract.md)。

</details>

### 02｜能力设计与自主权分配

<details>
<summary>什么时候增加长期记忆或多 Agent？</summary>

当任务契约与失败证据显示跨任务信息复用或可分工协作确有价值，并能验证收益及额外风险时。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第02章](../docs/02-CapabilityAndAutonomy.md)。

</details>

### 03｜L1 应用层：任务、流程与用户交互

<details>
<summary>Run 结束是否足以显示任务完成？</summary>

不足。要区分成功、失败、取消、暂停等，并按任务验收条件核验结果。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第03章](../docs/03-ApplicationAndInteraction.md)。

</details>

### 04｜L2 运行层：执行循环与控制

<details>
<summary>final 文本能否直接触发成功状态？</summary>

应先按契约验证完成证据；结束回复、达到预算和完成任务是不同语义。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第04章](../docs/04-AgentLoopAndControl.md)。

</details>

### 05｜L2 运行层：上下文组装、预算与压缩

<details>
<summary>怎样验证压缩有效？</summary>

同时检查结构不变量、关键语义、后续执行表现、错误恢复和回归指标，而不只看节约 token。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第05章](../docs/05-ContextEngineering.md)。

</details>

### 06｜L2 运行层：记忆的选择、使用与维护

<details>
<summary>模型召回的记忆与真实系统冲突怎么办？</summary>

核对来源、版本和适用范围，必要时重新查询权威系统、保留未决状态并纠正过期记忆。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第06章](../docs/06-MemoryLifecycle.md)。

</details>

### 07｜L2 运行层：执行状态、持久化与恢复

<details>
<summary>Fork 是否复制外部世界？</summary>

不会。分叉的是执行/交互状态及允许复制的引用；真实外部动作不能因分叉被假设撤销或重做。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第07章](../docs/07-StateAndRecovery.md)。

</details>

### 08｜L2 运行层：多 Agent 协作与调度

<details>
<summary>A2A 是否自动解决多 Agent 分工？</summary>

不解决。互操作协议不代替目标分解、权限、预算、调度、汇聚和最终验收。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第08章](../docs/08-MultiAgentCoordination.md)。

</details>

### 09｜L3 接入层：模型适配、路由与容错

<details>
<summary>模型切换后可以把整个任务再跑一遍吗？</summary>

不能默认这样做。必须保留已执行动作与状态，重新验证协议兼容和恢复语义。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第09章](../docs/09-ModelAccessAndRouting.md)。

</details>

### 10｜L3 接入层：工具契约、注册与发现

<details>
<summary>Registry 与可见工具集合是什么关系？</summary>

Registry 是完整目录；可见集合是经过策略、环境和任务筛选后提供给当前模型的视图。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第10章](../docs/10-ToolContractAndDiscovery.md)。

</details>

### 11｜L3 接入层：工具执行、副作用与取消

<details>
<summary>取消请求得到确认是否说明副作用已回滚？</summary>

不是。取消传播、真正终止与外部结果核对是独立步骤，已完成动作可能需要补偿且不一定可逆。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第11章](../docs/11-ToolExecutionAndEffects.md)。

</details>

### 12｜L3 接入层：知识、记忆与扩展能力接入

<details>
<summary>为什么记忆策略与 Memory Store 接口分章？</summary>

前者决定保存和使用什么，后者兑现受控读写；分清职责能独立更换存储而保持运行语义。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第12章](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

### 13｜L4 资源层：模型、数据与执行环境

<details>
<summary>模型和数据库在 L4 是否意味着它们是次要的？</summary>

不意味着。分层表达能力与事实的提供关系，不对重要性排序。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第13章](../docs/13-ResourcesAndEnvironments.md)。

</details>

### 14｜横切治理：身份、权限、审批与安全

<details>
<summary>外部文档能否修改系统权限？</summary>

不能。外部内容是待评估的数据，不能成为新的可信授权或覆盖上层策略。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第14章](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

### 15｜横切治理：观测、评测与持续改进

<details>
<summary>一个 bad case 应怎样变成改进？</summary>

用轨迹定位责任与原因，构建可复现用例，修改对应机制，做回归与受控上线，并保留回滚方案。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第15章](../docs/15-ObservabilityAndEvaluation.md)。

</details>

### 16｜系统收口：部署、成本、选型与演进

<details>
<summary>什么时候把 Harness 和执行环境拆开部署？</summary>

当隔离、长任务恢复、资源类型、独立扩容或故障边界提出需要时，而不是为了模仿某个产品目录。

继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？

完整机制：[第16章](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

## 3. 不要这样回答

“用了模型就是 Agent”“Harness 等于整个产品”“Memory 就是所有状态”“Schema 合法就能执行”“超时表示没成功”“有沙箱就安全”“Checkpoint 保证外部动作只执行一次”“多个 Agent 一定更好”“模型说完成就是完成”。

纠正时说明具体责任和失败窗口，不用另一句口号替代。

## 4. 44 道真人问题回到哪里

下表只维护学习位置，不复制或重算研究证据。

| Canonical | 主责章节 |
|---|---|
| `AGENT-001` | [02 能力设计与自主权分配](../docs/02-CapabilityAndAutonomy.md) |
| `AGENT-002` | [01 Agent 系统与任务契约](../docs/01-AgentSystemAndTaskContract.md) |
| `AGENT-003` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-004` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-005` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-006` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-007` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-008` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-009` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-010` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-011` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-012` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-014` | [06 L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md) |
| `AGENT-015` | [06 L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md) |
| `AGENT-016` | [06 L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md) |
| `AGENT-017` | [07 L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md) |
| `AGENT-018` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-019` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-020` | [11 L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md) |
| `AGENT-021` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-022` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-023` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-024` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-025` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-026` | [11 L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md) |
| `AGENT-027` | [07 L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md) |
| `AGENT-028` | [14 横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md) |
| `AGENT-029` | [07 L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md) |
| `AGENT-030` | [08 L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md) |
| `AGENT-031` | [08 L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md) |
| `AGENT-032` | [09 L3 接入层：模型适配、路由与容错](../docs/09-ModelAccessAndRouting.md) |
| `AGENT-034` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-035` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-036` | [16 系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md) |
| `AGENT-037` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-038` | [09 L3 接入层：模型适配、路由与容错](../docs/09-ModelAccessAndRouting.md) |
| `AGENT-041` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-042` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-043` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-044` | [14 横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md) |
| `AGENT-045` | [03 L1 应用层：任务、流程与用户交互](../docs/03-ApplicationAndInteraction.md) |
| `AGENT-046` | [08 L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md) |
| `AGENT-047` | [16 系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md) |
| `AGENT-048` | [16 系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md) |
