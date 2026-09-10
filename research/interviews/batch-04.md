# Batch 04 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-09

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **23** 个正式来源。

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

## S057 快手｜AI 应用开发｜留用实习一面｜发布 2026-08-26，35min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/631e9b79e433415ca3dea24642f94b4c

真人 / 第一人称证据：作者明确写公司、AI 应用开发岗位和 35 分钟时长；问题连续深挖本人智能体平台。次日作者二次编辑，记录已约二面但被告知没有转正 HC，因此主动拒绝二面，招聘时间线完整。

高价值问题：

1. 项目中真正与 AI 相关的部分是什么，另一个项目是否真的属于 Agent？
2. 智能体平台以什么产品形态存在，是否接入 IM？
3. Clarification / 反问什么时候触发，怎样实现？
4. 从用户输入到最终回答的完整问答链路是什么？
5. Intent Tree / Intent Recognition 怎样实现，准确率如何测？
6. Evaluation Set 谁构建、数量多大、怎样证明代表真实业务？
7. MCP Tool 使用时有哪些注意事项，调用失败如何处理？
8. 真实用户规模、每日会话量是多少？
9. 候选人是否真正做过模型训练 / 图像分类，项目边界在哪里？
10. Coding：反转链表；平时如何使用 AI 学习。

去重：URL 与“无转正 HC → 拒绝二面”的流程未在现有 Batch 出现；与其它快手 AI Application / Agent 样本作者和项目链不同。

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

## S062 中兴通讯｜Agent 开发｜实习一面凉经｜发布 2026-05-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/81ef46253510446d93530b20fcb0815f

真人 / 第一人称证据：作者为东南大学候选人，主页能看到连续个人求职记录；本帖明确是“实习 Agent 开发一面凉经 / 发面经攒人品”。面试官围绕候选人在北京医疗科技公司的 RAG 实习逐层挑战具体实现，尤其直接质疑其“>512 Token 存向量库、<512 存缓存”的设计是否能被检索，具有强项目验真痕迹。

高价值问题：

1. 北京医疗科技实习实际做了什么，RAG Knowledge Base 从原始 Text 到可检索数据的完整流程是什么？
2. 候选人所说“大于 512 Token 存向量数据库、小于 512 存缓存”具体是什么意思？如果某部分不进入 Vector DB，查询时如何找到？
3. 用户 Natural Language 表达高度不确定时，RAG Response 的波动和错误怎样评估与治理？
4. Retrieval 中的 Vector Distance 是否来自 Embedding Model，文本向量化过程怎样解释？
5. 实际使用哪个 Embedding Model，为什么？
6. 项目是否使用 GPU，公司是否有训练 / 推理资源，RAG 部署在本地还是企业服务器？
7. Knowledge Distillation 是什么，为什么项目会使用？
8. 是否写过 Skill，Skill 在当前 Agent 体系里是什么？
9. 项目使用哪些语言和开发工具？除了 Cursor，候选人是否能独立编码？
10. Cursor / AI Coding 与本人手写代码各自适合什么场景，怎样证明自己理解生成代码？
11. 英语 / CET6 等沟通能力如何满足岗位需求？

去重：URL 未在 `S001–S230` 出现；“512 Token → Vector DB / Cache 的设计被面试官反问检索闭环”是独特现场题序，历史中未发现同作者同流程或高相似复制。

---

## S063 字节跳动｜Agent 全栈开发｜一面｜面试 / 发布 2026-06-23｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/b62416eaa3764a9ba46269c0058019fd

真人 / 第一人称证据：候选人以本人一面复盘发布，明确项目 `utbench`、实习 SQL 问题与两道现场 Coding；文末自评“细节没讲到位”，并写面试官也觉得总体还行，次日作者在评论区更新“凉经+1”。

高价值问题：

1. `utbench` 如何衡量模型生成效果，Evaluation 指标怎样设计？
2. 实习中的 SQL 多表查询 / Slow Query 是怎样定位和优化的？
3. Agent 调用 Tool 的完整链路是什么，还有哪些调用方式？
4. Agent 如何判断是否需要调用工具，MCP 解决了什么协议问题？
5. Context Window 满后有哪些 Compression 策略，分别会丢什么信息？
6. RAG 的完整链路和 Embedding / Vector Retrieval 如何实现？
7. Agent Memory 如何管理，哪些状态存 Context、Cache 或持久化存储？
8. Multi-Agent 如何协作、隔离上下文并传递 Task State？
9. Multi-Agent Workflow 与生成质量如何量化 Evaluation？
10. Coding：Merge Intervals；实现带输入输出的 LRU Cache，并满足平均 `O(1)`。

去重：URL 与独特项目词 `utbench` 均未在现有来源出现；与已有字节 Agent / AI 全栈面经题序、项目语义和作者流程均不同。

---

## S064 字节跳动｜大模型应用开发｜一面｜发布 2026-03-21｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/95b8c6edf3ad46818b94605675a12089

真人 / 第一人称证据：这是与 S184 不同候选人的独立场次；作者以本人项目为主线连续回答 RAG、Agent、FastAPI、Python Concurrency 与 Coding，信息密度很高。

