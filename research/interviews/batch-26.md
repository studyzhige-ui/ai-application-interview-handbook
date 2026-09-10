# Batch 26 — HUMAN-A 真人高质量第一人称面经（最终主动搜索批次）

采集日期：2026-09-10

> 本批从 `S374` 继续编号。按“最后一次主动搜索”的要求，本轮只搜索 **2026 年大公司**，显著扩大搜索量，并继续覆盖牛客、小红书、知乎、脉脉、个人博客、独立站、技术社区、企业面经页与搜索索引。平台不设配额；所有来源仍执行完全相同的 HUMAN-A Gate。
>
> 分配编号前已重新直接回读 `batch-01.md` ～ `batch-25.md`，覆盖 `S001–S373` 全历史；对最终候选执行 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、5～10 个连续独特题序、招聘 Timeline 与跨平台 / 跨年份复制链去重。GitHub Code Search 的 0 命中仍只作辅助，不能证明未收录。
>
> HUMAN-A Gate 不变：**真人面试官 + 候选人本人第一人称 + 高技术密度 + 强现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非答案帖 / 非 AI 自动面试 / 非重复 = HUMAN-A**。通过 Role Scope 后保留整场真实问题，不因为某场大量考 Java / Redis / MQ / Security 就只摘 AI 名词。
>
> 本轮最终放行 **6 个独立 HUMAN-A（S374–S379）**，全部来自 2026 年大公司。新增来自百度、蚂蚁国际、阿里云和快手；其中快手为三个不同候选人的独立招聘流程。主动搜索阶段在本批后按用户要求正式收官；这是一项研究流程上的冻结决定，不代表宣称公开互联网已被数学意义上完全穷尽。

---

## S374 百度｜AI 应用工程师｜社招一面｜发布 2026-07-17，视频面，已挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/26578b46ce064ac6a5f67d41adb07eb7

真人 / 第一人称证据：作者 `shiyo` 的个人主页仅有这一篇公开面经，不是批量内容账号。原帖明确写“百度 AI 应用工程师 社招、一面、视频面、不含手撕、挂了”，并按自我介绍 → 项目深挖 → 八股 → 反问记录全过程。作者保留多个现场状态：权限越界不是本人模块、面后专门询问同事确认；Context 压缩重要性排序被前一个问题带偏；RAG Chunk Size 理由没有答好；BM25 当场漏掉 IDF；最后从系统状态发现未通过并复盘可能原因。

整场技术问题：

1. Multi-Agent 项目如何实现个性化 / 千人千面？
2. Multi-Agent 工作区和权限如何管理？越权访问其他目录时怎样处理？
3. 从零独立开发 Agent 时为什么选择 LangChain？
4. 为什么当前 Agent 没用 Vector DB，什么场景才需要？
5. Message / Context 如何维护？
6. 文件过大、Context Window 不足时怎样 Compression？
7. Tool 如何动态加载、注册？未来 Tool 数量继续增长时怎样优化 Discovery / Loading？
8. 一次 Agent Context 包含哪些信息，压缩时怎样判断信息重要性？
9. Production RAG 从 Chunk → Embedding → Hybrid Retrieval → Rerank → LLM 的完整链路是什么？
10. Chunk 怎样切、为什么带多级标题，Chunk Size 为什么取约 200–500？参数如何验证？
11. BM25 的核心机制是什么，IDF 在其中起什么作用？
12. 反问：业务方向和内部模型使用情况。

去重：已直接回读 `S001–S373`，当前 URL、作者和 7/17 百度社招流程未入库；“Multi-Agent Workspace / Permission → 越权目录 → 从零 Agent → Dynamic Tool Loading → Context Importance → Production RAG / BM25”连续题序未在历史正式来源形成同场重复。外部按罕见连续短语反查，仅定位到当前原帖及其站内展示，未发现更早同序来源。

---

## S375 蚂蚁国际｜AI 应用开发｜一面｜发布 2026-04-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/2e79e7a4e32648e39cdfdadddfe1dfa3

