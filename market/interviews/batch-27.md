# Batch 27 — 2026-09-16 Daily HUMAN-A Continuous Monitoring

采集日期：2026-09-16

> 本批是持续监测恢复后的第一个正式日批次。当天 10:00 / 17:00 / 22:00 三次检索合并为一个 Batch；主动发现窗口为运行时最近 3 天，但正式归档前重新直接回读 `batch-01.md`～`batch-26.md` 全历史执行去重。
>
> 本批正式新增 **7 个 HUMAN-A 独立招聘流程：`S280–S286`**。新来源先进入 Research 证据层；Canonical / Curriculum 不因单日新增自动调整。

---

## S280 美团｜AI 后端｜一面 + 二面（同一候选人同流程合并）｜2026-09｜HUMAN-A

作者：`SOLDIER_627`

一面来源：https://api-cdn.nowcoder.com/discuss/927579574932705280?sourceSSR=post

二面来源：https://www.nowcoder.com/discuss/929087871779110912

真人 / 第一人称证据：作者长期记录本人求职 Timeline；一面约 76 分钟、二面约 59 分钟，两轮围绕同一美团 AI 后端招聘流程连续推进，并保留项目答题状态、架构讨论和后续轮次信息。作者历史还存在快手 AI 全栈流程，但公司和招聘流程不同，不能跨公司合并。

补充作者账号：小红书 `63044ffc0000000012000359`（Soldier），与既有牛客SOLDIER_627同场题序、项目和76/59分钟完全对应。

### 一面完整题序（跨平台同场补核）

补核时间：2026-10-07 UTC（北京时间10-08），属10-07采集任务第二轮遗漏复查。
补充来源：https://www.xiaohongshu.com/explore/6aa2579b0000000029014c80

时间线：面试日未披露；发布/编辑显示：09-10 上海。只有发布月日，未给面试日/年份；不补日期

本人及流程依据：精确净时长76min；具体项目逐层追问路由、分层取证、评测收益、上传回调幂等；作者归属沿用父代理已核S280

记录边界：原号与无编号段序按原帖保留；背景/反问/未披露占位不等于新技术题。

### 一面｜1

1. （原题1(1)）自我介绍

### 一面｜2

1. （原题2(1)）故障诊断Skill项目解决的问题与目标
2. （原题2(2)）Skill是否基于开源项目
3. （原题2(3)）数万历史工单如何分领域；是否聚类；场景划分是否产品推动
4. （原题2(4)）Skill错误路由或幻觉如何识别和兜底
5. （原题2(5)）渐进开放工具外，执行/输出后还有什么校验和门禁
6. （原题2(6)）分层取证如何分层及逐层进出
7. （原题2(7)）项目卡点难点及解决过程
8. （原题2(8)）项目如何评测；具体指标和内部收益
9. （原题2(9)）被动诊断改成主动发现问题如何设计

### 一面｜3

1. （原题3(1)）多模态视频检索平台目标及本人角色
2. （原题3(2)）视频分片上传/断点续传；同分片重复上传怎么办
3. （原题3(3)）后端MySQL表结构设计
4. （原题3(4)）多使用方隔离与存量迁移方案
5. （原题3(5)）Go后端与算法端的超时/事件流转/异常；同任务重复回调怎么办
6. （原题3(6)）线上规模、最大吞吐、单任务耗时；还能否更快
7. （原题3(7)）上线反馈与收益
8. （原题3(8)）是否调研开源或业界同类方案
9. （原题3(9)）项目卡点及解决过程

### 一面｜4

1. （原题4(1)）RAG完整链路；文本块大小如何选择
2. （原题4(2)）回复差或答非所问如何区分检索问题与生成问题

### 一面｜5

1. （原题5(1)）Agent与Workflow区别及适用场景
2. （原题5(2)）如何保证工具调用安全；是否开放全部工具
3. （原题5(3)）如何理解Agent Harness
4. （原题5(4)）使用Codex/Claude时是否用过Hooks等特性

### 一面｜6

1. （原题6(1)）Java接入Agent含鉴权、参数、调用、流式结果、回调和落库，适合什么设计模式
2. （原题6(2)）高QPS本地缓存/Redis/DB架构中，DB更新后如何更新两级缓存

### 一面｜7

1. （原题7(1)）Java线程池核心参数与拒绝策略
2. （原题7(2)）常见GC及大致原理

### 一面｜8

