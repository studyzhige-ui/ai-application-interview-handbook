# Batch 08 — AI Application 全链路高质量面经（岗位范围收紧批）

采集日期：2026-09-09

> 本批继续执行“宁缺毋滥”，并新增 `research/quality/role-scope-policy.md`：只把 **AI 应用开发 / Agent 开发 / AI 全栈 / 大模型应用 / AI 后端 / Agent Runtime** 等与目标方向直接相关的岗位纳入正式样本。
>
> 传统数据分析、BI、纯推荐算法、纯训练/Infra、以及“传统后端只顺带问一句 AI Coding”的场次不进入本批统计。
>
> 本批刻意覆盖整条能力链，而不是只搜 Harness：Python / FastAPI / MySQL / Redis / MQ / Vector DB / RAG / Agent / Production Engineering 都可以出现，但前提是它们来自目标 AI 岗位的真实面试。

---

## S087 字节跳动｜大模型应用开发实习一面｜2026-03-21 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/95b8c6edf3ad46818b94605675a12089

高价值问题：

1. RAG 递归字符切片相比固定长度切片的优势和适用边界是什么？
2. Milvus 中按文档分类检索时，多个 Collection 与 Partition 应如何取舍？
3. Function Calling 从模型生成结构化参数到本地代码执行、再把结果返回模型的完整链路是什么？
4. FastAPI Middleware 与 Dependency Injection 分别适合承载哪些逻辑？
5. Python `multiprocessing` 与 `threading` 如何组合以提升不同类型任务的吞吐？
6. `asyncio.gather` 与 `asyncio.as_completed` 在并发请求多个模型时有什么差异？单个模型超时如何降级？
7. Context Window 溢出时除了硬截断，还能如何压缩、筛选和保留关键信息？
8. Multi-Agent 的状态同步难点是什么？A2A 场景如何避免两个 Agent 陷入递归对话？

价值：非常典型的 **Python Runtime + FastAPI + RAG + Agent** 同场深挖，是统一知识路线的重要样本。

---

## S088 佰聆数据｜助理 AI 应用开发工程师实习一面｜2026-07-14 面试 / 07-15 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/discuss/906897383676538880

高价值问题：

1. LLM 结构化输出在 Python 中如何做 JSON / Schema 校验？
2. Agent Skill 与 Prompt Engineering、MCP 分别解决什么问题？
3. A2A / Sub-Agent 的协作关系如何设计？
4. Context Management 应如何组织长期对话和任务信息？
5. 前端与 Agent 服务之间采用什么通信协议更合适？
6. 如果用 FastAPI 承载一个类似 Claude Code 的完整系统，除了路由接口还缺哪些服务能力？
7. FastAPI 所处 Web Server / ASGI 运行栈应该如何理解？
8. 如果只选一个 Python 知识点证明自己的 Python 深度，会选择什么并如何展开？

价值：直接暴露了我们必须单独学习 **FastAPI / ASGI / Schema / Agent Service**，不能只会写 `@app.post()`。

---

## S089 字节跳动｜AI 全栈研发实习生一面｜2026-06-05｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/73f02711ba764ec096cfe2a5798a5048

高价值问题：

1. MySQL 脏读、幻读在项目中如何处理？
2. 三个高频查询字段如何设计索引？`LIKE` 与联合索引如何判断是否能命中？
3. Redis 如何避免缓存击穿，AI 服务里一般保存什么数据？
4. RAG 的文档格式、入库流程、检索流程、Chunk 与向量维度如何设计？
5. 检索准确率如何优化，除了简单加权还有哪些重排/融合方案？
6. Kafka 在系统中承担什么职责，如何降低消息丢失与一致性问题？
7. RAG 问答记忆如何设计？
8. 大模型如何完成 Tool Calling？

价值：一场面试横跨 **MySQL → Redis → Kafka → RAG → Memory → Tool Calling**，非常符合 AI 全栈岗位的真实能力画像。

---

## S090 腾讯｜AI 应用开发一面｜2026-07-25 面试 / 07-30 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/a02baa2ac6634904992561494a1746a4

高价值问题：

1. Prompt、RAG、Fine-tuning、Workflow、Agent 应如何根据问题性质选择？
2. 为什么复杂任务不一定都要上 Agent？Workflow 与 Agent 的边界是什么？
3. Context Engineering 的目标是什么，截断与压缩如何避免破坏任务信息？
4. AI 应用上线后应该持续观察哪些质量、延迟、成本和失败指标？
5. 出现线上问题时如何设计降级？
6. Prompt、Model、Retrieval Index 更新后如何做版本管理与回滚？
7. Agentic RAG 相比固定 RAG 解决了什么问题？什么时候反而应该保持固定 RAG？
8. 迭代检索如何限制延迟、Token 与成本？

