# Batch 16 一手面试流程

采集日期：2026-09-10

## S225 字节跳动｜AI Agent 研发｜秋招一面｜发布 2026-08-31，凉经｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/2ba7e96d48634777990b28c2cb322f40

真人 / 第一人称证据：作者 `27秋招大李GOAT` 以本人一面凉经发布，明确写到部门正做测评，因此围绕本人实习重点追 Benchmark；同时坦言几个后端八股没答上、与面试官一起笑了，Agent Benchmark 只知道 SWE、部分指标也不清楚。问题顺序从实习 / Benchmark → MySQL / Redis / OS / Network → Agent Benchmark → 现场 Coding，自然且现场痕迹强。

高价值问题：

1. 实习中的 Benchmark 是怎样构建的，为什么选择这些指标？
2. MySQL Index 的基本机制和常见使用边界是什么？
3. Redis Cache Expiration / Update Strategy 怎样设计？
4. Distributed Lock 的核心正确性问题是什么？
5. OS 中 Stack 与 Heap 的差异是什么？
6. TCP 与 UDP 的核心差异和应用边界是什么？
7. 了解哪些 Agent Benchmark，分别评价什么能力？
8. 如果从零设计一个 Defect-fix / Bug-fix Benchmark，Task、Dataset、Environment、Metric 和 Verification 怎样拆？
9. Coding：Longest Palindromic Substring。

去重：已直接回读 `S001–S224`；URL 未入库，作者 / 日期 / 字节流程独立，且“业务测评实习 → Agent Benchmark → 从零设计缺陷修复 Benchmark”的连续题序未在历史来源出现。

---

## S226 阿里云｜AI 全栈开发工程师｜秋招一面｜面试 2026-08-12，发布 08-13｜HUMAN-A

来源：https://api-cdn.nowcoder.com/feed/main/detail/e67dfce683ea4a82bbf6e48456a22b92

真人 / 第一人称证据：作者明确给出阿里云秋招、AI 全栈岗位和 8 月 12 日一面；先在阿里平台做不能运行代码的算法题，随后因面试官问“是否熟悉 Python”进入连续 Python 深挖，最后回到 Agent 生成代码质量。评论区也继续讨论 Python 深度和 Agent Code Quality 的回答边界。

高价值问题：

1. Coding：LeetCode 2958 / 最多 K 个重复元素的最长子数组，不能运行代码时如何保证边界正确？
2. Python Function Parameters 有哪些形式，调用和绑定规则怎样理解？
3. `*args` / `**kwargs` 的语义和典型用途是什么？
4. Duck Typing 如何理解，它给接口设计带来什么收益和风险？
5. Iterator 与 Generator 有什么区别，底层执行 / 状态保存机制怎样理解？
6. Python Slicing 的语义和实现成本是什么？
7. 如何验证 Agent Generated Code 的质量？
8. 如何系统提升 Agent Generated Code 的正确性、可维护性和可测试性？
9. Agent 的基本工作原理和执行循环是什么？

去重：已直接对照所有历史 Batch；阿里云已有多个 Agent / AI Backend 样本，但没有该作者、8/12 AI Full-stack 流程或“Python 迭代器 / 生成器 / Duck Typing → Agent Code Quality”的同场题序。

---

## S227 阿里淘天｜AI / Agent 应用方向｜秋招一面｜面试 / 发布 2026-08-18，次日已挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/8e5fb9efdc154b9e913a2c8bde2a2a0b

真人 / 第一人称证据：作者 `Huang7_7` 明确写 `8.18 淘天 AI 秋招一面`，评论区次日由楼主更新“已经 g 了”。问题围绕业务项目、Workflow / Agent、A2A、Skill、Context 与 Memory 连续展开，实际职责明显属于 AI Application / Agent Role Scope。

高价值问题：

1. 项目解决什么真实业务问题，本人负责哪一部分？
2. 业务中最困难的问题是什么，个人具体怎样解决？
3. Workflow 与 Agent 的工程边界是什么，各自适合什么任务？
4. A2A / Multi-Agent 适合什么类型的任务，什么时候反而不应拆？
5. 怎样理解 Skill，它与 Agent / Workflow 的关系是什么？
6. 大型工程导致 Context Explosion 时怎样治理？
7. LLM API 本身无状态，为什么 AI Client 能表现出“有记忆”，Session / History / Persistent Memory 怎样实现？
8. LangChain 与 LangGraph 分别解决什么问题，工程选型边界是什么？

去重：URL、作者、8/18 淘天招聘流程均未入库；独特的“无状态 API → 有状态 AI Client Memory”追问与本场业务 Agent 题序未在 `S001–S224` 发现同场来源。

---

## S228 快手｜AI 全栈开发（音视频）｜一面 + 二面（同一候选人同流程合并）｜发布 2026-08-31 / 09-07｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/a30242712e8d456c839ff4223470f491

二面来源：https://www.nowcoder.com/discuss/926528416512315392

真人 / 第一人称证据：两个页面均由同一作者 `牛客523469060号` 发布，学校 / 技术方向一致；一面围绕 Skill / Workflow、Agent Stop、合规强保证和离线评测，二面约 55 分钟继续沿同一故障诊断 Skill 深挖 Agent 路由、Evaluation、敏感信息、SubAgent、鉴权与音视频基础，明显是同一招聘流程，因此合并为一个 `Sxxx`。

高价值问题：

