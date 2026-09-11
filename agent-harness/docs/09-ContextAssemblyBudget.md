# 09. Context Assembly、Budget、Cache 与 Tool Result Offloading

Agent Runtime 每次调用模型前都要回答一个问题：

> **这一次模型到底应该看到什么？**

这就是 Context Assembly。

如果把它理解成：

```text
System Prompt
+ 全部 Chat History
```

会很快在 Production 里遇到：

- Context Window 爆满；
- 旧信息污染当前任务；
- Tool Result 巨大；
- 权限和 Tenant 信息混入错误请求；
- Prompt Cache 命中率差；
- Context 成本不可控；
- 同一事实被重复注入。

所以成熟 Harness 的 Context 不是“聊天记录”，而是：

> **Runtime 为当前 Model Call 编译出来的一次性输入视图。**

---

## 1. Context、Memory、State、History 先分清

```text
Context
= 当前这一次模型调用真正看见的内容

Memory
= 可以在未来被再次取回的信息

State
= Runtime 当前执行事实

History
= 已经发生过的 message / event 记录
```

因此：

```text
History 很长
≠ Context 必须全部包含 History

Memory 存在
≠ 每次都注入全部 Memory

State 持久化
≠ 全部 State 都应该变成自然语言 Prompt
```

Context Assembly 的本质就是：

```text
从多种来源中选择
→ 排序
→ 去重
→ 裁剪
→ 编译成模型可消费输入
```

---

# 2. 一次 Agent Context 可能来自哪些 Source

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

---

# 3. Context Assembly 应该是“Compiler”，不是字符串拼接

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

---

# 4. Assembly Order 为什么重要

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

---

# 5. Token Budget 要分区，而不是统一“还剩多少”

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

---

# 6. Claude Code 源码提供了什么实现证据

固定源码索引里，`QueryEngine.ts` 会加载：

- memory prompt；
- session storage；
- system prompt parts；
- file history；
- plugin / skill 相关状态；
- compact / snip 相关能力。

`ToolUseContext` 还显式维护：

```text
loadedNestedMemoryPaths
tool-result budget
content replacement state
dynamic skill discovery
permission decision
```

这支持一个成熟 Runtime 的稳定抽象：

```text
Context
≠ transcript concatenation

Context
= selected runtime projection
```

这里我们只引用索引已核验的源码事实，不把 Claude Code 的具体排序当成所有 Agent 的通用标准。

---

# 7. Large Tool Result 为什么不能直接塞回 Context

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

---

# 8. Offloading 和 Truncation 有什么区别

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

---

# 9. Prompt / Context Cache 应该缓存什么

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

---

# 10. Context Pollution / Stale Context

一个常见失败不是“Context 不够”，而是：

> **Context 太多，而且包含了已经失效的信息。**

例如：

```text
早期 Plan: 修改 A.py
后面已经决定改 B.py

但旧 Plan 仍然在 Context 中高优先级出现
→ 模型反复回到 A.py
```

或者：

```text
旧 permission
旧 file content
旧 dependency version
旧 tool result
```

因此每个 Context Item 都最好能回答：

```text
Source?
Version?
Freshness?
Still relevant?
```

---

# 11. Context Dedup 为什么重要

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

---

# 12. Context Assembly Failure Timeline

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

---

# 13. HUMAN-A 信号

本章主要承接：

- `AGENT-008`：Context Assembly；
- `AGENT-011`：Large Tool Result / Offloading；
- `AGENT-012`：Prompt / Context Cache。

其中真人面经已经把 Context 问题追到 L4：不仅问“Context 包含什么”，还会追“顺序、预算、缓存、超限后怎么办”。

---

# 14. 面试怎么答

## Q：Agent Context 应该怎么组装？

🎯 **建议回答**：

> 我会把 Context 当成 Runtime 为当前 model call 编译出来的 view，而不是把全部聊天历史拼进去。来源通常包括 system/runtime instruction、当前目标与约束、最近 history、相关 memory/RAG、tool schema 和最新 tool result。每类来源设置优先级和 token budget，并记录 source/version/freshness；大 Tool Result 外部化成 artifact，只把摘要和引用放进 Context。这样 Context Assembly 才能做去重、过期控制、缓存和后续 compaction。

## Q：Tool Result 太大怎么办？

> 不优先做不可逆截断，而是完整结果持久化到 artifact store，在 Context 里保留摘要、metadata、引用和少量相关片段，后续需要时再按范围或检索 rehydrate。

---

# 15. 高频易错点

⚠️ **Context = History。** 错，History 只是 Context Source 之一。

⚠️ **Context Window 有 1M，就可以全塞。** 成本、噪声、位置利用和 stale 信息仍然存在。

⚠️ **Tool Result 太大就截前 5k。** 可能不可逆丢失关键证据。

⚠️ **Prompt Cache 只看文本 hash。** 还要考虑模型、工具、策略、Tenant 等版本边界。

---

# 16. 本章自测

<details><summary>1. 为什么 Context 应该被看作 compiled view？</summary>

因为 Runtime 需要从 instruction、history、memory、retrieval、tool、state 等不同来源中选择、排序、去重和预算，最终只生成当前调用需要的输入。
</details>

<details><summary>2. Context Offloading 和 Truncation 有什么区别？</summary>

Offloading 保留完整 artifact，只在 Context 中放摘要/引用，因此可以重新加载；Truncation 直接丢内容，通常不可恢复。
</details>

<details><summary>3. 为什么 Context Cache 需要版本信息？</summary>

因为 instruction、tool schema、policy、provider 都可能变化；没有版本边界会让旧 Prefix 在新运行中被错误复用。
</details>
