# 批次采集与排除记录

[← 采集日志](README.md)

以下仅保留原批次的采集事实、未准入记录和去重处理；当时数量属于历史日志，不能代替当前分析。研究观察、冻结题库计划与课程安排已移除。

## batch-01 · 本轮明确排除 / 去重

来源：原批次第 148–162 行。

Batch 11 主动扩大了平台和历史月份召回，但以下内容继续保持 **零贡献**：

- 京东后端 Agent 的 04-30 与 05-08 两篇文章出现几乎逐题一致的 12 道问题，当前无法可靠确认哪一篇是真正候选人原场次，因此整条重复链均不进入正式库；
- 滴滴花小猪某 Agent 面经的评论区直接出现“复制粘贴别人的帖子”质疑，无法通过非转载 Gate；
- `AIGC小白入门记`、面经专栏、含“思路参考 / 标准答案 / 完整解析”的内容型页面；
- Mock Interview / AI 自动面试 / 自动生成题库；
- 个人博客中的模拟面试、一般求职感想、低信息密度 Interview Reflection；即使作者真实，也不满足本项目高密度技术面标准；
- 普通后端 / 前端岗位仅顺带使用 AI Coding，无法证明实际职责属于 AI Application / Agent 的场次；
- 只有搜索摘要、标题或截图，无法稳定打开正文的线索；
- 字节 04-08 同时出现后端 Agent 一面 / 二面近似流程，但无法稳定确认作者关系，本批只保留证据更明确的一面，不擅自合并也不重复计数；
- 不同 URL 但题序 / 项目描述高度相同的后发版本继续按语义重复处理。

## batch-02 · 本轮明确排除 / 去重

来源：原批次第 334–349 行。

Batch 09 搜索量继续扩大，但以下内容保持 **零贡献**：

- WeThinkIn / RockyDing、“三年面试五年模拟”、面灵 AI、卡码笔记、CSDN / 51CTO / 2048AI 等题库、答案、整理、路线或 SEO 内容；即使它们引用真实面经，也只能用来回溯候选人原帖，不能直接贡献问题；
- 同一份“5 年经验大模型应用开发、多家公司面试”在 CSDN、51CTO、AtomGit、财经站等处的大量跨站转载；
- “林小白zii”一类按公司聚合几十场面经的合集账号 / 汇总帖，只作索引，不作为候选人本人场次；
- 带“思路参考 / 完整答案 / 真题解析”的二次内容；
- 只有标准化问题列表、缺少面试日期 / 轮次 / 状态 / 互动等现场证据的帖子；
- AI 自动面试 / 模拟面试；
- 普通后端岗位仅因标题或一两个问题带 AI / Agent 字样，但无法证明实际 Role Scope 的场次；
- 同一候选人的字节 AI 全栈 9/1 一面与 9/8 二面合并为 S161，一个流程只计一次；
- 字节 Agent 后端 S164 存在题序高度相似的另一版本，只保留有明确二面与横向淘汰结果的来源；
- 同花顺 S166 / S167 经企业页核验为不同账号 / 学校的两位独立候选人，因此不错误合并；
- 小红书 S028 优先保留作者个人博客原文，牛客同步页只作为跨平台回溯证据。

## batch-04 · 本轮明确排除

来源：原批次第 499–509 行。

本轮扩大搜索时，以下内容即使“题很多”仍未进入正式 Batch：

- CSDN / AtomGit / 聚合面试站中“必杀技、满分答案、高手解析、学员复盘、题库导航”等二次内容；
- 搜索摘要显示为真实面试，但正文无法稳定打开或无法确认候选人本人身份的帖子；
- 与已有来源题序、措辞高度一致的重复转载 / 二次发布；
- 自动 AI 面试、纯算法训练、大模型训练 Infra、传统数据分析 / BI 等非目标岗位；
- 目标岗位标题虽然正确，但正文明显以“标准答案提示”而不是候选人面试过程为主体的内容。

## batch-05 · 本轮明确排除

来源：原批次第 441–454 行。

本轮为了扩大 Recall 搜索了大量企业页、话题页、作者页和跨平台索引，但没有降低 HUMAN-A 门槛。明确排除了：

- 同一账号短时间批量发布大量不同公司的“面经 + 标准答案 / 付费专栏”内容，无法确认候选人本人；
- “帮粉丝复盘 / 群友投稿 / 学员上岸”类二次转述，即使问题很完整也不计真人第一人称；
- 去哪儿等正文直接附逐题标准答案、真实性与原始现场边界被二次加工污染的内容；
- 只有企业页 / 话题页摘要而找不到稳定原帖的线索；
- 9 月 8 日百度 AI 测开等虽然包含 Agent / LangGraph / Skill，但岗位属于测试开发，不通过 Role Scope Gate；
- 9 月 8 日快手一面等虽然问到 Skill / Memory，但原帖无法稳定确认目标岗位名称，不以“碰巧问 AI”代替岗位准入；
- 传统后端 / 普通算法岗，仅因简历中出现 Agent 或 AI Coding 而被零散追问的场次；
- 与 `S001–S074` 已有来源为同一场、同一原帖或高度一致的跨页面重复。

## batch-07 · 本批清洗与研究观察

来源：原批次第 391–396 行。

本批正式新增：**16 个 HUMAN-A（S042–S128）**。

---

## batch-07 · 本轮明确排除 / 去重

来源：原批次第 698–711 行。

本批搜索量继续扩大，但以下内容仍然 **零贡献**：

- 2026-04-02 一篇与 03-21 小红书社区工程 AI 与全栈题序几乎逐条一致的后发帖子：按重复处理；
- 阿里灵犀同一套题的后续高度相似版本：只保留更早、正文稳定的 04-03 来源；
- 哔哩哔哩原帖之后出现的“含完整答案 / 三年面试五年模拟”二次整理与跨站搬运；
- 迅雷“服务端开发(AI)”等页面：虽然题目看起来很贴目标方向，但正文已混入答法 / 方法论，并位于“AI-Agent 面试实战”内容链，不能作为 HUMAN-A；
- 小米 / 月之暗面等付费或内容创作者型“面经”页面，正文无法稳定核验候选人本人和完整现场；
- 凌脉等技术问题覆盖很漂亮但正文过于模板化、候选人本人现场痕迹不足的帖子；
- 字节剪映等只能从搜索列表看到标题 / 摘要，却没有稳定原帖 URL 的线索；
- Role Scope 外的普通后端、测试 / 测开、纯训练算法岗位，即使顺带出现 Agent 名词也不计。

## batch-08 · 本轮明确排除 / 去重

来源：原批次第 373–387 行。

本批扩大 Recall 时，以下内容继续保持 **零贡献**：

- 同一 AI 面经内容账号在短时间连续发布字节 / 阿里 / 快手 / 算法 / Infra 等大量“真人叙事”帖子，同时经营付费专栏 / 简历项目内容；即使单篇写了“挂 / 过”，跨帖模板化和商业内容链导致候选人本人真实性无法可靠确认；
- DeepSeek Harness、字节 Agent、得物 Agent 等带“思路参考 / 标准答案 / 完整回答”的内容型帖子；
- “三年面试五年模拟”、RockyDing / WeThinkIn、面经总结、企业题目聚合等二次整理；
- 宇树科技 Agent 等题目非常对口但正文几乎是标准化问题清单、缺少轮次互动 / 答题状态 / 结果时间线的帖子；
- CVTE 另一篇虽然现场感很强，但正文只记“项目追问 + Vibe Coding”等少量泛信息，具体技术问题密度不足，不进入正式库；
- AI 自动面试 / 模拟面试；
- 匿名公司、岗位无法稳定确认，或只有搜索摘要无法核验正文的线索；
- 普通后端 / 测开 / 纯训练算法岗位仅顺带问一两个 Agent / RAG 问题的场次；
- 腾讯 AI 应用 03-21、03-23 与 S155 题序高度相同的后发版本，只计重复信号；
- 同候选人的淘天二面 / 三面、Token Foundry 三轮均按一个招聘流程保守计数。

## batch-12 · 本批清洗与研究观察

来源：原批次第 103–114 行。

本批正式新增：**10 个 HUMAN-A（S045–S208）**。

后续维护补充：Batch 13 搜索中发现 `S027` 同一候选人的 8 月 17 日小红书 Agent 二面，已按同一招聘流程合并回 `S027`；来源总数不因此增加。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## batch-12 · 典型排除

