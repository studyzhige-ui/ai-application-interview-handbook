# HUMAN-A Continuous Monitoring Daily Log

本文件是每天三次持续检索的滚动工作日志，不是正式 HUMAN-A 来源库。

用途：记录当天三次检索覆盖、已核验候选、典型排除和平台 / 公司 / Query 盲区，让晚间把三次检索合并为当天一个 Batch，并避免重复劳动。

固定规则：

1. 主动发现只看运行时最近 3 天；
2. 普通线索可以记录为“已排除 / 待追源”，但只有完整通过 HUMAN-A + Role Scope + 全历史去重的候选才进入 `inbox.md`；
3. Morning / Afternoon 不分配 `Sxxx`、不创建 Batch；
4. Evening 完成第三次搜索和最终全库去重后，统一生成当天唯一正式 Batch；
5. 0 正式新增也是合法结果，不允许为凑数降低门槛。

---

## 2026-09-16

### 10:00 Morning Search

- Status: completed
- Discovery window：2026-09-13 ～ 2026-09-16 的最新发布 / 更新。
- Baseline：重新读取 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 Batch，并直接回读 `batch-01.md`～`batch-26.md` 全历史。确认 26 个正式 Batch、`S001–S279` 共 279 个 HUMAN-A、下一编号 `S280`。
- Search effort：至少 **38 组定向 Query**，覆盖字节 / 抖音、阿里 / 淘宝闪购、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米、科大讯飞及中小型 AI Application / Agent 岗位。
- Verification effort：实际尝试打开 / 核验 **20+** 个近期原始候选、作者页或可追源条目；打不开、只停留聚合页、只有摘要或复制链不清的结果不计 HUMAN-A。
- Passed → Inbox：3 个流程：① 美团 AI 后端 `SOLDIER_627` 一面 + 二面；② 科大讯飞 Agent 研发 · Harness 三轮；③ 快手 AI 全栈一面。
- Platform：牛客稳定原帖最多；小红书 / 知乎 / 脉脉 / CSDN / 独立博客没有找到同时满足最近 3 天、稳定原文、第一人称、Role Scope 的非牛客 HUMAN-A。

Morning 主要信号：Skill / Harness 开始进入 Routing Conflict、Context Bloat、Case Replay / Fault Injection；AI Coding 开始追 Production Bad Case 与 Review Bottleneck；Backend / OS Foundation 仍与 Agent 同场。Morning 不改 Canonical / Curriculum。

Morning 待追源：新旦智能、淘宝闪购、望尘科技；快手 9/14 二面 Role Scope 待确认。典型排除包括批量内容账号、AI 自动面试、纯搜推 / 纯推理训练 Infra、普通后端仅顺带问 AI。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：继续只看最近 3 天；优先补 Morning 未充分覆盖的平台、公司和岗位叫法。
- Baseline：再次读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 Batch，并再次直接回读 `batch-01.md`～`batch-26.md` 全历史。当前正式基线仍为 26 Batch / 279 HUMAN-A / 最大 `S279` / 下一 `S280`。
- Search effort：本轮新增至少 **31 组定向 Query**，覆盖 Agent / AI Application / AI Backend / AI Full-stack / AI Native / Harness，以及美团、小红书、字节、智谱、淘宝闪购、快手、百度、腾讯、蚂蚁、京东、滴滴、B站、OPPO / vivo / 小米等，同时专门搜索小红书 / 知乎 / 脉脉 / CSDN / 独立站。
- Verification effort：实际打开、稳定读取或追源 **22+** 个候选原帖 / 作者记录 / 平台聚合入口。
- Passed HUMAN-A → Inbox：4 个新增流程：① 美团 AI Agent；② 美团 AI 后端开发工程师；③ 智谱 AI Native Builder；④ 小红书 AI 应用研发。加上 Morning 3 个，当前 Inbox 共 7 个候选流程。

Afternoon 关键排除 / 待追源：

- 字节 Agent 9/15 `小妞脂`：历史已有同作者 `S076` 字节 Agent 流程，当前不能证明独立 BU / 新招聘流程，暂不收；
- 去哪儿 AI 全栈：AI 自动面试，违反 Human Interviewer Gate；
- 新旦智能 AI 应用：题目强但原始正文持续 Cache Miss；
- 淘宝闪购 AI 一面：聚合内容可读，但稳定原帖 / 作者链未闭环；
- 望尘科技 AI 全栈：原帖直链未稳定定位；
- 快手 9/14 二面：正文抓取 / Role Scope 证据不足；
- PDD 批量面经链：内容账号 / 合集风险；
- 北京网梯：AI 自动面试；
- 字节 AI Infra：岗位主体为 GPU / MPI / Profiling / Serving Infra，Role Scope 外；
- 旧日期 Ctrip 等结果：超出本轮最近 3 天发现窗口。

Afternoon 新信号：Agent Reliability 从抽象“防幻觉”变成确定性 Gate；Evaluation 参数开始被验真；Agent Security / Data Governance 进入应用面试；AI Application 仍要求 System Design / Failure Recovery；Skill / Claude Code 进入项目验真。Afternoon 不新增 Canonical、不修改 Curriculum。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：继续限定最近 3 天。
- Baseline / full-history dedup：重新读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 Batch，并再次**逐个直接回读 `batch-01.md`～`batch-26.md` 全历史**。确认正式基线仍为 26 Batch / `S001–S279` / 279 HUMAN-A / 下一 `S280` 后才执行最终编号。
- Search effort：第三轮完成 **50+ 组定向 Query 变体**，重点补蚂蚁、淘宝闪购、百度、腾讯、京东、滴滴、B站、OPPO / vivo / 小米、Coding Agent / Harness / AI Native 等盲区，并复查 Afternoon 的待追源线索。
- Verification effort：第三轮继续尝试打开 / 回读 / 追作者或企业页 **20+** 个近期候选与 provenance 入口；最近 3 天高质量供给不足时不使用旧内容或低质量页面补数。
- New HUMAN-A after Evening search：**0 个**。晚间没有发现比当前 Inbox 7 个流程更可靠、且同时满足稳定原帖 / 作者 / Role Scope / 全历史去重的新来源。
- Final dedup：Morning + Afternoon 的 7 个 Inbox 候选全部再次通过最终 Gate；没有发现与 `S001–S279` 同场重复。
- Final Batch：创建 `batch-27.md`，统一分配 `S280–S286`。

Evening 重点复核：

1. **蚂蚁 9/15 高密度 Agent / AI Native 线索**：企业聚合入口能看到 Write-risk、Long-task Harness、Hooks / Plugins、Agent Eval 等连续追问，但原始正文直接回读仍不稳定；保留为待追源线索，零贡献。
2. **蚂蚁 9/14 `AIGC小白入门记`**：原帖技术题丰富，但作者属于历史已经明确排除的批量内容账号链；技术密度不能覆盖 provenance 缺陷，零贡献。
3. **淘宝闪购 9/14 AI 一面**：聚合入口与作者求职状态可提供旁证，但仍未形成“稳定原帖直链 + 作者正文”的完整证据链；不升级 HUMAN-A。
4. **新旦智能 / 望尘科技**：继续因 Cache Miss / 原帖直链不稳定而排除。
5. **字节 `小妞脂` 9/15**：历史 `S076` 已确认同作者字节 Agent 9/3 流程；未找到独立 BU / 新流程证据，继续不新增。
6. **PDD Agent 批量页面**：近期搜索出现多份“面经 01/02/03...”并夹标准答案 / SQL / 代码，属于整理 / 内容链风险，零贡献。
7. **招聘 JD / 内推 / 题库 / 新闻**：只用于理解岗位市场或追原帖，不贡献 HUMAN-A。

### Final Summary

- Three-round search effort：**至少 119 组 Query 变体**（Morning ≥38 + Afternoon ≥31 + Evening ≥50）。
- Three-round verification effort：**至少 62 次候选页 / 作者页 / provenance 入口打开或追源尝试**（Morning 20+ + Afternoon 22+ + Evening 20+；这是工作量次数，不等于 62 个唯一 URL）。
- Final additions：**7 个 HUMAN-A，`S280–S286`**。
- Current formal library：**27 Batch / 286 HUMAN-A / `S001–S286`**。
- Next ID：**`S287`**。
- Inbox：归档后清空。
- Canonical / Curriculum：**本日不修改**；`S280–S286` 进入后续 periodic mapping / review。

当日主要市场信号：

1. Skill / Harness 开始稳定进入 Routing Conflict、Context Bloat、Case Replay / Fault Injection、Loop Stop 与 Production Gate；
2. Reliability 从“降低幻觉”转向确定性约束、用户二次确认、权限与可恢复执行；
3. Evaluation 追问已经进入 Test Set、Elo、阈值、Case 代表性和参数依据；
4. Agent Security / Sensitive-data Exfiltration 开始直接出现；
5. AI Coding 从工具使用转向 Bad Case、Review Throughput、Testing 与 Production Verification；
6. MySQL / Redis / OS / Concurrency / System Design 继续与 Agent / RAG 同场，Foundation 不能被弱化。

饱和度 / 盲区：最近 3 天牛客仍是最容易稳定核验的公开原帖来源；小红书 / 知乎 / 脉脉 / CSDN / 独立站，以及百度 / 腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等公司，在当前 3 天窗口内的目标岗位高质量第一人称可核验供给偏少。最新热门结果层已经出现明显局部饱和：历史命中、内容账号、AI 自动面试、Role Scope 模糊、聚合页和原帖失效占比较高。因此下一轮继续重点做跨平台与作者 Timeline 补盲，但不降低 Gate。

---

## 2026-09-17

### 10:00 Morning Search

- Status: completed
- Discovery window：2026-09-14 ～ 2026-09-17 的最新发布 / 更新。
- Baseline：重新读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy 和最新 `batch-27.md`；随后逐个直接回读 `batch-01.md`～`batch-27.md` 全历史。确认当前正式基线为 **27 Batch / 286 HUMAN-A / `S001–S286` / 下一 `S287`**，Inbox 在本轮开始时为空。
- Search effort：至少 **97 组 Query 变体**。除目标岗位通用词外，逐公司覆盖字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，并补 `AI Application`、`AI Backend`、`AI Full-stack`、`Coding Agent`、`Harness`、`AI Native`、`大模型应用开发`、`智能体开发` 等岗位别名；另外单独搜索小红书 / 知乎 / 脉脉 / CSDN / 独立站等非牛客来源。
- Verification effort：显式执行 **20 次以上**近期候选页 / 作者页 / provenance 入口打开核验；其中部分牛客原始直链仍出现 Cache Miss / Timeout，因此只把能稳定取得正文和招聘上下文的页面用于准入判断，不以搜索摘要代替原帖。
- Passed HUMAN-A → Inbox：**0 个**。本轮没有发现同时满足“最近 3 天 + 第一人称真人面试 + 高技术密度 + 目标 Role Scope + 稳定正文 + 全历史去重”的新流程，因此 Inbox 继续为空；不分配 `Sxxx`、不创建 Batch。

Morning 重点排除 / 观察：

1. **小米 9/15 后端二面**：候选人本人第一人称，Agent / MCP / Harness / Skill / Multi-Agent / Evaluation 追问密集，现场痕迹也足，但页面只明确为普通“后端”二面，无法证明岗位 / 团队主体属于 AI Application / Agent；按 Role Scope Gate 排除，不因为 AI 问题多就纳入。
2. **小米 9/16 测开一面**：原帖稳定、真人现场明确，也问到 AI 使用问题与“Skill 能否保证安全”，但岗位主体是测试开发，属于 Role Scope 外；零贡献。
3. **百度网盘近期后端二面**：出现多模态模型 / Spring AI Alibaba / Agent 项目追问，但岗位仍是普通后端，当前证据不足以证明 AI Application / Agent 为团队职责主体；按同一 Gate 排除。
4. **百度 9/16 `agent面试`**：只是候选人询问“有没有人面过、有没有手撕”，不是本人已发生的面试复盘，不满足 HUMAN-A。
5. **近期聚合 / 合集 / 答案化页面**：仍大量出现“XX 公司 Agent 面经 01/02/03”“面 20 家 Agent 岗真题整理”“面试路线 / 必考题”等内容；即使题目很新也属于合集、教学或内容账号，零贡献。
6. **招聘 JD / 人才报告 / 技术趋势文章**：可作为市场旁证，但不贡献 HUMAN-A。近期公开岗位仍能看到 Agent Runtime / Context / Memory / Tool / Safety / Observability 等职责，但研究库只统计真实候选人面试现场。
7. **非牛客平台**：本轮专门补小红书、知乎、脉脉、博客 / 技术社区检索，仍未找到最近 3 天内同时满足稳定原文、第一人称招聘现场和目标 Role Scope 的可核验新 HUMAN-A。

Morning 主要信号：**Agent / Harness / Skill 正在明显向普通后端、测开等非目标岗位扩散**。这说明“面试里出现 Agent 名词”越来越不能作为 Role Scope 的替代证据，反而需要更严格地区分“目标 AI Application / Agent 岗”与“普通岗位开始要求 AI 素养”。这一现象只作为市场观察，不进入目标岗位频率统计，也不触发 Canonical / Curriculum 修改。

Morning 盲区：最近 3 天的目标岗位高质量第一人称原帖供给偏少，百度 / 腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等公司仍缺新的可核验目标岗样本；非牛客平台的稳定正文与作者 provenance 仍是主要约束。17:00 应重点补这些公司与平台，并继续追 9/16～9/17 新发布结果，而不是重复上午同一组关键词。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 3 天滚动窗口；重点补 2026-09-15 ～ 09-17 新发布，9/14 只保留仍在 72 小时窗口内的晚间来源。
- Baseline：再次读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 `batch-27.md`，并逐个直接回读 `batch-01.md`～`batch-27.md` 全历史。确认正式基线仍为 **27 Batch / 286 HUMAN-A / `S001–S286` / 下一 `S287`**。
- Search effort：本轮新增至少 **60 组定向 Query / Query 变体**，重点补 Morning 的百度 / 腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等盲区，同时继续覆盖字节、阿里系、蚂蚁、小红书、快手、美团及 `AI Application` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `RAG` 等岗位别名，并追牛客作者 / 企业页及非牛客可核验来源。
- Verification effort：显式打开 / 回读 / 追源 **20+** 个近期候选原帖、作者页、企业页或 provenance 入口。
- Passed HUMAN-A → Inbox：**1 个新流程：字节 Agent 秋招一面（作者 `吃饱了撑的容器`，2026-09-16 15:09）**。当前 Inbox 共 1 个候选；不分配 `Sxxx`、不创建 Batch。

Afternoon 通过项：

1. **字节 Agent 秋招一面**：稳定原帖直接可读；候选人明确写“当天下午已约二面”，页面身份为“小红书 Agent 开发（实习员工）”。连续追问覆盖滑动窗口 / 摘要压缩 Memory、文档在线更新并发幂等、RocketMQ 在更新链路的位置及 MQ vs 定时任务、DeepSeek Harness / Pi Agent、Computer Use 本地 / 云端机制、Claude Code Context Compression、AI Coding 完整工作流，再落到 MySQL B+ Tree 与两道 Coding。已直接回读全历史确认没有同场 URL / 作者 / 连续题序重复；搜索 0 命中仅作辅助。

Afternoon 重点排除 / 待追源：

1. **去哪儿旅行 9/16 AI 应用开发（全栈）**：候选人本人、46 分钟真人技术面、Role Scope 清楚且作者主页稳定，但公开可稳定读取的正文主要是流程级摘要；具体“6 道真题”没有形成可稳定文本证据，当前技术密度不够 HUMAN-A Gate，暂不进 Inbox。
2. **蚂蚁 9/14 AI Agent 开发**：原帖稳定且题目很强，但作者为 `AIGC小白入门记`，属于历史已经识别并排除的批量内容账号链；继续零贡献。
3. **淘宝闪购 9/14 AI 一面**：本轮终于定位到可稳定检索的原帖与作者 `JeffreyLove`，但发布时间 9/14 13:04，在 17:00 运行时已超出严格 72 小时发现窗口；不因后来补齐 provenance 越过时间 Gate。
4. **小红书 PE / 产品工程师（全栈）二面**：Agent / Coding Agent 技术密度高，但当前岗位证据仍无法证明 AI Application / Agent 是职位主体，Role Scope 模糊，暂不收。
5. **小红书 Agentic 端侧推理优化**：岗位主体为端侧模型推理、量化 / 压缩 / MLSys，默认属于应用层 Role Scope 外。
6. **滴滴 9/16 大模型开发（NiceOffer）**：二次整理页信息充分，但暂无候选人原始第一人称来源，不能用整理站替代 HUMAN-A provenance。
7. **普通后端 / 测开近期 Agent 深挖**：继续按 Morning 同一规则排除；“问了 Agent”不等于目标 Agent 岗。

Afternoon 主要信号：**前沿 Agent 名词正在从“定义题”进入集成验真**。本轮新增候选不是单独问 Harness / Computer Use，而是继续追“是否值得替换当前方案、怎样与现有 Agent 集成、文档并发更新如何幂等、MQ 为什么放在这个位置、AI Coding 工作流是否足够 AI Native”。同时数据库与算法照常同场出现，说明目标 Agent 岗仍然要求把前沿能力落回 Production Engineering。该信号只记 Market Observation，不新增 Canonical、不修改 Curriculum。

