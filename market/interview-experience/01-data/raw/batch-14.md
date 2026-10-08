# Batch 14 一手面试流程

采集日期：2026-09-10

## S213 九号公司｜Agent 开发实习｜一面｜发布 2026-08-31，约 90min，已 OC｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c0b53fdd38e041d2bc779753d04ee2ce

真人 / 第一人称证据：作者与 `S042 / S077` 同属一个可核验候选人时间线，但九号是独立公司流程。作者记录约 90 分钟面试、项目深挖和当前 OC 状态，面试官不断追问真实业务指标、团队分工与失败案例，现场结构明显区别于标准题单。

高价值问题：

1. 实习 Agent 的真实业务目标、上下游、团队分工和本人职责是什么？
2. LangGraph 自动拆题里每个 Node 的输入 / 输出和完整数据流是什么？
3. 项目宣称提高效率，具体提升了多少、怎样测，原先人工痛点是什么？
4. OCR 批处理失败时怎样恢复，识别质量怎样优化？
5. 候选人本人是否参与数据清洗 / 模型训练，项目边界在哪里？
6. 电商 Agent 如何做订单自动处理和任务编排？
7. “准确率 90%+”的数据来源是什么，剩余 10% 是哪些 Failure Case？
8. Tool Registry 为什么拆接口 / 能力 / 实现层，Dynamic Loading 怎样工作？
9. 长任务如何形成闭环并把反馈 / 交付状态返回给用户？
10. PI Agent、DeepSeek Harness 分别怎样理解；Agent 岗为什么仍强调工程能力？

去重：URL 与九号公司招聘流程未在旧 Batch 出现；同作者其它公司面试属于独立流程，分别计数。

---

## S214 字节跳动中国交易与广告｜后端日常实习（实际面试主体为 Agent / Harness）｜一面 + 二面 + 三面 + HR，已书面 Offer｜2026-06-17 / 06-22 / 06-24｜HUMAN-A

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

去重：已直接回读 `S001–S266`。历史虽有多条字节中国交易与广告来源，但当前作者、6 月完整三轮 Timeline 和“Agent / Harness → Skill Resource Loading → 三层 Memory → Context Compression / Checkpoint → 重复 Tool Failure → Java / Index / Cache / TCP → 二面 Persona Initialization / SSE / Evaluation → 三面 Goal-oriented Outcome + 两个 System Design”的连续链均独立。三轮属于同一候选人同一招聘流程，合并为一个来源。

---

## S215 快手｜AI 全栈开发工程师｜秋招一面｜面试 2026-08-25，发布 08-26｜HUMAN-A

来源：https://www.nowcoder.com/discuss/921807075905130496

真人 / 第一人称证据：作者 `小妞脂` 明确给出公司、8 月 25 日、AI 全栈岗位；现场先深挖个人项目和实习业务，再要求 `O(N)` 的第 K 大，候选人记录自己先想到最小堆、后来才切到 Quickselect 思路，并进行 AI Coding 页面开发。作者还写到面试官认为其表达不够清晰，现场痕迹明确。

高价值问题：

1. 做两个个人项目的驱动力是什么，过程中遇到哪些困难？
2. 实习主要负责哪个业务，能否讲清完整业务链和本人职责？
3. 开发过程中怎样使用 AI，什么才算高质量 AI-assisted Development？
4. 公司内部如何管理 AI 工具、规范和研发流程？
5. Coding：数组第 K 大，要求平均 `O(N)`，为什么 Heap 不满足要求，Quickselect 怎样处理？
6. AI Coding：现场实现“满一定金额赠送赠品”的页面 / 功能，如何从需求到可验收结果？
7. 实习项目如何讲清楚而不是只描述技术名词，表达本身怎样影响项目验真？

去重：与 `S216`、`S228` 均为不同作者、不同日期和不同流程；本场以“实习业务验真 + O(N) Kth Largest + AI Coding 页面”为独立题序，不因同公司 / 同岗位错误合并。

---

## S216 快手｜AI 应用开发｜秋招一面｜发布 2026-08-20，50min｜HUMAN-A

来源：https://www.nowcoder.com/discuss/919948330229071872

真人 / 第一人称证据：作者明确写出公司、`AI应用开发` 岗位和 50 分钟时长；项目追问连续 7～8 问，并直接写“麻了”。后半段从线程池追到 OOM / Java Memory Model，再做现场算法和反问；评论区继续围绕结果、项目来源、算法与 Vibe Coding 流程讨论。

高价值问题：

1. 为什么业务需要当前功能，项目真实价值是什么？
2. 当前功能最难的工程问题有哪些，怎样解决？
3. 不从业务而从技术资源角度，Thread Pool 参数应怎样配置？
4. 使用 Thread Pool 时有哪些常见风险和注意事项？
5. 为什么不直接使用 `Executors` 提供的默认线程池？
6. 自定义线程池时线程数量如何确定，依据哪些 CPU / I/O 特征？
7. 什么情况会导致 OOM，怎样定位？
8. Java Memory Model 怎样理解？
9. Coding：给定多个区间，计算互不重叠区间数量。
10. 反问：校招生最需要补哪些能力，当前面试表现最明显的问题是什么？

去重：历史已有多场快手 AI Application，但本作者、50min 流程、项目 7～8 连续追问及“线程池技术参数 → OOM → JMM → 区间 Coding”题序均不同，确认为独立候选人流程。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

