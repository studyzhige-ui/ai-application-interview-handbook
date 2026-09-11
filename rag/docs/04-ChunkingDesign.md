# 04｜Chunking Design：原则、Strategy、Size、Overlap 与实验方法

Chunking 的本质不是“把文档切成 512 Token”，而是决定：

> **什么粒度的内容应该作为一次 Retrieval Unit，被独立召回并交给下游排序与生成？**

因此 Chunk Principle、Strategy、Size 和 Overlap 应该在同一个设计闭环中学习。

---

## 1. 为什么不能整篇文档直接 Embedding

如果文档很长：

```text
one document
→ one embedding
```

会把很多主题压进一个 Vector。

Query 只问其中一个细节时：

- Vector 表示过于平均；
- 返回整篇文档浪费 Context；
- Reranker 输入过长；
- Citation 粒度太粗。

所以需要把文档拆成更小 Retrieval Unit。

---

## 2. 但 Chunk 越小也不是越好

如果切得太小：

```text
一句话
一句话
一句话
```

会失去：

- 上下文；
- 主语；
- 定义与解释关系；
- 表格 Header；
- 前后条件；
- Section 语义。

所以 Chunking 永远是：

```text
Retrieval Specificity
vs
Semantic Completeness
```

的 Trade-off。

---

## 3. Chunk Size 的核心矛盾

### Large Chunk

优点：

- 语义完整；
- 更容易包含答案上下文；
- Citation 不容易断裂。

代价：

- Embedding 主题混合；
- Rerank 成本高；
- Context 占用大；
- 一个 Chunk 可能包含大量无关内容。

### Small Chunk

优点：

- 定位精细；
- 候选更纯；
- Context 利用率高。

代价：

- 语义被切断；
- Query 需要跨 Chunk 才能回答；
- Top-K 需要更多候选；
- 邻接恢复更复杂。

没有通用最佳值。

---

## 4. Fixed-size Chunk

最简单：

```text
每 N tokens 切一次
```

优点：

- 实现简单；
- 容量可预测；
- 适合快速 Baseline。

问题：

```text
可能在句子 / 表格 / Section 中间切断
```

所以它适合做基线，不一定是最终方案。

---

## 5. Recursive / Separator-based Chunk

优先按较大语义边界分割：

```text
Section
→ Paragraph
→ Sentence
→ Token
```

只有超过目标大小才继续向下切。

优点是比固定长度更尊重文本结构。

但如果原始 Parser 已经丢失结构，Recursive Splitter 也无法凭空恢复。

---

## 6. Structure-aware Chunk

对于 Markdown / HTML / Docs：

```text
Heading hierarchy
List
Code Block
Table
```

都可以参与 Chunk Boundary。

例如：

```text
H2 Section
→ one or more chunks
→ each keeps heading path
```

这样检索到 Chunk 时仍知道：

```text
Product > Authentication > Token Refresh
```

提高可解释性和 Context Construction。

---

## 7. Semantic Chunk

Semantic Chunking 尝试根据内容变化判断边界：

```text
sentence embeddings
→ detect semantic shift
→ split
```

理论上能避免纯 Token Boundary。

但代价包括：

- 更多 Embedding Cost；
- 算法参数；
- 边界不稳定；
- Rebuild 可重复性更难；
- 不一定比结构化 Chunk 更好。

所以必须通过 Eval 证明。

---

## 8. Overlap 为什么存在

假设重要事实跨越 Chunk Boundary：

```text
Chunk A ends: “This policy applies when ...”
Chunk B starts: “the user is an enterprise customer.”
```

完全无 Overlap 可能让条件和结论分离。

Overlap 通过复制邻近 Token：

```text
Chunk A: 1–512
Chunk B: 449–960
```

降低边界信息丢失。

---

## 9. Overlap 不是越大越好

Overlap 太大会：

- Index Size 增长；
- Embedding Cost 增长；
- Top-K 返回大量近重复 Chunk；
- Context 重复；
- Reranker 浪费算力。

所以 Overlap 是边界补偿机制，不是免费提高 Recall 的旋钮。

---

## 10. Chunk Size 应由 Query Pattern 决定

如果用户常问：

```text
“这个 API 参数默认值是多少？”
```

小而精确的 Chunk 可能更好。

如果常问：

