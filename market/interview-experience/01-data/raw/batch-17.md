# Batch 17 一手面试流程

采集日期：2026-09-10

## S231 OPPO｜IT 开发（实际纯 Agent）｜27 届秋招一面｜面试 2026-08-27，发布 09-02，已挂｜HUMAN-A

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

去重：已直接回读 `S001–S230`。URL 未入库；作者、8/27 OPPO 流程和“ReAct Runtime → 高德 MCP 设计 → Skill 渐进加载 → Word 图文 Context → Text-to-SQL 黑话 / Ontology → 新仓库演进”的连续题序均未发现历史同场或复制链。

---

## S232 腾讯｜后台 Agent 开发｜日常 / 实习一面｜发布 2026-04-29｜HUMAN-A

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

去重：URL 与作者流程未在 `S001–S230` 出现；“EasyExcel 10000 行 → 5000 行失败恢复”这一罕见项目题序经全历史直接回读和辅助检索均未命中。

---

## S233 成都某中厂（网络安全 / 自研 Agent 产品）｜Agent 产品开发实习｜一面｜面试 2026-06-15，发布 06-26｜HUMAN-A

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

## S234 杭州某小厂｜Agent 开发实习｜一面｜面试 2026-08-18，发布 08-20，先 OC 后流程中断｜HUMAN-A

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

## S235 阿里灵犀互娱｜交易支付·大模型应用开发｜秋招一面 + 二面 + 三面 / HR｜2026-08-31 / 09-02 / 09-07，09-08 意向｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/ff4827f42c5844b9967d6751d2e3b9b3

二面来源：https://www.nowcoder.com/feed/main/detail/c8935da5044a4376b9f45d2cc46ba469

三面来源：https://www.nowcoder.com/feed/main/detail/85a64d94c3374a10afa20d7466d24d5d

流程来源：https://www.nowcoder.com/feed/main/detail/f29afdc906bd47d9b3812fbc1ce3cf96

真人 / 第一人称证据：同样由 `27备战秋招` 发布，但这是与 `S114` 完全不同公司的独立招聘流程。作者给出完整 Timeline：8/31 15:00–16:00 一面、9/2 17:00–18:00 二面、9/7 11:00–12:00 三面 + HR 交叉面，9/8 收到意向书；HR 还反馈面试官认为其 AI / LLM 理解和工程实践较强。各轮持续围绕同一 `CR Agent`、Backend Engineering、Harness 与游戏 Agent 展开，合并计一个来源。

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

去重：一 / 二 / 三面与 Timeline 全部属于同一灵犀互娱流程，因此合并一个 `S235`。`S114` 虽是同一作者且都出现 `CR Agent`，但公司、招聘时间线、面试官和业务完全不同，按规则属于两个独立真人命中。各 URL 与题序均未在 `S001–S230` 入库。

---

