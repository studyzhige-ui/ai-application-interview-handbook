# Batch 12 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> 本批从 `S255` 继续编号，严格执行：**真人面试官 + 候选人本人第一人称 + 高信息密度 + 真实现场痕迹 + AI Application / Agent 目标岗位 + 正文稳定可核验 + 非转载 / 非合集 / 非重复 = HUMAN-A**。
>
> 本轮继续按 `公司 × 岗位别名 × 月份 × 技术关键词` 扩大 Recall，并回看企业 / 话题页、作者时间线、评论区与跨站结果。平台没有配额；搜索摘要、题库、完整答案、课程 / SEO、付费墙和无法稳定确认原作者的复制链均零贡献。
>
> 通过 Role Scope 后保留整场真实技术问题，不只摘 Agent / RAG：Backend、Java / Python、MySQL、Redis、并发、网络、Coding、AI Coding、System Design 与 Agent Harness / Runtime 同等记录。
>
> 去重固定执行三层：**URL 精确去重 + 题序 / 项目语义去重 + 作者 / 招聘流程时间线去重**。同一候选人同一流程多轮合并为一个 `Sxxx`。

---

## S255 腾讯｜AI 应用开发｜一面｜面试 2026-07-25，发布 07-30｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a02baa2ac6634904992561494a1746a4

真人 / 第一人称证据：作者明确写出 7 月 25 日本人 AI 应用开发一面，正文是连续技术问题而非答案整理；文末更新“现在还没有消息，估计是凉了”并以“发面经攒人品”发布，评论继续询问批次 / 手撕，招聘现场与面后状态可核验。

高价值问题：

1. Prompt、RAG、微调、Workflow、Agent 分别应在什么情况下选择？
2. 为什么很多应用不应该一开始就微调，为什么复杂任务也不一定适合 Agent？
3. Workflow 与 Agent 的工程分界线是什么？
4. Token / Context Window 对线上工程意味着什么，上下文被截断时先怎么处理？
5. 大模型应用上线前最关注哪些效果、延迟、稳定性和成本指标？
6. LLM / RAG 服务如何设计降级策略？
7. 成本超预算时应优先优化哪一层，如何证明优化有效？
8. Prompt / Model / Index 如何做版本管理和快速回滚？
9. Agentic RAG 与固定“一次检索后生成”的差异是什么，哪些 bad case 才值得升级？
10. 多轮补检如何限制延迟和成本，避免 Agentic RAG 无界扩张？

去重：URL 未在 `S001–S254` 出现；公司 / 岗位 / 题序与现有腾讯样本不构成同场，未发现同作者同流程已入库记录。

---

## S256 嘉为科技｜AI 应用开发｜技术面｜面试 2026-07-15，发布 07-16｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/fb4da04c8f2846b19060315fd05a2e4b

真人 / 第一人称证据：作者以本人 7 月 15 日面试发布“发面经攒人品”，25 个问题中持续保留“我说了什么 / 当时如何回答”的第一人称括注，问题从真实项目一路追到 Redis、Spring AI、JVM、并发与 Claude Code，具有自然面试流而非标准化题单。

高价值问题：

1. 项目里为什么使用 `CompletableFuture`，为什么需要自定义线程池？
2. 项目真实部署过吗，常见部署方式分别怎样选择？
3. Bloom Filter 的原理和适用场景是什么？
4. Redisson 可重入锁、Watchdog 如何实现，无限续期怎样避免演变成死锁？
5. Redis Cluster 与 Sentinel 的边界是什么？
6. Spring AI 中 Memory 如何实现，直接使用模型 SDK 与 Spring AI 的取舍是什么？
7. 批量导入同一券 / 卡密时如何处理并发、加密和重复发券重试？
8. 实习项目里的状态机如何保证消息重试后不重复执行？
9. Claude Code 在真实实习开发里怎么使用，哪些工作由人负责兜底？
10. MyBatis 接口代理、Bean 生命周期、Java 对象头与锁升级机制如何解释？

