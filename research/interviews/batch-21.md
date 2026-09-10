# Batch 21 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S338` 继续编号。本轮专门扩大搜索量，用于判断“连续两批只新增 6 个”究竟是搜索 Recall 不足，还是热门公司真人来源已接近饱和。搜索仍以热门公司为主，但把重点从 8–9 月热门结果页扩展到 **2026-03～07 历史长尾 + 作者 Timeline + 公司 / 岗位 / 月份交叉检索**。
>
> 本轮保守统计发起 **120+ 组公司 × 岗位别名 × 月份 × 平台 / 技术关键词检索组合**，逐页核验数十个候选；随后重新直接回读 `batch-01.md` ～ `batch-20.md`，覆盖 `S001–S337` 全历史。正式来源仍必须同时满足：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非重复 = HUMAN-A**。
>
> 最终放行 **11 个独立 HUMAN-A（S338–S348）**。这说明前两批“每批 6 个”并不等价于整体饱和：扩大历史月份和作者 Timeline 后仍能显著抬高新增量。但 8–9 月热门关键词第一页依旧大量由历史重复、内容账号、后发扩写、同场多 URL 与正文不稳定构成，因此当前更准确的判断是：**热门结果面局部饱和，但热门公司的历史长尾真实来源仍未挖完。**

---

## S338 腾讯｜Agent 开发｜日常实习一面｜发布 2026-04-09，已挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/aef9769bc0604700bcc8ed4fa8db8377

真人 / 第一人称证据：作者 `Elite求职中` 以本人“T厂 Agent开发日常实习一面挂凉经”发布，开场先现场手撕约 5 分钟，之后连续深挖多模态 RAG、实习意图识别、代码生成、Qwen Tool Calling、Memory、状态机和代码助手；正文还保留到岗时间、毕业论文等真实招聘流程问题。作者主页 / 评论表现为个人求职轨迹，不是内容账号。

整场技术问题：

1. 多模态 RAG 中图片如何预处理并向量化检索？
2. 多模态预处理最难的工程问题是什么？
3. 怎样避免跨业务场景召回“看起来相似、实际错误”的步骤？
4. Retrieval Precision / Recall 使用什么评估框架，指标具体怎么算？
5. 为什么不能只追 Recall 而忽略 Precision？
6. 实习里的 Intent Recognition 模型解决什么真实问题，效果提升怎样证明？
7. 数据集怎样构造，项目周期和开发人员配置怎样？
8. 代码生成项目为什么做，与经典 Agent / Coding Framework 解决的问题有何不同？
9. 为什么相关经典框架不能直接适配 Qwen，问题发生在哪个协议 / Tool Calling 环节？
10. 怎样让 Qwen 正确使用 Tool；Thinking / Non-thinking Model 输出有哪些差异？
11. 怎样处理错误 Tool Call、空 Tool Call 和无效结构化输出？
12. 项目是完全自研还是参考已有实现，本人真正做了哪些改造？
13. Long-term / Short-term Memory 由谁定义，分类依据是什么？
14. Long-term Memory 怎样维护、总结和更新，什么时候触发 Summary？
15. Short-term Memory 如何晋升为长期记忆，怎样与已有 Memory 合并？
16. FIFO 淘汰长期记忆有什么问题，是否应该改为 Retrieval-on-demand？
17. Memory 占据 Context Window、压缩输出空间时怎样治理？
18. State Machine 在 Agent 中承担什么职责，大模型怎样感知当前 State？
19. RAG 在当前系统什么时机触发？
20. 大规模代码助手落地最大的工程难点是什么？
21. 怎样让模型理解大型 Repo，并高效找到相关依赖和调用关系？
22. 除 Dependency Graph 外，还有哪些 Repo Understanding / Retrieval 方案？
23. 模型后训练如何利用真实 Bad Case；只有约 400 条差回答时怎样扩展到万级训练数据？
24. 最近看过哪些 Agent / AI Engineering 技术文章或框架，它们解决什么问题？

