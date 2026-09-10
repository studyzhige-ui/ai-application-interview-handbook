# Batch 17 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S309` 继续编号。仍只接受：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场痕迹 + AI Application / Agent 目标岗位 + 正文稳定可核验 + 非转载 / 非合集 / 非重复 = HUMAN-A**。
>
> 本轮在分配编号前重新直接回读 `batch-01.md` ～ `batch-16.md`，覆盖 `S001–S308` 全历史，并逐项执行 URL 精确比对、公司 / 岗位 / 日期 / 轮次比对、题序 / 项目语义比对、作者 / 招聘流程时间线比对。GitHub Code Search 的 0 命中仅作为辅助保险，不作为“未收录”的证明。
>
> 同一候选人同一公司同一招聘流程的多轮继续合并；同一候选人面试不同公司，若招聘流程独立则分别计数。通过 Role Scope 后仍保留整场真实技术问题，包括 Backend / Java / Python / MySQL / Redis / Network / Concurrency / Coding 等，不只摘 Agent 名词。

---

## S309 OPPO｜IT 开发（实际纯 Agent）｜27 届秋招一面｜面试 2026-08-27，发布 09-02，已挂｜HUMAN-A

来源：https://www.nowcoder.com/discuss/923561467092160512

真人 / 第一人称证据：作者明确记录约 40 分钟真人一面、无手撕、没有传统 Java 八股，“几乎全程围绕 Agent 项目连续深挖”；面后更新已挂，并写自己第一次被纯 Agent 拷打、很多问题靠面试官给上下文和引导才继续回答。问题从 ReAct 代码实现一路进入 MCP、Skill、多模态 Context、Text-to-SQL 和 AI Coding / 新仓库上手，现场链路完整。

高价值问题：

1. Agent 具备哪些区别于普通 LLM Chat 的核心特征？
2. ReAct 从代码 / Runtime 视角怎样实现，除了 Loop 与 Function Calling 之外还有哪些机制驱动循环？
3. Agent Loop 上一轮结果如何传到下一轮，哪些状态应进入 Context，为什么不能把所有生成文本无差别塞进去？
4. MCP `stdio` 与 Streamable HTTP 的差异是什么？如果设计高德 MCP，会怎样拆 Tool、Schema、Transport 与执行边界？
5. Skill 的 Progressive Loading / Progressive Disclosure 怎样实现？
6. Word 文档同时有文字和图片，Agent 读取后需要返回图文混合 Response，Parsing、Context、引用与最终输出链路怎样设计？
7. Text-to-SQL 如何处理业务“黑话”和语义近似词？除了 Text-to-SQL，还能否通过 Ontology 等方式做智能问数？
8. Cursor / Copilot / Codex / Claude Code 等 Coding Agent 在真实开发中怎样使用？
9. 进入陌生仓库后怎样完成从 0 到 1 的理解、定位和第一次需求修改？
10. 两个月后旧需求再次演进时，怎样恢复历史 Context、重新理解影响范围并安全修改？

去重：已直接回读 `S001–S308`。URL 未入库；作者、8/27 OPPO 流程和“ReAct Runtime → 高德 MCP 设计 → Skill 渐进加载 → Word 图文 Context → Text-to-SQL 黑话 / Ontology → 新仓库演进”的连续题序均未发现历史同场或复制链。

---

## S310 腾讯｜后台 Agent 开发｜日常 / 实习一面｜发布 2026-04-29｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/5a6705afdb45487e852c29bad27575d5

真人 / 第一人称证据：作者 `max_81` 的主页是少量本人求职流程记录，并非批量面经账号。本帖以“继续分享最近面经”发布，候选人明确保留“微服务熔断降级不会，自己把话题引到限流”等现场回答状态。岗位标题明确是后台 Agent 开发，但真实一面大量考察 Java / Middleware / MySQL，最后再回到大模型项目，属于目标 Agent Backend 的完整工程能力样本。

高价值问题：

