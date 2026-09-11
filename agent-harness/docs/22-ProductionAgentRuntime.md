# 22. Production Agent Runtime Architecture

前面 21 个知识小板块分别解决了：

```text
Loop
Tool
Context
Memory
State
Checkpoint
Security
MCP
Multi-Agent
Trace
Eval
Coding Workflow
```

最后要把它们重新装进一个真正可部署的系统。

Production Agent 的核心问题是：

> **当一个 Agent 从单机 Demo 变成多用户、长任务、高并发、可恢复的平台后，Runtime 应怎样拆服务、保存状态、隔离执行环境并治理成本？**

---

## 1. 先看一个单机 Demo

```text
HTTP Request
→ Python Process
→ Model API
→ Tool
→ Response
```

小 Demo 没问题。

但 Production 会出现：

```text
请求运行 30 分钟
进程重启
用户断线
多个 worker
Sandbox 执行代码
Tool 要访问内部系统
Provider 限流
Context 很大
需要审批
需要 Resume
需要 Trace / Eval
```

于是单进程对象不再足够。

---

# 2. 一个通用 Production Agent Runtime

```text
Client
  ↓
API / Streaming Gateway
  ↓
Session / Run Service
  ↓
Scheduler / Queue
  ↓
Harness Worker
  ├─ Model Provider Gateway
  ├─ Tool Gateway
  ├─ Retrieval / Memory
  ├─ Permission / Policy
  └─ Sandbox / Execution Environment
  ↓
Durable Event / State Store
  ↓
Trace / Eval / Audit
```

这不是某个框架固定拓扑，而是从前面 Runtime 问题推导出的通用组件。

---

# 3. Brain / Hands / Durable Session 分离

Anthropic `Scaling Managed Agents: Decoupling the brain from the hands` 提供了很有价值的成熟参考：

```text
brain / harness
hands / execution environment
durable session log
```

课程抽象：

```text
Harness Worker
= 决策与 Runtime 控制

Execution Environment
= 真正访问文件 / 进程 / 网络 / Tool 的“手”

Durable Session
= Context Window 之外可恢复的执行事实
```

分离后的好处：

- Harness 可以水平扩容；
- Sandbox 可以独立重建；
- Session 不绑某一个进程；
- Execution Risk 和 Model Runtime 分离；
- 长任务可以迁移 Worker。

---

# 4. API / Streaming Gateway

入口负责：

```text
auth
tenant
request id
run create/resume/cancel
stream events
rate / quota boundary
```

长任务不应该让：

```text
一个 HTTP handler
```

一直持有全部 Runtime State。

更稳：

```text
POST /runs
→ run_id

GET /runs/{id}
POST /runs/{id}/cancel
STREAM /runs/{id}/events
```

Transport 细节 Primary 在 FastAPI / Backend；Agent 模块关心 Run Lifecycle。

---

# 5. Harness Worker 应尽量可替换

如果所有 Session State 都只在 Worker Memory：

```text
worker crash
→ run lost
```

Production 更希望：

```text
Worker loads durable run state
→ execute one / several steps
→ persist progress
→ another worker can resume
```

这并不要求每一步都完全 stateless，但要求：

> **正确性不能依赖某台机器永远不死。**

---

# 6. Scheduler / Queue 为什么重要

如果 1000 个用户同时发 Agent 任务：

```text
全部立刻起模型 + sandbox + tool
```

可能压垮：

```text
Provider quota
GPU
DB
Tool Backend
Sandbox pool
```

需要：

```text
queue
priority
tenant quota
concurrency limit
backpressure
admission control
```

通用 Queue / Backpressure 算法 Primary 在 AI Backend Engineering，但这里需要把它们映射到：

```text
Run / Tool / Subagent Budget
```

---

# 7. Execution Sandbox Pool

Coding / Browser / Shell Agent 需要隔离环境。

可以：

```text
prewarm sandbox pool
→ assign to run
→ mount scoped workspace
→ execute
→ collect artifact
→ reset / destroy
```

需要治理：

```text
CPU / memory
filesystem
network
process count
timeout
secret
image version
```

Sandbox 生命周期不一定和 Session 生命周期相同。

---

# 8. Tool Gateway

不要让所有 Tool 各自随意访问生产系统。

可以引入：

```text
Tool Gateway
```

负责：

```text
auth / credential
policy
schema validation
rate limit
timeout
idempotency
trace
```

Model / Harness 只拿到：

```text
受控 Tool Contract
```

而不是底层数据库密码。

---

# 9. Model Provider Gateway

负责统一：

```text
provider adapter
model routing
retry / fallback
usage / cost
stream normalization
quota
```

Agent Loop 不应该到处写：

```text
if provider == ...
```

否则 Framework / Provider 细节会污染 Runtime 主线。

---

# 10. Durable Event / State Store

至少要支撑：

```text
Session
Run
State Version
Event
Checkpoint
Approval
Side-effect Ledger
Artifact Reference
```

真正大 Artifact：

```text
log
file snapshot
browser output
```

可以独立进入 Object / Artifact Store。

---

# 11. 多租户隔离

所有层都需要 Tenant Boundary：

```text
API auth
Session state
Memory
Artifact
Tool credential
Sandbox
Trace
Quota
```

只在数据库表里加 `tenant_id` 不够。

真正危险的是：

```text
Tenant A Run
→ 错拿 Tenant B Credential / Memory / Artifact
```

所以 identity 必须贯穿整个 Runtime。

---

# 12. Long-running Agent 如何跨 Worker

```text
Worker A acquires run lease
→ execute
→ checkpoint
→ lease expires / worker dies
→ Worker B loads checkpoint
→ reconcile side effect
→ continue
```

