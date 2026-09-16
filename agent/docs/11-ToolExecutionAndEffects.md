# 11. L3 接入层：工具执行、副作用与取消

[← 10](10-ToolContractAndDiscovery.md) · [Agent 主线](../README.md) · [12 →](12-KnowledgeAndCapabilityAccess.md)

> 主线位置：**L3 接入层**。工具已被找到并形成请求，继续定义怎样可靠兑现这次调用。
>
> 本章产物：**调用生命周期、错误、并发、副作用与取消语义**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 按 Invocation→结果→失败→并发/取消分段读。把07章的稳定逻辑动作标识带进来：一次重试可以有新 attempt_id，但不能因此变成新的业务操作。

[从调用请求到可接受结果](#part-1) → [错误分类与有限恢复](#part-2) → [并发必须围绕资源与副作用](#part-3) → [取消、进度和最终结果](#part-4)

<a id="part-1"></a>

## 1. 从调用请求到可接受结果

L2 发出或批准调用、管理执行状态；L3 将调用转换为受控 Invocation 并连接执行后端；L4 产生真实结果。工具执行是跨层的一条链路，本章从接入边界展开。

它不是天然的分布式事务。即使所有步骤在一个 Executor 中实现，外部副作用与本地检查点仍可能不是原子的。

### 一次完整 Tool Execution

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

### Executor 为什么不应该直接暴露原始函数

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

### Tool Result 不是一段字符串

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
  "retry_hint": "requires_action_reconciliation"
}
```

### 为什么日志、模型输出、Host Metadata 应分层

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

### Result Validation

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

<a id="part-2"></a>

## 2. 错误分类与有限恢复

Repair 修改错误参数，Retry 重试有资格重试的请求，Fallback 更换能力，Fail 终止无法安全推进的动作。

### Failure Classification

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

### Repair、Retry、Fallback、Fail 不是一回事

#### Repair

模型生成的参数错：

```text
Invalid Arguments
→ structured feedback
→ model repairs arguments
```

#### Retry

相同请求可能因临时故障成功：

```text
429 / transient network / temporary unavailable
→ backoff
→ retry
```

#### Fallback

当前能力失败，换另一能力：

```text
provider A unavailable
→ provider B
```

#### Fail

继续执行没有意义或风险过大：

```text
permission denied
invalid invariant
irrecoverable state corruption
```

### Retry Eligibility 必须先判断幂等与副作用

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

### Timeout 也不是一种简单失败

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

### 错误反馈给模型应该“可行动”

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

### Pre / Post Tool Hook 为什么很有用

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

<a id="part-3"></a>

## 3. 并发必须围绕资源与副作用

工具名称不同不代表资源不冲突，只读也不保证无额度消耗。调度依据应来自可信契约及当前资源范围。

### 为什么 Tool 不能默认并发

模型一次可能给出多个 Tool Call：

```text
read_file(A)
read_file(B)
run_tests()
```

看起来可以并发。

但如果是：

```text
edit_file(A)
run_tests()
```

并发可能产生：

```text
测试读取旧文件
测试读取写到一半的文件
结果对应未知版本
```

所以并发不是“async gather 全开”。

### Tool Side Effect 分类

至少可以分：

#### Pure / Read-only

```text
search
read_file
query snapshot
```

#### Local Mutable

```text
edit workspace
write temp file
modify local cache
```

#### External Reversible

```text
create draft issue
upload temporary artifact
```

#### External Irreversible / High Risk

```text
send email
publish
charge
production delete
```

不同等级决定：

- 是否可并发；
- 是否需 Approval；
- 是否能 Retry；
- 是否需要 Compensation / Ledger。

### Concurrency Safety 应是 Tool Contract 的一部分

不要让 Scheduler 猜。

可以有：

```python
class ToolRuntime:
    def is_read_only(self, args) -> bool: ...
    def is_concurrency_safe(self, args) -> bool: ...
    def resource_keys(self, args) -> list[str]: ...
```

例如：

```text
read_file(a.py) + read_file(b.py)
→ parallel okay

edit_file(a.py) + edit_file(a.py)
→ conflict

edit_file(a.py) + run_tests(repo)
→ ordering required
```

### Resource Key 比“Tool Name”更准确

两个不同 Tool 也可能操作同一资源：

```text
apply_patch(path=a.py)
format_file(path=a.py)
```

因此冲突判断可以基于：

```text
workspace:file:a.py
repo:working-tree
customer:123
order:789
```

建立资源锁 / 调度约束。

<a id="part-4"></a>

## 4. 取消、进度和最终结果

取消是一套传播、确认、资源释放与结果核对协议，不是把状态字段改成 cancelled。进度信息不能代替最终回执。

### 用户取消为什么必须传播

用户点击 Stop 时，不能只停止下一次模型调用。

取消应该沿执行树传播：

```text
Run Cancel
   ↓
