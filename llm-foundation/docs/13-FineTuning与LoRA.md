# 27. Fine-tuning、SFT 与 LoRA / PEFT：什么时候值得训练自己的适配层

Fine-tuning 很容易被理解成：

> “Prompt 不好用，就训练一下模型。”

这是危险的。

真正应该建立的闭环是：

```text
为什么需要 Fine-tuning？
→ SFT 学什么？
→ Full Fine-tuning 成本为什么高？
→ LoRA / PEFT 为什么能降低成本？
→ 数据如何决定上限？
→ 怎样验证没有过拟合和能力退化？
→ 什么时候 RAG / Prompt 更合适？
```

---

## 1. Fine-tuning 改变的是什么

Prompt / RAG 主要改变：

```text
Inference-time Input / Context
```

Fine-tuning 改变：

```text
Model Parameters / Adapter Parameters
```

因此它更适合反复出现、希望模型“内化”的行为模式，例如：

- 特定任务格式；
- 领域语言习惯；
- 稳定分类/抽取能力；
- 某种交互风格；
- Tool/Protocol 行为；
- 小模型在特定任务上的能力适配。

---

## 2. SFT 是什么

SFT = Supervised Fine-Tuning。

训练数据常表示为：

```text
Input / Instruction
→ Desired Output
```

模型通过监督学习让给定输入下的输出分布更接近示范答案。

例如：

```text
customer message
→ support category JSON
```

或：

```text
medical note
→ structured extraction
```

---

## 3. 数据质量为什么比“多跑几个 Epoch”重要

Fine-tuning 的上限很大程度来自训练数据。

需要关注：

```text
Correctness
Coverage
Diversity
Consistency
Label Quality
Hard Cases
Negative Examples
Data Leakage
Train/Test Separation
```

如果示范本身互相矛盾：

```text
same input pattern
→ different desired behavior
```

模型会学到混乱边界。

所以：

> **Fine-tuning 首先是 Dataset Engineering 问题。**

---

## 4. 为什么必须有独立 Eval Set

不能：

```text
在训练集上表现很好
→ 宣布 Fine-tuning 成功
```

要留：

```text
Train
Validation
Test / Holdout
```

并覆盖：

- 常见案例；
- Hard Cases；
- Out-of-distribution；
- 原模型重要通用能力；
- Safety / Refusal；
- 格式与协议。

否则可能只是记住训练样本。

---

## 5. Full Fine-tuning 为什么贵

全参数训练意味着大量 Model Weight 都参与更新。

代价包括：

- GPU Memory；
- Optimizer State；
- Gradient；
- Training Compute；
- Checkpoint Storage；
- Deployment / Serving Version 管理。

大模型上这个成本非常高。

这正是 PEFT 出现的背景。

---

## 6. PEFT 是什么

PEFT = Parameter-Efficient Fine-Tuning。

核心目标：

> **只训练很少一部分新增或选择性参数，让大部分 Base Model 保持冻结。**

这样减少：

- Trainable Parameters；
- Optimizer Memory；
- Checkpoint Size；
- 多任务适配成本。

LoRA 是最典型方案之一。

---

## 7. LoRA 的核心直觉

原来某层权重：

```text
W
```

LoRA 不直接全量更新 W，而学习一个低秩增量：

```text
W' = W + ΔW
ΔW = B A
```

其中 Rank `r` 远小于原矩阵维度。

于是训练参数从完整大矩阵降低到两个较小矩阵。

直觉上：

> **很多任务适配不需要在所有方向上自由修改巨大权重，只需学习一个低秩更新空间。**

---

## 8. Rank r 控制什么

更高 Rank：

```text
Adapter Capacity ↑
Trainable Parameters ↑
Memory / Compute ↑
```

更低 Rank：

```text
更便宜
但可能表达能力不足
```

不能认为：

```text
r 越大越好
```

需要用 Eval 找到任务合适点。

---

## 9. LoRA 通常插在哪里

常见目标模块可能包括：

```text
Q / K / V / O Projection
FFN Projection
```

但具体选哪些层、哪些投影取决于模型架构与训练工具。

