# 28. End-to-End Evaluation：Baseline、Ablation、Regression 与 Bad Case Attribution

上一章建立了 Eval Dataset 和指标，这一章回答更重要的问题：

> **一次 RAG 改动到底有没有让完整系统变好？如果变差，到底坏在哪一层？**

因此 End-to-end Eval、Experiment、Regression 和 Bad Case Attribution 应该放在一个完整质量工程闭环中。

---

## 1. 为什么 Retrieval 指标好不等于最终答案好

可能出现：

```text
Recall ↑
但 Context 变长 / 噪声 ↑
→ Answer Quality ↓
```

也可能：

```text
Rerank NDCG ↑
但正确 Evidence 被 Context Builder 截掉
→ Answer Wrong
```

所以必须同时看：

```text
Retrieval Layer
+
Generation Layer
+
System Cost / Latency
```

---

## 2. End-to-end Eval 看什么

可以包含：

```text
Answer Correctness
Faithfulness / Groundedness
Completeness
Citation Correctness
Refusal Correctness
Latency
Token / Model Cost
```

高风险场景还要有：

- Permission leakage；
- stale answer；
- unsafe answer；
- unsupported claim。

---

## 3. Baseline 为什么重要

没有 Baseline，你只知道：

```text
new score = 0.82
```

不知道：

```text
old score = 0.81 or 0.60?
```

每次实验都要明确：

```text
Baseline Configuration
vs
Candidate Configuration
```

并固定其它变量。

---

## 4. Ablation 是什么

假设新系统同时加入：

```text
Query Rewrite
Hybrid
Reranker
Parent-child
```

最终指标提高，但你不知道是谁贡献的。

Ablation 做：

```text
Baseline
+ Rewrite only
+ Hybrid only
+ Reranker only
+ Hybrid + Reranker
...
```

这样能看到单个组件的增益与交互。

---

## 5. 为什么一次只改一个变量

如果：

```text
Chunk Size changed
Embedding changed
TopK changed
Reranker changed
```

同时上线，Bad Case 时无法 Attribution。

除非是完整方案 A/B，否则迭代尽量：

```text
one controlled change
→ eval
→ decide
```

这就是 Retrieval Engineering，而不是调参玄学。

---

## 6. Regression Set

每次重要线上错误都应该变成：

```text
query
expected evidence / behavior
root cause label
```

加入 Regression Set。

后续任何模型/Chunk/Index/Prompt 更新都重新测试。

目标：

> **系统犯过的重要错误不轻易再犯。**

---

## 7. Bad Case Attribution 的第一原则

不要从“最终答案错”直接跳到某个组件。

按链路逐层问：

```text
Source has answer?
↓
Parser preserved it?
↓
Chunk contains coherent evidence?
↓
Retriever recalled it?
↓
Fusion/Reranker kept it?
↓
Context Builder included it?
↓
Model followed evidence?
↓
Citation correct?
```

第一处失败点通常就是主要 Root Cause。

---

## 8. 一张标准 Attribution 表

| Layer | Check | Typical Fix |
|---|---|---|
| Corpus | Source 是否存在答案 | Source Coverage / Freshness |
| Parse | Ground Truth 是否保留 | Parser/OCR/Layout |
| Chunk | Evidence 是否被切断 | Chunk Strategy / Parent-child |
| Query | Rewrite 是否漂移 | Rewrite / Clarification |
| Retrieval | Relevant ID 是否进入 TopN | Dense/Sparse/Hybrid |
| Rerank | 是否被错误降权 | Model/Truncation/Candidate |
| Context | 是否真正进入 Prompt | Budget/Dedup/Coverage |
| Generation | 是否误读 Evidence | Prompt/Model/Verification |
| Citation | Source 是否支持 Claim | Mapping/Verifier |

这个表应该成为日常 RAG Debug SOP。

---

## 9. Retrieval Bad Case 怎样进一步拆

### Exact 也找不到

更像：

```text
Embedding / Chunk / Query / Metric
```

### Exact 找到、ANN 找不到

更像：

```text
Vector Index / ANN Parameter
```

### No-filter 找到、Filter 后找不到

更像：

```text
Permission / Version / Metadata Filter
```

### Retriever 找到、Reranker 掉了

更像：

```text
Reranker Domain / Truncation / Score
```

这种分层能避免盲目调一个参数。

---