高价值问题：

1. Recursive Character Splitter 与 Fixed Chunk 有什么差异？
2. Milvus Collection 与 Partition / Metadata Filter 怎样使用？
3. Counseling Agent 中 Reflection 怎样实现？
4. 工业图纸类 Hallucination 怎样通过 Prompt / Post-processing 控制？
5. Function Calling 从模型 JSON 到代码执行再回填结果的完整过程是什么？
6. vLLM PagedAttention 怎样理解？
7. FastAPI Middleware 与 Dependency Injection 的差异是什么？
8. `multiprocessing` 与 `threading` 怎样选择？
9. `asyncio.gather` 与 `as_completed` 有什么差异，Timeout / Fallback 怎样处理？
10. Context Overflow 除了直接 Truncate 还能怎样治理？
11. Multi-Agent State 怎样同步？
12. A2A Communication 怎样避免递归对话 / 无限互调？
13. Coding：LRU。

---

## S065 字节跳动｜Agent 开发｜二面｜面试 2026-07-18，发布 07-24｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/eccea78e38b447c9a3ae73570c5d00b6

真人 / 第一人称证据：作者“找工小蜜蜂”明确给出二面日期 7 月 18 日，并写整场基本在与面试官聊天；评论继续围绕岗位、项目和后续流程核验。作者主页还能看到更早一次字节暑期 Agent 一面凉经，当前场次时间更晚且为独立流程，未与旧流程混算。

高价值问题：

1. 两个项目是不是学校项目，硕士期间实验室真实做了什么？
2. 为什么做当前 Agent 项目，项目出发点是什么？
3. Agent Framework 如何选型，除了 LangChain 还调研过什么？
4. Agent 的核心组成与运行机制怎样解释？
5. Planning 主要由 Agent Framework 还是模型承担，常见实现方式有哪些？
6. Short-term / Long-term Memory 的边界是什么？
7. Function Call 的内容是否应该写入短期记忆；如果不写会产生什么问题？
8. MCP / 自写 Tool 分别怎样实现，大模型 Tool 机制带来什么价值？
9. RAG Retrieval 实际调过哪些召回参数，如何判断调优有效？
10. Python 基础与 Coding：合并两个有序数组。

去重：当前二面与作者更早的“暑期一面凉经”属于不同时间段、不同招聘流程；URL、题序和本轮项目问法未在正式来源中命中，因此按独立招聘流程计数。

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

## S067 OPPO｜AI 全栈开发｜一面｜面试 / 发布 2026-08-13｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/cf5a82411c1e473385d8fcae6c250a6e

真人 / 第一人称证据：作者明确写这是本人第一次正式面试，记录自己 HTTP 状态码卡壳、面试官会换成候选人更熟悉的问题、整体氛围较融洽；反问还直接确认该岗位前端、后端和 Agent 的能力比例，Role Scope 清晰。

高价值问题：

1. 从用户输入 Prompt 到前端输出，AI Full-stack 链路中做了哪些处理？
2. 为什么按段落切 Chunk，实际 Retrieval 效果怎样？
3. 怎样判断 Evidence 不足并拒答，而不是让模型硬生成？
4. 为什么一个项目需要 Multi-Agent，而不是一个更大的单 Agent？
5. Short-term / Long-term Memory 怎样理解？
6. 常见 HTTP Status Code 及工程语义是什么？
7. 实际遇到 Hallucination 时怎样处理？
8. 全栈中自己最擅长哪一侧，如何用真实项目证明？
9. 页面卡顿如何定位性能瓶颈并优化？
10. 岗位如何平衡 Frontend / Backend / Agent 能力？

去重：URL、候选人“处女面”时间线及项目追问未在现有 OPPO 样本中出现；与 `S106` 为不同候选人、不同流程。

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

## S070 阿里云｜后端 Agent 开发｜实习一面｜发布 2026-05-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/10dc395d6a704e1ea22a8fbc0049c7da

真人 / 第一人称证据：作者以本人后端 Agent 实习一面发布并写“给我面没招了”；整场几乎都是系统 / 数据库 / Redis 基础，评论区甚至有人问“这问了 Agent 吗”，正是目标 Agent Backend 真实基础权重证据。

高价值问题：

1. Connect / Read / Write 等常见 Timeout 分别解决什么问题？
2. select / poll / epoll 的核心差异是什么？
3. Red-Black Tree 的特点是什么，OS 哪些机制会用到它？
4. CPU Load 与 CPU Usage 有什么区别；低利用率高 Load 如何排查？
5. `df` 显示磁盘满但找不到大文件可能是什么原因？
6. OS Memory Reclaim 怎么工作，阈值不合理会有什么后果？
7. MySQL Back-to-table 如何发生、如何避免；连接数打满怎样治理？
8. SQL Injection 如何避免；自增 ID 达到上限会怎样？
9. Redis + Lua 怎样保证秒杀扣减原子性，Logical Expire 与 Physical Expire 怎么选？
10. Redis Penetration、Redisson Lock、Sliding-window Rate Limit 怎样设计？

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
