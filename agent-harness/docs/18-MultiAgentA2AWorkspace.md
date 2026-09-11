# 18. Multi-Agent、Subagent、Handoff、A2A 与 Workspace Concurrency

Multi-Agent 是 Agent 面试里非常容易“概念先行”的部分。

很多回答会变成：

> “任务复杂就拆多个 Agent，提高并行度。”

但真实 Production 问题更难：

```text
什么时候值得拆？
谁拥有任务？
上下文怎样隔离？
如何避免重复工作？
多个 Agent 同时改一个 Workspace 怎么办？
失败一个如何收敛？
A2A 和 MCP 到底什么关系？
```

这一章的目标是把 Multi-Agent 从“角色扮演”还原成：

> **任务所有权、能力委托、上下文隔离、共享资源并发和结果聚合问题。**

---

## 1. 什么时候真的值得 Multi-Agent

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

---

# 2. Subagent as Tool

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

---

# 3. Handoff 模式

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

---

# 4. Manager / Worker 模式

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

---

# 5. Task Ownership 必须显式

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

---

# 6. Context Isolation 为什么很重要

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

---

# 7. Claude Code `Task.ts` 提供的实现信号

固定源码索引确认 Task 类型明确区分：

```text
local_bash
local_agent
remote_agent
in_process_teammate
local_workflow
monitor_mcp
dream
```

并且 Task state 包含：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

这直接支持课程抽象：

> Subagent / Background Task 应是有身份、状态机、输出位置、取消语义的一等 Runtime 对象。

---

# 8. Workspace Concurrency 是 Coding Agent 的高风险点

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

---

# 9. 共享 Workspace 的几种策略

## 9.1 单 Writer

```text
多个 Agent 研究
→ 一个 Integrator 真正写文件
```

最简单可靠。

## 9.2 Isolated Branch / Worktree

```text
Agent A → branch A
Agent B → branch B
→ merge / review
```

适合 Coding Agent。

## 9.3 Fine-grained Ownership

```text
Agent A owns frontend/
Agent B owns backend/
```

但要处理跨目录依赖。

## 9.4 Optimistic Merge

各自产生 Patch：

```text
base_version
patch
```

合并时检测冲突。

---

# 10. Shared State 也会 Race

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

---

# 11. Multi-Agent Failure

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

---

# 12. Budget Explosion

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

---

# 13. Recursive Delegation / Deadlock

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

---

# 14. A2A 解决什么

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

---

# 15. A2A 和内部 Subagent 有什么区别

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

---

# 16. Result Aggregation 不是“把所有答案拼起来”

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

---

# 17. HUMAN-A 信号

本章主要承接：

- `AGENT-030` Multi-Agent Architecture：29 个独立来源；
- `AGENT-031` Workspace / Shared-resource Concurrency：7 个；
- `AGENT-046` A2A Protocol：6 个。

真实面试深度已经进入：

```text
怎样分工？
Context 共享吗？
文件冲突怎么办？
A2A 和 MCP 区别？
如何避免递归互调？
```

---

# 18. 面试怎么答

## Q：什么时候用 Multi-Agent？

🎯 **30 秒回答**：

> 我只在任务可并行拆分、不同子任务需要明显不同 Context/能力，或者单 Agent Context 已经过载时考虑 Multi-Agent。设计重点不是“多少角色”，而是 task ownership、context isolation、budget、partial failure、result aggregation 和 shared-resource concurrency。Coding 场景最好给不同 Agent 独立 branch/worktree 或单 writer，避免并行覆盖同一 workspace。

## Q：MCP 和 A2A 区别？

> MCP 主要标准化 Agent Host 与 Tool/Resource/Prompt Server 的连接；A2A 面向独立 Agent System 之间的 capability discovery、task collaboration 和 artifact/status exchange。内部 Subagent 一般仍在同一 Runtime 控制域，和 A2A 对端的信任边界不同。

---

# 19. 高频易错点

⚠️ **复杂任务就应该 Multi-Agent。** 线性依赖任务常得不偿失。

⚠️ **Subagent 拿完整 Parent Context 最简单。** 会增加 Token、泄漏和噪声。

⚠️ **并行写同一个 Repo 只需要 Git 自动 merge。** 语义冲突和测试中间态仍然存在。

⚠️ **A2A = MCP for agents。** 两者连接对象和任务语义不同。

---

# 20. 本章自测

<details><summary>1. 为什么 Task Ownership 是 Multi-Agent 的核心？</summary>

没有明确 owner，多个 Agent 可能重复执行相同任务、同时产生副作用或互相覆盖状态；ownership 是协调和恢复的基础。
</details>

<details><summary>2. 为什么 Workspace 隔离常比“约定不要冲突”可靠？</summary>

模型约定不能防止并发写；独立 branch/worktree、单 writer 或 versioned patch 可以在执行层检测和限制冲突。
</details>

<details><summary>3. Multi-Agent 最大的新成本是什么？</summary>

除了 Token 成本，还增加 task decomposition、ownership、context transfer、partial failure、shared-state concurrency、aggregation、trace 和 eval 复杂度。
</details>
