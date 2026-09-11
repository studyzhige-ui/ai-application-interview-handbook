# 20. Agent Evaluation、Benchmark 与 Data Flywheel

Agent 很容易出现一种假进步：

> Demo 看起来更聪明了，但没有人能证明整体任务成功率真的提高。

因为 Agent 的输出不是单一文本，它还包含：

```text
是否选对 Tool
是否调用成功
是否走对 Route
是否满足最终任务
是否产生错误副作用
用了多少 Token / Cost / Time
```

所以 Agent Evaluation 必须分层。

---

## 1. 先分清 Agent Harness 和 Eval Harness

Anthropic Agent Evals 官方资料明确强调区分：

```text
Agent Harness
= 让 Agent 真正执行任务的 Runtime

Evaluation Harness
= 给 Agent 提供任务环境、收集结果、运行 grader、计算 metric 的系统
```

这两个 Harness 不能混。

如果 Eval Harness 有 bug：

```text
Agent 可能没变
但分数变了
```

---

# 2. 最终结果比“模型说完成了”更重要

错误评价：

```text
Agent final answer:
“任务已经完成。”
→ pass
```

模型可能只是声称成功。

更好的 Outcome Verification：

```text
代码任务 → tests pass?
数据任务 → target rows correct?
浏览任务 → expected state exists?
客服任务 → policy + resolution satisfied?
```

原则：

> **优先评价 Environment Outcome，而不是自我报告。**

---

# 3. Eval 分四层

## 3.1 Final Outcome

```text
task_success
correctness
acceptance_criteria
```

## 3.2 Process / Runtime

```text
loop length
unnecessary steps
repeated action
recovery behavior
```

## 3.3 Component

```text
tool selection
argument validity
intent route
memory retrieval
compaction correctness
```

## 3.4 Resource / Safety

```text
latency
cost
token
tool calls
permission violation
unsafe side effect
```

最终不能只看一个总分。

---

# 4. Eval Dataset 从哪里来

HUMAN-A `AGENT-035` 直接问 Benchmark / Ground Truth。

数据集来源可以是：

```text
真实线上任务抽样
线上 Bad Case
人工设计核心能力 Case
历史 Incident
安全 / adversarial Case
边界输入
长任务 / 大 Context Case
```

最危险的做法：

```text
只用开发者自己写的 20 个 Happy Path
```

这种 Benchmark 很容易被系统“学会”。

---

# 5. Dataset 要分层采样

例如：

```text
simple 30%
medium 40%
long-horizon 20%
safety / adversarial 10%
```

还可以按：

```text
tenant
domain
tool type
repository size
language
provider
```

分桶。

如果只看 aggregate score：

```text
某个少数关键场景可能退化
```

---

# 6. Ground Truth 不一定是一个字符串

对于 Agent，Ground Truth 可能是：

```text
expected environment state
required files changed
forbidden files untouched
required API called once
final database rows
artifact exists
```

所以常见 grader：

```text
unit test
script
SQL query
filesystem diff
HTTP state check
```

往往比 LLM Judge 更可靠。

---

# 7. LLM Judge 什么时候适合

适合：

```text
开放文本质量
helpfulness
reasoning artifact quality
summary quality
```

但需要：

```text
rubric
calibration
human spot check
judge version pinning
```

不要：

```text
Agent Model
和 Judge Model
完全同源偏差
→ 就当绝对真值
```

---

# 8. Process Metric 为什么也重要

两个 Agent 最终都成功：

```text
A: 4 tool calls, $0.05, 8s
B: 37 tool calls, $1.20, 90s
```

Outcome 一样，但 Production 质量不同。

所以要看：

```text
steps
cost
latency
retries
subagents
compactions
permission prompts
```

---

# 9. Tool / Routing Eval

Tool Runtime 可以独立评：

```text
Tool selection accuracy
Argument validity
Permission correctness
Repair success rate
Timeout recovery
```

Router 可以评：

```text
intent confusion matrix
model route success
fallback rate
cost-quality frontier
```

这样 Bad Case 才能定位到组件。

---

# 10. Agent Eval 与 Trace 的关系

上一章 Trace 保存：

```text
model
context
tool
state
cost
```

Eval Harness 可以读取 Trace：

```text
Final failed
→ Tool selection correct?
→ Tool execution failed?
→ Context lost constraint?
→ Route wrong?
```

所以：

```text
Trace = evidence
Eval = judgment
```

---

# 11. Regression 为什么必须自动化

