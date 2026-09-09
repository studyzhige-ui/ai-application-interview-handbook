# Batch 06 — 2026 AI 应用 / Agent 高置信真实面经

采集日期：2026-09-09

> 本批开始执行更严格的“宁缺毋滥”规则：**只把能较高置信确认是候选人本人复盘、且包含足够技术细节的来源纳入正式 `Sxxx` 样本。**
>
> 本轮主动排除了：短视频二次创作、SEO/题库型博客、`含完整答案` 的模拟栏目、无法区分真实场次与二次整理的帖子、只有“面了/挂了”但几乎没有问题细节的内容。它们即使能提供关键词，也不进入正式频率统计。
>
> 问题均为简洁转述，保留考察意图，不复制第三方正文。

---

## S064 百度｜Agent Harness 研发工程师｜一面｜2026-09-08｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/discuss/926928449204129792

高价值问题：

1. 如何理解 Agent Harness，它和 Agent 本身、普通框架的职责边界是什么？
2. Coding Agent 修复代码是否正确，应该用哪些维度评判，而不能只看“模型说修好了”？
3. 多 Agent 并行修复代码时，多个 Agent 同时修改一个文件怎么处理冲突？文件锁、工作区隔离、合并分别适合什么场景？
4. Claude Code 在代码规范、并行修改与冲突控制方面有哪些可借鉴的工程机制？
5. Claude Code 的沙箱机制应该解决哪些风险？
6. 日志预处理/压缩以降低 Token 时，如何避免丢失根因证据？
7. 多模型参与同一个任务时，如何保证上下文、输出协议和状态的连续性？
8. 没有显式错误日志的缺陷，Coding Agent 如何继续定位？
9. Python async IO、生成器、上下文管理器等语言能力在 Agent Runtime 中有哪些实际用途？

价值：**目前最直接命中“Agent Harness”岗位名称的一手样本之一**，而且面试官明确把 Claude Code 实现作为工程参照，应作为后续 Harness 课程与源码研究的高权重样本。

---

## S065 百度｜Agent 开发日常实习｜2026-09-07｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60

高价值问题：

1. Hybrid Retrieval 具体由哪些检索器组成？为什么这样组合？
2. RAG 文档 Chunk 粒度如何确定，有没有实验或业务依据？
3. 自研 Coding Agent 相比开源 Agent 的优势到底是什么？
4. Tool Layer 的“兜底”是什么意思，Tool Executor 的职责如何展开？
5. Long-term Memory 如何实现？
6. MCP 的 stdio 与 Streamable HTTP 如何实现、语义有什么不同？
7. Agent 执行中断以后如何续跑？
8. Agent 是否是黑盒？如何通过日志/Trace 感知当前执行到哪里、卡在哪里？
9. Multi-Agent 如何设计？

价值：发布时间极新，问题从项目一路追到 Tool Executor、MCP Transport、Resume 与 Observability，技术密度高。

---

## S066 百度｜Agent / AI 应用后端｜一面｜2026-09（发布日期 09-09，面试日期未明确）｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/72858aade19d443facc870fea8bb134f

高价值问题：

1. LLM Runtime 与 Tool Runtime 分别负责什么？为什么需要拆层？
2. Model Routing 的依据是什么？
3. Retry 是否适用于所有错误？参数错误、业务错误、超时应该如何区别处理？
4. SSE 与 WebSocket 如何选，Agent Streaming 如何落地？
5. 多轮 Tool Call 的 Context 怎么管理，大 Tool Result 怎么处理？
6. Tool Timeout、并发调用和幂等怎么设计？
7. Trace Hook 应该在哪些 Runtime 层埋点，一次用户请求最后如何呈现完整 Trace？
8. Memory、Checkpoint、用户隔离、主子 Agent 分别怎么设计？
9. PDF 表格为什么可能需要保留/转换结构，Chunk 太大太小有什么影响？
10. Hybrid Retrieval 为什么同时需要 BM25 和向量检索？RRF 为什么不用直接加权？参数如何验证？
11. 如何验证 Agent 最终结论正确，并把 Citation 与证据关联起来？
12. MySQL MVCC、redo/undo/binlog、索引等基础仍被连续追问。