Afternoon 盲区：百度 / 腾讯 / 京东 / B站 / OPPO / vivo 在最近 3 天仍缺可稳定核验的目标岗第一人称高密度样本；非牛客平台仍以摘要 / 聚合 / 登录墙为主。22:00 应继续补这些盲区，并重新回读全历史后再对当前 Inbox 做最终去重。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：严格限定运行时最近 3 天 / 72 小时；继续补 Afternoon 的公司、平台和岗位别名盲区。
- Baseline / full-history dedup：重新读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy 与最新 `batch-27.md`；随后再次**逐个直接回读 `batch-01.md`～`batch-27.md` 全历史**。确认正式基线为 **27 Batch / 286 HUMAN-A / `S001–S286` / 下一 `S287`** 后才执行最终编号。
- Search effort：第三轮新增 **60+ 组定向 Query / 变体**，继续覆盖字节 / 抖音、阿里 / 千问 / 淘宝、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，并补 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Computer Use` 等组合及非牛客来源。
- Verification effort：第三轮显式打开、回读或追源 **20+** 个近期原帖、作者页、企业聚合入口或 provenance 线索；不使用旧面经或低质量页面补数量。
- New HUMAN-A after Evening search：**0 个**。第三轮没有发现新的、同时满足最近 72 小时、稳定原帖、候选人第一人称、目标 Role Scope、高技术密度和全历史去重的独立流程。
- Final dedup：Afternoon Inbox 的字节 Agent 候选再次通过最终 Gate；未发现与 `S001–S286` 同场重复。
- Final Batch：创建 `batch-28.md`，统一分配 **`S287`**。

Evening 重点复核：

1. **千问技术部 9/16 一面**：真人第一人称和技术密度很高，出现 Agent Plan / Replan、Context、Tool Calling、Reconnect、Evaluation、Regression 等连续追问；但岗位主体无法稳定确认属于本库目标 AI Application / Agent Role Scope，不因为题目高级扩大范围。
2. **小红书 Agentic 端侧推理优化 9/14**：正文稳定且第一人称，但后半技术主体明显转入端侧模型推理、量化 / 压缩、蒸馏 / SFT 等 Model / Training / Inference Optimization 边界，按 Role Scope 保守排除。
3. **京东 AI Agent 9/14**：题序高度相关，但作者为历史已识别的 `AIGC小白入门记` 内容账号链；继续零贡献。
4. **去哪儿旅行 9/16 AI 应用开发（全栈）**：Role Scope 与招聘现场成立，但公开可稳定读取的正文仍只有流程级摘要，技术问题细节不足 A-grade Gate；不为数量降低标准。
5. **百度网络研发 / B站测开等近期 Agent 深挖**：出现 LangGraph、OpenClaw、Skill / MCP / Evaluation 等，但岗位主体是网络研发 / 测试开发，Role Scope 外。
6. **聚合页 / 二次整理 / 标准答案 / JD / 内推 / 新闻 / Search Snippet**：只用于发现与旁证，不贡献 HUMAN-A。

### Final Summary

- Three-round search effort：**至少 217 组 Query / Query 变体**（Morning ≥97 + Afternoon ≥60 + Evening ≥60）。
- Three-round verification effort：**至少 60 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试；这是工作量次数，不代表 60 个唯一 URL。
- Final additions：**1 个 HUMAN-A，`S287`**。
- Current formal library：**28 Batch / 287 HUMAN-A / `S001–S287`**。
- Next ID：**`S288`**。
- Inbox：归档后清空。
- Canonical / Curriculum：**本日不修改**；`S287` 进入后续 periodic mapping / review。

当日主要市场信号：

1. Harness 已从定义题进入“是否值得替换现有架构、怎样迁移”的工程判断；
2. Context / Memory 继续向窗口大小、切换条件、Compression Mechanism 等可验证细节下沉；
3. Agent Backend 与并发幂等、MQ 位置、在线更新可靠性继续合流；
4. Computer Use 的本地 / 云端执行机制开始进入真实目标岗位面试；
5. AI Coding 越来越要求说明完整研发 Workflow 与是否真正 AI Native，而不只是工具清单；
6. MySQL / Coding 等 Foundation 继续与最新 Agent 能力同场，不能弱化。

饱和度 / 盲区：当前最近 3 天公开热门结果层仍呈**局部饱和 + 高 provenance 成本**：内容账号、聚合页、Role Scope 模糊、普通岗位 Agent 深挖与正文不可稳定回读占比较高。牛客仍是最容易稳定核验的公开原帖来源；百度 / 腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等目标公司及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，当前窗口内仍缺新的高质量可核验目标岗第一人称样本。下一轮继续补这些盲区与作者 Timeline，但不降低 HUMAN-A Gate。

---

## 2026-09-18

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-15 10:00 ～ 2026-09-18 10:00**；只把窗口内新发布 / 更新作为主动发现对象，历史页面仅用于去重与追源。
- Baseline：重新读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy 和最新 `batch-28.md`；随后再次逐个直接回读 `batch-01.md`～`batch-28.md` 全历史。确认当前正式基线为 **28 Batch / 287 HUMAN-A / `S001–S287` / 下一 `S288`**，本轮开始时 Inbox 为空。
- Search effort：至少 **60 组定向 Query / Query 变体**，继续覆盖字节 / 抖音、阿里 / 千问 / 淘宝、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，并补携程、去哪儿、顺丰、米哈游等近期结果；岗位别名覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `RAG` / `大模型应用开发` / `智能体开发`，同时搜索牛客、小红书、知乎、脉脉及可追源公开页面。
- Verification effort：实际打开、稳定读取或追源 **20+ 次**近期候选原帖、作者页、企业面经页、聚合入口或 provenance 线索。最近 72 小时目标岗原创供给不足，没有用旧面经、JD 或低质量页面补 HUMAN-A 数量。
- Passed HUMAN-A → Inbox：**0 个**。本轮没有找到新的、同时满足真人面试官 + 候选人第一人称 + 高技术密度 + 目标 Role Scope + 稳定原文 + 全历史去重的独立流程；Inbox 继续为空，不分配 `Sxxx`，不创建 Batch。

Morning 重点复核 / 排除：

1. **去哪儿旅行 9/16 AI 应用开发工程师（全栈）**：作者 `Harry00` 的个人主页和招聘现场都稳定可核验，46 分钟真人技术面、Role Scope 也清楚；但当前公开稳定正文依旧主要是流程级摘要与工程方向描述，具体技术题只通过平台“查看真题”入口存在，正文没有形成足够高密度、可直接核验的连续题序，因此继续不升级 HUMAN-A。
2. **携程 9/15–9/16 AI Agent 开发**：近期聚合页能连续发现多个 `携程 AI Agent开发一面` 条目，但本轮仍未稳定定位到候选人本人原始正文与作者 Timeline；二次聚合只能作为 Recall 线索，不能替代 HUMAN-A provenance。
3. **字节近期 Agent 深挖线索**：出现“Harness 怎么做、Tool 超时、Context 爆掉、Agent 中途重启恢复”等高价值追问的推荐片段，但完整原帖 / 作者页未能稳定回读，且可见连续问题数量不足 A-grade Gate；零贡献。
4. **百度 9/17 后端一面**：候选人本人、问题具体，确实追到 AI 应用服务平台、会话管理、Agent 是否参与、Workflow vs Agent；但岗位明确为普通后端，当前没有证据证明团队 / 招聘主体属于 AI Application / Agent，按 Role Scope 排除。该条进一步说明普通 Backend 正在吸收 Agent 素养，但不能污染目标岗位频率。
5. **小米 9/15 后端二面等旧候选**：继续只能证明普通后端 / 测开岗位问了 Agent / MCP / Skill，而不能证明目标 Role Scope；不因连续多天反复出现而升级。
6. **FaceTomato / NiceOffer / “面经-01/02/03” / 批量标准答案链**：近期确实能发现携程、顺丰、米哈游等 AI Application / Agent 标题，但属于二次整理、聚合或系列内容风险；没有原帖 provenance 就保持零贡献。
7. **招聘 JD / 企业职位页**：快手 AI 应用开发 / AI 全栈、阿里云 AI Agent 开发、字节 AI 应用后端等当前岗位页面仍明确强调 Agent 工程、Bad Case / Evaluation、线上稳定性、AI Coding 与模型 + 系统结合，但这些只作为市场旁证，不贡献 HUMAN-A。

Morning 主要观察：**最近 72 小时公开结果层的瓶颈已经从“有没有 Agent 内容”进一步转成“有没有稳定、候选人本人、目标岗原帖”**。二次聚合与普通 Backend 的 Agent 深挖越来越多，因此 provenance + Role Scope Gate 的价值继续上升。与此同时，当前目标岗 JD 继续把 AI Coding、Bad Case / Evaluation、P99 / SLO、灰度回滚与 Agent 系统放在同一工程职责中，和既有 HUMAN-A 中“Production Engineering + Agent”的趋势一致；但 JD 只作旁证，不直接改变 Canonical / Curriculum。

Morning 盲区：优先继续追 **携程 9/15–9/16 Agent、顺丰科技 9/15 AI 应用、米哈游 9/15 Agent 方向** 的候选人原帖与作者 Timeline；百度 / 腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 在当前窗口仍缺新的目标岗高密度第一人称原帖；小红书 / 知乎 / 脉脉等非牛客来源仍受登录墙、摘要和转载链约束。17:00 应以这些 provenance 缺口为主，而不是机械重复上午关键词。

Morning 不新增 Canonical，不修改 Curriculum。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时滚动，约为 **2026-09-15 17:08 ～ 2026-09-18 17:08**；主动发现只使用该窗口内新发布 / 更新，历史页面只做 provenance 与全库去重。
- Baseline：再次读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy 与最新 `batch-28.md`；并再次逐个直接回读 `batch-01.md`～`batch-28.md` 全历史。确认正式基线仍为 **28 Batch / 287 HUMAN-A / `S001–S287` / 最大 `S287` / 下一 `S288`**。本轮运行中 `main` 已因 Python 教材维护前进到新的提交，但 Research 监测文件与上午结果保持完整，没有覆盖并发更新。
- Search effort：本轮新增至少 **85 组定向 Query / Query 变体**，重点补 Morning 的携程 / 顺丰 / 米哈游 provenance 缺口，以及腾讯、京东、滴滴、B站、OPPO / vivo / 小米、百度、快手等公司；同时继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `AI Native` / `Coding Agent` / `Harness` / `Runtime` / `RAG` / `大模型应用开发` 等岗位别名，并复查牛客企业页、作者 Timeline 与可核验公开来源。
- Verification effort：显式打开、回读或追源 **25+ 次**近期候选原帖、作者页、企业页、职位页或 provenance 入口；其中若干直接原帖出现 Cache Miss，因此不以企业页片段或 Search Snippet 替代稳定原文。
- Passed HUMAN-A → Inbox：**1 个新流程：蚂蚁一面（作者 `Decadeqqq`，面试日期 2026-09-15，原帖发布 2026-09-17 21:17）**。当前 Inbox 共 1 个候选；Afternoon 不分配 `Sxxx`、不创建 Batch。

Afternoon 通过项：

1. **蚂蚁｜AI Native / Agent 应用方向（实际面试内容明确）｜一面**：原帖现在可以稳定直接回读，作者以“发面经攒人品、被问穿了”记录本人现场，正文为连续 24 个问题而不是标准答案包装。问题从“为什么引入 Agent、写操作风险、Agent 接管整个写链路”继续追到 Long-task 管理、Harness vs Backend API、开源 Agent Framework 定制、Claude Hooks / Plugins / Extensions 与改内核的 Trade-off、AI Native 平台 API、Zod / 参数校验与业务语义错误、Agent Evaluation、Gate Metric、Review Agent 与 Hallucination。作者主页还能连续核验 9/8、9/10 Shopee、9/12 得物、PDD、字节等本人求职记录，个人候选人 Timeline 成立。岗位正式名称没有稳定公开，因此不猜 BU / Title；但整场技术主体明显属于本库允许的 AI Application / Agent Role Scope。
2. **全历史去重**：在分配 Inbox 前已直接回读 `batch-01.md`～`batch-28.md`；未发现当前 URL、作者 `Decadeqqq`，也未发现“Agent 写链路风险 → Harness / Backend 双视角长任务 → Framework Kernel vs Hooks / Plugins → AI Native API / Zod / 业务错误 → Eval Gate / Review Agent”的 5–10+ 连续独特题序同场来源。GitHub Search 对 URL / 作者的 0 命中只作辅助，不作为未收录证明。

Afternoon 重点排除 / 待追源：

1. **快手 9/17 AI 应用开发一面 / 二面**：快手企业面经页可看到两条同一时间段的高密度 Agent 结果，包含多轮审查 Memory、长任务崩溃恢复、并发修改会话记忆等；但两个直接原帖当前均 Cache Miss，企业页片段又带明显解释 / 答案式展开，无法稳定确认候选人原始正文与作者 Timeline。继续待追源，不进 Inbox。
2. **PDD 9/15 AI Agent 面经 `林小白zii`**：页面按“面经 01 / 02 / 03”批量合并多场，并给出大量标准化展开题序；属于合集 / 内容链风险，不满足候选人本人单一招聘流程 provenance，零贡献。
3. **B站 Agent 结果**：近期能搜到 `AIGC小白入门记` 的 AI 应用 / Agent 页面，但该账号已属历史明确排除的批量内容链，且当前页面日期不在本轮最近 72 小时内；不升级。
4. **滴滴 9/17 网约车技术部日常实习**：原帖是真人、场景设计密度高，但目前可核验内容属于普通工程 / 场景设计，没有证据证明招聘主体是 AI Application / Agent；按 Role Scope 排除。
5. **百度 9/17 普通后端、快手普通 Java / 前端、B站测开等**：即使出现 Agent、AI Coding、SSE、Tool Call、Evaluation，也不能用候选人项目里的 AI 内容替代岗位 Role Scope，继续零贡献。
6. **JD / 企业页 / 聚合 / NiceOffer / 标准答案页**：只用来发现原帖或理解市场，不贡献 HUMAN-A。非牛客平台本轮仍没有找到能同时满足稳定原文、候选人第一人称、目标岗和最近 72 小时的新来源。

Afternoon 主要观察：**目标 Agent 面试正在把“模型会不会做”进一步压到“副作用与平台契约能否被确定性治理”**。本轮蚂蚁候选连续追写操作风险、Long-task Harness、Framework Kernel vs Extension、AI Native API、参数 / 业务语义错误、Eval Gate 与 Review Agent，说明平台级 Agent Engineering 已把 Safety / Side Effect、API Contract、Validation、Evaluation Gate 和 Framework Extensibility 放在同一条项目验真链上。这个信号目前只来自单日新增证据，先作为 Market Observation；不新增 Canonical、不修改 Curriculum。

Afternoon 盲区：22:00 应优先再次追快手 9/17 AI 应用一 / 二面的稳定原帖与作者 Timeline，并继续补携程 / 顺丰 / 米哈游以及腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 的目标岗原始第一人称来源；同时对当前蚂蚁 Inbox 候选重新执行最终全历史去重后再决定是否分配 `S288`。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-15 22:00 ～ 2026-09-18 22:00**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline 与全库去重。
- Baseline / full-history dedup：重新读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy 和最新 `batch-28.md`；随后再次**逐个直接回读 `batch-01.md`～`batch-28.md` 全历史**。确认正式基线为 **28 Batch / 287 HUMAN-A / `S001–S287` / 下一 `S288`** 后才执行最终编号。`main` 在 Afternoon 后由 Coding & Problem Solving 更新前进，晚间以最新 HEAD 为父提交，保留并发教材改动。
- Search effort：第三轮完成至少 **100 组定向 Query / Query 变体**，重点补快手 9/17 AI 应用一 / 二面、携程 / 顺丰 / 米哈游、腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米 / 百度，以及 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `AI Native` / `Coding Agent` / `Harness` / `Runtime` / `RAG` 等岗位别名，并继续追作者 Timeline 和原始正文。
- Verification effort：第三轮实际打开、回读或追源 **25+ 次**近期候选原帖、作者页、企业面经页、职位页或 provenance 入口；搜索摘要、JD、聚合页、笔试和打不开的原帖不替代 HUMAN-A 原始证据。
- New HUMAN-A after Evening search：**0 个**。第三轮没有发现新的、同时满足最近 72 小时 + 真人面试官 + 候选人第一人称 + 高技术密度 + 目标 Role Scope + 稳定原文 + 全历史去重的独立流程。
- Final dedup：Afternoon Inbox 的蚂蚁候选重新直接与 `S001–S287` 全历史核对，再次通过最终 Gate；未发现同 URL、同作者、同流程或 5–10+ 连续独特题序的历史重复。
- Final Batch：创建 `batch-29.md`，将当前唯一通过者分配为 **`S288`**。

Evening 重点复核：

1. **蚂蚁 9/15 一面｜`Decadeqqq`**：稳定原帖保持可直接回读，24 个连续问题和“发面经攒人品 / 被问穿了”现场痕迹完整；作者 Timeline 可继续串起 Shopee、得物、PDD 等本人求职记录。写操作风险 → 完整写链路 → Long-task Harness / Backend API → Framework Kernel vs Hooks / Plugins / Extensions → AI Native API / Zod / 业务语义错误 → Eval Gate / Review Agent 的连续题序仍未在历史库出现。最终归档 `S288`。
2. **千问技术部 9/16 一面｜同作者 `Decadeqqq`**：原帖稳定、1h15min、Plan / Replan、Tool Calling、Context、Reconnect、Evaluation、Review Agent 等技术密度很高；但本仓库前一日已因岗位主体无法稳定确认属于 AI Application / Agent Role Scope 而排除。晚间未获得新的职位 / 招聘主体证据，因此维持原判断，不因同作者已有合格蚂蚁流程而顺带放行。
3. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：搜索结果与作者主页能确认当天确有 `agent开发` 面试和个人求职 Timeline，但当前稳定入口只暴露前几道问题及“14 道真题”提示，直接原帖详情仍无法稳定回读，无法完整核验 A-grade 技术链；保留为后续 provenance / 正文补齐线索，零贡献。
4. **快手 9/17 AI 应用一 / 二面**：继续没有补到稳定可直接回读的候选人原帖；企业页 / 搜索片段不能替代原始正文，零贡献。
5. **水滴 9/17 AI 全栈**：当前可核验的是笔试，不是 Human Interviewer，排除。
6. **百度 9/17 后端一面**：真人第一人称且问到 AI 应用平台、Agent 与 Workflow，但岗位主体仍是普通后端，Role Scope 排除。
7. **JD / 企业页 / 聚合 / 题库 / 面经索引 / 标准答案页**：只作为市场旁证或 Recall，不贡献 HUMAN-A。

### Final Summary

- Three-round search effort：**至少 245 组 Query / Query 变体**（Morning ≥60 + Afternoon ≥85 + Evening ≥100）。
- Three-round verification effort：**至少 70 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试；这是工作量次数，不代表 70 个唯一 URL。
- Final additions：**1 个 HUMAN-A，`S288`**。
- Current formal library：**29 Batch / 288 HUMAN-A / `S001–S288`**。
- Next ID：**`S289`**。
- Inbox：归档后清空。
- Canonical / Curriculum：**本日不修改**；`S288` 进入后续 periodic mapping / review。

当日主要市场信号：

1. Agent 安全正在从“输出会不会幻觉”继续下沉到**有副作用写操作、权限、Tool / API Contract 与业务语义 Validation**；
2. Long-task / Harness 不只考 Loop，而开始与 Backend API、恢复、扩展机制和 Framework Kernel Trade-off 联动；
3. Eval 从“做过评测”进入 Gate / Metric / Review Agent 可靠性；
4. Agent / Skill / AI Coding 已明显向普通 Backend、Data、Test 岗扩散，因此 Role Scope Gate 必须比过去更严格；
5. Foundation / Production Engineering 仍是最新 Agent 能力的承载层，不能被新名词替代。

饱和度 / 盲区：最近 72 小时公开热门层继续表现为**局部饱和 + provenance 成本高**。牛客仍最容易拿到可核验原帖，但新结果大量落在笔试、聚合、内容账号、普通岗位 AI 项目追问或原帖不可稳定回读；腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等目标公司以及小红书 / 知乎 / 脉脉 / 独立博客，在严格 Gate 下仍缺新的目标岗高密度第一人称样本。下一轮继续追 4399 9/18 Agent、快手 9/17 AI 应用一 / 二面及跨平台作者源，不降低 Gate。

---

## 2026-09-19

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-16 10:07 ～ 2026-09-19 10:07**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline 与去重参考。
- Baseline：重新读取当前 `main`、Market README、Inbox、Daily Log、两份 Market Policy 和最新 `batch-29.md`。确认当前正式基线为 **29 Batch / 288 HUMAN-A / `S001–S288` / 下一 `S289`**，本轮开始时 Inbox 为空。由于本轮没有候选进入 Inbox、也不分配 ID，因此没有触发“入 Inbox / 分配 ID 前”的全历史 Batch 回读；若 Afternoon 出现达到准入的候选，必须先直接回读 `batch-01.md`～`batch-29.md` 再写入 Inbox。
- Search effort：至少 **90 组定向 Query / Query 变体**。逐公司覆盖字节 / 抖音、阿里 / 千问 / 淘宝、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，并继续补 4399、阳光电源、携程、去哪儿、米哈游、顺丰等近期线索；岗位别名覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `AI Native` / `Coding Agent` / `Harness` / `Runtime` / `RAG` / `大模型应用开发` / `智能体开发`。另外单独搜索小红书、知乎、脉脉、CSDN、博客园、掘金、Bilibili 等非牛客公开来源。
- Verification effort：显式打开、回读或追源 **20+ 次**近期候选原帖、作者页、企业页、职位页或 provenance 入口；Search Snippet、JD、聚合页、课程 / 面经宝典和打不开的原帖均不替代 HUMAN-A 原始证据。
- Passed HUMAN-A → Inbox：**0 个**。本轮没有新的流程同时满足真人面试官 + 候选人第一人称 + 高技术密度 + 目标 Role Scope + 稳定原始正文 / URL + 全历史去重；Inbox 继续为空，不分配 `Sxxx`，不创建 Batch。

Morning 重点复核 / 待追源：

1. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：相比昨晚有实质进展——最新作者索引已能完整暴露 14 道连续问题，包含“如何判断自己真正掌握而不是依赖 AI 工具”、10 万级日志如何处理、Harness 架构、Agent 场景与效果、Agent 生成 SQL 的错误检测、项目 90% 测试用例通过率如何统计 / 失败原因、从数据开发转 AI 的能力缺口，以及反问中面试官说明团队是约 20+ 人的内部业务 AI 研发团队、独立构建内部 AI Agent。技术密度、真人互动、Role Scope 和作者个人求职 Timeline 都很强；但**仍未稳定解析 / 打开这篇面经的 post-specific 原帖详情 URL**，普通作者页直读还是旧快照，没有可靠地包含该新帖。按照 Verifiable Gate，搜索索引里的完整正文仍不能替代稳定原始详情页，因此 Morning 继续不进 Inbox。Afternoon 优先追该帖 direct detail / 可稳定作者正文。
2. **阳光电源 AI 应用开发工程师一面｜面试 9/18 10:00｜`小红不是绿`**：最新企业 / 索引结果可见 10 个连续问题，包含线上支付失败全链路诊断、RAG 召回低的原因与改进、PDF 表格 / 图片解析、MPC / Function Calling 区别、客户端实习与 AI 应用 / 后端职业选择、局部组件 vs 端到端参与等；目标岗位和真人现场都很清楚。但 direct detail 当前仍 Cache Miss，企业页直读也存在索引 / 快照不一致，未形成稳定原始正文闭环；继续待追源，不进 Inbox。
3. **去哪儿旅行 9/16 AI 应用开发（全栈）**：可稳定读取的仍是 46 分钟真人面试流程摘要，Role Scope 清楚，但具体技术问题链没有形成可直接核验的高密度正文；维持既有排除。
4. **普通 Data / Backend / Test 岗 AI 深挖**：`AAA野生原子弹批发` 同期海信大数据开发面试也会问 AI 平台、AI 能做什么、未来规划，但岗位主体仍是数据开发；水滴近期 AI 测试结果是笔试。继续按 Role Scope / Human Interviewer Gate 排除，不能因为 Agent / AI 话题扩散就污染目标岗位统计。
5. **非牛客平台补盲**：小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客园 / Bilibili 当前窗口主要返回课程、面试宝典、标准答案、旧复盘或 AI 新闻，未找到新的、稳定可核验的目标岗位第一人称 HUMAN-A。
6. **招聘 JD / 企业职位页**：近期快手 AI 应用、小米 Agent / 智能风控、中国电子云 AI Coding 等岗位继续强调 Context / Tool / Multi-Agent、权限与审计、Agent Loop、代码检索 / Evaluation 等，只作为市场旁证，不贡献 HUMAN-A。

Morning 主要观察：**“Harness + AI 开发真实性验证”开始出现在目标 Agent 面试的同一条追问链里**。4399 线索不只问 Harness，还追“AI 工具帮你完成后，怎样证明自己真正会”“大规模日志怎样处理”“Agent SQL 如何检测错误”“测试用例 90% 通过率怎样得到”，更接近对 AI-assisted Engineering 的可验证工程能力检查；但由于该来源的 post-specific provenance 尚未闭环，这一信号目前只记作 Recall / Market Observation，不新增 Canonical、不修改 Curriculum。

Morning 盲区：Afternoon 优先继续追 **4399 9/18 Agent 开发** 与 **阳光电源 9/18 AI 应用开发** 的稳定原帖详情；继续补快手 9/17 AI 应用一 / 二面、9/18～9/19 字节 / 阿里 / 腾讯 / 美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米的新发布目标岗原帖，以及非牛客平台的候选人本人正文。质量门槛不变。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-16 17:00 ～ 2026-09-19 17:00**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline 与全库去重。
- Baseline / full-history dedup：重新读取当前 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-29.md`，随后**逐个直接回读 `batch-01.md`～`batch-29.md` 全历史**。正式基线确认仍为 **29 Batch / 288 HUMAN-A / `S001–S288` / 最大 `S288` / 下一 `S289`**。本轮运行中 `main` 从上午基线继续前进到官方 2027 岗位同步相关提交；compare 确认并发变更只涉及 `.github/workflows/`、`market/jobs/` 和 `tools/`，未改动 monitoring / interviews，因此本轮以最新 HEAD 安全重放，不覆盖并发更新。当前根目录仍无 `research/` 一级目录。
- Search effort：Afternoon 新增至少 **110 组定向 Query / Query 变体**，重点补 Morning 的 4399 / 阳光电源 / 快手 9/17 AI 应用一二面，以及字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米等；岗位别名继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `AI Native` / `Coding Agent` / `Harness` / `Runtime` / `RAG` / `大模型应用开发` / `智能体开发`，并继续追牛客作者 Timeline 与小红书 / 知乎 / 脉脉 / 博客 / 技术社区可核验原文。
- Verification effort：实际打开、回读或追源 **25+ 次**近期原帖、作者页、企业页和 provenance 入口；Cache Miss / Search Snippet / 企业聚合只计验证工作量，不替代正式 HUMAN-A 原始证据。
- Passed HUMAN-A → Inbox：**1 个新流程：阳光电源 AI 应用开发工程师一面（作者 `小红不是绿`，面试 2026-09-18 10:00）**。当前 Inbox 共 **1** 个候选；Afternoon 不分配 `Sxxx`、不创建 Batch。

