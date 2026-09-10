# Batch 19 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S326` 继续编号。按本轮要求，搜索重点重新收回**热门公司**，优先覆盖百度、阿里系、字节、腾讯、美团、快手、小红书、拼多多、OPPO 等；但公司热度不构成质量加分，正式来源仍必须同时满足：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非重复 = HUMAN-A**。
>
> 分配编号前，先确认当前 `main` 仍为 Batch 18 基线 `S001–S325`；结合本会话上一批刚完成的 `batch-01.md` ～ `batch-17.md` 全历史直接回读结果，重新读取最新 `batch-18.md`，并对本批每个候选回查相关历史 Batch，执行 URL、公司 / 岗位 / 日期 / 轮次、作者、项目语义、5～10 个独特题序特征与招聘 Timeline 去重。GitHub Code Search 的 0 命中仍只作辅助。
>
> 本轮热门公司噪声非常明显：拼多多强候选最终确认作者属于“100+ 社招面经 / 订阅内容”生态，按非内容账号 Gate 撤出；快手 7 月候选向前追到 2 月同序一二面以及 3 / 4 月多个高度同序版本，原始归属不再可靠，因此整条复制链排除；美团、腾讯、字节多条热门结果则直接命中历史正式来源。宁可只保留 6 个独立样本，也不为公司覆盖率降低标准。

---

## S326 百度｜Agent 开发｜秋招一面｜发布 2026-09-06｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/72858aade19d443facc870fea8bb134f

真人 / 第一人称证据：作者 `无欲a` 以本人“百度 Agent 一面”发布，明确写这是自己的秋招第一面；记录面试官持续引导、后半段计算机基础发挥不好，以及 Coding 先提出堆方案后被提示继续往 Quickselect 优化。整场从本人 Agent 项目连续进入 Runtime、Streaming、Trace、Memory、RAG、MySQL / Network 与现场 Coding，面试流非常完整。

整场技术问题：

1. 代码问答 / 代码诊断 Agent 面对线上报错日志时，能否定位 Bug 与对应代码位置？
2. LLM Runtime 与 Tool Runtime 分别负责哪些职责，边界怎样划分？
3. 多模型路由依据什么信号，模型失败时怎样分类 Retry，参数错误是否应该重试？
4. Agent Streaming 怎样实现；SSE 与普通 HTTP、WebSocket 的通信语义有什么差异？
5. 多轮 Tool Call 的 Context 怎样维护，Tool Result 过大时如何处理？
6. Context 截断除了“丢信息”之外还会造成哪些真实执行问题，项目里遇到过什么 Case？
7. Tool Timeout、并发执行和 Idempotency 怎样设计？
8. Trace Hook 放在哪些 Runtime 层，一次用户请求怎样映射成完整 Trace？
9. Trace 数据怎样用于节点级故障定位和后续分析？
10. Memory 怎样设计，不同用户状态如何隔离？
11. Checkpoint 应保存哪些状态，为什么采用 Main Agent + SubAgent？
12. RAG 为什么需要存在，Offline / Online 完整链路是什么？
13. PDF 如何解析；为保持语义连续性怎样 Chunk，表格为什么可能转为 HTML？
14. Chunk 过大 / 过小分别有什么代价，参数如何通过实验确定？
15. Hybrid Retrieval 为什么组合 BM25 与 Vector Retrieval，两者分别补什么短板？
16. 如何通过实验验证纯向量与 Hybrid 的收益，而不是只凭经验选型？
17. RRF 怎样融合排序，为什么不简单做线性权重；RRF 常数怎样确定？
18. RAG Evaluation Dataset 怎样构建；业务实体和时间信息应在 Retrieval 前还是后提取？
19. 面对“某上市公司去年毛利率下降”之类金融问题，从 Prompt 到检索、计算、结论的完整 Agent 链路怎样设计？
20. 最终结论怎样 Verification，并把 Citation / Reference 正确映射回证据？
21. InnoDB、默认隔离级别、MVCC、幻读治理、binlog / undo / redo 怎样解释？
22. Clustered / Non-clustered Index 的区别是什么？
23. 子网与 VLAN 的基本边界是什么？
24. Coding：数组 Top-K；先讨论 Heap，再在面试官提示下继续到 Quickselect 与复杂度优化。

去重：历史中百度 `S034 / S197` 同样出现 Resume / Trace / Memory，但当前作者、日期、项目和完整题序不同；本场独有“LLM Runtime vs Tool Runtime → Streaming → Tool 并发 / 幂等 → Trace Hook → PDF 表格 HTML → RRF 常数 → 金融指标 Agent → MySQL / Network → Top-K”长链，确认是独立招聘流程。