1. （原题8(1)）AI工作或项目有哪些经验与踩坑；一个大项目如何做下来

### 一面｜9

1. （原题9(1)）手写二叉树层序遍历

### 二面完整题序（跨平台同场补核）

补核时间：2026-10-07 UTC（北京时间10-08），属10-07采集任务第二轮遗漏复查。
补充来源：https://www.xiaohongshu.com/explore/6aa7d40b000000002601b231

时间线：面试日未披露；发布/编辑显示：09-14 上海。只有发布月日，未给面试日/年份；不补日期

本人及流程依据：净时长59min，沿同一Skill项目追问改造收益、路由冲突、自然语言测试和故障注入；作者归属沿用父代理S280核验

记录边界：原号与无编号段序按原帖保留；背景/反问/未披露占位不等于新技术题。

### 二面｜1

1. （原题1(1)）自我介绍

### 二面｜2

1. （原题2(1)）上段实习独立还是团队开发；本人职责
2. （原题2(2)）原固定Workflow如何运作
3. （原题2(3)）Skill比Workflow优势；如何降低维护成本

### 二面｜3

1. （原题3(1)）多Skill如何路由正确
2. （原题3(2)）同产品多个Skill如何解决路由冲突
3. （原题3(3)）Skill增加时如何提高路由准确率
4. （原题3(4)）Skill增多造成上下文膨胀如何处理

### 二面｜4

1. （原题4(1)）Skill开发主要挑战
2. （原题4(2)）自然语言Skill与确定性代码的测试/调试差异
3. （原题4(3)）是否回放历史问题或注入已知故障验证端到端效果

### 二面｜5

1. （原题5(1)）Skill使用什么模型、Harness及执行框架
2. （原题5(2)）是否了解PI Agent或DeepSeek Harness
3. （原题5(3)）Agent Loop何时终止

### 二面｜6

1. （原题6(1)）是否还亲自写代码；最近手写何时
2. （原题6(2)）如何看待仅用AI而不手写代码
3. （原题6(3)）AI产码超过人工Review速度时怎么办
4. （原题6(4)）长期应重视代码审美还是操控Agent
5. （原题6(5)）实习中传统编程/代码审美具体提升及例子

### 二面｜7

1. （原题7(1)）云服务器产品及核心能力
2. （原题7(2)）裸金属提供虚拟化还是直接交付物理机
3. （原题7(3)）云服务器Region级与AZ级容灾

### 二面｜8

1. （原题8(1)）数组与整数K：统计和为K的连续子数组数

### 二面｜9

1. （原题9(1)）AI快速发展对后端岗位和职业的影响
2. （原题9(2)）安全/架构经验被AI内化后，资深工程师经验是否仍有价值

去重：晚间最终归档前再次直接回读全部历史 Batch；同作者历史快手流程属于另一家公司独立招聘流程。美团一 / 二面属于同候选人同公司同流程，因此合并为一个 `S280`，不按轮次虚增。

---

## S281 科大讯飞｜Agent 研发工程师 · Harness 方向｜线下一面 + 二面 + HR｜2026-09-11｜HUMAN-A

作者：`Tale2229`

来源：https://www.nowcoder.com/feed/main/detail/671d2fa1d7c04322837ee1f5788dd69d

真人 / 第一人称证据：作者记录从北京到武汉参加线下面试，半天连续一面、二面和 HR；一面多道基础题答不上时明确记录自己的判断和状态，随后意外进入二面，最终继续记录等待结果。招聘现场和时间线完整。

代表性技术链：

1. 即时通信 / 多节点消息处理架构怎样设计？
2. Agent 项目真实解决什么问题，本人做了哪些核心实现？
3. Short-term / Long-term Memory 怎样分层？
4. Knowledge Base 增量更新如何保证新鲜度和旧索引失效？
5. Agent Loop / Harness 分别承担哪些职责？
6. LangGraph Node / State 怎样设计？
7. AI Coding 在真实项目中的参与度如何证明，生成代码由谁验证？
8. IPC 有哪些常见方式，Process / Thread / User-Kernel 边界怎样理解？
9. Deadlock / RWLock 怎样分析？
10. AVL 与 Red-Black Tree 如何比较？
11. Memory Fragmentation 怎样产生和治理？
12. 现场算法与传统基础能力如何和 Agent 工程同场考察？

去重：历史科大讯飞 `S178 / S179` 为不同作者、不同月份、不同项目和题序；当前流程独立。