去重：URL 与标题均未在现有 Batch 命中；题序与项目链路未发现现有同场复制。

---

## S257 字节跳动｜Agent 全栈开发｜一面｜面试 / 发布 2026-06-23｜HUMAN-A

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

## S258 广州某小厂｜Agent 后端开发｜一面（三阶段）｜发布 2026-06-12｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/a23d2e7a98ac433a82a41c8108646780

真人 / 第一人称证据：作者明确记录整场约 2.5 小时，分为 1h 架构深挖、1h Vibe Coding、30min 围绕改进代码继续追问；多次写到面试官会提示 / 引导并给反馈，自己后半段已记不清具体追问，现场痕迹非常强。

高价值问题：

1. 共享屏幕带面试官阅读提交作业的核心代码，并解释关键设计。
2. ReAct 的理解以及其写法 / 工程实现如何演进？
3. Function Calling 底层如何从模型输出走到真实函数执行？
4. Tool 只返回字符串有什么局限；结构化 Tool Result 如何支持后端生命周期管理？
5. 如果从 Tool Registration 开始重做一个 Tool Framework，会怎样设计 Registry、Schema、Execution 与 Result？
6. 5–10 分钟的异步 Tool 怎样执行而不阻塞 Agent 主循环？
7. 异步 Tool 尚未结束时用户继续对话，结果何时、通过什么 Hook / Event 插回 Context？
8. 现场 Vibe Coding：在现有 Agent Framework 上选择一个方向做真实改进。
9. 第三阶段围绕候选人刚写出的改动继续做架构与实现追问，并要求解释取舍。

去重：URL、题序和“1h 架构 + 1h Vibe Coding + 30min 复盘”时间线均未在现有来源命中；未发现跨站同场原帖冲突。

---

## S259 多益网络｜AI 应用工程师｜一面 + 三面（同一候选人同流程合并）｜2026-08-20 / 08-28｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/f5f1a4daff104fcb8c48476ed9c99f39

三面来源：https://www.nowcoder.com/discuss/922801355649974272

真人 / 第一人称证据：两个页面由同一作者发布，三面正文明确链接一面为“前传”，因此按同一候选人同一招聘流程合并为一个来源。一面保留自己项目细节编得不扎实、没听清追问等状态；三面记录约 50 分钟、RAG 回答到一半被面试官切题、Coding 因边界条件导致死循环、面后自评以及评论区其他候选人的流程核验。

高价值问题：

1. 三级 Memory 如何实现，为什么能声称 20 轮后仍保留 90% 信息，怎样验证这个指标？
2. 为什么项目需要 RAG，它在完整用户请求链路中解决什么问题？
3. 项目真实团队如何分工，候选人本人负责哪些部分，项目指标是否真实？
4. Multi-Agent 项目为什么要做，协作触发和信息流转如何设计？
5. AI Coding 在项目中的实际编码占比与使用方式是什么，怎样做人工验证？
6. 三面深挖 `Router / WorkList / InvocationQueue / Session` 分别存什么、一次输入怎样流转？
7. Context Compression 策略怎样设计；把当前 Agent 架构做成分布式后要改哪些状态边界？
8. `InvocationQueue` 如何保证执行过程中信息不丢失？
9. 主流 Agent Architecture、RAG Dense / Sparse Retrieval 的作用与组合方式是什么？
10. MySQL Index 类型及优缺点、多线程与多进程怎样理解？
11. 给一个新功能，如何让 AI 参与需求、实现、测试与人工验收，而不是只生成代码？
12. Coding：合并有序数组；现场实现出现死循环时如何快速定位边界条件。

去重：一面与三面明确同作者 / 同岗位 / 同流程，主动合并，不拆成两个 HUMAN-A；两条 URL 均未在 `S001–S254` 收录。

---

## S260 小红书｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-12 / 08-17，发布 09-02｜HUMAN-A

一面来源：https://www.nowcoder.com/feed/main/detail/f1ed02bfdae04730837753b62e0d58b9

二面来源：https://www.nowcoder.com/feed/main/detail/9f7361c709f4413396988b4f334a0d6f

