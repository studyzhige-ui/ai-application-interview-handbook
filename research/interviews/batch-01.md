# Batch 01 — 2026 AI 应用 / Agent 真实面经（公开可访问样本）

采集日期：2026-09-09

> 本文件保存研究所需的来源元数据与问题简洁转述，不复制第三方面经整篇正文。部分牛客合集/专栏页面只公开部分题目，因此这里只记录本次检索时实际可见内容；后续若找到原帖或更多公开内容再增量补齐。

## S001 安软｜AI 应用开发实习生｜2026-07-25

来源：https://api-cdn.nowcoder.com/feed/main/detail/40920533fad14136bff01c3928c7e953

可见问题：

1. 如何介绍两个 AI 项目的真实个人贡献？
2. 如何理解 AI Coding 能做与不能做的工作边界？
3. 如何区分 AI 生成代码与自己设计/手写的部分？
4. 模型选型如何权衡能力、稳定性与成本？
5. Coding Agent 遇到超长上下文或幻觉时，如何把任务拉回正确方向？
6. 自研 Agent 架构如何设计？
7. RAG 如何评测与优化？
8. Redis 在 AI 应用中的作用？
9. IO 多路复用原理与应用？
10. 数据库性能如何优化？

## S002 凌脉｜AI 应用开发实习生｜2026-07-11

来源：https://www.nowcoder.com/feed/main/detail/76f5be8b8bd5420b94d32a66e26a7ad9

可见问题：

1. 文档管理/RAG 项目解决什么业务问题？
2. 长文档如何保证总结和回答准确？
3. 完整 RAG 链路如何设计，做过哪些优化？
4. Qdrant 与 Redis 分别保存什么数据，为什么这样分工？
5. Redis 是否可能产生 BigKey，如何处理？
6. MCP 在项目里如何使用？
7. 模型调用与 Token 成本如何控制？
8. Coding Agent 有哪些工程约束？

## S003 阿里｜AI Agent / AI 应用｜2026-08/07/06（合集可见部分）

来源：https://www.nowcoder.com/discuss/923739430513299456

可见问题：

1. Agent 完整执行链路是什么？
2. Agent 做过哪些优化，如何量化调优效果？
3. 语义检索如何实现？
4. 向量数据库在项目中承担什么职责？
5. 为什么选择 LangChain/LangGraph，了解其底层流程吗？
6. 如何约束模型输出格式和规则？
7. Memory 模块怎么设计？
8. 多轮、多会话下 Memory 怎么隔离与管理？
9. Agent 系统整体容错如何设计？
10. Context 管理怎么优化？
11. Agent 为什么出现幻觉或乱调工具，如何缓解？
12. Agent 评测指标体系怎么设计？
13. 主 Agent 如何规划任务并保证拆解合理？
14. 子 Agent 上下文如何传递？
15. ReAct 的流程、优点和缺点是什么？
16. Function Calling 完整流程是什么？
17. Function Call JSON 不合法怎么处理？
18. 模型捏造 Tool 参数如何处理？
19. 多 Agent 常见协作模式有哪些？
20. 多用户并发导致 Agent API 卡死时如何设计？
21. 一万个长文档如何构建可扩展 RAG 知识库？
22. 数据库索引原理、事务隔离、MVCC 等基础如何解释？

## S004 阿里｜AI Agent / AI 应用｜2026-04（合集可见部分）

来源：https://www.nowcoder.com/discuss/923740380485406720

可见问题：

1. MCP 如何承载/内置业务 SOP？
2. AI 项目工作成效如何量化？
3. HyDE 生成中间内容质量不佳时，如何评估其对检索的影响？
4. 向量数据库如何选型，常见产品有什么差异？
5. Agent 架构怎么设计？
6. RAG 检索链路如何实现？
7. Agent 的工具调用能力如何训练，训练数据应该包含什么？
8. LangChain 架构和核心模块是什么？
9. Agent 开发范式有哪些？
10. Multi-Agent 如何设计？
11. Agent 之间如何通信？
12. MCP 在项目中具体做了什么？

## S005 字节跳动｜AI Agent 开发｜2026-08/07（合集 01 可见部分）

来源：https://www.nowcoder.com/discuss/922659050167226368

可见问题：

