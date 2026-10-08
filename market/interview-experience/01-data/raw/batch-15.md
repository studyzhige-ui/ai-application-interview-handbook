# Batch 15 一手面试流程

采集日期：2026-09-10

## S217 某小厂｜AI Agent / 大模型应用开发｜HR + 技术一面｜面试 / 发布 2026-09-04｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/10b2fcaf73d2401f8636bd0459e1cd08

真人 / 第一人称证据：作者说明先与 HR 沟通再进入技术面，并记录自己从传统 Backend 转 AI Application / Agent 的求职过程；作者主页是持续的个人求职时间线，不是批量面经账号。面试从本人 Agent 项目一路追到 TB 级金融 PDF RAG System Design 和 Transformer 基础。

高价值问题：

1. 为什么从传统 Backend 转向 AI Application / Agent？
2. 小米客诉分析 Agent 使用什么模型，多模型选型依据是什么？
3. 项目最大的技术挑战是什么，如何迭代解决？
4. RAG 知识库真实数据量级是多少？
5. System Design：面对 600GB–1TB 金融 PDF 数据，从零设计垂直 RAG。
6. 电子 PDF 与扫描 PDF 如何统一解析，并保持跨页语义连续？
7. Chunking 与 Hybrid Retrieval 怎样设计，Vector / Keyword 权重如何确定？
8. TB 级语料全量 Embedding 的计算与存储成本如何优化，增量更新怎么做？
9. Transformer、Self-Attention、Multi-head Attention 与 Activation Function 的应用工程理解要到什么深度？
10. Cosine Similarity 与 BM25 在混合检索中分别解决什么问题？

去重：已直接回读历史 Batch 并比对 URL、公司流程与独特的 TB 级金融 PDF RAG 场景；未发现已入库同场或高相似复制链。

---

## S218 美团｜Agent 开发｜日常实习一面｜发布 2026-08-25，75min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/58159306df52463ab75d72daa80d66df

真人 / 第一人称证据：作者 `QHN沙壁` 为持续记录本人求职流程的真实候选人。本场围绕智能运维 Agent 连续深挖 75 分钟；现场 Coding 一题快速完成、另一题只讲出思路未写完，评论区继续讨论项目来源和岗位技术侧重点，现场痕迹明确。

高价值问题：

1. 为什么做智能运维 Agent，完整系统如何运转，中间件为什么这样选？
2. 大模型 Context 已很大时，为什么还需要 RAG；直接把原始文档 / 代码库交给 Agent 用文件搜索或 `grep` 有何优缺点？
3. 即使暂时忽略 Token Cost，RAG 与 Tool-based Repository Search 的核心架构差异是什么？
4. 文档怎样 Chunk / Index / Store / Retrieve / Rank，Markdown 没有清晰标题时怎样切？
5. Keyword + Vector Hybrid Retrieval 如何组合，短 Query 与长 Chunk 的匹配问题怎样处理？
6. Hallucination / Retrieval Error 怎样建立 Evaluation 和 Regression？
7. Plan-and-Execute 与 ReAct、Single-Agent 与 Multi-Agent 怎样取舍？
8. Agent 与 Harness 的边界是什么？
9. Context Trimming、Prompt Cache 与 Milvus 等组件在真实系统中怎样使用？
10. 3 万 Goroutine 与 3 万 Thread 的资源与调度差异是什么？
11. Vibe Coding / Spec Coding 怎样进入真实研发流程并保证 AI 生成代码正确？
12. Coding：有序链表合并与最长有效括号；候选人保留了现场完成 / 未完成状态。

去重：历史库已有 8/23 美团 Agent 等场次，但作者、日期、项目与题序均不同；当前来源是独立候选人招聘流程，不因同公司同岗位误合并。

---

## S219 元石科技｜后端 / Agent｜一面｜发布 2026-08-25｜HUMAN-A

来源：https://www.nowcoder.com/discuss/921742843704549376

真人 / 第一人称证据：作者明确写整场几乎都在“拷打实习项目”，并承认自己对项目理解仍不够、被问懵；问题从简历里的 Agent 长链路编排一路追到 Context 每一层具体如何拼接、Memory 回填位置、Red-team Agent、Fingerprint 聚类和自动修复，具有明显的项目验真连续追问。

高价值问题：

