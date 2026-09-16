# 06. L2 运行层：记忆的选择、使用与维护

[← 05](05-ContextEngineering.md) · [Agent 主线](../README.md) · [07 →](07-StateAndRecovery.md)

> 主线位置：**L2 运行层**。当前上下文清楚后，再决定哪些信息值得跨步骤、跨任务复用。
>
> 本章产物：**记忆读写、来源、更新与失效策略**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 按选择→写入→召回→纠错→失效走完生命周期。暂把 Memory Store 当成带作用域和版本的存取接口；12章讲接口，13章讲实际存储，不能把三个责任混成一个数据库。

[记忆策略属于运行层，记忆数据库不属于运行层](#part-1) → [选择、提取、写入与按需召回](#part-2) → [纠错、冲突与失效是核心机制](#part-3) → [记忆的安全与验收](#part-4)

<a id="part-1"></a>

## 1. 记忆策略属于运行层，记忆数据库不属于运行层

这一章回答哪些信息值得未来再次使用。L2 决定何时写、何时读、如何更新和失效；L3 提供受控存取接口；L4 保存记录及索引。这是一项跨层能力的职责分解，不是三个互相重复的 Memory 模块。

### 先把 Context / Memory / State / History 分开

这是整个 Agent Runtime 最重要的边界之一：

```text
Context
= 当前这一次模型调用能看到什么

Memory
= 为未来再次取回而保存的信息

State
= Runtime 当前执行事实

History
= 已经发生的 message / event 记录

Checkpoint
= 可以恢复执行的位置与状态快照/引用
```

所以：

```text
Chat History ≠ Memory
Memory ≠ State
State ≠ Context
```

它们可以互相投影，但不是一个概念。

### Memory 为什么不能“什么都存”

如果所有历史都永久保存：

```text
Token / Storage ↑
Noise ↑
Contradiction ↑
Retrieval Cost ↑
Stale Fact ↑
Privacy Risk ↑
```

最终会得到一个“信息坟场”。

Memory 需要一个生命周期：

```text
Observe
→ Decide whether to remember
→ Extract / Normalize
→ Validate
→ Store
→ Retrieve on demand
→ Update / Consolidate
→ Expire / Correct / Delete
```

### Memory 可以怎样分层

课程层常见的实用划分：

#### Working Memory

当前任务正在使用的信息：

```text
current goal
current plan
active constraints
recent tool evidence
```

它通常更接近 Runtime State / Current Context。

#### Episodic Memory

发生过的事件：

```text
上次部署失败的原因
用户上一次确认过的选择
某次 incident 的处理结果
```

#### Semantic Memory

较稳定事实：

```text
用户偏好
项目架构
组织规范
领域知识摘要
```

#### Procedural Memory

“怎么做”的程序性知识：

```text
部署步骤
排障 SOP
代码修改规范
```

在某些系统里它更接近 Skill / Instruction，而不是普通向量 Memory。

这只是课程抽象，不声称 Claude Code / Codex 使用完全相同的四类命名。

<a id="part-2"></a>

## 2. 选择、提取、写入与按需召回

把长期记忆作为有来源、作用域和生命周期的信息资产，不把所有聊天自动永久存入向量库。

### 什么时候应该写 Memory

不建议：

```text
每个 turn 结束
→ 把整段 conversation embedding 一遍
→ 永久存储
```

更合理的是定义 Write Policy：

```text
stable fact?
future value?
user consent / privacy allowed?
already known?
confidence enough?
expires?
```

例如：

```text
“我今天有点累”
```

通常不应该自动晋升长期 Memory。

而：

```text
“这个项目所有 Python 服务统一用 uv 管理依赖”
```

可能更适合持久化。

### Extraction：从对话变成 Memory Record

不要直接把自然语言聊天原文当长期 Memory 唯一结构。

可以抽成：

```python
MemoryRecord(
    id="mem_123",
    kind="project_fact",
    subject="dependency_manager",
    value="uv",
    source_event_id="evt_456",
    confidence=0.96,
    version=3,
    created_at=...,
    expires_at=None,
)
```

这样后续才容易：

```text
去重
更新
冲突检测
版本化
删除
审计来源
```

### Retrieval-on-demand 为什么比“全量注入”更重要

Memory Store 可能有十万条记录。

每次都塞进 Context：

```text
不可行
```

因此：

```text
Current Task / Query
→ Memory Retrieval
→ Relevant Memory
→ Context Assembly
```

这和 RAG 有相似性，但对象不同：

```text
RAG 主要检索外部知识证据
Memory 主要检索 Agent / User / Task 历史沉淀
```

二者的权限、更新和正确性标准也可能不同。

### Memory Consolidation 是什么

随着时间推移可能出现：

```text
mem1: 用户喜欢简洁回答
mem2: 用户偏好先给结论
mem3: 用户不希望长篇背景
```

可以合并成更稳定的 higher-level memory：

```text
response_style = concise / conclusion-first
```

但 Consolidation 不能把来源和版本完全抹掉，否则错误后无法追踪。

推荐保留：

```text
derived_from = [mem1, mem2, mem3]
```

<a id="part-3"></a>

## 3. 纠错、冲突与失效是核心机制

记忆是一份可被纠正的历史表示，不是现实世界的最终权威。

### Memory Correctness：错误事实比“没有记住”更危险

`AGENT-016` 直接追问过期摘要、错误事实和冲突信息。

例如：

```text
Memory v1: production DB = mysql-prod-a
后来迁移：production DB = mysql-prod-b
```

如果旧 Memory 仍被召回：

```text
Agent 可能操作错误环境
```

所以 Memory 必须支持：

```text
version
valid_from / valid_to
superseded_by
source
confidence
```

对于高风险事实，最好优先从 Source of Truth 重新验证，而不是只信长期 Memory。

### Memory Conflict 怎么处理

假设：

```text
Memory A: deploy branch = main
Memory B: deploy branch = release
```

不能直接随机挑一个。

可以：

```text
compare timestamp
compare source authority
check project scope
ask user
query Source of Truth
```

Runtime 还应该能记录：

```text
conflict unresolved
```

而不是强行“总结成一个答案”。

### Memory Staleness / Expiration

有些 Memory 天生有 TTL：

```text
临时 feature flag
临时 incident status
短期用户任务偏好
```

有些是版本驱动：

```text
repository architecture
API contract
team policy
```

所以 Memory 失效策略可以包括：

```text
TTL
Source version mismatch
Explicit invalidation
Superseded-by
Low confidence decay
Manual correction
```

### Memory Failure Timeline

```text
T0  User 说：部署用 branch=main
T1  Runtime 写长期 Memory
T2  项目迁移到 release branch
T3  Source of Truth 更新
T4  Memory 没失效
T5  两周后 Agent 召回旧 Memory
T6  Agent 尝试操作 main
```

根因不是：

```text
Vector DB 召回不准
```

而是：

```text
Memory Lifecycle 缺少 Version / Invalidation
```

<a id="part-4"></a>

## 4. 记忆的安全与验收

保存和使用信息都要满足用户、租户与项目边界；召回后仍需依据任务风险验证其适用性。

### Privacy / Tenant Boundary

Memory 往往包含高敏感上下文：

```text
user preference
workspace information
internal project data
credential-related metadata
```

因此必须在 Key / Namespace / Query Filter 层绑定：

```text
tenant_id
user_id
workspace_id
agent_scope
```

不能只靠 Prompt 里写：

> “请不要读别人的 Memory。”

真正的隔离要在存储 / Query 层 enforce。

### 高频易错点

⚠️ **Memory = Vector DB。** Vector DB 只是可能的存储/检索组件。

⚠️ **Chat History 全存就是 Memory。** 这会制造噪声和陈旧事实。

⚠️ **Long-term Memory 永久有效。** Production 必须考虑失效和冲突。

⚠️ **Memory 召回结果默认可信。** 高风险事实应重新验证 Source of Truth。

## 用一个记录推演纠错，而不是“再加一句忽略之前”

文件报告任务里，`目录A只读`是当前授权约束，应来自契约/策略，不应只存成可以被召回排名改变的Memory。`用户偏好按主题组织报告`则可能是未来可复用的记忆候选。

```text
m1: preference=按日期组织, source=用户此前确认, version=1
m2: preference=按主题组织, source=用户本次纠正, supersedes=m1
```

写入m2后，读取路径必须排除已失效的m1，缓存/向量索引也要最终对齐有效版本。只在新Prompt里说“忽略旧偏好”不能阻止下一次检索再次召回m1。

检验要覆盖错误偏好纠正、租户隔离、删除后不再召回和冲突未决；来源权威性及适用范围优先于单个相似度或模型置信度。与真实业务系统冲突时回查权威事实。

既有Claude Code索引记录了 `memdir/memdir.ts` 的memory prompt和 `loadedNestedMemoryPaths` 去重线索；它支持“Memory是Context来源之一”，**不支持凭空断言其完整写入、合并或TTL算法**。详见[已核验与待读范围](../../research/agent-sources/claude-code-source-index.md)。

## 本章自测

<details>
<summary>Memory 为什么不是把 History 全部存起来？</summary>

Memory 是为未来复用选择并维护的信息，具有来源、作用域、版本和失效策略；History 是发生过的记录。

</details>

<details>
<summary>模型召回的记忆与真实系统冲突怎么办？</summary>

核对来源、版本和适用范围，必要时重新查询权威系统、保留未决状态并纠正过期记忆。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>更新Memory但检索索引未更新会怎样？</summary>

旧记录可能继续被召回；读取端须核对有效版本/失效标记，并使派生索引和缓存最终对齐。

</details>

<details>
<summary>相似度最高的Memory可以覆盖当前审批吗？</summary>

不能；权限来自可信契约与执行策略，Memory不能产生授权。

</details>

## 回到主线

现在应能独立说明：记忆读写、来源、更新与失效策略。下一章：[L2 运行层：执行状态、持久化与恢复](07-StateAndRecovery.md)。

对应真人问题：`AGENT-014`、`AGENT-015`、`AGENT-016`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 05](05-ContextEngineering.md) · [Agent 主线](../README.md) · [07 →](07-StateAndRecovery.md)
