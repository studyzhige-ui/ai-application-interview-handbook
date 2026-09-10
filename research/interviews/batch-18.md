# Batch 18 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S320` 继续编号。正式来源仍必须同时满足：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场 / 招聘流程痕迹 + AI Application / Agent Role Scope + 正文稳定可核验 + 非转载 / 非合集 / 非内容账号 / 非重复 = HUMAN-A**。
>
> 分配编号前已重新直接回读 `batch-01.md` ～ `batch-17.md`，覆盖 `S001–S319`；随后逐条执行 URL、公司 / 岗位 / 日期 / 轮次、作者、项目语义、5～10 个独特题序特征与招聘 Timeline 去重。GitHub Code Search 的 0 命中只作辅助，不作为“未收录”证明。
>
> 本轮尤其严格处理复制链：发现 7 月 12 日一条带 PDD 内推导流的“AI Agent 面经”与 7 月 7 日更早的真人 Coding Agent 原帖几乎逐题同序。后发页面排除，只保留更早、作者评论区能继续核验本人被问穿现场的原帖。另有 9 月淘天专栏候选因内容账号属性 + 60% 付费墙无法完整核验而排除；一条 7 月字节 AI 应用候选因题序与历史 `S229` 高度重合而在分配 ID 前撤出。

---

## S320 匿名 B 端小公司｜Coding Agent / Agent 开发｜技术面｜面试 2026-07-06，发布 07-07｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/5733bf8605d44262a596ad7ba738e737

真人 / 第一人称证据：作者“迷茫期已过”明确写“7.6 面试”、B 端小公司，并在评论区继续回应“面试原本没太准备，结果被问穿了”；其他候选人追问公司 / 岗位、项目来源，形成真实互动。正文从本人本地 Coding Agent 项目一路追到 Context / Memory 污染、Harness、Benchmark、安全审计与大型 Repo 跨模块修改，不是答案型题单。

整场技术问题：

1. 本地 Coding Agent 从输入任务到最终修改代码的完整执行链路是什么？
2. 支持多个模型后端时，怎样抽象请求格式、响应结构、错误码和 Retry？
3. 一个新 Tool 从定义、注册、被 Agent 发现到最终调用，完整生命周期是什么？
4. 文件不存在、命令超时、权限不足等 Tool Failure 出现时，怎样 Recovery / Retry？
5. 多轮代码修改导致 Context 不断增长时，真实项目里怎样治理？
6. Context Compression 后如何判断没有破坏当前任务？
7. Task Summary、File Summary、Process Notes 等压缩产物怎样生成和维护，哪些信息不能丢？
8. 摘要漏掉关键约束、导致后续 Agent 做错时，怎样发现并纠正？
9. Long-term Memory 中保存了过时 File Summary 时，怎样避免污染后续判断？
10. 模型把错误结论写进 Memory 后，如何修正并阻止错误继续传播？
11. Agent 反复读取同一文件或重复调用同一 Tool 时，如何识别重复状态 / Loop？
12. RAG、Memory 与 Context Engineering 在 Coding Agent 中分别解决什么问题，怎样协同？
13. Agent Harness 与单纯调用 LLM API 的本质区别是什么？
14. Agent Benchmark / Case / Metric 怎样设计，如何判断一次改动真的让 Agent 变强？
15. 生成错误 Patch 后，怎样 Rollback、Verify 与 Retry？
16. 一个真实需求到来时，日常怎样使用 AI 辅助完成开发？
17. 怎样拆需求、读代码、让模型修改、跑测试并 Review 结果？
18. 如果把本地 Coding Agent 做成团队内部工具，文件读写、命令执行、Sensitive Data、Permission 与 Audit 怎样设计？
19. 大型代码仓库跨模块修改时，如何先理解 Architecture，再做 Retrieval、Planning、Modification 与 Verification？

去重：URL 未在 `S001–S319` 正式库出现；“多模型后端 → Tool Lifecycle → Context Compression 正确性 → 过时 File Summary / 错误 Memory → 重复状态 → Harness / Benchmark → Patch Rollback → 团队权限审计 → 大 Repo 跨模块修改”题序未在历史 Batch 构成同场重复。外部核验发现 07-12 的 `https://www.nowcoder.com/discuss/905861577826463744` 几乎逐题重排并加入 PDD 内推导流，发布时间晚于本帖且缺少原作者评论互动，判后发复制链，不计新来源。

---

## S321 北京 B 端 AI 小公司｜AI / Agent 开发｜技术面｜面试 2026-07-14，发布 07-23，约 60min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/43d1bfd538dc43edb6739e00dabf054c