价值：这是一份非常罕见的“**Runtime + RAG + MySQL 基础**”三层同时深挖的一手面经，后续做跨模块知识地图时权重很高。

---

## S067 百度｜AI 测试 / Agent 评测方向｜一面｜2026-09-08｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/1992e19e6a3c401e9d07349988f5dbfd

高价值问题：

1. Agent 测试集如何构建，Agent 输出效果如何评测？
2. 并行节点发生状态冲突如何处理？
3. Trace 如何构建，并用于定位 Agent 返回结果不理想的原因？
4. Checkpointer 的机制与 State Schema 如何设计？
5. Codex 如何用于自动化测试/验证？
6. Skill 的原理与真实应用场景是什么？
7. MCP 服务在 Agent 系统里承担什么职责？
8. Agent Tool 如何防止目录/路径穿越等安全问题？

价值：岗位偏 AI 测试，但问题直接覆盖 Agent Evaluation、Checkpoint、Trace、Codex 与 Tool Security；**只用于这些交叉能力，不把传统测开问题计入 Agent 频率。**

---

## S068 小鹏汽车｜Agent 开发实习｜一面｜2026-08-28｜原始/第一人称｜高置信

来源：https://api-cdn.nowcoder.com/feed/main/detail/3832f2e0ba074b4782daa6ff7a65a1f9

高价值问题：

1. ReAct 与 Plan Mode 在项目里分别怎么实现？
2. Multi-Agent 的任务分配与协同编排怎么做？
3. Context 过长采用什么压缩策略，实际节省多少 Token？
4. 压缩以后如何**量化评估关键信息保留率**，而不是只靠主观感觉？
5. Skill 的功能边界如何定义？
6. 用户偏好信息为什么异步持久化，如何避免影响主请求？

价值：把 Context Compaction 从“会压缩”追到“**节省多少 + 信息保真怎么测**”，对 Harness Evaluation 很重要。

---

## S069 MINISO 名创优品｜Agent 开发实习｜一面｜2026-08-26｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/f844a4ac20be44bc9b3f756bd0ebb84c

高价值问题：

1. 为什么业务 Workflow 要拆成多个 Subgraph，主图与子图之间怎么传 State？
2. 外部任务已成功、但写 Checkpoint 前进程宕机，恢复后如何避免**重复产生外部副作用**？
3. Skill 从 Bad Case 学习时，如何防止错误经验/错误提示词污染后续任务？
4. ReAct 与 Plan-and-Solve 如何在同一 Agent 中分工？
5. 流程编排型 Multi-Agent 与自主规划型 Multi-Agent 有何区别？
6. 大量信息在多个 Agent 之间传递时，如何避免 Context 丢失和 Token 爆炸？
7. ReAct 执行发生偏移时如何校正？
8. Tool Result 如何压缩，同时保留必要信息、权限语义、注入防护与校验信息？

价值：对 Checkpoint Crash Window、Memory/Skill Poisoning、Tool Result Compression 的考察很成熟。

---

## S070 美团｜Agent 开发｜一面｜2026-08-23｜原始/第一人称｜高置信

来源：https://api-cdn.nowcoder.com/feed/main/detail/1d067ce539c64d3988eabb9b646ef8a0

高价值问题：

1. Agent 项目整体架构与业务价值怎么讲？
2. RAG 文档切分、召回、生成完整链路如何实现？
3. Multi-Agent 如何分配任务、并行执行、管理 State 并汇总最终结果？
4. Agent Context 如何管理，为什么需要 Context Compression？
5. Routing 如何判断请求应该进入哪个 Agent？
6. 并发与异步的区别，在 Agent 后端分别适用于什么任务？
7. 任务调度、Tool Call、State 管理等 Agent 工程问题如何整体设计？
8. 如果从零设计一个 Agent 应用，需要考虑哪些系统层？

价值：问题不花哨，但覆盖从 RAG 到 Multi-Agent、Context、Routing、Async 的主干，是高质量“系统骨架”样本。