来源：原批次第 115–126 行。

- **拼多多提前批 AI Agent 一面复制链**：`328260668ec94ebda5c84de205d13a58` 与 `d0c1a59663a2408fb9f8b52b87ccaaec` 来自不同账号、发布时间相差约一天，但题序、项目语义和措辞高度一致；无法可靠确认真正原场次，按规则整链排除，不猜原作者。
- **快手 AI 应用 / Agent 开发 9 月内容链**：正文由内容账号持续生产，并出现订阅 / 付费墙、同一叙事多版本扩写；即使问题漂亮也不进入 HUMAN-A。
- **CSDN / Agent 社区学习路线、107 道题、完整答案 / 面试“必杀技”**：属于教学、SEO、题库或二次整理，全部零贡献。
- **只能从搜索摘要 / 聚合页看到标题或片段的跨平台结果**：无法稳定核验候选人本人和原始正文，排除。
- **月之暗面 AI-Native Desktop 三轮题单**：Role Scope 匹配且问题很有价值，但正文缺少足够明确的候选人第一人称现场状态 / 面后结果，本批按保守标准不纳入正式统计。
- **字节 9.3 Agent 开发**：Batch 12 当时因单页现场 / 招聘流程证据不足而暂缓；Batch 13 沿作者主页补齐连续秋招时间线后升级为 HUMAN-A `S076`。这属于补证后升级，不是降低准入门槛。
- **京东 5.8 后端 Agent 等边缘候选**：题目本身有价值，但当前能确认的现场 / 招聘流程证据仍不足，继续不进入 HUMAN-A。

---

## batch-13 · 本批清洗与研究观察

来源：原批次第 106–117 行。

本批正式新增：**12 个 HUMAN-A（S047–S212）**。

同时完成一项存量修正：小红书 `S027` 同一候选人的 8 月 17 日二面被作者后续补发，已并入 `S027`，不新增来源数量。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## batch-13 · 典型排除

来源：原批次第 118–127 行。

- **AIGC小白入门记内容账号链**：同一账号短时间连续发布快手、阿里等多家公司“真人叙事”，并进入订阅 / 付费专栏；无法把这些页面当作独立候选人原始面经，全部零贡献。
- **去哪儿 AI 全栈 / AI 应用的自动 AI 面**：页面明确描述 AI 面试官根据候选人关键词自动追问，即使题目覆盖 MCP / Memory / Harness，也属于 AI 自动面试，按固定规则排除。
- **平安科技 Agent 开发“完整答案型”页面**：正文大段直接给出标准化方案 / 答案，不满足候选人本人真实现场复盘标准，排除。
- **阿里 AI 全栈标准题单、推荐区“思路参考 / 标准答案”内容**：缺少足够候选人现场痕迹或属于教学化整理，不能因题目高级而入库。
- **跨平台 / 推荐页摘要**：只能看到搜索摘要而无法回到稳定原文的线索继续保持零贡献。

---

## batch-14 · 典型排除

来源：原批次第 155–167 行。

- **B 端小公司 Agent / 法本信息 AI Agent 复制链**：`5733bf8605d44262a596ad7ba738e737` 与后发法本页面的前十余题几乎逐题同序同措辞；虽然发布时间不同，但无法可靠确认真正原始候选人，按规则整链排除，不猜“更早就是原帖”。
- **阿里控股 9 月 AI 全栈内容账号链**：作者主页显示数百篇高频多公司发布、明显私域 / 订阅导流和批量面经生产特征；即使题目很前沿，也不能当独立候选人原始经历。
- **AIGC小白入门记 / NiceOffer / 面灵 AI / 各类面试宝典**：属于付费内容、二次整理、聚合、标准答案或内容化生产，继续零贡献。
- **去哪儿 AI 全栈 AI 自动面**：明确由 AI 面试官自动追问，即使包含 MCP / Memory / Harness，也不属于真人面试。
- **美团 9 月 AI 全栈付费墙页面**：只能稳定核验部分正文，剩余内容需订阅 / 单篇购买，无法完整验证上下文，因此排除。
- **快手 4/9 AI Agent 页面**：搜索结果能看到高质量题目和“已过”，但本轮无法稳定打开完整正文，按“摘要不能入 HUMAN-A”规则排除。
- **汇川 AI 全栈 8 月场次**：岗位匹配、题目也足够多，但正文更像标准化题序，候选人现场 / 结果痕迹弱于本批正式样本，暂不硬收。
- **同一作者多家公司合集帖**：即使作者本人可信，只要单页混合多家公司且无法干净划分独立场次，就不以合集形式正式计数。

---

## batch-15 · 本批清洗与研究观察

来源：原批次第 203–212 行。

本批正式新增：**8 个 HUMAN-A（S217–S224）**。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## batch-15 · 本批在分配 ID 前删除的重复来源

来源：原批次第 213–225 行。

1. **拼多多 2026-07-25 AI Agent 线下面试**：候选 URL `45f6e73...` 已在历史 `S061` 正式入库，删除。
2. **京东 2026-05-07 AI Agent**：虽 URL 不同，但与历史 `S185` 的 ThreadLocal → RPC/HTTP → 限流 → RAG → Agent vs Workflow → AI Coding 题序和语义高度一致，无法证明独立原场，删除。
3. **Moka 2026-04-27 后端 AI 应用**：虽 URL 不同，但与历史 `S181` 的 Video Progress Redis → Hash/TTL → RabbitMQ Delay → Memory → MCP/SSE 追问链高度一致，删除。
4. **字节 2026-08-06 AI 应用开发**：URL `15af3788...` 已在历史正式来源中出现，删除。
5. **影石 2026-03-11 Agent 开发**：URL `f9c5e9f...` 已在历史 `S187` 正式入库，删除。
6. **米哈游 2026-04-24 Agent 研发**：发现更早 2026-04-09、不同作者的同公司页面，SFT → Attention / RNN → Workflow vs Agent → Memory → MCP → Few-shot → Sandbox → AI Code Testing → LRU 几乎逐题同序；无法证明 4/24 页面是独立原场，因此不进入正式 Batch。

上述来源在本批正式编号前即被剔除，**不占用 `Sxxx`，因此本批连续编号为 `S217–S224`。**

---

## batch-16 · 本批清洗与研究观察

来源：原批次第 153–162 行。

本批正式新增：**8 个 HUMAN-A（S225–S230）**。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## batch-16 · 典型排除 / 去重

来源：原批次第 163–175 行。

- **去哪儿 AI 自动面试**：即使问题覆盖 Agent / MCP / Memory / Harness，面试官不是人，继续零贡献。
- **`AIGC小白入门记`、`赛文X`、RockyDing / WeThinkIn 等内容链**：批量多公司叙事、付费 / 订阅、标准答案或二次整理特征明显，不能作为候选人本人原始场次。
- **米哈游 4/9 与 4/24 Agent 研发近似逐题复制链**：此前已发现 SFT → Attention / RNN → Workflow vs Agent → Memory → MCP → Few-shot → Sandbox → AI Code Testing → LRU 基本同序，原场归属仍不够可靠，本轮继续整链不新增。
- **快手另一篇 Harness / RabbitMQ / Security 深挖帖**：作者本身看起来真实，但当前页面无法稳定确认具体目标岗位，Role Scope 证据不足，本批不正式收录。
- **小鹏 Agent 开发 15 题页面、百度某 20+ 题 Agent 页面**：题目很对口，但单页结构过度标准化、候选人现场 / 招聘状态证据弱于本批正式样本，保守排除。
- **菜鸟物流智能体、部分 Agent 算法 / DeepSeek Harness 页面**：要么第一人称现场不足，要么岗位更偏模型 / 算法或内容型整理，不因题目“高级”降低 Gate。
- **同一候选人快手 AI 全栈一面 + 二面**：明确同作者同公司连续流程，合并为 `S228`，不按两个 URL 虚增来源。
- **同一作者字节 `S225` 与淘天 `S230`**：不同公司、不同时间、不同招聘流程，按规则分别计为独立真人命中。

---

## batch-17 · 本批清洗与研究观察

来源：原批次第 154–163 行。

本批正式新增：**11 个 HUMAN-A（S231–S235）**。

---

> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。

---

## batch-17 · 典型排除 / 去重