真人 / 第一人称证据：作者明确记录 7 月 14 日、约 60 分钟，并写自己“坐在学校的小破面试亭、只有一个小风扇”“刚刚没讲清楚又被问了一遍”“感觉 gg 了”。末段还现场打开一个项目，用 AI 修 Bug、生成背景 / 根因 / 解决方案材料并口头汇报，面试官随后给出项目不错但工程细节表达不清的反馈，现场痕迹很强。

整场技术问题：

1. 为什么选择当前 Multi-Agent 项目，真实目标是什么？
2. 自己负责的 Adapter 模块怎样适配多个外部 Agent？
3. 不同 Agent 事件格式怎样统一适配；第一次没讲清后为什么被再次追问？
4. 项目为什么叫 IM 风格，IM 风格在 Agent 协作里具体指什么？
5. 为什么选择 OpenCode 作为 Local Agent，它在系统里承担什么职责？
6. 自建 Agent 的底层逻辑是什么，用户可以自定义哪些能力？
7. 不同 Agent 的 Tool Calling 有什么差异，怎样实现？
8. 第二个 RAG 项目的完整链路是什么？
9. RAG 的分词 / Chunk Strategy 怎样设计？
10. Embedding Model 怎样选型，为什么选当前模型？
11. LangGraph 中有哪些 Node，各自职责是什么？
12. RAG 是全局触发还是按条件触发，触发机制怎样设计？
13. Retrieval Recall 怎样评测，不同问题类型是否分别建立 Evaluation？
14. 简历中的效果数字具体怎样测出来，基线和验证方式是什么？
15. Multi-turn Conversation Compression 怎样做，Short-term / Long-term Memory 哪些内容优先裁剪？
16. Dynamic Compression 实际效果怎样验证？
17. AI 协作现场题：打开真实项目，使用 AI 处理一个 Bug，输出背景、Root Cause、Solution，并做简短汇报。
18. 面试反馈：项目认可，但工程化细节表达不清，应怎样证明真正做过而不是只讲架构名词？

去重：URL、作者、日期与招聘场次均未在正式库出现；独特的“外部 Agent Adapter / Event 适配 → IM 风格 → OpenCode Local Agent → RAG 评测数字验真 → Dynamic Compression → 现场 AI Debug + Root Cause 汇报”题序未与历史来源重合。

---

## S322 佰聆数据｜助理 AI 应用开发工程师实习｜一面｜面试 2026-07-14，发布 07-15｜HUMAN-A

来源：https://www.nowcoder.com/discuss/906897383676538880

真人 / 第一人称证据：作者“魔仙堡的小莫仙w”明确给出公司、岗位、面试日期，并记录“面试官迟到 5 分钟、不开摄像头”“Agent 相关基本答上来了”“面试官偏实际应用、没有沿简历项目展开”等现场评价；评论区继续询问后续流程，属于个人面试记录而非题库。

整场技术问题：

1. Python 中处理 / 校验大模型调用产生 JSON 输出常用什么包或机制，LangGraph / LangChain 中怎样落地？
2. 怎样理解 Agent Skill？
3. Skill、传统 Prompt Engineering 与 MCP 的差异和边界是什么？
4. 大模型检索了解哪些 Retrieval Algorithm？
5. 是否做过 Fine-tuning；资源受限时如何根据训练现象判断 Learning Rate 偏高或偏低？
6. A2A Protocol 与 SubAgent 分别解决什么问题？
7. Prompt Engineering 的核心组成和实际设计原则是什么？
8. 如果从零设计 Context Management 功能，会包含哪些内容？
9. Frontend 调用 Agent 时如何选择通信协议？
10. 已经会 FastAPI GET / POST 后，如果要支撑 Claude Code 式完整体系，还需要补哪些 Runtime / Streaming / Session 能力？
11. FastAPI 在 Python 中的底层 Web Server / ASGI 组件是什么，调用链怎样理解？
12. 如果面试官认为 Python 理解不深，怎样用一个具体知识点证明 Python 能力？

去重：已回读全部历史 Batch；URL、佰聆数据流程和“LLM JSON 校验 → Skill / Prompt / MCP → Fine-tuning LR → A2A / SubAgent → 前端 Agent 协议 → FastAPI / ASGI 底层 → Python 深度验真”连续题序均未出现。

---

## S323 机械星球（要务科技）｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-16，凉经｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/e07bd10a97f84ece9f2ce6298b2ca72c

真人 / 第一人称证据：作者 `Luxlord` 直接以 7 月 14 日 AI 应用开发一面凉经发布，问题中保留大量即时反应：承认三个项目都是个人练手、真实用户只是舍友；Spring / Nacos 追问时“开始憋笑”“不敢再说学过 SpringCloud”；把 Shell 听成“xue”并在面后问 AI 才确认。属于难以模板化伪造的真实答题状态。