1. Coding：Minimum Path Sum。
2. Java Interface 与 Abstract Class 的区别是什么？
3. 几万次字符串拼接应该选择 `String`、`StringBuilder` 还是 `StringBuffer`，为什么？
4. Java 常见线程安全手段是什么；`synchronized` 能怎样使用和修饰代码？
5. Spring / Java 中哪些 Annotation 可以实现 Dependency Injection？
6. HashMap 何时扩容，扩容流程和关键机制是什么？
7. MyBatis 如何避免 SQL Injection？
8. 微服务 Circuit Breaker / Degrade 与 Rate Limit 分别解决什么问题，常见限流方案有哪些？
9. Kafka 如何支撑高流量与高可用？
10. MySQL 出现 Slow Query 时怎样定位和优化？
11. 简历使用 EasyExcel 解析 1 万行 Excel，如果处理到第 5000 行失败，怎样设计断点、幂等、重试和恢复，避免前 5000 行重复写入？
12. 项目接入了哪个 LLM，为什么这样选？
13. 大模型应用的数据具体存在哪里，如何组织？
14. 项目中的模型 / 应用准确率怎样定义和测量？

去重：URL 与作者流程未在 `S001–S308` 出现；“EasyExcel 10000 行 → 5000 行失败恢复”这一罕见项目题序经全历史直接回读和辅助检索均未命中。

---

## S311 字节跳动｜后端 Agent 开发｜实习一面 1h｜发布 2026-04-19｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d73020680b3b42c3ac579e2f25721d90

真人 / 第一人称证据：作者以本人“字节后端 Agent 开发实习一面 1h”发布，问题沿真实 RAG 项目连续追设计理由与失败案例，而不是背 RAG 流程；尤其会追候选人自己加的“小结”为什么反而降低 Recall、为什么只 Embedding 标题，以及 Skill 是否真能替代 Tool。最后有现场 Coding。

高价值问题：

1. 当前 RAG 与传统 RAG 有什么真正的 Innovation / 落地差异，还是只是把标准方案实现了一遍？
2. RAG 效果怎样 Evaluation，失败应如何 Attribution？
3. 给文档额外生成“小结”后反而导致召回率下降，可能的负向机制是什么？
4. 为什么只对标题做 Embedding，而不是对段落正文一起做 Embedding？这种策略的 Recall / Precision 代价是什么？
5. Prompt Engineering 与 Context Engineering 的本质区别是什么？
6. 当前热门的 Skill 概念到底解决什么问题？
7. Skill 与 Tool / Function Call 的职责边界是什么？
8. Skill 能否覆盖 Tool、从而完全不需要 Tool？为什么？
9. 所谓“Skill 替代 Function Call”在实现层究竟怎样发生，哪些执行仍必须由确定性 Runtime 完成？
10. Coding：非递归实现 Binary Tree Preorder Traversal。

去重：URL、作者和 4/19 字节流程未入库；“RAG 小结造成 Recall 下降 → 标题-only Embedding → Skill 是否覆盖 Tool / Function Call”连续题序未在历史来源发现。

---

## S312 中兴通讯｜Agent 开发｜实习一面凉经｜发布 2026-05-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/81ef46253510446d93530b20fcb0815f

真人 / 第一人称证据：作者为东南大学候选人，主页能看到连续个人求职记录；本帖明确是“实习 Agent 开发一面凉经 / 发面经攒人品”。面试官围绕候选人在北京医疗科技公司的 RAG 实习逐层挑战具体实现，尤其直接质疑其“>512 Token 存向量库、<512 存缓存”的设计是否能被检索，具有强项目验真痕迹。

高价值问题：

1. 北京医疗科技实习实际做了什么，RAG Knowledge Base 从原始 Text 到可检索数据的完整流程是什么？
2. 候选人所说“大于 512 Token 存向量数据库、小于 512 存缓存”具体是什么意思？如果某部分不进入 Vector DB，查询时如何找到？
3. 用户 Natural Language 表达高度不确定时，RAG Response 的波动和错误怎样评估与治理？
4. Retrieval 中的 Vector Distance 是否来自 Embedding Model，文本向量化过程怎样解释？
5. 实际使用哪个 Embedding Model，为什么？
6. 项目是否使用 GPU，公司是否有训练 / 推理资源，RAG 部署在本地还是企业服务器？
7. Knowledge Distillation 是什么，为什么项目会使用？
8. 是否写过 Skill，Skill 在当前 Agent 体系里是什么？
9. 项目使用哪些语言和开发工具？除了 Cursor，候选人是否能独立编码？
10. Cursor / AI Coding 与本人手写代码各自适合什么场景，怎样证明自己理解生成代码？
11. 英语 / CET6 等沟通能力如何满足岗位需求？

