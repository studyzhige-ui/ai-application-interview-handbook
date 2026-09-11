# 10. Tool Executor / Result：从模型意图到真实环境动作

前两章解决了：

```text
Tool 是什么协议？
Registry 里有哪些 Tool？
Router 应该把 Call 交给谁？
```

这一章进入最关键的执行边界：

> **Tool Executor 怎样把一个经过校验的 Tool Call 变成真实环境动作，又怎样把复杂结果安全地转换成 Model-visible Result？**

`AGENT-018` Tool Calling Protocol 有 **29 个 HUMAN-A 来源**。面试官如果继续深挖，通常会追到 Execution、Result、Error、Permission 和 Context。

---

# 1. 先讲人话：模型输出的是“意图”，Executor 才产生“事实”

模型说：

```json
{
  "tool": "run_test",
  "arguments": {
    "target": "tests/test_users.py"
  }
}
```

这只是：

> “模型希望运行测试。”

真正发生：

```text
在哪台机器？
哪个 workspace？
什么 cwd？
哪些 env？
权限是什么？
Sandbox 什么策略？
Timeout 多久？
Stdout/Stderr 如何捕获？
进程 Exit Code 是多少？
输出太长怎么办？
```

这些全部属于 Executor / Execution Environment。

---

# 2. Tool Execution 的标准路径

推荐理解成：

```text
Validated ToolCall
      ↓
Build Execution Context
      ↓
Permission / Approval
      ↓
Acquire Execution Resource
      ↓
Execute
      ↓
Collect Raw Output
      ↓
Normalize ToolResult
      ↓
Persist Runtime Event / Metadata
      ↓
Project Model-visible Result
```

注意：

```text
Raw Output
≠ Model-visible Result
```

这是本章第二个核心结论。

---

# 3. Executor 为什么需要 Runtime Context

一个 Tool 的执行环境可能需要：

```text
run_id
turn_id
step_id
call_id
user / tenant
workspace
cwd
permission
sandbox policy
cancel token
trace context
secret handle
timeout
```

教学实现：

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionContext:
    run_id: str
    call_id: str
    tenant_id: str
    workspace: Path
    timeout_seconds: float
    cancel_token: object
```

然后：

```python
result = await executor.execute(call, context)
```

而不是让 Tool 从全局变量到处读取当前用户和 workspace。

---

# 4. 为什么 Tool Executor 要与 Tool Spec 分开理解

Spec 负责：

```text
模型知道什么
```

Executor 负责：

```text
系统实际怎么做
```

例如模型看到：

```text
run_test(target: string)
```

底层可以：

```text
Local subprocess
or
Docker sandbox
or
Remote worker
or
Kubernetes job
```

只要 Tool Contract 稳定，底层执行方式可以演进。

这就是：

```text
Capability Interface
vs
Execution Implementation
```

---

# 5. Local Executor 的最小例子

```python
import asyncio
from dataclasses import dataclass


@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str


async def run_command(command: list[str], cwd: str, timeout: float):
    proc = await asyncio.create_subprocess_exec(
        *command,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=timeout,
        )
    except TimeoutError:
        proc.kill()
        await proc.wait()
        raise

    return CommandResult(
        exit_code=proc.returncode,
        stdout=stdout.decode(errors="replace"),
        stderr=stderr.decode(errors="replace"),
    )
