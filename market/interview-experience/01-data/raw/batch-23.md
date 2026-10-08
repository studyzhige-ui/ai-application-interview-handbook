# Batch 23 一手面试流程

采集日期：2026-09-10

## S267 小红书｜PE 全栈（AI 全链路方向）｜一面 35min｜发布 2026-03-31｜HUMAN-A

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

## S268 小红书｜PE 工程师·AI 与全栈方向｜技术面｜面试 2026-07-03，发布 07-09｜HUMAN-A

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

去重：已直接回读 `S001–S266`。本场“AI 改造已有系统 → Cache → 多实例 Access/Refresh Token → Refresh Latency → 并发刷新 / 异常边界 → In-place Coding”的长场景链未在历史小红书来源出现；Role Scope 由岗位标题和面试方向明确支持。

---

## S269 字节跳动抖音电商 / 中国交易与广告｜AI 开发 / 全栈开发｜一面 50min｜面试 2026-08-24｜HUMAN-A

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

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

