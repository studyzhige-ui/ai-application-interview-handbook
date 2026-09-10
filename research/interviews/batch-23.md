# Batch 23 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S361` 继续编号，延续 Batch 21 / 22 的**热门公司优先 + 高搜索量 + 最新层 / 3～7 月长尾双线 + 作者 Timeline**策略。本轮在收尾前重新直接回读 `batch-01.md` ～ `batch-22.md`，覆盖 `S001–S360` 全历史；随后对最终候选执行 URL、公司 / 岗位 / 日期 / 轮次、作者、项目语义、5～10 个独特题序与招聘 Timeline 去重。
>
> 正式来源标准不变：**真人面试官 + 候选人本人第一人称 + 高技术密度 + 强现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非答案帖 / 非 AI 自动面试 / 非重复 = HUMAN-A**。同一候选人同一公司同一招聘流程的多轮继续合并，不按轮次虚增样本。
>
> 本轮最终只放行 **5 个独立 HUMAN-A（S361–S365）**。数量下降不直接解释为来源饱和：Batch 21 / 22 在完整高搜索量周期分别新增 11 / 12 个，而 Batch 23 是对已经形成的候选池做收尾；同时本轮继续主动排除 Role Scope 模糊、内容账号、投稿 / 答案包装和来源链不稳定的热门公司页面。

---

## S361 字节跳动中国交易与广告｜后端日常实习（实际面试主体为 Agent / Harness）｜一面 + 二面 + 三面 + HR，已书面 Offer｜2026-06-17 / 06-22 / 06-24｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/ccba40c7281f4d9197b01fe9c140b13d

二面来源：https://www.nowcoder.com/feed/main/detail/3d3475963ac647c0ae7f43da487248ad

三面来源：https://www.nowcoder.com/feed/main/detail/7274018294c84a118e0854e64ea580aa

真人 / 第一人称证据：三个页面可由同一候选人 `喜羊羊吃草中` 的个人 Timeline 串成完整流程：6 月 17 日一面后约 4 小时收到二面通知，6 月 22 日二面后次日下午约三面，6 月 24 日三面，6 月 26 日推进 HR，6 月 29 日 HR 面，7 月 1 日收到书面 Offer。作者后续身份也显示为字节后端实习员工。虽然岗位标题是后端日常实习，但一、二面主体持续围绕候选人的 Agent / Harness / Memory / Skill / MCP / Evaluation 项目，面试官还明显弱化传统后端项目，因此按实际面试职责通过 AI Backend / Agent Role Scope。

整场技术问题：

### 一面

1. 候选人的 Agent 项目解决什么问题，与 Claude Code、Codex、Hermes 等现有 Coding Agent 的差异是什么？
2. Agent 的整体 Architecture 怎样拆，Harness Layer 为什么需要单独存在？
3. 为什么需要 Built-in Tools；模型怎样在多个 Tool 中稳定选到正确能力？
4. Tool 与 Skill 的职责边界是什么？
5. Skill 如何按需加载，而不是把全部能力一次性塞进 Context？
6. 一个 Skill 中的 Reference、Script、Asset 等资源怎样被发现、读取和执行？
7. Agent 每一轮怎样判断当前应加载哪个 Skill？
8. 三层 Memory 为什么这样分层，各层分别保存什么？
9. 一次 Agent Loop 发给模型的 Context 由哪些部分组成，拼装顺序和裁剪策略是什么？
10. Long Context 超窗后怎样 Compression；Checkpoint 在压缩、恢复和长任务中承担什么职责？
11. 最近若干轮对话如何压缩，同时避免把初始目标和关键约束压丢？
12. Tool 执行失败时如何把错误反馈给 Agent，而不直接破坏主循环？
13. 同一个失败 Tool 被模型连续重复调用时，Runtime 如何识别、限次、改路或终止？
14. Java 创建线程有哪些方式？Thread、Runnable、Callable 的关系和使用边界是什么？
15. ThreadPool `corePoolSize=4` 时一次进入 8 个任务，Queue 满后任务如何在核心线程、队列和非核心线程之间流转？
16. Producer / Consumer 并发模型怎样实现并避免线程安全问题？
17. Database Index 为什么能提高查询效率，索引真正优化的是什么？
18. 联合索引 `(A,B,C,D)` 面对 `A > 1 AND B = 0` 时怎样利用索引？
19. `SELECT *` 与只查询 `A,B,C` 对索引覆盖和回表有什么影响，索引应怎样调整？
20. Database 与 Cache 的数据一致性如何保证？
21. Hot Key / 热点 Cache 到期时怎样避免大量请求瞬间压向数据库？
22. TCP 连接已经建立后，A 端突然崩溃而 B 端继续发送数据，会发生什么，怎样感知对端失效？
23. Coding：有序数组中统计平方后不同值的个数，要求 `O(1)` 额外空间；候选人现场需要面试官引导继续优化。

