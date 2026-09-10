# Batch 24 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S366` 继续编号，执行一轮新的**热门公司优先 + 高搜索量 + 8～9 月最新层 / 3～7 月长尾双线 + 作者 Timeline**搜索。搜索覆盖字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO / vivo / 小米等，并交叉使用 AI Application、Agent、RAG、AI Backend、AI Full-stack、Coding Agent、Harness / Runtime、Applied AI / FDE 等岗位别名。
>
> 分配编号前已重新直接回读 `batch-01.md` ～ `batch-23.md`，覆盖当前正式基线 `S001–S365`；对最终候选逐项执行 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、5～10 个连续独特题序和招聘 Timeline 去重。**GitHub Code Search / 搜索引擎 0 命中仍不能证明未收录。** 本轮就实际出现了多个“Code Search 0 命中、但历史正文明确已收录”的候选，因此一律以直接历史回读为准。
>
> HUMAN-A Gate 不变：**真人面试官 + 候选人本人第一人称 + 高技术密度 + 强现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非答案帖 / 非 AI 自动面试 / 非重复 = HUMAN-A**。同一候选人同一公司同一招聘流程的多轮必须合并；同一候选人不同公司 / BU 且招聘流程独立时可以分别计数。
>
> 本轮最终只放行 **4 个独立 HUMAN-A（S366–S369）**。没有为了数量补样本：热门结果页中历史重复、内容账号、付费 / 答案包装、后发复制链和 Role Scope 模糊页面占比继续很高；真正新增主要来自作者 Timeline 和此前未覆盖的独立流程。

---

## S366 阿里云｜Agent Infra（Data Infra）｜秋招一面 + AI Coding｜面试 2026-08-31，发布 09-01｜HUMAN-A

来源：https://www.nowcoder.com/discuss/924245733962719232

真人 / 第一人称证据：作者 `Florentino_73` 以本人面试 Timeline 连续记录求职过程，本帖明确写出 `8.31 阿里云 Agent Infra 一面`。整场先约 30 分钟自我介绍 / 项目与蚂蚁实习深挖，再做系统场景、现场递归 Coding，反问时确认团队主要做 Agent Infra 的 Data Infra，包括数据处理、状态持久化与 post-train；随后还有约 120 分钟 AI Coding。作者账号存在长期个人求职 / 实习记录，不是批量面经内容账号。

整场技术问题：

1. 自我介绍和项目介绍，重点深挖蚂蚁实习经历。
2. 只有一台 Intel SGX 机器时，如何面向多租户提供计算服务，并处理单用户约 1GB 数据？
3. EPC 资源只有约 512MB、计算数据需要不断切入 / 切出 EPC 时，怎样保证这个过程中的安全性？
4. 用户数据量 / PV 变为原来的 4 倍，但系统吞吐量没有提升，可能有哪些原因？
5. 上述场景可能遇到哪些瓶颈？
6. Coding：按规则解析嵌套编码字符串，例如 `3[ab2[c]]`，现场使用递归实现。
7. 反问：团队主要做 Agent Infra 的 Data Infra，包括数据处理、状态持久化与 post-train 等。
8. AI Coding：实现一套从阿里云 SLS 动态写入 MySQL 的系统，并考虑各种异常情况。

去重：已直接回读 `S001–S365`。当前 URL、作者的 8/31 阿里云流程以及“SGX 多租户 / EPC 换入换出 → 4×PV 吞吐不涨 → 嵌套串 Coding → Agent Infra Data Infra → SLS→MySQL 120min AI Coding”连续题序均未在历史正式来源中出现。另检索到后发的阿里云 Agent Infra 扩写 / 题解页面，只作为复制链信号，不计来源。

---

## S367 阿里淘天｜AI 应用研发｜秋招一面 + AI Coding｜面试 2026-08-26，发布 08-27｜HUMAN-A

来源：https://www.nowcoder.com/discuss/922452114809376768

真人 / 第一人称证据：同为作者 `Florentino_73` 的本人求职记录，但这是 8 月 26 日淘天 AI 应用研发独立面试，和 8 月 31 日阿里云 Agent Infra 属于不同组织 / 岗位与独立招聘流程，因此不合并。正文记录约 30 分钟项目深挖、5 分钟业务数据结构题、约 30 分钟 AI Coding，并在反问中确认业务重点是把平台商家与用户场景 Agent 化，Role Scope 明确。

整场技术问题：

1. 约 30 分钟自我介绍和项目介绍，主要深挖华为项目中的模型调优与 RAG 相关问题。
2. 某个 URL 一秒内涌入大量需求，但系统只能处理 100 个时，适合使用什么数据结构？
3. 需要实时维护商品销量 Top 10，适合使用什么数据结构？
4. AI Coding：实现商品计价系统，优惠策略需要能够随时更新，例如会员价、满减等。
5. 围绕平时使用 AI Coding 的心得和实际遇到的问题继续交流。
6. 反问：团队主要把平台商家与用户场景做 Agent 化。

去重：已直接回读 `S001–S365`。历史阿里 / 淘天 AI Application 来源很多，但没有当前作者的 8/26 流程和“华为模型调优 / RAG → 单 URL 高并发容量 → 实时商品 Top10 → 动态优惠商品计价 AI Coding”连续题序。同作者 8/31 阿里云为独立招聘流程，按规则分别计数。

