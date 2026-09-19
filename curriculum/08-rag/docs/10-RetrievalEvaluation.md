# 10｜Retrieval Evaluation：Metrics、Ground Truth、Dataset 与 LLM Judge

没有 Evaluation 的 RAG 优化，本质是：

```text
“我改了参数，感觉几个 Demo 更好了。”
```

这一章先建立 Evaluation 的基础设施：

```text
Evaluation Dataset
→ Ground Truth / Relevance Labels
→ Retrieval Metrics
→ Judge / Human Review
```

下一章再进入 End-to-end Experiment / Regression / Bad Case。

---

## 1. 先区分 Retrieval Eval 和 Answer Eval

### Retrieval Eval

问：

```text
正确 Evidence 有没有被找到？
排名是否足够靠前？
```

### Generation Eval

问：

```text
最终答案是否正确、Grounded、完整？
```

两者必须分开，否则最终 Answer 错时不知道是哪一层失败。

---

## 2. Evaluation Dataset 至少包含什么

最基本：

```text
query
relevant_document / chunk IDs
```

更成熟还可以包含：

```text
answerable / unanswerable
expected answer facts
query type
source version
permission scope
difficulty
domain slice
```

如果只保存自然语言“参考答案”，很难直接评 Retrieval。

---

## 3. Ground Truth 从哪里来

可以来自：

- 人工标注；
- 历史客服/搜索日志人工清洗；
- 文档作者提供 QA；
- Production 点击/成功行为（谨慎）；
- Synthetic Query + 人工/模型验证；
- Bad Case 回流。

不同来源可信度不同，应该记录 Dataset Provenance。

---

## 4. Synthetic Data 为什么有用又危险

可以从文档自动生成 Query：

```text
Document
→ LLM generates questions
→ expected source = document
```

优点：快速扩大覆盖。

风险：

- Query 风格不像真实用户；
- 问题可能过于容易；
- LLM 生成错误；
- Source 泄漏到 Query；
- Dataset 偏向生成模型习惯。

所以 Synthetic 更适合补 Coverage，而不能完全替代真实 Query。

---

## 5. Recall@K

如果 Query 有相关文档集合 `R`，Top-K 返回 `T_K`：

```text
Recall@K = |R ∩ T_K| / |R|
```

直觉：

> 应该找的 Evidence，有多少进入前 K。

对于“至少找到一条就够”的任务，也常看 Hit Rate / Success@K。

---

## 6. Precision@K

```text
Precision@K = relevant retrieved / K
```

问的是：

> 返回的前 K 里有多少是真的相关。

第一阶段 Retriever 常更偏 Recall；最终 Context 更关心 Precision / Evidence Density。

---

## 7. MRR

MRR = Mean Reciprocal Rank。

对每个 Query 找第一条相关结果的位置：

```text
rank = 1 → 1.0
rank = 2 → 0.5
rank = 5 → 0.2
```

再取平均。

它适合：

> 只要第一条正确结果越靠前越好的任务。

---

## 8. NDCG

当相关性不只是二元：

```text
highly relevant
partially relevant
irrelevant
```

NDCG 可以同时考虑：

- Relevance Grade；
- Ranking Position。

它更适合多级相关性的检索场景。

应用工程面试需要理解意义，不必手算完整公式。

---

## 9. Metric 必须和任务对齐

例如：

### QA

只要正确证据进入 Top20，后面有 Reranker，第一阶段可以更看 Recall@20。

### Search UI

用户只看前 3 条，可能更看 NDCG@3 / MRR。

### Multi-hop

需要多个 Evidence 都出现，单一 Hit Rate 不够。

所以没有“RAG 最重要指标固定是 Recall@5”这种答案。

---

## 10. Query Slice 比总体平均更重要

Dataset 应分：

```text
Exact term
Semantic paraphrase
Multi-hop
Table
Long document
Freshness
Permission
No-answer
Multilingual
Hard negative
```

总体 Recall 提升，可能只是简单 Query 变多，而真正困难 Slice 退化。

所以 Regression 要按 Slice 看。

---