### 二面

24. 项目是学校 / 个人项目还是生产项目，真正的使用者和价值是什么？
25. 当前 Agent 与 Codex / Claude Code 的核心差异是什么，哪些能力是自己真正实现的？
26. Hermes 等方案与“从零实现 Agent”在 Harness / Tool / Context 层有什么差异？
27. 项目代码主要手写还是 AI-assisted，候选人如何证明自己理解生成代码？
28. 与 AI 协作做需求时，怎样先完成 Persona / Role 初始化，再让模型理解项目本地约束？
29. Java 与 Python 用于 Agent / Backend 工程时如何取舍？
30. 项目中最困难的问题是什么，为什么难，最后怎样验证解决？
31. SSE 的通信方式和适用场景是什么？
32. 为什么当前 Streaming 不使用 WebSocket；SSE 与 WebSocket 在连接模型和协议层有什么差异？
33. RAG 在当前项目中解决什么问题，什么时候触发？
34. Skill、MCP、Tool、Function Calling 分别处于哪一层，各自解决什么问题？
35. Agent Evaluation 怎样自动化；如何判断一次 Agent / Harness 改动真的变好？
36. 为什么想做 LLM / Agent 方向，长期技术兴趣是什么？
37. Java HashMap 的数据结构、树化条件和 Resize 机制是什么？
38. ConcurrentHashMap 怎样实现并发安全？
39. ThreadLocal 的实现和 Memory Leak 风险是什么？
40. Redis Lua 脚本为什么适合库存扣减等原子业务？
41. Coding：判断一个数是否为 2 的幂；Longest Substring Without Repeating Characters。

### 三面

42. 竞赛 / 项目中最困难的工作是什么，候选人如何定义自己的贡献？
43. 当前 Agent 从零搭建时最独特的价值是什么，与其它 Agent 产品有什么差异？
44. 面试官要求给出更“Goal-oriented”的结果案例：怎样证明 Agent 最终解决了业务目标，而不是只做了技术模块？
45. 测试 Agent 的指标是否足以代表最终 Outcome；什么才算真正的目标达成？
46. System Design：设计一套世界杯比赛预测系统，数据、模型、服务和评测如何组织？
47. System Design：设计餐厅选址系统，怎样融合业务数据、约束和决策逻辑？
48. 过去两年遇到的最大困难和最有成就感的事是什么？
49. 自己的优势 / 短板如何影响未来工程工作？

去重：已直接回读 `S001–S360`。历史虽有多条字节中国交易与广告来源，但当前作者、6 月完整三轮 Timeline 和“Agent / Harness → Skill Resource Loading → 三层 Memory → Context Compression / Checkpoint → 重复 Tool Failure → Java / Index / Cache / TCP → 二面 Persona Initialization / SSE / Evaluation → 三面 Goal-oriented Outcome + 两个 System Design”的连续链均独立。三轮属于同一候选人同一招聘流程，合并为一个来源。

---

## S362 快手｜AI 应用服务端开发｜一面 + 二面 + 三面｜2026-08-26 / 09-01 / 09-09｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/1f6732ca32c74e17af502c71e77c8c59

二面来源：https://www.nowcoder.com/feed/main/detail/2892c62d66b24268959644260a7d7044

三面来源：https://www.nowcoder.com/feed/main/detail/ef8b41f126664ff2879337d43889a4ee

真人 / 第一人称证据：三篇均由候选人 `27备战秋招` 发布，个人主页是可连续核验的本人求职 Timeline，并明确记录快手 `AI应用服务端`：8 月 26 日一面、9 月 1 日二面、9 月 9 日三面。作者在二面保留“Coding 虽做出但过程不好、感觉面试官态度变化”“SDD 被继续挑战”等现场状态；三面又记录面试官交流体感、到岗时间和其它 Offer，属于连续真人招聘流程而非题单整理。

整场技术问题：

### 一面

