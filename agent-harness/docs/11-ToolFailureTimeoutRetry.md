# 11. Tool Failure / Timeout / Retry：失败语义比“try/except”重要

`AGENT-020` 在冻结 HUMAN-A 中有 **27 个独立来源**，是 Tool Runtime 最核心的高频问题之一。

面试里常见的差距是：

```text
初级：Tool 报错了就 try/except，然后 retry。

成熟：先判断失败发生在哪一层、是否可修复、是否可重试、是否已经产生副作用，再决定 Repair / Retry / Fallback / Fail。
```

这一章建立 Tool Failure 的完整模型。

---

# 1. 先讲人话：不是所有失败都该 Retry

几个失败：

```text
A. HTTP 503
B. JSON 参数缺字段
C. 用户没有权限
D. 文件路径写错
E. 支付 API 超时，但不知道请求是否已经成功
F. Runtime 找不到注册 Tool
G. Tool Handler 内部 invariant 被破坏
```

如果全部：

```python
for _ in range(3):
    retry()
```

会产生非常不同的坏结果。

因此第一原则：

> **Retry 是 Failure Classification 之后的策略，不是默认动作。**

---

# 2. Tool Failure 的七层分类

## 2.1 Protocol / Parse Failure

例如：

```text
Tool Call JSON 解析失败
未知 payload type
```

可能需要：

- 返回 validation error 给模型；
- 或 Runtime Fatal。

---

## 2.2 Argument / Semantic Failure

例如：

```text
path 不存在
start > end
resource_id 编造
```

通常：

```text
Repair
```

比原样 Retry 更合理。

---

## 2.3 Permission Failure

```text
permission denied
approval rejected
path outside workspace
```

通常：

```text
不要自动 Retry
```

因为权限不会因为重复调用突然变好。

可以：

- 请求审批；
- 选择低权限替代路径；
- 明确终止。

---

## 2.4 Dependency / Transient Failure

例如：

```text
HTTP 429
HTTP 503
connection reset
temporary DNS failure
```

可能：

```text
Retry + Backoff + Jitter
```

---

## 2.5 Timeout

Timeout 最危险的点不是“慢”，而是：

> **你可能不知道副作用是否已经发生。**

例如：

```text
create_ticket request sent
↓
client timeout
↓
server may already have created ticket
```

这时盲目 Retry 可能重复创建。

---

## 2.6 Business Failure

例如：

```text
库存不足
issue 已关闭
branch protection 拒绝 push
```

系统工作正常，只是业务条件不满足。

应该反馈给模型重新规划，而不是基础设施 Retry。

---

## 2.7 Fatal Runtime Failure

例如：

```text
Tool payload 与 Runtime handler 类型完全不兼容
state corruption
impossible invariant
```

继续让模型“再试试”可能没有意义。

应：

```text
Fail Run / Escalate
```

---

# 3. 一个 Error Taxonomy

```python
from dataclasses import dataclass
from enum import Enum


class ErrorKind(str, Enum):
    INVALID_ARGUMENTS = "invalid_arguments"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    RATE_LIMITED = "rate_limited"
    TRANSIENT = "transient"
    TIMEOUT = "timeout"
    BUSINESS_REJECTED = "business_rejected"
    FATAL = "fatal"


@dataclass
class ToolError:
    kind: ErrorKind
    message: str
    retryable: bool
    repairable: bool
    side_effect_status: str  # none / committed / unknown
```

最后一个字段尤其重要：

```text
side_effect_status
```

因为 Timeout 后的恢复策略取决于它。

---

# 4. Repair / Retry / Fallback / Fail 四种动作

## Repair

改变 Tool Call：

```text
path 错
→ search correct path
→ call again
```

## Retry

相同语义动作再次尝试：

```text
503
→ backoff
→ same request
```

## Fallback

换依赖或路径：

```text
primary model unavailable
→ fallback model

MCP search unavailable
→ local search
```

## Fail

明确终止当前动作或 Run：

```text
permission permanently denied
fatal invariant
budget exhausted
```

成熟 Runtime 的核心是：

> **错误类别 → 策略映射。**

---

# 5. 一个简单 Decision Table

| Failure | Repair | Retry | Fallback | Fail |
|---|---:|---:|---:|---:|
| invalid args | ✅ | ❌ 原样不该 | 可能 | 超预算后 |
| not found | ✅ | ❌ | 可能 | 最终 |
| permission denied | 可能 | ❌ | ✅ 低权限路径 | ✅ |
| 429 | ❌ | ✅ | ✅ | 超预算后 |
| 503 | ❌ | ✅ | ✅ | 超预算后 |
| timeout read-only | ❌ | ✅ | 可能 | 超预算后 |
| timeout write | 先查副作用 | 危险 | 可能 | 视情况 |
| fatal runtime | ❌ | ❌ | 少数情况 | ✅ |

---

# 6. Retry 为什么需要 Backoff + Jitter