Afternoon 通过项：

1. **阳光电源｜AI 应用开发工程师｜一面｜9/18 10:00**：本轮补齐了 Morning 缺失的 post-specific 原始详情 URL：`https://www.nowcoder.com/feed/main/detail/122fd928ee824ed99c8f834233d1ac23?sourceSSR=enterprise`。Exact URL 检索能够完整回读原始正文，作者 `小红不是绿`，正文以 `#发面经攒人品 #秋招面试记录` 发布。作者主页显示为大连大学 2027 Java 候选人，并连续记录 BIGO、上海华力、阳光电源等本人招聘 Timeline，不是批量内容账号。
2. **整场问题**：自我介绍；线上支付失败时整个执行 / 诊断链路如何走；为什么需要 Network 这一步；RAG 召回低可能原因与解决；PDF 同时含表格 / 图片时怎样解析；原文第 6 题写作“`MPC和Function Calling的区别`”；客户端实习而项目偏 AI 应用 / 后端的选择与职业规划；更喜欢局部 Component 还是端到端参与；如果资源更充足下一步怎样改进当前实习 / 项目；反问。当前不自行把原文 `MPC` 改写为 `MCP`。
3. **全历史去重**：在写入 Inbox 前已逐个直接回读 `batch-01.md`～`batch-29.md`。未发现同 URL、作者、公司 / 日期 / 岗位，或“支付失败全链路 → Network → RAG 低召回 → 异构 PDF → Function Calling 边界 → 端到端 Ownership”连续题序的历史同场来源。GitHub 对 exact URL 的 0 命中只作辅助证据。

Afternoon 重点排除 / 待追源：

1. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：作者个人 Timeline、目标 Role Scope 与 14 道连续题序都很强，已能看到“如何证明自己真正掌握而不是依赖 AI”“10 万级日志处理”“Harness Architecture”“Agent 生成 SQL 的错误检测”“90% 测试通过率如何得到”等内容；但仍没有稳定解析到 post-specific 原帖详情 URL。按 Stable Original Gate，作者索引 / 搜索结果即使完整也不能替代原帖，继续待追源、不进 Inbox。
2. **快手 9/17 AI 应用开发一 / 二面**：继续无法稳定回读候选人原始详情正文；企业页 / Search Snippet 不能替代原帖，零贡献。
3. **快手 AI 全栈 `明天会有好天气`**：重新回读全历史确认该场就是 `batch-27.md` 的 `S282`，属于正式历史精确重复；不因近期再次命中重新进入 Inbox。
4. **OPPO 9/18 线下面 `鹤逸123`**：真人第一人称、两轮技术 + HR，传统 Backend 问题后确实追到 AI Memory / AI Development Flow；但页面无法证明目标岗位主体属于 AI Application / Agent，作者 Timeline 也更偏通用 Java 求职。按 Role Scope Gate 排除，不能因为问到 AI 就升级。
5. **去哪儿 9/16 AI 应用开发（全栈）**：Role Scope 和真人现场仍成立，但稳定正文依旧主要是流程摘要，连续技术题不足，维持既有排除。
6. **非牛客平台 / 聚合 / JD**：本轮继续覆盖小红书、知乎、脉脉、CSDN、掘金、博客园、Bilibili 与职位页；最新高曝光结果仍主要是课程、答案、整理、职位或转载，未形成新的可核验候选人本人 HUMAN-A。

Afternoon 主要观察：**AI Application 面试的工程验真继续从“会不会 Agent 名词”转向 Production Diagnosis + Retrieval Failure Attribution + Heterogeneous Document Processing + End-to-end Ownership。** 阳光电源直接让候选人解释线上支付失败的完整链路、Network 为什么存在、RAG 低召回怎样分层定位、PDF 表格 / 图片怎样处理，并继续问候选人偏好局部模块还是端到端参与。这与既有“Production Engineering + Agent”趋势一致，但仍只作为 Market Observation，不新增 Canonical、不修改 Curriculum。与此同时，4399 待追源线索持续强化 Harness + AI-assisted Engineering Authenticity Verification；OPPO 普通 Java 流程也开始问 AI Memory / Development Flow，进一步说明 Role Scope Gate 不能放松。

Afternoon 盲区：22:00 优先继续追 **4399 9/18 Agent 开发** 的 post-specific 原帖、**快手 9/17 AI 应用一 / 二面** 的稳定正文，并继续补 9/18～9/19 字节 / 阿里 / 腾讯 / 美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米以及非牛客候选人原帖。对当前阳光电源 Inbox 候选，22:00 必须再次直接回读全部历史 Batch 后再决定是否分配当前真实下一 `Sxxx`。

Afternoon 不新增 Canonical，不修改 Curriculum，也不写入 `market/interview-experience/01-data/`、`market/analysis/` 或任何 Curriculum 正文。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-16 22:00 ～ 2026-09-19 22:00**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline 与全库去重。
- Baseline / full-history dedup：重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-29.md`，随后再次**逐个直接回读 `batch-01.md`～`batch-29.md` 全历史**。确认正式基线为 **29 Batch / 288 HUMAN-A / `S001–S288` / 最大 `S288` / 下一 `S289`** 后才执行最终编号。晚间运行中 `main` 相对开始时前进 5 个提交；compare 确认这些并发变更只涉及 `market/jobs/` 与 `tools/`，没有修改 `market/monitoring/` 或 `market/interview-experience/01-data/raw/`，因此基于最新 HEAD 安全重放。根目录复核仍**没有 `research/` 一级目录**。
- Search effort：Evening 新增至少 **100 组定向 Query / Query 变体**，继续覆盖字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及 4399、阳光电源等近端线索；岗位别名继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `AI Native` / `Coding Agent` / `Harness` / `Runtime` / `RAG` / `大模型应用开发` / `智能体开发`，同时继续追牛客原帖、作者 Timeline 与非牛客可核验公开来源。
- Verification effort：第三轮显式打开、回读或追源 **20+ 次**近期原帖、作者页、企业页、推荐入口、职位页或 provenance 线索；这是验证工作量，不等于 20 个唯一原始 HUMAN-A 页面。Search Snippet、企业聚合、JD、答案化展示与打不开的原帖均不替代稳定候选人原始证据。
- New HUMAN-A after Evening search：**0 个**。第三轮没有发现新的、同时满足最近 72 小时 + 真人面试官 + 候选人第一人称 + 高技术密度 + 目标 Role Scope + 稳定原文 + 全历史去重的独立流程。
- Final dedup：Afternoon Inbox 的阳光电源候选再次与 `S001–S288` 全历史核对，仍通过最终 Gate；未发现同 URL、同作者、同公司同流程或连续独特题序的历史重复。GitHub Code Search 对 exact URL、作者和独特组合的 0 命中仅作辅助证据。
- Final Batch：创建 `batch-30.md`，将当前唯一最终通过者分配为 **`S289`**；归档后 Inbox 清空。

Evening 重点复核：

1. **阳光电源 AI 应用开发工程师一面｜9/18 10:00｜`小红不是绿`**：post-specific 原始详情页晚间仍可稳定直接回读，明确显示公司、时间、岗位以及 10 个现场问题；原文第 6 题仍写作 `MPC和Function Calling的区别`，不自行修正。最终归档 `S289`。
2. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：作者 Timeline、Role Scope 与 14 道连续题序仍然很强，涉及 Harness Architecture、10 万级日志、Agent 生成 SQL 错误检测、90% 测试通过率来源以及“如何证明不是只依赖 AI 工具”；但晚间仍没有稳定拿到 post-specific 原始详情页。作者索引 / Search Snippet 不能替代 Stable Original，继续待追源、零贡献。
3. **快手 9/17 AI 应用开发一 / 二面**：相关推荐 / 企业入口继续暴露长任务服务崩溃恢复、并发修改会话记忆等高价值问题，但候选人原始详情正文与作者 provenance 仍不够稳定，且部分展示片段混入明显解释 / 答案式展开；不升级 HUMAN-A。
4. **PDD / B站 / 腾讯等合集、完整答案和 Agent 面经总结**：近期结果中继续出现“面经 06/07/08”“含完整答案”“Agent 面经总结”等整理型页面，不是候选人本人单一招聘流程原始证据；全部零贡献。
5. **OPPO 9/18 线下面、普通 Data / Backend / Test 岗近期 AI 深挖**：真人面试中已经出现 AI Memory、AI Development Flow、Agent / AI Coding 等内容，但岗位主体并非 AI Application / Agent；继续按 Role Scope 排除。
6. **小红书近期多模态算法 / 端侧推理等结果**：岗位主体落在模型 / 算法 / 推理优化边界；同平台 9/15 AI 应用研发则已是历史 `S286`，不重复计数。
7. **JD / 企业页 / 内推 / 题库 / 聚合 / 新闻**：只用于发现和市场旁证，不贡献 HUMAN-A。

### Final Summary

- Three-round search effort：**至少 300 组 Query / Query 变体**（Morning ≥90 + Afternoon ≥110 + Evening ≥100）。
- Three-round verification effort：**至少 65 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 20+ + Afternoon 25+ + Evening 20+）；这是工作量次数，不代表 65 个唯一 URL。
- Final additions：**1 个 HUMAN-A，`S289`**。
- Current formal Market library：**30 Batch / 289 HUMAN-A / `S001–S289`**。
- Next ID：**`S290`**。
- Inbox：归档后清空。
- Frozen Canonical / Curriculum：**本日不修改**；`S289` 只进入后续 periodic canonical mapping / review candidate。

当日主要市场信号：

1. **AI Application 项目验真继续落到 Production Diagnosis。** 面试官不只问 RAG / Function Calling 名词，而是要求从线上支付失败完整链路解释系统如何定位问题，并追 Network 为什么存在。
2. **Retrieval Failure Attribution 与异构文档处理仍是稳定工程问题。** RAG 低召回要能分层定位原因；PDF 表格 / 图片需要给出实际解析链路，而不是只报 Parser 名称。
3. **End-to-end Ownership 被直接验证。** 候选人会被问更偏局部 Component 还是全链路参与，以及资源充分时下一步怎样演进系统。
4. **Harness + AI-assisted Engineering Authenticity Verification 是值得继续追的弱信号。** 4399 线索已经把 Harness、SQL 验错、测试指标和“AI 帮你完成后是否真正掌握”放在一起，但 provenance 尚未闭环，因此当前只作为观察，不进入正式频率。
5. **Agent / AI 术语继续向普通 Backend / Data / Test 岗扩散。** 这使 Role Scope Gate 更重要，而不是更宽松；出现 Memory / Agent / AI Coding 不能替代目标岗位证据。

饱和度 / 盲区：最近 72 小时公开结果层继续呈现**局部饱和 + provenance 成本高**。牛客仍是最容易拿到稳定第一人称原帖的平台，但内容合集、答案化页面、普通岗位 AI 深挖与原帖不稳定占比较高；4399 9/18 Agent、快手 9/17 AI 应用一 / 二面仍是最值得继续补 provenance 的近端线索。腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺新的高质量、稳定可核验目标岗第一人称来源。继续补盲，但不降低 Gate。

---

## 2026-09-20

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-17 10:09 ～ 2026-09-20 10:09**；主动发现只使用窗口内新发布 / 更新，历史页面只用于 provenance、作者 Timeline 与去重参考。
- Baseline：重新读取当前 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 和最新 `batch-30.md`。当前文件与最新 Batch 一致显示正式 Market 基线为 **30 Batch / 289 HUMAN-A / `S001–S289` / 下一 `S290`**，本轮开始时 Inbox 为空。根目录复核没有 `research/` 一级目录。由于本轮 **0 个候选进入 Inbox、0 个 ID 分配**，未触发“准入前直接回读全部历史 Batch”的写入前 Gate；若 Afternoon 有候选达到准入线，必须先直接回读 `batch-01.md`～`batch-30.md` 全历史。
- Search effort：至少 **100 组定向 Query / Query 变体**。逐公司覆盖字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，并补 4399、携程等近端线索；岗位别名覆盖 `AI Application` / `Agent` / `RAG` / `AI Backend` / `AI Full-stack` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `大模型应用开发` / `智能体开发`。另对小红书、知乎、脉脉、CSDN、掘金、博客等非牛客来源做补盲。
- Verification effort：显式打开、回读或追源 **25+ 次**候选原帖、作者页、企业页、话题页或 provenance 入口；其中多个 post-specific 牛客 URL 仍出现 Cache Miss。Search Snippet、企业聚合、作者索引、JD、答案化页面均只算验证工作量，不替代 Stable Original。
- Passed HUMAN-A → Inbox：**0 个**。本轮没有新的流程完整满足 HUMAN-A + Role Scope + Stable Original Gate，因此 Inbox 继续为空；不分配 `Sxxx`、不创建 Batch。

Morning 重点复核 / 排除：

1. **字节广告团队 Agent 一 / 二面｜9/19 17:07**：最新直接搜索结果可完整看到两轮连续问题，一面包含 Redis 分布式锁、MySQL 聚簇索引、内部 Skill 平台（上传 / 下载 / 发布）与本地 Runtime 设计、最长回文串；二面 Leader 继续追 AI 提效、营销会场秒杀系统、现场演示本人 Demo、Skill vs Function Call，以及算法题。真人现场、技术密度和目标 Role Scope 都很强；但 post-specific 原帖 `https://www.nowcoder.com/discuss/930870582843805696?sourceSSR=home` 本轮直接打开仍 Cache Miss，且当前搜索结果没有稳定给出作者身份 / Timeline，因此暂不进 Inbox。Afternoon 优先补作者 provenance 与可稳定原文。
2. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：作者主页索引今天已经能稳定暴露完整问题链和连续求职 Timeline，问题继续覆盖“如何证明不是只依赖 AI”、十万级日志、Harness、Agent SQL 验错、测试成功率来源与转 AI 能力缺口；团队反问也明确为约 20+ 人内部业务 AI 研发。但仍未拿到可长期稳定核验的 post-specific 原帖详情 URL；延续昨日同一 Stable Original Gate，不因为作者索引变完整就降低准入标准。
3. **携程 AI 应用开发一 / 二面｜9/18 发布**：企业 / 话题入口出现同一流程两轮高密度问题，一面涉及 Agent 原子能力编排、Context Compression 触发阈值、Agent 写操作权限、CAS / AQS、ThreadLocal、索引、缓存一致性、MQ 与 AI Coding；二面继续追内容生产 Agent、Skill 评测、Bad Case、模型选型、多模态与 MCP。但当前仍未稳定定位候选人 post-specific 原帖与作者 Timeline，且企业页文本呈结构化展开；按 provenance Gate 继续零贡献。
4. **快手 AI 应用开发秋招一面｜9/19 19:35**：企业页能看到项目架构、核心 Prompt、多轮审查 Memory 等连续追问，但展示文本混入明显解释 / 答案式扩写，未定位候选人原帖与作者 provenance；不升级 HUMAN-A。
5. **B站“大模型面试岗” 9/19**：正文明确是内容作者“跟一个面试 B 站大模型算法实习岗的学员聊了两个小时后让对方复述”，属于二手转述，不是候选人本人第一人称；同时岗位偏算法，直接排除。
6. **PDD AI Agent `林小白zii` 系列**：仍按“面经 01 / 02 / 03...”批量合并不同日期场次，并混入标准答案 / SQL / 代码展开，属于合集 / 内容链风险；零贡献。
7. **9/20 新出现的匿名 `Agent 开发面经`**：技术链覆盖 Workflow / Multi-Agent Stage、状态机、HITL、Tool Call、RAG、JSON Schema、失败重试 / 降级等，但作者明确不披露公司与具体岗位 / 项目信息，无法建立公司 / 招聘流程和 Role Scope 的稳定闭环；当前只作 Recall，不进 Inbox。
8. **非牛客平台与聚合站**：NiceOffer、面灵、CSDN / 博客、求职整理页等仍以二次整理、答案、旧面经或泛化题库为主；本轮未发现最近 72 小时内新的、同时满足第一人称 + 真人面试 + 目标 Role Scope + Stable Original 的来源。