1. CR Agent 项目的业务背景、完整链路和本人职责是什么？
2. Agent-to-Agent / A2A 与 MCP 分别解决什么问题，如何配合？
3. Java 常见 Design Pattern 在当前工程里怎样实际使用？
4. SDD / Spec-driven Development 怎样理解，怎样约束 AI Coding 或 Agent 开发？
5. Coding：现场算法实现与复杂度说明。
6. 日常写代码有多少使用 AI，形成了怎样的 AI-assisted Development 习惯？

### 二面

7. 继续深挖 CR Agent：真正的技术难点和业务价值是什么？
8. 微软实习中的 Backend 工作是什么，哪些能力能迁移到 Agent Service？
9. Coding：现场完成算法题；候选人自评最终写出，但过程不够顺畅。
10. SDD 在真实项目中具体怎样落地，为什么面试官会继续挑战方案细节？
11. 如何证明 Spec / Test / Review 确实约束了 AI 生成结果，而不是只加了一份文档？

### 三面

12. CR Agent 为什么需要 Distributed Architecture？
13. 多 Agent 之间怎样通信，Agent-to-Agent Message / State 应怎样组织？
14. 某个 Agent / Service 执行失败后，系统怎样保证整体 Stability 和恢复能力？
15. Redis Lua 如果封装了过多业务逻辑，会带来什么维护、演进和可测试性问题？
16. Coding：两道基础算法现场实现。
17. 反问 / 招聘：团队业务方向、候选人的业务兴趣、其它 Offer 和春节后实习到岗时间。

去重：已直接回读所有历史快手来源。本场独特的“CR Agent → A2A / MCP → Java Design Pattern → SDD → 二面微软 Backend + SDD 追问 → 三面 Distributed Agent / A2A Communication / Failure Stability / Lua 业务逻辑膨胀”的连续流程未在历史样本出现；三轮同作者同公司同岗位，主动合并。

---

## S363 小红书｜PE 全栈（AI 全链路方向）｜一面 35min｜发布 2026-03-31｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ca5c689da55241a184b39ed4b8f04e63

真人 / 第一人称证据：候选人明确记录 35 分钟一面，其中约 15 分钟项目、约 20 分钟围绕“怎样用 Agent 优化 / 重构项目”深挖；无手撕，作者多次记录“不会、被问蒙、第一次被问这么深”等现场状态。反问时面试官解释 PE Full-stack 是结合 AI 做全链路开发，因此实际职责明确通过 AI Full-stack Role Scope。

整场技术问题：

1. 项目整体做什么，是否真实有用户 / 落地，还是只做了压测？
2. Bloom Filter 怎样治理 Cache Penetration？
3. 如果攻击者通过 Botnet 大量生成不存在的商品 ID，Bloom Filter False Positive 和后端压力应怎样处理？
4. APT / Annotation Processing Tool Framework 在项目里怎样使用？
5. 为什么该框架能带来约数量级的性能提升，具体优化点是什么？
6. 怎样通过 JMeter / QPS 等证据证明瓶颈和收益确实来自当前 Framework，而不是其它变量？
7. Nested Loop / Nested Cycle 等实现为什么可能成为性能问题？
8. Recursive Mapping 怎样设计并控制复杂度？
9. 怎样通过 APT Plugin / Decorator 统一 Logging 和 Error Collection？
10. 前端页面是否大量由 AI 生成；候选人自己真正负责什么？
11. AI Frontend Engineering 与“让模型随便生成一个页面”有什么差异？
12. 普通 Demo Page 与可维护的 Production Frontend 在工程上差在哪里？
13. AI 在真实工程中的主要限制是什么，哪些工作必须人工兜底？
14. 过去参加前端训练 / 项目时如何使用 AI 辅助开发？
15. 如果把当前电商系统 MCP 化，Server、Tool、权限和业务接口怎样拆？
16. 用户画像 / 搜索推荐数据应该继续放 MySQL，还是引入 Vector DB，怎样取舍？
17. PostgreSQL Horizontal Scaling 与 `pgvector` 怎样组合，什么时候会成为瓶颈？
18. PostgreSQL 同时承载 Vector 与 Graph-like Relationship 是否合适，边界在哪里？
19. Embedding Layer 怎样设计，数据何时生成、更新和检索？
20. Agent 是否应该直接读取数据库，还是应通过受控 Tool / Service Layer 访问？
21. Agent 调用外部能力有哪些方式？
22. Function Calling 的完整机制是什么？
23. Skill 与 MCP 的边界是什么，各自适合封装哪类能力？