必须组合前面学过的：

```text
Checkpoint
State Version
Lease / Fencing
Idempotency
Artifact
```

这就是为什么 Production Architecture 必须放在最后：它是前面所有机制的汇合。

---

# 13. Streaming 和 Durable State 不要混

Streaming Event：

```text
给用户实时 UX
```

Durable Event：

```text
支持恢复 / 审计
```

有些事件两边都需要，但语义不同。

例如 Token delta 可以：

```text
stream only
```

而 Tool Side Effect Confirmation 必须：

```text
durable
```

---

# 14. Deployment / Scaling 的核心指标

除了普通 API QPS：

```text
active runs
steps/sec
model calls/sec
tool calls/sec
sandbox utilization
queue delay
context tokens/run
cost/run
run duration
resume rate
failure rate
```

如果只看：

```text
HTTP P95
```

很难理解 Agent 平台真正瓶颈。

---

# 15. Cost Governance

Agent 的成本不是只有 Model Token：

```text
model
embedding / retrieval
sandbox compute
tool API
storage
trace
subagent multiplication
```

所以 Budget 可在：

```text
run
tenant
workspace
model
subagent
```

多层限制。

例如：

```text
user budget exhausted
→ pause / ask / switch cheaper route
```

而不是无限执行直到 Provider 拒绝。

---

# 16. Failure Domain

Production 需要知道每个组件挂掉会怎样。

```text
API Gateway down
→ 新请求受影响，已有 Run 是否继续？

Harness Worker down
→ checkpoint 后能否接管？

Model Provider down
→ queue / fallback / fail?

Tool Backend down
→ retry eligibility?

State Store down
→ 是否必须停止外部 side effect?

Trace Store down
→ fail-open or fail-closed?
```

这些都应该写进 Runtime Policy。

---

# 17. 一个 Production Failure Timeline

```text
T0 Worker A 获得 run lease
T1 Agent 调用 payment tool
T2 Payment success
T3 State Store timeout
T4 Worker A crash
T5 Worker B 接管
```

这时 B 必须：

```text
load durable state
→ inspect side-effect ledger
→ reconcile payment external reference
→ mark step done
→ continue
```

否则会重复扣款。

你会发现 Production Architecture 不能脱离前面的 Reliability 章节。

---

# 18. Observability / Eval Plane

生产平台应能从：

```text
Run Trace
→ bad case attribution
→ eval dataset
→ regression
```

形成闭环。

同时平台运营指标：

```text
success / cost / latency / safety
```

用于：

```text
routing
capacity
budget
release decision
```

---

# 19. Brain / Hands 分离不是唯一正确架构

重要提醒：

Anthropic Managed Agents 是成熟产品参考，不是所有 Agent 系统的唯一拓扑。

小系统可以：

```text
single service
```

只要 Runtime Contract 清楚。

当出现：

```text
长任务
sandbox
多租户
横向扩容
```

再逐步拆分。

正确原则是：

> **架构复杂度应由 Failure / Scale / Security 需求推动，而不是因为“Agent 平台应该长这样”。**

---

# 20. HUMAN-A 与 Tier C

Agent Canonical 中大量 L4 问题最终都会落到本章：

```text
Checkpoint
Permission
Multi-Agent
Resilience
Trace
Evaluation
```

Tier C 中 Anthropic Managed Agents 提供 brain/hands/session 分离参考；OpenAI / Anthropic 其它资料补充 HITL、Tracing、Sandbox、Evaluation。

这些外部资料只补课程完整性，不改变 HUMAN-A 频率。

---

# 21. 面试怎么答

## Q：Production Agent Backend 怎么设计？

🎯 **2 分钟骨架**：

> 我会把 Agent 平台拆成 API/streaming gateway、durable session/run service、scheduler/queue、可替换 harness worker、model provider gateway、tool gateway、sandbox/execution pool、artifact store、durable state/event store 和 trace/eval plane。Run 状态不能只在 worker memory，要能 checkpoint/resume；Tool side effect 需要 idempotency/ledger；permission 与 sandbox 分层；tenant identity 贯穿 state、memory、artifact、credential 和 trace；并用 queue/quota/backpressure 控制 provider、tool 和 sandbox 资源。规模小时这些可以同进程实现，但边界要先设计清楚。

---

# 22. 高频易错点

⚠️ **Production Agent = 多开几个 FastAPI worker。** Long-running State / Sandbox / Tool / Provider 都需要独立治理。

⚠️ **Durable Session = 把聊天存 DB。** 还需 Run State / Side Effect / Approval / Artifact。

⚠️ **所有组件从第一天微服务化。** 先保持边界，规模和故障需求再推动拆分。

⚠️ **Streaming Event 就是 Durable Event。** UX 与恢复审计需求不同。

---

# 23. 本章自测

<details><summary>1. 为什么 Harness Worker 最好能被替换？</summary>

生产实例会重启、扩缩容和故障；如果正确性依赖某台 Worker 的内存状态，长任务无法可靠恢复或迁移。
</details>

<details><summary>2. 为什么 Tool Gateway 有价值？</summary>

它集中处理 credential、policy、validation、timeout、idempotency 和 trace，避免每个 Tool/Agent 直接持有生产 Secret 和各自实现安全策略。
</details>

<details><summary>3. Brain / Hands / Session 分离要解决什么？</summary>

把决策 Runtime、隔离执行环境和 durable state 分开，使 sandbox 可重建、worker 可横向扩容、长任务可恢复，同时降低执行环境的 blast radius。
</details>
