# 27｜Fine-tuning 与 SFT 基础

## 1. Fine-tuning 在做什么

预训练模型已经拥有通用语言和知识能力。

Fine-tuning 的目标通常不是“重新训练一个模型”，而是：

> 在已有模型基础上，用更贴近目标任务的数据继续优化，使模型在特定输入分布上形成更符合要求的行为。

常见形式：

```text
Base Model
  ↓
Task / Domain Dataset
  ↓
Fine-tuning
  ↓
Adapted Model
```

---

## 2. SFT 是什么

SFT = Supervised Fine-Tuning。

训练数据一般形如：

```text
Input / Instruction
→ Desired Response
```

模型继续做 next-token training，但目标数据从通用预训练语料变成高质量任务示例。

它很适合让模型学习：

- Instruction Following；
- Domain Style；
- 格式；
- 专用问答模式；
- Tool Call Pattern；
- 分类 / 抽取行为。

---

## 3. 数据质量比“条数”更重要

SFT 最大风险之一是低质量数据。

需要检查：

```text
Correctness
Consistency
Coverage
Diversity
Hard Cases
Duplicates
Leakage
Production Match
```

如果训练数据本身充满幻觉、格式错误或冲突，模型会把这些行为学进去。

---

## 4. Train / Validation / Test

不能把所有数据都用于训练。

至少应该拆：

```text
Train
→ 更新参数

Validation
→ 训练过程调参 / 选择 checkpoint

Test / Holdout
→ 最终评估
```

如果 Eval Case 泄漏进训练集，得到的分数没有真实泛化意义。

---

## 5. Full Fine-tuning

Full Fine-tuning 会更新大量甚至全部模型参数。

优点：

- 适配能力强；
- 可以充分改变模型行为。

代价：

- GPU / 显存 / 训练成本高；
- Checkpoint 大；
- 多任务版本维护昂贵；
- 更容易出现灾难性遗忘等风险。

应用团队通常不会一上来就 Full Fine-tune 大模型。

---

## 6. Fine-tuning 不是知识库同步工具

把公司 FAQ Fine-tune 进模型后：

- 如何删除错误知识？
- 如何按 Tenant 隔离？
- 如何引用来源？
- 明天政策更新怎么办？

这些都很麻烦。

因此：

> 动态事实知识优先 RAG / Tool；Fine-tuning 更适合稳定行为模式。

---

## 7. Evaluation 必须覆盖 Regression

Fine-tuning 后不仅要看目标任务有没有提升，还要看：

```text
General Capability
Safety
Instruction Following
Formatting
Tool Calling
Hallucination
Long Context
Old Success Cases
```

模型可能在专项任务变好，却在通用能力上退化。

---

## 8. Fine-tuning 的 Deployment 成本

训练完成后还要考虑：

- Model Artifact；
- Serving Engine Compatibility；
- Quantization；
- Adapter Loading；
- Rollback；
- Versioning；
- A/B Test；
- Observability。

所以“训练成功”离“Production 可用”还有很远。

---

## 9. Fine-tuning 项目怎么说才可信

面试中不要只说：

> “我们做了 LoRA，效果提升 20%。”

应该能回答：

```text
为什么 Fine-tune？
Baseline 是什么？
Dataset 从哪里来？
多少 Hard Case？
如何去重？
Train / Eval 怎么切？
指标是什么？
有没有 Regression？
部署成本如何？
```

---

## 10. 🎯 面试怎么回答

> Fine-tuning 是在预训练模型基础上继续用目标任务数据优化模型行为。SFT 用 Input → Desired Response 的监督样本继续做 next-token training，适合 Instruction、领域风格、格式和专用任务行为。应用工程上我更关注数据质量、Train/Eval 隔离、Baseline、Regression 和部署成本；动态知识通常优先 RAG，而不是反复 Fine-tune。

---

## 11. ⚠️ 易错点

错误：

> 数据越多 Fine-tuning 一定越好。

错误：

> Fine-tuning 就是把知识“存进模型”。

错误：

> 训练 Loss 降低就说明业务效果一定提升。

---

<details>
<summary>自测：Fine-tuning 前为什么必须建立 Prompt-only / RAG Baseline？</summary>

因为如果更便宜、更容易维护的 Prompt 或 RAG 已经达到目标，就没有必要承担训练和部署成本；同时 Baseline 也是证明 Fine-tuning 真实增益的参照。

</details>