去重：已直接回读 `S001–S337`。本场独特的“多模态跨场景误召回 → Qwen Tool Call 适配 → Memory 生长 / 淘汰 → State Machine → Repo Dependency Retrieval → 400 Bad Case 扩万级训练集”连续长链未在历史 Tencent 来源中构成同场；URL、作者和日期也均独立。

---

## S339 腾讯｜AI Application / Agent（实际面试内容明确）｜实习二面｜发布 2026-04-08，约 50min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/4d7f1675cf01408283a41aa044f13215

真人 / 第一人称证据：作者 `java仔想找实习` 记录本人腾讯二面，正文结束直接写“自己给自己挖坑，很多细节答不上来”“面完感觉被抽干了，像做了一次小丑”，评论区也有同期二面候选人互动。虽然标题没有写完整岗位名，但整场技术主体是 Text2SQL、RAG、Multi-Agent、Memory、MCP，实际职责明确通过 AI Application / Agent Role Scope。

整场技术问题：

1. 不同表规模下 Text2SQL 的技术方案怎样变化？
2. 为什么把表中每一行做 Embedding，使用什么 Embedding Model？
3. Row-level Vectorization 与 Table Metadata Retrieval 的优劣是什么？
4. Text2SQL 业界常见方案 / Framework / Failure Mode 有哪些？
5. Jira Agent / RAG 项目解决什么问题，高频 Query 是什么？
6. 为什么使用 Keyword + Vector Hybrid Retrieval，各自负责什么 Recall？
7. 结构化数据为什么适合固定 Chunk，哪些数据不适合？
8. 长文档怎样 Chunk，按标点切分造成语义割裂时怎么解决？
9. 为什么需要 Rerank；项目加 Rerank 后效果反而变差，如何定位？
10. Query Rewrite 怎样做，具体解决哪些检索问题？
11. RAG 与 Small-model Fine-tuning 分别适合什么场景？
12. Multi-Agent 使用什么 Architecture，Task 怎样 Orchestrate？
13. 对 OpenCloud / Perplexity 等 Agent System 的理解是什么？
14. Short-term / Long-term Memory 怎样设计与协作？
15. Agent 相比直接调用 LLM 的工程价值是什么？
16. 怎样允许用户自定义 Agent 与 MCP，完整配置 / 执行流程怎样设计？

去重：URL 未在历史 Batch 出现；“Text2SQL Row Embedding vs Metadata → Jira Hybrid RAG → Rerank 负收益 → Query Rewrite → Multi-Agent / Memory → 用户自定义 Agent + MCP”题序与已收腾讯样本不同，未发现同作者同公司同流程的既有来源。

---

## S340 小红书｜Agent 开发｜一面｜发布 2026-04-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3a50438ddf984a38a2b98fa8ead0328c

真人 / 第一人称证据：作者 `想奋斗的柠檬精天天摸鱼` 为持续记录本人求职进度的候选人账号，本帖明确写“小红书 agent 开发一面 / 发点面经攒人品”。问题不是标准 Agent 八股，而是围绕超长 Context、内部代码库检索、小红书问一问 / Search AI Summary 的真实成本与缓存场景连续追问，并有线程调度 Coding。

整场技术问题：

1. 项目数据来源是什么，怎样保证数据真实可用？
2. Context 过长时怎样处理？
3. 如果内容非常长、且每个字符都重要，不能简单截断怎么办？
4. 把长任务拆成多次执行时，怎样保证每次都拿到足够 Context？
5. 怎样设计 Cache，哪些结果值得缓存？
6. 企业内部代码库怎样构建 Knowledge / Retrieval Layer？
7. Fuzzy Query Retrieval 怎样保证结果质量？
8. Query Rewrite 后再检索的完整链路是什么？
9. 对小红书“问一问”和搜索栏 AI Summary 的产品 / 技术理解是什么？
10. 如果自己设计，怎样平衡模型 Cost 与 Response Speed？
11. 问一问可以按帖子粒度缓存，Search AI Summary 应怎样缓存？
12. 对“搜索量不大不小”的中频 Keyword，Cache / Online Generation 怎样取舍？
13. Coding / Scheduling：给定 N 个任务耗时、最多 K 个线程并行，求最小总完成时间。

