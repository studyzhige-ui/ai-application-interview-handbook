# RAG Canonical Questions — S001–S279 全库纵向扫描 v1

更新日期：2026-09-10

> 本文件只描述冻结 HUMAN-A 中真实出现的 RAG 考察方式。它不是用面经反推出来的“题库课程”；后续 RAG 教材仍会从 Corpus → Parse → Chunk → Index → Retrieve → Rerank → Context → Generate → Evaluate → Operate 建立完整知识体系。

## 1. 当前扫描结论

- Canonical Questions：**30** 道
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数，同一来源的连续追问只计一次
- 当前版本：`v1`；完成 Agent Harness 后再做跨模块 Merge / Split 审计

### 高频信号

- **RAG-002** · 31 个来源 · 🔥🔥🔥：Production RAG 从 Ingestion 到最终 Answer 的完整链路是什么？
- **RAG-007** · 29 个来源 · 🔥🔥🔥：Chunk Strategy 怎样选择？Fixed / Recursive / Semantic / Parent-child / Structure-aware 如何取舍？
- **RAG-013** · 24 个来源 · 🔥🔥🔥：为什么要做 Hybrid Retrieval，多路召回怎样融合？
- **RAG-015** · 22 个来源 · 🔥🔥🔥：为什么需要 Rerank，如何平衡精度、延迟、成本并处理“Rerank 反而变差”？
- **RAG-021** · 21 个来源 · 🔥🔥🔥：RAG 质量怎样 Evaluation，Dataset、Recall / Precision、Faithfulness、Answer Quality 怎样组织？
- **RAG-019** · 18 个来源 · 🔥🔥🔥：RAG Bad Case / Hallucination 出现时，怎样区分 Parsing、Chunk、Retrieval、Rerank、Prompt、Generation 问题？
- **RAG-010** · 17 个来源 · 🔥🔥🔥：Query Rewrite / Decomposition / Multi-query / Intent / Clarification 怎样改善 Retrieval？
- **RAG-024** · 13 个来源 · 🔥🔥🔥：Knowledge Base 怎样做增量更新、版本管理、旧数据清理和在线新鲜度保障？
- **RAG-004** · 12 个来源 · 🔥🔥🔥：PDF / OCR / Layout / Markdown / HTML 等异构文档怎样可靠解析？
- **RAG-008** · 12 个来源 · 🔥🔥🔥：Chunk Size / Overlap 如何设置，参数如何通过实验验证而不是照抄默认值？
- **RAG-001** · 11 个来源 · 🔥🔥🔥：为什么需要 RAG？什么时候 Long Context、文件搜索、更强模型或 Fine-tuning 更合适？

---

## 2. Canonical Questions

### RAG-001 · 为什么需要 RAG？什么时候 Long Context、文件搜索、更强模型或 Fine-tuning 更合适？

- **Topic**：RAG Boundary
- **Question Type**：Why / Comparison
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**11**
- **Evidence Sources**：`S023`, `S031`, `S045`, `S068`, `S145`, `S218`, `S222`, `S249`, `S257`, `S267`, `S275`

**真实问法变体：**
- 为什么需要 RAG，直接把文档放进大 Context 不行吗？
- 不做 RAG、换更强模型会不会更好？
- RAG 与 Fine-tuning / Repo Search 各自适合什么场景？

### RAG-002 · Production RAG 从 Ingestion / Parse / Chunk / Embedding / Index 到 Retrieve / Rerank / Context / LLM 的完整链路是什么？

- **Topic**：End-to-end Pipeline
- **Question Type**：Concept / Project
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**31**
- **Evidence Sources**：`S006`, `S021`, `S024`, `S026`, `S029`, `S031`, `S040`, `S053`, `S063`, `S068`, `S071`, `S074`, `S081`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S163`, `S184`, `S200`, `S211`, `S217`, `S240`, `S249`, `S251`, `S262`, `S275`, `S277`

**真实问法变体：**
- 企业知识库从文档上传到最终回答经历什么？
- Offline / Online 两条链路分别是什么？
- Production RAG 怎样把每个阶段串起来？

### RAG-003 · 建 RAG 前怎样审计 Corpus：数据来源、质量、重复、版本、权限和真实规模如何影响方案？

- **Topic**：Corpus / Data Audit
- **Question Type**：Project / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S052`, `S056`, `S058`, `S217`, `S246`, `S248`, `S275`