去重：历史小红书 AI Full-stack / Agent 场次很多，但当前“APT 性能验真 → AI Frontend Engineering → 电商系统 MCP 化 → PostgreSQL / pgvector / Graph → Embedding Layer → Agent 是否直读 DB → Function Calling / Skill / MCP”连续题序、作者和 3 月流程均未出现。

---

## S364 小红书｜PE 工程师·AI 与全栈方向｜技术面｜面试 2026-07-03，发布 07-09｜HUMAN-A

来源：https://www.nowcoder.com/discuss/904825433772806144

真人 / 第一人称证据：标题和公司明确标注 `PE工程师-AI与全栈方向`；候选人按本人 7 月 3 日面试复盘发布。技术主体不是题库，而是从已有系统优化进入一个长 System Design：第三方 Access Token / Refresh Token 在多实例并发下如何缓存、刷新和处理异常，面试官持续针对边界条件追问；作者明确记录该部分被问得很深、方案不断被挑战。

整场技术问题：

1. 过去实习 / 项目中本人真正负责什么，最有代表性的系统是什么？
2. 如果给现有系统引入 AI，应优先改造哪里，为什么？
3. 当前 System Design 中最浪费研发时间、最影响效率的环节是什么，AI 能怎样帮助？
4. Cache 的基本设计、失效和一致性需要考虑什么？
5. System Design：第三方 API 的 Access Token 会过期，需要调用 Refresh Token 接口刷新；在多实例服务中如何设计 Token Cache 与 Refresh 机制？
6. Refresh HTTP Call 本身存在 Latency 时，怎样避免大量并发请求同时阻塞或重复刷新？
7. 多个实例同时发现 Token 过期时，如何避免 Refresh Stampede，并保证所有实例最终拿到一致的新 Token？
8. 如果刷新过程中请求失败、返回旧 Token、实例崩溃或锁超时，怎样恢复？
9. Token 快过期和已经过期两种状态是否应采用不同策略？
10. 面试官连续增加异常 Case 后，怎样证明方案具备可用性，而不是只覆盖 Happy Path？
11. Coding：原地移除数组中所有等于给定值的元素，并把剩余元素紧凑排列。

去重：已直接回读 `S001–S360`。本场“AI 改造已有系统 → Cache → 多实例 Access/Refresh Token → Refresh Latency → 并发刷新 / 异常边界 → In-place Coding”的长场景链未在历史小红书来源出现；Role Scope 由岗位标题和面试方向明确支持。

---

## S365 字节跳动抖音电商 / 中国交易与广告｜AI 开发 / 全栈开发｜一面 50min｜面试 2026-08-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6dede073825e4ab493fcbce7f598a6c8

真人 / 第一人称证据：作者 `BCZMJ` 以本人 8 月 24 日、约 50 分钟 `AI 开发 / 全栈开发` 一面复盘发布，正文保留基础题遗忘、算法在面试官提示后才推进、实现中发生 Overflow 等现场状态。问题从个人 Multi-Agent 项目一路进入 Memory / Context、HTTPS / Certificate、OS / Memory 与 Coding，属于目标 AI Full-stack 的完整工程能力样本。

整场技术问题：

1. 项目最有意思的部分是什么，为什么做这个项目？
2. 项目的完整运行流程怎样组织，关键 Architecture 为什么这样设计？
3. 为什么不用 LangChain 等现成 Framework，而选择当前实现？
4. 为什么 Attack Detection / 安全判断不直接交给 LLM，确定性逻辑与模型的边界怎样划分？
5. 为什么多个 Agent 之间没有直接通过 Network Service 通信？
6. 多 Agent 当前怎样交互、传递 State 和结果？
7. Agent Memory 怎样管理？
8. Context Window 有什么限制，超限后怎样处理？
9. Model 是自部署还是调用外部服务，怎样选择？
10. HTTPS 为什么能保证传输机密性与完整性？
11. Root Certificate / CA 在 TLS Trust Chain 中承担什么职责？
12. Process 与 Thread 的区别是什么？
13. 为什么 Thread 通常比 Process 更轻量？
14. OS 创建 Process 时会为它分配 / 建立哪些资源和地址空间？
15. Stack / Heap 在 Process 与 Thread 之间分别怎样共享或隔离？
16. 只有 1GB Physical Memory 时能否打开 / 处理 2GB File，Virtual Memory 怎样参与？
17. 如果系统关闭 Swap，上述场景又会怎样变化？
18. Coding：寻找序列中的“第一个不同数字”类问题，先讨论 Time / Space Complexity，再继续优化实现。
19. 算法过程中候选人需要面试官提示，并在实现阶段遇到 Integer Overflow；应怎样识别边界并修正？