去重：历史 `S260` 为另一候选人的 OpenManus / Harness 流程；本场独特的“小红书产品场景缓存 → 中频搜索词 → 超长不可丢 Context → 内部代码库模糊检索 → K 线程最小 makespan”题序独立。另有 3 月小红书多页面出现 Deep Research 停止条件等高度同序链，本批未混入该不确定复制链。

---

## S341 字节跳动｜Agent 开发｜实习一面 + 二面（同一候选人同流程合并）｜发布 2026-06-17 / 06-23｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/075c06bf50a143a785c039f9951624f6

二面来源：https://www.nowcoder.com/feed/main/detail/675f834ce9fa4a29b2c413d87241e6bb

真人 / 第一人称证据：两篇均由作者 `Ariasu` 发布，作者主页只有这两篇求职记录；公司、岗位、项目和时间线连续，一面 6/17，二面 6/23，明确属于同一字节 Agent 招聘流程，因此只计一个 `Sxxx`。一面持续追 Context 三层压缩、会话恢复、Skill / Tool、Multi-Agent 与 RAG 增量知识，二面继续追 Memory 生长、Token 成本、GraphRAG 与 SFT / DPO / GRPO。

整场技术问题：

### 一面

1. Claude Code 与 Codex 各自有什么特点？
2. 一次请求给模型的 Prompt / Context 由哪些部分组成，哪些必须注入？
3. 自己的 Coding Agent 与 Claude Code / Codex 的本质差异是什么？
4. Context Compression 怎样做？为什么采用三层压缩策略？
5. 三层压缩各自压什么、在什么条件触发？
6. 怎样发现“压缩过度已经伤害任务效果”，如何恢复？
7. 用户在旧任务上继续加功能时，怎样恢复 Session，哪些状态必须重新注入？
8. Tool Calling 完整链路是什么，Skill 能否替代 Tool？
9. Skill 体系怎样设计，模型实际调用 Tool / Skill 的次数怎样观测？
10. 复杂任务的 Planning 怎样生成和更新？
11. Multi-Agent Orchestration 怎样实现，各 SubAgent 有何区别？
12. SubAgent 是否应该共享全部 Tools，为什么？
13. 第二个 RAG 项目的数据源是什么，入库前怎样清洗冗余噪声？
14. PDF 各种结构怎样解析，是否做 Knowledge Extraction？
15. Knowledge Base 增量更新怎样实现？
16. 多文档内容冲突怎样解决，如何做版本控制和错误文档 Rollback？
17. Coding：0/1 Grid 中判断左上到右下是否存在可行路径。

### 二面

18. Coding Agent 从输入到执行的完整 Chain 是什么？
19. Skill 分层体系怎样实现，用户输入怎样匹配相关 Skill？
20. Skill 是否可以从执行轨迹自动沉淀，还是只能人工构造？
21. Long-term / Short-term Memory 怎样设计；为什么还区分 Static / Dynamic Long-term Memory？
22. 每轮都可能写 Memory 时，怎样避免长期记忆快速膨胀？
23. LLM 怎样决定是否 Recall 某条长期记忆？
24. Context Compaction 的 Token Window / Trigger Threshold 怎样定，为什么？
25. Dynamic Prompt 与 Static Prompt 有何区别？
26. 模型底座如何选；生成约 1000 行代码需要多少 Token / Cost，是否真正量化过？
27. 为什么 Agent Cost 会达到当前水平，哪些环节最耗 Token？
28. 为什么当前项目需要 GraphRAG，而不是纯 Vector Retrieval？
29. 什么问题才算 Multi-hop / Reasoning Query？
30. Llama3、SFT、DPO、GRPO 等训练 / 对齐方法在当前项目里理解到什么深度，Data 与 Evaluation 怎样设计？