**真实问法变体：**
- 知识库真实数据量级是多少？
- 文档来自 Crawl、业务同步还是 Upload？
- 噪声和重复片段怎样治理？

### RAG-004 · PDF / OCR / Layout / Markdown / HTML 等异构文档怎样可靠解析？电子 PDF 与扫描 PDF 如何统一处理？

- **Topic**：Parsing / OCR / Layout
- **Question Type**：System Design / Project
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**12**
- **Evidence Sources**：`S024`, `S029`, `S052`, `S058`, `S074`, `S095`, `S162`, `S184`, `S217`, `S240`, `S253`, `S275`

**真实问法变体：**
- PDF / 图片 / Markdown 怎么 Parse？
- 扫描件和电子 PDF 怎样统一进入 RAG？
- Layout-aware Parsing 为什么重要？

### RAG-005 · 表格、图片与多模态内容怎样保留结构和引用关系？Cross-page Table 被切断时如何恢复语义？

- **Topic**：Multimodal / Table Parsing
- **Question Type**：Failure Analysis / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S024`, `S052`, `S058`, `S074`, `S162`, `S217`, `S240`, `S253`, `S275`

**真实问法变体：**
- 跨页表格怎么处理？
- 同一文档两个相关表格被切开后怎样保留关系？
- Word / PDF 图文混排怎样检索并返回图文引用？

### RAG-006 · 文档切分为什么是 RAG 的核心环节？Chunk Granularity 会怎样影响 Recall、Precision、Context Noise 与 Generation？

- **Topic**：Chunking Principles
- **Question Type**：Why / Deep Dive
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**15**
- **Evidence Sources**：`S002`, `S022`, `S024`, `S026`, `S037`, `S040`, `S054`, `S058`, `S062`, `S072`, `S074`, `S217`, `S240`, `S253`, `S275`

**真实问法变体：**
- 为什么 Chunking 很关键？
- Chunk 太大 / 太小分别有什么问题？
- Chunk Boundary 怎样影响最终回答？

### RAG-007 · Chunk Strategy 怎样选择？Fixed、Recursive、Semantic、Parent-child、Structure-aware 等策略各自适合什么数据？

- **Topic**：Chunk Strategy
- **Question Type**：Comparison / Project
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**29**
- **Evidence Sources**：`S002`, `S018`, `S021`, `S022`, `S024`, `S026`, `S029`, `S031`, `S037`, `S040`, `S054`, `S055`, `S058`, `S064`, `S068`, `S072`, `S074`, `S081`, `S084`, `S095`, `S101`, `S109`, `S162`, `S184`, `S217`, `S240`, `S249`, `S253`, `S275`

**真实问法变体：**
- 长文档怎样 Chunk？
- Parent-child Index 为什么需要？
- Markdown 没有标题时怎么切？
- 为什么按段落 / 多级标题切？

### RAG-008 · Chunk Size / Overlap 如何设置？参数应怎样通过 Dataset / Experiment 验证，而不是照抄 512 或默认值？

- **Topic**：Chunk Parameters
- **Question Type**：Trade-off / Evaluation
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**12**
- **Evidence Sources**：`S002`, `S022`, `S054`, `S062`, `S065`, `S072`, `S074`, `S109`, `S217`, `S240`, `S253`, `S275`

**真实问法变体：**
- Chunk Size 为什么是 200–500 / 512？
- Overlap 为什么这样设？
- 参数怎么用实验验证？

### RAG-009 · Chunk 把强逻辑关系、充分必要条件或跨块上下文切断时，怎样通过 Overlap、Parent-child、Neighbor Expansion、Semantic Boundary 修复？

- **Topic**：Semantic Boundary Failure
- **Question Type**：Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S024`, `S058`, `S162`, `S218`, `S240`, `S253`

**真实问法变体：**
- “A 是 B 的充分必要条件”恰好被切开怎么办？
- 跨页 / 跨块关联怎样恢复？

### RAG-010 · Query Rewrite / Decomposition / Multi-query / Intent / Clarification 怎样改善 Retrieval？什么时候应该先向用户追问？

- **Topic**：Query Transformation
- **Question Type**：System Design / Comparison
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**17**
- **Evidence Sources**：`S008`, `S024`, `S040`, `S055`, `S056`, `S057`, `S066`, `S072`, `S081`, `S095`, `S101`, `S132`, `S148`, `S150`, `S240`, `S249`, `S250`

