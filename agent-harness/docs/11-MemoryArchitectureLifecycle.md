# 11. Memory Architecture、Lifecycle 与 Correctness

Agent 一旦跨多轮、多任务运行，就会遇到一个经典问题：

> **哪些信息应该被“记住”，记多久，什么时候再取回来？**

如果回答只是：

> “把聊天记录存进 Vector DB。”

那还没有真正进入 Agent Memory Engineering。

Memory 的核心不是“有个数据库”，而是：

```text
什么值得写？
写成什么形式？
什么时候召回？
怎样更新？
什么时候过期？
错误 Memory 怎么纠正？
```

---

## 1. 先把 Context / Memory / State / History 分开

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

---

# 2. Memory 为什么不能“什么都存”

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

---

# 3. Memory 可以怎样分层

课程层常见的实用划分：

## 3.1 Working Memory

当前任务正在使用的信息：

```text
current goal
current plan
active constraints
recent tool evidence
```

它通常更接近 Runtime State / Current Context。

## 3.2 Episodic Memory

发生过的事件：

```text
上次部署失败的原因
用户上一次确认过的选择
某次 incident 的处理结果
```

## 3.3 Semantic Memory

较稳定事实：

```text
用户偏好
项目架构
组织规范
领域知识摘要
```

## 3.4 Procedural Memory

“怎么做”的程序性知识：

```text
部署步骤
排障 SOP
代码修改规范
```

在某些系统里它更接近 Skill / Instruction，而不是普通向量 Memory。

这只是课程抽象，不声称 Claude Code / Codex 使用完全相同的四类命名。

---

# 4. 什么时候应该写 Memory

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

---

# 5. Extraction：从对话变成 Memory Record

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

---

# 6. Retrieval-on-demand 为什么比“全量注入”更重要

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

---

# 7. Memory Consolidation 是什么

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

---

# 8. Memory Correctness：错误事实比“没有记住”更危险

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

---

# 9. Memory Conflict 怎么处理

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

---

# 10. Memory Staleness / Expiration

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

---

# 11. Privacy / Tenant Boundary

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

多租户 State 下一章继续。

---

# 12. Claude Code 固定源码侧的证据

Claude Code Source Index 已确认：

- `QueryEngine` 会加载 `memdir/memdir.ts` 的 memory prompt；
- Tool context 维护 `loadedNestedMemoryPaths`，避免 nested memory 重复注入；
- session / context / memory 是不同 Runtime 路径。

这支持：

> **Memory 是 Context Source，但不等于整个 Context。**

索引还明确建议后续阅读 `memdir/*` 继续研究具体生命周期；因此本章不会凭空宣称 Claude Code 的具体写入算法。

---

# 13. HUMAN-A 信号

本章主要承接：

- `AGENT-014` Memory Architecture：36 个独立来源；
- `AGENT-015` Memory Lifecycle：8 个；
- `AGENT-016` Memory Correctness / Staleness：6 个。

真人面试已经从：

```text
“Memory 怎么做？”
```

深入到：

```text
什么时候晋升长期？
怎么更新？
错了怎么办？
过期怎么办？
```

---

# 14. Memory Failure Timeline

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

---

# 15. 面试怎么答

## Q：Agent Memory 怎么设计？

🎯 **30 秒回答**：

> 我会先把 Memory 和 Context、State、History 分开。Memory 不是全量聊天记录，而是经过 write policy 选出的、未来有价值的信息。写入时做 extraction、去重、来源和版本记录；使用时按当前任务 retrieval-on-demand；长期还要支持 consolidation、TTL、supersede、conflict 和人工 correction。高风险事实不能只信 Memory，要能回 Source of Truth 验证。多用户场景还要在存储与查询层绑定 tenant/user/workspace 隔离。

## Q：Memory 错了怎么办？

> Memory Record 要有 source、version、confidence、validity 和 superseded-by 之类元数据；发生冲突时按来源权威性和版本验证，必要时查询 Source of Truth 或让用户确认，并把旧 Memory 显式失效，而不是只在 Prompt 里追加一句“忽略之前的内容”。

---

# 16. 高频易错点

⚠️ **Memory = Vector DB。** Vector DB 只是可能的存储/检索组件。

⚠️ **Chat History 全存就是 Memory。** 这会制造噪声和陈旧事实。

⚠️ **Long-term Memory 永久有效。** Production 必须考虑失效和冲突。

⚠️ **Memory 召回结果默认可信。** 高风险事实应重新验证 Source of Truth。

---

# 17. 本章自测

<details><summary>1. 为什么 Memory 不应该等于完整 History？</summary>

History 是发生过的事件记录；Memory 是为未来价值而选择、提取、维护的信息。两者生命周期和检索目标不同。
</details>

<details><summary>2. Memory Consolidation 为什么必须保留来源？</summary>

因为 higher-level memory 可能总结错误。保留 derived_from/source 才能审计、纠错和重新计算。
</details>

<details><summary>3. 为什么高风险事实不应该只依赖 Memory？</summary>

Memory 可能过期或错误；生产数据库、权限、付款状态等高风险事实应尽量回 Source of Truth 做实时验证。
</details>
