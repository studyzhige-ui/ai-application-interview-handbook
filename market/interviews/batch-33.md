# Batch 33 — 2026-09-22 Daily HUMAN-A Continuous Monitoring

采集日期：2026-09-22

> 本批合并当天 10:00 / 17:00 / 22:00 三次最近 72 小时持续检索。正式编号前重新读取最新 `main`、Market README、Inbox、Daily Log、两份 Market Policy 与最新正式 Batch，并再次直接回读 `batch-01.md`～`batch-31.md` 全历史；同时将 2026-09-21 backlog 先恢复为 `batch-32.md / S292–S293`，再对本批候选做交叉去重。
>
> 本批正式新增 **2 个 HUMAN-A 独立招聘流程：`S294–S295`**。另确认蚂蚁 `Decadeqqq` 9.21 二面属于既有 `S288` 同一招聘流程的后续轮次，合并回 `S288`，不新增 Source Count。日常采集只维护 Market Evidence，不修改 Frozen Canonical / `market/analysis/` Frozen 统计 / Curriculum。

---

## S294 度小满｜AI 全栈｜一面｜发布 2026-09-20 17:39｜HUMAN-A

作者：`SOLDIER_627`

来源：https://www.nowcoder.com/discuss/931241025345978368?sourceSSR=post&weFlow=true

备用同源入口：https://ac.nowcoder.com/discuss/1677258?type=0

真人 / 第一人称证据：post-specific 原帖稳定可直接回读，作者明确记录本人一面，净时长约 53 分钟；题目按真实顺序展开，Coding 要求先说明思路，再现场编码并运行通过。作者主页与小红书、字节、百度、美团、快手等本人招聘记录形成连续 Candidate Timeline，不是内容账号。

Role Scope：岗位标题直接为 `度小满AI全栈一面`；面试官还明确围绕候选人“主要做 Backend 与 Agent”追 Frontend 参与度，并要求设计 AI Q&A 功能，属于目标 AI Full-stack / Application 范围。

整场技术链：

1. 自我介绍。
2. 做过项目里最有挑战的功能是什么，Pain Point 与解决方式是什么？
3. 候选人主要做 Backend 与 Agent，Frontend 实际参与到什么程度？
4. 从浏览器输入 URL 到页面展示发生什么；TCP 为什么三次握手？
5. HTTP 502 / 504 分别表示什么；301 / 302 有什么区别？
6. Process 与 Thread 的区别；浏览器为什么采用多进程架构？
7. Go GMP Scheduler 怎样工作？
8. MySQL 为什么使用 B+Tree，而不是 Hash / Binary Tree / B-Tree；哪些 SQL 会导致 Index Invalid？
9. Redis 为什么快；Cache Avalanche / Breakdown / Penetration 怎样治理？
10. CSS `flex: 1` 表示什么？
11. CORS / 跨域是什么，有哪些处理方式？
12. 常见 Frontend Framework 与工程选型怎样理解？
13. Debounce 与 Throttle 的差异与适用场景是什么？
14. AI-assisted Development 中最有代表性的真实 Case 是什么；采用度、收益、踩坑和 AI 不擅长的部分怎样评价？
15. System Design：从 Frontend / Backend、User Experience、Security 与 Engineering 角度设计一个 AI Q&A 功能。
16. Coding：Restore IP Addresses / 复原 IP 地址，先解释思路，再现场编码并运行通过。

最终去重：在本轮编号前已直接回读正式 `batch-01.md`～`batch-31.md` 全历史，并与本次恢复的 `batch-32.md` 候选交叉核验。未发现度小满同公司 / 同招聘流程、当前 URL，或“Browser / Network → OS / GMP → MySQL / Redis → Frontend Foundation → AI-assisted Development → AI Q&A System Design → Restore IP”的历史同场来源。同作者不同公司按独立招聘流程分别计数。

---