**真实问法变体：**
- Query Rewrite 解决什么问题？
- Multi-dimensional Rewrite / Query Decomposition 怎么做？
- 信息不完整时应检索还是先 Clarify？

### RAG-011 · Retrieval Miss / No-hit 如何定义？阈值怎样设置，何时拒答、澄清或走 Fallback？

- **Topic**：No-hit / Refusal
- **Question Type**：Failure Analysis / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S052`, `S055`, `S067`, `S081`, `S109`, `S240`

**真实问法变体：**
- “没有检索到知识”怎么判断？
- Evidence 不足时为什么不能硬生成？
- Threshold 怎么定？

### RAG-012 · Dense Retrieval 与 Keyword / BM25 Sparse Retrieval 各自擅长什么？为什么专有名词、短 Query、精确条款容易暴露纯向量短板？

- **Topic**：Dense vs Sparse
- **Question Type**：Comparison / Failure Analysis
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**15**
- **Evidence Sources**：`S018`, `S031`, `S034`, `S037`, `S066`, `S072`, `S081`, `S095`, `S150`, `S184`, `S200`, `S217`, `S218`, `S251`, `S275`

**真实问法变体：**
- 为什么纯 Vector 对专有名词不稳定？
- BM25 与 Vector Retrieval 分别解决什么？

### RAG-013 · 为什么要做 Hybrid Retrieval？Dense / Sparse / Multi-way Retrieval 的结果怎样融合并验证收益？

- **Topic**：Hybrid Retrieval
- **Question Type**：Why / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**24**
- **Evidence Sources**：`S018`, `S031`, `S034`, `S037`, `S040`, `S058`, `S066`, `S072`, `S081`, `S084`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S184`, `S200`, `S211`, `S217`, `S218`, `S240`, `S251`

**真实问法变体：**
- Keyword + Vector 怎么融合？
- Multi-way Retrieval 比单路 Recall 提升多少，怎么证明？

### RAG-014 · RRF / Fusion 为什么常用于多路召回？为什么不简单线性加权，融合参数怎样调？

- **Topic**：Fusion / RRF
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S072`, `S087`, `S095`, `S132`, `S163`, `S211`, `S224`, `S240`, `S249`, `S251`

**真实问法变体：**
- 为什么 RRF 而不是加权求和？
- RRF `k` 怎样调？

### RAG-015 · 为什么需要 Rerank？如何平衡 Precision、Latency、Cost，并定位“Rerank 加上去反而变差”？

- **Topic**：Reranking
- **Question Type**：Why / Troubleshoot / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**22**
- **Evidence Sources**：`S021`, `S037`, `S054`, `S069`, `S081`, `S084`, `S087`, `S095`, `S101`, `S109`, `S132`, `S148`, `S150`, `S163`, `S184`, `S211`, `S212`, `S223`, `S240`, `S249`, `S258`, `S277`

**真实问法变体：**
- 为什么召回后还要 Rerank？
- Rerank Top20→Top5 为什么这样设？
- Rerank 负收益怎么定位？

### RAG-016 · Retrieval / Rerank Top-K 怎样设置？K 在 Recall、Context Noise、Latency 与 Token Cost 之间如何取舍？

- **Topic**：Top-K
- **Question Type**：Trade-off / Evaluation
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S021`, `S069`, `S081`, `S084`, `S095`, `S101`, `S109`, `S184`, `S240`

### RAG-017 · Retrieval Evidence 怎样组装进 LLM Context？标题、Metadata、邻居块、来源信息与顺序怎样影响回答？

- **Topic**：Context Construction
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S024`, `S066`, `S095`, `S168`, `S218`, `S240`, `S275`

**真实问法变体：**
- 为什么 Chunk 要带多级标题？
- Retrieval Evidence 放进 Context 时怎样减少 Lost-in-the-middle / Noise？

### RAG-018 · 最终回答怎样做 Grounding / Citation / Reference Mapping，保证结论能回到真实证据？

- **Topic**：Grounding / Citation
- **Question Type**：System Design / Verification
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S052`, `S240`, `S275`

**真实问法变体：**
- 最终结论怎么映射回 Reference？
- 图文 / 表格证据怎样被正确引用？

