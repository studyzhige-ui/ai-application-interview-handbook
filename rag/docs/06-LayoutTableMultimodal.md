# 06｜Layout、Table、Image 与 Multimodal Document

## 1. 为什么纯文本 Parser 不够

企业知识里很多事实存在于：

```text
Table
Chart
Screenshot
Diagram
Multi-column Layout
Cross-page Structure
```

如果直接 `extract_text()`，内容可能还在，但**关系已经丢了**。

例如：

```text
产品 | 价格 | 生效日期
A    | 100  | 2026-01
B    | 200  | 2026-02
```

被拆成：

```text
产品 价格 生效日期 A 100 2026-01 B 200 2026-02
```

LLM 很难保证行列对应。

---

## 2. Layout 是语义的一部分

文档中的：

- 标题层级；
- 缩进；
- 列；
- Caption；
- 页眉 / 页脚；
- 图注；
- 表格位置；

都可能表达语义。

所以结构化 Parser 应尽量保留：

```text
element_type
reading_order
page
bbox
parent_heading
caption
```

---

## 3. Table 的三种常见处理方式

### 方式 A：转 Markdown / HTML

优点：

- 易进 LLM；
- 保留一定行列结构。

问题：

- 复杂合并单元格容易失真。

### 方式 B：转结构化 JSON

适合：

- 表格字段稳定；
- 后续可做结构化查询。

### 方式 C：保留图片 + 视觉模型理解

适合：

- 图表；
- 非规则表；
- 复杂布局。

实际系统可以组合使用。

---

## 4. Cross-page Table 为什么难

一个表跨两页时，第二页可能只有数据行，没有 Header。

如果按 Page 直接 Chunk：

```text
Page 1：Header + rows 1-20
Page 2：rows 21-40
```

第二块缺少字段语义。

修复思路：

- 检测表格延续关系；
- 复制 Header；
- 用 Table ID 串联；
- 保留前后 Page Link；
- Chunk 时按 Table 而不是 Page。

---

## 5. 图片怎样进入 RAG

可选路线：

```text
Image
→ OCR / Caption
→ Text Retrieval
```

或：

```text
Image
→ Multimodal Embedding
→ Cross-modal Retrieval
```

或：

```text
Image Candidate
→ Multimodal LLM
→ Final Reasoning
```

选择取决于：

- 是否主要是文字；
- 是否需要视觉关系；
- 成本；
- Query 类型。

---

## 6. Multimodal RAG 的 Lineage

图片 / 表格也需要：

```text
document_id
page
bbox
element_id
caption
source_uri
permission
version
```

否则最终 Citation 只能说“来自某份 PDF”，无法定位证据。

---

## 7. Failure Case

### 表格被切成很多普通段落

数字还在，行列关系没了。

### 图片只保存 OCR 文本

图表趋势、箭头、空间关系被丢失。

### 多模态模型全量解析所有页

质量可能好，但成本、延迟和可复现性变差。

更成熟的方案往往先做 Parser / Router，只对必要元素调用视觉模型。

---

## 8. 🎯 面试怎么回答

> 多模态文档的关键是保留结构，而不是只提取文字。表格需要保留行列、Header 和跨页关系；图片要判断 OCR 文本是否足够，还是需要 Multimodal Embedding / Vision Model。Parser 输出最好保留 element type、page、bbox、parent 和 source lineage，这样 Chunk、Retrieval 和 Citation 都能回到原始视觉证据。

---

<details>
<summary>自测：跨页表格为什么不能简单按 Page Chunk？</summary>

因为下一页的数据行可能失去 Header、Caption 和前页上下文，导致字段语义断裂。应该识别同一 Table 的连续关系，并按结构恢复后再切分。

</details>
