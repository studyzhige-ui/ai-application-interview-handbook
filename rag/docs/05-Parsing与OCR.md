# 05｜Parsing：PDF / Markdown / HTML / Office / OCR

## 1. Parser 是 Retrieval 的第一层 Recall

如果原文根本没有被正确解析出来，后面所有 Retrieval 都无能为力。

所以可以把 Parsing 看成：

> **RAG 最前面的 Recall Gate。**

错误的 Parser 会产生：

```text
Missing Text
Wrong Reading Order
Broken Table
Header Noise
OCR Error
Page Boundary Loss
```

这些错误会一路传到 Chunk、Embedding 和 Generation。

---

## 2. 不同文档不是同一种问题

### Markdown / Plain Text

结构通常比较清晰：

- Heading；
- List；
- Code Block；
- Table。

### HTML

要去掉：

- Navigation；
- Footer；
- Cookie Banner；
- Script / Style；
- Related Links。

### Office

要保留：

- Heading；
- Paragraph；
- Table；
- Sheet；
- Slide；
- Notes。

### PDF

最复杂，因为 PDF 更像“页面绘制指令”，不一定有天然阅读顺序。

---

## 3. Electronic PDF vs Scanned PDF

### Electronic PDF

通常存在文本层，可以直接提取文字。

但仍可能有：

- 多栏顺序错；
- 字符编码问题；
- 表格拆碎；
- Header / Footer 重复。

### Scanned PDF

本质上是一页页图片，需要：

```text
Image
→ OCR
→ Layout Analysis
→ Text / Table / Block
```

所以不能对所有 PDF 使用同一 Parser 路径。

---

## 4. Parser Router

Production 可以先检测：

```text
file type
text layer exists?
scan ratio?
layout complexity?
table / image density?
```

再路由：

```text
Simple Text Parser
Document Parser
OCR Pipeline
Vision Model
Specialized Table Parser
```

这比所有文件统一跑最昂贵 OCR 更合理。

---

## 5. Reading Order

双栏论文常出现：

```text
左栏第一段
右栏第一段
左栏第二段
右栏第二段
```

被错误解析成：

```text
左栏第一段
左栏第二段
右栏第一段
右栏第二段
```

Embedding 看见的已经不是原文逻辑。

所以 Parser 质量不能只看“有没有提取到字”。

---

## 6. OCR Error 的传播

例如型号：

```text
O1-2026
```

OCR 错成：

```text
01-202G
```

Dense Retrieval 也许还能模糊召回，但 BM25 / 精确检索可能直接 Miss。

所以专有名词、编号、金额、日期场景需要专门 QA。

---

## 7. Parser Output 不应该只有纯文本

更好的中间表示可以保留：

```text
Element
├─ type: heading / paragraph / table / image / code
├─ text
├─ page
├─ bbox
├─ parent
├─ order
└─ metadata
```

这样后面 Chunk 才能 Structure-aware，并且 Citation 能回到 Page / Region。

---

## 8. Parsing Evaluation

建议建立 Parser Test Set：

- 普通文本 PDF；
- 扫描件；
- 双栏；
- 多页表格；
- 图片 Caption；
- 中英混排；
- 公式；
- 代码；
- Header / Footer。

指标不一定只有一个数字，可以同时检查：

```text
Text Coverage
Reading Order
Table Integrity
OCR Accuracy
Structure Preservation
```

---

## 9. Failure Case

### Parser 改版后 Recall 突然下降

可能不是 Embedding 变差，而是 Reading Order / Heading 丢失。

### OCR 全量开启导致成本爆炸

大量电子 PDF 本来可直接提取。

### Parser 只输出 Markdown

如果转换过程丢掉 Page / BBox，Citation 可能无法回原文位置。

---

## 10. 🎯 面试怎么回答

> Parsing 是 RAG 的第一层 Recall。不同文档要区分电子 PDF、扫描 PDF、HTML、Office 等路线；PDF 尤其要处理 Reading Order、Table、Header / Footer 和 OCR。Production Parser 最好输出结构化 Element，而不只是纯文本，并保留 page / bbox / parent / type 作为后续 Chunk 和 Citation 的 Lineage。Parser 也需要自己的 Test Set，否则检索下降时很容易误怪 Embedding。

---

<details>
<summary>自测：为什么扫描 PDF 和电子 PDF 不应该默认走完全相同流程？</summary>

扫描 PDF 没有可靠文本层，需要 OCR / Layout；电子 PDF 常能直接提取文本，强行统一走 OCR 会增加成本并可能引入新的识别错误。

</details>
