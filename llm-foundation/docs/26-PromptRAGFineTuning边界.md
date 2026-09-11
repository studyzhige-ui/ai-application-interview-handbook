# 26｜Prompt vs RAG vs Fine-tuning：什么时候该换手段

> 很多 AI 项目最容易犯的错误，是遇到效果问题就直接问：“要不要 Fine-tune？”

正确做法是先判断：

> **问题究竟缺的是指令、知识、能力，还是系统执行。**

---

## 1. 四类问题先分清

### 1.1 指令问题

模型其实会做，但不知道你想要什么。

例如：

- 输出格式不稳定；
- 标签定义不清；
- 语气不对；
- 决策标准模糊。

优先：

```text
Prompt / Few-shot / Structured Output
```

### 1.2 外部知识问题

模型不知道：

- 公司内部文档；
- 最新政策；
- 实时订单；
- 不断更新的知识库。

优先：

```text
RAG / Tool
```

### 1.3 行为能力问题

模型长期在某个任务分布上表现差，例如：

- 特定领域表达；
- 特定格式 / 风格；
- 某类分类边界；
- 专用 Tool Use Pattern。

才开始考虑：

```text
Fine-tuning / SFT / Preference Optimization
```

### 1.4 Runtime 问题

例如：

- Tool 超时；
- 重复扣款；
- Agent 忘记 Checkpoint；
- 权限越界；

这不是 Prompt、RAG、Fine-tuning 应该解决的。

Primary 在 Backend / Agent Harness。

---

## 2. Prompt 适合什么

Prompt 的优势：

- 快；
- 成本低；
- 不需要训练；
- 易迭代；
- 易回滚。

适合：

```text
Task Definition
Output Contract
Few-shot Boundary
Reasoning Instruction
Style / Persona
```

局限：

- 每次都占 Context；
- 太复杂后脆弱；
- 很难补充模型不存在的最新知识；
- 不能替代 Runtime。

---

## 3. RAG 适合什么

RAG 适合：

```text
Knowledge changes often
Private corpus
Need citation
Need permission
Need freshness
Large corpus
```

它改变的是：

> **模型当前看见的证据。**

而不是直接改变模型参数。

因此知识更新通常只需更新 Corpus / Index，不必重新训练模型。

---

## 4. Fine-tuning 适合什么

Fine-tuning 更像：

> **改变模型在某种输入分布下的行为倾向。**

典型目标：

- Domain style；
- 特定格式；
- 分类 / 抽取能力；
- 专用行为；
- Tool Use Pattern；
- 小模型蒸馏专用任务。

不适合拿来维护每周变化的知识库。

---

## 5. 一个常用决策树

```text
效果不好
  ↓
模型理解任务吗？
  ├─ 否 → Prompt / Examples
  ↓ 是
缺的是外部事实吗？
  ├─ 是 → RAG / Tool
  ↓ 否
是 Runtime / Permission / Reliability 吗？
  ├─ 是 → Backend / Agent Harness
  ↓ 否
是稳定重复的行为能力差距吗？
  ├─ 是 → Fine-tuning Candidate
  ↓
先建立 Eval 再决定
```

---

## 6. 为什么经常是组合，而不是三选一

一个真实系统可能同时使用：

```text
Fine-tuned Model
+
Prompt
+
RAG
+
Tools
```

例如客服系统：

- Fine-tuning：学习品牌语气和分类行为；
- Prompt：规定当前任务和输出格式；
- RAG：提供最新产品政策；
- Tool：查询实时订单。

它们解决不同层的问题。

---

## 7. Fine-tuning 前必须有 Baseline

训练前至少要知道：

```text
Base Model Score
Prompt-only Score
RAG Score
Failure Categories
Cost / Latency Baseline
```

否则训练后无法证明改进来自 Fine-tuning，也不知道是否值得训练成本。

---

## 8. 数据量不是唯一问题

Fine-tuning 数据要看：

- Label Quality；
- Coverage；
- Diversity；
- Hard Cases；
- Leakage；
- Production Distribution；
- Train / Eval Split。

100 万条低质量数据，不一定比 5000 条精心构造的任务数据更有价值。

---

## 9. 🎯 面试怎么回答

> 我会先做问题归因。Prompt 解决任务表达和输出约束，RAG / Tool 解决外部、私有和实时知识，Fine-tuning 更适合稳定重复的行为能力差距，而超时、权限、幂等属于 Runtime。Fine-tuning 前我会先建立 Base / Prompt / RAG Baseline 和 Evaluation Set，只有确认问题是模型行为能力而不是知识或系统问题，才值得投入训练。

---

## 10. ⚠️ 易错点

错误：

> 模型不知道公司最新政策，所以 Fine-tune 一遍。

知识持续变化时通常更适合 RAG。

错误：

> Fine-tuning 后就不需要 Prompt。

仍然需要描述当前任务和 Context。

错误：

> RAG 比 Fine-tuning 高级，所以所有问题都用 RAG。

它们解决不同问题。

---

<details>
<summary>自测：企业政策每周更新，为什么不优先 Fine-tune？</summary>

因为参数更新成本高、知识难快速撤回与引用；RAG 可以独立更新 Corpus / Index，并保留权限、版本和引用链，更适合持续变化的事实知识。

</details>