```

这还没有 Sandbox / Secret / Resource Limit，但至少体现：

- process lifetime；
- timeout；
- output collection；
- exit code。

---

# 6. Tool Result 的三种表示不要混

成熟系统经常至少有三种结果视图。

## 6.1 Authoritative Result

系统内部最完整结果：

```text
完整 stdout
完整 artifact
HTTP response metadata
external resource id
```

## 6.2 Log / Trace Representation

为了 Observability：

```text
可能做 redaction
可能截断
可能不记录 media
```

## 6.3 Model-visible Result

为了下一轮模型决策：

```text
只保留必要信息
控制 token
隐藏内部 metadata
```

如果把三者混成一个字符串，会同时伤害：

- Debug；
- Context；
- Security。

---

# 7. Codex `ToolOutput` 对这个问题的直接实现证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`codex-rs/tools/src/tool_output.rs` 的 `ToolOutput` 明确区分：

```text
log_output()
```

注释说明这是**有意有损的诊断表示**，不是 authoritative tool result。

同时还有：

```text
success_for_logging()
contains_external_context()
fallback_token_limit_override()
to_response_item()
post_tool_use_response()
code_mode_result()
tool_result_metadata()
```

这正好告诉我们：

> **同一个 Tool Result 会根据日志、模型、Hook、Code Mode、Host Metadata 等消费场景投影成不同形态。**

---

# 8. 为什么 Log Output 不能当完整结果

例如 Tool 返回图片 + 文本 + encrypted metadata。

日志可能只记录：

```text
"generated image successfully"
```

如果以后 Replay 只依赖这个字符串：

```text
真实 artifact 已经丢失
```

所以 Trace 系统需要明确：

```text
Diagnostic representation
≠ Exact evidence
```

Codex Rollout Trace 也专门区分 raw payload evidence 与 reducer 后的 conversation/tool representation。

---

# 9. Model-visible Result 应该“足够，但不一定完整”

例如 `grep` 搜索结果有 20,000 行。

直接回填：

```text
20,000 lines
```

会浪费 Context。

更合理：

```json
{
  "matches": 1843,
  "shown": 50,
  "items": [...],
  "artifact_ref": "tool-result://run_123/call_9",
  "truncated": true
}
```

模型如果需要，再：

```text
read_tool_result(ref, offset, limit)
```

这会在第 18 章 Tool Result Offloading 深挖。

---

# 10. Tool Result 里的 External Context

外部网页、MCP、Ticket、Email 都可能包含：

```text
不可信内容
Prompt Injection
过期事实
敏感数据
```

因此 Runtime 最好给 Result Metadata 标记：

```text
origin
trust level
external context
source timestamp
```

Codex `ToolOutput.contains_external_context()` 甚至会影响 Memory Generation：固定源码中，如果 Tool Output 含 external context 且相关配置开启，会把线程 memory mode 标记为 polluted。

这非常值得注意：

> **Tool Result 不只是“文本”，它还携带信任与生命周期语义。**

---

# 11. Result Normalize 为什么要稳定

不同执行器可能返回：

```text
subprocess tuple
HTTP response
MCP CallToolResult
DB rows
Python object
```

Runtime 最好归一化成内部结果协议：

```python
@dataclass
class NormalizedToolResult:
    ok: bool
    content: object | None
    error: object | None
    artifact_ref: str | None
    metadata: dict
