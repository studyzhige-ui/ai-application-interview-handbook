# Batch 05 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 本批继续严格执行统一准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 搜索方式不依赖单一泛关键词，而是继续组合公司、岗位别名、月份与技术关键词，并沿企业页、话题页、作者页、精确标题与跨页面索引回溯原帖。本轮重点补 2026 年 3–9 月历史缺口与 9 月近期新增内容。
>
> 问题均为研究所需的简洁转述，不复制第三方正文。低质量线索、合集、标准答案、AI 自动面试、非本人投稿、岗位越界和无法稳定核验的内容均不贡献任何问题。

---

## S075 阿里控股｜AI 全栈开发｜二面 / Leader 面｜发布 2026-09-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a11a3a9e0d824969b44db5bb2149ef9f

真人 / 第一人称证据：作者以本人二面记录发布，结尾明确评价“Leader 面问得很细”；问题围绕自己的动态 Agent 工作流平台连续追问，并追到真实业务量、Token、RPC 延迟、失败回退和大规模业务统一等 Production 细节。

高价值问题：

1. 动态 Agent Workflow 平台如何实现，需求进入后哪些步骤由 Agent 自主完成？
2. 大模型首次生成代码错误时，整体流程是否中断，怎样回退、重试和恢复？
3. 如何验证模型宣称“已执行”的动作真的发生，避免执行幻觉？
4. RAG / Knowledge Layer 如何对模型输出做事实锚定与约束？
5. 为什么采用 Multi-Agent，而不是全部用 CLI / Script；Agent 间如何交互？
6. Workflow 的确定性编排与模型自由决策如何划分边界？
7. 非预设 Skill 如何从对话和执行轨迹中沉淀，小模型如何评价“绕路”与质量？
8. 如何用 Token、请求量、长时间运行等真实指标衡量 Agent 平台规模？
9. 数千个业务的 Agent 流程如何抽象、合并并控制重构后的正交性与冗余？
10. Model RPC 延迟较高时，同步 / 异步调用链如何设计，异步 Runtime 如何选型？

---

## S076 字节跳动｜Agent 开发｜秋招一面｜面试 2026-09-03，发布 09-04｜HUMAN-A

来源：https://www.nowcoder.com/discuss/925342611194286080

真人 / 第一人称证据：作者明确给出 9 月 3 日一面，按项目、八股、算法顺序记录，并写“发面经攒人品”；问题绑定本人 AI 项目，包含长任务突然变慢、Tool 参数可靠性与 Context 压缩信息损失等现场场景题。

高价值问题：

1. AI 项目中的结构化评分如何设计字段和维度？
2. RAG 的离线上传与在线问答链路分别如何实现？
3. Agent Harness 应如何理解，它与模型和 Agent Logic 的边界是什么？
4. 一个通常 5 分钟完成的长任务突然运行 15–20 分钟，应如何定位延迟来源？
5. 长任务延迟异常可以从模型、Tool、网络、队列、上下文和循环次数哪些层面治理？
6. Tool 入参固定但由模型结合上下文生成时，Runtime 如何保障调用可靠性？
7. 对话轮次不断增长导致 Context Window 膨胀时如何治理？
8. Summary / Compaction 必然损失信息时，怎样最小化关键事实、约束和任务状态的丢失？
9. Coding：给定数字集合，构造小于目标整数的最大可表示数字。

---

## S077 深信服｜Agent 开发实习生｜一面 + 二面｜发布 2026-09-02｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/14b2c379ae434062a009aefea9fc5df9

真人 / 第一人称证据：作者完整记录两轮，明确面试官介绍岗位包含 AI Agent 平台、Harness 工程工具和 Agent 数据分析；二面后被告知通过、等待 HR，随后收到感谢信，并详细描述本人对这一结果的感受和时间线。

高价值问题：

