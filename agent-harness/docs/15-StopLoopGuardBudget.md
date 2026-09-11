# 15. Stop Condition / Loop Guard / Budget：Agent 什么时候必须停

`AGENT-006` 在冻结 HUMAN-A 中有 **15 个独立来源**。它经常以非常具体的形式出现：

```text
Agent 死循环怎么办？
一直重复调用同一个 Tool 怎么办？
怎样防止越做越偏？
什么时候强制停止？
怎么控制 Token / Cost / Step？
```

一个 Agent 如果只有：

```python
while not model_says_done:
    continue
```

就把“是否继续执行”的全部控制权交给了模型。

Production Runtime 不能这样做。

---

# 1. 先讲人话：Stop 不是一个条件，而是多层安全网

Agent 结束通常有三类原因：

```text
A. 正常完成
B. 等待外部输入
C. Runtime 强制终止
```

进一步：

```text
正常完成
→ verified success

等待
→ approval / user / external event

强制终止
→ step budget / time / cost / loop / cancel / fatal
```

因此：

> **Stop Condition 是 Runtime Policy，不应该只依赖模型自报 Done。**

---

# 2. 为什么“模型说完成”不够

模型可能：

```text
过早结束
```

例如：

```text
“测试已通过”
```

但实际上没运行测试。

也可能：

```text
永远不结束
```

例如不断：

```text
search → read → search → read
```

所以需要：

```text
Model Stop Signal
+ Runtime Guard
+ Outcome Verification
```

---

# 3. Runtime 的八种 Stop Guard

## 3.1 Max Step

```text
step_count >= 30
→ stop
```

最简单，也最重要。

不能解决所有问题，但能防无限循环。

---

## 3.2 Wall-clock Deadline

```text
run started 10 minutes ago
deadline = 10 minutes
→ stop
```

适合控制 SLA 和 Worker 占用。

---

## 3.3 Token Budget

```text
input_tokens + output_tokens >= budget
```

避免长任务无限消耗。

---

## 3.4 Monetary Cost Budget

如果不同模型/Tool 有成本：

```text
estimated_cost_usd >= 2.0
→ pause / stop / downgrade
```

---

## 3.5 Tool-call Budget

例如：

```text
web_search <= 20
browser_action <= 100
```

某些 Tool 比 Model Call 更昂贵或风险更高。

---

## 3.6 Repeated Action Guard

```text
same tool + same normalized args
重复 N 次
→ block / feedback / stop
```

---

## 3.7 No-progress Guard

即使每次调用参数略有变化，也可能没有实际进展。

例如：

```text
连续 10 次 search
没有新 artifact
没有 plan step 完成
没有新 test evidence
```

可以判定：

```text
stalled
```

---

## 3.8 Cancellation / Fatal

```text
user cancel
parent cancel
runtime fatal
security violation
```

必须优先停止。

---

# 4. Max Step 不是最终方案

如果只设：

```text
max_steps = 100
```

Agent 可能：

```text
前 99 步都在浪费钱
```

所以 Max Step 只是 Hard Guard。

还需要 Soft Guard：

```text
repeated failure
no progress
cost acceleration
goal drift
```

越早发现越好。

---

# 5. Dead Loop 的典型模式

## 5.1 Exact Repetition

```text
read_file("missing.py")
→ not found
read_file("missing.py")
→ not found
```

最容易检测。

## 5.2 Near Repetition

```text
search("auth bug")
search("authentication bug")
search("login auth issue")
```

参数不同，但语义接近。

## 5.3 Oscillation

```text
edit A → edit B → revert A → revert B
```

## 5.4 Circular Delegation

```text
Agent A → Agent B
Agent B → Agent A
```

## 5.5 Plan Thrashing

```text
Plan v1 → v2 → v3 → v4
```

一直规划，不执行。

---

# 6. Repetition Fingerprint

最简单：

```python
import json
import hashlib


def action_fingerprint(tool_name, args):
    normalized = json.dumps(args, sort_keys=True)
    raw = f"{tool_name}:{normalized}"
    return hashlib.sha256(raw.encode()).hexdigest()
```

记录最近：

```text
fingerprint
error kind
result digest
```

如果：

```text
same fingerprint + same failure
```

重复多次，Runtime 可以反馈：

```json
{
  "error_type": "repeated_action",
  "message": "same failing action has already been attempted 3 times"
}
```

---

# 7. No-progress 比 Repetition 更难

Agent 可能每一步都不重复，但一直没有接近目标。

需要定义“Progress Evidence”。

Coding Agent 可以看：

```text
new failing test understood
new file identified
patch created
test count improved
plan step completed
```

Research Agent 可以看：

```text
new authoritative source
claim verified
uncertainty reduced
```

因此：

> **Progress Metric 必须跟任务类型有关。**

---

# 8. Goal Drift

