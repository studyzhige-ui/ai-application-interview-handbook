# 03. L1 应用层：任务、流程与用户交互

[← 02](02-CapabilityAndAutonomy.md) · [Agent 主线](../README.md) · [04 →](04-AgentLoopAndControl.md)

> 主线位置：**L1 应用层**。自主权确定后，先设计用户如何把工作交给系统并拿到结果。
>
> 本章产物：**任务流程与交互契约**。

[应用层先把输入组织成任务](#part-1) → [业务流程与运行循环分别编排什么](#part-2) → [入口路由：决定请求交给谁](#part-3) → [交互是执行协议的一部分](#part-4) → [交付、权限与本层的完成标准](#part-5)

<a id="part-1"></a>

## 1. 应用层先把输入组织成任务

本层面向用户和业务工作，不要求具体行业案例。入口可以是对话、API、文件上传、定时触发或外部事件；入口形式不能取代任务模型。

```text
接收输入 → 认证与范围校验 → 澄清/归类 → 建立任务契约
→ 选择确定性流程或 Agent 执行 → 展示状态 → 验收与交付
```

Task 记录目标、范围、请求者、验收条件和业务状态。Agent Definition 是可版本化的执行配置；Agent Instance 是执行中的实例。两者都不等于用户交给系统的任务。一个配置可以服务多个任务，一个任务也可以调用多个实例。

幂等的任务创建接口需要区分“重复收到同一个请求”和“用户确实要重新运行”；不能仅凭文本相同就去重。

<a id="part-2"></a>

## 2. 业务流程与运行循环分别编排什么

应用流程关心必须经过的任务阶段，运行循环关心为了推进当前阶段下一步获取什么信息、调用什么能力。一个应用流程可以在多个阶段调用同一个运行时。

Task / Run 的对照是业务与执行之间的契约，不必绑定为一种固定树。应用通过 start、status、events、steer、cancel、approval 等逻辑接口与运行层协作；具体 API 名称由产品定义。

Task 完成必须有验收证据。Run 停止可能是成功、失败、取消、预算耗尽或等待人工，不应统一显示为“任务已完成”。

<a id="part-3"></a>

## 3. 入口路由：决定请求交给谁

意图路由负责选择任务类型、应用流程或执行角色。它与 L3 的供应商适配、工具分发不是同一个问题。

### Intent Recognition 可以有多种实现

HUMAN-A `AGENT-045` 直接比较：

```text
Rule
Small Model
LLM Classification
Tool-schema autonomous selection
```

没有一种方案永远最好。

#### Rule

优点：

```text
快
可解释
稳定
```

适合明确协议：

```text
/command
固定 route
明显 keyword / tenant policy
```

#### Small Classifier

适合：

```text
标签稳定
数据充足
需要低延迟
```

#### LLM Router

适合：

```text
意图开放
语言复杂
需要语义理解
```

但成本和不确定性更高。

#### Agent 自主 Tool Selection

当 Tool Schema 已经足够表达能力时，模型可以直接选择 Tool，不一定需要独立 intent classifier。

### Router 也需要 Evaluation

不要只说：

> “我们用 LLM 做 Intent，效果不错。”

至少建立：

```text
labeled routing dataset
confusion matrix
per-intent precision / recall
fallback rate
unknown rate
latency
cost
```

更重要的是：

```text
routing error 的 downstream impact
```

例如：

```text
普通问答错路由到 destructive agent
```

比：

```text
FAQ 被路由到 generic chat
```

风险高得多。

因此不同 intent 可以有不同 error cost。

<a id="part-4"></a>

## 4. 交互是执行协议的一部分

用户需要看到进度、阻塞原因、可操作的确认请求和真实的最终结果，而不只是模型生成的文本流。

| 用户动作 | 应用层责任 | 运行层责任 |
|---|---|---|
| 澄清与追加约束 | 关联原任务，记录新的契约版本 | 在安全边界让新指令生效 |
| 确认操作 | 展示具体对象、参数、范围和后果 | 暂停、保存批准记录并在执行时重校验 |
| 取消 | 告知请求已接收及可能尚未停止的动作 | 传播取消、核对结果、释放资源 |
| 断线重连 | 恢复事件位置，补取权威状态 | 保留必要事件与持久执行状态 |
| 转人工 | 提供上下文、证据、待办和未决风险 | 暂停或移交控制权，避免双方同时写入 |

界面断开不等于任务必须取消；取消请求收到也不等于外部动作已回滚。需要为这些语义制定清楚的产品行为。

流式 token 是体验信息，动作回执和审批结果是执行事实。两者可以一起展示，但不要用一个临时 WebSocket 连接承载唯一任务状态。

<a id="part-5"></a>

## 5. 交付、权限与本层的完成标准

结果可以包含文本、结构化数据、文件、差异、证据引用、外部操作回执及未完成事项。交付必须说明哪些已验证、哪些仍未知，不能把“已发送请求”解释为“目标状态已经实现”。

L1 提供认证、确认与接管入口，L2 维护它们的执行语义，L3 传递可信身份并校验调用，L4 执行真实授权和资源隔离。安全贯穿各层，不归某一个对话按钮独占。

本层应验证重复输入、缺失信息、断线重连、取消、审批过期和转人工等交互路径。完成本章后，你应能画出用户任务的阶段，再把其中需要动态决策的一段交给下一章的运行循环。

## 本章自测

<details>
<summary>用户断线后任务应不应该取消？</summary>

由产品语义决定。连接生命周期与任务生命周期不同，必须明确定义继续、暂停、取消和重连补取状态的行为。

</details>

<details>
<summary>Run 结束是否足以显示任务完成？</summary>

不足。要区分成功、失败、取消、暂停等，并按任务验收条件核验结果。

</details>

## 回到主线

现在应能独立说明：任务流程与交互契约。下一章：[L2 运行层：执行循环与控制](04-AgentLoopAndControl.md)。

对应真人问题：`AGENT-045`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 02](02-CapabilityAndAutonomy.md) · [Agent 主线](../README.md) · [04 →](04-AgentLoopAndControl.md)
