# Batch 33 一手面试流程

采集日期：2026-09-22

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

### 二面补充（44分钟，不新增Source）

补核时间：2026-10-07 UTC（北京时间10-08），属10-07采集任务第二轮遗漏复查。
补充来源：https://www.xiaohongshu.com/explore/6ab24065000000003401ba1f

时间线：面试日未披露；发布/编辑显示：09-22 上海。只有发布月日，未给面试日/年份；不补日期

本人及流程依据：净时长44min；对个人职责与Skill/平台贡献划界，中断状态恢复、先验控制和产后验收有连续换问法；沿用既有S294本人核验

记录边界：原号与无编号段序按原帖保留；背景/反问/未披露占位不等于新技术题。

### 二面｜1

1. （原题1(1)）简短自我介绍

### 二面｜2

1. （原题2(1)）故障定位完整链路及本人负责/投入部分
2. （原题2(2)）Workflow转Skill后准确性及两者优劣
3. （原题2(3)）所需Agent/MCP架构具体段落；能力来自定位平台、云服务还是现成平台；自己做Agent/MCP还是只供Skill

### 二面｜3

1. （原题3(1)）Agent编排；Plan/ReAct/LangGraph为现成技术还是自研
2. （原题3(2)）问题定位单次执行还是多轮对话
3. （原题3(3)）为何要用户授权；中断后如何继续、存哪些状态；Agent是否自行记录状态

### 二面｜4

1. （原题4(1)）简历中最擅长哪些语言和中间件
2. （原题4(2)）实习是否使用MySQL

### 二面｜5

1. （原题5(1)）MySQL索引优化、慢查询处理及索引注意事项
2. （原题5(2)）MySQL和Redis一致性常用方案
3. （原题5(3)）实际工作采用哪种一致性方案

### 二面｜6

1. （原题6(1)）一次HTTP请求的执行链路
2. （原题6(2)）简历网关路由中网关的主要作用
3. （原题6(3)）网关最主要的功能

### 二面｜7

1. （原题7(1)）Codex等AI工具开发如何确保正确性；生成后如何验收
2. （原题7(2)）换问法：AI开始前做什么提高输出正确性及可控性
3. （原题7(3)）当前AI Coding问题及本人踩坑

### 二面｜8

1. （原题8(1)）介绍刚才未问而自己擅长的组件或能力
2. （原题8(2)）Skill/项目代码提交规模；是否全由AI编写
3. （原题8(3)）AI Coding、手写、算法和协作中哪个最强

最终去重：在本轮编号前已直接回读正式 `batch-01.md`～`batch-31.md` 全历史，并与本次恢复的 `batch-32.md` 候选交叉核验。未发现度小满同公司 / 同招聘流程、当前 URL，或“Browser / Network → OS / GMP → MySQL / Redis → Frontend Foundation → AI-assisted Development → AI Q&A System Design → Restore IP”的历史同场来源。同作者不同公司按独立招聘流程分别计数。

---

## S295 百度｜Agent 后端｜三面｜发布 2026-09-22 09:13｜HUMAN-A

作者：`SOLDIER_627`

来源：https://www.nowcoder.com/discuss/931476137576845312

真人 / 第一人称证据：post-specific 原帖稳定可直接回读，作者记录本人三面，净时长约 42 分钟；面试官开场先介绍团队业务，再由候选人围绕方案提问，随后继续深挖候选人近期 Agent / Skill 经历和技术 Trade-off，招聘现场与互动结构明确。作者 Candidate Timeline 连续稳定。

Role Scope：面试官明确介绍团队主要做内部 AI 研发提效平台，让 AI 参与需求开发与落地，涉及 Agent Orchestration、Workflow Optimization、本地 / 云端开发；另一主线是动态知识库，用 AI 自动采集、更新和治理研发知识，再反哺 Code Generation / Testing。属于直接目标 Agent Backend / AI Application 范围。

### 一面、二面补充（同流程，不新增Source）

补核时间：2026-10-07 UTC（北京时间10-08），属10-07采集任务第二轮遗漏复查。
补充来源：https://www.nowcoder.com/discuss/924730985210458112
补充来源：https://www.nowcoder.com/discuss/929431883266424832

时间线：09-02一面；09-15二面；发布/编辑显示：一面09-11 10:53编辑；二面09-30 14:50编辑。原页只显月日；若归入2026仅为当前站内日期显示/个人时间线的推断，非独立印出的年份。发帖或编辑日不等于面试日。

本人及流程依据：同ID的百度一二三面连续9/2、9/15、9/21，45/27/42分钟；原帖本人项目与追问一致。

记录边界：原号与无编号段序按原帖保留；背景/反问/未披露占位不等于新技术题。

### 一面

1. （原题1）自我介绍
2. （原题2）迁移前Workflow形态，节点是Prompt还是代码
3. （原题3）Skill核心能力与整体流程
4. （原题4）Skill背后MCP的用途
5. （原题5）只诊断还是直接自动修复故障
6. （原题6，拆分追问a）Agent所用模型
7. （原题6，拆分追问b）是否有用户上传截图等多模态场景
8. （原题7）Skill是否承载流程、规则、授权点和输出报告定义
9. （原题8）对比国内外开源Skill、组件或方案的调研
10. （原题9，拆分追问a）MCP调用的详细步骤
11. （原题9，拆分追问b）谁发起、谁执行调用
12. （原题9，拆分追问c）模型、Agent、Client与Server如何分工
13. （原题10）Agent上下文构成
14. （原题11，拆分追问a）上下文过大怎样继续多轮对话
15. （原题11，拆分追问b）上下文过长的常见处理策略
16. （原题12，拆分追问a）压缩时是否区别对待各种内容
17. （原题12，拆分追问b）具体压缩方式
18. （原题13）OpenCode、Claude Code、Codex、DeepSeek上下文机制的区别（保留原帖分类）
19. （原题14）当前Skill是否使用Memory或外部知识
20. （原题15，拆分追问a）Memory检索与更新设计
21. （原题15，拆分追问b）用户从北京迁居上海，如何更新旧居住信息
22. （原题16）手撕最长回文子串

### 二面

1. （原题1）自我介绍
2. （原题2.1）故障诊断实习背景、使用场景和本人工作
3. （原题2.2）为什么诊断逻辑用Skill而非确定性服务
4. （原题2.3）已有Workflow为何改为Skill
5. （原题2.4）同Skill多次或跨模型执行如何保证稳定，失败实例及处理
6. （原题2.5）项目原有基础、本人定位和范围
7. （原题2.6）Skill诊断成功率和失败率等量化效果
8. （原题2.7）当前诊断故障耗时
9. （原题2.8）提速约三分之一减少了哪些步骤
10. （原题2.9）取消Plan/中间派发是否损伤成功率和质量，怎样评测
11. （原题2.10）模型调用和Token优化
12. （原题3.1）另一实习的视频分析处理人脸还是行为识别
13. （原题4.1）Java线程池工作流程
14. （原题4.2）线程池大小设计
15. （原题5.1）MySQL索引失效的常见场景

### 三面（既有完整技术链）

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

