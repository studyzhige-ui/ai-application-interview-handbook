# Batch 13 一手面试流程

采集日期：2026-09-10

## S209 亚信安全｜大模型智能体 / AI Native 工具研发｜技术一面｜面试 2026-09-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/00254f151d484eb89f8ab6781125d05a

真人 / 第一人称证据：作者个人主页持续记录本人秋招笔试 / 面试，本帖明确岗位方向与技术一面；评论中作者后续直接更新“挂了”，招聘结果可核验。问题由 RAG Evaluation 连续追到多日 Agent Runtime、Redis / Kafka / ES 与模型预算控制，具有明显现场连续追问结构。

高价值问题：

1. RAG Evaluation Dataset 怎样构建，每个 Case 跑几次、用什么指标？
2. Agent 从用户提问到最终结果的 End-to-End Latency 大概多少，如何测量？
3. 数据中台是什么量级，真实遇到过哪些工程困难？
4. 对 Transformer、微调和小模型需要掌握到什么应用工程深度？
5. 运行数小时甚至数天的 Agent 如何保证稳定性？
6. 第三方 API 中途失败后，怎样通过 Checkpoint / Resume 避免任务从头重跑？
7. Redis / Kafka / Elasticsearch 在 Agent Backend 各自适合什么场景？
8. 如何用 Redis 同时实现“每个 Key 每分钟 N 次请求”和 Token Budget 限流？
9. 十个并发请求在实际 Token 消耗尚未确定时，怎样预留预算避免并发超卖？
10. Streaming Output 过程中预算归零时，继续生成还是截断，如何定义业务策略？

去重：URL、预算并发预留与多日任务 Resume 场景均未在现有来源出现；作者招聘时间线独立。

---

## S210 联想｜AI 应用开发｜一面｜发布 2026-04-02，20min｜HUMAN-A

来源：https://www.nowcoder.com/discuss/869169098146537472

真人 / 第一人称证据：作者本人发布联想 AI 应用开发一面，记录整场约 20 分钟、无 Coding，并在第二天更新收到感谢信；评论区还有其他同岗位候选人核验流程和技术方向。

高价值问题：

1. RAG 的 Text Chunk Strategy 怎样选择？
2. 怎样理解 AI Agent，实际了解哪些 Agent Framework？
3. RAG 怎样构建多轮对话所需 Context？
4. Prompt Engineering 有哪些真实项目经验？
5. 常见 Agent Tool 怎样设计和接入？
6. RAG Hallucination 如何发现和治理？
7. 了解哪些 Vector Database，Similarity 如何计算？
8. 最近两年的 Agent Framework 变化怎样理解？
9. Agent Skill 的职责和使用方式是什么？
10. Python Closure 在项目什么场景中使用？
11. Java 中如何降低 Memory Leak 风险？

去重：URL、20 分钟流程和题序未在 `S001–S208` 中出现；评论区能与同岗位候选人交叉核验，不属于答案型文章。

---

## S211 上海某独角兽小厂｜AI 全栈开发｜技术面｜发布 2026-08-28，已通过｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6468c9ab07664b15901a3470fad6115f

真人 / 第一人称证据：作者开头明确“面试通过了，分享一下面经”，岗位为 AI 全栈；问题围绕本人项目的 Vector Retrieval、Context、Memory、Evaluation 和 Agent Trace 连续深挖，并追到产品工程取舍，结构明显不同于分类题库。

高价值问题：

1. 如何向非专业人解释 Vector Retrieval 与 Similarity？
2. IVF 与 HNSW 两种 ANN Index 的基本原理与取舍是什么？
3. FAISS 与数据库自带 Vector Index 怎样选择，是否真正调过参数？
4. Bi-Encoder 与 Cross-Encoder 的差异和复杂度成本是什么？
5. Vector + BM25 Hybrid Retrieval 如何融合，RRF / Rerank 分别解决什么问题？
6. Recall、Precision、F1 冲突时怎样根据业务做 Trade-off？
7. Agent / RAG 的 Context Expansion 如何控制，效果怎样量化？
8. 为什么不做简单 RAG，而要做 Multi-Agent System？
9. Evaluation Dataset 怎样构建？
10. Agent Execution Trace 用什么工具记录，如何支撑 Debug / Evaluation？
11. 为了快速上线是否可以暂时牺牲代码质量，怎样划重构边界？
12. 怎样理解 Product Engineer / AI Full-stack 方向？

去重：URL、IVF/HNSW→RRF/Rerank→Trace 的连续题序未在现有来源命中；作者面试通过结果提供现场真实性信号。

---

## S212 文远知行｜AI 全栈开发｜三面｜面试 2026-08-18，进入横向｜HUMAN-A

来源：https://www.nowcoder.com/discuss/920018465497382912

真人 / 第一人称证据：作者“小妞脂”明确给出 8 月 18 日三面和 AI 全栈岗位；正文写“直接开始压力”、比较三面与前两面面试官追问深度，并在面后进入横向、评论区继续与其它候选人核验横向流程，现场与招聘状态明确。

高价值问题：

1. Coding：现场 BFS。
2. 高并发秒杀中如何保证 Redis 与 MySQL Data Consistency？
3. 用户购买后立即退款时，库存 / 订单一致性如何设计？
4. Distributed Lock / RedLock 在什么边界下使用，风险是什么？
5. PGVector 中文本最终怎样转成向量并存储？
6. Embedding 在 RAG 中具体表示什么？
7. Rerank 为什么能提升 Retrieval Quality？
8. RAG 还有哪些新的 Retrieval / Orchestration 玩法，何时值得用？
9. AI 应用岗为什么仍会追问模型训练完整流程，应该掌握到什么边界？
10. 实习项目本人到底做了什么，能否经得住三面继续深挖？

去重：同作者还存在字节 `S076`，但公司、岗位流程、日期和题序均完全独立，应视为不同候选流程的两次真人命中；文远知行 URL 未在旧 Batch 收录。

---

