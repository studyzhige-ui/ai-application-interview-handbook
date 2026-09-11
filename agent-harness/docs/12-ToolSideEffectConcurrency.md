# 12. Tool Side Effect / Concurrency：能不能并行，取决于“会改变什么”

Tool Runtime 一旦支持并行，很容易出现一个误区：

> “模型一次发了 4 个 Tool Call，那就 `asyncio.gather()` 全部并发。”

这对只读搜索可能很好，对写文件、发邮件、更新订单、修改同一 Workspace 则可能直接制造竞态。

`AGENT-031` Shared Workspace Concurrency 有 **7 个 HUMAN-A 来源**，`AGENT-029` External Side Effect 有 **6 个来源**。Claude Code / Codex 源码也都把 Parallel / Concurrency Semantics 放进 Tool Contract。

---

# 1. 先讲人话：Tool 的关键不是“慢不慢”，而是“会不会改变世界”

比较：

```text
read_file("a.py")
search_code("UserService")
```

和：

```text
write_file("a.py")
send_email(...)
create_issue(...)
run_migration(...)
```

第一组主要读取环境。

第二组会改变：

- Workspace；
- 外部系统；
- 数据库；
- 用户可见状态。

这类变化叫：

> **Side Effect。**

一旦有 Side Effect，就要开始考虑：

```text
顺序
并发
重复执行
回滚
补偿
可见性
```

---

# 2. Tool 可以先分四类

## 2.1 Pure / Deterministic

```text
calculate_hash(text)
parse_json(text)
```

相同输入大概率得到相同输出，也不改变外部状态。

最适合并行和重试。

---

## 2.2 Read-only External

```text
read_file
search_db
GET /ticket/123
```

不主动写状态，但结果可能随时间变化。

通常并发风险较低，但仍可能：

- 触发 rate limit；
- 读取不一致 snapshot；
- 暴露敏感数据。

---

## 2.3 Idempotent Write

例如：

```text
PUT /resource/123 with exact desired state
```

重复执行的最终状态相同。

但也不能简单等于“绝对安全”，因为：

- audit log 可能重复；
- webhook 可能重复触发；
- 实现未必真的幂等。

---

## 2.4 Non-idempotent / Destructive

```text
send_email
charge_card
append_comment
create_order
delete_branch
```

重复或并发执行可能产生不可逆后果。

这类 Tool 通常需要最强控制。

---

# 3. `isReadOnly` 和 `isDestructive` 不是一回事

一个 Tool 不是只读：

```text
write_file
```

但未必 destructive：

```text
创建一个新临时文件
```

另一个：

```text
delete_database
```

明显 destructive。

所以可以至少有：

```text
read_only
write
irreversible / destructive
```

不同风险层级对应：

- Approval；
- Sandbox；
- Concurrency；
- Retry Policy。

---

# 4. Claude Code Tool Contract 的直接证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`Tool.ts` 直接定义：

```text
isConcurrencySafe(input)
isReadOnly(input)
isDestructive?(input)
```

而且这些方法接收 `input`。

这说明风险并不一定只由 Tool 名字决定。

例如同一个 Bash Tool：

```text
ls -la
```

和：

```text
rm -rf build/
```

执行语义完全不同。

---

# 5. Codex 也把“是否支持并行 Tool Call”写进 Runtime Contract

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/tools/src/tool_executor.rs` 中：

```text
supports_parallel_tool_calls()
```

默认返回 `false`。

`ToolRegistry.supports_parallel_tool_calls()` 还会检查 Tool Exposure，再由 Router 提供：

```text
tool_supports_parallel(call)
```

这个默认值很有工程含义：

> **并发应是 Tool 明确声明的能力，而不是 Runtime 默认假设。**

---

# 6. 为什么两个“写不同文件”的 Tool 也未必安全并行

看起来：

```text
Agent A → edit a.py
Agent B → edit b.py
```

不同文件。

但可能同时依赖：

```text
package lock
formatter
code generation
shared build artifact
git index
working tree state
```

所以 Concurrency Safety 不能只看：

```text
path 是否相同
```

还要看更广的 shared resource。

---

# 7. Lost Update 是最经典的 Race

初始：

```text
config.py = version 1
```

两个 Agent：

```text
A read v1
B read v1

A write v2A
B write v2B
```

最终：

```text
v2A 被 v2B 覆盖
```

A 的修改丢失。

这就是 Lost Update。

解决方法可能包括：

- serialization；
- optimistic version check；
- patch against expected base；
- workspace isolation；
- merge conflict detection。

---

# 8. Optimistic Concurrency Control

给文件/资源一个版本：

```text
etag = abc123
```

Tool Call：

```json
{
  "path": "config.py",
  "expected_version": "abc123",
  "patch": "..."
}
```

执行时：

```text
current_version == expected_version
→ apply

