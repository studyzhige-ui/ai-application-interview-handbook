# 06. Tool Execution：结果回填、错误分类与有限恢复

模型终于选对工具，不代表任务从此一帆风顺。参数可能错，服务可能超时，返回结果也可能不可用。重要的不只是捕获异常，而是知道错误发生在哪一步、谁能够修复它。

[← 上一章](05-ToolRegistrationAndDiscovery.md) · [Agent 目录](../README.md) · [下一章 →](07-ToolConcurrencyAndCancellation.md)

---

<a id="section-1"></a>

## 1. 一次完整 Tool Execution

<a id="legacy-06-01"></a>

调用可以在不同位置失败：请求形状、业务含义、权限、外部执行和结果可用性。先看一次正常调用经过哪些边界，才能知道错误应该交给模型、程序、用户还是诊断系统。

```text
Model emits Tool Call
        ↓
Parse / Normalize
        ↓
Resolve Runtime Handler
        ↓
Validate Arguments
        ↓
Permission / Policy
        ↓
Execute
        ↓
Normalize Result / Error
        ↓
Emit Runtime Event / Trace
        ↓
Project model-visible Tool Result
        ↓
Return Observation to Loop
```

任何一步都可能失败。

---

<a id="section-2"></a>

## 2. Executor 为什么不应该直接暴露原始函数

<a id="legacy-06-02"></a>

如果 Runtime（运行时执行系统） 只是：

```python
# 仅展示裸函数调用：省略了授权、结果语义、超时和副作用判断。
result = func(**args)
```

它很难统一：

- timeout；
- cancellation；
- trace；
- retry；
- result size；
- post-hook；
- sandbox；
- metrics；
- external context 标记。

更合理的是显式 Invocation（调用实例）：

```python
# 调用数据示意：标识关联本次执行；期限与租户由宿主用于控制，并非都发给模型。
from dataclasses import dataclass

@dataclass
class ToolInvocation:
    call_id: str
    tool_name: str
    args: dict
    run_id: str
    step_id: str
    deadline_ms: int | None
    tenant_id: str
```

Executor（执行器） 接收 Invocation，而不是只接收业务参数。

---

<a id="section-3"></a>

## 3. Tool Result 不是一段字符串

<a id="legacy-06-03"></a>

一个稳定 Result 可以区分：

```text
model_visible_content
status
structured_data
artifacts
retryable
host_metadata
trace_fields
```

例如：

```json
{
  "status": "failed",
  "error_kind": "timeout",
  "summary": "tests exceeded 60s",
  "artifact_ref": "logs/test-call-31.txt",
  "retryable": true
}
```

---

<a id="section-4"></a>

## 4. 为什么日志、模型输出、Host Metadata 应分层

<a id="legacy-06-04"></a>

同一次 Tool Output 可能需要三个 projection：

```text
Model
→ 只需要足够继续决策的信息

Log / Telemetry
→ 需要诊断摘要，但不能泄露 secret / 大媒体

Host
→ 可保存完整 artifact id、内部 metadata、security label
```

把三者混成一个字符串会产生：

- Secret 泄露；
- Context 爆炸；
- Debug 信息不足；
- Replay（重放） 不可靠。

内部错误可能带服务地址或令牌。日志在受控范围保留排障线索，模型只接收可行动的脱敏说明。Projection（投影）就是面向不同使用者提供不同表示，不是再复制一份全文。

---

<a id="section-5"></a>

## 5. Failure Classification

<a id="legacy-06-05"></a>

建议至少区分：

```text
InvalidArguments
SchemaMismatch
PermissionDenied
ToolUnavailable
Timeout
Cancelled
ExecutionError
DependencyError
ResultValidationError
FatalRuntimeError
```

不同错误对应不同恢复策略。

| 发生的事 | 首先由谁处理 | 是否给模型 | 下一步 |
|---|---|---|---|
| 参数少字段、格式错误 | 校验层 | 可给简短修复提示 | 有限次重新构造参数 |
| 业务对象不存在/资料不足 | 工具适配与任务逻辑 | 可提供安全的业务反馈 | 换合法输入、澄清或部分交付 |
| 临时网络错误、限流 | 适配器 | 通常先由程序按预算恢复，最终再反馈 | 仅对安全可重复的请求有限重试 |
| 无权限 | 权限层 | 告知拒绝或需确认，但不暴露秘密 | 停止该动作，不能换身份绕过 |
| 人工批准尚未到达 | 运行时 | 可显示等待，不是错误修复 | 暂停并等待 |
| 用户取消 | 控制层 | 必要时记录取消观察 | 停派新任务、传播取消 |
| 状态损坏、处理器程序Bug | 宿主/运行时 | 不把堆栈交模型无限自救 | 停止或隔离，报错给维护者 |
| 请求已发出，但是否成功未知 | 业务核对流程 | 告知结果未确认 | 查回执/幂等键，不能盲重试 |

程序内部一次重试成功，不必把每次超时堆给模型。反过来，模型已经需要决定“继续还是请求用户帮助”时，不能吞掉最终失败使其以为工具成功。