Morning 主要观察：近期高价值线索继续把 **Skill / Runtime、Context Compression、Agent 写权限、现场 Demo、AI-assisted Engineering 验真** 放入真实招聘追问链，但今天上午这些线索的 provenance 仍未全部闭环，不能把它们升级为正式 HUMAN-A 频率。尤其字节广告团队已经从“是否懂 Skill”进一步追到“内部 Skill 平台如何发布、本地 Runtime 怎么设计、能不能现场演示 Demo”；这只记录为 Market Observation，不新增 Canonical，也不修改 Curriculum。

Morning 盲区：17:00 优先追 **字节广告团队 9/19 Agent 一 / 二面** 的作者身份与稳定原帖、**4399 9/18 Agent** 的 post-specific URL、**携程 9/18 AI 应用开发一 / 二面** 的候选人原帖与 Timeline，以及 **快手 9/19 AI 应用开发** 的原始正文；继续补腾讯 / 美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米和非牛客平台的新发布目标岗来源。质量门槛不变。

Morning 不修改 `market/interview-experience/01-data/`、`market/analysis/` Frozen 统计或任何 Curriculum 正文。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-17 16:58 ～ 2026-09-20 16:58**；主动发现只使用窗口内新发布 / 更新，历史页面只用于 provenance、作者 Timeline 与全历史去重。
- Baseline / full-history dedup：重新读取当前 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-30.md`；由于本轮出现可进入 Inbox 的候选，随后**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-30.md` 全历史**。正式基线确认仍为 **30 Batch / 289 HUMAN-A / `S001–S289` / 最大 `S289` / 下一 `S290`**。根目录复核仍无 `research/` 一级目录。
- Search effort：Afternoon 新增至少 **100 组定向 Query / Query 变体**。除 Morning 的字节广告团队、4399、携程、快手近端线索外，继续覆盖字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场；岗位别名继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `RAG` / `大模型应用开发` / `智能体开发`，并补小红书、知乎、脉脉、博客 / 技术社区等非牛客来源。
- Verification effort：显式打开、回读或追源 **30+ 次**近期 post-specific 原帖、作者页、企业页、推荐入口和 provenance 线索；这是验证工作量，不等于 30 个唯一 URL。Cache Miss、Search Snippet、企业聚合和答案化展示均不替代 Stable Original。
- Passed HUMAN-A → Inbox：**2 个独立招聘流程**，均来自同一真实候选人 `中二的西红柿起床了`，但公司不同，按规则分别暂存：① 小红书 AI 全栈开发实习一面；② Shopee Chatbot 研发实习一面。Afternoon **不分配 `Sxxx`、不创建 Batch**。

Afternoon 通过项：

1. **小红书｜AI 全栈开发实习｜一面｜面试 8/25，发布 9/18 15:43**：post-specific 原帖 `https://www.nowcoder.com/feed/main/detail/c712eda7fbf44ba69835b6dd2ff7fc4c?sourceSSR=enterprise` 可稳定直接回读。作者明确记录“回忆一下”“大部分时间都在问项目”，面试官围绕项目反复追“为什么一定要 Multi-Agent、怎样编排”，要求候选人说服其 Architecture Choice；随后进入 Skill、RAG / Vector DB、Harness，再继续追 Evaluation、成果、同事反馈、准确率和具体功能，候选人对未覆盖点明确写“终于投降了说这块没有想到”。无手撕 / 无传统八股，约 40 分钟项目深挖，一面未通过。作者同一账号还有长期个人学业 / 求职记录，以及本周 Shopee 本人面经，Candidate Timeline 成立。
2. **Shopee｜Chatbot 研发实习｜一面｜面试 9/18，发布 9/19 16:25**：post-specific 原帖 `https://www.nowcoder.com/feed/main/detail/9f02a7f8009d4aca9fc730a18b9f96cc` 可稳定直接回读。连续问题为 Agent 定义 → Function Call / Tool / MCP → 项目 RAG 与文档规模 → Linux Process → 数组第 K 大；Coding 从“排序后取第 K 个”继续追 Quick Sort 复杂度、机制和手写实现，再问其它方法，作者明确记录自己“不会 / 发呆”、最后用 `sort` 两行写完，之后再问日常 AI Coding。整场 20 多分钟，现场失败状态明确。岗位标题为 `chatbot研发实习`，技术主体明确属于 AI Application / Agent Chatbot，而不是普通后端顺带问 AI。
3. **作者真实性 / Timeline**：同一账号 `中二的西红柿起床了` 还可稳定回读 5 月本人关于从国有银行去 HKU CS、希望未来做 Agent 开发的长期个人记录；两篇新面经同样显示香港大学 C++、上海发布，个人候选人画像连续，不是短期批量面经账号。
4. **全历史去重**：写入 Inbox 前已逐个直接回读全部 30 个正式 Batch，并核验 URL、作者、公司 / 日期 / 岗位、项目语义与连续题序。历史虽已有多条小红书 AI Full-stack / Agent 和 Shopee Agent 来源，但没有当前作者、URL 或相同连续题序；Shopee 历史 `S081 / S239` 等为其它候选人 / 其它月份独立流程。GitHub exact URL / 作者 0 命中仅作辅助，不作为未收录证明。

Afternoon 重点排除 / 待追源：

1. **字节广告团队 Agent 一 / 二面｜9/19**：搜索层继续能读到内部 Skill 平台上传 / 下载 / 发布、本地 Runtime、AI 提效、现场 Demo、Skill vs Function Call 等强链路，但 post-specific 原帖仍无法稳定直接回读且作者 Timeline 未闭环；继续零贡献。
2. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：作者主页现在能稳定确认本人求职 Timeline 与该场 Agent 开发面试，且 14 道问题链包含“怎样证明不是只依赖 AI 工具”、十万级日志、Harness、Agent SQL 验错、测试通过率来源等；但仍缺可稳定直接回读的 post-specific 原帖详情页。严格执行 Stable Original Gate，不因为作者索引已经很完整就升级 HUMAN-A。
3. **携程 AI 应用开发一 / 二面｜9/18 发布**：企业入口的连续问题仍然很强，包括 Agent 原子能力编排、Context Compression 阈值、Agent 写权限、CAS / AQS、ThreadLocal、Cache / MQ / AI Coding，以及二面 Skill Evaluation / Bad Case / Multimodal / MCP；两个 post-specific 详情页仍 Cache Miss，作者 Timeline 未闭环，继续零贡献。
4. **腾讯 AI 全栈｜9/18 面试、9/19 发布**：可检索到大文件 JSONL + 高并发、CSRF / 同源、数据库模拟任务队列、Worker Crash / Graceful Exit、JS Rate Limiter 等完整真人链，且有面后秒挂状态；但 exact post-specific 直链直接回读仍 Cache Miss，按 Stable Original Gate 排除，不以 Search Cache 替代原帖。
5. **小红书 Agent 平台研发一面｜9/20 14:15**：企业页可见约 29 分钟真人一面和 10 道问题，涉及既往团队职责、转 Agent 动机、团队协作 / Evaluation 与高并发商品详情 System Design；但 post-specific 详情页仍 Cache Miss，且作者 provenance 未闭环，不进 Inbox。
6. **快手近期 AI 应用 / AI 全栈**：企业页继续出现高密度 Agent / AI Coding 结果，但部分是历史 `S282` 等精确重复，部分正文混入答案式展开且缺原作者 provenance；没有新的稳定独立 HUMAN-A。
7. **PDD `林小白zii` 系列、腾讯“超全整理”等**：明显属于多场合集 / 答案 / 内容整理链；即使题目新也零贡献。
8. **非牛客平台**：本轮继续补小红书 / 知乎 / 脉脉 / 博客 / 技术社区，仍未发现最近 72 小时内同时满足 Stable Original + Candidate First-person + 目标 Role Scope 的新增来源。

Afternoon 主要观察：**“Architecture Choice 必须被证明”正在成为 Agent 项目验真的更明确形式。** 小红书新候选不是停在“做了 Multi-Agent”，而是面试官反复要求解释为什么必须 Multi-Agent、怎样编排，再继续追 Harness、RAG 与 Evaluation / 真实反馈 / 准确率。这与过去单纯问框架定义不同，更接近“为什么这个架构真的必要、怎样用结果证明”。与此同时，Shopee Chatbot 仍把 Agent / MCP / RAG 与 Linux / Algorithm / AI Coding 放在同场，继续说明目标 AI Application 岗的 Foundation 不能弱化。以上只进入 Market Observation，不修改 Frozen Canonical、`market/analysis/` Frozen 统计或 Curriculum 正文。

Afternoon 盲区：22:00 优先重新核验当前 2 个 Inbox 候选的稳定原帖与作者 Timeline，并再次直接回读全部正式 Batch 做最终去重；继续追字节广告团队、4399、携程、腾讯 AI 全栈、小红书 Agent 平台研发的 post-specific 原帖 / 作者 provenance，以及美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米和非牛客平台的新目标岗来源。质量门槛不变。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-17 21:58 ～ 2026-09-20 21:58**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline 与全库去重。
- Baseline / full-history dedup：重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-30.md`，并在分配任何编号前再次**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-30.md` 全历史**。确认归档前正式基线仍为 **30 Batch / 289 HUMAN-A / `S001–S289` / 最大 `S289` / 下一 `S290`**。晚间运行期间 `main` 又前进 6 个提交；compare 确认并发变更只涉及 `.github/workflows/`、`market/jobs/` 与 `tools/`，没有修改 monitoring / interviews，因此基于最新 HEAD 安全重放。根目录再次复核，**没有 `research/` 一级目录**。
- Search effort：第三轮新增至少 **100 组定向 Query / Query 变体**，继续覆盖字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场；岗位别名继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `RAG` / `大模型应用开发` / `智能体开发`，并重点复查字节广告团队、4399、携程、腾讯 AI 全栈、小红书 Agent 平台研发与非牛客平台盲区。
- Verification effort：第三轮显式打开、回读或追源 **20+ 次**近期 post-specific 原帖、作者页、企业页、搜索结果与 provenance 入口；Search Snippet、企业聚合、答案化展示或只能取得页面壳的原帖不替代 Stable Original。
- New HUMAN-A after Evening search：**0 个**。第三轮没有发现新的、同时满足最近 72 小时 + 真人面试官 + 候选人本人第一人称 + 高技术密度 + 目标 Role Scope + Stable Original + 全历史去重的独立招聘流程。
- Final dedup：Afternoon Inbox 的两个候选重新与 `S001–S289` 全历史逐项核对，均再次通过最终 Gate；没有出现更早 canonical source、同公司同流程后续轮次或复制链证据。
- Final Batch：创建 `batch-31.md`，按当前真实下一编号连续归档 **`S290–S291`**；归档后 Inbox 清空。

Evening 重点复核：

1. **小红书 AI 全栈开发实习一面｜`中二的西红柿起床了`**：post-specific 原帖晚间仍可稳定回读，作者、发布时间、现场失败状态和“为什么必须 Multi-Agent → 编排 → Skill → RAG / Vector DB → Harness → Evaluation / 成果 / 反馈 / 准确率”的连续追问完整。最终归档 `S290`。
2. **Shopee Chatbot 研发实习一面｜同作者**：原帖晚间仍稳定可读；Agent → Function Call / Tool / MCP → RAG 文档规模 → Linux Process → 第 K 大 / Quick Sort 连续深追 → AI Coding 的题序和“不会 / 发呆 / 用 sort 两行完成”的现场状态完整。与 `S290` 是同一候选人、不同公司独立招聘流程，最终归档 `S291`。
3. **字节广告团队 Agent 一 / 二面｜9/19 17:07**：当前 Search 层能够完整回读两轮问题，包含内部 Skill Platform 上传 / 下载 / 发布、本地 Runtime、AI 提效、营销秒杀、现场 Demo、Skill vs Function Call 与 Coding；但 direct post-specific open 仍只返回页面壳，且作者账号 / Timeline 未稳定闭环。技术价值很高但 provenance 仍不满足 Stable Original Gate，继续零贡献。
4. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：作者主页与完整 14 题索引保持可见，包含 Harness、十万级日志、Agent SQL 验错、90% 测试通过率来源和“如何证明不是只依赖 AI”；但 post-specific 详情正文仍未稳定闭环，继续待追源。
5. **快手 AI 全栈 `明天会有好天气`**：全历史直接回读再次确认就是正式 `S282`，精确重复，零新增。
6. **携程 9/18 AI 应用一 / 二面、腾讯 9/18 AI 全栈、小红书 9/20 Agent 平台研发**：仍主要依赖企业 / 话题索引或 Search Cache，候选人 post-specific 原始正文与作者 provenance 未完整闭环，不升级 HUMAN-A。
7. **B站 9/19“大模型面试岗”**：正文明确为内容作者让一位学员复述其面试，属于二手转述而非候选人本人第一人称；且岗位偏算法，排除。
8. **普通 Backend / Data / Test 岗近期 Agent / Memory / AI Coding 深挖**：继续严格按 Role Scope 排除；“出现 Agent 名词”不能替代目标职位证据。
9. **合集 / 标准答案 / 内容号 / JD / 内推 / 聚合 / 新闻**：只用于发现与市场旁证，不贡献 HUMAN-A。

### Final Summary

- Three-round search effort：**至少 300 组 Query / Query 变体**（Morning ≥100 + Afternoon ≥100 + Evening ≥100）。
- Three-round verification effort：**至少 75 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 25+ + Afternoon 30+ + Evening 20+）；这是工作量次数，不代表 75 个唯一 URL。
- Final additions：**2 个 HUMAN-A，`S290–S291`**。
- Current formal Market library：**31 Batch / 291 HUMAN-A / `S001–S291`**。
- Next ID：**`S292`**。
- Inbox：归档后清空。
- Frozen Canonical / `market/analysis/` / Curriculum：**本日不修改**；`S290–S291` 只进入后续 periodic canonical mapping / review candidate。

当日主要市场信号：

1. **Architecture Choice 必须被证明。** 真实面试已经从“用了 Multi-Agent”进一步追到为什么必须 Multi-Agent、为什么不能更简单、怎样编排，以及结果 / 准确率 / 使用者反馈能否证明架构值得存在。
2. **Agent / MCP / RAG 与 Foundation 仍同场。** Shopee Chatbot 把 Agent、Function Call / Tool / MCP、RAG 与 Linux Process、Quick Sort 深追、AI Coding 放在同一场，应用岗的系统基础与算法能力不能弱化。
3. **Skill / Runtime 正继续向平台级设计与现场验真下沉。** 字节广告团队待追源样本已经问内部 Skill Platform 发布、本地 Runtime、现场 Demo 与 Skill vs Function Call；provenance 未闭环，因此仅记 Market Observation，不计正式频率。
4. **AI-assisted Engineering 的真实性验证继续增强。** 4399 待追源样本同时追 Harness、SQL 验错、测试通过率来源与“如何证明不是只依赖 AI 工具”；值得继续追，但当前不进入 HUMAN-A。
5. **Role Scope Gate 需要继续收紧。** Agent / Memory / AI Coding 已扩散到普通 Backend / Data / Test 岗；术语出现本身越来越不能证明岗位主体属于目标范围。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现**局部饱和 + 高 provenance 成本**。牛客仍是最容易取得稳定候选人原帖的平台，但企业聚合、Search Cache、答案化页面与 post-specific Cache Miss 占比较高；字节广告团队、4399、携程、腾讯 AI 全栈、小红书 Agent 平台研发仍是最值得继续补 provenance 的近端线索。腾讯 / 美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺更多稳定可核验的新目标岗第一人称来源。继续补盲，但不降低 Gate。

---

## 2026-09-21

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-18 10:09 ～ 2026-09-21 10:09**；主动发现只使用窗口内新发布 / 更新，窗口外页面只用于 provenance、作者 Timeline、Role Scope 与历史背景判断。
- Baseline：重新读取当前 `main`、`market/README.md`、`market/interview-experience/05-logs/inbox.md`、`market/interview-experience/05-logs/daily-log.md`、两份 Market Policy 和最新 `market/interview-experience/01-data/raw/batch-31.md`。当前正式 Market 基线为 **31 Batch / 291 HUMAN-A / `S001–S291` / 最大 `S291` / 下一 `S292`**，本轮开始时 Inbox 为空；仓库根目录复核仍**没有 `research/` 一级目录**。由于本轮最终 **0 个候选进入 Inbox、0 个 ID 分配**，未触发“准入 / 编号前逐个直接回读全部历史 Batch”的写入前 Gate；若 Afternoon 有候选达到准入线，必须先直接回读 `batch-01.md`～`batch-31.md` 全历史。
- Search effort：至少 **180 组定向 Query / Query 变体**。逐公司覆盖字节 / 抖音、阿里 / 阿里云 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，并继续补 4399、携程、Shopee、去哪儿等近端线索；岗位别名覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `RAG` / `大模型应用开发` / `智能体开发`。另外单独补小红书 / 知乎 / 脉脉 / CSDN / 掘金 / Bilibili / 独立技术社区与聚合站，用于追原帖而非替代原帖。
- Verification effort：显式打开、回读或追源 **27+ 次** post-specific 原帖、作者主页、企业面经页、话题页、二次整理页和 provenance 入口；其中多条牛客 direct detail 只能返回页面壳。Search Snippet、企业聚合、二次整理和 JD 只算验证工作量，不替代 Stable Original。
- Passed HUMAN-A → Inbox：**0 个**。本轮没有新的流程完整满足真人面试官 + 候选人本人第一人称 + 高技术密度 + 目标 Role Scope + Stable Original + 可核验 Candidate Timeline / provenance；Inbox 继续为空，不分配 `Sxxx`、不创建 Batch。

Morning 重点复核 / 排除：

1. **字节 AI 后端开发二面｜当前热门新帖**：已定位 post-specific 原帖 `https://www.nowcoder.com/feed/main/detail/a197824e0e6e444297482be3c155b0a8`，目标 Role Scope 成立；二次索引可见 Redis、RAG、大规模预约系统设计与算法等连续内容。但 direct original 本轮仍只返回页面壳，作者身份 / Timeline 也未闭环。不能用面灵等二次整理替代候选人原帖，因此 Morning 只记待追源，零贡献。
2. **阿里云 AI 应用开发一面｜9/16 面、9/19 挂**：企业面经页当前可见真人流程，技术链包含 LLM Hallucination、RAG 定义 / 完整流程、两个 RAG 实现如何比较与选型、MCP、百亿级商品 CRUD / 分库分表思路、AI Coding 与现场 Coding；Role Scope 很强。但稳定入口仍是企业聚合页，尚未定位候选人 post-specific 原帖与账号 Timeline，不进 Inbox。Afternoon 优先追原始详情与作者 provenance。
3. **小红书 Agent 平台研发一面｜9/20**：企业页仍可见约 29 分钟真人一面和目标 Agent 平台岗位，但 post-specific 原帖、作者身份与 Timeline 仍未闭环；延续昨日 Stable Original Gate，零贡献。
4. **4399 Agent 开发｜9/18｜`AAA野生原子弹批发`**：作者主页与个人求职 Timeline 继续稳定，14 道问题链仍覆盖“如何证明不是只依赖 AI”、十万级日志、Harness、Agent SQL 验错、测试成功率来源等；但 post-specific 原始详情正文依然无法稳定取得。作者索引不能替代原帖，继续待追源。
5. **携程前端一面｜9/20 发布**：这是本轮稳定可直接回读的候选人原帖，连续问 Skill、Agent Context 中的 Message 分类、如何搭建简单 Chat Harness、是否读过 DeepSeek Harness 源码，说明 Harness / Skill 已明显扩散进普通前端招聘；但标题明确为前端工程师，无法证明目标 AI Application / Agent Role Scope，因此严格排除，不贡献 HUMAN-A。
6. **欣旺达 9/20 数据开发 AI 面**：页面明确为 `AI面`，属于 AI 自动面试，同时岗位主体是数据开发；同时违反 Human Interviewer 与 Role Scope Gate，直接排除。
7. **PDD Agent 系列、NiceOffer / 面灵等近期页面**：继续存在“面经 06/07/08”、题目摘要、准备建议、标准答案或来源转述等内容链 / 聚合风险；只用于 Recall / 追原帖，零贡献。
8. **匿名 `Agent 开发面经`、其它非牛客来源**：匿名来源仍不披露公司 / 具体岗位，无法闭环招聘流程；小红书 / 知乎 / 脉脉 / CSDN / 掘金 / Bilibili 等本轮新结果仍以课程、JD、趋势文章、转载或旧复盘为主，没有新的、稳定可核验目标岗候选人本人 HUMAN-A。

