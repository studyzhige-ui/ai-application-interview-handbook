# 18. Large Tool Result / Offloading：大结果不应该直接塞回 Context

`AGENT-011` 在冻结 HUMAN-A 中有 **11 个独立来源**。

这是一个非常工程化的问题：

```text
Tool 返回 5MB 日志怎么办？
Repo Search 命中几千项怎么办？
SQL 返回 10 万行怎么办？
Browser 抓到超长页面怎么办？
```

最差答案：

> “直接截断前 N 个字符。”

截断可以兜底，但成熟 Runtime 更希望：

> **把完整结果保留在 Context 外，只向模型提供 Preview + Reference + Retrieval Interface。**

这就是 Tool Result Offloading。

---

# 1. 先讲人话：Context 是工作台，不是仓库

Tool 原始结果：

```text
10 MB test log
```

模型本轮可能只需要：

```text
1. 哪些 test failed
2. 第一段 stack trace
3. 完整日志在哪里
```

所以：

```text
Raw Result
→ Artifact / External Storage

Context
→ Summary / Preview + Reference
```

不要把 Context Window 当 Object Storage。

---

# 2. Truncate 和 Offload 的区别

## Truncate

```text
abcdef...XYZ
```

只保留前 20K。

优点：

- 简单；
- 不需要额外存储。

缺点：

- 后半部分永久不可访问；
- 关键错误可能恰好在尾部；
- 不能按需继续读取。

## Offload

```text
完整结果 → artifact store
模型看到 → preview + ref
```

优点：

- 完整信息仍在；
- Context 小；
- 后续可按需 read/search。

缺点：

- 需要生命周期、权限、清理和引用协议。

---

# 3. 标准 Offload Pipeline

```text
Tool executes
    ↓
Raw Result
    ↓
Estimate / Measure Size
    │
    ├─ Small → inline
    │
    └─ Large
         ↓
   Persist Artifact
         ↓
   Build Preview
         ↓
   Return Reference
         ↓
Model may call read/search artifact later
```

---

# 4. 一个 Tool Result Reference

```json
{
  "ok": true,
  "truncated": true,
  "preview": "first error lines...",
  "artifact": {
    "id": "artifact_123",
    "size_bytes": 5242880,
    "content_type": "text/plain"
  },
  "hint": "use read_artifact with offset/limit for more"
}
```

模型有需要再调用：

```text
read_artifact(artifact_123, offset=50000, limit=5000)
```

或者：

```text
search_artifact(artifact_123, pattern="AssertionError")
```

---

# 5. 为什么 Preview 要“帮助下一步决策”

如果 Preview 永远是：

```text
前 2KB
```

不一定最好。

Test Log 更有价值的 Preview 可能是：

```text
exit code
failed test names
error summary
last 100 lines
```

Search Result 更有价值：

```text
total matches
best matches
path distribution
```

SQL Result：

```text
row count
columns
first rows
aggregation summary
```

因此：

> **Preview Strategy 可以 Tool-specific。**

---

# 6. 为什么 Artifact Ref 本身也需要权限

假设：

```text
artifact://tenant-A/run-1/tool-result-9
```

Tenant B 不能通过猜 ID 读取。

所以 Artifact Store 必须继承：

- tenant scope；
- session/run ownership；
- permission；
- retention；
- encryption / secret policy。

不要把：

```text
filepath
```

当成无条件可共享公共地址。

---

# 7. Claude Code 的真实 Offloading 实现

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`utils/toolResultStorage.ts` 文件开头直接说明：

> Utility for persisting large tool results to disk instead of truncating them.

固定快照中它会：

```text
计算 persistence threshold
→ session-specific tool-results directory
→ 以 toolUseId 构造文件名
→ 把完整文本写盘
→ 生成有限 preview
→ 返回 filepath / originalSize / isJson / hasMore
```

随后构造模型可见信息：

```text
Output too large
Full output saved to: ...
Preview: ...
```

这就是非常直接的成熟产品证据。

---

# 8. 为什么 Claude Code 用 `toolUseId` 做存储身份

源码注释说明：

```text
tool_use_id is unique per invocation
```

因此同一个 Tool Result 重放时，可以避免每个 API Turn 重复写一份。

固定实现还用：

```text
writeFile(..., flag='wx')
```

而不是：

```text
stat → write
```