1. Agent Tool 数量过多、接口上百时，如何解决 Tool Discovery 与 Selection 问题？
2. Agent 的准确率 / 端到端效果如何定义并构建评测？
3. 一个业务 Agent 的用户目标、数据流、处理链和最终效果如何完整说明？
4. AI Coding 在生产代码中如何形成可验证的方法论和质量保障流程？
5. 动态 Tool Registry 如何实现注册、动态注入与运行时更新？
6. 自研 Tool 调用体系与 MCP、LangChain Tools / Skills 的差异是什么？
7. 上百个 Tool 中如何让模型稳定找到正确接口，Tool Retrieval 如何实现？
8. 当前 Tool 都无法完成任务时，Agent 应如何扩展能力或安全失败？
9. 自研 Multi-Agent Framework 与 AutoGen / CrewAI 等框架如何比较？
10. Coding：最长无重复子串。

---

## S078 拼多多｜Agent 开发｜二面｜面试 2026-08-25，发布 09-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f5e7351df8364147ac8da085b99d9d18

真人 / 第一人称证据：作者明确给出 8 月 25 日、40 分钟二面，记录自己的面试感想以及现场手撕；问题围绕真实 Agent 系统的任务隔离、结果正确性、评测与框架选型。

高价值问题：

1. Agent 如何隔离不同用户 / 不同任务的状态、文件和执行环境？
2. 如何保证 Agent 分析过程和最终输出尽可能正确？
3. Agent Evaluation 应覆盖哪些维度，测试用例如何构造？
4. 一个真实 Agent 业务的完整执行链路如何描述？
5. LangChain 与 LangGraph 的核心工程差异是什么？
6. 自研 Agent Framework 与开源框架相比，收益、代价和边界是什么？
7. Coding：设计线程安全的 LRU Cache。

---

## S079 蚂蚁财富技术部｜Agent / AI 应用方向｜秋招一面（电话面）｜发布 2026-08-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/02718e9f48ff436f96d6ee8c6f11a47e

真人 / 第一人称证据：候选人逐项记录约 1.5 小时电话面，问题围绕本人实习产出持续追问；末尾直接记录面试官对其“实习过程中的真实经验”的反馈，具有明显真人互动痕迹。

高价值问题：

1. 为什么某类 Agent Memory 用 Markdown / 文件而不是 RAG，记忆更新的语义匹配可靠性如何保证？
2. Agent Teams、主 Agent + Sub-agent 和固定 Workflow 应怎样取舍，各自缺点是什么？
3. 如果取消人工把关，如何让全自动 Agent 流水线达到可接受的交付可靠性？
4. MySQL ACID、B+Tree、MVCC 以及 redo / undo / binlog 分别如何工作？
5. Redis 缓存穿透、击穿、雪崩如何治理？
6. MQ 如何保证发送可靠性，并处理重复消费？
7. 限流、熔断、降级分别解决什么问题，常见限流算法如何选择？
8. 模型产生 Tool Call 的完整链路是什么？
9. Long-term / Short-term Memory、MCP、Agent 组成与 Harness 分别如何理解？
10. Temperature、Top-k、Top-p 如何影响生成，为什么 Temperature=0 仍不一定完全确定？
11. Prompt Injection 有哪些更确定性的工程防护，Skill Lazy Loading 如何设计？
12. Coding / 场景题：会议冲突判断与最少会议室数量。

---

## S080 平安健康保险｜AI 应用开发｜秋招一面｜面试 2026-08-23，发布 08-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/6c11a75a8bd44628943deff3e42ae15c

真人 / 第一人称证据：作者给出完整时间线：8 月 19 日投递、8 月 23 日面试、8 月 26 日收到感谢信，并写明自己的 Coding Agent 来源、27 分钟时长和反问内容。

高价值问题：

1. Agent Loop 的最小执行过程是什么？
2. Harness Engineering 与 Prompt / Agent Logic 的差异是什么？
3. 什么场景值得引入 Sub-agent？
4. 模型“偷懒”或提前宣称完成时如何治理？
5. Agent Hallucination 如何从 Runtime、Verification 和 Context 层控制？
6. 一个 Skill 的组成、适用场景和真实编写经验是什么？
7. SDD / Spec-driven Development 在 AI Coding 中解决什么问题？
8. 输入大量 PDF、最终输出 HTML 且需要 Knowledge Base 核验时，LLM Workflow 如何设计？
9. Coding Agent 能否 Self-bootstrap，如何区分真正自研与借助其他 Agent 完成？