来源：原批次第 164–177 行。

- **某中厂 Agent 应用开发实习候选页**：初筛时第一人称与问题密度看起来合格，但最终复核阶段正文连续无法稳定打开，只能依赖搜索摘要。按“搜索摘要不能代替稳定正文”规则，最终撤出本批，不占编号。
- **卓驭 Agent、自变量 Agent 平台、平安银行 AI 开发、浦发 AI 开发等 `赛文X / 100+ 社招面经记录` 内容链**：单页表面像真人面经，但作者 / 合集链具有批量多公司内容生产特征，全部零贡献。
- **蚂蚁若干不同账号同序 Agent 帖**：Memory / Agent Team / MySQL / Redis / MQ 等题序高度重合，无法可靠确认独立原场，继续整链排除。
- **9/8 快手一面（Skill / Memory / 项目真实性追问）**：现场痕迹很强，但页面无法稳定证明具体招聘岗位属于目标 AI Application / Agent Role Scope，不因出现 Skill / Memory 就越过岗位 Gate。
- **BIGO Java Backend**：同一真实候选人的 Agent 项目被深挖，信息质量高，但招聘岗位本身仍是普通 Java Backend，缺乏足够证据证明岗位职责属于目标 Role Scope，本批不收。
- **去哪儿 AI 自动面试**：问题再贴 Agent 也不是人类面试官，继续零贡献。
- **AIGC小白入门记、RockyDing、WeThinkIn、Yuka 完整答案等内容 / 付费 / 二次整理页**：继续排除。
- **快手 `S114` 三轮**：明确同作者、同公司、同 `CR Agent`、连续 8/26 → 9/1 → 9/9，只计一个来源。
- **灵犀互娱 `S235` 三轮 + Timeline**：明确同一招聘流程，只计一个来源；但与同作者的快手 `S114` 属于不同公司流程，分别计数。

---

## batch-18 · 本批典型排除 / 重复案例

来源：原批次第 123–133 行。

- **后发复制 / 导流**：`https://www.nowcoder.com/discuss/905861577826463744`，07-12 发布，19 道 Coding Agent 问题与 `S236` 07-07 原帖几乎逐题同序，并夹带 PDD 内推链接；排除后发链。
- **历史语义重复**：07-14 字节 AI 应用开发 `https://www.nowcoder.com/feed/main/detail/3e22dc2df03d4227ab70ea9c2d896086` 真人痕迹很强，但“Agent 模块 / API 异常自恢复 / Token → 线程池重设计 → JVM 类加载 → MySQL 三日志 / 两阶段提交 → 合并数组”的连续题序与历史 `S192` 高度重合；不新增。
- **内容账号 + 付费墙**：09-04 淘天 Agent 业务场景帖 `https://www.nowcoder.com/discuss/925525428259885056` 作者为专栏型账号，正文约 60% 被付费墙截断，无法完整稳定核验；排除。
- **模板化但第一人称不足**：安软 AI 应用开发实习 `https://api-cdn.nowcoder.com/feed/main/detail/40920533fad14136bff01c3928c7e953` 虽题量大、元数据完整，但正文高度结构化，缺少候选人答题状态 / 追问 / 结果 / 现场互动，无法稳定证明是候选人本人第一人称原始面经；排除。
- **推广型“精品面经”**：字节火山方舟 Managed Agent 候选正文夹带 Agent 题库 / GitHub 项目推荐，整体呈内容推广包装；在无法排除内容账号属性前不纳入。
- **低密度**：微博智搜、游戏小厂 AI 全栈等虽有真人现场，但仅 5～7 个高度概括的问题且缺少足够连续追问，质量不稳定，本批不为凑数放行。

---

## batch-19 · 本批典型排除 / 重复案例

来源：原批次第 219–231 行。

- **内容账号 Gate：拼多多复活赛 Agent 一面** `https://www.nowcoder.com/feed/main/detail/2109cf8eb0254507911fbf86bcbf51e4`，技术题非常强，但作者 `赛文X` 同时经营“100+ 社招面经记录 / 订阅内容”生态。当前规则明确要求非内容账号，因此编号前撤出。
- **快手多版本复制链**：7/30 `https://www.nowcoder.com/feed/main/detail/8ef62dcdde1340f987507d2d1e1433a8` 的“父子索引 → BM25 → Rerank Top-K → 限流 → RAG Eval”题序，继续追到 2/9 一二面 `511a8021...`、3/20 `f4567cec...`、4/9 `7ce89f...` 等多个高度同序版本；无法可靠确认 7 月页为独立场次，整条不确定链不收。
- **美团精确重复**：9/2 AI 后端 `https://www.nowcoder.com/feed/main/detail/9b94f595d15148869e0334029b5ddb67` 已是历史 `S011`；不因近期重新进入热门结果而重复编号。
- **腾讯精确重复**：AI 应用 `a02baa2ac6634904992561494a1746a4` 已是 `S045`；WXG Agent / Coding Agent `3ffc762437274543b6a8f5e2ea6fb535` 已是 `S130`。
- **字节精确 / 语义重复**：TikTok Agent、App Infra、9/3 Agent 等热门结果均已在历史 Batch；另有 Seed / 专栏式页面存在答案化、付费或内容包装，继续零贡献。
- **阿里云后发扩写**：09-07 页面与 `S244` 的 SGX / EPC / PV / Coding 题序高度一致却加入大量额外高级题，无法证明为独立候选场次，排除后发链。
- **OPPO 明确转载**：`953daca379ac40d58a813b972175dc87` 明写“帮转”，只保留 `S245` 原作者页面。
- **美团疑似分享账号**：`398d270fc3eb407ca2341007cd13a1b2` 虽题量足，但作者以“继续分享最近面经”方式持续发布，评论还出现把美团误称腾讯的异常内容信号；当前无法稳定确认候选人本人，排除。

---

## batch-20 · 本批典型排除 / 重复案例

来源：原批次第 79–90 行。

- **OPPO 历史语义重复**：8/13 `cf5a82411c1e473385d8fcae6c250a6e` 与历史 `S128` 的 `920830730643443712` 几乎整段同序，包括“段落切 Chunk → 证据不足拒答 → Multi-Agent → Long/Short Memory → HTTP Status Code → Hallucination → Frontend → 页面卡顿 → 首次面试”连续链；不论是同作者多 URL 还是复制链，都不新增。
- **小红书 OpenManus 高相似链**：8/9 `223fa82f...` 的“业务指标 → Agent 实际使用 → OpenManus → Harness → Multi-Agent 并发 → Long/Short Memory → ReAct Planner/Executor/Critic”与历史 `S027` 高度重合，无法证明独立，排除。
- **滴滴疑似复制 / 混编**：AI Agent Backend `17ee6ae95cc44ec19b9eefadb69da6b3` 后半段“Redis 单线程 / ZSet / Sentinel / BigKey → Channel vs Mutex → Go 调度 → 实时模糊搜索 → 二维码登录 → 服务发现”与 `S110` 快手原场形成长连续同序链，不能因为公司标题不同就视为独立，排除。
- **腾讯正文不稳定**：4 月 AI Backend `db9014c0dcad4d4d985427e330dc1461` 技术密度很高，但原始正文最终无法稳定完整打开，主要依赖 Search Cache；按硬 Gate 排除。
- **抖音电商同作者相邻双帖**：`925065999378829312` 与 `S246` 同作者、同公司 / 业务且发布时间仅相差约 1 分钟，但题序不同、流程关系无法确认。为避免错误合并或双计，本批只保留能独立成立的 `S246` 页面；相邻页零贡献。
- **内容账号 / 付费包装**：热门搜索中仍有同一账号短时间批量发布快手 / 美团 / PDD 等“完整面经”并伴随付费墙、答案化包装的结果，继续零贡献。
- **历史精确重复**：美团 9/2 AI 后端等结果已是旧库正式来源；热门结果重新出现不新增编号。

---

## batch-21 · 本轮扩大搜索的典型排除 / 重复案例

来源：原批次第 260–273 行。