来避免 check-then-write race。

这提供两个通用启发：

> **Artifact 应绑定稳定 Invocation ID；写入也要考虑并发竞争。**

---

# 9. 为什么 Offload 不是简单“写文件”

Production Cloud 环境可能没有稳定本地磁盘。

所以抽象应是：

```text
ArtifactStore
```

实现可以：

- local filesystem；
- object storage；
- database blob；
- remote execution workspace。

Tool Result 只引用逻辑 ID。

例如：

```python
artifact = await artifact_store.put(
    run_id=ctx.run_id,
    call_id=ctx.call_id,
    data=raw_output,
)
```

---

# 10. Artifact 生命周期

Tool Result Artifact 不应该永远保存。

需要考虑：

```text
Retention TTL
Run deletion
Session deletion
Tenant policy
Debug retention
Eval retention
```

例如：

```text
normal run artifacts: 7 days
failed-run debug artifacts: 30 days
secret-containing artifacts: shorter / encrypted
```

具体规则由产品安全要求决定。

---

# 11. Offloading 与 Compaction 的区别

容易混：

```text
Offloading
= 大块原始结果移到 Context 外，保留 reference

Compaction
= 把一段历史/上下文压缩成较短语义表示
```

例如：

```text
5MB Tool Log
→ offload artifact

50 turn conversation
→ compact summary
```

两者可以组合。

---

# 12. Offloading 应尽可能早发生

错误路径：

```text
Tool Result 5MB
→ 先 append messages
→ token count 爆炸
→ 再 compact
```

更好：

```text
Tool Result produced
→ result-size policy
→ offload immediately
→ only preview enters history
```

这样避免大结果污染后续多轮 Context。

---

# 13. Aggregate Tool Result Budget

单个结果都不大：

```text
10K × 20 tools = 200K
```

还是会爆。

所以 Runtime 还需要：

```text
per-tool-result cap
+ aggregate active result budget
```

Claude Code `ToolUseContext` 中有：

```text
contentReplacementState
```

其注释明确提到 per-conversation-thread tool result budget / aggregate replacement decisions。

这说明生产实现会处理“总量”而不是只处理单结果。

---

# 14. Old Tool Result 可以进一步降级

时间越久，原始 Result 的直接价值通常越低。

可以分层：

```text
Recent result
→ richer preview

Older result
→ short summary + ref

Very old irrelevant result
→ reference only / cleared projection
```

但 Artifact 本身仍可保留到 TTL。

这叫：

> **Progressive Context Dehydration。**

---

# 15. 哪些结果不能只给 Preview

有些结果是短但关键：

```text
transaction id
commit hash
external resource id
approval id
```

这些应该结构化保存在 Runtime State。

不要让：

```text
唯一外部订单 ID
```

只存在一段以后可能被清掉的 Tool Result Text 里。

---

# 16. Artifact 与 Runtime State 的边界

例如：

```text
full test log → Artifact
last_test_exit_code → State
failed_test_names → State / Context projection
artifact_id → State
```

这样 Resume 时无需重新解析 5MB 日志，关键事实已经结构化。

---

# 17. Search-before-read

对于超大 Artifact，一个非常高效的模式：

```text
search_artifact(pattern)
→ offsets / matching lines
→ read_artifact(offset, limit)
```

而不是：

```text
read entire artifact back into Context
```

这和 Coding Agent 处理代码仓库的原则相似：

```text
Search first
Read relevant slice
```

---

# 18. Multimodal Result

Tool 可能返回：

- image；
- audio；
- binary；
- PDF。

Offload 策略需要：

```text
content type
media metadata
model support
signed access / reference
```

Claude Code 当前 `toolResultStorage.ts` 明确只对某类 text content 做文件 persistence；遇到 non-text content 会返回无法持久化的错误。

这说明：

> **Artifact Store 需要按媒体类型设计，不是所有结果都能当 txt。**

---

# 19. Security：Tool Result 可能包含 Secret

Shell 输出：

```text
env
```

可能打印 Token。

如果 Offload：

```text
完整 Secret 被持久化到 artifact store
```

因此需要：

- redaction；
- encryption；
- restrictive ACL；
- retention；
- secret scanning。

而模型 Preview 也要脱敏。

---

# 20. Prompt Injection 与 Artifact

网页 Tool 返回 2MB 页面，其中有：