真人 / 第一人称证据：作者 `想奋斗的柠檬精天天摸鱼` 是长期个人求职账号，历史上持续记录本人不同公司的招聘流程和普通社区互动，不是订阅 / 题库内容账号。本帖明确以“给我面没招了，发点面经攒攒人品”发布；问题围绕自己的检索、会话、限流与缓存工程连续追问，包含针对恶意用户压垮模型、恶意 Prompt 和双层缓存的具体场景，Role Scope 明确为 AI 应用开发。

整场技术问题：

1. 实习与熟悉项目深挖：本人真正负责什么？
2. Multi-way Retrieval 为什么需要，多路结果怎样 Fusion？
3. Intent Recognition 怎样实现，多路检索相比单路的 Recall 提升如何证明？
4. Conversation Memory 怎样做，Sliding Window 如何设计？
5. Summary Compression 使用什么策略，如何避免关键信息丢失？
6. Fair Queue 怎样设计：只按 Request 还是还要按 User / Tenant？
7. 100 个用户中单个恶意用户大量发请求、甚至可能拖垮模型服务时如何限制？
8. 用户用恶意 Prompt 请求模型私密信息时如何防护？
9. Model Selection 如何做，是否比较过不同模型效果？
10. Circuit Breaker / Degradation 的实际效果怎样验证？
11. RAG Chunking 使用什么方法？
12. Cache Aside 与 L2 Cache 怎样理解？
13. ThreadLocal 中放什么，何时必须 Cleanup？
14. 为什么写操作更常选择删除 Cache 而不是直接更新 Cache？
15. System Design：商品信息采用两级缓存时，Local Cache 与 Redis 分别存什么、怎样分工？

去重：已直接回读全部历史 Batch。当前 URL、4/21 蚂蚁国际流程和“Multi-way Retrieval → Conversation Memory → User-level Fair Queue / 恶意洪泛 → Prompt Security → Circuit Breaker → Cache Aside / L2 Cache”长链未在历史正式来源出现。作者次日存在阿里云另一独立招聘流程，组织、岗位与题序完全不同，按规则分别计数。

---

## S376 阿里云｜后端 AI 开发｜27 届实习一面｜发布 2026-04-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/37add5c1c697419ca0589d2c9782f797

真人 / 第一人称证据：同为个人候选人 `想奋斗的柠檬精天天摸鱼`，但这是与 `S375` 不同的阿里云独立招聘流程。原帖稳定保留“继续分享最近面经”的个人时间线，并在安全部分直接写某个 `K...` 术语“真不知道，甚至没听出来”，评论区还有从业者调侃 Java 候选人被问了大量安全问题，现场感明显。岗位标题明确为“后端 AI 开发”，且 Agent 代码执行、RAG 企业知识库权限和 Tool Security 属于面试主体之一，通过 AI Backend Role Scope 后整场安全 / Redis 问题全部保留。

整场技术问题：

1. 实习经历深挖。
2. Redis 有哪些 Security Risk？无密码 Redis 暴露会导致什么风险？
3. System Design 是否考虑 User Permission / Authorization？
4. Bloom Filter 解决什么问题？
5. Cache Breakdown 怎样治理？
6. Agent System 是否允许执行代码？若允许，安全边界应放在哪里？
7. Enterprise RAG Knowledge Base 怎样管理员工访问权限并防止越权 Retrieval？
8. Tool Calling 从输入、选择、参数、执行到输出分别可能出现哪些安全问题？
9. 对 OpenClaw 的理解是什么？
10. 项目实际代码量、日常编码量是多少，怎样证明工程参与深度？
11. Reverse Shell 是什么？
12. Docker Escape 是什么，常见触发边界有哪些？
13. Web Security：SQL Injection、XSS、CSRF 分别是什么？
14. 是否有 CTF Experience？
15. Fastjson 可能出现哪些安全问题？

