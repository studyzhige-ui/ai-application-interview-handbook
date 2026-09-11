# 06｜Self-Attention 与 Q / K / V

## 1. 先讲人话

Self-Attention 可以先理解成：

> 当前 Token 在更新自己的表示时，要决定“前文哪些 Token 更值得关注”。

例如：

```text
The animal didn't cross the street because it was too tired.
```

模型处理 `it` 时，需要从前文判断它和 `animal` 的关系更强。

Attention 就是在做这种**动态关系加权**。

---

## 2. Q / K / V 是什么

每个 Token 的 hidden state 会经过不同线性变换，得到：

```text
Q = Query
K = Key
V = Value
```

直觉上：

- `Q`：我现在想找什么信息；
- `K`：我这里提供什么特征；
- `V`：如果你关注我，真正要拿走什么内容。

---

## 3. Scaled Dot-Product Attention

核心形式：

```text
Attention(Q, K, V)
= softmax(QK^T / sqrt(d_k)) V
```

拆开看：

### Step 1：Q 和 K 做相似度

```text
QK^T
```

得到当前位置对其它位置的相关性分数。

### Step 2：缩放

除以：

```text
sqrt(d_k)
```

避免维度增大后 Dot Product 数值过大，让 Softmax 过早饱和。

### Step 3：Softmax

把分数变成权重分布。

### Step 4：对 V 加权求和

最终得到结合上下文后的新表示。

---

## 4. 为什么 Q / K / V 不直接用同一个向量

因为“匹配”和“传递信息”是两个不同角色。

如果全都用原始 hidden state，没有独立投影，模型表达关系的自由度会更小。

Q/K 投影学习：

> 哪些特征适合判断关系？

V 投影学习：

> 关系建立后，哪些信息应该真正传过去？

---

## 5. Self-Attention 为什么叫 Self

因为 Q、K、V 都来自同一个输入序列。

如果 Query 来自一个序列，而 Key / Value 来自另一个序列，就属于 Cross-Attention 的典型形式。

Decoder-only LLM 主体通常依赖 Self-Attention；多模态模型中可能出现 Cross-Attention 或其它融合结构。

---

## 6. Attention Score ≠ 人类可解释因果

应用里不要过度把 Attention Weight 解释成：

> “模型就是因为这个 Token 才做出这个决定。”

Attention Weight 是模型内部计算的一部分，不等价于完整因果解释。

这点在做可解释性、Debug 或安全分析时很重要。

---

## 7. Attention 与序列长度

如果是标准 Dense Self-Attention，Token 两两之间要形成关系矩阵。

因此序列越长：

- Attention 计算越重；
- 中间状态更大；
- Prefill 成本上升。

这也是 Long Context 需要模型结构、Kernel、Serving 系统一起优化的原因。

---

## 8. 一个极简例子

假设当前位置 Q 对三个历史 Token 的打分是：

```text
[1.2, 0.1, 2.0]
```

Softmax 后可能得到类似：

```text
[0.28, 0.09, 0.63]
```

那么最终输出更多地吸收第三个 Token 对应的 V。

真正模型当然是高维矩阵、多头、多层，但直觉相同。

---

## 9. 🎯 面试怎么回答

> Self-Attention 让每个 Token 根据上下文动态聚合其它 Token 的信息。输入 hidden state 会投影成 Q、K、V，Q 与所有 K 做缩放点积得到相关性分数，经过 Softmax 形成权重，再对 V 做加权求和。Q/K 负责“匹配关系”，V 负责“传递内容”。这种机制使模型能直接建立远距离 Token 依赖。

---

## 10. ⚠️ 易错点

错误：

> Q、K、V 是三个不同 Token。

它们通常是同一个 Token hidden state 经过三组不同权重矩阵投影得到的表示。

错误：

> Attention Weight 就是模型推理的完整解释。

不是。

---

## 11. 🔍 继续追问

- 为什么要除 `sqrt(d_k)`？
- 为什么要 Multi-Head？
- Decoder-only 为什么需要 Causal Mask？
- KV Cache 为什么缓存 K/V 而不是 Q？
- MQA / GQA 为什么能减少 KV Cache？

---

<details>
<summary>自测：为什么 KV Cache 通常缓存 K 和 V，而 Q 不需要长期缓存？</summary>

Decode 新 Token 时，需要用当前 Token 的新 Q 去查询所有历史 Token 的 K/V；当前 Q 只服务本次位置，不会在未来被作为历史匹配库反复使用，而历史 K/V 会被后续每个新 Token 重复访问。

</details>