- **Code Search 0 命中但历史已收**：阿里平头哥 4/28 候选在辅助 Code Search 中没有直接命中，但重新直接回读历史 Batch 后确认就是历史 `S118`；再次证明不能把“0 命中”当未收录证据。
- **拼多多历史精确重复**：7/25 提前批线下 AI Agent 两轮原帖 `45f6e73f8e9d4888b9c066a160f89f60` 已是历史 `S061`，不新增。
- **同候选人同公司后续轮次**：`想奋斗的柠檬精天天摸鱼` 的腾讯 4/27 页面已经是历史 `S020`；同公司相邻后续流程不因为出现新 URL 就重复计数，也不反向修改历史 Batch。
- **作者级复制风险**：账号 `星轨偏差` 的腾讯 5/3 页面虽然 URL / 作者不同，但“Minimum Path Sum → Java Interface/Abstract Class → StringBuilder/Buffer → synchronized → DI → HashMap → MyBatis → 熔断限流 → Kafka → Slow Query → EasyExcel 1 万行 / 第 5000 行失败恢复”的长题序与历史 `S232` 几乎整场一致。该账号其它新候选（如京东）因此进入高风险 Provenance 状态，本批全部不收。
- **正文稳定失败，即使 Search Snippet 很强也不收**：蚂蚁国际 4/21、京东 5/3、快手 4/30 等若干候选在搜索结果里题目很强，但重新打开原始正文时只剩壳页 / Internal Error / 极少行，按 Verifiable Gate 排除。
- **美团同作者同公司相邻双帖**：`脆片温柔` 4/7 与 4/14 两条都像真实面试，但同公司、同岗位方向、时间仅隔一周，无法证明不同招聘流程；不拆两个 ID，只保留 4/14 现场验真证据更完整的页面。
- **字节同作者同公司相邻流程**：`想奋斗的柠檬精天天摸鱼` 4/21 与 5/4 均为字节 AI / Agent 方向，但流程边界无法稳定确认，因此只计 5/4 一个独立来源，避免双计。
- **Bilibili / CSDN / 聚合站“2026 大厂面经”**：大量页面明确写“整理全网干货 / 高频题 / 每题标准答案 / 资料包”，以及 NiceOffer 等二次整理站，即使公司标题热门也全部零贡献。
- **最新热门结果面仍高度饱和**：9 月热门关键词返回的大量字节 / 腾讯 / 美团 / PDD / 百度结果已在 `S001–S247`，或属于内容账号、后发扩写、转载 / 帮转；本轮大部分新增来自 4–6 月长尾和作者 Timeline，而不是 9 月第一页。

---

## batch-22 · Batch 22 最终校验中的典型排除 / 合并

来源：原批次第 319–332 行。

- **腾讯 `Akhasi` 流程归属不清，整链排除。** 作者 04-19 同日存在“腾讯视频一面（过）”和“腾讯视频二面（横向挂）”，但 05-21 又发布另一条“腾讯二面”。无法可靠确认 05 月页面究竟是同一流程、重新被捞还是另一岗位，因此不猜、不合并、不编号。
- **阿里灵犀不稳定一面零贡献。** `猪脚饭之王` 的 04-03 灵犀一面页在最终复核时再次无法稳定打开，因此不使用其中任何题目；只保留能够稳定核验的 04-10 二面 `S260`。05-06 不同作者逐题复刻一面的问题只作为复制链证据。
- **京东物流两轮主动合并。** 04-08 一面与 04-14 二面均为 `纯马牛马牛🐮`，同公司同招聘流程，合并为 `S262`，不按轮次虚增。
- **小红书两轮主动合并。** `猪脚饭之王` 04-06 一面明确次日约二面，04-08 二面后续挂，两页合并为 `S259`。
- **美团 5 月复制链排除。** 一条看似很强的新候选向前追到 04-20 更早页面，出现“Fuzzy Query → RRF 参数 → 空教室 / 火锅场景 → Hallucination Chain → HTTP3 / V8”等长连续同序，原始归属无法可靠确认，整链不收。
- **阿里平头哥后续轮次不新增。** 04-29 二面可确认属于历史 `S118` 同候选同流程；遵循不修改历史 Batch 的当前指令，本批不另增编号。
- **近期百度整齐题单继续排除。** 同账号多日重复 / 扩写，正文称只问少量开放架构题却又整齐列出大量题目，内容包装风险高，未进入 HUMAN-A。
- **字节高密度题单因现场证据不足未放行。** 某 04-08 页面虽然问题多，但作者页面和正文不足以达到当前对真人现场 / 招聘交互的严格阈值；宁可不收。
- **快手大题单不因题量高自动升级。** 一条 4 月候选按知识域整齐覆盖大量问题，评论区也出现“真的会问这么多吗”的质疑；没有足够强的现场与作者证据前保持排除。

---

## batch-23 · Batch 23 最终校验中的典型排除 / 合并

来源：原批次第 107–119 行。

- **字节中国交易与广告三轮主动合并。** `喜羊羊吃草中` 的一面、二面、三面以及个人 Timeline 能形成 6/17 → 6/22 → 6/24 → HR → 7/1 书面 Offer 的完整链，统一归入 `S214`，不按轮次拆号。
- **快手 AI 应用服务端三轮主动合并。** `27备战秋招` 的个人 Timeline 明确给出 8/26 一面、9/1 二面、9/9 三面，统一归入 `S114`。
- **字节 8/23 中国交易与广告高密度候选因 Role Scope 模糊排除。** 虽然候选人的 Agent 项目被问得很深，但页面无法稳定证明岗位本身属于 AI Application / Agent，而非普通后端仅深挖候选人 AI 项目，因此不收。
- **阿里国际“朋友 / 小伙伴投稿 + 完整答案”页面排除。** 不满足候选人本人第一人称，并带答案包装，零贡献。
- **淘天等批量多公司面经账号继续按内容账号风险排除。** 即使题目看起来完整，也不因为热门公司或题量大降低 Gate。
- **小红书普通 PE / 后端仅偶发问 Agent 的页面排除。** 只有能够明确确认 `AI+全栈` 或实际职责主体属于 AI Application 的场次才进入本批。
- **快手父子索引 / BM25 / Rerank 长链继续排除。** 已出现多个日期 / URL 的高度同序版本，原始归属不可靠，不猜原场。
- **9 月热门结果页历史命中继续增多。** 小红书 9/8 已是历史 `S033`、美团 9/2 已是 `S011`、京东 4/10 已是 `S247` 等，均不重复计数。

---

## batch-24 · 典型排除

来源：原批次第 53–61 行。

- 阿里 Token Foundry 8/17 → 8/24 → 9/3 三轮：看似新强候选，GitHub Code Search 0 命中，但直接历史回读确认就是已收录 `S144`，零新增。
- 字节 TikTok AI Agent 8/9：Code Search 0 命中，但直接历史回读确认已在早期 Batch 收录，零新增。
- 小红书 Agent 服务端 9/8：搜索末段一度看起来是最新真人强候选，但再次对历史正文后确认与历史 `S033` 为同 URL / 同场，撤回，不分配新 ID。
- 拼多多同一候选人 8/23 → 8/25 → 8/31 多轮：后续页面属于同一候选人同一公司同一招聘流程，不能按轮次新增；历史文件不修改，本批零贡献。
- 7 月字节某 AI 应用页面：罕见连续题序与历史其它公司来源高度同构，复制链原始归属不能稳定确认，整链排除。
- 美团 / 阿里 / 快手若干高密度页面：作者主页表现为批量面经 / 答案 / 订阅内容生态，按“非内容账号”Gate 排除。
- 腾讯、OPPO / vivo / 小米等若干候选：正文不稳定、Role Scope 不明确、历史命中或只能取得搜索摘要，均不为公司覆盖率降低标准。

## batch-25 · 典型排除

来源：原批次第 134–141 行。

- 小红书公开索引中的“淘天 AI Agent 一面问麻了”等标题：只能稳定取得索引 / 标题，且罕见题序与历史 `S087` 高度同构；索引仅作导航，零贡献。
- `lazy_learner` 4/6 腾讯 AI 后端短帖：连续题序几乎逐题命中 2025 年另一作者腾讯 IEG 后端一面，按复制链排除；不影响对同作者 4/2 独立原帖的单独核验。
- 百度广告投放 / 大模型应用一组高密度页面：岗位内容强，但作者 Timeline 对同一轮日期出现 8/05 与 8/18 冲突，无法稳定解释，按 Timeline 冲突排除。
- 9 月美团 / 快手 / PDD 等多条由同类账号发布的精致“真人叙事 + 60% 付费 / 答案”页面：账号长期批量覆盖多家公司，按内容账号 / 付费答案包装排除。
- 小米 Agent 三面等页面：来自同类批量内容账号且正文大比例付费，无法完整核验原场，零贡献。