去重：两 URL 均未在 `S001–S337` 出现；同作者同公司同项目明确合并。独特的“三层 Context Compression → 压缩质量检测 / Session 恢复 → Skill 调用次数 → RAG 版本回滚 → 二面 Memory Growth / Token Cost → GraphRAG → Alignment 方法”连续链未在历史字节来源出现。

---

## S342 字节跳动安全与风控｜后端研发实习生（AI Agent）｜一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/604a4a66936d4a00b4a6b22b5a40bb0c

真人 / 第一人称证据：作者 `zzzilik` 明确以本人“字节跳动-后端研发实习生（ai agent）-安全与风控 一面面经”发布，实习深挖约 20 分钟，随后从 Hybrid Retrieval / RRF / Vector DB 进入 OpenClaw、网络、Redis、OS、GIL 和 Coding。作者其它动态是个人求职时间线，不是批量答案账号。

整场技术问题：

1. 实习项目本人真正负责什么，核心效果怎样验证？
2. 了解哪些 Vector Index，各自优缺点是什么？
3. 为什么业务选择 Hybrid Retrieval，收益来自哪里？
4. RRF 怎样融合多路排序？
5. 怎样在 Rerank Quality 与 Latency 之间权衡？
6. 了解哪些 Vector Database，各自边界是什么？
7. OpenClaw Architecture 怎样理解，它的 Context Engineering 怎么做？
8. HTTP 与 HTTPS 的核心区别是什么？
9. TCP 三次握手 / 四次挥手怎样工作，为什么握手不能只有两次？
10. Redis Persistence 有哪些机制，各自适合什么业务？
11. Process 与 Thread 的区别是什么？
12. Python GIL 怎样影响并发？
13. Coding：Fold / 重排链表类问题。
14. Coding / Design：实现 Singleton Pattern。

去重：作者、日期、BU 和题序独立；历史字节安全 / Agent 样本中未出现“Vector Index → Hybrid/RRF → Rerank Latency → OpenClaw Context → HTTP/TCP → Redis Persistence → GIL → Fold List/Singleton”同场长链。

---

## S343 腾讯｜AI 应用开发后端｜实习一面｜发布 2026-04-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/144c6ae334b24c0aa643ed43ccfebaac

真人 / 第一人称证据：作者 `面试从容应对` 明确写“腾讯实习 ai应用开发后端面经分享 / 攒人品”，项目深挖约 40 分钟，随后面试官现场引入跨境汇款金融场景继续追 Agent Timeout / Failure 与资金安全，再问不停服更新 RAG KB 和 Coding，面试结构非常自然。

整场技术问题：

1. 项目是否已有正式用户，为什么当前没有上线？
2. Multi-Agent 怎样编排，具体执行流程是什么？
3. Training Sample 从哪里来，是否做过 Model Tuning？
4. Agent Failure / Interrupt 怎样处理，Retry 怎样保证安全？
5. 金融场景：跨境汇款 Agent 超时 / 失败时怎样保护资金安全？
6. 有副作用的金融 Tool 怎样避免重复执行和错误恢复？
7. RAG Knowledge Base 更新时怎样做到不停服？
8. 项目里实际用过哪些 Design Pattern，为什么？
9. Coding：Maximum Area of Island / DFS。

去重：历史腾讯 Agent Backend 场次虽多，但当前作者、日期和“40min 项目验真 → 跨境汇款资金安全 → RAG Hot Update → Design Pattern → Island DFS”题序独立；未发现同候选人同流程已入库来源。

---

## S344 美团｜AI 全栈开发｜日常实习一面｜发布 2026-04-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/71e51594f46f45e18bc8481286895031