1. 为什么把原 Workflow 改成 Skill，二者优缺点分别是什么？
2. 怎样定义一个 Good Skill，它的实现架构怎样支撑项目目标？
3. Agent 怎样判断任务已经完成并可靠停止？
4. 模型可能忽略 Skill 文档时，高合规场景如何提供确定性的强约束？
5. Skill 怎样 Self-test，如何降低大规模 Offline Evaluation 成本？
6. 如何在线下预估 Skill 优化收益以及上线后的 Human-handoff / 转人工率变化？
7. 二面继续追：业务 Agent 的 Intent Routing 用 Rule、Small Model 还是 Main Model，怎样选择？
8. 故障诊断链路如何分别评估 Routing、Tool、Document Retrieval 与 Final Diagnosis？
9. Evaluation Case 和 Expected Output 从哪里来，是否经过值班人员 / Domain Expert Review？
10. 怎样验证 Offline Case 与线上真实故障 / 排障路径具有一致性？
11. 为什么把故障诊断做成 Skill，而不是单独搭一个专用 Agent？
12. Agent 必须读取内部算法 / 代码才能诊断时，Prompt Injection 与 Sensitive-data Leakage 怎样从架构层治理？
13. SubAgent 读取敏感信息、主 Agent / Review Agent 过滤输出是否足够，权限与鉴权应放在哪一层？
14. 音视频方向中 VOD / Live / Transcoding 的基本链路怎样理解？
15. Coding：有序 `1..N` 序列缺一个元素，给出多种算法并比较复杂度。

去重：一面 / 二面同作者同公司同岗位连续，主动合并不重复计数；历史快手来源中未出现该候选人的“Skill 大规模评测 → 转人工率 → Domain Expert Case Review → Sensitive SubAgent / Auth”完整链路。

---

## S229 华为某 BG｜Agent 岗位｜技术面 + 主管面｜2026-06 中旬 / 07 上旬，07 中旬 Offer｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/63f974c8a2214503bdc0ad7505cdc15b

真人 / 第一人称证据：作者完整记录 4 月投递、两次综测、6 月中旬约 50 分钟技术面、两周后 7 月上旬主管面及 7 月中旬 Offer。最强真实性信号是候选人主动承认 Agent 项目代码阶段主要做外围服务、没有直接参与 Agent 核心实现，但熟悉架构；现场拓扑排序写得低效也被面试官直接指出。

高价值问题：

1. TCP 三次握手怎样进行，为什么不能只做两次？
2. C 语言临时变量通常存在哪类内存区域？
3. 基于 ReAct + 改造 RAG 的 Agent 项目整体架构是什么？
4. 候选人本人到底参与了哪些实现，怎样区分外围 Service 与 Agent Core 的真实贡献？
5. Coding：Topological Sort，怎样从正确性进一步优化复杂度和实现？
6. 主管面继续追：C Source 到 Executable 的 Compilation / Assembly / Linking 流程是什么？
7. Compilation Unit 到 Object File 的具体过程怎样理解？
8. Computer Use Agent 的业务背景、系统结构与执行链是什么？
9. RAG、Skill、MCP 分别解决什么问题，怎样在 Agent 中组合？
10. 面试官建议继续学习主流 Agent Framework / Coding Agent，应用工程师应该读到什么深度？

去重：直接回读 `S001–S224` 后未发现华为同流程正式样本；“CS Foundation → 主动承认 Agent Core 非本人实现 → Computer Use Agent → C 编译链”的作者 / 项目 / 题序均独立。

---

## S230 阿里淘天｜Agent 优化 / 业务 Agent 编排｜一面 + 二面（同流程合并）｜2026-04 上旬，04-09 发布 / 补二面状态｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/d81d1ddb6d8245e7b6a7aa71f175e72b

二面补充来源：https://www.nowcoder.com/feed/main/detail/78e68b3d67be4273b43cf9d9d3660d57

真人 / 第一人称证据：作者同为 `27秋招大李GOAT`，但这是与 `S225` 字节完全不同的公司招聘流程。作者写一面后泡了一周才通过，并在 4 月 9 日补充二面：同类场景题因为刚在一面讨论过、又能套 OpenClaw / Claude Code 的思路，答得过于流畅反而被面试官质疑是否用 AI 搜索；这种不完美互动与流程连续性非常强。

高价值问题：

1. Agent Memory 应如何设计？
2. Workflow、Agent、Skill 的职责边界和适用场景是什么？
3. Prompt 应从目标、约束、Context、Tool、Output 等哪些维度设计？
4. Vibe Coding 现场拿到问题时，为什么应该先 Clarify Requirement，而不是立刻开始写？
5. 一个业务 Agent System 中，每个 Agent 到底负责什么，输入 / 输出必须怎样讲清楚？
6. 业务 Agent 的设计编排优化与 Model Training / Algorithm Optimization 有什么本质差异？
7. 为什么业务理解可能比“会更多框架 API”更重要，怎样把业务目标映射为 Agent Capability？
8. 二面遇到相似场景题时，如何把 OpenClaw / Claude Code 等成熟产品思路迁移到新场景，而不是照搬答案？
9. AI Coding / 面试场景中，怎样证明回答来自真实理解而不是即时搜索？

去重：同作者的 `S225` 是 8 月字节 AI Agent 研发流程，本场是 4 月淘天 Agent 优化流程，允许独立计数；本场两条 URL 属于同一淘天流程，因此合并为一个来源。历史 Batch 未发现相同作者 / 公司 / 业务 Agent 编排流程的正式样本。

---

