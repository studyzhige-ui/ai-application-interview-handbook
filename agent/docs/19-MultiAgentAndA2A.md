# 19. Multi-Agent / A2A：内部协作与跨系统任务

Multi-Agent 是 Agent 面试里非常容易“概念先行”的部分。

很多回答会变成：

> “任务复杂就拆多个 Agent，提高并行度。”

但真实 Production（生产环境） 问题更难：

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

[← 上一章](18-RoutingAndProviderResilience.md) · [Agent 目录](../README.md) · [下一章 →](20-TraceReplayAndDiagnosis.md)

---

<a id="section-1"></a>

## 1. 什么时候真的值得 Multi-Agent

<a id="legacy-18-01"></a>

多个Agent首先增加的是交接责任：谁持有控制权，子任务拿到什么信息，结果如何回来，失败由谁收口。先解释这些，再谈并行收益。

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

<a id="section-2"></a>

## 2. Subagent as Tool

<a id="legacy-18-02"></a>

最简单模式：

```text
Parent Agent
→ call subagent(task)
→ receive result
```

对于 Parent 来说，Subagent（子Agent） 很像一个复杂 Tool。

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

<a id="section-3"></a>

## 3. Handoff 模式

<a id="legacy-18-03"></a>

另一种模式：

```text
Agent A
→ 把控制权交给 Agent B
```

Handoff（控制权交接） 需要明确：

```text
新的 owner 是谁？
原 Agent 还继续吗？
Context 传多少？
State 共享还是 snapshot？
用户后续消息交给谁？
```

所以 Handoff 是 Ownership Transition，而不只是函数调用。

---

<a id="section-4"></a>

## 4. Manager / Worker 模式

<a id="legacy-18-04"></a>

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

<a id="section-5"></a>

## 5. Task Ownership 必须显式

<a id="legacy-18-05"></a>

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

报告中的Agent A负责资料事实，Agent B检查引用。父级应交给B目标、允许读取范围、待检查报告引用、预算及输出约定，而不是把自己的所有历史和凭证复制过去。B返回“哪条引用缺失、来源位置、检查范围”，比完整transcript更容易被父级验证。

Task ownership（任务所有权）回答谁负责推进哪个任务；Workspace ownership（工作区所有权）回答谁有权改哪个资源。两个上下文分开不会自动避免同时写同一文件。先单写者或独立工作区，确需并发时再加入锁、基线检查和合并验证。

父级取消要传给仍属于该任务的子工作，子任务超时不一定让父任务失败；可部分汇聚或请求补充，但必须披露缺口。递归委派需限制深度、总预算与相互等待，防止A等B、B又等A。

---

<a id="section-6"></a>

## 6. Context Isolation 为什么很重要

<a id="legacy-18-06"></a>

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

<a id="section-7"></a>

## 7. Claude Code `Task.ts` 提供的实现信号

<a id="legacy-18-07"></a>

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

> Subagent / Background Task 应是有身份、状态机、输出位置、取消语义的一等 Runtime（运行时执行系统） 对象。

---

<a id="section-8"></a>

## 8. Workspace Concurrency 是 Coding Agent 的高风险点

<a id="legacy-18-08"></a>

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

<a id="section-9"></a>

## 9. 共享 Workspace 的几种策略

<a id="legacy-18-09"></a>

### 9.1 单 Writer

```text
多个 Agent 研究
→ 一个 Integrator 真正写文件
```

最简单可靠。

### 9.2 Isolated Branch / Worktree

```text
Agent A → branch A
Agent B → branch B
→ merge / review
```

适合 Coding Agent。

### 9.3 Fine-grained Ownership

```text
Agent A owns frontend/
Agent B owns backend/
```

但要处理跨目录依赖。

### 9.4 Optimistic Merge

各自产生 Patch：

```text
base_version
patch
```

合并时检测冲突。

---

<a id="section-10"></a>

## 10. Shared State 也会 Race

<a id="legacy-18-10"></a>

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

<a id="section-11"></a>

## 11. Multi-Agent Failure

<a id="legacy-18-11"></a>

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

一个子任务失败，不应自动重跑所有成功子任务。独立有效产物先保留；最终验收需要交叉核验时就明确缺口。子任务的重试仍受自己的预算与动作身份约束。

---

<a id="section-12"></a>

## 12. Budget Explosion

<a id="legacy-18-12"></a>

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

并在 Trace（执行追踪） 记录：

```text
parent-child relation
```

---

<a id="section-13"></a>

## 13. Recursive Delegation / Deadlock

<a id="legacy-18-13"></a>

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

<a id="section-14"></a>

## 14. A2A 解决什么

<a id="legacy-18-14"></a>

A2A（Agent2Agent，智能体间互操作协议）用于独立Agent系统之间协作，让调用方不用了解对方内部Prompt、工具和框架，也能发现能力、交换消息、跟踪任务与获取产物。本节按**核验时官方1.0规范**解释，0.3的接口名字不能不标版本直接混用。

