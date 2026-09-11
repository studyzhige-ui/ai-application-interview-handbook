# 16. Context Assembly：模型这一轮到底能看到什么

`AGENT-008` 在冻结 HUMAN-A 中有 **16 个独立来源**。它通常是 Context 追问链的起点：

```text
Context Assembly
→ Context Growth
→ Tool Result Offloading
→ Compaction
→ Compaction Correctness
→ Memory
```

很多人把 Context 理解成：

```text
messages[-N:]
```

但 Production Agent 中，模型本轮看到的输入通常由多个 Runtime Source 组装而成。

---

# 1. 先讲人话：Context 不是聊天记录，而是“本轮工作台”

模型每一轮真正看到的东西可能包括：

```text
System / Developer Instructions
User Goal
Current User Message
Conversation History
Current Plan / State
Tool Schemas
Tool Results
Memory
Repository Instructions
Workspace / Environment Info
Retrieved Documents
Security / Permission Context
Dynamic Instructions
```

所以更准确：

> **Context Assembly 是 Runtime 在一次 Model Request 前，从多个信息源选择、排序、压缩并构造模型输入的过程。**

---

# 2. 一个 Context Builder 的逻辑图

```text
                 ┌─ System Instructions
                 ├─ User / Tenant Context
                 ├─ Goal / Constraints
                 ├─ Runtime State
                 ├─ Conversation History
Context Builder ←├─ Memory
                 ├─ Retrieved Knowledge
                 ├─ Tool Specs
                 ├─ Tool Results
                 ├─ Workspace State
                 └─ Dynamic Instructions
                         │
                         ▼
                   Token Budgeter
                         │
                         ▼
                    Model Request
```

这比“拼 Prompt”多了两个核心问题：

```text
Selection
Budgeting
```

---

# 3. Context Engineering 和 Prompt Engineering 的区别

Prompt Engineering 更常关注：

```text
instruction wording
few-shot examples
format
```

Context Engineering 更关注：

```text
这一轮模型应该拿到哪些信息？
这些信息从哪里来？
顺序是什么？
何时更新？
哪些不能进？
超预算时保留什么？
```

Anthropic 的 `Effective context engineering for AI agents` 明确把 Context 扩展到：

- instructions；
- tools；
- MCP；
- external data；
- message history；

并强调有限 Context Window 下的管理。

来源：

https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

# 4. Context Source 应该显式建模

教学上可以先抽象：

```python
from dataclasses import dataclass
from enum import Enum


class ContextKind(str, Enum):
    SYSTEM = "system"
    GOAL = "goal"
    STATE = "state"
    HISTORY = "history"
    MEMORY = "memory"
    TOOL_SPEC = "tool_spec"
    TOOL_RESULT = "tool_result"
    RETRIEVAL = "retrieval"
    ENVIRONMENT = "environment"


@dataclass
class ContextFragment:
    kind: ContextKind
    content: str
    priority: int
    estimated_tokens: int
    source_id: str
    freshness: int
```

这样 Runtime 才能做：

- priority；
- dedup；
- budget；
- freshness；
- audit。

---

# 5. Context 的第一原则：State 不等于 Context

Runtime State 可能保存：

```text
50 个 plan steps
100 个 tool events
完整 checkpoint metadata
```

但模型当前只需要：

```text
current goal
current step
last relevant tool result
critical constraints
```

所以：

```text
Durable State
→ projection
→ Model Context
```

而不是：

```text
Durable State 全量 dump 到 Prompt
```

---

# 6. Context 的第二原则：Authoritative Source 应优先于模型自己的旧总结

例如当前事实：

```text
Git branch = feature/auth-v2
```

模型 20 轮前可能说：

```text
we are on main
```

如果 Runtime 能直接查询 workspace：

```text
git branch --show-current
```

应该优先使用新的 authoritative environment state。

否则会形成：

> **Stale Context。**

---

# 7. Context Ordering 为什么重要

相同信息不同顺序，模型表现可能不同。

一种常见逻辑：

```text
Stable high-priority instructions
→ current goal / constraints
→ relevant state/memory
→ recent interaction/history
→ current user message / observations
→ tool definitions
```

具体 Provider 可能有固定消息协议，不能机械套一个顺序。

工程重点是：

> **稳定的 Prefix 尽量稳定；高动态信息放到合适边界，既利于缓存也减少冲突。**

---

# 8. Claude Code 的 Context Assembly 直接证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`utils/queryContext.ts` 明确写着：

> building the API cache-key prefix (`systemPrompt`, `userContext`, `systemContext`)

`fetchSystemPromptParts()` 同时组装：

