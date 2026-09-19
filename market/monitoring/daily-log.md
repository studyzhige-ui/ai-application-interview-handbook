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