真人 / 第一人称证据：两篇均由同一作者发布，作者展示身份与项目时间线一致。一面作者写自己第一次正式面 Agent、几乎没准备，晚饭后即收到二面邀请；二面明确面试时间 8 月 17 日，记录“被问得很凶”、面试官技术很强、自己复盘感觉一般，但仍被约三面。属于同一候选人同一小红书 Agent 秋招流程，因此合并为一个来源。

高价值问题：

1. 实习项目真正关注哪些业务 / 技术指标，数字如何获得、上下游和代码框架是什么？
2. Agent 在真实项目中到底用在哪里，而不是简历上只写一个框架名？
3. OpenManus 使用什么框架，怎样理解 Agent Harness？
4. Multi-Agent 并发会带来哪些资源竞争问题，如何限制并发量并隔离 Context / State？
5. Long-term / Short-term Memory 的底层实现方式是什么？
6. ReAct 与 Planner / Executor / Critic 的关系是什么，为什么当前项目不用另一种模式？
7. 二面继续追：实习 Agent 从输入到结果的完整架构与数据流是什么，结构化结论如何产生并校验？
8. 为什么选择 OpenManus，而不是 LangGraph 做编排？Workflow 与自主 Agent 的边界是什么？
9. Prompt Injection 如何泄露 System Prompt 或绕过指令，怎样建立防护边界？
10. Tool Call 如果没有次数 / 权限限制会带来哪些风险，怎样做 Permission、Quota 与高风险操作确认？
11. 如果把现有单 Agent 改成 Multi-Agent，会新增哪些冲突、共享资源和状态一致性风险？
12. System Design：本地 Agent + 云端 Agent 需要服务大量设备时，怎样做任务路由、状态同步与安全边界？

去重：一面与二面由同一作者、同公司、同岗位且招聘时间线连续，二面主动合并回 `S260`，不新增来源数量；与现有小红书其它候选人的题序、项目和作者均不同。

---

## S261 拼多多｜Agent 开发｜二面｜面试 2026-08-25，40min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/f5e7351df8364147ac8da085b99d9d18

真人 / 第一人称证据：作者明确给出 8 月 25 日、40 分钟二面，正文区分“项目&基础 / 手撕”，面后评价“没有硬八股，抓住问题与项目结合点先说原理再说应用”，并以发面经攒人品发布。

高价值问题：

1. Agent 怎样实现不同任务之间的状态与 Context Isolation？
2. Agent 如何保证分析和最终输出的准确性？
3. Evaluation 体系怎样设计，测试用例覆盖范围如何确定？
4. 从用户输入到 Agent 执行 / 回答的完整业务流是什么？
5. LangChain 与 LangGraph 的核心差异是什么，什么场景需要图状态机？
6. 自研 Agent Framework 与开源框架的差异和选择依据是什么？
7. Coding：实现线程安全的 LRU，并解释并发控制选择。

去重：本来源与检索到的拼多多“提前批一面”复制链作者、日期和题序均不同，是独立候选人的二面；URL 未入库。

---

## S262 要务科技｜AI 应用开发实习生｜一面｜发布 2026-08-27｜HUMAN-A

来源：https://www.nowcoder.com/discuss/922574588683227136

真人 / 第一人称证据：作者以本人暑期一面记录项目与八股；面试官要求直接共享屏幕讲代码，作者明确写“让人有点懵，希望有二面”，评论区继续围绕 Harness / 权限问题讨论，具备现场操作和面后状态痕迹。

高价值问题：

1. 登录功能如何实现 Authentication / Authorization，AOP 与 Interceptor 怎样选？
2. 结构化商户信息怎样做 Embedding 并写入 Vector DB？
3. 只做 Dense Vector Retrieval 会出现哪些召回问题，怎样改进？
4. MCP 的核心作用是什么，是否真正写过 MCP Server 而不仅是配置插件？
5. Skill 与 Harness 的关系是什么，Skill Metadata 在加载 / 选择阶段起什么作用？
6. Python 在 AI Service 中用到什么深度，是否真正用 LangChain 做过 RAG？
7. Linux 实操能力如何，线上常用哪些命令 / 中间件？
8. Docker 如何完成 AI 应用的打包、部署与环境隔离？
9. 共享屏幕阅读项目代码时，如何证明简历里的实现确实是本人完成？