1. Harness 与 Orchestrator 有什么区别？
2. ReAct 与 Plan 模式如何选择？
3. Context 超过模型窗口怎么办？
4. Agent 出现路径震荡/反复执行如何优化？
5. Context 与长期 Memory 有何区别？
6. 工具描述太多导致 Prompt 过长怎么办？
7. 多 Agent 同时修改文件如何避免冲突？
8. 一个完整 Agent 系统有哪些核心模块？
9. Chatbot 和 Agent 的边界是什么？
10. Planning、Memory、Tool Use、Execution 分别做什么？
11. 意图识别有哪些实现方式？
12. 用 LLM 做意图分类时 Zero-shot 与 Few-shot 怎么选？
13. RAG 从文档入库到生成答案的完整流程？
14. 用户连续触发多个工具时如何避免 Tool 调用混乱？
15. RAG 召回差应该从哪些维度排查？
16. Agent 测评如何设计测试集？
17. Skill 路由如何设计测试集？
18. MySQL 索引为什么快，底层原理是什么？
19. Planning 应该由框架承担还是由模型承担？
20. 短期记忆与长期记忆有什么区别？
21. MCP 等工具协议如何使用？
22. Redis 在 Agent 系统里有哪些应用场景？
23. RAG 为什么使用父子索引？
24. 消息队列在 Agent 系统中有什么作用？

## S006 字节跳动｜AI Agent 开发｜2026-07/06/05（合集 02 可见部分）

来源：https://www.nowcoder.com/discuss/922659486983036928

可见问题：

1. 如何评价 Agent 能力（排除模型本身能力）？
2. 不同模型受限时，如何针对模型特点优化 Agent 全流程？
3. 面向收敛业务场景，如何专项优化 Agent？
4. RAG Agent 的评测集如何构建？
5. Agent/RAG 评测应该观测哪些指标？
6. 如何调研通用或开源评测基准？
7. 海量线上日志如何沉淀成有限、可维护的离线评测集？
8. Agent 如何调用 Tool？
9. Agent 如何判断是否应该调用 Tool？
10. MCP 解决什么问题？
11. Context Window 满了如何压缩？有哪些压缩策略？
12. Skill 分层体系如何设计？
13. 用户输入如何路由到相关 Skill？
14. Skill 如何沉淀和演进？
15. Claude Code 与 Codex 各自有哪些特点？
16. 输入模型的 Prompt 通常由哪些部分组成？
17. 自研 Coding Agent 与 Claude Code/Codex 的差异是什么？
18. 上下文压缩如何实现？
19. 多层压缩为什么需要分层，每层目标是否相同？
20. 如何发现压缩过度导致质量下降，并恢复？
21. Agent 如何支持在原任务基础上继续修改/追加需求？
22. ReAct 与 Plan-and-Execute 各自优劣？
23. RAG 从 Chunk 到最终生成的完整链路？
24. Multi-way Retrieval 是什么？
25. Rerank 在 RAG 中解决什么问题？
26. RAG 与 Fine-tuning 如何选择？
27. 多跳问题需要多次检索时如何优化？

## S007 字节跳动｜AI Agent 开发｜2026-08/04/03（合集 03 可见部分）

来源：https://www.nowcoder.com/discuss/922659809084571648

可见问题：

1. LangChain 与 LangGraph 的区别和适用场景？
2. 为什么选择 AI 应用开发方向？
3. 如何持续跟进 Agent 前沿？
4. 如何理解 Agent 系统？
5. Tool 的设计原则是什么？
6. Memory 有哪些类型？
7. ReAct 与 Plan-Execute 适用于哪些任务？
8. Planning 有哪些实现方式？
9. 长期记忆和短期记忆如何实现？
10. Filesystem 在 Coding Agent 中扮演什么角色？
11. Skills 相比传统 Tool/Agent 能力抽象有什么优势？
12. Harness Engineering 怎么理解？
13. 同一模糊任务在不同 Agent 上表现不一致，如何提高稳定性？
14. RAG 在项目中如何存储与召回？
15. 为什么使用模块化单 Agent 而不是 Multi-Agent？如何衡量协作开销？

## S008 百度｜大模型研发（Agent 方向）｜2026-08-18

来源：https://www.nowcoder.com/discuss/921590204903723008

可见问题：

1. Prompt Engineering → Context Engineering → Harness Engineering 的演进关系是什么？
2. Context 快超过窗口时怎么处理？如果自己设计压缩机制会怎么做？
3. Claude Code 的 Context 压缩如何理解？
4. 从零搭建团队 RAG 的完整步骤？
5. 如果设计 Agent 学习体系，如何组织章节和资料来源？
6. Claude Code 类 Coding Agent 应重点研究哪些系统模块？
7. 数据库索引如何在实际项目里使用？
8. 设计结构化业务表时如何建模与索引？

## S009 美团｜AI 全栈 / Agent 开发｜2026-09（公开可见部分）