```

模型层不应该知道：

```text
这个 Tool 底层用 requests 还是 grpc
```

---

# 12. Executor 和 Sandbox 的关系

Executor 负责：

```text
如何执行
```

Sandbox 负责：

```text
执行时物理能碰到什么
```

例如 Shell Executor：

```text
command = "pytest"
```

可能在：

```text
read-only workspace
workspace-write sandbox
network disabled container
```

所以：

```text
ToolExecutor
+ ExecutionEnvironment/Sandbox
```

经常是组合关系。

第 29 章会深入。

---

# 13. Executor 与 Permission 的顺序

高风险 Tool：

```text
send_email
```

正确：

```text
Validate
→ Permission
→ Approval if needed
→ Execute
```

错误：

```text
Execute
→ ask user whether it was okay
```

Claude Code 固定源码中的 `CanUseToolFn` 就是 Tool execution 的显式输入，说明 Tool 执行前存在独立 permission decision boundary。

---

# 14. Claude Code Permission Execution 证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`hooks/useCanUseTool.tsx` 当前直接定义：

```text
CanUseToolFn(tool, input, toolUseContext, assistantMessage, toolUseID, ...)
→ Promise<PermissionDecision>
```

实现中会处理：

```text
allow
deny
ask
abort
```

并根据 interactive / coordinator / swarm worker 等不同运行环境走不同 permission handler。

这说明执行权限不是 Tool 内部随手 `if` 一下，而可以成为独立 Runtime Policy Pipeline。

---

# 15. Codex Tool Execution Pipeline 证据

`codex-rs/core/src/tools/registry.rs` 当前 dispatch 路径包含：

```text
lookup tool
→ payload kind check
→ pre-tool-use hook
→ optional input rewrite
→ notify tool start
→ execute handler
→ telemetry
→ post-tool-use hook
→ optional feedback/block
→ notify finish
→ accepted result
```

这个顺序非常有教学价值。

它说明 Production Tool Execution 不只是：

```rust
handler(args).await
```

而是完整生命周期。

---

# 16. PostToolUse Hook 一个很细的语义

Codex Registry 固定源码里有一句注释非常重要：

> PostToolUse block rejects the result, not the already-completed tool execution.

也就是说：

```text
Tool 已经执行
→ 副作用可能已经发生
→ Post Hook 再 block
```

不能误以为：

```text
“block result = 回滚执行”
```

这直接连到后面的 Side Effect / Compensation。

Runtime 必须区分：

```text
Execution Outcome
vs
Result Acceptance / Model Visibility
```

---

# 17. Execution Result 的 Success 也不是 Task Success

Tool：

```text
apply_patch
```

返回 success：

```text
patch applied
```

不代表：

```text
Bug fixed
```

还要：

```text
run test
review diff
verify outcome
```

所以有三层：

```text
Tool Execution Success
≠ Step Goal Success
≠ Overall Task Success
```

面试里能讲清这三层，会明显比“Tool 成功就继续”更成熟。

---

# 18. Remote Executor

当 Tool 在 Remote Worker 执行时，还要增加：

```text
request serialization
execution lease
worker identity
heartbeat
network timeout
result callback / polling
idempotency
artifact storage
```

逻辑仍然是 Tool Executor，但物理执行已经是分布式系统问题。

Production Architecture 章节会再收束。

---

# 19. Executor Resource Control

Tool 可能消耗：

- CPU；
- Memory；
- Disk；
- Network；
- API Quota。

因此 Execution Context 可以携带：

```text
wall clock timeout
cpu quota
memory limit
network policy
output limit
```

否则一个 Agent Tool 可以拖垮整个 Harness Worker。

---

# 20. AI 应用场景：SQL Tool

模型请求：

```json
{
  "query": "SELECT ..."
}
```

Executor 不应该：

```python
cursor.execute(model_sql)
```

直接跑。

应该至少：

```text
Validate query kind
→ Permission / DB scope
→ read-only connection
→ statement timeout
→ row limit
→ execute
→ normalize rows
→ truncate / artifact offload
→ model-visible summary
```

如果是写 SQL：

- Approval；
- transaction；
- idempotency；
- audit；

要求更高。

---

# 21. 高频易错点

⚠️ **Model Tool Call = Tool 已执行**  
前者只是请求/意图。

⚠️ **Raw Tool Output 全部回填模型**  
Context 会爆炸，也可能泄露敏感数据。

⚠️ **Log = authoritative result**  
日志往往是有损、截断、脱敏表示。

⚠️ **Post Hook block 能回滚 Tool**  
不一定。Tool 可能已经产生副作用。

⚠️ **Tool success = task success**  
还需要更高层 Outcome Verification。

---

# 22. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Tool Executor 是模型意图和真实环境之间的执行边界。经过 schema/policy 后，Executor 在明确的 workspace、sandbox、timeout、cancel context 中执行，再把 raw result 归一化。Production 里我会区分 authoritative result、log/trace representation 和 model-visible result，避免大结果、敏感信息和不可信外部内容直接进入 Context。

## Level 2｜2–3 分钟

> 我会把 Tool Spec 与 Executor 解耦，同一个 run_test spec 可以底层跑 local subprocess 或 remote sandbox。执行链是 validate → permission/approval → acquire environment → execute → collect → normalize → persist event → project result。Result 要带 call_id、success/error、artifact ref 和 metadata。Tool Output 成功只代表这次动作执行成功，不代表整体任务完成，还要做 outcome verification。

## Level 3｜继续追问

🔍 **为什么 Log Output 不应该复用 Model Result？**  
日志侧需要诊断和脱敏，模型侧需要 Token-efficient decision context，二者目标不同。

🔍 **PostToolUse block 后副作用怎么办？**  
不能假设回滚；要用 idempotency/compensation/transaction 等手段处理。

🔍 **Remote Tool Executor 额外难点？**  
Lease、worker failure、network retry、idempotency、artifact store、cancel propagation。

---

# 23. 本章证据

## HUMAN-A

- `AGENT-018` Tool Calling Protocol：29 sources；
- `AGENT-020` Tool Failure：27 sources；
- `AGENT-028` Permission / Sandbox：20 sources。

## Claude Code

- `Tool.ts`
- `hooks/useCanUseTool.tsx`
- `Task.ts`

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

## OpenAI Codex

- `codex-rs/tools/src/tool_executor.rs`
- `codex-rs/tools/src/tool_output.rs`
- `codex-rs/core/src/tools/registry.rs`

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

---

# 24. 自测

<details><summary>1. 为什么 Raw Tool Output 不应该直接等于 Model-visible Result？</summary>

Raw Output 可能过大、含敏感/内部 metadata 或不可信内容；模型只需要支持下一步决策的受控投影。日志、模型、Host 也可能需要不同表示。
</details>

<details><summary>2. Tool Execution Success 和 Task Success 有什么区别？</summary>

前者只说明某个动作成功执行，例如 patch 写入成功；Task Success 要验证更高层目标，例如测试通过、业务状态正确。
</details>

<details><summary>3. 为什么 Permission 应在 Executor 前？</summary>

Permission 是决定这次动作是否允许发生；如果先执行再判断，副作用已经产生，安全控制失去意义。
</details>

<details><summary>4. PostToolUse Hook block 是否意味着 Tool 没执行？</summary>

不一定。像 Codex 当前实现中，PostToolUse 是执行后阶段，block 可以拒绝结果进入后续流程，但不能自动撤销已经发生的外部副作用。
</details>
