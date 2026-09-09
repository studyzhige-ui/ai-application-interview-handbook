# Batch 01 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 正式样本采用统一固定标准，与平台无关：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 牛客、小红书、知乎、脉脉、技术社区、视频平台等都可以成为来源，但任何平台都不能降低准入门槛。
>
> 本文件只保存来源元数据、真人/第一人称证据与问题的简洁转述，不复制第三方正文。

---

## S001 阿里云｜Agent 开发｜一面｜2026-08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/42ba29ab006d4bb793112eb263d18f6a

真人 / 第一人称证据：作者明确记录自己被再次捞起后参加 Agent 开发面试，描述面试结果，并记录现场 AI Coding。

高价值问题：

1. 平时如何使用 AI 辅助编码，是否形成稳定工作流？
2. 常用 Skill 有哪些，不同 Skill 的结构和职责有什么差异？
3. 是否自己写过 Skill，设计 Skill 时最需要约束什么？
4. 对近期 Agent 产品的理解到什么程度？
5. Claude Code 与其他 Harness 产品在系统设计上有什么区别？
6. 是否真正读过成熟 Agent / Harness 源码？
7. 一个可靠 Harness 至少需要哪些核心能力？
8. Agent Tool Calling 有哪些实现方式？
9. 如何保证大量 Tool 按需发现、按需调用，而不是全部塞入 Context？
10. 为什么需要 Sub-agent，什么任务才值得拆成 Agent？
11. Agent 间通信如何组织？
12. 从零设计 Agent Loop 时需要考虑哪些 Runtime 问题？

---

## S002 字节跳动 TikTok｜AI Agent 开发｜秋招一面｜2026-08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7b1b40fda3244715a82bcb4a821ca887

真人 / 第一人称证据：候选人明确记录面试日期、现场互动感受和后续等待状态。

高价值问题：

1. 会议转写从音视频输入到文本、摘要的完整工程链路是什么？
2. ASR 服务为什么这样选，识别准确率如何评估与优化？
3. 实时音视频中的用户隐私数据如何保护？
4. 系统为什么采用中心化或去中心化架构？
5. RAG Chunk Size / Chunk Strategy 如何根据数据和评测确定？
6. Tokenization 为什么会把一个词拆成多个 Token？为什么 LLM 使用 Token 而不是字符 / 单词？
7. Transformer / QKV / Attention 的核心过程如何解释到应用工程需要的深度？
8. Lost in the Middle 为什么发生，长 Context 为什么不是越大越好？
9. Context Window 的能力边界由什么决定？
10. SFT / PPO / DPO / GRPO 等方法分别解决什么问题，应用工程师需要理解到什么程度？
11. 为什么选 Multi-Agent，为什么还需要中心化编排？
12. 数据结构 Coding：List → Tree、Zig-zag Tree Traversal。

---

## S003 影石创新｜AI Agent｜一面｜2026-08-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b406c87436a54864bfc0cf4a20299f62

真人 / 第一人称证据：作者明确写出面试日期、次日得知失败，并逐题记录现场问题。

高价值问题：

1. Spec Coding 与 Harness 如何理解，Harness 为什么能提升复杂任务完成能力？
2. 从零设计 Agent 系统需要哪些模块？
3. Tool / API 超时、异常应该由 Runtime 如何分类、重试、降级？
4. 是否应该让 LLM 参与错误分析和自动恢复？模型与确定性 Runtime 的边界在哪里？
5. 短期 / 长期 Memory 如何设计？
6. Context 为什么需要压缩，压缩后的信息损失如何检测与恢复？
7. Prompt 优化除了增加规则约束还能做什么？
8. Agent 幻觉与 Token 消耗异常如何定位？
9. 一个 Skill 从设计、上线到效果验证的生命周期是什么？
10. Java 线程池如何运行，如果重新设计线程池会考虑哪些约束？
11. MySQL undo / redo / binlog 分别做什么？
12. redo log 与 binlog 的两阶段提交为什么需要存在？

---

## S004 小红书｜大模型平台 Agentic 全栈研发｜一面｜2026-08-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e5e9311a623940eead6ec98c65e7f9e8

真人 / 第一人称证据：候选人明确记录面试日期、结果、面试官引导与反问讨论，并指出自己没有答好的具体问题。

高价值问题：

1. Agent 在真实研发业务里到底解决什么问题，为什么不是普通客服 / Workflow？
2. Agent 的写操作边界如何划分？
3. Harness 层包含哪些职责？
4. 编排层如何重构，节点 / 边 / 状态如何组织？
5. 意图分流如何保证清晰，怎么识别 Query 是模糊还是明确？
6. Skill 和 Tool 的职责区别是什么？Skill 何时 Fetch / Load？
7. 不同基础模型表现不一致时，应用层如何做适配与稳定性治理？
8. 5000～6000 用户、十几万日请求量下 Agent 服务如何扩容？
9. 为什么选择 SQLite 或其他存储，什么时候需要迁移到更完整的数据层？
10. 为什么自研 Agent Runtime，而不是直接使用 LangGraph 等框架？
11. HashMap、MySQL B+Tree、联合索引等基础如何解释？
12. RAG / Vector Knowledge Base 在真实业务里如何做技术选型？

