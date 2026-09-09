# Batch 04 — 2026 AI 应用 / Agent 真实面经（新增样本）

采集日期：2026-09-09

> 本批重点补充 2026 年 8 月下旬到 9 月上旬的新鲜样本，并继续区分来源质量：
>
> - `原始/第一人称`：候选人直接复盘，统计权重最高。
> - `整理/待核实`：二次整理、专栏型账号或难以确认是否为直接候选人复盘，保留为“问题信号”，但不与第一人称样本等权计数。
> - 只保存来源元数据与问题简洁转述，不复制第三方面经全文。

## S035 字节跳动｜Agent 开发｜2026-09-03｜原始/第一人称

来源：https://www.nowcoder.com/discuss/925342611194286080

可见问题：

1. 如何理解 Agent Harness，它与一般 Agent 框架的边界是什么？
2. 一个平时 5 分钟完成的长程 Agent 任务突然耗时 15～20 分钟，如何定位延迟来自模型、Tool、检索、网络、调度还是上下文膨胀？
3. 对长程任务的性能退化如何优化，并如何验证优化有效？
4. Tool 有固定参数 Schema 时，如何保证模型根据上下文稳定地产生合法、真实、可执行的参数？
5. 多轮对话导致 Context Window 不断膨胀时如何处理？
6. Summary / Compaction 必然丢信息时，如何尽量保留关键事实、约束、任务状态与可恢复性？
7. RAG 的离线入库与在线问答链路分别如何设计？
8. 项目中的结构化评分结果如何约束输出 Schema 并验证？

## S036 深信服｜AI Agent｜2026-08-21｜原始/第一人称

来源：https://www.nowcoder.com/feed/main/detail/83326f3bcc5546b2b556373ad29a6d71

可见问题：

1. 了解哪些 Coding Agent？如何理解 pi 一类 Agent/Harness 的设计？
2. 基于 VLM 的 Benchmark 系统如何搭建？
3. 强化学习平台如何做资源管理？
4. 如何区分“模型效果评测”和“Agent/Harness 效果评测”？
5. Codex 的核心 Agent Runtime / Harness 是如何实现的？

> 这一条对本项目尤其重要：面试官已经开始直接要求候选人理解 Codex 等成熟 Agent 产品的实现，而不仅是会调用 LangChain/LangGraph。

## S037 美团｜AI 全栈｜2026-09-01｜原始/第一人称

来源：https://www.nowcoder.com/feed/main/detail/ccf6c19be7424f139ea4d6b3c557764d

可见问题：

1. Codex 与 Claude Code 的 Context 压缩原理如何理解？
2. 如果不依赖现成 Agent 产品，自己从零实现一个 Agent，会如何划分 Runtime / Tool / State / Context 等核心模块？
3. 现场 AI Coding 时如何正确处理需求、验证生成代码并兜底？
4. 前端性能优化与 Agent 应用的工程基础如何结合？

## S038 百度｜开发岗位（Agent 项目深挖）｜2026-09-01｜原始/第一人称

来源：https://www.nowcoder.com/feed/main/detail/22468da481974784bb19116f5b0134c1

可见问题：

1. 三层 Memory 如何设计？每层保存什么？
2. 摘要式 Context 压缩怎么做？
3. Claude Code 的 Memory / Context 管理如何实现？
4. 如果 Agent 需要执行固定工作流，应该如何设计？
5. Skill 的含义是什么，何时适合封装成 Skill？
6. 实际使用过哪些开源 Skill / Agent 能力？
7. 不同基础模型在 Agent 场景中的能力差异如何判断？
8. Redis 字段如何设计在业务缓存中才合理？
9. 支付成功但回调丢失时如何保证最终一致性？

## S039 字节跳动｜AI 应用开发（中国交易与广告）｜2026-08-27｜原始/第一人称

来源：https://www.nowcoder.com/feed/main/detail/b34f6902e8544fe2953696ed52e49dba

可见问题：