---

## S327 百度｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-20 / 08-26｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/53542e2dcfd44b1d84b0ae55b4fc1b35

二面来源：https://www.nowcoder.com/feed/main/detail/bca7dc14bd654e91b89792608111b211

真人 / 第一人称证据：两篇均由作者 `在抱佛脚的芝士很完美` 发布，学校、技术方向与时间线一致。一面明确标注 8 月 20 日，二面标注 8 月 26 日；二面作者写“没什么八股，全在问项目细节”，后段被要求直接共享代码讲实现。两轮属于同一百度 Agent 秋招流程，因此合并为一个 `Sxxx`。

整场技术问题：

### 一面

1. 把 Agent 部署在本机用于异常进程排查时，需要考虑哪些权限、资源与安全边界？
2. Sandbox Instance 的并发数量受哪些资源约束，怎样做隔离？
3. 给现有 Agent 扩展能力时，功能、Tool 与 Runtime 应怎样拆？
4. Agent 遇到自身无法解决的任务时怎样安全失败、Fallback 或请求人工介入？
5. Memory Module 怎样设计；Long-term、Short-term 与当前 Context 冲突时以什么规则解决？
6. 从零设计 Enterprise Internal QA Agent，Knowledge、Retrieval、权限与生成链路怎样组织？
7. Agent 从识别到执行一个 Skill / Tool 的完整生命周期是什么？
8. LLM Token 的生成过程怎样理解，常见 Chat API Parameters 各自影响什么？
9. 模型本体是否天然具有跨请求 Memory，应用层怎样补足？
10. Linux 中怎样查看 CPU / Process 状态？
11. Docker Container 内进程与直接运行在 Host 上有什么隔离差异？
12. TCP 丢包怎样恢复；访问下游 TCP Service 发生 Connection Timeout 时如何端到端排查？
13. 传统 Backend 与 Agent Engineering 的复杂性分别体现在哪里？
14. Coding：Greedy + Heap 类现场题。

### 二面

15. 主流 Cloud Monitoring / Observability 组件有哪些，Agent 服务如何接入？
16. 为什么不直接使用开源 Agent Framework，而选择自行封装？
17. 不依赖开源框架时，至少需要自己实现哪些 Loop、State、Tool、Memory 与 Failure Handling 能力？
18. LangChain RAG 从数据进入到 Retrieval / Generation 的完整流程是什么？
19. FastAPI 异步调用 LLM 时，`await` 等待期间 CPU / Event Loop / Thread 的实际行为是什么？
20. Kubernetes 部署 Agent Service 需要理解哪些基本能力？
21. Windows 环境运行 Docker 时，资源隔离底层怎样实现？
22. 二面现场共享代码：怎样从真实实现证明上述框架封装和运行机制确实是本人完成？

去重：两条 URL 均未进入 `S001–S325`；同作者 8/20 → 8/26 时间线连续，主动合并。与历史百度 Coding Agent / Harness 来源相比，本场“本地异常进程 Agent → Sandbox 并发 → Memory Conflict → Enterprise QA → Linux / Docker / TCP → 自研 Framework → FastAPI Async → K8s / Windows Docker → 共享代码”题序独立。

---

## S328 阿里优酷 / 大文娱 AI 创新业务｜Agent 开发（实际面试内容）｜秋招一面｜面试 2026-09-03，发布 09-04，已过｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/bdebbb6088b6405e9eb2bd2c345acb6e

真人 / 第一人称证据：作者 `北巷南街` 的账号可连续核验本人字节后端实习、转正与外部秋招 Timeline；该帖明确更新“一面已过”。作者后续进度帖把该流程记为“阿里优酷 9.3 一面、约 9.7 二面”，原帖反问又明确出现“大文娱 AI 创新业务”。由于原帖标题内部 BU 名称与 Timeline 表述存在差异，本库不继续猜组织层级，只按可确认的阿里优酷 / 大文娱 AI 创新业务归档。正文围绕本人风控归因 Agent 被连续追到架构、Checkpoint、Skill、Evaluation、Java 稳定性与 RAG。

整场技术问题：