Agent 调 Prompt / Tool / Model / Compaction 任一处，都可能：

```text
修一个 Case
坏十个旧 Case
```

因此每次发布：

```text
Baseline
→ Candidate
→ Same Eval Suite
→ compare per bucket
→ block regression
```

不要只看平均分。

---

# 12. SWE-bench 为什么是重要参考

SWE-bench 用真实 GitHub Issue + Repository Environment 验证代码修改是否真正解决问题。

课程借鉴的是：

> **Coding Agent 的评价应该看 Repository / Test 环境真实结果，而不是只判断生成 Patch 看起来合理。**

这会在下一章 Coding Agent 继续展开。

---

# 13. Benchmark Contamination / Overfitting

如果团队天天盯同一批 Case 改 Prompt：

```text
Benchmark 变成训练集
```

需要：

```text
train/dev/test split
hidden holdout
rotating production sample
new bad cases
```

尤其 LLM Judge rubric 也可能被针对性优化。

---

# 14. Data Flywheel

HUMAN-A `AGENT-041` 追问 Self-evolution / Data Flywheel。

健康闭环：

```text
Production Trace
→ Failure / Bad Case
→ Attribution
→ Curated Eval Case
→ Fix Prompt / Tool / Runtime / Model
→ Offline Regression
→ Canary
→ Production Metrics
→ New Evidence
```

不是：

```text
收集所有用户数据
→ 自动训练
→ 自动上线
```

Data Flywheel 的核心是：

> **把真实失败转成可重复验证的工程资产。**

---

# 15. Online Validation

Offline 过了也要：

```text
shadow
canary
A/B
rollback threshold
```

观察：

```text
task success
user correction
cost
latency
safety incident
fallback
```

因为真实流量分布永远比离线 Dataset 更复杂。

---

# 16. Evaluation Failure Timeline

```text
T0  团队改 Prompt
T1  Demo 5 个 Case 全部变好
T2  没跑 Regression
T3  上线
T4  高频 Tool 选择准确率下降
T5  成本上涨 2x
T6  用户只看到“回答变慢”
```

根因：

```text
没有 Component + Resource Eval
```

---

# 17. HUMAN-A 信号

本章主要承接：

- `AGENT-034` Agent Evaluation：27 个独立来源；
- `AGENT-035` Benchmark Engineering：12 个；
- `AGENT-041` Data Flywheel：6 个。

真实面试已经会要求：

```text
Final Result 怎么测？
Process 怎么测？
Dataset 怎么来？
线上 Bad Case 怎么回流？
```

---

# 18. 面试怎么答

## Q：Agent 应该怎么评估？

🎯 **30 秒回答**：

> 我会把 eval 分成最终 outcome、process/runtime、component 和 resource/safety 四层。最终优先验证真实环境状态，例如测试、DB、文件或 API，而不是相信 Agent 自报成功；再看 tool selection、routing、compaction、cost、latency 等过程指标。Dataset 来自真实线上任务、Bad Case 和 adversarial case，并做 bucket/holdout。每次 Prompt/Tool/Model 改动都跑同一 regression suite，再用 canary 验证线上分布。

## Q：Data Flywheel 怎么做？

> Production trace 先做 failure attribution，把代表性失败人工/半自动整理成新的 eval case，修复后离线 regression，再灰度上线；重点是把真实失败转成可重复测试，而不是自动把所有用户数据拿去训练。

---

# 19. 高频易错点

⚠️ **Agent 自己说完成就算成功。** 必须验证 environment outcome。

⚠️ **只看 final accuracy。** 成本、步骤、Tool、Safety 也可能退化。

⚠️ **LLM Judge 就是真值。** 需要 rubric 和校准。

⚠️ **Eval Dataset 一次建好永久使用。** 会过拟合且生产分布变化。

---

# 20. 本章自测

<details><summary>1. Agent Harness 和 Eval Harness 有什么区别？</summary>

前者负责真正执行 Agent；后者负责提供任务环境、采集执行结果、运行 grader 和计算指标。Eval Harness 的正确性本身也需要验证。
</details>

<details><summary>2. 为什么 Environment Outcome 通常比 Final Text 更可靠？</summary>

Agent 可能声称已经完成，但实际文件、测试、数据库或外部系统状态并未达到目标；环境状态可以独立验证。
</details>

<details><summary>3. Data Flywheel 的核心产物是什么？</summary>

不是“更多日志”，而是经过归因、去重和标注后可重复运行的 Evaluation / Regression Case，以及对应修复和线上验证证据。
</details>
