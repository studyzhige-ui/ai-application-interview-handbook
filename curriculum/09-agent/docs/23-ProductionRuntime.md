# 23. Production Agent：从单进程到可运营执行系统

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

Production（生产环境） Agent 的核心问题是：

> **当一个 Agent 从单机 Demo 变成多用户、长任务、高并发、可恢复的平台后，Runtime（运行时执行系统） 应怎样拆服务、保存状态、隔离执行环境并治理成本？**

[← 上一章](22-CodingAgentDelivery.md) · [Agent 目录](../README.md) · [下一章 →](24-FrameworkSelection.md)

---

<a id="section-1"></a>

## 1. 先看一个单机 Demo

<a id="legacy-22-01"></a>

一个用户、短任务、允许失败后重来，单进程调用模型和只读工具完全可以是合理产品。问题出在承诺“运行半小时、断线继续、重启恢复、多人隔离”，却仍把唯一任务状态放在HTTP处理函数的局部变量里。

先写服务要承诺什么：是否跨连接运行、允许丢失多少工作、能否重复操作、多少并发、数据能保存多久。然后从承诺推导组件，而不是看到成熟产品有Sandbox（沙箱） Pool就先建一套。

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

<a id="section-2"></a>

## 2. 一个通用 Production Agent Runtime

<a id="legacy-22-02"></a>

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

图里的框是职责与故障边界，不要求第一天全部微服务化。先把接口与状态边界讲清，有独立扩缩容、隔离或跨重启承诺时再拆对应部分。

---

<a id="section-3"></a>

## 3. Brain / Hands / Durable Session 分离

<a id="legacy-22-03"></a>

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

<a id="section-4"></a>

## 4. API / Streaming Gateway

<a id="legacy-22-04"></a>

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

一直持有全部 Runtime State（状态）。

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

<a id="section-5"></a>

## 5. Harness Worker 应尽量可替换

<a id="legacy-22-05"></a>

如果所有 Session State 都只在 Worker Memory（记忆）：

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

<a id="section-6"></a>

## 6. Scheduler / Queue 为什么重要

<a id="legacy-22-06"></a>

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

<a id="section-7"></a>

## 7. Execution Sandbox Pool

<a id="legacy-22-07"></a>

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

<a id="section-8"></a>

## 8. Tool Gateway

<a id="legacy-22-08"></a>

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

<a id="section-9"></a>

## 9. Model Provider Gateway

<a id="legacy-22-09"></a>

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

否则 Framework / Provider（模型服务方） 细节会污染 Runtime 主线。

---

<a id="section-10"></a>

## 10. Durable Event / State Store

<a id="legacy-22-10"></a>

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

真正大 Artifact（产物）：

```text
log
file snapshot
browser output
```

可以独立进入 Object / Artifact Store。

Durable表示所选事实有相应持久保证，不表示无限保存所有信息。任务状态、关键回执、产物和诊断Trace（执行追踪）按不同目的管理；恢复看第12–13章，诊断看第20章，本章只组合这些责任。

---

<a id="section-11"></a>

## 11. 多租户隔离

<a id="legacy-22-11"></a>

所有层都需要 Tenant（租户） Boundary：

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

<a id="section-12"></a>

## 12. Long-running Agent 如何跨 Worker

<a id="legacy-22-12"></a>

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

<a id="section-13"></a>

## 13. Streaming 和 Durable State 不要混

<a id="legacy-22-13"></a>

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

<a id="section-14"></a>

## 14. Deployment / Scaling 的核心指标

<a id="legacy-22-14"></a>

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

<a id="section-15"></a>

## 15. Cost Governance

<a id="legacy-22-15"></a>

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

所以 Budget（预算） 可在：

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

应比较每个合格任务的总成本，包括额外重试、工具、子Agent和人工处理，而不只比较模型单价。预算用完后的交付语义也要提前定义。

---

<a id="section-16"></a>

## 16. Failure Domain

<a id="legacy-22-16"></a>

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

<a id="section-17"></a>

## 17. 一个 Production Failure Timeline

<a id="legacy-22-17"></a>

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

```text
报告上传已成功 → Worker没来得及保存回执 → 进程重启
→ 队列重新投递 → 新Worker读取原操作ID
→ 查询下游得到已有报告 → 补齐状态 → 交付
```

如果系统没有下游查询/去重，架构图再漂亮也不能证明不会重复上传。反过来，诊断Trace暂时不可用不应使已确认的报告事实消失；关键业务状态与可采样观测仍要分开。

<details>
<summary>两个成熟产品怎样作为对照，而不是指定架构模板</summary>

Codex固定Session、工具Router（路由器）、执行环境与rollout记录提供可组合的职责实例；Claude Code QueryEngine、工具目录、会话存储和取消路径也是运行支撑实例。它们告诉我们模型之外需要处理哪些实际工作，不表示你的Web服务必须照抄内部目录或默认拓扑。

部署在CLI、开发机、云沙箱或企业后端时，连接寿命、资源访问和故障承诺不同。读产品源码应先还原其环境，再提取能迁移的机制。框架具体提供哪些API与持久语义，下一章用官方接口对照。

</details>

---

<a id="section-18"></a>

## 18. Observability / Eval Plane

<a id="legacy-22-18"></a>

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

<a id="section-19"></a>

## 19. Brain / Hands 分离不是唯一正确架构

