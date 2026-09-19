# 21. Agent Evaluation、Benchmark 与 Data Flywheel

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

[← 上一章](20-TraceReplayAndDiagnosis.md) · [Agent 目录](../README.md) · [下一章 →](22-CodingAgentDelivery.md)

---

<a id="section-1"></a>

## 1. 先分清 Agent Harness 和 Eval Harness

<a id="legacy-20-01"></a>

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

### 用一次考试理解两个Harness

Agent Harness负责真的执行任务；Eval Harness（评测设施）准备题目和环境、启动试验、收集结果并评分。Grader（评分器）判断某项条件，Metric（指标）汇总测量结果。

例如检查报告引用：Agent生成报告，评分器验证引用是否有效、内容是否支持结论，评测设施汇总一组任务的表现。若评分器把空引用也当有效，分数上涨并不是Agent变强。**被测系统和测量工具都需要核对。**

---

<a id="section-2"></a>

## 2. 最终结果比“模型说完成了”更重要

<a id="legacy-20-02"></a>

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

<a id="section-3"></a>

## 3. 四个评测视角：结果、过程、组件、资源与安全

<a id="legacy-20-03"></a>

四项是互补评测视角，不是部署架构层。我们先看完成质量，再解释过程、组件、资源和安全是否退化。

### 3.1 Final Outcome

```text
task_success
correctness
acceptance_criteria
```

### 3.2 Process / Runtime

```text
loop length
unnecessary steps
repeated action
recovery behavior
```

### 3.3 Component

```text
tool selection
argument validity
intent route
memory retrieval
compaction correctness
```

### 3.4 Resource / Safety

```text
latency
cost
token
tool calls
permission violation
unsafe side effect
```

最终不能只看一个总分。

### 用同一份报告对照

| 观察 | 结果 | 过程/组件 | 资源与安全 |
|---|---|---|---|
| 正确但重复读20次同一文件 | 可能达标 | 有重复行动 | 成本/时延可能超限 |
| 文字好看但引用不存在 | 不达标 | 引用/证据校验失效 | 低成本不能弥补 |
| 内容正确但读取未授权文件 | 不可直接交付 | 授权门失效 | 安全不合格 |

先从任务契约定义“怎样算完成”，再选测量项，避免先堆指标却不知道在衡量什么。

---

<a id="section-4"></a>

## 4. Eval Dataset 从哪里来

<a id="legacy-20-04"></a>

HUMAN-A `AGENT-035` 直接问 Benchmark（基准测试） / Ground Truth。

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

<a id="section-5"></a>

## 5. Dataset 要分层采样

<a id="legacy-20-05"></a>

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

上述比例只是分桶采样的示意。不同任务分布应有不同权重；少见但高风险的安全失败可以单列，不能被大量简单题的平均值掩盖。

---

<a id="section-6"></a>

## 6. Ground Truth 不一定是一个字符串

<a id="legacy-20-06"></a>

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

<a id="section-7"></a>

## 7. LLM Judge 什么时候适合

<a id="legacy-20-07"></a>

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

Rubric（评分细则）把好坏拆成可判条件，Calibration（校准）将模型评分与人工样本比较。固定配置服务公平比较，不意味着每条事件都复制所有版本全文。

---

<a id="section-8"></a>

## 8. Process Metric 为什么也重要

<a id="legacy-20-08"></a>

两个 Agent 最终都成功：

```text
A: 4 tool calls, $0.05, 8s
B: 37 tool calls, $1.20, 90s
```

Outcome 一样，但 Production（生产环境） 质量不同。

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

<a id="section-9"></a>

## 9. Tool / Routing Eval

<a id="legacy-20-09"></a>

Tool Runtime（运行时执行系统） 可以独立评：

```text
Tool selection accuracy
Argument validity
Permission correctness
Repair success rate
Timeout recovery
```

Router（路由器） 可以评：

```text
intent confusion matrix
model route success
fallback rate
cost-quality frontier
```

这样 Bad Case 才能定位到组件。

---

<a id="section-10"></a>

## 10. Agent Eval 与 Trace 的关系

<a id="legacy-20-10"></a>

上一章 Trace（执行追踪） 保存：

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

<a id="section-11"></a>

## 11. Regression 为什么必须自动化

<a id="legacy-20-11"></a>

