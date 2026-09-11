# 25｜Grounding、Citation 与 Reference Mapping

## 1. 先讲人话

RAG 的价值不只是“让模型看到知识”，还要让最终回答能够回答：

> **这句话到底依据了哪份真实来源？**

Grounding 关注回答是否建立在 Evidence 上；Citation 关注能否把回答中的 Claim 映射回具体 Source。

---

## 2. Grounding 的基本链路

```text
Source Document
→ Parsed Element
→ Chunk
→ Retrieved Evidence
→ Context
→ Answer Claim
→ Citation
```

如果中间任一层没有稳定 Identity，Citation 就只能做成“看起来像引用”。

---

## 3. Citation 不应只存 URL

最好至少保留：

```text
source_id
document_id
version
chunk_id
section / page
source_uri
```

这样用户点击引用时，能回到准确位置，而不是整个 300 页 PDF 首页。

---

## 4. Claim-level Citation

简单做法是答案末尾列几个来源；更严格的做法是让每个关键 Claim 都绑定 Evidence。

例如：

```text
退款必须在 30 天内申请。[S1]
海外订单不适用无理由退款。[S2]
```

这比统一写：

> 参考文档：A、B、C

更容易验证。

---

## 5. Citation 可能“存在但错误”

常见 Failure：

- 引用来源和 Claim 无关；
- 引用的是旧版本；
- 模型把多个 Source 的结论混在一起；
- Citation ID 和 Context 排序错位；
- 页面 / Section 定位不准。

所以需要评估：

```text
Citation Presence
Citation Correctness
Citation Completeness
```

---

## 6. Grounding 与 Hallucination

有 Citation 不代表没有 Hallucination。

模型可能：

- 引用了真实文档；
- 但结论超出了文档内容。

因此要区分：

```text
Source exists
≠ Claim supported by source
```

---

## 7. Conflict Handling

如果检索到两个版本冲突：

```text
2024：30 天
2025：14 天
```

Context Construction 应优先根据 Version / Validity 处理，而不是让模型自己猜。

必要时回答：

> “不同版本文档存在冲突，当前最新有效版本为……”

---

## 8. 🎯 面试怎么回答

> Grounding 是让模型的关键结论受 Retrieved Evidence 支持，Citation 则把 Answer Claim 映射回具体 Source。Production RAG 需要 document/chunk/version/page 等稳定 Lineage，最好做 Claim-level Citation，并验证 Citation Correctness 和 Completeness。仅仅有链接不代表答案真的 Grounded，因为模型仍可能基于来源做超范围推断。

## 9. ⚠️ 易错点

- “有 Citation 就等于无幻觉”；
- 只引用整个文档首页；
- 不区分版本；
- Source ID 在 Prompt 中重排后引用错位。

## 10. 🔍 继续追问

- Citation Correctness 怎么自动评估？
- 多个 Source 冲突怎么办？
- 如何做 Claim-level Evidence Mapping？

<details><summary>查看参考答案：为什么 Lineage 是 Citation 的前置？</summary>

因为 Citation 必须知道最终 Claim 对应的 Context 来自哪个 Chunk，而 Chunk 又要能回到特定 Document Version 和原始 Source。没有稳定血缘，只能提供模糊来源，无法可靠验证或回放。

</details>