1. Agent 长链路任务编排与 Context Governance 实际做了什么？
2. 多级 Context Compression 有哪些策略，分别在什么时机触发？
3. 一次 Model Request 中 System Prompt、Memory、Chat History、Tool Result 怎样排列和注入？
4. Tool Result 为什么这样写回 Context，换一种位置会有什么影响？
5. Long-term Memory 如何存储、Retrieval，并重新拼到 Context 的哪个位置？
6. Red-team Agent 的目标系统和攻击 / 测试边界是什么？
7. Reasoner、Worker、Intent、Fact 怎样形成自由探索任务闭环？
8. Stable Fingerprint 如何生成、聚类并驱动重复问题的自动修复？
9. 长报告 / 大量问题交给模型分类时怎样控制 Context 长度与 Token Cost？
10. 自动生成修复方案是一次 LLM Call 还是独立 Agent，第一轮 Reasoner 输入什么？
11. Agent 如何访问需要修改的 Skill、角色描述和知识库？
12. Coding：Longest Common Prefix。

去重：直接回读历史 Batch 后，未发现相同 URL、相同元石招聘流程或“Red-team / Fingerprint → Context 逐层拼装”同序来源；与其它公司使用相似项目的场次属于不同招聘流程。

---

## S220 匿名游戏公司（1000–9999 人）｜AI Agent 应用开发｜一面 + 后续二面｜面试 2026-03-03｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/416c3118a9c84fe0a43dc00f9eb9bec2

真人 / 第一人称证据：作者主页只有少量普通个人动态。本帖明确说明公司规模和游戏业务，一面围绕本人“口腔医疗多模态 Multi-Agent”项目，现场给出 AI 漫剧 Agent System Design 并持续追人物一致性与 Evaluation；作者更新当天下午一面后立刻约二面，而二面面试官迟到、玩手机、十几分钟草草结束，真实现场痕迹很强。

高价值问题：

1. 多模态 Multi-Agent 医疗项目的完整链路是什么？
2. Coze 新旧两种编排形态有什么差异，节点如何设计？
3. 实际写过哪些 MCP Tool？
4. Context Management 与 Memory 怎样实现？
5. ReAct 及不同执行模式的差异是什么？
6. System Design：只给题材，让 AI 自动创作、执行并自反馈迭代一部漫剧，完整 Agent 应怎样设计？
7. 这套系统最关键的三个风险是什么，怎样治理？
8. 如何保证人物跨片段一致，生成片段如何 Evaluation？
9. 如果先发 MVP，哪些 Node / Capability 必须保留？
10. Cursor / Codex 连续错误修改同一段代码时，怎样跳出错误循环并恢复？

去重：匿名公司本身不影响 HUMAN-A。历史 Batch 未发现相同 URL、相同多模态医疗项目 + AI 漫剧 System Design 题序或同作者同流程来源。

---

## S221 某中型 AI 设备研发公司｜AI Agent 开发｜一面 + 二面 + HR/Boss，已 Offer｜发布 2026-06-17｜HUMAN-A

来源：https://ai.codefather.cn/post/2067118684236795905

真人 / 第一人称证据：来自公开个人型社区正文。作者明确说明自己 35+、寻找下一阶段工作，本场公司为自研 AI 产品甲方、岗位聚焦内部 AI 提效；一面两位面试官线上约 50 分钟，二面同两位面试官现场约 55 分钟，之后还有 HR / Boss 面并最终拿到 Offer。正文包含候选人“现场没想过、向面试官请教后再拆方案”的反应和面后总结。

高价值问题：

1. 最近项目整体 Architecture 是什么，本人做了哪些 AI Efficiency 工作？
2. 团队规模、技术栈、Cloud Deployment、Monitoring 与 Security 怎样落地？
3. RAG 与 LangGraph Agent 在真实项目中怎样使用？
4. AI 如何进入 System Operations / 运维场景？
5. Vibe Coding 实际使用哪些工具，如何避免只追求速度？
6. 系统真实数据规模、Concurrency 场景与简历指标如何证明？
7. 二面如何为 Vector DB 数据导入 / 更新设计完整 Agent / Workflow？
8. 如果把公司现有内部系统整体 AI 化，怎样拆功能、Tool、Skill 与 State？
9. Model Selection 用哪些效果、Latency、Cost 指标？
10. Context Engineering / Compression 怎样做，优化前后如何比较？
11. Prompt Optimization 如何通过真实 Case 和 Regression 证明有效？
12. 陌生业务场景下，如何先澄清需求再完成现场 System Design？

去重：直接对照历史正式 Batch 后未发现同 URL / 同招聘流程；正文具有连续一二面与 Offer 时间线，未发现可确认的跨平台同场已入库来源。

---

## S222 美团 Keeta｜Agent 开发（智能客服）｜一面｜发布 2026-04-28｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/abef26e941054c9db854cba7c81049cd

