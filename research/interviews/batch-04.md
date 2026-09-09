# Batch 04 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> 本批继续执行统一固定准入：**真人面试官 + 候选人本人第一人称 + 高信息密度 + AI Application / Agent 目标岗位 + 正文可稳定核验 + 非转载重复**。
>
> 本轮继续扩大搜索 Recall，但没有为了数量降低门槛。搜索覆盖牛客公开原帖、企业 / 话题索引以及牛客之外的公开搜索结果；CSDN / 聚合站 / 题库站中大量“完整答案、高手解析、学员复盘、资源导流”内容全部排除。
>
> 问题均为简洁转述，只保存面试研究所需的信息，不复制第三方正文。

---

## S052 阿里｜Agent 开发｜校招一面｜2026-02-27｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/79bb100d34fb45c8a2c2d395561e028b

真人 / 第一人称证据：作者直接以“凉经”记录自己的阿里 Agent 一面，开头保留明显的面后挫败感；问题围绕本人实习与多模态知识库项目连续深挖。

高价值问题：

1. 文档中图片等异构内容如何解析、加工，并避免最终只返回文字而丢失视觉信息？
2. 大规模文档下人工建立图文对应关系是否可扩展？
3. 多模态解析后的回答正确性如何验证，错误如何检测？
4. 使用另一个 LLM 做评测时，Judge 本身的正确率与一致性如何验证？
5. 用户问题不在知识库中时，系统何时拒答、何时澄清、何时请求补充信息？
6. Retrieval Recall、Faithfulness 等指标如何定义和计算？
7. LoRA 的作用、收益和真实落地情况如何说明？
8. Python / Java、多线程、类加载和 MQ 等基础能力为什么仍会在 Agent 岗被追问？

去重说明：检索到 03-10 的另一篇几乎相同题序帖子，视为重复信号，不重复计数。

---

## S053 阿里云｜AI Agent 开发｜一面｜2026-03-05｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a1a7c399c264425fa9ff0b051d9c4407

真人 / 第一人称证据：作者以同岗一面问题清单发布并明确“攒人品”，题目从本人实习 / 项目持续追到工作流、部署、数据库和 RAG，具有自然面试顺序。

高价值问题：

1. Agent / Workflow 项目是如何搭建的？
2. Workflow 的效果如何评测？
3. 项目采用单体还是微服务部署，Kubernetes 在其中承担什么职责？
4. DDD 如何理解并用于业务建模？
5. MySQL 多表更新应注意什么？
6. Redis Pub/Sub 的机制和适用边界是什么？
7. 工作流设计如何考虑可用性？
8. 分库分表在真实项目中如何落地？
9. RAG 在系统中的职责和链路如何解释？

---

## S054 快手｜AI 应用开发｜日常实习一面｜2026-02-12｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b0a3346badb4410da60e1aa46e570451

真人 / 第一人称证据：作者明确写“前段时间面的、约 40 分钟”，并以自己的日常实习一面复盘发布；题目从项目连续进入 Memory、RAG、Vector DB、Python 与 HTTP。

高价值问题：

1. LangGraph 相比 LangChain 的工程差异是什么，State Snapshot 大致如何实现？
2. Vector Memory 如何更新用户画像，短期和长期 Memory 如何区分？
3. Safety Guardrail 如何做敏感信息拦截？
4. RAG Chunk 粒度如何选择？
5. IVF_FLAT 与 HNSW 的核心差异和适用场景是什么？
6. CoT 为什么可能帮助复杂任务推理？
7. 常见 LLM Hallucination 如何从工程层治理？
8. Function Calling 从 Tool Selection 到执行结果回传的流程是什么？
9. vLLM PagedAttention 的思想是什么？
10. Python list / tuple、decorator 与 HTTP GET / POST 等基础如何解释？

---

## S055 快手｜AI 应用开发｜实习一面｜2026-04-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d554c8c779b44d78ad5371819f1ff38e

真人 / 第一人称证据：候选人直接写“给我面没招了”，以本人一面复盘发布；问题明显围绕其 AI 工具使用与知识库项目继续追问，而非标准题库排序。

高价值问题：