---

## S081 虾皮｜Agent 开发｜一面｜面试 2026-08-20，发布 08-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/79fe3fc8f8cb4c4d9beca478f4279e3a

真人 / 第一人称证据：作者给出明确面试日期和目标岗位，以本人项目为起点按自然顺序记录 17 个问题，评论区继续围绕“楼主本场面试”讨论；问题没有标准答案包装，跨 Agent、RAG、Redis、MQ、MySQL 和 Coding。

高价值问题：

1. Single-Agent、Multi-Agent 与 Workflow 应按什么条件选型？
2. ReAct 中 Thought / Action / Observation 的职责是什么，Tool Message 为什么要单独建模？
3. Short-term / Long-term Memory 如何实现，哪些数据适合长期保存？
4. Context 超窗时 Sliding Window 与 Dynamic Summary 各有什么优缺点？
5. RAG 为什么使用父子索引，BM25 + Vector + Rerank 如何组合？
6. Knowledge Base 持续更新时如何处理向量索引、缓存失效和旧文档召回？
7. 多模态 Agent 中视觉编码结果如何与 LLM 融合？
8. Redis 在 Agent 中如何承担 Session、Semantic Cache、Distributed Lock，并设置合理过期策略？
9. MQ 为什么比“直接写数据库传任务状态”更适合部分 Agent 异步链路？
10. MySQL Composite Index 与 LIKE 查询在什么条件下能 / 不能使用索引？
11. Coding：反转单链表并分析复杂度。

---

## S082 MiniMax｜Agent Infra / 平台研发工程师｜秋招二面｜面试 2026-08-19，发布 08-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/362fd78c774b4e80813f48e1139b8230

真人 / 第一人称证据：候选人明确记录 8 月 19 日二面，描述面试官交流风格，并多次以自己的蚂蚁实习经历回答；结尾总结本轮更强调 Agent 底层设计、应用和产品化。

高价值问题：

1. Agent Infra 的运行周期 / 执行过程应如何 Observability，为什么有些产品不对外暴露？
2. 实习中最具设计价值的 Agent Infra 工作是什么，如何证明是本人核心贡献？
3. Agent Protocol 是否应该承载更多能力，协议边界如何决定？
4. 面向用户的平台侧如何把底层 Agent 能力产品化？
5. Agent Self-evolution 应如何实现并防止错误经验累积？
6. AI 时代工程师如何把一次项目经验沉淀为可复用的平台 / Harness 能力？
7. 如何从业务视角解释 Agent Infra，而不仅是描述底层技术组件？

---

## S083 字节跳动｜Agent 开发｜一面｜面试 2026-08-12，发布 08-24｜HUMAN-A

来源：https://www.nowcoder.com/discuss/921444774287003648

真人 / 第一人称证据：作者明确给出岗位、8 月 12 日面试和 1 小时以上时长；面试官让候选人在自己的三个项目中任选一个展开，并一路追问到 RAG、AI Coding、Streaming、数据库、并发场景和现场 Coding。

高价值问题：

1. 如何选择一个最能代表自己的 Agent 项目并讲清业务与技术价值？
2. RAG 项目经验如何展开说明，而不是只背 Pipeline？
3. AI Coding 如何保证生成代码质量，而不是只追求生成速度？
4. SSE 与 WebSocket 的协议特性和适用场景有什么区别？
5. 数据库常见索引结构与查询优化思路是什么？
6. 热点榜单实时更新且高并发时，数据结构和数据库如何选型？
7. Coding：两个栈实现队列，并继续追问如何实现线程安全。

---

## S084 快手｜AI Agent 开发｜一面｜面试 2026-07-20，发布 07-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8ef62dcdde1340f987507d2d1e1433a8

真人 / 第一人称证据：作者明确写出 7 月 20 日、AI Agent 开发、40 分钟，连续记录 25 个问题并以“发面经攒人品”结束；问题覆盖 RAG、Context、Memory、Tool Security、Rate Limit、Bloom Filter、MySQL Index 与 Evaluation。