A2A不是多Agent的唯一通信方式。一个进程中的子Agent可以用函数、队列或框架私有对象；独立组织和异构系统才更需要共同协议。

| 对象 | 含义 | 报告任务例子 |
|---|---|---|
| Agent Card（能力卡片） | 能做什么、支持哪些接口与认证方式 | 外部“引用审查Agent”的介绍与端点 |
| Message（消息） | 带类型内容的交互 | 提交报告及审查要求 |
| Task（任务） | 可被跟踪的执行对象 | 长时间引用审查的taskId与状态 |
| Artifact（产物） | 任务交付的结果材料 | 审查表、修改建议文件 |
| Context标识 | 关联交互上下文 | 后续补充某来源仍关联同次审查 |

这里的Task是A2A协议对象，不要求与自己内部Run一一相等；Message也不是对方全部模型上下文。能力卡片不能替代认证，更不能把卡片写的“可信”当授权证明。

### 一次完整跨系统委派

```text
发现并验证Agent Card → 选择共同支持的接口/版本与认证
→ SendMessage提交目标、输入与必要范围
→ 简单请求直接得到Message；长任务得到Task
→ 根据能力查询GetTask或订阅/流式接收状态与产物
→ 若需要输入，补充信息并关联原任务
→ 完成后取得Artifact并按自身验收检查
→ 取消时请求CancelTask，再确认实际终态与已有产物
```

在官方1.0 JSON-RPC绑定中方法名包含`SendMessage`，与旧版常见`message/send`不同；HTTP与gRPC绑定又有对应编码。先理解共同对象和生命周期，再按实际SDK版本写请求，不靠背一个URL认识协议。

`SendMessage`响应可以是Task或直接Message，不能假设每次都创建长任务。Streaming（流式更新）与Push（推送）是需确认支持的能力；断线后不应重新委派一个新任务，而应使用既有task身份查询。远端取消可能无法撤销已完成动作，Caller与远端系统都需说清部分结果和授权边界。

---

<a id="section-15"></a>

## 15. A2A 和内部 Subagent 有什么区别

<a id="legacy-18-15"></a>

| 比较 | MCP | A2A |
|---|---|---|
| 主要抽象 | AI应用接入工具、资源、模板 | 独立Agent系统委派与交付任务 |
| 典型发现对象 | Server能力及工具目录 | Agent Card与支持的接口/技能 |
| 调用者通常关心 | 某个能力的参数与返回 | 目标、任务进度和产物 |
| 内部Loop是否由协议规定 | 不规定 | 不规定远端内部规划/工具实现 |
| 是否绝对只能同步 | 不是，可有流式/长任务扩展 | 不是，可直接消息或长任务 |

可以用MCP工具封装一次A2A委派，也可以让A2A服务内部调用MCP。选择取决于你的公共接口是“调用这项能力”还是“把工作交给另一个独立Agent系统”，而不是看到多Agent就强上A2A。

<details>
<summary>Codex、Claude与框架中的内部子Agent，不应硬套A2A</summary>

Claude用户固定`Task.ts`区分本地命令、本地/远程Agent等任务类型，维护状态和输出位置；这些是产品内部对象，不足以证明它们统一走A2A。Codex固定源码里的子Agent路径和上下文继承同样应按自己的运行时契约理解。

OpenAI Agents SDK官方用handoffs和agents-as-tools区分控制转移与返回；LangGraph可以把子图作为复杂状态流程的一部分。以上都可以表达多Agent，但并不要求每个内部调用通过A2A网络协议。只有读到具体适配器和协议请求，才应声称某个产品采用了某版A2A。

</details>

---

<a id="section-16"></a>

## 16. Result Aggregation 不是“把所有答案拼起来”