来源：https://www.nowcoder.com/discuss/925163415465635840

可见问题：

1. 智能行程规划 Agent 如何设计 Tool 编排与异常处理？
2. 用户需求模糊时如何设计多轮澄清？
3. RAG 召回不相关时 Query Rewrite 如何优化？
4. Markdown 没有标题时如何 Chunk？
5. 短 Query 和长 Chunk 在向量化与检索上有什么问题？
6. 如何保证 Agent 输出 JSON 满足下游 Schema？

## S010 腾讯｜AI 应用开发后端｜2026-04-24（汇总页面可见部分）

来源：https://www.nowcoder.com/discuss/877151327091027968

可见问题：

1. Multi-Agent 如何编排，状态如何流转？
2. Agent 失败/中断后如何恢复？
3. Retry 如何保证业务安全和幂等？
4. 金融/资金类场景下 Agent 超时失败如何保证安全？
5. RAG 知识库如何不停服更新？
6. Agent 循环太长或死循环怎么限制？
7. Agent Prompt 如何约束幻觉？
8. 向量检索效果如何评估？
9. SSE/WebSocket 在流式 Agent 中如何选择？

## S011 腾讯｜AI 应用开发｜2026-04-21（汇总页面可见部分）

来源：https://www.nowcoder.com/discuss/878600528970735616

可见问题：

1. 分库分表如何设计？
2. 跨库/跨表查询如何处理？
3. 如何通过游标/书签思路规避深分页？
4. MySQL 事务隔离级别？
5. Redis Lua 与普通原子指令如何选择？
6. Redis 并发控制如何设计？
7. MQ 如何选型并接入 AI 应用后端？
8. Agent 机制与后端系统如何组合？

## S012 虾皮｜Agent 开发一面｜2026-08-20 左右

来源：https://www.nowcoder.com/discuss/921527746415562752

可见问题：

1. Agent 项目整体架构和个人负责部分？
2. 单 Agent / Multi-Agent / Workflow 为什么这样选？
3. ReAct 的 Thought/Action/Observation 分别承担什么职责？
4. Tool 返回结果的消息结构为什么要单独设计？
5. 短期记忆与长期记忆分别如何实现？
6. 哪些信息适合进入长期记忆？

## S013 小红书｜AI Agent 开发｜2026-08-12（公开可见/关联页面）

来源：https://www.nowcoder.com/discuss/919617105761165312

关联公开讨论：https://www.nowcoder.com/discuss/872820735335485440

可见问题：

1. MCP、Function Calling、Skills、Agent 分别处于什么层次？
2. Agent 的 Planning / Execution / Reflection 如何形成闭环？
3. Reflection 如何限制预算，避免无限自我循环？
4. Redis 数据类型及底层编码应该如何解释？
5. 如何把后端的并发、缓存、数据库、可观测能力迁移到 Agent 工程？

## S014 月之暗面｜AI Agent 开发｜2026-07-21

来源：https://www.nowcoder.com/discuss/922643334898647040

可见问题：

1. 如何介绍 Agent 项目的完整链路？
2. ReAct、Tool、RAG、短期工作记忆、长期记忆如何组合？
3. 长链任务如何持续执行而不是一次性生成？

## S015 哔哩哔哩｜AI 应用 / Agent 开发｜2026-08-18

来源：https://www.nowcoder.com/discuss/923535010743754752

可见问题：

1. 为什么选择 AI Agent 方向？
2. 如何从传统后端能力过渡到 Agent 工程？
3. Agent 不应只是“Prompt 外壳”，真正的工程闭环包含哪些组件？
4. 如何把权限、状态、验证和业务系统组织进 Agent？

## Batch 01 初步观察

仅从这一批公开可见样本，企业问题已经明显从“会不会 LangChain API”向以下方向迁移：

- **Harness / Runtime**：Context、Compaction、Tool Runtime、Skill、Filesystem、Orchestration、并发与文件冲突。
- **Reliability**：Timeout、Retry、Idempotency、死循环、异常恢复、JSON/Tool 参数校验。
- **Evaluation**：离线评测集、线上日志回流、Skill 路由评测、Agent 独立于模型的能力评价。
- **RAG 工程化**：Chunk、Query Rewrite、父子索引、多路检索、Rerank、多跳、热更新、召回故障定位。
- **数据分层**：MySQL、Redis、Vector DB 在同一 Agent 系统中的职责边界。
- **传统后端仍然重要**：索引、MVCC/事务、Redis、IO 多路复用、MQ、并发、流式通信。

这批数据只作为第一批样本，不用于宣称最终频率结论。