高价值问题：

1. RAG 为什么引入父子索引和 BM25，Rerank 后 Top-K 如何确定？
2. Context Engineering 与 Memory 应怎样设计？
3. Function Calling 和 Agent Task Planning 如何实现？
4. Prompt Injection 与 Tool Calling Security 如何防护？
5. Distributed Token Bucket、Leaky Bucket、Sliding Window 的机制和适用场景如何比较？
6. Bloom Filter 的原理、误判和适用边界是什么？
7. MySQL Index Invalidation 与 LIKE 查询的索引行为如何判断？
8. RAG Evaluation 应包含哪些维度，评测集如何构建？
9. Retrieval Relevance 与最终 Answer Quality 分别如何系统优化？
10. 一千条数据求和等批处理任务应如何拆分、并发和汇总？
11. RAG 性能瓶颈可以从 Parsing、Retrieval、Rerank、Model 哪些层优化？
12. 当前 Context 如何存储、裁剪和更新？

---

## S085 快手｜Data Agent｜一面｜发布 2026-07-09｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c60afbadffaa427996767343c3f2049e

真人 / 第一人称证据：作者以本人“最奇怪的一次面试”复盘，详细记录自己告诉面试官没背 Java 八股后对方停止追问、两道 Easy 算法都不会、最后反问聊天半小时等强烈现场痕迹。

高价值问题：

1. 为什么要做 Mini-Claude / Coding Agent 类项目，真实目标是什么？
2. Context Engineering、Prompt Engineering、Harness Engineering 应如何区分？
3. Tool Layer 在 Agent 中承担什么职责？
4. Long-term / Short-term Memory 如何设计？
5. 实际遇到 Agent Hallucination 时如何定位并治理？
6. ReAct 范式如何运行？
7. Agent Dead Loop 如何检测、限制和恢复？
8. 权限控制与 Tool Failure Retry 如何设计？
9. 一个 Production Agent 最关键的系统组件有哪些？
10. Sub-agent 在什么任务中值得使用？
11. Coding：股票买卖问题。

---

## S086 美团｜大模型应用开发｜一面｜发布 2026-03-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/7855c8b9c1d040e188660dacbf7533c1

真人 / 第一人称证据：作者以本人“大模型应用开发一面、喜提人才库”发布并写“攒人品”；问题围绕自己的 AI 项目持续追问 Embedding、Function Calling、Memory、Vector DB、Async Response，同时进入 Redis 与并发控制。

高价值问题：

1. Embedding Vector Retrieval 的基本原理是什么，怎样提升检索准确性？
2. Function Calling 如何从自然语言中解析意图并生成结构化调用？
3. 对话 Memory 如何保存，超过容量后怎样裁剪 / 总结，Prompt 是否变化？
4. 原始文本如何切分、Embedding 并导入 Vector DB，Chunk 依据是什么？
5. 非阻塞响应如何实现，异步链路需要哪些 Runtime / Library 支持？
6. AI 服务使用什么协议，与 HTTPS 等常见协议如何区分职责？
7. Redis ZSet / Sorted Set 的底层数据结构与典型用途是什么？
8. Redis Lua 在什么场景下用于保证原子性？
9. Optimistic Lock 如何工作，适合什么并发更新场景？
10. Global Unique ID 如何生成，系统做过怎样的压力测试？

---

## S087 阿里淘天｜AI 应用开发 / Agent｜一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a0306a045d594b02b63fb0654d517901

真人 / 第一人称证据：作者直接写“给我面没招了，发点面经攒人品”，问题围绕本人的 Multi-stage RAG 和 Multi-Agent 项目连续深挖 20 余问，具有明确追问链和项目验真特征。

高价值问题：