真人 / 第一人称证据：作者 `脆片温柔` 明确记录本人美团 AI 全栈一面并“攒人品”；前半段持续比较自己 Agent 的 Memory / Retrieval 与 OpenClaw（原帖称“龙虾”），随后要求共享屏幕演示 Agent Architecture、Function、Code，面试官甚至查看 Cursor 对话记录来验真项目；作者明确写“Java 项目一点没问，全问 AI”，最后还有 LC21 与 AI Coding，现场痕迹很强。

整场技术问题：

1. 项目核心架构与本人贡献是什么？
2. Short-term / Long-term Memory 与 Search / Retrieval 是什么关系？
3. OpenClaw 的 Memory Mechanism 与当前项目有什么差异？
4. 如果把 OpenClaw Tool 全部剥离，只比较 Memory / Retrieval，两套方案差异是什么？
5. 自己还做过哪些 Agent 项目，是否真正使用 MCP？
6. 为什么需要 Progressive Disclosure？
7. Skill 与 MCP 的边界是什么？
8. Skill Progressive Disclosure 在实现层怎样落地？
9. 共享屏幕：现场演示 Agent 架构、功能和真实 Code，并回答实现细节。
10. 面试官查看 Cursor Conversation History，怎样证明 AI Coding 过程中本人理解并主导修改？
11. Coding：Merge Two Sorted Lists。
12. AI Coding：现场完成一项开发题并解释验证方式。

去重：同作者 4/7 还存在另一条美团“后端 AI 开发一面”，但同公司、时间仅隔一周，无法可靠证明为独立招聘流程；本批不拆两个编号，也不让 4/7 页面贡献问题，只保留现场证据更强、能够独立成立的 4/14 AI Full-stack 原帖为一个来源。

---

## S345 蚂蚁｜智能体 / 大模型应用｜暑期一面 + AI 应用开发二面（同一候选人同流程合并）｜发布 2026-04-10 / 04-24｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/8d817a84839949ed85d2bc7fe5f8e9bf

二面来源：https://www.nowcoder.com/feed/main/detail/73d4714ff5b940c39d69f02d0d7edeea

真人 / 第一人称证据：两篇均由作者 `脆片温柔` 发布，一面标题明确“蚂蚁27暑期智能体大模型应用一面”，二面明确“蚂蚁实习 AI应用开发二面 70m”；项目 / 时间线连续，因此按同一候选人同公司同流程合并。二面从 MinerU / RAGAS、LangGraph State、Memory、GraphRAG 深挖到 Tool Parameter Hallucination、Self-reflection、Human-in-the-loop 和 Skill / MCP。

整场技术问题：

### 一面

1. 实习 / 项目最重要的技术选择和难点是什么？
2. 单机与 Cluster 怎样选，系统如何支持 Horizontal Scaling？
3. 防重复下单 Token 怎样生成 / 传递，TTL 怎样定？
4. Order ID 为什么选 Snowflake 而不是 Auto-increment，集群环境下怎样保证正确？
5. Order State Machine 怎样设计，中间状态和 Trigger 是什么？
6. “商家已接单”等事件遇到 Network Reorder / Retry 时如何避免状态更新错乱？
7. Sharding Key 怎样选？
8. 爆款视频评论导致 Data Skew / Hot Partition 怎么处理？
9. 一级评论 / 二级回复表怎样设计？
10. `reply_count` Hot Update 怎样优化？
11. 如果全程 AI Coding，一个外卖 / 评论业务怎样从需求拆到可交付实现？
12. 把系统按 Submodule 逐个交给 AI 实现有什么局限？
13. AI Coding 普及后，Software Testing 怎样与 AI 协作？

### 二面

