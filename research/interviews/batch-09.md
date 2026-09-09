# Batch 09 — AI Application / Agent 高质量面经（全链路继续扩展）

采集日期：2026-09-09

> 本批继续同时执行两道门槛：
>
> 1. **Source Quality Gate**：优先第一人称、技术问题具体、可核验的真实面试；过滤题库拼接、SEO 博客和水内容。
> 2. **Role Scope Gate**：只收 AI 应用开发、Agent 开发、AI 全栈、大模型应用、AI 后端、Agent Runtime 等目标方向。传统数据分析/BI/纯算法训练/普通后端仅顺带问 AI 的场次不进入正式样本。
>
> 通过岗位准入后，保留该 AI 岗位真实问到的整条能力链：Python / FastAPI / MySQL / Redis / Backend / Vector DB / RAG / Agent / System Design，而不是只摘“看起来像 AI”的问题。

---

## S101 字节跳动｜AI 应用开发｜一面｜2026-07-14｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/34e45df5ee2043dc8fdc48cd1384f1b4

高价值问题：

1. 项目中的幻觉问题如何从 Prompt、Tool、RAG、模型侧分层治理？
2. System Prompt / 约束提示具体如何设计，如何处理“知识不足时不应该胡答”？
3. Agent 的短期记忆和长期记忆分别怎么实现？
4. 如果从零设计一个 Agent，需要哪些核心模块？
5. 外部 API 超时、报错时如何分类处理、重试或降级？
6. 是否可以让模型自己修复 Tool/API 调用失败？什么应该交给模型，什么必须由 Runtime 控制？
7. Token 消耗突然过快时，从 Context、Tool Result、循环步数和重复调用等角度如何排查？

价值：问题从 Agent 结构一路追到 **Memory、Failure Handling、Token Debugging**，是应用层一面常见的“从项目追工程边界”样本。

---

## S102 哔哩哔哩 B站｜AI 应用研发实习｜二面｜2026-06-15 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/a88fde0d7efc4779aa67d9841871aa90

高价值问题：

1. Temperature 是什么，实际工程中什么时候会调整？
2. Function Call、MCP、Skill 的职责边界是什么？
3. 使用过哪些 Skill，如何理解 Skill 的可复用能力封装？
4. 系统设计：多 Agent 自动 PR 系统如何设计？
5. 系统设计：单 Agent 类 GPT Web 应用如何设计？
6. 上述系统如何设计 Sandbox、Agent 通信、Context、Tool 触发和安全边界？
7. AI 出现后，软件工程经验为什么仍然重要？

价值：二面直接进入 **Agent System Design**，并明确把 Sandbox / Context / Tool / Security 作为系统级能力，而不是框架 API。

---

## S103 指数引力｜AI Agent 开发｜一面｜2026-02-11｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/e29b36c7ab554d3aa60fc4ec68150346

高价值问题：

1. Redis 用于增量更新/监听时，BigKey、BigValue 会带来什么问题？
2. Redis Pub/Sub 在多 Key / 多监听场景下如何组织？
3. MySQL 治理和性能优化做过哪些具体工作？
4. ReAct Agent 与 Multi-Agent 在项目里如何落地？
5. MCP、Skill、Function Call 的关系是什么？
6. Function Call 在 RAG 知识库业务里如何嵌入完整链路？
7. 如果实现类似 Claude Code / Cursor 的 Coding Agent，需要哪些核心能力？
8. Multi-Agent 中 Plan 如何设计？
9. 长任务 Context 接近阈值后如何压缩，不同 Agent 场景如何选择 Context 管理方式？

价值：一场面试同时覆盖 **Redis/MySQL 基础 + Coding Agent + MCP/Skill + Context Compaction**，非常符合统一知识路线。

---

## S104 新大陆集团｜大模型应用开发｜线下一面｜面试 2026-06-15，发布 2026-07-04｜原始/第一人称｜B

来源：https://www.nowcoder.com/feed/main/detail/1a85477771e0493086facc1e97cc3a48