去重：与 `S263` 虽同公司同岗位，但作者、学校、发布时间、项目和问题链完全不同，确认为不同候选人的独立招聘流程，分别计数。

---

## S263 要务科技｜AI 应用开发实习生｜一面｜面试 2026-09-07，约 46min｜HUMAN-A

来源：https://www.nowcoder.com/discuss/926539013991796736

真人 / 第一人称证据：作者明确给出本人背景、9 月 7 日一面和约 46 分钟时长，逐题保留自己真实回答、未考虑到的地方以及面试官建议；文末记录面试官正面评价、改进建议和“还有二面”的流程信息，现场证据非常完整。

高价值问题：

1. 第三方消息接入中，落库成功但发送失败如何实现 Final Consistency、Retry 与用户可见状态？
2. Webhook 大面积堆积如何扩展；Signature、Idempotency、主动拉取怎样形成多重保障？
3. 20 万行 Excel 怎样解析 / 批量导入，如何控制内存和 DB 压力？
4. PDF 转写为什么能从约 31 分钟降到 2.5 分钟，性能收益怎样验证？
5. AI 客服为什么做 30 秒消息聚合 / Debounce，体验与延迟怎么权衡？
6. Prompt Injection 与高风险写操作怎样治理；为什么应把修改权限留给用户或受控 Tool？
7. PDF / Word / PPT / 图片型 PDF 混合知识库如何解析并做多模态 RAG？
8. 多语言语境差异会怎样影响 Embedding / Retrieval，未覆盖的 Failure Case 怎么处理？
9. AI Coding 从需求澄清、Skill、Plan、实现到 Compile / Unit Test / Browser Test 的完整流程是什么？
10. 如何限制 AI 重复造轮子，Skill Progressive Disclosure 如何降低 Context Token 占用？
11. 实时口语 / 客服辅助场景中 ASR、LLM、SSE / WebSocket 怎样组成低延迟链路？
12. Redis 在鉴权与权限缓存中的职责是什么，怎样避免前端越权？

去重：独特第三方托管 / Webhook / PDF 性能优化项目链及作者时间线未在现有 Batch 出现；与同公司 `S262` 为不同候选人，不合并。

---

## S264 猎豹移动｜Agent 全栈开发｜技术面｜发布 2026-05-13，约 40min｜HUMAN-A

来源：https://www.nowcoder.com/feed/main/detail/1388e30b7bb64f0ea60599f828263a14

真人 / 第一人称证据：作者标题即明确“40min，忘记录了，但是还记得一些面经”，是本人面后根据记忆复盘而非二次整理；问题围绕同一 Agent 全栈场景连续进入 Graph / DAG、循环 RAG、Memory、Multi-Agent、Gateway 和项目本人职责。

高价值问题：

1. Graph / DAG Agent Framework 怎样理解，DAG 与允许循环的图分别适合什么任务？
2. “每日自动分析并编排工作计划”的 Agent 应怎样设计整体架构？
3. 这类持久化能力应该沉淀为 Skill 还是 Long-term Memory，判断边界是什么？
4. Multi-Agent 出现 Dead Loop 或 Agent 互相推诿时，怎样监控、检测并终止？
5. Long-running Generation 被截断导致代码 / 文档不完整时，工程上怎样恢复？
6. Prompt 层的 Few-shot / Self-check 与代码层 Retry / Cleanup 分别能解决什么？
7. MCP 与 Skill 的职责边界是什么？
8. 如何设计一个统一 LLM Gateway，处理多模型接入、路由、限流与失败降级？
9. Skill 能力未来怎样演进，怎样避免全部能力一次性进入 Context？
10. 项目 / 竞赛中候选人本人担任什么角色，具体负责哪些代码与架构决策？