去重：已直接回读 `S001–S373`。当前 URL、作者的 4/22 阿里云流程以及“Redis Security → Permission → Agent Code Execution → RAG ACL / 越权 → Tool Security → Reverse Shell / Docker Escape → Web Security / Fastjson”连续题序均未入库。搜索到后发个人博客将这场面试整理成“阿里后台八股文”并补答案，发布时间晚于当前牛客原帖，只作为复制链信号，不计来源。

---

## S377 快手杭州电商｜大模型应用 Java｜一面 + 二面（同一候选人同流程合并）｜面试 2026-03-05 / 03-09，发布 03-15，二面后当晚 OC｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/e198a07fa1744750b5d2b6df5ac74ac5

二面来源：https://www.nowcoder.com/feed/main/detail/4fd1625793814fe1a596f1d14eececbf

真人 / 第一人称证据：两篇均由 `在游泳的打工鸭很亲切` 发布，身份均为 NUS Java，发布时间相邻，明确记录 3 月 5 日一面、3 月 9 日二面，属于同一快手大模型应用招聘流程。作者从 2024 年起已有普通求职社区评论 / 互动，并非为批量面经新建的内容号。一面结尾记录面试官当场告知通过；二面则记录设计模式答得不好、原本要求写 Producer / Observer Pattern 时不会，主动请求换题，改为 Union-Find 后只写一半转口述，最后当晚收到 OC，现场与招聘时间线完整。

整场技术问题：

### 一面

1. Knowledge-base QA 从 Document Ingestion 到最终 Answer 的完整链路是什么？
2. Vector Retrieval 使用什么 Index？Recall 后是否 Rerank？
3. Knowledge Base 的 Precision / Recall 怎样 Evaluation？
4. Spring AI Alibaba Function Calling 如何实现，Model 如何决定调用哪个 Tool？
5. Tool Call Failure 怎样处理？
6. Execute-Plan Mode 怎样实现？
7. 常用哪些模型、Coding Model，怎样做选择？
8. ES、Milvus 等 Vector Database / Index 方案怎样比较？
9. Prompt Engineering 有哪些真实实践原则？
10. 是否了解 GraphRAG / Agentic RAG？
11. 秒杀下单中 Redis Lua 做什么，为什么需要原子脚本？
12. 项目是否做过 Load Test，对 QPS 有什么量化认知？
13. 什么时候使用 Distributed Cache，什么时候再加 Local Cache？
14. Java ThreadPool 核心参数、任务执行流程和线程数如何配置？
15. 当前 RAG 最大 Bottleneck 是什么？
16. System Design：设计百万 / 千万级商品 Knowledge Base QA。
17. 商家动态更新价格 / 描述时，知识库如何增量更新并保持新鲜度？
18. Coding：Binary Tree Level-order Traversal。

### 二面

19. 项目真实使用过程中遇到过什么问题？
20. Spring AI Alibaba 与其它 RAG Framework 的差异是什么；哪些能力复用、哪些自己实现？
21. Vector DB 使用什么 Index Algorithm？
22. 看过哪些 RAG 论文 / 前沿机制，业内主要优化方向是什么？
23. 类比“人看书”时，能否通过目录 / 摘要等结构提升 Retrieval Efficiency / Recall？
24. Java Collection 的继承体系与 HashMap 父类 / 接口关系是什么？
25. Collection / JDK / Spring 源码中有哪些 Design Pattern？
26. Singleton 有哪些实现方式？
27. 如何看待 Vibe Coding，AI-assisted Coding 有哪些局限？
28. Coding / Design：最初要求 Producer + Observer Pattern；候选人不会后请求换题，改为 Union-Find / 集合合并，现场未完整写完。

去重：两篇同作者、同公司、同岗位、连续轮次，主动合并为一个 `Sxxx`。本轮还检索到 3 月 18 日另一页面几乎逐题复用了 3/5 一面的“Knowledge QA → Function Calling → Execute Plan → Lua → ThreadPool → 百万/千万商品 KB”顺序；后者发布时间更晚，因此判为后发复制页、零贡献，只保留当前 3/5 + 3/9 原始流程。