去重：URL 未在 `S001–S308` 出现；“512 Token → Vector DB / Cache 的设计被面试官反问检索闭环”是独特现场题序，历史中未发现同作者同流程或高相似复制。

---

## S313 成都某中厂（网络安全 / 自研 Agent 产品）｜Agent 产品开发实习｜一面｜面试 2026-06-15，发布 06-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d770696f3495465d9e3d40c3d631d54c

真人 / 第一人称证据：作者明确记录约 30 分钟一面，并完整写出第一次求职面试的时间线：6/11 开始投递、当天 HR 主动联系、收到 6/15 面试邀约；面试前焦虑，现场不会就直接说不了解，面试官会引导并给项目 / Agent 学习建议。作者同时说明公司在网络安全领域有业务且近年自研 Agent 产品，Role Scope 清晰。

高价值问题：

1. Prompt Engineering、Context Engineering、Harness Engineering、Loop Engineering 四者有什么区别？
2. 为什么 Context Engineering 能解决单一 Prompt 无法解决的问题？
3. Harness 主要解决哪些 Agent 工程问题？
4. Function / Tool Calling 从模型决定调用到真实工具执行、结果回填的完整流程是什么？
5. BM25 与 Vector Retrieval 的差异和组合方式是什么？
6. 构建 RAG 时最核心的环节是什么，Data Processing / Chunking 为什么关键？
7. PDF 语料真实量级是多少？普通 Chunking 丢失跨片段关联时怎么办，GraphRAG 是否适用？
8. 是否建立自己的 Evaluation Dataset 验证 RAG，而不是只看几个 Demo？
9. LoRA Fine-tuning 解决什么问题，候选人实际怎样做？
10. 应先改 Prompt 还是直接 Fine-tune，什么情况下微调才值得？训练数据来自哪里、质量如何保证？
11. 除 RAG 项目外还做过哪些 Agent，是否理解其 Runtime / Framework 原理？
12. Dify / Coze Workflow 与 Codex / Claude Code 这类 Agent 产品在自主性和工程结构上有什么不同？
13. 是否真正使用过 Claude Code / Skill，Skill 的原理与 Progressive Disclosure 是什么？

去重：历史直接回读未发现同 URL / 同作者 / 同招聘流程；“Prompt → Context → Harness → Loop Engineering 四层辨析”及其后连续 RAG / LoRA / Claude Code 题序未在正式库命中。

---

## S314 启云方｜AI Agent｜一面｜发布 2026-09-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fea2d18bd59a421da7d16fe16223d38c

真人 / 第一人称证据：作者 `评论是德国的` 主页只有少量本人求职记录，能串起小鹏、BIGO、宁波银行等流程，不是批量面经账号。本场前约 12 分钟问问题，之后约 40 分钟要求候选人手画执行流程并与面试官讨论；核心不是“会不会背 Function Calling”，而是追到 Model Structured Output 与外部 Agent Runtime 的真实边界。

高价值问题：

1. 日常使用哪些 AI Coding Tool，在 VS Code 中实际接过哪些 API？为什么选择 Codex / CoderX，和 DeepSeek 使用体验怎样比较？
2. 如果项目主要使用 TypeScript，是否能接受并快速迁移？
3. 怎样理解 Agent，Agent Developer 实际在开发哪些层？
4. “通过语言调用工具”到底是什么意思？以天气 Tool 为例，自然语言输入之后如何走到真实函数执行？
5. Tool 是否需要提前注册，需要提供 Name、Description、Schema、Permission 等哪些 Metadata？
6. Tool Selection 是关键词 / Rule / Intent Recognition，还是模型基于 Tool Schema 自主选择？
7. 模型决定 Tool Call 后，调用信息返回在哪里？是否只是普通文本再用 Regex 解析？
8. Tool Call 为什么通常是 Structured Output，JSON / 固定字段在协议中怎样表示？
9. Assistant Text 与 Tool Call 是否属于不同 Content Block / Message Data？
10. 模型究竟有没有“直接执行工具”，还是只生成结构化调用请求，由 Agent Loop / Runtime 负责执行和回填？
11. 手画 System Design：系统包含 Agent Loop、Model、Tool、Filesystem，用户说“帮我写一个贪吃蛇小游戏”后，完整执行路径怎样流转？

