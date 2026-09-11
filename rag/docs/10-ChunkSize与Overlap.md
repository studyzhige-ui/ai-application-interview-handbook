# 10｜Chunk Size / Overlap 怎样实验

## 1. 先讲人话

Chunk Size 和 Overlap 经常被当成“经验参数”，例如直接写 512 / 128。真正的工程问题不是记住某组数字，而是理解：

> **这两个参数分别改变了什么，以及怎样证明当前取值适合自己的 Corpus 和 Query。**

---

## 2. Chunk Size 在改变什么

Chunk 越大：

- 语义上下文更完整；
- 单个命中携带更多信息；
- 但局部语义可能被稀释；
- Context Noise 增加；
- 一个 Chunk 占用更多 Token。

Chunk 越小：

- Retrieval Unit 更精细；
- 更容易匹配局部问题；
- 但逻辑可能被切断；
- Chunk 数量和索引规模增加。

因此核心 Trade-off 是：

```text
Semantic Completeness
        ↕
Retrieval Specificity
```

---

## 3. Overlap 在解决什么

Overlap 的目的主要是降低边界损失。

例如：

```text
Chunk A: ...退款条件必须满足 X、Y
Chunk B: Y，并且必须在 30 天内...
```

没有 Overlap 时，条件可能被拆开。

但 Overlap 过大又会：

- 重复 Embedding；
- 重复命中；
- Context 冗余；
- 索引放大。

所以 Overlap 是“边界保险”，不是越大越好。

---

## 4. 字符、Token 还是结构？

应用工程中更推荐按 Token 或结构理解预算。

因为最终 LLM Context 是 Token 预算；但在很多文档中，结构边界比纯 Token 长度更重要。

因此常见做法不是：

```text
每 500 token 强制切
```

而是：

```text
先按结构切
→ 超长 section 再按 token 递归拆
```

---

## 5. 怎样做参数实验

准备真实 Query Dataset，然后固定其它变量：

```text
Strategy A: 256 / overlap 32
Strategy B: 512 / overlap 64
Strategy C: 800 / overlap 80
```

至少观察：

- Recall@K；
- Hit Rate；
- Context Token 数；
- Duplicate Candidate Rate；
- End-to-end Correctness / Faithfulness；
- Latency / Cost。

不要一次同时换 Embedding、Chunk、Rerank 和 Prompt，否则无法知道收益来自哪里。

---

## 6. 不同 Corpus 的直觉

- FAQ：天然 Question/Answer 单元，Size 不是主要参数；
- 法律条款：优先结构完整性；
- API 文档：优先 Heading + Code Block；
- 长叙述文本：可以实验 Recursive + Token Limit；
- 表格：不能简单按 Token 切行。

---

## 7. Failure Case

### Overlap 太小

答案跨边界，Top-K 里每块都只有半句话。

### Overlap 太大

Top-5 全是同一段的相邻重复块，Coverage 降低。

### Chunk 太大

Embedding 召回到“整章”，但 Query 需要其中一句，Reranker 也难区分。

---

## 8. 🎯 面试怎么回答

> Chunk Size 决定检索粒度与上下文完整性的平衡；Overlap 用于缓解边界切断，但会增加重复索引和 Context 冗余。参数不应该照抄默认值，而应在真实 Query / Ground Truth 上固定其它变量做实验，比较 Recall、Hit Rate、Context Token、重复率以及最终 Answer Quality。对结构化文档，通常先尊重章节或条款边界，再对超长部分做 Token 级递归拆分。

## 9. ⚠️ 易错点

- 直接说“512 最好”；
- 只看 Retrieval Recall，不看最终 Answer；
- Overlap 大到几乎复制整个 Chunk；
- 同时修改多个变量导致无法归因。

## 10. 🔍 继续追问

- 为什么 Recall 提升但最终回答可能变差？
- 如何判断 Overlap 导致重复污染？
- Chunk Size 与 Top-K 为什么要联动调？

<details><summary>查看参考答案：为什么 Chunk Size 与 Top-K 不能完全独立调？</summary>

因为二者共同决定最终 Context 的信息量。小 Chunk 往往需要更大的 K 才能覆盖完整证据；大 Chunk 即使 K 较小也可能带来大量 Token 和噪声。因此应从总 Candidate / Context Budget 角度联合评估。

</details>