1. 日常开发如何使用 AI Coding、MCP、Skill 等工具提升效率？
2. 使用 AI 生成前后端代码时如何组织开发流程？
3. Spec / 规范驱动开发在 AI Coding 中解决什么问题？
4. System Prompt 与 User Prompt 的职责有什么区别？
5. RAG 中 Query Rewrite 和多层递进检索如何设计？
6. 如何定义“没有检索到知识”，阈值应怎样通过实验确定？
7. Retrieval Accuracy 如何测量？
8. RAG 的主要局限是什么，哪些场景应考虑其他方案？
9. CI/CD 如何接入 AI 应用工程流程？

---

## S056 京东｜AI 应用开发｜实习一面｜2026-04-14｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ef1605e55cc0498c8e23a1da10bc82b8

真人 / 第一人称证据：作者以 AI 应用开发同岗一面分享发布并主动邀请同岗交流；问题围绕本人平台项目是否真实上线、为何自研、团队规模和量化指标逐层追问。

高价值问题：

1. 项目是自主尝试还是业务需求，为什么值得做？
2. 平台提供什么能力，是否真实部署、上线和被用户使用？
3. 为什么选择自研部署而不是成熟 SaaS / 开源产品？
4. 企业 Knowledge Base 如何构建？
5. 模型如何选型和部署？
6. 并发压力和索引优化具体如何处理？
7. “专有名词召回提升 30%”这类指标如何定义并证明？
8. Query Decomposition 在检索中如何使用？
9. 如何持续关注并判断新的 AI 产品是否值得引入？

---

## S057 快手｜AI 应用开发｜留用实习一面｜2026-08-26｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/631e9b79e433415ca3dea24642f94b4c

真人 / 第一人称证据：作者明确写出公司、岗位、35 分钟时长，并二次更新“第二天约二面、因没有转正 HC 拒绝继续”；真实性与时间线非常清晰。

高价值问题：

1. 智能体平台如何接入 IM / 对话入口？
2. Clarification / 反问机制是什么，什么时候触发？
3. 一次完整问答链路如何流转？
4. Intent Tree / Intent Classification 如何设计？
5. 意图识别准确率如何评测？
6. Evaluation Dataset 如何构建，规模多少，谁负责维护？
7. MCP Tool 调用需要注意哪些 Failure Case？
8. Tool 调用失败后如何恢复？
9. 用户量、日会话量等真实规模如何影响 Agent Service 设计？

---

## S058 腾讯｜AI 应用开发｜日常实习二面｜2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/98687348b95f4f61b3e7edbc631a7790

真人 / 第一人称证据：作者明确写二面 1 小时，面试官连续质疑“哪些是你真正做的”，问题高度绑定其 Multi-Agent、医学语料和 GraphRAG 实习工作，具有很强真人项目验真特征。

高价值问题：

1. Multi-Agent 架构中本人究竟负责什么，哪些是团队已有设计？
2. Agent End-to-End Success Rate、Tool Miscall Rate 如何量化与改进？
3. 医学语料预处理如何分工和落地？
4. Layout-aware PDF Parsing 使用什么工具，是否横向比较过其他方案？
5. 噪声、重复片段和 Chunk Boundary 如何治理？
6. 跨页 / 被切断的表格如何识别与修复？
7. GraphRAG 的 Triple Extraction 如何做，LLM 抽取错误怎样发现？
8. Community Summary 的设计目的是什么？
9. GraphRAG、Vector Retrieval、Hybrid Retrieval 如何做横向量化对比？
10. 现场 AI Coding：从文本抽取 Entity / Relationship / Claim 并输出规范结构。

---

## S059 蚂蚁｜Agent 开发｜暑期一面｜2026-04-15｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/0bdc61d927e94d0a8ec5997343126276

真人 / 第一人称证据：作者以“Agent 开发一面”发布并记录本人实习被连续深挖；问题集中在长任务、Redis、代码影响分析与 Sandbox，呈明显工程场景追问链。

高价值问题：

1. Long-running Task 卡住时，Runtime 如何感知 State Transition？
2. 如何用定时任务 / 补偿机制恢复长期任务？
3. Redis ZSet 分片扩容发生 Rebalance 时如何减少阻塞？
4. 多实例环境中 Distributed Lock 如何正确使用？
5. 修改通用鉴权方法时，Coding Agent 如何分析全站影响范围？
6. IDE 的 Call Hierarchy / Jump-to-definition 背后需要什么代码索引能力？
7. RAG 召回过期且危险的运维指令时，系统层如何阻止执行？
8. Sandbox 在 Agent 执行外部操作时应隔离哪些风险？

---