高价值问题：

1. 向量库里不存在用户所需文档时，RAG 应该怎么处理？
2. 用户自己也无法补充信息时，系统应该如何拒答、升级或请求人工知识补充？
3. 从零建设企业内部知识库 RAG，面对上百份真实文档，正式建库前应该如何做语料调研？
4. PDF、表格、编码、格式转换、扫描件等数据质量问题应该在什么阶段暴露和治理？

价值：题量不大，但它问到了很多 Demo 教程忽略的 **Knowledge Gap + Corpus Discovery / Data Audit**。因公开问题数量较少，标记为 B，不与高密度 A 级样本等权。

---

## S105 懂车帝｜AI Agent｜一面｜2026-08-28 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/69e209d77a4647b7896ef3fd835239b6

高价值问题：

1. Multi-Agent 为什么这样拆，Agent 间如何任务分工和通信？
2. Agent 的结束条件、异常退出、State Management 怎么设计？
3. Agent Evaluation 如何建立，并如何驱动后续优化？
4. Tool、Skill、Workflow、Agent 的职责分别是什么？什么场景必须依赖 Workflow？
5. Context Engineering 主要解决哪些问题？
6. 企业级成熟 Agent 系统需要具备哪些核心能力？
7. RAG 知识库如何提升 Recall 和 Context Matching？
8. Vibe Coding / Coding Agent 的安全开发流程如何设计？
9. 人工 Code Review 在 AI 生成代码时代应该重点检查什么？
10. `AGENTS.md` 一类项目规则文件应该包含哪些规范、边界和执行约束？

价值：除了 Agent/RAG 主干，还出现了 **Project-level Rule File / Coding Governance**，与 Codex / Claude Code 后续源码研究直接相关。

---

## S106 AI 初创公司｜Agent 开发实习｜2026-04-17｜原始/第一人称｜B

来源：https://www.nowcoder.com/feed/main/detail/632b151ada3a404894f1dc1c30dcbd19

高价值问题：

1. Python dict 与 list 的基本差异和使用场景？
2. RAG 为什么选 Chroma，向量库选型依据是什么？
3. RAG 链路里最容易出问题的环节是什么？
4. Multi-Agent 的短期/长期 Memory 核心目标分别是什么？
5. 长期 Memory 持续增长时如何控制存储规模和过期策略？
6. Short-term Memory 压缩后，未来如果又需要完整历史，原始 Transcript 应如何保存和重新取回？
7. Memory 应该保存在平台数据库、云端还是本地？如何根据隐私、可移植性和产品形态选择？
8. 一个现有 RAG 项目 Chunk 设计明显不合理时，如何重新评估和迁移？

价值：公司匿名，故不参与公司频率统计；但问题对 **Memory Storage Boundary / Transcript vs Visible Context** 很有价值。

---

## S107 某游戏公司（1000–9999 人）｜AI Agent 应用开发｜一面｜2026-03-03｜原始/第一人称｜B

来源：https://www.nowcoder.com/feed/main/detail/416c3118a9c84fe0a43dc00f9eb9bec2

高价值问题：

1. Coze / Agent 编排中的节点怎么设计？
2. MCP Tool 实际写过哪些，输入输出怎么设计？
3. Context 与 Memory 如何管理？
4. ReAct 不同模式如何选择？
5. 场景设计：从一个题材自动生成完整 AI 漫剧，并让系统自评、迭代，如何设计完整 Workflow/Agent Pipeline？
6. 在这种多阶段生成系统里，人物/剧情一致性和阶段评测怎么保证？
7. 如果先做 MVP，哪些节点必须保留，哪些能力可以延后？
8. Coding Agent 反复修改同一处仍然报错时，如何停止无效循环并切换 Debug 策略？

价值：公司未公开，降权为 B；但它提供了很好的 **Generative Workflow / Iterative Evaluation / MVP Boundary** 场景题。

---