价值：这不是“背组件定义”，而是在考 **AI Architecture Decision + Production Governance**。

---

## S091 小红书｜AI 全栈开发日常实习一面｜2026-04-02｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/ab913bd0d7c2434e895f4dfc54e96627

高价值问题：

1. 进程和线程的区别是什么？
2. Redis 内存淘汰与 Key 过期删除分别有哪些策略？
3. MySQL 深分页为什么慢，如何改写 SQL 或查询方式？
4. 用户口语化 Query 在 RAG 中检索不到时如何定位和优化？
5. 点赞功能如何做数据模型、并发和缓存设计？
6. Redis Set 形成 BigKey 后如何治理？
7. 算法：最长递增子序列。

价值：说明 AI 全栈的一面仍会直接考 **OS/Python 所依赖的并发基础 + MySQL + Redis + RAG Query**。

---

## S092 京东科技｜AI 全栈 / Agent 研发一面｜2026-06-11｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/e80b257b1c064970a72c9679c2177585

高价值问题：

1. MySQL 慢 SQL 如何定位？为什么有些 SQL 是随着数据量增长才逐渐变慢？
2. UUID 作为 MySQL 主键有什么索引局部性与写入代价？
3. Redis 为什么常被描述为单线程执行命令？缓存与数据库一致性怎么处理？
4. Kafka 的核心优势是什么，Partition 数量如何规划，消息积压怎么处理？
5. 突发流量超过服务容量时如何限流、削峰、降级与保护下游？
6. Agent Bad Case 如何收集、归因和转成评测集？
7. Tool Result 过长导致 Context 膨胀怎么办？
8. Tool 数量太多时如何避免模型选择困难与 Prompt/Schema 膨胀？

价值：非常典型的 **Production Backend + Agent Runtime** 组合。

---

## S093 淘天｜AI 应用开发 / Agent 岗一面｜2026-04-10｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/a0306a045d594b02b63fb0654d517901

高价值问题：

1. BM25 与向量检索的 Hybrid Retrieval 如何融合？
2. 扫描 PDF、OCR 和表格结构化抽取有哪些真实工程难点？
3. Multi-Agent State / Checkpoint 如何避免状态竞争，并如何做全局状态管理？
4. MCP Tool 的标准化输入输出、兼容性与流式结果如何设计？
5. 子任务失败或数据为空时，Workflow 如何 Retry / Degrade？
6. FastAPI + SSE 如何把 LangGraph 节点的中间执行结果实时推给前端？
7. Checkpoint 如何持久化，断线重连后如何 Resume？
8. 向量数据库与索引如何选型，RRF 之后为什么还可能需要模型 Reranker？

价值：RAG、FastAPI Streaming 与 Agent State Runtime 在一场面试中形成了完整链路。

---

## S094 阿里国际｜大模型应用开发一面｜2026-04-23｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/4e5ec0e1d8fa46d5b02b7db3c31beaeb

高价值问题：

1. Agent Step 执行后问题仍未解决，下一轮应该如何处理？
2. Step 执行过程中产生新问题，如何修改计划而不让流程失控？
3. 复杂业务中的 MCP 应如何设计？
4. 不同知识库规模下 RAG 架构、索引和存储选型如何变化？
5. Context Window 与 Token 成本如何控制，又如何评估压缩质量？
6. Short-term Memory 如何晋升为 Long-term Memory？
7. Skill、MCP、Tool 在概念与 Runtime 职责上有什么区别？
8. Skill / Harness 的自我迭代如何避免变成不可控的自修改？如何评测 Skill 好坏？
9. Agent Evaluation 应准备哪些测试集和指标？

价值：强化 **Agent Harness / Skill / Memory / Eval** 的系统边界，而不是框架 API。

---

## S095 联影｜Agent 开发一面｜2026-07-08｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/d5a9001f0d5048518ad85c494d1f6d54

高价值问题：

1. 进程、线程、协程如何区分？
2. Python 如何利用多核？GIL、多进程、C Extension 与 Async I/O 各解决什么问题？
3. Temperature / Top-p 对生成行为有什么影响？
4. BM25 + Vector 双路召回后，进入 Reranker 的候选量怎么定？
5. Reranker 是否可以删除？排序变化为什么会影响最终回答？
6. Chunk 数量、LLM 调用次数和延迟成本如何权衡？
7. 医疗设备等离线 / 私有部署场景下，RAG 如何处理 Docker 镜像、Local Model、Private Vector Store、权限、日志脱敏和版本管理？
8. GraphRAG / Agentic RAG 适合解决什么问题？

价值：把 **Python 并发基础 + RAG 检索 + 私有化 Production** 串得非常完整。

---