如果 1000 个 Agent Worker 同时收到 503：

```text
立即 retry
→ 再次同时打爆依赖
```

指数退避：

```text
1s
2s
4s
8s
```

再加随机 Jitter，避免同步重试。

教学代码：

```python
import asyncio
import random


async def retry_with_backoff(fn, max_attempts=4):
    for attempt in range(max_attempts):
        try:
            return await fn()
        except TemporaryError:
            if attempt == max_attempts - 1:
                raise

            base = 2 ** attempt
            delay = base + random.random()
            await asyncio.sleep(delay)
```

真实系统还要尊重：

```text
Retry-After
Deadline
Budget
Cancellation
```

---

# 7. Retry Budget 为什么必须同时存在

如果每个 Layer 都 retry 3 次：

```text
Agent Loop retry 3
× Tool Gateway retry 3
× HTTP Client retry 3
= 最坏 27 次
```

这叫 Retry Amplification。

所以需要：

```text
Run-level / Step-level Retry Budget
```

例如：

```text
max_attempts = 4
max_retry_time = 15s
max_cost = ...
```

而不是每层独立无限重试。

---

# 8. Timeout 必须是 Deadline，不只是单次 wait_for

假设：

```text
Tool 总 deadline = 10s
```

内部：

```text
DNS 2s
connect 3s
retry 4s
```

下一次 retry 不应该又获得完整 10s。

所以更成熟：

```text
absolute deadline
→ 每次 attempt 计算 remaining time
```

这避免长任务不断“续命”。

---

# 9. Timeout + Side Effect 是最危险组合

例如：

```text
POST /create-order
```

客户端等待 5s 后 timeout。

可能状态：

```text
1. Server 没收到
2. Server 收到但没执行
3. Server 已执行，但 response 丢了
```

因此 Runtime 不知道：

```text
能不能 Retry？
```

解决方法通常是：

- idempotency key；
- operation id；
- query status；
- external resource correlation；
- side-effect ledger。

第 27 章会完整讲。

---

# 10. 模型应该看到多少 Error

模型需要足够信息做 Repair：

```json
{
  "error_type": "not_found",
  "message": "file src/ap.py does not exist",
  "repairable": true
}
```

但不一定应该看到：

```text
internal stack trace
secret token
private network topology
host path
```

所以 Error 也要：

```text
Internal Diagnostic
vs
Model-visible Feedback
```

---

# 11. Error Feedback 应该告诉模型“下一步可能做什么”吗？

可以给结构化可操作信息，但不要过度替模型规划。

例如：

```json
{
  "error_type": "not_found",
  "requested_path": "src/ap.py",
  "available_hint": "use repository search to locate the file"
}
```

这比：

```text
ERROR 404
```

更利于自我修复。

但安全上不能：

```text
把所有隐藏资源名都泄露出来
```

---

# 12. Repeated Failure Detection

Agent 常见死循环：

```text
call A(args=x)
→ fail
call A(args=x)
→ fail
call A(args=x)
→ fail
```

Runtime 可以维护：

```text
failure fingerprint
= tool + normalized args + error kind
```

如果重复达到阈值：

```text
1. 告诉模型“同一调用已失败 N 次”
2. 要求 change approach
3. disable tool temporarily
4. terminate step/run
```

这和 Loop Guard 直接关联。

---

# 13. Circuit Breaker 属于哪一层

单个 Agent 的 retry 和全局依赖健康不是一回事。

如果某 MCP Server 已经：

```text
连续 1000 次失败
```

没必要让每个 Agent 都先失败 3 次。

Circuit Breaker 可以：

```text
closed
→ open after threshold
→ fail fast
→ half-open probe
→ close if recovered
```

这更偏 Runtime Resilience / Backend Infrastructure，会在 `AGENT-038` 对应章节再次扩展。

---

# 14. Codex 对 Error Semantic 的直接证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/tools/src/function_call_error.rs` 只有两个非常清晰的顶层语义：

```text
RespondToModel(String)
Fatal(String)
```

这个简洁设计很有启发：

```text
错误要么可以作为 Observation 反馈模型继续修
要么 Runtime 认为它是 Fatal
```

例如 Registry 中：

- unsupported tool → `RespondToModel`；
- PreToolUse hook block → `RespondToModel`；
- incompatible payload → `Fatal`。

这说明“失败能否继续循环”应该是显式 Runtime 语义。

---

# 15. Codex Registry 的 Tool Failure Lifecycle

固定源码 dispatch 会：

```text
start ToolDispatchTrace
→ lookup
→ validate payload kind
→ pre hook
→ execute
→ telemetry
→ post hook
→ notify finish
→ record complete/failed
```

即使失败，也会：

- 记录 trace；
- 产生 finish outcome；
- 区分 handler 是否已经执行。

这对副作用判断很重要。

---

# 16. Claude Code Permission Failure 证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`hooks/useCanUseTool.tsx` 的 Permission Decision 显式区分：