<a id="legacy-18-16"></a>

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

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[A2A官方规范](https://a2a-protocol.org/latest/specification/)。

---

<a id="human-a"></a>

## 17. HUMAN-A 信号

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

<a id="interview"></a>

## 18. 面试怎么答

### Q：什么时候用 Multi-Agent？

🎯 **30 秒回答**：

> 我只在任务可并行拆分、不同子任务需要明显不同 Context/能力，或者单 Agent Context 已经过载时考虑 Multi-Agent。设计重点不是“多少角色”，而是 task ownership、context isolation、budget、partial failure、result aggregation 和 shared-resource concurrency。Coding 场景最好给不同 Agent 独立 branch/worktree 或单 writer，避免并行覆盖同一 workspace。

### Q：MCP 和 A2A 区别？

🎯 **30 秒回答**：

> MCP 主要标准化 Agent Host 与 Tool/Resource/Prompt Server 的连接；A2A 面向独立 Agent System 之间的 capability discovery、task collaboration 和 artifact/status exchange。内部 Subagent 一般仍在同一 Runtime 控制域，和 A2A 对端的信任边界不同。

### Q：多Agent什么时候值得？

🎯 **30 秒回答**：

> 当子任务独立、可并行、上下文可隔离且结果可验证时，分工可能有收益；还需计算Token、协调、错误和汇聚成本。强依赖同一工作区、反复互等时，单Agent或简单工具并行可能更好，应与基线比较。

### Q：Handoff与Agent-as-Tool有什么区别？

🎯 **30 秒回答**：

> Agent-as-Tool通常保留父级控制，子任务返回结果后父级继续；Handoff把当前处理权交给另一个Agent。Manager/Worker还要负责多任务调度和最终验收。它们是控制关系，不自动决定通信协议或部署进程。

### Q：A2A原理与完整生命周期是什么？

🎯 **30 秒回答**：

> 先用Agent Card发现能力、接口版本和认证，发送消息发起或继续工作，简单请求可直接回Message，长任务用Task跟踪状态与Artifact。调用方查询、订阅或补充输入，最终独立验收；取消需确认终态，不等于外部动作回滚。协议不规定远端内部Loop。

### Q：两个Agent同时改文件怎么办？

🎯 **30 秒回答**：

> 分开Context只隔离信息，不隔离资源。应明确写入所有权，采用单写者、独立工作区或版本检查加合并验证。结果汇聚验证来源与冲突，而不是把两个答案拼起来当成功。

---

<a id="pitfalls"></a>

## 19. 高频易错点

⚠️ **复杂任务就应该 Multi-Agent。** 线性依赖任务常得不偿失。

⚠️ **Subagent 拿完整 Parent Context 最简单。** 会增加 Token、泄漏和噪声。

⚠️ **并行写同一个 Repo 只需要 Git 自动 merge。** 语义冲突和测试中间态仍然存在。

⚠️ **A2A = MCP for agents。** 两者连接对象和任务语义不同。

⚠️ **多Agent必定更强。** 收益需覆盖协调成本和新的失败模式。

⚠️ **A2A就是Agent互相发字符串。** 它定义发现、消息、任务、产物与交互语义。

⚠️ **用了Subagent就一定走A2A。** 内部控制可以用私有接口。

⚠️ **Agent Card等于认证。** 它声明信息，身份和访问授权另验证。

⚠️ **取消Task等于撤销远端动作。** 已有结果和副作用仍要核对。

⚠️ **MCP绝不支持长任务。** 当前规范可有任务扩展，需按版本比较。

---

<a id="self-test"></a>

## 20. 本章自测

<details><summary>1. 为什么 Task Ownership 是 Multi-Agent 的核心？</summary>

没有明确 owner，多个 Agent 可能重复执行相同任务、同时产生副作用或互相覆盖状态；ownership 是协调和恢复的基础。

</details>

<details><summary>2. 为什么 Workspace 隔离常比“约定不要冲突”可靠？</summary>

模型约定不能防止并发写；独立 branch/worktree、单 writer 或 versioned patch 可以在执行层检测和限制冲突。

</details>

<details><summary>3. Multi-Agent 最大的新成本是什么？</summary>

除了 Token 成本，还增加 task decomposition、ownership、context transfer、partial failure、shared-state concurrency、aggregation、trace 和 eval 复杂度。

</details>

<details><summary>4. 父级把所有历史与密钥交给检查Agent有什么问题？</summary>

扩大泄漏和上下文噪声，并可能跨权限边界。只传目标、必要证据、授权范围和输出契约，由可信程序管理凭证。

</details>

<details><summary>5. 为什么子任务成功不等于父任务成功？</summary>

子任务只满足局部目标，父级仍要检查覆盖、冲突、全局约束和最终交付。

</details>

<details><summary>6. A2A请求直接返回Message，是否违反协议？</summary>

不违反。官方1.0允许简单请求直接返回消息，不必每次生成持久Task。

</details>

<details><summary>7. 网络断开后直接重新SendMessage创建任务有何风险？</summary>

可能重复委派工作和副作用。应保留原任务身份并查询或重新订阅状态，按服务契约决定重试。

</details>

<details><summary>8. A等B而B又委派回A，怎样防？</summary>

明确任务依赖、委派深度与预算，检测循环等待并停止或重规划；仅有协议消息传输不会自动解决调度死锁。

</details>

<details><summary>9. 两个Agent用了独立文件副本，最后合并还要检查什么？</summary>

基线是否一致、修改是否冲突、最终文件是否满足约束与测试。隔离避免直接覆盖，但不保证合并语义正确。

</details>

<details><summary>10. 怎样证明某产品的多Agent用了A2A？</summary>

需要读取实际协议适配与请求实现，或对应官方支持说明；仅看到remote_agent、handoff或task字段不能推出协议。

</details>

---

[← 上一章](18-RoutingAndProviderResilience.md) · [Agent 目录](../README.md) · [下一章 →](20-TraceReplayAndDiagnosis.md)