1. BM25 与 Vector Retrieval 的 Hybrid Strategy 如何设计并证明提升？
2. PDF Scan、OCR、Table Extraction 的主要难点是什么，识别准确率如何评估？
3. Multi-Agent State 与 Checkpoint 如何设计，怎样处理状态竞争与全局状态？
4. 传统 Tool Call 与 MCP 的完整调用链有何不同，MCP 的缺点和兼容挑战是什么？
5. MCP Tool 的参数 / 返回结构如何标准化，结果能否 Streaming？
6. 主 Agent / Sub-agent 架构如何划分，一个 Session 的 Token 规模如何控制？
7. 子任务数据为空或执行失败时，Workflow 如何 Retry / Fallback / Degrade？
8. FastAPI + SSE 如何把 LangGraph 各 Node 的中间结果实时推送到前端？
9. 为什么选择 LangGraph 而不是简单 LangChain 编排？
10. Checkpoint 如何持久化，断线重连后怎样恢复之前的执行状态？
11. 对话状态应该落内存、数据库还是其他存储，如何权衡？
12. Vector DB / Index、RRF 与模型精排如何选型？

---

## S088 阿里云｜Agent 开发｜一面｜面试 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/discuss/872120976190816256

真人 / 第一人称证据：作者明确记录 60 分钟真人面试，前半小时问答、后半小时现场 AI Coding；正文保留自己答不上 RPC 问题、请求面试官提示仍没答出的状态。

高价值问题：

1. Workflow 与 Agent 的区别是什么，什么场景应该选择哪一种？
2. 分布式系统中进程间通信有哪些方式，单机和跨主机分别如何选择？
3. HTTP 与 RPC 的核心差异是什么，RPC 为什么在部分内部服务中更高效？
4. MQ、HTTP、RPC 等跨主机通信方式的可靠性、耦合度和延迟如何比较？
5. Data + AI 在业务平台中可能如何结合？
6. 实习 / 项目开发中最大的工程难题是什么，如果重做会如何改善？
7. AI Coding：实现本地 YAML / INI 配置文件监听与热更新模块。
8. 使用 AI 修改代码后，如何继续发现问题、让模型迭代并由人验证？

---

## S089 字节跳动｜后端 AI 开发｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f46e1419b49c4fe6832a1180b344af23

真人 / 第一人称证据：作者明确写“给我面没招了，感觉自己好菜”，问题从自己的订单 / 缓存项目连续追到 WebSocket 弱网、ID、Redis、ThreadLocal、TCP、安全与 OpenClaw，并附 SQL 和算法题。

高价值问题：

1. WebSocket 推送在弱网断连时如何恢复，什么时候主动回源拉取状态？
2. 订单 ID 如何生成，随机部分如何处理碰撞和全局唯一性？
3. Multi-level Cache 具体缓存什么，怎样与 Distributed Lock 防止秒杀超卖？
4. ThreadLocal 为什么能做到线程隔离，ThreadLocalMap 存在哪里，为什么可能内存泄漏？
5. TCP 四次挥手为什么需要服务端分两次发送，为什么等待 2MSL？
6. SYN Flood / SYN Attack 如何检测与缓解？
7. OpenClaw / Agent 产品的核心实现机制有哪些？
8. 通义千问、DeepSeek 等模型在应用侧如何比较并选型？
9. SQL 场景题如何分析索引与执行计划？
10. Coding：二叉树 Zigzag Traversal，并讲解复杂度。

---

## S090 字节跳动财经｜AI 应用开发｜日常一面｜发布 2026-06-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fb73d21e0a8c400380e579bc7e4fa65f

真人 / 第一人称证据：作者以本人“日常一面凉经”发布，评论区继续确认届别与简历相关性；问题围绕营销抽奖项目连续追问 Redis、MySQL Transaction、Binlog 与主从一致性，属于明确 AI 应用岗位中的 Backend Foundation 深挖。

高价值问题：

1. 秒杀 / 抽奖类业务如何限制奖品数量并治理高并发？
2. Redis 的高并发能力为什么通常高于 MySQL，二者存储与执行机制有什么不同？
3. Redis 为什么以内存为核心，而关系数据库需要以持久化磁盘结构为核心？
4. Transaction 的核心语义是什么，MySQL 如何实现提交与失败回滚？
5. 机器故障时事务保证会受到哪些边界条件影响？
6. MySQL 主从复制如何工作，怎样理解主从一致性与复制延迟？
7. Binlog 在事务生命周期中的写入时机是什么？
8. SQL 执行与 Binlog Event 的对应关系是什么？
9. 批量 / 延迟同步会造成什么一致性风险？
10. 主库故障时如何看待尚未同步到从库的数据以及 Failover 一致性？