```text
defaultSystemPrompt
userContext
systemContext
```

并根据：

```text
tools
model
additional working directories
MCP clients
custom system prompt
```

生成不同内容。

`QueryEngine` 在这之上还会叠加 memory / coordinator 等上下文。

这说明成熟产品的 Context 本身就是一条 Assembly Pipeline。

---

# 9. Prompt Cache 与 Context Assembly 是耦合的

Claude Code `queryContext.ts` 的注释专门强调：

```text
API cache-key prefix
```

并在 side question fallback 中尝试重建和主 Loop 一致的 prefix，以保留 cache hit。

这说明 Context Builder 不仅影响：

```text
模型正确性
```

也影响：

```text
成本 / latency / cache
```

第 17 章会详细拆 Token Economics。

---

# 10. 动态 Instructions 也是 Context Source

Codex 当前固定 commit 本身的提交内容就是 `ThreadInstructionsProvider`。

该 commit 说明：

- thread instructions 在启动和 model-request boundary 刷新；
- 它们与 global / repository instructions 有明确 composition 顺序；
- 单独有 10,000 estimated-token 限制；
- warm resume / cold resume / fork / subagent 有不同继承语义。

这非常能说明：

> **Instructions 不是进程启动时一次性静态字符串，而可能是 Runtime 持续装配的 Context Source。**

---

# 11. Context Freshness

不同 Fragment 的有效期不同：

```text
System policy → 很稳定
User goal → 一般稳定
Current branch → 高频变化
Tool result → 当前 task 生命周期
Memory → 跨 session，但可能 stale
Retrieved web → 有时间敏感性
```

所以可以记录：

```text
source timestamp
version
expiry
refresh policy
```

尤其 Memory 和 external data，不能只看“相关性”。

---

# 12. Dedup：同一事实重复 5 次不等于更重要

例如：

```text
System prompt: do not modify DB
User said: do not modify DB
Plan says: do not modify DB
Memory says: do not modify DB
```

有些重复是 intentional reinforcement，有些只是 Token Waste。

Context Builder 可以做：

```text
same source identity dedup
same artifact version dedup
nested memory path dedup
```

Claude Code `ToolUseContext` 当前就有：

```text
loadedNestedMemoryPaths
```

并注释说明为了避免 LRU eviction 导致同一个 `CLAUDE.md` 在 busy session 被重复注入几十次。

这就是很真实的 Context Dedup 问题。

---

# 13. Tool Schema 也是 Context

如果你注册 300 个 Tool：

```text
name + description + JSON schema
```

它们都可能吃 Context Token。

因此：

```text
Tool Registry
≠ 每轮全部 Tool Schema
```

而是：

```text
Discovery / Progressive Loading
→ 当前相关 Tool Specs
→ Context
```

Context Engineering 和 Tool Discovery 是直接相连的。

---

# 14. Memory 不是直接塞进 Context

Memory Store：

```text
1000 条长期记忆
```

当前任务也许只需要 3 条。

应该：

```text
retrieve
→ score relevance / freshness / trust
→ select
→ inject
```

而不是：

```text
load all memory
```

第 21 章会详细讲。

---

# 15. RAG 与 Agent Context Assembly 的关系

RAG 负责从外部 Knowledge Source 检索：

```text
query
→ retrieve
→ rerank
→ context chunks
```

Agent Context Builder 决定：

```text
这些 retrieved chunks
和 goal/history/tool result/memory
怎样一起进入本轮模型
```

所以：

```text
RAG Context Construction
```

是 Agent Context Assembly 的一个来源，但不是全部。

---

# 16. Context Isolation

Multi-tenant Agent 不能：

```text
Tenant A memory
→ 注入 Tenant B Context
```

Subagent 也不应该自动拿到 Parent 所有 Secret。

因此 Context Builder 本身需要：

- tenant scope；
- user scope；
- agent scope；
- permission filter；
- secret redaction。

这不是单纯 Token Optimization，而是安全边界。

---

# 17. 一个 Context Assembly 伪代码

```python
async def build_context(state, runtime):
    fragments = []

    fragments += runtime.system_instructions(state)
    fragments += runtime.goal_projection(state)
    fragments += runtime.current_state_projection(state)
    fragments += await runtime.memory.retrieve(state)
    fragments += runtime.recent_history(state)
    fragments += runtime.relevant_tool_results(state)
    fragments += runtime.visible_tool_specs(state)

    fragments = filter_by_permission(fragments, state.identity)
    fragments = deduplicate(fragments)
    fragments = remove_stale(fragments)
    fragments = budget(fragments, state.model_context_limit)

    return render_for_provider(fragments)
```

