# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，而是用 **HUMAN-A 真人高质量第一人称面经**校准 AI Application / Agent Engineer 的真实面试市场：公司实际问什么、追到多深、怎样验真项目，以及哪些能力要求 Coding / Debug / System Design / AI Coding。

> **完整知识体系决定应该学什么；HUMAN-A 面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**373 个**
- 来源编号：`S001–S373`
- 当前最大编号：`S373`
- 下一条正式来源：**`S374`**
- 正式 Batch：`batch-01.md` ～ `batch-25.md`
- 最新 Batch：[`interviews/batch-25.md`](interviews/batch-25.md)，新增 **4 个 HUMAN-A（S370–S373）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**热门结果页局部饱和进一步加强，但热门公司全年真人来源仍不能判定整体饱和。Batch 24 / 25 两轮完整扫描都只新增 4 个，新增边际明显下降；但 Batch 25 的 4 条全部来自 3～6 月长尾，并且作者 Timeline 仍能挖出此前未收录的大厂独立流程。因此当前更准确的判断是“8～9 月热门结果层高度饱和，历史长尾尚有残余增量，Provenance / 去重已成为主要成本”。**

Batch 25 在编号前重新直接回读 `batch-01.md` ～ `batch-24.md`，覆盖 `S001–S369` 全历史，并主动把平台搜索扩展到小红书、知乎、脉脉、个人博客、独立站和技术社区。最终只保留 4 个独立招聘流程：字节中国交易与广告·生活服务 Agent 工程师池、阿里千问 Agent 开发、腾讯 AI 后台开发、京东科技 AI 全栈 Agent 研发。非牛客平台本轮零新增不是平台配额不足，而是原文稳定性、作者归属、复制链或内容账号 Gate 未通过。

---

## 2. 唯一正式来源标准：HUMAN-A

正式来源必须同时满足：

```text
真人面试官
+
候选人本人第一人称
+
高信息密度
+
真实现场 / 招聘流程痕迹
+
目标 AI Application / Agent 岗位
+
正文稳定可核验
+
非转载 / 非合集 / 非内容账号 / 非答案帖 / 非重复
=
HUMAN-A
```

详细规则：

- [`quality/source-quality-policy.md`](quality/source-quality-policy.md)
- [`quality/role-scope-policy.md`](quality/role-scope-policy.md)

**平台一视同仁且主动多平台搜索。** 牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客、独立站与技术社区都属于搜索面；平台只影响核验难度，不影响准入标准，也不存在平台配额。搜索索引、二次转载和 Search Snippet 只用于找到原始 HUMAN-A，不能单独贡献题目。

---

## 3. Role Scope

核心研究方向：

```text
AI 应用开发 / AI 应用研发
Agent / 智能体开发
大模型 / LLM Application
RAG / 知识库应用
AI Backend / Agent Backend
AI Full-stack
Agent Harness / Agent Runtime
Coding Agent
Applied AI Engineer / FDE
AI-Native Application Engineer
```

岗位标题不是唯一依据。标题叫 Backend，只要岗位职责和整场招聘流程明确属于 Agent / RAG / LLM Service / Runtime，可以进入；反之，普通 Backend 只顺带问候选人的 Agent 项目、但岗位本身无法确认属于目标方向时，不收。

Batch 25 给出了两个新的边界案例：`S370` 的候选人是前端画像，但招聘方明确说明前端 / 后端 / 客户端统一进入 Agent 工程师池，再按简历技术栈提问，因此 React / JS 真实问题全部保留；`S372` 标题明确为腾讯 AI 后台开发，即使整场主要考 Redis / MySQL / JVM / TCP，仍属于目标 AI Backend 的真实工程底座样本。

---

## 4. 通过 Role Scope 后，整场技术问题全部保留

确认是一场目标 AI 岗 HUMAN-A 后，真实出现的基础和 AI 技术问题都保留：

```text
Python / FastAPI / ASGI / asyncio
Java / Spring / Go / JavaScript / React
MySQL / Redis / Vector Database
LLM Foundation / RAG
Agent / MCP / Skill / Tool / Memory
Agent Harness / Runtime
System Design
OS / Network / Concurrency
MQ / Kafka
HTTP / SSE / WebSocket
Coding / Debug / Security / Evaluation
AI Coding
```

不使用普通 Backend、普通 Frontend、数据分析、推荐 / 广告算法等 Role Scope 外场次人为抬高基础题频率；但目标 Agent / AI Backend 场次真实考到的前后端基础必须原样保留。

---

## 5. 去重：必须在分配 `Sxxx` 前完成

固定执行：

```text
全部历史 Batch 直接回读
+
URL 精确去重
+
公司 / 岗位 / 日期 / 轮次比对
+
题序 / 项目语义去重
+
作者 / 招聘流程 Timeline 去重
+
外部原帖 / 后发复制链核验
```

强制规则：

- GitHub Code Search / 搜索引擎“0 命中”只能辅助，不能证明未收录；
- 每个候选至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特连续题序；
- 同一候选人同一公司同一招聘流程的一面 / 二面 / 三面 / Leader 面必须合并为一个 `Sxxx`；
- 同一候选人不同公司 / BU、招聘流程独立时可以分别计数；
- 不同 URL、不同平台但题序 / 项目语义高度一致时必须继续追源；
- 无法确认复制链原始候选人时整链排除；
- 搜索摘要、公开索引只负责发现，正文最终不能稳定打开则零贡献；
- 不同候选人的独立流程即使出现相同常见问题，仍分别计数。

