# Agent｜Review 与综合自测

[← 模块主页](../README.md) · [↑ Handbook 总目录](../../README.md) · [Learning Path](../../roadmap/learning-path.md) · [高频面试题 →](../interview/高频面试题.md)

> **用途：第二遍复习。** Review 不负责重新复制正文，而是要求从空白纸重建主线、机制、Failure / Trade-off 与面试表达。
>
> **学习路线是可选入口。** 如需整体安排，可参考 [Learning Path](../../roadmap/learning-path.md)；本 Review 也可以按个人节奏独立使用。

---

> 复习目标不是再读 24 个知识小板块，而是能从空白纸画出 Runtime，并沿 Failure Case 推演。**教材文件按知识闭环组织；面试题仍按可独立追问能力保持更细粒度。**

## 图 1｜最小 Runtime

```text
Goal
 ↓
Context → Model → Decision
             │
       ┌─────┴─────┐
       ▼           ▼
     Final       Tool Call
                    ↓
            Validate / Policy
                    ↓
                 Execute
                    ↓
               Observation
                    └────→ Context / State → Loop
```

## 图 2｜Context 与 State

```text
可核对/复用的信息来源
├─ 必要状态与业务回执
├─ 交互记录
├─ 产物和外部事实
└─ 经过筛选的记忆（仍可能过期或有误）
      ↓ projection
Model Context
├─ Instructions
├─ Current Goal
├─ Selected History
├─ Selected Memory
├─ Tools
└─ Observations
```

**Context 不是 Source of Truth。**

## 图 3｜长任务正确性

```text
Tool Intent
→ persist
→ execute side effect
→ persist result
→ checkpoint
→ continue

Crash?
→ load checkpoint
→ reconcile external state
→ 已确认则补齐记录；未执行且可安全重试才重试
→ 无法确认则保持待核对，不自动重做或补偿
```

## 图 4｜同一次动作的不同安全检查

```text
Untrusted Input
      ↓
Guardrail / Validation
      ↓
Permission / Approval
      ↓
Sandbox / Credential / Egress
      ↓
Tool Execution
```

## 图 5｜能力扩展

```text
Capability Catalog
├─ Built-in Tools
├─ MCP
├─ Skills
├─ Plugins / Hooks
└─ Agents
      ↓
Discovery / Routing
      ↓
Progressive Loading
```

## 图 6｜Multi-Agent

```text
Manager
├─ Specialist A → Artifact A
├─ Specialist B → Artifact B
└─ Specialist C → Artifact C
       ↓
Aggregate / Verify
```

并行收益必须覆盖 token、协调、冲突和 Eval 成本。

## 图 7｜Production

```text
API
 ↓
Run / Session Service
 ↓
Harness Workers ─→ Model Providers
 ↓
Tool Gateway ─→ Sandbox / External Systems
 ↓
Event + State + Artifact Store
 ↓
Trace / Eval
```

---

# 综合自测

<details><summary>1. Agent 和 Workflow 的根本区别？</summary>
Workflow 路径主要由程序预定义；Agent 根据中间 Observation 动态选择后续动作。步骤多不代表一定要 Agent。
</details>

<details><summary>2. Harness 为什么不是 System Prompt？</summary>
Harness 还负责真实 Tool execution、state、permission、sandbox、cancellation、recovery、trace，这些无法由 Prompt 强制保证。
</details>

<details><summary>3. Tool Call 为什么不能直接执行？</summary>
它是模型生成的非可信输入，要经过 schema/semantic validation、permission/approval、environment policy 后才能执行。
</details>

<details><summary>4. Context 与 Memory 区别？</summary>
Context 是当前 inference 实际看到的 token；Memory 是未来可再次检索的信息源，只会选择性注入 Context。
</details>

<details><summary>5. Compaction 最危险的问题？</summary>
Silent information loss 与 stale summary。Goal、hard constraints、side-effect、artifact/version 等 invariant 不能靠有损摘要维持。
</details>

<details><summary>6. Checkpoint 后为什么仍可能重复扣款？</summary>
外部 Tool 成功与 checkpoint 写入之间存在 crash window；需要 stable idempotency key、side-effect ledger 和 reconcile。
</details>

<details><summary>7. Permission 和 Sandbox 区别？</summary>
Permission 是逻辑 policy / approval；Sandbox 是执行环境的强制 filesystem/network/process 边界。
</details>

<details><summary>8. Prompt Injection 为什么不能只靠检测？</summary>
Classifier 会漏。还需要 least privilege、approval、sandbox、egress/secret containment 限制 blast radius。
</details>

<details><summary>9. MCP、Skill、Tool 怎么区分？</summary>
Tool 是动作 contract；MCP 是连接 Tool/Resource/Prompt Server 的协议；Skill 是可发现/加载的程序性知识与资源包。
</details>

<details><summary>10. 为什么 Tool 多时要 Progressive Loading？</summary>
全量 schema 浪费 Context 并降低选择精度；先 discovery 候选再加载完整 contract。
</details>

<details><summary>11. Multi-Agent 什么时候不值得？</summary>
强依赖、共享 workspace、难聚合的任务通常协调成本大于并行收益。
</details>

