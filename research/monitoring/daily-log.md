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