```text
“这一政策适用于哪些条件，例外是什么？”
```

需要更完整上下文。

所以应分析：

```text
Question granularity
Answer span length
Document structure
Reranker max length
LLM context budget
```

再设计 Chunk。

---

## 11. 不同内容类型应有不同策略

不要对所有文档统一：

```text
512 + overlap 64
```

可以按类型：

### API Doc

```text
endpoint / section aware
```

### Contract

```text
clause aware
```

### FAQ

```text
one Q&A as unit
```

### Table

```text
header + row group
```

### Code

```text
function / class / AST boundary
```

这比全局固定值更符合知识结构。

---

## 12. Chunk Header / Context Enrichment

一个正文段落：

```text
“It expires after 30 days.”
```

单独 Embedding 很模糊。

如果添加结构 Header：

```text
Document: Enterprise Trial Policy
Section: Expiration
“It expires after 30 days.”
```

语义更完整。

但 Enrichment 也会增加 Token 和重复信息，需要 Eval。

---

## 13. Chunk 参数必须通过实验选择

不要用：

```text
“业界都用 512”
```

作为理由。

更正确的实验：

```text
same corpus
same embedding
same retriever
same eval queries

variant A: 256 / overlap 32
variant B: 512 / overlap 64
variant C: structure-aware
```

比较：

- Recall@K；
- MRR / NDCG；
- Reranker Quality；
- Context Tokens；
- Answer Quality；
- Index Size / Cost。

---

## 14. Chunking Failure 怎么看

常见 Bad Case：

### Answer span 被切断

```text
Ground truth split across chunks
```

### Chunk 太大

```text
retrieved chunk contains answer
but reranker / LLM distracted by unrelated content
```

### Chunk 太小

```text
retrieved text lacks subject / condition
```

### Duplicate overlap

```text
Top5 = same paragraph repeated 5 times
```

这些应该在 Bad Case Attribution 中单独标记。

---

## 15. Chunking 和 Embedding Model 有关系

Embedding Model 有最大输入长度。

Chunk 超过模型有效长度可能：

- 截断；
- 表示质量下降；
- 计算更贵。

因此 Chunk Size 不能脱离模型 Input Limit。

---

## 16. Chunking 和 Reranker 有关系

Reranker 通常对：

```text
query + candidate
```

一起编码。

Chunk 太长会导致：

- Input Truncation；
- Latency 增长；
- Candidate 数减少。

所以 Chunk Design 是整个 Retrieval Funnel 的前置参数。

---

## 17. 常见错误

- Chunk 越小 Recall 越高：不一定。
- Overlap 越大越安全：会制造重复和成本。
- Semantic Chunk 一定比 Recursive 好：需要 Eval。
- Chunk Size 是 Vector DB 参数：它属于 Retrieval Data Model。
- 一套 Size 适合所有文档类型：错误。
- “512”本身就是合理解释：不是。

---

## 18. 面试怎么答

### Q：Chunk Size 怎么定？

> 我不会直接给固定值。先看文档结构、典型 Query 粒度、答案跨度、Embedding/Reranker 长度限制和 LLM Context Budget，再建立几个策略 Baseline，用真实 Evaluation Query 比较 Recall、Ranking、Answer Quality、Context Token 和 Index Cost。Chunk 是 Retrieval Unit，目标是在语义完整性和检索精度之间找到 Operating Point。

### Q：Overlap 为什么需要？

> 它主要补偿 Chunk Boundary，把跨边界的上下文复制到相邻 Chunk，降低答案/条件被切断的概率；但太大又会造成 Index 膨胀、重复候选和 Context 浪费，所以也必须实验。

---

## 19. 自测

<details><summary>1. 为什么不存在通用最佳 Chunk Size？</summary>
因为最优粒度取决于文档结构、Query/Answer 粒度、Embedding/Reranker 限制、Context Budget 和业务指标。
</details>

<details><summary>2. 为什么 Overlap 会影响 Top-K Diversity？</summary>
大量重叠会生成高度相似 Chunk，它们可能同时占据前几个候选，挤掉其它相关证据。
</details>

<details><summary>3. Chunking 改动为什么必须跑 End-to-end Eval？</summary>
它不仅改变 Retriever Recall，还会改变 Reranker 输入、Context Token 和最终生成质量。
</details>