整场技术问题：

1. 三个项目是否都是个人练手，是否真实部署、是否有人实际使用？
2. RAG 项目真实用户反馈过哪些不足？
3. RAG 项目最难的部分是什么，Spring AI 编排和 RAG Quality 分别踩过什么坑？
4. LangGraph 项目最难的地方是什么，Multi-Agent 信息传递、格式与 Hallucination 怎样处理？
5. Full-stack 开发中的 CORS / Cross-origin 怎样解决？
6. Spring Boot 类 / Bean 加载顺序怎样控制？
7. Authentication 怎样做，Token 如何在前后端传递？
8. 不同 Controller 的 Authorization / Access Control 怎样实现？
9. Nacos 作为 Registration Center 怎样使用？
10. Spring Boot 启动后怎样加载 Nacos Configuration？
11. Nacos 配置更新后如何实现 Hot Reload / Dynamic Refresh？
12. 是否使用过 Linux，实际部署服务器是什么系统？
13. 本地怎样连接和操作云端 Linux？
14. 自己的项目如何部署，Production Monitoring 怎样做？
15. 是否写过 Shell Script；候选人现场没听清术语，面后才确认？
16. 给一个 Monolith Legacy Project，怎样拆成 Microservices？
17. 拆分后 Service Discovery、OpenFeign / MQ、Gateway Auth、Nginx / Sentinel、Distributed Transaction、Cache、Thread Pool、SQL Optimization 分别放在哪里？
18. 反问：公司真实业务是否做 Agent，以及团队如何看待 AI Coding？

去重：历史中虽有大量“AI 岗 + Java / Spring”样本，但本场“练手项目是否真有人用 → Spring AI / LangGraph → CORS / Auth → Spring Boot 加载顺序 → Nacos 配置热更 → 连 Linux 系统名都没注意 → Shell 听音失误 → Monolith 改微服务”的真人失败轨迹和题序独立，URL / 作者 / 公司流程均未命中。

---

## S324 钉学科技｜FDE 实习｜技术面｜面试 2026-08-13，发布 08-18｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/c837307a81854e208eea037766f0bdcf

真人 / 第一人称证据：作者以本人 8 月 13 日 FDE 实习面试记录发布，末尾写“面试官说答得还可以，但是三天了还没有推进后续”；评论区有人质疑“这更像 AI 应用开发”，恰好反向说明岗位实际技术职责集中在 Agent / RAG / Workflow，符合本库 FDE / Applied AI Role Scope，而不是传统售前或纯方案岗。

整场技术问题：

1. 简历中的项目是否为本人核心参与，具体负责什么？
2. Code Review Workflow 中三个并行 SubAgent 在 Prompt 与 Tool Selection 上怎样区分职责？
3. Supervisor Agent 汇总多个 SubAgent 结果时，怎样处理 Conflict 与 Priority？
4. RAG 只做 Vector Retrieval 有什么缺陷，BM25 补了什么短板？
5. 两路 Retrieval 的结果怎样 Merge / Rank？
6. 给一个真实 Case，证明 Hybrid Retrieval 比单一路径更好？
7. SubAgent 循环 Retry 到上限后怎样终止、降级或转人工？
8. LangGraph Checkpointer / Workflow Persistence 应保存哪些 State 字段？
9. Human-in-the-loop 长时间不确认时，Timeout Policy 怎样设计？
10. Node State 同时落 MySQL 与 Redis 时，怎样处理一致性？
11. Workflow 中断后 Resume，如果用户已经切换 Model，旧状态如何兼容 / Migration？
12. MCP 与 Function Call 的区别是什么？
13. LangChain 与 LangGraph 分别适合什么场景？
14. 使用 LangGraph 编排 Workflow 时，Edge、Node、State 哪个最重要，为什么？

去重：URL 与钉学 FDE 招聘流程未在 `S001–S319` 出现；“三并行 Code Review SubAgent → Supervisor Conflict Merge → Hybrid Retrieval Case → Retry Upper Bound → Checkpointer 字段 → Human Timeout → MySQL/Redis State Consistency → Resume 后模型切换”的题序高度独特，未发现同场复制链。

---

## S325 虾皮（Shopee）｜Agent 开发｜二面｜发布 2026-08-24，约 30min，面后即挂｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/345b668e35a9451bb397a9189dfdc943

真人 / 第一人称证据：作者为持续记录本人社招面试的全栈候选人。本帖明确写“二面、30min、面完就挂”，并记录“感觉方向又不匹配、自己说的东西面试官不接话”；评论区围绕学历、Runtime 与岗位匹配继续互动，招聘结果与现场情绪明确。