---

## S091 阿里淘天｜AI 应用研发｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d2cc9a03316c45d888146c5b631e18b8

真人 / 第一人称证据：作者以本人暑期 AI 应用研发一面发布并写“攒人品”；问题从真实后端项目一路自然过渡到 RAG、MCP、Agent、OpenClaw Memory 和 Skills，完整体现目标岗位的基础工程 + AI 应用混合考察。

高价值问题：

1. 一个好的 RESTful API 应该考虑哪些可用性、幂等、错误码和演进因素？
2. 库存扣减如何保证幂等，多级 Cache 的生命周期如何设计？
3. 秒杀场景缓存失效如何避免 Cache Breakdown / Avalanche，空值缓存有哪些副作用？
4. ThreadLocal 的使用场景、生命周期和风险是什么？
5. 评论 / 回复系统的表结构如何设计？
6. RAG 与 Internet Search 的职责边界是什么，为什么不能互相完全替代？
7. MCP 解决什么问题，相比普通 Tool Integration 有哪些额外成本？
8. 为什么 MCP Tool Schema 可能显著增加 Context 长度，它与对话历史如何共同占用窗口？
9. 一个 Agent 项目应如何证明自己真正搭建过而不是只调用框架？
10. OpenClaw 类 Agent 的分层 Memory 如何实现？
11. Skill 是什么，怎样证明自己真正设计 / 编写过 Skill？

---

## S092 美团｜AI 后端开发｜二面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/94492fe4332a4c4984982c315d4353f7

真人 / 第一人称证据：作者明确以本人 AI 后端二面发布并邀请同岗候选人交流；问题从本人实习与技术选型追到 Redis、Vector DB、幂等、Prompt、Agent Memory 与 AI Coding。

高价值问题：

1. 项目中的技术选型如何说明，为什么某些状态选择 Redis 而不是数据库？
2. Vector DB 在项目中具体承担什么职责？
3. Backend Storage 如何做 Idempotency Design？
4. Prompt Engineering 在真实项目中沉淀了哪些可复用经验？
5. 当前单体 AI 应用如果真正上线，需要从可用性、扩展性和 Observability 哪些方向改造？
6. Agent Memory System 应如何分层与存储？
7. Short-term Memory 遇到 Context Window 上限时有哪些方案？
8. 怎样降低 Token 消耗同时保留关键任务状态？
9. AI Coding 在真实开发流程中应怎样使用与验证？

---

## S093 携程｜AI 后端｜暑期一面｜发布 2026-04-10｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0514bdd618cf43ae9be9240bc483cc9a

真人 / 第一人称证据：作者明确以“AI 后端一面”发布并写“发点面经攒人品”；问题先验证 AI Coding 的生产可用性，再连续追问分库分表、缓存、锁、事务与算法，属于目标 AI Backend 岗的完整基础工程考察。

高价值问题：

1. AI Coding 生成的代码质量如何评估，什么条件下才允许进入生产？
2. Sharding Key 为什么按某个业务核心 ID 选择，何时应启动 Sharding？
3. 分库分表后跨 Shard 查询、分页和全局排序如何实现？
4. 评论 / 多级回复表结构如何设计以减少 I/O？
5. Sharding-JDBC 等中间件在路由和聚合中承担什么职责？
6. Bloom Filter 与空值缓存分别解决什么问题，怎样权衡误判与污染？
7. Distributed Lock 解锁时如何保证原子性，避免误删他人锁？
8. Optimistic Lock 如何解决并发更新冲突？
9. 订单流程中扣库存与生成订单如何用 Transaction 保证一致性？
10. Coding：LRU Cache 或 Merge K Sorted Lists。

---

## S094 美团｜AI 后端开发｜二面｜发布 2026-04-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/2c7a3f42d7a8466785dad5a0c82df526