去重：全历史回读未发现启云方正式样本；URL、作者流程和“天气 Tool → Structured Tool Call → 手画 Agent Loop / Model / Tool / Filesystem 贪吃蛇执行链”均独立。

---

## S315 小鹏汽车｜AI 全栈产品研发培训生｜一面 13min｜发布 / 更新 2026-09-02，已挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ff967cd4e7384b26b38823025297450b

真人 / 第一人称证据：与 `S314` 为同一真实候选人，但小鹏是完全独立的公司招聘流程。作者明确记录飞书面试只有约 13 分钟、无法确认对方是否开摄像头、体验一般，并于 9/2 更新已挂；问题集中在本人 LangChain / RAG 能力和“Chunk 切断逻辑关系”的具体失败场景。

高价值问题：

1. AI 方向做过哪些真实项目 / 技术尝试，个人最擅长哪一块？
2. LangChain 在项目里具体做了什么，而不是只调用过哪些 API？
3. RAG 的完整实现链路是什么？
4. LLM 如何处理模糊 Intent Recognition，其工程机制怎样理解？
5. RAG 常见 Text / Semantic Chunking 方式有哪些？
6. Fixed Chunk 把强逻辑关系切到不同块时会产生什么问题？
7. 例如“A 是 B 的充分必要条件”恰好被切开，Retrieval / Generation 是否还能保持逻辑完整？
8. 如何通过 Parent-child Chunk、Overlap、Semantic Chunking、Metadata / Neighbor Expansion 等方式修复 Context / Semantic Loss？
9. 怎样理解 AI Full-stack Engineer，前端 / Backend / Model / Agent 的边界怎样协作？

去重：同作者 `S314` 为启云方流程，本场是小鹏独立招聘流程；URL、公司、日期和“充分必要条件被 Chunk 切断”场景均未在旧库命中。

---

## S316 杭州某小厂｜Agent 开发实习｜一面｜面试 2026-08-18，发布 08-20，先 OC 后流程中断｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d53ba1a49015406e9bd8216f48028198

真人 / 第一人称证据：作者明确写“8.18 一面已 OC，纯八股，结尾有反转”，后续原本约二面，但临时电话确认自己是 28 届后没有继续消息。虽然题目几乎都是传统 Backend Foundation，但岗位明确是 Agent 开发实习，这正是“目标 AI / Agent 岗并不保证一面问 Agent”的市场信号，因此通过 Role Scope 后保留整场技术问题。

高价值问题：

1. Java 三大特性；Overload 与 Override 的区别。
2. `String`、`StringBuffer`、`StringBuilder` 的差异与适用场景。
3. Spring Boot 的优缺点；常用 Annotation 有哪些？
4. MySQL Index Optimization 常见方式是什么，什么是 Back-to-table？
5. Transaction ACID 是什么，MySQL 四种 Isolation Level 怎样比较？
6. Non-repeatable Read 与 Phantom Read 的本质区别是什么？
7. Redis 的主要特性是什么；Cache Penetration / Breakdown / Avalanche 怎样治理？
8. TCP 与 UDP 的差异是什么？
9. Git 如何从远程仓库拉取项目并进行版本协作？
10. 项目通过 Docker 还是本地运行，Docker 从 Build 到 Run 的基本流程是什么？
11. 两个简历项目的真实实现细节是什么？
12. 平时怎样使用 AI 辅助开发？

去重：URL、作者和 8/18 杭州流程未入库。虽然单题多为高频 Backend 八股，但题序、候选人流程和明确 Agent 岗位均独立；不因“常见题”误判为重复。

---

## S317 滴滴｜AI Agent 后端｜两轮技术面，已挂｜2026 秋招 / 实习季｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/17ee6ae95cc44ec19b9eefadb69da6b3