去重：URL、作者和 8/24 AI 全栈流程未在历史库出现；“Multi-Agent Communication → Memory / Context → HTTPS Root CA → Process / Thread Resources → 1GB Memory vs 2GB File / No Swap → Coding Hint + Overflow”连续题序独立。

---

## Batch 23 最终校验中的典型排除 / 合并

- **字节中国交易与广告三轮主动合并。** `喜羊羊吃草中` 的一面、二面、三面以及个人 Timeline 能形成 6/17 → 6/22 → 6/24 → HR → 7/1 书面 Offer 的完整链，统一归入 `S361`，不按轮次拆号。
- **快手 AI 应用服务端三轮主动合并。** `27备战秋招` 的个人 Timeline 明确给出 8/26 一面、9/1 二面、9/9 三面，统一归入 `S362`。
- **字节 8/23 中国交易与广告高密度候选因 Role Scope 模糊排除。** 虽然候选人的 Agent 项目被问得很深，但页面无法稳定证明岗位本身属于 AI Application / Agent，而非普通后端仅深挖候选人 AI 项目，因此不收。
- **阿里国际“朋友 / 小伙伴投稿 + 完整答案”页面排除。** 不满足候选人本人第一人称，并带答案包装，零贡献。
- **淘天等批量多公司面经账号继续按内容账号风险排除。** 即使题目看起来完整，也不因为热门公司或题量大降低 Gate。
- **小红书普通 PE / 后端仅偶发问 Agent 的页面排除。** 只有能够明确确认 `AI+全栈` 或实际职责主体属于 AI Application 的场次才进入本批。
- **快手父子索引 / BM25 / Rerank 长链继续排除。** 已出现多个日期 / URL 的高度同序版本，原始归属不可靠，不猜原场。
- **9 月热门结果页历史命中继续增多。** 小红书 9/8 已是历史 `S199`、美团 9/2 已是 `S198`、京东 4/10 已是 `S337` 等，均不重复计数。

## Batch 23 现实信号 / 饱和度复核

1. **本批 5 个不能直接解释为整体饱和。** 本轮是对已形成候选池做收尾，不是一个完整的新高搜索量周期；Batch 21 / 22 在完整扩量搜索下仍分别新增 11 / 12 个。
2. **热门公司最新结果页继续局部饱和。** 9 月泛关键词搜索中历史命中、内容账号、答案版和 Role Scope 模糊页面占比继续上升。
3. **作者 Timeline 的价值继续高。** 字节和快手都通过作者主页把分散的多轮页面合并成一个真实招聘流程，既提高 Recall，又防止按轮次虚增来源。
4. **Agent / Harness 面试继续向 Runtime 细节下沉。** Skill Resource Loading、三层 Memory、Context Compaction / Checkpoint、重复 Tool Failure 控制和自动 Evaluation 已经进入热门公司面试。
5. **AI Full-stack 的边界正在扩大。** 小红书开始把 Frontend Engineering、MCP、PostgreSQL / pgvector、Embedding、Agent 数据访问和分布式 Token Refresh 放在同一个岗位中考察。
6. **Backend Foundation 仍是硬门槛。** 字节在 Agent 项目后继续问 Java ThreadPool、Database Index、Cache Consistency、TCP、HTTPS / Root CA、Process / Thread、Virtual Memory / Swap。
7. **Role Scope 校验的重要性继续上升。** 热门公司普通后端面试也可能深挖候选人的 Agent 项目；只有岗位职责或整场主体能明确落入目标 AI Application / Agent 范围，才进入正式库。

## 本批统计

- 新增 HUMAN-A：**5 个**
- 编号范围：`S361–S365`
- 累计 HUMAN-A：**365 个**
- 当前最大编号：`S365`
- 下一条正式来源：**`S366`**
- Inbox：归档后为空
- 饱和度判断：**热门结果页局部饱和；热门公司全年真人来源整体尚不能判定饱和。下一轮继续用高搜索量同时跑最新层、3～7 月长尾和作者 Timeline。**