1. 风控归因 Agent 的业务背景、核心场景与完整方案是什么？
2. 为什么设计三级 Agent，而不是单一 ReAct + Tool？
3. 第二层为什么仍是编排 Agent；Main / Orchestrator / Atomic SubAgent 各自职责是什么？
4. 多层 Agent 怎样通信和传 Context，怎样保证子 Agent 不漏关键约束？
5. 纯 ReAct 除 Tool Call 不稳定外还有哪些问题；多层架构带来的 Latency / Cost 代价怎样衡量？
6. 三级结构是否真的提升准确率，在哪些真实 Case 中体现？
7. 多 Agent 完整执行链的 Observability 怎样做，如何同时看异常与 Token Usage？
8. 所谓 Agent“工程底座”到底包含哪些 Runtime 能力？
9. TAE Memory 与 Redis Checkpoint 各自解决什么问题？
10. Tool 已经产生外部成功副作用，但 Redis Checkpoint 写失败时，恢复后怎样避免重复执行？
11. Skill 多后端可插拔加载怎样实现？
12. 项目最困难的工程问题是什么，候选人怎样定位并解决？
13. 是否阅读 Claude Code 源码；它如何治理 Context？
14. Agent 正在执行时用户追加新要求，新指令怎样进入当前任务状态并影响后续计划？
15. 为什么用约 20 个真实归因 Case 并重复多轮执行；这样的 Dataset 覆盖是否足够？
16. Task Completion Rate 从低于一半提升到接近全量成功，指标、Baseline 与实验怎样定义？
17. Agent Evaluation 是人工还是机器；Dataset / Ground Truth 由谁构建，怎样保证可信？
18. 传统 Java 业务里的充值、退款、异步消息如何避免漏退、重复退款和状态错乱？
19. 全链路排查 Skill 怎样工作；按 LogID 拉日志时如何保证信息足够完整？
20. RAG 从 Ingestion 到 Recall / Fusion / Rerank 的完整链路是什么？
21. Query Rewrite 的作用是什么；飞书文档、表格、图片等异构内容分别怎样 Chunk？
22. 同一文档中两个逻辑相关表格被切分时，如何保存跨块关系？

去重：URL、作者与 9/3 阿里流程未在历史正式库出现；独特的“三级风控归因 Agent → Tool 成功但 Checkpoint 写失败 → Skill 多后端加载 → Claude Code 增量指令 → 真实 Case 三轮 Eval → 退款状态 → 飞书表格关联 Chunk”连续链与历史阿里样本不同。作者 Timeline 已出现同流程二面，但当前二面原始正文无法稳定打开，因此本批不让二面贡献任何问题，也不会把它另算新来源。

---

## S329 阿里控股｜Agent Infra 开发工程｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-17 / 08-21｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/0354c1c8f1164c8aaf0e3bb796b535c8

二面来源：https://www.nowcoder.com/feed/main/detail/627844d5923149b6ac46a631b2b41d5a

真人 / 第一人称证据：两篇均由 `爱写代码的菜coder` 发布。一面记录开场麦克风故障，二面继续沿同一蚂蚁 Agent 实习项目深挖，并明确写到“因为与岗位工作很像，Agent 自进化技术细节持续追了约 15 分钟”。作者招聘 Timeline 还能闭环到“阿里控股完成全部流程”，同一招聘流程证据充分。

整场技术问题：

### 一面

1. MAS / Multi-Agent System 中怎样做 Agent Selection？
2. 系统性能怎样同时用论文指标和真实业务数据证明？
3. 已经按 Role 划分 Agent 后，为什么还需要维护 Agent Pool？
4. Memory Mechanism 怎样实现，Long-term Memory Bad Case 怎样发现和修复？
5. 实习中怎样识别不合理请求，优化后面对高请求量时系统表现怎样？
6. 服务实际消耗多少资源，怎样发布；Multi-machine Deployment 如何扩展？
7. 蚂蚁实习完整做了什么，本人负责边界是什么？
8. Agent Self-evolution 怎样实现？
9. “进化”用哪些 Metric 判断，如何避免把偶然结果当能力提升？
10. Agent 自进化所需数据怎样采样 / 收集？
11. 项目中最有价值的工作是什么？
12. DAU 以及其它线上指标如何用于判断 Infra 价值？

### 二面

13. 蚂蚁实习从输入到交付的完整工作链路是什么？
14. Agent 侧具体怎样运行，真正遇到过哪些技术难点？
15. Agent 平台的展示 / 交互形态为什么这样定？
16. 因与目标团队工作高度匹配，继续对 Agent Self-evolution 做实现层连续追问：数据、触发、评估、回滚和有效性怎样闭环？
17. 除简历已有工作外，还有哪部分技术产出最能证明个人能力？
18. 平时怎样使用、约束和“驾驭”AI，而不是被工具牵着走？
19. 为什么选择当前团队，如何看待其它 Offer 与岗位匹配？

去重：两轮同作者、同岗位、同公司、四天间隔，合并为一个来源。历史阿里系虽已有 Agent Platform / Runtime 样本，但未出现该候选人的“Agent Pool → Self-evolution → Evolution Metric / Data Collection → DAU / Resource → 二面 15min Self-evolution 深挖”招聘链。