### RAG-019 · RAG Bad Case / Hallucination 出现时，怎样区分 Parsing、Chunk、Embedding、Retrieval、Rerank、Prompt、Generation、Runtime 的问题？

- **Topic**：Bad Case Attribution
- **Question Type**：Troubleshoot
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**18**
- **Evidence Sources**：`S010`, `S022`, `S037`, `S041`, `S045`, `S052`, `S055`, `S058`, `S061`, `S067`, `S081`, `S095`, `S109`, `S150`, `S218`, `S240`, `S249`, `S255`

**真实问法变体：**
- RAG 不准时从哪里开始排查？
- 怎么发现是 Recall 不准导致模型幻觉？
- Answer Bad Case 怎样分层归因？

### RAG-020 · 怎样定义 Retrieval Quality：Recall、Precision、Hit Rate、MRR / NDCG 等指标分别回答什么问题？

- **Topic**：Retrieval Metrics
- **Question Type**：Concept / Evaluation
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**15**
- **Evidence Sources**：`S021`, `S022`, `S037`, `S052`, `S055`, `S058`, `S065`, `S095`, `S101`, `S109`, `S132`, `S184`, `S211`, `S240`, `S248`

### RAG-021 · RAG 质量怎样做 End-to-end Evaluation？Retrieval、Faithfulness、Answer Relevance / Correctness 应怎样分层？

- **Topic**：RAG Evaluation
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**21**
- **Evidence Sources**：`S021`, `S022`, `S031`, `S037`, `S041`, `S052`, `S055`, `S057`, `S058`, `S061`, `S074`, `S095`, `S101`, `S109`, `S148`, `S184`, `S211`, `S218`, `S240`, `S253`, `S277`

**真实问法变体：**
- RAGAS 怎样评测？
- Knowledge Base Precision / Recall 怎么测？
- 如何判断改动真的让 RAG 变好？

### RAG-022 · Evaluation Dataset / Ground Truth 从哪里来？怎样保证样本代表线上真实 Query，并避免 LLM Judge 自己不可靠？

- **Topic**：Evaluation Dataset / Judge
- **Question Type**：Evaluation / Failure Analysis
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S052`, `S057`, `S058`, `S061`, `S095`, `S218`, `S240`, `S246`, `S253`

**真实问法变体：**
- Evaluation Set 谁构建，规模多大？
- LLM Judge 的一致性怎么验证？
- Offline Case 与线上真实问题如何对齐？

### RAG-023 · 怎样用 Baseline / Ablation / A-B Experiment 证明 Chunk、Hybrid、Rerank、GraphRAG 等优化的真实收益？

- **Topic**：Experiment Design
- **Question Type**：Evaluation / Project Verification
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S055`, `S057`, `S058`, `S072`, `S218`, `S240`, `S246`, `S257`

**真实问法变体：**
- 为什么说 Recall 提升了 30%？
- Hybrid 相比纯 Vector 的收益怎么证明？
- GraphRAG 的 Baseline 和 Metric 是什么？

### RAG-024 · Knowledge Base 怎样做增量更新、版本管理、旧数据清理和在线新鲜度保障？

- **Topic**：Incremental Update / Freshness
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**13**
- **Evidence Sources**：`S055`, `S068`, `S095`, `S101`, `S109`, `S127`, `S140`, `S170`, `S217`, `S240`, `S246`, `S275`, `S277`

**真实问法变体：**
- 单篇文档更新时哪些实体 / Chunk / Index 局部更新？
- Knowledge Base 如何不停服更新？
- 旧版本向量怎样清理？

### RAG-025 · 企业 RAG 怎样做 Permission / Tenant Filtering，防止检索到用户无权读取的知识？

- **Topic**：Permission / Security
- **Question Type**：Security / System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S059`, `S254`, `S275`

**真实问法变体：**
- 员工对 Knowledge Base 的访问权限怎么管？
- 过期且危险的运维指令被召回后怎样阻止执行？

### RAG-026 · 百 GB / TB 级语料怎样做 Ingestion、Embedding、Index Build、并行处理与成本控制？

- **Topic**：Large-scale RAG
- **Question Type**：System Design / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S056`, `S217`, `S240`, `S277`

**真实问法变体：**
- 600GB–1TB 金融 PDF 怎样从零建设 RAG？
- 全量 Embedding 的计算 / 存储成本怎样优化？
- 百万 / 千万商品 Knowledge Base QA 怎样设计？

