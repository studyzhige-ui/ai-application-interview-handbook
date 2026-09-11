# 19｜Sparse Retrieval / BM25：精确词为什么仍重要

## 1. 先讲人话

Sparse Retrieval 关注的是词项匹配。BM25 是其中最经典的排序方法之一。

它特别适合：

- 错误码；
- 产品编号；
- 人名 / 地名；
- 专有名词；
- 法规条款号；
- 精确短语。

也就是那些“字面上必须对”的问题。

---

## 2. BM25 的核心直觉

BM25 主要考虑：

```text
某个词在当前文档里是否重要
+
这个词在整个语料里是否稀有
+
文档长度归一化
```

可以粗略理解为：

- 一个词在文档里出现，多一些通常更重要；
- 但出现次数的收益会饱和；
- 在所有文档都常见的词，区分度低；
- 稀有词区分度更高。

---

## 3. 为什么 Keyword 时代没有结束

假设用户搜索：

```text
ERR-1042
```

Dense 可能召回“连接错误”“网络异常”等语义相似内容；BM25 则能直接把包含 `ERR-1042` 的文档排到前面。

对于：

```text
SKU
函数名
API 名
版本号
制度编号
```

精确词项往往比语义泛化更可靠。

---

## 4. Sparse Retrieval 的弱点

### 同义表达

用户说“离职”，文档写“劳动关系终止”，词面可能不重合。

### 拼写 / 词形变化

取决于 Analyzer / Tokenizer。

### 长自然语言 Query

大量低价值词项可能稀释真正意图。

所以 Sparse 和 Dense 是互补的，而不是互相淘汰。

---

## 5. Analyzer 很重要

BM25 的实际表现不仅由公式决定，还取决于：

- 中文分词；
- Lowercase；
- Stop Words；
- Stemming / Lemmatization；
- Synonym；
- N-gram；
- Keyword Field。

例如产品 ID 不应该被普通 Analyzer 拆坏。

---

## 6. Field-aware Search

企业文档常有多个字段：

```text
title
heading
body
product_id
tags
```

可以给予不同权重，例如标题命中比正文命中更强。

但权重同样需要实验，不要凭经验堆参数。

---

## 7. 怎样评估 Sparse

和 Dense 一样，需要 Ground Truth。

重点看不同 Query Slice：

- Exact Term；
- Short Query；
- Natural Language；
- Rare Entity；
- Synonym Query。

通常 Sparse 会在 Exact / Rare Term Slice 上更强。

---

## 8. 🎯 面试怎么回答

> Sparse Retrieval / BM25 依赖词项匹配和 IDF 等统计信号，特别擅长错误码、产品编号、专有名词和精确短语。Dense 擅长语义泛化，但可能忽略词面精确性，所以两者通常互补。BM25 的实际效果还依赖 Analyzer、Field 权重和 Query 分布，最终应在真实 Dataset 上按 Query Slice 比较。

## 9. ⚠️ 易错点

- “有 Embedding 后 BM25 没用了”；
- 忽略中文分词和 Analyzer；
- 产品编号被错误 Tokenize；
- 不区分不同 Query 类型，只看总平均指标。

## 10. 🔍 继续追问

- BM25 为什么会有词频饱和？
- Title / Body 权重怎么调？
- 中文 Sparse Retrieval 最容易踩什么坑？

<details><summary>查看参考答案：为什么 Hybrid Retrieval 经常优于单独 Dense？</summary>

因为 Dense 和 Sparse 使用不同信号：前者提供语义泛化，后者提供精确词项匹配。真实 Query 同时包含概念性问题和错误码、实体、版本号等精确需求，因此合并两类信号通常覆盖更广。

</details>