应用工程面试不必背某个框架的参数名，应该理解：

> Adapter 插入位置决定“允许模型在哪些子空间发生可训练变化”。

---

## 10. LoRA 与 Quantization 可以结合

例如 QLoRA 思路：

```text
Base Model Quantized
+
LoRA Adapter Trainable
```

降低 Base Weight 内存，让较小 GPU 也能完成适配。

但要区分：

```text
Quantization → 表示/存储/计算精度优化
LoRA → 参数高效训练方法
```

不是同一技术。

---

## 11. Fine-tuning 不适合解决动态知识

如果问题是：

```text
公司最新文档
每天变化的价格
实时库存
用户私有数据
```

Fine-tuning 很快会过期，而且无法灵活按权限删除/更新。

这类问题优先：

```text
RAG / DB / Tool
```

Fine-tuning 更适合：

```text
How to behave
```

而不是：

```text
What are today's facts
```

---

## 12. Catastrophic Forgetting / Capability Regression

训练到特定领域后，模型可能：

- 过度偏向训练格式；
- 通用能力下降；
- Safety 行为变化；
- 对未见输入过拟合；
- 输出多样性下降。

所以 Eval 不只测目标任务，还要测：

```text
重要通用 Regression Set
```

---

## 13. 什么时候 Fine-tuning 才值得做

建议先满足：

```text
1. 已有稳定 Base Model
2. Prompt / RAG / Tool 不能经济解决
3. Failure Pattern 可重复
4. 有足够高质量训练数据
5. 有独立 Eval
6. 能承担训练与部署版本治理
```

否则先做更轻的干预。

---

## 14. Fine-tuning 的 Production Versioning

需要记录：

```text
base_model_version
training_dataset_version
adapter_version
training_config
code_version
eval_version
```

上线要支持：

```text
A/B
Canary
Rollback
```

而不是“训练完覆盖旧模型”。

---

## 15. Serving LoRA 的工程价值

如果多个 Tenant / Task 共用一个 Base Model，可以：

```text
Base Model
├── Adapter A
├── Adapter B
└── Adapter C
```

比部署多个完整模型副本更节省存储和显存。

但 Runtime 还要解决：

- Adapter Loading；
- Cache；
- Routing；
- Version；
- Tenant Isolation；
- Batch Compatibility。

---

## 16. 常见错误

- Fine-tuning 就是把知识库背进模型：不适合作为动态事实存储。
- 数据越多越好：脏数据和冲突数据会伤害模型。
- Training Loss 下降就代表上线变好：必须看独立 Eval。
- LoRA 完全等价于 Full Fine-tuning：能力/灵活性和成本不同。
- Rank 越大越好：错误。
- Fine-tuning 后不需要 Regression：非常危险。

---

## 17. 面试怎么答

### Q：什么时候会考虑 Fine-tuning？

> 当 Prompt/RAG/Tool 已经不能经济稳定地解决一个重复行为或特定任务能力缺口，并且我有足够高质量标注数据和独立 Eval 时才会考虑。动态知识通常优先 RAG；Fine-tuning 更适合行为、格式、领域任务适配。上线还需要版本、Canary 和通用能力 Regression。

### Q：LoRA 为什么省资源？

> LoRA 冻结 Base Weight，只学习低秩更新矩阵 `ΔW=BA`，训练参数量和 Optimizer State 大幅减少，因此更适合大模型低成本任务适配；Rank 和插入层决定容量与成本，需要通过 Eval 选择。

---

## 18. 自测

<details><summary>1. 为什么 Fine-tuning Dataset 必须有版本？</summary>
模型行为与训练数据强相关，版本化才能复现、比较和回滚某次适配结果。
</details>

<details><summary>2. LoRA 和 Quantization 分别解决什么？</summary>
LoRA 解决参数高效训练；Quantization 主要降低权重/激活/KV 等表示精度和资源成本。
</details>

<details><summary>3. 为什么目标任务变好后仍要测通用 Regression？</summary>
Fine-tuning 可能导致过拟合、遗忘或 Safety/格式行为改变，需要确认没有破坏重要原能力。
</details>