Morning 主要观察：**Harness / Skill 的“岗位扩散”已经非常明显，反而要求 Role Scope Gate 更严格。** 携程普通前端的稳定真人原帖已经直接问到 Chat Harness 与 DeepSeek Harness 源码；这类证据说明前沿 Agent 素养正在成为更广泛的软件工程能力，但不能被错误计入目标 AI Application / Agent 面试频率。另一方面，阿里云 AI 应用开发待追源样本仍把 RAG 方案选型与百亿级 CRUD / 数据库设计放在同一场，继续强化“AI Application = LLM/RAG + Production System Design”的市场方向；由于 provenance 尚未闭环，目前只记 Market Observation，不新增 Canonical、不修改 Curriculum。

Morning 盲区：17:00 优先追 **字节 AI 后端二面** 的作者与可稳定原文、**阿里云 AI 应用开发一面** 的 post-specific 原帖 / Candidate Timeline、**小红书 9/20 Agent 平台研发** 与 **4399 9/18 Agent** 的 stable original；继续补腾讯 / 美团 / 快手 / 百度 / 蚂蚁 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米及非牛客平台在 9/20～9/21 新发布的目标岗第一人称来源。质量门槛不变。

Morning 不修改 `market/interview-experience/01-data/`、`market/analysis/` Frozen Canonical 统计或任何 Curriculum 正文。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-18 17:00 ～ 2026-09-21 17:00**；主动发现只使用窗口内新发布 / 更新，历史页面只用于 provenance、作者 Timeline、Role Scope 与全历史去重。
- Baseline / full-history dedup：重新读取当前 `main`、`market/README.md`、`market/interview-experience/05-logs/inbox.md`、`market/interview-experience/05-logs/daily-log.md`、两份 Market Policy 和最新 `batch-31.md`；由于本轮出现可进入 Inbox 的候选，随后**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-31.md` 全历史**。重新确认正式 Market 基线为 **31 Batch / 291 HUMAN-A / `S001–S291` / 最大 `S291` / 下一 `S292`**。根目录复核仍没有 `research/` 一级目录。
- Search effort：Afternoon 新增至少 **120 组定向 Query / Query 变体**，针对 Morning 盲区重点追字节 AI 后端 / AI 全栈、阿里云 AI 应用、小红书 Agent 平台、4399 Agent，并继续覆盖字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场；岗位别名继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `RAG` / `大模型应用开发` / `智能体开发`。同时继续补小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等非牛客来源。
- Verification effort：显式打开、回读或追源 **25+ 次** post-specific 原帖、作者主页、企业页、搜索结果和 provenance 入口。只把 Stable Original + Candidate First-person 用于准入；Search Snippet、企业聚合、二次整理、JD 和页面壳只计验证工作量。
- Passed HUMAN-A → Inbox：**2 个独立招聘流程**，均由真实候选人 `SOLDIER_627` 发布，但公司不同，按规则分别暂存：① 小红书 Agent 平台研发一面；② 字节 AI 全栈（飞书）一面。Afternoon **不分配 `Sxxx`、不创建 Batch**。

Afternoon 通过项：

1. **小红书｜Agent 平台研发｜一面｜发布 9/20 14:15**：Morning 尚未闭环的 post-specific 原帖 `https://www.nowcoder.com/discuss/931189826643066880?sourceSSR=enterprise` 本轮已可稳定直接回读。作者 `SOLDIER_627`，同济大学 2027 Java，净时长约 29 分钟；正文明确记录上一段实习、求职方向、团队协作与 System Design，评论区楼主补充“面试官迟到 + 面完秒挂”，真人招聘现场成立。岗位标题直接为 Agent 平台研发。技术链包括：后续更想做 Agent 还是后端 → 设计支撑 **10 万 QPS** 且可水平扩展的商品详情服务（底层只有一张 MySQL 商品表）→ 管理端改价后如何完整设计缓存更新 / 失效链路保证 C 端价格新鲜度 → 现场最长回文字符串。原帖与作者主页均稳定可核验。
2. **字节｜AI 全栈（飞书）｜一面｜发布 9/21 14:28**：post-specific 原帖 `https://www.nowcoder.com/discuss/931555466247700480?sourceSSR=users` 可稳定直接回读，作者同为 `SOLDIER_627`，净时长约 1 小时。连续问题从 Agent 项目 Architecture → Agent 不遵守 Skill 限制时怎样治理、是否应把 Skill 规则写进更高优先级规范，继续进入海量监控视频 OOM / 多长视频串并行、分块上传与断点续传、一致性 / 清理、视频合并失败，再追 MySQL Index、SQL 800ms→50ms 后接口仍慢的端到端定位、Cache / Concurrency，最后是 10 万位大整数相加、Heap、HashMap、一致性哈希。Role Scope 与高技术密度均明确。
3. **作者真实性 / Timeline**：作者主页当前显示 18 篇发布，并连续记录 9/21 字节 AI 全栈、百度 Agent 后端三面，9/20 度小满 AI 全栈、小红书 Agent 平台，以及此前快手 AI 全栈、美团 AI 后端等本人招聘流程；个人身份、技术栈和求职 Timeline 连续稳定，不是批量内容账号。
4. **全历史去重**：写入 Inbox 前已逐个直接回读 `batch-01.md`～`batch-31.md`。历史确有同一候选人的其它公司正式流程（如快手 AI 全栈、美团 AI 后端）；这些与当前小红书、字节属于不同公司 / 独立招聘流程，不跨公司合并。未发现两个当前 URL、当前公司流程，或“小红书 Agent 平台 → 10 万 QPS / 缓存新鲜度 → 最长回文”“字节 Skill 遵从性 → 海量视频 OOM / 断点续传 / 清理 → SQL 端到端性能 → 大数 / Heap / HashMap / Consistent Hashing”的历史同场来源。GitHub Search 对作者 / exact URL 的 0 命中仅作辅助，不作为未收录证明。

Afternoon 重点排除 / 待追源：

1. **百度 Agent 后端三面｜同作者 `SOLDIER_627`｜9/21 09:13**：作者 Timeline 已能看到团队做内部 AI 研发提效平台、动态知识库等高价值内容，但 post-specific direct open 本轮仍只返回页面壳；同一作者并不能替代 Stable Original Gate。并且若后续补齐，需要与其已有百度同招聘流程轮次合并，而不是按轮次重复计数。
2. **度小满 AI 全栈一面｜同作者｜9/20 17:39**：作者页可见完整高密度摘要，但 post-specific 详情仍只返回页面壳；按 Stable Original Gate 不进 Inbox。
3. **腾讯 AI 全栈 9/18**：仍能定位高并发 JSONL、Worker Crash / Graceful Exit、数据库任务队列、JS Rate Limiter 等真人链，但 direct original 本轮仍是页面壳，继续零贡献。
4. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：作者 Timeline 和 Harness / 十万级日志 / Agent SQL 验错 / 测试通过率 / AI 真实性验证链仍然很强，但 post-specific Stable Original 仍未闭环；继续待追源。
5. **阿里云 AI 应用开发一面**：企业入口依旧可见 Hallucination、RAG 完整链与两方案比较、MCP、百亿级商品 CRUD / 分库分表、AI Coding / Coding，但候选人 post-specific 原帖与 Timeline 仍未闭环；企业聚合不替代 HUMAN-A provenance。
6. **合集 / 内容站 / 二次整理 / AI 自动面试 / 普通岗位 AI 深挖**：NiceOffer 等标准化页面、PDD 系列面经、SHEIN 转述、欣旺达 AI 自动面、普通 Backend / Frontend / Test 中的 Agent / Skill / Memory 深挖均继续按对应 Gate 排除，不因技术词新而放宽。
7. **非牛客平台**：本轮继续补小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等；最近 72 小时高曝光结果仍主要是课程、JD、整理、转载或旧复盘，没有新的、稳定可核验目标岗候选人本人 HUMAN-A。

Afternoon 主要观察：**Agent / AI Application 的工程验真正在进一步呈现“规则遵从 + 生产链路 + Foundation”三层同场。** 字节新候选不只问 Agent / Skill，而是追模型不遵守 Skill 约束时怎样提高规则优先级，再把同一场切到海量视频 OOM、断点续传 / 清理、SQL 端到端性能和传统数据结构；小红书 Agent 平台则直接用 10 万 QPS 商品详情与缓存新鲜度验证平台候选人的 System Design。前沿 Agent 能力没有替代传统工程底座，而是和它一起被验真。该信号只进入 Market Observation，**不修改 `market/interview-experience/01-data/`、`market/analysis/` Frozen 统计或任何 Curriculum 正文**。

Afternoon 盲区：22:00 应重新核验当前 2 个 Inbox 候选的 Stable Original 与作者 Timeline，并再次直接回读全部历史 Batch 做最终去重；继续追同作者百度 Agent 后端三面 / 度小满 AI 全栈的 post-specific 原文，以及 4399、阿里云、腾讯 AI 全栈、携程 / 快手等近端高价值线索。质量门槛不变。

---

## 2026-09-22

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-19 09:57 ～ 2026-09-22 09:57**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline、Role Scope 与去重参考。
- Baseline / recovery note：重新读取当前 `main`、`market/README.md`、`market/interview-experience/05-logs/inbox.md`、`market/interview-experience/05-logs/daily-log.md`、两份 Market Policy 与最新 `batch-31.md`。正式 Market 基线仍为 **31 Batch / 291 HUMAN-A / `S001–S291` / 最大 `S291` / 下一 `S292`**；根目录仍无 `research/` 一级目录。当前 `main` 仍停在 2026-09-21 Afternoon 状态：昨日 22:00 Finalize 未落库，Inbox 保留昨日已经通过准入 Gate 的 **2 个旧待归档流程**（小红书 Agent 平台研发、字节 AI 全栈（飞书））。Morning 按阶段规则不补发 ID、不创建 Batch，也不改动这两个既有 Inbox 条目；22:00 Finalize 必须重新直接回读全部正式 Batch 后处理这份 backlog。由于本轮没有新的独立候选进入 Inbox、也不分配 ID，本轮未触发新增候选准入前的全历史重新回读。
- Search effort：至少 **120 组定向 Query / Query 变体**，覆盖字节 / 抖音、阿里 / 阿里云 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及 4399、携程、度小满等近端线索；岗位别名继续覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `RAG` / `大模型应用开发` / `智能体开发`。同时补小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等非牛客来源。
- Verification effort：显式打开、回读或追源 **25+ 次** post-specific 原帖、作者主页、企业面经页、话题页与 provenance 入口；这是验证次数，不等于 25 个唯一 HUMAN-A URL。Search Snippet、企业聚合、二次整理和页面壳只计验证工作量，不替代 Stable Original。
- New independent HUMAN-A → Inbox：**0 个**。本轮没有新的独立招聘流程需要写入 Inbox；当前 Inbox 总数仍为 **2 个**，均为 2026-09-21 Afternoon 已通过全历史去重的 backlog。Morning 不分配 `Sxxx`、不创建 Batch。

Morning 重点复核 / 排除：

1. **百度 Agent 后端三面｜`SOLDIER_627`｜2026-09-22 09:13**：本轮 post-specific 原帖 `https://www.nowcoder.com/discuss/931476137576845312` 已恢复为可稳定直接回读，约 42 分钟；面试官明确介绍内部 AI 研发提效平台、Agent 编排 / Workflow、本地与云端开发、动态知识库，随后围绕知识来源 / 更新、关系库与向量库、Milvus 架构、Agent / Skill 项目、端到端耗时、Quality Gate，以及“多 1 分钟换 20–30pp 准确率”的性能—质量权衡持续追问。技术密度与 Role Scope 均成立。但 9/21 Afternoon 已记录同一候选人的百度同招聘流程线索，并明确要求若原帖闭环应与更早百度轮次合并；按“同候选人 + 同公司 + 同流程多轮合并”的当前规则，本轮将它标记为 **same-process merge candidate**，不作为新独立 HUMAN-A、不新增 Inbox / S ID。22:00 全历史回读后再决定如何合并回最早 source。
2. **蚂蚁 9.21 二面｜`Decadeqqq`**：post-specific 原帖与作者主页现在均可稳定核验，连续追 Agent Runtime、Knowledge vs Skills 覆盖、读写鉴权 / 用户确认、Long-task Plan、AI Native 一年 Roadmap、CLI / Skills 暴露、研发—测试—验收流程 AI Native 化、Agent 全托管服务目标、Base Agent 插件化，以及 Tool / Memory / Permission / Agent Loop 插件化。但该作者的 **9.15 蚂蚁一面已正式归档为 `S288`**；公司、作者与招聘 Timeline 明确属于同一蚂蚁流程。因此这是 **S288 的二面 extension / merge candidate**，不是新 Source Count，不进 Inbox、不占新 ID。
3. **度小满 AI 全栈一面｜`SOLDIER_627`**：搜索索引可见约 53 分钟完整基础与工程问法（URL→页面、TCP、HTTP 502/504、301/302、进程线程 / 浏览器多进程、Go GMP、MySQL B+Tree 等），但 direct post-specific 页面本轮仍只返回页面壳；Stable Original 未闭环，继续 zero contribution。
4. **`Decadeqqq` 9.21 帆软一面 / 小红书一面**：作者本人和题序都稳定，但前者主体仍偏通用系统 / Go / DB，仅尾部涉及 Agent Cost 与大仓库幻觉；后者主体是 TNC / CDN / TLS / QUIC / DNS / NAT / Maglev 等网络与流量基础，AI 主要作为开发 / 故障辅助。当前没有稳定证据证明招聘主体属于目标 AI Application / Agent Role Scope，严格排除，避免把“AI 素养扩散”误计为目标岗频率。
5. **4399 Agent 9/18、阿里云 AI 应用、近期快手 / 腾讯等近端线索**：仍主要卡在 post-specific Stable Original / 作者 provenance 或企业聚合；继续追源，不降 Gate。
6. **非牛客平台 / 合集 / 答案 / JD / AI 自动面试**：本轮跨平台结果仍以课程、技术文章、内容整理、招聘页和旧复盘为主；没有新的、稳定可核验候选人本人目标岗 HUMAN-A。

Morning 主要观察：今天两个最强的新证据都不是“新 Source”，而是**同一招聘流程的追问深度继续加深**。百度三面把动态知识库的“自动更新”继续压到知识质量、实际采纳度、Skill Quality Gate 与准确率 / 延迟 Trade-off；蚂蚁二面则把 `S288` 一面的写操作风险 / Harness / Eval 继续推进到 Runtime、权限、CLI / Skills 暴露、组织流程 AI Native 化与 Tool / Memory / Permission / Agent Loop 插件化。这强化了“流程级合并比 Source Count 更重要”的维护原则。只记 Market Observation / merge candidate，不修改 Frozen Canonical、`market/analysis/` 或 Curriculum。

Morning 盲区：17:00 优先补 **SOLDIER_627 百度同流程的更早轮次定位与可合并 source**、度小满 AI 全栈 original、4399 9/18 Agent、阿里云 AI 应用，以及 9/21～9/22 字节 / 腾讯 / 美团 / 快手 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米的新目标岗原帖；继续补非牛客 Candidate First-person 来源。质量门槛不变。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-19 17:52 ～ 2026-09-22 17:52**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline、Role Scope 与全历史去重。Morning 的近端线索可继续追 provenance，但不会用窗口外旧内容补新样本。
- Baseline / full-history dedup：重新读取当前 `main`、`market/README.md`、`market/interview-experience/05-logs/inbox.md`、`market/interview-experience/05-logs/daily-log.md`、两份 Market Policy 与最新 `batch-31.md`；由于本轮有新增候选进入 Inbox，随后**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-31.md` 全历史**。正式基线重新确认仍为 **31 Batch / 291 HUMAN-A / `S001–S291` / 最大 `S291` / 下一 `S292`**。当前根目录仍无 `research/` 一级目录。
- Search effort：Afternoon 新增至少 **140 组定向 Query / Query 变体**，针对 Morning 盲区重点追 `SOLDIER_627` 的百度 / 度小满流程、4399 Agent、阿里云 AI 应用，同时继续覆盖字节 / 抖音、阿里 / 千问、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场；岗位别名覆盖 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `RAG` / `大模型应用开发` / `智能体开发`，并继续补小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等非牛客来源。
- Verification effort：显式打开、回读或追源 **25+ 次** post-specific 原帖、作者主页、企业页、搜索结果和 provenance 入口；这是验证工作量，不等于 25 个唯一 HUMAN-A URL。Search Snippet、企业聚合、二次整理、JD 和页面壳不替代 Stable Original。
- Passed HUMAN-A → Inbox：**1 个新增独立招聘流程：度小满 AI 全栈一面（作者 `SOLDIER_627`，发布 2026-09-20 17:39）**。加上 2026-09-21 Afternoon 遗留的 2 个 backlog，当前 Inbox 共 **3 个**独立招聘流程。Afternoon **不分配 `Sxxx`、不创建 Batch**。

Afternoon 通过项：

1. **度小满｜AI 全栈｜一面｜发布 9/20 17:39**：Morning 尚未闭环的 post-specific 原帖 `https://www.nowcoder.com/discuss/931241025345978368?sourceSSR=post&weFlow=true` 本轮已恢复为稳定可直接回读，并有同源 `https://ac.nowcoder.com/discuss/1677258?type=0`。作者 `SOLDIER_627`，同济大学 2027 Java，净面试时长约 **53 分钟**。题目按真实顺序覆盖：项目最具挑战功能及 Pain Point → 候选人主要做 Backend / Agent、Frontend 参与度 → URL 到页面 / TCP → HTTP 502 / 504 与 301 / 302 → Process / Thread、浏览器多进程 → Go GMP → MySQL B+Tree / Index Invalid → Redis 为什么快及缓存三大问题 → CSS `flex:1`、CORS、前端框架、Debounce / Throttle → AI-assisted Development 的真实 Case、采用度 / 坑 / AI 弱项 → 从 Frontend / Backend、体验、安全与工程角度设计 AI Q&A 功能 → Coding `Restore IP Addresses`，先讲思路再现场编码并运行通过。Role Scope、技术密度与真人现场均成立。
2. **作者真实性 / Timeline**：同一作者当前可稳定串起小红书 Agent 平台、字节 AI 全栈、百度 Agent 后端、度小满 AI 全栈以及此前美团 / 快手等本人招聘流程；不同公司按规则视为独立招聘流程，不因为作者相同跨公司合并。当前账号呈持续个人求职轨迹，不是批量内容号。
3. **全历史去重**：写入 Inbox 前已逐个直接回读 `batch-01.md`～`batch-31.md`，并核验 URL、作者、公司 / 岗位 / 日期、项目语义与连续题序。未发现度小满同公司同流程、当前 URL，或“浏览器 / Network → OS / GMP → MySQL / Redis → Frontend Foundation → AI-assisted Development → AI Q&A System Design → Restore IP”连续链的历史同场来源。GitHub 对标题、URL ID、作者 + 度小满的 0 命中只作辅助，不作为未收录证明。
4. **Backlog 状态**：9/21 Afternoon 已通过的“小红书 Agent 平台研发”和“字节 AI 全栈（飞书）”仍保留在 Inbox；本轮不补发 ID、不提前创建昨天 Batch。22:00 必须基于最新 `main` 再次直接回读全部正式 Batch，并对 3 个 Inbox 候选统一 Finalize。

