# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，而是用 **HUMAN-A 真人高质量第一人称面经**校准 AI Application / Agent Engineer 的真实面试市场：公司实际问什么、追到多深、怎样验真项目，以及哪些能力要求 Coding / Debug / System Design / AI Coding。

> **完整知识体系决定应该学什么；HUMAN-A 面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**365 个**
- 来源编号：`S001–S365`
- 当前最大编号：`S365`
- 下一条正式来源：**`S366`**
- 正式 Batch：`batch-01.md` ～ `batch-23.md`
- 最新 Batch：[`interviews/batch-23.md`](interviews/batch-23.md)，新增 **5 个 HUMAN-A（S361–S365）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**热门结果页已明显局部饱和，但热门公司全年真人来源整体尚不能判定饱和。Batch 21 / 22 的完整高搜索量周期仍分别新增 11 / 12 个；Batch 23 是已有候选池的收尾批次，5 个新增不能单独视为饱和信号。**

Batch 23 在编号前重新直接回读 `batch-01.md` ～ `batch-22.md`，覆盖 `S001–S360` 全历史。最终只保留 5 个独立招聘流程：字节中国交易与广告完整三轮 + HR/Offer、快手 AI 应用服务端三轮、小红书 PE 全栈 AI 方向、小红书 PE 工程师 AI+全栈方向、字节抖音电商 / 中国交易与广告 AI 开发/全栈。

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

平台一视同仁。牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客与独立站都执行同一 Gate；平台只影响核验难度，不影响准入门槛。

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

岗位标题不是唯一依据。标题叫 Backend，只要实际职责和整场面试主体明确围绕 Agent / RAG / LLM Service / Runtime，可以进入；反之，普通 Backend 仅深挖候选人的 Agent 项目、但岗位本身无法确认属于目标方向时，不收。

Batch 23 的典型案例：字节 `S361` 虽为后端日常实习，但一、二面主体持续围绕 Agent / Harness / Skill / Memory / Evaluation，因此通过；另一个 8/23 字节页面虽 Agent 项目问得多，但岗位 Role Scope 无法稳定确认，因此排除。

---

## 4. 通过 Role Scope 后，整场技术问题全部保留

确认是一场目标 AI 岗 HUMAN-A 后，真实出现的基础和 AI 技术问题都保留：

```text
Python / FastAPI / ASGI / asyncio
Java / Spring / Go
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

不使用普通 Backend、数据分析、推荐 / 广告算法等 Role Scope 外场次人为抬高基础题频率。

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
- 同一候选人不同公司、招聘流程独立时可以分别计数；
- 不同 URL 但题序 / 项目语义高度一致时必须继续追源；
- 无法确认复制链原始候选人时整链排除；
- 搜索摘要只负责发现，正文最终不能稳定打开则零贡献；
- 不同候选人的独立流程即使出现相同常见问题，仍分别计数。

Batch 23 中，字节 `S361` 的三轮和快手 `S362` 的三轮均通过作者 Timeline 合并；快手父子索引 / BM25 / Rerank 多日期高度同序链继续排除；热门公司投稿 / 答案包装和内容账号仍零贡献。

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
技术关键词
×
作者 Timeline / 原始正文
```

热门公司优先：字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等。

时间线继续双跑：

- **最新层：2026-08～09**，追秋招新增和后续轮次；
- **补漏层：2026-03～07**，深扫热门公司历史长尾。

岗位别名：AI 应用开发、AI 应用研发、Agent 开发、智能体开发、大模型应用、LLM Application、RAG、AI Backend、Agent Backend、AI Full-stack、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

搜索不能停在结果页：

```text
搜索引擎 / 企业页 / 话题页
→ 精确公司 + 岗位 + 日期 / 轮次
→ 作者主页 / 候选人 Timeline
→ 原始正文 / 评论区
→ 跨页面复制关系
→ 全历史 Batch 最终去重
```

---

## 7. 当前饱和度判断

1. **最新热门结果页局部饱和已经较明确。** 8～9 月泛搜中历史重复、内容账号、答案版、后发扩写和 Role Scope 模糊结果越来越多。
2. **热门公司全年来源尚未整体饱和。** Batch 21 / 22 在扩大 Recall 后仍分别新增 11 / 12 个，主要来自 3～7 月长尾与作者 Timeline。
3. **Batch 23 的 5 个不作为独立饱和证据。** 该批是在已有候选池基础上做收尾，不是完整新一轮高搜索量实验。
4. **去重 / Provenance 成本高于搜索成本。** 新 URL 很多，但真正需要验证的是作者、流程、原始正文和罕见题序。
5. **下一轮继续扩量搜索。** 只有当最新层、3～7 月长尾、作者 Timeline 三条路径连续多轮都出现明显低新增，才判断热门公司 HUMAN-A 接近饱和。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-22.md
│   └── batch-23.md
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

- 从 **`S366`** 开始；
- 继续保持 Batch 21 / 22 的高搜索量，不因 Batch 23 只有 5 个就降低 Recall；
- 热门公司优先，尤其继续深挖腾讯、字节 / 抖音、美团、快手、小红书、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及百度 / 阿里 / 蚂蚁历史长尾；
- 最新 8～9 月与 3～7 月长尾同时搜索；
- 优先沿已核验真人作者 Timeline 找同公司后续轮次与不同公司独立流程；
- 继续重点观察 Agent Runtime Verification、Context / Memory Correctness、RAG Evaluation、AI Coding Verification、Harness / AgentOS；
- 继续补 Java / Python / FastAPI / Go / MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
- 内容账号、投稿 / 答案、付费墙、后发扩写、同作者流程不清、换公司标题同序链继续零容忍；
- 分配编号前再次直接回读 `S001–S365` 全历史。