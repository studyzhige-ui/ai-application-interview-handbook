# 29｜Baseline、Ablation、A-B 与 Regression

## 1. 先讲人话

RAG 很容易陷入这种“优化”：

> 换了 Chunk、Embedding、Hybrid、Rerank、Prompt，一起上线，然后觉得答案好像更好了。

这不是可靠实验，因为你不知道到底哪一步带来了收益，也不知道哪一步其实在退化。

Production RAG 必须建立：

```text
Baseline
→ One Change at a Time
→ Offline Evaluation
→ Ablation
→ Online A/B
→ Regression Gate
```

---

## 2. Baseline

Baseline 要尽量简单、稳定、可复现。

例如：

```text
Recursive Chunk
+ Dense Retrieval
+ Fixed Top-K
+ No Rerank
+ Stable Prompt
```

它不需要最强，但要成为所有后续改动的参照。

---

## 3. Ablation

Ablation 的思想是：

> 把某个组件拿掉，看看收益是否真的来自它。

例如比较：

```text
Dense
Dense + BM25
Dense + BM25 + RRF
Dense + BM25 + RRF + Rerank
```

这样才能回答：

- Hybrid 带来多少 Recall？
- Rerank 带来多少 Precision？
- 增加的 Latency 值不值得？

---

## 4. 单变量实验

如果你想验证 Chunk Size：

```text
只改 Chunk Size
其他 Embedding / Query / Rerank / Prompt 固定
```

否则实验结论不可解释。

---

## 5. Offline Regression

每次变更都跑固定 Dataset：

```text
Old Pipeline
vs New Pipeline
```

不仅看平均值，还要检查：

- 哪些 Case 从错变对；
- 哪些 Case 从对变错；
- 哪个 Query Slice 退化。

这比只看 +2% 总分更有价值。

---

## 6. Online A/B

当 Offline 通过后，再在真实流量中比较：

- 用户反馈；
- Reformulation；
- Escalation；
- Latency；
- Cost；
- Refusal；
- Citation Usage。

对于高风险场景，还需要灰度和快速 Rollback。

---

## 7. Regression Gate

可以定义上线门槛：

```text
Recall 不下降超过 X
Faithfulness 不下降
Critical Slice 0 regression
P95 Latency < SLO
Cost / Query < Budget
```

不是所有指标都要求提升，但关键指标不能不可控退化。

---

## 8. Experiment Metadata

每次实验至少记录：

```text
corpus_version
parser/chunker_version
embedding_version
index_version
retrieval_config
reranker_version
prompt_version
model_version
dataset_version
```

否则几周后很难重现结果。

---

## 9. 🎯 面试怎么回答

> RAG 优化要先有稳定 Baseline，然后通过单变量实验和 Ablation 判断 Chunk、Hybrid、Rerank 等组件各自的真实贡献。Offline 用固定 Dataset 做 Regression，并关注 Case-level 和 Slice-level 退化；通过后再做 Online A/B。所有 Corpus、Index、Model、Prompt、Dataset 版本都要记录，才能复现和 Rollback。

## 10. ⚠️ 易错点

- 一次同时改五个组件；
- 只看平均分，不看关键 Slice；
- 没有 Baseline；
- 实验结果无法复现版本配置。

<details><summary>查看参考答案：为什么 Ablation 比“新系统分数更高”更有价值？</summary>

因为 Ablation 能隔离组件贡献，告诉你复杂度和成本到底换来了什么。如果不做拆分，无法知道收益来自 Hybrid、Rerank 还是 Prompt，也无法在成本压力下决定该保留哪些组件。

</details>