```text
allow
deny
ask
```

并处理 Abort。

因此：

```text
Permission Denial
```

不是普通 transient execution error，不能无脑 retry。

---

# 17. Tool Error 应不应该计入 Step？

如果：

```text
Tool 503
Runtime internal retry
→ success
```

可以仍视为同一语义 Step 的多个 attempt。

如果：

```text
Tool not_found
→ feedback to model
→ model decides search instead
```

这是新的 Agent Step。

所以要区分：

```text
Infrastructure Attempt
vs
Agent Re-decision
```

这和第 5 章 Run/Turn/Step 对齐。

---

# 18. Retry 与 Cancellation 必须联动

正在 backoff：

```text
sleep 8s
```

用户取消任务。

Runtime 不应该：

```text
睡完再 retry
```

Backoff wait 应该 cancellation-aware。

同理：

```text
deadline expired
```

后续 retry 必须停止。

---

# 19. AI 应用场景：MCP Tool 不可用

模型调用：

```text
github.create_issue
```

MCP Server disconnected。

合理策略：

```text
1. classify as capability unavailable
2. 不要伪造 success
3. 如果 reconnect 快且 safe → bounded retry
4. 如果有 REST fallback → fallback
5. 否则反馈模型，让它说明无法完成或改用其它路径
6. Trace 记录 provider/server origin
```

而不是：

```text
一直重新调用 create_issue
```

---

# 20. AI 应用场景：Search API 429

Search 是只读、相对容易 Retry。

可以：

```text
Retry-After
+ jitter
+ global rate limiter
+ alternate search provider
```

但如果整个 Run 剩余 2 秒 deadline：

```text
再等 10 秒不合理
```

Retry Policy 必须知道上层 Budget。

---

# 21. 高频易错点

⚠️ **Error = Exception**  
Agent Runtime 需要结构化 Failure Semantics。

⚠️ **所有 Timeout 都 Retry**  
写操作 Timeout 可能已经产生副作用。

⚠️ **所有 4xx 都不 Retry，所有 5xx 都 Retry**  
只是粗略经验，仍要结合业务语义和 provider contract。

⚠️ **每层各 retry 3 次**  
可能造成 Retry Amplification。

⚠️ **模型修参数也叫 Retry**  
更准确是 Repair / Re-plan。

---

# 22. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Tool 失败后我不会默认 retry，而会先分类：invalid args、permission、not found、transient、timeout、business rejection、fatal。Invalid args 更适合 Repair，429/503 可以 bounded retry + backoff/jitter，permission 通常不该自动 retry；写操作 timeout 要先确认副作用状态，否则可能重复执行。Runtime 还要限制 retry budget、支持 cancellation，并把可恢复错误结构化反馈给模型。

## Level 2｜2–3 分钟

> 我会把错误协议里加入 retryable、repairable 和 side_effect_status。Retry 使用 deadline-aware backoff，并避免多层 retry amplification。同一个 tool+args+error 重复失败会做 fingerprint，达到阈值后要求模型改路或停止。错误分 internal diagnostic 和 model-visible feedback，避免泄露 secret。对于跨依赖连续失败，再用 circuit breaker/fallback，而不是每个 Agent 独立撞墙。

## Level 3｜继续追问

🔍 **Tool timeout 后怎么判断能否 Retry？**  
先看操作是否 read-only/idempotent，是否有 idempotency key / status query，副作用状态是否 known。

🔍 **为什么 Retry Budget 要跨 Layer？**  
避免 Agent、Gateway、HTTP Client 层层乘法重试。

🔍 **什么时候错误应该 Fatal？**  
Runtime invariant 损坏、payload 与 handler 不兼容、无法保证安全继续时。

---

# 23. HUMAN-A 与追问链

- `AGENT-020` Tool Failure：27 sources；
- `AGENT-038` Runtime Resilience：15 sources；
- `AGENT-029` External Side Effect / Idempotency：6 sources。

Verified Tool Chain：

```text
Tool Lifecycle
→ Discovery
→ Failure
→ Permission / Sandbox
```

---

# 24. 自测

<details><summary>1. Repair 和 Retry 的区别？</summary>

Retry 是相同语义动作再次尝试；Repair 是修改参数、路径或策略后形成新的调用。
</details>

<details><summary>2. 为什么写操作 Timeout 不能直接 Retry？</summary>

因为 Server 可能已经完成副作用，只是 response 丢失。直接重试可能重复创建/发送/扣款，需要 idempotency/status reconciliation。
</details>

<details><summary>3. Retry Amplification 是什么？</summary>

多个系统层各自独立重试，导致总尝试次数乘法增长。例如三层各 3 次最坏可变成 27 次。
</details>

<details><summary>4. `RespondToModel` 和 Fatal 体现了什么设计思想？</summary>

明确区分可作为 Observation 让 Agent 修复的错误与 Runtime 无法安全继续的错误，避免所有 exception 都同一处理。
</details>
