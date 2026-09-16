# 16. 系统收口：部署、成本、选型与演进

[← 15](15-ObservabilityAndEvaluation.md) · [Agent 主线](../README.md) · [复习与自测 →](../review/README.md)

> 主线位置：**四层组合与工程落地**。最后把同一套职责组合成可部署、可运营、可演进的系统。
>
> 本章产物：**完整设计、选型理由与验证方案**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 这是系统收口，不是新的组件清单。§1–2把四层落成部署/故障边界，§3比较选型，§4以代码交付作实现对照，§5再重建完整设计。先掌握各段输入输出，再按需要深入框架与Coding细节；无须一次读完，也不另拆平行课程。

[把逻辑职责落成部署与故障边界](#part-1) → [规模、成本、可靠性与升级](#part-2) → [框架选型是职责匹配，不是架构起点](#part-3) → [以 Codex 类工作过程检验交付闭环](#part-4) → [最终设计与讲解顺序](#part-5)

<a id="part-1"></a>

## 1. 把逻辑职责落成部署与故障边界

完成前15章后，才需要讨论一个进程还是多个服务。以下部署组件是前面职责的实现，不是需要另背的一套架构层：应用入口承载 L1，Harness Worker 承载 L2，模型/工具/数据适配承载 L3，各类服务、存储和执行环境承载 L4。

同一进程可以同时实现这些责任；长任务、隔离、扩容与故障需求出现后再拆开。接口、状态所有权和验收条件仍沿用同一张图。

### 先看一个单机 Demo

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

### 一个通用 Production Agent Runtime

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

### Brain / Hands / Durable Session 分离

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

### Harness Worker 应尽量可替换

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

### Scheduler / Queue 为什么重要

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

### 把旧版Gateway与持久层职责放回四层

| 实现组件 | 承载职责 | 必须交接的事实 |
|---|---|---|
| API/Streaming Gateway | L1任务入口、身份绑定、进度与交付 | task/run关联、取消/确认请求、重连位置 |
| Harness Worker / Scheduler | L2循环、预算、状态与执行权 | 检查点、租约、未决动作和停止原因 |
| Tool Gateway | L3调用校验、凭证边界、执行适配 | 稳定operation、attempt、结果/回执、策略版本 |
| Model Gateway | L3供应商兼容、限流和容错 | 能力约束、调用usage、失败原因；不是全任务重跑 |
| State / Artifact / External Services | L4保存事实及真实副作用 | 版本、可核对状态、授权访问和保留策略 |
| Trace / Eval / Audit | 横切观测、验收和改进 | 贯穿各层的关联ID、证据与评分版本 |

这是同一张逻辑图的部署映射，不要求每行一个微服务。尤其不要让Gateway或浏览器保存唯一任务状态，也不能让Worker无协调地把同一个Run分配给两个writer。旧版专章的价值是明确这些边界，不是拓扑画得越复杂越好。

<a id="part-2"></a>

## 2. 规模、成本、可靠性与升级

把端到端成本和失败预算归到任务，而不只看 HTTP 时延或单次模型 token。

### 多租户隔离

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

### Long-running Agent 如何跨 Worker

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

这就是为什么 生产部署需要在职责与机制清楚之后讨论：它是前面所有机制的汇合。

### Streaming 和 Durable State 不要混

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

### Deployment / Scaling 的核心指标

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

### Cost Governance

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

### Failure Domain

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

### 一个 Production Failure Timeline

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

### Observability / Eval Plane

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

### Brain / Hands 分离不是唯一正确架构

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

<a id="part-3"></a>

## 3. 框架选型是职责匹配，不是架构起点

用自己的任务契约、执行语义、故障测试和退出路径比较实现方案。产品 API 与默认行为随版本变化，下面的映射用于比较职责，不是永恒的功能承诺。

### 先写自己的 Requirement Matrix

在选框架前列：

```text
Agent Loop
Tool Contract
Structured Output
Streaming
Session
Checkpoint / Resume
HITL
Memory
MCP
Sandbox
Multi-Agent
Trace
Eval
Provider Adapter
Deployment
```

然后问：

```text
哪些必须有？
哪些自己已有？
哪些希望交给框架？
```

否则“框架选型”会变成品牌偏好。

### Framework 提供的价值通常是什么

框架常帮你解决：

```text
boilerplate
common integration
state / graph abstraction
tool binding
streaming
session persistence
trace hooks
MCP integration
```

好处：

```text
更快开发
少造通用轮子
生态多
```

代价：

```text
abstraction lock-in
hidden runtime semantics
upgrade cost
debug difficulty
```

所以没有“永远用框架”或“永远自研”。

### OpenAI Agents SDK 怎样映射

Tier C 官方入口公开的 Runtime Primitive 包括：

```text
built-in agent loop
function tools
handoffs / agents-as-tools
guardrails
sessions
HITL
MCP
tracing
sandbox agents
```

映射到课程：

```text
Loop           → 03
Tool            → 04–07
Handoff         → 18
Guardrail       → 15
Session / HITL  → 12–14
MCP             → 16
Trace           → 19
Sandbox         → 14
```

这正说明课程 Primitive 可以映射框架，而不需要反过来重建课程目录。

### LangGraph 适合解决什么类型问题

当你的 Agent 明显需要：

```text
State Graph
explicit node/edge
branch
pause/resume
human approval
workflow-like determinism
```

Graph abstraction 很有价值。

例如：

```text
classify
→ retrieve
→ if low confidence ask user
→ generate
→ verify
```

用 State Graph 表达清楚。

但如果只是：

```text
LLM ↔ Tool simple loop
```

不一定需要复杂 Graph。

### LangChain 适合什么

LangChain 长期价值更多在：

```text
model/tool/retriever integration
common abstractions
ecosystem
```

但生产 Runtime 的：

```text
state correctness
permission
sandbox
checkpoint semantics
idempotency
```

仍然需要你自己理解。

不能回答：

> “用了 LangChain，所以这些问题框架都处理了。”

### 什么时候自研 Runtime

可能适合自研：

```text
产品有独特 execution semantics
严格 permission / sandbox
极强 long-running state
高性能 / 极低 overhead
特殊 multi-agent scheduler
强审计 / 合规
现有平台已有很多基础设施
```

但“自研”也不等于：

```text
一切从 socket 开始写
```

可以：

```text
自研 control plane
+ 使用成熟 provider SDK
+ 使用 MCP
+ 使用标准 storage / tracing
```

### Build-vs-Buy Matrix

| 维度 | 偏 Framework | 偏自研 |
|---|---|---|
| 上线速度 | ✅ | |
| 常见 Integration | ✅ | |
| 特殊 Runtime Semantics | | ✅ |
| 强权限/隔离 | 视框架 | ✅ |
| Long-running Recovery | 看成熟度 | ✅/混合 |
| 可观测性 | 生态可提供 | 自己控制 |
| 团队维护能力 | 低 | 高 |
| Lock-in 敏感 | | ✅ |

真实决策通常是：

```text
Hybrid
```

### Framework Selection 的错误方法

#### 只看 Star

```text
GitHub Star 多
→ 选它
```

不能说明适合你的 Failure Model。

#### 只看 Demo

Demo 很难暴露：

```text
checkpoint corruption
provider failover
permission
multi-tenant state
trace cost
```

#### 只看 Feature Checklist

两个框架都写：

```text
supports memory
```

但 Memory 的：

```text
write policy
version
correctness
```

可能完全不同。

### Framework Evaluation 应该用真实 Workload

建立一个小基准：

```text
1. Tool Calling Task
2. Long-running Resume Task
3. HITL Task
4. Multi-agent Task
5. Context Compaction Task
6. Failure / Retry Task
```

对每个 Framework 看：

```text
实现复杂度
可控性
debuggability
latency
state persistence
trace
failure behavior
```

这样选型证据比“团队觉得 API 好看”强。

### Escape Hatch 很重要

使用框架时要知道：

```text
能否获取 raw provider response?
能否自定义 state store?
能否接管 tool execution?
能否覆盖 retry?
能否插入 permission?
能否导出 trace?
```

如果所有关键路径都被封死：

```text
未来 Production Requirement 出现时很难扩展
```

### Framework Upgrade 风险

Agent Framework 演进非常快。

升级可能改变：

```text
message schema
tool serialization
checkpoint format
state graph semantics
provider adapter
```

所以应用层应尽量隔离：

```text
Domain State
Tool Contract
Eval Dataset
```

不要全部绑死框架内部对象。

### 自研最小 Runtime 到底需要什么

一个很小但完整的自研 Loop 可以只有：

```text
Run State
Context Builder
Model Adapter
Tool Registry
Tool Executor
Stop Policy
Event Log
```

然后逐步加入：

```text
checkpoint
permission
trace
MCP
multi-agent
```

这比一开始写“企业级 Agent Platform”更容易验证。

### Framework 不会替你解决业务正确性

即使框架提供：

```text
checkpoint
memory
retry
```

你仍然要决定：

```text
Tool 已成功但 checkpoint 失败怎么办？
Memory 过期怎么办？
哪个动作必须 approval？
什么算任务成功？
```

这些是业务/Runtime Contract，不是一个 API 开关。

### Framework Migration

如果未来迁移框架，最重要的是把下面几层保持独立：

```text
Domain State
Tool Contract
Event / Trace Schema
Eval Dataset
Business Acceptance Criteria
```

如果这些都绑框架：

```text
迁移 = 重写整个 Agent 产品
```

反之可以：

```text
换 Orchestrator
但 Tool / State / Eval 不全部推倒
```

<a id="part-4"></a>

## 4. 以 Codex 类工作过程检验交付闭环

这里使用代码产物的验证方式作为成熟 Agent 的实现对照：理解资源、执行修改、独立验证、审阅差异、准确交付。不是新增一个行业项目，也不把测试通过等同于所有业务问题已被证明。

### Coding Agent 最大的问题不是生成，而是理解和验证

模型很容易生成：

```text
看起来合理的 patch
```

但它可能：

```text
改错文件
漏掉调用方
破坏接口
测试没跑
只修表面症状
```

所以 Harness 要提供的不只是 `edit_file`，还要有：

```text
repo discovery
search
navigation
workspace state
command execution
diff
test
verification
```

### Patch 应尽量小

目标：

```text
minimal sufficient change
```

而不是：

```text
顺手重构全项目
```

小 Patch 的优势：

- Review 容易；
- Regression Surface 小；
- 失败更容易归因；
- Rollback 简单；
- Test 范围更明确。

Planning 时可以显式限制：

```text
Non-goal: 不做无关重构
```

### Test 是 Outcome Verification，不是装饰

HUMAN-A `AGENT-036 Code Verification` 有 24 个独立来源。

最低验证层：

```text
syntax / compile
unit test
typecheck
lint
integration test
```

具体跑哪些取决于 Repository。

Agent 不能只说：

> “修改应该能工作。”

必须尽量执行可以独立验证的检查。

### Test Failure 怎么处理

不是：

```text
Test fail
→ 修改到 test 变绿
```

因为 Agent 可能“修测试”来掩盖 bug。

需要先分类：

```text
existing failure?
caused by patch?
flaky?
environment issue?
expectation changed legitimately?
```

如果要修改 Test：

```text
必须说明为什么 expectation 应改变
```

### Diff Review 是另一道防线

Tests 全过也可能出现：

```text
删除日志
放宽权限
绕过验证
加入 hardcoded secret
```

所以最终要：

```text
git diff
→ inspect changed files
→ check scope
→ check unexpected deletion
→ check security
```

Human Review 可以建立在 Diff 上，而不是重新读整个仓库。

### Acceptance Criteria 必须独立于 Agent 自评

例如 Issue：

```text
修复 retry 时重复扣款
```

完成标准应该是：

```text
new regression test reproduces old bug
patch makes test pass
existing tests pass
no duplicate external call
```

而不是：

```text
Agent: “我已解决重复扣款问题。”
```

SWE-bench 的重要启发正是：

> 用真实 repository environment 和测试结果判断问题是否真正解决。

### Verification Pyramid

可以从便宜到贵：

```text
Parse / Compile
→ Static Analysis / Typecheck
→ Targeted Unit Test
→ Related Test Suite
→ Integration / E2E
→ Full Regression
```

不是每次都跑完整 E2E，但高风险修改应该逐层提高验证强度。

### AI-assisted Development 中人的责任

健康流程：

```text
Human owns requirement / acceptance / risk
Agent accelerates discovery / patch / test
Runtime records evidence
Human reviews high-impact decision
```

不是：

```text
Agent 写代码
→ Human 只点 Merge
```

也不是：

```text
Agent 只能补全几行代码
```

责任边界取决于可验证性和风险。

### Coding Agent Failure Timeline

```text
T0  Agent 搜到相似函数 A
T1  未继续查真实调用方 B
T2  修改 A
T3  只跑了单个 unit test
T4  Test pass
T5  上线后 B 仍走另一条路径
T6  Bug 仍存在
```

根因：

```text
Repo Understanding + Acceptance Verification 不完整
```

不是“模型代码能力差”。

<a id="part-5"></a>

## 5. 最终设计与讲解顺序

```text
任务契约 → 能力与自主权 → L1 应用流程 → L2 执行与状态
→ L3 接口契约 → L4 资源与环境 → 安全与质量 → 部署、成本与演进
```

讲一个机制时，先说明它位于哪项责任之下、补上什么缺口，再解释工作方式、失败边界和验证方法。讲一个项目时，先讲目标、环境与成功标准，再沿四层展开自己的实现和取舍。

一个可复用的面试开场：

> 我先明确目标、范围、环境、权限和验收，判断哪些步骤由程序控制、哪些交给模型动态判断。然后按应用、运行、接入、资源四层设计，说明任务怎样被承接，执行如何循环并恢复，信息和动作通过什么契约连接，真实状态保存在哪里。最后检查权限、副作用、故障、成本和评测，依据实际需求决定是否增加长期记忆、多 Agent 或独立执行环境。

最终验收不是能背出所有术语，而是面对新任务能推导必要能力、解释职责和状态流动，并说明如何证明系统有效且可控。

## 把最终方案讲回最初的任务

回到01章的文件报告，不要按工具清单汇报。先说授权输入与输出验收，再说明为什么选择固定读取或受控Loop，接着画应用/运行/接入/资源的交接、失败恢复和验证。最后才回答是否需要队列、多Worker、长期Memory、多Agent和独立沙箱。

当任务规模尚小时，一个进程可实现四层职责；当持续时间、隔离或并发需求变化时，再根据瓶颈和失败证据拆分。升级不只增加组件，也增加状态迁移、版本兼容、回滚和运营责任。

框架对照是旧版保留的实现参考，不是版本无关的功能保证。候选框架应在固定版本上实际验证工具调用、断点恢复、审批、取消、压缩、追踪与迁移，记录未支持能力；官方资料和源码只证明读到的部分，不替业务验收。

## 本章自测

<details>
<summary>选框架前要有哪几项东西？</summary>

任务契约、控制权、四层职责、状态和副作用语义、失败测试及成本约束。

</details>

<details>
<summary>什么时候把 Harness 和执行环境拆开部署？</summary>

当隔离、长任务恢复、资源类型、独立扩容或故障边界提出需要时，而不是为了模仿某个产品目录。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>四层图是否必须对应四个部署服务？</summary>

不是；逻辑职责与部署边界独立，按隔离、规模、生命周期和故障需求决定拆分。

</details>

<details>
<summary>框架支持Checkpoint就能宣称长任务可靠了吗？</summary>

不能；要验证业务状态、外部副作用、批准、环境引用、版本迁移与恢复实验。

</details>

[本章面试练习与具体追问](../interview/README.md#chapter-16) · [综合复习](../review/README.md)

## 回到主线

现在应能独立说明：完整设计、选型理由与验证方案。接下来闭卷重建总图，再进入面试训练。

对应真人问题：`AGENT-036`、`AGENT-047`、`AGENT-048`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 15](15-ObservabilityAndEvaluation.md) · [Agent 主线](../README.md) · [复习与自测 →](../review/README.md)