## S060 拼多多｜AI Agent｜提前批一面｜2026-08-17｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/d0c1a59663a2408fb9f8b52b87ccaaec

真人 / 第一人称证据：候选人记录提前批进面、现场 Coding 先写暴力解后被面试官要求继续优化，以及反问环节；属于明显的个人面试现场记录。

高价值问题：

1. LLM API 调用失败有哪些常见原因？
2. 如何判断调用是否真正成功，并建立系统化排查路径？
3. 除 Rate Limit 外，Model Provider 还会有哪些 Failure Mode？
4. Agent 对话历史记忆不足时如何优化？
5. 多个 AI Role 同时存在时，用户信息、角色状态与 Memory 如何隔离？
6. 多轮历史如何既保持可用，又避免 Context 无限增长？
7. Coding：判断两棵树是否相同，并根据面试官反馈继续优化实现。

去重说明：检索到后续另一篇高度相同的题序帖子，不重复计数。

---

## S061 拼多多｜AI Agent｜提前批线下两轮｜2026-07-25｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/45f6e73f8e9d4888b9c066a160f89f60

真人 / 第一人称证据：作者明确记录 AI Agent 岗、两轮各约 1 小时、两位面试官业务方向不同、没有进入三面，并保留自己“协作问题答得差、动态规划不会”等现场状态。

高价值问题：

1. Dual Analysis Agent + Judge Agent 与 Analysis Agent + Validator 的结构差异是什么？
2. Claude Code、Hermes、OpenClaw 等 Agent 产品架构如何比较？
3. Agent Accuracy 如何定义，Regression Test 怎样覆盖版本改动？
4. 测试失败后如何定位是模型、Prompt、Tool 还是 Runtime 的问题？
5. Workflow 与 Agent 如何做方案取舍？
6. Function 与 Skill 应在什么场景分别使用？
7. 线上 OOM 如何定位和治理？
8. 多人协作开发对 Agent 工程提出哪些额外要求？

---

## S062 中兴通讯｜Agent 开发｜实习一面｜2026-05-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/81ef46253510446d93530b20fcb0815f

真人 / 第一人称证据：作者以“实习 Agent 开发一面凉经”发布，正文围绕自己的医疗科技实习持续追问 RAG 细节，并保留学校、毕业时间、实习时长等自然面试信息。

高价值问题：

1. 从原始文本到企业 RAG Knowledge Base 的完整处理链路是什么？
2. Chunk / Token 阈值与 Vector DB / Cache 的存储设计是否合理？
3. 如果内容没有进入向量索引，查询时如何还能找到它？
4. 用户自然语言表达高度变化时，Retrieval 稳定性如何保证？
5. 文本是如何被 Embedding Model 转换成向量的？
6. Embedding Model 如何选，是否需要 GPU？
7. Knowledge Base 应部署在本地还是企业服务端？
8. Knowledge Distillation 在应用工程中是什么？
9. Skill 是什么，是否自己真正写过？
10. Cursor / AI Coding 与独立编码能力如何平衡？

---

## S063 字节跳动｜Agent 全栈｜一面｜2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b62416eaa3764a9ba46269c0058019fd

真人 / 第一人称证据：作者以“字节 Agent 全栈一面”发布并标注发面经，评论中补充自己最终凉经；问题按项目 → SQL → Agent → RAG → Multi-Agent → Coding 顺序展开。

高价值问题：

1. Agent / Coding Benchmark 如何衡量模型生成效果？
2. SQL 多表查询和 Slow Query 如何定位与优化？
3. Agent 如何产生 Tool Call，如何判断什么时候应该调用 Tool？
4. MCP 解决了 Tool Integration 的什么问题？
5. Context Window 满了以后有哪些 Compaction 方法？
6. RAG 的完整 Retrieval / Embedding 链路是什么？
7. Agent Memory 如何存储与管理？
8. Multi-Agent 如何协作、传递 Context 与 Task State？
9. Multi-Agent Workflow 和输出质量如何量化评估？
10. Coding：Merge Intervals、LRU。

---

## S064 字节跳动｜大模型应用开发｜实习一面｜2026-03-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/95b8c6edf3ad46818b94605675a12089

真人 / 第一人称证据：作者明确写一面 1 小时，并以“给我面没招了、发面经攒人品”发布；问题横跨本人项目、FastAPI、Python Async、RAG 和 Multi-Agent。

高价值问题：