14. MinerU 遇到 Cross-page Table 时怎样保持表格语义完整？
15. RAGAS 怎样评测；Answer Relevance 低时怎样区分 Retrieval 问题和 Generation 问题？
16. LangGraph State 怎样定义 / 流转；Node 很多时如何避免 State Object 过大甚至 OOM？
17. Long-term Memory 怎样从多轮对话提炼 Structured User Profile，并存入 Vector DB？
18. Chunk Overlap 的作用是什么，怎样平衡粒度与语义完整性？
19. GraphRAG 召回大量关联信息后，怎样用 Reflection / CoT Filter Noise？
20. ReAct 的核心机制是什么？
21. Tool Parameter Hallucination / Syntax Error 怎样自动检测和修复？
22. Centralized Multi-Agent Orchestration 与 P2P 协作有何优劣？
23. Self-reflection 如何发现自身输出中的逻辑错误？
24. Long-term Memory 怎样设计生命周期？
25. Payment 等高风险操作怎样插入 Human-in-the-loop？
26. Skill 怎样设计，Skill 与 MCP / OpenClaw Filesystem / Code Environment 有什么边界？
27. Vibe Coding 怎样从自然语言任务变成可靠执行路径，Context Cache 怎样参与？

去重：两轮同作者 / 同公司 / 同招聘季，主动合并一个 ID。历史蚂蚁来源未出现“订单状态乱序 / 热评论 → MinerU 跨页表格 → RAGAS Attribution → LangGraph State OOM → Tool Parameter Hallucination → Payment HITL”完整题序，确认独立。

---

## S346 阿里云｜后端 AI 开发｜实习一面｜发布 2026-04-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/37add5c1c697419ca0589d2c9782f797

真人 / 第一人称证据：作者 `想奋斗的柠檬精天天摸鱼` 记录本人“阿里云27实习 后端AI开发一面面经”，正文自然地从 Redis Security、Permission、企业 RAG 越权一路追到 Agent Code Execution、Tool Security、Reverse Shell、Docker Escape、Web Security；其中一个安全术语作者直接写“真不知道，甚至没听出来是什么”，有明显现场失败痕迹。

整场技术问题：

1. 实习项目最核心的本人工作是什么？
2. Redis 有哪些 Security Risk？
3. Redis 无密码访问会导致哪些真实攻击面？
4. System Design 中怎样做 User Permission / Authorization？
5. Bloom Filter 在系统中解决什么问题？
6. Cache Breakdown 怎样治理？
7. Agent 是否具有执行代码能力，执行边界怎样限制？
8. Enterprise RAG 中怎样管理员工对 Knowledge Base 的访问权限，防止越权读取？
9. Tool Calling 哪些环节最容易发生 Security Issue？
10. OpenClaw 的执行 / 权限模型怎样理解？
11. 项目代码量、日常编码量是多少，怎样证明本人真实工程能力？
12. Reverse Shell 是什么，Agent / Sandbox 场景怎样防止被利用？
13. Docker Escape 是什么，容器是否等于绝对安全？
14. 常见 Web Security：SQL Injection、XSS、CSRF 分别怎样防？
15. Fastjson 等反序列化风险怎样理解？
16. 是否有 CTF / Security Practice 经验？

去重：历史阿里云 Agent / AI Backend 来源中未出现“Redis 无密码 → 企业 Knowledge Permission → Agent Code Execution / Tool Security → Reverse Shell / Docker Escape / Web Security”同场安全长链；作者和 URL 也均未入库。

---

## S347 字节跳动｜后端 AI 开发｜实习一面 1h｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ab0601f3dbad49ab87ea870a00bb3691

真人 / 第一人称证据：作者 `想奋斗的柠檬精天天摸鱼` 明确写“27实习-字节后端ai开发一面 1h / 发点面经攒攒人品”。问题从 Smart Ops Agent 的真实含义、Spring AI Alibaba 覆盖边界、Planner/Executor/Supervisor 架构，连续追到 RAG / Fine-tuning、MySQL/Redis 和万级 Producer / Consumer 并发场景。

整场技术问题：

