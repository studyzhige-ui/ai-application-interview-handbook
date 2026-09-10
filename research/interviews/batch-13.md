# Batch 13 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S265` 继续编号，仍只接受：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场痕迹 + AI Application / Agent 目标岗位 + 正文稳定可核验 + 非转载 / 非合集 / 非重复 = HUMAN-A**。
>
> 本轮继续做 `公司 × 岗位别名 × 月份 × 技术关键词` 精确回扫，并沿作者主页、同一招聘流程后续轮次、企业页 / 话题页和评论区补证。搜索摘要只负责发现；题目再“高级”，如果候选人、真人面试或原始正文不能稳定核验，仍然零贡献。
>
> 通过 Role Scope 后继续保留整场真实技术问题：Python / Java、Backend、MySQL、Redis、Network、Frontend、Coding、Vector DB、RAG、Agent、Harness / Runtime、Evaluation、AI Coding 与 System Design 一视同仁。
>
> 三层去重保持不变：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。本轮另外发现 `S260` 同一候选人的小红书二面，已回写原来源，不新增 `Sxxx`。

---

## S265 FOSHO｜AI 应用开发 / Agent 开发｜一面｜面试 2026-07-16，发布 07-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d95927b94e994681beee22975766721e

真人 / 第一人称证据：作者明确记录 `26.7.16`、30 分钟、一面、零八股且全程围绕本人项目追问；正文按“长视频理解 AI 问答系统 → Mini Coding Agent”自然推进，并以本人求职面经发布，不是答案型整理。

高价值问题：

1. 长视频从上传、ASR / 转写到可问答状态的完整处理链路是什么？
2. 视频转写 / 摘要属于长耗时任务时，Backend 如何异步执行和管理状态？
3. 大文件如何做 Multipart Upload 与断点续传，大小上限如何设计？
4. 用户对视频提问后，如何检索相关片段并组装 Prompt？
5. 当前系统的主要性能瓶颈是什么，下一步准备优化哪里？
6. 单视频问答如何扩展成多视频资源库与跨视频 Retrieval？
7. Mini Coding Agent 已实现哪些能力，Context Management 怎样设计？
8. 为什么不用现成 Agent Framework，而选择自己实现？
9. Coding Agent 为什么选择 Go，而不是 Python / TypeScript？

去重：URL、长视频理解项目链和 Mini Coding Agent 题序均未在 `S001–S264` 正式来源中出现；未发现同作者同流程已入库场次。

---

## S266 字节跳动｜Agent 开发｜二面｜面试 2026-07-18，发布 07-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/eccea78e38b447c9a3ae73570c5d00b6

真人 / 第一人称证据：作者“找工小蜜蜂”明确给出二面日期 7 月 18 日，并写整场基本在与面试官聊天；评论继续围绕岗位、项目和后续流程核验。作者主页还能看到更早一次字节暑期 Agent 一面凉经，当前场次时间更晚且为独立流程，未与旧流程混算。

高价值问题：

1. 两个项目是不是学校项目，硕士期间实验室真实做了什么？
2. 为什么做当前 Agent 项目，项目出发点是什么？
3. Agent Framework 如何选型，除了 LangChain 还调研过什么？
4. Agent 的核心组成与运行机制怎样解释？
5. Planning 主要由 Agent Framework 还是模型承担，常见实现方式有哪些？
6. Short-term / Long-term Memory 的边界是什么？
7. Function Call 的内容是否应该写入短期记忆；如果不写会产生什么问题？
8. MCP / 自写 Tool 分别怎样实现，大模型 Tool 机制带来什么价值？
9. RAG Retrieval 实际调过哪些召回参数，如何判断调优有效？
10. Python 基础与 Coding：合并两个有序数组。

去重：当前二面与作者更早的“暑期一面凉经”属于不同时间段、不同招聘流程；URL、题序和本轮项目问法未在正式来源中命中，因此按独立招聘流程计数。

---

## S267 快手｜AI 应用开发｜留用实习一面｜发布 2026-08-26，35min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/631e9b79e433415ca3dea24642f94b4c

真人 / 第一人称证据：作者明确写公司、AI 应用开发岗位和 35 分钟时长；问题连续深挖本人智能体平台。次日作者二次编辑，记录已约二面但被告知没有转正 HC，因此主动拒绝二面，招聘时间线完整。

高价值问题：

