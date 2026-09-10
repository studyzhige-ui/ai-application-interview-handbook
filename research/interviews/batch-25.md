# Batch 25 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S370` 继续编号。搜索继续执行**热门公司优先 + 高搜索量 + 8～9 月最新层 / 3～7 月长尾 + 作者 Timeline**，并按本轮要求主动扩大平台覆盖：除牛客外，系统搜索小红书、知乎、脉脉、个人博客、独立站、技术社区与公开索引。**平台不设配额，也不降低准入门槛**；索引、搜索摘要、转载和答案整理只用于发现原帖，不能直接贡献题目。
>
> 分配编号前已重新直接回读 `batch-01.md` ～ `batch-24.md`，覆盖 `S001–S369` 全历史；对最终候选逐项执行 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、5～10 个连续独特题序和招聘 Timeline 去重。GitHub Code Search 的 0 命中仅作辅助。本轮再次实际发现“新页面看似真人，但连续题序可追到 2025 年其它作者旧面经”的情况，因此仍以直接历史回读和外部复制链核验为最终依据。
>
> HUMAN-A Gate 不变：**真人面试官 + 候选人本人第一人称 + 高技术密度 + 强现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非答案帖 / 非 AI 自动面试 / 非重复 = HUMAN-A**。通过 Role Scope 后保留整场真实技术问题，不因为某场主要考 React、Redis、MySQL、GC 或 TCP 就只摘 AI 名词。
>
> 本轮最终放行 **4 个独立 HUMAN-A（S370–S373）**。虽然主动扩大了非牛客平台搜索，但本批没有任何非牛客页面通过最终 Gate：小红书原帖常只能取得标题 / 索引或与已收来源形成跨平台同序链；知乎、脉脉、博客和独立站当前高召回结果主要是课程、题库、答案扩写、转载或“学员面经”整理。没有为了平台多样性硬收低可验证来源。

---

## S370 字节跳动中国交易与广告·生活服务｜Agent 开发 / Agent 工程师池（前端画像）｜一面｜面试 / 发布 2026-06-08，一面已过｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b75d87aac5a74076b3a28c692f2f6d3c

真人 / 第一人称证据：作者 `自在极意前端嘉豪` 为东南大学前端候选人，正文先交代自己正在初创公司实习、因 HR 说明岗位是新开的 HC 且侧重前端与 AI Coding 而接面。面试按 0–10min 项目、10–15min React Hook、15–40min Coding、40–50min JS 基础记录，保留“Hook 链表实现答不了”“版本比较 O(1) 思路对但没有写出来”等现场状态。作者在评论区当晚更新“一面过，还有两轮技术一轮 HR”。反问阶段 HR 进一步明确：前端 / 后端 / 客户端进入同一个大池子，**统一按 Agent 工程师招聘，再根据简历技术栈提问**；因此虽然本场问题明显偏前端，Role Scope 仍由招聘流程直接确认。

整场技术问题：

1. 项目深挖：当前项目做了什么，本人负责什么，怎样说明真实产出？
2. React Hook 使用时需要注意哪些规则？
3. 为什么 Hook 不能放在条件语句中调用？
4. 能否手写一段类似 Hook 链表的数据结构 / 执行机制，解释条件调用为什么会破坏顺序？候选人现场未写出。
5. Coding：比较两个版本号。
6. 在上一题基础上要求 `O(1)` 额外空间完成版本号比较；候选人想到逐段转数字，但现场没有完整写出。
7. JavaScript 有哪些基本数据类型？
8. JavaScript 中判断数据类型有哪些方式？
9. 为什么 `typeof null === "object"`？
10. 反问 / 招聘：Agent 工程师大池如何按候选人背景分配前端、后端、客户端和 AI Coding / Agent 能力的考察权重？

去重：已直接回读 `S001–S369`，当前 URL、作者与 6/8 生活服务流程均未入库；“Agent 工程师统一大池招聘 → React Hook 条件调用 / 链表实现 → O(1) 版本比较 → JS 类型”的连续题序未在历史来源形成同场重复。外部继续搜索作者 Timeline，只找到其明确更新一面通过、后续仍有两轮技术面；未找到可稳定核验的同公司后续轮次原帖，因此本批只收当前一面，未来若发现同流程后续轮次应合并而非新增 ID。

---

## S371 阿里千问｜Agent 开发｜日常实习一面｜发布 2026-03-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/41b996517ec140bbaf27889bf06b0db0

真人 / 第一人称证据：作者 `lazy_learner` 的账号可串起数月个人求职 Timeline，持续参与多家公司实习 / 春招讨论，并非批量面经或订阅内容账号。本帖明确为“阿里千问 Agent 开发一面-日常实习”，从论文、实习、项目自然进入 Retrieval / Embedding / Rerank / GraphRAG / Multimodal，再现场手写带 Mask 的 Multi-Head Attention 和 RoPE；作者保留“MHA 只写了个大致思路”的现场完成状态，评论区也有同岗位候选人围绕手撕难度互动。

整场技术问题：