## batch-26 · 典型排除

来源：原批次第 175–183 行。

- 9 月 PDD / 快手等“浙江大学 算法工程师”批量页面：同类账号跨公司高频发布，常带 60% 付费 / 订阅内容，按内容账号与付费答案包装排除。
- RockyDing / WeThinkIn、博客园 / CSDN 等“含完整答案”“真题 Top50”“面试全攻略”页面：正文明确属于整理、解析或跨渠道汇总，零贡献。
- 快手 3/18 大模型应用页面：连续 20+ 题几乎逐题命中更早 3/5 原场，判后发复制，零贡献。
- 美团 9 月 AI 后端个人帖：账号真人，但正文只有实习 / 项目拷打、AI Coding、少量 Redis / MySQL 概括，信息密度不足，零贡献。
- 腾讯 4 月若干强候选：部分只能稳定打开二次汇总而原始正文无法完整访问，按 Stable Original Gate 排除；另有原帖虽问题多但缺少足够现场 / 招聘流程证据，保守排除。
- 快手效果营销、京东物流、阿里云 SRE 等普通 Backend / SRE 流程：即使候选人项目里出现 RAG / Agent，也不能证明岗位本身属于目标 Role Scope，零贡献。
- 已核验真人作者的 PDD / 快手 Kstar / 百度等进度帖：只有流程状态而没有找到可稳定核验的对应完整技术原帖，进度帖本身不贡献题目。

## batch-27 · 当日最终清洗 / 明确排除

来源：原批次第 312–326 行。

以下高技术密度结果仍然 **零贡献**，原因是 Provenance / Role Scope / 去重 Gate 未通过：

- **字节 Agent 9/15｜作者 `小妞脂`**：历史已存在同作者 `S076` 字节 Agent 9/3 流程；无法证明是独立 BU / 新招聘流程，不能因新 URL 或 Search 0 命中重复计数。
- **蚂蚁 9/15 高密度 Agent / AI Native 页面**：可从企业聚合页看到 Write-risk、Long-task Harness、Hooks / Plugins、Agent Eval 等强问题，但原始正文直接回读不稳定；在稳定原帖和作者链补齐前不收。
- **蚂蚁 9/14 `AIGC小白入门记` Agent 开发页**：技术题覆盖 Eval、RAG、权限、Checkpoint、Redis / Kafka / MySQL，但作者属于历史已确认的批量内容账号链，零贡献。
- **新旦智能 AI 应用开发**：LangChain 1.0、Hermes Self-evolution / Memory、Harness、Eval、Codex Quality 等题很强，但原始正文持续 Cache Miss，不满足 Verifiable Gate。
- **淘宝闪购 AI 一面 9/14**：聚合入口能读到完整 Agent / Memory / Scale 问题，但原帖直链 / 作者链仍未稳定闭环，不把聚合摘要升级为 HUMAN-A。
- **望尘科技 AI 全栈 9/14**：能从关联页面看到面试时长、Java 与 AI Coding Quality，但原帖直链没有稳定定位，继续零贡献。
- **快手 9/14 二面**：正文 / Role Scope 证据仍不足，不能因为含 Agent / RAG 问题就默认是目标岗位。
- **PDD Agent 批量面经链**：近期页面以“面经 01/02/03...”批量整理并混入标准答案 / 代码段，无法证明每篇为作者本人原场，按内容账号 / 合集排除。
- **去哪儿 / 北京网梯等 AI 自动面试**：违反 Human Interviewer Gate。
- **纯 AI Infra / Training / GPU / MPI / Serving Infra**：即使包含 MCP / Skill / Agent 名词，只要岗位主体不属于 AI Application / Agent，按 Role Scope 排除。

## batch-28 · 当日最终清洗 / 明确排除

来源：原批次第 74–84 行。

以下近期高密度结果仍然 **零贡献**，原因是 HUMAN-A / Role Scope / Verifiable / 去重 Gate 未完整通过：

- **千问技术部 9/16 一面**：真人第一人称和 Agent 技术密度都很高，包含 Plan / Replan、Context、Tool Calling、Reconnect、Agent Eval、Regression 等连续追问；但原帖无法稳定确认目标岗位本身属于本库 AI Application / Agent Role Scope，而不是其它研发岗位深挖候选人 Agent 项目，因此不因为题目漂亮扩大岗位边界。
- **小红书 Agentic 端侧推理优化 9/14**：正文稳定且第一人称，但技术主体明显落在端侧模型推理、量化 / 压缩、蒸馏 / SFT 等 Model / Training / Inference Optimization 边界，默认不属于本库 AI Application / Agent 应用工程范围。
- **京东 AI Agent 9/14**：题序很强，但作者为 `AIGC小白入门记`，属于历史已识别的批量内容账号链；继续零贡献。
- **去哪儿旅行 AI 应用开发（全栈）9/16**：Role Scope 与真人招聘流程明确，但公开稳定正文仍主要是流程级摘要，具体技术题没有形成足够可核验文本，暂不满足 A-grade 技术密度。
- **百度网络研发 / B站测开等近期 Agent 深挖**：面试中虽出现 LangGraph、OpenClaw、Skill、MCP 或 Agent Evaluation，但岗位主体分别是网络研发 / 测试开发等 Role Scope 外方向。
- **近期聚合页、整理站、标准答案、招聘 JD、内推、新闻和搜索摘要**：只用于发现原帖或理解市场，不贡献 HUMAN-A。

## batch-28 · 2026-09-17 Final Summary

来源：原批次第 85–104 行。

- Three-round search effort：**至少 217 组 Query / Query 变体**（Morning ≥97 + Afternoon ≥60 + Evening ≥60）。
- Three-round verification effort：**至少 60 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试；这是工作量次数，不代表 60 个唯一 URL。
- Final additions：**1 个 HUMAN-A：`S287`**。
- Current formal library：**28 Batch / 287 HUMAN-A / `S001–S287`**。
- Next ID：**`S288`**。
- Inbox：归档后清空。


1. **Harness 从名词题进入“是否值得替换现有架构”的迁移判断。** 面试官会要求比较 DeepSeek Harness / Pi Agent，并讨论接入当前 Agent 需要改变哪些系统层。
2. **Context / Memory 追问继续参数化、机制化。** 不只问 Sliding Window / Summary 是什么，而会追窗口大小、切换条件和 Claude Code Context Compression。
3. **Agent Backend 与传统可靠性机制继续合流。** 在线文档更新会直接追并发幂等、MQ 放置与 MQ vs 定时任务，而不是把 Agent 当作孤立模型调用。
4. **Computer Use 开始进入真实应用面试。** 本地 / 云端执行环境、控制方式和 Runtime 边界成为可追问内容。
5. **AI Coding 正从“会不会用工具”进入完整研发 Workflow 与 AI Native 程度验真。**
6. **Foundation 仍然同场。** MySQL B+Tree 与算法追问没有因为 Harness / Computer Use 出现而消失。

饱和度 / 盲区：最近 3 天公开结果层继续表现出较高局部饱和度与 provenance 成本——内容账号、聚合 / 整理页、普通岗位 Agent 深挖、Role Scope 模糊以及原帖不稳定占比较高。牛客仍是最容易稳定核验的公开原帖来源；百度 / 腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺新的高质量可核验目标岗第一人称样本。后续继续做跨平台与作者 Timeline 补盲，但不降低 Gate。

## batch-29 · 当日最终清洗 / 明确排除

来源：原批次第 58–66 行。