---

## S330 阿里云｜Agent Infra / Data Infra｜秋招一面 + AI Coding｜面试 2026-08-31，发布 09-01｜HUMAN-A

来源：https://www.nowcoder.com/discuss/924245733962719232

真人 / 第一人称证据：作者 `Florentino_73` 明确记录 8 月 31 日阿里云一面，并按 30min 项目深挖、10min 系统场景、20min Coding、反问、120min AI Coding 的实际时间结构复盘。反问中团队明确做 Agent Infra 的 Data Infra，包括数据处理、State Persistence 与 Post-train 相关工作，Role Scope 清晰。

整场技术问题：

1. 先围绕蚂蚁实习经历做约 30 分钟项目深挖：本人承担什么、核心系统怎样工作、工程难点是什么？
2. System Design：一台 Intel SGX 机器要向多租户提供计算服务，而单用户数据约 1GB，怎样设计资源与安全隔离？
3. EPC 资源只有约 512MB、数据必须频繁换入换出时，怎样保护机密性与完整性？
4. 用户数据 / PV 增长到原来的约 4 倍但系统吞吐没有提升，应该从哪些层定位 Bottleneck？
5. 该 SGX / EPC 场景潜在的 CPU、Memory、I/O、Encryption、Scheduling 瓶颈分别是什么？
6. Coding：解析嵌套重复字符串，要求用递归完成正确展开。
7. 反问确认 Agent Infra Data Infra 的边界：Data Processing、State Persistence 与 Post-train 数据链怎样衔接？
8. 120 分钟 AI Coding：实现阿里云 SLS → MySQL 的动态写入系统。
9. SLS → MySQL 数据接入如何处理 Schema / Mapping 的动态变化？
10. 长时间运行的数据写入任务需要覆盖哪些异常、Retry、幂等、断点和错误恢复场景？
11. AI Coding 产出的数据系统如何通过测试与运行结果证明可交付，而不是只生成第一版代码？

去重：原始 09-01 页面稳定可核验。外部追链发现 09-07 另一页面复用了“SGX 1GB / EPC 512MB → PV 4x 吞吐不涨 → 嵌套字符串”核心题序，同时扩写出大量额外高级题；由于发布时间更晚且同序特征强，本批只保留 8/31 原场，不让后发扩写页面贡献问题。

---

## S331 OPPO｜AI 应用研发 / Agent 方向（实际内容明确）｜秋招一面｜发布 2026-08-21，约 50min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/5a94fd0b4f924b8b903f28087b28d701

真人 / 第一人称证据：作者 `启明_不想秋招版` 记录约 50 分钟一面，并写自己原本想推掉流程但未能推掉；面试官主要沿简历持续追项目细节、个人贡献、异常处理和落地效果。虽然标题只写“OPPO 一面”，正文明确讨论“AI 应用研发方向”、Agent 项目、MCP / Skill / Tool / RAG 与 AI Coding，实际 Role Scope 清晰。

整场技术问题：

1. Agent 项目解决什么真实问题，为什么值得做？
2. 整体 Agent Flow 与核心模块怎样拆？
3. 候选人本人负责哪些模块，哪些是独立完成而非团队成果？
4. 用户需求从输入到最终交付怎样流转，哪些步骤需要 Human Confirmation？
5. 项目效果指标怎样定义、采集和统计？
6. Tool 参数错误、Execution Failure、Timeout 分别怎样处理？
7. 怎样保证 Agent 最终输出可靠？
8. AI 修改代码后怎样做 Regression / Verification，避免引入新问题？
9. MCP、Skill、Tool 与 RAG 的职责边界和适用场景分别是什么？
10. 真实客户端 / 业务功能如何接入 AI 能力；Network Failure 时怎样 Fallback？
11. 日常怎样使用 AI 工具，哪些工作可以交给 AI，哪些决策必须由人掌控？
12. 对 AI Application Engineering 的理解是什么，业务落地与 Infra 方向怎样选择？
13. 大模型怎样改变学习 / 开发方式，候选人的长期学习计划是什么？
14. 对目标岗位和团队的理解到什么程度？

去重：历史有其它 OPPO AI / Agent 场次，但作者、日期、项目与题序均不同。另发现 `https://www.nowcoder.com/feed/main/detail/953daca379ac40d58a813b972175dc87` 明确以“帮转 @启明_不想秋招版”方式转载本帖并夹带其它团队招聘信息；该页面只作为复制证据，零贡献。

---

## 本批典型排除 / 重复案例