真人 / 第一人称证据：作者以 AI 后端二面分享发布并主动邀请同岗交流；问题围绕本人项目容量、三级 Cache、并发和 5000 万行数据处理持续深入，信息密度高且不是题库分类式整理。

高价值问题：

1. 项目中真正最难的工程问题是什么，个人负责边界在哪里？
2. 聚合 Bucket / Counter 类设计解决什么问题？
3. 系统是否做过压测，如何估算真实 QPS 和容量上限？
4. Three-level Cache 为什么需要三级，每一级缓存什么？
5. Local Cache 失效瞬间大量请求打到 Redis 时如何避免级联击穿？
6. Feed / 大对象全部放 Local Cache 会带来哪些内存与失效问题？
7. 5000 万行表如何设计高效批量读取与跨接口发送，避免一次性加载？
8. 数据迁移 / 批处理场景怎样通过分页、游标、并发和 Backpressure 降低总耗时？
9. SQL 场景题中如何根据数据规模设计索引与访问路径？

---

# 本轮明确排除

本轮为了扩大 Recall 搜索了大量企业页、话题页、作者页和跨平台索引，但没有降低 HUMAN-A 门槛。明确排除了：

- 同一账号短时间批量发布大量不同公司的“面经 + 标准答案 / 付费专栏”内容，无法确认候选人本人；
- “帮粉丝复盘 / 群友投稿 / 学员上岸”类二次转述，即使问题很完整也不计真人第一人称；
- RockyDing《三年面试五年模拟》、高频题解析、答案宝典、课程导流等学习资料；
- 去哪儿等正文直接附逐题标准答案、真实性与原始现场边界被二次加工污染的内容；
- 只有企业页 / 话题页摘要而找不到稳定原帖的线索；
- 9 月 8 日百度 AI 测开等虽然包含 Agent / LangGraph / Skill，但岗位属于测试开发，不通过 Role Scope Gate；
- 9 月 8 日快手一面等虽然问到 Skill / Memory，但原帖无法稳定确认目标岗位名称，不以“碰巧问 AI”代替岗位准入；
- 传统后端 / 普通算法岗，仅因简历中出现 Agent 或 AI Coding 而被零散追问的场次；
- 与 `S001–S074` 已有来源为同一场、同一原帖或高度一致的跨页面重复。

# Batch 05 观察

本批新增 `S075–S094` 共 **20 个 HUMAN-A 来源**，当前干净核心样本达到 **94 个**。

这一批进一步强化了几条值得直接反映到学习体系的真人信号：

1. **Harness / Runtime 已从“概念题”进入可验证工程细节**：执行幻觉、Long-running Latency、Tool Discovery、Dynamic Registry、Task Isolation、Compaction、Permission、Self-evolution、自动交付可靠性都被真实追问。
2. **Agent 的重点越来越像一个分布式后端系统**：RPC / Async、MQ、Checkpoint、Retry / Fallback、Streaming、Rate Limit、Cache、Idempotency、Observability 和 Capacity 不再是“额外加分项”。
3. **RAG 继续从 Pipeline 背诵走向实验与数据依据**：父子索引、BM25 + Vector + Rerank、OCR / Table、Index Update、RRF、Top-K 与 Evaluation 都要求解释为什么这么做、如何证明有效。
4. **基础工程是真实主线，不是传统后端题库硬塞进来的**：明确标注 AI 应用 / AI 后端的真人场次中，MySQL Transaction / MVCC / Log、Redis Cache / Lock、ThreadLocal、TCP、WebSocket、Sharding、Bloom Filter 被长时间连续追问。
5. **项目验真越来越严格**：是否真正负责核心模块、指标怎么测、业务量多大、失败后怎么恢复、AI 代码能否进生产、为什么不用 Workflow / Script，都是区分 Demo 与 Production Experience 的高频追问。

当前 94 个样本仍没有显示来源明显饱和。下一批继续维持同一 HUMAN-A 门槛，优先补 3–9 月尚未覆盖的公司 / 轮次以及新发布的 Agent Runtime / AI Backend 深挖。