# 11. Advanced Chunk Structure：Parent-child、Neighbor、Semantic Boundary 与 Chunk Data Model

基础 Chunking 决定“切多大”；这一章解决更难的问题：

> **如果检索需要小粒度，但回答又需要大上下文，怎样同时满足？如何让 Chunk 可追溯、可扩展、可权限过滤？**

因此 Parent-child、Neighbor、Semantic Boundary 和 Chunk Data Model 应属于同一个“高级 Retrieval Unit”知识块。

---

## 1. Small Chunk / Large Context 的矛盾

Retriever 往往喜欢：

```text
small focused chunk
```

因为语义更纯。

生成模型往往需要：

```text
larger surrounding context
```

因为要理解条件、定义和例外。

这两个需求可以通过“检索粒度”和“上下文粒度”分离解决。

---

## 2. Parent-child Retrieval

一种典型结构：

```text
Parent Section
├── Child Chunk A
├── Child Chunk B
└── Child Chunk C
```

Index Child：

```text
small unit → easier retrieval
```

命中 Child 后返回：

```text
parent section / selected siblings
```

于是：

```text
fine retrieval
+
rich generation context
```

兼得。

---

## 3. Parent 为什么不能无限大

如果 Parent 是整篇 50 页 PDF：

```text
child hit
→ return entire document
```

就失去意义。

Parent 通常应该是：

- Section；
- Subsection；
- FAQ Group；
- Function / Class；
- Table + Description。

仍然要符合 Context Budget。

---

## 4. Neighbor Window

有些文档天然是连续文本。

命中：

```text
chunk_i
```

可以扩展：

```text
chunk_{i-1}
chunk_i
chunk_{i+1}
```

这叫 Neighbor Expansion。

它适合补全跨 Chunk 上下文，但要防：

- Context 重复；
- 邻居其实属于不同 Section；
- 多个命中 Chunk 扩展后大面积重叠。

---

## 5. Semantic Boundary Failure

即使使用语义/结构化切分，也可能发生：

### Definition 与 Exception 分离

```text
Chunk A: general rule
Chunk B: exception
```

只召回 A 会得到错误结论。

### Table Header 与 Row 分离

```text
Chunk A: columns
Chunk B: values
```

Row 没有 Header 就不可解释。

### Pronoun / Reference 分离

```text
Chunk B starts: “It is valid for 30 days.”
```

不知道 `it` 指什么。

高级 Chunk Structure 的目标就是让这些依赖关系可恢复。

---

## 6. Retrieval Unit 不等于 Storage Unit

可以有：

```text
Stored Parent Document
Stored Chunk
Stored Sentence / Node
```

而真正参与 ANN / BM25 的可能只是某一层。

所以系统要明确：

```text
Index Unit
Return Unit
Citation Unit
```

它们可以不同。

---

## 7. 一个成熟 Chunk Data Model

可以至少包含：

```text
chunk_id
document_id
parent_id
section_path
ordinal
text
content_hash
source_uri
page / bbox
content_version
parser_version
chunker_version
embedding_version
tenant_id
permission_scope
created_at
```

不是每个系统都需要全部字段，但必须支持：

- Traceability；
- Update/Delete；
- Parent/Neighbor；
- Permission；
- Citation；
- Version；
- Debug。

---

## 8. Hierarchy 怎么设计

常见：

```text
Document
→ Section
→ Subsection
→ Chunk
→ Sentence
```

不同层可以承担：

```text
retrieval
context expansion
citation
summary
```

例如：

```text
search child chunk
→ return parent section
→ cite original page
```

---

## 9. Chunk Metadata 为什么不能无限塞正文

有人为了补语义，会把：

```text
title
path
author
permissions
version
```

全部拼到 Embedding Text 中。

问题是：

- 相同 Metadata 重复污染向量；
- Token Cost 增大；
- 权限字段可能不应参与语义；
- Structured Filter 和 Semantic Signal 混在一起。