真人 / 第一人称证据：作者明确以“滴滴 AI Agent 后端面经 / 两轮面经 / 已凉凉 / 发面经攒人品”发布。题目从本人 Agent 项目持续追到 Memory、Hallucination、Context Pollution，再大幅进入 Spring、Redis、Go Runtime、MySQL、WebSocket、扫码登录、Service Discovery 和 GC，能够很好代表 Agent Backend 的真实基础深度。

高价值问题：

1. 最近 Agent 项目是实习还是个人项目，本人具体负责哪些部分，最难的问题是什么、怎样解决？
2. Agent 的典型模块与常见设计范式有哪些？
3. Short-term / Long-term Memory 如何区分，Memory Compression 有哪些策略？
4. Agent 如何降低 Hallucination；放到工业场景时还需要哪些 Verification / Guardrail？
5. Multi-Agent / 多 Async Task 如何防止 Context Pollution？
6. 项目为什么选择 Spring 或 Socket，协议 / Framework 取舍是什么？
7. Spring AOP Proxy 在什么情况下失效；Circular Dependency 如何定位；Spring MVC 完整执行流程是什么？
8. Maven Transitive Dependency 会引入什么冲突，怎样处理？
9. Redis 支持哪些结构、为什么快、为何常说核心命令单线程；发生 Blocking 会有什么影响？
10. ZSet 底层结构与应用场景是什么；Sentinel 怎样工作；BigKey 对 Memory / Latency 有什么影响？
11. Go Channel 与 Mutex 在并发控制上的差异是什么；GMP 中 P 的 Local Queue 为空 / 非空时如何调度 G？
12. MQ 适合什么场景？Database Transaction ACID 与 MVCC 怎样实现？
13. Database Index 底层结构是什么，哪些写法会导致 Index Invalid？
14. 设计类似淘宝搜索框的实时商品名 Fuzzy Search；输入联想与点击搜索的技术差异是什么？实时交互为什么可能使用 WebSocket？
15. 微信扫码登录从 PC 二维码到手机授权、Token / Session 建立的完整流程是什么？
16. 微服务 Service Discovery / Load Balancing 怎样实现，Nacos / Consul 如何注册、保活与 Heartbeat？
17. JVM GC 基本机制和 CMS Collector 如何工作？
18. Coding：Reverse Linked List。

去重：URL 和两轮滴滴 AI Agent Backend 流程未在 `S001–S308` 出现；“Agent Memory / Context Pollution → Spring → Redis → Go GMP → 实时搜索 / WebSocket → 扫码登录 → Service Discovery → CMS”的长题序未发现同场复制。

---

## S318 快手｜AI 应用服务端开发｜秋招一面 + 二面 + 三面（同一候选人合并）｜2026-08-26 / 09-01 / 09-09｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/1f6732ca32c74e17af502c71e77c8c59

二面来源：https://www.nowcoder.com/feed/main/detail/2892c62d66b24268959644260a7d7044

三面来源：https://www.nowcoder.com/feed/main/detail/ef8b41f126664ff2879337d43889a4ee

真人 / 第一人称证据：三篇均由 `27备战秋招` 发布，作者主页明确给出连续时间线：8/26 一面、9/1 二面、9/9 三面，项目始终是本人 `CR Agent`，因此严格合并为一个来源。二面记录 Coding 虽做出但过程不好、面试官态度明显变化以及自己对 SDD 追问的挫败感；三面又恢复为业务 / 架构交流并讨论 Offer 与实习时间，现场与流程连续性很强。

高价值问题：

**一面：**

1. 深挖 `CR Agent` 项目：解决什么问题，本人负责什么？
2. A2A 与 MCP 的职责和通信差异是什么？
3. Java 常见 Design Pattern 如何在真实工程里使用？
4. SDD / Spec-driven Development 怎样理解？
5. 现场 Coding。
6. 平时 AI Coding 使用频率和真实工作流是什么？

**二面：**

7. 再次深挖 `CR Agent` 设计与实现。
8. 继续追微软实习中的 Backend 设计。
9. Coding 虽完成，但面试官继续评价实现过程、思路表达和工程质量。
10. 继续讨论 SDD，要求证明不是只会背定义。

**三面：**

