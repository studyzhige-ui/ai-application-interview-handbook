# Batch 21 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **8** 个正式来源。

---

## S248 腾讯｜Agent 开发｜日常实习一面｜发布 2026-04-09，已挂｜HUMAN-A

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

去重：已直接回读 `S001–S247`。本场独特的“多模态跨场景误召回 → Qwen Tool Call 适配 → Memory 生长 / 淘汰 → State Machine → Repo Dependency Retrieval → 400 Bad Case 扩万级训练集”连续长链未在历史 Tencent 来源中构成同场；URL、作者和日期也均独立。

---

## S249 腾讯｜AI Application / Agent（实际面试内容明确）｜实习二面｜发布 2026-04-08，约 50min｜HUMAN-A

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

## S250 小红书｜Agent 开发｜一面｜发布 2026-04-24｜HUMAN-A

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

去重：历史 `S027` 为另一候选人的 OpenManus / Harness 流程；本场独特的“小红书产品场景缓存 → 中频搜索词 → 超长不可丢 Context → 内部代码库模糊检索 → K 线程最小 makespan”题序独立。另有 3 月小红书多页面出现 Deep Research 停止条件等高度同序链，本批未混入该不确定复制链。

---

## S251 字节跳动安全与风控｜后端研发实习生（AI Agent）｜一面｜发布 2026-04-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/604a4a66936d4a00b4a6b22b5a40bb0c

真人 / 第一人称证据：作者 `zzzilik` 的主页可串起本人 2026 实习求职 Timeline，并在不同公司持续记录个人面试；本帖标题明确为“字节跳动-后端研发实习生（ai agent）-安全与风控 一面面经”，正文以“发面经攒人品”发布。前半段围绕候选人实习中的 Vector Retrieval、Hybrid Retrieval、RRF、OpenClaw / Context Engineering，后半段进入 Network、Redis、OS、Python 与现场 Coding；岗位标题虽是后端，但 AI Agent / RAG 是明确业务与面试主体，按 AI Backend / Agent Role Scope 通过。

整场技术问题：

1. 约 20 分钟实习深挖。
2. 了解哪些 Vector Index，各自优缺点是什么？
3. 实习项目为什么使用 Hybrid Retrieval；从业务角度分析这样做的收益。
4. RRF 算法怎样工作？
5. 怎样平衡 Rerank 的速度与质量？
6. 了解哪些 Vector Retrieval Database，各自优缺点是什么？
7. OpenClaw 的 Architecture 怎样理解，Context Engineering 是怎样做的？
8. HTTP 与 HTTPS 的区别是什么？
9. TCP 三次握手和四次挥手的流程是什么，为什么建立连接需要三次握手而不是两次？
10. Redis 有哪些 Persistence 机制，各自优缺点和适用场景是什么？
11. Process 与 Thread 的区别是什么？
12. Python GIL 的机制和影响是什么？
13. Coding：对折链表。
14. Coding / Design：实现 Singleton Pattern。

去重：已直接回读 `S001–S269`。作者 4 月还存在快手等其它公司独立求职流程，其中部分已在历史库；本场是字节安全与风控独立流程，不与不同公司合并。当前 URL 和“Hybrid Retrieval / RRF → Vector DB → OpenClaw Context → HTTPS / TCP → Redis Persistence → GIL → 链表 / Singleton”连续题序未在正式来源中形成同场重复。

---

## S252 美团｜AI 全栈开发｜日常实习一面｜发布 2026-04-14｜HUMAN-A

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

## S253 蚂蚁｜智能体 / 大模型应用｜暑期一面 + AI 应用开发二面（同一候选人同流程合并）｜发布 2026-04-10 / 04-24｜HUMAN-A

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

## S254 阿里云｜后端 AI 开发｜实习一面｜发布 2026-04-22｜HUMAN-A

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

## S255 百度｜AI 应用开发｜实习一面｜发布 2026-05-03｜HUMAN-A

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

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## 本轮扩大搜索的典型排除 / 重复案例