## 10. Generation Bad Case 怎样拆

如果正确 Evidence 已在 Prompt：

检查：

- Prompt 是否要求 Grounding；
- Evidence 是否冲突；
- Context 是否太长；
- 关键证据位置；
- Model Capability；
- Query 是否多义；
- Answer Format / Tool；
- 是否需要 Verification。

这时继续调 Retriever 可能没有意义。

---

## 11. No-answer Case 必须单独测

很多系统只评：

```text
知识库里有答案的 Query
```

于是模型学会“永远回答”。

还需要：

```text
unanswerable
out-of-domain
permission denied
stale/conflicting source
```

评估：

```text
Refusal Precision
Refusal Recall
Unsupported Answer Rate
```

---

## 12. A/B 与 Offline Eval 的关系

Offline Eval：

- 快；
- 可重复；
- 适合大量实验。

Online A/B：

- 反映真实流量；
- 能看到任务成功和用户行为；
- 风险更高、噪声更多。

合理流程：

```text
Offline Gate
→ Shadow / Canary
→ A/B
→ Production Monitor
```

不是直接把未经验证的检索配置全量上线。

---

## 13. 需要同时看成本

方案 A：

```text
quality +1%
latency +200%
cost +300%
```

不一定值得。

实验报告最好同时包含：

```text
Quality Delta
P95 / P99 Delta
Token Delta
Model Cost
Index Cost
Failure Slice
```

最终选择 Pareto 更合理的方案。

---

## 14. Version Lock

复现一次 Eval 需要记录：

```text
corpus snapshot
parser/chunker version
embedding/index version
retrieval config
reranker version
prompt/model version
judge version
```

否则两次跑分差异可能根本不是你以为的那个变量。

---

## 15. Bad Case Taxonomy

建议给 Case 打标签：

```text
SOURCE_MISSING
PARSE_ERROR
CHUNK_BOUNDARY
QUERY_DRIFT
RETRIEVAL_MISS
FILTER_ERROR
RERANK_ERROR
CONTEXT_DROP
MODEL_UNGROUNDED
CITATION_ERROR
STALE_DATA
PERMISSION_ERROR
```

长期统计各类比例，才能知道团队应该优先优化哪一层。

---

## 16. Evaluation Flywheel

```text
Production Trace
→ Bad Case
→ Human / Judge Review
→ Root Cause
→ Add Regression Case
→ Improve Component
→ Offline Eval
→ Deploy
→ More Production Evidence
```

这是成熟 RAG 最重要的持续迭代机制之一。

---

## 17. 常见错误

- Retrieval 指标提升就宣布 RAG 提升：不完整。
- 四个组件一起改然后比较总分：很难 Attribution。
- 只测 Answerable Query：会导致过度回答。
- Bad Case 直接换 Embedding：没有分层证据。
- Regression 只看总体平均：要看 Slice 和 Critical Case。
- Eval 不记录版本：无法复现。

---

## 18. 面试怎么答

### Q：RAG 怎么证明优化有效？

> 先固定 Evaluation Dataset 和版本化 Baseline，分层看 Retrieval Metrics 与最终 correctness/faithfulness/citation，同时记录 latency/cost。组件优化用 Ablation 隔离变量，通过 Offline Regression 后再 Canary/A-B。线上 Bad Case 按 Source→Parse→Chunk→Query→Retrieval→Rerank→Context→Generation→Citation 找第一失败层，并回流 Regression Set。

### Q：RAG 召回不准怎么定位？

> 先确认 Source/Parser/Chunk 是否存在 Ground Truth，再比较 Exact vs ANN、有无 Filter、Retriever vs Reranker 的结果，逐层排除 Embedding、Index、Filter、Rerank，而不是先盲调 TopK 或 efSearch。

---

## 19. 自测

<details><summary>1. 为什么 Ablation 比“新版整体更好”更有价值？</summary>
因为它能定位每个组件的独立贡献和交互，避免不知道提升来自哪里。
</details>

<details><summary>2. Bad Case Attribution 的第一步是什么？</summary>
确认权威 Source 中是否本来就存在正确答案；没有的话后续 Retrieval 不可能修复。
</details>

<details><summary>3. 为什么 No-answer Query 必须加入 Regression？</summary>
否则系统可能在有答案 Case 上表现很好，却在无证据时持续 Hallucinate。
</details>
