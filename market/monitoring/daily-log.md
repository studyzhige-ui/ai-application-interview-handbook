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

Afternoon 不新增 Canonical，不修改 Curriculum，也不写入 `interview/canonical/`、`market/analysis/` 或任何 Curriculum 正文。

### 22:00 Evening Search + Finalize

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-16 22:00 ～ 2026-09-19 22:00**；主动发现只使用窗口内新发布 / 更新，历史页面仅用于 provenance、作者 Timeline 与全库去重。
- Baseline / full-history dedup：重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-29.md`，随后再次**逐个直接回读 `batch-01.md`～`batch-29.md` 全历史**。确认正式基线为 **29 Batch / 288 HUMAN-A / `S001–S288` / 最大 `S288` / 下一 `S289`** 后才执行最终编号。晚间运行中 `main` 相对开始时前进 5 个提交；compare 确认这些并发变更只涉及 `market/jobs/` 与 `tools/`，没有修改 `market/monitoring/` 或 `market/interviews/`，因此基于最新 HEAD 安全重放。根目录复核仍**没有 `research/` 一级目录**。
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

Morning 不修改 `interview/canonical/`、`market/analysis/` Frozen 统计或任何 Curriculum 正文。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-17 16:58 ～ 2026-09-20 16:58**；主动发现只使用窗口内新发布 / 更新，历史页面只用于 provenance、作者 Timeline 与全历史去重。
- Baseline / full-history dedup：重新读取当前 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-30.md`；由于本轮出现可进入 Inbox 的候选，随后**逐个直接回读 `market/interviews/batch-01.md`～`batch-30.md` 全历史**。正式基线确认仍为 **30 Batch / 289 HUMAN-A / `S001–S289` / 最大 `S289` / 下一 `S290`**。根目录复核仍无 `research/` 一级目录。
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
- Baseline / full-history dedup：重新读取最新 `main`、`market/README.md`、Inbox、Daily Log、两份 Market Policy 与最新 `batch-30.md`，并在分配任何编号前再次**逐个直接回读 `market/interviews/batch-01.md`～`batch-30.md` 全历史**。确认归档前正式基线仍为 **30 Batch / 289 HUMAN-A / `S001–S289` / 最大 `S289` / 下一 `S290`**。晚间运行期间 `main` 又前进 6 个提交；compare 确认并发变更只涉及 `.github/workflows/`、`market/jobs/` 与 `tools/`，没有修改 monitoring / interviews，因此基于最新 HEAD 安全重放。根目录再次复核，**没有 `research/` 一级目录**。
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
- Baseline：重新读取当前 `main`、`market/README.md`、`market/monitoring/inbox.md`、`market/monitoring/daily-log.md`、两份 Market Policy 和最新 `market/interviews/batch-31.md`。当前正式 Market 基线为 **31 Batch / 291 HUMAN-A / `S001–S291` / 最大 `S291` / 下一 `S292`**，本轮开始时 Inbox 为空；仓库根目录复核仍**没有 `research/` 一级目录**。由于本轮最终 **0 个候选进入 Inbox、0 个 ID 分配**，未触发“准入 / 编号前逐个直接回读全部历史 Batch”的写入前 Gate；若 Afternoon 有候选达到准入线，必须先直接回读 `batch-01.md`～`batch-31.md` 全历史。
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

Morning 不修改 `interview/canonical/`、`market/analysis/` Frozen Canonical 统计或任何 Curriculum 正文。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：严格按运行时最近 72 小时，约为 **2026-09-18 17:00 ～ 2026-09-21 17:00**；主动发现只使用窗口内新发布 / 更新，历史页面只用于 provenance、作者 Timeline、Role Scope 与全历史去重。
- Baseline / full-history dedup：重新读取当前 `main`、`market/README.md`、`market/monitoring/inbox.md`、`market/monitoring/daily-log.md`、两份 Market Policy 和最新 `batch-31.md`；由于本轮出现可进入 Inbox 的候选，随后**逐个直接回读 `market/interviews/batch-01.md`～`batch-31.md` 全历史**。重新确认正式 Market 基线为 **31 Batch / 291 HUMAN-A / `S001–S291` / 最大 `S291` / 下一 `S292`**。根目录复核仍没有 `research/` 一级目录。
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

Afternoon 主要观察：**Agent / AI Application 的工程验真正在进一步呈现“规则遵从 + 生产链路 + Foundation”三层同场。** 字节新候选不只问 Agent / Skill，而是追模型不遵守 Skill 约束时怎样提高规则优先级，再把同一场切到海量视频 OOM、断点续传 / 清理、SQL 端到端性能和传统数据结构；小红书 Agent 平台则直接用 10 万 QPS 商品详情与缓存新鲜度验证平台候选人的 System Design。前沿 Agent 能力没有替代传统工程底座，而是和它一起被验真。该信号只进入 Market Observation，**不修改 `interview/canonical/`、`market/analysis/` Frozen 统计或任何 Curriculum 正文**。

Afternoon 盲区：22:00 应重新核验当前 2 个 Inbox 候选的 Stable Original 与作者 Timeline，并再次直接回读全部历史 Batch 做最终去重；继续追同作者百度 Agent 后端三面 / 度小满 AI 全栈的 post-specific 原文，以及 4399、阿里云、腾讯 AI 全栈、携程 / 快手等近端高价值线索。质量门槛不变。