---

## S005 字节跳动｜AI 应用开发｜一面 + 二面｜2026-05-12 / 05-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/61aa7e8d56ca4eb4a5a873512a72d616

真人 / 第一人称证据：作者记录 HR 联系、一面后约二面、二面后结果，并描述面试官对项目技术价值的反馈和 Coding 测试现场讨论。

高价值问题：

1. 实际数据库优化做了什么，数据量多大，是否分库分表？
2. MySQL 索引何时失效，为什么“用了索引”仍可能很慢？
3. B+Tree 为什么适合索引？慢查询如何定位？
4. Redis 高可用 / 高性能如何通过主从、Sentinel、Cluster 实现？
5. Redis 与 MySQL 如何在同一业务里分层使用？
6. Vibe Coding、Skill 和其他 AI 编程范式如何理解？
7. 二面为什么继续追项目的业务价值，而不是只问实现？
8. 实际索引优化为何能带来性能提升，如何证明不是偶然？
9. 回表查询、顺序 I/O 与随机 I/O 的关系是什么？
10. Coding：实现一个有最大容量的 Blocking Queue，并处理并发正确性。

---

## S006 阿里国际 / Lazada｜Agent 开发暑期实习｜一面｜2026-04-22｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/40ef1dff3eac4d5ba86bc78372376be3

真人 / 第一人称证据：候选人后续实际入职，并明确记录一面、二面、HR 面时间线以及入职后确认面试官身份的经历。

高价值问题：

1. 磁盘如何存储信息，应用工程师需要理解哪些存储基础？
2. 进程与线程有什么区别？
3. Transformer 原理和 Multi-Head Attention 如何解释？
4. 实习 IM 项目中本人真正负责了什么？
5. Agent 客服项目为什么需要 RAG，完整回答生成链路如何实现？
6. 对 LangGraph 做过哪些真实改造，而不是只调用框架？
7. Agent Memory System 如何设计？
8. 为什么选择 Agent 开发方向，如何把既有后端 / 系统经验迁移过来？

---

## S007 唯品会｜Agent 开发｜社招一面｜2026-08-28 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/64c0631bfa1d4dfa9be3d5956f8a3b97

真人 / 第一人称证据：作者以个人社招面试记录形式发布，问题围绕自己的生产故障、项目规模、历史重构与团队推动展开。

高价值问题：

1. 最近一次线上故障如何定位与处理？
2. 设计一个测试 Agent，真正需要交付哪些能力和验收指标？
3. Agent 的 DAU、数据量、任务量如何影响架构？
4. Agent 自动任务分配与调用链如何设计？
5. Agent 失败时如何兜底？Leader Agent 挂掉后 Multi-Agent 怎么恢复？
6. MCP 框架如何选，Transport Protocol 如何选？
7. Agent Bad Case 如何 Debug？
8. Text-to-SQL 的边界与风险是什么？
9. gRPC / tRPC、服务发现、负载均衡如何支撑 Agent Backend？
10. GMP / GC STW 等 Runtime 基础为什么在 AI Backend 仍然重要？
11. 回滚、A/B Test、流量分桶和统计显著性如何用于 AI 功能发布？
12. 异步队列如何防止消息丢失？

---

## S008 字节跳动抖音基础架构｜Agent 开发｜一面 90min｜2026-04-09 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/91c5394e57c14927841d7a86bfe427c2

真人 / 第一人称证据：作者明确记录 90 分钟一面和问题顺序，内容围绕自己的实习和项目逐层展开。

高价值问题：

1. Prompt Template 如何构建？
2. 为什么使用 Single Agent / Multi-Agent，Sub-agent 分别承担什么任务？
3. 代码生成系统如何统计 Branch Coverage，Code Instrumentation 如何实现？
4. AST / LSP 无法覆盖的代码如何提前识别和过滤？
5. Mock 如何实现，如何影响 AI 生成测试的有效性？
6. 多维 Query Rewrite 与需要用户补充信息的查询如何实现？
7. Intent Classification 为什么需要并行化？
8. Retrieval Pipeline 如何实现？
9. Context Engineering / To-do List 为什么能帮助模型聚焦？
10. Skill 的原理和实现是什么？
11. Self-Attention / QKV 为什么这样设计？
12. Python GIL、Lock / RLock、Semaphore 的机制与使用场景？

---

## S009 蚂蚁国际｜Agent 开发｜一面｜2026-05-09 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1f6e9337fb534f8c81326e3b55001e49

真人 / 第一人称证据：候选人以个人“凉经”形式记录同岗真人一面，问题围绕自己的实习、项目、笔试交互和交付流程展开。

高价值问题：