Agent 调 Prompt / Tool / Model / Compaction（上下文压缩） 任一处，都可能：

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

新旧版本用相同任务、可控环境和评分方法对照，并重复必要试验以区分随机波动。外部服务不可用导致的失败应标记为基础设施问题；留出未参与调Prompt的任务，检查是否只记住开发样例。

---

<a id="section-12"></a>

## 12. SWE-bench 为什么是重要参考

<a id="legacy-20-12"></a>

SWE-bench 用真实 GitHub Issue + Repository Environment 验证代码修改是否真正解决问题。

课程借鉴的是：

> **Coding Agent 的评价应该看 Repository / Test 环境真实结果，而不是只判断生成 Patch 看起来合理。**

这会在下一章 Coding Agent 继续展开。

---

<a id="section-13"></a>

## 13. Benchmark Contamination / Overfitting

<a id="legacy-20-13"></a>

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

<a id="section-14"></a>

## 14. Data Flywheel

<a id="legacy-20-14"></a>

HUMAN-A `AGENT-041` 追问 Self-evolution / Data Flywheel（数据反馈迭代闭环）。

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

假设加入Rerank后Agent成本增加、成功率没提高。先定位是候选里没有证据、排序问题、上下文丢证据还是模型忽略，不要直接说“再加一个Critic”。修改其中一个责任点，固定其他条件，做Ablation（消融对比），再在回归集确认没有伤害其他任务。

```text
坏例子 → 关联有限诊断证据 → 找到失败阶段
→ 构造可重复条件 → 修改对应机制
→ 局部验证 + 整体回归 → 小范围上线与回退
```

Data flywheel（数据改进循环）指这样的持续过程，不是把全部用户对话无条件拿去训练。收集、脱敏、授权、分布变化和隐私删除都要控制。

---

<a id="section-15"></a>

## 15. Online Validation

<a id="legacy-20-15"></a>

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

<a id="section-16"></a>

## 16. Evaluation Failure Timeline

<a id="legacy-20-16"></a>

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

| 实验 | 故意注入的条件 | 应看到什么 |
|---|---|---|
| 参数修复 | 必填参数缺失 | 有限修复，无直接执行 |
| 压缩 | 长日志挤占目标 | 关键约束保留，后续任务仍正确 |
| 恢复 | 外部成功后本地未存回执 | 核对原操作，不新建重复动作 |
| 取消 | 子工具迟到成功 | 不派发新动作，记录真实结果 |
| 记忆纠错 | 旧偏好已撤销 | 不再以旧记忆覆盖新指令 |
| 安全 | 文档伪造批准 | 真实授权门拒绝 |

表格是测试设计，不意味着本仓库已运行全部真实系统测试。教学代码的单元断言、框架集成测试和生产故障演练应分开报告。

<details>
<summary>官方框架与Benchmark提供什么，不提供什么</summary>

OpenAI Agents SDK提供Tracing等执行证据入口，评测仍需自己定义任务验收。SWE-bench原论文及基准用真实仓库问题检验代码修复，强调运行环境与测试结果；分数受数据、环境、工具与评测流程影响，不能直接外推到你的企业报告Agent。

Codex/Claude的工具、工作区和测试调用能形成验证链，但“使用了同一个产品”不等于本项目已经通过相同评测。引用固定源码是解释实现，声称质量提升必须有自己的数据与实验。

</details>

---

官方核对入口（2026-09-17，协议/产品按文中注明版本）：[Anthropic Agent Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)。

---

<a id="human-a"></a>

## 17. HUMAN-A 信号

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

<a id="interview"></a>

## 18. 面试怎么答

### Q：Agent 应该怎么评估？

🎯 **30 秒回答**：

> 我会把 eval 分成最终 outcome、process/runtime、component 和 resource/safety 四层。最终优先验证真实环境状态，例如测试、DB、文件或 API，而不是相信 Agent 自报成功；再看 tool selection、routing、compaction、cost、latency 等过程指标。Dataset 来自真实线上任务、Bad Case 和 adversarial case，并做 bucket/holdout。每次 Prompt/Tool/Model 改动都跑同一 regression suite，再用 canary 验证线上分布。

### Q：Data Flywheel 怎么做？

🎯 **30 秒回答**：