- **千问技术部 9/16 一面｜同作者 `Decadeqqq`**：原帖稳定、1h15min、Plan / Replan、Tool Calling、Context、Reconnect、Evaluation、Review Agent 等技术密度很高；但前一日已因岗位主体无法稳定确认属于 AI Application / Agent Role Scope 而排除。晚间没有获得新的职位 / 招聘主体证据，因此维持原判断，不因同作者已有合格蚂蚁流程而顺带放行。
- **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：搜索结果与作者主页能确认当天确有 `agent开发` 面试和个人求职 Timeline，但当前稳定入口只暴露前几道问题及“14 道真题”提示，直接原帖详情仍无法稳定回读，无法完整核验 A-grade 技术链；保留为后续追源线索，零贡献。
- **快手 9/17 AI 应用开发一 / 二面**：继续没有补到稳定可直接回读的候选人原帖；企业页 / 搜索片段不能替代原始正文，零贡献。
- **水滴 9/17 AI 全栈**：当前可核验的是笔试，不是 Human Interviewer，排除。
- **百度 9/17 后端一面**：真人第一人称且问到 AI 应用平台、Agent 与 Workflow，但岗位主体仍是普通后端，Role Scope 排除。
- **JD / 企业页 / 聚合 / 题库 / 面经索引 / 标准答案页**：只作为市场旁证或 Recall，不贡献 HUMAN-A。

## batch-29 · 当日三轮监测摘要

来源：原批次第 67–85 行。

- Three-round search effort：**至少 245 组 Query / Query 变体**（Morning ≥60 + Afternoon ≥85 + Evening ≥100）。
- Three-round verification effort：**至少 70 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试；这是工作量次数，不代表 70 个唯一 URL。
- Final additions：**1 个 HUMAN-A，`S288`**。
- Current formal library：**29 Batch / 288 HUMAN-A / `S001–S288`**。
- Next ID：**`S289`**。
- Inbox：归档后清空。


1. Agent 安全正在从“输出会不会幻觉”继续下沉到**有副作用写操作、权限、Tool / API Contract 与业务语义 Validation**；
2. Long-task / Harness 不只考 Loop，而开始与 Backend API、恢复、扩展机制和 Framework Kernel Trade-off 联动；
3. Eval 从“做过评测”进入 Gate / Metric / Review Agent 可靠性；
4. Agent / Skill / AI Coding 已明显向普通 Backend、Data、Test 岗扩散，因此 Role Scope Gate 必须比过去更严格；
5. Foundation / Production Engineering 仍是最新 Agent 能力的承载层，不能被新名词替代。

饱和度 / 盲区：最近 72 小时公开热门层继续表现为**局部饱和 + provenance 成本高**。牛客仍最容易拿到可核验原帖，但新结果大量落在笔试、聚合、内容账号、普通岗位 AI 项目追问或原帖不可稳定回读；腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等目标公司以及小红书 / 知乎 / 脉脉 / 独立博客，在严格 Gate 下仍缺新的目标岗高密度第一人称样本。下一轮继续追 4399 9/18 Agent、快手 9/17 AI 应用一 / 二面及跨平台作者源，不降低 Gate。

## batch-30 · 当日最终清洗 / 明确排除

来源：原批次第 40–50 行。

以下近期高密度线索在 22:00 仍然 **零贡献**，没有为了新增数量降低 Gate：

- **4399 Agent 开发 9/18｜作者 `AAA野生原子弹批发`**：作者 Timeline、目标 Role Scope 与 14 道连续题序都很强，可见 Harness Architecture、10 万级日志、Agent 生成 SQL 错误检测、90% 测试通过率来源以及“如何证明不是只依赖 AI 工具”等问题；但仍未稳定拿到 post-specific 原始详情页，作者索引 / Search Snippet 不能替代 Stable Original，继续待追源。
- **快手 9/17 AI 应用开发一 / 二面**：推荐 / 企业入口仍能看到长任务崩溃恢复、并发修改会话记忆等高价值问题，但候选人原始详情正文与 provenance 仍不够稳定，且部分展示片段混入解释 / 答案式展开；继续排除。
- **PDD / B站 / 腾讯等“面经 06/07/08”“完整答案”“Agent 面经总结”页面**：属于合集、内容账号或答案化整理，不是候选人本人单一招聘流程原始证据。
- **OPPO 9/18 线下面、9/17 数据 / 测试等普通工程岗位**：真人面试中已经出现 AI Memory、AI Development Flow 等内容，但岗位主体并非 AI Application / Agent；继续按 Role Scope 排除。
- **小红书近期多模态算法 / 端侧推理等结果**：岗位主体落在模型 / 算法 / 推理优化边界，不因为出现 Agent 术语扩大本库范围。
- **招聘 JD、企业职位页、聚合页、内推、题库与新闻**：仅用于发现线索或理解市场，不贡献 HUMAN-A。

## batch-30 · 2026-09-19 Final Summary

来源：原批次第 51–69 行。

- Three-round search effort：**至少 300 组 Query / Query 变体**（Morning ≥90 + Afternoon ≥110 + Evening ≥100）。
- Three-round verification effort：**至少 65 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 20+ + Afternoon 25+ + Evening 20+）；这是工作量次数，不代表 65 个唯一 URL。
- Final additions：**1 个 HUMAN-A：`S289`**。
- Current formal Market library：**30 Batch / 289 HUMAN-A / `S001–S289`**。
- Next ID：**`S290`**。
- Inbox：归档后清空。


1. **AI Application 项目验真继续落到 Production Diagnosis。** 面试官不只问 RAG / Function Calling 名词，而是要求从线上支付失败完整链路解释系统如何定位问题，并追 Network 为什么存在。
2. **Retrieval Failure Attribution 与异构文档处理仍是稳定工程问题。** RAG 低召回要能分层定位原因；PDF 表格 / 图片需要给出实际解析链路，而不是只报 Parser 名称。
3. **End-to-end Ownership 被直接验证。** 候选人会被问更偏局部 Component 还是全链路参与，以及资源充分时下一步怎样演进系统。
4. **Harness + AI-assisted Engineering Authenticity Verification 是值得继续追的弱信号。** 4399 线索已经把 Harness、SQL 验错、测试指标和“AI 帮你完成后是否真正掌握”放在一起，但 provenance 尚未闭环，因此当前只作为观察，不进入正式频率。
5. **Agent / AI 术语继续向普通 Backend / Data / Test 岗扩散。** 这使 Role Scope Gate 更重要，而不是更宽松；出现 Memory / Agent / AI Coding 不能替代目标岗位证据。

饱和度 / 盲区：最近 72 小时公开结果层继续呈现**局部饱和 + provenance 成本高**。牛客仍是最容易拿到稳定第一人称原帖的平台，但内容合集、答案化页面、普通岗位 AI 深挖与原帖不稳定占比较高；4399 9/18 Agent、快手 9/17 AI 应用一 / 二面仍是最值得继续补 provenance 的近端线索。腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺新的高质量、稳定可核验目标岗第一人称来源。继续补盲，但不降低 Gate。

## batch-31 · 当日最终清洗 / 明确排除

来源：原批次第 65–76 行。

以下近期高密度结果仍然 **零贡献**，原因是 Stable Original / Candidate Provenance / Role Scope / 全历史去重 Gate 未完整通过：

- **字节广告团队 Agent 一 / 二面｜发布 2026-09-19 17:07**：搜索层可完整看到 Redis Distributed Lock、MySQL Clustered Index、内部 Skill 平台上传 / 下载 / 发布、本地 Runtime、AI 提效、营销秒杀 System Design、现场 Demo、Skill vs Function Call 与 Coding；但 post-specific 页面直接回读仍只返回页面壳，作者账号 / Timeline 无法稳定闭环。高价值但 provenance 不足，继续待追源，不因题目前沿而降低 Stable Original Gate。
- **4399 Agent 开发｜面试 2026-09-18｜`AAA野生原子弹批发`**：作者主页能稳定确认个人求职 Timeline，并能看到“证明不是只依赖 AI、十万级日志、Harness、Agent SQL 验错、90% 测试通过率”等 14 道问题；但仍未取得可长期稳定直接回读的 post-specific 原帖详情正文。作者索引 / Search Snippet 不替代原始详情页。
- **快手 AI 全栈 `明天会有好天气`**：全历史直接回读确认就是既有 `S282`，属于精确历史重复。
- **携程 9/18 AI 应用开发一 / 二面、腾讯 9/18 AI 全栈、小红书 9/20 Agent 平台研发**：当前主要依赖企业 / 话题索引或 Search Cache，post-specific 原始正文与作者 provenance 未完整闭环；零贡献。
- **B站 9/19 “大模型面试岗”**：正文明确是内容作者让一位学员复述面试，属于二手转述，不是候选人本人第一人称；且岗位偏算法。
- **普通 Backend / Data / Test 岗近期 Agent / Memory / AI Coding 深挖**：不能用“问到 AI”替代目标 Role Scope；继续排除。
- **合集 / 标准答案 / 内容号 / JD / 内推 / 聚合 / 新闻**：只用于发现与市场旁证，不贡献 HUMAN-A。