- **Code Search 0 命中但历史已收**：阿里平头哥 4/28 候选在辅助 Code Search 中没有直接命中，但重新直接回读历史 Batch 后确认就是历史 `S118`；再次证明不能把“0 命中”当未收录证据。
- **拼多多历史精确重复**：7/25 提前批线下 AI Agent 两轮原帖 `45f6e73f8e9d4888b9c066a160f89f60` 已是历史 `S061`，不新增。
- **同候选人同公司后续轮次**：`想奋斗的柠檬精天天摸鱼` 的腾讯 4/27 页面已经是历史 `S020`；同公司相邻后续流程不因为出现新 URL 就重复计数，也不反向修改历史 Batch。
- **作者级复制风险**：账号 `星轨偏差` 的腾讯 5/3 页面虽然 URL / 作者不同，但“Minimum Path Sum → Java Interface/Abstract Class → StringBuilder/Buffer → synchronized → DI → HashMap → MyBatis → 熔断限流 → Kafka → Slow Query → EasyExcel 1 万行 / 第 5000 行失败恢复”的长题序与历史 `S232` 几乎整场一致。该账号其它新候选（如京东）因此进入高风险 Provenance 状态，本批全部不收。
- **正文稳定失败，即使 Search Snippet 很强也不收**：蚂蚁国际 4/21、京东 5/3、快手 4/30 等若干候选在搜索结果里题目很强，但重新打开原始正文时只剩壳页 / Internal Error / 极少行，按 Verifiable Gate 排除。
- **美团同作者同公司相邻双帖**：`脆片温柔` 4/7 与 4/14 两条都像真实面试，但同公司、同岗位方向、时间仅隔一周，无法证明不同招聘流程；不拆两个 ID，只保留 4/14 现场验真证据更完整的页面。
- **字节同作者同公司相邻流程**：`想奋斗的柠檬精天天摸鱼` 4/21 与 5/4 均为字节 AI / Agent 方向，但流程边界无法稳定确认，因此只计 5/4 一个独立来源，避免双计。
- **Bilibili / CSDN / 聚合站“2026 大厂面经”**：大量页面明确写“整理全网干货 / 高频题 / 每题标准答案 / 资料包”，以及 NiceOffer 等二次整理站，即使公司标题热门也全部零贡献。
- **最新热门结果面仍高度饱和**：9 月热门关键词返回的大量字节 / 腾讯 / 美团 / PDD / 百度结果已在 `S001–S247`，或属于内容账号、后发扩写、转载 / 帮转；本轮大部分新增来自 4–6 月长尾和作者 Timeline，而不是 9 月第一页。

---

## Batch 21 搜索漏斗 / 饱和度判断

1. **搜索量显著增加后，新增 HUMAN-A 从连续两批的 6 个提高到 11 个。** 这不是放松门槛：本轮反而重新直接回读了全部 20 个历史 Batch，并继续执行稳定正文 / 作者 / 题序硬 Gate。
2. **因此“当前整体已接近来源饱和”证据不足。** 如果整体真正接近饱和，把 Query 组合扩到 120+、增加 3–7 月长尾和作者 Timeline 后，边际产出应该仍接近 0–3；实际仍得到 11 个独立来源，说明此前搜索 Recall 确实还有缺口。
3. **但“热门最新结果面局部饱和”已经很明确。** 8–9 月普通热门关键词搜索的新增率很低，重复 / 内容包装 / 同场多 URL / 不稳定正文比例高；新的正式来源越来越依赖精确月份、作者主页、候选人跨公司 Timeline 和项目独特词。
4. **4–6 月历史长尾仍有可观剩余。** 本轮腾讯 `S248/S249/S158`、字节 `S107/S251/S097`、小红书 `S250`、美团 `S252`、蚂蚁 `S253`、阿里云 `S254`、百度 `S255` 大量来自春季实习周期，说明这一区间过去覆盖仍不充分。
5. **下一轮应继续做“固定搜索预算下的边际产出实验”。** 建议继续保持每轮至少约 100 组公司 × 岗位 × 月份 × 平台组合，同时单独记录新增来源来自 `最新结果页 / 历史长尾 / 作者 Timeline / 牛客外原帖` 哪个 Bucket；只有连续多轮在相同搜索强度下新增持续降到很低，才应判断接近整体饱和。

本批新增 **11 个 HUMAN-A：`S248–S255`**。正式库累计 **348 个**，下一编号 **`S256`**。当前结论：**不是整体饱和；此前确有搜索 Recall 不足，同时热门最新结果面已经局部饱和。**