1. Agent 项目的核心功能是什么？
2. “智能运维助手”的运维具体指什么业务动作？
3. 系统有哪些主要组件，数据 / 控制流怎样走？
4. Spring AI Alibaba 覆盖了哪些部分，哪些 Runtime 能力仍需自己实现？
5. Planner / Executor / Supervisor Pattern 的优势是什么？
6. 三个 Agent 与一个 Agent 相比，关键收益和额外代价是什么？
7. RAG 的核心流程是什么？
8. Recall / Rerank 使用什么算法；如果没做 Rerank，为什么？
9. 为什么当前业务需要 RAG？
10. Model Response Bad Case 应怎样从 RAG 层优化，又在什么情况下考虑 Fine-tuning？
11. Fine-tuning 属于 Pre-train 还是 Post-train，应用工程师需要理解哪些边界？
12. MySQL 与 Redis 各自适合什么数据 / 访问模式，“Relational”是什么意思？
13. Redis 能否承担持久存储，而不仅是 Cache？
14. System Design：1 万 Producer、5 万 Consumer 的 Java 生产消费模型怎样做并发控制、队列、背压与资源治理？

去重：同作者 4 月还有其它公司独立招聘流程，可以分别计数；同作者 4/21 另有字节相关页面，但与 5/4 同公司、同招聘季且流程关系无法稳定拆分，本批只保留能独立成立、信息更完整的 5/4 一面，不对 4/21 另行编号或补题。历史字节样本没有当前“Spring AI Alibaba → 3-Agent vs 1-Agent → RAG/Fine-tuning → 万级 Producer/Consumer”连续链。

---

## S348 百度｜AI 应用开发｜实习一面｜发布 2026-05-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c55cd0d8ef1f40f39a0a5b2b4f9b7974

真人 / 第一人称证据：作者 `静息狂想` 以本人“27实习百度 AI应用开发面经分享”发布，开头自评“面完人都通透了，还是太菜了，下去沉淀一下”。题目从实习 / 项目验真进入 Intent Recognition、Base Model Selection、FAISS、Evaluation、4-GPU Distributed Deployment、PagedAttention、Rerank、Load Test / Bad Case 与现场 Coding，实际 Role Scope 清晰。

整场技术问题：

1. 实习项目本人负责什么，遇到过什么问题、怎样解决？
2. Intent Recognition 怎样实现？
3. Base Model 怎样选型，考虑哪些能力 / 成本 /延迟信号？
4. 为什么使用 FAISS，有没有比较其它 Vector DB / Index？
5. FAISS 核心原理怎样理解？
6. 系统回答效果怎样 Evaluation？
7. 四张 GPU 做 Distributed Deployment 怎样实现？
8. PagedAttention 的核心思想是什么，为什么能改善推理 Memory Management？
9. Rerank 怎样设计，实测是否真的有提升？
10. Model / Service Load Test 怎样做？
11. 出现 Answer Bad Case 时怎样从 Retrieval / Model / Prompt / Runtime 分层定位？
12. Coding：删除链表倒数第 N 个节点。

去重：URL 未入库；直接回读全部历史 Batch 后未发现“Intent → FAISS → 4 卡部署 → PagedAttention → Rerank 实测 → Load Test / Bad Case → 链表”同序百度场次。搜索外部题序也未找到更早同序原场，当前作为独立候选流程收录。

---

## 本轮扩大搜索的典型排除 / 重复案例