1. Recursive Character Splitter 相比固定长度 Chunk 的优势是什么？
2. Milvus 中 Collection 与 Partition 如何用于分类检索？
3. Agent Reflection 在应用中如何落地？
4. Function Calling 从模型生成参数到本地执行再回传结果的完整链路是什么？
5. FastAPI Middleware 与 Dependency Injection 分别适合处理什么逻辑？
6. Python multiprocessing 与 threading 如何组合提升吞吐？
7. `asyncio.gather` 与 `as_completed` 有何差异，单个模型超时如何降级？
8. Prompt / Context 过长时，除了截断还可以怎样治理？
9. Multi-Agent State Sync 的主要难点是什么？
10. A2A 如何避免两个 Agent 递归对话？

---

## S065 字节跳动｜Agent 开发｜二面｜面试 2026-07-18，发布 07-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/eccea78e38b447c9a3ae73570c5d00b6

真人 / 第一人称证据：作者明确记录二面日期、整体交流体感并以个人面经发布；问题围绕本人学校项目与 Agent 设计逐层讨论。

高价值问题：

1. Agent Framework 选型应该看什么，为什么不能只会 LangChain？
2. Agent 的核心组件和 Runtime Mechanism 如何描述？
3. Planning 应由 Framework 还是 Model 承担？
4. Planning 有哪些实现范式？
5. Short-term / Long-term Memory 分别解决什么问题？
6. Function Call / Tool Result 是否应该进入短期会话历史，为什么？
7. MCP / 自定义 Tool 的工程收益和代价是什么？
8. RAG Recall 参数如何调优并验证？
9. Python 基础与 Coding 如何结合实际工程表达？

---

## S066 腾讯｜AI 应用开发｜实习一面｜2026-05-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/35b5651df49241298b951c6e6bdf5b19

真人 / 第一人称证据：作者以同岗实习一面发布并明确“攒人品”；题目从真实服务监控与 Prompt 模块化连续追到 RAG、Context、SSE、Memory 与 Agent 产品。

高价值问题：

1. AI Application 的 Prometheus Metrics 应覆盖哪些业务 / 服务指标？
2. Prompt、MCP 等调用模块为什么要抽象成独立层？
3. 切换基础模型以后 Prompt 是否需要重新适配？
4. 预设 Prompt 过长或包含敏感内容时如何检测和治理？
5. 长 Prompt 被切分后如何避免语义损伤？
6. RAG 与 Fuzzy Search 有什么差异，如何提高 Recall？
7. Context 的边界到底包含什么，Tool Schema / Tool Result 是否属于 Context？
8. SSE 在 AI Streaming Service 中如何工作？
9. Memory Module 应如何分层设计？
10. 如何从工程角度理解 OpenClaw 等 Agent 产品？

---

## S067 OPPO｜AI 全栈｜一面｜面试 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/cf5a82411c1e473385d8fcae6c250a6e

真人 / 第一人称证据：作者明确写 8 月 13 日、第一次正式面试，并保留自己在 HTTP 状态码处卡壳、面试官切换到会的问题、对面试氛围的感受和反问内容。

高价值问题：

1. 用户 Prompt 进入系统后到前端输出，中间经历哪些 AI / Backend 处理？
2. 为什么按 Paragraph Chunk，效果如何验证？
3. 如何判断证据不足并让系统拒答？
4. 为什么选择 Multi-Agent，而不是一个大 Agent？
5. Short-term / Long-term Memory 如何理解？
6. 常见 HTTP Status Code 在 Service Debugging 中意味着什么？
7. Hallucination 如何发现和缓解？
8. AI 全栈岗位里前端性能问题如何定位和优化？

---

## S068 字节跳动｜后端 Agent 开发｜暑期二面｜2026-04-08｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1b2e5502708e4a0fba3d281f9b371de3

真人 / 第一人称证据：作者以暑期实习二面个人记录发布；面试官要求白板画系统架构，并沿模块、通信、RAG、Tool、Auth、Prompt、Context 继续追问，现场链路非常清晰。

高价值问题：

1. 白板从零画一个 Agent Backend 的系统架构，应包含哪些模块？
2. 模块之间如何通信？
3. RAG 文档 Processing / Incremental Update 如何组织成独立 Pipeline？
4. Tool 应如何设计，怎样挑一个复杂 Tool 解释完整执行链路？
5. Single-Agent 与 Multi-Agent 如何选？
6. Authentication 与 Validation 如何放在 Agent Service 边界？
7. System Prompt 如何构造？
8. Long / Short Context 如何管理？
9. Agent 如何知道有哪些 Tool 可用？
10. RAG 相比直接把大量文档塞进 Context 的优势是什么？

