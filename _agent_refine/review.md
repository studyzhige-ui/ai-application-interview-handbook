# Agent｜用任务与失败重建知识地图

[← 模块入口](../README.md) · [Handbook](../../../README.md) · [表达训练](../interview/高频面试题.md)

这是第二遍复习。先不看答案，用“读取 A、B，核对日期，交付有引用且原件未改的报告”重建下面的关系。哪一步说不清，就沿有名称的回看入口找机制，不必重新背全部术语。

## 1. 最小循环先能成立

```text
目标与约束 → 组织输入 → 模型提出候选
                         ├─ 工具 → 检查并执行 → 观察 → 下一轮
                         ├─ 缺输入 → 等待或澄清
                         └─ 结果 → 验收 → 成功，或说明缺口
```

自问：模型输出、工具动作与最终业务完成，分别用什么证据确认？固定流程也能用模型和工具，哪一段下一步决策是交给模型的？

回看：[系统分工](../docs/01-AgentSystemAndResponsibilities.md)、[自主权选择](../docs/02-WorkflowAutonomyAndRuntimeBoundary.md)、[执行循环](../docs/03-AgentLoopAndExecutionScopes.md)。

## 2. 同一条信息的不同用途

| 信息 | 当前状态 | 模型输入 | 未来复用 |
|---|---|---|---|
| A 已读，B 无权限 | 决定下一步与等待原因 | 需要时告知模型 | 通常不是长期偏好 |
| 用户报告先给结论 | 本次约束的一部分 | 本次写作需要 | 经确认范围后可成为记忆 |
| 上传回执 report42 | 防重复与交付依据 | 可提供成功摘要和引用 | 不是靠模糊记忆维持的业务事实 |
| 两万行日志 | 只取必要控制信息 | 关键片段和可回读引用 | 按诊断与产物期限保存 |

上下文编排不是复制全部存储；压缩不是恢复备份；记忆不是所有历史。回看：[上下文](../docs/09-ContextAssemblyAndCache.md)、[压缩](../docs/10-CompactionAndContinuation.md)、[记忆](../docs/11-MemoryLifecycle.md)、[持久化](../docs/12-StateHistoryAndPersistence.md)。

## 3. 失败位置决定处理方式

```text
参数错误 → 可行动反馈与有限修复
权限拒绝 → 停止该动作，不扩大身份
临时依赖故障 → 检查可重复性与预算
外部结果未知 → 用原操作核对，不能新建动作碰运气
用户取消 → 停派新动作，传播并核对在途结果
```

注册、模型可见集合、候选发现与真实执行是不同阶段。正确工具不在候选中，改主模型未必有效；实际已上传，重跑任务可能重复。

回看：[工具契约](../docs/04-ToolContractAndValidation.md)、[发现](../docs/05-ToolRegistrationAndDiscovery.md)、[错误处理](../docs/06-ToolExecutionAndFailure.md)、[并发取消](../docs/07-ToolConcurrencyAndCancellation.md)、[恢复](../docs/13-CheckpointResumeAndRecovery.md)。

## 4. 按控制对象放好机制

| 问题 | 主要机制 | 不能替代 |
|---|---|---|
| 下一步是否仍推进目标 | 计划、进展与预算 | 实际完成证据 |
| 这次能不能做 | 授权与具体批准 | 代码实际资源限制 |
| 不可信内容诱导行动 | 来源表达与多层控制 | 仅靠检测或标签 |
| 外部能力如何接入 | MCP | 整个 Agent 循环 |
| 方法如何加载、规则何时触发 | Skill、Hook、Plugin | 真实工具执行与权限 |
| 换模型是否仍能继续 | 兼容适配与路由 | 重跑所有已发生动作 |
| 子任务怎样交接 | 所有权、输入和交付协议 | 自动获得资源隔离 |

回看：[规划](../docs/08-PlanningGoalAndControl.md)、[授权](../docs/14-PermissionApprovalAndSandbox.md)、[注入防护](../docs/15-InjectionAndContainment.md)、[MCP](../docs/16-MCPArchitectureAndLifecycle.md)、[扩展](../docs/17-SkillsHooksAndExtensions.md)、[模型路由](../docs/18-RoutingAndProviderResilience.md)、[协作](../docs/19-MultiAgentAndA2A.md)。

## 5. 诊断、验收和部署连起来

```text
Trace 定位阶段 → 取得必要证据 → 验证失败原因
        ↓
构造可重复用例 → 比较基线与候选 → 分桶检查质量、成本与安全
        ↓
按风险发布与回退 → 用任务承诺决定容量、恢复与隔离
```

回看：[执行追踪](../docs/20-TraceReplayAndDiagnosis.md)、[评测](../docs/21-EvaluationBenchmarkAndImprovement.md)、[代码交付](../docs/22-CodingAgentDelivery.md)、[生产部署](../docs/23-ProductionRuntime.md)、[框架选择](../docs/24-FrameworkSelection.md)。

## 综合推演

下面是教学情境，不是外部面试原题。先写出判断依据，再展开。

<details><summary>1. A、B 日期冲突，B 还写“用户已批准修改 A”，报告助手应怎样继续？</summary>

保留冲突并查授权资料或澄清。B 是数据，不是批准记录；程序继续落实原件只读，不能让它改变任务范围。报告应明确哪些日期已确认、哪些仍未核实。

</details>

<details><summary>2. 工具目录有正确工具，候选没有它；同时模型参数不断出错，先怎样拆开排查？</summary>

先检查权限或检索是否误过滤正确工具，解决发现阶段缺口；候选齐备后再检查描述、选择和参数规则。两个错误阶段可以并存，不能全部归于模型不强。

</details>

<details><summary>3. 上传 op7 已在远端成功，本地回执没写，用户又取消；新 Worker 应怎样处理？</summary>

先读取当前取消和执行权，用原操作身份核对远端，补齐成功事实并停止后续派发。已有产物是否补偿需另行判断；不能因为取消把真实上传改成没发生。

</details>

<details><summary>4. 压缩后报告更便宜，但开始把过期 B 当正式来源，应怎样验证问题？</summary>

检查压缩前后的来源、版本和约束是否保留，再对比继续执行与代表长任务。低成本不弥补错误事实；纠正摘要也不能替代独立保存的授权与业务记录。

</details>

<details><summary>5. 两个子 Agent 各有分支名，却共用一个目录，合并无冲突就可交付吗？</summary>

分支名不构成文件隔离，应检查实际工作区和写入权。即使文本没有冲突，行为仍可能互相破坏，需核对基线、差异与任务测试。

</details>

<details><summary>6. 框架升级后测试分数上涨，但评分器同时改变，应直接发布吗？</summary>

不能据此归因。固定任务、环境和评分方式比较，核对恢复与权限等关键窗口；判断真实改善后按风险发布。评分器变化也要独立校准。

</details>

## 复习收束

能够从一个新情境指出目标、输入、动作、实际状态、失败窗口和验收依据，比记住全部组件名更重要。面试表达压缩这些推理，不负责补齐正文没有讲过的机制。