1. 论文深挖：研究问题、方法和本人真实贡献是什么？
2. 实习深挖：真实负责的工作、上下游和难点是什么？
3. 项目深挖：系统目标、技术路线和本人实现边界是什么？
4. Retrieval 是否使用 Embedding，具体使用什么 Embedding Model？
5. Embedding Model 本身通常怎样训练，训练目标是什么？
6. BGE Reranker 精排模型与 Embedding Model 的作用和推理方式有什么区别？
7. GraphRAG 与普通 RAG 的核心差异是什么，各适合什么场景？
8. 多模态系统中的 Schema / 数据组织怎样理解？
9. Coding / 模型实现：手写带 Mask 的 Multi-Head Attention；候选人现场只写出大致思路。
10. Coding / 模型实现：手写 RoPE / Rotary Positional Embedding。

去重：已直接回读全部历史 Batch，并对“论文 / 实习 / 项目 → Embedding 训练 → BGE Reranker vs Embedding → GraphRAG → Multimodal Schema → MHA with Mask → RoPE”连续题序做外部精确检索，仅定位到当前原帖，未发现更早同序来源或跨平台镜像。该作者另有腾讯 AI 后台等不同公司流程；不同公司招聘流程独立，不与本来源合并。

---

## S372 腾讯｜AI 后台开发｜暑期实习一面｜发布 2026-04-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/184f5a028eb646d480400001efe721ea

真人 / 第一人称证据：作者同为 `lazy_learner`，但这是与 `S371` 不同公司的独立招聘流程。本帖标题明确为“腾讯暑期实习 AI 后台开发一面面经分享”，开头写“努力拥抱 AI 中”，问题按现场 Coding → 实习 / 项目 → 压测 / Cache → MySQL / Redis → JVM / Network 的顺序展开，并在评论区继续讨论压测和 HotKey。虽然本场几乎没有 Agent / RAG 名词，但岗位本身明确为 AI Backend，按 Role Scope Gate 通过；因此真实出现的 Backend Foundation 全部保留。

整场技术问题：

1. Coding：Merge K Sorted Lists / 合并 K 个有序链表。
2. 实习经历深挖。
3. 项目的整体 Architecture 与 Request Chain 是什么，Cache 放在哪一层？
4. 项目怎样做 Load / Stress Test，真实压测指标是什么？
5. 是否遇到过 HotKey，怎样发现和治理？
6. Bloom Filter 的基本原理、解决什么问题、主要缺点是什么？
7. Bloom Filter 存在 False Positive，误判率怎样设定 / 估算并与空间成本权衡？
8. Cache 与 Database 的 Dual-write Consistency 怎样保证？
9. Redis Distributed Lock 的基本原理是什么？
10. MySQL 中实际存哪些数据，项目是否需要 Sharding / 分库分表？
11. Redis 有哪些常用数据结构，项目实际用了哪些？
12. MySQL Clustered Index 与 Non-clustered Index 有什么区别？
13. Back-to-table、SQL Optimization 与 `EXPLAIN` 怎样结合排查？
14. Java Garbage Collection 的基本机制与常见算法是什么？
15. HashMap / Hash Table 底层原理是什么，JDK 1.8 之后有什么关键改进？
16. MySQL Transaction Isolation Level 有哪些？
17. InnoDB 默认隔离级别下如何处理 Phantom Read？
18. TCP 三次握手和四次挥手怎样工作？
19. 如何看待 AI 与程序员的关系，AI Coding 会怎样改变日常研发？

去重：已直接回读 `S001–S369`，URL 和本场题序未入库；外部连续题序检索未发现更早同序来源。需要特别区分：同作者 4/6 另有一篇“腾讯 AI 后端开发”短帖，其“慢查询 → Redis 为什么快 → 缓存雪崩 → 几十亿 int 去重”连续题序可追到 2025 年另一作者腾讯 IEG 后端面经，已判复制链并排除；**本来源只使用 4/2 这篇独立、完整且未发现复制源的原帖**。

---

## S373 京东科技｜AI 全栈 Agent 研发｜一面｜发布 2026-06-11，等待结果｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e80b257b1c064970a72c9679c2177585

真人 / 第一人称证据：作者 `猫猫不会分布式` 发布时身份显示为美团 Java 开发实习员工，后续公开互动中又显示为小红书 Search PE 产品工程师实习员工，账号持续参与本人求职 / 笔试 / 面试讨论，符合个人候选人 Timeline。正文明确为“京东科技 AI 全栈 Agent 研发一面”，从部门介绍和实习项目验真进入 MySQL、Redis、Kafka、突发流量，再切到 Agent frontier、Bad Case、Evaluation、Tool Context 与 Tool 数量膨胀。作者保留“Tool Context 太长没有回答好、面试官给了前沿 Agent 设计建议”以及反问面试表现、当前仍等待结果等现场痕迹。

整场技术问题：

