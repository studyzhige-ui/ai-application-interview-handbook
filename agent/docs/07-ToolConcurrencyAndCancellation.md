# 07. Tool Control：副作用、并发、取消与进度

两个工具同时执行，看起来更快；用户按下取消，看起来应该立即停下。但只要工具会写文件或调用外部系统，真实情况就复杂起来。先看动作改变了什么，再看并发与取消怎样协调。

[← 上一章](06-ToolExecutionAndFailure.md) · [Agent 目录](../README.md) · [下一章 →](08-PlanningGoalAndControl.md)

---

<a id="section-1"></a>

## 1. 为什么 Tool 不能默认并发

<a id="legacy-07-01"></a>

并发安全先看是否读写同一资源，不能只看函数是否async。两个不同工具也可能修改同一个文件；两个只读工具也可能共享会变化的环境。

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

---

<a id="section-2"></a>

## 2. Tool Side Effect 分类

<a id="legacy-07-02"></a>

至少可以分：

### Pure / Read-only

```text
search
read_file
query snapshot
```

### Local Mutable

```text
edit workspace
write temp file
modify local cache
```

### External Reversible

```text
create draft issue
upload temporary artifact
```

### External Irreversible / High Risk

```text
send email
publish
charge
production delete
```

不同等级决定：

- 是否可并发；
- 是否需 Approval（批准）；
- 是否能 Retry（重试）；
- 是否需要 Compensation / Ledger。

---

<a id="section-3"></a>

## 3. Concurrency Safety 应是 Tool Contract 的一部分

<a id="legacy-07-03"></a>

不要让 Scheduler 猜。

可以有：

```python
# 接口示意：程序根据本次参数及资源判断并发，不仅依赖工具名称。
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

---

<a id="section-4"></a>

## 4. Resource Key 比“Tool Name”更准确

<a id="legacy-07-04"></a>

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

---

<a id="section-5"></a>

## 5. 用户取消为什么必须传播

<a id="legacy-07-05"></a>

假设用户取消报告任务，此时运行时正在等模型，模型阶段之后还有文件读取，某个工具又启动了子进程。仅把页面按钮改成“已取消”，不会通知这些活动。

```text
用户取消 → Run控制器：不再派发新动作
                 ↓
           模型请求 / 正在等待的工具
                 ↓
           子协程 / 子进程 / 子Agent
                 ↓
            各自清理与结果核对
```

Cancellation（取消）首先是停止意图。每层需要感知这个意图，并在自己有控制权的范围停止。例如取消HTTP等待可以中断本地连接，但远端服务器可能仍在执行；取消协程不能自动杀掉独立子进程，也不能撤销已发送邮件。传播是为了避免“父任务结束了，孩子还在花钱、占资源或写数据”。

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

---

<a id="section-6"></a>

## 6. Cancellation 是协议，不是一个布尔值

<a id="legacy-07-06"></a>

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

这时 Runtime（运行时执行系统） 更应该：

```text
mark cancel requested
→ wait for commit outcome
→ reconcile state
```

而不是假装强制取消成功。

先把运行标成取消中并阻止新动作；向可取消的子任务发信号；等待或超时处理清理；收集已经结束或迟到的结果；最后按业务语义标记取消完成或需要人工核对。这里的“取消完成”必须说明是本地执行已停止，还是外部动作也确认结束。

已经发生的写入可能需要 Compensation（补偿动作），例如删除刚创建的临时报告；但补偿是新的业务动作，不是时间倒流，也可能失败。邮件通常不能可靠撤回，必须如实告知。

---

<a id="section-7"></a>

## 7. Parent / Child Cancellation

<a id="legacy-07-07"></a>

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

---

<a id="section-8"></a>

## 8. Progress 为什么是 Runtime Primitive

<a id="legacy-07-08"></a>

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

---

<a id="section-9"></a>

## 9. Streaming Result 与 Final Result 要分开

<a id="legacy-07-09"></a>

例如 Shell：

```text
stdout chunks
stderr chunks
exit code
final summary
```

不要把所有 streaming chunk 都永久写入 Model History（历史记录）。

更合理：

```text
live stream → UI / artifact
final compact result → model
full output → external artifact
```

这会在 Context Offloading 章节继续使用。

进度90%不等于成功回执。最终校验仍可能失败；UI需要中间进度，模型通常只需关键阶段和最终结果。不要把每个进度片段都塞进后续上下文。

---

<a id="section-10"></a>

## 10. Side Effect + Cancellation 的危险窗口

<a id="legacy-07-12"></a>

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

这会在 Checkpoint（检查点） / Idempotency 章节进一步展开。

“已请求取消”和“外部结果待核对”可以同时成立。收到迟到回执后补齐事实，告诉用户哪些已发生、哪些没继续。取消停止后续推进，不会使已经提交的动作倒流。

---

<a id="section-11"></a>

## 11. 产品实现与官方资料对照（按需展开）

<details>
<summary>源码证据：Claude Code</summary>

<a id="legacy-07-10"></a>

固定快照的 `Tool.ts` 有：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior(): cancel | block`；
- progress callback。

`utils/abortController.ts` 还实现 Parent → Child AbortController 传播，并处理 listener 清理。

这些实现直接说明：

> Concurrency / Cancellation 属于 Tool Runtime Contract，而不是 UI 细节。

</details>

<details>
<summary>源码证据：Codex</summary>

<a id="legacy-07-11"></a>

