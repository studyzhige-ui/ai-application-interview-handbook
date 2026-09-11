# Agent Harness / Runtime Review

> 复习目标不是再读 47 章，而是能从空白纸画出 Runtime，并沿 Failure Case 推演。

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
Durable Truth
├─ State
├─ Event Log
├─ Artifact
└─ Memory
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
→ idempotent retry / compensation
```

## 图 4｜安全四层

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
当时模型看到了什么、做了什么 Tool Call、环境真实结果是什么、State 怎样变化、为何失败/重试。
</details>

<details><summary>14. Agent Eval 最终看什么？</summary>
优先看 environment outcome / artifact correctness，不是模型自己声明完成。
</details>

<details><summary>15. Coding Agent 的完成条件？</summary>
不仅有 patch，还要通过项目合适的 test/lint/typecheck/build，并检查 diff 与需求语义。
</details>

<details><summary>16. 为什么 Run/Turn/Step 要分层？</summary>
让 retry、budget、checkpoint、trace、cancel、approval 都有明确 scope。
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