---

## S378 快手｜AI 应用服务端开发｜二面｜面试 2026-04-09，发布 04-11｜HUMAN-A

来源：https://www.nowcoder.com/discuss/872512773710696448

真人 / 第一人称证据：作者 `纯马牛马牛🐮` 是南京林业大学后端候选人，个人账号在相邻日期记录京东物流等不同公司的本人求职流程，不是面经内容账号。本帖明确写“4.9 面，没后续了”，原因不是技术结果，而是候选人只能 6 月到岗，面试官表示中间会继续招人、若 6 月仍有名额再捞；同时现场询问到岗时间和可实习时长，招聘流程痕迹很强。问题明确来自“快手 AI 应用服务端开发 二面”。

整场技术问题：

1. 什么时候能到岗、能实习多久？
2. Redis Cluster 如何工作，底层 Storage Logic 怎么理解？
3. Redis 单节点与 Cluster 的 Performance / Capacity 大概如何估计？
4. Agent 项目为什么使用 Spring AI Alibaba？
5. Spring AI Alibaba、LangChain4j、Spring AI 怎样比较，Framework Selection 依据是什么？
6. 实际使用 Spring AI Alibaba 时哪些能力好用、哪些地方不方便？
7. Agent Orchestration 的 DAG 是什么；项目为什么使用 / 没使用？
8. 是否用过 OpenClaw，对内部技术机制了解多少？
9. 项目为什么选 RabbitMQ，与其它 MQ 比较有哪些优缺点？候选人现场承认主要因为当时只学过 RabbitMQ，并认为 RocketMQ 可能更适合部分场景。
10. Coding：Merge K Sorted Lists；候选人说明前几天 PDD 一面刚做过同题。
11. 反问：团队转正率与考察方式。

去重：已直接回读全部历史快手来源。当前 URL、作者和“到岗时间导致流程暂停 → Redis Cluster → Spring AI Alibaba / LangChain4j / Spring AI 选型 → Agent DAG → OpenClaw → RabbitMQ → Merge K Lists”连续题序未在 `S001–S373` 形成同场重复。未找到可稳定核验的同作者快手一面原帖，因此不猜测、不补写，只收当前二面。

---

## S379 快手｜大模型应用 Java 实习｜一面｜面试 2026-08-17，发布 08-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/756a5f6d2c914bf0a9edca5787bf6266

真人 / 第一人称证据：作者 `Wang_PD` 的个人 Timeline 可串起 3 月得物安全开发入职讨论、8 月快手面试和 9 月知乎全栈一面，账号持续记录本人求职 / 实习而非批量搬运。本帖明确写“8.17 日面”，约 30 分钟全问项目，随后约 30 分钟 Vibe Coding，要求用 AI 现场做出一个浏览器插件并给了 Mock Data；这种现场交付比普通题单具有更强真人验证。岗位标题明确为“大模型应用 Java 实习”。

整场技术问题：

1. Agent 的完整 Workflow 是什么？
2. 常见 Agent Development Paradigm 有哪些，怎样选择？
3. Tool 如何调用，工程上需要注意哪些 Failure / Validation 问题？
4. 项目中的 Tool Integration 做过什么优化，解决了什么问题，指标如何得到？
5. Redis Distributed Lock 如何与 Kafka 协同，为什么当前业务这样设计？
6. Kafka 怎样提高消费可靠性并保证业务幂等？
7. SkillHub 的 Skill Storage Logic 怎样设计，是否做 Compliance Verification？
8. Agent 自动运营体系怎样搭建，效果用什么 Benchmark / Metric 评价？
9. Vibe Coding：约 30 分钟内使用 AI 做出浏览器插件，支持 Tab Management、Browsing-history Storage 和 Next-action Recommendation，并基于给定 Mock Data 完成交付。
10. 反问团队 / 流程。

