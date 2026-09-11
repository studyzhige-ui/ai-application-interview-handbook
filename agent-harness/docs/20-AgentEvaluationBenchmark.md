# 20｜Agent Evaluation、Benchmark 与 Data Flywheel

> 本章把 Agent Evaluation、Benchmark Engineering 与 Self-evolution / Data Flywheel 放在一个闭环里：**先定义什么叫成功，再构造代表真实任务的数据集，最后用线上 Bad Case 持续改进并 Regression。**

## 1. Agent Eval 不能只看 Final Answer 文本

Agent 是执行系统，因此至少分四层：

```text
Outcome
Process
Tool / Routing
Cost / Reliability
```

### Outcome

任务真的完成了吗？

### Process

是否出现无效循环、危险步骤、过多 Replan？

### Tool / Routing

正确 Tool 被发现了吗？参数对吗？Fallback 合理吗？

### Cost / Reliability

Latency、Token、Cost、Retry、Failure 是否可接受？

## 2. Final Answer ≠ Outcome

Coding Agent 说：

> “Bug 已修复。”

应该验证：

```text
test pass
diff correct
regression absent
acceptance criteria met
```

客服 Agent 说：

> “退款已完成。”

应该查业务系统 Outcome，而不是只给语言分。

## 3. Evaluation Harness 与 Agent Harness

```text
Agent Harness
= 执行任务

Evaluation Harness
= 构造环境、输入、grader、outcome check、metrics
```

二者职责不同。

Anthropic Agent Eval 工程资料也明确区分 transcript、environment outcome、agent harness、evaluation harness / suite。

## 4. Benchmark Dataset 怎么构建

来源：

```text
real production tasks
historical bad cases
human-designed edge cases
security cases
long-running tasks
rare failure modes
```

每个 Case 最好包含：

```text
initial environment
input / goal
allowed tools
expected outcome
acceptance criteria
ground truth / grader
risk labels
```

## 5. Offline Case 怎么代表线上

防止 Benchmark 失真：

- 按真实流量分层采样；
- 保留长尾难例；
- 避免只选“容易有标准答案”的 Case；
- 定期加入新 Bad Case；
- 区分 regression set 和 exploration set。

## 6. Grader

可以组合：

```text
exact / rule grader
unit test / environment grader
LLM judge
human review
business outcome
```

LLM Judge 适合语义质量，但不应替代可执行 Ground Truth。

## 7. Data Flywheel

```text
Production Trace
→ Bad Case Mining
→ Attribution
→ Label / Ground Truth
→ Eval Dataset
→ Prompt / Tool / Model / Runtime Change
→ Offline Regression
→ Canary / A-B
→ Production Metrics
→ New Bad Cases
```

这才是 Agent “自我进化”的工程闭环。

## 8. 避免 Eval Overfitting

如果所有优化都针对固定 100 条 Case：

```text
score ↑
real-world quality 未必 ↑
```

需要：

```text
holdout
fresh production sample
adversarial case
periodic dataset refresh
```

## 9. HUMAN-A

- `AGENT-034` Agent Evaluation：27 来源；
- `AGENT-035` Benchmark / Dataset：12 来源；
- `AGENT-041` Data Flywheel：6 来源。

Verified Follow-up Chain 常在 Tool/Context/Failure 后追：

> “那你怎么证明这样改真的更好？”

## 10. 🎯 面试回答

> Agent Eval 要把最终 Outcome、执行过程、Tool/Route 和成本可靠性分层验证，不能只给最终文本打分。Benchmark 应从真实任务和 Bad Case 构造可复现环境与 Acceptance Criteria，优先用 Unit Test、环境状态、业务结果等可执行 grader，再辅以 LLM Judge。线上 Trace 持续挖 Bad Case，进入 Dataset、Regression、Canary/A-B 后再回线上，形成 Data Flywheel。

<details><summary>自测：为什么 Agent 自己说“完成了”不能作为 Ground Truth？</summary>

因为模型陈述只是生成结果，不是环境 Outcome；真正成功要由外部可验证状态、测试、业务结果或独立 grader 证明。
</details>