---

## S282 快手｜AI 全栈｜秋招一面｜发布 2026-09-15｜HUMAN-A

作者：`明天会有好天气`

来源：https://www.nowcoder.com/feed/main/detail/60d833cbae7f4a668a0bed9e18a428f1

真人 / 第一人称证据：岗位标题明确 AI 全栈；作者按本人秋招流程发布，并保留“很多八股说不上来”等现场状态。整场不是只问 AI 名词，而是把 Backend Foundation 与 AI Coding 生产实践混合考察。

代表性技术链：

1. 实习项目真实负责什么？
2. MySQL `INSERT` 的执行链路是什么？
3. redo log / binlog 两阶段提交为什么需要？
4. JVM GC / ZGC 的基本机制和适用边界是什么？
5. Slow SQL 怎样定位与优化？
6. 日常 AI Coding Workflow 怎样组织？
7. 上线代码由 AI 生成 / 修改后遗漏 Bad Case，怎样发现、回滚、补测试并避免复发？
8. Java Object Creation 过程怎样理解？
9. Repeatable Read 与 MVCC / Lock 的关系是什么？
10. Coding：最大岛屿面积等现场算法。

去重：全历史未发现当前 URL、作者和“Backend Foundation → AI Coding Production Bad Case”连续流程的同场来源；历史快手 AI 全栈 / Agent 来源均为其他候选人或不同流程。

---

## S283 美团｜AI Agent｜一面｜发布 2026-09-15｜HUMAN-A

作者：`会收到的打工人`

来源：https://www.nowcoder.com/feed/main/detail/50bcdc47e7754aa7be59b6318fea514b?sourceSSR=subject

真人 / 第一人称证据：作者为个人求职账号，明确记录本人一面；问题沿一个 Agent 项目持续深挖，具有自然的“项目 → Failure → Framework / Runtime → Knowledge”追问结构，而非分类题库。

代表性技术链：

1. Agent 项目的业务背景、实际落地和结果是什么？
2. Long Agent Flow 怎样保证每一步按预期执行？
3. Long-task Hallucination 怎样检测和抑制？
4. “置信度”怎样定义，什么场景必须二次向用户确认？
5. Multi-Agent Context Bloat 怎样治理？
6. LangChain / LangGraph / Raw Agent 怎样取舍？
7. 为什么需要 / 不需要手写 Agent Runtime？
8. Knowledge Base 怎样设计？
9. 产品持续更新后，知识怎样保持 Freshness 与 Accuracy？

去重：与当天其他美团候选人为不同作者、不同项目与独立招聘流程；全历史未发现同 URL / 作者 / 连续题序。

---

## S284 美团｜AI 后端开发工程师｜一面｜发布 2026-09-15｜HUMAN-A

作者：`纯牛马🐮🐴`

来源：https://www.nowcoder.com/feed/main/detail/b3b11822cef24f689c9600e4415f4043

真人 / 第一人称证据：作者记录“周四面完、周一挂”、多个问题不会 / 蒙数字、手撕未完成等现场状态；同日还有本人其它公司面试与求职状态。反问确认团队属于小象超市物流供应链，实际工作是传统 Backend + Agent，符合 AI Backend Role Scope。

代表性技术链：

1. AI 题目 / Agent 方案如何设计？
2. 图像编辑模型怎样调研和比较？
3. Elo Model Evaluation 怎样做 Pairwise Comparison？
4. Prompt Test Set 多大才有代表性，怎样构建和回归？
5. On-call Agent 的 Context / Memory 怎样设计？
6. Context Compression 为什么在约 80% 占用时触发，阈值依据是什么？
7. Redis Cluster / Cache Selection 怎样按业务负载选型？
8. 商品图片 URL 自动刷新怎样设计 Cache / Consistency？
9. MySQL Isolation / Join 怎样理解？
10. Integer Reverse Overflow 与 SQL Coding 等现场题。

去重：全历史未出现当前 URL、作者和“Elo → Prompt Test Set → Context Compression 参数验真 → Redis Cache Refresh”连续题序。

---

## S285 智谱｜AI Native Builder 实习｜一面｜发布 2026-09-16｜HUMAN-A

作者：`牛客671002402号`

来源：https://www.nowcoder.com/discuss/929419257438302208?sourceSSR=%E5%85%B6%E4%BB%96