---

## S368 字节跳动抖音｜Agent 开发｜秋招一面｜面试 2026-08-14，08-16 未通过，发布 08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7189761b1a954e9b80765acb988c96bf

真人 / 第一人称证据：候选人明确写“秋招岗位，8 月 14 号面的，8 月 16 号上午接到通知说是没过”，保留完整面试结果与面后难度感受。问题从本人实习 / 项目验真进入状态机扩展、安全攻防、高流量在线统计、Aerospike / Redis，再到 Vibe Coding 分布式限流 System Design，题序自然且技术密度高。

整场技术问题：

1. 实习经历中遇到过最具挑战的问题是什么？
2. 已介绍项目整体流程后，继续展开其中具体的技术实现细节。
3. 业务状态机不断扩展到 20 多种甚至更多状态时，怎样设计和维护？
4. SSRF 漏洞是什么，产生原因是什么？
5. CSRF 是什么，它与 SSRF 最大的区别是什么？
6. 给出一个真实 CSRF 攻击场景。
7. 为什么 CSRF 请求能够携带用户 Cookie，浏览器在其中扮演什么角色？
8. 常见 CSRF 防御方案有哪些，各自适合什么场景？
9. AI 异步生成场景每分钟产生大量任务时，如何实时统计每个任务平均耗时的变化趋势，同时避免把全部数据存入内存？
10. 大规模实时指标计算有哪些常见数据结构 / 算法可以降低内存压力？
11. Aerospike 与 Redis 有哪些区别？
12. Aerospike 的数据存储和读写机制怎样实现？
13. Redis 与 Aerospike 分别适合哪些业务场景，怎样选型？
14. Vibe Coding：设计一套 Distributed Rate Limiter 的整体架构。
15. 分布式限流中怎样处理一致性、性能和故障问题？

去重：已直接回读 `S001–S365`。URL、8/14 抖音 Agent 流程和“状态机扩展 → SSRF / CSRF → 大规模在线耗时趋势 → Aerospike / Redis → Vibe Coding 分布式限流”连续题序均未在历史正式来源出现。作者更早的其它字节页面中存在与历史其它公司高度同序的复制风险，本来源单独按当前独特题序与明确招聘 Timeline 验证，不从那些不确定页面引入任何问题。

---

## S369 字节跳动安全与风控｜后端研发实习生（AI Agent）｜一面｜发布 2026-04-26｜HUMAN-A

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

去重：已直接回读 `S001–S365`。作者 4 月还存在快手等其它公司独立求职流程，其中部分已在历史库；本场是字节安全与风控独立流程，不与不同公司合并。当前 URL 和“Hybrid Retrieval / RRF → Vector DB → OpenClaw Context → HTTPS / TCP → Redis Persistence → GIL → 链表 / Singleton”连续题序未在正式来源中形成同场重复。

---

## 本批观察

1. **热门结果页的局部饱和进一步加深。** 新 URL 很多，但大量候选最终是历史正式来源、后发答案 / 扩写、内容账号、同候选人同流程后续轮次或不确定复制链。
2. **Code Search 0 命中不能证明未收录。** 本轮多个强候选在仓库搜索中显示 0 命中，但直接历史回读仍能定位到已收录 URL / 题序；因此继续坚持“先全历史正文，再分配编号”。
3. **AI Coding 正从附加题变成独立工程验证。** 本批同时出现约 30 分钟商品计价系统、约 120 分钟 SLS→MySQL 动态写入系统和 Vibe Coding 分布式限流，重点明显不只在传统 LeetCode。
4. **Agent / AI Backend 与系统工程底座继续强耦合。** SGX / EPC、多租户、安全、流式指标、Aerospike / Redis、TCP、Redis Persistence、Python GIL 与 RAG / Context / Agent Infra 同场出现。
5. **热门公司全年真人来源尚未整体饱和。** 8 月仍能发现未收录的独立大厂流程，3～7 月长尾也继续补到字节安全与风控样本；但 Provenance / 去重成本已经明显高于单纯搜索成本。

## 典型排除

- 阿里 Token Foundry 8/17 → 8/24 → 9/3 三轮：看似新强候选，GitHub Code Search 0 命中，但直接历史回读确认就是已收录 `S148`，零新增。
- 字节 TikTok AI Agent 8/9：Code Search 0 命中，但直接历史回读确认已在早期 Batch 收录，零新增。
- 小红书 Agent 服务端 9/8：搜索末段一度看起来是最新真人强候选，但再次对历史正文后确认与历史 `S033` 为同 URL / 同场，撤回，不分配新 ID。
- 拼多多同一候选人 8/23 → 8/25 → 8/31 多轮：后续页面属于同一候选人同一公司同一招聘流程，不能按轮次新增；历史文件不修改，本批零贡献。
- 7 月字节某 AI 应用页面：罕见连续题序与历史其它公司来源高度同构，复制链原始归属不能稳定确认，整链排除。
- 美团 / 阿里 / 快手若干高密度页面：作者主页表现为批量面经 / 答案 / 订阅内容生态，按“非内容账号”Gate 排除。
- 腾讯、OPPO / vivo / 小米等若干候选：正文不稳定、Role Scope 不明确、历史命中或只能取得搜索摘要，均不为公司覆盖率降低标准。