1. 从 AI 写代码到真正上线交付，完整流程应该怎样组织？
2. 前后端 + 中间件 + AI 的完整系统架构如何讲清楚？
3. 多应用 / 多仓库需求变更时，AI 如何跨系统完成修改？
4. 项目真实用了多少 Token，成本如何度量？
5. 如何降低 Token 成本？
6. SDD / TDD 如何与 Agent Coding 结合？
7. Skill 有哪些创建方式和组织形态？
8. Function Calling 的完整机制是什么？
9. Function Calling 与 MCP 的职责边界是什么？
10. MCP Client / Server 有哪些通信方式，如何配置？
11. Tool Schema 如何告诉模型有哪些工具可用？
12. 如何验证 AI 写出的代码真的正确，而不是“模型说完成了”？

---

## S010 小红书｜AI 后端开发｜一面｜2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/169b2d8f7a134843b114b820ee692186

真人 / 第一人称证据：作者明确记录面试日期、75 分钟连续追问、自己的现场感受和反问得到的评价。

高价值问题：

1. LRU 为什么使用 HashMap + 双向链表，还有哪些缓存淘汰策略？
2. 秒杀系统的主要风险如何分层解决？
3. RocketMQ Transaction Message 在一致性里做什么？
4. Redis Lua 为什么能保证单实例脚本原子执行？
5. Redis → MQ → MySQL 如何处理最终一致性？
6. Redis Set / ZSet 底层结构和复杂度是什么？
7. MySQL MVCC / Isolation Level 如何联系起来？
8. 联合索引、范围查询、回表、B+Tree 为什么这样设计？
9. 大 Offset 深分页为什么慢，优化后为什么真的变快？
10. 一个完整 Agent 需要哪些模块？
11. Memory 什么时候写、什么时候读、一次读多少？
12. RAG 如何评估，召回 / 回答效果差时如何优化？

---

## S011 美团零食杂售｜AI 后端开发｜一面｜2026-09-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/9b94f595d15148869e0334029b5ddb67

真人 / 第一人称证据：候选人明确记录部门、岗位、面试日期，并描述自己被追问卡住的具体问题和等待结果状态。

高价值问题：

1. 实习项目迁移 / 改造如何证明正确性？
2. Agent 项目本人做了什么？
3. RAG 如何落地？
4. Tool Registry 为什么采用 Singleton，生命周期应该如何管理？
5. MySQL Slow Query 如何定位？
6. 什么情况下 Optimizer 可能放弃索引走 Full Table Scan？
7. 常见 Index Invalidation 场景有哪些？
8. 支付重复请求如何设计 Idempotency？
9. AI Coding：根据少量需求直接实现订单详情页面，如何补足验收标准？
10. Coding：Top-K / 第 K 大并限制复杂度。

---

## S012 启云方｜AI Agent 开发｜一面｜2026-09-03 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fea2d18bd59a421da7d16fe16223d38c

真人 / 第一人称证据：作者记录真人面试节奏，先进行问答，随后围绕执行流程图继续讨论约 40 分钟，存在明显连续追问链。

高价值问题：

1. “自然语言调用 Tool”从协议层到底是什么意思？
2. Tool 是否需要预注册，注册时需要哪些 Schema / Metadata？
3. Tool Selection 是关键词、意图分类还是模型推理？
4. 模型决定调用 Tool 后，Tool Call 信息到底出现在什么消息 / 字段里？
5. Tool Call 是普通文本解析，还是独立结构化输出？
6. Assistant Text 与 Tool Call 是否属于不同数据块？
7. 真正执行外部动作的是模型，还是 Agent Loop / Tool Runtime？
8. Function Calling 的“模型生成请求”和“Runtime 执行”如何分层？
9. 手画：Agent Loop + Model + Tool + Filesystem 接到“写一个贪吃蛇游戏”后，完整执行链路是什么？

---

## S013 字节跳动 App Infra｜Agent 开发｜秋招一面｜2026-08-26 发布｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0bec32fbb3344ff98f16b97f47c7b857

真人 / 第一人称证据：候选人记录面试官岗位介绍、项目追问、多个“答得含糊 / 没答上”的现场状态以及面后对二面的判断。

高价值问题：

1. KV Cache 为什么能加速 LLM 推理？
2. 浏览器点击到服务端返回，一次请求经历哪些网络层？
3. TCP 为什么三次握手 / 四次挥手，四次是否总是必要？
4. MySQL 为什么用 B+Tree，Leftmost Prefix 如何工作？
5. Redis Cache Penetration / Breakdown / Avalanche 如何治理？
6. 多机器如何生成 Unique ID？若还要求近似单调 / 自增怎么办？
7. 这些基础设施能力为什么会成为 App Infra Agent 开发的一面核心？
8. Coding：基础排序实现。

---

## 本批观察

- Harness / Tool / Skill 已经进入 Runtime 与源码理解层面。
- MySQL、Redis、MQ、网络、并发仍是 AI Application / Agent 岗的重要底座。
- LLM Foundation 需要掌握应用工程深度，包括 Token、Attention、Long Context、KV Cache 等。
- 新增来源的价值主要是校准真实问法与优先级，而不是无限扩张学习题库。