1. 项目中真正与 AI 相关的部分是什么，另一个项目是否真的属于 Agent？
2. 智能体平台以什么产品形态存在，是否接入 IM？
3. Clarification / 反问什么时候触发，怎样实现？
4. 从用户输入到最终回答的完整问答链路是什么？
5. Intent Tree / Intent Recognition 怎样实现，准确率如何测？
6. Evaluation Set 谁构建、数量多大、怎样证明代表真实业务？
7. MCP Tool 使用时有哪些注意事项，调用失败如何处理？
8. 真实用户规模、每日会话量是多少？
9. 候选人是否真正做过模型训练 / 图像分类，项目边界在哪里？
10. Coding：反转链表；平时如何使用 AI 学习。

去重：URL 与“无转正 HC → 拒绝二面”的流程未在现有 Batch 出现；与其它快手 AI Application / Agent 样本作者和项目链不同。

---

## S268 小红书｜AI 全栈开发｜业务交叉面 + 二面（同一候选人同流程合并）｜发布 2026-06-25 / 07-01｜HUMAN-A

业务交叉面来源：https://www.nowcoder.com/feed/main/detail/45d2815e4dc54a2fa9161273f6046c97

二面来源：https://www.nowcoder.com/feed/main/detail/b0aba5ebac994002a27bf0892b8991f9

真人 / 第一人称证据：两个页面均由同一作者 `Recall_15` 发布，岗位均为小红书 AI 全栈开发；首轮约 40 分钟，作者记录面试官对业务、AI Coding 和系统上线的具体追问，二面再次约 40 分钟并写“问很细、95% 答上来、希望能过”等现场状态，因此合并为一个招聘流程来源。

高价值问题：

1. 实习里的 AI 开发到底难在哪里，哪些部分是候选人独立完成？
2. 一个功能从 Task 到 Production Release 的完整流程是什么，上线看哪些正 / 负向指标？
3. 从零做一个 AI 产品，前端、后端、部署和运维分别要承担什么？
4. 大模型流量突然上涨时，如何监控、扩容、降级和回滚？
5. AI Coding 生成的低质量代码有哪些典型问题，怎样人工兜底？
6. 给一个模糊需求，如何快速做多平台 Prototype / MVP，并定义验收时间和标准？
7. 视频编辑 Agent 的核心难点是什么，Tool Call / Memory / Prompt Orchestration 怎样组织？
8. 文本 → 编辑脚本 → 视频的完整链路怎样设计，视频质量如何 Evaluation？
9. 如何把生成 / 编辑延迟从约 30 分钟降到约 5 分钟，并证明优化有效？
10. 音视频同步、分辨率、字幕等工程问题如何保证稳定性？
11. LangGraph 在这类 Agent 中承担什么关键职责？
12. 多模态知识库怎样做可验证 Retrieval，关键帧如何选择？

去重：两条 URL 为同一作者、同公司、同岗位连续轮次，主动合并为一个 `Sxxx`；现有正式来源未出现该作者和视频编辑 Agent 项目链。

---

## S269 亚信安全｜大模型智能体 / AI Native 工具研发｜技术一面｜面试 2026-09-02｜HUMAN-A

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

## S270 联想｜AI 应用开发｜一面｜发布 2026-04-02，20min｜HUMAN-A

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

去重：URL、20 分钟流程和题序未在 `S001–S264` 中出现；评论区能与同岗位候选人交叉核验，不属于答案型文章。

---

## S271 字节跳动｜AI 应用开发｜一面 + 二面（同一候选人同流程合并）｜2026-05-12 / 05-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/61aa7e8d56ca4eb4a5a873512a72d616

真人 / 第一人称证据：作者给出完整时间线：5 月 7 日 HR 联系、5 月 12 日一面后约 20–30 分钟约二面、5 月 15 日二面后挂并被其它部门捞。二面记录面试官迟到、Coding 中途离开、自己多处回答未戳中技术价值、现场代码出现 Bug 且和面试官一起排查未果，现场痕迹非常强。

高价值问题：

1. 实习中的 Database Optimization 具体怎么做，数据量级和是否 Sharding？
2. MySQL Index 为什么快、什么时候失效、用了索引为什么仍可能很慢？
3. Slow Query 如何定位和解决，B+Tree 为什么适合数据库索引？
4. Redis 的 Sentinel、Cluster、Master-Replica 怎样提供高可用 / 高性能？
5. Redis 与 MySQL 混合使用时怎样考虑数据一致性？
6. Vibe Coding、Skill 和其它 AI Coding 范式怎样理解？
7. Coding：按头尾交替规则重排单链表，并满足 `O(n)` / `O(1)`。
8. 二面项目验真：业务流程、本人负责部分、上下游问题和真实技术价值分别是什么？
9. 简历写“数据库优化提升 20%”时，具体怎样测；为什么真的提升？
10. Back-to-table Query 为什么涉及 Sequential IO / Random IO，当前场景怎样优化？
11. Coding：实现有最大容量的 Blocking Queue；现场出现 Bug 时如何 Debug？
12. 平时怎样使用 AI，为什么想做 AI Assistant，AI 提效的真实预期是什么？