真人 / 第一人称证据：作者主页有本人 Claude Code、Langfuse 等技术学习 / 开发记录，并非面经内容账号。本场从自己的 Agent 项目进入智能客服开放题，面试官现场补充“非订单类问题更适合知识库、订单类复杂流程当前用 Skill”，随后继续追 SFT / DPO 与 Claude Code；算法题快慢指针思路正确但未完整写出代码。

高价值问题：

1. Main Agent Loop、Mem0 Memory、RAG 与 Hallucination Control 怎样实现？
2. Agentic RAG / 主动式 Retrieval 与当前固定 RAG 的核心差异是什么？
3. 外卖客服不同用户场景中，哪些问题适合 RAG，哪些更适合 Skill / Workflow？
4. 订单相关问题为什么不应只靠 Knowledge Base？
5. 医疗模型 SFT 的数据如何构造？
6. DPO 的 chosen / reject 数据怎样生成，Evaluation 有什么局限？
7. Fine-tuning 项目与 Agent 项目是什么关系，为什么都要做？
8. Claude Code 在 Agent 开发里怎样使用，真实遇到过什么问题？
9. Claude Code 的 Memory / Context 行为怎样理解？
10. Coding：删除链表倒数第 K 个节点；候选人给出 Fast/Slow Pointer 思路但未完整实现。

去重：直接回读历史 Batch 后未发现相同 URL、相同作者或 Keeta 智能客服这一招聘流程；与其它美团 Agent 来源题序 / 项目语义不同。

---

## S223 阿里国际｜AI 应用开发｜暑期技术面约 1h｜发布 2026-04-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/05618d54fc8f487bb9413ad2adfc1591

真人 / 第一人称证据：作者 `星轨偏差` 明确写“面试很难，感觉自己说不明白业务逻辑”，主页只有十余条个人求职 / 生活动态，可连续核验其求职过程。整场从实习 AI 部分进入 Rerank / 大规模 Retrieval、Agent Service、Memory，再深入 Streaming、Kafka、Distributed Lock 与 OOM。

高价值问题：

1. 实习经历中真正与 AI 相关的部分是什么？
2. Vector Recall 后为什么还要 Rerank，Coarse / Fine Rank 的成本和精度差异是什么？
3. 文档量大时怎样更快召回 / 检索？
4. Agent 与 RAG 怎样封装成对外 Service？
5. 常见 Agent Paradigm、多 Agent 设计时最核心关注点是什么？
6. Agent Memory 怎样理解，是否真正实践过？
7. LangChain / LangGraph / LangChain4j 各自使用了哪些能力？
8. Streaming Output 可以怎样实现？
9. Kafka 为什么能支撑高吞吐？
10. 除 Redis 外，还有哪些 Distributed Lock 实现路径？
11. 真实系统遇到 OOM 时怎样定位？

去重：同作者还发布过其它公司的本人流程，但不同公司可以独立计数；历史阿里国际来源作者、时间线与题序不同，本 URL 未正式入库。

---

## S224 美团｜AI 全栈开发｜实习一面｜发布 2026-04-20｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/3a899c176bef400883ae833ae1094086

真人 / 第一人称证据：同为 `星轨偏差` 的个人求职流程，但本场属于美团独立招聘。本帖以本人一面“攒人品”发布，将 RAG / Multi-step Agent Failure 与真实用户、Latency 指标、安全过滤、Vibe Coding 连在一起，并继续追 HTTP、V8、MySQL、IVF/HNSW 与 Java 基础，符合目标 AI Full-stack 的完整工程范围。

高价值问题：

1. 项目是个人还是实习项目，是否真实上线？最大难点是什么？
2. 怎样识别 Ambiguous Query 并做精确 Retrieval？
3. Keyword Drift 时如何平衡 Vector + Keyword，RRF 参数 `K` 怎样调？
4. Multi-step Agent 前序产生幻觉后，如何避免 Error Propagation？
5. 如果 Evaluator Agent 本身也 Hallucinate，怎样保证评测可靠？
6. 是否有真实用户；简历写 Latency 降低 40%，是 Online Data 还是个人测试？
7. ToC 产品如何做 Sensitive / Unsafe Content Filtering？
8. Vibe Coding 的完整 Workflow 是什么；Long Task 中 Context 丢失、忘需求、乱改代码怎样治理？
9. HTTP/1.1、HTTP/2、HTTP/3 的核心差异，为什么内部服务仍常用 HTTP/2？
10. V8 GC、MySQL B+Tree、IVF vs HNSW 分别怎样解释？
11. AI Coding 现场写函数，并把这套流程抽象成一个 Skill。

去重：同作者其它公司流程独立；历史美团 AI Full-stack 来源为不同作者 / 日期 / 项目题序。本 URL 及“RRF → 幻觉链 → 40% 指标 → AI Coding Skill”连续题序未正式入库。

---