## S096 OPPO｜大模型应用开发一面｜2026-03-26｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/06aa48522cef44dfa62cbdda528cde6f

高价值问题：

1. GraphRAG 中 Graph 具体承担什么作用，为什么可能比普通 RAG 更合适？
2. 检索系统如何理解 Recall、MRR、Accuracy 等指标？
3. 除 LLM-as-a-Judge 外，还有哪些回答质量评测方式？
4. 多个专家对同一答案评分分歧很大时，评测体系如何处理？
5. 常见 Agent 与 Memory 管理范式有哪些？
6. 实际工程中最难的一次编码问题是什么，如何定位和解决？

价值：补强 **Evaluation Reliability**，提醒我们“有一个 Judge 分数”并不等于评测可靠。

---

## S097 文远知行｜AI 全栈开发三面｜2026-08-18｜原始/第一人称｜A

来源：https://www.nowcoder.com/discuss/920018465497382912

高价值问题：

1. 高并发交易场景中如何保证 Redis 与 MySQL 的一致性？
2. 用户购买后立即退款时，库存 / 订单 / 缓存状态如何保持可恢复的一致性？
3. pgvector 中文本如何经过 Embedding 变成可检索向量？
4. Reranker 在 RAG 中解决什么问题？
5. RAG 还有哪些更进一步的检索/推理模式？
6. 算法：BFS。

价值：来自明确 AI 全栈岗位，基础数据库一致性与 Vector/RAG 同场出现；只保存问题本身，不把帖子中候选人的答案提示当成标准结论。

---

## S098 淘宝闪购｜AI 全栈开发一面｜2026-08-20 面试 / 08-25 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/0b09c812c2964a12a41ac222101bf228

高价值问题：

1. 消息队列如何避免重复消费？
2. 消息消费失败后如何 Retry、Dead Letter 或人工恢复？
3. 服务 OOM 应该如何系统排查？
4. 如何从 0 搭建一个前后端协作的系统？
5. Multi-Agent 之间如何通信？
6. 如果让你测试一个 Agent 项目，测试维度和用例如何设计？
7. Coding：无重复字符最长子串、LRU。

价值：把 **可靠消息 / OOM Debugging / Agent Test / Coding** 放到同一个 AI 全栈面试中。

---

## S099 字节跳动｜Agent 开发一面｜2026-09-03 面试 / 09-04 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/discuss/925342611194286080

高价值问题：

1. 如何理解 Agent Harness？
2. 长程任务历史上 5 分钟完成，某次退化到 15–20 分钟，如何定位延迟来源？
3. Tool 有固定 Schema 时，如何保证模型结合 Context 生成可靠参数并安全执行？
4. 多轮任务 Context 不断增长应该如何治理？
5. Compaction / Summary 不可避免丢信息，如何尽量保住 Task Constraint、关键事实和未完成状态？
6. RAG 的离线上传与在线问答链路如何设计？
7. Coding：约束数字集合下求小于 N 的最大数。

价值：非常新鲜的 **Harness / Long-running Runtime / Tool Reliability / Context Compaction** 一线信号。

---

## S100 美团｜AI 后端工程师一面｜2026-09-02 面试 / 09-04 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/discuss/924679647910993920

高价值问题：

1. 项目是否真正承担过从运营配置到用户触达的端到端业务链路？
2. MySQL MVCC 应如何解释？
3. Kafka 的核心机制是什么？
4. Kafka 以 User ID 作为 Partition Key 时会带来哪些热点、负载倾斜和扩缩容问题？
5. 算法：二叉树层序遍历。

价值：问题数量不多，但公司、岗位、日期和轮次明确；它说明 AI 后端一面依然会用 **数据库 + MQ + 真实业务链路** 验证工程基本功，因此作为 A 级有效样本保留。

---

# Batch 08 结论

这一批最重要的不是又增加了多少 Agent 新名词，而是进一步验证了我们现在的统一路线：

```text
Python Runtime
   ↓
FastAPI / ASGI / Streaming
   ↓
MySQL / Redis / MQ
   ↓
Vector DB / RAG
   ↓
Agent / Harness
   ↓
Production / Evaluation / System Design
```

同一场 AI 应用面试经常横跨其中 3～6 层。因此后续搜集必须同时满足两点：

1. **岗位方向正确**：服务 AI Application / Agent，而不是借其他岗位的问题“凑基础题”。
2. **完整保留该 AI 岗位实际问到的基础能力**：不能因为我们更关注 Agent，就把 Python / FastAPI / MySQL / Redis / MQ 从原面经里人为裁掉。

本批新增正式来源 `S087–S100`，全部按第一人称高置信 A 级样本处理。低质量短视频、SEO 标准答案文、模拟题库和与目标岗位无关的数据分析/推荐算法面经均未纳入。