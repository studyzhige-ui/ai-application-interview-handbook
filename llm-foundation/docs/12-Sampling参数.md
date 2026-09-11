# 12｜Temperature / Top-k / Top-p 与 Determinism

## 1. 先讲人话

模型已经产生下一 Token 的概率分布后，Sampling 参数决定：

> 我们到底从这个分布里多“保守”还是多“发散”地选 Token。

最常见的三个概念：

```text
Temperature
Top-k
Top-p
```

---

## 2. Temperature

Temperature 会调整 logits 的相对尖锐程度。

直觉：

```text
低 Temperature
→ 高概率 Token 更占优势
→ 输出更稳定 / 保守

高 Temperature
→ 分布更平
→ 更多候选有机会被采样
→ 输出更发散
```

典型形式：

```text
softmax(logits / T)
```

当 `T` 越小，分布越尖锐。

---

## 3. Top-k

只保留概率最高的 k 个候选，再从中采样。

例如：

```text
整个词表 100k
Top-k = 40
→ 只在前 40 个候选里采样
```

它控制候选集合大小。

---

## 4. Top-p / Nucleus Sampling

不是固定保留 k 个，而是选择最小的一组高概率 Token，使累计概率达到 p。

例如：

```text
p = 0.9
```

高确定性位置可能只需几个 Token 就覆盖 0.9；不确定位置可能需要几十个。

因此 Top-p 会根据分布动态调整候选集合。

---

## 5. 这些参数怎样组合

Provider 和模型实现可能不同，常见逻辑是先调整 logits，再裁剪候选，再抽样。

应用工程上不要死背一个固定执行顺序，应该看具体 API 文档。

更重要的是理解：

```text
Temperature → 改分布形状
Top-k       → 固定候选数量
Top-p       → 按累计概率裁候选
```

---

## 6. 为什么 Temperature=0 仍不等于数学意义上的绝对确定

很多 API 会把 Temperature=0 解释成非常接近 greedy 的确定性生成。

但端到端系统仍可能存在：

- 底层并行计算非完全确定；
- 模型版本更新；
- Provider 路由到不同后端；
- 动态系统指令；
- Tool / Retrieval 结果变化；
- Sampling 实现差异。

所以工程上更准确的表述是：

> 低随机 Sampling 能提高可重复性，但不能把一个分布式 LLM Service 当成严格纯函数。

---

## 7. 不同任务怎样选

### Structured Extraction / Classification

通常更偏稳定：

```text
低 Temperature
+ Structured Output
+ Schema Validation
```

### Coding

通常也偏稳定，但有时需要探索多个候选。

### Brainstorm / Creative Writing

可以提高随机性和候选多样性。

### RAG Factual QA

更重要的是 Grounding / Evidence / Verification，不应该靠“Temperature 调低”解决事实错误。

---

## 8. Sampling 不是模型能力开关

如果模型不知道某个事实：

```text
Temperature = 0
```

不会凭空让它知道。

如果 Prompt 有歧义：

```text
Top-p = 0.1
```

也不会自动消除歧义。

所以 Sampling 参数主要调**输出分布行为**，不是替代 Prompt / RAG / Model Selection。

---

## 9. 🎯 面试怎么回答

> Temperature 控制概率分布尖锐程度，低值让高概率 Token 更占优势；Top-k 只保留概率最高的 k 个候选；Top-p 则保留累计概率达到阈值的一组候选。它们本质上都在控制 Decoding 的随机性和候选范围。对于结构化抽取、代码或事实 QA 通常更偏稳定，但事实正确性仍要靠 Context、RAG 和 Verification，而不是单靠把 Temperature 调低。

---

## 10. ⚠️ 易错点

错误：

> Temperature 越低，答案越正确。

它主要影响随机性，不直接提高事实知识。

错误：

> Temperature=0 就保证全链路 bit-for-bit 一致。

工程系统通常不能这样承诺。

---

<details>
<summary>自测：Top-k 和 Top-p 的核心区别是什么？</summary>

Top-k 固定保留 k 个高概率候选；Top-p 根据累计概率动态决定候选集合大小。

</details>
