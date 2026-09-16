# 05. L2 运行层：上下文组装、预算与压缩

[← 04](04-AgentLoopAndControl.md) · [Agent 主线](../README.md) · [06 →](06-MemoryLifecycle.md)

> 主线位置：**L2 运行层**。循环需要每步输入；先解决当前该给模型看什么。
>
> 本章产物：**上下文编译、预算与压缩的正常/失败路径**。

[Context Manager 管的是当前模型可见信息](#part-1) → [从来源到可调用的上下文](#part-2) → [先处理增长，再考虑压缩](#part-3) → [Compaction 是上下文管理机制](#part-4) → [验证继续执行是否仍然正确](#part-5)

<a id="part-1"></a>

## 1. Context Manager 管的是当前模型可见信息

运行层现在需要决定每一步给模型看什么。上下文只是当前模型输入，不是全部历史、全部执行状态或全部业务事实。Prompt 是其中的指令部分；RAG 与 Memory 可以提供材料；Context Manager 选择与组织这些材料。

可以把输入表示为带 source、version、scope、trust、priority 和 token estimate 的片段。权限过滤和可信指令边界先于相关性排序，不能因为一段外部文本“很相关”就把它升级成系统指令。

<a id="part-2"></a>

## 2. 从来源到可调用的上下文

先选择与规范化，再排序、去重、分配预算，最后编码为模型接口支持的消息。

### 一次 Agent Context 可能来自哪些 Source

常见来源：

```text
System / Runtime Instructions
User Request
Recent Conversation History
Current Goal / Plan / Constraints
Working State
Relevant Memory
RAG Evidence
Tool Schema
Loaded Skills / MCP Capability
Tool Result
Workspace / File Snapshot
Permission / Environment Metadata
```

但这些来源的优先级、稳定性和预算完全不同。

可以粗分：

```text
Stable Prefix
Dynamic Task Context
Ephemeral Observation
External Artifact Reference
```

### Context Assembly 应该是“Compiler”，不是字符串拼接

推荐把每类输入建模成结构化单元：

```python
@dataclass
class ContextItem:
    kind: str
    content: str
    priority: int
    token_cost: int
    source_id: str
    version: str | None
    expires_at: float | None
```

然后：

```text
collect sources
→ normalize
→ permission filter
→ deduplicate
→ score priority
→ enforce budget
→ render provider-specific messages
```

这样 Runtime 才能回答：

```text
为什么这段内容被放进去？
为什么另一段被丢掉？
它来自哪个版本？
它什么时候过期？
```

### Assembly Order 为什么重要

不同 Provider / Model 的具体行为会变，但工程上仍需要一个稳定策略。

例如：

```text
1. Stable Runtime Instruction
2. Security / Policy Boundary
3. Current Goal + Constraints
4. Latest User Request
5. Selected History
6. Relevant Memory / Retrieval
7. Tool / Skill Capability
8. Recent Tool Observation
9. Output Contract
```

这里不是说所有模型都必须使用这个固定顺序，而是强调：

> **Context 顺序应该是显式设计，不是 Dict / List 的偶然遍历结果。**

### Token Budget 要分区，而不是统一“还剩多少”

假设 Model Context = 128k。

不能简单：

```text
把东西一直塞到 128k
```

因为还要为输出、Tool Result、后续 Turn 和 Compaction 留空间。

可以按类别设置软预算：

```text
Instructions      10k
Goal / State       8k
Recent History    20k
Memory / RAG      30k
Tool Definitions  20k
Tool Results      20k
Reserve Output    20k
```

数字只是示意，真正值要结合模型和任务。

重要思想：

> **不同 Context Source 应有不同 Budget 和退化策略。**

### Context Dedup 为什么重要

相同信息可能同时存在于：

```text
System Prompt
Memory
RAG
Recent History
Tool Result
```

重复并不是免费：

- 增加 Token；
- 放大某些信息权重；
- 让模型误以为重复事实更重要；
- 降低 Cache 稳定性。

所以 Runtime 可以对：

```text
source_id
content hash
artifact id
memory id
```

做去重。

Claude Code 索引里 `loadedNestedMemoryPaths` 用来避免某些 nested memory 重复注入，也支持这个课程方向。

<a id="part-3"></a>

## 3. 先处理增长，再考虑压缩

大量工具输出应保留可重新读取的产物引用。截断、外部化和缓存解决不同问题，不能互相冒充。

### Large Tool Result 为什么不能直接塞回 Context

例如：

```text
cat 5MB log
run test → 30,000 lines
search repository → 5,000 matches
```

如果 Tool Result 原样回填：

```text
Context 爆炸
→ 成本上升
→ Noise 上升
→ Compaction 提前触发
→ 甚至把真正重要状态挤掉
```

更成熟的策略：

```text
Tool produces artifact
        ↓
Runtime persists full result externally
        ↓
Context only keeps:
- summary
- artifact id/path
- metadata
- selected relevant excerpt
```

Claude Code 的 `utils/toolResultStorage.ts` 索引明确用于：

> 持久化 large tool results，而不是不可逆地直接截断。

因此课程抽象是：

```text
Large Result
→ Offload
→ Reference
→ Selective Rehydrate
```

### Offloading 和 Truncation 有什么区别

错误做法：

```text
result[:5000]
```

问题：

```text
后面重要错误被直接丢掉
而且无法恢复
```

更好的做法：

```text
Full Artifact 保存
+ Context 中放摘要 / 索引 / 指针
```

如果后续需要：

```text
read artifact range
search artifact
load relevant section
```

这就是可恢复的 Context Offloading。

### Prompt / Context Cache 应该缓存什么

`AGENT-012` 关注 Prompt / Context Cache。

缓存最适合：

```text
稳定、重复、可版本化的 Prefix
```

例如：

```text
System Instructions
Stable Tool Schema Set
Stable Policy
Repository Instruction Snapshot
```

不适合长期缓存：

```text
Current User Request
Latest Tool Result
Mutable Runtime State
Short-lived Permission
```

缓存 Key 至少需要考虑：

```text
model/provider
instruction version
tool schema version
policy version
tenant / workspace boundary
```

否则可能发生：

```text
旧 Context 被错误复用
```

<a id="part-4"></a>

## 4. Compaction 是上下文管理机制

压缩的目标是支持后续执行，而不是写一篇漂亮摘要。关键状态必须能从持久记录恢复；不能只有摘要里保留唯一业务回执。

### Compaction 为什么存在

随着 Agent 运行：

```text
User Message
Assistant Message
Tool Call
Tool Result
Plan
Memory
RAG Evidence
File Content
Error / Retry
```

不断累积。

如果不处理：

```text
Token ↑
Cost ↑
Latency ↑
Noise ↑
最终超过 Context Window
```

即使窗口足够大，也不代表应该无限保留：

> **Long Context Capacity ≠ 无限有效注意力 ≠ 免费存储。**

### Compaction 与普通 Summary 的区别

普通 Summary 只关心：

```text
把长文本变短
```

Runtime Compaction 还必须关心：

```text
当前 Goal 还在吗？
约束还在吗？
已经完成什么？
哪些 Tool Side Effect 已发生？
当前 Workspace / Artifact 在哪里？
有哪些 unresolved problem？
哪些 approval 已经给过？
哪些状态不能重复执行？
```

所以正确抽象是：

```text
Compaction
= Select
+ Summarize / Project
+ Preserve Invariants
+ Build Replacement History
+ Persist
+ Recompute Budget
+ Trace / Validate
```

### Compaction 什么时候触发

常见触发可以分：

#### Token Threshold

```text
estimated_context_tokens > soft_limit
```

提前压缩，而不是等 Provider 报 `context_length_exceeded`。

#### Phase Boundary

例如：

```text
一个大 Task 完成
→ 切换到下一个阶段
```

此时适合把“旧阶段的过程细节”压成阶段结论。

#### Tool Result Pressure

大量日志 / 文件 / Search Result 造成 Context 激增。

这时优先：

```text
Offload / Reference
```

不一定马上压整个 Conversation。

### 哪些信息必须保留

建议至少定义一个 Compaction Invariant Set。

##### Goal / Acceptance

```text
当前主目标
完成标准
禁止事项 / Constraints
```

##### Runtime Progress

```text
已经完成的步骤
当前进行到哪里
下一步候选
Blocked 原因
```

##### Side-effect Ledger

```text
Tool X 已经写 DB
Tool Y 已经发送消息
Payment request 已提交 idempotency_key=...
```

这类信息丢失会导致 Resume 后重复副作用。

##### Artifact References

```text
修改过哪些文件
日志 artifact 在哪里
测试结果 path / id
```

##### Unresolved Evidence

```text
哪些假设未验证
哪些测试仍失败
哪些用户问题未回答
```

### 哪些内容适合压缩或外部化

例如：

```text
重复 Tool Schema
大量 raw log
已经完成阶段的逐步对话
旧搜索结果
可通过 artifact id 重新取回的文件
```

原则：

> **丢过程之前先确认能否重建。**

如果某个结果无法再次获取，又会影响后续决策，就不能只留一句模糊 Summary。

### Replacement History 为什么重要

一种危险做法：

```text
old history
+ summary message
```

这样旧内容仍然占 Context，根本没有真正压缩。

另一种危险做法：

```text
history = [summary]
```

但 Summary 丢失了 System / Current User Goal / Tool Correlation。

更合理的是：

```text
Stable Instructions
+ Required Current State
+ Compact Summary
+ Recent High-value Events
+ Artifact References
```

形成新的 Replacement View。

这也解释了为什么 Codex `compact.rs` 会专门处理 replacement history，而不是只生成一个文本字段。

<a id="part-5"></a>

## 5. 验证继续执行是否仍然正确

检查压缩后的结构、语义和后续行为。缓存命中或 token 下降不等于上下文质量提升。

### Compaction Correctness 怎样验证

`AGENT-010` 直接问：

> Summary 后如何验证信息没有丢坏？

至少可以分四层。

#### Structural Invariant

例如：

```text
current_goal exists
current_task_id exists
pending_steps preserved
side_effect_ledger preserved
artifact refs resolvable
```

#### Semantic Invariant

把压缩前关键事实做成 checklist：

```text
Constraint A still present?
Decision B still present?
Failure C still unresolved?
```

#### Continuation Test

同一个 Agent 从：

```text
Before Compaction Context
```

和：

```text
After Compaction Context
```

继续执行，检查关键下一步是否一致。

#### Regression Eval

建立长任务数据集：

```text
run without compaction
vs
run with compaction
```

比较：

```text
Task Success
Wrong Re-execution
Missed Constraint
Cost
Latency
```

### Compaction 失败怎么办

Compaction 自己也可能失败：

```text
summary model timeout
summary too long
provider context error
persistence failure
hook failure
```

不应该：

```text
原 history 已删
→ compaction failed
→ session destroyed
```

更稳的流程：

```text
1. Build compact candidate
2. Validate candidate
3. Persist replacement / metadata
4. Atomically switch active view
5. Keep prior generation for rollback
```

这是课程层的通用设计建议，不声称 Claude Code / Codex 恰好按这个五步实现。

### Stale Context 是另一类问题

Context 不超限，也可能坏。

例如：

```text
文件已经修改
但 Context 里还是旧文件内容
```

或者：

```text
用户已撤销某个约束
旧 Summary 仍说“必须遵守”
```

所以 Context Item / Summary 最好携带：

```text
source
version
timestamp / generation
```

当底层事实更新：

```text
invalidate / refresh / rehydrate
```

### Summary Error 会产生“压缩后的错误记忆”

错误摘要很危险，因为它会变成新的高权重事实。

例如原始 History：

```text
User: 不要改数据库
Agent: 好的
```

Summary 错写：

```text
用户允许修改数据库 schema
```

后续模型可能稳定执行错误行为。

因此高风险 Constraint 应尽量：

```text
结构化持久化
```

而不是只存在自然语言 Summary。

### Compaction 和 Memory 的边界

不要把两者混成：

```text
Compaction Summary = Long-term Memory
```

Compaction 目标：

```text
让当前 Run 在有限 Context 内继续
```

Memory 目标：

```text
让未来 Run / Future Turn 可以重新取回有价值信息
```

二者可以共享提取结果，但生命周期、写入标准和失效标准不同。

### Context Assembly Failure Timeline

```text
T0  Tool 返回 100k tokens 日志
T1  Runtime 全量塞进 History
T2  下一轮 Context 接近窗口上限
T3  早期 Goal / Constraint 被裁掉
T4  模型仍看到大量日志噪声
T5  Agent Goal Drift
T6  自动 Compaction 生成不完整摘要
```

根因不是单纯：

```text
Context Window 太小
```

而是：

```text
Assembly / Budget / Offloading 没设计好
```

## 本章自测

<details>
<summary>Compaction 为什么不能替代持久化？</summary>

它管理当前模型可见信息，可能有损；审批、回执、进度等恢复事实需要独立保存。

</details>

<details>
<summary>怎样验证压缩有效？</summary>

同时检查结构不变量、关键语义、后续执行表现、错误恢复和回归指标，而不只看节约 token。

</details>

## 回到主线

现在应能独立说明：上下文编译、预算与压缩的正常/失败路径。下一章：[L2 运行层：记忆的选择、使用与维护](06-MemoryLifecycle.md)。

对应真人问题：`AGENT-008`、`AGENT-009`、`AGENT-010`、`AGENT-011`、`AGENT-012`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 04](04-AgentLoopAndControl.md) · [Agent 主线](../README.md) · [06 →](06-MemoryLifecycle.md)