去重：URL 和完整 DAG / 循环 RAG / 工作计划 Agent 题序未在 `S001–S254` 命中；未发现同作者同场转载。

---

# 本批清洗与研究观察

本批正式新增：**10 个 HUMAN-A（S255–S264）**。

后续维护补充：Batch 13 搜索中发现 `S260` 同一候选人的 8 月 17 日小红书 Agent 二面，已按同一招聘流程合并回 `S260`；来源总数不因此增加。

## 典型排除

- **拼多多提前批 AI Agent 一面复制链**：`328260668ec94ebda5c84de205d13a58` 与 `d0c1a59663a2408fb9f8b52b87ccaaec` 来自不同账号、发布时间相差约一天，但题序、项目语义和措辞高度一致；无法可靠确认真正原场次，按规则整链排除，不猜原作者。
- **快手 AI 应用 / Agent 开发 9 月内容链**：正文由内容账号持续生产，并出现订阅 / 付费墙、同一叙事多版本扩写；即使问题漂亮也不进入 HUMAN-A。
- **CSDN / Agent 社区学习路线、107 道题、完整答案 / 面试“必杀技”**：属于教学、SEO、题库或二次整理，全部零贡献。
- **只能从搜索摘要 / 聚合页看到标题或片段的跨平台结果**：无法稳定核验候选人本人和原始正文，排除。
- **月之暗面 AI-Native Desktop 三轮题单**：Role Scope 匹配且问题很有价值，但正文缺少足够明确的候选人第一人称现场状态 / 面后结果，本批按保守标准不纳入正式统计。
- **字节 9.3 Agent 开发**：Batch 12 当时因单页现场 / 招聘流程证据不足而暂缓；Batch 13 沿作者主页补齐连续秋招时间线后升级为 HUMAN-A `S275`。这属于补证后升级，不是降低准入门槛。
- **京东 5.8 后端 Agent 等边缘候选**：题目本身有价值，但当前能确认的现场 / 招聘流程证据仍不足，继续不进入 HUMAN-A。

## 本批新增信号

1. **“先判断要不要 Agent”已经成为真实能力题。** 腾讯直接把 Prompt / RAG / Fine-tuning / Workflow / Agent 放在同一个选择题里，继续验证面试官关注的是工程边界，而不是背框架名词。
2. **Harness / Runtime 正从抽象概念进入控制边界。** 异步 Tool 的生命周期、Tool Result Schema、Hook 回填 Context、Queue 不丢状态、Context Isolation、Skill Progressive Disclosure 都来自真实追问。
3. **AI Coding 已经变成项目验真的一部分。** 面试官会问真实编码占比、怎样从需求到 Plan / Test、是否共享屏幕看代码、AI 生成代码由谁验证，而不是只问“用没用 Cursor / Claude Code”。
4. **Agent 面试仍然是完整软件工程面试。** Redis、MySQL、线程池、JVM、Webhook 一致性、鉴权、Docker、SSE / WebSocket 与 RAG / Agent 同场出现，没有理由把基础工程从目标岗位知识体系里拆掉。
5. **项目指标必须能被证明。** “20 轮后保留 90% 信息”“PDF 31 分钟优化到 2.5 分钟”都会立刻被追问验证方法、真实数据和本人贡献。
6. **重复与内容化污染继续上升。** 泛搜索更容易命中后发改写、付费专栏和“完整答案”，但精确公司 / 岗位 / 作者页仍能找到新的独立真人场次。

## 饱和判断

**仍未达到来源饱和。** 与 Batch 11 相比，本轮严格 Gate 后新增数量下降到 10，且重复 / 内容账号 / 低质量比例继续升高，这是“开始接近更深水区”的信号；但 2026-09 最新原帖、精确公司岗位搜索和作者时间线仍能稳定产生新的独立 HUMAN-A，因此尚不满足停止条件。

下一条正式来源从 **`S265`** 开始（历史记录；当前基线已由 Batch 13 推进）。