## S295 百度｜Agent 后端｜三面｜发布 2026-09-22 09:13｜HUMAN-A

作者：`SOLDIER_627`

来源：https://www.nowcoder.com/discuss/931476137576845312

真人 / 第一人称证据：post-specific 原帖稳定可直接回读，作者记录本人三面，净时长约 42 分钟；面试官开场先介绍团队业务，再由候选人围绕方案提问，随后继续深挖候选人近期 Agent / Skill 经历和技术 Trade-off，招聘现场与互动结构明确。作者 Candidate Timeline 连续稳定。

Role Scope：面试官明确介绍团队主要做内部 AI 研发提效平台，让 AI 参与需求开发与落地，涉及 Agent Orchestration、Workflow Optimization、本地 / 云端开发；另一主线是动态知识库，用 AI 自动采集、更新和治理研发知识，再反哺 Code Generation / Testing。属于直接目标 Agent Backend / AI Application 范围。

整场技术链：

1. 团队内部 AI 研发提效平台、Agent 编排与 Workflow 的业务边界是什么？
2. 动态知识库的知识来自哪里，在研发中怎样使用，定时更新还是事件触发？
3. Relational DB 与 Vector DB 在知识系统中怎样分工？
4. AI 怎样自动保证 Knowledge Quality，并为代码任务加载足够精准的知识？
5. 怎样评测知识在真实研发任务中的实际采纳效果？
6. Milvus 的架构是什么，维护的是文件、内容还是索引？
7. 近期 Agent / Skill 技术方案做了什么，优化前后端到端耗时分别是多少？
8. 从 Plan / Action 切换到更轻量方案后，Planning / Self-healing 能力是否受损，Context 怎样处理？
9. 提速具体减少了哪些环节，怎样权衡 Efficiency 与 Stability？
10. 原 Workflow 为什么改成 Agent + Skill？
11. 多个 Skill 串联时，能否为每个阶段设置 Quality Gate，不达标时重新执行 / 修正？
12. 如果多花约 1 分钟可把准确率提高 20–30 个百分点，怎样做 Quality / Latency Trade-off？
13. 单个 Skill 与整合效果分别由谁负责，Ownership 怎样划分？
14. 动态知识、Self-healing 与 Code Self-test 是否会进一步自动化？

最终去重：Morning 曾因“同作者 + 百度三面”先保守标记 same-process merge candidate；Evening Finalize 按规则重新直接回读全部正式 `batch-01.md`～`batch-31.md` 后，未发现 `S001–S291` 中存在该候选人的百度正式 Source，也未发现当前 URL / 百度招聘流程或上述连续独特题序。9 月 21 日 / 22 日其它 `SOLDIER_627` 条目分别属于小红书、字节、度小满等不同公司，不跨公司合并。因此本条是当前库中该候选人的**百度独立招聘流程首个正式 Source**；标题虽为三面，若后续找回同一百度流程的一 / 二面，只合并回 `S295`，不再增加 Source Count。

---

## Existing-process extension — S288 蚂蚁｜9.21 二面｜不新增 ID

作者：`Decadeqqq`

二面来源：https://www.nowcoder.com/feed/main/detail/52b419448b854e24bbdf41ca9e6ffe06?sourceSSR=enterprise

去重结论：作者、公司与招聘 Timeline 明确属于 `batch-29.md / S288` 的同一蚂蚁招聘流程。本轮只把后续轮次证据合并回 `S288`，不创建 `S296` 或其它新编号。

二面新增追问深度：