<details><summary>12. A2A 和内部 Subagent 区别？</summary>
内部 Subagent 可用 Runtime 私有 contract；A2A 面向独立、可能异构且内部不透明的 Agent 系统互操作。
</details>

<details><summary>13. Trace 至少要能回答什么？</summary>
先定位阶段、耗时和错误，再按需要取得授权的输入与工具证据；关键回执独立保存，不默认永久全量Trace。
</details>

<details><summary>14. Agent Eval 最终看什么？</summary>
优先看 environment outcome / artifact correctness，不是模型自己声明完成。
</details>

<details><summary>15. Coding Agent 的完成条件？</summary>
不仅有 patch，还要通过项目合适的 test/lint/typecheck/build，并检查 diff 与需求语义。
</details>

<details><summary>16. 为什么 Run/Turn/Step 要分层？</summary>
声明本项目的会话、任务执行、反馈轮与步骤口径，让重试、预算、取消与恢复有明确范围；产品Turn需单独映射。
</details>

<details><summary>17. 远程 Tool 取消后为什么可能仍要 reconcile？</summary>
客户端停止等待不代表远端副作用停止，late completion 仍可能改变真实世界。
</details>

<details><summary>18. Framework 选型的正确起点？</summary>
先列 Runtime requirements，再看框架 state/recovery/tool/security/trace 是否匹配，而不是从框架 API 反推需求。
</details>

<details><summary>19. 如何判断 Context 中一段信息该不该保留？</summary>
问它是否会改变当前决策、是否可低成本重建、是否最新可信、是否挤占更关键 Goal/State。
</details>

<details><summary>20. Production Agent 为什么需要 durable event/state？</summary>
因为进程、worker、sandbox 都可能失败或迁移；真实任务不能随单进程内存一起消失。
</details>


---

## 按薄弱主题回到正文

[01](../docs/01-AgentSystemAndResponsibilities.md) · [02](../docs/02-WorkflowAutonomyAndRuntimeBoundary.md) · [03](../docs/03-AgentLoopAndExecutionScopes.md) · [04](../docs/04-ToolContractAndValidation.md) · [05](../docs/05-ToolRegistrationAndDiscovery.md) · [06](../docs/06-ToolExecutionAndFailure.md) · [07](../docs/07-ToolConcurrencyAndCancellation.md) · [08](../docs/08-PlanningGoalAndControl.md) · [09](../docs/09-ContextAssemblyAndCache.md) · [10](../docs/10-CompactionAndContinuation.md) · [11](../docs/11-MemoryLifecycle.md) · [12](../docs/12-StateHistoryAndPersistence.md) · [13](../docs/13-CheckpointResumeAndRecovery.md) · [14](../docs/14-PermissionApprovalAndSandbox.md) · [15](../docs/15-InjectionAndContainment.md) · [16](../docs/16-MCPArchitectureAndLifecycle.md) · [17](../docs/17-SkillsHooksAndExtensions.md) · [18](../docs/18-RoutingAndProviderResilience.md) · [19](../docs/19-MultiAgentAndA2A.md) · [20](../docs/20-TraceReplayAndDiagnosis.md) · [21](../docs/21-EvaluationBenchmarkAndImprovement.md) · [22](../docs/22-CodingAgentDelivery.md) · [23](../docs/23-ProductionRuntime.md) · [24](../docs/24-FrameworkSelection.md)

编号与正式课程一致，复习可独立按个人节奏使用。

## 综合失败推演

<details><summary>1. 同一工具连续失败，应该重试、修参数还是终止？</summary>

先区分结构、语义、权限、依赖与副作用阶段。缺参数可让模型有限修复；短暂依赖故障按预算重试；权限拒绝不绕过；结果未知先核对。

</details>

<details><summary>2. 压缩后忘了“不修改原件”，只修摘要就够吗？</summary>

上下文选择与压缩会影响决策，但禁止写入还应由真实权限与执行隔离保证。分别测试摘要是否保留约束、授权门是否拒绝越界，不能互相替代。

</details>

<details><summary>3. 工具成功后检查点未写，用户又取消，怎样恢复？</summary>

核对稳定操作身份和外部结果，补齐事实再决定继续或停止。取消不等于已执行动作回滚；没有核对能力时不能靠重复执行来确认。

</details>

<details><summary>4. MCP断线是否意味着远端没有执行？</summary>

不意味着。协议连接与业务结果是不同问题。目录可以重新发现，已发出的写操作仍需核对；RPC请求ID本身不是幂等保证。

</details>

<details><summary>5. 子Agent循环等待并同时写一个文件，是同一种故障吗？</summary>

循环等待用依赖图、委派深度与超时处理；共享写入用所有权、隔离工作区或版本合并处理。上下文隔离不能自动解决两者。

</details>

<details><summary>6. 新模型Benchmark更高分，生产更慢，怎样判断？</summary>

分结果、过程、组件、成本和安全指标，核对任务分布与评分设置，再用Trace定位耗时和Provider兼容。单一分数不够证明适合本任务。

</details>
