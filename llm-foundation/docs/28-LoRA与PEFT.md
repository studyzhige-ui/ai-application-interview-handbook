# 28｜LoRA / PEFT：低成本参数适配

## 1. 为什么需要 PEFT

大模型参数很多，如果每个业务都 Full Fine-tune：

```text
Task A → 一整份模型
Task B → 又一整份模型
Task C → 再一整份模型
```

训练、存储和 Serving 成本都很高。

PEFT = Parameter-Efficient Fine-Tuning，目标是：

> **只训练很小一部分新增或选定参数，就让模型适配新任务。**

LoRA 是最常见方法之一。

---

## 2. LoRA 的核心直觉

原始线性层：

```text
y = Wx
```

LoRA 不直接完整更新大矩阵 W，而是假设任务所需参数变化可以用低秩矩阵表示：

```text
W' = W + ΔW
ΔW = B A
```

其中：

```text
A: r × d
B: d × r
r << d
```

训练时冻结原始 W，只更新 A/B。

这样训练参数量显著减少。

---

## 3. 为什么叫 Low-Rank

如果完整更新矩阵是：

```text
d × d
```

LoRA 用：

```text
d × r
+
r × d
```

近似表达更新，其中 r 很小。

所以需要训练和保存的参数大幅减少。

---

## 4. LoRA 通常插在哪里

常见位置包括 Attention 的线性投影：

```text
Q
K
V
O
```

也可能放 FFN 等模块。

具体 Target Module 要结合模型和任务，不要背成：

> “LoRA 永远只训练 Q/V。”

不同框架默认值可能不同。

---

## 5. Rank r 的 Trade-off

`r` 越大：

- 适配容量更高；
- 可训练参数更多；
- 显存 / 存储 / 计算增加。

`r` 太小：

- 可能表达能力不足。

所以不能说：

> Rank 越大越好。

需要通过 Eval 选择。

---

## 6. LoRA 的优势

### Training

- 可训练参数少；
- Optimizer State 少；
- 显存更低；
- 训练更快。

### Artifact

Adapter 文件远小于完整模型副本。

### Multi-task

可以：

```text
Base Model
├─ Adapter A
├─ Adapter B
└─ Adapter C
```

按任务加载。

---

## 7. LoRA 不是免费午餐

仍然可能出现：

- 数据质量问题；
- Overfitting；
- Base Capability Regression；
- Adapter Compatibility；
- Serving 复杂度；
- 多 Adapter 调度成本；
- Quantization Compatibility。

而且如果任务和 Base Model 差距很大，小 LoRA 未必足够。

---

## 8. QLoRA 的直觉

QLoRA 的核心组合是：

```text
Quantized Base Model
+
LoRA Adapter Training
```

这样可以进一步降低训练显存。

要注意：

> Base Weight 的低精度存储和 Adapter 的训练精度是不同层次，不能简单说“所有东西都是 4 bit 训练”。

---

## 9. Merge vs Runtime Adapter

部署时常见两种思路。

### Merge

把 LoRA 更新合并进 Base Weight。

优点：

- 推理路径简单。

缺点：

- 每个任务可能又生成完整权重版本。

### Runtime Adapter

Base Model 不变，运行时加载 Adapter。

优点：

- 多任务复用 Base；
- Artifact 小。

缺点：

- Serving Engine 要支持 Adapter 管理；
- 多租户调度更复杂。

---

## 10. PEFT 不只有 LoRA

还存在：

- Adapter；
- Prefix Tuning；
- Prompt Tuning；
- IA3；
- 其它低秩 / 选择性参数更新方法。

应用岗重点是理解：

> PEFT 是一类“减少可训练参数”的适配策略，不要把 LoRA 当作 Fine-tuning 的同义词。

---

## 11. 🎯 面试怎么回答

> LoRA 属于 PEFT。它冻结 Base Model 的原始权重，把目标权重变化近似成两个低秩矩阵 BA，只训练这部分新增参数，因此训练显存、Optimizer State 和 Adapter Artifact 都明显更小。Rank 决定适配容量与成本，需要用真实 Eval 选择。部署时可以 Merge，也可以运行时加载 Adapter；LoRA 只是低成本适配手段，仍然不能绕过数据质量、Regression 和 Serving 管理。

---

## 12. ⚠️ 易错点

错误：

> LoRA = Fine-tuning。

LoRA 是 Fine-tuning 的一种参数高效实现。

错误：

> Rank 越高一定越好。

错误：

> QLoRA 就是全模型用 INT4 做普通梯度更新。

---

<details>
<summary>自测：LoRA 为什么能显著减少训练参数？</summary>

因为不更新完整大矩阵 W，而只学习低秩增量 ΔW = BA，其中 rank r 远小于原矩阵维度，因此可训练参数从 O(d²) 降为近似 O(dr)。

</details>