### RAG-027 · RAG Latency / Cost 的主要瓶颈在哪里？Parse、Embedding、Retrieve、Rerank、LLM、Cache 各层怎样优化？

- **Topic**：Latency / Cost
- **Question Type**：Troubleshoot / Trade-off
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S021`, `S029`, `S045`, `S109`, `S217`, `S223`, `S257`

**真实问法变体：**
- Vector Retrieval 单次耗时多少？
- 当前 RAG 最大 Bottleneck 是什么？
- 怎样在更强模型、RAG、Cache 间做成本对照？

### RAG-028 · GraphRAG / Knowledge Graph Retrieval 相比普通 Vector RAG 解决什么问题？Triple / Community / Graph Update 怎样保证质量？

- **Topic**：GraphRAG
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S037`, `S058`, `S072`, `S211`, `S246`, `S267`, `S272`, `S277`

**真实问法变体：**
- GraphRAG 与普通 RAG 的核心差异是什么？
- Triple Extraction 错了怎么办？
- 哪些 Query 真正需要 Graph DB？

### RAG-029 · Agentic RAG 与固定 One-shot RAG 有什么区别？什么时候应该让 Agent 主动决定检索、重写、继续检索或停止？

- **Topic**：Agentic RAG
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S045`, `S081`, `S109`, `S150`, `S222`, `S277`

**真实问法变体：**
- Agentic RAG 与普通 RAG 有什么区别？
- 哪些场景固定 RAG 反而更合适？

### RAG-030 · Code RAG / Repository QA 与 AST、LSP、ripgrep、Filesystem Search 等 Tool-based Search 怎样分工？

- **Topic**：Code RAG Boundary
- **Question Type**：Comparison / System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S038`, `S059`, `S132`, `S145`, `S218`

**真实问法变体：**
- Coding Agent 为什么不一定依赖 Vector Code RAG？
- 大 Context 已经很强，为什么还需要 RAG / 索引？

---

## 3. 真人面经中的典型 RAG 追问链

### 3.1 最常见的“从 Demo 追到工程”链

```text
完整 RAG Pipeline
→ 文档怎么 Parse
→ Chunk 为什么这样切
→ Chunk Size / Overlap 为什么这样设
→ Embedding / Index 为什么这样选
→ 为什么 Hybrid
→ RRF / Rerank
→ Top-K
→ 指标怎么测
→ Bad Case 怎么归因
→ 增量更新怎么办
```

### 3.2 “你这个优化真的有效吗？”链

```text
声称 Recall / Accuracy 提升
→ Baseline 是什么
→ Dataset 从哪里来
→ Metric 是什么
→ 单模块还是 E2E
→ Ablation 做了吗
→ LLM Judge 可信吗
→ Failure Case 是什么
→ 线上是否仍成立
```

### 3.3 “RAG 不是万能解”链

```text
为什么 RAG
→ Long Context 不行吗
→ 更强 Model 不行吗
→ Fine-tuning 呢
→ Tool-based File / Repo Search 呢
→ GraphRAG 什么时候值得
→ Agentic RAG 什么时候值得
```

---

## 4. 对后续 RAG 教材的校准建议

1. 正式课程必须从 **Corpus Audit / Parsing** 开始，不能把 RAG 简化成 `split → embed → vector search`；
2. Chunking 应拆成 Principles、Strategy、Parameters、Semantic Boundary Failure 四层；
3. Retrieval 主线按 `Dense → Sparse / BM25 → Hybrid → Fusion / RRF → Rerank → Top-K` 连续讲；
4. Evaluation 必须与 Implementation 同级，至少拆 Retrieval、Generation、E2E、Dataset / Judge、Experiment Design；
5. Production 章节必须包含 Incremental Update、Version / Freshness、Permission、Large-scale Ingestion、Latency / Cost；
6. Bad Case 应建立明确的分层 Troubleshooting Tree，让学生能回答“召回不准怎么定位”而不只列优化方法；
7. GraphRAG、Agentic RAG、Code RAG 应作为边界 / 进阶能力，不应遮住标准 RAG 主干；
8. 面经没有直接高频覆盖的 Parser 选型细节、Embedding Batch、Index Lifecycle、Evaluation 公式等仍由知识体系补齐，不能因为统计低就删除。
