# 06｜Tool Execution、Result 与 Failure Semantics

> 本章合并旧 `10-ToolExecutionResult` 与 `11-ToolFailureTimeoutRetry`。Tool Call 真正困难的地方不是“调到函数”，而是**Runtime 怎样把一次调用从请求推进到可解释结果，并正确区分可修复失败、可重试失败和致命失败。**

## 1. 一次完整 Tool Execution

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

## 2. Executor 为什么不应该直接暴露原始函数

如果 Runtime 只是：

```python
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

更合理的是显式 Invocation：

```python
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

Executor 接收 Invocation，而不是只接收业务参数。

## 3. Tool Result 不是一段字符串

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

## 4. 为什么日志、模型输出、Host Metadata 应分层

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
- Replay 不可靠。

## 5. Failure Classification

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

## 6. Repair、Retry、Fallback、Fail 不是一回事

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

## 7. Retry Eligibility 必须先判断幂等与副作用

错误做法：

```python
for _ in range(3):
    try:
        return await call_tool()
    except Exception:
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

## 8. Timeout 也不是一种简单失败

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

## 9. 错误反馈给模型应该“可行动”

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

## 10. Result Validation

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

## 11. Pre / Post Tool Hook 为什么很有用

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

> Post Tool Hook 如果 block，实际外部副作用可能已经发生。

不能把“结果没有回给模型”误解成“Tool 没执行”。

## 12. 源码证据：Codex

固定快照中：

- `ToolRouter` 把 `ResponseItem` 规范化成带 `tool_name / call_id / payload` 的 `ToolCall`；
- `ToolRegistry` 负责 dispatch；
- `CoreToolRuntime` / `ToolExecutor` 提供统一执行接口；
- `FunctionCallError` 至少区分 `RespondToModel` 与 `Fatal`；
- Registry 执行链有 pre/post tool hooks、telemetry、tool lifecycle notification；
- `ToolOutput` 区分 log representation、model-facing response 与 host metadata。

这些实现非常清楚地表明：

> Tool Execution 是一个 Runtime Transaction，而不是函数调用语法糖。

## 13. HUMAN-A 对应

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

## 14. 🎯 30 秒回答

> 一次 Tool Call 应被 Runtime 当成完整 Invocation：解析、路由、参数校验、授权、执行、结果校验、Trace，再把规范化 Observation 回填给模型。失败要分类，Invalid Arguments 更适合 Repair，临时依赖故障才可能 Retry；涉及副作用时必须先判断幂等、执行是否已开始以及结果是否只是丢失，不能见异常就盲重试。

## 15. ⚠️ 易错点

- Exception = Retry——错；
- Timeout = Tool 没执行——错；
- HTTP 200 = Result 可用——错；
- Post Hook Block = 副作用没发生——错；
- Tool Output = Log String——错。

## 16. 🔍 继续追问

```text
两个 Tool 可以并发吗？
写文件 Tool 和读文件 Tool 怎样调度？
用户取消时怎样传播？
后台 Tool 怎样汇报进度？
```

下一章进入 Side Effect / Concurrency / Cancellation。

<details><summary>自测：为什么 Timeout 后最危险的是直接 Retry 写操作？</summary>

因为 Timeout 只代表调用方没及时拿到结果，外部系统可能已经提交副作用。没有 idempotency key、operation status 或 ledger 时直接重试可能造成重复写。
</details>