---

<a id="section-6"></a>

## 6. Repair、Retry、Fallback、Fail 不是一回事

<a id="legacy-06-06"></a>

### Repair

模型生成的参数错：

```text
Invalid Arguments
→ structured feedback
→ model repairs arguments
```

### Retry

相同请求可能因临时故障成功：

```text
429 / transient network / temporary unavailable
→ backoff
→ retry
```

### Fallback

当前能力失败，换另一能力：

```text
provider A unavailable
→ provider B
```

### Fail

继续执行没有意义或风险过大：

```text
permission denied
invalid invariant
irrecoverable state corruption
```

---

<a id="section-7"></a>

## 7. Retry Eligibility 必须先判断幂等与副作用

<a id="legacy-06-07"></a>

错误做法：

```python
# 反例：下面的函数形状有效，但重试策略错误。不要用于真实写入。
async def unsafe_retry(call_tool):
    for _ in range(3):
        try:
            return await call_tool()
        except Exception:
            # 错误点：吞掉异常且未区分授权、参数、未知副作用等失败。
            pass
```

如果 Tool 是：

```text
send_email
create_order
charge_card
publish_release
```

第一次可能已经成功，只是 Response 丢了。

盲重试会制造重复副作用。

所以：

```text
Failure
→ Did execution start?
→ Could side effect have committed?
→ Is call idempotent?
→ Is there an idempotency key / operation ledger?
→ Retry eligibility
```

参数校验前拒绝，通常尚无副作用，可以让模型有限改参；上传超时可能已经成功，不能用一次新上传来“确认”。两种失败不由相同重试逻辑处理。

---

<a id="section-8"></a>

## 8. Timeout 也不是一种简单失败

<a id="legacy-06-08"></a>

至少区分：

```text
Queue Timeout
Connect Timeout
Execution Timeout
Result Read Timeout
Overall Deadline
```

Execution Timeout 最危险，因为：

```text
Client 认为超时
≠ Server 一定停止执行
```

所以副作用 Tool 要继续考虑 operation id / status query / idempotency。

---

<a id="section-9"></a>

## 9. 错误反馈给模型应该“可行动”

<a id="legacy-06-09"></a>

低质量：

```text
Tool failed: 500
```

高质量：

```json
{
  "error_kind": "file_not_found",
  "path": "src/foo.py",
  "retryable": false,
  "suggestion": "search repository for the symbol before reading a path"
}
```

但也不能泄露：

- internal secret；
- stack trace 中的凭证；
- 不应模型可见的 policy detail。

---

<a id="section-10"></a>

## 10. Result Validation

<a id="legacy-06-10"></a>

Tool 自己返回成功，也可能结果不可用：

```text
HTTP 200 but empty body
command exit 0 but expected artifact missing
JSON parses but field invariant broken
```

所以执行后还能有：

```text
Execution Success
→ Result Validation
→ Accepted Result / Rejected Result
```

---

<a id="section-11"></a>

## 11. Pre / Post Tool Hook 为什么很有用

<a id="legacy-06-11"></a>

Pre Tool：

```text
rewrite input
block dangerous action
inject environment
```

Post Tool：

```text
validate result
redact
attach context
record audit
```

但要注意：

> Post Tool Hook（生命周期钩子） 如果 block，实际外部副作用可能已经发生。

不能把“结果没有回给模型”误解成“Tool 没执行”。

---

<a id="section-12"></a>

## 12. 产品实现与官方资料对照（按需展开）

<details>
<summary>源码证据：Codex</summary>

<a id="legacy-06-12"></a>

固定快照中：

- `ToolRouter` 把 `ResponseItem` 规范化成带 `tool_name / call_id / payload` 的 `ToolCall`；
- `ToolRegistry` 负责 dispatch；
- `CoreToolRuntime` / `ToolExecutor` 提供统一执行接口；
- `FunctionCallError` 至少区分 `RespondToModel` 与 `Fatal`；
- Registry（注册表） 执行链有 pre/post tool hooks、telemetry、tool lifecycle notification；
- `ToolOutput` 区分 log representation、model-facing response 与 host metadata。

这些实现非常清楚地表明：

> Tool Execution 是一个受控调用生命周期，而不是函数调用语法糖；它不天然提供跨系统原子事务。

</details>