11. 是否了解部门业务、对业务是否真正感兴趣？
12. 为什么 `CR Agent` 需要做成 Distributed Architecture？
13. Agent 与 Agent 之间怎样通信，异常发生后怎样保证系统稳定？
14. Lua Script 包裹过长业务逻辑会产生哪些阻塞、可维护性与 Redis Event Loop 风险？
15. 两道简单 Coding。
16. 当前是否有其它 Offer；如果发 Offer，何时能够实习？

去重：三轮 URL 分别检查均未入库；全历史直接回读也未发现该作者快手流程。三轮明确同候选人同公司同项目，因此只占一个 `S318`，不按轮次虚增。

---

## S319 阿里灵犀互娱｜交易支付·大模型应用开发｜秋招一面 + 二面 + 三面 / HR｜2026-08-31 / 09-02 / 09-07，09-08 意向｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/ff4827f42c5844b9967d6751d2e3b9b3

二面来源：https://www.nowcoder.com/feed/main/detail/c8935da5044a4376b9f45d2cc46ba469

三面来源：https://www.nowcoder.com/feed/main/detail/85a64d94c3374a10afa20d7466d24d5d

流程来源：https://www.nowcoder.com/feed/main/detail/f29afdc906bd47d9b3812fbc1ce3cf96

真人 / 第一人称证据：同样由 `27备战秋招` 发布，但这是与 `S318` 完全不同公司的独立招聘流程。作者给出完整 Timeline：8/31 15:00–16:00 一面、9/2 17:00–18:00 二面、9/7 11:00–12:00 三面 + HR 交叉面，9/8 收到意向书；HR 还反馈面试官认为其 AI / LLM 理解和工程实践较强。各轮持续围绕同一 `CR Agent`、Backend Engineering、Harness 与游戏 Agent 展开，合并计一个来源。

高价值问题：

**一面：**

1. 深挖 `CR Agent` 项目。
2. 高并发系统怎样设计？
3. 给定复杂游戏业务场景，如何设计应用 / Agent 方案？候选人明确记录这题很难、答得不好。
4. 现场 Coding；候选人自评一般但本轮通过。

**二面：**

5. 深挖微信相关 Backend Design。
6. 再次深挖 `CR Agent` Architecture。
7. Agent Harness 怎样理解，在项目里承担什么？
8. Agent / Service 异常怎样处理和恢复？
9. AI Search 怎样设计？

**三面 + HR：**

10. 最难的项目是什么，真正的 Challenge 在哪里？
11. 怎样与团队协作、怎样学习新知识？
12. 与上下游意见不一致时如何推进，自己意见被反对时怎样处理？
13. 候选人做的 Backend Agent 与游戏内部 Agent 有什么不同？
14. 如果为具体游戏设计 Agent，会怎样拆 Goal、State、Action / Tool、Memory、Evaluation 与安全边界？
15. 是否真正玩过相关游戏，能否把技术方案映射到业务场景？

去重：一 / 二 / 三面与 Timeline 全部属于同一灵犀互娱流程，因此合并一个 `S319`。`S318` 虽是同一作者且都出现 `CR Agent`，但公司、招聘时间线、面试官和业务完全不同，按规则属于两个独立真人命中。各 URL 与题序均未在 `S001–S308` 入库。

---

# 本批清洗与研究观察

本批正式新增：**11 个 HUMAN-A（S309–S319）**。

## 典型排除 / 去重

- **某中厂 Agent 应用开发实习候选页**：初筛时第一人称与问题密度看起来合格，但最终复核阶段正文连续无法稳定打开，只能依赖搜索摘要。按“搜索摘要不能代替稳定正文”规则，最终撤出本批，不占编号。
- **卓驭 Agent、自变量 Agent 平台、平安银行 AI 开发、浦发 AI 开发等 `赛文X / 100+ 社招面经记录` 内容链**：单页表面像真人面经，但作者 / 合集链具有批量多公司内容生产特征，全部零贡献。
- **蚂蚁若干不同账号同序 Agent 帖**：Memory / Agent Team / MySQL / Redis / MQ 等题序高度重合，无法可靠确认独立原场，继续整链排除。
- **9/8 快手一面（Skill / Memory / 项目真实性追问）**：现场痕迹很强，但页面无法稳定证明具体招聘岗位属于目标 AI Application / Agent Role Scope，不因出现 Skill / Memory 就越过岗位 Gate。
- **BIGO Java Backend**：同一真实候选人的 Agent 项目被深挖，信息质量高，但招聘岗位本身仍是普通 Java Backend，缺乏足够证据证明岗位职责属于目标 Role Scope，本批不收。
- **去哪儿 AI 自动面试**：问题再贴 Agent 也不是人类面试官，继续零贡献。
- **AIGC小白入门记、RockyDing、WeThinkIn、Yuka 完整答案等内容 / 付费 / 二次整理页**：继续排除。
- **快手 `S318` 三轮**：明确同作者、同公司、同 `CR Agent`、连续 8/26 → 9/1 → 9/9，只计一个来源。
- **灵犀互娱 `S319` 三轮 + Timeline**：明确同一招聘流程，只计一个来源；但与同作者的快手 `S318` 属于不同公司流程，分别计数。

