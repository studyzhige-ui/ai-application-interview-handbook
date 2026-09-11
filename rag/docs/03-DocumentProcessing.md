# 05. Document Processing：Parsing、OCR、Layout、Multimodal、Cleaning 与 Dedup

RAG 的第一道质量门槛不是向量检索，而是：

> **原始文档有没有被正确还原成可检索的信息结构？**

PDF、扫描件、网页、Office、表格和图片都可能在解析时丢失语义。

所以 Parsing、Layout、OCR、Cleaning 和 Dedup 应该作为一个完整“Document Processing”子系统学习。

---

## 1. 为什么不能直接 `extract_text()` 就结束

文档里的语义不仅来自字符，还来自结构：

```text
Heading
Paragraph
List
Table
Caption
Footnote
Page
Section
Image
Code Block
```

如果 Parser 只输出一串纯文本：

```text
标题层级消失
表格列错位
页眉页脚混进正文
图片信息丢失
```

后续 Chunk 再聪明也无法恢复原结构。

---

## 2. 不同 Source 的解析难点

### Markdown / HTML

结构相对明确，但要处理：

- Navigation；
- Boilerplate；
- Hidden Element；
- Link / Anchor；
- Code Block。

### PDF

PDF 更像“页面绘制格式”，并不天然保存正确阅读顺序。

常见问题：

```text
双栏顺序错
Header / Footer 混入
表格变散乱 Token
断行
页码
扫描图片无文字层
```

### Office

需要保留：

- Heading；
- Table；
- Sheet / Slide；
- Notes；
- Embedded Object。

---

## 3. OCR 什么时候需要

如果 PDF 只是扫描图片：

```text
no text layer
```

普通 Parser 得不到正文，需要 OCR。

OCR Pipeline 可以理解为：

```text
page image
→ layout / region detection
→ text recognition
→ reading order
→ confidence
```

OCR 错误会直接变成检索噪声，例如：

```text
0 ↔ O
1 ↔ l
表格数字错位
```

因此应保留 OCR Confidence / Page Metadata，便于后续质量分析。

---

## 4. Layout 为什么重要

假设一页两栏：

```text
left column A B C
right column D E F
```

错误读取顺序可能变成：

```text
A D B E C F
```

语义完全被破坏。

Layout-aware Parser 会尝试恢复：

```text
Block
Bounding Box
Reading Order
Section Hierarchy
```

这对论文、报告、合同尤其重要。

---

## 5. Table 为什么不能简单 Flatten

例如：

| Product | Q1 | Q2 |
|---|---:|---:|
| A | 10 | 20 |
| B | 12 | 25 |

如果变成：

```text
Product Q1 Q2 A 10 20 B 12 25
```

模型未必知道列关系。

可以考虑：

- Markdown Table；
- Row-wise serialization；
- Table summary + raw structure；
- 单独 Table Chunk；
- Query-time Structured Tool。

具体选法要由 Query Pattern 和 Eval 决定。

---

## 6. Image / Multimodal Document 怎么处理

图片可能承担：

- Chart；
- Diagram；
- Screenshot；
- Form；
- Product Image；
- Slide Visual。

可选策略：

```text
image → caption / OCR / VLM extraction
→ multimodal embedding / text representation
```

不要自动假设“图片内容都能靠 OCR 转文字”，图表关系往往需要 Vision Model 理解。

---

## 7. 保留结构，再决定 Chunk

一个好的 Parser 输出应该尽量像：

```text
Document
├── Section
│   ├── Heading
│   ├── Paragraph
│   ├── Table
│   └── Figure
└── Section
```

而不是：

```text
one giant string
```

Chunking 应在结构信息仍存在时做决策。

---

## 8. Cleaning 解决什么

典型脏内容：

```text
Page Header / Footer
Cookie Banner
Navigation
Repeated Legal Footer
Broken Unicode
Invisible Character
Extra Whitespace
Generated TOC
Tracking Params
```

Cleaning 的目标不是“文本越短越好”，而是：

> **删除对检索没有价值、会污染相似度或重复结果的内容，同时保留语义结构。**

---