else
→ conflict
```

Agent 看到：

```json
{
  "error_type": "conflict",
  "repairable": true
}
```

再重新读取 / merge。

这比静默覆盖安全得多。

---

# 9. Pessimistic Lock 什么时候合适

如果资源非常敏感且冲突成本高：

```text
acquire lock
→ modify
→ release
```

但长 Agent 任务不能：

```text
拿锁 20 分钟边思考边操作
```

否则：

- 锁占用太久；
- worker crash 可能留下 stale lease；
- 并发吞吐低。

所以更常见：

```text
short critical section
or
lease with expiry
```

而不是跨整个 Agent Run 持有数据库锁。

---

# 10. Workspace Isolation 是 Coding Agent 常见解法

Multi-Agent 同时改代码时，可以：

```text
Parent Workspace
├─ Agent A → worktree A
└─ Agent B → worktree B
```

每个 Agent 独立修改。

最后：

```text
merge / cherry-pick / conflict resolution
```

这样把：

```text
共享写冲突
```

转化成：

```text
显式 merge conflict
```

通常更容易管理。

---

# 11. 并行 Tool Calls 的收益

对于独立只读 Tool：

```text
read a.py = 500ms
read b.py = 500ms
read c.py = 500ms
```

串行：

```text
~1500ms
```

并行：

```text
~500ms + overhead
```

所以不能为了安全全部串行。

目标是：

> **只并行“语义上独立、资源上无冲突、预算上允许”的调用。**

---

# 12. 一个 Concurrency Planner

教学抽象：

```python
def can_run_in_parallel(calls, registry):
    for call in calls:
        tool = registry.get(call.tool_name)
        if not tool.is_concurrency_safe(call.arguments):
            return False

    if has_resource_conflict(calls):
        return False

    return True
```

真实系统可能进一步：

```text
group calls by conflict domain
```

例如：

```text
Group 1: read-only web search → parallel
Group 2: writes to workspace X → serialize
Group 3: writes to workspace Y → serialize separately
```

---

# 13. Side Effect Ledger

对于高风险外部动作，可以记录：

```text
operation_id
call_id
tool_name
idempotency_key
status
external_resource_id
committed_at
```

例如：

```json
{
  "operation_id": "op_123",
  "tool": "create_jira",
  "status": "committed",
  "external_resource_id": "AI-456"
}
```

这样 Resume 时先查：

```text
这个 side effect 是否已发生？
```

而不是直接重放 Tool。

第 27 章会完整展开。

---

# 14. 并发和 Retry 会互相放大

两个并发写操作：

```text
A conflict
B conflict
```

如果双方都自动 retry：

```text
再次同时碰撞
```

可能形成：

```text
livelock
```

需要：

- jitter；
- backoff；
- conflict-aware re-read；
- serialization fallback。

---

# 15. “Parallel Safe” 也可能与当前 Context 有关

Tool 自身：

```text
read_file
```

通常 parallel safe。

但如果两次读取后，模型要求：

```text
根据 read A 结果决定是否 read B
```

那是 Planning Dependency，不能并行。

所以并行至少有两层：

```text
Tool-level concurrency safety
AND
Plan-level dependency independence
```

---

# 16. Tool Call 顺序为什么要进入 Trace

如果 Bug 只在：

```text
write A
then write B
```

时出现，而并发执行顺序不稳定，Trace 必须记录：

- start time；
- finish time；
- resource；
- version；
- call_id；

否则无法重现竞态。

---

# 17. 数据库 Tool 的并发问题

两个 Agent：

```text
read balance=100
A subtract 30
B subtract 50
```

如果使用：

```text
read-modify-write
```

可能最终错误。

正确性应尽量由数据库提供：

```sql
UPDATE account
SET balance = balance - 30
WHERE id = ?
  AND balance >= 30;
