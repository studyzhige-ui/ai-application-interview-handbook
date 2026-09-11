# 07｜Cleaning、Normalization、Dedup 与 Boilerplate Removal

## 1. 先讲人话

RAG 不是“把文件丢进 Embedding 就结束”。如果 Corpus 里混着重复页面、页眉页脚、导航、免责声明、乱码、旧版本和抽取噪声，那么后面的 Chunk、Embedding、Retrieval 会一起被污染。

因此 Ingestion 的第一条工程原则是：

> **先把可检索知识清理成稳定、可追溯的内容，再谈向量检索。**

---

## 2. 四类清理问题

### 2.1 Normalization

典型操作：

- Unicode / 空白归一；
- 连续换行整理；
- OCR 常见错字与断词修复；
- 标题层级标准化；
- URL / 文件路径规范化；
- 保留必要 Markdown / Table 结构。

不要把 Normalization 写成“所有格式都删掉”。结构本身就是语义。

### 2.2 Boilerplate Removal

网页 / PDF 常见噪声：

```text
页眉
页脚
公司版权
导航菜单
目录重复块
下载提示
Cookie Banner
```

如果这些文字在每页都重复，它们会制造大量高度相似 Chunk。

### 2.3 Dedup

至少要区分：

- 文件级完全重复；
- 文本级完全重复；
- 近重复；
- 同一文档不同版本。

前三类通常需要去重；最后一类不能简单删掉，因为它涉及 Freshness / Version。

### 2.4 Invalid Content

例如：

- 空页；
- OCR 只有乱码；
- Parser 只提取到水印；
- 内容长度异常；
- 解析失败但被错误标记为成功。

Production Pipeline 必须显式统计这些失败，而不是静默写入索引。

---

## 3. 去重不要只做字符串相等

可以形成多级策略：

```text
File Hash
→ Exact Text Hash
→ Canonical Text Hash
→ Near Duplicate
→ Version Relationship
```

其中 Near Duplicate 可以使用 SimHash / MinHash / Embedding Similarity 等辅助方法，但阈值必须通过真实语料验证。

---

## 4. 为什么重复内容会伤害 Retrieval

假设同一条政策被重复索引 20 次：

```text
Query
→ Top-10
→ 8 个结果其实来自同一份重复文档
```

那么候选集的“表面 Recall”看起来很高，实际 Coverage 很差。

重复还会导致：

- Reranker 候选浪费；
- Context 重复；
- Token Cost 增加；
- Citation 看起来有多个来源，实际上只有一个事实源。

---

## 5. 清理过程也必须可追溯

不要只存清理后的文本。建议至少保留：

```text
raw_document_id
parser_version
cleaner_version
raw_hash
clean_text_hash
removed_sections
quality_flags
```

这样 Bad Case 才能回答：

> “这段内容到底是源文件没有，还是 Parser / Cleaner 把它删掉了？”

---

## 6. AI 应用中的典型 Failure

### Failure A：把页眉当正文

结果：所有 Chunk 都带公司名和固定标题，Embedding 被公共噪声牵引。

### Failure B：去重过度

两个看起来高度相似的产品规格页，其实型号不同。错误合并会丢知识。

### Failure C：旧版本没有标记

搜索同时命中新旧制度，LLM 得到互相冲突的 Evidence。

---

## 7. 🎯 面试怎么回答

> RAG Ingestion 前需要做 Normalization、Boilerplate Removal、Invalid Content 过滤和分层去重。去重不能只做文本完全相等，还要识别近重复和版本关系。清理本身也要版本化和可追溯，因为 Parsing/Cleaning 错误会直接污染 Chunk 与 Retrieval。最终要用重复率、无效内容率和真实 Retrieval Case 验证清理是否有效。

## 8. ⚠️ 面试易错点

- “所有 HTML 标签都删掉”——可能把结构语义一起删掉。
- “相似就去重”——版本、型号、条款差异可能非常关键。
- “去重只节省存储”——它还直接影响 Recall Coverage、Rerank 和 Context Noise。

## 9. 🔍 继续追问

- 如何判断两个文档是版本关系而不是重复？
- Near Duplicate 阈值怎么定？
- 清理规则升级后是否需要全量 Re-index？

<details><summary>查看参考答案：为什么 Cleaning 是 Retrieval 的前置，而不是后处理？</summary>

因为错误和重复一旦进入 Chunk / Embedding / Index，后续每个阶段都会继承污染。越晚治理，定位成本越高。因此应该优先在 Corpus / Ingestion 层消除确定性噪声，并保留 Lineage 以便回溯。

</details>
