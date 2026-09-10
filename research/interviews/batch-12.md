# Batch 12 — HUMAN-A 真人高质量第一人称面经

采集日期：2026-09-10

> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。
> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。
> 本批去重后当前保留 **4** 个正式来源。

---

## S205 广州某小厂｜Agent 后端开发｜一面（三阶段）｜发布 2026-06-12｜HUMAN-A

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

## S206 要务科技｜AI 应用开发实习生｜一面｜发布 2026-08-27｜HUMAN-A

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

去重：与 `S207` 虽同公司同岗位，但作者、学校、发布时间、项目和问题链完全不同，确认为不同候选人的独立招聘流程，分别计数。

---

## S207 要务科技｜AI 应用开发实习生｜一面｜面试 2026-09-07，约 46min｜HUMAN-A

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

去重：独特第三方托管 / Webhook / PDF 性能优化项目链及作者时间线未在现有 Batch 出现；与同公司 `S206` 为不同候选人，不合并。

---

## S208 猎豹移动｜Agent 全栈开发｜技术面｜发布 2026-05-13，约 40min｜HUMAN-A

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

去重：URL 和完整 DAG / 循环 RAG / 工作计划 Agent 题序未在 `S001–S006` 命中；未发现同作者同场转载。

---

# 本批清洗与研究观察

本批正式新增：**10 个 HUMAN-A（S045–S208）**。

后续维护补充：Batch 13 搜索中发现 `S027` 同一候选人的 8 月 17 日小红书 Agent 二面，已按同一招聘流程合并回 `S027`；来源总数不因此增加。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## 典型排除

- **拼多多提前批 AI Agent 一面复制链**：`328260668ec94ebda5c84de205d13a58` 与 `d0c1a59663a2408fb9f8b52b87ccaaec` 来自不同账号、发布时间相差约一天，但题序、项目语义和措辞高度一致；无法可靠确认真正原场次，按规则整链排除，不猜原作者。
- **快手 AI 应用 / Agent 开发 9 月内容链**：正文由内容账号持续生产，并出现订阅 / 付费墙、同一叙事多版本扩写；即使问题漂亮也不进入 HUMAN-A。
- **CSDN / Agent 社区学习路线、107 道题、完整答案 / 面试“必杀技”**：属于教学、SEO、题库或二次整理，全部零贡献。
- **只能从搜索摘要 / 聚合页看到标题或片段的跨平台结果**：无法稳定核验候选人本人和原始正文，排除。
- **月之暗面 AI-Native Desktop 三轮题单**：Role Scope 匹配且问题很有价值，但正文缺少足够明确的候选人第一人称现场状态 / 面后结果，本批按保守标准不纳入正式统计。
- **字节 9.3 Agent 开发**：Batch 12 当时因单页现场 / 招聘流程证据不足而暂缓；Batch 13 沿作者主页补齐连续秋招时间线后升级为 HUMAN-A `S076`。这属于补证后升级，不是降低准入门槛。
- **京东 5.8 后端 Agent 等边缘候选**：题目本身有价值，但当前能确认的现场 / 招聘流程证据仍不足，继续不进入 HUMAN-A。

---

## 本批新增信号

1. **“先判断要不要 Agent”已经成为真实能力题。** 腾讯直接把 Prompt / RAG / Fine-tuning / Workflow / Agent 放在同一个选择题里，继续验证面试官关注的是工程边界，而不是背框架名词。
2. **Harness / Runtime 正从抽象概念进入控制边界。** 异步 Tool 的生命周期、Tool Result Schema、Hook 回填 Context、Queue 不丢状态、Context Isolation、Skill Progressive Disclosure 都来自真实追问。
3. **AI Coding 已经变成项目验真的一部分。** 面试官会问真实编码占比、怎样从需求到 Plan / Test、是否共享屏幕看代码、AI 生成代码由谁验证，而不是只问“用没用 Cursor / Claude Code”。
4. **Agent 面试仍然是完整软件工程面试。** Redis、MySQL、线程池、JVM、Webhook 一致性、鉴权、Docker、SSE / WebSocket 与 RAG / Agent 同场出现，没有理由把基础工程从目标岗位知识体系里拆掉。
5. **项目指标必须能被证明。** “20 轮后保留 90% 信息”“PDF 31 分钟优化到 2.5 分钟”都会立刻被追问验证方法、真实数据和本人贡献。
6. **重复与内容化污染继续上升。** 泛搜索更容易命中后发改写、付费专栏和“完整答案”，但精确公司 / 岗位 / 作者页仍能找到新的独立真人场次。

---

## 饱和判断

**仍未达到来源饱和。** 与 Batch 11 相比，本轮严格 Gate 后新增数量下降到 10，且重复 / 内容账号 / 低质量比例继续升高，这是“开始接近更深水区”的信号；但 2026-09 最新原帖、精确公司岗位搜索和作者时间线仍能稳定产生新的独立 HUMAN-A，因此尚不满足停止条件。

下一条正式来源从 **`S047`** 开始（历史记录；当前基线已由 Batch 13 推进）。
