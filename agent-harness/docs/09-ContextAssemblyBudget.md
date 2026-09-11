# 09｜Context Assembly、Budget、Cache 与 Tool Result Offloading

> 本章合并旧 `16-ContextAssembly`、`17-ContextBudget*`、`18-ToolResultOffloading`，并纳入 Context Cache。核心问题只有一个：**有限 Context Window 里，这一轮到底给模型看什么。**

## 1. Context 不是 Chat History

一次 Model Call 的 Context 可能包含：

```text
System / Policy
User Goal / Latest Instruction
Current Runtime State
Relevant History
Memory
Retrieval Evidence
Tool Schema
Tool Result / Artifact Reference
Workspace / Environment Context
```

Harness 负责选择、排序、去重和预算。

## 2. Context Assembly 是 Runtime Data Pipeline

```text
Collect sources
→ normalize
→ policy / tenant filter
→ rank by relevance & authority
→ deduplicate
→ budget allocation
→ order / serialize
→ model request
```

顺序会影响模型行为，所以不能把 Context 当成无序字符串池。

## 3. Budget 应按信息类型分层

例如：

```text
hard instructions        15%
current goal/state       10%
recent interaction       20%
retrieved evidence       25%
tool definitions         10%
working artifacts        15%
reserve / output         5%
```

比例不是固定公式，重点是：

> Context Window 是一个需要分配的稀缺 Runtime Resource。

## 4. Stable Prefix 与 Context / Prompt Cache

重复不变的：

```text
system instructions
stable tool schemas
project instructions
```

适合形成稳定 prefix，提高缓存命中。

频繁改变 Tool 顺序、动态把无关 Schema 插进前缀，会破坏 cache locality。

## 5. 大 Tool Result 不应全部塞进 Context

例如：

```text
100MB log
large SQL result
repo-wide grep output
```

合理路径：

```text
Tool Result
→ persist external artifact
→ generate bounded preview / summary
→ return artifact_ref + metadata
→ load slices on demand
```

这比直接 truncate 更好，因为信息仍可追溯。

## 6. Offloading 的数据契约

```json
{
  "artifact_ref": "tool-results/call_31.txt",
  "original_size": 280123,
  "preview": "...",
  "has_more": true,
  "content_type": "text/plain"
}
```

模型只看到足够下一步决策的信息；需要细节时再读取 artifact。

## 7. Stale Context

Context 不仅会“太长”，还会“过时”：

```text
旧文件摘要
旧计划
旧权限信息
旧 Tool Result
旧 Memory
```

Assembly 阶段应考虑：

```text
version
freshness
source authority
superseded_by
```

## 8. 源码证据

Claude Code 固定快照的 `queryContext.ts` 明确组装 system prompt、user context、system context，并考虑 cache-safe prefix；`toolResultStorage.ts` 会把大 Tool Result 持久化到 session 目录，用 preview + filepath 替代把完整内容持续塞进模型上下文。

Codex 的 `ToolOutput` 也区分 model-facing output、log representation 与 host metadata。

## 9. HUMAN-A

- `AGENT-008` Context Assembly：16 来源；
- `AGENT-011` Large Tool Result / Offloading：11 来源；
- `AGENT-012` Prompt / Context Cache：5 来源。

## 10. 🎯 面试回答

> Context Engineering 是 Harness 在每次模型调用前构造 inference state：从 System、Goal、Runtime State、History、Memory、Retrieval、Tool Schema 和 Tool Result 中选择并排序，在有限 Token Budget 内保留最有价值信息。大 Tool Result 应外部化为 Artifact + Preview，而不是不可逆截断；稳定前缀可以配合 Context Cache 降低成本。

<details><summary>自测：Context 和 Memory 最大区别是什么？</summary>

Context 是当前一次模型调用实际看见的输入；Memory 是未来可再次召回的信息来源，是否进入 Context 由 Harness 决定。
</details>