## 11. Ground Truth 粒度问题

同一个答案可能存在：

```text
Document-level Ground Truth
Chunk-level Ground Truth
Passage-level Ground Truth
```

如果 Chunking 改变，旧 `chunk_id` Ground Truth 可能失效。

因此可以同时保留：

```text
document_id
source span / page
semantic answer fact
```

让 Dataset 更耐迁移。

---

## 12. Label 不是绝对客观

“相关”可能有主观性。

可以采用：

- 多人标注；
- Label Guideline；
- Disagreement Review；
- graded relevance；
- hard negative 标注。

尤其法律/企业政策中，“相关但过期”的文档不能简单标成正例。

---

## 13. LLM Judge 能做什么

LLM Judge 可以辅助：

- Query-Document Relevance；
- Answer Correctness；
- Faithfulness；
- Citation Support；
- Completeness；
- Pairwise Preference。

优点：

```text
便宜地扩大自动评估覆盖
```

但它不是 Ground Truth 本身。

---

## 14. LLM Judge 的风险

包括：

- Position Bias；
- Verbosity Bias；
- Self-preference；
- Prompt Sensitivity；
- Domain Knowledge Limitation；
- Judge Model Version Drift。

所以需要：

```text
human-labeled calibration set
```

比较 Judge 和人工判断的一致性。

---

## 15. Judge Prompt 也要版本化

记录：

```text
judge_model
judge_prompt_version
temperature / config
rubric
```

否则 Eval 分数变化可能只是 Judge 自己变了。

---

## 16. Online Signal 和 Offline Eval

Offline Dataset 优点：

- 可重复；
- 快速 Regression；
- 容易做 Ablation。

Online Signal 可以反映真实用户：

- click / copy；
- thumbs up/down；
- reformulation；
- task success；
- escalation。

但 Online Signal 有强烈行为偏差，不能直接当真值。

最好形成：

```text
Offline Eval
+
Online Telemetry
+
Human Review
```

闭环。

---

## 17. Eval Dataset 应持续增长

最有价值的 Dataset 往往来自 Production Failure：

```text
Bad Case
→ root cause
→ label
→ add to regression set
```

这样系统每犯一次重要错误，都变成未来不会轻易再犯的测试。

这就是 Data Flywheel。

---

## 18. 常见错误

- 只看 Recall，不看 Ranking/Final Answer：不完整。
- Synthetic QA 就是真实用户分布：错误。
- 一个总体平均分能代表所有 Query：错误。
- LLM Judge 分数就是客观真相：错误。
- Chunk 策略改了还直接用旧 Chunk ID Ground Truth：可能失效。
- Eval Dataset 一次建完永久不变：Production 应持续回流。

---

## 19. 面试怎么答

### Q：RAG 怎么评估？

> 我会先把 Retrieval 和 Generation 分层。Retrieval Dataset 至少有 Query 和 Relevant Source/Chunk，按任务看 Recall@K、Hit Rate、MRR、NDCG 等，并按 exact-term、semantic、multi-hop、permission、no-answer 等 Slice 拆分。最终 Answer 再评 correctness、faithfulness、citation。LLM Judge 可以规模化辅助，但要用人工标注集校准并版本化 Judge。

### Q：Evaluation Dataset 怎么建设？

> 组合真实 Query/Bad Case、人工标注和经过验证的 Synthetic Data，记录来源、版本和 Query Slice；Production Failure 归因后持续回流 Regression Set，让 Dataset 随系统演进增长。

---

## 20. 自测

<details><summary>1. Recall@K 和 MRR 关注点有什么不同？</summary>
Recall 关注相关 Evidence 是否进入前 K；MRR 特别关注第一条相关结果排多靠前。
</details>

<details><summary>2. 为什么 LLM Judge 需要人工 Calibration Set？</summary>
Judge 本身有偏差和版本漂移，需要用人工真值确认它与业务评判标准是否一致。
</details>

<details><summary>3. 为什么要按 Query Slice 看指标？</summary>
总体平均可能掩盖某类重要困难 Query 的退化。
</details>
