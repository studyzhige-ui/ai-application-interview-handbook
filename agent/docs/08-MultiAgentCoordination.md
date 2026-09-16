# 08. L2 运行层：多 Agent 协作与调度

[← 07](07-StateAndRecovery.md) · [Agent 主线](../README.md) · [09 →](09-ModelAccessAndRouting.md)

> 主线位置：**L2 运行层**。先有一个可控执行单元，再讨论如何把工作分给多个执行单元。
>
> 本章产物：**委派、汇聚、共享资源与取消协议**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 先判断任务能否独立分工，再理解交接、汇聚和共享资源。子 Agent 暂作返回状态与产物的执行单元；工具传输细节在后续接入层展开，不能因为尚未学协议就把失败当成不会发生。

[多 Agent 是运行拓扑，不是新的架构层](#part-1) → [隔离上下文并协调共享资源](#part-2) → [调度、取消、预算与死锁](#part-3) → [跨系统协作与内部子 Agent 不同](#part-4)

<a id="part-1"></a>

## 1. 多 Agent 是运行拓扑，不是新的架构层

先有单 Agent 的目标、状态、工具与恢复语义，再判断是否值得分工。增加执行角色不能修复一个不清晰的任务契约。

### 什么时候真的值得 Multi-Agent

常见适合条件：

```text
任务可以并行拆分
不同子任务需要明显不同能力 / Context
单 Agent Context 已经过载
需要独立权限 / 环境隔离
开放探索空间很大
```

例如 Research：

```text
Agent A → 查市场
Agent B → 查技术
Agent C → 查法规
Manager → 汇总
```

不适合的例子：

```text
一个线性 5 步任务
每一步强依赖上一步
```

强行 Multi-Agent 只会增加：

```text
Token
Coordination
State Sync
Failure Surface
```

Anthropic Multi-Agent Research 官方工程文章也强调：Multi-Agent 适合高并行、开放探索，但会显著增加 token 与协调成本，不是默认优于 Single Agent。

### Subagent as Tool

最简单模式：

```text
Parent Agent
→ call subagent(task)
→ receive result
```

对于 Parent 来说，Subagent 很像一个复杂 Tool。

优点：

```text
边界清晰
Context 隔离
容易限 Budget
容易 Trace
```

适合：

```text
repo research
independent analysis
parallel search
```

### Handoff 模式

另一种模式：

```text
Agent A
→ 把控制权交给 Agent B
```

Handoff 需要明确：

```text
新的 owner 是谁？
原 Agent 还继续吗？
Context 传多少？
State 共享还是 snapshot？
用户后续消息交给谁？
```

所以 Handoff 是 Ownership Transition，而不只是函数调用。

### Manager / Worker 模式

```text
Manager
├─ Worker A
├─ Worker B
└─ Worker C
```

Manager 负责：

```text
split task
assign ownership
track progress
aggregate result
resolve conflict
stop workers
```

Worker 不应该都认为：

```text
“我是最终负责整个任务的人。”
```

否则容易重复执行。

### Task Ownership 必须显式

可以给每个 Task：

```text
task_id
parent_task_id
owner_agent_id
status
dependencies
budget
workspace_scope
```

如果没有 ownership：

```text
两个 Agent 都看到待办
→ 两个都执行
→ duplicate side effect
```

这和 Backend Queue 的 competing consumer 问题类似，但 Agent 还多了模型自主决策的不确定性。

<a id="part-2"></a>

## 2. 隔离上下文并协调共享资源

子任务可以并行，但共享写入不能默认安全。权限、预算、上下文与资源所有权要随委派明确。

### Context Isolation 为什么很重要

错误：

```text
把 Parent 的全部 Context 复制给每个 Subagent
```

问题：

```text
Token 爆炸
权限信息泄漏
无关噪声
所有 Agent 看见相同偏见
```

更好：

```text
Subtask Goal
+ Relevant Constraints
+ Required Artifacts
+ Allowed Tools
+ Expected Output Contract
```

也就是：

> **传 Task Contract，不是复制整个脑子。**

### Workspace Concurrency 是 Coding Agent 的高风险点

两个 Agent 同时：

```text
Agent A → edit auth.py
Agent B → edit auth.py
```

可能发生：

```text
Lost Update
Patch Conflict
Test 在错误中间状态执行
一个 Agent 覆盖另一个 Agent 的修复
```

HUMAN-A `AGENT-031` 专门追问多 Agent 并行修改同一文件 / Workspace。

### 共享 Workspace 的几种策略

#### 单 Writer

```text
多个 Agent 研究
→ 一个 Integrator 真正写文件
```

最简单可靠。

#### Isolated Branch / Worktree

```text
Agent A → branch A
Agent B → branch B
→ merge / review
```

适合 Coding Agent。

#### Fine-grained Ownership

```text
Agent A owns frontend/
Agent B owns backend/
```

但要处理跨目录依赖。

#### Optimistic Merge

各自产生 Patch：

```text
base_version
patch
```

合并时检测冲突。

### Shared State 也会 Race

不只是文件。

例如：

```text
Agent A: task.status = done
Agent B: task.status = blocked
```

需要：

```text
versioned state
append-only event
ownership
compare-and-set
```

不要让多个 Agent 随意覆盖共享 JSON。

<a id="part-3"></a>

## 3. 调度、取消、预算与死锁

委派关系必须有界。父任务结束、子任务超时或部分失败时，运行时应有可解释的汇聚与清理行为。

### Multi-Agent Failure

假设：

```text
3 workers
A success
B timeout
C returns bad result
```

Manager 需要策略：

```text
retry B?
replace worker?
accept partial?
reassign C?
stop all?
```

所以 Multi-Agent 不是只解决并行，还引入：

```text
Partial Failure
```

### Budget Explosion

如果 Parent 每轮产生 5 个 Subagent，每个又产生 5 个：

```text
1 → 5 → 25 → 125
```

很快失控。

需要：

```text
max_depth
max_children
shared cost budget
subagent token budget
timeout
```

并在 Trace 记录：

```text
parent-child relation
```

### Recursive Delegation / Deadlock

Agent A：

```text
ask B to solve
```

Agent B：

```text
ask A to solve
```

或者：

```text
A waits B
B waits C
C waits A
```

需要：

```text
delegation graph
cycle detection
timeout
ownership rule
```

### Result Aggregation 不是“把所有答案拼起来”

Manager 要判断：

```text
结果是否互相冲突？
哪些有证据？
哪个更新？
是否重复？
是否达到 Acceptance Criteria？
```

可以要求 Subagent Output Contract：

```text
summary
evidence
artifacts
open_questions
confidence
```

而不是自由文本。

<a id="part-4"></a>

## 4. 跨系统协作与内部子 Agent 不同

A2A 讨论跨 Agent 系统的发现、任务和消息交互；协议连接不会自动提供正确分工、可信结果或业务一致性。

### A2A 解决什么

A2A 面向：

```text
独立 Agent System
↔ 独立 Agent System
```

官方规范强调：

- capability discovery；
- interaction modality negotiation；
- collaborative task management；
- secure information exchange。

课程边界：

```text
MCP
→ Agent / Host 连接 Tool / Resource

A2A
→ Agent System 与 Agent System 协作
```

二者不是互相替代。

### A2A 和内部 Subagent 有什么区别

内部 Subagent：

```text
同一个 Runtime 控制域
```

通常共享：

```text
auth
trace
budget
policy
session family
```

A2A 对端可能：

```text
独立部署
独立权限
内部实现不可见
```

因此更需要协议化：

```text
capability
identity
task
artifact
status
error
security
```

## 分工示例：同一报告的两个调查方向

只有当两个来源集合确实可以独立调查，才尝试让两个子执行单元分别返回证据。交接契约至少包含目标、授权范围、预算、截止时间、允许的产物形式和失败状态；不默认继承父级全部历史和写权限。

子A完成、子B超时时，父级要根据验收决定部分交付、继续单独调查或返回未完成，不能把A的成功算作整个任务成功。汇聚的是证据、来源和未决问题，不是把两份完整transcript重新塞回父Context。

共享产物写入采用唯一writer或隔离目录加版本化汇聚。上下文隔离只隔离信息，不会自动消除共享文件竞争。父级预算还需包含子任务占用，避免递归委派放大成本。

旧版 `Task.ts` 对照的价值在于任务具有状态、输出位置和取消语义；这些产品Task类型不等于本课程L1业务Task，见[Claude Code任务索引](../../research/agent-sources/claude-code-source-index.md)。

## 本章自测

<details>
<summary>子 Agent 分开上下文后，共享文件写入就安全了吗？</summary>

没有。信息隔离与资源并发是两件事，需要写入所有权、隔离工作区、锁或版本化合并。

</details>

<details>
<summary>A2A 是否自动解决多 Agent 分工？</summary>

不解决。互操作协议不代替目标分解、权限、预算、调度、汇聚和最终验收。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>子任务一半成功、一半超时，父任务如何汇聚？</summary>

根据验收判断部分交付、继续调查或失败，保留未决证据；不能用成功子任务覆盖失败部分。

</details>

<details>
<summary>父Agent的批准是否默认能传给所有子Agent？</summary>

不能；按任务范围、身份、参数和资源重新约束，不能因委派扩大权限。

</details>

## 回到主线

现在应能独立说明：委派、汇聚、共享资源与取消协议。下一章：[L3 接入层：模型适配、路由与容错](09-ModelAccessAndRouting.md)。

对应真人问题：`AGENT-030`、`AGENT-031`、`AGENT-046`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 07](07-StateAndRecovery.md) · [Agent 主线](../README.md) · [09 →](09-ModelAccessAndRouting.md)