```text
Ignore previous instructions...
```

即使 Offload 了，也不代表安全。

后续 Agent 按需读取 Artifact 时，仍然是：

> **untrusted external context。**

所以 Artifact Metadata 最好保留 origin/trust。

---

# 21. 一个 Offloading 实现

```python
async def normalize_large_result(raw, ctx, store, max_inline=20_000):
    text = serialize(raw)

    if len(text) <= max_inline:
        return {
            "inline": text,
            "truncated": False,
        }

    artifact = await store.put(
        owner=ctx.tenant_id,
        run_id=ctx.run_id,
        call_id=ctx.call_id,
        data=text,
    )

    return {
        "preview": make_preview(text),
        "artifact_id": artifact.id,
        "size": len(text),
        "truncated": True,
    }
```

Production 还需要：

- streaming write；
- content type；
- redaction；
- TTL；
- dedup；
- quota。

---

# 22. Offload 的可观测指标

可以监控：

```text
tool_result_bytes_total
offloaded_result_count
inline_result_tokens
artifact_readback_count
artifact_storage_bytes
offload_failure_rate
preview_to_full-read ratio
```

如果：

```text
90% Artifact 立刻被完整读回
```

说明 Preview/Tool Design 可能不合理。

---

# 23. 高频易错点

⚠️ **大结果直接截断就行**  
会永久丢失信息，优先考虑 offload + reference。

⚠️ **Artifact Ref 不需要权限**  
Ref 本身是数据访问入口。

⚠️ **Tool Result 只按单个大小限制**  
还要控制 aggregate active result budget。

⚠️ **Offload = Compaction**  
一个迁移原始数据位置，一个做语义压缩。

⚠️ **关键 ID 只留在 Tool Text**  
应该结构化写 Runtime State。

---

# 24. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> 大 Tool Result 我不会直接全部塞进 Context，也不只做不可逆截断，而是把完整结果 offload 到 Artifact Store，只给模型 preview、size、artifact ref 和按需 read/search 接口。关键结构化事实如 exit code、resource id 另存 Runtime State。这样能控制 Context，又保留后续取回能力。

## Level 2｜2–3 分钟

> 我会同时设 per-result 和 aggregate budget。Result 生成后立即判断大小，大结果先 redaction/持久化，按 Tool 类型做语义 preview。Artifact ID 绑定 run/call/tenant，并有 ACL、TTL、content type。后续尽量 search-before-read，不把完整 artifact 再塞回 Context。Offloading 和 compaction 分开：前者保存原始结果到外部，后者压缩历史语义。

## Level 3｜继续追问

🔍 **为什么用 call_id / toolUseId 作为 Artifact identity？**  
它稳定对应一次 Tool Invocation，便于 dedup、trace 和 replay。

🔍 **本地文件 Offload 在多实例服务里有什么问题？**  
后续 Worker 可能读不到，需要共享 object store 或 workspace affinity。

🔍 **Preview 怎么设计？**  
按 Tool 语义提取支持下一步决策的信息，而不是一律取前 N 字符。

---

# 25. 本章证据

## HUMAN-A

- `AGENT-011` Large Tool Result / Offloading：11 sources；
- Related `AGENT-009` Context Compaction：41 sources。

## Claude Code

- `utils/toolResultStorage.ts`
- `Tool.ts` 中 `contentReplacementState`

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

源码实现中的具体 file path / threshold 属于该产品快照，不等价于通用唯一做法。

---

# 26. 自测

<details><summary>1. Truncate 和 Offload 最大区别是什么？</summary>

Truncate 丢弃超出部分；Offload 把完整结果保存到 Context 外，再用 preview + reference 让模型按需取回。
</details>

<details><summary>2. 为什么关键 resource id 应该进 Runtime State？</summary>

Tool Result Context 未来可能被 compact/clear，Resume 和幂等需要稳定结构化事实，不能重新从历史文本猜。
</details>

<details><summary>3. 为什么需要 aggregate Tool Result Budget？</summary>

单个结果都在限制内，多个结果累计仍可能占满 Context，所以还要控制总活跃结果体积。
</details>

<details><summary>4. Artifact 为什么必须继承 tenant/permission？</summary>

它保存完整原始数据，是新的数据访问入口；如果只凭可猜 ID 读取，会产生跨租户泄露。
</details>
