# 29｜RLHF / DPO / GRPO / Distillation 的应用工程边界

> 这一章不把你训练成 RLHF 算法工程师，而是让你知道：**SFT 之后，为什么还需要偏好优化；不同 Post-training 方法在解决什么问题；什么时候应用团队应该关心，什么时候不该自己做。**

## 1. 为什么 SFT 之后还不够

SFT 学的是：

```text
Input
→ Desired Response
```

但很多“好回答”很难用唯一标准答案描述。

例如：

- 哪个回答更有帮助？
- 哪个更安全？
- 哪个更符合风格？
- 哪个推理更简洁？
- 哪个代码 Patch 更容易通过测试？

这更像：

> **偏好比较。**

于是出现 Preference Optimization。

---

## 2. RLHF 的基本链路

RLHF = Reinforcement Learning from Human Feedback。

经典高层流程：

```text
SFT Model
→ Collect Human Preference
→ Train Reward Model
→ RL Optimization
→ Aligned Model
```

其中 RL 阶段常见 PPO 等算法。

应用岗需要理解的是：

- Human Preference 如何变成训练信号；
- Reward Model 只是偏好代理；
- 对齐可能改变模型行为；
- Reward Hacking / Distribution Shift 仍存在。

不要求推导 PPO 公式。

---

## 3. DPO

DPO = Direct Preference Optimization。

它尝试绕过显式 Reward Model + 在线 RL 的复杂流程，直接利用 Preference Pair：

```text
Prompt
Chosen Response
Rejected Response
```

优化模型更偏向 Chosen。

直觉上：

> 用成对偏好数据直接做策略偏好学习。

优势通常是训练流程更简单、工程复杂度更低。

---

## 4. GRPO 应该理解到什么程度

GRPO 属于近年来 Reasoning / Post-training 场景经常讨论的方法家族。

应用工程师重点知道：

- 它仍属于基于奖励信号的策略优化思路；
- 会比较一组采样结果形成相对优势；
- 常被用于可验证 Reasoning / Reward 场景；
- 训练稳定性、Reward Design、Sampling Cost 都是关键。

不要在不了解具体论文 / 实现时把它说成：

> “DPO 的升级版”。

它们优化方式和训练设定不同。

---

## 5. Reward 为什么危险

如果 Reward 定义不好，模型可能学会：

```text
最大化分数
≠
真正完成任务
```

例如：

- 利用 Judge 偏差；
- 输出特定格式骗分；
- 过度冗长；
- 找 Benchmark 漏洞。

这就是 Reward Hacking / Specification Gaming 的工程风险。

所以：

> Evaluation / Verification 必须独立于单一训练 Reward。

---

## 6. Knowledge Distillation

Distillation 的目标可以理解为：

```text
Strong Teacher
      ↓
生成 Target / Logit / Preference / Reasoning Data
      ↓
Smaller Student
```

让更小模型学习大模型行为。

应用价值：

- 降成本；
- 降延迟；
- 做领域小模型；
- 把昂贵 Teacher 能力迁移到高吞吐 Student。

---

## 7. Distillation 不是“复制全部能力”

Student 容量有限。

通常需要明确：

```text
要蒸馏什么任务？
数据覆盖哪些场景？
Teacher 输出是否可靠？
是否保留 Hard Case？
General Capability 会损失多少？
```

更像任务级能力压缩，而不是魔法式复制。

---

## 8. Synthetic Data

现代 Fine-tuning / Distillation 常使用强模型生成训练数据。

优点：

- 快速扩充；
- 能生成 Hard Case；
- 能统一格式。

风险：

- Teacher Hallucination；
- 风格单一；
- Error Amplification；
- 数据污染；
- 过拟合 Teacher Bias。

因此 Synthetic Data 也需要过滤和人工 / 规则验真。

---

## 9. 应用团队什么时候真的需要 Post-training

优先顺序通常是：

```text
Prompt / Structured Output
→ RAG / Tool
→ Model Selection
→ SFT / LoRA
→ Preference Optimization / Distillation
```

不是绝对规则，但对于多数 AI Application 团队，这是更合理的成本递进。

如果只是 100 个内部用户的知识问答，不应该一开始就搭 RLHF Pipeline。

---

## 10. 面试里怎样回答 PPO / DPO / GRPO

如果不是算法岗，不需要装作会完整推导。

更好的回答结构：

```text
它解决什么问题
→ 训练信号是什么
→ 是否需要 Reward Model
→ 工程复杂度
→ 典型风险
→ 应用场景
```

例如 DPO：

> DPO 用 chosen / rejected Preference Pair 直接优化模型偏好，不需要显式训练 Reward Model 再跑 PPO，因此训练链更简单。但它仍依赖高质量偏好数据，且离线 Preference 分布不一定覆盖 Production 行为。

---

## 11. 🎯 面试怎么回答

> SFT 主要学习示范答案，Preference Optimization 则解决“多个可行回答里哪个更符合人类偏好”的问题。RLHF 常通过 Human Preference → Reward Model → RL；DPO 直接利用 chosen / rejected Pair 优化偏好，流程更简单；GRPO 属于基于奖励的策略优化方法之一，应用时重点看 Reward 和采样成本。Distillation 则用强 Teacher 帮助小 Student 学特定能力，常用于降低延迟和成本。应用团队是否做这些方法，必须先证明 Prompt、RAG、Model Selection 和普通 SFT 已经不能满足需求。

---

## 12. ⚠️ 易错点

错误：

> RLHF = PPO。

PPO 只是 RLHF 中可能采用的一种策略优化算法。

错误：

> DPO 不需要偏好数据。

需要 chosen / rejected 等 Preference Signal。

错误：

> Distillation 后小模型等价于 Teacher。

不会自动保留全部能力。

错误：

> Reward 越高，Production 一定越好。

需要独立 Evaluation 防 Reward Hacking。

---

<details>
<summary>自测：SFT 和 DPO 最核心的训练信号差别是什么？</summary>

SFT 通常学习“给定输入应该生成什么目标答案”；DPO 学习“在两个回答之间更偏好哪一个”，因此更直接地利用 Preference Pair 调整行为偏好。

</details>