- **内容账号 Gate：拼多多复活赛 Agent 一面** `https://www.nowcoder.com/feed/main/detail/2109cf8eb0254507911fbf86bcbf51e4`，技术题非常强，但作者 `赛文X` 同时经营“100+ 社招面经记录 / 订阅内容”生态。当前规则明确要求非内容账号，因此编号前撤出。
- **快手多版本复制链**：7/30 `https://www.nowcoder.com/feed/main/detail/8ef62dcdde1340f987507d2d1e1433a8` 的“父子索引 → BM25 → Rerank Top-K → 限流 → RAG Eval”题序，继续追到 2/9 一二面 `511a8021...`、3/20 `f4567cec...`、4/9 `7ce89f...` 等多个高度同序版本；无法可靠确认 7 月页为独立场次，整条不确定链不收。
- **美团精确重复**：9/2 AI 后端 `https://www.nowcoder.com/feed/main/detail/9b94f595d15148869e0334029b5ddb67` 已是历史 `S198`；不因近期重新进入热门结果而重复编号。
- **腾讯精确重复**：AI 应用 `a02baa2ac6634904992561494a1746a4` 已是 `S255`；WXG Agent / Coding Agent `3ffc762437274543b6a8f5e2ea6fb535` 已是 `S176`。
- **字节精确 / 语义重复**：TikTok Agent、App Infra、9/3 Agent 等热门结果均已在历史 Batch；另有 Seed / 专栏式页面存在答案化、付费或内容包装，继续零贡献。
- **阿里云后发扩写**：09-07 页面与 `S330` 的 SGX / EPC / PV / Coding 题序高度一致却加入大量额外高级题，无法证明为独立候选场次，排除后发链。
- **OPPO 明确转载**：`953daca379ac40d58a813b972175dc87` 明写“帮转”，只保留 `S331` 原作者页面。
- **美团疑似分享账号**：`398d270fc3eb407ca2341007cd13a1b2` 虽题量足，但作者以“继续分享最近面经”方式持续发布，评论还出现把美团误称腾讯的异常内容信号；当前无法稳定确认候选人本人，排除。

## Batch 19 信号

1. **热门公司仍能挖到新的独立 HUMAN-A，但必须精确搜公司 + 岗位 + 作者 Timeline。** 本轮回到热门公司后仍确认 6 个新流程，说明“热门公司来源已完全饱和”的判断还过早。
2. **Observability 从日志题升级到 Agent Runtime Trace。** 百度 `S326` 会直接追 Trace Hook 放在哪层、一次请求怎样形成 Trace、如何用 Trace 定位具体节点，已经是 Runtime 级验真。
3. **RAG 参数需要实验依据。** `S326` 不只问 Hybrid / RRF，而继续追为什么不用线性权重、RRF 常数怎样定、纯 Vector 与 Hybrid 的收益如何实验验证，并要求最终结论带可追溯 Citation。
4. **Agent Infra 开始与 Data / System Infra 深度融合。** 阿里云 `S330` 把 SGX / EPC、多租户安全、吞吐瓶颈、State Persistence 与 120min SLS → MySQL AI Coding 放在同一场，Agent Infra 已远不只是编排框架。
5. **Agent Self-evolution 从前沿名词变成真实工程题。** 阿里控股 `S329` 连续追 Agent Pool、自进化机制、Evolution Metric、数据采集、DAU、Resource 与二面 15 分钟实现细节，要求证明闭环而不是讲概念。
6. **Checkpoint + External Side Effect 继续成为热门公司的可靠性核心。** 阿里 `S328` 的“Tool 已成功但 Checkpoint 写失败”要求候选人处理恢复后的重复执行风险，与 Long-running Agent 的 Idempotence 直接连接。
7. **AI 应用项目验真越来越强调 Delivery / Regression。** OPPO `S331` 连续追个人贡献、真实效果、Tool Failure、Human Confirmation 和 AI 修改代码后的 Regression，而不是只问用了哪个 Framework。
8. **热门结果页的复制 / 内容包装比例非常高。** 本轮 PDD 强候选因内容账号撤出，快手强候选因跨月份同序复制链撤出，美团 / 腾讯 / 字节大量结果已是历史正式来源；“热门公司优先”必须与更严格 Provenance 同时执行。

本批新增 **6 个 HUMAN-A：`S326–S331`**。正式库累计 **331 个**，下一编号 **`S332`**。当前整体仍未达到来源饱和；热门公司中百度、阿里系仍能通过作者 Timeline 与精确岗位搜索找到高价值独立来源，但字节、腾讯、美团、快手的热门搜索面已表现出更高的历史重复 / 内容包装比例。