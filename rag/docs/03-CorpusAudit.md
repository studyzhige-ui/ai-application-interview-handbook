# 03｜Corpus Audit：先审计数据，再谈检索

## 1. 为什么第一步不是选 Embedding

如果知识库本身：

- 有很多重复文档；
- 新旧版本混在一起；
- 扫描 PDF 解析失败；
- 权限标签缺失；
- 真实数据只有 2 万条，却按“亿级”设计；

那么后面讨论 HNSW、Rerank 都可能是在优化错误问题。

所以 Production RAG 的第一步应该是：

> **先知道自己到底有什么数据。**

---

## 2. Corpus Audit 要回答什么

### 来源

```text
Wiki?
Confluence?
PDF?
Database?
Object Storage?
Website?
Git Repo?
User Upload?
```

不同来源决定：

- 更新方式；
- 权限；
- Parser；
- 增量同步。

### 规模

不要只统计“文档数”。

还要看：

```text
Raw bytes
Pages
Parsed text size
Chunks after split
Total tokens
Images / tables
Daily change volume
```

### 质量

- 空文件；
- OCR 错字；
- 重复；
- 过期；
- Boilerplate；
- Broken encoding；
- 内容冲突。

### 权限

每个文档是否有：

- Tenant；
- ACL；
- Group；
- Owner；
- Confidentiality Level。

---

## 3. Version 冲突是最危险的数据问题之一

例如：

```text
Employee-Handbook-v1.pdf
Employee-Handbook-v2.pdf
Employee-Handbook-final.pdf
Employee-Handbook-final-final.pdf
```

如果全索引：

> 同一个问题可能召回互相矛盾的政策。

所以必须定义：

```text
Source of Truth
Canonical Document
Version Policy
Effective Time
Superseded By
```

---

## 4. Query Distribution 也属于 Corpus Audit

只看文档不够，还要看用户会怎么问。

例如：

```text
Corpus 是产品文档
用户 Query 却大量是故障码 + 版本号
```

那么 Sparse / Keyword 价值可能比纯 Dense 更高。

需要采样：

- Search Log；
- FAQ；
- Support Ticket；
- Internal Chat；
- User Interview。

因为 RAG 是：

```text
Corpus Distribution
×
Query Distribution
```

共同决定的系统。

---

## 5. 建立 Corpus Profile

可以维护：

```text
source_type
language
file_type
size
page_count
token_count
updated_at
version
owner
permission
parser_status
quality_flags
```

然后统计：

```text
PDF 占比
扫描件占比
表格占比
重复率
解析失败率
平均更新周期
权限分布
```

这些数据会直接影响后续设计。

---

## 6. 不同 Corpus 对 Chunk Strategy 的影响

### FAQ

天然问答单元，不一定需要固定长度切块。

### Product Manual

标题层级明显，适合 Structure-aware。

### Contract / Regulation

条款边界重要，不能随意打断条件关系。

### Long Report

可能需要 Parent-child / Section Summary。

### Source Code

结构单位可能是 Symbol / Function / Class，而不是自然段。

所以 Chunk 不是先拍一个 512 Token 默认值。

---

## 7. Audit 输出应该是什么

至少得到一份可执行结论：

```text
Corpus Scope
Source of Truth
Parser Matrix
Permission Model
Update Frequency
Estimated Chunk Count
Query Types
Known Quality Risks
Evaluation Sampling Plan
```

之后才进入 Parser / Chunk / Retrieval 设计。

---

## 8. Failure Case

### Demo Corpus 很干净，上线数据很脏

本地 100 个 Markdown 效果很好，上线 30 万 PDF 后质量崩。

### 只统计文档数

10 万份短 FAQ 和 10 万份 200 页 PDF 完全不是同一个规模。

### 没有真实 Query

团队只用自己编的“漂亮问题”评测，线上用户缩写、拼写错、型号词一来全部 Miss。

---

## 9. 🎯 面试怎么回答

> RAG 设计前我会先做 Corpus Audit，而不是先选向量库。至少统计数据来源、真实规模、文件类型、语言、OCR / 表格比例、重复和版本冲突、更新频率、权限模型，同时采样真实 Query Distribution。因为 Parser、Chunk、Dense/Sparse 策略、增量更新和 Evaluation Set 都依赖这些事实。Corpus 不干净时，后面调 Embedding 或 HNSW 往往是在优化错误层。

---

<details>
<summary>自测：为什么 Query Log 也属于 Corpus Audit 阶段的重要输入？</summary>

因为检索策略由“有什么知识”和“用户怎么问”共同决定。只看文档无法判断是否需要 Keyword、Query Rewrite、Clarification 或特定 Evaluation Case。

</details>