`AGENT-007` 有 **4 个 HUMAN-A 来源**，频率不算最高，但非常重要。

例如 Goal：

```text
修复一个分页 Bug
```

Agent 后来开始：

```text
重构 ORM
升级框架
重写 API
```

这就是 Goal Drift。

可以通过：

```text
immutable original goal
critical constraints
plan scope
periodic goal check
```

约束。

---

# 9. Goal 应该成为 Runtime State 的一等对象

不要只放在第一条 User Message，然后让它被 200 条历史淹没。

可以保存：

```python
@dataclass
class GoalState:
    original_goal: str
    constraints: list[str]
    success_criteria: list[str]
```

每次 Context Assembly 都可以重新注入关键部分。

这也是 Context Compaction 时必须保护的内容。

---

# 10. Budget 不是只有 Token

Production Agent Budget 可以有：

```text
Step Budget
Token Budget
Dollar Budget
Wall-clock Budget
Tool-call Budget
External API Budget
Subagent Budget
Sandbox CPU/Memory Budget
```

不同任务需要不同组合。

例如 Coding Agent：

```text
max 40 steps
max 15 minutes
max 3 subagents
max 20 test runs
```

---

# 11. Budget 应该可以分配给 Subagent

Parent：

```text
total budget = $5
```

不能让：

```text
Subagent A = $5
Subagent B = $5
Subagent C = $5
```

否则总成本越界。

需要：

```text
parent remaining budget
→ child allocation
→ child usage accounted back
```

这叫 Budget Hierarchy。

---

# 12. Soft Limit 与 Hard Limit

## Soft Limit

例如剩余 20% Budget：

```text
提醒模型收敛
降低搜索范围
切换便宜模型
停止 spawn subagent
```

## Hard Limit

```text
budget exhausted
→ no further model/tool execution
```

只用 Hard Limit 会突然终止，用户体验差。

Soft Limit 允许 Graceful Degradation。

---

# 13. Budget 触发后不一定直接 Fail

可以进入：

```text
PARTIAL / NEEDS_USER / BUDGET_EXHAUSTED
```

然后输出：

```text
已完成什么
未完成什么
当前证据
继续需要什么
```

比：

```text
500 Internal Error
```

更合理。

---

# 14. Claude Code 的 Budget 证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`QueryEngineConfig` 直接包含：

```text
maxTurns?
maxBudgetUsd?
taskBudget?
```

`ToolUseContext` 也携带 `maxBudgetUsd`。

这说明成熟 Coding Agent Runtime 把 Budget 当作明确配置，而不是 Prompt 里的软建议。

---

# 15. Codex 的 Runtime Budget / Stop 证据

固定 commit：

```text
fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

`compact.rs` 当前错误处理里能看到：

```text
SessionBudgetExceeded
ContextWindowExceeded
TurnAborted
Interrupted
```

Tool Router dispatch 也携带：

```text
terminal_outcome_reached
```

用于确保 Tool lifecycle terminal outcome 只被一个路径认领。

这些具体实现说明：

> **停止、预算和终止状态需要 Runtime 显式建模。**

---

# 16. Loop Guard 与 Tool Failure 联动

Tool 失败：

```text
not_found
```

第一次：

```text
允许模型 Repair
```

第三次同样失败：

```text
Runtime 提示 repeated failure
```

第五次：

```text
禁止继续调用 / stop
```

所以 Loop Guard 不是独立组件，它消费：

- Tool Error；
- Action Trace；
- Plan Progress；
- Budget Usage。

---

# 17. Loop Guard 与 Compaction 的关系

Compaction 后如果丢失：

```text
“Tool X 已经失败 4 次”
```

模型可能重新开始撞墙。

所以关键 Loop State 应该：

```text
保存在 Runtime State
```

而不是只依赖 History。

例如：

```text
failure counters
action fingerprints
budget usage
plan progress
```

都不应因 Context 压缩而消失。

---

# 18. Loop Guard 与 Memory 的关系

不要把临时 Failure Counter 写成长期 Memory：

```text
“search_code 永远失败”
```

可能只是本次 Session 暂时故障。

所以：

```text
Runtime State
≠ Long-term Memory
```

Guard State 通常是 Run-scoped。

---

# 19. 一个 Loop Guard 示例

```python
class LoopGuard:
    def __init__(self, max_steps=30, max_same_action=3):
        self.max_steps = max_steps
        self.max_same_action = max_same_action

    def check(self, state, next_action):
        if state.step_count >= self.max_steps:
            return "max_steps"

        fp = fingerprint(next_action)
        if state.action_counts.get(fp, 0) >= self.max_same_action:
            return "repeated_action"

        if state.cancel_requested:
            return "cancelled"

        if state.budget.exhausted():
            return "budget_exhausted"

        return None
