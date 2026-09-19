# 04｜Attention 与 Position：QKV、Multi-Head、Causal Mask 与 RoPE

这一章回答 Transformer 里最常被问的一组问题：

```text
Q / K / V 是什么？
Attention 为什么能让 Token 看上下文？
为什么需要 Multi-Head？
生成模型为什么要 Causal Mask？
没有 RNN 后，顺序信息从哪里来？
RoPE 又解决什么？
```

这些概念本质上属于同一个“Token 怎样有条件地读取其它位置”的知识闭环。

---

## 1. Self-Attention 的核心问题

给定当前位置 Token 的表示，模型要决定：

> **我应该从其它可见 Token 中读取多少信息？**

Self-Attention 把同一组 Hidden State 映射成：

```text
Q = Query
K = Key
V = Value
```

可以先用数据库类比理解：

```text
Query  = 我正在找什么
Key    = 每个位置拿什么和 Query 匹配
Value  = 匹配后真正取回什么信息
```

这只是直觉类比，不是严格等价。

---

## 2. Attention Score 怎么形成

简化形式：

```text
score(i,j) = Qi · Kj / sqrt(dk)
```

然后经过 Softmax：

```text
weight(i,j) = softmax(score)
```

最后：

```text
output_i = Σ weight(i,j) * Vj
```

也就是当前位置 i 对其它位置 j 的 Value 做加权汇总。

---

## 3. 为什么要除以 sqrt(dk)

维度变大时 Dot Product 数值范围容易变大，Softmax 可能过度尖锐，梯度和数值稳定性变差。

Scaling：

```text
1 / sqrt(dk)
```

用于控制 Score 尺度。

应用工程面试通常理解这个原因即可，不需要完整统计推导。

---

## 4. Self-Attention 为什么比 RNN 更适合并行

RNN 通常有时间依赖：

```text
h1 → h2 → h3 → ...
```

Attention 在训练/Prefill 时可以一次计算序列中大量 Token 之间的关系，因此更适合矩阵并行计算。

但这不代表生成阶段也能一次生成所有 Token，因为 Autoregressive Decode 仍然是逐 Token 依赖。

---

## 5. Multi-Head Attention 为什么需要多个 Head

单个 Attention Head 只有一套投影空间。

Multi-Head 允许不同 Head 学习不同的关系模式：

```text
Head 1 → 某类局部关系
Head 2 → 某类长距离依赖
Head 3 → 某类实体/语法关联
...
```

不要把每个 Head 固定解释成人类可命名功能；更稳妥的说法是：

> 多头让模型在多个子空间并行建模不同关系，再合并结果。

---

## 6. Causal Mask 为什么生成模型必须有

训练 Decoder-only LLM 时，位置 i 不应该偷看未来 Token。

因此 Attention Matrix 会屏蔽：

```text
j > i
```

形成：

```text
Token 1: 看 1
Token 2: 看 1,2
Token 3: 看 1,2,3
...
```

这就是 Causal Mask。

没有它，训练时模型可能读取答案后面的 Token，推理时却没有这些信息，训练目标会失真。

---

## 7. Padding Mask 与 Causal Mask 不一样

### Padding Mask

屏蔽 Batch 中补齐长度的无效 Padding Position。

### Causal Mask

屏蔽未来位置。

它们解决两个不同问题，不能混为一谈。

---

## 8. Attention 为什么需要位置信息

纯 Attention 对 Token 集合本身并没有天然的序列顺序概念。

例如：

```text
A B C
C B A
```

如果没有任何 Position Signal，模型难以区分顺序关系。

因此需要 Positional Encoding。

---

## 9. Absolute Position 与 Relative Position 直觉

一种思路是给每个位置加入：

```text
position 0
position 1
position 2
```

的表示。

另一种思路更强调 Token 之间的相对位置关系。

现代大模型中 RoPE 是非常常见的一种机制。

---

