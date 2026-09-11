# 07｜Multi-Head Attention 与 Causal Mask

## 1. 为什么一个 Attention Head 不够

单个 Head 只能在一个投影空间里建立 Token 关系。

Multi-Head Attention 的直觉是：

> 让模型同时用多组不同的 Q/K/V 投影，从多个“观察角度”建模关系。

可以想象不同 Head 分别更擅长捕捉：

- 局部语法关系；
- 指代关系；
- 长距离依赖；
- 结构边界；
- 某类模式。

这不是说每个 Head 都能被清晰解释成一个固定人类概念，而是表示空间被拆成多个并行子空间。

---

## 2. Multi-Head 的基本流程

对于每个 Head：

```text
X
→ Q_i, K_i, V_i
→ Attention_i
```

多个 Head 的结果再：

```text
Concat(head_1, head_2, ...)
→ Output Projection
```

因此模型可以在同一层同时建模多种关系。

---

## 3. 为什么 Decoder-only LLM 需要 Causal Mask

训练 Next-token Prediction 时，第 i 个位置不能偷看未来答案。

例如：

```text
我 喜欢 学 习
```

预测“学”时，不能提前看见后面的“习”。

所以 Attention Matrix 要屏蔽未来位置：

```text
       K1 K2 K3 K4
Q1     ✓  ×  ×  ×
Q2     ✓  ✓  ×  ×
Q3     ✓  ✓  ✓  ×
Q4     ✓  ✓  ✓  ✓
```

这就是 Causal / Autoregressive Mask 的核心直觉。

---

## 4. Mask 怎样进入 Attention

通常会在 Softmax 前，对不允许访问的位置加入一个非常大的负值，使 Softmax 后权重接近 0。

概念上：

```text
score = QK^T / sqrt(d_k)
score = score + mask
weight = softmax(score)
```

因此未来 Token 不会参与当前位置的信息聚合。

---

## 5. Causal Mask 与 Padding Mask 不一样

### Causal Mask

解决：

> 不能看未来。

### Padding / Attention Mask

解决：

> Batch 中补齐出来的无效位置不应该参与计算。

两者目的不同，可能同时存在。

---

## 6. Multi-Head、MQA、GQA 的关系

标准 Multi-Head Attention 中，不同 Head 可以拥有独立 Q/K/V。

Serving 时 KV Cache 很大，于是出现优化思路：

```text
MHA：多个 Q Head + 多个 K/V Head
MQA：多个 Q Head + 共享更少 K/V
GQA：多个 Q Head 分组共享 K/V
```

应用工程师不需要掌握每个模型的具体配置，但要知道：

> GQA / MQA 的重要工程动机之一，是减少 KV Cache 和内存带宽压力，从而改善推理效率。

---

## 7. 为什么 Multi-Head 不是“Head 越多越好”

Head 数量与：

- Hidden Dimension；
- Head Dimension；
- 模型规模；
- 训练设计；
- Serving 成本；

一起决定模型结构。

不能脱离模型整体说：

> 32 Head 一定比 16 Head 强。

---

## 8. 🎯 面试怎么回答

> Multi-Head Attention 使用多组独立投影，让模型能在多个表示子空间中同时建模 Token 关系。Decoder-only LLM 还需要 Causal Mask，保证位置 i 只能关注自己和过去 Token，不能在训练时提前看到未来答案，从而与自回归 next-token prediction 一致。Serving 中的 MQA / GQA 则通过减少 K/V Head 数量降低 KV Cache 和带宽压力。

---

## 9. ⚠️ 易错点

错误：

> 每个 Attention Head 都能稳定对应一个明确语言学功能。

不能做这种过度解释。

错误：

> Causal Mask 是为了屏蔽 Padding。

这是两个不同 Mask。

---

<details>
<summary>自测：为什么训练时已经有完整句子，仍要 Causal Mask？</summary>

因为训练目标是模拟“根据过去预测下一个 Token”。如果当前位置能看到未来 Token，就会泄露标签信息，训练目标和真实生成过程不一致。

</details>