Afternoon 重点排除 / 合并线索：

1. **百度 Agent 后端三面｜同作者 `SOLDIER_627`**：Stable Original 现已可回读，但这是同一候选人、同一百度招聘流程的后续轮次，属于 same-process merge candidate；不作为新的 Source Count、不新增 Inbox。22:00 重新回读全历史后再判断应合并回哪个最早百度 source。
2. **蚂蚁 9/21 二面｜`Decadeqqq`**：Runtime、Knowledge vs Skills、读写鉴权 / 用户确认、Long-task Plan、CLI / Skills 暴露、AI Native 研发流程与 Tool / Memory / Permission / Agent Loop 插件化都很强，但它是正式 `S288` 蚂蚁一面的同流程二面 extension；不新增 Source Count，不占新 ID。
3. **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：14 道连续题序、作者 Timeline、Harness / 十万级日志 / Agent SQL 验错 / 90% 测试通过率 / AI 真实性验证依旧很强，但 post-specific Stable Original 仍未闭环；继续零贡献。
4. **阿里云 AI 应用开发一面**：企业聚合入口仍能看到 Hallucination、RAG 全流程、两套 RAG 方案比较、MCP、百亿级商品 CRUD / 分库分表、AI Coding / Coding；但候选人 post-specific 原始正文与 Timeline 仍未闭环，企业页不能替代 HUMAN-A provenance。
5. **杭州微链词元等 9/22 新 AI 应用线索**：搜索 / 移动入口可见近期目标岗标题，但 direct detail 仍 Cache Miss，无法核验完整原文与作者 provenance；继续待追源。
6. **欣旺达 9/20 数据开发 AI 面、9/22 数据开发等**：岗位主体为 Data Development 且部分属于 AI 自动面试，Role Scope / Human Interviewer Gate 不通过。
7. **9/19 某小厂前端实习等**：即使会追 Agent、MCP、Skill，岗位主体仍是普通 Frontend；严格按 Role Scope 排除。
8. **NiceOffer / 面灵 / 教程 / “完整答案” / JD / 聚合 / 非牛客内容页**：继续只作发现与市场旁证。本轮小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等没有形成新的、最近 72 小时稳定可核验 Candidate First-person 目标岗来源。

Afternoon 主要观察：**AI Full-stack 继续表现为“完整软件工程底座 + AI-assisted Development + AI Feature System Design”的一体化考察，而不是轻量的前端 + 调模型。** 度小满同一场约 53 分钟把 Browser / Network、Process / Thread、Go GMP、MySQL / Redis、Frontend Foundation 与 AI Coding 实践、AI 问答端到端设计放在一起；这与近期小红书 / 字节的 Agent 平台 / AI 全栈验真形成互补。另一方面，百度三面与蚂蚁二面继续加深同一招聘流程的 Knowledge Quality、Runtime / Permission 与平台化追问，再次说明流程级合并比 Source Count 更重要。以上只进入 Market Observation / merge candidate，不修改 Frozen Canonical、`market/analysis/` 或 Curriculum。

Afternoon 盲区：22:00 优先重新核验当前 **3 个 Inbox 候选**的 Stable Original / Candidate Timeline，并再次直接回读全部正式 Batch做最终去重；继续追 4399 9/18 Agent、阿里云 AI 应用、杭州微链词元、9/21～9/22 字节 / 腾讯 / 美团 / 快手 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米新目标岗原帖，以及非牛客 Candidate First-person 来源。质量门槛不变。

Afternoon 不修改 `market/interview-experience/01-data/`、`market/analysis/` Frozen Canonical 统计或任何 Curriculum 正文。

### 22:00 Evening Search + Finalize — Backfilled 2026-09-23

- Status: completed; this section backfills the 2026-09-22 Evening record that was missing from the rolling log while the formal Market Evidence had already been committed.
- Finalize / full-history dedup：重新直接回读当时全部正式 Batch 后，先将 2026-09-21 已通过 Gate 但漏掉 Finalize 的两个 backlog 独立恢复为 `batch-32.md` / `S292–S293`，再把 2026-09-22 当日正式新增归入唯一日批次 `batch-33.md`。没有把两天来源混进同一个 Batch。
- 2026-09-22 Final additions：**2 个独立 HUMAN-A：`S294–S295`**，分别为度小满 AI 全栈一面与百度 Agent 后端三面；蚂蚁 9/21 二面按同候选人 + 同公司 + 同招聘流程规则合并回既有 `S288`，不虚增 Source Count。
- Three-round search effort：**至少 360 组 Query / Query 变体**；verification effort：**至少 75 次**候选原帖 / 作者页 / provenance 入口的打开、回读或追源尝试。
- Final baseline：**33 Batch / 295 HUMAN-A / `S001–S295`，下一 `S296`**；Inbox 归档后清空。
- Frozen Canonical / `market/analysis/` / Curriculum：日常采集不修改。Finalize 后还修复了 `market/interview-experience/01-data/raw/**` 日常变更误触发 Frozen Market Analysis rebuild 的 Workflow 边界，最终没有保留日常采集导致的 Frozen Analysis 改写。

2026-09-22 主要信号：百度把动态知识库继续追到 Knowledge Quality、实际采纳、Skill Quality Gate 与 Accuracy–Latency Trade-off；度小满 AI Full-stack 则再次表现为完整软件工程底座 + AI-assisted Development + AI Feature System Design。流程级合并继续优先于 Source Count。

---

## 2026-09-23

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-20 10:00 ～ 2026-09-23 10:00**；主动发现只使用窗口内新发布 / 更新，历史页面只用于 provenance、作者 Timeline、Role Scope 与去重。
- Baseline / full-history dedup：重新读取最新 `main`、Market README、Inbox、Daily Log、两份 Market Policy 与最新 `batch-33.md`。在候选进入 Inbox 前，已**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-33.md` 全历史**，确认正式基线为 **33 Batch / 295 HUMAN-A / `S001–S295` / 下一 `S296`**；根目录无 `research/` 一级目录。
- Search effort：至少 **120 组定向 Query / Query 变体**，覆盖字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场，并补小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等平台。
- Verification effort：实际打开、回读或追源 **25+ 次** post-specific 原帖、作者页、企业页与 provenance 入口。
- Passed HUMAN-A → Inbox：**1 个**，上海联蔚数科 AI 工程实习生 / Agent 技术面，作者 `牛客488100460号`，发布 2026-09-21 18:59。Morning 只进入 Inbox，不分配 ID、不创建 Batch。
- Candidate signal：短场中已经直接追 `Harness → Skill vs MCP → Skill/MCP 数量过多 → Knowledge Base → Coding Agent Tool → 无框架 Context Compression / Memory → Multi-Agent`；反问确认团队做 Knowledge Base / Agent、实习工作会参与 Agent 相关调研与开发。
- Typical exclusions：字节广告团队、4399、阿里云等强线索继续卡 Stable Original / author provenance；普通 Frontend / Backend / Data / Test 即使深挖 Harness / Skill / Agent 也按 Role Scope 排除。

Morning 不修改 `market/interview-experience/01-data/`、Frozen `market/analysis/` 或任何 Curriculum 正文。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：继续严格按运行时最近 72 小时；重点补 Morning 的公司 / 平台 / Query 盲区。
- Baseline：正式 Market 仍为 **33 Batch / 295 HUMAN-A / 最大 `S295` / 下一 `S296`**；Morning 候选已经完成过 `batch-01.md`～`batch-33.md` 全历史去重。
- Search effort：本轮新增至少 **120 组定向 Query / Query 变体**；verification effort：**25+ 次**候选原帖 / 作者页 / provenance 入口回读或追源。
- New independent HUMAN-A：**0 个**。Inbox 仍为 Morning 的 **1 个**上海联蔚数科候选；Afternoon 不分配 `Sxxx`、不创建 Batch。
- Stable Original recheck：Afternoon 直接打开同一 post-specific URL 时出现暂时性页面不可读，因此没有提前归档，也没有因单次抓取失败删除已通过候选；明确要求 Evening 再验证 Stable Original 后才可分配 `S296`。
- Typical exclusions：PDD Agent、快手大模型应用、4399、阿里云及多条企业聚合 / Search Cache 结果因为 Stable Original、作者 provenance 或 Role Scope 不完整继续零贡献。

Afternoon 主要观察：Agent / Harness / Skill 已快速扩散到普通软件工程岗位；目标库因此继续收紧 Role Scope，而不是因为新术语出现就扩大统计范围。Frozen Canonical / Analysis / Curriculum 不修改。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：严格按运行时最近 72 小时；继续补字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及 `AI Application` / `AI Backend` / `AI Full-stack` / `Agent` / `RAG` / `Coding Agent` / `Harness` / `Runtime` / `Applied AI` / `FDE` / `大模型应用开发` / `智能体开发`，并继续跨牛客、小红书、知乎、脉脉、博客 / 技术社区补盲。
- Baseline / final dedup：重新读取最新 `main`、Market README、Inbox、Daily Log、两份 Market Policy 与最新 `batch-33.md`，并在分配编号前再次**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-33.md` 全历史**。确认归档前真实基线仍为 **33 Batch / 295 HUMAN-A / `S001–S295` / 最大 `S295` / 下一 `S296`**。
- Search effort：Evening 新增至少 **100 组 Query / Query 变体**；verification effort：显式打开、回读或追源 **20+ 次**近期候选原帖、作者页、企业页与 provenance 入口。
- Stable Original final recheck：上海联蔚数科 exact post-specific 检索在 Evening 再次完整取得候选人正文、作者、发布时间和全部连续题序，Morning 的来源质量结论得到重复验证；没有出现转载、复制链或内容账号反证。
- New HUMAN-A after Evening search：**0 个额外流程**。Morning Inbox 的上海联蔚数科候选最终通过 HUMAN-A + Role Scope + Stable Original + 全历史去重 Gate。
- Final Batch：创建当天唯一正式 `market/interview-experience/01-data/raw/batch-34.md`，分配 **`S296`**；归档后 Inbox 清空。

Evening 重点复核 / 排除：

1. **上海联蔚数科 AI 工程实习生 / Agent｜`牛客488100460号`**：最终归档 `S296`。关键链为 Agent Framework → Harness → Skill / MCP 数量膨胀 → Knowledge Base → Coding Agent Tool → 无框架 Context Compression / Memory → Multi-Agent；反问确认团队与实习工作均直接涉及 Agent。
2. **作业帮 9/23 一面｜`Decadeqqq`**：第一人称与 Agent Evaluation 技术密度很高，追 Tool Idempotency、断连 / 重连续跑、Audit、真实 User Trace、Eval Set、Deterministic Metric、Agent Reviewer 与 Dataset 演进；但同作者此前公开作业帮流程标为 `全栈开发`，当前页面没有新增证据证明招聘主体属于目标 AI Application / Agent，按 Role Scope Gate 排除。
3. **某科技 9/23｜`中二的西红柿起床了`**：作者本人明确写“看似 Agent / AI 开发，实际更像科研助理”，岗位重心是文献调研 / 医疗 AI 研究支持，Role Scope 排除。
4. **4399、阿里云及其它近期高密度结果**：继续受 Stable Original、作者 provenance、Role Scope 或窗口边界限制；企业页 / Search Snippet / 内容整理不替代候选人原始正文。
5. **普通 Backend / Frontend / Test / Data、AI 自动面试、合集 / 标准答案 / 内容号 / JD / 内推 / 新闻**：继续按既定 Gate 排除或仅作市场旁证。

### Final Summary

- Three-round search effort：**至少 340 组 Query / Query 变体**（Morning ≥120 + Afternoon ≥120 + Evening ≥100）。
- Three-round verification effort：**至少 70 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 25+ + Afternoon 25+ + Evening 20+）。
- Final additions：**1 个 HUMAN-A：`S296`**。
- Current formal Market library：**34 Batch / 296 HUMAN-A / `S001–S296`**。
- Next ID：**`S297`**。
- Inbox：归档后清空。
- Frozen Canonical / `market/analysis/` / Curriculum：**本日不修改**；`S296` 只进入后续 periodic canonical mapping / review candidate。

当日主要市场信号：

1. **Capability Scalability 进入基础验真。** Skill / MCP 数量增长后如何 Discovery、如何控制 Context Pressure，已经是短场 Agent 面试可直接追的问题。
2. **Runtime Ownership 继续下钻。** 不使用 Framework 时怎样自己实现 Context Compression 与 Memory，要求候选人真正理解 Harness / Runtime，而不是只会 API。
3. **Agent 术语正在跨岗位扩散。** 作业帮普通 Full-stack 流程也能深挖 Agent Evaluation，因此 Role Scope Gate 必须继续保持严格。
4. **流程级去重优先于 Source Count。** 强题目但 Role Scope / provenance 不闭环的页面继续零贡献。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现**局部饱和 + provenance / Role Scope 成本高**。牛客仍是最容易稳定核验候选人原帖的平台；非牛客渠道当前窗口仍缺新的稳定目标岗第一人称来源。大厂检索持续覆盖，但大量新命中属于普通岗位 AI 素养扩散、聚合 / 内容链、窗口外旧帖或 Stable Original 不足。继续补盲，不降低 Gate。

---
## 2026-09-24

### 10:00 Morning Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-21 10:00 ～ 2026-09-24 10:00**；历史页面只用于 provenance、Role Scope 与去重判断，不拿窗口外旧内容补数。
- Baseline：重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-34.md`；当前正式基线为 **34 Batch / 296 HUMAN-A / `S001–S296` / 下一 `S297`**，Inbox 起始为 0。仓库根目录未出现 `research/` 一级目录。
- Search effort：至少 **75 组定向 Query / Query 变体**，覆盖字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场，并补 `AI Application`、`Agent`、`RAG`、`AI Backend`、`AI Full-stack`、`Coding Agent`、`Harness / Runtime`、`Applied AI`、`FDE`、`大模型应用开发`、`智能体开发` 与牛客 / 小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 等平台。
- Verification effort：显式执行 **20+ 次** post-specific / 候选页 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试；仅搜索摘要、话题聚合、企业聚合或页面壳不视为 Stable Original。
- Passed HUMAN-A → Inbox：**0 个**。本轮没有候选同时满足真人第一人称、高技术密度、目标 Role Scope、Stable Original 与非重复，因此 Inbox 继续为空；Morning 不分配 `Sxxx`、不创建 Batch。由于没有候选进入 Inbox，本轮未触发“候选准入前逐个回读全部历史 Batch”的强制 Gate。

Morning 重点排除 / 待追源：

1. **字节剪映 AI 前端一面（9/22）**：话题聚合可见自研 Agent Framework、为何不用 LangGraph、ReAct Loop、Tool Registry / `tool_call` JSON Schema、本地 Execution 与 Context 追加等连续高密度内容，且标题显示 `ai前端秋招生`；但当前仍只能稳定取得话题聚合，无法取得可重复回读的 post-specific 候选原帖，且 AI 前端是否属于目标 AI Application Role Scope 仍需原帖业务上下文闭环，因此不进 Inbox。
2. **水滴 AI 应用开发一面**：近期第一人称线索存在，但 post-specific 直接回读仍不稳定，当前可见内容也主要是“项目 / 业务深挖”概述，缺少足够连续具体题序；Stable Original / A-grade Quality 均未闭环。
3. **快手 AI 全栈二面**：近期候选人只记录“二面挂、两次面试官均偏后端、被指出后端能力不足”等结果与体验，缺少具体技术问题序列；信息密度不足，不升 HUMAN-A。
4. **作业帮 9/23 `Decadeqqq`**：Agent Evaluation 题链很强，但最新 `batch-34.md` 已明确确认该招聘流程主体为普通 Full-stack，Role Scope 不闭环；继续零贡献，不因问题高级而扩大统计边界。
5. **新浪测开 / 美团 AI 数据开发 / 普通前后端中的 Agent 问题**：分别属于 Test / Data / 非目标软件工程岗位；即使出现 Test Agent、Spring AI、Agent / MCP / Skill，也按 Role Scope Gate 排除。
6. **合集 / 内容号 / 企业聚合 / AI 自动面试 / 标准答案 / 课程与 JD**：只作发现与市场旁证，不贡献 HUMAN-A。小红书 / 知乎 / 脉脉 / CSDN / 掘金 / 博客 / Bilibili 本轮未形成新的、最近 72 小时稳定可核验 Candidate First-person 目标岗来源。

Morning 主要观察：**Agent 技术栈继续向 AI Frontend、Test、Data 与普通 Full-stack 扩散，而“目标岗位 + 稳定原帖 + 高密度题序”的同时满足率继续下降。** 因此本轮保持 Role Scope 与 provenance 双 Gate，不把 Agent 术语本身当作准入依据。字节 AI 前端线索显示自研 Agent Runtime / ReAct / Tool Execution 已可能进入前端方向的项目深挖，但在 Stable Original 与 Role Scope 闭环前仅保留为待追源市场信号。

Morning 不修改 `market/interview-experience/01-data/`、Frozen `market/analysis/` 或任何 Curriculum 正文。

## 2026-09-24 Afternoon

- Discovery window：严格按运行时最近 72 小时，约 `2026-09-21 17:01` ～ `2026-09-24 17:01`。
- Baseline：运行前重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与 `batch-34.md`；在新候选进入 Inbox 前又逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-34.md` 全历史，确认正式基线仍为 **34 Batch / 296 HUMAN-A / `S001–S296` / next `S297`**。
- Structure check：仓库根目录未出现 `research/` 一级目录；历史 Batch / Log 内旧 `research/...` 仅视作历史文本，不作为当前路径。
- Search coverage：在 Morning 基础上补齐字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米与 broader AI Application / Agent 市场；同时覆盖 Nowcoder、小红书、知乎、脉脉、CSDN、掘金等公开入口。本轮新增执行 **80+ 组 Query / Query 变体**，并完成 **24+ 次**候选原帖、作者页、企业 / 话题页或 provenance 入口的显式打开 / 回读 / 追源尝试。
- HUMAN-A pass：**1 个独立招聘流程进入 Inbox**，Morning / Afternoon 均不分配 ID、不创建 Batch。

### Afternoon admitted candidate

- **字节跳动中国交易与广告｜AI 全栈开发工程师｜一面｜作者 `牛客826994329号`｜面试 2026-09-16，发布 2026-09-24**
  - Original：`https://www.nowcoder.com/discuss/932587389027962880?sourceSSR=dynamic`
  - Stable Original / HUMAN-A：post-specific 精确检索可重复取得完整正文；作者主页显示 2027 届研发候选人，并长期记录 PDD、字节、水滴、亚信安全、视源等本人投递 / 笔面 Timeline；正文保留面试官表情、候选人复盘等真实现场状态。
  - Role Scope：标题明确 `AI全栈开发工程师`；反问明确团队在中国区交易与广告业务建设 Agent 能力，并强调 AI 加持下端到端 Full-stack / Business Ownership，属于目标 AI Application / AI Full-stack 范围。
  - Technical chain：AI Pipeline 节点准确性 / Hallucination / Evaluation / Code Generation Quality → Doris vs Hive / ES 与亿级至千亿级数据过滤优化 → MQ 驱动的用户隔离实时轮播 → Redis / MySQL 持久化与一致性 → MQ 幂等 → WebSocket vs Polling / 长连接稳定性 → SQL / Index Design。
  - Dedup：准入前已直接回读 `batch-01.md`～`batch-34.md`。历史 `S036 / S160 / S214 / S246 / S269` 等字节中国交易与广告 / 抖音 AI 来源均为其他作者、日期、项目与连续题序；未发现当前 URL、作者或同一招聘流程。GitHub exact URL / 作者 / 罕见题序搜索 0 命中仅作为辅助。
  - Status：`pending Evening Finalize`；22:00 必须再次直接回读全历史后才能决定是否分配当前真实 next ID。