<a id="legacy-22-19"></a>

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

<a id="human-a"></a>

## 20. HUMAN-A 信号

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

<a id="interview"></a>

## 21. 面试怎么答

### Q：Production Agent Backend 怎么设计？

🎯 **建议回答**：

> 我会把 Agent 平台拆成 API/streaming gateway、durable session/run service、scheduler/queue、可替换 harness worker、model provider gateway、tool gateway、sandbox/execution pool、artifact store、durable state/event store 和 trace/eval plane。Run 状态不能只在 worker memory，要能 checkpoint/resume；Tool side effect 需要 idempotency/ledger；permission 与 sandbox 分层；tenant identity 贯穿 state、memory、artifact、credential 和 trace；并用 queue/quota/backpressure 控制 provider、tool 和 sandbox 资源。规模小时这些可以同进程实现，但边界要先设计清楚。

### Q：生产Agent Backend怎么设计？

🎯 **30 秒回答**：

> 从任务时长、恢复、并发和权限承诺出发，分清入口交互、可靠任务状态、Worker循环、模型/工具接入、执行环境与产物。长任务用任务ID和独立进度查询；关键副作用有核对依据；容量按模型、工具和存储分别控制。不是一开始把所有责任拆微服务。

### Q：为什么断开SSE不一定取消任务？

🎯 **30 秒回答**：

> 连接负责传输，任务生命周期由产品契约决定。已接受长任务可以继续运行，重连查询权威状态；真正取消需要明确操作并传播到执行子工作，不能把丢连接等同业务终止。

### Q：为什么增加Worker可能更慢？

🎯 **30 秒回答**：

> 瓶颈可能是模型配额、工具服务或存储；更多Worker增加争用、排队和重试。应看阶段容量与租户热点，用背压和准入控制，而不是只调进程数。

### Q：怎样跨Worker恢复而不重复副作用？

🎯 **30 秒回答**：

> 可靠保存任务身份、取消和未决操作，协调执行权，接手先核对原操作及回执，再重建环境和上下文继续。租约不自动杀死旧Worker，写入边界要防旧所有者继续提交。

---

<a id="pitfalls"></a>

## 22. 高频易错点

⚠️ **Production Agent = 多开几个 FastAPI worker。** Long-running State / Sandbox / Tool / Provider 都需要独立治理。

⚠️ **Durable Session = 把聊天存 DB。** 还需 Run State / Side Effect / Approval（批准） / Artifact。

⚠️ **所有组件从第一天微服务化。** 先保持边界，规模和故障需求再推动拆分。

⚠️ **Streaming Event 就是 Durable Event。** UX 与恢复审计需求不同。

⚠️ **Production必须很多微服务。** 部署拆分依据独立扩容、隔离和故障需求。

⚠️ **每个Run永久绑一个容器最好。** 可能浪费资源并耦合生命周期，应按任务选择。

⚠️ **增加Worker能解决供应商限流。** 可能制造更大限流与重试压力。

⚠️ **进度流就是可靠任务状态。** 流可断开，业务状态应有适当权威存储。

⚠️ **Trace不可用就不能知道任务成功。** 成功由业务状态与验收证据确认。

---

<a id="self-test"></a>

## 23. 本章自测

<details><summary>1. 为什么 Harness Worker 最好能被替换？</summary>

生产实例会重启、扩缩容和故障；如果正确性依赖某台 Worker 的内存状态，长任务无法可靠恢复或迁移。

</details>

<details><summary>2. 为什么 Tool Gateway 有价值？</summary>

它集中处理 credential、policy、validation、timeout、idempotency 和 trace，避免每个 Tool/Agent 直接持有生产 Secret 和各自实现安全策略。

</details>

<details><summary>3. Brain / Hands / Session 分离要解决什么？</summary>

把决策 Runtime、隔离执行环境和 durable state 分开，使 sandbox 可重建、worker 可横向扩容、长任务可恢复，同时降低执行环境的 blast radius。

</details>

<details><summary>4. 短只读任务是否必须入队并建数据库？</summary>

不必，只要故障和容量承诺允许简单同步实现。复杂度应由需要推导。

</details>

<details><summary>5. 队列重复投递会不会自动重复报告？</summary>

若执行有稳定操作身份与下游幂等/核对，可避免新逻辑副作用；队列本身不保证所有业务动作只做一次。

</details>

<details><summary>6. 沙箱被清理，报告还应能交付吗？</summary>

若产品承诺保留产物，就应在清理前转存到合适持久位置并保留授权引用，不能把唯一结果留在临时目录。

</details>

<details><summary>7. 多个租户共用Worker，只在Prompt写隔离够吗？</summary>

不够，身份必须贯穿数据查询、凭证、工具和产物访问；模型文本不构成隔离。

</details>

<details><summary>8. 每次模型调用更便宜，却任务总成本更高，为什么？</summary>

可能需要更多步骤、重试、工具和失败返工，应比较每成功任务成本及质量。

</details>

<details><summary>9. 架构图有Checkpoint、Queue和Trace，是否已证明可恢复？</summary>

没有，需明确保存和外部副作用的时间线，并实际测试故障窗口。组件名存在不等于协议正确。

</details>

---

[← 上一章](22-CodingAgentDelivery.md) · [Agent 目录](../README.md) · [下一章 →](24-FrameworkSelection.md)