---

## S069 腾讯｜AI 应用开发｜实习一面｜2026-03-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1a94be753ca94a0dbe4616f140d4501f

真人 / 第一人称证据：作者以同岗实习一面发布并“攒人品”；题目从本人项目与 Rerank 继续进入 Context / Memory、限流、Redis、MySQL，能很好代表 AI Application Foundation 的真人考察。

高价值问题：

1. Rerank 后 Top-K 如何选择，K 值如何通过实验验证？
2. Context Engineering 与 Memory 如何实现？
3. LRU 的核心数据结构和复杂度是什么？
4. Distributed Token Bucket、Leaky Bucket、Sliding Window 如何比较？
5. Redis 如何实现 Sliding Window Rate Limit？
6. Bloom Filter 适合解决什么问题，有哪些缺点？
7. MySQL Index Invalidation 有哪些常见情况？
8. 为什么 MySQL Index 常用 B+Tree，不同 Storage Engine 有什么差异？
9. Isolation Level、MVCC、ReadView 与 Lock 如何联系起来？

---

## S070 阿里云｜后端 Agent 开发｜实习一面｜2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/10dc395d6a704e1ea22a8fbc0049c7da

真人 / 第一人称证据：作者明确写“给我面没招了”，以本人后端 Agent 实习一面发布；问题集中验证 Agent Backend 所需的 OS / Network / MySQL / Redis Production 基础。

高价值问题：

1. Connect / Read / Write 等 Timeout 分别解决什么问题？
2. select / poll / epoll 的核心差异是什么？
3. CPU Load 与 CPU Usage 不一致时如何诊断？
4. 磁盘满但找不到大文件时如何排查？
5. OS Memory Reclaim / Threshold 设置错误会导致什么？
6. MySQL Back-to-table 如何产生，怎样用 Covering Index 等方式避免？
7. DB Connection Pool 打满如何发现与处理？
8. SQL Injection 如何防？Auto Increment ID 到上限怎么办？
9. Redis + Lua 如何保证库存扣减等多步骤原子性？
10. Cache Logical Expiry、Physical Expiry、Distributed Lock 与 Sliding Window Rate Limit 如何设计？

---

## S071 字节跳动｜AI 应用开发｜实习一面｜2026-05-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/516e7ae39c054e209c7e8baad42def18

真人 / 第一人称证据：作者明确以 27 实习 AI 应用开发一面发布并邀请同岗交流；问题从本人 AI Coding / Agent 实践一路追到推理服务、RAG、MCP 和 Multi-Agent。

高价值问题：

1. 如何使用 AI Coding 开发一个真实 AI Agent？
2. LangChain / LangGraph 的使用体验和工程边界是什么？
3. AI 应用部署在云上时需要哪些基础设施能力？
4. 常见 LLM Inference Engine 和关键推理指标有哪些？
5. Prefill / Decode 分离解决什么问题，KV Cache 在系统中如何影响资源？
6. Prompt 如何设计和迭代？
7. RAG 如何构建？
8. Fine-tuning 项目做过什么，如何说明它与应用层的边界？
9. MCP 是什么，Tool Call 失败如何恢复？
10. Structured Output 如何保证？
11. Multi-Agent Workflow 如何组织？

---

## S072 阿里｜大模型应用开发｜一面凉经｜2026-06-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/ad38af692250449380e373dda5d74048

真人 / 第一人称证据：作者明确以个人“凉经”发布，并记录自己当场回答过哪些方向；面试官围绕其文档处理链路、Hybrid Retrieval 和 RRF 参数连续追问。

高价值问题：

1. 文档上传 → Parse → Chunk → Embedding 链路为什么适合用 MQ 异步解耦？
2. 为什么纯 Vector Retrieval 对专有名词 / 制度条款可能表现较差？
3. Keyword Retrieval + Vector Retrieval 如何融合？
4. 为什么使用 RRF，而不是简单线性加权？
5. RRF 的 `k` 参数如何调，为什么某个默认值不能直接照搬？
6. Chunk Size / Overlap 为什么这样选，参数过大过小有什么问题？
7. 如何用实验验证 Chunk 参数的效果？
8. GraphRAG / TreeRAG 分别适合什么问题？
9. Graph 如何构建，GraphRAG 的主要工程难点是什么？