Batch 25 的典型去重：同一真实候选人 `lazy_learner` 的 4/6 腾讯 AI 后端短帖看似满足公司 / 岗位 / 第一人称，但“慢查询 → Redis 为什么快 → 缓存雪崩导致服务宕机 → 几十亿 int 去重”的罕见连续题序可追到 2025 年另一作者的腾讯 IEG 后端面经，因此该短帖零贡献；同作者 4/2 的腾讯 AI 后台长复盘则单独完成来源链核验、未发现更早复制源后作为 `S372` 收录。跨平台也使用同一标准：小红书索引中与历史 `S095` 同序的“淘天 AI Agent 一面问麻了”不因换平台而新增。

---

## 6. 搜索策略

持续执行：

```text
热门公司优先
×
岗位别名
×
最新月份 + 历史长尾
×
多平台主动召回
×
技术关键词
×
作者 Timeline / 原始正文
```

热门公司优先：字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等。

时间线继续双跑：

- **最新层：2026-08～09**，追秋招新增和后续轮次；
- **补漏层：2026-03～07**，深扫热门公司历史长尾。

平台层主动搜索：牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、博客园、掘金、个人博客、独立站、公开技术社区等。**平台覆盖是 Recall 策略，不是收录配额。**

岗位别名：AI 应用开发、AI 应用研发、Agent 开发、智能体开发、大模型应用、LLM Application、RAG、AI Backend、Agent Backend、AI Full-stack、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

搜索不能停在结果页：

```text
搜索引擎 / 企业页 / 话题页 / 平台索引
→ 精确公司 + 岗位 + 日期 / 轮次
→ 作者主页 / 候选人 Timeline
→ 原始正文 / 评论区
→ 跨平台复制关系
→ 全历史 Batch 最终去重
```

---

## 7. 当前饱和度判断

1. **8～9 月热门结果层已高度局部饱和。** 本轮最新层继续大量命中历史来源、内容账号、答案包装、同场多 URL、付费墙和 Role Scope 模糊内容。
2. **3～7 月历史长尾仍有残余增量。** Batch 25 的 `S370–S373` 全部来自 3～6 月，说明热门公司的全年真人来源尚未完全挖尽。
3. **新增边际下降已经形成连续信号。** Batch 21 / 22 分别新增 11 / 12 个，Batch 23 为候选池收尾新增 5 个，Batch 24 / 25 两轮完整扫描都只新增 4 个。还不能据此单独宣布全年饱和，但应继续观察下一轮。
4. **Provenance / 去重成本明显高于搜索成本。** 新页面数量仍多，但真正独立的候选人流程越来越少；跨平台镜像和跨年份复制链进一步增加核验成本。
5. **非牛客平台目前的主要瓶颈是可验证性，而不是不搜索。** 小红书常见原文访问 / 稳定 URL 问题，知乎 / 脉脉 / 博客搜索结果则更容易落到题库、职业内容和二次整理；只有原始候选人正文真正通过 Gate 才会进入正式库。
6. **下一轮继续高 Recall，但搜索重心进一步向 Timeline / 长尾迁移。** 如果最新层、3～7 月长尾、作者 Timeline、非牛客原文四条路径连续多轮都低新增，才判断热门公司 HUMAN-A 接近饱和。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-24.md
│   └── batch-25.md
├── monitoring/
│   └── inbox.md
├── quality/
│   ├── source-quality-policy.md
│   └── role-scope-policy.md
└── questions/
    └── README.md
```

`interviews/` 是正式 HUMAN-A；`monitoring/inbox.md` 只保存已经满足 HUMAN-A、但尚未归入正式 Batch 的候选。普通线索、低质量帖子和待核验摘要不进入 Inbox。

Canonical Question 只允许由正式 HUMAN-A 产生证据。

---

## 9. 下一轮优先级

- 从 **`S374`** 开始；
- 继续高搜索量，不因 Batch 24 / 25 连续只有 4 个就降低 HUMAN-A 门槛；
- 热门公司优先，尤其继续深挖腾讯、字节 / 抖音、美团、快手、小红书、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及百度 / 阿里 / 蚂蚁历史长尾；
- 最新 8～9 月与 3～7 月长尾同时搜索，但增加 3～6 月和作者 Timeline 的预算；
- 继续主动搜索小红书、知乎、脉脉、个人博客、独立站等非牛客平台，优先寻找可稳定打开的候选人原帖，不接受平台索引替代原文；
- 优先沿已核验真人作者 Timeline 找同公司后续轮次与不同公司 / BU 的独立招聘流程；
- 继续重点观察 Agent Runtime Verification、Context / Memory Correctness、RAG Evaluation、AI Coding Verification、Harness / AgentOS、Tool Discovery / Context Control；
- 继续补 Java / Python / Go / JavaScript / React / FastAPI / MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
- 内容账号、投稿 / 答案、付费墙、后发扩写、同作者流程不清、跨平台同序链继续零容忍；
- 特别警惕“作者是真人但单篇内容是复制”的情况，分配编号前再次直接回读 `S001–S373` 全历史并做跨年份题序检索。