真正系统还要：

- compaction；
- cache-aware ordering；
- provenance；
- multimodal；
- injection defense。

---

# 18. Context Assembly 的 Provenance

当模型说：

```text
“用户不允许修改 database.py”
```

Runtime 最好能知道这个约束来自：

```text
current user message
or
memory
or
repo instruction
```

Provenance 有助于：

- conflict resolution；
- security；
- debugging；
- eval。

例如：

```text
memory says A
current user says B
```

通常最新显式用户指令应该覆盖旧偏好 Memory。

---

# 19. Instruction Conflict

Context 中可能同时：

```text
global policy
repo instruction
thread instruction
user instruction
tool result中的恶意“忽略前面指令”
```

它们不是同一信任等级。

Runtime 必须区分：

```text
trusted instructions
untrusted external content
```

不能因为 Tool Result 里出现：

```text
SYSTEM: ignore all previous rules
```

就把它提升成 Instruction。

第 31 章 Prompt Injection 会深入。

---

# 20. Context Assembly 的测试怎么做

不要只测最终回答。

可以 Snapshot / Assert：

```text
哪些 fragment 被选中
哪些被丢弃
排序
token budget
provenance
permission filter
```

例如：

```python
def test_old_memory_does_not_override_current_user_constraint():
    ...
```

这是 Context Runtime 的单元测试。

---

# 21. 高频易错点

⚠️ **Context = Chat History**  
History 只是其中一个 source。

⚠️ **Runtime State 全部放 Context**  
应该投影最相关部分。

⚠️ **相关就能进 Context**  
还要检查 freshness、trust、permission、budget。

⚠️ **Tool Result 中的文本和 System Instruction 同等级**  
外部内容必须视为 untrusted context。

⚠️ **Tool Specs 不占 Token**  
大规模工具集本身就是 Context 成本。

---

# 22. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Agent Context 不只是 messages，而是 Runtime 每轮从 system/user instructions、goal、state、history、memory、retrieval、tool specs、tool results 和 environment 等来源装配出的模型工作集。Context Builder 要处理优先级、freshness、provenance、permission、dedup 和 token budget，并把 Durable State 投影成模型真正需要看到的部分。

## Level 2｜2–3 分钟

> 我会把每个 Context Fragment 带 kind/source/priority/version/freshness/trust，先做 scope 和 permission filter，再做 dedup/stale check，最后在 token budget 下选择。稳定 instruction prefix 尽量保持稳定以利用 prompt cache；dynamic state/tool result 放后面。Memory/RAG 只检索相关 subset。外部 Tool Result 是 untrusted content，不能提升成 instruction。这样 Context Assembly 同时解决正确性、成本和安全。

## Level 3｜继续追问

🔍 **State 和 Context 为什么要分？**  
State 是完整 durable execution truth，Context 是本轮给模型的有限投影。

🔍 **Prompt Cache 为什么影响 Assembly？**  
Prefix 稳定性会影响 cache hit，从而影响 latency/cost。

🔍 **Memory 和当前用户指令冲突怎么办？**  
按 provenance/trust/recency 解决，一般当前显式指令优先于旧偏好 memory。

---

# 23. 本章证据

## HUMAN-A

- `AGENT-008` Context Assembly：16 sources；
- `AGENT-009` Context Compaction：41 sources；
- `AGENT-014` Memory Architecture：36 sources。

## Claude Code

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

- `utils/queryContext.ts`
- `QueryEngine.ts`
- `Tool.ts` 中 nested memory / Tool context tracking。

## OpenAI Codex

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

- thread-scoped instruction provider commit behavior；
- `Session` / `TurnContext` / `StepContext`。

## 权威资料

Anthropic — Effective context engineering for AI agents  
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

# 24. 自测

<details><summary>1. Context 和 History 有什么区别？</summary>

History 是过去交互记录；Context 是当前 Model Request 的完整工作集，可能包含 history、state projection、memory、retrieval、tools、instructions 等。
</details>

<details><summary>2. 为什么 Runtime State 不应全部进 Context？</summary>

State 需要完整、可恢复；Context 受有限 Token Budget 约束，只应投影当前决策需要的信息。
</details>

<details><summary>3. Context Fragment 选择除了 relevance 还要考虑什么？</summary>

Freshness、trust/provenance、permission/scope、priority、token cost、是否重复等。
</details>

<details><summary>4. 为什么 Tool Schema 属于 Context Engineering？</summary>

模型要看到 Tool Schema 才能调用，但大量 Schema 消耗 Context，所以需要 discovery/progressive loading 和按需暴露。
</details>