### Typical exclusions / hold-outs

- **字节剪映 AI 前端 9/22**：话题页可见自研 Agent Framework、ReAct Loop、Tool Registry / JSON Schema / Local Execution 等强问题，但 post-specific 原帖仍不能稳定闭环，且岗位 `AI 前端` 是否满足本库目标 AI Application Role Scope 仍需团队职责原文支持；不进 Inbox。
- **作业帮 9/23 一面｜`Decadeqqq`**：Agent Idempotency、Reconnect、Audit、Trace、Eval Set、Deterministic Metric、Agent Reviewer 等问题很强，但招聘主体仍无法证明属于目标 AI Application / Agent 岗；按 Role Scope Gate 排除。
- **携程 AI 应用开发 9/3 面试、9/21 15:51 发布**：技术链很强且原始页面可检索，但到本次 Afternoon 运行时已超出最近 72 小时发现窗口约 1 小时，且 Morning 未进入 Inbox；本轮不以过窗内容补数。
- **阿里云 / PDD 等近期“面经-05 / 面经 06/07/08 / 完整答案”**：批量多场整理、付费 / 答案化包装或内容账号，继续零贡献。
- **9/23 `看似 Agent 实际科研助理`、新浪测开等**：岗位主体落在科研助理 / Test 等 Role Scope 外方向；不因出现 Agent 术语放宽 Gate。
- 非牛客渠道本轮仍未形成新的“最近 72 小时 + 候选人本人 + 稳定原文 + 目标 Role Scope + 高密度连续题序”来源；继续视为平台盲区，不用二次文章或招聘 JD 补数。

### Afternoon signal

- **AI Full-stack 的真实考法继续向“AI Pipeline Quality + 大规模数据工程 + Realtime Backend”合流。** 新候选不是只问 Agent 名词，而是要求同时证明模型链路准确性、代码生成质量、数据选型 / 性能优化、消息实时链路、一致性、幂等与连接稳定性。
- **Role Scope 与 Provenance 成本继续上升。** Agent / Harness / Eval 术语已经扩散到普通 Frontend / Full-stack / Test / Research Support；必须继续依赖岗位主体、团队职责、作者 Timeline 与 Stable Original，而不能按关键词计数。
- Frozen Canonical / `market/analysis/` / Curriculum：**本轮不修改**。
- Afternoon state：正式 Market 仍为 **34 Batch / 296 HUMAN-A / next `S297`**；Inbox **1**。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：继续严格限定运行时最近 72 小时，约 **2026-09-21 22:00 ～ 2026-09-24 22:00**。
- Baseline / full-history dedup：在正式编号前重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 Batch，并**逐个直接回读 `market/interview-experience/01-data/raw/batch-01.md`～`batch-34.md` 全历史**。确认归档前真实基线为 **34 Batch / 296 HUMAN-A / `S001–S296` / 下一 `S297`**。
- Search effort：第三轮新增至少 **100 组 Query / Query 变体**，继续覆盖字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米及更广 AI Application / Agent 市场，并补牛客、小红书、知乎、脉脉、博客 / 技术社区入口。
- Verification effort：第三轮显式完成 **20+ 次** post-specific 原帖、作者页、企业 / 话题页和 provenance 入口的打开、回读或追源尝试；部分入口发生 Cache Miss / 页面壳，不以摘要替代原文。
- Evening new independent HUMAN-A：**0 个**。第三轮没有发现第二个同时通过 HUMAN-A + Role Scope + Stable Original + 全历史去重的新招聘流程。
- Finalized Inbox：Afternoon 唯一候选 **字节跳动中国交易与广告｜AI 全栈开发工程师｜一面** 再次完成全历史去重。Evening direct post-specific 出现暂时性 Cache Miss，但当天 Afternoon 已重复取得稳定完整正文，作者个人招聘 Timeline 与当前帖子标题仍可核验，且没有出现复制 / 转载反证，因此维持 Stable Original 结论并正式归档。
- Final Batch：创建当天唯一 `market/interview-experience/01-data/raw/batch-35.md`，分配 **`S297`**；归档后 Inbox 清空。
- Frozen boundary：本日只维护 Market Evidence；**不修改** `market/interview-experience/01-data/`、Frozen `market/analysis/` 或任何 Curriculum 正文。

Evening 重点排除 / 待追源：

1. **字节剪映 AI 前端一面（9/22 发布）**：话题层可见自研 Agent Framework、LangGraph 取舍、ReAct Loop、Tool Registry、`tool_call` JSON Schema、本地执行与 Context 回填等强链路；但 post-specific 原帖 / 作者 Timeline 与 AI Application Role Scope 尚未同时稳定闭环，继续待追源。
2. **携程近期 AI 面试复盘**：明确属于 AI 自动面试，不满足 Human Interviewer Gate。
3. **`林小白zii`、`AIGC小白入门记` 等内容 / 付费链**：技术密度不覆盖 provenance 缺陷，继续零贡献。
4. **算法 / SFT / RL / 模型训练、Test / Data / 普通 Backend / Frontend 岗**：仅出现 Agent / MCP / Skill / AI Coding 不足以通过 Role Scope。
5. **宁德时代工业 Agent 近端线索**：真人招聘痕迹存在，但公开技术题序过短、信息密度不足。
6. **企业聚合 / Search Snippet / JD / 内推 / 题库 / 完整答案 / 二次整理**：只用于 Recall 和市场旁证，不贡献 HUMAN-A。

### Final Summary

- Three-round search effort：**至少 255 组 Query / Query 变体**（Morning ≥75 + Afternoon ≥80 + Evening ≥100）。
- Three-round verification effort：**至少 64 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 20+ + Afternoon 24+ + Evening 20+；这是工作量次数，不代表 64 个唯一 URL）。
- Final additions：**1 个 HUMAN-A：`S297`**。
- Current formal Market library：**35 Batch / 297 HUMAN-A / `S001–S297`**。
- Next ID：**`S298`**。
- Inbox：**0**。
- Canonical / Frozen Market Analysis / Curriculum：**本日不修改**。

当日主要市场信号：

1. **AI Full-stack 正把 AI Pipeline Quality 与传统大规模系统工程合成同一套能力模型。** Node Accuracy、Hallucination / Deviation、Code Generation Quality 会和 Doris、超大数据过滤、MQ、Cache / DB Consistency、WebSocket、SQL / Index 同场出现。
2. **Evaluation 更靠近真实业务链。** 不只问“有没有评测”，而是分别追代码生成质量、业务知识准确性、节点质量和端到端结果怎样验证。
3. **Realtime Backend 与 Agent 产品体验继续合流。** 用户隔离 MQ、最近 N 条状态、幂等、WebSocket / Polling 与长连接稳定性进入 AI 全栈直接考察。
4. **Agent 技术继续向其它岗位扩散，Role Scope / Provenance Gate 需要继续收紧。** 剪映 AI 前端等线索技术内容很强，但边界与原始证据未闭环前不计正式频率。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现 **局部饱和 + 高 provenance 成本**。牛客仍最容易取得稳定第一人称线索，但 post-specific Cache Miss、内容账号、答案化页面和普通岗位 AI 深挖占比高；字节剪映 AI 前端仍是最值得继续补原帖 / 作者 Timeline 的近端线索。腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客渠道，在当前窗口内没有形成第二个完整通过 Gate 的新独立流程；继续补盲，但不降低 Gate。

---

## 2026-09-26

### 10:00 Morning Search

- Status: completed（本次 run-now 在约 09:43 本地时间启动，按 Morning 阶段执行）。
- Discovery window：严格使用运行时最近 72 小时，约 **2026-09-23 09:43 ～ 2026-09-26 09:43**。
- Baseline：首先读取最新 `main`、Market README、Inbox、Daily Log、两份 Market Policy 与最新 `batch-35.md`；根目录无顶层 `research/`。出现准入候选后，分 4 组**逐个直接回读 `batch-01.md`～`batch-35.md` 全历史**。按正式 `## Sxxx` 条目重新核算：35 Batch / 297 HUMAN-A / 最大 `S297` / 下一 `S298`。
- Search effort：至少 **50 组 Query / Query 变体**，覆盖字节/抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO/vivo/小米，并覆盖 Agent / AI Application / RAG / AI Backend / AI Full-stack / Harness / Runtime / Coding Agent 等岗位叫法；同时补牛客外平台检索。
- Verification effort：显式打开、回读或追作者 / provenance **28+ 次**；稳定取得 post-specific 正文的候选再继续做作者 Timeline 和全历史去重。
- Passed HUMAN-A → Inbox：**4 个独立流程**：① 小红书 Product Engineer（AI 与全栈方向）社区工程一面；② 迅雷 Agent 一面；③ 百度搜索 AI 全栈（偏前端）一面；④ 字节 Agent 开发后端日常实习一面。
- Morning 阶段：**不分配 `Sxxx`，不创建 Batch**；正式 Market 仍为 35 Batch / 297 HUMAN-A / next `S298`。

Morning 典型排除：vivo Agent 9/22 虽质量合格但已超当前 72h 发现窗口；阿里淘天最新帖存在逐题答案化 / 内容包装风险；美团近期 AI 全栈目前只有企业聚合层，原帖与作者 provenance 未闭环；批量内容号 / 答案链、AI 自动面试、普通 Backend / Frontend / Test / Data 岗仅出现 Agent 术语均继续零贡献。

Morning 主要市场信号：

1. **RAG 正从“讲流程”继续下沉到 Retrieval Quality Engineering**：检索策略选型、Recall bad case、Chunk / overlap、BM25+Vector、RRF、Cross-Encoder 与 Domain Mismatch 开始被连续追问；
2. **AI Coding / Skill 开始进入团队级工程约束**：不仅问“用不用”，还问 progressive loading、CLAUDE.md 与跨 Coding Agent 的规范一致性；
3. **Agent Memory / Intent Routing 开始要求量化与冲突处理**：意图正确性、置信度、历史方案复用 vs 新方案选择成为现场问题；
4. AI Full-stack 继续把 React/Vue、Cache、限流、异步、并发等 Foundation 与 Agent / RAG 同场验证，不能弱化传统工程基础。

本轮只维护 Market Evidence；Frozen Canonical、Frozen `market/analysis/` 与 Curriculum 不修改。



---

## 2026-10-07 批量补采与历史Inbox恢复

- Baseline：最新main `6799b2e615aa77bd0928100876a7cda65f10636c`；35 Batch / 297 HUMAN-A / next S298；9/26 Inbox实有4条
- Scope：跨平台批量补采，不冒充严格最近72小时的日常三次监测；历史来源单列，未证实年份与发帖/面试日期分开记录
- 检索：公共网页181个去重查询字符串（主扫描76、公司补盲55、小红书公开发现42、交叉追源8），与小红书站内8个宽查询及2个身份定向查询分开计；重复滚动/作者主页不再当新query累加
- 原帖核验：去重后160个详情URL尝试；132个正文完整读取。牛客87个尝试/80个完整，另7个未完整；小红书73个详情尝试/52个完整，另21个仅正文或技术图未读完
- 小红书可见/已读noteID最低212个；这不是212篇已核验面经。52个完整原帖中11篇含原图，共47张原图逐张读取；图片数不等于来源数
- 公开目录另发现30个小红书链接线索，未独立贡献HUMAN-A；未宣称平台穷尽
- 原始采集记录103张，杰尼龟原帖明确两公司分场形成104个审核分流项。最终新收54个独立流程：牛客32、小红书22；其中7个历史补录单列
- 同流程6张后续轮次原帖合并至4个Real流程；S144/S036/S293/S294的跨平台重发及S176原帖不重复计数
- 未准入：24条待核验、13条明确未准入；这些是已建审核记录的分流计数，不是所有搜索结果的排除总量
- 恢复：9/26旧Inbox四条均于今日重新打开原帖，归入唯一恢复Batch 36，S298–S301；不再计作今日新发现
- 今日新批：Batch 37，S302–S355；S287另回并同作者字节秋招二面，新增Source为0
- Final：37 Batch / 355 HUMAN-A / S001–S355；next S356；Inbox 0
- 质量边界：私密/已删除原帖不以缓存补入；普通后端/算法/数据岗位即使Agent题很强仍须岗位Gate；不能按平台或AI题占比区别准入。题序项含自介、反问和未披露占位，不报告虚增的技术题数
- Frozen Canonical / market/analysis / Curriculum：不修改；235 ACTIVE Canonical仍保持既有冻结口径

覆盖明细：[coverage-2026-10-07.json](coverage-2026-10-07.json)。保留与去重：[review-holds-2026-10-07.md](review-holds-2026-10-07.md)。新的每日采集已启用，从2026-10-08起约北京时间19:00运行，首次执行尚未核验；这不改写旧每日三次计划及历史断更事实。


---

## 2026-10-07 既有小红书图片线索补查收口

- 上节保留初版归档快照；本节为同日增量，不重新发现21个URL，不增加公共网页查询或站内宽查询计数
- 范围：初版21条待图线索全部分类。19整帖完整回读；另2条已有充分排除证据即停止，未读取/未闭环图不冒充已读；待分类队列0
- 裁决：6个新增独立流程、5条保留、8条排除、2条同文/跨平台重复。6个来源为sword百度、又又百度、多吃碳水科大讯飞及小红书、悲伤土豆鸡肉饭快手、zed字节；全部对照S001–S355及彼此完成URL/账号/流程/连续题序检查
- 编号：原图补查追加同日Batch37的S356–S361；不新建同日Batch38。三轮/多轮仍合为一个Source
- 最终新发现：60个独立流程（牛客32、小红书28，含原有单列7个历史补录）；另外恢复9/26旧Inbox4个。S287只补同流程二面，新增0
- 最终库：37 Batch / 361 HUMAN-A / S001–S361；next S362；Inbox0。待核29条、明确未准入21条，另5条既有Source重复、6条合轮卡、2条对应保留主流程的重复卡
- 覆盖合并：181个去重公共查询、站内8个宽查询/2个身份查询不变；160个不同原帖详情尝试不变。完整回读132+19=151，其中牛客80、小红书52+19=71；牛客7条未完整，小红书2条未完整且已按证据排除
- 图片：初版47张加本次86张完整映射的原图共133张；磁盘替换图、加载截图与重复文件不计新原图。cris资料帖10个文件映射不全、ttf仅读1/4图，均不计整帖回读
- 原图保真：sword原编号缺28/29不补；又又为编辑器故障改口述，不认定算法不会；科大讯飞作者遗忘的RAG/Bug细节不补；快手按原图主题顺序、重复追问只记一次；zed原文URL缓存不改成LRU，开源自荐不转成面试题
- 复制链：炒肉多两平台112项逐序相同，周也帖是一面1–25同文子集；新增均为0，未认定谁复制谁，所对应牛客主流程归属仍待核
- 派生索引：raw-term-candidates.md按原有tools/build_gap_candidates.py同步，为可复现召回辅助表，不是正式Canonical Evidence。生成器、workflow、冻结/人工维护分析、235 ACTIVE Canonical与Curriculum均未改

覆盖及逐项裁决见[覆盖账本](coverage-2026-10-07.json)、[审核保留项](review-holds-2026-10-07.md)。以上是广泛多轮检索和限定队列补查结果，不宣称两个平台绝对无遗漏。


### 第二轮遗漏复查：2026-10-07 UTC / 北京时间10-08凌晨

在用户确认合并PR46后，继续按原HUMAN-A准入规则补查遗漏。开始时main为`7d69e2fd73af3c69100a5a866f0e31aaa7157654`，37批/361流程；本轮是10/7大扫描任务续查，实际北京时间已跨日，仍延长Batch37，不另建重复日批次。

- 正式新增：25个独立流程，S362–S386；牛客9、小红书16。累计正式库386个/37批，下一编号S387
- 既有来源补充：S123、S280、S294、S295、S329、S333，共8条候选记录并入6个Source。S123/S333未能证明独立投递，保守补充且明确不确定性
- 本轮唯一原帖尝试130条，实际完整回读115条；牛客44/50、小红书71/80。下载成功、可达页面和搜索卡不代替完整阅读
- 与首轮原帖按ID去重后，整个任务累计尝试288条、完整回读266条；两轮都完整读过0条，未直接把轮次工作量相加
- 本轮公共检索记录86条，按文本规范化去重86条；其中额外公司检索前32条为执行目标回填，不能冒称原始请求日志。小红书11个主查询文本/12个排序组合，另1次同帖恢复检索；重复滚动不增加查询数
- 候选记录裁决：25准入、8旧来源补充、36保留、33排除、2重复、6原图访问阻塞。完整回读的排除项仍记工作量，但不计正式来源
- 小红书80条固定原帖队列均已分类：71完整图文、1只完成部分图片即排除、2正文明确转载/合集提前排除、6原图未完成。原139张卡片中90张未打开，作为下次缺口，不能声称全平台穷尽
- 验证码：官方滑块正常尝试3次仍未通过，停止重试；6条未读图片不补造题目。仍观察到登录账号入口，不将验证码等同登录失效

关键去重：周也4399图文逐号对应S316，零新增；九方智投找到更早牛客原作者小红不是绿/369008148，RFF误写、第13题感受和题序相同，只收当前公开可回读的原作者一个流程。相同昵称的账号分别核ID；海尔/安克同一账号的本人归属仍待证。赛文X本轮13个公司流程及额外转转共14条沿用历史来源排除，未因技术密度越过来源Gate。

新增涵盖2024商汤、2025广州历史原帖和2026或年份未明样本；发布日期、面试日期、届别及推断年份逐条区分。原编号、原小节和无编号追问位置保留，作者答案与感想不改造成题。序列项包括背景、反问和未披露占位，未把其合计宣称为技术题数量。

详见[第二轮覆盖账本](coverage-2026-10-07-round2.json)及[审核记录](review-holds-2026-10-07-round2.md)。本次仅维护Market证据与既有脚本生成的raw-term召回辅助索引；Frozen Canonical、正式频率/冻结分析、Curriculum和JD均未改变。


---

## 2026-10-08 已审核增量归档（草稿审阅分支）

- 远端main基线仍为`7d69e2fd73af3c69100a5a866f0e31aaa7157654`，361个流程/37批；上一日分支`3fc678d792a84181a6214a57555e09dc894a4ce0`已有25个新增及6个旧来源补充。
- 本日只追加13个已独立审核流程，Batch38 / S387–S399：牛客9、小红书4。前三项为抖音电商三轮、中兴原图补核、经纬恒润；后十项为追加复查。
- 分支合计399个流程/38批，下一编号S400；相对main新增38个，未合并前不声称main已更新。
- 抖音电商三轮仍一个Source，四组题面占位不展开；作者推断、反问及现场反馈独立保留。中兴原号1–11和react原拼写、经纬恒润PPT工作流纠正及无手撕保留。
- AI王朝一/二面合并且不把答案扩为问题；ZeroDay不补原缺号5/13；武汉HR+技术合一个流程且技术原7复合问不拆；火山原文无号，60为编辑短记项而非原题数。
- 天津9/1、武汉5/20原文未明示年份，不沿用采集卡推定2026年；火山原文明示2026/08/14予以保留。发布/编辑时间不替代面试日。
- HOLD、排除、同流程补充均新增0；两条部分图片线索读完后仍保留，未因图读完自动准入。未宣称搜索平台穷尽。
- 只维护Market原始证据、覆盖日志及既有raw-term召回索引；Frozen Canonical仍235 ACTIVE，冻结频率、课程、JD、代码和工作流均不改。

详见[Batch38](../01-data/raw/batch-38.md)、[本日覆盖账本](coverage-2026-10-08.json)及[保留记录](review-holds-2026-10-08.md)。


---

## 2026-10-08 第二次有限增量采集