去重：检索到另一个入口 URL 指向同一正文，按同场只保留当前稳定原帖；该候选人的 5/12–5/15 流程未在正式来源中出现。

---

## S272 平安健康保险｜AI 应用开发｜秋招一面｜面试 2026-08-23，08-26 感谢信｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6c11a75a8bd44628943deff3e42ae15c

真人 / 第一人称证据：作者明确记录 8 月 19 日投递、8 月 23 日面试、8 月 26 日收到感谢信；项目是自己参考 Claude Code / Kimi 思路拼出的 Coding Agent，评论区继续讨论现场 PDF→HTML System Design 题，流程与项目归属可核验。

高价值问题：

1. Agent Loop 的核心执行结构是什么？
2. 怎样理解 Harness Engineering，它和单纯 Prompt / Workflow 有什么区别？
3. 什么场景应该使用 Sub-agent？
4. 模型“偷懒”或不完成任务时怎样检测和约束？
5. Hallucination 怎样治理？
6. Skill 的组成、应用场景和加载方式是什么？
7. 是否理解 SDD / Spec-driven Development，它怎样约束 Coding Agent？
8. System Design：输入大量 PDF、输出 HTML、期间还要与知识库核对，如何设计 LLM Workflow？
9. 自研 Coding Agent 能否 Self-bootstrap，还是依赖其它 Coding Agent 开发？
10. 金融保险业务中 Agent / Vibe Coding 实际落地到什么程度，人工开发边界在哪里？

去重：URL、Claude Code 架构项目与投递→面试→感谢信时间线均未在现有来源出现。

---

## S273 OPPO｜AI 全栈开发｜一面｜面试 / 发布 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/cf5a82411c1e473385d8fcae6c250a6e

真人 / 第一人称证据：作者明确写这是本人第一次正式面试，记录自己 HTTP 状态码卡壳、面试官会换成候选人更熟悉的问题、整体氛围较融洽；反问还直接确认该岗位前端、后端和 Agent 的能力比例，Role Scope 清晰。

高价值问题：

1. 从用户输入 Prompt 到前端输出，AI Full-stack 链路中做了哪些处理？
2. 为什么按段落切 Chunk，实际 Retrieval 效果怎样？
3. 怎样判断 Evidence 不足并拒答，而不是让模型硬生成？
4. 为什么一个项目需要 Multi-Agent，而不是一个更大的单 Agent？
5. Short-term / Long-term Memory 怎样理解？
6. 常见 HTTP Status Code 及工程语义是什么？
7. 实际遇到 Hallucination 时怎样处理？
8. 全栈中自己最擅长哪一侧，如何用真实项目证明？
9. 页面卡顿如何定位性能瓶颈并优化？
10. 岗位如何平衡 Frontend / Backend / Agent 能力？

去重：URL、候选人“处女面”时间线及项目追问未在现有 OPPO 样本中出现；与 `S175` 为不同候选人、不同流程。

---

## S274 上海某独角兽小厂｜AI 全栈开发｜技术面｜发布 2026-08-28，已通过｜HUMAN-A

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

## S275 字节跳动｜Agent 开发｜秋招一面｜面试 2026-09-03，发布 09-04｜HUMAN-A

来源：https://www.nowcoder.com/discuss/925342611194286080

真人 / 第一人称证据：本帖此前因单页现场证据偏弱未在 Batch 12 入库。本轮沿作者“小妞脂”主页回溯，确认其持续记录百度、文远知行等多家公司明确日期、多轮与结果的本人秋招时间线；当前帖子与该时间线一致，且项目、算法与 Harness 追问具有独立场次特征，因此在补足作者 / 招聘流程证据后升级为 HUMAN-A。

高价值问题：