1. 最简单的 Agent Loop 由哪些消息和状态组成？
2. 一个长时间运行的 Agent 任务，用户主动取消时如何做到可取消、可清理、不会留下半完成副作用？
3. Agent Runtime 中常见 message 类型有哪些，模型消息、Tool Call、Tool Result、状态事件如何区分？
4. 短期 Memory、长期 Memory 与 Context Window 如何管理？
5. Redis 分布式锁如何加锁、释放与续期？
6. 业务未结束但锁快到期时 WatchDog / Lease Renewal 如何实现？
7. RocketMQ 延时消息如何实现，不用 MQ 时有哪些替代设计？
8. Redis 为什么高 QPS，IO 多路复用和 Reactor 模式如何理解？
9. 配置中心动态刷新失败时，如何保证应用内配置一致性和可用性？
10. 如何实现“相同 key 串行、不同 key 并行”的线程安全任务执行器？

## S040 滴滴｜后端实习（纯 Agent 项目）｜2026-08-27｜原始/第一人称

来源：https://www.nowcoder.com/discuss/924334862113198080

可见问题：

1. 在本地低性能模型条件下，异步 Agent 任务如何提高吞吐？
2. 异步任务失败或连接中断后，如何保证任务不丢失？
3. Kafka 与 MySQL 如何协作承载任务调度？为什么 MQ 只放 Task ID 而不是完整任务数据？
4. 任务执行结果与数据库状态更新如何保证原子性 / 最终一致性？
5. 如何防止同一 Agent Task 重复入队、重复执行或重复产生副作用？
6. Task Token、版本号、CAS、乐观锁分别解决什么问题？
7. 实例宕机后如何扫描、识别、接管和恢复未完成任务？
8. Task Lease / Expire Time 如何设置？
9. 热点 Key / 热点文档导致乐观锁冲突时如何优化？
10. Elasticsearch 与 Redis 在同一 AI 后端中如何分工？
11. Redis 过期时间、惰性删除、定期删除如何实现且避免影响请求延迟？
12. Kafka Producer / Broker / Consumer 三端如何共同保证可靠性？
13. 超大文件（几十 GB）如何流式读取、分块去重并输出，避免内存爆炸？

## S041 某公司｜AI 大模型应用 / Agent 工程师｜2026-09-04｜原始/第一人称

来源：https://www.nowcoder.com/feed/main/detail/10b2fcaf73d2401f8636bd0459e1cd08

可见问题：

1. 设计一个 600GB～1TB 金融垂类 RAG，从 0 到 1 的完整架构是什么？
2. 电子 PDF 与扫描 PDF 混合时，如何做解析、OCR、版面结构恢复与质量控制？
3. 如何避免固定 Chunk 破坏跨页语义连续性？
4. TB 级文档如何设计 Hybrid Retrieval，并决定向量召回与 BM25 的组合方式？
5. 全量 Embedding 成本过高时，初始化建库、增量更新、重复内容缓存和存储成本如何优化？
6. Cosine Similarity 与 BM25 在检索链路中分别解决什么问题？
7. Transformer / Attention 等基础是否能解释到模型推理流程层面？

## S042 拼多多｜Agent 二面｜2026-08-25｜原始/第一人称（页面相关推荐可见）

来源：https://www.nowcoder.com/feed/main/detail/f5e7351df8364147ac8da085b99d9d18

可见问题：

1. Agent 如何隔离不同用户 / 不同任务的 State 与资源？
2. 如何保证 Agent 分析与最终输出结果的准确性？
3. Agent Evaluation 测试用例应该覆盖哪些失败模式与业务边界？
4. 完整 Agent 业务流如何描述？
5. LangChain 与 LangGraph 的核心区别是什么？
6. 为什么选择自研 Agent Runtime 或开源框架，二者边界如何权衡？
7. 手写线程安全 LRU，考察 Agent 后端仍然需要扎实并发与数据结构基础。

## S043 阿里巴巴｜Agent 开发｜2026-09-03｜整理/待核实

来源：https://www.nowcoder.com/discuss/925162488314765312