## 10. RoPE 的核心直觉

RoPE = Rotary Positional Embedding。

它不是简单：

```text
Token Embedding + Position Vector
```

而是把位置编码融入 Q / K 的旋转变换，让 Attention Score 能表达相对位置关系。

从应用工程角度，需要理解：

```text
Position
→ influences Q/K geometry
→ influences Attention score
```

而不需要手推完整复数旋转公式。

---

## 11. RoPE 和 Long Context 的关系

模型训练时通常有一定位置分布和长度范围。

把 Context Window 扩得远超训练范围时，即使工程上能够分配更大的 KV Cache，也不代表模型对超长位置仍保持同等质量。

因此长上下文能力同时涉及：

- Position Encoding；
- Training / Fine-tuning Length；
- RoPE Scaling 等扩展技术；
- Attention Compute；
- KV Cache；
- 信息利用能力。

不能只看 API 的 `max_context_tokens`。

---

## 12. Attention 的计算成本直觉

朴素 Full Attention 对长度 `L` 的 Attention Matrix 规模近似：

```text
L × L
```

所以序列变长时，Prefill Attention 的计算和内存压力会显著增加。

现代系统会通过：

- FlashAttention；
- GQA / MQA；
- Sliding Window；
- Sparse / Local Attention；
- Kernel Optimization；

等方式优化。

这些不是本模块必须全部深入的算法，但需要知道：

> Context Length 会真实影响推理资源，而不是一个免费的配置值。

---

## 13. QKV 和 KV Cache 的关系

Autoregressive 生成时，历史 Token 的 K / V 在后续 Decode 中会反复使用。

因此可以缓存历史 K/V：

```text
KV Cache
```

避免每生成一个新 Token 都重新计算历史所有位置的 K/V。

所以理解 QKV 是理解 KV Cache 的直接前置。

---

## 14. 常见错误

- Q/K/V 是三个不同 Token：错，是同一 Hidden State 经过不同投影。
- Attention 就是相似度搜索：有类似直觉，但包含 Learnable Projection、Softmax、Value Aggregation 等，不等同 Vector DB。
- Multi-Head 每个 Head 都有固定人类语义：过度解读。
- Causal Mask 是为了忽略 Padding：错。
- RoPE 只是给 Token 加位置编号：不准确。
- Context Window 大小只由 RoPE 决定：错误。

---

## 15. 面试怎么答

### Q：Q、K、V 怎么理解？

> Self-Attention 会把每个位置的 Hidden State 投影成 Query、Key、Value。Query 与其它位置的 Key 计算相关度，经 Softmax 得到权重，再对对应 Value 加权聚合，从而让当前位置吸收其它可见 Token 的信息。

### Q：为什么需要 Causal Mask？

> Autoregressive 模型训练时当前位置只能使用自己和过去 Token，不能看到未来答案，因此通过 Causal Mask 屏蔽未来位置，使训练时的信息边界与真实生成一致。

### Q：RoPE 在做什么？

> RoPE 把 Position 信息编码进 Q/K 的旋转变换，使 Attention Score 能感知相对位置关系。它是现代 LLM 位置建模的常见方案，也和 Long Context 扩展能力有关，但 Context 上限不只由 RoPE 决定。

---

## 16. 自测

<details><summary>1. Q/K/V 为什么来自同一个输入却要三套投影？</summary>
因为“当前要找什么”“拿什么匹配”“最终取回什么信息”是三个不同角色，Learnable Projection 让模型学习不同空间。
</details>

<details><summary>2. Multi-Head 的主要价值是什么？</summary>
让模型在多个子空间并行建模不同关系，再合并结果，提高表达能力。
</details>

<details><summary>3. 为什么理解 QKV 后自然会引出 KV Cache？</summary>
Decode 时历史 Token 的 K/V 会被后续每个新 Token 重复读取，因此缓存它们可以避免重复计算。
</details>
