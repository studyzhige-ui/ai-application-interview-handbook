# 08｜FFN、Residual 与 Normalization

> Attention 不是 Transformer 的全部。一个 Block 里还必须理解 FFN、Residual 和 Normalization，它们共同决定信息怎样被加工并稳定地穿过很多层。

## 1. FFN 是什么

Feed-Forward Network 通常对每个 Token 位置独立执行相同的非线性变换。

经典形式可以粗略写成：

```text
FFN(x) = W2 · activation(W1 · x + b1) + b2
```

很多现代 LLM 会使用不同激活与门控结构，例如 GELU、SwiGLU 等，但核心角色相同：

> Attention 负责“从别的位置拿信息”，FFN 负责“在当前位置进一步加工这些信息”。

---

## 2. 为什么 Attention 后还需要 FFN

如果只有 Attention，模型主要在做上下文加权组合。

FFN 提供更强的非线性变换能力，让每个位置的表示可以进一步重编码。

可以把一个 Block 简化成：

```text
Attention：和别人交流
FFN：自己再思考加工
```

这是直觉，不是严格数学定义，但很适合建立整体认知。

---

## 3. Residual Connection

Residual 的核心形式：

```text
output = x + F(x)
```

它允许原始信息直接跨过一个子层，同时叠加新变换。

作用包括：

- 帮助深层网络稳定训练；
- 改善梯度传播；
- 让每层学习“增量修改”而不是完全重写表示。

---

## 4. Normalization

Normalization 用于控制激活尺度并稳定网络。

Transformer 家族中常见 LayerNorm、RMSNorm 等。

应用工程师不需要推导其统计性质，但应知道：

> Norm 是深层 Transformer 稳定计算的重要组成，而不是可有可无的格式化步骤。

---

## 5. Pre-Norm 与 Post-Norm

不同架构会把 Norm 放在子层前或后。

概念上：

```text
Pre-Norm:
x → Norm → Attention → +x

Post-Norm:
x → Attention → +x → Norm
```

现代 LLM 常使用更适合深层训练稳定性的变体。

面试时如果没有问具体模型，不要武断说所有 Transformer 都只有一种顺序。

---

## 6. FFN 为什么常占大量参数

Attention 很显眼，但 FFN 层通常也包含巨大的矩阵参数。

这意味着模型规模、显存、计算量并不只来自 Attention。

当讨论：

```text
Model Size
Inference Cost
Quantization
MoE
```

时，FFN 参数都是重要组成。

---

## 7. MoE 与 FFN 的关系直觉

Mixture-of-Experts 模型常把普通 FFN 替换成多个 Expert，并通过 Router 让一个 Token 只激活部分 Expert。

直觉：

```text
Dense FFN
→ 每个 Token 都走同一套大 FFN

MoE
→ Router 选择少量 Expert
→ 总参数可很大
→ 每 Token 激活参数相对少
```

这能帮助理解为什么一些 MoE 模型“总参数很大，但每 Token 实际计算没有同比增长”。

这里只建立边界，不展开训练路由算法。

---

## 8. 🎯 面试怎么回答

> Transformer Block 不只有 Attention。Self-Attention 负责跨 Token 聚合上下文，FFN 对每个位置进行非线性特征变换；Residual Connection 让原表示和增量变换相加，帮助信息和梯度在深层网络传播；Normalization 控制激活尺度、提高训练稳定性。不同模型会在 Norm 顺序、激活函数和 FFN 结构上有差异。

---

## 9. ⚠️ 易错点

错误：

> FFN 是全序列之间再次做交互。

通常 FFN 是 position-wise，对每个 Token 位置独立应用相同网络。

错误：

> Transformer 的大部分能力全来自 Attention。

这是过度简化。

---

<details>
<summary>自测：Attention 和 FFN 哪个负责跨 Token 交互？</summary>

主要是 Attention。FFN 通常对每个位置独立做非线性变换。

</details>