## 9. Normalization 要谨慎

可能做：

- Unicode normalize；
- Whitespace normalize；
- URL canonicalization；
- Case normalize（视业务）；
- 标点统一。

但不要破坏：

- Code；
- ID；
- SKU；
- Formula；
- Legal clause number；
- Case-sensitive symbol。

Normalization 必须知道领域语义。

---

## 10. Exact Dedup

可以根据：

```text
content hash
canonical URL
source ID
```

识别完全重复文档。

好处：

- 减少 Index；
- 避免 Top-K 被同一内容占满；
- 降低 Embedding Cost。

---

## 11. Near Duplicate 更难

例如：

```text
政策 v1
政策 v1 copied to another folder
政策 v1 + one paragraph changed
```

可以使用：

- normalized text hash；
- shingling / MinHash；
- embedding similarity；
- source metadata。

但 Near-dedup 要防误删真正不同文档。

---

## 12. Boilerplate 为什么特别危险

假设每份文档都有相同 Footer：

```text
Company Confidential - Contact support@example.com
```

如果每个 Chunk 都带这段：

```text
Embedding gets repeated signal
Sparse index repeated term
Top-K may return many duplicates
```

所以 Boilerplate Removal 能显著提高 Corpus Signal-to-noise。

---

## 13. Parser Version 必须可追踪

如果 Parser 升级：

```text
v1 reading order wrong
v2 fixed
```

需要知道：

```text
哪些 Chunk 来自 v1？
是否需要 Reparse / Re-embed？
```

因此建议记录：

```text
parser_version
ocr_version
cleaning_version
```

这和上一章 Lineage 直接连接。

---

## 14. Parsing 质量怎么评估

可以建立文档级 QA Sample：

```text
Expected heading structure
Expected table values
Expected OCR text
Expected page/source mapping
```

并监控：

- Parse Success Rate；
- Empty Document Rate；
- OCR Confidence；
- Table Parse Failure；
- Chunk Count Distribution；
- Duplicate Ratio。

不要等最终 RAG Answer 错了才发现 Parser 早就丢信息。

---

## 15. Failure Attribution

如果回答缺少一个表格数字：

```text
Source has it?
→ Parser extracted it?
→ Table structure preserved?
→ Chunk contains it?
→ Retriever recalled it?
```

如果第二步就失败，调 HNSW 或 Reranker没有意义。

---

## 16. 常见错误

- PDF 有文本层就等于解析正确：错误。
- OCR 成功率高就表示内容质量高：还要看 Layout/数字/表格。
- 所有表格都转纯文本就行：可能丢结构。
- Cleaning 越激进越好：可能删掉业务关键 ID/格式。
- Dedup 就是删除相似内容：要区分版本和合法相似文档。

---

## 17. 面试怎么答

### Q：复杂 PDF 怎么做 RAG？

> 我会先把 Parsing 视为独立质量层：检测文本层/OCR，恢复 Layout 和 Reading Order，对 Table/Image 使用结构化或 Multimodal 解析，并保留 page/bbox/source lineage。之后再 Cleaning/Dedup 和 Chunk。Bad Case 中先验证 Parser 是否保留了 Ground Truth，再判断 Retrieval。

### Q：为什么要 Dedup？

> 重复文档会浪费 Embedding/Index 资源，还可能让 Top-K 被同一内容占满、放大 Boilerplate 信号。但需要区分 Exact Duplicate、Near Duplicate 和 Historical Version，不能简单按相似度删除。

---

## 18. 自测

<details><summary>1. 为什么 Layout 是 Retrieval Quality 的上游？</summary>
因为错误阅读顺序会直接破坏段落/表格语义，后续 Chunk 和 Embedding 无法恢复原关系。
</details>

<details><summary>2. Cleaning 为什么不能统一 lower-case 所有内容？</summary>
因为 Code、ID、SKU 等领域信息可能区分大小写或格式。
</details>

<details><summary>3. Parser Upgrade 为什么可能需要 Re-embedding？</summary>
解析输出内容/结构改变后，Chunk 内容也会改变，旧 Embedding 不再对应新文本。
</details>