```

Production 还需要：

- no-progress；
- deadline；
- security；
- child budgets；
- goal drift；
- graceful stop。

---

# 20. Stop Result 也要结构化

例如：

```json
{
  "status": "budget_exhausted",
  "completed": [
    "identified root cause",
    "implemented patch"
  ],
  "remaining": [
    "full regression test"
  ],
  "evidence": [
    "target test passed"
  ]
}
```

这样用户可以决定：

```text
继续
扩大预算
人工接手
```

---

# 21. Outcome Verification 决定“正常结束”

例如任务：

```text
修复 Bug
```

Stop Criteria 不应该只是：

```text
model says done
```

可以是：

```text
target test passes
AND
no new lint failure
AND
patch exists
```

模型 Final 只是触发：

```text
verify completion
```

不是完成本身。

---

# 22. 动态 Stop Policy

不是所有任务都 `max_steps=30`。

可以根据：

```text
task class
risk
cost
user plan
model capability
```

分配：

```text
简单问答 → 3 steps
repo bugfix → 40 steps
long-running migration → checkpointed multi-run
```

但动态 Budget 也必须有全局上限。

---

# 23. 一个 Agent 卡住时的 Runtime 处理

检测：

```text
过去 8 step：
- 5 次 search
- 3 次 read
- 0 plan progress
- 0 artifact change
```

Runtime 可以给模型注入：

```text
You have made no measurable progress in the last 8 steps.
Do not repeat the same search strategy.
Choose one of: change approach, ask user, or stop with partial result.
```

再给 2–3 步机会。

如果仍无进展：

```text
stop
```

这比直到 max_steps=100 更好。

---

# 24. 高频易错点

⚠️ **模型说 Done = 任务成功**  
必须做 Outcome Verification。

⚠️ **有 max_steps 就解决死循环**  
只能最终兜底，不能及时识别 no-progress / oscillation。

⚠️ **Budget = Token**  
还包括时间、Dollar、Tool、Subagent、资源。

⚠️ **Stop = Failed**  
可能是 waiting approval、partial、budget exhausted、cancelled。

⚠️ **Guard State 只存在 History**  
Compaction 后会丢，应该结构化保存。

---

# 25. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Agent Stop 不能只依赖模型自报 Done。我会有三层：模型终止信号、Runtime Guard、Outcome Verification。Guard 包括 max step、deadline、token/cost/tool/subagent budget、重复 action、no-progress、cancel 和 fatal。对于死循环还会做 action fingerprint 和 progress evidence；达到 soft limit 先收敛/降级，hard limit 才强制停止。

## Level 2｜2–3 分钟

> 我会把 original goal、constraints、budget、action counters、failure fingerprints 和 progress 放在 Run State，而不是只在 history。Tool 同样失败多次后先反馈模型改路，再触发 stop。预算做层级管理，Parent 给 Subagent 分配子预算，避免成本放大。最终模型说 Final 后，Runtime 运行 verifier，根据 Test/Artifact/Business State 判断是否真正 success，否则继续或失败。

## Level 3｜继续追问

🔍 **怎么判断 no-progress？**  
按任务定义 progress evidence，例如 Coding 看 patch/test/plan-step，Research 看新证据和不确定性下降。

🔍 **Soft Limit 有什么用？**  
提前收敛、禁用昂贵能力、切便宜模型，避免突然硬停。

🔍 **Goal Drift 怎么处理？**  
固定 original goal/constraints，周期性比对当前 plan/action 是否仍服务目标，越界时 replan/stop/ask user。

---

# 26. 本章证据

## HUMAN-A

- `AGENT-006` Stop / Dead Loop / Oscillation：15 sources；
- `AGENT-007` Goal Drift：4 sources；
- `AGENT-038` Runtime Resilience：15 sources。

## Claude Code

`QueryEngineConfig`：`maxTurns`, `maxBudgetUsd`, `taskBudget`。

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

## OpenAI Codex

`SessionBudgetExceeded` / `TurnAborted` / `Interrupted` / terminal outcome tracking。

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

---

# 27. 自测

<details><summary>1. 为什么模型 Final 不能直接等于 Task Success？</summary>

模型只是声明自己认为可以结束；Runtime 还要根据测试、artifact、业务状态等外部证据验证成功条件。
</details>

<details><summary>2. Max Step 为什么不够？</summary>

它只能防止无限运行，不能提前识别重复失败、oscillation、no-progress 和 goal drift，可能在达到上限前已经浪费大量成本。
</details>

<details><summary>3. Budget 为什么要做 Parent/Child 分层？</summary>

Multi-Agent 中如果每个 Child 都拥有完整 Parent Budget，总成本会成倍放大。需要分配子预算并汇总使用量。
</details>

<details><summary>4. Loop Guard 的状态为什么不能只放 Context？</summary>

Context 会被裁剪/压缩；failure counter、action fingerprint、budget usage 等正确性状态必须持久存在于 Runtime State。
</details>