- main核验基线081c287：399流程/38批。发布依赖架构迁移PR48，基于其分支，不宣称main已更新或合并。
- 先核旧Inbox（0）和未归档保留项，再检索新候选。最终新增2个历史原帖独立流程：牛客DeepWisdom/Sora1016、 小红书Unity中国/MeGuMin，S400–S401追加同日Batch38；当前分支401流程/38批，next S402，Inbox0。
- 牛客44条公开查询，8个原帖13次直取，5个本日完整正文；另2个壳页、1个访问失败。21项审核记录：1准入、5待核、7重复、8排除。
- 小红书dot云端登录/站内搜索/原帖正文验证成功；4个站内查询，7个原帖尝试，其中4个主帖完整、另2个部分核验、1个受限。OSAKO正文4图读完，置顶二面评论附图未读，不补二面。7条记录：1准入、4待核、2排除；末条访问异常300017，一次刷新无效后停止该站。
- Unity公开跨平台去重另3条查询，不把查询无命中作为唯一去重依据；38批399流程全文比对并回读相似题链，两条独立复核通过。
- 新来源发布日期分别只显示06-12、07-30；都不是今日面试日期，年份及真实面试日保持未知。DeepWisdom二面仅状态；Unity原7转写不清、14/17/20业务说明/复盘/反馈不贡献技术频率。
- 只更新market面经数据、准入契约、记录裁决和原有脚本生成的分析；课程/JD/root interview/匹配规则/验证器不改。market派生已重建。完整检查因10个root interview证据块未获授权同步而失败，不为全绿越界；相应补丁留待另行许可。

见[覆盖账本](coverage-2026-10-08-round2.json)及[逐项保留/排除](review-holds-2026-10-08-round2.md)。有限范围结果，不宣称平台穷尽。


### 2026-10-08 11:56 UTC起：完成9条复核并更正覆盖

- 两平台登录、站内搜索与原帖读取均实际验证。牛客5条原帖4条完整、1条明确删除；小红书4条原帖全部可读，补完金山8图和OSAKO置顶二面图。
- 原9项不再以待核交付：浪潮与东成机电2条通过独立复核，S402–S403追加Batch38；另7条逐项写明排除本批理由，未指控虚假或断言重复。
- 更正：上轮小红书300017是相邻帖子链接参数误配，不能称平台封锁；牛客yzxcxy旧HTML为壳页，上轮5条完整更正为4条已证实完整，不推断删除时间。
- 浪潮原文没有新增题干，改判来自纠正旧质量判断：6条明确追问已满足原政策，不确定的LRU推测/HashMap残缺继续不计技术频率。
- 当前403流程/38批、next S404、Inbox0；PR49累计新增4流程（牛客2、小红书2）。两条新档24序列项，17技术记录，不作原子题总数。
- 原有401流程与既有来源保全不变；只更新market面经。10个root自动证据块仍待范围许可，因此完整--check及1项生成一致性测试仍失败。

[逐条复核结论与更正](reverification-2026-10-08.md) / [结构化复核](reverification-2026-10-08.json)。

## 2026-10-08 精简架构重放说明

保留403个正式流程的完整原始资料与全部核验纠错。旧规则分析及root自动证据同步已退出现行工具；上述历史派生指标与检查差异不再是现行生成口径。新机械核验只确认原文哈希、来源链接、稳定ID和结构记录计数，不作语义判断。


## 2026-10-09 每日有限增量（独立草稿分支）

- 开始时重新核远端main `84a22babd7738f431d75eba7ce75fdeeaf062627`，PR48/49已合并；403来源/38批，Inbox0。PR52是独立JD工作，不占面经编号。
- 正式新增2个独立流程：S404中科曙光AI Agent一面（牛客），S405虾皮Agent一/二面合1（小红书）。同日只建Batch39；当前分支405来源/39批，next S406，未合并前不声称main已更新。
- 正常云端浏览器验证两平台登录、搜索、原帖与必要作者记录。主候选11个不同原帖完整回读：牛客4、小红书7；小红书18张主帖原图，图片/评论/跨平台不扩大流程数。两平台各3个站内查询文本，查询排序组合分别4/5；有限已加载结果，不宣称穷尽。
- 2准入、9个原帖排除本批：火山两平台4帖缺独立于飞书转业务流程的证据；Nolo2帖缺稳定雇主/流程边界；小鹏1帖逐序对应S321；理想1帖岗位职责未闭环；Soldier字节二面1帖未指向飞书或广告既有流程。未以待核交付，也未断言排除者虚假。
- 保留实际披露日期、原题序及追问/答案边界；50个新增序列项不等于50道技术题。仅原始证据、哈希契约、机械索引与日志计数变更，现有语义分析快照不改。
- 现行面经机械检查与24项单元测试通过；远端PR/CI结果另在Draft PR中核实。

逐项来源、访问状态、排除所缺必要事实和去重依据见[本日采集记录](collection-2026-10-09.md)。

## 2026-10-20 每日真人面经增量（独立 Draft PR）

### 结果、基线与范围

- 正式新增2个独立招聘流程，统一放入[Batch40](../01-data/raw/batch-40.md)：S408百度百科Agent Harness一面；S409小红书AI应用工程师一面。当前分支407来源/40批/408区块，16个新增编辑序列项；其中包含反问、未披露难点和求职状态问题，不称16道技术题。未合并前main仍为405来源/39批。
- 2026-10-20重新读取main `22138c509757c892bbb45e2855268530a99a8ee4`、完整tree、全部PR和分支。open PR为0、closed PR为80，唯一分支main；较昨日仅4个JD自动扫描文件变化，面经和政策未变。恢复并逐blob验证96个任务文件，其中39批原始资料完整；未有当天批次或占号。
- 已读现行HUMAN-A、Role Scope、模型复核边界、契约、来源保全、现有日志与Inbox。正式基线S001–S405，405来源、406区块、6206结构记录；Inbox当前0。对全部正式资料进行身份/URL/题链召回，完整审读百度22个、小红书31个相关区块；具体差异随原始来源保存。不是仅凭搜索未命中准入，也未重做全量语义分析。
- 旧任务的未发布S406/S407原件、URL与身份仍未恢复；它们不在正式契约和计数内。保留这两个空号，不重用、不伪造恢复；新的S408/S409已对完整可用正式历史去重，但无法断言与已丢失未发布材料绝无重合。这个证据缺口不等同已有正式来源重复。
- 本轮直接任务要求独立分支Draft PR、用户审阅前不得merge，与仓库日常直接main流程不同，按本轮要求交付真实原始增量。PR80仍为机器人关闭且未合并；只含未完成日志的PR保护未改。本轮有真实准入数据，不重建纯失败日志PR。

### 正常浏览器实际覆盖

- 先复核昨日未归档的百度候选，再查昨日理想候选，然后新增搜索。牛客使用 `理想智能应用研发一面`、`AI Agent 面经` 两个正常站内查询；小红书使用 `百度Agent Harness 女面试官`、`AI应用开发 面经` 两个正常站内查询。只核实际已加载结果，不声称穷尽最近三日、所有平台或所有未归档线索。
- 小红书正常已登录。3篇主候选全部正文和5张图片完整读取：百度1/1图、虾皮3/3图、小红书AI应用1/1图；另1篇作者背景全文及1张无题干生活图。合计4篇全文、6/6张图，没有部分图片计作完整。读取19条真人评论：百度15/15、小红书AI应用4/4，均至THE END；虾皮及背景帖显示无评论。3个作者主页目录用于归属核验，不计额外面经来源。
- 牛客2篇原帖均实际出现登录弹窗，全文未完成；不读取弹窗后的遮挡内容作为完整证据，不关闭原帖门槛或换路绕过。搜索卡仅用于定位，平台自动题量、自动总结与AI配图不算面试证据。
- 没有启用仓库采集器、网络脚本、接口重放、代理或用户本地电脑。小红书搜索自动出现的AI面板被关闭，未把答案或摘要作为原文。

### 逐项裁决

R01｜百度百科｜27届秋招呱呱🐸（蔚来黑子版）｜准入S408

原帖：https://www.xiaohongshu.com/explore/6ad03fba0000000019031a66

账号69c1d4bb000000002600244b。昨日保全候选今天重新读全文、唯一岗位流程图、全部15评论及主页。当前发布显示5天前 重庆；图片投递日2026-10-08不是面试日。作者确认一面、约70分钟、无手撕、次日查看流程结束。Multi-Agent→并行文件冲突→共享数据通信→工具编排→RAG语义切分→压缩保真→百科配图场景及两项反问，具体原顺序、作者答案和未知日期均在Batch40保留。S032/S275/S367等虽有部分共同概念，但作者/时间背景/岗位与连续链不同，未发现已收同流程。

R02｜小红书｜淡淡就顺顺｜准入S409

原帖：https://www.xiaohongshu.com/explore/6ac901c30000000014002b53

账号5f2f5d28000000000101fd54。正文、1张封面及4评论完整，显示编辑于10-09 广东，年份和实际面试日未披露。本人40分钟一面，开发项目20分钟、手撕20分钟；4个项目复合问、最长无重复子串及复杂度、其他offer询问依序保留，作者未公开答案。评论确认被拒、约两三天出结果。作者主页和下述背景帖支持本人求职记录；不把未命名的其他公司失败经历与小红书硬合并。S382的TinyBERT/评测/分层记忆链及其他近邻不构成同流程证据。

辅助背景：https://www.xiaohongshu.com/explore/6ab625bf000000000b0054b9

作者同上，标题为秋招阶段性总结，编辑于09-25。完整正文说明本人从八月初投递、不同算法/研发岗位匹配情况；1张生活图和无评论状态已核。只作作者背景，不单独计来源，不凭此推断小红书具体部门或招聘日期。

E01｜虾皮Agent开发一面｜person｜排除本批

原帖：https://www.xiaohongshu.com/explore/6ad5a8d6000000002a0267f9

账号69a62dfb000000001d01ec68。发布显示1天前 上海。正文仅标签，3/3图片共20项整理题单完整读取：Agent/Workflow选择、ReAct、Tool Message、记忆、压缩、RAG父子索引/混检/更新、多模态、训练名词、Redis/MQ/MySQL、链表、重试、意图稳定、Prompt灰度、排障、评测和反问；未披露本人回答、面试现场经历或申请流程，页面无评论。作者简介是更新大模型知识，主页可见携程等题单。不能仅凭标题或题干中的第二人称证明作者就是候选人。本批缺的是可核第一人称及独立招聘流程，不断言虚假，也未把共同问题认定为已证实转载；零贡献正式题目。

E02｜理想智能应用研发一面｜同尘去｜本批全文核验未完成，排除

实际打开的官方链接：https://www.nowcoder.com/discuss/941713098040221696?sourceSSR=search

账号451293820；搜索卡显示昨天00:11。正常打开原帖后显示登录弹窗，缺完整正文、实际日期/轮次上下文及必要作者流程证据。卡片里的AI Coding片段不作完整面经；不把访问受限报告为合格候选不存在。

E03｜字节AI Agent全栈开发面经｜ZESHAWN_｜本批全文核验未完成，排除

实际打开的官方链接：https://www.nowcoder.com/feed/main/detail/88e22e99028942bcbac1ed57395f2e60?sourceSSR=search

账号171466012；搜索卡显示今天03:49。打开原帖后同样存在登录弹窗；缺完整正文、必要图片和第一人称招聘流程核验。没有提取遮挡后的题单，不以平台自动解析的20题作为实际题数。

### 保全与检查边界

只新增Batch40，并机械追加provenance、contract、sources、raw-manifest；同步既有daily-log、Inbox和两处当前计数。旧39批原始文件、旧406个完整来源区块、既有模型审阅快照与问题归并、课程、JD、代码和workflow保持原样。现行403来源/6156记录分析快照不重建；本次16结构项进入快照外待月度处理范围。正式库来源数按实际ID集合取407，不取最大编号409。

发布前再次核main及并发PR，保全与离线检查结果、远端commit及CI真实终态记录于本次Draft PR；不手动启动runner或dispatch。

## 2026-10-21 每日真人面经增量（更新现有 Draft PR）

### 本日结果与基线

- 本日首次正式准入4个流程：S410淘天AI应用研发一面、S411新凯来AI Agent开发一面、S412华为AI应用同日三轮、S413字节AI应用全栈日常实习一面，统一[Batch41](../01-data/raw/batch-41.md)。共87个结构序列项，不称87道技术题；不把三轮、两项投递、图片或评论计为独立流程。
- 实时main为`22138c509757c892bbb45e2855268530a99a8ee4`；全部open PR仅PR81，仍open/draft、未合并，head为`f8f8bd5351d9638340e70a7446d9783bf5483f98`。main405来源/39批，PR81已含昨日S408/S409共407来源/40批/408区块/6222结构记录。未发现当天批次或编号占用，追加后当前分支411来源/41批/412区块/6309结构记录，next S414。未合并前不改写main的来源数。
- 重新读现行HUMAN-A、Role Scope、模型复核边界、契约、原始历史、现有日志与候选；任务相关main96个及PR81的97个文件全部与远端Git blob匹配。先处理旧淘天、新凯来候选，再作新发现核验。对完整407个正式来源/408区块作身份、URL与题链召回并全文复核近邻；不重建语义归并、频率或备考成品。
- S406/S407仍是原件及URL缺失、从未发布的旧标签，不在正式来源计数内；不重用、不虚构恢复。与完整可用正式历史完成去重，与不可恢复未发布原件的未知重合无法作保证。未知材料缺口本身不是已有正式重复，不能据此永久拒绝可独立核验的新来源。
- 本轮任务允许在自身PR81安全追加本日Batch41。该要求与仓库日常直接main流程不同，遵照本轮独立Draft PR交付、用户审阅前不合并。PR80纯日志关闭保护保持原样；本次为4份真实原始准入增量，不重复创建纯未完成日志PR。

### 实际平台与正文覆盖

- 使用dot云端正常浏览器；小红书已登录且可正常搜索/原帖/原图/评论。4个不同站内查询依次为`10.12淘天AI应用研发一面`、`新凯来 AI Agent开发工程师`、`AI应用 面经`、`字节AI应用全栈一面`。读取默认正常结果，整理时另重复一次淘天查询以校验疑问边界；只作有限本日覆盖，不称穷尽全部近期帖子。
- 小红书4份目标原帖全文、4/4张配图、74/74条真人评论全部读取（淘天23、新凯来35、华为7、字节9），包含折叠回复，均至THE END。另2份辅助帖全文、2张配图、48/48评论（阿里45、字节投递3）。总计6篇全文、6张必要原帖图片、122评论；没有部分正文或未读图片冒充完整。评论中的无关营销配图未另开，不作为原帖题干或额外图片完成量。公开主页核验3个作者，不计额外面经来源。
- 牛客先正常搜索`理想智能应用研发一面`，再试`AI Agent 面经`。前者原帖实际显示登录弹窗，后者搜索页也出现登录门槛后停止。仅1篇原帖打开尝试、0篇全文；第二次搜索卡没有逐帖打开，不算额外核验或排除数。没有读取遮挡正文、关闭原帖门槛、换路规避限制，也没有把平台自动总结、题量或AI配图作为原文。
- 首次导航误把页面相对href交给goto，返回URL无效；随后取同一可见链接的绝对href正常打开，才看到牛客登录门槛。前者是参数错误，不虚记成平台访问拒绝或绕过成功。未使用用户电脑、仓库采集器、网络抓取脚本或接口重放。

### 逐项裁决

R01｜Real｜淘天｜旧未归档候选，准入S410

https://www.xiaohongshu.com/explore/6acf187a000000001a028c66

正文原20项依序保留，涵盖Coding Agent完整调用、缓存/历史上下文、工具重复调用、压缩及项目/时序知识图谱/模型选择。作者评论明确秋招、无手撕；时长、结果和面试年份未披露。全历史联合121区块/120来源全文审读后确认同作者阿里/淘天正式来源为0。本次首次计1个，不要求先证明与全部从未准入旧线索均属不同投递；未证实与旧4.7淘天的关系，后续补齐时须保守合并核验。不能把已收其他公司的相同候选人或复用项目误当本公司流程重复。

A01｜Real｜8.25/8.26阿里控股旧帖｜仅流程辅助，不独立准入

https://www.xiaohongshu.com/explore/6a900250000000001f01e975

发布显示08-27，未显示年份。全文自述分两天笔试/面试，保留3项笔试、19项面试的存在作为审读事实，但作者明确使用AI合并知识点，不能声称这是原现场逐题顺序。实际内容与作者回复均以传统后端八股为主，缺足以证明目标AI应用实质范围的证据；与本日淘天的部门/独立投递关系也未说明。本批不给第二个ID、不把它当已正式收录淘天的重复凭证；45评论与1封面只支持辅助核验。

R02｜山田リョウ｜新凯来｜旧未归档候选，准入S411

https://www.xiaohongshu.com/explore/6aca0fa7000000001403b5b4

发布显示10-10，实际面试日未披露。11项编辑顺序保留RAG项目→混合召回→cross-encoder→效果→未展开的小模型项目→挫折→未披露题干的编码。作者明确开发方向、单摄像头线上一面约50分钟，手撕没写出来但自认为思路正确，随后获知通过。主管面原定20号线下但改期，仅安排不计已完成轮次。83个正式历史近邻全文核验没有同流程/复制证据；与S301等只有公共概念相似。

R03｜Real｜华为｜新发现，准入S412

https://www.xiaohongshu.com/explore/6ad85d9f000000002b00e343

发布昨天23:37 湖北，标题面试日10.20不补年份。武研所同日一面、二面、主管面合成1流程；作者评论说明质量与流程IT，称中午查到进池而非offer。按三轮顺序保留15项编辑短记，唯一具体作者答案是受提示后改用滑动窗口处理x/点号题；组合总和仅自述快速完成。与S229/S327的日期、背景和连续题链不同，不因同雇主就合并。

R04｜烧灯续昼｜字节｜新发现，准入S413

https://www.xiaohongshu.com/explore/6ad84c85000000002c01c27d

保留原41项顺序，Python/HTTP/应用诊断→AI长任务及压缩→本人长期记忆项目的图字段/共享/本地模型/截图触发/冲突/评测→后缀最小值编码主题→反问。完整正文加作者9评论确立本人日常实习一面、部分没答上来、非剪映；没有公开答案或完整算法题。发布显示昨天22:24，搜索卡6小时前，封面OCT21，记录显示差异，实际面试日仍未知。新两篇合计54个历史完整近邻已复核，无相同身份或连续事件题链证据；不能仅凭昵称零命中准入。

A02｜烧灯续昼｜字节投递记录｜仅流程辅助，不另计来源

https://www.xiaohongshu.com/explore/6ac8e7f3000000001c02d2f7

发布显示10-09 江苏。全文/1张已打码投递图/3评论；作者说上一次生活服务后端HR联系时自己拒绝，近期有两条投递，其中一项可见Agent全栈实习。无本篇面试题，不把HR联络、拒绝或投递数量算面试流程；没有证据把R04硬配某项申请，打码内容不尝试识别。

E01｜同尘去｜理想智能应用研发一面｜登录限制，排除本批

实际打开官方链接：https://www.nowcoder.com/discuss/941713098040221696?sourceSSR=search

搜索卡账号451293820、时间10-19 00:11。原帖登录门槛阻止完整正文和作者流程核验，缺的是全文及实际岗位/题序/轮次背景，不断言内容虚假或没有新增。搜索摘要不能代替原文；本轮正式库零贡献。后续搜索也遇登录门槛，没有宣称牛客采集完成。

### 保全与验证边界

只增加Batch41，机械追加来源凭证、契约、sources、raw-manifest，并同步本日志、Inbox及两处当前计数。旧40批原文、408个区块和昨日PR81全部增量逐字节保全；403来源/6156记录的模型快照不改，本次87结构项只加入快照外原始范围。提交前重新读取main、所有open PR及自身branch head，以当时远端head作安全lease；具体检查、提交和CI终态在PR81说明中核验。若CI仍是base已有JD布局错误，只报告原因，不越界修改。