固定快照的 `ToolRouter` / Invocation（调用实例） 会携带 `CancellationToken`，Registry（注册表） 还能查询 Tool 是否支持 parallel calls。

这支持同样的稳定抽象：

```text
Tool Scheduler
需要知道 parallel capability + cancellation token
```

</details>

具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 12. HUMAN-A 信号

- `AGENT-026` Timeout / Cancel / Interrupt / Resume（恢复执行）：10 来源；
- `AGENT-029` 外部副作用 + Resume 重复执行：6 来源；
- `AGENT-031` 多 Agent 共享 Workspace 并发：7 来源。

真人面试通常不是单问 `asyncio.cancel()`，而是继续追：

```text
取消怎样传播？
Tool 正在写怎么办？
Worker 死了怎么办？
Resume 会不会重复写？
```

---

<a id="interview"></a>

## 13. 面试怎么答

### Q：怎样设计工具并发、取消与进度？

🎯 **30 秒回答**：

> Tool Runtime 要显式管理副作用、并发和取消。并发不能只看 Tool Name，而应看 read/write semantics 和资源冲突；用户取消要从 Run 向 Tool、Subprocess、Subagent（子Agent） 传播，但副作用进入提交阶段后可能无法真正撤销，需要记录 unknown outcome 并做 reconcile。长 Tool 还应该产生结构化 progress，UI/Trace（执行追踪） 和 Model Context 可以使用不同 projection。

### Q：用户取消为什么必须传播？

🎯 **30 秒回答**：

> 一个任务通常还拥有模型请求、工具协程、子进程或子Agent。父任务不再等待并不会自动停止这些工作。运行时要停止新派发、把取消意图传给子工作、等待清理并核对迟到结果。远端动作是否真正停止需看下游能力，不能把协程取消等同于外部回滚。

### Q：哪些工具可以并发？

🎯 **30 秒回答**：

> 按真实资源和副作用判断，而不是按async或工具名称。读取不同静态资料通常容易并发；不同工具修改同一文件也会冲突。可以用单写者、工作区隔离或版本检查控制写入，并在并行完成后按调用ID关联结果、验证合并效果。

### Q：用户取消后工具又返回成功怎么办？

🎯 **30 秒回答**：

> 不能丢掉这条事实。应把迟到回执关联原操作，更新实际结果，同时禁止后续动作。若副作用已发生，按业务规则决定保留、补偿或请人处理，并准确告知用户取消的范围，而不是改成失败来掩盖成功写入。

### Q：运行中用户改了约束，怎么生效？

🎯 **30 秒回答**：

> 先把新输入绑定正确Run，区分补充、替换目标和取消；在下一安全决策点更新输入与控制状态。对可能违反新约束的活动停止派发并按可中断性处理，已发生动作需核对。不能修改已发出的模型请求来假装新约束早已生效。

---

<a id="pitfalls"></a>

## 14. 高频易错点

⚠️ 所有只读 Tool 都绝对安全并发——仍可能依赖 shared mutable environment；

⚠️ `cancelled` = 没发生副作用——错；

⚠️ progress chunk 全塞 Chat History——会污染 Context；

⚠️ 子 Tool cancel 自动 kill 整个 Run——不一定；

⚠️ `async gather` = Agent concurrency strategy——远远不够。

⚠️ **取消本地请求等于远端动作停止。** 只能确认本地停止等待，远端需单独核对。

⚠️ **只读工具没有任何风险。** 可能泄露敏感数据、消耗配额或导致过载。

⚠️ **同名工具互斥，不同名就独立。** 冲突取决于共享资源。

⚠️ **进度显示100%就是业务成功。** 仍要等待结果契约及业务验收。

---

<a id="self-test"></a>

## 15. 本章自测

<details><summary>1. 自测：为什么 Resource Key 比 Tool Name 更适合并发冲突检测？</summary>

因为不同 Tool 可能修改同一个文件、Workspace 或业务对象；冲突来自共享资源，而不是来自函数名字是否相同。

</details>

<details><summary>2. 父协程被取消，独立子进程一定退出吗？</summary>

不一定。独立进程需要显式信号、等待和必要的强制终止策略；还需处理输出与文件清理。不能把语言协程生命周期推广到整个操作系统。

</details>

<details><summary>3. 取消邮件发送后发现已送达，应怎样处理？</summary>

记录送达事实，停止进一步发送，向用户说明取消未能撤回已有邮件。可行补救依赖邮件业务，不能自动再发一封或假装没有发生。

</details>

<details><summary>4. 格式化和替换文本两个工具为什么会冲突？</summary>

它们名字不同但可能同时写同一文件，后写覆盖前写。资源身份与基线版本才是并发判定的依据。

</details>

<details><summary>5. 用户只是补充一个日期，也应停止所有工具吗？</summary>

未必。若不影响当前动作安全性，可排队到下一决策点。需要先解释输入意图和生效时机，而不是统一取消策略。

</details>

<details><summary>6. 取消完成前为什么还要处理结果？</summary>

已经提交的动作可能稍后成功，忽略结果会留下未知副作用，恢复或再次执行时可能重复。处理结果不是重新启动任务，而是核对已有事实。

</details>

<details><summary>7. 先采用串行执行是不是不专业？</summary>

不是。若任务规模小且写入冲突多，串行是降低正确性复杂度的合理基线。只有测得可并行独立工作与收益后，才承担协调成本。

</details>

---

[← 上一章](06-ToolExecutionAndFailure.md) · [Agent 目录](../README.md) · [下一章 →](08-PlanningGoalAndControl.md)