1. Agent Runtime 怎样设计？
2. Knowledge Base 与 Skills 分别承载什么，怎样验证能覆盖真实业务场景？
3. Agent Read / Write Operation 分别怎样鉴权和控制风险，为什么写操作最终仍要求 User Confirmation？
4. Long-running Task 怎样用 Plan 防止 Agent 盲目调用 Tool 和丢失全局方向？
5. 如果继续做一年 AI Native 化，Roadmap 应怎样分阶段？
6. 平台怎样补齐 CLI / Skills 暴露，并把 Frontend Interaction 改造成 Agent-centric？
7. 研发、测试、验收和沟通流程怎样进一步 AI Native 化？
8. 如果业务只给 Service Goal 与 Traffic Intent，由 Agent 全托管后续操作，系统怎样设计？
9. 面向具体业务自研 Agent 与基于通用 Base Agent 做 Plugin，各有什么 Trade-off？
10. Tool / Memory / Permission Management / Agent Loop 全面 Plugin 化意味着什么？

---

# 当日最终清洗 / 明确排除

- **拼多多 `agent 一面`、星网锐捷 Agent 两轮、vivo 线下面 Agent 开发**：2026-09-22 Evening 的牛客最新流中出现了新鲜标题，均属于值得继续追的近端线索，但 direct post-specific 原帖在本轮均 Cache Miss，无法完成 Stable Original + Candidate First-person 全文核验；全部零贡献，不用标题 / 热榜补数。
- **字节 AI 全栈（飞书）**：属于 2026-09-21 已通过但 Finalize 失败的 backlog，本次恢复归入 `batch-32.md / S293`，不重复计入本日新增。
- **4399 Agent 9/18、阿里云 AI 应用、近期快手 / 腾讯等**：技术链仍有价值，但继续卡在 Stable Original / 作者 provenance 或企业聚合，零贡献。
- **Kuaishou / Shopee 等“完整答案 / 每题答案”页面、`AIGC小白入门记` 等内容链**：按答案帖 / 内容号 Gate 排除。
- **普通 Backend / Frontend / Data / Test 岗出现 Agent / Skill / AI Coding**：没有目标 Role Scope 时继续排除；术语扩散不等于目标岗位样本。
- **AI 自动面试、JD、内推、题库、聚合、Search Snippet、二次整理**：只用于发现 / 市场旁证，不贡献 HUMAN-A。

# 当日三轮监测摘要

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
- Frozen Canonical / `market/analysis/` / Curriculum：**本日不修改**。

当日主要市场信号：

1. **Knowledge Quality 正进入 Agent Backend 的真实验真链。** 百度不是只问“动态知识库如何更新”，而是追知识质量、精准加载、实际采纳、Milvus、Skill Quality Gate 与最终研发效果。
2. **Accuracy–Latency Trade-off 被要求量化。** “多约 1 分钟换 20–30pp 准确率”要求候选人把 Agent Quality 与用户 / 系统延迟放在同一决策框架里。
3. **Runtime / Permission / AI Native SDLC 继续下沉。** 蚂蚁 `S288` 二面把一面的写操作风险 / Harness / Eval 继续推进到 Runtime、读写权限、User Confirmation、Long-task Plan、CLI / Skills 暴露、AI Native 研发流程与 Plugin 化。
4. **AI Full-stack 仍然是完整软件工程底座 + AI Feature 的组合。** 度小满把 Network / OS / Go / MySQL / Redis / Frontend Foundation 与 AI-assisted Development、AI Q&A System Design 放在同一场。
5. **新鲜供给不等于可入库供给。** PDD / 星网锐捷 / vivo 的新标题说明市场仍有新增，但 Stable Original / Candidate First-person 仍是公开来源的主要瓶颈；0 个可稳定核验也比放宽 Gate 更正确。

饱和度 / 盲区：最近 72 小时牛客仍是最容易获得第一人称技术面经的平台，但最新流中 Cache Miss、企业聚合、答案化和 Role Scope 外 AI 深挖仍占很高比例。PDD Agent、星网锐捷 Agent、vivo Agent 开发、4399、阿里云 AI 应用仍值得下一轮优先追 stable original；腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米以及小红书 / 知乎 / 脉脉 / 独立技术社区仍缺更多稳定目标岗 Candidate First-person 样本。继续补盲，不降低 HUMAN-A Gate。