## 本批新增信号

1. **Tool Calling 正从“模型会调工具”升级为协议 / Runtime 本质题。** 启云方连续追问：Tool 是否注册、模型返回的是 Text 还是 Structured Call、JSON 字段在哪里、真正执行者到底是 Model 还是 Agent Loop，并要求手画 `Agent Loop → Model → Tool → Filesystem`。这类题需要把协议数据结构与执行控制面讲清楚。
2. **RAG 面试开始大量使用“反例验真”。** 字节问“小摘要为什么反而降低 Recall”、标题-only Embedding 为什么合理；中兴直接挑战 512 Token 分流设计是否形成检索闭环；小鹏用“充分必要条件被 Chunk 切开”测试候选人是否真正理解 Semantic Boundary。
3. **Skill vs Tool 不再停留在名词区别。** 面试官会继续追 Skill 能否覆盖 Function Call、所谓“替代”实际替代的是能力描述 / Procedure 还是确定性 Executor，以及 Progressive Disclosure 在 Context 层如何实现。
4. **Agent Backend 的传统工程权重仍然极高。** 腾讯和杭州小厂明确是 Agent 开发岗，但一面可大量甚至几乎全部考 Java / Spring / MySQL / Redis / Kafka / Network；滴滴 AI Agent Backend 更把 Spring、Redis、Go GMP、Service Discovery、GC 与 Agent Memory 放在同一轮次链路中。
5. **Context Engineering 正向“信息结构与生命周期”靠拢。** ReAct 上一轮结果怎么传、哪些内容应该单独存、哪些能进入下一轮、陌生代码库两个月后需求再次演进怎样恢复历史知识，都比“Context 太长怎么办”更具体。
6. **AI Coding 开始考长期软件维护，而不只是现场生成代码。** OPPO 直接追陌生 Repo 的 0→1 上手以及旧需求两个月后演进；中兴追“除了 Cursor 你自己会不会写”；快手二面会评价 Coding 过程与工程表达，而不仅看最终 AC。
7. **业务 Agent 与 Domain Knowledge 的融合更明显。** 灵犀互娱要求把 Backend Agent 与 Game Agent 区分，并让候选人现场设计游戏 Agent；说明业务状态、动作空间、限制条件和 Evaluation 需要与 Agent Architecture 一起准备。
8. **多轮招聘流程是更强的 Provenance 证据。** 快手 8/26→9/1→9/9 和灵犀 8/31→9/2→9/7→9/8 意向都能沿同一作者时间线闭环；这种来源可信度显著高于孤立的标准化题单。
9. **稳定正文仍是硬门槛。** 本轮即使已在初筛中准备收录，最终发现正文只能依赖摘要，也会撤掉；“找到过”不等于“可正式归档”。

## 饱和判断

**仍未达到来源饱和，但已经进入高去重、高 Provenance 核验成本阶段。** 在 `S001–S308` 全历史重新直接回读后，本轮仍确认 11 个独立 HUMAN-A，并且出现 Tool Call Runtime 本质、RAG 反例验真、长期代码维护、游戏 Agent Domain Design 等新增信号。说明精确作者 / 公司 / 轮次搜索仍有增量；但泛搜索里内容账号、答案版、自动面、同序改写和不稳定正文占比继续升高，后续仍应坚持“少而真”。

下一条正式来源从 **`S320`** 开始。