1. 部门 / 岗位业务介绍后，实习项目的真实背景、本人职责和关键技术点是什么？
2. 实习中处理过哪些 Slow SQL，具体怎样定位和优化？
3. 一张表刚创建时查询正常、数据增长后逐渐变慢，可能是什么原因，怎样排查？
4. UUID 为什么通常不适合作为 InnoDB Primary Key / Clustered Index？
5. Redis 为什么常被描述为单线程执行命令，它为什么仍然很快？
6. Redis Cache 与数据库之间怎样保证 Data Consistency？
7. Kafka 相比其它 MQ 有什么优势？
8. 实习中 Kafka Partition Count 怎样设置，为什么这样设置？
9. Kafka Message Backlog / 积压出现时怎样定位和处理？
10. 服务遭遇未预料的突发流量峰值时，怎样限流、削峰、扩容和保护下游？
11. 最近关注哪些 Frontier Agent / Agent Engineering 进展？
12. 实习中的 Agent Bad Case 怎样发现、归因和修复？
13. Agent Performance / Effect 怎样量化，使用哪些指标和 Evaluation 方法？
14. Tool Call 返回的 Context 太长时怎样压缩、引用或延迟加载，同时避免丢失任务关键事实？候选人现场未答好，面试官进一步讨论前沿设计。
15. 当 Tool List 持续膨胀时，怎样优化 Tool Discovery / Selection，而不是把所有 Schema 一次性塞入 Context？
16. 候选人在 Agent 方向相比普通后端候选人的优势是什么？
17. 反问 / 反馈：面试官如何评价候选人在 Backend 与 Agent 两方面的表现，当前流程进度如何？

去重：已直接回读 `S001–S369`。历史京东来源虽已有 AI Application / Agent 样本，但当前作者、6/11 京东科技流程和“Slow SQL 随数据增长 → UUID 主键 → Kafka Partition / Backlog → 突发流量 → Agent Bad Case / Evaluation → Tool Context 过长 → Tool List 膨胀”的连续链均独立。对 URL、作者与罕见题序做外部回查未发现更早复制源或同公司后续轮次原帖。

---

## 本批观察

1. **平台覆盖扩大，不等于平台配额。** 本轮主动搜索小红书、知乎、脉脉、个人博客、独立站等；最终非牛客零新增，原因不是没搜，而是当前召回结果多为标题 / 索引不可稳定回原文、跨平台镜像、课程题库、答案扩写或学员整理。平台稀缺不能成为降 HUMAN-A 门槛的理由。
2. **Agent Engineer 正在吞并传统端侧 / 后端边界。** 字节 `S370` 的招聘方明确把前端、后端、客户端放入统一 Agent 工程师池，再根据简历技术栈考察；因此真实 Agent 岗可能出现 React / JS 等端侧基础，而非只问 RAG / MCP。
3. **AI Backend 的基础工程权重仍然非常高。** 腾讯 `S372` 几乎整场是 Redis / MySQL / GC / TCP；京东 `S373` 同时考 MySQL、Redis、Kafka、流量治理与 Agent Evaluation / Tool Context。这进一步说明课程与面试准备不能把“AI 应用工程”理解成只会框架 API。
4. **模型 / Retrieval 深度仍会出现在 Agent Application 岗。** 阿里千问 `S371` 直接追 Embedding Training、BGE Reranker、GraphRAG，并要求手写 MHA + Mask 与 RoPE，说明部分团队会把模型机制追到实现层。
5. **复制链需要跨年份追。** 本轮 `lazy_learner` 4/6 腾讯短帖表面上满足公司 / 岗位 / 第一人称，但罕见连续题序可追到 2025 年另一作者的腾讯 IEG 后端面经，因此整条短帖撤出；URL 新和作者真人都不足以证明该场独立。
6. **热门结果页继续饱和，但 3～6 月长尾仍有增量。** 本批 4 条全部来自 3～6 月，而 8～9 月最新层大部分被历史命中、内容账号、付费答案或复制链过滤。下一轮需要继续加大历史长尾和个人 Timeline 比例。

## 典型排除

- 小红书公开索引中的“淘天 AI Agent 一面问麻了”等标题：只能稳定取得索引 / 标题，且罕见题序与历史 `S095` 高度同构；索引仅作导航，零贡献。
- 知乎 / 脉脉 / 个人博客与独立站的多条 2026 Agent 面试结果：主要是课程、题库、面试指南、学员复盘或转载扩写，不能证明候选人本人原场，零贡献。
- `lazy_learner` 4/6 腾讯 AI 后端短帖：连续题序几乎逐题命中 2025 年另一作者腾讯 IEG 后端一面，按复制链排除；不影响对同作者 4/2 独立原帖的单独核验。
- 百度广告投放 / 大模型应用一组高密度页面：岗位内容强，但作者 Timeline 对同一轮日期出现 8/05 与 8/18 冲突，无法稳定解释，按 Timeline 冲突排除。
- 9 月美团 / 快手 / PDD 等多条由同类账号发布的精致“真人叙事 + 60% 付费 / 答案”页面：账号长期批量覆盖多家公司，按内容账号 / 付费答案包装排除。
- 小米 Agent 三面等页面：来自同类批量内容账号且正文大比例付费，无法完整核验原场，零贡献。