Turn / Step Cancel
   ↓
Tool Invocation Cancel
   ↓
Subprocess / Network / Subagent Cancel
   ↓
Resource Cleanup
```

否则会出现：

```text
UI 显示 cancelled
但后台 shell 还在跑
```

### Cancellation 是协议，不是一个布尔值

需要定义：

```text
谁发起？
什么时候可中断？
子任务是否继承？
正在执行副作用怎么办？
怎样清理？
结果还能否回填？
取消是否可 Resume？
```

某些 Tool 可以即时取消：

```text
search
read
```

某些操作进入 Commit Phase 后不能安全撤销：

```text
publish_release
```

这时 Runtime 更应该：

```text
mark cancel requested
→ wait for commit outcome
→ reconcile state
```

而不是假装强制取消成功。

### Parent / Child Cancellation

长任务里常有：

```text
Run
└─ Subagent
   └─ Tool
      └─ subprocess
```

理想行为：

```text
Parent Abort
→ Child Abort
```

但：

```text
Child Abort
≠ 自动取消 Parent
```

否则一个局部 Tool 失败可能杀死整个 Run。

### Progress 为什么是 Runtime Primitive

长 Tool 如果 5 分钟没有任何 Event，用户无法区分：

```text
正在工作
卡住
网络断了
worker 死了
```

所以长 Tool 可以输出：

```json
{
  "type": "tool_progress",
  "call_id": "c_17",
  "phase": "running_tests",
  "percent": 60,
  "message": "312/520 tests completed"
}
```

Progress 不一定全部进入 Model Context。

可以同时投影到：

```text
UI
Trace
Metrics
Model（必要时）
```

### Streaming Result 与 Final Result 要分开

例如 Shell：

```text
stdout chunks
stderr chunks
exit code
final summary
```

不要把所有 streaming chunk 都永久写入 Model History。

更合理：

```text
live stream → UI / artifact
final compact result → model
full output → external artifact
```

这会在 Context Offloading 章节继续使用。

### Side Effect + Cancellation 的危险窗口

最经典情况：

```text
Tool 开始写外部系统
→ 用户 Cancel
→ 外部系统提交成功
→ Runtime 没拿到结果
```

此时不能记录：

```text
cancelled = no effect
```

需要保存：

```text
operation_id
unknown outcome
reconciliation required
```

这会在 Checkpoint / Idempotency 章节进一步展开。

## 把执行结果分成事实、建议与展示

响应里的 `retryable`只能是错误处理提示，不能独自授权重放。是否重试还取决于动作类型、是否已开始、可核对性、幂等保证与剩余预算；Tool返回的文字也不能覆盖可信权限策略。

旧版Codex对照明确区分 `FunctionCallError::RespondToModel` 与 `Fatal`，以及 `ToolOutput` 的日志/模型/Host表示。这里吸收的是“可向模型反馈的局部错误”与“必须停止/上报的运行时错误”不能混为一谈；名字和具体分支仍属于固定快照，不是所有框架标准。对照入口：[Codex工具层索引](../../research/agent-sources/codex-source-index.md)。

取消测试必须覆盖：提交前取消、等待执行时取消、执行中合作式取消、客户端断线但任务继续、取消后迟到成功回执。最后一种要回到07章核对动作，而不是丢弃事件并宣称没有发生。只读工具也可能泄露数据；可并发性由具体资源和输入决定，不由 `async` 关键字决定。

## 本章自测

<details>
<summary>超时是否说明动作没有发生？</summary>

不说明。调用方可能只是未收到响应，必须根据执行阶段与外部结果判断重试资格。

</details>

<details>
<summary>取消请求得到确认是否说明副作用已回滚？</summary>

不是。取消传播、真正终止与外部结果核对是独立步骤，已完成动作可能需要补偿且不一定可逆。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>Timeout回包写了retryable=true就能重试吗？</summary>

不能；提示不是授权，仍需判断动作副作用、执行阶段、幂等/核对能力和预算。

</details>

<details>
<summary>取消后远程动作成功回执晚到，应该丢弃吗？</summary>

不能；记录并核对外部结果，停止后续动作，必要时补偿或转人工。

</details>

[本章面试练习与具体追问](../interview/README.md#chapter-11) · [综合复习](../review/README.md)

## 回到主线

现在应能独立说明：调用生命周期、错误、并发、副作用与取消语义。下一章：[L3 接入层：知识、记忆与扩展能力接入](12-KnowledgeAndCapabilityAccess.md)。

对应真人问题：`AGENT-020`、`AGENT-026`。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 10](10-ToolContractAndDiscovery.md) · [Agent 主线](../README.md) · [12 →](12-KnowledgeAndCapabilityAccess.md)
