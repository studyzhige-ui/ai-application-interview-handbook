# 44｜Agent Evaluation、Benchmark 与 Outcome Verification

## 1. 最大原则

> Agent 说“完成了”不等于任务完成。

Anthropic Agent Evals 把 transcript 和 environment outcome 明确区分：真正评价的是最终环境状态。

## 2. Eval 四层

```text
Decision / Tool Selection
Trajectory / Process
Artifact Quality
Environment Outcome
```

不同任务重点不同。

## 3. Dataset 从哪里来

- 真实线上任务脱敏；
- 历史失败 Case；
- 人工构造 edge case；
- benchmark；
- regression cases。

不要只用 10 个 happy path。

## 4. Grader

### Deterministic

```text
test passed
DB row exists
file content matches
HTTP result
```

优先。

### LLM Judge

适合主观质量，但要校准：

- rubric；
- pairwise / reference；
- judge model drift；
- human sample audit。

## 5. Agent Harness 也要 Eval

同一 Model，改变 Tool description、Context、Compaction、Loop policy，都可能改变成功率。

因此我们评的是：

```text
Model + Harness + Tools + Environment
```

## 6. SWE-bench 的启发

Coding Eval 用真实 issue + repo + test/patch outcome，说明“可验证环境结果”比问模型自己是否修好可靠得多。

## 🎯 面试

Agent Eval 要分 trajectory 和 outcome。我优先用 deterministic environment grader 验证真实结果，再用 LLM Judge 补主观质量；Dataset 来自真实任务和 Bad Case，并对 Context、Tool、Model、Harness 改动做 regression。

<details><summary>自测：Tool Call Accuracy 100% 是否代表 Agent 成功？</summary>

不代表。工具都调用“正确”仍可能没有完成最终业务目标，必须看 environment outcome / artifact。
</details>
