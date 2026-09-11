# 09｜Fixed / Recursive / Structure-aware / Semantic Chunk

## 1. 先讲人话

Chunk Strategy 决定“按照什么边界切”。不同文档的天然结构不同，所以不存在一个适合所有 Corpus 的切法。

常见策略可以理解为：

```text
最简单：Fixed
→ 尽量保留文本边界：Recursive
→ 尊重文档结构：Structure-aware
→ 尊重语义边界：Semantic
```

---

## 2. Fixed Chunk

按固定字符 / Token 长度切。

优点：

- 实现简单；
- 吞吐稳定；
- 容易批量处理。

缺点：

- 不理解段落、标题和逻辑；
- 容易把句子、表格、代码块切断。

适合：结构弱、格式统一、对切分边界不敏感的文本。

---

## 3. Recursive Chunk

按一组优先分隔符逐级尝试，例如：

```text
章节
→ 段落
→ 换行
→ 句子
→ 字符
```

它比 Fixed 更容易保留自然语言边界，是很多通用文档的实用起点。

但它仍然主要依赖“文本形式”，不真正理解业务语义。

---

## 4. Structure-aware Chunk

利用源文档结构：

- Markdown Heading；
- HTML DOM；
- PDF Layout；
- 表格；
- 法律条款；
- API 文档章节；
- 代码 AST。

例如：

```text
H2: 退款规则
  H3: 国内订单
  H3: 海外订单
```

Chunk 应保留 `section_path`，而不只是正文。

这种方式在企业知识库中通常比纯 Fixed 更可靠。

---

## 5. Semantic Chunk

根据语义变化决定边界，例如比较相邻句子的 Embedding，相似度明显下降时切开。

优点：

- 更接近主题边界；
- 对结构不规范文本可能有效。

代价：

- Ingestion 成本更高；
- 参数更多；
- 结果不一定稳定；
- 很容易出现“算法看起来高级，但实际指标没提升”。

所以 Semantic Chunk 必须做 Evaluation，而不是因为名字高级就默认更好。

---

## 6. Parent-child Strategy

严格来说它不是单纯切法，而是两层 Retrieval Model：

```text
Parent Section
├── Child 1
├── Child 2
└── Child 3

小 Child 用于召回
命中后回取 Parent
```

它能缓解“检索需要细粒度、生成需要完整上下文”的矛盾。

---

## 7. Strategy Selection Framework

先看数据：

| Corpus | 起始策略 |
|---|---|
| FAQ | Question/Answer 结构切分 |
| Markdown 文档 | Heading-aware |
| 法规 / 合同 | 条款 / 章节结构 |
| PDF 报告 | Layout + Heading |
| Code | AST / Symbol-aware |
| 普通长文本 | Recursive |
| 结构极差文本 | Recursive + Semantic 实验 |

然后通过 Evaluation Dataset 比较，而不是凭感觉选最终方案。

---

## 8. 🎯 面试怎么回答

> 常见 Chunk Strategy 有 Fixed、Recursive、Structure-aware 和 Semantic。Fixed 最简单但容易切断逻辑；Recursive 尽量保留自然文本边界；Structure-aware 利用标题、表格、条款等文档结构；Semantic 根据语义变化切分。实际项目一般先从与 Corpus 结构匹配的简单方案开始，再通过 Recall、Precision 和 End-to-end 指标验证是否需要更复杂策略。Parent-child 则常用于解决“细粒度检索、粗粒度生成”的冲突。

## 9. ⚠️ 易错点

- “Semantic Chunk 一定最好”——没有 Evaluation 不能这么说。
- “所有文档统一一种切法”——不同 Corpus 的天然结构不同。
- “切完只保留文本”——会丢失章节、位置和血缘。

## 10. 🔍 继续追问

- FAQ 为什么不适合固定长度切？
- 法律文档如何避免拆散充分必要条件？
- Semantic Chunk 的阈值怎么验证？

<details><summary>查看参考答案：为什么先从简单策略开始通常更好？</summary>

简单策略更容易解释、复现和做 Baseline。只有当 Evaluation 明确显示结构或语义边界问题时，再引入更复杂策略，才能知道复杂度真正带来了什么收益。

</details>