---

## S071 懂车帝｜Agent 开发｜一面｜2026-08-13｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/8d84590d7efe4c78943b28708b4395f2

高价值问题：

1. 用户给出模糊描述时，Agent 如何澄清或补足信息？
2. Leader Agent 如何判断问题出在执行链路的哪个位置？
3. Trace ID 与普通日志分别承担什么职责？
4. 不同 Case 经过不同链路时，Agent 如何识别当前配置与处理路径？
5. 如果日志级别/日志内容本身有误，Agent 会不会被错误观测信息带偏？
6. Multi-Agent 应该按什么粒度划分？业务线越来越多时，如何避免 Agent 数量无限膨胀？
7. 线上模块增删以后，Agent 能力与配置如何同步演进？
8. Agent 改代码后如何防止“修好一个 Case、破坏其他 Case”？

价值：重点不是八股，而是 **Observability Evidence、Agent Topology Governance 与 Regression Safety**，是目前很少见的方向。

---

## S072 字节跳动｜AI 应用开发｜一面｜2026-08-06｜原始/第一人称｜高置信

来源：https://api-cdn.nowcoder.com/feed/main/detail/15af3788a038477bba99f2f9d94b2cef

高价值问题：

1. Agent 核心模块如何拆解？
2. Tool 的职责边界、参数 Schema、错误码如何设计？
3. 短期/长期 Memory 如何做存储、过期、去重？
4. ReAct 与 Plan-Execute 如何选，怎么避免无限循环或多 Agent 相互推诿？
5. Multi-Agent 如何通信与保存共享 State？
6. RAG 从入库到查询的完整链路、Chunk 实验、Hybrid Retrieval、Rerank 如何设计？
7. RAG 与 Fine-tuning 如何取舍？
8. Agent 如何做 Latency / Cost 优化、Bad Case 归因、超时异常处理与 Observability？

价值：涵盖 Agent + RAG 的完整工程主线，且问题围绕项目追问，不是纯题库罗列。

---

## S073 快手｜AI Agent 开发｜一面｜2026-07-20｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/8ef62dcdde1340f987507d2d1e1433a8

高价值问题：

1. 父子索引为什么存在？BM25 为什么要与向量检索组合？
2. Rerank 后 TopK 怎么取？
3. Context Engineering、Memory、Function Calling、Planning 怎么设计？
4. Prompt Injection 和 Tool Safety 怎么防？
5. 分布式令牌桶、漏桶、滑动窗口限流分别怎么工作，如何选型？
6. Bloom Filter 怎么实现？
7. 数据库索引失效有哪些场景，LIKE 查询如何影响索引？
8. RAG 如何构造评测集、衡量相关度/答案质量/性能？

价值：非常典型地把 Agent/RAG 与分布式限流、数据库和数据结构基础混合考察。

---

## S074 腾讯 CSIG｜后台开发（Agent/Memory 项目）｜二面｜2026-07-18/20｜原始/第一人称｜高置信｜已 Offer

来源：https://www.nowcoder.com/discuss/906488290021306368

高价值问题：

1. 为什么 Memory 要设计成三层？一层平铺架构有什么问题？
2. 三层数据分别放在不同存储时，其生命周期、持久化和膨胀治理怎么做？
3. Milvus 历史 Memory 的全量压缩怎么做，什么时候触发，压缩比例如何验证？
4. 跨会话 Memory Recall 与个性化 Prompt 注入怎么实现？
5. Skill 输出占满 Context 时怎么办？
6. Codex 的 fork conversation 与 Sub-agent 有什么区别？
7. Codex / Claude Code 读取源代码时为什么不一定采用“长期 Memory + RAG”这套架构？
8. 已经有 Codex/Claude Code 的 Code Review，为什么还要自研 Code Review Agent？什么场景更适合封装成 Skill？

价值：**对成熟 Coding Agent 产品架构的比较非常深入**。后续 Agent Harness 模块研究 Codex / Claude Code 时，这是很好的真实面试需求证据。

---