1. AI 项目的整体架构是什么，简历评分怎样 Structured Output？
2. RAG 的 Offline Upload 与 Online QA 两条链路分别怎样实现？
3. 如何理解 Agent Harness？
4. 正常 5 分钟的 Long-running Agent 突然跑到 15–20 分钟，怎样定位延迟来源？
5. 发现延迟后，从 Model / Tool / Network / Queue / Retry / Context 哪些层定位和治理？
6. Tool 参数由模型结合 Context 生成时，如何保证 Tool Call Reliability？
7. Conversation 轮数增长导致 Context Window 膨胀时怎么处理？
8. Summary / Compression 必然丢信息，怎样保护关键约束和任务状态？
9. Coding：给定数字集合，可重复使用数字，求严格小于 `n` 的最大可构成数字。

去重：URL 与题序未在现有来源出现；本轮新增的是作者时间线证据，而不是因题目内容“看起来高级”降低门槛。

---

## S276 文远知行｜AI 全栈开发｜三面｜面试 2026-08-18，进入横向｜HUMAN-A

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

去重：同作者还存在字节 `S275`，但公司、岗位流程、日期和题序均完全独立，应视为不同候选流程的两次真人命中；文远知行 URL 未在旧 Batch 收录。

---

# 本批清洗与研究观察

本批正式新增：**12 个 HUMAN-A（S265–S276）**。

同时完成一项存量修正：小红书 `S260` 同一候选人的 8 月 17 日二面被作者后续补发，已并入 `S260`，不新增来源数量。

## 典型排除

- **AIGC小白入门记内容账号链**：同一账号短时间连续发布快手、阿里等多家公司“真人叙事”，并进入订阅 / 付费专栏；无法把这些页面当作独立候选人原始面经，全部零贡献。
- **去哪儿 AI 全栈 / AI 应用的自动 AI 面**：页面明确描述 AI 面试官根据候选人关键词自动追问，即使题目覆盖 MCP / Memory / Harness，也属于 AI 自动面试，按固定规则排除。
- **平安科技 Agent 开发“完整答案型”页面**：正文大段直接给出标准化方案 / 答案，不满足候选人本人真实现场复盘标准，排除。
- **阿里 AI 全栈标准题单、推荐区“思路参考 / 标准答案”内容**：缺少足够候选人现场痕迹或属于教学化整理，不能因题目高级而入库。
- **跨平台 / 推荐页摘要**：只能看到搜索摘要而无法回到稳定原文的线索继续保持零贡献。

## 本批新增信号

1. **Long-running Agent 已从“会不会 Resume”升级为运行时诊断题。** 亚信安全直接问数天任务的 Checkpoint / Resume；字节要求定位原本 5 分钟任务突然变成 15–20 分钟的具体原因；FOSHO 则从长视频异步处理追到状态与恢复。
2. **Token / Cost Budget 开始变成 Backend Concurrency 问题。** 亚信安全把 Redis Rate Limit、Token Budget、并发预算预留与 Streaming 中途预算耗尽放在同一组追问里，成本控制已不是简单计费统计。
3. **Vector / Retrieval 深度继续上升。** IVF、HNSW、FAISS、PGVector、Bi-Encoder / Cross-Encoder、BM25、RRF、Rerank、Recall / Precision Trade-off 都进入目标岗位真人面试。
4. **项目验真越来越依赖量化证据。** 快手追 Intent Accuracy、Evaluation Set、用户数和日会话；小红书追 30min→5min 的视频处理优化；字节追“数据库性能提升 20%”到底怎么测，答不清会被直接卡住。
5. **AI Coding 正和 Harness / SDD / Product Engineering 汇合。** 平安健康问 Coding Agent 自举与 SDD；FOSHO问为什么自研 Coding Agent；小红书 / OPPO把 AI Coding 质量、MVP、上线与前端性能放进同一场。
6. **AI Full-stack 不是“前端 + 调模型”的轻量岗位。** OPPO、小红书、文远知行、上海独角兽都同时考察 Agent / RAG 与页面性能、Backend、数据库一致性、Vector Retrieval、Evaluation 和 Production Trade-off。
7. **作者时间线是越来越重要的真实性证据。** 随着内容账号和付费“真人叙事”增多，只看单页文风已不够；作者历史招聘流程、跨轮次更新和评论互动成为三层去重与 HUMAN-A Gate 的关键补证手段。

## 饱和判断

**仍未达到来源饱和。** 泛搜索污染率和重复率继续上升，但本轮在 `S001–S264` 基线上仍确认 12 个独立 HUMAN-A，并额外找到一个已收录候选人的真实后续轮次；精确公司 / 岗位、作者主页和历史月份回扫仍有实际产出，因此尚不满足停止条件。

下一条正式来源从 **`S277`** 开始。