## S108 字节跳动｜暑期后端 Agent 开发｜一面｜2026-04-08｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/fa55d9f475624bfb95d943a5c00a599f

高价值问题：

1. 单 Agent + 更多 Tool 与 Multi-Agent 两条路线怎么选？
2. 如果模型可以自己决定是否调用 Tool，为什么还需要 Orchestration / Workflow？
3. Tool 本质是 RPC 接口时，为什么不能全部统一封装后交给一个 Agent？
4. RAG 如何搭建，Vector Similarity / Embedding / TopK 分别在什么位置？
5. Retrieval Evaluation 应该看哪些指标？
6. Multi-Agent 局部失败、链路失败如何处理？
7. Multi-Agent Context Handoff 为什么更适合 JSON / Slot 等结构化传递，而不是自由文本？
8. 在线系统如何权衡 Latency 与 Agent 效果？

价值：非常适合校准 **Single Agent vs Tool Orchestration vs Multi-Agent**，也是结构化 State Handoff 的高质量样本。

---

## S109 美团｜AI 后端开发｜一面｜2026-04-07｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/398d270fc3eb407ca2341007cd13a1b2

高价值问题：

1. Agent Loop 的完整流程，以及用户最直观感知到的是什么？
2. RAG 如何选模型，如何评估 Accuracy / Recall，知识库如何持续更新？
3. Redis 分布式锁什么时候应该使用？
4. Cache 与 Database 的更新机制、风险和一致性怎么解释？
5. 账户互转如何避免死锁，引入固定加锁顺序后还有哪些风险？
6. TCP/UDP、可靠传输等网络基础为什么仍会在 AI 后端岗出现？
7. 项目表结构如何设计，海量用户数据如何分表查询？
8. SOLID / DDD / 设计模式如何用于 AI 后端工程？
9. 海量数据 Top-K 如何实现？

价值：再次证明目标 AI 岗的基础能力不是附录：**Redis / DB / Network / System Design 与 Agent/RAG 同场出现**。

---

## S110 阿里控股｜AI 全栈开发｜二面 / Leader 面｜2026-09-08 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/a11a3a9e0d824969b44db5bb2149ef9f

高价值问题：

1. Dynamic Workflow 平台如何实现？用户提出需求后 Agent 到底能自动完成到什么程度？
2. Coding Agent 第一次修改失败时流程是否中断，如何回退和继续？
3. 模型声称“已经执行”但实际上没有发生外部动作时，如何避免把模型自述当成执行事实？
4. RAG / Knowledge Layer 如何做事实锚定？
5. 为什么使用 Multi-Agent，而不是全部做成 CLI / Script？
6. Workflow 应该偏确定性编排还是高自由度自治？
7. 非预设 Skill 如何从对话/Bad Case 中沉淀？如何判断“走弯路”并评测 Skill？
8. 数千业务是否能共用统一 Agent 流程？能力正交性、冗余和治理怎么处理？
9. Model RPC 延迟很高时，同步/异步链路如何选择？
10. 如何用真实 Token、需求数、运行时长来评估系统成本与负载？

价值：很新鲜的社招/Leader 面，重点是 **Dynamic Workflow、Execution Truth、Skill Evolution、Scale Governance**。

---

## S111 Moka｜Agent 开发｜一面（社招）｜2026-08-28｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/520a8fd058b64965a036b5c92376fc90

高价值问题：

1. Agent 系统的时延问题如何重构？
2. 开源 Agent 轮子很多时，技术选型应该看哪些维度？
3. MCP + Skill 为什么这样组合，为什么不直接全部用 Script / CLI？
4. Knowledge Base 为什么要单独分层？
5. Pre-production 环境如何做自动化验证？
6. 真实流量执行后，如何判断 Agent 结果好不好，不只看性能，还要看效果指标？
7. A/B Test 如何用于 AI 系统优化？
8. AI Coding 时代，传统软件工程经验还有哪些不可替代的价值？
9. AI-native 团队真正的工程特征是什么，阻碍 AI-first 的因素有哪些？

