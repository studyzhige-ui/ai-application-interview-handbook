# 08｜为什么 Chunking 是 RAG 核心

## 1. 先讲人话

Chunking 决定了系统“以什么粒度理解和召回知识”。

如果一整本手册只存成一个 Chunk，检索虽然可能命中，但 Context 会巨大且噪声很多；如果一句话切成一个 Chunk，语义关系又可能被拆散。

所以 Chunking 的本质不是“切字符串”，而是：

> **把文档转换成既能被检索，又能保留足够语义上下文的 Retrieval Unit。**

---

## 2. Chunking 同时影响四件事

### Recall

Chunk 太大：Query 的局部语义可能被大块文本稀释。

Chunk 太小：关键答案可能被切散，单个 Chunk 不足以匹配完整问题。

### Precision

Chunk 越大，命中后携带的无关内容通常越多。

### Context Noise

检索出的内容最终要进入 LLM。Chunk 粒度过粗会把大量无关信息带进 Context。

### Storage / Cost

Chunk 越小，Chunk 数量越多：

```text
更多 Embedding
→ 更大 Index
→ 更多 Metadata
→ 更高 Ingestion / Storage Cost
```

---

## 3. 一个核心矛盾

RAG Chunking 一直在平衡：

```text
Retrieval Precision
        ↕
Semantic Completeness
```

太细：检索精准但语义不完整。

太粗：语义完整但检索与 Context 噪声变大。

这也是为什么不存在一个“万能 Chunk Size”。

---

## 4. Chunk 不等于最终 Context

Production RAG 常把“检索粒度”和“送给 LLM 的上下文粒度”拆开。

例如：

```text
小 Chunk 做检索
        ↓
命中 child chunk
        ↓
回取 parent section / neighbor window
        ↓
送给 LLM
```

这就是 Parent-child / Context Expansion 的思想。

---

## 5. Chunking 需要保留结构

一个好的 Chunk 至少应知道：

```text
document_id
version
section_path
chunk_id
position
parent_id
page / heading
source_url
```

否则后面很难做：

- Citation；
- Neighbor Expansion；
- 权限过滤；
- 版本删除；
- Bad Case Replay。

---

## 6. AI 应用中的典型 Failure

### Failure A：按固定字符数切法律条款

条件和结论被拆到不同 Chunk，导致检索只召回一半逻辑。

### Failure B：整个 FAQ 页面一个 Chunk

用户问一个具体问题，但 Chunk 包含几十个 FAQ，Embedding 表征被稀释。

### Failure C：忽略标题路径

正文“支持 30 天退货”被命中，但不知道它属于哪个产品或地区章节。

---

## 7. Chunking 不是一次性配置

应该把它当成可实验参数：

```text
Chunk Strategy
+ Size
+ Overlap
+ Parent Window
+ Metadata
        ↓
Evaluation Dataset
        ↓
Recall / Precision / Answer Quality
```

---

## 8. 🎯 面试怎么回答

> Chunking 是 RAG 的核心，因为它定义了 Retrieval Unit，直接影响 Recall、Precision、Context Noise 和存储成本。Chunk 过大会稀释局部语义并增加噪声，过小会切断上下文。Production 中通常还会把检索粒度和最终 Context 粒度分离，比如小块检索、Parent-child 回取。Chunk Strategy 和参数应该通过真实 Evaluation Dataset 验证，而不是照抄默认值。

## 9. ⚠️ 面试易错点

- “Chunk 越小越精准”——可能破坏语义完整性。
- “Overlap 越大越安全”——会制造重复索引与 Context 冗余。
- “Chunking 只是预处理”——它直接决定 Retrieval 的基本单位。

## 10. 🔍 继续追问

- 如何判断应该按段落还是按语义切？
- Chunk Size 应按字符、Token 还是结构决定？
- Parent-child 为什么能缓解粒度矛盾？

<details><summary>查看参考答案：为什么 Chunking 必须和 Evaluation 联动？</summary>

因为 Chunking 没有脱离数据和 Query 分布的绝对最优配置。只有在代表真实业务的问题集上比较 Retrieval 与 End-to-end 指标，才能判断某个粒度是否真正改善系统。

</details>