去重：已直接回读 `S001–S373`。当前 URL、作者、8/17 流程和“Agent Project → Tool Integration Metric → Redis Lock + Kafka → SkillHub Compliance → Agent 自动运营 Benchmark → 30min Browser Plugin Vibe Coding”连续链均未在历史来源出现。外部按罕见题序检索仅定位到当前原帖及站内话题 / 评论镜像，未发现更早独立来源。

---

## 最终批次观察

1. **最后一次扩大搜索仍然能找到新增，但增量主要来自历史长尾与企业深页，而不是 9 月热门第一页。** 最终 6 条中，4 条来自 3～4 月，1 条来自 7 月，1 条来自 8 月。
2. **最新热门结果层已经高度饱和且内容化严重。** 9 月大厂 Agent 搜索持续出现历史已收 URL、60% 付费“真人叙事”、带完整答案专栏、浙江大学算法工程师等批量模板账号，以及同题序后发页面。
3. **跨平台主动搜索没有产生额外正式来源。** 本轮再次主动检索小红书、知乎、脉脉、博客园、CSDN、个人博客 / 独立站；能稳定检索到的高曝光页面大量明确自述为“流传面经整理”“多渠道汇总”“题目 + 参考答案 / 推荐回答”，或只是索引 / 二次转载。平台多样性不能替代原始候选人真实性。
4. **Agent 应用岗位与传统工程底座继续深度耦合。** 蚂蚁国际同时问 Retrieval / Memory / Fair Queue / Cache；阿里云把 Agent / RAG 权限与 Redis / Container / Web Security 放在一起；快手三条流程又把 RAG / Agent 与 Java ThreadPool、Redis Cluster、MQ、Design Pattern、System Design 绑定。
5. **AI Coding / Vibe Coding 已成为可观察的交付验证。** `S379` 直接给 30 分钟浏览器插件任务，而 `S377` 二面也明确追问 Vibe Coding 的局限；考察从“会不会用 AI”继续转向“是否能按时间交付并知道 AI 的边界”。
6. **复制链追源仍是最重要的质量控制。** 本轮快手 3/18 强候选最终追到更早的 3/5 原场，说明“新 URL + 高技术密度”仍远远不够，发布时间、作者和连续题序必须同时成立。
7. **主动采集阶段在 Batch 26 后按用户要求结束。** 当前结论是：8～9 月大厂热门结果层高度局部饱和，3～7 月仍可能理论上存在残余长尾，但继续搜索的边际收益已经显著低于 Provenance / 去重成本。本项目从此冻结主动搜索基线，不把“停止主动搜索”表述成“互联网绝对没有遗漏”。

## 典型排除

- 9 月 PDD / 快手等“浙江大学 算法工程师”批量页面：同类账号跨公司高频发布，常带 60% 付费 / 订阅内容，按内容账号与付费答案包装排除。
- RockyDing / WeThinkIn、博客园 / CSDN 等“含完整答案”“真题 Top50”“面试全攻略”页面：正文明确属于整理、解析或跨渠道汇总，零贡献。
- 快手 3/18 大模型应用页面：连续 20+ 题几乎逐题命中更早 3/5 原场，判后发复制，零贡献。
- 美团 9 月 AI 后端个人帖：账号真人，但正文只有实习 / 项目拷打、AI Coding、少量 Redis / MySQL 概括，信息密度不足，零贡献。
- 腾讯 4 月若干强候选：部分只能稳定打开二次汇总而原始正文无法完整访问，按 Stable Original Gate 排除；另有原帖虽问题多但缺少足够现场 / 招聘流程证据，保守排除。
- 快手效果营销、京东物流、阿里云 SRE 等普通 Backend / SRE 流程：即使候选人项目里出现 RAG / Agent，也不能证明岗位本身属于目标 Role Scope，零贡献。
- 已核验真人作者的 PDD / 快手 Kstar / 百度等进度帖：只有流程状态而没有找到可稳定核验的对应完整技术原帖，进度帖本身不贡献题目。