---

## S073 点点互动｜Agent 开发｜秋招一面｜2026-08-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/31f72c4716744e4686fbe3d70b778b19

真人 / 第一人称证据：作者以“秋招一面凉经”发布，明确岗位为 Agent 开发，问题从实习项目进入 Agent Loop、Failure、Cost、异步连接与 Redis，并附现场算法题。

高价值问题：

1. Agent 的基本模块有哪些？
2. 从 User Input 到 Final Answer 的完整 Agent Chain 如何运行？
3. Agent Failure 常见原因有哪些？
4. Agent 一直循环时怎样检测并终止？
5. 如何控制 Agent Latency 与 Cost？
6. ReAct 与 One-shot LLM Call 的本质区别是什么？
7. ReAct 常见工程问题有哪些？
8. 为什么跨 Event Loop 复用连接会出错？
9. Redis 在 Agent System 中能承担哪些职责？
10. Coding：最长无重复子串。

---

## S074 阿里淘天｜Agent 开发｜一面凉经｜2026-04-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/edbf58731d884f8f9e094a9b2eda0cf9

真人 / 第一人称证据：作者明确写“面没招了、发点面经攒人品”，问题围绕本人 LangGraph / RAG 项目连续追问，具有明确真人项目验真特征。

高价值问题：

1. LangGraph 与 LangChain 的差异是什么，为什么项目选择 LangGraph？
2. Graph Node 之间的 State 如何流转？
3. 如何验证某个 Node 的效果，而不是只看最终回答？
4. Agent / Workflow Observability 如何设计？
5. Prompt Combination / Prompt Assembly 如何实现？
6. RAG 项目如何组织完整链路？
7. Chunk 如何切分，Overlap 如何设置？
8. Embedding Model 如何选型？
9. 简历中声明的效果数据如何验证？
10. 图片和表格如何解析，若重新做一次会如何改进？

---

# 本轮明确排除

本轮扩大搜索时，以下内容即使“题很多”仍未进入正式 Batch：

- CSDN / AtomGit / 聚合面试站中“必杀技、满分答案、高手解析、学员复盘、题库导航”等二次内容；
- 把他人面经包装成“录友 / 粉丝上岸复盘”的课程或社群导流文章；
- 搜索摘要显示为真实面试，但正文无法稳定打开或无法确认候选人本人身份的帖子；
- 与已有来源题序、措辞高度一致的重复转载 / 二次发布；
- 自动 AI 面试、纯算法训练、大模型训练 Infra、传统数据分析 / BI 等非目标岗位；
- 目标岗位标题虽然正确，但正文明显以“标准答案提示”而不是候选人面试过程为主体的内容。

# Batch 04 观察

本批新增 `S052–S074` 共 **23 个 HUMAN-A 来源**，当前干净核心样本达到 **74 个**。

本轮最值得注意的不是“又出现了多少新名词”，而是整条能力路线继续得到独立真人样本支持：

1. **Python / FastAPI / Async 已经是 AI Application Service 的真实面试主线**：FastAPI Middleware / DI、multiprocessing / threading、`asyncio.gather` / `as_completed`、Event Loop、HTTP / SSE 等被直接追问。
2. **MySQL / Redis / OS / Network 没有消失**：索引、MVCC、回表、连接池、Redis Lua / Lock / Rate Limit、I/O Multiplexing、CPU / Disk Debugging 继续与 Agent / RAG 同场出现。
3. **RAG 更强调“可证明”**：Chunk、Rerank、Hybrid Retrieval、RRF、GraphRAG、Layout-aware Parsing 不只问怎么做，还追“为什么这样做、指标怎么定义、收益怎么证明”。
4. **Agent Runtime 更强调执行边界和 Production Failure**：Long-running Task、State Compensation、Tool Failure、Sandbox、Context / Memory、Multi-Agent State、OOM、Cost / Latency、Regression Evaluation 都来自真人技术面。
5. **项目真实性是高频验真点**：是否上线、用户量、团队分工、个人贡献、是否自主设计、量化收益、Benchmark 是否可信，经常比“背框架 API”更重要。

当前仍未出现来源饱和迹象；继续扩大 Recall 时保持同一 HUMAN-A 标准，不设每批固定数量目标。