> Production trace 先做 failure attribution，把代表性失败人工/半自动整理成新的 eval case，修复后离线 regression，再灰度上线；重点是把真实失败转成可重复测试，而不是自动把所有用户数据拿去训练。

### Q：Agent评测和普通文本生成评测有何不同？

🎯 **30 秒回答**：

> 除了最终文本，还要检查行动过程、工具选择与参数、环境产物、恢复和安全预算。可确定性验证的优先用程序检查，开放语义再用校准Judge或人工；结果不以模型自称完成为准。

### Q：如何根据评测改善Agent？

🎯 **30 秒回答**：

> 先从坏例子定位失败责任，构造可重复输入与环境，修改对应组件，固定其他条件做消融，再做整体回归和小范围上线。不要看到总分低就随意换模型或堆多Agent。

### Q：LLM Judge可以做唯一评分器吗？

🎯 **30 秒回答**：

> 通常不合适。它对开放语义有价值，但可能偏好风格、受提示和模型影响；文件、测试、权限与实际副作用应由相应程序或环境证据验证，Judge需和人工校准并报告局限。

### Q：Benchmark高分能证明生产可用吗？

🎯 **30 秒回答**：

> 不能直接。任务分布、工具环境、数据污染和评测条件都可能不同，需要本业务代表样本、失败路径和线上受控验证。基准可作对照，不替代任务契约。

---

<a id="pitfalls"></a>

## 19. 高频易错点

⚠️ **Agent 自己说完成就算成功。** 必须验证 environment outcome。

⚠️ **只看 final accuracy。** 成本、步骤、Tool、Safety 也可能退化。

⚠️ **LLM Judge 就是真值。** 需要 rubric 和校准。

⚠️ **Eval Dataset 一次建好永久使用。** 会过拟合且生产分布变化。

⚠️ **模型说完成就算成功。** 完成需要外部验收证据。

⚠️ **只看平均成功率。** 长尾、风险类别和成本分布可能被掩盖。

⚠️ **有Trace就已经评测。** Trace提供过程，评测依据标准判断好坏。

⚠️ **所有坏例子都靠更长Prompt修复。** 可能是权限、数据、工具或恢复机制问题。

⚠️ **收集所有对话就是数据飞轮。** 需要授权、归因、回归与治理。

---

<a id="self-test"></a>

## 20. 本章自测

<details><summary>1. Agent Harness 和 Eval Harness 有什么区别？</summary>

前者负责真正执行 Agent；后者负责提供任务环境、采集执行结果、运行 grader 和计算指标。Eval Harness 的正确性本身也需要验证。

</details>

<details><summary>2. 为什么 Environment Outcome 通常比 Final Text 更可靠？</summary>

Agent 可能声称已经完成，但实际文件、测试、数据库或外部系统状态并未达到目标；环境状态可以独立验证。

</details>

<details><summary>3. Data Flywheel 的核心产物是什么？</summary>

不是“更多日志”，而是经过归因、去重和标注后可重复运行的 Evaluation / Regression（回归测试） Case，以及对应修复和线上验证证据。

</details>

<details><summary>4. 报告引用存在但不支持结论，哪种检查不足？</summary>

引用可解析属于结构检查，仍需语义支持验证。不能把链接存在当作事实正确。

</details>

<details><summary>5. 修改压缩算法后如何比较？</summary>

固定代表长任务、输入/工具与评分标准，重复运行比较约束遗漏、任务成功、费用与时延，并检查非长任务回归。

</details>

<details><summary>6. 为何可以没有唯一标准文本答案？</summary>

许多任务允许不同表达和实现，验收可用事实、约束和行为条件，而不是逐字比对。

</details>

<details><summary>7. 新模型只跑一次更快，是否可以宣布优化？</summary>

不能充分证明。需代表样本与多次测量，控制环境变化并比较质量与风险。

</details>

<details><summary>8. 故障测试表已经写好，能标记全部通过吗？</summary>

不能。测试设计与实际执行证据不同，需明确哪些是单元断言、集成验证或未运行的演练。

</details>

<details><summary>9. 怎么防止记住测试题而误判质量？</summary>

保留独立评估集，避免把答案混入提示或训练，并检测分布变化。基准和线上任务要分开报告。

</details>

---

[← 上一章](20-TraceReplayAndDiagnosis.md) · [Agent 目录](../README.md) · [下一章 →](22-CodingAgentDelivery.md)