具体实现以[固定源码与官方索引](../../../references/agent/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 13. HUMAN-A 信号

- `AGENT-020` Tool Call Failure Handling：27 来源；
- `AGENT-038` Runtime Resilience Policy：15 来源；
- Verified Chain 多次出现 `Tool Failure → Retry/Fallback → Permission/Stop`。

这里必须保持两个层级：

```text
本章
= 单次 Tool Invocation 的错误语义

后续 Routing / Resilience 章
= 跨 Tool / Model / Provider 的整体恢复策略
```

---

<a id="interview"></a>

## 14. 面试怎么答

### Q：一次工具调用怎样从请求走到可用结果？

🎯 **30 秒回答**：

> 一次 Tool Call 应被 Runtime 当成完整 Invocation：解析、路由、参数校验、授权、执行、结果校验、Trace（执行追踪），再把规范化 Observation（观察结果） 回填给模型。失败要分类，Invalid Arguments 更适合 Repair，临时依赖故障才可能 Retry（重试）；涉及副作用时必须先判断幂等、执行是否已开始以及结果是否只是丢失，不能见异常就盲重试。

### Q：工具出错后，所有错误都交给模型吗？

🎯 **30 秒回答**：

> 不是。可修复参数或业务信息不足，可以提供简短反馈让模型选择合法下一步；临时传输故障通常先由程序有限恢复；权限拒绝、取消和宿主故障由控制系统处理。必须区分模型、运行状态、用户界面与诊断通道，并脱敏，不能让模型拿内部堆栈无限重试。

### Q：哪些错误可以自动重试？

🎯 **30 秒回答**：

> 不仅看错误码。需要同时确认错误可能是暂时的、动作可安全重复或下游支持幂等、先前结果不是尚未核对的未知写入，并且剩余deadline和重试预算允许。500、429或timeout都不自动保证安全；未知副作用应先核对。

### Q：工具HTTP成功但没有生成目标文件怎么办？

🎯 **30 秒回答**：

> 这只说明请求层完成，工具结果契约未满足。程序应检查预期产物或业务状态，再把明确的失败或缺口回填；不能把HTTP200、退出码0与任务验收成功混在一起。也不应随意重复有副作用的动作来碰运气。

### Q：怎样设计工具结果的多种表示？

🎯 **30 秒回答**：

> 内部结果保留程序需要的状态与回执；模型侧保留足够继续工作的摘要和引用；Trace侧记录耗时、阶段与错误类别，敏感载荷按需授权保存。这样既能调试，又不让日志无限膨胀或把秘密和大输出注入上下文。

### 🔍 继续追问与下一步

```text
两个 Tool 可以并发吗？
写文件 Tool 和读文件 Tool 怎样调度？
用户取消时怎样传播？
后台 Tool 怎样汇报进度？
```

下一章进入 Side Effect / Concurrency / Cancellation。

---

<a id="pitfalls"></a>

## 15. 高频易错点

⚠️ Exception = Retry——错；

⚠️ Timeout = Tool 没执行——错；

⚠️ HTTP 200 = Result 可用——错；

⚠️ Post Hook Block = 副作用没发生——错；

⚠️ Tool Output = Log String——错。

⚠️ **异常都可让模型自己修。** 模型不能修复凭证权限、宿主状态损坏或已发生的外部动作。

⚠️ **timeout表示没有执行。** 可能已成功但回包丢失，需核对。

⚠️ **工具自己说可重试就立即重试。** 需要可信程序结合副作用与预算判定。

⚠️ **日志、用户消息、模型Tool Result可以共用全部原始内容。** 它们的权限、长度与用途不同，应分别投影。

---

<a id="self-test"></a>

## 16. 本章自测

<details><summary>1. 自测：为什么 Timeout 后最危险的是直接 Retry 写操作？</summary>

因为 Timeout 只代表调用方没及时拿到结果，外部系统可能已经提交副作用。没有 idempotency key、operation status 或 ledger 时直接重试可能造成重复写。

</details>

<details><summary>2. 参数缺失和HTTP临时断连，为什么处理不同？</summary>

缺参需要改变候选；临时断连可能重试原请求。把缺参请求原样重复只会继续失败，把网络错误都交模型重新规划也会增加成本和不确定性。

</details>

<details><summary>3. 权限拒绝后模型提议调用另一个同能力工具，可以吗？</summary>

只有另一个动作本身在合法范围内才可执行，不能把替代工具当作绕过权限的方式。授权应针对真实目标和身份，而非仅针对工具名字。

</details>

<details><summary>4. 邮件发送超时，重试前问什么？</summary>

问请求是否可能已到下游、能否用稳定操作身份查询结果、下游是否支持幂等。不能每次生成新邮件ID再发送，否则查询与去重关系会丢失。

</details>

<details><summary>5. 工具错误能否直接包含环境变量？</summary>

不应。模型反馈和用户错误只需可行动信息；内部诊断也需要脱敏、访问控制及短保留。凭证不能因为调试方便而扩散。

</details>

<details><summary>6. 工具执行成功与任务成功哪里不同？</summary>

工具只完成局部契约，如读取文本或生成文件；任务还要检查整体目标，如来源支持结论。局部结果是完成证据之一，不是全部验收。

</details>

<details><summary>7. 发生不可恢复状态损坏，应该要求模型换Prompt吗？</summary>

不应该。它是程序正确性问题，应停止或隔离受影响执行并由维护者处理。继续让模型调用工具可能扩大损坏，不能用自然语言自救代替可信状态检查。

</details>

---

[← 上一章](05-ToolRegistrationAndDiscovery.md) · [Agent 目录](../README.md) · [下一章 →](07-ToolConcurrencyAndCancellation.md)