价值：对 **Release Validation / Online Evaluation / A-B Testing** 很有价值，属于 Production AI System 的重要补充。

---

## S112 快手｜Agent 开发（日常实习）｜一面｜2026-08-13｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/ce1b038c57c44cc08464561a8cfa0434

高价值问题：

1. Agent 的短期/长期 Memory 如何分工？
2. Context 不够时，截断、摘要、检索召回怎么选？
3. ReAct 与 Workflow 如何选？
4. Tool 调用失败如何处理？检索证据冲突时信任谁？
5. Go Channel / Mutex / GMP 等并发基础为什么会被追问？
6. Redis 为什么快，数据结构怎么选？
7. 类搜索框实时模糊搜索如何设计？
8. 扫码登录完整流程与鉴权如何设计？
9. Nacos / Consul 的服务注册、发现、心跳如何工作？
10. 工程手撕：100 个任务调用外部接口，最大并发限制为 3，如何实现有界并发？

价值：很典型的 **Agent 中台 = Agent + Backend Runtime**。尤其“有界并发调用 Tool/API”与生产 Agent 高度相关。

---

## S113 京东｜大模型应用开发实习｜一面｜2026-03-19 发布｜原始/第一人称｜A

来源：https://www.nowcoder.com/feed/main/detail/5ecaca5990d74c94840f01d83835eb69

高价值问题：

1. RAG 与 Multi-Agent 的定位和后续发展怎么看？
2. Elasticsearch 与 Vector DB 在检索系统中分别承担什么职责？
3. 用户输入不标准时如何预处理、Query Rewrite 或做检索兜底？
4. Hybrid Retrieval 的权重如何配置和验证？
5. Vector Retrieval 如何保障 Recall / Precision？
6. 不同向量数据库的选型差异是什么？
7. IVF 与 HNSW 的核心差异是什么？
8. RAG 系统 Accuracy 如何评估？

价值：Vector DB / Retrieval 密度很高，适合作为后续 Vector DB 模块验收样本。

---

## S114 某小厂（公司匿名）｜AI Agent / 大模型应用开发｜技术一面｜2026-09-04｜原始/第一人称｜B

来源：https://www.nowcoder.com/feed/main/detail/10b2fcaf73d2401f8636bd0459e1cd08

高价值问题：

1. 面向 600GB–1TB PDF 语料，如何从 0 设计垂直 RAG？
2. 电子 PDF 与扫描 PDF 如何统一解析，如何保证 OCR、跨页语义和结构信息质量？
3. TB 级语料初始化 Embedding 和后续增量更新的算力/存储成本如何优化？
4. Transformer 的核心结构和推理链路是什么？
5. Self-Attention 与 Multi-Head Attention 分别解决什么问题？
6. 常见相似度计算为什么会选择 Cosine？
7. BM25 在 Hybrid Retrieval 中承担什么角色？

价值：公司匿名所以不参与公司频率统计；但它明确显示 **AI 应用岗开始重新追 LLM Foundation（Transformer/Attention）**，同时仍结合大规模 RAG 场景，而不是纯算法岗理论题。

---

# Batch 09 观察

这一批继续强化了三个趋势：

1. **整条路线都在被问**：Python/并发、Redis/MySQL、网络、Vector DB、RAG、Agent、Coding Agent、System Design 并不是彼此独立的面试模块。
2. **Agent 问题正在从“组件定义”进入“控制与治理”**：项目规则文件、Execution Truth、Workflow 自由度、Skill 演进、Release Validation、A/B Test、Bounded Concurrency 都是成熟系统才会遇到的问题。
3. **LLM Foundation 不能完全缺席**：至少 Transformer、Attention、Temperature/Top-p 这类工程应用需要理解；但仍应保持应用开发深度，而不是滑向训练算法岗的 CUDA / RLHF / 大规模训练 Infra。

本批正式新增 `S101–S114` 共 **14 个来源**。其中匿名公司样本均降权为 B，不进入公司级频率统计。