整场技术问题：

1. 个人 Agent 项目具体做了什么，哪些部分值得深挖？
2. 未来技术发展方向怎样选择？
3. 新一代 Framework / Tool 出现时，怎样判断旧方案是否应该淘汰，而不是盲目追新？
4. Agent Runtime 在 Retry 这一层的实现细节是什么？
5. 如果从零做新一代 AI-native Platform，核心架构怎样拆？
6. 是否了解 Operations Research Agent，它与普通通用 Agent 有什么差异？
7. 怎样看待当前新一轮 AI 技术革命，对 Agent 工程岗位意味着什么？

去重：历史已有 `S081` 虾皮 Agent 一面，但作者、题序和招聘 Timeline 不同：`S081` 为另一位候选人的 8/20 一面，重点是 ReAct / Tool Message / Memory / Context；本场为另一作者的二面并围绕“旧轮子淘汰判断 → Runtime Retry 细节 → AI-native Platform → 运筹学 Agent”展开，确认是独立招聘流程，不合并。

---

## 本批典型排除 / 重复案例

- **后发复制 / 导流**：`https://www.nowcoder.com/discuss/905861577826463744`，07-12 发布，19 道 Coding Agent 问题与 `S320` 07-07 原帖几乎逐题同序，并夹带 PDD 内推链接；排除后发链。
- **历史语义重复**：07-14 字节 AI 应用开发 `https://www.nowcoder.com/feed/main/detail/3e22dc2df03d4227ab70ea9c2d896086` 真人痕迹很强，但“Agent 模块 / API 异常自恢复 / Token → 线程池重设计 → JVM 类加载 → MySQL 三日志 / 两阶段提交 → 合并数组”的连续题序与历史 `S229` 高度重合；不新增。
- **内容账号 + 付费墙**：09-04 淘天 Agent 业务场景帖 `https://www.nowcoder.com/discuss/925525428259885056` 作者为专栏型账号，正文约 60% 被付费墙截断，无法完整稳定核验；排除。
- **模板化但第一人称不足**：安软 AI 应用开发实习 `https://api-cdn.nowcoder.com/feed/main/detail/40920533fad14136bff01c3928c7e953` 虽题量大、元数据完整，但正文高度结构化，缺少候选人答题状态 / 追问 / 结果 / 现场互动，无法稳定证明是候选人本人第一人称原始面经；排除。
- **推广型“精品面经”**：字节火山方舟 Managed Agent 候选正文夹带 Agent 题库 / GitHub 项目推荐，整体呈内容推广包装；在无法排除内容账号属性前不纳入。
- **低密度**：微博智搜、游戏小厂 AI 全栈等虽有真人现场，但仅 5～7 个高度概括的问题且缺少足够连续追问，质量不稳定，本批不为凑数放行。

## Batch 18 信号

1. **Coding Agent 的 Context / Memory 正确性进入“污染治理”阶段。** 面试官不只问压缩，而是追过时 File Summary、错误结论写入 Memory、重复状态与压缩后任务完整性。
2. **AI Coding 开始被直接当成现场能力测试。** `S321` 要求打开真实项目，让 AI 修 Bug，并输出背景、Root Cause、Solution 后现场汇报，已经从“你平时用不用 Cursor”升级成可观察的工程协作行为。
3. **FDE / Applied AI 正在下钻 Runtime State。** `S324` 连续追 Checkpointer 字段、Human-in-the-loop Timeout、MySQL / Redis 状态一致性和 Resume 后切换 Model，岗位边界明显偏工程交付而非纯方案。
4. **FastAPI / Python 不能只会 API 表层。** `S322` 从 Agent 前端协议继续追到 FastAPI / ASGI 底层和“怎样证明 Python 深度”，AI 应用岗位的 Runtime 基础要求在上升。
5. **AI 应用岗依然大量验真传统后端。** `S323` 把 RAG / LangGraph 与 CORS、Auth、Spring Boot、Nacos、Linux、Monitoring、Monolith → Microservice 放在同一场里，说明“Agent + Backend”仍是一体化能力模型。
6. **复制链 / 内容包装已经成为主要噪声。** 本轮强候选中同时出现后发逐题改写、付费专栏、推广型“精品面经”和历史同序换公司标签；新增来源的 Provenance 成本继续上升。

本批新增 **6 个 HUMAN-A：`S320–S325`**。正式库累计 **325 个**，下一编号 **`S326`**。当前尚未整体达到来源饱和，但牛客热门 Agent 关键词已明显接近**局部来源饱和**：新的高质量独立样本更多来自长尾日期、冷门公司、FDE / AI Application 别名和作者 Timeline 深挖，而不是热门搜索结果页。