## batch-31 · 2026-09-20 Final Summary

来源：原批次第 77–95 行。

- Three-round search effort：**至少 300 组 Query / Query 变体**（Morning ≥100 + Afternoon ≥100 + Evening ≥100）。
- Three-round verification effort：**至少 75 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 25+ + Afternoon 30+ + Evening 20+）；这是工作量次数，不代表 75 个唯一 URL。
- Final additions：**2 个 HUMAN-A：`S290–S291`**。
- Current formal Market library：**31 Batch / 291 HUMAN-A / `S001–S291`**。
- Next ID：**`S292`**。
- Inbox：归档后清空。


1. **Architecture Choice 必须被证明。** “做了 Multi-Agent”已经不够；真实面试会持续追为什么必须 Multi-Agent、为什么不能更简单、怎样编排，以及结果 / 准确率 / 使用者反馈怎样证明架构值得存在。
2. **Agent / MCP / RAG 仍与 Foundation 同场。** Shopee Chatbot 把 Agent、Function Call / Tool / MCP、RAG 与 Linux Process、Quick Sort 深追和 AI Coding 放在一场面试里，说明应用岗基础工程与算法能力不能弱化。
3. **Skill / Runtime 正继续向平台级设计与现场验真下沉。** 字节广告团队待追源样本已经问内部 Skill Platform 的上传 / 下载 / 发布、本地 Runtime、现场 Demo 与 Skill vs Function Call；但 provenance 尚未闭环，因此当前只作为 Market Observation，不计正式频率。
4. **AI-assisted Engineering 的真实性验证继续增强。** 4399 待追源样本同时追 Harness、SQL 验错、测试通过率来源和“如何证明不是只依赖 AI 工具”，值得继续监测，但当前不进入正式 HUMAN-A。
5. **Role Scope Gate 需要继续收紧。** Agent / Memory / AI Coding 已扩散到普通 Backend / Data / Test 岗；术语出现本身越来越不能证明目标岗位职责。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现**局部饱和 + 高 provenance 成本**。牛客仍是最容易取得稳定候选人原帖的平台，但企业聚合、Search Cache、答案化页面和 post-specific Cache Miss 占比较高；字节广告团队、4399、携程、腾讯 AI 全栈、小红书 Agent 平台研发仍是值得追 provenance 的近端线索。腾讯 / 美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺更多稳定可核验的新目标岗第一人称来源。继续补盲，但不降低 Gate。

## batch-32 · Recovery Final Summary

来源：原批次第 71–80 行。

- 恢复日期：2026-09-22。
- 归属监测日：2026-09-21。
- Final additions：**2 个 HUMAN-A，`S292–S293`**。
- 恢复后中间基线：**32 Batch / 293 HUMAN-A / `S001–S293`**。
- Next ID：**`S294`**。

Recovery 原因只记录为监测流水恢复，不改变来源质量标准；本批仍以 9 月 21 日当日已经通过 Gate 的候选为唯一内容。

## batch-33 · 当日最终清洗 / 明确排除

来源：原批次第 213–221 行。

- **拼多多 `agent 一面`、星网锐捷 Agent 两轮、vivo 线下面 Agent 开发**：2026-09-22 Evening 的牛客最新流中出现了新鲜标题，均属于值得继续追的近端线索，但 direct post-specific 原帖在本轮均 Cache Miss，无法完成 Stable Original + Candidate First-person 全文核验；全部零贡献，不用标题 / 热榜补数。
- **字节 AI 全栈（飞书）**：属于 2026-09-21 已通过但 Finalize 失败的 backlog，本次恢复归入 `batch-32.md / S293`，不重复计入本日新增。
- **4399 Agent 9/18、阿里云 AI 应用、近期快手 / 腾讯等**：技术链仍有价值，但继续卡在 Stable Original / 作者 provenance 或企业聚合，零贡献。
- **Kuaishou / Shopee 等“完整答案 / 每题答案”页面、`AIGC小白入门记` 等内容链**：按答案帖 / 内容号 Gate 排除。
- **普通 Backend / Frontend / Data / Test 岗出现 Agent / Skill / AI Coding**：没有目标 Role Scope 时继续排除；术语扩散不等于目标岗位样本。
- **AI 自动面试、JD、内推、题库、聚合、Search Snippet、二次整理**：只用于发现 / 市场旁证，不贡献 HUMAN-A。

## batch-33 · 当日三轮监测摘要

来源：原批次第 222–244 行。

- Discovery window：运行时最近 72 小时，Evening 约为 **2026-09-19 22:01 ～ 2026-09-22 22:01**。
- Morning search effort：**至少 120 组 Query / 变体，25+ 次验证 / 追源**。
- Afternoon search effort：**至少 140 组 Query / 变体，25+ 次验证 / 追源**。
- Evening search effort：**至少 100 组 Query / 变体，25+ 次稳定回读 / 30+ 次打开或追源尝试**。
- Three-round total：**至少 360 组 Query / Query 变体，至少 75 次候选原帖 / 作者页 / provenance 验证或追源尝试**。
- Final additions for 2026-09-22：**2 个 HUMAN-A，`S294–S295`**。
- Same-process extension：**S288 蚂蚁二面，0 新 ID**。
- Current formal Market library：**33 Batch / 295 HUMAN-A / `S001–S295`**。
- Next ID：**`S296`**。
- Inbox：归档后清空。


1. **Knowledge Quality 正进入 Agent Backend 的真实验真链。** 百度不是只问“动态知识库如何更新”，而是追知识质量、精准加载、实际采纳、Milvus、Skill Quality Gate 与最终研发效果。
2. **Accuracy–Latency Trade-off 被要求量化。** “多约 1 分钟换 20–30pp 准确率”要求候选人把 Agent Quality 与用户 / 系统延迟放在同一决策框架里。
3. **Runtime / Permission / AI Native SDLC 继续下沉。** 蚂蚁 `S288` 二面把一面的写操作风险 / Harness / Eval 继续推进到 Runtime、读写权限、User Confirmation、Long-task Plan、CLI / Skills 暴露、AI Native 研发流程与 Plugin 化。
4. **AI Full-stack 仍然是完整软件工程底座 + AI Feature 的组合。** 度小满把 Network / OS / Go / MySQL / Redis / Frontend Foundation 与 AI-assisted Development、AI Q&A System Design 放在同一场。
5. **新鲜供给不等于可入库供给。** PDD / 星网锐捷 / vivo 的新标题说明市场仍有新增，但 Stable Original / Candidate First-person 仍是公开来源的主要瓶颈；0 个可稳定核验也比放宽 Gate 更正确。

饱和度 / 盲区：最近 72 小时牛客仍是最容易获得第一人称技术面经的平台，但最新流中 Cache Miss、企业聚合、答案化和 Role Scope 外 AI 深挖仍占很高比例。PDD Agent、星网锐捷 Agent、vivo Agent 开发、4399、阿里云 AI 应用仍值得下一轮优先追 stable original；腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米以及小红书 / 知乎 / 脉脉 / 独立技术社区仍缺更多稳定目标岗 Candidate First-person 样本。继续补盲，不降低 HUMAN-A Gate。

## batch-34 · 当日最终清洗 / 明确排除

来源：原批次第 43–51 行。

以下近期结果在 22:00 仍然 **零贡献**；没有为了 Source Count 降低 Gate：

- **作业帮 9/23 一面｜`Decadeqqq`**：候选人本人第一人称且 Agent Evaluation 技术链很强，连续追 Tool Idempotency、断连 / 重连续跑、Audit、真实 User Trace、Eval Set、Deterministic Metric、Agent Reviewer、低分 Case 调优与 Evaluation Dataset 演进。但同作者此前公开记录把作业帮流程标为 `全栈开发`，当前 9/23 面经也没有新增证据证明招聘主体属于 AI Application / Agent；按 Role Scope Gate 保守排除，不因题目高级而扩大统计边界。
- **某科技 9/23｜`中二的西红柿起床了`**：作者本人新帖明确复盘“看似 Agent / AI 开发，实际更像科研助理”的岗位，工作重点偏文献调研 / 医疗 AI 研究支持；不属于当前 AI Application / Agent 工程 Role Scope。
- **4399 Agent、阿里云 AI 应用及若干近期大厂高密度线索**：仍受 Stable Original、作者 provenance、Role Scope 或最近 72 小时边界约束；企业页、Search Snippet、聚合、答案化页面不替代候选人原始正文。
- **窗口外旧面经、普通 Backend / Frontend / Test / Data 岗里的 Agent 深挖、AI 自动面试、合集 / 题库 / 标准答案 / 内容号 / JD / 内推 / 新闻**：继续按对应 Gate 排除或仅作市场旁证。