```

或 transaction / version condition。

不要试图只靠 Agent Prompt：

> “请不要发生并发冲突。”

---

# 18. 外部 API 的并发 Limit

即使 Tool 是 read-only：

```text
search API
```

并发 100 个也可能触发：

- 429；
- quota exhaustion；
- provider ban。

所以：

```text
Concurrency Safe
≠ Unlimited Concurrency
```

Runtime 还需要：

- semaphore；
- rate limit；
- tenant quota；
- backpressure。

通用流控属于 AI Backend Engineering，但 Tool Runtime 要暴露并尊重这些限制。

---

# 19. Side Effect 与 Approval 的关系

可以用风险矩阵：

| Tool | Side Effect | Reversible | Approval |
|---|---|---|---|
| read_file | 无 | - | 通常不需要 |
| write temp file | 低 | 容易 | 可能自动 |
| edit source | 中 | 可 git rollback | 视模式 |
| send email | 外部 | 很难撤回 | 常需要 |
| delete production data | 高 | 可能不可逆 | 强审批 |

Permission / Approval 章节会正式展开。

---

# 20. 一个 Coding Agent 并发例子

任务：

```text
修复 API + 补测试 + 更新 docs
```

可以：

```text
Subagent A → source worktree
Subagent B → test worktree
Subagent C → docs worktree
```

但最终必须：

```text
merge
→ resolve conflict
→ run integrated tests
```

不能：

```text
三个 Agent 都说自己成功
→ 直接宣布任务成功
```

共享资源并发最终仍然要 Outcome Verification。

---

# 21. 高频易错点

⚠️ **模型一次发多个 Tool Call = 都可以 parallel**  
还要看依赖和资源冲突。

⚠️ **不同文件就不会冲突**  
可能共享 git index、build artifact、generated file。

⚠️ **Read-only = unlimited parallel**  
仍有 Rate Limit / QPS / Memory 等资源限制。

⚠️ **Lock 越大越安全**  
长时间持锁会严重降低吞吐并增加 failure complexity。

⚠️ **Prompt 可以解决 Race Condition**  
真正正确性要靠版本、事务、锁、隔离或 workspace design。

---

# 22. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Tool 是否能并行不能只看模型一次发了几个 Call，而要看 Tool 的 side effect、是否 concurrency-safe、调用之间有没有依赖以及是否访问同一资源。只读独立 Tool 可以并行；写操作要做版本校验、序列化、锁或 workspace isolation。高风险外部副作用还要结合 idempotency、approval 和 side-effect ledger，不能靠 Prompt 避免冲突。

## Level 2｜2–3 分钟

> 我会把 read-only、destructive、concurrency-safe 等属性放进 Tool Contract，并按 input 判断。Runtime 先做 plan dependency analysis，再做 resource conflict analysis，安全的组并行执行。文件类 Tool 可以用 expected version/OCC；Multi-Agent Coding 可以用独立 worktree 再 merge；外部 API 用 operation id/idempotency key。并发失败后不能双方立即同步 retry，要 backoff 或退化为 serialization。

## Level 3｜继续追问

🔍 **为什么 `supports_parallel_tool_calls` 默认 false 更合理？**  
因为并发可能破坏共享状态，安全能力应显式 opt-in。

🔍 **Optimistic Lock 适合 Agent 吗？**  
适合冲突较少、读取/思考时间长的场景；发现冲突后让 Agent re-read / merge。

🔍 **Multi-Agent 为什么常用 workspace isolation？**  
把隐式 race 转成显式 merge，降低共享写状态复杂度。

---

# 23. 本章证据

## HUMAN-A

- `AGENT-031` Workspace / Shared-resource Concurrency：7 sources；
- `AGENT-029` External Side Effect：6 sources；
- `AGENT-030` Multi-Agent：29 sources。

## Claude Code

`Tool.ts`：

```text
isConcurrencySafe(input)
isReadOnly(input)
isDestructive(input)
```

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

## OpenAI Codex

`ToolExecutor.supports_parallel_tool_calls()`；Registry / Router 的 parallel support 查询。

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

---

# 24. 自测

<details><summary>1. 两个 read_file 一定能并行吗？</summary>

Tool 本身通常 concurrency-safe，但还要确认计划上没有先后依赖，并考虑 I/O / QPS / resource budget。Tool-level safe 不等于系统层无限并行。
</details>

<details><summary>2. 什么是 Lost Update？</summary>

两个执行者基于同一个旧版本读取并分别写回，后写入者覆盖前者结果，导致前一个更新丢失。
</details>

<details><summary>3. 为什么 Coding Agent 常用 worktree 隔离？</summary>

让不同 Agent 在独立 workspace 修改，减少共享写竞态，最终通过 merge/conflict resolution 显式合并。
</details>

<details><summary>4. 为什么 Tool 的 destructive/concurrency 属性可能要按 input 判断？</summary>

同一个通用 Tool 不同输入风险不同，例如 Bash 的 `ls` 和 `rm -rf`，不能只按 Tool Name 静态分类。
</details>
