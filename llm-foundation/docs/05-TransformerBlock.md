# 05. Transformer Block：Architecture、FFN、Residual 与 Normalization

这一章先建立一个完整 Transformer Block，再把 Attention 的细节留给下一章。

应用工程师不需要从头推导全部训练数学，但必须能回答：

```text
一个 Token 表示进入模型后经历什么？
Attention 和 FFN 各负责什么？
为什么要 Residual？
Normalization 在稳定什么？
为什么重复很多层后模型能形成复杂表示？
```

---

## 1. Decoder-only LLM 的整体路径

简化来看：

```text
Token IDs
→ Token Embedding
→ Position Information
→ Transformer Block × N
→ Final Norm
→ LM Head
→ Logits
→ Next Token
```

现代生成式 LLM 常采用 Decoder-only Transformer，但具体实现会在 Norm、Activation、Attention、Position Encoding 等细节上不同。

课程关心稳定的结构思想，而不是把某一个模型实现当作所有 LLM 的定律。

---

## 2. 一个 Transformer Block 大致有什么

简化成：

```text
Input Hidden State
      │
      ├─ Norm
      ↓
Self-Attention
      ↓
+ Residual
      │
      ├─ Norm
      ↓
FFN / MLP
      ↓
+ Residual
      ↓
Output Hidden State
```

Attention 负责 Token 之间的信息交互；FFN 负责对每个位置的表示做非线性变换。

---

## 3. Hidden State 是什么

每个 Token 在每一层都有一个向量表示：

```text
h_i^(layer)
```

它不是固定不变的“Token Embedding”。

经过每层：

```text
Attention
+
FFN
```

Token 表示会不断吸收上下文信息。

所以同一个词在不同句子里的最终表示可以不同。

---

## 4. Attention 负责什么

Attention 的核心作用是：

> **让当前位置根据其它可见位置的信息更新自己的表示。**

例如：

```text
“The animal didn't cross the street because it was tired.”
```

模型需要把 `it` 和前面合适的实体建立联系。

具体 Q/K/V、Multi-Head 和 Causal Mask 下一章展开。

---

## 5. FFN / MLP 负责什么

Attention 混合的是不同 Token 位置的信息。

FFN 通常对每个 Token 位置独立执行同一组非线性变换：

```text
h
→ linear up projection
→ activation / gating
→ linear down projection
```

可以把它理解为：

> Attention 决定“从哪里取信息”，FFN 进一步“加工这个位置已经拥有的信息”。

现代模型常使用不同的门控 MLP 变体，具体形式随架构不同。

---

## 6. 为什么 FFN 参数很多

Transformer 中 FFN 中间维度通常比 Hidden Size 大。

这使得每层拥有较强的非线性表示能力。

因此模型参数量并不只来自 Attention；MLP/FFN 往往也是很大的一部分。

---

## 7. Residual Connection 为什么重要

典型结构不是：

```text
h = attention(h)
h = ffn(h)
```

而更像：

```text
h = h + attention(...)
h = h + ffn(...)
```

Residual 让每个子层学习：

> **在已有表示基础上增加什么变化。**

它有助于：

- 信息直接跨层传播；
- 深层网络优化；
- 梯度传播；
- 减少“每层都必须完全重建表示”的负担。

---

## 8. Normalization 做什么

LayerNorm / RMSNorm 等 Norm 机制用于控制激活尺度，帮助深层网络稳定训练和推理。

应用工程深度需要知道：

```text
Norm
≠ 把 Token 语义归一化成同一个东西
```

它是网络内部数值稳定机制。

不同模型可能使用：

- LayerNorm；
- RMSNorm；
- Pre-Norm；
- Post-Norm。

不要把某一种实现绝对化。

---

## 9. Pre-Norm 与 Post-Norm 的直觉

### Post-Norm 风格

```text
h → sublayer → add residual → norm
```

### Pre-Norm 风格

```text
h → norm → sublayer → add residual
```

现代大模型中 Pre-Norm / RMSNorm 很常见，因为深层训练稳定性较好，但课程不要求死记具体模型选择。

真正要理解：

> Norm 的位置会影响数值与优化行为，但不改变“Attention + FFN + Residual”这个主干。

---

## 10. 为什么要堆很多层

单层只能进行有限次数的信息交互和变换。

堆叠：

```text
Block 1
→ Block 2
→ ...
→ Block N
```

让 Token 表示逐层抽象。

可以粗略理解为：

```text
局部模式
→ 上下文组合
→ 更复杂语义 / 任务表示
```

但不要把“某一层一定负责某种具体能力”说得过度确定。

---

## 11. Parameter Count 和 Compute 的直觉

模型更大通常意味着：

```text
更多 Layers
更大 Hidden Size
更大 FFN
更多 Attention Heads
```

这会增加：

- Weight Memory；
- Matrix Multiplication；
- KV Cache（受层数/头配置等影响）；
- Serving Cost。

所以 Model Size 最终会体现在应用工程的 Latency / Throughput / Cost 上。

---

## 12. 常见错误

- Transformer 就是 Attention：错误，还有 FFN、Residual、Norm、Position 等。
- FFN 会直接让不同 Token 互相通信：主要跨 Token 交互由 Attention 完成。
- Residual 只是为了防止模型忘记输入：过度简化，它也是深层网络优化与信息流的重要机制。
- 所有模型都用完全相同 Transformer Block：错误。
- 应用工程师完全不需要懂 Transformer：如果不懂，很难解释 Context、KV Cache、Serving 和长上下文成本。

---

## 13. 面试怎么答

### Q：Transformer Block 里主要有什么？

> 一个现代 Decoder Block 可以抽象成 Attention 子层和 FFN/MLP 子层，并通过 Residual Connection 和 Normalization 连接。Attention 负责不同 Token 之间的信息交互，FFN 对每个位置的表示做非线性加工，Residual 和 Norm 帮助深层网络保持稳定的信息与梯度流。

### Q：Attention 和 FFN 的角色有什么区别？

> Attention 更像“从其它 Token 聚合哪些上下文”，FFN 更像“对当前位置聚合后的表示进一步加工”。两者重复多层后形成复杂上下文表示。

---

## 14. 自测

<details><summary>1. 为什么只讲 Attention 不能完整描述 Transformer？</summary>
因为每层通常还包含 FFN/MLP、Residual、Normalization 和位置机制，这些共同决定模型的表达和稳定性。
</details>

<details><summary>2. Residual Connection 的核心价值是什么？</summary>
让信息和梯度可以跨层直接流动，每个子层只需学习对已有表示的增量变换，帮助训练深网络。
</details>

<details><summary>3. Attention 和 FFN 哪一个主要负责跨 Token 信息交换？</summary>
Attention。
</details>