## batch-34 · 2026-09-23 Final Summary

来源：原批次第 52–69 行。

- Three-round search effort：**至少 340 组 Query / Query 变体**（Morning ≥120 + Afternoon ≥120 + Evening ≥100）。
- Three-round verification effort：**至少 70 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 25+ + Afternoon 25+ + Evening 20+）；这是工作量次数，不代表 70 个唯一 URL。
- Final additions：**1 个 HUMAN-A：`S296`**。
- Current formal Market library：**34 Batch / 296 HUMAN-A / `S001–S296`**。
- Next ID：**`S297`**。
- Inbox：归档后清空。


1. **Capability Scalability 开始进入短场 Agent 基础验真。** 面试官不只问 Skill / MCP 是什么，而会直接追数量膨胀后怎样做 Discovery、怎样避免 Context Pressure。
2. **Runtime Ownership 被继续下钻。** “没有使用 Framework 时，Context Compression 与 Memory 怎么自己实现”要求候选人解释底层运行时，而不是只会框架 API。
3. **Harness 已成为 Agent 应用岗的基础语汇之一。** 但同一天作业帮等普通 Full-stack 流程也会深挖 Agent Evaluation，说明术语扩散继续加快，Role Scope Gate 必须保持严格。
4. **流程级去重仍比 Source Count 更重要。** 本轮全历史回读后只保留真正独立招聘流程；强题目但 Role Scope 不闭环的页面继续零贡献。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现**局部饱和 + provenance / Role Scope 成本高**。牛客仍是最容易稳定核验候选人原帖的平台；小红书 / 知乎 / 脉脉 / 博客 / 技术社区等非牛客渠道在当前窗口没有形成新的稳定目标岗第一人称来源。字节 / 阿里系 / 腾讯 / 美团 / 快手 / 百度 / 蚂蚁 / PDD / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等公司仍持续扫描，但大量近期命中属于窗口外旧帖、普通岗位 AI 素养扩散、聚合 / 内容链或 Stable Original 不足。继续补盲，但不降低 Gate。

## batch-35 · 当日最终清洗 / 明确排除

来源：原批次第 39–49 行。

以下近期结果在 Evening Finalize 后仍然 **零贡献**，没有为了数量降低 Gate：

- **字节剪映 AI 前端一面｜发布 2026-09-22**：公开话题层可看到自研 Agent Framework、为什么不用 LangGraph、ReAct Loop、Tool Registry、`tool_call` JSON Schema、本地 Tool Execution 与 Context 回填等完整技术链；但 post-specific 原帖 / 作者 Timeline 与“AI 前端”实际工作是否属于本库 AI Application Role Scope 仍未同时稳定闭环，继续待追源，不进入 HUMAN-A。
- **携程近期 AI 面试复盘**：公开内容明确属于 AI 自动面试，不满足真人面试官 Gate。
- **`林小白zii`、`AIGC小白入门记` 等批量内容 / 付费面经链**：即使 Agent / Harness / RAG 题目密度很高，也不满足候选人本人原始招聘流程 provenance，排除。
- **近期算法 / SFT / RL / 模型训练岗位、Test / Data / 普通 Backend / Frontend 岗**：仅出现 Agent、MCP、Skill、AI Coding 等术语不能替代目标 Role Scope；不扩大统计边界。
- **宁德时代工业 Agent 近端线索**：招聘现场存在，但公开可核验技术内容过少、信息密度不足，不进入 HUMAN-A。
- **企业聚合、搜索摘要、JD、内推、题库、完整答案、二次整理、博客摘要**：只用于发现线索或市场旁证，不贡献正式来源。

## batch-35 · 2026-09-24 Final Summary

来源：原批次第 50–71 行。

- Discovery window：运行时最近 72 小时，约覆盖 **2026-09-21 22:00 ～ 2026-09-24 22:00** 的新发布 / 更新。
- Morning search effort：**至少 75 组 Query / 变体，20+ 次验证 / 追源**。
- Afternoon search effort：**至少 80 组 Query / 变体，24+ 次验证 / 追源**。
- Evening search effort：**至少 100 组 Query / Query 变体，20+ 次显式原帖 / 作者页 / provenance 打开、回读或追源尝试**。
- Three-round total：**至少 255 组 Query / Query 变体，至少 64 次候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试**；这是工作量次数，不代表 64 个唯一 URL。
- Final additions：**1 个 HUMAN-A：`S297`**。
- Current formal Market library：**35 Batch / 297 HUMAN-A / `S001–S297`**。
- Next ID：**`S298`**。
- Inbox：归档后清空。


1. **AI Full-stack 正把 AI Pipeline Quality 与传统大规模系统工程合成同一套能力模型。** 面试不会停在 Agent / RAG 名词，而是继续追 Node Accuracy、Hallucination / Deviation、Code Generation Quality、大数据存储与检索、MQ、Cache / DB Consistency 和实时连接。
2. **Evaluation 越来越靠近业务链路。** “方案是否有效”要分别落到代码生成质量、业务知识准确性、节点质量与端到端结果，而不是只给一个整体准确率。
3. **大规模数据能力仍是 AI Application 的硬底座。** Doris / Hive / ES 选型、Inverted Index、超大规模过滤和 SQL / Index Design 与 Agent 能力建设在同一场出现。
4. **Realtime Backend 与 Agent 产品体验开始强耦合。** 用户隔离 MQ、最近 N 条状态、幂等、WebSocket / Polling 与长连接稳定性成为 AI 全栈的直接考察对象。
5. **Agent 术语继续跨岗位扩散，因此 Role Scope / Provenance Gate 需要继续收紧。** 剪映 AI 前端等新鲜线索技术上很强，但在岗位边界和稳定原始证据没有闭环前仍不能正式计数。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现 **局部饱和 + 高 provenance 成本**。牛客仍是最容易取得稳定第一人称线索的平台，但 post-specific Cache Miss、内容账号、答案化页面和普通岗位 AI 深挖占比很高；字节剪映 AI 前端仍是最值得继续追原帖 / 作者 Timeline 的近端线索。腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客渠道，在当前窗口内没有形成第二个同时满足 HUMAN-A + Role Scope + Stable Original + 全历史去重的新独立流程。继续补盲，但不降低 Gate。

## batch-36 · Recovery Summary

来源：原批次第 187–192 行。

- 恢复正式来源：4；S298–S301
- 恢复后阶段基线：36 Batch / 301 HUMAN-A
- 本批结束后的下一编号：S302
- 原 Inbox 四条已恢复，后续本轮新发现进入 Batch 37

## batch-37 · Final Summary

来源：原批次第 4779–4789 行。

- 本批合计新增：85个独立流程，S302–S386（首轮及其图片补查60个，第二轮遗漏复查25个）
- 本轮另恢复旧Inbox：4个，见Batch36；不重复计为新发现
- 第二轮新增平台：牛客9、小红书16；本批累计牛客41、小红书44
- 第二轮补充既有S123、S280、S294、S295、S329、S333；S123/S333的新增帖子未证明独立投递，保守不增来源
- 正式Market：37 Batch / 386 HUMAN-A / S001–S386
- 下一编号：S387

首轮覆盖及保留项见 [首轮覆盖账本](coverage-2026-10-07.json) 与 [首轮未准入记录](review-holds-2026-10-07.md)。第二轮见 [覆盖账本](coverage-2026-10-07-round2.json) 与 [未准入 / 去重记录](review-holds-2026-10-07-round2.md)。

## batch-38 · Final Summary

来源：原批次第 894–899 行。

- 本日新增13个独立流程：牛客9、小红书4；S387–S399
- 本分支相对main合计新增38个流程：上一日25、本日13，另含上一日6个旧来源补充
- 分支证据库：38 Batch / 399 HUMAN-A；main是否采用以PR审核合并为准