可见问题信号：

1. 电商智能客服 Agent 如何按售前、售后、订单等职责拆分？
2. 短期/长期 Memory 分别用什么存储层，为什么？
3. 多 Agent 同时修改同一订单状态时，如何保证并发一致性？
4. MCP 与传统 API Gateway 的职责边界和本质区别是什么？
5. Skill Registry 如何支持动态注册、版本、权限和灰度？
6. 业务场景下“挂了怎么办、量大怎么办”的 Production 设计正在成为重点。

> 该账号存在大量“整理式”面经，统计时仅作为问题方向信号，不与第一人称原帖等权。

## S044 DeepSeek｜Agent / Harness｜2026-09｜整理/待核实

来源：https://www.nowcoder.com/discuss/925527442863714304

可见问题信号：

1. Harness 与 LangChain 这类应用框架的核心差异是什么？
2. Agent Loop 如何设计 Early Stop / Budget / Max Step，既避免无限循环又不误杀有效长任务？
3. 多人协作 Agent 平台如何设计共享状态、权限和调度？

> 来源真实性尚不足以当作独立“公司真实场次”强证据，先保留为低权重信号。

## S045 字节跳动｜豆包 Seed / Agent 开发｜2026-08｜整理/待核实

来源：https://www.nowcoder.com/discuss/922625105077751808

可见问题信号：

1. 多轮对话和复杂任务下，Agent 对话状态如何管理？
2. ReAct Loop 每一步输入输出协议如何定义？
3. Tool Call JSON 或参数错误时，Runtime 如何校验与恢复？
4. Multi-Agent 如何通信、传递状态并处理子 Agent 故障？

## S046 阿里云｜可观测存储 AI Agent 工程岗｜2026-08-25｜原始/第一人称

来源：https://www.nowcoder.com/discuss/923528884249710592

可见问题：

1. Agent 的存储查询优化是怎么做的？
2. 如何从 Agent 上层查询优化继续追到存储层的 IO / SSD / 磁盘成本？
3. 一次“存储查询”的完整路径中发生了什么？
4. 对 AI 应用工程师而言，什么时候需要理解到底层存储，而不仅是 ORM / SQL？

## S047 钉钉｜一面｜2026-04-15｜原始/第一人称

来源：https://www.nowcoder.com/feed/main/detail/65b882e8ef5b4e4abf589368c27feae9

可见问题：

1. 阻塞 / 非阻塞与性能之间是什么关系？
2. RAG 完整链路如何描述？
3. Graph / Graph RAG 如何构建？
4. MCP 的定义、优势和适用边界是什么？
5. 文档切分完整流程如何设计？
6. 除 Milvus 外还了解哪些向量数据库，如何比较？
7. AI Coding 产出错误时，是自己修、让 Agent 修，还是使用自动验证闭环？
8. 除 Coding 外，AI Agent 还能落地哪些真实业务场景？

## Batch 04 新增信号

这一批与前三批相比出现了几个非常清晰的新趋势：

- **Harness 已经从“名词”变成 Runtime Debugging 问题**：延迟退化、取消、Early Stop、消息协议、State 隔离、Tool 参数可靠性、Compaction 保真。
- **成熟 Agent 产品源码开始直接进入面试**：Codex、Claude Code 的 Context / Memory / Runtime 实现已经被直接追问。
- **长程任务的生命周期成为核心**：Cancel、Lease、Retry、Resume、Duplicate Execution、Side-effect Idempotency。
- **RAG 开始进入 TB 级数据工程**：OCR / 版面解析、跨页 Chunk、Embedding 成本、增量索引，而不仅是“切块 + 向量库”。
- **传统后端仍然与 Agent 深度耦合**：Redis 锁和过期、Kafka 可靠性、MySQL/CAS、线程安全调度、大文件流式处理。
- **来源质量必须分层**：随着 Agent 面经热度增加，牛客出现越来越多整理/付费专栏式内容，不能把它们与第一人称原始面经等权统计。