- **Code Search 0 命中但历史已收**：阿里平头哥 4/28 候选在辅助 Code Search 中没有直接命中，但重新直接回读历史 Batch 后确认就是历史 `S122`；再次证明不能把“0 命中”当未收录证据。
- **拼多多历史精确重复**：7/25 提前批线下 AI Agent 两轮原帖 `45f6e73f8e9d4888b9c066a160f89f60` 已是历史 `S061`，不新增。
- **同候选人同公司后续轮次**：`想奋斗的柠檬精天天摸鱼` 的腾讯 4/27 页面已经是历史 `S020`；同公司相邻后续流程不因为出现新 URL 就重复计数，也不反向修改历史 Batch。
- **作者级复制风险**：账号 `星轨偏差` 的腾讯 5/3 页面虽然 URL / 作者不同，但“Minimum Path Sum → Java Interface/Abstract Class → StringBuilder/Buffer → synchronized → DI → HashMap → MyBatis → 熔断限流 → Kafka → Slow Query → EasyExcel 1 万行 / 第 5000 行失败恢复”的长题序与历史 `S310` 几乎整场一致。该账号其它新候选（如京东）因此进入高风险 Provenance 状态，本批全部不收。
- **正文稳定失败，即使 Search Snippet 很强也不收**：蚂蚁国际 4/21、京东 5/3、快手 4/30 等若干候选在搜索结果里题目很强，但重新打开原始正文时只剩壳页 / Internal Error / 极少行，按 Verifiable Gate 排除。
- **美团同作者同公司相邻双帖**：`脆片温柔` 4/7 与 4/14 两条都像真实面试，但同公司、同岗位方向、时间仅隔一周，无法证明不同招聘流程；不拆两个 ID，只保留 4/14 现场验真证据更完整的页面。
- **字节同作者同公司相邻流程**：`想奋斗的柠檬精天天摸鱼` 4/21 与 5/4 均为字节 AI / Agent 方向，但流程边界无法稳定确认，因此只计 5/4 一个独立来源，避免双计。
- **Bilibili / CSDN / 聚合站“2026 大厂面经”**：大量页面明确写“整理全网干货 / 高频题 / 每题标准答案 / 资料包”，以及 NiceOffer 等二次整理站，即使公司标题热门也全部零贡献。
- **最新热门结果面仍高度饱和**：9 月热门关键词返回的大量字节 / 腾讯 / 美团 / PDD / 百度结果已在 `S001–S337`，或属于内容账号、后发扩写、转载 / 帮转；本轮大部分新增来自 4–6 月长尾和作者 Timeline，而不是 9 月第一页。

## Batch 21 搜索漏斗 / 饱和度判断

1. **搜索量显著增加后，新增 HUMAN-A 从连续两批的 6 个提高到 11 个。** 这不是放松门槛：本轮反而重新直接回读了全部 20 个历史 Batch，并继续执行稳定正文 / 作者 / 题序硬 Gate。
2. **因此“当前整体已接近来源饱和”证据不足。** 如果整体真正接近饱和，把 Query 组合扩到 120+、增加 3–7 月长尾和作者 Timeline 后，边际产出应该仍接近 0–3；实际仍得到 11 个独立来源，说明此前搜索 Recall 确实还有缺口。
3. **但“热门最新结果面局部饱和”已经很明确。** 8–9 月普通热门关键词搜索的新增率很低，重复 / 内容包装 / 同场多 URL / 不稳定正文比例高；新的正式来源越来越依赖精确月份、作者主页、候选人跨公司 Timeline 和项目独特词。
4. **4–6 月历史长尾仍有可观剩余。** 本轮腾讯 `S338/S339/S343`、字节 `S341/S342/S347`、小红书 `S340`、美团 `S344`、蚂蚁 `S345`、阿里云 `S346`、百度 `S348` 大量来自春季实习周期，说明这一区间过去覆盖仍不充分。
5. **下一轮应继续做“固定搜索预算下的边际产出实验”。** 建议继续保持每轮至少约 100 组公司 × 岗位 × 月份 × 平台组合，同时单独记录新增来源来自 `最新结果页 / 历史长尾 / 作者 Timeline / 牛客外原帖` 哪个 Bucket；只有连续多轮在相同搜索强度下新增持续降到很低，才应判断接近整体饱和。

本批新增 **11 个 HUMAN-A：`S338–S348`**。正式库累计 **348 个**，下一编号 **`S349`**。当前结论：**不是整体饱和；此前确有搜索 Recall 不足，同时热门最新结果面已经局部饱和。**