真人 / 第一人称证据：除了技术题，面试中还出现出生年份、住址、研究生论文压力、可实习时长等强招聘现场信息；项目追问持续到 Architecture、团队分工和本人负责边界，符合候选人本人第一人称技术面。

代表性技术链：

1. 怎样理解 AI Native Builder 岗位？
2. 日常使用哪些 AI Development Tool，怎样判断真正提效？
3. 最深项目的工期、Architecture、Team Ownership 和本人责任是什么？
4. Quality Data System 怎样设计？
5. Intent Recognition / Routing 怎样实现？
6. 如果用户让 Agent 导出所有供应商和员工敏感数据，怎样阻止 Data Exfiltration？
7. Service Crash / Restart 后长任务和状态怎样恢复？
8. 10 万人抢 100 张票怎样设计高并发系统？
9. Anti-bot 怎样做？
10. Redis Power-loss 后数据 / 业务怎样恢复？
11. 给传统课程平台增加 AI Teaching Assistant，什么条件下才算真正 AI Native？

去重：全历史未发现当前 URL、作者、智谱流程和“Agent Data Exfiltration → Restart Recovery → 秒杀 / Anti-bot → AI Native 产品判断”题序。

---

## S286 小红书｜AI 应用研发（社区搜索 / Agent）｜一面｜面试 / 发布 2026-09-15｜HUMAN-A

作者：`Florentino_73`

来源：https://www.nowcoder.com/discuss/929475914579136512?sourceSSR=post&weFlow=true

真人 / 第一人称证据：作者有长期个人求职记录；本场按 `5min 自我介绍 → 30min 项目深挖 → 20min 手撕 → 反问业务` 记录，反问明确岗位主要做社区搜索 Agent，招聘现场与 Role Scope 清晰。

代表性技术链：

1. 金融 Agent 的完整 Architecture / 使用场景是什么？
2. RAG Evaluation 怎样做？
3. 项目最大的工程难点是什么，如何验证解决？
4. 日常怎样使用 AI Tool？
5. 最近关注哪些 AI Frontier，怎样判断是否值得引入？
6. 什么是 Good Skill，设计 Skill 时需要哪些约束？
7. Claude Code CLI 怎样使用，为什么不是“会用工具”就够？
8. 蚂蚁实习的具体工作与本人 Contribution 是什么？
9. 为什么需要 Agent Group Chat，是否真正落地，而不是 Demo？
10. Coding：平方根结果保留两位小数。
11. 反问：社区搜索 Agent 的真实业务与技术方向。

去重：全历史未出现当前 URL、作者的小红书流程和连续题序；作者本人身份可由长期求职 Timeline 支持，非批量内容账号。

---

# 当日最终清洗 / 明确排除

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

# Batch 27 市场观察

1. **Skill / Harness 已从概念题进入 Production Control。** Routing Conflict、Progressive Tool Gate、Case Replay / Fault Injection、Loop Stop、Context Bloat 和 Harness 选型开始连续出现。
2. **Agent Reliability 正从“防幻觉”走向确定性门禁。** 置信度、二次用户确认、敏感写操作、数据导出限制、Restart Recovery 都要求明确的 Runtime / Permission Boundary。
3. **Evaluation 开始验参数而不是验名词。** Elo 怎样比较、Prompt Test Set 多大、Context 为什么 80% 压缩、Offline Case 是否代表线上故障，都要求解释实验依据。
4. **AI Coding 已进入 Production Verification。** 面试官关心 Bad Case 漏检、Review Bottleneck、真实落地和人类 Review / Test，而不是只问使用了哪个工具。
5. **Backend / OS / System Design 仍是目标岗位硬能力。** MySQL、Redis、GC、IPC、Lock、秒杀、Anti-bot、Recovery 与 Agent / RAG 同场出现。
6. **Provenance 成本高于搜索成本。** 最近结果里“题很强但原帖不稳、内容账号、聚合页、同候选人后续轮次”的比例很高；持续维护必须继续接受 0 新增或少新增，而不能用漂亮题目替代 HUMAN-A。

# Canonical / Curriculum 处理

- `S280–S286` 本批先作为 Research Evidence 正式入库；
- 明确能映射现有 Canonical 的问题在后续 periodic review 中统一处理；
- 本批出现的 Skill / Harness Reliability、Agent Security、Evaluation Parameter Proof 等信号暂时只记录趋势；
- **本批不新增 Canonical，不修改 Curriculum。**