应该区分：

```text
Embedding Content
vs
Metadata / Filter Fields
```

只有真正需要语义增强的 Header 才考虑加入 Embedding 文本。

---

## 10. Contextualized Chunk

有些系统会给每个 Chunk 添加短 Context：

```text
“本段来自企业退款政策的海外订单章节。”
+
original chunk
```

这种 Contextual Enrichment 可以减少 Chunk 脱离上下文后的歧义。

但它必须：

- 可版本化；
- 成本可控；
- 通过 Eval 证明有收益；
- 不制造事实幻觉。

---

## 11. Chunk ID 应该怎样生成

完全随机 UUID 简单，但 Diff / Incremental Update 不方便。

可考虑：

```text
stable document_id
+
logical path / ordinal
+
content hash / version
```

但也要避免：

- 内容小改导致全部 ID 级联变化；
- Ordinal 改变造成缓存大量失效。

ID 策略和更新模型要一起设计。

---

## 12. Parent-child 如何影响 Index 数量

可能只 Index Child：

```text
child vector index
→ fetch parent by parent_id
```

也可以同时 Index：

```text
parent summary
child detail
```

做多粒度检索。

后者会增加：

- Index Size；
- Fusion Complexity；
- Evaluation 难度。

所以不是层级越多越高级。

---

## 13. Duplicate Context 怎么合并

如果 Top5 命中：

```text
child 1 from parent A
child 2 from parent A
child 3 from parent A
```

Parent Expansion 后不能把 Parent A 重复三次。

Context Builder 应做：

```text
stable dedup
merge overlapping windows
preserve best evidence score / source mapping
```

这也是为什么 Retrieval Result 需要结构化 ID，而不是只有文本字符串。

---

## 14. Citation Unit 设计

用户看到的 Citation 可以是：

```text
Document
Page
Section
Paragraph
Chunk
```

如果 Chunk 是内部技术单元，不一定适合直接展示。

因此可通过 Lineage 映射：

```text
internal chunk_id
→ user-visible document/page/section
```

---

## 15. 常见错误

- Parent-child 就是把所有 Child 的 Parent 全文返回：要受 Budget 约束。
- Neighbor Window 固定 ±1 永远合理：要尊重结构边界。
- Chunk Metadata 越多都应该拼进 Embedding 文本：错误。
- 随机 ID 不影响更新：会增加增量维护和调试困难。
- Index Unit = Context Unit = Citation Unit：不一定。

---

## 16. 面试怎么答

### Q：小 Chunk 和完整上下文怎么兼顾？

> 可以把 Retrieval Unit 和 Context Unit 分离，例如 Index 小 Child Chunk，命中后根据 parent_id 或 neighbor relationship 扩展到较大的 Section/Window；这样保持召回粒度，同时给 LLM 足够上下文。需要用稳定 Chunk Data Model 记录 hierarchy、position、version、permission 和 lineage，并在 Context Builder 去重合并重叠扩展。

### Q：Chunk Data Model 为什么重要？

> 因为 Parent-child、增量更新、删除、权限、Citation、Bad Case Replay 都依赖稳定 ID 和 Lineage。只存 `text + vector` 很难支持 Production 生命周期。

---

## 17. 自测

<details><summary>1. Index Unit 和 Return Unit 为什么可以不同？</summary>
小单元更利于精准召回，而生成可能需要更大的上下文，因此可以命中小 Chunk 后扩展 Parent/Neighbor。
</details>

<details><summary>2. 为什么 Permission 应作为 Metadata，而不是简单拼进 Embedding Text？</summary>
权限是硬过滤约束，不应依赖语义相似度决定，而且拼接会污染向量表示。
</details>

<details><summary>3. Parent-child 最大的额外工程成本是什么？</summary>
需要维护稳定层级关系、扩展/去重逻辑、更多版本一致性和更复杂 Evaluation。
</details>