## S075 法本信息｜AI Agent 开发｜2026-07-24｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/d8f5de441b7a4f7ba32164ef37cce1fc

高价值问题：

1. 本地 Coding Agent 从任务输入到代码修改的完整 Runtime 链路是什么？
2. 多模型 Backend 如何统一请求/响应、错误码、重试？
3. 新 Tool 从定义、注册、发现到调用的完整生命周期是什么？
4. 文件不存在、命令超时、权限不足等 Tool Failure 如何分类恢复？
5. Coding 过程中 Context 如何治理，压缩后如何验证当前任务没有被破坏？
6. Task Summary、File Summary、Process Notes 等压缩产物如何生成、更新和失效？
7. Long-term Memory 中过期文件摘要、模型错误结论如何发现和纠错？
8. 如何识别反复读同一文件、重复调用同一工具等冗余状态？
9. RAG、Memory、Context Engineering 分别解决什么问题？
10. Agent Harness 与直接调用 LLM API 的本质区别是什么？
11. Benchmark / Case / Metric 怎么设计，如何判断一次改动真的让 Agent 变强？
12. 错误 Patch 如何回滚、验证、再尝试？

价值：目前收集到的 Coding Agent / Harness 一手面经中技术密度最高的一组之一。

---

## S076 上海 Agent 初创团队｜Agent 工程｜2026-07-06｜原始/第一人称｜高置信

来源：https://www.nowcoder.com/feed/main/detail/708ff271220c4ccf86da290e265dfc4a

高价值问题：

1. 如何评价 Agent 能力并尽量排除基础模型能力的影响？
2. 当模型选型受限时，如何针对不同模型优化整条 Agent 链路？
3. 面向收敛业务场景，除了 RAG，还能怎样把脚本、SQL、规则与 Tool 组织进 Agent？
4. Skill 的目录结构与能力边界是什么？Skills 相比 MCP 的工程优势是什么？
5. 面向非技术用户，Agent/Skill 安装与分发如何降低门槛？
6. Claude Code 如何检索代码？为什么某些 Coding Agent 从“代码 RAG”转向更直接的 Repo Search / Read / Tool-driven Navigation？
7. Embedding Model 怎么选，RAG Chunk 粒度怎么定？
8. Redis Streams 为什么适合某些 Agent 任务/事件场景？
9. 数据库性能上限如何估计？

价值：开放题比例高，直接追问 Claude Code / Codex 产品差异和“为什么不用某种常见方案”，有助于课程避免只教固定框架 API。

---

## 本轮明确排除的来源类型

本轮搜索过程中发现了不少“看起来题很多”的内容，但未纳入正式 `Sxxx`：

- 标题带 `三年面试五年模拟 / 含完整答案 / 面试宝典`，正文明显以标准答案为主、无法确认真实场次的内容；
- 把多家公司问题拼成一个故事、但无法追溯每一场原始面试来源的跨公司复盘；
- 短视频只说“Agent 面试很难 / 一二三面分别考什么”，没有足够可核验技术问题；
- 二次博客把公开题目重新包装成“高手答案 / 完整解析”的 SEO 内容；
- 小红书只有搜索标题、没有稳定正文与足够元数据的帖子，继续留在 `research/leads/`，不升级为正式样本。

## Batch 06 结论

与前几批相比，本批数量刻意收缩，但平均信息密度显著提高。新增信号集中在：

- Harness 岗位开始直接以 **Claude Code / Codex 的实现**追问候选人；
- Tool Executor / Tool Runtime 成为独立工程层，不再只是“Function Calling”；
- Context Compaction 开始要求**量化保真评估**；
- Memory / Skill 的错误写入与污染治理开始成为面试问题；
- Checkpoint 的“外部副作用已成功、状态尚未落盘”Crash Window 被直接考察；
- Agent Observability 开始追问“Trace/Log 本身是否可信”；
- Multi-Agent 不只问协作，还问拓扑膨胀、共享文件冲突与模块演进；
- RAG/Agent 面试继续稳定混入 MySQL、Redis、限流、异步与网络基础。
